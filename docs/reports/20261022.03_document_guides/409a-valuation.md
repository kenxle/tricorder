# 409A valuation

Written 2026-10-22 for the Tricorder document guides. Quotes are checked word for word against saved pages (see `quotes_equity.csv`). Many sources on this topic are valuation or equity-software vendors; they are marked. Rules here are summaries for a reader, not tax advice.

**In one line:** a 409A report tells the reader whether the company prices its stock options legally, and the one question that matters is whether the report is current for every grant made under it.

## 1. What it is

A 409A valuation is an outside appraisal of what the company's common stock is worth. The number sets the lowest price at which options can be granted. CRV (a fund) describes it as:

> "an independent appraisal that sets the fair market value of your common stock and determines the strike price your employees will pay to exercise their options." ([CRV](https://crv.com/content/409a-valuation-before-series-a))

A valuation firm or a cap table platform prepares it, using the company's financials, cap table, projections and round terms. It arrives as a PDF report with an effective date, a method, a common stock price per share and, usually, the preferred price it was built from. The board adopts it before it prices grants.

## 2. At seed and at Series A

The data-room research marks it N, L, Y for pre-seed, seed and Series A: leave it out at pre-seed, lighter at seed, include at Series A ([research_data_room.md](../20261022.02_research/research_data_room.md), row 14). Kruze's checklist, a vendor view, asks for the last two valuations and marks them No at pre-seed, Maybe at seed and Yes from Series A on ([Kruze](https://kruzeconsulting.com/blog/due-diligence-checklist/); [kruze_stage_rows.csv](raw/409a-valuation/kruze_stage_rows.csv)). Hustle Fund puts it in the seed additions: "Equity plan, grant records, and the latest valuation used for option pricing, if applicable." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))

- **At seed**, a report exists only if the company has granted options. Many companies get the first one around their first financing.
- **At Series A**, it is expected, and the history matters. CRV: "Series A investors view your 409A compliance history as a signal of how well you run your company." ([CRV](https://crv.com/content/409a-valuation-before-series-a)) A Series A is also a trigger for a new report. CRV: "Most companies treat a financing round as a material event, so you should assume you will need to refresh your 409A promptly after closing." ([CRV](https://crv.com/content/409a-valuation-before-series-a))

## 3. What a first pass checks

In order:

1. Is there a report from an independent provider, with an effective date?
2. Is the effective date within 12 months of today and of the latest option grant?
3. Did a financing (a priced round, or a SAFE or note with a cap), a down round, acquisition talks or another big event happen after the effective date? If so, is there a newer report?
4. Is the common price below the preferred price? That is normal.
5. Over time, does the common price rise as the company raises and grows?
6. Was every option granted at or above the common price in force on the grant date?
7. Did the board adopt the report and approve each grant?
8. Do the facts printed in the report (revenue, cash, share counts, round terms) match the rest of the room?

## 4. Green flags

- **A current report from an independent provider.** CRV: "You must price every option granted at or above the FMV from your most recent valid 409A, and an old number or founder estimate will not provide safe harbor protection." ([CRV](https://crv.com/content/409a-valuation-before-series-a))
- **A refresh after each round.** Burkland, a fractional CFO firm (vendor): "Be sure to get new 409(a) valuations done after each investment round, material event, or twelve months from your last one." ([Burkland](https://burklandassociates.com/2021/11/02/surviving-due-diligence-part-3-cap-tables/))
- **A sensible history.** CRV says Series A readers "look for a logical progression: early valuations should be low and should increase as the company raises rounds and hits milestones." ([CRV](https://crv.com/content/409a-valuation-before-series-a))
- **The board adopted it.** CRV counts "ensuring board documentation of each valuation" among the habits that prevent stalls. ([CRV](https://crv.com/content/409a-valuation-before-series-a))
- **The company reads its own report.** The same CRV passage lists "reading the report before using it" ([CRV](https://crv.com/content/409a-valuation-before-series-a)). A founder who can say why the common price sits below the preferred price shows it.
- **The report agrees with the room.** An appraiser asks for financial statements, projections and a summary of business developments (Redwood Valuation, a valuation vendor), so a report is a third party's copy of the company's numbers on one date. When those numbers match the deck and model, that is corroboration from a source outside the company. ([Redwood](https://www.redwoodvaluation.com/blog/409a-valuation-refresh))

## 5. Red flags and pitfalls

- **Options granted with no 409A at all (common).** CRV lists "Waiting too long for the first valuation" among "These four mistakes account for the majority of 409A problems that surface during fundraising". ([CRV](https://crv.com/content/409a-valuation-before-series-a)) CRV also says a founder estimate gets no safe harbor, and that the penalties land on employees: "The penalties are severe, and they fall on your employees, not your company." ([CRV](https://crv.com/content/409a-valuation-before-series-a)) Cake Equity (vendor): "The compliance risk falls primarily on the employee, not the company." ([Cake Equity](https://www.cakeequity.com/guides/409a-required-before-issuing-stock-options))
- **A report older than 12 months.** Redwood: "the 12-month clock runs from the effective date of the valuation, not the date the report was delivered." ([Redwood](https://www.redwoodvaluation.com/blog/409a-valuation-refresh))
- **A financing after the report with no refresh (common).** CRV's same list names "Using an outdated valuation after a funding event" ([CRV](https://crv.com/content/409a-valuation-before-series-a)). Redwood says "Either condition can make continued reliance unreasonable", meaning age or new information that may materially affect value. For SAFEs and notes the test is case by case. Redwood notes there is no fixed 90-day rule: "There is no regulatory requirement to obtain a new 409A valuation within 90 days after a material event." ([Redwood](https://www.redwoodvaluation.com/blog/409a-valuation-refresh))
- **A low strike set before a hot round and never refreshed.** Angel Investors Network (vendor): "If a company has been granting options on an expired report, ask how many grants went out and who is fixing them." The same piece says "A low common value is not a red flag by itself, given the preferred gap above." ([Angel Investors Network](https://angelinvestorsnetwork.com/angel-investing/409a-valuation-what-investors-should-check))
- **Flat values through obvious growth (less common).** CRV: "Flat 409A values during obvious periods of growth raise questions." ([CRV](https://crv.com/content/409a-valuation-before-series-a))
- **Grants priced below the common price in force (rare but serious).** The cost lands in diligence. OneGC (vendor): "Diligence readiness: Acquirers and investors check 409A compliance; gaps become escrow holdbacks and re-pricing exercises." ([OneGC](https://onegc.com/blog/409a-valuation-cost-and-when-you-need-one))
- **No board approval for the grants.** Holloway's guide, written by two lawyers: "All option grants must be approved by the Board, and priced at the time of board approval." ([Holloway](https://www.holloway.com/g/angel-investing/sections/legal-due-diligence-for-angel-investments))
- **A reader's mistake: treating the gap to the preferred price as a discount.** CRV: "A 409A values only common stock, which will almost always produce a number lower than your fundraising valuation. That outcome is normal and expected." ([CRV](https://crv.com/content/409a-valuation-before-series-a)) A Hacker News commenter, grellas, explains the same point at length: "They are two different measures, each used for a distinct purpose, and are quite compatible with one another." ([Hacker News](https://news.ycombinator.com/item?id=5799229)) This is one commenter's explanation, not an investor's statement.
- **The exposure is in later grants.** Redwood says options already granted under a then-current valuation "are typically not put at risk solely because a later material event occurs", so the exposure sits with grants made after the report went stale. ([Redwood](https://www.redwoodvaluation.com/blog/409a-valuation-refresh))

## 6. How Tricorder checks it

No FRAMEWORKS entry covers this document yet (the checklist marks it "not checked yet"). The checks below are proposals.

### What a script can check

A model first reads the report and the option ledger into fields (below). Then scripts compute. Date math uses a date tool.

- **`409a_age`** (proposed). Formula: `months_old(grant) = months_between(effective_date, grant_date)`. Flag a grant when this is over 12. Run it for today and for the room's as-of date too.
- **`409a_event_gap`** (proposed). For each material event with date `d` (priced round close, SAFE or note with a cap, down round, acquisition talks): flag when `effective_date < d ≤ grant_date` and no later valuation is in the room. Events come from the prior-financing papers and the cap table.
- **`strike_vs_fmv`** (proposed). For each grant: `strike − common_fmv(valuation in force at grant date)`. List any negative result.
- **`409a_progression`** (proposed, report only). The series of (effective date, common price) with the change between neighbors and the preferred price at the time. List flat runs as questions.
- **`common_to_preferred_ratio`** (proposed, report only). `common_fmv ÷ preferred_price`. No threshold; show the number.
- **`409a_inputs_match_room`** (proposed). Compare revenue, cash and share counts printed in the report with the deck, model and cap table, within `match_tolerance`.

### What needs a model to read

- The report's effective date and delivery date, provider name and independence statement, method (market approach, income approach, asset approach; option pricing method; discount for lack of marketability), equity value, share counts, preferred price and common price. It must quote each.
- The option ledger: grant date, number, strike, holder.
- The board consent that adopts the report and the one that approves the grants (see the minutes guide).

### What Tricorder cannot check and leaves to the operator

- Whether the provider is independent and qualified in the legal sense.
- Whether an event was "material". Redwood: that is "a facts-and-circumstances reasonableness test, not a checklist". A tax lawyer decides.
- Whether past grants were mispriced and how to cure that.
- Whether the report's inputs were true. The report restates what the company told the appraiser.

## 7. Which readout pieces it feeds

- **Legal and cap table**, mainly.
- It touches **team** only through the option records.

Checklist items ([CHECKLIST.md](../../ongoing/CHECKLIST.md)): 409A valuation (the document); 409A valuation is current; employment, advisory and option grant records; every instrument and grant on the cap table has a document.

## 8. If it is missing

- **Pre-seed:** not expected. Nothing to flag.
- **Seed:** a gap only if the cap table shows options granted. Hustle Fund's "if applicable" is the test. The label is `watch`, with an ask.
- **Series A:** a gap, and a likely red flag if options are outstanding and no report exists, because Kruze marks it Yes at this stage and CRV names the first-grant rule. The call on how serious it is belongs to the operator.

**Ask-list line:** "Please send the latest 409A report and the one before it, the option grant ledger with grant dates and strike prices, and the board approval for each grant."

## 9. In the Hollis Voice room

**Not in the room.** The room has no 409A report and no option ledger. It does show options: the cap table lists 1,148,000 options granted to 11 holders and 1,034,000 available. So options are outstanding and the strike prices cannot be tested. The expense ledger has no line for a valuation provider (its vendors include Pembry Legal Services for legal fees and Dunmore Accounting Group for bookkeeping and tax), though a cap table platform could bundle one. There is no planted flag. At Series A this is a gap and an ask.

Timing the operator would test if the report arrives: the 2025 SAFE of $3,500,000 on a $28,000,000 cap is a financing event, so a report dated before it would be stale for later grants (Redwood's SAFE point).

## 10. Sources

Each page is saved under [raw/409a-valuation/](raw/409a-valuation/).

- [CRV, 409A valuation: why you need one before Series A](https://crv.com/content/409a-valuation-before-series-a), [saved](raw/409a-valuation/crv_com_content_409a_valuation_before_series_a.txt). Fund view.
- [Hustle Fund, Angel investing due diligence checklist](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step), [saved](raw/409a-valuation/hustlefund_vc_post_angel_squad_angel_investing_due_diligence_checklist_step_by_step.txt). Fund view.
- [Redwood Valuation, 409A refresh schedule](https://www.redwoodvaluation.com/blog/409a-valuation-refresh), [saved](raw/409a-valuation/redwoodvaluation_com_blog_409a_valuation_refresh.txt). Valuation vendor; cites Treasury Regulation 1.409A-1(b)(5)(iv)(B).
- [Cake Equity, Is a 409A required before issuing stock options](https://www.cakeequity.com/guides/409a-required-before-issuing-stock-options), [saved](raw/409a-valuation/cakeequity_com_guides_409a_required_before_issuing_stock_options.txt). Equity software vendor.
- [OneGC, 409A valuation cost and when you need one](https://onegc.com/blog/409a-valuation-cost-and-when-you-need-one), [saved](raw/409a-valuation/onegc_com_blog_409a_valuation_cost_and_when_you_need_one.txt). Legal services vendor.
- [Angel Investors Network, 409A valuation: what angel investors should check](https://angelinvestorsnetwork.com/angel-investing/409a-valuation-what-investors-should-check), [saved](raw/409a-valuation/angelinvestorsnetwork_com_angel_investing_409a_valuation_what_investors_should_check.txt). Vendor.
- [Burkland Associates, Surviving due diligence part 3](https://burklandassociates.com/2021/11/02/surviving-due-diligence-part-3-cap-tables/), [saved](raw/409a-valuation/burklandassociates_com_2021_11_02_surviving_due_diligence_part_3_cap_tables.txt). Vendor.
- [Holloway, Legal due diligence for angel investments](https://www.holloway.com/g/angel-investing/sections/legal-due-diligence-for-angel-investments), [saved](raw/409a-valuation/holloway_com_g_angel_investing_sections_legal_due_diligence_for_angel_investments.txt). Two lawyers.
- [Kruze, VC due diligence checklist](https://kruzeconsulting.com/blog/due-diligence-checklist/), [saved](raw/409a-valuation/kruzeconsulting_com_blog_due_diligence_checklist.txt) and [stage rows](raw/409a-valuation/kruze_stage_rows.csv). Vendor.
- [Hacker News comment by grellas](https://news.ycombinator.com/item?id=5799229), [saved](raw/409a-valuation/hn_item_5799229.json). One commenter.

Pages that blocked automated fetching: Armanino's 409A white paper (HTTP 403). Pages I could not fetch: Pulley's 409A guide (404 at the address I tried) and YC's Series A diligence checklist (404 at the blog address; I did not find a fetchable copy).

Reddit: no thread URLs surfaced in search, so there is no `.json` list.
