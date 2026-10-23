# The memo and its PDF

The operator exports a draft memo for the partners' meeting from a room's readout. It has the template's 16 sections in order; each is filled from the readout or names the gap that leaves it empty, and the recommendation and outcome cases stay blank for the operator. The partners open an interactive page: one click on any line opens the claims behind it, one more opens a claim's source text with the quote marked and the sources that agree or disagree. A PDF of the same memo footnotes every claim to its file and locator. Each operator edit makes a numbered version, and the operator's own sentences are marked as theirs.

## Sub-features

- `me-export` writes a new version, the page and the PDF from the room's readout.
- `me-sections` gives the 16 sections in the template's order, each filled or naming its gap (`Not in the room:` or `Not in the readout yet:`).
- `me-drill` opens a line's claims in one click and a claim's sources, with the agreeing and disagreeing claims, in the second.
- `me-pdf` is the partner view: every cited claim footnoted with file, place, what it reads as and date read; no ask list, ids or blanks.
- `me-quotes` reruns the quote checker on every claim; a failure moves to the "could not verify" box in section 14.
- `me-edit` applies many in-place edits as one version under the typed name, marks operator lines and figures with no source, detaches claims from a rewrite with a new figure, and on a 409 keeps the edits to reapply.
- `me-views` gives the partner view by default (no plumbing, the answer first, empty sections in one line) and the operator view behind the toggle.

## How to get to it (user POV)

- `python3 -m memo data_room/<room>` after the readout is built (`python3 -m scans.memo data_room/<room>`). `--edit edits.json --author NAME` applies edits. Output in `out/<room>/memo/`: `memo_v<N>.json`, `memo.html`, `memo.pdf`.
- `python3 -m memo out/<room>/readout.json --room-dir data_room/<room>` from a readout file.
- API: `POST /api/rooms/<room>/memo`, `GET /api/rooms/<room>/memo[?version=N]`, `GET /api/rooms/<room>/memo/versions`, `POST /api/rooms/<room>/memo/edits` with `{"author", "base_version", "edits": [...]}`.
- The page: `GET /api/rooms/<room>/memo.html` (editing on when served), or open `memo.html` from disk (read only). The PDF: `GET /api/rooms/<room>/memo.pdf`.

## Driving it with control.sh

Preconditions:

- `control.sh doctor` prints `OK` for this run.
- Node and a scratch `node_modules` with `playwright` (`npm i --no-save playwright` outside the repo), for the click proof.

- **Build the readout.** Run `control.sh cli python3 -m scans.redflags data_room/hollis_voice`, then `scans.claims` (unset `ANTHROPIC_API_KEY` so no model is called), then `scans.memo`. Each exits 0.
- **Export.** Run `control.sh cli python3 -m memo data_room/hollis_voice`. Exit 0; stdout JSON has `"version": 1`, `"sections": 16`, `"claims"` equal to the readout's claim count, `"could_not_verify": 0`, and `sections_empty` naming each empty section with its one line.
- **Read it back.** Run `control.sh api GET /api/rooms/hollis_voice/memo`. HTTP 200; 16 sections; section 15's only line has `kind` `slot` and `audience` `operator`.
- **Quote check.** Run `control.sh cli python3 -m schema.check_quotes data_room/hollis_voice <run>/out/hollis_voice/readout.json`. Exit 0.
- **Both views, two clicks, in Chromium.** Run `NODE_PATH=<scratch>/node_modules node docs/features/20261023.03_memo_export/spike/drive_memo.js http://127.0.0.1:<port>/api/rooms/hollis_voice/memo.html <evidence dir> memo`. Exit 0; `memo_drive.json` has `partner_plumbing` empty (no claim id, check name, checklist number, command or blank in what a partner sees), `partner_first_screen` starting with the round and the red flags, and in the operator view `opened_in_one_click` equal to `drillable`, `sources_opened_in_two_clicks` and `quotes_marked` equal to `claims_seen`, `failures` empty, `phone_horizontal_scroll` false. It saves `memo_{light,dark}_{top,drill}.png` and `memo_phone_dark.png`. Stable handles: `.line[data-line-id]` with class `aud-<audience>`, its `.line-open` button (`aria-expanded`), `.drill .claim[data-claim-id]`, `.source-open`, `.source-text mark`, `.agree`, `.disagree`, `#view-toggle`, `#theme-toggle`.
- **Edit in one sitting.** Run `NODE_PATH=... node docs/features/20261023.03_memo_export/spike/edit_in_page.js http://127.0.0.1:<port>/api/rooms/hollis_voice/memo.html <evidence dir> "Priya Shah"` on a fresh version 1. Exit 0; `edit_in_page.json` shows "Save 3 changes as version 2", a 409 because another author saved version 2 through the API first, the three changes kept and reapplied as version 3, the rewritten cash line with no claims and `$2,100,000` as the operator's figure, and section 2 opening with "Recommendation." Handles: `#edit-author`, `#edit-save`, `#edit-discard`, `#edit-status`, `#edit-reapply`, `.op-add`, `.op-tools`, `textarea.op-text`.
- **PDF.** Save `GET /api/rooms/hollis_voice/memo.pdf` with `curl -o`. Its text has `[n] <file>, <locator>: ...` notes numbered from 1, every cited source's file and locator, no claim id, check name, checklist number, ask list or blank, no unformatted number, and section 2 opens with the recommendation once one is written.
- **Versions.** Run `control.sh api GET /api/rooms/hollis_voice/memo/versions`. Body `[1,2,3]` after the edit drive.

## Gotchas

- The pieces and top_flags merge steps are not built yet. The summary says "No verdicts yet" and lists the flags by severity instead.
- `uvicorn` does not reload: restart with `cleanup` and `launch` after a code change, or the page is the old one.
- The memo writes into this run's `out/<room>/memo/`; versions are never overwritten, so a second export makes version 2 and keeps operator lines.
- `control.sh shot` captures `/`, the readout page, not the memo; use the drive script for the memo page.
- Opened from disk the page is read only; editing appears only at `/api/rooms/<room>/memo.html`.
- The PDF uses reportlab from `requirements.txt`; an environment installed before 2026-10-23 may need `pip install -r requirements.txt` again.
