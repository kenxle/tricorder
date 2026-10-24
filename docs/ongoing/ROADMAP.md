# Roadmap

What Tricorder builds next, and who builds it. Today is Saturday 2026-10-24. Hacking runs 10:30 AM to 4:30 PM, the demo freezes at 3:30 PM, and judging starts at 4:30 PM. The team is forming on site, so this page names roles; the [board](../BULLETIN.md) names the people behind each one.

**The framework:** every slice serves a step of the [demo workflow](diagrams/demo_workflow.md): a real list of YC companies, our own research, requests for the data room, red and green flags, the associate's steering, and the interactive memo for the principals.

## Charter

**What belongs:** The plan at a glance: what to build next and in what order, who builds it, what is built, and what waits on Ken. One line per slice.

**What does not:** A slice's detail. Each slice has its own file in [roadmap/](roadmap/), with what it includes and how we know it works; those files are the seeds of a brief. Work in flight lives on the [board](../BULLETIN.md). How the code fits together lives in [ARCHITECTURE.md](ARCHITECTURE.md).

**Status:** each slice's status is checked against the code and kept in [status.csv](roadmap/status.csv), one row per slice. [status_counts.py](roadmap/status_counts.py) counts them. Update the row when a slice moves.

## Up next: the demo path

Build in this order. The first three are the demo and are always shown. The rest follow the [demo fallback order](roadmap/saturday.md#demo-fallback-order) in reverse: if one is not working at the 2:30 PM fallback call, it shows saved results on stage, and it is still built.

| # | Slice | What is left to build | Who | Waits on |
|---|---|---|---|---|
| 1 | [redflag-engine](roadmap/redflag-engine.md) (partly built) | The red flags in the numbers: the planted-flag checks still missing (deck claims page, ARR definition, burn against the hiring plan, deck against model, customer concentration, gross margin, vanity metric, cap table and the green-flag cells) | design-and-finance | nothing; the readers and schema are built |
| 2 | [readout](roadmap/readout.md) (partly built) | Link sources across claims, build the ask list, and the model pass that writes connecting sentences | captain | redflag-engine for real output; builds on saved output until then |
| 3 | [readout-page](roadmap/readout-page.md) (partly built) | The page judges see: the claims and cohort panels, the memo link, the video jump, the ask-list copy button, the reorder buttons | frontend | readout |
| 4 | [pitch-video](roadmap/pitch-video.md) (not started) | Transcribe the pitch video and pull its claims with timestamps | backend-and-data | Ken's recorded video (record-pitch-video); the script works until then |
| 5 | [contract-terms-saturday](roadmap/contract-terms-saturday.md) (not started) | The model reading of the contracts, and contract checks 2 and 5 | backend-and-data | pitch-video comes first in that role's day |
| 6 | [claim-result](roadmap/claim-result.md) (partly built) | Check web sources against their saved copies | captain | cached-data |
| 7 | [cached-data](roadmap/cached-data.md) (not started) | Save every outside call under `cache/` so the demo runs without the network | agent | Ken's keys |
| 8 | [comps](roadmap/comps.md) (not started) | The comparable-companies panel | design-and-finance | cached-data |
| 9 | [signals-readings](roadmap/signals-readings.md) (not started) | The saved market-signal readings | agent | cached-data |
| 10 | [market-signals](roadmap/market-signals.md) (not started) | The market-signals panel and its live run on the real company | frontend | signals-readings |
| 11 | [outside-in](roadmap/outside-in.md) (not started) | The outside-world tabs for the real company's live beat: website, Hacker News, App Store, SEC filings | agent | Ken's pick of YC companies (yc-rooms), Ken's keys |
| 12 | [demo-freeze](roadmap/demo-freeze.md) (partly built) | Frozen outputs in `demo/frozen/`, the 3:30 PM tag, the rehearsal | captain | everything above; starts at 1:00 PM |

**Due at 11:00 AM:** the first social post for the $150 social content prize. An agent drafts both posts ([social-posts](roadmap/social-posts.md)) and Ken posts at 11:00 and 3:30.

## Ben: the TypeScript port

Ken decided at 11:00 AM: Tricorder moves to TypeScript, with a React web app and a React Native app sharing one core. Benjamin builds it. The Python version keeps running the demo until the TypeScript one scores the same on every room's answer key.

| Slice | What is left to build | Who |
|---|---|---|
| [typescript-port](roadmap/typescript-port.md) (not started) | The shared TypeScript core (schema, readers, scans, merge, scoring), the React web app and the React Native app | Benjamin |

## After the demo path

Everything on the roadmap is built today. Agents take these once the demo path is covered, in this order. Each joins the demo at an integration point and shows its last passing run if it is not live.

| Slice | What is left to build | Who |
|---|---|---|
| [sponsor-adapters](roadmap/sponsor-adapters.md) (not started) | One adapter per sponsor (Akta, Crunchbase, Nicrron), keys arrive today | agent |
| [saturday-specs](roadmap/saturday-specs.md) (partly built) | Example result files in sample_out/, the static readout mock, one test call per schema | agent |
| [room-templates](roadmap/room-templates.md) (not started) | Templated data rooms: swap a company profile in on the fly | agent |
| [frameworks-scan](roadmap/frameworks-scan.md) (not started) | Lean canvas and the other frameworks as one prompt and schema each | agent |
| [comps-deep](roadmap/comps-deep.md) (not started) | Form D and EDGAR comps in depth | agent |
| [financial-model](roadmap/financial-model.md) (not started) | Tricorder's own rebuilt model the operator can work in | agent |
| [video-moments](roadmap/video-moments.md) (not started) | The strip of moments on the video player | agent |
| [checklist-coverage](roadmap/checklist-coverage.md) (partly built) | The coverage panel on the readout page, the register of the guides' proposed checks | agent |
| [claim-support](roadmap/claim-support.md) (partly built) | Ken's call on figures only the company's model states, the video transcript waits on the recorded video | agent |
| [reader-scenarios](roadmap/reader-scenarios.md) (not started) | Each memo reader gets their own copy to steer and can try what-ifs on the financial model | agent |
| [bank-check](roadmap/bank-check.md) (not started) | The Plaid sandbox bank check | agent with Ken for Plaid |
| [founder-profiles](roadmap/founder-profiles.md) (not started) | A card per founder from GitHub, personal sites and talks | agent |
| [online-presence](roadmap/online-presence.md) (not started) | The company's footprint: web, Hacker News, Product Hunt, app stores, Reddit pages Ken saves | agent |
| [reference-checks](roadmap/reference-checks.md) (not started) | Prepare the operator's reference calls (low priority: Ken is not sure Tricorder can take this on) | agent |
| [stage-views](roadmap/stage-views.md) (not started) | First screens that suit the company's stage | agent |
| [inbox-forward](roadmap/inbox-forward.md) (not started) | A forwarding address such as deals@ that starts a readout | agent |
| [inbound-unasked](roadmap/inbound-unasked.md) (not started) | Diligence that starts on the inbound email before the investor asks | agent |
| [inbox-apis](roadmap/inbox-apis.md) (not started) | Gmail and Outlook connected through their official APIs | agent with Ken for Google's verification |
| [multiplayer](roadmap/multiplayer.md) (not started) | Several people build the same readout at once (uncertain: Ken is not sure this works) | agent |

## Waiting on Ken

- [keys](roadmap/keys.md): Put the API keys in `.env` on the demo laptop.
- [yc-rooms](roadmap/yc-rooms.md): Pick the real YC companies for the live beat. An agent then builds their synthetic rooms.
- [record-pitch-video](roadmap/record-pitch-video.md): Read each room's pitch script into a video, flatly.
- [founder-brief](roadmap/founder-brief.md): Edit the one-page founder brief in your own words. It is what the judges get.
- [demo-script](roadmap/demo-script.md): Read the three-minute core aloud against a timer.
- [pilot](roadmap/pilot.md): Find one fund to use Tricorder on real inbound deals.
- [product](roadmap/product.md): What makes Tricorder a product: the fund buys, the associate uses.
- [Proposals waiting on Ken](roadmap/proposals.md): which Startup Due Dil ideas to adopt.
- The defaults the orchestrator chose while Ken was away: board tasks TRI-wave1-defaults (deck-against-books and checklist-coverage defaults) and TRI-wave2-defaults (seven defaults, including whether a figure only the company's own model states counts as support).
- [blind-room](roadmap/blind-room.md): find the person outside the build who picks the variant room's flags and seals its key.

## Built

- [data-room](roadmap/data-room.md).
- [research-gaps](roadmap/research-gaps.md).
- [skeleton](roadmap/skeleton.md): merged in PR #2.
- [checklist](roadmap/checklist.md).
- [skeleton-card](roadmap/skeleton-card.md).
- [readout-store](roadmap/readout-store.md): merged in PR #8.
- [steering](roadmap/steering.md): merged in PR #8.
- [accounting-mislabels](roadmap/accounting-mislabels.md): merged in PR #4.
- [deck-vs-books](roadmap/deck-vs-books.md): merged in PR #4.
- [contract-terms](roadmap/contract-terms.md): merged in PR #8.
- [founder-requests](roadmap/founder-requests.md): merged in PR #8.
- [memo-export](roadmap/memo-export.md): merged in PR #8.
- [readers](roadmap/readers.md): merged in PR #2.

## Today

The full run of show, with every role's column, is in [saturday.md](roadmap/saturday.md#run-of-show). Who owns which folders: [saturday.md](roadmap/saturday.md#who-owns-what). The readers and the quote checker were built ahead in the skeleton, so the 10:30 hours planned for them go to the next item on the demo path.

| Time | What happens |
|---|---|
| 10:30 to 11:30 | Captain: claim-result. Frontend: readout-page. Backend-and-data: readers. Design-and-finance: redflag-engine. Captain posts at 11:00. |
| 11:30 | **Integration 1:** readers and the quote checker merged. |
| 11:30 to 12:30 | Captain: readout. Frontend: readout-page. Backend-and-data: pitch-video. Design-and-finance: redflag-engine on the deck and the seed drop. |
| 12:30 to 1:00 | Lunch at desks. |
| 1:00 to 1:30 | **Integration 2:** the first end-to-end run on the seed drop. |
| 1:30 to 2:30 | Captain: readout verdicts, flags, ask list, then the score script. Frontend: source panels and video jump. Backend-and-data: pitch-video. Design-and-finance: the clean room, then comps. |
| 2:30 | **Fallback call:** whatever is not producing claims shows saved results on stage. |
| 2:30 to 3:30 | Captain: demo-freeze. Frontend: page polish and market-signals. Backend-and-data: contract-terms-saturday. Design-and-finance: comps. |
| 3:30 | **Demo freeze:** tag `demo-freeze`. Captain posts again. The outside person sends the variant room's key. |
| 3:30 to 4:30 | All four rehearse, twice, one run on the backup laptop. Fresh runs on the variant and clean rooms. |
| 4:30 to 6:00 | Judging, then every team's demo and the winner. |

## More

- [How to read a slice file](roadmap/how_to_read.md), and the roadmap's first charter with its sources.
- [Ken's asks and where they are built](roadmap/asks.md): every feature Ken asked for, and the slice that builds it.
- [Saturday](roadmap/saturday.md): the window, who owns what, the demo laptop, the run of show and the demo fallback order.
- [The demo](DEMO.md): the rooms, the beat sheet, what runs live, the fallbacks.
- [Now to Friday night](roadmap/before_saturday.md): the first horizon's notes from before today.
- [The one workflow we demo](roadmap/demo_workflow.md): the roadmap's earlier write-up of the demo's shape.
