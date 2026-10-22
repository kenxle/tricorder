"""For every active B2B or Fintech company in the saved YC Spring 2026 list, ask the HN Algolia API
for stories linking to the company's domain and for "Launch HN" stories naming it.
Saves raw JSON per company under raw/demo_companies/hn/ and writes demo_hn_scan.csv (one row per company).

Run: python3 -I demo_hn_scan.py
"""
import csv
import json
import pathlib
import re
import time
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / "raw" / "demo_companies"
HN = RAW / "hn"
API = "https://hn.algolia.com/api/v1/search"


def get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "tricorder-research"}), timeout=30) as r:
        return json.loads(r.read())


def domain(w):
    d = re.sub(r"^https?://(www\.)?", "", (w or "").strip()).split("/")[0]
    return d


def main():
    HN.mkdir(parents=True, exist_ok=True)
    data = json.loads((RAW / "yc_algolia_spring_2026.json").read_text())
    rows = []
    for h in data["hits"]:
        if h.get("industry") not in ("B2B", "Fintech") or h.get("status") != "Active":
            continue
        d = domain(h.get("website"))
        dom = get({"query": d, "restrictSearchableAttributes": "url", "hitsPerPage": 50}) if d else {"hits": []}
        launch = get({"query": f"Launch HN {h['name']}", "tags": "story", "hitsPerPage": 20})
        launch_hits = [x for x in launch["hits"] if (x.get("title") or "").lower().startswith("launch hn") and h["name"].lower() in (x.get("title") or "").lower()]
        (HN / f"{h['slug']}.json").write_text(json.dumps({"domain_query": d, "domain_hits": dom["hits"], "launch_hits": launch_hits}, indent=1))
        dom_hits = [x for x in dom["hits"] if d and d in (x.get("url") or "")]
        rows.append({
            "slug": h["slug"], "name": h["name"], "industry": h.get("industry"), "subindustry": h.get("subindustry"),
            "locations": h.get("all_locations"), "team_size": h.get("team_size"), "website": h.get("website"),
            "launched_at": h.get("launched_at"),
            "hn_domain_stories": len(dom_hits),
            "hn_domain_max_points": max([x.get("points") or 0 for x in dom_hits], default=0),
            "hn_domain_comments": sum([x.get("num_comments") or 0 for x in dom_hits]),
            "launch_hn": len(launch_hits),
            "launch_hn_titles": " || ".join(x["title"] for x in launch_hits),
            "launch_hn_ids": " ".join(x["objectID"] for x in launch_hits),
            "one_liner": h.get("one_liner"),
        })
        time.sleep(0.2)
    with open(HERE / "demo_hn_scan.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("companies scanned:", len(rows))


if __name__ == "__main__":
    main()
