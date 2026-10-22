"""Total the Hollis Voice expense ledger by vendor, for the material-agreements guide.

Run: python3 -I ledger_vendor_totals.py
Reads data_room/hollis_voice/02_financials/expense_ledger.csv (synthetic room).
Writes ledger_vendor_totals.csv next to this script: one row per vendor and category.
Threshold 25000 is the DocSend checklist figure for "obligations exceeding $25,000".
"""
import csv
import pathlib
from collections import defaultdict

HERE = pathlib.Path(__file__).resolve().parent
LEDGER = HERE.parents[4] / "data_room" / "hollis_voice" / "02_financials" / "expense_ledger.csv"
THRESHOLD = 25000
LAST12_FROM = "2025-10"

rows = list(csv.DictReader(open(LEDGER)))
total = defaultdict(float)
last12 = defaultdict(float)
months = defaultdict(set)
booked = defaultdict(set)
for r in rows:
    k = (r["vendor"], r["category"])
    amt = float(r["amount_usd"])
    total[k] += amt
    months[k].add(r["month"])
    booked[k].add(r["booked_as"])
    if r["month"] >= LAST12_FROM:
        last12[k] += amt

out = HERE / "ledger_vendor_totals.csv"
with open(out, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["vendor", "category", "booked_as", "months_with_lines", "total_usd", "last_12_months_usd", "over_threshold_last_12"])
    for k in sorted(total, key=lambda k: -last12[k]):
        w.writerow([k[0], k[1], "|".join(sorted(booked[k])), len(months[k]), round(total[k], 2), round(last12[k], 2), last12[k] > THRESHOLD])
print("rows in ledger:", len(rows))
print("vendor-category rows written:", len(total))
print("over threshold in last 12 months:", sum(1 for k in total if last12[k] > THRESHOLD))
non_payroll = [k for k in total if not k[1].startswith("payroll") and k[1] != "support_staff"]
print("non-payroll vendor-category rows:", len(non_payroll))
print("non-payroll over threshold in last 12 months:", sum(1 for k in non_payroll if last12[k] > THRESHOLD))
print("distinct non-payroll vendors over threshold:", len({k[0] for k in non_payroll if last12[k] > THRESHOLD}))

rent = sorted((r["month"], float(r["amount_usd"])) for r in rows if r["category"] == "rent")
steps = [(rent[i][0], rent[i - 1][1], rent[i][1]) for i in range(1, len(rent)) if rent[i][1] != rent[i - 1][1]]
print("rent months:", len(rent), "first:", rent[0], "last:", rent[-1])
print("months where rent changed from the month before:", len(steps))
for s in steps:
    print("  rent change in", s[0], "from", s[1], "to", s[2])
ins = [float(r["amount_usd"]) for r in rows if r["category"] == "insurance"]
print("insurance lines:", len(ins), "total:", round(sum(ins), 2))
