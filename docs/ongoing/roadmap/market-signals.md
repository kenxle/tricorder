# market-signals

Hiring, traffic, reviews, news and pricing for the demo company's real competitors, and the live outside-world run on one approved real company.

- **Status today:** not started. Left: the market-signals panel and its live run.
- **Who builds it:** Benjamin (Ken, 11:33 AM), from the [brief](../../features/20261024.01_pre_room_diligence/00_brief.md).
- **Waits on:** signals-readings (this week's `cache/signals/signals.json`); yc-rooms and cached-data, for the approved real company's saved calls.
- **Horizon:** Saturday
- **Checked against:** no scans/signals/.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

Hiring, traffic, reviews, news and pricing for the demo company's real competitors, and the live outside-world run on one approved real company. Fifth in the feasibility research's ranking. For Hollis Voice it is a static panel of this week's cached competitor readings, because live signals cannot show much for a company with no outside footprint ([critique_buildability.md](../../features/20261022.01_hackathon_plan/critique_buildability.md), finding 9). Backend-and-data's freed hours go to the readers and the video.

**The live run on a real company** ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:49 PM block). For the approved real company the demo uses, the panel sends this week's saved calls for that company again, live on stage. It uses only the sources that need no paid plan: the company's website, Hacker News, Apple's App Store lookup and SEC EDGAR. It takes this slice's slot, so Saturday's hours do not change. Any call that fails or is slow shows this week's saved copy from [cached-data](cached-data.md), with its date. The full live scan, with resolution and every tab, is [outside-in](outside-in.md), which an agent builds before Saturday and which joins this panel on Saturday.

**Waits on:** signals-readings (this week's `cache/signals/signals.json`); yc-rooms and cached-data, for the approved real company's saved calls.

**Includes:**

- The signals panel in the readout page, reading `cache/signals/signals.json` through the server.
- Each reading shows the date it was taken, and each number links to its saved source.
- On the approved real company's readout, a live re-run of its saved calls. Each fresh answer is saved beside the old copy and shown with the time it was read. The panel carries the room's synthetic label.

**Done when:** the panel shows at least three competitors on the readout page, and every number's link opens its saved copy. On the approved real company, the live re-run shows each source with the time it was read, and with the network off it shows this week's saved copies with their dates.

**Who:** frontend.

**Hours:** 0.25 (inside the 2:30 to 3:30 PM polish hour).

**Judgment:** no.
