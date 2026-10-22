# Pitch deck

**In one line:** the deck is the list of claims. Tricorder reads it first, turns every number into a claim, and then looks for the file that proves each one.

Written 2026-10-22 for the Tricorder document guides (group: story). Every quote below was checked word for word against the saved page by `raw/_verify_story/verify_quotes_story.py`; the rows are in `quotes_story.csv`. Where a quote comes from a company that sells data rooms or deck tools, it is marked as a vendor view. Where an investor's words reach me only through a news article, I paraphrase and say so.

## 1. What it is

The deck is a 10 to 20 slide presentation that tells the company's story and states its numbers. The CEO prepares it, sometimes with a coach or the finance lead. It arrives as a PDF, or as a tracked link (DocSend and similar tools). Sequoia's long-standing outline starts with "Start here: define your company in a single declarative sentence." and then runs through problem, solution, why now, market, competition, business model, team, financials and vision ([Sequoia](https://www.sequoiacap.com/article/writing-a-business-plan/)).

Investors give it little time. DocSend, now part of Dropbox and a vendor of deck sharing, says: "our data shows that investors spend less than 3 minutes reviewing pitch decks these days." ([Dropbox/DocSend, vendor view](https://www.dropbox.com/resources/docsend-pitch-deck-research)) CRV says most seed decks run 10 to 15 slides: "Most seed decks land in the 10 to 15 slide range and rarely need more than 20." ([CRV](https://www.crv.com/content/what-investors-look-for)) The law firm Wilson Sonsini says: "Keep this deck short and focused. 12 to 14 slides may work – 25 slides will not." ([Wilson Sonsini](https://www.wsgr.com/images/content/2/6/26592/Pitching-to-US-VCs.pdf))

## 2. At seed and at Series A

It is expected at both stages, and it is the one document every investor asks for first (a16z lists it first in its data room guide).

- **Seed:** a story with a few numbers. a16z says: "At a minimum, the deck should include your company’s thesis, product vision, competitive landscape, traction, and team, as well as a rough road map or plan for how you will use the funds." ([a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/)) CRV adds: "Conservative growth models also outperform hockey stick projections at seed, where investors know your financial forecasts are educated guesses at best." ([CRV](https://www.crv.com/content/what-investors-look-for))
- **Series A:** a set of numbers with a story around it. CRV: "Seed decks often open with a problem narrative, while Series A decks more often lead with traction before revisiting the problem for context." and "Every slide in your deck should pair vision with verifiable proof" ([CRV](https://www.crv.com/content/series-a-pitch-deck)). CRV also says Series A traction grows from one slide to several, with growth, margin, customer acquisition cost, payback and retention. Peony, a data room vendor, puts the change this way: a seed room presents and a Series A room proves ([Peony, vendor view](https://www.peony.ink/blog/series-a-data-room)).
- **What changes for Tricorder:** at seed the deck may be the only place a number appears, so a claim with no second source is normal and reads as "not enough in the room". At Series A the same claim should have a file behind it.

## 3. What a first pass checks

In this order:

1. What does each slide claim? List every number with its slide, label, period and definition.
2. Is there a file in the room for each number? Peony: "Everything in the deck is a claim; everything in the room is the proof." ([Peony, vendor view](https://www.peony.ink/blog/series-a-data-room))
3. Do the deck's numbers match the model, the metrics export, the one-pager and what the founder says on video?
4. Does the deck show the whole history, or only part of it (a chart that starts after the first revenue month, skipped months, a hidden dip)?
5. What do the definitions hide? "Customers" against paying customers, ARR against MRR, one-time fees, pilots.
6. Is each chart honest? Cumulative lines for metrics that should not be cumulative, axes that start above zero.
7. Does the ask make sense? Amount, the milestones the money reaches, use of funds, and the round in the cap table.
8. Do the market and competition slides stand up? (See the market guide.)
9. Do the team slide's claims match the bios?
10. Does the story match what is online?

## 4. Green flags

- **Every number can be traced to a file.** Visible, a vendor, says: "Every claim in the deck needs to be backed by a document somewhere in the room." ([Visible, vendor view](https://visible.vc/blog/what-to-include-in-your-data-room/)) A deck whose claims all find a second source in the room is the strongest sign Tricorder can show.
- **The deck and the one-pager agree.** Visible says the opposite is the usual first damage: "Internal contradictions between the two are the most common credibility hit at the opening of diligence." ([Visible, vendor view](https://visible.vc/blog/what-to-include-in-your-data-room/))
- **Vision paired with proof** at Series A (CRV quote above), with one clear proof point on the opening slide.
- **The ask names milestones, not just months.** Hunter Walk, a seed investor, headlines this point: "Focus on Milestones You’ll Use This Funding Round to Achieve, Not Just Time It Buys You" and "Tell me what you’re going to accomplish with my dollars as the headline." ([Hunter Walk](https://hunterwalk.com/2022/08/01/three-startup-pitch-deck-mistakes-that-are-red-flags-for-venture-investors/))
- **A short, plain leave-behind.** YC: "Generally make sure the slide deck is a coherent leave-behind." ([YC](https://www.ycombinator.com/blog/how-to-raise-a-seed-round/)) DocSend's data shows something related: "First, none of the successful decks in our dataset had tables of contents, but instead got right to the point and didn’t bother with any extraneous information." ([Dropbox/DocSend, vendor view](https://www.dropbox.com/resources/docsend-pitch-deck-research)) Treat that as vendor data on a small sample.
- **The founder can speak to the numbers left out.** A Columbia Business School venture professor told TechCrunch that founders pick the few numbers that look best and that an investor's job is to ask about the rest; a founder who can explain what they left out is a good sign. This is TechCrunch's report of her words, so I paraphrase it ([TechCrunch](https://techcrunch.com/2023/08/08/liar-liar-pants-on-fire/)).

## 5. Red flags and pitfalls

Common:

- **The deck and the model disagree.** a16z gives the standard example: "Numbers that aren’t consistent with what’s in the deck. For example, your deck says $2M in ARR, but your model shows $1.5M." ([a16z](https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/)) CRV: "When burn or revenue differs between the deck, the model and the accounting records, the gap suggests carelessness or something worse, and either reading damages the deal." ([CRV](https://www.crv.com/content/what-is-a-data-room)) And CRV: "Your annual recurring revenue (ARR) in the deck should reconcile to the underlying billing, contract and revenue schedules." (same page). Angel Investors Network, which sells marketing and education, calls inconsistent numbers "a critical red flag" and explains why: "Inconsistent numbers are a critical red flag because they indicate either carelessness (the founder does not review their own materials) or deception (different numbers are presented to create different impressions)." ([Angel Investors Network, educator view](https://angelinvestorsnetwork.com/capital-raising/how-to-identify-red-flags-pitch-deck))
- **Only part of the history.** The associate quoted in the voice-of-the-customer research: "If revenue in the deck doesn’t match the P&L, or you show only part of your history, everything else becomes questionable." ([Startups Magazine](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal)) Ken has asked for this check as the `deck-vs-books` roadmap slice.
- **Odd or invented metrics.** SaaStr's founder Jason Lemkin: "Weird metrics like “Quarterly MRR” or odd ways to describe revenue are immediate flags." ([SaaStr](https://www.saastr.com/as-a-venture-capitalist-what-are-some-red-flags-that-would-make-you-reject-a-startup-immediately))
- **A cumulative number shown as activity.** a16z: "registered users is one of those dreaded “cumulative” metrics that can go up-and-to-the-right even when a business is shrinking." and "Metrics that should never be reported in a cumulative fashion include revenue, new users, and bookings." ([a16z](https://a16z.com/16-more-startup-metrics/))
- **A weak ask slide.** Haje Jan Kamps, a pitch coach writing in TechCrunch, lists the usual mistakes, among them "Including a valuation on the slide." and "Omitting what the funds will be used for." ([TechCrunch](https://techcrunch.com/2022/12/11/the-ask))
- **An exit slide in a seed deck.** Hunter Walk: "Don’t Put an Exit Slide in a Seed Deck (or any deck before growth round IMO)". ([Hunter Walk](https://hunterwalk.com/2022/08/01/three-startup-pitch-deck-mistakes-that-are-red-flags-for-venture-investors/)) It is a style flag, not a numbers flag, so Tricorder notes it and does not score it.
- **Bios that feel inflated.** Same post: "Founder/Team Bios Which Feel Deceptive".
- **A Series A deck that reads like a seed deck.** CRV: "Investors discount hypotheticals to zero because the work hasn’t actually been done." ([CRV](https://www.crv.com/content/series-a-pitch-deck))
- **Unclear why you win.** Lemkin: "In a competitive space, not being clear on why you are different and why you win." is close to an immediate pass (same SaaStr page).

Rare but serious:

- **Numbers that are made up.** In 2025 a federal jury convicted the founder of the student-aid startup Frank of fraud for inflating its customer count to win a $175 million sale to JPMorgan Chase; prosecutors said the real count was about one tenth of what was shown ([PYMNTS](https://www.pymnts.com/legal/2025/frank-founder-charlie-javice-convicted-of-175-million-fraud/), news report, paraphrased). TechCrunch reports that SoftBank sued the events app IRL after an investigation found most of its users were fake ([TechCrunch](https://techcrunch.com/2023/08/08/liar-liar-pants-on-fire/), paraphrased). Tricorder does not detect fraud. It finds differences in reporting; a fake that is the same in every file gets through.

## 6. How Tricorder checks it

**What a script can check**

- `Deck claim extraction` (FRAMEWORKS 1.1): parse the claims page or slide text into rows of label, value and slide; re-parse each quote to a number, so the model cannot change "$2.5M" into another figure.
- `deck_claim_vs_named_cell` (1.5): pair each deck number with the model's named cell, the metrics export and the one-pager; flag a gap above the match tolerance.
- `cumulative_column_shown_as_active` (1.8): test whether a customer or user count equals the last value of a cumulative column.
- `cap_table_reconcile` (1.10) for the ask: raise, pre-money and ownership against the cap table.
- The rebuilt numbers from 1.2 to 1.9 (ARR, retention, burn, concentration, margin, unit economics), each set against the deck's claim.
- Proposed `history_complete`: from the deck's chart data (or the claims sidecar) and the P&L, compute `first_plotted_month`, `last_plotted_month` and `months_plotted`; flag a chart that starts after the first revenue month or plots fewer months than the P&L holds.
- Proposed `use_of_funds_sums`: the lines add to the raise, and the percentages times the raise equal the amounts. Also print the function split next to the hiring plan's split (see the roadmap guide).
- Proposed `deck_as_of`: the deck's stated date against the room's date.

**What needs a model to read**

- Pull each claim from each slide with its exact words and slide number; the script re-parses the number.
- Match labels that differ ("clinics", "logos", "paying accounts") and spot a different date or definition behind the same label.
- Read charts (vision): what the axis starts at, which months are plotted, whether the line is cumulative.
- Mark claims that carry no number ("we win because...") as not checkable from the room.
- Read the team slide's claims and flag the ones the bios do not support.

**What Tricorder cannot check (leave to the operator)**

- Whether a number is true when every file repeats it. Customer calls, reference calls and a bank check settle that.
- Whether this is the same deck the founder sent other investors.
- The quality of the story and the pitch. That is the partner's judgment.

## 7. Which readout pieces it feeds

- **The pitch itself.** Checklist items: "Pitch deck" (id C60), "Every number on the deck pulled out as a claim and tied to a file" (C64), "Deck numbers match the model and the metrics export" (C65), "The ask on the deck matches the round in the cap table" (C67), "No chart with a truncated y-axis, or a cumulative chart..." (C70), "Use of funds plan for this round" (C96, not checked yet) and "The founder walks from the source data to each flagged number" (C71).
- **Every business piece**, through each claim's label: traction and revenue, retention, burn and runway, unit economics, customers, market and team. The deck's claims are the starting list for all of them.
- **The ask list**, through any deck number with no file behind it.

## 8. If it is missing

- **Seed:** a gap, not a flag. The operator may hold the deck outside the room. Without it Tricorder has no claim list, and the framework returns one gap: "Not in the room: the pitch deck".
- **Series A:** a bigger gap, because the deck is what the rest of the room is tested against. Still not a flag.
- **Ask-list line:** "Please send the current deck, the version you sent to other investors, with its date."

## 9. In the Hollis Voice room

The room holds `01_overview/pitch_deck.pdf`, 14 slides, in the full room and the seed drop. Slide 14 is a claims page with 14 rows. Six of the 14 rows are named by planted flags (ARR, clinics, largest customer, gross margin, net revenue retention, runway); the script `raw/pitch-deck/hollis_deck_claims_vs_flags.py` lists them (output saved beside it).

Planted flags that show up in the deck:

- **ARR, slide 3:** the deck says $2.5M; the model says $2,240,868, a gap of $259,132. The one-page overview repeats the deck's figure.
- **Clinics, slide 3:** 357 is the last value of the cumulative accounts-created column; 212 accounts pay.
- **Largest customer, slide 4:** "No customer above 9% of ARR"; the largest is 21.0% of MRR. (Needs the second tier.)
- **Gross margin, slide 5:** 80%; 58.1% with hosting, model usage, phone costs, licences and support in cost of revenue.
- **Retention, slide 6:** 102.6% net revenue retention; 87.3% rebuilt from the customer file. (Needs the second tier.)
- **Runway, slide 11:** 37 months; 19 months once all 24 planned hires are paid.

Green flags in the deck:

- **The round adds up:** $9,000,000 on slide 13, in the cap table and in the model (three files).
- **The market figure is stated the same way** on slide 8 and in the model's Market tab, and both call it a company estimate.
- **Headcount agrees:** 17 today on slide 10 and in the model; 41 after hiring on slide 12 and in the hiring plan.

Decoys the deck must not trigger: slide 7 says the $500 onboarding fee "is not part of recurring revenue", and slide 4 mentions that Brookline Row pays once a year in advance. Both are handled correctly in the data. The use-of-funds lines on slide 13 add to $9,000,000.

## 10. Sources

Each page is saved under `raw/pitch-deck/`.

- Sequoia, "Writing a business plan": https://www.sequoiacap.com/article/writing-a-business-plan/ , `sequoiacap_com_article_writing_a_business_plan.txt`
- CRV, seed pitch: https://www.crv.com/content/what-investors-look-for , `crv_com_content_what_investors_look_for.txt`
- CRV, Series A pitch deck: https://www.crv.com/content/series-a-pitch-deck , `crv_com_content_series_a_pitch_deck.txt`
- CRV, what is a data room: https://www.crv.com/content/what-is-a-data-room , `crv_com_content_what_is_a_data_room.txt`
- a16z, data rooms: https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/ , `a16z_com_the_insiders_guide_to_data_rooms_what_to_know_before_you_raise.txt`
- a16z, 16 more startup metrics: https://a16z.com/16-more-startup-metrics/ , `a16z_com_16_more_startup_metrics.txt`; 16 startup metrics: https://a16z.com/16-startup-metrics/ , `a16z_com_16_startup_metrics.txt`
- YC, how to raise a seed round: https://www.ycombinator.com/blog/how-to-raise-a-seed-round/ , `ycombinator_com_blog_how_to_raise_a_seed_round.txt`
- Wilson Sonsini, "Pitching to US VCs": https://www.wsgr.com/images/content/2/6/26592/Pitching-to-US-VCs.pdf , `wsgr_com_images_content_2_6_26592_Pitching_to_US_VCs_pdf.txt`
- Hunter Walk, three deck mistakes: https://hunterwalk.com/2022/08/01/three-startup-pitch-deck-mistakes-that-are-red-flags-for-venture-investors/ , `hunterwalk_com_2022_08_01_three_startup_pitch_deck_mistakes_that_are_red_flags_for_venture_investors.txt`
- Hunter Walk, competitive 2x2: https://hunterwalk.com/2020/05/25/if-your-pitch-deck-has-a-competitive-2x2-im-going-to-ask-you-this-question/ , `hunterwalk_com_2020_05_25_if_your_pitch_deck_has_a_competitive_2x2_im_going_to_ask_you_this_question.txt`
- SaaStr (Jason Lemkin), 13 things that say "don't fund me": https://www.saastr.com/as-a-venture-capitalist-what-are-some-red-flags-that-would-make-you-reject-a-startup-immediately , `web_saastr_com_as_a_venture_capitalist_what_are_some_red_flags_that_would_make_you_reject_a_startup_immediately.txt`
- TechCrunch, Kamps, "The one slide 95% of founders get wrong": https://techcrunch.com/2022/12/11/the-ask , `techcrunch_com_2022_12_11_the_ask.txt`
- TechCrunch, Szkutak, "No, it's never too early to make sure a founder is telling the truth": https://techcrunch.com/2023/08/08/liar-liar-pants-on-fire/ , `techcrunch_com_2023_08_08_liar_liar_pants_on_fire.txt`
- TechCrunch, Cutler, DocSend study of 200 decks (2015, small sample): https://techcrunch.com/?p=1167693 , `techcrunch_com_p_1167693.txt`
- Startups Magazine, associate quote: https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal , `web_startupsmagazine_co_uk_how_to_build_a_data_room_that_closes_the_deal.txt`
- PYMNTS on the Frank verdict (news): https://www.pymnts.com/legal/2025/frank-founder-charlie-javice-convicted-of-175-million-fraud/ , `pymnts_com_legal_2025_frank_founder_charlie_javice_convicted_of_175_million_fraud.txt`
- Vendor and educator views: Dropbox/DocSend https://www.dropbox.com/resources/docsend-pitch-deck-research , `dropbox_com_resources_docsend_pitch_deck_research.txt`; Visible https://visible.vc/blog/what-to-include-in-your-data-room/ , `visible_vc_blog_what_to_include_in_your_data_room.txt`; Peony https://www.peony.ink/blog/series-a-data-room , `peony_ink_blog_series_a_data_room.txt`; Angel Investors Network https://angelinvestorsnetwork.com/capital-raising/how-to-identify-red-flags-pitch-deck , `angelinvestorsnetwork_com_capital_raising_how_to_identify_red_flags_pitch_deck.txt`
- Also saved and read, not quoted: Jia Lin Yong (VC) on seed deck mistakes https://jialinyong.substack.com/p/common-mistakes-in-pre-seedseed-decks ; Alexander Jarvis, 40 pitch red flags https://www.alexanderjarvis.com/40-pitch-red-flags-which-will-undermine-your-startup-fundraise/ ; Liam Gill, 3 red flags https://persuade-and-raise.beehiiv.com/p/3-red-flags-pitch-decks ; the SaaStr summary of Michael Seibel's pitch talk.
- The YC library page "How to build your seed round pitch deck" loads by script with no text, so I did not use it (saved as `ycombinator_com_library_2u_how_to_build_your_seed_round_pitch_deck.txt`).
