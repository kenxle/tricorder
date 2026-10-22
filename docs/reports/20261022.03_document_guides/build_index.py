"""Write INDEX.md: one row per document guide, with its group and first sentence of 'What it is'."""
import csv, glob, os, re
here = os.path.dirname(os.path.abspath(__file__))
groups = {}
for q in glob.glob(os.path.join(here, "quotes_*.csv")):
    g = os.path.basename(q)[7:-4]
    with open(q) as f:
        for row in csv.DictReader(f):
            groups.setdefault(row["guide"].strip().removesuffix(".md"), g)
rows = []
for p in sorted(glob.glob(os.path.join(here, "*.md"))):
    slug = os.path.basename(p)[:-3]
    if slug.startswith("00_") or slug == "INDEX":
        continue
    t = open(p).read()
    title = re.search(r"^# (.+)$", t, re.M).group(1).strip()
    m = re.search(r"##\s*1?\.?\s*What it is\s*\n+(.+?)(?<=[.!?])\s", t, re.S)
    first = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    first = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", first)
    rows.append((groups.get(slug, "?"), title, slug, first))
rows.sort()
out = ["# Document guides", "", f"One guide per document a seed or Series A data room can hold. {len(rows)} guides, listed by group. Written from [the brief](00_brief.md); this index is built by [build_index.py](build_index.py).", ""]
cur = None
for g, title, slug, first in rows:
    if g != cur:
        out += ["", f"## {g.capitalize()}", "", "| Guide | What it is |", "|---|---|"]
        cur = g
    out.append(f"| [{title}]({slug}.md) | {first.replace('|', '/')} |")
open(os.path.join(here, "INDEX.md"), "w").write("\n".join(out) + "\n")
print(len(rows), "guides indexed;", sum(1 for r in rows if r[0] == "?"), "without a group;", sum(1 for r in rows if not r[3]), "without a first sentence")
