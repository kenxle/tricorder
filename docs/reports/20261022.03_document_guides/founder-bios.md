# Founder bios

Document guide for Tricorder's scans, checklist and memo. Written 2026-10-22. Sources are saved under [raw/founder-bios/](raw/founder-bios/). Quotes are checked word for word against those saved pages by [build_quotes_people.py](raw/_people_tools/build_quotes_people.py); the results are in [quotes_people.csv](quotes_people.csv).

## What it is

A short bio for each founder: the roles held, schools, what they built, how long they worked in the customer's industry, and why they started this company. The founders write it. It arrives as a PDF page, a deck slide, or a few lines in a cover note, often with a LinkedIn link beside it.

Investors treat it as a set of claims to test, not as proof. One associate says that before opening a data room they already have ten tabs up, checking "any co-founder issues, and whether your story matches what's online" ([Startups Magazine, quoting an associate](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal)).

## At seed and at Series A

The research table marks founder bios as expected at pre-seed, seed and Series A. See [the 30-document table](../20261022.02_research/research_data_room.md). What changes is how hard the bio is tested.

- **Pre-seed and seed.** The bio carries much of the first pass because there is little else. Visible says "At pre-seed, founder bios with relevant experience are sufficient." ([Visible](https://visible.vc/blog/what-to-include-in-your-data-room/), a data-room vendor). Hustle Fund says that at the earliest stages "the team carries unusual weight because the product and market approach may change." ([Hustle Fund checklist](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)).
- **Series A.** The bio is still there, but the company's own record (customers, hires, growth) now speaks for the founders. Formal checks move to after the term sheet. Jason Lemkin of SaaStr lists "Full background checks" and "Formal reference calls" among the deep dives that "often come post term-sheet these days", and adds "If you have something to hide here, it will likely come out later. Post term sheet." ([SaaStr, Lemkin](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet)).
- **A split of opinion.** a16z lists the document as one that can wait: "We definitely want to understand the background of the founding team and other executives, but we generally use LinkedIn for this." ([a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/)). Tricorder does not scrape LinkedIn, so it builds the same picture from the bio, GitHub, personal sites, talks and press.

## What a first pass checks

An associate asks these in order.

1. Do the bios agree across every file? The deck's team slide, the overview, the bios page, the video script, the cap table and the hiring plan should give the same names, titles and start years.
2. Is each claim a dated, checkable fact (employer, role, years, a thing shipped) or an adjective?
3. Does the founder's past match the customer's world? Investors look for "energetic founders working on an idea that grew organically out of their own experience", as Paul Graham wrote on Hacker News about reading YC applications ([the Hacker News account pg, which is Paul Graham's, 2014](https://news.ycombinator.com/item?id=7481618)).
4. Does the public record match the bio? GitHub, a personal site, talks, papers and press should show the same story with dates.
5. Who is full time? Cooley's request list asks for "A list of officers and directors. If any officers are not currently devoting 100% of their business time to the Company, please note them on this list." ([Cooley GO sample list](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/)).
6. How long have the co-founders known each other, and has anyone left? ([Hustle Fund checklist](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step) asks "Co-founder history: How long have the founders known each other, what have they built or overcome together, and why did they choose to partner?")
7. Can the founders explain their own numbers? This is tested in the meeting or the video, and Tricorder reads it from the video claims.

## Green flags

- **A dated, specific fit signal in the first line.** Hustle Fund says the best founders "often have personal experience with the pain point" ([Hustle Fund](https://www2.hustlefund.vc/post/angel-squad-how-hustle-fund-reviews-1000-startups-per-month-for-its-angel-investing-group)). A deck-advice vendor suggests founders "swap exits for four founder-market fit signals: domain-obsession tenure, customer proximity, technical depth proof, and a hard thing you already shipped" ([Causo, vendor view](https://hub.causo.ai/guides/team-slide-first-time-founder)).
- **Public work that predates the company.** The same Hustle Fund page says the test is "This isn't about pedigree or where someone went to school." Dated work in the field before the company existed backs the bio better than a famous logo.
- **The founders know their core numbers and separate fact from guess.** Hustle Fund: "Founders do not need every number memorized, especially before launch. They do need to know which measures drive the company and where to find them." Its green flag list adds "Intellectual honesty. The founder distinguishes fact, estimate, and hypothesis." ([Hustle Fund red-flag guide](https://www.hustlefund.vc/post/angel-squad-red-flags-in-startup-founders-that-experienced-investors-never-ignore)).
- **Lived experience, not only a resume.** Jonathan Hua, a former early-stage investor at SVG Ventures-THRIVE and Scrum Ventures, wrote: "I look for founder-market fit: the unfair edge or lived experience that makes these specific people right for this specific problem, not just qualified in general." He adds "Their resume only tells me what they’ve already done, while adversity tells me what they’ll do when things inevitably get tough." ([The Data Room, Hua, Sep 2026](https://thedataroom.substack.com/p/how-a-vc-does-due-diligence-on-your-company)).
- **Bad news comes out early.** Lemkin: "So disclose whatever issues there are early." ([SaaStr](https://www.saastr.com/what-kind-of-background-check-do-vcs-do-on-the-entrepreneurs-they-fund/)). A bio that already names a gap, and who covers it, reads as self-aware.
- **Co-founders who disagree and still decide.** "Healthy co-founders disagree. What matters is whether they can make a decision, support it, and resolve tension without leaving the company stuck." ([Hustle Fund red-flag guide](https://www.hustlefund.vc/post/angel-squad-red-flags-in-startup-founders-that-experienced-investors-never-ignore)).

## Red flags and pitfalls

**Common**

- **Adjectives instead of facts.** A deck-advice vendor contrasts "6 years as a radiology tech at Mount Sinai, read 40,000+ scans" with "Passionate about using AI to transform healthcare. Previously at a major hospital." ([Causo, vendor view](https://hub.causo.ai/guides/team-slide-first-time-founder)). The second version cannot be checked.
- **Logos with no link to the problem.** Waveup (a deck vendor) lists "I don't know why these logos are here" as a real investor objection ([Waveup, vendor view](https://waveup.com/blog/why-your-decks-team-slide-is-the-most-important-one/)).
- **Founders who cannot explain their own numbers.** Hustle Fund describes a call where "The founder could not explain monthly traffic, conversion rate, returning-customer percentage, or customer acquisition cost (CAC)." The concern was the missing command, not weak metrics ([Hustle Fund](https://www.hustlefund.vc/post/angel-squad-red-flags-in-startup-founders-that-experienced-investors-never-ignore)).
- **Answers that shift.** "The concern is a material claim that keeps changing after you define the terms." (same page).
- **Unresolved co-founder conflict or part-time founders.** Same page, and Cooley's full-time question above.
- **References who all benefit from the founder's success.** Hua: "Founder pitfall: only offering references who are direct beneficiaries of your success, an investor, a close friend, a subordinate. I always ask for at least one reference outside the people you’d naturally choose." His list of things that lose points includes "References that sound like they’re reading from a script you gave them." (same page).
- **Bad back-channel references.** A SaaStr post says "If a VC hears negative feedback about the founder or team during backchannel reference checks, it’s often game over." ([SaaStr](https://www.saastr.com/dear-saastr-what-are-the-top-red-flags-for-vcs-when-deciding-to-invest-in-a-sstartup)). Lemkin tempers it: one rough reference will not stop a deal.

**Rare but serious**

- **Made-up credentials used to raise money.** The SEC alleged that the founder of a startup called Centricity raised $2.8 million from seven investors, from 2019 through 2021, by "making fraudulent misrepresentations about Centricity’s customers and revenue as well as Brackett’s own educational and employment background." ([SEC press release, republished by AltsWire](https://thediwire.com/?p=43904)). These are allegations in a complaint. The SEC page itself blocked automated fetching, so the republished copy is the source.
- **Undisclosed litigation or earlier fraud.** A founder-diligence vendor says "The moment investors uncover undisclosed litigation or missing IP assignments, the deal either dies or the valuation gets renegotiated." ([Angel Investors Network, vendor view](https://angelinvestorsnetwork.com/startups/founder-diligence-what-investors-actually-check)).
- **Material issues found late.** Lemkin: "Finding material issues late in the potential investment process is a big flag." ([SaaStr](https://www.saastr.com/what-kind-of-background-check-do-vcs-do-on-the-entrepreneurs-they-fund/)).

**Pitfalls for the reader**

- A discrepancy is a prompt, not a verdict. Hustle Fund says to "verify only the identity, employment, education, professional license, litigation, or other history that could change your thesis, and treat a discrepancy as a prompt for context rather than an automatic finding of misconduct." ([Hustle Fund checklist](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step)).
- A thin reference network is not a red flag. GoingVC: "don’t let the absence of a strong reference network automatically serve as a red flag, especially for underrepresented founders who may be building outside the established networks that make back-channel references easy to find." ([GoingVC](https://www.goingvc.com/post/how-to-reference-check-a-founder)).
- Background checks are still unusual at the earliest stages. Form Ventures: "Still vanishingly rare." ([Form Ventures](https://formventures.substack.com/p/team-talks-ii-founder-reference-calls)).

## How Tricorder checks it

**What a script can check**

- `industry_tenure`, `github_age_months`, `domain_repos`, `predates_company` and `timeline`: already defined in [FRAMEWORKS 6.1 founder-market fit](../../ongoing/FRAMEWORKS.md). They run after Saturday.
- Proposed `bio_cross_file_consistency`: take (name, title, employer, start year) from each file that names the person. Flag any pair of files where the name or title text differs, or where a start year differs. Formula: `mismatch = COUNT of person-fields whose normalised text is not equal across files`.
- Proposed `tenure_within_company_age`: `claimed_months_at_company ≤ as_of_date − founding_date`. A bio that says "since 2023" for a company founded in 2024 gets flagged.
- Proposed `founders_on_cap_table`: every founder named in the bios holds common stock on the cap table.
- Proposed `bio_has_dates`: the share of bio claims that carry a year or a duration. A low share means the scan will write gaps, not findings.

**What needs a model to read**

- Pull each claim (employer, role, school, years, product shipped) out of the bios, the deck and the video, with the exact quote and its date.
- Match claims to public pages and write the 6.1 label with the quote it relied on.
- It must quote the span. It must not infer age, gender, ethnicity, nationality, religion, politics, health or family, and must not treat missing GitHub activity as a negative ([FRAMEWORKS 6.1](../../ongoing/FRAMEWORKS.md)).

**What Tricorder cannot check (leave to the operator)**

- Degrees and past employers: a university or employer check, with the founder's consent.
- Litigation and criminal records: a paid background check after the term sheet.
- Reference calls, on-list and off-list. Form Ventures and GoingVC both treat these as the main tool, and "Most funds I spoke with only do reference calls at the end of the process" ([Form Ventures](https://formventures.substack.com/p/team-talks-ii-founder-reference-calls)).
- Whether the founders work well together.

Tricorder finds differences between what the bio says and what the public record and the other files say. It does not say a founder lied.

## Readout pieces and checklist items

- **Team** piece. On Saturday only the headcount label feeds it. The founder scans (6.1, 6.2) are after Saturday.
- Checklist items ([CHECKLIST](../../ongoing/CHECKLIST.md)): C53 (founder bios), C55 (founder-market fit from dated public work), C91 (co-founder issues), C97 (reference list), C57 (background checks) and C58 (founder reference calls). C57 and C58 are "not checked yet" and marked "not stated" for stage.

## If it is missing

- **Seed and Series A: a gap, not a red flag.** The research says a missing document is a question for the operator ([the data-room research, 1.5](../20261022.02_research/research_data_room.md)). The scans can still profile named founders from public sources.
- **Ask-list line:** "Please send a one-page bio for each founder with dated roles and years, and the GitHub, site or talk links you want us to look at."

## In the Hollis Voice room

The room holds it twice: `05_team/founder_bios.pdf` and deck slide 10 ([data room README](../../../data_room/README.md)).

- The bios name two founders (CEO and CTO) and four senior staff. The CEO "ran operations for a regional veterinary group for nine years". The CTO "spent eleven years building speech and telephony systems at Kestrel Telecom Software". Only the CTO lists a GitHub handle, and it is a placeholder.
- **No planted flag.** The answer key's team facts list the same six names and titles. The README says every name matches across the deck, bios, overview, video script and cap table.
- **Green flag.** Staff today, 17, agrees between deck slide 10 and the model's `STAFF_NOW` (green flag GF3 in `answer_key.json`). That is why the team piece reads strong.
- **What a scan would find.** The CEO's bio names no employer and gives no years. A 6.1 scan finds a claim it cannot date and writes a gap. That is a fair demo of "no public evidence found" on a synthetic founder.

## Sources

Each page is saved in [raw/founder-bios/](raw/founder-bios/). Vendor views are marked.

- [Visible, what to include in your data room](https://visible.vc/blog/what-to-include-in-your-data-room/) (vendor) | [saved](raw/founder-bios/visible_vc_blog_what_to_include_in_your_data_room.txt)
- [a16z, the insider's guide to data rooms](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/) | [saved](raw/founder-bios/a16z_com_the_insiders_guide_to_data_rooms_what_to_know_before_you_raise.txt)
- [Hustle Fund, angel investing due diligence checklist](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step) | [saved](raw/founder-bios/hustlefund_vc_post_angel_squad_angel_investing_due_diligence_checklist_step_by_step.txt)
- [Hustle Fund, startup red flags: investor screening guide](https://www.hustlefund.vc/post/angel-squad-red-flags-in-startup-founders-that-experienced-investors-never-ignore) | [saved](raw/founder-bios/web_hustlefund_vc_post_angel_squad_red_flags_in_startup_founders_that_experienced_investors_never_ignore.txt)
- [Hustle Fund, how it reviews 1000+ startups a month](https://www2.hustlefund.vc/post/angel-squad-how-hustle-fund-reviews-1000-startups-per-month-for-its-angel-investing-group) | [saved](raw/founder-bios/www2_hustlefund_vc_post_angel_squad_how_hustle_fund_reviews_1000_startups_per_month_for_its_angel_in.txt)
- [Hustle Fund, cultural due diligence](https://www2.hustlefund.vc/post/angel-squad-cultural-due-diligence-why-company-culture-matters-to-angel-investment-returns) | [saved](raw/founder-bios/www2_hustlefund_vc_post_angel_squad_cultural_due_diligence_why_company_culture_matters_to_angel_inve.txt)
- [SaaStr, what types of due diligence VCs do for seed and Series A](https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet) | [saved](raw/founder-bios/saastr_com_how_when_why_vcs_do_due_diligence_pre_and_post_term_sheet.txt)
- [SaaStr, what kind of background checks VCs do](https://www.saastr.com/what-kind-of-background-check-do-vcs-do-on-the-entrepreneurs-they-fund/) | [saved](raw/founder-bios/saastr_com_what_kind_of_background_check_do_vcs_do_on_the_entrepreneurs_they_fund.txt)
- [SaaStr, top red flags for VCs](https://www.saastr.com/dear-saastr-what-are-the-top-red-flags-for-vcs-when-deciding-to-invest-in-a-sstartup) | [saved](raw/founder-bios/saastr_com_dear_saastr_what_are_the_top_red_flags_for_vcs_when_deciding_to_invest_in_a_sstartup.txt)
- [Form Ventures, Team Talks: founder reference calls](https://formventures.substack.com/p/team-talks-ii-founder-reference-calls) | [saved](raw/founder-bios/formventures_substack_com_p_team_talks_ii_founder_reference_calls.txt)
- [The Data Room (Jonathan Hua), how a VC does due diligence on your company](https://thedataroom.substack.com/p/how-a-vc-does-due-diligence-on-your-company) | [saved](raw/founder-bios/web_thedataroom_substack_com_p_how_a_vc_does_due_diligence_on_your_company.txt)
- [GoingVC, how to reference check a founder](https://www.goingvc.com/post/how-to-reference-check-a-founder) | [saved](raw/founder-bios/goingvc_com_post_how_to_reference_check_a_founder.txt)
- [First Round Review, what to expect at a seed partner meeting](https://review.firstround.com/heres-what-you-can-really-expect-when-pitching-your-seed-stage-startup-at-a-vc-partner-meeting/) | [saved](raw/founder-bios/review_firstround_com_heres_what_you_can_really_expect_when_pitching_your_seed_stage_startup_at_a_vc.txt)
- [Startups Magazine, how to build a data room that closes the deal](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal) | [saved](raw/founder-bios/web_startupsmagazine_co_uk_how_to_build_a_data_room_that_closes_the_deal.txt)
- [Hacker News item 7481618, a comment by pg](https://news.ycombinator.com/item?id=7481618) | [saved JSON](raw/founder-bios/hn_yc_application_read_comment.json)
- [Cooley GO, sample VC due diligence request list](https://www.cooleygo.com/documents/sample-vc-due-diligence-request-list/) | [saved](raw/founder-bios/cooley_vc_dd_request_list.txt)
- [DocSend, the startup fundraising due diligence checklist](https://www.docsend.com/blog/due-diligence-checklist/) | [saved](raw/founder-bios/docsend_com_blog_due_diligence_checklist.txt) (read through a browser by an earlier session)
- [SEC press release on Centricity, republished by AltsWire](https://thediwire.com/?p=43904) | [saved](raw/founder-bios/thediwire_com_p_43904.txt). The original SEC pages returned HTTP 403.
- [Angel Investors Network, founder diligence](https://angelinvestorsnetwork.com/startups/founder-diligence-what-investors-actually-check) (vendor) | [saved](raw/founder-bios/angelinvestorsnetwork_com_startups_founder_diligence_what_investors_actually_check.txt)
- [Causo, the team slide fix for first-time founders](https://hub.causo.ai/guides/team-slide-first-time-founder) (vendor) | [saved](raw/founder-bios/hub_causo_ai_guides_team_slide_first_time_founder.txt)
- [Waveup, the team slide](https://waveup.com/blog/why-your-decks-team-slide-is-the-most-important-one/) (vendor) | [saved](raw/founder-bios/waveup_com_blog_why_your_decks_team_slide_is_the_most_important_one.txt)
- [Echai, presenting a team slide with no big names](https://echai.ventures/startingup/pitch-deck/how-should-i-present-my-team-slide-when-we-are-first-time-founders-with-no-big-brand-names-on-it) (summary of a TechCrunch piece) | [saved](raw/founder-bios/echai_ventures_startingup_pitch_deck_how_should_i_present_my_team_slide_when_we_are_first_time_found.txt)
- [Ten saved Hacker News search results on founder background checks](raw/founder-bios/hn_vc_background_check_founder.json) and [on reference checks](raw/founder-bios/hn_investors_reference_checks_founders.json). Read, not cited: the comments were opinion without a named investor behind them.

Pages that blocked automated fetching: the SEC litigation release and press release pages (HTTP 403), and the Justice Department press release (returned no text).
