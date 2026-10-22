# Architecture

## Charter

**What belongs:** The shape of the system at a level a person can hold in their head. The stack and the folder structure. The surfaces people and agents touch, and the outside services behind them. The main models and how they relate, in outline.

**What does not:** How one feature works. That goes in a diagram or its own ongoing doc. How a feature got built. That stays in docs/features/.

**Level of detail:** A paragraph or a short table per area. Link out when a section passes three paragraphs.

**Describes:** the code root named in Settings

**Sources:** The feasibility research ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), the main source: stack, scans, data sources, keys, model calls), the data room research ([research_data_room.md](../reports/20261022.02_research/research_data_room.md): the generator, the plants, the answer key), the landscape research ([research_landscape.md](../reports/20261022.02_research/research_landscape.md): sponsor tools, what the panel will ask), the writers' brief ([00_brief_for_writers.md](../features/20261022.01_hackathon_plan/00_brief_for_writers.md): the inbox block and the data rule), the guardrails ([guardrails.md](../../.claude/guardrails.md)), and three official pages read on 2026-10-22 for the inbox design: Google's [Gmail API scopes](https://developers.google.com/workspace/gmail/api/auth/scopes), Microsoft's [Graph permissions reference](https://learn.microsoft.com/en-us/graph/permissions-reference) and Postmark's [inbound webhook](https://postmarkapp.com/developer/webhooks/inbound-webhook). No code exists yet; this doc is the design the [roadmap](ROADMAP.md) builds.

## The stack

Python scans as plain command-line functions, each writing one JSON file. FastAPI serves those files. A React page shows the readout. Every scan returns the same typed result: a list of claims, each with its sources. This is the feasibility research's recommendation (Part 4.1). The scans are Python-shaped (whisper, ffmpeg, pandas, openpyxl, the Anthropic and GitHub SDKs), and the page only reads JSON, so the TypeScript person never waits on Python.

Alternatives, and why not:

- **One Streamlit app.** The fastest way to get a screen up, but the frontend role has little to do, and the footnote popovers and video jumps are awkward. A prior financial-AI hackathon also listed "Simple Streamlit only applications" among its disqualified projects ([research_landscape.md](../reports/20261022.02_research/research_landscape.md), Part 4).
- **Rails for the app, Python scans as subprocesses.** Ken stays in the stack he knows, but he becomes the bottleneck for the page, the frontend role has no natural place, and the demo laptop needs two runtimes.

## Folder layout

One folder per person, so Saturday's pull requests do not touch the same files. Owners follow the feasibility research's Part 4.1, with market signals given to backend-and-data.

| Folder | What it holds | Owner on Saturday |
|---|---|---|
| `schema/` | The Claim models, the exported JSON Schema, generated TypeScript types in `schema/ts/`, the quote checker. The models and the JSON Schema are written this week by the skeleton slice (option B on the overview page) and are frozen from then; only the quote checker is Saturday work. | captain |
| `scans/memo/` | Merges the scan results into the readout. | captain |
| `eval/` | Scores a readout against the answer key. | captain |
| `demo/` | The demo script's files and the frozen outputs. | captain |
| `readout/` | The React readout page. | frontend |
| root files, `server/`, `bin/` | Dependency list, CI, `.env.example`, the FastAPI app, `bin/ci-py`, `bin/ci-web` and `bin/smoke`. | backend-and-data |
| `scans/video/`, `scans/signals/` | Pitch video and market signals. | backend-and-data |
| `scans/redflags/`, `scans/comps/` | Red-flag engine and comps. | design-and-finance |
| `scans/frameworks/`, `scans/presence/`, `scans/founders/` | After Saturday. | agent |
| `data_room/` | The generator, the two rooms (`hollis_voice/` and `hollis_voice_seed_drop/`) and the answer key `answer_key.json`. Written this week. | agent |
| `cache/` | Outside data saved this week: Form D, XBRL facts, Akta pulls, pricing pages. | agent |
| `sample_out/` | Hand-written example results, one per scan. | captain |
| `out/` | Scan results, one folder per room. Ignored by git. | nobody; scans write it |

Each scan keeps its tests inside its own folder (`scans/redflags/tests/`), so no shared test folder collects edits. Each scan also keeps its prompts, typed in from [FRAMEWORKS.md](FRAMEWORKS.md), in its own folder (`scans/redflags/prompts/`), so the scan's owner edits them and no shared `prompts/` folder collects edits.

## The Claim schema

Every scan writes one ScanResult. The readout is built only from claims. The feasibility research's Pydantic sketch (Part 4.1) is the starting point; this version adds the value, the check and the confidence label.

The JSON Schema in [FRAMEWORKS.md](FRAMEWORKS.md) ("The shared Claim") is the single source for every field type. The Pydantic models below follow it. If the two ever differ, FRAMEWORKS wins.

```python
class Source(BaseModel):
    kind: Literal["file", "url", "api", "video"]
    uri: str                 # path inside the room, a URL, or the API call
    locator: str             # "slide 3", "page 2", "ARR_Build!E14", "ARR_TOTAL", "row 118", "clause 7", "t=35-41"
    start_s: float | None    # video only, copied from the transcript
    end_s: float | None
    quote: str               # the exact span; the quote checker looks for it at the locator
    retrieved_at: str | None # ISO date the source was read; null when not known

class Value(BaseModel):
    number: float
    unit: Literal["USD", "USD_per_month", "USD_per_year", "percent", "months", "days", "accounts", "count"]
    label: Literal["arr", "mrr", "paying_accounts", "accounts_created", "nrr_12m", "grr_12m", "cohort_size", "gross_margin", "cost_of_revenue", "runway_months", "net_burn_monthly", "payroll_monthly", "hires", "headcount", "cash", "largest_customer_share", "top3_customer_share", "arpa", "acv", "cac", "payback_months", "ltv", "raise_amount", "pre_money", "post_money", "ownership", "tam", "sam", "som", "price", "contract_term", "notice_period", "signal", "other"]
    period: str | None       # "2026-09"

class Check(BaseModel):
    kind: Literal["script", "model"]
    name: str                # check name from FRAMEWORKS.md, or the prompt id
    model: str | None        # model id when kind is "model"

class Claim(BaseModel):
    id: str                  # "redflags-004"
    scan: str
    text: str                # the sentence the readout shows
    value: Value | None
    severity: Literal["info", "watch", "flag"] | None
    check: Check
    confidence: Literal["computed", "quoted", "judged", "unverified"]
    sources: list[Source]    # at least one, enforced
    conflicts_with: list[str] = []   # ids of claims that disagree

class Gap(BaseModel):
    what: str                # "No customer contracts in the room"
    why: str                 # "file missing", "link needs a viewer email", "Akta plan returns 403"
    would_need: str          # the source that would close it

class Panel(BaseModel):
    name: str                # "comps table", "signals grid", "video moments"
    columns: list[str]       # column names
    rows: list[list[str]]    # one list of strings per row

class ScanResult(BaseModel):
    scan: str
    room: str
    ran_at: str
    inputs: list[str]        # files and calls the scan read
    claims: list[Claim]
    gaps: list[Gap]
    panels: list[Panel] = [] # optional named tables or lists the page shows beside the claims
```

**Confidence is a label, not a number.** `computed`: a script recomputed the number from the source. `quoted`: a model read it and the quote checker found the quote. `judged`: a model's reading with nothing to recompute, such as whether a cohort note hides churn. `unverified`: the quote checker could not find the quote; the readout puts the claim in a "could not verify" box instead of the memo.

**The quote checker** (`schema/check_quotes.py`) opens each source at its locator and looks for the quote with spacing and case ignored: PDF page text through pdfplumber, spreadsheet cells through openpyxl with cached values, CSV rows, markdown lines, transcript segments for video. URL and API sources are checked against the copy saved in `cache/`. It needs no model (feasibility Part 4.1).

## The scan interface

| Part | Rule |
|---|---|
| Function | `run(room_dir: Path) -> ScanResult` |
| Command | `python -m scans.<name> <room_dir>`, for example `python -m scans.redflags data_room/hollis_voice_seed_drop` |
| Output | `out/<room>/<name>.json`, one ScanResult |
| Inputs | Files in the room, files in `cache/`, and outside calls only when `TRICORDER_OFFLINE` is unset |
| Isolation | No scan imports another scan. A scan never reads another scan's output; only the memo does. |
| Failure | A missing input or a refused call is a Gap, and the scan still exits 0. A crash exits non-zero. |

**How the readout merges them.** `scans/memo/` reads every `out/<room>/*.json` that exists and runs the quote checker again. It links claims that carry a Value with the same label, unit and period whose numbers differ by more than the tolerance (1 percent, the data room research's deck-against-model tolerance), and writes each link into both claims' `conflicts_with`. It orders the readout: conflict groups first, then flags by severity, then the other scans. One model pass writes connecting sentences, and each must cite claim ids or it is dropped (feasibility 1.8). A scan with no output file becomes a gap in the readout. The result is `out/<room>/readout.json`, which the page renders.

## The data room and the answer key

The generator is the data room research's design (Part 3.6), and lives at `data_room/`. `generate.py --seed 20261024` runs one simulation (`src/facts.py`) and writes every file from it. Each plant is one function that takes a true fact, returns the shown value, and records where it wrote it. `--no-plants` writes a room that reconciles everywhere. Output: `data_room/hollis_voice/` (the full room) and `data_room/hollis_voice_seed_drop/` (the thin first tier). Both rooms also hold `01_overview/claims.json`, the deck's claims page (slide 14) as data, written from the same list, so the claims can be read when PDF text extraction fails.

The answer key, `data_room/answer_key.json`, sits outside both room folders so Tricorder is never pointed at it. It holds the 8 planted entries and the 3 decoys, each with its locations, the true value, the shown value, the check name and the tolerance (data room research, Part 3.6). The check names are the red-flag engine's check names, fixed this week in [FRAMEWORKS.md](FRAMEWORKS.md).

**How the test compares.** `eval/score.py <room>` reads `out/<room>/readout.json` and the answer key. A planted entry counts as found when a readout claim with severity `flag` has the key's check name and cites at least one of the key's files. A decoy counts as wrongly flagged when a `flag` claim cites the decoy's file and location. It prints found of 8 and decoys flagged of 3, and the page shows that score. The data room research expects 5 entries from the seed drop and the other 3 from the full room (Part 3.4). The red-flag engine's own test in `scans/redflags/tests/` runs the same comparison on that scan alone.

## The inbox input (after Saturday)

The brief makes the inbox an input and recommends a forwarding address first, because it needs no OAuth review. None of the research tracks covered the inbox, so the facts below come from the three official pages named in the Sources line.

| Path | How it works | What it costs us |
|---|---|---|
| **Forwarding address (first)** | The investor forwards a pitch email to an address such as deals@. A mail-receiving service turns each message into a webhook call. Postmark's inbound webhook, for example, posts the message as JSON with an `Attachments` array (name, content, content type, length). The server saves the PDFs into a new company folder and runs the scans. | A domain and a service account. Tricorder sees only what the investor chooses to forward. |
| **Gmail API** | Read the investor's mailbox for decks. | Google lists `gmail.readonly`, `gmail.metadata` and `gmail.modify` as restricted scopes. Restricted scopes need restricted-scope OAuth app verification, and an app that stores or sends that data on servers must also pass a security assessment. |
| **Microsoft Graph** | Read Outlook mail through `Mail.Read`. | The delegated permission reads the signed-in user's mailbox and needs no admin consent; Microsoft says it is available for personal accounts too. The application permission reads every mailbox and needs admin consent. |

**Links in the email.** DocSend links need the viewer's email and cannot be fetched blind (brief, 11:20 AM block). Google Drive, Dropbox and Notion links are fetched only when they open without a sign-in. Any link that cannot be opened becomes a Gap that tells the investor what to do, such as "open the DocSend link and drop the PDF here".

**The data rule** (brief, 11:20 AM block). The mailbox is read for decks only. Nothing is stored beyond the readout and its sources. The investor can see and delete everything pulled. The forwarding path keeps this rule easiest, because nothing outside the forwarded message is ever read.

## Outside data sources

From the feasibility research's Part 2, with the link it read for each. On Saturday the comps and signals scans read the copies saved in `cache/`; live calls are for after Saturday.

| Source | Terms that shape the code |
|---|---|
| SEC EDGAR (data.sec.gov, full-text search, Form D files) | No key. Every request sends a declared User-Agent with a contact address, plus `Accept-Encoding: gzip, deflate`. 10 requests a second. No CORS, so call it from the server. The full-text JSON endpoint is undocumented; treat it as able to break. Form D has no business description. |
| Akta (Wokelo) | `x-api-key` header. Pay-as-you-go: 25 requests a minute, Company Search 100 a day, Company Data 100 a month, News 10,000 a month, and 403 on headcount, traffic, jobs, social posts and reviews. Those need the Subscription plan. The p99 latency on some signals runs past 55 seconds, so the demo reads saved files. |
| Tavily | Key. Free 1,000 credits a month, no card. Development key 100 requests a minute. |
| You.com | Key for the API, $5 per 1,000 searches; or the keyless MCP profile at 100 queries a day. |
| GitHub | Token. 60 requests an hour without one, 5,000 with one; search 30 a minute with a token. |
| Hacker News (Algolia) | No key. 10,000 requests an hour per IP. |
| arXiv | No key. One request every three seconds, one connection at a time. |
| Apple App Store lookup | No key. About 20 calls a minute. The review feed is undocumented. |
| Product Hunt | Token. Its terms say non-commercial use only. |
| Crunchbase | REST is sales-gated. The landscape research says use its MCP as a research aid only, not as a shipped data source. |
| X, Facebook | Skipped: X is paid per read; Facebook page posts need app review. |
| LinkedIn | Never. The organisers' tracks say its terms prohibit scraping. |
| Reddit | Never fetched by an agent. Only pages Ken saved by hand are read. |

## Environment variables

All secrets come from the environment and are never committed ([guardrails.md](../../.claude/guardrails.md)). `.env.example` lists them with empty values.

| Variable | What it is for | Needed |
|---|---|---|
| `ANTHROPIC_API_KEY` | Every model call | Saturday |
| `TRICORDER_MODEL_READ` | Model for reading and the memo pass; default `claude-opus-5-5` | Saturday |
| `TRICORDER_MODEL_BULK` | Model for bulk classification; default `claude-haiku-5-5` | Saturday |
| `TRICORDER_OFFLINE` | `1` makes every scan read `cache/` and make no outside calls; the demo runs with it on | Saturday |
| `TRICORDER_OUT_DIR` | Where results go; default `out/` | Saturday |
| `WHISPER_CPP_BIN` | Path to the whisper.cpp command | Saturday |
| `WHISPER_MODEL_PATH` | Path to the downloaded whisper model file | Saturday |
| `EDGAR_USER_AGENT` | The declared User-Agent with a contact address | This week (cache) and after |
| `AKTA_API_KEY` | Akta company data, news and signals | This week (cache) and after |
| `TAVILY_API_KEY` | Search and page extraction | This week (cache) and after |
| `YOU_API_KEY` | Second search source | After |
| `GITHUB_TOKEN` | Founder profiles | After |
| `PRODUCT_HUNT_TOKEN` | Presence scan, if its terms allow | After |
| `OPENAI_API_KEY` | Whisper API fallback only | Optional |
| `INBOUND_WEBHOOK_SECRET` | Checks that an inbound mail call came from the mail service | After (inbox-forward) |

Nicrron's gateway is not in the stack. It is OpenAI-compatible ([research_landscape.md](../reports/20261022.02_research/research_landscape.md), Part 2), and we have not checked that it passes Anthropic's structured-output setting through.

## Model calls

**Anthropic's API with structured outputs.** Each prompt passes a JSON Schema in `output_config.format`, or a Pydantic class to `client.messages.parse(...)`, and reads `parsed_output` ([structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), via feasibility 1.10). Opus 5.5 does the red-flag reading and the memo pass; Haiku 5.5 does bulk classification. The feasibility research lists Opus 5.5 at $4 and $20 per million tokens in and out, and Haiku 5.5 at $0.10 and $0.50 for prompts up to 100,000 tokens.

**Citations cannot be combined with structured output.** The API returns a 400 when the citations feature is sent together with `output_config.format` (feasibility 1.8). So Tricorder does not use Anthropic's citations. Each claim carries its own quoted span and locator, and the quote checker confirms the span is really in the source. This also works for scans with no document behind them, such as comps and signals.

**Whisper runs locally through whisper.cpp.** ffmpeg makes a 16 kHz mono WAV, which is the only input whisper.cpp reads, and whisper.cpp returns segments with timestamps, running on the GPU through Metal on Apple Silicon (feasibility 1.5). The model then picks claims by segment id, so times are copied, not guessed. The API is the fallback only: OpenAI's docs show word and segment timestamps only for `whisper-1`, which is deprecated and shuts down 2027-02-26, and the recommended `gpt-transcribe` ($0.0045 a minute, files up to 25 MB) shows none (feasibility 1.5).
