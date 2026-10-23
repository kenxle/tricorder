# Product thinking: steering in one sentence

Roadmap slice: [steering](../../ongoing/ROADMAP.md#steering). Brief: [01_brief.md](01_brief.md).

## User job

- **Who.** The operator working in the readout. Usually the associate who prepares the memo. At some funds it is the partner, who runs diligence alone ([PERSONAS.md](../../ongoing/PERSONAS.md), "The partner who finds the disagreement too late", Do: "our partners run diligence themselves without handing it to junior staff").
- **Trigger.** A line in the readout looks wrong, thin or framed badly. The operator knows something the scans did not read: the pilot is not recurring revenue, or the full room has arrived.
- **What they want.** Say it once, in their own words, on that line, and see the line change in place, with what changed and why.
- **What they do today.** Edit a memo by hand, or rerun a spreadsheet. Nothing ties the edit back to the sources.

## Evidence

- Ken's 1:12 PM and 1:15 PM blocks: a comment or instruction on a piece rewrites it or gets more info ([ROADMAP.md](../../ongoing/ROADMAP.md#steering)).
- Ken's 2:21 PM edit to the product brief: one plain sentence, no setup, no menus, the answer on that line.
- The partner persona's proof is the pilot counted as ARR (PF1 in `data_room/answer_key.json`). "Treat the pilot as non-recurring" is the sentence a partner who distrusts ARR would type.
- The full room catches entries the seed drop cannot (PERSONAS.md, Series A stage). "Read the full room" is the sentence an associate types when tier two arrives.

## What the code holds today (observed, 2026-10-23)

- The merge's `pieces` and `top_flags` steps are not built on any branch (`scans/memo/` holds `merge.py`, `checklist.py`, `coverage.py`). A readout has no piece verdicts yet. Steering needs a verdict before and after, so it must supply the FRAMEWORKS "Piece verdicts" rule itself until the readout slice lands, and use the merge's step as soon as it exists.
- No built check feeds the retention piece. Entry 1.3 (`cohorts` in `scans/redflags/scan.py`'s list) is not written. Without it "read the full room" on retention adds nothing.
- The only built scan is `redflags` (entries 1.12 and 1.14). It has no model readings, so "pass the instruction to their model readings" has nowhere to go yet.

## Assumptions that could change the plan

- A1. A definition steer ("treat the pilot as non-recurring") may produce a new figure if a script computes it from the room's own cells, and the check's own number stays beside it. This reads FEATURES.md "A steer changes the reading, not the numbers" as: what is read can change, a script's number never changes because someone asked. Open for Ken.
- A2. The script half of entry 1.3 is small enough to write here, so the retention Done-when can run. The model half (reading the cohort note) waits for its owner.
- A3. With no model key, wording rules can tell a rewrite from a more-info request and spot a number request well enough for the demo sentences. A model reading through `clients/llm.py` does it better when a key is set.

## Priority

The demo's overview card asks whether one steer runs live. Steering also unblocks reader-scenarios and the outside tabs' "get more info" steers (ROADMAP waits-on lines). Doing nothing leaves the readout read-only on Saturday.

## Recommendation

Build the steer as a server route that takes one sentence, a piece and an optional line, with a deterministic path that needs no key and a model path behind `clients/llm.py`. Rebuild verdicts by the FRAMEWORKS rule, keep every revision in the readout and in the store, and show the revised line in place with a diff. Flag the two stand-ins (verdicts, the 1.3 script half) for their owners.
