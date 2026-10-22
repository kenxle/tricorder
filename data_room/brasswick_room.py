#!/usr/bin/env python3
"""Generate the synthetic Brasswick seed data room for the Tricorder demo.

Everything here is invented. Brasswick, its people, its customers, its vendors and its numbers are fictional.

Run it through generate.py with the room's own virtual environment:

    data_room/.venv/bin/python data_room/generate.py --company brasswick

Outputs:
    data_room/brasswick/                 the seed room (13 files, six folders)
    data_room/answer_key_brasswick.json  every planted flag, decoy and green flag, with locations and numbers

Brasswick is a seed company, so its room is one thin tier and there is no separate seed drop. The Hollis
Voice room is the Series A room. The two rooms carry different kinds of planted flags.

The seed is fixed, so every file comes out byte for byte the same each run. Files are overwritten in
place. Nothing is deleted.
"""
import calendar
import csv
import datetime
import io
import json
import math
import random
import statistics
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
from reportlab.lib.utils import ImageReader, simpleSplit  # noqa: E402
from reportlab.pdfgen import canvas as rl_canvas  # noqa: E402
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOM = HERE / "brasswick"
KEY_PATH = HERE / "answer_key_brasswick.json"
FOOTER = "Synthetic data room for Deal Flow NYC 2026. Not a real company."
COMPANY = "Brasswick, Inc."

SEED = 20261025
N_MONTHS = 17               # 2025-05 .. 2026-09
LAST = N_MONTHS - 1
LTM = list(range(LAST - 11, LAST + 1))    # 2025-10 .. 2026-09
FIRST_2026 = 8                            # index of 2026-01


def mlabel(i):
    """Month label for month index i (0 is 2025-05). Works past the end of the history."""
    k = 2025 * 12 + 4 + i
    return f"{k // 12}-{k % 12 + 1:02d}"


MONTH_LABELS = [mlabel(m) for m in range(N_MONTHS)]


def month_name(i):
    k = 2025 * 12 + 4 + i
    return f"{calendar.month_name[k % 12 + 1]} {k // 12}"


# ---------------------------------------------------------------------------------------------
# The company. Every name below is invented.
# ---------------------------------------------------------------------------------------------
LIST_PRICE = {"Lane": 2_400, "Fleet": 4_800}
ANNUAL_DISCOUNT = 0.10
RECOVERY_FEE = 0.30          # Brasswick keeps 30% of what it recovers; 70% goes back to the broker
BIG_FEE = 11_850

# (name, start month index, first plan, role). Ids follow start order.
CUSTOMER_SPEC = [
    ("Corvane Logistics", 0, "Network", "big"),
    ("Kelderton Freight Partners", 0, "Fleet", "raise"),
    ("Ludgate Transport Brokers", 1, "Lane", "upgrade"),
    ("Pinnock Freight Group", 2, "Lane", "churn"),
    ("Marrowgate Logistics", 3, "Fleet", None),
    ("Ashby Fenwick Freight", 4, "Lane", None),
    ("Varrick Lane Logistics", 5, "Fleet", None),
    ("Quellby Haulage", 7, "Lane", None),
    ("Dunsmore Carriers Brokerage", 8, "Fleet", None),
    ("Tessmore Freight", 9, "Lane", "annual_decoy"),
    ("Hethersett Freight", 11, "Fleet", None),
    ("Wexcombe Logistics", 12, "Lane", None),
    ("Tarrow Brokerage", 13, "Lane", None),
    ("Fennimore Shipping Group", 14, "Fleet", None),
    ("Ostley Freight", 16, "Lane", "annual_sept"),
]
CHURN_AT = 7                 # Pinnock's last paying month is 2025-11
UPGRADE_AT = 11              # Ludgate moves from Lane to Fleet in 2026-04
RAISE_AT = 12                # Kelderton's price rises at its anniversary, 2026-05
OSTLEY_LIST = 2_550          # Lane with the carrier-portal add-on

CEO = {"name": "Celia Brandvold", "title": "Chief Executive Officer and co-founder"}
CTO = {"name": "Marcus Ashdown", "title": "Chief Technology Officer and co-founder"}
SENIOR = [("Lena Haverkamp", "Founding Engineer"), ("Owen Tierney", "Customer Success Lead")]

# Employees: (title, department, start month index, start day, base pay). Department keys: rd, cs, sm, ga.
STAFF = [
    (CEO["title"], "ga", 0, 1, 108_000),
    (CTO["title"], "rd", 0, 1, 104_500),
    ("Founding Engineer", "rd", 0, 12, 157_000),
    ("Customer Success Lead", "cs", 3, 4, 98_500),
    ("Account Executive", "sm", 6, 17, 112_000),
    ("Machine Learning Engineer", "rd", 10, 2, 168_500),
    ("Implementation Specialist", "cs", 13, 8, 86_000),
]
LOAD = 1.22
RAISE_2026 = 1.03            # pay rise in January 2026 for staff hired before it

# Planned hires after the seed: (title, department, plan month, start day, base pay)
HIRES = [
    ("Account Executive", "sm", 2, 3, 118_500),
    ("Senior Machine Learning Engineer", "rd", 3, 1, 176_000),
    ("Customer Success Manager", "cs", 4, 14, 97_500),
    ("Growth Marketing Manager", "sm", 5, 19, 132_000),
    ("Account Executive", "sm", 6, 1, 121_000),
    ("Solutions Engineer", "rd", 8, 9, 142_500),
    ("Backend Engineer", "rd", 10, 6, 161_500),
]

# The contract engineering studio and the labelling contractors (flag BF3), and the fractional controller (decoy DC2).
STUDIO = "Norrgate Software Studio"
SOW1_FEE, SOW2_FEE = 19_800, 26_500
SOW1_START, SOW2_START = 2, 14          # 2025-07 and 2026-07
CONTRACTOR_PAY = "Fernway Contractor Payments"
LABELLERS = ["A. Kirwan", "T. Brennan"]
LABEL_START = 4
CONTROLLER = "Abbotsford Finance Partners"
CONTROLLER_FEE = 2_950
CONTROLLER_START = 6

CASH_START = 641_318
SEED_RAISE = 3_000_000
SEED_PRE = 16_000_000
SEED_MONTH = 2               # plan month 2 (2026-11) is when the seed money lands
SAFES = [("Theodora Vance (angel)", 150_000, 6_000_000, "2025-01"),
         ("Wickham Row Angels LLC", 350_000, 6_000_000, "2025-01")]
SAFE_C_NAME, SAFE_C_CAP, SAFE_C_DATE = "Halyard Pre-Seed Fund I, LP", 12_000_000, "2025-07"
PROF_PLAN = 2_800            # legal and filing fees in the plan
PROGRAMS = 30_000            # marketing programs a month once the seed lands
OFFICE_STEP = (7, 3_900)     # plan month 7: a larger office, rent and other up by this much
PLAN_HORIZON = 48
GROWTH = (0.03, 0.015, 0.01)   # plan growth a month: months 1-12, 13-24, after

MARKET_BROKERS = 3_600
MARKET_ACV = 54_000
MARKET_TAM = MARKET_BROKERS * MARKET_ACV

F = {}                       # every fact, filled by build_facts()
LOC = defaultdict(list)      # answer-key locations by flag, decoy and green flag id


def money(n):
    return f"${n:,.0f}"


def pct(x, d=0):
    return f"{x * 100:.{d}f}%"


# ---------------------------------------------------------------------------------------------
# Customers, revenue and recoveries
# ---------------------------------------------------------------------------------------------
def build_customers(rng):
    customers = []
    for i, (name, start, plan, role) in enumerate(CUSTOMER_SPEC):
        c = {"id": f"C{1001 + i}", "name": name, "start": start, "plan0": plan, "role": role,
             "end": CHURN_AT if role == "churn" else N_MONTHS,
             "fee": [0] * N_MONTHS, "plans": [None] * N_MONTHS, "annual": role in ("annual_decoy", "annual_sept")}
        if role == "big":
            fee = BIG_FEE
        elif role == "annual_decoy":
            fee = round(LIST_PRICE["Lane"] * (1 - ANNUAL_DISCOUNT))
        elif role == "annual_sept":
            fee = round(OSTLEY_LIST * (1 - ANNUAL_DISCOUNT))
        else:
            mult = rng.choice([0.9, 0.95, 1.0, 1.0, 1.05, 1.1, 1.15]) * (1 + rng.uniform(-0.02, 0.02))
            fee = int(round(LIST_PRICE[plan] * mult / 5) * 5)
        plan_now = plan
        for m in range(start, c["end"]):
            if role == "upgrade" and m == UPGRADE_AT:
                plan_now = "Fleet"
                fee = int(round(LIST_PRICE["Fleet"] * 0.95 / 5) * 5)
            if role == "raise" and m == RAISE_AT:
                fee = int(round(fee * 1.06 / 5) * 5)
            c["fee"][m] = fee
            c["plans"][m] = plan_now
        customers.append(c)
    return customers


def build_recoveries(customers, rng):
    """Carrier invoices audited and money recovered, per customer and month. The four months after a broker
    joins hold a back-audit of the invoices it paid before; after that recoveries settle."""
    for c in customers:
        base_fee = next(f for f in c["fee"] if f)
        inv_rate = rng.uniform(1.10, 1.50)
        steady = rng.uniform(0.40, 0.70)
        back = base_fee * (rng.uniform(6.0, 8.0) if c["start"] <= 4 else rng.uniform(1.5, 2.5))
        c["invoices"] = [0] * N_MONTHS
        c["recovered"] = [0.0] * N_MONTHS
        for m in range(c["start"], c["end"]):
            ramp = 0.55 if m == c["start"] else 1.0
            c["invoices"][m] = round(c["fee"][m] * inv_rate * ramp * (1 + rng.gauss(0, 0.05)))
            if m == c["start"]:
                continue
            amt = c["fee"][m] * steady * (1 + rng.gauss(0, 0.05))
            k = m - c["start"]
            if k <= 4:
                amt += back * (0.2, 0.3, 0.3, 0.2)[k - 1]
            c["recovered"][m] = round(amt, 2)


def shown_total(customers):
    """Total revenue as the P&L states it: subscription revenue (with the September annual invoice booked
    whole, flag BF4) plus recoveries at their gross amount (flag BF1)."""
    out = []
    for m in range(N_MONTHS):
        sub = sum(c["fee"][m] for c in customers)
        if m == LAST:
            o = next(c for c in customers if c["role"] == "annual_sept")
            sub += 12 * o["fee"][m] - o["fee"][m]
        out.append(sub + sum(c["recovered"][m] for c in customers))
    return out


def history_shape_ok(total):
    rising = all(total[m] > total[m - 1] for m in range(FIRST_2026 + 1, N_MONTHS))
    hidden_peak = max(total[:FIRST_2026])
    return rising and hidden_peak >= 1.12 * total[FIRST_2026]


# ---------------------------------------------------------------------------------------------
# Costs: the expense ledger
# ---------------------------------------------------------------------------------------------
def staff_at(m):
    return [s for s in STAFF if s[2] <= m]


def build_ledger(customers, lr):
    rows = []

    def add(m, day, vendor, desc, cat, booked, amt):
        rows.append((MONTH_LABELS[m], f"{MONTH_LABELS[m]}-{day:02d}", vendor, desc, cat, booked, round(amt, 2)))

    factors = {s[0]: 1.0 for s in STAFF}
    booked_dept = {"rd": ("payroll_engineering", "R&D", "Engineering, salaries and benefits"),
                   "cs": ("payroll_customer_success", "Cost of revenue", "Customer success and implementation, salaries and benefits"),
                   "sm": ("payroll_sales", "S&M", "Sales, salaries and benefits"),
                   "ga": ("payroll_g_and_a", "G&A", "General and administrative, salaries and benefits")}
    for m in range(N_MONTHS):
        last_day = calendar.monthrange(int(MONTH_LABELS[m][:4]), int(MONTH_LABELS[m][5:]))[1]
        invoices = sum(c["invoices"][m] for c in customers)
        # Payroll by department, two runs a month. A person who starts mid-month is paid for the days worked.
        dept = defaultdict(float)
        for (title, dk, s0, sday, base) in staff_at(m):
            rise = RAISE_2026 if (m >= FIRST_2026 and s0 < FIRST_2026) else 1.0
            share = 1.0 if m > s0 else (last_day - sday + 1) / last_day
            dept[dk] += base * LOAD / 12 * rise * share * factors[title]
        for dk in ("rd", "cs", "sm", "ga"):
            if dept[dk] <= 0:
                continue
            cat, booked, desc = booked_dept[dk]
            total = dept[dk] * (1 + (0 if m == LAST else lr.gauss(0, 0.01)))
            first = round(total * (0.5 + lr.gauss(0, 0.003)), 2)
            add(m, 15, "Gristmill Payroll", desc + " (first run)", cat, booked, first)
            add(m, last_day, "Gristmill Payroll", desc + " (second run)", cat, booked, round(total - first, 2))
        # Delivery costs
        add(m, lr.randint(2, 6), "Ferrous Cloud Services", "Cloud compute, storage and database", "cloud_hosting", "Cost of revenue",
            (1_150 + 0.019 * invoices) * (1 + lr.gauss(0, 0.04)))
        add(m, lr.randint(8, 14), "Lantern Document AI", "Document reading API, pages processed", "document_ai", "Cost of revenue",
            0.034 * invoices * (1 + lr.gauss(0, 0.05)))
        add(m, lr.randint(9, 16), "Velloway Language API", "Language model API usage", "language_model_api", "Cost of revenue",
            0.022 * invoices * (1 + lr.gauss(0, 0.06)))
        # Recovery remittances: 70% of what was recovered for each broker goes back to it
        for c in customers:
            if c["recovered"][m] > 0:
                fee = round(c["recovered"][m] * RECOVERY_FEE, 2)
                add(m, lr.randint(12, 22), c["name"], "Remittance of carrier refunds recovered for the customer",
                    "recovery_remittance", "Cost of revenue", round(c["recovered"][m] - fee, 2))
        # Contract engineering and labelling (BF3): booked as professional services under G&A
        if m >= SOW1_START:
            sow, fee = ("SOW 2", SOW2_FEE) if m >= SOW2_START else ("SOW 1", SOW1_FEE)
            add(m, lr.randint(1, 5), STUDIO, f"Contract engineering, {sow}, {month_name(m)}", "professional_services", "G&A", fee)
            if m != LAST and lr.random() < 0.3:
                add(m, lr.randint(20, 27), STUDIO, f"Additional engineering hours, {month_name(m)}", "professional_services", "G&A",
                    lr.uniform(1_200, 4_800))
        if m >= LABEL_START:
            for who in LABELLERS:
                add(m, lr.randint(25, last_day), CONTRACTOR_PAY, f"Contractor payout: invoice labelling, {who}", "professional_services", "G&A",
                    lr.uniform(3_100, 4_600))
        if lr.random() < 0.6 or m in (0, 9):
            add(m, lr.randint(6, 24), "Thistlewood Legal LLP", "Legal and filing fees", "professional_services", "G&A",
                lr.uniform(900, 2_400) if m not in (0, 9) else lr.uniform(6_000, 9_500))
        # Fractional controller (decoy DC2): a contractor the plan does keep
        if m >= CONTROLLER_START:
            add(m, lr.randint(1, 3), CONTROLLER, "Fractional controller, monthly retainer", "accounting", "G&A", CONTROLLER_FEE)
            if m == 10:
                add(m, 20, CONTROLLER, "2025 tax returns and year-end close", "accounting", "G&A", 3_400)
        # Office and other
        add(m, 1, "Dockyard Commons Workspace", "Office rent", "rent", "G&A", 2_150.00 if m < 8 else 4_680.00)
        add(m, lr.randint(1, 7), "Tallyhouse Tools", "Software subscriptions and tools", "tools", "G&A",
            (420 + 165 * len(staff_at(m))) * (1 + lr.gauss(0, 0.05)))
        add(m, lr.randint(1, 5), "Ravelston Insurance Brokers", "Insurance premiums", "insurance", "G&A", (640 if m < 8 else 910) * (1 + lr.gauss(0, 0.02)))
        add(m, lr.randint(5, 26), "Gullwing Travel", "Travel to customers and freight conferences", "travel", "G&A", lr.uniform(350, 3_800))
        add(m, lr.randint(1, 28), "Brimley Office Supply", "Office supplies and team meals", "other", "G&A", lr.uniform(150, 900))
    rows.sort(key=lambda r: (r[0], r[1], r[2], r[3]))
    return rows


# ---------------------------------------------------------------------------------------------
# The forward plan
# ---------------------------------------------------------------------------------------------
def forecast(with_contractors):
    sub = F["contracted_mrr"]
    rec = statistics.mean(F["recovered_total"][LAST - 2:])
    infra0 = F["pl"]["host"][LAST] + F["pl"]["apis"][LAST]
    dept = {dk: F["pl_payroll"][dk][LAST] for dk in ("rd", "cs", "sm", "ga")}
    other = F["other_plan"]
    contractors = F["contractor_rate"] if with_contractors else 0.0
    cash = CASH_START
    rows, runway = [], None
    for t in range(1, PLAN_HORIZON + 1):
        g = GROWTH[0] if t <= 12 else GROWTH[1] if t <= 24 else GROWTH[2]
        sub *= 1 + g
        rec *= 1 + g
        for (_title, dk, st, _day, base) in HIRES:
            if st == t:
                dept[dk] += base * LOAD / 12
        remit = (1 - RECOVERY_FEE) * rec
        infra = infra0 * sub / F["contracted_mrr"]
        prof = PROF_PLAN + contractors
        prog = PROGRAMS if t >= SEED_MONTH else 0
        oth = other + (OFFICE_STEP[1] if t >= OFFICE_STEP[0] else 0)
        payroll = sum(dept.values())
        revenue = sub + rec
        costs = remit + infra + payroll + prof + CONTROLLER_FEE + prog + oth
        burn = costs - revenue
        raised = SEED_RAISE if t == SEED_MONTH else 0
        cash += raised - burn
        rows.append({"t": t, "label": mlabel(LAST + t), "sub": sub, "rec": rec, "remit": remit, "infra": infra,
                     "dept": dict(dept), "payroll": payroll, "prof": prof, "acct": CONTROLLER_FEE, "prog": prog, "other": oth,
                     "revenue": revenue, "costs": costs, "burn": burn, "raised": raised, "cash": cash,
                     "heads": len(STAFF) + sum(1 for h in HIRES if h[2] <= t)})
        if cash <= 0 and runway is None:
            runway = t - 1
    return rows, (runway if runway is not None else PLAN_HORIZON)


# ---------------------------------------------------------------------------------------------
# Facts
# ---------------------------------------------------------------------------------------------
def build_facts():
    rng = random.Random(SEED)
    customers = build_customers(rng)
    for attempt in range(3000):
        build_recoveries(customers, random.Random(SEED + 101 + 7919 * attempt))
        if history_shape_ok(shown_total(customers)):
            break
    else:
        sys.exit("No noise stream gives a revenue history with the planted shape")
    F["noise_attempt"] = attempt
    F["customers"] = customers
    big = next(c for c in customers if c["role"] == "big")
    ostley = next(c for c in customers if c["role"] == "annual_sept")
    tess = next(c for c in customers if c["role"] == "annual_decoy")
    F["big"], F["ostley"], F["tess"] = big, ostley, tess

    sub_true = [sum(c["fee"][m] for c in customers) for m in range(N_MONTHS)]
    recovered = [round(sum(c["recovered"][m] for c in customers), 2) for m in range(N_MONTHS)]
    fees = [[round(c["recovered"][m] * RECOVERY_FEE, 2) for m in range(N_MONTHS)] for c in customers]
    remitted = [[round(c["recovered"][m] - fees[i][m], 2) for m in range(N_MONTHS)] for i, c in enumerate(customers)]
    for i, c in enumerate(customers):
        c["recovery_fee"], c["remitted"] = fees[i], remitted[i]
    fee_total = [round(sum(c["recovery_fee"][m] for c in customers), 2) for m in range(N_MONTHS)]
    remit_total = [round(sum(c["remitted"][m] for c in customers), 2) for m in range(N_MONTHS)]
    ostley_gap = 12 * ostley["fee"][LAST] - ostley["fee"][LAST]
    sub_shown = [sub_true[m] + (ostley_gap if m == LAST else 0) for m in range(N_MONTHS)]
    total_shown = [round(sub_shown[m] + recovered[m], 2) for m in range(N_MONTHS)]
    paying = [sum(1 for c in customers if c["fee"][m] > 0) for m in range(N_MONTHS)]
    invoices = [sum(c["invoices"][m] for c in customers) for m in range(N_MONTHS)]
    F.update(sub_true=sub_true, sub_shown=sub_shown, recovered_total=recovered, fee_total=fee_total, remit_total=remit_total,
             total_shown=total_shown, paying=paying, invoices=invoices, ostley_gap=ostley_gap,
             invoices_cum=[sum(invoices[:m + 1]) for m in range(N_MONTHS)])
    F["contracted_mrr"] = sub_true[LAST]
    F["ever"] = len(customers)
    F["big_share"] = BIG_FEE / sub_true[LAST]
    # Deferred revenue at the data date: the months of Tessmore's annual plan paid for and not yet delivered
    F["tess_months_left"] = tess["start"] + 12 - N_MONTHS
    F["deferred"] = tess["fee"][LAST] * F["tess_months_left"]

    # The ledger and the P&L lines it gives
    ledger = build_ledger(customers, random.Random(SEED + 20))
    F["ledger"] = ledger
    by = defaultdict(float)
    for (label, _d, _v, _desc, cat, _b, amt) in ledger:
        by[(label, cat)] += amt

    def series(*cats):
        return [round(sum(by[(MONTH_LABELS[m], c)] for c in cats), 2) for m in range(N_MONTHS)]

    pl = {
        "remit": series("recovery_remittance"), "host": series("cloud_hosting"),
        "apis": series("document_ai", "language_model_api"), "cs": series("payroll_customer_success"),
        "p_rd": series("payroll_engineering"), "p_sm": series("payroll_sales"), "p_ga": series("payroll_g_and_a"),
        "prof": series("professional_services"), "acct": series("accounting"),
        "other": series("rent", "tools", "insurance", "travel", "other"),
    }
    F["pl"] = pl
    F["pl_payroll"] = {"rd": pl["p_rd"], "cs": pl["cs"], "sm": pl["p_sm"], "ga": pl["p_ga"]}
    assert all(abs(pl["remit"][m] - remit_total[m]) < 0.05 for m in range(N_MONTHS)), "remittances differ from the customer file"
    costs = [round(sum(pl[k][m] for k in pl), 2) for m in range(N_MONTHS)]
    F["costs"] = costs
    F["op"] = [round(total_shown[m] - costs[m], 2) for m in range(N_MONTHS)]
    F["net_loss_actual"] = round(-sum(F["op"]), 2)
    F["heads"] = [len(staff_at(m)) for m in range(N_MONTHS)]

    # Contractors in September (flag BF3) and the fractional controller (decoy DC2)
    sept = [r for r in ledger if r[0] == MONTH_LABELS[LAST]]
    F["studio_sept"] = round(sum(r[6] for r in sept if r[2] == STUDIO), 2)
    F["labellers_sept"] = round(sum(r[6] for r in sept if r[2] == CONTRACTOR_PAY), 2)
    F["contractor_rate"] = round(F["studio_sept"] + F["labellers_sept"], 2)
    F["legal_sept"] = round(sum(r[6] for r in sept if r[2] == "Thistlewood Legal LLP"), 2)
    F["other_plan"] = round(statistics.mean(pl["other"][LAST - 2:]), -2)

    # Plan: as the model shows it, and with the contractors kept on
    F["fc_shown"], F["runway_shown"] = forecast(False)
    F["fc_true"], F["runway_true"] = forecast(True)
    F["burn_shown"] = sum(r["burn"] for r in F["fc_shown"][:12]) / 12
    F["burn_true"] = sum(r["burn"] for r in F["fc_true"][:12]) / 12

    # Revenue claims
    F["ltm_shown"] = round(sum(total_shown[m] for m in LTM), 2)
    F["ltm_remitted"] = round(sum(remit_total[m] for m in LTM), 2)
    F["ltm_net_of_pass_through"] = round(F["ltm_shown"] - F["ltm_remitted"], 2)
    F["ltm_true_net"] = round(sum(sub_true[m] + fee_total[m] for m in LTM), 2)
    F["ltm_recovered"] = round(sum(recovered[m] for m in LTM), 2)
    hidden = total_shown[:FIRST_2026]
    F["hidden_peak"] = max(hidden)
    F["hidden_peak_month"] = MONTH_LABELS[hidden.index(F["hidden_peak"])]
    F["jan_2026"] = total_shown[FIRST_2026]
    F["drop_from_peak"] = 1 - F["jan_2026"] / F["hidden_peak"]

    # Money raised and the cash bridge
    safe_ab = sum(s[1] for s in SAFES)
    target_pre = 120_000
    safe_c = math.ceil((F["net_loss_actual"] - F["deferred"] + CASH_START + target_pre - safe_ab) / 50_000) * 50_000
    F["safe_c"] = safe_c
    F["raised_total"] = safe_ab + safe_c
    F["net_loss_pre"] = round(F["raised_total"] - CASH_START - F["net_loss_actual"] + F["deferred"])
    F["bridge_cash"] = F["raised_total"] - F["net_loss_pre"] - F["net_loss_actual"] + F["deferred"]
    F["bridge_diff"] = round(F["bridge_cash"] - CASH_START, 2)
    check_plants_are_material()


def check_plants_are_material():
    problems = []
    if F["ltm_remitted"] / F["ltm_net_of_pass_through"] <= 0.15:
        problems.append("BF1 (pass-through money is under 15% of net revenue)")
    if F["drop_from_peak"] < 0.10:
        problems.append("BF2 (the hidden fall is under 10%)")
    if F["runway_shown"] - F["runway_true"] < 3 or F["runway_shown"] >= PLAN_HORIZON:
        problems.append("BF3 (runway gap under 3 months, or the plan never runs out)")
    if F["ostley_gap"] / F["contracted_mrr"] <= 0.10:
        problems.append("BF4 (the annual invoice moves MRR by 10% or less)")
    if not 50_000 <= F["net_loss_pre"] <= 250_000:
        problems.append(f"the loss before 2025-05 is {F['net_loss_pre']:,}")
    if abs(F["bridge_diff"]) >= 1:
        problems.append("the cash bridge is off by a dollar or more")
    if problems:
        sys.exit("The Brasswick room does not hold together: " + "; ".join(problems))


# ---------------------------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------------------------
def write_csv(rel, header, rows):
    path = ROOM / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    w.writerows(rows)
    path.write_bytes(buf.getvalue().encode("utf-8"))


def write_text(rel, text):
    path = ROOM / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def c2(x):
    return f"{x:.2f}"


METRICS = "03_metrics/monthly_metrics.csv"
CUST = "03_metrics/revenue_by_customer.csv"
LEDGER = "02_financials/expense_ledger.csv"
MODEL = "02_financials/financial_model.xlsx"
CAP = "02_financials/cap_table.xlsx"
DECK = "01_overview/pitch_deck.pdf"
CLAIMS_SIDECAR = "01_overview/claims.json"
COVER = "00_welcome/cover_note_and_index.pdf"
BIOS = "05_team/founder_bios.pdf"


def build_tables():
    customers = F["customers"]
    rows = []
    for m in range(N_MONTHS):
        for c in customers:
            if c["fee"][m] <= 0:
                continue
            if c["annual"]:
                billed = 12 * c["fee"][m] if m == c["start"] else 0
            else:
                billed = c["fee"][m]
            rows.append((MONTH_LABELS[m], c["id"], c["name"], c["plans"][m], c["fee"][m], billed, c["invoices"][m],
                         c2(c["recovered"][m]), c2(c["recovery_fee"][m]), c2(c["remitted"][m])))
    write_csv(CUST, ["month", "customer_id", "customer_name", "plan", "subscription_revenue", "billings", "carrier_invoices_audited",
                     "recovered_from_carriers", "recovery_fee", "remitted_to_customer"], rows)

    rows = []
    for m in range(N_MONTHS):
        rows.append((MONTH_LABELS[m], c2(F["total_shown"][m]), F["sub_shown"][m], c2(F["recovered_total"][m]), F["paying"][m],
                     F["invoices"][m], F["invoices_cum"][m]))
    write_csv(METRICS, ["month", "total_revenue", "subscription_revenue", "recovery_revenue", "paying_brokers",
                        "carrier_invoices_audited", "carrier_invoices_audited_since_launch"], rows)
    LOC["BF4"].append({"file": METRICS, "row_key": {"month": MONTH_LABELS[LAST]}, "column": "subscription_revenue",
                       "expect": F["sub_shown"][LAST], "label": "metrics subscription revenue, 2026-09, with the annual invoice booked whole"})
    LOC["BF2"].append({"file": METRICS, "row_key": {"month": MONTH_LABELS[0]}, "column": "total_revenue",
                       "expect": round(F["total_shown"][0], 2), "label": "first month of revenue in the metrics export"})
    LOC["BF2"].append({"file": METRICS, "row_key": {"month": F["hidden_peak_month"]}, "column": "total_revenue",
                       "expect": round(F["hidden_peak"], 2), "label": "highest month before the deck's chart begins"})
    LOC["DC3"].append({"file": METRICS, "row_key": {"month": MONTH_LABELS[LAST]}, "column": "carrier_invoices_audited_since_launch",
                       "expect": F["invoices_cum"][LAST], "label": "cumulative column, labelled as such"})

    write_csv(LEDGER, ["month", "date", "vendor", "description", "category", "booked_as", "amount_usd"],
              [(a, b, c, d, e, f, c2(amt)) for (a, b, c, d, e, f, amt) in F["ledger"]])
    GREEN_LOCS["GF2"].append({"file": CUST, "count_rows": {"month": MONTH_LABELS[LAST]}, "where_positive": "subscription_revenue",
                              "value": F["paying"][LAST], "label": "customers with subscription revenue in 2026-09"})
    GREEN_LOCS["GF3"].append({"file": CUST, "row_key": {"month": MONTH_LABELS[LAST], "customer_id": F["big"]["id"]},
                              "column": "subscription_revenue", "value": BIG_FEE, "label": "largest customer's September revenue"})


GREEN_LOCS = defaultdict(list)


# ---------------------------------------------------------------------------------------------
# Workbooks
# ---------------------------------------------------------------------------------------------
def new_workbook(rel):
    path = ROOM / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    wb = xlsxwriter.Workbook(str(path))
    wb.set_properties({"title": path.stem, "author": "Brasswick (synthetic)", "company": "Brasswick (synthetic)",
                       "comments": FOOTER, "created": datetime.datetime(2026, 10, 2, 9, 0, 0)})
    return wb


def formats(wb):
    f = {}
    ink = "#22262E"
    f["title"] = wb.add_format({"bold": True, "font_size": 14})
    f["bold"] = wb.add_format({"bold": True})
    f["head"] = wb.add_format({"bold": True, "bg_color": ink, "font_color": "#FFFFFF", "align": "center"})
    f["headl"] = wb.add_format({"bold": True, "bg_color": ink, "font_color": "#FFFFFF"})
    f["sect"] = wb.add_format({"bold": True, "bg_color": "#F1EADB"})
    f["usd"] = wb.add_format({"num_format": "#,##0"})
    f["usd2"] = wb.add_format({"num_format": "#,##0.00"})
    f["usdb"] = wb.add_format({"num_format": "#,##0", "bold": True, "top": 1})
    f["pct"] = wb.add_format({"num_format": "0.0%"})
    f["pct2"] = wb.add_format({"num_format": "0.00%"})
    f["pctb"] = wb.add_format({"num_format": "0.0%", "bold": True})
    f["int"] = wb.add_format({"num_format": "#,##0"})
    f["intb"] = wb.add_format({"num_format": "#,##0", "bold": True, "top": 1})
    f["dec"] = wb.add_format({"num_format": "0.0000"})
    f["note"] = wb.add_format({"italic": True, "font_color": "#555555"})
    f["name"] = wb.add_format({"bold": True, "bg_color": "#FFF4CC", "num_format": "#,##0"})
    f["namep"] = wb.add_format({"bold": True, "bg_color": "#FFF4CC", "num_format": "0.0%"})
    f["namet"] = wb.add_format({"bold": True, "bg_color": "#FFF4CC"})
    return f


def a1(row, col):
    return xlsxwriter.utility.xl_rowcol_to_cell(row, col)


def col_name(col):
    return xlsxwriter.utility.xl_col_to_name(col)


def build_model():
    wb = new_workbook(MODEL)
    fm = formats(wb)

    def reg(fid, sheet, cell, name=None, expect=None, label=None):
        e = {"file": MODEL, "sheet": sheet, "cell": cell}
        if name:
            e["named_cell"] = name
        if expect is not None:
            e["expect"] = expect
        if label:
            e["label"] = label
        LOC[fid].append(e)

    ws_readme = wb.add_worksheet("README")
    ws_ass = wb.add_worksheet("Assumptions")
    ws_pl = wb.add_worksheet("P&L")
    ws_rev = wb.add_worksheet("Revenue_Build")
    ws_team = wb.add_worksheet("Team")
    ws_cash = wb.add_worksheet("Cash_Runway")
    ws_bridge = wb.add_worksheet("Cash_Bridge")

    # ---- README
    ws_readme.set_column(0, 0, 112)
    lines = [
        ("Brasswick: financial model", "title"),
        ("Data as of 2026-09-30. All figures in US dollars. Actual months 2025-05 to 2026-09. Plan months 2026-10 onward.", None),
        ("", None),
        ("Tabs", "bold"),
        ("Assumptions: the inputs the plan uses.", None),
        ("P&L: monthly income statement, 17 months of actuals and 12 months of plan.", None),
        ("Revenue_Build: subscription revenue by broker in September 2026.", None),
        ("Team: employees today and the hires the seed pays for.", None),
        ("Cash_Runway: monthly cash and the number of months the cash lasts.", None),
        ("Cash_Bridge: money raised, less losses since the company began, to cash at the data date.", None),
        ("", None),
        ("Definitions", "bold"),
        ("Subscription revenue: platform fees for the month. Brokers pay by monthly load volume.", None),
        ("Recovery revenue: money recovered from carriers for overbilled invoices. The broker's share is paid back to it and sits in cost of revenue.", None),
        ("MRR: subscription revenue booked in the month.", None),
        ("Runway: the number of months after 2026-09-30 in which cash stays above zero.", None),
        ("", None),
        (FOOTER, "note"),
    ]
    for r, (txt, style) in enumerate(lines):
        ws_readme.write(r, 0, txt, fm[style] if style else None)

    # ---- Assumptions
    ws_ass.set_column(0, 0, 50)
    ws_ass.set_column(1, 1, 16)
    ws_ass.set_column(2, 2, 92)
    ws_ass.write(0, 0, "Assumptions", fm["title"])
    ws_ass.write(1, 0, "Cells with a yellow fill are named cells.", fm["note"])
    ws_ass.write_row(3, 0, ["Input", "Value", "Note"], fm["headl"])
    assum = [
        ("AS_OF_DATE", "Data date", "2026-09-30", "namet", "Last day of the last actual month."),
        ("CASH_START", "Cash at the data date (USD)", CASH_START, "name", "Bank balance at 2026-09-30."),
        ("LOAD_FACTOR", "Loaded cost factor on base pay", LOAD, "name", "Base pay times this factor gives payroll cost with taxes and benefits."),
        ("GROWTH_Y1", "Revenue growth a month, plan months 1 to 12", GROWTH[0], "namep", "Subscription and recovery revenue."),
        ("GROWTH_Y2", "Revenue growth a month, plan months 13 to 24", GROWTH[1], "namep", ""),
        ("GROWTH_LATER", "Revenue growth a month, after plan month 24", GROWTH[2], "namep", ""),
        ("RECOVERY_FEE_SHARE", "Brasswick's share of money recovered", RECOVERY_FEE, "namep",
         "The rest is paid to the broker and booked in cost of revenue."),
        ("PROF_SERVICES_USD_MONTH", "Professional services (USD a month)", PROF_PLAN, "name", "Legal and filing fees. Held flat."),
        ("ACCOUNTING_USD_MONTH", "Accounting (USD a month)", CONTROLLER_FEE, "name", "Fractional controller retainer. Held flat."),
        ("PROGRAMS_USD_MONTH", "Marketing programs after the seed (USD a month)", PROGRAMS, "name", "Starts the month the seed closes."),
        ("OTHER_USD_MONTH", "Rent, tools, insurance, travel and other (USD a month)", F["other_plan"], "name",
         f"Rises by {money(OFFICE_STEP[1])} from plan month {OFFICE_STEP[0]} for a larger office."),
        ("SEED_RAISE", "Seed raise (USD)", SEED_RAISE, "name", "Priced seed round."),
        ("SEED_PRE_MONEY", "Seed pre-money valuation (USD)", SEED_PRE, "name", "See the cap table."),
        ("SEED_PLAN_MONTH", "Plan month the seed cash arrives", SEED_MONTH, "name", "Plan month 1 is 2026-10."),
        ("RAISED_SAFE_2025_01", "Raised in 2025-01: angel SAFEs (USD)", sum(s[1] for s in SAFES), "name", "Two SAFEs. See the cap table."),
        ("RAISED_SAFE_2025_07", "Raised in 2025-07: pre-seed SAFE (USD)", F["safe_c"], "name", "One SAFE. See the cap table."),
        ("NET_LOSS_BEFORE_2025_05", "Net loss before 2025-05 (USD)", F["net_loss_pre"], "name", "Spend before the first paying broker. Cash_Bridge ties this to cash."),
    ]
    ASS = {}
    for i, (nm, label, val, fmt, note) in enumerate(assum):
        r = 4 + i
        ws_ass.write(r, 0, label)
        ws_ass.write(r, 1, val, fm[fmt])
        if note:
            ws_ass.write(r, 2, note, fm["note"])
        wb.define_name(nm, f"=Assumptions!$B${r + 1}")
        ASS[nm] = f"B{r + 1}"
    ws_ass.write(4 + len(assum) + 1, 0, FOOTER, fm["note"])
    reg("BF3", "Assumptions", ASS["PROF_SERVICES_USD_MONTH"], name="PROF_SERVICES_USD_MONTH", expect=PROF_PLAN,
        label="plan professional services: legal only")
    LOC["DC2"].append({"file": MODEL, "sheet": "Assumptions", "cell": ASS["ACCOUNTING_USD_MONTH"], "named_cell": "ACCOUNTING_USD_MONTH",
                       "expect": CONTROLLER_FEE, "label": "plan keeps the fractional controller"})
    GREEN_LOCS["GF1"].append({"file": MODEL, "sheet": "Assumptions", "cell": ASS["SEED_RAISE"], "named_cell": "SEED_RAISE",
                              "value": SEED_RAISE, "label": "seed raise in the model"})
    F["ass_cell"] = ASS

    # ---- P&L
    n_plan = 12
    n_cols = N_MONTHS + n_plan
    ws_pl.set_column(0, 0, 46)
    ws_pl.set_column(1, 1, 9)
    ws_pl.set_column(2, 1 + n_cols, 11)
    ws_pl.freeze_panes(5, 2)
    ws_pl.write(0, 0, "Brasswick: income statement and 12-month plan (USD)", fm["title"])
    ws_pl.write(1, 0, "Actual through 2026-09. Plan from 2026-10.", fm["note"])
    ws_pl.write(3, 0, "Line", fm["headl"])
    ws_pl.write(3, 1, "Section", fm["headl"])
    ws_pl.write(4, 0, "", fm["headl"])
    ws_pl.write(4, 1, "", fm["headl"])
    for j in range(n_cols):
        ws_pl.write(3, 2 + j, mlabel(j), fm["head"])
        ws_pl.write(4, 2 + j, "Actual" if j < N_MONTHS else "Plan", fm["head"])
    layout = [
        ("sec_rev", "Revenue", "", "sect"),
        ("sub", "Subscription revenue", "Revenue", None),
        ("rec", "Recovery revenue", "Revenue", None),
        ("tot", "Total revenue", "Revenue", None),
        ("sec_cogs", "Cost of revenue", "", "sect"),
        ("remit", "Recoveries paid to customers", "COGS", None),
        ("host", "Cloud hosting", "COGS", None),
        ("apis", "Document and language model APIs", "COGS", None),
        ("cs", "Payroll: customer success and implementation", "COGS", None),
        ("cogs", "Total cost of revenue", "COGS", None),
        ("gp", "Gross profit", "", None),
        ("gm", "Gross margin", "", None),
        ("sec_opex", "Operating expenses", "", "sect"),
        ("p_rd", "Payroll: engineering", "R&D", None),
        ("p_sm", "Payroll: sales and marketing", "S&M", None),
        ("prog", "Marketing programs", "S&M", None),
        ("p_ga", "Payroll: general and administrative", "G&A", None),
        ("prof", "Professional services", "G&A", None),
        ("acct", "Accounting", "G&A", None),
        ("other", "Rent, tools, insurance, travel and other", "G&A", None),
        ("opex", "Total operating expenses", "", None),
        ("op", "Operating result", "", None),
        ("sec_memo", "Memo", "", "sect"),
        ("payroll", "Payroll", "Memo", None),
        ("burn", "Net burn (negative of operating result)", "Memo", None),
        ("heads", "Employees at month end", "Memo", None),
    ]
    R = {}
    for i, (key, label, sec, style) in enumerate(layout):
        R[key] = 5 + i
        ws_pl.write(R[key], 0, label, fm[style] if style else None)
        ws_pl.write(R[key], 1, sec, fm[style] if style else None)
        if style == "sect":
            for j in range(n_cols):
                ws_pl.write(R[key], 2 + j, "", fm["sect"])
    pl = F["pl"]
    host_share = pl["host"][LAST] / (pl["host"][LAST] + pl["apis"][LAST])
    V = {}
    for j in range(n_cols):
        if j < N_MONTHS:
            v = {"sub": F["sub_shown"][j], "rec": F["recovered_total"][j], "remit": pl["remit"][j], "host": pl["host"][j],
                 "apis": pl["apis"][j], "cs": pl["cs"][j], "p_rd": pl["p_rd"][j], "p_sm": pl["p_sm"][j], "prog": 0,
                 "p_ga": pl["p_ga"][j], "prof": pl["prof"][j], "acct": pl["acct"][j], "other": pl["other"][j]}
        else:
            r_ = F["fc_shown"][j - N_MONTHS]
            v = {"sub": round(r_["sub"], 2), "rec": round(r_["rec"], 2), "remit": round(r_["remit"], 2),
                 "host": round(r_["infra"] * host_share, 2), "apis": round(r_["infra"] * (1 - host_share), 2),
                 "cs": round(r_["dept"]["cs"], 2), "p_rd": round(r_["dept"]["rd"], 2), "p_sm": round(r_["dept"]["sm"], 2),
                 "prog": r_["prog"], "p_ga": round(r_["dept"]["ga"], 2), "prof": r_["prof"], "acct": r_["acct"], "other": r_["other"]}
        c = 2 + j
        col = lambda key, c=c: a1(R[key], c)
        for key in ("sub", "rec", "remit", "host", "apis", "cs", "p_rd", "p_sm", "prog", "p_ga", "prof", "acct", "other"):
            ws_pl.write_number(R[key], c, v[key], fm["usd"])
        tot = v["sub"] + v["rec"]
        ws_pl.write_formula(R["tot"], c, f"={col('sub')}+{col('rec')}", fm["usdb"], tot)
        cogs_k = ["remit", "host", "apis", "cs"]
        cogs = sum(v[k] for k in cogs_k)
        ws_pl.write_formula(R["cogs"], c, "=" + "+".join(col(k) for k in cogs_k), fm["usd"], cogs)
        gp = tot - cogs
        ws_pl.write_formula(R["gp"], c, f"={col('tot')}-{col('cogs')}", fm["usdb"], gp)
        ws_pl.write_formula(R["gm"], c, f"={col('gp')}/{col('tot')}", fm["pct"], gp / tot)
        opex_k = ["p_rd", "p_sm", "prog", "p_ga", "prof", "acct", "other"]
        opex = sum(v[k] for k in opex_k)
        ws_pl.write_formula(R["opex"], c, "=" + "+".join(col(k) for k in opex_k), fm["usdb"], opex)
        op = gp - opex
        ws_pl.write_formula(R["op"], c, f"={col('gp')}-{col('opex')}", fm["usdb"], op)
        payroll = v["cs"] + v["p_rd"] + v["p_sm"] + v["p_ga"]
        ws_pl.write_formula(R["payroll"], c, f"={col('cs')}+{col('p_rd')}+{col('p_sm')}+{col('p_ga')}", fm["usd"], payroll)
        ws_pl.write_formula(R["burn"], c, f"=-{col('op')}", fm["usd"], -op)
        if j < N_MONTHS:
            ws_pl.write_number(R["heads"], c, F["heads"][j], fm["int"])
        V[j] = dict(v, tot=tot, cogs=cogs, gp=gp, op=op)
    for j in range(N_MONTHS):
        assert abs(V[j]["op"] - F["op"][j]) < 0.05, "P&L operating result differs from the facts"
    last_c = 2 + LAST
    wb.define_name("SUB_REVENUE_2026_09", f"='P&L'!${col_name(last_c)}${R['sub'] + 1}")
    ws_pl.write(R["heads"] + 2, 0, FOOTER, fm["note"])
    reg("BF4", "P&L", a1(R["sub"], last_c), name="SUB_REVENUE_2026_09", expect=F["sub_shown"][LAST],
        label="P&L subscription revenue, 2026-09")
    reg("BF1", "P&L", a1(R["rec"], 0), expect="Recovery revenue", label="row label: recoveries counted as revenue")
    reg("BF1", "P&L", a1(R["remit"], 0), expect="Recoveries paid to customers", label="row label: the customers' share in cost of revenue")
    reg("BF1", "P&L", f"{a1(R['tot'], 2 + LTM[0])}:{a1(R['tot'], last_c)}", label="total revenue, 2025-10 to 2026-09")
    reg("BF3", "P&L", a1(R["prof"], 0), expect="Professional services", label="row that holds the contractors in the actual months")
    reg("BF3", "P&L", a1(R["prof"], last_c), expect=round(pl["prof"][LAST], 2), label="professional services, 2026-09 actual")
    reg("BF3", "P&L", a1(R["prof"], last_c + 1), expect=PROF_PLAN, label="professional services, 2026-10 plan")
    F["pl_rows"] = R
    F["pl_V"] = V

    # ---- Revenue_Build
    ws_rev.set_column(0, 0, 12)
    ws_rev.set_column(1, 1, 30)
    ws_rev.set_column(2, 2, 10)
    ws_rev.set_column(3, 3, 30)
    ws_rev.set_column(4, 5, 18)
    ws_rev.set_column(6, 6, 70)
    ws_rev.write(0, 0, "Subscription revenue by broker, 2026-09 (USD)", fm["title"])
    ws_rev.write(1, 0, "Brokers paying in September 2026. Annual plans are paid once a year, in advance.", fm["note"])
    ws_rev.write_row(3, 0, ["Customer id", "Customer", "Plan", "Billing", "Monthly fee (contract)", "Revenue booked 2026-09", "Note"], fm["headl"])
    r = 4
    first = r
    paying = [c for c in F["customers"] if c["fee"][LAST] > 0]
    for c in paying:
        booked = 12 * c["fee"][LAST] if c["role"] == "annual_sept" else c["fee"][LAST]
        billing = "Monthly"
        note = ""
        if c["role"] == "annual_decoy":
            billing = "Annual, paid in advance"
            note = "Annual plan invoiced 2026-02-01 for twelve months. Booked monthly."
        if c["role"] == "annual_sept":
            billing = "Annual, paid in advance"
            note = "Annual plan invoiced 2026-09-01."
        if c["role"] == "big":
            note = "Network plan, 24-month agreement from 2025-05-01."
        ws_rev.write(r, 0, c["id"])
        ws_rev.write(r, 1, c["name"])
        ws_rev.write(r, 2, c["plans"][LAST])
        ws_rev.write(r, 3, billing)
        ws_rev.write_number(r, 4, c["fee"][LAST], fm["usd"])
        ws_rev.write_number(r, 5, booked, fm["usd"])
        if note:
            ws_rev.write(r, 6, note, fm["note"])
        if c["role"] == "annual_sept":
            reg("BF4", "Revenue_Build", a1(r, 5), expect=booked, label="Ostley Freight's annual invoice booked as September revenue")
            reg("BF4", "Revenue_Build", a1(r, 4), expect=c["fee"][LAST], label="Ostley Freight's monthly fee under the contract")
        if c["role"] == "big":
            GREEN_LOCS["GF3"].append({"file": MODEL, "sheet": "Revenue_Build", "cell": a1(r, 4), "value": BIG_FEE,
                                      "label": "largest customer's monthly fee in the model"})
        if c["role"] == "annual_decoy":
            LOC["DC1"].append({"file": MODEL, "sheet": "Revenue_Build", "cell": a1(r, 5), "expect": c["fee"][LAST],
                               "label": "Tessmore Freight booked at its monthly fee"})
        r += 1
    last_r = r - 1
    ws_rev.write(r, 1, "Paying brokers", fm["bold"])
    ws_rev.write_formula(r, 2, f"=COUNTA(A{first + 1}:A{last_r + 1})", fm["name"], len(paying))
    wb.define_name("PAYING_BROKERS", f"=Revenue_Build!$C${r + 1}")
    GREEN_LOCS["GF2"].append({"file": MODEL, "sheet": "Revenue_Build", "cell": a1(r, 2), "named_cell": "PAYING_BROKERS",
                              "value": len(paying), "label": "paying brokers in the model"})
    r += 1
    ws_rev.write(r, 1, "Contracted monthly fees", fm["bold"])
    ws_rev.write_formula(r, 4, f"=SUM(E{first + 1}:E{last_r + 1})", fm["usdb"], F["contracted_mrr"])
    wb.define_name("CONTRACTED_FEES_2026_09", f"=Revenue_Build!$E${r + 1}")
    r += 1
    ws_rev.write(r, 1, "MRR, September 2026", fm["bold"])
    ws_rev.write_formula(r, 5, f"=SUM(F{first + 1}:F{last_r + 1})", fm["name"], F["sub_shown"][LAST])
    wb.define_name("MRR_2026_09", f"=Revenue_Build!$F${r + 1}")
    reg("BF4", "Revenue_Build", a1(r, 5), name="MRR_2026_09", expect=F["sub_shown"][LAST], label="model MRR, September 2026")
    r += 2
    ws_rev.write(r, 1, "Recovery revenue, 2026-09")
    ws_rev.write_number(r, 5, F["recovered_total"][LAST], fm["usd"])
    ws_rev.write(r, 6, "Money recovered from carriers in September for overbilled invoices.", fm["note"])
    r += 1
    ws_rev.write(r, 1, "Total revenue, 2026-09", fm["bold"])
    ws_rev.write_formula(r, 5, f"=F{r - 2}+F{r}", fm["usdb"], F["sub_shown"][LAST] + F["recovered_total"][LAST])
    ws_rev.write(r + 2, 0, FOOTER, fm["note"])

    # ---- Team
    ws_team.set_column(0, 0, 40)
    ws_team.set_column(1, 1, 14)
    ws_team.set_column(2, 4, 18)
    ws_team.write(0, 0, "Team: employees and planned hires", fm["title"])
    ws_team.write(1, 0, "Full-time employees on payroll. Base pay in USD a year.", fm["note"])
    ws_team.write_row(3, 0, ["Employee", "Department", "Start date", "Base pay (USD)"], fm["headl"])
    dept_name = {"rd": "Engineering", "cs": "Customer success", "sm": "Sales", "ga": "G&A"}
    r = 4
    for (title, dk, s0, sday, base) in STAFF:
        ws_team.write(r, 0, title)
        ws_team.write(r, 1, dept_name[dk])
        ws_team.write(r, 2, f"{MONTH_LABELS[s0]}-{sday:02d}")
        ws_team.write_number(r, 3, base, fm["usd"])
        r += 1
    ws_team.write(r, 0, "Employees today", fm["bold"])
    ws_team.write_formula(r, 1, f"=COUNTA(A5:A{r})", fm["name"], len(STAFF))
    wb.define_name("EMPLOYEES_NOW", f"=Team!$B${r + 1}")
    emp_row = r
    r += 2
    ws_team.write_row(r, 0, ["Planned hire", "Department", "Start date", "Base pay (USD)", "Monthly cost (USD)"], fm["headl"])
    r += 1
    h_first = r
    for (title, dk, t, day, base) in HIRES:
        ws_team.write(r, 0, title)
        ws_team.write(r, 1, dept_name[dk])
        ws_team.write(r, 2, f"{mlabel(LAST + t)}-{day:02d}")
        ws_team.write_number(r, 3, base, fm["usd"])
        ws_team.write_formula(r, 4, f"=D{r + 1}*LOAD_FACTOR/12", fm["usd"], base * LOAD / 12)
        r += 1
    ws_team.write(r, 0, "Employees after these hires", fm["bold"])
    ws_team.write_formula(r, 1, f"=B{emp_row + 1}+COUNTA(A{h_first + 1}:A{r})", fm["name"], len(STAFF) + len(HIRES))
    wb.define_name("EMPLOYEES_AFTER_HIRES", f"=Team!$B${r + 1}")
    ws_team.write(r + 3, 0, FOOTER, fm["note"])

    # ---- Cash_Runway
    ws_cash.set_column(0, 0, 50)
    ws_cash.set_column(1, 13, 15)
    ws_cash.write(0, 0, "Cash and runway (USD)", fm["title"])
    ws_cash.write(2, 0, "Runway (months of cash from the data date)", fm["bold"])
    ws_cash.write(3, 0, "Average net burn, plan months 1 to 12 (USD a month)", fm["bold"])
    ws_cash.write(4, 0, "Cash at the data date (USD)", fm["bold"])
    hdr = 6
    ws_cash.write_row(hdr, 0, ["Month", "Plan month", "Subscription revenue", "Recovery revenue", "Total revenue", "Cost of revenue",
                               "Payroll", "Professional services", "Accounting", "Marketing programs", "Rent, tools and other",
                               "Net burn", "Equity raised", "Ending cash"], fm["headl"])
    r0 = hdr + 1
    ws_cash.write(r0, 0, MONTH_LABELS[LAST])
    ws_cash.write_number(r0, 1, 0, fm["int"])
    ws_cash.write_formula(r0, 13, "=CASH_START", fm["usd"], CASH_START)
    rows = F["fc_shown"]
    for i, x in enumerate(rows):
        r = r0 + 1 + i
        n = r + 1
        ws_cash.write(r, 0, x["label"])
        ws_cash.write_number(r, 1, x["t"], fm["int"])
        ws_cash.write_number(r, 2, x["sub"], fm["usd"])
        ws_cash.write_number(r, 3, x["rec"], fm["usd"])
        ws_cash.write_formula(r, 4, f"=C{n}+D{n}", fm["usd"], x["revenue"])
        ws_cash.write_number(r, 5, x["remit"] + x["infra"], fm["usd"])
        ws_cash.write_number(r, 6, x["payroll"], fm["usd"])
        ws_cash.write_formula(r, 7, "=PROF_SERVICES_USD_MONTH", fm["usd"], x["prof"])
        ws_cash.write_formula(r, 8, "=ACCOUNTING_USD_MONTH", fm["usd"], x["acct"])
        ws_cash.write_number(r, 9, x["prog"], fm["usd"])
        ws_cash.write_number(r, 10, x["other"], fm["usd"])
        ws_cash.write_formula(r, 11, f"=F{n}+G{n}+H{n}+I{n}+J{n}+K{n}-E{n}", fm["usd"], x["burn"])
        ws_cash.write_number(r, 12, x["raised"], fm["usd"])
        ws_cash.write_formula(r, 13, f"=N{n - 1}+M{n}-L{n}", fm["usd"], x["cash"])
    first_t, last_t = r0 + 2, r0 + 1 + len(rows)
    ws_cash.write_formula(2, 1, f'=COUNTIF(N{first_t}:N{last_t},">0")', fm["name"], F["runway_shown"])
    ws_cash.write_formula(3, 1, f"=AVERAGE(L{first_t}:L{first_t + 11})", fm["name"], F["burn_shown"])
    ws_cash.write_formula(4, 1, "=CASH_START", fm["name"], CASH_START)
    wb.define_name("RUNWAY_MONTHS", "=Cash_Runway!$B$3")
    wb.define_name("AVG_NET_BURN_12M", "=Cash_Runway!$B$4")
    reg("BF3", "Cash_Runway", "B3", name="RUNWAY_MONTHS", expect=F["runway_shown"], label="runway in months")
    reg("BF3", "Cash_Runway", "B4", name="AVG_NET_BURN_12M", expect=round(F["burn_shown"], 2), label="average net burn, plan months 1 to 12")
    reg("BF3", "Cash_Runway", f"H{first_t}:H{first_t + 11}", label="professional services, plan months 1 to 12")
    LOC["DC2"].append({"file": MODEL, "sheet": "Cash_Runway", "cell": f"I{first_t}:I{first_t + 11}",
                       "label": "accounting held in every plan month"})
    ws_cash.write(last_t + 1, 0, FOOTER, fm["note"])
    F["cash_first_t"] = first_t

    # ---- Cash_Bridge
    ws_bridge.set_column(0, 0, 62)
    ws_bridge.set_column(1, 1, 18)
    ws_bridge.set_column(2, 2, 90)
    ws_bridge.write(0, 0, "Cash bridge: money raised to cash at the data date (USD)", fm["title"])
    ws_bridge.write(1, 0, "Cash burn is taken as the operating result in the P&L, adjusted for annual plans paid in advance.", fm["note"])
    ws_bridge.write_row(3, 0, ["Line", "USD", "Note"], fm["headl"])
    op_range = f"'P&L'!{a1(R['op'], 2)}:{a1(R['op'], 1 + N_MONTHS)}"
    tess = F["tess"]
    bridge = [
        ("Raised in 2025-01: angel SAFEs", "=RAISED_SAFE_2025_01", sum(s[1] for s in SAFES), "usd", "Two SAFEs. See the cap table."),
        ("Raised in 2025-07: pre-seed SAFE", "=RAISED_SAFE_2025_07", F["safe_c"], "usd", "One SAFE. See the cap table."),
        ("Total raised before the seed", "=B5+B6", F["raised_total"], "usdb", ""),
        ("Less: net loss before 2025-05", "=NET_LOSS_BEFORE_2025_05", F["net_loss_pre"], "usd", "Spend before the first paying broker."),
        ("Less: net loss 2025-05 to 2026-09", f"=-SUM({op_range})", F["net_loss_actual"], "usd", "Sum of the P&L operating result over the 17 actual months."),
        ("Plus: annual plans paid in advance, not yet delivered", "", F["deferred"], "usd",
         f"{tess['name']}: {F['tess_months_left']} months of its annual plan at {money(tess['fee'][LAST])} a month."),
        ("Cash at 2026-09-30 from the bridge", "=B7-B8-B9+B10", F["bridge_cash"], "usdb", ""),
        ("Cash at 2026-09-30 in Assumptions", "=CASH_START", CASH_START, "usd", "Bank balance."),
        ("Difference", "=B11-B12", F["bridge_diff"], "usd2", "Rounding only: the loss before 2025-05 is stated in whole dollars."),
    ]
    for i, (lab, form, val, fmt, note) in enumerate(bridge):
        ws_bridge.write(4 + i, 0, lab, fm["bold"] if fmt == "usdb" else None)
        if form:
            ws_bridge.write_formula(4 + i, 1, form, fm[fmt], val)
        else:
            ws_bridge.write_number(4 + i, 1, val, fm[fmt])
        if note:
            ws_bridge.write(4 + i, 2, note, fm["note"])
    wb.define_name("DEFERRED_REVENUE_USD", "=Cash_Bridge!$B$10")
    wb.define_name("CASH_BRIDGE_DIFF", "=Cash_Bridge!$B$13")
    LOC["DC1"].append({"file": MODEL, "sheet": "Cash_Bridge", "cell": "B10", "named_cell": "DEFERRED_REVENUE_USD", "expect": F["deferred"],
                       "label": "deferred revenue: Tessmore's months not yet delivered"})
    reg("BF4", "Cash_Bridge", "B10", name="DEFERRED_REVENUE_USD", expect=F["deferred"],
        label="deferred revenue holds only Tessmore; Ostley's eleven undelivered months are missing")
    ws_bridge.write(15, 0, FOOTER, fm["note"])
    wb.close()


def build_cap_table():
    wb = new_workbook(CAP)
    fm = formats(wb)
    ws = wb.add_worksheet("Cap_Table")
    ws.set_column(0, 0, 42)
    ws.set_column(1, 1, 30)
    ws.set_column(2, 5, 20)
    ws.write(0, 0, "Brasswick, Inc.: fully diluted cap table", fm["title"])
    ws.write(1, 0, "As of 2026-09-30. SAFEs shown as converted at their cap. Pro forma shows the seed round.", fm["note"])
    ws.write_row(3, 0, ["Holder", "Class", "Shares", "% fully diluted", "Pro forma shares", "Pro forma %"], fm["headl"])
    safes = [(n, a, c) for (n, a, c, _d) in SAFES] + [(SAFE_C_NAME, F["safe_c"], SAFE_C_CAP)]
    plain = [(CEO["name"] + " (CEO)", "Common", 4_186_500), (CTO["name"] + " (CTO)", "Common", 3_962_000),
             ("Options granted (5 holders)", "Option pool, granted", 612_400), ("Options available", "Option pool, unissued", 791_600)]
    nonsafe = sum(h[2] for h in plain)
    tot = round(nonsafe / (1 - sum(a / c for (_n, a, c) in safes)))
    for _ in range(50):
        nxt = nonsafe + sum(round(a / c * tot) for (_n, a, c) in safes)
        if nxt == tot:
            break
        tot = nxt
    safe_shares = [round(a / c * tot) for (_n, a, c) in safes]
    holders = plain + [(n + " (SAFE converted)", "Preferred (from SAFE)", sh) for (n, _a, _c), sh in zip(safes, safe_shares)]
    total = sum(h[2] for h in holders)
    new_shares = round(total * SEED_RAISE / SEED_PRE)
    post = total + new_shares
    r = first = 4
    tot_row_idx = first + len(holders) + 1
    for (name, cls, sh) in holders:
        ws.write(r, 0, name)
        ws.write(r, 1, cls)
        ws.write_number(r, 2, sh, fm["int"])
        ws.write_formula(r, 3, f"=C{r + 1}/C${tot_row_idx + 1}", fm["pct2"], sh / total)
        ws.write_formula(r, 4, f"=C{r + 1}", fm["int"], sh)
        ws.write_formula(r, 5, f"=E{r + 1}/E${tot_row_idx + 1}", fm["pct2"], sh / post)
        r += 1
    ws.write(r, 0, "Seed investors (new)")
    ws.write(r, 1, "Seed Preferred")
    ws.write_number(r, 2, 0, fm["int"])
    ws.write_formula(r, 3, f"=C{r + 1}/C${tot_row_idx + 1}", fm["pct2"], 0)
    lead_row = r
    ws.write_formula(r, 5, f"=E{r + 1}/E${tot_row_idx + 1}", fm["pct2"], new_shares / post)
    r += 1
    ws.write(r, 0, "Total", fm["bold"])
    ws.write_formula(r, 2, f"=SUM(C{first + 1}:C{r})", fm["intb"], total)
    ws.write_formula(r, 3, f"=SUM(D{first + 1}:D{r})", fm["pctb"], 1.0)
    ws.write_formula(r, 4, f"=SUM(E{first + 1}:E{r})", fm["intb"], post)
    ws.write_formula(r, 5, f"=SUM(F{first + 1}:F{r})", fm["pctb"], 1.0)
    tot_row = r
    r += 2
    ws.write(r, 0, "SAFE conversion", fm["bold"])
    r += 1
    ws.write_row(r, 0, ["Investor", "Purchase amount (USD)", "Post-money cap (USD)", "Ownership", "Conversion price (USD)", "Shares"], fm["headl"])
    r += 1
    s_first = r
    for (name, amt, cap), sh in zip(safes, safe_shares):
        ws.write(r, 0, name)
        ws.write_number(r, 1, amt, fm["usd"])
        ws.write_number(r, 2, cap, fm["usd"])
        ws.write_formula(r, 3, f"=B{r + 1}/C{r + 1}", fm["pct2"], amt / cap)
        ws.write_formula(r, 4, f"=C{r + 1}/C${tot_row + 1}", fm["dec"], cap / total)
        ws.write_formula(r, 5, f"=ROUND(B{r + 1}/E{r + 1},0)", fm["int"], sh)
        r += 1
    ws.write(r, 0, "Total SAFEs", fm["bold"])
    ws.write_formula(r, 1, f"=SUM(B{s_first + 1}:B{r})", fm["usdb"], sum(a for (_n, a, _c) in safes))
    ws.write_formula(r, 5, f"=SUM(F{s_first + 1}:F{r})", fm["intb"], sum(safe_shares))
    r += 2
    ws.write(r, 0, "Seed round", fm["bold"])
    r += 1
    rows = [("Pre-money valuation (USD)", SEED_PRE, "usd", None), ("New money (USD)", SEED_RAISE, "usd", None),
            ("Post-money valuation (USD)", SEED_PRE + SEED_RAISE, "usd", f"=B{r + 1}+B{r + 2}"),
            ("Price per share (USD)", SEED_PRE / total, "dec", f"=B{r + 1}/C{tot_row + 1}"),
            ("New shares issued", new_shares, "int", f"=ROUND(B{r + 2}/B{r + 4},0)"),
            ("Seed ownership", new_shares / post, "pct2", f"=B{r + 5}/E{tot_row + 1}")]
    for i, (lab, val, fmt, form) in enumerate(rows):
        ws.write(r + i, 0, lab)
        if form:
            ws.write_formula(r + i, 1, form, fm[fmt], val)
        else:
            ws.write_number(r + i, 1, val, fm[fmt])
    ws.write_formula(lead_row, 4, f"=B{r + 5}", fm["int"], new_shares)
    GREEN_LOCS["GF1"].append({"file": CAP, "sheet": "Cap_Table", "cell": a1(r + 1, 1), "value": SEED_RAISE, "label": "seed new money in the cap table"})
    ws.write(r + 8, 0, FOOTER, fm["note"])
    wb.close()
    F["cap"] = {"total_pre": total, "new_shares": new_shares, "post": post, "safe_shares": safe_shares}


# ---------------------------------------------------------------------------------------------
# The deck
# ---------------------------------------------------------------------------------------------
INK = colors.HexColor("#22262E")
BRASS = colors.HexColor("#B08D3C")
GREYTXT = colors.HexColor("#555555")
PAPER = colors.HexColor("#F4EFE4")
SW, SH = 960, 540
N_SLIDES = 12


def png_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def chart_revenue_2026():
    fig, ax = plt.subplots(figsize=(6.0, 3.3))
    xs = list(range(FIRST_2026, N_MONTHS))
    ax.bar(range(len(xs)), [F["total_shown"][m] / 1000 for m in xs], color="#B08D3C")
    ax.set_xticks(range(len(xs)))
    ax.set_xticklabels([calendar.month_abbr[int(MONTH_LABELS[m][5:])] for m in xs], fontsize=8)
    ax.set_ylabel("Revenue ($ thousands)", fontsize=9)
    ax.set_ylim(0, None)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    return png_bytes(fig)


def deck_claims():
    return [
        ("Revenue, last 12 months", money(F["ltm_shown"]), 4),
        ("MRR, September 2026", money(F["sub_shown"][LAST]), 4),
        ("Paying brokers", str(F["paying"][LAST]), 4),
        ("Monthly revenue chart", f"{MONTH_LABELS[FIRST_2026]} to {MONTH_LABELS[LAST]}", 4),
        ("Brokers still paying", f"{F['paying'][LAST]} of {F['ever']}", 5),
        ("Largest customer", f"{round(F['big_share'] * 100)}% of subscription revenue", 5),
        ("Carrier invoices audited, September 2026", f"{F['invoices'][LAST]:,}", 5),
        ("Carrier invoices audited since launch", f"{F['invoices_cum'][LAST]:,}", 5),
        ("Recovery fee", f"{round(RECOVERY_FEE * 100)}% of money recovered", 6),
        ("Market size (company estimate)", money(MARKET_TAM), 7),
        ("Full-time employees", str(len(STAFF)), 9),
        ("Average monthly net burn, next 12 months", money(round(F["burn_shown"])), 10),
        ("Runway", f"{F['runway_shown']} months", 10),
        ("Employees after the seed hires", str(len(STAFF) + len(HIRES)), 10),
        ("Seed raise", money(SEED_RAISE), 11),
        ("Pre-money valuation", money(SEED_PRE), 11),
    ]


def build_deck():
    path = ROOM / DECK
    path.parent.mkdir(parents=True, exist_ok=True)
    c = rl_canvas.Canvas(str(path), pagesize=(SW, SH), invariant=1)
    c.setTitle("Brasswick: seed pitch deck")
    c.setAuthor("Brasswick (synthetic)")
    c.setSubject(FOOTER)

    def logo(x, y, size, word=True, word_color=colors.white):
        """The Brasswick mark: a brass tile with two sheets laid over each other, an invoice on a load."""
        c.setFillColor(BRASS)
        c.roundRect(x, y, size, size, size * 0.2, fill=1, stroke=0)
        c.setStrokeColor(colors.white)
        c.setLineWidth(max(1.2, size * 0.06))
        c.rect(x + size * 0.18, y + size * 0.30, size * 0.42, size * 0.50, fill=0, stroke=1)
        c.rect(x + size * 0.40, y + size * 0.18, size * 0.42, size * 0.50, fill=0, stroke=1)
        if word:
            c.setFillColor(word_color)
            c.setFont("Helvetica-Bold", size * 0.62)
            c.drawString(x + size * 1.25, y + size * 0.24, "Brasswick")

    def frame(n, title):
        c.setFillColor(colors.white)
        c.rect(0, 0, SW, SH, fill=1, stroke=0)
        c.setFillColor(INK)
        c.rect(0, SH - 84, SW, 84, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 30)
        c.drawString(48, SH - 54, title)
        logo(SW - 186, SH - 58, 30)
        c.setFillColor(GREYTXT)
        c.setFont("Helvetica", 9)
        c.drawString(48, 22, FOOTER)
        c.drawRightString(SW - 48, 22, f"Slide {n} of {N_SLIDES}")

    def para(text, x, y, width=860, size=20, lead=28, bold=False, color=colors.black):
        font = "Helvetica-Bold" if bold else "Helvetica"
        c.setFont(font, size)
        c.setFillColor(color)
        for line in simpleSplit(text, font, size, width):
            c.drawString(x, y, line)
            y -= lead
        return y

    def bullets(items, x, y, width=860, size=19, lead=26, gap=9):
        for it in items:
            c.setFillColor(BRASS)
            c.rect(x, y + 3, 7, 7, fill=1, stroke=0)
            y = para(it, x + 22, y, width - 22, size, lead)
            y -= gap
        return y

    def stat(x, y, big, label, size=46):
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", size)
        c.drawString(x, y, big)
        c.setFillColor(GREYTXT)
        c.setFont("Helvetica", 15)
        c.drawString(x, y - 24, label)

    def heading(text, x, y):
        c.setFont("Helvetica-Bold", 21)
        c.setFillColor(INK)
        c.drawString(x, y, text)

    claims = deck_claims()
    cv = {lab: val for (lab, val, _s) in claims}

    # 1 Title
    c.setFillColor(INK)
    c.rect(0, 0, SW, SH, fill=1, stroke=0)
    logo(60, 410, 64, word=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 64)
    c.drawString(60, 330, "Brasswick")
    c.setFont("Helvetica", 27)
    c.drawString(60, 282, "Every carrier invoice, matched to the load before you pay it")
    c.setFillColor(BRASS)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(60, 200, f"Seed  |  {money(SEED_RAISE)}  |  Long Island City, New York  |  Founded 2025")
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 14)
    c.drawString(60, 160, "Data as of 2026-09-30")
    c.setFillColor(colors.HexColor("#B8BCC4"))
    c.setFont("Helvetica", 9)
    c.drawString(60, 22, FOOTER)
    c.drawRightString(SW - 48, 22, f"Slide 1 of {N_SLIDES}")
    c.showPage()

    # 2 Problem
    frame(2, "The problem")
    bullets(["Freight brokers pay thousands of carrier invoices a month.",
             "Many carry charges the rate confirmation never agreed: detention, lumper fees, extra stops, a second copy of the same invoice.",
             "Settlement teams check a sample by hand. The rest gets paid."], 48, 410, 430, 18, 25)
    c.setFillColor(PAPER)
    c.roundRect(520, 150, 392, 290, 8, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(538, 418, "Example: load 48213")
    rows = [("Rate confirmation", "Linehaul $2,150, fuel included"), ("Carrier invoice", "Linehaul $2,150"),
            ("", "Detention $225"), ("", "Lumper $180"), ("Brasswick", "Detention not on the rate confirmation."),
            ("", "No lumper receipt attached."), ("", "Holds $405 and asks the carrier for proof.")]
    y = 390
    for a, b in rows:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(538, y, a)
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)
        c.drawString(660, y, b)
        c.setFillColor(INK)
        y -= 30
    c.showPage()

    # 3 Product
    frame(3, "The product")
    bullets(["Reads each carrier invoice, the rate confirmation, the bill of lading and the proof of delivery.",
             "Matches the invoice to the load in the broker's transportation management system.",
             "Approves clean invoices for payment and holds the ones that do not match, with the reason.",
             "Writes the dispute to the carrier and tracks the answer.",
             "On invoices a broker paid before it joined, chases the overbilled amounts back from carriers."], 48, 410, 860, 19, 26)
    c.showPage()

    # 4 Traction
    frame(4, "Traction")
    stat(48, 380, f"${F['ltm_shown'] / 1e3:,.0f}K", "Revenue, last 12 months")
    stat(48, 280, money(F["sub_shown"][LAST]), "MRR, September 2026")
    stat(48, 180, str(F["paying"][LAST]), "Paying brokers")
    c.drawImage(ImageReader(chart_revenue_2026()), 380, 120, width=540, height=297)
    c.setFillColor(GREYTXT)
    c.setFont("Helvetica", 12)
    c.drawString(392, 424, f"Monthly revenue, {month_name(FIRST_2026)} to {month_name(LAST)}")
    para("Revenue grew every month in 2026.", 392, 92, 520, 16, 20, bold=True, color=INK)
    c.showPage()

    # 5 Customers
    frame(5, "Customers")
    bullets([f"{F['paying'][LAST]} of the {F['ever']} brokers who have paid us still do.",
             f"Our largest customer, {F['big']['name']}, is {round(F['big_share'] * 100)}% of subscription revenue, on a 24-month agreement to 2027-04-30.",
             f"Carrier invoices audited in September 2026: {F['invoices'][LAST]:,}.",
             f"Carrier invoices audited since launch: {F['invoices_cum'][LAST]:,}.",
             "Brokers from 40 to 400 employees, moving dry van, reefer and flatbed loads."], 48, 410, 860, 19, 26)
    c.showPage()

    # 6 Business model
    frame(6, "How we make money")
    heading("Subscription", 48, 420)
    bullets([f"Priced by monthly load volume: Lane {money(LIST_PRICE['Lane'])} a month, Fleet {money(LIST_PRICE['Fleet'])} a month, Network on contract.",
             "Annual plans are paid once a year in advance and cost 10% less."], 48, 388, 410, 17, 24)
    heading("Recoveries", 500, 420)
    bullets(["On invoices a broker paid before it joined, we chase overbilled charges back from carriers.",
             f"We keep {round(RECOVERY_FEE * 100)}% of the money recovered."], 500, 388, 410, 17, 24)
    c.showPage()

    # 7 Market
    frame(7, "Market")
    stat(48, 380, f"{MARKET_BROKERS:,}", "US freight brokers with ten or more staff (company estimate)")
    stat(48, 270, money(MARKET_ACV), "What one of them would pay a year (company estimate)")
    stat(48, 160, money(MARKET_TAM), "Market size (company estimate)")
    c.showPage()

    # 8 Competition
    frame(8, "Why brokers choose us")
    bullets(["Freight audit firms check after the money has gone out. We check before it is paid.",
             "Transportation management systems store the documents but do not compare them.",
             "Our matching reads the documents as they arrive, in any format the carrier sends."], 48, 410, 860, 19, 26)
    c.showPage()

    # 9 Team
    frame(9, "Team")
    people = [(CEO["name"], "CEO and co-founder", "Ran carrier settlement at a mid-size freight brokerage for nine years."),
              (CTO["name"], "CTO and co-founder", "Built document extraction for insurance claims software."),
              (SENIOR[0][0], SENIOR[0][1], "Shipped the first matching engine in eight weeks."),
              (SENIOR[1][0], SENIOR[1][1], "Onboards every broker and runs the recovery desk.")]
    for i, (nm, role, line) in enumerate(people):
        x = 48 + (i % 2) * 440
        y = 400 - (i // 2) * 130
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 19)
        c.drawString(x, y, nm)
        c.setFillColor(BRASS)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x, y - 22, role)
        para(line, x, y - 46, 400, 14, 19)
    para(f"{len(STAFF)} full-time employees today.", 48, 110, 860, 18, 24, bold=True, color=INK)
    c.showPage()

    # 10 Plan
    frame(10, "Plan and runway")
    stat(48, 380, f"{F['runway_shown']} months", "Runway after the seed closes, from 2026-09-30")
    stat(48, 280, money(round(F["burn_shown"])), "Average monthly net burn, next 12 months")
    stat(48, 180, str(len(STAFF) + len(HIRES)), f"Employees after the seed hires ({len(HIRES)} hires)")
    bullets([f"{len(HIRES)} hires: two account executives, a growth marketer, three engineers and a customer success manager.",
             "Marketing programs start the month the seed closes."], 500, 380, 410, 16, 22)
    c.showPage()

    # 11 Ask
    frame(11, "The ask")
    stat(48, 380, money(SEED_RAISE), "Seed raise")
    stat(48, 280, money(SEED_PRE), "Pre-money valuation")
    heading("Use of funds", 500, 400)
    y = 368
    for lab, share in (("Engineering", 0.40), ("Sales and marketing", 0.40), ("Customer success", 0.12), ("General and administrative", 0.08)):
        para(f"{lab}: {money(SEED_RAISE * share)} ({share * 100:.0f}%)", 500, y, 410, 16, 22)
        y -= 28
    c.showPage()

    # 12 Appendix
    frame(12, "Appendix: key metrics")
    c.setFont("Helvetica", 11)
    c.setFillColor(GREYTXT)
    c.drawString(48, 438, "Key metrics from this deck, with the slide where each appears.")
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(INK)
    c.drawString(48, 414, "Metric")
    c.drawString(470, 414, "Value")
    c.drawString(840, 414, "Slide")
    y = 394
    c.setFont("Helvetica", 11.5)
    c.setFillColor(colors.black)
    for (lab, val, sl) in claims:
        c.drawString(48, y, lab)
        c.drawString(470, y, val)
        c.drawString(840, y, str(sl))
        y -= 20.5
    c.showPage()
    c.save()

    F["claims"] = [{"label": lab, "value": val, "slide": sl} for (lab, val, sl) in claims]
    write_text(CLAIMS_SIDECAR, json.dumps({"source": DECK, "slide": N_SLIDES, "claims": F["claims"]}, indent=2, ensure_ascii=False) + "\n")

    def claim_loc(fid, lab, store=LOC):
        row = next(x for x in claims if x[0] == lab)
        store[fid].append({"file": DECK, "page": N_SLIDES, "claims_row": lab, "text": f"{lab} {row[1]} {row[2]}",
                           "slide_ref": row[2], "label": f"appendix row '{lab}'"})

    claim_loc("BF1", "Revenue, last 12 months")
    LOC["BF1"].append({"file": DECK, "page": 6, "text": f"We keep {round(RECOVERY_FEE * 100)}% of the money recovered.",
                       "label": "the deck itself says Brasswick keeps only 30%"})
    claim_loc("BF2", "Monthly revenue chart")
    LOC["BF2"].append({"file": DECK, "page": 4, "text": f"Monthly revenue, {month_name(FIRST_2026)} to {month_name(LAST)}", "label": "chart caption"})
    LOC["BF2"].append({"file": DECK, "page": 4, "text": "Revenue grew every month in 2026.", "label": "the claim the short chart supports"})
    claim_loc("BF3", "Average monthly net burn, next 12 months")
    claim_loc("BF3", "Runway")
    claim_loc("BF4", "MRR, September 2026")
    claim_loc("DC3", "Carrier invoices audited since launch")
    LOC["DC3"].append({"file": DECK, "page": 5, "text": f"Carrier invoices audited since launch: {F['invoices_cum'][LAST]:,}.",
                       "label": "deck labels the cumulative count as cumulative"})
    GREEN_LOCS["GF1"].append({"file": DECK, "page": 11, "text": money(SEED_RAISE), "value": SEED_RAISE, "label": "deck seed raise, slide 11"})
    GREEN_LOCS["GF2"].append({"file": DECK, "page": 5, "text": f"{F['paying'][LAST]} of the {F['ever']} brokers who have paid us still do.",
                              "value": F["paying"][LAST], "label": "deck: brokers still paying, slide 5"})


# ---------------------------------------------------------------------------------------------
# Other PDFs
# ---------------------------------------------------------------------------------------------
STYLES = getSampleStyleSheet()
S_BODY = ParagraphStyle("bw_body", parent=STYLES["BodyText"], fontName="Helvetica", fontSize=10.5, leading=15, spaceAfter=6)
S_SMALL = ParagraphStyle("bw_small", parent=S_BODY, fontSize=9, leading=12, textColor=GREYTXT)
S_H1 = ParagraphStyle("bw_h1", parent=STYLES["Heading1"], fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=INK, spaceAfter=10)
S_H2 = ParagraphStyle("bw_h2", parent=STYLES["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=INK, spaceBefore=8, spaceAfter=4)
S_CELL = ParagraphStyle("bw_cell", parent=S_BODY, fontSize=9, leading=12, spaceAfter=0)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def P(text, style=S_BODY):
    return Paragraph(esc(text), style)


def tbl(rows, widths):
    data = [[Paragraph(esc(str(x)), S_CELL) for x in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9C2B2")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                           ("BACKGROUND", (0, 0), (-1, 0), PAPER)]))
    return t


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
                            title=title, author="Brasswick (synthetic)", subject=FOOTER, invariant=1)
    doc.build(story, onFirstPage=foot, onLaterPages=foot)


MSA = "04_contracts/msa_corvane_logistics.pdf"
ORDER_OSTLEY = "04_contracts/order_form_ostley_freight.pdf"
ORDER_TESS = "04_contracts/order_form_tessmore_freight.pdf"
SOW = "04_contracts/sow_norrgate_software_studio.pdf"
SCRIPT = "01_overview/pitch_video_script.md"
SPOKEN_RUNWAY = 36           # "close to three years" (flag BF5)

ROOM_FILES = [
    (COVER, "Cover note and an index of the room."),
    (DECK, f"Pitch deck, {N_SLIDES} slides. The last slide is an appendix of key metrics."),
    (SCRIPT, "Two-minute script for the pitch video."),
    (MODEL, "Financial model: assumptions, P&L, revenue by broker, team, cash and runway, cash bridge."),
    (CAP, "Fully diluted cap table with the three SAFEs and the seed round."),
    (LEDGER, "Expense ledger: every payment out of the operating account, by date, vendor and category."),
    (METRICS, "Monthly metrics: revenue, paying brokers, carrier invoices audited."),
    (CUST, "Revenue by customer by month: subscription fees, billings, recoveries and remittances."),
    (MSA, "Master services agreement: Corvane Logistics, our largest customer."),
    (ORDER_OSTLEY, "Order form: Ostley Freight, annual plan."),
    (ORDER_TESS, "Order form: Tessmore Freight, annual plan."),
    (SOW, "Statement of work: Norrgate Software Studio."),
    (BIOS, "Founder and senior team bios."),
]


def build_cover_note():
    story = [P(COMPANY, S_H1),
             P("Data room for the seed round. Data as of 2026-09-30."),
             P("Thank you for taking a look. This is what we have put together so far: the deck, the model, the cap table, our "
               "monthly numbers, revenue by customer, the expense ledger and our main contracts. Ask us for anything that is not here."),
             P(f"{CEO['name']}, Chief Executive Officer", S_SMALL),
             Spacer(1, 10)]
    rows = [["#", "File", "What it is"]]
    for i, (rel, what) in enumerate(ROOM_FILES, 1):
        rows.append([str(i), rel, what])
    story.append(tbl(rows, [28, 236, 240]))
    make_pdf(COVER, story, "Brasswick: cover note and index")


def build_bios():
    story = [P("Founders", S_H1)]
    bios = [(CEO, "Celia ran carrier settlement at a mid-size freight brokerage in New Jersey for nine years. Her team paid about "
                  "fourteen thousand carrier invoices a month and checked a small sample of them by hand. She holds a bachelor's degree "
                  "in supply chain management. She founded Brasswick in 2025."),
            (CTO, "Marcus spent eight years building document extraction for insurance claims software, most recently as a principal "
                  "engineer. He holds a master's degree in computer science. He co-founded Brasswick in 2025.")]
    for p, text in bios:
        story += [P(p["name"], S_H2), P(p["title"], S_SMALL), P(text), Spacer(1, 8)]
    story += [PageBreak(), P("Senior team", S_H1)]
    texts = {"Founding Engineer": "built search and matching systems at a logistics software company and joined Brasswick in 2025.",
             "Customer Success Lead": "worked in carrier relations at a freight brokerage and joined Brasswick in 2025. He onboards each "
                                      "broker and runs the recovery desk."}
    for nm, role in SENIOR:
        story += [P(nm, S_H2), P(role, S_SMALL), P(f"{nm.split()[0]} {texts[role]}")]
    make_pdf(BIOS, story, "Brasswick: founder bios")


def build_contracts():
    big = F["big"]
    story = [P("Master Services Agreement: Corvane Logistics", S_H1),
             P(f"Between {COMPANY} (the Provider) and Corvane Logistics (the Customer). Effective date: 2025-05-01."),
             tbl([["Item", "Detail"],
                  ["Plan", "Network"],
                  ["Platform fee", f"{money(BIG_FEE)} a month, fixed for the initial term."],
                  ["Initial term", "24 months, from 2025-05-01 to 2027-04-30."],
                  ["Renewal", "Renews for 12 months at a time unless either party gives 60 days written notice before the term ends."],
                  ["Payment", "Monthly in advance, net 30 days."],
                  ["Recovery fee", f"{round(RECOVERY_FEE * 100)}% of money recovered from carriers (section 4)."]], [110, 390]),
             PageBreak(),
             P("Terms", S_H1),
             P("1. Services. The Provider checks the Customer's carrier invoices against the load documents before payment and "
               "holds invoices that do not match."),
             P("2. Fees. The platform fee is fixed for the initial term."),
             P("3. Termination. Either party may end this agreement for a material breach that is not fixed within 30 days of written notice."),
             P(f"4. Recovery services. The Provider asks carriers to refund amounts the Customer overpaid on invoices paid before the "
               f"effective date. Carriers pay refunds into the Provider's collection account. The Provider keeps a fee of "
               f"{round(RECOVERY_FEE * 100)}% of each refund and pays the other {round((1 - RECOVERY_FEE) * 100)}% to the Customer "
               f"within 15 days of receipt. Refunds belong to the Customer until they are paid out."),
             P("5. Data. The Customer owns its load and invoice data. The Provider uses it only to run the service."),
             PageBreak(),
             P("Signatures", S_H1),
             P(f"Signed for the Provider: {CEO['name']}, Chief Executive Officer"),
             P("Signed for the Customer: Renata Szabo, Vice President, Carrier Settlement"),
             P("Date: 2025-04-24")]
    make_pdf(MSA, story, "Master services agreement: Corvane Logistics")
    LOC["BF1"].append({"file": MSA, "page": 2, "text": "4. Recovery services.", "label": "refunds belong to the customer; Brasswick keeps 30%"})
    GREEN_LOCS["GF3"].append({"file": MSA, "page": 1, "text": f"{money(BIG_FEE)} a month", "value": BIG_FEE,
                              "label": "platform fee in the signed agreement"})

    def order_form(rel, name, start_label, fee, list_price, signer):
        y, mo = int(start_label[:4]), int(start_label[5:])
        end = datetime.date(y + 1, mo, 1) - datetime.timedelta(days=1)
        annual = 12 * fee
        story = [P(f"Order Form: {name}", S_H1),
                 P(f"Between {COMPANY} (the Provider) and {name} (the Customer). Effective date: {start_label}-01."),
                 tbl([["Item", "Detail"],
                      ["Plan", "Lane" + (", with the carrier portal" if list_price != LIST_PRICE["Lane"] else "")],
                      ["Term", f"12 months, from {start_label}-01 to {end.isoformat()}."],
                      ["Annual fee", f"{money(annual)}, invoiced once, in advance. That is 12 months at {money(fee)} a month, "
                                     f"{round(ANNUAL_DISCOUNT * 100)}% off the {money(list_price)} list price for paying a year up front."],
                      ["Recovery fee", f"{round(RECOVERY_FEE * 100)}% of money recovered from carriers."],
                      ["Renewal", "Renews for 12 months at a time unless either party gives 30 days written notice."]], [110, 390]),
                 PageBreak(),
                 P("Terms", S_H1),
                 P("1. Services. The Provider checks the Customer's carrier invoices against the load documents before payment."),
                 P("2. Fees. The Customer pays the annual fee once, in advance. The service is delivered in every month of the term."),
                 P("3. Termination. Either party may end this order form for a material breach that is not fixed within 30 days of "
                   "written notice. If the Provider ends the service early, it refunds the fee for the months not delivered."),
                 Spacer(1, 18),
                 P(f"Signed for the Provider: {CEO['name']}, Chief Executive Officer"),
                 P(f"Signed for the Customer: {signer}")]
        make_pdf(rel, story, f"Order form: {name}")
        return annual

    o, t = F["ostley"], F["tess"]
    a_o = order_form(ORDER_OSTLEY, o["name"], MONTH_LABELS[o["start"]], o["fee"][LAST], OSTLEY_LIST, "Dorian Feld, Owner")
    a_t = order_form(ORDER_TESS, t["name"], MONTH_LABELS[t["start"]], t["fee"][LAST], LIST_PRICE["Lane"], "Mirela Costa, Operations Director")
    LOC["BF4"].append({"file": ORDER_OSTLEY, "page": 1, "text": f"{money(a_o)}, invoiced once, in advance", "label": "annual fee paid ahead"})
    LOC["BF4"].append({"file": ORDER_OSTLEY, "page": 2, "text": "The service is delivered in every month of the term.", "label": "earned month by month"})
    LOC["DC1"].append({"file": ORDER_TESS, "page": 1, "text": f"{money(a_t)}, invoiced once, in advance", "label": "annual fee paid ahead"})
    LOC["DC1"].append({"file": CUST, "row_key": {"month": MONTH_LABELS[t["start"]], "customer_id": t["id"]}, "column": "billings",
                       "expect": a_t, "label": "the whole annual fee billed in 2026-02"})
    LOC["DC1"].append({"file": CUST, "row_key": {"month": MONTH_LABELS[t["start"]], "customer_id": t["id"]}, "column": "subscription_revenue",
                       "expect": t["fee"][LAST], "label": "revenue in 2026-02 is one month"})
    F["ostley_annual"], F["tess_annual"] = a_o, a_t

    story = [P("Statement of Work No. 2", S_H1),
             P(f"Under the Master Consulting Agreement dated 2025-06-20 between {COMPANY} (the Client) and {STUDIO} (the Contractor)."),
             tbl([["Item", "Detail"],
                  ["Term", "12 months, from 2026-07-01 to 2027-06-30. Follows Statement of Work No. 1 (2025-07-01 to 2026-06-30)."],
                  ["Team", "Three engineers and one quality lead, working with the Client's engineering team."],
                  ["Work", "Invoice matching models, the carrier portal, and connections to brokers' transportation management systems."],
                  ["Fee", f"{money(SOW2_FEE)} a month, invoiced at the start of each month."],
                  ["Additional hours", "$95 an hour, only with the Client's written approval."],
                  ["Ending early", "Either party may end this statement of work on ninety (90) days written notice."]], [110, 390]),
             PageBreak(),
             P("Terms", S_H1),
             P("1. Ownership. All work product belongs to the Client on payment. The Contractor assigns to the Client all rights in it."),
             P("2. Confidentiality. Each party keeps the other's non-public information private."),
             P("3. Staffing. The Contractor names the team members and keeps them on the work for the term where it can."),
             Spacer(1, 18),
             P(f"Signed for the Client: {CTO['name']}, Chief Technology Officer"),
             P("Signed for the Contractor: Jonas Ilves, Managing Director"),
             P("Date: 2026-06-18")]
    make_pdf(SOW, story, "Statement of work: Norrgate Software Studio")
    LOC["BF3"].append({"file": SOW, "page": 1, "text": f"{money(SOW2_FEE)} a month", "label": "contract engineering fee"})
    LOC["BF3"].append({"file": SOW, "page": 1, "text": "ninety (90) days written notice", "label": "cannot end before plan month 4"})
    LOC["BF3"].append({"file": SOW, "page": 1, "text": "12 months, from 2026-07-01 to 2027-06-30", "label": "runs through the first nine plan months"})


# ---------------------------------------------------------------------------------------------
# The pitch video script
# ---------------------------------------------------------------------------------------------
def build_script():
    f = F
    runway_sentence = "With the hires in our plan, that gives us close to three years of runway."
    text = f"""# Brasswick: two-minute pitch script

Read this out loud at a steady pace. Each time stamp marks where that part should begin.

**0:00 Who we are**

Hi, I'm {CEO['name']}, co-founder and CEO of Brasswick. Freight brokers pay thousands of carrier invoices every month. Many of them carry charges nobody agreed to, like detention, lumper fees or the same invoice sent twice. Settlement teams check a few by hand and pay the rest.

**0:20 What it does**

Brasswick reads every carrier invoice and matches it to the load. It checks the rate confirmation, the bill of lading and the proof of delivery. Clean invoices go through. The ones that do not match are held, with the reason, and we write the dispute to the carrier.

**0:40 Traction**

We started charging in May 2025. Revenue over the last twelve months was {money(round(f['ltm_shown']))}. {f['paying'][LAST]} brokers pay us today, and {f['paying'][LAST]} of the {f['ever']} who have ever paid us are still with us.

**1:00 How we make money**

Brokers pay a monthly subscription based on how many loads they move. On invoices they paid before they joined us, we chase the overbilled money back from carriers and keep {round(RECOVERY_FEE * 100)} percent of what we recover.

**1:15 Team**

I ran carrier settlement at a freight brokerage for nine years. My co-founder, {CTO['name']}, built document extraction for insurance claims software. We have {len(STAFF)} full-time people today.

**1:35 The ask**

We are raising three million dollars in a seed round. We will hire {len(HIRES)} people, mostly in sales and engineering. {runway_sentence}

**1:50 Close**

Thank you. I'm {CEO['name'].split()[0]}, and I would love to show you a live invoice.

---

{FOOTER}
"""
    write_text(SCRIPT, text)
    LOC["BF5"].append({"file": SCRIPT, "time": "1:35", "text": runway_sentence, "label": "spoken runway, about 36 months"})
    claim = next(x for x in deck_claims() if x[0] == "Runway")
    LOC["BF5"].append({"file": DECK, "page": N_SLIDES, "claims_row": "Runway", "text": f"Runway {claim[1]} {claim[2]}",
                       "slide_ref": claim[2], "label": "appendix row 'Runway'"})


# ---------------------------------------------------------------------------------------------
# The answer key
# ---------------------------------------------------------------------------------------------
def ledger_sum(vendor, month):
    return round(sum(r[6] for r in F["ledger"] if r[2] == vendor and r[0] == month), 2)


def build_answer_key():
    f = F
    sept = MONTH_LABELS[LAST]
    LOC["BF3"].append({"file": LEDGER, "vendor": STUDIO, "month": sept, "expect": f["studio_sept"], "label": "contract engineering, 2026-09"})
    LOC["BF3"].append({"file": LEDGER, "vendor": CONTRACTOR_PAY, "month": sept, "expect": f["labellers_sept"], "label": "labelling contractors, 2026-09"})
    LOC["DC2"].append({"file": LEDGER, "vendor": CONTROLLER, "month": sept, "expect": CONTROLLER_FEE, "label": "fractional controller, 2026-09"})
    LOC["BF1"].append({"file": LEDGER, "category": "recovery_remittance", "months": [MONTH_LABELS[m] for m in LTM],
                       "expect": f["ltm_remitted"], "label": "remittances to brokers, 2025-10 to 2026-09"})
    LOC["BF1"].append({"file": CUST, "columns": ["recovered_from_carriers", "recovery_fee", "remitted_to_customer"],
                       "label": "per-broker recoveries, Brasswick's fee and the broker's share"})
    flags = [
        {"id": "BF1", "name": "Recoveries counted at their gross amount",
         "mislabel_kind": "c. Gross merchandise value or pass-through money shown as revenue",
         "piece": "traction and revenue",
         "locations": LOC["BF1"],
         "shown": {"value": round(f["ltm_shown"]), "unit": "USD", "label": "deck revenue, last 12 months (P&L total revenue, 2025-10 to 2026-09)",
                   "details": {"recovered_from_carriers_ltm": round(f["ltm_recovered"]), "pass_through_counted": round(f["ltm_remitted"])}},
         "true": {"value": round(f["ltm_net_of_pass_through"]), "unit": "USD",
                  "label": "the same 12 months with the brokers' 70% share taken out",
                  "details": {"revenue_ltm_fully_net": round(f["ltm_true_net"]),
                              "fully_net_note": "Also removes BF4's undelivered months of the Ostley Freight invoice.",
                              "gross_to_net_ratio": round(f["ltm_shown"] / f["ltm_net_of_pass_through"], 3)}},
         "check": "gross_vs_net_revenue",
         "check_description": "Sum remitted_to_customer in revenue_by_customer.csv (or the recovery_remittance lines in expense_ledger.csv) over the 12 months and subtract it from the deck's revenue. The agreement's section 4 says refunds belong to the customer, so only the 30% fee is Brasswick's revenue.",
         "tolerance": 0.01,
         "files_needed": [DECK, MODEL, CUST, LEDGER, MSA],
         "catchable_from_seed_drop": None,
         "decoy": False},
        {"id": "BF2", "name": "The deck's revenue chart starts after a fall",
         "mislabel_kind": "Partial history: a chart that starts after the first revenue month and hides a dip",
         "piece": "traction and revenue",
         "locations": LOC["BF2"],
         "shown": {"value": FIRST_2026, "unit": "first month index", "label": f"chart from {MONTH_LABELS[FIRST_2026]} to {sept}, '{'Revenue grew every month in 2026.'}'",
                   "details": {"chart_start": MONTH_LABELS[FIRST_2026], "months_shown": N_MONTHS - FIRST_2026}},
         "true": {"value": 0, "unit": "first month index", "label": f"revenue history starts {MONTH_LABELS[0]}",
                  "details": {"history_start": MONTH_LABELS[0], "months_hidden": FIRST_2026, "hidden_peak_month": f["hidden_peak_month"],
                              "hidden_peak_total_revenue": round(f["hidden_peak"], 2), "first_chart_month_total_revenue": round(f["jan_2026"], 2),
                              "fall_from_peak": round(f["drop_from_peak"], 3),
                              "why": "Back-audit recoveries for the first brokers peaked in 2025 and then ran out."}},
         "check": "deck_history_vs_metrics",
         "check_description": "Compare the chart's first month with the first month of revenue in monthly_metrics.csv. List the months left out and test whether revenue fell in them: the highest month before the chart against the chart's first month.",
         "tolerance": 0,
         "files_needed": [DECK, METRICS],
         "catchable_from_seed_drop": None,
         "decoy": False},
        {"id": "BF3", "name": "Contractors left out of burn and runway",
         "mislabel_kind": "e. Contractors left out of headcount and burn",
         "piece": "burn and runway",
         "locations": LOC["BF3"],
         "shown": {"value": f["runway_shown"], "unit": "months", "label": "runway in the model and deck",
                   "details": {"avg_net_burn_first_12_months": round(f["burn_shown"]), "plan_professional_services": PROF_PLAN}},
         "true": {"value": f["runway_true"], "unit": "months", "label": "runway when the contractors paid in 2026-09 stay on",
                  "details": {"avg_net_burn_first_12_months": round(f["burn_true"]), "contractor_spend_2026_09": round(f["contractor_rate"], 2),
                              "studio_2026_09": f["studio_sept"], "labellers_2026_09": f["labellers_sept"],
                              "full_time_equivalents_left_out": 6, "sow_notice_days": 90, "sow_end": "2027-06-30"}},
         "check": "contractor_spend_vs_headcount_and_burn",
         "check_description": "Find contractor lines in expense_ledger.csv (vendor and description: contract engineering, contractor payouts). Add the 2026-09 run rate to the plan's professional services, rerun the cash plan from Cash_Runway and compare runway and average burn with the deck.",
         "tolerance": 0.01,
         "files_needed": [LEDGER, MODEL, DECK, SOW],
         "catchable_from_seed_drop": None,
         "decoy": False},
        {"id": "BF4", "name": "An annual prepayment booked as one month's revenue",
         "mislabel_kind": "g. Deferred revenue counted as earned",
         "piece": "traction and revenue",
         "locations": LOC["BF4"],
         "shown": {"value": f["sub_shown"][LAST], "unit": "USD", "label": "deck and model MRR, September 2026",
                   "details": {"ostley_booked_2026_09": f["ostley_annual"], "deferred_revenue_on_bridge": f["deferred"]}},
         "true": {"value": f["contracted_mrr"], "unit": "USD", "label": "subscription revenue earned in September 2026, from the customer file",
                  "details": {"ostley_earned_2026_09": f["ostley"]["fee"][LAST], "ostley_undelivered": f["ostley_gap"],
                              "deferred_revenue_should_be": f["deferred"] + f["ostley_gap"]}},
         "check": "deferred_revenue_vs_earned",
         "check_description": "Sum subscription_revenue in revenue_by_customer.csv for 2026-09 and compare with the P&L and the deck's MRR. The month's P&L figure equals billings, not revenue. Ostley Freight's order form bills a year in advance for service delivered month by month.",
         "tolerance": 0.01,
         "files_needed": [DECK, MODEL, CUST, ORDER_OSTLEY],
         "catchable_from_seed_drop": None,
         "decoy": False},
        {"id": "BF5", "name": "Spoken runway above the deck",
         "mislabel_kind": "A spoken number that disagrees with the deck",
         "piece": "burn and runway",
         "locations": LOC["BF5"],
         "shown": {"value": SPOKEN_RUNWAY, "unit": "months", "label": "spoken in the pitch video at 1:35: close to three years of runway"},
         "true": {"value": f["runway_shown"], "unit": "months", "label": "deck and model runway",
                  "details": {"runway_with_contractors": f["runway_true"]}},
         "check": "spoken_number_vs_claims_page",
         "check_description": "Transcribe the video, find the runway sentence and compare it with the deck's appendix row Runway.",
         "tolerance": 0.1,
         "files_needed": [SCRIPT, DECK],
         "catchable_from_seed_drop": None,
         "decoy": False,
         "note": "The script stands in for the video until Ken records it. Hollis Voice's spoken number is ARR; Brasswick's is runway, so the video scan has to read a different claim."},
    ]
    decoys = [
        {"id": "DC1", "name": "Annual prepayment spread correctly", "locations": LOC["DC1"], "must_not_flag": True,
         "details": {"customer_id": f["tess"]["id"], "annual_fee": f["tess_annual"], "monthly_revenue": f["tess"]["fee"][LAST],
                     "billings_month": MONTH_LABELS[f["tess"]["start"]], "deferred_at_2026_09_30": f["deferred"]},
         "why": "Tessmore Freight paid a year in advance in 2026-02. The billings column shows the whole fee that month, revenue is one twelfth a month, and the cash bridge carries the four undelivered months as deferred revenue. It is the same kind of contract as BF4, booked the right way. A scan that flags it, or reads its billings spike as revenue, is wrong."},
        {"id": "DC2", "name": "A contractor the plan keeps", "locations": LOC["DC2"], "must_not_flag": True,
         "details": {"vendor": CONTROLLER, "monthly_retainer": CONTROLLER_FEE},
         "why": "The fractional controller is paid as a contractor, and the plan keeps the retainer in every month. A scan that flags every contractor line is wrong. Only the contract engineers and labellers are left out."},
        {"id": "DC3", "name": "A cumulative count labelled as cumulative", "locations": LOC["DC3"], "must_not_flag": True,
         "details": {"since_launch": f["invoices_cum"][LAST], "september": f["invoices"][LAST]},
         "why": "The deck gives carrier invoices audited since launch, says so, and gives the September count beside it. The metrics file's column is named since_launch and is the running sum of the monthly column. It is not shown as an active count. A vanity-metric scan that flags any deck number equal to a cumulative column is wrong."},
    ]
    green = [
        {"id": "GF1", "piece": "the pitch itself", "name": "The round adds up", "label": "raise_amount", "number": SEED_RAISE, "unit": "USD",
         "tolerance": 0.01, "locations": GREEN_LOCS["GF1"], "independent_sources": 3,
         "sources_note": "The deck (slide 11), the cap table and the model are three different files."},
        {"id": "GF2", "piece": "retention", "name": "Brokers stay", "label": "paying_brokers", "number": f["paying"][LAST], "unit": "count",
         "tolerance": 0.01, "locations": GREEN_LOCS["GF2"], "independent_sources": 3,
         "sources_note": f"The deck says {f['paying'][LAST]} of {f['ever']}. The customer file has {f['ever']} brokers ever and {f['paying'][LAST]} paying in 2026-09, and the model's Revenue_Build counts the same {f['paying'][LAST]}."},
        {"id": "GF3", "piece": "customers", "name": "The largest account is on paper", "label": "largest_customer_monthly_fee", "number": BIG_FEE,
         "unit": "USD", "tolerance": 0.01, "locations": GREEN_LOCS["GF3"], "independent_sources": 3,
         "sources_note": "The signed agreement, the customer file and the model's Revenue_Build all give the same fixed fee, for every month since 2025-05."},
    ]
    files = [r for (r, _w) in ROOM_FILES] + [CLAIMS_SIDECAR]
    key = {
        "company": "Brasswick (fictional)",
        "synthetic_notice": FOOTER,
        "seed": SEED, "as_of": "2026-09-30",
        "mode": "main",
        "stage": "seed",
        "plants": [x["id"] for x in flags],
        "clean_room": False,
        "room_path": f"data_room/{ROOM.name}",
        "seed_drop_path": None,
        "seed_drop_files": [],
        "full_room_files": files,
        "flags": flags, "decoys": decoys,
        "green_flags": green,
        "green_flags_note": "Positives. Each is a number three different files state the same way. Each sits in a piece with no planted flag: the pitch itself, retention and customers.",
        "deck_claims": F["claims"],
        "facts": {
            "customers_ever_paying": f["ever"], "paying_accounts": f["paying"][LAST], "subscription_revenue_2026_09": f["contracted_mrr"],
            "mrr_shown_2026_09": f["sub_shown"][LAST], "revenue_ltm_shown": round(f["ltm_shown"], 2),
            "revenue_ltm_net_of_pass_through": round(f["ltm_net_of_pass_through"], 2), "revenue_ltm_fully_net": round(f["ltm_true_net"], 2),
            "recovery_fee_share": RECOVERY_FEE,
            "ask": SEED_RAISE, "pre_money": SEED_PRE, "cash": CASH_START, "employees_now": len(STAFF),
            "employees_after_hiring": len(STAFF) + len(HIRES),
            "raised_before_seed": f["raised_total"], "angel_safes": sum(s[1] for s in SAFES), "pre_seed_safe": f["safe_c"],
            "net_loss_before_2025_05": f["net_loss_pre"], "net_loss_2025_05_to_2026_09": round(f["net_loss_actual"], 2),
            "deferred_revenue_on_bridge": f["deferred"], "cash_bridge_difference": f["bridge_diff"],
            "big_customer_id": f["big"]["id"], "big_customer_share": round(f["big_share"], 3),
            "ostley_customer_id": f["ostley"]["id"], "tessmore_customer_id": f["tess"]["id"],
            "churned_customer_id": next(c["id"] for c in f["customers"] if c["role"] == "churn"),
            "contractor_run_rate_2026_09": round(f["contractor_rate"], 2),
            "model_avg_net_burn_12m": round(f["burn_shown"], 2), "true_avg_net_burn_12m": round(f["burn_true"], 2),
            "runway_shown": f["runway_shown"], "runway_true": f["runway_true"],
            "plan_growth": list(GROWTH), "plan_programs_usd_month": PROGRAMS, "plan_other_usd_month": f["other_plan"],
            "plan_office_step": list(OFFICE_STEP), "seed_plan_month": SEED_MONTH, "load_factor": LOAD,
            "team": [{"name": CEO["name"], "title": CEO["title"]}, {"name": CTO["name"], "title": CTO["title"]}]
                    + [{"name": nm, "title": role} for nm, role in SENIOR],
        },
        "counts": {"flags": len(flags), "decoys": len(decoys), "green_flags": len(green),
                   "flags_catchable_from_seed_drop": None, "flags_needing_full_room": None},
        "notes": [
            "Brasswick is a seed company. Its room is one thin tier, sent before a first meeting, so there is no separate seed drop.",
            "Four planted flags are of kinds the Hollis Voice room does not carry: gross against net revenue (BF1), a partial-history chart (BF2), contractors left out of burn (BF3) and deferred revenue counted as earned (BF4). The fifth, a spoken number above the deck (BF5), is the same family as Hollis Voice's PF2b, but on runway, not ARR.",
            "BF3 and BF5 both touch runway. The deck says 29 months, the video says close to three years, and with the contractors kept on the cash lasts 23 months.",
            "BF1 and BF4 both raise the deck's revenue. Each flag's true value removes only its own error. facts.revenue_ltm_fully_net removes both.",
            "Cash reconciles: money raised, less the loss before 2025-05 and the 17 monthly operating results, plus Tessmore's undelivered months, equals cash at 2026-09-30 (sheet Cash_Bridge). The ledger agrees: total spend less billings and recoveries collected equals the P&L loss less the deferred revenue.",
            "The deck's market figures are labelled company estimates and are not planted flags.",
        ],
    }
    KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    KEY_PATH.write_text(json.dumps(key, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------------------------
def main(args):
    """Build the Brasswick room. Called by generate.py with its parsed arguments."""
    global KEY_PATH
    if args.plants.strip().lower() != "all" or args.seed is not None:
        sys.exit("The Brasswick room has one fixed seed and all five flags. Leave out --plants and --seed with --company brasswick.")
    if args.key_out:
        KEY_PATH = Path(args.key_out).expanduser().resolve()
    ROOM.mkdir(parents=True, exist_ok=True)
    build_facts()
    build_tables()
    build_model()
    build_cap_table()
    build_deck()
    build_script()
    build_cover_note()
    build_bios()
    build_contracts()
    build_answer_key()
    n_folders = len({Path(r).parts[0] for (r, _w) in ROOM_FILES})
    print(f"Wrote {len(ROOM_FILES) + 1} files in {n_folders} folders to {ROOM}")
    print(f"Wrote {KEY_PATH}")
    f = F
    print(f"Revenue, last 12 months: shown {f['ltm_shown']:,.2f}; net of pass-through {f['ltm_net_of_pass_through']:,.2f}; fully net {f['ltm_true_net']:,.2f}")
    print(f"MRR 2026-09: shown {f['sub_shown'][LAST]:,}; earned {f['contracted_mrr']:,}")
    print(f"Chart starts {MONTH_LABELS[FIRST_2026]}; history starts {MONTH_LABELS[0]}; hidden peak {f['hidden_peak']:,.2f} in {f['hidden_peak_month']}; "
          f"{MONTH_LABELS[FIRST_2026]} {f['jan_2026']:,.2f}")
    print(f"Runway shown {f['runway_shown']} true {f['runway_true']}; average burn shown {f['burn_shown']:,.0f} true {f['burn_true']:,.0f}; "
          f"contractors {f['contractor_rate']:,.2f} a month")
    print(f"Raised before the seed {f['raised_total']:,}; loss before 2025-05 {f['net_loss_pre']:,}; loss 2025-05 to 2026-09 {f['net_loss_actual']:,.2f}; "
          f"deferred {f['deferred']:,}; cash {CASH_START:,}; bridge difference {f['bridge_diff']:.2f}")
    print(f"Spoken runway {SPOKEN_RUNWAY} months against the deck's {f['runway_shown']}")
    print("Planted flags: BF1, BF2, BF3, BF4, BF5")
