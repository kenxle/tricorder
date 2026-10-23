# Product thinking: accounting mislabels

## User job

The associate who prepares the memo opens a data room and has to find out whether each headline number is what its label says. A number filed under a label it does not earn is the most common way a deck says more than the books support ([PRODUCT_BRIEF.md](../../ongoing/PRODUCT_BRIEF.md), "The problem"). Today they rebuild MRR, revenue and burn by hand from the customer file and the ledger, or they skip it. The partner who reads the memo wants to see, for each flagged number, the number claimed, the number recomputed and where both sit.

Ken asked for this by name. On the "ARR that is not recurring" finding he wrote: "this is good. we should look for this specifically, but also any other accounting mislabeling" ([writers' brief](../20261022.01_hackathon_plan/00_brief_for_writers.md), 1:32 PM block). Ken is quoting himself in a project document, so the brief line is the link.

## Evidence and assumptions

Observed, from the spike ([02_interface_example.md](02_interface_example.md), [spike/spike_run.txt](spike/spike_run.txt)):

- On Hollis Voice, one sub-check fires: the Marlow pilot's $15,000 sits in the `mrr` column. The other five that can run return clear, and both decoys stay clear.
- On Brasswick, the second demo room, four sub-checks fire, and they catch three of its five planted flags (BF1, BF3, BF4). Those three are keyed to entry 1.12's check names in `data_room/answer_key_brasswick.json`. The scoring rule in the skeleton's `eval/score.py` counts all three as found and no decoy as flagged ([spike/score_run.txt](spike/score_run.txt)).
- On the clean room nothing fires.

Assumptions that could change the plan:

- That Brasswick is a valid acceptance room for this slice. The roadmap slice names only Hollis Voice and a generated test room. If Ken wants Hollis Voice only, kinds c, e and g lose their only real flag.
- That one cause shown twice is acceptable on the readout. The pilot shows in entry 1.2 (ARR) and here (MRR). Brasswick's Ostley invoice fires both kind b and kind g. The readout has to group them, or the associate sees three flags for one fact.
- That a clear sub-check should write an info claim. The spike does, so the readout can show "checked, clear" with a source. Entry 1.12 says a claim on a decoy is a false positive; an info claim on the tie-out is not about the decoy, but a reviewer could read it that way.

## Priority

Wave 1 of the [feature breakdown](../20261022.10_feature_breakdown/00_breakdown.md) runs this beside deck-vs-books and checklist-coverage. It joins the Saturday redflag-engine, which has 3.0 hours for seven checks and cannot absorb six more ([ROADMAP.md](../../ongoing/ROADMAP.md), redflag-engine). Building it now is the only way these kinds are on stage. It also unblocks the contract-terms-saturday slice, whose Done when expects Ostley Freight to show "as one cause with the annual prepayment flag from entry 1.12 (BF4)" ([ROADMAP.md](../../ongoing/ROADMAP.md), contract-terms-saturday).

What it displaces: little. It is scripts only, with no model call and no key, in one module.

## Options

- **Do nothing.** The engine shows kinds a (ARR side) and d on Saturday. Brasswick's three mislabel flags are then caught by nothing, and the Brasswick readout shows two of five flags.
- **Fold the six checks into the engine's Saturday hours.** Rejected by the roadmap: the hours are spent.
- **Build them here as one module, scripts only.** Recommended.
- **Add a model reading now.** Entry 1.12 has a prompt. It is not needed to catch any planted flag, and the engine is scripts only on Saturday. Deferred.

## Recommendation

Build `scans/redflags/mislabels.py` with the seven sub-checks (six plus kind c), test first, against Hollis Voice, its seed drop, the clean room, Brasswick and a resale test room written at test time. Raise three things with the coordinator: Brasswick as an acceptance room, the kind e formula change that BF3 needs, and how the readout groups one cause shown by two checks. See [00_progress.md](00_progress.md), "Attention needed".
