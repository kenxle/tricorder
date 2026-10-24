// Server-only streaming adapter. The browser never chooses the upstream address.
import { requestQuerySchema } from "@tricorder/request-ui/catalog";

const localAddress = (host: string) =>
  ["localhost", "127.0.0.1", "[::1]"].includes(host);
const fail = (status: number, detail: string) =>
  Response.json(
    { detail },
    { headers: { "Cache-Control": "no-store" }, status }
  );

const sameOrigin = (request: Request, url: URL) => {
  if (request.headers.get("sec-fetch-site") === "cross-site") {
    return false;
  }
  const origin = request.headers.get("origin");
  if (origin !== null) {
    return origin === url.origin;
  }
  const referer = request.headers.get("referer");
  if (!referer) {
    return true;
  }
  try {
    return new URL(referer).origin === url.origin;
  } catch {
    return false;
  }
};

const validUpstream = (target: URL) =>
  !(
    !localAddress(target.hostname) ||
    !["http:", "https:"].includes(target.protocol) ||
    target.username ||
    target.password ||
    target.pathname !== "/" ||
    target.search ||
    target.hash
  );

export const proxyRequestUI = async (
  request: Request,
  upstream = process.env.TRICORDER_RPC_URL ??
    `http://127.0.0.1:${process.env.TRICORDER_RPC_PORT ?? "8789"}`,
  fetcher: typeof fetch = fetch
) => {
  const url = new URL(request.url);
  if (!localAddress(url.hostname) || !sameOrigin(request, url)) {
    return fail(403, "The request UI adapter is local and same-origin only.");
  }
  if (request.method !== "GET") {
    return fail(405, "The request UI supports GET only.");
  }
  if (url.pathname !== "/api/ui/request") {
    return fail(404, "Unknown request UI endpoint.");
  }
  const entries = [...url.searchParams.entries()];
  const query = requestQuerySchema.safeParse(Object.fromEntries(entries));
  if (
    !query.success ||
    new Set(entries.map(([key]) => key)).size !== entries.length
  ) {
    return fail(400, "Send a saved company slug and a supported stage.");
  }
  let target: URL;
  try {
    target = new URL(upstream);
    if (!validUpstream(target)) {
      return fail(503, "TRICORDER_RPC_URL must be a local RPC origin.");
    }
  } catch {
    return fail(503, "TRICORDER_RPC_URL must be a local RPC origin.");
  }
  target.pathname = "/ui/request";
  target.search = new URLSearchParams(query.data).toString();
  try {
    const response = await fetcher(target, {
      method: "GET",
      redirect: "error",
      signal: request.signal,
    });
    const headers = new Headers({
      "Cache-Control": "no-store",
      "Content-Type":
        response.headers.get("content-type") ?? "application/json",
    });
    const version = response.headers.get("x-tricorder-ui-version");
    if (version) {
      headers.set("X-Tricorder-UI-Version", version);
    }
    return new Response(response.body, { headers, status: response.status });
  } catch {
    return fail(
      502,
      "The local RPC server is unavailable. Start pnpm --filter @tricorder/rpc dev."
    );
  }
};
