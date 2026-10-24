# claim-support

The claims workflow in full ([diagrams/claims_workflow.md](../diagrams/claims_workflow.md); [writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:41 PM block): every claim in the deck and the pitch video, checked against every other document and the outside world.

- **Status today:** partly built. Left: Ken's call on figures only the company's model states, the video transcript waits on the recorded video.
- **Who builds it:** agent.
- **Waits on:** [checklist-coverage](checklist-coverage.md) for where each claim's evidence should live; record-pitch-video (the saved transcript); saturday-specs (the claim prompts).
- **Horizon:** Now to Friday night
- **Checked against:** merged in PR #8, scans/claims/ exists.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The claims workflow in full ([diagrams/claims_workflow.md](../diagrams/claims_workflow.md); [writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:41 PM block): every claim in the deck and the pitch video, checked against every other document and the outside world. Saturday does this for the deck's appendix claims and the video's transcript against the model and the revenue rows; this slice widens it.

**Waits on:** [checklist-coverage](checklist-coverage.md) for where each claim's evidence should live; record-pitch-video (the saved transcript); saturday-specs (the claim prompts).

**Joins on Saturday:** [readout](readout.md) and [pitch-video](pitch-video.md).

**Includes:**

- Claim extraction from every slide (text, charts, the appendix) and every transcript sentence with a number or a checkable fact, each with its slide and position or video second and the quoted span.
- Normalising each claim to one unit, period and definition, with spoken figures marked as spoken and rounded.
- An evidence map per claim kind (from the checklist and the document guides) saying which documents and outside sources should support it.
- A label per claim: supported (two independent sources agree), contradicted (a source disagrees, both shown), or unsupported (a gap with an ask-list line).
- A claims table in the readout's drill-down: every claim, its label, and its sources.

**Done when:** on both demo rooms, every numeric claim on every slide and in the video script has a label; each planted contradiction is labelled contradicted with both sources; each green flag's claim is labelled supported with its two sources; and the quote checker passes on every claim.

**Who:** agent.

**Judgment:** yes.

**Status:** built and merged in PR #8 on 2026-10-23. The code is `scans/claims/` and the merge step `scans/memo/claim_support.py`. In all four rooms every figure in the deck and the pitch script is labelled and every claim passes the quote checker. One Done when line is open: Hollis Voice GF2 ($252,000,000 market) and GF3's 17 staff read unsupported, because only the financial model states them. Whether the company's own model counts as support is for Ken (board row TRI-wave2-defaults). The video's transcript waits on the recorded pitch video. Feature folder: [20261023.06_claim_support](../../features/20261023.06_claim_support/00_progress.md).
