# reader-scenarios

Each reader of the memo gets their own copy to steer, and can try what-if changes on the financial model ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:01 PM block).

- **Status today:** not started. Left: each memo reader gets their own copy to steer and can try what-ifs on the financial model.
- **Who builds it:** agent.
- **Waits on:** [memo-export](memo-export.md); [steering](steering.md); [financial-model](financial-model.md), whose scripts do the recomputing.
- **Horizon:** Now to Friday night
- **Checked against:** no scenarios code in memo/.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

Each reader of the memo gets their own copy to steer, and can try what-if changes on the financial model ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:01 PM block). The operator's memo is the shared version. A partner's changes stay in the partner's copy.

**Waits on:** [memo-export](memo-export.md); [steering](steering.md); [financial-model](financial-model.md), whose scripts do the recomputing.

**Includes:**

- A shared memo version, and one copy per reader laid over it. A reader steers their copy (rewrite a section, ask for more information) by the same rules as [steering](steering.md), without changing anyone else's.
- Each copy says what the reader changed and which shared version it started from.
- What-if inputs on the model: a reader changes a few assumptions, such as churn, price, hiring pace, or the pilot counted or not, and sees what the numbers become.
- The same scripts recompute from the company's own model and rows. The source files never change.
- Every tweaked number is marked as the reader's scenario, shown beside the company's figure and Tricorder's rebuilt figure, so nobody mistakes a what-if for a fact.

**Done when:**

- Two readers steer their own copies of the Hollis Voice memo differently. Each sees only their own changes, and the shared version is unchanged.
- A reader who sets "pilot not counted" sees ARR recomputed by the script, marked as their scenario, beside the company's figure and the rebuilt figure.
- After any scenario, the room's files are byte for byte the same as before.
- A new shared version shows each reader which version their copy started from.

**Who:** agent.

**Judgment:** yes.
