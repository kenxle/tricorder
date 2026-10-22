# Cap table, fully diluted, current and pro forma

Written 2026-10-22 for the Tricorder document guides. This is the reference the scans, the checklist and the memo draw on for the cap table. Quotes are checked word for word against saved pages (see `quotes_equity.csv`). Vendor views are marked as vendor views.

**In one line:** the cap table is the first file a seed or Series A reader opens, and a reader trusts it when it adds to 100 percent, shows every SAFE and option, matches the round on the deck, and has a signed document behind every row.

## 1. What it is

A cap table lists every holder of the company's equity and what each one holds: common stock, preferred stock, options, warrants, SAFEs and notes. "Fully diluted" counts options, the unissued option pool and convertible instruments as if they were exercised or converted. "Current" is the table today. "Pro forma" is the table after the round being raised closes; AngelList describes it this way:

> "This is a version of the cap table that shows the updated company ownership after a financing round closes." ([AngelList](https://learn.angellist.com/articles/cap-table))

The founder or a finance lead prepares it. At seed it is usually a spreadsheet; by Series A it is usually an export from a cap table platform such as Carta or Pulley, with the ledgers behind it. Cooley GO publishes a sample:

> "Simple capitalization table showing current capitalization including options." ([Cooley GO sample](https://www.cooleygo.com/documents/sample-cap-table-simple/))

## 2. At seed and at Series A

The data-room research marks the cap table as expected at pre-seed, seed and Series A ([research_data_room.md](../20261022.02_research/research_data_room.md), row 5 of the 30-document table). Kruze's checklist, a vendor view, also expects the detailed cap table, the option pool details, the funding history and the list of current investors at every stage from pre-seed to Series C ([Kruze](https://kruzeconsulting.com/blog/due-diligence-checklist/); the cells are in [kruze_stage_rows.csv](raw/cap-table/kruze_stage_rows.csv)).

What changes between the two stages:

- **At seed**, the table is short: founders, a few SAFEs or notes, an option pool, and a pro forma for the round. A spreadsheet is normal. Hustle Fund's checklist asks for it fully diluted, "including issued shares, options, warrants, SAFEs, notes, side letters, and promised grants" ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)).
- **At Series A**, the table has more rows and more history: converted SAFEs, a seed round that may be priced, a larger option ledger, and departures. The reader now tests the table against documents. CRV says investors "expect one cap table file that settles ownership, with nothing else in the room contradicting it" ([CRV](https://www.crv.com/content/what-is-a-data-room)). Legal counsel starts from the table and checks each line against the signed papers and the board approvals ([Promise Legal](https://blog.promise.legal/startup-central/the-carta-cap-table-compliance-playbook-for-startups/), a legal services vendor).
- **The pro forma matters more at Series A.** It has to show every SAFE converting and what the option pool becomes, because the lead is pricing off it. AngelList says "The pro-forma cap table must account for potential conversions of convertible debt or SAFEs (if the financing round triggers a conversion)." ([AngelList](https://learn.angellist.com/articles/cap-table))

## 3. What a first pass checks

In order:

1. Is there one current, dated table, and a pro forma for this round?
2. Do the holders add to 100 percent fully diluted? Does every row have a class and a share count?
3. Is every SAFE and note a row, and does each convert at its stated cap or discount?
4. Is the option pool shown, split into granted, available and promised?
5. Who holds what: the founders' combined share, whether founder shares vest, anyone who left and still holds a large block, and any early investor holding a very large share.
6. Does the round on the deck (amount, pre-money, post-money, ownership) match the pro forma?
7. Do other files agree with it (the overview's money raised, the model's cash bridge, the team files)?
8. Does a signed document sit behind each instrument and grant? A script can list what is in the room; a lawyer confirms the rest.

CRV puts the cap table first on the deal team's first-pass list:

> "the cap table, the financial model, the articles of incorporation and the intellectual property (IP) assignment agreements" ([CRV](https://www.crv.com/content/what-is-a-data-room))

## 4. Green flags

- **The table ties out and the founder can explain it.** CRV (a fund, so a fund's view): "Your ability to model your own cap table is a credibility signal that experienced investors notice immediately." ([CRV](https://www.crv.com/content/safe-agreements-for-startups)) A VC newsletter puts the test this way: "If you can’t explain your own cap table in two minutes, no investor will explain a check to their LPs." ([VC Unfiltered, by 1752vc](https://vcunfiltered.beehiiv.com/p/the-cap-table-never-lies))
- **Records are kept as the company goes.** CRV says "founders with systematic record keeping can respond to due diligence requests same-day instead of digging through old emails to reconstruct ownership history". ([CRV](https://crv.com/content/409a-valuation-before-series-a))
- **A clean, organized room lowers the reader's guard.** Cooley GO, a law firm: "disorganized companies tend to get labeled as having “hair” and are typically subjected to higher levels of due diligence scrutiny". ([Cooley GO](https://www.cooleygo.com/cant-afford-disorganized)) The reverse follows: a clean table is read faster.
- **Founders hold unvested shares.** NASPP, the stock plan professionals' association: "A founder who owns all their equity outright could, in theory, walk away tomorrow without consequence." ([NASPP](https://www.naspp.com/blog/what-do-investors-look-for-on-your-cap-table)) A table that shows founder vesting answers this.
- **The option pool is shown and sized to a hiring plan.** NASPP lists an employee pool among what investors want to see, and says a missing or used-up pool can point to hiring trouble ahead ([NASPP](https://www.naspp.com/blog/what-do-investors-look-for-on-your-cap-table)).
- **The holders are a short list of people who add value.** SVB's article says to get a "lead investor, a strategic investor, a great angel, not a list of 30 random people." ([SVB](https://www.svb.com/startup-insights/startup-equity/understanding-startup-cap-table/))
- **The same numbers appear in more than one file.** CRV wants a single cap table "with nothing else in the room contradicting it" ([CRV](https://www.crv.com/content/what-is-a-data-room)). When the raise and the money raised before it agree across the cap table, the model and the overview, that is a corroborated number the readout can show as strong.
- **Counsel's ledger sits behind the spreadsheet.** Promise Legal (vendor view) defines a compliant table as one where "A cap table is compliant when the ownership and fully diluted math in Carta matches (1) the signed transaction documents and (2) the company’s underlying corporate authority." ([Promise Legal](https://blog.promise.legal/startup-central/the-carta-cap-table-compliance-playbook-for-startups/))

## 5. Red flags and pitfalls

Marked **common** or **rare but serious**.

- **The table does not add up, or has impossible rows (common).** A holder over 100 percent, shares for a person who does not exist, a negative number. LTSE (a stock exchange operator, vendor view) lists these as "impossibles" and says investors treat honest slips as far less serious ([LTSE](https://ltse.com/insights/what-investors-look-for-in-cap-tables)). Burkland (a fractional CFO firm) says startups carry the table "replete with all the mistakes, mathematical errors, and missing information" when many people edit one spreadsheet. ([Burkland](https://burklandassociates.com/2021/11/02/surviving-due-diligence-part-3-cap-tables/))
- **A promise with no paper (common).** Burkland: "if it’s not written down, it probably doesn’t exist from a cap table perspective." ([Burkland](https://burklandassociates.com/2021/11/02/surviving-due-diligence-part-3-cap-tables/)) Hustle Fund tells investors to pause on "A cap table that does not reconcile or undisclosed securities, debt, promises, or side letters." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))
- **An unconverted SAFE, an undocumented grant or a number with no purchase agreement (common).** CRV: "The usual culprits behind a conflicting percentage are an unconverted SAFE, an undocumented option grant or a spreadsheet number with no stock purchase agreement behind it." ([CRV](https://www.crv.com/content/what-is-a-data-room))
- **Stacked SAFEs founders did not model (common).** CRV: "Stacking multiple SAFEs at different valuation caps is the most common way founders give away more of their company than they intended." ([CRV](https://www.crv.com/content/safe-agreements-for-startups)) The detail is in the prior-financing guide.
- **Dead equity (common, and often serious).** A departed founder or employee still holding a large block. LTSE: "Dead equity is a huge red flag and can easily scare away potential investors, from angels to institutions." ([LTSE](https://ltse.com/insights/what-investors-look-for-in-cap-tables)) Colligan Law, a startup law firm: "Maybe the most common cap table problem is the existence of large pools of dead equity." ([Colligan Law](https://insights.colliganlaw.com/post/102fu5z/why-do-cap-tables-kill-startup-companies)) Holloway's angel investing guide, written by two lawyers, adds that a big block held by someone who left "suggests that the company may not have had a stock vesting plan in place for founders early on", and tells the investor to confirm that person signed an IP assignment. ([Holloway](https://www.holloway.com/g/angel-investing/sections/legal-due-diligence-for-angel-investments))
- **Founders already thin (common).** Open Core Ventures, a fund whose model gives founders less, says "Lower founder ownership is a valid concern for future investors." ([OCV handbook](https://handbook.opencoreventures.com/cap-table-concerns)) A VC newsletter argues a thin founder team is a flight risk ([VC Unfiltered](https://vcunfiltered.beehiiv.com/p/the-cap-table-never-lies)). Treat this as a question for the partner; it is a judgment about incentive, not an error.
- **Promised percentages and early rights (less common).** Colligan Law lists promises of a fixed ownership percentage or anti-dilution rights to early participants who add little as a repeat problem, along with non-accredited investors in early rounds. ([Colligan Law](https://insights.colliganlaw.com/post/102fu5z/why-do-cap-tables-kill-startup-companies))
- **The option pool shuffle hides the real pre-money (common).** Venture Hacks: "Many entrepreneurs think their pre-money valuation determines their percentage ownership of the company." ([Venture Hacks](https://venturehacks.com/topics/option-pool)) A pool created before the new money lowers the effective pre-money.
- **A crowded or concentrated table (less common).** A VC newsletter says a round stitched from many small checks with no lead can mean the better investors passed, and that an early investor holding 30 to 40 percent can block the next round. ([VC Unfiltered](https://vcunfiltered.beehiiv.com/p/the-cap-table-never-lies)) The same piece says the cap table is "necessary, not sufficient": a messy table on a strong company can still be a yes.
- **Several versions in the room (common).** CRV wants one file that settles ownership. A deck, a model and a spreadsheet that give different holders or totals are a difference in reporting that the readout shows.
- **Shares that were never validly issued (rare but serious).** If a board never approved an issuance, or the charter did not authorize enough shares, the stock can be defective. Holloway warns that "Many, many companies have wound up in protracted and expensive lawsuits because they did not carefully document stock ownership". ([Holloway](https://www.holloway.com/g/angel-investing/sections/legal-due-diligence-for-angel-investments)) A cure exists in some cases; see the board and stockholder minutes guide.
- **A clean dashboard that hides a legal gap (rare but serious).** Promise Legal: "Carta is excellent at organizing what you input, but it does not validate legal authority, interpret SAFE/option terms, or cure missing board or stockholder actions." ([Promise Legal](https://blog.promise.legal/startup-central/the-carta-cap-table-compliance-playbook-for-startups/)) The tool's output is only as good as the documents behind it.

A note on tone. Tricorder reports differences. Hustle Fund's own advice fits: "treat a discrepancy as a prompt for context rather than an automatic finding of misconduct". ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))

## 6. How Tricorder checks it

### What a script can check

- **`cap_table_reconcile`** (exists, [FRAMEWORKS 1.10](../../ongoing/FRAMEWORKS.md)). Holders add to 100.00 percent fully diluted; each post-money SAFE converts at amount ÷ cap; Series A ownership = raise ÷ post-money; post-money = pre-money + raise.
- **`cap_table_row_integrity`** (proposed). Formula: for each row, shares ≥ 0; share count is a whole number; class is not blank; holder names are unique; total shares equals the sum of the rows; no row's percentage exceeds 100. This catches LTSE's "impossibles".
- **`pro_forma_roundtrip`** (proposed). Formula: price = pre-money ÷ pre-round fully diluted shares; new shares = raise ÷ price; post-round shares = pre-round shares + new shares (+ any pool increase); ownership = new shares ÷ post-round shares. Compare each result with the deck's ask slide and with any term sheet in the room. Compare the pro forma's own total with this result.
- **`safe_stack_total`** (proposed). Formula: sum of amount ÷ post-money cap across the SAFEs. This is the share SAFE holders take before any priced share is sold.
- **`pool_after_round`** (proposed). Formula: unissued pool ÷ post-round fully diluted shares, plus a flag when the pro forma shows no pool increase while a term sheet or the hiring plan implies one. When a post-round pool target `o` is given, Venture Hacks' formulas give the new pool shares `n = (x × o × t) ÷ (p − o × t)`, the price `s = p ÷ (x + n)` and the effective pre-money `e = s × x`, where `p` is the pre-money, `t` the post-money and `x` the existing shares. ([Venture Hacks](https://venturehacks.com/topics/option-pool))
- **`founder_ownership_before_after`** (proposed, report only). Founders' combined share before and after the round. Founders are the people named as founders in the team files.
- **`holder_in_team_files`** (proposed, a question and not a flag). For each named non-investor holder, look for the name in the bios, hiring plan and payroll vendor lines. A holder who appears nowhere is a dead-equity question.
- **Cross-file agreement.** The raise and the money raised before it, read from the cap table, the model and the overview, compared within `match_tolerance`. When they agree, the readout shows a corroborated number.

### What needs a model to read

- The notes, footnotes and legend on the sheet: assumptions such as "SAFEs shown as converted at their cap", any mention of an advisor grant, a warrant, a side letter or a promised option. The model must quote the cell.
- Which instruments have a document in the room's file list. FRAMEWORKS 1.10 already asks for "Not in the room: the signed <instrument>" as a gap for each SAFE or note with no file.
- Class names and the entity name on the table against the charter and the financing documents, when those are in the room.
- Whether a Series A pro forma follows the term sheet's pool and conversion terms, when a term sheet is in the room.

### What Tricorder cannot check and leaves to the operator

- Whether the table matches the stock ledger, the signed purchase agreements and the board approvals. That is a lawyer's tie-out, or a platform export with the ledgers.
- Whether every share was validly authorized and issued.
- Side letters, verbal promises and handshake equity that were never written down.
- Whether a departed holder is still "dead" in practice. That takes a reference call.
- The money side: whether the SAFE and note amounts on the table were actually wired. That is a bank statement or a call to the investor.

## 7. Which readout pieces it feeds

- **Legal and cap table** (the piece for ownership and the papers behind it).
- **The pitch itself.** FRAMEWORKS 1.10 sends the cap table's claims (the raise, the pre-money, the ownership and the money raised before the round) to the pitch itself, where they corroborate the deck.

Checklist items it covers ([CHECKLIST.md](../../ongoing/CHECKLIST.md)):

- Cap table, fully diluted (the document itself).
- Cap table adds to 100 percent fully diluted, every SAFE converts at its cap, the option pool is shown.
- Every instrument and grant on the cap table has a document.
- Pro forma cap table, after this round.
- The ask on the deck matches the round in the cap table.
- Investors who have invested, checked against the cap table.

## 8. If it is missing

- **Pre-seed, seed and Series A:** a gap at every stage, and it is the first gap, because the research puts the cap table on the first-pass list at all three. The label is `cannot_check`. It is not a red flag until the founder declines to supply it. Hustle Fund names that as the pause point: "Refusal to share the basic evidence needed to understand cash, ownership, terms, or material obligations." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)) That judgment is the operator's.
- Hustle Fund also says missing or irreconcilable basics, including the cap table, "can stall a close until the gaps are resolved". ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))

**Ask-list line:** "Please send the current fully diluted cap table (every holder, class, SAFE, note, option grant and promised grant, with a date), and a pro forma table for this round that shows how each SAFE converts and what the option pool becomes."

## 9. In the Hollis Voice room

**Held:** yes. `02_financials/cap_table.xlsx` is in the full room and in the thin first tier (the seed drop). It is the clean decoy **DC3** in the answer key: a correct scan must not flag it.

What it shows (all figures recomputed by `raw/_equity_tools/hv_cap_math.py` from the workbook's cells):

- 14,424,000 shares fully diluted before the Series A.
- Founders: the CEO holds 4,437,000 (30.7612 percent) and the CTO holds 3,598,000 (24.9445 percent). Together 55.7058 percent.
- Options: 1,148,000 granted to 11 holders (7.9590 percent) and 1,034,000 available (7.1686 percent).
- Three SAFEs shown converted at their caps: Tidewater Seed Fund I, LP, $1,200,000 on a $12,000,000 post-money cap (10.0000 percent); Winifred Hartley, an angel, $800,000 on the same cap (6.6667 percent); Ostrander Lane Ventures II, LP, $3,500,000 on a $28,000,000 post-money cap (12.5000 percent). Together 29.1667 percent.
- Series A: $9,000,000 on a $45,000,000 pre-money gives a $54,000,000 post-money, a price of $3.1198 a share, 2,884,800 new shares and 16.6667 percent ownership. After the round the founders hold 46.4215 percent.

**Green flags in it:** the $9,000,000 raise appears in the cap table, the model (`SERIES_A_RAISE`) and deck slide 13. This is a green flag in the answer key's `green_flags`. FRAMEWORKS's piece-verdict example also shows the $5,500,000 raised before the round agreeing across the overview, the cap table and the model.

**What it does not hold, and what that does to the label.** The room has no SAFE documents, no option ledger and no stock ledger. FRAMEWORKS 1.10 says a table with an instrument that has no document in the room reads `watch`, and that a missing SAFE document is "a `watch` and an ask". The same entry says the expected label on Hollis Voice is `clear`, and the answer key requires DC3 to stay unflagged. Those two lines disagree. The orchestrator needs to pick one: either `watch` (with the asks) is the right label and DC3 means "no flag", or the rule changes so a seed-drop room without SAFE papers reads `clear`.

**A small observation, not a planted flag:** the pro forma leaves "Options available" at 1,034,000 shares. That is 7.1686 percent of the shares before the round and 5.9738 percent after it. If the term sheet asks for a pool top-up, the effective pre-money is lower than $45,000,000. The right ask is the term sheet's pool terms.

## 10. Sources

Each page is saved under [raw/cap-table/](raw/cap-table/).

- [Cooley GO, Sample VC Due Diligence Request List (PDF)](https://www.cooleygo.com/wp-content/uploads/2014/07/Cooley-GO-Tip-Sheet-Sample-VC-Due-Diligence-Request-List.pdf), [saved](raw/cap-table/cooleygo_com_wp_content_uploads_2014_07_Cooley_GO_Tip_Sheet_Sample_VC_Due_Diligence_Request_List_pdf.txt). Law-firm view; Cooley says it does not endorse it as a "market" standard.
- [Cooley GO, Sample Cap Table (Simple)](https://www.cooleygo.com/documents/sample-cap-table-simple/), [saved](raw/cap-table/cooleygo_com_documents_sample_cap_table_simple.txt)
- [Cooley GO, Why You Can't Afford To Be Disorganized](https://www.cooleygo.com/cant-afford-disorganized), [saved](raw/cap-table/cooleygo_com_cant_afford_disorganized.txt)
- [CRV, What is a data room](https://www.crv.com/content/what-is-a-data-room), [saved](raw/cap-table/crv_com_content_what_is_a_data_room.txt). Fund view.
- [CRV, SAFE agreements for startups](https://www.crv.com/content/safe-agreements-for-startups), [saved](raw/cap-table/crv_com_content_safe_agreements_for_startups.txt). Fund view.
- [CRV, 409A valuation before Series A](https://crv.com/content/409a-valuation-before-series-a), [saved](raw/cap-table/crv_com_content_409a_valuation_before_series_a.txt). Fund view.
- [Hustle Fund, Angel investing due diligence checklist](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step), [saved](raw/cap-table/hustlefund_vc_post_angel_squad_angel_investing_due_diligence_checklist_step_by_step.txt). Fund view.
- [VC Unfiltered by 1752vc, The Cap Table Never Lies](https://vcunfiltered.beehiiv.com/p/the-cap-table-never-lies), [saved](raw/cap-table/vcunfiltered_beehiiv_com_p_the_cap_table_never_lies.txt). Fund newsletter.
- [Open Core Ventures handbook, Cap table concerns](https://handbook.opencoreventures.com/cap-table-concerns), [saved](raw/cap-table/handbook_opencoreventures_com_cap_table_concerns.txt). Fund view.
- [Holloway, Legal due diligence for angel investments](https://www.holloway.com/g/angel-investing/sections/legal-due-diligence-for-angel-investments), [saved](raw/cap-table/holloway_com_g_angel_investing_sections_legal_due_diligence_for_angel_investments.txt). Two lawyers.
- [Colligan Law, Why do cap tables kill startup companies](https://insights.colliganlaw.com/post/102fu5z/why-do-cap-tables-kill-startup-companies), [saved](raw/cap-table/insights_colliganlaw_com_post_102fu5z_why_do_cap_tables_kill_startup_companies.txt). Law firm.
- [Burkland Associates, Surviving due diligence part 3: cap tables](https://burklandassociates.com/2021/11/02/surviving-due-diligence-part-3-cap-tables/), [saved](raw/cap-table/burklandassociates_com_2021_11_02_surviving_due_diligence_part_3_cap_tables.txt). Vendor (fractional CFO firm).
- [LTSE, What investors look for in cap tables](https://ltse.com/insights/what-investors-look-for-in-cap-tables), [saved](raw/cap-table/ltse_com_insights_what_investors_look_for_in_cap_tables.txt). Vendor.
- [NASPP, What do investors look for on your cap table](https://www.naspp.com/blog/what-do-investors-look-for-on-your-cap-table), [saved](raw/cap-table/naspp_com_blog_what_do_investors_look_for_on_your_cap_table.txt). Trade association.
- [SVB, Understanding a startup cap table](https://www.svb.com/startup-insights/startup-equity/understanding-startup-cap-table/), [saved](raw/cap-table/svb_com_startup_insights_startup_equity_understanding_startup_cap_table.txt). Bank article that passes on quotes from investors; used as the bank's own text.
- [BetaKit, Ask an Investor: What is a broken cap table?](https://betakit.com/ask-an-investor-what-is-a-broken-cap-table/), [saved](raw/cap-table/betakit_com_ask_an_investor_what_is_a_broken_cap_table.txt)
- [AngelList, Cap table guide](https://learn.angellist.com/articles/cap-table), [saved](raw/cap-table/learn_angellist_com_articles_cap_table.txt). Vendor.
- [Venture Hacks, Option pool](https://venturehacks.com/topics/option-pool), [saved](raw/cap-table/venturehacks_com_topics_option_pool.txt)
- [Promise Legal, The Carta cap table compliance playbook](https://blog.promise.legal/startup-central/the-carta-cap-table-compliance-playbook-for-startups/), [saved](raw/cap-table/blog_promise_legal_startup_central_the_carta_cap_table_compliance_playbook_for_startups.txt). Vendor (legal services).
- [Kruze, VC due diligence checklist](https://kruzeconsulting.com/blog/due-diligence-checklist/), [saved](raw/cap-table/kruzeconsulting_com_blog_due_diligence_checklist.txt) and [stage rows](raw/cap-table/kruze_stage_rows.csv). Vendor (accounting firm).
- [Hacker News comment on the Stability AI story](https://news.ycombinator.com/item?id=36728372), [saved](raw/cap-table/hn_item_36728372.json). One reader's view.

Pages that blocked automated fetching: Carta's cap table guide and investor due diligence guide (HTTP 403), and DocSend's seed investor post (HTTP 403). The orchestrator can read them in a browser.

Reddit: none of the searches surfaced a Reddit thread URL, so there is no `.json` list.
