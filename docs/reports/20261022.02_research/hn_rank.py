"""Rank digest entries by how many first-pass-diligence phrases they contain; print the top ones.

Run: python3 -I hn_rank.py [N]
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
DIGEST = HERE / "raw" / "voc" / "hn_digest.txt"

PHRASES = [
    r"data room", r"due diligence", r"diligence", r"investment memo", r"\bmemo\b", r"red flag",
    r"cohort", r"churn", r"\bARR\b", r"recurring", r"as an angel", r"I invest", r"we invest",
    r"I'm a VC", r"I am a VC", r"associate", r"principal", r"partner meeting", r"cap table",
    r"spreadsheet", r"excel", r"pitchbook", r"crunchbase", r"customer calls?", r"reference calls?",
    r"background check", r"financial model", r"\bdeck\b", r"missed", r"regret", r"hours", r"weeks",
    r"first pass", r"screen", r"applications",
]


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    entries = DIGEST.read_text().split("\n=== ")
    scored = []
    for e in entries:
        score = sum(1 for p in PHRASES if re.search(p, e, re.I))
        scored.append((score, e))
    scored.sort(key=lambda x: -x[0])
    for score, e in scored[:n]:
        print(f"[{score}] === {e[:1800]}\n")


if __name__ == "__main__":
    main()
