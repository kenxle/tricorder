# Customer contracts and order forms (top ten)

Written 2026-10-22 for the Tricorder document guides. Quotes are checked word for word against the saved pages by [verify_quotes_customers.py](raw/verify_quotes_customers.py); each is listed in [quotes_customers.csv](quotes_customers.csv). A vendor view is marked as one.

## Summary

- **This is the paper behind the revenue.** It decides whether the customers counted in ARR can leave, when, and at what price.
- **Series A expects it; seed can do with less.** The lead at Series A wants the signed contracts for the ten largest customers and anything above about $20,000.
- **The most common problem is a count that runs ahead of the paper.** A pilot, a one-time deal or a contract the customer can cancel in a few months is counted as a year of recurring revenue.
- **Tricorder already reads these contracts.** [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md) entry 1.13 (Contract terms) compares each contract's terms with how the customer is counted. This guide adds the stage rules, the flags with sources, four extra checks and the ask-list line.
- **In the Hollis Voice room** only three contracts exist, in the second tier. One is the planted pilot, one is the largest customer, one is a clean decoy.

## 1. What it is

A customer contract is the signed agreement between the company and one customer. It can be an order form, a master services agreement with a statement of work, subscription terms, a pilot or trial agreement, or an amendment. It sets the term, the price, how it renews and how either side can end it. The founder or the company's operations lead gathers them, usually as signed PDFs. DocSend's checklist also asks for the company's standard terms of service for customers, which is the template the individual contracts start from ([DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/)).

## 2. At seed and at Series A

- **Pre-seed:** not expected. The data-room table marks it N.
- **Seed:** lighter (L). Visible's stage table marks the row 'Major customer, vendor, partner contracts' as not needed at pre-seed, lighter at seed, and expected at Series A and growth. ([Visible, an investor-update vendor](https://visible.vc/blog/what-to-include-in-your-data-room/)) A seed room with paying business customers can hold the standard order form and the largest customer's contract. (My reading; no source gives a seed minimum.)
- **Series A:** expected (Y). “At Series A, the lead wants the signed contract and may call the customer.” ([Peony, a data room vendor](https://www.peony.ink/blog/series-a-data-room)) The ask is “Top ~10 customer contracts and any material contract above ~$20,000” ([Peony, a data room vendor](https://www.peony.ink/blog/series-a-data-room)), and Kruze lists “Top 10 client invoices and contracts (only matters for b2b companies)” ([Kruze Consulting](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/)).
- **When it is shared:** often held back until after a term sheet. Peony says customer contracts belong in the second tier, shared after a signed term sheet, so a lead who has not committed does not see them. ([Peony, a data room vendor](https://www.peony.ink/blog/series-a-data-room))
- **What changes:** at seed the associate asks whether the revenue is real; at Series A, whether it is recurring (my reading). Juro says the revenue-quality questions (are contracts genuinely recurring, on what terms, with what termination rights) matter most from Series B on, and that at Series A investors mostly check that the agreements exist and are signed. ([Juro, a contract software vendor](https://juro.com/learn/contract-due-diligence)) Fortune's reporting suggests early-stage funds already ask the recurring question when a founder claims ARR from pilots (see section 5).

## 3. What a first pass checks

In order:

1. Which customers carry the revenue, and is there a contract in the room for each of the ten largest?
2. Is each contract signed by both sides, dated, and current, with every amendment attached?
3. What are the start date, the end date and the length of the term?
4. Can the customer leave while the term runs? Notice that ends a running contract is a different thing from notice not to renew at the end of the term.
5. Does it renew by itself, for how long, and with what notice?
6. Is it a pilot, trial or evaluation? Does anything make the customer buy afterwards?
7. What price does it state, with what discount, ramp and one-time fees? Does that match the revenue counted?
8. Has it gone live? A contract that starts next quarter is not this quarter's revenue.
9. Does it hold exclusivity, most-favored-customer pricing, a change-of-control right, uncapped liability, or a refund or clawback?
10. Do the contracts share one template, or has every deal been written by hand?

## 4. Green flags

- **Signed paper behind every counted customer.** “Your annual recurring revenue (ARR) in the deck should reconcile to the underlying billing, contract and revenue schedules.” ([CRV](https://www.crv.com/content/what-is-a-data-room))
- **A long, fixed term with no exit for convenience.** Buyers split ARR by how much can leave soon. “A buyer does not just ask how much ARR you have. They ask how much of that ARR can walk away in the next 30 days.” ([Livmo, an advisory firm](https://livmo.com/blog/saas-contract-length-valuation/)) Livmo reports that ChartMogul data on more than 2,500 SaaS companies shows annual plans drive stronger retention, and that annual prepaid customers sit in the strongest risk band a buyer uses. ([Livmo, an advisory firm, second-hand ChartMogul figures](https://livmo.com/blog/saas-contract-length-valuation/))
- **A pilot that is paid and has a plan to convert.** “In the companies I work closely with, roughly, the conversions vary fairly widely from about 60% to over 90%.” ([Jason Lemkin, SaaStr](https://www.saastr.com/what-is-the-typical-conversion-from-paid-pilot-to-annual-contract-in-b2b-saas-2))
- **ARR that equals what the paper supports.** “ARR gives full credit for the annualized recurring contract and nets out non-recurring revenue” ([Bessemer Venture Partners](https://www.bvp.com/atlas/scaling-to-100-million))
- **One template with the deviations explained.** “If there are contracts with non-standard terms, known gaps, or issues you're aware of, address them in a covering note rather than waiting for them to be discovered.” ([Juro, a contract software vendor](https://juro.com/learn/contract-due-diligence))
- **Auto-renewal that the company tracks.** “Auto-renewal contracts can be a positive signal, supporting revenue predictability, or a concern if they've created obligations the business isn't actively tracking.” ([Juro, a contract software vendor](https://juro.com/learn/contract-due-diligence))

## 5. Red flags and pitfalls

Common:

- **Pilots, one-time deals and unactivated contracts counted as recurring.** “Founders are counting pilots, one-time deals, or unactivated contracts as recurring revenue, six VCs told Fortune” ([Fortune, Sep 2025](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/)) A top-firm VC told Fortune about a defense-tech founder who claimed $325,000 of ARR from a contract that turned out to be a two-week pilot, backed by 'good authority' that the customer would keep paying; the VC wanted a signed piece of paper. ([Fortune, Sep 2025, unnamed VC](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/))
- **Booked ARR on contracts the customer can leave.** Fortune writes that “contracts frequently have provisions that let customers opt out at any time for any reason” ([Fortune, Sep 2025](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/)) An early-stage VC told Fortune that some founders sign contracts with kill provisions, claim the booked ARR, and give the customer an out: a million-dollar-a-year contract that the customer can cancel after three months for no reason. ([Fortune, Sep 2025, unnamed VC](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/)) Jason Lemkin of SaaStr says established vendors often turn pilots into opt-outs: “allowing new customers to cancel the contract after 60 days for any or no reason if they aren’t happy” ([Jason Lemkin, SaaStr](https://www.saastr.com/what-is-the-typical-conversion-from-paid-pilot-to-annual-contract-in-b2b-saas-2)). So a short opt-out is normal. The flag is counting it as a year of ARR, not the clause.
- **Signed but not yet live.** “there was clear separation between ARR, CAR (signed contract value before activation), and recognized revenue (actual revenue booked)” ([Fortune, Sep 2025](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/)) Lighter Capital, a revenue-based lender, defines committed MRR as current MRR plus signed contracts going into production, minus revenue likely to churn. ([Lighter Capital, a lender](https://www.lightercapital.com/blog/how-to-calculate-committed-mrr-cmrr))
- **Missing, unsigned or hasty paper.** “Many early-stage businesses reach Series A with contracts that were put together quickly, without standardized contract templates or proper execution.” ([Juro, a contract software vendor](https://juro.com/learn/contract-due-diligence)) “A data room does not cure a missing board approval, an unsigned IP assignment, or a contract that says something different from your deck.” ([Consilium Law, Aug 2026](https://consilium.law/sparkpoint/startup-fundraising-legal-due-diligence-checklist/))
- **A deck that says one thing and a contract another.** “Where they disagree, the disagreement is the finding.” ([Consilium Law, Aug 2026](https://consilium.law/sparkpoint/startup-fundraising-legal-due-diligence-checklist/))
- **Counting a free pilot as a customer.** A free pilot is a weak signal. Lemkin writes: “unpaid pilots are a waste of time … 95% of the time” ([Jason Lemkin, SaaStr](https://www.saastr.com/what-is-the-typical-conversion-from-paid-pilot-to-annual-contract-in-b2b-saas-2))

Rare but serious:

- **A termination right for the customer's convenience in a large account.** “Contracts that contain a termination for convenience right for the other party will be discounted by buyers, potentially materially reducing enterprise value at exit.” ([Koley Jessen, Jan 2026](https://www.koleyjessen.com/insights/publications/9-contract-issues-that-can-diminish-value-in-pe-portfolio-companies)) (This firm writes about private-equity portfolio companies; the point carries to any buyer later.)
- **A change-of-control right in the largest customer's contract.** “To a buyer, that ARR is no longer clean recurring revenue. It is conditional revenue.” ([Accord & Shield Legal, Jul 2026](https://accordshield.com/blog-diligence-grade-contracts)) “Some contracts give the counterparty rights to terminate, renegotiate, or require consent in the event of a change of control.” ([Juro, a contract software vendor](https://juro.com/learn/contract-due-diligence))
- **Most-favored-customer pricing.** “MFN clauses promise a customer they will always receive the lowest price offered to anyone else.” ([Koley Jessen, Jan 2026](https://www.koleyjessen.com/insights/publications/9-contract-issues-that-can-diminish-value-in-pe-portfolio-companies))
- **Exclusivity or minimum commitments that limit the company.** “Restrictions that could constrain the financing, operations, growth, or a later transaction: exclusivity, most-favored-customer pricing, minimum commitments, renewal terms.” ([Consilium Law, Aug 2026](https://consilium.law/sparkpoint/startup-fundraising-legal-due-diligence-checklist/))
- **Side agreements and verbal promises outside the signed paper.** Juro lists side agreements, verbal commitments and informal arrangements as exposure investors look for at Series A. ([Juro, a contract software vendor](https://juro.com/learn/contract-due-diligence))
- **Inconsistent terms across customers.** “Gaps and inconsistencies don't necessarily indicate wrongdoing, but they do suggest a business that hasn't been rigorous about managing its obligations, which is itself a risk factor investors take seriously.” ([Juro, a contract software vendor](https://juro.com/learn/contract-due-diligence))

## 6. How Tricorder checks it

**How this guide fits entry 1.13.** [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md) entry 1.13 (Contract terms) already reads every customer contract and compares it with how the customer is counted. This guide uses its names, labels and settings (`short_notice_days`, `min_contract_months`, `match_tolerance`) and changes none of them. What this guide adds:

- the stage rules and ask-list wording for the document;
- the green and red flags with their sources;
- four checks that 1.13 does not run: top-ten coverage by name, signature and date, a renewal calendar, and clause notes;
- a note that 1.13 should run at seed too, because the pilot and cancellation problems appear before Series B.

**What a script can check**

Existing checks (from entry 1.13, all after Saturday except the pilot reading):

- `cancellable_within_notice_vs_arr`: a customer who can leave within `short_notice_days` is counted as a year of ARR.
- `pilot_without_duty_to_convert_vs_recurring`: a pilot with no duty to convert counted as recurring.
- `plan_revenue_past_term_end`: the plan keeps a contract's revenue after its term ends.
- `signed_not_live_vs_revenue`: a signed contract that has not started counted as revenue.
- `contract_price_vs_counted_price`: the counted price differs from the contract's price.
- `counted_line_without_contract`: a counted line with no contract in the room.
- Entry 1.2's `arr_from_subscription_rows` and entry 1.6's `top_customer_share` stay where they are.

Proposed additions (names are mine):

- `top_ten_contract_coverage`. Rank customers by counted MRR in the as-of month (onboarding excluded). Ties are listed, not broken silently. `coverage_top10 = (top-ten customers with a contract in the room) ÷ 10`. Each missing one writes "Not in the room: the contract for <customer>" and one ask-list line. It differs from `counted_line_without_contract`, which works on the model's ARR lines, not on the ten largest customers by name.
- `contract_execution_state`. For each contract the model returns the signer names, titles and signature date, each with a quote and page. The script writes a `watch` when a party has no signature or date, and `cannot_check` when the file has no text layer. This answers the Juro point that “A contract that was never properly executed isn't enforceable in the way the parties might assume.” ([Juro, a contract software vendor](https://juro.com/learn/contract-due-diligence))
- `renewal_calendar`. From the typed terms entry 1.13 already produces, a script lists each contract's `term_end`, `last_notice_day` and `earliest_exit` in date order. A date inside the plan window (the months the model plans) is a `watch`. It uses 1.13's own formulas; it adds no new setting.
- `clause_notes`. Where 1.13's typed terms say `exclusivity`, `most_favoured_customer` or `change_of_control` is stated, the script writes a `watch` on any customer whose `plan_share` is above `match_tolerance`, with the quote. The comparisons in 1.13 do not use these three terms today. A watch is a question for a lawyer, not a verdict.

**What needs a model to read**

- Every term in the 1.13 prompt: dates, term, both kinds of notice, termination for convenience, pilot or trial and duty to convert, fee schedule, discount, list price, exclusivity, most-favored-customer, change of control, other clauses that change what the customer pays or when it can leave.
- Signature blocks, dates and amendment dates.
- Whether the contracts share one template, shown by quoting the clauses that differ.
- Clauses 1.13 does not list: uncapped liability, indemnity, assignment, and refund or credit rights.
- For each term, the model must quote the exact span and give the page. A term without a quote that the checker can find is not used.

**What Tricorder cannot check (the operator does)**

- Whether the contract on file is the one in force, and whether a side letter or verbal promise exists. Ask the founder; Juro lists these as the exposure investors look for.
- Whether the customer is real and paying. That needs the bank check ([ROADMAP.md](../../ongoing/ROADMAP.md) bank-check slice) or a customer call.
- Whether a clause will be triggered by this financing. That is for a lawyer.
- A contract changed to match the books. Entry 1.13 says so: such a contract gets through, and the readout says so wherever it matters.

## 7. Readout pieces and checklist items

Feeds the **traction and revenue** and **customers** pieces; the renewal calendar also informs **retention**.

Checklist items ([CHECKLIST.md](../../ongoing/CHECKLIST.md)): the document itself, customer contracts and order forms (C34); a customer who can leave on short notice is not counted as a year of ARR (C38); a pilot with no duty to convert is not counted as recurring (C39); the plan keeps no revenue past a contract's end (C40); a signed contract that has not gone live is not counted (C41); the counted price matches the contract (C42); every counted customer line has a contract (C43); ARR rebuilt from contracts and revenue rows (C05); and customer concentration (C37).

## 8. If it is missing

- **Seed:** a gap, not a red flag. The room is expected to be thin. If the deck claims recurring revenue from named customers and no contract is in the room, the claim is unsupported, and the readout says "not enough in the room" for traction.
- **Series A:** a gap that holds the traction and customers pieces at "not enough in the room". It turns into a red flag when other files show a pilot or a short exit that the paper would settle, as in the Hollis row label "Marlow Veterinary Group (pilot)".
- **Ask-list line (seed):** "Please send the standard order form and the signed contract for your largest paying customer."
- **Ask-list line (Series A):** "Please send the signed contracts, order forms and amendments for your ten largest customers by revenue, any pilot or trial agreement, and any contract above $20,000."

## 9. In the Hollis Voice room

The full room holds three contracts in [04_customers/](../../../data_room/hollis_voice/04_customers/). They are second-tier files, absent from the seed drop (the thin first tier a founder sends before a first meeting); the cover note says they are shared on request after a first meeting. On the seed drop, entry 1.13 returns `cannot_check` with the gap "Not in the room: customer contracts".

- **[Marlow pilot](../../../data_room/hollis_voice/04_customers/pilot_agreement_marlow.pdf).** Planted red flag: pilot booked as ARR. Six months, $15,000 a month, either side may end it on 30 days notice, and nothing requires the customer to buy. The financial model counts it at $180,000 a year against $90,000 of total fees.
- **[Cedar & Pine order form](../../../data_room/hollis_voice/04_customers/order_form_cedar_pine.pdf).** The largest customer, 40 locations, a 24-month term to 2027-10-31, fees fixed, no exit except an unfixed breach. The paper is clean. The planted flag is the deck: it says no customer is above 9 percent of ARR, and this contract makes the customer 21.0 percent of subscription MRR (figure from entry 1.6). This is a green flag for the paper and a red flag for the claim.
- **[Brookline Row order form](../../../data_room/hollis_voice/04_customers/order_form_brookline_row.pdf).** The decoy: an annual prepaid plan at 10 percent off list. It must not be flagged.
- **What is not in the room.** Of 213 customers with revenue in 2026-09, the room holds a contract for three. By the script [top_customers_vs_contracts.py](raw/customer-contracts-and-order-forms/top_customers_vs_contracts.py), two of the ten largest have one (Cedar & Pine ranks first and Marlow second). Ranks 3 to 10 all tie at $1,099 a month, and none of those customers has a contract in the room. Entry 1.13 reports that the three contracts cover 27.6 percent of counted MRR. No standard terms, no master agreement, no side letter.

## 10. Sources

Saved under [raw/customer-contracts-and-order-forms/](raw/customer-contracts-and-order-forms/).

- [Fortune, Sep 2025](https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/)
- [Peony, Series A data room](https://www.peony.ink/blog/series-a-data-room) (vendor view)
- [Visible, what to include in your data room](https://visible.vc/blog/what-to-include-in-your-data-room/) (vendor view)
- [Kruze Consulting, VC due diligence checklists](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/)
- [CRV, what is a data room](https://www.crv.com/content/what-is-a-data-room)
- [Bessemer Venture Partners, scaling to $100 million](https://www.bvp.com/atlas/scaling-to-100-million)
- [Hustle Fund, angel due diligence checklist](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)
- [Juro, contract due diligence](https://juro.com/learn/contract-due-diligence) (vendor view)
- [Consilium Law, legal due diligence checklist](https://consilium.law/sparkpoint/startup-fundraising-legal-due-diligence-checklist/)
- [Koley Jessen, nine contract issues](https://www.koleyjessen.com/insights/publications/9-contract-issues-that-can-diminish-value-in-pe-portfolio-companies)
- [Accord & Shield Legal, diligence-grade contracts](https://accordshield.com/blog-diligence-grade-contracts)
- [Livmo, SaaS contract length and valuation](https://livmo.com/blog/saas-contract-length-valuation/) (advisory firm; second-hand figures)
- [Jason Lemkin, SaaStr, paid pilot conversion](https://www.saastr.com/what-is-the-typical-conversion-from-paid-pilot-to-annual-contract-in-b2b-saas-2)
- [Lighter Capital, committed MRR](https://www.lightercapital.com/blog/how-to-calculate-committed-mrr-cmrr) (lender view)
- Also saved and read, not quoted: the [Koley Jessen commercial-contracts PDF](https://www.koleyjessen.com/media/publication/119_Important_Considerations_for_Portfolio_Company_Commercial_Contracts.pdf), [Potomac Law on change of control](https://www.potomaclaw.com/news-Change-of-Control-Problem-Nobody-Owns-in-M-and-A-Until-Its-Too-Late), [Torys on commercial contracts](https://torys.com/startup-legal-playbook/negotiating-commercial-contracts), [Acquisition Stars on SaaS contract assignment](https://acquisitionstars.com/blog/saas-customer-contracts-ma-assignment), [Standard Ledger on pilots](https://www.standardledger.co/uk/article/from-pilot-to-paid-how-to-stop-giving-your-product-away-for-free/) and [Stage 2 Capital on pilots](https://gtm.stage2.capital/p/should-we-offer-pilots).
- Local: [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md) entries 1.2, 1.6, 1.11 and 1.13; [CHECKLIST.md](../../ongoing/CHECKLIST.md); the Hollis Voice room and [answer key](../../../data_room/answer_key.json); the 30-document table in [research_data_room.md](../20261022.02_research/research_data_room.md).

## Pages that blocked automated fetching

None for this guide. The DocSend checklist was saved earlier through a browser by the orchestrator.

Reddit: none suggested.
