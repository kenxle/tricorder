# Plan: steering in one sentence

PRD: [03_prd.md](03_prd.md). Architecture: [04_architecture.md](04_architecture.md).

## Throughput checkpoint

One owner, one sitting. The slices share `steering/engine.py`, so splitting them would mean two writers on one file. Blocking prerequisite: the readout store (this branch is cut from `forge/readout-store`). No other wave 2 builder touches `steering/`, `scans/redflags/cohorts.py` or the new page files. Shared files touched: one import and one `include_router` line in `server/app.py`; `pyproject.toml` `testpaths` gains `steering`; `readout/vite.config.ts` gains a second build input.

## Slices

1. **Entry 1.3, script half** (`scans/redflags/cohorts.py`). Tests first in `scans/redflags/tests/test_cohorts.py`. Lands alone safely: it only adds retention claims.
2. **Verdicts and sentence reading** (`steering/verdicts.py`, `steering/classify.py`, `steering/models.py`). Tests first.
3. **Engine, rereads, rewording, CLI** (`steering/engine.py`, `rereads.py`, `reword.py`, `__main__.py`). Tests first on the real rooms with a temporary out folder and store.
4. **Routes** (`server/steering_routes.py`). Tests first with FastAPI's TestClient.
5. **Page** (`readout/src/Steering.tsx` and the entry). `bin/ci-web`, then driven in Chromium.
6. **Verification map and drive** (`.claude/skills/verify-tricorder/features/steering.md`, `06_verification.md`, `evidence/`).

## Verification

| Requirement | Acceptance or failure case | Command or observation | Owner | Evidence or status |
|---|---|---|---|---|
| STEER-R1, R15 | A first-time user steers one line with one sentence and Enter; the revised line appears under it | Chromium on `/steer.html`, light and dark | builder | evidence/ |
| STEER-R2, R3 | Rules on the demo sentences; model path on hand-built responses; a model answer naming a term not in the sentence falls back | `steering/tests/test_classify.py` | builder | |
| STEER-R4 | "make ARR 3 million" changes no claim; note says the numbers stay | `test_engine.py::test_number_request_*`, CLI transcript | builder | |
| STEER-R5, R6 | "treat the pilot as non-recurring" on traction adds the $2,060,868 line; the check's line stays | `test_engine.py::test_pilot_*`, API response | builder | |
| STEER-R7, R16 | "read the full room" on the seed drop's retention line adds rebuilt NRR and GRR marked new; verdict not enough to weak, moved by the NRR claim | `test_engine.py::test_full_room_*`, API response | builder | |
| STEER-R8 | "pull the competitor's pricing pages" changes nothing and says so | `test_engine.py::test_named_source_*` | builder | |
| STEER-R9 | A rewording that changes a number is refused | `test_engine.py::test_reword_*` (hand-built responses) | builder | |
| STEER-R10 | Every added claim passes the quote checker | `test_engine.py`, and `python -m schema.check_quotes` on the steered readout | builder | |
| STEER-R11 | Verdicts by the FRAMEWORKS rule; says which rebuilt them | `test_verdicts.py` | builder | |
| STEER-R12, R13 | Two steers leave two revisions in the readout and two new store versions | `test_engine.py::test_revisions_kept`, `GET /api/store/demo/<room>/versions` | builder | |
| STEER-R14 | Routes answer; bad piece and empty sentence are 422 | `server/tests/test_steering_routes.py` | builder | |
| 1.3 script half | Seed drop: tab NRR claim and a gap; full room: 87.3% against 102.6%, 68 against 57, GRR 73.4% | `scans/redflags/tests/test_cohorts.py` | builder | |
| Gates | full suite 0 failed; `bin/ci-py`; `bin/ci-web` | commands | builder | |
