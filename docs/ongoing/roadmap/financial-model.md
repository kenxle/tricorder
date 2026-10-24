# financial-model

The financial modeling Ken asked for in the 10:10 AM dictation.

- **Status today:** not started. Left: Tricorder's own rebuilt model the operator can work in.
- **Who builds it:** agent.
- **Waits on:** data-room; saturday-specs (the check list and entries 1.3 and 1.9); [readout-store](readout-store.md).
- **Horizon:** Now to Friday night
- **Checked against:** no model scan in scans/.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The financial modeling Ken asked for in the 10:10 AM dictation. Saturday's [redflag-engine](redflag-engine.md) rebuilds the numbers it checks: burn against the hiring plan, deck against the model, retention and gross margin. This slice adds a rebuilt model the operator can work in.

**Waits on:** data-room; saturday-specs (the check list and entries 1.3 and 1.9); [readout-store](readout-store.md).

**Joins on Saturday:** [redflag-engine](redflag-engine.md), whose rebuilt numbers sit beside the full model.

**Includes:**

- **Tricorder's own version of the model**, built from the raw data the way a Series A lead does ("a lead builds their own model from your raw data", [the data-room research](../../reports/20261022.02_research/research_data_room.md), 1.3; Ken at 2:40 PM: "i was already planning on building our own versions of models"). The room's revenue, cost and headcount rows go into one monthly table with burn, cash and runway, and each cell links to the row it came from.
- **Side by side with the company's model.** Every line of the company's model sits beside Tricorder's rebuilt line, and a difference beyond the match tolerance becomes a disagreement claim in the right piece.
- Unit economics recomputed from the room's rows, by [FRAMEWORKS.md](../FRAMEWORKS.md) entry 1.9.
- The model's reading of the cohort tab's note, with the prompt in entry 1.3. Saturday keeps the script rebuild of the cohorts; this reading moved here to make room for contract terms on Saturday. It is a claim that quotes the note and never decides a number is wrong.
- The operator can change one assumption, such as a hire's start month or a churn rate, and see runway move. The script's own figure stays on screen beside it, and the operator's case is marked as theirs.
- Market size, bottom-up, stays in [frameworks-scan](frameworks-scan.md) (entry 5.6).

**Done when:**

- On the full room, the rebuilt runway with all planned hires matches the answer key's figure, and every cell opens its source row.
- Each unit-economics figure returns a claim with its sources. A figure the room cannot support is a gap.
- Changing a hire's start month moves runway, and the script's figure still shows beside it.

**Who:** agent.

**Judgment:** yes.
