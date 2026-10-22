"""Summarise the saved GitHub API responses under raw/demo_companies/github_*.json.

Run: python3 -I demo_github_summary.py
"""
import json
import pathlib

RAW = pathlib.Path(__file__).resolve().parent / "raw" / "demo_companies"
for p in sorted(RAW.glob("github_*.json")):
    d = json.loads(p.read_text())
    if isinstance(d, list):
        print(p.name, [(r["name"], r["stargazers_count"]) for r in d])
    elif "items" in d:
        print(p.name, [i["login"] for i in d["items"]][:6])
    else:
        print(p.name, d.get("login"), "|", d.get("name"), "| repos", d.get("public_repos"), "| followers", d.get("followers"), "|", d.get("blog"), "| since", (d.get("created_at") or "")[:10])
