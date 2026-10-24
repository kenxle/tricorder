import assert from "node:assert/strict";
import { test } from "node:test";

import { highlightSegments, validSelection } from "../src/annotations/model.ts";
import {
  annotationStorageKey,
  createAnnotationStore,
} from "../src/annotations/store-core.ts";

const memoryStorage = () => {
  const values = new Map();
  return {
    getItem: (name) => values.get(name) ?? null,
    setItem: (name, value) => values.set(name, value),
  };
};

const target = {
  blockId: "revenue",
  scopeId: "company:ploy",
  scopeLabel: "Ploy · Revenue",
  text: "Revenue grew 30% last year.",
};

const input = { comment: "Check the contracts.", end: 15, start: 0, target };

test("two associates retain attribution and exact evidence across persona changes and restart", () => {
  const storage = memoryStorage();
  const store = createAnnotationStore(storage);
  const mutableTarget = { ...target };
  assert.equal(
    store.getState().addAnnotation({ ...input, target: mutableTarget }),
    true
  );
  mutableTarget.text = "Changed elsewhere";
  store.getState().setPersona("alex");
  assert.equal(
    store
      .getState()
      .addAnnotation({ ...input, comment: "Reconcile to the ledger." }),
    true
  );
  store.getState().setPersona("jordan");
  const restored = createAnnotationStore(storage).getState();
  assert.equal(restored.personaId, "jordan");
  assert.deepEqual(
    restored.annotations.map(({ authorId }) => authorId),
    ["maya", "alex"]
  );
  assert.equal(restored.annotations[0].target.text, target.text);
  assert.equal(restored.annotations[0].quote, "Revenue grew 30");
  assert.notEqual(restored.annotations[0].id, restored.annotations[1].id);
  assert.ok(Number.isFinite(Date.parse(restored.annotations[0].createdAt)));
  assert.equal(restored.storageError, null);
});

test("the GP can read existing annotations but cannot add one", () => {
  const store = createAnnotationStore(memoryStorage());
  store.getState().addAnnotation(input);
  store.getState().setPersona("jordan");
  assert.equal(store.getState().addAnnotation(input), false);
  assert.equal(store.getState().annotations.length, 1);
  store.getState().setPersona("not-a-persona");
  assert.equal(store.getState().personaId, "jordan");
});

test("selection mode is transient, associate-only and cleared by persona changes", () => {
  const storage = memoryStorage();
  const store = createAnnotationStore(storage);
  store.getState().setSelectingText(true);
  assert.equal(store.getState().selectingText, true);
  assert.equal(store.getState().annotations.length, 0);
  assert.equal(createAnnotationStore(storage).getState().selectingText, false);
  store.getState().setPersona("alex");
  assert.equal(store.getState().selectingText, false);
  store.getState().setSelectingText(true);
  store.getState().setPersona("jordan");
  store.getState().setSelectingText(true);
  assert.equal(store.getState().selectingText, false);
  store.getState().setPersona("maya");
  store.getState().setSelectingText(true);
  store.getState().setSelectingText(false);
  assert.equal(store.getState().selectingText, false);
});

test("invalid selections and empty comments never enter the diligence record", () => {
  const store = createAnnotationStore(memoryStorage());
  for (const invalid of [
    { comment: "  " },
    { start: -1 },
    { start: 0.5 },
    { end: Number.NaN },
    { end: target.text.length + 1 },
    { end: 0 },
    { end: 1, start: 2 },
    { end: 8, start: 7 },
    { target: { ...target, scopeId: "" } },
  ]) {
    assert.equal(
      store.getState().addAnnotation({ ...input, ...invalid }),
      false
    );
  }
  assert.deepEqual(store.getState().annotations, []);
});

test("persistence failures do not report success or append unsaved annotations", () => {
  const storage = memoryStorage();
  const store = createAnnotationStore(storage);
  assert.equal(store.getState().addAnnotation(input), true);
  const initial = storage.getItem(annotationStorageKey);
  storage.setItem = () => {
    throw new Error("Disk unavailable");
  };
  assert.equal(store.getState().addAnnotation(input), false);
  assert.equal(store.getState().annotations.length, 1);
  assert.match(store.getState().storageError, /not been saved/u);
  assert.equal(storage.getItem(annotationStorageKey), initial);
  store.getState().setPersona("alex");
  assert.equal(store.getState().personaId, "maya");
});

test("malformed, future-version, forged-author and mismatched-quote records restore safely", () => {
  const storage = memoryStorage();
  const store = createAnnotationStore(storage);
  store.getState().addAnnotation(input);
  const valid = JSON.parse(storage.getItem(annotationStorageKey));
  const [annotation] = valid.annotations;
  const invalidRecords = [
    "{broken",
    JSON.stringify({ ...valid, version: 2 }),
    JSON.stringify({ ...valid, personaId: "unknown" }),
    JSON.stringify({
      ...valid,
      annotations: [{ ...annotation, authorId: "jordan" }],
    }),
    JSON.stringify({
      ...valid,
      annotations: [{ ...annotation, quote: "Different evidence" }],
    }),
    JSON.stringify({ ...valid, annotations: [annotation, annotation] }),
  ];
  for (const record of invalidRecords) {
    storage.setItem(annotationStorageKey, record);
    const restored = createAnnotationStore(storage).getState();
    assert.deepEqual(restored.annotations, []);
    assert.equal(restored.personaId, "maya");
    assert.match(restored.storageError, /could not be restored/u);
    assert.equal(storage.getItem(annotationStorageKey), record);
  }
});

test("overlapping annotations preserve every character and reject changed source snapshots", () => {
  const store = createAnnotationStore(memoryStorage());
  store.getState().addAnnotation({ ...input, end: 12, start: 0 });
  store.getState().addAnnotation({ ...input, end: 15, start: 8 });
  const { annotations } = store.getState();
  const segments = highlightSegments(target.text, annotations);
  assert.equal(segments.map(({ text }) => text).join(""), target.text);
  assert.deepEqual(
    segments.map(({ start, end, annotationIds }) => [
      start,
      end,
      annotationIds.length,
    ]),
    [
      [0, 8, 1],
      [8, 12, 2],
      [12, 15, 1],
      [15, target.text.length, 0],
    ]
  );
  assert.deepEqual(
    highlightSegments("Updated revenue", annotations).map(
      ({ highlighted }) => highlighted
    ),
    [false]
  );
});

test("selection uses native UTF-16 offsets without splitting surrogate pairs", () => {
  const text = "A 🚀 company";
  assert.equal(validSelection(text, 2, 4), true);
  assert.equal(validSelection(text, 2, 3), false);
  assert.equal(validSelection(text, 3, 4), false);
  const store = createAnnotationStore(memoryStorage());
  assert.equal(
    store.getState().addAnnotation({
      ...input,
      end: 4,
      start: 2,
      target: { ...target, text },
    }),
    true
  );
  assert.equal(store.getState().annotations[0].quote, "🚀");
  assert.equal(
    highlightSegments(text, store.getState().annotations)[1].text,
    "🚀"
  );
});

test("identical qualifiers in different evidence items never share annotations", async () => {
  const { annotationsForTarget } = await import("../src/annotations/model.ts");
  const first = {
    blockId: "company says",
    scopeId: "company:sazabi/outside/evidence:one",
    scopeLabel: "Sazabi · source one",
    text: "company says",
  };
  const second = {
    ...first,
    scopeId: "company:sazabi/outside/evidence:two",
    scopeLabel: "Sazabi · source two",
  };
  const note = {
    authorId: "maya",
    comment: "Verify this source",
    createdAt: "2026-10-24T19:00:00.000Z",
    end: 7,
    id: "one",
    quote: "company",
    start: 0,
    target: first,
  };
  assert.equal(annotationsForTarget([note], first).length, 1);
  assert.equal(annotationsForTarget([note], second).length, 0);
  assert.equal(
    annotationsForTarget([note], { ...first, text: "independently verified" })
      .length,
    0
  );
});
