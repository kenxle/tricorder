import type { PythonAPI } from "@tricorder/schema/api";
import { initTRPC, TRPCError } from "@trpc/server";
import { z } from "zod";

export type RoomInfo = PythonAPI["GET /api/rooms"]["output"][number];
type PythonQuery = keyof PythonAPI & `GET ${string}`;
type QueryInput<K extends PythonQuery> = PythonAPI[K]["path"] & PythonAPI[K]["query"];

export interface RPCContext {
  apiURL: string;
  fetch: typeof globalThis.fetch;
}

const t = initTRPC.context<RPCContext>().create();

const roomID = z.string().regex(/^[A-Za-z0-9_-]+$/, "Expected a room ID containing letters, digits, underscores or hyphens.");

// Steering appends tags such as .steer1 to newly merged claim IDs.
const claimID = z.string().regex(/^[A-Za-z0-9_.-]+$/)
  .refine((value) => value !== "." && value !== "..", "Expected a claim ID containing letters, digits, underscores, hyphens or dots.");
const version = z.number().int().safe().positive().nullish().transform((value) => value ?? undefined);

// Objects strip unknown keys, and null/omitted versions both select the latest.
// Let tRPC infer the client input and parsed resolver input from these schemas.
const roomInput = z.object({ room: roomID, version });
const resultInput = z.object({ room: roomID, scan: roomID });
const sourceInput = z.object({ room: roomID, claim_id: claimID, i: z.number().int().safe().nonnegative() });
const fundInput = z.object({ fund: roomID });
const companyInput = z.object({ fund: roomID, company: roomID, version });

async function pythonJSON<K extends PythonQuery>(ctx: RPCContext, operation: K, input: QueryInput<K>): Promise<PythonAPI[K]["output"]> {
  // The operation selects both the Python URL and its generated response type.
  const params = { ...input } as Record<string, unknown>;
  const path = operation.slice(4).replace(/\{([^}]+)\}/g, (_match, name: string) => {
    const value = params[name];
    if (value === undefined) throw new Error(`Missing Python path parameter: ${name}`);
    delete params[name];
    return encodeURIComponent(String(value));
  });
  const url = new URL(path, ctx.apiURL);
  for (const [name, value] of Object.entries(params)) {
    if (value !== undefined && value !== null) url.searchParams.set(name, String(value));
  }
  let response: Response;
  try {
    response = await ctx.fetch(url, {
      signal: AbortSignal.timeout(30_000),
      redirect: "error",
    });
  } catch {
    throw new TRPCError({ code: "SERVICE_UNAVAILABLE", message: "The Python API is unavailable." });
  }
  if (!response.ok) {
    const code = response.status === 404 ? "NOT_FOUND"
      : response.status === 403 ? "FORBIDDEN"
      : response.status === 400 || response.status === 422 ? "BAD_REQUEST"
      : "BAD_GATEWAY";
    let message = "The Python API could not complete this request.";
    if (code !== "BAD_GATEWAY") {
      const body: unknown = await response.json().catch(() => null);
      if (body && typeof body === "object" && "detail" in body && typeof body.detail === "string") {
        message = body.detail;
      }
    }
    throw new TRPCError({ code, message });
  }
  try {
    // FastAPI validates declared response models. The generated contract is
    // compile-time only; this boundary does not validate the JSON a second time.
    return await response.json() as PythonAPI[K]["output"];
  } catch {
    throw new TRPCError({ code: "BAD_GATEWAY", message: "The Python API returned invalid JSON." });
  }
}

export const appRouter = t.router({
  health: t.procedure.query(({ ctx }) => pythonJSON(ctx, "GET /health", {})),
  scan: t.router({
    list: t.procedure.query(({ ctx }) => pythonJSON(ctx, "GET /api/scans", {})),
  }),
  room: t.router({
    list: t.procedure.query(({ ctx }) => pythonJSON(ctx, "GET /api/rooms", {})),
    readout: t.procedure.input(roomID).query(({ ctx, input }) =>
      pythonJSON(ctx, "GET /api/rooms/{room}/readout", { room: input })),
    result: t.procedure.input(resultInput).query(({ ctx, input }) =>
      pythonJSON(ctx, "GET /api/rooms/{room}/results/{scan}", input)),
    steerable: t.procedure.input(roomID).query(({ ctx, input }) =>
      pythonJSON(ctx, "GET /api/rooms/{room}/steerable", { room: input })),
    revisions: t.procedure.input(roomID).query(({ ctx, input }) =>
      pythonJSON(ctx, "GET /api/rooms/{room}/revisions", { room: input })),
    source: t.procedure.input(sourceInput).query(({ ctx, input }) =>
      pythonJSON(ctx, "GET /api/rooms/{room}/claims/{claim_id}/sources/{i}", input)),
  }),
  memo: t.router({
    get: t.procedure.input(roomInput).query(({ ctx, input }) =>
      pythonJSON(ctx, "GET /api/rooms/{room}/memo", input)),
    versions: t.procedure.input(roomID).query(({ ctx, input }) =>
      pythonJSON(ctx, "GET /api/rooms/{room}/memo/versions", { room: input })),
  }),
  store: t.router({
    companies: t.procedure.input(fundInput).query(({ ctx, input }) =>
      pythonJSON(ctx, "GET /api/store/{fund}", input)),
    holding: t.procedure.input(companyInput).query(({ ctx, input }) =>
      pythonJSON(ctx, "GET /api/store/{fund}/{company}", { fund: input.fund, company: input.company })),
    versions: t.procedure.input(companyInput).query(({ ctx, input }) =>
      pythonJSON(ctx, "GET /api/store/{fund}/{company}/versions", { fund: input.fund, company: input.company })),
    readout: t.procedure.input(companyInput).query(({ ctx, input }) =>
      pythonJSON(ctx, "GET /api/store/{fund}/{company}/readout", input)),
  }),
  founderRequests: t.router({
    list: t.procedure.input(roomID).query(({ ctx, input }) =>
      pythonJSON(ctx, "GET /api/rooms/{room}/founder-requests", { room: input })),
    received: t.procedure.input(roomID).query(({ ctx, input }) =>
      pythonJSON(ctx, "GET /api/rooms/{room}/founder-requests/received", { room: input })),
  }),
});

export type AppRouter = typeof appRouter;
