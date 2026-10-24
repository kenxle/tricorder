"""Check every relative Markdown link under docs/ and in AGENTS.md.

A link passes when its file exists and, for a link into a Markdown file with
#anchor, the anchor matches a heading in that file (GitHub's slug rule:
lowercase, punctuation dropped, spaces to hyphens). Web links, mailto links and
links inside code spans or code blocks are skipped.

Run: python3 docs/features/20261022.01_hackathon_plan/check_doc_links.py [path ...]
With paths, it checks only those files or folders. Exits 0 when every link passes.
"""

import re
import sys
from pathlib import Path
from urllib.parse import unquote

REPO = Path(__file__).resolve().parents[3]
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIP_DIRS = {"node_modules", ".git", "raw", "__pycache__"}


def slug(heading):
    h = heading.strip().lower()
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")


def anchors(path, cache={}):
    if path not in cache:
        found, fence = set(), False
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("```"):
                fence = not fence
            elif not fence and line.startswith("#"):
                found.add(slug(line.lstrip("#")))
        cache[path] = found
    return cache[path]


def links(path):
    fence = False
    for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if line.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        line = re.sub(r"`[^`]*`", "", line)
        for m in LINK.finditer(line):
            yield n, m.group(1)


def files(args):
    roots = [Path(a).resolve() for a in args] or [REPO / "docs", REPO / "AGENTS.md"]
    for r in roots:
        if r.is_file():
            yield r
        else:
            for f in sorted(r.rglob("*.md")):
                if not SKIP_DIRS & set(f.relative_to(r).parts):
                    yield f


def main(args):
    bad = checked = 0
    for f in files(args):
        for n, url in links(f):
            if url.startswith(("http://", "https://", "mailto:")):
                continue
            checked += 1
            target, _, anchor = url.partition("#")
            dest = (f.parent / unquote(target)).resolve() if target else f
            problem = None
            if not dest.exists():
                problem = "no such file"
            elif anchor and dest.suffix == ".md" and slug(unquote(anchor)) not in anchors(dest):
                problem = f"no heading #{anchor}"
            if problem:
                bad += 1
                print(f"{f.relative_to(REPO)}:{n}: {url}: {problem}")
    print(f"{checked} relative links checked, {bad} broken")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
