# Legal and cap table: expert knowledge

Written by the Tricorder team from the [cap table guide](../docs/reports/20261022.03_document_guides/cap-table.md), the [prior financing guide](../docs/reports/20261022.03_document_guides/prior-financing.md), the [claims, disputes and inquiries guide](../docs/reports/20261022.03_document_guides/claims-disputes-inquiries.md), the [board and stockholder minutes guide](../docs/reports/20261022.03_document_guides/board-stockholder-minutes.md), [FRAMEWORKS.md](../docs/ongoing/FRAMEWORKS.md) entry 1.10 (cap table reconciliation), and the SEC's [Form D page](https://www.sec.gov/resources-small-businesses/exempt-offerings/filing-form-d-notice) and [Form D form and instructions](https://www.sec.gov/files/formd.pdf). The public pages they quote are linked below. This is the team's reading of those sources.

This file gives the model an investor's lens on who owns the company and whether the papers and the public record back it up. Scripts remain the source of computed figures. Do not invent a benchmark that is not cited here.

## What an expert checks first

- **One table that adds up.** CRV says investors "expect one cap table file that settles ownership, with nothing else in the room contradicting it" ([CRV](https://www.crv.com/content/what-is-a-data-room)). Holders add to 100 percent fully diluted, and every SAFE, note and option pool is a row.
- **A signed paper behind every row.** Hustle Fund asks for the "Current cap table and schedule of outstanding SAFEs, notes, options, warrants, and side letters." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))
- **The public filing.** The SEC: "A company must file this notice within 15 days after the first sale of securities in the offering." ([SEC](https://www.sec.gov/resources-small-businesses/exempt-offerings/filing-form-d-notice)) A Form D on EDGAR is the one independent source for the amount sold and the number of investors.
- **A written claims statement.** Hustle Fund's pre-seed baseline asks for "Written disclosure of threatened claims, regulatory inquiries, or known disputes." "None" is a valid answer.

## Rules

- **Match instruments to rows both ways.** Every row has a paper, and every paper has a row. A row with no paper in the room reads `watch`, with an ask. It is not a cap table error (FRAMEWORKS 1.10).
- **Count signed instruments, not commitments.** A cap table that shows an investor with no signed SAFE or purchase agreement is counting a promise. Burkland: "if it’s not written down, it probably doesn’t exist from a cap table perspective." ([Burkland](https://burklandassociates.com/2021/11/02/surviving-due-diligence-part-3-cap-tables/)) Report the signed total and the unsigned total separately.
- **Know who must file Form D.** The SEC: "The federal securities laws require the notice to be filed by companies that have sold securities without registration under the Securities Act of 1933 in an offering made under Rule 504 or 506 of Regulation D or Section 4(a)(5) of the Securities Act." A company that relied on a different exemption has no Form D to find, so ask which exemption it used.
- **Time the filing from the first signed instrument.** The SEC: "For this purpose, the date of first sale is the date on which the first investor is irrevocably contractually committed to invest." A due date on a weekend or holiday moves to the next business day. Compute days from the first signed SAFE or purchase agreement to the filing date. No Form D on EDGAR more than 15 days after that date is a question for the founder. BCLP, a law firm, adds that "an issuer that fails to file a Form D will almost certainly have failed to make a proper blue sky notice filing" ([BCLP](https://bclplaw.com/en-US/events-insights-news/sec-enforcement-actions-for-failure-to-file-form-d-a-wake-up-call-for-startups-and-private-fund-advisers.html)).
- **Search EDGAR by company name.** The research found that EDGAR full-text search does not index Form D content. The company-name lookup and the quarterly Form D data sets do find filings ([research_demo_companies.md](../docs/reports/20261022.02_research/research_demo_companies.md)).
- **Compare the amount and the holders with the Form D.** The instruction for Item 13 says: "Also enter the dollar amount of securities sold in the offering as of the filing date." The instruction for Item 14 asks the issuer to "specify the total number of investors who already have invested." ([SEC Form D](https://www.sec.gov/files/formd.pdf)) Compare these with the cap table rows for that offering. A match to the dollar is a number corroborated by an independent government filing. A Form D filed before later closings shows less, so check for amendments.
- **Rebuild the pro forma.** Price, new shares, SAFE conversions and the pool after the round should rebuild from the round's terms. AngelList: "The pro-forma cap table must account for potential conversions of convertible debt or SAFEs (if the financing round triggers a conversion)." ([AngelList](https://learn.angellist.com/articles/cap-table))
- **Read the claims statement against the room.** Cooley GO: "In financing transactions, failure to thoroughly disclose can result in all manner of negative consequences, including breach of contract damages or a retroactive (downward) adjustment to the investment purchase price (i.e., valuation)." ([Cooley GO](https://www.cooleygo.com/what-is-a-disclosure-schedule-and-why-do-i-need-to-prepare-one/)) A dispute named in another file and missing from the statement is a difference to show.
- **Report differences. Leave intent to the operator.** Hustle Fund: "Red flags concern truth, ownership, authority, or a risk that can kill the company." Tricorder quotes both sides and never says a company hid something.

## Benchmarks, with their context

- **15 calendar days is a legal deadline, not a benchmark.** BCLP reports that in December 2024 the SEC settled actions against a private fund adviser and two pre-IPO companies for filing Form D late.
- **Stacked SAFEs.** CRV: "Stacking multiple SAFEs at different valuation caps is the most common way founders give away more of their company than they intended." ([CRV](https://www.crv.com/content/safe-agreements-for-startups))
- **Dead equity.** LTSE, a vendor: "Dead equity is a huge red flag and can easily scare away potential investors, from angels to institutions." ([LTSE](https://ltse.com/insights/what-investors-look-for-in-cap-tables))
- **One large early holder.** A VC newsletter says an early investor holding 30 to 40 percent can block the next round ([VC Unfiltered](https://vcunfiltered.beehiiv.com/p/the-cap-table-never-lies)). One newsletter's view.
- **No dilution or holder-count benchmark.** No source here gives typical dilution per round or a cutoff for how many holders is too many. Show the numbers with no line.

## Stage expectations

- **Seed:** a spreadsheet with founders, SAFEs or notes, an option pool and a pro forma. Hustle Fund wants it fully diluted, "including issued shares, options, warrants, SAFEs, notes, side letters, and promised grants". Grant records and minutes are lighter.
- **Series A:** CRV: "This is also when all outstanding SAFEs convert into actual shares, so the Series A is where your early fundraising decisions become visible on the cap table." The lead's counsel ties each line to signed papers and board approvals, and the claims statement becomes a formal disclosure schedule.

## What to ask

- The current fully diluted cap table and a pro forma for this round, showing how each SAFE converts and what the option pool becomes.
- The signed SAFE or note, with any side letter, for every investor on the table.
- The Form D file number and any amendments, or the exemption the company relied on, and the state notice filings.
- Bank statements that show each investor's wire.
- Board consents approving each issuance and the option plan.
- A written statement of any pending or threatened claim, dispute or regulatory inquiry, or a statement that there are none.

## Sources and boundaries

- Quotes from the guides were checked word for word against saved copies ([quotes_equity.csv](../docs/reports/20261022.03_document_guides/quotes_equity.csv)). The SEC quotes were checked against the live SEC page and the Form D PDF on 2026-10-24.
- Vendors (LTSE, Burkland, AngelList) are read as their views.
- A lawyer's tie-out of the stock ledger, whether shares were validly issued, side letters outside the room, and court records beyond federal dockets are the operator's to check.
- The SEC says it cannot guarantee the accuracy of Form D data ([FRAMEWORKS.md](../docs/ongoing/FRAMEWORKS.md), entry 2.2). A Form D shows what the company filed. It does not prove the money arrived.
