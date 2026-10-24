# Product thinking: deck-vs-books

## User job

The associate who prepares the memo opens a deck and a data room. Before they trust any number on a slide, they want to know two things. Does the revenue in the deck match the books for the same period? And does the deck show the whole revenue history, or only the flattering part?

Her rule, in her words: "If revenue in the deck doesn’t match the P&L, or you show only part of your history, everything else becomes questionable." ([associate at a seed-focused fund, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal), quoted in [ROADMAP.md](../../ongoing/roadmap/deck-vs-books.md)).

Today she does it by hand. She reads each revenue number off the deck, finds the month in the P&L tab, and eyeballs the chart against the monthly column. A chart that starts late is easy to miss, because nothing on the slide says what came before.

The partner who reads the memo needs the result as one line with both sources, so they can drill into it ([USER_STORIES.md](../../ongoing/USER_STORIES.md), "The partner who reads the memo").

## Evidence and assumptions

Observed, in the rooms:

- Hollis Voice's deck shows three revenue figures: ARR of $2,500,000 on slides 3 and 14, a monthly recurring revenue chart on slide 3, and plan growth of 3.5% a month on slide 11. Source: the spike's run, [spike/out/hollis_voice.txt](spike/out/hollis_voice.txt).
- The Hollis Voice chart covers the whole history, 2025-01 to 2026-09, so the real room has no partial-history flag. The roadmap's test deck is needed to show the flag on Hollis Voice.
- Brasswick already plants the partial-history flag. BF2 in `data_room/answer_key_brasswick.json`: the chart starts at 2026-01 and the 8 months before it hold a peak in 2025-09. Its check name is `deck_history_vs_metrics`. The spike catches it ([spike/out/validate_brasswick.txt](spike/out/validate_brasswick.txt)).
- The chart bars are an image on both decks. No bar value is in the PDF text. The spike reads the bars' heights from pixels and compares their shape with the P&L. It worked on all four charts it tried ([spike/out/crop_render_check.txt](spike/out/crop_render_check.txt)).

Assumptions that could change the plan:

- A1. The model's P&L tab is "the books" for a seed or Series A company. Neither room has a separate accounting export. If a room arrives with QuickBooks or Xero exports, those become the books and the P&L tab becomes a second read.
- A2. Real decks draw charts in many styles. The pixel reader is built for the rooms' single-colour bar charts. A real deck's chart may need the model's vision reading as a fallback.
- A3. The associate treats any partial history as a red flag, even when the hidden months hold nothing bad. Her quote says so. A partner might call a hidden early ramp harmless. This is a product decision for Ken (see the PRD, open question Q2).

## Priority

The breakdown ([00_breakdown.md](../20261022.10_feature_breakdown/00_breakdown.md)) puts this in wave 1 beside accounting-mislabels and checklist-coverage. It is small, it needs no model key, and it joins the red-flag engine, which is first in the demo. It also gives Brasswick's BF2 a home: no other slice names `deck_history_vs_metrics`.

What it displaces: nothing on Saturday. It is built before Saturday by an agent.

## Options

- **Do nothing.** The engine's `deck_claim_vs_named_cell` already flags the deck's ARR against `ARR_TOTAL`. It does not look at the chart, the history window or any period other than the as-of month. BF2 would stay uncaught.
- **Model only.** Ask the model to read the chart and compare. Slower, needs a key, and the numbers would be judged, not computed. The roadmap says the script decides a number is wrong.
- **Script, as the spike does (recommended).** Text figures by regex, the chart window from its caption, bar shape from pixels, all matched to P&L cells. The model is a fallback for charts the script cannot read.

## Recommendation

Build the script check inside the red-flag engine, as `scans/redflags/deck_vs_books.py`. It writes two check names: `deck_revenue_vs_pnl` for the period-by-period match and `deck_history_vs_metrics` for partial history. Add Brasswick's BF2 to the slice's Done when. Ask Ken one question: is a partial history with nothing bad in the hidden months a flag or a watch?
