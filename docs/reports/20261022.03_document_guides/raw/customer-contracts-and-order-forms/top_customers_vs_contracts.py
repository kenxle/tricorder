"""Rank Hollis Voice customers by September 2026 MRR and mark which ones have a contract in the room.

Run: python3 -I top_customers_vs_contracts.py
Reads data_room/hollis_voice/03_metrics/customer_mrr_by_month.csv and the file names in 04_customers/.
Writes top_customers_vs_contracts.csv next to this script (top 15 customers, then the totals).
"""
import csv
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOM = HERE.parents[4] / "data_room" / "hollis_voice"
AS_OF = "2026-09"
CONTRACT_IDS = {"C0087": "order_form_cedar_pine.pdf", "C0219": "pilot_agreement_marlow.pdf", "C0193": "order_form_brookline_row.pdf"}

rows = [r for r in csv.DictReader(open(ROOM / "03_metrics" / "customer_mrr_by_month.csv")) if r["month"] == AS_OF]
mrr = {}
names = {}
types = {}
for r in rows:
    if r["product_type"] == "Onboarding":
        continue
    mrr[r["customer_id"]] = mrr.get(r["customer_id"], 0) + float(r["mrr"])
    names[r["customer_id"]] = r["customer_name"]
    types[r["customer_id"]] = r["product_type"]
ranked = sorted(mrr, key=lambda c: -mrr[c])
total = sum(mrr.values())
files = sorted(p.name for p in (ROOM / "04_customers").glob("*.pdf"))
assert set(CONTRACT_IDS.values()) == set(files), files

with open(HERE / "top_customers_vs_contracts.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["rank", "customer_id", "customer_name", "product_type", "mrr_2026_09", "share_of_counted_mrr", "contract_in_room"])
    for i, c in enumerate(ranked[:15], 1):
        w.writerow([i, c, names[c], types[c], mrr[c], round(mrr[c] / total, 4), CONTRACT_IDS.get(c, "")])
top10 = ranked[:10]
print("customers with MRR in", AS_OF, ":", len(ranked))
print("counted MRR (all product types except onboarding):", total)
print("top 10 with a contract in the room:", [c for c in top10 if c in CONTRACT_IDS])
print("count of top 10 with a contract:", sum(1 for c in top10 if c in CONTRACT_IDS))
print("contracts in the room that are outside the top 10:", [c for c in CONTRACT_IDS if c not in top10])
print("top 10 share of counted MRR:", round(sum(mrr[c] for c in top10) / total, 4))
print("rank of Marlow:", ranked.index("C0219") + 1, "rank of Cedar:", ranked.index("C0087") + 1, "rank of Brookline:", ranked.index("C0193") + 1)
