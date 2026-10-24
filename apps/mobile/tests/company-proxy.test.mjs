import assert from "node:assert/strict";
import { test } from "node:test";

import { proxyCompany } from "../src/company/proxy.ts";

const origin = "http://localhost:8081";
const endpoint = `${origin}/api/company/readout?url=https%3A%2F%2Fploy.ai`;
const unused = () => {
  throw new Error("Must not fetch");
};

test("company proxy accepts only exact routes and bounded, unambiguous queries", async () => {
  const invalidQueries = [
    "/api/company/readout",
    "/api/company/readout?url=",
    "/api/company/readout?url=%20",
    "/api/company/readout?url=ploy.ai&extra=1",
    "/api/company/readout?url=ploy.ai&url=sazabi.com",
    `/api/company/readout?url=${"x".repeat(2049)}`,
    "/api/company/section?company=ploy",
    "/api/company/section?company=ploy&section=wrong",
    "/api/company/section?company=ploy&section=founders&section=outside",
    "/api/company/section?company=ploy&section=founders&url=elsewhere",
    "/api/company/section?company=..&section=founders",
    "/api/company/section?company=ploy%2Foutside&section=founders",
    `/api/company/section?company=${"x".repeat(101)}&section=founders`,
  ];
  await Promise.all(
    invalidQueries.map(async (path) => {
      const response = await proxyCompany(
        new Request(`${origin}${path}`),
        undefined,
        unused
      );
      assert.equal(response.status, 400, path);
    })
  );
  const route = await proxyCompany(
    new Request(`${origin}/api/company/anything`),
    undefined,
    unused
  );
  assert.equal(route.status, 404);
  const method = await proxyCompany(
    new Request(endpoint, { method: "POST" }),
    undefined,
    unused
  );
  assert.equal(method.status, 405);
});

test("company proxy rejects foreign hosts, browser origins and nonlocal upstreams", async () => {
  await Promise.all(
    [
      { origin: "https://evil.example" },
      { referer: "https://evil.example/page" },
      { referer: "invalid" },
      { "sec-fetch-site": "cross-site" },
    ].map(async (headers) => {
      const response = await proxyCompany(
        new Request(endpoint, { headers }),
        undefined,
        unused
      );
      assert.equal(response.status, 403);
    })
  );
  const foreignHost = await proxyCompany(
    new Request(endpoint.replace("localhost", "evil.example")),
    undefined,
    unused
  );
  assert.equal(foreignHost.status, 403);
  await Promise.all(
    [
      "https://evil.example",
      "http://localhost.evil.example",
      "http://user:pass@localhost",
      "http://localhost/path",
      "http://localhost?target=elsewhere",
      "http://localhost#fragment",
      "file:///tmp/fixture.json",
      "invalid",
    ].map(async (upstream) => {
      const response = await proxyCompany(
        new Request(endpoint),
        upstream,
        unused
      );
      assert.equal(response.status, 503, upstream);
    })
  );
});

test("company proxy forwards a company URL as data only and preserves errors", async () => {
  await Promise.all(
    [200, 400, 404, 503].map(async (status) => {
      const body =
        status === 200 ? { version: 1 } : { detail: "Saved data unavailable" };
      const response = await proxyCompany(
        new Request(endpoint, { headers: { origin } }),
        "http://127.0.0.1:8789",
        (target, options) => {
          assert.equal(target.origin, "http://127.0.0.1:8789");
          assert.equal(target.pathname, "/company/readout");
          assert.equal(target.searchParams.get("url"), "https://ploy.ai");
          assert.equal(options.method, "GET");
          assert.equal(options.redirect, "error");
          assert.ok(options.signal instanceof AbortSignal);
          return Response.json(body, { status });
        }
      );
      assert.equal(response.status, status);
      assert.equal(response.headers.get("cache-control"), "no-store");
      assert.deepEqual(await response.json(), body);
    })
  );
  const response = await proxyCompany(
    new Request(
      `${origin}/api/company/section?company=sazabi&section=founders`,
      { headers: { referer: `${origin}/?company=sazabi.com` } }
    ),
    "http://127.0.0.1:8789",
    (target) => {
      assert.equal(
        String(target),
        "http://127.0.0.1:8789/company/section?company=sazabi&section=founders"
      );
      return Response.json({ section: "founders" });
    }
  );
  assert.equal(response.status, 200);
});

test("company proxy propagates cancellation and reports connection failures", async () => {
  const controller = new AbortController();
  const request = new Request(endpoint, { signal: controller.signal });
  const deferred = Promise.withResolvers();
  const promise = proxyCompany(
    request,
    "http://127.0.0.1:8789",
    (_url, options) => {
      options.signal.addEventListener("abort", () =>
        deferred.reject(options.signal.reason)
      );
      return deferred.promise;
    }
  );
  controller.abort();
  const cancelled = await promise;
  assert.equal(cancelled.status, 504);
  const unavailable = await proxyCompany(new Request(endpoint), undefined, () =>
    Promise.reject(new Error("ECONNREFUSED"))
  );
  assert.equal(unavailable.status, 502);
  const body = await unavailable.json();
  assert.match(body.detail, /local RPC server is unavailable/u);
});
