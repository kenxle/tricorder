# Feature progress: the memo and its PDF

**Now (2026-10-23).** Built, tested and driven on branch `forge/memo-export`. `python3 -m memo data_room/hollis_voice` writes a 16-section draft memo, an offline interactive page and a footnoted PDF from the readout. Every Done when line passes on Hollis Voice ([06_verification.md](06_verification.md)). Full suite: 218 passed, 18 skipped, 0 failed; `bin/ci-py` green. **Next:** the orchestrator's independent review at the checkpoint, and the persona agents run cold on the page.

Roadmap slice: [memo-export](../../ongoing/ROADMAP.md#memo-export). Route: prototype first.

## Attention needed

- **Orchestrator: shared files touched.** `server/app.py` gets one import and one `include_router` line, placed just before the page mount (a mount at "/" catches every route added after it). `requirements.txt` gains `reportlab>=4.0` (the PDF; already in `data_room/requirements.txt`). `pyproject.toml` adds `memo` to `testpaths`, or the suite never runs `memo/tests`.
- **Orchestrator: persona review was not independent.** This session had no subagent tool, so the builder followed the two persona files itself. Run `persona-partner` and `persona-associate` cold on `evidence/memo_v3.html` and the screenshots.
- **Captain (merge steps): the memo waits on three steps.** Until `scans/memo/link.py`, `pieces.py` and `top_flags.py` exist, the memo shows gap lines for the verdicts and the top flags, and the page says agreement is "Not checked yet". Nothing in `memo/` needs to change when they land; the tests already run a readout with pieces and flags (hand-built, labelled).
- **Captain (schema, after Saturday):** `Readout.connecting` as `{text, claim_ids}` and a `Readout.steps_run` list would let the memo show connecting sentences as claim lines and tell "step ran, found nothing" from "step not built" ([04_architecture.md](04_architecture.md), "Proposed schema changes").
- **Template owner: routing without pieces.** The template's row for entry 1.12 puts accounting mislabels in section 6. The memo routes by value label before entry, so the MRR mislabel (label `mrr`) lands in section 7 with traction. Ken's call (PRD question 2).
- **Ken: PDF notes.** Notes print at the end of each section, numbered across the memo, not at the foot of each page (PRD question 1).
- **Scan owners: claim sentences.** The memo shows each claim's own text. The mislabel sentences ("Mislabel kind a: non-recurring revenue in MRR") read as checker output to an associate.
- **Frontend: a mount in the readout page.** The memo is a standalone page at `/api/rooms/<room>/memo.html`. A link from the readout page's masthead would be one line in `App.tsx`, not added here.
- **Verify skill: `control.sh shot` only captures `/`.** The memo page is driven by `spike/drive_memo.js`; the orchestrator may move it into the skill.

## Documents

- [product_thinking.md](product_thinking.md), [01_brief.md](01_brief.md)
- [02_prototype/](02_prototype/) and [02_prototype_decision.md](02_prototype_decision.md): the real and simulated pages, their drive results, the persona review
- [03_prd.md](03_prd.md): ME-R1 to ME-R19, failure cases, questions
- [04_architecture.md](04_architecture.md): the data shape, routing, the PDF choice
- [05_plan.md](05_plan.md): slices and the verification table
- [06_verification.md](06_verification.md) and [evidence/](evidence/): the drive by the verify-tricorder recipe
- Map: [.claude/skills/verify-tricorder/features/memo-export.md](../../../.claude/skills/verify-tricorder/features/memo-export.md)
- `spike/`: `build_prototype.py`, `drive_memo.js`, `edit_in_page.js`

## Work and evidence

| Outcome | Owner | State | Evidence or blocker | Next action |
|---|---|---|---|---|
| Export fills every section or names its gap | builder | done | CLI summary in `evidence/cli_*.txt`; `test_every_section_is_filled_or_names_its_gap` | none |
| Every line to its claims in one click, a claim's source in two | builder | done | `evidence/memo_drive.json` (Chromium, served page) | none |
| Every claim in the PDF footnoted with source and locator | builder | done | `evidence/pdf_check.txt`, `memo_v1.pdf`, `memo_v3.pdf` | none |
| Quote checker passes on every claim in both forms | builder | done | `evidence/pdf_check.txt`; `test_every_claim_in_the_page_passes_the_quote_checker` | none |
| Operator edits, numbered versions, operator lines marked | builder | done | `evidence/edit_in_page.json`, `memo_operator_line_*.png` | none |
| Independent review | orchestrator | not started | | checkpoint |
| Persona agents, cold | orchestrator | not started | no subagent tool here | run both |

## Decisions and events

- 2026-10-23: worktree from origin/main cc86536. The readout on main has 10 claims, 19 gaps, 27 asks, no pieces or flags; the memo is designed to name what is missing.
- 2026-10-23: the builder module began as the prototype's renderer, and its first tests were written right after it rather than before. The CLI, PDF and routes were test-first (7 red tests, then green), as were the later fixes (dates as figures, operator lines above the coverage closer). Stated plainly so the review can weigh it.
- 2026-10-23: reportlab for the PDF ([04_architecture.md](04_architecture.md), "The PDF").
- 2026-10-23: merged origin/main for `.claude/skills/verify-tricorder/`; drove the recipe on port 8813.
- No approval was needed or given.

## To delete at cleanup

- `/tmp/claude-0/-home-claude/46d40c2c-7610-5980-8cc8-4007978d4e75/scratchpad/memo-export/` (scratch out folders, the verify runs `memo-export` and `memo-export-final`, and the scratch Node Playwright in `pw/`).
- The worktree `/home/claude/wt/memo-export` once merged.
