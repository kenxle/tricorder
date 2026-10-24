import assert from "node:assert/strict";
import { request } from "node:http";
import { test, type TestContext } from "node:test";
import { createTRPCClient, httpBatchLink, TRPCClientError } from "@trpc/client";
import type { AppRouter } from "./router.ts";
import { createRPCServer } from "./server.ts";

async function fixture(t: TestContext, upstream: typeof globalThis.fetch) {
  const server = createRPCServer({ apiURL: "http://127.0.0.1:8787", fetch: upstream });
  await new Promise<void>((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolve);
  });
  t.after(() => new Promise<void>((resolve, reject) => {
    server.closeAllConnections();
    server.close((error) => error ? reject(error) : resolve());
  }));
  const address = server.address();
  assert(address && typeof address === "object");
  const url = `http://127.0.0.1:${address.port}/trpc`;
  return { url, client: createTRPCClient<AppRouter>({ links: [httpBatchLink({ url })] }) };
}

test("typed HTTP client batches room list and readout against the Python routes", async (t) => {
  const rooms = [{ id: "hollis_voice", path: "data_room/hollis_voice", inputs: ["deck"], has_readout: true }];
  const readout = { company: "Hollis Voice", claims: [] };
  const calls: string[] = [];
  const { client } = await fixture(t, async (input, init) => {
    const url = new URL(String(input));
    calls.push(url.pathname);
    assert.equal(init?.redirect, "error");
    assert(init?.signal);
    assert.equal(url.origin, "http://127.0.0.1:8787");
    return Response.json(url.pathname === "/api/rooms" ? rooms : readout);
  });
  const results = await Promise.all([client.room.list.query(), client.room.readout.query("hollis_voice")]);
  assert.deepEqual(results, [rooms, readout]);
  assert.deepEqual(calls.sort(), ["/api/rooms", "/api/rooms/hollis_voice/readout"]);
});

test("invalid room input never reaches Python", async (t) => {
  let calls = 0;
  const { client } = await fixture(t, async () => {
    calls += 1;
    return Response.json({});
  });
  await assert.rejects(client.room.readout.query("../outside"), (error: unknown) =>
    error instanceof TRPCClientError && error.data.code === "BAD_REQUEST");
  assert.equal(calls, 0);
});

for (const [status, code] of [[404, "NOT_FOUND"], [403, "FORBIDDEN"], [422, "BAD_REQUEST"]] as const) {
  test(`upstream ${status} retains its detail and maps to ${code}`, async (t) => {
    const { client } = await fixture(t, async () => Response.json({ detail: "no room 'missing'" }, { status }));
    await assert.rejects(client.room.readout.query("missing"), (error: unknown) =>
      error instanceof TRPCClientError && error.data.code === code && error.message === "no room 'missing'");
  });
}

test("Python internal failures do not expose upstream details", async (t) => {
  const { client } = await fixture(t, async () => Response.json({ detail: "private traceback" }, { status: 500 }));
  await assert.rejects(client.room.list.query(), (error: unknown) =>
    error instanceof TRPCClientError && error.data.code === "BAD_GATEWAY" && !error.message.includes("private"));
});

test("an unreachable Python API reports service unavailable", async (t) => {
  const { client } = await fixture(t, async () => { throw new Error("private socket detail"); });
  await assert.rejects(client.room.list.query(), (error: unknown) =>
    error instanceof TRPCClientError && error.data.code === "SERVICE_UNAVAILABLE" && !error.message.includes("private"));
});

test("malformed successful JSON reports a gateway error", async (t) => {
  const { client } = await fixture(t, async () => new Response("not JSON"));
  await assert.rejects(client.room.list.query(), (error: unknown) =>
    error instanceof TRPCClientError && error.data.code === "BAD_GATEWAY");
});

test("Host guard rejects DNS rebinding and POST requests before Python", async (t) => {
  let calls = 0;
  const { url } = await fixture(t, async () => {
    calls += 1;
    return Response.json([]);
  });
  const status = await new Promise<number | undefined>((resolve, reject) => {
    const req = request(`${url}/room.list`, { headers: { Host: "attacker.example" } }, (res) => {
      res.resume();
      resolve(res.statusCode);
    });
    req.on("error", reject);
    req.end();
  });
  assert.equal(status, 403);
  const response = await fetch(`${url}/room.list`, { method: "POST", body: "anything" });
  assert.equal(response.status, 405);
  assert.equal(response.headers.get("access-control-allow-origin"), null);
  assert.equal(calls, 0);
});

test("oversized batches are rejected before any Python calls", async (t) => {
  let calls = 0;
  const { url } = await fixture(t, async () => {
    calls += 1;
    return Response.json([]);
  });
  const response = await fetch(`${url}/${Array(11).fill("room.list").join(",")}?batch=1`);
  assert.equal(response.status, 400);
  assert.equal(calls, 0);
});
