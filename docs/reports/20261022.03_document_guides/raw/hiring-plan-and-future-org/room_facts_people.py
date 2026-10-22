"""Facts from the Hollis Voice room that the people guides cite. Run: python3 -I room_facts_people.py"""
import csv, collections, pathlib
import openpyxl

ROOM = pathlib.Path("/Users/kennethstclair/Documents/workspace/tricorder/data_room/hollis_voice")

hires = list(csv.DictReader(open(ROOM / "05_team/hiring_plan.csv")))
print("hiring_plan.csv rows:", len(hires))
by_dept = collections.Counter(h["department"] for h in hires)
print("hires by department:", dict(by_dept))
print("headcount_after_hire first/last:", hires[0]["headcount_after_hire"], hires[-1]["headcount_after_hire"])
base = [int(h["base_salary_usd"]) for h in hires]
print("sum base pay of all hires:", sum(base))
print("min/max base pay:", min(base), max(base))
starts = [h["start_date"] for h in hires]
print("first/last start date:", starts[0], starts[-1])
print("hires with a start date on the 1st of a month:", sum(1 for s in starts if s.endswith("-01")))
print("columns in hiring_plan.csv:", list(hires[0].keys()))

wb = openpyxl.load_workbook(ROOM / "02_financials/financial_model.xlsx", data_only=True)
ws = wb["Hiring_Plan"]
model_rows = [r for r in ws.iter_rows(values_only=True) if r[0] and r[1] and r[2]]
model_header = model_rows[0]
model_roles = [r[0] for r in model_rows[1:]]
print("roles in the model's Hiring_Plan tab:", len(model_roles))
print("columns in model Hiring_Plan tab:", list(model_header))
csv_roles = [h["role"] for h in hires]
print("model roles equal the first rows of the CSV:", model_roles == csv_roles[:len(model_roles)])

ct = openpyxl.load_workbook(ROOM / "02_financials/cap_table.xlsx", data_only=True)["Cap_Table"]
rows = {r[0]: r for r in ct.iter_rows(values_only=True) if r[0]}
granted = rows["Options granted (11 holders)"]
avail = rows["Options available"]
total = rows["Total"]
print("shares total:", total[2], "pro forma total:", total[4])
print("options granted shares:", granted[2], "pct fully diluted:", round(granted[3] * 100, 2))
print("options available shares:", avail[2], "pct fully diluted:", round(avail[3] * 100, 2))
pool = granted[2] + avail[2]
print("whole pool shares:", pool, "pct before A:", round(pool / total[2] * 100, 2), "pct after A:", round(pool / total[4] * 100, 2))
print("available pool shares per planned hire:", round(avail[2] / len(hires)))
print("available pool pct after A per planned hire:", round(avail[5] * 100 / len(hires), 3))
print("rows on the cap table naming an advisor:", sum(1 for k in rows if "dvis" in str(k)))

ledger = list(csv.DictReader(open(ROOM / "02_financials/expense_ledger.csv")))
tot = collections.defaultdict(float)
for r in ledger:
    tot[r["vendor"]] += float(r["amount_usd"])
for v in ["Halcyon Inference API", "Marsh Speech Licensing", "Tallow Telecom"]:
    lines = [r for r in ledger if r["vendor"] == v]
    print(v, "lines:", len(lines), "total usd:", round(tot[v], 2), "category:", {r["category"] for r in lines}, "booked_as:", {r["booked_as"] for r in lines})
print("distinct vendors:", len(tot))
print("ledger lines mentioning an AI model provider, privacy, or security vendor by description:",
      [r["description"] for r in ledger if any(k in r["description"].lower() for k in ("privacy", "security", "soc 2", "pen test", "legal"))][:5])

import json
key = json.load(open("/Users/kennethstclair/Documents/workspace/tricorder/data_room/answer_key.json"))
named = key["facts"]["team"]
staff_now = key["facts"]["staff_now"]
print("people named in the bios and deck:", len(named))
print("staff today:", staff_now)
print("staff not named anywhere in the bios:", staff_now - len(named))
print("option holders on the cap table (from the row label): 11")
print("current titles:", [p["title"] for p in named])
print("planned titles:", sorted({h["role"] for h in hires}))
cur_titles = {p["title"].lower() for p in named}
print("planned roles equal to a current title:", [h["role"] for h in hires if h["role"].lower() in cur_titles])

import re, subprocess
before_raise = [h for h in hires if h["start_date"] < "2027-01-01"]
print("hires starting before the Series A cash arrives (plan month 4, 2027-01):", len(before_raise), [h["hire_id"] for h in before_raise])
print("hires starting in 2027-01 or later:", len(hires) - len(before_raise))
print("planned hires per quarter if spread evenly over four quarters:", len(hires) / 4)
txt = subprocess.run(["pdftotext", "-layout", str(ROOM / "01_overview/pitch_deck.pdf"), "-"], capture_output=True, text=True).stdout
deck = {m.group(1): int(m.group(2)) for m in re.finditer(r"^\s*(Engineering|Sales|Customer Success|Support|Marketing|G&A):\s*(\d+)\s*$", txt, re.M)}
print("deck slide 12 breakdown:", deck)
csv_counts = dict(by_dept)
print("deck breakdown equals the CSV department counts:", deck == csv_counts)
print("deck breakdown sums to:", sum(deck.values()))

print("---- AI and data governance facts ----")
for name in ["order_form_cedar_pine.pdf", "pilot_agreement_marlow.pdf", "order_form_brookline_row.pdf"]:
    t = subprocess.run(["pdftotext", "-layout", str(ROOM / "04_customers" / name), "-"], capture_output=True, text=True).stdout
    hits = [ln.strip() for ln in t.splitlines() if re.search(r"recording|appointment data|\bdata\b|privacy|retention|train", ln, re.I) and "Synthetic data room" not in ln]
    print(name, "lines naming recordings, data, privacy, retention or training:", len(hits), hits[:2])
for h in hires:
    if h["role"] in ("Security Engineer", "Machine Learning Engineer", "Finance Manager"):
        print("planned hire:", h["hire_id"], h["role"], h["start_date"], h["base_salary_usd"])
files_text = " ".join(str(p) for p in ROOM.rglob("*") if p.is_file())
print("files in the full room whose name mentions privacy, security, model, policy, SOC, DPA or AI:",
      [p.name for p in ROOM.rglob("*") if p.is_file() and re.search(r"privacy|security|model_card|policy|soc|dpa|governance", p.name, re.I)])
print("number of files in the full room:", sum(1 for p in ROOM.rglob("*") if p.is_file()))
print("expense lines for Halcyon Inference API booked in R&D, share of all ledger spend:",
      round(tot["Halcyon Inference API"] / sum(tot.values()) * 100, 2), "percent")
