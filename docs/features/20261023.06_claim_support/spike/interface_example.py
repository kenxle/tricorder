"""Print the claim-support interface example from the real rooms.

    python3 docs/features/20261023.06_claim_support/spike/interface_example.py <scratch_out_dir>

Runs the commands a user runs (redflags, claims, memo, then the claim_support
step) on hollis_voice and brasswick with TRICORDER_OUT_DIR set to the scratch
folder, then prints, as JSON: the claims table's columns, one claim and its
table row for each label, the counts panel, one gap, and one claim the memo
step relabelled. Nothing here is typed by hand; 02_interface_example.md pastes
this output.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def build(room: str, out: Path) -> dict:
    env = dict(os.environ, TRICORDER_OUT_DIR=str(out))
    env.pop("ANTHROPIC_API_KEY", None)
    for mod in ("scans.redflags", "scans.claims", "scans.memo", "scans.memo.claim_support"):
        subprocess.run([sys.executable, "-m", mod, str(ROOT / "data_room" / room)], cwd=ROOT, env=env,
                       check=True, capture_output=True)
    return json.loads((out / room / "readout.json").read_text(encoding="utf-8"))


def panel(readout: dict, name: str) -> dict:
    return next(p for p in readout["panels"] if p["name"] == name)


def row_for(readout: dict, cid: str) -> dict:
    p = panel(readout, "claims table")
    return next(dict(zip(p["columns"], r)) for r in p["rows"] if r[0] == cid)


def trim(claim: dict) -> dict:
    keep = ("id", "scan", "text", "severity", "confidence", "check", "value", "sources", "conflicts_with", "corroborated_by")
    return {k: claim[k] for k in keep}


def main(out_dir: str) -> int:
    out = Path(out_dir)
    hv, bw = build("hollis_voice", out), build("brasswick", out)
    claims = {c["id"]: c for c in hv["claims"] if c["scan"] == "claims"}
    rows = [row_for(hv, cid) for cid in claims]
    pick = {}
    for label, where, stated in (("supported", "slide 8", "near $252,000,000"),
                                 ("contradicted", "script line 15", "about three million dollars"),
                                 ("unsupported", "slide 7", "$349")):
        pick[label] = next(r for r in rows if r["label"] == label and r["where"].startswith(where) and r["stated"] == stated)
    relabelled = next(c for c in bw["claims"] if c["scan"] == "claims" and c["conflicts_with"])
    example = {
        "claims_table_columns": panel(hv, "claims table")["columns"],
        "hollis_voice": {label: {"row": r, "claim": trim(claims[r["claim id"]])} for label, r in pick.items()},
        "hollis_voice_counts": panel(hv, "claims table counts")["rows"],
        "hollis_voice_gap": next(g for g in hv["gaps"] if "pitch claims on list price" in g["what"]),
        "brasswick_relabelled_by_memo_step": {"row": row_for(bw, relabelled["id"]), "claim": trim(relabelled)},
    }
    print(json.dumps(example, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
