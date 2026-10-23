"""Pull every figure out of the deck and the pitch video, by script.

Each figure becomes a Statement: where it is (slide and line, script line, or
transcript segment and seconds), the exact quoted span, the words around it,
and the kind `kinds.classify` gives it. Nothing here compares anything.

Sources, in the order FRAMEWORKS entry 1.1 reads them:
- every content slide of `pitch_deck.pdf`, read through `schema.readers.pdf_pages`;
- the claims page (the appendix slide that lists each metric with its slide);
- `claims.json`, the claims page as data, used when the PDF has no readable text;
- `pitch_video.transcript.json` beside the video (whisper segments), or, until
  the video is recorded, `pitch_video_script.md`, cited by line and labelled as
  the script, never as the video.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from scans.base import find
from scans.claims.kinds import KINDS, classify_with_entities
from scans.claims.numbers import Mention, mentions

FOOTER = re.compile(r"^Synthetic data room for ")
APPENDIX_HEADER = re.compile(r"^(Claim|Metric) Value Slide$")
BEAT = re.compile(r"^\*\*(\d+):(\d{2})\s+(.*?)\*\*$")
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9$])")


@dataclass
class Statement:
    origin: str              # deck, appendix, claims_json, script, transcript, model
    uri: str                 # path inside the room
    locator: str             # "slide 3", "line 15", "seg 4"
    quote: str               # exact span, as the reader returns it
    sentence: str            # the words the kind was read from
    mention: Mention
    kind: str
    slide: int | None = None
    line: int | None = None
    seg: int | None = None
    start_s: float | None = None
    end_s: float | None = None
    beat: str | None = None          # the script's "0:35" heading above the line
    cited_slide: int | None = None   # appendix rows: the slide each row names
    appendix_label: str | None = None
    repeats: list["Statement"] = field(default_factory=list)  # the same fact elsewhere in the deck

    @property
    def spoken(self) -> bool:
        return self.origin in ("script", "transcript")

    @property
    def where(self) -> str:
        if self.origin == "script":
            return f"script line {self.line}" + (f" (beat {self.beat})" if self.beat else "")
        if self.origin == "transcript":
            return f"video {self.start_s:.0f}s to {self.end_s:.0f}s (segment {self.seg})"
        if self.origin == "appendix":
            return f"slide {self.slide}, claims page row" + (f" (cites slide {self.cited_slide})" if self.cited_slide else "")
        if self.origin == "claims_json":
            return f"claims.json, {self.locator}"
        return f"slide {self.slide}"


def _rel(path: Path, room: Path) -> str:
    return str(path.relative_to(room))


def _roles(text: str, ms: list[Mention]) -> list[str | None]:
    """'14 of the 15': part and whole. 'from 17 to 41': from and to."""
    roles: list[str | None] = [None] * len(ms)
    for i in range(len(ms) - 1):
        between = text[ms[i].end:ms[i + 1].start]
        if re.fullmatch(r"\s+of\s+(the\s+)?", between):
            roles[i], roles[i + 1] = "part", "whole"
        elif re.fullmatch(r"\s+to\s+", between) and re.search(r"\bfrom\s+$", text[:ms[i].start]):
            roles[i], roles[i + 1] = "from", "to"
    return roles


def _local(text: str, ms: list[Mention], i: int) -> str:
    start = ms[i - 1].end if i > 0 else 0
    end = ms[i + 1].start if i + 1 < len(ms) else len(text)
    return text[start:end]


def _kind(m: Mention, local: str, sentence: str, fallbacks: tuple[str, ...], role: str | None) -> str:
    for text in (sentence,) + fallbacks:
        kind = classify_with_entities(m, local.lower(), text.lower(), text, role)
        if kind != "other":
            return kind
    return "other"


def _usable(m: Mention, kind: str) -> bool:
    return m.kind_hint in KINDS[kind].expects


def _near(a: float | None, b: float | None, precision: float) -> bool:
    if a is None or b is None:
        return False
    return abs(a - b) <= max(precision / 2, 1e-9) or abs(a - b) <= 0.005 * max(abs(a), abs(b))


# Deck -----------------------------------------------------------------------


def _pages(deck: Path) -> list[str] | None:
    from schema.readers import pdf_pages

    try:
        pages = pdf_pages(deck)
    except Exception:  # an unreadable PDF falls back to claims.json
        return None
    return pages if any(p.strip() for p in pages) else None


def as_of(pages: list[str]) -> str | None:
    """The deck's own data date, "2026-09-30", from 'Data as of 2026-09-30'."""
    for text in pages:
        m = re.search(r"as of (\d{4}-\d{2}-\d{2})", text)
        if m:
            return m.group(1)
    return None


def _good_row(c) -> bool:
    if not (isinstance(c, dict) and isinstance(c.get("label"), str) and isinstance(c.get("value"), str)):
        return False
    try:
        int(c.get("slide") or 0)
    except (TypeError, ValueError):
        return False
    return True


def claims_json_rows(room: Path) -> tuple[list[dict], int]:
    """(usable rows, rows skipped). A row needs a text label, a text value and a slide
    number; anything else in a founder's file is skipped and counted, never a crash."""
    for path in find(room, "deck_claims"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return [], 1
        rows = data.get("claims", []) if isinstance(data, dict) else []
        rows = rows if isinstance(rows, list) else []
        good = [c for c in rows if _good_row(c)]
        return good, len(rows) - len(good)
    return [], 0


def _claims_json(room: Path) -> list[dict]:
    return claims_json_rows(room)[0]


def _split_row(row: str, known: list[dict]) -> tuple[str, str, int | None] | None:
    """'Runway 29 months 10' -> ('Runway', '29 months', 10). claims.json gives the
    exact split when it exists; otherwise the value starts at the first figure that is
    not part of the label ('September 2026', 'next 12 months')."""
    for c in known:
        candidate = f"{c['label']} {c['value']} {c['slide']}"
        if row.strip() == candidate:
            return c["label"], c["value"], int(c["slide"])
    m = re.match(r"^(.*\S)\s+(\d+)$", row.strip())
    if not m:
        return None
    body, slide = m.group(1), int(m.group(2))
    for mention in mentions(body):
        if mention.qualifier or (mention.kind_hint == "month" and re.search(r",\s*$", body[:mention.start])):
            continue
        if mention.kind_hint == "year":
            continue
        start = mention.start
        hedge = re.search(r"(under|over|about|above|below)\s+$", body[:start])
        if hedge:
            start = hedge.start()
        return body[:start].strip(), body[start:].strip(), slide
    return None


def _appendix(pages: list[str]) -> int | None:
    for n, text in enumerate(pages, start=1):
        if any(APPENDIX_HEADER.match(line.strip()) for line in text.splitlines()):
            return n
    return None


def _joined_lines(lines: list[str]) -> list[tuple[str, list[int]]]:
    """Lines a wrap split in two are joined back: a line with no closing
    punctuation followed by one that starts in lower case."""
    out: list[tuple[str, list[int]]] = []
    for i, line in enumerate(lines):
        if out and line[:1].islower() and not re.search(r"[.!?:]$", out[-1][0]):
            out[-1] = (out[-1][0] + "\n" + line, out[-1][1] + [i])
        else:
            out.append((line, [i]))
    return out


def deck_statements(room: Path) -> tuple[list[Statement], list[str], str | None, bool]:
    """(statements, notes, as_of, read_from_pdf)."""
    decks = find(room, "deck")
    known = _claims_json(room)
    if not decks:
        return [], ["no deck"], None, False
    deck = decks[0]
    uri = _rel(deck, room)
    pages = _pages(deck)
    if pages is None:
        return claims_json_statements(room, known), ["the deck PDF has no readable text; read claims.json"], None, False

    out: list[Statement] = []
    appendix = _appendix(pages)
    legend: list[tuple[int, Mention, str]] = []  # (cited slide, value mention, row label)

    if appendix:
        lines = [l for l in pages[appendix - 1].splitlines() if l.strip()]
        start = next(i for i, l in enumerate(lines) if APPENDIX_HEADER.match(l.strip())) + 1
        for line in lines[start:]:
            if FOOTER.match(line):
                continue
            split = _split_row(line, known)
            if not split:
                continue
            label, value, cited = split
            offset = line.index(value)
            vms = [m for m in mentions(value) if not m.qualifier]
            roles = _roles(value, vms)
            for i, m in enumerate(vms):
                m.start += offset
                m.end += offset
                kind = _kind(m, value[vms[i].start - offset:vms[i].end - offset], f"{label} {value}", (), roles[i])
                if not _usable(m, kind):
                    kind = "other"
                out.append(Statement("appendix", uri, f"slide {appendix}", line, f"{label} {value}", m, kind,
                                     slide=appendix, cited_slide=cited, appendix_label=label))
                legend.append((cited, m, f"{label} {value}"))

    for n, text in enumerate(pages, start=1):
        if n == appendix:
            continue
        raw = [l for l in text.splitlines() if l.strip() and not FOOTER.match(l)]
        example_slide = any(l.startswith("Example") for l in raw)
        groups = _joined_lines(raw)
        consumed: set[int] = set()
        for g, (block, idxs) in enumerate(groups):
            if g in consumed:
                continue
            for sentence_text in _sentences(block):
                ms = mentions(sentence_text)
                roles = _roles(sentence_text, ms)
                for i, m in enumerate(ms):
                    if m.qualifier:
                        continue
                    rest = sentence_text.replace(m.printed, "", 1).split()
                    big = len(ms) == 1 and len(rest) <= 2 and block == sentence_text
                    label_line = groups[g + 1][0] if big and g + 1 < len(groups) else ""
                    row = next((lab for cited, lm, lab in legend if cited == n and _same_value(m, lm)), None)
                    fallbacks = tuple(x for x in (row, block, label_line) if x)
                    kind = _kind(m, _local(sentence_text, ms, i), row or (label_line if big else "") or sentence_text,
                                 fallbacks, roles[i])
                    if kind != "other" and not _usable(m, kind):
                        kind = "other"
                    if example_slide:
                        kind = "example"
                    if kind == "other" and m.kind_hint == "month" and any(
                            o is not m and o.kind_hint in ("number", "currency", "percent") for o in ms):
                        continue  # "audited in September 2026: 75,337": the month names the figure's period
                    quote = sentence_text
                    if big and label_line and not _has_claim(label_line):
                        quote = sentence_text + "\n" + label_line
                        consumed.add(g + 1)
                    out.append(Statement("deck", uri, f"slide {n}", quote, (row or label_line or sentence_text), m, kind, slide=n))
    _merge_appendix(out)
    return out, [], as_of(pages), True


def _has_claim(line: str) -> bool:
    """A label line under a big number holds no figure of its own (a month or a
    'next 12 months' names the big number's period)."""
    return any(not m.qualifier and m.kind_hint not in ("month", "range") for m in mentions(line))


def _same_value(a: Mention, b: Mention) -> bool:
    if a.iso or b.iso:
        return a.iso == b.iso
    return a.unit == b.unit and _near(a.number, b.number, max(a.precision, b.precision))


def _sentences(block: str) -> list[str]:
    return [s for s in _SENTENCE_END.split(block) if s.strip()]


def _merge_appendix(statements: list[Statement]) -> None:
    """A claims-page row and the content slide it cites state one fact. The content
    slide's statement is kept and the row becomes its repeat."""
    rows = [s for s in statements if s.origin == "appendix"]
    content = [s for s in statements if s.origin == "deck"]
    for row in rows:
        match = next((c for c in content if c.slide == row.cited_slide and c.kind == row.kind
                      and _same_value(c.mention, row.mention)), None)
        if match is None:
            match = next((c for c in content if c.slide == row.cited_slide and _same_value(c.mention, row.mention)
                          and c.kind in ("other", row.kind)), None)
            if match is not None and match.kind == "other":
                match.kind = row.kind
        if match is not None:
            match.repeats.append(row)
            statements.remove(row)


def claims_json_statements(room: Path, known: list[dict]) -> list[Statement]:
    paths = find(room, "deck_claims")
    if not paths:
        return []
    path = paths[0]
    raw = path.read_text(encoding="utf-8")
    out = []
    for n, c in enumerate(known, start=1):
        span = re.search(r'"label":\s*' + re.escape(json.dumps(c["label"])) + r',\s*"value":\s*' + re.escape(json.dumps(c["value"])), raw)
        if not span:
            continue
        for m in mentions(c["value"]):
            if m.qualifier:
                continue
            kind = _kind(m, c["value"], f"{c['label']} {c['value']}", (), None)
            if not _usable(m, kind):
                kind = "other"
            out.append(Statement("claims_json", _rel(path, room), f"row {n}", span.group(0), f"{c['label']} {c['value']}", m, kind,
                                 cited_slide=int(c.get("slide") or 0) or None, appendix_label=c["label"]))
    return out


# Pitch video ----------------------------------------------------------------


def video_statements(room: Path) -> tuple[list[Statement], str | None]:
    """(statements, which source): the transcript when it exists, else the script."""
    from schema.readers import transcript_segments

    for path in find(room, "video"):
        if path.suffix == ".json" or path.with_name(path.stem + ".transcript.json").exists():
            tpath = path if path.suffix == ".json" else path.with_name(path.stem + ".transcript.json")
            out = []
            for seg in transcript_segments(tpath):
                for sentence_text in _sentences(seg["text"]):
                    out += _spoken(sentence_text, "transcript", _rel(tpath, room), f"seg {seg['id']}",
                                   seg=seg["id"], start_s=seg["start_s"], end_s=seg["end_s"])
            return out, "transcript"
    for path in find(room, "video_script"):
        out, beat = [], None
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            head = BEAT.match(line.strip())
            if head:
                beat = f"{head.group(1)}:{head.group(2)}"
                continue
            if not line.strip() or line.startswith(("#", "---")) or FOOTER.match(line) or beat is None:
                continue
            for sentence_text in _sentences(line):
                out += _spoken(sentence_text, "script", _rel(path, room), f"line {n}", line=n, beat=beat)
        return out, "script"
    return [], None


def _spoken(text: str, origin: str, uri: str, locator: str, **where) -> list[Statement]:
    ms = mentions(text)
    roles = _roles(text, ms)
    out = []
    for i, m in enumerate(ms):
        if m.qualifier:
            continue
        kind = _kind(m, _local(text, ms, i), text, (), roles[i])
        if kind != "other" and not _usable(m, kind):
            kind = "other"
        out.append(Statement(origin, uri, locator, text, text, m, kind, **where))
    return out
