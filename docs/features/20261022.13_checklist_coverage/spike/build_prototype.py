"""Inline the spike's output into the clickable prototype.

Run from the repo root, after coverage_spike.py has written spike/out/:

    python3 docs/features/20261022.13_checklist_coverage/spike/build_prototype.py

Reads spike/prototype_template.html and spike/out/*.json, and writes
02_prototype/prototype.html with the data inlined. The page fetches nothing.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
TEMPLATE = HERE / "prototype_template.html"
TARGET = HERE.parent / "02_prototype" / "prototype.html"

RUNS = {
    "seed_drop:series_a": "seed_drop_series_a.json",
    "seed_drop:seed": "seed_drop_seed.json",
    "seed_drop:pre_seed": "seed_drop_pre_seed.json",
    "full_room:series_a": "full_room_series_a.json",
    "full_room:seed": "full_room_seed.json",
    "full_room:pre_seed": "full_room_pre_seed.json",
    "stage_unknown": "stage_unknown.json",
}
KEEP_COV = ["item_id", "item", "kind", "checklist_piece", "piece", "expected", "status", "projected",
            "found_in", "found_note", "check_entry", "missing_inputs", "ask"]


def slim(d):
    out = {k: d.get(k) for k in ["room", "room_files", "stage", "stage_source", "label", "label_reason",
                                 "counts", "asks", "suppressed_asks", "notes"]}
    out["coverage"] = [{k: r[k] for k in KEEP_COV} for r in d.get("coverage", [])]
    out["gaps"] = [{"what": g["what"], "would_need": g["would_need"]} for g in d.get("gaps", [])]
    return out


def main():
    data = {key: slim(json.loads((OUT / name).read_text())) for key, name in RUNS.items()}
    deck = json.loads((OUT / "seed_drop_auto.json").read_text())["stage_source"]
    data["deck_stage"] = {"stage": json.loads((OUT / "seed_drop_auto.json").read_text())["stage"], "source": deck}
    html = TEMPLATE.read_text().replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(html)
    print(f"wrote {TARGET.relative_to(HERE.parents[3])} ({len(html)} bytes, {len(RUNS)} runs inlined)")


if __name__ == "__main__":
    main()
