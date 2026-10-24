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


PIECES = {
    "retention": {"ploy": retention_ploy, "sazabi": retention_sazabi},
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
