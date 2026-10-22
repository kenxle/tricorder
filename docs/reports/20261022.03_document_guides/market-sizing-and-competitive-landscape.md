# Market sizing and competitive landscape

**In one line:** investors size the market themselves, so this document is a test of how the founder thinks. Tricorder rebuilds the market from a customer count times a price, and reads the competition slide for who is missing.

Written 2026-10-22 for the Tricorder document guides (group: story). Every quote below was checked word for word against the saved page by `raw/_verify_story/verify_quotes_story.py`; the rows are in `quotes_story.csv`. Vendor views are marked.

## 1. What it is

Two parts that Tricorder's table treats as one document:

- **Market sizing:** the founder's estimate of how much revenue the product could earn, in layers. CRV, a seed and Series A fund, defines them: TAM is "the full revenue available at complete market share", SAM is the slice the current product and distribution can reach, and SOM is what the company can realistically win in three to five years ([CRV](https://www.crv.com/content/how-investors-evaluate-market-size)).
- **Competitive landscape:** who else sells to the same buyers, shown as a table, a two by two chart or a paragraph. It includes indirect rivals and the status quo.

The CEO prepares both. They usually sit on one or two deck slides, sometimes in a model tab or a short memo. Visible, a vendor, lists market sizing and the competitive landscape as two rows, both included at every stage ([Visible, vendor view](https://visible.vc/blog/what-to-include-in-your-data-room/)).

## 2. At seed and at Series A

It is expected at both stages in the deck, but a separate file is optional. a16z lists market sizing among the documents it does not need: "Market sizing. We’ll do our own work sizing the market." ([a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/)) Tunguz, a venture investor, does the same check first after a meeting: "The first thing is to verify market size and whether it foots with the data the company presented." ([Tunguz](https://www.tomtunguz.com/breaking-down-a-typical-vcstartup-diligence-process/))

What CRV expects at each stage:

- **Pre-seed:** "Investors are buying your read on the market more than the market itself."
- **Seed:** "The working threshold at most institutional funds moves into billion-dollar territory." YC's guide says the same in its own way: "Total Available Market (TAM) >$1B if possible." ([YC](https://www.ycombinator.com/blog/how-to-raise-a-seed-round/))
- **Series A:** "Funds at this stage need a market that supports a venture scale revenue outcome." and "The sizing also has to reconcile with recurring revenue you can already show". (CRV, same page as above.)

At every stage CRV says: "At every one of these stages, we’ve seen a number you can defend do more for a founder than a big one."

So what changes is the proof. At seed the logic is judged. At Series A the market figure must square with the company's own recurring revenue and its hiring plan.

## 3. What a first pass checks

1. Which layers does the deck give (TAM, SAM, SOM), and what are the figures?
2. Is each built bottom-up (a count of customers times a price) or top-down (a share of a large industry figure)? CRV: "A top-down figure presented alone draws more skepticism than almost anything else on a market slide."
3. Is each input named, sourced and dated? CRV: "Imprecision is fine, provided you can identify the customers counted and the price used."
4. Does the price per customer match what customers pay in the room today?
5. Is the market drawn tightly? CRV: "A tight market definition reads as research; a broad one reads as a guess."
6. Does the obtainable layer fit the revenue plan, the raise and the hiring plan? CRV: "Your obtainable market has to line up with the amount you're raising, the financial model and the hiring plan."
7. Who is named as competition: direct rivals, indirect ones, the old way of doing it?
8. Does the competitor chart hold up when the competitors look at it?
9. Do outside signals on the named competitors (hiring, traffic, reviews, pricing, wins) tell a different story?

## 4. Green flags

- **Bottom-up math with named inputs.** CRV, above. A bottom-up figure and a top-down cross-check that are close is better still; CRV says investors "examine the bottom-up model customer by customer and use the published total as a cross-check" (same page).
- **A defensible number rather than a big one** (CRV quote above), including a figure that is smaller than the fund's usual threshold but well argued.
- **A tight definition and a reconciled obtainable layer** (CRV quotes above). CRV: "SOM draws more scrutiny than the other two layers, because it is the only one that has to reconcile with the revenue line in your financial model." ([CRV](https://www.crv.com/content/how-investors-evaluate-market-size))
- **Two files that state the same market figure.** Tricorder counts this as agreement, with the note that both come from the company.
- **Competition shown honestly.** The authors of Angel Investing: Start to Finish tell investors to "Start with the list of competitors provided by the company and look at those products closely." ([Holloway](https://www.holloway.com/g/angel-investing/sections/diligence-on-competition)) A founder who names the leaders and says where the product is weaker passes that test.
- **A clear reason to win.** SaaStr's Jason Lemkin counts the lack of one as close to an immediate pass: "In a competitive space, not being clear on why you are different and why you win." ([SaaStr](https://www.saastr.com/as-a-venture-capitalist-what-are-some-red-flags-that-would-make-you-reject-a-startup-immediately))

## 5. Red flags and pitfalls

Common:

- **Founders overestimate the market.** A fund partner who built his own ten-agent diligence tool says the finding it raises most often is founders overestimating market size (Tech.eu, paraphrased: [Tech.eu](https://tech.eu/2026/08/25/inside-startup-due-dil-the-ai-tool-turning-hours-of-vc-diligence-into-10-minutes/)).
- **A top-down figure on its own, with no customer count or price.** CRV lists "Presenting a filtered report figure with no customer count or price behind it, which leaves an investor unable to test a single input." ([CRV](https://www.crv.com/content/how-investors-evaluate-market-size))
- **Claiming the whole category.** CRV: "Sizing the market as the entire industry when your product serves one segment of it."
- **Out-of-date figures and transaction volume shown as revenue.** CRV lists both ("Citing figures that have aged out:" and "Confusing transaction volume with revenue:"). The second is a mislabel of the kind Tricorder's accounting-mislabel entry (FRAMEWORKS 1.12) checks in the financials.
- **"We have no competitors."** Rafferty Jackson, an angel and pitch judge, writes: "The blank competitor slide is a tombstone of naivety, not a dramatic demonstration of a great business." ([Once Upon a Pitch](https://raffertyjackson.substack.com/p/the-no-competitor-nonsense)) The Holloway book says: "If a company says there is no competition it may be a red flag that they don’t understand their customers or their market." ([Holloway](https://www.holloway.com/g/angel-investing/sections/diligence-on-competition)) Wilson Sonsini's list for a summary says "Your competition (and don’t say that there isn’t any!)" ([Wilson Sonsini](https://www.wsgr.com/images/content/2/6/26592/Pitching-to-US-VCs.pdf)).
- **A two by two with the company alone in the top right.** Hunter Walk, a seed investor: "I’m going to ask you what the competitors on the slide would say about it if they were critiquing the matrix categories and their placement." ([Hunter Walk](https://hunterwalk.com/2020/05/25/if-your-pitch-deck-has-a-competitive-2x2-im-going-to-ask-you-this-question/)) CRV says it no longer works: "A two by two matrix with your company conveniently placed in the top right corner no longer works." ([CRV](https://www.crv.com/content/what-investors-look-for))
- **A capture percentage with no basis.** CRV lists "Assigning share with no basis" among the usual mistakes (same market page).

Rare but serious:

- **A leader the founder does not know about.** Holloway: "If the entrepreneur was really unaware of clearly competitive products (unless they are very niche) that might be a red flag that they have not done enough homework on their own market." ([Holloway](https://www.holloway.com/g/angel-investing/sections/diligence-on-competition))
- **A large market with an entrenched leader.** CRV: "A large market with an entrenched leader is often a worse opportunity than a smaller fragmented one." This is a judgment for the partner, not a document error.

## 6. How Tricorder checks it

**What a script can check**

- **Bottom-up rebuild** (FRAMEWORKS 5.6, after Saturday). `ACV = rebuilt recurring ARR ÷ paying accounts`; `TAM = cited count of potential customers × ACV`; `SAM = cited count of reachable customers × ACV`; `SOM = customers the plan adds × ACV`, checked against the sales hires in the hiring plan; `deck_gap = deck TAM ÷ bottom-up TAM`. The entry will not use a count from memory. With no cited count it returns "Not in the room: a cited count of target customers".
- **The deck's own arithmetic:** clinics times price equals the stated TAM (`MARKET_CLINICS × MARKET_ACV_USD = MARKET_TAM_USD`), and deck slide and model tab agree. This is `deck_claim_vs_named_cell` (1.5) on the market claims.
- **Proposed `planning_acv_vs_observed_acv`:** `planning ÷ observed − 1`, where planning is the price per customer in the market estimate and observed is subscription ARR per paying account from the customer file.
- **Proposed `competitor_names_present`:** count the companies named on the competition slide. Zero is a gap. Entries 3.1 (hiring, web traffic, reviews) and 3.2 (pricing and customer wins) need those names.
- **Proposed `som_vs_sales_capacity`:** customers implied by SOM against sales hires and a quota. It needs a quota and a ramp time from the model; without them it returns a gap.

**What needs a model to read**

- Quote each stated layer and the sentence that says how it was built; say whether it is bottom-up or top-down, with "judged" confidence when the deck does not say.
- Read a customer count from each saved public source, with its geography and year.
- Read the competition slide: direct, indirect and status-quo rivals; claims of "no competitors"; positioning claims with no support.
- Apply the business frameworks (5.4 Porter's five forces, 5.5 SWOT) to the market, with every claim quoted.

**What Tricorder cannot check (leave to the operator)**

- Whether the fund's thesis needs a billion-dollar market. That is the partner's call.
- Whether the product really wins against a named rival. Customer calls and a trial of the rival's product settle that.
- Calls to people in the industry. Tunguz does this himself: "I’ll call a few friends in the industry who can help me better understand the dynamics in the sector."

## 7. Which readout pieces it feeds

- **Market.** Checklist items: "Market sizing and competitive landscape" (id C47), "Bottom-up TAM, SAM and SOM against the deck's market size" (C48), "Competitors' hiring, headcount, web traffic and reviews against the deck's competition slide" (C49) and "Published pricing and announced customer wins, for the company and its competitors" (C50).
- **The pitch itself,** through the deck's market and competition slides.
- **The ask list:** a cited count of target customers, and the names of the nearest competitors.

## 8. If it is missing

- **Seed:** a gap, not a flag. a16z does its own sizing, and Tricorder's rule is that a missing document is a question for the operator.
- **Series A:** a gap that matters more, because the figure has to match the recurring revenue and the hiring plan. Still not a flag.
- **Ask-list line:** "Please send your market sizing: the count of target customers with its source and date, the price per customer, and your three nearest competitors by name."

## 9. In the Hollis Voice room

The room has no separate market document. The market sits on deck slide 8, slide 9 (competition) and the model's `Market` tab. No flag is planted here; this is where the room's market green flag lives.

Numbers from the script `raw/market-sizing-and-competitive-landscape/hollis_market_math.py` (output saved beside it):

- **Green flag:** slide 8 and the model's Market tab agree: about 28,000 independent clinics and a market of $252,000,000, which is the clinics times $9,000. Both are labeled "company estimate", and the model says "No outside source is in the room." The readout reads the market piece as looking strong, with the note that both files come from the company.
- **The price is cautious.** The planning figure of $9,000 is 92.6 percent of what a paying clinic pays today ($9,721 in subscription ARR per paying clinic). The same 28,000 clinics at $9,721 give $272,190,113.
- **No cited customer count.** Entry 5.6 will return the gap "Not in the room: a cited count of target customers" until a source page is attached.
- **Share today:** 212 paying clinics are 0.76 percent of 28,000.
- **Size against the usual threshold:** $252,000,000 is 25.2 percent of one billion dollars. CRV's seed threshold and YC's ">$1B" are about the fund's rules, not about whether the figure is wrong. The partner decides.
- **No named competitors.** Slide 9 compares four columns: answering services, generic AI receptionists, practice software add-ons and Hollis Voice. It names no company. FRAMEWORKS 3.1 lists the competition slide as the source of "the competitor names the founder chose", so on this room the scan has no names to look up. Either the demo deck should name a few real or fictional competitors, or 3.1 should be told to use the category names.
- **One unsupported claim:** "Chains already have call centers. Independent clinics do not." (slide 8).
- **The competition columns name how the others fall short** (a script, a generic tool, a single system) but give no evidence. That is an unsupported positioning claim, not a flag.

## 10. Sources

Each page is saved under `raw/market-sizing-and-competitive-landscape/`.

- CRV, "How investors evaluate market size": https://www.crv.com/content/how-investors-evaluate-market-size , `crv_com_content_how_investors_evaluate_market_size.txt`
- CRV, seed pitch: https://www.crv.com/content/what-investors-look-for , `crv_com_content_what_investors_look_for.txt`
- Tomasz Tunguz: https://www.tomtunguz.com/breaking-down-a-typical-vcstartup-diligence-process/ , `tomtunguz_com_breaking_down_a_typical_vcstartup_diligence_process.txt`
- a16z, data rooms: https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/ , `a16z_com_the_insiders_guide_to_data_rooms_what_to_know_before_you_raise.txt`
- YC, how to raise a seed round: https://www.ycombinator.com/blog/how-to-raise-a-seed-round/ , `ycombinator_com_blog_how_to_raise_a_seed_round.txt`
- Hunter Walk, the competitive 2x2: https://hunterwalk.com/2020/05/25/if-your-pitch-deck-has-a-competitive-2x2-im-going-to-ask-you-this-question/ , `hunterwalk_com_2020_05_25_if_your_pitch_deck_has_a_competitive_2x2_im_going_to_ask_you_this_question.txt`
- Rafferty Jackson, "The no competitor nonsense": https://raffertyjackson.substack.com/p/the-no-competitor-nonsense , `raffertyjackson_substack_com_p_the_no_competitor_nonsense.txt`
- Holloway, Angel Investing: Start to Finish, "Diligence on competition" (preview): https://www.holloway.com/g/angel-investing/sections/diligence-on-competition , `holloway_com_g_angel_investing_sections_diligence_on_competition.txt`
- SaaStr (Jason Lemkin): https://www.saastr.com/as-a-venture-capitalist-what-are-some-red-flags-that-would-make-you-reject-a-startup-immediately , `web_saastr_com_as_a_venture_capitalist_what_are_some_red_flags_that_would_make_you_reject_a_startup_immediately.txt`
- Wilson Sonsini, "Pitching to US VCs": https://www.wsgr.com/images/content/2/6/26592/Pitching-to-US-VCs.pdf , `wsgr_com_images_content_2_6_26592_Pitching_to_US_VCs_pdf.txt`
- Sequoia, "Writing a business plan" (its competition step reads "Who are your direct and indirect competitors. Show that you have a plan to win."): https://www.sequoiacap.com/article/writing-a-business-plan/ , `sequoiacap_com_article_writing_a_business_plan.txt`
- Tech.eu (news), paraphrased: https://tech.eu/2026/08/25/inside-startup-due-dil-the-ai-tool-turning-hours-of-vc-diligence-into-10-minutes/ , `web_tech_eu_2026_08_25_inside_startup_due_dil_the_ai_tool_turning_hours_of_vc_diligence_into_10_minutes.txt`
- Vendor view: Visible https://visible.vc/blog/what-to-include-in-your-data-room/ , `visible_vc_blog_what_to_include_in_your_data_room.txt`
- Saved and read, not quoted: Alexander Jarvis, 40 pitch red flags https://www.alexanderjarvis.com/40-pitch-red-flags-which-will-undermine-your-startup-fundraise/ ; Launchrock on market size https://www.launchrock.com/library/expert-advice/market-size ; Causo (a deck vendor) on the TAM slide https://hub.causo.ai/guides/tam-slide-market-size ; BD Emerson on TAM https://www.bdemerson.com/article/total-addressable-market ; Omnipitch on competitors https://omnipitch.substack.com/p/my-competitors-arent-close ; Papermark on the competitor slide https://www.papermark.com/blog/competitor-analysis-pitch-deck.md
- I looked for a Tomasz Tunguz or a16z post on market sizing by name and did not find one by search. The CRV guide is the fullest investor source I found; it is written by a fund that sells its attention to founders, so read it as a fund's stated view.
