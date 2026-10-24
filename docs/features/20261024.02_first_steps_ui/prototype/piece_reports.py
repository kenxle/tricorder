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


# Market --------------------------------------------------------------------------------------------------------


def big(n: float) -> str:
    """$1.44B for a billion or more, else synthetic_rooms.millions."""
    return f"${n / 1e9:.2f}B" if n >= 1e9 else millions(n)


def market_ploy(R: Room) -> dict:
    deck_mkt, model_mkt, annual, deck_count = R.v("ma-1"), R.v("ma-2"), R.v("ma-3"), int(R.v("ma-4"))
    assert close(deck_count * annual, deck_mkt), "the deck's market is its count times the price"
    model_count = round(model_mkt / annual)
    assert close(model_count * annual, model_mkt) and model_count == int(R.quote("ma-2")), "the model's market is its count times the price"
    assert close(annual, 12 * R.f["pro"]), "the price is the Pro plan's, a year"
    arr = R.v("tr-3")
    paying_sub = int(R.v("tr-4")) - 1  # the pilot pays but is not in recurring ARR
    arpa = arr / paying_sub
    share = arr / model_mkt
    chart = {"kind": "bars", "unit": "usd", "barmode": "group",
             "x": [f"Deck: {deck_count:,} companies", f"Model: {model_count:,} companies"],
             "series": [{"name": f"At the Pro list price, {money(annual)} a year", "y": [deck_mkt, model_mkt], "style": "plan",
                         "text": [big(deck_mkt), big(model_mkt)]},
                        {"name": f"At what a paying workspace pays today, {money(arpa)} a year", "y": [deck_count * arpa, model_count * arpa], "style": "mixed",
                         "text": [big(deck_count * arpa), big(model_count * arpa)]}],
             "label": f"Market size, count times price: the deck's {deck_count:,} companies and the model's {model_count:,}, each at the Pro list price "
                      f"of {money(annual)} a year and at today's {money(arpa)} a year per paying workspace."}
    return build(R, "market", [
        {"lead": "Count times price.", "refs": ["ma-4", "ma-1", "ma-2"],
         "body": f"The deck counts {deck_count:,} target companies and the model {model_count:,}. At {money(annual)} a year each, that is "
                 f"{money(deck_mkt)} or {money(model_mkt)}. The company's own files disagree by {deck_count - model_count:,} companies."},
        {"lead": "Which price.", "refs": ["ma-3", "tr-3", "tr-4"],
         "body": f"Both use the Pro plan's list price, which is a ceiling. The {paying_sub:,} workspaces on plans and contracts pay {money(arpa)} a year on average today. "
                 f"At that price the model's count gives {big(model_count * arpa)}."},
        {"lead": "How much is won so far.", "refs": ["tr-3", "ma-2"],
         "body": f"Recurring revenue of {money(arr)} a year is {pct(share)} of the model's market."},
        {"lead": "Both counts are the company's.", "refs": [],
         "body": "The deck and the model come from the founder, so two of them agreeing would still be one estimate. "
                 "The room holds no outside source for how many companies could buy."},
    ], [
        f"What makes up the {deck_count - model_count:,} companies between the deck's count and the model's.",
        "The source behind the count, and what a target company has to look like to be in it.",
        "The market at the price paying workspaces pay today, by plan.",
    ], chart)


def market_sazabi(R: Room) -> dict:
    mkt = R.v("ma-1")
    annual = 12 * R.v("ue-4")
    assert close(annual, 12 * R.f["growth"]), "the price is the Growth plan's, a year"
    count = round(mkt / annual)
    assert close(count * annual, mkt) and f"{count:,}" in R.quote("ma-1"), "the deck's market is its count times the price"
    arr = R.v("tr-3")
    paying = int(R.v("cu-2"))
    arpa = arr / paying
    ratio = mkt / arr
    chart = {"kind": "bars", "unit": "usd", "x": [f"At the Growth list price, {money(annual)} a year", f"At what a paying team pays today, {money(arpa)} a year"],
             "series": [{"name": f"{count:,} engineering teams", "y": [mkt, count * arpa], "styles": ["plan", "mixed"],
                         "text": [big(mkt), big(count * arpa)]}],
             "label": f"Market size for the deck's {count:,} engineering teams: {big(mkt)} at the Growth list price, "
                      f"{big(count * arpa)} at what a paying team pays today."}
    return build(R, "market", [
        {"lead": "Count times price.", "refs": ["ma-1"],
         "body": f"The deck sizes the market at {money(mkt)}: {count:,} engineering teams at the Growth plan's {money(annual)} a year. "
                 "No other file in the room states the count."},
        {"lead": "Which price.", "refs": ["ue-4", "cu-2", "tr-3"],
         "body": f"Growth is the top self-serve plan, so its price is a ceiling. The {paying} paying teams bring {money(arpa)} a year on average today. "
                 f"At that price the same count gives {big(count * arpa)}."},
        {"lead": "How much is won so far.", "refs": ["tr-3"],
         "body": f"The deck's market is {ratio:,.0f} times today's recurring revenue of {money(arr)} a year. "
                 "A market that large rests on the count, so the count needs a source."},
        {"lead": "The count needs a source.", "refs": [],
         "body": "The room does not say where the count comes from, or what makes an engineering team a buyer. "
                 "One company estimate is a starting point, not evidence."},
    ], [
        f"Where the {count:,} engineering teams come from, and what a team has to look like to be in it.",
        "The market at the price paying teams pay today, by plan.",
        "Which segment the company wins first, and how many teams are in it.",
    ], chart)


# The pitch itself ----------------------------------------------------------------------------------------------


def round_terms(R: Room) -> dict:
    rd = R.r["round"]
    raise_, pre, post = num(rd["raise"]), num(rd["pre_money"]), num(rd["post_money"])
    assert close(post, pre + raise_), "post-money is pre-money plus the raise"
    own = raise_ / post
    assert pct(own, 2) == rd["ownership"], "ownership matches the room's round"
    return {"name": rd["name"], "raise": raise_, "pre": pre, "post": post, "own": own}


def runway_end(R: Room, style: str) -> float:
    """Months until the cash runs out on one line of Kimmy's cash chart (burn and runway report)."""
    s = next(x for x in R.report("burn_and_runway")["chart"]["series"] if x["style"] == style)
    end, label = s["points"][-1][0], float(s["end"].split()[0])
    assert abs(end - label) <= 0.06, "the line's end matches its label"
    return label


def yc_fit(months: float) -> str:
    """Where a runway sits against YC's 12 to 18 months (knowledge/the_pitch_itself.md)."""
    return "past that" if months > 18 else "inside that" if months >= 12 else "short of that"


def multiple_chart(post: float, arrs: list[tuple[str, float, str]], what: str) -> dict:
    return {"kind": "bars", "unit": "multiple", "x": [a[0] for a in arrs],
            "series": [{"name": "Post-money as a multiple of ARR", "y": [round(post / a[1], 2) for a in arrs], "styles": [a[2] for a in arrs],
                        "text": [f"{post / a[1]:,.1f}x" for a in arrs]}],
            "label": f"{what} of {big(post)} as a multiple of ARR: " + ", ".join(f"{a[0]} {post / a[1]:,.1f}x" for a in arrs) + "."}


def pitch_ploy(R: Room) -> dict:
    t = round_terms(R)
    assert close(t["raise"], R.v("pi-1"))
    deck_arr, model_arr, arr = R.v("tr-1"), R.v("tr-2"), R.v("tr-3")
    rw_round, rw_hires = runway_end(R, "round"), runway_end(R, "hires")
    share = R.v("pi-2")
    chart = multiple_chart(t["post"], [(f"Deck ARR, {big(deck_arr)}", deck_arr, "plan"), (f"Model ARR, {money(model_arr)}", model_arr, "plan"),
                                       (f"Rebuilt ARR, {money(arr)}", arr, "mixed")], "Post-money")
    return build(R, "the_pitch_itself", [
        {"lead": "The ask.", "refs": ["pi-1"],
         "body": f"A {big(t['raise'])} {t['name']} at {big(t['pre'])} pre-money, so {big(t['post'])} post. The new money buys {pct(t['own'], 2)} of the company."},
        {"lead": "The price against revenue.", "refs": ["tr-1", "tr-3"],
         "body": f"The post-money is {t['post'] / deck_arr:.1f} times the deck's ARR and {t['post'] / arr:.1f} times ARR rebuilt from the customer file. "
                 "The pilot is the difference. Tricorder sets no line for the multiple. The partner weighs it against comparable rounds."},
        {"lead": "What the round buys.", "refs": ["pi-1", "bu-2"],
         "body": f"With the round in the bank and every planned hire paid, the cash lasts {rw_round:.1f} months. Without the round, {rw_hires:.1f}. "
                 f"YC advises raising enough to reach the next fundable milestone, usually 12 to 18 months out. {rw_round:.1f} months is {yc_fit(rw_round)}."},
        {"lead": "A pitch claim that holds.", "refs": ["pi-2"],
         "body": f"The deck says {R.f['batch_share_pct']}% of the YC batch use Ploy. The workspace file tags {pct(share)}, and the launch post agrees."},
    ], [
        "The use of funds by line, each tied to a dated milestone and to the hiring plan.",
        "The pro forma cap table after the round, with the option pool.",
        f"Which ARR the {big(t['pre'])} pre-money was set on: the deck's, or the one without the pilot.",
    ], chart)


def pitch_sazabi(R: Room) -> dict:
    t = round_terms(R)
    cap_total, unsigned, signed = R.v("pi-1"), R.v("pi-2"), R.v("lc-2")
    assert close(cap_total, t["raise"]) and close(signed + unsigned, cap_total), "signed plus unsigned is the round"
    arr = R.v("tr-3")
    rw_round, rw_hires = runway_end(R, "round"), runway_end(R, "hires")
    chart = {"kind": "bars", "unit": "usd", "barmode": "stack", "x": ["What the deck says", "What the SAFE schedule shows"],
             "series": [{"name": "Called closed", "y": [cap_total, 0], "style": "plan", "text": [big(cap_total), ""]},
                        {"name": "Signed SAFEs", "y": [0, signed], "style": "good", "text": ["", big(signed)], "textposition": "inside"},
                        {"name": "Commitments with no signed SAFE", "y": [0, unsigned], "style": "thin", "text": ["", f"{big(unsigned)} unsigned"]}],
             "label": f"The {t['name'].lower()} as the deck states it, {big(cap_total)} closed, and as the SAFE schedule shows it: "
                      f"{big(signed)} signed and {big(unsigned)} with no signed SAFE."}
    return build(R, "the_pitch_itself", [
        {"lead": "The ask.", "refs": ["pi-1"],
         "body": f"An {big(cap_total)} {t['name'].lower()} on SAFEs at a {big(t['post'])} post-money cap. If it all converts at the cap, the seed owns {pct(t['own'], 2)}."},
        {"lead": "Called closed, partly unsigned.", "refs": ["pi-2", "lc-2"],
         "body": f"The deck calls the round closed. The SAFE schedule shows {money(signed)} signed and {money(unsigned)} of commitments with no signed SAFE: "
                 f"{pct(unsigned / cap_total)} of the round. A commitment is a promise until the paper is signed."},
        {"lead": "The price against revenue.", "refs": ["tr-3"],
         "body": f"The {big(t['post'])} cap is {t['post'] / arr:,.0f} times recurring ARR of {money(arr)}. "
                 "Tricorder sets no line for the multiple. At seed the price rests on more than revenue, and the partner weighs it against comparable rounds."},
        {"lead": "What the unsigned money changes.", "refs": ["bu-2", "pi-2"],
         "body": f"With every planned hire, the cash in the bank lasts {rw_hires:.1f} months. If the unsigned {big(unsigned)} comes in, {rw_round:.1f}. "
                 f"YC advises raising enough for the next fundable milestone, usually 12 to 18 months out. The signed money alone gives {rw_hires:.1f} months, {yc_fit(rw_hires)}."},
    ], [
        f"Who the unsigned commitments are, and when they sign.",
        "Signed copies of every SAFE, so the schedule ties to the papers.",
        "The use of funds by line, each tied to a dated milestone.",
    ], chart)


# Legal and cap table -------------------------------------------------------------------------------------------

FORM_D_DAYS = 15  # knowledge/legal_and_cap_table.md: the SEC's Form D page, due within 15 calendar days after the first sale


def legal_ploy(R: Room) -> dict:
    rows = {r[0]: r for r in R.panel("legal_and_cap_table")["rows"]}
    sold, safe, inv = (num(rows["Seed total sold"][1]), num(rows["From SAFEs that converted"][1]), int(num(rows["Seed investors"][1])))
    for k in ("Seed total sold", "From SAFEs that converted", "Seed investors"):
        assert rows[k][1] == rows[k][2], f"cap table and Form D agree on {k}"
    assert close(sold, R.v("lc-1")) and close(safe, R.v("lc-2")) and inv == R.v("lc-3") and sold == R.f["sold"] and safe == R.f["safe"] and inv == R.f["investors"]
    assert any("pro forma" in g for g in R.drill_gaps("legal_and_cap_table")), "the room says the pro forma is not in it"
    chart = {"kind": "bars", "unit": "usd", "barmode": "group", "x": ["Seed total sold", "From SAFEs that converted"],
             "series": [{"name": "Cap table", "y": [sold, safe], "style": "good", "text": [big(sold), big(safe)]},
                        {"name": "SEC Form D", "y": [sold, safe], "style": "plan", "text": [big(sold), big(safe)]}],
             "label": f"The cap table against the SEC Form D: {money(sold)} sold and {money(safe)} from SAFEs in both."}
    return build(R, "legal_and_cap_table", [
        {"lead": "The cap table matches the public record.", "refs": ["lc-1"],
         "body": f"The seed total on the cap table, {money(sold)}, is the amount sold on the SEC Form D, to the dollar. "
                 "A filing the company does not control agreeing with its own file is a small green flag."},
        {"lead": "The SAFEs and the holders agree too.", "refs": ["lc-2", "lc-3"],
         "body": f"{money(safe)} of SAFEs converted into the seed, the figure the Form D gives. The cap table lists {inv} seed holders, the Form D's count."},
        {"lead": "No claims stated.", "refs": ["lc-4"],
         "body": "The claims statement says there are no lawsuits, threatened claims or regulator contact. It is the company's own statement. "
                 "A litigation and lien search would test it."},
        {"lead": "The pro forma is missing.", "refs": [],
         "body": "The room holds no pro forma cap table after the Series A. Without it, the ownership after the round cannot be rebuilt from its terms."},
    ], [
        "The pro forma cap table after the Series A, with SAFE conversions and the option pool.",
        "Signed copies of the seed stock purchase agreements, so each row ties to a paper.",
        "Founder vesting schedules and any side letters.",
    ], chart)


def legal_sazabi(R: Room) -> dict:
    rows = {r[0]: r for r in R.panel("legal_and_cap_table")["rows"]}
    cap, signed = num(rows["Seed total"][1]), num(rows["Seed total"][2])
    holders_cap, holders_signed = int(num(rows["Holders"][1])), int(num(rows["Holders"][2]))
    unsigned = num(rows["Without a signed SAFE"][1])
    assert close(cap, R.v("lc-1")) and close(signed, R.v("lc-2")) and close(cap - signed, unsigned) and close(unsigned, R.v("pi-2"))
    first_sale, last_signed = rows["First sale"][2], rows["Last SAFE signed"][2]
    due = (dt.date.fromisoformat(first_sale) + dt.timedelta(days=FORM_D_DAYS)).isoformat()
    assert rows["First sale"][3] == f"Form D due by {due}", "the Form D due date matches the room's"
    as_of = R.r["as_of"]
    late = (dt.date.fromisoformat(as_of) - dt.date.fromisoformat(due)).days
    edgar = int(R.f["edgar_formd"])
    assert edgar == R.v("lc-3")
    still, post_date = R.f["still_raising_date"], R.f["seed_post_date"]
    pad = dt.timedelta(days=28)
    chart = {"kind": "timeline", "height": 340,
             "range": [(dt.date.fromisoformat(first_sale) - pad).isoformat(), (dt.date.fromisoformat(as_of) + pad).isoformat()],
             "gap": {"from": due, "to": as_of, "label": f"No Form D on EDGAR: {late} days past due",
                     "mid": (dt.date.fromisoformat(due) + (dt.date.fromisoformat(as_of) - dt.date.fromisoformat(due)) / 2).isoformat()},
             "events": [{"date": first_sale, "short": "First SAFE funded", "label": f"First SAFE funded, {first_sale}", "style": "accent"},
                        {"date": due, "short": "Form D due", "label": f"Form D due, {FORM_D_DAYS} days after the first sale", "style": "bad"},
                        {"date": still, "short": "Press: still raising", "label": f"The press reports the company still raising, {still}", "style": "bad"},
                        {"date": post_date, "short": "Company post: seed raised", "label": f"The company's post announces the seed, {post_date}", "style": "plan"},
                        {"date": last_signed, "short": "Last SAFE signed", "label": f"Last SAFE signed, {last_signed}", "style": "plan"},
                        {"date": as_of, "short": "Room as of", "label": f"The room's as-of date. EDGAR has {edgar} Form D filings", "style": "bad"}],
             "label": f"The seed's dates: first SAFE funded {first_sale}, Form D due {due}, press says still raising {still}, company post {post_date}, "
                      f"last SAFE signed {last_signed}. EDGAR has {edgar} Form D filings as of {as_of}."}
    return build(R, "legal_and_cap_table", [
        {"lead": "The cap table counts more than is signed.", "refs": ["lc-1", "lc-2"],
         "body": f"The cap table's seed total is {money(cap)}, the amount in the company's post. The signed SAFEs add to {money(signed)} from {holders_signed} holders. "
                 f"The other {money(unsigned)} comes from {holders_cap - holders_signed} commitments with no signed SAFE. A row with no paper is a promise."},
        {"lead": "No Form D on file.", "refs": ["lc-3"],
         "body": f"The first SAFE was funded on {first_sale}. A Form D is due {FORM_D_DAYS} days after the first sale, so by {due}. "
                 f"EDGAR has {edgar} Form D filings for the company, and the room's as-of date is {late} days past the due date. "
                 "A filing may sit under another legal name, so this is a question for the founder before it is a flag."},
        {"lead": "The round kept raising after it was announced.", "refs": ["lc-2", "pi-2"],
         "body": f"The press reported the company still raising on {still}. The company announced the seed on {post_date}, and SAFEs were still being signed until {last_signed}. "
                 "The deck calls the round closed."},
        {"lead": "No claims stated.", "refs": ["lc-4"],
         "body": "The claims statement says there are no lawsuits, threatened claims or regulator contact. It is the company's own statement."},
    ], [
        "Was a Form D filed, and under what legal name? If not, why not?",
        f"Who the {holders_cap - holders_signed} unsigned commitments are, and when they sign.",
        "Signed copies of every SAFE, and the pro forma cap table after the seed converts.",
    ], chart)


# The outside world ---------------------------------------------------------------------------------------------

# The four answers the room gives a public fact, in the room view's words (room_view.js, PRE), and how each reads.
STATUS = [("confirms", "Confirmed by the room", "good"), ("answers", "Answered by the room", "mixed"),
          ("differs", "The room differs", "bad"), ("not settled", "Not settled by the room", "plan")]
FACT = {"prices": "the prices", "team": "the team size", "formd_sold": "the Form D amount", "formd_safe": "the SAFEs on the Form D",
        "formd_investors": "the Form D's investor count", "batch_share": "the share of the YC batch", "usage": "the launch post's usage",
        "engineers": "the engineer count", "still_raising": "the press report that it was still raising", "design_partners": "the design partner count",
        "seed": "the seed total", "formd_none": "the missing Form D", "hiring": "the job posts against the hiring plan",
        "named_customers": "the customers named in public", "revenue_range": "the Form D's revenue range"}


ASK = {"seed": "Signed copies of every SAFE behind the seed total, and who the unsigned commitments are.",
       "formd_none": "Was a Form D filed, and under what legal name?",
       "named_customers": "Contracts or invoices for the customers named in public, or why they are not in the room.",
       "hiring": "Which roles in the hiring plan are open now, and where they are posted."}


def listing(xs: list[str]) -> str:
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def outside_world(R: Room) -> dict:
    pcs = R.r["prechecks"]
    assert all(pc["pre"] in FACT for pc in pcs), "every public fact has a name"

    def claim_of(pc):
        s = pc["source"]
        return next((cid for cid, c in R.C.items() if any(x.get("uri") == s["uri"] and x.get("locator") == s["locator"] for x in c["sources"])), None)

    by = {k: [pc for pc in pcs if pc["status"] == k] for k, _, _ in STATUS}
    assert sum(len(v) for v in by.values()) == len(pcs), "every public fact has one of the four answers"
    refs = lambda k: sorted({c for c in (claim_of(pc) for pc in by[k]) if c})
    names = lambda k: [FACT[pc["pre"]] for pc in by[k]]
    paras = [{"lead": "What the public record confirms.", "refs": refs("confirms"),
              "body": f"{len(by['confirms'])} of {len(pcs)} checks against the public record come back confirmed: {listing(names('confirms'))}. "
                      "Each pairs a public source with a room file, a small green flag."}]
    if by["answers"]:
        paras.append({"lead": "Where the public record is silent.", "refs": refs("answers"),
                      "body": f"The public record left {listing(names('answers'))} open, and the room answers it. " + " ".join(pc["room"] for pc in by["answers"])})
    if by["differs"]:
        paras.append({"lead": "Where the room differs.", "refs": refs("differs"),
                      "body": f"The room differs on {listing(names('differs'))}. " + " ".join(pc["room"] for pc in by["differs"])
                              + " Each difference is a question for the founder, with both dates named."})
    if by["not settled"]:
        paras.append({"lead": "What the room cannot settle.", "refs": refs("not settled"),
                      "body": f"The room cannot settle {listing(names('not settled'))}. " + " ".join(pc["room"] for pc in by["not settled"])
                              + " A missing record is a gap and a question, not a flag on its own."})
    chart = {"kind": "bars", "unit": "count", "orientation": "h", "x": [label for _, label, _ in STATUS],
             "series": [{"name": "Public facts", "y": [len(by[k]) for k, _, _ in STATUS], "styles": [st for _, _, st in STATUS],
                         "text": [str(len(by[k])) for k, _, _ in STATUS],
                         "hover": [listing([FACT[pc["pre"]] for pc in by[k]]) if by[k] else "none" for k, _, _ in STATUS]}],
             "range": [0, len(pcs) + 1],
             "label": f"{len(pcs)} public facts checked against the room: " + ", ".join(f"{len(by[k])} {label.lower()}" for k, label, _ in STATUS) + "."}
    asks = [ASK.get(pc["pre"], f"A dated document that explains {FACT[pc['pre']]}.") for pc in (by["differs"] + by["not settled"])][:3]
    asks.append("Any public figure the founder expects to have changed since it was published, with the date it changed.")
    assert int(R.v("ow-1")) <= len(by["confirms"]), "the room's count of agreeing facts fits the checks"
    return build(R, "outside_world", paras, asks, chart)


PIECES = {
    "retention": {"ploy": retention_ploy, "sazabi": retention_sazabi},
    "outside_world": {"ploy": outside_world, "sazabi": outside_world},
    "legal_and_cap_table": {"ploy": legal_ploy, "sazabi": legal_sazabi},
    "the_pitch_itself": {"ploy": pitch_ploy, "sazabi": pitch_sazabi},
    "market": {"ploy": market_ploy, "sazabi": market_sazabi},
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
