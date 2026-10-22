"""Counts for the demo-company track, from the saved YC batch data and the HN scan.

Run: python3 -I demo_batch_counts.py
Writes demo_batch_counts.txt.
"""
import json
import pathlib
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / "raw" / "demo_companies"
d = json.loads((RAW / "yc_algolia_spring_2026.json").read_text())
batch = pd.DataFrame(d["hits"])
scan = pd.read_csv(HERE / "demo_hn_scan.csv")
facets = json.loads((RAW / "yc_algolia_batch_facets.json").read_text())["results"][0]["facets"]["batch"]
lines = [
    f"Spring 2026 companies in YC directory: {len(batch)}",
    f"Directory facet count for Spring 2026: {facets.get('Spring 2026')}",
    "By industry: " + ", ".join(f"{k} {v}" for k, v in batch["industry"].value_counts().items()),
    f"Active B2B or Fintech companies scanned on HN: {len(scan)}",
    f"Of those, with a Launch HN or Show HN title containing 'YC P26' found by name: {scan['launch_hn_titles'].fillna('').str.contains('P26').sum()}",
    f"Of those, with at least one HN story linking their domain: {(scan['hn_domain_stories'] > 0).sum()}",
    f"Of those, located in New York City: {scan['locations'].fillna('').str.contains('New York').sum()}",
]
(HERE / "demo_batch_counts.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
