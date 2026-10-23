"""Draft a message to the founder from the readout's ask list.

A pure script over the readout, the room's file names and the guidance table: no model call,
no network, nothing sent. The operator copies the text or opens the mailto link in their own
mail app (ROADMAP.md, founder-requests).

Before a line reaches the founder it is checked against the room (03_prd.md, FR-R22 to FR-R25):
a line whose document the room already holds is dropped or reworded to what is still missing,
lines that ask for the same papers become one, and closing paperwork waits for the term sheet.
The pinned five are ranked by what settles the decision first (FR-R26).

Every word the founder reads goes through `founder_text`, which keeps out file paths, cell
references, claim ids and checklist ids (wave 1 review, U8).
"""

from __future__ import annotations

import os
import re
from dataclasses import asdict, dataclass, field
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

from schema.claim import AskItem, Readout
from founder_requests import guidance as gd
from scans.memo import checklist as cl

ASKS_PANEL = "checklist ask lines"      # written by scans/memo/coverage.py
COUNTS_PANEL = "checklist coverage counts"
# Some mail apps cut a mailto link past about 2,000 characters. Past this the page offers copy first.
MAILTO_MAX = 2000
DEFAULT_REASON = "before our partner meeting"
DEFAULT_DAYS = 7

# Ask text written for the founder where the line's own words read badly (the checklist's
# "Please send: <item>." fallback) or repeat another line. Keyed by checklist id.
FOUNDER_TEXT = {
    # One plain ask; the form goes on the "Ideally it includes" line, so the ask stays short.
    "C04": "Please send the investor updates you have sent since your first outside money.",
    "C22": "Please send your hiring plan for the next 12 to 18 months.",
    "C30": "Please send how you work out acquisition cost, lifetime value and payback.",
    "C36": "Please send a snapshot of your sales pipeline.",
    "C63": "Please send a recorded demo or a sandbox login, and a one-page roadmap.",
    "C74": "Please send your incorporation documents: the filed certificate with amendments, the bylaws and the first board consent.",
    "C76": "Please send the signed invention assignment agreements for each founder, employee and contractor, and a list of anyone who has not signed.",
    "C80": "Please send a short statement of any lawsuits, threatened claims, disputes or regulator contact, or say there are none.",
    "C102": "Please send a one-page note on the AI models and vendors the product uses and the data behind them.",
    "C77": "Please send the board and stockholder consents or minutes that approved each SAFE, note, stock issuance and option grant.",
    "C99": "Please send copies of your insurance policies, with the certificates.",
    "C100": "Please send any loan, lien or other charge on the company, or say there are none.",
    "C101": "Please send a list of your patents, trademarks, copyrights and domain names, with filing numbers.",
    "C110": "Please send your property leases.",
    "C111": "Please send your consulting agreements.",
    "C112": "Please send any licence of your IP to others, and of other people's IP to you.",
    "C113": "Please send any agreement that needs someone else's consent, or has change-of-control terms, because of this round.",
    "C114": "Please send any agreement with an officer, a director or a company they are tied to.",
}

# Item titles where the checklist row has no document guide of its own: "ask" rows (only the founder
# can answer) and rows whose guide covers a different document. These rows carry no guidance.
OWN_TITLE = {
    "C29": "Current burn and cash",
    "C46": "Customer reference calls",
    "C58": "People we can call about the founders",
    "C71": "A walk through the numbers",
    "C97": "Reference list",
    "C101": "Patents, trademarks, copyrights and domain names",
}

# Lines that ask for the same papers become one (FR-R23). The first id present names the guide.
@dataclass(frozen=True)
class Family:
    ids: tuple[str, ...]
    title: str
    text: str          # may hold {beyond}: filled when the room already holds part of it


FAMILIES = (
    Family(("C73", "C78"), "Option grants and 409A",
           "Please send the option grant ledger with the signed grant and advisor agreements, and the latest 409A report."),
    Family(("C98", "C99", "C100", "C110", "C111", "C112", "C113", "C114"), "Material agreements",
           "Please send a list of agreements over $25,000 with copies: your lease, any loan or lien, insurance "
           "policies, IP licences and consulting agreements{beyond}."),
    Family(("C35", "C46", "C58", "C97"), "People we can call",
           "Please send names and contacts of people we can call: three customers (your largest and one who "
           "stopped using the product), two people who have worked with the founders, and a current investor "
           "or advisor. Any letters of intent too."),
)

# Closing paperwork: at pre-seed and seed it is asked after the term sheet, never in the first pass (FR-R24).
CLOSING_AT_SEED = {"C74", "C76", "C77"}
EARLY_STAGES = {"pre_seed", "seed"}

# What settles the decision first: the readout's own piece order (FR-R26).
PIECE_WEIGHT = ("traction_and_revenue", "retention", "burn_and_runway", "unit_economics", "customers",
                "market", "comps", "team", "the_pitch_itself")

# What founder must never see.
_LOCATION = re.compile(r"\s*\([^()]*(?:\.xlsx|\.csv|\.pdf|\.md|\.json|![A-Z]+\$?\d+)[^()]*\)")
_PATH = re.compile(r"\b[\w./-]*\w\.(?:xlsx|csv|pdf|md|json)\b")
_CELL = re.compile(r"\b\w+![A-Z]+\$?\d+\b")
_CHECKLIST_ID = re.compile(r"\bC\d{1,3}\b")
_CLAIM_ID = re.compile(r"\b[a-z]+-\d{3}\b")
_INTERNAL = re.compile(r"Not in the room:|Also needed for", re.I)
LEAKS = (_PATH, _CELL, _CHECKLIST_ID, _CLAIM_ID, _INTERNAL)


def leaks(text: str) -> list[str]:
    """Every internal reference in a text: the tests and the route both call this."""
    return [m.group(0) for pat in LEAKS for m in pat.finditer(text)]


def guidance_for(checklist_id: str | None):
    """A document row's guidance. Rows in OWN_TITLE get none: their guide is about another document."""
    if checklist_id in OWN_TITLE:
        return None
    return gd.for_item(checklist_id)


def title_for(checklist_id: str | None) -> str:
    g = guidance_for(checklist_id)
    if g:
        return g.title
    return OWN_TITLE.get(checklist_id or "", "Other")


def founder_text(ask: AskItem) -> str:
    """One ask line in words the founder reads."""
    if ask.checklist_id in FOUNDER_TEXT:
        return FOUNDER_TEXT[ask.checklist_id]
    text = _LOCATION.sub("", ask.what)
    for pat in (_CELL, _PATH, _CHECKLIST_ID, _CLAIM_ID):
        text = pat.sub("", text)
    text = re.sub(r"\s+([,.;:])", r"\1", re.sub(r"\s{2,}", " ", text)).strip(" ,;")
    m = re.match(r"Please send:\s*(.+)", text)
    if m:
        item = m.group(1).rstrip(".")
        text = f"Please send your {item[0].lower() + item[1:]}."
    elif not re.match(r"(Please|Send|If)\b", text):
        text = f"Please send {text}"
    text = text[0].upper() + text[1:]
    return text if text.endswith((".", "?")) else text + "."


def _rows() -> dict[str, cl.Row]:
    return {r.id: r for r in cl.load()}


def _names(ids: list[str]) -> str:
    """Checklist ids as the items' plain names, for the operator's view (no codes)."""
    rows = _rows()
    return "; ".join(rows[i].item for i in ids if i in rows)


def operator_why(why: str) -> str:
    """The readout's reason with the "Also needed for C12, C24." codes turned into item names."""
    def repl(m):
        return "Also needed for: " + _names(_CHECKLIST_ID.findall(m.group(1))) + "."
    return re.sub(r"Also needed for ([C\d, ]+)\.", repl, why)


@dataclass
class Item:
    number: int                 # the first line's position in readout.asks, from 1
    lines: list[int]            # every readout ask line this item stands for
    text: str                   # founder words
    operator_why: str           # the readout's reason, for the operator only; never in the message
    piece: str
    checklist_id: str | None
    covers: list[str]
    if_you_have_it: bool
    ask_stage: str              # before_second_meeting or after_term_sheet
    top: int | None             # rank in the pinned five (FR-R26)
    title: str                  # the heading the operator reads
    guidance: dict | None       # {guide, title, what, form, good, path}, for the operator
    includes: str | None        # "Ideally it includes ..." for the founder
    in_room: list[str]          # room files that already answer part of it (operator view)
    rests_on_flag: bool
    requests: list[dict] = field(default_factory=list)  # [{checklist_id, name}]: what a reply's file can answer


@dataclass
class Held:
    """A line not asked because the room already holds it (operator view)."""
    number: int
    title: str
    files: list[str]


def _panel(readout: Readout, name: str):
    return next((p for p in readout.panels if p.name == name), None)


def _stage(readout: Readout) -> str | None:
    p = _panel(readout, COUNTS_PANEL)
    return dict((r[0], r[1]) for r in p.rows).get("stage") if p else None


def flagged_pieces(readout: Readout) -> set[str]:
    """Pieces a red flag or a weak verdict rests on: from piece verdicts when the merge wrote them,
    and from each flag claim's check name through the checklist rows that name that check."""
    out = {p.name for p in readout.pieces if p.verdict == "looking_weak"}
    rows = cl.load()
    for c in readout.claims:
        if c.severity != "flag":
            continue
        name = cl.check_names(c.check.name)
        exact = [r for r in rows if name in cl.ROW_CHECKS.get(r.id, set())]
        by_entry = [r for r in rows if r.id not in cl.ROW_CHECKS
                    and any(name in cl.ENTRY_CHECKS.get(e, set()) for e in r.entries)]
        out |= {r.readout_piece for r in (exact or by_entry)}
    return out


def _held(row: cl.Row | None, files: list[str]) -> list[str]:
    """Room files that are this document by name (coverage's file patterns). Coverage's "contained in"
    rules are left out on purpose: a model's P&L sheet is not the balance sheet a gap asks for."""
    if row is None or row.kind != "document":
        return []
    return cl.match_document(row, files, None)


def items(readout: Readout, room_dir: Path | None = None) -> list[Item]:
    """Every line to ask the founder, after the room check, the merges and the ranking."""
    return analyse(readout, room_dir)[0]


def held_lines(readout: Readout, room_dir: Path | None) -> list[Held]:
    """Lines not asked because the room already holds their document."""
    return analyse(readout, room_dir)[1]


def analyse(readout: Readout, room_dir: Path | None = None) -> tuple[list[Item], list[Held]]:
    panel = _panel(readout, ASKS_PANEL)
    rows_by_what = {r[0].strip().lower(): r for r in panel.rows} if panel else {}
    rows = _rows()
    files = cl.room_files(room_dir) if room_dir else []
    sow = [f for f in files if re.search(r"(^|/)sow_", f.lower())]
    early = _stage(readout) in EARLY_STAGES
    flagged = flagged_pieces(readout)

    raw: list[Item] = []
    held: list[Held] = []
    for n, a in enumerate(readout.asks, start=1):
        prow = rows_by_what.get(a.what.strip().lower())
        covers = [c.strip() for c in prow[1].split(",") if c.strip()] if prow else ([a.checklist_id] if a.checklist_id else [])
        g = guidance_for(a.checklist_id)
        row = rows.get(a.checklist_id or "")
        text, in_room = founder_text(a), []
        if room_dir is not None:
            have = _held(row, files)
            # Lines whose own document is in the room: reword to what is still missing, or drop.
            if have and a.from_kind == "gap" and "product type" in a.why:
                text, in_room = ("Please add the kind of revenue (subscription, pilot or one-time fee) to each row "
                                 "of the revenue by customer file you sent, and an MRR column to the monthly metrics."), have
            elif have:
                held.append(Held(n, title_for(a.checklist_id), have))
                continue
            # A line that also asks for a document the room holds: ask only for the rest.
            revenue = _held(rows.get("C03"), files)
            if a.checklist_id == "C14" and revenue:
                text, in_room = ("Please send the cohort export behind the deck's retention figure, with a "
                                 "one-line definition of a cohort."), revenue
        stage = prow[3] if prow else "before_second_meeting"
        if early and a.checklist_id in CLOSING_AT_SEED:
            stage = "after_term_sheet"
        raw.append(Item(
            number=n, lines=[n], text=text, operator_why=operator_why(a.why), piece=a.piece,
            checklist_id=a.checklist_id, covers=covers, if_you_have_it=a.if_you_have_it, ask_stage=stage, top=None,
            title=title_for(a.checklist_id),
            guidance=(asdict(g) | {"good": list(g.good), "path": g.path}) if g else None,
            includes=gd.includes(g.guide) if g and not (in_room and a.checklist_id == "C03") else None,
            in_room=in_room,
            rests_on_flag=a.from_kind == "gap" and a.piece in flagged,
            requests=[{"checklist_id": row.id, "name": row.item}] if row and row.kind in ("document", "ask") else [],
        ))

    out = _merge_families(raw, sow)
    _rank(out)
    return out, held


def _merge_families(raw: list[Item], sow: list[str]) -> list[Item]:
    out: list[Item] = []
    taken: dict[int, Item] = {}
    for it in raw:
        fam = next((f for f in FAMILIES if it.checklist_id in f.ids), None)
        if fam is None:
            out.append(it)
            continue
        key = FAMILIES.index(fam)
        if key not in taken:
            beyond = ""
            if sow:
                names = [re.sub(r"_", " ", Path(f).stem[4:]).title() for f in sow]
                beyond = f" beyond the {', '.join(names)} statement of work already in the room"
            g = guidance_for(it.checklist_id) or next((guidance_for(i) for i in fam.ids if guidance_for(i)), None)
            merged = Item(**{**asdict(it), "text": fam.text.format(beyond=beyond), "title": fam.title,
                             "guidance": (asdict(g) | {"good": list(g.good), "path": g.path}) if g else None,
                             "includes": gd.includes(g.guide) if g else None,
                             "in_room": list(it.in_room) + (sow if "{beyond}" in fam.text else [])})
            taken[key] = merged
            out.append(merged)
            continue
        m = taken[key]
        m.lines.append(it.number)
        m.covers += [c for c in it.covers if c not in m.covers]
        m.if_you_have_it = m.if_you_have_it and it.if_you_have_it
        if it.ask_stage == "before_second_meeting":
            m.ask_stage = "before_second_meeting"
        m.rests_on_flag = m.rests_on_flag or it.rests_on_flag
        m.requests += [r for r in it.requests if r not in m.requests]
        m.operator_why += " " + it.operator_why
    return out


def _rank(all_items: list[Item]) -> None:
    """The pinned five: asked before the second meeting, ranked by what settles the decision first."""
    weight = {p: i for i, p in enumerate(PIECE_WEIGHT)}
    pool = [i for i in all_items if i.ask_stage == "before_second_meeting"]
    pool.sort(key=lambda i: (weight.get(i.piece, len(weight)), not i.rests_on_flag, i.if_you_have_it, i.number))
    for n, it in enumerate(pool[:5], start=1):
        it.top = n


def default_selection(all_items: list[Item]) -> list[int]:
    """The pinned five, in rank order."""
    top = sorted((i for i in all_items if i.top), key=lambda i: i.top)
    return [i.number for i in top] or [i.number for i in all_items]


# Company and greeting --------------------------------------------------------------------


_SIGN_OFF = re.compile(r"^([A-Z][a-z]+)(?: [A-Z][\w'-]+)+, (?:Chief Executive Officer|CEO|Co-?founder|Founder)", re.M)


def company_and_greeting(room_dir: Path | None, room: str) -> tuple[str, str, str | None]:
    """(company name, greeting name or "", where each was read). Read from the deck's first line and
    the cover note's sign-off; the room id when the deck is unreadable."""
    company, first, source = room.replace("_", " ").title(), "", None
    if room_dir is None:
        return company, first, source
    from schema.readers import pdf_page
    from scans.base import find

    for path in find(room_dir, "deck"):
        try:
            line = pdf_page(path, 1).strip().splitlines()[0].strip()
        except Exception:  # noqa: BLE001 - an unreadable deck leaves the room id
            continue
        if line and len(line) <= 60:
            company, source = line, f"{path.relative_to(room_dir)}, slide 1"
            break
    for path in find(room_dir, "company_name"):
        if "cover_note" not in path.name:
            continue
        try:
            m = _SIGN_OFF.search(pdf_page(path, 1))
        except Exception:  # noqa: BLE001
            continue
        if m:
            first = m.group(1)
            source = (source + "; " if source else "") + f"{path.relative_to(room_dir)}, page 1"
            break
    return company, first, source


# The message -----------------------------------------------------------------------------


@dataclass
class Draft:
    room: str
    company: str
    to: str
    subject: str
    body: str
    mailto: str
    mailto_fits: bool
    read_from: str | None
    by: str
    items: list[Item] = field(default_factory=list)
    leaks: list[str] = field(default_factory=list)


def mailto(to: str, subject: str, body: str) -> str:
    enc = lambda s: quote(s, safe="")  # noqa: E731 - spaces as %20, never "+" (RFC 6068)
    return f"mailto:{quote(to, safe='@')}?subject={enc(subject)}&body={enc(body.replace(chr(10), chr(13) + chr(10)))}"


def default_by(today: date | None = None) -> date:
    return (today or date.today()) + timedelta(days=DEFAULT_DAYS)


def _when(d: date) -> str:
    return f"{d.strftime('%A')} {d.day} {d.strftime('%B')}"


def _block(n: int, it: Item, seen_guides: set) -> list[str]:
    lines = [f"{n}. {it.text}"]
    guide = it.guidance["guide"] if it.guidance else None
    if it.includes and guide not in seen_guides:
        lines.append(f"   Ideally it includes {it.includes}.")
        seen_guides.add(guide)
    return lines


def draft(readout: Readout, numbers: list[int] | None = None, room_dir: Path | None = None, to: str = "",
          sender: str | None = None, fund: str | None = None, by: date | str | None = None,
          reason: str = DEFAULT_REASON) -> Draft:
    """The message for the chosen items (numbers as on the page); the pinned five when none."""
    every, held = analyse(readout, room_dir)
    if not every:
        raise ValueError("Nothing to ask for: the readout's ask list is empty.")
    by_line = {n: i for i in every for n in i.lines}
    wanted = numbers if numbers else default_selection(every)
    bad = [n for n in wanted if n not in by_line]
    if bad:
        why = " (the room already holds it)" if bad[0] in {h.number for h in held} else ""
        raise ValueError(f"no ask line {bad[0]}{why}; the readout has {len(readout.asks)}")
    chosen = list({id(by_line[n]): by_line[n] for n in wanted}.values())
    company, first, read_from = company_and_greeting(room_dir, readout.room)
    sender = os.environ.get("TRICORDER_OPERATOR_NAME", "") if sender is None else sender
    fund = os.environ.get("TRICORDER_FUND_NAME", "") if fund is None else fund
    when = by if isinstance(by, date) else (date.fromisoformat(by) if by else default_by())

    need = [i for i in chosen if not i.if_you_have_it]
    maybe = [i for i in chosen if i.if_you_have_it]
    one = len(chosen) == 1
    body = [f"Hi {first}," if first else "Hello,", "",
            f"Thanks for sharing the {company} data room. Could you send the {'item' if one else 'items'} below "
            f"by {_when(when)}? We would like {'it' if one else 'them'} {reason}. A rough version is fine, and if "
            "something does not exist yet, just say so.", ""]
    seen: set = set()
    n = 0
    for it in need:
        n += 1
        body += _block(n, it, seen)
    if maybe:
        body += (["", "If you have them:"] if need else [])
        for it in maybe:
            n += 1
            body += _block(n, it, seen)
    body += ["", "Thanks,"] + [x for x in (sender, fund) if x]
    text = "\n".join(body).rstrip() + "\n"
    subject = f"{company}: {'one thing' if one else 'a few things'} before our next meeting"
    link = mailto(to, subject, text)
    return Draft(room=readout.room, company=company, to=to, subject=subject, body=text, mailto=link,
                 mailto_fits=len(link) <= MAILTO_MAX, read_from=read_from, by=when.isoformat(), items=chosen,
                 leaks=leaks(subject + "\n" + text))
