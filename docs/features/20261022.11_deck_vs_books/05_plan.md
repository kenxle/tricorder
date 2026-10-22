# Plan: deck-vs-books

Requirements: [03_prd.md](03_prd.md). Design: [04_architecture.md](04_architecture.md). Progress: [00_progress.md](00_progress.md).

## Implementation strategy

### Throughput checkpoint

- **Blocking prerequisites.** The skeleton (`schema/claim.py`, `schema/readers.py`, `schema/settings.py`, `scans/base.py`, `scans/redflags/scan.py`, `eval/score.py`) must be on `main`. It is on `origin/claude/project-thread-ce34ga` at `573567f` and was landing when this was written. Nothing else blocks: the data rooms are generated and committed.
- **Independent workstreams.** None worth splitting. The module is one file. The spike that it follows is one script of 576 lines (`wc -l spike/deck_vs_books_spike.py`), including its printing and argument handling. The three slices share `Books` and `DeckFigure`.
- **Shared writable state.** `schema/settings.py` got one new key, `chart_shape_tolerance` (default 0.02), with the schema owner's agreement on 2026-10-22. Nothing else outside `scans/redflags/deck_vs_books.py` and `scans/redflags/tests/` was written.
- **Smallest safe decomposition.** One owner, one branch (`feat/deck-vs-books`), three commits in the order below, one pull request. Each commit leaves the engine running, because `scan.py` skips the module until it exists and the module returns empty lists for anything it cannot read.

### Slices

| # | Outcome | Scope | Depends on | Landing |
|---|---|---|---|---|
| 1 | Text figures matched to the P&L, with gaps | `load_books`, `deck_figures` (text only), `match_figure`, `check`; DVB-R1 to R5, R10 to R13 | the skeleton on `main` | Commit 1. On Hollis Voice the engine gains the ARR claim and the plan-growth claim. |
| 2 | Charts and partial history | `read_bars` with the pdfplumber crop render, the shape match, `history`; the test-deck fixtures; DVB-R6 to R8 | slice 1 | Commit 2. Brasswick's BF2 is found. |
| 3 | Revenue rows when the P&L is missing | the DVB-R9 fallback for the window check | slice 2 | Commit 3, then the PR. |

### Workstream contract (the one builder)

- **Outcome:** `scans/redflags/deck_vs_books.py` and `scans/redflags/tests/test_deck_vs_books.py`, passing every row below.
- **Read first:** this Plan, the PRD's requirements, the architecture's "The skeleton it plugs into", [02_interface_example.md](02_interface_example.md), and the spike ([spike/deck_vs_books_spike.py](spike/deck_vs_books_spike.py)), which is a working reference, not code to copy as is: it reads with pypdf and openpyxl directly, and production reads through `schema/readers.py`.
- **Owned files:** `scans/redflags/deck_vs_books.py`, `scans/redflags/tests/test_deck_vs_books.py`, `scans/redflags/tests/deck_vs_books_fixtures.py`.
- **Authority:** no edit to `scan.py`, `schema/`, `data_room/` or `docs/ongoing/`. Ask the skeleton owner before adding the setting.
- **Uncertainty rule:** if a requirement and a room disagree, stop and write it under "Attention needed" in Progress, rather than working around it.
- **Quality checks:** `pytest scans/redflags/tests/test_deck_vs_books.py`, then `pytest`, then the commands in the table.
- **Completion evidence:** the table's Evidence column filled with real output.

### Test fixtures

- **The rooms.** Tests read `data_room/hollis_voice`, `hollis_voice_seed_drop`, `hollis_voice_clean` and `brasswick` in place. They never write there.
- **Missing files.** A test that needs a missing P&L or deck copies the other room files it needs into pytest's `tmp_path` and runs the check on the copy.
- **Test decks.** As built: `deck_vs_books_fixtures.make_room()` copies the Hollis Voice files the check reads into pytest's `tmp_path` and writes the test deck there, drawn from the room's own P&L. Drawing needs matplotlib, reportlab and pypdf, which are in `data_room/requirements.txt` but not in the root `requirements.txt`, so those tests skip cleanly when one is missing. Nothing was added to `requirements.txt`. The earlier idea of committed fixture PDFs was dropped.

## Verification

Built test-first on 2026-10-22: the test file was written and run red (the module did not exist), then the module made it green. The one defect found after that (a bar under 1 percent of the tallest was missed) got a red assertion first, then the fix. Test names are in `scans/redflags/tests/test_deck_vs_books.py`. Test rooms are built in pytest's `tmp_path` by `scans/redflags/tests/deck_vs_books_fixtures.py`; tests that need a test deck skip when matplotlib, reportlab or pypdf is missing.

Evidence files: [evidence/pytest.txt](evidence/pytest.txt), [evidence/pipeline.txt](evidence/pipeline.txt), [evidence/test_rooms.txt](evidence/test_rooms.txt).

| Requirement | Acceptance/failure case | Command/observation | Owner | Evidence/status |
|---|---|---|---|---|
| DVB-R1 | Hollis Voice: figures on slides 3, 11 and 14, none unmatched. Brasswick: LTM revenue, September MRR, the slide 4 chart, "grew every month" | `test_finds_every_revenue_figure_hollis`, `test_finds_every_revenue_figure_brasswick` | agent | Pass. Claims in [pipeline.txt](evidence/pipeline.txt). |
| DVB-R1 | No claims page: figures come from `claims.json` (`claims[0]`) | `test_claims_json_fallback` | agent | Pass. "no_claims_page" in [test_rooms.txt](evidence/test_rooms.txt). |
| DVB-R2, R3, R4 | Hollis Voice ARR $2,500,000 against $2,240,868 (12 x `P&L!W10`), 11.6%, `flag`, sources slide 3 "$2.5M", slide 14, `P&L!W10` | `test_hollis_arr_flags_against_pnl` | agent | Pass. `redflags-007` in [pipeline.txt](evidence/pipeline.txt). |
| DVB-R2, R3, R4 | Brasswick LTM $943,340 (12 P&L cells) and MRR $84,810 match, `info` | `test_brasswick_stated_figures_match` | agent | Pass. Gaps of 0.0%. |
| DVB-R3 | Half-step and tolerance rule, four cases | `test_rounded_figure_within_half_step_matches` | agent | Pass. |
| DVB-R3 | Clean room: ARR $2,060,868 matches, no `flag` | `test_clean_room_has_no_flags` | agent | Pass. |
| DVB-R5 | P&L and revenue rows missing: 3 unmatched `info` claims, "no P&L to match against" | `test_missing_pnl_lists_figures_unmatched` | agent | Pass. Last case in [test_rooms.txt](evidence/test_rooms.txt). |
| DVB-R6 | Hollis Voice chart: 21 bars match the recurring line | `test_chart_bars_match_books_hollis` | agent | Pass. |
| DVB-R6 | Quarterly test deck: 7 bars against the books by quarter | `test_quarterly_chart_compared_by_quarter` | agent | Pass, 0.4 points. |
| DVB-R6 | `chart_shape_tolerance` is read from `schema.settings.load()`; a tiny override turns the chart claim into a flag | `test_chart_shape_tolerance_is_a_setting` | agent | Pass. Default 0.02 added to `schema/settings.py` with the schema owner's agreement. |
| DVB-R7 | Test deck from 2025-07: "Shows part of the history", 2025-01 to 2025-06, the climb from $2,651 to $19,462, severity `watch` (default chosen by the orchestrator, open for Ken: nothing bad hidden) | `test_chart_starting_six_months_late_is_flagged` | agent | Pass. "starts_late" in [test_rooms.txt](evidence/test_rooms.txt). The roadmap's Done when. |
| DVB-R7 | Brasswick: `flag` naming 2025-05 to 2025-12, the 2025-09 peak of $84,090, the 28.2% fall to $60,400 | `test_brasswick_partial_history_names_hidden_peak` | agent | Pass. `redflags-010` in [pipeline.txt](evidence/pipeline.txt). |
| DVB-R7 | Brasswick BF2 found by the scorer, no decoy flagged | `test_brasswick_bf2_counts_as_found_and_no_decoy_flagged`; `python3 -m scans.redflags data_room/brasswick`, `python3 -m scans.memo data_room/brasswick`, `python3 -m eval.score data_room/brasswick` | agent | Pass. "found BF2", "decoys flagged 0 of 3" (BF1, BF3, BF4 come from the mislabels check). |
| DVB-R7 | No Hollis Voice or clean-room decoy flagged by this check | `test_hollis_answer_key_decoys_stay_clear` | agent | Pass. `eval.score data_room/hollis_voice`: decoys flagged 0 of 3. |
| DVB-R7 | Real Hollis Voice deck: window `info` | `test_full_history_chart_is_info` | agent | Pass. `redflags-009`. |
| DVB-R7 | Quarterly test deck: partial history `watch`, "no month inside a quarter fell" | `test_quarterly_chart_flags_partial_history` | agent | Pass. |
| DVB-R7 | Severity of hidden months: climb is `watch`; dip, peak or flat stretch is `flag` | `test_hidden_months_severity` (4 cases) | agent | Pass. |
| DVB-R8 | Unreadable chart: gap "a readable chart on slide 3", window still checked, no bar claim | `test_unreadable_chart_is_a_gap` | agent | Pass. |
| DVB-R9 | No claim cites the revenue rows when the P&L is present (Brasswick, clean room) | `test_revenue_row_differences_write_no_claim` | agent | Pass. |
| DVB-R9 | P&L missing, revenue rows present: the window check runs from `customer_mrr_by_month.csv` and cites it | `test_window_from_revenue_rows_when_pnl_missing` | agent | Pass. "starts_late, P&L missing" in [test_rooms.txt](evidence/test_rooms.txt). |
| DVB-R10 | No deck: one gap, no claims. No P&L: gap with `piece` "traction_and_revenue" | `test_missing_deck_is_one_gap`, `test_missing_pnl_gap_has_piece` | agent | Pass. |
| DVB-R10 | Chart reaching 2024-10 to 2024-12, before the books: ask-list gap, and no false "skipped" claim | `test_chart_months_missing_from_books_is_a_gap` | agent | Pass after the tiny-bar fix. "before_books" in [test_rooms.txt](evidence/test_rooms.txt). |
| DVB-R11 | Labels: ARR `arr` / `USD_per_year`; partial history `other` / `months` | `test_value_labels_route_pieces` | agent | Pass. |
| DVB-R12 | Every claim passes the quote checker on four rooms and four test rooms; no absolute uris | `test_every_claim_passes_quote_checker` (4 rooms), `test_every_claim_passes_quote_checker_on_test_rooms` (4 decks) | agent | Pass. The memo's re-check left 0 of this check's claims unverified on Hollis Voice and Brasswick ([pipeline.txt](evidence/pipeline.txt)). |
| DVB-R13 | No network, no model: a socket connect raises, and the check still runs | `test_runs_offline` | agent | Pass. |
| DVB-R13 | No pypdf and no anthropic import in the module | `test_bars_read_without_pypdf` | agent | Pass. Nothing added to `requirements.txt`. |
| Contract | `check(room, ids)` returns claims, gaps and one Panel; ids come from `Ids` | `test_claim_ids_come_from_ids`, `test_match_table_panel` | agent | Pass. "deck against the books" is in both readouts' panels. |
| All | Full suite green | `python3 -m pytest` | agent, then the captain at merge | 184 passed ([pytest.txt](evidence/pytest.txt)), working tree at 2026-10-22T20:18Z, including the parallel mislabels and coverage work. |
| Roadmap Done when | Every Hollis Voice deck revenue figure matched or listed; the late test deck reported with its months; quote checker passes | the rows above for R1, R4, R7, R12 | agent | Pass. The late deck is a `watch`, not a `flag`, by Ken's decision; the roadmap's word "flagged" should read "reported". |

## Testing review

Selected findings from reading the spike's runs, with what the Plan does about each:

| Finding | Disposition |
|---|---|
| The pixel reader is tuned to the generator's charts. A real deck can break it. | Accepted for Saturday. The rooms are generated. DVB-R8 makes failure a gap, not a wrong flag, when no bars are found. A real deck with a stacked chart could still give a false shape flag: noted in the architecture's failure modes. |
| The spike lists unmatched figures outside the claims. `ScanResult` has no such list. | Changed: unmatched figures become `info` claims (DVB-R5). |
| The clean room's `mrr` column carries the pilot while its P&L recurring line does not. | Revenue rows are a cross-check only (DVB-R9). |

## Rollout and release

No flag. The pull request merges to `main` when `pytest` passes and the table's commands read as expected. The captain merges, by [guardrails.md](../../../.claude/guardrails.md). No human document approval is needed for this route.
