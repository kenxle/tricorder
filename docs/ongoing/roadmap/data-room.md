# data-room

The synthetic Hollis Voice data room, its generator and its answer key, built to the [data room research](../../reports/20261022.02_research/research_data_room.md), Part 3.

- **Status today:** done.
- **Who builds it:** agent.
- **Waits on:** nothing. It builds to the research's recommended company (Hollis Voice, an AI phone agent for independent vet clinics). If Ken picks another company on the overview page, the generator takes a different config. Ken's yes or no on installing `xlsxwriter` decides whether model formulas carry stored values; without it the generator writes plain values (research Part 3.6).
- **Horizon:** Now to Friday night
- **Checked against:** data_room/ generator and the four rooms exist, slice Status line says built.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The synthetic Hollis Voice data room, its generator and its answer key, built to the [data room research](../../reports/20261022.02_research/research_data_room.md), Part 3.

**Waits on:** nothing. It builds to the research's recommended company (Hollis Voice, an AI phone agent for independent vet clinics). If Ken picks another company on the overview page, the generator takes a different config. Ken's yes or no on installing `xlsxwriter` decides whether model formulas carry stored values; without it the generator writes plain values (research Part 3.6).

**Includes:**

- `data_room/generate.py`, `data_room/check.py`, `hollis_voice/` (the full room) and `hollis_voice_seed_drop/` (the thin first tier), as built ([data_room/README.md](../../../data_room/README.md)).
- 17 files in the full room and 12 in the seed drop (the answer key's `full_room_files` and `seed_drop_files`), every one generated from one seeded simulation (seed 20261024).
- The 8 planted entries (7 flags plus the video variant), the 3 clean decoys and the 3 green flags in the answer key.
- `data_room/answer_key.json` outside both room folders, so Tricorder is never pointed at it. Each entry's `check` field uses the check names written in the [saturday-specs](saturday-specs.md) slice, so Saturday's test can match a readout flag to a key entry.
- `01_overview/claims.json` in both rooms, written by the generator from the same list as the deck's claims slide (slide 14), with the deck's claims as data, the fallback the feasibility research recommends when PDF reading fails ([research_feasibility.md](../../reports/20261022.02_research/research_feasibility.md), 1.1 and 1.9).
- The footer "Synthetic data room for Deal Flow NYC 2026. Not a real company." on every page and sheet. Invented names only; emails on `example.com`.
- A fresh web search for the company name before it appears anywhere public (research open point).
- Real green flags, set by the overview page's card "Green flags in the demo room". The recommended answer frees the customers piece: the generator drops the customer-concentration plant, so the order forms, the revenue-by-customer file and the metrics export agree, and customers reads strong. If Ken picks that answer, the slices and the beat sheet that name the concentration flag change in the same pull request.

**Done when:**

- `data_room/.venv/bin/python data_room/generate.py` writes both rooms and the answer key from a clean checkout.
- If Ken picks "Free the customers piece" on the card, at least one business piece built from independent files reads looking strong on the full room.
- `data_room/.venv/bin/python data_room/check.py` ends with 0 failed. On 2026-10-22 it printed "276 passed, 0 failed".
- The reference checks stay inside `data_room/check.py`. Saturday's red-flag engine is written fresh in the room and does not copy them.

**Status:** built. The green-flags card is still open, so the customer-concentration plant is still in the room.

**Who:** agent. Ken reviews the deck and the video script.

**Judgment:** yes.
