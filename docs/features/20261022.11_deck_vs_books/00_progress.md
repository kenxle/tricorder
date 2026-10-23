# Feature progress: deck-vs-books

Merged to `main` in PR #4 on 2026-10-23 (merge commit `dc10bbc`). `scans/redflags/deck_vs_books.py` runs inside the red-flag engine. On Hollis Voice it flags the deck's ARR, $2,500,000 against the P&L's $2,240,868 (11.6%), and matches the slide 3 chart and the plan growth. On Brasswick it catches BF2: `python3 -m eval.score data_room/brasswick` prints "found BF2" with 0 of 3 decoys flagged. Review round 1 is done: findings S1 to S5 are fixed, each with a failing test first through the real `check()`. The check is written up as entry 1.14 in [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md#114-deck-revenue-against-the-books), and the roadmap slice is marked done. Next action: none for this feature. The open items below each have an owner.

Every number on this page comes from [evidence/](evidence/) (the built module) or [spike/out/](spike/out/) (the spike).

## Attention needed

1. **Partial history: flag or watch (Ken).** Two defaults were chosen by the orchestrator and are open for Ken. Hidden months that hold only a climb make a `watch`; a dip or a flat stretch makes a `flag`. Months after a chart's last month (review S3) follow the same rule as months before its first. Say if either should change; each is one condition in `scans/redflags/deck_vs_books.py`.
2. **Brasswick "grew every month in 2026" (Ken).** Review U2. Revenue fell $2,705 from 2025-12 to 2026-01, and the claim is `info` because only months inside 2026 are compared. Compare January with December, or keep `info`. BF2's partial-history flag already shows the fall.
3. **The ARR overlap with PF2 (readout owner).** PRD Q1. On Hollis Voice this check and `deck_claim_vs_named_cell` both flag the deck's $2,500,000, against P&L!W10 here and against `ARR_TOTAL` there. The readout should group flag claims that share a label, unit and period, so the top flags list does not show the same problem twice. Board row TRI-readout-group-flags.
4. **A wording slip in `data_room/README.md` (data-room owner).** Its BF2 row says the 2025-09 peak of $84,090 is "28% above January 2026". The peak is 39.2% above January ($60,400), and January is 28.2% below the peak ([spike/out/brasswick.json](spike/out/brasswick.json), `peak_above_chart_first_pct` and `fall_from_peak_pct`). The key's `fall_from_peak` is 0.282, so the key is right. Board row TRI-brasswick-readme.

Closed on 2026-10-23: the FRAMEWORKS entry was applied (entry 1.14 and its two rows), and the roadmap's Done when now names BF2 and says the late test deck is "reported".

## Release record

- PR #4, merged to `main` on 2026-10-23, merge commit `dc10bbc` (PR head `229f8db`, GitHub CI green on it).
- Tests: `bin/ci-py` on `main`, 203 passed. This module's file holds 53 of them.
- Acceptance: "found BF2", decoys flagged 0 of 3 ([evidence/pipeline.txt](evidence/pipeline.txt)).
- Real output shown to Ken on the wave 1 demo page, built by [build_demo.py](../20261022.10_feature_breakdown/demo/build_demo.py).
- Unverified: nothing for this module. The readout grouping in item 3 is not built.

## Review round 1

Review: [review_wave1.md](../20261022.10_feature_breakdown/review_wave1.md), read, not edited. Each fix got a failing test first, run through the real `check()` (test rooms built in `tmp_path`, or `load_pnl` patched to drop a cell). Outputs of every case: [evidence/review_round1.txt](evidence/review_round1.txt).

| Finding | Disposition | Test, red then green |
|---|---|---|
| S1. The half-step rule never ran in production | Fixed. `deck_figures` keeps the half step for a short-form figure when no exact form appears anywhere in the deck. A "$2.2M" ARR against $2,240,868 now matches, and the claim says "within the rounding of the printed $2.2M". The real deck's exact $2,500,000 is unchanged. | `test_s1_short_form_figure_uses_half_step_through_check`, `test_s1_exact_form_keeps_one_percent_rule` |
| S2. A plan-growth mismatch was `info` | Fixed. 8.0% against plan columns of 3.50% is a `flag`. | `test_s2_plan_growth_mismatch_is_a_flag` |
| S3. A chart that ends early read "no month left out" | Fixed, the wider way: months after the chart's last month are partial history too. A Brasswick chart from 2025-05 to 2025-09 is a `flag` naming 2025-10 to 2026-09 and the fall to $60,400, 28.2% below the chart's last month. The "no month left out" text now appears only when both ends were checked. This widens DVB-R7; the PRD says so. The orchestrator chose this as the default, open for Ken: trailing months could read as a `watch` instead. | `test_s3_chart_ending_early_is_partial_history`, `test_s3_whole_window_still_info` |
| S4. A blank revenue cell crashed the engine | Fixed. Each figure runs inside a guard. A missing cell is one gap naming the month, and the other figures still run. A books value of 0 is unmatched. Identical gaps from several figures are written once (also review U5's point, for this module). | `test_s4_blank_revenue_cell_is_a_gap_not_a_crash` (also runs `scans.redflags.scan.run`), `test_s4_zero_books_value_is_unmatched_not_a_crash` |
| S5. "Grew every month" cited the wrong cells | Fixed. A flag cites each month that fell and the month before it: on Brasswick's 2025 test, 2025-09 to 2025-12. | `test_s5_grew_flag_cites_the_months_that_fell` |
| U1. Misleading reason with no as-of month | Taken. The reason now reads "the deck states no 'Data as of' month, so the period is unknown". | `test_u1_no_as_of_month_gives_the_real_reason` |
| U2. Brasswick "grew every month in 2026" is `info` though January fell $2,705 from December | Not changed. A product call for Ken: compare January with December, or keep `info`. BF2's partial-history flag already shows the fall. | none |
| U3. Hard-coded room shapes | Not changed for this module. `ROW_COLUMNS` is used only when the P&L is missing. An unknown customer file then gives the P&L gap and no window, which is true. | none |
| U7. The history value added skipped bars | Taken. The value counts months left out only (8, not 9, on a chart missing one bar). | `test_u7_history_value_counts_months_left_out_only` |
| S6 to S12, U4 to U6, U8 to U10 | Aimed at the mislabels and coverage modules. Not this feature's files. | none |

## Documents

- [product_thinking.md](product_thinking.md) and [01_brief.md](01_brief.md): the job and the short brief.
- [02_interface_example.md](02_interface_example.md): the prototype, real Claim JSON from the spike.
- [03_prd.md](03_prd.md): requirements DVB-R1 to DVB-R13.
- [04_architecture.md](04_architecture.md): the module, the data shapes, the alternatives, the points settled.
- [05_plan.md](05_plan.md): the slices and the [verification table](05_plan.md#verification), with evidence in every row.
- [proposed_frameworks_entry.md](proposed_frameworks_entry.md): the entry for FRAMEWORKS.md.
- [evidence/](evidence/): `pytest.txt`, `pipeline.txt` (the engine, the memo and the scorer on both rooms), `test_rooms.txt` (the check on each test room, before review round 1) and `review_round1.txt` (each review case after the fixes).

## Work and evidence

| Outcome | Owner | State | Evidence or blocker | Next action |
|---|---|---|---|---|
| Docs through the Plan, and the spike | agent | done, committed by the parent | [02_interface_example.md](02_interface_example.md) | none |
| Tests written first | agent | done | Run red (the module did not exist), then green | none |
| `scans/redflags/deck_vs_books.py` | agent | merged in PR #4 | 53 passed ([pytest.txt](evidence/pytest.txt)) | none |
| `chart_shape_tolerance` in `schema/settings.py` | agent, agreed by the schema owner | merged in PR #4 | `test_chart_shape_tolerance_is_a_setting` | none |
| BF2 found through the real pipeline | agent | done | "found BF2", decoys flagged 0 of 3 ([pipeline.txt](evidence/pipeline.txt)) | none |
| FRAMEWORKS entry 1.14 | agent, applied at closeout | applied 2026-10-23 | [proposed_frameworks_entry.md](proposed_frameworks_entry.md) | none |

## Files written in the build

- `scans/redflags/deck_vs_books.py`: the check. `check(room, ids)` returns claims, gaps and one Panel, "deck against the books".
- `scans/redflags/tests/test_deck_vs_books.py`: 53 tests, one or more per row of the Plan's table, including the review round 1 cases.
- `scans/redflags/tests/deck_vs_books_fixtures.py`: builds test rooms in `tmp_path`. Tests that draw a test deck skip when matplotlib, reportlab or pypdf is missing. Nothing was added to `requirements.txt`.
- `schema/settings.py`: one line, `chart_shape_tolerance: 0.02`, with a comment naming its source.
- Untouched: `scans/redflags/scan.py`, `scans/redflags/mislabels.py` and its tests, `docs/ongoing/`, `data_room/`.

## Decisions and events

- 2026-10-22T20:02Z: spike runs recorded in `spike/out/`.
- 2026-10-22: the orchestrator chose a default, open for Ken to change: hidden months holding only a climb make a `watch`. A dip or a flat stretch keeps a `flag`. The PRD's DVB-R7 and Q2 were updated.
- 2026-10-22: the schema owner agreed to `chart_shape_tolerance` in `schema/settings.py`. The framework now merges a third `check()` element into `ScanResult.panels`, so the match table ships as a Panel.
- 2026-10-22: tests written first and run red. The module made them green.
- 2026-10-22: a defect found while recording evidence. On a test deck whose chart starts before the books, the bar for $900 (under 1 percent of the tallest bar) was missed, which gave a false "1 months are skipped" flag. A red assertion was added, then the bar reader was fixed to scan the bottom-most bar row. The spike script still has the old reader; it is a record, not production code.
- 2026-10-22T20:18Z: whole suite 184 passed. `eval.score` runs in [pipeline.txt](evidence/pipeline.txt) used `TRICORDER_OUT_DIR` pointed at a scratch folder, so nothing was written to `out/` in the repo.
- 2026-10-22T20:38Z: review round 1 fixed (S1 to S5, U1, U7, and duplicate gaps). Whole suite 203 passed. Pipeline rerun: Brasswick still "found BF2", decoys flagged 0 of 3 on both rooms.
- No human approval was needed or given for these documents. The route does not require one.
- 2026-10-22: CI on the PR went red. Six fix-round tests built slides without the skip guard, and CI has no pypdf. The guard moved into the shared slide-size helper (commit `e0551fb`).
- 2026-10-23: merged in PR #4. Closeout applied entry 1.14 to FRAMEWORKS.md and marked the roadmap slice done.

## To delete at cleanup

- Nothing in the repo from this feature.
- `docs/features/20261022.12_accounting_mislabels/spike/test_rooms/`: generated test rooms from the wave (untracked). The same line is on the other wave 1 pages.
- The worktree `/tmp/claude-0/-home-claude/76c6a462-572c-5250-967a-649aceb49eaf/scratchpad/wt2` and its local branch `tmp-ce34ga`, used to merge the skeleton branch. Its work is on `main` through PR #2 and PR #4. Remove with `git worktree remove --force` and `git branch -D tmp-ce34ga`.
- Outside the repo: a skeleton copy and scan outputs in this session's scratchpad (`/tmp/claude-0/.../scratchpad/skel` and `.../scratchpad/out`). The operating system owns `/tmp`.
- Environment: `matplotlib==3.11.2` was installed into the system Python with pip, for the test decks. It matches `data_room/requirements.txt`.
