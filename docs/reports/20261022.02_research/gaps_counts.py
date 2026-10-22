"""Counts and quote checks for the research-gaps track. Reads gaps_quotes.csv (one row per quote or paraphrase).

1. Checks every verbatim quote against the saved page text in raw/gaps/. Each saved file starts with
   "SOURCE: <url>", which is how a row's link finds its file. Before comparing, both sides get the same
   light normalising: curly quotes become straight quotes, en and em dashes become hyphens, and runs of
   whitespace become one space. Nothing else is changed.
2. Prints rows by question and layer, persona and layer, source type, and year.
3. Prints the per-deal and per-hour figures the write-up uses, computed from numbers in the cited sources.

Run: python3 -I gaps_counts.py
"""
import csv
import pathlib
import re
from collections import Counter, defaultdict

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / "raw" / "gaps"
ROWS = list(csv.DictReader((HERE / "gaps_quotes.csv").open(encoding="utf-8")))


def norm(text):
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = text.replace("–", "-").replace("—", "-").replace("‍", "").replace("​", "")
    return re.sub(r"\s+", " ", text).strip()


def saved_pages():
    pages = {}
    for path in sorted(RAW.glob("*.txt")):
        first = path.read_text(errors="replace").split("\n", 1)[0]
        if first.startswith("SOURCE: "):
            pages.setdefault(first[len("SOURCE: "):].strip(), []).append(path)
    return pages


def year(date):
    m = re.match(r"(\d{4})", date)
    return int(m.group(1)) if m else None


def check_quotes(pages):
    print("QUOTE CHECK (verbatim quotes against saved page text)")
    ok, bad, missing = 0, [], []
    for r in ROWS:
        if r["kind"] != "quote":
            continue
        files = pages.get(r["link"])
        if not files:
            missing.append(r["id"])
            continue
        body = " ".join(norm(f.read_text(errors="replace")) for f in files)
        if norm(r["text"]) in body:
            ok += 1
        else:
            bad.append(r["id"])
    print(f"  quotes found verbatim: {ok}")
    print(f"  quotes not found: {len(bad)} {bad}")
    print(f"  quotes with no saved page: {len(missing)} {missing}")
    paras = [r for r in ROWS if r["kind"] == "paraphrase"]
    with_page = sum(1 for r in paras if r["link"] in pages)
    print(f"  paraphrases: {len(paras)}, with a saved page: {with_page}")
    return not bad and not missing


def tables():
    print("\nFILES AND ROWS")
    print("  saved page text files in raw/gaps:", len(list(RAW.glob("web_*.txt"))))
    print("  saved Hacker News comment files in raw/gaps:", len(list(RAW.glob("hn_item_*.txt"))))
    print("  saved Hacker News search files in raw/gaps:", len(list(RAW.glob("hn_*.json"))))
    print("  total rows:", len(ROWS))
    print("  by kind:", dict(Counter(r["kind"] for r in ROWS)))
    print("  distinct source links:", len({r["link"] for r in ROWS}))

    layers = ["say", "do", "pay", "context"]
    print("\nQUESTION x LAYER (rows)")
    qt = defaultdict(Counter)
    for r in ROWS:
        qt[r["question"]][r["layer"]] += 1
    print("  " + "question".ljust(24) + "".join(l.ljust(9) for l in layers) + "total")
    for q in sorted(qt):
        print("  " + q.ljust(24) + "".join(str(qt[q][l]).ljust(9) for l in layers) + str(sum(qt[q].values())))

    print("\nPERSONA x LAYER (rows)")
    pt = defaultdict(Counter)
    for r in ROWS:
        pt[r["persona"]][r["layer"]] += 1
    print("  " + "persona".ljust(24) + "".join(l.ljust(9) for l in layers) + "total")
    for p in sorted(pt, key=lambda p: -sum(pt[p].values())):
        print("  " + p.ljust(24) + "".join(str(pt[p][l]).ljust(9) for l in layers) + str(sum(pt[p].values())))

    print("\nPAY-LAYER ROWS BY QUESTION")
    for q, n in sorted(Counter(r["question"] for r in ROWS if r["layer"] == "pay").items()):
        print(f"  {q}: {n}")

    print("\nSOURCE TYPES:", dict(Counter(r["source_type"] for r in ROWS)))

    years = Counter(year(r["date"]) for r in ROWS)
    print("\nROWS BY YEAR:", {k: years[k] for k in sorted(years, key=lambda y: (y is None, y or 0))})
    dated = [y for y in (year(r["date"]) for r in ROWS) if y]
    recent = sum(1 for y in dated if y >= 2025)
    old = sum(1 for y in dated if y < 2020)
    print(f"  dated rows: {len(dated)}; from 2025 or later: {recent} ({recent / len(dated):.0%}); before 2020: {old} ({old / len(dated):.0%})")
    print("  undated rows:", sum(1 for r in ROWS if not year(r["date"])))


def figures():
    print("\nFIGURES USED IN THE WRITE-UP (inputs are from the cited sources)")
    day = 8
    print(f"  118 survey hours as {day}-hour working days: {118 / day:.1f}")
    print(f"  81 early-stage hours as {day}-hour working days: {81 / day:.1f}")
    print(f"  120 hours (Strebulaev) as {day}-hour working days: {120 / day:.1f}")
    print(f"  250 hours (Strebulaev, all deals) as {day}-hour working days: {250 / day:.1f}")
    print(f"  angel median 20 hours as {day}-hour working days: {20 / day:.1f}")

    print("  New York Angels dues as a share of the expected yearly investment: "
          f"{4000 / 50000:.0%} (4,000 / 50,000)")
    print("  37 Angels dues as a share of the one required 25,000 investment: "
          f"{3000 / 25000:.0%} later years, {5000 / 25000:.0%} first year")
    print("  Syndicate lead's 500 fee as a share of the 2,500 minimum check: "
          f"{500 / 2500:.0%}; the later 7% fee on the same check: {0.07 * 2500:.0f} dollars")
    low, high = 3500 / (5 * 12), 3500 / (3 * 12)
    print("  Angel Squad 3,500 spread over one year of shared deals (3 to 5 a month): "
          f"{low:.0f} to {high:.0f} dollars per deal shown")
    print("  Per-deal cash prices for diligence in the sources: Lagos network about 600; "
          "report service 4,900 (2007)")
    print("  Sydecar per-SPV cost range with the 2,000 regulatory fee: "
          f"{2500 + 2000:,} to {12500 + 2000:,} dollars")


def main():
    pages = saved_pages()
    passed = check_quotes(pages)
    tables()
    figures()
    print("\nRESULT:", "all quotes verified" if passed else "SOME QUOTES FAILED: fix before publishing")


if __name__ == "__main__":
    main()
