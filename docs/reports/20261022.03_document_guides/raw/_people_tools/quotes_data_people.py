FB, KT, HP, EO, AI = ("founder-bios", "key-team-bios-and-org-chart", "hiring-plan-and-future-org",
                      "employment-advisory-and-option-grant-records", "ai-and-data-governance-documents")

VISIBLE = "https://visible.vc/blog/what-to-include-in-your-data-room/"
VISIBLE_F = "visible_vc_blog_what_to_include_in_your_data_room.txt"
A16Z = "https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/"
A16Z_F = "a16z_com_the_insiders_guide_to_data_rooms_what_to_know_before_you_raise.txt"
HF_CHECK = "https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step"
HF_CHECK_F = "hustlefund_vc_post_angel_squad_angel_investing_due_diligence_checklist_step_by_step.txt"
HF_RED = "https://www.hustlefund.vc/post/angel-squad-red-flags-in-startup-founders-that-experienced-investors-never-ignore"
HF_RED_F = "web_hustlefund_vc_post_angel_squad_red_flags_in_startup_founders_that_experienced_investors_never_ignore.txt"
KRUZE_DD = "https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/"
KRUZE_DD_F = "kruzeconsulting_com_what_are_examples_of_vc_due_diligence_check_lists.txt"
COOLEY_LIST = "https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/"
COOLEY_LIST_F = "cooley_vc_dd_request_list.txt"
DOCSEND = "https://www.docsend.com/blog/due-diligence-checklist/"
DOCSEND_F = "docsend_com_blog_due_diligence_checklist.txt"
SAASTR_DD = "https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet"
SAASTR_DD_F = "saastr_com_how_when_why_vcs_do_due_diligence_pre_and_post_term_sheet.txt"
SAASTR_BG = "https://www.saastr.com/what-kind-of-background-check-do-vcs-do-on-the-entrepreneurs-they-fund/"
SAASTR_BG_F = "saastr_com_what_kind_of_background_check_do_vcs_do_on_the_entrepreneurs_they_fund.txt"
FORM = "https://formventures.substack.com/p/team-talks-ii-founder-reference-calls"
FORM_F = "formventures_substack_com_p_team_talks_ii_founder_reference_calls.txt"
GOINGVC = "https://www.goingvc.com/post/how-to-reference-check-a-founder"
GOINGVC_F = "goingvc_com_post_how_to_reference_check_a_founder.txt"
FIRSTROUND = "https://review.firstround.com/heres-what-you-can-really-expect-when-pitching-your-seed-stage-startup-at-a-vc-partner-meeting/"
FIRSTROUND_F = "review_firstround_com_heres_what_you_can_really_expect_when_pitching_your_seed_stage_startup_at_a_vc.txt"
STARTUPSMAG_DR = "https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal"
STARTUPSMAG_DR_F = "web_startupsmagazine_co_uk_how_to_build_a_data_room_that_closes_the_deal.txt"
HN_PG = "https://news.ycombinator.com/item?id=7481618"
SEC_ALTS = "https://thediwire.com/?p=43904"
SEC_ALTS_F = "thediwire_com_p_43904.txt"
CAUSO = "https://hub.causo.ai/guides/team-slide-first-time-founder"
CAUSO_F = "hub_causo_ai_guides_team_slide_first_time_founder.txt"
WAVEUP = "https://waveup.com/blog/why-your-decks-team-slide-is-the-most-important-one/"
WAVEUP_F = "waveup_com_blog_why_your_decks_team_slide_is_the_most_important_one.txt"
AIN = "https://angelinvestorsnetwork.com/startups/founder-diligence-what-investors-actually-check"
AIN_F = "angelinvestorsnetwork_com_startups_founder_diligence_what_investors_actually_check.txt"
HF_FRAME = "https://www2.hustlefund.vc/post/angel-squad-how-hustle-fund-reviews-1000-startups-per-month-for-its-angel-investing-group"
HF_FRAME_F = "www2_hustlefund_vc_post_angel_squad_how_hustle_fund_reviews_1000_startups_per_month_for_its_angel_in.txt"
HF_CULT = "https://www2.hustlefund.vc/post/angel-squad-cultural-due-diligence-why-company-culture-matters-to-angel-investment-returns"
HF_CULT_F = "www2_hustlefund_vc_post_angel_squad_cultural_due_diligence_why_company_culture_matters_to_angel_inve.txt"

# ---------------------------------------------------------------- founder bios
q(FB, "At pre-seed, founder bios with relevant experience are sufficient.", VISIBLE, VISIBLE_F)
q(FB, "We definitely want to understand the background of the founding team and other executives, but we generally use LinkedIn for this.", A16Z, A16Z_F)
q(FB, "The founder could not explain monthly traffic, conversion rate, returning-customer percentage, or customer acquisition cost (CAC).", HF_RED, HF_RED_F)
q(FB, "Founders do not need every number memorized, especially before launch. They do need to know which measures drive the company and where to find them.", HF_RED, HF_RED_F)
q(FB, "Healthy co-founders disagree. What matters is whether they can make a decision, support it, and resolve tension without leaving the company stuck.", HF_RED, HF_RED_F)
q(FB, "Intellectual honesty. The founder distinguishes fact, estimate, and hypothesis.", HF_RED, HF_RED_F)
q(FB, "verify only the identity, employment, education, professional license, litigation, or other history that could change your thesis, and treat a discrepancy as a prompt for context rather than an automatic finding of misconduct.", HF_CHECK, HF_CHECK_F)
q(FB, "Co-founder history: How long have the founders known each other, what have they built or overcome together, and why did they choose to partner?", HF_CHECK, HF_CHECK_F)
q(FB, "Commitment: Are the founders full-time? If not, what is the transition plan and what dependencies remain?", HF_CHECK, HF_CHECK_F)
q(FB, "If you have something to hide here, it will likely come out later. Post term sheet.", SAASTR_DD, SAASTR_DD_F)
q(FB, "Sometimes, a VC will issue a term sheet just talking to the CEO. But it can help a lot to talk to the other founders too, especially the CTO if there is one.", SAASTR_DD, SAASTR_DD_F)
q(FB, "Finding material issues late in the potential investment process is a big flag.", SAASTR_BG, SAASTR_BG_F)
q(FB, "So disclose whatever issues there are early.", SAASTR_BG, SAASTR_BG_F)
q(FB, "Most VCs do reference calls. From my conversations, few feel like they do them very well.", FORM, FORM_F)
q(FB, "Still vanishingly rare.", FORM, FORM_F)
q(FB, "Founders tend to prep and provide 1-2 curated referees, so a couple of off-book references can have a multiplier effect on an investor’s context, insight and conviction.", FORM, FORM_F)
q(FB, "don’t let the absence of a strong reference network automatically serve as a red flag, especially for underrepresented founders who may be building outside the established networks that make back-channel references easy to find.", GOINGVC, GOINGVC_F)
q(FB, "At First Round, we typically have anywhere from 5-15 diligence conversations, all of which are with people who can speak about the business (such as prospective or actual customers) or who can speak about the founders (such as former colleagues).", FIRSTROUND, FIRSTROUND_F)
q(FB, "Before I even open your data room, I already have ten tabs up. I’m checking your traffic, reviews, investors, any co-founder issues, and whether your story matches what’s online.", STARTUPSMAG_DR, STARTUPSMAG_DR_F)
q(FB, "the main thing I looked for was energetic founders working on an idea that grew organically out of their own experience.", HN_PG, "hn_yc_application_read_comment.json")
q(FB, "If any officers are not currently devoting 100% of their business time to the Company, please note them on this list.", COOLEY_LIST, COOLEY_LIST_F)
q(FB, "making fraudulent misrepresentations about Centricity’s customers and revenue as well as Brackett’s own educational and employment background.", SEC_ALTS, SEC_ALTS_F)
q(FB, "Investors are specifically checking whether you inflated your resume.", AIN, AIN_F)
q(FB, "swap exits for four founder-market fit signals: domain-obsession tenure, customer proximity, technical depth proof, and a hard thing you already shipped.", CAUSO, CAUSO_F)
q(FB, "This isn't about pedigree or where someone went to school.", HF_FRAME, HF_FRAME_F)
q(FB, "Second: can the founder execute?", HF_FRAME, HF_FRAME_F)
q(FB, "Third: is the founder coachable?", HF_FRAME, HF_FRAME_F)
p(FB, "Fund-side view: the Brackett case. The SEC alleges a startup founder raised $2.8 million from seven investors partly by misstating his own education and work history, and by inventing customers and revenue. These are allegations in a complaint, not findings. The SEC's own page blocked automated fetching, so the text comes from a republished copy of the press release.", SEC_ALTS, SEC_ALTS_F)
p(FB, "The Hustle Fund red-flag guide says to calibrate to the stage the company claims, to record a concern neutrally, to ask one neutral follow-up, to request evidence the team already uses and to check another source.", HF_RED, HF_RED_F)
p(FB, "Cultural due diligence (Hustle Fund): ask for a specific event, who acted, and what happened afterward, rather than relying on a values statement.", HF_CULT, HF_CULT_F)

# --------------------------------------------------------- key team and org chart
q(KT, "VCs invest in teams before products; bios and org chart are non-negotiable", VISIBLE, VISIBLE_F)
q(KT, "Seed and Series A founders also need bios for the key team members, an org chart, and a hiring plan tied directly to the use of funds.", VISIBLE, VISIBLE_F)
q(KT, "By Series A, employment and advisory agreements with IP assignment and key-person retention terms become standard diligence asks.", VISIBLE, VISIBLE_F)
q(KT, "We definitely want to understand the background of the founding team and other executives, but we generally use LinkedIn for this.", A16Z, A16Z_F)
q(KT, "Org chart", KRUZE_DD, KRUZE_DD_F)
q(KT, "Any transactions with executives (as in, did the founder borrow money from the startup, or vice versa)", KRUZE_DD, KRUZE_DD_F)
q(KT, "Salary schedule for all employees", KRUZE_DD, KRUZE_DD_F)
q(KT, "Company organizational chart", DOCSEND, DOCSEND_F)
q(KT, "List of company employees including title, salary, bonus potential, commissions, exempt or non-exempt status, and contact information", DOCSEND, DOCSEND_F)
q(KT, "Role coverage: Who owns product, engineering, sales, operations, and finance? Which missing role becomes urgent after the raise?", HF_CHECK, HF_CHECK_F)
q(KT, "One executive role remains open, with a credible owner and hiring plan.", HF_CHECK, HF_CHECK_F)
q(KT, "Founder bios, org chart with open roles, signed IP assignment for every contributor, stock plan and option pool summary", "https://www.papermark.com/blog/data-room-for-yc-startups", "papermark_com_blog_data_room_for_yc_startups.txt")
q(KT, "Meeting rest of the team . Sometimes VCs will meet folks other than the founders pre-term sheet, but sometimes they think the founders are enough, and meet the others during post-term sheet diligence.", SAASTR_DD, SAASTR_DD_F)
q(KT, "Many expensive lawsuits have arisen from former early employees who might have been promised stock or who had not vested their stock before they were terminated or quit.", "https://www.holloway.com/g/angel-investing/sections/legal-diligence-on-other-founder-board-of-directors-and-employee-issues", "holloway_com_g_angel_investing_sections_legal_diligence_on_other_founder_board_of_directors_and_empl.txt")
q(KT, "Make sure to ask about any founders or employees who are no longer with the company.", "https://www.holloway.com/g/angel-investing/sections/legal-diligence-on-other-founder-board-of-directors-and-employee-issues", "holloway_com_g_angel_investing_sections_legal_diligence_on_other_founder_board_of_directors_and_empl.txt")
q(KT, "Equal space for low-commitment advisors signals a thin core team", WAVEUP, WAVEUP_F)
q(KT, "Never list contractors or non-essential staff just to look bigger", WAVEUP, WAVEUP_F)
q(KT, "A capable engineer can still lead a team where nobody feels able to report a product problem.", HF_CULT, HF_CULT_F)
q(KT, "Which customer, use case, or product request are you deliberately saying no to right now, and why?", HF_RED, HF_RED_F)
q(KT, "Healthy co-founders disagree. What matters is whether they can make a decision, support it, and resolve tension without leaving the company stuck.", HF_RED, HF_RED_F)
q(KT, "Agreements with officers and directors", DOCSEND, DOCSEND_F)
q(KT, "A list of officers and directors.", COOLEY_LIST, COOLEY_LIST_F)

# ------------------------------------------------------------------ hiring plan
KRUZE_CF = "https://kruzeconsulting.com/blog/build-a-rolling-cash-forecast/"
KRUZE_CF_F = "kruzeconsulting_com_blog_build_a_rolling_cash_forecast.txt"
q(HP, "Headcount is often 60-80% of total burn. So if your forecast doesn’t model hiring clearly, it’s basically a guess.", KRUZE_CF, KRUZE_CF_F)
q(HP, "a rough rule of thumb for many U.S. companies is 1.25-1.4 times base salary for fully loaded cost, but your actual multiplier will depend on your benefits and locations.", KRUZE_CF, KRUZE_CF_F)
q(HP, "Build some slack into your model and assume most future hires start a month or two later than you would like.", KRUZE_CF, KRUZE_CF_F)
q(HP, "Projecting hiring plans for the next 3 years", KRUZE_DD, KRUZE_DD_F)
q(HP, "Headcount is the largest line item the new capital will fund, and the team folder is the place where you show investors exactly what they are paying for.", VISIBLE, VISIBLE_F)
q(HP, "Seed and Series A founders also need bios for the key team members, an org chart, and a hiring plan tied directly to the use of funds.", VISIBLE, VISIBLE_F)
q(HP, "A 12 to 18 month operating plan with assumptions, hiring, use of funds, and a downside case.", HF_CHECK, HF_CHECK_F)
q(HP, "Compare the answer with the roadmap, recent releases, pipeline, hiring plan, and how people actually spend their time.", HF_RED, HF_RED_F)
q(HP, "“Hire and grow” is not a financing plan.", HF_RED, HF_RED_F)
q(HP, "Reconcile current cash, monthly burn, planned hires, debt or other obligations, and a simple monthly forecast with the amount being raised.", HF_RED, HF_RED_F)
q(HP, "Likely pass when the cash and burn figures do not reconcile, the round does not fund a clear learning or value milestone, or the founders cannot explain a downside plan.", HF_RED, HF_RED_F)
q(HP, "Startups whose burn is too high relative to their growth will find it hard to fundraise.", "https://sacks.substack.com/p/the-burn-multiple-51a7e43cb200", "sacks_substack_com_p_the_burn_multiple_51a7e43cb200.txt")
q(HP, "A startup that over-burns is effectively claiming that its sales will be spring-loaded.", "https://sacks.substack.com/p/the-burn-multiple-51a7e43cb200", "sacks_substack_com_p_the_burn_multiple_51a7e43cb200.txt")
q(HP, "Issue: hiring aggressively just before fundraising. This increases your costs immediately, but your revenue probably won’t be affected for at least a few months.", "https://www.codingvc.com/common-startup-timing-mistakes-and-how-to-avoid-them", "codingvc_com_common_startup_timing_mistakes_and_how_to_avoid_them.txt")
q(HP, "You can’t just plan to add 3 salespeople or 3 engineers next month.", "https://www.codingvc.com/common-startup-timing-mistakes-and-how-to-avoid-them", "codingvc_com_common_startup_timing_mistakes_and_how_to_avoid_them.txt")
q(HP, "If you know what goals you have to hit for a Series A, then your seed funding should provide enough runway to reach those goals and have 3-5 months left over for fundraising.", "https://www.codingvc.com/common-startup-timing-mistakes-and-how-to-avoid-them", "codingvc_com_common_startup_timing_mistakes_and_how_to_avoid_them.txt")
q(HP, "the ‘average’ company in the dataset had 4 people on their team when they were founded, and 18 months later they had 25 people.", "https://writing.pointnine.com/p/off-to-a-flying-start-who-should", "writing_pointnine_com_p_off_to_a_flying_start_who_should.txt")
q(HP, "As a founder, however, please don’t think that in order to be successful you must have 25 people on your team 18 months after founding.", "https://writing.pointnine.com/p/off-to-a-flying-start-who-should", "writing_pointnine_com_p_off_to_a_flying_start_who_should.txt")
q(HP, "I look at burn against progress: a team that did a lot on a little earns real trust, and a team that burned a lot to produce very little earns uncompromising scrutiny.", "https://thedataroom.substack.com/p/how-a-vc-does-due-diligence-on-your-company", "web_thedataroom_substack_com_p_how_a_vc_does_due_diligence_on_your_company.txt")
q(HP, "The number of employees more than quadrupled from 90 in 2020 to around 400 in 2021.", "https://kjlabuz.substack.com/p/fast", "web_kjlabuz_substack_com_p_fast.txt")
q(HP, "Use a hiring plan to size the option pool.", "https://venturehacks.com/option-pool-shuffle", "venturehacks_com_option_pool_shuffle.txt")
q(HP, "Next, make a hiring plan for the next 12 months. Add up the options you need to give to the new hires.", "https://venturehacks.com/option-pool-shuffle", "venturehacks_com_option_pool_shuffle.txt")
q(HP, "Total cash cost per quarter: sum of all hired-or-active employees' cash compensation. Feeds burn rate.", "https://www.launchrock.com/library/expert-advice/hiring-plan", "launchrock_com_library_expert_advice_hiring_plan.txt")
q(HP, "Headcount, once added, becomes something else entirely: a fixed monthly commitment that runs quietly in the background.", "https://www.peoplematters.in/article/business/the-hidden-cost-of-rapid-hiring-in-startups-how-headcount-decisions-silently-destroy-runway-48328", "peoplematters_in_article_business_the_hidden_cost_of_rapid_hiring_in_startups_how_headcount_decision.txt")
p(HP, "Cooley GO, as summarized by Rework (a secondary source): build an option budget from the hires needed over roughly the next 12 to 18 months instead of accepting a percentage because an investor calls it standard.", "https://resources.rework.com/libraries/startup-terms/employee-option-pool", "resources_rework_com_libraries_startup_terms_employee_option_pool.txt")
p(HP, "Fast, as told in a newsletter post-mortem (secondary): burn doubled over two quarters of 2021 partly because headcount ballooned, against revenue of about $600,000 for the year.", "https://kjlabuz.substack.com/p/fast", "web_kjlabuz_substack_com_p_fast.txt")
p(HP, "Launchrock (vendor): a hiring plan lists, for each role, start date, level, total pay, department, reason for the role and dependencies such as 'after Series A closes'.", "https://www.launchrock.com/library/expert-advice/hiring-plan", "launchrock_com_library_expert_advice_hiring_plan.txt")

# ------------------------------------------------- employment, advisory, grants
HOLLOWAY = "https://www.holloway.com/g/angel-investing/sections/legal-diligence-on-other-founder-board-of-directors-and-employee-issues"
HOLLOWAY_F = "holloway_com_g_angel_investing_sections_legal_diligence_on_other_founder_board_of_directors_and_empl.txt"
CARTA_OPT = "https://carta.com/blog/issuing-options-mistakes/"
CARTA_OPT_F = "carta_com_blog_issuing_options_mistakes.txt"
ONLYCFO = "https://www.onlycfo.io/p/cap-table-nightmares"
ONLYCFO_F = "onlycfo_io_p_cap_table_nightmares.txt"
PEONY_A = "https://www.peony.ink/blog/series-a-data-room"
PEONY_A_F = "peony_ink_blog_series_a_data_room.txt"
q(EO, "By Series A, employment and advisory agreements with IP assignment and key-person retention terms become standard diligence asks.", VISIBLE, VISIBLE_F)
q(EO, "Current shareholder and optionee lists, including issuance dates and original issuance price.", COOLEY_LIST, COOLEY_LIST_F)
q(EO, "A list of any employees or consultants who have not signed Proprietary Information and Invention Agreements, including a list any periods of time where key employees or consultants performed services for the Company while not bound by such agreements.", COOLEY_LIST, COOLEY_LIST_F)
q(EO, "Copies of offer letters.", COOLEY_LIST, COOLEY_LIST_F)
q(EO, "Consulting contracts.", COOLEY_LIST, COOLEY_LIST_F)
q(EO, "Equity already promised to early employees, customers or consultants.", DOCSEND, DOCSEND_F)
q(EO, "Vesting schedules related to any issuances of stock or options", DOCSEND, DOCSEND_F)
q(EO, "Current cap table on a fully diluted basis, including issued shares, options, warrants, SAFEs, notes, side letters, and promised grants.", HF_CHECK, HF_CHECK_F)
q(EO, "Founder ownership and vesting, employee option capacity, and advisor grants.", HF_CHECK, HF_CHECK_F)
q(EO, "Incentives: What are the vesting terms, option pool, advisor grants, and consequences if a founder leaves?", HF_CHECK, HF_CHECK_F)
q(EO, "The board has to approve all stock option grants ahead of time, either at a board meeting or by unanimous written consent. If your board hasn’t approved an option grant, no options have actually been granted.", CARTA_OPT, CARTA_OPT_F)
q(EO, "To avail yourself of the 409A safe harbor with the IRS, you need to get a new 409A valuation every 12 months, or sooner if you have a material event or transaction, (like a new financing round).", CARTA_OPT, CARTA_OPT_F)
q(EO, "Phantom grants : promised but never board-approved.", ONLYCFO, ONLYCFO_F)
q(EO, "No board approval = no grant.", ONLYCFO, ONLYCFO_F)
q(EO, "A Series B company discovered, mid-diligence, that three engineers thought they had 1% each. The CEO had “promised it.” The board had not.", ONLYCFO, ONLYCFO_F)
q(EO, "If your strike price is below FMV, it’s a Section 409A violation.", ONLYCFO, ONLYCFO_F)
q(EO, "option grants promised in offer letters but never board-approved or issued (found years later, at exercise or exit)", "https://founderscpa.com/blog/common-startup-cap-table-mistakes", "founderscpa_com_blog_common_startup_cap_table_mistakes.txt")
q(EO, "83(b) elections missed on founder restricted stock (a thirty-day window with no cure, converting cheap early gains into ordinary income later)", "https://founderscpa.com/blog/common-startup-cap-table-mistakes", "founderscpa_com_blog_common_startup_cap_table_mistakes.txt")
q(EO, "The Code does not provide for a late 83(b) election.", "https://terms.law/insights/section-83b-election-when-founder-forgets.html", "terms_law_insights_section_83b_election_when_founder_forgets_html.txt")
q(EO, "You have 30 days after the date of the stock grant to file it.", "https://gust.com/blog/missing-the-83b-deadline-can-spell-disaster-for-founders/", "gust_com_blog_missing_the_83b_deadline_can_spell_disaster_for_founders.txt")
q(EO, "It is not uncommon for founders who try to do it themselves to not timely file 83(b) elections, fail to adopt bylaws, fail to execute stock purchase agreements at all, and other mishaps.", HOLLOWAY, HOLLOWAY_F)
q(EO, "All employees should have signed an offer letter or employment agreement, and also an IP assignment agreement and a confidentiality or non-disclosure agreement.", HOLLOWAY, HOLLOWAY_F)
q(EO, "Make sure to ask the entrepreneur who is an employee and who is a contractor.", HOLLOWAY, HOLLOWAY_F)
q(EO, "Founders should have similar agreements assigning their relevant work that was done before the startup was legally formed to the startup.", HOLLOWAY, HOLLOWAY_F)
q(EO, "Many expensive lawsuits have arisen from former early employees who might have been promised stock or who had not vested their stock before they were terminated or quit.", HOLLOWAY, HOLLOWAY_F)
q(EO, "Un-papered equity — a grant you promised a key hire or advisor with no signed agreement on file. It has to be papered before it can be counted.", PEONY_A, PEONY_A_F)
q(EO, "Missing IP assignments — founders, early employees, or contractors who never assigned their work to the company.", PEONY_A, PEONY_A_F)
q(EO, "Employment agreements, offer letters, and the option-grant records behind the pool.", PEONY_A, PEONY_A_F)
q(EO, "IP assignment. Every founder, employee, contractor, and friend-who-helped-for-a-weekend needs a signed agreement assigning their work to the company.", "https://www.papermark.com/blog/data-room-for-yc-startups", "papermark_com_blog_data_room_for_yc_startups.txt")
q(EO, "Misclassification of workers is one of the most common – and most costly – issues uncovered during due diligence.", "https://www.fisherphillips.com/en/news-insights/steps-for-built-to-sell-tech-startups-to-lock-down-employment-law-compliance.html", "fisherphillips_com_en_news_insights_steps_for_built_to_sell_tech_startups_to_lock_down_employment_la.txt")
q(EO, "Founder’s Stock is often subject to a vesting schedule.", "https://www.cooleygo.com/founder-basics-founders-stock/", "cooleygo_com_founder_basics_founders_stock.txt")
q(EO, "Under a typical vesting schedule, the stock vests in monthly or quarterly increments over four years", "https://www.cooleygo.com/founder-basics-founders-stock/", "cooleygo_com_founder_basics_founders_stock.txt")
q(EO, "The vesting schedule may be agreed to at the time of the Founders Stock is first issued, or may be imposed later as a condition of investment by outside investors.", "https://www.cooleygo.com/founder-basics-founders-stock/", "cooleygo_com_founder_basics_founders_stock.txt")
q(EO, "Venture capitalists require vesting as a condition to funding your company.", "https://assets.fenwick.com/legacy/FenwickDocuments/Start-up_Legal_Resource_Guide.pdf", "fenwick_start_up_legal_resource_guide.txt")
q(EO, "a common vesting schedule for an advisor is two years with a three-month cliff", "https://holloway.com/g/equity-compensation/sections/typical-startup-advisor-equity-levels", "holloway_com_g_equity_compensation_sections_typical_startup_advisor_equity_levels.txt")
q(EO, "Advisor grants also typically have a longer exercise window post termination of service, and will usually have single trigger acceleration on an acquisition", "https://holloway.com/g/equity-compensation/sections/typical-startup-advisor-equity-levels", "holloway_com_g_equity_compensation_sections_typical_startup_advisor_equity_levels.txt")
q(EO, "founder service agreements,", "https://help.seedlegals.com/en/data-room-how-it-can-enhance-your-funding-round", "help_seedlegals_com_en_data_room_how_it_can_enhance_your_funding_round.txt")
q(EO, "employment agreements for key team members,", "https://help.seedlegals.com/en/data-room-how-it-can-enhance-your-funding-round", "help_seedlegals_com_en_data_room_how_it_can_enhance_your_funding_round.txt")
q(EO, "Don’t let your investors determine the size of the option pool for you. Use a hiring plan to justify a small option pool, increase your share price, and increase your effective valuation.", "https://venturehacks.com/option-pool-shuffle", "venturehacks_com_option_pool_shuffle.txt")
q(EO, "Undocumented agreements: Verbal promises to advisors or early employees that aren't reflected in legal documentation", AIN, AIN_F)
q(EO, "Detailed cap tables are important because they give me insight into how the company's stakeholders might have shifted over time. For example, is there someone who owns equity but is no longer with the business?", "https://www.docsend.com/blog/4-types-of-documents-founders-must-have-in-their-fundraising-data-room-and-a-few-additional-tips/", "docsend_com_blog_4_types_of_documents_founders_must_have.txt")
q(KT, "There can often be an inclination to inflate titles of new hires in the very early stages of starting a business — it can be a cost-effective way to attract great candidates and can appear to quickly solve the issue of building out a leadership team. But in the medium term, there can be a price to pay for doing this: you can end up with a reasonably inexperienced leadership team that you can’t hire above because the existing team already hold C-suite titles.", "https://writing.pointnine.com/p/off-to-a-flying-start-who-should", "writing_pointnine_com_p_off_to_a_flying_start_who_should.txt")
p(EO, "Gust, Cake, terms.law and Launchrock agree on the rule (30 days from the grant date). Cake adds that a missed election 'frequently surfaces during due diligence at Series A or later'. terms.law, a law-firm memo, says the Treasury rules allow narrow, case-by-case relief that the IRS has granted only rarely.", "https://terms.law/insights/section-83b-election-when-founder-forgets.html", "terms_law_insights_section_83b_election_when_founder_forgets_html.txt")
p(EO, "Founder Institute FAST framework, as reproduced by the Holloway Guide: advisor grants run from 0.15 percent to 1.00 percent depending on the advisor's role and the company's stage.", "https://holloway.com/g/equity-compensation/sections/typical-startup-advisor-equity-levels", "holloway_com_g_equity_compensation_sections_typical_startup_advisor_equity_levels.txt")
p(EO, "Carta's issuing-options guide lists the usual option mistakes: wrong timing, no current 409A, no board approval, mixing up ISOs and NSOs, and untracked vesting.", CARTA_OPT, CARTA_OPT_F)

# ---------------------------------------------------- AI and data governance
WILLKIE = "https://www.willkie.com/publications/2025/09/optimizing-ai-investments-protecting-value-and-managing-risk-through-expert-diligence"
WILLKIE_F = "willkie_com_publications_2025_09_optimizing_ai_investments_protecting_value_and_managing_risk_throug.txt"
KATTEN = "https://katten.com/ai-deals-call-for-tailored-approach-to-address-hidden-risks"
KATTEN_F = "katten_com_ai_deals_call_for_tailored_approach_to_address_hidden_risks.txt"
SMAG_AI = "https://startupsmagazine.co.uk/the-new-due-diligence-why-vcs-are-walking-away-from-ai-startups-with-hidden-legal-risk"
SMAG_AI_F = "startupsmagazine_co_uk_the_new_due_diligence_why_vcs_are_walking_away_from_ai_startups_with_hidden_l.txt"
PEONY_AI = "https://www.peony.ink/downloads/ai-due-diligence-checklist.pdf"
PEONY_AI_F = "peony_ink_downloads_ai_due_diligence_checklist_pdf.txt"
AIB = "https://aibusiness.vc/vc/ai-startup-due-diligence-checklist-2026"
AIB_F = "aibusiness_vc_vc_ai_startup_due_diligence_checklist_2026.txt"
INNOV = "https://theinnovationattorney.substack.com/p/what-ai-startups-should-document"
INNOV_F = "theinnovationattorney_substack_com_p_what_ai_startups_should_document.txt"
GIBSON = "https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/"
GIBSON_F = "gibsondunn_com_eu_ai_act_omnibus_agreement_postponed_high_risk_deadlines_and_other_key_changes.txt"
q(AI, "AI/ML and data governance (New for 2026).", DOCSEND, DOCSEND_F)
q(AI, "AI model documentation: Architecture, training methodologies, performance metrics, and validation processes", DOCSEND, DOCSEND_F)
q(AI, "Training data provenance: Documentation of data sources, licensing, and rights to use training data", DOCSEND, DOCSEND_F)
q(AI, "Third-party AI services: Agreements with AI service providers (OpenAI, Anthropic, Google, etc.) and associated terms", DOCSEND, DOCSEND_F)
q(AI, "Model security: Safeguards against model theft, adversarial attacks, and prompt injection vulnerabilities", DOCSEND, DOCSEND_F)
q(AI, "Regulatory preparedness: Documentation showing awareness of and preparation for emerging AI regulations.", DOCSEND, DOCSEND_F)
q(AI, "The only thing standing between you and the investor's money is the due diligence process.", DOCSEND, DOCSEND_F)
q(AI, "Every AI tool is trained on data, therefore we need to understand where an AI company obtains the data it uses to develop and train its tools, whether from its own customers or other collection methods, or from a third-party provider, and whether it has requisite legal authority to use that data for training purposes.", WILLKIE, WILLKIE_F)
q(AI, "Where it subcontracts out some or all of the operation or development of its tools (for example, if its tool is built on a large-language model), an analysis is required to determine whether the rights, limitations, and obligations in the applicable contracts align with the contractual rights granted by the sources of the data.", WILLKIE, WILLKIE_F)
q(AI, "Copyright and database-rights risks should be addressed expressly where training or fine-tuning relies on scraped, licensed or customer-provided data.", KATTEN, KATTEN_F)
q(AI, "A buyer who inherits a model trained on contested data may also acquire significant latent liability.", KATTEN, KATTEN_F)
q(AI, "“We used publicly available data” is no longer an answer; it is a red flag", SMAG_AI, SMAG_AI_F)
q(AI, "Compliance evidence at seed, not Series B. SOC 2 progress and AI bias audits, once growth-stage concerns, are now appearing in seed-stage checklists.", SMAG_AI, SMAG_AI_F)
q(AI, "Request a per-dataset training-data manifest: source, acquisition date, license terms, intended-use scope, licensee-of-record.", PEONY_AI, PEONY_AI_F)
q(AI, "Investors ask where training or context data originates, what rights are granted by customers, and what restrictions apply to model usage.", AIB, AIB_F)
q(AI, "If you depend on one model provider today, say so clearly, explain why, and show the path to multi-provider resilience.", AIB, AIB_F)
q(AI, "Investors are not looking for perfection.", AIB, AIB_F)
q(AI, "A training data audit means producing a list of every source, a license or receipt for each, and a note on where the scraped and public domain material sits.", INNOV, INNOV_F)
q(AI, "Dependencies: Which cloud, model, platform, supplier, manufacturer, or license can change cost or access?", HF_CHECK, HF_CHECK_F)
q(AI, "For security, scope questions to the data and promises involved.", HF_CHECK, HF_CHECK_F)
q(AI, "A company selling into healthcare, finance, government, or large enterprises may need specialist review and evidence that matches its claims.", HF_CHECK, HF_CHECK_F)
q(AI, "At seed, add retention, unit economics, go-to-market (GTM) repeatability, hiring, security, contracts, and a fuller financial review.", HF_CHECK, HF_CHECK_F)
q(AI, "2 August 2026 remains an active compliance date. The Article 50 transparency obligations for AI systems largely remain on the original schedule.", GIBSON, GIBSON_F)
q(AI, "These changes only take legal effect upon formal adoption and publication of the Omnibus in the Official Journal, expected before 2 August 2026.", GIBSON, GIBSON_F)
q(AI, "High-risk obligations for stand-alone Annex III systems are deferred to 2 December 2027", GIBSON, GIBSON_F)
q(AI, "calls containing AI-generated voices are subject to consent requirements imposed on “artificial or prerecorded voices” under the TCPA.", "https://orrick.com/Insights/2024/02/Did-the-FCC-Really-Ban-AI-Generated-Voice-Calls-No-But-Restrictions-Apply", "orrick_com_Insights_2024_02_Did_the_FCC_Really_Ban_AI_Generated_Voice_Calls_No_But_Restrictions_Appl.txt")
q(AI, "Algorithmic disgorgement is the process in which illegally obtained data is removed from an AI model, and the destruction of any models or algorithms built using such data.", "https://www.lathropgpm.com/insights/artificial-intelligence-and-algorithmic-disgorgement/", "lathropgpm_com_insights_artificial_intelligence_and_algorithmic_disgorgement.txt")
q(AI, "On July 20, 2026, U.S. District Judge Araceli Martínez-Olguín of the Northern District of California granted final approval of the class action settlement in Bartz v. Anthropic PBC", "https://pearlcohen.com/federal-court-approves-1-5-billion-anthropic-copyright-settlement-largest-in-history", "pearlcohen_com_federal_court_approves_1_5_billion_anthropic_copyright_settlement_largest_in_history.txt")
q(AI, "Anthropic agreed to pay $1.5 billion plus interest to a class of copyright owners whose works were allegedly torrented and commercially exploited from pirated datasets", "https://pearlcohen.com/federal-court-approves-1-5-billion-anthropic-copyright-settlement-largest-in-history", "pearlcohen_com_federal_court_approves_1_5_billion_anthropic_copyright_settlement_largest_in_history.txt")
q(AI, "The court granted Google’s motion to dismiss and found that Plaintiff’s CIPA claim was barred by section 631’s exemption from liability for telephone companies and their agents.", "https://www.globalpolicywatch.com/2024/07/california-federal-court-dismisses-complaint-accusing-google-of-wiretapping-customer-service-calls/", "globalpolicywatch_com_2024_07_california_federal_court_dismisses_complaint_accusing_google_of_wireta.txt")
p(AI, "Search note: I found no law-firm or venture-firm checklist that sets AI governance documents by stage (seed or Series A). The sources are the DocSend checklist (no stages), a law-firm investor note (Willkie), an M&A note (Katten), journalism and vendor guides. Treat the stage calls in this guide as judgment.", DOCSEND, DOCSEND_F)
p(AI, "Thomson Reuters v. Ross Intelligence (February 2025) is described by a law firm (Revera) as one of the first major rulings to treat training on protected content as infringement, which raised the weight of training-data provenance.", "https://www.revera.legal/?p=8249", "revera_legal_p_8249.txt")
p(AI, "Everalbum, Kurbo/WW, Ring and Edmodo: the FTC has required deletion of models or algorithms built on data collected without the right consent (Lathrop GPM summary of the orders).", "https://www.lathropgpm.com/insights/artificial-intelligence-and-algorithmic-disgorgement/", "lathropgpm_com_insights_artificial_intelligence_and_algorithmic_disgorgement.txt")
p(AI, "Judge Alsup held that training on purchased books was fair use and that building a central library from pirated copies was not; the later $1.5 billion settlement covers the pirated works (Pearl Cohen; Jurist).", "https://pearlcohen.com/federal-court-approves-1-5-billion-anthropic-copyright-settlement-largest-in-history", "pearlcohen_com_federal_court_approves_1_5_billion_anthropic_copyright_settlement_largest_in_history.txt")
p(AI, "Ambriz v. Google: a customer sued over Google's contact-centre AI listening to calls to Verizon. The court dismissed the claim in June 2024 with leave to amend, on the ground that Google acted as Verizon's agent. Later history was not checked.", "https://www.globalpolicywatch.com/2024/07/california-federal-court-dismisses-complaint-accusing-google-of-wiretapping-customer-service-calls/", "globalpolicywatch_com_2024_07_california_federal_court_dismisses_complaint_accusing_google_of_wireta.txt")

# added after the first draft
SAASTR_RF = "https://www.saastr.com/dear-saastr-what-are-the-top-red-flags-for-vcs-when-deciding-to-invest-in-a-sstartup/"
SAASTR_RF_F = "saastr_com_dear_saastr_what_are_the_top_red_flags_for_vcs_when_deciding_to_invest_in_a_sstartup.txt"
q(FB, "The concern is a material claim that keeps changing after you define the terms.", HF_RED, HF_RED_F)
q(FB, "If a VC hears negative feedback about the founder or team during backchannel reference checks, it’s often game over.", SAASTR_RF, SAASTR_RF_F)
q(FB, "The moment investors uncover undisclosed litigation or missing IP assignments, the deal either dies or the valuation gets renegotiated.", AIN, AIN_F)
q(FB, "The best founders often have personal experience with the pain point.", HF_FRAME, HF_FRAME_F)

# founder-bios guide, second pass
q(FB, "At the earliest stages, the team carries unusual weight because the product and market approach may change.", HF_CHECK, HF_CHECK_F)
q(FB, "Formal reference calls", SAASTR_DD, SAASTR_DD_F)
q(FB, "Full background checks", SAASTR_DD, SAASTR_DD_F)
q(FB, "The deep dives often come post term-sheet these days", SAASTR_DD, SAASTR_DD_F)
q(FB, "6 years as a radiology tech at Mount Sinai, read 40,000+ scans", CAUSO, CAUSO_F)
q(FB, "Passionate about using AI to transform healthcare. Previously at a major hospital.", CAUSO, CAUSO_F)
q(FB, "I don't know why these logos are here", WAVEUP, WAVEUP_F)
q(FB, "Most funds I spoke with only do reference calls at the end of the process", FORM, FORM_F)
q(FB, "A list of officers and directors. If any officers are not currently devoting 100% of their business time to the Company, please note them on this list.", COOLEY_LIST, COOLEY_LIST_F)
q(FB, "Intellectual honesty.", HF_RED, HF_RED_F)

# key-team guide, second pass
HOLLOWAY_T = "https://www.holloway.com/g/angel-investing/sections/legal-diligence-on-other-founder-board-of-directors-and-employee-issues"
q(KT, "beware of companies where the majority of the team working at the office are classified as contractors.", HOLLOWAY_T, HOLLOWAY_F)
q(KT, "Legal due diligence. Are there ex-founder issues? Cap table issues? Do the founders have enough unvested stock left? Are there any issues with founders that have left the company?", SAASTR_DD, SAASTR_DD_F)
q(KT, "Look out for founders who intend to use almost the entire proceeds of the offering to pay themselves back for foregone salaries or unreimbursed expenses or other accrued liabilities", HOLLOWAY_T, HOLLOWAY_F)
q(KT, "To make this slightly easier to remember, the average company hires the following people in the first 18 months:", "https://writing.pointnine.com/p/off-to-a-flying-start-who-should", "writing_pointnine_com_p_off_to_a_flying_start_who_should.txt")
q(KT, "The concern is a material claim that keeps changing after you define the terms.", HF_RED, HF_RED_F)
p(KT, "Point Nine guest study of 15 European B2B software companies that later raised large Series A rounds: the average company hired 2 or 3 founders, 1 to 2 C-levels, 1 to 2 VPs or Directors, 1 to 2 Heads of, 1 to 2 Leads and 18 individual contributors in the first 18 months. The sample picked winners, so it describes success, not a norm.", "https://writing.pointnine.com/p/off-to-a-flying-start-who-should", "writing_pointnine_com_p_off_to_a_flying_start_who_should.txt")
p(KT, "Kruze lists the org chart, a salary schedule for all employees, a three-year hiring plan and any transactions with executives together as the HR items in a venture diligence request.", KRUZE_DD, KRUZE_DD_F)
p(KT, "SeedLegals (UK equity platform): lead investors often ask for founder service agreements and employment agreements for key team members.", "https://help.seedlegals.com/en/data-room-how-it-can-enhance-your-funding-round", "help_seedlegals_com_en_data_room_how_it_can_enhance_your_funding_round.txt")

q(KT, "Corporate records and documents", DOCSEND, DOCSEND_F)
q(KT, "Org chart and/or team bios", A16Z, A16Z_F)
q(KT, "only advisors with real skin in the game", WAVEUP, WAVEUP_F)

# hiring-plan guide, second pass
LAUNCH = "https://www.launchrock.com/library/expert-advice/hiring-plan"
LAUNCH_F = "launchrock_com_library_expert_advice_hiring_plan.txt"
q(HP, "Hiring plan disconnected from financials : company has a hiring plan but doesn't tie it to burn-rate or runway models. Plan and financial model diverge.", LAUNCH, LAUNCH_F)
q(HP, "Are we actually hiring at the pace we modeled?", KRUZE_CF, KRUZE_CF_F)
q(HP, "what would you cut first if progress is slower?", HF_RED, HF_RED_F)
q(HP, "hire after Series A closes.", LAUNCH, LAUNCH_F)
q(HP, "A hiring plan is a structured roadmap of roles to fill over a defined period (typically 12-18 months), with role-by-role timing, costs, and dependencies.", LAUNCH, LAUNCH_F)
q(HP, "Charitably, $600,000 in annual revenue covers the salary of five junior software engineers in the United States.", "https://kjlabuz.substack.com/p/fast", "web_kjlabuz_substack_com_p_fast.txt")
q(HP, "Almost every founder regrets using capital to keep a high-burn rate engine going that isn’t scaling rapidly.", "https://www.saastr.com/every-top-founder-ever-i-should-have-acted-on-bad-trends-earlier/", "web_saastr_com_every_top_founder_ever_i_should_have_acted_on_bad_trends_earlier.txt")

# The Data Room (Jonathan Hua), copied into three more folders
HUA = "https://thedataroom.substack.com/p/how-a-vc-does-due-diligence-on-your-company"
HUA_F = "web_thedataroom_substack_com_p_how_a_vc_does_due_diligence_on_your_company.txt"
q(FB, "I look for founder-market fit: the unfair edge or lived experience that makes these specific people right for this specific problem, not just qualified in general.", HUA, HUA_F)
q(FB, "Their resume only tells me what they’ve already done, while adversity tells me what they’ll do when things inevitably get tough.", HUA, HUA_F)
q(FB, "Founder pitfall: only offering references who are direct beneficiaries of your success, an investor, a close friend, a subordinate. I always ask for at least one reference outside the people you’d naturally choose.", HUA, HUA_F)
q(FB, "References that sound like they’re reading from a script you gave them.", HUA, HUA_F)
q(KT, "Key personnel with almost no equity , like a VP of Engineering holding 0.1% fully diluted at a company raising a Series C, is a huge retention risk I’ll price into the term sheet whether the founder addresses it or not.", HUA, HUA_F)
q(KT, "Advisor equity that never got attached to deliverables , such as eight advisors holding 2% each with vesting schedules that already expired, signals a judgment problem more than a cap table problem.", HUA, HUA_F)
q(EO, "Key personnel with almost no equity , like a VP of Engineering holding 0.1% fully diluted at a company raising a Series C, is a huge retention risk I’ll price into the term sheet whether the founder addresses it or not.", HUA, HUA_F)
q(EO, "Advisor equity that never got attached to deliverables , such as eight advisors holding 2% each with vesting schedules that already expired, signals a judgment problem more than a cap table problem.", HUA, HUA_F)
q(EO, "a large advisor grant nobody negotiated hard on", HUA, HUA_F)
q(EO, "A deck that claims 55% founder ownership and a cap table that shows 48% fully diluted registers as the first real crack in credibility, and is far more damaging than a simple rounding error would be.", HUA, HUA_F)

# employment, advisory, grants: second pass
CAKE = "https://www.cakeequity.com/guides/83b-election-reminder-equity"
CAKE_F = "cakeequity_com_guides_83b_election_reminder_equity.txt"
FISHER = "https://www.fisherphillips.com/en/news-insights/steps-for-built-to-sell-tech-startups-to-lock-down-employment-law-compliance.html"
FISHER_F = "fisherphillips_com_en_news_insights_steps_for_built_to_sell_tech_startups_to_lock_down_employment_la.txt"
q(EO, "the issue frequently surfaces during due diligence at Series A or later.", CAKE, CAKE_F)
q(EO, "Provide every employee with a signed offer letter outlining title, salary, at-will status, start date, and any bonus or equity offers.", FISHER, FISHER_F)
q(EO, "Unclear or undocumented equity promises can derail M&A deals and dilute your equity.", FISHER, FISHER_F)
q(EO, "The certified-mail return receipt is the documentary evidence I would not skip.", "https://terms.law/insights/section-83b-election-when-founder-forgets.html", "terms_law_insights_section_83b_election_when_founder_forgets_html.txt")
q(EO, "A clean, single-source-of-truth cap table is the difference between a smooth raise and a nine-figure haircut.", ONLYCFO, ONLYCFO_F)
q(EO, "Multiple truths = no truth. If two versions exist, investors assume there’s a third one with even scarier numbers.", ONLYCFO, ONLYCFO_F)
q(EO, "The board can only grant stock options at the current fair market value (FMV), so simply granting the stock options later isn’t a solution when the FMV increased 100x.", ONLYCFO, ONLYCFO_F)
q(EO, "ISOs can only be issued to employees, whereas NSOs can be issued to employees and advisors , directors, consultants, and contractors.", CARTA_OPT, CARTA_OPT_F)
q(EO, "Check that a company is not carrying accrued or deferred salaries on its balance sheet.", HOLLOWAY, HOLLOWAY_F)
q(EO, "The most consequential gap in this folder at any stage is the IP assignment from former contractors or employees.", VISIBLE, VISIBLE_F)
q(EO, "This is the single most common finding at Series A and the easiest to fix at seed", "https://www.papermark.com/blog/data-room-for-yc-startups", "papermark_com_blog_data_room_for_yc_startups.txt")

q(EO, "Equity grant records and option pool", VISIBLE, VISIBLE_F)
q(EO, "Founder equity purchase and vesting records, plus approvals for issuances", HF_CHECK, HF_CHECK_F)
q(EO, "stock plan and grant ledger", "https://www.papermark.com/blog/data-room-for-yc-startups", "papermark_com_blog_data_room_for_yc_startups.txt")
q(EO, "Shareholder information and agreements", DOCSEND, DOCSEND_F)
q(EO, "Equity grants", DOCSEND, DOCSEND_F)
q(EO, "copies of Section 83(b) elections the founders filed with the IRS, if the founders’ shares were subject to vesting", HOLLOWAY, HOLLOWAY_F)
q(EO, "From the diligence trenches, in descending frequency", "https://founderscpa.com/blog/common-startup-cap-table-mistakes", "founderscpa_com_blog_common_startup_cap_table_mistakes.txt")

# AI guide, second pass
q(AI, "including the use of shortcuts or vaporware that would undermine both the investment and an investor’s credibility in the market.", WILLKIE, WILLKIE_F)
q(AI, "Investors should also inquire about specific protections for inputs and outputs against leakage and adversarial attacks.", WILLKIE, WILLKIE_F)
q(AI, "A founder who can show a signed license agreement for every commercial dataset, and a documented fair use analysis for everything else, walks into due diligence with an answer instead of an apology.", INNOV, INNOV_F)
q(AI, "GPL licensed code inside an AI pipeline creates a contamination risk", INNOV, INNOV_F)
q(AI, "You need clear policy, consistent contract templates, and documented exceptions.", AIB, AIB_F)
q(AI, "If your customer contracts are silent, your investors will not be", SMAG_AI, SMAG_AI_F)
q(AI, "A documented yes scores 1 (Red) on the Data Layer regardless of how clean the other four tests are, and it is the most quantifiable downside in AI diligence.", PEONY_AI, PEONY_AI_F)
q(AI, "Reject any manifest line reading 'publicly available web data' with no further documentation, and trace it back to a named source instead.", PEONY_AI, PEONY_AI_F)
q(AI, "including the requirement to disclose to users when they are interacting with AI systems, remain unaffected", GIBSON, GIBSON_F)
q(AI, "Diligence should examine what data the target holds; how it was collected; whether it includes personal data; whether it was obtained under contractual restrictions; and whether it can be used for model training, fine-tuning, validation, product improvement and postclosing integration.", KATTEN, KATTEN_F)
q(AI, "explicitly does not release claims related to AI outputs or future conduct.", "https://pearlcohen.com/federal-court-approves-1-5-billion-anthropic-copyright-settlement-largest-in-history", "pearlcohen_com_federal_court_approves_1_5_billion_anthropic_copyright_settlement_largest_in_history.txt")
q(AI, "Willkie is a trusted adviser to global investors at the cutting edge of the AI frontier.", WILLKIE, WILLKIE_F)
q(AI, "AI/ML and data governance", DOCSEND, DOCSEND_F)
