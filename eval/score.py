"""Score a readout against a room's answer key.

    python -m eval.score <room_dir> [answer_key.json]

A planted entry counts as found when a readout claim with severity "flag" has
the key's check name and cites at least one of the key's files. A decoy counts
as wrongly flagged when a "flag" claim cites the decoy's file and one of its
locations. Prints found of planted and decoys flagged of decoys.

The answer key sits outside every room folder. Only this script and the
tests read it; no scan ever does.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from schema.claim import Claim, Readout, ScoreLine
from scans.base import out_dir, room_name

DATA_ROOM = Path(__file__).resolve().parent.parent / "data_room"


def key_for(room_dir: Path) -> Path | None:
    """The answer key whose room_path or seed_drop_path names this room."""
    name = Path(room_dir).resolve().name
    for key in sorted(DATA_ROOM.glob("answer_key*.json")):
        data = json.loads(key.read_text(encoding="utf-8"))
        if name in (Path(data.get("room_path", "")).name, Path(data.get("seed_drop_path", "") or "").name):
            return key
    return None


def _check_names(entry: dict) -> set[str]:
    names = entry.get("check")
    if isinstance(names, str):
        return {names}
    return set(names or [])


def _locator_keys(loc: dict) -> set[str]:
    keys = set()
    if "cell" in loc and "sheet" in loc:
        keys.add(f"{loc['sheet']}!{loc['cell']}".lower())
    if "named_cell" in loc:
        keys.add(loc["named_cell"].lower())
    if "page" in loc:
        keys.update({f"page {loc['page']}", f"slide {loc['page']}"})
    return keys


def _cites(claim: Claim, files: set[str], locators: set[str] | None = None) -> bool:
    for s in claim.sources:
        if s.uri in files and (locators is None or not locators or s.locator.lower() in locators):
            return True
    return False


def score(readout: Readout, key: dict, room: str) -> tuple[ScoreLine, list[str]]:
    flags = [c for c in readout.claims if c.severity == "flag"]
    lines, found = [], 0
    for entry in key.get("flags", []):
        files = {loc["file"] for loc in entry.get("locations", [])}
        names = _check_names(entry)
        hit = any(c.check.name.removesuffix(".read") in names and _cites(c, files) for c in flags)
        found += hit
        lines.append(f"{'found ' if hit else 'missed'} {entry['id']} {entry.get('name', '')}")
    wrongly = 0
    for entry in key.get("decoys", []):
        files = {loc["file"] for loc in entry.get("locations", [])}
        locators = set().union(*(_locator_keys(loc) for loc in entry.get("locations", []))) if entry.get("locations") else set()
        hit = any(_cites(c, files, locators) for c in flags)
        wrongly += hit
        lines.append(f"{'FLAGGED' if hit else 'clear  '} {entry['id']} {entry.get('name', '')} (decoy)")
    line = ScoreLine(room=room, found=found, planted=len(key.get("flags", [])), decoys_flagged=wrongly, decoys=len(key.get("decoys", [])))
    return line, lines


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__.strip().splitlines()[2].strip())
        return 2
    room_dir = Path(argv[0])
    key_path = Path(argv[1]) if len(argv) > 1 else key_for(room_dir)
    if key_path is None:
        print(f"no answer key names {room_dir}")
        return 2
    readout_path = out_dir(room_dir) / "readout.json"
    if not readout_path.exists():
        print(f"no readout at {readout_path}; run python -m scans.memo {room_dir}")
        return 2
    readout = Readout.model_validate_json(readout_path.read_text(encoding="utf-8"))
    line, lines = score(readout, json.loads(key_path.read_text(encoding="utf-8")), room_name(room_dir))
    print("\n".join(lines))
    print(f"{line.room}: found {line.found} of {line.planted}; decoys flagged {line.decoys_flagged} of {line.decoys}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
