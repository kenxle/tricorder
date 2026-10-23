"""Checklist coverage: a merge step (FRAMEWORKS.md, "Checklist coverage").

    def apply(readout: Readout, room_dir: Path) -> Readout

Runs after "pieces" and "top_flags" and before "asks" (scans/memo/merge.py,
STEPS). For the company's stage it gives every checklist item one status,
writes the ask lines for what is missing, and writes three Panels the page
reads. A pure script: no model call, no network. Design and requirements:
docs/features/20261022.13_checklist_coverage/ (03_prd.md, 04_architecture.md).

What it writes into the readout:

- Panel "checklist coverage": one row per checklist item.
- Panel "checklist coverage counts": the stage, its source, the label, the counts.
- Panel "checklist ask lines": per ask line, the checklist ids it covers, where
  it came from, when to ask, and its top-five rank.
- AskItems appended to readout.asks, with checklist_id set. A gap that names a
  checklist item gets its line here, in the gap's own words; the ask-list step
  skips such gaps through checklist.gap_is_asked().
- Gaps from the cap table's instrument rows (entry 1.10, row C82), with piece
  "the_pitch_itself".
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from schema.claim import PIECE_ORDER, AskItem, Gap, Panel, Readout
from scans.base import find, out_dir
from scans.memo import checklist as cl

COVERAGE_PANEL = "checklist coverage"
COUNTS_PANEL = "checklist coverage counts"
ASKS_PANEL = "checklist ask lines"
STATUSES = ("checked", "found", "missing", "not_checked", "not_expected")
STAGE_LINE = re.compile(r"^\s*(Pre-seed|Preseed|Seed|Series [A-Z])\s*\|", re.I | re.M)
STAGE_WORDS = {"pre-seed": "pre_seed", "preseed": "pre_seed", "seed": "seed", "series a": "series_a"}


# Stage -------------------------------------------------------------------------


def read_deck_stage(room_dir: Path):
    """(stage, word, source text) from the deck's cover or round slide, else claims.json."""
    from schema.readers import pdf_pages

    for deck in find(room_dir, "deck"):
        try:
            pages = pdf_pages(deck)
        except Exception:
            continue
        for n, text in enumerate(pages, start=1):
            m = STAGE_LINE.search(text)
            if m:
                line = text[m.start():].splitlines()[0].strip()
                word = re.sub(r"\s+", " ", m.group(1)).strip()
                return STAGE_WORDS.get(word.lower()), word, f"{deck.relative_to(room_dir)}, slide {n}: {line}"
    for claims in find(room_dir, "deck_claims"):
        try:
            data = json.loads(claims.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for c in data.get("claims", []):
            m = re.match(r"(Pre-seed|Seed|Series [A-Z]) raise", str(c.get("label", "")), re.I)
            if m:
                return STAGE_WORDS.get(m.group(1).lower()), m.group(1), f"{claims.relative_to(room_dir)}, label: {c['label']}"
    return None, None, None


def read_stage(room_dir: Path) -> dict:
    deck_stage, word, source = read_deck_stage(room_dir)
    out = {"stage": deck_stage, "set_by": "deck" if deck_stage or word else None, "deck_stage": deck_stage,
           "word": word, "source": source}
    op = out_dir(room_dir) / "operator.json"
    if op.exists():
        try:
            chosen = json.loads(op.read_text(encoding="utf-8")).get("stage")
        except ValueError:
            chosen = None
        if chosen:
            out.update(stage=chosen if chosen in cl.STAGES else None, set_by="operator", word=chosen)
    return out


# Statuses ----------------------------------------------------------------------


def _claims_for(row, claims, found_files):
    names = cl.ROW_CHECKS.get(row.id) or set().union(*(cl.ENTRY_CHECKS.get(e, set()) for e in row.entries))
    hits = [c for c in claims if cl.check_names(c.check.name) in names]
    if row.kind == "document":
        hits = [c for c in hits if any(s.uri in found_files for s in c.sources)]
    return [c.id for c in hits]


def _statuses(rows, stage, found, claims):
    by_id = {r.id: r for r in rows}
    recs = {}
    for r in rows:
        level = r.stage[stage]
        rec = {"row": r, "level": level, "status": None, "detail": "", "covers_by": None}
        if r.kind == "document":
            files, note = found[r.id]
            ids = _claims_for(r, claims, files) if files else []
            if files:
                rec["status"] = "checked" if ids else "found"
                rec["detail"] = "In the room: " + ", ".join(files[:3]) + (", ..." if len(files) > 3 else "") \
                    + (f" ({note})" if note else "") + (f". Read by {', '.join(ids)}." if ids else "")
            elif cl.expected(level):
                rec["status"], rec["detail"] = "missing", "Not in the room."
            else:
                rec["status"], rec["detail"] = "not_expected", f"Not expected at this stage ({level})."
        elif r.kind == "check":
            inputs = cl.CHECK_INPUTS.get(r.id, [])
            missing = [i for i in inputs if not found.get(i, ([], None))[0]]
            later = [i for i in missing if not cl.expected(by_id[i].stage[stage])]
            ids = _claims_for(r, claims, [])
            rec["missing_inputs"] = missing
            if not cl.expected(level):
                rec["status"], rec["detail"] = "not_expected", f"Not expected at this stage ({level})."
            elif ids:
                # A check can run on a fallback file (1.12 kind a reads the model's ARR_Build when the
                # customer file is absent). It is checked; a missing file is still asked for.
                rec["status"], rec["detail"] = "checked", f"Checked by {', '.join(ids)} ({r.checked_by})."
                asked = [i for i in missing if i not in later]
                if asked:
                    rec["detail"] += f" {', '.join(asked)} would let it run on the fuller file."
                rec["missing_inputs"] = asked
            elif missing and later:
                rec["status"] = "not_checked"
                rec["detail"] = f"Cannot run: needs {', '.join(later)}, not expected at this stage."
            elif missing:
                rec["status"] = "missing"
                rec["detail"] = f"Cannot run: needs {', '.join(missing)}, not in the room."
            elif r.entries == ("1.11",):
                rec["status"], rec["detail"] = "found", "Its files are in the room; entry 1.11 checks only that they are there."
            elif r.check_exists:
                rec["status"], rec["detail"] = "not_checked", f"No claim from {r.checked_by} yet."
            else:
                rec["status"], rec["detail"] = "not_checked", "No check is built for this item yet."
        elif r.kind == "outside":
            ids = _claims_for(r, claims, [])
            if not cl.expected(level):
                rec["status"], rec["detail"] = "not_expected", f"Not expected at this stage ({level})."
            elif ids:
                rec["status"], rec["detail"] = "checked", f"Checked by {', '.join(ids)}."
            else:
                rec["status"] = "not_checked"
                rec["detail"] = (f"No claim from {r.checked_by} yet. Tricorder reads this itself; it is never asked of the founder."
                                 if r.check_exists else "No check is built for this item yet. It is never asked of the founder.")
        else:  # ask the founder
            if cl.expected(level):
                rec["status"], rec["detail"] = "missing", "Only the founder can give this."
            else:
                rec["status"], rec["detail"] = "not_expected", f"Not expected at this stage ({level})."
        recs[r.id] = rec
    return recs


# The cap table's instruments (entry 1.10, row C82) ----------------------------


def instrument_gaps(room_dir: Path, files: list[str]) -> list[Gap]:
    from schema.readers import xlsx_sheet, xlsx_sheet_names

    gaps = []
    for path in find(room_dir, "cap_table"):
        rel = str(path.relative_to(room_dir))
        try:
            sheet = xlsx_sheet_names(path)[0]
            rows = xlsx_sheet(path, sheet)
        except Exception:
            continue
        in_safe = False
        for n, row in enumerate(rows, start=1):
            first = row[0] if row else None
            if first == "SAFE conversion":
                in_safe = True
                continue
            if not isinstance(first, str):
                continue
            if in_safe and first == "Investor":
                continue
            if in_safe and first.startswith("Total"):
                in_safe = False
                continue
            if in_safe:
                key = re.sub(r"\W+", "_", first.lower())[:8]
                if not any("safe" in f.lower() and key in f.lower() for f in files):
                    gaps.append(Gap(what=f"Not in the room: the signed SAFE for {first}", why="file missing",
                                    would_need=f"the signed SAFE for {first} ({rel}, {sheet}!A{n})",
                                    piece="the_pitch_itself"))
            elif first.startswith("Options granted"):
                if not any(re.search(cl.DOC_PATTERNS["C78"], f.lower()) for f in files):
                    gaps.append(Gap(what=f"Not in the room: the option grant records behind '{first}'",
                                    why="file missing",
                                    would_need=f"the option grant records for every holder ({rel}, {sheet}!A{n})",
                                    piece="the_pitch_itself"))
    return gaps


# Ask lines ---------------------------------------------------------------------


def _line(what, why, piece, from_kind, checklist_id, covers, if_you_have_it, stage):
    late = checklist_id in cl.AFTER_TERM_SHEET
    if late and not why.startswith("After the term sheet."):
        why = "After the term sheet. " + why
    return {"item": AskItem(what=what, why=why, piece=piece, from_kind=from_kind, checklist_id=checklist_id,
                            if_you_have_it=if_you_have_it),
            "covers": list(covers), "ask_stage": "after_term_sheet" if late else "before_second_meeting"}


LOCATION = re.compile(r"\s*\(([^()]*(?:\.xlsx|\.csv|\.pdf|\.md|![A-Z]+\d)[^()]*)\)")


def _founder_text(would_need: str):
    """Ask text the founder reads: no file path or cell reference. Returns (text, location)."""
    m = LOCATION.search(would_need)
    if not m:
        return would_need, None
    return (would_need[:m.start()] + would_need[m.end():]).strip(), m.group(1)


def _ask_lines(rows, recs, gaps, stage, has_flag):
    by_id = {r.id: r for r in rows}
    level = lambda i: by_id[i].stage[stage]  # noqa: E731
    lines, claimed, held = [], {}, []

    # Gaps that name a checklist item: their own words win (CC-R15).
    safe_gaps, by_gap_what = [], {}
    for g in gaps:
        items = cl.items_for_gap(g)
        if not items:
            continue
        if not any(cl.expected(level(i)) for i in items):
            held.append(g.what)
            continue
        if items == ["C75"] and g.what.startswith("Not in the room: the signed SAFE for"):
            safe_gaps.append(g)
            continue
        if g.what in by_gap_what:  # two scans missing the same document ask once (CC-R14)
            line = lines[by_gap_what[g.what]]
            line["covers"] += [i for i in items if i not in line["covers"]]
            continue
        piece = g.piece or by_id[items[0]].readout_piece
        what, where = _founder_text(g.would_need)
        line = _line(what, g.what + (f" ({where})" if where else ""), piece, "gap", items[0], items,
                     all(level(i) != "yes" for i in items if cl.expected(level(i))), stage)
        lines.append(line)
        by_gap_what[g.what] = len(lines) - 1
        for i in items:
            claimed.setdefault(i, len(lines) - 1)
    if safe_gaps:  # Ken's default: one line for all SAFEs, naming each.
        holders = [g.what.replace("Not in the room: the signed SAFE for ", "") for g in safe_gaps]
        lines.append(_line("Please send the signed SAFE, with any side letter, for each of: " + "; ".join(holders) + ".",
                           f"Not in the room: the signed SAFEs for {len(holders)} holders on the cap table.",
                           "the_pitch_itself", "gap", "C75", ["C75"], level("C75") != "yes", stage))
        claimed.setdefault("C75", len(lines) - 1)

    # Checklist items: missing documents and asks, with missing checks folded into their files.
    want = {}
    for cid, rec in recs.items():
        if rec["status"] != "missing":
            continue
        r = rec["row"]
        if r.kind in ("document", "ask"):
            if cid == "C71" and has_flag:
                rec["detail"] = "Asked through one walk-through line per flag, written by the ask-list step."
                continue
            want.setdefault(cl.SAME_REQUEST.get(cid, cid), []).append(cid)
        elif r.kind == "check":
            for inp in rec.get("missing_inputs", []):
                want.setdefault(inp, []).append(cid)
    for cid, rec in recs.items():  # checked rows that a fuller file would let run more completely
        if rec["status"] == "checked" and rec["row"].kind == "check":
            for inp in rec.get("missing_inputs", []):
                if recs.get(inp, {}).get("status") == "missing":
                    want.setdefault(inp, []).append(cid)

    guides = cl.guide_asks()
    for target in sorted(want, key=lambda c: int(c[1:])):
        covered = sorted(set(want[target]), key=lambda c: int(c[1:]))
        if target in claimed:
            line = lines[claimed[target]]
            line["covers"] += [c for c in covered if c not in line["covers"]]
            continue
        row = by_id[target]
        guide = guides.get(target)
        what = cl.ASK_TEXT.get(target) or (guide[1] if guide and guide[1] else f"Please send: {row.item}.")
        checks = [c for c in covered if c != target]
        why = "Only the founder can answer this." if row.kind == "ask" else f"Not in the room: {row.item}."
        if checks:
            why += " Also needed for " + ", ".join(checks) + "."
        yes = any(level(c) == "yes" for c in covered)
        covered = [target] + [c for c in covered if c != target] if target in covered else covered
        lines.append(_line(what, why, row.readout_piece, "checklist", target, covered, not yes, stage))

    # One line per request: rows whose guide gives the same words (the AI governance rows share
    # one guide) become one line covering all of them (CC-R14).
    merged, seen = [], {}
    for l in lines:
        key = l["item"].what.strip().lower()
        if key in seen:
            keep = seen[key]
            keep["covers"] += [c for c in l["covers"] if c not in keep["covers"]]
            if not l["item"].if_you_have_it:
                keep["item"].if_you_have_it = False
            continue
        seen[key] = l
        merged.append(l)
    lines = merged

    # Order: pieces in the overview's order; gap lines, then checklist lines.
    lines.sort(key=lambda l: (PIECE_ORDER.index(l["item"].piece), 0 if l["item"].from_kind == "gap" else 1))
    # Ken's default: the five most blocking required lines are pinned at the top of the page.
    ranked = sorted((l for l in lines if not l["item"].if_you_have_it and l["ask_stage"] == "before_second_meeting"),
                    key=lambda l: (-len(l["covers"]), PIECE_ORDER.index(l["item"].piece), l["item"].checklist_id or ""))
    for n, l in enumerate(ranked[:5], start=1):
        l["top"] = n
    return lines, held


# The step ----------------------------------------------------------------------


def apply(readout: Readout, room_dir: Path) -> Readout:
    room_dir = Path(room_dir)
    rows = cl.load()
    st = read_stage(room_dir)
    readout.panels = [p for p in readout.panels if p.name not in (COVERAGE_PANEL, COUNTS_PANEL, ASKS_PANEL)]
    counts = [["stage", st["stage"] or ""], ["stage_set_by", st["set_by"] or ""], ["deck_stage", st["deck_stage"] or ""],
              ["stage_source", st["source"] or ""]]
    stage = st["stage"]
    if stage not in cl.STAGES:
        if st["word"]:
            reason = f"The stage '{st['word']}' is not pre-seed, seed or Series A. The operator picks the stage."
        else:
            reason = "No round slide states a stage, and the operator has not set one. The operator picks the stage."
        counts += [["label", "stage_unknown"], ["label_reason", reason]]
        readout.panels.append(Panel(name=COUNTS_PANEL, columns=["key", "value"], rows=counts))
        return readout

    files = cl.room_files(room_dir)
    found = {r.id: cl.match_document_with_note(r, files, room_dir) for r in rows if r.kind == "document"}
    recs = _statuses(rows, stage, found, readout.claims)

    known = {g.what for g in readout.gaps}
    readout.gaps += [g for g in instrument_gaps(room_dir, files) if g.what not in known]
    has_flag = any(c.severity == "flag" for c in readout.claims)
    lines, held = _ask_lines(rows, recs, readout.gaps, stage, has_flag)

    existing = {a.what.strip().lower() for a in readout.asks}
    kept = [l for l in lines if l["item"].what.strip().lower() not in existing]
    offset = len(readout.asks)
    readout.asks += [l["item"] for l in kept]
    line_of = {}  # position in readout.asks, counting from 1
    for n, l in enumerate(kept, start=offset + 1):
        for c in l["covers"]:
            line_of.setdefault(c, n)

    cov_rows = [[r.id, r.item, r.readout_piece, r.kind, recs[r.id]["level"], recs[r.id]["status"],
                 recs[r.id]["detail"], str(line_of.get(r.id, ""))] for r in rows]
    status_counts = {s: sum(1 for r in recs.values() if r["status"] == s) for s in STATUSES}
    counts += [["label", "built"],
               ["label_reason", f"Stage {stage}, set by the {st['set_by']}." + (f" Source: {st['source']}." if st["source"] else "")]]
    counts += [[s, str(n)] for s, n in status_counts.items()]
    counts += [["items", str(len(rows))],
               ["expected", str(sum(1 for r in recs.values() if cl.expected(r["level"])))],
               ["ask_lines", str(len(kept))],
               ["ask_lines_if_you_have_it", str(sum(1 for l in kept if l["item"].if_you_have_it))],
               ["ask_lines_after_term_sheet", str(sum(1 for l in kept if l["ask_stage"] == "after_term_sheet"))],
               ["gap_asks_held_back", str(len(held))]]
    readout.panels += [
        Panel(name=COVERAGE_PANEL, columns=["id", "item", "piece", "kind", "expected", "status", "detail", "ask_line"],
              rows=cov_rows),
        Panel(name=COUNTS_PANEL, columns=["key", "value"], rows=counts),
        Panel(name=ASKS_PANEL, columns=["what", "checklist_ids", "from_kind", "ask_stage", "top_five"],
              rows=[[l["item"].what, ", ".join(l["covers"]), l["item"].from_kind, l["ask_stage"], str(l.get("top", ""))]
                    for l in kept]),
    ]
    return readout
