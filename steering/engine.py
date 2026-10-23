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
import os
import sys
from pathlib import Path
from typing import Callable

from schema.check_quotes import check_claim
from schema.claim import PIECE_ORDER, Claim, Panel, Piece, PieceRevision, Readout, ScanResult, Steer
from scans.base import available, now_iso, out_dir, room_name, write_result
from scans.memo.merge import (READS_PANEL, SEED_SUFFIX, build_readout, full_room_of, load_results, reads_panel,
                               reads_room, write_readout)
from steering import verdicts
from steering.classify import model_available, read_sentence
from steering.models import Reading, SteerOutcome, StoreNote
from steering.rereads import exclude_from_recurring, possessive
from steering.reword import reword

MAX_SENTENCE = 500
MAX_AUTHOR = 80     # a name, written into the claim text, the note and every revision (review wave 2b, S3)
MAX_LINE_ID = 120
VERDICT_WORDS = {"looking_strong": "Looking strong", "looking_weak": "Looking weak", "mixed": "Mixed",
                 "not_enough_in_the_room": "Not enough in the room"}
PIECE_WORDS = {p: p.replace("_", " ") for p in PIECE_ORDER}


class BadSteer(ValueError):
    """The steer cannot run as asked: an empty sentence, an unknown piece or line."""


class NoReadout(LookupError):
    """No readout and no scan results for the room."""


class ScanFailed(RuntimeError):
    """A scan crashed while a steer reran it. Nothing was written: no result, no readout, no store version."""

    def __init__(self, scan: str, err: Exception):
        self.scan = scan
        super().__init__(f"{scan} failed: {type(err).__name__}: {err}")


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
        readout, _ = _rebuild(readout, Path(room_dir))
    return readout


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
    """Run every scan first and write their results only when all of them ran, so a crash leaves out/ as it was."""
    results = []
    for name in scans:
        try:
            results.append(importlib.import_module(f"scans.{name}.scan").run(room))
        except Exception as err:  # any scan's crash stops the steer, named (review wave 2b, O2)
            raise ScanFailed(name, err) from err
    for result in results:
        write_result(result, room)
    return results


def _merge_piece(before: Readout, fresh: Readout, piece: str, tag: str) -> tuple[Readout, list[str], list[str]]:
    """The before readout with the piece's claims, unverified claims and gaps taken from the fresh merge.
    Returns (readout, added ids, dropped ids). Matched claims keep their ids; new ones get the tag.
    The operator's scenario lines (scan "steering") are no check's output, so the rerun never drops them
    (review wave 2b, S6): they stay in the readout as they were."""
    old = [c for c in _piece_claims(before, piece) if c.scan != "steering"]
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


OVERVIEW = "overview"


def operator(author: str | None) -> str | None:
    """Who steered: the request's author, else the TRICORDER_OPERATOR setting, else nobody named."""
    return author or os.environ.get("TRICORDER_OPERATOR") or None


def _merge_all(before: Readout, fresh: Readout, tag: str | None) -> tuple[Readout, list[str], list[str]]:
    """The whole readout from the fresh merge (every piece), keeping the before ids of claims it states the
    same way, the operator's scenario lines, and every steer's record. Returns (readout, added, dropped).
    A fresh claim with no match gets the tag; with tag None (a rebuild) it keeps its own id unless that id is
    already taken."""
    kept_ids = {_key(c): c.id for c in before.claims if c.scan != "steering"}
    taken = {c.id for c in before.claims + before.unverified}
    ids: dict[str, str] = {}
    for c in fresh.claims + fresh.unverified:
        if _key(c) in kept_ids:
            ids[c.id] = kept_ids[_key(c)]
        elif tag is not None:
            ids[c.id] = f"{c.id}.{tag}"
        else:
            ids[c.id] = c.id if c.id not in taken else f"{c.id}.rebuilt"
        taken.add(ids[c.id])

    def remap(c: Claim) -> Claim:
        return c.model_copy(update={"id": ids.get(c.id, c.id),
                                    "conflicts_with": [ids.get(i, i) for i in c.conflicts_with],
                                    "corroborated_by": [ids.get(i, i) for i in c.corroborated_by]})

    claims = [remap(c) for c in fresh.claims]
    fresh_keys = {_key(c) for c in fresh.claims}
    added = [c.id for c in claims if c.id not in {b.id for b in before.claims}]
    dropped = [c.id for c in before.claims if c.scan != "steering" and _key(c) not in fresh_keys]
    scenarios = [c for c in before.claims if c.scan == "steering"]
    steer_panels = [p for p in before.panels if p.name.startswith("steer ") or p.name == READS_PANEL]
    merged = before.model_copy(update={
        "claims": claims + scenarios, "unverified": [remap(c) for c in fresh.unverified], "gaps": fresh.gaps,
        "asks": fresh.asks, "panels": fresh.panels + steer_panels, "scans_run": fresh.scans_run,
        "scans_missing": fresh.scans_missing})
    return merged, added, dropped


def carry(before: Readout, fresh: Readout, room: Path) -> Readout:
    """A rebuilt readout that keeps what the steers left (review wave 2b, S7): every revision, every "steer N"
    panel, the "reads room" switch and the operator's scenario lines. Claims the rebuild states the same way keep
    their ids, so every revision's ids still resolve, and a model rewording is put back on the line it changed.
    Verdicts and the scenario reasons are rebuilt as a steer rebuilds them."""
    reworded = {(r[2]): r[3] for p in before.panels if p.name.startswith("steer ") for r in p.rows
                if len(r) > 3 and r[0] == "wording"}
    if reworded:
        fresh = fresh.model_copy(update={"claims": [c.model_copy(update={"text": reworded[c.text]}) if c.text in reworded else c
                                                    for c in fresh.claims]})
    merged, _, _ = _merge_all(before, fresh, None)
    merged = merged.model_copy(update={"built_at": fresh.built_at, "synthetic_notice": fresh.synthetic_notice,
                                       "connecting": fresh.connecting, "scores": fresh.scores})
    out, _ = _rebuild(merged, room)
    return out


def scenario_reasons(readout: Readout) -> Readout:
    """A piece the operator steered with a scenario line reads that line as its reason: the rewrite redoes the
    piece, it does not only add to it. The check's line it replaces stays in the readout."""
    by_id = {c.id: c for c in readout.claims}
    pieces = {p.name: p for p in readout.pieces}
    for panel in readout.panels:
        if not panel.name.startswith("steer "):
            continue
        for row in panel.rows:
            if row[0] == "replaced" and row[3] in by_id:
                name = verdicts.piece_of(by_id[row[3]])
                if name in pieces:
                    pieces[name] = pieces[name].model_copy(update={"reason": by_id[row[3]].text, "reason_claim_ids": [row[3]]})
    return readout.model_copy(update={"pieces": [pieces[p.name] for p in readout.pieces]})


def _rebuild(readout: Readout, room: Path) -> tuple[Readout, str]:
    out, by = verdicts.rebuild(readout, room)
    return scenario_reasons(out), by


def claim_room(readout: Readout, claim_id: str, room_dir: Path) -> Path:
    """The room a claim's files open from: the full room for any line once the readout reads it."""
    return reads_room(readout, room_dir)


def steer(room_dir: str | Path, piece: str, sentence: str, claim_id: str | None = None, author: str | None = None,
          *, fund: str = "demo", llm: Callable | None = None, save: bool = True) -> SteerOutcome:
    room_dir = Path(room_dir)
    sentence = " ".join((sentence or "").split())
    author = operator(author)
    if not sentence:
        raise BadSteer("type one sentence")
    if len(sentence) > MAX_SENTENCE:
        raise BadSteer(f"one sentence, up to {MAX_SENTENCE} characters")
    if author is not None and len(author) > MAX_AUTHOR:
        raise BadSteer(f"an author name, up to {MAX_AUTHOR} characters")
    if claim_id is not None and len(claim_id) > MAX_LINE_ID:
        raise BadSteer(f"a line id, up to {MAX_LINE_ID} characters")
    if piece not in PIECE_ORDER and piece != OVERVIEW:
        raise BadSteer(f"no piece {piece!r}; pieces are {', '.join(PIECE_ORDER)}, or {OVERVIEW}")

    current = load_readout(room_dir)
    if claim_id is not None:
        line = next((c for c in current.claims + current.unverified if c.id == claim_id), None)
        if line is None:
            raise BadSteer(f"no line {claim_id!r} in the readout")
        if verdicts.piece_of(line) != piece:
            raise BadSteer(f"line {claim_id!r} is in {verdicts.piece_of(line)}, not {piece}")
    if not current.pieces:
        current, _ = _rebuild(current, room_dir)
    n = len(current.revisions) + 1
    tag = f"steer{n}"

    reading = read_sentence(sentence, llm=llm)
    if piece == OVERVIEW and not (reading.kind == "more_info"):
        raise BadSteer("On the overview, a steer reads more of the room, such as \"read the full room\". "
                       "A rewrite goes on the piece or the line it is about.")
    reading_room = reads_room(current, room_dir)
    source_room = reading_room
    notes: list[str] = []
    wording: list[tuple[str, str, str]] = []
    replaced: list[tuple[str, str]] = []  # (check line id, scenario line id)
    working, added, dropped = current, [], []
    headline = ""

    if reading.kind == "more_info":
        if reading.source == "full_room":
            full = full_room_of(room_dir)
            if full is None:
                headline = "Nothing new read: this room is already the full room."
                notes.append("This room is already the full room, or has no second tier beside it, so nothing new was read.")
            elif reading_room == full:
                headline = f"Nothing new read: every piece already reads {room_name(full)}, the full room."
                notes.append("An earlier steer switched this readout to the full room, so nothing new was read.")
            else:
                source_room = full
                _rerun(sorted(available()), full)
                working, added, dropped = _merge_all(current, build_readout(full, keep_steers=False), tag)
        else:
            headline = "Not fetched: Tricorder does not fetch outside sources on a steer yet."
            notes.append(f"You asked for {reading.source_named}. Ask the founder for it, or add it to the room.")
    else:
        if reading.number_text is None:
            _rerun(_scans_feeding(current, piece), reading_room)
            working, added, dropped = _merge_piece(current, build_readout(reading_room, keep_steers=False), piece, tag)
        if reading.term:
            piece_claims = _piece_claims(working, piece)
            if claim_id is not None:
                line = [c for c in piece_claims if c.id == claim_id and c.value and c.value.label == "arr"]
                piece_claims = line or piece_claims
            counter = iter(range(1, 1000))
            got = exclude_from_recurring(reading.term, piece_claims, reading_room, lambda: f"{tag}-{next(counter):03d}", author)
            same = lambda c: (c.text, c.value.model_dump_json() if c.value else None)  # noqa: E731
            held = {same(c): c.id for c in working.claims if c.scan == "steering"}
            repeats = [held[same(c)] for c in got["claims"] if same(c) in held]
            if repeats:  # the same scenario line an earlier steer added: keep that one, add no copy
                fresh_lines = [c for c in got["claims"] if same(c) not in held]
                got = {**got, "claims": fresh_lines,
                       "replaces": {k: v for k, v in got["replaces"].items() if k in {c.id for c in fresh_lines}},
                       "notes": [f"the scenario line is already in the piece ({', '.join(repeats)}), so no copy was added."] + got["notes"]}
            notes += got["notes"]
            working = working.model_copy(update={"claims": working.claims + got["claims"]})
            added += [c.id for c in got["claims"]]
            replaced = [(old, new) for new, old in got["replaces"].items()]
            if got["claims"]:
                headline = "Added a scenario line." if len(got["claims"]) == 1 else f"Added {len(got['claims'])} scenario lines."
                figures = "; ".join(f"${got['check_figure'][c.id]:,.0f}" for c in got["claims"])
                notes.insert(0, f"Your scenario line is new. The original check still shows {figures}.")
            else:
                headline = "Nothing changed: " + (got["notes"][0] if got["notes"] else "no line to reread.")
        elif reading.number_text is not None:
            target = next((c for c in current.claims if c.id == claim_id), None) if claim_id else None
            named = _label_named(sentence)
            target = target or next((c for c in _piece_claims(current, piece) if c.value and c.value.label == named), None) \
                or next((c for c in _piece_claims(current, piece) if c.id in next(p for p in current.pieces if p.name == piece).reason_claim_ids), None) \
                or next((c for c in _piece_claims(current, piece) if c.value is not None), None)
            headline = "Refused: computed numbers do not change on request."
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
            headline = f"Reworded {len(wording)} line{'s' if len(wording) != 1 else ''}." if wording else "Nothing changed: no line was reworded."
        else:
            headline = "Nothing changed: Tricorder could not tell what to change from this sentence."
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
        replaced = [(o, nw) for o, nw in replaced if nw not in failed]

    # The record of what replaced what goes in before the rebuild, so the scenario reason applies.
    rows = [["replaced", old, next(c.text for c in current.claims + working.claims if c.id == old), new] for old, new in replaced]
    working = working.model_copy(update={"panels": working.panels + [Panel(name=f"steer {n}: what changed", columns=["Change", "Claim", "Before", "After"], rows=rows)]})
    after_r, rebuilt_by = _rebuild(working, source_room)
    working_panels = [p for p in after_r.panels if p.name != f"steer {n}: what changed"]

    before_pieces = {p.name: p for p in current.pieces}
    after_pieces = {p.name: p for p in after_r.pieces}
    moved_pieces = [p for p in PIECE_ORDER if before_pieces[p].verdict != after_pieces[p].verdict]
    if piece == OVERVIEW:
        piece = moved_pieces[0] if moved_pieces else next((verdicts.piece_of(c) for c in after_r.claims if c.id in added), PIECE_ORDER[0])
        typed_on = OVERVIEW
    else:
        typed_on = piece
    before_piece, after_piece = before_pieces[piece], after_pieces[piece]
    moved = _moved_by(current, after_r, before_piece, after_piece, added, dropped)
    now = {c.id: c for c in after_r.claims}
    was = {c.id: c for c in current.claims}

    new_sources = sorted({s.uri for i in added for s in now[i].sources} - {s.uri for c in current.claims for s in c.sources})
    whose = possessive(author)
    if reading.kind == "more_info" and source_room != reading_room:
        files = f"Read {len(new_sources)} new file{'s' if len(new_sources) != 1 else ''}"
        movers = [f"{PIECE_WORDS[p]} moved to {VERDICT_WORDS[after_pieces[p].verdict]}" for p in moved_pieces]
        headline = f"{files}; {', '.join(movers) if movers else 'no verdict moved'}."
        head = (f'More info on {whose} instruction: "{sentence}". Every piece now reads {room_name(source_room)}, '
                f"the full room, instead of {room_name(room_dir)}. {len(added)} new claim{'s' if len(added) != 1 else ''}, marked new"
                + (f" ({', '.join(new_sources)})." if new_sources else "."))
    elif reading.kind == "more_info":
        head = f'More info on {whose} instruction: "{sentence}".'
    elif reading.number_text is not None and not reading.term:
        head = f'{whose[0].upper() + whose[1:]} instruction: "{sentence}".'
    else:
        head = f'Rewritten on {whose} instruction: "{sentence}".'
    if before_piece.verdict == after_piece.verdict:
        verdict = "Verdict unchanged."
    else:
        movers = "; ".join(f'"{now[i].text.rstrip(".")}"' for i in moved if i in now) or "the rule"
        verdict = f"Verdict: {VERDICT_WORDS[before_piece.verdict]} to {VERDICT_WORDS[after_piece.verdict]}, moved by {movers}."
    if before_piece.reason != after_piece.reason:
        verdict += " The reason line changed."
    numbers = "" if reading.number_text and not reading.term else " The checks' numbers are unchanged."
    note = " ".join(filter(None, [headline, head, verdict + numbers, " ".join(notes), _path_words(reading), _rebuilt_words(rebuilt_by)]))

    sources_added = sorted({f"{s.uri}, {s.locator}" for i in added for s in now[i].sources}
                           - {f"{s.uri}, {s.locator}" for c in current.claims for s in c.sources})
    revision = PieceRevision(
        steer=Steer(piece=piece, kind=reading.kind, instruction=sentence, claim_id=claim_id, at=now_iso(), author=author),
        before=before_piece, after=after_piece, claims_added=added, sources_added=sources_added,
        claims_dropped=dropped, verdict_moved_by=moved, note=note)

    rows = [["headline", "", "", headline], ["typed on", claim_id or "", "", typed_on],
            ["read as", "", "", ("more info" if reading.kind == "more_info" else "rewrite") + f" ({reading.path})"]]
    rows += [["added", i, "", now[i].text] for i in added]
    rows += [["dropped", i, was[i].text, ""] for i in dropped if i in was]
    rows += [["replaced", old, was.get(old, now.get(old)).text, new] for old, new in replaced]
    rows += [["wording", i, b, a] for i, b, a in wording]
    rows += [["unverified", i, "", "quote not found"] for i in failed]
    rows.append(["verdict", ", ".join(moved), before_piece.verdict, after_piece.verdict])
    rows += [["piece moved", p, before_pieces[p].verdict, after_pieces[p].verdict] for p in moved_pieces if p != piece]
    rows.append(["reason", ", ".join(after_piece.reason_claim_ids), before_piece.reason, after_piece.reason])
    if source_room != reading_room:
        rows.append(["source", "", room_name(room_dir), room_name(source_room)])
    if reading.number_text and not reading.term:
        rows.append(["number", claim_id or "", reading.number_text, "unchanged"])
    rows.append(["rebuilt by", "", "", rebuilt_by])
    changes = Panel(name=f"steer {n}: what changed", columns=["Change", "Claim", "Before", "After"], rows=rows)

    marker = [reads_panel(room_name(source_room), n)] if source_room != reading_room else []
    working_panels = [p for p in working_panels if not (marker and p.name == READS_PANEL)]
    readout = after_r.model_copy(update={"revisions": current.revisions + [revision], "panels": working_panels + marker + [changes]})
    write_readout(readout, room_dir)
    store = _save(readout, fund, room_dir, source_room) if save else StoreNote(saved=False, why="not asked to save")
    return SteerOutcome(readout=readout, revision=revision, changes=changes, reading=reading,
                        source_room=room_name(source_room), rebuilt_by=rebuilt_by, store=store)


def _llm():
    from clients.llm import read

    return read


def _save(readout: Readout, fund: str, room_dir: Path, source_room: Path) -> StoreNote:
    """Every revision is kept in the store as a new version. The results kept are the readout's own
    room's; files resolve in the source room, which holds every file the sources name (a seed drop's
    files are copies of its full room's), so a more-info steer stores the new files its lines cite and
    nothing else the full room holds."""
    try:
        from store import open_store

        results, _ = load_results(room_dir)
        got = open_store().save(fund, room_name(room_dir), readout, source_room, results)
        return StoreNote(saved=True, version=got.version, new=got.new)
    except Exception as err:  # a refused id, a full disk: the steer stands, the response says why
        return StoreNote(saved=False, why=f"{type(err).__name__}: {err}")


# --------------------------------------------------------------------------- command line


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m steering", description="Steer one piece of a readout with one sentence.")
    parser.add_argument("room_dir", type=Path)
    parser.add_argument("piece", choices=[*PIECE_ORDER, "overview"])
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
    except ScanFailed as err:
        print(str(err), file=sys.stderr)
        return 1
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
