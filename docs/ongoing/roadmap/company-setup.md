# company-setup

Start diligence on a real company before any data room exists: pick it from the YC Spring 2026 list, set it up, and kick off our own research.

- **Status today:** not started. Steps 1 and 2 of the [demo workflow](../diagrams/demo_workflow.md); Ken asked where they were on 2026-10-24 at 11:27 AM.
- **Who builds it:** agent, until someone on the team takes it.
- **Waits on:** nothing to start. The list is saved. The research it kicks off is [outside-in](outside-in.md), [founder-profiles](founder-profiles.md), [comps](comps.md) and [market-signals](market-signals.md), which need [cached-data](cached-data.md) and Ken's keys to show real results.
- **Checked against:** the list of YC Spring 2026 companies is saved at [yc_spring_2026_companies.csv](../../reports/20261022.02_research/raw/demo_companies/yc_spring_2026_companies.csv), written by [demo_yc_batch.py](../../reports/20261022.02_research/demo_yc_batch.py) from YC's public directory. Nothing in the app reads it; the app starts from a room, not a company.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

Ken, 11:15 AM: "we want to start with a real list of YC spring 26 companies and kick off our due diligence. we run our own models and do internet reserach." 11:27 AM: "where is the stuff on the initial setup of the company and running our first bits of diligence before the data room?"

### Includes

- The operator opens Tricorder on the list of YC Spring 2026 companies: name, one-line pitch, website, industry, team size, from the saved CSV.
- Picking a company sets it up: its record holds the name, the website, the founders and the batch, and it is saved in the store like a readout ([readout-store](readout-store.md)).
- Setting it up kicks off the research that needs no data room, at once: the outside world ([outside-in](outside-in.md)), the founders ([founder-profiles](founder-profiles.md)), comparable companies ([comps](comps.md)) and market signals ([market-signals](market-signals.md)).
- The first readout is ready before any room: what the outside world says, with every claim sourced, and the gaps only a data room can fill.
- Those gaps feed the first data-room request ([room-requests](room-requests.md)), so the associate's first ask is already drafted.
- Each real company's data room for the demo is synthetic, made by [yc-rooms](yc-rooms.md), and every page says so.

### Done when

- On the demo laptop, the operator picks one of Ken's chosen companies from the list, and its first readout appears with outside-world claims, each with its source.
- The same run works with the network off, from [cached-data](cached-data.md).
- The readout's gaps show up as checked items in room-requests.

**Judgment:** yes. It is the demo's first screen.
