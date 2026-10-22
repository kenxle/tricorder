# Historical P&L, balance sheet, cash flow (monthly)

*In short: the past statements are the one place a founder's story meets the books. A first pass checks that they cover the whole history, that revenue and costs are labelled honestly, and that the deck's numbers come from them. When the pitch and the P&L disagree, investors believe the P&L.*

Written 2026-10-22. Quotes were checked word for word against saved pages by [financials_quotes.py](raw/financials_quotes.py); results are in [quotes_financials.csv](quotes_financials.csv). Vendor and accounting-firm views are marked.

## 1. What it is

Three statements, month by month, from the company's accounting system:

- the profit and loss statement (revenue, cost of revenue, operating costs, net result);
- the balance sheet (cash, receivables, deferred revenue, payables, equity);
- the cash flow statement (cash in and out, split into operating, investing and financing).

The founder's bookkeeper, controller or outside accountant prepares them. They arrive as exports from QuickBooks, Xero or a similar tool, or as a spreadsheet the finance lead keeps. At small companies the P&L alone is often all that exists.

a16z asks for the P&L first and treats the other two as optional if the cash balance is shown:

> "Historical P&L and burn. This should show the path from gross revenue through net income (loss) through cash outflow on a monthly basis. Make sure to break out different types of revenue (if applicable) and all of your major costs." ([Justine Moore, a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/))

## 2. At seed and at Series A

The research table marks historical statements as lighter at pre-seed, expected at seed and expected at Series A ([data-room research](../20261022.02_research/research_data_room.md)).

- **Seed.** Visible (vendor) says seed founders add history to the pre-seed set:

  > "Seed founders add 6 to 18 months of historical financials and an early KPI dashboard." ([Visible](https://visible.vc/blog/what-to-include-in-your-data-room/))

  Gale Wilkinson, a managing partner at Vitalize Venture Capital, asks for a P&L since inception, a year-to-date statement and the latest balance sheet:

  > "Founders should include historical profit-and-loss statements since inception as well as a year-to-date statement if it's the middle of the year. I also need to see the company's most recent balance sheet." ([Gale Wilkinson, on DocSend](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/))

- **Series A.** All three statements, monthly, over a longer span. Kruze, an accounting firm, lists the common request:

  > "Past 3 year financial statements (income statement, balance sheet, cash flow)" ([Vanessa Kruze, Kruze Consulting](https://kruzeconsulting.com/what-kind-of-financial-data-should-a-company-prepare-when-seeking-series-a-venture-capital-funding/))

  Eagle Rock CFO (fractional-CFO firm, vendor view) asks for a monthly P&L for 24 months with a comparison to plan, and monthly balance sheets with attention to receivables and deferred revenue:

  > "Monthly P&L for the past 24 months. Include comparisons to budget/plan." ([Eagle Rock CFO](https://www.eaglerockcfo.com/blog/series-a-preparation/data-room-checklist))

  > "Pay particular attention to accounts receivable aging and deferred revenue." ([Eagle Rock CFO](https://www.eaglerockcfo.com/blog/series-a-preparation/data-room-checklist))

- **Accounting basis.** Stripe's guide (vendor view) says Series A investors expect accrual-based statements:

  > "Investors in the Series A stage and beyond will typically expect GAAP and IFRS financial statements." ([Stripe](https://stripe.com/resources/more/cash-vs-accrual-accounting))

  David Cummings, a founder and investor, wrote in 2011 that early startups can stay on cash accounting, then conceded in the comments:

  > "I agree accrual accounting is best once the startup is off the ground but in the earliest of stages I still stand by cash being king." ([David Cummings, on his blog](https://davidcummings.org/2011/06/06/accrual-vs-cash-basis-accounting-for-startups/))

- **Where the law firms land on monthly statements.** In the NVCA-style investor rights agreement, monthly statements are a right investors may ask for after closing. MoFo says early companies often leave it out:

  > "For early stage companies, it is common to leave out this requirement to lessen the administrative burden on the company and its small team." ([Morrison Foerster, ScaleUp](https://scaleup.mofo.com/guidance/ask-a-mofo-common-provisions-in-venture-capital-term-sheets-information-and-observer-rights))

  Reporting duties after closing and requests during diligence differ. The investor rights agreement often drops monthly statements for early companies, yet the Series A data-room guides above ask for monthly history. A seed company without monthly balance sheets is normal. A Series A room is expected to have them.

Standard Ledger (UK accounting firm) gives a UK version: two to three years of statements where available, plus year-to-date management accounts ([Standard Ledger](https://www.standardledger.co/uk/article/preparing-your-financials-for-investor-due-diligence)).

## 3. What a first pass checks

1. How many months does it cover, and does that reach back to the first revenue? a16z flags a short slice of a long history.
2. Are all three statements there, or only a P&L?
3. Do the revenue lines separate subscription, pilot, one-time and services revenue?
4. Is cost of revenue complete (hosting, model usage, support, telephony, licences), or do delivery costs sit in R&D or sales?
5. Does payroll match the headcount and the hiring plan?
6. Does revenue in the deck match the P&L, period by period?
7. Does the statement's net result, plus financing, explain the bank balance?
8. Is the basis stated (cash or accrual), and is prepaid revenue held as deferred revenue?

## 4. Green flags

- **The P&L and the deck agree, month by month.** One associate says what happens when they do not:

  > "If revenue in the deck doesn't match the P&L, or you show only part of your history, everything else becomes questionable." ([Startups Magazine, an associate quoted](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal))

  Jonathan Hua, who built diligence decks at SVG Ventures-THRIVE and then Scrum Ventures, says which side wins when they differ:

  > "When the pitch and the P&L disagree, the P&L wins, every time, no exceptions." ([Jonathan Hua, The Data Room](https://thedataroom.substack.com/p/how-a-vc-does-due-diligence-on-your-company))

- **Whole history, monthly, with actuals clearly marked.** a16z asks for monthly data and gives the failure case (section 5).
- **The books were closed on time and do not move.** Kruze:

  > "VCs do not expect historical financials to change dramatically during a fund raise, which can happen if you haven't done a good job keeping and closing your books." ([Vanessa Kruze, Kruze Consulting](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/))

- **Delivery costs are in cost of revenue.** High Alpha:

  > "If your gross margins are this high for a SaaS company, you're missing some costs that should be included in cost of goods sold (COGS)." ([Blake Koriath, High Alpha](https://www.highalpha.com/blog/want-to-raise-a-seed-or-series-a-heres-a-tip-dont-have-impossible-financial-projections))

  A P&L that already puts hosting, model usage and support in cost of revenue is a green flag for unit economics.
- **The cash result ties to the bank balance.** Hustle Fund says to compare the operating calculation with the bank movement:

  > "If the operating calculation and bank movement do not agree, ask which financing flow, one-time payment, or timing difference is missing." ([Hustle Fund](https://www.hustlefund.vc/post/angel-squad-startup-burn-rate-management-what-investors-should-actually-watch-for))

- **Revenue recognised over the service period, with deferred revenue on the balance sheet.** Kruze's worked example is a customer who pays upfront for 12 months; the revenue is spread and the rest is deferred ([Kruze Consulting](https://kruzeconsulting.com/blog/startup-accounting-due-diligence-mistakes/)).

## 5. Red flags and pitfalls

**Common**

- **Part of the history.** a16z:

  > "For example, you only show three months of data when your company is three years old, or you show quarterly but not monthly revenue." ([Justine Moore, a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/))

  Tricorder's `deck-vs-books` slice on the roadmap is built around this.

- **Books that are behind.** Kruze:

  > "One of the most common due diligence issues is simply having books that are behind." ([Kruze Consulting](https://kruzeconsulting.com/blog/startup-accounting-due-diligence-mistakes/))

- **Cash-basis revenue.** Kruze:

  > "A common mistake is recording the full value of a customer contract as revenue when the cash arrives or the invoice is issued (cash accounting)." ([Kruze Consulting](https://kruzeconsulting.com/blog/startup-accounting-due-diligence-mistakes/))

  Taxstra (vendor) puts it more bluntly: "Prepaid cash is not income; it is an obligation." ([Taxstra](https://taxstra.com/startup-accounting/)) And DualEntry (vendor):

  > "If you've been recognizing revenue on cash receipt rather than ratable delivery, you're looking at a retroactive restatement before close." ([DualEntry](https://www.dualentry.com/blog/series-a-saas-accounting))

- **Revenue is not cash.** Hustle Fund:

  > "Revenue recognized on an income statement may not arrive in the bank during the same month." ([Hustle Fund](https://www.hustlefund.vc/post/angel-squad-startup-burn-rate-management-what-investors-should-actually-watch-for))

- **Inconsistent categories.** Kruze:

  > "Poor categorization can also lead to inconsistent financial reporting." ([Kruze Consulting](https://kruzeconsulting.com/blog/startup-accounting-due-diligence-mistakes/))

  The same page names payroll as the easy place for investors to spot gaps:

  > "Payroll is often a company's largest expense, which means discrepancies are easy for investors to spot." ([Kruze Consulting](https://kruzeconsulting.com/blog/startup-accounting-due-diligence-mistakes/))

- **Gross margin above what the business can earn,** because delivery costs sit in R&D or sales (High Alpha quote above).
- **Personal and company expenses mixed.** Visible lists this as a seed-stage pitfall ("Mixing personal and company expenses") in its stage table ([Visible, vendor view](https://visible.vc/blog/what-to-include-in-your-data-room/)).

**Rare but serious**

- **Statements that do not come from a ledger.** If the statements are typed in a spreadsheet and the bank balance is not reconciled, the numbers can say anything. Tricorder cannot see this; only an accountant's read-only access can (section 6).
- **Fabricated or altered books.** Cases are in the [bank statements guide](bank-statements.md). A difference between the statements and the bank is the signal; Tricorder reports the difference and not the cause.
- **Investor-update numbers that differ from the statements.** Visible (vendor) calls a mismatch between dashboard numbers and deck numbers "one of the fastest ways to lose credibility" ([Visible](https://visible.vc/blog/what-to-include-in-your-data-room/)).

## 6. How Tricorder checks it

**What a script can check**

Existing checks in [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md):

- 1.12 Accounting mislabels: `billings_vs_recognised_revenue`, `deferred_revenue_vs_earned`, `one_time_fees_in_recurring_metrics`, `contractor_spend_vs_headcount_and_burn`, `capitalised_spend_vs_pnl_and_cash`, and `mrr_column_vs_subscription_rows`. All except the first ARR-side check wait for the roadmap's accounting-mislabels slice.
- 1.7 Gross margin composition, `gross_margin_from_ledger`.
- 1.4 Burn against the hiring plan and runway, `payroll_from_hiring_plan_and_rerun_cash`.
- 1.11 What the room cannot settle: asks for the statements when they are missing.
- 1.5 Deck-against-model reconciliation, `deck_claim_vs_named_cell`, for revenue and burn claims against the P&L.

Proposed new checks:

- `statements_present_by_month`. For each month since the first revenue month, record whether a P&L, a balance sheet and a cash flow statement exist. Show the first and last month and any gap in the run.
- `history_covers_company_life`. Compare the first month in the statements with the first revenue month in the metrics export and the incorporation date. Flag when the statements start later and the deck's chart starts earlier.
- `deck_revenue_vs_pnl_by_month`. For each month the deck shows revenue, `gap = |deck - P&L| / P&L`. Flag months past `match_tolerance`. (This is the roadmap's `deck-vs-books` slice.)
- `balance_sheet_balances`. For each month, `assets - (liabilities + equity)` equals zero within a cent.
- `cash_rolls_forward`. Ending cash in month t equals ending cash in t-1 plus the month's net cash flow.
- `deferred_revenue_roll`. `begin + billings - recognised = end` for each month. An annual plan paid up front must pass.
- `restated_between_versions`. When two versions of the same month appear (data room and an investor update), flag a change past tolerance.
- `subtotals_foot`. Re-add subtotals.

**What needs a model to read**

- The statement notes: basis of accounting (cash or accrual), revenue recognition policy, how annual plans are treated. Quote the line.
- The mapping of ledger accounts to P&L lines (which account is "R&D", which is "cost of revenue").
- Whether a line labelled "revenue" is bookings, billings, gross sales or pass-through (accounting mislabels, kinds b and c).
- Unusual lines: related-party items, founder loans, one-time gains.

**What Tricorder cannot check**

- That the statements came from the ledger and not from a spreadsheet written for the room. An operator can ask for read-only access to the accounting system, or ask the accountant.
- That the ledger itself is true. A bank call or bank connector is the check (see the bank statements guide).
- Whether the company's revenue recognition is right under GAAP. That is an accountant's judgment.

## 7. Which readout pieces it feeds

- **Burn and runway:** checklist row "Historical P&L, balance sheet, cash flow (monthly)".
- **Traction and revenue:** the revenue lines and the mislabel checks (bookings or billings as revenue, deferred revenue counted as earned).
- **Unit economics:** the cost-of-revenue lines and gross margin.
- **The pitch itself:** deck numbers against the P&L.

Checklist rows covered: Historical P&L, balance sheet, cash flow (monthly); Revenue is what was delivered, not bookings or billings; Cash collected ahead of delivery is not counted as earned; Gross margin rebuilt with every delivery cost; Expense ledger or expense breakdown by function ([CHECKLIST.md](../../ongoing/CHECKLIST.md)).

## 8. If it is missing

A gap at every stage in the readout. At seed the P&L matters more than the other two statements. At Series A all three are expected, and the ask goes high in the list.

One-line ask for the founder: "Please send monthly profit and loss, balance sheet and cash flow statements from the first month of revenue to the last closed month, exported from your accounting system, with the basis (cash or accrual) stated."

## 9. In the Hollis Voice room

No separate statement files. The only historical statement is the P&L tab inside `02_financials/financial_model.xlsx`, with 21 actual months (2025-01 to 2026-09) and 12 plan months. There is no balance sheet and no cash flow statement. The workbook does not use the words "deferred revenue". The Cash_Bridge tab says cash burn is the operating result and "does not track working capital timing". Numbers are from [hollis_financials_facts_output.json](raw/hollis_financials_facts_output.json).

What the room shows:

- The P&L equals the expense ledger in all 21 actual months (largest gap $0.00), and the P&L's subscription revenue equals the customer file in all 21 months (largest gap $0.00). Those are agreements between two files that both come from the founder.
- The Cash_Bridge ties money raised, less losses, to the $1,800,000 cash figure, with a difference of -$0.24 (rounding).

Planted flags in the P&L:

- Gross margin leaves out hosting, inference and support. The P&L books "Cloud hosting and model inference" under R&D and "Customer support specialists" under S&M. Margin shown is 80 percent; rebuilt from the ledger for 2026-09 it is 58.15 percent (script), and the key says 58.1 percent.
- The pilot counted as recurring revenue ("Recurring revenue (subscription plus pilot)") is the same fact as the planted pilot-as-ARR flag.

Decoys the P&L must not trip: the $500 onboarding fee is its own row ("Onboarding fees (one-time)"); the annual prepay from Brookline Row shows as cash in the billings column but as monthly revenue in the P&L.

A "not in the room" gap: balance sheet and cash flow statement. The ask list should request them.

## 10. Sources

Each page is saved under [raw/historical-financials/](raw/historical-financials/).

| Source | Type | Saved file |
|---|---|---|
| [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/) | fund | a16z_com_the_insiders_guide_to_data_rooms_what_to_know_before_you_raise.txt |
| [Kruze Consulting, financial data for Series A](https://kruzeconsulting.com/what-kind-of-financial-data-should-a-company-prepare-when-seeking-series-a-venture-capital-funding/), [VC diligence lists](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/), [accounting mistakes](https://kruzeconsulting.com/blog/startup-accounting-due-diligence-mistakes/) | accounting firm | kruzeconsulting_com_*.txt (three files) |
| [Eagle Rock CFO](https://www.eaglerockcfo.com/blog/series-a-preparation/data-room-checklist) | fractional CFO (vendor) | eaglerockcfo_com_blog_series_a_preparation_data_room_checklist.txt |
| [DocSend, Gale Wilkinson](https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/) | fund partner (saved through a browser) | docsend_com_blog_4_types_of_documents_founders_must_have.txt |
| [The Data Room, Jonathan Hua](https://thedataroom.substack.com/p/how-a-vc-does-due-diligence-on-your-company) | former VC, newsletter | web_thedataroom_substack_com_p_how_a_vc_does_due_diligence_on_your_company.txt |
| [Startups Magazine](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal) | magazine | web_startupsmagazine_co_uk_how_to_build_a_data_room_that_closes_the_deal.txt |
| [Hustle Fund, burn rate](https://www.hustlefund.vc/post/angel-squad-startup-burn-rate-management-what-investors-should-actually-watch-for) | fund | web_hustlefund_vc_post_angel_squad_startup_burn_rate_management_what_investors_should_actually_watch_for.txt |
| [High Alpha](https://www.highalpha.com/blog/want-to-raise-a-seed-or-series-a-heres-a-tip-dont-have-impossible-financial-projections) | fund and studio | highalpha_com_blog_want_to_raise_a_seed_or_series_a_heres_a_tip_dont_have_impossible_financial_projections.txt |
| [CRV](https://www.crv.com/content/what-is-a-data-room) | fund | crv_com_content_what_is_a_data_room.txt |
| [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) | vendor | visible_vc_blog_what_to_include_in_your_data_room.txt |
| [Morrison Foerster, ScaleUp](https://scaleup.mofo.com/guidance/ask-a-mofo-common-provisions-in-venture-capital-term-sheets-information-and-observer-rights) | law firm | scaleup_mofo_com_guidance_ask_a_mofo_common_provisions_in_venture_capital_term_sheets_information_and_observer.txt |
| [Stripe](https://stripe.com/resources/more/cash-vs-accrual-accounting), [Taxstra](https://taxstra.com/startup-accounting/), [DualEntry](https://www.dualentry.com/blog/series-a-saas-accounting), [Puzzle](https://puzzle.io/blog/cash-vs-accrual-accounting-startups), [Forecastr](https://www.forecastr.co/blog/saas-financial-model-series-a), [Promise Legal](https://promise.legal/startup-legal-guide/funding/series-a-prep) | vendors | stripe_com_*, taxstra_com_*, dualentry_com_*, puzzle_io_*, forecastr_co_*, promise_legal_* |
| [David Cummings](https://davidcummings.org/2011/06/06/accrual-vs-cash-basis-accounting-for-startups/) | founder and investor blog, 2011 | davidcummings_org_2011_06_06_accrual_vs_cash_basis_accounting_for_startups.txt |
| [Standard Ledger](https://www.standardledger.co/uk/article/preparing-your-financials-for-investor-due-diligence) | accounting firm (UK) | standardledger_co_uk_article_preparing_your_financials_for_investor_due_diligence.txt |
| [SaaStr, Point Nine talk write-up](https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital) | media | saastr_com_saas_investor_pitch_metrics_2024_christoph_janz_point_nine_capital.txt |

Saved but not used: Kruze's cash-to-accrual and runway pages, Bain Capital Ventures' diligence page, the DocSend diligence checklist, the a16z 16 startup metrics page, Lighter Capital's CMRR page, Forecastr, Puzzle and Promise Legal (read only for background).
