# Feature progress: accounting mislabels

Merged to `main` in PR #4 on 2026-10-23 (merge commit `dc10bbc`). `scans/redflags/mislabels.py` was built test first, and after the review fix round its 68 tests pass. The red-flag engine carries the module's claims and its three panels. On Brasswick, `eval.score` finds BF1, BF3 and BF4 from this module, and no room flags a decoy. The proposed text is applied to entry 1.12 in [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md#112-accounting-mislabels), and the roadmap slice is marked done. Next action: none for this feature. The one open item below has an owner.

Roadmap slice: [accounting-mislabels](../../ongoing/ROADMAP.md#accounting-mislabels). Route: prototype first, with an interface example in place of a screen.

## Attention needed

1. **Entry 1.2's flag must cite `ARR_Build!E13` (redflag-engine owner, Saturday).** This module links its `mrr` column flag to the pilot-as-ARR flag by that shared source. Entry 1.2 is not built yet. Board row TRI-arr-cites-e13.

Closed on 2026-10-23:

- **The seed-drop fallback is a cell read, not a model call.** The coordinator had asked that kind a's fallback follow a "model-fallback rule". "The model" in entry 1.12 meant the company's financial model workbook. The fallback reads cells, makes no LLM call and needs no key, so its claim stays `computed` with severity `flag`. `test_makes_no_model_call` proves it. Entry 1.12 now says "the financial model workbook (`financial_model.xlsx`)" in both places, so the misreading cannot recur from the doc.
- **Entry 1.12 carries the proposed text.** The kind e plan test and vendor propagation, the kind g bridge test, Brasswick as kind c's room, and the wording above were applied from [proposed_frameworks_changes.md](proposed_frameworks_changes.md).

## Release record

- PR #4, merged to `main` on 2026-10-23, merge commit `dc10bbc` (PR head `229f8db`, GitHub CI green on it).
- Tests: `bin/ci-py` on `main`, 203 passed. This module's file holds 68 of them.
- Acceptance: Brasswick "found 4 of 5; decoys flagged 0 of 3" (BF1, BF3 and BF4 from this module, BF2 from deck-vs-books). No decoy flagged in any of the four rooms.
- Real output shown to Ken on the wave 1 demo page, built by [build_demo.py](../20261022.10_feature_breakdown/demo/build_demo.py).
- Unverified: the link to the pilot-as-ARR flag, until entry 1.2 exists (item 1).

## Review fix round (docs/features/20261022.10_feature_breakdown/review_wave1.md)

Each fix started with a failing test. Before the fixes, six new tests failed: `test_mrr_not_run_on_brasswick`, `test_one_time_fees_not_run_on_brasswick`, `test_every_not_run_kind_writes_a_gap`, `test_billings_flag_cites_the_customer_rows_it_totals`, `test_one_text_cell_is_skipped_and_counted` and `test_many_text_cells_make_the_subcheck_cannot_check`. All pass now.

| Finding | Disposition | Proof |
|---|---|---|
| S6. A not_run kind writes no gap (a, h) | Fixed. Kind a writes "Not in the room: a revenue export by product type" and kind h writes "Not in the room: one-time fees by month", each with `why` "not stated in the file". | The three S6 tests. Brasswick's result now holds 4 gaps, against 2 before. |
| S7. The kind b flag cites only `P&L!S7` | Fixed. The flag also cites the customer rows where billings and revenue differ, largest first: Ostley Freight (row 141) and Tessmore Freight (row 136). Its text names them. | `test_billings_flag_cites_the_customer_rows_it_totals` |
| S8. A text cell fails the whole sub-check | Fixed. `num()` reads a text cell as 0 and counts it. When the text cells are at or under `match_tolerance` of the cells a sub-check read, it writes a gap saying how many it skipped. Above that, the sub-check returns cannot_check. | `test_one_text_cell_is_skipped_and_counted` (kind h stays clear; the gap says "1 of N"); `test_many_text_cells_make_the_subcheck_cannot_check` (250 text fees put kind h at cannot_check, and kind a still flags) |
| U4. Clear claims cite the CSV header row | Taken, cheaply. The three clear texts now say that `scans/redflags/mislabels.py` summed the columns in the header row they cite. | the quote check still passes on every room |
| U10. The workbook test saves with openpyxl | Taken. `test_missing_pnl_row_is_a_gap` now patches the parsed P&L in memory, and it also asserts that kind e still sees real totals. | passes |
| U3. Hard-coded room shapes | Deferred. Fine for Saturday, as the review says. A third room shape would need "file not recognised" wording. | none |
| U6. Gaps in the claim id sequence | Declined. The review calls it harmless, and tests match on check names, not ids. | none |

After the fixes: `python3 -m scans.redflags data_room/brasswick` writes 11 claims and 4 gaps. `python3 -m eval.score data_room/brasswick` prints "found 4 of 5; decoys flagged 0 of 3". The `lahe.js serve` count was 0 before and 0 after.

## Decisions settled by the coordinator

- Brasswick is an acceptance room.
- No change to `generate.py`. The resale room is a pytest fixture in `tmp_path`.
- The link to the pilot flag is the shared source `ARR_Build!E13`.
- `check()` returns a third element, `list[Panel]`. Entry 1.12's tables go there: "accounting mislabels: entry", "accounting mislabels: checks" and "accounting mislabels: lines".

## Documents

- [product_thinking.md](product_thinking.md), [01_brief.md](01_brief.md), [02_interface_example.md](02_interface_example.md) (from the spike), [03_prd.md](03_prd.md), [04_architecture.md](04_architecture.md), [05_plan.md](05_plan.md) (its evidence column now holds real results), [proposed_frameworks_changes.md](proposed_frameworks_changes.md)
- Code: `scans/redflags/mislabels.py`, `scans/redflags/tests/test_mislabels.py`
- Spike (throwaway): [spike/](spike/)

## Work and evidence

| Outcome | Owner | State | Evidence or blocker | Next action |
|---|---|---|---|---|
| Docs to Plan | agent | done | this folder, committed by the parent | none |
| Tests written first | agent | done | Run before the module existed, the file failed at collection with `ImportError: cannot import name 'mislabels'`. The red check covered the whole file, not each test. | none |
| Module | agent | merged in PR #4 | `python3 -m pytest scans/redflags/tests/test_mislabels.py`: 68 passed after the fix round (64 before) | none |
| Full suite | agent | green | `python3 -m pytest`: 203 passed in 17.86s after the fix round (183 before). An earlier run set aside `scans/memo/tests/test_coverage.py` (147 passed without it), while another agent's checklist module was still missing. | none |
| Engine on Hollis Voice | agent | done | `python3 -m scans.redflags data_room/hollis_voice`: "redflags: 10 claims, 4 gaps". redflags-001 is the `mrr_column_vs_subscription_rows` flag ($186,739 against $171,739, $15,000, 8.7%). Claims 002 to 006 are info tie-outs for b, e, f, g and h. Claims 007 to 010 come from deck_vs_books. | none |
| Score | agent | done | `python3 -m scans.redflags`, `python3 -m scans.memo`, `python3 -m eval.score` per room. brasswick: found 4 of 5 (BF1, BF3, BF4 from this module; BF2 from deck_vs_books), decoys flagged 0 of 3. hollis_voice: found 0 of 8, decoys 0 of 3. hollis_voice_seed_drop: found 0 of 8, decoys 0 of 3. hollis_voice_clean: found 0 of 0, decoys 0 of 3. Hollis Voice's planted flags belong to the Saturday checks, which do not exist yet. | none |
| Helper processes | agent | checked | `ps -axo command \| grep -c "[l]ahe.js serve"`: 0 before and 0 after. The tests start no process. | none |

## Decisions and events

- 2026-10-22T19:58Z: started the docs and the spike.
- 2026-10-22T20:07Z: docs written; the parent committed them.
- Coordinator decisions received (listed above). Wrote `test_mislabels.py` from the Plan's verification table, then the module.
- The first full run failed one test. The watch fixture edited the Brasswick workbook with openpyxl, which drops cached formula values, so the totals read as empty. The fix patches the parsed P&L in memory.
- Added panel tests after the framework update: `test_panels_carry_entry_checks_and_lines`, `test_seed_drop_entry_label`, `test_engine_result_holds_mislabels_claims_and_panels`.
- 2026-10-22T20:14Z: all green as above. No human approval is needed for this route; none was given.
- 2026-10-23: merged in PR #4. Closeout applied the proposed text to entry 1.12.

## Not for commit

- `spike/test_rooms/` (about 960K): generated copies of the Hollis Voice room.
- `out/`: engine, memo and score results. Git already ignores it.

## To delete at cleanup

- `docs/features/20261022.12_accounting_mislabels/spike/test_rooms/`: generated copies of the Hollis Voice room (about 960K, untracked), rewritten by each spike run.
- The worktree `/tmp/claude-0/-home-claude/76c6a462-572c-5250-967a-649aceb49eaf/scratchpad/wt2` and its local branch `tmp-ce34ga`, used to merge the skeleton branch. Its work is on `main` through PR #2 and PR #4. Remove with `git worktree remove --force` and `git branch -D tmp-ce34ga`. The same line is on the other wave 1 pages.
- The scratch copy of the skeleton's `schema/`, `scans/base.py` and `eval/score.py` in this session's scratchpad folder. It is outside the repo.
- `out/hollis_voice/`, `out/hollis_voice_seed_drop/`, `out/hollis_voice_clean/`, `out/brasswick/`: result files from the acceptance commands. Git ignores them.
