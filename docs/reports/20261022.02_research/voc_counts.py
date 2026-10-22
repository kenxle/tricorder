"""Counts for the R1 voice-of-customer track. Reads voc_quotes.csv (one row per quote or paraphrase).

Prints: rows by kind, rows with links, persona x layer table, question counts, year spread,
and each persona's highest evidence layer (pay > do > say).
Run: python3 -I voc_counts.py
"""
import csv
import pathlib
import re
from collections import Counter, defaultdict

HERE = pathlib.Path(__file__).resolve().parent
ROWS = list(csv.DictReader((HERE / "voc_quotes.csv").open(encoding="utf-8")))
RANK = {"say": 1, "do": 2, "pay": 3}
CUSTOMER_PERSONAS = ["partner_principal", "solo_angel", "accelerator_screener", "associate", "corporate_vc"]


def year(date):
    m = re.match(r"(\d{4})", date)
    return int(m.group(1)) if m else None


def main():
    raw = HERE / "raw" / "voc"
    print("saved HN query files:", len(list(raw.glob("hn_*_comment.json")) + list(raw.glob("hn_*_story.json"))))
    print("saved web page text files:", len(list(raw.glob("web_*.txt"))))
    print("total rows:", len(ROWS))
    kinds = Counter(r["kind"] for r in ROWS)
    print("by kind:", dict(kinds))
    linked = [r for r in ROWS if r["link"].startswith("http")]
    print("rows with a link:", len(linked))
    print("verbatim quotes with a link:", sum(1 for r in linked if r["kind"] == "quote"))
    print("verbatim quotes from the person's or firm's own publication or own comment:",
          sum(1 for r in linked if r["kind"] == "quote" and r["source_type"] in ("own_words", "community_comment", "interview")))

    print("\npersona x layer (rows):")
    table = defaultdict(Counter)
    for r in ROWS:
        table[r["persona"]][r["layer"]] += 1
    layers = ["say", "do", "pay", "context"]
    print("persona".ljust(24) + "".join(l.ljust(9) for l in layers) + "total")
    for persona in sorted(table, key=lambda p: -sum(table[p].values())):
        row = table[persona]
        print(persona.ljust(24) + "".join(str(row[l]).ljust(9) for l in layers) + str(sum(row.values())))

    print("\nhighest layer with evidence, customer personas (pay > do > say):")
    ranked = []
    for p in CUSTOMER_PERSONAS:
        present = [l for l in table[p] if l in RANK]
        top = max(present, key=lambda l: RANK[l]) if present else "none"
        ranked.append((RANK.get(top, 0), table[p][top] if top in RANK else 0, sum(table[p].values()), p, top))
    for score, top_n, total, p, top in sorted(ranked, reverse=True):
        print(f"  {p}: highest={top} ({top_n} rows at that layer, {total} rows in all)")

    print("\nrows by question:")
    for q, n in Counter(r["question"] for r in ROWS).most_common():
        print(f"  {q}: {n}")

    print("\nrows by year:")
    years = Counter(year(r["date"]) for r in ROWS)
    for y in sorted(years):
        print(f"  {y}: {years[y]}")
    old = sum(n for y, n in years.items() if y and y < 2020)
    recent = sum(n for y, n in years.items() if y and y >= 2025)
    print(f"rows before 2020: {old} of {len(ROWS)} ({old / len(ROWS):.0%})")
    old_src = Counter(r["source_type"] for r in ROWS if year(r["date"]) and year(r["date"]) < 2020)
    print("source types of rows before 2020:", dict(old_src))
    print(f"rows from 2025 or later: {recent} of {len(ROWS)} ({recent / len(ROWS):.0%})")

    print("\nsource types:", dict(Counter(r["source_type"] for r in ROWS)))


if __name__ == "__main__":
    main()
