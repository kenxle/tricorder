"""Render the quotes table and the counts block into research_voice_of_customer.md.

Replaces the text between <!-- TABLE START --> and <!-- TABLE END -->, and between
<!-- COUNTS START --> and <!-- COUNTS END -->, from voc_quotes.csv and voc_counts.py output.
Run: python3 -I voc_table.py
"""
import csv
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
DOC = HERE / "research_voice_of_customer.md"
NAMES = {
    "associate": "Associate",
    "partner_principal": "Partner or principal",
    "solo_angel": "Angel",
    "accelerator_screener": "Accelerator screener",
    "corporate_vc": "Corporate VC",
    "outsourced_diligence": "Outsourced diligence",
    "observer": "Observer",
    "fund_staff_unstated": "Fund staff, role unstated",
    "vendor_claim": "Vendor claim",
    "fund_buyers_mixed": "Data buyers, mixed",
}


def table():
    rows = list(csv.DictReader((HERE / "voc_quotes.csv").open(encoding="utf-8")))
    out = ["| # | Persona | Layer | Date | Quote or paraphrase | Link |", "|---|---|---|---|---|---|"]
    for r in rows:
        text = r["text"].replace("|", "/").replace("\n", " ")
        cell = f"\"{text}\"" if r["kind"] == "quote" else f"Paraphrase ({r['source_type'].replace('_', ' ')}): {text}"
        out.append(f"| {r['id']} | {NAMES[r['persona']]} | {r['layer']} | {r['date']} | {cell} | [source]({r['link']}) |")
    return "\n".join(out)


def counts():
    res = subprocess.run([sys.executable, "-I", str(HERE / "voc_counts.py")], capture_output=True, text=True, check=True)
    return "```\n" + res.stdout.strip() + "\n```"


def main():
    doc = DOC.read_text(encoding="utf-8")
    doc = re.sub(r"<!-- TABLE START -->.*?<!-- TABLE END -->",
                 lambda m: "<!-- TABLE START -->\n" + table() + "\n<!-- TABLE END -->", doc, flags=re.S)
    doc = re.sub(r"<!-- COUNTS START -->.*?<!-- COUNTS END -->",
                 lambda m: "<!-- COUNTS START -->\n" + counts() + "\n<!-- COUNTS END -->", doc, flags=re.S)
    DOC.write_text(doc, encoding="utf-8")
    print("rendered")


if __name__ == "__main__":
    main()
