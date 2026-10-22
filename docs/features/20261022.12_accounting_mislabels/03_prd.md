# PRD: accounting mislabels

Context, users and problem: [01_brief.md](01_brief.md) and [product_thinking.md](product_thinking.md). Rules: [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md), entry 1.12, which this PRD follows except where a requirement says "extends 1.12". The agreed output: [02_interface_example.md](02_interface_example.md). Every number below comes from the spike run in [spike/spike_run.txt](spike/spike_run.txt) or the score in [spike/score_run.txt](spike/score_run.txt), both written by the scripts in [spike/](spike/).

## Scope

In scope:

- Six sub-checks from entry 1.12: `mrr_column_vs_subscription_rows` (kind a, the `mrr` column), `billings_vs_recognised_revenue` (b), `contractor_spend_vs_headcount_and_burn` (e), `capitalised_spend_vs_pnl_and_cash` (f), `deferred_revenue_vs_earned` (g) and `one_time_fees_in_recurring_metrics` (h).
- Kind c, `gross_vs_net_revenue`.
- A gap for each kind the room cannot test, worded as entry 1.12 gives it.
- A resale test room for kind c, written at test time.
- Both room shapes in the repo: Hollis Voice (`customer_mrr_by_month.csv`) and Brasswick (`revenue_by_customer.csv`).

Not in scope:

- The ARR side of kind a (entry 1.2, `arr_from_subscription_rows`) and kind d (entry 1.7, `gross_margin_from_ledger`). The engine owns them.
- The model reading in entry 1.12. Nothing planted needs it. It can follow after Saturday.
- Rerunning the cash plan for Brasswick's runway (BF3's 23 months). See open question Q4.
- Changing `data_room/generate.py`. See open question Q2.

## Solution outline

One module, `scans/redflags/mislabels.py`, with one function per sub-check and a `check(room, ids)` that runs them in entry 1.12's order. Each sub-check reads the room through `schema/readers.py`, computes its formula, and returns claims and gaps. The red-flag engine's `scan.py` already lists `mislabels` in `CHECKS`, so landing the module turns it on. Details: [04_architecture.md](04_architecture.md).

## Requirements

Each sub-check ends in exactly one outcome. The outcome decides what it writes:

| Outcome | What the sub-check writes |
|---|---|
| flag | One or more claims with severity "flag" |
| watch | One claim with severity "watch" |
| clear | One claim with severity "info" that states the tie-out it ran, plus any gap entry 1.12 lists beside the clear |
| cannot_check | No claim. The gap entry 1.12 gives, with `why` "file missing" |
| not_run | No claim. A gap with `why` "not stated in the file" |

### Shared

- **AM-R1. Contract.** The module exposes `check(room: Path, ids: Ids) -> tuple[list[Claim], list[Gap]]`. It takes each claim id from `ids()`. It reads files only through `schema.readers` and the room finders in `scans.base`. It reads `match_tolerance` from `schema.settings.load()`. It makes no network call and no model call.
- **AM-R2. Claim fields.** Every claim has `check.kind` "script", `check.name` equal to its sub-check name, `check.model` null, `confidence` "computed", at least one source, and empty `conflicts_with` and `corroborated_by`.
- **AM-R3. Kind named.** Every flag and watch claim's text ends with its mislabel kind in plain words, for example "Mislabel kind a: non-recurring revenue in MRR." The redflag-engine slice asks the same of its two kinds. (Not yet in the spike.)
- **AM-R4. Gaps.** Every gap's `what` starts with "Not in the room:", uses entry 1.12's wording, and sets `piece` from entry 1.12's table: kinds a, b, c, g and h feed `traction_and_revenue`; e and f feed `burn_and_runway`. Its `would_need` is a document an operator can ask for in an email.
- **AM-R5. Quote checker.** Every claim passes `schema.check_quotes.check_claim` on the room it ran on. A CSV source quotes the whole row text. A cell source quotes the cell's value as `text_at` renders it.
- **AM-R6. Bad input never crashes.** A missing column, an empty file, a missing P&L row or a `LocatorError` turns into a gap for that sub-check. The other sub-checks still run.

### Kind a: the `mrr` column

- **AM-R7.** Recompute subscription MRR per month from the customer file (`product_type` "Subscription"). Flag each month where `monthly_metrics.mrr` exceeds it by more than `match_tolerance`.
- **AM-R8.** The claim names the non-subscription line that makes up the difference when the line equals it within tolerance. It cites the metrics row, the largest customer-file row of each non-subscription product type, and the model's `ARR_Build` row for the same line (label and ARR counted).
  - Full room: flags 2026-08 and 2026-09. For 2026-09, MRR shown $186,739, subscription rows $171,739, difference $15,000 (8.7%), equal to Marlow Veterinary Group's Pilot row. It cites `customer_mrr_by_month.csv` row 2101 and `ARR_Build!A13` and `ARR_Build!E13`.
- **AM-R9. Link to the pilot-as-ARR flag.** The link is the shared source: this claim and entry 1.2's flag both cite the pilot's `ARR_Build` row. The readout groups claims that share a source locator under one cause. No new field. See [04_architecture.md](04_architecture.md), decision D3.
- **AM-R10. Seed-drop fallback.** With no customer file, read `ARR_Build` (the Product type column and the monthly history's Subscription MRR) as entry 1.12 says, and add the gap "Not in the room: a revenue export by product type". With `ARR_Build` missing too, return cannot_check with that gap.
  - Seed drop: flags, with the same $15,000 and 8.7%, citing `ARR_Build!A13`, `B13` and `C39`.

### Kind b: billings shown as revenue

- **AM-R11.** Per actual month, compare the P&L row "Subscription revenue" with subscription billings and subscription revenue from the customer file. Flag a month when the P&L figure sits nearer billings and differs from revenue by more than `match_tolerance`. Run the same test on `ARR_TOTAL ÷ 12` for the as-of month.
  - Full room: clear. The P&L row matches revenue in all 21 months, largest difference $0. Billings differ from revenue in 18 months, which annual plans explain.
  - Brasswick: flags 2026-09. P&L $84,810; billings $82,650; revenue $59,565.
- **AM-R12.** With no billings column or no customer file: cannot_check, gap "Not in the room: an invoices or billings export".

### Kind c: gross against net revenue

- **AM-R13.** Find pass-through money in the customer file: a column whose name says remitted or pass-through (with a sibling fee column as the net), or rows whose product type says resale or pass-through.
- **AM-R14.** Find which revenue-labelled figure holds it: a P&L Revenue row or a metrics column whose as-of value equals the gross amount within tolerance and sits nearer the gross than the net. Flag when the pass-through share of the last 12 months' revenue exceeds `match_tolerance` and the figure's label does not say "gross". Cite the holding figure, the pass-through row, and a ledger line paid on at cost when one exists.
  - Brasswick: flags. $264,214.66 of pass-through inside $943,339.50 of P&L total revenue over the 12 months to 2026-09, 28.0%; net $679,124.84. The ledger shows the same $264,214.66 paid on.
  - Resale test room, option on: flags. $36,825 inside $1,386,023 of the `mrr` column, 2.7%.
  - Resale test room, option off, and the full room: not_run, gap "Not in the room: a revenue export that separates pass-through money".
- **AM-R15.** With no customer file: cannot_check with that gap.

### Kind e: contractors left out of headcount and burn

- **AM-R16.** Find contractor lines by entry 1.12's keywords plus "contract engineering", "statement of work" and "SOW" (extends 1.12). Once one line from a vendor matches, every line from that vendor counts.
- **AM-R17.** Flag a month whose ledger total differs from P&L cost of revenue plus operating expenses by more than `match_tolerance` (entry 1.12's tie test).
- **AM-R18. Plan test (extends 1.12).** Find the P&L row that holds the contractor lines: the row whose as-of actual equals the ledger sum of their categories. Flag when the first plan month's value on that row, less the row's non-contractor actual, covers less than the contractor run rate. Cite both P&L cells, the contractor ledger rows and the staff count cell.
  - Brasswick: flags. Contractor lines $34,708.97 in 2026-09 from Fernway Contractor Payments and Norrgate Software Studio, in "Professional services" ($36,149.98). The plan puts $2,800 on that row from 2026-10. Entry 1.12's keyword list alone misses Norrgate Software Studio.
- **AM-R19.** Watch when contractor lines exist and neither test flags. Clear otherwise, with the gap "Not in the room: a list of contractors, or an org chart that shows them".
  - Full room: clear. Ledger ties in all 21 months, largest difference $0. No contractor lines.
- **AM-R20.** With no ledger: cannot_check, gap "Not in the room: an expense ledger".

### Kind f: capitalised costs off the P&L

- **AM-R21.** Entry 1.12's three tests: asset-named lines, the tie gap, and the cash bridge difference against cash. Always add the gap "Not in the room: a balance sheet". The claim text never says a treatment is wrong.
  - Full room: clear. Every line is booked as Cost of revenue, G&A, R&D or S&M; bridge difference -$0.24 against $1,800,000.
  - Brasswick: clear. Bridge difference $0.21 against $641,318.
- **AM-R22.** With no ledger: cannot_check, gap "Not in the room: an expense ledger".

### Kind g: deferred revenue counted as earned

- **AM-R23.** Entry 1.12's two tests: P&L "Subscription revenue" above revenue earned, and `ARR_Build` "Subscription ARR" above 12 times as-of subscription revenue. On a flag, name the customers whose unearned invoice amounts add to the excess.
  - Full room: clear. Deferred at 2026-09 is $104,876 across 28 customers. Subscription ARR is $2,060,868, which is 12 times $171,739.
  - Brasswick: flags. P&L $84,810 against $59,565 earned; the $25,245 excess is Ostley Freight's unearned invoice.
- **AM-R24. Bridge test (extends 1.12).** When the model names a deferred revenue cell, compare it with the rebuilt balance. Write it as a flag only when no P&L flag fired, and as info otherwise, because the cell is also a decoy location (Brasswick DC1).
  - Brasswick: info. Rebuilt $33,885 across 2 customers; the bridge carries $8,640.
- **AM-R25.** With no customer file: cannot_check, gap "Not in the room: a balance sheet with a deferred revenue line". With no deferred cell in the model, add that gap beside a clear.

### Kind h: one-time fees in recurring metrics

- **AM-R26.** Entry 1.12's two tests: the `mrr` gap equal to the month's fees, and ARR counted on an Onboarding row. With no customer file, take fees from the P&L row "Onboarding fees (one-time)" and subscription MRR from `ARR_Build`.
  - Full room and seed drop: clear. 2026-09 fees $9,500; `mrr` gap $15,000; ARR counted on "Onboarding fees" $0.
  - Brasswick: not_run. No fee column and no fee row.

### Decoys, clean room and scoring

- **AM-R27. Decoys stay clear.** No flag or watch claim cites a Brookline Row (C0193) row, a June 2026 customer-file row, an Onboarding row, `ARR_Build!A14` or `E14`, or the Brookline order form. On Brasswick, no flag claim cites a DC1 or DC2 location.
- **AM-R28. Clean room.** On `hollis_voice_clean`, no sub-check flags or watches.
- **AM-R29. Answer-key score.** `python -m eval.score` reports 0 decoys flagged on Hollis Voice, its seed drop, the clean room and Brasswick, and finds BF1, BF3 and BF4 on Brasswick. The spike's score with the same rule: Brasswick 3 found, 0 of 3 decoys; the Hollis rooms 0 of 3 decoys.

### Test room

- **AM-R30.** A test fixture writes the resale test room to a temporary folder from `data_room/hollis_voice`: a Resale row per paying subscription clinic from 2026-04 at $25 a location, and the same money added to the `mrr` column. With the option off it writes an unchanged copy. Nothing is written under `data_room/`.

## Failure cases

| Case | Expected |
|---|---|
| Seed drop, customer file and ledger missing | a and h run from the model; b, c, e, f, g return cannot_check with their gaps |
| Room with no model | a, b, g, h fall back to what the CSVs hold; a P&L comparison that cannot run is a gap, not a crash |
| A column renamed or missing | that sub-check returns cannot_check with `why` "column missing" |
| A number cell holds text | the row is skipped and counted; when more than 1 percent of rows are skipped, the sub-check returns cannot_check |
| Annual prepay in billings (DC2) | b and g stay clear |
| Onboarding fee in its own row (DC1) | h stays clear |
| Contractor the plan keeps (Brasswick DC2) | e stays clear on it |
| One cause found by two checks (pilot: 1.2 and a; Ostley: b and g) | both claims cite one shared locator, so the readout groups them |

## Analytics and logging

None beyond the ScanResult. The result file is the record of what ran.

## Rollout

No flag. `scans/redflags/scan.py` already lists `mislabels`; a missing module is skipped. Landing the module turns it on for every room.

## Open questions

- **Q1. Is Brasswick an acceptance room for this slice?** The slice names only Hollis Voice. Brasswick's key names three 1.12 checks and contract-terms-saturday expects BF4 from entry 1.12. Recommended: yes. Owner: coordinator, then Ken.
- **Q2. Does the resale option go into `generate.py`?** The slice asks for a generator option. Brasswick now gives kind c a real room, and a test fixture can write the resale room at test time. Recommended: the fixture now, the generator option only if someone needs a committed room. The design is in [04_architecture.md](04_architecture.md). Owner: coordinator.
- **Q3. Entry 1.12 changes.** AM-R16, AM-R18 and AM-R24 extend 1.12. FRAMEWORKS.md should say so before the module lands. Owner: whoever keeps FRAMEWORKS.md.
- **Q4. Runway for BF3.** BF3's true value is a runway (23 months against 29). Rerunning the cash plan is entry 1.4's job. Recommended: this module states the contractor run rate the plan leaves out, and burn_runway reads it. Owner: redflag-engine.
- **Q5. Info claims on clear sub-checks.** Recommended yes, so a clear shows its work. A reviewer may prefer clears as panel rows only. Owner: readout.

Resolved:

- Kind a runs on the seed drop through the `ARR_Build` fallback, because entry 1.12 says so ("kinds a, d and h still run"). The answer key's `catchable_from_seed_drop` is false for PF1, but that field is about entry 1.2's check. Flagged in Progress for confirmation.
- The link to the pilot-as-ARR flag uses a shared source, because the module returns only claims and gaps.
