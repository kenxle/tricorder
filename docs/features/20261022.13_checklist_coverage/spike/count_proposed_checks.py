"""Count the checks the document guides propose, to size the guides' part of the plan.

Run from the repo root:
    python3 docs/features/20261022.13_checklist_coverage/spike/count_proposed_checks.py

Inside each guide's "How Tricorder checks it" section, the sub-blocks start with a heading or a
bold line. In the block about scripts, a bullet is "existing" when it names a FRAMEWORKS entry
(for example "1.4", "entry 1.12", "(exists") and "proposed" otherwise. Bullets in the block about
what Tricorder cannot check are "operator" items. Model-reading bullets are counted apart.
The counts are approximate: the guides were written by different agents and their shapes vary.
"""
import re
from pathlib import Path

GUIDES = Path(__file__).resolve().parents[4] / "docs/reports/20261022.03_document_guides"
EXISTING = re.compile(r"(^|\W)(entry\s+)?\d\.\d{1,2}\b|\(exists|already defined", re.I)
HEAD = re.compile(r"^\s*(#{3,4}\s+(.*)|\*\*(.*?)\*\*\s*:?\s*)$")
tot = {"existing": 0, "proposed": 0, "model": 0, "operator": 0}
for g in sorted(GUIDES.glob("*.md")):
    if g.name in ("INDEX.md", "00_brief.md"):
        continue
    sec = re.search(r"^## [^\n]*How Tricorder checks it[^\n]*\n(.*?)(?=^## |\Z)", g.read_text(), re.S | re.M)
    c = {"existing": 0, "proposed": 0, "model": 0, "operator": 0}
    block = None
    for line in (sec.group(1).splitlines() if sec else []):
        h = HEAD.match(line)
        if h:
            t = (h.group(2) or h.group(3) or "").lower()
            block = "script" if "script" in t else "model" if "model" in t else \
                    "operator" if ("cannot" in t or "operator" in t) else None
            continue
        if not re.match(r"^\s*[-*]\s", line) or block is None:
            continue
        if block == "script":
            c["existing" if EXISTING.search(line[:120]) else "proposed"] += 1
        else:
            c[block] += 1
    for k in tot:
        tot[k] += c[k]
    print(f"{g.name}: " + " ".join(f"{k}={v}" for k, v in c.items()) + ("" if sec else " (no section)"))
print("TOTAL guides=33 " + " ".join(f"{k}={v}" for k, v in tot.items()))
