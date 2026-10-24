# Retention: expert knowledge

Written by the Tricorder team from the [cohort or retention export guide](../docs/reports/20261022.03_document_guides/cohort-or-retention-export.md), the [monthly revenue by customer guide](../docs/reports/20261022.03_document_guides/monthly-revenue-by-customer.md), and [FRAMEWORKS.md](../docs/ongoing/FRAMEWORKS.md) entry 1.3 (cohort retention rebuild). The public pages they quote are linked below. This is the team's reading of those sources, not Kimmy's expert input.

This file gives the model an investor's lens on whether customers stay. Scripts remain the source of computed figures. Do not invent a benchmark that is not cited here.

## What an expert checks first

Retention answers a question no headline number can: do customers stay, and do they spend more over time? Before reading a retention figure, establish:

- **What it counts.** Customers or revenue, net or gross. David Skok: "There are two ways to run Cohort Analysis: the first looks at the number of customers, and the second looks at the Revenue. Each teaches us something different and valuable." ([SaaS Metrics 2.0](https://www.forentrepreneurs.com/saas-metrics-2/))
- **Who is in the starting count.** Each cohort's starting size should match the customers who started paying that month. A definition that drops customers who left soon after signing removes the steepest part of the curve.
- **How long the record is.** A cohort needs 12 months to give a 12-month figure. A few months of history is a short record, and a handful of customers moves the percentages a long way.
- **Where the number comes from.** The deck's retention number should come out of a table the room holds. Peony: "If your deck says 130% net revenue retention, they want the cohort export that produces it." ([Peony](https://www.peony.ink/blog/series-a-data-room))

## Rules

- **Show gross beside net.** Net retention blends upsells with loss. a16z: "Gross churn estimates the actual loss to the business, while net revenue churn understates the losses (as it blends upsells with absolute churn)." ([16 Startup Metrics](https://a16z.com/16-startup-metrics/))
- **Rebuild from the customer file.** Rebuild cohorts from monthly revenue by customer and compare them with the deck and the model. Use the raw file as it is: never drop, add or adjust a customer (FRAMEWORKS.md 1.3).
- **Look for two trends.** a16z wants "Stabilization of retention in each cohort after a period such as 6 or 12 months" and "Newer cohorts performing progressively better than older cohorts." ([16 More Startup Metrics](https://a16z.com/16-more-startup-metrics/))
- **Keep plan types apart.** Monthly and annual plans churn differently. A blended number can hide a weak segment.
- **A stated churn rate needs a source.** An assumption in the model that no customer file supports is a claim, not evidence. Ask what it counts and where it comes from.
- **Watch for churn that has not shown yet.** Annual contracts show no loss until a renewal date passes. Jason Lemkin: "Churn is a problem that lurks, especially in annual deals." ([SaaStr](https://www.saastr.com/every-top-founder-ever-i-should-have-acted-on-bad-trends-earlier/))

## Benchmarks, with their context

- **Gross retention under 80 percent.** Lemkin: "Anything below 80% signals churn issues that need fixing before scaling." ([SaaStr, top Series A metrics](https://www.saastr.com/dear-saastr-what-are-the-top-10-metrics-series-a-investors-look-at/)) This is one investor's line, written for SaaS at Series A. Tricorder treats it as a setting (`grr_line`), not a pass or fail.
- **Gross retention of 85 to 90 percent is typical in Bessemer's data.** Bessemer: "Looking at gross retention by ARR range, we find that it is relatively consistent at 85-90%." ([Scaling to $100 Million](https://www.bvp.com/atlas/scaling-to-100-million)) Bessemer adds that it has seen successful SMB-focused companies at 70 to 80 percent. Read the line against the customer segment.
- **Revenue retention above customer retention is good.** Christoph Janz: "What you'll want to see is that your MRR churn is lower than your customer churn due to account expansions." ([Janz, on Andrew Chen's blog](https://andrewchen.com/the-easiest-spreadsheet-for-churn-mrr-and-cohort-analysis-guest-post/))
- **A monthly churn rate compounds.** A monthly rate carried over 12 months gives the share of customers left after a year. This is arithmetic, done by a script, not a benchmark.

## Stage expectations

- **Seed:** lighter. A short table with the few cohorts that exist is normal. Visible lets a seed founder leave out a "full cohort analysis if too early" ([Visible](https://visible.vc/blog/what-to-include-in-your-data-room/)). If the room holds the customer file, rebuild the cohorts from it.
- **Series A:** expected and checked. CRV: "Investors look hard at cohort retention" ([CRV](https://www.crv.com/content/what-is-a-data-room)). A retention claim with nothing behind it is a red flag at this stage.

## What to ask

- Monthly revenue by customer from the first paying month, so retention can be rebuilt.
- The cohort export behind any retention number in the deck, with a one-line definition of a cohort.
- Gross retention beside net retention.
- Where the model's churn assumption comes from, and whether it counts customers or revenue.
- Churn split by plan or customer size, with monthly and annual plans apart.

## Sources and boundaries

- Every quote above was checked word for word against saved copies listed in the [cohort or retention export guide](../docs/reports/20261022.03_document_guides/cohort-or-retention-export.md) ([raw copies](../docs/reports/20261022.03_document_guides/raw/cohort-or-retention-export/)).
- Vendors (Visible, Peony) are read as their views.
- The 80 percent line and the 85 to 90 percent range are context for the reader. Do not apply them to a company outside SaaS without saying so.
