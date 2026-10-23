# The roadmap, parted into Feature Forge features

Written 2026-10-22 by the "First roadmap features" thread. This page groups the product slices in [ROADMAP.md](../../ongoing/ROADMAP.md) into features that each go through Feature Forge once. It says which route each one takes, what it waits on, and the order agents pick them up. The roadmap stays the source for what each slice must include. This page only decides the order and the route.

## How a feature goes through the forge

The Feature Forge skills are installed in this repo at `.claude/skills/` (feature-forge, brief, architecture, plan, whetstone). Each feature gets a folder under `docs/features/` with these files, in order:

1. `00_progress.md`: what is true now, what needs Ken, the next step.
2. `01_brief.md`, with a `product_thinking.md` note: who it serves, the problem, the outcome.
3. `02_prototype/` for a feature people see, or `02_interface_example.md` for a scan. A scan's example is the real Claim JSON its spike prints on the data room, never typed by hand.
4. `03_prd.md`: requirements with stable IDs and failure cases.
5. `04_architecture.md`: inputs, data shapes, where it plugs in, alternatives.
6. `05_plan.md`: slices and the one verification table.
7. Then TDD on a branch, independent review, a PR to `main`.

Features people see get a persona review once the persona agents exist (the "Persona reviews" thread is building them) and follow the style guide once Ken picks one (the "Style guides and sample homepages" thread).

## The code layout every feature builds on

Set by the "Architecture and framework setup" thread, from the roadmap's skeleton slice. Scans are Python packages at the repo root under `scans/<name>/`. Shared types come from `schema/claim.py` (Source, Value, Check, Claim, Gap, Panel, ScanResult, Piece, TopFlag, AskItem, Readout). File readers are in `schema/readers.py`. A scan exposes `run(room_dir) -> ScanResult`, and each check returns a list of claims and a list of gaps. [ARCHITECTURE.md](../../ongoing/ARCHITECTURE.md) is the authority once that thread writes it.

## Wave 1: scans that need only the data room and the schema

These run on files already in `data_room/`. No API key, no host, no decision from Ken. They are the first features through the forge.

| Feature | Roadmap slice | Route | Lives in | Status |
|---|---|---|---|---|
| Deck revenue against the books | [deck-vs-books](../../ongoing/ROADMAP.md#deck-vs-books) | Prototype-first, interface example | `scans/redflags/deck_vs_books.py` | Merged in PR #4, 2026-10-23: [folder](../20261022.11_deck_vs_books/) |
| Accounting mislabels | [accounting-mislabels](../../ongoing/ROADMAP.md#accounting-mislabels) | Prototype-first, interface example | `scans/redflags/mislabels.py` | Merged in PR #4, 2026-10-23: [folder](../20261022.12_accounting_mislabels/) |
| Checklist coverage and the ask list | [checklist-coverage](../../ongoing/ROADMAP.md#checklist-coverage) | Prototype-first, clickable prototype | `scans/memo/coverage.py` | Merged in PR #4, 2026-10-23: [folder](../20261022.13_checklist_coverage/) |
| Tricorder's own financial model | [financial-model](../../ongoing/ROADMAP.md#financial-model) | Prototype-first, clickable prototype (the runway what-if) | `scans/model/` | Next |
| Business frameworks | [frameworks-scan](../../ongoing/ROADMAP.md#frameworks-scan) | Prototype-first, interface example | `scans/frameworks/` | Next, needs the Anthropic key |

Wave 1's first three features are closed out in [01_closeout.md](01_closeout.md).

## Wave 2: the readout as a product

These turn scan output into something the associate and the partner use. They wait on the readout store, and most have a screen, so they wait on the style guide too.

| Feature | Roadmap slices | Route | Waits on |
|---|---|---|---|
| Readout store and delete | [readout-store](../../ongoing/ROADMAP.md#readout-store) | Prototype-first, interface example | Skeleton |
| Steering in one sentence | [steering](../../ongoing/ROADMAP.md#steering) | Prototype-first, clickable prototype | Readout store |
| Contract terms in full | [contract-terms](../../ongoing/ROADMAP.md#contract-terms) | Prototype-first, interface example | Readout store |
| Claim support | [claim-support](../../ongoing/ROADMAP.md#claim-support) | Prototype-first, interface example | Checklist coverage, the pitch transcript |
| Requests to the founder | [founder-requests](../../ongoing/ROADMAP.md#founder-requests) | Prototype-first, clickable prototype | Checklist coverage |
| The memo and its PDF | [memo-export](../../ongoing/ROADMAP.md#memo-export) | Prototype-first, clickable prototype | Example readout files |
| Reader copies and scenarios | [reader-scenarios](../../ongoing/ROADMAP.md#reader-scenarios) | Prototype-first, clickable prototype | Memo, steering, financial model |
| First screens by stage | [stage-views](../../ongoing/ROADMAP.md#stage-views) | Prototype-first, clickable prototype | Readout store, outside-in |
| Video moments | [video-moments](../../ongoing/ROADMAP.md#video-moments) | Prototype-first, clickable prototype | Ken's recorded pitch video |

### Wave 2 status (2026-10-23)

Run by the "Wave 2 roadmap features" thread. Each feature went through the forge, got an independent persona review (associate and partner) where people see it, and one fix round. The independent code and security review ([review_wave2a.md](review_wave2a.md)) covered readout store, founder requests, contract terms and claim support; memo export and steering still need theirs (board row TRI-wave2-review-memo-steering). Closeout: [02_closeout.md](02_closeout.md). Each has a page in `.claude/skills/verify-tricorder/features/` and was driven once through `control.sh`.

| Feature | Folder | Code |
|---|---|---|
| Readout store and delete | [20261023.01](../20261023.01_readout_store/) | `store/`, `server/store_routes.py` |
| Requests to the founder | [20261023.02](../20261023.02_founder_requests/) | `founder_requests/`, `server/founder_requests_routes.py`, `server/local_guard.py`, `readout/src/FounderRequests.tsx` |
| The memo and its PDF | [20261023.03](../20261023.03_memo_export/) | `memo/`, `server/memo_routes.py` |
| Contract terms in full | [20261023.04](../20261023.04_contract_terms/) | `scans/redflags/contract_reader.py`, `contract_terms_full.py` |
| Steering in one sentence | [20261023.05](../20261023.05_steering/) | `steering/`, `server/steering_routes.py`, `scans/redflags/cohorts.py` (entry 1.3 script half), `readout/src/Steering.tsx` |
| Claim support | [20261023.06](../20261023.06_claim_support/) | `scans/claims/`, `scans/memo/claim_support.py` |

Still waiting: reader copies and scenarios (on the financial model), first screens by stage (on outside-in), video moments (on the recorded pitch video).

## Wave 3: the outside world

These read the web and the sponsor APIs. Each waits on Ken's keys (board row TRI-sponsor-keys) and, for real companies, his pick of YC companies (TRI-approve-yc).

| Feature | Roadmap slices | Waits on |
|---|---|---|
| Sponsor adapters | [sponsor-adapters](../../ongoing/ROADMAP.md#sponsor-adapters) | Nothing this week. Can start now |
| Saved outside data | [cached-data](../../ongoing/ROADMAP.md#cached-data), [signals-readings](../../ongoing/ROADMAP.md#signals-readings) | Keys, the YC pick |
| Comps in depth | [comps-deep](../../ongoing/ROADMAP.md#comps-deep) | Saved outside data |
| The associate's ten tabs | [outside-in](../../ongoing/ROADMAP.md#outside-in) | Keys |
| Founder profiles, online presence, reference checks | [founder-profiles](../../ongoing/ROADMAP.md#founder-profiles), [online-presence](../../ongoing/ROADMAP.md#online-presence), [reference-checks](../../ongoing/ROADMAP.md#reference-checks) | Outside-in, plus a terms check for GitHub and Reddit |

## Wave 4: inbox, bank and rooms, each gated on Ken

| Feature | Roadmap slices | Ken's part |
|---|---|---|
| Forwarded pitch emails, diligence before anyone asks | [inbox-forward](../../ongoing/ROADMAP.md#inbox-forward), [inbound-unasked](../../ongoing/ROADMAP.md#inbound-unasked) | Pick a domain and a mail service |
| Gmail and Outlook | [inbox-apis](../../ongoing/ROADMAP.md#inbox-apis) | Google's verification |
| Bank check | [bank-check](../../ongoing/ROADMAP.md#bank-check) | A Plaid developer account |
| Templated rooms | [room-templates](../../ongoing/ROADMAP.md#room-templates) | The YC pick, for the real-company rooms |
| Multiplayer | [multiplayer](../../ongoing/ROADMAP.md#multiplayer) | Marked uncertain by Ken |

## Not forged by agents

The team's Saturday slices (readers, claim-result, redflag-engine, readout, readout-page, pitch-video, contract-terms-saturday, comps, market-signals, demo-freeze) are built in the room on Saturday. The skeleton and saturday-specs belong to the architecture thread. Pilot and product are Ken's.

## Why this order

- Wave 1 needs nothing anyone is waiting on. The data room, the answer key and the FRAMEWORKS entries already exist, so a scan can be built and scored today.
- The three first features are all deterministic scripts. Principle 1 in the [product brief](../../ongoing/PRODUCT_BRIEF.md) says a script decides a number is wrong, so they carry the most trust per hour of work.
- Deck against books and the mislabels feed the traction and revenue piece, the weakest piece in [the one workflow we demo](../../ongoing/ROADMAP.md#the-one-workflow-we-demo). Coverage feeds the ask list, which every later feature in wave 2 uses.
