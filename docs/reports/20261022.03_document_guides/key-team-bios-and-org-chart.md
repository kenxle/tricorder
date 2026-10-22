# Key team bios and org chart

Document guide for Tricorder's scans, checklist and memo. Written 2026-10-22. Sources are saved under [raw/key-team-bios-and-org-chart/](raw/key-team-bios-and-org-chart/). Quotes are checked word for word against the saved pages by [build_quotes_people.py](raw/_people_tools/build_quotes_people.py); results are in [quotes_people.csv](quotes_people.csv). Facts about the Hollis Voice room come from [room_facts_people.py](raw/key-team-bios-and-org-chart/room_facts_people.py) and its output [room_facts_people.out.txt](raw/key-team-bios-and-org-chart/room_facts_people.out.txt).

## What it is

Two files that sit together. The first is a short bio for each person below the founders who matters to the plan: the head of sales, the lead engineer, the controller. The second is an org chart: boxes for the people on payroll, lines for who reports to whom, and often boxes for open roles.

The founders or an operations lead prepare it. It arrives as a PDF page, a slide, or an export from a chart tool. DocSend's checklist files the chart under "Corporate records and documents" as "Company organizational chart", and lists "List of company employees including title, salary, bonus potential, commissions, exempt or non-exempt status, and contact information" under employee relations ([DocSend checklist](https://www.docsend.com/blog/due-diligence-checklist/)).

## At seed and at Series A

The research table marks it lighter at pre-seed and expected at seed and Series A. See [the 30-document table](../20261022.02_research/research_data_room.md). Visible splits it into two rows and shows the difference:

- Key team member bios: lighter at pre-seed, expected from seed on.
- Current org chart: left out at pre-seed, lighter at seed, expected at Series A.

([Visible master checklist](https://visible.vc/blog/what-to-include-in-your-data-room/), a data-room vendor.) Its text says "Seed and Series A founders also need bios for the key team members, an org chart, and a hiring plan tied directly to the use of funds." By Series A, "employment and advisory agreements with IP assignment and key-person retention terms become standard diligence asks." Papermark (another vendor) puts "org chart with open roles" in the team folder a YC company builds before Demo Day ([Papermark](https://www.papermark.com/blog/data-room-for-yc-startups)).

a16z lists "Org chart and/or team bios" as a document that can wait: "We definitely want to understand the background of the founding team and other executives, but we generally use LinkedIn for this." ([a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/)). Kruze, an accounting firm, lists "Org chart" and "Salary schedule for all employees" among the HR items in a venture request ([Kruze](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/)).

What changes from seed to Series A: the seed investor wants to see that the people in the plan exist. The Series A investor and counsel also want the paper behind them (offer letters, retention terms, IP assignments) and a salary list that ties to payroll.

## What a first pass checks

1. Does the number of people on the chart equal the staff count in the deck, the overview and the model?
2. Who owns product, engineering, sales, operations and finance? Hustle Fund's checklist asks "Role coverage: Who owns product, engineering, sales, operations, and finance? Which missing role becomes urgent after the raise?" ([Hustle Fund checklist](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)).
3. Do the titles fit the people's experience, and do they leave room to hire above them?
4. How long has each key person been there, and has anyone important left? SaaStr's list of legal checks asks "Are there ex-founder issues? Cap table issues? Do the founders have enough unvested stock left? Are there any issues with founders that have left the company?" ([SaaStr, Lemkin](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet)).
5. Are contractors marked as contractors, and are they counted in headcount and burn?
6. Are any executives paid or lent money outside payroll? Kruze asks for "Any transactions with executives (as in, did the founder borrow money from the startup, or vice versa)".
7. Do the people named in the hiring plan and the chart exist outside the company's own files?
8. Are the advisors real, and what have they done?

## Green flags

- **The count agrees across files.** The deck, the overview and the model give the same staff number. A number that two independent files state the same way is the readout's definition of corroborated ([FRAMEWORKS, piece verdicts](../../ongoing/FRAMEWORKS.md)).
- **Every core function has a named owner, and the one gap has a plan.** Hustle Fund's list of acceptable uncertainty includes "One executive role remains open, with a credible owner and hiring plan." ([Hustle Fund checklist](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)).
- **Titles that match experience and leave headroom.** An executive-search partner who studied early hiring at 15 European software companies warns against inflated titles: "you can end up with a reasonably inexperienced leadership team that you can’t hire above because the existing team already hold C-suite titles." ([Point Nine, guest post by Erevena](https://writing.pointnine.com/p/off-to-a-flying-start-who-should)). The sample was companies that went on to raise large rounds, so it describes success and is not a norm.
- **Open roles drawn on the chart and tied to the hiring plan.** Papermark: "org chart with open roles" (above).
- **Retention terms for key people.** Visible: key-person retention terms "become standard diligence asks" by Series A.
- **A short, working list of advisors.** Waveup (a deck vendor) says to include "only advisors with real skin in the game" and warns that "Equal space for low-commitment advisors signals a thin core team" ([Waveup, vendor view](https://waveup.com/blog/why-your-decks-team-slide-is-the-most-important-one/)).

## Red flags and pitfalls

**Common**

- **The chart and the headcount disagree.** Hustle Fund names the pattern: "The concern is a material claim that keeps changing after you define the terms." ([Hustle Fund red-flag guide](https://www.hustlefund.vc/post/angel-squad-red-flags-in-startup-founders-that-experienced-investors-never-ignore)).
- **Every box has a C-level title.** Same Point Nine post, quote above. It also reports that the average company in its sample hired a small number of C-levels in the first 18 months ("To make this slightly easier to remember, the average company hires the following people in the first 18 months:" followed by a list that includes 1 to 2 C-levels and 18 individual contributors).
- **A wall of advisors, or contractors drawn as staff.** Waveup, above. Its table says never list contractors "just to look bigger".
- **Roles nobody owns.** Hustle Fund's role-coverage question above.
- **Contractors standing in for staff.** The Holloway angel-investing guide (Joe Wallin and Pete Baltaxe) says to ask who is an employee and who is a contractor, and to "beware of companies where the majority of the team working at the office are classified as contractors." ([Holloway Guide, Wallin and Baltaxe](https://www.holloway.com/g/angel-investing/sections/legal-diligence-on-other-founder-board-of-directors-and-employee-issues)).

**Rare but serious**

- **A departed founder or early employee with a claim on stock.** Holloway: "Many expensive lawsuits have arisen from former early employees who might have been promised stock or who had not vested their stock before they were terminated or quit." (same page).
- **Key people with almost no equity, and advisors with a lot.** Hua: "Key personnel with almost no equity , like a VP of Engineering holding 0.1% fully diluted at a company raising a Series C, is a huge retention risk I’ll price into the term sheet whether the founder addresses it or not." On the other side: "Advisor equity that never got attached to deliverables , such as eight advisors holding 2% each with vesting schedules that already expired, signals a judgment problem more than a cap table problem." ([The Data Room, Hua, Sep 2026](https://thedataroom.substack.com/p/how-a-vc-does-due-diligence-on-your-company)).
- **Founders who plan to pay themselves back from the round.** Holloway: "Look out for founders who intend to use almost the entire proceeds of the offering to pay themselves back for foregone salaries or unreimbursed expenses or other accrued liabilities".
- **Loans between the company and an executive.** Kruze's request, above.
- **Key people with no retention terms.** Visible, above.

## How Tricorder checks it

**What a script can check**

- The headcount label already exists: the `piece_verdicts` check compares `headcount` claims across files ([FRAMEWORKS](../../ongoing/FRAMEWORKS.md)). On Hollis Voice it is the green flag GF3.
- Proposed `org_chart_headcount`: `boxes_on_chart − staff_today`, where staff today comes from the deck, the model and the overview. A non-zero result is a difference in reporting, not a finding about people.
- Proposed `title_collision`: `planned_roles ∩ current_titles`. A planned hire whose title already belongs to a current person is flagged. The room is built to pass this ([README](../../../data_room/README.md)).
- Proposed `function_coverage`: for each of product, engineering, sales, operations and finance, `TRUE` if a current person or a planned hire (from the hiring plan) holds it. A function with neither is a gap.
- Proposed `c_level_share`: `c_level_titles ÷ staff_today`, shown to the operator. There is no published cutoff, so Tricorder shows the ratio and sets no threshold.
- Proposed `names_in_older_files`: people named in the deck or earlier bios who are missing from the chart. This catches a quiet departure.
- C56, "the people in the plan exist": a search for a dated public trace of each named person (never LinkedIn scraping). It has no check yet in [CHECKLIST](../../ongoing/CHECKLIST.md).

**What needs a model to read**

- An org chart is often an image. A model with vision reads the boxes, titles and reporting lines and writes each as a claim with the page and the box text as its quote.
- Reading bios for start years and prior roles, with the exact span quoted.
- It must not infer age, gender, ethnicity, nationality, religion, politics, health or family, and must not treat a thin public profile as a negative ([FRAMEWORKS 6.1](../../ongoing/FRAMEWORKS.md)).

**What Tricorder cannot check (leave to the operator)**

- Whether a person on the chart is on payroll. A payroll export or a call with the controller settles it.
- Reference calls on key hires.
- Whether retention agreements were signed and what they say. A lawyer reads them.
- Contractor classification, which is a legal call.

## Readout pieces and checklist items

- **Team** piece (the `headcount` label), and **burn and runway** through the `hires` label.
- Checklist items ([CHECKLIST](../../ongoing/CHECKLIST.md)): C54 (key team bios and org chart), C56 (the people in the plan exist), C97 (reference list: management, customers, investors, advisors), C25 (contractors counted in headcount and burn) and C93 (the company's own hiring against the plan).

## If it is missing

- **Pre-seed:** not a gap. Visible leaves the org chart out at that stage.
- **Seed:** a light gap. Ask for it, and do not mark the team piece weak for its absence.
- **Series A:** a gap with a firm ask. Still not a red flag by itself: the research says to treat a missing document as a question for the operator ([data-room research, 1.5](../20261022.02_research/research_data_room.md)).
- **Ask-list line:** "Please send a current org chart (names, titles, who reports to whom, contractors marked, open roles) and a short bio for each person who reports to a founder."

## In the Hollis Voice room

- **Not in the room as an org chart.** There is no org chart and no employee list. The nearest files are the bios page and deck slide 10.
- **What is there.** Four senior staff are named: the Head of Sales, Head of Customer Success, a part-time Controller and the Lead Voice Engineer. With the two founders that is 6 people named, against 17 staff today. So 11 people are not named anywhere. The cap table shows 11 option holders. The room does not say whether those are the same people (computed in room_facts_people.py).
- **Planted flags:** none for this document.
- **Green flag:** staff today, 17, agrees between deck slide 10 and the model's `STAFF_NOW` (GF3). Staff after hiring, 41, agrees between deck slide 12 and the last row of the hiring plan.
- **No title collision.** No planned role equals a current title. The plan's "Director of Enterprise Sales" sits above the current Head of Sales, which the README calls a deliberate choice.
- **What the demo can show.** The ask list would read: an org chart or payroll list that names all 17 people.

## Sources

Each page is saved in [raw/key-team-bios-and-org-chart/](raw/key-team-bios-and-org-chart/). Vendor views are marked.

- [Visible, what to include in your data room](https://visible.vc/blog/what-to-include-in-your-data-room/) (vendor) | [saved](raw/key-team-bios-and-org-chart/visible_vc_blog_what_to_include_in_your_data_room.txt)
- [a16z, the insider's guide to data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/) | [saved](raw/key-team-bios-and-org-chart/a16z_com_the_insiders_guide_to_data_rooms_what_to_know_before_you_raise.txt)
- [Kruze, VC due diligence checklists](https://kruzeconsulting.com/what-are-examples-of-vc-due-diligence-check-lists/) (accounting firm) | [saved](raw/key-team-bios-and-org-chart/kruzeconsulting_com_what_are_examples_of_vc_due_diligence_check_lists.txt)
- [DocSend, the startup fundraising due diligence checklist](https://www.docsend.com/blog/due-diligence-checklist/) | [saved](raw/key-team-bios-and-org-chart/docsend_com_blog_due_diligence_checklist.txt) (read through a browser by an earlier session)
- [Hustle Fund, angel investing due diligence checklist](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step) | [saved](raw/key-team-bios-and-org-chart/hustlefund_vc_post_angel_squad_angel_investing_due_diligence_checklist_step_by_step.txt)
- [Hustle Fund, startup red flags](https://www.hustlefund.vc/post/angel-squad-red-flags-in-startup-founders-that-experienced-investors-never-ignore) | [saved](raw/key-team-bios-and-org-chart/web_hustlefund_vc_post_angel_squad_red_flags_in_startup_founders_that_experienced_investors_never_ignore.txt)
- [Hustle Fund, cultural due diligence](https://www2.hustlefund.vc/post/angel-squad-cultural-due-diligence-why-company-culture-matters-to-angel-investment-returns) | [saved](raw/key-team-bios-and-org-chart/www2_hustlefund_vc_post_angel_squad_cultural_due_diligence_why_company_culture_matters_to_angel_inve.txt)
- [Point Nine Land, who to hire to raise a Series A (guest post by Erevena)](https://writing.pointnine.com/p/off-to-a-flying-start-who-should) | [saved](raw/key-team-bios-and-org-chart/writing_pointnine_com_p_off_to_a_flying_start_who_should.txt)
- [Holloway Guide, Angel Investing: legal diligence on founder, board and employee issues](https://www.holloway.com/g/angel-investing/sections/legal-diligence-on-other-founder-board-of-directors-and-employee-issues) | [saved](raw/key-team-bios-and-org-chart/holloway_com_g_angel_investing_sections_legal_diligence_on_other_founder_board_of_directors_and_empl.txt)
- [SaaStr, diligence at seed and Series A](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet) | [saved](raw/key-team-bios-and-org-chart/saastr_com_how_when_why_vcs_do_due_diligence_pre_and_post_term_sheet.txt)
- [Papermark, data room for YC startups](https://www.papermark.com/blog/data-room-for-yc-startups) (vendor) | [saved](raw/key-team-bios-and-org-chart/papermark_com_blog_data_room_for_yc_startups.txt)
- [Peony, Series A data room](https://www.peony.ink/blog/series-a-data-room) (vendor) | [saved](raw/key-team-bios-and-org-chart/peony_ink_blog_series_a_data_room.txt)
- [SeedLegals, data room help page](https://help.seedlegals.com/en/data-room-how-it-can-enhance-your-funding-round) (vendor) | [saved](raw/key-team-bios-and-org-chart/help_seedlegals_com_en_data_room_how_it_can_enhance_your_funding_round.txt)
- [Waveup, the team slide](https://waveup.com/blog/why-your-decks-team-slide-is-the-most-important-one/) (vendor) | [saved](raw/key-team-bios-and-org-chart/waveup_com_blog_why_your_decks_team_slide_is_the_most_important_one.txt)
- [The Data Room (Jonathan Hua), how a VC does due diligence on your company](https://thedataroom.substack.com/p/how-a-vc-does-due-diligence-on-your-company) | [saved](raw/key-team-bios-and-org-chart/web_thedataroom_substack_com_p_how_a_vc_does_due_diligence_on_your_company.txt)
- [Cooley GO, sample VC due diligence request list](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/) | [saved](raw/key-team-bios-and-org-chart/cooley_vc_dd_request_list.txt)

No page for this guide blocked automated fetching. The searches turned up no public investor post that says how to read an org chart for title inflation; the Point Nine study is the closest, and it is one executive-search firm's sample.
