# Hiring plan and future org

Document guide for Tricorder's scans, checklist and memo. Written 2026-10-22. Sources are saved under [raw/hiring-plan-and-future-org/](raw/hiring-plan-and-future-org/). Quotes are checked word for word against the saved pages by [build_quotes_people.py](raw/_people_tools/build_quotes_people.py); results are in [quotes_people.csv](quotes_people.csv). Facts about the Hollis Voice room come from [room_facts_people.py](raw/hiring-plan-and-future-org/room_facts_people.py) and its output [room_facts_people.out.txt](raw/hiring-plan-and-future-org/room_facts_people.out.txt).

## What it is

A list of the people the company plans to add: one row per hire with title, department, start date and pay, and sometimes the equity grant. A hiring-plan guide from Startups.com describes it as "a structured roadmap of roles to fill over a defined period (typically 12-18 months), with role-by-role timing, costs, and dependencies." ([Startups.com via Launchrock, vendor view](https://www.launchrock.com/library/expert-advice/hiring-plan)). Kruze, an accounting firm, asks for plans "for the next 3 years" ([Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/)).

The CEO or the finance lead prepares it. It usually arrives as a tab in the financial model, a CSV, or a slide on use of funds, drawn as the future-state org chart.

## At seed and at Series A

The research table marks it lighter at pre-seed and expected at seed and Series A. See [the 30-document table](../20261022.02_research/research_data_room.md).

- **Seed.** A short list tied to what the round must prove. Hustle Fund wants "A 12 to 18 month operating plan with assumptions, hiring, use of funds, and a downside case." ([Hustle Fund checklist](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)). Visible: seed founders need "a hiring plan tied directly to the use of funds" ([Visible, vendor](https://visible.vc/blog/what-to-include-in-your-data-room/)).
- **Series A.** A role-by-role grid that feeds payroll, burn, runway and the option pool. Visible calls it the document that shows investors "exactly what they are paying for": "Headcount is the largest line item the new capital will fund, and the team folder is the place where you show investors exactly what they are paying for."
- **What changes.** At seed the question is whether the plan is sensible. At Series A the question is whether the model pays for every hire in the plan.

## What a first pass checks

1. Does the model's payroll include every hire in the plan, at the plan's start month and pay?
2. Is the load factor (taxes and benefits on top of base pay) fair? Kruze cites a rule of thumb: "a rough rule of thumb for many U.S. companies is 1.25-1.4 times base salary for fully loaded cost, but your actual multiplier will depend on your benefits and locations." ([Kruze, rolling cash forecast](https://kruzeconsulting.com/blog/build-a-rolling-cash-forecast/)).
3. Are start dates realistic? Kruze: "Build some slack into your model and assume most future hires start a month or two later than you would like."
4. What runway follows from cash, the raise and the whole plan, and does the deck say the same?
5. Does each hire serve a milestone? Hustle Fund asks "what would you cut first if progress is slower?" ([Hustle Fund red-flag guide](https://www.hustlefund.vc/post/angel-squad-red-flags-in-startup-founders-that-experienced-investors-never-ignore)).
6. Does the plan hire hard just before the raise? Leo Polovets, writing on his Coding VC blog in 2016, lists "Issue: hiring aggressively just before fundraising. This increases your costs immediately, but your revenue probably won’t be affected for at least a few months." ([Coding VC, Polovets](https://www.codingvc.com/common-startup-timing-mistakes-and-how-to-avoid-them)).
7. Is there an equity grant for each hire, and does the option pool cover them?
8. Has the company hit its earlier hiring plans? Kruze's forecast review asks "Are we actually hiring at the pace we modeled?"

## Green flags

- **The model pays for the whole plan.** Kruze: "Headcount is often 60-80% of total burn. So if your forecast doesn’t model hiring clearly, it’s basically a guess." A model whose payroll rebuilds from the plan is the opposite of a guess.
- **Start dates with slack, and triggers written down.** The Startups.com guide says to write a dependency on each role, such as "hire after Series A closes." ([Launchrock](https://www.launchrock.com/library/expert-advice/hiring-plan)).
- **A downside case.** Hustle Fund's checklist asks for "a downside case" and its red-flag guide asks what the founders would cut first.
- **An option budget built from the plan.** Venture Hacks: "Use a hiring plan to size the option pool." ([Venture Hacks](https://venturehacks.com/option-pool-shuffle)). Rework, summarising Cooley GO, says the same ([Rework, secondary](https://resources.rework.com/libraries/startup-terms/employee-option-pool)).
- **Hiring that stays tied to progress.** Jonathan Hua, a former early-stage investor at SVG Ventures-THRIVE and Scrum Ventures, wrote in his newsletter: "I look at burn against progress: a team that did a lot on a little earns real trust, and a team that burned a lot to produce very little earns uncompromising scrutiny." ([The Data Room, Hua, Sep 2026](https://thedataroom.substack.com/p/how-a-vc-does-due-diligence-on-your-company)).

## Red flags and pitfalls

**Common**

- **A plan that is not tied to the model.** The Startups.com guide names it: "Hiring plan disconnected from financials : company has a hiring plan but doesn't tie it to burn-rate or runway models. Plan and financial model diverge." ([Launchrock](https://www.launchrock.com/library/expert-advice/hiring-plan)). Hustle Fund's rule is stricter: "Likely pass when the cash and burn figures do not reconcile, the round does not fund a clear learning or value milestone, or the founders cannot explain a downside plan."
- **"Hire and grow" with no milestone.** Hustle Fund: "“Hire and grow” is not a financing plan."
- **Hires that all start next month.** Polovets: "You can’t just plan to add 3 salespeople or 3 engineers next month."
- **Base pay with no load.** Kruze, above.
- **Burn out of line with growth.** David Sacks wrote, in his April 2020 post on the burn multiple, "Startups whose burn is too high relative to their growth will find it hard to fundraise." and "A startup that over-burns is effectively claiming that its sales will be spring-loaded." ([Sacks, The Burn Multiple](https://sacks.substack.com/p/the-burn-multiple-51a7e43cb200)). The page's rule-of-thumb table did not survive in the saved text, so no multiple is quoted here.
- **Headcount as a commitment that is easy to forget.** "Headcount, once added, becomes something else entirely: a fixed monthly commitment that runs quietly in the background." ([People Matters, a trade publication](https://www.peoplematters.in/article/business/the-hidden-cost-of-rapid-hiring-in-startups-how-headcount-decisions-silently-destroy-runway-48328)).
- **No link between the plan and the option pool.** Venture Hacks and Rework, above.

**Rare but serious**

- **Hiring that outruns revenue by a wide margin.** A newsletter post-mortem of the startup Fast says "The number of employees more than quadrupled from 90 in 2020 to around 400 in 2021." and, of the revenue, "Charitably, $600,000 in annual revenue covers the salary of five junior software engineers in the United States." ([Fast post-mortem, secondary](https://kjlabuz.substack.com/p/fast)). It is one outside account, so treat it as a story, not a measurement.
- **A founder who regrets high burn.** A SaaStr post by Jason Lemkin: "Almost every founder regrets using capital to keep a high-burn rate engine going that isn’t scaling rapidly." ([SaaStr](https://www.saastr.com/every-top-founder-ever-i-should-have-acted-on-bad-trends-earlier/)).
- **Runway that ends before the next raise.** Polovets: "If you know what goals you have to hit for a Series A, then your seed funding should provide enough runway to reach those goals and have 3-5 months left over for fundraising."

**Pace is context, not a test.** Point Nine's guest study of 15 European software companies that later raised large rounds found the average company went from 4 people to 25 in 18 months, and the author adds "please don’t think that in order to be successful you must have 25 people on your team 18 months after founding." ([Point Nine, guest post](https://writing.pointnine.com/p/off-to-a-flying-start-who-should)). The sample picked winners, so it says nothing about how fast a normal company should hire.

## How Tricorder checks it

**What a script can check**

- `payroll_from_hiring_plan_and_rerun_cash`: already defined and set to run on Saturday ([FRAMEWORKS 1.4](../../ongoing/FRAMEWORKS.md)). Formula in that entry: `loaded_monthly_cost(hire) = base_pay × load_factor ÷ 12`, summed from each start month, then the cash roll is rerun and compared with the model's runway and the deck.
- C25, contractors counted in headcount and burn: [FRAMEWORKS 1.12 accounting mislabels](../../ongoing/FRAMEWORKS.md), after Saturday.
- Proposed `start_date_slip_scenario`: rerun the cash roll with every start date moved one month and two months later (Kruze), and show runway for the three cases. Formula: `runway(slip) = last month t with cash(t) > 0`, for slip in 0, 1, 2.
- Proposed `load_factor_in_band`: show whether the model's factor sits between 1.25 and 1.4. Context only.
- Proposed `headcount_chain`: `headcount_after_hire` rises by one per row, and its last value equals the deck's staff-after-hiring number.
- Proposed `dept_counts_match_deck`: department counts in the plan equal the deck's hiring slide.
- Proposed `pool_covers_plan`: `unissued_pool_shares ≥ SUM(grant_shares per planned hire)`. It needs an equity column; without one the check writes a gap.
- Proposed `hires_before_raise`: count the hires that start before the month the raise lands, to show how much hiring is paid from existing cash.

**What needs a model to read**

- Start dates, pay and role notes that sit in text, and matching a plan role to the P&L line that should carry it ([FRAMEWORKS 1.4](../../ongoing/FRAMEWORKS.md)).
- Reading the deck's use-of-funds and hiring slides, quoting the number and the slide.
- It must quote each figure it relies on, and it must not suggest a motive for a mismatch.

**What Tricorder cannot check (leave to the operator)**

- Whether any role is in recruiting, or has an offer out.
- Whether pay levels match the market for the city and the role. That needs a pay benchmark Tricorder does not hold.
- The true loaded cost. Only the company's payroll provider shows it.
- A call with the CEO about earlier hiring misses.

## Readout pieces and checklist items

- **Burn and runway** piece (`hires`, `payroll_monthly`, `runway_months`), **team** (`headcount`) and **the pitch itself** (use of funds).
- Checklist items ([CHECKLIST](../../ongoing/CHECKLIST.md)): C22 (hiring plan and future org), C24 (payroll rebuilt from the plan), C25 (contractors counted), C29 (current monthly burn and bank balance), C93 (the company's open roles against the plan, from outside). C22 and C24 are checked by FRAMEWORKS 1.4.

## If it is missing

- **Pre-seed:** not a gap.
- **Seed:** a gap if the model's payroll grows. Without a plan, Tricorder cannot rebuild payroll, so the burn and runway piece shows "not enough in the room" for the hiring part. It is a question, not a red flag.
- **Series A:** the same gap, and a stronger one. Entry 1.4 cannot run, and the deck's runway stands unchecked.
- **Ask-list line:** "Please send the hiring plan for the next 12 to 18 months: role, department, start date, base pay and equity grant for each planned hire."

## In the Hollis Voice room

- **In the room, twice.** `05_team/hiring_plan.csv` has 24 rows with `hire_id`, `role`, `department`, `start_date`, `base_salary_usd` and `headcount_after_hire`. The model's `Hiring_Plan` tab lists the first 8. Deck slide 12 gives the department split. The department counts in the CSV equal the deck's split (10, 5, 3, 3, 1 and 2), and they total 24 ([room_facts_people.out.txt](raw/hiring-plan-and-future-org/room_facts_people.out.txt)).
- **Planted red flag PF4: burn and runway do not match the hiring plan.** The model pays for 8 of the 24 hires. The deck and model say 37 months of runway. Rebuilt from all 24 hires it is 19 months. Average net burn over the first 12 plan months is $374,462 in the model and $480,062 rebuilt ([FRAMEWORKS 1.4](../../ongoing/FRAMEWORKS.md); `answer_key.json`). This is the research's soft spot: no published list names it as a flag, so the check is built from Kruze's method.
- **Other facts from the script.** Base pay across the 24 planned hires sums to $3,960,000 a year. The first start is 2026-10-01 and the last 2027-09-08. Six hires (H01 to H06) start before the Series A cash lands in 2027-01.
- **A gap the plan leaves.** The CSV has no equity column, so `pool_covers_plan` cannot run. The cap table holds 1,034,000 unissued option shares, which is 43,083 per planned hire if split evenly. The room does not say what each hire is meant to receive.
- **Green flag nearby.** Staff after hiring, 41, agrees between deck slide 12 and the last row of the plan (`answer_key.json`, GF3).

## Sources

Each page is saved in [raw/hiring-plan-and-future-org/](raw/hiring-plan-and-future-org/). Vendor views are marked.

- [Kruze, build a rolling cash forecast](https://kruzeconsulting.com/blog/build-a-rolling-cash-forecast/) (accounting firm) | [saved](raw/hiring-plan-and-future-org/kruzeconsulting_com_blog_build_a_rolling_cash_forecast.txt)
- [Kruze, VC due diligence checklists](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/) | [saved](raw/hiring-plan-and-future-org/kruzeconsulting_com_what_are_examples_of_vc_due_diligence_check_lists.txt)
- [Visible, what to include in your data room](https://visible.vc/blog/what-to-include-in-your-data-room/) (vendor) | [saved](raw/hiring-plan-and-future-org/visible_vc_blog_what_to_include_in_your_data_room.txt)
- [Hustle Fund, angel investing due diligence checklist](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step) | [saved](raw/hiring-plan-and-future-org/hustlefund_vc_post_angel_squad_angel_investing_due_diligence_checklist_step_by_step.txt)
- [Hustle Fund, startup red flags](https://www.hustlefund.vc/post/angel-squad-red-flags-in-startup-founders-that-experienced-investors-never-ignore) | [saved](raw/hiring-plan-and-future-org/web_hustlefund_vc_post_angel_squad_red_flags_in_startup_founders_that_experienced_investors_never_ignore.txt)
- [David Sacks, The Burn Multiple](https://sacks.substack.com/p/the-burn-multiple-51a7e43cb200) | [saved](raw/hiring-plan-and-future-org/sacks_substack_com_p_the_burn_multiple_51a7e43cb200.txt)
- [Coding VC (Leo Polovets), common startup timing mistakes](https://www.codingvc.com/common-startup-timing-mistakes-and-how-to-avoid-them) | [saved](raw/hiring-plan-and-future-org/codingvc_com_common_startup_timing_mistakes_and_how_to_avoid_them.txt)
- [Point Nine Land (guest post), who to hire to raise a Series A](https://writing.pointnine.com/p/off-to-a-flying-start-who-should) | [saved](raw/hiring-plan-and-future-org/writing_pointnine_com_p_off_to_a_flying_start_who_should.txt)
- [Venture Hacks, the option pool shuffle](https://venturehacks.com/option-pool-shuffle) | [saved](raw/hiring-plan-and-future-org/venturehacks_com_option_pool_shuffle.txt)
- [Rework, employee option pool](https://resources.rework.com/libraries/startup-terms/employee-option-pool) (secondary summary of Cooley GO) | [saved](raw/hiring-plan-and-future-org/resources_rework_com_libraries_startup_terms_employee_option_pool.txt)
- [Startups.com via Launchrock, hiring plan](https://www.launchrock.com/library/expert-advice/hiring-plan) (vendor) | [saved](raw/hiring-plan-and-future-org/launchrock_com_library_expert_advice_hiring_plan.txt)
- [People Matters, the hidden cost of rapid hiring](https://www.peoplematters.in/article/business/the-hidden-cost-of-rapid-hiring-in-startups-how-headcount-decisions-silently-destroy-runway-48328) | [saved](raw/hiring-plan-and-future-org/peoplematters_in_article_business_the_hidden_cost_of_rapid_hiring_in_startups_how_headcount_decision.txt)
- [The Data Room (Jonathan Hua), how a VC does due diligence on your company](https://thedataroom.substack.com/p/how-a-vc-does-due-diligence-on-your-company) | [saved](raw/hiring-plan-and-future-org/web_thedataroom_substack_com_p_how_a_vc_does_due_diligence_on_your_company.txt)
- [Fast post-mortem newsletter](https://kjlabuz.substack.com/p/fast) (secondary) | [saved](raw/hiring-plan-and-future-org/web_kjlabuz_substack_com_p_fast.txt)
- [SaaStr, every top founder: I should have acted on bad trends earlier](https://www.saastr.com/every-top-founder-ever-i-should-have-acted-on-bad-trends-earlier/) | [saved](raw/hiring-plan-and-future-org/web_saastr_com_every_top_founder_ever_i_should_have_acted_on_bad_trends_earlier.txt)
- [Dover, how to hire as a seed startup](https://www.dover.com/blog/how-to-hire-as-a-seed-startup) (vendor, read not cited) | [saved](raw/hiring-plan-and-future-org/dover_com_blog_how_to_hire_as_a_seed_startup.txt)
- [Forecastr](https://www.forecastr.co/blog/headcount-planning-protect-runway) and [PitchNHire](https://www.pitchnhire.com/founders/hiring-plan-and-runway) (vendors, read not cited) | [Forecastr saved](raw/hiring-plan-and-future-org/forecastr_co_blog_headcount_planning_protect_runway.txt), [PitchNHire saved](raw/hiring-plan-and-future-org/pitchnhire_com_founders_hiring_plan_and_runway.txt)
- [Startup Fortune, build your hiring plan before the runway runs out](https://startupfortune.com/build-your-startup-hiring-plan-before-the-runway-runs-out/) | [saved](raw/hiring-plan-and-future-org/startupfortune_com_build_your_startup_hiring_plan_before_the_runway_runs_out.txt). The saved page is mostly site navigation and was not used.
- [Peony, Series A data room](https://www.peony.ink/blog/series-a-data-room) and [Papermark, data room for YC startups](https://www.papermark.com/blog/data-room-for-yc-startups) (vendors, read not cited) | [Peony saved](raw/hiring-plan-and-future-org/peony_ink_blog_series_a_data_room.txt), [Papermark saved](raw/hiring-plan-and-future-org/papermark_com_blog_data_room_for_yc_startups.txt)

Pages that blocked automated fetching: none for this guide. A hiring-plan example hosted on Notion (electricnoirstudios.notion.site) returned no text, because it needs JavaScript.
