"""Check every quoted passage in the six financials guides against the saved pages.

Run: python3 -I raw/check_guide_quotes.py   (from the document_guides folder)
A passage is text inside straight or curly double quotes with at least 5 words (4 for short ones in
table cells is skipped). It passes if its normalised form appears in any saved file in the guide's raw
folder. Prints each failure with the guide and the passage.
"""
import json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import financials_quotes as fq

HERE = pathlib.Path(__file__).resolve().parent.parent
GUIDES = ["financial-model", "historical-financials", "audited-or-reviewed-financials", "bank-statements", "tax-returns", "use-of-funds-plan"]
bad = 0
total = 0
for g in GUIDES:
    md = (HERE / f"{g}.md").read_text(encoding="utf-8")
    corpus = ""
    for f in (HERE / "raw" / g).iterdir():
        if f.suffix in (".txt", ".json", ".md"):
            try:
                corpus += " " + fq.load(g, f.name)
            except Exception:
                pass
    # also the shared facts output and any scripts' text are not quote sources
    for m in re.finditer(r'["“]([^"“”\n]{20,}?)["”]', md):
        t = m.group(1).strip()
        if len(t.split()) < 5:
            continue
        total += 1
        if fq.norm(t) not in corpus:
            bad += 1
            print("NOT FOUND in", g, "::", t[:140])
print("quoted passages checked", total, "failures", bad)
