import assert from "node:assert/strict";
import { test } from "node:test";

import {
  emptyRoomState,
  openRoomArrival,
  receiveRoomArrival,
  restoreRoomState,
  roomStorageKey,
  validateRoomArrival,
} from "../src/company/room-arrival-state.ts";

const snapshotAt = "2026-10-24";

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
  snapshotAt,
  stage: sequence === 1 ? "partial" : "full",
  syntheticNotice: "Synthetic, not this company's data.",
  version: 1,
  waiting: [],
});

test("received and opened arrivals survive reopening without opening a pending notice", () => {
  const partial = arrival();
  const received = receiveRoomArrival(
    emptyRoomState("ploy", snapshotAt),
    partial
  );
  assert.equal(received.opened, 0);
  const restored = restoreRoomState(
    "ploy",
    snapshotAt,
    JSON.stringify(received)
  );
  assert.deepEqual(restored, received);
  const opened = openRoomArrival(restored, partial);
  const fullPending = receiveRoomArrival(opened, arrival("ploy", 2));
  assert.equal(fullPending.received, 2);
  assert.equal(fullPending.opened, 1);
  assert.deepEqual(
    restoreRoomState("ploy", snapshotAt, JSON.stringify(fullPending)),
    fullPending
  );
});

test("duplicate and out-of-order arrivals never regress or duplicate the current state", () => {
  const full = arrival("ploy", 2);
  const state = openRoomArrival(
    receiveRoomArrival(emptyRoomState("ploy", snapshotAt), full),
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
    receiveRoomArrival(emptyRoomState("ploy", snapshotAt), partial),
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
  assert.deepEqual(
    restoreRoomState("ploy", snapshotAt),
    emptyRoomState("ploy", snapshotAt)
  );
  for (const value of [
    { ...emptyRoomState("sazabi", snapshotAt) },
    { ...emptyRoomState("ploy", snapshotAt), opened: 1 },
    { ...emptyRoomState("ploy", snapshotAt), received: 2 },
    { ...emptyRoomState("ploy", snapshotAt), received: 3 },
    { ...emptyRoomState("ploy", snapshotAt), version: 2 },
    { ...emptyRoomState("ploy", snapshotAt), injected: true },
  ]) {
    assert.throws(() =>
      restoreRoomState("ploy", snapshotAt, JSON.stringify(value))
    );
  }
  assert.throws(() => restoreRoomState("ploy", snapshotAt, "not JSON"));
});

test("snapshot-scoped progress starts fresh while retaining the previous snapshot unchanged", () => {
  const previousArrival = arrival("ploy", 2);
  const previousState = openRoomArrival(
    receiveRoomArrival(emptyRoomState("ploy", snapshotAt), previousArrival),
    previousArrival
  );
  const nextSnapshot = "2026-10-25";
  const previousKey = roomStorageKey("ploy", snapshotAt);
  const nextKey = roomStorageKey("ploy", nextSnapshot);
  const storage = new Map([[previousKey, JSON.stringify(previousState)]]);
  assert.notEqual(previousKey, nextKey);
  assert.notEqual(nextKey, roomStorageKey("sazabi", nextSnapshot));
  const fresh = restoreRoomState("ploy", nextSnapshot, storage.get(nextKey));
  assert.equal(fresh.received, 0);
  assert.equal(fresh.opened, 0);
  assert.throws(() => receiveRoomArrival(fresh, previousArrival));
  const nextArrival = { ...arrival(), snapshotAt: nextSnapshot };
  const nextState = openRoomArrival(
    receiveRoomArrival(fresh, nextArrival),
    nextArrival
  );
  storage.set(nextKey, JSON.stringify(nextState));
  assert.deepEqual(
    restoreRoomState("ploy", snapshotAt, storage.get(previousKey)),
    previousState
  );
  assert.deepEqual(
    restoreRoomState("ploy", nextSnapshot, storage.get(nextKey)),
    nextState
  );
  assert.throws(() =>
    restoreRoomState("ploy", nextSnapshot, storage.get(previousKey))
  );
  assert.throws(() => validateRoomArrival(nextState, previousArrival));
});
