#!/usr/bin/env python3
"""Score the spike's flag claims with the skeleton's real eval.score rule.

    python3 score_spike.py --skeleton-dir <dir holding schema/, scans/, eval/>

The skeleton dir is a copy of the skeleton branch's schema/, scans/base.py and
eval/score.py (git show origin/claude/project-thread-ce34ga:<path>). Reads out/*.json
written by mislabels_spike.py. Prints found of planted and decoys flagged.
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
ROOMS = {"hollis_voice": "answer_key.json", "hollis_voice_seed_drop": "answer_key.json",
         "hollis_voice_clean": "answer_key_clean.json", "brasswick": "answer_key_brasswick.json"}

ap = argparse.ArgumentParser()
ap.add_argument("--skeleton-dir", required=True)
args = ap.parse_args()
sys.path.insert(0, args.skeleton_dir)
from schema.claim import Claim, Readout  # noqa: E402
from eval.score import score  # noqa: E402

for room, key in ROOMS.items():
    out = json.loads((HERE / "out" / f"{room}.json").read_text(encoding="utf-8"))
    readout = Readout(room=room, built_at="spike", claims=[Claim(**c) for c in out["result"]["claims"]])
    line, lines = score(readout, json.loads((REPO / "data_room" / key).read_text(encoding="utf-8")), room)
    print(f"== {room}: found {line.found} of {line.planted} planted, decoys flagged {line.decoys_flagged} of {line.decoys}")
    for ln in lines:
        print("   " + ln)
