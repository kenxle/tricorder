#!/usr/bin/env python3
"""Generate the synthetic Hollis Voice data room for the Tricorder demo.

Everything here is invented. Hollis Voice, its people, its clinics and its numbers are fictional.

Run with the room's own virtual environment:

    data_room/.venv/bin/python data_room/generate.py

It is rerunnable. The seed is fixed, so the CSV, PDF and Markdown files come out byte for byte the
same each time, and the workbooks hold the same cell values. Files are overwritten in place. The
script never deletes anything.

Outputs:
    data_room/hollis_voice/            the full Series A room (16 files, six folders)
    data_room/hollis_voice_seed_drop/  copies of the 11 files of the thin first tier
    data_room/answer_key.json          every planted flag and decoy, with locations and numbers

The numbers come from the research's seeded simulation (docs/reports/20261022.02_research/
data_room_design_numbers.py). The simulation below is copied from it unchanged, so the room
matches the research. The script stops with an error if a key number drifts from the research.
"""
import calendar
import csv
import datetime
import io
import json
import math
import random
import shutil
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import xlsxwriter  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import letter  # noqa: E402
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # noqa: E402
from reportlab.lib.units import inch  # noqa: E402
from reportlab.lib.utils import ImageReader, simpleSplit  # noqa: E402
from reportlab.pdfgen import canvas as rl_canvas  # noqa: E402
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOM = HERE / "hollis_voice"
SEED_DROP = HERE / "hollis_voice_seed_drop"
KEY_PATH = HERE / "answer_key.json"

FOOTER = "Synthetic data room for Deal Flow NYC 2026. Not a real company."

# ---------------------------------------------------------------------------------------------
# The simulation, copied from the research's data_room_design_numbers.py
# ---------------------------------------------------------------------------------------------
SEED = 20261024
N_MONTHS = 21  # 2025-01 .. 2026-09
PLAN_PRICE = {"Starter": 349, "Standard": 649, "Pro": 1099}
PLAN_ORDER = ["Starter", "Standard", "Pro"]
PRICE_PLAN = {v: k for k, v in PLAN_PRICE.items()}


def mlabel(i):
    """Month label for month index i (0 is 2025-01). Works past the end of the history."""
    return f"{2025 + (i // 12)}-{(i % 12) + 1:02d}"


MONTH_LABELS = [mlabel(m) for m in range(N_MONTHS)]


def churn_p(tenure):
    if tenure <= 2:
        return 0.09
    if tenure <= 12:
        return 0.012
    return 0.01


UPGRADE_P = 0.04
ONBOARDING_FEE = 500

BIG = {"name": "Cedar & Pine Animal Hospitals", "start": 10, "mrr_start": 18000,
       "expand_at": 15, "mrr_after": 36000}
PILOT = {"name": "Marlow Veterinary Group", "monthly_fee": 15000, "months": 6,
         "start": 19, "termination_days": 30}


def simulate(rng):
    customers = []
    cid = 0
    for m in range(N_MONTHS):
        n_new = max(2, round(5 + 0.7 * m + rng.uniform(-1.5, 1.5)))
        for _ in range(n_new):
            cid += 1
            plan = rng.choices(PLAN_ORDER, weights=[45, 40, 15])[0]
            customers.append({"id": f"C{cid:04d}", "start": m, "plan": plan, "mrr": [0] * N_MONTHS,
                              "churn": None, "kind": "standard", "first_plan": plan})
    for c in customers:
        plan = c["plan"]
        for m in range(c["start"], N_MONTHS):
            tenure = m - c["start"] + 1
            if m > c["start"]:
                if rng.random() < churn_p(tenure):
                    c["churn"] = m
                    break
                if rng.random() < UPGRADE_P and PLAN_ORDER.index(plan) < 2:
                    plan = PLAN_ORDER[PLAN_ORDER.index(plan) + 1]
            c["mrr"][m] = PLAN_PRICE[plan]
        c["plan"] = plan
    big = {"id": "C-BIG", "start": BIG["start"], "plan": "Group", "mrr": [0] * N_MONTHS,
           "churn": None, "kind": "big", "first_plan": "Group"}
    for m in range(BIG["start"], N_MONTHS):
        big["mrr"][m] = BIG["mrr_start"] if m < BIG["expand_at"] else BIG["mrr_after"]
    customers.append(big)
    return customers


# Forward plan settings (the same constants the research used)
LAST = N_MONTHS - 1
CASH_START = 1_800_000
SERIES_A = 9_000_000
SERIES_A_MONTH = 3          # month 3 of the plan is 2026-12; the money lands in month 4 (2027-01)
SERIES_A_PRE = 45_000_000
SAFE_AMOUNT = 2_000_000
SAFE_CAP = 12_000_000
HEADCOUNT_NOW = 17
BASE_NOW = 140_000
LOAD = 1.28
TELEPHONY_PCT, LICENCES_PCT, INFRA_PCT = 0.15, 0.05, 0.11
RENT_ETC = 60_000
PROGRAMS = 140_000
GROWTH = 0.035
HIRE_BASE = 165_000
PLANNED_HIRES = 24
MODELED_HIRES = 8
TRIAL_CONVERSION = 0.70

# Current staff by department: head count and average base pay. Sums to 17 people at 140,000.
DEPTS_NOW = OrderedDict([
    ("rd", (7, 155_000)),     # engineering and product
    ("sm", (6, 135_000)),     # sales, marketing, implementation (support is shown on its own row)
    ("sup", (2, 95_000)),     # customer support specialists
    ("ga", (2, 147_500)),     # general and administrative
])

# The 24-hire plan. Two hires start each month from 2026-10. Each pair's base pay sums to 330,000,
# which keeps the research's average of 165,000 a hire, so the research's runway numbers hold.
# (role, department, base pay). Department keys: rd, sm, sup, ga.
HIRES = [
    ("Senior Voice Engineer", "Engineering", "rd", 190_000), ("Customer Success Manager", "Customer Success", "sm", 140_000),
    ("Machine Learning Engineer", "Engineering", "rd", 185_000), ("Account Executive", "Sales", "sm", 145_000),
    ("Backend Engineer", "Engineering", "rd", 175_000), ("Implementation Specialist", "Customer Success", "sm", 155_000),
    ("Head of Sales", "Sales", "sm", 215_000), ("Support Specialist", "Support", "sup", 115_000),
    ("Data Engineer", "Engineering", "rd", 180_000), ("Marketing Manager", "Marketing", "sm", 150_000),
    ("Security Engineer", "Engineering", "rd", 195_000), ("Support Specialist", "Support", "sup", 135_000),
    ("Frontend Engineer", "Engineering", "rd", 170_000), ("Account Executive", "Sales", "sm", 160_000),
    ("Engineering Manager", "Engineering", "rd", 205_000), ("Implementation Specialist", "Customer Success", "sm", 125_000),
    ("Machine Learning Engineer", "Engineering", "rd", 190_000), ("Finance Manager", "G&A", "ga", 140_000),
    ("QA Engineer", "Engineering", "rd", 150_000), ("Account Executive", "Sales", "sm", 180_000),
    ("Solutions Engineer", "Sales", "sm", 180_000), ("Support Lead", "Support", "sup", 150_000),
    ("Product Manager", "Engineering", "rd", 185_000), ("Recruiter", "G&A", "ga", 145_000),
]

# The numbers the research prints. generate.py stops if a computed value drifts from these.
RESEARCH = {
    "customers_ever": 250, "paying_now": 212, "mrr_true": 171739, "arr_true": 2060868,
    "arr_model": 2240868, "arr_deck": 2500000, "arr_video": 3000000, "big_share": 0.21, "top3": 0.222,
    "gm_shown": 0.8, "gm_true": 0.581, "nrr_true": 0.873, "grr_true": 0.734, "nrr_reported": 1.026,
    "cohort_true": 68, "cohort_reported": 57, "accounts_cum": 357, "runway_shown": 37, "runway_true": 19,
    "burn_shown": 374462, "burn_true": 480062,
}


def forecast(hires, n_months=60):
    """The forward cash plan. `hires` is a list of (start_t, dept_key, base_pay). Follows the research."""
    rec_now = F["rec_now"]
    dept = {k: n * base * LOAD / 12 for k, (n, base) in DEPTS_NOW.items()}
    hosting = INFRA_PCT * rec_now
    cash = CASH_START
    rev = rec_now
    rows = []
    runway = None
    for t in range(1, n_months + 1):
        for (st, dk, base) in hires:
            if st == t:
                dept[dk] += base * LOAD / 12
        rev *= (1 + GROWTH)
        tel, lic = rev * TELEPHONY_PCT, rev * LICENCES_PCT
        cogs = tel + lic
        program = PROGRAMS if t > SERIES_A_MONTH else 0
        payroll = sum(dept.values())
        burn = payroll + hosting + RENT_ETC + program + cogs - rev
        raised = 0
        if t == SERIES_A_MONTH + 1:
            raised = SERIES_A
            cash += SERIES_A
        cash -= burn
        rows.append({"t": t, "label": mlabel(N_MONTHS - 1 + t), "rev": rev, "tel": tel, "lic": lic, "cogs": cogs,
                     "dept": dict(dept), "payroll": payroll, "hosting": hosting, "rent": RENT_ETC,
                     "program": program, "burn": burn, "raised": raised, "cash": cash,
                     "heads": HEADCOUNT_NOW + sum(1 for h in hires if h[0] <= t)})
        if cash <= 0 and runway is None:
            runway = t - 1
    if runway is None:
        runway = n_months
    return rows, runway


F = {}   # all facts, filled by build_facts()


# ---------------------------------------------------------------------------------------------
# Names. Word lists only; nothing here is a real clinic or person.
# ---------------------------------------------------------------------------------------------
CLINIC_A = ["Alder", "Briar", "Cypress", "Dunmore", "Elmhurst", "Fairmont", "Garnet", "Hawthorn", "Ivywood",
            "Juniper", "Kestrel", "Larkfield", "Marigold", "Northgate", "Oakhaven", "Pinecrest", "Quarry",
            "Ridgeway", "Silverbrook", "Thistle", "Underhill", "Vesper", "Wrenfield", "Yarrow", "Zephyr",
            "Amberley", "Birchwood", "Cobble", "Driftwood", "Foxglove"]
CLINIC_B = ["Court", "Lane", "Park", "Hill", "Crossing", "Square", "Green", "Point", "Landing", "Gate",
            "Hollow", "Terrace", "Commons", "Mill", "Bridge", "Meadow", "Harbor", "Corner", "Heights", "Walk"]
CLINIC_S = ["Animal Hospital", "Veterinary Clinic", "Pet Care", "Veterinary Group", "Animal Clinic",
            "Veterinary Hospital"]
BROOKLINE = "Brookline Row Veterinary"

CEO = {"name": "Imogen Tarrant", "title": "Chief Executive Officer and co-founder"}
CTO = {"name": "Teodoro Brandt", "title": "Chief Technology Officer and co-founder"}
FOUNDER_GITHUB = {CEO["name"]: "hollis-voice-demo", CTO["name"]: "hollis-voice-demo"}   # placeholder handles; swap for the demo organisation's
SENIOR = [
    ("Marguerite Dunleavy", "Head of Sales"),
    ("Anselm Okoye-Ruiz", "Head of Customer Success"),
    ("Hallie Vandermeer", "Controller (part time)"),
    ("Lucan Faraday-Moss", "Lead Voice Engineer"),
]
SAFE_A_NAME = "Tidewater Seed Fund I, LP"
SAFE_B_NAME = "Anselm Hartley (angel)"
SERIES_A_LEAD = "Series A investors (new)"

# Registry of planted locations for the answer key.
LOC = defaultdict(list)


def money(n):
    return f"${n:,.0f}"


def pct(x, d=1):
    return f"{x * 100:.{d}f}%"


# ---------------------------------------------------------------------------------------------
# Facts
# ---------------------------------------------------------------------------------------------
def build_facts():
    rng = random.Random(SEED)
    customers = simulate(rng)
    namer = random.Random(SEED + 1)
    F["customers"] = customers

    mrr_total = [sum(c["mrr"][m] for c in customers) for m in range(N_MONTHS)]
    paying = [sum(1 for c in customers if c["mrr"][m] > 0) for m in range(N_MONTHS)]
    ever = len(customers)
    true_mrr = mrr_total[LAST]
    true_arr = 12 * true_mrr
    pilot_arr = 12 * PILOT["monthly_fee"]
    model_arr = true_arr + pilot_arr
    deck_arr = math.ceil(model_arr * 1.10 / 100_000) * 100_000
    video_arr = math.ceil((deck_arr + 250_000) / 500_000) * 500_000
    F.update(mrr_total=mrr_total, paying=paying, ever=ever, true_mrr=true_mrr, true_arr=true_arr,
             pilot_arr=pilot_arr, model_arr=model_arr, deck_arr=deck_arr, video_arr=video_arr)

    # Pilot months: the pilot pays from PILOT start to the end of the history
    pilot_mrr = [PILOT["monthly_fee"] if m >= PILOT["start"] else 0 for m in range(N_MONTHS)]
    rec = [mrr_total[m] + pilot_mrr[m] for m in range(N_MONTHS)]    # recurring revenue as the books show it
    F["pilot_mrr"], F["rec"] = pilot_mrr, rec
    F["rec_now"] = rec[LAST]

    # Concentration
    mrrs = sorted((c["mrr"][LAST] for c in customers if c["mrr"][LAST] > 0), reverse=True)
    F["big_share"] = BIG["mrr_after"] / true_mrr
    F["top3"] = sum(mrrs[:3]) / true_mrr
    F["claimed_share"] = 0.09

    # Vanity metric
    cum_ever = [sum(1 for c in customers if c["start"] <= m) for m in range(N_MONTHS)]
    F["cum_created"] = [round(x / TRIAL_CONVERSION) for x in cum_ever]
    F["accounts_cum"] = F["cum_created"][LAST]

    # Cohorts
    rows = []
    for start in range(0, LAST - 11):
        cohort = [c for c in customers if c["start"] == start and c["kind"] == "standard"]
        end_m = start + 12
        start_mrr = sum(c["mrr"][start] for c in cohort)
        end_mrr = sum(c["mrr"][end_m] for c in cohort)
        capped = sum(min(c["mrr"][end_m], c["mrr"][start]) for c in cohort)
        early = [c for c in cohort if c["churn"] is not None and c["churn"] - c["start"] <= 2]
        kept = [c for c in cohort if c not in early]
        kept_start = sum(c["mrr"][start] for c in kept)
        kept_end = sum(c["mrr"][end_m] for c in kept)
        curve = [sum(c["mrr"][start + k] for c in kept) / kept_start for k in range(13)]
        rows.append({"cohort": MONTH_LABELS[start], "customers": len(cohort), "early": len(early),
                     "start_mrr": start_mrr, "end_mrr": end_mrr, "capped_end": capped,
                     "rep_customers": len(kept), "rep_start": kept_start, "rep_end": kept_end, "curve": curve})
    ts = sum(r["start_mrr"] for r in rows)
    F["cohorts"] = rows
    F["nrr_true"] = sum(r["end_mrr"] for r in rows) / ts
    F["grr_true"] = sum(r["capped_end"] for r in rows) / ts
    F["nrr_rep"] = sum(r["rep_end"] for r in rows) / sum(r["rep_start"] for r in rows)
    F["cohort_true"] = sum(r["customers"] for r in rows)
    F["cohort_rep"] = sum(r["rep_customers"] for r in rows)

    # Customer names
    combos = [(a, b, s) for a in CLINIC_A for b in CLINIC_B for s in CLINIC_S]
    namer.shuffle(combos)
    standard = [c for c in customers if c["kind"] == "standard"]
    names = {}
    for c, (a, b, s) in zip(standard, combos):
        names[c["id"]] = f"{a} {b} {s}"
    names["C-BIG"] = BIG["name"]
    # Brookline Row: an ordinary customer on the Standard plan, active now, with a first annual term in force
    pool = [c for c in standard if c["churn"] is None and c["first_plan"] == "Standard" and c["plan"] == "Standard"
            and 9 <= c["start"] <= 19]
    brook = pool[namer.randrange(len(pool))]
    names[brook["id"]] = BROOKLINE
    F["names"], F["brook"] = names, brook

    # Gross margin from the ledger numbers (built in build_ledger)
    build_ledger()
    last_basis = rec[LAST]
    led = F["ledger_last"]
    cogs_shown = led["telephony"] + led["third_party_licences"]
    cogs_true = cogs_shown + led["cloud_hosting"] + led["model_inference"] + led["support_staff"]
    F["gm_shown"] = 1 - cogs_shown / last_basis
    F["gm_true"] = 1 - cogs_true / last_basis

    # Forward plan
    model_hires = [(1 + i // 2, h[2], h[3]) for i, h in enumerate(HIRES[:MODELED_HIRES])]
    all_hires = [(1 + i // 2, h[2], h[3]) for i, h in enumerate(HIRES)]
    F["model_hires"], F["all_hires"] = model_hires, all_hires
    shown_rows, shown_runway = forecast(model_hires, 60)
    true_rows, true_runway = forecast(all_hires, 60)
    F.update(fc_shown=shown_rows, runway_shown=shown_runway, fc_true=true_rows, runway_true=true_runway,
             burn_shown=sum(r["burn"] for r in shown_rows[:12]) / 12,
             burn_true=sum(r["burn"] for r in true_rows[:12]) / 12)

    drift = {
        "customers_ever": F["ever"], "paying_now": paying[LAST], "mrr_true": true_mrr, "arr_true": true_arr,
        "arr_model": model_arr, "arr_deck": deck_arr, "arr_video": video_arr,
        "big_share": round(F["big_share"], 3), "top3": round(F["top3"], 3),
        "gm_shown": round(F["gm_shown"], 3), "gm_true": round(F["gm_true"], 3),
        "nrr_true": round(F["nrr_true"], 3), "grr_true": round(F["grr_true"], 3),
        "nrr_reported": round(F["nrr_rep"], 3), "cohort_true": F["cohort_true"],
        "cohort_reported": F["cohort_rep"], "accounts_cum": F["accounts_cum"],
        "runway_shown": shown_runway, "runway_true": true_runway,
        "burn_shown": round(F["burn_shown"]), "burn_true": round(F["burn_true"]),
    }
    bad = {k: (drift[k], RESEARCH[k]) for k in RESEARCH if drift[k] != RESEARCH[k]}
    if bad:
        sys.exit(f"Numbers drifted from the research: {bad}")


# ---------------------------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------------------------
HC = [round(4 + 13 * m / 20) for m in range(N_MONTHS)]    # head count by month; 17 in the last month


def build_ledger():
    rows = []
    rec = F["rec"]
    for m in range(N_MONTHS):
        label = MONTH_LABELS[m]
        basis = rec[m]
        scale = HC[m] / HEADCOUNT_NOW
        tel = round(TELEPHONY_PCT * basis, 2)
        lic = round(LICENCES_PCT * basis, 2)
        infra = round(INFRA_PCT * basis, 2)
        host = round(0.04 * basis, 2)
        inf = round(infra - host, 2)
        rows.append((label, "Tallow Telecom", "Phone minutes and SIP trunking", "telephony", "Cost of revenue", tel))
        rows.append((label, "Marsh Speech Licensing", "Speech recognition and voice licences", "third_party_licences", "Cost of revenue", lic))
        rows.append((label, "Brindle Cloud Hosting", "Cloud compute and storage", "cloud_hosting", "R&D", host))
        rows.append((label, "Halcyon Inference API", "Language model and speech API usage", "model_inference", "R&D", inf))
        sup = round(2 * 95_000 * LOAD / 12 * scale, 2)
        rows.append((label, "Ironbridge Payroll Services", "Customer support specialists, salaries and benefits", "support_staff", "S&M", sup))
        for key, cat, booked, desc in (("rd", "payroll_engineering", "R&D", "Engineering and product, salaries and benefits"),
                                       ("sm", "payroll_sales_marketing", "S&M", "Sales, marketing and implementation, salaries and benefits"),
                                       ("ga", "payroll_g_and_a", "G&A", "General and administrative, salaries and benefits")):
            n, base = DEPTS_NOW[key]
            rows.append((label, "Ironbridge Payroll Services", desc, cat, booked, round(n * base * LOAD / 12 * scale, 2)))
        other = round(RENT_ETC * (0.4 + 0.6 * HC[m] / HEADCOUNT_NOW), 2)
        rent = round(other * 0.45, 2)
        tools = round(other * 0.25, 2)
        legal = round(other * 0.15, 2)
        rest = round(other - rent - tools - legal, 2)
        rows.append((label, "Gantry Workspace", "Office rent", "rent", "G&A", rent))
        rows.append((label, "Deskwise Software", "Software subscriptions and tools", "tools", "G&A", tools))
        rows.append((label, "Pembry Legal Services", "Legal and filing fees", "legal", "G&A", legal))
        rows.append((label, "Various", "Insurance, travel and other", "other", "G&A", rest))
    F["ledger"] = rows
    by = defaultdict(float)
    for (label, _v, _d, cat, _b, amt) in rows:
        by[(label, cat)] += amt
    F["ledger_by"] = by
    F["ledger_last"] = {cat: by[(MONTH_LABELS[LAST], cat)] for cat in
                        ("telephony", "third_party_licences", "cloud_hosting", "model_inference", "support_staff")}


def write_csv(path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    w.writerows(rows)
    path.write_bytes(buf.getvalue().encode("utf-8"))


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def build_tables():
    customers, names = F["customers"], F["names"]
    # customer_mrr_by_month.csv
    rows = []
    for m in range(N_MONTHS):
        label = MONTH_LABELS[m]
        for c in customers:
            if c["start"] == m:
                rows.append((label, c["id"], names[c["id"]], 17 if c["kind"] == "big" else 1,
                             c["first_plan"], "Onboarding", 0, ONBOARDING_FEE))
        for c in customers:
            v = c["mrr"][m]
            if v > 0:
                plan = "Group" if c["kind"] == "big" else PRICE_PLAN[v]
                rows.append((label, c["id"], names[c["id"]], 17 if c["kind"] == "big" else 1,
                             plan, "Subscription", v, 0))
        if m >= PILOT["start"]:
            rows.append((label, "P-MARLOW", PILOT["name"], 4, "Pilot", "Pilot", PILOT["monthly_fee"], 0))
    write_csv(ROOM / "03_metrics/customer_mrr_by_month.csv",
              ["month", "customer_id", "customer_name", "locations", "plan", "product_type", "mrr", "one_time_fee"], rows)
    F["cust_rows"] = rows

    # monthly_metrics.csv
    crng = random.Random(SEED + 2)
    rows = []
    calls = []
    for m in range(N_MONTHS):
        days = calendar.monthrange(2025 + m // 12, m % 12 + 1)[1]
        n_calls = round(F["paying"][m] * crng.uniform(330, 410) * days / 30)
        calls.append(n_calls)
        mrr = F["rec"][m]
        rows.append((MONTH_LABELS[m], mrr, 12 * mrr, F["paying"][m], F["cum_created"][m], n_calls))
    F["calls"] = calls
    write_csv(ROOM / "03_metrics/monthly_metrics.csv",
              ["month", "mrr", "arr", "paying_accounts", "accounts_created_cumulative", "calls_handled"], rows)

    # expense_ledger.csv
    write_csv(ROOM / "02_financials/expense_ledger.csv",
              ["month", "vendor", "description", "category", "booked_as", "amount_usd"],
              [(a, b, c, d, e, f"{amt:.2f}") for (a, b, c, d, e, amt) in F["ledger"]])

    # hiring_plan.csv
    rows = []
    for i, (role, dept, _k, base) in enumerate(HIRES):
        t = 1 + i // 2
        rows.append((f"H{i + 1:02d}", role, dept, f"{mlabel(N_MONTHS - 1 + t)}-01", base))
    write_csv(ROOM / "05_team/hiring_plan.csv", ["hire_id", "role", "department", "start_date", "base_salary_usd"], rows)
    F["hire_rows"] = rows


# ---------------------------------------------------------------------------------------------
# Workbooks
# ---------------------------------------------------------------------------------------------
def new_workbook(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    wb = xlsxwriter.Workbook(str(path))
    wb.set_properties({"title": path.stem, "author": "Hollis Voice (synthetic)", "company": "Hollis Voice (synthetic)",
                       "comments": FOOTER, "created": datetime.datetime(2026, 10, 1, 9, 0, 0)})
    return wb


def formats(wb):
    f = {}
    f["title"] = wb.add_format({"bold": True, "font_size": 14})
    f["bold"] = wb.add_format({"bold": True})
    f["head"] = wb.add_format({"bold": True, "bg_color": "#14213D", "font_color": "#FFFFFF", "align": "center"})
    f["headl"] = wb.add_format({"bold": True, "bg_color": "#14213D", "font_color": "#FFFFFF"})
    f["sect"] = wb.add_format({"bold": True, "bg_color": "#E8EEF4"})
    f["usd"] = wb.add_format({"num_format": "#,##0"})
    f["usd2"] = wb.add_format({"num_format": "#,##0.00"})
    f["usdb"] = wb.add_format({"num_format": "#,##0", "bold": True, "top": 1})
    f["pct"] = wb.add_format({"num_format": "0.0%"})
    f["pctb"] = wb.add_format({"num_format": "0.0%", "bold": True})
    f["pct2"] = wb.add_format({"num_format": "0.00%"})
    f["int"] = wb.add_format({"num_format": "#,##0"})
    f["intb"] = wb.add_format({"num_format": "#,##0", "bold": True, "top": 1})
    f["dec"] = wb.add_format({"num_format": "0.00"})
    f["wrap"] = wb.add_format({"text_wrap": True, "valign": "top"})
    f["note"] = wb.add_format({"italic": True, "font_color": "#555555"})
    f["name"] = wb.add_format({"bold": True, "bg_color": "#FFF4CC", "num_format": "#,##0"})
    f["namep"] = wb.add_format({"bold": True, "bg_color": "#FFF4CC", "num_format": "0.0%"})
    f["namet"] = wb.add_format({"bold": True, "bg_color": "#FFF4CC"})
    return f


def a1(row, col, abs_=False):
    return xlsxwriter.utility.xl_rowcol_to_cell(row, col, row_abs=abs_, col_abs=abs_)


def build_model():
    path = ROOM / "02_financials/financial_model.xlsx"
    wb = new_workbook(path)
    fm = formats(wb)
    rel = "02_financials/financial_model.xlsx"

    def reg(flag, sheet, cell, name=None, expect=None, label=None):
        entry = {"file": rel, "sheet": sheet, "cell": cell}
        if name:
            entry["named_cell"] = name
        if expect is not None:
            entry["expect"] = expect
        if label:
            entry["label"] = label
        LOC[flag].append(entry)

    ws_readme = wb.add_worksheet("README")
    ws_ass = wb.add_worksheet("Assumptions")
    ws_pl = wb.add_worksheet("P&L")
    ws_arr = wb.add_worksheet("ARR_Build")
    ws_coh = wb.add_worksheet("Cohorts")
    ws_hire = wb.add_worksheet("Hiring_Plan")
    ws_cash = wb.add_worksheet("Cash_Runway")

    # ---- README
    ws_readme.set_column(0, 0, 110)
    lines = [
        ("Hollis Voice: financial model", "title"),
        ("Data as of 2026-09-30. All figures in US dollars. Actual months 2025-01 to 2026-09. Plan months 2026-10 onward.", None),
        ("", None),
        ("Tabs", "bold"),
        ("Assumptions: the inputs the plan uses.", None),
        ("P&L: monthly income statement, 21 months of actuals and 12 months of plan.", None),
        ("ARR_Build: how annual recurring revenue (ARR) is built up at the data date.", None),
        ("Cohorts: 12-month revenue retention of customer cohorts.", None),
        ("Hiring_Plan: the hires the plan pays for.", None),
        ("Cash_Runway: monthly cash and the number of months the cash lasts.", None),
        ("", None),
        ("Definitions", "bold"),
        ("ARR: monthly recurring revenue from signed, live agreements, times 12. One-time fees are left out.", None),
        ("Gross margin: recurring revenue less cost of revenue, divided by recurring revenue.", None),
        ("Net revenue retention: revenue from a group of customers 12 months after they started, divided by what they paid in their first month.", None),
        ("Runway: the number of months after 2026-09-30 in which cash stays above zero.", None),
        ("", None),
        (FOOTER, "note"),
    ]
    for r, (txt, style) in enumerate(lines):
        ws_readme.write(r, 0, txt, fm[style] if style else None)

    # ---- Assumptions
    ws_ass.set_column(0, 0, 46)
    ws_ass.set_column(1, 1, 18)
    ws_ass.set_column(2, 2, 80)
    ws_ass.write(0, 0, "Assumptions", fm["title"])
    ws_ass.write(1, 0, "Cells with a yellow fill are named cells.", fm["note"])
    ws_ass.write_row(3, 0, ["Input", "Value", "Note"], fm["headl"])
    pr = F["fc_shown"][0]
    assum = [
        ("AS_OF_DATE", "Data date", "2026-09-30", "namet", "Last day of the last actual month."),
        ("CASH_START", "Cash at the data date (USD)", CASH_START, "name", "Bank balance at 2026-09-30."),
        ("REV_GROWTH", "Recurring revenue growth per month", GROWTH, "namep", "A flat planning rate."),
        ("LOAD_FACTOR", "Loaded cost factor on base pay", LOAD, "name", "Base pay times this factor gives payroll cost including taxes and benefits."),
        ("STAFF_NOW", "Staff at the data date", HEADCOUNT_NOW, "name", "All departments."),
        ("AVG_BASE_NOW", "Average base pay today (USD a year)", BASE_NOW, "name", "Across the 17 current staff."),
        ("TELEPHONY_PCT", "Telephony as a share of recurring revenue", TELEPHONY_PCT, "namep", "Booked in cost of revenue."),
        ("LICENCES_PCT", "Software licences as a share of recurring revenue", LICENCES_PCT, "namep", "Booked in cost of revenue."),
        ("HOSTING_USD_MONTH", "Cloud hosting and model inference (USD a month)", round(INFRA_PCT * F["rec_now"], 2), "name", "Booked under R&D. Held at the September 2026 level in the plan."),
        ("RENT_ETC_USD_MONTH", "Rent, tools, legal and other (USD a month)", RENT_ETC, "name", "Booked under G&A. Held flat."),
        ("PROGRAMS_USD_MONTH", "Marketing programs after the raise (USD a month)", PROGRAMS, "name", "Starts the month the Series A closes."),
        ("SERIES_A_RAISE", "Series A raise (USD)", SERIES_A, "name", "Lands in plan month 4 (2027-01)."),
        ("SERIES_A_PLAN_MONTH", "Plan month the Series A cash arrives", SERIES_A_MONTH + 1, "name", "Plan month 1 is 2026-10."),
        ("REV_START_USD_MONTH", "Recurring revenue in the last actual month (USD)", F["rec_now"], "name", "From P&L, 2026-09."),
    ]
    ASS_CELL = {}
    for i, (nm, label, val, fmt, note) in enumerate(assum):
        r = 4 + i
        ws_ass.write(r, 0, label)
        ws_ass.write(r, 1, val, fm[fmt])
        ws_ass.write(r, 2, note, fm["note"])
        wb.define_name(nm, f"=Assumptions!$B${r + 1}")
        ASS_CELL[nm] = f"B{r + 1}"
    r = 4 + len(assum)
    ws_ass.write(r, 0, "Payroll today (USD a month)")
    pay_now = HEADCOUNT_NOW * BASE_NOW * LOAD / 12
    ws_ass.write_formula(r, 1, "=STAFF_NOW*AVG_BASE_NOW*LOAD_FACTOR/12", fm["name"], pay_now)
    ws_ass.write(r, 2, "Staff times average base pay times the loaded factor, divided by 12.", fm["note"])
    wb.define_name("PAYROLL_NOW_USD_MONTH", f"=Assumptions!$B${r + 1}")
    ws_ass.write(r + 2, 0, FOOTER, fm["note"])

    # ---- P&L
    ws_pl.set_column(0, 0, 44)
    ws_pl.set_column(1, 1, 9)
    ws_pl.set_column(2, 2 + N_MONTHS + 12, 11)
    ws_pl.freeze_panes(5, 2)
    ws_pl.write(0, 0, "Hollis Voice: income statement and 12-month plan (USD)", fm["title"])
    ws_pl.write(1, 0, "Actual through 2026-09. Plan from 2026-10. Gross margin is on recurring revenue (subscription plus pilot).", fm["note"])
    ws_pl.write(3, 0, "Line", fm["headl"])
    ws_pl.write(3, 1, "Section", fm["headl"])
    ws_pl.write(4, 0, "", fm["headl"])
    ws_pl.write(4, 1, "", fm["headl"])
    n_cols = N_MONTHS + 12
    for j in range(n_cols):
        lab = mlabel(j)
        ws_pl.write(3, 2 + j, lab, fm["head"])
        ws_pl.write(4, 2 + j, "Actual" if j < N_MONTHS else "Plan", fm["head"])

    R = {}
    layout = [
        ("sec_rev", "Revenue", "", "sect"),
        ("sub", "Subscription revenue", "Revenue", None),
        ("pilot", "Pilot revenue", "Revenue", None),
        ("onb", "Onboarding fees (one-time)", "Revenue", None),
        ("rec", "Recurring revenue (subscription plus pilot)", "Revenue", None),
        ("tot", "Total revenue", "Revenue", None),
        ("sec_cogs", "Cost of revenue", "", "sect"),
        ("tel", "Telephony", "COGS", None),
        ("lic", "Third-party software licences", "COGS", None),
        ("cogs", "Total cost of revenue", "COGS", None),
        ("gp", "Gross profit (recurring revenue less cost of revenue)", "", None),
        ("gm", "Gross margin", "", None),
        ("sec_opex", "Operating expenses", "", "sect"),
        ("p_rd", "Payroll: engineering and product", "R&D", None),
        ("host", "Cloud hosting and model inference", "R&D", None),
        ("p_sm", "Payroll: sales, marketing and implementation", "S&M", None),
        ("sup", "Customer support specialists", "S&M", None),
        ("prog", "Marketing programs", "S&M", None),
        ("p_ga", "Payroll: general and administrative", "G&A", None),
        ("rent", "Rent, tools, legal and other", "G&A", None),
        ("opex", "Total operating expenses", "", None),
        ("op", "Operating result (gross profit plus onboarding fees less operating expenses)", "", None),
        ("sec_memo", "Memo", "", "sect"),
        ("payroll", "Payroll", "Memo", None),
        ("burn", "Net burn (negative of operating result)", "Memo", None),
        ("heads", "Staff at month end", "Memo", None),
    ]
    row0 = 5
    for i, (key, label, sec, style) in enumerate(layout):
        R[key] = row0 + i
        ws_pl.write(R[key], 0, label, fm[style] if style else None)
        ws_pl.write(R[key], 1, sec, fm[style] if style else None)
        if style == "sect":
            for j in range(n_cols):
                ws_pl.write(R[key], 2 + j, "", fm["sect"])

    led = F["ledger_by"]
    fc = F["fc_shown"]
    # Build monthly values
    V = {}   # (key, j) -> value

    def put(key, j, val):
        V[(key, j)] = val

    for j in range(n_cols):
        if j < N_MONTHS:
            label = MONTH_LABELS[j]
            sub = F["mrr_total"][j]
            pilot = F["pilot_mrr"][j]
            onb = ONBOARDING_FEE * sum(1 for c in F["customers"] if c["start"] == j)
            put("sub", j, sub); put("pilot", j, pilot); put("onb", j, onb)
            put("tel", j, led[(label, "telephony")]); put("lic", j, led[(label, "third_party_licences")])
            put("p_rd", j, led[(label, "payroll_engineering")]); put("host", j, round(led[(label, "cloud_hosting")] + led[(label, "model_inference")], 2))
            put("p_sm", j, led[(label, "payroll_sales_marketing")]); put("sup", j, led[(label, "support_staff")])
            put("prog", j, 0)
            put("p_ga", j, led[(label, "payroll_g_and_a")])
            put("rent", j, round(sum(led[(label, c)] for c in ("rent", "tools", "legal", "other")), 2))
            put("heads", j, HC[j])
        else:
            r_ = fc[j - N_MONTHS]
            put("rec", j, r_["rev"])
            put("onb", j, 0)
            put("tel", j, r_["tel"]); put("lic", j, r_["lic"])
            put("p_rd", j, r_["dept"]["rd"]); put("host", j, r_["hosting"])
            put("p_sm", j, r_["dept"]["sm"]); put("sup", j, r_["dept"]["sup"]); put("prog", j, r_["program"])
            put("p_ga", j, r_["dept"]["ga"]); put("rent", j, r_["rent"])
            put("heads", j, r_["heads"])

    for j in range(n_cols):
        c = 2 + j
        col = lambda key: a1(R[key], c)
        actual = j < N_MONTHS
        for key in ("onb", "tel", "lic", "p_rd", "host", "p_sm", "sup", "prog", "p_ga", "rent"):
            ws_pl.write_number(R[key], c, V[(key, j)], fm["usd"])
        ws_pl.write_number(R["heads"], c, V[("heads", j)], fm["int"])
        if actual:
            ws_pl.write_number(R["sub"], c, V[("sub", j)], fm["usd"])
            ws_pl.write_number(R["pilot"], c, V[("pilot", j)], fm["usd"])
            rec = V[("sub", j)] + V[("pilot", j)]
            ws_pl.write_formula(R["rec"], c, f"={col('sub')}+{col('pilot')}", fm["usd"], rec)
        else:
            rec = V[("rec", j)]
            ws_pl.write_number(R["rec"], c, rec, fm["usd"])
        put("rec", j, rec)
        tot = rec + V[("onb", j)]
        ws_pl.write_formula(R["tot"], c, f"={col('rec')}+{col('onb')}", fm["usd"], tot)
        cogs = V[("tel", j)] + V[("lic", j)]
        ws_pl.write_formula(R["cogs"], c, f"={col('tel')}+{col('lic')}", fm["usd"], cogs)
        gp = rec - cogs
        ws_pl.write_formula(R["gp"], c, f"={col('rec')}-{col('cogs')}", fm["usdb"], gp)
        gm = gp / rec
        ws_pl.write_formula(R["gm"], c, f"={col('gp')}/{col('rec')}", fm["pct"], gm)
        opex = sum(V[(k, j)] for k in ("p_rd", "host", "p_sm", "sup", "prog", "p_ga", "rent"))
        ws_pl.write_formula(R["opex"], c, f"={col('p_rd')}+{col('host')}+{col('p_sm')}+{col('sup')}+{col('prog')}+{col('p_ga')}+{col('rent')}",
                            fm["usdb"], opex)
        op = gp + V[("onb", j)] - opex
        ws_pl.write_formula(R["op"], c, f"={col('gp')}+{col('onb')}-{col('opex')}", fm["usdb"], op)
        payroll = V[("p_rd", j)] + V[("p_sm", j)] + V[("sup", j)] + V[("p_ga", j)]
        ws_pl.write_formula(R["payroll"], c, f"={col('p_rd')}+{col('p_sm')}+{col('sup')}+{col('p_ga')}", fm["usd"], payroll)
        ws_pl.write_formula(R["burn"], c, f"=-{col('op')}", fm["usd"], -op)
        put("gm", j, gm); put("payroll", j, payroll); put("burn", j, -op); put("gp", j, gp)
    last_c = 2 + LAST
    wb.define_name("GM_PCT", f"='P&L'!${xlsxwriter.utility.xl_col_to_name(last_c)}${R['gm'] + 1}")
    reg("PF6", "P&L", a1(R["gm"], last_c), name="GM_PCT", expect=V[("gm", LAST)], label="Gross margin, 2026-09")
    reg("PF6", "P&L", a1(R["host"], 0), expect="Cloud hosting and model inference", label="row label, booked under R&D")
    reg("PF6", "P&L", a1(R["sup"], 0), expect="Customer support specialists", label="row label, booked under S&M")
    reg("PF4", "P&L", a1(R["payroll"], 0), expect="Payroll", label="plan row Payroll")
    reg("PF4", "P&L", f"{a1(R['payroll'], N_MONTHS + 2)}:{a1(R['payroll'], n_cols + 1)}", label="Payroll, plan months 2026-10 to 2027-09")
    ws_pl.write(R["heads"] + 2, 0, FOOTER, fm["note"])
    F["pl_rows"] = R

    # ---- ARR_Build
    ws_arr.set_column(0, 0, 52)
    ws_arr.set_column(1, 1, 14)
    ws_arr.set_column(2, 4, 16)
    ws_arr.set_column(5, 5, 90)
    ws_arr.write(0, 0, "ARR build at 2026-09-30 (USD)", fm["title"])
    ws_arr.write(1, 0, "ARR is monthly recurring revenue from signed, live agreements times 12. One-time fees are left out.", fm["note"])
    ws_arr.write_row(3, 0, ["Line", "Product type", "Customers", "MRR", "ARR counted", "Note"], fm["headl"])
    quarters = [(0, 2), (3, 5), (6, 8), (9, 11), (12, 14), (15, 17), (18, 20)]
    r = 4
    first = r
    arr_rows = []
    for (a, b) in quarters:
        grp = [c for c in F["customers"] if a <= c["start"] <= b and c["mrr"][LAST] > 0]
        mrr = sum(c["mrr"][LAST] for c in grp)
        yq = f"{2025 + a // 12} Q{(a % 12) // 3 + 1}"
        ws_arr.write(r, 0, f"Subscriptions signed {yq}")
        ws_arr.write(r, 1, "Subscription")
        ws_arr.write_number(r, 2, len(grp), fm["int"])
        ws_arr.write_number(r, 3, mrr, fm["usd"])
        ws_arr.write_formula(r, 4, f"=D{r + 1}*12", fm["usd"], mrr * 12)
        ws_arr.write(r, 5, "Monthly plans and annual plans paid up front; revenue is spread over the term.", fm["note"])
        arr_rows.append((len(grp), mrr))
        r += 1
    last_q = r - 1
    sub_cnt = sum(x[0] for x in arr_rows)
    sub_mrr = sum(x[1] for x in arr_rows)
    ws_arr.write(r, 0, "Subscription ARR", fm["bold"])
    ws_arr.write(r, 1, "Subscription")
    ws_arr.write_formula(r, 2, f"=SUM(C{first + 1}:C{last_q + 1})", fm["intb"], sub_cnt)
    ws_arr.write_formula(r, 3, f"=SUM(D{first + 1}:D{last_q + 1})", fm["usdb"], sub_mrr)
    ws_arr.write_formula(r, 4, f"=SUM(E{first + 1}:E{last_q + 1})", fm["usdb"], sub_mrr * 12)
    sub_row = r
    r += 1
    ws_arr.write(r, 0, "Marlow Veterinary Group (pilot)")
    ws_arr.write(r, 1, "Pilot")
    ws_arr.write_number(r, 2, 1, fm["int"])
    ws_arr.write_number(r, 3, PILOT["monthly_fee"], fm["usd"])
    ws_arr.write_formula(r, 4, f"=D{r + 1}*12", fm["usd"], PILOT["monthly_fee"] * 12)
    ws_arr.write(r, 5, "Six-month pilot signed 2026-08-01. Counted at $15,000 a month times 12.", fm["note"])
    pilot_row = r
    r += 1
    n_new = sum(1 for c in F["customers"] if c["start"] == LAST)
    ws_arr.write(r, 0, "Onboarding fees (one-time, excluded)")
    ws_arr.write(r, 1, "Onboarding")
    ws_arr.write_number(r, 2, n_new, fm["int"])
    ws_arr.write_number(r, 3, 0, fm["usd"])
    ws_arr.write_number(r, 4, 0, fm["usd"])
    ws_arr.write(r, 5, f"$500 per new clinic. September 2026: {n_new} new clinics, ${ONBOARDING_FEE * n_new:,} in fees. One-time, so not counted in ARR.", fm["note"])
    onb_row = r
    r += 1
    ws_arr.write(r, 0, "ARR total", fm["bold"])
    ws_arr.write_formula(r, 4, f"=E{sub_row + 1}+E{pilot_row + 1}+E{onb_row + 1}", fm["name"], F["model_arr"])
    wb.define_name("ARR_TOTAL", f"=ARR_Build!$E${r + 1}")
    arr_total_row = r
    reg("PF1", "ARR_Build", a1(r, 4), name="ARR_TOTAL", expect=F["model_arr"], label="model ARR total")
    reg("PF1", "ARR_Build", a1(pilot_row, 0), expect="Marlow Veterinary Group (pilot)", label="pilot row label")
    reg("PF1", "ARR_Build", a1(pilot_row, 4), expect=F["pilot_arr"], label="pilot counted as ARR")
    reg("PF2", "ARR_Build", a1(r, 4), name="ARR_TOTAL", expect=F["model_arr"], label="model ARR total")
    LOC["DC1"].append({"file": rel, "sheet": "ARR_Build", "cell": a1(onb_row, 0), "expect": "Onboarding fees (one-time, excluded)",
                       "label": "onboarding row, correctly excluded"})
    LOC["DC1"].append({"file": rel, "sheet": "ARR_Build", "cell": a1(onb_row, 4), "expect": 0, "label": "ARR counted for the fee"})
    r += 2
    ws_arr.write(r, 0, "Monthly history", fm["bold"])
    r += 1
    ws_arr.write_row(r, 0, ["Month", "", "Subscription MRR", "Pilot MRR", "ARR (total MRR times 12)"], fm["headl"])
    r += 1
    for m in range(N_MONTHS):
        ws_arr.write(r, 0, MONTH_LABELS[m])
        ws_arr.write_number(r, 2, F["mrr_total"][m], fm["usd"])
        ws_arr.write_number(r, 3, F["pilot_mrr"][m], fm["usd"])
        ws_arr.write_formula(r, 4, f"=(C{r + 1}+D{r + 1})*12", fm["usd"], 12 * F["rec"][m])
        r += 1
    ws_arr.write(r + 1, 0, FOOTER, fm["note"])

    # ---- Cohorts
    ws_coh.set_column(0, 0, 30)
    ws_coh.set_column(1, 4, 16)
    ws_coh.set_column(5, 17, 8)
    ws_coh.write(0, 0, "Cohorts: 12-month revenue retention", fm["title"])
    ws_coh.write(1, 0, "Cohort = customers still active after onboarding", fm["note"])
    ws_coh.write_row(3, 0, ["Cohort (first invoice month)", "Customers", "Starting MRR", "MRR after 12 months",
                            "Net revenue retention"], fm["headl"])
    for k in range(13):
        ws_coh.write(3, 5 + k, f"M{k}", fm["head"])
    r = 4
    first = r
    for row in F["cohorts"]:
        ws_coh.write(r, 0, row["cohort"])
        ws_coh.write_number(r, 1, row["rep_customers"], fm["int"])
        ws_coh.write_number(r, 2, row["rep_start"], fm["usd"])
        ws_coh.write_number(r, 3, row["rep_end"], fm["usd"])
        ws_coh.write_formula(r, 4, f"=D{r + 1}/C{r + 1}", fm["pct"], row["rep_end"] / row["rep_start"])
        for k in range(13):
            ws_coh.write_number(r, 5 + k, row["curve"][k], fm["pct"])
        r += 1
    last = r - 1
    cust_total = sum(x["rep_customers"] for x in F["cohorts"])
    s0 = sum(x["rep_start"] for x in F["cohorts"])
    s1 = sum(x["rep_end"] for x in F["cohorts"])
    ws_coh.write(r, 0, "All cohorts", fm["bold"])
    ws_coh.write_formula(r, 1, f"=SUM(B{first + 1}:B{last + 1})", fm["intb"], cust_total)
    ws_coh.write_formula(r, 2, f"=SUM(C{first + 1}:C{last + 1})", fm["usdb"], s0)
    ws_coh.write_formula(r, 3, f"=SUM(D{first + 1}:D{last + 1})", fm["usdb"], s1)
    ws_coh.write_formula(r, 4, f"=D{r + 1}/C{r + 1}", fm["namep"], s1 / s0)
    wb.define_name("NRR_12M", f"=Cohorts!$E${r + 1}")
    wb.define_name("COHORT_CUSTOMERS", f"=Cohorts!$B${r + 1}")
    reg("PF3", "Cohorts", a1(r, 1), name="COHORT_CUSTOMERS", expect=cust_total, label="customers in the nine cohorts")
    reg("PF3", "Cohorts", a1(r, 4), name="NRR_12M", expect=round(s1 / s0, 6), label="12-month net revenue retention")
    reg("PF3", "Cohorts", "A2", expect="Cohort = customers still active after onboarding", label="note that drops early leavers")
    ws_coh.write(r + 2, 0, FOOTER, fm["note"])

    # ---- Hiring_Plan (the model counts only the first eight hires)
    ws_hire.set_column(0, 0, 30)
    ws_hire.set_column(1, 1, 20)
    ws_hire.set_column(2, 5, 18)
    ws_hire.write(0, 0, "Hiring plan used in this model", fm["title"])
    ws_hire.write(1, 0, "Loaded monthly cost = base pay times the load factor, divided by 12.", fm["note"])
    ws_hire.write_row(3, 0, ["Role", "Department", "Start month", "Base pay (USD a year)", "Loaded cost (USD a month)"], fm["headl"])
    r = 4
    first = r
    for i, (role, dept, _k, base) in enumerate(HIRES[:MODELED_HIRES]):
        t = 1 + i // 2
        ws_hire.write(r, 0, role)
        ws_hire.write(r, 1, dept)
        ws_hire.write(r, 2, mlabel(N_MONTHS - 1 + t))
        ws_hire.write_number(r, 3, base, fm["usd"])
        ws_hire.write_formula(r, 4, f"=D{r + 1}*LOAD_FACTOR/12", fm["usd"], base * LOAD / 12)
        r += 1
    ws_hire.write(r, 0, "Hires in this plan", fm["bold"])
    ws_hire.write_formula(r, 1, f"=COUNTA(A{first + 1}:A{r})", fm["name"], MODELED_HIRES)
    wb.define_name("HIRES_COUNTED", f"=Hiring_Plan!$B${r + 1}")
    reg("PF4", "Hiring_Plan", a1(r, 1), name="HIRES_COUNTED", expect=MODELED_HIRES, label="hires the model pays for")
    ws_hire.write(r + 1, 0, "Staff after these hires", fm["bold"])
    ws_hire.write_formula(r + 1, 1, f"=STAFF_NOW+B{r + 1}", fm["int"], HEADCOUNT_NOW + MODELED_HIRES)
    ws_hire.write(r + 3, 0, FOOTER, fm["note"])

    # ---- Cash_Runway (48 plan months)
    ws_cash.set_column(0, 0, 44)
    ws_cash.set_column(1, 9, 16)
    ws_cash.write(0, 0, "Cash and runway (USD)", fm["title"])
    rows48, runway48 = forecast(F["model_hires"], 48)
    ws_cash.write(2, 0, "Runway (months of cash from the data date)", fm["bold"])
    ws_cash.write(3, 0, "Average net burn, plan months 1 to 12 (USD a month)", fm["bold"])
    ws_cash.write(4, 0, "Cash at the data date (USD)", fm["bold"])
    hdr = 6
    ws_cash.write_row(hdr, 0, ["Month", "Plan month", "Recurring revenue", "Cost of revenue", "Payroll",
                               "Hosting, rent, tools, legal and other", "Marketing programs", "Net burn",
                               "Equity raised", "Ending cash"], fm["headl"])
    r0 = hdr + 1
    ws_cash.write(r0, 0, "2026-09")
    ws_cash.write_number(r0, 1, 0, fm["int"])
    ws_cash.write_formula(r0, 9, "=CASH_START", fm["usd"], CASH_START)
    prev_cash = CASH_START
    for i, x in enumerate(rows48):
        r = r0 + 1 + i
        ws_cash.write(r, 0, x["label"])
        ws_cash.write_number(r, 1, x["t"], fm["int"])
        ws_cash.write_number(r, 2, x["rev"], fm["usd"])
        ws_cash.write_number(r, 3, x["cogs"], fm["usd"])
        ws_cash.write_number(r, 4, x["payroll"], fm["usd"])
        ws_cash.write_number(r, 5, x["hosting"] + x["rent"], fm["usd"])
        ws_cash.write_number(r, 6, x["program"], fm["usd"])
        ws_cash.write_formula(r, 7, f"=D{r + 1}+E{r + 1}+F{r + 1}+G{r + 1}-C{r + 1}", fm["usd"], x["burn"])
        ws_cash.write_number(r, 8, x["raised"], fm["usd"])
        ws_cash.write_formula(r, 9, f"=J{r}+I{r + 1}-H{r + 1}", fm["usd"], x["cash"])
        prev_cash = x["cash"]
    first_t, last_t = r0 + 2, r0 + 1 + len(rows48)      # 1-based rows of plan months 1 and 48
    avg12 = sum(x["burn"] for x in rows48[:12]) / 12
    ws_cash.write_formula(2, 1, f'=COUNTIF(J{first_t}:J{last_t},">0")', fm["name"], runway48)
    ws_cash.write_formula(3, 1, f"=AVERAGE(H{first_t}:H{first_t + 11})", fm["name"], avg12)
    ws_cash.write_formula(4, 1, "=CASH_START", fm["name"], CASH_START)
    wb.define_name("RUNWAY_MONTHS", "=Cash_Runway!$B$3")
    wb.define_name("AVG_NET_BURN_12M", "=Cash_Runway!$B$4")
    reg("PF4", "Cash_Runway", "B3", name="RUNWAY_MONTHS", expect=runway48, label="runway in months")
    reg("PF4", "Cash_Runway", "B4", name="AVG_NET_BURN_12M", expect=round(avg12, 2), label="average net burn, plan months 1 to 12")
    ws_cash.write(last_t + 1, 0, FOOTER, fm["note"])
    F["model_runway"], F["model_avg12"] = runway48, avg12
    F["ass_cell"] = ASS_CELL
    wb.close()


def build_cap_table():
    path = ROOM / "02_financials/cap_table.xlsx"
    wb = new_workbook(path)
    fm = formats(wb)
    rel = "02_financials/cap_table.xlsx"
    ws = wb.add_worksheet("Cap_Table")
    ws.set_column(0, 0, 40)
    ws.set_column(1, 1, 30)
    ws.set_column(2, 5, 20)
    ws.write(0, 0, "Hollis Voice, Inc.: fully diluted cap table", fm["title"])
    ws.write(1, 0, "As of 2026-09-30. SAFEs shown as converted at their cap. Pro forma shows the Series A.", fm["note"])
    ws.write_row(3, 0, ["Holder", "Class", "Shares", "% fully diluted", "Pro forma shares", "Pro forma %"], fm["headl"])
    pool_total = 2_000_000
    holders = [
        (CEO["name"] + " (CEO)", "Common", 4_400_000),
        (CTO["name"] + " (CTO)", "Common", 3_600_000),
        ("Options granted (11 holders)", "Option pool, granted", 1_150_000),
        ("Options available", "Option pool, unissued", pool_total - 1_150_000),
        (SAFE_A_NAME + " (SAFE converted)", "Preferred (from SAFE)", 1_200_000),
        (SAFE_B_NAME + " (SAFE converted)", "Preferred (from SAFE)", 800_000),
    ]
    r = 4
    first = r
    total = sum(h[2] for h in holders)
    new_shares = round(total * SERIES_A / SERIES_A_PRE)
    post = total + new_shares
    for (name, cls, sh) in holders:
        ws.write(r, 0, name)
        ws.write(r, 1, cls)
        ws.write_number(r, 2, sh, fm["int"])
        ws.write_formula(r, 3, f"=C{r + 1}/C${first + len(holders) + 2}", fm["pct2"], sh / total)
        ws.write_formula(r, 4, f"=C{r + 1}", fm["int"], sh)
        ws.write_formula(r, 5, f"=E{r + 1}/E${first + len(holders) + 2}", fm["pct2"], sh / post)
        r += 1
    ws.write(r, 0, SERIES_A_LEAD)
    ws.write(r, 1, "Series A Preferred")
    ws.write_number(r, 2, 0, fm["int"])
    ws.write_formula(r, 3, f"=C{r + 1}/C${first + len(holders) + 2}", fm["pct2"], 0)
    lead_row = r
    ws.write_formula(r, 5, f"=E{r + 1}/E${first + len(holders) + 2}", fm["pct2"], new_shares / post)
    r += 1
    tot_row = r
    ws.write(r, 0, "Total", fm["bold"])
    ws.write_formula(r, 2, f"=SUM(C{first + 1}:C{r})", fm["intb"], total)
    ws.write_formula(r, 3, f"=SUM(D{first + 1}:D{r})", fm["pctb"], 1.0)
    ws.write_formula(r, 4, f"=SUM(E{first + 1}:E{r})", fm["intb"], post)
    ws.write_formula(r, 5, f"=SUM(F{first + 1}:F{r})", fm["pctb"], 1.0)
    wb.define_name("CAP_TOTAL_PCT", f"=Cap_Table!$D${r + 1}")
    LOC["DC3"].append({"file": rel, "sheet": "Cap_Table", "cell": a1(r, 3), "named_cell": "CAP_TOTAL_PCT", "expect": 1.0,
                       "label": "holders add to 100 percent"})
    LOC["DC3"].append({"file": rel, "sheet": "Cap_Table", "cell": a1(r, 2), "expect": total, "label": "fully diluted shares before the Series A"})
    r += 2
    ws.write(r, 0, "SAFE conversion", fm["bold"])
    r += 1
    ws.write_row(r, 0, ["Investor", "Purchase amount (USD)", "Post-money cap (USD)", "Ownership", "Conversion price (USD)", "Shares"], fm["headl"])
    r += 1
    safe_first = r
    price = SAFE_CAP / total
    for (name, amt, sh) in ((SAFE_A_NAME, 1_200_000, 1_200_000), (SAFE_B_NAME, 800_000, 800_000)):
        ws.write(r, 0, name)
        ws.write_number(r, 1, amt, fm["usd"])
        ws.write_number(r, 2, SAFE_CAP, fm["usd"])
        ws.write_formula(r, 3, f"=B{r + 1}/C{r + 1}", fm["pct2"], amt / SAFE_CAP)
        ws.write_formula(r, 4, f"=C{r + 1}/C${tot_row + 1}", fm["dec"], price)
        ws.write_formula(r, 5, f"=B{r + 1}/E{r + 1}", fm["int"], amt / price)
        LOC["DC3"].append({"file": rel, "sheet": "Cap_Table", "cell": a1(r, 5), "expect": amt / price,
                           "label": f"shares from the {name} SAFE at the cap"})
        r += 1
    ws.write(r, 0, "Total SAFEs", fm["bold"])
    ws.write_formula(r, 1, f"=SUM(B{safe_first + 1}:B{r})", fm["usdb"], SAFE_AMOUNT)
    ws.write_formula(r, 3, f"=SUM(D{safe_first + 1}:D{r})", fm["pctb"], SAFE_AMOUNT / SAFE_CAP)
    ws.write_formula(r, 5, f"=SUM(F{safe_first + 1}:F{r})", fm["intb"], SAFE_AMOUNT / price)
    r += 2
    ws.write(r, 0, "Series A", fm["bold"])
    r += 1
    rows = [
        ("Pre-money valuation (USD)", SERIES_A_PRE, "usd", None),
        ("New money (USD)", SERIES_A, "usd", None),
        ("Post-money valuation (USD)", SERIES_A_PRE + SERIES_A, "usd", f"=B{r + 1}+B{r + 2}"),
        ("Price per share (USD)", SERIES_A_PRE / total, "dec", f"=B{r + 1}/C{tot_row + 1}"),
        ("New shares issued", new_shares, "int", f"=B{r + 2}/B{r + 4}"),
        ("Series A ownership", new_shares / post, "pct2", f"=B{r + 2}/B{r + 3}"),
    ]
    for i, (lab, val, fmt, form) in enumerate(rows):
        ws.write(r + i, 0, lab)
        if form:
            ws.write_formula(r + i, 1, form, fm[fmt], val)
        else:
            ws.write_number(r + i, 1, val, fm[fmt])
    ws.write_formula(lead_row, 4, f"=B{r + 5}", fm["int"], new_shares)
    LOC["DC3"].append({"file": rel, "sheet": "Cap_Table", "cell": a1(r + 5, 1), "expect": round(new_shares / post, 6), "label": "Series A ownership"})
    ws.write(r + 8, 0, FOOTER, fm["note"])
    wb.close()
    F["cap"] = {"total_pre": total, "new_shares": new_shares, "post": post, "price_safe": price}


# ---------------------------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------------------------
def png_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def chart_mrr():
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    xs = list(range(N_MONTHS))
    ax.bar(xs, [v / 1000 for v in F["rec"]], color="#1B998B")
    ax.set_xticks(xs[::3])
    ax.set_xticklabels([MONTH_LABELS[i] for i in xs[::3]], fontsize=8)
    ax.set_ylabel("Monthly recurring revenue ($ thousands)", fontsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    return png_bytes(fig)


def chart_cohorts():
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for row in F["cohorts"]:
        ax.plot(range(13), [100 * v for v in row["curve"]], color="#B8C4D0", lw=1)
    agg = []
    for k in range(13):
        num = sum(r_["curve"][k] * r_["rep_start"] for r_ in F["cohorts"])
        den = sum(r_["rep_start"] for r_ in F["cohorts"])
        agg.append(100 * num / den)
    ax.plot(range(13), agg, color="#14213D", lw=3, label="All cohorts")
    ax.axhline(100, color="#999999", lw=0.8, ls="--")
    ax.set_xlabel("Months since first invoice", fontsize=9)
    ax.set_ylabel("Net revenue retention (%)", fontsize=9)
    ax.legend(frameon=False, fontsize=9, loc="lower left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    return png_bytes(fig)


# ---------------------------------------------------------------------------------------------
# The deck
# ---------------------------------------------------------------------------------------------
NAVY = colors.HexColor("#14213D")
TEAL = colors.HexColor("#1B998B")
GREYTXT = colors.HexColor("#555555")
LIGHT = colors.HexColor("#E8EEF4")
SW, SH = 960, 540
DECK = "01_overview/pitch_deck.pdf"


def deck_claims():
    """Every number the deck states, with the slide it first appears on."""
    mkt_clinics, mkt_acv = 28_000, 9_000
    return [
        ("ARR", money(F["deck_arr"]), 3),
        ("Clinics on Hollis", f"{F['accounts_cum']}", 3),
        ("Calls handled, September 2026", f"{F['calls'][LAST]:,}", 3),
        ("Largest customer", "under 9% of ARR", 4),
        ("Gross margin", "80%", 5),
        ("Net revenue retention", f"{pct(F['nrr_rep'])} (12 months)", 6),
        ("US independent clinics (company estimate)", f"{mkt_clinics:,}", 8),
        ("Market size (company estimate)", money(mkt_clinics * mkt_acv), 8),
        ("Runway", f"{F['runway_shown']} months", 11),
        ("Average monthly net burn, next 12 months", money(round(F["burn_shown"])), 11),
        ("Planned hires, next 12 months", f"{PLANNED_HIRES}", 12),
        ("Staff after hiring", f"{HEADCOUNT_NOW + PLANNED_HIRES}", 12),
        ("Series A raise", money(SERIES_A), 13),
        ("Pre-money valuation", money(SERIES_A_PRE), 13),
    ]


def build_deck():
    path = ROOM / DECK
    path.parent.mkdir(parents=True, exist_ok=True)
    c = rl_canvas.Canvas(str(path), pagesize=(SW, SH), invariant=1)
    c.setTitle("Hollis Voice: Series A pitch deck")
    c.setAuthor("Hollis Voice (synthetic)")
    c.setSubject(FOOTER)

    def frame(n, title):
        c.setFillColor(colors.white)
        c.rect(0, 0, SW, SH, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.rect(0, SH - 84, SW, 84, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 30)
        c.drawString(48, SH - 54, title)
        c.setFillColor(GREYTXT)
        c.setFont("Helvetica", 9)
        c.drawString(48, 22, FOOTER)
        c.drawRightString(SW - 48, 22, f"Slide {n} of 14")

    def para(text, x, y, width=860, size=20, lead=28, bold=False, color=colors.black):
        font = "Helvetica-Bold" if bold else "Helvetica"
        c.setFont(font, size)
        c.setFillColor(color)
        for line in simpleSplit(text, font, size, width):
            c.drawString(x, y, line)
            y -= lead
        return y

    def bullets(items, x, y, width=860, size=20, lead=28, gap=10):
        for it in items:
            c.setFillColor(TEAL)
            c.circle(x + 4, y + 6, 3.5, fill=1, stroke=0)
            y = para(it, x + 22, y, width - 22, size, lead)
            y -= gap
        return y

    def stat(x, y, big, label, size=54):
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", size)
        c.drawString(x, y, big)
        c.setFillColor(GREYTXT)
        c.setFont("Helvetica", 16)
        c.drawString(x, y - 26, label)

    def image(buf, x, y, w, h):
        c.drawImage(ImageReader(buf), x, y, width=w, height=h)

    def page(n, title):
        frame(n, title)

    # 1 Title
    c.setFillColor(NAVY)
    c.rect(0, 0, SW, SH, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 64)
    c.drawString(60, 330, "Hollis Voice")
    c.setFont("Helvetica", 28)
    c.drawString(60, 280, "The phone agent for independent veterinary clinics")
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(60, 200, f"Series A  |  {money(SERIES_A)}  |  Brooklyn, New York  |  Founded 2024")
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 14)
    c.drawString(60, 160, "Data as of 2026-09-30")
    c.setFillColor(colors.HexColor("#B8C4D0"))
    c.setFont("Helvetica", 9)
    c.drawString(60, 22, FOOTER)
    c.drawRightString(SW - 48, 22, "Slide 1 of 14")
    c.showPage()

    # 2 Problem and product
    page(2, "Problem and product")
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(NAVY)
    c.drawString(48, 420, "The problem")
    y = bullets(["Front desks are busy with people at the counter, so calls go to voicemail.",
                 "A pet owner who cannot get through calls the next clinic.",
                 "Clinics lose appointments and refill requests they never see."], 48, 385, 420, 18, 25)
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(NAVY)
    c.drawString(500, 420, "The product")
    bullets(["Hollis Voice answers every call, day and night.",
             "It books the appointment into the clinic's calendar.",
             "It sends refill requests to staff to approve.",
             "It texts the pet owner a confirmation."], 500, 385, 420, 18, 25)
    c.showPage()

    # 3 Where we are
    page(3, "Where we are")
    stat(48, 410, "$2.5M", "ARR")
    stat(48, 310, f"{F['accounts_cum']}", "Clinics on Hollis")
    stat(48, 210, f"{F['calls'][LAST]:,}", "Calls handled in September 2026", 40)
    image(chart_mrr(), 360, 80, 560, 315)
    c.setFillColor(GREYTXT)
    c.setFont("Helvetica", 11)
    c.drawString(360, 62, "Monthly recurring revenue, January 2025 to September 2026.")
    LOC["PF2"].append({"file": DECK, "page": 3, "text": "$2.5M", "expect": F["deck_arr"], "label": "deck ARR on the traction slide"})
    LOC["PF7"].append({"file": DECK, "page": 3, "text": "Clinics on Hollis", "label": "deck label"})
    LOC["PF7"].append({"file": DECK, "page": 3, "text": f"{F['accounts_cum']}", "expect": F["accounts_cum"], "label": "deck clinic count"})
    c.showPage()

    # 4 Customers
    page(4, "Customers")
    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(NAVY)
    c.drawString(48, 420, "No customer above 9% of ARR")
    bullets(["A broad base of independent clinics, from one-room practices to hospital groups.",
             "Cedar & Pine Animal Hospitals runs Hollis Voice across 17 locations.",
             "Marlow Veterinary Group started a pilot in August 2026.",
             "Brookline Row Veterinary and other clinics pay once a year, in advance."], 48, 360, 860, 20, 28)
    LOC["PF5"].append({"file": DECK, "page": 4, "text": "No customer above 9% of ARR", "label": "deck concentration claim"})
    c.showPage()

    # 5 Unit economics
    page(5, "Unit economics")
    stat(48, 400, "80%", "Gross margin", 72)
    bullets(["Cost of revenue is phone minutes and speech software licences.",
             "Phone minutes are 15% of revenue. Licences are 5%.",
             "Plans start at $349 a month."], 48, 290, 860, 20, 28)
    LOC["PF6"].append({"file": DECK, "page": 5, "text": "80%", "label": "deck gross margin"})
    LOC["PF6"].append({"file": DECK, "page": 5, "text": "Gross margin", "label": "deck label"})
    c.showPage()

    # 6 Cohort chart
    page(6, "Retention")
    stat(48, 400, pct(F["nrr_rep"]), "Net revenue retention", 60)
    para("Twelve months after the first invoice, cohorts pay more than they did at the start.", 48, 310, 330, 18, 25)
    image(chart_cohorts(), 400, 70, 520, 292)
    c.setFillColor(GREYTXT)
    c.setFont("Helvetica", 11)
    c.drawString(400, 52, "Cohorts count customers still active after onboarding. Nine cohorts, January to September 2025.")
    LOC["PF3"].append({"file": DECK, "page": 6, "text": pct(F["nrr_rep"]), "label": "deck net revenue retention"})
    LOC["PF3"].append({"file": DECK, "page": 6, "text": "Cohorts count customers still active after onboarding.", "label": "chart caption"})
    c.showPage()

    # 7 Pricing
    page(7, "Pricing")
    x = 48
    for name, price, desc in (("Starter", "$349", "One location, basic call answering"),
                              ("Standard", "$649", "Booking and refill requests"),
                              ("Pro", "$1,099", "Everything, with priority support"),
                              ("Group", "Custom", "Multi-location hospitals")):
        c.setFillColor(LIGHT)
        c.roundRect(x, 190, 208, 210, 8, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(x + 16, 360, name)
        c.setFont("Helvetica-Bold", 34)
        c.drawString(x + 16, 310, price)
        c.setFillColor(GREYTXT)
        c.setFont("Helvetica", 12)
        c.drawString(x + 16, 285, "a month" if price != "Custom" else "per agreement")
        para(desc, x + 16, 250, 176, 14, 19, color=colors.black)
        x += 224
    para("A one-time onboarding fee of $500 applies to each new clinic. It is not part of recurring revenue.", 48, 150, 860, 16, 22)
    c.showPage()

    # 8 Market
    page(8, "Market")
    bullets(["About 28,000 independent veterinary clinics in the United States (company estimate).",
             "At about $9,000 a year per clinic, that is a market near $252,000,000 (company estimate).",
             "Chains already have call centers. Independent clinics do not."], 48, 410, 860, 22, 30)
    c.showPage()

    # 9 Competition
    page(9, "Competition")
    x = 48
    for name, line in (("Answering services", "People read a script and take a message. No booking, no refills."),
                       ("Generic AI receptionists", "Built for any business. They do not know a vet clinic's calls."),
                       ("Practice software add-ons", "Tied to one system and rarely answer the phone well."),
                       ("Hollis Voice", "Built for vet clinics: vaccine reminders, refills and emergency routing.")):
        c.setFillColor(NAVY if name == "Hollis Voice" else LIGHT)
        c.roundRect(x, 190, 208, 220, 8, fill=1, stroke=0)
        c.setFillColor(colors.white if name == "Hollis Voice" else NAVY)
        c.setFont("Helvetica-Bold", 17)
        for i, ln in enumerate(simpleSplit(name, "Helvetica-Bold", 17, 176)):
            c.drawString(x + 16, 380 - i * 22, ln)
        para(line, x + 16, 330, 176, 14, 19, color=colors.white if name == "Hollis Voice" else colors.black)
        x += 224
    c.showPage()

    # 10 Team
    page(10, "Team")
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(NAVY)
    c.drawString(48, 420, CEO["name"])
    para("CEO and co-founder. Ran operations for a regional veterinary group before Hollis Voice.", 48, 392, 400, 15, 21)
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(NAVY)
    c.drawString(500, 420, CTO["name"])
    para("CTO and co-founder. Spent eleven years building speech systems at a telecom software company.", 500, 392, 400, 15, 21)
    y = 300
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(NAVY)
    c.drawString(48, y, "Senior team")
    y -= 28
    for nm, role in SENIOR:
        para(f"{nm}, {role}", 48, y, 860, 15, 20)
        y -= 26
    para(f"{HEADCOUNT_NOW} people today.", 48, y - 10, 860, 16, 22, bold=True)
    c.showPage()

    # 11 Plan and use of funds
    page(11, "Plan and runway")
    stat(48, 400, f"{F['runway_shown']} months", "Runway", 60)
    stat(48, 290, money(round(F["burn_shown"])) + " a month", "Average net burn over the next 12 months", 40)
    bullets(["The Series A is planned to close in January 2027.",
             "Revenue grows 3.5% a month in the plan.",
             "The plan funds marketing programs from the month the round closes."], 48, 200, 860, 18, 25)
    LOC["PF4"].append({"file": DECK, "page": 11, "text": f"{F['runway_shown']} months", "expect": F["runway_shown"], "label": "deck runway"})
    LOC["PF4"].append({"file": DECK, "page": 11, "text": money(round(F["burn_shown"])) + " a month", "expect": round(F["burn_shown"]), "label": "deck average net burn"})
    c.showPage()

    # 12 Hiring
    page(12, "Hiring")
    counts = defaultdict(int)
    for h in HIRES:
        counts[h[1]] += 1
    stat(48, 400, f"{PLANNED_HIRES} hires", "Planned over the next 12 months", 52)
    para(f"Staff grows from {HEADCOUNT_NOW} to {HEADCOUNT_NOW + PLANNED_HIRES}.", 48, 330, 860, 22, 30, bold=True)
    y = 280
    for dept in ("Engineering", "Sales", "Customer Success", "Support", "Marketing", "G&A"):
        para(f"{dept}: {counts[dept]}", 48, y, 400, 18, 24)
        y -= 28
    LOC["PF4"].append({"file": DECK, "page": 12, "text": f"{PLANNED_HIRES} hires", "expect": PLANNED_HIRES, "label": "deck planned hires"})
    c.showPage()

    # 13 The ask
    page(13, "The ask")
    stat(48, 400, money(SERIES_A), "Series A", 60)
    para(f"At {money(SERIES_A_PRE)} pre-money, for {pct(SERIES_A / (SERIES_A + SERIES_A_PRE), 2)} of the company.", 48, 330, 860, 20, 28)
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(NAVY)
    c.drawString(48, 270, "Use of funds")
    y = 240
    for lab, share in (("Engineering", 0.40), ("Sales and marketing", 0.35), ("Customer success and support", 0.15), ("General and administrative", 0.10)):
        para(f"{lab}: {money(SERIES_A * share)} ({share * 100:.0f}%)", 48, y, 860, 17, 24)
        y -= 28
    c.showPage()

    # 14 Claims
    page(14, "Claims page")
    c.setFont("Helvetica", 11)
    c.setFillColor(GREYTXT)
    c.drawString(48, 438, "Every number in this deck, with the slide where it first appears.")
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(NAVY)
    c.drawString(48, 414, "Claim")
    c.drawString(520, 414, "Value")
    c.drawString(840, 414, "Slide")
    y = 392
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    claims = deck_claims()
    for (lab, val, sl) in claims:
        c.drawString(48, y, lab)
        c.drawString(520, y, val)
        c.drawString(840, y, str(sl))
        y -= 22
    LOC["CLAIMS"] = [{"label": lab, "value": val, "slide": sl} for (lab, val, sl) in claims]
    for flag, lab in (("PF2", "ARR"), ("PF7", "Clinics on Hollis"), ("PF5", "Largest customer"), ("PF6", "Gross margin"),
                      ("PF3", "Net revenue retention"), ("PF4", "Runway")):
        row = [x for x in claims if x[0] == lab][0]
        LOC[flag].append({"file": DECK, "page": 14, "claims_row": lab, "text": row[1], "slide_ref": row[2],
                          "label": f"claims row '{lab}'"})
    c.showPage()
    c.save()


# ---------------------------------------------------------------------------------------------
# Platypus PDFs
# ---------------------------------------------------------------------------------------------
STYLES = getSampleStyleSheet()
S_BODY = ParagraphStyle("body", parent=STYLES["BodyText"], fontName="Helvetica", fontSize=10.5, leading=15, spaceAfter=6)
S_SMALL = ParagraphStyle("small", parent=S_BODY, fontSize=9, leading=12, textColor=GREYTXT)
S_H1 = ParagraphStyle("h1", parent=STYLES["Heading1"], fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=NAVY, spaceAfter=10)
S_H2 = ParagraphStyle("h2", parent=STYLES["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=NAVY, spaceBefore=8, spaceAfter=4)
S_CLAUSE = ParagraphStyle("clause", parent=S_BODY, leftIndent=0)
S_CELL = ParagraphStyle("cell", parent=S_BODY, fontSize=9, leading=12, spaceAfter=0)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def make_pdf(rel, story, title):
    path = ROOM / rel
    path.parent.mkdir(parents=True, exist_ok=True)

    def foot(cv, doc):
        cv.saveState()
        cv.setFont("Helvetica", 8)
        cv.setFillColor(GREYTXT)
        cv.drawString(54, 30, FOOTER)
        cv.drawRightString(letter[0] - 54, 30, f"Page {doc.page}")
        cv.restoreState()

    doc = SimpleDocTemplate(str(path), pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54,
                            title=title, author="Hollis Voice (synthetic)", subject=FOOTER, invariant=1)
    doc.build(story, onFirstPage=foot, onLaterPages=foot)


def tbl(rows, widths, head=True):
    data = [[Paragraph(esc(str(x)), S_CELL) for x in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    style = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B8C4D0")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if head:
        style.append(("BACKGROUND", (0, 0), (-1, 0), LIGHT))
    t.setStyle(TableStyle(style))
    return t


def P(text, style=S_BODY):
    return Paragraph(esc(text), style)


def date_add_months(y, m, n):
    idx = (y * 12 + (m - 1)) + n
    return idx // 12, idx % 12 + 1


ROOM_FILES = [
    ("00_welcome/cover_note_and_index.pdf", "Cover note and a numbered index of the room.", "first"),
    ("01_overview/pitch_deck.pdf", "Pitch deck, 14 slides. Slide 14 lists every number with its slide.", "first"),
    ("01_overview/company_overview.pdf", "One-page company overview.", "first"),
    ("01_overview/pitch_video_script.md", "Two-minute script for the pitch video.", "first"),
    ("02_financials/financial_model.xlsx", "Financial model: assumptions, P&L, ARR build, cohorts, hiring plan, cash.", "first"),
    ("02_financials/cap_table.xlsx", "Fully diluted cap table with the two SAFEs and the option pool.", "first"),
    ("02_financials/expense_ledger.csv", "Expense lines by month with vendor and category.", "second"),
    ("03_metrics/monthly_metrics.csv", "Monthly metrics: MRR, ARR, paying accounts, accounts created, calls.", "first"),
    ("03_metrics/customer_mrr_by_month.csv", "Revenue by customer by month, with plan and product type.", "second"),
    ("04_customers/order_form_cedar_pine.pdf", "Order form: Cedar & Pine Animal Hospitals, 17 locations.", "second"),
    ("04_customers/pilot_agreement_marlow.pdf", "Pilot agreement: Marlow Veterinary Group.", "second"),
    ("04_customers/order_form_brookline_row.pdf", "Order form: Brookline Row Veterinary, annual plan.", "second"),
    ("05_team/founder_bios.pdf", "Founder and senior team bios.", "first"),
    ("05_team/hiring_plan.csv", "Hiring plan: 24 hires over the next 12 months.", "first"),
    ("06_product/product_one_pager.pdf", "Product one-pager: what it does, pricing, integrations.", "first"),
    ("06_product/website_copy.md", "Home page and pricing copy.", "first"),
]


def build_cover_note():
    story = [P("Hollis Voice, Inc.", S_H1),
             P("Data room for the Series A. Data as of 2026-09-30."),
             P("Thank you for your time. This room has two tiers. The first tier is the deck, the model, the cap table, the metrics, the team "
               "and the product. The second tier is the detail behind the numbers: revenue by customer, the expense ledger and the customer "
               "agreements. We share the second tier after a term sheet. Every number in the deck ties to a file in this room, and the deck's "
               "last slide lists each one."),
             P("Imogen Tarrant, Chief Executive Officer", S_SMALL),
             Spacer(1, 10)]
    rows = [["#", "File", "What it is", "Tier"]]
    for i, (rel, what, tier) in enumerate(ROOM_FILES, 1):
        rows.append([str(i), rel, what, "First tier" if tier == "first" else "Second tier"])
    story.append(tbl(rows, [22, 190, 230, 60]))
    make_pdf("00_welcome/cover_note_and_index.pdf", story, "Hollis Voice: cover note and index")


def build_overview():
    story = [P("Hollis Voice: company overview", S_H1),
             P("Hollis Voice is an AI phone agent for independent veterinary clinics. It answers every call, books appointments and "
               "sends refill requests to staff. The company was founded in 2024 and is based in Brooklyn, New York."),
             P("Who", S_H2),
             P(f"{CEO['name']} (CEO) and {CTO['name']} (CTO) founded the company. {HEADCOUNT_NOW} people work there today."),
             P("Traction", S_H2),
             P(f"ARR: {money(F['deck_arr'])}. Clinics on Hollis: {F['accounts_cum']}. Gross margin: 80%. Net revenue retention over 12 months: {pct(F['nrr_rep'])}. "
               f"Largest customer: under 9% of ARR. Calls handled in September 2026: {F['calls'][LAST]:,}. All figures are as of 2026-09-30."),
             P("The ask", S_H2),
             P(f"We are raising {money(SERIES_A)} in a Series A at {money(SERIES_A_PRE)} pre-money. We plan to hire {PLANNED_HIRES} people over the next 12 months and "
               f"expect {F['runway_shown']} months of runway."),
             P("Earlier funding", S_H2),
             P(f"{money(SAFE_AMOUNT)} in SAFEs on a {money(SAFE_CAP)} post-money cap."),
             P("Contact: hello@hollisvoice.example", S_SMALL)]
    make_pdf("01_overview/company_overview.pdf", story, "Hollis Voice: company overview")
    for flag in ("PF2", "PF7"):
        LOC[flag].append({"file": "01_overview/company_overview.pdf", "page": 1,
                          "text": f"ARR: {money(F['deck_arr'])}" if flag == "PF2" else f"Clinics on Hollis: {F['accounts_cum']}",
                          "label": "overview repeats the deck claim"})


def build_bios():
    story = [P("Founders", S_H1)]
    bios = [
        (CEO, "Imogen ran operations for a regional veterinary group for nine years. She managed front desks, scheduling and staffing across several "
              "clinics, and saw how many calls went unanswered. She holds a bachelor's degree from Hudson Valley Polytechnic. She founded Hollis Voice in 2024."),
        (CTO, "Teodoro spent eleven years building speech and telephony systems at Kestrel Telecom Software, most recently as a director of engineering. "
              "He holds a master's degree in computer science from Lakeshore Institute of Technology. He co-founded Hollis Voice in 2024."),
    ]
    for p, text in bios:
        story += [P(p["name"], S_H2), P(p["title"], S_SMALL), P(text),
                  P(f"GitHub: github.com/{FOUNDER_GITHUB[p['name']]}", S_SMALL), Spacer(1, 8)]
    story.append(PageBreak())
    story.append(P("Senior team", S_H1))
    texts = {
        "Head of Sales": "Marguerite sold software to multi-location service businesses for twelve years before joining Hollis Voice in 2025.",
        "Head of Customer Success": "Anselm led onboarding for a scheduling software company and joined Hollis Voice in 2025.",
        "Controller (part time)": "Hallie is a certified public accountant who works with several early-stage companies. She joined Hollis Voice in 2026.",
        "Lead Voice Engineer": "Lucan built call-routing systems at a regional telephone carrier and joined Hollis Voice in 2025.",
    }
    for nm, role in SENIOR:
        story += [P(nm, S_H2), P(role, S_SMALL), P(texts[role])]
    make_pdf("05_team/founder_bios.pdf", story, "Hollis Voice: founder bios")


def build_one_pager():
    story = [P("Hollis Voice: product one-pager", S_H1),
             P("What it does", S_H2),
             P("Hollis Voice answers a clinic's phone line. It talks to the caller, books or moves an appointment, takes a refill request, "
               "routes an emergency to the on-call vet, and texts the owner a confirmation. Staff see a short summary of every call."),
             P("Pricing", S_H2),
             tbl([["Plan", "Price a month", "Who it is for"],
                  ["Starter", "$349", "One location, basic call answering"],
                  ["Standard", "$649", "Booking and refill requests"],
                  ["Pro", "$1,099", "Everything, with priority support"],
                  ["Group", "Custom", "Multi-location hospitals"]], [90, 100, 300]),
             Spacer(1, 6),
             P("A one-time onboarding fee of $500 applies to each new clinic. Annual plans can be paid once a year in advance."),
             P("Works with", S_H2),
             P("Common veterinary practice management systems through calendar sync. Standard phone lines and SIP trunks. Text messages to pet owners."),
             P("Contact: hello@hollisvoice.example", S_SMALL)]
    make_pdf("06_product/product_one_pager.pdf", story, "Hollis Voice: product one-pager")


def build_orders():
    bk = F["brook"]
    # Cedar & Pine: 3 pages
    story = [P("Order Form: Cedar & Pine Animal Hospitals", S_H1),
             P("Between Hollis Voice, Inc. (the Provider) and Cedar & Pine Animal Hospitals (the Customer). Effective date: 2025-11-01."),
             tbl([["Item", "Detail"],
                  ["Plan", "Group"],
                  ["Locations", "9 at signing. 17 from 2026-04-01 (see Amendment No. 1)."],
                  ["Monthly fee", "$18,000 until 2026-03-31. $36,000 from 2026-04-01."],
                  ["Initial term", "24 months, from 2025-11-01 to 2027-10-31."],
                  ["Renewal", "Renews for 12 months at a time unless either party gives 90 days written notice before the term ends."],
                  ["Payment", "Monthly in advance, net 30 days."],
                  ["Onboarding fee", "$500, one time, invoiced with the first month."]], [110, 380]),
             PageBreak(),
             P("Terms", S_H1),
             P("1. Services. The Provider answers the Customer's phone lines with its AI phone agent, books appointments and sends refill requests to Customer staff."),
             P("2. Fees. Fees are fixed for the initial term. The Provider will not raise them during the initial term."),
             P("3. Termination. Either party may end this order form for a material breach that is not fixed within 30 days of written notice. "
               "The Customer has no other right to end the order form during the initial term."),
             P("4. Data. The Customer owns its call recordings and appointment data. The Provider uses them only to run the service."),
             P("5. Service levels. The Provider aims for 99.5% monthly availability of the phone agent."),
             PageBreak(),
             P("Amendment No. 1", S_H1),
             P("Effective 2026-04-01. The Customer adds 8 locations, for a total of 17. The monthly fee becomes $36,000 for the rest of the initial term. "
               "All other terms stay the same."),
             Spacer(1, 18),
             P("Signed for the Provider: Imogen Tarrant, Chief Executive Officer"),
             P("Signed for the Customer: Delia Marchetti-Owens, Chief Operating Officer")]
    make_pdf("04_customers/order_form_cedar_pine.pdf", story, "Order form: Cedar & Pine Animal Hospitals")
    LOC["PF5"].append({"file": "04_customers/order_form_cedar_pine.pdf", "page": 1, "text": "$36,000 from 2026-04-01", "label": "largest customer fee"})

    # Marlow pilot: 3 pages, clauses 2, 7, 8 are the ones that matter
    story = [P("Pilot Agreement: Marlow Veterinary Group", S_H1),
             P("Between Hollis Voice, Inc. (the Provider) and Marlow Veterinary Group (the Customer). Effective date: 2026-08-01."),
             P("1. Pilot. The Provider will run a pilot of its AI phone agent at 4 Customer locations. The pilot is a trial of the service. "
               "It is not a subscription."),
             P("2. Term and fees. The pilot runs for six (6) months, from 2026-08-01 to 2027-01-31. The Customer pays $15,000 a month, "
               "$90,000 in total, invoiced monthly."),
             P("3. Services. The Provider answers calls on the Customer's pilot phone lines and books appointments."),
             P("4. Setup. The Provider connects the phone lines and the appointment calendar during the first week."),
             PageBreak(),
             P("5. Reporting. The Provider sends a monthly summary of calls handled and appointments booked."),
             P("6. Confidentiality. Each party keeps the other's non-public information private."),
             P("7. Termination. Either party may end this pilot at any time, for any reason, by giving thirty (30) days written notice."),
             P("8. No duty to convert. Nothing in this agreement requires the Customer to buy a subscription when the pilot ends. "
               "Any subscription needs a separate order form signed by both parties."),
             P("9. Governing law. The laws of the State of New York apply."),
             PageBreak(),
             P("Signatures", S_H1),
             P("Signed for the Provider: Imogen Tarrant, Chief Executive Officer"),
             P("Signed for the Customer: Gideon Pellworth, Managing Partner"),
             P("Date: 2026-08-01")]
    make_pdf("04_customers/pilot_agreement_marlow.pdf", story, "Pilot agreement: Marlow Veterinary Group")
    for t_, lab in (("2. Term and fees.", "term and fees"), ("7. Termination.", "30 days notice"), ("8. No duty to convert.", "no duty to convert")):
        LOC["PF1"].append({"file": "04_customers/pilot_agreement_marlow.pdf", "page": 2 if t_[0] in "78" else 1, "text": t_, "label": lab})

    # Brookline Row: 2 pages, ordinary annual prepaid plan
    y0 = 2025 + bk["start"] // 12
    m0 = bk["start"] % 12 + 1
    ey, em = date_add_months(y0, m0, 12)
    annual = 12 * PLAN_PRICE["Standard"]
    d_start = f"{y0}-{m0:02d}-01"
    last_day = (datetime.date(ey, em, 1) - datetime.timedelta(days=1)).isoformat()
    story = [P("Order Form: Brookline Row Veterinary", S_H1),
             P(f"Between Hollis Voice, Inc. (the Provider) and Brookline Row Veterinary (the Customer). Effective date: {d_start}."),
             tbl([["Item", "Detail"],
                  ["Plan", "Standard, 1 location"],
                  ["Term", f"12 months, from {d_start} to {last_day}."],
                  ["Annual fee", f"{money(annual)}, invoiced once, in advance (12 months at {money(PLAN_PRICE['Standard'])} a month)."],
                  ["Renewal", "Renews for 12 months at a time unless either party gives 30 days written notice."],
                  ["Onboarding fee", "$500, one time."]], [110, 380]),
             PageBreak(),
             P("Terms", S_H1),
             P("1. Services. The Provider answers the Customer's phone line, books appointments and sends refill requests to staff."),
             P("2. Fees. The Customer pays the annual fee once, in advance. The service is delivered in every month of the term."),
             P("3. Termination. Either party may end this order form for a material breach that is not fixed within 30 days of written notice."),
             Spacer(1, 18),
             P("Signed for the Provider: Imogen Tarrant, Chief Executive Officer"),
             P("Signed for the Customer: Odalys Brennecke, Practice Owner")]
    make_pdf("04_customers/order_form_brookline_row.pdf", story, "Order form: Brookline Row Veterinary")
    LOC["DC2"].append({"file": "04_customers/order_form_brookline_row.pdf", "page": 1, "text": money(annual), "label": "annual prepaid fee"})
    LOC["DC2"].append({"file": "03_metrics/customer_mrr_by_month.csv", "customer_name": BROOKLINE, "customer_id": bk["id"],
                       "product_type": "Subscription", "mrr": PLAN_PRICE["Standard"], "label": "customer row for Brookline Row Veterinary"})
    F["brook_annual"] = annual


# ---------------------------------------------------------------------------------------------
# Markdown files
# ---------------------------------------------------------------------------------------------
def build_markdown():
    script = f"""# Hollis Voice: two-minute pitch script

Read this out loud on your phone. Keep a steady pace. Each time stamp marks where that part should begin.

**0:00 Who we are**

Hi, I'm {CEO['name']}, co-founder and CEO of Hollis Voice. Independent veterinary clinics miss calls. The front desk is busy with people at the counter, the phone rings out, and the pet owner calls the next clinic. The clinic never learns that the appointment was lost.

**0:20 What it does**

Hollis Voice is an AI phone agent. It answers every call, day and night. It books the appointment, sends refill requests to the staff, and texts the pet owner a confirmation. It plugs into the clinic's existing phone line, so there is nothing new for the staff to learn.

**0:35 Traction**

We started charging in January 2025. Since then we have grown every quarter. Today we're at about three million dollars in annual recurring revenue.

**0:50 Clinics, retention and our largest customer**

That is {F['accounts_cum']} clinics on Hollis. Net revenue retention is a little over one hundred percent, so the clinics we win spend more over time. Our biggest customer runs Hollis Voice across seventeen locations, and it is still under nine percent of ARR. The base is spread out.

**1:10 Why we win**

The other options are answering services that read a script, or generic AI receptionists that do not know a vet clinic. We built for vet clinics. Vaccine reminders, refill requests and emergency routing work from day one. Our agent knows the difference between a booking and a poisoning.

**1:30 Team**

My co-founder, {CTO['name']}, spent eleven years building speech systems at a telecom software company. I ran operations for a regional veterinary group. We know both the phone and the front desk.

**1:45 The ask**

We are raising nine million dollars. We plan to hire twenty-four people over the next year, mostly engineers and salespeople. At our plan, that gives us {F['runway_shown']} months of runway.

**1:55 Close**

Thank you. I'm {CEO['name'].split()[0]}, and I would love to show you a live call.

---

{FOOTER}
"""
    words = len(" ".join(l for l in script.splitlines() if not l.startswith("**") and not l.startswith("#") and not l.startswith("Read this") and l != "---" and not l.startswith("Synthetic")).split())
    if not 250 <= words <= 340:
        sys.exit(f"Video script has {words} spoken words; expected about 300")
    F["script_words"] = words
    write_text(ROOM / "01_overview/pitch_video_script.md", script)
    LOC["PF2b"].append({"file": "01_overview/pitch_video_script.md", "time": "0:35", "text": "we're at about three million dollars in annual recurring revenue",
                        "expect": F["video_arr"], "label": "spoken ARR"})
    LOC["PF7"].append({"file": "01_overview/pitch_video_script.md", "time": "0:50", "text": f"{F['accounts_cum']} clinics on Hollis", "label": "spoken clinic count"})

    web = f"""# Hollis Voice

## Never miss another call

Hollis Voice is the AI phone agent for independent veterinary clinics. It answers every call, books the appointment and sends refill requests to your staff.

Trusted by {F['accounts_cum']} independent veterinary clinics.

## How it works

1. Forward your clinic's phone line to Hollis Voice.
2. Hollis Voice talks to the caller, books or moves the appointment, and takes the refill request.
3. Your staff see a short summary of every call and approve what needs approval.

## Built for vet clinics

- Vaccine reminders and booking in the clinic's own calendar.
- Refill requests that go to staff for approval.
- Emergency calls routed to your on-call vet.
- Text confirmations to pet owners.

## Pricing

| Plan | Price | Who it is for |
|---|---|---|
| Starter | $349 a month | One location, basic call answering |
| Standard | $649 a month | Booking and refill requests |
| Pro | $1,099 a month | Everything, with priority support |
| Group | Custom | Multi-location hospitals |

There is a one-time onboarding fee of $500 for each new clinic. Annual plans can be paid once a year in advance.

## Contact

hello@hollisvoice.example

---

{FOOTER}
"""
    write_text(ROOM / "06_product/website_copy.md", web)
    LOC["PF7"].append({"file": "06_product/website_copy.md", "text": f"Trusted by {F['accounts_cum']} independent veterinary clinics.", "label": "website repeats the clinic count"})


# ---------------------------------------------------------------------------------------------
# Answer key
# ---------------------------------------------------------------------------------------------
SEED_FILES = [rel for (rel, _w, tier) in ROOM_FILES if tier == "first"]


def build_answer_key():
    f = F
    arr_gap = f["deck_arr"] - f["model_arr"]
    flags = [
        {"id": "PF1", "name": "Pilot booked as ARR",
         "organiser_direction": "revenue counted as ARR when it is not recurring",
         "locations": LOC["PF1"],
         "shown": {"value": f["model_arr"], "unit": "USD", "label": "model ARR_TOTAL, with the pilot counted at $180,000 a year",
                   "details": {"pilot_arr_counted": f["pilot_arr"], "metrics_arr_2026_09": 12 * f["rec"][LAST]}},
         "true": {"value": f["true_arr"], "unit": "USD", "label": "recurring ARR from subscription rows",
                  "details": {"pilot_fees_contracted_total": PILOT["monthly_fee"] * PILOT["months"], "pilot_notice_days": PILOT["termination_days"]}},
         "check": "arr_from_subscription_rows",
         "check_description": "Recompute ARR as 12 times the 2026-09 MRR of rows with product_type = Subscription in customer_mrr_by_month.csv and compare with ARR_TOTAL.",
         "tolerance": 0.01,
         "files_needed": ["02_financials/financial_model.xlsx", "03_metrics/customer_mrr_by_month.csv", "04_customers/pilot_agreement_marlow.pdf"],
         "catchable_from_seed_drop": False,
         "note": "The model row label 'Marlow Veterinary Group (pilot)' hints at it in the seed drop, but the mechanical check needs the customer file."},
        {"id": "PF2", "name": "Deck ARR disagrees with the model",
         "organiser_direction": "numbers that disagree between the deck and the model",
         "locations": LOC["PF2"],
         "shown": {"value": f["deck_arr"], "unit": "USD", "label": "deck ARR", "details": {"gap_to_model": arr_gap}},
         "true": {"value": f["model_arr"], "unit": "USD", "label": "model ARR_TOTAL", "details": {"recurring_arr": f["true_arr"]}},
         "check": "deck_claim_vs_named_cell",
         "check_description": "Match the deck claim labelled ARR to the named cell ARR_TOTAL.",
         "tolerance": 0.01,
         "files_needed": ["01_overview/pitch_deck.pdf", "02_financials/financial_model.xlsx"],
         "catchable_from_seed_drop": True},
        {"id": "PF2b", "name": "Video ARR disagrees with the deck",
         "organiser_direction": "numbers that disagree between the deck and the model",
         "locations": LOC["PF2b"],
         "shown": {"value": f["video_arr"], "unit": "USD", "label": "spoken ARR, about three million dollars"},
         "true": {"value": f["deck_arr"], "unit": "USD", "label": "deck ARR"},
         "check": "spoken_arr_vs_claims_page",
         "check_description": "Transcribe the video, extract the ARR sentence and compare it with the claims page.",
         "tolerance": 0.01,
         "files_needed": ["01_overview/pitch_video_script.md", "01_overview/pitch_deck.pdf"],
         "catchable_from_seed_drop": True},
        {"id": "PF3", "name": "Churn hidden in the cohort tab",
         "organiser_direction": "churn hidden in cohort charts",
         "locations": LOC["PF3"],
         "shown": {"value": round(f["nrr_rep"], 3), "unit": "ratio", "label": "12-month net revenue retention in the model and deck",
                   "details": {"customers": f["cohort_rep"]}},
         "true": {"value": round(f["nrr_true"], 3), "unit": "ratio", "label": "12-month net revenue retention rebuilt from the customer file",
                  "details": {"gross_revenue_retention": round(f["grr_true"], 3), "customers": f["cohort_true"],
                              "customers_dropped": f["cohort_true"] - f["cohort_rep"]}},
         "check": "rebuild_cohorts_from_customer_file",
         "check_description": "Rebuild the nine 2025 cohorts from customer_mrr_by_month.csv. Compare month-0 counts and net retention with the Cohorts tab. Compute gross retention.",
         "tolerance": 0.005,
         "files_needed": ["02_financials/financial_model.xlsx", "03_metrics/customer_mrr_by_month.csv", "01_overview/pitch_deck.pdf"],
         "catchable_from_seed_drop": False},
        {"id": "PF4", "name": "Burn and runway do not match the hiring plan",
         "organiser_direction": "burn that does not match the hiring plan",
         "locations": LOC["PF4"],
         "shown": {"value": f["runway_shown"], "unit": "months", "label": "runway in the model and deck",
                   "details": {"hires_counted": MODELED_HIRES, "avg_net_burn_first_12_months": round(f["burn_shown"])}},
         "true": {"value": f["runway_true"], "unit": "months", "label": "runway when all 24 planned hires are paid for",
                  "details": {"hires_in_plan": PLANNED_HIRES, "avg_net_burn_first_12_months": round(f["burn_true"])}},
         "check": "payroll_from_hiring_plan_and_rerun_cash",
         "check_description": "Build payroll from hiring_plan.csv times LOAD_FACTOR in Assumptions, rerun the cash plan with the Assumptions settings, and compare runway and burn with Cash_Runway and the deck.",
         "tolerance": 0.01,
         "files_needed": ["05_team/hiring_plan.csv", "02_financials/financial_model.xlsx", "01_overview/pitch_deck.pdf"],
         "catchable_from_seed_drop": True},
        {"id": "PF5", "name": "Customer concentration",
         "organiser_direction": "an additional published flag",
         "locations": LOC["PF5"],
         "shown": {"value": f["claimed_share"], "unit": "ratio", "label": "deck claim: no customer above 9% of ARR"},
         "true": {"value": round(f["big_share"], 3), "unit": "ratio", "label": "largest customer share of MRR (customer C-BIG)",
                  "details": {"top3_share": round(f["top3"], 3)}},
         "check": "top_customer_share",
         "check_description": "Top-one and top-three share of 2026-09 subscription MRR from customer_mrr_by_month.csv; compare with the deck claim.",
         "tolerance": 0.001,
         "files_needed": ["03_metrics/customer_mrr_by_month.csv", "01_overview/pitch_deck.pdf"],
         "catchable_from_seed_drop": False},
        {"id": "PF6", "name": "Gross margin excludes hosting, inference and support",
         "organiser_direction": "an additional published flag",
         "locations": LOC["PF6"],
         "shown": {"value": round(f["gm_shown"], 3), "unit": "ratio", "label": "gross margin in the deck and model"},
         "true": {"value": round(f["gm_true"], 3), "unit": "ratio", "label": "gross margin with hosting, inference, telephony, licences and support in cost of revenue"},
         "check": "gross_margin_from_ledger",
         "check_description": "Add the ledger lines with categories cloud_hosting, model_inference and support_staff to telephony and licences for 2026-09 and recompute gross margin on recurring revenue.",
         "tolerance": 0.002,
         "files_needed": ["02_financials/financial_model.xlsx", "01_overview/pitch_deck.pdf"],
         "files_needed_full_check": ["02_financials/expense_ledger.csv"],
         "catchable_from_seed_drop": True,
         "note": "The seed drop shows the hosting and support rows under R&D and S&M in the P&L. The ledger gives the exact check."},
        {"id": "PF7", "name": "Cumulative sign-ups shown as active clinics",
         "organiser_direction": "an additional published flag",
         "locations": LOC["PF7"],
         "shown": {"value": f["accounts_cum"], "unit": "accounts", "label": "deck clinic count, the last value of accounts_created_cumulative"},
         "true": {"value": f["paying"][LAST], "unit": "accounts", "label": "paying accounts (column paying_accounts)"},
         "check": "cumulative_column_shown_as_active",
         "check_description": "Match the deck clinic count to the last value of the column named accounts_created_cumulative (a column that never decreases) and compare it with paying_accounts. A never-decreasing test alone is not enough: paying_accounts also only rises in this room, so the column name and the deck match are the decisive checks.",
         "tolerance": 0,
         "files_needed": ["03_metrics/monthly_metrics.csv", "01_overview/pitch_deck.pdf"],
         "catchable_from_seed_drop": True},
    ]
    for fl in flags:
        fl["decoy"] = False
        fl["in_seed_drop_files"] = [x for x in fl["files_needed"] if x in SEED_FILES]
    decoys = [
        {"id": "DC1", "name": "Onboarding fee excluded from ARR correctly", "locations": LOC["DC1"], "must_not_flag": True,
         "why": "The $500 one-time fee is shown in ARR_Build with zero ARR counted. A checker must not flag it as ARR."},
        {"id": "DC2", "name": "Annual prepay counted as recurring correctly", "locations": LOC["DC2"], "must_not_flag": True,
         "why": "Brookline Row pays once a year in advance. Revenue is spread monthly and ARR counts it once, at 12 times the monthly price."},
        {"id": "DC3", "name": "Clean cap table", "locations": LOC["DC3"], "must_not_flag": True,
         "why": "Holders add to 100 percent and the SAFE conversion at the stated cap is right."},
    ]
    key = {
        "company": "Hollis Voice (fictional)",
        "synthetic_notice": FOOTER,
        "seed": SEED, "as_of": "2026-09-30",
        "room_path": "data_room/hollis_voice",
        "seed_drop_path": "data_room/hollis_voice_seed_drop",
        "seed_drop_files": SEED_FILES,
        "full_room_files": [r[0] for r in ROOM_FILES],
        "flags": flags, "decoys": decoys,
        "deck_claims": LOC["CLAIMS"],
        "facts": {
            "customers_ever_paying": f["ever"], "paying_accounts": f["paying"][LAST], "mrr_subscription": f["true_mrr"],
            "arr_true_recurring": f["true_arr"], "arr_model": f["model_arr"], "arr_deck": f["deck_arr"], "arr_video": f["video_arr"],
            "ask": SERIES_A, "pre_money": SERIES_A_PRE, "cash": CASH_START, "staff_now": HEADCOUNT_NOW,
            "staff_after_hiring": HEADCOUNT_NOW + PLANNED_HIRES,
            "model_avg_net_burn_12m": round(f["burn_shown"], 2), "true_avg_net_burn_12m": round(f["burn_true"], 2),
        },
        "counts": {"flags": len(flags), "decoys": len(decoys),
                   "flags_catchable_from_seed_drop": sum(1 for x in flags if x["catchable_from_seed_drop"]),
                   "flags_needing_full_room": sum(1 for x in flags if not x["catchable_from_seed_drop"])},
        "notes": [
            "The deck's market figures (28,000 clinics and a $252,000,000 market) are labelled company estimates and are not planted flags.",
            "The company overview and website copy repeat the deck's ARR and clinic count. They are the same planted claims, not new ones.",
            "Founder GitHub handles are placeholders. Replace them with the demo organisation's handle in generate.py (FOUNDER_GITHUB).",
            "The data room gives no cash history, only cash at 2026-09-30, so it does not claim to reconcile cash since inception.",
        ],
    }
    KEY_PATH.write_text(json.dumps(key, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def copy_seed_drop():
    for rel in SEED_FILES:
        dst = SEED_DROP / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOM / rel, dst)


def main():
    ROOM.mkdir(parents=True, exist_ok=True)
    build_facts()
    build_tables()
    build_model()
    build_cap_table()
    build_deck()
    build_cover_note()
    build_overview()
    build_bios()
    build_one_pager()
    build_orders()
    build_markdown()
    build_answer_key()
    copy_seed_drop()
    print(f"Wrote {len(ROOM_FILES)} files to {ROOM}")
    print(f"Wrote {len(SEED_FILES)} files to {SEED_DROP}")
    print(f"Wrote {KEY_PATH}")
    print(f"True recurring ARR {F['true_arr']:,}; model {F['model_arr']:,}; deck {F['deck_arr']:,}; video {F['video_arr']:,}")
    print(f"Runway shown {F['runway_shown']} true {F['runway_true']}; gross margin shown {F['gm_shown']:.3f} true {F['gm_true']:.3f}")


if __name__ == "__main__":
    main()
