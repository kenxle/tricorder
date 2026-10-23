"""python -m memo <room_dir | readout.json> [--room-dir DIR] [--edit edits.json --author NAME] [--no-pdf]

Writes a new memo version to out/<room>/memo/memo_v<N>.json, and the page
(memo.html) and the PDF (memo.pdf) beside it. With --edit, applies the
operator's edits (a JSON list of {action, section, line_id, text, claim_ids})
to the latest version instead of redrafting. Prints a JSON summary.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pydantic import ValidationError

from founder_requests.intake import rooms_root
from scans.base import ROOT

from memo.edit import EditError
from memo.export import NoReadout, edit, export
from memo.model import Edit


def _room_for(readout: Path, room_dir: str | None) -> Path:
    if room_dir:
        return Path(room_dir)
    name = json.loads(readout.read_text(encoding="utf-8"))["room"]
    for parent in (ROOT / "data_room", rooms_root()):  # rooms/, or TRICORDER_ROOMS_DIR, as the server reads them
        if (parent / name).is_dir():
            return parent / name
    raise NoReadout(f"cannot find room {name!r}; pass --room-dir")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="python -m memo", description=__doc__.strip().splitlines()[0])
    ap.add_argument("target", help="a room folder, or a readout.json")
    ap.add_argument("--room-dir", help="the room folder, when target is a readout.json outside out/<room>/")
    ap.add_argument("--edit", help="a JSON file of operator edits")
    ap.add_argument("--author", help="who made the edits")
    ap.add_argument("--no-pdf", action="store_true")
    args = ap.parse_args(argv)
    target = Path(args.target)
    try:
        if target.is_file():
            room, readout = _room_for(target, args.room_dir), target
        elif target.is_dir():
            room, readout = target, None
        else:
            raise NoReadout(f"{target} is neither a room folder nor a readout.json")
        if args.edit:
            if not args.author:
                raise EditError("--edit needs --author")
            edits = [Edit.model_validate(e) for e in json.loads(Path(args.edit).read_text(encoding="utf-8"))]
            out = edit(room, edits, args.author, pdf=not args.no_pdf)
        else:
            out = export(room, readout, pdf=not args.no_pdf)
    except (NoReadout, EditError, ValidationError, json.JSONDecodeError) as err:
        print(f"memo: {err}", file=sys.stderr)
        return 2
    memo = out.memo
    print(json.dumps({
        "memo": str(out.json), "html": str(out.html), "pdf": str(out.pdf) if out.pdf else None,
        "version": memo.version, "sections": len(memo.sections), "claims": len(memo.claims),
        "could_not_verify": sum(1 for ln in memo.section(14).lines if ln.kind == "unverified"),
        "sections_empty": {f"{s.number}. {s.title}": s.empty_because for s in memo.sections if s.empty_because},
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
