# Feature progress: checklist coverage

**Now.** Slices 1 and 2 of the [Plan](05_plan.md) are built test-first and not yet committed: `scans/memo/checklist.py`, `scans/memo/coverage.py` and `scans/memo/tests/test_coverage.py` (37 tests). Full suite: `python3 -m pytest`, 184 passed (2026-10-22). The memo merge on the seed drop writes the coverage Panels and 25 checklist ask lines. The prototype is rebuilt from the product step, with Ken's six defaults applied and the chip overflow fixed, and has screenshots. **Next:** the parent commits; Ken reviews the defaults; slice 3 (operator stage route and the React panel) and slice 4 (guide-check register).

Roadmap slice: [checklist-coverage](../../ongoing/ROADMAP.md#checklist-coverage). Route: prototype first.

## Attention needed

- **Ken: six defaults were set for you on 2026-10-22,** listed in [02_prototype_decision.md](02_prototype_decision.md), "Defaults set". Override any of them; each is one table or one function.
- **Ask-list step owner (captain):** `scans/memo/asks.py` does not exist yet, so it was not edited. When it is written, it must call `scans.memo.checklist.gap_is_asked(readout.asks, gap)` before writing a gap line and keep coverage's lines ([04_architecture.md](04_architecture.md), "As built").
- **Deck-vs-books owner:** the red-flag scan writes claims with check names `deck_history_vs_metrics` and `deck_revenue_vs_pnl`. No checklist row names them, so they check nothing in coverage. If they should check a row (C27 or C65 are candidates), say which and it is one line in `ROW_CHECKS`.

- **Ken: five design questions and one scope question.** In [02_prototype_decision.md](02_prototype_decision.md) and [03_prd.md](03_prd.md), "Questions". The scope one: the document guides propose 176 checks (`spike/count_proposed_checks.py`, approximate). The roadmap asks for each to become a check or be marked as the operator's. Recommendation: build only the script checks that run on the demo rooms before Saturday, and register the rest.
- **Captain (schema owner): the coverage output fits the frozen schema as two Panels.** `AskItem.piece` cannot be empty, so company-records lines (legal, cap table) go under "the pitch itself" until Ken decides. Proposed additions for after Saturday are in [04_architecture.md](04_architecture.md), "Proposed schema additions".
- **Captain (ask-list step owner): a seam contract.** The ask-list step must keep coverage's lines and call the shared dedupe function ([04_architecture.md](04_architecture.md), "The seam with the ask-list step").
- **Checklist owner: `docs/ongoing/checklist.csv` row C23 has an empty `hollis_voice_file`,** though `data_room/hollis_voice/02_financials/expense_ledger.csv` exists. Not edited here (ongoing docs are off limits to this thread). Coverage finds it by file name anyway (`test_match_by_pattern_not_column`).
- **Skeleton owner: `scans.base.INPUT_KINDS["contracts"]` includes `*/sow_*.pdf`.** Brasswick's `04_contracts/sow_norrgate_software_studio.pdf` reads as a vendor's statement of work, not a customer contract. Coverage keeps SOWs out of customer contracts (`test_sow_is_not_a_customer_contract`). Whether `INPUT_KINDS` should change is the skeleton owner's call.
- **Roadmap wording.** Its Done when says coverage marks every item "found, checked or missing". Items not expected at the stage, and check rows with no check built, need two more statuses (`not_expected` from FRAMEWORKS, and `not_checked`). The PRD reads the Done when that way.

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
| Persona review of the prototype | persona-review thread | pending | persona agents not built yet | run associate and partner personas; record in 02_prototype_decision.md |
| PRD, architecture, Plan | this thread | done | linked above | Ken's answers may change CC-R10, CC-R17, the piece mapping |
| Slice 1: checklist module and coverage records | this thread | built, uncommitted | `python3 -m pytest scans/memo/tests/test_coverage.py`: 37 passed; full suite 184 passed | parent commits |
| Slice 2: ask lines and dedupe | this thread | built, uncommitted | same run; real merge output below | parent commits |
| Slice 3: operator stage route and React panel | builder | not started | needs the readout page shell | start |
| Slice 4: guide-check register | builder | not started | Ken's default 6 sets the scope | start |
| Prototype on product output, chips wrap | this thread | done | `02_prototype/screenshot.png`, `02_prototype/screenshot_phone_dark.png` | Ken reviews |

### Product counts (real merge)

From `TRICORDER_OUT_DIR=<scratch> python3 -m scans.redflags data_room/<room>` then `python3 -m scans.memo data_room/<room>`, read from the readout's "checklist coverage counts" Panel, 2026-10-22. Stage from the deck (Series A, slide 1). Every room is synthetic.

| Room | Checked | Found | Missing | Not checked yet | Not expected | Ask lines | If you have it | After term sheet | Checked rows |
|---|---|---|---|---|---|---|---|---|---|
| Seed drop, Series A | 3 | 15 | 65 | 26 | 0 | 25 | 7 | 3 | C02, C19, C20 |
| Full room, Series A | 11 | 16 | 40 | 42 | 0 | 21 | 7 | 3 | C02, C03, C06, C07, C09, C10, C19, C20, C23, C25, C26 |

Top five on the seed drop, by checklist id requested: C03 (monthly revenue by customer), C34 (customer contracts), C23 (expense ledger), C35 (customer references), C04 (investor updates). Missing is higher than in the spike because "not stated" items are now expected (Ken's default 1), and "checked" now needs a real claim.

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

## Decisions and events

- 2026-10-22, by 19:58 UTC (file time of the earliest surviving spike output): spike running on branch `claude/project-thread-dfe7j4`.
- 2026-10-22: the skeleton builder pushed `schema/claim.py`, `scans/base.py` and `scans/memo/merge.py` on `claude/project-thread-ce34ga`. Coverage is a merge step `scans/memo/coverage.py` with `apply(readout, room_dir) -> Readout`, after `top_flags` and before `asks`. Architecture and Plan use those names.
- 2026-10-22: decided the gap's words win over the checklist's when both name one document (CC-R15), so the readout slice's four seed-drop lines survive.
- 2026-10-22: decided missing checks fold into their input document's request (CC-R9).
- 2026-10-22 20:03 UTC: docs written.
- 2026-10-22: coordinator set six defaults for Ken's questions; code and prototype follow them.
- 2026-10-22: slices 1 and 2 built test-first; prototype rebuilt from the product step; chip overflow, phone-width overflow and a duplicate expense-ledger line fixed.
- No approvals given or needed yet. Ken's answers are pending.

## To delete at cleanup

- `docs/features/20261022.13_checklist_coverage/spike/run_all.sh`, `print_counts.py` and `spike/out/`: the spike's runner and outputs, superseded by the product step once Ken has read the spike counts.
- `scans/memo/__pycache__/` and `scans/memo/tests/__pycache__/` entries for the new modules (git-ignored).
- Scratch files under `/tmp/claude-0/.../scratchpad/` (`out/`, `measure.html`, `phone.html`): left to the OS.

- `docs/features/20261022.13_checklist_coverage/spike/out/unknown_stage.json`: an early duplicate of `stage_unknown.json`, from a first run before the name changed.
- `docs/features/20261022.13_checklist_coverage/spike/__pycache__/`: Python bytecode left by importing the spike to check guide mapping.
- `/tmp/claude-0/-home-claude/76c6a462-572c-5250-967a-649aceb49eaf/scratchpad/proto_smoke.js` and `r.sh`: throwaway test helpers outside the repo (under /tmp, which the OS owns; listed only so nobody looks for them).
