"""Check the "Ken's asks and where they are built" table in ROADMAP.md.

For every row it confirms:
  - the row links to at least one slice;
  - every link is an in-page anchor that matches a slice heading in the file;
  - the "When it is built" column names the horizon of each linked slice, in
    link order, with repeats next to each other collapsed
    (for example "Now to Friday night, then Saturday").

A slice is a level-3 heading whose name is lowercase words joined by hyphens
and whose section has a "**Who:**" line. Its horizon is the level-2 section it
sits under: "Now to Friday night" or "Saturday".

Run: python3 docs/features/20261022.01_hackathon_plan/check_asks_table.py
Exits 0 when every row passes, 1 otherwise.
"""

import re
import sys
from pathlib import Path

ROADMAP = Path(__file__).resolve().parents[2] / "ongoing" / "ROADMAP.md"
TABLE_HEADING = "## Ken's asks and where they are built"
SLICE_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK = re.compile(r"\]\(#([^)]+)\)")


def horizon_for(h2):
    text = h2.lower()
    if text.startswith("now to friday night"):
        return "Now to Friday night"
    if text.startswith("saturday"):
        return "Saturday"
    return None


def find_slices(lines):
    slices = {}
    h2 = None
    current = None
    for line in lines:
        if line.startswith("## "):
            h2 = line[3:].strip()
            current = None
        elif line.startswith("### "):
            name = line[4:].strip()
            current = name if SLICE_NAME.match(name) else None
            if current:
                slices[current] = {"horizon": horizon_for(h2), "has_who": False}
        elif current and line.startswith("**Who:**"):
            slices[current]["has_who"] = True
    return {n: s["horizon"] for n, s in slices.items() if s["has_who"]}


def table_rows(lines):
    try:
        start = lines.index(TABLE_HEADING)
    except ValueError:
        sys.exit(f"FAIL: heading not found: {TABLE_HEADING}")
    rows = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        if line.startswith("|"):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows[2:]  # skip the header and separator lines


def main():
    lines = ROADMAP.read_text(encoding="utf-8").splitlines()
    slices = find_slices(lines)
    rows = table_rows(lines)
    problems = []
    for i, cells in enumerate(rows, start=1):
        if len(cells) != 3:
            problems.append(f"row {i}: expected 3 cells, found {len(cells)}")
            continue
        ask, slice_cell, when_built = cells
        anchors = LINK.findall(slice_cell)
        if not anchors:
            problems.append(f"row {i} ({ask}): no slice link")
            continue
        horizons = []
        for anchor in anchors:
            if anchor not in slices:
                problems.append(f"row {i} ({ask}): #{anchor} is not a slice heading")
                continue
            h = slices[anchor]
            if not horizons or horizons[-1] != h:
                horizons.append(h)
        expected = ", then ".join(horizons)
        if horizons and when_built != expected:
            problems.append(
                f"row {i} ({ask}): when-built says '{when_built}', slices say '{expected}'"
            )
    print(f"{len(slices)} slices found in {ROADMAP.name}")
    print(f"{len(rows)} rows in the asks table")
    if problems:
        for p in problems:
            print("FAIL:", p)
        sys.exit(1)
    print("PASS: every row links to a slice that exists, and every horizon matches")


if __name__ == "__main__":
    main()
