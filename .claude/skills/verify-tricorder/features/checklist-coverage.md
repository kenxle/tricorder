# Checklist coverage and the ask list

When the readout is built, every item on the diligence checklist gets one status for the company's stage: checked by a scan, found in the room, missing, not checked yet, or not expected at this stage. Every missing item becomes one line to ask the founder for, beside the lines from scan gaps, and no request appears twice.

## Sub-features

- `cc-stage` reads the stage from the deck's round slide, or from the operator's choice.
- `cc-status` gives each checklist item one status, with the scan or file behind it.
- `cc-asks` turns missing items into ask lines, marked "if you have it" or "after the term sheet" where the checklist says so.
- `cc-dedupe` keeps one line when a gap and a checklist item ask for the same thing.
- `cc-panels` writes the panels `checklist coverage`, `checklist coverage counts` and `checklist ask lines`.

## How to get to it (user POV)

- Build the readout: `python3 -m scans.memo <room>`, or `bin/smoke <room>` for scans plus memo.
- Through the API: `POST /api/rooms/<room>/readout`, then `GET /api/rooms/<room>/readout`.
- On the readout page, the section `aria-label="Ask list"`.

## Driving it with control.sh

Preconditions:

- `control.sh doctor` prints `OK` for this run.

- **Run the scans and the memo on the seed drop.** Run `control.sh cli bin/smoke data_room/hollis_voice_seed_drop`. Exit code 0.
- **Read the counts.** Run `control.sh api GET /api/rooms/hollis_voice_seed_drop/readout`. The panel `checklist coverage counts` has `stage` `series_a`, `stage_set_by` `deck`, and a `stage_source` quoting `01_overview/pitch_deck.pdf, slide 1`. Its `items` equals the number of rows in `docs/ongoing/checklist.csv`.
- **Read the asks.** In the same response, `asks` holds lines with `from_kind` `checklist` and a `checklist_id`. No two lines share the same `what`. The count matches the panel's `ask_lines`.
- **Change the stage.** Write `{"stage": "pre_seed"}` to `<run>/out/hollis_voice_seed_drop/operator.json`, then run `control.sh api POST /api/rooms/hollis_voice_seed_drop/readout`. The counts panel shows `stage_set_by` `operator`, and items expected only at a later stage leave the ask list.
- **Full room.** Run `control.sh cli bin/smoke data_room/hollis_voice` and read its readout. Fewer items are missing than on the seed drop, because the full room holds the customer files.
- **On the page.** Run `control.sh shot coverage-asks`. The DOM has the section `aria-label="Ask list"` with the ask lines for `hollis_voice`.

## Gotchas

- "Checked" counts only checks that ran in this run. Run the scans before the memo, or every check item reads "not checked yet".
- Ken's checklist grew to 193 items on 2026-10-22. Items C110 to C193 have no file-matching rules yet, so they never read "found".
- The operator's stage lives in this run's `out/`, so it does not leak into Ken's instance. Remove it from the run folder list at cleanup, not by hand.
- The readout page has no coverage panel yet. The panels are in the readout JSON.
