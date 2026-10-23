# Requests to the founder

From the readout's ask list, the operator drafts a short message to the founder for one line or a ticked group: one plain line per item, one "Ideally it includes ..." line per kind of document, a date with a reason, and a sign-off. Lines for files the room already holds are dropped or reworded, and lines for the same papers merge. They copy it or open it in their own mail app; Tricorder sends nothing. When the founder replies, the operator adds the files, each for the requests it answers: each lands in the right numbered folder of a room under `rooms/`, the scans that had not seen them run once, the readout is rebuilt, and the receipt says what changed in plain words.

## Sub-features

- `fr-list` lists every item with its founder words, title, piece, "Top N", "A red flag rests on it", "If you have it" and "After the term sheet", and the lines not asked for because the room holds them. No check code shows.
- `fr-rank` pins the five that settle the decision first (piece weight, then red flags); closing paperwork waits for the term sheet at seed.
- `fr-draft` drafts one message for one item or many: date, reason, sign-off, a greeting from the cover note and the company from the deck.
- `fr-copy-mailto` gives the text to copy and a `mailto:` link, with a warning past 2,000 characters.
- `fr-no-leak` keeps file paths, cell references, claim ids and checklist ids out of the founder's text.
- `fr-copy-room` copies a synthetic room to `rooms/<room>_live`, because `data_room/` is never written.
- `fr-add` saves a reply's files (several in one add, one file for several requests) under names coverage recognises, reruns waiting scans once, rebuilds the readout, logs each file, and says what changed in plain words.
- `fr-refuse` refuses bad names, kinds, sizes, links, overwrites, and any write into `data_room/`.

## How to get to it (user POV)

- Command line: `python3 -m founder_requests list|draft|copy-room|add <room> ...`.
- API: `GET /api/rooms/<room>/founder-requests`, `POST /api/rooms/<room>/founder-requests/draft` with `{"numbers": [...], "to": "...", "sender": "...", "fund": "...", "by": "YYYY-MM-DD"}`, `POST /api/rooms/<room>/founder-requests/copy` with `{}`, `POST /api/rooms/<room>/founder-requests/files?answers=<C22, a line number, or several comma separated>&name=<file name>` with the raw file as the body and `Content-Type: application/octet-stream` (the local guard refuses text/plain and other sites), `POST /api/rooms/<room>/founder-requests/batch` with `{"files": [{"name", "answers", "data": <base64>}]}`, `GET /api/rooms/<room>/founder-requests/received`.
- Page: the section `aria-label="Requests to the founder"` under the ask list: checkboxes `Select <title>`, buttons `Draft request for N selected`, `Draft request for <title>` and `Add the founder's reply`; the drawer `aria-label="Draft to the founder"` with the trust line, `To`, `Ask for it by`, `Your name`, `Fund`, `Copy text` and the link `Open in mail app`; and the block `aria-label="Add the founder's reply"` with `Files from the reply` (several), then per file `It answers` / `It also answers` and `Add N files to the room`. The result is `aria-label="What changed"`.

## Driving it with control.sh

Preconditions:

- `control.sh doctor` prints `OK` for this run.
- No folder `rooms/brasswick_live` exists in the checkout. If one does, pick another copy name (`copy-room --as`, or `{"name": "..."}` on the copy route), build its readout, and on the page pick that room in `Room` before adding files (the page's own copy step always uses `<room>_live`).
- `readout/dist/` was built from this checkout after the panel landed (`bin/ci-web`), or the page has no panel.

- **Build the readout.** Run `control.sh cli python3 -m scans.redflags data_room/brasswick`, then `control.sh cli python3 -m scans.memo data_room/brasswick`. Both exit 0.
- **List the lines.** Run `control.sh cli python3 -m founder_requests list data_room/brasswick`. Line 1 is `Monthly revenue by customer  [Top 1, ...]` and asks only for the kind of revenue and an MRR column; line 6 is `Hiring plan  [Top 5]`; incorporation, IP and minutes read `after the term sheet`.
- **Draft from the command line.** Run `control.sh cli python3 -m founder_requests draft data_room/brasswick --to celia@example.com --sender "Sam Ortiz" --fund "Example Ventures" --by 2026-11-06`. Output starts `Subject: Brasswick: a few things before our next meeting`, the body starts `Hi Celia,`, says `by Friday 6 November`, each item is one line plus at most one `Ideally it includes`, it ends `Sam Ortiz` / `Example Ventures`, and the mailto line says under 2,000 characters with no "long for a mail link".
- **Draft through the API.** Run `control.sh api POST /api/rooms/brasswick/founder-requests/draft '{"numbers":[6],"to":"celia@example.com"}'`. HTTP 200, `subject` `Brasswick: one thing before our next meeting`, `leaks` `[]`.
- **Refuse the synthetic room.** `curl -s -X POST -H 'Content-Type: application/octet-stream' --data-binary @founder_requests/tests/fixtures/synthetic_brasswick_hiring_plan.csv "<url>/api/rooms/brasswick/founder-requests/files?answers=C22&name=plan.csv"` answers 409 and names `python -m founder_requests copy-room data_room/brasswick`. `git status --short data_room` prints nothing.
- **Copy and build the copy's readout.** Run `control.sh api POST /api/rooms/brasswick/founder-requests/copy '{}'` (HTTP 200, `room` `brasswick_live`), then `control.sh api POST /api/rooms/brasswick_live/scans/redflags` and `control.sh api POST /api/rooms/brasswick_live/readout`.
- **On the page.** Open `<url>/` in Chromium (Playwright; the fix-round script is `docs/features/20261023.02_founder_requests/evidence/fix_round/drive_page.js`), pick `brasswick` in `Room`, choose `Draft request for 5 selected`, read the trust line, fill `To`, `Your name`, `Fund` and `Ask for it by`, choose `Copy text` (status `Copied.`) and read the `Open in mail app` href (under 2,000 characters). Pick the working room, set `Files from the reply` to the hiring plan fixture and a synthetic reference-list PDF, pick `Hiring plan` for the first and `People we can call: Reference list: ...` plus `People we can call: Founder reference calls` for the second, choose `Add 2 files to the room`. `What changed` reads `Coverage now finds Hiring plan and future org.`, `Coverage now finds Reference list: ...`, `No check reads these files yet, so no number changed.` and `The ask list is down from 32 to 30 lines.`; no scan name shows. No `Hiring plan` line remains. Screenshot light and dark, and at 390 px wide.
- **Read the change back.** `control.sh api GET /api/rooms/brasswick_live/results/redflags` lists `05_team/hiring_plan.csv` in `inputs` with a new `ran_at`. `control.sh api GET /api/rooms/brasswick_live/readout` has no ask with `checklist_id` `C22`, and the `checklist coverage` panel row `C22` reads `found`. `control.sh api GET /api/rooms/brasswick_live/founder-requests/received` lists the file.
- **Add from the command line.** Run `control.sh cli python3 -m founder_requests add rooms/brasswick_live <a .pdf starting %PDF-> --for C73`. The receipt's `files[0].saved` is under `06_legal/` with `409a` in the name, `summary` reads `Coverage now finds 409A valuation.` and `No check reads this file yet, so no number changed.`, and `scans_rerun` is `[]` (no scan reads a 409A report yet).
- **Refuse a bad kind.** `curl ... "files?answers=C22&name=..%2F..%2Fescape.exe"` on `brasswick_live` answers 415.

## Gotchas

- `control.sh shot` opens the page on `hollis_voice` and cannot pick a room, so the page steps need a Playwright script; `control.sh api` sends only JSON, so uploads go through `curl --data-binary` or the CLI.
- The working copy lives in the checkout's `rooms/` (git-ignored), not in the run folder. List `rooms/brasswick_live` for cleanup; a second run must use another copy name.
- A second file for the same item is saved beside the first (`hiring_plan_from_founder_...`) with a `note`: the scans still read the first.
- The copy has no readout in this run until you build it; adding a file first gives `status_before` `unknown`.
- Only scans whose needs are met and whose last result did not list a current room input rerun. Today only `redflags` is built, so a file that no input kind names (a 409A report) reruns nothing; the merge still runs and coverage changes.
- The default five on Brasswick fits a mail link (about 1,750 characters). Ticking many items goes past 2,000, where some mail apps cut a link; the page warns and copy is the primary action.
- A file for an ask only the founder can give (founder reference calls) is saved and logged, but coverage cannot find it, so its line stays; the receipt says so.
