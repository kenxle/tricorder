# The memo and its PDF

The operator exports a draft memo for the partners' meeting from a room's readout. It has the template's 16 sections in order; each is filled from the readout or names the gap that leaves it empty, and the recommendation and outcome cases stay blank for the operator. The partners open an interactive page: one click on any line opens the claims behind it, one more opens a claim's source text with the quote marked and the sources that agree or disagree. A PDF of the same memo footnotes every claim to its file and locator. Each operator edit makes a numbered version, and the operator's own sentences are marked as theirs.

## Sub-features

- `me-export` writes a new version, the page and the PDF from the room's readout.
- `me-sections` gives the 16 sections in the template's order, each filled or naming its gap (`Not in the room:` or `Not in the readout yet:`).
- `me-drill` opens a line's claims in one click and a claim's sources, with the agreeing and disagreeing claims, in the second.
- `me-pdf` footnotes every cited claim with its id, file, locator, quote and date read.
- `me-quotes` reruns the quote checker on every claim; a failure moves to the "could not verify" box in section 14.
- `me-edit` applies operator edits as a new version, marks operator lines and figures with no source, and refuses an edit based on an old version.

## How to get to it (user POV)

- `python3 -m memo data_room/<room>` after the readout is built (`python3 -m scans.memo data_room/<room>`). `--edit edits.json --author NAME` applies edits. Output in `out/<room>/memo/`: `memo_v<N>.json`, `memo.html`, `memo.pdf`.
- `python3 -m memo out/<room>/readout.json --room-dir data_room/<room>` from a readout file.
- API: `POST /api/rooms/<room>/memo`, `GET /api/rooms/<room>/memo[?version=N]`, `GET /api/rooms/<room>/memo/versions`, `POST /api/rooms/<room>/memo/edits` with `{"author", "base_version", "edits": [...]}`.
- The page: `GET /api/rooms/<room>/memo.html` (editing on when served), or open `memo.html` from disk (read only). The PDF: `GET /api/rooms/<room>/memo.pdf`.

## Driving it with control.sh

Preconditions:

- `control.sh doctor` prints `OK` for this run.
- Node and a scratch `node_modules` with `playwright` (`npm i --no-save playwright` outside the repo), for the click proof.

- **Build the readout.** Run `control.sh cli python3 -m scans.redflags data_room/hollis_voice`, then `control.sh cli python3 -m scans.memo data_room/hollis_voice`. Both exit 0.
- **Export.** Run `control.sh cli python3 -m memo data_room/hollis_voice`. Exit 0; stdout JSON has `"version": 1`, `"sections": 16`, `"claims": 10`, `"could_not_verify": 0`, and `sections_empty` naming each empty section with its gap text.
- **Read it back.** Run `control.sh api GET /api/rooms/hollis_voice/memo`. HTTP 200; `sections` has 16 entries numbered 1 to 16; every section has lines; section 15's only line has `kind` `slot`.
- **Quote check.** Run `control.sh cli python3 -m schema.check_quotes data_room/hollis_voice <run>/out/hollis_voice/readout.json`. Exit 0, "10 claims checked". Every claim in the memo is one of these.
- **Two clicks, in Chromium.** Run `NODE_PATH=<scratch>/node_modules node docs/features/20261023.03_memo_export/spike/drive_memo.js http://127.0.0.1:<port>/api/rooms/hollis_voice/memo.html <evidence dir> memo`. Exit 0; `memo_drive.json` has `opened_in_one_click` equal to `drillable`, `sources_opened_in_two_clicks` and `quotes_marked` equal to `claims_seen`, and `failures` empty. It saves `memo_{light,dark}_{top,drill}.png` and `memo_phone_dark.png`. Stable handles: `.line[data-line-id]`, its `.line-open` button (`aria-expanded`), `.drill .claim[data-claim-id]`, `.source-open`, `.source-text mark`, `.agree`, `.disagree`, `#copy-asks`.
- **PDF.** Run `control.sh api GET /api/rooms/hollis_voice/memo.pdf` for the status, and save the file with `curl -o`. Its text holds `[n] redflags-00k.` notes for all 10 claims, each naming `<file>, <locator>`.
- **Edit.** Run `control.sh api POST /api/rooms/hollis_voice/memo/edits '{"author":"Verifier","base_version":1,"edits":[{"action":"replace","line_id":"s15-recommendation","text":"Wait for bank statements; invest up to $1.5M."}]}'`. HTTP 200, `"version": 2`; section 15's line has `kind` `operator`, `author` `Verifier` and `unsourced_numbers` `["$1.5M"]`. The same call again answers HTTP 409.
- **Versions.** Run `control.sh api GET /api/rooms/hollis_voice/memo/versions`. Body `[1,2]`.

## Gotchas

- The pieces, top_flags and link merge steps are not built on main yet. The memo says so in gap lines, and the page says agreement is "Not checked yet". Do not read 0 agreeing sources as a finding.
- The memo writes into this run's `out/<room>/memo/`; versions are never overwritten, so a second export makes version 2 and keeps operator lines.
- `control.sh shot` captures `/`, the readout page, not the memo; use the drive script for the memo page.
- Opened from disk the page is read only; editing appears only at `/api/rooms/<room>/memo.html`.
- The PDF uses reportlab from `requirements.txt`; an environment installed before 2026-10-23 may need `pip install -r requirements.txt` again.
