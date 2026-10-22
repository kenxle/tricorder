# Plan: checklist coverage

Requirements: [03_prd.md](03_prd.md). Design: [04_architecture.md](04_architecture.md). UI baseline: [02_prototype_decision.md](02_prototype_decision.md) and [02_prototype/prototype.html](02_prototype/prototype.html). Progress: [00_progress.md](00_progress.md).

Builds on the skeleton on branch `claude/project-thread-ce34ga` (schema, `scans/base.py`, `scans/memo/merge.py` with the `coverage` step reserved). Builder's model: Opus (the roadmap marks this slice Judgment: yes).

## Builder's reading list

Read before code: [04_architecture.md](04_architecture.md); [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md) "The shared Claim", "Checklist coverage", "Ask list", 1.10, 1.11; [CHECKLIST.md](../../ongoing/CHECKLIST.md) "How to read the rows"; `schema/claim.py`, `scans/base.py`, `scans/memo/merge.py`; the spike `spike/coverage_spike.py` (its tables are a starting point, not the product).

Rules from [AGENTS.md](../../../AGENTS.md) that bind every slice: never delete a file; plain words and no em dashes in anything a person reads; every count from a script; code lands by PR to `main`.

## Slices

Each slice lands on its own branch `feat/checklist-coverage-<n>` through a PR, with `bin/ci-py` green, and leaves the readout working.

### Slice 1. The checklist module and coverage records

- **Outcome.** `scans/memo/checklist.py` and `scans/memo/coverage.py` exist. `apply()` writes the two Panels for a known stage, and the `stage_unknown` counts Panel otherwise. No ask lines yet.
- **Scope.** ChecklistRow load and validation; `read_stage` (operator.json, deck slide line through `schema.readers.pdf_page`, then `claims.json`); file matching by patterns and the cover note; `ENTRY_CHECKS` and `ROW_CHECKS`; the five statuses.
- **Requirements.** CC-R1, CC-R3, CC-R4, CC-R5, CC-R6, CC-R7, CC-R18 (Panels part), CC-R20.
- **Depends on.** The skeleton merged to `main`.
- **Safe landing.** The merge already skips a missing step; adding it only adds Panels.

### Slice 2. Ask lines and dedupe

- **Outcome.** Coverage appends checklist `AskItem`s; the shared `items_for_gap` and `expected` functions exist; 1.10's script instrument reading writes gaps; 1.11's five asks and their after-term-sheet mark are in.
- **Scope.** Guide ask-line loader; fold of missing checks; `SAME_REQUEST`; held-back gap requests for later stages; C71 handling; the instrument reading over `Cap_Table`'s "SAFE conversion" block and "Options granted" row through `schema.readers.xlsx_sheet`.
- **Requirements.** CC-R8 to CC-R16, CC-R18 (AskItem part).
- **Depends on.** Slice 1.
- **Integration owner.** This slice writes the seam tests; the captain's ask-list step (readout slice) must pass them. If `scans/memo/asks.py` exists when this lands, this slice adds the seam calls to it in the same PR, with the captain as reviewer.

### Slice 3. The operator's stage and the panel

- **Outcome.** A server route sets the stage; the readout page shows the coverage panel per the prototype.
- **Scope.** `POST /rooms/{room}/stage` in `server/app.py` writing `out/<room>/operator.json` and rerunning the merge; a React component in `readout/` reading the two Panels, built against `sample_out/` plus a coverage sample file this slice adds.
- **Requirements.** CC-R2, CC-R19.
- **Depends on.** Slice 1. The readout page's shell (readout-page slice) for the component's home; until it exists, the component ships with a test page.
- **Safe landing.** The page hides the panel when the Panels are absent.

### Slice 4. The guides' proposed-check register

- **Outcome.** `proposed_checks.csv` in this folder lists every proposed check from the 33 guides with a disposition. The ones marked `built` run on the demo rooms.
- **Scope.** A script extracts candidates (`spike/count_proposed_checks.py` is the start: 176 proposed, approximate); a person or agent marks each `built`, `later:<slice>` or `operator`. `built` is limited to script checks over files the demo rooms hold. Candidates: `customer_file_ties_to_pnl`, `customer_file_vs_metrics_counts` (monthly revenue by customer guide), `safe_stack_total`, `pro_forma_roundtrip` (cap table guide). Each becomes a claim in the redflags scan's output through a small PR to that scan, reviewed by its owner.
- **Optional.** `scans/cap_notes/` for 1.10's model question 4, only if Ken wants model readings of cap table notes before Saturday. Hollis Voice's cap table holds one note line (row 2, how SAFEs are shown) and no note naming a grant, so it would find nothing on the demo rooms (read with openpyxl from `data_room/hollis_voice/02_financials/cap_table.xlsx`).
- **Requirements.** CC-R17.
- **Depends on.** Ken's answer to PRD question 6. Independent of slices 1 to 3.

## Throughput checkpoint

- **Blocking prerequisites.** The skeleton on `main` (it is on `claude/project-thread-ce34ga`, landing now). For slice 2's seam: the ask-list step's file name, which is fixed (`scans/memo/asks.py`).
- **Independent workstreams.** Slices 1 and 2 are one stream: they share `checklist.py`. Slice 3's React component can start in parallel against a hand-written sample Panel. Slice 4 is independent.
- **Shared writable state.** `scans/memo/asks.py` (captain's), `server/app.py` (skeleton owner's), `readout/` (frontend's). Each touch goes through a PR with that owner reviewing. `docs/ongoing/checklist.csv` is read only here; fixes to it go to the checklist owner.
- **Smallest safe decomposition.** One agent owns slices 1 and 2 in sequence. A second agent may take slice 3's component. Slice 4's marking is a separate short task. A single owner for 1 to 3 is fine if only one agent is free; the Saturday deadline is the only pressure.

## Verification

Test file: `scans/memo/tests/test_coverage.py` (37 tests; the checklist-module tests live there too), run by `bin/ci-py`. Built test-first on 2026-10-22: the file was written and run red (import error) before `scans/memo/checklist.py` and `scans/memo/coverage.py` existed. Tests run on `data_room/hollis_voice_seed_drop`, `data_room/hollis_voice` and `data_room/brasswick`. TDD: write each named test red, then green. Spike numbers are the expected values to start from; where the product's matching differs from the spike (cover note, `ROW_CHECKS`), the test's number is re-derived by the script and the change noted in Progress.

| Requirement | Acceptance/failure case | Command/observation | Owner | Evidence/status |
|---|---|---|---|---|
| CC-R1 | Seed drop: stage `series_a` from `01_overview/pitch_deck.pdf`, slide 1, quote starts "Series A". Brasswick: `seed`, slide 1. | `test_stage_read_from_deck_cover`, `test_stage_brasswick_is_seed` | slice 1 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R1 | Deck text unreadable: `claims.json` label "Series A raise" gives `series_a`. | `test_stage_falls_back_to_claims_json` (deck reader patched to raise `LocatorError`) | slice 1 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R2 | operator.json says `pre_seed`: stage is `pre_seed`, counts Panel keeps `deck_stage=series_a`; claims, pieces and flags identical to the run without it. | `test_operator_stage_wins_and_changes_nothing_else` | slice 1 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R2 | Route accepts only the three stages; anything else is 422 and writes nothing. | `server/tests/test_app.py::test_set_stage_route` | slice 3 builder | Not started (slice 3). |
| CC-R3 | No deck and no claims.json: label `stage_unknown`, no coverage rows, no checklist asks. | `test_unknown_stage_writes_no_statuses` (tmp room with only a CSV) | slice 1 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R3 | Stage "Series B" (deck or operator): `stage_unknown`, reason names "Series B". | `test_stage_outside_three_is_unknown` | slice 1 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R4 | Seed drop at Series A: 109 records, one status each, counts add to 109. | `test_every_item_has_one_status` | slice 1 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R4 | A CSV with level "maybe" fails `checklist.load`. | `test_load_rejects_unknown_level` | slice 1 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R5 | Fake redflags claim with `check.name` `arr_from_subscription_rows` on the full room marks C05 checked with that claim id; with no claims C05 is not checked. | `test_check_row_needs_a_real_claim` | slice 1 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R5 | A claim from 1.12 kind b does not mark C06 (kind a) checked. | `test_row_checks_are_exact_for_1_12_and_1_13` | slice 1 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R5 | Every entry named in checklist.csv's `checked_by` has a check name in `ENTRY_CHECKS`. | `test_entry_checks_cover_every_entry` | slice 1 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R5 | Seed drop at Series A: C05 `missing` with `missing_inputs` C03 and C34; at pre-seed, C08 `not_checked` because C03 is not expected. | `test_missing_check_names_inputs`, `test_check_with_later_stage_input_is_not_checked` | slice 1 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R5 | An outside row is never `missing`; a check returning `cannot_check` is never `checked`. | `test_outside_rows_never_missing`, `test_cannot_check_is_not_checked` | slice 1 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R6 | Full room: C23 found at `02_financials/expense_ledger.csv` although its `hollis_voice_file` is blank. Brasswick: C34 holds the two order forms and the MSA, not the SOW. | `test_match_by_pattern_not_column`, `test_sow_is_not_a_customer_contract` | slice 1 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R6 | For every Hollis Voice document row whose `hollis_voice_file` names a file, the matcher finds that file (oracle test). | `test_matcher_agrees_with_hollis_voice_column` | slice 1 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R7 | Every record has a non-empty detail cell in the coverage Panel. | `test_every_row_says_why` | slice 1 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R8 | Seed drop at Series A: every missing row has an ask; the "if you have it" lines are exactly those whose covered rows are all "lighter". | `test_every_missing_item_is_asked`, `test_lighter_items_are_if_you_have_it` | slice 2 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R9 | The C03 line covers 19 ids on the seed drop at Series A; no line has a check row as its `checklist_id`. | `test_missing_checks_fold_into_documents` | slice 2 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R10 | Seed drop at pre-seed: no line covers only rows marked no or not stated; the four sample gaps for C03, C34 and C23, and the options gap (C78), get no line. | `test_pre_seed_asks_nothing_expected_later` | slice 2 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R11 | Every line from a document row with a guide uses the guide's quoted request verbatim; no line contains "flag", "fraud" or "discrepan". | `test_ask_text_comes_from_guide`, `test_ask_text_names_no_flag` | slice 2 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R12 | Full room at Series A: C21, C01 and C79 lines start "After the term sheet."; with one flag claim present, no C71 line. | `test_cannot_settle_asks_and_stage`, `test_walk_through_replaced_by_flag_lines` | slice 2 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R13 | Seed drop: three gaps "Not in the room: the signed SAFE for ..." (Tidewater, Hartley, Ostrander) and one for the option grants, each with a `Cap_Table!A<row>` source. | `test_cap_table_instruments_without_documents` | slice 2 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R14 | Merged readout on all three rooms at their deck stage: zero repeated `what`, and no checklist id on both a gap line and a checklist line. | `test_no_request_twice` (runs the real merge with fake scan outputs) | slice 2 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R15 | Seed drop with the four FRAMEWORKS sample gaps: exactly the four gap lines for the expense ledger, monthly revenue by customer, the Marlow pilot agreement and the Cedar & Pine order form; no checklist line for C03, C23 or C34. | `test_gap_wins_over_checklist` (fixture: `spike/sample_gaps_seed_drop.json`) | slice 2 builder, captain reviews | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R16 | Full room at Series A: one line covers C35 and C46. | `test_same_request_rows_fold` | slice 2 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| CC-R17 | `proposed_checks.csv` has one row per proposed check, each with a disposition; every `built` check has a passing test in its scan. | `python3 docs/features/20261022.13_checklist_coverage/spike/count_proposed_checks.py` against the CSV's row count; owner reads the dispositions | slice 4 owner | Not started (slice 4). Ken's default 6: build only checks that run on the demo rooms. |
| CC-R18 | Readout validates as `schema.claim.Readout`; Panels named "checklist coverage" and "checklist coverage counts"; `bin/ci-py` green with no change to `schema/claim.schema.json`. | `test_readout_with_coverage_validates`; `bin/ci-py` | slice 1 and 2 builders | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). Full suite `python3 -m pytest`: 184 passed. No change to `schema/`. |
| CC-R19 | Page on the seed drop: stage line names slide 1; switching to pre-seed shows the diff box and 11 lines; a missing row's link scrolls to its ask; copy reports its count or its failure. Light and dark screenshots on the PR. | `bin/ci-web`; browser check against the prototype; screenshots | slice 3 builder | Prototype rebuilt from the product step; screenshots `02_prototype/screenshot.png` and `screenshot_phone_dark.png` (headless Chromium). The React panel is not started (slice 3). |
| CC-R20 | Coverage runs with the network off and no API key set. | `TRICORDER_OFFLINE=1 python -m scans.memo data_room/hollis_voice_seed_drop` with `ANTHROPIC_API_KEY` unset | slice 1 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). (`test_runs_offline` blocks sockets). |
| Roadmap Done when | "On the seed drop at Series A, coverage lists every checklist item as found, checked or missing, and the counts come from a script." Product reading: every item has a status, including `not_checked` and `not_expected`; counts from the counts Panel. | `test_every_item_has_one_status` plus `bin/smoke data_room/hollis_voice_seed_drop` | slice 1 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). Real merge: `python3 -m scans.memo data_room/hollis_voice_seed_drop` after `python3 -m scans.redflags` writes the coverage Panels and 25 checklist ask lines; counts 3 checked, 15 found, 65 missing, 26 not checked, 0 not expected. |
| Roadmap Done when | "Every missing Series A item becomes one ask-list line. Set to pre-seed, the same room asks for no item expected only later." | `test_every_missing_item_is_asked`, `test_pre_seed_asks_nothing_expected_later` | slice 2 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |
| Roadmap Done when | "No request appears twice when a gap and a checklist item name the same thing." | `test_no_request_twice`, `test_gap_wins_over_checklist` | slice 2 builder | Pass, 2026-10-22: `python3 -m pytest scans/memo/tests/test_coverage.py` (37 passed). |

## Build status, 2026-10-22

Slices 1 and 2 are built (not committed by this thread): `scans/memo/checklist.py`, `scans/memo/coverage.py`, `scans/memo/tests/test_coverage.py`. `scans/memo/asks.py` does not exist yet, so it was not edited. Coverage therefore writes the ask line for every gap that names a checklist item, in the gap's words, and `checklist.gap_is_asked(asks, gap)` is ready for the ask-list step to call before it writes a gap line. Slices 3 and 4 are not started.

## Testing findings and dispositions

No separate testing reviewer was run. From the spike:

- **The seam with the ask-list step is the riskiest part.** Two owners write into `readout.asks`. Disposition: the dedupe rule is one shared function, and `test_no_request_twice` runs the real merge, not coverage alone.
- **"Checked" cannot be tested on real scans before Saturday.** Disposition: fake scan outputs in `tmp_path` with real check names (the pattern in `scans/memo/tests/test_merge.py`), plus the Saturday integration point.
- **Numbers will move.** When the product matcher adds the cover note and `ROW_CHECKS`, counts can differ from the spike's. Disposition: tests assert rules and named rows first, and totals only from the script's own output.

## Rollout and final verification

- Each slice merges to `main` by PR after `bin/ci-py` (and `bin/ci-web` for slice 3) passes and an independent reviewer reads the diff.
- At the Saturday 1:00 PM integration point, rerun `python -m scans.memo` on both demo rooms with the real scan outputs. Check that rows the scans checked flip to `checked` and that `test_no_request_twice` still holds on the real readout.
- Release authority: the captain merges on Saturday ([ROADMAP.md](../../ongoing/ROADMAP.md), "How to read a slice"). Before Saturday, Ken reviews.
