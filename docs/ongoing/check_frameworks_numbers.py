"""Check that the Hollis Voice figures FRAMEWORKS.md quotes match the answer key.

Every figure below is computed here from data_room/answer_key.json (and, for a few
cost and cap-table lines, from the generated files in data_room/hollis_voice/),
formatted the way FRAMEWORKS.md writes it, and looked for in FRAMEWORKS.md. A figure
that is missing means the doc and the key disagree, or the doc stopped quoting it.
It also fails if a figure the generator no longer produces is still in the doc.

Run: data_room/.venv/bin/python docs/ongoing/check_frameworks_numbers.py
(plain python3 works too; it reads the CSVs only, not the workbooks).
Exits 0 when every check passes, 1 otherwise.
"""

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = (ROOT / "docs" / "ongoing" / "FRAMEWORKS.md").read_text(encoding="utf-8")
KEY = json.loads((ROOT / "data_room" / "answer_key.json").read_text(encoding="utf-8"))
ROOM = ROOT / "data_room" / "hollis_voice"


def usd(x, cents=False):
    return f"${x:,.2f}" if cents else f"${round(x):,}"


def pct(x, places=1):
    return f"{x * 100:.{places}f}%"


flags = {f["id"]: f for f in KEY["flags"]}
decoys = {d["id"]: d for d in KEY["decoys"]}
greens = {g["id"]: g for g in KEY["green_flags"]}
facts = KEY["facts"]
BIG_FEE = int(next(l["text"] for l in flags["PF5"]["locations"] if "order_form" in l["file"]).split()[0].strip("$").replace(",", ""))
PILOT_FEE = flags["PF1"]["shown"]["details"]["pilot_arr_counted"] / 12

checks = []


def need(label, text):
    checks.append((label, text))


# Planted flags: shown and true values.
need("PF1 shown, model ARR", usd(flags["PF1"]["shown"]["value"]))
need("PF1 true, recurring ARR", usd(flags["PF1"]["true"]["value"]))
need("PF1 pilot counted as ARR", usd(flags["PF1"]["shown"]["details"]["pilot_arr_counted"]))
need("PF1 pilot fees in total", usd(flags["PF1"]["true"]["details"]["pilot_fees_contracted_total"]))
need("PF1 notice days", f"{flags['PF1']['true']['details']['pilot_notice_days']} days")
need("PF2 shown, deck ARR", usd(flags["PF2"]["shown"]["value"]))
need("PF2 gap to model", usd(flags["PF2"]["shown"]["details"]["gap_to_model"]))
need("PF2b shown, spoken ARR", usd(flags["PF2b"]["shown"]["value"]))
need("PF3 shown NRR", pct(flags["PF3"]["shown"]["value"]))
need("PF3 true NRR", pct(flags["PF3"]["true"]["value"]))
need("PF3 rebuilt GRR", pct(flags["PF3"]["true"]["details"]["gross_revenue_retention"]))
need("PF3 customers shown", f"{flags['PF3']['shown']['details']['customers']} shown")
need("PF3 customers rebuilt", f"{flags['PF3']['true']['details']['customers']} rebuilt")
need("PF3 customers dropped", f"{flags['PF3']['true']['details']['customers_dropped']} dropped")
need("PF4 runway shown", f"{flags['PF4']['shown']['value']} months")
need("PF4 runway rebuilt", f"{flags['PF4']['true']['value']} months")
need("PF4 hires in the model", f"The model counts {flags['PF4']['shown']['details']['hires_counted']}")
need("PF4 hires in the plan", f"The plan holds {flags['PF4']['true']['details']['hires_in_plan']} hires")
need("PF4 burn shown", usd(flags["PF4"]["shown"]["details"]["avg_net_burn_first_12_months"]))
need("PF4 burn rebuilt", usd(flags["PF4"]["true"]["details"]["avg_net_burn_first_12_months"]))
need("PF5 largest share", pct(flags["PF5"]["true"]["value"]))
need("PF5 top three share", pct(flags["PF5"]["true"]["details"]["top3_share"]))
need("PF5 deck ceiling", f"{round(flags['PF5']['shown']['value'] * 100)}% of ARR")
need("PF6 shown margin", f"{round(flags['PF6']['shown']['value'] * 100)}%")
need("PF6 rebuilt margin", pct(flags["PF6"]["true"]["value"]))
need("PF7 shown clinics", str(flags["PF7"]["shown"]["value"]))
need("PF7 paying accounts", str(flags["PF7"]["true"]["value"]))

# Arithmetic on the flags that the doc quotes.
need("excess over recurring ARR", pct((facts["arr_model"] - facts["arr_true_recurring"]) / facts["arr_true_recurring"]))
need("deck against model", pct(facts["arr_deck"] / facts["arr_model"] - 1))
need("deck against rebuilt", pct(facts["arr_deck"] / facts["arr_true_recurring"] - 1))
need("video against deck", pct(facts["arr_video"] / facts["arr_deck"] - 1))
need("video against model", pct(facts["arr_video"] / facts["arr_model"] - 1))
need("burn gap", usd(facts["true_avg_net_burn_12m"] - facts["model_avg_net_burn_12m"]))
need("ARPA", usd(facts["mrr_subscription"] / facts["paying_accounts"], cents=True))
need("ACV", usd(facts["arr_true_recurring"] / facts["paying_accounts"]))
need("largest customer on model ARR", pct(BIG_FEE * 12 / facts["arr_model"]))
for label, stated, found in [("runway", 37, 19), ("clinics", 357, 212), ("largest customer", 9, 21),
                             ("gross margin", 80, 58.1), ("retention", 102.6, 87.3)]:
    need(f"top red flag gap, {label}", pct(abs(stated - found) / found))

# Decoys.
need("DC1 onboarding fee", "$500")
need("DC2 annual fee", usd(decoys["DC2"]["details"]["annual_fee"]))
need("DC2 monthly revenue", usd(decoys["DC2"]["details"]["monthly_revenue"]))
need("DC2 list price", usd(decoys["DC2"]["details"]["list_price"]))
need("DC3 Series A ownership", pct(next(l["expect"] for l in decoys["DC3"]["locations"] if l.get("cell") == "B28"), 2))

# Green flags.
need("GF1 raise", usd(greens["GF1"]["number"]))
need("GF2 market size", usd(greens["GF2"]["number"]))
need("GF3 staff today", f"{greens['GF3']['number']} staff today")
need("GF3 staff after hiring", f"to {greens['GF3']['also_agree'][0]['number']}")

# Key facts the doc quotes.
need("subscription MRR", usd(facts["mrr_subscription"]))
need("cash", usd(facts["cash"]))
need("pre-money", usd(facts["pre_money"]))
need("post-money", usd(facts["pre_money"] + facts["ask"]))
need("SAFEs before the Series A", usd(facts["raised_before_series_a"]))
need("pre-seed SAFEs", usd(facts["pre_seed_safes"]))
need("seed SAFE", usd(facts["seed_safe"]))
need("cash bridge difference", f"−${abs(facts['cash_bridge_difference']):.2f}")
need("largest customer locations", f"{facts['big_customer_locations']} locations")

# Generated files: the 2026-09 cost lines and the missing hires.
ledger = list(csv.DictReader(open(ROOM / "02_financials" / "expense_ledger.csv", newline="")))
sep = {}
for row in ledger:
    if row["month"] == "2026-09":
        sep[row["category"]] = sep.get(row["category"], 0) + float(row["amount_usd"])
cor = sep["telephony"] + sep["third_party_licences"]
hosting = sep["cloud_hosting"] + sep["model_inference"]
support = sep["support_staff"]
need("cost of revenue shown, 2026-09", usd(cor, cents=True))
need("hosting and inference, 2026-09", usd(hosting, cents=True))
need("support staff, 2026-09", usd(support, cents=True))
need("full cost of revenue, 2026-09", usd(cor + hosting + support, cents=True))
need("Tallow share of full cost of revenue", pct(sep["telephony"] / (cor + hosting + support)))
need("rebuilt margin from the lines", pct(1 - (cor + hosting + support) / (facts["mrr_subscription"] + PILOT_FEE)))
hires = list(csv.DictReader(open(ROOM / "05_team" / "hiring_plan.csv", newline="")))
missing = hires[flags["PF4"]["shown"]["details"]["hires_counted"]:]
need("missing hires, loaded monthly cost", usd(sum(int(h["base_salary_usd"]) for h in missing) * 1.28 / 12))
need("full room file count", f"The {len(KEY['full_room_files'])} files in the full room")

# Figures the generator no longer produces.
stale = ["$165,000", "$17,600 a month", "two SAFEs and an option pool", "$2,000,000 ÷ $12,000,000 = 16.67%",
         "The 16 files", "data_room_design_numbers", "data_room_planted.csv"]


def main():
    problems = [f"{label}: '{text}' not found" for label, text in checks if text not in DOC]
    problems += [f"stale figure still in the doc: '{t}'" for t in stale if t in DOC]
    print(f"{len(checks)} figures checked against data_room/answer_key.json and the generated files")
    print(f"{len(stale)} stale figures checked for absence")
    if problems:
        for p in problems:
            print("FAIL:", p)
        sys.exit(1)
    print("PASS: every figure FRAMEWORKS.md quotes for the planted flags, decoys and green flags matches the key")


if __name__ == "__main__":
    main()
