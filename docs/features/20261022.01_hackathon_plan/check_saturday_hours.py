"""Check that Saturday's hours in ROADMAP.md add up.

For each role it confirms:
  - the "Hours" lines of the Saturday slices that role owns add up to the build
    window (10:30 AM to the 3:30 PM freeze, less the half-hour lunch);
  - the "Who owns what" table lists the same slices and the same total;
  - the run of show gives each slice the same hours its "Hours" line gives.

It also checks every "Waits on" line in the file: each slice name it mentions must
be a slice heading, and it prints the gap between the Luma page's nine hours and
the schedule's six-hour hacking window.

A slice is a level-3 heading whose name is lowercase words joined by hyphens and
whose section has a "**Who:**" line. Times in the run of show are read from its
first column ("10:30 to 11:30"). A cell that names two slices gives the later one
its stated hours and the first one the rest of the cell.

Run: python3 docs/features/20261022.01_hackathon_plan/check_saturday_hours.py
Exits 0 when every check passes, 1 otherwise.
"""

import re
import sys
from pathlib import Path

ROADMAP = Path(__file__).resolve().parents[2] / "ongoing" / "ROADMAP.md"
SLICE_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)+$|^[a-z0-9]+$")
ROLES = ["captain", "frontend", "backend-and-data", "design-and-finance"]
# Hyphenated words in Waits on lines that are plain English or role names, not slices.
NOT_SLICES = set(ROLES) | {"30-document", "mail-receiving", "non-commercial", "earliest-stage"}

# The schedule: hacking 10:30 AM to 4:30 PM, lunch inside it. The roadmap freezes
# the demo at 3:30 PM and puts lunch at 12:30 to 1:00 PM.
BUILD_START, FREEZE, LUNCH = 10.5, 15.5, 0.5
HACK_END = 16.5
LUMA_HOURS = 9


def clock(text):
    """'10:30' -> 10.5, using the afternoon for 1 to 6 o'clock."""
    h, m = text.split(":")
    h = int(h)
    if h < 9:
        h += 12
    return h + int(m) / 60


def parse_slices(lines):
    slices, h2, cur = {}, None, None
    for line in lines:
        if line.startswith("## "):
            h2, cur = line[3:].strip(), None
        elif line.startswith("### "):
            name = line[4:].strip()
            cur = name if SLICE_NAME.match(name) else None
            if cur:
                slices[cur] = {"h2": h2, "who": None, "hours": None, "extra": None, "waits": ""}
        elif cur and line.startswith("**Who:**"):
            slices[cur]["who"] = line
        elif cur and line.startswith("**Hours:**"):
            nums = re.findall(r"(\d+(?:\.\d+)?)", line.split("(")[0])
            slices[cur]["hours"] = float(nums[0])
            plus = re.search(r"plus (\d+(?:\.\d+)?) for all four", line)
            slices[cur]["extra"] = float(plus.group(1)) if plus else None
        elif cur and line.startswith("**Waits on:**"):
            slices[cur]["waits"] = line
    return slices


def table(lines, heading_prefix):
    start = next(i for i, l in enumerate(lines) if l.startswith(heading_prefix))
    rows = []
    for line in lines[start + 1:]:
        if line.startswith("#"):
            break
        if line.startswith("|"):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows[2:]


def main():
    lines = ROADMAP.read_text(encoding="utf-8").splitlines()
    slices = parse_slices(lines)
    problems = []
    window = FREEZE - BUILD_START - LUNCH
    print(f"Build window per role: {BUILD_START} to {FREEZE} less {LUNCH} lunch = {window} hours")
    print(f"Hacking window by the schedule: {HACK_END - BUILD_START} hours; Luma page: {LUMA_HOURS}; "
          f"gap {LUMA_HOURS - (HACK_END - BUILD_START)} hours")

    saturday = {n: s for n, s in slices.items() if s["h2"] and s["h2"].startswith("Saturday")}
    owner = {}
    for name, s in saturday.items():
        if s["hours"] is None:
            problems.append(f"{name}: Saturday slice with no Hours line")
            continue
        role = next((r for r in ROLES if s["who"] and f"**Who:** {r}" in s["who"]), None)
        if role is None:
            problems.append(f"{name}: Who line names no single role: {s['who']}")
            continue
        owner[name] = role

    sums = {r: 0.0 for r in ROLES}
    for name, role in owner.items():
        sums[role] += saturday[name]["hours"]

    owns = {r[0]: r for r in table(lines, "### Who owns what")}
    total = 0.0
    for role in ROLES:
        mine = sorted(n for n, r in owner.items() if r == role)
        listed = sorted(x.strip() for x in owns[role][2].split(","))
        stated = float(owns[role][3])
        total += sums[role]
        print(f"{role}: {', '.join(f'{n} {saturday[n]['hours']}' for n in mine)} = {sums[role]}")
        if abs(sums[role] - window) > 1e-9:
            problems.append(f"{role}: slices add to {sums[role]}, window is {window}")
        if listed != mine:
            problems.append(f"{role}: owners table lists {listed}, slices say {mine}")
        if abs(stated - sums[role]) > 1e-9:
            problems.append(f"{role}: owners table says {stated} hours, slices add to {sums[role]}")
    print(f"All four roles: {total} person-hours")

    # Run of show.
    show = table(lines, "### Run of show")
    got = {}
    rehearsal = 0.0
    for row in show:
        m = re.match(r"(\d+:\d\d) to (\d+:\d\d)", row[0])
        if not m:
            continue
        a, b = clock(m.group(1)), clock(m.group(2))
        if a >= FREEZE and b <= HACK_END and "Rehearse" in row[1]:
            rehearsal += b - a
        if a < BUILD_START or b > FREEZE:
            continue
        for role, cell in zip(ROLES, row[1:5]):
            mine = [n for n, r in owner.items() if r == role]
            named = [n for n in sorted(mine, key=lambda n: cell.find(n)) if re.search(rf"(?<![a-z-]){re.escape(n)}(?![a-z-])", cell)]
            if not named:
                continue
            left = b - a
            for later in named[1:]:
                got[(role, later)] = got.get((role, later), 0) + saturday[later]["hours"]
                left -= saturday[later]["hours"]
            got[(role, named[0])] = got.get((role, named[0]), 0) + left
    for name, role in owner.items():
        h = got.get((role, name), 0.0)
        if abs(h - saturday[name]["hours"]) > 1e-9:
            problems.append(f"run of show gives {role} {h} hours on {name}; its Hours line says {saturday[name]['hours']}")
    print(f"Run of show: every slice's hours match its Hours line" if not any(p.startswith("run of show") for p in problems) else "Run of show: mismatches below")
    extra = saturday.get("demo-freeze", {}).get("extra")
    print(f"Rehearsal after the freeze: {rehearsal} hours for all four; demo-freeze says {extra}")
    if extra is not None and abs(rehearsal - extra) > 1e-9:
        problems.append(f"rehearsal rows add to {rehearsal}, demo-freeze says {extra}")

    # Waits on lines.
    names = set(slices)
    for name, s in slices.items():
        for tok in re.findall(r"(?<![A-Za-z#/_.-])([a-z0-9]+(?:-[a-z0-9]+)+)(?![A-Za-z_.-])", s["waits"]):
            if tok not in names and tok not in NOT_SLICES:
                problems.append(f"{name}: Waits on names '{tok}', which is not a slice")
    for name, s in slices.items():
        for anchor in re.findall(r"\]\(#([^)]+)\)", s["waits"]):
            if anchor not in names:
                problems.append(f"{name}: Waits on links #{anchor}, which is not a slice")
    print(f"Waits on: checked {sum(1 for s in slices.values() if s['waits'])} lines against {len(names)} slices "
          f"(words treated as plain English: {', '.join(sorted(NOT_SLICES - set(ROLES)))})")

    if problems:
        for p in problems:
            print("FAIL:", p)
        sys.exit(1)
    print("PASS: every role's hours fill its window, the owners table and the run of show agree")


if __name__ == "__main__":
    main()
