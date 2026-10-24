// Server-only adapter. A company URL selects saved data, never a fetch target.
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
  localAddress(target.hostname) &&
  ["http:", "https:"].includes(target.protocol) &&
  !target.username &&
  !target.password &&
  target.pathname === "/" &&
  !target.search &&
  !target.hash;

const validQuery = (url: URL) => {
  const entries = [...url.searchParams.entries()];
  if (new Set(entries.map(([key]) => key)).size !== entries.length) {
    return false;
  }
  if (url.pathname === "/api/company/readout") {
    const companyURL = url.searchParams.get("url");
    return (
      entries.length === 1 &&
      companyURL !== null &&
      companyURL.trim().length > 0 &&
      companyURL.length <= 2048
    );
  }
  const company = url.searchParams.get("company");
  if (url.pathname === "/api/company/room") {
    const stage = url.searchParams.get("stage");
    return (
      entries.length === 2 &&
      company !== null &&
      /^[a-z0-9][a-z0-9-]{0,99}$/u.test(company) &&
      stage !== null &&
      ["partial", "full"].includes(stage)
    );
  }
  const section = url.searchParams.get("section");
  return (
    entries.length === 2 &&
    company !== null &&
    /^[a-z0-9][a-z0-9-]{0,99}$/u.test(company) &&
    section !== null &&
    ["founders", "comps", "signals", "outside"].includes(section)
  );
};

export const proxyCompany = async (
  request: Request,
  upstream = process.env.TRICORDER_RPC_URL ??
    `http://127.0.0.1:${process.env.TRICORDER_RPC_PORT ?? "8789"}`,
  fetcher: typeof fetch = fetch
) => {
  const url = new URL(request.url);
  if (!localAddress(url.hostname) || !sameOrigin(request, url)) {
    return fail(403, "The company adapter is local and same-origin only.");
  }
  if (request.method !== "GET") {
    return fail(405, "Saved company readouts support GET only.");
  }
  if (
    ![
      "/api/company/readout",
      "/api/company/section",
      "/api/company/room",
    ].includes(url.pathname)
  ) {
    return fail(404, "Unknown company endpoint.");
  }
  if (!validQuery(url)) {
    return fail(400, "Send a company URL or a company slug and section.");
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
  target.pathname = url.pathname.slice(4);
  target.search = url.search;
  const signal = AbortSignal.any([request.signal, AbortSignal.timeout(30_000)]);
  try {
    const response = await fetcher(target, {
      method: "GET",
      redirect: "error",
      signal,
    });
    return new Response(response.body, {
      headers: {
        "Cache-Control": "no-store",
        "Content-Type":
          response.headers.get("content-type") ?? "application/json",
      },
      status: response.status,
    });
  } catch {
    return fail(
      signal.aborted ? 504 : 502,
      signal.aborted
        ? "The saved company request did not finish. Please retry."
        : "The local RPC server is unavailable. Start pnpm --filter @tricorder/rpc dev."
    );
  }
};
