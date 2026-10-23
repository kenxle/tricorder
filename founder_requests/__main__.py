"""Requests to the founder, from the command line.

    python -m founder_requests list <room_dir>
    python -m founder_requests draft <room_dir> [--lines N ...] [--all] [--to EMAIL] [--sender NAME] [--json]
    python -m founder_requests copy-room <room_dir> [--as NAME]
    python -m founder_requests add <room_dir> <file> --for C22|N [--copy]

`draft` prints the subject, the message and the mailto link; it sends nothing. `add` saves a reply's
file in the room, reruns the scans that were waiting on it and rebuilds the readout. A room in
data_room/ is never written: `copy-room` (or `add --copy`) copies it to rooms/<room>_live first.
Exit codes: 0 done, 1 refused, 2 bad arguments or no readout.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from schema.claim import Readout
from scans.base import out_dir
from founder_requests import draft as d
from founder_requests import intake as ik


def _readout(room: Path) -> Readout:
    path = out_dir(room) / "readout.json"
    if not path.exists():
        print(f"No readout for {room.name} yet. Build it first: python -m scans.memo {room}", file=sys.stderr)
        raise SystemExit(2)
    return Readout.model_validate_json(path.read_text(encoding="utf-8"))


def cmd_list(args) -> int:
    for i in d.items(_readout(args.room_dir)):
        tags = [f"Top {i.top}"] if i.top else []
        tags += ["if you have it"] if i.if_you_have_it else []
        tags += ["after the term sheet"] if i.ask_stage == "after_term_sheet" else []
        print(f"{i.number:>3}. {i.title}" + (f"  [{', '.join(tags)}]" if tags else ""))
        print(f"     {i.text}")
    return 0


def cmd_draft(args) -> int:
    readout = _readout(args.room_dir)
    numbers = [i.number for i in d.items(readout)] if args.all else args.lines
    try:
        out = d.draft(readout, numbers, room_dir=args.room_dir, to=args.to, sender=args.sender)
    except ValueError as err:
        print(err, file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(asdict(out), indent=2))
        return 0
    print(f"Subject: {out.subject}\n\n{out.body}")
    print(f"mailto ({len(out.mailto)} characters{'' if out.mailto_fits else '; long for a mail link, copy the text instead'}):")
    print(out.mailto)
    return 0


def cmd_copy(args) -> int:
    try:
        dest = ik.copy_room(args.room_dir, args.as_name)
    except ik.IntakeError as err:
        print(err.message, file=sys.stderr)
        return 1
    print(f"Copied {args.room_dir} to {dest}")
    return 0


def cmd_add(args) -> int:
    room = args.room_dir
    try:
        if ik.is_synthetic(room) and args.copy:
            existing = ik.rooms_root() / (room.name + ik.COPY_SUFFIX)
            room = existing if existing.is_dir() else ik.copy_room(room)
        receipt = ik.receive(room, args.file.read_bytes(), args.file.name, args.answers)
    except ik.IntakeError as err:
        print(err.message, file=sys.stderr)
        return 1
    print(json.dumps(receipt, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m founder_requests", description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list", help="every ask line with its founder words")
    s.add_argument("room_dir", type=Path)
    s.set_defaults(fn=cmd_list)
    s = sub.add_parser("draft", help="draft a message; nothing is sent")
    s.add_argument("room_dir", type=Path)
    s.add_argument("--lines", type=int, nargs="+", help="ask line numbers; default the pinned top five")
    s.add_argument("--all", action="store_true", help="every ask line")
    s.add_argument("--to", default="")
    s.add_argument("--sender", default="")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_draft)
    s = sub.add_parser("copy-room", help="copy a room to rooms/ so replies can be added")
    s.add_argument("room_dir", type=Path)
    s.add_argument("--as", dest="as_name", default=None)
    s.set_defaults(fn=cmd_copy)
    s = sub.add_parser("add", help="add a founder's file, rerun waiting scans, rebuild the readout")
    s.add_argument("room_dir", type=Path)
    s.add_argument("file", type=Path)
    s.add_argument("--for", dest="answers", required=True, help="checklist id (C22) or ask line number")
    s.add_argument("--copy", action="store_true", help="for a data_room/ room, work in rooms/<room>_live")
    s.set_defaults(fn=cmd_add)
    args = p.parse_args(argv)
    if not args.room_dir.is_dir():
        p.error(f"{args.room_dir} is not a folder")
    if getattr(args, "file", None) is not None and not args.file.is_file():
        p.error(f"{args.file} is not a file")
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
