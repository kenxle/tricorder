# PRD: deck-vs-books

Context, users and the problem are in the [short brief](01_brief.md) and [product_thinking.md](product_thinking.md). The agreed behavior is the output in [02_interface_example.md](02_interface_example.md). This page adds scope, requirements and failure cases.

## Scope

In scope:

- Every revenue figure the deck shows, in text or as a bar chart: a headline total (ARR, MRR, revenue over a span), a chart's bars and window, and a growth sentence.
- Matching each to the same period in the model's P&L tab.
- Partial history: a chart that starts after the first revenue month, skips months, or shows quarters where the books hold months.
- The gaps these produce, which the ask list reads.

Not in scope:

- The deck's ARR against `ARR_TOTAL`. That is the engine's `deck_claim_vs_named_cell` (PF2). This feature compares against P&L cells instead (see Q1).
- Whether the books themselves are right. A pilot in recurring revenue (PF1), an annual invoice booked in one month (Brasswick BF4) and gross recoveries (BF1) belong to entries 1.2 and 1.12.
- Non-revenue figures: clinics, calls, margin, runway, market size.
- Revenue figures outside the deck (the overview, the video, the website). The video is entry 4.3.
- A model reading of charts. It is a later fallback (DVB-R8), not built in this slice.

## Solution outline

A script inside the red-flag engine reads the deck by slide and the P&L by cell. It finds the revenue figures by pattern, maps each to a P&L line and period, and compares with `match_tolerance`. It reads a chart's window from its caption and its bars from the chart's pixels. It compares the window with the first revenue month in the books. It writes one Claim per figure and one per chart window, under two check names: `deck_revenue_vs_pnl` and `deck_history_vs_metrics`. Missing inputs become Gaps.

## Requirements

Each requirement has a stable id. The Plan's verification table names the test for each.

::: callout-req
**DVB-R1. Find every deck revenue figure.** The check reads the claims page (the last slide whose title starts with "Appendix") and keeps each row whose label contains ARR, MRR or revenue and whose value is a dollar amount. For each row it finds the same figure on the cited content slide, in its printed form (for example "$2.5M" for $2,500,000). It also finds chart captions of the form "Monthly|Quarterly [recurring] revenue, <Month YYYY> to <Month YYYY>" and the growth sentences "Revenue grows X% a month in the plan." and "Revenue grew every month in YYYY.". When the deck has no claims page, it reads `01_overview/claims.json` instead (FRAMEWORKS entry 1.1).
:::

::: callout-req
**DVB-R2. Map each figure to a P&L line and period.** The mapping is a fixed table in the code:

| Deck label | P&L line | Period |
|---|---|---|
| ARR | 12 times the first line whose label starts "Recurring revenue", else "Subscription revenue" | the as-of month, from "Data as of YYYY-MM-DD" on slide 1 |
| MRR, <Month YYYY> | "Subscription revenue" | that month |
| Revenue, last 12 months | the sum of "Total revenue" | the 12 actual months ending at the as-of month |
| Chart captioned "recurring revenue" | the recurring line above | each month in the caption's window |
| Chart captioned "revenue" | "Total revenue" | each month in the window |
| "X% a month in the plan" | month-on-month growth of the recurring line | the plan columns |
| "grew every month in YYYY" | "Total revenue", month on month | the actual months of that year |

A label the table does not cover is unmatched (DVB-R5).
:::

::: callout-req
**DVB-R3. Compare with the tolerance.** A figure matches when `|deck − books| ÷ |books| ≤ match_tolerance` from `schema.settings.load()` (default 0.01). A figure printed in short form, with no exact form anywhere in the deck, also matches when the difference is within half a unit of its last printed digit ($2.5M is within $50,000). This keeps a rounded figure from reading as a mismatch (FRAMEWORKS 1.5, "What it must not do"). The claim then says the match is "within the rounding of the printed" figure. A books value of 0 makes the figure unmatched, never a division by zero.
:::

::: callout-req
**DVB-R4. One claim per matched figure.** Each matched or mismatched figure is a Claim with check name `deck_revenue_vs_pnl`, confidence `computed`, and sources on both sides: the deck slide or slides with the figure as printed, and every P&L cell the books figure was made from. A mismatch has severity `flag`. A match has severity `info`. The claim's text names both numbers, how the books figure was made, and the gap in percent.
:::

::: callout-req
**DVB-R5. Unmatched figures are listed.** A figure with no P&L counterpart is an `info` claim with its deck source and the reason, for example "no rule maps the label 'Bookings' to a P&L line". When the P&L is missing, every figure is unmatched for that reason.
:::

::: callout-req
**DVB-R6. Chart bars against the books.** The check counts the chart's bars and measures each bar's height in pixels. It compares each bar's height as a share of the tallest bar with each period's revenue as a share of the largest period. The bars match when the count equals the number of periods and the largest difference is at most `chart_shape_tolerance` (in `schema/settings.py`, default 0.02, that is 2 points of the tallest bar). A match is an `info` claim. A wrong count or shape is a `flag` claim. Both use `deck_revenue_vs_pnl`.
:::

::: callout-req
**DVB-R7. Partial history.** The first revenue month is the first actual month in which "Total revenue" is above zero. The check compares it with the chart's first month. It writes a claim, check name `deck_history_vs_metrics`, that starts "Shows part of the history:" when any of these hold. Its severity is `flag` when the hidden months hold a dip (a month-on-month fall, or a peak above the chart's first month) or a flat stretch (three months in a row within 1 percent of each other), when months are skipped, or when quarters hide a monthly fall. It is `watch` when the hidden months hold only a climb, or quarters hide no fall (Ken's decision, 2026-10-22, relayed by the coordinator):

- the chart starts after the first revenue month. The claim lists the months left out and says what they hold: the peak and the fall from it to the chart's first month when revenue fell, or the climb from the first to the last left-out month when it did not;
- the chart ends before the last actual month (added in review round 1, finding S3). The claim lists the months left out after it. It is a `flag` when revenue in them falls below the chart's last month, falls month on month, or goes flat, and a `watch` when it only keeps climbing;
- the chart has fewer monthly bars than its window has months. The claim says how many are skipped;
- the chart shows quarters where the books hold months. The claim names any month inside a quarter where revenue fell, or says none fell.

Its sources are the chart's caption, the first revenue month's cell, the peak's cell and the chart's first month's cell. Its value is the number of months left out before and after the window (skipped bars are not counted), unit `months`, label `other`. A chart that covers the whole history, from the first revenue month to the last actual month, is an `info` claim under the same check name.
:::

::: callout-req
**DVB-R8. A chart the script cannot read.** When the slide has no image, or the image has no single-colour bars, the check writes the gap "Not in the room: a readable chart on slide N". The window check (DVB-R7) still runs from the caption. A later model reading may fill the bars as `judged` claims. It is not built in this slice.
:::

::: callout-req
**DVB-R9. Revenue rows as a cross-check only.** The check may sum the customer revenue rows (`customer_mrr_by_month.csv` or `revenue_by_customer.csv`) by month. It writes no claim from the difference, because the differences found belong to other checks (BF4 on Brasswick; the pilot in the clean room's `mrr` column). When the P&L is missing and the revenue rows are present, the first revenue month and the chart window (DVB-R7) are read from the revenue rows, and the claim cites them.
:::

::: callout-req
**DVB-R10. Missing inputs are gaps.** Each gap sets `piece` to `traction_and_revenue`:

- no deck: "Not in the room: the pitch deck (01_overview/pitch_deck.pdf)", and no claims;
- no P&L: "Not in the room: the monthly P&L (02_financials/financial_model.xlsx, P&L tab)", would need "The monthly income statement for every month since the first revenue";
- a chart window that reaches months the books do not hold: "Not in the room: monthly revenue for <first> to <last>, shown on slide N", would need "The monthly P&L for <first> to <last>". These go on the ask list.
:::

::: callout-req
**DVB-R11. Feeds the right pieces.** Claims with label `arr` or `mrr` feed traction and revenue, by the readout's rule (FRAMEWORKS "Piece verdicts"). Partial-history claims and claims with label `other` feed the pitch itself. Gaps feed traction and revenue (DVB-R10).
:::

::: callout-req
**DVB-R12. Every claim passes the quote checker.** Every source's uri is relative to the room. Every quote is the text the shared reader returns at the locator: the slide text for a deck source, `str(value)` for a cell. `python -m schema.check_quotes <room> out/<room>/redflags.json` marks no claim of this check unverified.
:::

::: callout-req
**DVB-R13. Scripts only, offline, shared readers.** No model call. No network. Files are read through `schema/readers.py`. Chart pixels come from pdfplumber's page render, cropped to the image's box. No new dependency.
:::

## Failure cases

| Case | What happens | Requirement | Seen in the spike |
|---|---|---|---|
| The P&L is missing | One gap. Every figure listed as unmatched. Window check from the revenue rows if present | DVB-R5, R9, R10 | [hollis_voice_no_pnl.txt](spike/out/hollis_voice_no_pnl.txt) (the revenue-row fallback is not spiked) |
| The deck chart is unreadable | Gap "a readable chart on slide 3". Window still checked from the caption | DVB-R8 | [hollis_voice_chart_unreadable.txt](spike/out/hollis_voice_chart_unreadable.txt) |
| The deck shows quarters, the books hold months | Books summed by quarter. Bars compared by quarter. Partial-history flag that names any hidden monthly fall | DVB-R6, R7 | [hollis_voice_chart_quarterly.txt](spike/out/hollis_voice_chart_quarterly.txt) |
| The chart starts late | Partial-history flag with the months left out and what they hold | DVB-R7 | [hollis_voice_chart_starts_late.txt](spike/out/hollis_voice_chart_starts_late.txt), [brasswick.txt](spike/out/brasswick.txt) |
| The chart shows months the books do not hold | Gap for the ask list | DVB-R10 | Not spiked: no room has it |
| No deck | Gap, no claims | DVB-R10 | Not spiked |
| A deck label no rule maps | Unmatched info claim | DVB-R5 | Not spiked: every revenue label in both rooms maps |
| The plan columns hold no cached values | Unmatched info claim | DVB-R5 | Handled in the spike code; no room has it |

## Analytics and logging

None beyond the ScanResult. The claims are the record.

## Rollout and flags

No flag. `scans/redflags/scan.py` already lists `deck_vs_books` in `CHECKS` and skips a module that does not exist yet. The slice lands when its module and tests merge.

## Questions

Open, for Ken or the owner named:

- **Q1. The ARR overlap with PF2 (readout owner).** On Hollis Voice this feature flags the deck's $2,500,000 against the P&L's $2,240,868 (12 times recurring revenue for 2026-09), a gap of 11.6%. The engine's `deck_claim_vs_named_cell` flags the same deck figure against `ARR_TOTAL`, which holds the same $2,240,868. The scorer counts neither twice, because the check names differ. The readout could show two red lines for one problem. Recommendation: keep both claims, because they cite different sources, and have the readout group flag claims with the same label, unit and period into one top flag. Source: [spike/out/hollis_voice.txt](spike/out/hollis_voice.txt).
- **Q3. A `revenue` value label (schema owner).** `Value.label` has `arr` and `mrr` but no revenue key. A deck's "Revenue, last 12 months" and the partial-history count use `other`, so the memo cannot link them across sources. Recommendation: leave it for Saturday; add `revenue` after.

Resolved:

- **Q2, flag or watch when the hidden months hold nothing bad.** Default chosen by the orchestrator on 2026-10-22, open for Ken to change: a `watch`. It stays a `flag` when the hidden months hold a dip or a flat stretch. On the test deck the six months left out hold a climb from $2,651 to $19,462, so it is a watch ([evidence/test_rooms.txt](evidence/test_rooms.txt)).

- Which check name for partial history: `deck_history_vs_metrics`, because `answer_key_brasswick.json` uses it for BF2 and `eval.score` matches on it.
- Where the chart's numbers come from: the pixels, scale free, because the bar values are not in the PDF text and the model is not on the main path. The spike read 21, 9, 15 and 7 bars correctly and matched shapes within 0.4 points ([02_interface_example.md](02_interface_example.md)).
- The books: the model's P&L tab, because neither room has an accounting export (product note, A1).
