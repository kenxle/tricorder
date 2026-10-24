# deck-vs-books

The associate's rule, as a feature: "If revenue in the deck doesn’t match the P&L, or you show only part of your history, everything else becomes questionable." ([associate at a seed-focused fund, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal); [writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:19 PM block).

- **Status today:** done.
- **Who builds it:** agent.
- **Waits on:** data-room; saturday-specs (the check list, including `deck_claim_vs_named_cell`).
- **Horizon:** Now to Friday night
- **Checked against:** merged in PR #4, scans/redflags/deck_vs_books.py exists.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The associate's rule, as a feature: "If revenue in the deck doesn’t match the P&L, or you show only part of your history, everything else becomes questionable." ([associate at a seed-focused fund, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal); [writers' brief](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:19 PM block). Saturday's red-flag engine already compares the deck's claims with the model's named cells (`deck_claim_vs_named_cell` in [FRAMEWORKS.md](../FRAMEWORKS.md)). This slice adds the two halves of her rule that it does not cover.

**Waits on:** data-room; saturday-specs (the check list, including `deck_claim_vs_named_cell`).

**Joins on Saturday:** [redflag-engine](redflag-engine.md).

**Includes:**

- **Deck revenue against the P&L, period by period.** Every revenue figure the deck shows (a total, a chart's bars, a growth rate) is matched to the same period in the monthly P&L and the revenue rows, by script. A mismatch above the match tolerance is a disagreement claim with both sources.
- **Partial history.** A script finds the first month revenue appears in the books and compares it with the window the deck shows. A deck chart that starts later than the books, skips months, or shows quarters where the books hold months is flagged as "shows part of the history", with the months left out and what they hold (for example a dip, or a period of flat revenue).
- Both feed the traction and revenue piece and the pitch itself, and missing months the books do not hold go on the ask list.

**Done when:** on the Hollis Voice room, every deck revenue figure is matched to a P&L period or listed as unmatched; a test deck whose chart starts six months after the first revenue month is reported with the months it leaves out (it is a watch, because those months hold only a climb); on Brasswick, `python3 -m eval.score data_room/brasswick` counts BF2 as found; and the quote checker passes on every claim.

**Who:** agent.

**Judgment:** no.

**Status:** done. Merged in PR #4 on 2026-10-23. The code is `scans/redflags/deck_vs_books.py`, written up as [FRAMEWORKS.md](../FRAMEWORKS.md) entry 1.14. Feature folder: [20261022.11_deck_vs_books](../../features/20261022.11_deck_vs_books/00_progress.md).
