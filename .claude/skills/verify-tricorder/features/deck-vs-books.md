# Deck against books

The red-flag engine matches every revenue figure in the pitch deck to the same period in the monthly P&L, checks that a revenue chart follows the P&L's shape, and reports a chart that leaves out months the books hold. Each finding is a claim with the deck slide and the P&L cell as sources.

## Sub-features

- `dvb-figure` matches each deck revenue figure (ARR, MRR, last-12-months revenue, plan growth) to its P&L period and flags a gap above tolerance.
- `dvb-shape` checks that a revenue chart's bars follow the P&L month by month.
- `dvb-history` reports a chart that starts late, ends early or skips months, with what the left-out months hold. A climb is a watch; a dip or a flat stretch is a flag.
- `dvb-gap` writes a gap, not a crash, when the P&L or a revenue cell is missing.

## How to get to it (user POV)

- Run the red-flag scan on a room: `python3 -m scans.redflags <room>`.
- Run every scan and the memo: `bin/smoke <room>`.
- Through the API: `POST /api/rooms/<room>/scans/redflags`, then `GET /api/rooms/<room>/results/redflags`.

## Driving it with control.sh

Preconditions:

- `control.sh doctor` prints `OK` for this run.

- **Run the scan on Hollis Voice.** Run `control.sh cli python3 -m scans.redflags data_room/hollis_voice`. Exit code 0.
- **Read the figure flag.** Run `control.sh api GET /api/rooms/hollis_voice/results/redflags`. One claim with `check.name` `deck_revenue_vs_pnl` and severity `flag` says the deck's ARR of $2,500,000 (slide 3) differs from the P&L's $2,240,868, a gap of 11.6%, citing `01_overview/pitch_deck.pdf` slide 3 and `02_financials/financial_model.xlsx` `P&L!W10`.
- **Check the shape and history are clear.** In the same response, the `deck_revenue_vs_pnl` claim about the slide 3 chart and the `deck_history_vs_metrics` claim are severity `info`: 21 bars for 2025-01 to 2026-09, starting at the first revenue month.
- **Prove a source.** Run `control.sh api POST /api/rooms/hollis_voice/source '<that claim's P&L source object>'`. The returned text contains the source's `quote`.
- **Run Brasswick.** Run `control.sh cli python3 -m scans.redflags data_room/brasswick`, then `control.sh api GET /api/rooms/brasswick/results/redflags`. A `deck_history_vs_metrics` claim with severity `flag` says the slide 4 chart starts at 2026-01, 8 months after the first revenue month.
- **Score Brasswick.** Build the readout first with `control.sh cli python3 -m scans.memo data_room/brasswick`, then run `control.sh cli python3 -m eval.score data_room/brasswick`. The transcript has `found  BF2`.
- **Clean room stays clear.** Run the scan on `data_room/hollis_voice_clean` and read its result. Every `deck_revenue_vs_pnl` and `deck_history_vs_metrics` claim is severity `info`; the deck's ARR of $2,060,868 matches the P&L.

## Gotchas

- Results go to this run's `out/`, so `GET .../results/redflags` returns 404 until the scan ran in this run.
- The late-start and quarterly test decks exist only inside the unit tests (`scans/redflags/tests/test_deck_vs_books.py`), built in a temporary folder. There is no room for them in `data_room/`.
- Those tests skip when matplotlib, reportlab or pypdf is missing. A skip is not a pass.
- The deck ARR flag and the engine's PF2 flag (deck against the model) describe the same ARR. The answer key credits PF2 to `deck_claim_vs_named_cell`, so this flag does not raise Hollis Voice's score.
