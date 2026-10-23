"""Build the readout from whatever scan results exist.

    python -m scans.memo <room_dir>

The merge itself is fixed: load each out/<room>/<scan>.json, run the quote
checker again, move unverified claims to their own box, and turn each missing
scan into a gap. Everything after that is a step in STEPS, run in order. A
step is a module in this package with

    def apply(readout: Readout, room_dir: Path) -> Readout

A step that does not exist yet is skipped, so the readout slices can land in
any order without editing this file. Every step is a script: verdicts, flags
and asks never come from a model (FRAMEWORKS.md, "The readout").

A rebuild keeps the steers (review wave 2b, S7). When the readout on disk
holds revisions, `build_readout` keeps them, their "steer N: what changed"
panels and the operator's scenario lines (steering.engine.carry does it). When
a "read the full room" steer switched the readout, the rebuild reads the full
room's scan results and resolves every source there.

Which room a readout's sources resolve in (review wave 2b, B1) is one panel:

    Panel(name="reads room", columns=["Room", "Since"], rows=[["<full room name>", "steer <n>"]])

`reads_room(readout, room_dir)` reads it, and `readout_room(room_dir)` reads it
from out/<room>/readout.json. Every reader of a readout's sources (the memo,
the source and file routes, steering) resolves the room through one of them.
The panel only ever names the seed drop's own full room, the sibling folder
named without "_seed_drop"; any other name is ignored, so a readout cannot
point a reader at another folder.
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path

from schema.check_quotes import check_result
from schema.claim import Panel, Readout, ScanResult
from scans import SCANS
from scans.base import available, gap, now_iso, out_dir, room_name, synthetic_notice

STEPS: tuple[str, ...] = (
    "link",        # conflicts_with and corroborated_by (ARCHITECTURE, "How the readout merges")
    "claim_support",  # pitch claims relabelled against other scans' flags (claim-support slice)
    "pieces",      # FRAMEWORKS "Piece verdicts"
    "top_flags",   # FRAMEWORKS "Top green and red flags"
    "coverage",    # FRAMEWORKS "Checklist coverage"
    "asks",        # FRAMEWORKS "Ask list"
    "connecting",  # the one model pass: connecting sentences, each citing claim ids
)


SEED_SUFFIX = "_seed_drop"
READS_PANEL = "reads room"


def full_room_of(room_dir: Path) -> Path | None:
    """The seed drop's second tier: the sibling folder named without '_seed_drop'."""
    name = Path(room_dir).resolve().name
    if not name.endswith(SEED_SUFFIX):
        return None
    full = Path(room_dir).resolve().parent / name[: -len(SEED_SUFFIX)]
    return full if full.is_dir() else None


def reads_panel(room: str, steer_n: int) -> Panel:
    """The marker a "read the full room" steer writes: the room every source resolves in, and since which steer."""
    return Panel(name=READS_PANEL, columns=["Room", "Since"], rows=[[room, f"steer {steer_n}"]])


def reads_room(readout: Readout | None, room_dir: Path) -> Path:
    """The room the readout's sources resolve in: the full room once a "read the full room" steer switched it,
    else the room itself. Also reads the "source" row of a steer panel, which readouts steered before the
    "reads room" panel carry."""
    room_dir = Path(room_dir)
    full = full_room_of(room_dir) if readout is not None else None
    if full is None:
        return room_dir
    named = {r[0] for p in readout.panels if p.name == READS_PANEL for r in p.rows if r}
    named |= {r[3] for p in readout.panels if p.name.startswith("steer ") for r in p.rows if len(r) > 3 and r[0] == "source"}
    return full if full.name in named else room_dir


def on_disk(room_dir: Path) -> Readout | None:
    path = out_dir(room_dir) / "readout.json"
    if not path.exists():
        return None
    return Readout.model_validate_json(path.read_text(encoding="utf-8"))


def readout_room(room_dir: Path) -> Path:
    """The room the readout at out/<room>/readout.json resolves its sources in (see reads_room)."""
    return reads_room(on_disk(room_dir), room_dir)


def _steered(readout: Readout | None) -> bool:
    return readout is not None and bool(readout.revisions or any(c.scan == "steering" for c in readout.claims)
                                        or any(p.name == READS_PANEL for p in readout.panels))


def load_results(room_dir: Path) -> tuple[list[ScanResult], list[str]]:
    results, missing = [], []
    folder = out_dir(room_dir)
    for name in SCANS:
        path = folder / f"{name}.json"
        if path.exists():
            results.append(ScanResult.model_validate_json(path.read_text(encoding="utf-8")))
        else:
            missing.append(name)
    return results, missing


def _step(name: str):
    try:
        return importlib.import_module(f"scans.memo.{name}")
    except ModuleNotFoundError as err:
        if err.name == f"scans.memo.{name}":
            return None
        raise


def build_readout(room_dir: Path, *, keep_steers: bool = True) -> Readout:
    """The readout from the scan results. With keep_steers (the default, for every rebuild a person starts),
    a steered readout on disk keeps its revisions, steer panels, scenario lines and full-room switch.
    Steering passes keep_steers=False for the fresh build it merges itself."""
    room_dir = Path(room_dir)
    before = on_disk(room_dir) if keep_steers else None
    steered = _steered(before)
    source = reads_room(before, room_dir) if steered else room_dir
    results, missing = load_results(source)
    built = set(available())
    readout = Readout(room=room_name(room_dir), built_at=now_iso(), synthetic_notice=synthetic_notice(room_dir))
    for result in results:
        checked, _ = check_result(result, source)
        readout.claims += [c for c in checked.claims if c.confidence != "unverified"]
        readout.unverified += [c for c in checked.claims if c.confidence == "unverified"]
        readout.gaps += checked.gaps
        readout.panels += checked.panels
        readout.scans_run.append(result.scan)
    for name in missing:
        why = "the scan did not run on this room" if name in built else "the scan is not built yet"
        readout.gaps.append(gap(f"Not in the room: the {name} scan's results", why, f"python -m scans.{name} {source}"))
    readout.scans_missing = missing
    for name in STEPS:
        module = _step(name)
        if module is not None:
            readout = module.apply(readout, source)
    if steered:
        from steering.engine import carry  # steering owns what a steer leaves in a readout

        readout = carry(before, readout, source)
    return readout


def write_readout(readout: Readout, room_dir: Path) -> Path:
    target = out_dir(room_dir) / "readout.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(readout.model_dump_json(indent=2) + "\n", encoding="utf-8")
    return target


def main(argv: list[str]) -> int:
    fresh = "--fresh" in argv
    args = [a for a in argv if a != "--fresh"]
    if len(args) != 1 or not Path(args[0]).is_dir():
        print("usage: python -m scans.memo <room_dir> [--fresh]\n"
              "  --fresh  start over: drop the steers' revisions, scenario lines and full-room switch")
        return 2
    readout = build_readout(Path(args[0]), keep_steers=not fresh)
    target = write_readout(readout, Path(args[0]))
    print(json.dumps({
        "readout": str(target),
        "claims": len(readout.claims),
        "unverified": len(readout.unverified),
        "gaps": len(readout.gaps),
        "scans_run": readout.scans_run,
        "scans_missing": readout.scans_missing,
        "revisions_kept": len(readout.revisions),
        "reads_room": room_name(reads_room(readout, Path(args[0]))),
    }, indent=2))
    return 0
