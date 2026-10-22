# Material agreements other than customer contracts

Written 2026-10-22 for the Tricorder document guides. Quotes are checked word for word against the saved pages by [verify_quotes_customers.py](raw/verify_quotes_customers.py); each is listed in [quotes_customers.csv](quotes_customers.csv). A vendor view is marked as one.

## Summary

- **This is the pile of everything the company has signed except customer contracts.** Leases, loans and liens, vendor and licensing agreements, insurance policies, consulting agreements, agreements with officers, and any agreement with obligations over $25,000.
- **It is a Series A item, read mostly by counsel after a term sheet.** A seed room needs a list of what the company owes and any debt; the copies come later.
- **The most useful first-pass check is arithmetic on the expense ledger.** A vendor paid more than the threshold in a year should have an agreement in the room. A lease, loan or policy that shows up in the books should too.
- **Most serious findings are rare:** a lender's lien on the IP, a founder's personal guarantee, a covenant that the next round breaks, a contractor who never assigned the code, a copyleft licence in the product.
- **In the Hollis Voice room** none of these documents exist, but the expense ledger shows ten non-payroll vendors above $25,000 in the last twelve months, rent that steps up three times, and insurance premiums. All would need paper.

## 1. What it is

DocSend's checklist groups these as 'Material agreements' and lists property leases, loans and liens, loans the company has made, insurance policies, licences of the company's IP to others and of other people's IP to the company, standard forms, consulting agreements, agreements with officers and directors, and anything outside the ordinary course that could matter to the business. ([DocSend, due diligence checklist](https://www.docsend.com/blog/due-diligence-checklist/)) One item sets the line for what counts: “Any agreements or understandings between your company and others with obligations exceeding $25,000” ([DocSend, due diligence checklist](https://www.docsend.com/blog/due-diligence-checklist/)). Cooley's request list, written for investor counsel, splits the same ground into debt financing, other agreements, and management and consultants. It asks for “All debt instruments and credit agreements entered into by the Company, including lease financing, which are currently in effect.” ([Cooley GO, sample request list](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/)) “Real property leases, including any amendments and all exhibits to such documents.” ([Cooley GO, sample request list](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/)) It also asks for “Consulting contracts.” ([Cooley GO, sample request list](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/))

The founder, the finance lead or outside counsel assembles them. They arrive as signed PDFs, often with a one-page list. This guide covers every agreement except customer contracts, which have [their own guide](customer-contracts-and-order-forms.md).

## 2. At seed and at Series A

The sources do not agree on a threshold, and DocSend names no stage.

- **DocSend.** DocSend frames its whole checklist as what investors ask for after a term sheet is signed. ([DocSend, due diligence checklist, page note](https://www.docsend.com/blog/due-diligence-checklist/)) Its line for a material agreement is $25,000.
- **Peony** (a data room vendor) sets it lower, at about $20,000: “Top ~10 customer contracts and any material contract above ~$20,000” ([Peony, a data room vendor](https://www.peony.ink/blog/series-a-data-room))
- **MaRS**, a Canadian innovation hub, sets it lower still. “Typically, contracts exceeding a specific financial value (normally $5,000) or with key partners need to be shared with an investor.” ([MaRS Discovery District](https://learn.marsdd.com/article/data-room-basics-for-startups-stage-2-data-for-investor-due-diligence/))
- **Kruze** lists “Material contracts with vendors/suppliers” ([Kruze Consulting](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/)) among the common financial diligence items.
- **Visible.** Visible's stage table marks the row 'Major customer, vendor, partner contracts' as not needed at pre-seed, lighter at seed, and expected at Series A and growth. ([Visible, an investor-update vendor](https://visible.vc/blog/what-to-include-in-your-data-room/))
- **Counsel's view.** Cooley's list is the fullest, and counsel works from it after the term sheet (my reading). Consilium Law says the inventory of consent and notice triggers should be done “before serious diligence access, since consent timelines belong to the counterparty” ([Consilium Law, Aug 2026](https://consilium.law/sparkpoint/startup-fundraising-legal-due-diligence-checklist/))

What this means for Tricorder: seed is lighter, Series A is expected. The threshold is a setting, `material_agreement_threshold_usd`, defaulting to $25,000 (DocSend) and changeable by the operator to the fund's own line.

Debt changes by stage. “Most institutional venture lenders will expect at least one preferred round of equity financing before being willing to provide a venture debt facility.” ([Foley Hoag, Aug 2024](https://foleyhoag.com/news-and-insights/publications/alerts-and-updates/2024/august/10-things-to-know-about-venture-debt/)) So a seed room with venture debt is unusual and worth a note, while a Series A room with a lender is ordinary. Peony lists a separate venture debt data room as the debt raise that often follows a Series A. ([Peony, a data room vendor](https://www.peony.ink/blog/series-a-data-room))

Insurance has its own timing. “Business insurance before a funding round, specifically Directors & Officers (D&O) Insurance, is typically required by investors as a condition of close.” ([Vouch, an insurance broker, vendor view](https://www.vouch.us/blog/when-does-my-startup-need-insurance)) This is a broker's view; no investor-published standard was found. “Tech and SaaS contracts often also require Cyber Insurance and Tech E&O Insurance.” ([Vouch, an insurance broker, vendor view](https://www.vouch.us/blog/when-does-my-startup-need-insurance))

## 3. What a first pass checks

In order:

1. Is there a list of material agreements, and is a copy in the room for each?
2. Which vendors were paid more than the threshold in the last twelve months, and which of those have an agreement in the room?
3. Does the company have any debt: bank loans, venture debt, equipment financing, notes other than SAFEs? Do the books show interest, loan proceeds or a lender? Do the loan documents match?
4. For each loan: what is pledged, what covenants apply, what counts as a default, are there warrants, did the founders give a personal guarantee?
5. For the lease: rent schedule, end date, renewal, guarantee, and who must consent to an assignment.
6. For key vendors and licences: term, price changes, minimum commitments, exclusivity, what happens on a change of control, and whether the licence lets the company do what it does.
7. For insurance: which policies, which limits, for what period, and is D&O in place at close.
8. For consultants and contractors: is each agreement signed, does it assign the work to the company, and are they treated as contractors in the books?
9. For agreements with officers, directors and their affiliates: what is owed to or by the company?
10. Which agreements need a consent or approval because of this financing?

## 4. Green flags

- **A contract register.** “Create a master log that records, for each contract, the counterparty, the contract type, the effective date , the expiry or renewal date, whether it has been properly executed, and any material or unusual terms.” ([Juro, a contract software vendor](https://juro.com/learn/contract-due-diligence))
- **Executed copies, kept apart from drafts.** Klehr's checklist names the opposite as a common mistake (see section 5).
- **Disclosure in a cover note rather than discovery.** “If there are contracts with non-standard terms, known gaps, or issues you're aware of, address them in a covering note rather than waiting for them to be discovered.” ([Juro, a contract software vendor](https://juro.com/learn/contract-due-diligence))
- **Debt of an ordinary shape.** A law firm describes the usual terms. “Venture lenders typically receive a first-priority (senior) security interest in all assets of the company.” ([Foley Hoag, Aug 2024](https://foleyhoag.com/news-and-insights/publications/alerts-and-updates/2024/august/10-things-to-know-about-venture-debt/)) “It is common for intellectual property to be excluded from the collateral grant, but remain subject to a negative pledge” ([Foley Hoag, Aug 2024](https://foleyhoag.com/news-and-insights/publications/alerts-and-updates/2024/august/10-things-to-know-about-venture-debt/)) Debt like this is not a flag by itself. A first-priority claim on the IP is the exception. Jon Levy of YC writes: “Sometimes lenders ask for a first-priority security interest on a company’s IP” ([Jon Levy, Y Combinator](https://www.ycombinator.com/blog/venture-debt-101-basics-and-approach)) and says companies should not accept that term.
- **Old liens cleared.** A paid-off loan can leave a filing that looks live: “A UCC-1 filing that appears active can represent paid-off debt with a missing termination statement, or it can represent a live obligation.” ([Acquisition Stars (advisory blog)](https://acquisitionstars.com/blog/ucc-lien-search-buying-a-business)) A UCC-3 termination or a payoff letter for each paid loan clears it.
- **Insurance in place before it is demanded.** D&O, plus cyber and E&O where customer contracts ask for them (see section 2).
- **Signed assignments from everyone who built the product.** This is the opposite of the contractor flag in section 5.
- **A written open-source policy and a dependency inventory.** Promise Legal advises: “Maintain a dependency inventory. List every open-source dependency in your project, including transitive dependencies.” ([Promise Legal, a law firm blog](https://blog.promise.legal/startup-central/open-source-license-compliance-for-startups/))

## 5. Red flags and pitfalls

Common:

- **Missing or unsigned agreements.** “A contract that was never properly executed isn't enforceable in the way the parties might assume.” ([Juro, a contract software vendor](https://juro.com/learn/contract-due-diligence))
- **Executed and draft copies mixed.** “Mixing executed and draft contracts.” ([Klehr Harrison Harvey Branzburg](https://klehr.com/publications/startup-evolution-a-year-long-journey-through-a-founders-toolkit-due-diligence-ready-building-a-data-room-that-wins-investor-confidence/))
- **Contractors with no assignment.** “Payment alone does not transfer ownership.” ([Revision Legal, Jun 2026](https://revisionlegal.com/corporate/revision-legal/ip-assignment-mistakes-startup-acquisition-due-diligence/)) “Paying for development work does not, by itself, create the written chain of title an investor wants.” ([CRV](https://www.crv.com/content/what-is-a-data-room))
- **A lease that the founders guarantee.** “Especially for start-ups or new businesses lacking a strong credit history and steady revenues, commercial landlords will likely ask the owners to sign personal guarantees of their company’s lease obligations.” ([Taft Law, Nov 2023](https://www.taftlaw.com/news-events/law-bulletins/even-the-smallest-commercial-lease-is-a-big-deal-here-are-seven-key-issues-prospective-tenants-need-to-consider-and-address/)) “Commercial leases almost always require the landlord to give prior approval beforehand.” ([Taft Law, Nov 2023](https://www.taftlaw.com/news-events/law-bulletins/even-the-smallest-commercial-lease-is-a-big-deal-here-are-seven-key-issues-prospective-tenants-need-to-consider-and-address/))
- **A cloud or vendor commitment above what the company will use.** “An AWS EDP shortfall is the unused part of your annual commitment, invoiced in full with no discount.” ([Redress Compliance, a licensing advisory, vendor view](https://redresscompliance.com/aws-edp-shortfall-risk-management)) (This is an advisory firm's view of AWS enterprise deals.)
- **Heavy dependence on one supplier.** “Investors want to understand whether the business has supplier dependencies that create concentration risk” ([Juro, a contract software vendor](https://juro.com/learn/contract-due-diligence)). For an AI product, the analyst firm Verdantix writes: “Model labs can turn access to API services on or off with limited notice by ending contracts” ([Verdantix, an analyst firm](https://www.verdantix.com/insights/blog/enterprise-software-vendors-should-heed-warning-from-anthropic-s-usage-limit-reduction))
- **Insurance missing at close.** “It's not a policy to scramble for after a term sheet.” ([Vouch, an insurance broker, vendor view](https://www.vouch.us/blog/when-does-my-startup-need-insurance))

Rare but serious:

- **A first-priority lien on the IP.** “Sometimes lenders ask for a first-priority security interest on a company’s IP” ([Jon Levy, Y Combinator](https://www.ycombinator.com/blog/venture-debt-101-basics-and-approach)) (YC says companies should not accept it.) A negative pledge on the IP is common, but it still limits later financing. “It is common for intellectual property to be excluded from the collateral grant, but remain subject to a negative pledge” ([Foley Hoag, Aug 2024](https://foleyhoag.com/news-and-insights/publications/alerts-and-updates/2024/august/10-things-to-know-about-venture-debt/))
- **A default that triggers on a change in business or on the investor.** Foley Hoag says lenders may use “an event of default that is either triggered by a material adverse change (MAC) with respect to the business or a lack of investor support” ([Foley Hoag, Aug 2024](https://foleyhoag.com/news-and-insights/publications/alerts-and-updates/2024/august/10-things-to-know-about-venture-debt/)) YC defines investor abandonment: “A clause that allows the lender to demand repayment if a company’s investor doesn’t invest in the company’s future round.” ([Jon Levy, Y Combinator](https://www.ycombinator.com/blog/venture-debt-101-basics-and-approach))
- **A personal guarantee by the founders.** Foley Hoag: “the venture lender may request a personal guaranty from the founders” ([Foley Hoag, Aug 2024](https://foleyhoag.com/news-and-insights/publications/alerts-and-updates/2024/august/10-things-to-know-about-venture-debt/))
- **A covenant or subordination that the new round breaks.** Foley Hoag says “Venture debt agreements contain tight restrictions on a company’s ability to engage in certain activities without lender consent” ([Foley Hoag, Aug 2024](https://foleyhoag.com/news-and-insights/publications/alerts-and-updates/2024/august/10-things-to-know-about-venture-debt/)) It adds that “venture lenders typically require that all existing debt of the company, including convertible notes, is subordinated to the new debt facility” ([Foley Hoag, Aug 2024](https://foleyhoag.com/news-and-insights/publications/alerts-and-updates/2024/august/10-things-to-know-about-venture-debt/))
- **A lien that shows on the public record for a loan already paid.** Acquisition Stars writes that “lenders do not always file UCC-3 terminations promptly, or at all” ([Acquisition Stars (advisory blog)](https://acquisitionstars.com/blog/ucc-lien-search-buying-a-business)) InCorp: “These filings remain effective for five years from filing dates unless terminated earlier or continued before expiration.” ([InCorp, a registered-agent service](https://www.incorp.com/resources/knowledge-base/what-is-a-ucc-search)) A terminated filing needs care too. Cogency Global writes, for lenders, that “it may be your first inclination to ignore a UCC that has a termination listed” ([Cogency Global, a filing services firm](https://www.cogencyglobal.com/blog/ucc-termination-statements-part-2/))
- **Agreements that need consent because of the financing.** Cooley's list asks for “Agreements requiring consents or approvals in connection with the financing.” ([Cooley GO, sample request list](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/)) Consilium Law lists “Merger and change-of-control provisions, reviewed separately.” ([Consilium Law, Aug 2026](https://consilium.law/sparkpoint/startup-fundraising-legal-due-diligence-checklist/))
- **Related-party agreements and loans.** Cooley's list asks for “Any agreements, understandings or proposed transactions between the Company and any of its employees, officers, directors, affiliates, or any affiliate thereof” ([Cooley GO, sample request list](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/))
- **A non-compete or exclusive that limits the business.** Cooley's list asks for a “Brief description of any contract restricting the ability of the Company to compete in any line of business with any person or entity” ([Cooley GO, sample request list](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/))
- **Copyleft code in the product.** Lathrop GPM writes that “open source license compliance comes up relatively routinely in connection with financing (debt or equity funding) and M&A transactions” ([Lathrop GPM, 2021](https://www.lathropgpm.com/insights/understanding-and-complying-with-open-source-software-licenses-why-when-and-how/)) It adds that “requirements to provide representations and warranties on current and past compliance in financings and M&A agreements are typical” ([Lathrop GPM, 2021](https://www.lathropgpm.com/insights/understanding-and-complying-with-open-source-software-licenses-why-when-and-how/)) Law firms report that funds scan the code: “Venture capital firms and acquirers use software composition analysis (SCA) tools like FOSSA and Black Duck to scan codebases for open-source dependencies” ([Promise Legal, a law firm blog](https://blog.promise.legal/startup-central/open-source-license-compliance-for-startups/)) The model investment agreement asks the company to confirm it has not used open source “in any manner that would materially restrict the ability of the Company to protect its proprietary interests” ([FOSSA, quoting the NVCA model form, vendor view](https://fossa.com/blog/copyleft-licenses-venture-capital-connection/))

## 6. How Tricorder checks it

Today the checklist marks material agreements with obligations over $25,000 (C98), insurance policies (C99), and loans, liens and other encumbrances (C100) as "not checked yet". The only existing script check near this area is entry 1.11 (What the room cannot settle) in [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md), which tests whether IP assignments are present. Entry 1.12 kind e (contractors left out of headcount and burn) covers consultants in the books. Everything below is proposed; the names are mine.

**What a script can check**

- `material_agreement_coverage`. For each vendor-category in the expense ledger, sum the last twelve months. Skip payroll lines. If the sum is above `material_agreement_threshold_usd` and no agreement in the room names the vendor, write the gap "Not in the room: the agreement with <vendor> (<category>, $<sum> in the last twelve months)". Report `covered_share = (spend with an agreement in the room) ÷ (spend above the threshold)`.
- `debt_without_agreement`. If the model, balance sheet or ledger shows interest expense, loan proceeds, a lender, or a debt balance, and no credit agreement is in the room, write a gap. A cash bridge that reconciles on equity money alone means no debt is expected.
- `insurance_lines_without_policy`. If the ledger holds insurance premiums, ask for the policies and certificates. When a policy is read, a `watch` if its period ended before the as-of date.
- `rent_steps_vs_lease`. Compare each month's ledger rent with the lease's rent schedule, within `match_tolerance`. A step in the ledger with no step in the lease is a gap.
- `commitment_vs_spend`. If an agreement states a minimum annual commitment `C` and the ledger shows annual spend `S`, then `shortfall = max(0, C − S)`. A `watch` when it is above zero, carried into the fixed obligations the burn piece uses.
- `warrants_in_cap_table`. If a loan agreement grants warrants, the cap table must hold a matching row (the check belongs with entry 1.10, Cap table reconciliation). A mismatch is a flag.
- `consultant_without_agreement`. A ledger vendor tagged consulting or contractor, or a contractor named in the hiring plan, needs an agreement in the room.

**What needs a model to read**

- **Loans and security:** parties, amount, collateral, whether IP is pledged or only under a negative pledge, covenants, events of default (MAC, investor abandonment), warrants, guarantees, subordination, change of control.
- **Leases:** rent schedule, term, renewal, guarantee, assignment and subletting, and operating cost terms.
- **Vendor and licence agreements:** term, renewal, minimum commitment, price change rights, exclusivity, assignment, change of control, field of use, and whether the licence passes to a buyer.
- **Insurance:** type (D&O, cyber, E&O, general liability), limits, period, named insured.
- **Consulting agreements:** present-tense assignment of work product, scope, fees, whether the person works as an employee in all but name.
- **Consent triggers:** a list of agreements with assignment, change-of-control, consent or negative covenants. “Merger and change-of-control provisions, reviewed separately.” ([Consilium Law, Aug 2026](https://consilium.law/sparkpoint/startup-fundraising-legal-due-diligence-checklist/))
- For each item the model must quote the exact span and give the page. The checker drops any term whose quote it cannot find.

**What Tricorder cannot check (the operator does)**

- **A lien search** at the state filing office (a UCC search), and any payoff letter from a lender. Tricorder can ask for them. A paid search or a lawyer runs them.
- **Whether a loan or side agreement exists that nobody disclosed.** Every file in the room comes from the founder.
- **Whether a clause will be triggered by this financing.** That is for counsel.
- **Open-source compliance of private code.** It needs a scan of the codebase, which the founder or a scanning vendor runs. If the company has a public repository, a scan can run on it.
- **Whether a contractor is correctly classified**, and whether the insurer will confirm the policy.

## 7. Readout pieces and checklist items

Feeds **burn and runway** (rent, debt service, vendor minimums), **unit economics** (telephony, model usage and licence agreements set the cost of revenue), **legal and cap table** (liens, warrants, consents, IP licences, contractor assignments) and, for the lien search, the **outside world**.

Checklist items ([CHECKLIST.md](../../ongoing/CHECKLIST.md)): material agreements with obligations over $25,000 (C98); insurance policies (C99); loans, liens and other encumbrances (C100); agreements with third-party AI service providers (C104); every founder and contractor signed an IP assignment (C83). The checklist has no separate rows for leases, consulting agreements, licences in and out, agreements with officers and directors, or agreements needing consent; DocSend and Cooley name them. I suggest the checklist adds them.

## 8. If it is missing

- **Seed:** a gap, not a red flag. Ask only for a list of obligations over the threshold, any loan or note not on the cap table, the lease, and the insurance schedule.
- **Series A:** a gap that holds the legal and cap table piece, and the burn piece where it depends on the obligations, at "not enough in the room". It turns into a red flag when the books show something that needs paper (rent, a lender, insurance premiums, a large vendor) and no paper exists.
- **Ask-list line:** "Please send a schedule of every agreement with obligations over $25,000 and copies for your ten largest vendors; your lease; any loan, note or credit agreement with the lender's lien filings; your insurance policies and certificates, including D&O; and the agreements with any consultants or contractors, with their IP assignments."

## 9. In the Hollis Voice room

Not in the room. The 17 files contain no lease, loan, vendor agreement, licence, insurance policy or consulting agreement. The answer key plants no flag here, and the room's cash bridge uses only the two SAFE rounds as money in, so the room shows no debt.

What the expense ledger shows (the script [ledger_vendor_totals.py](raw/material-agreements-other-than-customer-contracts/ledger_vendor_totals.py) wrote [ledger_vendor_totals.csv](raw/material-agreements-other-than-customer-contracts/ledger_vendor_totals.csv); window is 2025-10 to 2026-09):

- **Ten non-payroll vendors are above $25,000 in the last twelve months, and none has an agreement in the room.** They are Gantry Workspace (rent), Tallow Telecom (telephony), Deskwise Software and Pinewell Analytics (tools), Halcyon Inference API (model usage), Pembry Legal Services, Marsh Speech Licensing (licences), Brindle Cloud Hosting, Dunmore Accounting Group and Tern Travel Desk. `material_agreement_coverage` would write ten gaps and a `covered_share` of zero.
- **Rent moves through four levels,** with three step-ups, in 2025-07, 2026-01 and 2026-07, ending at $27,240 a month. A lease would explain them. None is in the room.
- **Insurance premiums are in the ledger every month** from Pennant Insurance Brokers, with no policy to read.
- **Which agreements set the cost of revenue.** The deck says "Cost of revenue is phone minutes and speech software licences", and the ledger books Tallow Telecom and Marsh Speech Licensing that way. The planted margin flag is about hosting, model usage and support left out of cost of revenue. Those vendors (Brindle Cloud Hosting, Halcyon Inference API) have no agreements in the room either.

The demo can show this as a clean gap list built from the ledger, with the ask-list line above. It is not a planted flag. A later room variant could plant one, such as a vendor commitment above spend or a loan not on the cap table.

## 10. Sources

Saved under [raw/material-agreements-other-than-customer-contracts/](raw/material-agreements-other-than-customer-contracts/).

- [DocSend, due diligence checklist](https://www.docsend.com/blog/due-diligence-checklist/) (updated March 2026; saved through a browser)
- [Cooley GO, sample VC due diligence request list](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/)
- [Peony, Series A data room](https://www.peony.ink/blog/series-a-data-room) and [Visible, what to include in your data room](https://visible.vc/blog/what-to-include-in-your-data-room/) (vendor views)
- [Kruze Consulting, VC due diligence checklists](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/)
- [MaRS Discovery District, stage 2 data for investor due diligence](https://learn.marsdd.com/article/data-room-basics-for-startups-stage-2-data-for-investor-due-diligence/)
- [Klehr Harrison, due-diligence-ready data room](https://klehr.com/publications/startup-evolution-a-year-long-journey-through-a-founders-toolkit-due-diligence-ready-building-a-data-room-that-wins-investor-confidence/)
- [Juro, contract due diligence](https://juro.com/learn/contract-due-diligence) (vendor view)
- [Consilium Law, legal due diligence checklist](https://consilium.law/sparkpoint/startup-fundraising-legal-due-diligence-checklist/)
- [Foley Hoag, 10 things to know about venture debt](https://foleyhoag.com/news-and-insights/publications/alerts-and-updates/2024/august/10-things-to-know-about-venture-debt/)
- [Jon Levy, Y Combinator, Venture Debt 101](https://www.ycombinator.com/blog/venture-debt-101-basics-and-approach)
- [Acquisition Stars, UCC lien search](https://acquisitionstars.com/blog/ucc-lien-search-buying-a-business), [InCorp, what is a UCC search](https://www.incorp.com/resources/knowledge-base/what-is-a-ucc-search) and [Cogency Global, UCC termination statements](https://www.cogencyglobal.com/blog/ucc-termination-statements-part-2/) (filing and advisory firms)
- [Taft Law, commercial leases](https://www.taftlaw.com/news-events/law-bulletins/even-the-smallest-commercial-lease-is-a-big-deal-here-are-seven-key-issues-prospective-tenants-need-to-consider-and-address/)
- [Vouch, when a startup needs insurance](https://www.vouch.us/blog/when-does-my-startup-need-insurance) (broker; vendor view)
- [Redress Compliance, AWS EDP shortfall](https://redresscompliance.com/aws-edp-shortfall-risk-management) (advisory; vendor view)
- [Lathrop GPM, open source licences](https://www.lathropgpm.com/insights/understanding-and-complying-with-open-source-software-licenses-why-when-and-how/), [FOSSA, copyleft and venture capital](https://fossa.com/blog/copyleft-licenses-venture-capital-connection/) (vendor view) and [Promise Legal, open source compliance](https://blog.promise.legal/startup-central/open-source-license-compliance-for-startups/)
- [Revision Legal, IP assignment mistakes](https://revisionlegal.com/corporate/revision-legal/ip-assignment-mistakes-startup-acquisition-due-diligence/) and [CRV, what is a data room](https://www.crv.com/content/what-is-a-data-room)
- [Verdantix, model provider dependence](https://www.verdantix.com/insights/blog/enterprise-software-vendors-should-heed-warning-from-anthropic-s-usage-limit-reduction) (analyst view)
- Also saved and read, not quoted: [Vouch, what insurance startups need](https://www.vouch.us/blog/what-kind-of-insurance-do-startups-need), [DLA Piper on negative pledges](https://www.dlapiper.com/en-es/insights/publications/2024/09/ensuring-positive-outcomes-with-negative-pledges-in-venture-lending), [DLA Piper on acquisition consents](https://www.dlapiper.com/en-us/insights/publications/2024/07/acquisition-consents-for-venture-debt-transactions), [Capbase on venture debt](https://capbase.com/venture-debt-financing/), [Ashurst Perkins Coie on venture debt](https://www.ashurstperkinscoie.com/en/insights/four-tips-for-companies-considering-venture-debt-financing/) and [law.asia on investor rights](https://law.asia/startup-investments-terms/).
- Local: [FRAMEWORKS.md](../../ongoing/FRAMEWORKS.md) entries 1.10, 1.11 and 1.12; [CHECKLIST.md](../../ongoing/CHECKLIST.md); the Hollis Voice room, its [expense ledger](../../../data_room/hollis_voice/02_financials/expense_ledger.csv) and [README](../../../data_room/README.md).

## Pages that blocked automated fetching

The Wolters Kluwer guide on lien search strategy for legal due diligence returned HTTP 403. The orchestrator can read it through a browser. The DocSend checklist was saved earlier through a browser.

Reddit: none suggested.
