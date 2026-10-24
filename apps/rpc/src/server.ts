import { createHTTPServer } from "@trpc/server/adapters/standalone";

import type { SavedCompanyData } from "./company-data.ts";
import { serveCompany } from "./company-http.ts";
import { streamRequestUI } from "./request-ui-stream.ts";
import type { RequestUIPatchSource } from "./request-ui-stream.ts";
import { appRouter } from "./router.ts";

export interface RPCServerOptions {
  apiURL: string;
  fetch?: typeof globalThis.fetch;
  requestUIPatches?: RequestUIPatchSource;
  companyData?: () => SavedCompanyData;
}

function localHost(host: string | undefined): boolean {
  if (!host || !/^(localhost|127\.0\.0\.1|\[::1\])(?::[0-9]+)?$/i.test(host)) {
    return false;
  }
  try {
    // URL also rejects invalid ports, including those outside the TCP range.
    return new URL(`http://${host}`).port !== "0";
  } catch {
    return false;
  }
}

export function createRPCServer(options: RPCServerOptions) {
  return createHTTPServer({
    basePath: "/trpc/",
    createContext: () => ({
      apiURL: options.apiURL,
      fetch: options.fetch ?? globalThis.fetch,
    }),
    maxBatchSize: 10,
    maxBodySize: 8192,
    middleware(req, res, next) {
      if (!localHost(req.headers.host)) {
        res.writeHead(403, { "Content-Type": "application/json" });
        res.end(
          JSON.stringify({ detail: "This server answers only on localhost." })
        );
        return;
      }
      if (req.method !== "GET") {
        res.writeHead(405, {
          Allow: "GET",
          "Content-Type": "application/json",
        });
        res.end(
          JSON.stringify({
            detail: "The tRPC facade supports read-only GET queries.",
          })
        );
        return;
      }
      if (req.url?.split("?")[0] === "/ui/request") {
        void streamRequestUI(req, res, options.requestUIPatches);
        return;
      }
      if (
        ["/company/readout", "/company/section"].includes(
          req.url?.split("?")[0] ?? ""
        )
      ) {
        serveCompany(req, res, options.companyData);
        return;
      }
      next();
    },
    router: appRouter,
  });
}
