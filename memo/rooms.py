"""The rooms a readout's sources resolve in, and the one rule that keeps a source inside them.

    reads_room(readout, room_dir) -> the room every line's files open from now
    source_rooms(readout, room_dir) -> [that room, then the readout's own room], no others, ever
    resolve(uri, rooms) -> the file, inside one of those rooms, or LocatorError
    text_in(source, rooms) -> the text at the source's locator, read only from inside those rooms
    check_claim_in(claim, rooms) -> the quote check, with every file source held inside those rooms

A readout reads its own room. After a "read the full room" steer on a seed drop,
it reads the full room. Steering records the switch two ways, and either one counts:
a "reads room" panel with the row [<full room>, "steer N"] (the marker
scans/memo/merge.py names), and a row ["source", "", <seed drop>, <full room>] in
the steer's "steer N: what changed" panel (the marker older readouts carry). A
marker naming any folder other than the seed drop's own full room is ignored. The full room is the seed drop's sibling folder named without
"_seed_drop", so it is always under the same rooms root. The seed drop's own files
are byte-for-byte copies of the full room's, so every line, old or new, resolves
there after a switch.

A source never resolves outside those rooms: not an absolute path, not a "..",
not another room, not the repo's own files, and never a sealed answer key.
"""

from __future__ import annotations

from pathlib import Path

from schema.check_quotes import source_holds_quote
from schema.claim import Claim, Readout, Source
from schema.readers import LocatorError, text_at

SEED_SUFFIX = "_seed_drop"  # the same suffix steering/engine.py names
READS_PANEL = "reads room"  # the switch marker's panel name
SEALED_PREFIX = "answer_key"  # data_room/answer_key*.json: the planted flags, never served


class OutsideRoom(LocatorError):
    """A source or file path that would leave its room."""


def full_room_of(room_dir: str | Path) -> Path | None:
    """The seed drop's full room: its sibling named without '_seed_drop', or None."""
    own = Path(room_dir).resolve()
    if not own.name.endswith(SEED_SUFFIX):
        return None
    full = (own.parent / own.name[: -len(SEED_SUFFIX)]).resolve()
    return full if full.is_dir() and full.parent == own.parent else None


def reads_room(readout: Readout | None, room_dir: str | Path) -> Path:
    """The room the readout reads now: the full room once a steer switched it, else its own."""
    own = Path(room_dir)
    full = full_room_of(own)
    if readout is None or full is None:
        return own
    named = {r[0] for p in readout.panels if p.name == READS_PANEL for r in p.rows if r}
    named |= {r[3] for p in readout.panels if p.name.startswith("steer ") for r in p.rows if len(r) > 3 and r[0] == "source"}
    return full if full.name in named else own


def source_rooms(readout: Readout | None, room_dir: str | Path) -> list[Path]:
    """Where a source may resolve, in order: the room the readout reads, then its own room."""
    first = reads_room(readout, room_dir)
    own = Path(room_dir)
    return [first] if first.resolve() == own.resolve() else [first, own]


def resolve(uri: str, rooms: list[Path]) -> Path:
    """The file uri names, inside the first room that holds it. Never outside them."""
    rel = Path(uri)
    if rel.is_absolute() or not uri.strip():
        raise OutsideRoom(f"{uri!r} is not a path inside the room")
    for room in rooms:
        base = Path(room).resolve()
        target = (base / rel).resolve()
        if not target.is_relative_to(base) or target == base:
            raise OutsideRoom(f"{uri!r} leaves the room")
        if target.name.lower().startswith(SEALED_PREFIX):
            raise OutsideRoom(f"{uri!r} is sealed")
        if target.is_file():
            return target
    raise LocatorError(f"{uri} is not in {' or '.join(Path(r).name for r in rooms)}")


def is_file_source(source: Source) -> bool:
    return source.kind not in ("url", "api")


def room_holding(source: Source, rooms: list[Path]) -> Path:
    """The room a file source resolves in, for readers that take a room (the quote checker)."""
    path = resolve(source.uri, rooms)
    return next(Path(r) for r in rooms if path.is_relative_to(Path(r).resolve()))


def text_in(source: Source, rooms: list[Path]) -> str:
    """The text at a source's locator. A file source is read only from inside the rooms."""
    if not is_file_source(source):
        return text_at(source, rooms[0])
    return text_at(source, room_holding(source, rooms))


def check_claim_in(claim: Claim, rooms: list[Path]) -> tuple[Claim, list[str]]:
    """schema.check_quotes.check_claim, with each file source resolved inside the rooms only."""
    problems = []
    for source in claim.sources:
        room = rooms[0]
        if is_file_source(source):
            try:
                room = room_holding(source, rooms)
            except OutsideRoom as err:
                problems.append(str(err))
                continue
            except LocatorError:
                pass  # not in any room: the checker names the missing file
        ok, why = source_holds_quote(source, room)
        if not ok:
            problems.append(why)
    if problems:
        return claim.model_copy(update={"confidence": "unverified"}), problems
    return claim, []
