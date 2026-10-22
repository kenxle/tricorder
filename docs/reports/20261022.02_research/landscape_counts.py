"""Count what each tool's own pages show about the things Track 2 names.

Input: landscape_labels.csv. One row per tool and capability where the tool's saved
page text shows the capability. The row names the saved file and an exact phrase from it.
This script checks that every phrase really appears in its file (so no label rests on
memory), then counts.

A capability with no row means the pages I saved do not show it. It does not prove the
product lacks it. The saved pages are home, pricing and product pages.

Output: landscape_evidence.csv (every tool x capability, yes or not_shown) and a printed
summary that research_landscape.md quotes.

Run: python3 -I landscape_counts.py
"""
import csv
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw", "landscape")

CAPS = [
    "market_signals",
    "comps",
    "financial_red_flags",
    "reads_deck_or_data_room",
    "memo",
    "claim_to_source",
]

# Every tool the market map covers, with its group. Tools with no label rows still count.
TOOLS = {
    "Affinity": "incumbent", "Harmonic": "incumbent", "Specter": "incumbent", "Grata": "incumbent",
    "PitchBook": "incumbent", "Crunchbase": "incumbent", "Tracxn": "incumbent", "Dealroom": "incumbent",
    "CB Insights": "incumbent", "Carta (data side)": "incumbent", "NFX Signal": "incumbent", "Clay": "incumbent",
    "Wokelo": "entrant", "Keye": "entrant", "Termina": "entrant", "askRIA": "entrant", "V7 Go": "entrant",
    "Energent": "entrant", "Decile Hub": "entrant", "Fundwave": "entrant", "Visible": "entrant",
    "Apify AI Dealflow Analysis": "entrant", "Flybridge memo generator": "entrant", "Diligent (open source)": "entrant",
}


def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def main():
    labels = list(csv.DictReader(open(os.path.join(HERE, "landscape_labels.csv"), encoding="utf8")))
    cache = {}
    bad = []
    for r in labels:
        path = os.path.join(RAW, r["evidence_file"])
        if path not in cache:
            cache[path] = norm(open(path, encoding="utf8", errors="ignore").read()) if os.path.exists(path) else None
        text = cache[path]
        if text is None or norm(r["evidence_text"]) not in text:
            bad.append((r["tool"], r["capability"], r["evidence_file"], r["evidence_text"]))
        if r["tool"] not in TOOLS or r["capability"] not in CAPS or TOOLS[r["tool"]] != r["group"]:
            bad.append(("unknown tool, capability or group", r["tool"], r["capability"], r["group"]))
    if bad:
        print("LABEL PROBLEMS")
        for b in bad:
            print("  ", b)
        raise SystemExit(1)

    shown = {(r["tool"], r["capability"]) for r in labels}
    out = os.path.join(HERE, "landscape_evidence.csv")
    with open(out, "w", newline="", encoding="utf8") as fh:
        w = csv.writer(fh)
        w.writerow(["tool", "group", "capability", "shown_on_pages_read"])
        for tool, group in TOOLS.items():
            for cap in CAPS:
                w.writerow([tool, group, cap, "yes" if (tool, cap) in shown else "not_shown"])

    print("tools:", len(TOOLS))
    for group in ("incumbent", "entrant"):
        members = [t for t, g in TOOLS.items() if g == group]
        print("\n%s (%d tools)" % (group, len(members)))
        for cap in CAPS:
            names = [t for t in members if (t, cap) in shown]
            print("  %-24s %2d of %2d  %s" % (cap, len(names), len(members), ", ".join(names) or "none"))
    all_three = [t for t in TOOLS if all((t, c) in shown for c in ("market_signals", "comps", "financial_red_flags"))]
    print("\ntools showing market signals AND comps AND financial red flags on the pages read:", all_three or "none")
    full = [t for t in TOOLS if all((t, c) in shown for c in ("reads_deck_or_data_room", "financial_red_flags", "memo", "claim_to_source"))]
    print("tools showing data room reading AND red flags AND memo AND claim-to-source:", full or "none")
    print("\nwrote", out)


if __name__ == "__main__":
    main()
