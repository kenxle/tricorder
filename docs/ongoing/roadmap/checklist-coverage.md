# checklist-coverage

The readout's coverage against the [checklist](checklist.md), and an ask list that draws on it ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:56 PM block).

- **Status today:** partly built. Left: the coverage panel on the readout page, the register of the guides' proposed checks.
- **Who builds it:** agent.
- **Waits on:** checklist; saturday-specs (the example readout files).
- **Horizon:** Now to Friday night
- **Checked against:** merged in PR #4, board task TRI-coverage-panel (finish the panel and register) is open.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The readout's coverage against the [checklist](checklist.md), and an ask list that draws on it ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:56 PM block). An agent builds it before Saturday, outside the captain's readout hours and the frontend's page hours. The rules are "Checklist coverage" in [FRAMEWORKS.md](../FRAMEWORKS.md).

**Waits on:** checklist; saturday-specs (the example readout files).

**Joins on Saturday:** [readout](readout.md) (the ask list) and [readout-page](readout-page.md) (the coverage panel).

**Includes:**

- For each checklist item expected at the company's stage: found, checked or missing, with the scan that checked it and the piece it feeds.
- The ask list also draws on the checklist. Every item expected at the company's stage and missing from the room becomes a request, beside the lines from gaps and weak pieces. An item expected only at a later stage is not asked for.
- The company's stage comes from the deck's round slide, and the operator can change it.
- A coverage panel on the readout page.
- The reference guides' proposed checks, one guide per data-room document ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:38 PM block). Each proposed check becomes a check, or is marked as left to the operator, and each guide's missing-document line becomes its ask.
- Entry 1.10's model reading: the notes on the cap table, with each instrument and grant matched to its document (checklist row C82).
- Entry 1.11's asks, which no Saturday slice runs: bank statements, accountant-prepared statements, tax returns, IP assignments and customer references when the room lacks them, and one walk-through ask per flag ([FRAMEWORKS.md](../FRAMEWORKS.md), entry 1.11).

**Done when:**

- On the seed drop at Series A, coverage lists every checklist item as found, checked or missing, and the counts come from a script.
- Every missing Series A item becomes one ask-list line. Set to pre-seed, the same room asks for no item expected only later.
- No request appears twice when a gap and a checklist item name the same thing.

**Who:** agent.

**Judgment:** yes.

**Status:** done for every Done when check. Merged in PR #4 on 2026-10-23. The code is `scans/memo/coverage.py` and `scans/memo/checklist.py`. Besides found, checked and missing, coverage marks an item `not_checked` (no check has run yet) or `not_expected` (not expected at the stage). Two Includes items are still open on the board row TRI-coverage-panel: the coverage panel on the readout page, and the register of the guides' proposed checks. Feature folder: [20261022.13_checklist_coverage](../../features/20261022.13_checklist_coverage/00_progress.md).
