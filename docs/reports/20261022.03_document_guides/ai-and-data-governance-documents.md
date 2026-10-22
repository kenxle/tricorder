# AI and data governance documents

Document guide for Tricorder's scans, checklist and memo. Written 2026-10-22. Sources are saved under [raw/ai-and-data-governance-documents/](raw/ai-and-data-governance-documents/). Quotes are checked word for word against the saved pages by [build_quotes_people.py](raw/_people_tools/build_quotes_people.py); results are in [quotes_people.csv](quotes_people.csv). Facts about the Hollis Voice room come from [room_facts_people.py](raw/ai-and-data-governance-documents/room_facts_people.py) and its output [room_facts_people.out.txt](raw/ai-and-data-governance-documents/room_facts_people.out.txt).

This is the newest and least settled document group. No law firm or venture firm I found publishes a checklist that sets these documents by stage. The calls on stage below are my judgment from the sources, and they are marked as such. Nothing here is legal advice.

## What it is

DocSend's 2026 checklist adds a group it labels "AI/ML and data governance (New for 2026)". It holds eight items ([DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/), read through a browser and saved):

- **AI model documentation:** "Architecture, training methodologies, performance metrics, and validation processes".
- **Training data provenance:** "Documentation of data sources, licensing, and rights to use training data".
- **AI ethics and bias:** policies and tests to find and reduce algorithmic bias.
- **Data privacy compliance:** GDPR, CCPA and other regional rules.
- **Third-party AI services:** "Agreements with AI service providers (OpenAI, Anthropic, Google, etc.) and associated terms".
- **Responsible AI framework:** internal guidelines for building and deploying AI.
- **Model security:** "Safeguards against model theft, adversarial attacks, and prompt injection vulnerabilities".
- **Regulatory preparedness:** "Documentation showing awareness of and preparation for emerging AI regulations."

The CTO, a head of data or company counsel prepares them. In a young company they rarely exist as formal documents. What exists is a privacy policy, vendor terms, a security page, a few engineering notes and some customer contract clauses. The form is a set of policies, model cards, signed vendor contracts, data processing agreements and, for some, a SOC 2 report.

## At seed and at Series A

DocSend gives no stage. It frames the whole checklist as post-term-sheet work: "The only thing standing between you and the investor's money is the due diligence process." The [checklist](../../ongoing/CHECKLIST.md) therefore marks all eight items "not stated" at every stage (rows C102 to C109).

What other sources say:

- A UK business magazine says "Compliance evidence at seed, not Series B. SOC 2 progress and AI bias audits, once growth-stage concerns, are now appearing in seed-stage checklists." ([Startups Magazine, July 2026](https://startupsmagazine.co.uk/the-new-due-diligence-why-vcs-are-walking-away-from-ai-startups-with-hidden-legal-risk)). This is journalism by a marketing strategist, not investor data.
- Hustle Fund's angel checklist says "At seed, add retention, unit economics, go-to-market (GTM) repeatability, hiring, security, contracts, and a fuller financial review." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)). It scopes security to the data and promises involved, and says a company "selling into healthcare, finance, government, or large enterprises may need specialist review and evidence that matches its claims."
- Willkie, a law firm that advises investors, writes for AI investments in general and starts: "Willkie is a trusted adviser to global investors at the cutting edge of the AI frontier." ([Willkie, Sept 2025](https://www.willkie.com/publications/2025/09/optimizing-ai-investments-protecting-value-and-managing-risk-through-expert-diligence)).

My judgment, for the two primary personas (the associate who prepares the memo and the partner who reads it):

- **Seed:** expected only in thin form, and only when AI is the core of the product. A short note on which models the product uses and from whom, what data trains or tunes anything, how customer data is used, and the vendor terms. The other four items are not expected.
- **Series A, AI-core company:** expected in full for provenance, third-party agreements, privacy and security. Ethics and bias, a responsible-AI framework and regulatory preparedness stay lighter unless the product sits in a regulated use.
- **Company that only uses AI as a feature:** a privacy policy and the vendor terms are enough.

## What a first pass checks

1. What is the AI? A model the company trained, an open model it tuned, or calls to someone else's model? Hustle Fund's checklist asks "Dependencies: Which cloud, model, platform, supplier, manufacturer, or license can change cost or access?"
2. Where did any training or tuning data come from, and does the company have the right to use it? Willkie: "Every AI tool is trained on data, therefore we need to understand where an AI company obtains the data it uses to develop and train its tools, whether from its own customers or other collection methods, or from a third-party provider, and whether it has requisite legal authority to use that data for training purposes."
3. Do the contracts line up? Willkie again: "Where it subcontracts out some or all of the operation or development of its tools (for example, if its tool is built on a large-language model), an analysis is required to determine whether the rights, limitations, and obligations in the applicable contracts align with the contractual rights granted by the sources of the data."
4. What do customer contracts say about data use and about who is liable for outputs?
5. Is personal data (recordings, names, health details) in prompts, logs or training sets, and can it be deleted?
6. What security exists, scoped to the data held?
7. Which rules apply to this product and these customers?
8. Does the product do what the deck says it does? Willkie warns of "the use of shortcuts or vaporware that would undermine both the investment and an investor’s credibility in the market."
9. Does the cost of the AI vendor appear in cost of revenue? This links to the gross margin check.

## Green flags

- **A per-dataset record.** Peony, a data-room vendor, says to "Request a per-dataset training-data manifest: source, acquisition date, license terms, intended-use scope, licensee-of-record." ([Peony AI checklist, vendor](https://www.peony.ink/downloads/ai-due-diligence-checklist.pdf)).
- **A paper trail for the data.** The Innovation Attorney, a venture lawyer's newsletter (Oct 2026): "A founder who can show a signed license agreement for every commercial dataset, and a documented fair use analysis for everything else, walks into due diligence with an answer instead of an apology." ([Innovation Attorney](https://theinnovationattorney.substack.com/p/what-ai-startups-should-document)).
- **Dependence stated up front.** AI Business (a vendor site): "If you depend on one model provider today, say so clearly, explain why, and show the path to multi-provider resilience." It adds "Investors are not looking for perfection." ([AI Business, April 2026](https://aibusiness.vc/vc/ai-startup-due-diligence-checklist-2026)).
- **Consistent contract terms.** Same page: "You need clear policy, consistent contract templates, and documented exceptions."
- **A bill of materials for open-source code.** The Innovation Attorney warns "GPL licensed code inside an AI pipeline creates a contamination risk"; a company that has mapped its dependencies has the answer ready.

## Red flags and pitfalls

**Common**

- **"We used publicly available data" as the whole answer.** Startups Magazine: "“We used publicly available data” is no longer an answer; it is a red flag". Peony says to "Reject any manifest line reading 'publicly available web data' with no further documentation, and trace it back to a named source instead."
- **No contract for the AI vendor the product depends on.** DocSend lists "Agreements with AI service providers" as an item. Willkie's point on matching rights (above) cannot be tested without the contract.
- **Customer contracts silent on outputs.** Startups Magazine asks who is liable when a model defames someone, leaks personal data or reproduces copyrighted work: "If your customer contracts are silent, your investors will not be".
- **Personal data in training or logs with no plan.** Willkie names special risks from using personal data or confidential information to train AI, under privacy laws such as CCPA and GDPR. Katten, a law firm writing about AI company sales, lists what diligence should examine: "Diligence should examine what data the target holds; how it was collected; whether it includes personal data; whether it was obtained under contractual restrictions; and whether it can be used for model training, fine-tuning, validation, product improvement and postclosing integration." ([Katten](https://katten.com/ai-deals-call-for-tailored-approach-to-address-hidden-risks)).
- **Open-source licences nobody has mapped.** The Innovation Attorney, above.

**Rare but serious**

- **Training on pirated data.** In Bartz v. Anthropic, a federal judge gave final approval on July 20, 2026 to a class settlement in which "Anthropic agreed to pay $1.5 billion plus interest to a class of copyright owners whose works were allegedly torrented and commercially exploited from pirated datasets" ([Pearl Cohen](https://pearlcohen.com/federal-court-approves-1-5-billion-anthropic-copyright-settlement-largest-in-history)). The release "explicitly does not release claims related to AI outputs or future conduct." Jurist reports that the earlier ruling treated purchased books and pirated copies differently ([Jurist](https://www.jurist.org/news/2026/07/judge-approves-record-1-5-billion-settlement-involving-anthropic/)). Peony turns this into a test: "A documented yes scores 1 (Red) on the Data Layer regardless of how clean the other four tests are, and it is the most quantifiable downside in AI diligence." That score is the vendor's own scale.
- **An order to delete models.** A law-firm note defines the FTC's remedy: "Algorithmic disgorgement is the process in which illegally obtained data is removed from an AI model, and the destruction of any models or algorithms built using such data." ([Lathrop GPM](https://www.lathropgpm.com/insights/artificial-intelligence-and-algorithmic-disgorgement/)). It lists orders against Everalbum, Kurbo/WW, Ring and Edmodo.
- **Voice-agent rules.** Orrick: "calls containing AI-generated voices are subject to consent requirements imposed on “artificial or prerecorded voices” under the TCPA." ([Orrick, Feb 2024](https://orrick.com/Insights/2024/02/Did-the-FCC-Really-Ban-AI-Generated-Voice-Calls-No-But-Restrictions-Apply)). Orrick's title says the FCC did not ban such calls. A separate claim in Ambriz v. Google said a contact-centre AI wiretapped calls to Verizon. The court dismissed it in June 2024 with leave to amend, on the ground that Google acted as Verizon's agent ([Global Policy Watch](https://www.globalpolicywatch.com/2024/07/california-federal-court-dismisses-complaint-accusing-google-of-wiretapping-customer-service-calls/)). I did not check what happened next.
- **EU rules, if the product reaches the EU.** Gibson Dunn (May 27, 2026) reports a provisional agreement to move the high-risk deadline: "High-risk obligations for stand-alone Annex III systems are deferred to 2 December 2027". It adds that the transparency duty, "including the requirement to disclose to users when they are interacting with AI systems, remain unaffected" ([Gibson Dunn](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/)). The firm says the changes "only take legal effect upon formal adoption and publication of the Omnibus in the Official Journal, expected before 2 August 2026." My sources do not confirm that adoption happened, so check the final text before relying on the dates.

**Pitfalls for the reader**

- Most pages on this topic are vendor or marketing pieces. Willkie and Katten are law firms, but Katten writes about company sales and Willkie about investments in general. None of them sets a rule for seed against Series A.
- A model-written summary of a policy is not proof the practice exists. A policy on file shows intent; a vendor contract or a manifest shows fact.

## How Tricorder checks it

**What a script can check**

- Proposed `ai_governance_presence`: for each of the eight document types, `TRUE` if the room holds a file that matches by name or first-page heading (model card, training data manifest, DPA or privacy policy, vendor agreement, security policy, SOC 2 report). Every `FALSE` becomes a gap with a `would_need` line. It follows the same pattern as the `present(type)` test in [FRAMEWORKS 1.11](../../ongoing/FRAMEWORKS.md).
- Proposed `ai_vendor_spend_vs_agreements`: from the expense ledger, `ai_vendor_spend = SUM(amount WHERE category IN {model_inference, third_party_licences})`, listed per vendor, then `agreements_in_room = COUNT(files that name the vendor)`. A vendor with spend and no agreement is a gap.
- Existing `gross_margin_from_ledger` ([FRAMEWORKS 1.7](../../ongoing/FRAMEWORKS.md)): model inference booked outside cost of revenue shifts gross margin. This is the same cost seen from the margin side.
- Proposed `customer_contract_data_clause`: for each customer contract, `TRUE` if a clause names who owns call or customer data and how it may be used. A model finds the clause; a script counts.

**What needs a model to read**

- Customer contracts, vendor terms and policies: data ownership and use, whether customer data may train a model, retention, output ownership, liability caps and indemnities. Each claim carries the clause quoted and its page.
- A model card or technical note: what the model is, what it was trained on, how it is tested.
- It must not say a practice is compliant or legal. It reports what the paper says, and what is absent.

**What Tricorder cannot check (leave to the operator)**

- Whether training data was lawfully obtained. Only the engineers can say. Peony's binary question, whether any corpus included shadow-library content, goes to the CTO.
- Whether a policy is followed in practice.
- Security: a penetration test or SOC 2 audit is the evidence, and Tricorder cannot run one.
- Legal compliance and regulatory classification. A lawyer decides.
- Recording and consent practice on live calls, which varies by state.

## Readout pieces and checklist items

- **No readout piece names these documents today.** The checklist treats them as their own group of eight items (C102 to C109), all "not checked yet" and "not stated" for stage ([CHECKLIST](../../ongoing/CHECKLIST.md)).
- I suggest they feed the **legal and cap table** piece, with customer data clauses feeding **customers and contracts** and inference cost feeding **unit economics**.
- Related checklist items: C104 (agreements with third-party AI providers), C105 (data privacy compliance), C108 (model security), C109 (preparation for emerging AI regulation).

## If it is missing

- **Pre-seed:** not expected.
- **Seed:** a gap only if AI is core to the product. A question to the founder, not a red flag.
- **Series A, AI-core company:** a firm gap. Still not a red flag by itself, since the research says a missing document is a question for the operator ([data-room research, 1.5](../20261022.02_research/research_data_room.md)). A weak spoken answer, such as "publicly available data" with nothing behind it, reads worse than a missing file.
- **Ask-list line:** "Please send a one-page note on which AI models and vendors the product uses, what data any model was trained or tuned on and your rights to it, how customer and call data is used and kept, and the agreement with each AI vendor."

## In the Hollis Voice room

- **Not in the room.** None of the eight document types is among the 17 files. No file name mentions privacy, security, a model card, a policy, SOC or a data processing agreement ([room_facts_people.out.txt](raw/ai-and-data-governance-documents/room_facts_people.out.txt)). This is not a planted flag. It is a gap the room leaves.
- **The product is an AI phone agent**, so the items matter here.
- **Third-party vendors are visible in the expense ledger.** "Halcyon Inference API" (category `model_inference`, booked under R&D) has 21 lines totalling $110,564.84. "Marsh Speech Licensing" (category `third_party_licences`, booked in cost of revenue) has 21 lines totalling $77,685.71. No agreement with either vendor is in the room.
- **It links to a planted flag.** PF6 says the deck and model show an 80 percent gross margin while the true figure, with hosting, inference, telephony, licences and support in cost of revenue, is 58.1 percent (`answer_key.json`). The inference vendor is part of that gap.
- **One contract has a data clause.** The Cedar & Pine order form says "The Customer owns its call recordings and appointment data. The Provider uses them only to run the service." The Marlow pilot agreement and the Brookline Row order form have no data clause (from the script).
- **The hiring plan hints at security.** It plans a Security Engineer (H11, start 2027-03-01) and two Machine Learning Engineers (H03 and H17).
- **A possible regulatory question, not a finding.** The product page lists vaccine reminders and text confirmations to pet owners. If any reminder is a voice call, the FCC ruling on AI voices applies, and the operator should ask.
- **What the ask list would hold:** the Halcyon and Marsh agreements, what data the voice agent is trained or tuned on, how call recordings are kept and deleted, and how callers learn they are speaking to an AI.

## Sources

Each page is saved in [raw/ai-and-data-governance-documents/](raw/ai-and-data-governance-documents/). Vendor and secondary views are marked.

- [DocSend, the startup fundraising due diligence checklist](https://www.docsend.com/blog/due-diligence-checklist/) | [saved](raw/ai-and-data-governance-documents/docsend_com_blog_due_diligence_checklist.txt) (read through a browser by an earlier session; the page blocks automated fetches)
- [Willkie, optimizing AI investments](https://www.willkie.com/publications/2025/09/optimizing-ai-investments-protecting-value-and-managing-risk-through-expert-diligence) (law firm, PDF) | [saved text](raw/ai-and-data-governance-documents/willkie_com_publications_2025_09_optimizing_ai_investments_protecting_value_and_managing_risk_throug.txt) and [saved PDF](raw/ai-and-data-governance-documents/willkie_optimizing_ai_investments.pdf)
- [Katten, AI deals call for a tailored approach](https://katten.com/ai-deals-call-for-tailored-approach-to-address-hidden-risks) (law firm, about company sales) | [saved](raw/ai-and-data-governance-documents/katten_com_ai_deals_call_for_tailored_approach_to_address_hidden_risks.txt)
- [Startups Magazine, the new due diligence](https://startupsmagazine.co.uk/the-new-due-diligence-why-vcs-are-walking-away-from-ai-startups-with-hidden-legal-risk) | [saved](raw/ai-and-data-governance-documents/startupsmagazine_co_uk_the_new_due_diligence_why_vcs_are_walking_away_from_ai_startups_with_hidden_l.txt)
- [Peony, AI due diligence checklist (PDF)](https://www.peony.ink/downloads/ai-due-diligence-checklist.pdf) (vendor) | [saved text](raw/ai-and-data-governance-documents/peony_ink_downloads_ai_due_diligence_checklist_pdf.txt) and [saved PDF](raw/ai-and-data-governance-documents/peony_ink_downloads_ai_due_diligence_checklist.pdf)
- [AI Business, AI startup due diligence in 2026](https://aibusiness.vc/vc/ai-startup-due-diligence-checklist-2026) (vendor) | [saved](raw/ai-and-data-governance-documents/aibusiness_vc_vc_ai_startup_due_diligence_checklist_2026.txt)
- [The Innovation Attorney, what AI startups should document before a funding round](https://theinnovationattorney.substack.com/p/what-ai-startups-should-document) | [saved](raw/ai-and-data-governance-documents/theinnovationattorney_substack_com_p_what_ai_startups_should_document.txt)
- [Pearl Cohen, Bartz v. Anthropic final approval](https://pearlcohen.com/federal-court-approves-1-5-billion-anthropic-copyright-settlement-largest-in-history) (law firm) | [saved](raw/ai-and-data-governance-documents/pearlcohen_com_federal_court_approves_1_5_billion_anthropic_copyright_settlement_largest_in_history.txt)
- [Jurist, judge approves $1.5 billion settlement](https://www.jurist.org/news/2026/07/judge-approves-record-1-5-billion-settlement-involving-anthropic/) | [saved](raw/ai-and-data-governance-documents/jurist_org_news_2026_07_judge_approves_record_1_5_billion_settlement_involving_anthropic.txt)
- [Lathrop GPM, AI and algorithmic disgorgement](https://www.lathropgpm.com/insights/artificial-intelligence-and-algorithmic-disgorgement/) (law firm) | [saved](raw/ai-and-data-governance-documents/lathropgpm_com_insights_artificial_intelligence_and_algorithmic_disgorgement.txt)
- [Gibson Dunn, EU AI Act omnibus agreement](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/) (law firm, May 2026) | [saved](raw/ai-and-data-governance-documents/gibsondunn_com_eu_ai_act_omnibus_agreement_postponed_high_risk_deadlines_and_other_key_changes.txt)
- [Orrick, did the FCC really ban AI-generated voice calls](https://orrick.com/Insights/2024/02/Did-the-FCC-Really-Ban-AI-Generated-Voice-Calls-No-But-Restrictions-Apply) (law firm) | [saved](raw/ai-and-data-governance-documents/orrick_com_Insights_2024_02_Did_the_FCC_Really_Ban_AI_Generated_Voice_Calls_No_But_Restrictions_Appl.txt)
- [Cooley, FCC: AI-generated robocalls illegal under the TCPA](https://cooley.com/news/insight/2024/2024-02-15-fcc-ai-generated-robocalls-illegal-under-the-tcpa) (law firm, read not cited) | [saved](raw/ai-and-data-governance-documents/cooley_com_news_insight_2024_2024_02_15_fcc_ai_generated_robocalls_illegal_under_the_tcpa.txt)
- [Global Policy Watch, Ambriz v. Google](https://www.globalpolicywatch.com/2024/07/california-federal-court-dismisses-complaint-accusing-google-of-wiretapping-customer-service-calls/) | [saved](raw/ai-and-data-governance-documents/globalpolicywatch_com_2024_07_california_federal_court_dismisses_complaint_accusing_google_of_wireta.txt)
- [Hustle Fund, angel investing due diligence checklist](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step) | [saved](raw/ai-and-data-governance-documents/hustlefund_vc_post_angel_squad_angel_investing_due_diligence_checklist_step_by_step.txt)
- [Revera Legal, AI startup under investor scrutiny](https://www.revera.legal/?p=8249) (law firm; paraphrased only) | [saved](raw/ai-and-data-governance-documents/revera_legal_p_8249.txt)
- Read but not cited: [Data-Mania](raw/ai-and-data-governance-documents/data_mania_com_blog_ai_due_diligence_checklist.txt), [Pebblous](raw/ai-and-data-governance-documents/blog_pebblous_ai_blog_ai_startup_valuation_regulatory_readiness_en.txt), [Qubit Capital](raw/ai-and-data-governance-documents/qubit_capital_p_50404.txt), [LegalVision](raw/ai-and-data-governance-documents/legalvision_co_uk_corporations_ai_startup_funding.txt) and [Plausity](raw/ai-and-data-governance-documents/plausity_com_en_news_ai_startup_data_room_checklist_vc_due_diligence.txt). All are vendor or advisory pages.

Pages that blocked automated fetching or returned unusable text: the FTC's Everalbum pages (HTTP 404 at the addresses tried), and the Weil memo on algorithm destruction, whose PDF returned unreadable text ([placeholder file](raw/ai-and-data-governance-documents/weil_com_media_mailings_2021_q2_ftc_orders_destruction_of_algorithms_created_from_unlawfully_acquire.txt)). The DocSend page needs a browser.
