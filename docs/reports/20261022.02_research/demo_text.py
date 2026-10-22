"""Print the visible text of a saved page under raw/demo_companies/ (HTML or HN Algolia item JSON).

Run: python3 -I demo_text.py FILE [max_chars]
For an HN item, prints the story text and every comment with its author and id.
"""
import html
import json
import pathlib
import re
import sys

RAW = pathlib.Path(__file__).resolve().parent / "raw" / "demo_companies"


def to_text(raw):
    raw = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</p>|</h[1-6]>|</li>|</div>|</blockquote>", "\n", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    raw = re.sub(r"[ \t]+", " ", raw)
    return re.sub(r"\n\s*\n+", "\n", raw).strip()


def walk(item, depth, out):
    t = to_text(item.get("text") or "")
    if t or item.get("title"):
        out.append(f"{'  ' * depth}[{item.get('id')}] {item.get('author')}: {item.get('title') or ''} {t}")
    for c in item.get("children") or []:
        walk(c, depth + 1, out)


def main():
    path = RAW / sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
    raw = path.read_text(errors="replace")
    if path.suffix == ".json" and raw.lstrip().startswith("{") and '"children"' in raw:
        out = []
        walk(json.loads(raw), 0, out)
        print("\n".join(out)[:limit])
    else:
        print(to_text(raw)[:limit])


if __name__ == "__main__":
    main()
