"""Ask EDGAR full-text search (efts.sec.gov, unofficial JSON endpoint; see research_feasibility.md Part 2)
for Form D filings naming each shortlisted company since 2024. Saves raw JSON to
raw/demo_companies/edgar_formd_<slug>.json and prints the filer names and dates.

Run: python3 -I demo_formd.py [slug=Name ...]   (no arguments: the shortlist)
"""
import json
import pathlib
import time
import urllib.parse
import urllib.request

RAW = pathlib.Path(__file__).resolve().parent / "raw" / "demo_companies"
UA = "Tricorder Research tricorder-research@stclair.ai"
NAMES = {"sazabi": "Sazabi", "tasklet": "Tasklet", "expanse": "Expanse Labs", "testerarmy": "TesterArmy",
         "ploy": "Ploy", "minicor": "Minicor", "interfaze": "Interfaze", "superlog": "Superlog"}


def main():
    import sys
    names = dict(a.split("=", 1) for a in sys.argv[1:]) or NAMES
    for slug, name in names.items():
        q = urllib.parse.urlencode({"q": f'"{name}"', "forms": "D,D/A", "dateRange": "custom", "startdt": "2024-01-01", "enddt": "2026-10-22"})
        url = "https://efts.sec.gov/LATEST/search-index?" + q
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "identity"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read())
        except Exception as e:
            print(slug, "FAIL", e)
            continue
        (RAW / f"edgar_formd_{slug}.json").write_text(json.dumps(data, indent=1))
        hits = data.get("hits", {}).get("hits", [])
        print(slug, "hits:", len(hits))
        for h in hits[:8]:
            s = h["_source"]
            print("   ", s.get("display_names"), s.get("file_date"), s.get("form"), h["_id"])
        time.sleep(0.3)


if __name__ == "__main__":
    main()
