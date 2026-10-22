# Tax returns (three years)

*In short: tax returns are a Series A item that angels and seed funds often skip. A professional investor asks for them to see that the company is compliant and that the returns agree with the financials. The check is mostly "were they filed, for every year, and do they match the books".*

Written 2026-10-22. Quotes were checked word for word against saved pages by [financials_quotes.py](raw/financials_quotes.py); results are in [quotes_financials.csv](quotes_financials.csv). Accounting-firm and vendor views are marked. This guide is research for a diligence tool, not tax advice.

## 1. What it is

The company's filed income tax returns, with proof of filing. For a Delaware C corporation that means the federal Form 1120 and the state returns, usually with the payroll forms (941 and 940), sales tax filings if any, and the Delaware annual report and franchise tax. A CPA or tax firm prepares them. They arrive as PDFs from the tax software. Loss-making companies file too. The IRS instructions are plain:

> "Unless exempt under section 501, all domestic corporations (including corporations in bankruptcy) must file an income tax return whether or not they have taxable income." ([IRS, instructions for Form 1120](https://www.irs.gov/instructions/i1120))

## 2. At seed and at Series A

The research table gives no seed letter and a starred Series A "Y" ([data-room research](../20261022.02_research/research_data_room.md)), resting on one source. The sources I added fit that picture and add a split.

- **Seed: usually not asked.** Kruze, an accounting firm that prepares startup returns, says an angel or seed investor may not notice a missing return:

  > "Failure to file tax returns - an angel or seed investor may not notice, but by the time you are raising a big round from a professional investor, you bet they are going to ask for tax returns." ([Vanessa Kruze, Kruze Consulting](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/))

- **a16z does not want them up front:**

  > "Tax returns, audits, and legal docs like office leases or employee offer letters. We're not lawyers or accountants! If we have a concern, we'll request the documents we need." ([Justine Moore, a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/))

- **Series A: expected, by investor counsel.** Kruze's common tax requests:

  > "Past 3 years Federal tax returns" ([Vanessa Kruze, Kruze Consulting](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/))

  The same list adds three years of state returns, "Any correspondence with tax authorities" and the last two 409A valuations. A Kruze guide to seed-stage returns says later investors ask for all of them:

  > "It's common practice for sophisticated, later-stage venture investors to ask for all past returns so they can make sure that your company has been legally compliant and operating properly." ([Kruze Consulting](https://kruzeconsulting.com/blog/seed-stage-tax-returns/))

- **A vendor checklist lists them under "business plans and financials."** DocSend's diligence checklist, framed as what investors ask for after a term sheet, includes:

  > "Tax returns (from founding to present)" ([DocSend, vendor view](https://www.docsend.com/blog/due-diligence-checklist/))

- **Angels are told to check.** A guide for angels, the book *Angel Investing: Start to Finish* by Joe Wallin and Pete Baltaxe, says even a company with no revenue may have to file, and that sales and payroll taxes accrue without profit:

  > "Even if the company has no revenue, it may still need to file tax returns; and even if it is not making a profit, sales and payroll taxes still accrue." ([Joe Wallin and Pete Baltaxe, Angel Investing: Start to Finish, on Holloway](https://holloway.com/g/angel-investing/sections/legal-diligence-on-company-tax-issues))

## 3. What a first pass checks

1. Is a return there for every tax year since incorporation?
2. Is it the right form for the entity (a C corporation files Form 1120)?
3. Is there proof it was filed (e-file acceptance, or a filed copy)?
4. Do the return's gross receipts and net result agree with the P&L for the same year?
5. Are state returns there for the states where the company has employees or sales?
6. Are payroll forms present, and does the company use a payroll service?
7. Has the Delaware annual report and franchise tax been paid each year?
8. Is there any notice, penalty letter or open dispute?

## 4. Green flags

- **Every year filed, on time or on extension, with proof.** Kruze's seed-stage guide gives the deadline and the extension: Form 1120 is due April 15 for a calendar-year corporation, with an extension to October 15 if expected tax is paid ([Kruze Consulting](https://kruzeconsulting.com/blog/seed-stage-tax-returns/)).
- **Returns that agree with the financials.** The same page says a mismatch is what raises the flag:

  > "An acquirer's due diligence red flag goes up when a startup's financials don't match its tax returns." ([Kruze Consulting](https://kruzeconsulting.com/blog/seed-stage-tax-returns/))

  The IRS return carries a schedule for this reconciliation:

  > "Schedule M-1. Reconciliation of Income (Loss) per Books With Income per Return" ([IRS, instructions for Form 1120](https://www.irs.gov/instructions/i1120))

  Paro (vendor view) also tells companies to reconcile statements to returns every year ([Paro](https://paro.ai/blog/financial-review-vs-audit/)).
- **Payroll runs through a service.** The Holloway guide says payroll taxes are the scary ones because officers can be personally liable:

  > "Payroll taxes are especially scary because directors and officers can be personally responsible for them in certain circumstances." ([Wallin and Baltaxe, Holloway](https://holloway.com/g/angel-investing/sections/legal-diligence-on-company-tax-issues))

- **Delaware annual report and franchise tax paid on time.** Delaware's own page gives the March 1 deadline:

  > "All active Domestic Corporation Annual Reports and Franchise Taxes for the prior year are due annually on or before March 1st and are required to be filed online." ([Delaware Division of Corporations](https://corp.delaware.gov/paytaxes/))

- **Registered for sales tax in states where the company has nexus.** See the SaaS point below.

## 5. Red flags and pitfalls

**Common**

- **Returns never filed, including zero-activity years.** Kruze says the penalties can be steep and the deal can be delayed by months (Kruze quote in section 2; [Kruze Consulting](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/)). The Holloway guide says a company that forms a state corporation owes a federal return the first year "regardless of whether they have any income" ([Wallin and Baltaxe, Holloway](https://holloway.com/g/angel-investing/sections/legal-diligence-on-company-tax-issues)).
- **Returns that do not match the books** (Kruze quote in section 4).
- **Delaware annual report not filed.** Delaware states the penalty:

  > "Failure to file the report and pay the required franchise taxes will result in a penalty of $200.00 plus 1.5% interest per month on tax and penalty." ([Delaware Division of Corporations](https://corp.delaware.gov/paytaxes/))

- **No copy of the founders' 83(b) elections.** This is not a return, but the Holloway guide lists it among the tax items to check in legal diligence:

  > "The founders should have given the company copies of their filed elections." ([Wallin and Baltaxe, Holloway](https://holloway.com/g/angel-investing/sections/legal-diligence-on-company-tax-issues))

- **Sales tax not collected.** The same guide says the liability can build fast:

  > "Failure to collect and remit sales taxes can add up to a large liability in a short period of time, and it is not uncommon for companies to fall out of compliance with sales tax collect and remit requirements." ([Wallin and Baltaxe, Holloway](https://holloway.com/g/angel-investing/sections/legal-diligence-on-company-tax-issues))

  BDO, an accounting firm, gives the SaaS version after the *Wayfair* ruling:

  > "Following the decision, all states have enacted some form of legislation that adopts an economic nexus threshold (typically, this threshold is $100,000 in sales or 200 transactions)." ([BDO](https://www.bdo.com/insights/industries/technology/breaking-down-sales-and-use-tax-compliance-for-saas-companies))

  > "Sales tax exposure will remain a priority consideration during the due diligence process for any strategic deals taking place." ([BDO](https://www.bdo.com/insights/industries/technology/breaking-down-sales-and-use-tax-compliance-for-saas-companies))

  BDO's article dates from 2022 and counts about 20 states taxing SaaS then, so check the current state list before relying on it.

**Rare but serious**

- **Unremitted payroll tax.** The Holloway guide gives an example: a company ran its own payroll, the CEO did not pass withholding to the IRS, the board fired the CEO, and the company failed ([Wallin and Baltaxe, Holloway](https://holloway.com/g/angel-investing/sections/legal-diligence-on-company-tax-issues)).
- **A tax position in the return that the financials do not show.** Section 174 (research costs) changed in 2025. Anchin, an accounting firm, says the new rule restores full expensing of domestic research costs in the year incurred, for tax years beginning after 12/31/2024:

  > "restoring full expensing of domestic research or experimental expenditures (“R&E”) in the year incurred under new Internal Revenue Code (“IRC”) Section 174A." ([Anchin](https://www.anchin.com/articles/obbba-the-research-credit-and-section-174/))

  Kruze says the rule before 2025 required amortization of domestic R&D costs, which raised taxable income for many unprofitable startups ([Kruze Consulting](https://kruzeconsulting.com/blog/seed-stage-tax-returns/)). So a 2022 to 2024 return should show the old treatment. This is context for a reader, not a flag.

## 6. How Tricorder checks it

**What a script can check**

Existing: 1.11 What the room cannot settle checks whether tax returns are present and writes the ask, with the stage set to "after term sheet" ([FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md)). The checklist row "Tax returns were filed" rests on that.

Proposed new checks:

- `tax_years_covered_vs_age`. Tax years from incorporation to the last year-end before the data date, against the years found in the returns. Show the missing years. A company incorporated in 2024 and checked in 2026 has two possible years, not three.
- `return_gross_receipts_vs_pnl_revenue`. For each tax year, `gap = |gross receipts on the return - P&L revenue| / P&L revenue`. Flag past `match_tolerance`, and show the cash-versus-accrual note when the books are accrual and the return is not.
- `return_net_result_vs_pnl`. Net loss on the return, or the Schedule M-1 reconciliation, against the P&L net result.
- `entity_form_matches_cap_table`. Form 1120 for a C corporation; flag a partnership or S corporation return.
- `payroll_forms_present`. Four Form 941 filings per year in which the company had employees.
- `franchise_tax_each_year`. A Delaware annual report receipt for each year since incorporation.

**What needs a model to read**

- Gross receipts, deductions, net operating loss carryforward and any credits on the return, quoted by line.
- Research credit (Form 6765) and research-cost treatment, as in the Anchin quote.
- Any IRS or state notice, penalty letter or payment plan.
- The list of states on the state returns, set against where the company sells and employs people.

**What Tricorder cannot check**

- That the return was filed with the IRS. The operator can ask the company's CPA for the e-file acceptance, or have tax counsel confirm.
- Sales tax exposure by state. It needs revenue by customer state and a tax adviser. The Hollis Voice customer file has no state column.
- Whether a position on the return is correct. That is a tax professional's call.

## 7. Which readout pieces it feeds

- **Legal and cap table:** the checklist places "Tax returns (three years)" and "Tax returns were filed" here.
- **Traction and revenue:** gross receipts against the P&L, when the check can run.

Checklist rows: Tax returns (three years); Tax returns were filed ([CHECKLIST.md](../../ongoing/CHECKLIST.md)).

## 8. If it is missing

- **Pre-seed and seed:** not a gap. The readout says "not expected at this stage."
- **Series A:** a gap on the ask list, stage "after term sheet." It is not a red flag by itself. If the founder says the returns were never filed, the operator records the answer and Kruze's point applies (penalties, a delayed close).

One-line ask for the founder: "Please send the federal and state income tax returns filed since incorporation with proof of filing, the payroll tax filings, and the Delaware annual report and franchise tax receipts."

## 9. In the Hollis Voice room

Not in the room. The full room has 17 files and none is a tax return (checked in [hollis_financials_facts_output.json](raw/hollis_financials_facts_output.json)); the checklist records "not in the room." The company was founded in 2024 and the data date is 2026-09-30, so two calendar tax years have ended (2024 and 2025; script output). The ask should say "since incorporation," not "three years." No flag is planted for this document.

## 10. Sources

Each page is saved under [raw/tax-returns/](raw/tax-returns/).

| Source | Type | Saved file |
|---|---|---|
| [Kruze, VC diligence lists](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/), [seed-stage tax returns](https://kruzeconsulting.com/blog/seed-stage-tax-returns/), [startup tax return](https://kruzeconsulting.com/blog/post/startup-tax-return), [Delaware franchise tax](https://kruzeconsulting.com/blog/delaware-franchise-tax/), [audits in due diligence](https://kruzeconsulting.com/blog/prepare-for-audits-during-due-diligence/), [finance due diligence](https://kruzeconsulting.com/blog/finance-due-diligence-startups/), [SaaS sales tax](https://kruzeconsulting.com/blog/post/saas-sales-tax), [banking documentation](https://kruzeconsulting.com/blog/startup-due-diligence-banking-documentation/) | accounting firm | kruzeconsulting_com_*.txt |
| [IRS, instructions for Form 1120](https://www.irs.gov/instructions/i1120) | regulator | irs_gov_instructions_i1120.txt |
| [Delaware Division of Corporations](https://corp.delaware.gov/paytaxes/) | regulator | corp_delaware_gov_paytaxes.txt |
| [Wallin and Baltaxe, Angel Investing, on Holloway](https://holloway.com/g/angel-investing/sections/legal-diligence-on-company-tax-issues) | book excerpt for angels | holloway_com_g_angel_investing_sections_legal_diligence_on_company_tax_issues.txt |
| [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/) | fund | a16z_com_the_insiders_guide_to_data_rooms_what_to_know_before_you_raise.txt |
| [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) | vendor (saved through a browser) | docsend_com_blog_due_diligence_checklist.txt |
| [Cooley GO sample list](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/) | law firm | cooley_vc_dd_request_list.txt, cooleygo_com_documents_sample_vc_due_diligence_request_list.txt |
| [BDO](https://www.bdo.com/insights/industries/technology/breaking-down-sales-and-use-tax-compliance-for-saas-companies), [CLA](https://www.claconnect.com/en/resources/blogs/saas--think-youre-not-subject-to-sales-tax-think-again4-part-series) | accounting firms | bdo_com_*.txt, claconnect_com_*.txt |
| [Anchin](https://www.anchin.com/articles/obbba-the-research-credit-and-section-174/) | accounting firm | anchin_com_articles_obbba_the_research_credit_and_section_174.txt |
| [Paro](https://paro.ai/blog/financial-review-vs-audit/) | vendor | paro_ai_blog_financial_review_vs_audit.txt |

Pages that blocked me: Weaver's note on the 2025 tax law (HTTP 403). I did not find a law-firm checklist from Cooley, Fenwick, Orrick or Gunderson that spells out tax items beyond the Cooley sample request list, which has no tax-return line.
