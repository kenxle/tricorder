# Feature progress: checklist coverage

**Now.** Slices 1 and 2 of the [Plan](05_plan.md) are merged to `main` in PR #4 on 2026-10-23 (merge commit `dc10bbc`): `scans/memo/checklist.py`, `scans/memo/coverage.py` and `scans/memo/tests/test_coverage.py`. Every Done when check in the roadmap slice passes, and the slice is marked done. The memo merge writes the coverage Panels and the checklist ask lines. The prototype is rebuilt from the product step, with the six defaults the orchestrator chose (open for Ken), and has screenshots. **Next:** slice 3 (operator stage route and the React panel) and slice 4 (guide-check register), on board row TRI-coverage-panel.

Roadmap slice: [checklist-coverage](../../ongoing/roadmap/checklist-coverage.md). Route: prototype first.

## Attention needed

1. **Ken: six defaults, chosen by the orchestrator on 2026-10-22, open for Ken.** Listed in [02_prototype_decision.md](02_prototype_decision.md), "Defaults set". They answer the five design questions and the scope question first asked there. Override any of them; each is one table or one function.
2. **Captain (ask-list step owner, Saturday): the seam with `scans/memo/asks.py`.** That step does not exist yet. When it is written, it must keep coverage's lines and call `scans.memo.checklist.gap_is_asked(readout.asks, gap)` before writing a gap line ([04_architecture.md](04_architecture.md), "The seam with the ask-list step"). Board row TRI-asks-seam.
3. **Builder: slices 3 and 4, and the persona review.** The operator's stage route and the coverage panel on the readout page, and the register of the guides' proposed checks (176 by `spike/count_proposed_checks.py`, approximate). The persona agents now exist, so the prototype's persona review can run. Board row TRI-coverage-panel.
4. **Builder: the 84 rows added to the checklist (C110 to C193).** They carry stage columns. The five new document rows (C110 to C114) have no file pattern in `DOC_PATTERNS`, so they always read missing; C111 (consulting agreements) is asked of Brasswick although its room holds `04_contracts/sow_norrgate_software_studio.pdf`. The code comments in `scans/memo/checklist.py` still call the defaults "Ken's default". Board row TRI-checklist-new-rows.
5. **Checklist owner: `docs/ongoing/checklist.csv` row C23 has an empty `hollis_voice_file`,** though `data_room/hollis_voice/02_financials/expense_ledger.csv` exists. Coverage finds it by file name anyway (`test_match_by_pattern_not_column`). Board row TRI-c23-hollis-file.
6. **Skeleton owner: `scans.base.INPUT_KINDS["contracts"]` includes `*/sow_*.pdf`.** Brasswick's `04_contracts/sow_norrgate_software_studio.pdf` is a vendor's statement of work, not a customer contract. Coverage keeps SOWs out of customer contracts (`test_sow_is_not_a_customer_contract`). Board row TRI-input-kinds-sow.
7. **Captain (schema owner), after Saturday: company-records lines.** `AskItem.piece` cannot be empty, so legal and cap table lines go under "the pitch itself" (default 2). Proposed schema additions are in [04_architecture.md](04_architecture.md), "Proposed schema additions".

Closed on 2026-10-23:

- The deck-vs-books check names now check C65 (review S9).
- The roadmap's Done when said "found, checked or missing". The slice's status line now names `not_checked` and `not_expected` too, and FRAMEWORKS "Checklist coverage" lists `not_checked` in its status enum.

## Release record

- PR #4, merged to `main` on 2026-10-23, merge commit `dc10bbc` (PR head `229f8db`, GitHub CI green on it).
- Tests: `bin/ci-py` on `main`, 203 passed. `test_coverage.py` holds 42 of them.
- Acceptance: the real merge on each room (counts below, from the script).
- Real output shown to Ken on the wave 1 demo page, built by [build_demo.py](../20261022.10_feature_breakdown/demo/build_demo.py).
- Unverified: the ask-list seam (item 2), slices 3 and 4 (CC-R2 route, CC-R17, CC-R19 panel), the persona review.

### Counts on main at closeout (193 checklist items)

From `TRICORDER_OUT_DIR=<scratch> python3 -m scans.redflags data_room/<room>` then `python3 -m scans.memo data_room/<room>`, read from the readout's "checklist coverage counts" Panel, 2026-10-23, on `main` after PR #4. Stage from the deck. Every room is synthetic.

| Room | Stage | Checked | Found | Missing | Not checked yet | Not expected | Ask lines | If you have it | After term sheet |
|---|---|---|---|---|---|---|---|---|---|
| Seed drop | Series A | 7 | 14 | 68 | 104 | 0 | 30 | 12 | 3 |
| Full room | Series A | 13 | 15 | 45 | 120 | 0 | 27 | 12 | 3 |
| Brasswick | seed | 12 | 10 | 53 | 114 | 4 | 32 | 21 | 2 |

Not expected is 0 at Series A because no row of `checklist.csv` says "no" for Series A, and "not stated" counts as expected (default 1). Of the 84 new rows, 75 are check rows and all read "not checked yet": no built check carries their check names.

## Documents

- [product_thinking.md](product_thinking.md): the job, evidence, assumptions, priority
- [01_brief.md](01_brief.md): short brief
- [02_prototype/prototype.html](02_prototype/prototype.html) and [02_prototype_decision.md](02_prototype_decision.md): the prototype, what it shows, open questions, persona review (pending)
- [03_prd.md](03_prd.md): requirements CC-R1 to CC-R20 and failure cases
- [04_architecture.md](04_architecture.md): data shapes, the merge step, the seam, alternatives
- [05_plan.md](05_plan.md): four slices, throughput checkpoint, the verification table
- `spike/`: `coverage_spike.py`, `build_prototype.py`, `prototype_template.html`, `print_counts.py`, `count_proposed_checks.py`, `run_all.sh`, `sample_gaps_seed_drop.json`, and `out/*.json`

## Work and evidence

| Outcome | Owner | State | Evidence or blocker | Next action |
|---|---|---|---|---|
| Spike runs on seed drop, full room and Brasswick | this thread | done | `sh docs/features/20261022.13_checklist_coverage/spike/run_all.sh`; counts below from `spike/print_counts.py` | none |
| Prototype built from spike output | this thread | done | `02_prototype/prototype.html`; script run under Node with a stubbed DOM for every room, stage and filter, no error | Ken clicks through it |
| Persona review of the prototype | builder | pending | the persona agents now exist (PERSONA_REVIEWS.md) | run associate and partner personas; record in 02_prototype_decision.md |
| PRD, architecture, Plan | this thread | done | linked above | Ken's answers may change CC-R10, CC-R17, the piece mapping |
| Slice 1: checklist module and coverage records | this thread | merged in PR #4 | `python3 -m pytest scans/memo/tests/test_coverage.py`: 42 passed after the fix round; full suite 203 passed | none |
| Slice 2: ask lines and dedupe | this thread | merged in PR #4 | same run; real merge output below | none |
| Slice 3: operator stage route and React panel | builder | not started | needs the readout page shell | start |
| Slice 4: guide-check register | builder | not started | default 6 (chosen by the orchestrator, open for Ken) sets the scope | start |
| Prototype on product output, chips wrap | this thread | done | `02_prototype/screenshot.png`, `02_prototype/screenshot_phone_dark.png` | Ken reviews |

### Product counts (real merge)

From `TRICORDER_OUT_DIR=<scratch> python3 -m scans.redflags data_room/<room>` then `python3 -m scans.memo data_room/<room>`, read from the readout's "checklist coverage counts" Panel, 2026-10-22. Stage from the deck (Series A, slide 1). Every room is synthetic.

| Room | Checked | Found | Missing | Not checked yet | Not expected | Ask lines | If you have it | After term sheet | Checked rows |
|---|---|---|---|---|---|---|---|---|---|
| Seed drop, Series A | 3 | 15 | 65 | 26 | 0 | 25 | 7 | 3 | C02, C19, C20 |
| Full room, Series A | 11 | 16 | 40 | 42 | 0 | 21 | 7 | 3 | C02, C03, C06, C07, C09, C10, C19, C20, C23, C25, C26 |

Top five on the seed drop, by checklist id requested: C03 (monthly revenue by customer), C34 (customer contracts), C23 (expense ledger), C35 (customer references), C04 (investor updates). Missing is higher than in the spike because "not stated" items are now expected (default 1, chosen by the orchestrator, open for Ken), and "checked" now needs a real claim.

Differences from the design: the matcher uses file patterns plus "contained in" rules (a sheet, a page or a cell inside another file), not the cover note fallback in CC-R6. The `hollis_voice_file` column is used only as a test oracle (`test_matcher_agrees_with_hollis_voice_column`).

### Spike counts

From `python3 docs/features/20261022.13_checklist_coverage/spike/print_counts.py`, after `run_all.sh`. "Checked" is projected: no scan has run. Every room is synthetic.

| Run | Expected | Checked (projected) | Found | Missing | Not checked yet | Not expected | Ask lines | If you have it | After term sheet | Gap asks held back | Repeated requests | Missing with no ask |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Seed drop, Series A (deck's stage, 4 sample gaps) | 96 | 20 | 18 | 53 | 5 | 13 | 23 | 2 | 3 | 0 | 0 | 0 |
| Seed drop, seed | 91 | 20 | 18 | 45 | 8 | 18 | 20 | 10 | 1 | 1 | 0 | 0 |
| Seed drop, pre-seed | 55 | 20 | 18 | 11 | 8 | 52 | 11 | 4 | 0 | 5 | 0 | 0 |
| Seed drop, Series A, no sample gaps | 96 | 20 | 18 | 53 | 5 | 13 | 22 | 2 | 3 | 0 | 0 | 0 |
| Full room, Series A (deck's stage) | 96 | 41 | 21 | 28 | 6 | 13 | 19 | 2 | 3 | 0 | 0 | 0 |
| Full room, seed | 91 | 41 | 21 | 24 | 6 | 17 | 17 | 7 | 1 | 0 | 0 | 0 |
| Full room, pre-seed | 55 | 24 | 21 | 11 | 4 | 49 | 11 | 4 | 0 | 1 | 0 | 0 |
| Brasswick, seed (deck's stage) | 91 | 39 | 18 | 30 | 5 | 17 | 20 | 7 | 1 | 0 | 0 | 0 |

Seed drop at Series A, missing by kind: 17 documents, 33 checks, 3 founder asks. Full room at Series A: 14, 11 and 3. The stage-unknown run (`--stage series_b`) writes label `stage_unknown` and no statuses.

Spike limits, stated plainly: "checked" is a projection from inputs being present; the four seed-drop gaps are hand-written from FRAMEWORKS "Ask list" worked example, not scan output; matching uses `hollis_voice_file` first, which is wrong for Brasswick (the PRD's CC-R6 drops it as the matcher); the 1.10 instrument reading is a script over the SAFE block only.

## Review fix round (wave 1, 2026-10-22)

Review: `docs/features/20261022.10_feature_breakdown/review_wave1.md`. Each behavior fix had a failing test first (`python3 -m pytest scans/memo/tests/test_coverage.py`: 5 failed, then 42 passed).

| Finding | Disposition | Evidence |
|---|---|---|
| S9. Deck-vs-books claims never check C65 | Fixed. `deck_revenue_vs_pnl` and `deck_history_vs_metrics` added to entry 1.5's check names. | `test_deck_vs_books_claims_check_c65`; real merge: C65 checked on both Hollis Voice rooms |
| S10. C06 on the seed drop said "Cannot run" though a kind a claim ran | Fixed. A check row with a claim is `checked`; a missing input is still asked for and the row folds into that line. PRD CC-R5 updated. | `test_check_that_ran_without_a_missing_file_is_checked_and_still_asked`; real merge: C06 and C10 checked on the seed drop |
| S11a. `test_no_request_twice` did not run the merge | Fixed. It now runs `build_readout` with a fake redflags result on disk, including two gaps for one document. The seam with `asks.py` stays untested because that step does not exist; the Plan's row says so. | test passes |
| S11b. `test_cannot_check_is_not_checked` proved nothing | Fixed. It now shows the gap alone leaves C81 not checked and a claim checks it. PRD CC-R5 says a `cannot_check` result writes a gap and no claim. | test passes |
| S11c. Offline test patched too little | Fixed. Also patches `socket.socket.connect`. | `test_runs_offline` |
| S12. PRD and code disagree on file matching | Docs fixed to match the code: patterns, then contained-in rules. The PRD's own reasoning supports it: the cover note lists the same files the patterns already see, so the fallback would add nothing on these rooms. Deferred until a room needs it. | CC-R6, architecture flow, Plan slice 1 |
| U8. Founder text had cell references; balance-sheet gap tagged C03 | Taken. File and cell locations move from `what` to `why`; `items_for_gap` reads the gap's `what` first and `would_need` only when `what` names nothing; "balance sheet" maps to C20. | `test_founder_text_has_no_cell_reference`, `test_balance_sheet_gap_is_not_revenue_by_customer` |
| U9. `ask_line` counted coverage's own lines | Taken. It is now the position in `readout.asks`. | `test_ask_line_numbers_are_positions_in_readout_asks` |
| U5 (duplicate gaps in redflags.json) | Not coverage's to fix; coverage already merges them into one ask line. | `test_two_gaps_for_one_document_ask_once` |

Real merge after the fixes (redflags then memo, scratch out dir): seed drop 7 checked (C02, C06, C10, C19, C20, C60, C65), 14 found, 63 missing, 25 not checked, 25 ask lines; full room 13 checked, 15 found, 40 missing, 41 not checked, 22 ask lines.

Full suite at the end of this round: `python3 -m pytest`, 203 passed, 0 failed (2026-10-22). One earlier run in the round showed 2 failures in `scans/redflags/tests/test_deck_vs_books.py` while that builder's own test-first round was in progress; they passed on the rerun. The prototype and `02_prototype/screenshot.png` were rebuilt from the fixed step.

## Decisions and events

- 2026-10-22, by 19:58 UTC (file time of the earliest surviving spike output): spike running on branch `claude/project-thread-dfe7j4`.
- 2026-10-22: the skeleton builder pushed `schema/claim.py`, `scans/base.py` and `scans/memo/merge.py` on `claude/project-thread-ce34ga`. Coverage is a merge step `scans/memo/coverage.py` with `apply(readout, room_dir) -> Readout`, after `top_flags` and before `asks`. Architecture and Plan use those names.
- 2026-10-22: decided the gap's words win over the checklist's when both name one document (CC-R15), so the readout slice's four seed-drop lines survive.
- 2026-10-22: decided missing checks fold into their input document's request (CC-R9).
- 2026-10-22 20:03 UTC: docs written.
- 2026-10-22: the coordinator set six defaults for Ken's questions, open for Ken; code and prototype follow them.
- 2026-10-22: slices 1 and 2 built test-first; prototype rebuilt from the product step; chip overflow, phone-width overflow and a duplicate expense-ledger line fixed.
- 2026-10-22: Ken's checklist update on `main` grew the list from 109 to 193 items. A coverage test that hard-coded 109 broke; it now reads the count from `checklist.csv` (commit `b9ab9c4`).
- 2026-10-23: merged in PR #4.
- No approvals given or needed yet. Ken's answers on the defaults are pending.

## To delete at cleanup

- `docs/features/20261022.12_accounting_mislabels/spike/test_rooms/`: generated test rooms from the wave (untracked). The same line is on the other wave 1 pages.
- The worktree `/tmp/claude-0/-home-claude/76c6a462-572c-5250-967a-649aceb49eaf/scratchpad/wt2` and its local branch `tmp-ce34ga`, used to merge the skeleton branch. Its work is on `main` through PR #2 and PR #4. Remove with `git worktree remove --force` and `git branch -D tmp-ce34ga`.

- `docs/features/20261022.13_checklist_coverage/spike/run_all.sh`, `print_counts.py` and `spike/out/`: the spike's runner and outputs, superseded by the product step once Ken has read the spike counts.
- `scans/memo/__pycache__/` and `scans/memo/tests/__pycache__/` entries for the new modules (git-ignored).
- Scratch files under `/tmp/claude-0/.../scratchpad/` (`out/`, `measure.html`, `phone.html`): left to the OS.

- `docs/features/20261022.13_checklist_coverage/spike/out/unknown_stage.json`: an early duplicate of `stage_unknown.json`, from a first run before the name changed.
- `docs/features/20261022.13_checklist_coverage/spike/__pycache__/`: Python bytecode left by importing the spike to check guide mapping.
- `/tmp/claude-0/-home-claude/76c6a462-572c-5250-967a-649aceb49eaf/scratchpad/proto_smoke.js` and `r.sh`: throwaway test helpers outside the repo (under /tmp, which the OS owns; listed only so nobody looks for them).
