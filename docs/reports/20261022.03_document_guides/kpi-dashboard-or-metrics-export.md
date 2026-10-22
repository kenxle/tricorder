# KPI dashboard or metrics export (MRR, ARR, customers, churn)

Guide for the data-room document in row 9 of the 30-document table in [the data-room research](../20261022.02_research/research_data_room.md). Written 2026-10-22 from online sources only. Every quote was checked word for word against the page text saved under [raw/kpi-dashboard-or-metrics-export/](raw/kpi-dashboard-or-metrics-export/). The check list is in [quotes_metrics.csv](quotes_metrics.csv).

## What it is

A short table of company-level numbers by month: monthly recurring revenue (MRR), annual recurring revenue (ARR), paying customers, churn, and often cash and burn. The founder or the finance lead prepares it. It arrives as a spreadsheet or CSV, sometimes as a PDF or a screenshot from a billing or reporting tool.

Two plain definitions help. Lighter Capital, a lender, says "Monthly recurring revenue is the sum total of all revenue your company reliably earns every month from ongoing customer contracts and subscriptions." ([Lighter Capital](https://www.lightercapital.com/blog/four-metrics-to-track-when-raising-capital-for-your-saas-company)) Bessemer, a venture fund, says "ARR gives full credit for the annualized recurring contract and nets out non-recurring revenue." ([Bessemer](https://www.bvp.com/atlas/scaling-to-100-million))

It is the document a partner reads first after the deck, because it holds the same headline numbers in a form that can be checked. Visible, a vendor that sells investor-update software, calls it the most overlooked file: "The most overlooked sub-document at every stage is the metrics dashboard or KPI summary." ([Visible](https://visible.vc/blog/what-to-include-in-your-data-room/))

## At seed and at Series A

- **Pre-seed:** lighter. The research table marks it "L", a lighter version only if you have it.
- **Seed:** expected. Visible says "Seed founders add 6 to 18 months of historical financials and an early KPI dashboard." ([Visible](https://visible.vc/blog/what-to-include-in-your-data-room/)) The same page says this is where "investors start checking whether the numbers in your deck match the numbers in your room."
- **Series A:** expected, and checked against raw data. Peony, a data-room vendor, says the lead's associate builds a model from your raw data, so the dashboard has to sit beside its sources. Peony adds that "a dashboard alone invites the question “where does this come from?”" ([Peony](https://www.peony.ink/blog/series-a-data-room)) CRV, a venture fund, says "Your metrics file does more work than any other file at this round, and definitions that shift between documents cost you credibility." ([CRV](https://www.crv.com/content/what-is-a-data-room))
- **How deep the first look goes:** Jason Lemkin of SaaStr says pre-term-sheet diligence on a seed or Series A deal usually holds "Basic financials and model review. But often only a cursory one." ([SaaStr](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet)) The deep check comes after the term sheet: "Bank statements & deep financial review. To make sure whatever you have is true." (same page). The associate's first pass is the cursory one, so the export has to read clearly without a call.
- **How long a history:** SaaStr's write-up of a talk by Christoph Janz of Point Nine says the KPI sheet reaches back about two years or to launch, and runs month by month for early or product-led companies and quarter by quarter for slower enterprise sales ([SaaStr write-up of the Janz talk](https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital)). Those are the write-up's words about Janz's talk, not Janz's own page.

## What a first pass checks

In order:

1. **Does the run of months have gaps?** From the first revenue month to the as-of month, one row per month.
2. **What does each label mean?** Is ARR twelve times a recurring MRR, and does MRR hold subscription lines only?
3. **Does the deck's headline number equal the export's last row?**
4. **Is churn shown, and is it gross or net?** Does the export split MRR movement into new, expansion, contraction and churn?
5. **Is the customer count paying customers, or a cumulative count of sign-ups?**
6. **Do the monthly totals tie to the P&L revenue line and to the revenue-by-customer file?**
7. **Do definitions stay the same from month to month, in the deck and in the investor updates?**
8. **Is any jump explained?** SaaStr's write-up of the Janz talk says "Any big changes or sudden improvements are suspicious, so explain them well and make it easy for investors to connect the dots." ([SaaStr write-up](https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital))

## Green flags

- **A movement table.** New, expansion, contraction and churn that add up to the change in MRR. SaaStr's write-up of the Janz talk says "One thing to include for SaaS is what’s called the MRR or ARR movement." ([SaaStr write-up](https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital)) Eagle Rock CFO, an accounting firm, lists "Detailed MRR/ARR rollforward showing additions, churn, expansion, and contraction." ([Eagle Rock CFO](https://www.eaglerockcfo.com/blog/series-a-preparation/data-room-checklist))
- **One logic for history and plan.** "You don’t want to use a different model or logic for projections and historic numbers." ([SaaStr write-up](https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital))
- **Short enough to read at once.** "An investor needs to be able to digest it in half an hour" ([SaaStr write-up](https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital)).
- **A written definition and a dated source for each headline number.** Hustle Fund, a venture fund, tells its angels to "Reconcile headline metrics to a dated source and a clear definition." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))
- **Contracted, recognized and pilot revenue kept apart.** "Separate contracted revenue, recognized revenue, pipeline, pilots, letters of intent, and verbal interest." (same Hustle Fund page)
- **Gross and net churn both shown.** a16z says "Gross churn estimates the actual loss to the business, while net revenue churn understates the losses (as it blends upsells with absolute churn)." ([a16z](https://a16z.com/16-startup-metrics/))
- **The dashboard sits next to its sources and matches the investor updates.** Visible says "When the same numbers appear in both your data room dashboard and your monthly update, the two reinforce each other instead of competing for an investor's attention." ([Visible](https://visible.vc/blog/what-to-include-in-your-data-room/)) This is a vendor view.

## Red flags and pitfalls

**Common**

- **ARR is a run rate, not recurring revenue.** a16z: "Often, people will multiply one month’s all-in bookings by 12 to get to ARR." ([a16z](https://a16z.com/16-startup-metrics/)) And: "It should exclude one-time fees, professional service fees, and any variable usage fees." ([a16z](https://a16z.com/16-more-startup-metrics/))
- **Pilots, one-time deals and unactivated contracts counted as recurring.** Fortune reports that six VCs said founders are "counting pilots, one-time deals, or unactivated contracts as recurring revenue". ([Fortune](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/)) One early-stage VC told Fortune "Companies are signing contracts with kill provisions, so they’re claiming booked ARR, but giving their customers an out," (same article). One early-stage VC described a defense-tech startup whose founder claimed $325,000 of ARR that turned out to come from a two-week pilot (same article). This is news reporting, and the VCs are not named.
- **Signed but not yet live contracts mixed into ARR.** Bessemer keeps a separate measure for them: "CARR (Committed ARR) builds on the ARR concept by adding committed but not yet live contract values to total ARR and netting out forecasted churn or downsell." ([Bessemer](https://www.bvp.com/atlas/scaling-to-100-million)) A dashboard that labels this number ARR is mislabelled.
- **Letters of intent and talk counted as revenue.** "Letters of intent and verbal agreements are neither revenue nor bookings." ([a16z](https://a16z.com/16-startup-metrics/))
- **GAAP revenue stretched into MRR.** Baker Tilly, an accounting firm that sells SaaS finance services, says "many companies make the mistake of utilizing monthly GAAP recognized revenue as the basis for MRR and then extrapolating that value to report ARR." ([Baker Tilly](https://www.bakertilly.com/insights/your-arr-is-probably-wrong-and-could-be-costing-you))
- **A cumulative count shown as a live one.** "Cumulative charts by definition always go up and to the right for any business that is showing any kind of activity." ([a16z](https://a16z.com/16-startup-metrics/)) a16z also prefers active users to registered users for this reason ([a16z](https://a16z.com/16-more-startup-metrics/)).
- **Net churn only.** See the a16z line above on net churn understating the loss.
- **Short or broken history.** a16z's data-room guide lists "Limited historical financials" and gives the example "you only show three months of data when your company is three years old, or you show quarterly but not monthly revenue." ([a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/)) It also lists "Numbers that aren’t consistent across tabs or spreadsheets".
- **Odd metric names.** Lemkin: "Weird metrics like “Quarterly MRR” or odd ways to describe revenue are immediate flags." ([SaaStr](https://www.saastr.com/as-a-venture-capitalist-what-are-some-red-flags-that-would-make-you-reject-a-startup-immediately))
- **No shared definition of ARR.** Moran Chamsi, writing in Ctech after the Joonko fraud case, says "In fact, today, every company calculates its own ARR in the absence of a uniform standard." ([Ctech](https://calcalistech.com/ctechnews/article/b1jfcymt3)) So the definition on the page matters more than the number.
- **Deck and dashboard disagree.** "A mismatch between dashboard numbers and deck numbers is one of the fastest ways to lose credibility inside a folder you control completely." ([Visible](https://visible.vc/blog/what-to-include-in-your-data-room/)) CRV: "Your annual recurring revenue (ARR) in the deck should reconcile to the underlying billing, contract and revenue schedules." ([CRV](https://www.crv.com/content/what-is-a-data-room))

**Rare but serious**

- **Revenue held up by billings.** a16z warns that a company can show stable revenue for a long time just by working off its backlog of billings, which makes the business look healthier than it is ([a16z](https://a16z.com/16-startup-metrics/), section 7 on deferred revenue and billings).
- **A tool's default MRR passes for the investor's MRR.** GrowthOptix, which sells a finance layer on top of Stripe, tells of a Series A founder who pitched $100k MRR from the Stripe dashboard while the investor's analyst rebuilt $8.3k from invoice lines, because annual plans were counted as monthly revenue ([GrowthOptix](https://www.growthoptix.com/blog/why-not-just-use-stripes-native-dashboard)). The story names no company and cannot be checked, and it is marketing. It shows the mechanism, not how often it happens.
- **A refusal to share the basis.** Hustle Fund's pause list includes "Refusal to share the basic evidence needed to understand cash, ownership, terms, or material obligations." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))

## How Tricorder checks it

**What a script can check**

Existing checks in [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md):

- `deck_claim_vs_named_cell` (entry 1.5): deck number against the export's cell.
- `cumulative_column_shown_as_active` (entry 1.8): a never-falling column shown as a live count.
- `arr_from_subscription_rows` (entry 1.2): ARR rebuilt from subscription lines.
- `mrr_column_vs_subscription_rows`, `one_time_fees_in_recurring_metrics` and `billings_vs_recognised_revenue` (entry 1.12, after Saturday).

Proposed new checks:

- `metrics_export_arithmetic`. For each month: `arr = 12 × mrr`; when new, expansion, contraction and churn columns exist, `mrr(t) − mrr(t−1) = new + expansion − contraction − churn`; `paying_accounts(t)` equals the count of customer-file rows with MRR above zero. Flag a gap above `match_tolerance`.
- `metrics_history_coverage`. Count the months between the first revenue month in the customer file and the as-of month, and compare with the months in the export. Flag a missing month, or a series that starts after the first revenue. The minimum length is a setting. The sources suggest 6 to 18 months at seed ([Visible](https://visible.vc/blog/what-to-include-in-your-data-room/)) and about two years at Series A (SaaStr write-up of the Janz talk, above). The team sets the default.
- `export_vs_pnl_revenue`. Monthly MRR against the P&L subscription revenue row, for the months both hold.

**What needs a model to read, and what it must quote**

- The header, footnote or definitions tab that says what MRR, ARR and "customers" mean. Quote it.
- A label match between deck and export ("customers" against "logos" against "paying accounts"). Quote both labels.
- A PDF or screenshot export: read the numbers, and set the confidence to "judged".
- A change of definition between two versions of the file or between update emails. Quote both.

**What Tricorder cannot check, so the operator does**

- Whether the numbers match the billing system. The operator can ask for a read-only billing export or a screen share.
- Whether the revenue reached the bank. That is a bank call or a banking-connector check, which sits on the roadmap.
- Any set of fake numbers that is consistent across every file. Tricorder finds differences in reporting. It does not detect fraud, and a fake that agrees everywhere passes.

## Which readout pieces it feeds

- **Traction and revenue** (main). **Retention** when it holds a churn column. **Customers and contracts** through the paying-customer count.
- Checklist items: C02 (the KPI dashboard or metrics export itself), C05 (ARR rebuilt from subscription lines), C06 (the MRR column matches subscription rows), C07 (revenue is delivered revenue, not bookings or billings), C09 (cash collected ahead of delivery is not counted as earned), C10 (one-time fees kept out of MRR and ARR), C11 (a cumulative count is not shown as active customers), C12 (earlier updates agree with today's numbers).

## If it is missing

- **Pre-seed:** not a gap.
- **Seed:** a gap. Not a red flag by itself. The first-pass scans on ARR and the deck can still run on the deck's claims and the model.
- **Series A:** a gap that blocks the traction and revenue piece, since nothing ties the deck to a series of months. It becomes a red flag only if the founder declines to share it, which Hustle Fund's pause list treats as a reason to stop and look.
- **Ask-list line:** "Send monthly MRR, ARR and paying customers since the first revenue month, with new, expansion, contraction and churn split out, and one line defining each term."

## In the Hollis Voice room

Yes: `03_metrics/monthly_metrics.csv`, which is also in the seed drop. Counts below come from [hollis_voice_counts.py](raw/kpi-dashboard-or-metrics-export/hollis_voice_counts.py), output in [hollis_voice_counts_output.txt](raw/kpi-dashboard-or-metrics-export/hollis_voice_counts_output.txt).

- 21 monthly rows, 2025-01 to 2026-09. Columns: `month`, `mrr`, `arr`, `paying_accounts`, `accounts_created_cumulative`, `calls_handled`. `arr` is 12 times `mrr` in every row.
- **Planted flags it carries:**
  - Pilot booked as ARR (`PF1`). The 2026-09 `mrr` is $186,739. The subscription rows in the customer file add to $171,739. The $15,000 gap is the Marlow pilot. The file's `arr` of $2,240,868 equals the model's ARR total.
  - Sign-ups shown as active clinics (`PF7`). The deck's 357 clinics equals the last value of `accounts_created_cumulative`. The live count in `paying_accounts` is 212.
  - The deck's $2,500,000 ARR (`PF2`) and the video's "about three million" (`PF2b`) sit beside this file's $2,240,868.
- **Gaps in the file:** no churn column, no new, expansion or contraction split, no definition row. A scan on the seed drop cannot rebuild churn, because the customer file is not in the seed drop.
- No green flag is planted here. The three corroborated numbers (raise, market size, staff) come from other files.

## Sources

Fund and firm pages: [a16z, 16 Startup Metrics](https://a16z.com/16-startup-metrics/) and [16 More Startup Metrics](https://a16z.com/16-more-startup-metrics/); [a16z, data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/); [Bessemer, Scaling to $100 Million](https://www.bvp.com/atlas/scaling-to-100-million); [CRV](https://www.crv.com/content/what-is-a-data-room); [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step); Jason Lemkin on SaaStr: [red flags](https://www.saastr.com/as-a-venture-capitalist-what-are-some-red-flags-that-would-make-you-reject-a-startup-immediately), [how VCs do diligence](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet), [top ten metrics](https://www.saastr.com/dear-saastr-what-are-the-top-10-metrics-series-a-investors-look-at/); [SaaStr write-up of the Janz talk](https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital).

Vendors and advisers (read as their views): [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/); [Peony](https://www.peony.ink/blog/series-a-data-room); [Eagle Rock CFO](https://www.eaglerockcfo.com/blog/series-a-preparation/data-room-checklist); [Baker Tilly](https://www.bakertilly.com/insights/your-arr-is-probably-wrong-and-could-be-costing-you); [Lighter Capital](https://www.lightercapital.com/blog/four-metrics-to-track-when-raising-capital-for-your-saas-company), a lender that defines MRR; [GrowthOptix](https://www.growthoptix.com/blog/why-not-just-use-stripes-native-dashboard).

News and opinion: [Fortune](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/); [Ctech](https://calcalistech.com/ctechnews/article/b1jfcymt3).

Saved copies are in [raw/kpi-dashboard-or-metrics-export/](raw/kpi-dashboard-or-metrics-export/).
