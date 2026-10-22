"""Count the items in checklist.csv.

Run: python3 docs/ongoing/checklist_counts.py

Prints counts by readout piece, by kind, by stage expectation, by where the item
comes from, and by whether a check exists. CHECKLIST.md quotes this output.
"""
import csv
from collections import Counter
from pathlib import Path

CSV = Path(__file__).with_name("checklist.csv")

PIECES = ["traction and revenue", "retention", "burn and runway", "unit economics",
          "customers and contracts", "market", "comps", "team", "the pitch itself",
          "legal and cap table", "AI and data governance", "outside world"]
STAGES = [("pre_seed", "Pre-seed"), ("seed", "Seed"), ("series_a", "Series A")]
LEVELS = ["yes", "lighter", "no", "not stated"]
STATUSES = ["Saturday", "after Saturday", "not checked yet"]


def show(title, counter, order):
    print(f"\n{title}")
    for key in order:
        print(f"  {key}: {counter.get(key, 0)}")
    extra = set(counter) - set(order)
    if extra:
        raise SystemExit(f"unexpected values in {title}: {sorted(extra)}")


def main():
    with open(CSV, newline="") as fh:
        rows = list(csv.DictReader(fh))

    print(f"Items: {len(rows)}")
    show("By piece", Counter(r["piece"] for r in rows), PIECES)
    show("By kind", Counter(r["kind"] for r in rows), ["document", "check", "outside", "ask"])
    show("By where it comes from", Counter(r["comes_from"] for r in rows), ["data room", "outside", "founder"])

    print("\nBy stage expectation")
    print("  stage: " + ", ".join(LEVELS))
    for key, name in STAGES:
        c = Counter(r[key] for r in rows)
        extra = set(c) - set(LEVELS)
        if extra:
            raise SystemExit(f"unexpected stage values: {sorted(extra)}")
        print(f"  {name}: " + ", ".join(str(c.get(level, 0)) for level in LEVELS))

    show("By whether a check exists", Counter(r["check_exists"] for r in rows), ["yes", "no"])
    show("By check status", Counter(r["check_status"] for r in rows), STATUSES)

    print("\nNo check yet, by piece")
    c = Counter(r["piece"] for r in rows if r["check_exists"] == "no")
    for piece in PIECES:
        print(f"  {piece}: {c.get(piece, 0)}")


if __name__ == "__main__":
    main()
