"""Query YC's public company directory (the Algolia search key YC embeds in ycombinator.com/companies)
for one batch, save the raw JSON, and write a CSV of the companies.

Run: python3 -I demo_yc_batch.py "Spring 2026"
Reads the key from raw/demo_companies/yc_companies_spring2026.html.
"""
import csv
import json
import pathlib
import re
import sys
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / "raw" / "demo_companies"


def main():
    batch = sys.argv[1] if len(sys.argv) > 1 else "Spring 2026"
    page = (RAW / "yc_companies_spring2026.html").read_text()
    opts = json.loads(re.search(r"AlgoliaOpts = (\{[^}]*\})", page).group(1))
    url = f"https://{opts['app'].lower()}-dsn.algolia.net/1/indexes/*/queries"
    hits, facets = [], {}
    for pg in range(0, 10):
        body = {"requests": [{"indexName": "YCCompany_production",
                              "params": f"hitsPerPage=200&page={pg}&facets=%5B%22batch%22%5D&facetFilters=%5B%5B%22batch%3A{urllib.parse.quote(batch)}%22%5D%5D"}]}
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={
            "X-Algolia-Application-Id": opts["app"], "X-Algolia-API-Key": opts["key"],
            "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            res = json.loads(r.read())["results"][0]
        hits += res["hits"]
        facets = res.get("facets", facets)
        if pg >= res["nbPages"] - 1:
            break
    tag = re.sub(r"\W+", "_", batch.lower())
    (RAW / f"yc_algolia_{tag}.json").write_text(json.dumps({"batch": batch, "nbHits": len(hits), "facets": facets, "hits": hits}, indent=1))
    with open(RAW / f"yc_{tag}_companies.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "slug", "batch", "website", "one_liner", "industry", "subindustry", "status", "team_size", "regions", "tags", "launched_at"])
        for h in hits:
            w.writerow([h.get("name"), h.get("slug"), h.get("batch"), h.get("website"), h.get("one_liner"),
                        h.get("industry"), h.get("subindustry"), h.get("status"), h.get("team_size"),
                        "|".join(h.get("regions") or []), "|".join(h.get("tags") or []), h.get("launched_at")])
    print(batch, "companies:", len(hits))


if __name__ == "__main__":
    import urllib.parse
    main()
