# Architecture

## Charter

**What belongs:** The shape of the system at a level a person can hold in their head. The stack and the folder structure. The surfaces people and agents touch, and the outside services behind them. The main models and how they relate, in outline.

**What does not:** How one feature works. That goes in a diagram or its own ongoing doc. How a feature got built. That stays in docs/features/.

**Level of detail:** A paragraph or a short table per area. Link out when a section passes three paragraphs.

**Describes:** the code root named in Settings

**Sources:** [PRODUCT_BRIEF.md](PRODUCT_BRIEF.md), [FEATURES.md](FEATURES.md) and [ROADMAP.md](ROADMAP.md) (every slice, both horizons), [FRAMEWORKS.md](FRAMEWORKS.md) ("How every entry works" and "The readout"), the feasibility research ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), Part 4.1 for the stack and Part 2 for the outside sources), the [guardrails](../../.claude/guardrails.md), the earlier draft of this doc (git, commit 2c75f59), and the code on `main`. Where this doc and the code differ, the code is right and this doc is out of date.

## The shape in one paragraph

Tricorder is a set of Python scans that each read a company's files and write one JSON file of claims, a merge that turns those files into one readout, a small server that hands the readout to a web page, and the page. Every number a scan writes is a script's. A model only reads words, and every claim it writes carries the exact quote it relied on, which a script then finds again in the source. The readout is built only from claims, so every line on the page is two clicks from its source. The diagram is [diagrams/system.md](diagrams/system.md).

## The stack

**Moving to TypeScript.** Ken decided on 2026-10-24 at 11:00 AM to port Tricorder to TypeScript, with a React web app and a React Native app on one shared core. Ben builds it: [typescript-port](roadmap/typescript-port.md). Until the port scores the same on every answer key, the Python stack below is what runs.

| Layer | What | Why |
|---|---|---|
| Scans, merge, scoring | Python 3.11+, Pydantic, pandas, openpyxl, pdfplumber, the Anthropic SDK | The scans are Python-shaped (spreadsheets, PDFs, whisper, the model). The feasibility research recommends it (Part 4.1). |
| Server | FastAPI on uvicorn, `server/app.py`, localhost only. `server/local_guard.py` refuses a non-loopback Host, a cross-origin write and a text or form body on a JSON route. Each feature's routes live in `server/<feature>_routes.py`, included above the page mount. | The page reads JSON and never waits on Python. |
| Page | React 19, TypeScript, Vite, in `readout/` | The frontend works in parallel against generated types and sample files. No CDN, so the demo needs no wifi. |
| Store | Files: `out/<room>/` for results, `rooms/` for rooms that arrive by upload or the inbox, and `store_data/` for readouts saved per fund (`store/`, `python -m store`) | One laptop on Saturday. The store keeps each saved readout with its sources and files, lists what a fund holds for a company, and deletes it all with one confirmed command. |

Rejected: one Streamlit app (no room for the frontend role, and a prior financial-AI hackathon disqualified "Simple Streamlit only applications"), and Rails with Python subprocesses (two runtimes on the demo laptop, one bottleneck).

The web package also pins `@tanstack/intent` as development tooling for discovering agent skills in installed npm dependencies. Setup runs from `readout/`. No current dependency ships Intent skills, so no managed agent guidance has been generated. Commands live in [TESTING.md](TESTING.md#intent-agent-guidance).

## Folder layout

Each folder has one owner, so parallel pull requests do not touch the same files. Owners match the roadmap's "Who owns what"; the roadmap wins if they differ.

| Folder | What it holds | Owner on Saturday |
|---|---|---|
| `schema/` | `claim.py` (the models), `claim.schema.json` and `ts/claim.ts` (generated), `readers.py` (open a file at a locator), `check_quotes.py`, `settings.py` (the thresholds) | captain; `readers.py` backend-and-data |
| `scans/base.py` | The scan command line, result paths, ids, gaps, the input kinds a room holds | captain |
| `scans/redflags/` | Scan 1: one module per FRAMEWORKS entry 1.1 to 1.14 (1.14 is deck against the books). `contract_reader.py` is the one contract reader for entry 1.13. Each module numbers its own claims (`redflags-<module>-001`), and a module that crashes becomes a gap. | design-and-finance |
| `scans/comps/` | Scan 2: public comps and private rounds | design-and-finance |
| `scans/signals/` | Scan 3: market signals, from `cache/` | frontend on Saturday |
| `scans/video/` | Scan 4: transcript claims with timestamps, interesting moments | backend-and-data |
| `scans/claims/` | The claims workflow: every figure in the deck and the pitch script, labelled supported, contradicted or unsupported against the room | agent |
| `scans/readings/`, `scans/model/` | Model readings (pilot clause, cohort note); the model rebuild, unit economics and scenario numbers | backend-and-data; agent |
| `scans/frameworks/`, `scans/founders/`, `scans/presence/`, `scans/outside/` | Scans 5, 6 and 7, and the associate's ten tabs | agent |
| `scans/bank/` | The bank check | agent |
| `scans/memo/` | The merge and its steps: linking, claim support, piece verdicts, top flags, coverage, ask list, connecting sentences | captain |
| `clients/` | `llm.py`, the one door to the model; one module per outside source, each with off, sample and live modes | backend-and-data |
| `server/` | The FastAPI app | backend-and-data |
| `readout/` | The page | frontend |
| `eval/` | `score.py`: a readout against an answer key | captain |
| `memo/`, `inbox/`, `store/` | The memo export (built; reader copies not yet), the inbox webhook (not built), the readout store (built) | agent |
| `founder_requests/` | The request to the founder drafted from the ask list, and a reply's files added to the room so the waiting scans rerun | agent |
| `steering/` | One typed sentence on a piece or a line: the engine and the revisions; verdicts and headline flags use the shared merge steps | agent |
| `data_room/` | The generator, the synthetic rooms and their answer keys. No product code imports it. | agent |
| `cache/` | Outside data saved ahead, indexed by `cache/index.json` | agent |
| `sample_out/` | Hand-written example results, one folder per room | captain |
| `out/`, `rooms/` | Scan results and arriving rooms. Ignored by git. | nobody |
| `bin/` | `ci-py`, `ci-web`, `smoke`, `serve` | captain |

Each scan keeps its tests in `scans/<name>/tests/` and its prompts in `scans/<name>/prompts/`, so no shared folder collects edits.

## The Claim schema

`schema/claim.py` is the one place a field is defined. It follows the JSON Schema in [FRAMEWORKS.md](FRAMEWORKS.md) ("The shared Claim") field for field; if they ever differ, FRAMEWORKS wins and the code changes. `python -m schema.export` writes the JSON Schema and the page's TypeScript types from it, and a test fails when either is stale.

| Model | What it is |
|---|---|
| `Source` | Where a claim comes from: a file path, URL or API call, a locator, and the exact quote. |
| `Value` | A number with a unit, a label from a fixed list, and a period. The fixed label is how the merge matches the deck, the model and the video. |
| `Check` | Script or model, and the check name from FRAMEWORKS. |
| `Claim` | One sentence the readout shows, its value, severity, confidence label and at least one source. |
| `Gap` | Something not in the room: what, why, what would close it, and the piece it feeds. A missing input is a gap, never a claim. |
| `ScanResult` | What a scan writes: its claims, gaps and optional panels. |
| `Piece`, `TopFlag`, `AskItem` | The readout's overview rows, headline flags and ask list. |
| `Steer`, `PieceRevision` | One plain sentence from the operator, and the before and after it produced. |
| `Readout` | `out/<room>/readout.json`: everything the page renders, in the order it shows it. |

Confidence is a label, never a probability: `computed` (a script recomputed it), `quoted` (a model read it and the quote was found), `judged` (a model read past the words; the text starts "Reading:"), `unverified` (the quote was not found; the claim goes to the "could not verify" box).

## The scan interface

| Part | Rule |
|---|---|
| Code | `scans/<name>/scan.py` defines `NAME`, `NEEDS` (input kinds from `scans.base.INPUT_KINDS`) and `run(room_dir) -> ScanResult` |
| Command | `python -m scans.<name> <room_dir>`, through `scans.base.main` |
| Output | `out/<room>/<name>.json` (`TRICORDER_OUT_DIR` moves it) |
| Inputs | Files in the room through `schema/readers.py`, saved copies in `cache/`, and outside calls through `clients/` only when `TRICORDER_OFFLINE` is unset. A room can be partial: a deck alone is a valid room. |
| Isolation | No scan imports another scan or reads another scan's output. Only the merge does. |
| Failure | A missing input or a refused call is a Gap and the scan exits 0. A crash exits non-zero. |
| Inside a scan | The order in FRAMEWORKS ("The order of work inside a scan"): script first, model second, quote checker third, the script sets the label and severity last. |

The red-flag engine is one scan made of many checks. Each FRAMEWORKS entry is its own module with `check(room, ids) -> (claims, gaps)`, listed in `scans/redflags/scan.py`. A listed module that does not exist yet is skipped, so parallel branches each add a file and nothing else.

## How the readout is built

`python -m scans.memo <room_dir>` reads every scan result that exists, runs the quote checker again, moves unverified claims to their own box, and turns each missing scan into a gap. Then it runs its steps in order, each a module in `scans/memo/` with `apply(readout, room_dir) -> Readout`, skipped until it exists:

1. **link**: claims with the same label, unit and period are linked as conflicting (apart by more than the tolerance) or corroborating (agreeing, from independent sources; the deck, video, overview, website and one-pager count as one source).
2. **claim_support**: each pitch figure the claims scan labelled is relabelled against other scans' flags (`scans/memo/claim_support.py`). A flag relabels a figure only when both carry a Value of the same label, unit and period.
3. **pieces**: each claim goes to one of nine pieces, and each piece gets its verdict by the script rule in FRAMEWORKS ("Piece verdicts"). Implemented in `scans/memo/pieces.py`, also used by steering.
4. **top_flags**: the best green and worst red flags, one per piece, by the rule in FRAMEWORKS. Implemented in `scans/memo/top_flags.py`, also used by steering. A red flag without comparable linked figures stays inside its piece.
5. **coverage**: each checklist item marked checked, found, missing, not checked yet or not expected at the company's stage, and an ask line for each missing item (`scans/memo/coverage.py`; [CHECKLIST.md](CHECKLIST.md), FRAMEWORKS "Checklist coverage").
6. **asks**: the ask list, from gaps, weak pieces and missing checklist items.
7. **connecting**: the one model pass. Each sentence must cite claim ids or it is dropped. It never changes a verdict.

The order of the pieces on the page is a view, not data. Reordering changes no verdict.

## Steering

The operator types one plain sentence on a piece or a line. The server classifies it as a rewrite (rerun the piece's scans with the sentence as one more input to their model readings) or a request for more information (fetch the sources it names under the same rules as any input, then rerun). The merge rebuilds that piece and the top flags by the same scripts and stores a `PieceRevision` with the diff. A steer can change what is read, how claims are grouped and how they are worded. It never changes a script's number; when asked to, the revision says so and the number stays. A steer that changes a definition ("treat the pilot as non-recurring") may add a new figure beside the check's, labelled as the steer's, and the check's own line stays. The code is `steering/` and `server/steering_routes.py` (`/api/rooms/<room>/steerable`, `/steer`, `/revisions`); a steer writes the readout back to `out/<room>/readout.json` with its `PieceRevision`, and saves it to the readout store as a new version, so every revision is kept. `python -m steering <room_dir> <piece> "<sentence>"` runs the same steer from the command line.

## Speed: the readout fills in as inputs arrive

Each scan declares the input kinds it needs. A small scheduler watches a company's folder; when a file lands it starts every scan whose needs are now met, and each finished result triggers a fresh merge. A piece still missing an input shows `waiting_on_input` and names it, and the input goes on the ask list. The outside scans start on the company name alone, before the data room is opened. This is the inbound-unasked slice; `scans.base.room_inputs` and `NEEDS` are its building blocks.

## Inputs beyond the room

| Input | How it arrives |
|---|---|
| Inbox | A forwarding address first: a mail service posts each message to a webhook in `inbox/`, which saves the attachments as a new folder in `rooms/` and starts the scans. Gmail's read scopes are restricted and need a security assessment; Microsoft Graph's delegated `Mail.Read` is the later path. Links that need a sign-in (DocSend) become gaps telling the operator what to do. |
| Bank | Plaid Link, with the founder's consent. Balances and transactions are a source independent of the deck and the model. Withdrawing consent deletes the connection and everything pulled. Tests run on recorded Sandbox responses. |
| Outside world | Official APIs and saved pages only, through `clients/`. Saved copies live in `cache/` with the time they were read, so the demo runs offline and every URL source can be quote-checked. |
| Requests to the founder | The ask list becomes a short message with guidance on what to submit (`founder_requests/`). The operator copies it or opens it in their mail app; Tricorder never sends it. A reply's files are added to the room through `/api/rooms/<room>/founder-requests/files`, and the scans whose inputs they meet run again. A sample room in `data_room/` is never written; the reply goes to a working copy, `rooms/<room>_live`. |

The full table of outside sources, their keys and their limits is in the feasibility research, Part 2. LinkedIn is never scraped; Reddit is read only from pages Ken saved by hand.

## The memo export, reader copies and scenarios

`memo/` turns a readout into a draft memo in the sections of [MEMO_TEMPLATE.md](MEMO_TEMPLATE.md): an interactive page with the same drill-downs as the readout, and a static PDF with every claim footnoted. Each operator edit makes a numbered version, marked as the operator's (`/api/rooms/<room>/memo/edits`). The page is `/api/rooms/<room>/memo.html` and the PDF `/api/rooms/<room>/memo.pdf`, built with reportlab. Reader copies and what-ifs are not built yet. Each reader gets a private overlay of their own steers and what-if inputs on one shared version. A what-if goes to the same scripts that rebuilt the numbers, on an in-memory copy of the room; the result shows beside the company's figure and the rebuilt figure and never changes a claim, a verdict or a flag.

## Answer keys and scoring

Each synthetic room has an answer key beside it in `data_room/`, outside the room folder, so no scan is ever pointed at it. Only `eval/score.py` and the tests read keys. A planted entry counts as found when a claim with severity "flag" has the key's check name and cites one of the key's files; a decoy counts against when a flag cites its file and location. `python -m eval.score <room>` prints found of planted and decoys flagged.

## Model calls

All model calls go through `clients/llm.py`: structured outputs only (a Pydantic class in, a validated instance out), the shared system prompt from FRAMEWORKS, Opus 5.5 for reading and the memo pass and Haiku 5.5 for bulk classification, each a setting. A gateway such as Nicrron's is a base URL setting, once someone checks it passes structured outputs through. Citations are not used, because the API refuses them together with structured output; the quote checker does that job. A refusal becomes a gap.

The pitch video is transcribed locally by whisper.cpp into `pitch_video.transcript.json` beside the video; the model picks claims by segment id, so times are copied, never guessed.

## Environment variables

Secrets come from the environment and are never committed. `.env.example` lists every variable.

| Variable | For |
|---|---|
| `ANTHROPIC_API_KEY` | Every model call |
| `TRICORDER_MODEL_READ`, `TRICORDER_MODEL_BULK` | Model routing; defaults `claude-opus-5-5` and `claude-haiku-5-5` |
| `TRICORDER_LLM_BASE_URL` | A model gateway, if used |
| `TRICORDER_OFFLINE` | `1` reads `cache/` and makes no outside calls |
| `TRICORDER_OUT_DIR` | Where results go; default `out/` |
| `TRICORDER_STORE_DIR`, `TRICORDER_CACHE_DIR` | The readout store (default `store_data/`) and the outside-data cache (default `cache/`) |
| `TRICORDER_ROOMS_DIR` | Where arriving rooms and working copies go; default `rooms/` |
| `TRICORDER_UPLOAD_MAX_MB` | The largest file a founder's reply may add; default 25 |
| `TRICORDER_OPERATOR_NAME`, `TRICORDER_FUND_NAME` | The sign-off on a request to the founder |
| `TRICORDER_OPERATOR` | Who a steer is credited to when the request names nobody |
| `TRICORDER_CONTRACT_READER` | `script` keeps entry 1.13 on the script reader even when a model reading is registered |
| `TRICORDER_SETTINGS` | A JSON file of threshold overrides |
| `WHISPER_CPP_BIN`, `WHISPER_MODEL_PATH` | The local transcriber |
| `EDGAR_USER_AGENT`, `AKTA_API_KEY`, `TAVILY_API_KEY`, `YOU_API_KEY`, `GITHUB_TOKEN`, `PRODUCT_HUNT_TOKEN`, `CRUNCHBASE_API_KEY`, `NICRRON_API_KEY`, `OPENAI_API_KEY` | Outside sources; each client falls back to sample mode without its key |
| `INBOUND_WEBHOOK_SECRET` | Checks that an inbound mail call came from the mail service |
| `PLAID_CLIENT_ID`, `PLAID_SECRET`, `PLAID_ENV` | The bank check; `sandbox` for tests and the demo |

## Running it

`bin/smoke <room_dir>` runs every scan that exists, then the merge. `bin/serve` starts the server on port 8787 and serves the built page; `bin/serve --dev` adds the page's dev server. The gates are in [TESTING.md](TESTING.md).
