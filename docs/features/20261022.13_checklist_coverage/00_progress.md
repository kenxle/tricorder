# Feature progress: checklist coverage

**Now.** Brief, prototype, PRD, architecture and Plan are written. A runnable spike marks every checklist item for a room at a stage and builds the ask list with dedupe. The clickable prototype is built from the spike's real output on the synthetic Hollis Voice rooms. Nothing is committed from this folder yet; the parent thread commits. **Next:** Ken answers the open questions in [02_prototype_decision.md](02_prototype_decision.md); persona review runs when the persona agents exist; then slice 1 of the [Plan](05_plan.md) starts on the merged skeleton.

Roadmap slice: [checklist-coverage](../../ongoing/ROADMAP.md#checklist-coverage). Route: prototype first.

## Attention needed

- **Ken: five design questions and one scope question.** In [02_prototype_decision.md](02_prototype_decision.md) and [03_prd.md](03_prd.md), "Questions". The scope one: the document guides propose 176 checks (`spike/count_proposed_checks.py`, approximate). The roadmap asks for each to become a check or be marked as the operator's. Recommendation: build only the script checks that run on the demo rooms before Saturday, and register the rest.
- **Captain (schema owner): the coverage output fits the frozen schema as two Panels.** `AskItem.piece` cannot be empty, so company-records lines (legal, cap table) go under "the pitch itself" until Ken decides. Proposed additions for after Saturday are in [04_architecture.md](04_architecture.md), "Proposed schema additions".
- **Captain (ask-list step owner): a seam contract.** The ask-list step must keep coverage's lines and call the shared dedupe function ([04_architecture.md](04_architecture.md), "The seam with the ask-list step").
- **Checklist owner: `docs/ongoing/checklist.csv` row C23 has an empty `hollis_voice_file`,** though `data_room/hollis_voice/02_financials/expense_ledger.csv` exists. Not edited here (ongoing docs are off limits to this thread).
- **Skeleton owner: `scans.base.INPUT_KINDS["contracts"]` includes `*/sow_*.pdf`.** Brasswick's `04_contracts/sow_norrgate_software_studio.pdf` reads as a vendor's statement of work, not a customer contract. Coverage keeps SOWs out of customer contracts.
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
| Slices 1 to 4 | builder agents | not started | waits on the skeleton merging to `main` | start slice 1 |

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
- No approvals given or needed yet. Ken's answers are pending.

## To delete at cleanup

- `docs/features/20261022.13_checklist_coverage/spike/out/unknown_stage.json`: an early duplicate of `stage_unknown.json`, from a first run before the name changed.
- `docs/features/20261022.13_checklist_coverage/spike/__pycache__/`: Python bytecode left by importing the spike to check guide mapping.
- `/tmp/claude-0/-home-claude/76c6a462-572c-5250-967a-649aceb49eaf/scratchpad/proto_smoke.js` and `r.sh`: throwaway test helpers outside the repo (under /tmp, which the OS owns; listed only so nobody looks for them).
