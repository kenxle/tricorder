# Steering

The operator types one plain sentence on a piece of the readout, or on one line, and presses Enter. Tricorder reads the sentence as a rewrite or a request for more info, rebuilds that piece, and shows the revised lines where the operator typed, tagged with who steered and when ("Ken's steer, Oct 23, 03:06 AM") or "new", with a diff that opens with what happened ("Added a scenario line.", "Read 5 new files; ...", "Refused: ..."): the check line a scenario line replaced, lines dropped, wording changed, and the verdict before and after with the line that moved it. A request for a different number changes nothing and says the check's number stays. Every revision is kept in the readout and as a new store version.

## Sub-features

- `steer-rewrite-definition`: "treat the pilot as non-recurring" on traction and revenue adds one scenario line, ARR without the pilot, computed from two P&L cells and citing the pilot agreement's notice clause; it becomes the piece's reason, and the check's own ARR line stays as the diff's "before".
- `steer-more-info-full-room`: "read the full room" on the seed drop (a line, a piece, or the overview) reruns every scan on the full room and rebuilds every piece; the rebuilt NRR and GRR lines are tagged new and open the cohort rows they sum; retention moves from not enough in the room to looking weak, moved by the NRR line; a banner states the switch, and every line's source opens from the full room.
- `steer-number-guard`: "make ARR 3 million" changes no line and the note quotes the check's line back.
- `steer-named-source`: "pull the competitor's pricing pages" fetches nothing and says so.
- `steer-read-path`: every note says whether a model reading or the wording rules read the sentence.
- `steer-kept`: each steer appends a revision and a `steer N: what changed` Panel to the readout, and saves a new store version.
- `steer-author`: `Steer.author` is the request's `author`, else `TRICORDER_OPERATOR`.
- `steer-page`: one box on the overview ("Steer the overview"), per piece ("Steer this piece") and per line ("steer this line"); the first box shows "For example: treat the pilot as non-recurring"; Enter sends; the answer appears where it was typed. Mounted on the readout page `/` and on `/steer.html`.

## How to get to it (user POV)

- Terminal: `python3 -m steering <room_dir> <piece> "<sentence>" [--line <claim id>] [--fund demo] [--author <name>]`. It prints the revision, the added lines and the store save as JSON.
- API: `GET /api/rooms/<room>/steerable` (the readout with verdicts), `POST /api/rooms/<room>/steer` with `{"piece": "<piece>", "sentence": "<one sentence>", "claim_id": "<line id or null>"}`, `GET /api/rooms/<room>/revisions`, `GET /api/rooms/<room>/claims/<claim id>/sources/<i>` (a line's source text, from the room the line reads; answers `{"room", "text"}`).
- Page: the readout page `/` (its Overview section), or `/steer.html?room=<room>`. Each piece row has "Steer this piece"; each line has "steer this line". The text box is labelled "Steer in one sentence". Pieces are `[data-piece="<piece>"]`, lines `li.claim[data-claim="<id>"]`, each diff `role="status"` named "Steer N".
- Pieces are the schema names: `traction_and_revenue`, `retention`, `burn_and_runway`, `unit_economics`, `customers`, `market`, `comps`, `team`, `the_pitch_itself`.

## Driving it with control.sh

Preconditions:

- `TRICORDER_VERIFY_RUN=steering` and `TRICORDER_VERIFY_PORT=8815` (or another free port).
- Before `control.sh launch`, export `TRICORDER_STORE_DIR=<run folder>/store_data`, `TRICORDER_CACHE_DIR=<run folder>/cache` and `TRICORDER_OPERATOR=Ken`, so steers save into this run's store, never the repo's `store_data/`, and name who steered.
- `readout/dist/` holds `steer.html`. Rebuild with `bin/ci-web` after changing the page; `control.sh launch` builds only when `dist/` is missing.
- `ANTHROPIC_API_KEY` is unset, so the wording rules read every sentence. With a key set and `TRICORDER_OFFLINE` unset the model reads them instead; `control.sh` sets `TRICORDER_OFFLINE=1`, so it always runs the rules.
- For the page: Node 20 or later and a folder outside the repo with `npm i --no-save playwright`; set `CHROME` to a Chrome binary if Playwright's own is not installed.
- `control.sh doctor` prints `OK` for this run.

- **Build both readouts.** `control.sh cli python3 -m scans.redflags data_room/hollis_voice_seed_drop`, then `scans.claims`, then `scans.memo`, for the seed drop; the same three for `data_room/hollis_voice`. All exit 0.
- **Before.** `control.sh api GET /api/rooms/hollis_voice_seed_drop/steerable`. `HTTP 200`; the `retention` piece reads `not_enough_in_the_room` and its reason names the missing customer file. Note the id of the retention line that starts "The Cohorts tab states".
- **More info on a line.** `control.sh api POST /api/rooms/hollis_voice_seed_drop/steer '{"piece": "retention", "sentence": "read the full room", "claim_id": "<that id>"}'`. `HTTP 200`; `source_room` is `hollis_voice`; `revision.steer.author` `Ken`; `changes.rows[0]` is the headline "Read 5 new files; retention moved to Looking weak, ..."; `revision.before.verdict` `not_enough_in_the_room`, `revision.after.verdict` `looking_weak`; `claims_added` holds ids ending `.steer1` in several pieces; `claims_dropped` holds only the claims scan's "Unsupported" lines the full room supports; `verdict_moved_by` starts with the line "Rebuilt from the customer file, 12-month net revenue retention is 87.3% ...".
- **Rewrite on a piece.** `control.sh api POST /api/rooms/hollis_voice/steer '{"piece": "traction_and_revenue", "sentence": "treat the pilot as non-recurring"}'`. Headline "Added a scenario line."; one added line starting "On Ken's steer, pilot not counted: ARR $2,060,868." with a source `04_customers/pilot_agreement_marlow.pdf`, `page 2`; the traction piece's `reason` is that line; a `replaced` row names the line "The deck's ARR of $2,500,000 (slide 3) differs from the P&L's $2,240,868", which is still in `readout.claims`; the note says "Your scenario line is new. The original check still shows $2,240,868."
- **Number guard.** `control.sh api POST /api/rooms/hollis_voice/steer '{"piece": "traction_and_revenue", "sentence": "make ARR 3 million"}'`. `claims_added` and `claims_dropped` are empty, the note starts "Refused: computed numbers do not change on request." and says "You asked for 3 million. The check's number stays as it wrote it:", and does not say "Rewritten".
- **Quote checker.** `control.sh cli python3 -m schema.check_quotes data_room/hollis_voice <run folder>/out/hollis_voice/readout.json <run folder>/out/hollis_voice_seed_drop/readout.json` exits 0. Use the full room for both: the seed drop's new lines cite files only the full room holds.
- **Source of a full-room line on the seed drop.** `control.sh api GET /api/rooms/hollis_voice_seed_drop/claims/<the NRR .steer1 id>/sources/0` returns `"room":"hollis_voice"` and the customer file's header. `POST /api/rooms/hollis_voice_seed_drop/source` for the same file is 404, which is why the route exists.
- **Kept.** `control.sh api GET /api/rooms/hollis_voice/revisions` lists both instructions. `control.sh api GET /api/store/demo/hollis_voice/versions` lists versions 1 and 2 with `revisions` 1 and 2.
- **Terminal.** `control.sh cli python3 -m steering data_room/hollis_voice market "pull the competitor's pricing pages"` exits 0; the note says it was not fetched.
- **Page.** First reset both readouts: `control.sh cli python3 -m scans.memo data_room/hollis_voice_seed_drop` and the same for `data_room/hollis_voice` write them back with no revisions (the store keeps its versions). Then from the Playwright folder: `CHROME=<binary> node <repo>/docs/features/20261023.05_steering/verify_drive_page.mjs http://127.0.0.1:8815 <run folder>/evidence`. It opens `/steer.html`, clicks "steer this line" on the seed drop's Cohorts line (shot with the box open), types "read the full room", presses Enter, opens the rebuilt NRR line's source and its cohort rows, then on the readout page `/` steers Hollis Voice's traction piece with the pilot sentence and the number request. Proof is `page_drive.txt` (the placeholder, the banner, each diff's text, the source panel, the rows table, page errors) and the light, dark and phone screenshots it saves.

## Gotchas

- `control.sh shot` opens `/` and can show the steerable overview, but cannot type. Use the Playwright driver to steer.
- A steer writes back to this run's `out/<room>/readout.json`, and revisions stack. `python3 -m scans.memo <room>` writes a readout with no revisions, which is how the page step starts clean; read revision numbers from responses rather than assuming 1.
- "Read the full room" works only on a room named `<x>_seed_drop` with a sibling folder `<x>`. On the full room it changes nothing and says so.
- Until the merge's `pieces` and `top_flags` steps exist, verdicts come from steering's copy of the FRAMEWORKS rules, and every note says so. A plain `POST /api/rooms/<room>/readout` rebuild drops the pieces and the revisions from `out/`; the store keeps them.
- A scenario line replaces its check line in the piece list; the check line is in the diff as "Before, the check's line (kept)". A selector for the check line inside `ul.claims` finds nothing after the pilot steer.
- After "read the full room", a second one reads nothing new ("Nothing new read: every piece already reads hollis_voice"). Reset with `scans.memo` to drive it again.
