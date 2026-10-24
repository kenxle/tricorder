import assert from "node:assert/strict";
import { test } from "node:test";

import { proxyReadout } from "../src/readout/proxy.ts";

const local = "http://localhost:8081";
test("adapter rejects cross-site and DNS-rebinding requests before calling Python", async () => {
  const fetcher = async () => {
    throw new Error("must not reach Python");
  };
  for (const [url, headers] of [
    ["http://evil.example/api/rooms", {}],
    ["http://192.168.1.2:8081/api/rooms", {}],
    [`${local}/api/rooms`, { origin: "https://evil.example" }],
    [`${local}/api/rooms`, { "sec-fetch-site": "cross-site" }],
    [`${local}/api/rooms`, { referer: "https://evil.example/page" }],
  ]) {
    assert.equal(
      (await proxyReadout(new Request(url, { headers }), undefined, fetcher))
        .status,
      403
    );
  }
});
test("adapter forwards only permitted endpoints to a fixed loopback destination", async () => {
  const calls = [];
  const fetcher = async (input, init) => {
    calls.push({ init, url: String(input) });
    return Response.json({ room: "hollis_voice" });
  };
  const response = await proxyReadout(
    new Request(`${local}/api/rooms/hollis_voice/steer`, {
      body: JSON.stringify({
        piece: "overview",
        sentence: "read the full room",
      }),
      headers: { "Content-Type": "application/json" },
      method: "POST",
    }),
    undefined,
    fetcher
  );
  assert.equal(response.status, 200);
  assert.equal(
    calls[0].url,
    "http://127.0.0.1:8787/api/rooms/hollis_voice/steer"
  );
  assert.equal(
    calls[0].init?.body,
    JSON.stringify({ piece: "overview", sentence: "read the full room" })
  );
  assert.equal(new Headers(calls[0].init?.headers).has("origin"), false);
  assert.equal(
    (
      await proxyReadout(
        new Request(`${local}/api/store/fund`),
        undefined,
        fetcher
      )
    ).status,
    404
  );
  assert.equal(
    (
      await proxyReadout(
        new Request(`${local}/api/rooms?target=https://evil.example`),
        undefined,
        fetcher
      )
    ).status,
    404
  );
  assert.equal(
    (
      await proxyReadout(
        new Request(`${local}/api/rooms`),
        "https://evil.example",
        fetcher
      )
    ).status,
    503
  );
  assert.equal(calls.length, 1);
});
test("adapter preserves API failures, rejects form writes and permits dotted claim IDs", async () => {
  const fetcher = async () =>
    Response.json({ detail: "No readout yet." }, { status: 404 });
  const response = await proxyReadout(
    new Request(`${local}/api/rooms/hollis_voice/claims/steering.1/sources/0`),
    undefined,
    fetcher
  );
  assert.equal(response.status, 404);
  assert.equal((await response.json()).detail, "No readout yet.");
  assert.equal(
    (
      await proxyReadout(
        new Request(`${local}/api/rooms/hollis_voice/steer`, {
          body: "x=y",
          method: "POST",
        }),
        undefined,
        fetcher
      )
    ).status,
    415
  );
});
