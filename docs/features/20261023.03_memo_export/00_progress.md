# Feature progress: the memo and its PDF

**Landed (closeout, 2026-10-23).** Merged to `main` in PR #8, merge commit `60c45d5`. `bin/ci-py` on `main`: 648 passed, 0 failed; GitHub CI green. Open items now live on the board ([BULLETIN.md](../../BULLETIN.md)): TRI-pieces-top-flags (the verdicts and top flags the memo waits on), TRI-wave2-review-memo-steering (a code review and a persona re-read of the fix round), TRI-wave2-defaults (PDF notes, the MRR mislabel's section), TRI-page-wave2 (the masthead link) and TRI-wave2-small-fixes (the page driver in the verify skill). Wave closeout: [02_closeout.md](../20261022.10_feature_breakdown/02_closeout.md). **Next:** none in this folder. The "Now" paragraph below is the state at hand-off, kept as history.

**Now (2026-10-23, fix round).** The independent associate and partner reviews rated the first memo a checker's report. The fix round takes eight of their points: the first screen is the answer, a partner view with no plumbing is the default for the page and the only view in the PDF, empty sections are one line, flags print once, the recommendation opens the summary, the PDF reads sources as a partner would, the ARR figures sit side by side from claims, and editing is one sitting with a 409 that keeps the work. It also absorbs three integration merges (cohorts, claim support with about 60 pitch claims, per-module claim ids) and steering's replaced claims. `bin/ci-py` at a7b0e56: 648 passed, 0 failed. Fresh drive on port 8813 ([06_verification.md](06_verification.md)). **Next:** the checkpoint review.

Roadmap slice: [memo-export](../../ongoing/ROADMAP.md#memo-export). Route: prototype first.

## Attention needed

- **Orchestrator: shared files touched.** `server/app.py` gets one import and one `include_router` line, placed just before the page mount (a mount at "/" catches every route added after it). `requirements.txt` gains `reportlab>=4.0` (the PDF; already in `data_room/requirements.txt`). `pyproject.toml` adds `memo` to `testpaths`, or the suite never runs `memo/tests`.
- **Orchestrator: re-run the personas on the fix round.** The independent reviews were of the first build. A cold re-read of `evidence/fix_round/memo_v3.html` and `memo_v3.pdf` would show whether the eight takes landed.
- **Left for later (from the reviews):** narrative for empty sections needs the scans that feed them (deck claims, market signals, comps, founder profiles). The clinic count (357 against 212) was left for later in the brief, but the claims scan now writes it and the memo shows it as red flag "Paying accounts".
- **Claims scan owner: a script path in claim sentences.** Red-flag claim texts end with sentences like "scans/redflags/cohorts.py summed ...", and claim-support texts name check ids ("the redflags scan's rebuild_cohorts_from_customer_file check"). The memo drops or rewords them for partners; the scans could write them for people in the first place.
- **Captain: memo-local composition.** Until the link step writes `connecting` sentences, the memo writes one itself (the ARR figures side by side) and groups flags by subject ([04_architecture.md](04_architecture.md), "Memo-local composition").
- **Captain (merge steps): the memo waits on three steps.** Until `scans/memo/link.py`, `pieces.py` and `top_flags.py` exist, the memo shows gap lines for the verdicts and the top flags, and the page says agreement is "Not checked yet". Nothing in `memo/` needs to change when they land; the tests already run a readout with pieces and flags (hand-built, labelled).
- **Captain (schema, after Saturday):** `Readout.connecting` as `{text, claim_ids}` and a `Readout.steps_run` list would let the memo show connecting sentences as claim lines and tell "step ran, found nothing" from "step not built" ([04_architecture.md](04_architecture.md), "Proposed schema changes").
- **Template owner: routing without pieces.** The template's row for entry 1.12 puts accounting mislabels in section 6. The memo routes by value label before entry, so the MRR mislabel (label `mrr`) lands in section 7 with traction. Open for Ken (PRD question 2).
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
| Independent review | orchestrator | done (wave 2b) | `docs/features/20261022.10_feature_breakdown/review_wave2b.md` | fix round below, merged with the steering half |
| Persona agents, cold | orchestrator | done on the first build | recorded in [02_prototype_decision.md](02_prototype_decision.md) | re-run on the fix round |

## Review round (wave 2b)

Branch `fix/wave2b-memo`, from origin/main b948d09. Each test was run red against the code before the fix (by checking the old file out, running, and applying the fix back), then green.

| Finding | Fix | Commit | Test, red then green |
|---|---|---|---|
| B1, memo and server half: a steered seed drop's lines checked and opened in the seed drop (34 could not verify, 404 from `/source` and `/files`) | The memo build (quote check, `read_sources`, the PDF notes, the ARR side by side) and `POST /source` and `GET /files` resolve sources through `scans.memo.merge.reads_room` / `readout_room`, then `memo/rooms.py` keeps the file inside the readout's room or the one full room the marker names | 7d9b26a, 3ce33f4, da23932 | `memo/tests/test_steered_room.py`: export has 0 could not verify; the PDF notes the customer file; `POST /api/rooms/hollis_voice_seed_drop/source` for a `.steer1` line's source gives 200, `/files` too; before a steer both stay 404 |
| S1: chained `str.replace` let a line expand `{{DATA}}` and put markup in the page | One regex pass over the template (`memo.html.fill`); the embedded JSON escapes `<`, `>`, `&`, U+2028/9. No banner, numbered contents, no edge stripe kept | dbc1269 | `test_a_line_cannot_expand_a_placeholder_or_carry_markup` |
| S2: `POST /source` read any file (repo files, answer keys, other rooms) | `memo.rooms.resolve`: no absolute path, no `..`, no `answer_key*`, only the room (or its switched full room); 404 otherwise | 7d9b26a | `server/tests/test_app.py::test_source_refuses_any_path_outside_the_room` (6 paths), `test_source_refuses_an_answer_key_even_inside_a_room`; `memo/tests/test_rooms.py` |
| S3, memo half: edits of any size; PDF rebuilt on every GET | Limits in `memo/model.py` (line 2,000, author 80, batch 100, claims a line 50, operator lines a memo 500): 422 from the route, EditError from the CLI. Each version's PDF built once to `memo_v<N>.pdf` under a per-room lock; `GET memo.pdf` serves it | cba90b3 | `test_oversized_edits_are_refused_before_anything_is_saved`, `test_the_pdf_is_built_once_per_version` |
| S4: a lost race was a 500, and an edit could land on a newer version | The route passes the version it checked into `edit(base=...)`; `store.save` is an exclusive create (temp file, then `os.link`); `FileExistsError` is the same 409 with `latest_version`. `POST /memo` too | cba90b3 | `test_a_save_that_loses_the_race_is_a_409_not_a_500`, `test_racing_saves_of_one_version_make_one_version` (8 threads: one version) |
| O3: PDF notes short of ME-R14 | File sources carry the export's read date (`SourceText.read_at`); every note prints a date. ME-R14 amended: the claim id stays out of the PDF (ME-R20) | b53cef8 | `test_every_claim_in_the_pdf_has_a_note_naming_its_file_and_locator` (every note dated) |
| O4: the CLI ignored `TRICORDER_ROOMS_DIR` | `founder_requests.intake.rooms_root()`, as the server | 7de4522 | `test_cli_finds_a_readouts_room_under_tricorder_rooms_dir` |

Not done here, and why:

- B1 names `schema.check_quotes`' own CLI as a reader too. `schema/` is frozen for this round, so that CLI still checks against the room it is given. Pass the full room to it by hand after a switch.
- `scans/memo/merge.py` on this branch holds a stand-in of the steering branch's `reads_room` and `readout_room`, copied verbatim. Take `fix/wave2b-steering`'s version at merge.
- On this branch alone, `server/tests/test_steering_routes.py::test_a_full_room_line_opens_from_the_seed_drop_page` fails: it asserted the old 404 from `POST /source`. The steering branch removes that assertion. A trial merge of both branches in scratch passed the whole suite.

Real path, in scratch (offline, no key): `bin/smoke` on hollis_voice and its seed drop, then `python3 -m memo` on the seed drop gave 71 claims, 0 could not verify; after `steering.engine.steer(..., "retention", "read the full room")` the export gave version 2, 78 claims, 0 could not verify (the review saw 48 and 34). Over HTTP (uvicorn on port 8841, stopped by its pid): the `.steer1` line's `/source` and `/files` 200; `../../CLAUDE.md`, the answer key by absolute path and another room's CSV 404; the `{{DATA}}` and `<img onerror>` lines saved and rendered as text; a 2,001-character line and an 81-character author 422; `GET memo.pdf` twice in 0.016 s each; six concurrent edits on one version gave one 200 and five 409s, versions `[1,2,3,4]`.

## Decisions and events

- 2026-10-23: worktree from origin/main cc86536. The readout on main has 10 claims, 19 gaps, 27 asks, no pieces or flags; the memo is designed to name what is missing.
- 2026-10-23: the builder module began as the prototype's renderer, and its first tests were written right after it rather than before. The CLI, PDF and routes were test-first (7 red tests, then green), as were the later fixes (dates as figures, operator lines above the coverage closer). Stated plainly so the review can weigh it.
- 2026-10-23: reportlab for the PDF ([04_architecture.md](04_architecture.md), "The PDF").
- 2026-10-23: merged origin/main for `.claude/skills/verify-tricorder/`; drove the recipe on port 8813.
- 2026-10-23, fix round: merged `claude/project-thread-ea11in` four times (red-flag contract terms, cohorts and steering, claim support, per-module ids). Tests now find claims by check name; the fixture runs the claims scan with no model key.
- 2026-10-23, fix round: the container restarted mid-drive; the worktree survived, and the drive was rerun from a fresh launch.
- No approval was needed or given.

## To delete at cleanup

- `/tmp/claude-0/-home-claude/46d40c2c-7610-5980-8cc8-4007978d4e75/scratchpad/memo-export/` (scratch out folders `fix1` to `fix3`, the verify runs `memo-export`, `memo-export-final`, `memo-export-fix` to `memo-export-fix7`, `memo-export-final2`, `memo-export-guard`, probe scripts, and the scratch Node Playwright in `pw/`).
- The worktree `/home/claude/wt/memo-export` once merged.
- The worktree `/home/claude/wt/fix-memo` and branch `fix/wave2b-memo` once merged.
- `/tmp/claude-0/-home-claude/46d40c2c-7610-5980-8cc8-4007978d4e75/scratchpad/fix-memo/` (patches, `ci.log`, `integ.log`, the `run/` out, store and cache, `uvicorn.log`, `uvicorn.pid`), and the trial-merge worktree at `.../scratchpad/fix-memo/integ` (detached; remove with `git worktree remove`).
