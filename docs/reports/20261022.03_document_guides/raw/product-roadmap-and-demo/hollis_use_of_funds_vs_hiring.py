import csv, collections
rows = list(csv.DictReader(open("/Users/kennethstclair/Documents/workspace/tricorder/data_room/hollis_voice/05_team/hiring_plan.csv")))
groups = {"Engineering": ["Engineering"], "Sales and marketing": ["Sales", "Marketing"],
          "Customer success and support": ["Customer Success", "Support"], "General and administrative": ["G&A"]}
funds = {"Engineering": 3600000, "Sales and marketing": 3150000, "Customer success and support": 1350000, "General and administrative": 900000}
n = len(rows); pay_total = sum(float(r["base_salary_usd"]) for r in rows)
print("hires:", n, "| base pay of all hires:", round(pay_total), "| use of funds total:", sum(funds.values()))
for g, deps in groups.items():
    h = [r for r in rows if r["department"] in deps]
    pay = sum(float(r["base_salary_usd"]) for r in h)
    print(f"{g}: use of funds {funds[g]} = {funds[g]/sum(funds.values())*100:.1f} pct | hires {len(h)} = {len(h)/n*100:.1f} pct of hires | base pay {round(pay)} = {pay/pay_total*100:.1f} pct of hire base pay")
