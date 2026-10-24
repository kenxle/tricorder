import assert from "node:assert/strict";
import { once } from "node:events";
import { test } from "node:test";

import type { Spec } from "@json-render/core";

import {
  createRequestSpec,
  requestSpecPatches,
  validateRequestElement,
} from "./catalog.ts";
import type { RequestItem } from "./model.ts";
import { applyRequestPatch, readRequestStream } from "./stream.ts";

const item: RequestItem = {
  ask: "Share the café’s forecast 📊",
  checked: true,
  guidance: "Include assumptions",
  id: "C1",
  reason: "Revenue evidence",
  title: "Forecast",
};
const emptySpec = (): Spec => ({ elements: {}, root: "" });
const encode = (value: unknown) =>
  new TextEncoder().encode(`${JSON.stringify(value)}\n`);
const closedStream = (bytes: Uint8Array) =>
  new ReadableStream<Uint8Array>({
    start(controller) {
      controller.enqueue(bytes);
      controller.close();
    },
  });

test("catalog patches roundtrip to the full request spec", () => {
  for (const items of [[], [item]]) {
    let actual = emptySpec();
    for (const patch of requestSpecPatches(items)) {
      actual = applyRequestPatch(actual, patch);
    }
    assert.deepEqual(actual, createRequestSpec(items));
    assert.deepEqual(
      actual.elements["item-C1"]?.props.checked,
      items.length ? { $bindState: "/selected/C1" } : undefined
    );
  }
});

test("real stream accepts fragmented UTF-8 and renders before completion", async () => {
  const patches = requestSpecPatches([item]);
  const events = new EventTarget();
  const firstUpdate = once(events, "update");
  let streamController: ReadableStreamDefaultController<Uint8Array> | undefined;
  const body = new ReadableStream<Uint8Array>({
    start(controller) {
      streamController = controller;
    },
  });
  const updates: Spec[] = [];
  const result = readRequestStream(
    body,
    (spec) => {
      updates.push(spec);
      events.dispatchEvent(new Event("update"));
    },
    new AbortController().signal
  );
  assert.ok(streamController);
  streamController.enqueue(encode(patches[0]));
  streamController.enqueue(encode(patches[1]));
  await firstUpdate;
  assert.equal(updates.length, 1);
  assert.deepEqual(updates[0].elements.request.children, []);
  // Every UTF-8 code point can cross a chunk boundary, including the emoji.
  const remaining = new TextEncoder().encode(
    patches
      .slice(2)
      .map((patch) => JSON.stringify(patch))
      .join("\n")
  );
  for (const byte of remaining) {
    streamController.enqueue(Uint8Array.of(byte));
  }
  streamController.close();
  assert.deepEqual(await result, createRequestSpec([item]));
  assert.ok(updates.length > 1);
});

test("abort cancels a pending stream reader and releases its lock", async () => {
  let cancelled = false;
  const body = new ReadableStream<Uint8Array>({
    cancel() {
      cancelled = true;
    },
  });
  const controller = new AbortController();
  const result = readRequestStream(
    body,
    () => assert.fail("No layout should arrive"),
    controller.signal
  );
  const rejected = assert.rejects(result, /cancelled/u);
  controller.abort();
  await rejected;
  assert.equal(cancelled, true);
  assert.equal(body.locked, false);
});

test("already aborted requests cancel without accepting queued layouts", async () => {
  const controller = new AbortController();
  controller.abort();
  const body = closedStream(encode(requestSpecPatches([item])[0]));
  await assert.rejects(
    readRequestStream(
      body,
      () => assert.fail("No layout should arrive"),
      controller.signal
    ),
    /cancelled/u
  );
  assert.equal(body.locked, false);
});

test("truncated and malformed streams fail instead of reporting completion", async () => {
  const incomplete = requestSpecPatches([item])
    .slice(0, -1)
    .map((patch) => JSON.stringify(patch))
    .join("\n");
  await assert.rejects(
    readRequestStream(
      closedStream(new TextEncoder().encode(incomplete)),
      () => {},
      new AbortController().signal
    ),
    /before it was complete/u
  );
  await assert.rejects(
    readRequestStream(
      closedStream(new TextEncoder().encode('{"op":"add"')),
      () => {},
      new AbortController().signal
    ),
    SyntaxError
  );
});

test("stream rejects oversized input and cancels its source", async () => {
  let cancelled = false;
  const body = new ReadableStream<Uint8Array>({
    cancel() {
      cancelled = true;
    },
    start(controller) {
      controller.enqueue(new Uint8Array(1_000_001));
    },
  });
  await assert.rejects(
    readRequestStream(body, () => {}, new AbortController().signal),
    /size limit/u
  );
  assert.equal(cancelled, true);
});

test("elements reject unknown components, injected actions and unauthorized state bindings", () => {
  const attacks = [
    { children: [], props: {}, type: "WebView" },
    {
      children: [],
      props: { kind: "delete", label: "Delete" },
      type: "RequestButton",
    },
    {
      children: [],
      on: { press: { action: "delete" } },
      props: { kind: "copy", label: "Copy" },
      type: "RequestButton",
    },
    {
      children: [],
      props: { checked: { $bindState: "/selected/C2" }, item },
      type: "RequestToggle",
    },
    {
      children: [],
      props: { checked: { $bindState: "/__proto__/polluted" }, item },
      type: "RequestToggle",
    },
    {
      children: [],
      props: { checked: { $bindState: "/selected/C1", extra: "unsafe" }, item },
      type: "RequestToggle",
    },
    {
      children: [],
      props: {
        field: "custom",
        label: "Custom",
        value: { $bindState: "/editedDraft" },
      },
      type: "RequestInput",
    },
    {
      children: [],
      props: { field: "draft", label: "Draft", value: { $state: "/secret" } },
      type: "RequestInput",
    },
    { children: ["child"], props: { text: "Text" }, type: "RequestNote" },
  ];
  for (const attack of attacks) {
    assert.throws(() => validateRequestElement(attack));
  }
});

test("patches cannot mutate state, traverse paths, create cycles or reference absent elements", () => {
  const spec = createRequestSpec([item]);
  for (const path of [
    "/state/selected/C1",
    "/elements/__proto__",
    "/elements/constructor",
    "/elements/prototype",
    "/elements/request/props",
    "/elements/item-C1/../../state",
    "/root",
  ]) {
    assert.throws(() =>
      applyRequestPatch(spec, {
        op: "add",
        path,
        value: { children: [], props: {}, type: "RequestStatus" },
      })
    );
  }
  for (const children of [
    ["request"],
    ["missing"],
    ["constructor"],
    ["intro", "intro"],
  ]) {
    assert.throws(() =>
      applyRequestPatch(spec, {
        op: "replace",
        path: "/elements/request/children",
        value: children,
      })
    );
  }
  assert.throws(() =>
    applyRequestPatch(spec, { op: "remove", path: "/elements/status" })
  );
  assert.throws(() =>
    applyRequestPatch(spec, {
      op: "add",
      path: "/elements/nested",
      value: { children: [], props: {}, type: "RequestColumn" },
    })
  );
});

test("completion requires a root and each footer control with its installed meaning", async () => {
  const patches = requestSpecPatches([item]);
  const complete = createRequestSpec([item]);
  const cases = [
    patches.filter((patch) => patch.path !== "/root"),
    [
      ...patches,
      {
        op: "add",
        path: "/elements/status",
        value: {
          children: [],
          props: { text: "Fake status" },
          type: "RequestNote",
        },
      },
    ],
    [
      ...patches,
      {
        op: "add",
        path: "/elements/save",
        value: {
          children: [],
          props: { kind: "copy", label: "Save" },
          type: "RequestButton",
        },
      },
    ],
    [
      ...patches,
      {
        op: "replace",
        path: "/elements/request/children",
        value: complete.elements.request.children?.filter(
          (id) => id !== "draft"
        ),
      },
    ],
  ];
  await Promise.all(
    cases.map(async (updates) => {
      const body = closedStream(
        new TextEncoder().encode(
          updates.map((patch) => JSON.stringify(patch)).join("\n")
        )
      );
      await assert.rejects(
        readRequestStream(body, () => {}, new AbortController().signal),
        /before it was complete/u
      );
    })
  );
});
