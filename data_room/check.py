#!/usr/bin/env python3
"""The room's test. Reads the generated files back and checks every planted flag and decoy.

Run after generate.py, with the room's virtual environment:

    data_room/.venv/bin/python data_room/check.py

It reads answer_key.json and the files under data_room/hollis_voice/. For each flag it checks that the shown
value is where the key says it is, then recomputes the true value from the raw files (the way a diligence
scan would) and checks it matches the key. It exits with a non-zero status if anything is missing or wrong.

Workbooks are read with openpyxl. Formula cells are read for their stored values, which xlsxwriter writes.
PDFs are read with pdfplumber. CSV files are read with the csv module.
"""
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import openpyxl
import pdfplumber

HERE = Path(__file__).resolve().parent
KEY = json.loads((HERE / "answer_key.json").read_text(encoding="utf-8"))
ROOM = HERE / "hollis_voice"
SEED_DROP = HERE / "hollis_voice_seed_drop"

PASSES, FAILS = [], []


def ok(name, cond, detail=""):
    (PASSES if cond else FAILS).append(name)
    print(f"{'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail and not cond else ""))
    return cond


def near(a, b, tol_abs=0.0, tol_rel=0.0):
    return abs(a - b) <= max(tol_abs, tol_rel * abs(b))


# ---- readers -----------------------------------------------------------------------------------
_wb_cache, _pdf_cache = {}, {}


def workbook(rel, data_only=True):
    k = (rel, data_only)
    if k not in _wb_cache:
        _wb_cache[k] = openpyxl.load_workbook(ROOM / rel, data_only=data_only)
    return _wb_cache[k]


def named(wb, name):
    d = wb.defined_names[name]
    sheet, cell = d.attr_text.split("!")
    return wb[sheet.strip("'")][cell.replace("$", "")].value


def pdf_pages(rel):
    if rel not in _pdf_cache:
        with pdfplumber.open(ROOM / rel) as pdf:
            _pdf_cache[rel] = [(p.extract_text() or "") for p in pdf.pages]
    return _pdf_cache[rel]


def squash(t):
    return re.sub(r"\s+", " ", t)


def read_csv(rel):
    with open(ROOM / rel, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def num(s):
    return float(str(s).replace("$", "").replace(",", ""))


# ---- files exist, page counts, footer, no em dashes --------------------------------------------
def check_files():
    pages = {"00_welcome/cover_note_and_index.pdf": 1, "01_overview/pitch_deck.pdf": 14, "01_overview/company_overview.pdf": 1,
             "04_customers/order_form_cedar_pine.pdf": 3, "04_customers/pilot_agreement_marlow.pdf": 3,
             "04_customers/order_form_brookline_row.pdf": 2, "05_team/founder_bios.pdf": 2, "06_product/product_one_pager.pdf": 1}
    for rel in KEY["full_room_files"]:
        ok(f"file exists: {rel}", (ROOM / rel).is_file())
    for rel, n in pages.items():
        got = len(pdf_pages(rel))
        ok(f"page count {rel} is {n}", got == n, f"got {got}")
        ok(f"footer on every page of {rel}", all("Synthetic data room for Deal Flow NYC 2026" in p for p in pdf_pages(rel)))
    dash = []
    for rel in KEY["full_room_files"]:
        if rel.endswith(".pdf"):
            text = "\n".join(pdf_pages(rel))
        elif rel.endswith(".xlsx"):
            text = "\n".join(str(c.value) for ws in workbook(rel).worksheets for row in ws.iter_rows() for c in row if isinstance(c.value, str))
        else:
            text = (ROOM / rel).read_text(encoding="utf-8")
        if "—" in text:
            dash.append(rel)
    ok("no em dashes in any room file", not dash, str(dash))
    for rel in ("02_financials/financial_model.xlsx", "02_financials/cap_table.xlsx"):
        wb = workbook(rel)
        ok(f"footer on every sheet of {rel}", all(any(isinstance(c.value, str) and c.value.startswith("Synthetic data room") for row in ws.iter_rows() for c in row)
                                                  for ws in wb.worksheets))
    for rel in KEY["seed_drop_files"]:
        a, b = ROOM / rel, SEED_DROP / rel
        ok(f"seed drop copy identical: {rel}", b.is_file() and a.read_bytes() == b.read_bytes())
    ok("seed drop holds only the first-tier files",
       sorted(str(p.relative_to(SEED_DROP)) for p in SEED_DROP.rglob("*") if p.is_file()) == sorted(KEY["seed_drop_files"]))


def check_formulas_have_values():
    for rel in ("02_financials/financial_model.xlsx", "02_financials/cap_table.xlsx"):
        wf, wv = workbook(rel, False), workbook(rel, True)
        n, empty = 0, []
        for ws in wf.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str) and c.value.startswith("="):
                        n += 1
                        if wv[ws.title][c.coordinate].value is None:
                            empty.append(f"{ws.title}!{c.coordinate}")
        ok(f"{rel}: {n} formula cells all carry stored values", n > 0 and not empty, str(empty[:5]))


# ---- the key's own locations --------------------------------------------------------------------
def check_locations():
    for entry in KEY["flags"] + KEY["decoys"]:
        for loc in entry["locations"]:
            tag = f"{entry['id']} location: {loc['file']} {loc.get('sheet', '')}{loc.get('cell', '')}{loc.get('text', '')[:40] if 'text' in loc else ''}"
            rel = loc["file"]
            if rel.endswith(".xlsx") and "cell" in loc:
                wb = workbook(rel)
                cell = loc["cell"]
                if ":" in cell:
                    vals = [c.value for row in wb[loc["sheet"]][cell] for c in row]
                    ok(tag, all(isinstance(v, (int, float)) for v in vals) and len(vals) == 12)
                    continue
                val = wb[loc["sheet"]][cell].value
                if "named_cell" in loc:
                    ok(tag + " (named cell points here)", named(wb, loc["named_cell"]) == val)
                exp = loc.get("expect")
                if exp is None:
                    ok(tag, val is not None)
                elif isinstance(exp, str):
                    ok(tag, val == exp, f"got {val!r}")
                else:
                    ok(tag, isinstance(val, (int, float)) and near(val, exp, 1e-6, 1e-6), f"got {val!r} want {exp!r}")
            elif rel.endswith(".pdf") and "page" in loc:
                text = squash(pdf_pages(rel)[loc["page"] - 1])
                ok(tag, squash(loc["text"]) in text, f"page {loc['page']} lacks the text")
            elif rel.endswith(".md"):
                text = squash((ROOM / rel).read_text(encoding="utf-8"))
                ok(tag, squash(loc["text"]) in text)
            elif rel.endswith(".csv") and "customer_name" in loc:
                rows = [r for r in read_csv(rel) if r["customer_name"] == loc["customer_name"] and r["month"] == "2026-09"]
                ok(tag, len(rows) == 1 and rows[0]["product_type"] == loc["product_type"] and int(rows[0]["mrr"]) == loc["mrr"]
                   and rows[0]["customer_id"] == loc["customer_id"])


# ---- raw-file readers used by the flag checks ---------------------------------------------------
def cust_rows():
    return read_csv("03_metrics/customer_mrr_by_month.csv")


def claims():
    out = {}
    for line in pdf_pages("01_overview/pitch_deck.pdf")[13].splitlines():
        m = re.match(r"^(.*?)\s+(\$?[\d,\.]+%?(?: months| \(12 months\))?|under 9% of ARR)\s+(\d+)$", line.strip())
        if m:
            out[m.group(1)] = (m.group(2), int(m.group(3)))
    return out


def flag(fid):
    return next(f for f in KEY["flags"] if f["id"] == fid)


def month_index(label):
    y, m = label.split("-")
    return (int(y) - 2025) * 12 + int(m) - 1


def check_claims_page():
    got = claims()
    want = {c["label"]: (c["value"], c["slide"]) for c in KEY["deck_claims"]}
    ok("claims page lists every claim in the key", got == want, f"missing {set(want) - set(got)}")
    # each claim's slide holds the number (where the slide shows it in the same form)
    deck = pdf_pages("01_overview/pitch_deck.pdf")
    for label, (val, slide) in want.items():
        if label in ("ARR", "Calls handled, September 2026", "Largest customer", "Net revenue retention", "Clinics on Hollis"):
            probe = {"ARR": "$2.5M", "Largest customer": "9% of ARR"}.get(label, val.split(" ")[0])
            ok(f"claims row '{label}' appears on slide {slide}", probe in deck[slide - 1], probe)


def check_pf1():
    f = flag("PF1")
    wb = workbook("02_financials/financial_model.xlsx")
    arr_total = named(wb, "ARR_TOTAL")
    rows = cust_rows()
    sub = sum(int(r["mrr"]) for r in rows if r["month"] == "2026-09" and r["product_type"] == "Subscription")
    pilot = sum(int(r["mrr"]) for r in rows if r["month"] == "2026-09" and r["product_type"] == "Pilot")
    ok("PF1 true ARR from Subscription rows matches the key", 12 * sub == f["true"]["value"], f"{12 * sub}")
    ok("PF1 model ARR_TOTAL is the shown value", arr_total == f["shown"]["value"])
    ok("PF1 gap between ARR_TOTAL and Subscription ARR is the pilot at 12 months", arr_total - 12 * sub == 12 * pilot == f["shown"]["details"]["pilot_arr_counted"])
    ok("PF1 model ARR exceeds true ARR by more than the tolerance", (arr_total - 12 * sub) / (12 * sub) > f["tolerance"])
    m = {r["month"]: r for r in read_csv("03_metrics/monthly_metrics.csv")}
    ok("PF1 monthly_metrics arr (2026-09) counts the pilot", int(m["2026-09"]["arr"]) == arr_total)
    t = squash("\n".join(pdf_pages("04_customers/pilot_agreement_marlow.pdf")))
    ok("PF1 pilot agreement: six-month term and $90,000 in clause 2", "2. Term and fees." in t and "six (6) months" in t and "$90,000" in t)
    ok("PF1 pilot agreement: 30 days notice in clause 7", "7. Termination." in t and "thirty (30) days written notice" in t)
    ok("PF1 pilot agreement: no duty to convert in clause 8", "8. No duty to convert." in t)
    ok("PF1 pilot fees contracted equal the key", 15000 * 6 == f["true"]["details"]["pilot_fees_contracted_total"])


def check_pf2():
    f = flag("PF2")
    wb = workbook("02_financials/financial_model.xlsx")
    arr_total = named(wb, "ARR_TOTAL")
    deck = num(claims()["ARR"][0])
    ok("PF2 deck claims-page ARR is the shown value", deck == f["shown"]["value"])
    ok("PF2 model ARR_TOTAL is the true value (the model figure)", arr_total == f["true"]["value"])
    gap = deck - arr_total
    ok("PF2 gap to the model is as keyed", gap == f["shown"]["details"]["gap_to_model"], str(gap))
    ok("PF2 gap exceeds the 1 percent tolerance", gap / arr_total > f["tolerance"])


def check_pf2b():
    f = flag("PF2b")
    text = (ROOM / "01_overview/pitch_video_script.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*0:35[^\n]*\n\n(.*?)\n\n\*\*", text, re.S)
    ok("PF2b script has a 0:35 section", bool(m))
    para = m.group(1) if m else ""
    spoken = 3_000_000 if "three million dollars in annual recurring revenue" in para else None
    ok("PF2b spoken ARR is about three million dollars", spoken == f["shown"]["value"])
    deck = num(claims()["ARR"][0])
    ok("PF2b spoken ARR differs from the deck beyond the tolerance", spoken is not None and abs(spoken - deck) / deck > f["tolerance"] and deck == f["true"]["value"])
    words = len(" ".join(l for l in text.splitlines() if l and not l.startswith(("**", "#", "Read this", "---", "Synthetic"))).split())
    ok("PF2b script is about 300 words", 250 <= words <= 340, str(words))


def cohorts_from_csv():
    by = defaultdict(dict)
    for r in cust_rows():
        if r["product_type"] == "Subscription":
            by[r["customer_id"]][month_index(r["month"])] = int(r["mrr"])
    res = []
    for s in range(0, 9):
        group = [c for c, v in by.items() if min(v) == s]
        start = sum(by[c][s] for c in group)
        end = sum(by[c].get(s + 12, 0) for c in group)
        capped = sum(min(by[c].get(s + 12, 0), by[c][s]) for c in group)
        early, kept = [], []
        for c in group:
            last = max(by[c])
            churn = last + 1 if last < 20 else None
            (early if churn is not None and churn - s <= 2 else kept).append(c)
        res.append({"n": len(group), "early": len(early), "start": start, "end": end, "capped": capped,
                    "k_n": len(kept), "k_start": sum(by[c][s] for c in kept), "k_end": sum(by[c].get(s + 12, 0) for c in kept)})
    return res


def check_pf3():
    f = flag("PF3")
    wb = workbook("02_financials/financial_model.xlsx")
    res = cohorts_from_csv()
    ts = sum(r["start"] for r in res)
    nrr, grr = sum(r["end"] for r in res) / ts, sum(r["capped"] for r in res) / ts
    n_true = sum(r["n"] for r in res)
    ok("PF3 rebuilt net retention matches the key", near(nrr, f["true"]["value"], f["tolerance"] / 5), f"{nrr:.4f}")
    ok("PF3 rebuilt gross retention matches the key", near(grr, f["true"]["details"]["gross_revenue_retention"], f["tolerance"] / 5), f"{grr:.4f}")
    ok("PF3 rebuilt customer count is 68", n_true == f["true"]["details"]["customers"])
    ok("PF3 Cohorts tab customer total is the shown 57", named(wb, "COHORT_CUSTOMERS") == f["shown"]["details"]["customers"])
    ok("PF3 Cohorts tab net retention is the shown value", near(named(wb, "NRR_12M"), f["shown"]["value"], f["tolerance"] / 5))
    tab = wb["Cohorts"]
    first_col = [tab.cell(row=r, column=1).value for r in range(5, 14)]
    ok("PF3 nine cohorts are listed", len(first_col) == 9 and first_col[0] == "2025-01" and first_col[-1] == "2025-09")
    ok("PF3 tab drops the early leavers cohort by cohort", all(tab.cell(row=5 + i, column=2).value == r["k_n"] for i, r in enumerate(res)))
    ok("PF3 dropped customers equal the early leavers", n_true - sum(r["k_n"] for r in res) == f["true"]["details"]["customers_dropped"] == sum(r["early"] for r in res))
    ok("PF3 deck slide 6 shows the shown retention", f"{f['shown']['value'] * 100:.1f}%" in pdf_pages("01_overview/pitch_deck.pdf")[5])
    ok("PF3 gap between shown and true net retention is material", f["shown"]["value"] - f["true"]["value"] > 0.1)


def hires_from_csv():
    out = []
    for r in read_csv("05_team/hiring_plan.csv"):
        y, m, _ = r["start_date"].split("-")
        t = (int(y) - 2026) * 12 + int(m) - 9
        out.append((t, float(r["base_salary_usd"])))
    return out


def rerun_cash(wb, hires):
    a = lambda n: named(wb, n)
    load = a("LOAD_FACTOR")
    payroll = a("STAFF_NOW") * a("AVG_BASE_NOW") * load / 12
    rev, cash, burns, runway = a("REV_START_USD_MONTH"), a("CASH_START"), [], None
    for t in range(1, 61):
        payroll += sum(b for (st, b) in hires if st == t) * load / 12
        rev *= 1 + a("REV_GROWTH")
        cogs = rev * (a("TELEPHONY_PCT") + a("LICENCES_PCT"))
        prog = a("PROGRAMS_USD_MONTH") if t >= a("SERIES_A_PLAN_MONTH") else 0
        burn = payroll + a("HOSTING_USD_MONTH") + a("RENT_ETC_USD_MONTH") + prog + cogs - rev
        if t == a("SERIES_A_PLAN_MONTH"):
            cash += a("SERIES_A_RAISE")
        cash -= burn
        burns.append(burn)
        if cash <= 0 and runway is None:
            runway = t - 1
    return runway, sum(burns[:12]) / 12


def check_pf4():
    f = flag("PF4")
    wb = workbook("02_financials/financial_model.xlsx")
    hires = hires_from_csv()
    ok("PF4 hiring_plan.csv lists 24 hires", len(hires) == f["true"]["details"]["hires_in_plan"] == 24)
    ok("PF4 model Hiring_Plan counts 8 hires", named(wb, "HIRES_COUNTED") == f["shown"]["details"]["hires_counted"] == 8)
    ws = wb["Hiring_Plan"]
    model_roles = [ws.cell(row=r, column=1).value for r in range(5, 13)]
    csv_roles = [r["role"] for r in read_csv("05_team/hiring_plan.csv")][:8]
    ok("PF4 the model's eight hires are the first eight in the plan", model_roles == csv_roles)
    runway_true, burn_true = rerun_cash(wb, hires)
    runway_model, burn_model = rerun_cash(wb, hires[:8])
    ok("PF4 runway rerun with all 24 hires matches the key (19)", runway_true == f["true"]["value"], str(runway_true))
    ok("PF4 average burn rerun with all 24 hires matches the key", near(burn_true, f["true"]["details"]["avg_net_burn_first_12_months"], 1.0), f"{burn_true:.0f}")
    ok("PF4 rerun with the model's 8 hires reproduces Cash_Runway (37)", runway_model == named(wb, "RUNWAY_MONTHS") == f["shown"]["value"], str(runway_model))
    ok("PF4 model average burn matches the key", near(named(wb, "AVG_NET_BURN_12M"), f["shown"]["details"]["avg_net_burn_first_12_months"], 1.0))
    claim = claims()
    ok("PF4 deck claims-page runway is the shown value", claim["Runway"][0] == f"{f['shown']['value']} months")
    ok("PF4 deck claims-page burn is the shown value", num(claim["Average monthly net burn, next 12 months"][0]) == f["shown"]["details"]["avg_net_burn_first_12_months"])
    ok("PF4 deck says 24 planned hires", claim["Planned hires, next 12 months"][0] == "24")
    ok("PF4 runway gap is material", f["shown"]["value"] - f["true"]["value"] >= 12)


def check_pf5():
    f = flag("PF5")
    rows = [r for r in cust_rows() if r["month"] == "2026-09" and r["product_type"] == "Subscription"]
    mrr = sorted((int(r["mrr"]) for r in rows), reverse=True)
    total = sum(mrr)
    top1, top3 = mrr[0] / total, sum(mrr[:3]) / total
    ok("PF5 top customer share matches the key", near(top1, f["true"]["value"], 0.0005), f"{top1:.4f}")
    ok("PF5 top-three share matches the key", near(top3, f["true"]["details"]["top3_share"], 0.0005), f"{top3:.4f}")
    big = [r for r in rows if r["customer_id"] == "C-BIG"]
    ok("PF5 the largest customer is C-BIG, Cedar & Pine, 17 locations", len(big) == 1 and int(big[0]["mrr"]) == mrr[0] and big[0]["locations"] == "17"
       and big[0]["customer_name"] == "Cedar & Pine Animal Hospitals")
    ok("PF5 deck claims the largest customer is under 9%", claims()["Largest customer"][0] == "under 9% of ARR" and top1 > f["shown"]["value"])


def check_pf6():
    f = flag("PF6")
    wb = workbook("02_financials/financial_model.xlsx")
    led = defaultdict(float)
    for r in read_csv("02_financials/expense_ledger.csv"):
        if r["month"] == "2026-09":
            led[r["category"]] += float(r["amount_usd"])
    rows = [r for r in cust_rows() if r["month"] == "2026-09" and r["product_type"] in ("Subscription", "Pilot")]
    basis = sum(int(r["mrr"]) for r in rows)
    shown = 1 - (led["telephony"] + led["third_party_licences"]) / basis
    true = 1 - (led["telephony"] + led["third_party_licences"] + led["cloud_hosting"] + led["model_inference"] + led["support_staff"]) / basis
    ok("PF6 ledger gross margin with only telephony and licences is the shown 80%", near(shown, f["shown"]["value"], 0.0005), f"{shown:.4f}")
    ok("PF6 ledger gross margin with all delivery costs matches the key", near(true, f["true"]["value"], f["tolerance"] / 2), f"{true:.4f}")
    ok("PF6 model GM_PCT is the shown value", near(named(wb, "GM_PCT"), f["shown"]["value"], 0.0005))
    ws = wb["P&L"]
    labels = {ws.cell(row=r, column=1).value: ws.cell(row=r, column=2).value for r in range(1, 40)}
    ok("PF6 hosting and inference sit under R&D", labels.get("Cloud hosting and model inference") == "R&D")
    ok("PF6 support specialists sit under S&M", labels.get("Customer support specialists") == "S&M")
    ok("PF6 deck slide 5 shows 80% gross margin", "80%" in pdf_pages("01_overview/pitch_deck.pdf")[4] and claims()["Gross margin"][0] == "80%")
    ok("PF6 gap between shown and true is material", f["shown"]["value"] - f["true"]["value"] > 0.15)
    # P&L ties to the ledger for the last actual month
    col = 2 + 20 + 1
    tel_row = next(r for r in range(1, 40) if ws.cell(row=r, column=1).value == "Telephony")
    ok("P&L telephony for 2026-09 ties to the ledger", near(ws.cell(row=tel_row, column=col).value, led["telephony"], 0.005))


def check_pf7():
    f = flag("PF7")
    rows = read_csv("03_metrics/monthly_metrics.csv")
    cum = [int(r["accounts_created_cumulative"]) for r in rows]
    paying = [int(r["paying_accounts"]) for r in rows]
    ok("PF7 accounts_created_cumulative never decreases", all(b >= a for a, b in zip(cum, cum[1:])))
    ok("PF7 the deck number is not the paying count", num(claims()["Clinics on Hollis"][0]) != paying[-1])
    ok("PF7 the cumulative column's name says cumulative", "cumulative" in "accounts_created_cumulative" and cum[-1] > paying[-1])
    ok("PF7 deck clinic count equals the last cumulative value", num(claims()["Clinics on Hollis"][0]) == cum[-1] == f["shown"]["value"])
    ok("PF7 paying accounts now match the key", paying[-1] == f["true"]["value"])
    ok("PF7 the two differ", cum[-1] != paying[-1])
    sub = {r["customer_id"] for r in cust_rows() if r["month"] == "2026-09" and r["product_type"] == "Subscription"}
    ok("PF7 customer file agrees on paying accounts", len(sub) == paying[-1])


def check_decoys():
    wb = workbook("02_financials/financial_model.xlsx")
    ws = wb["ARR_Build"]
    row = next(r for r in range(1, 40) if ws.cell(row=r, column=1).value == "Onboarding fees (one-time, excluded)")
    ok("DC1 onboarding fees row adds nothing to ARR", ws.cell(row=row, column=5).value == 0)
    fees = [r for r in cust_rows() if r["product_type"] == "Onboarding"]
    ok("DC1 onboarding rows carry fees and no MRR", fees and all(int(r["mrr"]) == 0 and int(r["one_time_fee"]) == 500 for r in fees))
    ok("DC1 the Subscription ARR rebuild is unaffected by onboarding rows",
       12 * sum(int(r["mrr"]) for r in cust_rows() if r["month"] == "2026-09" and r["product_type"] == "Subscription") == flag("PF1")["true"]["value"])

    loc = next(l for l in KEY["decoys"][1]["locations"] if "customer_name" in l)
    months = [r for r in cust_rows() if r["customer_name"] == loc["customer_name"] and r["product_type"] == "Subscription"]
    idx = sorted(month_index(r["month"]) for r in months)
    ok("DC2 Brookline Row has an unbroken run of Subscription months at one price, through 2026-09",
       idx and idx[-1] == 20 and idx == list(range(idx[0], 21)) and len({r["mrr"] for r in months}) == 1)
    t = squash("\n".join(pdf_pages("04_customers/order_form_brookline_row.pdf")))
    ok("DC2 order form is an annual prepay worth 12 months of the monthly price", "$7,788" in t and "once, in advance" in t and int(months[0]["mrr"]) * 12 == 7788)
    ok("DC2 order form is a 12-month term with no pilot or exit-at-will clause", "12 months" in t and "pilot" not in t.lower() and "any reason" not in t)

    cap = workbook("02_financials/cap_table.xlsx")["Cap_Table"]
    shares = [cap.cell(row=r, column=3).value for r in range(5, 12)]
    total = cap.cell(row=12, column=3).value
    ok("DC3 cap table holders add to the total", sum(shares) == total)
    ok("DC3 holder percentages add to 100.00 percent", near(sum(cap.cell(row=r, column=4).value for r in range(5, 12)), 1.0, 1e-9))
    ok("DC3 pro forma percentages add to 100.00 percent", near(sum(cap.cell(row=r, column=6).value for r in range(5, 12)), 1.0, 1e-9))
    price = 12_000_000 / total
    s1, s2 = cap.cell(row=16, column=6).value, cap.cell(row=17, column=6).value
    ok("DC3 SAFE shares equal amount over the cap price", near(s1, 1_200_000 / price, 0.5) and near(s2, 800_000 / price, 0.5))
    ok("DC3 SAFEs own 2M over 12M of the company", near((s1 + s2) / total, 2_000_000 / 12_000_000, 1e-9))
    ok("DC3 the Series A is 9M of 54M post-money", near(cap.cell(row=26, column=2).value, 9_000_000 / 54_000_000, 1e-9))


def check_key_shape():
    ok("answer key has 8 flags and 3 decoys", len(KEY["flags"]) == 8 and len(KEY["decoys"]) == 3)
    ok("every flag names a file location, a shown value, a true value and a check",
       all(f["locations"] and "value" in f["shown"] and "value" in f["true"] and f["check"] for f in KEY["flags"]))
    seed = {f["id"] for f in KEY["flags"] if f["catchable_from_seed_drop"]}
    ok("five flags are catchable from the seed drop", seed == {"PF2", "PF2b", "PF4", "PF6", "PF7"})
    ok("every file a seed-drop flag needs is in the seed drop",
       all(x in KEY["seed_drop_files"] for f in KEY["flags"] if f["catchable_from_seed_drop"] for x in f["files_needed"]))
    ok("flags needing the full room name a file outside the seed drop",
       all(any(x not in KEY["seed_drop_files"] for x in f["files_needed"]) for f in KEY["flags"] if not f["catchable_from_seed_drop"]))


def main():
    check_files()
    check_formulas_have_values()
    check_locations()
    check_claims_page()
    check_pf1(); check_pf2(); check_pf2b(); check_pf3(); check_pf4(); check_pf5(); check_pf6(); check_pf7()
    check_decoys()
    check_key_shape()
    print(f"\n{len(PASSES)} passed, {len(FAILS)} failed")
    if FAILS:
        print("FAILED: " + "; ".join(FAILS))
        sys.exit(1)
    print("All planted flags and decoys are in the room exactly as the answer key says.")


if __name__ == "__main__":
    main()
