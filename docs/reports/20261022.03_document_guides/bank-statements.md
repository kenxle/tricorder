# Bank statements (3 to 12 months)

*In short: bank statements are how an investor checks that the revenue in the deck reached the bank. They usually come late (after a term sheet, or just before the wire). Several fraud cases involve altered statements, so Tricorder treats a PDF as a claim until the bank says the same.*

Written 2026-10-22. Quotes were checked word for word against saved pages by [financials_quotes.py](raw/financials_quotes.py); results are in [quotes_financials.csv](quotes_financials.csv). Vendor views are marked. Fraud cases are described as the sources describe them: charges and allegations unless a source says otherwise.

## 1. What it is

Monthly statements for every business bank account, and often the company's cards, loans and payment-processor balances. The bank produces them. The founder downloads and uploads them, usually as PDFs, sometimes as CSV exports. Kruze, an accounting firm, lists what investors ask for:

> "investors typically expect 12-24 months of business bank statements, monthly bank reconciliations tied to the general ledger" ([Kruze Consulting](https://kruzeconsulting.com/blog/startup-due-diligence-banking-documentation/))

Papermark, a data-room vendor, gives the purpose in one line:

> "Investors check that the revenue in the deck reaches the bank account. Three to six months of statements, exported as PDFs, ends that question in one click. Founders resist this one and should not; it is standard, and the alternative is a call about it." ([Papermark, vendor view](https://www.papermark.com/blog/data-room-for-yc-startups))

## 2. At seed and at Series A

The research table marks bank statements as not expected at pre-seed, lighter at seed and expected at Series A ([data-room research](../20261022.02_research/research_data_room.md)). Visible (vendor) shows the same pattern in its stage table, with "3 to 12 months" in the row name ([Visible](https://visible.vc/blog/what-to-include-in-your-data-room/)). The length varies by source: Papermark says three to six months, Visible three to twelve, Kruze twelve to twenty-four.

**Timing.** Most of the sources put the bank check late.

- Jason Lemkin of SaaStr splits diligence into before and after the term sheet and puts the bank check in the second half:

  > "Bank statements & deep financial review. To make sure whatever you have is true." ([Jason Lemkin, SaaStr](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet))

  In the first half he puts a basic financials and model review, "often only a cursory one." ([Jason Lemkin, SaaStr](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet))

- Papermark's guide for YC startups lists bank statements in a "pre-wire confirmation" set with incorporation papers and IP assignments ([Papermark, vendor view](https://www.papermark.com/blog/data-room-for-yc-startups)).
- A podcast summary in the 20VC newsletter says a SaaS fund founder argued investors should always check the bank account, because his most stressful investments all had made-up claims ([20VC newsletter, summary of a podcast](https://20vc.substack.com/p/20vc-newsletter-june-2nd-2024)).
- An observer on Hacker News is surprised how little checking happens:

  > "Wait, when they're doing due diligence, nobody actually checks anything with the bank? I think it might be harder to fake eligibility for a mortgage than $107 million ARR." ([Hacker News commenter](https://news.ycombinator.com/item?id=48606618))

**Angels ask earlier.** Hustle Fund's angel guide puts revenue verification before the wire:

> "For revenue claims, ask to see their Stripe dashboard or bank statements. Most honest founders will show you. If they hesitate or make excuses, that's a red flag the size of Texas." ([Hustle Fund, Angel Squad](https://www.hustlefund.vc/post/angel-squad-how-to-verify-startup-claims))

**Series A** adds depth. Kruze's list (12 to 24 months, monthly reconciliations tied to the general ledger, an approvals trail, and records showing how prior investor money was spent) is the Series A version ([Kruze Consulting](https://kruzeconsulting.com/blog/startup-due-diligence-banking-documentation/)).

## 3. What a first pass checks

1. Are all accounts there, in the company's legal name, with no month missing?
2. Does each statement add up (opening balance plus deposits minus withdrawals equals closing balance), and does each month's closing balance equal the next month's opening balance?
3. Do monthly deposits tie to revenue plus financing in the P&L?
4. Do investor wires match the cap table and the SAFEs?
5. Does the latest balance match the cash figure in the model and the deck?
6. Do outflows match the burn, and do payroll outflows match the payroll line?
7. Are there large or unusual transactions, founder transfers or related-party payments?

Hustle Fund's burn guide gives the reconciliation rule an associate can use:

> "If the operating calculation and bank movement do not agree, ask which financing flow, one-time payment, or timing difference is missing." ([Hustle Fund](https://www.hustlefund.vc/post/angel-squad-startup-burn-rate-management-what-investors-should-actually-watch-for))

Processor payouts are net, so deposits are smaller than revenue by fees and refunds. A reconciliation guide (vendor view) puts it simply:

> "Stripe subtracts its processing fee before it sends money." ([beancount.io](https://beancount.io/blog/2026/08/25/how-to-reconcile-stripe-payouts-gross-vs-net-fees-refunds-guide))

## 4. Green flags

- **Deposits tie to revenue after fees and timing,** and the monthly reconciliation exists. Kruze:

  > "Confirm your reported revenue and expenses match real cash movement" ([Kruze Consulting](https://kruzeconsulting.com/blog/startup-due-diligence-banking-documentation/))

- **Reconciled at the time, not backfilled.** Kruze lists "Evidence that reconciliations were performed close to month-end, not backfilled right before the raise" ([Kruze Consulting](https://kruzeconsulting.com/blog/startup-due-diligence-banking-documentation/)).
- **An edit history in the accounting system.** The same Kruze page calls it healthy and warns that its absence "can actually look suspicious" ([Kruze Consulting](https://kruzeconsulting.com/blog/startup-due-diligence-banking-documentation/)).
- **The founder offers it.** Hustle Fund says most honest founders will show the statements (quote in section 2).
- **Investor wires and SAFE amounts match the cap table.** This is my reading of Kruze's list item "Records showing how prior investment rounds were received into the bank account"; the page lists the records but does not call the match a green flag.

## 5. Red flags and pitfalls

**Common**

- **Hesitation or excuses** when asked (Hustle Fund quote in section 2).
- **A deck number that is not in the bank.** The same Hustle Fund guide gives the usual shape:

  > "We did $50k total last month but $40k was one-time setup fees." ([Hustle Fund, Angel Squad](https://www.hustlefund.vc/post/angel-squad-how-to-verify-startup-claims))

  The guide says a claim of "$50k MRR" often hides this. The deposits for that month would show the fees.

- **Cash-basis books against accrual metrics.** Kruze:

  > "Cash-basis books that don't match reported metrics. If your investor updates cite accrual-based revenue but your books are cash-basis, the numbers won't tie out cleanly." ([Kruze Consulting](https://kruzeconsulting.com/blog/startup-due-diligence-banking-documentation/))

- **Commingled funds.** Kruze:

  > "Commingled funds. Founder personal expenses run through the business account (or vice versa) without clear documentation." ([Kruze Consulting](https://kruzeconsulting.com/blog/startup-due-diligence-banking-documentation/))

- **Deposits that do not tie to revenue.** Papermark's red-flag list for buyers (an M&A article, vendor view) makes the sample-month tie-out the first test:

  > "Reconcile bank deposits to reported revenue for a sample of months. Where they do not tie, there is either unrecorded revenue, which a buyer cannot pay for because it cannot be financed or defended, or a bookkeeping failure, which is its own finding." ([Papermark, vendor view](https://www.papermark.com/blog/due-diligence-red-flags))

- **Vague answers on burn and runway.** Hustle Fund: "If they dodge questions about burn rate or runway, walk away." ([Hustle Fund, Angel Squad](https://www.hustlefund.vc/post/angel-squad-how-to-verify-startup-claims))

**Rare but serious: forged or altered statements.** In Joonko and YouPlus, the sources say an investor pressed for proof and was handed altered statements. In NS8, the statements fed the numbers shown to investors. ComplYant is the opposite case: the source says nobody appears to have asked.

| Case | What the source says | Source |
|---|---|---|
| Joonko | The SEC alleges the founder gave a suspicious investor falsified bank statements and forged contracts; the investor confronted her in mid-2023 | [Insurance Journal, reporting the SEC complaint](https://amp.insurancejournal.com/news/east/2024/06/14/779473.htm) |
| YouPlus | The SEC alleges the CEO provided falsified bank statements when an investor pressed for details | [Finance Magnates, reporting the SEC](https://financemagnates.com/fintech/sec-moves-against-tech-startup-youplus-for-defrauding-investors/amp) |
| NS8 | The SEC says the CEO touted bank statements showing payments that never happened | [CyberScoop, reporting the SEC](https://www.cyberscoop.com/ns8-cyber-fraud-prevention-startup-adam-rogas-sec-fbi/) |
| ComplYant | Angel Investors Network, citing the SEC complaint, reports monthly subscription income never above $620 against decks showing up to $250,000 a month, and says nobody appears to have asked for a bank statement. These are allegations | [Angel Investors Network](https://angelinvestorsnetwork.com/startups/complyant-shiloh-luckey-startup-fraud-diligence-lessons) |

The quotes behind the table:

> "When one of the investors grew suspicious of Raz's claims, Raz allegedly provided the investor with falsified bank statements and forged contracts in an effort to conceal the fraud." ([Insurance Journal](https://amp.insurancejournal.com/news/east/2024/06/14/779473.htm))

> "When an investor pressed Shamim to furnish details of those claims, he allegedly provided the investor with falsified bank statements in an effort to conceal the fraud." ([Finance Magnates](https://financemagnates.com/fintech/sec-moves-against-tech-startup-youplus-for-defrauding-investors/amp))

> "Adam Rogas, the co-founder and former CEO of the startup, touted bank statements showing payments from NS8 customers that never happened, according to the SEC." ([CyberScoop](https://www.cyberscoop.com/ns8-cyber-fraud-prevention-startup-adam-rogas-sec-fbi/))

In the NS8 case, the criminal complaint (as posted by a Hacker News commenter; I could not open the filing) says an audit firm's employee was directed to have company staff pull the statements:

> "The Auditor was directed by a more senior Audit Firm employee to have someone from NS8 log in to the online portal for each NS8 bank account, display the current account balance, and download monthly bank statements for fiscal year 2019." ([DOJ filing as posted by a Hacker News commenter](https://news.ycombinator.com/item?id=24522396))

A commenter on the same thread describes the usual rule:

> "You would not trust the account statements that the company gives you, you would get the same (hopefully) account statements yourself." ([Hacker News commenter PeterisP](https://news.ycombinator.com/item?id=24523476))

A chartered-accountant journal says the same about evidence:

> "Audit evidence is considered to be more reliable when obtained in a documented form directly by the auditor from sources independent of the entity being audited." ([BCA Journal](https://bcajonline.org/journal/external-confirmations-proving-existence-with-external-evidence/))

GoMechanic is a different kind of case: reporters say an EY probe during a funding round found inflated revenue and fictitious garages, from two anonymous sources:

> "A probe into the seven-year-old startup by EY as part of the due diligence for the recent funding deliberation found scores of issues, including inflated revenue and that some garages were fictitious, two sources said." ([TechCrunch](https://techcrunch.com/2023/01/17/sequoia-india-backed-gomechanic-faces-severe-trouble))

## 6. How Tricorder checks it

Tricorder finds differences in reporting. It does not detect forgeries and it does not say why files differ.

**What a script can check**

Existing: 1.11 What the room cannot settle. When statements are present, for each month `tie_gap(t) = deposits(t) - (revenue(t) + financing(t))`, flagged when `|tie_gap| / revenue` passes `match_tolerance` ([FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md)). I call this check `bank_tie_out`. It also writes the ask when statements are missing, with the stage set to "after term sheet", which matches the sources above.

Proposed new checks:

- `statement_balance_roll`. For each statement, `opening + deposits - withdrawals = closing` within a cent. Show the months that fail.
- `statement_chain`. Closing balance of month t equals opening balance of month t+1, for every account, and no month is missing between the first and last statement.
- `holder_name_matches_entity`. The account holder's name equals the company's legal name in the incorporation documents and the cap table.
- `bank_balance_vs_model_cash`. The latest closing balance equals the cash figure in the model's assumptions and the deck.
- `financing_deposits_vs_cap_table`. Each investor wire on a statement matches a SAFE or share purchase on the cap table by amount and month.
- `payroll_outflow_vs_pnl`. Payroll outflows by month against the P&L payroll line.
- `processor_payouts_vs_billings`. Processor payouts plus fees and refunds equal billings for the month, when a processor export is present.
- `pdf_producer_signals`. Read the PDF's producer and the gap between its creation and modification dates. This is weak evidence. Flinks, a bank-data vendor, says a single signal is often a false positive and that printing a statement to PDF can trigger one:

  > "Don't auto-reject on a single signal. A single fraud signal (especially “unusual document source” alone) may be a false positive." ([Flinks, vendor view](https://docs.flinks.com/guides/upload/fraud-signals))

  > "When users print their bank statement to PDF instead of downloading the original file, the resulting document may trigger fraud signals." ([Flinks, vendor view](https://docs.flinks.com/guides/upload/fraud-signals))

  So Tricorder shows these as a note beside a failed balance roll, and never alone.

**What needs a model to read**

- Classify each large deposit: customer payment, processor payout, investor wire, loan, transfer between the company's own accounts, refund. Quote the statement line.
- Spot founder transfers, related-party payments and round-number deposits near a fundraise. Show the lines; do not say what they mean.
- Read descriptions on payroll and tax payments.

**What Tricorder cannot check**

- That the statement is the bank's own. A bank call, a statement sent by the bank, or a connector with the founder's consent can; the roadmap's bank-check slice uses a banking connector, and Plaid's Sandbox can serve a test feed for a demo ([writers' brief, 1:52 PM block](../../features/20261022.01_hackathon_plan/00_brief_for_writers.md)).
- That every account is disclosed. Only the founder can say. A confirmation request sent by the auditor straight to the bank can ask about other facilities too, according to the BCA Journal.
- That the people who produced the statements did not control the process (the NS8 pattern). Statements should come from the bank, not from the company.

## 7. Which readout pieces it feeds

- **Burn and runway:** cash balance, burn, payroll outflows.
- **Traction and revenue:** deposits against revenue.

Checklist rows: Bank statements (3 to 12 months); Revenue in the deck reaches the bank; Bank feed through a banking connector (roadmap, not built); Current monthly burn and the bank balance behind it ([CHECKLIST.md](../../ongoing/CHECKLIST.md)).

## 8. If it is missing

- **Pre-seed:** not expected.
- **Seed:** a gap, asked for after a first meeting or at the pre-wire step. It is never a red flag.
- **Series A:** a gap that goes on the ask list with the stage "after term sheet" ([FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md), entry 1.11).

If the founder is asked and refuses, that is a fact for the operator to record. Hustle Fund treats it as a red flag (section 2). Tricorder only records that the item was requested and not received.

One-line ask for the founder: "Please send statements for every business bank account for the last 12 months, downloaded straight from the bank, or give read-only access through your bank."

## 9. In the Hollis Voice room

Not in the room. The full room has 17 files and none is a bank statement (checked in [hollis_financials_facts_output.json](raw/hollis_financials_facts_output.json)); the checklist records "not in the room".

What the room does hold that a bank statement would settle:

- The model's Assumptions tab gives "Cash at the data date (USD)" as $1,800,000 with the note "Bank balance at 2026-09-30".
- The Cash_Bridge tab ties money raised, less losses, to that cash within -$0.24. That agreement is inside the founder's own files.

FRAMEWORKS 1.11 turns the missing statements into an ask. No flag is planted for this document. The 1:52 PM decision lets the generator write a Hollis Voice bank feed whose deposits disagree with the revenue file in one planted place, for the roadmap's bank-check slice.

## 10. Sources

Each page is saved under [raw/bank-statements/](raw/bank-statements/).

| Source | Type | Saved file |
|---|---|---|
| [Kruze, banking documentation](https://kruzeconsulting.com/blog/startup-due-diligence-banking-documentation/) and [accounting mistakes](https://kruzeconsulting.com/blog/startup-accounting-due-diligence-mistakes/) | accounting firm | kruzeconsulting_com_blog_startup_due_diligence_banking_documentation.txt, kruzeconsulting_com_blog_startup_accounting_due_diligence_mistakes.txt |
| [Hustle Fund, verify claims](https://www.hustlefund.vc/post/angel-squad-how-to-verify-startup-claims) and [burn rate](https://www.hustlefund.vc/post/angel-squad-startup-burn-rate-management-what-investors-should-actually-watch-for) | fund | hustlefund_vc_post_angel_squad_how_to_verify_startup_claims.txt, web_hustlefund_vc_post_angel_squad_startup_burn_rate_management_what_investors_should_actually_watch_for.txt |
| [SaaStr, Lemkin on due diligence](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet) | media | saastr_com_how_when_why_vcs_do_due_diligence_pre_and_post_term_sheet.txt |
| [Papermark, YC data room](https://www.papermark.com/blog/data-room-for-yc-startups) and [red flags](https://www.papermark.com/blog/due-diligence-red-flags) | vendor | papermark_com_blog_data_room_for_yc_startups.txt, papermark_com_blog_due_diligence_red_flags.txt |
| [Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), [Peony](https://www.peony.ink/blog/series-a-data-room) | vendors | visible_vc_blog_what_to_include_in_your_data_room.txt, peony_ink_blog_series_a_data_room.txt |
| [20VC newsletter](https://20vc.substack.com/p/20vc-newsletter-june-2nd-2024) | newsletter | web_20vc_substack_com_p_20vc_newsletter_june_2nd_2024.txt |
| [Hacker News, data-room thread](https://news.ycombinator.com/item?id=48606618) | community | hn_data_room_diligence_comment.json |
| [Insurance Journal, Joonko](https://amp.insurancejournal.com/news/east/2024/06/14/779473.htm), [Calcalist, Joonko](https://www.calcalistech.com/ctechnews/article/rjekedprc), [Accounting Today, Joonko](https://accountingtoday.com/news/sec-charges-joonko-founder-ilit-raz-with-defrauding-investors) | news | amp_insurancejournal_com_*.txt, calcalistech_com_*.txt, accountingtoday_com_*.txt |
| [Finance Magnates, YouPlus](https://financemagnates.com/fintech/sec-moves-against-tech-startup-youplus-for-defrauding-investors/amp) | news | financemagnates_com_*.txt |
| [CyberScoop, NS8](https://www.cyberscoop.com/ns8-cyber-fraud-prevention-startup-adam-rogas-sec-fbi/) and [Hacker News NS8 threads](https://news.ycombinator.com/item?id=24522396) | news, community | cyberscoop_com_*.txt, hn_item_24522396.json, hn_item_24520960.json, hn_item_24519198.json, hn_item_23903894.json |
| [Angel Investors Network, ComplYant](https://angelinvestorsnetwork.com/startups/complyant-shiloh-luckey-startup-fraud-diligence-lessons) | angel network (secondary) | angelinvestorsnetwork_com_startups_complyant_shiloh_luckey_startup_fraud_diligence_lessons.txt |
| [TechCrunch, GoMechanic](https://techcrunch.com/2023/01/17/sequoia-india-backed-gomechanic-faces-severe-trouble) | news | techcrunch_com_2023_01_17_sequoia_india_backed_gomechanic_faces_severe_trouble.txt |
| [Flinks fraud signals](https://docs.flinks.com/guides/upload/fraud-signals), [DocuClipper](https://www.docuclipper.com/docs/understanding-bank-statement-fraud-detection/), [Bectran](https://bectran.com/post/detect-forged-bank-statements) | vendors | docs_flinks_com_*.txt, docuclipper_com_*.txt, bectran_com_*.txt |
| [beancount.io, Stripe payout reconciliation](https://beancount.io/blog/2026/08/25/how-to-reconcile-stripe-payouts-gross-vs-net-fees-refunds-guide) | vendor blog | beancount_io_blog_2026_08_25_how_to_reconcile_stripe_payouts_gross_vs_net_fees_refunds_guide.txt |
| [BCA Journal, external confirmations](https://bcajonline.org/journal/external-confirmations-proving-existence-with-external-evidence/) | accountants' journal | bcajonline_org_journal_external_confirmations_proving_existence_with_external_evidence.txt |
| [Standard Ledger](https://www.standardledger.co/uk/article/preparing-your-financials-for-investor-due-diligence), [Patron Accounting](https://www.patronaccounting.com/blog/due-diligence-ready-books-startups), [Cooley GO sample list](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/) | accounting and law firms | read for background; saved in this folder |

Pages that blocked me: two justice.gov press releases (one titled as a founder's guilty plea and one as a sentencing; justice.gov returns an empty page to scripts, so their saved files are empty), the NS8 complaint PDF on justice.gov (an HTML stub), the SEC's NS8 press release and litigation release and the Joonko litigation release (HTTP 403), the Document Cloud copy of the NS8 complaint (403), Staffing Industry Analysts on Joonko (403), a Newsfile copy of the SEC's Joonko release (empty), and one Calcalist Joonko link (404). The orchestrator can read these through a browser. A GameOn indictment appeared in a search result only; I did not use it.
