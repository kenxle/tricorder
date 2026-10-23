# Proposed FRAMEWORKS.md entry: deck revenue against the books

This is a proposal for whoever keeps [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md). It is written in that file's entry shape so it can be pasted in as entry 1.14, under "Scan 1. The red-flag engine". This folder does not edit `docs/ongoing/`. The code is `scans/redflags/deck_vs_books.py`. Its requirements are in [03_prd.md](03_prd.md).

Two rows would also join the table "Where each planted flag is caught":

| Planted entry | Entry that must catch it | Check name | Catchable from the seed drop |
|---|---|---|---|
| BF2 The deck's revenue chart starts after a fall (`answer_key_brasswick.json`) | 1.14 Deck revenue against the books | `deck_history_vs_metrics` | Brasswick has one tier |
| PF2 Deck ARR disagrees with the model, second read against the P&L | 1.14 | `deck_revenue_vs_pnl` | Yes. The scorer still credits PF2 to `deck_claim_vs_named_cell` only |

---

### 1.14 Deck revenue against the books

**Scope: built from now to Friday night, run on Saturday inside the red-flag engine.** The roadmap's [deck-vs-books](../../ongoing/ROADMAP.md#deck-vs-books) slice. Scripts only. No model reading.

**Inputs**

- `01_overview/pitch_deck.pdf`, every slide. The claims page (the last slide titled "Appendix ...") for stated figures, with `01_overview/claims.json` as the fallback (1.1).
- The P&L tab of `02_financials/financial_model.xlsx`: the header row ("Line", then one column per month), the row below it ("Actual" or "Plan"), and every line whose section is "Revenue".
- The customer revenue rows (`03_metrics/customer_mrr_by_month.csv` or `03_metrics/revenue_by_customer.csv`), only when the P&L is missing, and only for the chart's window.

**The questions it asks**

1. For each revenue figure in the deck, what does the P&L say for the same period?
2. Does a revenue chart's shape follow the P&L, month by month?
3. Does the chart start at the first month the books hold revenue, and end at the last actual month?
4. If later, what do the months left out hold: a climb, a dip, or a flat stretch?
5. Does the chart skip months, or show quarters where the books hold months?

The associate's rule behind it: "If revenue in the deck doesn’t match the P&L, or you show only part of your history, everything else becomes questionable." ([associate at a seed-focused fund, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal)).

**Mechanical check**

Check names: `deck_revenue_vs_pnl` and `deck_history_vs_metrics`. The second is the name `answer_key_brasswick.json` gives BF2.

```
figures = claims-page rows whose label has ARR, MRR or revenue and whose value is a dollar amount
        + chart captions "Monthly|Quarterly [recurring] revenue, <Month YYYY> to <Month YYYY>"
        + "Revenue grows X% a month in the plan." and "Revenue grew every month in YYYY."
as_of   = "Data as of YYYY-MM" on slide 1
for each stated figure:
    ARR                     -> 12 x the P&L's "Recurring revenue..." line at as_of
    MRR, <Month YYYY>       -> "Subscription revenue" for that month
    Revenue, last 12 months -> sum of "Total revenue" over the 12 actual months to as_of
    gap_rel = |deck - books| / |books|
    flag if gap_rel > match_tolerance, unless a short-form figure is within half its last printed digit
for each chart:
    bars    = pixel heights of the chart's bars, from pdfplumber's render of the chart's box
    shape   = max over periods of |bar / tallest bar - books / largest period|
    flag if the bar count differs from the periods, or shape > chart_shape_tolerance
    first   = first actual month with "Total revenue" > 0
    left_out = actual months from first up to the chart's first month
    if left_out: "shows part of the history"
        flag if left_out holds a peak above the chart's first month, a month-on-month fall,
             or three months in a row within 1 percent of each other
        watch if left_out holds only a climb
    trailing = actual months after the chart's last month
    if trailing: "shows part of the history"
        flag if revenue in them falls below the chart's last month, falls month on month, or goes flat
        watch if it only keeps climbing
    if the chart is quarterly: watch, or flag if a month inside a quarter fell
    if monthly bars < months in the window: flag (skipped months)
months the chart shows that the books lack -> gap, for the ask list
```

Settings: `match_tolerance` (0.01) and `chart_shape_tolerance` (0.02), from `schema.settings.load()`.

Worked example, Hollis Voice (`data_room/hollis_voice/`, run by `python3 -m scans.redflags`; output in [evidence/pipeline.txt](evidence/pipeline.txt)):

| Deck figure | Books | Result |
|---|---|---|
| ARR $2,500,000, slides 3 and 14 | 12 × `P&L!W10` (186,739) = $2,240,868 | 11.6% apart: flag |
| Chart on slide 3, 21 bars, 2025-01 to 2026-09 | "Recurring revenue (subscription plus pilot)", 21 months | shape within 0.4 points: info |
| Chart window from 2025-01 | first revenue month 2025-01 | whole history: info |
| "Revenue grows 3.5% a month in the plan.", slide 11 | the plan columns grow 3.50% a month | matches: info |

A test deck whose chart starts at 2025-07 leaves out 2025-01 to 2025-06, which hold a climb from $2,651 to $19,462. That is a watch ([evidence/test_rooms.txt](evidence/test_rooms.txt)).

Worked example, Brasswick (`data_room/brasswick/`): the chart on slide 4 starts at 2026-01. The books start at 2025-05. The 8 months left out hold a peak of $84,090 in 2025-09, and revenue fell 28.2% from it to $60,400 in 2026-01, with month-on-month falls in 2025-10 and 2025-12. That is a flag, and `python -m eval.score data_room/brasswick` counts BF2 as found. The deck's "Revenue, last 12 months" of $943,340 and "MRR, September 2026" of $84,810 match the P&L. Whether the P&L itself is right (BF1, BF4) is entry 1.12's question.

**Model reading**

None. A chart the script cannot read is a gap. A later version may read it with vision as `judged` claims.

**Output shape**

No model output, so no JSON Schema of its own. The check returns Claims and Gaps (the shared `$defs`) and one Panel, "deck against the books", with the columns Slide, Deck figure, Period, Books, How the books figure is made, Gap, Within tolerance.

- A stated figure: `value` with label `arr`, `mrr` or `other`, its unit and period. Sources: the deck slide or slides, and every P&L cell the books figure was made from.
- Partial history: text starts "Shows part of the history:". `value` is the months left out, unit `months`, label `other`. Sources: the caption, the first revenue month's cell, the peak's cell, the chart's first month's cell.
- A figure with no books counterpart: an `info` claim with the deck source and the reason.

**How the readout scores it**

- `flag` claims feed **traction and revenue** (labels `arr`, `mrr`) or **the pitch itself** (label `other`, partial history).
- A `watch` partial history shows under the pitch itself and does not by itself make a piece weak.
- Its gaps carry `piece` "traction_and_revenue" and go on the ask list.

**What it must not do**

- Say why a deck figure differs from the books, or why a chart starts late.
- Compare the deck's ARR with `ARR_TOTAL`. That is 1.5.
- Judge whether the books are right. That is 1.2 and 1.12.
- Read a chart's numbers from outside the room, or guess a bar it cannot see.
