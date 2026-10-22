# Feature progress: accounting mislabels

The brief, interface example, PRD, architecture and Plan are written, and a spike has run every sub-check on six rooms. Next: the builder takes slice S1 in [05_plan.md](05_plan.md) once the skeleton is on `main`. Three questions below need the coordinator before the module lands.

Roadmap slice: [accounting-mislabels](../../ongoing/ROADMAP.md#accounting-mislabels). Route: prototype first, with an interface example in place of a screen.

## Attention needed

1. **Brasswick holds real data for kinds c, e and g.** The slice and entry 1.12 say kind c has nothing to run on and name only Hollis Voice. But `data_room/answer_key_brasswick.json` keys BF1 to `gross_vs_net_revenue`, BF3 to `contractor_spend_vs_headcount_and_burn` and BF4 to `deferred_revenue_vs_earned`. The contract-terms-saturday slice also expects BF4 from entry 1.12. Recommended: make Brasswick an acceptance room (PRD AM-R29). Owner: coordinator, then Ken.
2. **Entry 1.12's kind e formula does not catch BF3.** Brasswick's contractors are inside the actual P&L, so the tie test is clear; they drop out only in the plan. Entry 1.12's keyword list also misses Norrgate Software Studio ("Contract engineering, SOW 1"). The spike adds a plan test and vendor propagation (AM-R16, AM-R18), and a bridge test for kind g (AM-R24). FRAMEWORKS.md entry 1.12 should say so. Owner: whoever keeps FRAMEWORKS.md.
3. **The resale generator option may not be needed in `generate.py`.** A pytest fixture can write the test room into a temporary folder, and Brasswick gives kind c a real room. The option is designed in [04_architecture.md](04_architecture.md) in case it is wanted. Owner: coordinator.
4. **Kind a fires on the seed drop.** Entry 1.12's fallback reads the model's `ARR_Build`, which is in the seed drop, so the pilot shows there too. The answer key marks PF1 not catchable from the seed drop, but that field is about entry 1.2's check, and `eval.score` does not count this claim for PF1. Confirm this is wanted. Owner: coordinator.
5. **The skeleton's contract returns only claims and gaps.** Entry 1.12's `checks` and `lines` tables, and a link field, have nowhere to go. The PRD uses a shared source as the link (D3 in the architecture). This is the one place the module split fights the PRD. Owner: redflag-engine, after Saturday.

## Documents

- [product_thinking.md](product_thinking.md): job, evidence, priority, options
- [01_brief.md](01_brief.md): short brief
- [02_interface_example.md](02_interface_example.md): the Claim JSON the spike emitted, rendered by [spike/render_example.py](spike/render_example.py)
- [03_prd.md](03_prd.md): requirements AM-R1 to AM-R30, failure cases, open questions
- [04_architecture.md](04_architecture.md): skeleton names confirmed from commit 573567f, data shapes, decisions, alternatives, generator design
- [05_plan.md](05_plan.md): slices, throughput checkpoint, verification table
- [spike/](spike/): `mislabels_spike.py`, `score_spike.py`, `render_example.py`, and their outputs `spike_run.txt`, `score_run.txt`, `out/*.json`

## Work and evidence

| Outcome | Owner | State | Evidence or blocker | Next action |
|---|---|---|---|---|
| Docs to Plan | agent | done | this folder | coordinator reads Attention needed |
| Spike on six rooms | agent | done | [spike/spike_run.txt](spike/spike_run.txt): Hollis Voice flag (kind a only); seed drop flag (a) with five cannot_check; clean room clear; resale off: c not_run; resale on: c flags; Brasswick: b, c, e, g flag | none |
| Spike claims validate | agent | done | FRAMEWORKS 1.12 JSON Schema, skeleton `schema.claim` models and `schema.check_quotes.check_claim`: "validation: ok" for all six rooms | none |
| Spike score | agent | done | [spike/score_run.txt](spike/score_run.txt), with the skeleton's `eval.score.score`: Brasswick 3 of 5 found (BF1, BF3, BF4), 0 of 3 decoys; Hollis rooms 0 of 3 decoys | none |
| Module, test first | builder | not started | waits on the skeleton on `main` | S1 in [05_plan.md](05_plan.md) |

Verification rows live in [05_plan.md](05_plan.md), "Verification".

## Decisions and events

- 2026-10-22T19:58Z: started. Read the slice, entry 1.12, the rooms and the answer keys.
- 2026-10-22, during the spike: the coordinator relayed the skeleton's names (`check(room, ids)`, `scans.base.Ids`, `schema.settings.load()`, `eval.score`). The architecture uses them as confirmed, read from `origin/claude/project-thread-ce34ga` at 573567f.
- Spike run 1 flagged Brasswick DC1 through the bridge-deferred claim. Changed that claim to info when a P&L flag already fired (AM-R24).
- Spike run 2 cited a Brookline Row resale row in the resale room's kind a claim. Changed kind a to cite the largest row per product type.
- Decided to cite the pilot's `ARR_Build` row in the kind a claim, so it shares a source with entry 1.2's flag (D3).
- 2026-10-22T20:07Z: docs written. No human approval is needed for this route; none was given.

## Not for commit

`spike/test_rooms/` (about 960K) holds two copies of the Hollis Voice room that the spike regenerates on every run. The parent may want to leave it out of the commit. It is generated; nothing reads it but the spike.

## To delete at cleanup

- `docs/features/20261022.12_accounting_mislabels/spike/test_rooms/`: generated copies of the Hollis Voice room, rewritten by each spike run.
- The scratch copy of the skeleton's `schema/`, `scans/base.py` and `eval/score.py` in this session's scratchpad folder. It is outside the repo.
