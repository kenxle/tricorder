"""Look for Form D filings by the shortlisted companies two ways:
1. issuer names in the SEC Form D quarterly data sets saved under raw/feasibility/formd/ (2026 Q3) and,
   if present, raw/demo_companies/formd/*.zip (other quarters);
2. EDGAR's company-name lookup (browse-edgar, type D, atom output), saved to raw/demo_companies/edgar_company_<slug>.xml.

Run: python3 -I demo_formd_lookup.py
"""
import csv
import io
import pathlib
import re
import time
import urllib.parse
import urllib.request
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / "raw" / "demo_companies"
UA = "Tricorder Research tricorder-research@stclair.ai"
PATTERNS = {"sazabi": r"\bsazabi\b", "tasklet": r"\btasklet\b", "expanse": r"\bexpanse (labs|compute|technologies)\b",
            "testerarmy": r"tester ?army", "ploy": r"^ploy\b", "minicor": r"\bminicor\b", "interfaze": r"\binterfaze|jigsawstack",
            "superlog": r"\bsuperlog\b"}
LOOKUP = {"sazabi": "sazabi", "tasklet": "tasklet", "expanse": "expanse", "testerarmy": "testerarmy", "ploy": "ploy",
          "minicor": "minicor", "interfaze": "interfaze", "superlog": "superlog"}


def zips():
    yield from sorted((HERE / "raw" / "feasibility" / "formd").glob("*.zip"))
    yield from sorted((RAW / "formd").glob("*.zip"))


def main():
    for z in zips():
        with zipfile.ZipFile(z) as zf:
            name = [n for n in zf.namelist() if n.upper().endswith("ISSUERS.TSV")][0]
            rows = list(csv.DictReader(io.TextIOWrapper(zf.open(name), encoding="utf-8", errors="replace"), delimiter="\t"))
        print(z.name, "issuers:", len(rows))
        for slug, pat in PATTERNS.items():
            hits = [r for r in rows if re.search(pat, r.get("ENTITYNAME", ""), re.I)]
            for h in hits:
                print("   ", slug, "|", h.get("ENTITYNAME"), "|", h.get("ACCESSIONNUMBER"), "|", h.get("STATEORCOUNTRY"), h.get("YEAROFINC_VALUE_ENTERED"))
    for slug, q in LOOKUP.items():
        url = "https://www.sec.gov/cgi-bin/browse-edgar?" + urllib.parse.urlencode({"company": q, "type": "D", "owner": "include", "count": "40", "action": "getcompany", "output": "atom"})
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
        except Exception as e:
            print(slug, "lookup FAIL", e)
            continue
        (RAW / f"edgar_company_{slug}.xml").write_bytes(data)
        names = re.findall(rb"<conformed-name>([^<]*)</conformed-name>|<title>([^<]*)</title>", data)
        print(slug, "lookup:", [ (a or b).decode()[:80] for a, b in names][:8])
        time.sleep(0.3)


if __name__ == "__main__":
    main()
