import assert from "node:assert/strict";
import { test } from "node:test";

import {
  emptyRoomState,
  openRoomArrival,
  receiveRoomArrival,
  restoreRoomState,
  validateRoomArrival,
} from "../src/company/room-arrival-state.ts";

const arrival = (company = "ploy", sequence = 1) => ({
  arrivalId: `${company}:arrival:${sequence}`,
  claims: {},
  company: { name: company, slug: company, website: `https://${company}.com` },
  files: [],
  flags: [],
  gaps: [],
  missingFiles: [],
  provenance: "saved-synthetic-replay",
  roomId: `${company}:room`,
  sequence,
  snapshotAt: "2026-10-24",
  stage: sequence === 1 ? "partial" : "full",
  syntheticNotice: "Synthetic, not this company's data.",
  version: 1,
  waiting: [],
});

test("received and opened arrivals survive reopening without opening a pending notice", () => {
  const partial = arrival();
  const received = receiveRoomArrival(emptyRoomState("ploy"), partial);
  assert.equal(received.opened, 0);
  const restored = restoreRoomState("ploy", JSON.stringify(received));
  assert.deepEqual(restored, received);
  const opened = openRoomArrival(restored, partial);
  const fullPending = receiveRoomArrival(opened, arrival("ploy", 2));
  assert.equal(fullPending.received, 2);
  assert.equal(fullPending.opened, 1);
  assert.deepEqual(
    restoreRoomState("ploy", JSON.stringify(fullPending)),
    fullPending
  );
});

test("duplicate and out-of-order arrivals never regress or duplicate the current state", () => {
  const full = arrival("ploy", 2);
  const state = openRoomArrival(
    receiveRoomArrival(emptyRoomState("ploy"), full),
    full
  );
  assert.equal(receiveRoomArrival(state, full), state);
  assert.equal(receiveRoomArrival(state, arrival()), state);
  assert.equal(openRoomArrival(state, arrival()), state);
  assert.equal(openRoomArrival(state, full), state);
});

test("failed or mismatched arrival validation preserves the last successful state", () => {
  const partial = arrival();
  const state = openRoomArrival(
    receiveRoomArrival(emptyRoomState("ploy"), partial),
    partial
  );
  const before = JSON.stringify(state);
  for (const invalid of [
    arrival("sazabi", 2),
    { ...arrival("ploy", 2), roomId: "other-room" },
    { ...arrival("ploy", 2), snapshotAt: "2027-01-01" },
    { ...arrival("ploy", 2), provenance: "fresh-analysis" },
    { ...arrival("ploy", 2), stage: "partial" },
    { ...arrival("ploy", 2), sequence: 3 },
    { ...arrival("ploy", 2), syntheticNotice: "" },
  ]) {
    assert.throws(() => receiveRoomArrival(state, invalid));
    assert.equal(JSON.stringify(state), before);
  }
  assert.throws(() => validateRoomArrival(state, partial, "full"));
  assert.throws(() => openRoomArrival(state, arrival("ploy", 2)));
});

test("saved metadata rejects foreign, malformed and impossible states", () => {
  assert.deepEqual(restoreRoomState("ploy"), emptyRoomState("ploy"));
  for (const value of [
    { ...emptyRoomState("sazabi") },
    { ...emptyRoomState("ploy"), opened: 1 },
    { ...emptyRoomState("ploy"), received: 2 },
    { ...emptyRoomState("ploy"), received: 3 },
    { ...emptyRoomState("ploy"), version: 2 },
    { ...emptyRoomState("ploy"), injected: true },
  ]) {
    assert.throws(() => restoreRoomState("ploy", JSON.stringify(value)));
  }
  assert.throws(() => restoreRoomState("ploy", "not JSON"));
});
