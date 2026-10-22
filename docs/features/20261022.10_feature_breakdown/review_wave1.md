# Review, wave 1: deck-vs-books, accounting mislabels, checklist coverage

Independent code-quality and completion review (Feature Forge, required before the pull request). The reviewer edited no code. This file is the only thing written to the repo.

## What was inspected

- Repo `/home/claude/tricorder`, branch `claude/project-thread-dfe7j4`, HEAD `2e246be156a48725baa4b57cf3664fc0dd9522cc`.
- Diff: `git diff origin/claude/project-thread-ce34ga...HEAD -- scans schema`, 9 files, 3,496 lines added:
  `scans/redflags/deck_vs_books.py` (601), `scans/redflags/mislabels.py` (837), `scans/memo/coverage.py` (360), `scans/memo/checklist.py` (305), their tests and fixtures, and one key in `schema/settings.py` (`chart_shape_tolerance`, 0.02).
- Authorities read: the three features' `03_prd.md` and `05_plan.md`; ARCHITECTURE "The scan interface" and "How the readout is built"; FRAMEWORKS 1.12 and the checklist rows in `docs/ongoing/checklist.csv`; the three answer keys; `eval/score.py`; `scans/redflags/scan.py`; `scans/memo/merge.py`.
- The working tree has one untracked folder that is not part of the diff: `docs/features/20261022.12_accounting_mislabels/spike/test_rooms/`.

## Commands run, with results

| Command | Result |
|---|---|
| `python3 -m pytest` | 184 passed in 13.3 s, 0 skipped (matplotlib, reportlab and pypdf are installed, so the test-deck tests ran) |
| `python3 -m scans.redflags data_room/hollis_voice` | 10 claims, 4 gaps |
| `python3 -m scans.redflags data_room/hollis_voice_seed_drop` | 6 claims, 6 gaps |
| `python3 -m scans.redflags data_room/hollis_voice_clean` | 10 claims, 4 gaps, no flag or watch |
| `python3 -m scans.redflags data_room/brasswick` | 11 claims, 2 gaps |
| `python3 -m scans.memo <room>` (each of the four) | 0 unverified claims in every room; coverage panels written |
| `python3 -m eval.score data_room/hollis_voice` | found 0 of 8; decoys flagged 0 of 3 |
| `python3 -m eval.score data_room/hollis_voice_seed_drop` | found 0 of 8; decoys flagged 0 of 3 |
| `python3 -m eval.score data_room/hollis_voice_clean` | found 0 of 0; decoys flagged 0 of 3 |
| `python3 -m eval.score data_room/brasswick` | found 4 of 5 (BF1, BF2, BF3, BF4; BF5 is the video scan's); decoys flagged 0 of 3 |
| `python3 -m scans.redflags data_room/hollis_voice_clean_seed_drop`, and the same on an empty room and a CSV-only room (scratchpad, `TRICORDER_OUT_DIR` in scratchpad) | No crash. Gaps written. |
| Probe scripts in the scratchpad (listed under each finding) | Results quoted in the findings |
| Search of the diff for U+2014 and U+2013 | None |
| Search of the four modules for `requests`, `urllib`, `socket`, `anthropic`, `httpx`, `openai` | None. No network or model call. |

The Hollis Voice score of 0 of 8 is expected for this wave. PF1 and PF2 are scored only under the engine's check names (`arr_from_subscription_rows`, `deck_claim_vs_named_cell`), which are not built yet. This wave's mislabels claim (`mrr_column_vs_subscription_rows`) and deck claim (`deck_revenue_vs_pnl`) flag the same problems under their own names, by design (mislabels PRD scope, deck-vs-books Q1).

## Findings, by severity

No blockers. Nothing here breaks the demo rooms, and every number checked on the four rooms matched the PRDs. The should-fix items are requirement gaps, one crash path, and false or unsourced claim text.

### Should fix

**S1. deck-vs-books: the half-step rule never runs in production.**
- Where: `scans/redflags/deck_vs_books.py:256` and `:265`. `number, _ = parse_money(printed)` throws the half step away, and `Figure(...)` is built without `half_step`, so it is always 0.0 when `_stated` reads it at `:412`.
- Requirement: DVB-R3 ("a figure printed in short form, with no exact form anywhere in the deck, also matches when the difference is within half a unit of its last printed digit").
- Observed: a `claims.json` fallback room whose ARR is "$2.2M" against books of $2,240,868 is a `flag` ("a gap of 1.8%"), though $40,868 is inside the $50,000 half step. Probe: `scratchpad/probe_dvb.py` printed `HALFSTEP probe: flag The deck's ARR of $2,200,000 ...`.
- Why the tests miss it: `test_rounded_figure_within_half_step_matches` calls `figure_matches()` directly with a hand-passed half step. No test goes through `deck_figures`.
- Fix: keep the half step from `parse_money`, and set it only when no exact form of the figure appears anywhere in the deck. Add a test through `check()` on a short-form room.

**S2. deck-vs-books: a plan-growth mismatch is written as `info`.**
- Where: `deck_vs_books.py:529`, where severity is the literal `"info"` whatever `ok` is.
- Requirement: DVB-R4 ("A mismatch has severity `flag`").
- Observed: a figure of 8.0% a month against plan columns of 3.50% gives `info` with the text "differs from". Probe output: `PLAN probe: info The deck's plan growth of 8.0% a month (slide 11) differs from ...`.
- Fix: `"info" if ok else "flag"`. Add a test with a mismatched percentage, for example a Figure built in the test.

**S3. deck-vs-books: a chart that ends early is reported as "no month left out".**
- Where: `deck_vs_books.py:470-513`. `_history` compares only the chart's first month with the first revenue month. It never compares the chart's last month with the last actual month, but the info text at `:506-507` says "runs to {end} with no month left out".
- Requirement: DVB-R7 and the principle that a claim states only what a script checked. The roadmap's rule is "show only part of your history".
- Observed: a Brasswick chart from 2025-05 to 2025-09, ending at the peak and hiding the 28% fall, gives `info`: "The revenue chart on slide 4 starts at 2025-05, the first revenue month in the books, and runs to 2025-09 with no month left out." The books run to 2026-09 (probe run inline, output quoted).
- Fix: at the least, stop the text from saying "no month left out" when `window[-1] < books.actual[-1]`. Better, treat trailing months left out the same way as leading ones (`describe_hidden` on the months after the window). That widens DVB-R7, so Ken or the PRD owner decides; the false text should be fixed either way.

**S4. deck-vs-books: one blank revenue cell crashes the whole red-flag scan.**
- Where: `deck_vs_books.py:551-593` has no per-figure guard. `_grew` (`:538`, `total[m]`), `_chart` (`:444`, `line[m]`) and `_history` (`:482`, `line[m]`) index month dictionaries that drop non-numeric cells (`load_pnl`, `:302-303`). `scans/redflags/scan.py:52` calls `check()` with no guard, so the mislabels claims are lost too.
- Requirement: DVB-R10 and ARCHITECTURE "Failure" (a missing input is a gap). Mislabels has this guard (AM-R6, `mislabels.py:804`).
- Observed: removing 2026-03 from Brasswick's "Total revenue" line in memory gives `CRASH in scan.run: KeyError '2026-03'`.
- Fix: wrap each figure's check in `check()` and turn an exception into a gap, as `mislabels._run` does. Also guard `abs(value)` = 0 at `:413`.

**S5. deck-vs-books: the "grew every month" flag cites the wrong cells.**
- Where: `deck_vs_books.py:548`. Sources are the cells for December of the year before and the first month only, not the months that fell.
- Requirement: DVB-R4 ("every P&L cell the books figure was made from").
- Observed: "grew every month in 2025" on Brasswick flags falls in 2025-10 and 2025-12 and cites only `P&L!C9` (2025-05).
- Fix: cite each falling month's cell and the month before it.

**S6. mislabels: `not_run` writes no gap for kinds a and h.**
- Where: `scans/redflags/mislabels.py:342-344` (kind a) and `:746-748` (kind h).
- Requirement: the PRD's outcome table ("not_run: No claim. A gap with `why` 'not stated in the file'") and AM-R4. Kind c does this right (`:492`).
- Observed: Brasswick's result holds 2 gaps, neither for kind a nor kind h, though `outcomes()` gives both `not_run`. An empty room is the same.
- Fix: write a gap in each `not_run` branch, worded from entry 1.12. Extend `test_mrr_not_run_on_brasswick` and `test_one_time_fees_not_run_on_brasswick` to assert the gap. `test_gaps_use_entry_1_12_wording_and_piece` checks only the "Not in the room:" prefix, so it could not catch this.

**S7. mislabels: the Brasswick kind b flag does not cite the numbers it states.**
- Where: `mislabels.py:436-439`. The claim states billings of $82,650 and revenue of $59,565 from `revenue_by_customer.csv`, but its only source is `P&L!S7`.
- Requirement: PRODUCT_BRIEF "every claim links to its source". AM-R5 passes only because the one source it has is quoted correctly.
- Fix: cite the customer-file rows behind the billings-side difference (the Ostley Freight row, as kind g does at `:700`). The clear claims at `:457`, `:654` and `:726` cite the CSV header row as their only file source. That is weak but not false; see U4.

**S8. mislabels: a text cell in a number column fails the whole sub-check.**
- Where: `mislabels.py:95-98`. `num()` raises `ValueError` on text, and `_run` (`:804`) turns that into `cannot_check` with gap text such as "ValueError: could not convert string to float".
- Requirement: the PRD failure case "A number cell holds text: the row is skipped and counted; when more than 1 percent of rows are skipped, the sub-check returns cannot_check". No test covers it.
- Fix: skip and count bad rows in the sums, and return `cannot_check` above 1 percent. Add the test.

**S9. coverage: this wave's deck checks never mark a row checked.**
- Where: `scans/memo/checklist.py:106`. `ENTRY_CHECKS["1.5"]` is `{"deck_claim_vs_named_cell", "deck_model_reconcile"}`. `deck_revenue_vs_pnl` and `deck_history_vs_metrics` appear nowhere in `checklist.py`.
- Requirement: CC-R5 ("checked" when a claim's check name belongs to the row's entry). C65, "Deck numbers match the model and the metrics export", is checked by 1.5.
- Observed: on all three merged readouts, C65 is "not_checked | No claim from 1.5 Deck-against-model reconciliation yet", although `redflags-007` to `-010` (Hollis Voice) are deck-against-P&L claims. `test_entry_checks_cover_every_entry` asserts only that each entry has some name.
- Fix: add both names to 1.5, or add a `ROW_CHECKS` entry for C65 (and C17 for partial history, if the checklist owner agrees). Add a test that feeds a `deck_revenue_vs_pnl` claim and expects C65 checked.

**S10. coverage: a check row that did run is reported as "Cannot run".**
- Where: `scans/memo/coverage.py:115-130`. The "missing inputs" branch comes before the "has a claim" branch.
- Requirement: CC-R5 and CC-R7, and FRAMEWORKS 1.12 ("with only the seed drop, kinds a, d and h still run from the model").
- Observed: on the seed drop, C06 is "missing | Cannot run: needs C03, not in the room" while `redflags-001` is a kind a flag from the ARR_Build fallback. The row's text is false. The PRD's rule ("a check row whose ... input documents are not in the room is `missing`") produces it, so the PRD wording needs a decision too.
- Fix: when claims exist, keep the request for the missing file but word the detail as "Checked by redflags-001 from the model; C03 would let it run on the customer file". Or mark it `checked` and still fold the row into C03's ask line.

**S11. coverage: three tests prove less than the plan says.**
- `test_no_request_twice` (`scans/memo/tests/test_coverage.py:311`) calls `coverage.apply` directly. The plan's CC-R14 row says it "runs the real merge with fake scan outputs". The seam with the ask-list step is not exercised. Since `asks.py` does not exist, at least rename the claim in the plan, and add the merge-level test when `asks.py` lands.
- `test_cannot_check_is_not_checked` (`:189`) passes no claims at all, so C81 could never be checked. It proves nothing about an entry that returned `cannot_check`. Feed a claim from an entry that also wrote a `cannot_check` gap, or drop the requirement's second clause.
- `test_runs_offline` (`:372`) patches only `socket.create_connection`. The deck-vs-books test patches `socket.socket.connect`, which also catches lower-level connections. Use the same patch here.

**S12. coverage: the PRD and the code disagree on file matching.**
- Where: `checklist.py:246-259`. CC-R6 and the architecture (`04_architecture.md:106`) say "patterns, then the cover note index". The code uses patterns and then `CONTAINED` rules. `00_progress.md:55` records the change, but the PRD and Plan still state the old rule.
- Fix: update CC-R6 and the Plan's slice 1 scope to match the code, or build the cover-note fallback. This is a docs fix unless Ken wants the fallback.

### Suggestions

- **U1. deck-vs-books, misleading reason.** `deck_vs_books.py:388-411`: when the deck has no "Data as of" line, an ARR or last-12-months figure is unmatched with "no rule maps the label 'ARR' to a P&L line". The real reason is that no as-of month was found.
- **U2. deck-vs-books, Brasswick "grew every month in 2026".** Revenue fell $2,705 from 2025-12 to 2026-01, and the claim is `info` because only months inside 2026 are compared. That follows DVB-R2 and the agreed interface example, but January's growth is negative month on month. It is part of BF2's story. This is a product call for Ken: compare January with December, or keep `info`.
- **U3. Hard-coded room shapes.** `deck_vs_books.py:55-56` (`ROW_COLUMNS`), `mislabels.py:41-42` and `:228-232` (`layout_for`), and `:350-351` and `:755` (`product_type`, `mrr`) name the two generators' files and columns. A third room's customer file under another name gives b, c and g a `cannot_check` gap with `why` "file missing", which is false because the file is there. This is fine for Saturday, but the gap's `why` should say "file not recognised".
- **U4. Header-row sources.** `mislabels.py:457`, `:654` and `:726` cite CSV row 1 as the source for computed totals (for example "$104,876 across 28 customers"). They pass the quote checker, but a reader who clicks finds column names. Name the script in the text, or cite one representative row.
- **U5. Duplicate gaps in one result.** An empty or CSV-only room gets "Not in the room: an expense ledger" twice (kinds e and f) and "a financial model" twice. Coverage merges them, but `redflags.json` shows both.
- **U6. Claim ids skip numbers.** `mislabels.py:801-807` throws away the claims of a sub-check that fails midway, but their ids are already taken from `Ids`, so the sequence has holes. This is harmless.
- **U7. History value.** `deck_vs_books.py:499` adds skipped bars to months left out in `Value.number`. DVB-R7 says the value is the number of months left out.
- **U8. Founder-facing ask text.** Gap lines use the raw `would_need` as `what`. The ask then reads "the option grant records for every holder (02_financials/cap_table.xlsx, Cap_Table!A7)", with an internal cell reference, or a fragment like "monthly revenue by customer with a product type column". On the seed drop, kind g's balance-sheet gap is tagged C03 because its `would_need` contains "revenue by customer" (`checklist.py:149`, `items_for_gap`).
- **U9. Ask line numbers.** `coverage.py:335-338`: the coverage panel's `ask_line` counts coverage's own lines, not positions in `readout.asks`. It will drift once the ask-list step adds lines.
- **U10. Brittle workbook test.** `test_missing_pnl_row_is_a_gap` saves the model with openpyxl, which drops cached formula values (the mislabels Plan says so). It passes for the right reason today, but other sub-checks in that run see empty totals.

## Verdicts by feature

| Feature | Code quality | Completion against the Plan |
|---|---|---|
| deck-vs-books (.11) | **Fail** until S2, S4 and S5 are fixed. The code is clear and well structured, and every demo-room number matches the Plan. | **Fail** on DVB-R3 (S1: marked Pass, but the test does not use the production path), DVB-R4 (S2, S5) and DVB-R7 (S3, false text). Every other row was verified: R1, R2, R5, R6, R8 to R13, BF2 found, 0 decoys. |
| accounting mislabels (.12) | **Pass**, with S7 to fix. Per-sub-check isolation, tolerance from settings and the claim fields are all correct. | **Fail**, narrowly: the outcome table's `not_run` gap (S6) and the PRD's text-cell failure case (S8). AM-R1 to AM-R5, AM-R7 to AM-R30 verified, including Brasswick BF1, BF3 and BF4, 0 decoys in all four rooms, and a clean room with no flag or watch. |
| checklist coverage (.13) | **Pass**, with S9 and S10 to fix. No model, no network, stage handling and dedupe correct on the three rooms. | Slices 1 and 2: **fail** on S9 (C65 not checked by the real claims) and S11 (the CC-R14 evidence overstates the test). CC-R1 to CC-R13, CC-R15, CC-R16 and CC-R18 verified on real merges. Slices 3 and 4 (CC-R2 route, CC-R17, CC-R19 panel): **unverified**, not started, as the Plan says. |

## To delete at cleanup

- Scratchpad probe and test rooms made by this review (outside the repo): `/tmp/claude-0/-home-claude/76c6a462-572c-5250-967a-649aceb49eaf/scratchpad/` (`probe_dvb.py`, `rooms/`, `out/`, and a temp room folder from `make_room`). Under `/tmp`, so the OS owns them.
- `out/<room>/redflags.json` and `readout.json` for the four rooms, rewritten by the commands above. `out/` is gitignored.
