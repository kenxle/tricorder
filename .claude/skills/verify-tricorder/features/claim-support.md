# Claim support

The claims scan lists every figure in the pitch deck and in the pitch video (its script until the video is recorded) and labels each one supported, contradicted or unsupported against the room's other documents. A contradicted claim shows both sides; an unsupported one carries an ask line and a gap. The memo step then relabels a claim that another scan has flagged. The user reads it as claims with `scan` `claims` and as the readout's "claims table" and "claims table counts" Panels.

## Sub-features

- `cs-extract` lists every figure on every slide and every script line (or transcript segment), with the slide, line or segment and the exact words. Claims-page rows are folded into the figure they repeat.
- `cs-normalise` gives each figure a kind, unit and period, and marks spoken figures spoken and rounded.
- `cs-label` labels each figure: supported (a document outside the pitch, other than the company's financial model, agrees), contradicted (a document disagrees, both cited), unsupported (an ask line and a gap naming the document; "only a model reading backs this" when the model alone agrees).
- `cs-spoken` contradicts a spoken figure that the deck disagrees with, under the answer key's check names `spoken_arr_vs_claims_page` and `spoken_number_vs_claims_page`.
- `cs-relabel` is the memo step: it relabels a claim to contradicted when another scan's flag quotes the same pitch words, or when a settling check's flag carries a figure of the same label, unit and period that breaks the claim. It names other settling flags without relabelling, and recounts the table.
- `cs-gaps` writes a gap, not a crash, for a missing deck, video, document, named cell or model key, and for a founder's file with other columns, text in a number cell, or a malformed claims.json.

## How to get to it (user POV)

- Run the scan on a room: `python3 -m scans.claims <room>`. It prints `claims: N claims, M gaps -> <out>/<room>/claims.json`.
- Build the readout and apply the memo step: `python3 -m scans.memo <room>`, then `python3 -m scans.memo.claim_support <room>`. The second command prints the "claims table counts" as JSON and ends with `"relabelled by the memo step": "yes"`. `scans.memo` already runs the step; the command reapplies it and prints the counts.
- Through the API: `POST /api/rooms/<room>/scans/claims`, then `GET /api/rooms/<room>/results/claims`, and `GET /api/rooms/<room>/readout` for the Panels.

## Driving it with control.sh

Preconditions:

- `control.sh doctor` prints `OK` for this run.
- The red-flag scan runs before the memo step, so the relabelling has flags to read.

- **Run the scans on Hollis Voice.** Run `control.sh cli python3 -m scans.redflags data_room/hollis_voice`, then `control.sh cli python3 -m scans.claims data_room/hollis_voice`. The second prints `claims: 64 claims, 19 gaps`. Exit code 0.
- **Read the spoken contradiction.** Run `control.sh api GET /api/rooms/hollis_voice/results/claims`. A claim with `check.name` `spoken_arr_vs_claims_page`, severity `flag`, text starting `Contradicted: The pitch video script (line 15, beat 0:35; the video is not recorded yet) gives ARR as about three million dollars`, cites `01_overview/pitch_video_script.md` `line 15`, `02_financials/financial_model.xlsx` `ARR_TOTAL` and `01_overview/pitch_deck.pdf` `slide 3`.
- **Read the ceiling the books break.** In the same response, a claim citing `slide 4` says `gives largest customer share as at most 9%, but revenue by customer (row 1984) says 21.0%`.
- **Prove a source.** Run `control.sh api POST /api/rooms/hollis_voice/source '<one source object from that claim>'`. The returned text contains the source's `quote`.
- **Build the readout and relabel.** Run `control.sh cli python3 -m scans.memo data_room/hollis_voice`, then `control.sh cli python3 -m scans.memo.claim_support data_room/hollis_voice`. The counts read `"claims": "64"`, `"supported": "24"`, `"contradicted": "10"`, `"unsupported": "30"`. The slide 6 NRR of 102.6% reads contradicted with `conflicts_with` naming the `redflags` `rebuild_cohorts_from_customer_file` flag (87.3%). The slide 11 runway (37) and burn ($374,462) read unsupported; their `ask` says "only a model reading backs this" and names `payroll_from_hiring_plan_and_rerun_cash` as not run.
- **Brasswick, relabelled by the memo step.** Run the same four commands on `data_room/brasswick`, then `control.sh api GET /api/rooms/brasswick/readout`. The one claim with `scan` `claims` and a non-empty `conflicts_with` is the slide 4 chart months (`redflags` `deck_history_vs_metrics`, which quotes the same slide words). In the "claims table" Panel, the rows for slide 4 `$943K` and slide 10 `29` and `$113,684` keep their label, and their `disagrees` column says the `gross_vs_net_revenue` or `contractor_spend_vs_headcount_and_burn` check "raises a problem with this figure, not compared figure to figure". Counts: 51 claims, 24 supported, 3 contradicted, 24 unsupported, 6 not counted.
- **Score.** Run `control.sh cli python3 -m eval.score data_room/brasswick`: `found 5 of 5; decoys flagged 0 of 3`. On `data_room/hollis_voice` the transcript has `found  PF2b` and `decoys flagged 0 of 3`.
- **Clean room stays clear.** Run the four commands on `data_room/hollis_voice_clean`. Counts: 0 contradicted. `eval.score` says `decoys flagged 0 of 3`.
- **Seed drop names what is missing.** Run them on `data_room/hollis_voice_seed_drop`. The claims result has a gap whose `why` contains `file missing: monthly revenue by customer`.

## Gotchas

- `scans.memo.claim_support` exits 2 with `no readout at ...` until `scans.memo` ran on the room in this run.
- The video is not recorded, so spoken claims cite the script by `line N`. A saved `01_overview/pitch_video.transcript.json` replaces them with `seg N` claims; the partial-room tests in `scans/claims/tests/test_inputs.py` prove that shape with a hand-built transcript.
- Since 2026-10-23 `scans.memo` already runs the step (it is in `scans/memo/merge.py` STEPS); running the command after it changes nothing.
- Without `ANTHROPIC_API_KEY` (always, under `control.sh`), the model reading is one gap, "no ANTHROPIC_API_KEY, so the model reading did not run". That is expected, not a failure.
- Hollis Voice scores 2 of 8 from these scans: PF6 and PF4's runway and burn read unsupported (backed only by the model, with a note in the ask column) until the red-flag engine's rebuild checks exist, and the key credits the rest (PF2, PF4, PF5 and PF7 among the ones this scan contradicts) to other checks' names.
