# room-templates

Templated data rooms with hidden issues ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:46 PM block).

- **Status today:** not started. Left: templated data rooms: swap a company profile in on the fly.
- **Who builds it:** agent.
- **Waits on:** data-room (Hollis Voice and the second invented company) and yc-rooms (the rooms for real companies) merged.
- **Horizon:** Now to Friday night
- **Checked against:** data_room/generate.py --company takes only hollis or brasswick.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

Templated data rooms with hidden issues ([writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:46 PM block). Ken: "we should actually set up a few different data rooms that will allow us to highlight different problems. the data rooms will need to be a little bit templated, so we can swap in new names on the fly, but we should make data rooms with hidden isseus in them, based on the problems we saw in the reserach." This week's generator already writes Hollis Voice, a second invented company, a clean room and a sealed variant, and [yc-rooms](yc-rooms.md) swaps a real company's public profile into it. This slice turns it into a template engine.

**Waits on:** data-room (Hollis Voice and the second invented company) and yc-rooms (the rooms for real companies) merged.

**Includes:**

- **A company profile swapped in on the fly:** name, sector, product, stage, founders, round, and for a real company its public facts with their links. One command writes a full room from a profile.
- **A library of hidden issues**, one plant per problem the research found: ARR that is not recurring, hidden cohort churn, burn out of line with the hiring plan, deck against model, deck revenue against the P&L and partial history, customer concentration, gross margin that leaves out costs, a vanity count, billings or deferred revenue shown as revenue, contractors left out of burn, contract terms that undercut how revenue is counted, cap-table problems. Each plant names the research it comes from, where it lives in the room, and the check that should catch it.
- **Green flags and decoys** chosen the same way, so every room has real strengths and traps, not only problems.
- **A room recipe:** a profile plus a set of plants, green flags and decoys, with a seed. Recipes for the demo (one per problem story Ken wants to tell) are saved and rerunnable.
- Every room from a real company's profile carries "Synthetic test document. Not this company's data." on every page, and its plants are named test plants.
- The answer key is written from the recipe, and `check.py` checks any room against its key.

**Done when:** a new room is generated from a profile and a recipe in one command; three recipes highlight three different problem sets; each passes `check.py`; and swapping the profile changes every name and leaves every planted problem in place.

**Who:** agent.

**Judgment:** yes.
