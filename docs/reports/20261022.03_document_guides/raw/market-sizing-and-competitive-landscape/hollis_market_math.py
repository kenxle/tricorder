import openpyxl
wb = openpyxl.load_workbook("/Users/kennethstclair/Documents/workspace/tricorder/data_room/hollis_voice/02_financials/financial_model.xlsx", data_only=True)
ws = wb["Market"]
vals = {r[0]: r[1] for r in ws.iter_rows(values_only=True) if r[0] and isinstance(r[1], (int, float))}
for k, v in vals.items(): print(k, "=", v)
clinics = [v for k, v in vals.items() if k.startswith("US independent")][0]
acv = [v for k, v in vals.items() if k.startswith("Annual contract")][0]
obs = [v for k, v in vals.items() if k.startswith("For comparison")][0]
print("deck TAM  = clinics x planning ACV =", clinics * acv)
print("same clinics x observed subscription ARR per paying clinic =", round(clinics * obs))
print("planning ACV as a share of observed =", round(acv / obs * 100, 1), "percent")
import json
facts = json.load(open("/Users/kennethstclair/Documents/workspace/tricorder/data_room/answer_key.json"))["facts"]
paying = facts["paying_accounts"]
print("paying accounts (answer key facts):", paying)
print("paying accounts as a share of the deck's 28,000 clinics =", round(paying / clinics * 100, 2), "percent")
print("deck TAM against $1,000,000,000 =", round(clinics * acv / 1e9 * 100, 1), "percent of one billion")
