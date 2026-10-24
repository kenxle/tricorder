import assert from "node:assert/strict";
import { test } from "node:test";

import { getPick, listPicks, resetPicks, setPick, subscribePicks, togglePick } from "../src/diligence/memo-picks.ts";

test("insights and flags default into the memo, claims default out", () => {
  resetPicks("t1");
  assert.equal(getPick("t1", "insight:0"), true);
  assert.equal(getPick("t1", "flag:tr-4"), true);
  assert.equal(getPick("t1", "claim:3"), false);
});

test("a pick is shared by every reader and notifies subscribers", () => {
  resetPicks("t2");
  let calls = 0;
  const off = subscribePicks(() => { calls += 1; });
  togglePick("t2", "claim:3");
  setPick("t2", "insight:1", false);
  off();
  assert.equal(getPick("t2", "claim:3"), true);
  assert.equal(getPick("t2", "insight:1"), false);
  assert.equal(calls, 2);
  assert.deepEqual(listPicks("t2"), [{ key: "claim:3", in: true }, { key: "insight:1", in: false }]);
  assert.equal(getPick("other", "claim:3"), false);
});
