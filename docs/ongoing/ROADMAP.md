# Roadmap

## Charter

**What belongs:** What gets built and in what order, grouped by horizon: now to Friday night, and Saturday. Everything in the product brief and [FEATURES.md](FEATURES.md) is built by the end of Saturday's demo. What each slice waits on. For Saturday, who builds each slice and its hour budget, and the run of show.

**What does not:** Dates promised to anyone. Work in flight; that lives on the board. How a slice works inside; that goes in its feature folder and in [ARCHITECTURE.md](ARCHITECTURE.md).

**Level of detail:** One slice per heading, with short lists. A builder can pick up a slice and know what done looks like.

**Sources:** The writers' brief ([00_brief_for_writers.md](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), every "Added" block from 10:15 AM through the 2:49 PM block on live demos with real YC companies), Ken's 2:21 PM edit to the product brief (steering easy enough for a partner, [PRODUCT_BRIEF.md](PRODUCT_BRIEF.md), "Steering the readout"), the landscape research's Part 5 on Startup Due Dil ([research_landscape.md](../reports/20261022.02_research/research_landscape.md)), the gaps research ([research_gaps.md](../reports/20261022.02_research/research_gaps.md)), the data room as generated ([data_room/README.md](../../data_room/README.md), [SEALING.md](../../data_room/SEALING.md), `data_room/answer_key.json`), the overview page's cards ([00_overview.md](../features/20261022.01_hackathon_plan/00_overview.md)), Ken's comments on the voice-of-the-customer research at 1:47 PM (the outside-in slice) and 1:50 PM (reference checks, low priority), the product brief's "What Tricorder gathers before the data room is opened" ([PRODUCT_BRIEF.md](PRODUCT_BRIEF.md)), the saved Plaid Sandbox page ([sandbox_user_custom.md](../reports/20261022.02_research/raw/feasibility/plaid/sandbox_user_custom.md)), the organisers' tracks ([problem_tracks.txt](../reports/20261022.01_hackathon_sources/problem_tracks.txt)), the feasibility research ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), the main source for scan order, stack, folder owners and keys), the data room research ([research_data_room.md](../reports/20261022.02_research/research_data_room.md)), the landscape research ([research_landscape.md](../reports/20261022.02_research/research_landscape.md)), the voice-of-the-customer research ([research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md)), the guardrails ([guardrails.md](../../.claude/guardrails.md)), the board ([BULLETIN.md](../BULLETIN.md)) and the three critiques ([judge](../features/20261022.01_hackathon_plan/critique_judge.md), [buildability](../features/20261022.01_hackathon_plan/critique_buildability.md), [demo](../features/20261022.01_hackathon_plan/critique_demo.md)), which set the Saturday slices, the demo opening and the beat sheet. The shape is copied from My Text Reminders' [ROADMAP.md](../../../my-text-reminders/docs/ongoing/ROADMAP.md). Hour budgets come from [the schedule](../features/20261022.01_hackathon_plan/00_brief_for_writers.md) and are added up by [check_saturday_hours.py](../features/20261022.01_hackathon_plan/check_saturday_hours.py), not by hand.

## How to read a slice

- **Waits on** names the slices or board rows that must be done first. Board rows are on [BULLETIN.md](../BULLETIN.md).
- **Includes** is the list of what the slice must contain. The reviewer checks the work against it.
- **Done when** is the list of checks that prove it works.
- **Joins on Saturday** appears on agent slices that extend one of the team's Saturday slices. The agent builds the slice before Saturday against the frozen Claim schema, the specs and the example result files in `sample_out/`, the way the readout page is built on Saturday morning before any scan runs. It is merged to `main` before Saturday with its tests passing on those files and on the data rooms. On Saturday it runs on the named slice's real output at the integration points, and any Done when check that needs that output is checked there.
- **Who** names a role: captain, frontend, backend-and-data, design-and-finance, "agent" for agent work from now to Friday night (documents, data, the skeleton and the product slices), or "Ken" for things only Ken can do. The board names the people behind each role.
- **Hours** appears on the team's Saturday slices only. It is a budget inside the six-hour hacking window, not a prediction. When a slice uses up its budget, the captain decides whether it ships as it is or shows saved results on stage, by the [demo fallback order](#demo-fallback-order).
- **Judgment** picks the builder's model when an agent builds or rebuilds the slice. Yes means Opus, because the slice needs design or product calls. No means Sonnet. Ken-only slices say "n/a".

A slice is done when its pull request is merged to `main`. On Saturday the captain merges, and a red CI blocks a merge even in the room ([guardrails.md](../../.claude/guardrails.md)).

## Ken's asks and where they are built

Every feature or behaviour Ken asked for on 2026-10-22, and the slice that builds it. "When Ken said it" is the time the [writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md) gives his words, or the document the ask came from. "When it is built" names the horizon of each linked slice, in link order. A script checks that every link points at a slice in this file and that the horizons match: [check_asks_table.py](../features/20261022.01_hackathon_plan/check_asks_table.py).

Five of the day's blocks are rules with nothing to build: the 1:21 PM block (no research labels in documents), the 1:24 PM block (say, do, pay is not user against buyer), the 1:12 PM rename to "the operator", the 2:35 PM block (the two primary personas are the associate who prepares the memo and the partner who reads it, at seed and Series A funds), and the 3:32 PM note (everything is built by the end of Saturday, and building starts now). The first three bind the documents. The fourth decides who every slice serves first. The last one sets this roadmap's two horizons.

| Ken's ask | When Ken said it | Slice that builds it | When it is built |
|---|---|---|---|
| Red flags in the financials and metrics | 10:15 AM (Track 2 pasted) | [redflag-engine](#redflag-engine) | Saturday |
| A memo where every claim links to its source | 10:15 AM (Track 2 pasted) | [claim-result](#claim-result), [readout](#readout) | Saturday |
| Market signals for the company and its competitors | 10:15 AM (Track 2 pasted) | [outside-in](#outside-in), [market-signals](#market-signals) | Now to Friday night, then Saturday |
| Competitive analysis | about 10:10 AM | [market-signals](#market-signals), [comps](#comps) | Saturday |
| Comps, each with why it is a fair comp | about 10:10 AM | [comps-deep](#comps-deep), [comps](#comps) | Now to Friday night, then Saturday |
| EDGAR full-text search for comps | 10:17 AM | [comps-deep](#comps-deep) | Now to Friday night |
| Financial modeling | about 10:10 AM | [financial-model](#financial-model), [redflag-engine](#redflag-engine) | Now to Friday night, then Saturday |
| A pitch video broken into claims with timestamps | about 10:10 AM | [pitch-video](#pitch-video) | Saturday |
| The video leads you to its interesting parts | about 10:10 AM | [video-moments](#video-moments) | Now to Friday night |
| Business frameworks: lean canvas, jobs to be done and the rest | about 10:10 AM | [frameworks-scan](#frameworks-scan) | Now to Friday night |
| Founder profiles: socials, GitHub, passion, from the industry or not | about 10:10 AM | [founder-profiles](#founder-profiles) | Now to Friday night |
| The company's presence online, including Reddit and Facebook | about 10:10 AM | [online-presence](#online-presence) | Now to Friday night |
| A Reddit mini-browser that saves each page Ken opens | about 10:10 AM | [online-presence](#online-presence) | Now to Friday night |
| The one-page founder brief | 10:18 AM | [founder-brief](#founder-brief) | Now to Friday night |
| A simulated data room | 10:26 AM | [data-room](#data-room) | Now to Friday night |
| Pull pitch decks out of the inbox | 11:20 AM | [inbox-forward](#inbox-forward), [inbox-apis](#inbox-apis) | Now to Friday night |
| Diligence starts on the inbound, before anyone asks | 11:20 AM | [inbound-unasked](#inbound-unasked) | Now to Friday night |
| The investor can see and delete everything pulled | 11:20 AM | [readout-store](#readout-store) | Now to Friday night |
| An overview of which pieces look strong and which look weak | 12:55 PM | [readout](#readout), [readout-page](#readout-page) | Saturday |
| Easy drill-downs to verify and corroborate every number | 12:55 PM | [readout](#readout), [readout-page](#readout-page) | Saturday |
| The readout opens on the best green flags and the worst red flags | 1:09 PM | [readout](#readout), [readout-page](#readout-page) | Saturday |
| The pitch line: "Point it at a startup, get a readout. Tricorder takes any data: decks, videos, spreadsheets, data rooms. It reveals insight you can trust, every claim sourced." | 10:34 AM (team-workshop session, board row TRI-new-pitch) | [demo-script](#demo-script) | Now to Friday night |
| Real green flags in the demo room | 1:09 PM (overview page card) | [data-room](#data-room) | Now to Friday night |
| Steer the readout by rewriting a piece | 1:12 PM | [steering](#steering) | Now to Friday night |
| Steer the readout by getting more info for a piece | 1:12 PM and 1:15 PM | [steering](#steering) | Now to Friday night |
| Angels want diligence and buy it by proxy | 1:27 PM | [product](#product) | Now to Friday night |
| Accounting mislabels, not only ARR that is not recurring | 1:32 PM | [accounting-mislabels](#accounting-mislabels), [redflag-engine](#redflag-engine) | Now to Friday night, then Saturday |
| Find differences in reporting; never claim to catch fraud | 1:33 PM | [demo-script](#demo-script), [bank-check](#bank-check) | Now to Friday night |
| Online research only, no interviews | 1:34 PM | [research-gaps](#research-gaps) | Now to Friday night |
| The same core job as the competitor, plus our extras | 1:36 PM | [product](#product) | Now to Friday night |
| First screens that suit the company's stage | 1:38 PM | [stage-views](#stage-views) | Now to Friday night |
| The operator can reorder the pieces | 1:38 PM (product brief, "The operator sets the order") | [stage-views](#stage-views), [readout-page](#readout-page) | Now to Friday night, then Saturday |
| The associate's ten tabs, opened automatically | 1:47 PM (comment on the voice-of-the-customer research) | [outside-in](#outside-in) | Now to Friday night |
| Reference checks, low priority | 1:50 PM (comment on the voice-of-the-customer research) | [reference-checks](#reference-checks) | Now to Friday night |
| A bank check through a banking connector | 1:52 PM | [bank-check](#bank-check) | Now to Friday night |
| Contracts as an input, checked for gaps such as cancellation periods | 1:53 PM, and 3:17 PM ("include contract terms for sat") | [contract-terms-saturday](#contract-terms-saturday) | Saturday |
| A list of things to ask the founder for | 1:54 PM | [readout](#readout), [readout-page](#readout-page) | Saturday |
| A diligence checklist | 1:56 PM | [checklist](#checklist) | Now to Friday night |
| Coverage against the checklist, and an ask list from missing items at the company's stage | 1:56 PM | [checklist-coverage](#checklist-coverage) | Now to Friday night |
| Help write the partners' memo: an interactive memo with drill-downs, plus a static PDF with footnotes, in a template built from real published memos | 1:58 PM and 2:00 PM | [memo-export](#memo-export) | Now to Friday night |
| Each reader gets their own steerable copy of the memo, and can try what-if changes on the model, marked as scenarios | 2:01 PM | [reader-scenarios](#reader-scenarios) | Now to Friday night |
| A blind room and a clean room against "rigged" | overview page card, "The blind room" | [blind-room](#blind-room), [demo-freeze](#demo-freeze) | Now to Friday night, then Saturday |
| Multiplayer: several people build one readout and split the work (uncertain) | 2:05 PM | [multiplayer](#multiplayer) | Now to Friday night |
| Deck revenue against the P&L, and decks that show only part of the history | 2:19 PM | [deck-vs-books](#deck-vs-books) | Now to Friday night |
| Speed: start every scan as early as its input exists, readout fills in as results land | 2:19 PM | [inbound-unasked](#inbound-unasked) | Now to Friday night |
| Steering easy enough for a partner who runs diligence: one plain sentence on the line that looks wrong, no setup, the answer on that line | 2:21 PM (Ken's edit to the product brief, "Steering the readout") | [steering](#steering) | Now to Friday night |
| The claims workflow: extract claims from the deck and video, check whether the other documents support them | 2:41 PM | [claim-support](#claim-support) | Now to Friday night |
| Templated data rooms with hidden issues, names swapped on the fly, one per problem story | 2:46 PM | [room-templates](#room-templates) | Now to Friday night |
| A reference guide for every document a seed or Series A room can hold: green flags, red flags and pitfalls, and how Tricorder checks it | 2:38 PM | [checklist](#checklist), [checklist-coverage](#checklist-coverage) | Now to Friday night |
| Synthetic rooms for 2 or 3 real YC spring companies so the internet scan runs live | 2:44 PM | [yc-rooms](#yc-rooms), [room-templates](#room-templates) | Now to Friday night |
| Live demos on real YC companies from a list Ken approves, each paired with a fake data room | 2:49 PM | [yc-rooms](#yc-rooms), [demo-script](#demo-script), [market-signals](#market-signals), [demo-freeze](#demo-freeze) | Now to Friday night, then Saturday |
| The sponsor tools (Akta, Crunchbase, Nicrron) in the product, built ahead with keys plugged in on the day | 2:56 PM | [sponsor-adapters](#sponsor-adapters) | Now to Friday night |
| Quick messages to the company asking for information, with guidance on what to submit | 3:15 PM | [founder-requests](#founder-requests) | Now to Friday night |

### Proposals waiting on Ken

These are not slices yet. Ken's board row "Answer the cards" asks which Startup Due Dil ideas to adopt, and he has not rejected any. Each comes from the landscape research's Part 5 ([research_landscape.md](../reports/20261022.02_research/research_landscape.md), "What Tricorder takes from it"). If Ken says yes, the idea becomes a slice in the horizon named here.

- **A yellow tier.** Startup Due Dil sorts findings into red, yellow and green, where yellow means "needs clarification". Tricorder's nearest match is a piece marked mixed, whose question goes on the ask list. The proposal is to name that tier on the page. Now to Friday night, inside [stage-views](#stage-views) or [checklist-coverage](#checklist-coverage).
- **Rerun when thin.** Its orchestrator reruns an agent when an area comes back thin. Tricorder's "get more info" steer does this when the operator asks. The proposal is to run it unasked when a piece reads "not enough in the room" and a source could fill it. Now to Friday night, inside [steering](#steering).
- **Regulatory and legal as their own areas.** Two of its nine specialist areas are regulatory compliance and legal. Tricorder covers them only through the checklist's legal and cap table items. The proposal is a scan for each. Now to Friday night.
- **A founder mode.** Startups run Startup Due Dil on themselves before they raise. The proposal is a founder version: a founder runs the readout on their own room and fixes what disagrees before an investor sees it. Now to Friday night, beside [product](#product).
- **Its prices as a reference.** It charges $49 a report, $449 a month for angels (up to 10 reports) and $999 a month for funds (up to 25 reports) (dev.ua, via the landscape research). The proposal is to use these as a reference point in [product](#product) pricing.

## The one workflow we demo

**Recommended: open on the top green and red flags, already waiting, then the overview, then drill into the weakest piece and one strong piece.** The first screen is the best green flags and the worst red flags for Hollis Voice's full room. Under them is the overview: each piece of the company with its mark (looking strong, looking weak, mixed, or not enough in the room) and its reason in one line ([writers' brief, 12:55 PM and 1:09 PM blocks](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). The first click opens the weakest piece, traction and revenue. There the ARR figures sit side by side: about $3.0M said on video, $2.5M in the deck, $2.24M in the model, $2.06M in the billing rows, each with its source chip ([critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md), verdict; the exact figures are in `data_room/answer_key.json`, `facts`). The next opens one strong piece, the pitch itself, which is also the green flag: the round on slide 13, corroborated by the cap table, each source opening the other. This is true on stage: the run finished before the captain walked up. The body follows the [demo-script](#demo-script) beat sheet: the green and red flags, the overview, the video sentence, the pilot clause, the strong piece, the gaps. Then one line reads out the runs on the sealed variant room and the clean room ([blind-room](#blind-room)). The forwarded pitch email is the closing "next" line: forward it, and the readout is waiting before you open it. That keeps the "before you even ask" moment from the brief's 11:20 AM block as what comes next.

**Then a real company, live.** One beat in the core switches to a real YC company from the list Ken approves, paired with its synthetic room ([yc-rooms](#yc-rooms); [writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:49 PM block). Its outside-world panel runs live on stage: the company's website, Hacker News, the App Store and SEC filings, read as the judges watch. Ken says out loud that the company is real and its data room is not: we wrote the room, every page says "Synthetic test document. Not this company's data.", and its problems are our test plants. Hollis Voice stays the controlled room whose planted flags are known. Why this form: judges remember what they saw working, and opening on a forward started by hand spends the first 20 seconds on the one thing on screen that is not real ([critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md), finding 2; [critique_judge.md](../features/20261022.01_hackathon_plan/critique_judge.md), finding 6).

**The real forward.** An agent builds the forwarding address before Saturday ([inbox-forward](#inbox-forward)), and the readout fills in as results land ([inbound-unasked](#inbound-unasked)). So the close can forward a real pitch email on stage. Whether the close shows it live or says it in one line is the overview page's card on the demo opening.

**The other forms:** open on the forwarded email, started by hand and said so; or open on the data room upload. The overview page carries the card ("The demo opening").

---

## Now to Friday night

Building starts now, by agents and the team ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 3:32 PM block). Everything in the product brief and [FEATURES.md](FEATURES.md) is built by the end of Saturday. This horizon holds the research, people work, data and documents, the [skeleton](#skeleton), and every product slice that is not one of the team's Saturday slices. The organisers wrote that Saturday is build-only. Whether code written before Saturday is allowed is still asked on Ken's board row TRI-ask-organisers; until they answer, Ken has chosen to build now. The data room generator lives in `data_room/`, and no product folder imports it.

Most product slices here extend one of the team's Saturday slices. Each of those carries a **Joins on Saturday** line ([How to read a slice](#how-to-read-a-slice)). The product slices are listed in the order of their Waits on lines, after the setup slices.

**What is left before Saturday.** Nothing here waits on interviews; there are none (brief, 1:34 PM block). Checked against the repo on 2026-10-22.

- Done: [research-gaps](#research-gaps), [checklist](#checklist) and [data-room](#data-room). The memo template ([MEMO_TEMPLATE.md](MEMO_TEMPLATE.md)) is written too.
- [skeleton](#skeleton): an agent, now. Not started: the repo has no `schema/` or `server/` folder yet.
- [blind-room](#blind-room): Ken finds the person outside the build, who follows [SEALING.md](../../data_room/SEALING.md) with their own seed and keeps the key. The plants-off switch, the clean room and the seed option are built.
- [keys](#keys): Ken.
- [cached-data](#cached-data): an agent, once Ken's keys are in. Not started: there is no `cache/` folder yet.
- [signals-readings](#signals-readings): an agent, after cached-data and the skeleton's Claim schema.
- [saturday-specs](#saturday-specs): an agent. The FRAMEWORKS entries exist. The example result files, the static readout mock and one test call per schema are still to do.
- [social-posts](#social-posts): an agent drafts, Ken edits. Not drafted yet.
- [demo-script](#demo-script): the beat sheet is below. Ken reads the core aloud against a timer.
- [yc-rooms](#yc-rooms): Ken approves the list of real YC companies on the overview page's demo-company card. Then an agent generates a synthetic room for each approved company, and cached-data saves each company's outside-world calls.
- [record-pitch-video](#record-pitch-video): Ken reads each room's script flatly, then installs whisper.cpp and saves the transcript.
- [founder-brief](#founder-brief): Ken edits it in his own words.
- The product slices from [readout-store](#readout-store) to [product](#product): agents, in the order of their Waits on lines, with Ken where a slice names him.

### data-room

The synthetic Hollis Voice data room, its generator and its answer key, built to the [data room research](../reports/20261022.02_research/research_data_room.md), Part 3.

**Waits on:** nothing. It builds to the research's recommended company (Hollis Voice, an AI phone agent for independent vet clinics). If Ken picks another company on the overview page, the generator takes a different config. Ken's yes or no on installing `xlsxwriter` decides whether model formulas carry stored values; without it the generator writes plain values (research Part 3.6).

**Includes:**

- `data_room/generate.py`, `data_room/check.py`, `hollis_voice/` (the full room) and `hollis_voice_seed_drop/` (the thin first tier), as built ([data_room/README.md](../../data_room/README.md)).
- 17 files in the full room and 12 in the seed drop (the answer key's `full_room_files` and `seed_drop_files`), every one generated from one seeded simulation (seed 20261024).
- The 8 planted entries (7 flags plus the video variant), the 3 clean decoys and the 3 green flags in the answer key.
- `data_room/answer_key.json` outside both room folders, so Tricorder is never pointed at it. Each entry's `check` field uses the check names written in the [saturday-specs](#saturday-specs) slice, so Saturday's test can match a readout flag to a key entry.
- `01_overview/claims.json` in both rooms, written by the generator from the same list as the deck's claims slide (slide 14), with the deck's claims as data, the fallback the feasibility research recommends when PDF reading fails ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), 1.1 and 1.9).
- The footer "Synthetic data room for Deal Flow NYC 2026. Not a real company." on every page and sheet. Invented names only; emails on `example.com`.
- A fresh web search for the company name before it appears anywhere public (research open point).
- Real green flags, set by the overview page's card "Green flags in the demo room". The recommended answer frees the customers piece: the generator drops the customer-concentration plant, so the order forms, the revenue-by-customer file and the metrics export agree, and customers reads strong. If Ken picks that answer, the slices and the beat sheet that name the concentration flag change in the same pull request.

**Done when:**

- `data_room/.venv/bin/python data_room/generate.py` writes both rooms and the answer key from a clean checkout.
- If Ken picks "Free the customers piece" on the card, at least one business piece built from independent files reads looking strong on the full room.
- `data_room/.venv/bin/python data_room/check.py` ends with 0 failed. On 2026-10-22 it printed "276 passed, 0 failed".
- The reference checks stay inside `data_room/check.py`. Saturday's red-flag engine is written fresh in the room and does not copy them.

**Status:** built. The green-flags card is still open, so the customer-concentration plant is still in the room.

**Who:** agent. Ken reviews the deck and the video script.

**Judgment:** yes.

### blind-room

A room Tricorder has never seen, and a room with nothing planted. The team wrote the room, planted the flags, wrote the answer key and then wrote one check per flag, so a perfect score on that room proves nothing to a partner ([critique_judge.md](../features/20261022.01_hackathon_plan/critique_judge.md), finding 1). A clean room that comes back clean is the strongest ten seconds against "rigged" ([critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md), finding 7).

**Waits on:** data-room. Ken finds the person outside the build.

**Includes:**

- A plants-off switch in `data_room/generate.py`. The data room research describes one, and the generator has none (demo critique, finding 7). With plants off, it writes the clean room: the same company with no planted flags.
- A second seed. Run with it, the generator moves the values and writes the variant room.
- Someone outside the build picks which flags the variant room carries: a teammate who is not writing the engine, or a friend. The judge's version drops or adds one flag. An agent that has not seen the check list runs the generator for them.
- The variant room's answer key is sealed. The person who picked the flags keeps it and sends it to the captain at the 3:30 PM freeze. Nobody building the engine opens it before then.
- Both rooms sit beside the others in `data_room/`, with no answer key inside either room folder.
- The variant room now in `data_room/` is a smoke test with seed 77. It was run while the generator was built, and its flags are known, so it cannot be the sealed room ([data_room/README.md](../../data_room/README.md)). The outside person writes a new one with their own seed and `--key-out` to a private path.

**Status:** the plants-off switch, the clean room (`hollis_voice_clean/`, with `answer_key_clean.json`) and the `--seed` and `--plants` options are built. The outside person and the sealed variant are not.

**Done when:**

- With plants off, the reference checks find nothing.
- The variant room exists, its key is with the outside person, and nobody on the build has opened it.
- On Saturday, the readout runs on the variant room and the clean room, and the real numbers are read out in one line ([demo-freeze](#demo-freeze)).

**Who:** agent for the switch and the second seed. The person outside the build picks the flags and seals the key.

**Judgment:** yes.

### record-pitch-video

Ken reads a few pitch scripts into video himself, flatly ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:51 PM block): "for the data room prep, we'll need to ask me to read a few scripts into a video. i'll just read them flatly, nothing crazy." One script per room: Hollis Voice, the second invented company, and each approved real-company room. The demo critic had suggested someone off stage record it, since judges who see the presenter play the founder may stop believing the room ([critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md), finding 5). Ken's decision stands; showing the clip as audio over the deck slides with captions, rather than his face, keeps that risk small.

**Waits on:** data-room (the script is written after the deck's claims page exists, research Part 3.6, step 7).

**Includes:**

- Ken's flat reading of each room's script (Hollis Voice: `01_overview/pitch_video_script.md`), over the deck slides, with the planted line at about 0:35 saying about three million dollars in ARR, against the deck's $2,500,000 (research Part 3.4, PF2b).
- A five-second clip of the 0:35 sentence, with burned-in captions, as an H.264 MP4. This clip is what plays on stage. The line is framed as the ladder: against the billing rows' $2,060,868, three million is 46% more (demo critique, finding 5).
- The video file copied into both rooms beside the script.
- A transcript made once by hand with whisper.cpp on the demo laptop and saved next to the video, so the demo has a result if the live run fails ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), 1.5).
- whisper.cpp is not installed on the demo laptop yet. Install it this week and save the transcript.
- A phone recording may be HEVC, which not every browser plays. Convert it once to H.264 MP4: `ffmpeg -i phone_recording.mov -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart pitch_video.mp4`.
- The video file stays out of git, because GitHub blocks files over 100 MiB. `.gitignore` lists `pitch_video.mp4` and `*.mov` under `data_room/`. Share the file outside git.

**Done when:** the video and the captioned clip play in the browser on the demo laptop, and the saved transcript contains the ARR sentence with its timestamp.

**Who:** Ken reads each script himself, flatly. On stage the clip plays as audio over the deck slides, with captions. For a real company's room, the clip carries the same synthetic label as the room, so Ken's reading never stands in for that company's founders.

**Judgment:** n/a.

### research-gaps

Online research that answers the organisers' three questions where the voice-of-the-customer research left gaps. It covers how long a first-pass memo takes and which part is slowest, whether angels would pay for a first pass of their own and what it is worth per deal, how data rooms reach investors and what they open first, regret stories about hidden churn and about burn against the hiring plan, and what funds pay for first-pass diligence in their own words. Today the partner's pay rating is inferred from a competitor's case study and a pricing roundup ([critique_judge.md](../features/20261022.01_hackathon_plan/critique_judge.md), finding 3).

**Waits on:** nothing.

**Done when:** [research_gaps.md](../reports/20261022.02_research/research_gaps.md) exists.

**Status:** done.

**Who:** agent.

**Judgment:** n/a.

### sponsor-adapters

The sponsor tools in the product, with keys that only arrive on the day ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:56 PM block). Ken: "let's make sure that these are in our roadmap and features. we won't get access to them until day of but we can do the other stuff ahead of time." The landscape research names three as most useful on Saturday: Akta (signals, company data and news, with source metadata on every response), Crunchbase (comps and funding data through its MCP), and the Nicrron gateway (one key for every model, with free repeat requests) ([research_landscape.md](../reports/20261022.02_research/research_landscape.md), Part 2).

**Waits on:** nothing this week; the keys on Saturday morning.

**Includes, before Saturday (no keys needed):**

- One small adapter per sponsor, written against its published docs (saved under the feasibility and landscape research's raw folders): the request it makes, the response it expects, and how each response field becomes a Claim with its source.
- A recorded sample response per adapter, shaped from the docs, so tests and the demo can run with no key and no network.
- A switch per adapter: off, sample, or live. Every scan works with all three off, using the free sources (Tavily, You.com, GitHub, EDGAR, Hacker News) and this week's cache.
- For Nicrron: model calls go through one client, so pointing it at the gateway is a setting, not a code change.

**Includes, Saturday 9:00 to 10:30 (captain, during breakfast and team formation, inside the existing window):**

- Paste the keys into each laptop's `.env`, flip each adapter to live, run one call each, and keep sample mode for any that fails.
- On stage, say which sponsor tool each panel used.

**Done when:** every adapter passes its tests in sample mode this week; on Saturday each one is live or falls back to sample mode without a code change.

**Who:** agent this week; captain on Saturday morning.

**Judgment:** no.

### keys

Every key and account Saturday needs, in a local `.env` that is never committed, plus the demo laptop's tools.

**Waits on:** nothing. This is the board row TRI-sponsor-keys (get the sponsor API keys before Saturday).

**Includes**, from the feasibility research's Part 5:

- Anthropic API key. Required for every scan.
- Tavily key. Free 1,000 credits a month, no card.
- You.com key, or the keyless MCP profile (100 queries a day).
- GitHub token. Free; 5,000 requests an hour.
- Akta key, which comes on the day (see [sponsor-adapters](#sponsor-adapters)), plus a question to the sponsor about the paid plan. Pay-as-you-go returns 403 on headcount, web traffic, jobs and reviews; those need the Subscription plan or a sponsor coupon.
- Product Hunt token. Optional; its terms say non-commercial use.
- OpenAI key. Optional; only for the Whisper API fallback.
- A declared EDGAR User-Agent string with a real contact address. No key.
- Not needed: HN Algolia, arXiv, Apple, ffmpeg, whisper.cpp. Skipped: Crunchbase (sales only), X (paid), Facebook (app review).
- whisper.cpp installed from Homebrew on the demo laptop, a model downloaded, and one run on a test clip, so the first run is not on stage.
- Each teammate runs the feasibility research's Part 0 checks on their own laptop.
- One test request to the Anthropic API from the command line, to find which request settings Opus 5.5 refuses (feasibility 1.10 says the bundled skill lists them, and no public page confirmed it).

**Done when:** the board row says which keys Ken has, and the EDGAR User-Agent test has run once without being blocked (feasibility 1.2).

**Who:** Ken.

**Judgment:** n/a.

### yc-rooms

Synthetic data rooms for real YC companies, so the outside-world scan runs live on a real public footprint while the room's documents are invented ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:44 PM, 2:46 PM and 2:49 PM blocks). Ken at 2:49 PM: "we want to have a list of YC companies and we'll pair them with fake data rooms and run live demos on them". The demo pairs one of these with Hollis Voice, the controlled room whose planted flags are known.

**Waits on:** data-room; Ken approves the list of companies on the overview page's card for the demo company.

**Includes:**

- **The candidate list.** Two or three real YC companies from the spring 2026 batch, proposed by a research agent, each with its public footprint: website, Hacker News, App Store, SEC filings and any announced round, saved with links. Ken picks. No room is generated before he does.
- **A profile per approved company,** built only from public pages: name, product, the founders' public bios and any announced round, each saved with its link.
- **A room per approved company,** written by this week's generator with the profile swapped in. The numbers are invented and plausible, anchored only to what the company has published. This is the first piece of [room-templates](#room-templates): the profile swap.
- **The safeguard.** An invented room under a real company's name must never read as a claim about that company. Every page and sheet carries "Synthetic test document. Not this company's data." Planted problems are named test plants in the answer key and on screen, and the demo says so out loud.
- An answer key per room, outside the room folder, as for Hollis Voice.
- A pitch script per room, which Ken reads flatly ([record-pitch-video](#record-pitch-video)).
- The company's outside-world calls saved this week by [cached-data](#cached-data), so Saturday's live run has a fallback.

**Done when:** each approved company has a room that passes `data_room/check.py` against its own key; a script finds the synthetic label on every page and sheet of every real-company room; and every public fact in each profile opens its saved page.

**Who:** agent, after Ken approves the list.

**Judgment:** yes.

### cached-data

The outside data the comps and market-signal scans read on Saturday, saved as files, so nothing on stage waits on a live call.

**Waits on:** keys (Akta and Tavily for the signal pulls; the EDGAR User-Agent for the SEC downloads); Ken's approved list in yc-rooms, for the real companies' calls.

**Includes**, from the feasibility research's 1.2, 1.3 and 1.6:

- The last four Form D quarterly zips.
- XBRL company facts for 8 to 12 public companies near the demo company's space.
- 10 to 20 Form D rounds chosen by hand as private comps.
- 3 to 5 real competitors in voice AI for vet clinics, with every Akta signal the key allows and their pricing pages through Tavily.
- Hacker News and app-store results for one or two of those competitors, run by hand.
- Each comp candidate's 10-K Item 1 text, which the comp prompt (2.1) reads.
- A saved page describing each Form D issuer, which the private-comp prompt (2.2) reads.
- `cache/index.json`, which maps each URL to its saved file. The quote checker reads it to check URL sources.
- For each real company Ken approves in [yc-rooms](#yc-rooms), its own outside-world calls: its website, Hacker News, Apple's App Store lookup and SEC EDGAR, plus Akta and Tavily where the keys allow. Each call is saved with its request (the endpoint and its parameters, never the key) in `cache/index.json`, so Saturday's live run can send the same calls again and fall back to these copies.
- Everything under `cache/` at the repo root, with the date each file was read.

**Done when:** each file opens, and a short `cache/README.md` lists what each file is and where it came from.

**Who:** agent, with Ken for anything behind his keys.

**Judgment:** no.

### signals-readings

This week's saved competitor readings, written as the market-signals panel's data, so Saturday only shows them. Live market signals cannot show much: the demo company has no outside footprint, Akta's pay-as-you-go plan returns 403 on hiring, traffic and reviews, and with one reading taken this week every signal is labelled `one_reading` ([critique_buildability.md](../features/20261022.01_hackathon_plan/critique_buildability.md), finding 9).

**Waits on:** cached-data, saturday-specs (the signals schema), skeleton (the Claim schema).

**Includes:**

- `cache/signals/signals.json` in the Claim schema: a short grid per competitor from the cached Akta pulls and Tavily pricing pages, each number linked to its saved source through `cache/index.json` (feasibility 1.3).
- For Hollis Voice itself, only what the room gives: website copy and pricing.
- For the approved real company the demo uses, its own readings from this week's saved calls, shown as the fallback for Saturday's live run.
- The date each reading was taken, shown on the panel.
- If Akta's paid signals were not available, the grid shows news and company data only, and the gap says why.

**Done when:** the file validates against the Claim schema, the grid covers at least three competitors, and every number's source opens from `cache/index.json`.

**Who:** agent, with Ken for anything behind his keys.

**Judgment:** no.

### saturday-specs

The [FRAMEWORKS.md](FRAMEWORKS.md) entries and the hand-written examples that the team types in on Saturday. These are specs, not code.

**Waits on:** FRAMEWORKS.md (written by the frameworks writer) and the Claim schema in [ARCHITECTURE.md](ARCHITECTURE.md).

**Includes:**

- The red-flag check list: for each check, a name, the inputs it reads, the formula, the tolerance and the sentence a person would write (feasibility 1.1). The names match the answer key's `check` field.
- The prompt that pulls claims out of the deck, and the prompt that pulls claims out of the video transcript with segment ids.
- The comp selection rules, the "why this is a fair comp" prompt and the comp schema (feasibility 1.2).
- The signals schema and the "what changed" prompt (feasibility 1.3).
- The memo's piece table, verdict rule, top-flags rule and ask-list rule ([FRAMEWORKS.md](FRAMEWORKS.md), "Piece verdicts", "Top green and red flags" and "Ask list"), and the prompt for its connecting sentences.
- One hand-written example result file per Saturday scan, in the Claim schema, so the readout page can be built from 10:30 before any scan runs.
- A static mock of the readout layout that Ken can edit (feasibility 1.8).
- Each structured-output schema sent once this week in a real call, so any refusal shows up before Saturday. On Saturday each request carries one schema.

**Done when:** each Saturday slice below names the spec entry it types in, and each example file validates against the Claim schema by eye and by the frameworks writer's check.

**Who:** agent. Ken reviews.

**Judgment:** yes.

### skeleton

The repo the four people build in, with the typed Claim schema and a stub for the shared file readers. The agent slices build in it too. This is option B on the [skeleton-card](#skeleton-card): with every role budgeted to its last minute, building it on Saturday spends the first half hour of two people and puts the team behind ([critique_buildability.md](../features/20261022.01_hackathon_plan/critique_buildability.md), finding 7).

**Waits on:** saturday-specs (the example files). Ken has chosen to build now; he still asks the organisers and tells the judges plainly. The Claim schema in [FRAMEWORKS.md](FRAMEWORKS.md), "The shared Claim", which is the single source for every field type.

**Includes:**

- The folder layout in [ARCHITECTURE.md](ARCHITECTURE.md), with a code-owners file mapping each folder to its role.
- One root dependency file listing everything known this week: the Anthropic SDK, Pydantic, FastAPI, the server runner, pdfplumber, openpyxl, pandas and an HTTP client.
- The FastAPI app in `server/` with the three routes the feasibility research names (list scans, run a scan, serve a result file) and a health route.
- `bin/ci-py`, which runs the Python tests, and `bin/ci-web`, which runs the readout page's type check and build. They are separate so a red TypeScript build does not block Python merges. The captain runs both before each merge, and the hosted CI runs the same two commands if one is set up.
- `bin/smoke <room>`, which runs every scan that exists, then the memo, and prints which scans ran and which are missing.
- `.env.example` with every variable in ARCHITECTURE.md, and `out/` ignored by git while `sample_out/` is kept.
- `schema/claim.py`: the Pydantic models (ScanResult, Claim, Source, Gap) typed in from the FRAMEWORKS JSON Schema, with "at least one source" enforced by the model.
- `schema/claim.schema.json` exported from it, and TypeScript types generated into `schema/ts/` for the readout page to import.
- `schema/readers.py` as a stub: one function per format (PDF by page, xlsx by cell, CSV by row, Markdown by line, transcript by segment), with signatures and no bodies. Backend-and-data fills it in on Saturday ([readers](#readers)).
- The hand-written example files from saturday-specs copied into `sample_out/`.
- The guardrails fields marked "Set by the first code slice" filled in: CI command, health check, smoke command ([guardrails.md](../../.claude/guardrails.md)).

**Done when:**

- `bin/ci-py` and `bin/ci-web` exit 0 on a fresh clone, the health route answers, and `bin/smoke data_room/hollis_voice_seed_drop` prints "no scans yet" without a crash.
- The schema is frozen and merged before Saturday.
- Every example file in `sample_out/` validates.

**If the organisers say no:** option A. The skeleton and the schema typing take the first half hour of backend-and-data and the captain on Saturday. Backend-and-data's half hour comes out of the contract-terms-saturday hour, which then reads Hollis Voice's contracts only. The captain's comes out of the quote checker, which goes back to the half hour first planned.

**Who:** agent. Ken reviews.

**Judgment:** no.

### social-posts

Drafts of Saturday's social posts for the $150 social content prize, so the captain only posts. The captain already carries the quote checker, the memo, the score script and every merge ([critique_buildability.md](../features/20261022.01_hackathon_plan/critique_buildability.md), finding 8).

**Waits on:** nothing. The voice is in [BRAND.md](BRAND.md), "Posting voice".

**Includes:**

- One post for 11:00 AM: the team at work and the synthetic room.
- One post for 3:30 PM: one finding from the frozen readout, with a blank for each number, filled from the screen in the photo.
- Each follows the posting rules: say the room is synthetic, one finding per post, nothing from the "do not post" list.

**Done when:** Ken has read both drafts. On Saturday the captain posts at 11:00 and 3:30 only.

**Who:** agent drafts. Ken edits and posts.

**Judgment:** yes.

### founder-brief

The one-page founder brief the organisers ask for: problem, customer, business model, and the one workflow we demo.

**Waits on:** the product brief ([PRODUCT_BRIEF.md](PRODUCT_BRIEF.md)), the landscape research, and the workflow section above.

**Includes:** the organisers' four headings and nothing more, in [founder_brief.md](../features/20261022.01_hackathon_plan/founder_brief.md). The founder-brief writer drafts it.

**Done when:** Ken has edited it in his own words. It is the thing he hands the judges.

**Who:** agent, then Ken.

**Judgment:** yes.

### checklist

One diligence checklist, [CHECKLIST.md](CHECKLIST.md) ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:56 PM block). It drives what the scans look for, the readout's coverage and the ask list.

**Waits on:** nothing. It is built from the data-room research's 30-document table and the published checklists it cites, plus the associate's ten tabs ([outside-in](#outside-in)) and the red flags.

**Includes:**

- Each item: what it is, the stage it is expected at (pre-seed, seed, Series A), where it comes from (a data-room document, an outside source, or the founder), which scan checks it, which readout piece it feeds, and which published checklists name it, with links.
- A script that builds a CSV of the items and their counts, so the doc's counts come from it.

**Done when:** CHECKLIST.md and its CSV exist, and every count in the doc matches the script's output.

**Status:** done. Its "Checked by" column names the FRAMEWORKS entries and marks which run Saturday. The reference guides, one per data-room document a seed or Series A room can hold, are being written now in `docs/reports/20261022.03_document_guides/` ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:38 PM block). When they land, each document row links its guide.

**Who:** agent. Ken reviews.

**Judgment:** yes.

### demo-script

The demo script and Saturday's run of show, written for the captain to present: a three-minute core with a five-minute extension. The schedule gives 5:30 to 6:00 for every team's demo and the winner ([brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)), so the slot is likely three minutes or less ([critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md), finding 1). The board row TRI-ask-organisers asks the slot length.

**Waits on:** data-room, blind-room, yc-rooms, record-pitch-video, and the overview page's card on the demo opening.

**Includes:**

- The beat sheet in [DEMO.md](DEMO.md#the-beat-sheet). It opens on the top green and red flags already waiting, then the overview, drills into the weakest piece (revenue, with its four ARR numbers) and one strong piece (the pitch itself), then shows a real YC company with its outside-world scan running live, and ends the core on the forward as the "next" line.
- The line Ken says out loud on the live beat: the company is real, its public footprint is read live, and its data room is synthetic, written by us, labelled on every page, with our test plants in it.
- Who says what and who drives the laptop.
- The fallback for each step: which saved file to show if a scan fails on stage.
- Answers ready for the questions the landscape research expects from this panel: where the data goes, what happens when a scan fails, what is hard to copy ([research_landscape.md](../reports/20261022.02_research/research_landscape.md), Part 3).
- The answer to "can it catch fraud": no. It finds differences in reporting between files and against the outside world, and shows each one. A fake that agrees across every file gets through ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:33 PM block).
- The run of show below, checked against the day's real schedule once the organisers answer the board row TRI-ask-organisers (who Roundtable is, the build window and more).

**The beat sheet** lives in [DEMO.md](DEMO.md#the-beat-sheet), with the rooms, what runs live, and the fallbacks. This slice owns writing and rehearsing it.

**Done when:**

- Ken has read the core aloud against a timer in three minutes or less, and the core plus the extension in five.
- The answer to "can it catch fraud" is on the answer sheet, and no line of the script claims fraud detection.

**Who:** agent, then Ken.

**Judgment:** yes.

### skeleton-card

A decision card for the overview page: does an empty repo skeleton count as code?

**Waits on:** nothing. The critics weigh it ([brief, 10:18 AM block](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)).

**The two options:**

- **A. The skeleton is code. Build it on Saturday.** The folder layout, the CI command and the typed Claim result are the first Saturday slices. They take the first half hour of two people. Before Saturday the repo holds only documents, `data_room/` and `cache/`. To a judge who asks what was built today, the answer is every line of product code.
- **B. The skeleton is setup. An agent writes it this week.** Empty folders and packages, `bin/ci-py`, `bin/ci-web`, the CI config, the dependency list, `.env.example`, the Claim schema typed in from the FRAMEWORKS JSON Schema, and the `schema/readers.py` stub, with no scan logic. The captain and backend-and-data each get half an hour back on Saturday. The risk: the organisers wrote "On Saturday you only build" and "Everything a founder does before writing code happens this week", and commits dated before Saturday are visible to anyone who looks.

**Status:** Ken's 3:32 PM decision to build now settles this as option B. The organisers' answer is still asked on the board row.

**This roadmap is written to option B**, as the buildability critic recommends ([critique_buildability.md](../features/20261022.01_hackathon_plan/critique_buildability.md), finding 7). Its condition: Ken asks the organisers first and tells the judges plainly. The [skeleton](#skeleton) slice sits in this week, and the freed half hours go to the slices the critics name: the captain's to the quote checker ([claim-result](#claim-result)), and backend-and-data's to the shared file readers ([readers](#readers)). If the organisers say no, the skeleton slice says what moves back.

**Who:** agent writes the card. Ken decides.

**Judgment:** n/a.

### readout-store

A persistent store of readouts, so a readout outlives one laptop.

**Waits on:** skeleton (the Claim schema and the shape of `readout.json`); a host for the product, which Ken picks (the guardrails' deploy field is empty until then). Until there is a host, the store runs on the demo laptop.

**Joins on Saturday:** [readout](#readout), whose `readout.json` it stores.

**Includes:** each readout, its sources and the files it read, stored per fund; a delete that removes all of them; a list of everything held for one company. This is the data rule from the brief: nothing is stored beyond the readout and its sources, and the investor can see and delete everything pulled.

**Done when:** a stored readout for Hollis Voice comes back with its sources and files; the list for that company shows everything held; and one delete leaves nothing for that company in the store or in `cache/`.

**Who:** agent.

**Judgment:** yes.

### steering

The operator steers the readout: a comment or short instruction on a piece makes Tricorder rewrite that piece, or get more info for it from new sources ([writers' brief, 1:12 PM block](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). It must be easy enough for a partner who runs diligence alone: one plain sentence on the line that looks wrong, with no setup and no menus, and the answer comes back on that line (Ken's 2:21 PM edit, [PRODUCT_BRIEF.md](PRODUCT_BRIEF.md), "Steering the readout").

**Waits on:** readout-store, so a revision outlives the session; saturday-specs (the example readout files and the piece rules it rebuilds by).

**Joins on Saturday:** [readout](#readout), whose piece and top-flag rules rebuild a steered piece, and [readout-page](#readout-page), which shows the instruction box and the diff.

**Includes:** an instruction box on every piece and on every line, for either kind of steer. The operator types one plain sentence and nothing else: no form, no menu, no choice of steer type. Tricorder tells the two kinds apart from the sentence. A rewrite reruns the scans that feed the piece on its inputs, with the instruction passed to their model readings. A request for more info first fetches or opens the new sources it names (the full room instead of the seed drop, another filing, a competitor's pages), under the same data and terms rules as any input, then runs the piece's scans with them; the new claims are marked new. The memo rebuilds the piece and the top green and red flags by the same script rules. The new piece replaces the old one with a visible diff: claims added and dropped, wording changed, and the verdict before and after with the claims that moved it. Every revision is kept.

**Done when:**

- On Hollis Voice, "treat the pilot as non-recurring" on traction and revenue rewrites that piece, and the diff shows what changed.
- On the Hollis Voice seed drop, "read the full room" on retention adds the claims from the second tier, marked new, and the diff names the claim that moved the verdict.
- An instruction that asks for a different script number leaves the number as the script computed it, and the revision says so.
- Every rewritten claim still passes the quote checker.
- A first-time user steers one line with one typed sentence and no other step, and the revised line appears where they typed.

**Who:** agent.

**Judgment:** yes.

### room-templates

Templated data rooms with hidden issues ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:46 PM block). Ken: "we should actually set up a few different data rooms that will allow us to highlight different problems. the data rooms will need to be a little bit templated, so we can swap in new names on the fly, but we should make data rooms with hidden isseus in them, based on the problems we saw in the reserach." This week's generator already writes Hollis Voice, a second invented company, a clean room and a sealed variant, and [yc-rooms](#yc-rooms) swaps a real company's public profile into it. This slice turns it into a template engine.

**Waits on:** data-room (Hollis Voice and the second invented company) and yc-rooms (the rooms for real companies) merged.

**Includes:**

- **A company profile swapped in on the fly:** name, sector, product, stage, founders, round, and for a real company its public facts with their links. One command writes a full room from a profile.
- **A library of hidden issues**, one plant per problem the research found: ARR that is not recurring, hidden cohort churn, burn out of line with the hiring plan, deck against model, deck revenue against the P&L and partial history, customer concentration, gross margin that leaves out costs, a vanity count, billings or deferred revenue shown as revenue, contractors left out of burn, contract terms that undercut how revenue is counted, cap-table problems. Each plant names the research it comes from, where it lives in the room, and the check that should catch it.
- **Green flags and decoys** chosen the same way, so every room has real strengths and traps, not only problems.
- **A room recipe:** a profile plus a set of plants, green flags and decoys, with a seed. Recipes for the demo (one per problem story Ken wants to tell) are saved and rerunnable.
- Every room from a real company's profile carries "Synthetic test document. Not this company's data." on every page, and its plants are named test plants.
- The answer key is written from the recipe, and `check.py` checks any room against its key.

**Done when:** a new room is generated from a profile and a recipe in one command; three recipes highlight three different problem sets; each passes `check.py`; and swapping the profile changes every name and leaves every planted problem in place.

**Who:** agent.

**Judgment:** yes.

### frameworks-scan

The business frameworks: lean canvas, jobs to be done and the rest in [FRAMEWORKS.md](FRAMEWORKS.md), one prompt and one schema each.

**Waits on:** skeleton (the Claim schema); saturday-specs (the FRAMEWORKS entries 5.1 to 5.6).

**Joins on Saturday:** [readout](#readout), which places its claims in their pieces.

**Includes:** a box that the room cannot support shows "not in the data room" (feasibility 1.4).

**Done when:** on Hollis Voice, every box of each framework quotes its source sentence or shows "not in the data room", and every claim passes the quote checker.

**Who:** agent.

**Judgment:** no.

### comps-deep

Comps from Form D and EDGAR in depth.

**Waits on:** cached-data (the Form D quarters and XBRL facts already saved); saturday-specs (the selection rules).

**Joins on Saturday:** [comps](#comps), whose table it extends.

**Includes:** every Form D quarter, ranking by the selection rules; EDGAR full-text search for business descriptions (the JSON endpoint is undocumented, so the scan falls back to cached results when it breaks, per feasibility Part 2); XBRL frames for public revenue. Crunchbase only with an arrangement for apps, per the landscape research.

**Done when:** on Hollis Voice, the ranked list draws on every saved Form D quarter, each comp's business description comes from full-text search or its cached copy, and every number passes the quote checker.

**Who:** agent.

**Judgment:** yes.

### accounting-mislabels

The rest of the accounting mislabels family ([FRAMEWORKS.md](FRAMEWORKS.md), entry 1.12; [writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:32 PM block). Saturday's [redflag-engine](#redflag-engine) runs the two kinds it already owns. Entry 1.12 marks six more as runnable on Hollis Voice. An agent builds them here, before Saturday, outside the engine's 3.0 hours.

**Waits on:** data-room; saturday-specs (entry 1.12's check names).

**Joins on Saturday:** [redflag-engine](#redflag-engine), whose pilot-as-ARR flag the `mrr` check links to.

**Includes:**

- The six sub-checks entry 1.12 marks Saturday that the engine does not run: `mrr_column_vs_subscription_rows`, `billings_vs_recognised_revenue`, `contractor_spend_vs_headcount_and_burn`, `capitalised_spend_vs_pnl_and_cash`, `deferred_revenue_vs_earned` and `one_time_fees_in_recurring_metrics`. Scripts only, as in the engine.
- Kind c, gross against net revenue (`gross_vs_net_revenue`), with a generator option that writes a resale line into a test room, because Hollis Voice has nothing to run it on.
- Each kind's gap when the room lacks its file, worded as entry 1.12 gives it.
- Each claim names its kind and feeds the piece entry 1.12 names.

**Done when:**

- On the full room, `mrr_column_vs_subscription_rows` finds the Marlow pilot's fee in the `mrr` column and links it to the pilot-as-ARR flag as one cause.
- The onboarding-fee decoy and the annual-prepay decoy stay clear.
- On the seed drop, each sub-check whose file is missing returns `cannot_check` with its gap.
- On the test room with a resale line, `gross_vs_net_revenue` fires. With the option off, it does not.
- Every claim passes the quote checker.

**Who:** agent.

**Judgment:** no.

### deck-vs-books

The associate's rule, as a feature: "If revenue in the deck doesn’t match the P&L, or you show only part of your history, everything else becomes questionable." ([associate at a seed-focused fund, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal); [writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:19 PM block). Saturday's red-flag engine already compares the deck's claims with the model's named cells (`deck_claim_vs_named_cell` in [FRAMEWORKS.md](FRAMEWORKS.md)). This slice adds the two halves of her rule that it does not cover.

**Waits on:** data-room; saturday-specs (the check list, including `deck_claim_vs_named_cell`).

**Joins on Saturday:** [redflag-engine](#redflag-engine).

**Includes:**

- **Deck revenue against the P&L, period by period.** Every revenue figure the deck shows (a total, a chart's bars, a growth rate) is matched to the same period in the monthly P&L and the revenue rows, by script. A mismatch above the match tolerance is a disagreement claim with both sources.
- **Partial history.** A script finds the first month revenue appears in the books and compares it with the window the deck shows. A deck chart that starts later than the books, skips months, or shows quarters where the books hold months is flagged as "shows part of the history", with the months left out and what they hold (for example a dip, or a period of flat revenue).
- Both feed the traction and revenue piece and the pitch itself, and missing months the books do not hold go on the ask list.

**Done when:** on the Hollis Voice room, every deck revenue figure is matched to a P&L period or listed as unmatched; a test deck whose chart starts six months after the first revenue month is flagged with the months it leaves out; and the quote checker passes on every claim.

**Who:** agent.

**Judgment:** no.

### contract-terms

The rest of customer contracts ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:53 PM block). The rules are entry 1.13, "Contract terms", in [FRAMEWORKS.md](FRAMEWORKS.md). Saturday's [contract-terms-saturday](#contract-terms-saturday) already reads every contract in both demo rooms and runs three comparisons (the notice check, the pilot check and the price check). This slice adds the rest.

**Waits on:** saturday-specs (entry 1.13's prompt and schema, which the Saturday reading uses too); data-room; [readout-store](#readout-store).

**Joins on Saturday:** [contract-terms-saturday](#contract-terms-saturday), whose readings of both demo rooms it extends.

**Includes:**

- Contracts upload with the room or on their own. A folder that holds only contracts is a valid input, and the contracts of rooms beyond the two demo rooms are read the same way.
- The clauses Saturday leaves unread: exclusivity, most-favoured-customer, change of control, and any other clause that changes what the customer pays or when it can leave. Each is a claim that quotes its clause.
- The three comparisons Saturday leaves out: `plan_revenue_past_term_end` (the plan keeps a contract's revenue after its term ends, or treats an automatic renewal as certain), `signed_not_live_vs_revenue` (a signed contract or amendment that has not started is counted as revenue) and `counted_line_without_contract` (a counted line has no contract in the room).
- The ARR and concentration entries keep their own checks and point to this one.
- A contract the room lacks becomes an ask-list line: the current contract language for that customer.

**Done when:**

- On the full Hollis Voice room, the plan check flags the Marlow pilot with its eight plan months after the term ends, and clears Cedar & Pine and Brookline Row.
- The exclusivity, most-favoured-customer and change-of-control fields return "not stated" for the Hollis Voice contracts, each read from the contract and not assumed.
- A test contract with a change-of-control clause returns that clause with its quote.
- A folder that holds only contracts produces a result with no crash.
- A test contract with a 30-day cancellation counted as a year of ARR produces a gap. The same contract with a one-year commitment does not.
- Every quote passes the quote checker.

**Who:** agent.

**Judgment:** yes.

### financial-model

The financial modeling Ken asked for in the 10:10 AM dictation. Saturday's [redflag-engine](#redflag-engine) rebuilds the numbers it checks: burn against the hiring plan, deck against the model, retention and gross margin. This slice adds a rebuilt model the operator can work in.

**Waits on:** data-room; saturday-specs (the check list and entries 1.3 and 1.9); [readout-store](#readout-store).

**Joins on Saturday:** [redflag-engine](#redflag-engine), whose rebuilt numbers sit beside the full model.

**Includes:**

- **Tricorder's own version of the model**, built from the raw data the way a Series A lead does ("a lead builds their own model from your raw data", [the data-room research](../reports/20261022.02_research/research_data_room.md), 1.3; Ken at 2:40 PM: "i was already planning on building our own versions of models"). The room's revenue, cost and headcount rows go into one monthly table with burn, cash and runway, and each cell links to the row it came from.
- **Side by side with the company's model.** Every line of the company's model sits beside Tricorder's rebuilt line, and a difference beyond the match tolerance becomes a disagreement claim in the right piece.
- Unit economics recomputed from the room's rows, by [FRAMEWORKS.md](FRAMEWORKS.md) entry 1.9.
- The model's reading of the cohort tab's note, with the prompt in entry 1.3. Saturday keeps the script rebuild of the cohorts; this reading moved here to make room for contract terms on Saturday. It is a claim that quotes the note and never decides a number is wrong.
- The operator can change one assumption, such as a hire's start month or a churn rate, and see runway move. The script's own figure stays on screen beside it, and the operator's case is marked as theirs.
- Market size, bottom-up, stays in [frameworks-scan](#frameworks-scan) (entry 5.6).

**Done when:**

- On the full room, the rebuilt runway with all planned hires matches the answer key's figure, and every cell opens its source row.
- Each unit-economics figure returns a claim with its sources. A figure the room cannot support is a gap.
- Changing a hire's start month moves runway, and the script's figure still shows beside it.

**Who:** agent.

**Judgment:** yes.

### video-moments

The video leads the operator to its interesting parts (the 10:10 AM dictation; [FRAMEWORKS.md](FRAMEWORKS.md), entry 4.2). On Saturday the [pitch-video](#pitch-video) slice gives claims with timestamps, and the page jumps to them. Its 2.5 hours go to transcription and claims, so ranking the moments comes here.

**Waits on:** record-pitch-video (the saved transcript with timestamps); saturday-specs (entry 4.2 and the labels from entries 1.2 to 1.9).

**Joins on Saturday:** [pitch-video](#pitch-video) (the claims with timestamps) and [redflag-engine](#redflag-engine) (the numbers the room disputes).

**Includes:**

- Entry 4.2's moments, starting with each place the founder says a number the room disputes, each with its start and end second.
- Keyframes at scene changes as thumbnails.
- A strip of moments on the video player. Each moment is one click from its second.

**Done when:** on Hollis Voice, the ARR sentence at about 0:35 is listed as a moment, its range covers the spoken sentence, and clicking it plays from there. Every moment's quote passes the quote checker.

**Who:** agent.

**Judgment:** no.

### checklist-coverage

The readout's coverage against the [checklist](#checklist), and an ask list that draws on it ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:56 PM block). An agent builds it before Saturday, outside the captain's readout hours and the frontend's page hours. The rules are "Checklist coverage" in [FRAMEWORKS.md](FRAMEWORKS.md).

**Waits on:** checklist; saturday-specs (the example readout files).

**Joins on Saturday:** [readout](#readout) (the ask list) and [readout-page](#readout-page) (the coverage panel).

**Includes:**

- For each checklist item expected at the company's stage: found, checked or missing, with the scan that checked it and the piece it feeds.
- The ask list also draws on the checklist. Every item expected at the company's stage and missing from the room becomes a request, beside the lines from gaps and weak pieces. An item expected only at a later stage is not asked for.
- The company's stage comes from the deck's round slide, and the operator can change it.
- A coverage panel on the readout page.
- The reference guides' proposed checks, one guide per data-room document ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:38 PM block). Each proposed check becomes a check, or is marked as left to the operator, and each guide's missing-document line becomes its ask.
- Entry 1.10's model reading: the notes on the cap table, with each instrument and grant matched to its document (checklist row C82).
- Entry 1.11's asks, which no Saturday slice runs: bank statements, accountant-prepared statements, tax returns, IP assignments and customer references when the room lacks them, and one walk-through ask per flag ([FRAMEWORKS.md](FRAMEWORKS.md), entry 1.11).

**Done when:**

- On the seed drop at Series A, coverage lists every checklist item as found, checked or missing, and the counts come from a script.
- Every missing Series A item becomes one ask-list line. Set to pre-seed, the same room asks for no item expected only later.
- No request appears twice when a gap and a checklist item name the same thing.

**Who:** agent.

**Judgment:** yes.

### claim-support

The claims workflow in full ([diagrams/claims_workflow.md](diagrams/claims_workflow.md); [writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:41 PM block): every claim in the deck and the pitch video, checked against every other document and the outside world. Saturday does this for the deck's appendix claims and the video's transcript against the model and the revenue rows; this slice widens it.

**Waits on:** [checklist-coverage](#checklist-coverage) for where each claim's evidence should live; record-pitch-video (the saved transcript); saturday-specs (the claim prompts).

**Joins on Saturday:** [readout](#readout) and [pitch-video](#pitch-video).

**Includes:**

- Claim extraction from every slide (text, charts, the appendix) and every transcript sentence with a number or a checkable fact, each with its slide and position or video second and the quoted span.
- Normalising each claim to one unit, period and definition, with spoken figures marked as spoken and rounded.
- An evidence map per claim kind (from the checklist and the document guides) saying which documents and outside sources should support it.
- A label per claim: supported (two independent sources agree), contradicted (a source disagrees, both shown), or unsupported (a gap with an ask-list line).
- A claims table in the readout's drill-down: every claim, its label, and its sources.

**Done when:** on both demo rooms, every numeric claim on every slide and in the video script has a label; each planted contradiction is labelled contradicted with both sources; each green flag's claim is labelled supported with its two sources; and the quote checker passes on every claim.

**Who:** agent.

**Judgment:** yes.

### founder-requests

Quick requests to the company while the room is being compiled ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 3:15 PM block). Ken: "While compiling the data room, there are quick ways to send messages to the company asking them for information, with guidance on what they should submit."

**Waits on:** [checklist-coverage](#checklist-coverage).

**Joins on Saturday:** [readout](#readout), whose ask list it drafts from.

**Includes:**

- From the ask list, one click drafts a message to the founder for any missing item or group of items, in plain words.
- Each request carries guidance on what to submit, taken from the document guides: what the document is, the form that works best, and what a good one shows (for example, monthly revenue by customer as a CSV with one row per customer per month).
- The operator reviews and sends it from their own email; Tricorder never sends anything itself.
- When the founder replies with files, they land in the room and the scans that waited on them start.

**Done when:** on the Brasswick room, the ask list produces a request for its missing documents with guidance for each, the operator can copy or open it in their email client, and a reply's attachment added to the room starts the waiting scans.

**Who:** agent.

**Judgment:** yes.

### memo-export

Tricorder helps the operator write the memo for the partners' meeting ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:58 PM and 2:00 PM blocks). The memo is interactive. It reads as a normal memo top to bottom, and behind every line sit the same two clicks the operator has in the readout. An agent builds it before Saturday, outside the captain's and the frontend's Saturday hours.

**Waits on:** saturday-specs (the example readout files). The template is written: [MEMO_TEMPLATE.md](MEMO_TEMPLATE.md), built from real published memos and memo templates.

**Joins on Saturday:** [readout](#readout), whose `readout.json` fills the memo.

**Includes:**

- The export: a draft memo in the template's sections, in order, filled from the readout's pieces, the checklist items, the top green and red flags, the gaps and the ask list, as the template says.
- The interactive memo: a page the partners open. From any line, one click opens the claims behind it. From any claim, one more opens its source and the sources that agree or disagree.
- A static PDF of the same memo for funds that need one, with every claim footnoted to its source.
- The operator edits the draft. A sentence the operator writes with no claim behind it is marked as theirs.

**Done when:**

- On Hollis Voice, the export fills every template section, or names the gap that leaves one empty.
- In the interactive memo, every line reaches its claims in one click and a claim's source in two.
- In the PDF, every claim carries a footnote that names its source and locator.
- Every claim in both forms passes the quote checker.

**Who:** agent.

**Judgment:** yes.

### reader-scenarios

Each reader of the memo gets their own copy to steer, and can try what-if changes on the financial model ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:01 PM block). The operator's memo is the shared version. A partner's changes stay in the partner's copy.

**Waits on:** [memo-export](#memo-export); [steering](#steering); [financial-model](#financial-model), whose scripts do the recomputing.

**Includes:**

- A shared memo version, and one copy per reader laid over it. A reader steers their copy (rewrite a section, ask for more information) by the same rules as [steering](#steering), without changing anyone else's.
- Each copy says what the reader changed and which shared version it started from.
- What-if inputs on the model: a reader changes a few assumptions, such as churn, price, hiring pace, or the pilot counted or not, and sees what the numbers become.
- The same scripts recompute from the company's own model and rows. The source files never change.
- Every tweaked number is marked as the reader's scenario, shown beside the company's figure and Tricorder's rebuilt figure, so nobody mistakes a what-if for a fact.

**Done when:**

- Two readers steer their own copies of the Hollis Voice memo differently. Each sees only their own changes, and the shared version is unchanged.
- A reader who sets "pilot not counted" sees ARR recomputed by the script, marked as their scenario, beside the company's figure and the rebuilt figure.
- After any scenario, the room's files are byte for byte the same as before.
- A new shared version shows each reader which version their copy started from.

**Who:** agent.

**Judgment:** yes.

### bank-check

**Compare the bank account with the books.** With the founder's consent, the investor connects the company's bank account through a banking connector. Tricorder compares deposits with the revenue rows, and outflows with the model's burn, and shows each difference as a claim with its sources ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:52 PM block). It is a check for differences in reporting, never fraud detection (1:33 PM block). A set of books that is fake but consistent with the bank can still get through, and the readout says so.

**Waits on:** [readout-store](#readout-store), so bank data is stored with the readout and deleted with it; a Plaid developer account, which is a board row for Ken.

**Joins on Saturday:** [readout](#readout), which places the bank claims in their pieces.

**Includes:**

- **Try the connector first, fake it if needed** (Ken, 3:11 PM: "we can try this, we just need to see if one of these connectors has a trial account and test data. or we could rig it up and fake it, just say we'd connect this here, and here's a sample bank statement you might get"). Plaid's sandbox has free test accounts and custom test data. If it is not working in time, the room carries a sample bank statement (a CSV and a PDF from the generator, labelled as a sample), and the readout shows where the connected account would plug in.
- **The connector: Plaid first.** Its Sandbox offers custom test users whose data covers Balance, Identity and Transactions, among other products ([Plaid Sandbox custom users](https://plaid.com/docs/sandbox/user-custom/), [saved copy](../reports/20261022.02_research/raw/feasibility/plaid/sandbox_user_custom.md)). No other connector is named here, because no other connector's sandbox docs have been read and saved. Plaid's production terms and pricing have not been read either; the builder reads them before any real account is connected.
- **The consent step.** The founder, not the investor, signs in to the bank through Plaid Link, Plaid's own sign-in flow, so the investor never sees the bank credentials. The page states what is read (balances and transactions, read only), for which accounts and for how long. Tricorder records the consent with its date. The founder can withdraw it, and withdrawing deletes the connection and every transaction pulled, under the data rule from the 11:20 AM block.
- **The checks.** Each is a script; a model only sorts messy transaction descriptions into categories.
  - Deposits against the revenue rows: deposits per month, matched to the revenue file's rows by customer and month, within `match_tolerance`.
  - Outflows against the model's burn: outflows per month against the model's net burn for the same months.
  - The bank balance at the as-of date against the model's cash. On Hollis Voice the model's cash rests on the model alone today, because no bank statement is in the room ([FRAMEWORKS.md](FRAMEWORKS.md), "Piece verdicts", worked example).
  - New check names in [FRAMEWORKS.md](FRAMEWORKS.md): `bank_deposits_vs_revenue_rows`, `bank_outflows_vs_model_burn`, `bank_balance_vs_model_cash`, written in the seven parts.
- **The pieces it feeds.** Deposits feed **traction and revenue**. Outflows and the balance feed **burn and runway**. The bank counts as a source independent of the narrative set and of the model, so a match corroborates and a difference contradicts.
- **The gap when no bank is connected.** "Not in the room: bank transactions (no bank connected)", with `would_need` "the founder connects the company's account". It is never a flag.
- **The demo path.** A Plaid Sandbox custom user with configured accounts, created in Sandbox Studio or with `/sandbox/public_token/create`. The limits from the saved page: a configuration larger than about 55 KB, or about 250 transactions, may make the sign-in fail, and more than ten accounts on one custom user fails. Use a non-OAuth test bank such as First Platypus Bank. `roll_dates_forward` keeps the dates current, and the generator leaves it off when a test needs exact dates.
- **The Hollis Voice bank feed.** The data-room generator writes a bank feed from the same simulation, within those limits. Its deposits disagree with the revenue file in one planted place. The plant goes in the answer key with its location, true value, shown value and check name. It is written only with a generator option and kept out of the Saturday rooms, so Saturday's score of found entries and decoys does not change.

**Done when:**

- On the Hollis Voice bank feed, `bank_deposits_vs_revenue_rows` finds the planted difference and nothing else.
- With the plant switched off, no bank check fires.
- On the Sandbox custom user, the bank's balance and transactions arrive through Plaid and match the generated feed.
- With no bank connected, the readout shows the gap and no flag.
- Withdrawing consent deletes the connection and every pulled transaction, and readout-store's list for the company shows none.
- Every claim passes the quote checker against the saved transaction data.
- Tests run on a recorded Sandbox response, so CI never calls Plaid.

**Who:** agent, with Ken for the Plaid account.

**Judgment:** yes.

### outside-in

**The associate's ten tabs, opened automatically.** An associate at Flyer One Ventures describes her first step on a deal: "Before I even open your data room, I already have ten tabs up. I’m checking your traffic, reviews, investors, any co-founder issues, and whether your story matches what’s online." ([Startups Magazine, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal); the [voice-of-the-customer research](../reports/20261022.02_research/research_voice_of_customer.md), row 1). Her routine is Tricorder's market-signal and presence scans, done by hand. This slice opens her tabs for her. It runs before the data room is opened, so it works on an inbound that holds only a company name and a deck. At the earliest stage there is often no data room at all, and these tabs carry the first pass ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:38 PM block). It builds the table in the product brief's "What Tricorder gathers before the data room is opened" ([PRODUCT_BRIEF.md](PRODUCT_BRIEF.md)). Every source term, limit and price below comes from the feasibility research's 1.3, 1.6, 1.7 and Part 2 ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md)), with the page that research read.

**Waits on:** the board row TRI-sponsor-keys (get the sponsor API keys before Saturday): Akta, Tavily, You.com, a GitHub token, the EDGAR User-Agent, and a Product Hunt token if Ken approves its terms; traffic and Akta's review signals also need Akta's Subscription plan or a sponsor coupon, and without it they run as gaps; [sponsor-adapters](#sponsor-adapters), for Akta in sample mode until the key arrives; [readout-store](#readout-store), so each company's pulled pages and claims outlive one laptop and the operator can see and delete them; [cached-data](#cached-data) (the `cache/index.json` rule); [yc-rooms](#yc-rooms), whose approved YC companies and their synthetic rooms are the live run under Done when; a decision on Product Hunt, whose API terms say non-commercial use (shared with online-presence); [steering](#steering), for the "get more info" steers only, since the tabs work without it.

**Joins on Saturday:** [claim-result](#claim-result) (the quote checker), [readout](#readout) (the linking and the piece verdicts) and [market-signals](#market-signals) (the panel it makes live).

**Includes:**

- **The input.** A company folder that may hold only a deck, or only an inbound email with a deck attached. A resolver reads four things and writes them to `company.json`, each with the locator it came from (a slide, or an email header line), so the quote checker can check the inputs too.
  - The company name: from the deck's cover slide, the email subject or the signature.
  - The domain: from URLs on the deck and the sender's address. Free mail domains (a list kept as a setting) never count as the company's domain.
  - The city: from the deck or the signature.
  - The founder names: from the team slide and the signature. When a room exists, also from the bios.
  - The operator can correct any field before the tabs run.
- **Resolving the right company.** Domain first, then name plus city.
  - Domain first: the scan fetches the home page on the domain. The company resolves when that page names it.
  - Then name plus city: search results, Akta Company Search (100 a day on pay-as-you-go, [Akta rate limits](https://docs.akta.pro/getting-started/rate-limits)) and the Form D issuer table (name, state and year of incorporation, [Form D data sets](https://www.sec.gov/data-research/sec-markets-data/form-d-data-sets)). A candidate resolves when its name and its city or state match in one source.
  - On an ambiguous match, it shows the candidates and never guesses. Ambiguous means two or more candidates fit, or the domain's page names a different company. The readout lists each candidate with its name, domain, city and the source that found it, and asks the operator to pick. No tab runs until they pick.
  - Every result a tab fetches is kept only when it ties to the resolved company by domain, or by name plus city. A same-named company elsewhere is dropped and listed in the run log.
- **The scan.** `scans/outside/`, a new folder beside `scans/presence/` and `scans/founders/` ([ARCHITECTURE.md](ARCHITECTURE.md)).
  - `run(company_dir) -> ScanResult`, run as `python -m scans.outside <company_dir>`, writing `out/<company>/outside.json`. It follows the scan interface in ARCHITECTURE.md.
  - One check name per tab: `outside_traffic`, `outside_reviews`, `outside_investors`, `outside_cofounders`, `outside_story`.
  - Each tab runs alone and fails alone. A source that refuses or times out becomes a gap, and the scan still exits 0.
  - Each source's client stays under that source's published limit, listed under each tab below.
  - Each run records the calls and credits it spent per source in the ScanResult's `inputs`. The cost of one company comes from that log, not from a guess.
  - Keys come from the environment variables in ARCHITECTURE.md: `AKTA_API_KEY`, `TAVILY_API_KEY`, `YOU_API_KEY`, `GITHUB_TOKEN`, `PRODUCT_HUNT_TOKEN`, `EDGAR_USER_AGENT`. A missing key makes that source `not_checked`, with a gap that names the variable.
  - With `TRICORDER_OFFLINE=1` it reads `cache/` only and makes no outside call.
- **The cache, for every tab.**
  - Every page and API response is saved under `cache/outside/<company>/<tab>/`, with the date it was read.
  - `cache/index.json` maps each URL, or each API call (the endpoint and its parameters, never the key), to its saved file and date. This is the rule from the [cached-data](#cached-data) slice.
  - The quote checker checks every URL and API source against its saved copy through `cache/index.json`. A claim whose source is not in the index is `unverified` and goes to the "could not verify" box.
  - A rerun reads the cache. It reads fresh only when the operator asks, or when the saved copy is older than a setting the team sets (`outside_max_age_days`).
  - readout-store's delete removes the company's saved files and their index entries.
- **Traffic.**
  - Source: Akta's Website Traffic signal, REST at `api.akta.pro` with the `x-api-key` header. Pay-as-you-go returns 403 on it. The Subscription 50 tier allows alternative signals at 10 a minute and 750 a month each ([Akta rate limits](https://docs.akta.pro/getting-started/rate-limits)), at $0.04 a credit against $0.05 on pay-as-you-go ([Akta credits](https://docs.akta.pro/getting-started/pricing)). Akta's slowest signals have a p99 latency past 55 seconds ([Akta latency](https://docs.akta.pro/getting-started/performance)), so the call runs in the background with a timeout and the readout never waits on it. The research names no second traffic source.
  - Fetches: traffic for the company's domain, and for the competitors named on the deck's competition slide.
  - Claims: one claim per dated reading, label `signal`, unit `count`, period the month. It runs entry 3.1's check in [FRAMEWORKS.md](FRAMEWORKS.md): a direction (rising, flat, falling) needs two dated readings, and one reading is `one_reading`. The company's own readings feed **traction and revenue**. The competitors' readings feed **market**.
  - Corroboration: there is one source, so a traffic claim is never marked corroborated, and the page shows "one source" beside it. It can contradict a deck claim about visitors only when label, unit and period match.
  - Gap: "Not in the room: web traffic for <company> (Akta plan returns 403)", or (no Akta key), or (no data for this domain). A 403 is `no_signal`, never zero.
  - Never: estimate traffic from anything else, such as search rank or Hacker News points. Never read a 403 or an empty answer as zero. Never claim a direction from one reading.
  - Get more info: "add <competitor> to the traffic comparison"; "take a fresh traffic reading" (which gives a direction once the earlier reading is from another month).
- **Reviews.**
  - Sources: Apple's Search and Lookup API, official, no key, about 20 calls a minute "subject to change", free ([Apple Search API](https://performance-partners.apple.com/search-api)). Lookup gives `averageUserRating`, `userRatingCount` and `currentVersionReleaseDate` ([saved sample](../reports/20261022.02_research/raw/feasibility/appstores/itunes_apple_com_lookup_id_284882215_country_us.txt)). Akta's Product Reviews and Employee Reviews, on the Subscription plan only, as for traffic. Review sites found through Tavily: free 1,000 credits a month with no card, a basic search 1 credit and an advanced one 2, a development key 100 requests a minute ([Tavily credits](https://docs.tavily.com/documentation/api-credits), [Tavily rate limits](https://docs.tavily.com/documentation/rate-limits)). Or through You.com: Web Search $5 per 1,000 calls, Contents $1 per 1,000 pages, or the keyless MCP profile at 100 queries a day ([You.com pricing](https://you.com/pricing), [You.com rate limits](https://you.com/docs/rate-limits)).
  - Off by default: Apple's customer-review feed answered the research's test but Apple does not document it ([saved sample](../reports/20261022.02_research/raw/feasibility/appstores/rss_reviews_sample.json)). It stays off until Ken decides. Google Play's official reviews API reads only reviews for your own apps ([Google Play Developer API](https://developers.google.com/android-publisher/reply-to-reviews)), and its public listings have no official API, so Google Play is skipped.
  - Fetches: the company's app, matched only when Apple's record names the company as the developer or links to its domain (the builder checks those field names in Apple's reference first); its rating, rating count and last release date; review pages found by search; Akta's review signals when the plan allows.
  - Claims: ratings and counts as `signal` claims. A rating needs a unit the schema lacks, so this slice adds `rating` to the unit list in FRAMEWORKS.md, the source for every field. Review themes come from entry 3.1's model reading: each theme quotes at least one review sentence with its date and rating, and shows how many reviews it rests on. Product reviews feed **customers**. A theme that contradicts a product claim in the deck feeds **the pitch itself**. Employee review themes feed **team**.
  - Corroboration: when the deck states a rating or a review count, Apple's Lookup value corroborates it within `match_tolerance`. The deck is the company's own words and Apple is not, so the two count as independent. A theme counts as recurring only when at least two reviews show it, and as corroborated only when two separate review sources show it.
  - Gap: "Not in the room: an app for <company>"; "Not in the room: product reviews for <company> (Akta plan returns 403)"; "Not in the room: reviews on a review site". No app is common for a business product and is never a weakness.
  - Never: treat a handful of reviews as the market's view. Never name or profile a reviewer. Never use Apple's review feed before Ken decides. Never read Google Play pages.
  - Get more info: "read the reviews on <URL>"; "look for the app under <other name>"; "only reviews since <date>".
- **Investors.**
  - Sources: the SEC's Form D data sets, quarterly ZIP files, free, no key, normal EDGAR fair access; the SEC says it cannot guarantee their accuracy ([Form D data sets](https://www.sec.gov/data-research/sec-markets-data/form-d-data-sets)). The issuer and offering tables hold name, state, year of incorporation, industry bucket, offering size, amount sold and sale date, and no business description. Every EDGAR request sends a declared User-Agent with a contact address plus `Accept-Encoding: gzip, deflate`, at no more than 10 requests a second, from the server because there is no CORS ([Accessing EDGAR data](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data), [EDGAR API documentation](https://www.sec.gov/edgar/sec-api-documentation)). EDGAR full-text search ([search page](https://www.sec.gov/edgar/search/), [FAQ](https://www.sec.gov/edgar/search/efts-faq.html)); its JSON endpoint is undocumented, so when it breaks the tab falls back to cached results. Akta News Signals, which work on pay-as-you-go at 10,000 a month, and Akta Company Data at 100 a month ([Akta rate limits](https://docs.akta.pro/getting-started/rate-limits)); the research did not check which funding fields Company Data returns, so the builder reads one response first. Press found through Tavily or You.com. The cap table and the deck's round slide, when the room holds them.
  - Not used: Crunchbase. Its Basic API is closed and access goes through its sales team ([Using the API](https://data.crunchbase.com/docs/using-the-api), [Basic](https://data.crunchbase.com/docs/crunchbase-basic-getting-started)). It is used only after an arrangement that covers apps, as in comps-deep.
  - Fetches: the company's own Form D rows, matched by issuer name, state and year of incorporation, from the same quarterly files comps-deep downloads; funding news; the company's own announcement pages.
  - Claims: each earlier round's amount and date, with the round named before a colon ("Seed: raised"), label `raise_amount`; each named investor as a claim with no value, quoting the source that names them. They feed **the pitch itself**. The round also shows beside the comps table as context, and is never counted as a comp.
  - Corroboration: a round's amount is corroborated when two of these agree within `match_tolerance`: the Form D amount sold, the cap table, and an outlet's own reporting. The deck and the company's own announcement count as one source. An investor's name is corroborated when outside press and the cap table name the same holder for the same round.
  - A difference, such as the deck's "raised to date" against the Form D amount sold, is shown with both quotes and no reason, as every difference is.
  - Gap: "Not in the room: a Form D filing matching <company>"; "Not in the room: press naming the <round> investors". No Form D is never a flag.
  - Never: name an investor no source names. Never take the deck's list of backers as confirmed. Never use Crunchbase data without an arrangement. Never read a missing filing as hiding something.
  - Get more info: "check Form D filings back to <year>"; "find press on the <round>"; "read the cap table from the full room".
- **Co-founder issues.**
  - Sources: the founder names from the input. GitHub REST for each founder's user and repos: `login`, `company`, `bio`, `public_repos`, `followers` and `created_at` ([GitHub Users API](https://docs.github.com/en/rest/users/users)); 60 requests an hour without a token and 5,000 with one, search 30 a minute with a token, a secondary limit of 900 points a minute ([REST limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api), [Search](https://docs.github.com/en/rest/search/search)). Personal sites, talks and posts found through Tavily or You.com, saved with URL and date. arXiv, one request every three seconds and one connection at a time ([arXiv terms](https://info.arxiv.org/help/api/tou.html)). Akta News Signals for arrivals and departures.
  - Linked only: X charges $0.005 a post read and $0.010 a user read ([X pricing](https://docs.x.com/x-api/getting-started/pricing)), so the tab links a founder's handle and reads nothing.
  - LinkedIn is never scraped; the organisers' tracks say its terms prohibit it ([problem tracks](../reports/20261022.01_hackathon_sources/problem_tracks.txt)). A LinkedIn export the founder shares with consent may be read.
  - Fetches: for each founder, dated sources that name the company and a role; dated sources that show two founders worked together before (an earlier employer named in two places, a shared repo, a co-written paper or talk); press naming a founder's arrival or departure; the company's team page today.
  - Claims: who each source names as a founder, with its date; "worked together before", with the dated sources; a departure named in a dated outside source. They feed **team**.
  - Corroboration: a founder's role is corroborated when the deck and a dated outside source agree, such as press, a talk host's page or GitHub organisation membership. The founders' own posts and the company's own site count as one source with the deck. Time together is shown only from dated sources that name both founders.
  - Differences: a person named as a co-founder in a dated outside source and missing from the deck's team slide, or a founding date that differs between sources. Each is shown with both quotes and severity `watch`, as a question for the operator. The script never makes it a flag, and nothing gives a reason for it.
  - Gap: "No public evidence found" for a founder, printed as that, never as a negative.
  - Never: scrape LinkedIn. Never infer anything in the "not fair" column of [FRAMEWORKS.md](FRAMEWORKS.md), Scan 6 (age, gender, ethnicity, nationality, religion, politics, health, family, or anything from a photo, voice or accent). Never read missing GitHub activity as a weakness. Never guess why a founder left. Never match a person by name alone: the source must also name the company or its domain. Never quote personal posts that are not about the company.
  - Get more info: "look up <person> named in <URL>"; "read this talk: <URL>"; "read the LinkedIn export the founder sent".
- **Whether the story matches what is online.**
  - Sources: the company's website, extracted through Tavily or You.com Contents ($1 per 1,000 pages, [You.com pricing](https://you.com/pricing)) and saved with its date. Hacker News through the Algolia API, no key, 10,000 requests an hour per IP ([HN Algolia API](https://hn.algolia.com/api)). Product Hunt's GraphQL API with a token; its limit is not published and its docs say it "must not be used for commercial purposes" ([Product Hunt API](https://api.producthunt.com/v2/docs)), so it stays `not_checked` until Ken's decision. Press found through Tavily, You.com and Akta News Signals. Apple Lookup for claims about the app. Customers' own pages, for customers the deck names.
  - Fetches: for each claim on the deck (entry 1.1's claim extraction), the same metric or fact on the website, in press, on Hacker News and on Product Hunt, each with its date. That covers numbers, customers named, the launch date, the founding date and the product's claims.
  - Claims: each outside statement as a claim carrying the deck claim's label, so the memo links them. Each feeds **whichever piece its label belongs to**. The website-against-deck number check is entry 7.1's, extended to press and customers' pages.
  - Corroboration: the company's website, blog, press releases and the founders' own posts join the narrative set in "Piece verdicts", so the website agreeing with the deck is one source. A deck claim is corroborated only by a source the company did not write: an outlet's own reporting, a customer's own page, a Form D row, an Apple record, or a Hacker News post by someone outside the company. A press release is marked `company_own_claim`, as in entry 3.2.
  - Differences: a website number that differs from the deck beyond `match_tolerance` is a conflict (entry 7.1's `site_disagrees_with_deck`). An older public figure is compared with a newer deck figure only with both dates named. This finds differences in reporting. It never calls anything fraud or fake ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:33 PM block).
  - Gap: `none_found` per source. An empty footprint is shown as a finding (`footprint_empty`), never as a flag.
  - Never: read a small footprint as a weak company. Never profile commenters. Never fetch reddit.com; Reddit is read only from pages Ken saved, through online-presence. Never use Product Hunt data in a paid product before Ken's decision.
  - Get more info: "check the customer logos on slide <n> against the customers' own sites"; "search Hacker News for <old product name>"; "read the company's blog".
- **Where it shows in the readout.**
  - A new rule in Step 1 of "Piece verdicts" in FRAMEWORKS.md: a claim from this scan goes to the piece its tab names above, as a claim from Scan 2 goes to comps.
  - A "Before the data room" panel through the ScanResult's `panels`: one row per tab, with its status (found, one reading, none found, not checked), its sources and the date each was read. The page groups this scan's gaps under "Not found online"; each gap's `what` still starts "Not in the room:", as the schema requires.
  - The top green and red flags draw on these claims by the same script rule as every other claim. Nothing missing online becomes a red flag.
- **The FRAMEWORKS.md entries it adds.** A "Scan 8. Outside-in" section. Investors and co-founder issues get new entries in the seven parts. Traffic and reviews run entry 3.1 on the company itself. The story tab runs entry 7.1, extended to press and customers' pages. The `rating` unit, the wider narrative set and the Step 1 rule go in the same change.
- **How it relates to the other slices.**
  - [market-signals](#market-signals) stays a separate Saturday slice. It shows this week's cached competitor readings, and on Saturday it re-sends one approved real company's saved calls live. This slice is the full live version for the company itself, and it keeps the competitor rows. Making the signals panel read every tab live is part of this slice.
  - [online-presence](#online-presence) stays separate and now waits on this slice. This slice builds the company resolver, the cache, and the Hacker News and Apple clients, so online-presence reuses those instead of building them again. What online-presence alone adds is the Reddit mini-browser and the Facebook page text the investor pastes.
  - [founder-profiles](#founder-profiles) stays separate and now waits on this slice. It judges each founder's fit and commitment (FRAMEWORKS.md, Scan 6). The co-founder tab asks a different question: the team's history together, and whether the sources agree on who the founders are. Both read the same GitHub and page fetches through the one cache built here.
  - [comps-deep](#comps-deep) stays separate. Both read the same Form D quarterly files. This slice reads the company's own rows; comps-deep ranks other companies.
  - [inbound-unasked](#inbound-unasked) is unchanged. Once it exists, this scan is the first to run on an inbound, because it needs only a name and a deck.

**Done when:**

- A recorded fixture under `scans/outside/tests/fixtures/` holds saved responses from every source (Akta, including a 403; Tavily; You.com; Hacker News; Apple Lookup; GitHub; Form D rows; EDGAR; Product Hunt), a fixture company, and a matching `cache/index.json`.
- Every test runs with `TRICORDER_OFFLINE=1` and a network guard that fails any outside call, so CI never calls the network.
- Resolution tests pass: the domain resolves the company; name plus city resolves it; a free mail sender's domain is ignored; two same-named candidates produce a candidate list, no fetch from any tab, and no claim.
- On the fixture, each tab writes its claims and gaps, and each claim lands in the piece its tab names.
- The Akta 403 in the fixture produces a `no_signal` gap and no claim with a value of zero.
- A fixture company with no footprint produces gaps only. No claim has severity "flag", and no piece verdict moves to looking weak because of it.
- A test shows the fetch client refuses any linkedin.com or reddit.com address.
- A fixture with a co-founder named in a dated outside article and missing from the deck produces a `watch` claim with both quotes, no reason, and no flag.
- A fixture where the deck's round amount matches the Form D amount sold marks the claim corroborated. A fixture where the deck matches only the company's own website does not.
- A folder holding only a deck PDF, and a folder holding only an inbound email, each produce `outside.json`.
- A live run on the real YC companies Ken approved in [yc-rooms](#yc-rooms), each paired with its synthetic room. On each, every tab returns claims or a gap with its reason, and every claim's source opens from `cache/index.json`.
- On a synthetic room under a real company's name, the story tab compares invented deck claims with real public pages. Every difference it shows carries the room's label, "Synthetic test document. Not this company's data.", and reads as a test result, never as a finding about the company.
- The quote checker passes on every claim, from the fixture and from both live runs.
- The run on Hollis Voice reports every outside source as none found or not checked, each with its reason, and every piece verdict is the same as in the run without this scan.
- The ScanResult lists the calls and credits spent per source.
- readout-store's delete removes the company's saved files and index entries.
- Each tab's "get more info" steer on the fixture adds claims marked new, and the diff names any verdict it moved.

**Who:** agent, with Ken for the keys, approving the two live companies, and the Product Hunt and Apple review feed decisions.

**Judgment:** yes.

### founder-profiles

A card per founder from GitHub, personal sites and talks. LinkedIn is never scraped.

**Waits on:** Ken reads GitHub's terms on persona accounts before any demo account is made (feasibility open point); [outside-in](#outside-in), for the company resolver, the founder names it pulls from the deck, and the GitHub client and cache it builds.

**Includes:**

- The GitHub user and repo data, and a founder-market fit note scored against the rubric in FRAMEWORKS.md (entry 6.1). Each line linked to its source.
- Whether each founder comes from the industry, from dated sources that name an earlier role in it (entry 6.1).
- A passion and commitment rating from public signals, by the rubric in entry 6.2: time spent on the problem, shown in GitHub, posts and talks, each signal dated and linked.
- The founder's socials linked. X is linked and not read, because reading costs money per post. LinkedIn is never scraped.

**Done when:**

- On a real founder Ken approves, the card shows the fit note, the industry background and the passion and commitment rating, each line linked to a dated source.
- A founder with no public footprint shows "No public evidence found", never a low rating.
- The fetch client refuses any linkedin.com address.

**Who:** agent.

**Judgment:** yes.

### online-presence

The company's footprint: web, Hacker News, Product Hunt, app stores, Reddit, Facebook.

**Waits on:** [outside-in](#outside-in), for the company resolver, the cache and the Hacker News and Apple clients it builds; someone reads Reddit's rules (the feasibility research did not); a decision on Product Hunt, whose API terms say non-commercial use.

**Includes:**

- Hacker News through Algolia and the Apple lookup, as in the feasibility research's 1.6.
- The Reddit mini-browser Ken described: a small browser pane in which Ken, signed in as himself, clicks Reddit links, and each page he opens is saved as JSON into the corpus. Agents never fetch reddit.com; the scan reads only what Ken saved.
- Facebook page text pasted by Ken.

**Done when:** on a real company Ken approved, the Hacker News and Apple results come back through outside-in's clients and cache; a Reddit page Ken opened in the mini-browser is saved as JSON and read by the scan; no test fetches reddit.com; and every claim passes the quote checker.

**Who:** agent.

**Judgment:** yes.

### reference-checks

Low priority: Ken is not sure Tricorder can take this on. Reference calls are routine, and investors say they do them poorly: "Most VCs do reference calls. From my conversations, few feel like they do them very well." ([seed investor, Jun 2025](https://formventures.substack.com/p/team-talks-ii-founder-reference-calls); the [voice-of-the-customer research](../reports/20261022.02_research/research_voice_of_customer.md), section 1). Tricorder prepares the calls. It never makes them.

**Waits on:** [outside-in](#outside-in); [founder-profiles](#founder-profiles).

**Includes:**

- A list of people the operator could ask, drawn from the founder profiles and the outside-in tabs: former colleagues shown in dated sources, co-investors named in Form D or press, and customers named in the deck. Each person carries the source that names them.
- A short question list for each person, drawn from the readout's weak pieces. Each question cites the claim it comes from.
- Tricorder never contacts anyone. It finds no contact details beyond what the source that names the person already shows.

**Done when:** on a real company Ken approved, every person listed carries the source that names them, every question cites its claim, and no contact detail appears that the source did not show.

**Who:** agent.

**Judgment:** yes.

### stage-views

First screens that suit the company's stage ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:38 PM block). The stage decides what exists about a company. At the earliest stage there is little or no data room, so the founders, the pitch itself and the outside world carry the first pass. At Series A the financial pieces do.

**Waits on:** [readout-store](#readout-store), to save an operator's order; [checklist](#checklist), for what each stage is expected to hold; [outside-in](#outside-in), whose tabs fill the earliest-stage pieces.

**Joins on Saturday:** [readout-page](#readout-page), whose up and down buttons it saves.

**Includes:**

- A default piece order per stage (pre-seed, seed, Series A), as a stated table beside "Piece verdicts" in FRAMEWORKS.md.
- The stage read from the deck's round slide or the inbound, which the operator can change.
- A piece the stage does not usually have data for says so, instead of reading as a gap.
- The operator's own order, from the readout page's up and down buttons, saved per operator and reused on the next company at that stage.

**Done when:**

- The same room set to pre-seed opens with team, the pitch itself and market first. Set to Series A, it opens with traction and revenue, retention, and burn and runway first. The verdicts are the same in both.
- An operator's saved order comes back on their next readout at that stage.

**Who:** agent.

**Judgment:** yes.

### inbox-forward

The first inbox input: a forwarding address such as deals@ through a mail-receiving service.

**Waits on:** readout-store; a domain and a mail-receiving service, which Ken picks.

**Joins on Saturday:** [readout](#readout), which builds the readout for each new company folder.

**Includes:** PDF attachments go into a new company folder. DocSend, Google Drive, Dropbox and Notion links are fetched only when they open without a sign-in; otherwise the readout records a gap that says what the investor must do. It needs no OAuth review, which is why the brief recommends it first.

**Done when:** an email with a deck attached, sent to the forwarding address, creates a company folder holding the deck; an email with a DocSend link that needs a sign-in produces the gap that says what the investor must do; and the investor's delete removes the folder.

**Who:** agent.

**Judgment:** yes.

### inbound-unasked

Diligence that starts on the inbound, before the investor asks.

**Waits on:** inbox-forward.

**Joins on Saturday:** [readout](#readout) and [readout-page](#readout-page), which fill in as results land.

**Includes:**

- The scans run when a deck arrives; the readout is one click away from the email, or the readout link is the reply. This is the brief's "before you even ask" moment.
- **Speed first** ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:19 PM block). Each scan starts the moment its input exists, not after the whole room is in: the outside-world tabs start on the company name, the deck scan on the deck, the model checks when the model lands. The readout fills in as results arrive, and each piece shows whether it is still running, done, or waiting on an input (which goes on the ask list).
- The operator sees the first green and red flags within the first scans' run, and is told when the readout is complete.

**Done when:** a forwarded email with only a deck produces a partial readout with the deck and outside-world pieces filled and the rest marked waiting; adding the model to the same company fills the financial pieces without rerunning the finished scans.

**Who:** agent.

**Judgment:** yes.

### inbox-apis

Gmail and Outlook connected through their official APIs.

**Waits on:** inbound-unasked; Google's verification for a restricted scope, including the security assessment, before anyone outside the team can connect a Gmail account (Ken); Microsoft's permission for Outlook.

**Includes:** read-only access, decks only, under the same data rule.

**Done when:** a team member's Gmail and Outlook test accounts connect, a deck in each inbox becomes a company folder, and disconnecting removes the access and everything pulled.

**Who:** agent, with Ken for Google's verification.

**Judgment:** yes.

### multiplayer

Uncertain: Ken is not sure this works. Several people share one diligence today: angels follow a lead and split the work with co-investors ("I do it so we can share the task of due diligence." [angel, Aug 2013](https://news.ycombinator.com/item?id=6202816)), and YC once had alumni help read applications ([the voice-of-the-customer research](../reports/20261022.02_research/research_voice_of_customer.md), "What they do instead"). The idea is to let more than one person build the same readout at once, so the work goes faster ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:05 PM block).

**Waits on:** [reader-scenarios](#reader-scenarios); [checklist-coverage](#checklist-coverage).

**Includes:**

- A shared readout that several people work in at once: a lead operator, teammates, or co-investors in a syndicate the lead invites.
- Splitting the checklist: each person takes pieces or checklist items, and the readout shows who is on what and what is still open.
- Each person's steers and findings land in the shared readout with their name on them; the per-reader copies from reader-scenarios stay private until shared.
- A co-investor sees only what the lead shares, and nothing from the room the lead has not opened to them.

**Done when:** two people work the Hollis Voice readout at once, each takes different checklist items, both see the other's progress, and the shared readout shows who found what.

**Before building:** a small test of whether co-investors would actually work in one readout, using the online research method (posts by syndicate leads and angel groups about how they split diligence today). If the evidence says no, drop the slice.

**Who:** agent.

**Judgment:** yes.

### pilot

One fund uses Tricorder on real inbound deals.

**Waits on:** research-gaps, readout-store, inbox-forward, and the data rule written into the product brief.

**Includes:** one fund's associate forwarding real decks for a set period; what they flagged, what they ignored, and whether the partner trusted the first pass.

**Done when:** a fund has agreed to the pilot and to how its real decks are handled under the commitment on confidential data. Real decks are real companies' confidential data, so no real deck enters Tricorder until Ken decides that handling.

**Who:** Ken.

**Judgment:** n/a.

### product

What makes Tricorder a product: the fund buys, the associate uses.

**Waits on:** pilot; the overview page's cards on what Tricorder becomes as a business and on the name (the trademark note in [BRAND.md](BRAND.md)).

**Includes:** pricing to the fund, not the associate. The voice-of-the-customer research found the associate is the user and the partner is the buyer, that funds already pay for data-room-to-memo tools, and that angels already pay to get diligence done by proxy ([research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md), personas). The [product brief](PRODUCT_BRIEF.md) carries the recommendation.

- Angels want diligence and lack the time. Giving up upside to an accelerator, following a lead or splitting with co-investors is diligence bought by proxy, so angels are buyers too ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:27 PM block).
- The tools that already turn a data room into a sourced memo validate the idea. Tricorder does the same core job and adds to it: the green and red flags readout, the red-flag engine with accounting mislabels, fast cross-checking, and the scans beyond the room (1:36 PM block). The pitch never frames a competitor as something to beat.

**Done when:** the product brief states the price, who pays and per what, and the pitch's answer to "who would buy it" matches it.

**Who:** Ken.

**Judgment:** n/a.

---

## Saturday

Saturday is finishing, integration, the demo freeze and the demo. The four people build the slices below in the six-hour window, and the agent slices from the first horizon join them at the integration points in the run of show.

### The window

The schedule gives 10:30 AM to 4:30 PM for hacking, with lunch, so the plan uses six hours. The Luma page also says "9 hours of focused building" ([research_landscape.md](../reports/20261022.02_research/research_landscape.md), summary). That gap is three hours, by [check_saturday_hours.py](../features/20261022.01_hackathon_plan/check_saturday_hours.py). The board row TRI-ask-organisers asks which is right. If the room opens for longer, the extra time goes to the pieces that are showing saved results, in the reverse of the [demo fallback order](#demo-fallback-order), so more of the demo runs live. The freeze still sits one hour before judging.

### Who owns what

Each person owns folders, so pull requests do not touch the same files. This follows the feasibility research's Part 4.1, with the shared file readers and the contract-terms reading given to backend-and-data, and the market-signals panel to frontend. The full layout is in [ARCHITECTURE.md](ARCHITECTURE.md).

| Role | Folders | Slices | Build hours |
|---|---|---|---|
| captain | `schema/` except `readers.py`, `scans/memo/`, `eval/`, `demo/` | claim-result, readout, demo-freeze | 4.5 |
| frontend | `readout/`, and on Saturday the live re-run in `scans/signals/` | readout-page, market-signals | 4.5 |
| backend-and-data | repo root files, `server/`, `schema/readers.py`, `scans/video/`, `scans/readings/` | readers, pitch-video, contract-terms-saturday | 4.5 |
| design-and-finance | `scans/redflags/`, `scans/comps/` | redflag-engine, comps | 4.5 |

Build hours run from 10:30 AM to the 3:30 PM freeze, less a half-hour lunch: 4.5 hours each, 18 person-hours in all, from [check_saturday_hours.py](../features/20261022.01_hackathon_plan/check_saturday_hours.py). The same script checks that each role's slices fill its window and that the run of show below gives each slice its stated hours. Rehearsal adds 45 minutes for all four.

The captain carries no schema typing (an agent writes it this week), no readers (backend-and-data owns them) and no post drafting (an agent drafts the posts this week). The captain posts at 11:00 and 3:30 only.

The agent slices from the first horizon are merged to `main` before Saturday. Each joins its Saturday slice at the integration points in the run of show.

`schema/` is frozen before Saturday, in the [skeleton](#skeleton) slice. On Saturday only the captain changes it, and only to fix a bug. The exception is `schema/readers.py`, which backend-and-data fills in from 10:30 to 11:30. A new Python dependency goes through the captain, because the dependency list sits in a root file.

### readers

The shared file readers every scan and the quote checker import. Before this slice nobody owned them, and the captain had half an hour for a quote checker across all five formats ([critique_buildability.md](../features/20261022.01_hackathon_plan/critique_buildability.md), finding 3).

**Waits on:** skeleton (the `schema/readers.py` stub, written this week).

**Includes:**

- `schema/readers.py` filled in: PDF by page, xlsx by cell, CSV by row, Markdown by line, transcript by segment. Each returns the text at a locator, so a scan can quote it and the quote checker can find it again.
- The quote checker and every scan import these readers. No scan writes its own.

**Done when:** a test reads one known locator from each of the five formats in `data_room/hollis_voice/` and gets the expected text, and the readers are merged at 11:30 AM.

**Who:** backend-and-data.

**Hours:** 1.0 (10:30 to 11:30 AM).

**Judgment:** no.

### claim-result

The script that checks every quote against its source. The typed Claim schema itself is written this week in the [skeleton](#skeleton) slice.

**Waits on:** skeleton (the frozen schema and the readers stub), readers. The captain builds against the readers stub from 10:30 and switches to the real readers when they merge at 11:30.

**Includes:**

- `schema/check_quotes.py`: opens each claim's source at its locator through `schema/readers.py` and confirms the quote is there. URL sources are checked against their saved copies through `cache/index.json`. A claim that fails gets the confidence label `unverified` and moves to the "could not verify" box.

**Done when:**

- Tests show a real quote passing, an invented quote failing, and a claim with no source refused.
- Every example file in `sample_out/` passes the checker.

**Who:** captain.

**Hours:** 1.0 (10:30 to 11:30 AM).

**Judgment:** yes.

### redflag-engine

The red flags in the financials and metrics: the organisers' first direction, and first in the feasibility research's ranking.

**Waits on:** skeleton (the schema, frozen this week), readers (merged at 11:30), data-room, saturday-specs (the check list). The pure checks that compute numbers start at 10:30.

**Includes:**

- Scripts only on Saturday. A junior Python-and-Excel builder has 3.0 hours for 7 checks, so this slice makes no model call ([critique_buildability.md](../features/20261022.01_hackathon_plan/critique_buildability.md), finding 2). Every planted flag already has a script check (feasibility Part 3.2).
- One pandas check per planted flag in the data room research's Part 3.4, over the CSVs and the model: pilot booked as ARR, deck ARR against the model (1 percent tolerance), churn hidden in the cohort tab, burn against the hiring plan, customer concentration, gross margin without delivery costs, cumulative sign-ups shown as active clinics. The video-against-deck variant is found by the readout slice, because it needs the video scan's output.
- Deck claims read from the deck's claims page (slide 14) by regex, with `01_overview/claims.json` as the fallback (feasibility 1.1 and 1.9). The buildability critic's regex read 14 of 14 rows; three rows need a better label split.
- Files are read through `schema/readers.py`. The scan writes no reader of its own.
- The script decides that a number is wrong (feasibility Part 3.2). The model reading that gives a flag its clause quotes (the pilot contract) is the [contract-terms-saturday](#contract-terms-saturday) slice, owned by backend-and-data after the video slice. The model's reading of the cohort note is built before Saturday by an agent, in [financial-model](#financial-model).
- Each flag is a Claim with the claimed number, the computed number, a severity, and sources pointing at both places.
- The cells behind the green flags, read by script with no judgement: the round from the cap table (new money, pre-money, Series A ownership) and the model (`SERIES_A_RAISE`), the market size (`MARKET_TAM_USD`), staff today (`STAFF_NOW`) and staff after hiring (the last row of `hiring_plan.csv`). The cap table's sum check (`cap_table_reconcile`, [FRAMEWORKS.md](FRAMEWORKS.md) entry 1.10) runs here, so the clean cap table (DC3) reads clear. The readout's strong pieces rest on these claims, and no other Saturday slice writes them.
- `python -m scans.redflags <room>` writes `out/<room>/redflags.json`.
- A test in `scans/redflags/tests/` that compares the output to the answer key by check name.
- Accounting mislabels, the Saturday part ([FRAMEWORKS.md](FRAMEWORKS.md), entry 1.12; [writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:32 PM block). The two kinds this slice already checks carry their mislabel kind on the claim: the pilot booked as ARR is kind a, and gross margin without delivery costs is kind d. Entry 1.12 marks six more sub-checks as runnable on this room. They sit outside this slice's 3.0 hours: an agent builds them before Saturday in the [accounting-mislabels](#accounting-mislabels) slice, and they join this slice's output on Saturday.

**Done when:**

- On the seed drop, the test finds the four flags the research says the seed drop can show from this scan: deck ARR against the model, burn against the hiring plan, gross margin, and the clinic count.
- On the full room it also finds the pilot as ARR, the cohort churn and the customer concentration.
- None of the three decoys (the onboarding fee, the annual prepay, the clean cap table) is flagged.
- The round, market size and staff claims match the answer key's `green_flags` values within 1 percent.
- On the clean room from [blind-room](#blind-room), no planted-flag check fires.
- The pilot-as-ARR flag and the gross-margin flag each name their mislabel kind from entry 1.12.
- The scan runs with no network, so it can run live on the demo laptop.
- Every claim passes the quote checker.

**Who:** design-and-finance.

**Hours:** 3.0 (10:30 AM to 2:00 PM, less lunch).

**Judgment:** yes.

### readout

The top green and red flags, the overview and its drill-downs, assembled from the scans' claims: every piece of the company with a verdict, every sentence sourced. Second in the feasibility research's ranking.

**Waits on:** claim-result. It is built against `sample_out/` until the real scans land at the 1:00 PM integration point.

**Includes:**

- `scans/memo/` reads every `out/<room>/*.json` that exists, runs the quote checker again, and links claims that disagree (same label, unit and period, values apart by more than the tolerance) into `conflicts_with`.
- Links claims from independent sources that agree (same label, unit and period, values within the tolerance) into `corroborated_by`.
- Groups the claims into the nine pieces and gives each piece its verdict by the stated script rule ([FRAMEWORKS.md](FRAMEWORKS.md), "Piece verdicts"): looking strong, looking weak, mixed or not enough in the room, with a one-line reason and the counts of corroborating and contradicting sources. Pieces go in a fixed order, strong and weak alike.
- Picks the best green flags and the worst red flags from the piece verdicts and the flags, by the stated script rule ([FRAMEWORKS.md](FRAMEWORKS.md), "Top green and red flags"), and puts them first in `readout.json`.
- One model pass that writes connecting sentences. Each sentence must cite claim ids; a sentence with none is dropped. If it is not working at the fallback call, the demo shows the script's top flags, pieces and verdicts without it; it is first in the [demo fallback order](#demo-fallback-order). On the demo laptop it shows as frozen output.
- A missing scan becomes a gap in the readout, not an error.
- The ask list at the end of `readout.json`: what the operator should request from the founder ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:54 PM block; [FRAMEWORKS.md](FRAMEWORKS.md), "Ask list"). A script builds it from each gap's `would_need` field and each weak piece's reason. Each line says what to ask for, the claim or gap it would settle, and the piece it feeds. No model call.
- Writes `out/<room>/readout.json`.

**Done when:**

- The four ARR figures in the data room research's Part 3.4 (the model's $2,240,868, the deck's $2,500,000, the video's spoken figure of about $3,000,000, and the recurring ARR the scan computes) show as one conflict group inside traction and revenue, and that piece reads looking weak.
- On the full room, the pitch itself reads looking strong, with `corroborated_by` linking slide 13 to the cap table's Series A rows (DC3, the clean cap table).
- Every piece has a verdict, including "not enough in the room" where no number has a second source.
- On the full room, the green flag is the round (the pitch itself), and the red flags come out in the order the rule gives: runway, clinics, largest customer, gross margin, retention ([FRAMEWORKS.md](FRAMEWORKS.md), "Top green and red flags", worked example).
- The video-against-deck flag is found here.
- Deleting one scan's output file leaves a gap in the readout and no crash.
- On the Hollis Voice seed drop, the ask list names the files the seed drop leaves out, each with the gap or weak-piece claim it would settle: the expense ledger (actual monthly spend, which settles current burn and gross margin), monthly revenue by customer (retention and the largest customer's share), the Marlow pilot agreement, and the largest customer's order form (their contract language). The seed drop's file list is in [data_room_files.csv](../reports/20261022.02_research/data_room_files.csv).

**Who:** captain.

**Hours:** 1.5 (11:30 AM to 12:30 PM, and 1:30 to 2:00 PM).

**Judgment:** yes.

### readout-page

The web page the judges see. The feasibility research calls the readout "the thing shown on screen".

**Waits on:** skeleton (the generated types and the server routes, written this week). From 10:30 it is built against the example files.

**Includes:**

- A React page in `readout/` that reads `readout.json` through the server.
- The best green flags and the worst red flags at the very top, green first, each line one click from its piece. A green flag gets the same size and the same source links as a red one.
- The overview under them: one row per piece, in a fixed default order, with its mark, its one-line reason and its counts of corroborating and contradicting sources. Strong and weak rows look the same size. This is the demo's first screen ([The one workflow we demo](#the-one-workflow-we-demo)).
- One click on a piece opens its drill-down: its claims, with each conflict shown side by side. Inside traction and revenue, the four ARR figures sit in large type, each with its source chip. The comps panel sits in comps, the signals panel in market, and the video moments in the pitch itself.
- A footnote on every sentence. It opens the source as an in-page panel: a pre-rendered PNG of the slide or page, a small HTML table with the cited cell highlighted, the clause text, or the video at its second through the media fragment (`#t=35`). URL sources open their saved copy from `cache/`. A click never launches Excel or a PDF viewer: a spreadsheet app opening on a projector is slow, and it shows the associate the room's tidy rows ([critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md), finding 6). The panel also lists every other source that corroborates or contradicts the claim, each one click away.
- The video player beside the video claims; clicking a claim jumps to its start.
- A "could not verify" box, a gaps panel, and the score lines for this room, the sealed variant room and the clean room.
- The ask list at the end of the page, with a copy button, so the operator can paste it into an email to the founder.
- A switch between the seed drop and the full room.
- Up and down buttons on each overview row, so the operator can reorder the pieces ([PRODUCT_BRIEF.md](PRODUCT_BRIEF.md), "The operator sets the order"). The order lives in the page only. Saving it, and a default order by stage, is the [stage-views](#stage-views) slice, which an agent builds before Saturday. The frontend builds the buttons in the 2:30 to 3:30 PM polish hour. If that hour runs short, the demo shows the default order.
- Served from localhost, with no fonts or scripts from a CDN, so it needs no venue wifi.

**Done when:**

- The page renders `sample_out/` at 11:00 AM and the real outputs at 1:00 PM.
- A missing scan shows its gap panel, not a blank page or an error.
- Every footnote opens its source in the page.
- One click opens a piece's claims, and one more opens a claim's source with its corroborating and contradicting sources.
- Moving a piece up or down keeps its mark, its claims and its links, and a reload shows the default order.

**Who:** frontend.

**Hours:** 4.25 (10:30 AM to 3:30 PM, less lunch and the quarter hour for the [market-signals](#market-signals) panel).

**Judgment:** yes.

### pitch-video

The pitch video broken into claims with timestamps, third in the feasibility research's ranking.

**Waits on:** claim-result, readers (transcript by segment), record-pitch-video, keys (whisper.cpp on the demo laptop).

**Includes:**

- ffmpeg makes a 16 kHz mono WAV; whisper.cpp transcribes it with timestamps (feasibility 1.5).
- The video prompt returns claims with the segment ids they came from, so start and end seconds are copied from the transcript, not guessed.
- Keyframes at scene changes for thumbnails, if the budget allows.
- `python -m scans.video <room>` writes `out/<room>/video.json`. If the live run fails, the scan reads this week's saved transcript and says so in the result.

**Done when:** `video.json` holds the ARR claim from the planted line, its time range covers the spoken sentence, and its quote passes the checker.

**Who:** backend-and-data.

**Hours:** 2.5 (11:30 AM to 2:30 PM, less lunch).

**Judgment:** no.

### contract-terms-saturday

Every contract in the room, read for its terms and checked against how each customer is counted, on both demo rooms. It is the Saturday part of entry 1.13, "Contract terms", in [FRAMEWORKS.md](FRAMEWORKS.md) ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 1:53 PM block).

**Waits on:** redflag-engine (the pilot flag these claims sit beside), pitch-video (backend-and-data starts this after the video slice), readers, claim-result (the quote checker).

**Includes:**

- One model request per room reads every contract in it, with entry 1.13's prompt and schema, one schema per request. Hollis Voice has three contracts in `04_customers/`: the Cedar & Pine order form, the Marlow pilot agreement and the Brookline Row order form. Brasswick has four in `04_contracts/`: the Corvane agreement, the Ostley and Tessmore order forms, and the Norrgate statement of work.
- The terms read: start, end and length; the notice that ends a running contract, kept apart from the notice not to renew; auto-renewal; pilot or trial terms and any duty to convert; the price, any discount and the list price; payment terms. Each stated term is a claim that quotes its clause. The request also returns the clause fields (exclusivity, most-favoured-customer, change of control), but nothing reads them until [contract-terms](#contract-terms).
- Brasswick's Norrgate statement of work is a supplier contract. It is read for its terms and shown as info claims. It is not matched to a customer row, so it produces no check and no missing-customer gap.
- Three of entry 1.13's script comparisons, run on both rooms: `cancellable_within_notice_vs_arr`, `pilot_without_duty_to_convert_vs_recurring` and `contract_price_vs_counted_price`. They compare each contract with the ARR build (Hollis Voice) or the model's `Revenue_Build` tab (Brasswick), the MRR column (`mrr` in `customer_mrr_by_month.csv`, or `subscription_revenue` in Brasswick's metrics and customer files), and the largest customer's share. The price check also confirms the fee behind that share.
- The model reads clauses. The script decides that a number is wrong. Each comparison cites the flag it explains and sits beside the claim from entries 1.2, 1.6 and, where it applies, 1.12.
- If the hour runs short, Hollis Voice is finished before Brasswick is started.
- `python -m scans.readings <room>` writes `out/<room>/readings.json`.

**Not in this slice:** checks 3, 4 and 6 (plan revenue past a contract's end, a signed contract not yet live, a counted line with no contract), the exclusivity, most-favoured-customer and change-of-control clauses, and contracts beyond the room's. An agent builds those before Saturday in [contract-terms](#contract-terms). The cohort note reading is in [financial-model](#financial-model), also built before Saturday.

**Done when:**

- On Hollis Voice, the Marlow pilot agreement's 30-day notice and its "nothing requires the Customer to buy a subscription" clause are read with quotes. The notice check and the pilot check both flag it, with the clause beside the ARR row (`ARR_Build!E13`) and the `mrr` rows.
- On Hollis Voice, Cedar & Pine's 90 days and Brookline Row's 30 days are read as notice not to renew, and both contracts return clear on all three checks. Brookline Row's 10 percent discount is read and matches the counted price.
- On Brasswick, the three customer contracts return their terms. Corvane and Tessmore return clear. The price check finds Ostley Freight's $27,540 in `Revenue_Build` against the order form's $2,295 a month, and reports it as one cause with the annual prepayment flag from entry 1.12 (BF4).
- The Norrgate statement of work returns its term, its notice and its fee as info claims, and no comparison.
- On the Hollis Voice seed drop, which holds no contracts, the entry returns `cannot_check` with the gap "Not in the room: customer contracts".
- Every quote passes the quote checker. On the demo laptop the readings show as frozen output, saved for both rooms under `demo/frozen/` before the freeze.

**Who:** backend-and-data.

**Hours:** 1.0 (2:30 to 3:30 PM). Fourth in the [demo fallback order](#demo-fallback-order): if it is not working at the freeze, the pilot flag still shows from the engine's script check, without clause quotes.

**Judgment:** no.

### comps

Comparable companies and recent rounds, each with the reason it is a fair comp. Fourth in the feasibility research's ranking. It stays a Saturday slice, ranked by script from this week's cached filings, so all three of Track 2's asks (market signals, comps, red flags) are on screen ([critique_judge.md](../features/20261022.01_hackathon_plan/critique_judge.md), finding 2).

**Waits on:** claim-result, cached-data, saturday-specs (the selection rules, prompt and schema).

**Includes:**

- 5 to 8 comps in two groups: recent private rounds from the cached Form D files, and public companies from the cached XBRL facts (feasibility 1.2).
- The selection rules from FRAMEWORKS.md applied by script. The model writes only the "why this is a fair comp" sentence, and the demo laptop shows that sentence as frozen output.
- Each comp's number carries its source: the filing or the Form D row.
- Reads `cache/` only on Saturday, so EDGAR being slow changes nothing on screen.
- `python -m scans.comps <room>` writes `out/<room>/comps.json`.

**Done when:** the table has at least five comps, each with a reason and a source that passes the checker.

**Who:** design-and-finance.

**Hours:** 1.5 (2:00 to 3:30 PM).

**Judgment:** yes.

### market-signals

Hiring, traffic, reviews, news and pricing for the demo company's real competitors, and the live outside-world run on one approved real company. Fifth in the feasibility research's ranking. For Hollis Voice it is a static panel of this week's cached competitor readings, because live signals cannot show much for a company with no outside footprint ([critique_buildability.md](../features/20261022.01_hackathon_plan/critique_buildability.md), finding 9). Backend-and-data's freed hours go to the readers and the video.

**The live run on a real company** ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), 2:49 PM block). For the approved real company the demo uses, the panel sends this week's saved calls for that company again, live on stage. It uses only the sources that need no paid plan: the company's website, Hacker News, Apple's App Store lookup and SEC EDGAR. It takes this slice's slot, so Saturday's hours do not change. Any call that fails or is slow shows this week's saved copy from [cached-data](#cached-data), with its date. The full live scan, with resolution and every tab, is [outside-in](#outside-in), which an agent builds before Saturday and which joins this panel on Saturday.

**Waits on:** signals-readings (this week's `cache/signals/signals.json`); yc-rooms and cached-data, for the approved real company's saved calls.

**Includes:**

- The signals panel in the readout page, reading `cache/signals/signals.json` through the server.
- Each reading shows the date it was taken, and each number links to its saved source.
- On the approved real company's readout, a live re-run of its saved calls. Each fresh answer is saved beside the old copy and shown with the time it was read. The panel carries the room's synthetic label.

**Done when:** the panel shows at least three competitors on the readout page, and every number's link opens its saved copy. On the approved real company, the live re-run shows each source with the time it was read, and with the network off it shows this week's saved copies with their dates.

**Who:** frontend.

**Hours:** 0.25 (inside the 2:30 to 3:30 PM polish hour).

**Judgment:** no.

### demo-freeze

Integration, the score, the freeze and the rehearsal.

**Waits on:** every slice above, and the agent slices that join them on Saturday.

**Includes:**

- The captain merges at the integration points and runs `bin/smoke` on both rooms.
- `eval/score.py` reads the readout and the answer key and prints how many of the 8 planted entries were found and how many of the 3 decoys were wrongly flagged. The score goes on the page as one line, with the real number, even if it is 7 ([critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md), finding 7).
- The clean-room run: the readout on the plants-off room from [blind-room](#blind-room). `eval/score.py` prints how many flags it raised.
- The variant run: at the 3:30 PM freeze the outside person sends the sealed key. The readout runs on the variant room, and `eval/score.py` prints the real numbers against that key. Nobody changes a check after the key opens.
- The approved real company's room, run like Hollis Voice's, with its outside-world panel's live re-run tested on the network the demo will use.
- The frozen outputs saved under `demo/frozen/` as the fallback for every step of the script, including the variant and clean runs, the real company's readout with this week's saved outside copies, and the last passing run of each agent slice shown on stage.
- A `demo-freeze` git tag at 3:30 PM. After it, nothing merges except a fix for a crash found in rehearsal, and only on the captain's call.
- The rehearsal: a three-minute core with a five-minute extension, from the beat sheet in [demo-script](#demo-script). At least two run-throughs, one of them on the backup laptop from the frozen files. The schedule gives 5:30 to 6:00 for every team's demo plus the winner, so the slot is likely three minutes or less (demo critique, finding 1).

**Done when:** the three-minute core on the frozen build fits three minutes, the core plus the extension fits five, and the backup laptop can show every step from saved files.

**Who:** captain. All four rehearse.

**Hours:** 2.0 for the captain (1:00 to 1:30 PM and 2:00 to 3:30 PM), plus 0.75 for all four (3:30 to 4:15 PM).

**Judgment:** n/a.

### A steer on stage (a card)

Ken's 1:12 PM and 1:15 PM comments let the operator steer the readout: an instruction on a piece rewrites it, or gets more info for it from new sources, with a visible diff ([steering](#steering)). An agent builds steering before Saturday, and it joins the readout and the readout page on Saturday. Whether the three-minute core shows one steer live (one piece rewritten from one instruction, such as "treat the pilot as non-recurring") is the overview page's card. It has no owner or hours in the table above, because the build is done before Saturday. Showing it costs demo seconds, not build hours.

### The demo laptop

From the buildability critique's finding 11 and the demo critique's "What else goes wrong live":

- **The demo laptop is Ken's:** M2 Max, with ffmpeg, Python 3.13 and Node 20. Backend-and-data's laptop is the backup, on `demo/frozen/`.
- **The live step runs script checks only.** They need no network. Panels that need a model (the memo's connecting sentences, the comp reasons, the contract-terms readings) show frozen output. Nothing on screen calls a model at render time. A live steer, if the card puts one on stage, is the exception: it calls a model and needs the network, and its fallback is a saved steer from `demo/frozen/`.
- **Only the live beat needs the network.** The page and the frozen files are served from localhost, with no fonts or scripts from a CDN. The real company's outside-world panel needs venue wifi or the phone hotspot. Without either, it shows this week's saved copies with their dates, and Ken says so.
- **Display.** Every laptop brings a USB-C to HDMI adapter. Rehearse at 1280 by 720 at 150% zoom.

### Run of show

| Time | captain | frontend | backend-and-data | design-and-finance | Integration point |
|---|---|---|---|---|---|
| 9:00 to 10:00 | Breakfast and team formation. Confirm roles and folders. Ask the organisers about the track change and the board's open questions (TRI-track-fix, TRI-ask-organisers). Ask Akta's people for a coupon. | Clone, install, run the Part 0 checks. | Clone, check whisper.cpp runs on the demo laptop. | Clone, open the data room, read the check list. | Every laptop has the `.env` keys and a USB-C to HDMI adapter. |
| 10:00 to 10:20 | Organisers' intros and demos. Note any sponsor offer. | Listen. | Listen. | Listen. | |
| 10:20 to 10:30 | Read this table aloud. Name the demo fallback order. | Huddle. | Huddle. | Huddle. | |
| 10:30 to 11:30 | claim-result: quote checker, against the readers stub. At 11:00, post the first social post. | readout-page on the example files. | readers. | redflag-engine: pure checks on the CSVs and the model. | |
| 11:30 | Merge the readers and the quote checker. | Pull. | Pull. | Pull. | **1. Readers merged.** If they are late, the memo's model pass shows saved output on stage. |
| 11:30 to 12:30 | readout: memo. | readout-page. | pitch-video. | redflag-engine: the deck's claims page by regex, the green-flag cells, and the seed drop. | |
| 12:30 to 1:00 | Lunch at desks. | Lunch. | Lunch. | Lunch. | |
| 1:00 to 1:30 | demo-freeze: merge, first full run on the seed drop. | readout-page on real outputs. | pitch-video. | redflag-engine: the full room. | **2. First end-to-end run.** If the red-flag engine does not find the seed drop's flags, backend-and-data pairs with design-and-finance after the video slice, and contract-terms-saturday falls back if the pairing runs past 2:30. |
| 1:30 to 2:00 | readout: finish the piece verdicts, the top green and red flags, conflicts and corroborations, and the ask list. | readout-page: in-page source panels. | pitch-video. | redflag-engine: the clean room. | |
| 2:00 to 2:30 | demo-freeze: score script, frozen outputs. | readout-page: source panels and video jump. | pitch-video. | comps. | |
| 2:30 | Run the full room, the clean room and the approved real company's room, read the score. | | | | **3. Fallback call.** Whatever is not producing claims shows saved results on stage, in the demo fallback order. Nothing is dropped from the build. The agent slices that joined today run on the full room. |
| 2:30 to 3:30 | demo-freeze. | readout-page polish: the ask list's copy button and the reorder buttons, and the market-signals panel with its live run on the approved real company. | contract-terms-saturday. | comps. | |
| 3:30 | Tag `demo-freeze`. Post the second social post. The outside person sends the variant room's key. | | | | **4. Demo freeze.** |
| 3:30 to 4:15 | Rehearse, presenting: the three-minute core, then the five-minute extension. | Rehearse, driving the laptop. | Rehearse on the backup laptop. | Rehearse, ready for numbers questions. | Two run-throughs. |
| 4:15 to 4:30 | Fresh runs on the variant room and the clean room, close tabs. | Page ready on all rooms. Test the live outside panel on the approved real company on the demo network. | Backup laptop on the frozen files, including the variant and clean runs. | Answer key scores checked for the full room and the variant room. | |
| 4:30 to 5:30 | Judging: presents. | Drives. | Backup. | Answers questions on the numbers. | |
| 5:30 to 6:00 | Demos and the winner: presents. | Drives. | Backup. | Ready. | |

**Who presents:** the captain. The frontend drives the readout page. Backend-and-data holds the backup laptop with the frozen files. Design-and-finance answers questions on the numbers. For the $150 social content prize, the captain posts at 11:00 and 3:30 only, from this week's drafts ([social-posts](#social-posts)), in the voice of [BRAND.md](BRAND.md).

### Demo fallback order

Nobody drops a feature because the day runs long. This list says what the demo skips, or shows from saved results, when a piece is not working at the 2:30 PM fallback call or the 3:30 PM freeze. The piece is still built; it just does not run live in the three minutes. The order is the feasibility research's demo-value ranking reversed (red-flag engine, readout, pitch video, comps, market signals), with the memo's model pass first, because the script's top flags, pieces and verdicts carry the demo on their own ([critique_buildability.md](../features/20261022.01_hackathon_plan/critique_buildability.md), notes):

1. **The memo's model pass.** The readout shows its script-set top flags, pieces and verdicts without the connecting sentences.
2. **Market signals.** The panel shows this week's saved readings. If the panel itself is not working, the demo skips it.
3. **Comps.** The panel shows the cached comp list without the live ranking, or the demo skips it.
4. **Contract terms** (contract-terms-saturday). The pilot flag still shows from the engine's script check, without clause quotes.
5. **Pitch video.** The demo plays the captioned clip and shows this week's saved transcript and claims, which the feasibility research already plans as the fallback.
6. **An agent slice that joined today.** Steering, the memo export, the outside-in tabs, the bank check and the rest each show their last passing run from `demo/frozen/`, or the demo skips them.

The red-flag engine, the readout and the readout page are always shown; they are the demo. Inside the readout page, the reorder buttons fall back first, to the default order; the ask list and its copy button stay. When a piece falls back, its owner pairs with the owner of the slice that is behind, in that owner's folder and branch, so pairing never causes a merge conflict.
