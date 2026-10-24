# signals-readings

This week's saved competitor readings, written as the market-signals panel's data, so Saturday only shows them.

- **Status today:** not started. Left: the saved signal readings.
- **Who builds it:** agent.
- **Waits on:** cached-data, saturday-specs (the signals schema), skeleton (the Claim schema).
- **Horizon:** Now to Friday night
- **Checked against:** no cache/signals/.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

This week's saved competitor readings, written as the market-signals panel's data, so Saturday only shows them. Live market signals cannot show much: the demo company has no outside footprint, Akta's pay-as-you-go plan returns 403 on hiring, traffic and reviews, and with one reading taken this week every signal is labelled `one_reading` ([critique_buildability.md](../../features/20261022.01_hackathon_plan/critique_buildability.md), finding 9).

**Waits on:** cached-data, saturday-specs (the signals schema), skeleton (the Claim schema).

**Includes:**

- `cache/signals/signals.json` in the Claim schema: a short grid per competitor from the cached Akta pulls and Tavily pricing pages, each number linked to its saved source through `cache/index.json` (feasibility 1.3).
- For Hollis Voice itself, only what the room gives: website copy and pricing.
- For the approved real company the demo uses, its own readings from this week's saved calls, shown as the fallback for Saturday's live run.
- The date each reading was taken, shown on the panel.
- If Akta's paid signals were not available, the grid shows news and company data only, and the gap says why.

**Done when:** the file validates against the Claim schema, the grid covers at least three competitors, and every number's source opens from `cache/index.json`.

**Who:** agent, with Ken for anything behind his keys.

**Judgment:** no.
