# Feature progress: claim support

**Now.** Built and verified on branch `forge/claim-support` (2026-10-23). The claims scan (`scans/claims/`) labels every pitch figure on all four rooms, and the memo step (`scans/memo/claim_support.py`) relabels claims against other scans' flags. The full suite passes (269 passed, 0 failed) and `bin/ci-py` is green. The verification run through `control.sh` is in [06_verification.md](06_verification.md), with its evidence in `evidence/`. **Next:** the orchestrator lists the step in `merge.py` (item 1 below) and integrates the branch.

Roadmap slice: [claim-support](../../ongoing/ROADMAP.md#claim-support). Diagram: [claims_workflow.md](../../ongoing/diagrams/claims_workflow.md). Route: prototype first, with an interface example printed by a spike.

## Attention needed

1. **Orchestrator: add `claim_support` to `scans/memo/merge.py` STEPS, after `link` and before `pieces`.** The step is `scans.memo.claim_support.apply(readout, room_dir)`. Until then, `python -m scans.memo.claim_support <room>` rewrites the readout the merge wrote. Without it, `POST /api/rooms/<room>/readout` drops the relabelling (BF1, BF2 and BF3 are credited to the red-flag engine anyway, so the score does not change).
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
