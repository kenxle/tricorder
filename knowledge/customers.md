# Customers: expert knowledge

Written by the Tricorder team from the [monthly revenue by customer guide](../docs/reports/20261022.03_document_guides/monthly-revenue-by-customer.md), the [customer contracts and order forms guide](../docs/reports/20261022.03_document_guides/customer-contracts-and-order-forms.md), the [customer references and letters of intent guide](../docs/reports/20261022.03_document_guides/customer-references-and-letters-of-intent.md), and [FRAMEWORKS.md](../docs/ongoing/FRAMEWORKS.md) entries 1.6 (customer concentration) and 1.13 (contract terms). The public pages they quote are linked below. This is the team's reading of those sources, not an investor's own input.

This file gives the model an investor's lens on who pays the company, how much each one matters, and what paper holds them. Scripts remain the source of computed figures. Do not invent a benchmark that is not cited here.

## What an expert checks first

A customer count and a logo slide say little until the revenue file and the contracts back them. Before reading a customer claim, establish:

- **Who carries the revenue.** The top one and top three customers' share, from the raw customer file. a16z: "Customer concentration is defined as the revenue of your largest customer or handful of customers relative to total revenue, with both revenues reflecting the same time period." ([16 More Startup Metrics](https://a16z.com/16-more-startup-metrics/))
- **Which revenue the share is measured on.** Recurring plan and contract revenue, usage overage, one-time fees and pilots each give a different share.
- **Who is paying.** Paying accounts, free users, trials and design partners are four different groups. A logo is not a paying customer until the customer file shows revenue for it (monthly revenue by customer guide).
- **What paper holds the largest customers.** Peony: "At Series A, the lead wants the signed contract and may call the customer." ([Peony](https://www.peony.ink/blog/series-a-data-room)) Peony is a data-room vendor.

## Rules

- **Measure concentration on recurring revenue first.** Use the subscription and contract revenue for one month, as FRAMEWORKS.md 1.6 does. a16z keeps variable usage out of ARR: "It should exclude one-time fees, professional service fees, and any variable usage fees." ([16 More Startup Metrics](https://a16z.com/16-more-startup-metrics/)) Then run the share again on total revenue with usage overage in, and label both. A customer with heavy overage can carry more of total revenue than of recurring revenue. When the deck states its figure "of ARR", run it on the model's ARR too (FRAMEWORKS.md 1.6).
- **Group rows that share an owner.** FRAMEWORKS.md 1.6: "A customer with 40 locations is one customer." Splitting one buyer into its sites makes the share look smaller.
- **Count paying customers only.** A customer counts in a month when the customer file shows revenue for it. Free users, free tiers, unpaid design partners and trials go on their own lines. Hustle Fund: "Separate contracted revenue, recognized revenue, pipeline, pilots, letters of intent, and verbal interest." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))
- **Treat design partners as demand, and check which ones pay.** CRV counts them as traction: "Letters of intent (LOIs) with dollar figures attached, design partners testing weekly builds, pilot commitments and pre-orders all count." ([CRV](https://www.crv.com/content/startup-traction)) Traction is not revenue. When a deck counts design partners as paying customers, match each one to the customer file. Signed paper is stronger than a letter. Jake Stein of Common Paper: "The most notable difference from an LOI is that a Design Partner Agreement is binding." ([Common Paper](https://commonpaper.com/blog/what-is-an-loi/))
- **Read the largest customers' contracts for term and exit.** The share matters more when the customer can leave soon. FRAMEWORKS.md 1.6 marks a watch when the largest customer can leave on 90 days notice or less (`short_notice_days`). Entry 1.13 checks that a pilot or a short exit is not counted as a year of ARR.
- **Concentration alone is not the flag.** MicroVentures: "concentration at an early stage is not necessarily a red flag on its own." ([MicroVentures](https://microventures.com/revenue-concentration-risk-when-one-customer-is-too-many)) The flag is a deck claim the customer file contradicts (FRAMEWORKS.md 1.6). A founder who names the concentration and a plan to spread it is a green flag (monthly revenue by customer guide).
- **Mixed models need both views.** When many self-serve accounts sit beside a few enterprise contracts, the contracts usually hold the largest shares. Check that the top ten have signed paper in the room.

## Benchmarks, with their context

- **20 percent from one customer.** MicroVentures: "A commonly referenced threshold in investor due diligence is whether any single customer accounts for more than 20% of a company’s total revenue." ([MicroVentures](https://microventures.com/revenue-concentration-risk-when-one-customer-is-too-many)) It adds that 30 to 40 percent can change valuation or deal terms ([research_data_room.md](../docs/reports/20261022.02_research/research_data_room.md) RF5, paraphrased). MicroVentures is a crowdfunding platform. Tricorder treats 20 percent as a setting (`concentration_line`), not a pass or fail.
- **a16z gives no line.** "As a rule of thumb, we tend to prefer companies with relatively low customer concentration because a business with only one or few customers runs a number of risks." ([16 More Startup Metrics](https://a16z.com/16-more-startup-metrics/)) It names the risks: the customers hold the leverage on price, steer the roadmap, and can force below-market terms.
- **Paid pilots convert often.** Jason Lemkin: "In the companies I work closely with, roughly, the conversions vary fairly widely from about 60% to over 90%." ([SaaStr](https://www.saastr.com/what-is-the-typical-conversion-from-paid-pilot-to-annual-contract-in-b2b-saas-2)) This is one investor's view of paid pilots in B2B SaaS. It says nothing about free ones.

## Stage expectations

- **Seed:** lighter. Hustle Fund lists "Revenue by customer, refunds, churn, gross margin, and concentration where relevant." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)) Visible marks major customer contracts as lighter at seed ([Visible](https://visible.vc/blog/what-to-include-in-your-data-room/)). Free design partners are normal at seed. Counting them as paying is not.
- **Series A:** expected and checked. Peony asks for "Top ~10 customer contracts and any material contract above ~$20,000" ([Peony](https://www.peony.ink/blog/series-a-data-room)). CRV says that at Series A "customer reference calls turn formal" ([CRV](https://www.crv.com/content/what-is-a-data-room)).

## What to ask

- Monthly revenue by customer since the first customer, one row per customer per month, with plan, kind of revenue (subscription, usage, pilot, one-time) and amount invoiced.
- The signed contracts, order forms and amendments for the ten largest customers, and any contract above $20,000.
- A list of free users, free design partners and trials, with start dates and whether each has converted to paid.
- The plan to spread revenue, when one customer is above the line.
- Names of customers to call, including the largest and one who left.

## Sources and boundaries

- Every quote above was checked word for word against saved copies listed in the three guides named at the top ([monthly revenue raw copies](../docs/reports/20261022.03_document_guides/raw/monthly-revenue-by-customer/), [contracts raw copies](../docs/reports/20261022.03_document_guides/raw/customer-contracts-and-order-forms/)). The a16z "rule of thumb" line was checked against the saved copy in [raw/kpi-dashboard-or-metrics-export/](../docs/reports/20261022.03_document_guides/raw/kpi-dashboard-or-metrics-export/).
- Vendors (Peony, Visible) and the crowdfunding platform (MicroVentures) are read as their views.
- Tricorder cannot confirm a customer exists or pays. That takes an invoice, a bank check or a call.
