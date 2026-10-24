# Ken's asks and where they are built

Back to the [roadmap](../ROADMAP.md).

Every feature or behaviour Ken asked for on 2026-10-22, and the slice that builds it. "When it is built" names the horizon of each linked slice, in link order. A script checks that every link points at a slice file in this folder and that the horizons match: [check_asks_table.py](../../features/20261022.01_hackathon_plan/check_asks_table.py).

Five of the day's blocks are rules with nothing to build: the 1:21 PM block (no research labels in documents), the 1:24 PM block (say, do, pay is not user against buyer), the 1:12 PM rename to "the operator", the 2:35 PM block (the two primary personas are the associate who prepares the memo and the partner who reads it, at seed and Series A funds), and the 3:32 PM note (everything is built by the end of Saturday, and building starts now). The first three bind the documents. The fourth decides who every slice serves first. The last one sets this roadmap's two horizons.

| Ken's ask | Slice that builds it | When it is built |
|---|---|---|
| Red flags in the financials and metrics | [redflag-engine](redflag-engine.md) | Saturday |
| A memo where every claim links to its source | [claim-result](claim-result.md), [readout](readout.md) | Saturday |
| Market signals for the company and its competitors | [outside-in](outside-in.md), [market-signals](market-signals.md) | Now to Friday night, then Saturday |
| Competitive analysis | [market-signals](market-signals.md), [comps](comps.md) | Saturday |
| Comps, each with why it is a fair comp | [comps-deep](comps-deep.md), [comps](comps.md) | Now to Friday night, then Saturday |
| EDGAR full-text search for comps | [comps-deep](comps-deep.md) | Now to Friday night |
| Financial modeling | [financial-model](financial-model.md), [redflag-engine](redflag-engine.md) | Now to Friday night, then Saturday |
| A pitch video broken into claims with timestamps | [pitch-video](pitch-video.md) | Saturday |
| The video leads you to its interesting parts | [video-moments](video-moments.md) | Now to Friday night |
| Business frameworks: lean canvas, jobs to be done and the rest | [frameworks-scan](frameworks-scan.md) | Now to Friday night |
| Founder profiles: socials, GitHub, passion, from the industry or not | [founder-profiles](founder-profiles.md) | Now to Friday night |
| The company's presence online, including Reddit and Facebook | [online-presence](online-presence.md) | Now to Friday night |
| A Reddit mini-browser that saves each page Ken opens | [online-presence](online-presence.md) | Now to Friday night |
| The one-page founder brief | [founder-brief](founder-brief.md) | Now to Friday night |
| A simulated data room | [data-room](data-room.md) | Now to Friday night |
| Pull pitch decks out of the inbox | [inbox-forward](inbox-forward.md), [inbox-apis](inbox-apis.md) | Now to Friday night |
| Diligence starts on the inbound, before anyone asks | [inbound-unasked](inbound-unasked.md) | Now to Friday night |
| The investor can see and delete everything pulled | [readout-store](readout-store.md) | Now to Friday night |
| An overview of which pieces look strong and which look weak | [readout](readout.md), [readout-page](readout-page.md) | Saturday |
| Easy drill-downs to verify and corroborate every number | [readout](readout.md), [readout-page](readout-page.md) | Saturday |
| The readout opens on the best green flags and the worst red flags | [readout](readout.md), [readout-page](readout-page.md) | Saturday |
| The pitch line: "Point it at a startup, get a readout. Tricorder takes any data: decks, videos, spreadsheets, data rooms. It reveals insight you can trust, every claim sourced." | [demo-script](demo-script.md) | Now to Friday night |
| Real green flags in the demo room | [data-room](data-room.md) | Now to Friday night |
| Steer the readout by rewriting a piece | [steering](steering.md) | Now to Friday night |
| Steer the readout by getting more info for a piece | [steering](steering.md) | Now to Friday night |
| Angels want diligence and buy it by proxy | [product](product.md) | Now to Friday night |
| Accounting mislabels, not only ARR that is not recurring | [accounting-mislabels](accounting-mislabels.md), [redflag-engine](redflag-engine.md) | Now to Friday night, then Saturday |
| Find differences in reporting; never claim to catch fraud | [demo-script](demo-script.md), [bank-check](bank-check.md) | Now to Friday night |
| Online research only, no interviews | [research-gaps](research-gaps.md) | Now to Friday night |
| The same core job as the competitor, plus our extras | [product](product.md) | Now to Friday night |
| First screens that suit the company's stage | [stage-views](stage-views.md) | Now to Friday night |
| The operator can reorder the pieces | [stage-views](stage-views.md), [readout-page](readout-page.md) | Now to Friday night, then Saturday |
| The associate's ten tabs, opened automatically | [outside-in](outside-in.md) | Now to Friday night |
| Reference checks, low priority | [reference-checks](reference-checks.md) | Now to Friday night |
| A bank check through a banking connector | [bank-check](bank-check.md) | Now to Friday night |
| Contracts as an input, checked for gaps such as cancellation periods | [contract-terms-saturday](contract-terms-saturday.md) | Saturday |
| A list of things to ask the founder for | [readout](readout.md), [readout-page](readout-page.md) | Saturday |
| A diligence checklist | [checklist](checklist.md) | Now to Friday night |
| Coverage against the checklist, and an ask list from missing items at the company's stage | [checklist-coverage](checklist-coverage.md) | Now to Friday night |
| Help write the partners' memo: an interactive memo with drill-downs, plus a static PDF with footnotes, in a template built from real published memos | [memo-export](memo-export.md) | Now to Friday night |
| Each reader gets their own steerable copy of the memo, and can try what-if changes on the model, marked as scenarios | [reader-scenarios](reader-scenarios.md) | Now to Friday night |
| A blind room and a clean room against "rigged" | [blind-room](blind-room.md), [demo-freeze](demo-freeze.md) | Now to Friday night, then Saturday |
| Multiplayer: several people build one readout and split the work (uncertain) | [multiplayer](multiplayer.md) | Now to Friday night |
| Deck revenue against the P&L, and decks that show only part of the history | [deck-vs-books](deck-vs-books.md) | Now to Friday night |
| Speed: start every scan as early as its input exists, readout fills in as results land | [inbound-unasked](inbound-unasked.md) | Now to Friday night |
| Steering easy enough for a partner who runs diligence: one plain sentence on the line that looks wrong, no setup, the answer on that line | [steering](steering.md) | Now to Friday night |
| The claims workflow: extract claims from the deck and video, check whether the other documents support them | [claim-support](claim-support.md) | Now to Friday night |
| Templated data rooms with hidden issues, names swapped on the fly, one per problem story | [room-templates](room-templates.md) | Now to Friday night |
| A reference guide for every document a seed or Series A room can hold: green flags, red flags and pitfalls, and how Tricorder checks it | [checklist](checklist.md), [checklist-coverage](checklist-coverage.md) | Now to Friday night |
| Synthetic rooms for 2 or 3 real YC spring companies so the internet scan runs live | [yc-rooms](yc-rooms.md), [room-templates](room-templates.md) | Now to Friday night |
| Live demos on real YC companies from a list Ken approves, each paired with a fake data room | [yc-rooms](yc-rooms.md), [demo-script](demo-script.md), [market-signals](market-signals.md), [demo-freeze](demo-freeze.md) | Now to Friday night, then Saturday |
| The sponsor tools (Akta, Crunchbase, Nicrron) in the product, built ahead with keys plugged in on the day | [sponsor-adapters](sponsor-adapters.md) | Now to Friday night |
| Quick messages to the company asking for information, with guidance on what to submit | [founder-requests](founder-requests.md) | Now to Friday night |
