# yc-rooms

Synthetic data rooms for real YC companies, so the outside-world scan runs live on a real public footprint while the room's documents are invented ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:44 PM, 2:46 PM and 2:49 PM blocks).

- **Status today:** waiting on Ken. Left: Ken picks the real YC companies, then an agent generates their synthetic rooms.
- **Who builds it:** agent after Ken.
- **Waits on:** data-room; Ken approves the list of companies on the overview page's card for the demo company.
- **Horizon:** Now to Friday night
- **Checked against:** data_room/generate.py offers only hollis and brasswick.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

Synthetic data rooms for real YC companies, so the outside-world scan runs live on a real public footprint while the room's documents are invented ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:44 PM, 2:46 PM and 2:49 PM blocks). Ken at 2:49 PM: "we want to have a list of YC companies and we'll pair them with fake data rooms and run live demos on them". The demo pairs one of these with Hollis Voice, the controlled room whose planted flags are known.

**Waits on:** data-room; Ken approves the list of companies on the overview page's card for the demo company.

**Includes:**

- **The candidate list.** Two or three real YC companies from the spring 2026 batch, proposed by a research agent, each with its public footprint: website, Hacker News, App Store, SEC filings and any announced round, saved with links. Ken picks. No room is generated before he does.
- **A profile per approved company,** built only from public pages: name, product, the founders' public bios and any announced round, each saved with its link.
- **A room per approved company,** written by this week's generator with the profile swapped in. The numbers are invented and plausible, anchored only to what the company has published. This is the first piece of [room-templates](room-templates.md): the profile swap.
- **The safeguard.** An invented room under a real company's name must never read as a claim about that company. Every page and sheet carries "Synthetic test document. Not this company's data." Planted problems are named test plants in the answer key and on screen, and the demo says so out loud.
- An answer key per room, outside the room folder, as for Hollis Voice.
- A pitch script per room, which Ken reads flatly ([record-pitch-video](record-pitch-video.md)).
- The company's outside-world calls saved this week by [cached-data](cached-data.md), so Saturday's live run has a fallback.

**Done when:** each approved company has a room that passes `data_room/check.py` against its own key; a script finds the synthetic label on every page and sheet of every real-company room; and every public fact in each profile opens its saved page.

**Who:** agent, after Ken approves the list.

**Judgment:** yes.
