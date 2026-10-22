# Financial model, 3 to 5 years

*In short: a first pass reads the model for three things. Are the assumptions written down? Do the past months match the books? Do costs grow with revenue? At Series A the associate rebuilds it.*

Written 2026-10-22 for the Tricorder document guides. Quotes were checked word for word against the saved pages by [financials_quotes.py](raw/financials_quotes.py); the results are in [quotes_financials.csv](quotes_financials.csv). Vendor and accounting-firm views are marked as such.

## 1. What it is

The financial model is the founders' spreadsheet of revenue, costs, hiring and cash. Past months are marked actual and future months are marked plan. The CEO or a finance lead prepares it. Some startups pay an accountant to build it. It usually arrives as an Excel or Google Sheets file with an assumptions tab and a few output tabs.

A model sent as a PDF of charts is weaker. Visible, a vendor of data-room and investor-update software, says a forecast shown as a chart with no spreadsheet behind it reads as marketing material:

> "A three-year forecast presented as a chart with no underlying spreadsheet reads as marketing material, not analysis. Include the model with assumptions visible." ([Visible, vendor view](https://visible.vc/blog/what-to-include-in-your-data-room/))

## 2. At seed and at Series A

The research table marks the model as expected at pre-seed, seed and Series A ([data-room research, 30-document table](../20261022.02_research/research_data_room.md)). What changes is how hard it is read, and the sources disagree about the seed stage.

**Seed: the model shows how the founder thinks.**

- A self-described seed-stage VC, writing on Hacker News as lpolovets, says the point is the founder's thinking, not the number in month 36:

  > "This is less about your predicted revenue in month 36, or whatever, and more about understanding how you think about the business for the next year or two." ([lpolovets, Hacker News](https://news.ycombinator.com/item?id=30323322))

- MaC Venture Capital, a seed fund, says a seed model is hard to get right but worth studying for its drivers:

  > "understanding the core assumptions driving a company's revenue and costs are key to understanding the fundamentals of their business and for this reason it is important to study their pro-forma financial model." ([MaC Venture Capital, Kauffman Fellows journal](https://www.kauffmanfellows.org/journal/venture-diligence-at-the-seed-stage))

- Jason Lemkin lists basic financials and a model review among the checks before a term sheet, and says the review is "often only a cursory one." ([Jason Lemkin, SaaStr](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet))

- a16z disagrees about early consumer companies. It wants milestones for the next 12 to 18 months and does not need a long model:

  > "This may be a controversial one, but it's often difficult to model forward-looking financials for early stage consumer companies. We love to hear the key milestones you're looking to hit in the coming 12-18 months (and what you'll need to get there), but we don't expect a fully-baked model." ([Justine Moore, a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/))

- The HN post title "I have never read a business plan or balance sheet" quotes a Paul Graham tweet ([Hacker News post](https://news.ycombinator.com/item?id=30318634)). I could not open the tweet. In that thread lpolovets answers that it does not apply to seed rounds at higher valuations.

**Series A: the associate rebuilds it and sets it against actuals.**

- Peony, a data-room vendor, puts the change this way:

  > "At seed, a financial model is a signal that you think rigorously. At Series A, it's an input the associate rebuilds and stress-tests." ([Peony, vendor view](https://www.peony.ink/blog/series-a-data-room))

- CRV puts the model in the short first-pass list with the cap table, the incorporation papers and the IP assignments:

  > "The initial pass concentrates on a short list of corporate and legal records: the cap table, the financial model, the articles of incorporation and the intellectual property (IP) assignment agreements." ([CRV](https://www.crv.com/content/what-is-a-data-room))

- Eagle Rock CFO, a fractional-CFO firm (vendor view), lists "Your 3-5 year projections with monthly detail for year one" and asks for scenario analysis ("base, upside, downside") ([Eagle Rock CFO](https://www.eaglerockcfo.com/blog/series-a-preparation/data-room-checklist)).

**How long the horizon should be.** The sources give different numbers.

| Source | What it asks for |
|---|---|
| [NFX](https://www.nfx.com/post/the-non-obvious-guide-to-fundraising) | 24 months monthly, plus 3 years annual "(if credible)" |
| [Gale Wilkinson, Vitalize Venture Capital, on DocSend](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/) | 3 years of annual projections at pre-seed, 5 years at seed |
| [Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/) (accounting firm) | "3 to 5 year projections, usually by month" |
| [SaaStr's write-up of a Point Nine talk](https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital) | about two years of projections for a Series A or B deck |
| [Standard Ledger](https://www.standardledger.co/uk/article/the-5-red-flags-in-your-financial-model-that-will-kill-investor-confidence/) (UK accounting firm) | at seed, at least 24 to 36 months |

Tricorder should read whatever horizon the model has and say what it is. It should not call a short horizon a flaw at seed.

## 3. What a first pass checks

An associate asks these in order:

1. Does the model open, with formulas and an assumptions tab, or is it pasted values or a PDF?
2. Are actual months and plan months marked apart? a16z asks for this:

   > "make sure it's clear where historicals end and future projections begin by highlighting projections in a different color, or adding an (A) after actuals and a (P) after projections." ([a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/))

3. Do the actual months match the P&L, the metrics export and the deck? (See section 5; this is where most red flags show.)
4. Does every revenue number come from a driver (customers, price, reps, conversion), or from a growth percentage applied to last month?
5. Do costs, headcount and hiring grow with revenue, and is the hiring plan paid for in the cost lines?
6. Is gross margin built with every delivery cost?
7. How many months of cash does the raise buy, and does that match the deck?
8. Is there a downside case?

## 4. Green flags

- **The assumptions sit on one page and each has a source or note.** Dave Parker, a founder and mentor, says so (a founder's view, not an investor's):

  > "Ideally, all of the assumptions should be on one page (not hard-coded into the model) so they can test your assumptions by adjusting the drivers without breaking the spreadsheet." ([Dave Parker, republished by Founder Institute](https://fi.co/insight/epic-fail-in-fundraising-screwing-up-your-financial-assumptions-by-daveparkersea))

  NFX says it briefly: "Each line should tell a story." ([NFX](https://www.nfx.com/post/the-non-obvious-guide-to-fundraising))

- **Past and future use the same logic.** SaaStr's write-up of a Point Nine talk says to use one model for history and projections, and to show ARR movement (new, expansion, contraction, churn) ([SaaStr](https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital)). This is a summary of the talk, not Christoph Janz's own words.
- **One model, linked across tabs, that agrees with the deck.** a16z lists the opposite as a red flag (below), so the model that ties out is a green flag.
- **The model shows the economics behind the growth.** High Alpha, a venture studio and fund, says what it wants:

  > "VCs expect you to be optimistic about your business, but they also want to know you understand the economics of your business." ([Blake Koriath, High Alpha](https://www.highalpha.com/blog/want-to-raise-a-seed-or-series-a-heres-a-tip-dont-have-impossible-financial-projections))

- **A downside case.** Standard Ledger (accounting firm view):

  > "If your model only shows the bull case, it raises questions about whether you've genuinely stress-tested your assumptions." ([Standard Ledger](https://www.standardledger.co/uk/article/the-5-red-flags-in-your-financial-model-that-will-kill-investor-confidence/))

- **Hires start later than hoped, and the plan says so.** Kruze, an accounting firm, advises:

  > "Build some slack into your model and assume most future hires start a month or two later than you would like." ([Kruze](https://kruzeconsulting.com/blog/build-a-rolling-cash-forecast/))

- **Buffer for the next raise.** The same commenter lists this among what a plan reveals:

  > "do you have buffer time set aside for a future fundraise?" ([lpolovets, Hacker News](https://news.ycombinator.com/item?id=30323322))

- **Projections that sit near the history.** a16z:

  > "In most cases, your projections shouldn't be vastly different from the historical data. If MAUs have grown ~20% MoM for the past six months, it's probably unrealistic to assume 200% MoM growth for the next year." ([a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/))

- **Three-year projections tied to an operating model.** Peony lists "Three-year forward projections tied to a real operating model, not a single hockey-stick line" as a Series A item ([Peony, vendor view](https://www.peony.ink/blog/series-a-data-room)).

## 5. Red flags and pitfalls

Common means several of the saved sources name it. Rare but serious means the sources describe it as a cause of lost deals or fraud cases.

**Common**

- **The deck and the model disagree.** a16z names it first:

  > "Numbers that aren't consistent with what's in the deck. For example, your deck says $2M in ARR, but your model shows $1.5M." ([a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/))

  CRV says why partners care:

  > "When burn or revenue differs between the deck, the model and the accounting records, the gap suggests carelessness or something worse, and either reading damages the deal." ([CRV](https://www.crv.com/content/what-is-a-data-room))

- **Numbers disagree across tabs or files.** The same a16z page says one linked model fixes this ([a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/)). Standard Ledger sees it in unit economics:

  > "We've seen models where the unit economics on page 2 of the deck don't reconcile with the revenue build in the model itself." ([Standard Ledger](https://www.standardledger.co/uk/article/the-5-red-flags-in-your-financial-model-that-will-kill-investor-confidence/))

- **Costs that do not grow with revenue.** High Alpha:

  > "The problem comes when cost growth is disconnected from revenue growth." ([Blake Koriath, High Alpha](https://www.highalpha.com/blog/want-to-raise-a-seed-or-series-a-heres-a-tip-dont-have-impossible-financial-projections))

- **Gross margin too high because delivery costs sit elsewhere.** The same High Alpha post:

  > "If your gross margins are this high for a SaaS company, you're missing some costs that should be included in cost of goods sold (COGS)." ([Blake Koriath, High Alpha](https://www.highalpha.com/blog/want-to-raise-a-seed-or-series-a-heres-a-tip-dont-have-impossible-financial-projections))

- **A hiring plan that is not in the burn.** The forward cash forecast is the place hires must show up. Hustle Fund, an early-stage fund:

  > "A forward cash forecast captures planned hires, renewals, taxes, collections, and other changes that history misses." ([Hustle Fund](https://www.hustlefund.vc/post/angel-squad-startup-burn-rate-management-what-investors-should-actually-watch-for))

- **Only the best case.** See the Standard Ledger quote in section 4.
- **Hard-coded cells where a formula belongs, and plain spreadsheet errors.** Parker's quote above covers hard-coded inputs. Spreadsheet research says errors are normal in real organisational spreadsheets:

  > "The most recent field audits, in contrast, generally used better methodologies and found errors in at least 86% of the spreadsheets audited." ([Raymond Panko, EuSpRIG 2000](https://arxiv.org/pdf/0802.3457.pdf))

  Panko's paper also names omission errors (something that should be in the model is left out). A hire missing from payroll is an omission error. A KPMG survey of financial models reported major errors in 95 percent of them ([Chadwick and Sue, University of Greenwich, citing KPMG](https://arxiv.org/pdf/0801.1514.pdf)); that figure is a consultancy survey, so I treat it as colour.
- **A blog list of other flags (vendor view).** [Venture Lab](https://venture-lab.org/2026/startup-financial-projections-red-flags/) lists, among twelve, churn that is missing or unrealistically low, profitability arriving just before the next raise, no sensitivity analysis, mixing up bookings, revenue and cash, and round numbers with no bottom-up calculation. It is a marketing-style article, and its quotes from "a partner at a seed-stage fund on r/startups" are second-hand, so I do not quote them.

**Rare but serious**

- **A model that leaves out contractors, capitalised costs or deferred revenue,** so burn and revenue are both wrong. Tricorder's accounting-mislabels entry covers these.
- **A raise that does not give the runway the deck claims.** NFX says the raise should give runway:

  > "Requested investment should provide at least 18-24 months of runway ." ([NFX](https://www.nfx.com/post/the-non-obvious-guide-to-fundraising))

  Jason Lemkin on burn against growth:

  > "If you're burning $3M to add $1M in ARR, that's a red flag." ([Jason Lemkin, SaaStr](https://www.saastr.com/dear-saastr-what-are-the-top-10-metrics-series-a-investors-look-at/))

- **A model whose past months do not match the books.** One associate's line sums it up:

  > "If revenue in the deck doesn't match the P&L, or you show only part of your history, everything else becomes questionable." ([Startups Magazine, an associate quoted](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal))

  Hustle Fund's angel guide goes further and reads a mismatch as intent:

  > "If the numbers in their deck don't match the numbers in their data room, that's not a small mistake." ([Hustle Fund](https://www.hustlefund.vc/post/angel-squad-how-to-verify-startup-claims))

  Tricorder reports this as a difference in reporting between files. It does not say why the files differ.

## 6. How Tricorder checks it

**What a script can check**

Existing checks in [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md):

- 1.4 Burn against the hiring plan and runway, `payroll_from_hiring_plan_and_rerun_cash`. It rebuilds payroll from the hiring plan and reruns cash.
- 1.5 Deck-against-model reconciliation, `deck_claim_vs_named_cell`.
- 1.2 ARR definition check, `arr_from_subscription_rows`, on the model's ARR build.
- 1.3 Cohort retention rebuild, `rebuild_cohorts_from_customer_file`, on the Cohorts tab.
- 1.7 Gross margin composition, `gross_margin_from_ledger`.
- 1.12 Accounting mislabels, the kinds that read the model's P&L and ARR build.

Proposed new checks (names and formulas are mine; thresholds are settings the builders set after testing on the rooms):

- `model_actuals_vs_books`. For each actual month and line, `gap = |model value - P&L file value| / |P&L file value|`. Flag a month when the gap passes `match_tolerance`.
- `plan_costs_vs_revenue_growth`. Over the plan horizon, `revenue_multiple = revenue(last) / revenue(first)` and `cost_multiple = (cost of revenue + payroll + other costs)(last) / (same)(first)`. Show both. Flag when `revenue_multiple / cost_multiple` passes the setting `cost_scale_gap`.
- `plan_growth_vs_recent_actual`. Compare the plan's monthly growth with the compound monthly growth of the last six actual months. Flag when the plan is above history by more than a setting. Show the plan below history as a note, not a flag.
- `plan_cells_typed_not_linked`. In plan columns, count cells that hold a typed number where the neighbouring cells hold formulas. Show the count and the rows.
- `downside_case_present`. Look for a scenario, downside or sensitivity tab, name or label. Show a gap when none is found.
- `subtotals_foot`. Re-add every subtotal and compare.
- `actual_plan_labels_present`. The column header marks each month as actual or plan.

**What needs a model to read**

- Each assumption's note: does it give a source, a benchmark or the founder's own data? Quote the cell and its note.
- Notes that say hires will start later than the plan's start month, or at different pay (entry 1.4 already asks this).
- The README's definitions of ARR and gross margin, set against the deck's. Quote both.
- Whether the model's story matches the deck's story (a sales model with no salespeople, for example).

**What Tricorder cannot check**

- Whether the assumptions are true for this market. That takes an operator, comps and a customer or reference call.
- Whether the file is the model the company runs on. Ask for a call where the CEO walks through it; Parker says a founder must be able to find things in the spreadsheet even with a CFO.
- Whether the model was built backward from a number. Only the founder can say.

## 7. Which readout pieces it feeds

- **Burn and runway** (primary): payroll, burn, runway, the hiring plan. Checklist rows: Financial model, 3 to 5 years; Payroll rebuilt from the hiring plan, burn and runway recomputed and compared with the deck; Contractors counted in headcount and burn; Capitalised costs do not keep cash spend off the P&L ([CHECKLIST.md](../../ongoing/CHECKLIST.md)).
- **Traction and revenue:** the ARR build and the revenue lines.
- **Retention:** the Cohorts tab.
- **Unit economics:** the cost-of-revenue lines and gross margin.
- **The pitch itself:** deck numbers against named cells.

## 8. If it is missing

At every stage a missing model is a gap, not a red flag. FRAMEWORKS.md says a missing document is a question for the operator. At pre-seed and seed, the operator can fall back on the deck and the milestones, as a16z does. At Series A the model sits on CRV's first-pass list, so the ask goes near the top of the list.

One-line ask for the founder: "Please send the current financial model as a spreadsheet with formulas and the assumptions tab visible, monthly for the next 24 months and annual after that, with actual months marked apart from plan months."

## 9. In the Hollis Voice room

The room holds the model: `02_financials/financial_model.xlsx`, in the first tier and the seed drop ([data_room/README.md](../../../data_room/README.md)). Numbers below come from [hollis_financials_facts.py](raw/hollis_financials_facts.py), saved as [hollis_financials_facts_output.json](raw/hollis_financials_facts_output.json), and from the answer key.

What it shows:

- Nine tabs, 29 named cells and 475 formulas. Every one of the 18 rows on the Assumptions tab has a note. Actual and plan months are labelled.
- 21 actual months (2025-01 to 2026-09) and 12 plan months in the P&L. The cash plan runs for 60 plan months, to 2031-09.
- No scenario, downside or sensitivity wording anywhere in the workbook. No balance sheet or cash flow statement. The Cash_Bridge tab says cash burn is the operating result and the model "does not track working capital timing".

Planted flags that sit in the model:

- Burn and runway do not match the hiring plan. The model pays for 8 of the 24 hires. It shows 37 months of runway and the rebuilt figure is 19 months. Average net burn is $374,462 in the model and $480,062 rebuilt (answer key; FRAMEWORKS 1.4).
- A pilot is counted as ARR: the model's ARR total is $2,240,868 and recurring ARR from subscription rows is $2,060,868.
- Gross margin leaves out hosting, inference and support: 80 percent shown, 58.1 percent with those costs (key).
- Deck ARR disagrees with the model ($2,500,000 on the deck against $2,240,868 in the model), and the cohort tab hides churn.

Green flag: the Series A raise of $9,000,000 agrees across the model, the cap table and deck slide 13 (key, "The round adds up"). The market size and staff-today numbers also agree between the deck and the model.

Observations the key does not plant. These are test cases for the proposed checks, not findings:

- From plan month 4 to plan month 60, payroll sits at one value ($394,666.67) while recurring revenue grows 7.61 times from plan month 1 to plan month 60. `plan_costs_vs_revenue_growth` would fire.
- The plan grows 3.5 percent a month. Recent actual MRR growth over the last six months is 11.76 percent a month. `plan_growth_vs_recent_actual` would stay quiet.
- In the P&L plan columns, 132 line cells are typed numbers and 96 are formulas. `plan_cells_typed_not_linked` would report the rows.
- The cost-of-revenue and operating-expense subtotals foot in all 33 months, and the P&L costs equal the expense ledger in all 21 actual months (largest gap $0.00). The room itself is consistent on those points.

## 10. Sources

Each page is saved under [raw/financial-model/](raw/financial-model/).

| Source | Type | Saved file |
|---|---|---|
| [a16z, insider's guide to data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/) | fund | a16z_com_the_insiders_guide_to_data_rooms_what_to_know_before_you_raise.txt |
| [NFX, non-obvious guide to fundraising](https://www.nfx.com/post/the-non-obvious-guide-to-fundraising) | fund | nfx_com_post_the_non_obvious_guide_to_fundraising.txt |
| [CRV, what is a data room](https://www.crv.com/content/what-is-a-data-room) | fund | crv_com_content_what_is_a_data_room.txt |
| [High Alpha, impossible financial projections](https://www.highalpha.com/blog/want-to-raise-a-seed-or-series-a-heres-a-tip-dont-have-impossible-financial-projections) | fund and studio | highalpha_com_blog_want_to_raise_a_seed_or_series_a_heres_a_tip_dont_have_impossible_financial_projections.txt |
| [MaC Venture Capital, venture diligence at the seed stage](https://www.kauffmanfellows.org/journal/venture-diligence-at-the-seed-stage) | fund | kauffmanfellows_org_journal_venture_diligence_at_the_seed_stage.txt |
| [lpolovets, Hacker News comment](https://news.ycombinator.com/item?id=30323322) and [the post it answers](https://news.ycombinator.com/item?id=30318634) | investor comment | hn_item_30323322.json, hn_item_30318634.json |
| [SaaStr, Lemkin on due diligence](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet), [top 10 metrics](https://www.saastr.com/dear-saastr-what-are-the-top-10-metrics-series-a-investors-look-at/), [Point Nine talk write-up](https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital) | fund and media | saastr_com_*.txt (three files) |
| [Hustle Fund, verify claims](https://www.hustlefund.vc/post/angel-squad-how-to-verify-startup-claims) and [burn rate](https://www.hustlefund.vc/post/angel-squad-startup-burn-rate-management-what-investors-should-actually-watch-for) | fund | hustlefund_vc_post_angel_squad_how_to_verify_startup_claims.txt, web_hustlefund_vc_post_angel_squad_startup_burn_rate_management_what_investors_should_actually_watch_for.txt |
| [Startups Magazine, data room guide](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal) | magazine | web_startupsmagazine_co_uk_how_to_build_a_data_room_that_closes_the_deal.txt |
| [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) | vendor | visible_vc_blog_what_to_include_in_your_data_room.txt |
| [Peony](https://www.peony.ink/blog/series-a-data-room) | vendor | peony_ink_blog_series_a_data_room.txt |
| [DocSend, Gale Wilkinson](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/) | fund partner on a vendor blog (saved through a browser) | docsend_com_blog_4_types_of_documents_founders_must_have.txt |
| [Kruze, VC diligence lists](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/) and [rolling cash forecast](https://kruzeconsulting.com/blog/build-a-rolling-cash-forecast/) | accounting firm | kruzeconsulting_com_what_are_examples_of_vc_due_diligence_check_lists.txt, kruzeconsulting_com_blog_build_a_rolling_cash_forecast.txt |
| [Standard Ledger, five red flags](https://www.standardledger.co/uk/article/the-5-red-flags-in-your-financial-model-that-will-kill-investor-confidence/) | accounting firm (UK) | standardledger_co_uk_article_the_5_red_flags_in_your_financial_model_that_will_kill_investor_confidence.txt |
| [Eagle Rock CFO](https://www.eaglerockcfo.com/blog/series-a-preparation/data-room-checklist) | fractional CFO firm | eaglerockcfo_com_blog_series_a_preparation_data_room_checklist.txt |
| [Dave Parker via Founder Institute](https://fi.co/insight/epic-fail-in-fundraising-screwing-up-your-financial-assumptions-by-daveparkersea) | founder and mentor | fi_co_insight_epic_fail_in_fundraising_screwing_up_your_financial_assumptions_by_daveparkersea.txt |
| [Venture Lab](https://venture-lab.org/2026/startup-financial-projections-red-flags/) | blog | venture_lab_org_2026_startup_financial_projections_red_flags.txt |
| [Panko, spreadsheet errors](https://arxiv.org/pdf/0802.3457.pdf) and [Chadwick and Sue](https://arxiv.org/pdf/0801.1514.pdf) | academic | arxiv_org_pdf_0802_3457_panko_2000_spreadsheet_errors.txt, arxiv_org_pdf_0801_1514_pdf.txt |

Saved but not used: Angel Investors Network on pitch-deck red flags, Aaron Pickard's Substack, the Computerworld sidebar on spreadsheet audits, Forecastr, the a16z 16 startup metrics page, Kruze's financial-models sales page.
