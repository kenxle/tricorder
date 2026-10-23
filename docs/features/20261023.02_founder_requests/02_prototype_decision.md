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
- **Default selection: the pinned top five.** The first round picked the hiring plan, roadmap and closing paperwork; the persona review below changed the rule (FR-R25).
- **The first top-five draft was about 4,500 characters as a mail link,** above the 2,000 at which some mail apps cut a link. The fix round cut it under 2,000 (FR-R26); "Copy text" stays the primary button and the warning stays for long selections.
- **The founder never sees the reason line.** The readout's `why` is internal and stays on the operator's side, where it names items, not check codes.
- **Ask rows get no guide block.** Rows only the founder can answer (current burn, founder references) and C101 (patents; its guide is about invention assignments) carry a title and no guidance, because their guide describes a different document.
- **A synthetic room is never written.** The first file copies `data_room/<room>` to `rooms/<room>_live`.

## Persona review

**Independent.** The orchestrator ran `persona-associate` and `persona-partner` as subagents on 2026-10-23. Each read only PERSONAS.md and this feature's screenshots, prototype and copied draft text. Their full reports were not left in a shared folder; what follows is the orchestrator's relay of them, quoted where it quoted them. An earlier builder-run read of the same screenshots is replaced by this section. Findings are simulated judgment, not customer evidence.

**Both rated it "workable".** The mechanics are right: tick, draft, copy or mail link, add the reply, receipt. The email was not sendable as drafted.

### The associate who spends days gathering (primary)

- Stuck: the draft asked for files the room already holds. Line 3 (cohort: "send monthly revenue by customer") and line 1 ask for what `03_metrics/revenue_by_customer.csv` and `monthly_metrics.csv` already hold. Line 29 asks for consulting agreements though a contractor statement of work is in the room.
- Stuck: it asked twice. Material agreements (line 23) repeats lines 24, 25, 28 and 29; the equity lines (13, 17, 20) repeat the 409A and the grants.
- Stuck: the email was long and formal: "What it is", "Best form" and "A good one shows" for every item ("reads like grading homework"), no date, no sign-off, a subject that did not read like a person.
- Stuck: the add box sat under 32 lines, took one file at a time, and the receipt said "Scans that were waiting ran again: redflags".
- Stuck: internal codes in the operator's view ("Also needed for C12").

### The partner who finds the disagreement too late (primary)

- Stuck: "Top five" picked the roadmap, incorporation documents, IP assignments, board minutes and the hiring plan, and left out revenue by customer, retention and the monthly financials: the things that settle the decision.
- Stuck: formation, IP and minutes are closing paperwork at seed, like bank statements.
- Stuck: the prior financing guidance asked for "the term sheet for this round", which the fund writes.
- Stuck: line 12's title said customer letters of intent while the line asks for references from management, investors and advisors.
- Stuck: the trust line ("Tricorder never sends this") was in the prototype but not in the built drawer.

### What I took and what I left

| Finding | Taken or left | Where |
|---|---|---|
| Top five ranks what settles the decision first | Taken | Piece weight (traction and revenue, retention, burn and runway first), then a red flag or weak piece resting on the item. FR-R25. On Brasswick: revenue by customer, investor updates, the cohort export, monthly financial statements, the hiring plan. |
| Formation, IP and minutes after the term sheet at seed | Taken | FR-R24. Never in the default five. |
| Never ask for a file the room holds | Taken | Each line is checked against the room's files with coverage's own patterns (`scans.memo.checklist.match_document`, pattern only, unedited). A held line drops and is listed for the operator as "Not asked for"; the revenue line and the cohort line are reworded to what is still missing. FR-R22. |
| Never ask twice | Taken | Material agreements, option grants and 409A, and the reference lines each merge into one item; material agreements says "beyond the Norrgate Software Studio statement of work already in the room". FR-R23. |
| Line 12's title and fold with 9 and 11 | Taken | One item, "People we can call". |
| Shorter, warmer email | Taken | One plain line per item and one "Ideally it includes ..." line per kind of document; a date with a reason; a sign-off with name and fund; subject "Brasswick: a few things before our next meeting". The default five on Brasswick is 1,750 characters as a mail link from the command line with name and fund, 1,744 on the page; under 2,000. FR-R26. |
| Drop "the term sheet for this round" | Taken | Prior financing reads "Signed PDFs, one per investor." |
| Trust line in the built drawer, plain synthetic-room line | Taken | "Tricorder never sends this. Copy it, or open it in your own mail app and send it from there." and "This is a sample room, so the files go into a working copy of it." |
| Several files, one file for several lines, add box reachable | Taken | FR-R28. The add box sits beside the list on a wide screen and above it on a phone; the toolbar has "Add the founder's reply". |
| Receipt in plain words | Taken | FR-R27: what coverage now finds, claims, flags and verdicts that moved, or "No check reads this file yet, so no number changed." |
| Hide check codes | Taken | "Also needed for: <item names>." No check code appears in the panel's text (checked on the page). |
| Coverage's own ask list repeats and asks for held files | Left, raised | Coverage's ask list is the captain's. Note for its owner in [00_progress.md](00_progress.md). |
| "What it is" and "Best form" in the operator's view | Left | The operator view keeps the guide link under "Where the guidance comes from"; the list stays short. |

## Prototype status

Throwaway. The real panel is `readout/src/FounderRequests.tsx`, built against the server routes, with the prototype as its UI baseline.
