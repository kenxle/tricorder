# Steering

The operator types one plain sentence on a piece of the readout, or on one line, and presses Enter. Tricorder reads the sentence as a rewrite or a request for more info, rebuilds that piece, and shows the revised lines where the operator typed, tagged "your steer" or "new", with a diff: lines added and dropped, wording changed, the verdict before and after and the line that moved it. A request for a different number changes nothing and says the check's number stays. Every revision is kept in the readout and as a new store version.

## Sub-features

- `steer-rewrite-definition`: "treat the pilot as non-recurring" on traction and revenue adds one line, ARR without the pilot, computed from two P&L cells; the check's own ARR line stays.
- `steer-more-info-full-room`: "read the full room" on the seed drop's retention line reruns the scans on the full room and adds the rebuilt NRR and GRR lines, tagged new; the verdict moves from not enough in the room to looking weak, moved by the NRR line.
- `steer-number-guard`: "make ARR 3 million" changes no line and the note quotes the check's line back.
- `steer-named-source`: "pull the competitor's pricing pages" fetches nothing and says so.
- `steer-read-path`: every note says whether a model reading or the wording rules read the sentence.
- `steer-kept`: each steer appends a revision and a `steer N: what changed` Panel to the readout, and saves a new store version.
- `steer-page`: one box per piece ("Steer this piece") and per line ("steer this line"); Enter sends; the answer appears under the line typed on.

## How to get to it (user POV)

- Terminal: `python3 -m steering <room_dir> <piece> "<sentence>" [--line <claim id>] [--fund demo] [--author <name>]`. It prints the revision, the added lines and the store save as JSON.
- API: `GET /api/rooms/<room>/steerable` (the readout with verdicts), `POST /api/rooms/<room>/steer` with `{"piece": "<piece>", "sentence": "<one sentence>", "claim_id": "<line id or null>"}`, `GET /api/rooms/<room>/revisions`.
- Page: `/steer.html?room=<room>`. Each piece row has "Steer this piece"; each line has "steer this line". The text box is labelled "Steer in one sentence". Pieces are `[data-piece="<piece>"]`, lines `li.claim[data-claim="<id>"]`, each diff `role="status"` named "Steer N".
- Pieces are the schema names: `traction_and_revenue`, `retention`, `burn_and_runway`, `unit_economics`, `customers`, `market`, `comps`, `team`, `the_pitch_itself`.

## Driving it with control.sh

Preconditions:

- `TRICORDER_VERIFY_RUN=steering` and `TRICORDER_VERIFY_PORT=8815` (or another free port).
- Before `control.sh launch`, export `TRICORDER_STORE_DIR=<run folder>/store_data` and `TRICORDER_CACHE_DIR=<run folder>/cache`, so steers save into this run's store, never the repo's `store_data/`.
- `readout/dist/` holds `steer.html`. Rebuild with `bin/ci-web` after changing the page; `control.sh launch` builds only when `dist/` is missing.
- `ANTHROPIC_API_KEY` is unset, so the wording rules read every sentence. With a key set and `TRICORDER_OFFLINE` unset the model reads them instead; `control.sh` sets `TRICORDER_OFFLINE=1`, so it always runs the rules.
- For the page: Node 20 or later and a folder outside the repo with `npm i --no-save playwright`; set `CHROME` to a Chrome binary if Playwright's own is not installed.
- `control.sh doctor` prints `OK` for this run.

- **Build both readouts.** `control.sh cli python3 -m scans.redflags data_room/hollis_voice_seed_drop`, then `control.sh cli python3 -m scans.memo data_room/hollis_voice_seed_drop`; the same two for `data_room/hollis_voice`. All exit 0.
- **Before.** `control.sh api GET /api/rooms/hollis_voice_seed_drop/steerable`. `HTTP 200`; the `retention` piece reads `not_enough_in_the_room` and its reason names the missing customer file. Note the id of the retention line that starts "The Cohorts tab states".
- **More info on a line.** `control.sh api POST /api/rooms/hollis_voice_seed_drop/steer '{"piece": "retention", "sentence": "read the full room", "claim_id": "<that id>"}'`. `HTTP 200`; `source_room` is `hollis_voice`; `revision.before.verdict` `not_enough_in_the_room`, `revision.after.verdict` `looking_weak`; `claims_added` holds two ids ending `.steer1`; `verdict_moved_by` names the line "Rebuilt from the customer file, 12-month net revenue retention is 87.3% ...".
- **Rewrite on a piece.** `control.sh api POST /api/rooms/hollis_voice/steer '{"piece": "traction_and_revenue", "sentence": "treat the pilot as non-recurring"}'`. One added line starting "On your steer (pilot treated as non-recurring): ARR is $2,060,868"; the line "The deck's ARR of $2,500,000 (slide 3) differs from the P&L's $2,240,868" is still in `readout.claims`; the note says "Verdict unchanged." and "The checks' numbers are unchanged."
- **Number guard.** `control.sh api POST /api/rooms/hollis_voice/steer '{"piece": "traction_and_revenue", "sentence": "make ARR 3 million"}'`. `claims_added` and `claims_dropped` are empty and the note says "You asked for 3 million. The check's number stays as it wrote it:".
- **Quote checker.** `control.sh cli python3 -m schema.check_quotes data_room/hollis_voice <run folder>/out/hollis_voice/readout.json <run folder>/out/hollis_voice_seed_drop/readout.json` exits 0. Use the full room for both: the seed drop's new lines cite files only the full room holds.
- **Source of a new line.** `control.sh api POST /api/rooms/hollis_voice/source` with the first source of a `.steer1` line returns text containing its quote.
- **Kept.** `control.sh api GET /api/rooms/hollis_voice/revisions` lists both instructions. `control.sh api GET /api/store/demo/hollis_voice/versions` lists versions 1 and 2 with `revisions` 1 and 2.
- **Terminal.** `control.sh cli python3 -m steering data_room/hollis_voice market "pull the competitor's pricing pages"` exits 0; the note says it was not fetched.
- **Page.** First reset both readouts: `control.sh cli python3 -m scans.memo data_room/hollis_voice_seed_drop` and the same for `data_room/hollis_voice` write them back with no revisions (the store keeps its versions). Then from the Playwright folder: `CHROME=<binary> node <repo>/docs/features/20261023.05_steering/verify_drive_page.mjs http://127.0.0.1:8815 <run folder>/evidence`. It opens `/steer.html`, clicks "steer this line" on the seed drop's Cohorts line, types "read the full room", presses Enter, then steers Hollis Voice's traction piece and ARR line. Proof is `page_drive.txt` (what appeared next to each line, every diff's text, page errors) and the light, dark and phone screenshots it saves.

## Gotchas

- `control.sh shot` opens `/`, the readout page, which has no steering box until `SteerableOverview` is mounted in `App.tsx`. Use the Playwright driver for the page.
- A steer writes back to this run's `out/<room>/readout.json`, and revisions stack. `python3 -m scans.memo <room>` writes a readout with no revisions, which is how the page step starts clean; read revision numbers from responses rather than assuming 1.
- "Read the full room" works only on a room named `<x>_seed_drop` with a sibling folder `<x>`. On the full room it changes nothing and says so.
- Until the merge's `pieces` and `top_flags` steps exist, verdicts come from steering's copy of the FRAMEWORKS rules, and every note says so. A plain `POST /api/rooms/<room>/readout` rebuild drops the pieces and the revisions from `out/`; the store keeps them.
- The phone-width shot opens the retention piece by clicking its row; on a run where retention already reads weak it starts open, so the click closes it. The shot still proves the layout has no sideways scroll.
