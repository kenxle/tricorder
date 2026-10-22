# Sales pipeline snapshot

Guide for the data-room document in row 17 of the 30-document table in [the data-room research](../20261022.02_research/research_data_room.md). Written 2026-10-22 from online sources only. Every quote was checked word for word against the page text saved under [raw/sales-pipeline-snapshot/](raw/sales-pipeline-snapshot/). The check list is in [quotes_metrics.csv](quotes_metrics.csv).

## What it is

A dated list or chart of the deals the company is working: who the buyer is, the dollar value, the stage, when the deal was created, when it is expected to close, where it came from, and the next step. A fuller version adds a history of closed-won and closed-lost deals. The founder or the head of sales prepares it, usually as an export from a customer-relationship tool (a CRM) or a hand-built sheet. A product-led company with no sales team may send a funnel table instead (visitors, sign-ups, trials, paid), which SaaStr's write-up of a talk by Christoph Janz of Point Nine describes as the product-led version.

The point of a pipeline in a data room is to show whether growth is repeatable. Investors read it as evidence of a sales process, not as revenue.

## At seed and at Series A

- **Pre-seed:** not expected. The research table marks it "N". Visible, a vendor, lists "sales pipeline" among things a pre-seed founder can leave out ([Visible](https://visible.vc/blog/what-to-include-in-your-data-room/)).
- **Seed:** lighter. Visible's seed row lets a founder skip a "detailed pipeline if pre-revenue". Hustle Fund, a venture fund, still lists "Cohort, retention, pipeline, unit-economics, and customer-concentration support." among seed additions ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)). Papermark, a data-room vendor, puts a "sales pipeline snapshot" in the traction folder of the room it recommends for Y Combinator startups, beside "Monthly revenue and ARR history, cohort retention, customer list with contract values" ([Papermark](https://www.papermark.com/blog/data-room-for-yc-startups)).
- **Series A:** expected. Visible: "At Series A, narrative gets replaced with proof: a sales pipeline with stage and probability, customer reference letters, detailed case studies" ([Visible](https://visible.vc/blog/what-to-include-in-your-data-room/)). Malpani Ventures, a B2B seed fund, asks Series A companies "What does your current pipeline look like? How does your pipeline move? How do you qualify leads from one level to the next?" ([Malpani Ventures](https://www.malpaniventures.com/blog/due-diligence-data-room)). SaaStr's write-up of the Janz talk lists sales and pipeline metrics as the fourth of five things to show a Series A or B investor: "Investors will ask how you’re doing sales, what the pipeline looks like, and how it’s evolved." ([SaaStr write-up of the Janz talk](https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital)) These are the write-up's words about the talk, not Janz's own page.
- **Rule of thumb for size:** Jason Lemkin of SaaStr lists pipeline coverage among his top ten Series A metrics: "A 3x pipeline coverage ratio (pipeline value = 3x your ARR target) is a good rule of thumb." ([SaaStr](https://www.saastr.com/dear-saastr-what-are-the-top-10-metrics-series-a-investors-look-at/)) The sources disagree on whether 3x is right (see red flags).

## What a first pass checks

In order:

1. **How fresh is it, and where did it come from?** A dated CRM export, or a hand-built list.
2. **Do the stages mean something?** Is there a written rule for entering each stage?
3. **How much is in each stage, and is a probability or weight applied?**
4. **What do the closed deals say?** Closed-won and closed-lost for several quarters, so the win rate can be rebuilt.
5. **Is the pipeline big enough for the plan?** Coverage is open pipeline divided by the target for the period.
6. **Is it clean?** Old deals, deals with no recent activity, close dates piled on a quarter end, deals created just before the raise, one deal that is half the total.
7. **Are pilots and letters of intent kept out of revenue and bookings?**
8. **Does it match the model's growth plan, and do closed-won deals show up later as customers?**

## Green flags

- **Funnel dollars that move.** SaaStr's write-up of the Janz talk: "Here, investors are looking for a new quarterly record regarding new pipeline added and closed-won." (same page)
- **A pruned pipeline.** "You need to be disciplined enough to remove deals from the pipeline that don’t fit your ICP." (same page) ICP means ideal customer profile.
- **Stage definitions tied to facts.** The Next Web, in a piece sponsored by HubSpot for Startups: "“Qualified” should describe a fact about the deal, such as a confirmed budget owner on the call, not a feeling." ([The Next Web](https://thenextweb.com/news/seed-startup-sales-pipeline-investors-want-to-see)) Treat this as sponsored content.
- **Honest loss data.** The same piece: "Investors read a pipeline with no closed-lost deals as a pipeline nobody has cleaned." So a file with closed-lost rows and reasons is a green flag.
- **Dead deals marked dead by the founder.** Livmo, an adviser that helps companies sell themselves, lists as a strength "aged deals already marked dead by your own team before anyone asked" ([Livmo](https://livmo.com/blog/sales-pipeline-due-diligence-saas/)). Livmo writes for buyers of whole companies, so this is a buyer's view, not a venture view.
- **Reps who hit their targets repeatably.** SaaStr's write-up of the Janz talk: "Over time, most of the salespeople hit their targets, and it’s proof for investors that you can hire and train AEs and get them to reach their quota in a repeatable, predictable manner." (same page)
- **A win rate the founder quotes before anyone computes it,** matching the export. Livmo's suggestion, from the buyer's side.

## Red flags and pitfalls

**Common**

- **A funnel that grows while closed-won does not.** SaaStr's write-up of the Janz talk: "Many companies show the middle or top of the funnel growing, but closed-won numbers don’t go up in proportion. That usually means something isn’t quite working." (same page)
- **A pipeline nobody has cleaned.** No closed-lost rows (The Next Web, above). Livmo's list of what sinks credibility fastest: "close dates that all land on the last day of a quarter, stages with no dated activity behind them, a third of the pipeline created in the month before diligence started, win rates that are quietly computed with closed-lost deals deleted, and one heroic deal that is half the total." ([Livmo](https://livmo.com/blog/sales-pipeline-due-diligence-saas/))
- **A coverage claim that the win rate does not support.** Livmo: "Close 25% of qualified deals and you need 4x." (same page) Dave Kellogg, an experienced software executive writing on his own blog, disagrees with the method. He explains "why it's wrong to invert win rate to calculate target pipeline coverage", says "the rule of thumb for pipeline coverage is 3.0x", and offers his own basic rule: "my basic rule of thumb is you win a third, you lose a third, and you slip a third". ([Kellogg](https://www.kellblog.com/target-pipeline-coverage-is-not-the-inverse-of-win-rate/)) So a coverage multiple is context for the reader, and Tricorder never uses it as a pass or fail line.
- **Pipeline passed off as revenue.** Hustle Fund tells its angels to "Separate contracted revenue, recognized revenue, pipeline, pilots, letters of intent, and verbal interest." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)) a16z: "Letters of intent and verbal agreements are neither revenue nor bookings." ([a16z](https://a16z.com/16-startup-metrics/))
- **A pilot counted as ARR.** Fortune reports that six VCs said founders are "counting pilots, one-time deals, or unactivated contracts as recurring revenue". ([Fortune](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/)) A pilot is a pipeline deal until it converts.

**Rare but serious**

- **A pipeline that agrees with the plan too well.** A growth plan backed out of a pipeline of invented or inflated deals. The only way to test it is to call the buyers, so Tricorder leaves it to the operator. (My reading, not a sourced case.)
- **Closed-lost history that has been deleted.** Livmo lists it in the quote above.

## How Tricorder checks it

**What a script can check**

No script exists yet. The checklist marks both related items "not checked yet" (see below). Proposed checks:

- `pipeline_snapshot_freshness`. Snapshot date against the as-of date. The maximum age is a setting for the team. No source gives one.
- `win_rate_rebuild`. From the closed history: narrow win rate = wins ÷ (wins + losses); broad win rate = wins ÷ (wins + losses + no-decisions). Both by count and by value. Kellogg defines the narrow and broad forms in the post above.
- `pipeline_coverage_vs_plan`. Coverage = open pipeline expected to close in the period ÷ the plan's new ARR for the period. Shown beside `1 ÷ win_rate` (Livmo's method) and the fixed 3x (Lemkin's rule). No pass or fail.
- `pipeline_hygiene`. Six counts, each with the deal rows behind it: share of open value older than twice the median closed sales cycle (Livmo uses twice the cycle); share with no activity in `stale_days` (a setting, since no source gives a number); share of close dates on the last day of a quarter; share created in the 30 days before the snapshot; the largest deal as a share of the total; number of closed-lost rows.
- `stage_conversion`. Stage-to-stage conversion rates from the history.
- `closed_won_vs_customer_file`. Closed-won deals by month against new customers by month in the revenue-by-customer file, matched by name and amount.
- `pipeline_vs_model_growth`. The plan's new ARR for the next 12 months against weighted open pipeline plus historical conversion.

**What needs a model to read, and what it must quote**

- The stage names and any definition of them. Quote the definition.
- Free-text next steps. Does the note name a step on the buyer's side? Quote the note with its deal.
- Deal types: pilot, trial, letter of intent, expansion of an existing customer. Quote the label or note.
- A pipeline given only as a chart or screenshot: read what is legible and set the confidence to "judged".

**What Tricorder cannot check, so the operator does**

- Whether the named buyers are real and in the stage the file says. That is a call to a late-stage prospect or a read-only look at the CRM.
- Deals that live outside the CRM. Ask the head of sales.
- A pipeline that is consistent everywhere but invented. Tricorder finds differences in reporting, not fraud.

## Which readout pieces it feeds

- **Customers and contracts** (main). **Traction and revenue** through the growth plan and any pilot counted in revenue.
- Checklist items: C36 (the sales pipeline snapshot), C45 (sales pipeline against the growth plan), C44 (letters of intent and verbal agreements kept out of revenue and bookings). All three are marked "not checked yet" in the checklist. C39 (a pilot or trial with no duty to convert is not counted as recurring) links to it.

## If it is missing

- **Pre-seed:** not a gap.
- **Seed:** normal, not a gap, and not a red flag. Visible says a pre-revenue seed company can leave out a detailed pipeline.
- **Series A:** a gap that leaves the "pipeline against the growth plan" question unanswered. It is not a red flag by itself. If the plan assumes sharp growth with no pipeline behind it, say so as a gap on the plan.
- **Ask-list line:** "Send an opportunity-level export from your CRM with deal name, amount, stage, created date, expected close date, source, last activity and next step, including closed-lost deals, for the last six to eight quarters." The six to eight quarters come from Livmo, a buyer's adviser. A seed company can send fewer.

## In the Hollis Voice room

Not in the room. The 17 files of the full room include no pipeline or CRM export (checked by [hollis_voice_counts.py](raw/kpi-dashboard-or-metrics-export/hollis_voice_counts.py), output in [hollis_voice_counts_output.txt](raw/kpi-dashboard-or-metrics-export/hollis_voice_counts_output.txt)). The checklist row for it says "not in the room". There is no planted flag for it and no green flag.

What the room does hold that touches sales:

- Slide 4 of the deck says the Marlow Veterinary Group "started a pilot in August 2026". That pilot is a pipeline deal counted as recurring revenue, which is the planted flag `PF1`. It shows why a pipeline file matters: with one, the pilot would sit in the pipeline and not in ARR.
- The hiring plan lists five Sales hires: three Account Executives, a Director of Enterprise Sales and a Solutions Engineer (from the same script). A growth plan with that much sales hiring is the case where a pipeline snapshot would be asked for, to test whether the pipeline supports it.

For the demo, the right output is one gap: "Not in the room: a sales pipeline snapshot", with the ask-list line above.

## Sources

Fund and firm pages: [Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step); [Malpani Ventures](https://www.malpaniventures.com/blog/due-diligence-data-room); [a16z, 16 Startup Metrics](https://a16z.com/16-startup-metrics/); [Jason Lemkin, SaaStr top ten metrics](https://www.saastr.com/dear-saastr-what-are-the-top-10-metrics-series-a-investors-look-at/); [SaaStr write-up of the Janz talk](https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital); [Dave Kellogg, Kellblog](https://www.kellblog.com/target-pipeline-coverage-is-not-the-inverse-of-win-rate/).

Vendors, advisers and sponsored content (read as their views): [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/); [Papermark](https://www.papermark.com/blog/data-room-for-yc-startups); [Livmo](https://livmo.com/blog/sales-pipeline-due-diligence-saas/), a sell-side adviser; [The Next Web, sponsored by HubSpot for Startups](https://thenextweb.com/news/seed-startup-sales-pipeline-investors-want-to-see).

News: [Fortune](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/).

Saved copies are in [raw/sales-pipeline-snapshot/](raw/sales-pipeline-snapshot/). The Hollis Voice counts script and output are in [raw/kpi-dashboard-or-metrics-export/](raw/kpi-dashboard-or-metrics-export/).
