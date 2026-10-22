"""Checks each quote word for word against the saved page, then writes quotes_people.csv.
Run: python3 -I build_quotes_people.py
A quote is verified when its text, after unifying curly quotes and collapsing white space,
is found inside the saved file's text. HN .json files are read comment by comment.
Paraphrase rows are not checked word for word and are written with verified = no.
"""
import csv, html, json, pathlib, re, sys

BASE = pathlib.Path("/Users/kennethstclair/Documents/workspace/tricorder/docs/reports/20261022.03_document_guides")
RAW = BASE / "raw"

def norm(s):
    s = html.unescape(s)
    s = (s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
          .replace(" ", " "))
    return re.sub(r"\s+", " ", s).strip()

def page_text(path):
    if path.suffix == ".json":
        d = json.loads(path.read_text())
        parts = []
        for h in d.get("hits", []):
            t = re.sub(r"<[^>]+>", " ", h.get("comment_text") or "")
            parts.append(norm(t))
        return " ".join(parts)
    return norm(path.read_text(errors="replace"))

# (guide, kind, text, link, saved_file relative to raw/)
Q = []
def q(guide, text, link, saved): Q.append((guide, "quote", text, link, f"{guide}/{saved}"))
def p(guide, text, link, saved): Q.append((guide, "paraphrase", text, link, f"{guide}/{saved}"))

exec(open(pathlib.Path(__file__).with_name("quotes_data_people.py")).read())

rows, bad = [], []
cache = {}
for guide, kind, text, link, saved in Q:
    path = RAW / saved
    if not path.exists():
        bad.append(("missing file", saved)); verified = "no"
    elif kind == "quote":
        if saved not in cache: cache[saved] = page_text(path)
        verified = "yes" if norm(text) in cache[saved] else "no"
        if verified == "no": bad.append(("not found", text[:90], saved))
    else:
        verified = "no"
    rows.append({"guide": guide, "kind": kind, "text": text, "link": link, "saved_file": f"raw/{saved}", "verified": verified})

out = BASE / "quotes_people.csv"
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["guide", "kind", "text", "link", "saved_file", "verified"])
    w.writeheader(); w.writerows(rows)
n_q = sum(1 for r in rows if r["kind"] == "quote")
n_ok = sum(1 for r in rows if r["kind"] == "quote" and r["verified"] == "yes")
print("rows:", len(rows), "quotes:", n_q, "verified quotes:", n_ok, "paraphrases:", len(rows) - n_q)
for b in bad: print("PROBLEM", b)
