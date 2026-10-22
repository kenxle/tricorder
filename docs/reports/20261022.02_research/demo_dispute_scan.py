"""Search HN (Algolia) stories and comments since 2025-06-01 that name each shortlisted company,
and flag any that contain dispute words. Saves raw JSON to raw/demo_companies/hn_dispute_<slug>.json
and writes demo_dispute_scan.csv (one row per flagged item plus a summary row per company).

Run: python3 -I demo_dispute_scan.py
"""
import csv
import html
import json
import pathlib
import re
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / "raw" / "demo_companies"
SINCE = 1748736000  # 2025-06-01 UTC
WORDS = re.compile(r"\b(lawsuit|sued|sue|suing|litigation|dispute|fraud|scam|cease and desist|banned|ban|violat\w*|terms of service|tos|stole|plagiar\w*|co-?founder (left|departed|quit))\b", re.I)
COMPANIES = {
    "sazabi": ["Sazabi"], "tasklet-2": ["Tasklet"], "expanse": ["expanse.sh", "Expanse (YC"],
    "testerarmy": ["TesterArmy", "tester.army"], "ploy": ["ploy.ai"], "minicor": ["Minicor"],
    "interfaze": ["Interfaze", "JigsawStack"], "superlog": ["Superlog"], "chert": ["Chert", "trychert"],
}


def get(q):
    p = {"query": q, "hitsPerPage": 200, "numericFilters": f"created_at_i>{SINCE}"}
    url = "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(p)
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "tricorder-research"}), timeout=30) as r:
        return json.loads(r.read())["hits"]


def text(h):
    t = (h.get("title") or "") + " " + (h.get("comment_text") or h.get("story_text") or "")
    return html.unescape(re.sub(r"<[^>]+>", " ", t))


def main():
    rows = []
    for slug, queries in COMPANIES.items():
        hits = {}
        for q in queries:
            for h in get(q):
                hits[h["objectID"]] = h
        (RAW / f"hn_dispute_{slug}.json").write_text(json.dumps(list(hits.values()), indent=1))
        named = [h for h in hits.values() if any(q.split(" ")[0].lower() in text(h).lower() for q in queries)]
        flagged = [h for h in named if WORDS.search(text(h))]
        rows.append({"slug": slug, "kind": "summary", "id": "", "items_naming_company": len(named), "flagged": len(flagged), "snippet": ""})
        for h in flagged:
            t = text(h)
            m = WORDS.search(t)
            rows.append({"slug": slug, "kind": "flag", "id": h["objectID"], "items_naming_company": "", "flagged": m.group(0),
                         "snippet": t[max(0, m.start() - 160): m.end() + 160].replace("\n", " ")})
    with open(HERE / "demo_dispute_scan.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        if r["kind"] == "summary":
            print(r["slug"], "items:", r["items_naming_company"], "flagged:", r["flagged"])


if __name__ == "__main__":
    main()
