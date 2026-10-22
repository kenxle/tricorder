# Monthly revenue by customer

Guide for the data-room document in row 10 of the 30-document table in [the data-room research](../20261022.02_research/research_data_room.md). Written 2026-10-22 from online sources only. Every quote was checked word for word against the page text saved under [raw/monthly-revenue-by-customer/](raw/monthly-revenue-by-customer/). The check list is in [quotes_metrics.csv](quotes_metrics.csv).

## What it is

A table with one row per customer per month, showing what each customer paid or was billed. Good versions also carry the plan, the kind of revenue (subscription, pilot, one-time fee, usage), the number of locations or seats, and the cash invoiced. The founder or finance lead prepares it, usually by exporting from the billing system or the accounting system. It arrives as a CSV or a spreadsheet tab.

From this one file an investor can build four things: customer cohorts, revenue cohorts, customer concentration and the sales cost per new customer. Bain Capital Ventures describes the first two directly. When a company is pulled into a process before it planned, "investors pare down the initial data request to two key items: Historical monthly P&L and monthly revenue by customer over time." ([Bain Capital Ventures](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/)) The author goes on: "This data allows us to put together customer and revenue cohorts which help answer a very simple yet profoundly important question for any business" (the question is how likely an acquired customer is to stay and grow). It is the raw material for retention, concentration and part of unit economics.

## At seed and at Series A

- **Pre-seed:** the research table marks it "not stated". No source asks for it.
- **Seed:** lighter. The evidence is thin. Hustle Fund, a venture fund, lists "Revenue by customer, refunds, churn, gross margin, and concentration where relevant." in its financial checklist and adds at seed "Monthly financial statements and revenue detail that reconcile to the traction claims." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)) My reading: the file is cheap to produce at seed, since the billing system holds it, so a seed company with a few dozen customers can send all of it and one with two or three customers can send a short table.
- **Series A:** expected, and used as the base for the associate's own model. Peony, a data-room vendor, says an associate "will build their own model from your raw data, call your top customers, and tie every claim in your deck back to a source in the room." ([Peony](https://www.peony.ink/blog/series-a-data-room)) Malpani Ventures, a B2B seed fund, lists for Series A "No of customers and revenue per customer over time" and "List of churned customers, revenue churn, reasons". ([Malpani Ventures](https://www.malpaniventures.com/blog/due-diligence-data-room)) Kruze Consulting, an accounting firm, lists "Top 10 client invoices and contracts (only matters for b2b companies)". ([Kruze](https://www.kruzeconsulting.com/what-kind-of-financial-data-should-a-company-prepare-when-seeking-series-a-venture-capital-funding/))

## What a first pass checks

In order:

1. **Is the file raw?** One row per customer per month, not a pivot or a summary. BCV's author says "Any investor worth their salt takes the raw customer file and runs their own analyses." ([Bain Capital Ventures](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/))
2. **Does it cover every month and every customer?** No missing months, no vanished customers.
3. **Does the monthly total tie to the P&L revenue line and to the metrics export?**
4. **What kinds of revenue are in it?** Subscription, pilot, one-time fee, usage, services.
5. **Who are the largest customers, and what share of revenue do they hold?**
6. **How many customers started each month, and how many stopped?** This feeds the cohort rebuild.
7. **Are annual prepayments shown as revenue or as cash?** The billed amount and the recognized amount should be different columns.
8. **Does each large customer have a contract in the room?**

## Green flags

- **A granular file the founder obviously uses.** BCV: "The best teams track their business at a granular level, showing great clarity of thought and a strong hold on the numbers." ([Bain Capital Ventures](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/))
- **A list of churned customers with reasons.** Malpani Ventures asks for it, quoted above.
- **Revenue and cash kept apart.** The file separates revenue from billings, with refunds and credits shown. Hustle Fund lists "refunds" in the same line as revenue by customer (quoted above).
- **The monthly total ties to the P&L.** CRV says ARR "should reconcile to the underlying billing, contract and revenue schedules." ([CRV](https://www.crv.com/content/what-is-a-data-room))
- **Concentration raised by the founder before the investor finds it.** MicroVentures, a crowdfunding platform, says a founder "who cannot articulate how the revenue base will become more distributed over the next 12 to 24 months, or who does not appear to view concentration as a meaningful risk, may warrant additional scrutiny during the diligence process." ([MicroVentures](https://microventures.com/revenue-concentration-risk-when-one-customer-is-too-many)) The reverse is a green flag: a plan to spread it, stated up front. The same page says "concentration at an early stage is not necessarily a red flag on its own."
- **Customer identity handled with care.** Visible, a vendor, tells founders to keep customer personal data out of the room and to use logo lists, aggregate cohort data or approved case studies instead. A file keyed by customer id, with the id-to-name key available on request, does that.

## Red flags and pitfalls

**Common**

- **Selected months or selected customers.** BCV: "Don’t cherry pick specific numbers or time periods." ([Bain Capital Ventures](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/)) a16z's data-room guide: "you only show three months of data when your company is three years old, or you show quarterly but not monthly revenue." ([a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/))
- **Concentration the deck does not admit.** a16z: "Customer concentration is defined as the revenue of your largest customer or handful of customers relative to total revenue, with both revenues reflecting the same time period." ([a16z](https://a16z.com/16-more-startup-metrics/)) It names three risks of a concentrated base: the customers hold the power on price, they can steer the product roadmap, and they can force below-market terms. MicroVentures says "A commonly referenced threshold in investor due diligence is whether any single customer accounts for more than 20% of a company’s total revenue." ([MicroVentures](https://microventures.com/revenue-concentration-risk-when-one-customer-is-too-many)) a16z gives no line. The 20 percent is a rule of thumb from a crowdfunding platform, so Tricorder takes it as a setting.
- **Pilot, trial or one-time lines sitting in the recurring total.** Fortune reports that six VCs said founders are "counting pilots, one-time deals, or unactivated contracts as recurring revenue". ([Fortune](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/))
- **Cash shown as revenue.** One fractional CFO, writing on HackerNoon, describes a client whose books recorded the full amount of an up-front customer payment as revenue in the month the cash arrived, so revenue spiked with each large invoice and nobody could say what ARR was ([HackerNoon](https://hackernoon.com/the-finance-function-saas-founders-build-too-late)). It is one adviser's account of one client. Eagle Rock CFO, an accounting firm, tells founders to "Pay particular attention to accounts receivable aging and deferred revenue." ([Eagle Rock CFO](https://www.eaglerockcfo.com/blog/series-a-preparation/data-room-checklist))
- **Totals that do not tie.** The monthly sum differs from the P&L or the metrics export. CRV treats this as a trust problem: see the quote above on reconciling ARR to billing and revenue schedules.
- **A summary in place of the file.** My reading of BCV's "raw customer file" line: if the room holds only a pivot, an investor cannot rerun the numbers, and the missing detail itself becomes the question.
- **Logos with no relationship context.** Visible lists "Customer logos without relationship context." as a common seed mistake. A logo is not a paying customer until the file shows revenue.

**Rare but serious**

- **A large customer in the file with no contract in the room.** Peony and Kruze both ask for the top ten contracts. Peony: "Top ~10 customer contracts and any material contract above ~$20,000" is the signed paper behind the logos. Tricorder's contract entry (`counted_line_without_contract`) handles this as a gap, never as a flag.
- **A refusal to share it.** Hustle Fund's pause list includes "Refusal to share the basic evidence needed to understand cash, ownership, terms, or material obligations." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))

## How Tricorder checks it

**What a script can check**

Existing checks in [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md):

- `arr_from_subscription_rows` (entry 1.2): ARR rebuilt from the subscription rows only.
- `rebuild_cohorts_from_customer_file` (entry 1.3): cohorts, net and gross retention.
- `top_customer_share` (entry 1.6): top-one and top-three share against the deck's claim, with the 20 percent line as a setting.
- Entry 1.12: `mrr_column_vs_subscription_rows`, `billings_vs_recognised_revenue`, `deferred_revenue_vs_earned`, `one_time_fees_in_recurring_metrics`.
- Entry 1.13: `counted_line_without_contract` for lines with no contract in the room.

Proposed new checks:

- `customer_file_ties_to_pnl`. For each month: `SUM(mrr)` over rows by product type against the P&L revenue rows that carry the same type. Flag a gap above `match_tolerance`. FRAMEWORKS reports that on Hollis Voice the P&L subscription row equals the file's subscription `mrr` in all 21 months.
- `customer_file_shape`. Count duplicate keys (month, customer id, product type); customers with a zero month between two paid months (reactivation or a missing month); months missing between the first and last; negative amounts; unknown product types. Each count is a claim with the row numbers.
- `customer_file_vs_metrics_counts`. Rows with revenue above zero per month against `paying_accounts` in the metrics export.
- `churned_customer_list`. Customers whose last paid month is before the as-of month, counted, so the readout can say how many customers have left even when the metrics export shows no churn column.

**What needs a model to read, and what it must quote**

- Column headers and notes that explain what "revenue", "MRR" and "billings" mean in this file. Quote the header.
- Free-text notes beside rows ("pilot", "credit", "paid annually"). Quote the note with its row.
- Whether a segment column (plan, size, vertical) exists, so the cohort scan can cut by it.

**What Tricorder cannot check, so the operator does**

- Whether the customers exist and pay what the file says. That is a reference call, a look at an invoice, or a bank-feed check.
- Whether a customer's contract matches the file. Tricorder reads contracts only when the room holds them.
- Privacy approvals before the file is shared outside the firm.

## Which readout pieces it feeds

- **Traction and revenue**, **retention**, **customers and contracts**. It also feeds **unit economics**, through new customers per month.
- Checklist items: C03 (the file itself), C05 (ARR rebuilt from subscription lines), C15 (gross and net retention rebuilt from revenue by customer), C37 (customer concentration against the deck's claim), C34 and C43 (contracts for the top customers and for every counted line).

## If it is missing

- **Pre-seed:** not a gap.
- **Seed:** a gap, lighter. Not a red flag.
- **Series A:** a gap that blocks three pieces at once (traction and revenue, retention, and the concentration part of customers). BCV names it as one of the two files a fund keeps when it cuts the request down, so a Series A room without it reads as not ready. It is a red flag only if the founder declines to share it.
- **Ask-list line:** "Send monthly revenue by customer for every month since the first customer, one row per customer per month, with plan, kind of revenue (subscription, pilot, one-time) and amount invoiced."

## In the Hollis Voice room

Yes: `03_metrics/customer_mrr_by_month.csv`. It is in the full room and not in the seed drop. Counts below come from [hollis_voice_counts.py](raw/kpi-dashboard-or-metrics-export/hollis_voice_counts.py), output in [hollis_voice_counts_output.txt](raw/kpi-dashboard-or-metrics-export/hollis_voice_counts_output.txt).

- 2,132 rows, 251 customers, 21 months (2025-01 to 2026-09). Columns: `month`, `customer_id`, `customer_name`, `locations`, `plan`, `product_type`, `mrr`, `one_time_fee`, `billings`. Product types: 1,880 subscription rows, 250 onboarding rows, 2 pilot rows.
- The file is clean in shape: no duplicate keys and no gaps inside a customer's paid life.
- 38 of the 250 subscription customers have no revenue in 2026-09. The metrics export has no churn column, so the customer file is the only place this shows.
- **Planted flags it carries:**
  - Pilot booked as ARR (`PF1`): Marlow Veterinary Group, customer C0219, product type Pilot, $15,000 a month in 2026-08 and 2026-09. The subscription rows for 2026-09 add to $171,739. With the pilot the total is $186,739.
  - Customer concentration (`PF5`): Cedar & Pine Animal Hospitals (C0087) pays $36,000 a month, which is 21.0 percent of 2026-09 subscription revenue. The top three are 22.2 percent. The deck says no customer is above 9 percent of ARR.
  - Churn hidden in the cohort tab (`PF3`): rebuilt from this file, the nine 2025 cohorts hold 68 customers with 87.3 percent net and 73.4 percent gross retention at 12 months. The model's tab shows 57 customers and 102.6 percent.
- **Decoys it carries:** all 250 onboarding rows have `mrr` zero and a $500 one-time fee (`DC1`, the fee must not count as ARR). Brookline Row Veterinary pays once a year: in 2026-06 the row shows `mrr` 584 and `billings` 7,008 (`DC2`, the billings spike must not read as revenue).
- No green flag is planted in this file.

## Sources

Fund and firm pages: [Bain Capital Ventures](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/); [a16z, 16 More Startup Metrics](https://a16z.com/16-more-startup-metrics/) and [a16z, data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/); [CRV](https://www.crv.com/content/what-is-a-data-room); [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step); [Malpani Ventures](https://www.malpaniventures.com/blog/due-diligence-data-room).

Vendors and advisers (read as their views): [Peony](https://www.peony.ink/blog/series-a-data-room); [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/); [Eagle Rock CFO](https://www.eaglerockcfo.com/blog/series-a-preparation/data-room-checklist); [Kruze Consulting](https://www.kruzeconsulting.com/what-kind-of-financial-data-should-a-company-prepare-when-seeking-series-a-venture-capital-funding/); [MicroVentures](https://microventures.com/revenue-concentration-risk-when-one-customer-is-too-many), a crowdfunding platform; [HackerNoon, a fractional CFO's post](https://hackernoon.com/the-finance-function-saas-founders-build-too-late).

News: [Fortune](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/).

Saved copies are in [raw/monthly-revenue-by-customer/](raw/monthly-revenue-by-customer/). The Hollis Voice counts script and output are in [raw/kpi-dashboard-or-metrics-export/](raw/kpi-dashboard-or-metrics-export/).
