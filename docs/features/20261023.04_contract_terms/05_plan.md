# Plan: contract-terms

Requirements: [03_prd.md](03_prd.md). Design: [04_architecture.md](04_architecture.md). Progress: [00_progress.md](00_progress.md).

## Implementation strategy

### Throughput checkpoint

- **Blocking prerequisites.** None: wave 1 is on `main` (the engine, the readers, the quote checker, the memo's coverage step).
- **Independent workstreams.** None worth splitting. The reader and the checks share `ContractTerms`.
- **Shared writable state.** One line in `scans/redflags/scan.py` (`CHECKS`), and one sentence in `scans/redflags/__init__.py`'s docstring. Nothing in `schema/`, `data_room/`, `server/` or `scans/memo/`.
- **Smallest safe decomposition.** One builder, branch `forge/contract-terms`, two slices.

### Slices

| # | Outcome | Scope | Landing |
|---|---|---|---|
| 1 | The shared reader and the clause notes | `contract_reader.py`; `clause_notes`; Panels; CT-R1, R2, R7, R8, R10, R11, R12 | Commit `3338036` |
| 2 | Checks 1, 3, 4 and 6 and the ask lines | `contract_terms_full.py` checks; CT-R3 to R6, R9, R13 | Commits `3338036` and `32a82d7` |

Tests were written first, as one file, and run red (the module did not exist: [evidence/tests_red.txt](evidence/tests_red.txt)); the modules made them green.

## Verification

Every row is a test in `scans/redflags/tests/test_contract_terms_full.py` that runs the real `check()`, the real engine (`scan.run`) or the real memo (`build_readout`), unless it says otherwise. Results: [evidence/tests_contract_terms.txt](evidence/tests_contract_terms.txt) (29 passed) and [evidence/ci_py.txt](evidence/ci_py.txt) (`bin/ci-py`, whole suite).

| Requirement | Test | Evidence |
|---|---|---|
| CT-R1 contracts found; contracts-only folder | `test_a_folder_of_only_contracts_is_read_with_no_crash` (also runs `scan.run` on the folder) | pass; driven by CLI in [06_verification.md](06_verification.md) |
| CT-R2 missing and unreadable inputs | `test_seed_drop_has_no_contracts_and_says_so`, `test_a_pdf_that_cannot_be_read_is_a_gap`, the contracts-only test's counting gap | pass |
| CT-R3 check 3 | `test_plan_check_flags_marlow_with_its_eight_plan_months`, `test_plan_check_clears_cedar_pine_and_brookline_row` | pass; Marlow $161,258 over 2027-02 to 2027-09, as FRAMEWORKS 1.13 states |
| CT-R4 check 4 | `test_signed_not_live_clears_the_three_hollis_contracts`, `test_signed_not_live_flags_revenue_before_the_effective_date` | pass |
| CT-R5 check 6 | `test_counted_lines_without_contract_are_seven_gaps`, `test_coverage_claim_is_27_6_percent` | pass |
| CT-R6 ask lines | `test_missing_contracts_become_ask_lines_through_the_memo` (engine, then the memo merge) | pass; seven C34 lines through the API in [06_verification.md](06_verification.md) |
| CT-R7 clause fields | `test_clause_fields_are_not_stated_on_hollis_read_from_each_contract`, `test_change_of_control_clause_returns_its_quote` | pass |
| CT-R8 other clauses | `test_fee_freeze_is_an_other_clause_on_cedar_pine` | pass |
| CT-R9 check 1 | `test_thirty_day_cancellation_counted_as_a_year_of_arr_is_flagged`, `test_one_year_commitment_is_not_flagged`, `test_notice_check_on_hollis_flags_marlow_only`, `test_a_term_that_ended_but_is_still_counted_is_flagged`, and the change-of-control test's last assert | pass |
| CT-R10 supplier contracts | `test_supplier_contract_gets_no_customer_checks` (Brasswick's Norrgate statement of work) | pass |
| CT-R11 one reading, model seam | `test_each_contract_is_read_once_for_both_modules`, `test_a_model_reader_plugs_in_and_a_failed_one_falls_back` (hand-built model reading, labelled; no model called) | pass |
| CT-R12 every quote | `test_every_quote_passes_the_quote_checker` (Hollis Voice, clean, Brasswick, seed drop), `test_every_quote_passes_on_the_test_contracts` | pass; 0 unverified claims in the memo merge |
| CT-R13 engine, offline, no decoy | `test_the_engine_lists_the_module_and_leaves_saturdays_name_free`, `test_no_decoy_is_flagged_and_claim_ids_are_unique`, `test_runs_offline`, `test_result_serialises` | pass; `eval.score` decoys flagged 0 of 3 before and after ([evidence/score_before.txt](evidence/score_before.txt), [evidence/score_after.txt](evidence/score_after.txt)) |
