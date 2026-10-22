"""Flatten saved HN Algolia JSON into one readable digest (raw/voc/hn_digest.txt).

Each entry: object id, author, date, permalink, and the plain comment text.
Run: python3 -I hn_digest.py
"""
import html
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / "raw" / "voc"

KEEP = re.compile(
    r"diligence|data room|memo|red flag|associate|cohort|churn|ARR|recurring|angel|"
    r"accelerator|application|pitchbook|crunchbase|spreadsheet|model|deck|fraud|"
    r"financials|metrics|analyst|partner",
    re.I,
)


def clean(text):
    text = re.sub(r"<p>", "\n", text or "")
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def main():
    seen = set()
    lines = []
    for path in sorted(RAW.glob("hn_*.json")):
        data = json.loads(path.read_text())
        for hit in data.get("hits", []):
            oid = hit.get("objectID")
            if oid in seen:
                continue
            seen.add(oid)
            body = clean(hit.get("comment_text") or hit.get("story_text") or "")
            title = hit.get("title") or hit.get("story_title") or ""
            if not KEEP.search(body + " " + title):
                continue
            lines.append(
                f"=== {oid} | {hit.get('author')} | {hit.get('created_at','')[:10]} | "
                f"https://news.ycombinator.com/item?id={oid} | src={path.name}\n"
                f"TITLE: {title}\nURL: {hit.get('url') or ''}\n{body}\n"
            )
    out = RAW / "hn_digest.txt"
    out.write_text("\n".join(lines))
    print(len(lines), "entries written to", out)


if __name__ == "__main__":
    main()
