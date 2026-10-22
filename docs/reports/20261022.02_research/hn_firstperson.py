"""Print digest entries where the writer speaks as an investor (first person), for quote mining.

Run: python3 -I hn_firstperson.py
"""
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
DIGEST = HERE / "raw" / "voc" / "hn_digest.txt"

FIRST = re.compile(
    r"(as an angel|I'?m an angel|I am an angel|angel investor myself|I angel invest|as a VC|I'?m a VC|"
    r"I am a VC|I worked (at|for) a (VC|venture)|when I was an? (associate|analyst|principal)|"
    r"I was an? (associate|analyst|principal)|our fund|my fund|we invest|I invest|I'?ve invested|"
    r"I run an? (accelerator|fund)|I read (YC )?applications|as an investor|I'?m an investor|"
    r"I do diligence|I've done diligence|during diligence we|in diligence we|our diligence|"
    r"I worked in (PE|private equity|VC|venture)|LP in)",
    re.I,
)
TOPIC = re.compile(r"diligence|data room|memo|red flag|cohort|churn|ARR|metric|deck|model|numbers|revenue|reference", re.I)


def main():
    entries = DIGEST.read_text().split("\n=== ")
    hits = [e for e in entries if FIRST.search(e) and TOPIC.search(e)]
    print(len(hits), "hits")
    for e in hits:
        print("=== " + e[:1500] + "\n")


if __name__ == "__main__":
    main()
