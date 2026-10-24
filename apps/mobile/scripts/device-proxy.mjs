import { createServer, request } from "node:http";
import { connect } from "node:net";

const forwardedHeaders = (incoming, metroPort) => ({
  ...Object.fromEntries(
    Object.entries(incoming.headers).filter(
      ([name]) => name !== "forwarded" && !name.startsWith("x-forwarded-")
    )
  ),
  host: `127.0.0.1:${metroPort}`,
});

// The launcher binds this listener to one local address and chooses one phone.
// Keep this gate on HTTP and upgrades: Metro's WebSocket also reaches local tools.
export const createDeviceProxy = ({ host, peer, port, metroPort }) => {
  const authority = `${host}:${port}`;
  const allowed = (incoming) =>
    incoming.socket.remoteAddress === peer &&
    incoming.headers.host === authority &&
    incoming.url?.startsWith("/") &&
    !incoming.url.startsWith("//") &&
    incoming.headers.referer === undefined;

  const server = createServer((incoming, outgoing) => {
    if (
      !allowed(incoming) ||
      incoming.headers.origin !== undefined ||
      incoming.headers["sec-fetch-site"] === "cross-site"
    ) {
      outgoing.writeHead(403).end("Restricted development connection");
      return;
    }
    const upstream = request(
      {
        headers: forwardedHeaders(incoming, metroPort),
        hostname: "127.0.0.1",
        method: incoming.method,
        path: incoming.url,
        port: metroPort,
      },
      (response) => {
        outgoing.writeHead(response.statusCode, response.headers);
        response.on("error", () => outgoing.destroy());
        response.on("aborted", () => outgoing.destroy());
        response.pipe(outgoing);
      }
    );
    upstream.on("error", () => {
      if (outgoing.headersSent) {
        outgoing.destroy();
      } else {
        outgoing.writeHead(502).end("Local Metro server is unavailable");
      }
    });
    incoming.on("error", () => upstream.destroy());
    incoming.on("aborted", () => upstream.destroy());
    outgoing.on("close", () => upstream.destroy());
    incoming.pipe(upstream);
  });
  server.on("clientError", (_error, socket) => {
    socket.end(
      "HTTP/1.1 403 Forbidden\r\nConnection: close\r\nContent-Length: 0\r\n\r\n"
    );
  });
  server.on("upgrade", (incoming, socket, head) => {
    if (
      !allowed(incoming) ||
      // Native RN WebSockets may synthesize this origin. Browsers also attach
      // fetch metadata, which is never needed by a native development client.
      (incoming.headers.origin !== undefined &&
        incoming.headers.origin !== `http://${authority}`) ||
      Object.keys(incoming.headers).some((name) =>
        name.startsWith("sec-fetch-")
      ) ||
      incoming.method !== "GET" ||
      incoming.headers.upgrade?.toLowerCase() !== "websocket"
    ) {
      socket.destroy();
      return;
    }
    const upstream = connect(metroPort, "127.0.0.1", () => {
      const headers = Object.entries(forwardedHeaders(incoming, metroPort))
        .flatMap(([name, value]) =>
          (Array.isArray(value) ? value : [value]).map(
            (entry) => `${name}: ${entry}`
          )
        )
        .join("\r\n");
      upstream.write(
        `${incoming.method} ${incoming.url} HTTP/1.1\r\n${headers}\r\n\r\n`
      );
      upstream.write(head);
      socket.pipe(upstream).pipe(socket);
    });
    upstream.on("error", () => socket.destroy());
    socket.on("error", () => upstream.destroy());
    socket.on("end", () => upstream.destroy());
    socket.on("close", () => upstream.destroy());
    upstream.on("end", () => socket.destroy());
    upstream.on("close", () => socket.destroy());
  });
  return server;
};
