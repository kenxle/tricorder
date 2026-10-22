"""Build the clickable prototype from the product coverage step.

Run from the repo root:

    python3 docs/features/20261022.13_checklist_coverage/spike/build_prototype.py [--scan-out DIR]

For each room (seed drop, full room) and stage (pre-seed, seed, Series A), it runs
scans.memo.coverage.apply on a readout holding the redflags scan's real claims and gaps
for that room, when DIR/<room>/redflags.json exists (run `python -m scans.redflags <room>`
with TRICORDER_OUT_DIR=DIR first). It also runs one "stage unknown" case. The output is
inlined into 02_prototype/prototype.html; the page fetches nothing. Every room is synthetic.
"""
import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO))

from schema.claim import Readout, ScanResult  # noqa: E402
from scans.memo import checklist, coverage  # noqa: E402

TEMPLATE = HERE / "prototype_template.html"
TARGET = HERE.parent / "02_prototype" / "prototype.html"
ROOMS = {"seed_drop": REPO / "data_room/hollis_voice_seed_drop", "full_room": REPO / "data_room/hollis_voice"}


def panel(readout, name):
    return next((p for p in readout.panels if p.name == name), None)


def run(room, stage, scan_out):
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["TRICORDER_OUT_DIR"] = tmp
        (Path(tmp) / room.name).mkdir()
        (Path(tmp) / room.name / "operator.json").write_text(json.dumps({"stage": stage}))
        readout = Readout(room=room.name, built_at="prototype")
        src = Path(scan_out) / room.name / "redflags.json" if scan_out else None
        if src and src.exists():
            result = ScanResult.model_validate_json(src.read_text())
            readout.claims, readout.gaps = list(result.claims), list(result.gaps)
        readout = coverage.apply(readout, room)
    counts = dict(panel(readout, coverage.COUNTS_PANEL).rows)
    out = {"counts": counts, "coverage": [], "asks": [], "claims_from_scan": len(readout.claims)}
    if counts.get("label") != "built":
        return out
    rows = {r.id: r for r in checklist.load()}
    cov = panel(readout, coverage.COVERAGE_PANEL)
    for r in cov.rows:
        d = dict(zip(cov.columns, r))
        d["checklist_piece"] = rows[d["id"]].piece
        out["coverage"].append(d)
    asks = panel(readout, coverage.ASKS_PANEL)
    lines = [a for a in readout.asks if a.checklist_id]
    for n, (a, meta) in enumerate(zip(lines, asks.rows), start=1):
        m = dict(zip(asks.columns, meta))
        out["asks"].append({"n": n, "what": a.what, "why": a.why, "piece": a.piece, "from_kind": a.from_kind,
                            "checklist_id": a.checklist_id, "if_you_have_it": a.if_you_have_it,
                            "covers": m["checklist_ids"].split(", "), "ask_stage": m["ask_stage"],
                            "top": int(m["top_five"]) if m["top_five"] else None})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan-out", default=os.environ.get("TRICORDER_OUT_DIR"))
    args = ap.parse_args()
    data = {}
    for key, room in ROOMS.items():
        for stage in checklist.STAGES:
            data[f"{key}:{stage}"] = run(room, stage, args.scan_out)
    data["stage_unknown"] = run(ROOMS["seed_drop"], "series_b", None)
    deck = coverage.read_deck_stage(ROOMS["seed_drop"])
    data["deck_stage"] = {"stage": deck[0], "source": deck[2]}
    html = TEMPLATE.read_text().replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
    TARGET.write_text(html)
    print(f"wrote {TARGET.relative_to(REPO)} ({len(html)} bytes)")
    for k, v in data.items():
        if k != "deck_stage":
            c = v["counts"]
            print(k, {s: c.get(s) for s in ("label", "checked", "found", "missing", "not_checked", "not_expected",
                                             "ask_lines", "ask_lines_if_you_have_it", "ask_lines_after_term_sheet",
                                             "gap_asks_held_back")}, "scan claims:", v["claims_from_scan"])


if __name__ == "__main__":
    main()
