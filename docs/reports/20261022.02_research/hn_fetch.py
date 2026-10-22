"""Fetch Hacker News comments and stories from the Algolia API for the R1 voice-of-customer track.

Saves each query's raw JSON under raw/voc/hn_<slug>_<tag>.json so later agents do not refetch.
Run: python3 -I hn_fetch.py
"""
import json
import pathlib
import re
import time
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "raw" / "voc"
OUT.mkdir(parents=True, exist_ok=True)

QUERIES = [
    ("due diligence VC", "comment"),
    ("due diligence startup investor", "comment"),
    ("investment memo", "comment"),
    ("data room diligence", "comment"),
    ("diligence associate", "comment"),
    ("VC associate diligence", "comment"),
    ("red flag startup investor", "comment"),
    ("ARR not recurring", "comment"),
    ("cohort churn investor", "comment"),
    ("angel investor diligence", "comment"),
    ("accelerator applications screening", "comment"),
    ("YC application read", "comment"),
    ("pitchbook expensive", "comment"),
    ("crunchbase pro data", "comment"),
    ("VC analyst spreadsheet", "comment"),
    ("investment memo ChatGPT", "comment"),
    ("diligence missed fraud investors", "comment"),
    ("revenue recognition startup investors misled", "comment"),
    ("data room first thing", "comment"),
    ("as an angel I diligence", "comment"),
    ("reference calls VC diligence", "comment"),
    ("VC associate memo", "comment"),
    ("investment committee memo", "comment"),
    ("pitchbook subscription", "comment"),
    ("affinity CRM VC", "comment"),
    ("cohort chart investors", "comment"),
    ("investors lied revenue startup", "comment"),
    ("diligence would have caught", "comment"),
    ("bank statements diligence investors", "comment"),
    ("VC due diligence AI tool", "comment"),
    ("angel syndicate diligence", "comment"),
    ("YC reads applications minutes", "comment"),
    ("customer references diligence startup", "comment"),
    ("we missed red flags invested", "comment"),
    ("should have caught it investor", "comment"),
    ("hebbia", "comment"),
    ("wokelo", "comment"),
    ("harmonic VC sourcing", "comment"),
    ("VC intern screening deals", "comment"),
    ("memo hours associate", "comment"),
    ("deal flow spreadsheet airtable", "comment"),
    ("angel investor ChatGPT pitch deck", "comment"),
    ("corporate venture diligence", "comment"),
    ("revenue run rate not ARR", "comment"),
    ("Builder.ai investors", "comment"),
    ("venture capital due diligence", "story"),
    ("investment memo", "story"),
    ("AI due diligence venture", "story"),
]


def slug(text):
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def main():
    for query, tag in QUERIES:
        params = urllib.parse.urlencode({"query": query, "tags": tag, "hitsPerPage": 50})
        url = f"https://hn.algolia.com/api/v1/search?{params}"
        path = OUT / f"hn_{slug(query)}_{tag}.json"
        if path.exists():
            continue
        req = urllib.request.Request(url, headers={"User-Agent": "tricorder-research/0.1"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
        data["_query_url"] = url
        path.write_text(json.dumps(data, indent=1))
        print(path.name, len(data.get("hits", [])))
        time.sleep(0.5)


if __name__ == "__main__":
    main()
