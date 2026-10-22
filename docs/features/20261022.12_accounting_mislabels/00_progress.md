# Feature progress: accounting mislabels

`scans/redflags/mislabels.py` is built test first and its 64 tests pass. The full suite passes: `python3 -m pytest`, 183 passed. The red-flag engine now carries the module's claims and its three panels. On Brasswick, `eval.score` finds BF1, BF3 and BF4 from this module, and no room flags a decoy. Next: the captain reviews and merges. The proposed FRAMEWORKS.md text is in [proposed_frameworks_changes.md](proposed_frameworks_changes.md).

Roadmap slice: [accounting-mislabels](../../ongoing/ROADMAP.md#accounting-mislabels). Route: prototype first, with an interface example in place of a screen.

## Attention needed

1. **The coordinator's fallback rule rests on a misreading, and the code does not follow it.** The coordinator asked that kind a's seed-drop result follow entry 1.12's "model-fallback rule": if the fallback is a model reading, it should not be a script flag, and offline with no API key it should be a gap. But "the model" in entry 1.12's fallback is the company's financial model workbook. The text reads "the `Product type` column of `ARR_Build` in the model". The fallback reads spreadsheet cells, makes no LLM call and needs no key. So the claim stays `computed`, with severity `flag`. `test_makes_no_model_call` replaces every function in `clients/llm.py` with one that fails, then runs the seed drop, and it passes. Item 4 of [proposed_frameworks_changes.md](proposed_frameworks_changes.md) proposes wording that removes the ambiguity. If the coordinator still wants the seed-drop claim downgraded to `watch`, that is a one-line change. Owner: coordinator.
2. **Entry 1.12 needs the proposed text.** The kind e plan test, vendor propagation and the kind g bridge test run in code but are not yet in FRAMEWORKS.md. Owner: whoever keeps FRAMEWORKS.md.
3. **Entry 1.2's flag must cite `ARR_Build!E13`.** The link by shared source depends on it. Nobody has built entry 1.2 yet. Owner: redflag-engine.

## Decisions settled by the coordinator

- Brasswick is an acceptance room.
- No change to `generate.py`. The resale room is a pytest fixture in `tmp_path`.
- The link to the pilot flag is the shared source `ARR_Build!E13`.
- `check()` returns a third element, `list[Panel]`. Entry 1.12's tables go there: "accounting mislabels: entry", "accounting mislabels: checks" and "accounting mislabels: lines".

## Documents

- [product_thinking.md](product_thinking.md), [01_brief.md](01_brief.md), [02_interface_example.md](02_interface_example.md) (from the spike), [03_prd.md](03_prd.md), [04_architecture.md](04_architecture.md), [05_plan.md](05_plan.md) (its evidence column now holds real results), [proposed_frameworks_changes.md](proposed_frameworks_changes.md)
- Code: `scans/redflags/mislabels.py`, `scans/redflags/tests/test_mislabels.py`
- Spike (throwaway): [spike/](spike/)

## Work and evidence

| Outcome | Owner | State | Evidence or blocker | Next action |
|---|---|---|---|---|
| Docs to Plan | agent | done | this folder, committed by the parent | none |
| Tests written first | agent | done | Run before the module existed, the file failed at collection with `ImportError: cannot import name 'mislabels'`. The red check covered the whole file, not each test. | none |
| Module | agent | done | `python3 -m pytest scans/redflags/tests/test_mislabels.py`: 64 passed in 2.60s | captain review |
| Full suite | agent | green | `python3 -m pytest`: 183 passed in 15.64s. An earlier run set aside `scans/memo/tests/test_coverage.py` (147 passed without it), while another agent's checklist module was still missing. | none |
| Engine on Hollis Voice | agent | done | `python3 -m scans.redflags data_room/hollis_voice`: "redflags: 10 claims, 4 gaps". redflags-001 is the `mrr_column_vs_subscription_rows` flag ($186,739 against $171,739, $15,000, 8.7%). Claims 002 to 006 are info tie-outs for b, e, f, g and h. Claims 007 to 010 come from deck_vs_books. | none |
| Score | agent | done | `python3 -m scans.redflags`, `python3 -m scans.memo`, `python3 -m eval.score` per room. brasswick: found 4 of 5 (BF1, BF3, BF4 from this module; BF2 from deck_vs_books), decoys flagged 0 of 3. hollis_voice: found 0 of 8, decoys 0 of 3. hollis_voice_seed_drop: found 0 of 8, decoys 0 of 3. hollis_voice_clean: found 0 of 0, decoys 0 of 3. Hollis Voice's planted flags belong to the Saturday checks, which do not exist yet. | none |
| Helper processes | agent | checked | `ps -axo command \| grep -c "[l]ahe.js serve"`: 0 before and 0 after. The tests start no process. | none |

## Decisions and events

- 2026-10-22T19:58Z: started the docs and the spike.
- 2026-10-22T20:07Z: docs written; the parent committed them.
- Coordinator decisions received (listed above). Wrote `test_mislabels.py` from the Plan's verification table, then the module.
- The first full run failed one test. The watch fixture edited the Brasswick workbook with openpyxl, which drops cached formula values, so the totals read as empty. The fix patches the parsed P&L in memory.
- Added panel tests after the framework update: `test_panels_carry_entry_checks_and_lines`, `test_seed_drop_entry_label`, `test_engine_result_holds_mislabels_claims_and_panels`.
- 2026-10-22T20:14Z: all green as above. No human approval is needed for this route; none was given.

## Not for commit

- `spike/test_rooms/` (about 960K): generated copies of the Hollis Voice room.
- `out/`: engine, memo and score results. Git already ignores it.

## To delete at cleanup

- `docs/features/20261022.12_accounting_mislabels/spike/test_rooms/`: generated copies of the Hollis Voice room, rewritten by each spike run.
- The scratch copy of the skeleton's `schema/`, `scans/base.py` and `eval/score.py` in this session's scratchpad folder. It is outside the repo.
- `out/hollis_voice/`, `out/hollis_voice_seed_drop/`, `out/hollis_voice_clean/`, `out/brasswick/`: result files from the acceptance commands. Git ignores them.
