"""Build quotes_financials.csv and check every quote against the saved page.

Run: python3 -I raw/financials_quotes.py   (from the document_guides folder)

Each row is (key, guide, kind, text, link, saved_file, support).
- kind "quote": text must appear word for word in the saved file, after both sides are
  normalised (curly quotes to straight, spaces collapsed, no space before punctuation).
- kind "paraphrase": text is my own words. `support` lists short exact strings from the
  saved file that the paraphrase rests on. verified = yes when every support string is found.
JSON files (Hacker News items) are read as text with HTML tags and entities removed.
Writes quotes_financials.csv one level up and prints any row that fails.
"""
import csv, html, json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "quotes_financials.csv"


def norm(s):
    s = html.unescape(s)
    s = re.sub(r"<[^>]+>", " ", s)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'),
                 ("‑", "-"), ("‐", "-"), ("–", "-"), (" ", " "), ("​", "")):
        s = s.replace(a, b)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([,.;:!?)])", r"\1", s)
    s = re.sub(r"([(])\s+", r"\1", s)
    s = re.sub(r"\s*-\s*", "-", s)
    return s.strip().lower()


def load(slug, fname):
    p = HERE / slug / fname
    raw = p.read_text(encoding="utf-8", errors="replace")
    if fname.endswith(".json"):
        raw = json.dumps(json.loads(raw))  # keep strings; unescape below
        raw = raw.encode().decode("unicode_escape", errors="ignore") if False else raw
        d = json.loads(p.read_text())
        parts = []
        def walk(n):
            if isinstance(n, dict):
                for k, v in n.items():
                    if isinstance(v, str):
                        parts.append(v)
                    else:
                        walk(v)
            elif isinstance(n, list):
                for v in n:
                    walk(v)
        walk(d)
        raw = " ".join(parts)
    return norm(raw)


ROWS = []


def q(key, guide, text, link, saved_file):
    ROWS.append((key, guide, "quote", text, link, saved_file, []))


def p(key, guide, text, link, saved_file, support):
    ROWS.append((key, guide, "paraphrase", text, link, saved_file, support))


FM = "financial-model"
HF = "historical-financials"
AF = "audited-or-reviewed-financials"
BS = "bank-statements"
TR = "tax-returns"
UF = "use-of-funds-plan"

A16Z = "https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/"
A16Z_F = "a16z_com_the_insiders_guide_to_data_rooms_what_to_know_before_you_raise.txt"
NFX = "https://www.nfx.com/post/the-non-obvious-guide-to-fundraising"
NFX_F = "nfx_com_post_the_non_obvious_guide_to_fundraising.txt"
KRUZEQ = "https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/"
KRUZEQ_F = "kruzeconsulting_com_what_are_examples_of_vc_due_diligence_check_lists.txt"
HALPHA = "https://www.highalpha.com/blog/want-to-raise-a-seed-or-series-a-heres-a-tip-dont-have-impossible-financial-projections"
HALPHA_F = "highalpha_com_blog_want_to_raise_a_seed_or_series_a_heres_a_tip_dont_have_impossible_financial_projections.txt"
MAC = "https://www.kauffmanfellows.org/journal/venture-diligence-at-the-seed-stage"
MAC_F = "kauffmanfellows_org_journal_venture_diligence_at_the_seed_stage.txt"
DATAROOM = "https://thedataroom.substack.com/p/how-a-vc-does-due-diligence-on-your-company"
DATAROOM_F = "web_thedataroom_substack_com_p_how_a_vc_does_due_diligence_on_your_company.txt"
HFBURN = "https://www.hustlefund.vc/post/angel-squad-startup-burn-rate-management-what-investors-should-actually-watch-for"
HFBURN_F = "web_hustlefund_vc_post_angel_squad_startup_burn_rate_management_what_investors_should_actually_watch_for.txt"
HFVERIFY = "https://www.hustlefund.vc/post/angel-squad-how-to-verify-startup-claims"
HFVERIFY_F = "hustlefund_vc_post_angel_squad_how_to_verify_startup_claims.txt"
VISIBLE = "https://visible.vc/blog/what-to-include-in-your-data-room/"
VISIBLE_F = "visible_vc_blog_what_to_include_in_your_data_room.txt"
CRV = "https://www.crv.com/content/what-is-a-data-room"
CRV_F = "crv_com_content_what_is_a_data_room.txt"
SM = "https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal"
SM_F = "web_startupsmagazine_co_uk_how_to_build_a_data_room_that_closes_the_deal.txt"
DOCSEND4 = "https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/"
DOCSEND4_F = "docsend_com_blog_4_types_of_documents_founders_must_have.txt"
SAASTR_DD = "https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet"
SAASTR_DD_F = "saastr_com_how_when_why_vcs_do_due_diligence_pre_and_post_term_sheet.txt"
TC23 = "https://techcrunch.com/2023/08/27/use-of-funds-are-not-percentages"
TC23_F = "techcrunch_com_2023_08_27_use_of_funds_are_not_percentages.txt"
TC22 = "https://techcrunch.com/2022/12/11/the-ask"
TC22_F = "techcrunch_com_2022_12_11_the_ask.txt"
KRUZEBANK = "https://kruzeconsulting.com/blog/startup-due-diligence-banking-documentation/"
KRUZEBANK_F = "kruzeconsulting_com_blog_startup_due_diligence_banking_documentation.txt"
KRUZEMIST = "https://kruzeconsulting.com/blog/startup-accounting-due-diligence-mistakes/"
KRUZEMIST_F = "kruzeconsulting_com_blog_startup_accounting_due_diligence_mistakes.txt"
KRUZESEEDTAX = "https://kruzeconsulting.com/blog/seed-stage-tax-returns/"
KRUZESEEDTAX_F = "kruzeconsulting_com_blog_seed_stage_tax_returns.txt"
KRUZEA = "https://kruzeconsulting.com/what-kind-of-financial-data-should-a-company-prepare-when-seeking-series-a-venture-capital-funding/"
KRUZEA_F = "kruzeconsulting_com_what_kind_of_financial_data_should_a_company_prepare_when_seeking_series_a_ventu.txt"
PAPERMARK = "https://www.papermark.com/blog/data-room-for-yc-startups"
PAPERMARK_F = "papermark_com_blog_data_room_for_yc_startups.txt"
PARO = "https://paro.ai/blog/financial-review-vs-audit/"
PARO_F = "paro_ai_blog_financial_review_vs_audit.txt"
MOFO = "https://scaleup.mofo.com/guidance/ask-a-mofo-common-provisions-in-venture-capital-term-sheets-information-and-observer-rights"
MOFO_F = "scaleup_mofo_com_guidance_ask_a_mofo_common_provisions_in_venture_capital_term_sheets_information_and_observer.txt"
BUILTIN = "https://builtin.com/blog/founder-cheatsheet-information-inspection-and-observer-rights-venture-financing"
BUILTIN_F = "builtin_com_blog_founder_cheatsheet_information_inspection_and_observer_rights_venture_financing.txt"
CARTA = "https://carta.com/learn/startups/financial-statements/financial-audits/"
CARTA_F = "carta_com_learn_startups_financial_statements_financial_audits.txt"
HOLLOWAY = "https://holloway.com/g/angel-investing/sections/legal-diligence-on-company-tax-issues"
HOLLOWAY_F = "holloway_com_g_angel_investing_sections_legal_diligence_on_company_tax_issues.txt"

# ---------------- financial-model ----------------
q("fm1", FM, "This may be a controversial one, but it’s often difficult to model forward-looking financials for early stage consumer companies. We love to hear the key milestones you’re looking to hit in the coming 12-18 months (and what you’ll need to get there), but we don’t expect a fully-baked model.", A16Z, A16Z_F)
q("fm2", FM, "In most cases, your projections shouldn’t be vastly different from the historical data. If MAUs have grown ~20% MoM for the past six months, it’s probably unrealistic to assume 200% MoM growth for the next year.", A16Z, A16Z_F)
q("fm3", FM, "Numbers that aren’t consistent with what’s in the deck. For example, your deck says $2M in ARR, but your model shows $1.5M.", A16Z, A16Z_F)
q("fm4", FM, "make sure it’s clear where historicals end and future projections begin by highlighting projections in a different color, or adding an (A) after actuals and a (P) after projections.", A16Z, A16Z_F)
q("fm5", FM, "This is less about your predicted revenue in month 36, or whatever, and more about understanding how you think about the business for the next year or two.", "https://news.ycombinator.com/item?id=30323322", "hn_item_30323322.json")
q("fm6", FM, "are the business model assumptions thoughtful or simplistic (e.g. ramp up team over time vs hire all on day one)? What ARE the key assumptions and levers?", "https://news.ycombinator.com/item?id=30323322", "hn_item_30323322.json")
q("fm7", FM, "do you have buffer time set aside for a future fundraise?", "https://news.ycombinator.com/item?id=30323322", "hn_item_30323322.json")
q("fm8", FM, "Include 24 months modeled monthly and another 3 years modeled annually (if credible).", NFX, NFX_F)
q("fm9", FM, "Each line should tell a story.", NFX, NFX_F)
q("fm10", FM, "VCs expect you to be optimistic about your business, but they also want to know you understand the economics of your business.", HALPHA, HALPHA_F)
q("fm11", FM, "The problem comes when cost growth is disconnected from revenue growth.", HALPHA, HALPHA_F)
q("fm12", FM, "If your gross margins are this high for a SaaS company, you’re missing some costs that should be included in cost of goods sold (COGS).", HALPHA, HALPHA_F)
q("fm13", FM, "All financial projections are only as good as the accuracy of their inputs, and at the seed stage it may be very difficult to have a firm grasp around the accuracy of the assumptions in a five or ten year financial projection.", MAC, MAC_F)
q("fm14", FM, "understanding the core assumptions driving a company’s revenue and costs are key to understanding the fundamentals of their business and for this reason it is important to study their pro-forma financial model.", MAC, MAC_F)
q("fm15", FM, "If your model only shows the bull case, it raises questions about whether you’ve genuinely stress-tested your assumptions.", "https://www.standardledger.co/uk/article/the-5-red-flags-in-your-financial-model-that-will-kill-investor-confidence/", "standardledger_co_uk_article_the_5_red_flags_in_your_financial_model_that_will_kill_investor_confidence.txt")
q("fm16", FM, "We’ve seen models where the unit economics on page 2 of the deck don’t reconcile with the revenue build in the model itself.", "https://www.standardledger.co/uk/article/the-5-red-flags-in-your-financial-model-that-will-kill-investor-confidence/", "standardledger_co_uk_article_the_5_red_flags_in_your_financial_model_that_will_kill_investor_confidence.txt")
q("fm17", FM, "Ideally, all of the assumptions should be on one page (not hard-coded into the model) so they can test your assumptions by adjusting the drivers without breaking the spreadsheet.", "https://fi.co/insight/epic-fail-in-fundraising-screwing-up-your-financial-assumptions-by-daveparkersea", "fi_co_insight_epic_fail_in_fundraising_screwing_up_your_financial_assumptions_by_daveparkersea.txt")
q("fm18", FM, "The most recent field audits, in contrast, generally used better methodologies and found errors in at least 86% of the spreadsheets audited.", "https://arxiv.org/pdf/0802.3457.pdf", "arxiv_org_pdf_0802_3457_panko_2000_spreadsheet_errors.txt")
q("fm19", FM, "When burn or revenue differs between the deck, the model and the accounting records, the gap suggests carelessness or something worse, and either reading damages the deal.", CRV, CRV_F)
q("fm20", FM, "The initial pass concentrates on a short list of corporate and legal records: the cap table, the financial model, the articles of incorporation and the intellectual property (IP) assignment agreements.", CRV, CRV_F)
q("fm21", FM, "At seed, a financial model is a signal that you think rigorously. At Series A, it's an input the associate rebuilds and stress-tests.", "https://www.peony.ink/blog/series-a-data-room", "peony_ink_blog_series_a_data_room.txt")
q("fm22", FM, "A three-year forecast presented as a chart with no underlying spreadsheet reads as marketing material, not analysis. Include the model with assumptions visible.", VISIBLE, VISIBLE_F)
q("fm23", FM, "3 to 5 year projections, usually by month (cash position is an important item they want to see projected)", KRUZEQ, KRUZEQ_F)
q("fm24", FM, "Build some slack into your model and assume most future hires start a month or two later than you would like.", "https://kruzeconsulting.com/blog/build-a-rolling-cash-forecast/", "kruzeconsulting_com_blog_build_a_rolling_cash_forecast.txt")
q("fm25", FM, "Companies at the pre-seed stage should show 3 years of annual projections, and companies at the seed stage should show 5 years.", DOCSEND4, DOCSEND4_F)
q("fm26", FM, "A forward cash forecast captures planned hires, renewals, taxes, collections, and other changes that history misses.", HFBURN, HFBURN_F)
q("fm27", FM, "If revenue in the deck doesn’t match the P&L, or you show only part of your history, everything else becomes questionable.", SM, SM_F)
q("fm30", FM, "If you’re burning $3M to add $1M in ARR, that’s a red flag.", "https://www.saastr.com/dear-saastr-what-are-the-top-10-metrics-series-a-investors-look-at/", "saastr_com_dear_saastr_what_are_the_top_10_metrics_series_a_investors_look_at.txt")
p("fm28", FM, "Paul Graham of Y Combinator tweeted that he has never read a business plan or balance sheet. This comes from the title of the Hacker News post that links the tweet; I could not open the tweet itself.", "https://news.ycombinator.com/item?id=30318634", "hn_item_30318634.json", ["I have never read a business plan or balance sheet"])
p("fm29", FM, "SaaStr's write-up of a talk by Christoph Janz of Point Nine Capital says to use the same model and logic for projections as for historic numbers, to report ARR movement (new, expansion, contraction, churn), and to explain any sudden improvement.", "https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital", "saastr_com_saas_investor_pitch_metrics_2024_christoph_janz_point_nine_capital.txt", ["You don’t want to use a different model or logic for projections and historic numbers.", "Any big changes or sudden improvements are suspicious", "contraction and churn"])

# ---------------- historical-financials ----------------
q("hf1", HF, "Historical P&L and burn. This should show the path from gross revenue through net income (loss) through cash outflow on a monthly basis. Make sure to break out different types of revenue (if applicable) and all of your major costs.", A16Z, A16Z_F)
q("hf2", HF, "For example, you only show three months of data when your company is three years old, or you show quarterly but not monthly revenue.", A16Z, A16Z_F)
q("hf3", HF, "When the pitch and the P&L disagree, the P&L wins, every time, no exceptions.", DATAROOM, DATAROOM_F)
q("hf4", HF, "VCs do not expect historical financials to change dramatically during a fund raise, which can happen if you haven’t done a good job keeping and closing your books.", KRUZEQ, KRUZEQ_F)
q("hf5", HF, "Past 3 year financial statements (income statement, balance sheet, cash flow)", KRUZEA, KRUZEA_F)
q("hf6", HF, "One of the most common due diligence issues is simply having books that are behind.", KRUZEMIST, KRUZEMIST_F)
q("hf7", HF, "A common mistake is recording the full value of a customer contract as revenue when the cash arrives or the invoice is issued (cash accounting).", KRUZEMIST, KRUZEMIST_F)
q("hf8", HF, "Payroll is often a company’s largest expense, which means discrepancies are easy for investors to spot.", KRUZEMIST, KRUZEMIST_F)
q("hf9", HF, "Poor categorization can also lead to inconsistent financial reporting.", KRUZEMIST, KRUZEMIST_F)
q("hf10", HF, "Monthly P&L for the past 24 months. Include comparisons to budget/plan.", "https://www.eaglerockcfo.com/blog/series-a-preparation/data-room-checklist", "eaglerockcfo_com_blog_series_a_preparation_data_room_checklist.txt")
q("hf11", HF, "Pay particular attention to accounts receivable aging and deferred revenue.", "https://www.eaglerockcfo.com/blog/series-a-preparation/data-room-checklist", "eaglerockcfo_com_blog_series_a_preparation_data_room_checklist.txt")
q("hf12", HF, "Founders should include historical profit-and-loss statements since inception as well as a year-to-date statement if it's the middle of the year. I also need to see the company's most recent balance sheet.", DOCSEND4, DOCSEND4_F)
q("hf13", HF, "Seed founders add 6 to 18 months of historical financials and an early KPI dashboard.", VISIBLE, VISIBLE_F)
q("hf14", HF, "Revenue recognized on an income statement may not arrive in the bank during the same month.", HFBURN, HFBURN_F)
q("hf15", HF, "If the operating calculation and bank movement do not agree, ask which financing flow, one-time payment, or timing difference is missing.", HFBURN, HFBURN_F)
q("hf16", HF, "Investors in the Series A stage and beyond will typically expect GAAP and IFRS financial statements.", "https://stripe.com/resources/more/cash-vs-accrual-accounting", "stripe_com_resources_more_cash_vs_accrual_accounting.txt")
q("hf17", HF, "Prepaid cash is not income; it is an obligation.", "https://taxstra.com/startup-accounting/", "taxstra_com_startup_accounting.txt")
q("hf18", HF, "If you've been recognizing revenue on cash receipt rather than ratable delivery, you're looking at a retroactive restatement before close.", "https://www.dualentry.com/blog/series-a-saas-accounting", "dualentry_com_blog_series_a_saas_accounting.txt")
q("hf19", HF, "Almost all startups should be cash basis as that most aligns with the nature of trying to get a business off the ground and being cash strapped", "https://davidcummings.org/2011/06/06/accrual-vs-cash-basis-accounting-for-startups/", "davidcummings_org_2011_06_06_accrual_vs_cash_basis_accounting_for_startups.txt")
q("hf20", HF, "I agree accrual accounting is best once the startup is off the ground but in the earliest of stages I still stand by cash being king.", "https://davidcummings.org/2011/06/06/accrual-vs-cash-basis-accounting-for-startups/", "davidcummings_org_2011_06_06_accrual_vs_cash_basis_accounting_for_startups.txt")
q("hf21", HF, "Investors will typically want two to three years of financial statements where available, along with year-to-date management accounts for the current period.", "https://www.standardledger.co/uk/article/preparing-your-financials-for-investor-due-diligence", "standardledger_co_uk_article_preparing_your_financials_for_investor_due_diligence.txt")
q("hf22", HF, "If revenue in the deck doesn’t match the P&L, or you show only part of your history, everything else becomes questionable.", SM, SM_F)
q("hf23", HF, "When burn or revenue differs between the deck, the model and the accounting records, the gap suggests carelessness or something worse, and either reading damages the deal.", CRV, CRV_F)
q("hf24", HF, "If your gross margins are this high for a SaaS company, you’re missing some costs that should be included in cost of goods sold (COGS).", HALPHA, HALPHA_F)
q("hf25", HF, "For early stage companies, it is common to leave out this requirement to lessen the administrative burden on the company and its small team.", MOFO, MOFO_F)
p("hf26", HF, "SaaStr's write-up of a Point Nine talk advises projecting about two years and building the history and the projection on the same logic.", "https://www.saastr.com/saas-investor-pitch-metrics-2024-christoph-janz-point-nine-capital", "saastr_com_saas_investor_pitch_metrics_2024_christoph_janz_point_nine_capital.txt", ["Projections should be around two years", "You don’t want to use a different model or logic for projections and historic numbers."])

# ---------------- audited-or-reviewed-financials ----------------
q("af1", AF, "it is not unusual for early stage companies to provide unaudited financials until later rounds of financing.", MOFO, MOFO_F)
q("af2", AF, "Typically for the Series Seed to Series A round, the financial statements are unaudited given that the cost of obtaining audited financials is not the best use of the company’s limited funds at the earlier stage.", BUILTIN, BUILTIN_F)
q("af3", AF, "Typically, this audit requirement is not put in place until the Series B round but sometimes may be required earlier, particularly when the company is operating in a highly regulated industry.", BUILTIN, BUILTIN_F)
q("af4", AF, "And many investors require later-stage startups to provide audited financials as part of their investment agreement.", CARTA, CARTA_F)
q("af5", AF, "Private companies , on the other hand, aren’t mandated by the SEC to conduct financial audits.", CARTA, CARTA_F)
q("af6", AF, "For example, venture capital investors often start asking for audited financial statements once startups reach their Series B or Series C funding round .", PARO, PARO_F)
q("af7", AF, "A financial review provides “limited assurance” that your financial statements are free from material misstatement and compliant with accounting standards.", PARO, PARO_F)
q("af8", AF, "Review costs are often around half of audit fees.", PARO, PARO_F)
q("af9", AF, "reviews often last a few days to several weeks, while audits typically take around three months to complete.", PARO, PARO_F)
q("af10", AF, "Series A founders need reviewed or audited financials, cohort analysis, unit economics, and a current 409A.", VISIBLE, VISIBLE_F)
q("af11", AF, "Tax returns, audits, and legal docs like office leases or employee offer letters. We’re not lawyers or accountants! If we have a concern, we’ll request the documents we need.", A16Z, A16Z_F)
q("af12", AF, "Most recent audited financial statements and latest unaudited monthly financial statements.", "https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/", "cooley_vc_dd_request_list.txt")
q("af13", AF, "Audit evidence is considered to be more reliable when obtained in a documented form directly by the auditor from sources independent of the entity being audited.", "https://bcajonline.org/journal/external-confirmations-proving-existence-with-external-evidence/", "bcajonline_org_journal_external_confirmations_proving_existence_with_external_evidence.txt")
q("af14", AF, "As part of its due diligence process, the Audit Firm had an employee (the “Auditor”) conduct a physical site visit at NS8’s offices in Las Vegas, Nevada.", "https://news.ycombinator.com/item?id=24522396", "hn_item_24522396.json")
q("af15", AF, "You would not trust the account statements that the company gives you, you would get the same (hopefully) account statements yourself.", "https://news.ycombinator.com/item?id=24523476", "hn_item_24520960.json")
q("af16", AF, "Typically, only Major Investors will be granted information rights.", MOFO, MOFO_F)
q("af17", AF, "the CPA did not become aware of any material modifications necessary to be in conformity with generally accepted accounting principles.", "https://www.wegnercpas.com/services/audit-assurance/comparing-compilations-reviews-audits/", "wegnercpas_com_services_audit_assurance_comparing_compilations_reviews_audits.txt")
q("af18", AF, "Empty folders with optimistic names (\"Customer Reference Letters\", \"Audited Financials\") at pre-seed and seed signal exactly what they look like.", VISIBLE, VISIBLE_F)
q("af19", AF, "Pre-revenue or pre-Series A companies are often given a carve-out (unaudited annual statements instead), since a full audit costs $15,000-$60,000.", "https://valueaddvc.com/blog/information-rights-in-venture-term-sheets-what-vcs-see-and-what-founders-control", "valueaddvc_com_blog_information_rights_in_venture_term_sheets_what_vcs_see_and_what_founders_control.txt")

# ---------------- bank-statements ----------------
q("bs1", BS, "Confirm your reported revenue and expenses match real cash movement", KRUZEBANK, KRUZEBANK_F)
q("bs2", BS, "investors typically expect 12-24 months of business bank statements, monthly bank reconciliations tied to the general ledger", KRUZEBANK, KRUZEBANK_F)
q("bs3", BS, "Cash-basis books that don’t match reported metrics. If your investor updates cite accrual-based revenue but your books are cash-basis, the numbers won’t tie out cleanly.", KRUZEBANK, KRUZEBANK_F)
q("bs4", BS, "Evidence that reconciliations were performed close to month-end, not backfilled right before the raise", KRUZEBANK, KRUZEBANK_F)
q("bs5", BS, "Commingled funds. Founder personal expenses run through the business account (or vice versa) without clear documentation.", KRUZEBANK, KRUZEBANK_F)
q("bs6", BS, "For revenue claims, ask to see their Stripe dashboard or bank statements. Most honest founders will show you. If they hesitate or make excuses, that's a red flag the size of Texas.", HFVERIFY, HFVERIFY_F)
q("bs7", BS, "We did $50k total last month but $40k was one-time setup fees.", HFVERIFY, HFVERIFY_F)
q("bs8", BS, "If the numbers in their deck don't match the numbers in their data room, that's not a small mistake.", HFVERIFY, HFVERIFY_F)
q("bs9", BS, "Investors check that the revenue in the deck reaches the bank account. Three to six months of statements, exported as PDFs, ends that question in one click. Founders resist this one and should not; it is standard, and the alternative is a call about it.", PAPERMARK, PAPERMARK_F)
q("bs10", BS, "Bank statements & deep financial review. To make sure whatever you have is true.", SAASTR_DD, SAASTR_DD_F)
q("bs11", BS, "Basic financials and model review . But often only a cursory one.", SAASTR_DD, SAASTR_DD_F)
q("bs12", BS, "Reconcile bank deposits to reported revenue for a sample of months. Where they do not tie, there is either unrecorded revenue, which a buyer cannot pay for because it cannot be financed or defended, or a bookkeeping failure, which is its own finding.", "https://www.papermark.com/blog/due-diligence-red-flags", "papermark_com_blog_due_diligence_red_flags.txt")
q("bs13", BS, "When one of the investors grew suspicious of Raz’s claims, Raz allegedly provided the investor with falsified bank statements and forged contracts in an effort to conceal the fraud.", "https://amp.insurancejournal.com/news/east/2024/06/14/779473.htm", "amp_insurancejournal_com_news_east_2024_06_14_779473_htm.txt")
q("bs14", BS, "When an investor pressed Shamim to furnish details of those claims, he allegedly provided the investor with falsified bank statements in an effort to conceal the fraud.", "https://financemagnates.com/fintech/sec-moves-against-tech-startup-youplus-for-defrauding-investors/amp", "financemagnates_com_fintech_sec_moves_against_tech_startup_youplus_for_defrauding_investors_amp.txt")
q("bs15", BS, "Adam Rogas, the co-founder and former CEO of the startup, touted bank statements showing payments from NS8 customers that never happened, according to the SEC.", "https://www.cyberscoop.com/ns8-cyber-fraud-prevention-startup-adam-rogas-sec-fbi/", "cyberscoop_com_ns8_cyber_fraud_prevention_startup_adam_rogas_sec_fbi.txt")
q("bs16", BS, "As part of its due diligence process, the Audit Firm had an employee (the “Auditor”) conduct a physical site visit at NS8’s offices in Las Vegas, Nevada.", "https://news.ycombinator.com/item?id=24522396", "hn_item_24522396.json")
q("bs17", BS, "You would not trust the account statements that the company gives you, you would get the same (hopefully) account statements yourself.", "https://news.ycombinator.com/item?id=24523476", "hn_item_24520960.json")
q("bs18", BS, "Don’t auto-reject on a single signal. A single fraud signal (especially “unusual document source” alone) may be a false positive.", "https://docs.flinks.com/guides/upload/fraud-signals", "docs_flinks_com_guides_upload_fraud_signals.txt")
q("bs19", BS, "When users print their bank statement to PDF instead of downloading the original file, the resulting document may trigger fraud signals.", "https://docs.flinks.com/guides/upload/fraud-signals", "docs_flinks_com_guides_upload_fraud_signals.txt")
q("bs20", BS, "Wait, when they're doing due diligence, nobody actually checks anything with the bank? I think it might be harder to fake eligibility for a mortgage than $107 million ARR.", "https://news.ycombinator.com/item?id=48606618", "hn_data_room_diligence_comment.json")
q("bs21", BS, "Stripe subtracts its processing fee before it sends money.", "https://beancount.io/blog/2026/08/25/how-to-reconcile-stripe-payouts-gross-vs-net-fees-refunds-guide", "beancount_io_blog_2026_08_25_how_to_reconcile_stripe_payouts_gross_vs_net_fees_refunds_guide.txt")
q("bs22", BS, "A probe into the seven-year-old startup by EY as part of the due diligence for the recent funding deliberation found scores of issues, including inflated revenue and that some garages were fictitious, two sources said.", "https://techcrunch.com/2023/01/17/sequoia-india-backed-gomechanic-faces-severe-trouble", "techcrunch_com_2023_01_17_sequoia_india_backed_gomechanic_faces_severe_trouble.txt")
q("bs23", BS, "Change logs from your accounting software showing edits to historical entries (a healthy sign; a lack of any edit history can actually look suspicious)", KRUZEBANK, KRUZEBANK_F)
q("bs24", BS, "If they dodge questions about burn rate or runway, walk away.", HFVERIFY, HFVERIFY_F)
q("bs25", BS, "If the operating calculation and bank movement do not agree, ask which financing flow, one-time payment, or timing difference is missing.", HFBURN, HFBURN_F)
p("bs26", BS, "On a podcast, a SaaS fund founder said investors should always check the bank account, and that his most stressful investments all had made-up claims in them (as summarised in the 20VC newsletter).", "https://20vc.substack.com/p/20vc-newsletter-june-2nd-2024", "web_20vc_substack_com_p_20vc_newsletter_june_2nd_2024.txt", ["Why Investors Should Always Check the Bank Account", "My most stressful investments all have bullshit in them."])
p("bs27", BS, "Angel Investors Network, summarising an SEC complaint against the founder of ComplYant, reports that actual monthly subscription income never passed $620 while investor decks showed up to $250,000 a month, and says one bank statement would have shown it. These are allegations.", "https://angelinvestorsnetwork.com/startups/complyant-shiloh-luckey-startup-fraud-diligence-lessons", "angelinvestorsnetwork_com_startups_complyant_shiloh_luckey_startup_fraud_diligence_lessons.txt", ["It never exceeded $620 in any single month.", "Nobody appears to have asked for a Stripe screenshot or a bank statement."])
p("bs28", BS, "Visible's stage table marks bank statements as not expected at pre-seed, lighter at seed, and expected at Series A.", VISIBLE, VISIBLE_F, ["Bank statements (3 to 12 months)"])

# ---------------- tax-returns ----------------
q("tr1", TR, "Failure to file tax returns - an angel or seed investor may not notice, but by the time you are raising a big round from a professional investor, you bet they are going to ask for tax returns.", KRUZEQ, KRUZEQ_F)
q("tr2", TR, "Past 3 years Federal tax returns", KRUZEQ, KRUZEQ_F)
q("tr3", TR, "It’s common practice for sophisticated, later-stage venture investors to ask for all past returns so they can make sure that your company has been legally compliant and operating properly.", KRUZESEEDTAX, KRUZESEEDTAX_F)
q("tr4", TR, "An acquirer’s due diligence red flag goes up when a startup’s financials don’t match its tax returns.", KRUZESEEDTAX, KRUZESEEDTAX_F)
q("tr5", TR, "Unless exempt under section 501, all domestic corporations (including corporations in bankruptcy) must file an income tax return whether or not they have taxable income.", "https://www.irs.gov/instructions/i1120", "irs_gov_instructions_i1120.txt")
q("tr6", TR, "Failure to file the report and pay the required franchise taxes will result in a penalty of $200.00 plus 1.5% interest per month on tax and penalty.", "https://corp.delaware.gov/paytaxes/", "corp_delaware_gov_paytaxes.txt")
q("tr7", TR, "Even if the company has no revenue, it may still need to file tax returns; and even if it is not making a profit, sales and payroll taxes still accrue.", HOLLOWAY, HOLLOWAY_F)
q("tr8", TR, "Payroll taxes are especially scary because directors and officers can be personally responsible for them in certain circumstances.", HOLLOWAY, HOLLOWAY_F)
q("tr9", TR, "Failure to collect and remit sales taxes can add up to a large liability in a short period of time, and it is not uncommon for companies to fall out of compliance with sales tax collect and remit requirements.", HOLLOWAY, HOLLOWAY_F)
q("tr10", TR, "The founders should have given the company copies of their filed elections.", HOLLOWAY, HOLLOWAY_F)
q("tr11", TR, "Tax returns, audits, and legal docs like office leases or employee offer letters. We’re not lawyers or accountants! If we have a concern, we’ll request the documents we need.", A16Z, A16Z_F)
q("tr12", TR, "Following the decision, all states have enacted some form of legislation that adopts an economic nexus threshold (typically, this threshold is $100,000 in sales or 200 transactions).", "https://www.bdo.com/insights/industries/technology/breaking-down-sales-and-use-tax-compliance-for-saas-companies", "bdo_com_insights_industries_technology_breaking_down_sales_and_use_tax_compliance_for_saas_companies.txt")
q("tr13", TR, "Sales tax exposure will remain a priority consideration during the due diligence process for any strategic deals taking place.", "https://www.bdo.com/insights/industries/technology/breaking-down-sales-and-use-tax-compliance-for-saas-companies", "bdo_com_insights_industries_technology_breaking_down_sales_and_use_tax_compliance_for_saas_companies.txt")
q("tr14", TR, "restoring full expensing of domestic research or experimental expenditures (“R&E”) in the year incurred under new Internal Revenue Code (“IRC”) Section 174A.", "https://www.anchin.com/articles/obbba-the-research-credit-and-section-174/", "anchin_com_articles_obbba_the_research_credit_and_section_174.txt")
q("tr15", TR, "In addition, make sure to perform annual reconciliations between your company’s financial statements and tax returns. Discrepancies between the two can trigger inquiries and cause delays during audits and reviews.", PARO, PARO_F)
q("tr16", TR, "Tax returns (from founding to present)", "https://www.docsend.com/blog/due-diligence-checklist/", "docsend_com_blog_due_diligence_checklist.txt")
q("tr17", TR, "Schedule M-1. Reconciliation of Income (Loss) per Books With Income per Return", "https://www.irs.gov/instructions/i1120", "irs_gov_instructions_i1120.txt")
q("tr18", TR, "Evidence of payroll tax payments and filings", KRUZEBANK, KRUZEBANK_F)
q("tr19", TR, "All active Domestic Corporation Annual Reports and Franchise Taxes for the prior year are due annually on or before March 1st and are required to be filed online.", "https://corp.delaware.gov/paytaxes/", "corp_delaware_gov_paytaxes.txt")

# ---------------- use-of-funds-plan ----------------
q("uf1", UF, "a detailed plan for the use of the funds from this round", DOCSEND4, DOCSEND4_F)
q("uf2", UF, "as well as a rough road map or plan for how you will use the funds.", A16Z, A16Z_F)
q("uf3", UF, "That means that in effect, a startup needs to think two funding rounds ahead when raising money: what you need to raise for this round, and the amount you will need for the next round, which will probably happen between 18 and 24 months from now.", TC23, TC23_F)
q("uf4", UF, "Spending 60% on operations makes me think that this is a very lopsided company.", TC23, TC23_F)
q("uf5", UF, "Then put a price tag on all of that and add a safety buffer of 20% to 40%, and that’s the amount of money you need to raise.", TC23, TC23_F)
q("uf6", UF, "Add 30% to 70% as a safety buffer (depending on how good your planning is and how predictable your business is), and that’s how much money you need to raise.", TC22, TC22_F)
q("uf7", UF, "You are not raising money to get 18 months of runway. You are raising money to hit a certain set of milestones.", TC22, TC22_F)
q("uf8", UF, "Put differently: If I’m going to invest $2 million into your startup, I want to know what that money buys me, in terms of progress for your company.", TC22, TC22_F)
q("uf9", UF, "Poor goals are vague: “Improve marketing,” or “Get more customers” or “Add features to our product.”", TC22, TC22_F)
q("uf10", UF, "If you expect something to take 18 months, but it takes 24, it’s a really poor look if you run out of money in month 19.", TC22, TC22_F)
q("uf11", UF, "Requested investment should provide at least 18-24 months of runway .", NFX, NFX_F)
q("uf12", UF, "Typically, companies raise enough capital to fund operations for around 18 months.", MAC, MAC_F)
q("uf13", UF, "It is important to know the company’s gross and net current and ramped burn rates to ensure that the amount being raised will be enough to get them to the next fundraising round.", MAC, MAC_F)
q("uf14", UF, "Their goal should be to raise as much money as needed to get to their next “fundable” milestone, which will usually be 12 to 18 months later.", "https://www.ycombinator.com/blog/how-to-raise-a-seed-round/", "ycombinator_com_blog_how_to_raise_a_seed_round.txt")
q("uf15", UF, "Seed and Series A founders also need bios for the key team members, an org chart, and a hiring plan tied directly to the use of funds.", VISIBLE, VISIBLE_F)
q("uf16", UF, "There is no universal good burn rate. The useful test is whether the company can reach a valuable milestone, preserve options, and explain the evidence each dollar is buying.", HFBURN, HFBURN_F)
q("uf17", UF, "If they dodge questions about burn rate or runway, walk away.", HFVERIFY, HFVERIFY_F)
q("uf18", UF, "if the burn rate is too high, I find they tend to run out of money as they scale to $5m-$10m ARR.", "https://www.saastr.com/10-of-my-top-seed-investing-mistakes", "saastr_com_10_of_my_top_seed_investing_mistakes.txt")
q("uf19", UF, "Reframe your points, focusing less on the day-to-day use of funds and more on the results.", "https://wiss.com/the-investors-perspective-how-pitch-decks-often-miss-the-point/", "wiss_com_the_investors_perspective_how_pitch_decks_often_miss_the_point.txt")
q("uf20", UF, "I look at burn against progress: a team that did a lot on a little earns real trust, and a team that burned a lot to produce very little earns uncompromising scrutiny.", DATAROOM, DATAROOM_F)
q("uf21", UF, "Almost every founder regrets using capital to keep a high-burn rate engine going that isn’t scaling rapidly.", "https://www.saastr.com/every-top-founder-ever-i-should-have-acted-on-bad-trends-earlier/", "web_saastr_com_every_top_founder_ever_i_should_have_acted_on_bad_trends_earlier.txt")
q("uf22", UF, "Build some slack into your model and assume most future hires start a month or two later than you would like.", "https://kruzeconsulting.com/blog/build-a-rolling-cash-forecast/", "kruzeconsulting_com_blog_build_a_rolling_cash_forecast.txt")
q("uf23", UF, "Don’t list a range.", TC22, TC22_F)

# ---------------- added after the guides were drafted ----------------
q("fm31", FM, "If the numbers in their deck don't match the numbers in their data room, that's not a small mistake.", HFVERIFY, HFVERIFY_F)
q("fm32", FM, "Your 3-5 year projections with monthly detail for year one", "https://www.eaglerockcfo.com/blog/series-a-preparation/data-room-checklist", "eaglerockcfo_com_blog_series_a_preparation_data_room_checklist.txt")
q("fm33", FM, "Three-year forward projections tied to a real operating model, not a single hockey-stick line", "https://www.peony.ink/blog/series-a-data-room", "peony_ink_blog_series_a_data_room.txt")
p("fm35", FM, "Eagle Rock CFO asks for scenario analysis (base, upside, downside) in the Series A model.", "https://www.eaglerockcfo.com/blog/series-a-preparation/data-room-checklist", "eaglerockcfo_com_blog_series_a_preparation_data_room_checklist.txt", ["Show scenario analysis (base, upside, downside)."])
p("fm36", FM, "Standard Ledger, a UK accounting firm, says seed investors want a revenue build, realistic headcount assumptions, unit economics and at least 24 to 36 months of projections.", "https://www.standardledger.co/uk/article/the-5-red-flags-in-your-financial-model-that-will-kill-investor-confidence/", "standardledger_co_uk_article_the_5_red_flags_in_your_financial_model_that_will_kill_investor_confidence.txt", ["at least 24-36 months of projections"])
p("fm37", FM, "Venture Lab, a blog, lists churn missing or unrealistically low, profitability just before the next raise, no sensitivity analysis, mixing up bookings, revenue and cash, and round numbers with no bottom-up calculation among twelve red flags.", "https://venture-lab.org/2026/startup-financial-projections-red-flags/", "venture_lab_org_2026_startup_financial_projections_red_flags.txt", ["Churn rate that is missing or unrealistically low", "Projections that hit profitability right before you need to raise again", "No sensitivity analysis or scenario modeling", "Mixing up bookings, revenue, and cash", "Round numbers everywhere with no bottom-up calculations"])
p("fm38", FM, "A KPMG survey of spreadsheet financial models, reported in a University of Greenwich teaching paper, found major errors in 95 percent of them.", "https://arxiv.org/pdf/0801.1514.pdf", "arxiv_org_pdf_0801_1514_pdf.txt", ["95% of models were found to contain major errors"])
p("fm39", FM, "Panko's paper describes omission errors: the developer leaves out something that should be in the model.", "https://arxiv.org/pdf/0802.3457.pdf", "arxiv_org_pdf_0802_3457_panko_2000_spreadsheet_errors.txt", ["Omission errors occur when the developer omits something that should be in the model."])
p("fm40", FM, "Dave Parker says a founder must know where things are in the spreadsheet even with a CFO.", "https://fi.co/insight/epic-fail-in-fundraising-screwing-up-your-financial-assumptions-by-daveparkersea", "fi_co_insight_epic_fail_in_fundraising_screwing_up_your_financial_assumptions_by_daveparkersea.txt", ["you have to know where they are in the spreadsheet"])
p("fm41", FM, "In the Hacker News thread, lpolovets says the Paul Graham view does not apply to seed rounds at ten times higher valuations.", "https://news.ycombinator.com/item?id=30323322", "hn_item_30323322.json", ["This won't apply to startups raising seed rounds at 10x higher valuations."])

q("hf27", HF, "Mixing personal and company expenses.", VISIBLE, VISIBLE_F)
q("hf28", HF, "one of the fastest ways to lose credibility", VISIBLE, VISIBLE_F)
p("hf29", HF, "Kruze's worked example: a customer who pays $24,000 upfront for a 12-month subscription; revenue is spread over the months and the unearned part is deferred revenue.", KRUZEMIST, KRUZEMIST_F, ["if a customer pays $24,000 upfront for a 12-month subscription", "recording the unearned portion as deferred revenue"])

p("af20", AF, "Wegner CPAs: a compilation gives no assurance, a review gives limited assurance, an audit gives reasonable assurance.", "https://www.wegnercpas.com/services/audit-assurance/comparing-compilations-reviews-audits/", "wegnercpas_com_services_audit_assurance_comparing_compilations_reviews_audits.txt", ["This is known as the expression of \u201cno assurance.\u201d", "to express \u201climited assurance\u201d on financial statements that have not been audited", "expresses \u201creasonable assurance\u201d that the financial statements fairly present"])
p("af21", AF, "Haven writes its audit checklist for Series A founders as if audits are normal at that stage.", "https://www.usehaven.com/blog-posts/financial-audit-prep-checklist-for-series-a-founders-startup-guide", "usehaven_com_blog_posts_financial_audit_prep_checklist_for_series_a_founders_startup_guide.txt", ["At Series A, startups typically face more formal and detailed financial examinations compared to seed rounds."])
p("af22", AF, "Carta lists the three outcomes of an audit: unqualified (clean) opinion, adverse opinion, disclaimer of opinion; it describes an adverse opinion as records not aligned with GAAP and egregiously misstated.", CARTA, CARTA_F, ["Unqualified opinion (clean opinion)", "Adverse opinion: Your financial records are not aligned with GAAP", "egregiously misstated", "Disclaimer of opinion"])
p("af23", AF, "Carta advises a first-time company to work with an auditor its investors recommend.", CARTA, CARTA_F, ["If it\u2019s your first financial audit, you may want to work with an auditor that\u2019s recommended by your investors."])
p("af24", AF, "Morrison Foerster says investors may negotiate to receive audited financial statements, and that only Major Investors typically get information rights.", MOFO, MOFO_F, ["Investors may negotiate to receive audited financial statements", "Typically, only Major Investors will be granted information rights."])
p("af25", AF, "Visible's stage table marks audited or reviewed financials as lighter at Series A.", VISIBLE, VISIBLE_F, ["Audited or reviewed financials"])

q("bs29", BS, "Records showing how prior investment rounds were received into the bank account", KRUZEBANK, KRUZEBANK_F)
q("bs30", BS, "Audit evidence is considered to be more reliable when obtained in a documented form directly by the auditor from sources independent of the entity being audited.", "https://bcajonline.org/journal/external-confirmations-proving-existence-with-external-evidence/", "bcajonline_org_journal_external_confirmations_proving_existence_with_external_evidence.txt")
p("bs31", BS, "Papermark's YC guide lists bank statements in a pre-wire confirmation set with incorporation documents, IP assignments and the stock plan.", PAPERMARK, PAPERMARK_F, ["Pre-wire confirmation Incorporation docs, IP assignments, stock plan, bank statements"])

q("tr21", TR, "Any correspondence with tax authorities", KRUZEQ, KRUZEQ_F)
q("tr22", TR, "Past 3 years State tax returns", KRUZEQ, KRUZEQ_F)
q("tr23", TR, "regardless of whether they have any income", HOLLOWAY, HOLLOWAY_F)
p("tr24", TR, "Kruze: Form 1120 is due April 15 for a calendar-year C corporation, with an extension to October 15 by filing Form 7004 and paying expected tax.", KRUZESEEDTAX, KRUZESEEDTAX_F, ["are due April 15, 2026 for the 2025 tax year", "Form 7004", "as long as you pay any expected tax with the extension"])
p("tr25", TR, "Kruze: before 2025, Section 174 required amortization of domestic R&D costs, which raised taxable income for many unprofitable startups.", KRUZESEEDTAX, KRUZESEEDTAX_F, ["required amortization of domestic R&D costs under Section 174"])
p("tr26", TR, "Kruze: IRS penalties for unfiled returns can be steep and a deal can be delayed by months.", KRUZEQ, KRUZEQ_F, ["the IRS penalties can be steep", "your deal can get delayed by months"])
p("tr27", TR, "Holloway: a company ran its own payroll, the CEO did not pass withholding to the IRS, the board fired the CEO and the company failed.", HOLLOWAY, HOLLOWAY_F, ["The CEO did not remit to the IRS the amounts of the income and employment tax withholding", "The board had to fire the CEO, and the company ultimately failed from this financial setback."])
p("tr28", TR, "BDO's article dates from 2022 and counts about 20 states taxing SaaS then.", "https://www.bdo.com/insights/industries/technology/breaking-down-sales-and-use-tax-compliance-for-saas-companies", "bdo_com_insights_industries_technology_breaking_down_sales_and_use_tax_compliance_for_saas_companies.txt", ["Approximately 20 states currently subject SaaS to tax", "tech M&A activity is expected to slow for the remainder of 2022"])
p("tr29", TR, "DocSend's diligence checklist is framed as what investors ask for after a term sheet is signed.", "https://www.docsend.com/blog/due-diligence-checklist/", "docsend_com_blog_due_diligence_checklist.txt", ["after a term sheet is signed"])
p("tr30", TR, "Cooley's sample VC request list has no tax-return line.", "https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/", "cooley_vc_dd_request_list.txt", ["Most recent audited financial statements"])

q("uf24", UF, "This might include detailed percentages or figures for areas like product development, marketing, staff salaries or operational costs.", "https://8base.com/blog/use-of-funds-slide", "8base_com_blog_use_of_funds_slide.txt")
q("uf25", UF, "Obviously, the easiest way to fail on this slide is to forget to include it altogether.", TC22, TC22_F)
q("uf26", UF, "Are they sure $5 million is enough to get to where they are going?", TC23, TC23_F)

q("bs32", BS, "The Auditor was directed by a more senior Audit Firm employee to have someone from NS8 log in to the online portal for each NS8 bank account, display the current account balance, and download monthly bank statements for fiscal year 2019.", "https://news.ycombinator.com/item?id=24522396", "hn_item_24522396.json")
q("af26", AF, "The Auditor was directed by a more senior Audit Firm employee to have someone from NS8 log in to the online portal for each NS8 bank account, display the current account balance, and download monthly bank statements for fiscal year 2019.", "https://news.ycombinator.com/item?id=24522396", "hn_item_24522396.json")


def main():
    rows = []
    bad = 0
    cache = {}
    for key, guide, kind, text, link, saved, support in ROWS:
        slug_dir = guide
        rel = saved
        if rel.startswith("../"):
            parts = rel.split("/")
            slug_dir = parts[1]
            rel = parts[2]
        ck = (slug_dir, rel)
        try:
            if ck not in cache:
                cache[ck] = load(slug_dir, rel)
            body = cache[ck]
        except FileNotFoundError:
            body = ""
            print("MISSING FILE", key, slug_dir, rel)
        if kind == "quote":
            ok = norm(text) in body
        else:
            ok = all(norm(s) in body for s in support)
        if not ok:
            bad += 1
            print("FAIL", key, kind, text[:90])
        rows.append([guide, kind, text, link, f"raw/{guide}/{saved}" if not saved.startswith("../") else f"raw/{saved[3:]}", "yes" if ok else "no"])
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["guide", "kind", "text", "link", "saved_file", "verified"])
        w.writerows(rows)
    nq = sum(1 for r in rows if r[1] == "quote" and r[5] == "yes")
    npar = sum(1 for r in rows if r[1] == "paraphrase" and r[5] == "yes")
    print(f"rows {len(rows)}; verified quotes {nq}; verified paraphrases {npar}; failures {bad}")


if __name__ == "__main__":
    main()
