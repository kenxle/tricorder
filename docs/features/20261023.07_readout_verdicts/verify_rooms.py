"""Rebuild the synthetic rooms and write one evidence row per claim and piece.

Run from the repository root with its Python environment:
    python docs/features/20261023.07_readout_verdicts/verify_rooms.py

Scan outputs and memo exports stay under /tmp/tricorder-readout-proof.
Only the evidence summaries beside this script are versioned.
"""

import csv
import importlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
os.environ["TRICORDER_OUT_DIR"] = "/tmp/tricorder-readout-proof"
os.environ["TRICORDER_OFFLINE"] = "1"
os.environ.pop("ANTHROPIC_API_KEY", None)

from memo.export import export
from scans.base import available, out_dir, write_result
from scans.memo import pieces, top_flags
from scans.memo.merge import build_readout, write_readout
from schema.claim import PIECE_ORDER

EVIDENCE = Path(__file__).parent / "evidence"


def main():
    EVIDENCE.mkdir(exist_ok=True)
    summaries, claim_rows = [], []
    for name in ("hollis_voice", "hollis_voice_seed_drop", "brasswick", "hollis_voice_clean"):
        room = ROOT / "data_room" / name
        for scan in available():
            module = importlib.import_module(f"scans.{scan}.scan")
            write_result(module.run(room), room)
        readout = build_readout(room)
        assert [p.name for p in readout.pieces] == list(PIECE_ORDER)
        assert readout == top_flags.apply(pieces.apply(readout, room), room)
        repeat = build_readout(room)
        assert readout.model_dump(exclude={"built_at"}) == repeat.model_dump(exclude={"built_at"})
        ids = {c.id for c in readout.claims}
        for p in readout.pieces:
            assert set(p.reason_claim_ids) <= set(p.claim_ids) <= ids
        for f in readout.top_flags:
            assert set(f.claim_ids) <= ids
            assert f.text == next(c.text for c in readout.claims if c.id == f.claim_ids[0])
        write_readout(readout, room)
        memo = export(room)
        assert memo.html.is_file() and memo.pdf.is_file()
        for c in readout.claims:
            claim_rows.append({"room": name, "id": c.id, "piece": pieces.piece_of(c),
                               "severity": c.severity, "confidence": c.confidence,
                               "conflicts": ";".join(c.conflicts_with), "corroborates": ";".join(c.corroborated_by),
                               "red_gap": pieces.red_gap(c, {c.id: c for c in readout.claims}), "text": c.text})
        summary = {"room": name, "claims": len(readout.claims), "unverified": len(readout.unverified),
                   "pieces": [p.model_dump() for p in readout.pieces],
                   "top_flags": [f.model_dump() for f in readout.top_flags],
                   "memo_html": str(memo.html), "memo_pdf": str(memo.pdf),
                   "scans_missing": readout.scans_missing}
        (EVIDENCE / f"{name}.json").write_text(json.dumps(summary, indent=2) + "\n")
        summaries.append({"room": name, "claims": len(readout.claims), "pieces": len(readout.pieces),
                          "greens": [f.piece for f in readout.top_flags if f.kind == "green"],
                          "reds": [f.piece for f in readout.top_flags if f.kind == "red"]})
    with (EVIDENCE / "claims.csv").open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=list(claim_rows[0]))
        writer.writeheader()
        writer.writerows(claim_rows)
    (EVIDENCE / "summary.json").write_text(json.dumps(summaries, indent=2) + "\n")
    print(json.dumps(summaries, indent=2))


if __name__ == "__main__":
    main()
