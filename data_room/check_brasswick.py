#!/usr/bin/env python3
"""The Brasswick room's test. Reads the generated files back and checks every planted flag, decoy and green flag.

Run it through check.py with the room's virtual environment:

    data_room/.venv/bin/python data_room/check.py --company brasswick

For each flag it checks that the shown value is where the key says, then rebuilds the true value from the raw
files the way a diligence scan would. It checks the decoys are honest, that the cash reconciles, that the green
flags agree across files, and that the room does not look built to be caught. It exits non-zero on any miss.
"""
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

import openpyxl
import pdfplumber

PASSES, FAILS = [], []
ROOM = KEY = None
_wb, _pdf = {}, {}

DECK = "01_overview/pitch_deck.pdf"
SCRIPT = "01_overview/pitch_video_script.md"
CLAIMS = "01_overview/claims.json"
MODEL = "02_financials/financial_model.xlsx"
CAP = "02_financials/cap_table.xlsx"
LEDGER = "02_financials/expense_ledger.csv"
METRICS = "03_metrics/monthly_metrics.csv"
CUST = "03_metrics/revenue_by_customer.csv"
MSA = "04_contracts/msa_corvane_logistics.pdf"
ORDER_OSTLEY = "04_contracts/order_form_ostley_freight.pdf"
ORDER_TESS = "04_contracts/order_form_tessmore_freight.pdf"
SOW = "04_contracts/sow_norrgate_software_studio.pdf"
COVER = "00_welcome/cover_note_and_index.pdf"
BIOS = "05_team/founder_bios.pdf"
SEPT = "2026-09"
LTM = ["2025-10", "2025-11", "2025-12"] + [f"2026-{m:02d}" for m in range(1, 10)]
# The deck, its sidecar, the video script and the cover note repeat one another, so they count as one source.
NARRATIVE = {DECK, CLAIMS, SCRIPT, COVER}


def ok(name, cond, detail=""):
    (PASSES if cond else FAILS).append(name)
    print(f"{'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail and not cond else ""))
    return cond


def near(a, b, tol_abs=0.0, tol_rel=0.0):
    return abs(a - b) <= max(tol_abs, tol_rel * abs(b))


def workbook(rel, data_only=True):
    if (rel, data_only) not in _wb:
        _wb[(rel, data_only)] = openpyxl.load_workbook(ROOM / rel, data_only=data_only)
    return _wb[(rel, data_only)]


def named(wb, name):
    sheet, cell = wb.defined_names[name].attr_text.split("!")
    return wb[sheet.strip("'")][cell.replace("$", "")].value


def pages(rel):
    if rel not in _pdf:
        with pdfplumber.open(ROOM / rel) as pdf:
            _pdf[rel] = [(p.extract_text() or "") for p in pdf.pages]
    return _pdf[rel]


def squash(t):
    return re.sub(r"\s+", " ", t)


def read_csv(rel):
    with open(ROOM / rel, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def num(s):
    return float(str(s).replace("$", "").replace(",", ""))


def flag(fid):
    return next(f for f in KEY["flags"] if f["id"] == fid)


def decoy(did):
    return next(d for d in KEY["decoys"] if d["id"] == did)


def claim(label):
    return next(c for c in KEY["deck_claims"] if c["label"] == label)["value"]


def pl_row(label):
    ws = workbook(MODEL)["P&L"]
    return next(r for r in range(1, 60) if ws.cell(row=r, column=1).value == label)


def pl_values(label, actual_only=True):
    ws = workbook(MODEL)["P&L"]
    r = pl_row(label)
    months = [ws.cell(row=4, column=c).value for c in range(3, 32)]
    return {m: ws.cell(row=r, column=3 + i).value for i, m in enumerate(months) if (not actual_only or i < 17)}


def file_text(rel):
    if rel.endswith(".pdf"):
        return "\n".join(pages(rel))
    if rel.endswith(".xlsx"):
        return "\n".join(str(c.value) for ws in workbook(rel).worksheets for row in ws.iter_rows() for c in row if isinstance(c.value, str))
    return (ROOM / rel).read_text(encoding="utf-8")


# ---- files ------------------------------------------------------------------------------------
def check_files():
    files = KEY["full_room_files"]
    for rel in files:
        ok(f"file exists: {rel}", (ROOM / rel).is_file())
    present = sorted(str(p.relative_to(ROOM)) for p in ROOM.rglob("*") if p.is_file())
    ok("the room holds exactly the files the key lists", present == sorted(files), str(set(present) ^ set(files)))
    want = {COVER: 1, DECK: 12, MSA: 3, ORDER_OSTLEY: 2, ORDER_TESS: 2, SOW: 2, BIOS: 2}
    for rel, n in want.items():
        ok(f"page count {rel} is {n}", len(pages(rel)) == n, str(len(pages(rel))))
        ok(f"footer on every page of {rel}", all("Synthetic data room for Deal Flow NYC 2026" in p for p in pages(rel)))
    for rel in (MODEL, CAP):
        ok(f"footer on every sheet of {rel}", all(any(isinstance(c.value, str) and c.value.startswith("Synthetic data room")
                                                      for row in ws.iter_rows() for c in row) for ws in workbook(rel).worksheets))
    ok("footer in the video script", "Synthetic data room for Deal Flow NYC 2026" in file_text(SCRIPT))
    dashed = [rel for rel in files if "\u2014" in file_text(rel) or "\u2013" in file_text(rel)]
    ok("no em or en dashes in any room file", not dashed, str(dashed))
    for rel in (MODEL, CAP):
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


def check_nothing_announces_itself():
    words = ["planted", "decoy", "answer key", "red flag", "green flag", "trap", "tricorder"]
    other_room = ["Hollis", "Cedar & Pine", "Marlow", "Brookline", "Imogen", "Teodoro", "Tarrant"]
    for rel in KEY["full_room_files"]:
        t = file_text(rel)
        hit = [w for w in words if w in t.lower()] + [w for w in other_room if w in t]
        ok(f"{rel} names no flag and nothing from the other room", not hit, str(hit))


# ---- the key's own locations --------------------------------------------------------------------
def check_location(tag, loc):
    rel = loc["file"]
    if rel.endswith(".xlsx"):
        wb = workbook(rel)
        if ":" in loc["cell"]:
            vals = [c.value for row in wb[loc["sheet"]][loc["cell"]] for c in row]
            return ok(tag, len(vals) == 12 and all(isinstance(v, (int, float)) for v in vals), str(vals[:3]))
        val = wb[loc["sheet"]][loc["cell"]].value
        if "named_cell" in loc and not ok(tag + " (named cell points here)", named(wb, loc["named_cell"]) == val):
            return False
        exp = loc.get("expect")
        if exp is None:
            return ok(tag, val is not None)
        if isinstance(exp, str):
            return ok(tag, val == exp, f"got {val!r}")
        return ok(tag, isinstance(val, (int, float)) and near(val, exp, 0.01), f"got {val!r} want {exp!r}")
    if rel.endswith(".pdf"):
        return ok(tag, squash(loc["text"]) in squash(pages(rel)[loc["page"] - 1]), f"page {loc['page']}")
    if rel.endswith(".md"):
        t = file_text(rel)
        return ok(tag, squash(loc["text"]) in squash(t) and f"**{loc['time']} " in t)
    rows = read_csv(rel)
    if "row_key" in loc:
        hit = [r for r in rows if all(r[k] == v for k, v in loc["row_key"].items())]
        return ok(tag, len(hit) == 1 and near(num(hit[0][loc["column"]]), loc["expect"], 0.01), str(hit[:1]))
    if "vendor" in loc:
        s = sum(num(r["amount_usd"]) for r in rows if r["vendor"] == loc["vendor"] and r["month"] == loc["month"])
        return ok(tag, near(s, loc["expect"], 0.01), f"{s:,.2f}")
    if "category" in loc:
        s = sum(num(r["amount_usd"]) for r in rows if r["category"] == loc["category"] and r["month"] in loc["months"])
        return ok(tag, near(s, loc["expect"], 0.5), f"{s:,.2f}")
    if "columns" in loc:
        return ok(tag, all(c in rows[0] for c in loc["columns"]))
    return ok(tag + " (unknown location type)", False)


def check_locations():
    for entry in KEY["flags"] + KEY["decoys"]:
        for loc in entry["locations"]:
            what = loc.get("sheet", "") + loc.get("cell", "") + loc.get("text", "")[:40] + loc.get("vendor", "") + loc.get("category", "")
            check_location(f"{entry['id']} location: {loc['file']} {what}", loc)


def check_claims_page():
    last = squash(pages(DECK)[11])
    ok("deck slide 12 is titled Appendix: key metrics", "Appendix: key metrics" in last)
    for c in KEY["deck_claims"]:
        ok(f"appendix row '{c['label']}' reads {c['value']} on slide {c['slide']}", squash(f"{c['label']} {c['value']} {c['slide']}") in last)
    side = json.loads((ROOM / CLAIMS).read_text(encoding="utf-8"))
    ok("claims.json holds the same rows as the appendix and the key", side["claims"] == KEY["deck_claims"])


# ---- the planted flags, rebuilt from raw files --------------------------------------------------
def check_bf1():
    f = flag("BF1")
    metrics = {r["month"]: r for r in read_csv(METRICS)}
    pl_tot = pl_values("Total revenue")
    deck_ltm = num(claim("Revenue, last 12 months"))
    ok("BF1 the deck's 12-month revenue is the P&L total revenue for 2025-10 to 2026-09", near(deck_ltm, sum(pl_tot[m] for m in LTM), 1.0))
    ok("BF1 the metrics export's total revenue agrees with the P&L", all(near(num(metrics[m]["total_revenue"]), pl_tot[m], 0.01) for m in pl_tot))
    cust = read_csv(CUST)
    rec_by = defaultdict(float)
    for r in cust:
        rec_by[r["month"]] += num(r["recovered_from_carriers"])
    ok("BF1 recovery revenue in the P&L is the gross amount recovered from carriers",
       all(near(v, rec_by[m], 0.05) for m, v in pl_values("Recovery revenue").items()))
    ok("BF1 every row splits recoveries into a 30% fee and a 70% remittance",
       all(near(num(r["recovery_fee"]) + num(r["remitted_to_customer"]), num(r["recovered_from_carriers"]), 0.011)
           and near(num(r["recovery_fee"]), 0.3 * num(r["recovered_from_carriers"]), 0.011) for r in cust))
    remit_cust = sum(num(r["remitted_to_customer"]) for r in cust if r["month"] in LTM)
    remit_ledger = sum(num(r["amount_usd"]) for r in read_csv(LEDGER) if r["category"] == "recovery_remittance" and r["month"] in LTM)
    ok("BF1 the customer file's remittances equal the ledger's remittance lines", near(remit_cust, remit_ledger, 0.5), f"{remit_cust:,.2f} vs {remit_ledger:,.2f}")
    ok("BF1 shown value is the deck's figure", near(f["shown"]["value"], deck_ltm, 1.0))
    ok("BF1 true value is the deck's figure less the brokers' share", near(f["true"]["value"], deck_ltm - remit_cust, 1.0),
       f"{deck_ltm - remit_cust:,.0f}")
    full = sum(num(r["subscription_revenue"]) + num(r["recovery_fee"]) for r in cust if r["month"] in LTM)
    ok("BF1 fully net revenue in the key matches the customer file", near(f["true"]["details"]["revenue_ltm_fully_net"], full, 1.0))
    msa = squash("\n".join(pages(MSA)))
    ok("BF1 the agreement says refunds belong to the customer and Brasswick keeps 30%",
       "keeps a fee of 30% of each refund" in msa and "Refunds belong to the Customer" in msa)
    ok("BF1 the pass-through is material (over 15% of net revenue)", remit_cust / (deck_ltm - remit_cust) > 0.15)


def check_bf2():
    f = flag("BF2")
    rows = read_csv(METRICS)
    months = [r["month"] for r in rows]
    tot = [num(r["total_revenue"]) for r in rows]
    deck4 = squash(pages(DECK)[3])
    start, end = claim("Monthly revenue chart").split(" to ")
    ok("BF2 the deck's chart covers 2026-01 to 2026-09", (start, end) == ("2026-01", SEPT) and "Monthly revenue, January 2026 to September 2026" in deck4)
    ok("BF2 revenue history in the metrics export starts earlier, with revenue in its first month", months[0] == "2025-05" and tot[0] > 0)
    i0 = months.index(start)
    hidden = tot[:i0]
    ok("BF2 eight months of revenue are left off the chart", len(hidden) == 8 == f["true"]["details"]["months_hidden"])
    peak = max(hidden)
    ok("BF2 revenue in the hidden months peaked above the chart's first month by 10% or more", peak >= 1.10 * tot[i0],
       f"{peak:,.0f} vs {tot[i0]:,.0f}")
    ok("BF2 the key's peak and fall match the file",
       near(peak, f["true"]["details"]["hidden_peak_total_revenue"], 0.01) and months[hidden.index(peak)] == f["true"]["details"]["hidden_peak_month"]
       and near(1 - tot[i0] / peak, f["true"]["details"]["fall_from_peak"], 0.001))
    ok("BF2 the deck's sentence is true for the months it shows, which is why it misleads",
       "Revenue grew every month in 2026." in deck4 and all(tot[k] > tot[k - 1] for k in range(i0 + 1, len(tot))))


def plan_rows():
    ws = workbook(MODEL)["Cash_Runway"]
    out = []
    for r in range(9, 9 + 48):
        out.append({"t": ws.cell(row=r, column=2).value, "burn": ws.cell(row=r, column=12).value, "raised": ws.cell(row=r, column=13).value,
                    "cash": ws.cell(row=r, column=14).value, "prof": ws.cell(row=r, column=8).value, "acct": ws.cell(row=r, column=9).value})
    return out


def runway_of(rows, extra, cash0):
    cash = cash0
    burns = []
    run = None
    for x in rows:
        b = x["burn"] + extra
        burns.append(b)
        cash += x["raised"] - b
        if cash <= 0 and run is None:
            run = x["t"] - 1
    return (run if run is not None else len(rows)), sum(burns[:12]) / 12


def check_bf3():
    f = flag("BF3")
    wb = workbook(MODEL)
    ledger = read_csv(LEDGER)
    contr = [r for r in ledger if r["month"] == SEPT and re.match(r"(Contract engineering|Additional engineering hours|Contractor payout)", r["description"])]
    rate = sum(num(r["amount_usd"]) for r in contr)
    ok("BF3 the ledger shows contract engineering and labelling paid in 2026-09", len({r["vendor"] for r in contr}) == 2 and rate > 0)
    ok("BF3 the key's contractor run rate matches the ledger", near(rate, f["true"]["details"]["contractor_spend_2026_09"], 0.01), f"{rate:,.2f}")
    ok("BF3 contractors are booked as professional services under G&A", all(r["category"] == "professional_services" and r["booked_as"] == "G&A" for r in contr))
    prof = pl_values("Professional services", actual_only=False)
    months = list(prof)
    ok("BF3 professional services in 2026-09 hold the contractors", prof[SEPT] >= rate)
    ok("BF3 the plan cuts professional services to legal fees only", all(prof[m] == named(wb, "PROF_SERVICES_USD_MONTH") for m in months[17:])
       and named(wb, "PROF_SERVICES_USD_MONTH") < 0.2 * rate)
    rows = plan_rows()
    cash0 = named(wb, "CASH_START")
    run_s, burn_s = runway_of(rows, 0, cash0)
    ok("BF3 the model's runway and burn come from its own cash plan", run_s == named(wb, "RUNWAY_MONTHS") and near(burn_s, named(wb, "AVG_NET_BURN_12M"), 0.01))
    ok("BF3 the deck's runway and burn match the model",
       claim("Runway") == f"{named(wb, 'RUNWAY_MONTHS')} months" and near(num(claim("Average monthly net burn, next 12 months")), named(wb, "AVG_NET_BURN_12M"), 0.5))
    run_t, burn_t = runway_of(rows, rate, cash0)
    ok("BF3 with the contractors kept on, runway and burn match the key's true values",
       run_t == f["true"]["value"] and near(burn_t, f["true"]["details"]["avg_net_burn_first_12_months"], 0.5), f"{run_t} months, {burn_t:,.0f}")
    ok("BF3 the gap is material (3 months or more)", f["shown"]["value"] - run_t >= 3)
    sow = squash(pages(SOW)[0])
    ok("BF3 the statement of work runs to 2027-06-30 and needs 90 days notice", "2027-06-30" in sow and "ninety (90) days written notice" in sow)
    ok("BF3 the deck counts employees only", claim("Full-time employees") == str(named(wb, "EMPLOYEES_NOW")))


def check_bf4():
    f = flag("BF4")
    wb = workbook(MODEL)
    cust = [r for r in read_csv(CUST) if r["month"] == SEPT]
    earned = sum(num(r["subscription_revenue"]) for r in cust)
    billed = sum(num(r["billings"]) for r in cust)
    shown = named(wb, "SUB_REVENUE_2026_09")
    ok("BF4 the P&L, Revenue_Build, metrics export and deck all show the same September MRR",
       shown == named(wb, "MRR_2026_09") == num(claim("MRR, September 2026")) == num(next(r for r in read_csv(METRICS) if r["month"] == SEPT)["subscription_revenue"])
       == f["shown"]["value"])
    ok("BF4 the customer file's September revenue is the key's true value", near(earned, f["true"]["value"], 0.01), f"{earned:,.0f}")
    ok("BF4 the September P&L figure sits nearer billings than revenue, and the gap is over 10%",
       abs(shown - billed) < abs(shown - earned) and abs(shown - earned) / earned > 0.10, f"{shown:,} vs billed {billed:,} vs earned {earned:,}")
    o = next(r for r in cust if r["customer_id"] == KEY["facts"]["ostley_customer_id"])
    ok("BF4 Ostley Freight billed a year in advance in September and earned one month",
       num(o["billings"]) == 12 * num(o["subscription_revenue"]) and near(shown - earned, 11 * num(o["subscription_revenue"]), 0.01))
    form = squash("\n".join(pages(ORDER_OSTLEY)))
    ok("BF4 the order form bills once in advance for service delivered every month",
       f"${12 * int(num(o['subscription_revenue'])):,}, invoiced once, in advance" in form and "delivered in every month of the term" in form)
    ok("BF4 the cash bridge carries no deferred revenue for Ostley", named(wb, "DEFERRED_REVENUE_USD") == decoy("DC1")["details"]["deferred_at_2026_09_30"])


def check_bf5():
    f = flag("BF5")
    t = squash(file_text(SCRIPT))
    ok("BF5 the script says close to three years of runway", "close to three years of runway" in t)
    deck = int(claim("Runway").split()[0])
    ok("BF5 the deck says a shorter runway, and the gap is over 10%", deck == f["true"]["value"] and (f["shown"]["value"] - deck) / deck > 0.10)
    words = len(re.findall(r"[A-Za-z0-9$,%.']+", t.split("---")[0]))
    ok("BF5 the script reads in about two minutes (230 to 380 words)", 230 <= words <= 380, str(words))
    facts = KEY["facts"]
    ok("BF5 every other number in the script agrees with the deck",
       claim("Revenue, last 12 months") in t and f"{facts['paying_accounts']} brokers pay us today" in t
       and f"{facts['paying_accounts']} of the {facts['customers_ever_paying']}" in t and f"{facts['employees_now']} full-time people" in t
       and "three million dollars" in t)


# ---- decoys -------------------------------------------------------------------------------------
def check_decoys():
    wb = workbook(MODEL)
    d1 = decoy("DC1")["details"]
    tess = [r for r in read_csv(CUST) if r["customer_id"] == d1["customer_id"]]
    bill = {r["month"]: num(r["billings"]) for r in tess}
    ok("DC1 Tessmore's whole annual fee is billed in 2026-02 and nothing after",
       bill[d1["billings_month"]] == d1["annual_fee"] and sum(v for m, v in bill.items() if m != d1["billings_month"]) == 0)
    ok("DC1 Tessmore's revenue is one twelfth every month", all(num(r["subscription_revenue"]) == d1["monthly_revenue"] for r in tess) and len(tess) == 8)
    cust = read_csv(CUST)
    feb_rev = sum(num(r["subscription_revenue"]) for r in cust if r["month"] == "2026-02")
    feb_bill = sum(num(r["billings"]) for r in cust if r["month"] == "2026-02")
    ok("DC1 the P&L books February as revenue, not billings", pl_values("Subscription revenue")["2026-02"] == feb_rev != feb_bill)
    ok("DC1 the cash bridge carries Tessmore's four undelivered months", named(wb, "DEFERRED_REVENUE_USD") == 4 * d1["monthly_revenue"])
    ok("DC1 every month but September books revenue, not billings",
       all(near(v, sum(num(r["subscription_revenue"]) for r in cust if r["month"] == m), 0.01) for m, v in pl_values("Subscription revenue").items() if m != SEPT))
    d2 = decoy("DC2")["details"]
    ret = sum(num(r["amount_usd"]) for r in read_csv(LEDGER) if r["vendor"] == d2["vendor"] and r["month"] == SEPT)
    ok("DC2 the fractional controller is paid as a contractor and the plan keeps it in every month",
       ret == d2["monthly_retainer"] == named(wb, "ACCOUNTING_USD_MONTH") and all(x["acct"] == ret for x in plan_rows()))
    d3 = decoy("DC3")["details"]
    rows = read_csv(METRICS)
    run, ok_sum = 0, True
    for r in rows:
        run += int(r["carrier_invoices_audited"])
        ok_sum &= int(r["carrier_invoices_audited_since_launch"]) == run
    ok("DC3 the since-launch column is the running sum of the monthly column", ok_sum)
    ok("DC3 the deck labels the cumulative count as cumulative and gives the month beside it",
       num(claim("Carrier invoices audited since launch")) == run == d3["since_launch"]
       and num(claim("Carrier invoices audited, September 2026")) == int(rows[-1]["carrier_invoices_audited"]) == d3["september"])


# ---- cash and cap table -------------------------------------------------------------------------
def check_cash():
    wb = workbook(MODEL)
    op = pl_values("Operating result")
    loss = -sum(op.values())
    raised = named(wb, "RAISED_SAFE_2025_01") + named(wb, "RAISED_SAFE_2025_07")
    pre, deferred, cash = named(wb, "NET_LOSS_BEFORE_2025_05"), named(wb, "DEFERRED_REVENUE_USD"), named(wb, "CASH_START")
    ok("CASH raised less all losses plus deferred revenue equals cash at 2026-09-30, within a dollar", near(raised - pre - loss + deferred, cash, 1.0),
       f"{raised - pre - loss + deferred:,.2f} vs {cash:,}")
    ok("CASH the bridge sheet's difference is under a dollar", abs(named(wb, "CASH_BRIDGE_DIFF")) < 1.0)
    ok("CASH the loss before 2025-05 is a plausible early spend", 50_000 <= pre <= 250_000, str(pre))
    cust = read_csv(CUST)
    receipts = sum(num(r["billings"]) + num(r["recovered_from_carriers"]) for r in cust)
    spend = sum(num(r["amount_usd"]) for r in read_csv(LEDGER))
    ok("CASH ledger spend less cash collected equals the P&L loss less deferred revenue", near(spend - receipts, loss - deferred, 1.0),
       f"{spend - receipts:,.2f} vs {loss - deferred:,.2f}")
    ok("CASH the key's raised total matches the model", raised == KEY["facts"]["raised_before_seed"])


def check_cap_table():
    cap = workbook(CAP)["Cap_Table"]
    rows = {cap.cell(row=r, column=1).value: r for r in range(1, 60) if isinstance(cap.cell(row=r, column=1).value, str)}
    tr = rows["Total"]
    holders = range(5, tr)
    total = cap.cell(row=tr, column=3).value
    ok("CAP holders add to the total and to 100 percent",
       sum(cap.cell(row=r, column=3).value for r in holders) == total and near(sum(cap.cell(row=r, column=4).value for r in holders), 1.0, 1e-9))
    safe_rows = range(rows["Investor"] + 1, rows["Total SAFEs"])
    amts = [cap.cell(row=r, column=2).value for r in safe_rows]
    caps = [cap.cell(row=r, column=3).value for r in safe_rows]
    shares = [cap.cell(row=r, column=6).value for r in safe_rows]
    ok("CAP each SAFE converts at its cap", all(near(s, a * total / c, 0.5) for s, a, c in zip(shares, amts, caps)))
    ok("CAP the SAFE amounts add to the money raised", sum(amts) == KEY["facts"]["raised_before_seed"])
    ok("CAP the share total is not a round number of millions", total % 1_000_000 != 0, str(total))


# ---- green flags --------------------------------------------------------------------------------
def read_green(loc):
    rel = loc["file"]
    if rel.endswith(".xlsx"):
        wb = workbook(rel)
        v = wb[loc["sheet"]][loc["cell"]].value
        if "named_cell" in loc and named(wb, loc["named_cell"]) != v:
            return None
        return v
    if rel.endswith(".pdf"):
        if squash(loc["text"]) not in squash(pages(rel)[loc["page"] - 1]):
            return None
        nums = [float(x.replace(",", "")) for x in re.findall(r"\d[\d,]*(?:\.\d+)?", loc["text"])]
        return loc["value"] if any(near(n, loc["value"], 0.01) for n in nums) else None
    rows = read_csv(rel)
    if "count_rows" in loc:
        return sum(1 for r in rows if all(r[k] == v for k, v in loc["count_rows"].items()) and num(r[loc["where_positive"]]) > 0)
    hit = [r for r in rows if all(r[k] == v for k, v in loc["row_key"].items())]
    return num(hit[0][loc["column"]]) if len(hit) == 1 else None


def check_green_flags():
    gfs = KEY["green_flags"]
    flagged = {f["piece"] for f in KEY["flags"]} | {"team"}      # BF3 also touches team
    ok("green flags: two or more, each in a piece with no planted flag", len(gfs) >= 2 and not ({g["piece"] for g in gfs} & flagged))
    for g in gfs:
        tag = f"{g['id']} ({g['piece']}, {g['number']:,})"
        vals = [read_green(l) for l in g["locations"]]
        ok(f"{tag}: every location is found and agrees within 1 percent", all(v is not None and near(v, g["number"], 0, g["tolerance"]) for v in vals), str(vals))
        files = {l["file"] for l in g["locations"]}
        indep = len(files - NARRATIVE) + (1 if files & NARRATIVE else 0)
        ok(f"{tag}: {indep} independent sources, as the key says", indep >= 2 and indep == g["independent_sources"])
    cust = read_csv(CUST)
    ok("GF2 the customer file holds 15 brokers ever and 14 in 2026-09",
       len({r["customer_id"] for r in cust}) == KEY["facts"]["customers_ever_paying"] == 15)
    big = [num(r["subscription_revenue"]) for r in cust if r["customer_id"] == KEY["facts"]["big_customer_id"]]
    ok("GF3 the largest customer paid the same fixed fee in all 17 months", len(big) == 17 and len(set(big)) == 1)
    share = big[-1] / sum(num(r["subscription_revenue"]) for r in cust if r["month"] == SEPT)
    ok("GF3 the deck's largest-customer share is honest", claim("Largest customer") == f"{round(share * 100)}% of subscription revenue")


# ---- the room does not look built ---------------------------------------------------------------
def check_realism():
    cust = read_csv(CUST)
    ids = sorted({r["customer_id"] for r in cust})
    ok("customer ids are ordinary (C and four digits)", all(re.fullmatch(r"C\d{4}", i) for i in ids))
    first = {}
    for r in cust:
        first.setdefault(r["customer_id"], r["month"])
    ok("customer ids run in start order", [first[i] for i in ids] == sorted(first[i] for i in ids))
    fees = {num(r["subscription_revenue"]) for r in cust if r["month"] == SEPT}
    ok("September fees are not just list prices (8 or more distinct values)", len(fees) >= 8, str(len(fees)))
    gm = list(pl_values("Gross margin").values())
    ok("gross margin varies over the 17 actual months", len({round(x, 4) for x in gm}) >= 12 and max(gm) - min(gm) > 0.02)
    pay = list(pl_values("Payroll").values())
    ok("payroll does not rise by one fixed amount", len({round(b - a, 2) for a, b in zip(pay, pay[1:]) if b > a}) >= 6)
    ledger = read_csv(LEDGER)
    rent = {r["amount_usd"] for r in ledger if r["category"] == "rent"}
    ok("rent moves in lease steps", len(rent) <= 3)
    vendors = {r["vendor"] for r in ledger if r["category"] != "recovery_remittance"}
    ok("the ledger has 12 or more vendors and none called Various", len(vendors) >= 12 and "Various" not in vendors, str(len(vendors)))
    team = workbook(MODEL)["Team"]
    pays = [team.cell(row=r, column=4).value for r in range(1, 40) if isinstance(team.cell(row=r, column=4).value, (int, float))]
    ok("salaries are not all multiples of 5,000", sum(1 for x in pays if x % 5000) >= 6)
    cover = squash("\n".join(pages(COVER))).lower()
    ok("cover note does not promise every number ties", "every number" not in cover and "ties" not in cover)
    ok("the cover note lists every file", all(rel in squash("\n".join(pages(COVER))) for rel in KEY["full_room_files"] if rel != CLAIMS))
    bios = squash("\n".join(pages(BIOS)))
    team_names = [t["name"] for t in KEY["facts"]["team"]]
    ok("team names agree across the deck, bios and script", all(n in bios and n in squash(pages(DECK)[8]) for n in team_names)
       and all(n in file_text(SCRIPT) for n in team_names[:2]))


def check_key_shape():
    flags, decoys = KEY["flags"], KEY["decoys"]
    ok("the key's counts match its lists", KEY["counts"]["flags"] == len(flags) and KEY["counts"]["decoys"] == len(decoys)
       and KEY["counts"]["green_flags"] == len(KEY["green_flags"]))
    ok("the key's plants are its flags", KEY["plants"] == [f["id"] for f in flags])
    new_kinds = [f for f in flags if f["id"] in ("BF1", "BF2", "BF3", "BF4")]
    ok("at least two flags of kinds the Hollis Voice room does not carry", len(new_kinds) >= 2
       and all(f["mislabel_kind"][:2] in ("c.", "e.", "g.") or f["mislabel_kind"].startswith("Partial history") for f in new_kinds))
    ok("at least two decoys and two green flags", len(decoys) >= 2 and len(KEY["green_flags"]) >= 2)
    ok("every flag names locations, a shown and a true value and a check",
       all(f["locations"] and "value" in f["shown"] and "value" in f["true"] and f["check"] for f in flags))
    ok("every file a flag needs is in the room", all(x in KEY["full_room_files"] for f in flags for x in f["files_needed"]))
    ok("the key says this is a seed room with no seed drop", KEY["stage"] == "seed" and KEY["seed_drop_path"] is None)


def run(room, key):
    global ROOM, KEY
    ROOM = Path(room).expanduser().resolve()
    KEY = json.loads(Path(key).expanduser().read_text(encoding="utf-8"))
    print(f"Checking {ROOM} against the key with plants: {', '.join(KEY['plants'])}")
    check_files()
    check_nothing_announces_itself()
    check_locations()
    check_claims_page()
    check_bf1()
    check_bf2()
    check_bf3()
    check_bf4()
    check_bf5()
    check_decoys()
    check_cash()
    check_cap_table()
    check_green_flags()
    check_realism()
    check_key_shape()
    print(f"\n{len(PASSES)} passed, {len(FAILS)} failed")
    if FAILS:
        print("FAILED: " + "; ".join(FAILS))
        return 1
    print("All planted flags, decoys and green flags are in the room exactly as the answer key says.")
    return 0
