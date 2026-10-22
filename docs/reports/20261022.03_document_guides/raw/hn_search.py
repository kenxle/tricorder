"""Hacker News Algolia search. Usage: python3 -I hn_search.py <slug> "<query>" [min_points]
Saves JSON to raw/<slug>/hn_<query>.json and prints id, points, date, first 200 chars of text/title."""
import json, pathlib, re, sys, urllib.parse, urllib.request
OUT = pathlib.Path(__file__).resolve().parent
slug, q = sys.argv[1], sys.argv[2]
tags = sys.argv[3] if len(sys.argv) > 3 else "comment"
url = "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode({"query": q, "tags": tags, "hitsPerPage": 20})
data = urllib.request.urlopen(url, timeout=30).read().decode()
name = re.sub(r"[^a-z0-9]+", "_", q.lower())[:60]
(OUT / slug / f"hn_{tags}_{name}.json").write_text(data)
for h in json.loads(data)["hits"]:
    t = re.sub(r"<[^>]+>", " ", h.get("comment_text") or h.get("title") or "")
    print(h["objectID"], h.get("points"), h["created_at"][:10], h.get("story_title") or "", "|", t[:260].replace("\n", " "))
