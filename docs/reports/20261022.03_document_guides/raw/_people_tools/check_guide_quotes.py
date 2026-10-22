"""Lists every double-quoted string in a guide that is not inside a verified quote in quotes_people.csv.
Run: python3 -I check_guide_quotes.py founder-bios
Strings that are not source quotes (room text, check names in code ticks) are reviewed by hand.
"""
import csv, html, pathlib, re, sys

BASE = pathlib.Path("/Users/kennethstclair/Documents/workspace/tricorder/docs/reports/20261022.03_document_guides")

def norm(s):
    s = html.unescape(s)
    s = (s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"'))
    return re.sub(r"\s+", " ", s).strip().lower()

slug = sys.argv[1]
verified = [norm(r["text"]) for r in csv.DictReader(open(BASE / "quotes_people.csv"))
            if r["kind"] == "quote" and r["verified"] == "yes" and r["guide"] == slug]
text = (BASE / f"{slug}.md").read_text()
text = re.sub(r"`[^`]*`", "", text)
found = []
for line in text.splitlines():
    found += re.findall(r'"([^"]{3,}?)"', line)
missing = []
for f in found:
    n = norm(f).strip(" .,;:")
    if not any(n in v for v in verified):
        missing.append(f)
print(f"{slug}: {len(found)} quoted strings, {len(missing)} not inside a verified quote")
for m in missing: print("  -", m[:160])
