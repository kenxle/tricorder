"""Count the roadmap's slices by status, from status.csv (one row per slice).

Run: python3 docs/ongoing/roadmap/status_counts.py
It also fails if a slice file has no status row, or a status row has no file.
"""

import csv
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader(open(HERE / "status.csv", encoding="utf-8")))
names = {r["slice"] for r in rows}
files = {f.stem for f in HERE.glob("*.md") if "\n## Detail\n" in f.read_text(encoding="utf-8")}
counts = Counter(r["status"] for r in rows)
print(f"{len(rows)} slices")
for status, n in counts.most_common():
    print(f"  {status}: {n}")
if names != files:
    print("FAIL: status rows and slice files differ:", sorted(names ^ files))
    sys.exit(1)
print("PASS: every slice file has one status row")
