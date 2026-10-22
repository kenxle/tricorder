# Cohort or retention export

Guide for the data-room document in row 11 of the 30-document table in [the data-room research](../20261022.02_research/research_data_room.md). Written 2026-10-22 from online sources only. Every quote was checked word for word against the page text saved under [raw/cohort-or-retention-export/](raw/cohort-or-retention-export/). The check list is in [quotes_metrics.csv](quotes_metrics.csv).

## What it is

A table that groups customers by the month they started and shows how many of them, or how much of their revenue, is left in each later month. Each row is a cohort. Each column is the number of months since the start. The first column is 100 percent. It may arrive as a tab in the financial model, a CSV, a chart pasted into the deck, or an export from an analytics or billing tool. The founder or a finance or data person prepares it.

Christoph Janz of Point Nine published a simple cohort template for early-stage SaaS startups. In his own words, the table's job is plain: "What you’ll want to see is that younger cohorts are getting better than older cohorts." ([Janz, on Andrew Chen's blog](https://andrewchen.com/the-easiest-spreadsheet-for-churn-mrr-and-cohort-analysis-guest-post/)) A cohort table answers a question no headline number can: whether customers stay.

## At seed and at Series A

- **Pre-seed:** not expected. The research table marks it "N".
- **Seed:** lighter. Visible, a vendor, lets a seed founder leave out a "full cohort analysis if too early" in its stage table ([Visible](https://visible.vc/blog/what-to-include-in-your-data-room/)). Hustle Fund, a venture fund, still lists "Cohort, retention, pipeline, unit-economics, and customer-concentration support." among its seed additions ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)). So a short table with the few cohorts that exist is normal at seed.
- **Series A:** expected, and checked. CRV, a venture fund, says "Investors look hard at cohort retention" at this round ([CRV](https://www.crv.com/content/what-is-a-data-room)). Peony, a data-room vendor, says "If your deck says 130% net revenue retention, they want the cohort export that produces it." ([Peony](https://www.peony.ink/blog/series-a-data-room)) SaaStr's write-up of a Janz talk says "You should have this ready to share before starting the fundraising process." ([SaaStr write-up of the Janz talk](https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital)) Those are the write-up's words about the talk, not Janz's own page.
- **What changes:** at seed the question is "do the first customers stay?" with a handful of cohorts. At Series A the associate rebuilds the cohorts from the revenue-by-customer file and compares them with the export. Visible says diligence teams "will work the room methodically, comparing your cohort retention to your stated net retention, your pipeline coverage to your projected bookings, and your reported headcount to your actual employment agreements." (same Visible page)

## What a first pass checks

In order:

1. **What does the table count?** Customers or revenue. Net or gross. Janz's template runs both. Skok, a venture investor, puts it this way: "There are two ways to run Cohort Analysis: the first looks at the number of customers, and the second looks at the Revenue. Each teaches us something different and valuable." ([David Skok](https://www.forentrepreneurs.com/saas-metrics-2/))
2. **Does each cohort's starting size match the customers who started that month?**
3. **Are all cohorts there, including the newest, and every month?**
4. **Does retention level off?** a16z wants "Stabilization of retention in each cohort after a period such as 6 or 12 months." ([a16z](https://a16z.com/16-more-startup-metrics/))
5. **Do newer cohorts do at least as well as older ones?** a16z: "Newer cohorts performing progressively better than older cohorts." (same a16z page)
6. **Is churn cut by plan, segment and contract size?** Are monthly and annual plans mixed?
7. **Is gross retention shown beside net?**
8. **Does the deck's retention number come out of the table?**
9. **Does usage fall while revenue holds?**

## Green flags

- **Gross and net both shown.** a16z: "Gross churn estimates the actual loss to the business, while net revenue churn understates the losses (as it blends upsells with absolute churn)." ([a16z](https://a16z.com/16-startup-metrics/))
- **Retention that levels off, and newer cohorts that do better.** Both are the a16z tests above. Janz, in his own template notes, adds what the table should show: "after a usually relatively high churn rate in the first lifetime months churn starts to stabilize (because the people who never really adopted the product in the first place are now gone)." ([Janz](https://andrewchen.com/the-easiest-spreadsheet-for-churn-mrr-and-cohort-analysis-guest-post/))
- **MRR churn lower than customer churn.** Janz: "What you’ll want to see is that your MRR churn is lower than your customer churn due to account expansions." (same Janz page)
- **Cuts by segment, with monthly and annual plans kept apart.** SaaStr's write-up of the Janz talk: "Don’t mix monthly and annual plans. If you do this all in one bucket, it doesn’t make sense." And on the best segment: "While a bit of cherry-picking in fundraising is allowed, be transparent and don’t overdo it." ([SaaStr write-up](https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital)) Jason Lemkin of SaaStr says "Break down churn by customer segment, use case, and ACV." ([SaaStr](https://www.saastr.com/dear-saastr-were-at-13m-arr-and-growing-but-our-grr-is-slipping-what-should-we-do/))
- **A usage cohort beside the revenue cohort for an early product.** The write-up says "you should consider having a cohort analysis based on usage indicators like certain activities people do in your software, especially if you’re early." (same SaaStr write-up)
- **The cohort export sits next to the retention number in the deck.** This is the point of Peony's line about a 130 percent claim, above: the associate wants the export that produces the number.

## Red flags and pitfalls

**Common**

- **Net retention only.** See the a16z line above. A strong net figure can sit on top of heavy customer loss. One fractional CFO writes "Blended NRR hides everything. A single big expansion can mask ten quiet churns." ([HackerNoon](https://hackernoon.com/the-finance-function-saas-founders-build-too-late)) This is an adviser's view.
- **Early leavers left out of the starting count.** Janz's note above says early churn is the steep part of the curve. A cohort definition that drops customers who left soon after signing removes that part. This is my reading of Janz's note. The planted flag in the Hollis Voice room works this way.
- **An artificially low starting base.** Bain Capital Ventures: "Too often I see a founder who will, for example, use an artificially low base to calculate their net dollar retention. That never works!" ([Bain Capital Ventures](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/))
- **The best cohorts only.** a16z: "don’t cherry-pick your best cohorts of users. Include the full data" ([a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/)).
- **A blended number that hides weak segments.** Visible: "Aggregate retention numbers that mask underlying segment weakness raise more questions than they settle." ([Visible](https://visible.vc/blog/what-to-include-in-your-data-room/)) The same page lists "Aggregate retention masking cohort weakness." as a common Series A mistake. Visible is a vendor.
- **Gross retention below the usual line.** Lemkin: "But yeah, 88% GRR is a red flag, especially at your scale." ([SaaStr](https://www.saastr.com/dear-saastr-were-at-13m-arr-and-growing-but-our-grr-is-slipping-what-should-we-do/)) And: "Anything below 80% signals churn issues that need fixing before scaling." ([SaaStr](https://www.saastr.com/dear-saastr-what-are-the-top-10-metrics-series-a-investors-look-at/)) Bessemer reports "Looking at gross retention by ARR range, we find that it is relatively consistent at 85-90%." ([Bessemer](https://www.bvp.com/atlas/scaling-to-100-million)) Bessemer adds that it has seen successful SMB-focused companies with 70 to 80 percent. The line is context for the reader, and Tricorder takes it as a setting (`grr_line`).
- **Mixed plan types and mixed segments in one cohort** (the Janz write-up lines above).

**Rare but serious**

- **Stealth churn.** Customers keep paying and use the product far less, so a revenue cohort looks healthy while usage drops. Lemkin writes that "Stealth churn is analog", and describes customers who "pay the same for now" but "use you 40% less". ([SaaStr](https://www.saastr.com/stealth-ai-churn-are-your-customers-starting-to-leave-already/)) The cohort export alone cannot show it. A usage export can.
- **Churn that has not yet shown.** Lemkin: "Churn is a problem that lurks, especially in annual deals. If your churn is too high, a lot of that revenue isn’t even real." ([SaaStr](https://www.saastr.com/every-top-founder-ever-i-should-have-acted-on-bad-trends-earlier/)) A young company with annual contracts may show 100 percent retention simply because no renewal date has passed.
- **A retention claim a customer contradicts.** CRV: "One customer reference that contradicts a retention claim can undo confidence late in diligence." ([CRV](https://www.crv.com/content/what-is-a-data-room)) And: "A claim with nothing behind it invites investors to re-check everything else you’ve said."
- **Very small cohorts.** Tunguz warns that early companies "may not have enough samples" for lifetime value ([Tunguz](https://tomtunguz.com/challenge-of-cac-ltv/), on LTV). The same reasoning applies to a cohort of a handful of customers: one customer moves its percentages a long way.

## How Tricorder checks it

**What a script can check**

Existing check in [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md): `rebuild_cohorts_from_customer_file` (entry 1.3). It rebuilds cohorts from the revenue-by-customer file and compares each cohort's count with the tab, the 12-month net retention (`NRR_12`) with the tab and the deck, and the gross retention (`GRR_12`) with the `grr_line`. It also runs a16z's newer-against-older test.

Proposed new checks:

- `cohort_levels_off`. For each cohort with 12 or more months, compare the average monthly loss in months 1 to 6 with months 7 to 12. Report cohorts where the later loss is not smaller. The 6 and 12 months come from a16z's wording. The method is ours.
- `grr_by_segment`. Compute `GRR_12` by plan, product type and size band (locations), and report any segment under `grr_line`. The segment cut follows Lemkin's and Janz's advice.
- `cohort_plan_mix`. Report cohorts that blend customers on different billing terms, using the billings pattern (a single large yearly invoice marks an annual payer).
- `cohort_size_floor`. Mark any cohort under a set count as "too small to read" so the readout does not draw a trend from it. The count is a setting for the team.
- `usage_vs_revenue_retention`. When the room holds per-customer usage, compare the usage cohort with the revenue cohort. Without usage data, the check returns a gap.

**What needs a model to read, and what it must quote**

- The definition of a cohort: the header, the note, the footnote. Quote it. Then say, starting the text with "Reading:", which customers it leaves out.
- Whether a chart in the deck is net, gross or unlabeled. Quote the label. If the chart is only an image, set the confidence to "judged".
- Whether the deck's chart shows every cohort the tab holds.

**What Tricorder cannot check, so the operator does**

- Whether customers say they stay. That is a customer reference call, which CRV says turns formal at Series A.
- Per-customer usage, if the room does not hold it. Ask the founder.
- A set of cohorts that is consistent across every file but invented. Tricorder finds differences in reporting, not fraud.

## Which readout pieces it feeds

- **Retention** (main). **Traction and revenue** through the revenue-weighted cohort.
- Checklist items: C14 (the cohort or retention export itself), C15 (gross and net retention rebuilt from revenue by customer and compared with the deck), C16 (newer cohorts do at least as well as older ones), C17 (no cohorts or periods left out, and enough months of history), C18 (customers who keep paying but use the product far less).

## If it is missing

- **Pre-seed:** not a gap.
- **Seed:** a gap, lighter, not a red flag. If the room holds the customer file, Tricorder rebuilds the cohorts itself and the export is not missed.
- **Series A:** a gap if the customer file is also absent. Then the retention piece reads "not enough in the room". It is a red flag when the deck states a retention number and the room holds nothing behind it. CRV: "A claim with nothing behind it invites investors to re-check everything else you’ve said." (same CRV page)
- **Ask-list line:** "Send monthly revenue by customer so we can rebuild retention, plus the cohort export behind the deck's retention number and a one-line definition of a cohort."

## In the Hollis Voice room

Partly. There is no separate cohort file. The cohort export is the `Cohorts` tab of `02_financials/financial_model.xlsx` (in the seed drop), and slide 6 of the deck shows it as a chart with a caption. The customer file that lets Tricorder rebuild it is in the full room only. Counts below come from [hollis_voice_counts.py](raw/kpi-dashboard-or-metrics-export/hollis_voice_counts.py), output in [hollis_voice_counts_output.txt](raw/kpi-dashboard-or-metrics-export/hollis_voice_counts_output.txt).

- **Planted flag: churn hidden in the cohort tab (`PF3`).** The tab's note in cell A2 reads "Cohort = customers still active after onboarding". The deck caption says the same. The tab shows 57 customers and 102.6 percent net retention at 12 months. Rebuilt from the customer file, the same nine cohorts (2025-01 to 2025-09) hold 68 customers, with 87.3 percent net and 73.4 percent gross retention. Eleven customers were dropped. Gross retention is below the 80 percent `grr_line`. My script reproduces the key's numbers.
- The tab shows net retention only. Gross retention appears nowhere in the room.
- The cohorts are small: 5 to 11 customers each in the rebuilt version, from the script.
- No usage data per customer is in the room, so stealth churn cannot be checked there.
- Catch: not from the seed drop alone. The check needs the customer file, which is in the full room.

## Sources

Fund and firm pages: [a16z, 16 Startup Metrics](https://a16z.com/16-startup-metrics/); [a16z, 16 More Startup Metrics](https://a16z.com/16-more-startup-metrics/); [a16z, data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/); [Bessemer, Scaling to $100 Million](https://www.bvp.com/atlas/scaling-to-100-million); [Bain Capital Ventures](https://baincapitalventures.com/insight/preparing-for-investor-due-diligence-as-part-of-fundraise-process-with-data-room-checklist/); [CRV](https://www.crv.com/content/what-is-a-data-room); [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step); [Christoph Janz, on Andrew Chen's blog](https://andrewchen.com/the-easiest-spreadsheet-for-churn-mrr-and-cohort-analysis-guest-post/); [SaaStr write-up of the Janz talk](https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital); [David Skok, SaaS Metrics 2.0](https://www.forentrepreneurs.com/saas-metrics-2/); Jason Lemkin on SaaStr: [GRR](https://www.saastr.com/dear-saastr-were-at-13m-arr-and-growing-but-our-grr-is-slipping-what-should-we-do/), [top ten metrics](https://www.saastr.com/dear-saastr-what-are-the-top-10-metrics-series-a-investors-look-at/), [stealth churn](https://www.saastr.com/stealth-ai-churn-are-your-customers-starting-to-leave-already/), [acting on bad trends](https://www.saastr.com/every-top-founder-ever-i-should-have-acted-on-bad-trends-earlier/); [Tomasz Tunguz](https://tomtunguz.com/challenge-of-cac-ltv/).

Vendors and advisers (read as their views): [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/); [Peony](https://www.peony.ink/blog/series-a-data-room); [HackerNoon, a fractional CFO's post](https://hackernoon.com/the-finance-function-saas-founders-build-too-late).

Saved copies are in [raw/cohort-or-retention-export/](raw/cohort-or-retention-export/). The Hollis Voice counts script and output are in [raw/kpi-dashboard-or-metrics-export/](raw/kpi-dashboard-or-metrics-export/).
