// Server-only adapter for the existing local Python API. Never imported by UI.
const ROOM = "[A-Za-z0-9_-]+";
const GET_PATH = new RegExp(
  `^/api/rooms(?:/${ROOM}/(?:readout|steerable|founder-requests|claims/[A-Za-z0-9_.-]+/sources/[0-9]+))?$`
);
const POST_PATH = new RegExp(
  `^/api/rooms/${ROOM}/(?:readout|source|steer|founder-requests/(?:draft|copy|batch))$`
);
const localAddress = (host: string) =>
  ["localhost", "127.0.0.1", "[::1]"].includes(host);
export async function proxyReadout(
  request: Request,
  upstream = process.env.TRICORDER_API_URL ?? "http://127.0.0.1:8787",
  fetcher: typeof fetch = fetch
) {
  const url = new URL(request.url);
  // The Expo server must also bind to loopback (package scripts use --localhost). No CORS.
  if (!localAddress(url.hostname)) {
    return Response.json(
      { detail: "The readout adapter is local only." },
      { status: 403 }
    );
  }
  const origin = request.headers.get("origin");
  const referer = request.headers.get("referer");
  let browserOrigin: string | null = origin;
  if (!browserOrigin && referer) {
    try {
      browserOrigin = new URL(referer).origin;
    } catch {
      browserOrigin = "invalid";
    }
  }
  if (
    (browserOrigin && browserOrigin !== url.origin) ||
    request.headers.get("sec-fetch-site") === "cross-site"
  ) {
    return Response.json(
      { detail: "Refused: this request came from another site." },
      { status: 403 }
    );
  }
  const allowed =
    request.method === "GET"
      ? GET_PATH.test(url.pathname)
      : request.method === "POST" && POST_PATH.test(url.pathname);
  if (!allowed || url.search) {
    return Response.json(
      { detail: "Unknown readout endpoint." },
      { status: 404 }
    );
  }
  if (
    request.method === "POST" &&
    request.headers.get("content-type")?.split(";")[0].trim() !==
      "application/json"
  ) {
    // A rebuild has no body, all other writes are JSON.
    if (!url.pathname.endsWith("/readout") || (await request.clone().text())) {
      return Response.json({ detail: "Send JSON." }, { status: 415 });
    }
  }
  try {
    const target = new URL(upstream);
    if (
      !["http:", "https:"].includes(target.protocol) ||
      !["localhost", "127.0.0.1", "[::1]"].includes(target.hostname)
    ) {
      return Response.json(
        { detail: "TRICORDER_API_URL must point at the local Python API." },
        { status: 503 }
      );
    }
    const response = await fetcher(new URL(url.pathname, target), {
      method: request.method,
      ...(request.method === "POST"
        ? {
            body: await request.text(),
            headers: { "Content-Type": "application/json" },
          }
        : {}),
      redirect: "error",
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
    return Response.json(
      {
        detail:
          "The local Python API is unavailable. Start pnpm dev or pnpm --filter @tricorder/api dev.",
      },
      { status: 502 }
    );
  }
}
