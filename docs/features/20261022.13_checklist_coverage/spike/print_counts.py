"""Print the coverage counts table the feature docs quote, from spike/out/*.json.

Run from the repo root, after run_all.sh:
    python3 docs/features/20261022.13_checklist_coverage/spike/print_counts.py
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "out"
RUNS = [("Seed drop, Series A (deck's stage, 4 sample gaps)", "seed_drop_series_a.json"),
        ("Seed drop, seed (operator)", "seed_drop_seed.json"),
        ("Seed drop, pre-seed (operator)", "seed_drop_pre_seed.json"),
        ("Seed drop, Series A, no sample gaps", "seed_drop_auto.json"),
        ("Full room, Series A (deck's stage)", "full_room_series_a.json"),
        ("Full room, seed (operator)", "full_room_seed.json"),
        ("Full room, pre-seed (operator)", "full_room_pre_seed.json"),
        ("Brasswick, seed (deck's stage)", "brasswick_auto.json")]
COLS = ["expected", "checked", "found", "missing", "not_checked", "not_expected", "ask_lines",
        "ask_lines_if_you_have_it", "ask_lines_after_term_sheet", "asks_suppressed_later_stage", "duplicate_requests",
        "missing_without_ask"]
print("| Run | " + " | ".join(COLS) + " | missing documents / checks / asks |")
print("|---|" + "---|" * (len(COLS) + 1))
for name, f in RUNS:
    c = json.loads((OUT / f).read_text())["counts"]
    m = c["missing_by_kind"]
    print(f"| {name} | " + " | ".join(str(c[k]) for k in COLS) + f" | {m['document']} / {m['check']} / {m['ask']} |")
