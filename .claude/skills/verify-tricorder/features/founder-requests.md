# Requests to the founder

From the readout's ask list, the operator drafts a plain-words message to the founder for one line or a ticked group, with guidance on what to send for each document (what it is, the best form, what a good one shows). They copy it or open it in their own mail app; Tricorder sends nothing. When the founder replies, the operator adds each file for the request it answers: it lands in the right numbered folder of a room under `rooms/`, the scans that had not seen it run again, and the readout is rebuilt.

## Sub-features

- `fr-list` lists every ask line with its founder words, title, piece, "Top N", "If you have it" and "After the term sheet".
- `fr-draft` drafts one message for one line or many, grouped by document, with guidance, a greeting from the cover note and the company from the deck.
- `fr-copy-mailto` gives the text to copy and a `mailto:` link, with a warning past 2,000 characters.
- `fr-no-leak` keeps file paths, cell references, claim ids and checklist ids out of the founder's text.
- `fr-copy-room` copies a synthetic room to `rooms/<room>_live`, because `data_room/` is never written.
- `fr-add` saves a reply's file under a name coverage recognises, reruns waiting scans, rebuilds the readout, and logs the receipt.
- `fr-refuse` refuses bad names, kinds, sizes, links, overwrites, and any write into `data_room/`.

## How to get to it (user POV)

- Command line: `python3 -m founder_requests list|draft|copy-room|add <room> ...`.
- API: `GET /api/rooms/<room>/founder-requests`, `POST /api/rooms/<room>/founder-requests/draft` with `{"numbers": [...], "to": "..."}`, `POST /api/rooms/<room>/founder-requests/copy` with `{}`, `POST /api/rooms/<room>/founder-requests/files?answers=<C22 or line number>&name=<file name>` with the raw file as the body, `GET /api/rooms/<room>/founder-requests/received`.
- Page: the section `aria-label="Requests to the founder"` under the ask list: checkboxes `Select line N`, buttons `Draft request for N selected` and `Draft request for line N`, the drawer `aria-label="Draft to the founder"` with `Copy text` and the link `Open in mail app`, and the block `aria-label="Add a file from the founder"` with `This file answers`, `File` and `Add to the room`. The result is the list `aria-label="What happened"`.

## Driving it with control.sh

Preconditions:

- `control.sh doctor` prints `OK` for this run.
- No folder `rooms/brasswick_live` exists in the checkout. If one does, pick another copy name (`copy-room --as`, or `{"name": "..."}` on the copy route) and use it below.
- `readout/dist/` was built from this checkout after the panel landed (`bin/ci-web`), or the page has no panel.

- **Build the readout.** Run `control.sh cli python3 -m scans.redflags data_room/brasswick`, then `control.sh cli python3 -m scans.memo data_room/brasswick`. Both exit 0.
- **List the lines.** Run `control.sh cli python3 -m founder_requests list data_room/brasswick`. Line 6 reads `Hiring plan  [Top 1]`.
- **Draft from the command line.** Run `control.sh cli python3 -m founder_requests draft data_room/brasswick --to celia@example.com --sender Sam`. Output starts `Subject: Brasswick: documents for our review`, the body starts `Hi Celia,`, each item has `What it is:`, `Best form:` and `A good one shows:`, and the last line is a `mailto:celia@example.com?subject=...` link with `%0D%0A` line breaks.
- **Draft through the API.** Run `control.sh api POST /api/rooms/brasswick/founder-requests/draft '{"numbers":[6],"to":"celia@example.com"}'`. HTTP 200, `subject` `Brasswick: one document for our review`, `leaks` `[]`.
- **Refuse the synthetic room.** `curl -s -X POST --data-binary @founder_requests/tests/fixtures/synthetic_brasswick_hiring_plan.csv "<url>/api/rooms/brasswick/founder-requests/files?answers=C22&name=plan.csv"` answers 409 and names `python -m founder_requests copy-room data_room/brasswick`. `git status --short data_room` prints nothing.
- **Copy and build the copy's readout.** Run `control.sh api POST /api/rooms/brasswick/founder-requests/copy '{}'` (HTTP 200, `room` `brasswick_live`), then `control.sh api POST /api/rooms/brasswick_live/scans/redflags` and `control.sh api POST /api/rooms/brasswick_live/readout`.
- **On the page.** Open `<url>/` in Chromium (Playwright), pick `brasswick` in `Room`, choose `Draft request for 5 selected`, fill `To`, choose `Copy text` (status `Copied.`) and read the `Open in mail app` href. Then pick `6. Hiring plan` in `This file answers`, set `File` to `founder_requests/tests/fixtures/synthetic_brasswick_hiring_plan.csv`, choose `Add to the room`. `What happened` reads `Saved as rooms/brasswick_live/05_team/hiring_plan.csv.`, `ran again: redflags`, `missing before, found now`, and one line fewer on the ask list. Pick `brasswick_live` in `Room`: no `Hiring plan` line remains. Screenshot light and dark.
- **Read the change back.** `control.sh api GET /api/rooms/brasswick_live/results/redflags` lists `05_team/hiring_plan.csv` in `inputs` with a new `ran_at`. `control.sh api GET /api/rooms/brasswick_live/readout` has no ask with `checklist_id` `C22`, and the `checklist coverage` panel row `C22` reads `found`. `control.sh api GET /api/rooms/brasswick_live/founder-requests/received` lists the file.
- **Add from the command line.** Run `control.sh cli python3 -m founder_requests add rooms/brasswick_live <a .pdf starting %PDF-> --for C73`. The receipt saves it under `06_legal/` with `409a` in the name, `status_after` `found`, and `scans_rerun` `[]` (no scan reads a 409A report yet).
- **Refuse a bad kind.** `curl ... "files?answers=C22&name=..%2F..%2Fescape.exe"` on `brasswick_live` answers 415.

## Gotchas

- `control.sh shot` opens the page on `hollis_voice` and cannot pick a room, so the page steps need a Playwright script; `control.sh api` sends only JSON, so uploads go through `curl --data-binary` or the CLI.
- The working copy lives in the checkout's `rooms/` (git-ignored), not in the run folder. List `rooms/brasswick_live` for cleanup; a second run must use another copy name.
- A second file for the same item is saved beside the first (`hiring_plan_from_founder_...`) with a `note`: the scans still read the first.
- The copy has no readout in this run until you build it; adding a file first gives `status_before` `unknown`.
- Only scans whose needs are met and whose last result did not list a current room input rerun. Today only `redflags` is built, so a file that no input kind names (a 409A report) reruns nothing; the merge still runs and coverage changes.
- A long draft (the top five on Brasswick is about 4,500 characters) is past the 2,000 at which some mail apps cut a link; the page warns and copy is the primary action.
