"""Count which red flags the voice-of-the-customer quotes name.

Reads voc_quotes.csv (one row per quote or paraphrase) and tags each row with
every red-flag theme its text names, using the keyword rules below. Writes one
row per quote with its tags to red_flag_labels.csv, then prints how many rows
name each theme. A row can name more than one theme, so the theme counts do
not add up to the row count.

The rules are keyword matches, not a reading. Check red_flag_labels.csv to see
exactly which rows each count rests on.

Run: python3 red_flag_counts.py
"""

import csv
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

THEMES = {
    "numbers that disagree": r"disagree|doesn.t match|don.t match|does not match|not match|mismatch|reconcile|differs between|inconsisten|story matches|match the P&L|tie to|ties to",
    "ARR not recurring": r"\bARR\b|recurring|\bMRR\b|annual run|run.rate|one.time|pilot",
    "hidden churn or weak retention": r"churn|cohort|retention",
    "burn out of line": r"\bburn|runway|hiring plan",
    "faked or forged documents": r"fraud|fake|forged|two sets of books|made.up",
    "customer concentration": r"concentration|largest customer|single customer",
    "cap table problems": r"cap table",
    "founder can't explain the numbers": r"could not explain|can.t explain|cannot explain",
}


def main() -> None:
    rows = list(csv.DictReader(open(HERE / "voc_quotes.csv", encoding="utf-8")))
    counts = Counter()
    out = []
    for r in rows:
        text = r["text"]
        tags = [name for name, pat in THEMES.items() if re.search(pat, text, flags=re.I)]
        for t in tags:
            counts[t] += 1
        out.append({"id": r["id"], "persona": r["persona"], "kind": r["kind"], "date": r["date"],
                    "tags": "; ".join(tags), "text": text, "link": r["link"]})
    with open(HERE / "red_flag_labels.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    tagged = sum(1 for o in out if o["tags"])
    print(f"rows in voc_quotes.csv: {len(rows)}")
    print(f"rows naming at least one red flag: {tagged}")
    sources = {name: set() for name in THEMES}
    for o in out:
        for tag in filter(None, o["tags"].split("; ")):
            sources[tag].add(o["link"])
    print("rows\tsources\ttheme")
    for name, n in counts.most_common():
        print(f"{n}\t{len(sources[name])}\t{name}")


if __name__ == "__main__":
    main()
