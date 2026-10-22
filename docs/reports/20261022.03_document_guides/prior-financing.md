# Prior financing: SAFEs, notes, term sheets

Written 2026-10-22 for the Tricorder document guides. Quotes are checked word for word against saved pages (see `quotes_equity.csv`). Vendor views are marked.

**In one line:** this folder holds the signed papers behind every dollar raised before this round, and the reader's job is to match each paper to a row on the cap table and see what each one turns into when the new round closes.

## 1. What it is

The papers for each earlier raise:

- **SAFEs and convertible notes**, with their side letters (pro rata, most favored nation, information rights, "major investor" status).
- **Term sheets**, both the one for the current round and any earlier ones that were signed.
- For a priced seed round: the stock purchase agreement, the charter that creates the preferred stock, and the investor rights, voting and first refusal agreements.
- Evidence that the raise was lawful: a Form D and state notice filings, or the exemption relied on.

The founder or the company's lawyer assembles it. Each item is usually a signed PDF. Cooley GO's request list asks for the agreements for "the purchase, repurchase, sale or issuance of securities" and for "Evidence of qualification or exemption under applicable federal and state blue sky laws for issuance or transfer of the Company’s securities", and for debt papers. ([Cooley GO list](https://www.cooleygo.com/wp-content/uploads/2014/07/Cooley-GO-Tip-Sheet-Sample-VC-Due-Diligence-Request-List.pdf))

## 2. At seed and at Series A

The data-room research marks this folder as expected at pre-seed, seed and Series A ([research_data_room.md](../20261022.02_research/research_data_room.md), row 19). Kruze's checklist, a vendor view, expects the shareholder agreements, SAFE and convertible debt papers and the history of rounds with valuation and terms at every stage, and gives its reason: "VCs need to verify the terms of these obligations since they affect company valuation." ([Kruze](https://kruzeconsulting.com/blog/due-diligence-checklist/); cells in [kruze_stage_rows.csv](raw/prior-financing/kruze_stage_rows.csv))

- **At seed**, the folder is mostly SAFEs and a few side letters, plus the term sheet or subscription papers for the current raise. Hustle Fund's pre-seed baseline asks for the "Proposed financing instrument, subscription document, or term sheet." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))
- **At Series A**, the SAFEs convert. CRV: "This is also when all outstanding SAFEs convert into actual shares, so the Series A is where your early fundraising decisions become visible on the cap table." ([CRV](https://www.crv.com/content/safe-agreements-for-startups)) The new lead's counsel reads every SAFE, every note and every side letter. Hustle Fund lists what to read in a priced round: "share class, liquidation preference, participation or conversion, seniority, anti-dilution provisions, option-pool treatment, voting and board rights, protective provisions, information rights, and pro rata rights". ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))

## 3. What a first pass checks

In order:

1. List every instrument: investor, date, type, amount, cap, discount, interest, maturity, and any side letter.
2. Match the list to the cap table. Every row on the table has a paper. Every paper has a row.
3. Is it the standard form, unmodified? What was changed?
4. Post-money or pre-money cap? This decides who bears the dilution.
5. Run the conversion at the new round's price. Does the result equal what the cap table shows?
6. For each note: is it past its maturity date, and what did the holders agree to?
7. Which rights reach into the new round: pro rata, most favored nation, information rights, first refusal?
8. Signed, dated, and the party names match the cap table.
9. Do the economics of the current term sheet match the pitch?
10. Is there evidence the earlier raises were filed correctly (Form D, state notices)?

## 4. Green flags

- **The standard form, unedited.** CRV (a fund): "Standardization is a feature." and "Deviating from the template adds legal complexity, slows closing and raises questions for investors who expect standard terms." ([CRV](https://www.crv.com/content/safe-agreements-for-startups))
- **A simple structure.** "The simpler the structure, the easier it is to model dilution and keep future fundraising clean." ([CRV](https://www.crv.com/content/safe-agreements-for-startups))
- **A cap in line with the market.** CRV says a cap "well above market norms without a strong reason" signals weak pricing discipline, so a cap with a stated reason reads well. ([CRV](https://www.crv.com/content/safe-agreements-for-startups))
- **Few, bounded side letters.** CRV says pro rata rights are best limited to the largest checks and the next round only. ([CRV](https://www.crv.com/content/safe-agreements-for-startups))
- **The founder has modeled the stack.** "Your ability to model your own cap table is a credibility signal" is CRV's phrase, and the same test applies to the SAFEs. ([CRV](https://www.crv.com/content/safe-agreements-for-startups))
- **Every instrument has a signed paper that matches the cap table row.** Hustle Fund asks for the "Current cap table and schedule of outstanding SAFEs, notes, options, warrants, and side letters." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))
- **Filings were made.** BCLP, a law firm, sets the Form D deadline at 15 calendar days after the first sale. The deadline is BCLP's. Reading a timely Form D on EDGAR as a sign of care is Tricorder's reading. ([BCLP](https://bclplaw.com/en-US/events-insights-news/sec-enforcement-actions-for-failure-to-file-form-d-a-wake-up-call-for-startups-and-private-fund-advisers.html))

## 5. Red flags and pitfalls

- **Stacked SAFEs at different caps (common).** OneGC (a legal services vendor): "each SAFE's percentage is fixed at signing, and every additional SAFE dilutes only the founders". ([OneGC](https://onegc.com/blog/five-safe-conversion-scenarios-every-founder-gets)) CRV: "Many founders only discover the total dilution when their lead investor runs the cap table math". ([CRV](https://www.crv.com/content/safe-agreements-for-startups))
- **A signed paper that does not match the cap table (common).** Promise Legal (vendor): "A Series A lead finds SAFE conversion terms in Carta that don’t match the signed SAFE." ([Promise Legal](https://blog.promise.legal/startup-central/the-carta-cap-table-compliance-playbook-for-startups/)) This is a difference in reporting between two files.
- **A cap table row with no paper (common).** CRV's list of causes of a conflicting percentage includes "a spreadsheet number with no stock purchase agreement behind it". ([CRV](https://www.crv.com/content/what-is-a-data-room))
- **Pro rata side letters handed out freely (common).** CRV: "Granting pro-rata rights to many SAFE holders can complicate your Series A fundraising." ([CRV](https://www.crv.com/content/safe-agreements-for-startups)) The YC guide gives the arithmetic: the allocation is the new investors' share ÷ (100% − the share held by SAFEs with pro rata), minus the new investors' share, and the guide's own example comes to 4.41 percent of the company on 15 percent of SAFEs with pro rata. ([YC SAFE guide](https://bookface-static.ycombinator.com/assets/ycdc/SAFE%20User%20Guide-a47c6588327d73aa2799e61ed7c2cae9f1a0ee9acfa9c43b62039dc06e715832.pdf))
- **MFN SAFEs that ride a lower cap (less common, serious).** OneGC: "In the worst case, MFN (Most Favored Nation) clauses in earlier SAFEs let those investors elect to convert on the terms of any later SAFE." ([OneGC](https://onegc.com/blog/five-safe-conversion-scenarios-every-founder-gets))
- **Edits to the template (common).** "Side letters are where much of the real negotiation happens in a SAFE round." ([CRV](https://www.crv.com/content/safe-agreements-for-startups)) A model has to read each one.
- **A note past its maturity date (less common, serious).** Allied Ventures, an investor network, says "startups and investors may extend the maturity date or revise terms (most common)", so the reader needs the extension or waiver in the room. ([Allied](https://www.allied.vc/guides/what-happens-when-convertible-notes-mature)) CRV: "Convertible notes also carry maturity dates, which can pressure founders to raise on weak terms or negotiate an extension if no priced round is in sight." ([CRV](https://www.crv.com/content/safe-agreements-for-startups))
- **A cap far above market (less common).** "A cap that sits well above market norms without a strong reason, such as traction, competitive pressure or an exceptional team, signals weak pricing discipline to many investors." ([CRV](https://www.crv.com/content/safe-agreements-for-startups))
- **Financing papers that differ from the pitch (less common, serious).** Hustle Fund: "Financing documents whose economics differ materially from the pitch." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))
- **A down or flat round against old caps (common since 2023, per OneGC).** OneGC lays out the case where the new price is below what earlier caps assumed and the lead asks for a bigger pool or tougher terms. ([OneGC](https://onegc.com/blog/five-safe-conversion-scenarios-every-founder-gets))
- **A missing or late Form D (rare but serious).** BCLP: "an issuer that fails to file a Form D will almost certainly have failed to make a proper blue sky notice filing". ([BCLP](https://bclplaw.com/en-US/events-insights-news/sec-enforcement-actions-for-failure-to-file-form-d-a-wake-up-call-for-startups-and-private-fund-advisers.html)) BCLP also reports that in December 2024 the SEC settled actions against a private fund adviser and two pre-IPO companies for filing Form D late.

## 6. How Tricorder checks it

### What a script can check

- **`cap_table_reconcile`** (exists, [FRAMEWORKS 1.10](../../ongoing/FRAMEWORKS.md), which the checklist names as the check that "reads the SAFE terms"). Each post-money SAFE: ownership = amount ÷ post-money cap, and shares at the cap price.
- **`instrument_register_match`** (proposed). Join the cap table's instrument rows to the signed papers on (investor, amount, date). Report rows with no paper and papers with no row.
- **`safe_conversion_recompute`** (proposed). Formula from the YC guide: shares = amount ÷ conversion price, where the cap price = cap ÷ Company Capitalization. YC's own wording is that "the number of shares issuable to the investor is equal to the (applicable pre- or post-money) valuation cap of the safe divided by the “Company Capitalization.”" ([YC SAFE guide](https://bookface-static.ycombinator.com/assets/ycdc/SAFE%20User%20Guide-a47c6588327d73aa2799e61ed7c2cae9f1a0ee9acfa9c43b62039dc06e715832.pdf)) In the post-money SAFE the capitalization includes outstanding shares and options, promised options, the unissued pool and other SAFEs and convertibles, and leaves out a pool increase made in the new round. With a discount, the holder takes the lower of the cap price and the discounted round price.
- **`note_maturity_check`** (proposed). Formula: flag a note when its maturity date is before the room's as-of date and the room holds no extension. Amount converting = principal + interest to the conversion date, per the note's terms.
- **`safe_stack_total`** (proposed, shared with the cap table guide). Sum of amount ÷ post-money cap.
- **`pro_rata_exposure`** (proposed). The YC formula above, applied to the SAFEs that have a pro rata side letter.
- **`form_d_lookup`** (proposed, roadmap). Search EDGAR for the issuer's Form D filings and compare the filing date to the first signed instrument: `days = filing_date − first_sale_date`, flagged when over 15 calendar days (BCLP). This is the checklist's outside item for who invested and when.

### What needs a model to read

- Each SAFE and note: cap, discount, pre or post money form, MFN, pro rata, information rights, major investor terms, conversion triggers, definitions of Company Capitalization. The model must quote the clause.
- Side letters, and where they depart from the YC form.
- The current term sheet: pre-money, amount, option pool treatment, liquidation preference, participation, board seats, protective provisions. The model must quote each term.
- For a note: interest rate, maturity date, qualified financing threshold and any extension or waiver.
- Names, dates and amounts against the cap table rows.

### What Tricorder cannot check and leaves to the operator

- Whether side letters exist beyond the ones in the room.
- Whether the money was wired (bank statement or a call to the investor).
- Whether each investor was eligible to buy, and whether state notice filings were made everywhere they were due.
- Whether an unsigned or edited form is what the parties actually agreed. A lawyer's call.
- How an MFN clause interacts with later SAFEs when the wording is unusual. A lawyer reads it.

## 7. Which readout pieces it feeds

- **Legal and cap table.**
- **The pitch itself**, where the "money raised before this round" claim is checked against the cap table and the model.

Checklist items: prior financing papers (the document itself); every instrument and grant on the cap table has a document; the cap table converts every SAFE at its cap; loans, liens and other encumbrances (for notes); the ask on the deck matches the round; investors checked against the cap table ([CHECKLIST.md](../../ongoing/CHECKLIST.md)).

## 8. If it is missing

- **Pre-seed, seed and Series A:** a gap at every stage. A cap table row with no paper reads `watch` under FRAMEWORKS 1.10, with an ask. It becomes a red flag only if the founder cannot produce a paper for money the table says was raised. That is the operator's call.
- Hustle Fund names the condition: "Missing or irreconcilable basics such as formation records, the cap table, financing documents, and IP assignments can stall a close until the gaps are resolved." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))

**Ask-list line:** "Please send the signed SAFE or note, with any side letter, for every investor on the cap table, and the term sheet for this round."

## 9. In the Hollis Voice room

**Not in the room as documents.** The room holds none of the signed SAFEs, no side letters and no term sheet. It holds the cap table that shows them, and the deck's ask slide.

What the room does show about prior financing:

- The cap table lists three SAFEs: Tidewater Seed Fund I, LP ($1,200,000) and Winifred Hartley, an angel ($800,000), each on a $12,000,000 post-money cap; and Ostrander Lane Ventures II, LP ($3,500,000) on a $28,000,000 post-money cap. Recomputed by script: 10.0000 percent, 6.6667 percent and 12.5000 percent, together 29.1667 percent. The conversion prices are $0.8319 and $1.9412 a share.
- Per FRAMEWORKS's piece-verdict example, the company overview, the cap table and the model agree on $5,500,000 raised before the round.
- The Series A terms are on the deck's ask slide (a $9,000,000 raise at a $45,000,000 pre-money).

No planted flag sits here. The cap table is the clean decoy DC3. A scan should list three "Not in the room: the signed SAFE" gaps (FRAMEWORKS 1.10) and ask for them. It should also ask for any pro rata side letter, because the cap table does not say whether one exists. The room's ledger shows legal fees to Pembry Legal Services in every month from January 2025 to September 2026 (21 lines, $144,223.54 in all, from `raw/_equity_tools/hv_ledger_legal.py`), so the company has a lawyer who holds these papers.

## 10. Sources

Each page is saved under [raw/prior-financing/](raw/prior-financing/).

- [YC, Post-money SAFE user guide (PDF)](https://bookface-static.ycombinator.com/assets/ycdc/SAFE%20User%20Guide-a47c6588327d73aa2799e61ed7c2cae9f1a0ee9acfa9c43b62039dc06e715832.pdf), [saved](raw/prior-financing/bookface_static_ycombinator_com_assets_ycdc_SAFE_20User_20Guide_a47c6588327d73aa2799e61ed7c2cae9f1a0.txt). Accelerator, primary source for the form.
- [CRV, SAFE agreements for startups](https://www.crv.com/content/safe-agreements-for-startups), [saved](raw/prior-financing/crv_com_content_safe_agreements_for_startups.txt). Fund view.
- [CRV, What is a data room](https://www.crv.com/content/what-is-a-data-room), [saved](raw/prior-financing/crv_com_content_what_is_a_data_room.txt). Fund view.
- [Hustle Fund, Angel investing due diligence checklist](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step), [saved](raw/prior-financing/hustlefund_vc_post_angel_squad_angel_investing_due_diligence_checklist_step_by_step.txt). Fund view.
- [Cooley GO, Sample VC Due Diligence Request List (PDF)](https://www.cooleygo.com/wp-content/uploads/2014/07/Cooley-GO-Tip-Sheet-Sample-VC-Due-Diligence-Request-List.pdf), [saved](raw/prior-financing/cooleygo_com_wp_content_uploads_2014_07_Cooley_GO_Tip_Sheet_Sample_VC_Due_Diligence_Request_List_pdf.txt). Law firm.
- [Kruze, VC due diligence checklist](https://kruzeconsulting.com/blog/due-diligence-checklist/), [saved](raw/prior-financing/kruzeconsulting_com_blog_due_diligence_checklist.txt) and [stage rows](raw/prior-financing/kruze_stage_rows.csv). Vendor.
- [OneGC, Five SAFE conversion scenarios](https://onegc.com/blog/five-safe-conversion-scenarios-every-founder-gets), [saved](raw/prior-financing/onegc_com_blog_five_safe_conversion_scenarios_every_founder_gets.txt). Vendor.
- [Allied Ventures, What happens when convertible notes mature](https://www.allied.vc/guides/what-happens-when-convertible-notes-mature), [saved](raw/prior-financing/allied_vc_guides_what_happens_when_convertible_notes_mature.txt). Investor network.
- [BCLP, SEC enforcement actions for failure to file Form D](https://bclplaw.com/en-US/events-insights-news/sec-enforcement-actions-for-failure-to-file-form-d-a-wake-up-call-for-startups-and-private-fund-advisers.html), [saved](raw/prior-financing/bclplaw_com_en_US_events_insights_news_sec_enforcement_actions_for_failure_to_file_form_d_a_wake_up_.txt). Law firm.
- [Promise Legal, The Carta cap table compliance playbook](https://blog.promise.legal/startup-central/the-carta-cap-table-compliance-playbook-for-startups/), [saved](raw/prior-financing/blog_promise_legal_startup_central_the_carta_cap_table_compliance_playbook_for_startups.txt). Vendor.
- [Torys, Pre-money versus post-money SAFE](https://www.torys.com/insights/publications/2021/02/pre-money-versus-post-money-safe), [saved](raw/prior-financing/torys_com_insights_publications_2021_02_pre_money_versus_post_money_safe.txt). Law firm; read, not quoted.

Pages that blocked automated fetching: the SEC's Form D page (HTTP 403) and Carta's blog post on pre-money and post-money SAFEs (HTTP 403).

Reddit: no thread URLs surfaced in search, so there is no `.json` list.
