# Plan: claim support

## Throughput checkpoint

One owner (this builder), one package (`scans/claims/`) plus one memo module. No shared writable state with the other wave 2 builders: no schema edit, no `merge.py` edit, no route, no page change. The slices ran in order because each reads the one before.

## Slices

| Slice | Outcome | Scope | Depends on | Lands as |
|---|---|---|---|---|
| 1. Number parser | Every printed and spoken figure parsed with unit, precision, hedge and bound | `scans/claims/numbers.py`, `test_numbers.py` | none | commit `b55ddcf` |
| 2. Extract, evidence, label | The claims scan on every room, with the table, counts and gaps | `extract.py`, `kinds.py`, `evidence.py`, `label.py`, `read.py`, `scan.py` | 1 | commits `eca84f1`, `2a6ba1e` |
| 3. Memo step | Claims relabelled against other scans' flags | `scans/memo/claim_support.py`, its tests | 2 | commits `7d3b921`, `e79f4ec`, `e9c91fd` |
| 4. Verification fixes and docs | Wording fixes found while driving the recipe, the failure case test, the dossier, the verification map | `label.py`, tests, this folder, `.claude/skills/verify-tricorder/features/claim-support.md` | 3 | commits from `f4e276d` on |

Integration owner: the orchestrator, who adds `claim_support` to `scans/memo/merge.py` STEPS after `link` and before `pieces`.

## Verification table

Revision: the branch head at report time. Every command runs from the worktree root. "Suite" means `python3 -m pytest`.

| Requirement | Acceptance or failure case | Command or observation | Owner | Evidence and status |
|---|---|---|---|---|
| CS-R1, CS-R2 | Every figure on every slide is in the table, appendix rows folded in as repeats | `test_every_figure_line_is_covered` (4 rooms) | builder | pass |
| CS-R3 | Script lines cited by line and beat and labelled as the script; transcript segments by seg with times | `test_script_claims_are_labelled_as_the_script_not_the_video`, `test_transcript_is_used_and_times_are_copied`, `test_whisper_cpp_output_shape` | builder | pass (transcripts hand-built) |
| CS-R4 | Spoken figures marked spoken and rounded | `test_spoken_figures_are_marked_spoken_and_rounded`, `test_numbers.py` | builder | pass |
| CS-R5, CS-R9 | Each unsupported row has an ask line and a gap naming the document | `test_unsupported_claims_have_an_ask_and_a_gap`, `test_seed_drop_names_the_missing_customer_file` | builder | pass |
| CS-R6, CS-R7 | Planted contradictions contradicted with both sources | `test_planted_contradictions_are_contradicted_with_both_sources`; `spike/count_done_when.py` | builder | pass for PF2, PF2b, PF4 (hires), PF5, PF7, BF4, BF5 in the scan; BF1, BF2, BF3 after the memo step |
| CS-R7 | Green flags supported with a source outside the pitch | `test_green_flags_are_supported_with_two_independent_sources` | builder | pass for Hollis GF1 to GF3, Brasswick GF1 to GF3 |
| CS-R7 | No contradiction on the clean room | `test_clean_room_has_no_contradiction` | builder | pass |
| CS-R8 | The pitch never supports itself | `test_independence_the_pitch_never_supports_itself` | builder | pass |
| CS-R10 | Table, counts and not-counted Panels | `test_every_claim_has_one_label_and_one_row`, `test_examples_are_not_counted_as_claims` | builder | pass |
| CS-R11 | Quote checker passes on every claim | `test_quote_checker_passes_on_every_claim` (4 rooms); `count_done_when.py` reports 0 failures | builder | pass |
| CS-R12 | No key is a gap; bad facts dropped; refusal is a gap | `test_read.py` (hand-built responses) | builder | pass; live model untested |
| CS-R13 | Other scans' flags relabel; a shared export row does not; could not verify shown | `test_claim_support.py` | builder | pass |
| CS-R14 | Model-only support is said | `test_model_only_support_is_said_out_loud`, `test_a_rebuild_flag_from_a_later_check_relabels_the_model_only_figure` | builder | pass |
| CS-R15 | PF2b and BF5 score through the claims scan | `test_spoken_entries_score_through_the_claims_scan`; `eval.score` in the verification run | builder | pass |
| CS-F1 to CS-F7 | Partial rooms and input shapes | `test_inputs.py` | builder | pass |
| CS-F8 | Model refusal | `test_refusal_is_a_gap` | builder | pass |
| CS-F9 | Worked examples set aside | `test_examples_are_not_counted_as_claims` | builder | pass (Brasswick, 6 figures) |
| All | Driven as a user through control.sh | [06_verification.md](06_verification.md), `evidence/` | builder | pass |
| All | Full suite and CI gate | `python3 -m pytest`; `bin/ci-py` | builder | see [00_progress.md](00_progress.md) |

## Not done in this slice

- PF3 (102.6% NRR) and PF6 (80% gross margin) read supported, backed only by the model, with the note from CS-R14. They turn contradicted when the red-flag engine's rebuild checks (`rebuild_cohorts_from_customer_file`, `gross_margin_from_ledger`) land and the memo step runs. PF4's runway (37) and burn ($374,462) wait the same way on `payroll_from_hiring_plan_and_rerun_cash`.
- The claims table on the readout page.
- The model reading run live.

## Release

The orchestrator integrates the branch. Readiness: the full suite at 0 failed, `bin/ci-py` green, the verification run's evidence in `evidence/`.
