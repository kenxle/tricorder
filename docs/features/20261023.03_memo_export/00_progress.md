# Feature progress: the memo and its PDF

**Now (2026-10-23, fix round).** The independent associate and partner reviews rated the first memo a checker's report. The fix round takes eight of their points: the first screen is the answer, a partner view with no plumbing is the default for the page and the only view in the PDF, empty sections are one line, flags print once, the recommendation opens the summary, the PDF reads sources as a partner would, the ARR figures sit side by side from claims, and editing is one sitting with a 409 that keeps the work. It also absorbs three integration merges (cohorts, claim support with about 60 pitch claims, per-module claim ids) and steering's replaced claims. Full suite at 2f4aea9: 552 passed, 0 failed; `bin/ci-py` green. Fresh drive on port 8813 ([06_verification.md](06_verification.md)). **Next:** the checkpoint review.

Roadmap slice: [memo-export](../../ongoing/ROADMAP.md#memo-export). Route: prototype first.

## Attention needed

- **Orchestrator: shared files touched.** `server/app.py` gets one import and one `include_router` line, placed just before the page mount (a mount at "/" catches every route added after it). `requirements.txt` gains `reportlab>=4.0` (the PDF; already in `data_room/requirements.txt`). `pyproject.toml` adds `memo` to `testpaths`, or the suite never runs `memo/tests`.
- **Orchestrator: re-run the personas on the fix round.** The independent reviews were of the first build. A cold re-read of `evidence/fix_round/memo_v3.html` and `memo_v3.pdf` would show whether the eight takes landed.
- **Left for later (from the reviews):** narrative for empty sections needs the scans that feed them (deck claims, market signals, comps, founder profiles). The clinic count (357 against 212) was left for later in the brief, but the claims scan now writes it and the memo shows it as red flag "Paying accounts".
- **Claims scan owner: a script path in claim sentences.** Red-flag claim texts end with sentences like "scans/redflags/cohorts.py summed ...", and claim-support texts name check ids ("the redflags scan's rebuild_cohorts_from_customer_file check"). The memo drops or rewords them for partners; the scans could write them for people in the first place.
- **Captain: memo-local composition.** Until the link step writes `connecting` sentences, the memo writes one itself (the ARR figures side by side) and groups flags by subject ([04_architecture.md](04_architecture.md), "Memo-local composition").
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
| Partner view, first screen, one-line sections, flags once | builder | done | `evidence/fix_round/memo_drive.json` (`partner_plumbing: []`, `partner_first_screen`) | none |
| Partner PDF, recommendation first, sources read as words | builder | done | `evidence/fix_round/pdf_check.txt`, `memo_v3.pdf` | none |
| Edit in one sitting, 409 reapply, detach on a new figure | builder | done | `evidence/fix_round/edit_in_page.json`, `memo_edit_*.png` | none |
| Many pitch claims, steered claims, tests robust to new checks | builder | done | `test_the_pitch_claims_read_as_one_line_per_section`, `test_a_claim_the_steer_replaced_is_the_new_lines_before`; suite green after three merges | none |
| Independent review | orchestrator | not started | | checkpoint |
| Persona agents, cold | orchestrator | done on the first build | recorded in [02_prototype_decision.md](02_prototype_decision.md) | re-run on the fix round |

## Decisions and events

- 2026-10-23: worktree from origin/main cc86536. The readout on main has 10 claims, 19 gaps, 27 asks, no pieces or flags; the memo is designed to name what is missing.
- 2026-10-23: the builder module began as the prototype's renderer, and its first tests were written right after it rather than before. The CLI, PDF and routes were test-first (7 red tests, then green), as were the later fixes (dates as figures, operator lines above the coverage closer). Stated plainly so the review can weigh it.
- 2026-10-23: reportlab for the PDF ([04_architecture.md](04_architecture.md), "The PDF").
- 2026-10-23: merged origin/main for `.claude/skills/verify-tricorder/`; drove the recipe on port 8813.
- 2026-10-23, fix round: merged `claude/project-thread-ea11in` four times (red-flag contract terms, cohorts and steering, claim support, per-module ids). Tests now find claims by check name; the fixture runs the claims scan with no model key.
- 2026-10-23, fix round: the container restarted mid-drive; the worktree survived, and the drive was rerun from a fresh launch.
- No approval was needed or given.

## To delete at cleanup

- `/tmp/claude-0/-home-claude/46d40c2c-7610-5980-8cc8-4007978d4e75/scratchpad/memo-export/` (scratch out folders `fix1` to `fix3`, the verify runs `memo-export`, `memo-export-final`, `memo-export-fix` to `memo-export-fix7`, `memo-export-final2`, probe scripts, and the scratch Node Playwright in `pw/`).
- The worktree `/home/claude/wt/memo-export` once merged.
