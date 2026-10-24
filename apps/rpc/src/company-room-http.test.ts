import assert from "node:assert/strict";
import { once } from "node:events";
import { test } from "node:test";
import type { TestContext } from "node:test";

import { createRPCServer } from "./server.ts";

const serve = async (t: TestContext, companyRoomData?: () => unknown) => {
  const server = createRPCServer({
    apiURL: "http://127.0.0.1:8787",
    companyRoomData,
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
  return `http://127.0.0.1:${address.port}`;
};

test("room arrivals are repeatable, company-scoped, GET-only saved results", async (t) => {
  const origin = await serve(t);
  await Promise.all(
    ["ploy", "sazabi"].map(async (company) => {
      const path = `${origin}/company/room?company=${company}&stage=full`;
      const response = await fetch(path);
      assert.equal(response.status, 200);
      assert.equal(response.headers.get("cache-control"), "no-store");
      const full = await response.json();
      assert.equal(full.company.slug, company);
      assert.equal(full.provenance, "saved-synthetic-replay");
      const partialResponse = await fetch(
        `${origin}/company/room?company=${company}&stage=partial`
      );
      assert.equal(partialResponse.status, 200);
      const partial = await partialResponse.json();
      assert.equal(partial.sequence, 1);
      assert.equal(full.sequence, 2);
      const replayResponse = await fetch(path);
      assert.deepEqual(await replayResponse.json(), full);
      const postResponse = await fetch(path, { method: "POST" });
      assert.equal(postResponse.status, 405);
      const foreign = await fetch(path, {
        headers: { origin: "https://foreign.example" },
      });
      assert.equal(foreign.status, 403);
    })
  );
  await Promise.all(
    [
      "company=ploy",
      "company=ploy&stage=other",
      "company=ploy&stage=partial&stage=full",
      "company=../ploy&stage=full",
      "company=ploy&stage=full&extra=1",
    ].map(async (query) => {
      const response = await fetch(`${origin}/company/room?${query}`);
      assert.equal(response.status, 400, query);
    })
  );
  const missing = await fetch(
    `${origin}/company/room?company=unknown&stage=full`
  );
  assert.equal(missing.status, 404);
});

test("room fixture failures are retryable and do not expose internals", async (t) => {
  const origin = await serve(t, () => {
    throw new Error("private fixture path");
  });
  const response = await fetch(
    `${origin}/company/room?company=ploy&stage=full`
  );
  assert.equal(response.status, 503);
  assert.doesNotMatch(
    JSON.stringify(await response.json()),
    /private fixture/u
  );
});
