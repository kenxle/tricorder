# Memo template

> **Update, 2:14 PM:** the deliverable is the interactive memo, not a PDF. See [The memo for the principal](../features/20261024.02_first_steps_ui/02_ui_decisions.md#the-memo-for-the-principal).

## Charter

**What belongs:** The memo Tricorder drafts for the partners' meeting. Its sections in order, what each holds, which readout pieces and checklist items fill it, how each line links down to its claims and sources, where the top green and red flags, the gaps and the ask list sit, which sections carry assumptions a reader can tweak, and what stays the operator's to write. A short filled example on the demo company.

**What does not:** How a piece's verdict or the headline flags are computed (that is [FRAMEWORKS.md](FRAMEWORKS.md), "The readout"). The list of diligence items (that is [CHECKLIST.md](CHECKLIST.md)). How the memo page looks (that is [STYLE_GUIDE.md](STYLE_GUIDE.md)). How the export, the reader copies and the scenarios are built (that is [ARCHITECTURE.md](ARCHITECTURE.md) and the [memo-export](roadmap/memo-export.md) and [reader-scenarios](roadmap/reader-scenarios.md) slices).

**Level of detail:** A builder can write the export from this file without asking: for each section, its inputs, its line kinds and its links. An operator can see what Tricorder will hand them and what they still have to write.

**Sources:** [the memo research](../reports/20261022.02_research/research_memos.md) with [memos.csv](../reports/20261022.02_research/memos.csv), [memo_section_counts.csv](../reports/20261022.02_research/memo_section_counts.csv) and [memo_sections.py](../reports/20261022.02_research/memo_sections.py); [the writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), its 1:58 PM block (this template), 2:00 PM block (an interactive memo) and 2:01 PM block (each reader's own copy and scenarios), and the blocks from 12:55 PM on (the readout's shape, the operator, steering, the ask list, the checklist); [PRODUCT_BRIEF.md](PRODUCT_BRIEF.md), "The readout" and "Steering the readout"; [FRAMEWORKS.md](FRAMEWORKS.md), "The readout" and the Piece and Claim schema; [CHECKLIST.md](CHECKLIST.md) with [checklist.csv](checklist.csv); [BRAND.md](BRAND.md), "A green flag and a red flag, at the top"; [ROADMAP.md](ROADMAP.md), the memo-export, reader-scenarios and financial-model slices; [data_room/answer_key.json](../../data_room/answer_key.json) for the example.

## Summary

- **The memo reads like the memos partners already know.** Its order comes from 28 published memos and 6 templates: summary and the ask first, then the company, market, product, the numbers, competition, team, deal terms, risks, outcomes, and the recommendation last ([the memo research](../reports/20261022.02_research/research_memos.md), "The usual order").
- **The opening summary carries the top green and red flags.** 25 of the 28 memos open with a summary. Tricorder's is the headline list from the readout, plus the nine pieces at a glance.
- **Every line drills down.** One click opens the claims behind a line. One more opens a claim's source in place and every source that agrees or disagrees. The partners get the same two clicks as the operator.
- **Gaps and the ask list are part of the memo.** A gap shows as "Not in the room" in the section it belongs to. The ask list sits just before the recommendation.
- **The operator writes the recommendation and the judgement.** Tricorder never says invest or pass, and never scores the company as a whole.
- **Each reader gets their own copy.** A reader can steer it and tweak four assumptions (whether the pilot counts, churn, price, hiring pace). The scripts recompute, and each tweaked number is marked as that reader's scenario. The shared version stays the operator's.
- **A static PDF stays available,** with every claim footnoted to its source.

## The sections, in order

The order follows the median position of each section in the published memos ([memo_section_counts.csv](../reports/20261022.02_research/memo_section_counts.csv)). Section names are plain words. Where the research found two common sections that Tricorder fills from the same pieces, they are joined.

| # | Section | What it holds | Filled from (readout pieces and entries) | Checklist items | Who writes it |
|---|---|---|---|---|---|
| 1 | Header | To, from, date, and a "Re" line naming the company, the round and the ask. The data date of the room. The memo's version. | The pitch itself (raise, pre-money). The room's as-of date. | The pitch deck (C60) and the cap table (C72). | Tricorder fills it; the operator signs it. |
| 2 | Summary and the ask | One paragraph on what the company does and what it is raising. Then the best green flags and the worst red flags. Then the nine pieces at a glance, each with its verdict and reason. A line left blank for the operator's recommendation. | Top green and red flags; piece verdicts ([FRAMEWORKS.md](FRAMEWORKS.md), "The readout"). | The one-page summary (C61) and every number on the deck tied to a file (C64). | Tricorder drafts; the operator writes the recommendation line. |
| 3 | Company and problem | Who the customer is, the problem, how the company solves it today, and why now. | Deck and overview claims (entry 1.1). Lean canvas and jobs to be done (5.1, 5.2). | The cover note (C59) and whether the story matches what is online (C92). | Tricorder drafts from the company's own words, marked as the company's. |
| 4 | Market | The market size, how it was built, and who built it. Outside signals for the company and its competitors. | Market piece. Market signals (3.1, 3.2). Bottom-up market size (5.6). | Market sizing (C47), bottom-up market size (C48), competitors' hiring and traffic (C49), published pricing and customer wins (C50). | Tricorder. |
| 5 | Product | What exists today, what is on the roadmap, and what customers say about it. | Deck, one-pager and website claims (1.1). The pitch video's claims with timestamps (4.1). Online presence (7.1). | Product roadmap and demo (C63), roadmap against the use of funds (C68), founder video (C62), reviews (C89). | Tricorder; product judgements are marked "Reading:". |
| 6 | Business model and unit economics | How the company makes money, its price, gross margin, and acquisition cost and payback. | Unit economics piece. Gross margin composition (1.7). Unit economics recompute (1.9). Accounting mislabels (1.12). | Unit economics (C30), gross margin rebuilt with every delivery cost (C31), CAC, payback and LTV recomputed (C32), blended CAC (C33). | Tricorder. |
| 7 | Traction and customers | Revenue and how it is counted, growth, retention, the largest customers, and what the contracts say. | Traction and revenue, retention and customers pieces. ARR definition check (1.2), cohort retention (1.3), deck against model (1.5), customer concentration (1.6), vanity metrics (1.8), contract terms (1.13), the video's three-way check (4.3). | Traction and revenue (C02 to C13), retention (C14 to C18), customers and contracts (C34 to C46). | Tricorder. |
| 8 | Competition and comparables | Who else does this, and the public companies and private rounds the company should be measured against, each with the reason it is a fair comparison. | Comps piece. Public comps (2.1) and recent private rounds (2.2). Competitors' signals (3.1, 3.2). Five forces (5.4). | Public comparable companies (C51), recent private rounds (C52). | Tricorder. |
| 9 | Team | The founders and senior team, what each has done before, how long they have worked together, and the hiring plan. | Team piece. Founder-market fit (6.1) and passion and commitment (6.2). | Founder bios (C53), key team bios (C54), founder-market fit (C55), the people in the plan exist (C56), co-founder issues (C91), the company's own hiring (C93). | Tricorder for facts; the operator for their view of the founders. |
| 10 | Financials, burn and runway | Cash, monthly burn, runway with and without the hiring plan, and the raises so far. | Burn and runway piece. Burn against the hiring plan (1.4). What the room cannot settle (1.11). | Financial model (C19), monthly statements (C20), bank statements (C21), hiring plan (C22), payroll rebuilt from the hiring plan (C24), current burn and bank balance (C29). | Tricorder. |
| 11 | Deal terms | The round, the price, the instrument, the investors before, and whether the cap table adds up. | The pitch itself piece. Cap table reconciliation (1.10). | Cap table (C72), prior financing documents (C75), the ask matches the cap table (C67), cap table adds to 100 percent (C81), investors checked against the cap table (C90). | Tricorder for the facts; the operator for whether the price is right. |
| 12 | Risks and open questions | Every red flag in full, every weak or mixed piece's reason, and the gaps that matter, each as a short labelled risk. | Every claim with severity "flag". The reasons of weak and mixed pieces. Gaps. | Whatever item each risk comes from. | Tricorder lists them; the operator ranks them and adds their own. |
| 13 | Outcomes | The operator's downside, base and upside cases. The facts they rest on: the round, the comps, and the runway with the hiring plan. | Deal terms, comps and burn and runway pieces. | Recent private rounds (C52). | The operator. |
| 14 | Diligence: what was checked and what to ask | Coverage: for the company's stage, which checklist items were found, checked or missing. The "could not verify" box. The ask list. | The checklist coverage and the ask list, built by script from gaps and weak pieces. | Every item expected at the stage, and the four asks: current burn and bank balance (C29), customer reference calls (C46), founder reference calls (C58), the founder walking from source data to each flagged number (C71). | Tricorder. |
| 15 | Recommendation | Invest, pass or wait. The amount and any conditions. The two reasons that decide it, and why it could be wrong. | Nothing. | None. | The operator. |
| 16 | Sources and change log | Every source the memo cites, with its file and locator or URL and the date read. The version log: each steer, each operator edit, and what changed. | Every claim's sources. The steer history. | Every number on the deck tied to a file (C64). | Tricorder. |

The research's "Appendix" (6 of 28 memos) is not a separate section. Its job, the supporting tables, is done by the drill-down: any table a claim rests on opens in place.

## How each line links down

Every line in the memo is one of five kinds. The kind shows on the line, so a reader always knows what stands behind it.

| Line kind | What it is | One click opens | Two clicks open |
|---|---|---|---|
| Claim line | A sentence Tricorder wrote from one or more claims. | The claims behind it: each claim's text, value, confidence label (computed, quoted or judged) and verdict mark (corroborated or contradicted). | The claim's source in place (the cell, the slide, the clause, the video second), with every other source that corroborates or contradicts it. |
| Reading line | A model's judgement with nothing to recompute. Starts with "Reading:". | The claims it cites. | Their sources. |
| Gap line | Starts "Not in the room:" and names what is missing. | The checklist item and its line on the ask list. | The item's published checklists, with links. |
| Operator line | A sentence the operator wrote. Marked as theirs, with no claim behind it. | Who wrote it, and in which version. | Nothing further. If the line states a number, the editor asks the operator to attach a claim or leaves the number marked "operator's figure, no source". |
| Scenario line | A number recomputed from a reader's tweaked assumptions. Exists only in that reader's copy. | The assumptions the reader changed. | The script that recomputed it and the room rows it read. |

Rules every section follows:

- **Every claim keeps its source link.** A claim line that loses its claims is dropped, not shown bare. The quote checker runs again on export. A claim that fails it moves to the "could not verify" box in section 14.
- **Sections open with their pieces.** Each section's first line names the readout pieces it draws on, with each piece's verdict and its corroborating and contradicting source counts. One click on a piece opens its claims, the same as in the readout.
- **Sections close with their coverage.** Each section's last line counts its checklist items found, checked and missing at the company's stage, and links to them.
- **Gaps sit where they belong.** "Not in the room: bank statements" sits in Financials, burn and runway, not only in section 14. Each gap links to its ask-list line.
- **Steers show.** When the operator steers a section, the new section replaces the old with a visible diff, and the change log in section 16 gets a line. A steer changes what is read and how it is worded. It never changes a script's number.

## The top green and red flags

They open the memo, inside section 2, in the shapes [BRAND.md](BRAND.md) sets ("A green flag and a red flag, at the top"). Green flags come first. A script picks both, by the rule in [FRAMEWORKS.md](FRAMEWORKS.md) ("Top green and red flags"): at most one per piece, green flags only from pieces that read looking strong, and no padding. Each flag is a claim line, so it drills down like any other.

Under the flags is the nine-piece table: piece, verdict, the one-line reason, and the two source counts. Strong pieces get the same space as weak ones, in the readout's piece order or the order the operator set.

Each red flag appears again in section 12, written as a risk, and in the section its piece belongs to. A red flag is a difference in reporting between files, or between a file and the outside world. The memo never calls it fraud.

## Gaps and the ask list

- **In the sections.** Each gap is a gap line in the section of its piece.
- **In section 14.** The coverage table for the company's stage, from [CHECKLIST.md](CHECKLIST.md): each item found, checked or missing. Then the ask list: one line per missing item expected at the stage and per weak piece that more information could settle. Each line says what to ask for, why (the claim or gap it would settle), and which section it feeds. An item marked "lighter" at the stage is asked for "if you have it". The operator can copy the list into an email to the founder.
- **A gap is not a red flag.** A missing document is a question for the operator, as [CHECKLIST.md](CHECKLIST.md) says.

## Risks and open questions

Section 12 follows the published habit and adds the structure the newest template asks for ([the memo research](../reports/20261022.02_research/research_memos.md), "How risks and open questions are written"):

- **A short label, then the risk in one or two sentences.** 13 of the 16 published risk sections are short labelled lists.
- **Each risk carries its evidence:** the stated number, the found number, and the two sources, as claim lines.
- **Each risk says what would settle it,** and links to the ask-list line that requests it.
- **The operator ranks the risks** and may add risks of their own, as operator lines. Tricorder lists them in the order of the headline red flags, then the other weak and mixed pieces, then gaps.

## The operator's part

Tricorder drafts everything it can source. These stay the operator's:

- **The recommendation** in section 15, and its one line in section 2: invest, pass or wait, the amount, the conditions, the two deciding reasons, and why it could be wrong.
- **The outcome cases** in section 13. Tricorder supplies the facts they rest on.
- **The judgement lines:** whether the price is right, what they think of the founders, how they rank the risks, and anything they add from a call or a meeting.
- **The signature.** The header's "From" line is the operator.

Every operator line is marked as theirs. Tricorder never fills these with its own words, and never writes an overall score.

## Each reader's copy and their scenarios

- **The shared version is the operator's.** It changes only when the operator edits or steers it. Each change makes a new version with a change-log line.
- **Each reader gets their own copy,** laid over the shared version. A reader can steer their copy (rewrite a section, ask for more information) by the same rules as the operator. Their copy says what they changed and which shared version it started from. When the shared version moves on, the reader sees which version their copy is based on.
- **A reader can tweak four assumptions.** The same scripts that rebuilt the numbers recompute them. The room's files never change.

| Assumption | Where a reader changes it | What it recomputes | Sections that show the result |
|---|---|---|---|
| The pilot counted as recurring, or not | Traction and customers | ARR and every figure built on ARR | 7, and the ARR line in 2 |
| Churn rate | Traction and customers | Retention, future revenue, lifetime value | 7, 6 and 10 |
| Price | Business model and unit economics | Revenue per account, payback, lifetime value | 6 and 7 |
| Hiring pace: which planned hires happen, and when | Financials, burn and runway | Payroll, monthly burn, runway | 10 and 13 |

- **Scenario numbers sit beside the real ones, never in place of them.** Each tweaked figure shows in three columns: the company's figure (with its source), Tricorder's rebuilt figure (with its script), and "Your scenario" (with the assumption changed). The scenario column is shaded and names the reader.
- **A scenario changes no verdict and no flag.** Verdicts and flags come from the room's files. A scenario is a what-if, so it is never written into a piece.
- **Scenarios stay in the reader's copy.** They never reach the shared version or the shared PDF. A reader who exports their own copy gets a PDF stamped as their scenario on every page that shows one.

## The static PDF

The same sections in the same order. Every claim line carries a footnote with the file, the locator, the quoted text and the date read. Gap lines and operator lines are marked as such. The "could not verify" box prints at the end of section 14. The PDF is made from the shared version, so it holds no reader's scenario.

## Example: Hollis Voice (fictional)

A short filled example on the synthetic room, cut down to the header, the summary, one section, one risk and part of the ask list. Every number comes from [data_room/answer_key.json](../../data_room/answer_key.json). The percentages are the answer key's ratios as [FRAMEWORKS.md](FRAMEWORKS.md) writes them ("Top green and red flags"). Arrows (↳) mark what one click opens.

> **To** Partners **From** [the operator] **Date** [date] **Re** Hollis Voice, Series A, $9,000,000 at $45,000,000 pre-money. Room data as of 2026-09-30. Shared version 1.
>
> **2. Summary and the ask**
>
> Hollis Voice sells a phone agent to independent veterinary clinics. It is raising a $9,000,000 Series A at a $45,000,000 pre-money valuation, after $5,500,000 in SAFEs.
>
> **Recommendation:** [the operator writes this]
>
> **Green flag: the round adds up.** $9,000,000, stated in the deck and the same in the cap table and the model (pitch_deck.pdf, slide 13; cap_table.xlsx, Cap_Table!B24; financial_model.xlsx, `SERIES_A_RAISE`). Nothing in the room contradicts it.
> ↳ 3 claims, 3 independent sources
>
> **Green flag: the market size is stated the same way twice.** $252,000,000, on deck slide 8 and in the model's Market tab (`MARKET_TAM_USD`). Both are the company's own estimate.
>
> **Green flag: staff today agrees.** 17, on deck slide 10 and in the model (`STAFF_NOW`).
>
> **Red flag: runway leaves out the hiring plan.** 37 months stated (the model and the deck); 19 months found when all 24 planned hires are paid for (hiring_plan.csv, rebuilt). Burn and runway reads looking weak.
>
> **Red flag: sign-ups shown as active clinics.** 357 stated (deck); 212 paying accounts found (monthly_metrics.csv, `paying_accounts`). Traction and revenue reads looking weak.
>
> **Red flag: one customer is 21% of revenue.** No customer above 9% stated (deck); the largest customer, Cedar & Pine, is 21% of MRR (customer_mrr_by_month.csv). Customers reads looking weak.
>
> [Two more red flags: gross margin, 80% stated against 58.1% rebuilt; net revenue retention, 102.6% stated against 87.3% rebuilt. Then the nine pieces at a glance.]
>
> **7. Traction and customers**
>
> Pieces: traction and revenue, looking weak. Retention, looking weak. Customers, looking weak.
>
> ARR is stated four ways. The founder says about $3,000,000 in the video, the deck says $2,500,000, the model says $2,240,868, and the subscription rows give $2,060,868.
> ↳ 4 claims: pitch_video_script.md at 0:35; pitch_deck.pdf, slide 3; financial_model.xlsx, ARR_Build!E15 (`ARR_TOTAL`); customer_mrr_by_month.csv, subscription rows
>
> The model counts the Marlow Veterinary Group pilot at $180,000 a year of ARR. The pilot agreement allows 30 days' notice and has no duty to convert. Its contracted fees total $90,000.
> ↳ 3 claims: financial_model.xlsx, ARR_Build!E13; pilot_agreement_marlow.pdf, page 2, "7. Termination." and "8. No duty to convert."
>
> | ARR | Company's figure | Tricorder rebuilt | Your scenario: pilot counted as recurring |
> |---|---|---|---|
> | | $2,500,000 (deck, slide 3) | $2,060,868 (subscription rows) | $2,240,868 |
>
> [The scenario column shows only in the copy of the reader who set it.]
>
> Not in the room: customer references and letters of intent. ↳ ask list
>
> **12. Risks and open questions**
>
> **Runway.** The model shows 37 months, but paying all 24 planned hires gives 19. The model's average monthly net burn over the last 12 months is $374,461.81; rebuilt from the hiring plan it is $480,061.81. Settled by: current monthly burn and the bank balance behind it. ↳ ask list
>
> **14. Diligence: what to ask the founder** (part)
>
> - Current monthly burn and the bank balance behind it. Why: the rebuilt burn is above the model's, and cash of $1,800,000 rests on the model alone. Feeds: Financials, burn and runway.
> - Bank statements for the last 3 to 12 months. Why: not in the room. Feeds: Financials, burn and runway.
> - The sales pipeline. Why: not in the room. Feeds: Traction and customers.
> - Whether Marlow Veterinary Group will convert, and on what terms. Why: the pilot is counted as ARR with no duty to convert. Feeds: Traction and customers.
>
> **15. Recommendation**
>
> [The operator writes this.]
