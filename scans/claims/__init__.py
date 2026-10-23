"""The claims workflow (docs/ongoing/diagrams/claims_workflow.md; ROADMAP "claim-support").

Every figure on every slide of the deck and in every sentence of the pitch
video (or, until it is recorded, its script) becomes one claim, labelled
supported, contradicted or unsupported against the rest of the room.

    numbers.py   find each printed or spoken figure
    extract.py   statements from the deck, the claims page, claims.json, the transcript or script
    kinds.py     what each figure is about, and the evidence map per kind
    evidence.py  the readers that say what each document states
    label.py     normalise, compare, label; the claims table Panel
    read.py      the model reading of slides with no figure a script can parse
    scan.py      run(room_dir) -> ScanResult

The memo step scans/memo/claim_support.py relabels against other scans' claims.
"""
