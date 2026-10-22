"""Counts from the SEC Form D data set for 2026 Q3. Run: python3 -I formd_counts.py 2026q3_d.zip"""
import csv, io, sys, zipfile, collections
csv.field_size_limit(10**7)
z = zipfile.ZipFile(sys.argv[1])
def rows(suffix):
    name = [n for n in z.namelist() if n.endswith(suffix)][0]
    with z.open(name) as f:
        yield from csv.DictReader(io.TextIOWrapper(f, encoding="utf-8", errors="replace"), delimiter="\t")
sub = {r["ACCESSIONNUMBER"]: r for r in rows("FORMDSUBMISSION.tsv")}
iss = {}
for r in rows("ISSUERS.tsv"):
    if r["IS_PRIMARYISSUER_FLAG"] == "YES":
        iss[r["ACCESSIONNUMBER"]] = r
groups = collections.Counter()
tech_equity_5_20 = []
n_off = 0
dates = []
for r in rows("OFFERING.tsv"):
    n_off += 1
    groups[r["INDUSTRYGROUPTYPE"]] += 1
    s = sub.get(r["ACCESSIONNUMBER"], {})
    dates.append(s.get("FILING_DATE", ""))
    try:
        amt = float(r["TOTALOFFERINGAMOUNT"])
    except ValueError:
        continue
    if r["INDUSTRYGROUPTYPE"] == "Other Technology" or r["INDUSTRYGROUPTYPE"] == "Computers":
        if r["ISEQUITYTYPE"] == "true" and 5_000_000 <= amt <= 20_000_000:
            tech_equity_5_20.append((iss.get(r["ACCESSIONNUMBER"], {}).get("ENTITYNAME", "?"), amt, r["INDUSTRYGROUPTYPE"]))
print("offerings in file:", n_off)
print("industry groups with counts:")
for g, c in groups.most_common(12):
    print(f"  {g}: {c}")
print("technology-type equity offerings between 5M and 20M:", len(tech_equity_5_20))
for e in tech_equity_5_20[:5]:
    print("  sample:", e)
