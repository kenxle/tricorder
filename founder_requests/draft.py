"""Draft a message to the founder from the readout's ask list.

A pure script over the readout and the guidance table: no model call, no
network, nothing sent. The operator copies the text or opens the mailto link
in their own mail app (ROADMAP.md, founder-requests).

Every word the founder reads goes through `founder_text`, which keeps out
file paths, cell references, claim ids and checklist ids (wave 1 review, U8).
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from urllib.parse import quote

from schema.claim import AskItem, Readout
from founder_requests import guidance as gd

ASKS_PANEL = "checklist ask lines"  # written by scans/memo/coverage.py
# Some mail apps cut a mailto link past about 2,000 characters. Past this the page offers copy first.
MAILTO_MAX = 2000

# Ask text written for the founder where the line's own words read badly (the checklist's
# "Please send: <item>." fallback). Keyed by checklist id; the operator still edits the draft.
FOUNDER_TEXT = {
    "C97": "Please send a reference list: people from management, customers, current investors and advisors we may call.",
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
# can answer) and rows whose guide covers a different document. These rows carry no guidance block.
OWN_TITLE = {
    "C29": "Current burn and cash",
    "C46": "Customer reference calls",
    "C58": "People we can call about the founders",
    "C71": "A walk through the numbers",
    "C101": "Patents, trademarks, copyrights and domain names",
}


def guidance_for(checklist_id: str | None):
    """A document row's guidance. Ask rows and the rows in OWN_TITLE get none: their guide is about another document."""
    if checklist_id in OWN_TITLE:
        return None
    return gd.for_item(checklist_id)


def title_for(checklist_id: str | None) -> str:
    g = guidance_for(checklist_id)
    if g:
        return g.title
    return OWN_TITLE.get(checklist_id or "", "Other")


# What the founder must never see.
_LOCATION = re.compile(r"\s*\([^()]*(?:\.xlsx|\.csv|\.pdf|\.md|\.json|![A-Z]+\$?\d+)[^()]*\)")
_PATH = re.compile(r"\b[\w./-]*\w\.(?:xlsx|csv|pdf|md|json)\b")
_CELL = re.compile(r"\b\w+![A-Z]+\$?\d+\b")
_CHECKLIST_ID = re.compile(r"\bC\d{1,3}\b")
_CLAIM_ID = re.compile(r"\b[a-z]+-\d{3}\b")
_INTERNAL = re.compile(r"Not in the room:|Also needed for", re.I)
LEAKS = (_PATH, _CELL, _CHECKLIST_ID, _CLAIM_ID, _INTERNAL)


def leaks(text: str) -> list[str]:
    """Every internal reference in a text: the test and the route both call this."""
    return [m.group(0) for pat in LEAKS for m in pat.finditer(text)]


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


@dataclass
class Item:
    number: int                 # the line's position in readout.asks, from 1
    text: str                   # founder words
    operator_why: str           # the readout's reason, for the operator only; never in the message
    piece: str
    checklist_id: str | None
    covers: list[str]
    if_you_have_it: bool
    ask_stage: str              # before_second_meeting or after_term_sheet
    top: int | None             # rank in the pinned top five
    title: str                  # the heading the founder reads
    guidance: dict | None       # {guide, title, what, form, good, path}


def _panel_rows(readout: Readout) -> dict[str, list[str]]:
    for p in readout.panels:
        if p.name == ASKS_PANEL:
            return {r[0].strip().lower(): r for r in p.rows}
    return {}


def items(readout: Readout) -> list[Item]:
    """Every ask line, with its founder words and guidance."""
    rows = _panel_rows(readout)
    out = []
    for n, a in enumerate(readout.asks, start=1):
        row = rows.get(a.what.strip().lower())
        covers = [c.strip() for c in row[1].split(",") if c.strip()] if row else ([a.checklist_id] if a.checklist_id else [])
        g = guidance_for(a.checklist_id)
        out.append(Item(
            number=n, text=founder_text(a), operator_why=a.why, piece=a.piece, checklist_id=a.checklist_id,
            covers=covers, if_you_have_it=a.if_you_have_it,
            ask_stage=row[3] if row else "before_second_meeting",
            top=int(row[4]) if row and row[4] else None,
            title=title_for(a.checklist_id),
            guidance=(asdict(g) | {"good": list(g.good), "path": g.path}) if g else None,
        ))
    return out


def default_selection(all_items: list[Item]) -> list[int]:
    """The pinned top five; with none pinned, every required line asked before the second meeting."""
    top = sorted((i for i in all_items if i.top), key=lambda i: i.top)
    if top:
        return [i.number for i in top]
    need = [i.number for i in all_items if not i.if_you_have_it and i.ask_stage == "before_second_meeting"]
    return need or [i.number for i in all_items]


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
    items: list[Item] = field(default_factory=list)
    leaks: list[str] = field(default_factory=list)


def _block(n: int, group: list[Item]) -> list[str]:
    g = group[0].guidance
    lines = [f"{n}. {group[0].title}"]
    lines += [i.text for i in group]
    if g:
        lines += [f"   What it is: {g['what']}", f"   Best form: {g['form']}",
                  "   A good one shows: " + "; ".join(g["good"]) + "."]
    return lines


def _groups(chosen: list[Item]) -> list[list[Item]]:
    """Lines that share a guide go under one heading, in the order they first appear."""
    groups: dict[str, list[Item]] = {}
    for i in chosen:
        key = i.guidance["guide"] if i.guidance else f"line-{i.number}"
        groups.setdefault(key, []).append(i)
    return list(groups.values())


def mailto(to: str, subject: str, body: str) -> str:
    enc = lambda s: quote(s, safe="")  # noqa: E731 - spaces as %20, never "+" (RFC 6068)
    return f"mailto:{quote(to, safe='@')}?subject={enc(subject)}&body={enc(body.replace(chr(10), chr(13) + chr(10)))}"


def draft(readout: Readout, numbers: list[int] | None = None, room_dir: Path | None = None,
          to: str = "", sender: str = "") -> Draft:
    """The message for the chosen ask lines (numbers from 1, as on the page); the default selection when none."""
    every = items(readout)
    if not every:
        raise ValueError("Nothing to ask for: the readout's ask list is empty.")
    by_n = {i.number: i for i in every}
    wanted = numbers if numbers else default_selection(every)
    bad = [n for n in wanted if n not in by_n]
    if bad:
        raise ValueError(f"no ask line {bad[0]}; the readout has {len(every)}")
    chosen = [by_n[n] for n in dict.fromkeys(wanted)]
    company, first, read_from = company_and_greeting(room_dir, readout.room)

    need = [i for i in chosen if not i.if_you_have_it]
    maybe = [i for i in chosen if i.if_you_have_it]
    body = [f"Hi {first}," if first else "Hello,", "",
            f"Thank you for the {company} data room. To finish our first pass, could you send the "
            + ("item" if len(chosen) == 1 else "items") + " below? A short note with each file is plenty. "
            "If something does not exist yet, just say so; that helps us too.", ""]
    n = 0
    for group in _groups(need):
        n += 1
        body += _block(n, group) + [""]
    if maybe:
        body += ["If you have them:", ""] if need else []
        for group in _groups(maybe):
            n += 1
            body += _block(n, group) + [""]
    body += ["Thank you,", sender] if sender else ["Thank you."]
    text = "\n".join(body).rstrip() + "\n"
    subject = f"{company}: " + ("one document for our review" if len(chosen) == 1 else "documents for our review")
    link = mailto(to, subject, text)
    return Draft(room=readout.room, company=company, to=to, subject=subject, body=text, mailto=link,
                 mailto_fits=len(link) <= MAILTO_MAX, read_from=read_from, items=chosen,
                 leaks=leaks(subject + "\n" + text))
