# Plan: accounting mislabels

Requirements: [03_prd.md](03_prd.md). Design: [04_architecture.md](04_architecture.md). Progress: [00_progress.md](00_progress.md).

Built test first on a `feat/accounting-mislabels` branch cut from `main` after the skeleton lands. The spike is throwaway: the builder reads it for behaviour and rebuilds the module through tests. All tests live in `scans/redflags/tests/test_mislabels.py` and run under `bin/ci-py` (`python -m schema.export --check`, then `python -m pytest`).

## Throughput checkpoint

- **Blocking prerequisites.** The skeleton on `main`: `schema/claim.py`, `schema/readers.py`, `schema/check_quotes.py`, `schema/settings.py`, `scans/base.py`, `scans/redflags/scan.py` and `eval/score.py`. All exist on `origin/claude/project-thread-ce34ga` (commit 573567f).
- **Independent workstreams.** The seven sub-checks are independent once the shared helpers exist (Layout, Pnl, the outcome-to-claims mapping). They could split three ways, but each is 20 to 60 lines over the same helpers.
- **Shared writable state.** Inside this feature: only `mislabels.py` and its test file. Outside it: `scans/redflags/` is shared with deck-vs-books (`deck_vs_books.py`) and the Saturday engine checks. Both this module and deck-vs-books parse the P&L tab. Neither edits `scan.py`. A shared `pnl.py` waits until both have landed.
- **Smallest safe decomposition.** One owner, five slices, one PR. Splitting the sub-checks across builders would make three people write the same helpers and the same fixtures for a module this size. The slices are commit boundaries, each green.

## Slices

| Slice | Outcome | Rows in the verification table | Depends on |
|---|---|---|---|
| S1. Frame and kind a | Layout, Pnl, Outcome, the outcome mapping, per-sub-check error capture; `mrr_column_vs_subscription_rows` with the seed-drop fallback and the shared-source link | AM-R1 to AM-R10 | skeleton |
| S2. Revenue family on the customer file | `billings_vs_recognised_revenue`, `deferred_revenue_vs_earned` (with the bridge test), `one_time_fees_in_recurring_metrics` | AM-R11, AM-R12, AM-R23 to AM-R26 | S1 |
| S3. Ledger family | `contractor_spend_vs_headcount_and_burn` (with vendor propagation and the plan test), `capitalised_spend_vs_pnl_and_cash` | AM-R16 to AM-R22 | S1 |
| S4. Kind c and the test room | The resale fixture; `gross_vs_net_revenue` on Brasswick and on the resale room | AM-R13 to AM-R15, AM-R30 | S1 |
| S5. Integration | Decoys, clean room, quote checker over every claim, the engine run and `eval.score` on all four rooms | AM-R27 to AM-R29 | S2 to S4 |

Integration owner: the builder. Safe landing: the module is listed in `CHECKS` already, so each merge to `main` turns on whatever sub-checks exist. Every slice keeps `bin/ci-py` green.

Contract for the builder:

- **Outcome.** `scans/redflags/mislabels.py` and `scans/redflags/tests/test_mislabels.py` pass every row below.
- **Read first.** This folder's PRD and architecture; [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md) "The shared Claim", "Settings" and entry 1.12; [data_room/README.md](../../../data_room/README.md); the skeleton's `schema/` and `scans/base.py`.
- **Owned files.** Only the two above. Do not edit `scan.py`, `schema/`, `data_room/` or another check's module.
- **Uncertainty rule.** If a room disagrees with a number in the PRD, rerun the spike (`python3 spike/mislabels_spike.py`) and trust the rooms. Ask the coordinator before changing a formula that the PRD marks "extends 1.12".
- **Never delete files.** List removals in Progress.

## Fixtures

```python
ROOMS = REPO / "data_room"
FULL, SEED, CLEAN, BRASS = (ROOMS / n for n in
    ("hollis_voice", "hollis_voice_seed_drop", "hollis_voice_clean", "brasswick"))

@pytest.fixture(scope="module")
def resale_rooms(tmp_path_factory) -> tuple[Path, Path]:
    """(off, on): copies of FULL; 'on' adds Resale rows from 2026-04 at $25 a location and the same money in mrr."""

def run(room) -> tuple[list[Claim], list[Gap]]:
    return mislabels.check(room, Ids("redflags"))

def by_check(claims, name, severity=None) -> list[Claim]: ...
```

## Verification

Commands run from the repo root. The evidence column records the run of 2026-10-22 on the branch claude/project-thread-dfe7j4: `python3 -m pytest -q scans/redflags/tests/test_mislabels.py` reports 68 passed (after the review fix round; see 00_progress.md). Test names are in `scans/redflags/tests/test_mislabels.py`.

| Requirement | Acceptance/failure case | Command/observation | Owner | Evidence/status |
|---|---|---|---|---|
| AM-R1 | `check(room, ids)` returns two lists of Claim and Gap; no network | `pytest scans/redflags/tests/test_mislabels.py::test_check_returns_claims_and_gaps` and `::test_runs_with_network_blocked` (socket patched to raise) | builder | pass: `test_check_returns_claims_and_gaps`, `test_runs_with_network_blocked`, `test_makes_no_model_call` |
| AM-R1 | Tolerance read from settings | `::test_tolerance_override_from_settings` (TRICORDER_SETTINGS file with 0.10 turns the full room's kind a flag into a clear: 8.7% is under 10%) | builder | pass: `test_tolerance_override_from_settings` |
| AM-R2 | Claim fields | `::test_every_claim_is_script_computed_with_its_check_name` over all four rooms | builder | pass on all four rooms |
| AM-R3 | Kind named in flag and watch text | `::test_flag_text_names_the_mislabel_kind` | builder | pass: every flag and watch text ends with its kind |
| AM-R4 | Gap wording and piece | `::test_gaps_use_entry_1_12_wording_and_piece` | builder | pass on all four rooms |
| AM-R5 | Quote checker | `::test_every_claim_passes_check_quotes` (all four rooms and both resale rooms) | builder | pass: `check_claim` on every claim, four rooms and both resale rooms |
| AM-R6 | A missing column or row becomes a gap | `::test_missing_column_is_a_gap_not_a_crash` (fixture drops `billings`), `::test_missing_pnl_row_is_a_gap`, `::test_locator_error_is_caught_per_subcheck` | builder | pass: all three tests |
| AM-R7, AM-R8 | Full room: pilot found in `mrr`, 2026-08 and 2026-09, $15,000, cites row 2101 | `::test_full_room_mrr_column_holds_the_pilot` | builder | pass: $186,739 against $171,739; row 2101 |
| AM-R9 | Link by shared source with entry 1.2 | `::test_mrr_claim_cites_the_pilot_arr_build_row` (cites `ARR_Build!A13` and `E13`); after the engine lands, `::test_mrr_claim_shares_a_source_with_arr_from_subscription_rows` on `scan.run(FULL)` | builder, then redflag-engine | pass: cites `ARR_Build!A13` and `ARR_Build!E13`; the engine-level test waits on entry 1.2 |
| AM-R10 | Seed drop: fallback runs; gap added | `::test_seed_drop_mrr_uses_arr_build_fallback` | builder | pass: fallback cites `ARR_Build!E13`, confidence computed, gap written |
| AM-R11 | Kind b clear on full room; DC2 June not flagged; Brasswick 2026-09 flagged | `::test_billings_clear_on_full_room`, `::test_billings_flags_brasswick_september` | builder | pass: clear on Hollis Voice; Brasswick $84,810 against $82,650 and $59,565 |
| AM-R12 | Kind b cannot_check on seed drop | `::test_seed_drop_cannot_check_without_customer_file[billings_vs_recognised_revenue]` | builder | pass |
| AM-R13, AM-R14 | Kind c flags Brasswick at 28.0%; resale on flags; off and full room not_run | `::test_gross_vs_net_flags_brasswick_recoveries`, `::test_gross_vs_net_fires_with_resale_on`, `::test_gross_vs_net_silent_with_resale_off` | builder | pass: Brasswick 28.0%; resale on 2.7%; off and full room not_run |
| AM-R15 | Kind c cannot_check on seed drop | `::test_seed_drop_cannot_check_without_customer_file[gross_vs_net_revenue]` | builder | pass |
| AM-R16 | Vendor propagation catches Norrgate | `::test_contractor_lines_include_the_whole_vendor` | builder | pass: Norrgate in, Abbotsford out |
| AM-R17 | Tie test clear on Hollis Voice | `::test_contractor_tie_clear_on_full_room` | builder | pass |
| AM-R18 | Plan test flags BF3; Brasswick DC2 controller stays clear | `::test_contractors_cut_from_plan_flag_brasswick` | builder | pass: $34,708.97 against $2,800 |
| AM-R19 | Full room clear with contractor-list gap; watch when contractors exist and no flag | `::test_contractors_clear_with_gap_on_full_room`, `::test_contractors_found_without_flag_is_watch` (fixture: a contractor line the plan keeps) | builder | pass: both tests (watch built by patching the plan in memory) |
| AM-R20, AM-R22 | e and f cannot_check on seed drop | `::test_seed_drop_cannot_check_without_customer_file[...]` parametrised over the ledger checks | builder | pass |
| AM-R21 | Kind f clear on both rooms, balance-sheet gap | `::test_capitalised_clear_with_balance_sheet_gap` | builder | pass: -$0.24 of $1,800,000; $0.21 of $641,318 |
| AM-R23 | Kind g clear on full room ($104,876 across 28 customers); Brasswick flagged for Ostley | `::test_deferred_clear_on_full_room`, `::test_deferred_flags_ostley_on_brasswick` | builder | pass: $104,876 across 28; Ostley $25,245 |
| AM-R24 | Bridge test info after a P&L flag | `::test_bridge_deferred_is_info_when_pnl_flag_fired` | builder | pass: info, $33,885 against $8,640 |
| AM-R25 | Kind g cannot_check on seed drop | parametrised seed-drop test | builder | pass |
| AM-R26 | Kind h clear on full room and seed drop; not_run on Brasswick | `::test_one_time_fees_clear[FULL]`, `::test_one_time_fees_clear[SEED]`, `::test_one_time_fees_not_run_on_brasswick` | builder | pass: $9,500 against $15,000; not_run on Brasswick |
| AM-R27 | No flag or watch cites a decoy row or cell | `::test_hollis_decoys_not_cited_by_any_flag`, `::test_brasswick_decoys_not_cited_by_any_flag` | builder | pass on all rooms |
| AM-R28 | Clean room: nothing flags or watches | `::test_clean_room_has_no_flag_or_watch` | builder | pass |
| AM-R29 | Answer-key score | `python -m scans.redflags data_room/<room>` then `python -m eval.score data_room/<room>` for the four rooms: 0 decoys flagged everywhere; BF1, BF3, BF4 found on Brasswick. As a test: `::test_eval_score_on_brasswick_finds_bf1_bf3_bf4` | builder at S5; captain at merge | pass: `python -m eval.score data_room/brasswick` prints found 4 of 5 (BF1, BF3, BF4 from this module; BF2 from deck_vs_books), decoys 0 of 3; Hollis Voice, seed drop and clean room decoys 0 of 3 |
| AM-R30 | Fixture writes only under `tmp_path` | `::test_resale_fixture_writes_nothing_under_data_room` (hash of `data_room/` before and after) | builder | pass: `test_resale_fixture_writes_nothing_under_data_room` |
| Entry 1.12 output shape | Panels carry the entry label, the checks table and the lines table; the engine result holds them | `::test_panels_carry_entry_checks_and_lines`, `::test_seed_drop_entry_label`, `::test_engine_result_holds_mislabels_claims_and_panels`; `python3 -m scans.redflags data_room/hollis_voice` | builder | pass: the engine writes 10 claims and 4 gaps to `out/hollis_voice/redflags.json`, redflags-001 to 006 from this module |
| All | Full suite green | `bin/ci-py` reads 0 failed | builder, then captain | pass: `python3 -m pytest` 203 passed |

## Testing findings

From the spike, before any review:

- Brasswick's kind b and kind g both flag the Ostley invoice. That is correct for each formula. The tests assert both, and the shared-source test asserts they share `P&L!S7`.
- The first spike run flagged Brasswick DC1 through the bridge-deferred claim. AM-R24 and its test exist because of that run.
- The resale room's kind a claim first cited a Brookline Row Resale row, because the fixture adds resale rows to every clinic. Kind a now cites the largest row per product type. The decoy test runs on the real rooms, where Brookline has no Resale row.

- Saving a workbook with openpyxl drops every cached formula value, so a test that edits the model on disk breaks the totals. The watch test patches the parsed P&L in memory instead.

## Rollout and final verification

- Merge after `bin/ci-py` is green and the AM-R29 commands print the expected score lines.
- On Saturday, at the engine's integration point, the captain runs `bin/smoke data_room/hollis_voice` and checks that the redflags result holds the mislabels claims beside entry 1.2's flag.

## Release authority

The captain merges to `main` ([ROADMAP.md](../../ongoing/ROADMAP.md), "How to read a slice"). No human document approval is needed for this route.
