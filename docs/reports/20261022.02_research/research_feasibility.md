# Feasibility per scan, the data sources, the data room and the stack

Written 2026-10-22 by the feasibility researcher (R3) for the Tricorder hackathon plan. Pages I relied on are saved under [raw/feasibility/](raw/feasibility/INDEX.md). Every rate limit, price and free-tier claim below carries the link I read it on. Counts come from [formd_counts.py](raw/feasibility/formd/formd_counts.py). The data room design itself is R4's job, in [research_data_room.md](research_data_room.md); Part 3 here adds the detection split and the build facts, and keeps R4's file list so the two files agree.

## Summary

- **Scans ranked by demo value for the build effort they ask.** Effort is relative (S, M, L), not a time estimate.
  1. Red-flag engine (S to M). The organisers' first direction, and the one a script can prove.
  2. Readout memo with a source on every claim (M). It is the thing shown on screen.
  3. Pitch video breakdown (M). Most visual; the deck-against-video mismatch is a clean flag.
  4. Comp builder (M). Needs pre-pulled data; EDGAR cannot describe a private company.
  5. Market signal tracker (M). Akta's richest signals need a paid plan; plan on a sponsor key or cached files.
  6. Business-model frameworks (S). One prompt and one schema each. Cheap, but easy for others to copy.
  7. Founder profiles (S to M). Good for the "people" story; public GitHub is the only clean source.
  8. Online presence (M). A synthetic company has no real footprint, so run it on real competitors.
- **Stack: Python scans as plain command-line functions, FastAPI serving their JSON files, and a React page for the readout.** The alternatives are one Streamlit app, or Rails with Python scans called as subprocesses.
- **Every scan returns one typed result: a list of claims, each with at least one source.** Anthropic's citations feature cannot be combined with structured output (the API returns a 400), so each claim carries its own quote and locator, and a script checks that the quote really appears in the source. [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- **Data room: R4's 16 files for "Hollis Voice" (an AI phone agent for vet clinics).** Seven planted flags plus one variant. Every flag ends in a script check with a number and a tolerance; a model is needed first to read the deck, the video transcript and the cohort-tab notes, and to categorise messy ledger lines. See Part 3.
- **Keys Ken must get this week:** Anthropic (required), Tavily (free, no card), You.com (free keyless tier, key for more), a GitHub token, an Akta key (and ask the sponsor about the paid plan), a Product Hunt token (optional). No key: SEC EDGAR (needs a declared User-Agent), HN Algolia, arXiv, Apple. Skip: Crunchbase (sales-gated), X (paid per read), Facebook (app review). Details in Part 5.
- **Two facts that change the plan.** First, Akta's pay-as-you-go plan returns 403 on headcount, web traffic, jobs, reviews and social posts, which is most of the market-signal scan. Second, OpenAI's `whisper-1` is deprecated and shuts down 2027-02-26, and the replacement's docs do not show word or segment timestamps; local whisper.cpp does give them and is already in Homebrew.

---

## Part 0. How I checked

What I ran on this Mac (read-only, no keys, no sign-ups):

| Check | Result |
|---|---|
| `which ffmpeg ffprobe` | Both installed at `/opt/homebrew/bin`, ffmpeg 8.0 |
| ffmpeg scene detection | Made a 5-second test clip with one hard cut; `select='gt(scene,0.4)'` found one cut and wrote one frame |
| `which whisper whisper-cli faster-whisper` | None installed |
| `import whisper`, `import faster_whisper` | Not installed |
| `brew info whisper-cpp` | Exists as `whisper.cpp` 1.9.5, bottled (not installed) |
| Python | 3.13.0; `openpyxl` 3.1.5 and `pandas` 3.0.1 installed; `pdfplumber` and `fitz` (PyMuPDF) not installed; `anthropic` not installed; `uv` 0.10.4 present |
| Node | v20.19.0 |
| Ruby | 3.2.3 |
| EDGAR full-text JSON (`efts.sec.gov/LATEST/search-index`) | Works with no key. [sample](raw/feasibility/efts_sample.json) |
| EDGAR XBRL frames (`data.sec.gov/api/xbrl/frames/us-gaap/Revenues/USD/CY2023.json`) | Works with no key; 2,679 data points in the sample. [sample](raw/feasibility/frames_sample_head.json) |
| EDGAR company facts | Returned HTTP 200 for one CIK (1.25 MB); not saved |
| Form D quarterly zip | Downloaded 2026 Q3 (3.65 MB); read with [formd_counts.py](raw/feasibility/formd/formd_counts.py) |
| Apple lookup and customer-review feed | Both returned JSON with no key. [lookup](raw/feasibility/appstores/itunes_apple_com_lookup_id_284882215_country_us.html), [reviews](raw/feasibility/appstores/rss_reviews_sample.json) |

The other teammates' machines may differ. Each person runs the same checks on their own laptop this week.

I did not fetch reddit.com. I did not run anything that needs a key.

---

## Part 1. The scans

Shared shape for every scan (details in Part 4): a command-line function takes a company folder and writes `out/<company>/<scan>.json`, a list of **claims**. A claim is a statement, a severity or score where it applies, and one or more **sources**. A source is a file with a locator (sheet and cell, page, line), a URL with the date it was read, an API call, or a video with start and end seconds, plus a short quote.

### 1.1 Red-flag engine on financials and metrics

**(a) What four people can get working in the room.**
- **Inputs:** the data room folder: the model (`xlsx`), the metrics and customer CSVs, the hiring plan CSV, the deck as PDF.
- **Output shown in the demo:** a ranked table of flags. Each row: what is wrong, the number the company claims, the number we computed, the severity, and links to both places. Click a link and the deck page or spreadsheet cell opens.
- **How it works:** a Python module of plain checks (recompute ARR from subscription rows, rebuild cohorts, add up payroll from the hiring plan, compare every claim in the deck to its source cell). A model reads the deck text to pull out its claims and turns each failed check into a sentence.
- **What the model does that a script cannot:** read the deck's claims page and the cohort-tab note ("Cohort = customers still active after onboarding"), and decide that the note hides churn.

**(b) Prepare this week, without product code.**
- The synthetic data room itself (R4's generator and answer key are the thing to build; see Part 3).
- A written list of checks, each as a name, the inputs it reads, the formula, the tolerance, and the sentence a human would write. This is a spec, not code.
- The prompt that extracts claims from the deck, and the JSON schema for a claim (the shared one).
- The answer key (`planted.csv`) so the team can tell a hit from a miss.
- A decision on how the deck gets parsed: see 1.9, parsing libraries.

**(c) Data sources and terms.** No external API. Inputs are local files. Libraries and their terms are in 1.9. Claude API terms are in 1.10.

**(d) Biggest risk on the day, and the fallback.**
- **Risk:** the model misreads a messy PDF, or a spreadsheet formula has no stored value (a file written by `openpyxl` has no cached results, so a reader asking for values gets `None`; R4 tested this). The mechanical checks then compare wrong numbers.
- **Fallback:** the generator writes `claims.json` next to the deck, with the same claims as machine-readable data. The scan reads `claims.json` if PDF extraction fails, and the demo says so. The checks run on CSVs and cached values, which do not depend on the PDF.

### 1.2 Comp builder

**(a) In the room.**
- **Inputs:** the company profile (sector, stage, business model) and its ask.
- **Output:** a table of 5 to 8 comparable companies, each with the reason it is a fair comp, one number (round size, revenue, multiple), and a source link. Two groups: recent private rounds (from Form D) and public companies (from EDGAR filings).
- **How it works:** EDGAR full-text search finds public companies whose 10-K text describes a similar business. XBRL frames pull revenue and gross profit for them. The Form D data gives recent private rounds by size, date and industry bucket. A model writes the "why a fair comp" sentence for each.
- **Limit I verified:** Form D carries no business description. Its issuer and offering tables hold name, state, year of incorporation, industry bucket, offering size, amount sold and sale date, with no text about what the company does. [Form D data sets](https://www.sec.gov/data-research/sec-markets-data/form-d-data-sets), fields read from the 2026 Q3 zip. Full-text search for "voice AI" restricted to Form D filings from 2026-09-01 to 2026-10-22 returned 0 hits ([sample](raw/feasibility/efts_formd_sample.json)). So Form D tells you a round happened; another source (web search, Akta) must say what the company does.
- **Scale of the filter:** in the 2026 Q3 file, 15,952 offerings; 1,114 are in the industry group "Other Technology"; 202 technology-type equity offerings were between $5 million and $20 million. Output: [formd_counts_output.txt](raw/feasibility/formd/formd_counts_output.txt). That is too many to eyeball and small enough to rank by script.

**(b) Prepare this week.**
- Download the last four Form D quarterly zips to the team's laptops (each a few MB; 2026 Q3 was 3.65 MB).
- Pre-pull XBRL company facts for a short list of public companies near the demo company's space (say 8 to 12), saved as JSON.
- Write the comp-selection rules as a one-page spec: which fields count, the weights, the exclusion rules. W4's frameworks doc owns the wording.
- Write the "why this is a fair comp" prompt and the comp schema.
- Run the User-Agent test against EDGAR so a blocked header is found before Saturday.

**(c) Sources.** See the table in Part 2: EDGAR full-text search, XBRL frames and company facts, Form D data sets, Akta, Crunchbase.

**(d) Risk and fallback.**
- **Risk:** the synthetic company has no true public comps, so the table looks thin or wrong to a judge.
- **Fallback:** use pre-pulled files for the 8 to 12 public companies and 10 to 20 Form D rounds, chosen by hand this week. The scan "runs live" over cached data. If EDGAR is slow or blocks the User-Agent, nothing changes on screen.

### 1.3 Market signal tracker

**(a) In the room.**
- **Inputs:** the company name and its competitors' names (the competitor list is part of the data room's one-pager).
- **Output:** a short grid per competitor: hiring (open roles), web traffic, reviews, news, with each number linked to its source. For the synthetic company, the only signals available are the ones the data room itself provides (website copy, pricing page).
- **How it works:** Akta's APIs for company data, news, jobs, traffic, reviews, then Tavily or You.com search for pricing pages and news. A model summarizes each competitor into claims.
- **Plan access matters:** Akta's pay-as-you-go plan returns 403 for Job Posts, Social Posts, Product Reviews, Website Traffic, Employee Reviews and Headcount Trends. Those need a Subscription plan. [Akta rate limits](https://docs.akta.pro/getting-started/rate-limits) On pay-as-you-go, News Signals (10,000 a month), Company Data (100 a month) and Company Search (100 a day) work. Per-credit cost is $0.05 pay-as-you-go and $0.04 on Subscription. [Akta credits](https://docs.akta.pro/getting-started/pricing)

**(b) Prepare this week.**
- Sign up at Akta's playground and create a key (the docs say the key is shown once). [Akta overview](https://docs.akta.pro/getting-started/overview)
- Ask the Akta people (community sponsor) whether a hackathon plan with the alternative signals exists. The docs give no free tier and no hackathon plan.
- Choose 3 to 5 real competitors in the demo company's space and pre-pull every Akta signal that the key allows. Save the JSON. Akta's latency for live alternative signals is long at the tail (p99 for Job Posts is 70,005 ms; Social Posts 55,589; Headcount Trends 55,175). [Akta latency](https://docs.akta.pro/getting-started/performance) A live call on stage can stall, so the demo reads the saved files.
- Write the signals schema and the "what changed" prompt.

**(c) Sources.** Akta (REST and MCP), Tavily, You.com, Product Hunt, app stores, HN. See Part 2.

**(d) Risk and fallback.**
- **Risk:** no paid Akta plan on Saturday, or the live call stalls.
- **Fallback:** the pre-pulled competitor files plus Tavily search for pricing pages. If Akta gives nothing, Tavily's free 1,000 credits a month cover search. [Tavily credits](https://docs.tavily.com/documentation/api-credits)

### 1.4 Business-model frameworks (lean canvas, jobs to be done and the rest)

**(a) In the room.**
- **Inputs:** the one-pager, deck text, website copy and product one-pager from the data room.
- **Output:** a lean canvas page (nine boxes) plus a jobs-to-be-done statement, each box a claim with a source quote from the deck or website. Add more frameworks (Porter's five forces, SWOT, TAM/SAM/SOM, unit economics) as extra pages.
- **How it works:** one prompt and one schema per framework, run through Claude with structured output, so the output is valid JSON every time. [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- **Caveat for the demo:** this scan is the easiest to build and the easiest for another team to copy. Its value is in the quote check: a box that says "customer segment: independent vet clinics" shows the deck sentence it came from.

**(b) Prepare this week.** W4's `FRAMEWORKS.md` entries are the prompts and schemas. Pre-write the JSON Schema for each. Run each prompt by hand against the synthetic deck text (in the Claude app, not as product code) and keep the best output as the "expected" file.

**(c) Sources.** Local files and Claude only.

**(d) Risk and fallback.**
- **Risk:** the model invents a box it cannot support from the text.
- **Fallback:** the schema requires a quote for every box; the quote checker drops any claim whose quote is not found in the source. An empty box shown as "not in the data room" is a good demo moment.

### 1.5 Pitch video breakdown (Whisper plus ffmpeg)

**(a) In the room.**
- **Inputs:** one 2-minute pitch video of the founder (Ken records it from the script in the data room, a phone clip is fine).
- **Output:** a timeline page. The video plays; beside it, a list of key claims, each with a start time. Click a claim and the video jumps there. Claims that disagree with the deck (the video says about $3,000,000 ARR; the deck says $2,500,000) are marked red.
- **How it works:**
  1. ffmpeg pulls 16 kHz mono WAV from the video (whisper.cpp reads only 16-bit WAV, per its README). [whisper.cpp README](https://github.com/ggml-org/whisper.cpp)
  2. whisper.cpp transcribes with timestamps; on Apple Silicon it runs on the GPU through Metal. [whisper.cpp README](https://github.com/ggml-org/whisper.cpp)
  3. A model reads the transcript segments and returns claims with the segment ids they came from, so the start and end seconds are copied from the transcript and not guessed.
  4. ffmpeg's `select` filter with a scene threshold grabs a keyframe at each scene change for thumbnails. [ffmpeg filters](https://ffmpeg.org/ffmpeg-filters.html) I tested it on a synthetic clip and it found the cut.
  5. The page uses the standard media fragment (`video.mp4#t=35`) to jump.
- **Local versus API:**
  - Local whisper.cpp: no key, no upload, timestamps built in. Not installed on this Mac yet; Homebrew has it (1.9.5, from my `brew info` check in Part 0).
  - faster-whisper: pip install, CPU int8 path; its README lists CPU and NVIDIA GPU options and no Apple GPU option. [faster-whisper README](https://github.com/SYSTRAN/faster-whisper)
  - OpenAI API: files up to 25 MB; the recommended model is `gpt-transcribe` at $0.0045 a minute. `whisper-1`, `gpt-4o-transcribe`, `gpt-4o-mini-transcribe` and the diarize model are deprecated and shut down 2027-02-26. The docs show word and segment timestamps only for the deprecated `whisper-1`. [OpenAI speech-to-text](https://platform.openai.com/docs/guides/speech-to-text), [OpenAI pricing](https://platform.openai.com/docs/pricing) So the API path works on Saturday through `whisper-1`, but it is the fallback, not the plan.

**(b) Prepare this week.**
- Ken records the video (or any teammate; it is a synthetic founder, so it must not use a real person's likeness without consent). The script already exists in R4's file list.
- Install whisper.cpp on the laptop that will run the scan; download a model file and run it once on a test clip so the first run is not on stage. (Model sizes: read the whisper.cpp README before choosing; I did not copy a number.)
- Write the claims prompt and the claim schema (with `start_s`, `end_s`, `segment_ids`).
- Keep the transcript of the finished video as a saved file, so the demo has a result even if the run fails.

**(c) Sources.** whisper.cpp, faster-whisper, OpenAI API, ffmpeg. Official API: OpenAI only; the others are open-source tools.

**(d) Risk and fallback.**
- **Risk:** first-run model download or a build error on a teammate's machine; a noisy room ruins a live recording.
- **Fallback:** the transcript and the claims JSON from this week's rehearsal. The demo plays the video and shows the saved result; the "live" step is optional.

### 1.6 Online presence (web, Hacker News, Product Hunt, app stores, Reddit, Facebook)

**(a) In the room.**
- **Inputs:** company name, website URL, founder names.
- **Output:** a one-screen "footprint" per company: web, Hacker News mentions, Product Hunt launch, app store rating and review count, Reddit threads Ken saved, Facebook page if any. A missing footprint is a finding too ("no Hacker News mention, no app").
- **For the synthetic company the footprint is empty by design.** Run it on one or two real competitors for the contrast, and say so on screen.
- **Per source, what is official:**
  - Hacker News: official Algolia search API, no key. [HN Algolia API](https://hn.algolia.com/api)
  - Product Hunt: official GraphQL API; needs a token; the docs say it must not be used for commercial purposes. [Product Hunt API](https://api.producthunt.com/v2/docs)
  - Apple App Store: official Search and Lookup API, about 20 calls a minute. [Apple Search API](https://performance-partners.apple.com/search-api) Customer reviews come from a feed I tested but that Apple's page does not document ([sample](raw/feasibility/appstores/rss_reviews_sample.json)); treat it as unofficial.
  - Google Play: the official reviews API only reads reviews for apps you own. [Google Play Developer API](https://developers.google.com/android-publisher/reply-to-reviews) Public listing pages have no official API; use search results or skip.
  - Reddit: agents never fetch it. Ken saves `.json` pages by hand into `docs/reports/20261022.02_research/reddit_corpus/raw/`; the scan reads local files. Reddit's rules were not read.
  - Facebook: reading another Page's posts needs an app with `pages_read_engagement` and `pages_read_user_content`, a role on the Page, or the "Page Public Content Access" feature. [Graph API Page feed](https://developers.facebook.com/docs/graph-api/reference/page/feed/) That is app review, not a Saturday task. Plan: Ken pastes the page text by hand.

**(b) Prepare this week.**
- Pick the 1 to 2 real competitors; run the HN and app-store queries by hand and save the results.
- Ken saves the Reddit `.json` URLs (R1's list) and any Facebook page text.
- Get a Product Hunt token (client-only token is enough for public data). [Product Hunt API](https://api.producthunt.com/v2/docs)
- Write the footprint schema.

**(c) Sources.** See Part 2.

**(d) Risk and fallback.** The risk is a thin, boring screen. Fallback: cut this scan from the live demo, and show it as one slide of saved results. It ranks last for demo value.

### 1.7 Founder profiles (GitHub, personal sites, X, talks; no LinkedIn scraping)

**(a) In the room.**
- **Inputs:** founder names and handles from the bios in the data room.
- **Output:** a card per founder: what they have built (repos), how active, how long on GitHub, their stated company and bio, a "founder-market fit" note from the bio, each line linked to its source.
- **How it works:** GitHub REST for the user and repos; a model reads the README and bio text and rates fit against a fixed rubric (W4 writes the rubric). The GitHub user object carries `login`, `company`, `bio`, `public_repos`, `followers` and `created_at`. [GitHub Users API](https://docs.github.com/en/rest/users/users)
- **What I did not verify:** exactly which contribution-history fields GraphQL gives. Read the GraphQL reference before promising a contribution graph.
- **Not used:** LinkedIn (the organisers' document says its terms prohibit scraping, [problem tracks](../20261022.01_hackathon_sources/problem_tracks.txt)). X is pay-per-read: $0.005 per post read and $0.010 per user read. [X API pricing](https://docs.x.com/x-api/getting-started/pricing) Not worth a key for the demo; link the handle only.

**(b) Prepare this week.**
- Create the demo founders' GitHub presence: public repos with real-looking histories. **Open point:** I did not read GitHub's terms on accounts that are personas. Read them before creating any account; the safe route is a GitHub organisation Ken owns, with repos he commits to. Decide before the data room's bio file is generated.
- Make a GitHub token. REST without a token is 60 requests an hour per IP, and with a token 5,000 an hour. [GitHub REST rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api) The GraphQL docs describe authentication only (personal token, GitHub App or OAuth app) and a limit of 5,000 points an hour per user. [GraphQL rate limits](https://docs.github.com/en/graphql/overview/rate-limits-and-node-limits-for-the-graphql-api) Search endpoints: 30 requests a minute authenticated, 10 unauthenticated. [GitHub search](https://docs.github.com/en/rest/search/search)
- Write the founder card schema and the fit rubric.

**(c) Sources.** GitHub, arXiv (official API, one request every three seconds, one connection at a time; [arXiv terms](https://info.arxiv.org/help/api/tou.html)), personal sites (public pages through search), talks (transcripts through search).

**(d) Risk and fallback.** The risk is a demo founder that looks fake. Fallback: show the scan on a real public founder from the competitor set, with a short note, and keep the synthetic founders to the bios.

### 1.8 The readout (first-draft memo with every claim linked)

**(a) In the room.**
- **Inputs:** the JSON from every other scan.
- **Output:** a single web page. At the top: the red-flag claims that conflict (deck against model, video against deck). Below: market signals, comps, frameworks, founders. Every sentence has a footnote that opens the exact source (file cell, PDF page, URL, video second).
- **How it works:** the memo is assembled from claims already written by the scans, not freely written by the model. A last model pass orders them and writes connecting sentences; the quote checker runs again over the final page and flags any sentence without a source.
- **Why not Anthropic citations:** the citations feature is rejected together with `output_config.format` (HTTP 400), and the PDF path processes each page as image plus text. [Structured outputs, incompatibilities](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support) Our own `source` fields give the same traceability on every scan, including the ones with no document.

**(b) Prepare this week.** The memo layout (a static mock in HTML that Ken can edit in the plan's style), the ordering rules (conflicts first), and the page's JSON contract (the shared claim schema).

**(c) Sources.** The other scans.

**(d) Risk and fallback.** The page needs every scan's JSON. Fallback: a `sample_out/` folder of pre-run JSON for every scan; the page renders whatever files exist, so a missing scan leaves a gap and not a crash.

### 1.9 Parsing PDFs and spreadsheets

| Need | Python | Node | Notes |
|---|---|---|---|
| Text and tables from PDF | `pdfplumber` (MIT; extracts characters, lines, tables) [README](https://github.com/jsvine/pdfplumber), [licence](https://raw.githubusercontent.com/jsvine/pdfplumber/stable/LICENSE.txt) | `pdf.js` [README](https://github.com/mozilla/pdf.js) | Both read text PDFs; neither does scans. |
| Fast PDF text | PyMuPDF; its README shows an AGPL licence badge, so check that before shipping it in a product. [README](https://github.com/pymupdf/PyMuPDF) | n/a | Fine for a hackathon; flag it for after. |
| Read `xlsx` | `openpyxl` (read/write `xlsx`; formulas have no value unless the file stores one) [docs](https://openpyxl.readthedocs.io/en/stable/) | `exceljs` [README](https://github.com/exceljs/exceljs) | Open with `data_only=True` to read cached values, and test that the generator stored them. |
| Send the PDF to Claude directly | n/a | n/a | Base64 PDF in the request: up to 600 pages per request (100 when the context window is under 1M tokens). [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support) |

Recommendation: the generator also writes a sidecar `claims.json` for the deck, so the scan does not depend on PDF layout. Parse the real PDF with `pdfplumber` as the live path and use the sidecar when it fails.

### 1.10 Claude API for typed results

- **Model ids I read** ([Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)): `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`, `claude-fable-5-1`.
- **Prices per million tokens, input / output** ([Pricing](https://platform.claude.com/docs/en/about-claude/pricing)): Opus 5.5 $4 / $20; Sonnet 5.5 $2 / $10; Haiku 5.5 $0.10 / $0.50 for prompts up to 100,000 tokens ($0.50 / $2.50 above).
- **Structured outputs:** pass a JSON schema in `output_config.format`, or pass a Pydantic class to `client.messages.parse(...)` and read `parsed_output`. [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- **Rate limits** depend on the account's tier and are shown in the Console. [Rate limits](https://platform.claude.com/docs/en/api/rate-limits)
- **Choice for the team:** Opus 5.5 for the red-flag reading and the memo pass; Haiku 5.5 for bulk classification (reviews, posts). The skill bundled with Claude Code says Opus 5.5 takes no `temperature`, no `top_p` and no forced `tool_choice`, and cannot turn thinking off. I did not find that on a public docs page, so test one call on Friday and drop any such parameter.
- **Saved:** [raw/feasibility/claude_api/](raw/feasibility/claude_api/INDEX.md).

---

## Part 2. Data sources: access, limits, price, link

"Official" means the owner publishes the API and documents it.

| Source | Official API? | Key? | Rate limit | Price / free tier | Read on |
|---|---|---|---|---|---|
| SEC EDGAR files and data.sec.gov APIs | Yes | No; declare a User-Agent | 10 requests per second | Free | [Accessing EDGAR data](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data) |
| EDGAR User-Agent rule | Yes | No | See above | The SEC's sample header is `Sample Company Name AdminContact@<sample company domain>.com`, plus `Accept-Encoding: gzip, deflate` | Same page |
| EDGAR submissions, company concept, company facts, frames | Yes | No | Same 10 per second; bulk ZIPs rebuilt nightly about 3 a.m. ET; no CORS, so call it from the server | Free | [EDGAR API documentation](https://www.sec.gov/edgar/sec-api-documentation) |
| EDGAR full-text search (web page) | The page and FAQ are official | No | Same 10 per second | Free; covers filings since 2001; boolean `NOT`, `OR`, `NEAR(n)`, quotes, trailing `*` | [Search page](https://www.sec.gov/edgar/search/), [FAQ](https://www.sec.gov/edgar/search/efts-faq.html) |
| EDGAR full-text JSON (`efts.sec.gov/LATEST/search-index?q=`) | **No.** I found no SEC page that documents it. It answered my test queries. Treat as unofficial; it could change. | No | Same 10 per second | Free | [my test](raw/feasibility/efts_sample.json) |
| Form D data sets | Yes (quarterly ZIP files) | No | Normal EDGAR fair access | Free; 2026 Q3 posted; updated quarterly; the SEC says it cannot guarantee accuracy | [Form D data sets](https://www.sec.gov/data-research/sec-markets-data/form-d-data-sets) |
| Akta (Wokelo) | Yes: REST at `api.akta.pro`, MCP at `https://mcp.akta.pro/mcp` | Yes, `x-api-key` | Pay-as-you-go: 25 per minute; Company Search 100 per day; Company Data 100 per month; List Generation 100 per month; News 10,000 per month; alternative signals not available. Subscription 50 tier: 100 per minute; alternative signals 10 per minute and 750 per month each | $0.05 per credit pay-as-you-go, $0.04 on Subscription; no free tier in the docs | [Rate limits](https://docs.akta.pro/getting-started/rate-limits), [Credits](https://docs.akta.pro/getting-started/pricing), [Overview](https://docs.akta.pro/getting-started/overview), [MCP setup](https://docs.akta.pro/docs/developer-tools/mcp/setup) |
| Wokelo's enterprise API (separate from Akta) | Yes, `api.wokelo.ai` | Yes: client id, secret, login, JWT; accounts are provisioned by Wokelo | `429` with `Retry-After` on overuse; no number published | Credits; "contact sales" | [Getting started](https://docs.wokelo.ai/getting-started), [Credits](https://docs.wokelo.ai/credits), [FAQs](https://docs.wokelo.ai/faqs) |
| Crunchbase | Yes, but sales-gated | Yes, provisioned | Enterprise key: 200 requests per minute, 3 at a time | The Basic API is closed ("We are no longer offering our Basic API"); access "available through the Crunchbase sales team" | [Using the API](https://data.crunchbase.com/docs/using-the-api), [Basic](https://data.crunchbase.com/docs/crunchbase-basic-getting-started) |
| Tavily | Yes | Yes | Development key 100 per minute, production 1,000 per minute; research endpoint 20 per minute | Free 1,000 credits a month, no card; pay-as-you-go $0.008 a credit; Project $30 for 4,000 credits; basic search 1 credit, advanced 2; startups can apply for 100k free credits | [Credits](https://docs.tavily.com/documentation/api-credits), [Rate limits](https://docs.tavily.com/documentation/rate-limits), [Pricing](https://www.tavily.com/pricing) |
| You.com | Yes | Key for the API; keyless MCP profile for search | Self-serve: Web Search, Contents, Answer, Research 10 per second; Finance Research 5 per second. Keyless MCP: 100 queries a day | Web Search $5 per 1,000 calls; Contents $1 per 1,000 pages; Answer $5 per 1,000; $10 free credit is shown on the pricing page as 2,000 searches | [Pricing](https://you.com/pricing), [Rate limits](https://you.com/docs/rate-limits), [Quickstart](https://you.com/docs/quickstart) |
| GitHub REST | Yes | Token for useful volume | 60 per hour unauthenticated; 5,000 per hour with a token; search 30 per minute authenticated; secondary limit 900 points per minute | Free | [REST limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api), [Search](https://docs.github.com/en/rest/search/search) |
| GitHub GraphQL | Yes | Token | 5,000 points per hour per user; secondary limit 2,000 points per minute | Free | [GraphQL limits](https://docs.github.com/en/graphql/overview/rate-limits-and-node-limits-for-the-graphql-api) |
| arXiv API | Yes | No | One request every three seconds, one connection at a time | Free | [Terms of use](https://info.arxiv.org/help/api/tou.html) |
| Hacker News search | Yes (Algolia) | No | 10,000 requests per hour per IP | Free | [HN Algolia API](https://hn.algolia.com/api) (the limit is in the page's script; [excerpt](raw/feasibility/hn/hn_api_rate_limits_excerpt.txt)) |
| Product Hunt | Yes (GraphQL v2) | Token (client-only token for public data) | Not published; "we reserve the right to rate-limit" | Free; "must not be used for commercial purposes" | [Product Hunt API](https://api.producthunt.com/v2/docs) |
| Apple App Store | Yes (Search and Lookup) | No | About 20 calls a minute, "subject to change" | Free | [Apple Search API](https://performance-partners.apple.com/search-api) |
| Apple customer-review feed | **No** (not on Apple's page; it answered my test) | No | Unknown | Free | [my test](raw/feasibility/appstores/rss_reviews_sample.json) |
| Google Play reviews | Official API only for your own apps | OAuth or service account | Not read | Free | [Google Play Developer API](https://developers.google.com/android-publisher/reply-to-reviews) |
| X (Twitter) | Yes | Yes, paid credits | 3 million post reads a month cap | $0.005 per post read; $0.010 per user read | [X pricing](https://docs.x.com/x-api/getting-started/pricing) |
| Facebook Pages | Yes, behind app review | Yes | Not read | Free | [Graph API Page feed](https://developers.facebook.com/docs/graph-api/reference/page/feed/) |
| Reddit | Not used; Ken saves JSON pages by hand | None | None | None | Brief rule |
| OpenAI speech-to-text | Yes | Yes | Not read | `gpt-transcribe` $0.0045 per minute; file limit 25 MB; `whisper-1` etc. deprecated, shut down 2027-02-26 | [Speech to text](https://platform.openai.com/docs/guides/speech-to-text), [Pricing](https://platform.openai.com/docs/pricing) |
| whisper.cpp | Open source tool | No | Local | Free | [README](https://github.com/ggml-org/whisper.cpp) |
| faster-whisper | Open source tool | No | Local | Free | [README](https://github.com/SYSTRAN/faster-whisper) |
| ffmpeg | Open source tool | No | Local | Free | [Filters](https://ffmpeg.org/ffmpeg-filters.html) |
| Claude API | Yes | Yes | Per account tier | Prices in 1.10 | [Pricing](https://platform.claude.com/docs/en/about-claude/pricing), [Rate limits](https://platform.claude.com/docs/en/api/rate-limits) |

**Notes on the table.**
- **Akta's own site blocks scripted fetches.** `akta.pro` answered my request with a Cloudflare challenge (HTTP 403). Its documentation lives at `docs.akta.pro`, which I read in full for pricing and limits. The Wokelo docs at `docs.wokelo.ai` are a different, enterprise product with the same parent company.
- **Third-party claim, not verified on Akta's pages:** a Scalekit article says the Akta MCP server launched 2026-07-23 with 17 tools. [Scalekit](https://www.scalekit.com/blog/akta-pro-mcp-vs-api) Akta's own MCP page confirms the server URL and the clients it supports. [MCP setup](https://docs.akta.pro/docs/developer-tools/mcp/setup)
- **Akta MCP versus REST:** the MCP route can be added to Claude Desktop or Claude Code with the same key as an `x-api-key` header. [MCP setup](https://docs.akta.pro/docs/developer-tools/mcp/setup) For scripted scans use REST: it returns JSON the scan can parse.
- **Free versus paid, in one line:** SEC, HN, arXiv and Apple are free and keyless. Tavily, You.com and GitHub are free with a key. Akta alternative signals, Crunchbase and X are paid or gated.

---

## Part 3. The synthetic data room

R4 designed the room. I read its [file list](data_room_files.csv) and [planted flags](data_room_planted.csv) and agree with them. The fictional company is **Hollis Voice**, an AI phone agent for independent veterinary clinics, raising a $9,000,000 Series A. R4's other options are Brasswick (freight invoices to loads) and Stoopline (compliance software for New York building owners). My view on the three: Hollis Voice suits this panel, because pilots-booked-as-ARR and model-inference costs missing from gross margin are things an AI-literate judge knows. One cost to weigh: real vendors already sell voice AI to vet clinics, which helps the market-signal scan (real competitors exist) and means the invented numbers must not look like any of theirs.

### 3.1 File list (R4's 16 files, with my notes on what each scan reads)

| File | Used by |
|---|---|
| `00_welcome/cover_note_and_index.pdf` | readout |
| `01_overview/pitch_deck.pdf` (14 slides; slide 14 is a claims page) | red flags, frameworks |
| `01_overview/company_overview.pdf` | frameworks |
| `01_overview/pitch_video_script.md` (and Ken's recording) | video |
| `02_financials/financial_model.xlsx` (README, Assumptions, P&L, ARR_Build, Cohorts, Hiring_Plan, Cash_Runway) | red flags |
| `02_financials/cap_table.xlsx` (clean decoy) | red flags (should find nothing) |
| `02_financials/expense_ledger.csv` | red flags (margin) |
| `03_metrics/monthly_metrics.csv` | red flags (vanity metric) |
| `03_metrics/customer_mrr_by_month.csv` | red flags (ARR, cohorts, concentration) |
| `04_customers/order_form_cedar_pine.pdf`, `pilot_agreement_marlow.pdf`, `order_form_brookline_row.pdf` (decoy) | red flags, readout |
| `05_team/founder_bios.pdf`, `05_team/hiring_plan.csv` | founders, red flags (burn) |
| `06_product/product_one_pager.pdf`, `06_product/website_copy.md` | frameworks, presence |

The brief asked for founder bios with "public-looking GitHub handles that are ours." R4's bios hold invented founders; add the handles of the GitHub organisation Ken sets up (see 1.7 for the open point on terms).

### 3.2 Flags, and how each is found

"Script" means a check with a number and a tolerance. "Model" means a model must read text first.

| Flag | Organiser example | Planted at | Script check | Model reading |
|---|---|---|---|---|
| PF1 Pilot booked as ARR | revenue counted as ARR when not recurring | `ARR_Build` row for the Marlow pilot; pilot agreement clauses | Recompute ARR from rows where `product_type = Subscription` and compare to `ARR_TOTAL` | Reads the pilot agreement to confirm 30 days notice and no duty to convert |
| PF2 Deck ARR differs from model | numbers that disagree between deck and model | Deck slide 3 and claims page; `ARR_TOTAL` | Match the deck claim labelled ARR to the named cell, 1 percent tolerance | Extracts the deck claim and its label from the PDF |
| PF2b Video ARR differs from deck | same | Video line at about 0:35 | Compare the two numbers once both are extracted | Extracts the spoken number from the transcript |
| PF3 Churn hidden in cohorts | churn hidden in cohort charts | `Cohorts` tab, which drops customers who left in two months; deck slide 6 | Rebuild cohorts from `customer_mrr_by_month.csv`; compare counts, net and gross retention | Reads the tab note and the chart caption and says why the cohort definition hides churn |
| PF4 Burn does not match the hiring plan | burn that does not match the hiring plan | `hiring_plan.csv` (24 hires) against the model's 8 | Payroll from the hiring plan times the load factor, rerun cash, compare to `Cash_Runway` and the deck's runway | Little; writes the explanation |
| PF5 Customer concentration | (extra) | `customer_mrr_by_month.csv`, customer C-BIG | Top-one and top-three share of MRR against the deck claim | Reads the order form for term and exit rights |
| PF6 Gross margin leaves out delivery cost | (extra) | `expense_ledger.csv`, P&L rows | Sum hosting, inference, telephony and support into cost of revenue; recompute | Reads ledger line descriptions that are not cleanly categorised |
| PF7 Cumulative sign-ups shown as active | (extra, the vanity metric) | `monthly_metrics.csv`, deck slide 3 | A column that never decreases is flagged; match the deck number to that column's last value | Reads the deck label ("clinics") against the column name |

Result: three flags (PF1, PF4, PF5) are pure script checks on the CSVs and the workbook. PF3, PF6 and PF7 are script checks too, but a model first reads a tab note, ledger lines or a deck label. PF2 and PF2b need a model to pull the number out of the PDF or the transcript before the script compares. The model's job is reading and explaining; the script's job is deciding that a number is wrong. R4's own count is 5 entries caught by the seed drop alone and 3 more from the full room.

**Decoys.** The cap table and the Brookline Row order form are clean, so a good tool says nothing about them. A "false positive count" is itself a number a judge can follow.

### 3.3 Building and checking the room

- A generator script makes every file from one seeded run and writes `planted.csv`. R4 already describes it (reportlab for the PDFs, matplotlib for charts, `xlsxwriter` so formulas carry cached values, `openpyxl` to reload and test).
- Two tools are missing on this Mac: `python-pptx` and `xlsxwriter` (R4). I did not install anything.
- Building the room is the right use of this week: it is data, not product code.

---

## Part 4. Stack recommendation

### 4.1 Recommended: Python scans, FastAPI to serve them, React for the readout

- **Structure.** One repo, one folder per scan: `scans/redflags/`, `scans/comps/`, `scans/signals/`, `scans/frameworks/`, `scans/video/`, `scans/presence/`, `scans/founders/`, plus `readout/` (React) and `schema/`.
- **The contract.** `schema/claim.schema.json` is frozen before anyone writes a scan. It holds `Claim` and `Source` (below). Pydantic models are generated from it for Python, and TypeScript types for the front end.
- **Each scan** is a plain function: `run(company_dir) -> ScanResult`, and a command: `python -m scans.redflags data_room/hollis`. It writes `out/hollis/redflags.json`. No scan imports another.
- **FastAPI** has three routes: list scans, run a scan, serve a result file. React reads `out/hollis/*.json` and renders the readout; it does not know how a scan works.
- **Who works without stepping on each other.**
  - The finance Python person: `scans/redflags/` and `scans/comps/`.
  - The Python and ML person: `scans/video/`, `scans/presence/`, `scans/founders/`.
  - The TypeScript person: `readout/`, owning the page, the footnote popover that opens a source, and the jump-to-second video player.
  - Ken: the data room, the prompts and framework schemas (`scans/frameworks/`), the memo assembly prompt, and the demo run.
  - Each person owns a folder, so merge conflicts happen only in `schema/`, which is frozen.
- **The shared result, as Pydantic:**

```python
class Source(BaseModel):
    kind: Literal["file", "url", "api", "video"]
    uri: str                      # path, URL, or API call
    locator: str                  # "ARR_Build!E14", "slide 3", "t=35-41", "line 12"
    quote: str                    # exact text, checked by script
    retrieved_at: str

class Claim(BaseModel):
    id: str
    scan: str
    text: str
    severity: Literal["info", "watch", "flag"] | None
    sources: list[Source]         # at least one
    conflicts_with: list[str] = []   # ids of claims that disagree
```

- **The quote checker.** A small script reads each claim, opens its source, and confirms the quote text appears at the locator. A claim that fails is dropped from the readout and listed in a "could not verify" box. It is the working version of "every claim links to its source", and it needs no model.
- **How the readout renders.** Conflicts first, then flags by severity, then the other scans. Each claim has a footnote number; the footnote opens the file page, cell, URL or video second.
- **Why this one.** The scans are Python-shaped (whisper, ffmpeg, pandas, openpyxl, Anthropic and GitHub SDKs). Three of the four people can work in Python or TypeScript with no new tool. The page only reads JSON.

### 4.2 Alternative A: one Streamlit app

- Everything in one Python process; tabs per scan; the fastest way to get something on screen.
- Costs: the TypeScript person has little to do; the readout's footnote popovers and video jumping are awkward. Best if the team's time is short or the React person is absent.

### 4.3 Alternative B: Rails for the app, Python scans as subprocesses

- Ken builds the app and the readout in Rails; the scans stay Python command-line functions that write JSON; Rails runs them and reads the files.
- Costs: Ken becomes the bottleneck for the page; the TypeScript person has no natural place; two runtimes to install on a demo laptop. Best if Ken wants to stay in the stack he knows and the others stay in Python.

(The company's own data and repo layout belong to W3's `ARCHITECTURE.md`; this section only gives the feasibility view.)

---

## Part 5. Keys and accounts Ken must get this week

| Item | Needed for | Cost / terms | Link |
|---|---|---|---|
| Anthropic API key | Every scan | Pay per token; see 1.10 | [Pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Tavily key | Search for pricing pages, news, founder talks | Free 1,000 credits a month, no card | [Tavily credits](https://docs.tavily.com/documentation/api-credits) |
| You.com key (or use the keyless MCP profile) | Second search source | Keyless: 100 queries a day; key: $5 per 1,000 searches | [You.com pricing](https://you.com/pricing) |
| GitHub token | Founder scan | Free; 5,000 requests an hour | [GitHub limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api) |
| Akta key, and a question to the sponsor about the paid plan | Market signals on competitors | Pay-as-you-go $0.05 a credit; alternative signals need Subscription | [Akta credits](https://docs.akta.pro/getting-started/pricing), [Akta rate limits](https://docs.akta.pro/getting-started/rate-limits) |
| Product Hunt token (optional) | Presence scan | Free; non-commercial use | [Product Hunt API](https://api.producthunt.com/v2/docs) |
| OpenAI key (optional) | Whisper API fallback | $0.0045 a minute for `gpt-transcribe` | [OpenAI pricing](https://platform.openai.com/docs/pricing) |
| A declared EDGAR User-Agent string, with a real contact address | EDGAR | None | [SEC](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data) |
| Not needed | HN Algolia, arXiv, Apple, ffmpeg, whisper.cpp | | |
| Skip | Crunchbase (sales only), X (paid), Facebook (app review) | | See Part 2 |

Also this week: install whisper.cpp and download a model on the demo laptop; check GitHub's terms before making demo accounts.

---

## Open points

- **Akta on Saturday.** I cannot tell from the docs whether a hackathon plan exists. Ask the sponsor.
- **GitHub demo accounts.** I did not read the terms for persona accounts.
- **Google Play, Product Hunt, Facebook, Claude API rate numbers.** Not read or not published; no numbers are given for them here.
- **`efts.sec.gov` search-index** is not documented by the SEC. If it breaks, the fallback is the EDGAR web search page or cached results.
- **Opus 5.5 request limits** (no temperature, no forced tool choice) come from the claude-api skill bundled with Claude Code, not a docs page I fetched.

## Cleanup needed

I removed nothing on purpose. Files in `raw/feasibility/` that can go once the research is closed, listed for the cleanup batch:

- Large duplicate HTML that also exists as `.txt`: `raw/feasibility/video/ffmpeg_filters.html`, `video/openai_pricing.html`, `video/openai_speech_to_text.html`, the four `www_sec_gov_*.html` files at the top of `raw/feasibility/`, `raw/feasibility/crunchbase/*.html`, `raw/feasibility/github/*.html`, `raw/feasibility/search/*.dl` and `appstores/*.html` where a `.txt` sits beside it.
- `raw/feasibility/hn/main.js` (2.6 MB, Algolia's script; the rate-limit line is kept in `hn_api_rate_limits_excerpt.txt`).
- `raw/feasibility/formd/2026q3_d.zip` (3.65 MB, re-downloadable; `formd_counts_output.txt` keeps the result).
- `raw/feasibility/frames_sample_head.json` (410 KB sample).

## Files written

- `/Users/kennethstclair/Documents/workspace/tricorder/docs/reports/20261022.02_research/research_feasibility.md` (this file)
- `/Users/kennethstclair/Documents/workspace/tricorder/docs/reports/20261022.02_research/raw/feasibility/` (saved pages and samples; scripts and output under `formd/`)
