"""Count the claim-support "Done when" lines on each demo room, by script.

    python3 docs/features/20261023.06_claim_support/spike/count_done_when.py <scratch_out_dir>

For each room it runs the commands a user runs (redflags, claims, memo, then the
claim_support step's own command), with TRICORDER_OUT_DIR set to the scratch
folder, and reads the readout back. Like eval/score.py, this script reads the
answer keys; no scan does. Prints one Markdown table per question and a JSON
summary on the last line.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from schema.check_quotes import check_claim  # noqa: E402
from schema.claim import Readout  # noqa: E402

ROOMS = {
    "hollis_voice": "answer_key.json",
    "brasswick": "answer_key_brasswick.json",
    "hollis_voice_seed_drop": "answer_key.json",
    "hollis_voice_clean": "answer_key_clean.json",
}
PITCH = ("01_overview/pitch_deck.pdf", "01_overview/pitch_video_script.md")


def build(room: str, out: Path) -> Readout:
    env = dict(os.environ, TRICORDER_OUT_DIR=str(out))
    env.pop("ANTHROPIC_API_KEY", None)
    for args in (["scans.redflags"], ["scans.claims"], ["scans.memo"], ["scans.memo.claim_support"]):
        subprocess.run([sys.executable, "-m", *args, str(ROOT / "data_room" / room)], cwd=ROOT, env=env,
                       check=True, capture_output=True)
    return Readout.model_validate_json((out / room / "readout.json").read_text(encoding="utf-8"))


def table(r: Readout) -> list[dict]:
    p = next(p for p in r.panels if p.name == "claims table")
    return [dict(zip(p.columns, row)) for row in p.rows]


def _flat(s: str) -> str:
    return " ".join(s.split()).lower()


def rows_for(location: dict, rows: list[dict], claims: dict) -> list[dict]:
    """Claims-table rows whose pitch quote (or a claims-page repeat) holds the key location's text."""
    text = _flat(location.get("text", ""))
    if not text or location["file"] not in PITCH:
        return []
    page = location.get("page")
    out = []
    for row in rows:
        c = claims.get(row["claim id"])
        if c is None:
            continue
        first = c.sources[0]
        here = first.uri == location["file"] and (page is None or re.search(rf"\b{page}\b", first.locator))
        repeat = page is not None and f"slide {page}, claims page row" in row["where"] and text in _flat(row["where"])
        if (here and (text in _flat(first.quote) or _flat(first.quote) in text)) or repeat:
            out.append(row)
    return out


def main(out_dir: str) -> int:
    out = Path(out_dir)
    summary = {}
    for room, key_name in ROOMS.items():
        key = json.loads((ROOT / "data_room" / key_name).read_text(encoding="utf-8"))
        r = build(room, out)
        rows = table(r)
        claims = {c.id: c for c in r.claims + r.unverified if c.scan == "claims"}
        labels = {k: sum(1 for x in rows if x["label"] == k) for k in ("supported", "contradicted", "unsupported", "could not verify")}
        numeric = [x for x in rows if claims[x["claim id"]].value is not None or re.search(r"\d", x["stated"])]
        failures = sum(1 for c in claims.values() if check_claim(c, ROOT / "data_room" / room)[1])
        from_script = sum(1 for x in rows if x["where"].startswith("script"))
        planted = []
        if room != "hollis_voice_clean":
            seed = room.endswith("seed_drop")
            for flag in key.get("flags", []):
                if seed and not flag.get("catchable_from_seed_drop"):
                    continue
                hits = {x["claim id"]: x for loc in flag["locations"] for x in rows_for(loc, rows, claims)}
                if not hits:
                    continue
                contra = [x for x in hits.values() if x["label"] == "contradicted"]
                both = [x for x in contra if len({s.uri for s in claims[x["claim id"]].sources}) >= 2]
                planted.append({"id": flag["id"], "pitch_figures": len(hits), "contradicted": len(contra),
                                "with_both_sources": len(both),
                                "others": [f"{x['stated']} ({x['where'].split(';')[0]}): {x['label']}" for x in hits.values()
                                           if x["label"] != "contradicted"]})
        greens = []
        for g in key.get("green_flags", []) if not room.endswith("seed_drop") else []:
            locs = list(g["locations"]) + [l for extra in g.get("also_agree", []) for l in extra["locations"]]
            hits = {x["claim id"]: x for loc in locs for x in rows_for(loc, rows, claims)}
            for x in hits.values():
                c = claims[x["claim id"]]
                outside = sorted({s.uri for s in c.sources if s.uri not in PITCH and "claims.json" not in s.uri})
                greens.append({"id": g["id"], "stated": x["stated"], "where": x["where"].split(";")[0], "label": x["label"],
                               "sources": [c.sources[0].uri] + outside})
        summary[room] = {"claims": len(rows), "numeric": len(numeric), "from_script": from_script, "labels": labels,
                         "quote_failures": failures, "planted": planted, "greens": greens,
                         "not_counted": len(next(p for p in r.panels if p.name == "claims not counted").rows)}

    print("| Room | Claims | Numeric | From the script | Supported | Contradicted | Unsupported | Could not verify | Quote checker failures | Examples not counted |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for room, s in summary.items():
        l = s["labels"]
        print(f"| {room} | {s['claims']} | {s['numeric']} | {s['from_script']} | {l['supported']} | {l['contradicted']} | "
              f"{l['unsupported']} | {l['could not verify']} | {s['quote_failures']} | {s['not_counted']} |")
    print()
    print("| Room | Planted entry | Pitch figures it touches | Contradicted | With both sources | The rest |")
    print("|---|---|---|---|---|---|")
    for room, s in summary.items():
        for p in s["planted"]:
            print(f"| {room} | {p['id']} | {p['pitch_figures']} | {p['contradicted']} | {p['with_both_sources']} | {'; '.join(p['others']) or 'none'} |")
    print()
    print("| Room | Green flag | Figure | Where | Label | Sources |")
    print("|---|---|---|---|---|---|")
    for room, s in summary.items():
        for g in s["greens"]:
            print(f"| {room} | {g['id']} | {g['stated']} | {g['where']} | {g['label']} | {', '.join(g['sources'])} |")
    print()
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
