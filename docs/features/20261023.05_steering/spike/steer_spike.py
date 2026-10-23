"""Spike: the real figures the steering prototype shows, printed from the rooms.

    TRICORDER_OUT_DIR=<scratch> python3 docs/features/20261023.05_steering/spike/steer_spike.py

Runs the redflags scan on the full room and the seed drop, then computes, by
script, the two figures the demo steers need:

- "treat the pilot as non-recurring": 12 x ('Recurring revenue (subscription
  plus pilot)' less 'Pilot revenue') for the as-of month, from the P&L cells.
- "read the full room" on retention: the Cohorts tab's stated NRR (seed drop
  and full room), and the 12-month NRR and GRR rebuilt from
  customer_mrr_by_month.csv (full room only).

Writes spike/out/spike.json. Nothing here is product code.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from schema.readers import xlsx_sheet  # noqa: E402
from scans.base import write_result  # noqa: E402
from scans.redflags import scan as redflags  # noqa: E402

HERE = Path(__file__).parent


def pnl_line(room: Path, name: str, month: str) -> float:
    rows = xlsx_sheet(room / "02_financials/financial_model.xlsx", "P&L")
    hdr = next(r for r in rows if r and r[0] == "Line")
    j = hdr.index(month)
    return next(r[j] for r in rows if r and r[0] == name)


def add_months(m: str, k: int) -> str:
    y, mm = map(int, m.split("-"))
    t = y * 12 + mm - 1 + k
    return f"{t // 12}-{t % 12 + 1:02d}"


def cohorts(room: Path) -> dict | None:
    path = room / "03_metrics/customer_mrr_by_month.csv"
    if not path.exists():
        return None
    mrr: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for r in csv.DictReader(path.open(encoding="utf-8")):
        mrr[r["customer_id"]][r["month"]] += float(r["mrr"] or 0)
    last = max(m for d in mrr.values() for m in d)
    start = end = capped = 0.0
    n = 0
    for d in mrr.values():
        first = min((m for m, v in d.items() if v > 0), default=None)
        if first is None or add_months(first, 12) > last:
            continue
        n += 1
        s, e = d[first], d.get(add_months(first, 12), 0.0)
        start, end, capped = start + s, end + e, capped + min(s, e)
    return {"customers": n, "nrr": round(100 * end / start, 1), "grr": round(100 * capped / start, 1)}


def tab_nrr(room: Path) -> dict:
    rows = xlsx_sheet(room / "02_financials/financial_model.xlsx", "Cohorts")
    total = next(r for r in rows if r and r[0] == "All cohorts")
    return {"customers": total[1], "nrr": round(100 * total[4], 1), "note": rows[1][0]}


def main() -> None:
    out = {}
    for name in ("hollis_voice", "hollis_voice_seed_drop"):
        room = ROOT / "data_room" / name
        result = redflags.run(room)
        write_result(result, room)
        rec = pnl_line(room, "Recurring revenue (subscription plus pilot)", "2026-09")
        pilot = pnl_line(room, "Pilot revenue", "2026-09")
        out[name] = {
            "claims": [{"id": c.id, "check": c.check.name, "severity": c.severity, "text": c.text} for c in result.claims],
            "gaps": [{"piece": g.piece, "what": g.what} for g in result.gaps],
            "pilot_steer": {"recurring_2026_09": rec, "pilot_2026_09": pilot, "arr_without_pilot": 12 * (rec - pilot),
                            "deck_arr": 2_500_000, "gap_pct": round(100 * abs(2_500_000 - 12 * (rec - pilot)) / (12 * (rec - pilot)), 1)},
            "cohorts_tab": tab_nrr(room),
            "cohorts_rebuilt": cohorts(room),
        }
    (HERE / "out").mkdir(exist_ok=True)
    (HERE / "out" / "spike.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    for name, d in out.items():
        print(name, json.dumps({k: d[k] for k in ("pilot_steer", "cohorts_tab", "cohorts_rebuilt")}))


if __name__ == "__main__":
    main()
