# Feature progress: claim support

**Landed (closeout, 2026-10-23).** Merged to `main` in PR #8, merge commit `60c45d5`. `bin/ci-py` on `main`: 648 passed, 0 failed; GitHub CI green. Open items now live on the board ([BULLETIN.md](../../BULLETIN.md)): TRI-wave2-defaults (is the company's model a source), TRI-claim-support-followups and TRI-claim-sentences. Wave closeout: [02_closeout.md](../20261022.10_feature_breakdown/02_closeout.md). **Next:** none in this folder. The "Now" paragraph below is the state at hand-off, kept as history.

**Now.** Review fix round for [review_wave2a.md](../20261022.10_feature_breakdown/review_wave2a.md) S5 to S8, O1, O4, O5 done on `forge/claim-support` after merging `claude/project-thread-ea11in` (which lists `claim_support` in `merge.py` STEPS and brings the cohort rebuild). Counts and scores below are from the fix round; the earlier sections keep the first build's numbers as history. **Next:** the orchestrator integrates the branch.

## Review fix round (2026-10-23)

| Finding | Fix | Test |
|---|---|---|
| S5: a founder file with other columns, text in a cell, or a bad claims.json crashed the scan | every reader call guarded; a failure reads as "not found in that file" and one gap names the file and the error; malformed claims.json rows skipped and counted | `test_a_hiring_plan_with_other_columns_is_a_gap_not_a_crash`, `test_text_in_a_metrics_cell_is_a_gap_not_a_crash`, `test_a_malformed_claims_json_is_a_gap_not_a_crash` |
| S6: a flag sharing only a check name relabelled a true figure | a settling flag relabels only when both carry a Value of the same label, unit and period and the flag's figure breaks the claim's own comparison; other settling flags are named in `disagrees` ("raises a problem with this figure, not compared figure to figure") and the label stays | `test_a_flag_that_agrees_with_the_ceiling_does_not_relabel`, `test_a_flag_that_breaks_the_ceiling_relabels`, `test_a_flag_that_cannot_be_compared_is_named_but_does_not_relabel` |
| S7: model-only support read supported | the scan labels a figure only the financial model states unsupported, "only a model reading backs this"; the memo step names settling checks that have not rebuilt the figure (an info line under the name does not count) | `test_a_figure_only_the_model_states_is_unsupported_and_says_so`, `test_runway_and_burn_name_the_rebuild_that_has_not_run`; PF3 relabelled by the cohort rebuild in `test_other_scans_flags_relabel_the_pitch_claim` |
| S8: a sum or count cited one unrelated row | evidence carries the first and last row of its range; texts and table columns say how the figure was made | `test_a_sum_cites_its_range_and_says_how_it_was_made`, `test_a_count_cites_its_range_and_says_how_it_was_made` |
| O1: `corroborated_by` never fired | the rule works; on the demo rooms no other scan writes a non-flag claim with a matching Value and no pitch source (red-flag Values are `other` or restate the deck's figure) | `test_corroborated_by_names_another_scans_agreeing_claim` (hand-built pair) |
| O4: the count row appended twice | written once; the ask note too | `test_the_count_row_is_written_once` |
| O5: loose bios and contract-date matches | founder years must sit in the sentence naming the founder the pitch names; each match's how names the exact words, line and page | `scans/claims/tests/test_evidence.py` (hand-built pages) |
| Steering: "357 clinics" twice | not a duplicate claim: the readout holds one claim, `claims-057`, and the steering page renders it twice. Separately, same-figure sentences on one slide or line are now one claim (Brasswick slides 5 and 10) | `test_one_row_per_figure_per_slide_or_line` |

Counts after the fix round, from `spike/count_done_when.py` at `f98091e`:

| Room | Claims | Supported | Contradicted | Unsupported | Quote checker failures |
|---|---|---|---|---|---|
| hollis_voice | 64 | 24 | 10 | 30 | 0 |
| brasswick | 51 | 24 | 3 | 24 | 0 |
| hollis_voice_seed_drop | 64 | 18 | 6 | 40 | 0 |
| hollis_voice_clean | 64 | 31 | 0 | 33 | 0 |

Scores (`eval.score`): hollis_voice 2 of 8, brasswick 5 of 5, seed drop 1 of 8, clean 0 of 0; 0 decoys flagged in every room.

What the fix round changed against the Done when: PF3 is now contradicted (cohort rebuild, 87.3%). BF1 ($943K) and BF3 (runway 29, burn $113,684) are no longer contradicted in the claims table: their flags carry Values the claim cannot be compared with (`other`, `payroll_monthly`), so the row names the flag instead. Green flags Hollis GF2 and GF3's 17 now read unsupported, because only the model states them. The answer key counts them green; that conflict is for Ken (Attention needed 13).

Roadmap slice: [claim-support](../../ongoing/ROADMAP.md#claim-support). Diagram: [claims_workflow.md](../../ongoing/diagrams/claims_workflow.md). Route: prototype first, with an interface example printed by a spike.

## Attention needed

1. **Done in the integration branch: `claim_support` is in `scans/memo/merge.py` STEPS after `link`.** The step is `scans.memo.claim_support.apply(readout, room_dir)`. Until then, `python -m scans.memo.claim_support <room>` rewrites the readout the merge wrote. Without it, `POST /api/rooms/<room>/readout` drops the relabelling (BF1, BF2 and BF3 are credited to the red-flag engine anyway, so the score does not change).
2. **Red-flag engine owner: PF3, PF6 and PF4's runway and burn are waiting on rebuild checks.** Hollis's 102.6% NRR, 80% gross margin, 37 months of runway and $374,462 burn read supported, backed only by the model. Their ask column says so. They turn contradicted when `rebuild_cohorts_from_customer_file` (1.3), `gross_margin_from_ledger` (1.7) or `payroll_from_hiring_plan_and_rerun_cash` (1.4) flag, through `CHECK_SETTLES`. `test_a_rebuild_flag_from_a_later_check_relabels_the_model_only_figure` proves that hand-off on a hand-built flag.
3. **Captain: overlap with FRAMEWORKS 1.5 (`deck_claim_vs_named_cell`).** The claims scan already contradicts the deck's ARR, clinic count and hires against the model's named cells (PF2, PF7, PF4 hires) under the check name `claim_support`. The key credits PF2 to `deck_claim_vs_named_cell`. If 1.5 is not built by Saturday, a one-line rename in `label._check_name` scores PF2. Not done: 1.5 owns that name.
4. **Eval owner: `eval/score.py` counts a decoy as flagged on its locator alone.** Brasswick DC3 lists `pitch_deck.pdf` slide 12 (the claims page), so no flag claim may cite the claims page. The claims scan cites the content slide as the first source and lists claims-page repeats only on supported claims.
5. **Asks step owner (unbuilt).** The claims scan writes one Gap per unsupported kind with the checklist id in `would_need`. Checklist coverage already turns them into ask lines on the page, but the line is the bare `would_need` text ("signed order forms that show the list price (C34)"), not a sentence. The claims table's own `ask` column has the full sentence ("Please send signed order forms that show the list price (C34), to back: $349."). The asks step could use that.
6. **Readout page owner: no component renders Panels.** The claims table is the Panel "claims table" (columns in [02_interface_example.md](02_interface_example.md)). It needs a component in the drill-down. No component was written here, to keep `readout/` untouched.
7. **Top-flags step (unbuilt).** The page shows "No flags yet" on Hollis, though the readout holds 8 contradicted pitch figures with severity `flag`. They reach the page once a top-flags step exists.
8. **Known misses.** Brasswick slide 9's spelled-out "nine ... years" is split by the PDF's columns and missed by the script; the model reading would catch it. Brasswick's slide 4 "Revenue grew every month in 2026" reads supported, which is true for 2026 (the planted fall, BF2, is in 2025 and is caught on the chart).
9. **Not built:** extraction from the overview, the one-pager and the website (founder-group repeats; PRD question 1 for Ken). The model reading is untested live (no key here).
10. **Persona review not run.** There is no visual prototype (the route used an interface example, since nothing draws the table), and this builder has no subagent tool to run the persona agents.
11. **Environment: `/dev/null` is a regular file in this container** (48 bytes, "unalias: unsetenv: not found", modified at 02:19 and 02:32 UTC). Not caused by this builder. `control.sh` and `git` still work, but anything that reads `/dev/null` expecting it empty may misbehave.
13. **Ken: is the company's financial model a source?** The review's rule (S7) makes a figure only the model states unsupported. The answer key calls Hollis GF2 (market $252,000,000) and GF3's 17 staff green flags, backed by the model alone. Either the key or the rule changes.
14. **Red-flag owner: BF1 and BF3 need a comparable Value.** `gross_vs_net_revenue` writes label `other`, and `contractor_spend_vs_headcount_and_burn` writes `payroll_monthly`. A flag Value of the rebuilt LTM revenue (label `other` has no match) or rebuilt runway and burn (`runway_months`, `net_burn_monthly`) would let the memo step relabel the deck's figures.
15. **Steering owner:** the duplicate "357 clinics" line is one claim (`claims-057`) drawn twice on the page.
12. **Schema proposals** for the captain, after Saturday: [04_architecture.md](04_architecture.md), "Proposed schema changes".

## Documents

- [product_thinking.md](product_thinking.md): the job, evidence, assumptions, priority
- [01_brief.md](01_brief.md): short brief
- [02_interface_example.md](02_interface_example.md): the claims table and one claim per label, printed by `spike/interface_example.py`
- [03_prd.md](03_prd.md): requirements CS-R1 to CS-R15, failure cases CS-F1 to CS-F9
- [04_architecture.md](04_architecture.md): components, shapes, the memo step, alternatives, proposed schema changes
- [05_plan.md](05_plan.md): slices and the verification table
- [06_verification.md](06_verification.md): the control.sh run and what it found
- Verification map: [.claude/skills/verify-tricorder/features/claim-support.md](../../../.claude/skills/verify-tricorder/features/claim-support.md)
- `spike/`: `count_done_when.py` (reads the answer keys; eval only), `interface_example.py`
- `evidence/`: transcripts, responses, light and dark page captures, `done_when_counts.txt`

## Work and evidence

| Outcome | Owner | State | Evidence or blocker | Next action |
|---|---|---|---|---|
| Number parser | builder | done | `test_numbers.py` | none |
| Claims scan: extract, evidence map, labels, Panels, gaps | builder | done | `test_scan.py`, `test_inputs.py`, `test_read.py` | none |
| Memo step | builder | done, not listed in merge | `test_claim_support.py` | orchestrator lists it (item 1) |
| Done-when counts on every room | builder | done | `spike/count_done_when.py`, below | none |
| Verification through control.sh | builder | done | [06_verification.md](06_verification.md) | none |
| Full suite and CI | builder | done | `python3 -m pytest`: 269 passed; `bin/ci-py`: 269 passed, exit 0 | none |
| Claims table on the page | page owner | not started | item 6 | build a Panel component |

### Done-when counts

From `python3 docs/features/20261023.06_claim_support/spike/count_done_when.py <scratch>` at `727ff5b`, which runs redflags, claims, memo and the claim_support step per room. Every room is synthetic. Full output: [evidence/done_when_counts.txt](evidence/done_when_counts.txt).

| Room | Claims | From the script | Supported | Contradicted | Unsupported | Quote checker failures | Examples not counted |
|---|---|---|---|---|---|---|---|
| hollis_voice | 64 | 10 | 39 | 8 | 17 | 0 | 0 |
| brasswick | 53 | 11 | 31 | 7 | 15 | 0 | 6 |
| hollis_voice_seed_drop | 64 | 10 | 33 | 6 | 25 | 0 | 0 |
| hollis_voice_clean | 64 | 11 | 44 | 0 | 20 | 0 | 0 |

Against the roadmap's Done when:

- **Every numeric claim on every slide and in the script has a label:** done on all four rooms (`test_every_figure_line_is_covered`, `test_every_claim_has_one_label_and_one_row`).
- **Each planted contradiction contradicted with both sources:** done for PF2, PF2b, PF4 (hires 24 against 8), PF5, PF7, BF1, BF2, BF3, BF4, BF5. Not done for PF3 and PF6, nor PF4's runway and burn (item 2). PF1 touches no pitch figure.
- **Each green flag supported with its sources:** done for Hollis GF1, GF2, GF3 and Brasswick GF1, GF2, GF3 (pitch plus a document outside it: the model, the cap table, the hiring plan, the metrics export or revenue by customer).
- **Quote checker passes on every claim:** done, 0 failures on every room.

Scores (`eval.score`, after the memo step): Brasswick 5 of 5, 0 decoys; Hollis 1 of 8 (PF2b, through this scan), 0 decoys; seed drop 1 of 8, 0 decoys; clean 0 of 0, 0 decoys.

## Decisions and events

- 2026-10-23T02:06Z: worktree made from `origin/main` at `e017a69`.
- The pitch documents count as one source; a founder document that disagrees with another still contradicts, shown "(same pitch)" (PF2b, BF5).
- A figure backed only by the model reads supported, with a note naming the rebuild check that would test it.
- The memo step matches other scans' flags on pitch sources only, after a shared export row relabelled unrelated claims and flagged Brasswick decoy DC3.
- Spoken tolerance applies only to rounded or hedged speech; "eleven" against "twelve years" must not agree.
- Interface example instead of a visual prototype: nothing on the page draws Panels yet.
- 02:41Z: final verification pass; two wording fixes came out of earlier passes (`f4e276d`, `727ff5b`).
- Server for run `claim-support` stopped by its own pid with `control.sh cleanup`. Uvicorn processes before launch: 0; after cleanup: 0.

## To delete at cleanup

- `/home/claude/wt/claim-support/out/hollis_voice/claims.json`: an early scan run that wrote to the worktree's git-ignored `out/`.
- `/home/claude/wt/claim-support/readout/node_modules/` and `readout/dist/`: built by `control.sh launch` for the page (git-ignored).
- `/home/claude/wt/claim-support/docs/features/20261023.06_claim_support/02_prototype/`: an empty folder, unused on this route.
- `/tmp/tricorder-verify/claim-support/`: the run folder (out, evidence copy, logs). Under `/tmp`, so the OS owns it.
- `/tmp/claude-0/-home-claude/46d40c2c-7610-5980-8cc8-4007978d4e75/scratchpad/claim-support/`: scratch outputs.
- `__pycache__/` folders under `scans/claims/` and `scans/memo/tests/` (git-ignored).
