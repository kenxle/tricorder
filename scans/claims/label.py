"""Normalise each statement, compare it with its evidence, and label it.

Rules (ROADMAP "claim-support", FRAMEWORKS 4.3, ARCHITECTURE "How the readout is built"):

- supported: at least one document outside the company's own telling agrees,
  so two independent sources (the pitch and that document) state the figure;
  and no document disagrees.
- contradicted: a document disagrees beyond the tolerance. The claim shows the
  statement and the disagreeing source. A spoken figure that disagrees with
  the deck is contradicted too, unless an independent document backs it.
- unsupported: nothing outside the pitch states it. A gap names the document
  that would, for the ask list.

Tolerances come from schema.settings: `match_tolerance` for printed figures,
widened to the rounding the figure was printed with ("$2.5M" allows 50,000),
and `spoken_tolerance` for any comparison with a spoken figure.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from schema.claim import Check, Claim, Gap, Panel, Source, Value
from schema.settings import load as load_settings
from scans.base import Ids, gap
from scans.claims.evidence import READERS, Evidence, Reading, independent_group
from scans.claims.extract import Statement
from scans.claims.kinds import KINDS
from scans.claims.numbers import HEDGES

TABLE = "claims table"
COUNTS = "claims table counts"
NOT_COUNTED = "claims not counted"
# Nouns that say what a bare figure counts, so "29" reads "29 months" in a sentence.
COUNT_NOUNS = {"months", "years", "weeks", "days", "hires", "people", "clinics", "brokers", "locations",
               "customers", "employees", "cohorts"}

COLUMNS = ["claim id", "label", "where", "quote", "kind", "stated", "normalised", "spoken",
           "agrees", "disagrees", "should be backed by", "ask"]

DOC_OF_READER = {
    "model": ("financial model", "C19"), "team": ("financial model", "C19"), "cap": ("cap table", "C72"),
    "metrics": ("metrics export", "C02"), "customers": ("revenue by customer", "C03"),
    "hiring": ("hiring plan", "C22"), "contract": ("customer contracts", "C34"), "bios": ("founder bios", "C53"),
}

UNIT_WORDS = {"USD": "USD", "USD_per_month": "USD a month", "USD_per_year": "USD a year", "percent": "percent",
              "months": "months", "accounts": "accounts", "count": ""}


@dataclass
class Labelled:
    st: Statement
    number: float | None
    label: str = "unsupported"
    agree: list[Evidence] = field(default_factory=list)
    disagree: list[Evidence] = field(default_factory=list)
    founder_agree: list[Statement] = field(default_factory=list)
    founder_disagree: list[Statement] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    claim: Claim | None = None

    @property
    def kind(self):
        return KINDS[self.st.kind]


def normalised_number(st: Statement) -> float | None:
    if st.kind == "grew_every_month":
        return 1.0  # the claim is that revenue rose every month: 1 means it did
    n = st.mention.number
    if n is None:
        return None
    kind = KINDS[st.kind]
    if kind.unit == "months" and st.mention.unit_word in ("years", "year"):
        return n * 12
    return n


def rounded_speech(st: Statement) -> bool:
    """A spoken figure said loosely: hedged ("about", "close to") or rounded ("three million")."""
    return st.spoken and (st.mention.hedge is not None or st.mention.precision > 1)


def tolerance(st: Statement, other: Statement | None, settings: dict) -> float:
    loose = rounded_speech(st) or (other is not None and rounded_speech(other))
    if loose:
        # spoken_tolerance decides a spoken figure; "about" or "three million" earns no more
        # room than that (FRAMEWORKS 4.3, "What it must not do").
        return float(settings["spoken_tolerance"])
    base = float(settings["match_tolerance"])
    n = normalised_number(st)
    if n and not st.spoken:
        scale = 12 if (KINDS[st.kind].unit == "months" and st.mention.unit_word in ("years", "year")) else 1
        base = max(base, (st.mention.precision * scale / 2) / abs(n))
    return base


def agrees(st: Statement, number: float | None, iso: str | None, tol: float) -> bool:
    if st.kind == "grew_every_month":
        return number == 1.0
    if st.mention.iso is not None or (number is None and iso is not None):
        mine = st.mention.iso or ""
        return bool(iso) and (iso == mine or iso.startswith(mine) or mine.startswith(iso))
    n = normalised_number(st)
    if n is None or number is None:
        return False
    if st.mention.bound == "max":
        return number <= n * (1 + tol)
    if st.mention.bound == "min":
        return number >= n * (1 - tol)
    if n == number:
        return True
    return abs(number - n) <= tol * max(abs(n), abs(number))


def _period(st: Statement, as_of: str | None) -> str | None:
    kind = KINDS[st.kind]
    month = (as_of or "")[:7] or None
    for m in [x for x in __import__("scans.claims.numbers", fromlist=["mentions"]).mentions(st.quote) if x.kind_hint == "month"]:
        month = m.iso
        break
    if kind.period == "as_of":
        return month
    if kind.period == "plan":
        return f"plan from {month}" if month else "plan"
    if kind.period == "ltm" and month:
        y, m = int(month[:4]), int(month[5:])
        start_y, start_m = (y, m - 11) if m > 11 else (y - 1, m + 1)
        return f"{start_y}-{start_m:02d} to {month}"
    return None


def _figure(st: Statement) -> str:
    m = st.mention
    hedge = f"{m.hedge} " if m.hedge and not m.printed.lower().startswith(m.hedge) else ""
    if m.hedge and m.bound and dict(HEDGES).get(m.hedge) != m.bound:
        # "No customer above 9%" is a ceiling: say "at most 9%", not "above 9%".
        hedge = {"max": "at most ", "min": "at least "}[m.bound]
    tail = f" {m.unit_word}" if m.kind_hint == "words" and m.unit_word else ""
    return f"{hedge}{m.printed}{tail}"


def _where_words(st: Statement) -> str:
    if st.origin == "script":
        return f"The pitch video script (line {st.line}, beat {st.beat}; the video is not recorded yet)"
    if st.origin == "transcript":
        return f"The pitch video ({st.start_s:.0f}s to {st.end_s:.0f}s)"
    if st.origin == "appendix":
        return f"The deck's claims page (slide {st.slide})"
    if st.origin == "claims_json":
        return "The deck's claims.json"
    if st.origin == "model":
        return f"The deck (slide {st.slide}, read by the model)"
    return f"The deck (slide {st.slide})"


def _source(st: Statement) -> Source:
    if st.origin == "transcript":
        return Source(kind="video", uri=st.uri, locator=st.locator, quote=st.quote, start_s=st.start_s, end_s=st.end_s)
    return Source(kind="file", uri=st.uri, locator=st.locator, quote=st.quote)


def _ev_words(e: Evidence) -> str:
    return f"{e.doc} ({e.words}): {e.printed}"


def _gap_pct(st: Statement, e: Evidence) -> str:
    n = normalised_number(st)
    if n and e.number is not None and not st.mention.bound:
        return f", {abs(e.number - n) / abs(n):.1%} {'lower' if e.number < n else 'higher'}"
    return ""


def label_all(room: Path, statements: list[Statement], as_of: str | None, ids: Ids) -> tuple[list[Labelled], list[Gap]]:
    settings = load_settings()
    out: list[Labelled] = []
    unreadable: dict[str, dict] = {}
    claims = [s for s in statements if s.kind != "example"]
    for st in claims:
        item = Labelled(st, normalised_number(st))
        tol = tolerance(st, None, settings)
        for key in KINDS[st.kind].evidence:
            try:
                reading = READERS[key](room, st, as_of)
            except Exception as exc:  # a founder's own file with other columns or text in a number cell
                reading = _unreadable(room, key, st, exc, unreadable)
            if reading.missing and reading.missing not in item.missing:
                item.missing.append(reading.missing)
            matched_docs = set()
            for e in reading.evidence:
                if e.group == "founder":
                    continue
                if reading.any_of and e.source.uri in matched_docs:
                    continue
                if agrees(st, e.number, e.iso, tol):
                    item.agree.append(e)
                    matched_docs.add(e.source.uri)
                elif not reading.any_of:
                    item.disagree.append(e)
        out.append(item)

    # The company's own telling against itself: the video's figure against the deck's.
    for a in out:
        for b in out:
            if a is b or a.st.kind != b.st.kind or a.st.kind == "other" or a.st.spoken == b.st.spoken:
                continue
            if a.st.mention.number is None and a.st.mention.iso is None:
                continue
            tol = tolerance(a.st, b.st, settings)
            other_n = normalised_number(b.st)
            if b.st.mention.bound or a.st.mention.bound:
                same = agrees(a.st, other_n, b.st.mention.iso, tol) or agrees(b.st, normalised_number(a.st), a.st.mention.iso, tol)
            else:
                same = agrees(a.st, other_n, b.st.mention.iso, tol)
            (a.founder_agree if same else a.founder_disagree).append(b.st)

    for item in out:
        if item.disagree:
            item.label = "contradicted"
        elif item.agree:
            item.label = "supported"
        elif item.founder_disagree:
            item.label = "contradicted"
        else:
            item.label = "unsupported"
        item.claim = _claim(item, ids, as_of)
    return out, _gaps(out) + _unreadable_gaps(unreadable)


# Reader key prefix -> the input kind scans.base.find looks up, to name the file that failed.
FILE_KIND = {"model": "model", "team": "model", "cap": "cap_table", "metrics": "metrics", "customers": "customers",
             "hiring": "hiring_plan", "contract": "contracts", "bios": "bios"}


def _unreadable(room: Path, key: str, st: Statement, exc: Exception, seen: dict) -> Reading:
    """A reader that raised: that document says nothing about this claim, and the file is
    named once in a gap. The claim falls through to the next document, or reads unsupported."""
    from scans.base import find

    prefix = key.split("_")[0]
    doc = DOC_OF_READER.get(prefix, (key, None))
    hits = find(room, FILE_KIND.get(prefix, prefix)) if prefix in FILE_KIND else []
    if prefix == "customers":
        hits = [h for h in hits if "customer" in h.name]
    rel = str(hits[0].relative_to(room)) if hits else doc[0]
    reason = f"{type(exc).__name__}: {exc}"
    entry = seen.setdefault(rel, {"doc": doc, "reasons": [], "kinds": [], "piece": KINDS[st.kind].piece})
    if reason not in entry["reasons"]:
        entry["reasons"].append(reason)
    if KINDS[st.kind].name not in entry["kinds"]:
        entry["kinds"].append(KINDS[st.kind].name)
    return Reading([], f"a readable {doc[0]} ({rel})")


def _unreadable_gaps(seen: dict) -> list[Gap]:
    out = []
    for rel, e in seen.items():
        doc, row = e["doc"]
        out.append(gap(f"Not in the room: a readable {doc}. {rel} could not be read for {', '.join(e['kinds'])}",
                       "a column or cell the script needs is missing or not a number: " + "; ".join(e["reasons"]),
                       f"{doc} with the expected columns" + (f" ({row})" if row else ""), e["piece"]))
    return out


def _check_name(item: Labelled) -> str:
    if item.st.spoken and item.label == "contradicted" and item.founder_disagree:
        return "spoken_arr_vs_claims_page" if item.st.kind == "arr" else "spoken_number_vs_claims_page"
    return "claim_support"


def _claim(item: Labelled, ids: Ids, as_of: str | None) -> Claim:
    st, kind = item.st, item.kind
    where, figure = _where_words(st), _figure(st)
    m = st.mention
    if (m.unit is None and m.kind_hint == "number" and (m.unit_word or "").lower() in COUNT_NOUNS
            and m.unit_word.lower() not in figure.lower()):
        figure = f"{figure} {m.unit_word}"   # "29" on a big-number slide reads "29 months" in the sentence
    if item.label == "supported":
        docs = "; ".join(f"{e.doc} ({e.words}: {e.printed})" for e in item.agree)
        text = f"Supported: {where} gives {kind.name} as {figure}. Outside the pitch, {docs} agree{'s' if len(item.agree) == 1 else ''}."
    elif item.label == "contradicted":
        parts = [f"{e.doc} ({e.words}) says {e.printed}{_gap_pct(st, e)}" for e in item.disagree]
        parts += [f"{_where_words(o)[0].lower()}{_where_words(o)[1:]} says {_figure(o)}" for o in item.founder_disagree
                  if (st.spoken or not item.disagree) and o.origin != "appendix"]
        text = f"Contradicted: {where} gives {kind.name} as {figure}, but " + "; ".join(parts) + "."
    else:
        text = f"Unsupported: {where} gives {kind.name} as {figure}. No document outside the pitch states it."
    value = None
    if item.number is not None and kind.unit:
        value = Value(number=item.number, unit=kind.unit, label=kind.label, period=_period(st, as_of))
    sources = [_source(st)]
    if item.label == "contradicted":
        sources += [s for e in item.disagree for s in e.sources]
        if st.spoken or not item.disagree:
            # A spoken figure is set against the deck's (FRAMEWORKS 4.3), so the deck's slide is shown too.
            sources += [_source(o) for o in item.founder_disagree if o.origin != "appendix"]
    else:
        sources += [_source(r) for r in st.repeats]
        sources += [s for e in item.agree for s in e.sources]
    seen, unique = set(), []
    for s in sources:
        if (s.uri, s.locator, s.quote) not in seen:
            seen.add((s.uri, s.locator, s.quote))
            unique.append(s)
    return Claim(id=ids(), scan="claims", text=text, value=value,
                 severity="flag" if item.label == "contradicted" else "info",
                 check=Check(kind="model", name=_check_name(item) + ".read", model=None) if st.origin == "model"
                 else Check(kind="script", name=_check_name(item), model=None),
                 confidence="quoted" if st.origin == "model" else "computed", sources=unique)


def backed_by(kind_name: str) -> str:
    docs = []
    for key in KINDS[kind_name].evidence:
        doc = DOC_OF_READER.get(key.split("_")[0])
        if doc and f"{doc[0]} ({doc[1]})" not in docs:
            docs.append(f"{doc[0]} ({doc[1]})")
    return ", ".join(docs) or f"{KINDS[kind_name].ask_doc}" + (f" ({KINDS[kind_name].ask_row})" if KINDS[kind_name].ask_row else "")


def ask_text(item: Labelled) -> str:
    kind = item.kind
    if item.label == "unsupported":
        return f"Please send {kind.ask_doc}" + (f" ({kind.ask_row})" if kind.ask_row else "") + f", to back: {_figure(item.st)}."
    if item.label == "contradicted":
        return f"Please walk us from the source data to {_figure(item.st)} ({item.st.where}) (C71)."
    return ""


def _gaps(items: list[Labelled]) -> list[Gap]:
    by_kind: dict[str, list[Labelled]] = {}
    for item in items:
        if item.label == "unsupported":
            by_kind.setdefault(item.st.kind, []).append(item)
    gaps = []
    for name, group in by_kind.items():
        kind = KINDS[name]
        missing = sorted({m for i in group for m in i.missing})
        wheres = "; ".join(f"{i.st.where}: {_figure(i.st)}" for i in group)
        n = len(group)
        gaps.append(gap(f"Not in the room: {kind.ask_doc}, to back {n} pitch claim{'s' if n > 1 else ''} on {kind.name} ({wheres})",
                        _why(missing),
                        kind.ask_doc + (f" ({kind.ask_row})" if kind.ask_row else ""), kind.piece))
    return gaps


def _why(missing: list[str]) -> str:
    gone = [m for m in missing if not m.startswith("a readable ")]
    bad = [m.removeprefix("a readable ") for m in missing if m.startswith("a readable ")]
    parts = (["file missing: " + ", ".join(gone)] if gone else []) + (["could not read: " + ", ".join(bad)] if bad else [])
    return "; ".join(parts) or "not stated in any document outside the pitch"


def _unit_words(item: Labelled) -> str:
    kind = item.kind
    if item.number is None or kind.unit is None:
        return (item.st.mention.iso or item.st.mention.printed)
    words = UNIT_WORDS.get(kind.unit or "", "")
    n = item.number
    shown = f"{n:,.0f}" if abs(n - round(n)) < 1e-9 else f"{n:,.2f}"
    bound = {"max": "at most ", "min": "at least "}.get(item.st.mention.bound or "", "")
    return f"{bound}{shown} {words}".strip()


def panels(items: list[Labelled], skipped: list[Statement], as_of: str | None, video_source: str | None) -> list[Panel]:
    rows = []
    order = {"contradicted": 0, "unsupported": 1, "supported": 2}
    for item in sorted(items, key=lambda i: (order[i.label], i.st.slide or 99, i.st.line or 0)):
        st = item.st
        period = item.claim.value.period if item.claim and item.claim.value else None
        normal = f"{item.kind.name}: {_unit_words(item)}" + (f", {period}" if period else "")
        spoken = ""
        if st.spoken:
            spoken = "spoken" + (", rounded" if st.mention.kind_hint == "words" or st.mention.hedge else "") + \
                     (f" ({st.mention.hedge})" if st.mention.hedge else "") + (", from the script" if st.origin == "script" else "")
        agree = [_ev_words(e) for e in item.agree] + [f"{o.where}: {_figure(o)} (same pitch)" for o in item.founder_agree]
        disagree = [_ev_words(e) for e in item.disagree] + [f"{o.where}: {_figure(o)} (same pitch)" for o in item.founder_disagree]
        where = st.where + "".join(f"; repeated at {r.where}: '{r.quote}'" for r in st.repeats)
        rows.append([item.claim.id, item.label, where, st.quote.replace("\n", " "), item.kind.name, _figure(st), normal, spoken,
                     "; ".join(agree), "; ".join(disagree), backed_by(st.kind), ask_text(item)])
    counts = {k: sum(1 for i in items if i.label == k) for k in ("supported", "contradicted", "unsupported")}
    by_origin: dict[str, int] = {}
    for i in items:
        by_origin[i.st.origin] = by_origin.get(i.st.origin, 0) + 1
    count_rows = [["claims", str(len(items))]] + [[k, str(v)] for k, v in counts.items()] + \
                 [[f"from {k}", str(v)] for k, v in sorted(by_origin.items())] + \
                 [["as of", as_of or "not stated"], ["video source", video_source or "none"],
                  ["not counted (examples)", str(len(skipped))]]
    out = [Panel(name=TABLE, columns=COLUMNS, rows=rows), Panel(name=COUNTS, columns=["what", "count"], rows=count_rows)]
    out.append(Panel(name=NOT_COUNTED, columns=["where", "quote", "why"],
                     rows=[[s.where, s.quote.replace("\n", " "), "an illustrative example on the slide, not a claim about the company"]
                           for s in skipped]))
    return out


def independent(uri: str) -> bool:
    return independent_group(uri) != "founder"
