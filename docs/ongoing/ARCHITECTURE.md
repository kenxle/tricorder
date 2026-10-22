# Architecture

## Charter

**What belongs:** The shape of the system at a level a person can hold in their head. The stack and the folder structure. The surfaces people and agents touch, and the outside services behind them. The main models and how they relate, in outline.

**What does not:** How one feature works. That goes in a diagram or its own ongoing doc. How a feature got built. That stays in docs/features/.

**Level of detail:** A paragraph or a short table per area. Link out when a section passes three paragraphs.

**Describes:** the code root named in Settings

**Sources:** The feasibility research ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), the main source: stack, scans, data sources, keys, model calls), the data room research ([research_data_room.md](../reports/20261022.02_research/research_data_room.md): the generator, the plants, the answer key), the landscape research ([research_landscape.md](../reports/20261022.02_research/research_landscape.md): sponsor tools, what the panel will ask), the research gaps ([research_gaps.md](../reports/20261022.02_research/research_gaps.md): how decks reach investors), the writers' brief ([00_brief_for_writers.md](../features/20261022.01_hackathon_plan/00_brief_for_writers.md): every "Added" block from 11:20 AM to 2:19 PM, for the inbox, the data rule, steering, contracts, the bank check, the ask list, the checklist, the memo, reader copies, multiplayer and speed), [PRODUCT_BRIEF.md](PRODUCT_BRIEF.md), [CHECKLIST.md](CHECKLIST.md) with [checklist.csv](checklist.csv), [MEMO_TEMPLATE.md](MEMO_TEMPLATE.md), the after-Saturday slices in [ROADMAP.md](ROADMAP.md), the overview page's skeleton card ([00_overview.md](../features/20261022.01_hackathon_plan/00_overview.md)), the guardrails ([guardrails.md](../../.claude/guardrails.md)), and four official pages: Google's [Gmail API scopes](https://developers.google.com/workspace/gmail/api/auth/scopes), Microsoft's [Graph permissions reference](https://learn.microsoft.com/en-us/graph/permissions-reference) and Postmark's [inbound webhook](https://postmarkapp.com/developer/webhooks/inbound-webhook), read on 2026-10-22, and Plaid's [Sandbox custom users](https://plaid.com/docs/sandbox/user-custom/) ([saved copy](../reports/20261022.02_research/raw/feasibility/plaid/sandbox_user_custom.md)). No product code exists yet. This doc is the design the [roadmap](ROADMAP.md) builds, starting with the empty skeleton an agent writes this week (option B on the overview page's skeleton card).

## The stack

Python scans as plain command-line functions, each writing one JSON file. FastAPI serves those files. A React page shows the readout. Every scan returns the same typed result: a list of claims, each with its sources. This is the feasibility research's recommendation (Part 4.1). The scans are Python-shaped (whisper, ffmpeg, pandas, openpyxl, the Anthropic and GitHub SDKs), and the page only reads JSON, so the TypeScript person never waits on Python.

Alternatives, and why not:

- **One Streamlit app.** The fastest way to get a screen up, but the frontend role has little to do, and the footnote popovers and video jumps are awkward. A prior financial-AI hackathon also listed "Simple Streamlit only applications" among its disqualified projects ([research_landscape.md](../reports/20261022.02_research/research_landscape.md), Part 4).
- **Rails for the app, Python scans as subprocesses.** Ken stays in the stack he knows, but he becomes the bottleneck for the page, the frontend role has no natural place, and the demo laptop needs two runtimes.

## Folder layout

One folder per person, so Saturday's pull requests do not touch the same files. Owners match the roadmap's "Who owns what" table, which is the source of truth when they differ.

| Folder | What it holds | Owner on Saturday |
|---|---|---|
| `schema/` | The Claim models, the exported JSON Schema, generated TypeScript types in `schema/ts/`, the quote checker. The models and the JSON Schema are written this week by the skeleton slice (option B on the overview page) and are frozen from then; only the quote checker is Saturday work. | captain |
| `scans/memo/` | Merges the scan results into the readout. | captain |
| `eval/` | Scores a readout against the answer key. | captain |
| `demo/` | The demo script's files and the frozen outputs. | captain |
| `readout/` | The React readout page, including the static market-signals panel. | frontend |
| root files, `server/`, `bin/` | Dependency list, CI, `.env.example`, the FastAPI app, `bin/ci-py`, `bin/ci-web` and `bin/smoke`. | backend-and-data |
| `schema/readers.py` | The shared file readers every scan and the quote checker import. | backend-and-data |
| `scans/video/`, `scans/readings/` | Pitch video, and the model readings (the pilot clause and the cohort note; cut first). | backend-and-data |
| `scans/signals/` | This week's cached competitor readings, which the readout page shows as a static panel. Written this week. | agent |
| `scans/redflags/`, `scans/comps/` | Red-flag engine and comps. | design-and-finance |
| `scans/frameworks/`, `scans/presence/`, `scans/founders/`, `scans/outside/` | After Saturday; `scans/outside/` is the associate's ten tabs. | agent |
| `data_room/` | The generator, the two rooms (`hollis_voice/` and `hollis_voice_seed_drop/`) and the answer key `answer_key.json`. Written this week. | agent |
| `cache/` | Outside data saved this week: Form D, XBRL facts, Akta pulls, pricing pages. | agent |
| `sample_out/` | Hand-written example results, one per scan. | captain |
| `out/` | Scan results, one folder per room. Ignored by git. | nobody; scans write it |

After Saturday the layout adds `store/` (saved readouts, per fund, with delete), `inbox/` (the forwarding webhook), `scans/bank/` (the bank check), `memo/` (the memo export, its versions and reader copies) and `scenarios/` (what-if recomputation). Contract terms and deck against the books stay inside `scans/redflags/`, because they are red-flag entries in [FRAMEWORKS.md](FRAMEWORKS.md).

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
    corroborated_by: list[str] = []  # ids of claims from an independent source that agree

class Gap(BaseModel):
    what: str                # "No customer contracts in the room"
    why: str                 # "file missing", "link needs a viewer email", "Akta plan returns 403"
    would_need: str          # the source that would close it

class Panel(BaseModel):
    name: str                # "comps table", "signals grid", "video moments"
    columns: list[str]       # column names
    rows: list[list[str]]    # one list of strings per row

class Piece(BaseModel):
    name: Literal["traction_and_revenue", "retention", "burn_and_runway", "unit_economics", "customers", "market", "comps", "team", "the_pitch_itself"]
    verdict: Literal["looking_strong", "looking_weak", "mixed", "not_enough_in_the_room"]
    reason: str              # one line, with its number and source
    reason_claim_ids: list[str]  # the claims the reason line rests on
    claim_ids: list[str]     # every claim in the piece, for the drill-down
    corroborating_sources: int   # independent sources behind its corroborated claims
    contradicting_sources: int   # sources behind its contradicted or flagged claims
    status: Literal["done", "running", "waiting_on_input"] = "done"  # the progressive readout; Saturday is always "done"
    waiting_on: list[str] = []   # inputs the piece still needs, such as "financial model"

class TopFlag(BaseModel):
    kind: Literal["green", "red"]
    piece: Literal["traction_and_revenue", "retention", "burn_and_runway", "unit_economics", "customers", "market", "comps", "team", "the_pitch_itself"]
    rank: int                # 1 is the strongest green or the worst red
    text: str                # the one headline line, with its numbers and sources
    claim_ids: list[str]     # the claims behind it, for the click into the piece

class AskItem(BaseModel):
    what: str                # "Current monthly burn and the bank balance behind it"
    why: str                 # the claim or gap it would settle, with its number
    piece: str               # the piece it feeds
    from_kind: Literal["gap", "weak_piece", "checklist"]
    claim_ids: list[str] = []    # claims or gaps it would settle
    checklist_id: str | None = None  # "C29", when it comes from a missing checklist item
    if_you_have_it: bool = False     # the item is only "lighter" at the company's stage

class ScanResult(BaseModel):
    scan: str
    room: str
    ran_at: str
    inputs: list[str]        # files and calls the scan read
    claims: list[Claim]
    gaps: list[Gap]
    panels: list[Panel] = [] # optional named tables or lists the page shows beside the claims
```

**The readout file** (`out/<room>/readout.json`) holds the top green and red flags first, then the nine Pieces, then every claim and gap, then the ask list. The page draws the headline list from the TopFlags, the overview from the Pieces, the drill-down from the claims each Piece lists, and the ask list from the AskItems. A Piece's verdict and the choice of top flags come from script rules, never a model ([FRAMEWORKS.md](FRAMEWORKS.md), "Piece verdicts" and "Top green and red flags").

**The order of the pieces is a view, not data.** On Saturday the page shows them in one default order and the operator can move them up and down. After Saturday the default order depends on the company's stage (pre-seed, seed, Series A), from a stated table beside "Piece verdicts" in FRAMEWORKS.md, and each operator's own order is saved per stage ([ROADMAP.md](ROADMAP.md), stage-views). Changing the order never changes a verdict.

**Confidence is a label, not a number.** `computed`: a script recomputed the number from the source. `quoted`: a model read it and the quote checker found the quote. `judged`: a model's reading with nothing to recompute, such as whether a cohort note hides churn. `unverified`: the quote checker could not find the quote; the readout puts the claim in a "could not verify" box instead of the memo.

**The quote checker** (`schema/check_quotes.py`) opens each source at its locator and looks for the quote with spacing and case ignored: PDF page text through pdfplumber, spreadsheet cells through openpyxl with cached values, CSV rows, markdown lines, transcript segments for video. URL and API sources are checked against the copy saved in `cache/`. It needs no model (feasibility Part 4.1).

## The claims workflow

The deck and the pitch video make the claims; every other document and the outside world either support each claim, contradict it, or say nothing. Extract, normalise, find evidence, compare by script, label as supported, contradicted or unsupported, then feed the pieces. The full flow and its steps: [diagrams/claims_workflow.md](diagrams/claims_workflow.md).

## The scan interface

| Part | Rule |
|---|---|
| Function | `run(room_dir: Path) -> ScanResult` |
| Command | `python -m scans.<name> <room_dir>`, for example `python -m scans.redflags data_room/hollis_voice_seed_drop` |
| Output | `out/<room>/<name>.json`, one ScanResult |
| Inputs | Files in the room, files in `cache/`, and outside calls only when `TRICORDER_OFFLINE` is unset. A room can be partial: a deck alone, or a folder of contracts alone, is a valid room. |
| Needs | Each scan declares the input kinds it needs (company name, deck, model, metrics, contracts, video). After Saturday the scheduler uses this to start it early. |
| Isolation | No scan imports another scan. A scan never reads another scan's output; only the memo does. |
| Failure | A missing input or a refused call is a Gap, and the scan still exits 0. A crash exits non-zero. |

**How the readout merges them.** `scans/memo/` reads every `out/<room>/*.json` that exists and runs the quote checker again. It links claims that carry a Value with the same label, unit and period whose numbers differ by more than the tolerance (1 percent, the data room research's deck-against-model tolerance), and writes each link into both claims' `conflicts_with`. It also links claims from independent sources whose numbers agree within the same tolerance, and writes each link into both claims' `corroborated_by`. Then it groups the claims into the nine pieces and gives each piece its verdict, by the script rule in [FRAMEWORKS.md](FRAMEWORKS.md) ("Piece verdicts"). Last, it picks the best green flags and the worst red flags from the piece verdicts and the flags, by the script rule in [FRAMEWORKS.md](FRAMEWORKS.md) ("Top green and red flags"). The readout opens on those, then lists the pieces, strong and weak alike, and each piece lists its claims for the drill-down. Then a script builds the ask list: one AskItem per gap (from its `would_need`), one per weak or mixed piece whose reason more information could settle, and, after Saturday, one per checklist item expected at the company's stage that the room lacks. Two lines that ask for the same thing are merged. One model pass writes connecting sentences, and each must cite claim ids or it is dropped (feasibility 1.8). It may shorten a piece's reason line, but never change its verdict. A scan with no output file becomes a gap in the readout. The result is `out/<room>/readout.json`, which the page renders.

## The data room and the answer key

The generator is the data room research's design (Part 3.6), and lives at `data_room/`. `generate.py --seed 20261024` runs one simulation (`src/facts.py`) and writes every file from it. Each plant is one function that takes a true fact, returns the shown value, and records where it wrote it. `--no-plants` writes a room that reconciles everywhere. Output: `data_room/hollis_voice/` (the full room) and `data_room/hollis_voice_seed_drop/` (the thin first tier). Both rooms also hold `01_overview/claims.json`, the deck's claims page (slide 14) as data, written from the same list, so the claims can be read when PDF text extraction fails.

The answer key, `data_room/answer_key.json`, sits outside both room folders so Tricorder is never pointed at it. It holds the 8 planted entries and the 3 decoys, each with its locations, the true value, the shown value, the check name and the tolerance (data room research, Part 3.6). The check names are the red-flag engine's check names, fixed this week in [FRAMEWORKS.md](FRAMEWORKS.md).

**How the test compares.** `eval/score.py <room>` reads `out/<room>/readout.json` and the answer key. A planted entry counts as found when a readout claim with severity `flag` has the key's check name and cites at least one of the key's files. A decoy counts as wrongly flagged when a `flag` claim cites the decoy's file and location. It prints found of 8 and decoys flagged of 3, and the page shows that score. The data room research expects 5 entries from the seed drop and the other 3 from the full room (Part 3.4). The red-flag engine's own test in `scans/redflags/tests/` runs the same comparison on that scan alone.

## Steering the readout (after Saturday)

The readout is a working surface. The operator can steer a piece with a comment or a short instruction ([writers' brief, 1:12 PM block](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). A steer is one of two kinds: rewrite the piece from what it already read, or get more info for it by reading new sources.

```python
class Steer(BaseModel):
    piece: Literal["traction_and_revenue", "retention", "burn_and_runway", "unit_economics", "customers", "market", "comps", "team", "the_pitch_itself"]
    kind: Literal["rewrite", "more_info"]
    instruction: str         # "treat the pilot as non-recurring", "read the full room"
    at: str                  # ISO time the operator gave it

class PieceRevision(BaseModel):
    steer: Steer
    before: Piece
    after: Piece
    claims_added: list[str]      # for more_info, the claims from the new sources, marked new on the page
    sources_added: list[str]     # files or URLs read for the first time
    claims_dropped: list[str]
    verdict_moved_by: list[str]  # claim ids that changed the verdict; empty if it did not move
```

How a steer runs:

1. The server takes the Steer and looks up which entries feed that piece, from the piece table in [FRAMEWORKS.md](FRAMEWORKS.md) ("Piece verdicts").
2. For a **rewrite**, those scans rerun on that piece's inputs only. The instruction goes to their model readings as one more input. The scripts rerun as they are, so a script's number comes out the same.
   For **more info**, the server first fetches or opens the new sources the instruction names, under the same rules as any input: official APIs and saved pages, nothing scraped against a site's terms, nothing kept beyond the readout and its sources. Examples: the full room instead of the seed drop, another filing from EDGAR, a competitor's pricing pages. Then those scans run on the piece's inputs plus the new sources. A source that cannot be opened becomes a gap that says why.
3. The memo rebuilds that piece and the top green and red flags, by the same script rules.
4. The new Piece replaces the old one. `readout.json` keeps every PieceRevision, and the page shows the diff: claims added (marked new when they come from new sources), claims dropped, wording changed, and the verdict before and after with the claims that moved it.

A steer can change what is read, how claims are grouped and how they are worded. An instruction that asks for a different number from a script is not carried out; the revision says so in one line, and the script's number stays.

## Contracts as an input

Customer contracts arrive with the room or on their own. A folder that holds only contracts is a valid room. The model reads each contract's terms (length, notice and cancellation period, auto-renewal, pilot terms and any duty to convert, price, payment terms and clauses such as change of control), and each term is a claim that quotes its clause. A script then compares the terms with how each customer is counted in ARR, MRR, concentration and the model's revenue. The model never decides a number is wrong. The rules are [FRAMEWORKS.md](FRAMEWORKS.md), entry 1.13. On Saturday a model reads only the pilot clause, in the redflag-readings slice, and only if that slice is kept. The full entry is the [contract-terms](ROADMAP.md#contract-terms) slice.

## The progressive readout (after Saturday)

Every scan starts the moment the inputs it needs exist ([writers' brief, 2:19 PM block](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). A small scheduler watches the company's folder. When a file lands, it starts every scan whose needs are now met and that has not run on those inputs: the outside-world scans on the company's name, the deck scan on the deck, the model checks when the model arrives. Each finished ScanResult triggers a fresh merge, so the readout fills in as results land. Pieces still missing inputs carry `status: waiting_on_input` and name the input, which also goes on the ask list. A scan reruns only when one of its own inputs changes. This is the [inbound-unasked](ROADMAP.md#inbound-unasked) slice.

## Checklist coverage (after Saturday)

[CHECKLIST.md](CHECKLIST.md) and its [checklist.csv](checklist.csv) list every item a first pass looks for, with the stage it is expected at and the FRAMEWORKS entry that checks it. The merge reads the CSV, takes the company's stage (from the deck's round slide, changeable by the operator), and marks each item expected at that stage as found, checked or missing. The counts come from that script. Missing items feed the ask list as above. This is the [checklist-coverage](ROADMAP.md#checklist-coverage) slice.

## The memo export, reader copies and scenarios (after Saturday)

**The export.** `memo/` turns a readout into a draft memo in the sections and order of [MEMO_TEMPLATE.md](MEMO_TEMPLATE.md). Each line is one of the template's line kinds (claim, reading, gap, operator, scenario) and keeps the claim ids behind it. The quote checker runs again on export. It writes two forms from the same data:

- **The interactive memo.** A page that reads top to bottom like a memo. From any line, one click opens its claims; from a claim, one more opens its source and the sources that agree or disagree, using the same drill-down as the readout page.
- **The static PDF.** The same sections, with every claim footnoted to its file, locator, quoted text and date read. It is made from the shared version only.

**Versions and overlays.** The operator's memo is the shared version. Each operator edit or steer makes a new numbered version with a change-log line. Each reader gets an overlay on one shared version: their own steers and their scenario inputs, stored apart from the shared version and never written into it. The reader's page is the shared version with their overlay applied, and it says which version it started from.

```python
class ReaderOverlay(BaseModel):
    reader: str
    base_version: int
    steers: list[Steer]              # same Steer as the readout's
    scenario_inputs: dict[str, float | bool]  # e.g. {"pilot_counts_as_arr": False, "monthly_churn": 0.02}
```

**Scenarios are recomputed by scripts.** A scenario input goes to the same scripts that rebuilt the numbers (the [financial-model](ROADMAP.md#financial-model) slice), which run on an in-memory copy of the room's rows. The room's files are never written; a test hashes them before and after. Each recomputed figure is a separate scenario value shown beside the company's figure and the rebuilt figure. It is never written into a Claim or a Piece, so it changes no verdict and no flag. This is the [memo-export](ROADMAP.md#memo-export) and [reader-scenarios](ROADMAP.md#reader-scenarios) slices.

## The bank check (after Saturday)

With the founder's consent, the company's bank account is connected through Plaid, the first banking connector ([writers' brief, 1:52 PM block](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). The founder signs in through Plaid Link, so the investor never sees the bank credentials. `scans/bank/` reads balances and transactions and runs three script checks: deposits against the revenue rows, outflows against the model's burn, and the balance against the model's cash. A model only sorts messy transaction descriptions. The bank counts as a source independent of the deck and the model, so a match corroborates and a difference contradicts. It finds differences in reporting, not fraud. Bank data is stored with the readout and deleted with it, and withdrawing consent deletes the connection and every transaction pulled. Plaid's Sandbox supports custom test users with configured accounts and transactions, so tests run on a recorded Sandbox response and CI never calls Plaid. This is the [bank-check](ROADMAP.md#bank-check) slice.

## Multiplayer (uncertain)

Ken is not sure this works ([writers' brief, 2:05 PM block](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). If an online check of how syndicate leads and angel groups split diligence says it is worth building, the shape is: one stored readout that several people work at once; each person claims checklist items or pieces; every steer, edit and finding carries its author; a co-investor sees only what the lead shares. Reader overlays stay private until shared. Nothing in the Saturday design depends on it. This is the [multiplayer](ROADMAP.md#multiplayer) slice.

## The inbox input (after Saturday)

The brief makes the inbox an input and recommends a forwarding address first, because it needs no OAuth review. The research gaps found that investors who write about it prefer a PDF in the inbox, and that early data rooms are mostly Google Drive folders ([research_gaps.md](../reports/20261022.02_research/research_gaps.md), section 3), which suits a forwarding address. The facts on each path below come from the three official pages named in the Sources line.

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
| `PLAID_CLIENT_ID`, `PLAID_SECRET` | The banking connector | After (bank-check) |
| `PLAID_ENV` | `sandbox` for tests and demos | After (bank-check) |

Nicrron's gateway is not in the stack. It is OpenAI-compatible ([research_landscape.md](../reports/20261022.02_research/research_landscape.md), Part 2), and we have not checked that it passes Anthropic's structured-output setting through.

## Model calls

**Anthropic's API with structured outputs.** Each prompt passes a JSON Schema in `output_config.format`, or a Pydantic class to `client.messages.parse(...)`, and reads `parsed_output` ([structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), via feasibility 1.10). Opus 5.5 does the red-flag reading and the memo pass; Haiku 5.5 does bulk classification. The feasibility research lists Opus 5.5 at $4 and $20 per million tokens in and out, and Haiku 5.5 at $0.10 and $0.50 for prompts up to 100,000 tokens.

**Citations cannot be combined with structured output.** The API returns a 400 when the citations feature is sent together with `output_config.format` (feasibility 1.8). So Tricorder does not use Anthropic's citations. Each claim carries its own quoted span and locator, and the quote checker confirms the span is really in the source. This also works for scans with no document behind them, such as comps and signals.

**Whisper runs locally through whisper.cpp.** ffmpeg makes a 16 kHz mono WAV, which is the only input whisper.cpp reads, and whisper.cpp returns segments with timestamps, running on the GPU through Metal on Apple Silicon (feasibility 1.5). The model then picks claims by segment id, so times are copied, not guessed. The API is the fallback only: OpenAI's docs show word and segment timestamps only for `whisper-1`, which is deprecated and shuts down 2027-02-26, and the recommended `gpt-transcribe` ($0.0045 a minute, files up to 25 MB) shows none (feasibility 1.5).
