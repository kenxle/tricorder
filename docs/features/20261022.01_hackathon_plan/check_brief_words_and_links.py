"""Count the product brief's words (Charter excluded) and check relative links
in PRODUCT_BRIEF.md and FEATURES.md: the file exists, and a #anchor matches a heading."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ONGOING = ROOT / "docs" / "ongoing"


def slug(heading):
    h = heading.strip().lower()
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")


def anchors(path):
    out = set()
    for line in path.read_text().splitlines():
        m = re.match(r"^#{1,6}\s+(.*)$", line)
        if m:
            out.add(slug(m.group(1)))
    return out


def brief_words():
    text = (ONGOING / "PRODUCT_BRIEF.md").read_text()
    start = text.index("## Charter")
    end = text.index("\n## ", start + 1)
    body = text[:start] + text[end:]
    body = re.sub(r"\]\([^)]*\)", "]", body)
    return len(re.findall(r"[A-Za-z0-9$][\w$'’.,%-]*", body))


def check_links(path):
    problems, count = [], 0
    for n, line in enumerate(path.read_text().splitlines(), 1):
        for target in re.findall(r"\]\(([^)\s]+)\)", line):
            if re.match(r"^[a-z]+:", target):
                continue
            count += 1
            file_part, _, anchor = target.partition("#")
            dest = (path.parent / file_part).resolve() if file_part else path
            if not dest.exists():
                problems.append(f"{path.name}:{n} missing file {target}")
                continue
            if anchor and dest.suffix == ".md" and anchor not in anchors(dest):
                problems.append(f"{path.name}:{n} missing anchor {target}")
    return count, problems


print(f"PRODUCT_BRIEF.md words, Charter excluded, link URLs excluded: {brief_words()}")
bad = 0
for name in ("PRODUCT_BRIEF.md", "FEATURES.md"):
    count, problems = check_links(ONGOING / name)
    print(f"{name}: {count} relative links checked, {len(problems)} broken")
    for p in problems:
        print("  " + p)
    bad += len(problems)
sys.exit(1 if bad else 0)
