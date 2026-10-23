# Feature progress: contract-terms

**Now.** Built, tested and driven. `scans/redflags/contract_reader.py` (the one contract reader for entry 1.13) and `scans/redflags/contract_terms_full.py` (checks 1, 3, 4 and 6 and the clause notes) run inside the red-flag engine. On Hollis Voice the plan check flags the Marlow pilot with its eight plan months after the term ends ($161,258 of plan revenue) and clears Cedar & Pine and Brookline Row. The three clause fields read "not stated" on every Hollis Voice contract, each citing every page it read. Whole suite: 214 passed, 18 skipped (wave 1's deck tests, matplotlib missing here) ([evidence/ci_py.txt](evidence/ci_py.txt)). **Next:** the orchestrator merges `forge/contract-terms`; Saturday's team adds `contract_terms.py` on the seam in [04_architecture.md](04_architecture.md).

Roadmap slice: [contract-terms](../../ongoing/ROADMAP.md#contract-terms). Route: prototype first, nonvisual, with an interface example printed by a real spike.

## Attention needed

1. **Saturday's contract-terms team (backend-and-data).** Check 1 (`cancellable_within_notice_vs_arr`) is built here, because this slice's Done when needs the 30-day test. Saturday's `contract_terms.py` should write only checks 2 and 5, register its model reading with `contract_reader.set_model_reader(fn)`, and read contracts only through `contract_reader.read_room`. It should not write "Not in the room: a customer row for <name>" again; this module does. The seam: [04_architecture.md](04_architecture.md), "The seam with Saturday's module".
2. **Ken: two rule questions** ([03_prd.md](03_prd.md), Q1 and Q2). A later renewal order form for a long-time customer trips check 4 under FRAMEWORKS' rule. A month-to-month contract has no term end, so check 3 cannot run on it.
3. **Roadmap wording (roadmap writer).** "A test contract with a 30-day cancellation counted as a year of ARR produces a gap" is met as a `flag` under check 1, which is FRAMEWORKS 1.13's sense of a gap ("any place the counting runs ahead of the paper"), not a `Gap` object (a missing input).
4. **Coverage owner (captain).** `scans/memo/checklist.py` has no mapping for `clause_notes`, the check name checklist row C172 gives, so C172 shows as not checked. One line in `ROW_CHECKS` (`"C172": {"clause_notes"}`) and the name in `ENTRY_CHECKS["1.13"]` would fix it. Also PRD Q4: the seven contract ask lines on Hollis Voice could fold into one, as the SAFE lines do.
5. **Server owner.** `server/app.py`'s `rooms()` lists only folders with a `00_` to `09_` subfolder. A contracts-only upload works through the CLI under any layout, and through the API only as `rooms/<name>/04_customers/*.pdf`.
6. **FRAMEWORKS owner.** Entry 1.13's `Term` has no status for a quote the checker cannot find; this module adds `quote_not_found` in its own model. Brasswick returns three `watch` results on check 3 (automatic renewals the plan carries, no non-renewal rate stated), which follows the entry's rule; the worked example does not list Brasswick for check 3.

## Review round 1 (wave 2a)

Review: [review_wave2a.md](../20261022.10_feature_breakdown/review_wave2a.md), read, not edited. Branch `claude/project-thread-ea11in` merged first (per-module claim ids, a module crash becomes a gap).

| Finding | Disposition | Test, red then green |
|---|---|---|
| B1. The clean room got two false flags on the Marlow pilot from checks 1 and 3, citing no ARR build cell | Fixed in `5b83853`. A check says a contract is counted only when `recurring_count` finds the counting row: an `ARR_Build` line for the customer or its cohort, or with no ARR build, the customer file's subscription rows. The flag cites that row (`ARR_Build!E13` for Marlow). Otherwise an info claim says what was found ("the ARR build does not count it"). Coverage counts only customers the counting holds: $36,584 of $171,739 in the clean room. | `test_clean_room_raises_no_flag_or_watch_on_marlow`, `test_a_counted_flag_cites_the_counting_row` (red, then green); `test_clean_room_coverage_leaves_out_the_uncounted_pilot` (written with the fix) |
| O8 (deck part). A deck that is not a PDF crashed `synthetic_notice` and `deck_vs_books` | Fixed in `debee0c`. No banner, and the gap "Not in the room: a readable pitch deck". | `scans/redflags/tests/test_unreadable_deck.py`, 3 tests, red then green, including the memo merge |

## Documents

- [product_thinking.md](product_thinking.md) and [01_brief.md](01_brief.md)
- [02_interface_example.md](02_interface_example.md): the prototype, generated from [spike/out/](spike/out/) by [spike/render_interface_example.py](spike/render_interface_example.py); the spike is [spike/contract_terms_spike.py](spike/contract_terms_spike.py)
- [03_prd.md](03_prd.md): CT-R1 to CT-R13, failure cases, questions
- [04_architecture.md](04_architecture.md): the reader, the seam, check 1's home, alternatives
- [05_plan.md](05_plan.md): slices and the [verification table](05_plan.md#verification)
- [06_verification.md](06_verification.md): the verify-tricorder run and the score before and after
- Map file: [.claude/skills/verify-tricorder/features/contract-terms.md](../../../.claude/skills/verify-tricorder/features/contract-terms.md)

## Work and evidence

| Outcome | Owner | State | Evidence | Next action |
|---|---|---|---|---|
| Tests first | agent | done | red: [evidence/tests_red.txt](evidence/tests_red.txt); green: [evidence/tests_contract_terms.txt](evidence/tests_contract_terms.txt) | none |
| Shared reader and clause notes | agent | done, committed | CT-R1, R7, R8, R10 to R12 rows in the Plan | none |
| Checks 1, 3, 4, 6 and ask lines | agent | done, committed | CT-R3 to R6, R9, R13 rows | none |
| Interface example from the spike | agent | done | [02_interface_example.md](02_interface_example.md), 0 quotes failed in every run ([spike/out/spike_run.txt](spike/out/spike_run.txt)) | none |
| Driven through verify-tricorder | agent | done | [06_verification.md](06_verification.md), [evidence/verify/](evidence/verify/) | none |
| Whole suite and `bin/ci-py` | agent | done | 214 passed, 18 skipped | none |
| `eval.score` before and after | agent | done | both `found 0 of 8; decoys flagged 0 of 3` | none |

## Done when, line by line

| Roadmap line | Result |
|---|---|
| The plan check flags the Marlow pilot with its eight plan months, and clears Cedar & Pine and Brookline Row | Done. Flag, 2027-02 to 2027-09, $161,258; Cedar & Pine info (term ends after the plan; last notice day 2027-08-02 in the window); Brookline Row info (0.31% of the plan, $3,355) |
| Exclusivity, MFN and change-of-control "not stated" on Hollis Voice, each read from the contract | Done. Panel status `not_stated` for each field; one claim per contract citing every page read |
| A change-of-control test contract returns its clause with its quote | Done. Quote "3. Change of control. If the Customer is acquired ..." passes the quote checker |
| A contracts-only folder produces a result with no crash | Done, through `check()`, `scan.run` and the CLI |
| 30-day cancellation counted as a year of ARR gives a gap; one-year commitment does not | Done as a check 1 `flag` and an `info` (see Attention needed 3) |
| Every quote passes the quote checker | Done on four rooms and the test contracts; 0 unverified in the memo merge |
| The ARR and concentration entries keep their own checks and point to this one | Not touched: entries 1.2 and 1.6 are not built yet; nothing here repeats them |

## Decisions and events

- 2026-10-23: the reading is a script, not a model (no key here; Saturday owns the model reading). Recorded in [04_architecture.md](04_architecture.md).
- 2026-10-23: module names `contract_reader.py` and `contract_terms_full.py`, leaving `contract_terms.py` for Saturday. `scan.CHECKS` lists `contract_terms` first so its model reader is set before either module reads.
- 2026-10-23: check 1 built here, for the Done when's 30-day test.
- 2026-10-23: test contracts are written by a small PDF writer in the tests, so no test skips for want of reportlab.
- 2026-10-23: merged `origin/main` (`ccaa2f2`) for the verify-tricorder skill; map file written there per the coordinator's update to the shared rules.
- 2026-10-23: a defect found while running the spike. Test contracts dated after the customer's first month tripped check 4. The fixtures now date each test contract from the customer's first month, and the one-year test asserts nothing else fires.
- 2026-10-23: a defect found by reading output. An ended term with no renewal printed a negative day count; it now reads "the term ended" and flags, with a test.

## To delete at cleanup

- Nothing in the repo.
- Outside the repo, in this session's scratchpad (the OS owns `/tmp`): `/tmp/claude-0/-home-claude/46d40c2c-7610-5980-8cc8-4007978d4e75/scratchpad/contract-terms/` (spike test rooms, the verify run folder, scan outputs, `contracts_only/`).
- In the worktree, git-ignored: `readout/node_modules/` and `readout/dist/`, built by `control.sh launch`.
