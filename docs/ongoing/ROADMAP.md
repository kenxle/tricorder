# Roadmap

## Charter

**What belongs:** What comes next and in what order, grouped by horizon: this week, Saturday, after Saturday. What each slice waits on. For Saturday, who builds each slice and its hour budget, and the run of show.

**What does not:** Dates promised to anyone. Work in flight; that lives on the board. How a slice works inside; that goes in its feature folder and in [ARCHITECTURE.md](ARCHITECTURE.md).

**Level of detail:** One slice per heading, with short lists. A builder can pick up a slice and know what done looks like.

**Sources:** The writers' brief ([00_brief_for_writers.md](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), every "Added" block through 2026-10-22 at 11:20 AM, the 12:55 PM block that makes the readout an overview, the 1:09 PM block that puts the best green flags and the worst red flags first, and the 1:12 PM block on steering), the organisers' tracks ([problem_tracks.txt](../reports/20261022.01_hackathon_sources/problem_tracks.txt)), the feasibility research ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), the main source for scan order, stack, folder owners and keys), the data room research ([research_data_room.md](../reports/20261022.02_research/research_data_room.md)), the landscape research ([research_landscape.md](../reports/20261022.02_research/research_landscape.md)), the voice-of-the-customer research ([research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md)), the guardrails ([guardrails.md](../../.claude/guardrails.md)), the board ([BULLETIN.md](../BULLETIN.md)) and the three critiques ([judge](../features/20261022.01_hackathon_plan/critique_judge.md), [buildability](../features/20261022.01_hackathon_plan/critique_buildability.md), [demo](../features/20261022.01_hackathon_plan/critique_demo.md)), which set the Saturday slices, the demo opening and the beat sheet. The shape is copied from My Text Reminders' [ROADMAP.md](../../../my-text-reminders/docs/ongoing/ROADMAP.md). Hour budgets come from [the schedule](../features/20261022.01_hackathon_plan/00_brief_for_writers.md) and were added up by a script, not by hand.

## How to read a slice

- **Waits on** names the slices or board rows that must be done first. Board rows are on [BULLETIN.md](../BULLETIN.md).
- **Includes** is the list of what the slice must contain. The reviewer checks the work against it.
- **Done when** is the list of checks that prove it works.
- **Who** names a role: captain, frontend, backend-and-data, design-and-finance, "agent" for this week's agent work (documents, data and the empty skeleton), or "Ken" for things only Ken can do. The board names the people behind each role.
- **Hours** appears on Saturday slices only. It is a budget inside the six-hour hacking window, not a prediction. When a slice uses up its budget, the captain decides whether it ships as it is, falls back to saved results, or is cut.
- **Judgment** picks the builder's model when an agent builds or rebuilds the slice after Saturday. Yes means Opus, because the slice needs design or product calls. No means Sonnet. Ken-only slices say "n/a".

A slice is done when its pull request is merged to `main`. On Saturday the captain merges, and a red CI blocks a merge even in the room ([guardrails.md](../../.claude/guardrails.md)).

## The one workflow we demo

**Recommended: open on the top green and red flags, already waiting, then the overview, then drill into the weakest piece and one strong piece.** The first screen is the best green flags and the worst red flags for Hollis Voice's full room. Under them is the overview: each piece of the company with its mark (looking strong, looking weak, mixed, or not enough in the room) and its reason in one line ([writers' brief, 12:55 PM and 1:09 PM blocks](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). The first click opens the weakest piece, traction and revenue. There the ARR figures sit side by side: about $3.0M said on video, $2.5M in the deck, $2.24M in the model, $2.06M in the billing rows, each with its source chip ([critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md), verdict; the exact figures are in `data_room/answer_key.json`, `facts`). The next opens one strong piece, the pitch itself, which is also the green flag: the round on slide 13, corroborated by the cap table, each source opening the other. This is true on stage: the run finished before the captain walked up. The body follows the [demo-script](#demo-script) beat sheet: the green and red flags, the overview, the video sentence, the pilot clause, the strong piece, the gaps. Then one line reads out the runs on the sealed variant room and the clean room ([blind-room](#blind-room)). The forwarded pitch email is the closing "next" line: forward it, and the readout is waiting before you open it. That keeps the "before you even ask" moment from the brief's 11:20 AM block as what comes next. Why this form: judges remember what they saw working, and opening on a forward started by hand spends the first 20 seconds on the one thing on screen that is not real ([critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md), finding 2; [critique_judge.md](../features/20261022.01_hackathon_plan/critique_judge.md), finding 6).

**The real forward, only if time allows.** The forwarding address is an after-Saturday slice ([inbox-forward](#inbox-forward)). A small inbox-polling script needs no OAuth review, so it can be built on Saturday, but only if the red-flag engine and the readout are done at the 2:30 cut call. Otherwise the close says it in one line.

**The other forms:** open on the forwarded email, started by hand and said so; or open on the data room upload. The overview page carries the card ("The demo opening").

---

## This week (no scan logic)

The organisers say Saturday is build-only and everything before code happens this week ([brief, 10:18 AM block](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). So this horizon holds research, people work, data and documents. The data room generator is a script: the organisers say to bring a synthetic data room, so making it is allowed and expected. It lives in `data_room/` and no product folder imports it. This roadmap is written to option B on the [skeleton-card](#skeleton-card), so an agent also writes the empty [skeleton](#skeleton) this week, with no scan logic.

### data-room

The synthetic Hollis Voice data room, its generator and its answer key, built to the [data room research](../reports/20261022.02_research/research_data_room.md), Part 3.

**Waits on:** nothing. It builds to the research's recommended company (Hollis Voice, an AI phone agent for independent vet clinics). If Ken picks another company on the overview page, the generator takes a different config. Ken's yes or no on installing `xlsxwriter` decides whether model formulas carry stored values; without it the generator writes plain values (research Part 3.6).

**Includes:**

- The layout from research Part 3.6 at the repo root: `data_room/generate.py`, `src/` (facts, plants, tables, workbook, pdfs, names, answer key), `tests/`, `hollis_voice/` (the full room) and `hollis_voice_seed_drop/` (the thin first tier).
- The 16 files in research Part 3.3, every one generated from one seeded simulation (seed 20261024).
- The 8 planted entries (7 flags plus the video variant) and the 3 clean decoys in research Part 3.4.
- `data_room/answer_key.json` outside both room folders, so Tricorder is never pointed at it. Each entry's `check` field uses the check names written in the [saturday-specs](#saturday-specs) slice, so Saturday's test can match a readout flag to a key entry.
- `01_overview/claims.json` in both rooms, written by the generator from the same list as the deck's claims slide (slide 14), with the deck's claims as data, the fallback the feasibility research recommends when PDF reading fails ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), 1.1 and 1.9).
- The footer "Synthetic data room for Deal Flow NYC 2026. Not a real company." on every page and sheet. Invented names only; emails on `example.com`.
- A fresh web search for the company name before it appears anywhere public (research open point).

**Done when:**

- `python3 data_room/generate.py` writes both rooms and the answer key from a clean checkout.
- The three tests in research Part 3.6 pass: with plants off, the reference checks find nothing; with plants on, each finds its flag and none finds a decoy; the same seed gives the same CSV and PDF bytes and the same workbook cell values.
- The reference checks stay inside `data_room/tests/`. Saturday's red-flag engine is written fresh in the room and does not copy them.

**Who:** agent. Ken reviews the deck and the video script.

**Judgment:** yes.

### blind-room

A room Tricorder has never seen, and a room with nothing planted. The team wrote the room, planted the flags, wrote the answer key and then wrote one check per flag, so a perfect score on that room proves nothing to a partner ([critique_judge.md](../features/20261022.01_hackathon_plan/critique_judge.md), finding 1). A clean room that comes back clean is the strongest ten seconds against "rigged" ([critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md), finding 7).

**Waits on:** data-room, including the generator changes in progress now. Ken finds the person outside the build.

**Includes:**

- A plants-off switch in `data_room/generate.py`. The data room research describes one, and the generator has none (demo critique, finding 7). With plants off, it writes the clean room: the same company with no planted flags.
- A second seed. Run with it, the generator moves the values and writes the variant room.
- Someone outside the build picks which flags the variant room carries: a teammate who is not writing the engine, or a friend. The judge's version drops or adds one flag. An agent that has not seen the check list runs the generator for them.
- The variant room's answer key is sealed. The person who picked the flags keeps it and sends it to the captain at the 3:30 PM freeze. Nobody building the engine opens it before then.
- Both rooms sit beside the others in `data_room/`, with no answer key inside either room folder.

**Done when:**

- With plants off, the reference checks find nothing.
- The variant room exists, its key is with the outside person, and nobody on the build has opened it.
- On Saturday, the readout runs on the variant room and the clean room, and the real numbers are read out in one line ([demo-freeze](#demo-freeze)).

**Who:** agent for the switch and the second seed. The person outside the build picks the flags and seals the key.

**Judgment:** yes.

### record-pitch-video

The founder's two-minute pitch, recorded as a voiceover over the deck slides by someone who is not on stage Saturday. The script opens "Hi, I'm Imogen Tarrant", and judges who see the presenter play the founder stop believing the room ([critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md), finding 5).

**Waits on:** data-room (the script is written after the deck's claims page exists, research Part 3.6, step 7).

**Includes:**

- The voiceover from `01_overview/pitch_video_script.md`, over the deck slides, with the planted line at about 0:35 saying about three million dollars in ARR, against the deck's $2,500,000 (research Part 3.4, PF2b).
- A five-second clip of the 0:35 sentence, with burned-in captions, as an H.264 MP4. This clip is what plays on stage. The line is framed as the ladder: against the billing rows' $2,060,868, three million is 46% more (demo critique, finding 5).
- The video file copied into both rooms beside the script.
- A transcript made once by hand with whisper.cpp on the demo laptop and saved next to the video, so the demo has a result if the live run fails ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), 1.5).
- whisper.cpp is not installed on the demo laptop yet. Install it this week and save the transcript.
- A phone recording may be HEVC, which not every browser plays. Convert it once to H.264 MP4: `ffmpeg -i phone_recording.mov -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart pitch_video.mp4`.
- The video file stays out of git, because GitHub blocks files over 100 MiB. `.gitignore` lists `pitch_video.mp4` and `*.mov` under `data_room/`. Share the file outside git.

**Done when:** the video and the captioned clip play in the browser on the demo laptop, and the saved transcript contains the ARR sentence with its timestamp.

**Who:** Ken arranges it. The voice is someone off stage, not the presenter: a friend, or a teammate who does not present. The founder is invented, so the video uses no real person's likeness without consent (feasibility 1.5).

**Judgment:** n/a.

### interviews

Two or three short diligence interviews with associates, principals or angels Ken knows, using the organisers' three questions. The interviews are what make the buyer story real. Today the partner's pay rating is inferred from a competitor's case study and a pricing roundup, and no buyer has spoken yet ([critique_judge.md](../features/20261022.01_hackathon_plan/critique_judge.md), finding 3).

**Waits on:** nothing. This is the board row TRI-interviews (run two or three diligence interviews before Saturday).

**Includes:** each answer in `docs/reports/20261022.02_research/interviews.md`, one section per person, role only. The voice-of-the-customer research found no public number for how long a first-pass memo takes, and no regret story about hidden churn; ask both directly. The judge's fix: put one named, consenting investor's answer in the founder brief's Problem section. The best version is one fund that says it would forward its next three decks.

**Done when:** at least two interviews are written up, and the demo script quotes what they said about the slowest part.

**Who:** Ken.

**Judgment:** n/a.

### keys

Every key and account Saturday needs, in a local `.env` that is never committed, plus the demo laptop's tools.

**Waits on:** nothing. This is the board row TRI-sponsor-keys (get the sponsor API keys before Saturday).

**Includes**, from the feasibility research's Part 5:

- Anthropic API key. Required for every scan.
- Tavily key. Free 1,000 credits a month, no card.
- You.com key, or the keyless MCP profile (100 queries a day).
- GitHub token. Free; 5,000 requests an hour.
- Akta key, plus a question to the sponsor about the paid plan. Pay-as-you-go returns 403 on headcount, web traffic, jobs and reviews; those need the Subscription plan or a sponsor coupon.
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

### cached-data

The outside data the comps and market-signal scans read on Saturday, saved as files, so nothing on stage waits on a live call.

**Waits on:** keys (Akta and Tavily for the signal pulls; the EDGAR User-Agent for the SEC downloads).

**Includes**, from the feasibility research's 1.2, 1.3 and 1.6:

- The last four Form D quarterly zips.
- XBRL company facts for 8 to 12 public companies near the demo company's space.
- 10 to 20 Form D rounds chosen by hand as private comps.
- 3 to 5 real competitors in voice AI for vet clinics, with every Akta signal the key allows and their pricing pages through Tavily.
- Hacker News and app-store results for one or two of those competitors, run by hand.
- Each comp candidate's 10-K Item 1 text, which the comp prompt (2.1) reads.
- A saved page describing each Form D issuer, which the private-comp prompt (2.2) reads.
- `cache/index.json`, which maps each URL to its saved file. The quote checker reads it to check URL sources.
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
- The memo's piece table, verdict rule and top-flags rule ([FRAMEWORKS.md](FRAMEWORKS.md), "Piece verdicts" and "Top green and red flags"), and the prompt for its connecting sentences.
- One hand-written example result file per Saturday scan, in the Claim schema, so the readout page can be built from 10:30 before any scan runs.
- A static mock of the readout layout that Ken can edit (feasibility 1.8).
- Each structured-output schema sent once this week in a real call, so any refusal shows up before Saturday. On Saturday each request carries one schema.

**Done when:** each Saturday slice below names the spec entry it types in, and each example file validates against the Claim schema by eye and by the frameworks writer's check.

**Who:** agent. Ken reviews.

**Judgment:** yes.

### skeleton

The empty repo the four people build in, with the typed Claim schema and a stub for the shared file readers. No scan logic. This is option B on the [skeleton-card](#skeleton-card): with every role budgeted to its last minute, building it on Saturday spends the first half hour of two people and puts the team behind ([critique_buildability.md](../features/20261022.01_hackathon_plan/critique_buildability.md), finding 7).

**Waits on:** the skeleton-card decision; Ken asks the organisers first and tells the judges plainly. saturday-specs (the example files). The Claim schema in [FRAMEWORKS.md](FRAMEWORKS.md), "The shared Claim", which is the single source for every field type.

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

**If the organisers say no:** option A. The skeleton and the schema typing take the first half hour of backend-and-data and the captain on Saturday. Backend-and-data's half hour comes out of the red-flag model readings. The captain's comes out of the quote checker, which goes back to the half hour first planned.

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

### demo-script

The demo script and Saturday's run of show, written for the captain to present: a three-minute core with a five-minute extension. The schedule gives 5:30 to 6:00 for every team's demo and the winner ([brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)), so the slot is likely three minutes or less ([critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md), finding 1). The board row TRI-ask-organisers asks the slot length.

**Waits on:** data-room, blind-room, record-pitch-video, and the overview page's card on the demo opening.

**Includes:**

- The beat sheet below. It opens on the top green and red flags already waiting, then the overview, drills into the weakest piece (revenue, with its four ARR numbers) and one strong piece (the pitch itself), and ends the core on the forward as the "next" line.
- Who says what and who drives the laptop.
- The fallback for each step: which saved file to show if a scan fails on stage.
- Answers ready for the questions the landscape research expects from this panel: where the data goes, what happens when a scan fails, what is hard to copy ([research_landscape.md](../reports/20261022.02_research/research_landscape.md), Part 3).
- The run of show below, checked against the day's real schedule once the organisers answer the board row TRI-ask-organisers (who Roundtable is, the build window and more).

**The beat sheet**, from the demo critique, with the variant and clean runs added, and reshaped after Ken's 12:55 PM and 1:09 PM comments to open on the top green and red flags, then the overview. Three-minute core, then the extension if the slot is five minutes. The frontend drives. Backend-and-data holds the backup laptop on `demo/frozen/`. Start a run on the sealed variant room in a hidden tab at 0:00. It runs script checks only, so it needs no network.

| Time | On screen | Ken says | Fallback |
|---|---|---|---|
| 0:00 | The top of the readout. The green flag: the round adds up. The red flags, worst first by the top-flags rule: runway 37 months shown, 19 with all 24 hires; clinics 357 claimed, 212 paying; largest customer under 9% claimed, 21% found; margin 80% against 58.1%; retention 102.6% shown, 87.3% rebuilt, 11 customers dropped (answer_key.json, PF3 to PF7). Below them, the overview: each piece with its mark and its reason in one line. | "Here's a startup the way you'd want a first pass: the best green flags, the worst red flags, then every piece of the company, strong or weak, one line each. Every number is two clicks from its source." | Backup laptop on the frozen readout. Last resort: a screenshot. |
| 0:30 | Click traction and revenue: the four ARR figures in large type, each with its source chip. Click "video 0:35": a five-second captioned clip, "about three million" | "Revenue reads weak: four ARR numbers. On video, three million. In the billing rows, $2.06 million. That's 46% more." | No sound: captions carry it. No video: the transcript line with its timestamp. |
| 1:00 | Click the model figure: ARR_Build row 13, "Marlow Veterinary Group (pilot)", then clause 8, "No duty to convert" | "Part of the gap is a six-month pilot counted as a year of revenue. Here's the clause." | Pre-rendered PNGs of the cell and the clause. |
| 1:30 | Back to the top, click the green flag; the pitch itself opens: slide 13's $9,000,000 at $45,000,000 pre-money for 16.67%, beside the cap table's Series A rows; click the cap table figure and slide 13 opens (answer_key.json, `deck_claims` and DC3) | "The green flag: the round adds up. The deck asks for nine million at forty-five pre, and the cap table computes the same 16.67%. Green flags get the same two clicks as red ones." | Pre-rendered PNGs of slide 13 and the cap table rows. |
| 2:00 | Back on the overview: market reads "not enough in the room"; the gaps panel ("not in the room"), then the score lines: this room; the sealed variant room, from the hidden tab with its start time; the clean room | "It says what's missing and leaves clean things alone. We planted eight problems and three traps. Today it found X and tripped Y. On a room someone outside the team planted and sealed, started when I began talking, it found X of N. On the same company with nothing planted, it raised Z flags." | Scores from the frozen run and the 4:15 variant and clean runs. Never wait on stage. |
| 2:30 | Readout header: "every line sourced" | "Next: forward the pitch email, and this is waiting before you open it. The partner pays per seat. If you do first passes, try it on your next deal." | None needed. |
| 3:00 | Switch from the seed drop to the full room: the three flags that need the second tier light up | "With the first tier alone, five of eight. Add the detail, and the pilot, the churn and the concentration appear." | Skip the beat. |
| 3:30 | The clean room's readout | "Same company, nothing planted. This is everything it flags." | Skip the beat. |
| 4:00 | Readout stays up | Questions: where the data goes, "isn't this a wrapper", what happens when a scan fails, what it finds in a room we didn't make (answers in BRAND.md) | n/a |

The numbers in the beats come from the room as the demo critic read it on 2026-10-22. The generator is being revised this week, so on Saturday use the numbers from the frozen run.

**Done when:** Ken has read the core aloud against a timer in three minutes or less, and the core plus the extension in five.

**Who:** agent, then Ken.

**Judgment:** yes.

### skeleton-card

A decision card for the overview page: does an empty repo skeleton count as code?

**Waits on:** nothing. The critics weigh it ([brief, 10:18 AM block](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)).

**The two options:**

- **A. The skeleton is code. Build it on Saturday.** The folder layout, the CI command and the typed Claim result are the first Saturday slices. They take the first half hour of two people. Before Saturday the repo holds only documents, `data_room/` and `cache/`. To a judge who asks what was built today, the answer is every line of product code.
- **B. The skeleton is setup. An agent writes it this week.** Empty folders and packages, `bin/ci-py`, `bin/ci-web`, the CI config, the dependency list, `.env.example`, the Claim schema typed in from the FRAMEWORKS JSON Schema, and the `schema/readers.py` stub, with no scan logic. The captain and backend-and-data each get half an hour back on Saturday. The risk: the organisers wrote "On Saturday you only build" and "Everything a founder does before writing code happens this week", and commits dated before Saturday are visible to anyone who looks.

**This roadmap is written to option B**, as the buildability critic recommends ([critique_buildability.md](../features/20261022.01_hackathon_plan/critique_buildability.md), finding 7). Its condition: Ken asks the organisers first and tells the judges plainly. The [skeleton](#skeleton) slice sits in this week, and the freed half hours go to the slices the critics name: the captain's to the quote checker ([claim-result](#claim-result)), and backend-and-data's to the shared file readers ([readers](#readers)). If the organisers say no, the skeleton slice says what moves back.

**Who:** agent writes the card. Ken decides.

**Judgment:** n/a.

---

## Saturday

### The window

The schedule gives 10:30 AM to 4:30 PM for hacking, with lunch, so the plan uses six hours. The Luma page also says "9 hours of focused building" ([research_landscape.md](../reports/20261022.02_research/research_landscape.md), summary). That gap is three hours, by the budget script. The board row TRI-ask-organisers asks which is right. If the room opens for longer, the extra time goes to bringing back cut slices in the reverse of the cut order. The freeze still sits one hour before judging.

### Who owns what

Each person owns folders, so pull requests do not touch the same files. This follows the feasibility research's Part 4.1, with the shared file readers and the red-flag model readings given to backend-and-data, and the market-signals panel to frontend. The full layout is in [ARCHITECTURE.md](ARCHITECTURE.md).

| Role | Folders | Slices | Build hours |
|---|---|---|---|
| captain | `schema/` except `readers.py`, `scans/memo/`, `eval/`, `demo/` | claim-result, readout, demo-freeze | 4.5 |
| frontend | `readout/` | readout-page, market-signals | 4.5 |
| backend-and-data | repo root files, `server/`, `schema/readers.py`, `scans/video/`, `scans/readings/` | readers, pitch-video, redflag-readings | 4.5 |
| design-and-finance | `scans/redflags/`, `scans/comps/` | redflag-engine, comps | 4.5 |

Build hours run from 10:30 AM to the 3:30 PM freeze, less a half-hour lunch: 4.5 hours each, 18 person-hours in all, from the budget script. Rehearsal adds 45 minutes for all four.

The captain carries no schema typing (an agent writes it this week), no readers (backend-and-data owns them) and no post drafting (an agent drafts the posts this week). The captain posts at 11:00 and 3:30 only.

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
- The script decides that a number is wrong (feasibility Part 3.2). The model readings that explain a flag (the pilot contract clause, the cohort note) are the [redflag-readings](#redflag-readings) slice, owned by backend-and-data after the video slice, or moved to after Saturday.
- Each flag is a Claim with the claimed number, the computed number, a severity, and sources pointing at both places.
- `python -m scans.redflags <room>` writes `out/<room>/redflags.json`.
- A test in `scans/redflags/tests/` that compares the output to the answer key by check name.

**Done when:**

- On the seed drop, the test finds the four flags the research says the seed drop can show from this scan: deck ARR against the model, burn against the hiring plan, gross margin, and the clinic count.
- On the full room it also finds the pilot as ARR, the cohort churn and the customer concentration.
- None of the three decoys (the onboarding fee, the annual prepay, the clean cap table) is flagged.
- On the clean room from [blind-room](#blind-room), no planted-flag check fires.
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
- One model pass that writes connecting sentences. Each sentence must cite claim ids; a sentence with none is dropped. This pass is first in the cut order: the script's top flags, pieces and verdicts are enough for the demo. On the demo laptop it shows as frozen output.
- A missing scan becomes a gap in the readout, not an error.
- Writes `out/<room>/readout.json`.

**Done when:**

- The four ARR figures in the data room research's Part 3.4 (the model's $2,240,868, the deck's $2,500,000, the video's spoken figure of about $3,000,000, and the recurring ARR the scan computes) show as one conflict group inside traction and revenue, and that piece reads looking weak.
- On the full room, the pitch itself reads looking strong, with `corroborated_by` linking slide 13 to the cap table's Series A rows (DC3, the clean cap table).
- Every piece has a verdict, including "not enough in the room" where no number has a second source.
- On the full room, the green flag is the round (the pitch itself), and the red flags come out in the order the rule gives: runway, clinics, largest customer, gross margin, retention ([FRAMEWORKS.md](FRAMEWORKS.md), "Top green and red flags", worked example).
- The video-against-deck flag is found here.
- Deleting one scan's output file leaves a gap in the readout and no crash.

**Who:** captain.

**Hours:** 1.5 (11:30 AM to 12:30 PM, and 1:30 to 2:00 PM).

**Judgment:** yes.

### readout-page

The web page the judges see. The feasibility research calls the readout "the thing shown on screen".

**Waits on:** skeleton (the generated types and the server routes, written this week). From 10:30 it is built against the example files.

**Includes:**

- A React page in `readout/` that reads `readout.json` through the server.
- The best green flags and the worst red flags at the very top, green first, each line one click from its piece. A green flag gets the same size and the same source links as a red one.
- The overview under them: one row per piece, in a fixed order, with its mark, its one-line reason and its counts of corroborating and contradicting sources. Strong and weak rows look the same size. This is the demo's first screen ([The one workflow we demo](#the-one-workflow-we-demo)).
- One click on a piece opens its drill-down: its claims, with each conflict shown side by side. Inside traction and revenue, the four ARR figures sit in large type, each with its source chip. The comps panel sits in comps, the signals panel in market, and the video moments in the pitch itself.
- A footnote on every sentence. It opens the source as an in-page panel: a pre-rendered PNG of the slide or page, a small HTML table with the cited cell highlighted, the clause text, or the video at its second through the media fragment (`#t=35`). URL sources open their saved copy from `cache/`. A click never launches Excel or a PDF viewer: a spreadsheet app opening on a projector is slow, and it shows the associate the room's tidy rows ([critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md), finding 6). The panel also lists every other source that corroborates or contradicts the claim, each one click away.
- The video player beside the video claims; clicking a claim jumps to its start.
- A "could not verify" box, a gaps panel, and the score lines for this room, the sealed variant room and the clean room.
- A switch between the seed drop and the full room.
- Served from localhost, with no fonts or scripts from a CDN, so it needs no venue wifi.

**Done when:**

- The page renders `sample_out/` at 11:00 AM and the real outputs at 1:00 PM.
- A missing scan shows its gap panel, not a blank page or an error.
- Every footnote opens its source in the page.
- One click opens a piece's claims, and one more opens a claim's source with its corroborating and contradicting sources.

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

### redflag-readings

The model readings that explain two red flags: the pilot contract's clauses and the note on the cohort tab. They moved out of the red-flag engine so that slice stays scripts only ([critique_buildability.md](../features/20261022.01_hackathon_plan/critique_buildability.md), finding 2).

**Waits on:** redflag-engine (the flags these readings explain), pitch-video (backend-and-data starts this after the video slice), readers.

**Includes:**

- The model reads `pilot_agreement_marlow.pdf` (term, termination, no duty to convert) and the cohort note, with the prompts in [FRAMEWORKS.md](FRAMEWORKS.md) entries 1.2 and 1.3, one schema per request.
- Each reading is a Claim that cites the flag it explains. It never decides a number is wrong; the engine's script already did.
- `python -m scans.readings <room>` writes `out/<room>/readings.json`.

**Done when:** the pilot flag carries the clause quotes, and every quote passes the checker. On the demo laptop the readings show as frozen output.

**Who:** backend-and-data.

**Hours:** 1.0 (2:30 to 3:30 PM). First in the cut order, with the memo's model pass. If cut, it moves to after Saturday.

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

Hiring, traffic, reviews, news and pricing for the demo company's real competitors. Fifth in the feasibility research's ranking. On Saturday it is a static panel of this week's cached competitor readings, because live signals cannot show much for a company with no outside footprint ([critique_buildability.md](../features/20261022.01_hackathon_plan/critique_buildability.md), finding 9). Backend-and-data's freed hours go to the readers and the video.

**Waits on:** signals-readings (this week's `cache/signals/signals.json`).

**Includes:**

- The signals panel in the readout page, reading `cache/signals/signals.json` through the server.
- Each reading shows the date it was taken, and each number links to its saved source.

**Done when:** the panel shows at least three competitors on the readout page, and every number's link opens its saved copy.

**Who:** frontend.

**Hours:** 0.25 (inside the 2:30 to 3:30 PM polish hour).

**Judgment:** no.

### demo-freeze

Integration, the score, the freeze and the rehearsal.

**Waits on:** every slice above that has not been cut.

**Includes:**

- The captain merges at the integration points and runs `bin/smoke` on both rooms.
- `eval/score.py` reads the readout and the answer key and prints how many of the 8 planted entries were found and how many of the 3 decoys were wrongly flagged. The score goes on the page as one line, with the real number, even if it is 7 ([critique_demo.md](../features/20261022.01_hackathon_plan/critique_demo.md), finding 7).
- The clean-room run: the readout on the plants-off room from [blind-room](#blind-room). `eval/score.py` prints how many flags it raised.
- The variant run: at the 3:30 PM freeze the outside person sends the sealed key. The readout runs on the variant room, and `eval/score.py` prints the real numbers against that key. Nobody changes a check after the key opens.
- The frozen outputs saved under `demo/frozen/` as the fallback for every step of the script, including the variant and clean runs.
- A `demo-freeze` git tag at 3:30 PM. After it, nothing merges except a fix for a crash found in rehearsal, and only on the captain's call.
- The rehearsal: a three-minute core with a five-minute extension, from the beat sheet in [demo-script](#demo-script). At least two run-throughs, one of them on the backup laptop from the frozen files. The schedule gives 5:30 to 6:00 for every team's demo plus the winner, so the slot is likely three minutes or less (demo critique, finding 1).

**Done when:** the three-minute core on the frozen build fits three minutes, the core plus the extension fits five, and the backup laptop can show every step from saved files.

**Who:** captain. All four rehearse.

**Hours:** 2.0 for the captain (1:00 to 1:30 PM and 2:00 to 3:30 PM), plus 0.75 for all four (3:30 to 4:15 PM).

**Judgment:** n/a.

### A steer on stage (a card, not yet a slice)

Ken's 1:12 PM and 1:15 PM comments let the operator steer the readout: an instruction on a piece rewrites it, or gets more info for it from new sources, with a visible diff ([steering](#steering)). Steering is an after-Saturday slice. One steer on stage (one piece rewritten from one instruction, such as "treat the pilot as non-recurring") is a candidate for Saturday, and the overview page carries it as a card. It has no owner or hours in the table above. If Ken picks it, the card names which slice gives up time, and the run of show changes then.

### The demo laptop

From the buildability critique's finding 11 and the demo critique's "What else goes wrong live":

- **The demo laptop is Ken's:** M2 Max, with ffmpeg, Python 3.13 and Node 20. Backend-and-data's laptop is the backup, on `demo/frozen/`.
- **The live step runs script checks only.** They need no network. Panels that need a model (the memo's connecting sentences, the comp reasons, the red-flag model readings) show frozen output. Nothing on screen calls a model at render time.
- **No venue wifi needed.** The page and the frozen files are served from localhost, with no fonts or scripts from a CDN. Bring a phone hotspot anyway.
- **Display.** Every laptop brings a USB-C to HDMI adapter. Rehearse at 1280 by 720 at 150% zoom.

### Run of show

| Time | captain | frontend | backend-and-data | design-and-finance | Integration point |
|---|---|---|---|---|---|
| 9:00 to 10:00 | Breakfast and team formation. Confirm roles and folders. Ask the organisers about the track change and the board's open questions (TRI-track-fix, TRI-ask-organisers). Ask Akta's people for a coupon. | Clone, install, run the Part 0 checks. | Clone, check whisper.cpp runs on the demo laptop. | Clone, open the data room, read the check list. | Every laptop has the `.env` keys and a USB-C to HDMI adapter. |
| 10:00 to 10:20 | Organisers' intros and demos. Note any sponsor offer. | Listen. | Listen. | Listen. | |
| 10:20 to 10:30 | Read this table aloud. Name the cut order. | Huddle. | Huddle. | Huddle. | |
| 10:30 to 11:30 | claim-result: quote checker, against the readers stub. At 11:00, post the first social post. | readout-page on the example files. | readers. | redflag-engine: pure checks on the CSVs and the model. | |
| 11:30 | Merge the readers and the quote checker. | Pull. | Pull. | Pull. | **1. Readers merged.** If they are late, cut the memo's model pass and the red-flag model readings now. |
| 11:30 to 12:30 | readout: memo. | readout-page. | pitch-video. | redflag-engine: the deck's claims page by regex, and the seed drop. | |
| 12:30 to 1:00 | Lunch at desks. | Lunch. | Lunch. | Lunch. | |
| 1:00 to 1:30 | demo-freeze: merge, first full run on the seed drop. | readout-page on real outputs. | pitch-video. | redflag-engine: the full room. | **2. First end-to-end run.** If the red-flag engine does not find the seed drop's flags, cut the red-flag model readings, and backend-and-data pairs with design-and-finance after the video slice. |
| 1:30 to 2:00 | readout: finish the piece verdicts, the top green and red flags, conflicts and corroborations. | readout-page: in-page source panels. | pitch-video. | redflag-engine: the clean room. | |
| 2:00 to 2:30 | demo-freeze: score script, frozen outputs. | readout-page: source panels and video jump. | pitch-video. | comps. | |
| 2:30 | Run the full room and the clean room, read the score. | | | | **3. Cut call.** Whatever is not producing claims falls back to saved results or is cut, in the cut order. The real inbox-polling forward is built only if the red-flag engine and the readout are done now, by whoever finishes their slice first. |
| 2:30 to 3:30 | demo-freeze. | readout-page polish, and the market-signals panel. | redflag-readings. | comps. | |
| 3:30 | Tag `demo-freeze`. Post the second social post. The outside person sends the variant room's key. | | | | **4. Demo freeze.** |
| 3:30 to 4:15 | Rehearse, presenting: the three-minute core, then the five-minute extension. | Rehearse, driving the laptop. | Rehearse on the backup laptop. | Rehearse, ready for numbers questions. | Two run-throughs. |
| 4:15 to 4:30 | Fresh runs on the variant room and the clean room, close tabs. | Page ready on all rooms. | Backup laptop on the frozen files, including the variant and clean runs. | Answer key scores checked for the full room and the variant room. | |
| 4:30 to 5:30 | Judging: presents. | Drives. | Backup. | Answers questions on the numbers. | |
| 5:30 to 6:00 | Demos and the winner: presents. | Drives. | Backup. | Ready. | |

**Who presents:** the captain. The frontend drives the readout page. Backend-and-data holds the backup laptop with the frozen files. Design-and-finance answers questions on the numbers. For the $150 social content prize, the captain posts at 11:00 and 3:30 only, from this week's drafts ([social-posts](#social-posts)), in the voice of [BRAND.md](BRAND.md).

### Cut order

The feasibility research ranks the scans by demo value: red-flag engine, readout, pitch video, comps, market signals. The cut order is that ranking reversed, with the model passes cut before any scan, because the script's top flags, pieces and verdicts are enough for the demo ([critique_buildability.md](../features/20261022.01_hackathon_plan/critique_buildability.md), notes):

1. **The memo's model pass and the red-flag model readings first.** The readout keeps its script-set top flags, pieces and verdicts. The readings move to after Saturday.
2. **Market signals second.** The panel is already static; if it is not built, it is dropped.
3. **Comps third.** The panel shows the cached comp list without the live ranking, or is dropped.
4. **Pitch video fourth.** The demo plays the captioned clip and shows this week's saved transcript and claims, which the feasibility research already plans as the fallback.

The red-flag engine, the readout and the readout page are never cut; they are the demo. When a slice is cut, its owner pairs with the owner of the slice that is behind, in that owner's folder and branch, so cutting never causes a merge conflict.

---

## After Saturday

These build the product. Each slice is sized for one agent in one sitting. None has hours.

### readout-store

A persistent store of readouts, so a readout outlives one laptop.

**Waits on:** the Saturday slices merged; a host for the product (the guardrails' deploy field is empty until then).

**Includes:** each readout, its sources and the files it read, stored per fund; a delete that removes all of them; a list of everything held for one company. This is the data rule from the brief: nothing is stored beyond the readout and its sources, and the investor can see and delete everything pulled.

**Who:** agent.

**Judgment:** yes.

### steering

The operator steers the readout: a comment or short instruction on a piece makes Tricorder rewrite that piece, or get more info for it from new sources ([writers' brief, 1:12 PM block](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)).

**Waits on:** readout-store, so a revision outlives the session.

**Includes:** the shape in [ARCHITECTURE.md](ARCHITECTURE.md), "Steering the readout". An instruction box on every piece, for either kind of steer. A rewrite reruns the scans that feed the piece on its inputs, with the instruction passed to their model readings. A request for more info first fetches or opens the new sources it names (the full room instead of the seed drop, another filing, a competitor's pages), under the same data and terms rules as any input, then runs the piece's scans with them; the new claims are marked new. The memo rebuilds the piece and the top green and red flags by the same script rules. The new piece replaces the old one with a visible diff: claims added and dropped, wording changed, and the verdict before and after with the claims that moved it. Every revision is kept.

**Done when:**

- On Hollis Voice, "treat the pilot as non-recurring" on traction and revenue rewrites that piece, and the diff shows what changed.
- On the Hollis Voice seed drop, "read the full room" on retention adds the claims from the second tier, marked new, and the diff names the claim that moved the verdict.
- An instruction that asks for a different script number leaves the number as the script computed it, and the revision says so.
- Every rewritten claim still passes the quote checker.

**Who:** agent.

**Judgment:** yes.

### inbox-forward

The first inbox input: a forwarding address such as deals@ through a mail-receiving service.

**Waits on:** readout-store; a domain and a mail-receiving service, which Ken picks.

**Includes:** the design in [ARCHITECTURE.md](ARCHITECTURE.md), "The inbox input". PDF attachments go into a new company folder. DocSend, Google Drive, Dropbox and Notion links are fetched only when they open without a sign-in; otherwise the readout records a gap that says what the investor must do. It needs no OAuth review, which is why the brief recommends it first.

**Who:** agent.

**Judgment:** yes.

### inbound-unasked

Diligence that starts on the inbound, before the investor asks.

**Waits on:** inbox-forward.

**Includes:** the scans run when a deck arrives; the readout is one click away from the email, or the readout link is the reply. This is the brief's "before you even ask" moment.

**Who:** agent.

**Judgment:** yes.

### inbox-apis

Gmail and Outlook connected through their official APIs.

**Waits on:** inbound-unasked; a pilot fund that asks for it; Google's verification for a restricted scope, including the security assessment (ARCHITECTURE.md, "The inbox input").

**Includes:** read-only access, decks only, under the same data rule.

**Who:** agent, with Ken for Google's verification.

**Judgment:** yes.

### frameworks-scan

The business frameworks: lean canvas, jobs to be done and the rest in [FRAMEWORKS.md](FRAMEWORKS.md), one prompt and one schema each.

**Waits on:** the Saturday slices merged.

**Includes:** a box that the room cannot support shows "not in the data room" (feasibility 1.4).

**Who:** agent.

**Judgment:** no.

### founder-profiles

A card per founder from GitHub, personal sites and talks. LinkedIn is never scraped.

**Waits on:** Ken reads GitHub's terms on persona accounts before any demo account is made (feasibility open point).

**Includes:** the GitHub user and repo data, and a founder-market fit note scored against the rubric in FRAMEWORKS.md. Each line linked to its source.

**Who:** agent.

**Judgment:** yes.

### online-presence

The company's footprint: web, Hacker News, Product Hunt, app stores, Reddit, Facebook.

**Waits on:** founder-profiles; someone reads Reddit's rules (the feasibility research did not); a decision on Product Hunt, whose API terms say non-commercial use.

**Includes:**

- Hacker News through Algolia and the Apple lookup, as in the feasibility research's 1.6.
- The Reddit mini-browser Ken described: a small browser pane in which Ken, signed in as himself, clicks Reddit links, and each page he opens is saved as JSON into the corpus. Agents never fetch reddit.com; the scan reads only what Ken saved.
- Facebook page text pasted by Ken.

**Who:** agent.

**Judgment:** yes.

### comps-deep

Comps from Form D and EDGAR in depth.

**Waits on:** the Saturday comps slice merged.

**Includes:** every Form D quarter, ranking by the selection rules; EDGAR full-text search for business descriptions (the JSON endpoint is undocumented, so the scan falls back to cached results when it breaks, per feasibility Part 2); XBRL frames for public revenue. Crunchbase only with an arrangement for apps, per the landscape research.

**Who:** agent.

**Judgment:** yes.

### pilot

One fund uses Tricorder on real inbound deals.

**Waits on:** interviews, readout-store, inbox-forward, and the data rule written into the product brief.

**Includes:** one fund's associate forwarding real decks for a set period; what they flagged, what they ignored, and whether the partner trusted the first pass.

**Who:** Ken.

**Judgment:** n/a.

### product

What makes Tricorder a product: the fund buys, the associate uses.

**Waits on:** pilot; the overview page's cards on what Tricorder is after Saturday and on the name (the trademark note in [BRAND.md](BRAND.md)).

**Includes:** pricing to the fund, not the associate. The voice-of-the-customer research found the associate is the user and the partner is the buyer, that funds already pay for data-room-to-memo tools, and only two angels' worth of evidence on what angels pay for ([research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md), personas). The [product brief](PRODUCT_BRIEF.md) carries the recommendation.

**Who:** Ken.

**Judgment:** n/a.
