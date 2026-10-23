# Prototype decision: requests to the founder

Prototype: [02_prototype/prototype.html](02_prototype/prototype.html), built by [spike/build_prototype.py](spike/build_prototype.py) from the real Brasswick readout (`TRICORDER_OUT_DIR=<scratch> python3 -m scans.redflags data_room/brasswick`, then `python3 -m scans.memo data_room/brasswick`) and the real draft module, `founder_requests/draft.py`. Every ask line, founder sentence and guidance block on the page is that module's output. Adding a file and the rerun are simulated on the page and labelled so.

Screenshots (Chromium, 2026-10-23), light and dark, desktop and phone: `02_prototype/proto_list_*`, `proto_draft_*`, `proto_added_*`.

## What it shows

1. The ask list, 32 lines on Brasswick, each with a checkbox, its founder words, its piece, chips for "Top N", "If you have it", "After the term sheet", and the readout's own reason marked "For you, not sent".
2. One click on a line's "Draft request" drafts a message for that line. The toolbar picks the top five, all required lines, all, or none, and "Draft request for N selected" drafts one message for the group.
3. The draft panel: To, Subject, an editable message, "Copy text", "Open in mail app" (a `mailto:` link), and a warning when the link is long.
4. "Add a file from the founder": pick the request the file answers, pick the file, add it. The simulated result says where it was saved, which scans ran again, and which ask line left the list.

## What trying it settled

- **One message per click, grouped by document.** Lines that share a guide (the six material-agreement lines) sit under one heading with the guidance once.
- **Default selection: the pinned top five.** On Brasswick: the hiring plan, the roadmap and demo, incorporation documents, IP assignments, board minutes.
- **The top-five draft is about 4,500 characters as a mail link,** above the 2,000 at which some mail apps cut a link. So "Copy text" is the primary button, and the mail link shows a warning past 2,000. The guidance stays in the message: it is the point of the feature.
- **The founder never sees the reason line.** The readout's `why` ("Not in the room: ... Also needed for C12.") is internal and stays on the operator's side.
- **Ask rows get no guide block.** Rows only the founder can answer (current burn, founder references) and C101 (patents; its guide is about invention assignments) carry a title and no guidance, because their guide describes a different document.
- **A synthetic room is never written.** The first file copies `data_room/<room>` to `rooms/<room>_live`.

## Persona review

**Limit: run by the builder in this session, not by independent persona subagents.** This session has no tool to start a subagent. I read `.claude/agents/persona-associate.md`, `persona-partner.md`, their PERSONAS.md sections and PERSONA_REVIEWS.md, then read the prototype screenshots as each persona. A builder knows what the page means, which is what a persona review is meant to get past, so the orchestrator should rerun both agents on the screenshots above. Findings are simulated judgment, not customer evidence.

### The associate who spends days gathering (primary)

**Verdict:** would use it on every room, because it turns the ask list into a sendable message in one step. **Rating:** workable.

- Works: one click from a line to a message with the form spelled out ("A CSV or a spreadsheet tab with one row per planned hire"). Fewer rounds of "that is not what we meant" is what kept a room from costing weeks. [Grounded: "It took us weeks to sift through the data", PERSONAS.md, associate, problem in their own words]
- Works: "For you, not sent" keeps the internal reason off the founder's screen. [Inferred]
- Stuck: lines 1 and 3 ask for monthly revenue by customer, and Brasswick's room already holds `revenue_by_customer.csv`. Sending that makes me look careless to the founder. [Grounded: "If it is wrong, I am the one who looks bad", PERSONAS.md, associate, objection]
- Stuck: the top-five draft is too long for the mail button, so the main path shows a warning. I would copy and paste into my mail anyway. [Inferred]
- Stuck: 32 lines with six "Material agreements" titles in a row is a lot to scan. [Inferred]
- Would change my mind: after adding a file, show me which scan ran and what changed in the readout, not only that the line left. [Inferred]

### The partner who finds the disagreement too late (primary)

**Verdict:** fine with it, as long as it never tips the founder off about a flag before the meeting. **Rating:** workable.

- Works: the message asks for documents and never states a finding. A request that names the disagreement gives the founder time to explain it away. [Inferred]
- Works: "After the term sheet" lines are off by default, so bank statements and tax returns are not asked for at the first pass. [Inferred]
- Stuck: nothing tells me which requests went out and which came back. [Inferred]
- Would change my mind: a record of requests drafted and files received per room. [Inferred]

### What I took and what I left

| Finding | Taken or left | Why |
|---|---|---|
| Show the scan that reran and the readout change after a file | Taken | The intake result returns the scans rerun, the item's checklist status before and after, and the ask count before and after (PRD FR-R13). |
| Lines that ask for a file already in the room | Left, raised | It comes from coverage's guide text for C14 and the deferred-revenue gap's `would_need`. Coverage's owner fixes it; see Attention needed in [00_progress.md](00_progress.md). |
| Long draft past the mail link limit | Taken in part | Copy is primary, the link warns. Shortening the guidance was rejected: the guidance is what the founder needs. |
| Many lines with one title | Left | The list follows the readout's order, which the coverage step owns. The draft groups them. |
| Record of requests and replies | Taken in part | Each received file is logged in `out/<room>/founder_requests.json`. Tricorder does not know whether a draft was sent, so drafts are not logged. |

## Prototype status

Throwaway. The real panel is `readout/src/FounderRequests.tsx`, built against the server routes, with the prototype as its UI baseline.
