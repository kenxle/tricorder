# PRD: requests to the founder

Context: [01_brief.md](01_brief.md), [product_thinking.md](product_thinking.md), the prototype and its review in [02_prototype_decision.md](02_prototype_decision.md). Roadmap slice: [founder-requests](../../ongoing/ROADMAP.md#founder-requests).

## Problem, user, context

The associate has an ask list and needs the founder to send what is missing, in a form the scans can read. Sending means rewriting each line for the founder; receiving means saving files into the room and rerunning scans by hand.

## Scope

In: drafting a message from any ask line or group of lines; guidance from the document guides; copy and `mailto:`; adding a reply's file to a room under `rooms/` through a route and a CLI; rerunning the scans whose inputs changed, then the merge; the panel on the readout page.

Out: sending mail; reading the operator's mailbox (inbox slices); a model call; tracking whether a draft was sent; changing the ask list's own lines (coverage owns them); a schema change.

## Solution outline

`founder_requests/` holds three modules: `guidance.py` (one entry per document guide), `draft.py` (ask lines to a message) and `intake.py` (a file to the room, then the reruns). `server/founder_requests_routes.py` exposes them; `python -m founder_requests` is the CLI; `readout/src/FounderRequests.tsx` is the panel.

## Requirements

### Drafting

- **FR-R1.** Every ask line in the readout is listed with its number (its position in `readout.asks`, from 1), its founder words, its title, its piece, whether it is in the pinned top five, whether it is "if you have it", and its ask stage.
- **FR-R2.** A draft can be made for one line or any set of lines. With no lines named, the draft covers the pinned top five; with none pinned, every required line asked before the second meeting.
- **FR-R3.** Each document line carries guidance from its document guide (the checklist row's `guide` column). The operator's view links the guide. The founder's text carries one "Ideally it includes ..." line per kind of document (FR-R26). Every guide the checklist names has guidance.
- **FR-R4.** Lines that share a guide appear under one heading in the message, with the guidance once.
- **FR-R5.** Lines marked "if you have it" go under "If you have them:", after the required lines.
- **FR-R6.** The subject, greeting and body contain no file path, cell reference, claim id, checklist id or the readout's internal phrases ("Not in the room:", "Also needed for"). Applies to every line on Brasswick and Hollis Voice.
- **FR-R7.** Every founder line is a full sentence that starts "Please", "Send" or "If" and ends with a full stop.
- **FR-R8.** The greeting uses the first name from the cover note's sign-off when there is one, else "Hello,". The company name comes from the deck's first line, else the room id. The draft says where it read them.
- **FR-R9.** The draft returns a `mailto:` link with the To, subject and body percent-encoded (spaces as `%20`, line breaks as `%0D%0A`), and whether it is at most 2,000 characters.
- **FR-R10.** Nothing is sent. No route or command opens a network connection or a mail client.

### Receiving

- **FR-R11.** A file is added for one or more named requests (checklist ids, or ask line numbers that resolve to checklist ids, comma separated). The first decides where it lands. An unknown request is refused.
- **FR-R12.** The file lands in the room's numbered folder for its item: the folder that already holds the item's documents; else the folder named for the item's piece (metrics, financials, contracts or customers, team, overview, legal); else a new folder with the next number.
- **FR-R13.** The file is saved under a name the scans and the coverage step recognise for that item (`hiring_plan.csv` for the hiring plan; a prefix from the coverage file patterns for other documents), so the item reads as found after the merge.
- **FR-R14.** The scans that were waiting run again: every built scan whose needs are met and that has no result yet, or whose last result did not list a room input file written at or after its `ran_at` (a file it left out on purpose does not keep it waiting). Then the merge rebuilds the readout. The answer gives each file's saved path and each request's coverage status before and after, the number of ask lines before and after, and the plain-words summary of FR-R27.
- **FR-R15.** Each received file is logged in `out/<room>/founder_requests.json`: when, the request, the original name, the saved path, its size and the scans rerun.

### Safety of the upload

- **FR-R16.** A room in `data_room/` is never written. Adding to it is refused with the command that copies it to `rooms/`. Copying never overwrites an existing room and never takes a name that a `data_room/` room has.
- **FR-R17.** The file name is reduced to its last path part, lower case letters, digits and underscores, at most 80 characters before the extension. A name that is empty, hidden (starts with a dot) or has a control character is refused.
- **FR-R18.** Only these kinds are accepted: PDF, CSV, XLSX, DOCX, PPTX, Markdown, text, JSON, PNG, JPEG, MP4. The bytes must match the kind (a PDF starts `%PDF-`; an Office file is a zip with `[Content_Types].xml`; text is UTF-8 with no NUL; JSON parses). A zip that would unpack past 100 MB is refused.
- **FR-R19.** A file over the size limit (25 MB, `TRICORDER_UPLOAD_MAX_MB`) or empty is refused before it is written.
- **FR-R20.** A file never overwrites another. The write is exclusive and does not follow links; the target must resolve inside the room.

- **FR-R29. Only this machine's page can write.** Every route refuses a request whose Host is not loopback, a write whose Origin or Referer is another site, and a write whose body is not JSON, octet-stream or multipart. The upload reruns run off the server's event loop, and each log entry records the scans rerun and their result.

### Page

- **FR-R21.** The readout page shows the panel: ask lines with checkboxes and per-line "Draft request", the draft with the trust line ("Tricorder never sends this. Copy it, or open it in your own mail app and send it from there."), a date, name and fund, Copy and "Open in mail app", and "Add the founder's reply" with the result. No check code appears in the panel's text. The add box sits beside the list on a wide screen and above it on a narrow one.

### Fix round: what the persona review changed (2026-10-23)

- **FR-R22. Never ask for a file the room holds.** Each line's own document is checked against the room's files with coverage's file patterns (`scans.memo.checklist.match_document`, pattern only). A held line is dropped and listed for the operator as "Not asked for: the room already holds these". A line whose document is held but still lacks something is reworded to the missing part: the revenue line asks for the kind of revenue on each row and an MRR column; the cohort line asks for the cohort export behind the deck's retention figure.
- **FR-R23. Never ask twice.** Lines that ask for the same document merge into one item that keeps every line number: material agreements (C98 to C100, C110 to C114), option grants and 409A (C73, C78), and people we can call (C35, C46, C58, C97). Material agreements names a statement of work already in the room ("beyond the ... statement of work already in the room"). A merged item lists each request a reply's file can answer, by its plain name.
- **FR-R24. Closing paperwork waits at seed.** At pre-seed and seed, incorporation documents and bylaws (C74), IP assignments (C76) and board minutes (C77) are "After the term sheet" and never in the default five.
- **FR-R25. The top five is what settles the decision first.** From the lines asked before the second meeting, rank by the piece's weight (traction and revenue, retention, burn and runway, unit economics, customers, market, comps, team, the pitch itself), then lines a red flag or a weak piece rests on, then required before "if you have it", then line order. Take five.
- **FR-R26. The email is short and reads like a person.** Subject "<Company>: a few things before our next meeting" ("one thing" for one item). The body thanks them for the room, asks by a date with a reason ("before our partner meeting"; default a week from today, editable), says a rough version is fine, then one plain line per item and one "Ideally it includes ..." line per kind of document, and signs off with the operator's name and fund (`TRICORDER_OPERATOR_NAME`, `TRICORDER_FUND_NAME`, or the two fields). On Brasswick the default five fits a mail link (at most 2,000 characters).
- **FR-R27. The receipt says what changed in plain words.** For each request: "Coverage now finds <item>.", or that it moved, or that it is still missing. Then claims that changed (same id, new words, said in the new words), new or dropped claims, new or dropped flags and moved piece verdicts, each sentence once; a check that could not read the new file is said plainly; or "No check reads this file yet, so no number changed." Then the ask list's count, if it changed. No scan module names.
- **FR-R28. Several files in one add.** Every file is checked before any is written; one bad file refuses the whole add. The waiting scans run once and the readout is rebuilt once. One file may answer several requests.

## Failure cases

| Case | Behaviour |
|---|---|
| Readout has no ask lines | List is empty; drafting is refused with "Nothing to ask for." |
| Readout has no checklist ask-lines panel (coverage did not run) | Lines still list; covers and top five are empty; default selection is every required line. |
| A line has no checklist id (a future ask-list step line) | Founder words and title "Other"; no guidance. |
| Deck or cover note unreadable | Company is the room id; greeting "Hello,". |
| Upload to `data_room/<room>` | 409, with `python -m founder_requests copy-room data_room/<room>`. |
| Same file name already in the folder | 409; nothing written. |
| A scan crashes on the new file | The answer lists it as failed with the last lines of its error; the merge still runs on the results that exist. |
| No readout before the file | The "before" status is "unknown"; the merge builds one. |

## UX

The panel follows the prototype ([02_prototype_decision.md](02_prototype_decision.md)) in the readout's design language (`readout/src/tokens.css`). Copy is the primary action. The "For you, not sent" reason stays on the operator's side.

## Analytics and logging

No analytics. The received-file log (FR-R15) is the record.

## Rollout and flags

No flag. The routes are new and nothing calls them until the panel mounts.

## Questions

- **Ken: lines that ask for a file the room already holds.** On Brasswick, line 3 (coverage's C14 text) and line 1 (a deferred-revenue gap) both ask for monthly revenue by customer, which the room has. The fix belongs to coverage and the red-flag gap text, not here.
- **Ken: the `_live` suffix** for the working copy of a synthetic room. Default set; one constant.

## PM findings and dispositions

From the builder-run persona read (02_prototype_decision.md): result shows the rerun and the change (taken, FR-R14); record of replies (taken as FR-R15); long mail link (copy primary, warning, FR-R9).
