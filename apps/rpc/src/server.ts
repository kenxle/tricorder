import { createHTTPServer } from "@trpc/server/adapters/standalone";
import { appRouter } from "./router.ts";

export interface RPCServerOptions {
  apiURL: string;
  fetch?: typeof globalThis.fetch;
}

function localHost(host: string | undefined): boolean {
  if (!host || !/^(localhost|127\.0\.0\.1|\[::1\])(?::[0-9]+)?$/i.test(host)) return false;
  try {
    // URL also rejects invalid ports, including those outside the TCP range.
    return new URL(`http://${host}`).port !== "0";
  } catch {
    return false;
  }
}

export function createRPCServer(options: RPCServerOptions) {
  return createHTTPServer({
    router: appRouter,
    basePath: "/trpc/",
    maxBodySize: 8_192,
    maxBatchSize: 10,
    createContext: () => ({ apiURL: options.apiURL, fetch: options.fetch ?? globalThis.fetch }),
    middleware(req, res, next) {
      if (!localHost(req.headers.host)) {
        res.writeHead(403, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ detail: "This server answers only on localhost." }));
        return;
      }
      if (req.method !== "GET") {
        res.writeHead(405, { "Allow": "GET", "Content-Type": "application/json" });
        res.end(JSON.stringify({ detail: "The tRPC facade supports read-only GET queries." }));
        return;
      }
      next();
    },
  });
}
