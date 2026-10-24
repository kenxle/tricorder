import assert from "node:assert/strict";
import { once } from "node:events";
import { createServer, request } from "node:http";
import { connect } from "node:net";
import { test } from "node:test";

import { createDeviceProxy } from "../scripts/device-proxy.mjs";

const listen = async (server) => {
  server.listen(0, "127.0.0.1");
  await once(server, "listening");
  return server.address().port;
};
const close = async (server) => {
  const closed = once(server, "close");
  server.closeAllConnections();
  server.close();
  await closed;
};
const send = async (port, overrides = {}, body = "") => {
  const outgoing = request({
    headers: { host: "127.0.0.1:8082" },
    hostname: "127.0.0.1",
    path: "/status",
    port,
    ...overrides,
  });
  const replied = once(outgoing, "response");
  outgoing.end(body);
  const [response] = await replied;
  let text = "";
  for await (const chunk of response) {
    text += chunk;
  }
  return { body: text, status: response.statusCode };
};
const proxyFor = (metroPort, peer = "127.0.0.1") =>
  createDeviceProxy({ host: "127.0.0.1", metroPort, peer, port: 8082 });

test("device proxy forwards HTTP body and status only to fixed loopback Metro", async () => {
  let received;
  const metro = createServer(async (incoming, response) => {
    let body = "";
    for await (const chunk of incoming) {
      body += chunk;
    }
    received = { body, headers: incoming.headers, url: incoming.url };
    response.writeHead(201).end("created");
  });
  const metroPort = await listen(metro);
  const proxy = proxyFor(metroPort);
  const port = await listen(proxy);
  try {
    const response = await send(
      port,
      {
        headers: {
          "content-type": "application/json",
          forwarded: "host=evil.example",
          host: "127.0.0.1:8082",
          "x-forwarded-for": "1.2.3.4",
          "x-forwarded-host": "evil.example",
          "x-forwarded-proto": "https",
        },
        method: "POST",
        path: "/api/rooms/test/steer",
      },
      '{"sentence":"check"}'
    );
    assert.deepEqual(response, { body: "created", status: 201 });
    assert.equal(received.body, '{"sentence":"check"}');
    assert.equal(received.url, "/api/rooms/test/steer");
    assert.equal(received.headers.host, `127.0.0.1:${metroPort}`);
    assert.equal(received.headers.forwarded, undefined);
    assert.equal(received.headers["x-forwarded-host"], undefined);
    assert.equal(received.headers["x-forwarded-for"], undefined);
    assert.equal(received.headers["x-forwarded-proto"], undefined);
  } finally {
    await close(proxy);
    await close(metro);
  }
});

test("device proxy rejects other peers, authorities, browser origins and absolute paths", async () => {
  const proxy = proxyFor(1);
  const port = await listen(proxy);
  const otherPeer = proxyFor(1, "127.0.0.2");
  const otherPort = await listen(otherPeer);
  try {
    const results = await Promise.all([
      ...[
        { host: "evil.example" },
        { host: "127.0.0.1:8082", origin: "" },
        { host: "127.0.0.1:8082", referer: "" },
        { host: "127.0.0.1:8082", origin: "http://127.0.0.1:8082" },
        { host: "127.0.0.1:8082", referer: "http://127.0.0.1:8082/" },
        { host: "127.0.0.1:8082", "sec-fetch-site": "cross-site" },
      ].map((headers) => send(port, { headers })),
      ...["//evil.example/", "http://evil.example/"].map((path) =>
        send(port, { path })
      ),
      send(otherPort),
    ]);
    for (const result of results) {
      assert.equal(result.status, 403);
    }
    const outage = await send(port);
    assert.equal(outage.status, 502);
  } finally {
    await close(proxy);
    await close(otherPeer);
  }
});

for (const origin of ["", "Origin: http://127.0.0.1:8082\r\n"]) {
  test(
    `device proxy forwards native WebSocket with ${origin ? "expected" : "absent"} Origin and closes both socket ends`,
    { timeout: 5000 },
    async () => {
      const metro = createServer();
      let received;
      let upstreamSocket;
      metro.on("upgrade", (incoming, socket, head) => {
        upstreamSocket = socket;
        received = { headers: incoming.headers, url: incoming.url };
        socket.write(
          "HTTP/1.1 101 Switching Protocols\r\nConnection: Upgrade\r\nUpgrade: websocket\r\n\r\n"
        );
        if (head.length) {
          socket.write(head);
        }
        socket.on("data", (chunk) => socket.write(chunk));
        socket.on("end", () => socket.destroy());
      });
      const metroPort = await listen(metro);
      const proxy = proxyFor(metroPort);
      const port = await listen(proxy);
      const client = connect(port, "127.0.0.1");
      try {
        await once(client, "connect");
        const echoed = async () => {
          let result = "";
          for await (const chunk of client.iterator({
            destroyOnReturn: false,
          })) {
            result += chunk;
            if (result.includes("head-data")) {
              return result;
            }
          }
          throw new Error("Socket closed before the upgrade head was echoed");
        };
        const echo = echoed();
        client.write(
          `GET /hot HTTP/1.1\r\nHost: 127.0.0.1:8082\r\n${origin}Connection: Upgrade\r\nUpgrade: websocket\r\nX-Forwarded-Host: evil.example\r\n\r\nhead-data`
        );
        assert.match(await echo, /101 Switching Protocols/u);
        assert.equal(received.url, "/hot");
        assert.equal(received.headers.host, `127.0.0.1:${metroPort}`);
        assert.equal(received.headers["x-forwarded-host"], undefined);
        const closed = once(upstreamSocket, "close");
        client.destroy();
        await closed;
      } finally {
        client.destroy();
        upstreamSocket?.destroy();
        await close(proxy);
        await close(metro);
      }
    }
  );
}

test(
  "device proxy drops rejected upgrades before reaching Metro",
  { timeout: 5000 },
  async () => {
    const metro = createServer();
    let reachedMetro = 0;
    metro.on("upgrade", (_incoming, socket) => {
      reachedMetro += 1;
      socket.destroy();
    });
    const metroPort = await listen(metro);
    const proxy = proxyFor(metroPort);
    const port = await listen(proxy);
    try {
      await Promise.all(
        [
          "Origin: http://evil.example\r\n",
          "Origin: \r\n",
          "Origin: http://127.0.0.1:8082\r\nReferer: \r\n",
          "Origin: http://127.0.0.1:8082\r\nSec-Fetch-Site: same-origin\r\n",
          "Origin: http://127.0.0.1:8082\r\nSec-Fetch-Mode: websocket\r\n",
          "Origin: http://127.0.0.1:8082\r\nSec-Fetch-Dest: empty\r\n",
          "Sec-Fetch-User: \r\n",
        ].map(async (headers) => {
          const client = connect(port, "127.0.0.1");
          try {
            await once(client, "connect");
            const closed = once(client, "close");
            let response = "";
            client.on("data", (chunk) => {
              response += chunk;
            });
            client.write(
              `GET /hot HTTP/1.1\r\nHost: 127.0.0.1:8082\r\n${headers}Connection: Upgrade\r\nUpgrade: websocket\r\n\r\n`
            );
            await closed;
            assert.equal(response, "");
          } finally {
            client.destroy();
          }
        })
      );
      assert.equal(reachedMetro, 0);
    } finally {
      await close(proxy);
      await close(metro);
    }
  }
);
