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
- **FR-R3.** Each document line carries guidance from its document guide (the checklist row's `guide` column): what the document is, the form that works best, and what a good one shows. Every guide the checklist names has guidance.
- **FR-R4.** Lines that share a guide appear under one heading in the message, with the guidance once.
- **FR-R5.** Lines marked "if you have it" go under "If you have them:", after the required lines.
- **FR-R6.** The subject, greeting and body contain no file path, cell reference, claim id, checklist id or the readout's internal phrases ("Not in the room:", "Also needed for"). Applies to every line on Brasswick and Hollis Voice.
- **FR-R7.** Every founder line is a full sentence that starts "Please", "Send" or "If" and ends with a full stop.
- **FR-R8.** The greeting uses the first name from the cover note's sign-off when there is one, else "Hello,". The company name comes from the deck's first line, else the room id. The draft says where it read them.
- **FR-R9.** The draft returns a `mailto:` link with the To, subject and body percent-encoded (spaces as `%20`, line breaks as `%0D%0A`), and whether it is at most 2,000 characters.
- **FR-R10.** Nothing is sent. No route or command opens a network connection or a mail client.

### Receiving

- **FR-R11.** A file is added for one named request (a checklist id, or the ask line's number, which resolves to its checklist id). An unknown request is refused.
- **FR-R12.** The file lands in the room's numbered folder for its item: the folder that already holds the item's documents; else the folder named for the item's piece (metrics, financials, contracts or customers, team, overview, legal); else a new folder with the next number.
- **FR-R13.** The file is saved under a name the scans and the coverage step recognise for that item (`hiring_plan.csv` for the hiring plan; a prefix from the coverage file patterns for other documents), so the item reads as found after the merge.
- **FR-R14.** The scans that were waiting run again: every built scan whose needs are met and whose last result did not list one of the room's current input files (or that has no result yet). Then the merge rebuilds the readout. The answer names the scans that ran, the item's coverage status before and after, and the number of ask lines before and after.
- **FR-R15.** Each received file is logged in `out/<room>/founder_requests.json`: when, the request, the original name, the saved path, its size and the scans rerun.

### Safety of the upload

- **FR-R16.** A room in `data_room/` is never written. Adding to it is refused with the command that copies it to `rooms/`. Copying never overwrites an existing room and never takes a name that a `data_room/` room has.
- **FR-R17.** The file name is reduced to its last path part, lower case letters, digits and underscores, at most 80 characters before the extension. A name that is empty, hidden (starts with a dot) or has a control character is refused.
- **FR-R18.** Only these kinds are accepted: PDF, CSV, XLSX, DOCX, PPTX, Markdown, text, JSON, PNG, JPEG, MP4. The bytes must match the kind (a PDF starts `%PDF-`; an Office file is a zip with `[Content_Types].xml`; text is UTF-8 with no NUL; JSON parses). A zip that would unpack past 100 MB is refused.
- **FR-R19.** A file over the size limit (25 MB, `TRICORDER_UPLOAD_MAX_MB`) or empty is refused before it is written.
- **FR-R20.** A file never overwrites another. The write is exclusive and does not follow links; the target must resolve inside the room.

### Page

- **FR-R21.** The readout page shows the panel: ask lines with checkboxes and per-line "Draft request", the draft with Copy and "Open in mail app", and "Add a file from the founder" with the result.

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
