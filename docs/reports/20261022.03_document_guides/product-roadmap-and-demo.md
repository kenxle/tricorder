# Product roadmap and demo

**In one line:** the demo shows what exists today and the roadmap says what comes next. The honest version of each says which parts are real, and Tricorder checks the roadmap against the money and the hires.

Written 2026-10-22 for the Tricorder document guides (group: story). Every quote below was checked word for word against the saved page by `raw/_verify_story/verify_quotes_story.py`; the rows are in `quotes_story.csv`. Vendor views are marked. News reports are paraphrased.

## 1. What it is

Two things that Tricorder's table groups as one document:

- **The roadmap:** a short plan of what the team will build and when. It is one or two slides, a one-page document or a link to a product board. YC suggests keeping it brief: "You can optionally include a summary product roadmap (6 quarters max) indicating what an investment buys." ([YC](https://www.ycombinator.com/blog/how-to-raise-a-seed-round/))
- **The demo:** a live walkthrough, a recording, a sandbox login or a clickable prototype. Hustle Fund's Angel Squad names the four forms: live product, recorded walkthrough, interactive sandbox and clearly labeled prototype ([Hustle Fund](https://www.hustlefund.vc/post/angel-squad-how-to-use-product-demos-to-convince-angel-investors)).

The CEO, product lead or CTO prepares them. Visible, a vendor, lists the roadmap and a demo or walkthrough video as two rows, both included at every stage ([Visible, vendor view](https://visible.vc/blog/what-to-include-in-your-data-room/)).

## 2. At seed and at Series A

- **Seed:** a working demo is expected. CRV: "A working demo is close to a requirement at this stage." ([CRV](https://www.crv.com/content/what-investors-look-for)) The roadmap is a plan the investor reads for judgment. Tomasz Tunguz, a venture investor, puts it in the second round of meetings: "I know it’s early and hard to forecast, but I’m looking to be convinced the founder has a good sense of where the company is going and why." ([Tunguz](https://www.tomtunguz.com/breaking-down-a-typical-vcstartup-diligence-process/)) a16z asks for it inside the deck: "as well as a rough road map or plan for how you will use the funds." ([a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/))
- **Series A:** the roadmap matters less as a story and more as a plan that the money and the team can deliver. CRV says a Series A deck should keep the roadmap short: "Product roadmap details should move to supporting material unless it supports a business claim." and "Your use of funds slide should connect directly to your go-to-market evidence and hiring plan." ([CRV](https://www.crv.com/content/series-a-pitch-deck))
- **What changes for Tricorder:** at seed the demo is the evidence the product exists. At Series A the demo is a given, and the question moves to the roadmap against the hiring plan and the burn.

## 3. What a first pass checks

1. Does a working product exist, and in what form is it shown (live, recording, sandbox, prototype)?
2. Does the demo say what is manual, scripted or simulated? Hustle Fund: "State which interactions work, which outputs are scripted, and what remains to be built."
3. Which roadmap items are built, in progress or planned, and by what date?
4. Does the roadmap fit the use of funds and the hiring plan? Is there an engineer in the plan for each major item?
5. Does each roadmap item tie to a business claim (retention, revenue, a new segment)?
6. Do the features in the deck, the one-pager, the website and the demo agree?
7. What does a person do behind the product today? Hustle Fund lists it as a question to ask: "Manual work: Where is a person operating behind the product today, and what is the plan for that work?"

## 4. Green flags

- **It says plainly what is live and what is not.** Hustle Fund: "If part of the output was prepared by a person, a rules engine, or a scripted prototype, say so." and "Clear boundaries build a stronger conversation than implied automation." ([Hustle Fund](https://www.hustlefund.vc/post/angel-squad-how-to-use-product-demos-to-convince-angel-investors))
- **It follows one user through one job.** The same post describes a four-minute path and adds, "Describe only what happened in front of the investor."
- **The demo is kept apart from proof of demand.** "A successful click path shows that the feature worked in the demo environment. User validation requires separate evidence." ([Hustle Fund](https://www.hustlefund.vc/post/angel-squad-how-to-use-product-demos-to-convince-angel-investors)) A dated, defined usage figure sits after the demo.
- **The roadmap names milestones and money.** Hunter Walk, a seed investor: "Tell me what you’re going to accomplish with my dollars as the headline." ([Hunter Walk](https://hunterwalk.com/2022/08/01/three-startup-pitch-deck-mistakes-that-are-red-flags-for-venture-investors/)) Haje Jan Kamps, a pitch coach, says an operating plan should include "product, traction, market validation and key hire milestones." ([TechCrunch](https://techcrunch.com/2022/12/11/the-ask))
- **It is short.** Six quarters at most (YC quote above).

## 5. Red flags and pitfalls

Common:

- **A wandering demo.** Rob Go, a seed investor at NextView: "Most demos feel kind of like a random walk." and "I find that the majority of these demos end up being relatively unproductive for the founders." ([NextView](https://nextview.vc/blog/5-common-mistakes-founders-make-when-giving-demos-to-investors/))
- **A polished demo of one scenario.** The authors of an angel-investing book warn that founders often show a polished demo of one specific scenario and the product may only work well under those constraints; their advice is to get a thorough demo and use the product yourself ([Angel Investing: Start to Finish, Holloway](https://www.holloway.com/g/angel-investing/sections/diligence-on-product-and-technology), paraphrased).
- **Screenshots or a mockup standing in for a product.** Hustle Fund: "Screenshots are a reasonable fallback and weak primary evidence of a working interaction." The formats list asks for a prototype to be labeled as one.
- **A demo used as proof that customers want it.** See the usage quote above.
- **A roadmap that leads at Series A.** CRV: "Founders paint an impressive picture of where the product is headed, only for investors to discover that most of the roadmap hasn’t been built yet." and "Investors discount hypotheticals to zero because the work hasn’t actually been done." ([CRV](https://www.crv.com/content/series-a-pitch-deck))
- **A roadmap with no money or people behind it.** Hunter Walk asks founders to lead with milestones, not months of runway: his headline says "Focus on Milestones You’ll Use This Funding Round to Achieve, Not Just Time It Buys You". Kamps lists "Omitting what the funds will be used for." as a common ask-slide mistake ([TechCrunch](https://techcrunch.com/2022/12/11/the-ask)).
- **Features that differ between the deck, the website and the demo.** This is the same kind of difference Tricorder looks for in numbers.

Rare but serious:

- **Automation that is not automation.** A federal indictment charged the founder of the shopping app Nate with securities and wire fraud; prosecutors say investors were told the app ran on proprietary AI while overseas contract workers placed the orders by hand ([Digital Commerce 360](https://www.digitalcommerce360.com/2025/04/11/nate-ecommerce-ceo-charged-fraud-fake-ai-claims/), news report, paraphrased). Tricorder does not detect fraud, and a clean demo cannot rule this out. The demo question to ask is the Hustle Fund one about manual work.

## 6. How Tricorder checks it

**What a script can check**

- There is no roadmap check yet; the checklist marks "Product roadmap against the use of funds" as "not checked yet". I propose `use_of_funds_vs_hiring_split`:
  - Group `hiring_plan.csv` by function and sum base pay: `share_hire(g) = base_pay(g) ÷ total base pay`.
  - `share_funds(g) = use-of-funds line(g) ÷ the raise`.
  - Print both next to each other with their difference. Use of funds also pays for programs, so a gap is a question for the operator, never a flag by itself.
- Proposed `roadmap_dates_vs_hire_starts`: for each roadmap item with a date and a function, check that the first hire in that function starts before the date.
- Proposed `use_of_funds_sums`: the lines add to the raise.
- Existing: `Pricing changes and customer wins` (FRAMEWORKS 3.2) compares published pricing and announced wins; the checklist maps the roadmap and demo to it, and to the claim extraction (1.1) for features named in the deck.
- Existing: the burn-against-hiring-plan check (`payroll_from_hiring_plan_and_rerun_cash`, 1.4) shows whether the money lasts for the hires the roadmap needs.

**What needs a model to read**

- Sort roadmap items into built, in progress and planned, and quote the words and dates.
- Read a demo's transcript and frames: what is shown live, what is scripted, and any "coming soon" or "beta" language.
- Compare the feature lists in the deck, the one-pager, the website and the demo.
- Link each roadmap item to a business claim, or say it has none.

**What Tricorder cannot check (leave to the operator)**

- Whether a person is operating behind the product. Ask, and use the product yourself.
- Whether the product scales, and whether the code is the company's. A technical call with the engineer and counsel settle those.
- Whether customers use it. Reference calls and product analytics settle that.

## 7. Which readout pieces it feeds

- **The pitch itself:** checklist items "Product roadmap and demo" (id C63), "Product roadmap against the use of funds" (C68, not checked yet) and "Use of funds plan for this round" (C96, not checked yet).
- **Burn and runway**, through the hiring plan that the roadmap needs.
- **Market**, through pricing and customer wins (FRAMEWORKS 3.2).
- **The ask list**, when the room holds no roadmap or no demo.

## 8. If it is missing

- **Seed:** a gap, not a flag. CRV treats a working demo as close to required, so it is a real question, but the operator may see it on a call.
- **Series A:** a bigger gap. At Series A the operator needs a way to see the product. Still not a flag.
- **Ask-list line:** "Please send a recorded demo or a login to a sandbox, and a one-page roadmap with dates and owners. Say which parts of the demo are live."

## 9. In the Hollis Voice room

The room holds neither a roadmap nor a demo recording. The checklist maps this document to `06_product/product_one_pager.pdf` (what it does, pricing, integrations). Related files are `06_product/website_copy.md`, deck slide 2 (a written example call), slide 12 (24 planned hires, 10 in engineering) and slide 13 (use of funds). All of these are in the seed drop.

What a Tricorder run would show:

- **Gap:** no roadmap and no demo in the room. Both go on the ask list.
- **Pricing agrees:** the Standard plan at $649 a month appears on deck slide 7, the one-pager, the website and the Brookline Row order form. The readout notes this as a corroboration inside the weak unit-economics piece.
- **The website repeats a planted claim:** "Trusted by 357 independent veterinary clinics" is PF7 (212 clinics pay).
- **Use of funds against the hiring plan** (script `raw/product-roadmap-and-demo/hollis_use_of_funds_vs_hiring.py`, output saved beside it): engineering is 40.0% of the funds, 41.7% of the hires and 46.2% of the hires' base pay; sales and marketing is 35.0% of the funds, 25.0% of the hires and 25.7% of base pay; customer success and support is 15.0% of the funds, 25.0% of the hires and 20.9% of base pay; general and administrative is 10.0% of the funds, 8.3% of the hires and 7.2% of base pay. The funds lines add to $9,000,000. Marketing programs and non-pay costs explain part of the sales and marketing gap, so this is a note for the operator, not a flag.
- **Related planted flag:** PF4. The deck and the model say 37 months of runway, but all 24 planned hires, which a roadmap would depend on, leave 19 months.

## 10. Sources

Each page is saved under `raw/product-roadmap-and-demo/`.

- Hustle Fund Angel Squad, "How to demo a product to investors": https://www.hustlefund.vc/post/angel-squad-how-to-use-product-demos-to-convince-angel-investors , `hustlefund_vc_post_angel_squad_how_to_use_product_demos_to_convince_angel_investors.txt`
- NextView (Rob Go): https://nextview.vc/blog/5-common-mistakes-founders-make-when-giving-demos-to-investors/ , `nextview_vc_blog_5_common_mistakes_founders_make_when_giving_demos_to_investors.txt`
- Holloway, Angel Investing: Start to Finish, product diligence (preview): https://www.holloway.com/g/angel-investing/sections/diligence-on-product-and-technology , `holloway_com_g_angel_investing_sections_diligence_on_product_and_technology.txt`
- CRV, seed pitch: https://www.crv.com/content/what-investors-look-for , `crv_com_content_what_investors_look_for.txt`
- CRV, Series A pitch deck: https://www.crv.com/content/series-a-pitch-deck , `crv_com_content_series_a_pitch_deck.txt`
- Tomasz Tunguz: https://www.tomtunguz.com/breaking-down-a-typical-vcstartup-diligence-process/ , `tomtunguz_com_breaking_down_a_typical_vcstartup_diligence_process.txt`
- YC, how to raise a seed round: https://www.ycombinator.com/blog/how-to-raise-a-seed-round/ , `ycombinator_com_blog_how_to_raise_a_seed_round.txt`
- a16z, data rooms: https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/ , `a16z_com_the_insiders_guide_to_data_rooms_what_to_know_before_you_raise.txt`
- Hunter Walk: https://hunterwalk.com/2022/08/01/three-startup-pitch-deck-mistakes-that-are-red-flags-for-venture-investors/ , `hunterwalk_com_2022_08_01_three_startup_pitch_deck_mistakes_that_are_red_flags_for_venture_investors.txt`
- TechCrunch, Kamps: https://techcrunch.com/2022/12/11/the-ask , `techcrunch_com_2022_12_11_the_ask.txt`
- Digital Commerce 360 on the Nate indictment (news): https://www.digitalcommerce360.com/2025/04/11/nate-ecommerce-ceo-charged-fraud-fake-ai-claims/ , `digitalcommerce360_com_2025_04_11_nate_ecommerce_ceo_charged_fraud_fake_ai_claims.txt`; Decrypt (news): https://decrypt.co/314469/startup-ceo-charged-ai-humans-philippines , `decrypt_co_314469_startup_ceo_charged_ai_humans_philippines.txt`
- Visible (vendor view): https://visible.vc/blog/what-to-include-in-your-data-room/ , `visible_vc_blog_what_to_include_in_your_data_room.txt`
- Also saved: Octopus Ventures on seed and Series A diligence https://octopusventures.com/guides/seed-and-series-a-deals-nailing-due-diligence/ ; SaaStr on diligence timing https://www.saastr.com/how-when-why-vcs-do-due-diligence-pre-and-post-term-sheet ; Wiss on use-of-funds slides https://wiss.com/the-investors-perspective-how-pitch-decks-often-miss-the-point/ ; madewithlove (a technical diligence firm) https://madewithlove.com/blog/5-red-flags-for-vcs-when-planning-to-invest-in-seed-or-series-a-companies.md ; Adamant https://adamant.beehiiv.com/p/good-deck-goes-bad-fundraising-fieldnotes-62524
- Blocked: the Justice Department release on Nate (justice.gov, bot check) and the SEC litigation release and complaint (sec.gov, HTTP 403). The orchestrator can read them in a browser: https://www.justice.gov/usao-sdny/pr/tech-ceo-charged-artificial-intelligence-investment-fraud-scheme , https://www.sec.gov/enforcement-litigation/litigation-releases/lr-26282
- I found no investor source on checking a roadmap against a headcount plan. That check is my proposal.
