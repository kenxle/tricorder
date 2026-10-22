# Audited or reviewed financials

*In short: at seed nobody expects them, and at Series A most sources say they are optional. They matter because an outside accountant's signed report is stronger evidence than the founder's own spreadsheet. A first pass compares them with the management numbers. An audit does not rule out fraud.*

Written 2026-10-22. Quotes were checked word for word against saved pages by [financials_quotes.py](raw/financials_quotes.py); results are in [quotes_financials.csv](quotes_financials.csv). Vendor views are marked.

## 1. What it is

Financial statements that an outside CPA firm has worked on, with the firm's signed report on the front. There are three levels, and the level matters:

- **Compilation.** The CPA assembles the numbers from management. Wegner CPAs says it gives "no assurance" ([Wegner CPAs](https://www.wegnercpas.com/services/audit-assurance/comparing-compilations-reviews-audits/)).
- **Review.** The CPA asks questions and runs analytical checks. The same page says the report gives "limited assurance" and states that the CPA "did not become aware of any material modifications necessary to be in conformity with generally accepted accounting principles" ([Wegner CPAs](https://www.wegnercpas.com/services/audit-assurance/comparing-compilations-reviews-audits/)).
- **Audit.** The CPA tests the numbers against outside evidence and the company's controls, and gives "reasonable assurance" ([Wegner CPAs](https://www.wegnercpas.com/services/audit-assurance/comparing-compilations-reviews-audits/)).

The company hires and pays the firm. The founder or finance lead sends the PDF. Paro, an accounting-software vendor, says a review runs far shorter and cheaper than an audit:

> "reviews often last a few days to several weeks, while audits typically take around three months to complete." ([Paro, vendor view](https://paro.ai/blog/financial-review-vs-audit/))

> "Review costs are often around half of audit fees." ([Paro, vendor view](https://paro.ai/blog/financial-review-vs-audit/))

## 2. At seed and at Series A

The research table marks audited or reviewed financials as not expected at pre-seed or seed and lighter at Series A ([data-room research](../20261022.02_research/research_data_room.md)). The sources mostly agree, with one inconsistency and one dissent.

**Seed: not expected.**

- Morrison Foerster, a law firm, says audits are often skipped until later rounds:

  > "it is not unusual for early stage companies to provide unaudited financials until later rounds of financing." ([Morrison Foerster, ScaleUp](https://scaleup.mofo.com/guidance/ask-a-mofo-common-provisions-in-venture-capital-term-sheets-information-and-observer-rights))

- Built In's founder cheatsheet by Becky Mancero says the same through Series A:

  > "Typically for the Series Seed to Series A round, the financial statements are unaudited given that the cost of obtaining audited financials is not the best use of the company's limited funds at the earlier stage." ([Built In](https://builtin.com/blog/founder-cheatsheet-information-inspection-and-observer-rights-venture-financing))

- Visible (vendor) warns against an empty placeholder:

  > "Empty folders with optimistic names (“Customer Reference Letters”, “Audited Financials”) at pre-seed and seed signal exactly what they look like." ([Visible, vendor view](https://visible.vc/blog/what-to-include-in-your-data-room/))

**Series A: optional to expected, depending on the source.**

- Visible's stage table marks audited or reviewed financials as lighter at Series A. Its prose then says "Series A founders need reviewed or audited financials, cohort analysis, unit economics, and a current 409A" ([Visible, vendor view](https://visible.vc/blog/what-to-include-in-your-data-room/)). The page disagrees with itself; I read "lighter" as the working answer.
- Built In says an audit requirement usually starts later:

  > "Typically, this audit requirement is not put in place until the Series B round but sometimes may be required earlier, particularly when the company is operating in a highly regulated industry." ([Built In](https://builtin.com/blog/founder-cheatsheet-information-inspection-and-observer-rights-venture-financing))

- Paro (vendor) agrees:

  > "For example, venture capital investors often start asking for audited financial statements once startups reach their Series B or Series C funding round ." ([Paro, vendor view](https://paro.ai/blog/financial-review-vs-audit/))

- Carta points to the period after the Series A:

  > "And many investors require later-stage startups to provide audited financials as part of their investment agreement." ([Carta](https://carta.com/learn/startups/financial-statements/financial-audits/))

- Haven, a startup-finance vendor, writes its audit checklist for "Series A founders" as if audits are normal then ([Haven, vendor view](https://www.usehaven.com/blog-posts/financial-audit-prep-checklist-for-series-a-founders-startup-guide)). I give this less weight because it cites no investor.
- a16z does not want audits sent up front:

  > "Tax returns, audits, and legal docs like office leases or employee offer letters. We're not lawyers or accountants! If we have a concern, we'll request the documents we need." ([Justine Moore, a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/))

- Cooley's sample request list, which counsel sends before closing a financing, asks for both kinds of statements, without a stage:

  > "Most recent audited financial statements and latest unaudited monthly financial statements." ([Cooley GO sample VC due diligence request list](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/))

**After closing,** audited statements come up as a contract term. A law-firm summary of the NVCA investors' rights agreement says investors "may negotiate to receive audited financial statements" and that only Major Investors get information rights ([Morrison Foerster, ScaleUp](https://scaleup.mofo.com/guidance/ask-a-mofo-common-provisions-in-venture-capital-term-sheets-information-and-observer-rights)). ValueAdd VC, a blog, puts the cost of a full audit at $15,000 to $60,000 and says companies before Series A are often given a carve-out ([ValueAdd VC](https://valueaddvc.com/blog/information-rights-in-venture-term-sheets-what-vcs-see-and-what-founders-control)).

## 3. What a first pass checks

1. Is there a signed report, and at what level: compilation, review or audit?
2. Who signed it, and is the firm real and independent of the company?
3. Which fiscal year does it cover, and how recent is it?
4. What is the opinion? For an audit: unqualified (clean), qualified, adverse, or disclaimer. For a review: the standard wording, or an exception.
5. Do the report's revenue, net loss, cash and total costs match the management P&L for the same year?
6. Do the notes describe revenue recognition, related-party items, debt and subsequent events in a way that fits the deck?
7. Does it carry a going-concern paragraph?

## 4. Green flags

- **A clean opinion on a recent year.** Carta lists the three outcomes of an audit: an unqualified opinion (also called a clean opinion), an adverse opinion, and a disclaimer of opinion ([Carta](https://carta.com/learn/startups/financial-statements/financial-audits/)). A clean opinion is the good one.

- **The accountant's numbers equal the management numbers.** The research table's reading step for this document is a comparison of reviewed numbers with management numbers ([data-room research](../20261022.02_research/research_data_room.md)). When they match, the management P&L has outside support for that year.
- **Evidence from outside the company.** A chartered-accountant journal explains why an audit counts for more than a management statement:

  > "Audit evidence is considered to be more reliable when obtained in a documented form directly by the auditor from sources independent of the entity being audited." ([BCA Journal](https://bcajonline.org/journal/external-confirmations-proving-existence-with-external-evidence/))

- **A firm used to VC-backed clients.** Carta advises a first-time company to work with an auditor its investors recommend ([Carta](https://carta.com/learn/startups/financial-statements/financial-audits/)). This is advice to founders, so it is a weak signal for investors.
- **The founder has the report ready at Series A.** Cooley's list treats it as something counsel asks for, so a room that already holds it shortens the list. This is my reading of those sources.

## 5. Red flags and pitfalls

**Common**

- **An empty "Audited Financials" folder or a claim with no report behind it** (Visible quote in section 2).
- **Management and accountant numbers that differ.** Paro adds a practical tie between statements and tax returns that auditors check:

  > "In addition, make sure to perform annual reconciliations between your company's financial statements and tax returns. Discrepancies between the two can trigger inquiries and cause delays during audits and reviews." ([Paro, vendor view](https://paro.ai/blog/financial-review-vs-audit/))

- **Calling a review or compilation an audit.** I found no source that documents founders doing this. I infer it from the three-level definitions above, so Tricorder reads the report's level from its own wording and never from the file name.
- **A qualified or adverse opinion, or a disclaimer.** Carta describes an adverse opinion as financial records "not aligned with GAAP" and "egregiously misstated" ([Carta](https://carta.com/learn/startups/financial-statements/financial-audits/)).

**Rare but serious**

- **An audit that relied on the company's own staff.** In the NS8 case, the criminal complaint (as posted by a Hacker News commenter; I could not open the filing myself) says an audit firm's employee was directed to have company staff pull the bank statements:

  > "The Auditor was directed by a more senior Audit Firm employee to have someone from NS8 log in to the online portal for each NS8 bank account, display the current account balance, and download monthly bank statements for fiscal year 2019." ([DOJ filing as posted by a Hacker News commenter](https://news.ycombinator.com/item?id=24522396))

  Another commenter, who describes audit work, explains the usual practice:

  > "You would not trust the account statements that the company gives you, you would get the same (hopefully) account statements yourself." ([Hacker News commenter PeterisP](https://news.ycombinator.com/item?id=24523476))

  CyberScoop reports the SEC's charge against the NS8 CEO:

  > "Adam Rogas, the co-founder and former CEO of the startup, touted bank statements showing payments from NS8 customers that never happened, according to the SEC." ([CyberScoop](https://www.cyberscoop.com/ns8-cyber-fraud-prevention-startup-adam-rogas-sec-fbi/))

  The lesson for Tricorder is that a signed report raises confidence in a year's numbers but does not remove the bank check. Tricorder never labels a piece "settled" because an accountant signed.

## 6. How Tricorder checks it

**What a script can check**

- 1.11 What the room cannot settle, `present(accountant_statements)`: is a file of this kind in the room?
- Proposed `management_vs_accountant_numbers`. For each fiscal year in the report, compare revenue, net loss, year-end cash and total operating costs with the sum of the management P&L for the same year: `gap = |report - management| / |management|`. Flag a line when the gap passes `match_tolerance`. The checklist lists this check as "not checked yet" ([CHECKLIST.md](../../ongoing/CHECKLIST.md), "Reviewed or audited numbers match management numbers").
- Proposed `report_year_is_recent`. Months between the report's fiscal year end and the data date; show the number and let the readout say "latest audited year is N months old".
- Proposed `report_balance_ties_to_bank`. Year-end cash in the report equals the bank statement balance on that date, when both are present.

**What needs a model to read**

- The assurance level, from the report's own wording: "audit", "review", "compilation", "reasonable assurance", "limited assurance", "no assurance". Quote the paragraph.
- The opinion type and any emphasis-of-matter or going-concern paragraph. Quote it.
- The firm's name, signature and date. Quote them.
- The notes: revenue recognition policy, related-party transactions, debt, commitments, subsequent events.
- Anything labelled "restated".

**What Tricorder cannot check**

- That the firm exists and signed this report. An operator calls the firm using contact details found independently, not the ones on the report.
- That the engagement was independent. Ask for the engagement letter.
- That the company's staff did not control what the accountant saw (the NS8 pattern). Only a direct bank confirmation addresses that, and it belongs to the accountant or the investor.

## 7. Which readout pieces it feeds

- **Traction and revenue:** the checklist places "Audited or reviewed financials" here.
- **Burn and runway:** net loss and year-end cash.

Checklist rows: Audited or reviewed financials (a document, lighter at Series A); Reviewed or audited numbers match management numbers (a check, not built yet) ([CHECKLIST.md](../../ongoing/CHECKLIST.md)).

## 8. If it is missing

- **Pre-seed and seed:** not a gap. The readout says "not expected at this stage" and leaves it off the ask list.
- **Series A:** a light gap. The sources split on whether it is expected, so it goes on the ask list as optional, after the items every source expects. It is never a red flag.

One-line ask for the founder: "If an outside accountant has reviewed or audited any year, please send the signed report and the statements it covers."

## 9. In the Hollis Voice room

Not in the room. The full room has 17 files and none is an accountant's report (checked in [hollis_financials_facts_output.json](raw/hollis_financials_facts_output.json)); the checklist records it as "not in the room". Hollis Voice is a Series A room, so this is the light gap in section 8. The company was founded in 2024 and the P&L inside the model is management accounts. No flag is planted for this document.

## 10. Sources

Each page is saved under [raw/audited-or-reviewed-financials/](raw/audited-or-reviewed-financials/).

| Source | Type | Saved file |
|---|---|---|
| [Morrison Foerster, ScaleUp](https://scaleup.mofo.com/guidance/ask-a-mofo-common-provisions-in-venture-capital-term-sheets-information-and-observer-rights) | law firm | scaleup_mofo_com_guidance_ask_a_mofo_common_provisions_in_venture_capital_term_sheets_information_and_observer.txt |
| [Built In founder cheatsheet](https://builtin.com/blog/founder-cheatsheet-information-inspection-and-observer-rights-venture-financing) | founder guide | builtin_com_blog_founder_cheatsheet_information_inspection_and_observer_rights_venture_financing.txt |
| [Nixon Peabody on the NVCA agreement](https://www.nixonpeabody.com/insights/articles/nvca-investor-rights-agreement) | law firm | nixonpeabody_com_insights_articles_nvca_investor_rights_agreement.txt |
| [ValueAdd VC](https://valueaddvc.com/blog/information-rights-in-venture-term-sheets-what-vcs-see-and-what-founders-control) | blog | valueaddvc_com_blog_information_rights_in_venture_term_sheets_what_vcs_see_and_what_founders_control.txt |
| [Cooley GO sample request list](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/) | law firm | cooley_vc_dd_request_list.txt, cooleygo_com_documents_sample_vc_due_diligence_request_list.txt |
| [Carta, financial audit preparation](https://carta.com/learn/startups/financial-statements/financial-audits/) | cap table vendor | carta_com_learn_startups_financial_statements_financial_audits.txt |
| [Paro](https://paro.ai/blog/financial-review-vs-audit/) | vendor | paro_ai_blog_financial_review_vs_audit.txt |
| [Haven](https://www.usehaven.com/blog-posts/financial-audit-prep-checklist-for-series-a-founders-startup-guide) | vendor | usehaven_com_blog_posts_financial_audit_prep_checklist_for_series_a_founders_startup_guide.txt |
| [Wegner CPAs](https://www.wegnercpas.com/services/audit-assurance/comparing-compilations-reviews-audits/) | accounting firm | wegnercpas_com_services_audit_assurance_comparing_compilations_reviews_audits.txt |
| [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/) | vendor | visible_vc_blog_what_to_include_in_your_data_room.txt |
| [a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/) | fund | a16z_com_the_insiders_guide_to_data_rooms_what_to_know_before_you_raise.txt |
| [BCA Journal](https://bcajonline.org/journal/external-confirmations-proving-existence-with-external-evidence/) | accountants' journal (India) | bcajonline_org_journal_external_confirmations_proving_existence_with_external_evidence.txt |
| [Hacker News, NS8 threads](https://news.ycombinator.com/item?id=24522396) | community | hn_item_24522396.json, hn_item_24520960.json |
| [CyberScoop, NS8](https://www.cyberscoop.com/ns8-cyber-fraud-prevention-startup-adam-rogas-sec-fbi/) | news | in raw/bank-statements/ |
| [Kruze, VC diligence lists](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/), [Eagle Rock CFO](https://www.eaglerockcfo.com/blog/series-a-preparation/data-room-checklist), [DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/) | accounting and vendor | kruzeconsulting_com_what_are_examples_of_vc_due_diligence_check_lists.txt, eaglerockcfo_*.txt, docsend_com_blog_due_diligence_checklist.txt |

Pages that blocked me: the Department of Justice press releases for NS8 and Joonko, the SEC complaint for NS8, and SEC litigation releases returned 403 or an empty page. The Hacker News comments quote the NS8 filing; I did not read the filing.
