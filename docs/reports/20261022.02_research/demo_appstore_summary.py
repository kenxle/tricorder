"""Summarise saved Apple Search API responses raw/demo_companies/appstore_*.json (app name, seller, rating count).

Run: python3 -I demo_appstore_summary.py
"""
import json
import pathlib

RAW = pathlib.Path(__file__).resolve().parent / "raw" / "demo_companies"
for p in sorted(RAW.glob("appstore_*.json")):
    d = json.loads(p.read_text())
    print(p.name, d.get("resultCount"), [(r.get("trackName"), r.get("sellerName"), r.get("userRatingCount")) for r in d.get("results", [])][:5])
