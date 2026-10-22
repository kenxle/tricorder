#!/usr/bin/env python3
"""Check the spike's output against the skeleton's real schema, quote checker and scorer.

    python3 validate_against_skeleton.py <skeleton_dir> <room_dir> <spike_output.json>

<skeleton_dir> is a folder holding the skeleton's schema/, scans/ and eval/
packages (for example from `git archive origin/claude/project-thread-ce34ga
schema scans eval`) and a data_room link. Nothing in the repo is changed.

Prints: whether every claim and gap parses as the skeleton's Claim and Gap,
which claims the quote checker could not verify, and the answer-key score
for these claims alone (a Readout holding only them).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main(skel: Path, room: Path, result_path: Path):
    sys.path.insert(0, str(skel))
    from schema.claim import Claim, Gap, Readout
    from schema.check_quotes import check_claim
    from eval.score import key_for, score

    data = json.loads(result_path.read_text())
    claims = [Claim.model_validate(c) for c in data["claims"]]
    gaps = [Gap.model_validate(g) for g in data["gaps"]]
    print(f"schema: {len(claims)} claims and {len(gaps)} gaps parse as schema.claim.Claim and Gap")
    bad = 0
    for c in claims:
        _, problems = check_claim(c, room)
        if problems:
            bad += 1
            print(f"  unverified {c.id}: {problems}")
    print(f"quote checker: {len(claims) - bad} of {len(claims)} claims verified")
    key_path = key_for(room)
    if key_path is None:
        print("score: no answer key names this room")
        return
    key = json.loads(key_path.read_text())
    line, lines = score(Readout(room=room.name, built_at="spike", claims=claims), key, room.name)
    print(f"score against {key_path.name} (these claims only): found {line.found} of {line.planted}, "
          f"decoys flagged {line.decoys_flagged} of {line.decoys}")
    for ln in lines:
        if ln.startswith("found") or ln.startswith("FLAGGED"):
            print("  " + ln)


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]).resolve(), Path(sys.argv[3]))
