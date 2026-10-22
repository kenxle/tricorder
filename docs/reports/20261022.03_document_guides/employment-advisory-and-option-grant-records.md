# Employment, advisory and option grant records

Document guide for Tricorder's scans, checklist and memo. Written 2026-10-22. Sources are saved under [raw/employment-advisory-and-option-grant-records/](raw/employment-advisory-and-option-grant-records/). Quotes are checked word for word against the saved pages by [build_quotes_people.py](raw/_people_tools/build_quotes_people.py); results are in [quotes_people.csv](quotes_people.csv). Facts about the Hollis Voice room come from [room_facts_people.py](raw/hiring-plan-and-future-org/room_facts_people.py) and its output [room_facts_people.out.txt](raw/hiring-plan-and-future-org/room_facts_people.out.txt).

Related guides cover the cap table itself, the 409A valuation, board and stockholder minutes, IP assignment and incorporation documents. This guide covers the paper behind each person's pay and stake: offer letters and employment agreements, advisor agreements, option grants and the founders' vesting. Nothing here is legal advice. Where a point is a legal call, the guide says to leave it to a lawyer.

## What it is

The signed documents that say what each person was promised and what they hold.

- **Employment:** offer letters, founder service agreements, key-employee agreements, plus the confidentiality and invention-assignment agreements that go with them.
- **Advisory:** one agreement per advisor, usually a standard form with equity that vests over time.
- **Option grants:** the equity plan, a grant notice and agreement for each holder, and a ledger (a list of every grant with holder, date, shares, strike price and vesting).
- **Founder stock:** purchase agreements with vesting, and copies of each founder's 83(b) tax filing.

Company counsel and an equity platform such as Carta or Pulley prepare them. They arrive as a folder of PDFs and a spreadsheet export of the ledger.

## At seed and at Series A

The research table marks the document set as absent at pre-seed, lighter at seed and expected at Series A. See [the 30-document table](../20261022.02_research/research_data_room.md). Visible shows the split: employment and advisory agreements are left out at pre-seed and lighter at seed, and the same holds for "Equity grant records and option pool" ([Visible, vendor](https://visible.vc/blog/what-to-include-in-your-data-room/)). It adds "By Series A, employment and advisory agreements with IP assignment and key-person retention terms become standard diligence asks."

- **Pre-seed still has founder paper.** Hustle Fund's pre-seed baseline includes "Founder equity purchase and vesting records, plus approvals for issuances" ([Hustle Fund checklist](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)).
- **Seed:** an option-pool summary, a stock plan and a grant ledger. Papermark's YC room puts "stock plan and grant ledger" in the pre-wire legal folder ([Papermark, vendor](https://www.papermark.com/blog/data-room-for-yc-startups)).
- **Series A:** counsel ties every grant on the cap table to a signed document and a board approval. Peony lists "Employment agreements, offer letters, and the option-grant records behind the pool" among the Series A items ([Peony, vendor](https://www.peony.ink/blog/series-a-data-room)). Cooley's request list asks for "Current shareholder and optionee lists, including issuance dates and original issuance price." and "Copies of offer letters." ([Cooley GO sample list](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/)).

DocSend's 2026 checklist puts the same ground under "Shareholder information and agreements" (vesting schedules) and "Equity grants", defined as "Equity already promised to early employees, customers or consultants." ([DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/)). DocSend frames the whole list as post-term-sheet work and names no stage.

## What a first pass checks

1. Does every holder of options or advisor shares on the cap table have a grant document and a ledger line?
2. Did the board approve each grant before it was made? Carta: "The board has to approve all stock option grants ahead of time, either at a board meeting or by unanimous written consent. If your board hasn’t approved an option grant, no options have actually been granted." ([Carta](https://carta.com/blog/issuing-options-mistakes/)).
3. Was the strike price at or above the 409A value on the grant date, and was that 409A current? Carta: "To avail yourself of the 409A safe harbor with the IRS, you need to get a new 409A valuation every 12 months, or sooner if you have a material event or transaction, (like a new financing round)."
4. Do the founders have vesting, and is there proof the 83(b) election was filed? Holloway's list of documents to expect includes "copies of Section 83(b) elections the founders filed with the IRS, if the founders’ shares were subject to vesting" ([Holloway Guide](https://www.holloway.com/g/angel-investing/sections/legal-diligence-on-other-founder-board-of-directors-and-employee-issues)).
5. Does each advisor have a written agreement with a scope, a vesting schedule and a grant size in a normal range?
6. Does every employee have an offer letter, an invention-assignment agreement and a confidentiality agreement? Holloway: "All employees should have signed an offer letter or employment agreement, and also an IP assignment agreement and a confidentiality or non-disclosure agreement." ([Holloway Guide, Wallin and Baltaxe](https://www.holloway.com/g/angel-investing/sections/legal-diligence-on-other-founder-board-of-directors-and-employee-issues)).
7. Who is a contractor and who is an employee? Holloway: "Make sure to ask the entrepreneur who is an employee and who is a contractor."
8. Is any equity promised but not granted, and has anyone left with a claim?
9. Do the numbers in the deck, the cap table and the ledger agree?

## Green flags

- **Everything reconciles to one source.** OnlyCFO, a finance newsletter with a guest post by an in-house lawyer: "A clean, single-source-of-truth cap table is the difference between a smooth raise and a nine-figure haircut." ([OnlyCFO](https://www.onlycfo.io/p/cap-table-nightmares)).
- **Grants priced off a current 409A and approved before they were made.** Carta, above.
- **Founders on vesting, with proof of the 83(b) filing.** Terms.law, a law-firm memo: "The certified-mail return receipt is the documentary evidence I would not skip." ([terms.law](https://terms.law/insights/section-83b-election-when-founder-forgets.html)). Cooley GO: "Founder’s Stock is often subject to a vesting schedule." and the typical schedule "vests in monthly or quarterly increments over four years" ([Cooley GO](https://www.cooleygo.com/founder-basics-founders-stock/)).
- **Advisors on standard terms with a purpose.** The Holloway Guide to Equity Compensation: "a common vesting schedule for an advisor is two years with a three-month cliff". Advisor grants "typically have a longer exercise window post termination of service, and will usually have single trigger acceleration on an acquisition" ([Holloway Guide](https://holloway.com/g/equity-compensation/sections/typical-startup-advisor-equity-levels)). It reproduces the Founder Institute's FAST ranges, which run from 0.15 percent to 1.00 percent by role and stage.
- **Real equity for the people who matter.** Jonathan Hua, a former early-stage investor, flags "Key personnel with almost no equity , like a VP of Engineering holding 0.1% fully diluted at a company raising a Series C, is a huge retention risk I’ll price into the term sheet whether the founder addresses it or not." ([The Data Room, Hua, Sep 2026](https://thedataroom.substack.com/p/how-a-vc-does-due-diligence-on-your-company)).
- **Signed invention assignments from everyone.** Papermark: "IP assignment. Every founder, employee, contractor, and friend-who-helped-for-a-weekend needs a signed agreement assigning their work to the company."

## Red flags and pitfalls

**Common**

- **Promised grants the board never approved.** OnlyCFO: "Phantom grants : promised but never board-approved." and "No board approval = no grant." Founders CPA, an accounting firm, lists "option grants promised in offer letters but never board-approved or issued (found years later, at exercise or exit)" first in its list "From the diligence trenches, in descending frequency" ([Founders CPA](https://founderscpa.com/blog/common-startup-cap-table-mistakes)). Peony names the same fault: "a grant you promised a key hire or advisor with no signed agreement on file".
- **A stale or missing 409A.** OnlyCFO: "If your strike price is below FMV, it’s a Section 409A violation." Fixing a late grant costs more because "The board can only grant stock options at the current fair market value (FMV), so simply granting the stock options later isn’t a solution when the FMV increased 100x." (same page).
- **Missing IP assignments.** Visible: "The most consequential gap in this folder at any stage is the IP assignment from former contractors or employees." Papermark calls it "the single most common finding at Series A and the easiest to fix at seed". Peony: "founders, early employees, or contractors who never assigned their work to the company".
- **Founders with no vesting, or a missed 83(b) election.** Founders CPA lists "83(b) elections missed on founder restricted stock (a thirty-day window with no cure, converting cheap early gains into ordinary income later)". Gust, a vendor: "You have 30 days after the date of the stock grant to file it." Terms.law notes the Code has no late election: "The Code does not provide for a late 83(b) election." It also describes narrow, case-by-case relief the IRS has granted rarely. Cake (vendor): "the issue frequently surfaces during due diligence at Series A or later." ([Cake](https://www.cakeequity.com/guides/83b-election-reminder-equity)).
- **Advisor equity with nothing attached to it.** Hua: "Advisor equity that never got attached to deliverables , such as eight advisors holding 2% each with vesting schedules that already expired, signals a judgment problem more than a cap table problem." He also names "a large advisor grant nobody negotiated hard on" as a reason a co-founder ends up with low ownership.
- **Several versions of the cap table.** OnlyCFO: "Multiple truths = no truth. If two versions exist, investors assume there’s a third one with even scarier numbers."
- **Verbal promises.** A founder-diligence vendor lists "Undocumented agreements: Verbal promises to advisors or early employees that aren't reflected in legal documentation" ([Angel Investors Network, vendor](https://angelinvestorsnetwork.com/startups/founder-diligence-what-investors-actually-check)).
- **Contractor misclassification.** Fisher Phillips, an employment-law firm: "Misclassification of workers is one of the most common – and most costly – issues uncovered during due diligence." ([Fisher Phillips](https://www.fisherphillips.com/en/news-insights/steps-for-built-to-sell-tech-startups-to-lock-down-employment-law-compliance.html)). Holloway adds that the company can end up with a tax liability. This is a legal call, so Tricorder only lists who is a contractor.

**Rare but serious**

- **A grant discovered mid-diligence.** OnlyCFO tells of "A Series B company discovered, mid-diligence, that three engineers thought they had 1% each. The CEO had “promised it.” The board had not." It is an unnamed anecdote.
- **A deck that disagrees with the cap table.** Hua: "A deck that claims 55% founder ownership and a cap table that shows 48% fully diluted registers as the first real crack in credibility, and is far more damaging than a simple rounding error would be."
- **A former employee with a claim.** Holloway: "Many expensive lawsuits have arisen from former early employees who might have been promised stock or who had not vested their stock before they were terminated or quit."
- **Accrued salaries or payback plans.** Holloway: "Check that a company is not carrying accrued or deferred salaries on its balance sheet."
- **Founders with no vesting at the Series A.** Cooley GO notes the schedule "may be imposed later as a condition of investment by outside investors". Fenwick's legal guide, undated and written for a TiE workshop, says "Venture capitalists require vesting as a condition to funding your company." ([Fenwick](https://assets.fenwick.com/legacy/FenwickDocuments/Start-up_Legal_Resource_Guide.pdf)).

## How Tricorder checks it

**What a script can check**

- Already planned: [FRAMEWORKS 1.10](../../ongoing/FRAMEWORKS.md), question 5, "Are there instruments or grants in the cap table with no document in the room?" It covers checklist item C82 and runs after Saturday. Entry 1.11 tests whether IP assignment files are present at all (C83).
- Proposed `grant_ledger_reconcile`: `SUM(ledger shares) = options granted on the cap table` and `COUNT(distinct ledger holders) = holders on the cap table`.
- Proposed `grant_has_approval`: for each grant, a board consent dated on or before the grant date. It needs the minutes (see the board minutes guide).
- Proposed `strike_at_or_above_fmv`: `strike ≥ fmv_409a(effective at grant date)`, `409a_age_months(grant date) ≤ 12`, and no financing event between the 409A date and the grant date.
- Proposed `founder_vesting_present`: each founder row has a schedule; record cliff and months; flag a founder fully vested at incorporation.
- Proposed `83b_copy_present`: a file exists for each founder whose stock vests. Tricorder checks only that the file is there.
- Proposed `advisor_grant_range`: show each advisor grant as a percent, the sum, and where it sits against the FAST range (0.15 to 1.00 percent). Context only.
- Proposed `signed_docs_per_person`: for each name on the staff list, an offer letter and an invention-assignment file exist.
- Proposed `pool_arithmetic`: `granted + available = pool`, with the pool as a percent before and after the round.

**What needs a model to read**

- Grant agreements and offer letters: strike, vesting, cliff, acceleration, exercise window, repurchase rights and any "promised" equity language.
- Advisor agreements: scope of work, deliverables, term.
- Compare each term with the ledger and write a claim with the clause quoted and the page.
- It must not say a grant is void or a tax is owed. It lists the difference and the clause, and leaves the legal call to a lawyer.

**What Tricorder cannot check (leave to the operator)**

- Whether the board really met and approved. Only the minute book and a lawyer's read settle it.
- Whether an 83(b) form was mailed and received. The certified-mail receipt is the evidence; the IRS holds the record.
- Whether a person is a contractor or an employee in law, and what the tax result is.
- Whether verbal promises exist. Ask the founders, and consider a call with a former employee.
- Whether a missing document can be fixed. That is for the company's counsel.

## Readout pieces and checklist items

- **Legal and cap table** piece, and **team** (retention).
- Checklist items ([CHECKLIST](../../ongoing/CHECKLIST.md)): C78 (employment, advisory and option grant records), C82 (every instrument and grant has a document), C83 (every founder and contractor signed an IP assignment), C76 (IP and invention assignment agreements), C73 and C85 (409A valuation, current), C77 and C84 (minutes approve each financing), C72 and C81 (cap table adds to 100 percent). C78 is marked "not checked yet".

## If it is missing

- **Pre-seed:** not a gap, apart from the founders' own vesting and 83(b) paper.
- **Seed:** a light gap. Ask for the ledger and any advisor agreements. Not a red flag.
- **Series A:** a gap with a firm ask. If the cap table shows options held by named people and the room holds no ledger or agreements, say so as a difference in reporting and put it to the founder. The research says a missing document is a question for the operator ([data-room research, 1.5](../20261022.02_research/research_data_room.md)).
- **Ask-list line:** "Please send the option grant ledger (holder, date, shares, strike, vesting, board approval date) with the signed grant agreements, every advisor agreement, and the founders' vesting and 83(b) filings."

## In the Hollis Voice room

- **Not in the room.** There is no grant ledger, no equity plan, no offer letter, no advisor agreement and no 409A. The 17 files in the full room do not include any of them ([data room README](../../../data_room/README.md)).
- **What the cap table shows.** "Options granted (11 holders)" is 1,148,000 shares, 7.96 percent fully diluted. "Options available" is 1,034,000 shares, 7.17 percent. The whole pool is 2,182,000 shares, 15.13 percent before the Series A and 12.61 percent after it. There are no advisor rows (all from [room_facts_people.out.txt](raw/hiring-plan-and-future-org/room_facts_people.out.txt)). The cap table is the clean decoy DC3, so a scan must stay quiet on its arithmetic.
- **No planted flag for this document.** The room is silent, which makes it a clean example of a "not in the room" gap. `pool_arithmetic` passes. `grant_ledger_reconcile` cannot run.
- **What the ask list would hold.** The ledger for the 11 holders, the grant agreements, the equity plan, the current 409A, and whether the part-time Controller is an employee or a contractor.

## Sources

Each page is saved in [raw/employment-advisory-and-option-grant-records/](raw/employment-advisory-and-option-grant-records/). Vendor views are marked.

- [Carta, issuing options: 5 common mistakes](https://carta.com/blog/issuing-options-mistakes/) (vendor) | [saved](raw/employment-advisory-and-option-grant-records/carta_com_blog_issuing_options_mistakes.txt)
- [OnlyCFO, cap table nightmares](https://www.onlycfo.io/p/cap-table-nightmares) (guest post by in-house counsel) | [saved](raw/employment-advisory-and-option-grant-records/onlycfo_io_p_cap_table_nightmares.txt)
- [Founders CPA, common startup cap table mistakes](https://founderscpa.com/blog/common-startup-cap-table-mistakes) (accounting firm) | [saved](raw/employment-advisory-and-option-grant-records/founderscpa_com_blog_common_startup_cap_table_mistakes.txt)
- [Holloway Guide, Angel Investing (Wallin and Baltaxe): legal diligence on founder, board and employee issues](https://www.holloway.com/g/angel-investing/sections/legal-diligence-on-other-founder-board-of-directors-and-employee-issues) | [saved](raw/employment-advisory-and-option-grant-records/holloway_com_g_angel_investing_sections_legal_diligence_on_other_founder_board_of_directors_and_empl.txt)
- [Holloway Guide to Equity Compensation, typical advisor equity levels](https://holloway.com/g/equity-compensation/sections/typical-startup-advisor-equity-levels) | [saved](raw/employment-advisory-and-option-grant-records/holloway_com_g_equity_compensation_sections_typical_startup_advisor_equity_levels.txt)
- [Cooley GO, founder's stock, vesting and founder departures](https://www.cooleygo.com/founder-basics-founders-stock/) | [saved](raw/employment-advisory-and-option-grant-records/cooleygo_com_founder_basics_founders_stock.txt)
- [Cooley GO, sample VC due diligence request list](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/) | [saved text](raw/employment-advisory-and-option-grant-records/cooley_vc_dd_request_list.txt) and [saved PDF](raw/employment-advisory-and-option-grant-records/cooley_vc_dd_request_list.pdf)
- [Fenwick, start-up legal resource guide (PDF, undated)](https://assets.fenwick.com/legacy/FenwickDocuments/Start-up_Legal_Resource_Guide.pdf) | [saved PDF](raw/employment-advisory-and-option-grant-records/fenwick_start_up_legal_resource_guide.pdf) and [text](raw/employment-advisory-and-option-grant-records/fenwick_start_up_legal_resource_guide.txt)
- [terms.law, when a founder forgets the 83(b) election](https://terms.law/insights/section-83b-election-when-founder-forgets.html) (law-firm memo) | [saved](raw/employment-advisory-and-option-grant-records/terms_law_insights_section_83b_election_when_founder_forgets_html.txt)
- [Gust, missing the 83(b) deadline](https://gust.com/blog/missing-the-83b-deadline-can-spell-disaster-for-founders/) (vendor) | [saved](raw/employment-advisory-and-option-grant-records/gust_com_blog_missing_the_83b_deadline_can_spell_disaster_for_founders.txt)
- [Cake, 83(b) reminders](https://www.cakeequity.com/guides/83b-election-reminder-equity) (vendor) | [saved](raw/employment-advisory-and-option-grant-records/cakeequity_com_guides_83b_election_reminder_equity.txt)
- [Fisher Phillips, employment law steps for tech startups](https://www.fisherphillips.com/en/news-insights/steps-for-built-to-sell-tech-startups-to-lock-down-employment-law-compliance.html) | [saved](raw/employment-advisory-and-option-grant-records/fisherphillips_com_en_news_insights_steps_for_built_to_sell_tech_startups_to_lock_down_employment_la.txt)
- [Visible, what to include in your data room](https://visible.vc/blog/what-to-include-in-your-data-room/) (vendor) | [saved](raw/employment-advisory-and-option-grant-records/visible_vc_blog_what_to_include_in_your_data_room.txt)
- [Papermark, data room for YC startups](https://www.papermark.com/blog/data-room-for-yc-startups) (vendor) | [saved](raw/employment-advisory-and-option-grant-records/papermark_com_blog_data_room_for_yc_startups.txt)
- [Peony, Series A data room](https://www.peony.ink/blog/series-a-data-room) (vendor) | [saved](raw/employment-advisory-and-option-grant-records/peony_ink_blog_series_a_data_room.txt)
- [SeedLegals, data room help](https://help.seedlegals.com/en/data-room-how-it-can-enhance-your-funding-round) (vendor) | [saved](raw/employment-advisory-and-option-grant-records/help_seedlegals_com_en_data_room_how_it_can_enhance_your_funding_round.txt)
- [DocSend, the startup fundraising due diligence checklist](https://www.docsend.com/blog/due-diligence-checklist/) | [saved](raw/employment-advisory-and-option-grant-records/docsend_com_blog_due_diligence_checklist.txt) (read through a browser by an earlier session)
- [Hustle Fund, angel investing due diligence checklist](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step) | [saved](raw/employment-advisory-and-option-grant-records/hustlefund_vc_post_angel_squad_angel_investing_due_diligence_checklist_step_by_step.txt)
- [The Data Room (Jonathan Hua), how a VC does due diligence on your company](https://thedataroom.substack.com/p/how-a-vc-does-due-diligence-on-your-company) | [saved](raw/employment-advisory-and-option-grant-records/web_thedataroom_substack_com_p_how_a_vc_does_due_diligence_on_your_company.txt)
- [Angel Investors Network, founder diligence](https://angelinvestorsnetwork.com/startups/founder-diligence-what-investors-actually-check) (vendor) | [saved](raw/employment-advisory-and-option-grant-records/angelinvestorsnetwork_com_startups_founder_diligence_what_investors_actually_check.txt)
- [Kruze, VC due diligence checklists](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/) | [saved](raw/employment-advisory-and-option-grant-records/kruzeconsulting_com_what_are_examples_of_vc_due_diligence_check_lists.txt)
- Read but not cited: [Qubit Capital](raw/employment-advisory-and-option-grant-records/qubit_capital_blog_cap_table_mistakes_series_a.txt), [Promise Legal on cap tables](raw/employment-advisory-and-option-grant-records/blog_promise_legal_startup_central_why_legal_oversight_startup_cap_table_non_negotiable.txt), [Promise Legal on advisor agreements](raw/employment-advisory-and-option-grant-records/blog_promise_legal_startup_central_startup_advisor_agreement_advisory_board_guide.txt), [EO Network (eShares)](raw/employment-advisory-and-option-grant-records/eonetwork_org_blog_10_common_cap_table_mistakes.txt), [Revision Legal](raw/employment-advisory-and-option-grant-records/revisionlegal_com_corporate_revision_legal_ip_assignment_mistakes_startup_acquisition_due_diligence.txt), [Venture Hacks](raw/employment-advisory-and-option-grant-records/venturehacks_com_option_pool_shuffle.txt), [Orrick on vesting](raw/employment-advisory-and-option-grant-records/orrick_com_en_tech_studio_resources_faq_what_is_vesting_should_initial_shares_sold_to_founders_be_su.txt), the [Founder Institute FAST page](raw/employment-advisory-and-option-grant-records/fi_co_contents_fast.txt) (mostly navigation text) and the [Carta 409A guide](raw/employment-advisory-and-option-grant-records/carta_com_learn_startups_equity_management_409a_valuation.txt).

Pages that blocked automated fetching or returned nothing: Fenwick's 409A paper at the old fenwick.com address (HTTP 404), and Carta's advisor-shares guide and Cooley GO's 83(b) article at the addresses I guessed (HTTP 404). No search result was a 403.
