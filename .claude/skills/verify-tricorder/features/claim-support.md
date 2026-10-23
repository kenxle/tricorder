# Claim support

The claims scan lists every figure in the pitch deck and in the pitch video (its script until the video is recorded) and labels each one supported, contradicted or unsupported against the room's other documents. A contradicted claim shows both sides; an unsupported one carries an ask line and a gap. The memo step then relabels a claim that another scan has flagged. The user reads it as claims with `scan` `claims` and as the readout's "claims table" and "claims table counts" Panels.

## Sub-features

- `cs-extract` lists every figure on every slide and every script line (or transcript segment), with the slide, line or segment and the exact words. Claims-page rows are folded into the figure they repeat.
- `cs-normalise` gives each figure a kind, unit and period, and marks spoken figures spoken and rounded.
- `cs-label` labels each figure: supported (a document outside the pitch agrees), contradicted (a document disagrees, both cited), unsupported (an ask line and a gap naming the document).
- `cs-spoken` contradicts a spoken figure that the deck disagrees with, under the answer key's check names `spoken_arr_vs_claims_page` and `spoken_number_vs_claims_page`.
- `cs-relabel` is the memo step: it relabels a claim to contradicted when another scan flags the same pitch figure or the check that settles its kind, and recounts the table.
- `cs-gaps` writes a gap, not a crash, for a missing deck, video, document, named cell or model key.

## How to get to it (user POV)

- Run the scan on a room: `python3 -m scans.claims <room>`. It prints `claims: N claims, M gaps -> <out>/<room>/claims.json`.
- Build the readout and apply the memo step: `python3 -m scans.memo <room>`, then `python3 -m scans.memo.claim_support <room>`. The second command prints the "claims table counts" as JSON and ends with `"relabelled by the memo step": "yes"`. Once the step is listed in `scans/memo/merge.py`, `scans.memo` alone does both.
- Through the API: `POST /api/rooms/<room>/scans/claims`, then `GET /api/rooms/<room>/results/claims`, and `GET /api/rooms/<room>/readout` for the Panels.

## Driving it with control.sh

Preconditions:

- `control.sh doctor` prints `OK` for this run.
- The red-flag scan runs before the memo step, so the relabelling has flags to read.

- **Run the scans on Hollis Voice.** Run `control.sh cli python3 -m scans.redflags data_room/hollis_voice`, then `control.sh cli python3 -m scans.claims data_room/hollis_voice`. The second prints `claims: 64 claims, 8 gaps`. Exit code 0.
- **Read the spoken contradiction.** Run `control.sh api GET /api/rooms/hollis_voice/results/claims`. A claim with `check.name` `spoken_arr_vs_claims_page`, severity `flag`, text starting `Contradicted: The pitch video script (line 15, beat 0:35; the video is not recorded yet) gives ARR as about three million dollars`, cites `01_overview/pitch_video_script.md` `line 15`, `02_financials/financial_model.xlsx` `ARR_TOTAL` and `01_overview/pitch_deck.pdf` `slide 3`.
- **Read the ceiling the books break.** In the same response, a claim citing `slide 4` says `gives largest customer share as at most 9%, but revenue by customer (row 1984) says 21.0%`.
- **Prove a source.** Run `control.sh api POST /api/rooms/hollis_voice/source '<one source object from that claim>'`. The returned text contains the source's `quote`.
- **Build the readout and relabel.** Run `control.sh cli python3 -m scans.memo data_room/hollis_voice`, then `control.sh cli python3 -m scans.memo.claim_support data_room/hollis_voice`. The counts read `"claims": "64"`, `"supported": "39"`, `"contradicted": "8"`, `"unsupported": "17"`.
- **Brasswick, relabelled by the memo step.** Run the same four commands on `data_room/brasswick`, then `control.sh api GET /api/rooms/brasswick/readout`. Claims with `scan` `claims` and a non-empty `conflicts_with` include the slide 4 chart months (`redflags` `deck_history_vs_metrics`), the slide 4 `$943K` (`gross_vs_net_revenue`), and the slide 10 runway and burn (`contractor_spend_vs_headcount_and_burn`). Counts: 53 claims, 31 supported, 7 contradicted, 15 unsupported, 6 not counted.
- **Score.** Run `control.sh cli python3 -m eval.score data_room/brasswick`: `found 5 of 5; decoys flagged 0 of 3`. On `data_room/hollis_voice` the transcript has `found  PF2b` and `decoys flagged 0 of 3`.
- **Clean room stays clear.** Run the four commands on `data_room/hollis_voice_clean`. Counts: 0 contradicted. `eval.score` says `decoys flagged 0 of 3`.
- **Seed drop names what is missing.** Run them on `data_room/hollis_voice_seed_drop`. The claims result has a gap whose `why` contains `file missing: monthly revenue by customer`.

## Gotchas

- `scans.memo.claim_support` exits 2 with `no readout at ...` until `scans.memo` ran on the room in this run.
- Until the step is listed in `scans/memo/merge.py`, `POST /api/rooms/<room>/readout` rebuilds the readout without it, so the API readout loses the relabelling. Rerun `control.sh cli python3 -m scans.memo.claim_support data_room/<room>` after any readout POST.
- The video is not recorded, so spoken claims cite the script by `line N`. A saved `01_overview/pitch_video.transcript.json` replaces them with `seg N` claims; the partial-room tests in `scans/claims/tests/test_inputs.py` prove that shape with a hand-built transcript.
- Without `ANTHROPIC_API_KEY` (always, under `control.sh`), the model reading is one gap, "no ANTHROPIC_API_KEY, so the model reading did not run". That is expected, not a failure.
- Hollis Voice scores 1 of 8 from these scans: PF3 and PF6 read supported (backed only by the model, with a note in the ask column) until the red-flag engine's rebuild checks exist, and the key credits the rest (PF2, PF4, PF5 and PF7 among the ones this scan contradicts) to other checks' names.
