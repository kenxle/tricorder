import assert from "node:assert/strict";
import { test } from "node:test";

import { savedDraftSchema, snapshotDraft } from "../src/request-ui/draft.ts";

test("saving an untouched generated draft freezes its displayed message and stage", () => {
  const form = {
    custom: "another item",
    customItems: [],
    editedDraft: null,
    selected: { C02: false },
  };
  const displayed =
    "Hi Corrected Founder,\nPlease share the Series A documents for Corrected Company.";
  const saved = snapshotDraft(form, "series_a", displayed);
  const storedJSON = JSON.stringify(saved);
  const restored = savedDraftSchema.parse(JSON.parse(storedJSON));
  assert.equal(restored.stage, "series_a");
  assert.equal(restored.form.editedDraft, displayed);
  assert.equal(restored.form.selected.C02, false);
  assert.equal(restored.form.custom, "another item");
  assert.equal(form.editedDraft, null);
});

test("saved requests reject malformed form bindings, stage and oversized edits", () => {
  const form = { custom: "", customItems: [], editedDraft: null, selected: {} };
  assert.throws(() => snapshotDraft(form, "other", "draft"));
  assert.throws(() => snapshotDraft(form, "seed", "x".repeat(20_001)));
  assert.throws(() =>
    snapshotDraft(
      { ...form, selected: { "../../private": true } },
      "seed",
      "draft"
    )
  );
});
