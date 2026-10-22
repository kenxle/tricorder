# Feature progress: deck-vs-books

The check is built and green, waiting for the parent to commit it and open a PR. `scans/redflags/deck_vs_books.py` runs inside the red-flag engine. On Hollis Voice it flags the deck's ARR, $2,500,000 against the P&L's $2,240,868 (11.6%), and matches the slide 3 chart and the plan growth. On Brasswick it catches BF2: `python3 -m eval.score data_room/brasswick` prints "found BF2" with 0 of 3 decoys flagged. Its 43 tests pass, and the whole suite passes: 184 tests, working tree at 2026-10-22T20:18Z. Next: the parent commits, then the captain merges.

Every number on this page comes from [evidence/](evidence/) (the built module) or [spike/out/](spike/out/) (the spike).

## Attention needed

1. **FRAMEWORKS.md has no entry for this check (FRAMEWORKS owner).** A paste-ready entry 1.14, with two rows for the "Where each planted flag is caught" table, is in [proposed_frameworks_entry.md](proposed_frameworks_entry.md).
2. **The roadmap's Done when (Ken or the roadmap writer).** Add "on Brasswick, `eval.score` counts BF2 as found". Also, the test deck is now a `watch`, by Ken's decision, so the roadmap's "is flagged with the months it leaves out" should read "is reported with the months it leaves out".
3. **The ARR overlap with PF2 (readout owner).** PRD Q1. On Hollis Voice this check and `deck_claim_vs_named_cell` both flag the deck's $2,500,000, against P&L!W10 here and against `ARR_TOTAL` there. The scorer credits PF2 only to the engine's check. The readout should group flag claims that share a label, unit and period, so the top flags list does not show the same problem twice.
4. **A wording slip in `data_room/README.md` (data-room owner).** Its BF2 row says the 2025-09 peak of $84,090 is "28% above January 2026". The peak is 39.2% above January ($60,400), and January is 28.2% below the peak ([spike/out/brasswick.json](spike/out/brasswick.json), `peak_above_chart_first_pct` and `fall_from_peak_pct`). The key's `fall_from_peak` is 0.282, so the key is right.

## Documents

- [product_thinking.md](product_thinking.md) and [01_brief.md](01_brief.md): the job and the short brief.
- [02_interface_example.md](02_interface_example.md): the prototype, real Claim JSON from the spike.
- [03_prd.md](03_prd.md): requirements DVB-R1 to DVB-R13.
- [04_architecture.md](04_architecture.md): the module, the data shapes, the alternatives, the points settled.
- [05_plan.md](05_plan.md): the slices and the [verification table](05_plan.md#verification), with evidence in every row.
- [proposed_frameworks_entry.md](proposed_frameworks_entry.md): the entry for FRAMEWORKS.md.
- [evidence/](evidence/): `pytest.txt`, `pipeline.txt` (the engine, the memo and the scorer on both rooms) and `test_rooms.txt` (the check on each test room).

## Work and evidence

| Outcome | Owner | State | Evidence or blocker | Next action |
|---|---|---|---|---|
| Docs through the Plan, and the spike | agent | done, committed by the parent | [02_interface_example.md](02_interface_example.md) | none |
| Tests written first | agent | done | Run red (the module did not exist), then green | none |
| `scans/redflags/deck_vs_books.py` | agent | done, not committed | 43 passed ([pytest.txt](evidence/pytest.txt)) | The parent commits |
| `chart_shape_tolerance` in `schema/settings.py` | agent, agreed by the schema owner | done, not committed | `test_chart_shape_tolerance_is_a_setting` | The parent commits |
| BF2 found through the real pipeline | agent | done | "found BF2", decoys flagged 0 of 3 ([pipeline.txt](evidence/pipeline.txt)) | none |
| Proposed FRAMEWORKS entry | agent | done | [proposed_frameworks_entry.md](proposed_frameworks_entry.md) | The FRAMEWORKS owner pastes it |

## Files written in the build

- `scans/redflags/deck_vs_books.py`: the check. `check(room, ids)` returns claims, gaps and one Panel, "deck against the books".
- `scans/redflags/tests/test_deck_vs_books.py`: 43 tests, one or more per row of the Plan's table.
- `scans/redflags/tests/deck_vs_books_fixtures.py`: builds test rooms in `tmp_path`. Tests that draw a test deck skip when matplotlib, reportlab or pypdf is missing. Nothing was added to `requirements.txt`.
- `schema/settings.py`: one line, `chart_shape_tolerance: 0.02`, with a comment naming its source.
- Untouched: `scans/redflags/scan.py`, `scans/redflags/mislabels.py` and its tests, `docs/ongoing/`, `data_room/`.

## Decisions and events

- 2026-10-22T20:02Z: spike runs recorded in `spike/out/`.
- 2026-10-22: Ken decided, through the coordinator, that hidden months holding only a climb make a `watch`. A dip or a flat stretch keeps a `flag`. The PRD's DVB-R7 and Q2 were updated.
- 2026-10-22: the schema owner agreed to `chart_shape_tolerance` in `schema/settings.py`. The framework now merges a third `check()` element into `ScanResult.panels`, so the match table ships as a Panel.
- 2026-10-22: tests written first and run red. The module made them green.
- 2026-10-22: a defect found while recording evidence. On a test deck whose chart starts before the books, the bar for $900 (under 1 percent of the tallest bar) was missed, which gave a false "1 months are skipped" flag. A red assertion was added, then the bar reader was fixed to scan the bottom-most bar row. The spike script still has the old reader; it is a record, not production code.
- 2026-10-22T20:18Z: whole suite 184 passed. `eval.score` runs in [pipeline.txt](evidence/pipeline.txt) used `TRICORDER_OUT_DIR` pointed at a scratch folder, so nothing was written to `out/` in the repo.
- No human approval was needed or given for these documents. The route does not require one.

## To delete at cleanup

- Nothing in the repo.
- Outside the repo: a skeleton copy and scan outputs in this session's scratchpad (`/tmp/claude-0/.../scratchpad/skel` and `.../scratchpad/out`). The operating system owns `/tmp`.
- Environment: `matplotlib==3.11.2` was installed into the system Python with pip, for the test decks. It matches `data_room/requirements.txt`.
