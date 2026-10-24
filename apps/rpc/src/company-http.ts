import type { IncomingMessage, ServerResponse } from "node:http";

import { z } from "zod";

import {
  CompanyUnavailableError,
  loadSavedCompanyData,
  savedCompanyReadout,
  savedCompanySection,
} from "./company-data.ts";
import type { SavedCompanyData } from "./company-data.ts";
import { loadSavedCompanyRoomData, savedCompanyRoom } from "./company-room.ts";

const readoutQuery = z
  .object({ url: z.string().trim().min(1).max(2048) })
  .strict();
const sectionQuery = z
  .object({
    company: z.string().regex(/^[a-z0-9][a-z0-9-]{0,99}$/u),
    section: z.enum(["founders", "comps", "signals", "outside"]),
  })
  .strict();
const roomQuery = z
  .object({
    company: z.string().regex(/^[a-z0-9][a-z0-9-]{0,99}$/u),
    stage: z.enum(["partial", "full"]),
  })
  .strict();
const sameOrigin = (req: IncomingMessage, origin: string) => {
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
const send = (res: ServerResponse, status: number, body: unknown) => {
  res.writeHead(status, {
    "Cache-Control": "no-store",
    "Content-Type": "application/json",
    "X-Content-Type-Options": "nosniff",
  });
  res.end(JSON.stringify(body));
};
export const serveCompany = (
  req: IncomingMessage,
  res: ServerResponse,
  load: () => SavedCompanyData = loadSavedCompanyData,
  loadRoom: () => unknown = loadSavedCompanyRoomData
) => {
  const url = new URL(req.url ?? "/", `http://${req.headers.host}`);
  if (!sameOrigin(req, url.origin)) {
    send(res, 403, { detail: "Refused: this request came from another site." });
    return;
  }
  const entries = [...url.searchParams.entries()];
  if (new Set(entries.map(([key]) => key)).size !== entries.length) {
    send(res, 400, { detail: "Send each query parameter once." });
    return;
  }
  const query = Object.fromEntries(entries);
  try {
    if (url.pathname === "/company/room") {
      const parsed = roomQuery.safeParse(query);
      if (!parsed.success) {
        send(res, 400, {
          detail: "Send a saved company slug and partial or full stage.",
        });
        return;
      }
      send(
        res,
        200,
        savedCompanyRoom(loadRoom(), parsed.data.company, parsed.data.stage)
      );
    } else if (url.pathname === "/company/readout") {
      const parsed = readoutQuery.safeParse(query);
      if (!parsed.success) {
        send(res, 400, { detail: "Send a company website or YC URL." });
        return;
      }
      send(res, 200, savedCompanyReadout(load(), parsed.data.url));
    } else {
      const parsed = sectionQuery.safeParse(query);
      if (!parsed.success) {
        send(res, 400, {
          detail: "Send a saved company slug and research section.",
        });
        return;
      }
      send(
        res,
        200,
        savedCompanySection(load(), parsed.data.company, parsed.data.section)
      );
    }
  } catch (error) {
    send(res, error instanceof CompanyUnavailableError ? 404 : 503, {
      detail:
        error instanceof CompanyUnavailableError
          ? error.message
          : "Saved company research is unavailable. Try again later.",
    });
  }
};
