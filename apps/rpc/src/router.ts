import type { Readout } from "@tricorder/schema";
import { initTRPC, TRPCError } from "@trpc/server";

export interface RoomInfo {
  id: string;
  path: string;
  inputs: string[];
  has_readout: boolean;
}

export interface RPCContext {
  apiURL: string;
  fetch: typeof globalThis.fetch;
}

const t = initTRPC.context<RPCContext>().create();

function roomID(value: unknown): string {
  if (typeof value !== "string" || !/^[A-Za-z0-9_-]+$/.test(value)) {
    throw new Error("Expected a room ID containing letters, digits, underscores or hyphens.");
  }
  return value;
}

async function pythonJSON<T>(ctx: RPCContext, path: string): Promise<T> {
  let response: Response;
  try {
    response = await ctx.fetch(new URL(path, ctx.apiURL), {
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
    // Python owns runtime validation (Pydantic for Readout). This facade shares
    // its generated TypeScript model; it does not validate the JSON a second time.
    return await response.json() as T;
  } catch {
    throw new TRPCError({ code: "BAD_GATEWAY", message: "The Python API returned invalid JSON." });
  }
}

export const appRouter = t.router({
  room: t.router({
    list: t.procedure.query(({ ctx }) => pythonJSON<RoomInfo[]>(ctx, "/api/rooms")),
    readout: t.procedure.input(roomID).query(({ ctx, input }) =>
      pythonJSON<Readout>(ctx, `/api/rooms/${encodeURIComponent(input)}/readout`)),
  }),
});

export type AppRouter = typeof appRouter;
