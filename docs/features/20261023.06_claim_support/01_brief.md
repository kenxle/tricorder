# Brief: claim support

**Users.** The associate who works a data room, and the partner who reads its top flags. See [product_thinking.md](product_thinking.md).

**Context.** Roadmap slice [claim-support](../../ongoing/ROADMAP.md#claim-support), diagram [claims_workflow.md](../../ongoing/diagrams/claims_workflow.md). Built before Saturday, so the readout's drill-down has a full claims table on the day.

**Problem.** A pitch makes about sixty checkable statements. Nobody checks them all by hand, and the ones left out are where the plants hide: a spoken ARR above the deck, a ceiling on customer share that one customer breaks, a hiring count three times the model's.

**Outcome.** For every figure on every slide and in every script sentence, one row: where it is, the exact words, what it means once normalised (unit, period, definition, spoken and rounded or not), which documents should back it, which do, which disagree, and a label:

- **supported**: a document outside the pitch agrees;
- **contradicted**: a document disagrees, and both sides are shown;
- **unsupported**: nothing outside the pitch states it, written as a gap with an ask line.

The memo step then relabels a figure that another scan has flagged (a rebuild of revenue, burn or the chart's history), so the table and the top flags agree.

**Constraints.**

- Script first; the model reading through `clients/llm.py` is optional and becomes a gap without a key.
- No schema change. The table is a Panel; each label is a Claim with the existing fields.
- Do not edit `scans/memo/merge.py`; the memo step is its own module and the orchestrator lists it.
- The deck, video, overview, website and one-pager are one source.

**Questions that shaped the interface example.**

1. Does the table need its own model, or do Claims plus a Panel carry it? Settled: Claims plus a Panel, with a schema proposal for later ([04_architecture.md](04_architecture.md)).
2. Should a figure that only the financial model backs read supported? Settled: yes, with a note in its ask column naming the rebuild check that would test it, until that check exists.

**Prototype.** A nonvisual route: [02_interface_example.md](02_interface_example.md), printed by `spike/interface_example.py` from the real rooms. No page component renders Panels yet, so there is nothing on screen to prototype; see "Attention needed" in [00_progress.md](00_progress.md).
