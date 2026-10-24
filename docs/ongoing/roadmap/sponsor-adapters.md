# sponsor-adapters

The sponsor tools in the product, with keys that only arrive on the day ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:56 PM block).

- **Status today:** not started. Left: one adapter per sponsor (Akta, Crunchbase, Nicrron), keys arrive today.
- **Who builds it:** agent.
- **Waits on:** nothing this week; the keys on Saturday morning.
- **Horizon:** Now to Friday night
- **Checked against:** clients/ holds only llm.py.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The sponsor tools in the product, with keys that only arrive on the day ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:56 PM block). Ken: "let's make sure that these are in our roadmap and features. we won't get access to them until day of but we can do the other stuff ahead of time." The landscape research names three as most useful on Saturday: Akta (signals, company data and news, with source metadata on every response), Crunchbase (comps and funding data through its MCP), and the Nicrron gateway (one key for every model, with free repeat requests) ([research_landscape.md](../../reports/20261022.02_research/research_landscape.md), Part 2).

**Waits on:** nothing this week; the keys on Saturday morning.

**Includes, before Saturday (no keys needed):**

- One small adapter per sponsor, written against its published docs (saved under the feasibility and landscape research's raw folders): the request it makes, the response it expects, and how each response field becomes a Claim with its source.
- A recorded sample response per adapter, shaped from the docs, so tests and the demo can run with no key and no network.
- A switch per adapter: off, sample, or live. Every scan works with all three off, using the free sources (Tavily, You.com, GitHub, EDGAR, Hacker News) and this week's cache.
- For Nicrron: model calls go through one client, so pointing it at the gateway is a setting, not a code change.

**Includes, Saturday 9:00 to 10:30 (captain, during breakfast and team formation, inside the existing window):**

- Paste the keys into each laptop's `.env`, flip each adapter to live, run one call each, and keep sample mode for any that fails.
- On stage, say which sponsor tool each panel used.

**Done when:** every adapter passes its tests in sample mode this week; on Saturday each one is live or falls back to sample mode without a code change.

**Who:** agent this week; captain on Saturday morning.

**Judgment:** no.
