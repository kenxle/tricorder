# Plan: deck-vs-books

Requirements: [03_prd.md](03_prd.md). Design: [04_architecture.md](04_architecture.md). Progress: [00_progress.md](00_progress.md).

## Implementation strategy

### Throughput checkpoint

- **Blocking prerequisites.** The skeleton (`schema/claim.py`, `schema/readers.py`, `schema/settings.py`, `scans/base.py`, `scans/redflags/scan.py`, `eval/score.py`) must be on `main`. It is on `origin/claude/project-thread-ce34ga` at `573567f` and was landing when this was written. Nothing else blocks: the data rooms are generated and committed.
- **Independent workstreams.** None worth splitting. The module is one file. The spike that it follows is one script of 576 lines (`wc -l spike/deck_vs_books_spike.py`), including its printing and argument handling. The three slices share `Books` and `DeckFigure`.
- **Shared writable state.** `schema/settings.py` gets one new key (`chart_shape_tolerance`). That file belongs to the skeleton owner, so the builder asks before adding it. Nothing else outside `scans/redflags/deck_vs_books.py` and `scans/redflags/tests/` is written.
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
- **Owned files:** the module, its test file, `scans/redflags/tests/fixtures/deck_vs_books/` (the three test decks as committed PDFs and the script that made them).
- **Authority:** no edit to `scan.py`, `schema/`, `data_room/` or `docs/ongoing/`. Ask the skeleton owner before adding the setting.
- **Uncertainty rule:** if a requirement and a room disagree, stop and write it under "Attention needed" in Progress, rather than working around it.
- **Quality checks:** `pytest scans/redflags/tests/test_deck_vs_books.py`, then `pytest`, then the commands in the table.
- **Completion evidence:** the table's Evidence column filled with real output.

### Test fixtures

- **The rooms.** Tests read `data_room/hollis_voice`, `hollis_voice_seed_drop`, `hollis_voice_clean` and `brasswick` in place. They never write there.
- **Missing files.** A test that needs a missing P&L or deck copies the other room files it needs into pytest's `tmp_path` and runs the check on the copy.
- **Test decks.** `make_test_decks.py` from the spike needs matplotlib, reportlab and pypdf, which are in `data_room/requirements.txt` but not in the root `requirements.txt`. So the three decks are made once with the data-room venv and committed as fixture PDFs, with the script beside them. A test copies the Hollis Voice room files it needs into `tmp_path` and puts the fixture deck at `01_overview/pitch_deck.pdf`, so every source uri stays relative.

## Verification

Tests are written first, red, then green. "Owner" is the builder unless named. Test names are in `scans/redflags/tests/test_deck_vs_books.py`.

| Requirement | Acceptance/failure case | Command/observation | Owner | Evidence/status |
|---|---|---|---|---|
| DVB-R1 | Hollis Voice: three revenue figures found (ARR on slides 3 and 14, the slide 3 chart, the slide 11 plan growth). Brasswick: four (LTM revenue, September MRR, the slide 4 chart, "grew every month") | `test_finds_every_revenue_figure_hollis`, `test_finds_every_revenue_figure_brasswick` | builder | Spike: [hollis_voice.txt](spike/out/hollis_voice.txt), [brasswick.txt](spike/out/brasswick.txt). Test not written. |
| DVB-R1 | No claims page: figures come from `claims.json` | `test_claims_json_fallback` | builder | Not spiked. |
| DVB-R2, R3, R4 | Hollis Voice ARR: $2,500,000 against $2,240,868 (12 x `P&L!W10`), 11.6%, severity `flag`, check `deck_revenue_vs_pnl`, sources slide 3 "$2.5M", slide 14 row, `P&L!W10` | `test_hollis_arr_flags_against_pnl` | builder | Spike claim in [02_interface_example.md](02_interface_example.md), section 1. |
| DVB-R2, R3, R4 | Brasswick LTM revenue $943,340 and September MRR $84,810 match the P&L within tolerance, severity `info` | `test_brasswick_stated_figures_match` | builder | Spike: gaps of 0.0% in [brasswick.txt](spike/out/brasswick.txt). |
| DVB-R3 | A short-form figure inside half a printed step is not a mismatch | `test_rounded_figure_within_half_step_matches` | builder | Not spiked as a separate case. |
| DVB-R3 | Clean room: deck ARR $2,060,868 matches, no `flag` claim from this check | `test_clean_room_has_no_flags` | builder | Spike: label `clear`, [hollis_voice_clean.txt](spike/out/hollis_voice_clean.txt). |
| DVB-R5 | P&L missing: every figure is an unmatched `info` claim with reason "no P&L to match against" | `test_missing_pnl_lists_figures_unmatched` | builder | Spike lists them, but as a separate list, not as claims: [hollis_voice_no_pnl.txt](spike/out/hollis_voice_no_pnl.txt). Production change. |
| DVB-R6 | Hollis Voice chart: 21 bars, shape within `chart_shape_tolerance` of the recurring line, `info` | `test_chart_bars_match_books_hollis` | builder | Spike: 21 bars, 0.4 points. |
| DVB-R6 | Quarterly test deck: 7 bars compared with the books summed by quarter | `test_quarterly_chart_compared_by_quarter` | builder | Spike: 7 bars, 0.2 points, [hollis_voice_chart_quarterly.txt](spike/out/hollis_voice_chart_quarterly.txt). |
| DVB-R7 | Test deck starting 2025-07: `flag`, check `deck_history_vs_metrics`, months left out 2025-01 to 2025-06, text names the climb from $2,651 to $19,462 | `test_chart_starting_six_months_late_is_flagged` | builder | Spike: [hollis_voice_chart_starts_late.txt](spike/out/hollis_voice_chart_starts_late.txt). This is the roadmap's Done when. |
| DVB-R7 | Brasswick: `flag` naming 2025-05 to 2025-12, the 2025-09 peak of $84,090 and the 28.2% fall to $60,400 | `test_brasswick_partial_history_names_hidden_peak` | builder | Spike: [brasswick.txt](spike/out/brasswick.txt). |
| DVB-R7 | Brasswick BF2 counts as found by the scorer, and no decoy is flagged | `python -m scans.redflags data_room/brasswick`, then `python -m eval.score data_room/brasswick`; read "found" for BF2 and "decoys flagged 0" | builder, then the orchestrator on the merged engine | Spike, scored with `eval.score.score` on these claims alone: found 1 of 5 (BF2), decoys flagged 0 of 3, [validate_brasswick.txt](spike/out/validate_brasswick.txt). |
| DVB-R7 | Hollis Voice real deck: window `info`, no partial-history flag | `test_full_history_chart_is_info` | builder | Spike: `redflags-dvb-003` info. |
| DVB-R7 | Quarterly test deck: partial-history `flag` saying no month inside a quarter fell | `test_quarterly_chart_flags_partial_history` | builder | Spike: `redflags-dvb-003` in [hollis_voice_chart_quarterly.txt](spike/out/hollis_voice_chart_quarterly.txt). |
| DVB-R8 | Unreadable test deck: gap "Not in the room: a readable chart on slide 3", window still checked | `test_unreadable_chart_is_a_gap` | builder | Spike: [hollis_voice_chart_unreadable.txt](spike/out/hollis_voice_chart_unreadable.txt). |
| DVB-R9 | No claim is written from revenue-row differences (Brasswick 2026-09, the clean room's pilot months) | `test_revenue_row_differences_write_no_claim` | builder | Spike writes none. |
| DVB-R9 | P&L missing, revenue rows present: the window check runs from the revenue rows and cites them | `test_window_from_revenue_rows_when_pnl_missing` | builder | Not spiked. |
| DVB-R10 | No deck: one gap, no claims. No P&L: the P&L gap with `piece="traction_and_revenue"` | `test_missing_deck_is_one_gap`, `test_missing_pnl_gap_has_piece` | builder | Spike: the P&L gap, without `piece` (the field was added after the spike's schema). |
| DVB-R10 | A chart window reaching months the books lack writes the ask-list gap | `test_chart_months_missing_from_books_is_a_gap` | builder | Not spiked: needs a made-up test deck whose chart starts before 2025-01. |
| DVB-R11 | Claim value labels: ARR `arr`; partial history `other` with unit `months` | `test_value_labels_route_pieces` | builder | Spike JSON in [02_interface_example.md](02_interface_example.md). |
| DVB-R12 | Every claim from this check passes the quote checker on all four rooms and on the test-deck rooms | `test_every_claim_passes_quote_checker` (calls `schema.check_quotes.check_claim`); and `python -m schema.check_quotes data_room/hollis_voice out/hollis_voice/redflags.json` | builder | Spike: all claims verified in every run, `spike/out/validate_*.txt`. |
| DVB-R13 | No network and no model call: the check passes with `TRICORDER_OFFLINE=1` and no `ANTHROPIC_API_KEY` | `TRICORDER_OFFLINE=1 pytest scans/redflags/tests/test_deck_vs_books.py` | builder | Not run. |
| DVB-R13 | Bars read from pdfplumber's crop render, not pypdf | `test_bars_read_without_pypdf` (asserts pypdf is not imported by the module) | builder | Spike check: same bar counts at 150 and 200 dpi, [crop_render_check.txt](spike/out/crop_render_check.txt). |
| All | Full suite green, engine still runs on every room | `pytest`; `python -m scans.redflags data_room/hollis_voice` and the other three rooms | builder, then the captain at merge | Not run. |
| Roadmap Done when | "every deck revenue figure is matched to a P&L period or listed as unmatched" on Hollis Voice | `test_finds_every_revenue_figure_hollis` plus `test_hollis_arr_flags_against_pnl` | builder | Spike: 3 of 3 matched, 0 unmatched. |

## Testing review

Selected findings from reading the spike's runs, with what the Plan does about each:

| Finding | Disposition |
|---|---|
| The pixel reader is tuned to the generator's charts. A real deck can break it. | Accepted for Saturday. The rooms are generated. DVB-R8 makes failure a gap, not a wrong flag, when no bars are found. A real deck with a stacked chart could still give a false shape flag: noted in the architecture's failure modes. |
| The spike lists unmatched figures outside the claims. `ScanResult` has no such list. | Changed: unmatched figures become `info` claims (DVB-R5). |
| The clean room's `mrr` column carries the pilot while its P&L recurring line does not. | Revenue rows are a cross-check only (DVB-R9). |

## Rollout and release

No flag. The pull request merges to `main` when `pytest` passes and the table's commands read as expected. The captain merges, by [guardrails.md](../../../.claude/guardrails.md). No human document approval is needed for this route.
