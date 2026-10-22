# Unit economics (CAC, LTV, payback)

Guide for the data-room document in row 12 of the 30-document table in [the data-room research](../20261022.02_research/research_data_room.md). Written 2026-10-22 from online sources only. Every quote was checked word for word against the page text saved under [raw/unit-economics/](raw/unit-economics/). The check list is in [quotes_metrics.csv](quotes_metrics.csv).

## What it is

A set of numbers that say whether the company makes money on the average customer after paying to win and serve them:

- **CAC** (customer acquisition cost): what it costs to win one new paying customer.
- **Payback**: how many months of gross profit from that customer repay the CAC.
- **LTV** (lifetime value): the profit a customer brings over the time they stay.
- **LTV to CAC**: the ratio of the two.

It arrives as one slide in the deck, a tab in the financial model, or a standalone sheet. The founder or finance lead prepares it. Some founders split it by channel or by customer size.

Bessemer says "Sales efficiency is capital efficiency" and picks CAC payback as its main measure. It defines the measure this way: "CAC payback is the rate at which the costs spent to acquire a customer are repaid by that customer, and it usually includes sales, marketing, and customer success expenses (at least the portion that ties to renewal/upsell/cross-sell)." ([Bessemer](https://www.bvp.com/atlas/scaling-to-100-million))

## At seed and at Series A

- **Pre-seed:** not expected. The research table marks it "N".
- **Seed:** lighter, and an honest "we cannot measure this yet" is fine. Hustle Fund, a venture fund, says to "Compare customer acquisition cost (CAC), gross margin, payback, and lifetime value only when the data is mature enough to support them." Its list of acceptable uncertainty includes "Unit economics are immature, and the team knows what it can and cannot measure." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)) Tomasz Tunguz of Theory Ventures goes further. Of LTV to CAC he says "But this figure is often meaningless for early stage startups." ([Tunguz, 2017](https://tomtunguz.com/challenge-of-cac-ltv/)) And: "In the early stages, payback period is a better metric to use." (same page)
- **Series A:** expected, and rebuilt. Peony, a data-room vendor, lists "A built financial/operating model with unit economics" with CAC, LTV and payback "the associate can rebuild" in its Series A room ([Peony](https://www.peony.ink/blog/series-a-data-room)). Bain Capital Ventures lists "Unit economics (e.g., LTV/CAC over time, payback period, CAC by channel)" in a full growth-stage request, and says its first look pairs the revenue-by-customer file with the P&L: "Comparing that with the sales and marketing spend from the P&L gives us an idea of how efficiently the company is able to acquire these customers and grow the business." ([Bain Capital Ventures](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/)) Kruze Consulting, an accounting firm, lists "CAC (customer acquisition costs - they may have a particular way they want to see this)" among common financial requests ([Kruze](https://www.kruzeconsulting.com/what-kind-of-financial-data-should-a-company-prepare-when-seeking-series-a-venture-capital-funding/)).
- **Why payback leads at both stages:** Tunguz says LTV needs years of customer behavior, while within 14 to 18 months most startups have real payback data (Tunguz 2017, above).

## What a first pass checks

In order:

1. **What went into CAC?** Ads only, or sales and marketing payroll too? Which months?
2. **Who counts as a new customer?** All new paying customers, or only those won through paid channels?
3. **Which margin is used?** None, the deck's gross margin, or a rebuilt one. a16z says "all costs associated with the manufacturing, delivery, and support of a product/service should be included" in gross profit ([a16z](https://a16z.com/16-startup-metrics/)).
4. **Where does the churn in LTV come from?** Observed customers lost, or an assumed rate.
5. **Is payback measured on gross profit, in months?**
6. **Is it split by channel, segment or plan?**
7. **Does the sales and marketing spend tie to the P&L and the expense ledger?**
8. **Is the support cost counted once, either in cost of revenue or in CAC, but not both and not neither?**

## Green flags

- **The CAC method is written down.** SaaStr's write-up of a talk by Christoph Janz of Point Nine: "Make it clear how you’ve calculated your CACs." ([SaaStr write-up of the Janz talk](https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital)) These are the write-up's words about the talk, not Janz's own page.
- **Payback on gross margin.** Tunguz: "It is amount of time a customer repays the cost of customer acquisition with gross profit dollars." ([Tunguz, 2020](https://www.tomtunguz.com/payback_period_2020/index.md)) Bessemer: "We also measure CAC payback against gross margin-adjusted ARR given that the variable costs associated with selling a cloud software product do not accrete to profit." ([Bessemer](https://www.bvp.com/atlas/scaling-to-100-million))
- **One channel that clearly works.** "Investors want to see one channel or source that’s clearly working and seems efficient and scalable." (SaaStr write-up of the Janz talk)
- **Paid and blended CAC both shown.** a16z: "While blended CAC [total acquisition cost / total new customers acquired across all channels] isn’t wrong, it doesn’t inform how well your paid campaigns are working and whether they’re profitable." ([a16z](https://a16z.com/16-startup-metrics/)) The same page says many investors like seeing both.
- **A cut by segment.** Skok, a venture investor, says early-stage companies test several kinds of customers and it is "very useful" to see which show the quickest return ([Skok](https://www.forentrepreneurs.com/saas-metrics-2/)). Bessemer sets different payback targets by segment, quoted below.
- **LTV measured on real months, not guessed.** a16z: "Note, if you have only few months of data, the conservative way to measure LTV is to look at historical value to date." ([a16z](https://a16z.com/16-startup-metrics/))
- **The founder says what is immature.** Hustle Fund's line above.
- **An adjustment that is disclosed.** SaaStr's write-up of the Janz talk: "Exclude some initial startup or buildup costs in the budget if it makes sense because you’re estimating the cost to acquire the next customer, which might be lower than the first ones when you had nothing. Be transparent and explain it." Skok makes the same point: "I suggest doing a very simple adjustment to the Sales & Marketing expenses to take only a portion of those salaries and expenses in the early days." ([Skok, definitions](https://www.forentrepreneurs.com/saas-metrics-2-definitions/)) An adjustment is a green flag only when it is stated. Left silent, it becomes a red flag.

## Red flags and pitfalls

**Common**

- **LTV built on revenue, not profit.** a16z: "A common mistake is to estimate the LTV as a present value of revenue or even gross margin of the customer instead of calculating it as net profit of the customer over the life of the relationship." ([a16z](https://a16z.com/16-startup-metrics/))
- **CAC that leaves costs out.** a16z: "One common problem with CAC metrics is failing to include all the costs incurred in user acquisition such as referral fees, credits, or discounts." (same a16z page) a16z's own definition: "Customer acquisition cost or CAC should be the full cost of acquiring users, stated on a per user basis."
- **Blended CAC that hides a weak paid channel.** See the a16z line above. One fractional CFO writing on HackerNoon says of blended payback "A blended number averages all of that away." ([HackerNoon](https://hackernoon.com/the-finance-function-saas-founders-build-too-late)) This is an adviser's view.
- **An inflated gross margin.** If delivery costs sit under R&D or sales, the margin used in LTV and payback is too high. Tunguz lists what cost of revenue holds: "This includes web hosting, software licensing fees for software embedded into the product like databases, and the customer success initiatives to on-board and retain customers." ([Tunguz](https://tomtunguz.com/not-all-revenue-dollars-are-created-equal/)) The room's gross margin scan (entry 1.7) catches this at the source.
- **Optimism about acquisition cost.** Skok: "Entrepreneurs are usually overoptimistic about how much it costs to acquire a customer." ([Skok](https://www.forentrepreneurs.com/saas-metrics-2/))
- **LTV from an assumed churn rate and a few months of data.** Tunguz: "Last, most early stage companies may not have enough samples to calculate LTV with statistical significance." (Tunguz 2017, above)
- **The ratio used as a spend trigger.** Tunguz: "If the ratio is greater than 3x, then it’s time to spend more." He says this links today's spend to forecast cash flows that are hard to calculate.
- **Benchmarks that disagree.** The sources do not agree on a good payback, so none is a test. Lemkin: "Your customer acquisition cost (CAC) payback period should be 12 months or less." ([SaaStr](https://www.saastr.com/dear-saastr-what-are-the-top-10-metrics-series-a-investors-look-at/)) Bessemer: "What we find is that the average CAC payback in the $1-10MM ARR bucket is 15 months" and "For cloud companies selling into SMB-focused accounts, you should target CAC payback <12 months; for mid-market-focused accounts, target CAC payback <18 months; and for enterprise-focused accounts, target <24 months." ([Bessemer](https://www.bvp.com/atlas/scaling-to-100-million)) Skok: "it is quite common to see very healthy SaaS businesses taking around 20 months to recover CAC." ([Skok, definitions](https://www.forentrepreneurs.com/saas-metrics-2-definitions/)) Tunguz, on public software companies in 2020: "The top quartile is 15 months; the median is 22 months; and the bottom quartile is 29 months." (Tunguz 2020, above) Tunguz in 2015 put the median SaaS startup at 15 months on gross margin ([Tunguz, 2015](https://tomtunguz.com/payback_period_cash/index.md)). An adviser on HackerNoon, citing a 2026 Benchmarkit report, writes that "the median B2B SaaS company took 16 months to earn back what it spent to acquire a customer" ([HackerNoon](https://hackernoon.com/the-finance-function-saas-founders-build-too-late)). Peony's table of commonly cited Series A guidance lists about 15 months of payback at $1 to $10 million of ARR and LTV to CAC of about 3 to 1 or better, and says these are "guidance, not pass/fail lines" ([Peony](https://www.peony.ink/blog/series-a-data-room)). For LTV to CAC, Bessemer says "We recommend investing in customer acquisition when CLTV / CACs are 3x+" and Skok says "The best SaaS businesses have a LTV to CAC ratio that is higher than 3, sometimes as high as 7 or 8." Tricorder shows these as context for the reader and never as a pass or fail line.

**Rare but serious**

- **The same support cost in neither place.** Support staff booked outside both cost of revenue and CAC makes both look better. Entry 1.9 asks that the cost be counted once.
- **Sales and marketing spend that does not tie to the ledger or the P&L.** The ledger shows contractors or program spend the P&L does not. See the contractors and capitalised-costs checks in entry 1.12.
- **A refusal to say how the numbers were built.** Peony's line that the associate wants to rebuild CAC, LTV and payback sets the expectation; the opposite of rebuildable is a reason to ask.

## How Tricorder checks it

**What a script can check**

The existing entry is "Unit economics recompute" (entry 1.9) in [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md). Its formulas:

```
ARPA           = MRR ÷ paying accounts, at the as-of month
CAC            = sales and marketing spend in a period ÷ new paying customers in that period
payback_months = CAC ÷ (ARPA × gross_margin_rebuilt)
LTV            = ARPA × gross_margin_rebuilt ÷ monthly logo churn rate
```

When entry 1.7 moves support staff out of S&M and into cost of revenue, the same cost comes out of the S&M used for CAC. Entry 1.9 gives no check name of its own; its framework value is `unit_economics`. Related existing checks: `gross_margin_from_ledger` (entry 1.7) and `rebuild_cohorts_from_customer_file` (entry 1.3, for churn).

Proposed named checks inside entry 1.9:

- `cac_payback_from_spend_and_new_customers`. The formulas above, computed for the trailing six months and for the full history by quarter. The window is a setting.
- `cac_cost_scope`. Lists which P&L and ledger lines went into the S&M figure, and flags any line moved between cost of revenue and S&M by another check.
- `sm_spend_ties_to_ledger`. Monthly S&M in the P&L against the ledger lines booked as sales and marketing, flagged above `match_tolerance`.
- `payback_by_segment`. Payback and gross-margin-adjusted payback by plan or size band, using the customer file.
- `ltv_observed_vs_assumed`. Compares the churn rate in the deck's LTV with the monthly logo churn seen in the customer file.

**What needs a model to read, and what it must quote**

- How the deck defines CAC, LTV and payback. Quote the definition or the footnote.
- Whether the CAC is blended or split by channel. Quote what says so.
- Which margin the LTV uses. Quote the number and its label.
- Which sales and marketing lines are paid acquisition, which are staff and which are unclear. Quote the ledger line.

**What Tricorder cannot check, so the operator does**

- Channel-level spend and lead sources that live in ad accounts or the CRM. Ask the founder for the export.
- Whether early "buildup" costs were fairly left out. That is a judgment call for the partner, with the founder's reasons in hand.
- Customer lifetime beyond the history in the room.
- Any set of numbers that is consistent everywhere but invented. Tricorder finds differences in reporting, not fraud.

## Which readout pieces it feeds

- **Unit economics** (main). Its spend side also touches **burn and runway**.
- Checklist items: C30 (unit economics as a document), C31 (gross margin rebuilt with every delivery cost), C32 (CAC, payback and LTV recomputed from spend and customer counts), C33 (blended CAC does not hide weak paid channels).

## If it is missing

- **Pre-seed:** not a gap.
- **Seed:** not a red flag. A gap only if the deck states a CAC, LTV or payback and the room holds nothing behind it.
- **Series A:** a gap that leaves the unit economics piece at "not enough in the room". If the deck states a ratio and the room holds no inputs, that is a claim with nothing behind it, which CRV says "invites investors to re-check everything else you’ve said." ([CRV](https://www.crv.com/content/what-is-a-data-room))
- **Ask-list line:** "Send monthly sales and marketing spend by line and channel, new paying customers by month and by source, and how the deck defines CAC, LTV and payback."

## In the Hollis Voice room

There is no unit-economics document. Slide 5 of the deck is titled "Unit economics" and holds one number, an 80 percent gross margin, with the line "Plans start at $349 a month". The deck states no CAC, LTV or payback. Entry 1.9 therefore adds the gap "Not in the room: CAC, payback or LTV in the deck". Counts below come from [hollis_voice_counts.py](raw/kpi-dashboard-or-metrics-export/hollis_voice_counts.py), output in [hollis_voice_counts_output.txt](raw/kpi-dashboard-or-metrics-export/hollis_voice_counts_output.txt).

- **Planted flag upstream:** the gross margin is 80 percent in the deck and the model, and 58.1 percent when hosting, inference and support are included (`PF6`). That moves every margin-based number here.
- **The inputs exist** for a rebuild: the P&L's three sales and marketing lines and the customer file's first paid month for each customer. The expense ledger books sales and marketing only as payroll and support staff, and the customer file has no lead-source field. Nothing splits spend or customers by channel, so CAC by channel is a gap.
- **A worked example from my script**, not the output of entry 1.9, which FRAMEWORKS says is built later. Window: 2026-04 to 2026-09. New paying customers: 101. Revenue per account in 2026-09: $810.09 a month ($171,739 of subscription MRR over 212 accounts).

| Reading | Spend used | CAC | Margin | Payback |
|---|---|---|---|---|
| The deck's world | all three S&M lines, $574,342 | $5,687 | 80% | 8.8 months |
| The rebuilt world | support specialists moved to cost of revenue, $452,560 | $4,481 | 58.1% | 9.5 months |
| Mixed, which counts support twice | all three lines, $574,342 | $5,687 | 58.1% | 12.1 months |

The mixed row is the mistake entry 1.9 warns about. The two consistent readings are close here (8.8 and 9.5 months), so the unit economics piece reads on how the founder defines things more than on the arithmetic. The check should show the table so the operator can see which lines moved.

## Sources

Fund and firm pages: [Bessemer, Scaling to $100 Million](https://www.bvp.com/atlas/scaling-to-100-million); [a16z, 16 Startup Metrics](https://a16z.com/16-startup-metrics/); [Bain Capital Ventures](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/); [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step); [CRV](https://www.crv.com/content/what-is-a-data-room); [Tomasz Tunguz: the false confidence of LTV/CAC](https://tomtunguz.com/challenge-of-cac-ltv/), [best-in-class payback in 2020](https://www.tomtunguz.com/payback_period_2020/index.md), [payback and working capital](https://tomtunguz.com/payback_period_cash/index.md), [what counts as cost of revenue](https://tomtunguz.com/not-all-revenue-dollars-are-created-equal/); [David Skok, SaaS Metrics 2.0](https://www.forentrepreneurs.com/saas-metrics-2/) and [its definitions page](https://www.forentrepreneurs.com/saas-metrics-2-definitions/); [Jason Lemkin, SaaStr top ten metrics](https://www.saastr.com/dear-saastr-what-are-the-top-10-metrics-series-a-investors-look-at/); [SaaStr write-up of the Janz talk](https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital).

Vendors and advisers (read as their views): [Peony](https://www.peony.ink/blog/series-a-data-room); [Kruze Consulting](https://www.kruzeconsulting.com/what-kind-of-financial-data-should-a-company-prepare-when-seeking-series-a-venture-capital-funding/); [HackerNoon, a fractional CFO's post](https://hackernoon.com/the-finance-function-saas-founders-build-too-late).

Saved copies are in [raw/unit-economics/](raw/unit-economics/). The Hollis Voice counts script and output are in [raw/kpi-dashboard-or-metrics-export/](raw/kpi-dashboard-or-metrics-export/).
