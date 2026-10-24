import assert from "node:assert/strict";
import { test } from "node:test";

import { proxyRequestUI } from "../src/request-ui/proxy.ts";

const endpoint = "http://localhost:8081/api/ui/request?company=ploy&stage=seed";
const unused = () => {
  throw new Error("Must not fetch");
};

test("request UI proxy restricts route, query and upstream", async () => {
  await Promise.all(
    [
      "",
      "?company=ploy&stage=no",
      "?company=ploy&stage=seed&extra=1",
      "?company=ploy&company=ploy&stage=seed",
    ].map(async (suffix) => {
      const response = await proxyRequestUI(
        new Request(`http://localhost:8081/api/ui/request${suffix}`),
        undefined,
        unused
      );
      assert.equal(response.status, 400);
    })
  );
  const route = await proxyRequestUI(
    new Request(endpoint.replace("/request?", "/other?")),
    undefined,
    unused
  );
  assert.equal(route.status, 404);
  const method = await proxyRequestUI(
    new Request(endpoint, { method: "POST" }),
    undefined,
    unused
  );
  assert.equal(method.status, 405);
  await Promise.all(
    [
      "https://evil.example",
      "http://user:pass@localhost",
      "http://localhost/path",
      "invalid",
    ].map(async (upstream) => {
      const response = await proxyRequestUI(
        new Request(endpoint),
        upstream,
        unused
      );
      assert.equal(response.status, 503);
    })
  );
});

test("request UI proxy rejects foreign hosts and browser origins", async () => {
  const foreign = await proxyRequestUI(
    new Request(endpoint.replace("localhost", "evil.example")),
    undefined,
    unused
  );
  assert.equal(foreign.status, 403);
  await Promise.all(
    [
      { origin: "https://evil.example" },
      { referer: "https://evil.example/page" },
      { referer: "bad" },
      { "sec-fetch-site": "cross-site" },
    ].map(async (headers) => {
      const response = await proxyRequestUI(
        new Request(endpoint, { headers }),
        undefined,
        unused
      );
      assert.equal(response.status, 403);
    })
  );
});

test("request UI proxy preserves progressive body, version and cancellation", async () => {
  let streamController;
  let cancelled = false;
  const stream = new ReadableStream({
    cancel() {
      cancelled = true;
    },
    start(controller) {
      streamController = controller;
      controller.enqueue(new TextEncoder().encode('{"op":"add"}\n'));
    },
  });
  const abort = new AbortController();
  const request = new Request(endpoint, { signal: abort.signal });
  const response = await proxyRequestUI(
    request,
    "http://127.0.0.1:8789",
    (target, options) => {
      assert.equal(
        String(target),
        "http://127.0.0.1:8789/ui/request?company=ploy&stage=seed"
      );
      assert.equal(options.redirect, "error");
      assert.equal(options.signal, request.signal);
      return Promise.resolve(
        new Response(stream, {
          headers: {
            "Content-Type": "application/x-ndjson",
            "X-Tricorder-UI-Version": "1",
          },
        })
      );
    }
  );
  assert.equal(response.headers.get("x-tricorder-ui-version"), "1");
  assert.equal(response.headers.get("cache-control"), "no-store");
  const reader = response.body.getReader();
  const first = await reader.read();
  assert.equal(new TextDecoder().decode(first.value), '{"op":"add"}\n');
  streamController.enqueue(new TextEncoder().encode('{"op":"replace"}\n'));
  const second = await reader.read();
  assert.equal(new TextDecoder().decode(second.value), '{"op":"replace"}\n');
  await reader.cancel();
  assert.equal(cancelled, true);
  abort.abort();
  assert.equal(request.signal.aborted, true);
});

test("request UI proxy preserves upstream errors", async () => {
  const response = await proxyRequestUI(new Request(endpoint), undefined, () =>
    Promise.resolve(
      Response.json({ detail: "Unknown company" }, { status: 404 })
    )
  );
  assert.equal(response.status, 404);
  assert.deepEqual(await response.json(), { detail: "Unknown company" });
});
