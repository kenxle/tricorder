# Roadmap

## Charter

**What belongs:** What comes next and in what order, grouped by horizon: this week, Saturday, after Saturday. What each slice waits on. For Saturday, who builds each slice and its hour budget, and the run of show.

**What does not:** Dates promised to anyone. Work in flight; that lives on the board. How a slice works inside; that goes in its feature folder and in [ARCHITECTURE.md](ARCHITECTURE.md).

**Level of detail:** One slice per heading, with short lists. A builder can pick up a slice and know what done looks like.

**Sources:** The writers' brief ([00_brief_for_writers.md](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), every "Added" block through 2026-10-22 at 11:20 AM), the organisers' tracks ([problem_tracks.txt](../reports/20261022.01_hackathon_sources/problem_tracks.txt)), the feasibility research ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), the main source for scan order, stack, folder owners and keys), the data room research ([research_data_room.md](../reports/20261022.02_research/research_data_room.md)), the landscape research ([research_landscape.md](../reports/20261022.02_research/research_landscape.md)), the voice-of-the-customer research ([research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md)), the guardrails ([guardrails.md](../../.claude/guardrails.md)) and the board ([BULLETIN.md](../BULLETIN.md)). The shape is copied from My Text Reminders' [ROADMAP.md](../../../my-text-reminders/docs/ongoing/ROADMAP.md). Hour budgets come from [the schedule](../features/20261022.01_hackathon_plan/00_brief_for_writers.md) and were added up by a script, not by hand.

## How to read a slice

- **Waits on** names the slices or board rows that must be done first. Board rows are on [BULLETIN.md](../BULLETIN.md).
- **Includes** is the list of what the slice must contain. The reviewer checks the work against it.
- **Done when** is the list of checks that prove it works.
- **Who** names a role: captain, frontend, backend-and-data, design-and-finance, "agent" for this week's non-code work, or "Ken" for things only Ken can do. The board names the people behind each role.
- **Hours** appears on Saturday slices only. It is a budget inside the six-hour hacking window, not a prediction. When a slice uses up its budget, the captain decides whether it ships as it is, falls back to saved results, or is cut.
- **Judgment** picks the builder's model when an agent builds or rebuilds the slice after Saturday. Yes means Opus, because the slice needs design or product calls. No means Sonnet. Ken-only slices say "n/a".

A slice is done when its pull request is merged to `main`. On Saturday the captain merges, and a red CI blocks a merge even in the room ([guardrails.md](../../.claude/guardrails.md)).

## The one workflow we demo

**Recommended: "forward the pitch email, get the readout" as the opening, with the data room as the body.** The demo opens on a pitch email from the Hollis Voice founder, deck attached. The captain says the investor forwards it to Tricorder and the readout is already waiting: the scans ran on the inbound before anyone asked. That readout is the seed-drop run (the thin first tier of the room). The forwarding address itself is an after-Saturday slice ([inbox-forward](#inbox-forward)), so on stage the captain says in one sentence that today the forward is started by hand. Then the body of the demo is the data room: point Tricorder at the full room, watch the three flags only the full room can show appear, and let the video line land last, as the [data room research](../reports/20261022.02_research/research_data_room.md) lays out in Part 3.7. The demo closes on the score against the answer key. Why this form: it is the "before you even ask" moment from the brief's 11:20 AM block, and the voice-of-the-customer research found the slow part of diligence is gathering and checking, not writing ([research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md), question 3).

**The other form: the data room upload only.** The demo starts with the upload and runs the same body. It shows nothing that is not built. It loses the opening moment and the answer to "when does this run?".

The demo critic weighs the two forms, and the overview page carries a card. The Saturday slices are the same for both forms: the only extra in the recommended form is one screenshot of the email in the demo script.

---

## This week (no product code)

The organisers say Saturday is build-only and everything before code happens this week ([brief, 10:18 AM block](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). So this horizon holds research, people work, data and documents. The one script in it is the data room generator: the organisers say to bring a synthetic data room, so making it is allowed and expected. It lives in `data_room/` and no product folder imports it.

### data-room

The synthetic Hollis Voice data room, its generator and its answer key, built to the [data room research](../reports/20261022.02_research/research_data_room.md), Part 3.

**Waits on:** nothing. It builds to the research's recommended company (Hollis Voice, an AI phone agent for independent vet clinics). If Ken picks another company on the overview page, the generator takes a different config. Ken's yes or no on installing `xlsxwriter` decides whether model formulas carry stored values; without it the generator writes plain values (research Part 3.6).

**Includes:**

- The layout from research Part 3.6 at the repo root: `data_room/generate.py`, `src/` (facts, plants, tables, workbook, pdfs, names, answer key), `tests/`, `out/hollis_series_a/` (the full room) and `out/hollis_seed_drop/` (the thin first tier).
- The 16 files in research Part 3.3, every one generated from one seeded simulation (seed 20261024).
- The 8 planted entries (7 flags plus the video variant) and the 3 clean decoys in research Part 3.4.
- `answer_key/planted_flags.json` outside `out/`, so Tricorder is never pointed at it. Each entry's `check` field uses the check names written in the [saturday-specs](#saturday-specs) slice, so Saturday's test can match a readout flag to a key entry.
- A `claims.json` sidecar next to the deck with the deck's claims as data, the fallback the feasibility research recommends when PDF reading fails ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), 1.1 and 1.9).
- The footer "Synthetic data room for Deal Flow NYC 2026. Not a real company." on every page and sheet. Invented names only; emails on `example.com`.
- A fresh web search for the company name before it appears anywhere public (research open point).

**Done when:**

- `python3 data_room/generate.py` writes both rooms and the answer key from a clean checkout.
- The three tests in research Part 3.6 pass: with plants off, the reference checks find nothing; with plants on, each finds its flag and none finds a decoy; the same seed gives the same CSV and PDF bytes and the same workbook cell values.
- The reference checks stay inside `data_room/tests/`. Saturday's red-flag engine is written fresh in the room and does not copy them.

**Who:** agent. Ken reviews the deck and the video script.

**Judgment:** yes.

### record-pitch-video

Ken records the founder's two-minute pitch on his phone from the script in the data room.

**Waits on:** data-room (the script is written after the deck's claims page exists, research Part 3.6, step 7).

**Includes:**

- The recording from `01_overview/pitch_video_script.md`, with the planted line at about 0:35 saying about three million dollars in ARR, against the deck's $2,500,000 (research Part 3.4, PF2b).
- The video file copied into both rooms beside the script.
- A transcript made once by hand with whisper.cpp on the demo laptop and saved next to the video, so the demo has a result if the live run fails ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), 1.5).

**Done when:** the video plays on the demo laptop, and the saved transcript contains the ARR sentence with its timestamp.

**Who:** Ken. The founder is invented, so the video uses no real person's likeness without consent (feasibility 1.5).

**Judgment:** n/a.

### interviews

Two or three short diligence interviews with associates, principals or angels Ken knows, using the organisers' three questions.

**Waits on:** nothing. This is the board row TRI-interviews (run two or three diligence interviews before Saturday).

**Includes:** each answer in `docs/reports/20261022.02_research/interviews.md`, one section per person, role only. The voice-of-the-customer research found no public number for how long a first-pass memo takes, and no regret story about hidden churn; ask both directly.

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
- Everything under `cache/` at the repo root, with the date each file was read.

**Done when:** each file opens, and a short `cache/README.md` lists what each file is and where it came from.

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
- The memo ordering prompt: conflicts first, then flags by severity, then the other scans.
- One hand-written example result file per Saturday scan, in the Claim schema, so the readout page can be built from 10:30 before any scan runs.
- A static mock of the readout layout that Ken can edit (feasibility 1.8).

**Done when:** each Saturday slice below names the spec entry it types in, and each example file validates against the Claim schema by eye and by the frameworks writer's check.

**Who:** agent. Ken reviews.

**Judgment:** yes.

### founder-brief

The one-page founder brief the organisers ask for: problem, customer, business model, and the one workflow we demo.

**Waits on:** the product brief ([PRODUCT_BRIEF.md](PRODUCT_BRIEF.md)), the landscape research, and the workflow section above.

**Includes:** the organisers' four headings and nothing more, in [founder_brief.md](../features/20261022.01_hackathon_plan/founder_brief.md). The founder-brief writer drafts it.

**Done when:** Ken has edited it in his own words. It is the thing he hands the judges.

**Who:** agent, then Ken.

**Judgment:** yes.

### demo-script

The five-minute demo script and Saturday's run of show, written for the captain to present. Five minutes is the length the demo critic checks against ([brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)).

**Waits on:** data-room, record-pitch-video, and the overview page's card on the demo workflow.

**Includes:**

- Both demo forms from the workflow section, with the recommended one first.
- Who says what and who drives the laptop.
- The fallback for each step: which saved file to show if a scan fails on stage.
- Answers ready for the questions the landscape research expects from this panel: where the data goes, what happens when a scan fails, what is hard to copy ([research_landscape.md](../reports/20261022.02_research/research_landscape.md), Part 3).
- The run of show below, checked against the day's real schedule once the organisers answer the board row TRI-ask-organisers (who Roundtable is, the build window and more).

**Done when:** Ken has read it aloud once against a timer.

**Who:** agent, then Ken.

**Judgment:** yes.

### skeleton-card

A decision card for the overview page: does an empty repo skeleton count as code?

**Waits on:** nothing. The critics weigh it ([brief, 10:18 AM block](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)).

**The two options:**

- **A. The skeleton is code. Build it on Saturday.** The folder layout, the CI command and the typed Claim result are the first Saturday slices ([skeleton](#skeleton) and [claim-result](#claim-result)). They take the first half hour of two people. Before Saturday the repo holds only documents, `data_room/` and `cache/`. To a judge who asks what was built today, the answer is every line of product code. This roadmap is written to option A.
- **B. The skeleton is setup. An agent writes it this week.** Empty folders and packages, `bin/ci`, the CI config, the dependency list, `.env.example`, and the Claim schema typed in from ARCHITECTURE.md, with no scan logic. The captain and backend-and-data each get half an hour back on Saturday, and that time goes first to slices that were cut. The risk: the organisers wrote "On Saturday you only build" and "Everything a founder does before writing code happens this week", and commits dated before Saturday are visible to anyone who looks.

**Who:** agent writes the card. Ken decides.

**Judgment:** n/a.

---

## Saturday

### The window

The schedule gives 10:30 AM to 4:30 PM for hacking, with lunch, so the plan uses six hours. The Luma page also says "9 hours of focused building" ([research_landscape.md](../reports/20261022.02_research/research_landscape.md), summary). That gap is three hours, by the budget script. The board row TRI-ask-organisers asks which is right. If the room opens for longer, the extra time goes to bringing back cut slices in the reverse of the cut order. The freeze still sits one hour before judging.

### Who owns what

Each person owns folders, so pull requests do not touch the same files. This follows the feasibility research's Part 4.1, with market signals given to backend-and-data. The full layout is in [ARCHITECTURE.md](ARCHITECTURE.md).

| Role | Folders | Slices | Build hours |
|---|---|---|---|
| captain | `schema/`, `prompts/`, `scans/memo/`, `eval/`, `demo/` | claim-result, readout, demo-freeze | 4.5 |
| frontend | `readout/` | readout-page | 4.5 |
| backend-and-data | repo root files, `server/`, `scans/video/`, `scans/signals/` | skeleton, pitch-video, market-signals | 4.5 |
| design-and-finance | `scans/redflags/`, `scans/comps/` | redflag-engine, comps | 4.5 |

Build hours run from 10:30 AM to the 3:30 PM freeze, less a half-hour lunch: 4.5 hours each, 18 person-hours in all, from the budget script. Rehearsal adds 45 minutes for all four.

`schema/` is frozen at 11:00 AM. After that, only the captain changes it, and only to fix a bug. A new Python dependency after 11:00 goes through the captain, because the dependency list sits in a root file.

### skeleton

The empty repo the four people build in.

**Waits on:** the skeleton-card decision. Under option B this slice moves to this week and takes no Saturday hours.

**Includes:**

- The folder layout in [ARCHITECTURE.md](ARCHITECTURE.md), with a code-owners file mapping each folder to its role.
- One root dependency file listing everything known this week: the Anthropic SDK, Pydantic, FastAPI, the server runner, pdfplumber, openpyxl, pandas and an HTTP client.
- The FastAPI app in `server/` with the three routes the feasibility research names (list scans, run a scan, serve a result file) and a health route.
- `bin/ci`, which runs the Python tests and the readout page's type check and build, and the same command in the hosted CI.
- `bin/smoke <room>`, which runs every scan that exists, then the memo, and prints which scans ran and which are missing.
- `.env.example` with every variable in ARCHITECTURE.md, and `out/` ignored by git while `sample_out/` is kept.
- The guardrails fields marked "Set by the first code slice" filled in: CI command, health check, smoke command ([guardrails.md](../../.claude/guardrails.md)).

**Done when:** `bin/ci` exits 0 on a fresh clone, the health route answers, and `bin/smoke data_room/out/hollis_seed_drop` prints "no scans yet" without a crash.

**Who:** backend-and-data.

**Hours:** 0.5 (10:30 to 11:00 AM).

**Judgment:** no.

### claim-result

The typed Claim result every scan returns, and the script that checks every quote against its source.

**Waits on:** saturday-specs (the schema text and examples), skeleton for the folders. The captain types the schema while the skeleton is built, so both finish at 11:00.

**Includes:**

- `schema/claim.py`: the Pydantic models from [ARCHITECTURE.md](ARCHITECTURE.md) (ScanResult, Claim, Source, Gap), with "at least one source" enforced by the model.
- `schema/claim.schema.json` exported from it, and TypeScript types generated into `schema/ts/` for the readout page to import.
- `schema/check_quotes.py`: opens each claim's source at its locator and confirms the quote is there. A claim that fails gets the confidence label `unverified` and moves to the "could not verify" box.
- The hand-written example files from saturday-specs copied into `sample_out/`.

**Done when:**

- The schema is frozen and merged at 11:00 AM.
- Tests show a real quote passing, an invented quote failing, and a claim with no source refused.
- Every example file in `sample_out/` validates.

**Who:** captain.

**Hours:** 1.0 (10:30 to 11:30 AM: schema by 11:00, quote checker by 11:30).

**Judgment:** yes.

### redflag-engine

The red flags in the financials and metrics: the organisers' first direction, and first in the feasibility research's ranking.

**Waits on:** claim-result (the schema at 11:00), data-room, saturday-specs (the check list and the deck prompt). The pure checks that compute numbers start at 10:30, before the schema is frozen.

**Includes:**

- One check per planted flag in the data room research's Part 3.4: pilot booked as ARR, deck ARR against the model (1 percent tolerance), churn hidden in the cohort tab, burn against the hiring plan, customer concentration, gross margin without delivery costs, cumulative sign-ups shown as active clinics. The video-against-deck variant is found by the readout slice, because it needs the video scan's output.
- Deck claims read from the PDF with pdfplumber and the deck prompt, with the `claims.json` sidecar as the fallback (feasibility 1.1 and 1.9).
- The model reads text and explains; the script decides that a number is wrong (feasibility Part 3.2).
- Each flag is a Claim with the claimed number, the computed number, a severity, and sources pointing at both places.
- `python -m scans.redflags <room>` writes `out/<room>/redflags.json`.
- A test in `scans/redflags/tests/` that compares the output to the answer key by check name.

**Done when:**

- On the seed drop, the test finds the four flags the research says the seed drop can show from this scan: deck ARR against the model, burn against the hiring plan, gross margin, and the clinic count.
- On the full room it also finds the pilot as ARR, the cohort churn and the customer concentration.
- None of the three decoys (the onboarding fee, the annual prepay, the clean cap table) is flagged.
- Every claim passes the quote checker.

**Who:** design-and-finance.

**Hours:** 3.0 (10:30 AM to 2:00 PM, less lunch).

**Judgment:** yes.

### readout

The first-draft memo assembled from the scans' claims: conflicts first, every sentence sourced. Second in the feasibility research's ranking.

**Waits on:** claim-result. It is built against `sample_out/` until the real scans land at the 1:00 PM integration point.

**Includes:**

- `scans/memo/` reads every `out/<room>/*.json` that exists, runs the quote checker again, and links claims that disagree (same label, unit and period, values apart by more than the tolerance).
- Orders the readout: conflicts first, then flags by severity, then video, comps and signals.
- One model pass that writes connecting sentences. Each sentence must cite claim ids; a sentence with none is dropped.
- A missing scan becomes a gap in the readout, not an error.
- Writes `out/<room>/readout.json`.

**Done when:**

- The four ARR figures in the data room research's Part 3.4 (the model's $2,240,868, the deck's $2,500,000, the video's spoken figure of about $3,000,000, and the recurring ARR the scan computes) show as one conflict at the top.
- The video-against-deck flag is found here.
- Deleting one scan's output file leaves a gap in the readout and no crash.

**Who:** captain.

**Hours:** 1.5 (11:30 AM to 12:30 PM, and 1:30 to 2:00 PM).

**Judgment:** yes.

### readout-page

The web page the judges see. The feasibility research calls the readout "the thing shown on screen".

**Waits on:** claim-result (the generated types at 11:00), skeleton (the server routes). From 10:30 it is built against the example files.

**Includes:**

- A React page in `readout/` that reads `readout.json` through the server.
- Conflicts at the top, then flags by severity, then panels for the video, comps and signals.
- A footnote on every sentence. It opens the source: the PDF page, the spreadsheet cell with its quote, the URL, or the video at its second through the media fragment (`#t=35`).
- The video player beside the video claims; clicking a claim jumps to its start.
- A "could not verify" box, a gaps panel, and the score against the answer key.
- A switch between the seed drop and the full room.

**Done when:**

- The page renders `sample_out/` at 11:00 AM and the real outputs at 1:00 PM.
- A missing scan shows its gap panel, not a blank page or an error.
- Every footnote opens its source.

**Who:** frontend.

**Hours:** 4.5 (10:30 AM to 3:30 PM, less lunch).

**Judgment:** yes.

### pitch-video

The pitch video broken into claims with timestamps, third in the feasibility research's ranking.

**Waits on:** claim-result, record-pitch-video, keys (whisper.cpp on the demo laptop).

**Includes:**

- ffmpeg makes a 16 kHz mono WAV; whisper.cpp transcribes it with timestamps (feasibility 1.5).
- The video prompt returns claims with the segment ids they came from, so start and end seconds are copied from the transcript, not guessed.
- Keyframes at scene changes for thumbnails, if the budget allows.
- `python -m scans.video <room>` writes `out/<room>/video.json`. If the live run fails, the scan reads this week's saved transcript and says so in the result.

**Done when:** `video.json` holds the ARR claim from the planted line, its time range covers the spoken sentence, and its quote passes the checker.

**Who:** backend-and-data.

**Hours:** 2.5 (11:00 AM to 2:00 PM, less lunch).

**Judgment:** no.

### comps

Comparable companies and recent rounds, each with the reason it is a fair comp. Fourth in the feasibility research's ranking.

**Waits on:** claim-result, cached-data, saturday-specs (the selection rules, prompt and schema).

**Includes:**

- 5 to 8 comps in two groups: recent private rounds from the cached Form D files, and public companies from the cached XBRL facts (feasibility 1.2).
- The selection rules from FRAMEWORKS.md applied by script. The model writes only the "why this is a fair comp" sentence.
- Each comp's number carries its source: the filing or the Form D row.
- Reads `cache/` only on Saturday, so EDGAR being slow changes nothing on screen.
- `python -m scans.comps <room>` writes `out/<room>/comps.json`.

**Done when:** the table has at least five comps, each with a reason and a source that passes the checker.

**Who:** design-and-finance.

**Hours:** 1.5 (2:00 to 3:30 PM).

**Judgment:** yes.

### market-signals

Hiring, traffic, reviews, news and pricing for the demo company's real competitors. Fifth in the feasibility research's ranking.

**Waits on:** claim-result, cached-data.

**Includes:**

- A short grid per competitor from the cached Akta pulls and Tavily pricing pages, each number linked to its source (feasibility 1.3).
- For Hollis Voice itself, only what the room gives: website copy and pricing.
- If Akta's paid signals were not available, the grid shows news and company data only, and the gap says why.
- `python -m scans.signals <room>` writes `out/<room>/signals.json`.

**Done when:** the grid covers at least three competitors, and every number passes the checker.

**Who:** backend-and-data.

**Hours:** 1.5 (2:00 to 3:30 PM).

**Judgment:** no.

### demo-freeze

Integration, the score, the freeze and the rehearsal.

**Waits on:** every slice above that has not been cut.

**Includes:**

- The captain merges at the integration points and runs `bin/smoke` on both rooms.
- `eval/score.py` reads the readout and the answer key and prints how many of the 8 planted entries were found and how many of the 3 decoys were wrongly flagged. The score goes on the page.
- The frozen outputs saved under `demo/frozen/` as the fallback for every step of the script.
- A `demo-freeze` git tag at 3:30 PM. After it, nothing merges except a fix for a crash found in rehearsal, and only on the captain's call.
- The rehearsal: at least two run-throughs of the demo script, one of them on the backup laptop from the frozen files.

**Done when:** a full run of the demo script on the frozen build fits five minutes, and the backup laptop can show every step from saved files.

**Who:** captain. All four rehearse.

**Hours:** 2.0 for the captain (1:00 to 1:30 PM and 2:00 to 3:30 PM), plus 0.75 for all four (3:30 to 4:15 PM).

**Judgment:** n/a.

### Run of show

| Time | captain | frontend | backend-and-data | design-and-finance | Integration point |
|---|---|---|---|---|---|
| 9:00 to 10:00 | Breakfast and team formation. Confirm roles and folders. Ask the organisers about the track change and the board's open questions (TRI-track-fix, TRI-ask-organisers). Ask Akta's people for a coupon. | Clone, install, run the Part 0 checks. | Clone, check whisper.cpp runs on the demo laptop. | Clone, open the data room, read the check list. | Every laptop has the `.env` keys. |
| 10:00 to 10:20 | Organisers' intros and demos. Note any sponsor offer. | Listen. | Listen. | Listen. | |
| 10:20 to 10:30 | Read this table aloud. Name the cut order. | Huddle. | Huddle. | Huddle. | |
| 10:30 to 11:00 | claim-result: type in the schema. | readout-page on the example files. | skeleton. | redflag-engine: pure checks on the CSVs. | |
| 11:00 | Freeze the schema, merge the skeleton. | Pull. | Pull. | Pull. | **1. Schema frozen.** If it is late, cut market signals now. |
| 11:00 to 12:30 | claim-result: quote checker (to 11:30). readout: memo (from 11:30). | readout-page. | pitch-video. | redflag-engine: deck claims and the seed drop. | |
| 12:30 to 1:00 | Lunch at desks. | Lunch. | Lunch. | Lunch. | |
| 1:00 to 1:30 | demo-freeze: merge, first full run on the seed drop. | readout-page on real outputs. | pitch-video. | redflag-engine: the full room. | **2. First end-to-end run.** If the red-flag engine does not find the seed drop's flags, cut market signals and backend-and-data pairs with design-and-finance. |
| 1:30 to 2:00 | readout: finish ordering and conflicts. | readout-page. | pitch-video. | redflag-engine. | |
| 2:00 to 2:30 | demo-freeze: score script, frozen outputs. | readout-page: footnotes and video jump. | market-signals. | comps. | |
| 2:30 | Run both rooms, read the score. | | | | **3. Cut call.** Whatever is not producing claims falls back to saved results or is cut, in the cut order. |
| 2:30 to 3:30 | demo-freeze. | readout-page polish. | market-signals. | comps. | |
| 3:30 | Tag `demo-freeze`. | | | | **4. Demo freeze.** |
| 3:30 to 4:15 | Rehearse, presenting. | Rehearse, driving the laptop. | Rehearse on the backup laptop. | Rehearse, ready for numbers questions. | Two run-throughs. |
| 4:15 to 4:30 | Fresh run, close tabs. | Page ready on both rooms. | Backup laptop on the frozen files. | Answer key score checked. | |
| 4:30 to 5:30 | Judging: presents. | Drives. | Backup. | Answers questions on the numbers. | |
| 5:30 to 6:00 | Demos and the winner: presents. | Drives. | Backup. | Ready. | |

**Who presents:** the captain. The frontend drives the readout page. Backend-and-data holds the backup laptop with the frozen files. Design-and-finance answers questions on the numbers. For the $150 social content prize, the captain posts at each integration point in the voice of [BRAND.md](BRAND.md).

### Cut order

The feasibility research ranks the scans by demo value: red-flag engine, readout, pitch video, comps, market signals. The cut order is that ranking reversed:

1. **Market signals first.** The panel shows the saved competitor files as one screen, or the panel is dropped.
2. **Comps second.** The panel shows the cached comp list without the live ranking, or is dropped.
3. **Pitch video third.** The demo plays the video and shows this week's saved transcript and claims, which the feasibility research already plans as the fallback.

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

**Includes:** pricing to the fund, not the associate. The voice-of-the-customer research found the associate is the user and the partner is the buyer, that funds already pay for data-room-to-memo tools, and that angels pay to avoid diligence rather than to do it ([research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md), personas). The [product brief](PRODUCT_BRIEF.md) carries the recommendation.

**Who:** Ken.

**Judgment:** n/a.
