"""Read the roadmap's slice files back into the one-file shape the checkers parse.

The roadmap was one long ROADMAP.md until 2026-10-24. Now ROADMAP.md is the plan
at a glance, and each slice lives in docs/ongoing/roadmap/<slice>.md, with
saturday.md and asks.md beside them. This module rebuilds the old layout in
memory, so check_asks_table.py and check_saturday_hours.py keep their rules:

  ## <horizon>                  from each slice file's "- **Horizon:**" line
  ### <slice>                   then the slice file's text under "## Detail"
  ## Saturday notes             then saturday.md, its "## " headings as "### "
  ## Ken's asks and where they are built
                                then asks.md's text

Links to a slice file, `](<slice>.md)`, read as `](#<slice>)`, the in-page
anchors the checkers expect.
"""

import re
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[2] / "ongoing" / "roadmap"
HORIZONS = ["Now to Friday night", "Saturday"]
ASKS_HEADING = "## Ken's asks and where they are built"


def slice_files():
    out = {}
    for f in sorted(FOLDER.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        m = re.search(r"^- \*\*Horizon:\*\* (.+)$", text, re.M)
        if m and "\n## Detail\n" in text:
            out[f.stem] = (m.group(1).strip(), text.split("\n## Detail\n", 1)[1])
    return out


def _anchors(text, names):
    def fix(m):
        name, rest = m.group(1), m.group(2) or ""
        return f"](#{name})" if name in names and not rest else m.group(0)
    return re.sub(r"\]\(([a-z0-9-]+)\.md(#[^)]*)?\)", fix, text)


def lines():
    files = slice_files()
    names = set(files)
    out = []
    for horizon in HORIZONS:
        out.append(f"## {horizon}")
        for name, (h, body) in files.items():
            if h == horizon:
                out.append(f"### {name}")
                out.extend(_anchors(body, names).splitlines())
    out.append("## Saturday notes")
    for line in (FOLDER / "saturday.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            continue
        out.append("#" + line if line.startswith("## ") else _anchors(line, names))
    out.append(ASKS_HEADING)
    for line in (FOLDER / "asks.md").read_text(encoding="utf-8").splitlines()[1:]:
        out.append(_anchors(line, names))
    return out
