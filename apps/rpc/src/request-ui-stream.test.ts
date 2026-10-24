import assert from "node:assert/strict";
import { once } from "node:events";
import { request } from "node:http";
import { test } from "node:test";
import type { TestContext } from "node:test";

import type { RequestUIPatchSource } from "./request-ui-stream.ts";
import { createRPCServer } from "./server.ts";

const fixture = async (
  t: TestContext,
  requestUIPatches?: RequestUIPatchSource
) => {
  const server = createRPCServer({
    apiURL: "http://127.0.0.1:8787",
    requestUIPatches,
  });
  const listening = once(server, "listening");
  server.listen(0, "127.0.0.1");
  await listening;
  t.after(async () => {
    const closed = once(server, "close");
    server.closeAllConnections();
    server.close();
    await closed;
  });
  const address = server.address();
  assert.ok(address && typeof address === "object");
  return `http://127.0.0.1:${address.port}/ui/request`;
};

test("request UI validates queries and saved company existence", async (t) => {
  const url = await fixture(t);
  await Promise.all(
    [
      "",
      "?company=ploy&stage=other",
      "?company=Ploy&stage=seed",
      "?company=ploy&stage=seed&extra=1",
      "?company=ploy&company=ploy&stage=seed",
    ].map(async (query) => {
      const response = await fetch(url + query);
      assert.equal(response.status, 400);
    })
  );
  const missing = await fetch(`${url}?company=missing-company&stage=seed`);
  assert.equal(missing.status, 404);
  const response = await fetch(`${url}?company=ploy&stage=seed`);
  assert.equal(response.status, 200);
  assert.equal(response.headers.get("x-tricorder-ui-version"), "1");
  assert.equal(response.headers.get("content-type"), "application/x-ndjson");
  const body = await response.text();
  assert.ok(body.endsWith("\n"));
  const patches = body
    .trim()
    .split("\n")
    .map((line) => JSON.parse(line));
  assert.ok(patches.length > 0);
  assert.ok(
    patches.every(
      (patch) => typeof patch.op === "string" && typeof patch.path === "string"
    )
  );
});

test("request UI retains GET/host guards and rejects foreign browser origins", async (t) => {
  const url = `${await fixture(t)}?company=ploy&stage=seed`;
  const post = await fetch(url, { method: "POST" });
  assert.equal(post.status, 405);
  const browserHeaders: Record<string, string>[] = [
    { origin: "https://evil.example" },
    { referer: "https://evil.example/page" },
    { "sec-fetch-site": "cross-site" },
  ];
  await Promise.all(
    browserHeaders.map(async (headers) => {
      const response = await fetch(url, { headers });
      assert.equal(response.status, 403);
    })
  );
  const foreignHost = request(url, { headers: { host: "evil.example" } });
  const responseReceived = once(foreignHost, "response");
  foreignHost.end();
  const [response] = await responseReceived;
  response.resume();
  assert.equal(response.statusCode, 403);
});

test("request UI delivers a patch before its source completes and cancels the source", async (t) => {
  const events = new EventTarget();
  const waiting = once(events, "release");
  const cancellation = once(events, "cancelled");
  const source: RequestUIPatchSource = async function* source(_query, signal) {
    try {
      yield { op: "add", path: "/first", value: true };
      await waiting;
      yield { op: "add", path: "/second", value: true };
      if (!signal.aborted) {
        await once(signal, "abort");
      }
    } finally {
      events.dispatchEvent(new Event("cancelled"));
    }
  };
  const url = await fixture(t, source);
  const controller = new AbortController();
  const response = await fetch(`${url}?company=ploy&stage=seed`, {
    signal: controller.signal,
  });
  assert.ok(response.body);
  const reader = response.body.getReader();
  const first = await reader.read();
  assert.equal(
    new TextDecoder().decode(first.value),
    '{"op":"add","path":"/first","value":true}\n'
  );
  events.dispatchEvent(new Event("release"));
  const second = await reader.read();
  assert.equal(
    new TextDecoder().decode(second.value),
    '{"op":"add","path":"/second","value":true}\n'
  );
  controller.abort();
  await cancellation;
});
