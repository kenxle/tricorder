# Feature progress: steering in one sentence

**Landed (closeout, 2026-10-23).** Merged to `main` in PR #8, merge commit `60c45d5`. `bin/ci-py` on `main`: 648 passed, 0 failed; GitHub CI green. Open items now live on the board ([BULLETIN.md](../../BULLETIN.md)): TRI-wave2-defaults (a steer may add a figure), TRI-pieces-top-flags (retire `steering/verdicts.py`), TRI-wave2-review-memo-steering, TRI-page-wave2 (the duplicate 357 clinics line) and TRI-wave2-small-fixes (the operator name). Wave closeout: [02_closeout.md](../20261022.10_feature_breakdown/02_closeout.md). **Next:** none in this folder. The "Now" paragraph below is the state at hand-off, kept as history.

**Now.** Fix round done on `forge/steering`, merged with `claude/project-thread-ea11in` (claims scan and claim support included). All eight items pass, driven through `control.sh` on port 8815 and in Chromium ([06_verification.md](06_verification.md)). Full suite after the last merge (320244e): 532 passed, 6 failed, the 6 known memo tests only. An earlier merge also showed 3 founder-requests failures; the integration branch has since fixed them. **Next:** the orchestrator merges.

Roadmap slice: [steering](../../ongoing/roadmap/steering.md). Route: prototype first.

## Attention needed

1. **Ken: a definition steer may add a new figure** beside the check's, labelled as the steer's. The coordinator made that call; Ken can reverse it ([03_prd.md](03_prd.md), question 1).
2. **Claims scan owner:** traction shows "gives paying customers as 357 clinics" twice (`evidence/fix_round/steer_traction_dark.png`).
3. **Readout slice owner (captain): `scans/memo/pieces.py` and `top_flags.py` still do not exist.** `steering/verdicts.py` is the stand-in; the readout page's overview now comes from `/steerable`, which uses it.
4. **Shared files touched:** `readout/src/App.tsx` (one import, the Overview section swapped for `SteerableSection`; the up and down buttons moved into it; a top flag now scrolls to its piece); `server/app.py` (one `include_router`); `pyproject.toml` testpaths; `readout/vite.config.ts`.
5. **Entry 1.3 owner:** `scans/redflags/cohorts.check()` now returns `(claims, gaps, panels)` and adds the panel "cohort retention rebuild".
6. **Setting:** `TRICORDER_OPERATOR` names who steers when the request does not. Unset, lines read "the operator's steer".
7. **Schema proposals** (captain, after Saturday): [04_architecture.md](04_architecture.md), "Proposed schema changes".

## Review round (wave 2b)

Review: `docs/features/20261022.10_feature_breakdown/review_wave2b.md` (worktree `review2`). Branch `fix/wave2b-steering` from main b948d09. Every test below was run red on b948d09's code (a scratch worktree with only the new test files copied in) and green on this branch.

| Finding | Fix | Commit | Test, red then green |
|---|---|---|---|
| B1, steering half | The switch is an explicit Panel `{"name": "reads room", "columns": ["Room", "Since"], "rows": [["<full room>", "steer <n>"]]}`, written by the switching steer and kept by every later steer and rebuild. `scans.memo.merge.reads_room(readout, room_dir)` and `readout_room(room_dir)` resolve it (and the older `source` row), only to the seed drop's own sibling full room. The memo and `server/app.py` halves are the memo builder's. | b5c8e46 | `test_the_full_room_marker_is_an_explicit_panel`, `test_rebuilding_a_switched_seed_drop_keeps_the_full_room` |
| S3, steer half | Size limits on `SteerBody`: sentence 1,000 raw, author 80, claim_id 120, piece and fund 64; the engine also holds author and line id. | b5c8e46 | `test_an_oversized_steer_field_is_422` (author and fund were 200 before), `test_a_name_at_the_limit_is_kept` |
| S5 | A definition after "don't", "do not", "never" or "not" is skipped, on the rules and the model path; the rest of the sentence is still read. | 10b9165 | `test_a_negated_definition_is_not_read_as_the_definition`, `test_a_negated_definition_still_reads_the_full_room`, `test_a_model_definition_on_a_negated_sentence_is_dropped`, `test_a_negated_definition_steer_adds_no_scenario_line` |
| S6 | `_merge_piece` keeps the operator's scenario lines out of the rerun, so they stay; a repeated pilot steer adds no copy and says so. | b5c8e46 | `test_a_later_rewrite_keeps_the_earlier_scenario_line`, `test_a_second_pilot_steer_keeps_the_first_line` |
| S7 | `build_readout` keeps a steered readout's revisions, steer panels, scenario lines, model rewordings and switch (`steering.engine.carry`), and a switched seed drop rebuilds from the full room's results. All three rebuild paths call it. `python -m scans.memo <room> --fresh` is the one way to start over. | b5c8e46, 978ec0f | `test_rebuilding_keeps_revisions_scenario_lines_and_panels`, `test_rebuilding_through_the_page_keeps_the_steer`, `test_the_merge_command_keeps_steers_and_starts_over_only_when_asked` |
| S8 | `reword.guard`: figures in order with units, each against the same source word, and the same agree, differ, up, down and negation words. A refused rewording keeps the line's words. Tested on HAND-BUILT model answers. | b5c8e46 | `test_a_rewording_that_swaps_two_figures_is_refused`, `test_a_rewording_that_changes_the_meaning_is_refused` (three cases) |
| S9 | "Matches" only within `match_tolerance` and on the same customer count. A tab below the rebuild by more than the tolerance is a watch that states the difference. | a761a3c | `test_a_tab_far_below_the_rebuild_is_not_a_match`, `test_a_tab_within_tolerance_with_more_customers_says_so` |
| O1 | A number is a request only after a request frame ("should be", "make", "use", "change ... to"); a bare year never is. PRD STEER-R4 says so. | 10b9165 | `test_a_number_with_no_request_frame_is_not_a_number_request`, `test_more_number_requests` |
| O2 | Every scan runs before any result is written; a crash raises `ScanFailed`, and the route answers 500 "redflags failed: ...". | b5c8e46 | `test_a_scan_that_crashes_during_a_steer_names_the_scan_and_writes_nothing`, `test_a_scan_crash_is_a_500_naming_the_scan` |

Changed on purpose: the hand-built plain rewording in `test_model_reword_keeps_numbers_and_quotes` used to turn "differs ... a gap of" into "lower", which the S8 guard now refuses; it keeps "differs" now. The assertion in `test_a_full_room_line_opens_from_the_seed_drop_page` that `POST .../source` is 404 after a switch pinned the B1 bug and is gone; the memo builder's test of that route replaces it.

Known limit: a founder file added to a switched seed drop is saved in the seed drop, but the rebuild reads the full room's results, so it shows only when the full room has it too.

## Code review of the fix round

A code review of the integrated wave 2b fix round (`git diff origin/main...8e7ba43`). Branch `fix/wave2b-round2` from 8e7ba43. Each new test was run red before its fix, then green. In item 5 the answer-key cases were red; the repo-file case was already a 404.

| Item | Fix | Commit | Test, red then green |
|---|---|---|---|
| 1. A line reworded twice came back with its first rewording after a rebuild | A second steer reran the piece's scans and reverted steer 1's words, so its model reworded the scan text, and `carry` mapped each rewording one step. `with_wording` now puts every earlier rewording back on the fresh merge before each steer and each rebuild, following A to B to C (`last_wording`, cycle-safe), so a valueless line also keeps its id | 89fbe81 | `test_a_line_reworded_twice_keeps_its_last_wording_and_id_after_a_rebuild`, `test_a_later_steer_that_reruns_the_scans_keeps_an_earlier_rewording` |
| 2. "from A to B" read A | A number right after "from" is skipped when another number follows; the frame's word class admits "%" | ab623a2 | `test_the_number_asked_for_is_the_one_read` ("Change ARR from $3M to $2.5M", "Update NRR from 120% to 110%") |
| 3. "Use the 2024 ARR of $2.1M" and "set the customer count to 2000" read nothing | A four-digit number right after a frame word (to, be, use, make, set, at, as and the like) is a request when the frame matches; the frame reaches five words. A bare year still is not (O1 tests green) | ab623a2 | `test_the_number_asked_for_is_the_one_read`, `test_a_bare_year_is_still_not_a_request` |
| 4. Curly "isn’t" and "aren’t" missed; "Why not treat ..." read as a negation | The definition reads U+2019; `NEGATED` skips "why not". "Don't treat ..." is still a negation (S5 tests green) | ab623a2 | `test_curly_apostrophes_and_why_not_read_the_definition` |
| 5. `GET /claims/{id}/sources/{i}` opened a source with raw `text_at`, so a forged readout returned the answer key | The route uses `server.app.readable_rooms` and `memo.rooms.text_in`, the rule `POST /source` uses; `OutsideRoom` is a 404 | 718f30d | `test_claim_source_opens_nothing_outside_the_room` (relative and absolute answer key, repo file) |
| 6. An unreadable readout made every `GET /files` and `POST /source` a 500 | `readable_rooms` falls back to the room when readout.json cannot be parsed, and caches the parse by mtime and size. Shared with memo export | e44a536 | `server/tests/test_app.py::test_an_unreadable_readout_falls_back_to_the_room` (bad JSON, old schema) |
| 8. The `added` comprehension rebuilt the before-id set per claim | Built once, in `_merge_all` and the same pattern in `_merge_piece`. No behavior change | 89fbe81 | No new test: the engine suite covers the behavior |
| 9. `guard` ran twice per refused line; "rebuild" and "rebuilt" were different source words | One call; one spelling per source word | bbd0561 | `test_a_refused_rewording_is_guarded_once`, `test_rebuild_and_rebuilt_are_one_source_word` |

Item 7 (memo saves without hard links) is on the memo export page.

## Documents

- [product_thinking.md](product_thinking.md), [01_brief.md](01_brief.md)
- [02_prototype/prototype.html](02_prototype/prototype.html) and [02_prototype_decision.md](02_prototype_decision.md) (persona review inside)
- [03_prd.md](03_prd.md), [04_architecture.md](04_architecture.md), [05_plan.md](05_plan.md), [06_verification.md](06_verification.md)
- [verify_drive_page.mjs](verify_drive_page.mjs), the map at `.claude/skills/verify-tricorder/features/steering.md`, [evidence/](evidence/)
- `spike/`: `steer_spike.py`, `build_prototype.py`, `prototype_template.html`, `out/spike.json`

## Work and evidence

| Outcome | Owner | State | Evidence or blocker | Next action |
|---|---|---|---|---|
| Spike and prototype | builder | done | `spike/out/spike.json`; `02_prototype/*.png` | none |
| Persona review | coordinator | done, both agents cold: workable, workable | [02_prototype_decision.md](02_prototype_decision.md) | none |
| Fix round, items 1 to 8 | builder | done | [06_verification.md](06_verification.md), `evidence/fix_round/` | none |
| Slice 1: entry 1.3 script half | builder | done | `scans/redflags/tests/test_cohorts.py` | owner adds the model half |
| Slice 2: reading and verdicts | builder | done | `steering/tests/test_classify.py`, `test_verdicts.py` | none |
| Slice 3: engine and CLI | builder | done | `steering/tests/test_engine.py` | none |
| Slice 4: routes | builder | done | `server/tests/test_steering_routes.py` | none |
| Slice 5: page | builder | done, mounted in App.tsx | `bin/ci-web`; `evidence/fix_round/steer_*.png` | none |
| Slice 6: verification | builder | done | [06_verification.md](06_verification.md) | none |

## Decisions and events

- 2026-10-23 02:02 UTC: worktree on `forge/steering` from `forge/readout-store` (4aa2cc8).
- Wrote the 1.3 script half and a verdict stand-in, because no built check fed retention and no verdict step existed (see Attention needed 2 and 3).
- A definition steer adds a computed line rather than changing the check's line (PRD question 1, open for Ken).
- During the drive: a more-info store save copied full-room files nothing cited; fixed to keep the readout's own results (commit 5185dc7).
- Fix round (coordinator, after both persona agents rated it workable): retention rows, the rewrite redoes the piece, headline first, author and time, full-room rerun of every piece, the pilot notice clause, the first-time example, the App.tsx mount. The coordinator answered PRD question 1.
- Merged `claude/project-thread-ea11in` twice; the second brought the claims scan, and the steering tests now build readouts with every available scan.
- Review wave 2a, O8: `cohorts.py` crashed on a blank month in the customer file. It now skips and counts unreadable rows and names them in a gap (commit 2360057; tests in `scans/redflags/tests/test_cohorts.py`).
- No human approval was needed or given.

## To delete at cleanup

- `/tmp/claude-0/-home-claude/46d40c2c-7610-5980-8cc8-4007978d4e75/scratchpad/fix-round2/` and the empty `/tmp/claude-0/-home-claude/46d40c2c-7610-5980-8cc8-4007978d4e75/scratchpad/fix-round2_dbg.py` (round 2 scratch and the ci-py log)

- `/tmp/claude-0/-home-claude/46d40c2c-7610-5980-8cc8-4007978d4e75/scratchpad/fix-steering/` (wave 2b scratch: out, store, cache, logs), including the git worktree `redcheck/` on b948d09 used for the red runs (remove with `git worktree remove`)

- `/tmp/claude-0/-home-claude/46d40c2c-7610-5980-8cc8-4007978d4e75/scratchpad/steering/` (scratch out folders and the Node Playwright install)
- `/tmp/tricorder-verify/steering-trial/` (a trial run before the real one)
- `/tmp/tricorder-verify/steering/` (the run folder; its evidence is copied into `evidence/`)
- `readout/node_modules/` and `readout/dist/` in this worktree (git-ignored, built by `bin/ci-web`)
