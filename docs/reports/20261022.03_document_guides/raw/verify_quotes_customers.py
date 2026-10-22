"""Check every quote and paraphrase in the three customers-group guides, then write quotes_customers.csv.

Run: python3 -I verify_quotes_customers.py   (from anywhere; paths come from this file's location)

For each entry below:
  - a quote must appear, word for word, in the saved page (curly quotes straightened, all white space ignored);
  - a paraphrase must have its support phrase in the saved page;
  - the entry is written to the CSV only if its text also appears in its guide.
Columns of quotes_customers.csv: guide, kind, text, link, saved_file, verified.
"""
import csv
import pathlib
import re

"""Quote and paraphrase registry for the customers group of document guides.

Each entry: id -> dict(guide, kind, text, link, label, folder, file, support)
  guide  : guide slug
  kind   : quote or paraphrase
  text   : the exact words (quote) or our paraphrase
  link   : page URL
  label  : short source name shown in the guide
  folder : raw folder (under raw/) holding the saved page
  file   : prefix of the saved file name in that folder
  support: for a paraphrase, a phrase that must appear in the saved page
"""

CC = "customer-contracts-and-order-forms"
CR = "customer-references-and-letters-of-intent"
MA = "material-agreements-other-than-customer-contracts"

FORTUNE = "https://fortune.com/2025/09/28/how-is-arr-calculated-startups-venture/"
PEONY = "https://www.peony.ink/blog/series-a-data-room"
CRVROOM = "https://www.crv.com/content/what-is-a-data-room"
VISIBLE = "https://visible.vc/blog/what-to-include-in-your-data-room/"
JURO = "https://juro.com/learn/contract-due-diligence"
KOLEY = "https://www.koleyjessen.com/insights/publications/9-contract-issues-that-can-diminish-value-in-pe-portfolio-companies"
CONSILIUM = "https://consilium.law/sparkpoint/startup-fundraising-legal-due-diligence-checklist/"
ACCORD = "https://accordshield.com/blog-diligence-grade-contracts"
LIVMO = "https://livmo.com/blog/saas-contract-length-valuation/"
SAASTR_PILOT = "https://www.saastr.com/what-is-the-typical-conversion-from-paid-pilot-to-annual-contract-in-b2b-saas-2"
HUSTLE_CHECK = "https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step"
KRUZE = "https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/"
BVP = "https://www.bvp.com/atlas/scaling-to-100-million"
LIGHTER = "https://www.lightercapital.com/blog/how-to-calculate-committed-mrr-cmrr"
DOCSEND_CHECK = "https://www.docsend.com/blog/due-diligence-checklist/"
DOCSEND_4 = "https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/"
COOLEY = "https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/"
HUA = "https://thedataroom.substack.com/p/how-a-vc-does-due-diligence-on-your-company"
PASCAL = "https://pascalsnotes.substack.com/p/how-to-go-about-customer-reference"
BETAKIT = "https://betakit.com/ask-an-investor-who-are-the-best-references-to-provide-to-vcs/"
VCBEAST = "https://vcbeast.com/guides/how-to-conduct-customer-reference-calls"
FIRSTROUND = "https://review.firstround.com/heres-what-you-can-really-expect-when-pitching-your-seed-stage-startup-at-a-vc-partner-meeting/"
NBER = "https://www.nber.org/system/files/working_papers/w22587/w22587.pdf"
CRV_TRACTION = "https://www.crv.com/content/startup-traction"
HUSTLE_LOI = "https://hustlefund.vc/blog-posts-founders/how-do-we-best-position-our-seemingly-slow-growth-to-investors-in-order-to-raise-our-seed"
GUST = "https://gust.com/blog/traction-is-validation-you-dont-control/"
COMMONPAPER = "https://commonpaper.com/blog/what-is-an-loi/"
REGISTER = "https://www.theregister.co.uk/2013/02/04/gartner_analyst_says_some_reference_customers_may_not_exist/"
FORM = "https://formventures.substack.com/p/team-talks-ii-founder-reference-calls"
LEARNINGLOOP = "https://learningloop.io/plays/letter-of-intent"
FOUNDERCOLLECTIVE = "https://foundercollective.com/blog/diligence-101-for-seed-stage-startups"
FOLEY = "https://foleyhoag.com/news-and-insights/publications/alerts-and-updates/2024/august/10-things-to-know-about-venture-debt/"
YC_DEBT = "https://www.ycombinator.com/blog/venture-debt-101-basics-and-approach"
ACQSTARS_UCC = "https://acquisitionstars.com/blog/ucc-lien-search-buying-a-business"
INCORP = "https://www.incorp.com/resources/knowledge-base/what-is-a-ucc-search"
TAFT = "https://www.taftlaw.com/news-events/law-bulletins/even-the-smallest-commercial-lease-is-a-big-deal-here-are-seven-key-issues-prospective-tenants-need-to-consider-and-address/"
VOUCH = "https://www.vouch.us/blog/when-does-my-startup-need-insurance"
REDRESS = "https://redresscompliance.com/aws-edp-shortfall-risk-management"
LATHROP = "https://www.lathropgpm.com/insights/understanding-and-complying-with-open-source-software-licenses-why-when-and-how/"
FOSSA = "https://fossa.com/blog/copyleft-licenses-venture-capital-connection/"
REVISION = "https://revisionlegal.com/corporate/revision-legal/ip-assignment-mistakes-startup-acquisition-due-diligence/"
VERDANTIX = "https://www.verdantix.com/insights/blog/enterprise-software-vendors-should-heed-warning-from-anthropic-s-usage-limit-reduction"
KLEHR = "https://klehr.com/publications/startup-evolution-a-year-long-journey-through-a-founders-toolkit-due-diligence-ready-building-a-data-room-that-wins-investor-confidence/"
MARS = "https://learn.marsdd.com/article/data-room-basics-for-startups-stage-2-data-for-investor-due-diligence/"
PROMISE = "https://blog.promise.legal/startup-central/open-source-license-compliance-for-startups/"
COGENCY = "https://www.cogencyglobal.com/blog/ucc-termination-statements-part-2/"


def Q(guide, text, link, label, folder, file, kind="quote", support=None):
    return dict(guide=guide, kind=kind, text=text, link=link, label=label, folder=folder, file=file, support=support)


R = {}

# ---------------------------------------------------------------- customer contracts
g = "customer-contracts-and-order-forms"
R["cc_fortune_count"] = Q(g, "Founders are counting pilots, one-time deals, or unactivated contracts as recurring revenue, six VCs told Fortune", FORTUNE, "Fortune, Sep 2025", CC, "fortune_com")
R["cc_fortune_optout"] = Q(g, "contracts frequently have provisions that let customers opt out at any time for any reason", FORTUNE, "Fortune, Sep 2025", CC, "fortune_com")
R["cc_fortune_car"] = Q(g, "there was clear separation between ARR, CAR (signed contract value before activation), and recognized revenue (actual revenue booked)", FORTUNE, "Fortune, Sep 2025", CC, "fortune_com")
R["cc_fortune_kill"] = Q(g, "An early-stage VC told Fortune that some founders sign contracts with kill provisions, claim the booked ARR, and give the customer an out: a million-dollar-a-year contract that the customer can cancel after three months for no reason.", FORTUNE, "Fortune, Sep 2025, unnamed VC", CC, "fortune_com", "paraphrase", "it says in three months, you can cancel for no reason")
R["cc_fortune_pilot"] = Q(g, "A top-firm VC told Fortune about a defense-tech founder who claimed $325,000 of ARR from a contract that turned out to be a two-week pilot, backed by 'good authority' that the customer would keep paying; the VC wanted a signed piece of paper.", FORTUNE, "Fortune, Sep 2025, unnamed VC", CC, "fortune_com", "paraphrase", "two-week pilot")
R["cc_peony_lead"] = Q(g, "At Series A, the lead wants the signed contract and may call the customer.", PEONY, "Peony, a data room vendor", CC, "peony_ink_blog_series_a")
R["cc_peony_top10"] = Q(g, "Top ~10 customer contracts and any material contract above ~$20,000", PEONY, "Peony, a data room vendor", CC, "peony_ink_blog_series_a")
R["cc_kruze_top10"] = Q(g, "Top 10 client invoices and contracts (only matters for b2b companies)", KRUZE, "Kruze Consulting", CC, "kruzeconsulting_com_what_are")
R["cc_crv_reconcile"] = Q(g, "Your annual recurring revenue (ARR) in the deck should reconcile to the underlying billing, contract and revenue schedules.", CRVROOM, "CRV", CC, "crv_com_content_what_is")
R["cc_consilium_deck"] = Q(g, "A data room does not cure a missing board approval, an unsigned IP assignment, or a contract that says something different from your deck.", CONSILIUM, "Consilium Law, Aug 2026", CC, "consilium_law")
R["cc_consilium_finding"] = Q(g, "Where they disagree, the disagreement is the finding.", CONSILIUM, "Consilium Law, Aug 2026", CC, "consilium_law")
R["cc_consilium_restrict"] = Q(g, "Restrictions that could constrain the financing, operations, growth, or a later transaction: exclusivity, most-favored-customer pricing, minimum commitments, renewal terms.", CONSILIUM, "Consilium Law, Aug 2026", CC, "consilium_law")
R["cc_juro_hasty"] = Q(g, "Many early-stage businesses reach Series A with contracts that were put together quickly, without standardized contract templates or proper execution.", JURO, "Juro, a contract software vendor", CC, "juro_com")
R["cc_juro_renew"] = Q(g, "Auto-renewal contracts can be a positive signal, supporting revenue predictability, or a concern if they've created obligations the business isn't actively tracking.", JURO, "Juro, a contract software vendor", CC, "juro_com")
R["cc_juro_gaps"] = Q(g, "Gaps and inconsistencies don't necessarily indicate wrongdoing, but they do suggest a business that hasn't been rigorous about managing its obligations, which is itself a risk factor investors take seriously.", JURO, "Juro, a contract software vendor", CC, "juro_com")
R["cc_juro_note"] = Q(g, "If there are contracts with non-standard terms, known gaps, or issues you're aware of, address them in a covering note rather than waiting for them to be discovered.", JURO, "Juro, a contract software vendor", CC, "juro_com")
R["cc_juro_cc"] = Q(g, "Some contracts give the counterparty rights to terminate, renegotiate, or require consent in the event of a change of control.", JURO, "Juro, a contract software vendor", CC, "juro_com")
R["cc_koley_tfc"] = Q(g, "Contracts that contain a termination for convenience right for the other party will be discounted by buyers, potentially materially reducing enterprise value at exit.", KOLEY, "Koley Jessen, Jan 2026", CC, "koleyjessen_com_insights")
R["cc_koley_mfn"] = Q(g, "MFN clauses promise a customer they will always receive the lowest price offered to anyone else.", KOLEY, "Koley Jessen, Jan 2026", CC, "koleyjessen_com_insights")
R["cc_accord_cond"] = Q(g, "To a buyer, that ARR is no longer clean recurring revenue. It is conditional revenue.", ACCORD, "Accord & Shield Legal, Jul 2026", CC, "accordshield")
R["cc_livmo_walk"] = Q(g, "A buyer does not just ask how much ARR you have. They ask how much of that ARR can walk away in the next 30 days.", LIVMO, "Livmo, an advisory firm", CC, "livmo_com")
R["cc_lemkin_conv"] = Q(g, "In the companies I work closely with, roughly, the conversions vary fairly widely from about 60% to over 90%.", SAASTR_PILOT, "Jason Lemkin, SaaStr", CC, "saastr_com_what_is")
R["cc_lemkin_unpaid"] = Q(g, "unpaid pilots are a waste of time … 95% of the time", SAASTR_PILOT, "Jason Lemkin, SaaStr", CC, "saastr_com_what_is")
R["cc_lemkin_optout"] = Q(g, "allowing new customers to cancel the contract after 60 days for any or no reason if they aren’t happy", SAASTR_PILOT, "Jason Lemkin, SaaStr", CC, "saastr_com_what_is")
R["cc_hustle_separate"] = Q(g, "Separate contracted revenue, recognized revenue, pipeline, pilots, letters of intent, and verbal interest.", HUSTLE_CHECK, "Hustle Fund, angel checklist", CC, "hustlefund_vc_post_angel")
R["cc_bvp_arr"] = Q(g, "ARR gives full credit for the annualized recurring contract and nets out non-recurring revenue", BVP, "Bessemer Venture Partners", CC, "bvp_com")
R["cc_lighter_cmrr"] = Q(g, "Lighter Capital, a revenue-based lender, defines committed MRR as current MRR plus signed contracts going into production, minus revenue likely to churn.", LIGHTER, "Lighter Capital, a lender", CC, "lightercapital_com_blog_how", "paraphrase", "signed contracts going into production")
R["cc_visible_row"] = Q(g, "Visible's stage table marks the row 'Major customer, vendor, partner contracts' as not needed at pre-seed, lighter at seed, and expected at Series A and growth.", VISIBLE, "Visible, an investor-update vendor", CC, "visible_vc_blog", "paraphrase", "Major customer, vendor, partner contracts")
R["cc_visible_secondtier"] = Q(g, "The most restricted folders (executed customer contracts, executive compensation, pending strategic activity) open only to the lead investor as the conversation matures.", VISIBLE, "Visible, an investor-update vendor", CC, "visible_vc_blog", "paraphrase", "executed customer contracts")
R["cc_peony_tiers"] = Q(g, "Peony says customer contracts belong in the second tier, shared after a signed term sheet, so a lead who has not committed does not see them.", PEONY, "Peony, a data room vendor", CC, "peony_ink_blog_series_a", "paraphrase", "over-exposes your customer contracts and detailed financials to a lead who hasn't committed")
R["cc_juro_seriesb"] = Q(g, "Juro says the revenue-quality questions (are contracts genuinely recurring, on what terms, with what termination rights) matter most from Series B on, and that at Series A investors mostly check that the agreements exist and are signed.", JURO, "Juro, a contract software vendor", CC, "juro_com", "paraphrase", "Investors will want to understand revenue quality")
R["cc_juro_sideletters"] = Q(g, "Juro lists side agreements, verbal commitments and informal arrangements as exposure investors look for at Series A.", JURO, "Juro, a contract software vendor", CC, "juro_com", "paraphrase", "side agreements, verbal commitments")
R["cc_livmo_annual"] = Q(g, "Livmo reports that ChartMogul data on more than 2,500 SaaS companies shows annual plans drive stronger retention, and that annual prepaid customers sit in the strongest risk band a buyer uses.", LIVMO, "Livmo, an advisory firm, second-hand ChartMogul figures", CC, "livmo_com", "paraphrase", "Annual prepaid customers sit in the strongest band")

# ---------------------------------------------------------------- references and LOIs
g = "customer-references-and-letters-of-intent"
R["cr_docsend4_list"] = Q(g, "a good strategy is to have your lead investor speak to these customer references, write up notes, and then share those in the data room", DOCSEND_4, "Gale Wilkinson, Vitalize Venture Capital, on DocSend", CR, "docsend_com_blog_4_types")
R["cr_docsend4_who"] = Q(g, "A seed investor's guest post on DocSend says the reference list names key members of the management team, one or two customers, one or two current investors (if any), advisors, and other people who know the founder well.", DOCSEND_4, "Gale Wilkinson, Vitalize Venture Capital, on DocSend", CR, "docsend_com_blog_4_types", "paraphrase", "1-2 customers")
R["cr_docsend_check"] = Q(g, "DocSend's checklist lists 'References' as its first group and describes it only as 'Customer and personal references'.", DOCSEND_CHECK, "DocSend, due diligence checklist", CR, "docsend_com_blog_due", "paraphrase", "Customer and personal references")
R["cr_pascal_ask"] = Q(g, "most VCs (or at least potential leads) will ask to speak to your customers (both existing as well as potential) at some point during a diligence process", PASCAL, "Pascal Unger, seed investor", CR, "pascalsnotes")
R["cr_pascal_logos"] = Q(g, "I’d put less emphasis on logos and more on true believers in your startup", PASCAL, "Pascal Unger, seed investor", CR, "pascalsnotes")
R["cr_pascal_23"] = Q(g, "2-3 customer introductions should be enough per VC firm", PASCAL, "Pascal Unger, seed investor", CR, "pascalsnotes")
R["cr_pascal_signal"] = Q(g, "Pascal Unger notes a signaling risk for early founders: customers do not want to work with a startup that may go out of business because its fundraise failed, so too many investor calls can hurt.", PASCAL, "Pascal Unger, seed investor", CR, "pascalsnotes", "paraphrase", "signaling risk")
R["cr_betakit_owner"] = Q(g, "The person who owns the relationship is much more important than seniority or prestige.", BETAKIT, "Sarah Marion, BetaKit Ask an Investor", CR, "betakit")
R["cr_betakit_pattern"] = Q(g, "VCs are more focused on patterns of negative feedback emerging, rather than one-off comments.", BETAKIT, "Sarah Marion, BetaKit Ask an Investor", CR, "betakit")
R["cr_betakit_love"] = Q(g, "If they don’t love you or your product, that’s a red flag!", BETAKIT, "Sarah Marion, BetaKit Ask an Investor", CR, "betakit")
R["cr_betakit_late"] = Q(g, "You should expect these to occur late in the process – sometimes post-term sheet.", BETAKIT, "Sarah Marion, BetaKit Ask an Investor", CR, "betakit")
R["cr_betakit_offlist"] = Q(g, "Sarah Marion warns founders that investors also call people the founder did not list, such as portfolio companies that have been the company's customers or partners.", BETAKIT, "Sarah Marion, BetaKit Ask an Investor", CR, "betakit", "paraphrase", "Off-list")
R["cr_vcbeast_mix"] = Q(g, "Tell them you need a mix: power users, occasional users, and at least 2 churned customers or prospects who didn't close.", VCBEAST, "VC Beast guide, no named author", CR, "vcbeast")
R["cr_vcbeast_flinch"] = Q(g, "A confident founder who believes in their product will give you churned customers without flinching.", VCBEAST, "VC Beast guide, no named author", CR, "vcbeast")
R["cr_vcbeast_coach"] = Q(g, "When you hear three references all use the same language (“game-changer,” “saves us X hours per week,” “the team is incredible”), that's a coaching signal.", VCBEAST, "VC Beast guide, no named author", CR, "vcbeast")
R["cr_vcbeast_defensive"] = Q(g, "A VC Beast guide says a confident founder gives up churned customers easily, while a defensive founder pushes back, offers excuses, or conveniently has no contacts left, and the investor should note it.", VCBEAST, "VC Beast guide, no named author", CR, "vcbeast", "paraphrase", "A defensive founder will push back")
R["cr_vcbeast_counts"] = Q(g, "For a seed deal: 5-7 calls minimum.", VCBEAST, "VC Beast guide, no named author", CR, "vcbeast")
R["cr_vcbeast_counts_a"] = Q(g, "For a Series A or B: 10-15 calls.", VCBEAST, "VC Beast guide, no named author", CR, "vcbeast")
R["cr_vcbeast_own"] = Q(g, "The references a founder doesn't give you are often more valuable than the ones they do.", VCBEAST, "VC Beast guide, no named author", CR, "vcbeast")
R["cr_hua_alone"] = Q(g, "what do people say when they think it can’t get back to the founder?", HUA, "Jonathan Hua, The Data Room", CR, "web_thedataroom")
R["cr_hua_pitfall"] = Q(g, "only offering references who are direct beneficiaries of your success, an investor, a close friend, a subordinate", HUA, "Jonathan Hua, The Data Room", CR, "web_thedataroom")
R["cr_hua_script"] = Q(g, "References that sound like they’re reading from a script you gave them.", HUA, "Jonathan Hua, The Data Room", CR, "web_thedataroom")
R["cr_hua_same"] = Q(g, "A reference who describes you the same way you describe yourself.", HUA, "Jonathan Hua, The Data Room", CR, "web_thedataroom")
R["cr_hua_missing"] = Q(g, "What’s still missing after multiple requests is rarely benign.", HUA, "Jonathan Hua, The Data Room", CR, "web_thedataroom")
R["cr_hua_weakest"] = Q(g, "Naming your own weakest number before I find it.", HUA, "Jonathan Hua, The Data Room", CR, "web_thedataroom")
R["cr_hua_flip"] = Q(g, "I’ve had calls flip my recommendation mid-conversation", HUA, "Jonathan Hua, The Data Room", CR, "web_thedataroom")
R["cr_firstround_5_15"] = Q(g, "At First Round, we typically have anywhere from 5-15 diligence conversations", FIRSTROUND, "First Round Review", CR, "review_firstround")
R["cr_firstround_nocust"] = Q(g, "assuming there are even customers to speak with", FIRSTROUND, "First Round Review", CR, "review_firstround")
R["cr_nber_refs"] = Q(g, "Late-stage firms also call more references (13 on average) than early-stage firms (8).", NBER, "Gompers, Gornall, Kaplan and Strebulaev, NBER", CR, "web_nber")
R["cr_crv_contra"] = Q(g, "One customer reference that contradicts a retention claim can undo confidence late in diligence.", CRVROOM, "CRV", CR, "crv_com_content_what_is")
R["cr_crv_formal"] = Q(g, "customer reference calls turn formal", CRVROOM, "CRV", CR, "crv_com_content_what_is")
R["cr_peony_calls"] = Q(g, "Peony places customer and reference calls in weeks 2 to 6 of a Series A process, with the lead calling top customers to verify retention and value.", PEONY, "Peony, a data room vendor", CR, "peony_ink_blog_series_a", "paraphrase", "The lead calls your top customers to verify retention and value")
R["cr_visible_logos"] = Q(g, "Logos without context are read as filler.", VISIBLE, "Visible, an investor-update vendor", CR, "visible_vc_blog")
R["cr_visible_case"] = Q(g, "One detailed case study with a named customer and a quantified outcome is worth more than ten logos on a slide.", VISIBLE, "Visible, an investor-update vendor", CR, "visible_vc_blog")
R["cr_visible_row"] = Q(g, "Visible's stage table marks 'Customer reference letters / LOIs' as not needed at pre-seed, lighter at seed, and expected at Series A and growth.", VISIBLE, "Visible, an investor-update vendor", CR, "visible_vc_blog", "paraphrase", "Customer reference letters / LOIs")
R["cr_crvt_loi"] = Q(g, "Letters of intent (LOIs) with dollar figures attached, design partners testing weekly builds, pilot commitments and pre-orders all count.", CRV_TRACTION, "CRV, on startup traction", CR, "crv_com_content_startup")
R["cr_crvt_waitlist"] = Q(g, "A waitlist you built from one tweet shows little.", CRV_TRACTION, "CRV, on startup traction", CR, "crv_com_content_startup")
R["cr_hustle_loi"] = Q(g, "having letters of intent gives investors strong signals that you’ll be able to move the needle on your sales metrics soon", HUSTLE_LOI, "Hustle Fund, Apr 2026", CR, "hustlefund_vc_blog")
R["cr_hustle_notbinding"] = Q(g, "the offer is not technically binding", HUSTLE_LOI, "Hustle Fund, Apr 2026", CR, "hustlefund_vc_blog")
R["cr_gust_backed"] = Q(g, "LOIs usually need to be backed by signed agreements to be compelling to investors", GUST, "Gust", CR, "gust_com")
R["cr_cp_weight"] = Q(g, "The prospect has no legal obligation to move forward after the LOI, so investors don’t give it as much weight as a signed sales contract.", COMMONPAPER, "Jake Stein, Common Paper", CR, "commonpaper")
R["cr_cp_usage"] = Q(g, "Startups most commonly use LOIs to secure non-binding commitments from prospective customers, often as proof of market validation to share with potential investors.", COMMONPAPER, "Jake Stein, Common Paper", CR, "commonpaper")
R["cr_cp_dpa"] = Q(g, "The most notable difference from an LOI is that a Design Partner Agreement is binding.", COMMONPAPER, "Jake Stein, Common Paper", CR, "commonpaper")
R["cr_ll_verbal"] = Q(g, "customers may verbally endorse your idea while never intending to buy it", LEARNINGLOOP, "Learning Loop, a validation toolkit", CR, "learningloop")
R["cr_hustlecheck"] = Q(g, "Separate contracted revenue, recognized revenue, pipeline, pilots, letters of intent, and verbal interest.", HUSTLE_CHECK, "Hustle Fund, angel checklist", CR, "hustlefund_vc_post_angel")
R["cr_register"] = Q(g, "A Gartner analyst reported that some vendor-supplied reference customers had not set the tool up in production, some turned out to be resellers, and some wins could not be verified to exist.", REGISTER, "The Register, 2013, second-hand report from a software buyer, not a VC", CR, "theregister", "paraphrase", "did not have the tool set up in production")
R["cr_form_few"] = Q(g, "Most VCs do reference calls. From my conversations, few feel like they do them very well.", FORM, "Form Ventures", CR, "formventures")
R["cr_form_end"] = Q(g, "Most funds I spoke with only do reference calls at the end of the process, as part of confirmatory diligence.", FORM, "Form Ventures", CR, "formventures")
R["cr_visible_lois"] = Q(g, "If you have customer reference letters, partnership agreements, or LOIs, add them here to validate early momentum.", VISIBLE, "Visible, an investor-update vendor", CR, "visible_vc_blog")
R["cr_foundercollective"] = Q(g, "Founder Collective suggests inviting all the investors to meet key clients together, which spares the clients a half-dozen reference calls.", FOUNDERCOLLECTIVE, "Founder Collective", CR, "web_foundercollective", "paraphrase", "saves your clients from a half-dozen reference calls")

# ---------------------------------------------------------------- material agreements
g = "material-agreements-other-than-customer-contracts"
R["ma_docsend_25k"] = Q(g, "Any agreements or understandings between your company and others with obligations exceeding $25,000", DOCSEND_CHECK, "DocSend, due diligence checklist", MA, "docsend_com_blog_due")
R["ma_docsend_items"] = Q(g, "Property leases (real estate and personal property); Loans, mortgages, liens, or encumbrances against your company; Loans provided by your company; Insurance policies", DOCSEND_CHECK, "DocSend, due diligence checklist", MA, "docsend_com_blog_due")
R["ma_docsend_ip"] = Q(g, "Licenses of any company intellectual property to third parties; Licenses of third-party intellectual property by your company", DOCSEND_CHECK, "DocSend, due diligence checklist", MA, "docsend_com_blog_due")
R["ma_docsend_consult"] = Q(g, "Consulting agreements; Agreements with officers and directors", DOCSEND_CHECK, "DocSend, due diligence checklist", MA, "docsend_com_blog_due")
R["ma_docsend_ai"] = Q(g, "Third-party AI services: Agreements with AI service providers (OpenAI, Anthropic, Google, etc.) and associated terms", DOCSEND_CHECK, "DocSend, due diligence checklist", MA, "docsend_com_blog_due")
R["ma_docsend_frame"] = Q(g, "DocSend frames its whole checklist as what investors ask for after a term sheet is signed.", DOCSEND_CHECK, "DocSend, due diligence checklist, page note", MA, "docsend_com_blog_due", "paraphrase", "after a term sheet is signed")
R["ma_cooley_debt"] = Q(g, "All debt instruments and credit agreements entered into by the Company, including lease financing, which are currently in effect.", COOLEY, "Cooley GO, sample request list", MA, "cooley_vc_dd_request_list.txt")
R["ma_cooley_guar"] = Q(g, "Any guarantees of third party obligations.", COOLEY, "Cooley GO, sample request list", MA, "cooley_vc_dd_request_list.txt")
R["ma_cooley_consent"] = Q(g, "Agreements requiring consents or approvals in connection with the financing.", COOLEY, "Cooley GO, sample request list", MA, "cooley_vc_dd_request_list.txt")
R["ma_cooley_related"] = Q(g, "Any agreements, understandings or proposed transactions between the Company and any of its employees, officers, directors, affiliates, or any affiliate thereof", COOLEY, "Cooley GO, sample request list", MA, "cooley_vc_dd_request_list.txt")
R["ma_cooley_compete"] = Q(g, "Brief description of any contract restricting the ability of the Company to compete in any line of business with any person or entity", COOLEY, "Cooley GO, sample request list", MA, "cooley_vc_dd_request_list.txt")
R["ma_cooley_lease"] = Q(g, "Real property leases, including any amendments and all exhibits to such documents.", COOLEY, "Cooley GO, sample request list", MA, "cooley_vc_dd_request_list.txt")
R["ma_cooley_consult"] = Q(g, "Consulting contracts.", COOLEY, "Cooley GO, sample request list", MA, "cooley_vc_dd_request_list.txt")
R["ma_peony_20k"] = Q(g, "Top ~10 customer contracts and any material contract above ~$20,000", PEONY, "Peony, a data room vendor", MA, "peony_ink_blog_series_a")
R["ma_kruze_vendor"] = Q(g, "Material contracts with vendors/suppliers", KRUZE, "Kruze Consulting", MA, "kruzeconsulting_com_what_are")
R["ma_mars_5k"] = Q(g, "Typically, contracts exceeding a specific financial value (normally $5,000) or with key partners need to be shared with an investor.", MARS, "MaRS Discovery District", MA, "learn_marsdd")
R["ma_mars_insure"] = Q(g, "Insurance policies and coverage details, and proof of payments", MARS, "MaRS Discovery District", MA, "learn_marsdd")
R["ma_visible_row"] = Q(g, "Visible's stage table marks the row 'Major customer, vendor, partner contracts' as not needed at pre-seed, lighter at seed, and expected at Series A and growth.", VISIBLE, "Visible, an investor-update vendor", MA, "visible_vc_blog", "paraphrase", "Major customer, vendor, partner contracts")
R["ma_klehr_mix"] = Q(g, "Mixing executed and draft contracts.", KLEHR, "Klehr Harrison Harvey Branzburg", MA, "klehr")
R["ma_juro_log"] = Q(g, "Create a master log that records, for each contract, the counterparty, the contract type, the effective date , the expiry or renewal date, whether it has been properly executed, and any material or unusual terms.", JURO, "Juro, a contract software vendor", MA, "juro_com")
R["ma_juro_supplier"] = Q(g, "Investors want to understand whether the business has supplier dependencies that create concentration risk", JURO, "Juro, a contract software vendor", MA, "juro_com")
R["ma_juro_unsigned"] = Q(g, "A contract that was never properly executed isn't enforceable in the way the parties might assume.", JURO, "Juro, a contract software vendor", MA, "juro_com")
R["ma_foley_collat"] = Q(g, "Venture lenders typically receive a first-priority (senior) security interest in all assets of the company.", FOLEY, "Foley Hoag, Aug 2024", MA, "foleyhoag")
R["ma_foley_ip"] = Q(g, "It is common for intellectual property to be excluded from the collateral grant, but remain subject to a negative pledge", FOLEY, "Foley Hoag, Aug 2024", MA, "foleyhoag")
R["ma_foley_cov"] = Q(g, "Venture debt agreements contain tight restrictions on a company’s ability to engage in certain activities without lender consent", FOLEY, "Foley Hoag, Aug 2024", MA, "foleyhoag")
R["ma_foley_mac"] = Q(g, "an event of default that is either triggered by a material adverse change (MAC) with respect to the business or a lack of investor support", FOLEY, "Foley Hoag, Aug 2024", MA, "foleyhoag")
R["ma_foley_guar"] = Q(g, "the venture lender may request a personal guaranty from the founders", FOLEY, "Foley Hoag, Aug 2024", MA, "foleyhoag")
R["ma_foley_sub"] = Q(g, "venture lenders typically require that all existing debt of the company, including convertible notes, is subordinated to the new debt facility", FOLEY, "Foley Hoag, Aug 2024", MA, "foleyhoag")
R["ma_foley_consent"] = Q(g, "Consent of the board of directors will be required and often shareholder consent is also needed", FOLEY, "Foley Hoag, Aug 2024", MA, "foleyhoag")
R["ma_foley_stage"] = Q(g, "Most institutional venture lenders will expect at least one preferred round of equity financing before being willing to provide a venture debt facility.", FOLEY, "Foley Hoag, Aug 2024", MA, "foleyhoag")
R["ma_yc_abandon"] = Q(g, "A clause that allows the lender to demand repayment if a company’s investor doesn’t invest in the company’s future round.", YC_DEBT, "Jon Levy, Y Combinator", MA, "ycombinator")
R["ma_yc_ip"] = Q(g, "Sometimes lenders ask for a first-priority security interest on a company’s IP", YC_DEBT, "Jon Levy, Y Combinator", MA, "ycombinator")
R["ma_yc_one"] = Q(g, "it is common for founders to speak to only one venture debt investor", YC_DEBT, "Jon Levy, Y Combinator", MA, "ycombinator")
R["ma_yc_repaid"] = Q(g, "venture debt investors expect to get repaid on every investment", YC_DEBT, "Jon Levy, Y Combinator", MA, "ycombinator")
R["ma_ucc_stale"] = Q(g, "lenders do not always file UCC-3 terminations promptly, or at all", ACQSTARS_UCC, "Acquisition Stars (advisory blog)", MA, "acquisitionstars_com_blog_ucc")
R["ma_ucc_same"] = Q(g, "A UCC-1 filing that appears active can represent paid-off debt with a missing termination statement, or it can represent a live obligation.", ACQSTARS_UCC, "Acquisition Stars (advisory blog)", MA, "acquisitionstars_com_blog_ucc")
R["ma_ucc_five"] = Q(g, "These filings remain effective for five years from filing dates unless terminated earlier or continued before expiration.", INCORP, "InCorp, a registered-agent service", MA, "incorp")
R["ma_taft_guar"] = Q(g, "Especially for start-ups or new businesses lacking a strong credit history and steady revenues, commercial landlords will likely ask the owners to sign personal guarantees of their company’s lease obligations.", TAFT, "Taft Law, Nov 2023", MA, "taftlaw")
R["ma_taft_assign"] = Q(g, "Commercial leases almost always require the landlord to give prior approval beforehand.", TAFT, "Taft Law, Nov 2023", MA, "taftlaw")
R["ma_vouch_do"] = Q(g, "Business insurance before a funding round, specifically Directors & Officers (D&O) Insurance, is typically required by investors as a condition of close.", VOUCH, "Vouch, an insurance broker, vendor view", MA, "vouch_us_blog_when")
R["ma_vouch_cyber"] = Q(g, "Tech and SaaS contracts often also require Cyber Insurance and Tech E&O Insurance.", VOUCH, "Vouch, an insurance broker, vendor view", MA, "vouch_us_blog_when")
R["ma_vouch_close"] = Q(g, "It's not a policy to scramble for after a term sheet.", VOUCH, "Vouch, an insurance broker, vendor view", MA, "vouch_us_blog_when")
R["ma_redress"] = Q(g, "An AWS EDP shortfall is the unused part of your annual commitment, invoiced in full with no discount.", REDRESS, "Redress Compliance, a licensing advisory, vendor view", MA, "redresscompliance")
R["ma_lathrop_fin"] = Q(g, "open source license compliance comes up relatively routinely in connection with financing (debt or equity funding) and M&A transactions", LATHROP, "Lathrop GPM, 2021", MA, "lathropgpm")
R["ma_lathrop_rep"] = Q(g, "requirements to provide representations and warranties on current and past compliance in financings and M&A agreements are typical", LATHROP, "Lathrop GPM, 2021", MA, "lathropgpm")
R["ma_fossa_nvca"] = Q(g, "in any manner that would materially restrict the ability of the Company to protect its proprietary interests", FOSSA, "FOSSA, quoting the NVCA model form, vendor view", MA, "fossa")
R["ma_promise_sca"] = Q(g, "Venture capital firms and acquirers use software composition analysis (SCA) tools like FOSSA and Black Duck to scan codebases for open-source dependencies", PROMISE, "Promise Legal, a law firm blog", MA, "blog_promise")
R["ma_revision_pay"] = Q(g, "Payment alone does not transfer ownership.", REVISION, "Revision Legal, Jun 2026", MA, "revisionlegal")
R["ma_crv_title"] = Q(g, "Paying for development work does not, by itself, create the written chain of title an investor wants.", CRVROOM, "CRV", MA, "crv_com_content_what_is")
R["ma_verdantix"] = Q(g, "Model labs can turn access to API services on or off with limited notice by ending contracts", VERDANTIX, "Verdantix, an analyst firm", MA, "verdantix")
R["ma_consilium_cc"] = Q(g, "Merger and change-of-control provisions, reviewed separately.", CONSILIUM, "Consilium Law, Aug 2026", MA, "consilium_law")
R["ma_consilium_stage"] = Q(g, "before serious diligence access, since consent timelines belong to the counterparty", CONSILIUM, "Consilium Law, Aug 2026", MA, "consilium_law")
R["ma_cogency"] = Q(g, "it may be your first inclination to ignore a UCC that has a termination listed", COGENCY, "Cogency Global, a filing services firm", MA, "cogencyglobal")

R["ma_peony_vdroom"] = Q(g, "Peony lists a separate venture debt data room as the debt raise that often follows a Series A.", PEONY, "Peony, a data room vendor", MA, "peony_ink_blog_series_a", "paraphrase", "the debt raise that often follows your Series A")
R["ma_juro_note"] = Q(g, "If there are contracts with non-standard terms, known gaps, or issues you're aware of, address them in a covering note rather than waiting for them to be discovered.", JURO, "Juro, a contract software vendor", MA, "juro_com")

R["cc_juro_unsigned"] = Q("customer-contracts-and-order-forms", "A contract that was never properly executed isn't enforceable in the way the parties might assume.", JURO, "Juro, a contract software vendor", CC, "juro_com")

R["ma_docsend_group"] = Q(g, "DocSend's checklist groups these as 'Material agreements' and lists property leases, loans and liens, loans the company has made, insurance policies, licences of the company's IP to others and of other people's IP to the company, standard forms, consulting agreements, agreements with officers and directors, and anything outside the ordinary course that could matter to the business.", DOCSEND_CHECK, "DocSend, due diligence checklist", MA, "docsend_com_blog_due", "paraphrase", "Property leases (real estate and personal property)")
R["ma_promise_inventory"] = Q(g, "Maintain a dependency inventory. List every open-source dependency in your project, including transitive dependencies.", PROMISE, "Promise Legal, a law firm blog", MA, "blog_promise")
R["cr_hua_outside"] = Q("customer-references-and-letters-of-intent", "I always ask for at least one reference outside the people you’d naturally choose.", HUA, "Jonathan Hua, The Data Room", CR, "web_thedataroom")
R["cr_firstround_none"] = Q("customer-references-and-letters-of-intent", "First Round's partner-meeting guide says that at the seed stage there often are no customers to speak with.", FIRSTROUND, "First Round Review", CR, "review_firstround", "paraphrase", "assuming there are even customers to speak with")


RAW = pathlib.Path(__file__).resolve().parent
GUIDES = RAW.parent


def norm(s):
    for a, b in (("\u2019", "'"), ("\u2018", "'"), ("\u201c", '"'), ("\u201d", '"'), ("\u00a0", " ")):
        s = s.replace(a, b)
    return re.sub(r"\s+", "", s)


rows = []
problems = 0
unused = []
guide_text = {}
for key, e in R.items():
    gpath = GUIDES / (e["guide"] + ".md")
    if e["guide"] not in guide_text:
        guide_text[e["guide"]] = norm(gpath.read_text())
    needle = e["text"] if e["kind"] == "quote" else e["support"]
    saved = None
    for p in sorted((RAW / e["folder"]).glob(e["file"] + "*")):
        if p.suffix == ".txt" and norm(needle) in norm(p.read_text(errors="replace")):
            saved = p
            break
    verified = "yes" if saved else "no"
    if not saved:
        problems += 1
    if norm(e["text"]) not in guide_text[e["guide"]]:
        unused.append(key)
        continue
    rows.append([e["guide"], e["kind"], e["text"], e["link"], str(saved.relative_to(GUIDES)) if saved else "", verified])

with open(GUIDES / "quotes_customers.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["guide", "kind", "text", "link", "saved_file", "verified"])
    w.writerows(rows)

print("rows written:", len(rows))
print("quotes verified:", sum(1 for r in rows if r[1] == "quote" and r[5] == "yes"))
print("paraphrases verified:", sum(1 for r in rows if r[1] == "paraphrase" and r[5] == "yes"))
print("not verified:", sum(1 for r in rows if r[5] == "no"))
print("registry entries not used in a guide:", len(unused), unused)
print("problems:", problems)
