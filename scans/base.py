"""What every scan shares: the command line, where results go, ids, gaps,
and which inputs a room holds.

A scan's __main__.py is two lines:

    from scans.base import main
    from scans.<name> import scan
    main(scan)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from types import ModuleType

from schema.claim import Gap, ScanResult

ROOT = Path(__file__).resolve().parent.parent

# Input kinds a scan can declare in NEEDS, and the room files that supply each.
# The scheduler (inbound-unasked) starts a scan once every kind it needs exists.
INPUT_KINDS: dict[str, tuple[str, ...]] = {
    "company_name": ("*/cover_note_and_index.pdf", "*/company_overview.pdf", "*/pitch_deck.pdf", "company.json"),
    "deck": ("*/pitch_deck.pdf",),
    "deck_claims": ("*/claims.json",),
    "overview": ("*/company_overview.pdf",),
    "video": ("*/pitch_video.mp4", "*/pitch_video.transcript.json"),
    "video_script": ("*/pitch_video_script.md",),
    "model": ("*/financial_model.xlsx",),
    "cap_table": ("*/cap_table.xlsx",),
    "ledger": ("*/expense_ledger.csv",),
    "metrics": ("*/monthly_metrics.csv",),
    "customers": ("*/customer_mrr_by_month.csv", "*/revenue_by_customer.csv"),
    "contracts": ("*/order_form_*.pdf", "*/pilot_agreement_*.pdf", "*/msa_*.pdf", "*/sow_*.pdf"),
    "hiring_plan": ("*/hiring_plan.csv",),
    "bios": ("*/founder_bios.pdf",),
    "website": ("*/website_copy.md",),
    "bank": ("bank/*.json",),
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def room_name(room_dir: str | Path) -> str:
    """data_room/hollis_voice_seed_drop -> hollis_voice_seed_drop."""
    return Path(room_dir).resolve().name


def out_dir(room_dir: str | Path) -> Path:
    """out/<room>/, or TRICORDER_OUT_DIR/<room>/."""
    base = Path(os.environ.get("TRICORDER_OUT_DIR", ROOT / "out"))
    return base / room_name(room_dir)


def offline() -> bool:
    """TRICORDER_OFFLINE=1: read cache/ only and make no outside calls."""
    return os.environ.get("TRICORDER_OFFLINE", "") not in ("", "0", "false")


def find(room_dir: str | Path, kind: str) -> list[Path]:
    """Every file in the room that supplies an input kind, sorted."""
    room = Path(room_dir)
    hits: set[Path] = set()
    for pattern in INPUT_KINDS[kind]:
        hits.update(room.glob(pattern))
    return sorted(hits)


def room_inputs(room_dir: str | Path) -> dict[str, list[str]]:
    """Which input kinds the room holds, with the files, relative to the room."""
    room = Path(room_dir)
    held = {}
    for kind in INPUT_KINDS:
        files = find(room, kind)
        if files:
            held[kind] = [str(f.relative_to(room)) for f in files]
    return held


def missing_needs(room_dir: str | Path, needs: tuple[str, ...]) -> list[str]:
    return [k for k in needs if not find(room_dir, k)]


def synthetic_notice(room_dir: str | Path) -> str | None:
    """The room's own "Synthetic ..." line, read from the first page of its
    deck or cover note, for the banner on every screen. Never read from an
    answer key: Tricorder is never pointed at one."""
    from schema.readers import pdf_page

    for kind in ("deck", "company_name"):
        for path in find(room_dir, kind):
            if path.suffix.lower() != ".pdf":
                continue
            for line in pdf_page(path, 1).splitlines():
                if "synthetic" in line.lower():
                    return re.sub(r"\s*(Slide|Page) \d+ of \d+\s*$", "", line).strip()
    return None


class Ids:
    """Claim ids unique inside a scan: redflags-001, redflags-002, ..."""

    def __init__(self, scan: str):
        self.scan, self.n = scan, 0

    def __call__(self) -> str:
        self.n += 1
        return f"{self.scan}-{self.n:03d}"


def gap(what: str, why: str, would_need: str, piece: str | None = None) -> Gap:
    """A missing input. `what` always starts with 'Not in the room:'."""
    if not what.startswith("Not in the room:"):
        what = "Not in the room: " + what[0].lower() + what[1:]
    return Gap(what=what, why=why, would_need=would_need, piece=piece)


def write_result(result: ScanResult, room_dir: str | Path) -> Path:
    target = out_dir(room_dir) / f"{result.scan}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(result.model_dump_json(indent=2) + "\n", encoding="utf-8")
    return target


def main(scan: ModuleType, argv: list[str] | None = None) -> None:
    """python -m scans.<name> <room_dir>: run the scan and write its result.

    A missing input or a refused call is a Gap and the scan still exits 0. A
    crash exits non-zero.
    """
    parser = argparse.ArgumentParser(prog=f"python -m scans.{scan.NAME}")
    parser.add_argument("room_dir", type=Path)
    args = parser.parse_args(argv)
    if not args.room_dir.is_dir():
        parser.error(f"{args.room_dir} is not a folder")
    result = scan.run(args.room_dir)
    target = write_result(result, args.room_dir)
    print(f"{scan.NAME}: {len(result.claims)} claims, {len(result.gaps)} gaps -> {target.relative_to(ROOT) if target.is_relative_to(ROOT) else target}")


def available() -> list[str]:
    """Scans that exist: a package with a scan.py."""
    from scans import SCANS

    here = Path(__file__).parent
    return [name for name in SCANS if (here / name / "scan.py").exists()]


_SLUG = re.compile(r"[^a-z0-9_]+")


def slug(text: str) -> str:
    return _SLUG.sub("_", text.lower()).strip("_")


if __name__ == "__main__":
    print("scans available:", ", ".join(available()) or "none yet", file=sys.stderr)
