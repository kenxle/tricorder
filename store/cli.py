"""python -m store: the readout store from a terminal. JSON on stdout.

    python -m store save <room_dir> [--fund demo] [--company <room name>]
    python -m store list <company> [--fund demo]
    python -m store get <company> [--fund demo] [--version N] [--full]
    python -m store companies [--fund demo]
    python -m store delete <company> [--fund demo] [--yes]

Exit 0 when done, 1 when nothing is held or a delete is not confirmed, 2 for
a bad id or bad arguments. Delete cannot be undone, so it asks the operator to
type the company id unless --yes is given.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .base import BadId, NotHeld, open_store
from .files import load_from_out


def _print(model_or_data) -> None:
    if hasattr(model_or_data, "model_dump_json"):
        print(model_or_data.model_dump_json(indent=2))
    else:
        print(json.dumps(model_or_data, indent=2))


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m store", description="The readout store: save, list, get and delete what is held per fund and company.")
    sub = p.add_subparsers(dest="command", required=True)

    def with_fund(sp):
        sp.add_argument("--fund", default="demo", help="fund id (default: demo)")
        return sp

    s = with_fund(sub.add_parser("save", help="store the room's current readout, its scan results and the files it read"))
    s.add_argument("room_dir", type=Path)
    s.add_argument("--company", help="company id (default: the room's folder name)")
    with_fund(sub.add_parser("list", help="everything held for one company")).add_argument("company")
    g = with_fund(sub.add_parser("get", help="a stored readout, the latest unless --version"))
    g.add_argument("company")
    g.add_argument("--version", type=int)
    g.add_argument("--full", action="store_true", help="print the whole readout and scan results")
    with_fund(sub.add_parser("companies", help="the companies held for a fund"))
    d = with_fund(sub.add_parser("delete", help="remove everything held for one company, and its outside pulls in cache/"))
    d.add_argument("company")
    d.add_argument("--yes", action="store_true", help="do not ask for confirmation")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    store = open_store()
    try:
        if args.command == "save":
            if not args.room_dir.is_dir():
                print(f"{args.room_dir} is not a folder", file=sys.stderr)
                return 2
            company = args.company or args.room_dir.resolve().name
            readout, results = load_from_out(args.room_dir)
            _print(store.save(args.fund, company, readout, args.room_dir, results))
        elif args.command == "list":
            _print(store.list_company(args.fund, args.company))
        elif args.command == "get":
            got = store.get(args.fund, args.company, args.version)
            if args.full:
                _print(got)
            else:
                r = got.readout
                _print({
                    "fund": got.fund, "company": got.company, "version": got.version.model_dump(mode="json"),
                    "readout": {"room": r.room, "built_at": r.built_at, "claims": len(r.claims), "unverified": len(r.unverified),
                                "gaps": len(r.gaps), "pieces": len(r.pieces), "revisions": len(r.revisions)},
                    "results": [x.scan for x in got.results],
                })
        elif args.command == "companies":
            _print(store.companies(args.fund))
        elif args.command == "delete":
            held = store.list_company(args.fund, args.company)
            if not args.yes:
                print(
                    f"This removes everything held for {args.fund}/{args.company}: {len(held.versions)} versions, "
                    f"{len(held.files)} files, {len(held.cache)} files in cache/, {held.total_bytes} bytes. It cannot be undone.",
                    file=sys.stderr,
                )
                print(f"Type the company id ({args.company}) to delete: ", end="", file=sys.stderr, flush=True)
                answer = sys.stdin.readline().strip()
                if answer != args.company:
                    print("Not confirmed. Nothing removed.", file=sys.stderr)
                    return 1
            _print(store.delete_company(args.fund, args.company))
    except BadId as err:
        print(f"bad id: {err}", file=sys.stderr)
        return 2
    except NotHeld as err:
        print(str(err), file=sys.stderr)
        return 1
    return 0
