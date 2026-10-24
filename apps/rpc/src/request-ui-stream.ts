import { once } from "node:events";
import { readFileSync } from "node:fs";
import type { IncomingMessage, ServerResponse } from "node:http";

import {
  requestQuerySchema,
  requestSpecPatches,
} from "@tricorder/request-ui/catalog";
import { requestItems } from "@tricorder/request-ui/model";
import { z } from "zod";

type Query = ReturnType<typeof requestQuerySchema.parse>;
type Patch = ReturnType<typeof requestSpecPatches>[number];
export type RequestUIPatchSource = (
  query: Query,
  signal: AbortSignal
) => Iterable<Patch> | AsyncIterable<Patch>;

const snapshotSchema = z.object({
  checklist: z.array(
    z.object({
      ask: z.string(),
      closing_at_early_stage: z.boolean(),
      guidance: z.object({ form: z.string(), what: z.string() }).nullable(),
      id: z.string(),
      includes: z.string().nullable(),
      kind: z.string(),
      stages: z.record(z.string()),
      title: z.string(),
    })
  ),
  companies: z.array(z.object({ slug: z.string() })),
  research: z.record(
    z.object({
      room_gaps: z.array(
        z.object({
          ids: z.array(z.string()),
          text: z.string(),
          why: z.string(),
        })
      ),
    })
  ),
});

class UnknownCompanyError extends Error {
  override name = "UnknownCompanyError";
}

export const savedRequestPatches: RequestUIPatchSource = (query) => {
  const snapshot = snapshotSchema.parse(
    JSON.parse(
      readFileSync(
        new URL(
          "../../../docs/features/20261024.02_first_steps_ui/prototype/data.json",
          import.meta.url
        ),
        "utf-8"
      )
    )
  );
  if (!snapshot.companies.some((company) => company.slug === query.company)) {
    throw new UnknownCompanyError("No saved company research exists.");
  }
  return requestSpecPatches(
    requestItems(
      snapshot.checklist,
      query.stage,
      snapshot.research[query.company]
    )
  );
};

const sameOrigin = (req: IncomingMessage, origin: string): boolean => {
  if (req.headers["sec-fetch-site"] === "cross-site") {
    return false;
  }
  if (req.headers.origin !== undefined) {
    return req.headers.origin === origin;
  }
  if (!req.headers.referer) {
    return true;
  }
  try {
    return new URL(req.headers.referer).origin === origin;
  } catch {
    return false;
  }
};

const failure = (res: ServerResponse, status: number, detail: string) => {
  res.writeHead(status, {
    "Cache-Control": "no-store",
    "Content-Type": "application/json",
  });
  res.end(JSON.stringify({ detail }));
};

export const streamRequestUI = async (
  req: IncomingMessage,
  res: ServerResponse,
  source: RequestUIPatchSource = savedRequestPatches
) => {
  const url = new URL(req.url ?? "/", `http://${req.headers.host}`);
  if (!sameOrigin(req, url.origin)) {
    failure(res, 403, "Refused: this request came from another site.");
    return;
  }
  const entries = [...url.searchParams.entries()];
  const query = requestQuerySchema.safeParse(Object.fromEntries(entries));
  if (
    !query.success ||
    new Set(entries.map(([key]) => key)).size !== entries.length
  ) {
    failure(res, 400, "Send a saved company slug and a supported stage.");
    return;
  }
  const controller = new AbortController();
  const abort = () => controller.abort();
  res.once("close", abort);
  try {
    const patches = source(query.data, controller.signal);
    res.writeHead(200, {
      "Cache-Control": "no-store",
      "Content-Type": "application/x-ndjson",
      "X-Content-Type-Options": "nosniff",
      "X-Tricorder-UI-Version": "1",
    });
    res.flushHeaders();
    for await (const patch of patches) {
      if (controller.signal.aborted) {
        break;
      }
      if (!res.write(`${JSON.stringify(patch)}\n`)) {
        await once(res, "drain", { signal: controller.signal });
      }
    }
    if (!controller.signal.aborted) {
      res.end();
    }
  } catch (error) {
    if (controller.signal.aborted) {
      return;
    }
    if (res.headersSent) {
      res.destroy();
    } else {
      failure(
        res,
        error instanceof UnknownCompanyError ? 404 : 500,
        error instanceof UnknownCompanyError
          ? error.message
          : "Saved request data is unavailable."
      );
    }
  } finally {
    res.off("close", abort);
  }
};
