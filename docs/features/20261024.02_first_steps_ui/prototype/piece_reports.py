"""Analyses for every piece of the company that Kimmy's two reports do not cover, one per piece, for Ploy and Sazabi.

Each analysis reads the room through a knowledge file in knowledge/<piece>.md, written by the Tricorder team from the
document guides and FRAMEWORKS.md. Every number here is computed from the synthetic room that synthetic_rooms.py
builds (imported, never edited), and asserted against the room's own figures where the room states them.

Writes piece_reports_data.js (window.TC_PIECE_REPORTS = {slug: [report, ...]}) and copies the knowledge files beside
the page so each analysis can link the file it was read with. piece_reports.js draws them.

Run: python3 piece_reports.py
"""

from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))

from synthetic_rooms import file_of, millions, money, month_label, pct, ploy_room, sazabi_room  # noqa: E402

# The order the analyses show in, after Kimmy's two. A piece shows only when its knowledge file exists.
ORDER = ["retention", "unit_economics", "customers", "market", "team", "the_pitch_itself", "legal_and_cap_table", "outside_world"]
TOL = 1e-6


def num(s: str) -> float:
    """A figure the room writes as text ("$4,650", "14.29%", "18") as a number."""
    return float(re.sub(r"[^0-9.\-]", "", s))


def close(a: float, b: float, rel: float = 1e-6) -> bool:
    return abs(a - b) <= rel * max(1.0, abs(a), abs(b))


class Room:
    """The room with lookups the analyses use."""

    def __init__(self, room: dict, facts: dict, slug: str):
        self.r, self.f, self.slug = room, facts, slug
        self.C = room["claims"]

    def v(self, cid: str) -> float:
        return self.C[cid]["value"]

    def quote(self, cid: str, i: int = 0) -> str:
        return self.C[cid]["sources"][i]["quote"]

    def panel(self, piece: str) -> dict:
        return next(d["panel"] for d in self.r["drill"] if d["piece"] == piece)

    def drill_gaps(self, piece: str) -> list[str]:
        return next((d["gaps"] for d in self.r["drill"] if d["piece"] == piece), [])

    def report(self, key: str) -> dict:
        return next(x for x in self.r["reports"] if x["key"] == key)

    def label(self, piece: str) -> str:
        return next(p["label"] for p in self.r["pieces"] if p["name"] == piece)


def build(room: Room, piece: str, paras: list[dict], asks: list[str], chart: dict) -> dict:
    for p in paras:
        for cid in p["refs"]:
            assert cid in room.C, f"{room.slug} {piece}: no claim {cid}"
    needs = sorted({file_of(s) for p in paras for cid in p["refs"] for s in room.C[cid]["sources"]} - {None})
    return {"key": f"piece-{piece}", "piece": piece, "title": room.label(piece), "knowledge": f"knowledge/{piece}.md",
            "paras": paras, "asks": asks, "chart": chart, "needs": needs}


# Retention -----------------------------------------------------------------------------------------------------


def retention_ploy(R: Room) -> dict:
    churn = R.v("re-1")
    assert close(churn, float(R.quote("re-1"))), "the churn figure is the model's cell"
    months = list(range(13))
    left = [100 * (1 - churn) ** k for k in months]
    history = R.report("traction_and_revenue")["chart"]["months"]
    n_hist = len(history)
    return build(R, "retention", [
        {"lead": "Only the model states it.", "refs": ["re-1"],
         "body": f"The model assumes monthly churn of {pct(churn)}. No other file in the room states a retention figure, "
                 "and the model does not say whether it counts customers or revenue."},
        {"lead": "What that means over a year.", "refs": ["re-1"],
         "body": f"Compounded for 12 months, {pct(churn)} a month leaves {left[12]:.1f}% of the starting customers or revenue. "
                 "One SaaS investor reads gross retention under 80% as a churn problem to fix before scaling."},
        {"lead": "The record is too short to test it.", "refs": ["tr-3"],
         "body": f"The customer file runs from {history[0]} to {history[-1]}: {n_hist} months. A 12-month retention figure needs 12 months, "
                 "so the room can neither confirm nor rebuild the model's churn."},
        {"lead": "Gross and net are both missing.", "refs": [],
         "body": "Net retention would show whether customers who stay spend more. Gross retention would show what is lost. "
                 "The room shows neither, so the retention piece reads not enough in the room."},
    ], [
        f"Does the {pct(churn)} monthly churn count customers or revenue, and what data is it based on?",
        f"A cohort export from {history[0]}, with gross and net revenue retention at each month.",
        "Churn split by plan, with self-serve and enterprise apart.",
    ], {"kind": "line", "unit": "percent", "x": months, "x_title": "Months after a customer starts",
        "series": [{"name": f"The model's {pct(churn)} a month, compounded", "y": [round(v, 2) for v in left], "style": "plan"}],
        "line": {"y": 80, "label": "80%: one investor's gross retention line"},
        "mark": {"x": n_hist - 1, "label": f"Oldest customers in the file: {n_hist - 1} months in"},
        "end": f"{left[12]:.1f}% at 12 months",
        "label": f"Share of customers or revenue left each month at the model's {pct(churn)} monthly churn: {left[12]:.1f}% after 12 months, "
                 f"under the 80% line. The oldest customers in the file are {n_hist - 1} months in."})


def retention_sazabi(R: Room) -> dict:
    rows = R.panel("retention")["rows"]
    plans = [r for r in rows if r[0] != "All"]
    allrow = next(r for r in rows if r[0] == "All")
    jun = [num(r[2]) for r in plans]
    sep = [num(r[4]) for r in plans]
    teams_jun, teams_sep = sum(num(r[1]) for r in plans), sum(num(r[3]) for r in plans)
    assert close(sum(jun), num(allrow[2])) and close(sum(sep), num(allrow[4])), "plan rows add to the All row"
    nrr = sum(sep) / sum(jun)
    assert close(nrr, R.v("re-1")), "net revenue retention matches the room's claim"
    logo = teams_sep / teams_jun
    churn = 1 - logo ** (1 / 3)
    assert close(churn, R.v("re-3")), "monthly churn matches the room's claim"
    lost = int(teams_jun - teams_sep)
    return build(R, "retention", [
        {"lead": "What the room shows.", "refs": ["re-1"],
         "body": f"The {int(teams_jun)} teams paying in 2026-06 paid {money(sum(jun))} a month then and {money(sum(sep))} in 2026-09. "
                 f"Net revenue retention is {pct(nrr)}. The deck says above {pct(R.v('re-2'), 0)}, and the customer file bears it out."},
        {"lead": "Revenue held better than customers.", "refs": ["re-1", "re-3"],
         "body": f"{int(teams_sep)} of the {int(teams_jun)} teams still pay: {pct(logo)} of customers. Revenue retention above customer retention "
                 "means the teams that stay moved to bigger plans, which is what an investor wants to see."},
        {"lead": "Gross retention is not shown.", "refs": ["re-2"],
         "body": "Net retention blends upgrades with losses. The room gives no gross retention, so the loss on its own is not visible. "
                 "The customer file can produce it team by team."},
        {"lead": "Three months is a short record.", "refs": ["re-3"],
         "body": f"{lost} team left, which works out to {pct(churn)} a month. With {int(teams_jun)} teams, one more loss moves every percentage a long way. "
                 f"A 12-month figure needs data to {month_label('2026-06', 12)}."},
    ], [
        "Gross revenue retention for the 2026-06 cohort, team by team.",
        "The 2026-07 and 2026-08 cohorts on the same basis.",
        "Why the team that left did so.",
    ], {"kind": "bars", "unit": "usd", "barmode": "group", "x": [r[0] for r in plans], "x_title": "Plan in 2026-06",
        "series": [{"name": f"2026-06: {int(teams_jun)} teams", "y": jun, "style": "plan"},
                   {"name": f"2026-09: {int(teams_sep)} of them still paying", "y": sep, "style": "good"}],
        "label": f"Monthly revenue from the teams paying in 2026-06, by the plan they started on: {money(sum(jun))} then and {money(sum(sep))} in 2026-09, "
                 f"net revenue retention of {pct(nrr)}."})


# Team ----------------------------------------------------------------------------------------------------------


def hiring(R: Room) -> dict:
    """The hiring plan as the room states it: total hires, how many the model's burn carries, and what the rest cost."""
    total = int(num(R.quote("bu-2", 0)))
    in_model = int(num(R.quote("bu-2", 1)))
    extra = R.r["whatif"]["extra_hires"]
    assert len(extra) == R.r["whatif"]["extra_count"] == total - in_model, "the hires outside the model add up"
    return {"total": total, "in_model": in_model, "extra": len(extra), "extra_cost": sum(h["monthly_cost"] for h in extra),
            "last_start": max(h["start"] for h in extra)}


def team_chart(team: int, h: dict) -> dict:
    return {"kind": "bars", "unit": "count", "barmode": "stack", "x": ["Today", "After the hiring plan"],
            "series": [{"name": "Team today", "y": [team, team], "style": "plan"},
                       {"name": "Hires the model's burn carries", "y": [0, h["in_model"]], "style": "good"},
                       {"name": "Hires outside the model's burn", "y": [0, h["extra"]], "style": "bad",
                        "text": ["", f"{team + h['total']} people"], "textposition": "outside"}],
            "label": f"Team of {team} today. The hiring plan adds {h['total']}, to {team + h['total']}. "
                     f"The model's burn carries {h['in_model']} of them and leaves {h['extra']} out."}


def team_ploy(R: Room) -> dict:
    team = int(R.v("te-1"))
    h = hiring(R)
    grows = "more than doubles it" if team + h["total"] > 2 * team else "grows it"
    return build(R, "team", [
        {"lead": "The headcount matches the public record.", "refs": ["te-1"],
         "body": f"The deck, the model and the YC page all say {team} people today. The company's files and the public record agreeing on headcount is a small green flag."},
        {"lead": f"The hiring plan {grows}.", "refs": ["bu-2"],
         "body": f"The plan adds {h['total']} people, which takes the team to {team + h['total']}. The model's burn carries {h['in_model']} of them."},
        {"lead": "The hires the model leaves out.", "refs": ["bu-2"],
         "body": f"The other {h['extra']} hires add {money(h['extra_cost'])} a month once all have started, by month {h['last_start']}. "
                 "Payroll is usually the largest part of burn, so a plan the model does not pay for makes the runway look longer than it is."},
        {"lead": "Who owns each function.", "refs": [],
         "body": "The room holds a founder bio and a hiring plan, but no org chart naming who leads sales, product and finance today. "
                 "That is the next thing to ask for."},
    ], [
        f"Which of the {h['total']} hires the round pays for first, and the milestone each one supports.",
        "An org chart or payroll list naming everyone counted today, with contractors marked.",
        "Founder vesting schedules and retention terms for key people.",
    ], team_chart(team, h))


def team_sazabi(R: Room) -> dict:
    team, eng = int(R.v("te-1")), int(R.v("te-2"))
    brex = int(num(R.quote("te-2", 1)))
    h = hiring(R)
    return build(R, "team", [
        {"lead": "The team matches the public record.", "refs": ["te-1", "te-2"],
         "body": f"The model and the YC page say {team} people. The staff list and the launch post say {eng} of them are engineers, "
                 f"{brex} from Brex. Independent sources agreeing is a small green flag."},
        {"lead": "Almost everyone builds.", "refs": ["te-2"],
         "body": f"{team - eng} of the {team} works outside engineering. That is a fact to report, not a score. "
                 "The question is who owns selling as the company moves from design partners to paying teams."},
        {"lead": "The hiring plan.", "refs": ["bu-2"],
         "body": f"The plan adds {h['total']} people, to {team + h['total']}. The model's burn carries {h['in_model']}. "
                 f"The other {h['extra']} add {money(h['extra_cost'])} a month once they start, by month {h['last_start']}."},
    ], [
        f"Which of the {h['total']} hires the seed pays for first, and the milestone each one supports.",
        "Who owns sales today, and when the first sales hire starts.",
        "Founder vesting schedules and retention terms for the early Brex engineers.",
    ], team_chart(team, h))


# Unit economics ------------------------------------------------------------------------------------------------

# knowledge/unit_economics.md: Bessemer's cloud average and a16z's observation for AI companies, as reference lines.
BESSEMER_GM = 65   # "Cloud software averages 65 to 70 percent gross margin in Bessemer's data"
A16Z_AI_GM = 55    # a16z: AI gross margins "often in the 50-60% range"; the line marks the middle


def where(gm: float) -> str:
    """Where a margin sits against the two reference ranges in knowledge/unit_economics.md."""
    g = gm * 100
    if g < 50:
        return "below a16z's 50 to 60% for AI companies"
    if g <= 60:
        return "inside a16z's 50 to 60% range for AI companies"
    if g < BESSEMER_GM:
        return "between the AI range and Bessemer's cloud average"
    if g <= 70:
        return "inside Bessemer's 65 to 70% cloud average"
    return "above Bessemer's 65 to 70% cloud average"


def margin_chart(views: list[str], gp: list[float], costs: list[dict], rev: float) -> dict:
    """Each bar is 100% of revenue: gross profit at the bottom, so its top is the margin, then each cost on top."""
    share = lambda xs: [round(100 * x / rev, 2) for x in xs]
    return {"kind": "bars", "unit": "percent", "barmode": "stack", "x": views, "range": [0, 100],
            "series": [{"name": "Gross profit", "y": share(gp), "style": "good", "text": [f"{100 * g / rev:.1f}% margin" for g in gp], "textposition": "inside", "textanchor": "start"}]
            + [{"name": c["name"], "y": share(c["y"]), "style": c["style"]} for c in costs],
            "lines": [{"y": BESSEMER_GM, "label": f"Bessemer: cloud software averages {BESSEMER_GM} to 70%", "style": "accent", "right": True},
                      {"y": A16Z_AI_GM, "label": "a16z: AI companies often 50 to 60%", "style": "plan", "right": True, "below": True}]}


def unit_economics_ploy(R: Room) -> dict:
    rows = {r[0]: r for r in R.panel("unit_economics")["rows"]}
    rev = num(next(r for k, r in rows.items() if k.startswith("Revenue"))[1])
    hosting, support, inference = num(rows["Hosting"][1]), num(rows["Support"][1]), num(rows["Model inference"][1])
    assert close(rev, R.v("tr-2") / 12), "September revenue is the model's MRR"
    assert close(inference, num(R.quote("ue-3", 0).split()[-1])), "inference matches the ledger row"
    gm_model, gm_full = 1 - (hosting + support) / rev, 1 - (hosting + support + inference) / rev
    assert close(gm_model, R.v("ue-2")) and close(gm_full, R.v("ue-3")), "margins match the room's claims"
    deck = R.v("ue-1")
    gaps = R.drill_gaps("unit_economics")
    assert any("acquisition cost" in g for g in gaps), "the room says acquisition cost is not in it"
    chart = margin_chart(["The model's books", "With inference in cost of revenue"],
                         [rev - hosting - support, rev - hosting - support - inference],
                         [{"name": "Hosting and support", "y": [hosting + support] * 2, "style": "plan"},
                          {"name": "Model inference", "y": [0, inference], "style": "bad"}], rev)
    chart["label"] = (f"Gross margin, each bar 100% of September revenue of {money(rev)}: {pct(gm_model)} on the model's books, "
                      f"{pct(gm_full)} with model inference in cost of revenue. Bessemer's cloud average is 65 to 70%.")
    return build(R, "unit_economics", [
        {"lead": "What it costs to serve.", "refs": ["ue-2"],
         "body": f"September revenue was {money(rev)}. The model counts {money(hosting)} of hosting and {money(support)} of support as cost of revenue, "
                 f"for a gross margin of {pct(gm_model)}."},
        {"lead": "Inference is a delivery cost.", "refs": ["ue-3", "ue-1"],
         "body": f"Model inference cost {money(inference)} in September, and the ledger books it under research and development. "
                 f"The product runs the model to do each customer's work, so it belongs in cost of revenue. Counted there, gross margin is {pct(gm_full)}. The deck says {pct(deck, 0)}."},
        {"lead": "Against the benchmarks.", "refs": ["ue-3"],
         "body": f"Bessemer's cloud companies average 65 to 70%. a16z sees AI companies often at 50 to 60%. "
                 f"At {pct(gm_full)} the margin sits {where(gm_full)}. The deck's {pct(deck, 0)} is {where(deck)}."},
        {"lead": "Prices check out. Acquisition cost is missing.", "refs": ["ue-4"],
         "body": "The model's prices match the public pricing page. The room holds no acquisition cost or payback period, "
                 "so what a customer earns against what it costs to win cannot be checked."},
    ], [
        "Model inference invoices for July to September, and how the cost moves with usage.",
        "Gross margin by plan, with inference in cost of revenue.",
        "Acquisition cost and payback by channel, with payback measured on gross profit.",
    ], chart)


def unit_economics_sazabi(R: Room) -> dict:
    rev = R.v("tr-2") / 12
    recurring = R.v("tr-3") / 12
    gm_model, gm_full, deck = R.v("ue-2"), R.v("ue-3"), R.v("ue-1")
    credits = (gm_model - gm_full) * rev
    assert close(credits, -num(R.quote("ue-3", 0))), "credits match the cloud bill's credits column"
    paid = (1 - gm_model) * rev
    cloud_net = num(R.quote("ue-3", 1))
    inference = paid - cloud_net
    cloud_gross = cloud_net + credits
    gm_recurring = 1 - (paid + credits) / recurring
    chart = margin_chart(["The model's books", "At full cloud price"],
                         [rev - paid, rev - paid - credits],
                         [{"name": "Cloud paid in cash, and inference", "y": [paid, paid], "style": "plan"},
                          {"name": "Cloud paid by credits", "y": [0, credits], "style": "bad"}], rev)
    chart["label"] = (f"Gross margin, each bar 100% of September revenue of {money(rev)}: {pct(gm_model)} on the model's books, "
                      f"{pct(gm_full)} with the cloud bill at full price. Bessemer's cloud average is 65 to 70%.")
    return build(R, "unit_economics", [
        {"lead": "What it costs to serve.", "refs": ["ue-2"],
         "body": f"September revenue in the model was {money(rev)}. Cost of revenue is {money(cloud_net)} of cloud after credits and "
                 f"{money(inference)} of model inference, for a gross margin of {pct(gm_model)}."},
        {"lead": "Credits pay part of the bill.", "refs": ["ue-3", "ue-1"],
         "body": f"Cloud credits covered {money(credits)} of the {money(cloud_gross)} cloud bill. Credits run out, so the margin to plan on prices the cloud in full: "
                 f"{pct(gm_full)}. The deck says {pct(deck, 0)}."},
        {"lead": "On recurring revenue alone.", "refs": ["tr-3"],
         "body": f"September revenue includes a one-time backfill. On recurring revenue of {money(recurring)}, with the cloud at full price, "
                 f"gross margin is {pct(gm_recurring)}: {where(gm_recurring)}."},
        {"lead": "Prices check out. Acquisition cost is missing.", "refs": ["ue-4"],
         "body": "The model's prices match the public pricing page. The room holds no acquisition cost or payback, "
                 "so what a team earns against what it costs to win cannot be checked."},
    ], [
        "Cloud invoices for July to September, with the credit balance and the date the credits expire.",
        "What it costs to serve the free design partners, and where that cost sits.",
        "Acquisition cost and payback, with payback measured on gross profit.",
    ], chart)


# Customers -----------------------------------------------------------------------------------------------------

CONCENTRATION_LINE = 20  # knowledge/customers.md: MicroVentures, "more than 20% of a company's total revenue"


def lines(R: Room) -> dict:
    return {l["name"]: l["units"] * l["price"] for l in R.r["whatif"]["lines"]}


def share_chart(names: list[str], values: list[float], total: float, styles: list[str], extra_lines: list[dict], label: str) -> dict:
    return {"kind": "bars", "unit": "percent", "orientation": "h", "x": names, "height": 80 + 44 * len(names),
            "series": [{"name": "Share", "y": [round(100 * v / total, 2) for v in values], "styles": styles,
                        "text": [f"{100 * v / total:.1f}%" for v in values]}],
            "lines": extra_lines + [{"y": CONCENTRATION_LINE, "label": "20%: a common investor threshold", "style": "bad"}],
            "label": label}


def customers_ploy(R: Room) -> dict:
    L = lines(R)
    model_mrr, sub_mrr = R.v("tr-2") / 12, R.v("tr-3") / 12
    pilot = R.r["whatif"]["pilot"]
    assert close(model_mrr - sub_mrr, pilot["mrr"]), "the pilot is the gap between the model's MRR and the rebuilt one"
    assert close(sum(L.values()), sub_mrr), "plans and contracts add to subscription MRR"
    name, largest = R.quote("cu-1").rsplit(",", 1)
    largest = float(largest)
    assert close(largest / model_mrr, R.v("cu-1")), "the largest customer's share matches the room's claim"
    units = {l["name"]: l["units"] for l in R.r["whatif"]["lines"]}
    paying = int(R.v("tr-4"))
    n_ent = paying - units["Starter plan"] - units["Pro plan"] - 1
    assert n_ent >= 1
    pilot_months = int(re.search(r"(\d+)-month pilot", R.quote("tr-3", 1)).group(1))
    credit_ws = int(num(R.quote("tr-4", 0).split()[0]))
    self_serve = L["Starter plan"] + L["Pro plan"]
    names = [f"{pilot['name']}, the pilot", f"{name}, largest contract", f"The other {n_ent - 1} contracts",
             f"Pro plans, {units['Pro plan']} workspaces", f"Starter plans, {units['Starter plan']} workspaces"]
    vals = [pilot["mrr"], largest, L["Enterprise contracts"] - largest, L["Pro plan"], L["Starter plan"]]
    chart = share_chart(names, vals, model_mrr, ["bad", "mixed", "plan", "plan", "plan"],
                        [{"y": 10, "label": "Deck: no customer above 10%", "style": "accent"}],
                        f"Share of September revenue of {money(model_mrr)}: the pilot {pct(pilot['mrr'] / model_mrr)}, "
                        f"the largest contract {pct(largest / model_mrr)}, Pro plans {pct(L['Pro plan'] / model_mrr)}.")
    return build(R, "customers", [
        {"lead": "The largest contract is small.", "refs": ["cu-1"],
         "body": f"{name} pays {money(largest)} a month: {pct(largest / model_mrr)} of September revenue. "
                 "Its order form agrees with the customer file, and the deck says no customer is above 10%."},
        {"lead": "The pilot is the biggest single payer.", "refs": ["tr-3", "cu-1"],
         "body": f"{pilot['name']} pays {money(pilot['mrr'])} a month for a {pilot_months}-month pilot: {pct(pilot['mrr'] / model_mrr)} of September revenue. "
                 f"Counted as a customer, it is above the deck's 10%. If it does not convert, that revenue ends."},
        {"lead": "The rest is spread across many accounts.", "refs": ["tr-3"],
         "body": f"{units['Starter plan'] + units['Pro plan']:,} self-serve workspaces bring {money(self_serve)} a month, {pct(self_serve / model_mrr)} of revenue. "
                 f"{n_ent} enterprise contracts bring {money(L['Enterprise contracts'])}."},
        {"lead": "Paying, not just using.", "refs": ["tr-4"],
         "body": f"{credit_ws:,} workspaces use credits and {paying:,} of them pay. Paying accounts are the customers. Free use is interest."},
    ], [
        f"Has {pilot['name']} signed an annual contract? If so, its term, price and notice period.",
        "Term, notice period and renewal date for each enterprise contract.",
        "The top three customers' share of revenue, month by month.",
    ], chart)


def customers_sazabi(R: Room) -> dict:
    L = lines(R)
    rebuilt = R.v("tr-3") / 12
    assert close(sum(L.values()), rebuilt), "plans, the contract and usage add to recurring MRR"
    name, ent = R.quote("cu-1").rsplit(",", 1)
    ent = float(ent)
    assert close(ent, L["Enterprise contract"]) and close(ent / rebuilt, R.v("cu-1")), "the contract's share matches the room's claim"
    paying = int(R.v("cu-2"))
    ws_total = int(re.search(r"out of (\d+) workspaces", R.C["cu-2"]["text"]).group(1))
    dp_paying, dp_total = int(R.v("tr-4")), int(num(R.quote("tr-4", 0).split()[0]))
    plan_names = [n for n in L if n.endswith(" plan") and not n.startswith("Recurring")]
    plans_total = sum(L[n] for n in plan_names)
    n_plans = paying - 1
    units = {l["name"]: l["units"] for l in R.r["whatif"]["lines"]}
    assert sum(units[n] for n in plan_names) == n_plans, "every paying team but the contract is on a plan"
    usage = L["Recurring usage over plan"]
    order = sorted(plan_names, key=lambda n: -L[n])
    names = [f"{name}, the one contract"] + [f"{n}s, {units[n]} teams" for n in order] + ["Recurring usage over plan"]
    vals = [ent] + [L[n] for n in order] + [usage]
    chart = share_chart(names, vals, rebuilt, ["bad"] + ["plan"] * len(order) + ["mixed"], [],
                        f"Share of recurring MRR of {money(rebuilt)}: {name} {pct(ent / rebuilt)}, against a common 20% threshold.")
    return build(R, "customers", [
        {"lead": "One customer is a large share.", "refs": ["cu-1"],
         "body": f"{name} pays {money(ent)} a month: {pct(ent / rebuilt)} of recurring revenue. Its order form agrees with the customer file. "
                 f"That is {'above' if 100 * ent / rebuilt > CONCENTRATION_LINE else 'below'} the {CONCENTRATION_LINE}% many investors use as a threshold."},
        {"lead": "Many small plans behind it.", "refs": ["cu-2"],
         "body": f"{n_plans} teams on plans bring {money(plans_total)} a month together, {money(plans_total / n_plans)} each on average."},
        {"lead": "Paying, not just signed up.", "refs": ["cu-2", "tr-4"],
         "body": f"{paying} teams pay out of {ws_total} workspaces. {dp_paying} of the {dp_total} design partners pay. The deck says all {dp_total} do. "
                 "Design partners show interest. The ones that pay are customers."},
        {"lead": "Usage beyond the plan.", "refs": ["tr-3"],
         "body": f"Recurring usage over plan adds {money(usage)} a month, {pct(usage / rebuilt)} of recurring revenue. It moves with how much teams log, so it can fall as well as rise."},
    ], [
        f"{name}'s signed terms: length, notice period and renewal date.",
        "Which design partners are expected to pay, on which plan, and when.",
        "The top three customers' share of recurring revenue, month by month.",
    ], chart)


PIECES = {
    "retention": {"ploy": retention_ploy, "sazabi": retention_sazabi},
    "customers": {"ploy": customers_ploy, "sazabi": customers_sazabi},
    "unit_economics": {"ploy": unit_economics_ploy, "sazabi": unit_economics_sazabi},
    "team": {"ploy": team_ploy, "sazabi": team_sazabi},
}


def main() -> None:
    data = json.loads((HERE / "data.json").read_text())
    rooms = {"ploy": ploy_room, "sazabi": sazabi_room}
    out = {}
    for slug, make in rooms.items():
        res = data["research"][slug]
        room = make(res["facts"], res["pre"])
        page_room = res["room"]
        R = Room(room, res["facts"], slug)
        reps = []
        for piece in ORDER:
            if piece not in PIECES or not (ROOT / "knowledge" / f"{piece}.md").exists():
                continue
            rep = PIECES[piece][slug](R)
            # The page reads data.js. Every claim an analysis cites must be there with the same value.
            for p in rep["paras"]:
                for cid in p["refs"]:
                    assert cid in page_room["claims"], f"{slug}: claim {cid} is not in data.js; rebuild data.js first"
                    a, b = page_room["claims"][cid]["value"], room["claims"][cid]["value"]
                    assert a == b or (isinstance(a, (int, float)) and close(a, b)), f"{slug}: claim {cid} differs from data.js"
            reps.append(rep)
        out[slug] = reps
    (HERE / "knowledge").mkdir(exist_ok=True)
    for piece in PIECES:
        src = ROOT / "knowledge" / f"{piece}.md"
        if src.exists():
            (HERE / "knowledge" / src.name).write_text(src.read_text())
    text = json.dumps(out, indent=1, ensure_ascii=False)
    (HERE / "piece_reports_data.js").write_text(
        "// Written by piece_reports.py. Do not edit by hand.\nwindow.TC_PIECE_REPORTS_DATA = " + text + ";\n")
    for slug, reps in out.items():
        print(f"{slug}: {', '.join(r['piece'] for r in reps)}")


if __name__ == "__main__":
    main()
