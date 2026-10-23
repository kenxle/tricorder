"""One steer: one sentence on a piece (or a line) rebuilds that piece.

    python -m steering <room_dir> <piece> "<sentence>" [--line <claim id>] [--fund demo] [--author name]

The flow (docs/features/20261023.05_steering/04_architecture.md, "Flow"):
load the readout, read the sentence, rerun the piece's scans on the right room,
apply the one reread the sentence asks for, quote-check what changed, rebuild
verdicts, record a PieceRevision and a "steer N: what changed" Panel, write
the readout back to out/<room>/readout.json, and save it to the store.

A steer never changes a check's number (FEATURES.md, "A steer changes the
reading, not the numbers").
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Callable

from schema.check_quotes import check_claim
from schema.claim import PIECE_ORDER, Claim, Panel, Piece, PieceRevision, Readout, ScanResult, Steer
from scans.base import available, now_iso, out_dir, room_name, write_result
from scans.memo.merge import build_readout, load_results, write_readout
from steering import verdicts
from steering.classify import model_available, read_sentence
from steering.models import Reading, SteerOutcome, StoreNote
from steering.rereads import exclude_from_recurring
from steering.reword import reword

MAX_SENTENCE = 500
SEED_SUFFIX = "_seed_drop"
VERDICT_WORDS = {"looking_strong": "Looking strong", "looking_weak": "Looking weak", "mixed": "Mixed",
                 "not_enough_in_the_room": "Not enough in the room"}
PIECE_WORDS = {p: p.replace("_", " ") for p in PIECE_ORDER}


class BadSteer(ValueError):
    """The steer cannot run as asked: an empty sentence, an unknown piece or line."""


class NoReadout(LookupError):
    """No readout and no scan results for the room."""


# --------------------------------------------------------------------------- loading


def load_readout(room_dir: Path) -> Readout:
    path = out_dir(room_dir) / "readout.json"
    if path.exists():
        return Readout.model_validate_json(path.read_text(encoding="utf-8"))
    results, _ = load_results(room_dir)
    if not results:
        raise NoReadout(f"no readout for {room_name(room_dir)}: run python -m scans.redflags {room_dir} "
                        f"and python -m scans.memo {room_dir} first")
    readout = build_readout(room_dir)
    write_readout(readout, room_dir)
    return readout


def steerable(room_dir: Path) -> Readout:
    """The room's readout with verdicts, built by the same rules a steer uses."""
    readout = load_readout(Path(room_dir))
    if not readout.pieces:
        readout, _ = verdicts.rebuild(readout, Path(room_dir))
    return readout


def full_room_of(room_dir: Path) -> Path | None:
    """The seed drop's second tier: the sibling folder named without '_seed_drop'."""
    name = Path(room_dir).resolve().name
    if not name.endswith(SEED_SUFFIX):
        return None
    full = Path(room_dir).resolve().parent / name[: -len(SEED_SUFFIX)]
    return full if full.is_dir() else None


# --------------------------------------------------------------------------- claims


def _key(c: Claim) -> tuple:
    if c.value is not None:
        return (c.check.name, c.value.label, c.value.unit, c.value.period, round(c.value.number, 6))
    return (c.check.name, c.text)


def _piece_claims(readout: Readout, piece: str) -> list[Claim]:
    return [c for c in readout.claims if verdicts.piece_of(c) == piece]


def _scans_feeding(readout: Readout, piece: str) -> list[str]:
    built = set(available())
    names = {c.scan for c in _piece_claims(readout, piece)} | {c.scan for c in readout.unverified if verdicts.piece_of(c) == piece}
    if any(g.piece == piece for g in readout.gaps):
        names |= set(readout.scans_run)
    names &= built
    return sorted(names) if names else sorted(built)


def _rerun(scans: list[str], room: Path) -> list[ScanResult]:
    results = []
    for name in scans:
        module = importlib.import_module(f"scans.{name}.scan")
        result = module.run(room)
        write_result(result, room)
        results.append(result)
    return results


def _merge_piece(before: Readout, fresh: Readout, piece: str, tag: str) -> tuple[Readout, list[str], list[str]]:
    """The before readout with the piece's claims, unverified claims and gaps taken from the fresh merge.
    Returns (readout, added ids, dropped ids). Matched claims keep their ids; new ones get the tag."""
    old = _piece_claims(before, piece)
    old_by_key = {_key(c): c for c in old}
    fresh_piece = _piece_claims(fresh, piece)
    taken = {id(c) for c in old}
    ids: dict[str, str] = {}
    for c in fresh_piece:
        match = old_by_key.get(_key(c))
        ids[c.id] = match.id if match is not None else f"{c.id}.{tag}"
    # Links point at fresh ids; a link to a claim outside the piece keeps the before id it matches, if any.
    before_by_key = {_key(c): c.id for c in before.claims}
    for c in fresh.claims:
        if c.id not in ids and _key(c) in before_by_key:
            ids[c.id] = before_by_key[_key(c)]

    def remap(c: Claim) -> Claim:
        return c.model_copy(update={"id": ids.get(c.id, c.id),
                                    "conflicts_with": [ids.get(i, i) for i in c.conflicts_with],
                                    "corroborated_by": [ids.get(i, i) for i in c.corroborated_by]})

    new_piece = [remap(c) for c in fresh_piece]
    new_keys = {_key(c) for c in fresh_piece}
    dropped = [c.id for c in old if _key(c) not in new_keys]
    added = [c.id for c in new_piece if c.id not in {o.id for o in old}]
    claims = [c for c in before.claims if id(c) not in taken] + new_piece
    unverified = [c for c in before.unverified if verdicts.piece_of(c) != piece] + \
                 [remap(c) for c in fresh.unverified if verdicts.piece_of(c) == piece]
    gaps = [g for g in before.gaps if g.piece != piece] + [g for g in fresh.gaps if g.piece == piece]
    return before.model_copy(update={"claims": claims, "unverified": unverified, "gaps": gaps}), added, dropped


# --------------------------------------------------------------------------- the steer

LABEL_WORDS = (("arr", "arr"), ("mrr", "mrr"), ("net revenue retention", "nrr_12m"), ("nrr", "nrr_12m"),
               ("gross revenue retention", "grr_12m"), ("grr", "grr_12m"), ("runway", "runway_months"),
               ("burn", "net_burn_monthly"), ("gross margin", "gross_margin"), ("cash", "cash"))


def _label_named(sentence: str) -> str | None:
    words = f" {sentence.lower()} "
    return next((label for word, label in LABEL_WORDS if f" {word} " in words or f" {word}," in words), None)



def _path_words(reading: Reading) -> str:
    kind = "more info" if reading.kind == "more_info" else "a rewrite"
    if reading.path == "model":
        return f"Read as {kind} by a model reading."
    why = f"; the model path was not used: {reading.fallback_why}" if reading.fallback_why else ("; no model key set" if not model_available() else "")
    return f"Read as {kind} by wording rules{why}."


def _rebuilt_words(by: str) -> str:
    if by == "merge":
        return "Verdicts rebuilt by the merge's pieces and top_flags steps."
    return ("Verdicts rebuilt by steering's copy of the FRAMEWORKS rules, because the merge's pieces "
            "and top_flags steps are not built yet." if by == "steering" else f"Verdicts rebuilt by {by}.")


def _moved_by(before_r: Readout, after_r: Readout, before: Piece, after: Piece, added: list[str], dropped: list[str]) -> list[str]:
    if before.verdict == after.verdict:
        return []
    now = {c.id: c for c in after_r.claims}
    was = {c.id: c for c in before_r.claims}
    decisive = lambda c: verdicts.contradicted(c) or verdicts.corroborated(c)  # noqa: E731
    moved = [i for i in added if i in now and decisive(now[i])] + [i for i in dropped if i in was and decisive(was[i])]
    return moved or list(after.reason_claim_ids)


def steer(room_dir: str | Path, piece: str, sentence: str, claim_id: str | None = None, author: str | None = None,
          *, fund: str = "demo", llm: Callable | None = None, save: bool = True) -> SteerOutcome:
    room_dir = Path(room_dir)
    sentence = " ".join((sentence or "").split())
    if not sentence:
        raise BadSteer("type one sentence")
    if len(sentence) > MAX_SENTENCE:
        raise BadSteer(f"one sentence, up to {MAX_SENTENCE} characters")
    if piece not in PIECE_ORDER:
        raise BadSteer(f"no piece {piece!r}; pieces are {', '.join(PIECE_ORDER)}")

    current = load_readout(room_dir)
    if claim_id is not None:
        line = next((c for c in current.claims + current.unverified if c.id == claim_id), None)
        if line is None:
            raise BadSteer(f"no line {claim_id!r} in the readout")
        if verdicts.piece_of(line) != piece:
            raise BadSteer(f"line {claim_id!r} is in {verdicts.piece_of(line)}, not {piece}")
    if not current.pieces:
        current, _ = verdicts.rebuild(current, room_dir)
    before_piece = next(p for p in current.pieces if p.name == piece)
    n = len(current.revisions) + 1
    tag = f"steer{n}"

    reading = read_sentence(sentence, llm=llm if llm is not None else None)
    source_room = room_dir
    notes: list[str] = []
    wording: list[tuple[str, str, str]] = []
    working, added, dropped = current, [], []
    sources_note = ""

    if reading.kind == "more_info":
        if reading.source == "full_room":
            full = full_room_of(room_dir)
            if full is None:
                notes.append(f"This room is already the full room, or has no second tier beside it, so nothing new was read.")
            else:
                source_room = full
                _rerun(_scans_feeding(current, piece), full)
                fresh = build_readout(full)
                working, added, dropped = _merge_piece(current, fresh, piece, tag)
        else:
            notes.append(f"You asked for {reading.source_named}. Tricorder does not fetch outside sources on a steer yet, "
                         f"so it was not fetched; ask the founder or add it to the room.")
    else:
        scans = _scans_feeding(current, piece)
        if reading.number_text is None:
            _rerun(scans, room_dir)
            working, added, dropped = _merge_piece(current, build_readout(room_dir), piece, tag)
        if reading.term:
            piece_claims = _piece_claims(working, piece)
            if claim_id is not None:
                line = [c for c in piece_claims if c.id == claim_id and c.value and c.value.label == "arr"]
                piece_claims = line or piece_claims
            counter = iter(range(1, 1000))
            new, why = exclude_from_recurring(reading.term, piece_claims, room_dir, lambda: f"{tag}-{next(counter):03d}")
            notes += why
            working = working.model_copy(update={"claims": working.claims + new})
            added += [c.id for c in new]
        elif reading.number_text is not None:
            target = next((c for c in current.claims if c.id == claim_id), None) if claim_id else None
            named = _label_named(sentence)
            target = target or next((c for c in _piece_claims(current, piece) if c.value and c.value.label == named), None) \
                or next((c for c in _piece_claims(current, piece) if c.id in before_piece.reason_claim_ids), None) \
                or next((c for c in _piece_claims(current, piece) if c.value is not None), None)
            ask = f"You asked for {reading.number_text}."
            notes.append(f'{ask} The check\'s number stays as it wrote it: "{target.text}"' if target
                         else f"{ask} No check in this piece states a number, so nothing changed.")
        elif reading.path == "model":
            kept, refused = reword(_piece_claims(working, piece), sentence, llm or _llm())
            if refused:
                notes.append("Rewording refused for " + "; ".join(refused) + ".")
            claims = []
            for c in working.claims:
                if c.id in kept:
                    wording.append((c.id, c.text, kept[c.id]))
                    c = c.model_copy(update={"text": kept[c.id]})
                claims.append(c)
            working = working.model_copy(update={"claims": claims})
        else:
            notes.append("No wording rule matched this sentence and no model key is set, so the lines keep their words.")

    # Quote-check what changed, against the room its sources are in.
    changed = set(added) | {w[0] for w in wording}
    failed = []
    claims = []
    for c in working.claims:
        if c.id in changed:
            checked, problems = check_claim(c, source_room)
            if problems:
                failed.append(c.id)
                working = working.model_copy(update={"unverified": working.unverified + [checked]})
                continue
        claims.append(c)
    working = working.model_copy(update={"claims": claims})
    if failed:
        notes.append(f"Could not verify {', '.join(failed)}: its quote was not found, so it went to the could-not-verify box.")
        added = [i for i in added if i not in failed]

    after_r, rebuilt_by = verdicts.rebuild(working, source_room)
    after_piece = next(p for p in after_r.pieces if p.name == piece)
    moved = _moved_by(current, after_r, before_piece, after_piece, added, dropped)
    now = {c.id: c for c in after_r.claims}
    was = {c.id: c for c in current.claims}

    # The note, in BRAND.md's words ("A steered piece").
    if reading.kind == "more_info" and source_room != room_dir:
        new_sources = sorted({s.uri for i in added for s in now[i].sources} - {s.uri for c in _piece_claims(current, piece) for s in c.sources})
        sources_note = f" Read {len(new_sources)} new source{'s' if len(new_sources) != 1 else ''} ({', '.join(new_sources)}) from {room_name(source_room)}."
        head = f'More info on your instruction: "{sentence}".{sources_note} {len(added)} new claim{"s" if len(added) != 1 else ""}, marked new.'
    elif reading.kind == "more_info":
        head = f'More info on your instruction: "{sentence}".'
    else:
        what = (f" Added {len(added)} line{'s' if len(added) != 1 else ''}." if added else "") + \
               (f" Dropped {len(dropped)} line{'s' if len(dropped) != 1 else ''}." if dropped else "") + \
               (f" Reworded {len(wording)} line{'s' if len(wording) != 1 else ''}." if wording else "")
        head = f'Rewritten on your instruction: "{sentence}".{what}'
    if before_piece.verdict == after_piece.verdict:
        verdict = "Verdict unchanged."
    else:
        movers = "; ".join(f'"{now[i].text.rstrip(".")}"' for i in moved if i in now) or "the rule"
        verdict = f"Verdict: {VERDICT_WORDS[before_piece.verdict]} to {VERDICT_WORDS[after_piece.verdict]}, moved by {movers}."
    if before_piece.reason != after_piece.reason:
        verdict += " The reason line changed."
    numbers = "" if reading.number_text else " The checks' numbers are unchanged."
    scope = f" Only {PIECE_WORDS[piece]} read the new source; other pieces still read {room_name(room_dir)}." if source_room != room_dir else ""
    note = " ".join(filter(None, [head, verdict + numbers + scope, " ".join(notes), _path_words(reading), _rebuilt_words(rebuilt_by)]))

    sources_added = sorted({f"{s.uri}, {s.locator}" for i in added for s in now[i].sources}
                           - {f"{s.uri}, {s.locator}" for c in _piece_claims(current, piece) for s in c.sources})
    revision = PieceRevision(
        steer=Steer(piece=piece, kind=reading.kind, instruction=sentence, claim_id=claim_id, at=now_iso(), author=author),
        before=before_piece, after=after_piece, claims_added=added, sources_added=sources_added,
        claims_dropped=dropped, verdict_moved_by=moved, note=note)

    rows = [["read as", "", "", ("more info" if reading.kind == "more_info" else "rewrite") + f" ({reading.path})"]]
    rows += [["added", i, "", now[i].text] for i in added]
    rows += [["dropped", i, was[i].text, ""] for i in dropped if i in was]
    rows += [["wording", i, b, a] for i, b, a in wording]
    rows += [["unverified", i, "", "quote not found"] for i in failed]
    rows.append(["verdict", ", ".join(moved), before_piece.verdict, after_piece.verdict])
    rows.append(["reason", ", ".join(after_piece.reason_claim_ids), before_piece.reason, after_piece.reason])
    if source_room != room_dir:
        rows.append(["source", "", room_name(room_dir), room_name(source_room)])
    if reading.number_text:
        rows.append(["number", claim_id or "", reading.number_text, "unchanged"])
    rows.append(["rebuilt by", "", "", rebuilt_by])
    changes = Panel(name=f"steer {n}: what changed", columns=["Change", "Claim", "Before", "After"], rows=rows)

    readout = after_r.model_copy(update={"revisions": current.revisions + [revision], "panels": after_r.panels + [changes]})
    write_readout(readout, room_dir)
    store = _save(readout, fund, room_dir, source_room) if save else StoreNote(saved=False, why="not asked to save")
    return SteerOutcome(readout=readout, revision=revision, changes=changes, reading=reading,
                        source_room=room_name(source_room), rebuilt_by=rebuilt_by, store=store)


def _llm():
    from clients.llm import read

    return read


def _save(readout: Readout, fund: str, room_dir: Path, source_room: Path) -> StoreNote:
    """Every revision is kept in the store as a new version. The source room holds every file the sources name."""
    try:
        from store import open_store

        results, _ = load_results(source_room)
        got = open_store().save(fund, room_name(room_dir), readout, source_room, results)
        return StoreNote(saved=True, version=got.version, new=got.new)
    except Exception as err:  # a refused id, a full disk: the steer stands, the response says why
        return StoreNote(saved=False, why=f"{type(err).__name__}: {err}")


# --------------------------------------------------------------------------- command line


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m steering", description="Steer one piece of a readout with one sentence.")
    parser.add_argument("room_dir", type=Path)
    parser.add_argument("piece", choices=PIECE_ORDER)
    parser.add_argument("sentence")
    parser.add_argument("--line", dest="claim_id", default=None, help="the claim id of the line typed on")
    parser.add_argument("--fund", default="demo")
    parser.add_argument("--author", default=None)
    args = parser.parse_args(argv)
    try:
        got = steer(args.room_dir, args.piece, args.sentence, args.claim_id, args.author, fund=args.fund)
    except (BadSteer, NoReadout) as err:
        print(str(err), file=sys.stderr)
        return 2
    added = {c.id: c.text for c in got.readout.claims if c.id in got.revision.claims_added}
    print(json.dumps({
        "room": got.readout.room, "piece": args.piece, "read_by": got.reading.path, "kind": got.reading.kind,
        "source_room": got.source_room, "rebuilt_by": got.rebuilt_by,
        "verdict": [got.revision.before.verdict, got.revision.after.verdict],
        "revision": got.revision.model_dump(include={"claims_added", "claims_dropped", "sources_added", "verdict_moved_by", "note"}),
        "added": added, "store": got.store.model_dump(), "revisions_kept": len(got.readout.revisions),
        "readout": str(out_dir(args.room_dir) / "readout.json"),
    }, indent=2))
    return 0
