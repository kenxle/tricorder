"""The one contract reader for FRAMEWORKS.md entry 1.13, "Contract terms".

Two modules use it and neither reads a contract on its own:

- `contract_terms_full.py` (built before Saturday): checks 1, 3, 4 and 6, and the
  clause notes (exclusivity, most-favoured-customer, change of control, and the
  other clauses that change what a customer pays or when it can leave).
- `contract_terms.py` (built on Saturday, the contract-terms-saturday slice):
  the model reading with entry 1.13's prompt, and checks 2 and 5.

`read_room(room)` finds every contract in a folder, reads each one once and
returns `ContractTerms` in the shape of entry 1.13's "contracts" items. The
result is cached per folder and file modification time, so the second module to
ask gets the same reading without opening the PDFs again.

How a contract is read today: by script. Each term is found by its heading and
wording in the PDF text (`schema.readers.pdf_pages`), and its quote is the exact
span the script matched, whitespace joined. Every quote is then confirmed by the
quote checker (`schema.check_quotes.source_holds_quote`); a term whose quote is
not found is marked `quote_not_found` and no check uses it.

The seam for Saturday: a model reading registers itself with
`set_model_reader(fn)`, where `fn(room, paths) -> list[ContractTerms]`. When one
is set and `TRICORDER_CONTRACT_READER` is not "script", `read_room` uses it, and
the script reading fills any field the model left `not_stated` only when the
model reading failed outright. The design is in
docs/features/20261023.04_contract_terms/04_architecture.md.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Literal

from pydantic import BaseModel, ConfigDict

from schema.check_quotes import source_holds_quote
from schema.claim import Gap, Source
from schema.readers import pdf_pages
from scans.base import INPUT_KINDS, gap

# --------------------------------------------------------------------------- shapes


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Term(_Strict):
    """FRAMEWORKS 1.13 "Term", plus one status of our own: quote_not_found."""

    status: Literal["stated", "not_stated", "quote_not_found"]
    value: str | float | int | bool | None = None
    quote: str | None = None
    page: int | None = None
    clause: str | None = None  # the clause number when the text has one, for the locator

    @property
    def stated(self) -> bool:
        return self.status == "stated"

    def locator(self) -> str:
        loc = f"page {self.page}"
        return f"{loc}, clause {self.clause}" if self.clause else loc


NOT_STATED = Term(status="not_stated")


class FeeLine(_Strict):
    amount_usd: float
    per: Literal["month", "year", "term"]
    from_date: str | None
    to_date: str | None
    locations: int | None
    quote: str
    page: int


class NamedClause(_Strict):
    name: str
    summary: str
    effective_date: str | None
    quote: str
    page: int
    clause: str | None = None


ContractKind = Literal["order_form", "pilot_agreement", "subscription_agreement", "other"]


class ContractTerms(_Strict):
    """One contract, in the shape of entry 1.13's "contracts" item.

    Fields beyond the entry: `title`, `counterparty` (customer or supplier),
    `pages`, `page_heads` (each page's first line, the pointer a "not stated"
    result cites) and `read_by` (script or model).
    """

    uri: str
    title: str
    counterparty: Literal["customer", "supplier"]
    customer_name: Term
    kind: ContractKind
    effective_date: Term
    term_start_date: Term = NOT_STATED
    term_end_date: Term
    term_months: Term
    auto_renews: Term
    renewal_months: Term
    non_renewal_notice_days: Term
    termination_for_convenience: Term
    convenience_notice_days: Term
    breach_cure_days: Term
    is_pilot_or_trial: Term
    duty_to_convert: Term
    fee_schedule: list[FeeLine]
    discount_percent: Term
    list_price_usd_per_month: Term
    payment_terms: Term
    one_time_fee_usd: Term
    exclusivity: Term
    most_favoured_customer: Term
    change_of_control: Term
    other_clauses: list[NamedClause]
    amendments: list[NamedClause]
    pages: int
    page_heads: list[str]
    read_by: Literal["script", "model"] = "script"

    @property
    def name(self) -> str:
        return str(self.customer_name.value) if self.customer_name.stated else Path(self.uri).stem

    @property
    def label(self) -> str:
        """How every claim about this contract starts: "<name> <kind words>"."""
        return f"{self.name} {kind_words(self.title)}"

    def terms(self) -> dict[str, Term]:
        return {k: v for k, v in self if isinstance(v, Term)}


@dataclass
class RoomContracts:
    contracts: list[ContractTerms] = field(default_factory=list)
    gaps: list[Gap] = field(default_factory=list)
    read_by: str = "script"


CLAUSE_FIELDS = ("exclusivity", "most_favoured_customer", "change_of_control")

# --------------------------------------------------------------------------- finding contracts

_NAME_PATTERNS = tuple(p.split("/", 1)[1] for p in INPUT_KINDS["contracts"])
_PARTY = re.compile(r"\(the (Customer|Client|Contractor|Supplier|Vendor|Provider)\)")
_TITLE = re.compile(r"(order form|agreement|statement of work|contract|\bmsa\b|\bsow\b)", re.I)


def _looks_like_contract(path: Path) -> bool:
    if any(path.match(p) for p in _NAME_PATTERNS):
        return True
    try:
        first = pdf_pages(path)[0] if pdf_pages(path) else ""
    except Exception:  # noqa: BLE001 - an unreadable PDF is judged by name only
        return False
    head = first.strip().splitlines()[0] if first.strip() else ""
    return bool(_PARTY.search(first) and _TITLE.search(head))


def contract_paths(room: str | Path) -> list[Path]:
    """Every PDF in the folder, at any depth, that is a contract.

    By file name first (the room's own patterns, `scans.base.INPUT_KINDS`), then by
    its first page: a party named "(the Customer)" or similar and a title that
    names an order form, agreement or statement of work. So a folder holding only
    contracts, under any names, is a valid input.
    """
    room = Path(room)
    return sorted(p for p in room.rglob("*.pdf") if p.is_file() and _looks_like_contract(p))


# --------------------------------------------------------------------------- reading one contract

DATE = r"(\d{4}-\d{2}-\d{2})"
NUM = r"(?:[a-z]+ \()?(\d+)\)?"
_ABBREV = {"no", "inc", "ltd", "co", "mr", "ms", "dr", "st", "corp", "llc"}


def _norm(text: str) -> str:
    return " ".join(text.split())


def _sentence(text: str, start: int, end: int) -> tuple[int, int]:
    """The sentence around text[start:end]: from the last boundary before it to the next after."""

    def boundary(i: int) -> bool:
        # A period at i ends a sentence when a space and a capital, digit or $ follow,
        # and the word before it is not an abbreviation such as "No." or "Inc.".
        if text[i] not in ".;" or i + 2 > len(text) or text[i + 1:i + 2] != " ":
            return i == len(text) - 1 and text[i] == "."
        nxt = text[i + 2:i + 3]
        if not (nxt.isupper() or nxt.isdigit() or nxt == "$"):
            return False
        word = re.search(r"(\w+)$", text[:i])
        return not (word and word.group(1).lower() in _ABBREV)

    s = start
    while s > 0 and not boundary(s - 1):
        s -= 1
    while s < len(text) and text[s] == " ":
        s += 1
    e = end - 1 if end > start and text[end - 1] in ".;" else end
    while e < len(text) and not boundary(e):
        e += 1
    return s, min(e + 1, len(text))


_CLAUSE_HEAD = re.compile(r"(?:^|(?<=[.\s]))(\d{1,2})\. [A-Z][A-Za-z ,'-]{2,40}\. ")
_TABLE_ROW = re.compile(r"^(Plan|Locations|Monthly fee|Annual fee|Initial term|Term|Renewal|Payment|Onboarding fee|"
                        r"Platform fee|Fee|Recovery fee|Ending early|Additional hours|Team|Work) ")


def _clause_number(text: str, pos: int) -> str | None:
    heads = [m for m in _CLAUSE_HEAD.finditer(text) if m.start() <= pos]
    return heads[-1].group(1) if heads else None


@dataclass
class _Doc:
    path: Path
    uri: str
    pages: list[str]  # whitespace-joined text, page 1 first
    rows: list[list[int]] = field(default_factory=list)  # per page: where each table row starts
    foot: list[int] = field(default_factory=list)  # per page: where the last line (the footer) starts

    @classmethod
    def of(cls, path: Path, uri: str, raw: list[str]) -> "_Doc":
        pages, rows, foot = [], [], []
        for page in raw:
            starts, pos, parts, last = [], 0, [], 0
            for line in page.splitlines():
                line = _norm(line)
                if not line:
                    continue
                if _TABLE_ROW.match(line):
                    starts.append(pos)
                last = pos
                parts.append(line)
                pos += len(line) + 1
            pages.append(" ".join(parts))
            rows.append(starts)
            foot.append(last if len(parts) > 1 else pos)
        return cls(path=path, uri=uri, pages=pages, rows=rows, foot=foot)

    def clause_text(self, m: re.Match, page: int) -> str:
        """The whole numbered clause around a match, heading included, or its sentence when unnumbered."""
        text = self.pages[page - 1]
        heads = list(_CLAUSE_HEAD.finditer(text))
        mine = [h for h in heads if h.start() <= m.start()]
        if not mine:
            return self.sentence(m, page)
        start = mine[-1].start()
        ends = [h.start() - 1 for h in heads if h.start() > m.start()]
        ends += [i for i in (text.find(" Signed for", m.end()),) if i > 0]
        ends.append(self.foot[page - 1] - 1 if self.foot else len(text))
        return text[start:max(min(ends), m.end())].strip()

    def find(self, pattern: str, flags: int = re.I) -> tuple[re.Match, int] | None:
        rx = re.compile(pattern, flags)
        for n, text in enumerate(self.pages, start=1):
            m = rx.search(text)
            if m:
                return m, n
        return None

    def find_all(self, pattern: str, flags: int = re.I) -> list[tuple[re.Match, int]]:
        rx = re.compile(pattern, flags)
        return [(m, n) for n, text in enumerate(self.pages, start=1) for m in rx.finditer(text)]

    def sentence(self, m: re.Match, page: int) -> str:
        text = self.pages[page - 1]
        s, e = _sentence(text, m.start(), m.end())
        # A page's "Item Detail" table runs its rows together once the lines are joined.
        # A row starts a sentence, and the next row ends it.
        rows = self.rows[page - 1] if self.rows else []
        s = max([s] + [r for r in rows if r <= m.start()])
        e = min([e] + [r - 1 for r in rows if r > m.end()])
        return text[s:e].strip()

    def term(self, m: re.Match, page: int, value, whole_sentence: bool = True) -> Term:
        quote = self.sentence(m, page) if whole_sentence else m.group(0)
        return Term(status="stated", value=value, quote=quote, page=page,
                    clause=_clause_number(self.pages[page - 1], m.start()))


def _money(s: str) -> float:
    return float(s.replace(",", ""))


def kind_words(title: str) -> str:
    """'Order Form: Cedar & Pine' -> 'order form'; 'Statement of Work No. 2' -> 'statement of work'."""
    head = title.split(":", 1)[0] if ":" in title else title
    head = re.sub(r"\s+No\.\s*\d+.*$", "", head).strip()
    return head.lower() or "contract"


def _kind(title: str) -> ContractKind:
    t = title.lower()
    if "order form" in t:
        return "order_form"
    if re.search(r"pilot|trial|evaluation", t):
        return "pilot_agreement"
    if re.search(r"subscription|master services|\bmsa\b|services agreement", t):
        return "subscription_agreement"
    return "other"


def _fees(doc: _Doc) -> list[FeeLine]:
    lines: list[FeeLine] = []
    for m, page in doc.find_all(r"\$([\d,]+(?:\.\d+)?)"):
        text = doc.pages[page - 1]
        before, after = text[max(0, m.start() - 40):m.start()], text[m.end():m.end() + 40]
        if re.match(r"\s*(an hour|list price)", after) or re.search(r"(Onboarding|Setup|Set-up|Implementation) fee\s*$", before) \
                or re.match(r",? one time", after) or re.search(r"That is \d+ months at\s*$", before):
            continue
        if re.search(r"(Annual fee|a year)\s*$", before) or re.match(r"\s*a year", after):
            per = "year"
        elif re.match(r"\s*in total", after):
            per = "term"
        elif re.match(r"\s*a month", after) or re.search(r"(Monthly fee|monthly fee becomes|fee becomes)\s*$", before):
            per = "month"
        elif re.search(r"\.\s*$", before) and re.match(r"\s*(until|from) ", after) and lines and lines[-1].per == "month":
            per = "month"  # "$18,000 until 2026-03-31. $36,000 from 2026-04-01."
        else:
            continue
        to_d = re.match(r"\s*until " + DATE, after)
        from_d = re.match(r"\s*from " + DATE, after)
        lines.append(FeeLine(amount_usd=_money(m.group(1)), per=per, from_date=from_d.group(1) if from_d else None,
                             to_date=to_d.group(1) if to_d else None, locations=None,
                             quote=doc.sentence(m, page), page=page))
    return lines


_CLAUSE_WORDS = {
    "exclusivity": r"\bexclusiv\w*",
    "most_favoured_customer": r"most[- ]favou?red|no (?:less|more) favou?rable|best (?:price|pricing|terms)|"
                              r"lowest price|price (?:parity|protection)",
    "change_of_control": r"change (?:of|in) control|\bis acquired\b|\bacquir\w+ by\b|\bmerger\b|\bmerges\b|"
                         r"sale of (?:all|substantially all)",
}

# Other clauses that change what the customer pays or when it can leave (entry 1.13, rule 9).
_OTHER = (
    ("fee freeze", "a clause that holds the fees fixed",
     r"fees? (?:are|is) fixed|will not raise|fixed for the initial term|price (?:lock|freeze)"),
    ("price increase", "a clause that lets the fees rise",
     r"may (?:raise|increase) (?:the )?(?:fees|prices)|price increase|\bCPI\b|\buplift\b"),
    ("minimum commitment", "a minimum commitment", r"\bminimum (?:commitment|spend|purchase|fee|term)\b"),
    ("refund or credit", "a refund or credit clause",
     r"refunds? the fee|refund (?:of|the) (?:fees?|amount)|service credits?|credit (?:against|toward) (?:the )?fees?"),
    ("usage-based fee", "a fee that varies with use",
     r"\$[\d,]+ an hour|\bper (?:call|minute|transaction|seat|user)\b|\d+% of (?:money|each|the|all)"),
)


def read_contract(path: Path, room: Path) -> ContractTerms:
    """Read one contract by script. Raises on a PDF that cannot be opened."""
    raw = pdf_pages(path)
    doc = _Doc.of(path, str(path.relative_to(room)), raw)
    heads = [next((ln.strip() for ln in p.splitlines() if ln.strip()), "") for p in raw]
    title = heads[0] if heads else path.stem

    # Parties. "and X (the Customer)" is a customer; "(the Contractor)" and its kin a supplier.
    counterparty, name = "customer", NOT_STATED
    hit = doc.find(r"and (.+?) \(the (Customer|Contractor|Supplier|Vendor)\)", 0)
    if hit:
        m, page = hit
        counterparty = "customer" if m.group(2) == "Customer" else "supplier"
        name = Term(status="stated", value=m.group(1).strip(), quote=m.group(0), page=page)
    elif ":" in title:
        name = Term(status="stated", value=title.split(":", 1)[1].strip(), quote=title, page=1)

    t: dict[str, Term] = {}
    hit = doc.find(r"Effective date:\s*" + DATE)
    t["effective_date"] = doc.term(hit[0], hit[1], hit[0].group(1), whole_sentence=False) if hit else NOT_STATED

    hit = doc.find(NUM + r" months?, from " + DATE + r" to " + DATE)
    if hit:
        m, page = hit
        t["term_months"] = doc.term(m, page, int(m.group(1)))
        t["term_start_date"] = doc.term(m, page, m.group(2))
        t["term_end_date"] = doc.term(m, page, m.group(3))
    else:
        t["term_months"] = t["term_start_date"] = t["term_end_date"] = NOT_STATED
        hit = doc.find(r"month[- ]to[- ]month")
        if hit:
            t["term_months"] = doc.term(hit[0], hit[1], 1)
    if not t["effective_date"].stated and t["term_start_date"].stated:
        t["effective_date"] = t["term_start_date"]

    # Renewal: "Renews for 12 months at a time unless either party gives 90 days written notice".
    t["auto_renews"] = t["renewal_months"] = t["non_renewal_notice_days"] = NOT_STATED
    hit = doc.find(r"renews? (?:automatically )?for " + NUM + r" months?(?: at a time)? unless (?:either party|a party|"
                   r"the Customer|the Provider) gives " + NUM + r" days")
    if hit:
        m, page = hit
        t["auto_renews"] = doc.term(m, page, True)
        t["renewal_months"] = doc.term(m, page, int(m.group(1)))
        t["non_renewal_notice_days"] = doc.term(m, page, int(m.group(2)))
    else:
        hit = doc.find(r"(?:does|will) not renew|no automatic renewal|not renew automatically")
        if hit:
            t["auto_renews"] = doc.term(hit[0], hit[1], False)
        else:
            hit = doc.find(r"renews automatically|automatically renews")
            if hit:
                t["auto_renews"] = doc.term(hit[0], hit[1], True)

    # Ending the contract while it runs. A right to end for an unfixed breach is neither notice.
    t["termination_for_convenience"] = t["convenience_notice_days"] = t["breach_cure_days"] = NOT_STATED
    hit = doc.find(r"material breach that is not (?:fixed|cured) within " + NUM + r" days")
    if hit:
        t["breach_cure_days"] = doc.term(hit[0], hit[1], int(hit[0].group(1)))
    for m, page in doc.find_all(r"\bmay (?:end|terminate|cancel)\b[^.]*?(?:" + NUM + r" days)?[^.]*\."):
        sent = doc.sentence(m, page)
        # A right to end for a breach, or only after an event (a change of control, insolvency),
        # is not a right to end for any reason.
        if re.search(r"breach|\bif\b|\bafter\b|\bupon\b|change (?:of|in) control|acquired|insolven|bankrupt", sent, re.I):
            continue
        days = re.search(NUM + r" days", sent)
        t["termination_for_convenience"] = doc.term(m, page, True)
        if days:
            t["convenience_notice_days"] = doc.term(m, page, int(days.group(1)))
        break
    if not t["termination_for_convenience"].stated:
        hit = doc.find(r"has no other right to (?:end|terminate|cancel)")
        if hit:
            t["termination_for_convenience"] = doc.term(hit[0], hit[1], False)

    # Pilot or trial, and any duty to buy afterwards.
    t["is_pilot_or_trial"] = t["duty_to_convert"] = NOT_STATED
    hit = doc.find(r"is a (?:trial|pilot|evaluation) of|not a subscription")
    if hit:
        t["is_pilot_or_trial"] = doc.term(hit[0], hit[1], True)
    elif re.search(r"\b(pilot|trial|evaluation)\b", title, re.I):
        t["is_pilot_or_trial"] = Term(status="stated", value=True, quote=title, page=1)
    hit = doc.find(r"Nothing in this agreement requires the Customer to (?:buy|purchase)")
    if hit:
        t["duty_to_convert"] = doc.term(hit[0], hit[1], False)
    else:
        hit = doc.find(r"(?:must|shall|agrees to) (?:buy|purchase|subscribe|convert)")
        if hit:
            t["duty_to_convert"] = doc.term(hit[0], hit[1], True)

    # Price terms.
    t["discount_percent"] = t["list_price_usd_per_month"] = NOT_STATED
    hit = doc.find(r"(\d+(?:\.\d+)?)% off the \$([\d,]+(?:\.\d+)?) list price")
    if hit:
        t["discount_percent"] = doc.term(hit[0], hit[1], float(hit[0].group(1)))
        t["list_price_usd_per_month"] = doc.term(hit[0], hit[1], _money(hit[0].group(2)))
    hit = doc.find(r"Payment (Monthly in advance, net \d+ days)|invoiced (once, in advance|monthly|at the start of each month)")
    t["payment_terms"] = doc.term(hit[0], hit[1], hit[0].group(1) or hit[0].group(2)) if hit else NOT_STATED
    hit = doc.find(r"(?:Onboarding|Setup|Set-up|Implementation) fee \$([\d,]+), one time")
    t["one_time_fee_usd"] = doc.term(hit[0], hit[1], _money(hit[0].group(1)), whole_sentence=False) if hit else NOT_STATED

    # The clause fields Saturday leaves unread.
    for fld, rx in _CLAUSE_WORDS.items():
        hit = doc.find(rx)
        if hit:
            m, page = hit
            t[fld] = Term(status="stated", value=True, quote=doc.clause_text(m, page), page=page,
                          clause=_clause_number(doc.pages[page - 1], m.start()))
        else:
            t[fld] = NOT_STATED

    other: list[NamedClause] = []
    seen = set()
    for name_, summary, rx in _OTHER:
        for m, page in doc.find_all(rx):
            quote = doc.sentence(m, page)
            clause = _clause_number(doc.pages[page - 1], m.start())
            # One note per clause: two sentences of one numbered clause are one clause.
            where = (name_, page, clause) if clause else (name_, quote)
            if where in seen:
                continue
            seen.add(where)
            other.append(NamedClause(name=name_, summary=summary, effective_date=None, quote=quote, page=page,
                                     clause=clause))

    # One note per kind of clause: a table row that restates a numbered clause is the same clause.
    best: dict[str, NamedClause] = {}
    for oc in other:
        if oc.name not in best or (oc.clause and not best[oc.name].clause):
            best[oc.name] = oc
    other = [oc for oc in other if best[oc.name] is oc]

    amendments: list[NamedClause] = []
    fees = _fees(doc)
    for m, page in doc.find_all(r"Amendment No\. (\d+) Effective " + DATE + r"\. (.+?)(?= Signed for| Synthetic data room|$)"):
        body = m.group(3).strip()
        quote = f"Effective {m.group(2)}. {body}"
        amendments.append(NamedClause(name=f"Amendment No. {m.group(1)}", summary=body.split(". ")[0].rstrip(".") + ".",
                                      effective_date=m.group(2), quote=quote, page=page))
        for fee in fees:  # an amendment's new fee runs from the amendment's date
            if fee.page == page and fee.from_date is None and fee.quote in quote:
                fee.from_date = m.group(2)

    return ContractTerms(
        uri=doc.uri, title=title, counterparty=counterparty, customer_name=name, kind=_kind(title),
        fee_schedule=fees, other_clauses=other, amendments=amendments, pages=len(raw), page_heads=heads, **t,
    )


# --------------------------------------------------------------------------- quotes confirmed


def _confirm(c: ContractTerms, room: Path) -> ContractTerms:
    """Every stated term's quote must be at its page, or the term is not used."""
    updates = {}
    for fld, term in c.terms().items():
        if term.stated and term.quote:
            ok, _ = source_holds_quote(Source(kind="file", uri=c.uri, locator=term.locator(), quote=term.quote), room)
            if not ok:
                updates[fld] = term.model_copy(update={"status": "quote_not_found"})
    keep = lambda items: [x for x in items if source_holds_quote(  # noqa: E731
        Source(kind="file", uri=c.uri, locator=f"page {x.page}", quote=x.quote), room)[0]]
    updates["other_clauses"] = keep(c.other_clauses)
    updates["amendments"] = keep(c.amendments)
    updates["fee_schedule"] = keep(c.fee_schedule)
    return c.model_copy(update=updates)


# --------------------------------------------------------------------------- the room, read once

ModelReader = Callable[[Path, list[Path]], list[ContractTerms]]
_model_reader: ModelReader | None = None
_CACHE: dict[tuple, RoomContracts] = {}


def set_model_reader(fn: ModelReader | None) -> None:
    """Saturday's model reading plugs in here. None removes it."""
    global _model_reader
    _model_reader = fn
    _CACHE.clear()


def _key(room: Path, paths: list[Path]) -> tuple:
    return (str(room.resolve()), os.environ.get("TRICORDER_CONTRACT_READER", ""), id(_model_reader),
            tuple((str(p), p.stat().st_mtime_ns) for p in paths))


def read_room(room: str | Path) -> RoomContracts:
    """Every contract in the folder, read once and cached. A PDF that cannot be read is a gap."""
    room = Path(room)
    paths = contract_paths(room)
    key = _key(room, paths)
    if key in _CACHE:
        return _CACHE[key]
    out = RoomContracts()
    use_model = _model_reader is not None and os.environ.get("TRICORDER_CONTRACT_READER", "") != "script"
    if use_model:
        try:
            out.contracts = [_confirm(c, room) for c in _model_reader(room, paths)]
            out.read_by = "model"
        except Exception as err:  # noqa: BLE001 - a failed model reading falls back to the script
            out.gaps.append(gap("Not in the room: a model reading of the contracts", f"model reading failed: {err}",
                                "a working model key; the script reading was used instead", "customers"))
            use_model = False
    if not use_model:
        for p in paths:
            try:
                out.contracts.append(_confirm(read_contract(p, room), room))
            except Exception as err:  # noqa: BLE001 - one bad PDF never stops the others
                rel = p.relative_to(room)
                out.gaps.append(gap(f"Not in the room: a readable copy of {rel}", f"the PDF could not be read ({type(err).__name__})",
                                    f"a text PDF of {rel}", "customers"))
    _CACHE[key] = out
    return out
