"""Build a draft memo from a readout, in MEMO_TEMPLATE.md's sections.

    build_memo(readout, room_dir) -> Memo (version 1)

Every line Tricorder writes here comes from the readout: a claim, a piece, a
top flag, a gap, a checklist coverage row or an ask item. Nothing is
invented. Where the readout has nothing for a section, the section gets a gap
line that names what is missing: a document not in the room, or a part of the
readout (a scan, a merge step) not built or not run yet.

The quote checker runs again on every claim first. A claim that fails it
moves to the "could not verify" box in section 14 and no line cites it.
"""

from __future__ import annotations

import csv
import importlib.util
import re
from collections import Counter
from pathlib import Path

from schema.check_quotes import check_claim
from schema.claim import Claim, Gap, Readout
from schema.readers import LocatorError, text_at
from scans.memo import checklist as cl

from memo.model import ChangeEntry, ChecklistRef, GapRef, Memo, MemoLine, MemoSection, SourceText, source_key
from memo.template import (
    BY_NUMBER, ENTRY_SECTION, FOLDER_SECTION, LABEL_SECTION, LABEL_WORDS, PIECE_SECTION, PIECE_WORDS,
    SECTIONS, STAGE_WORDS, VERDICT_WORDS, Section, scans_for,
)

SOURCE_TEXT_LIMIT = 6000
OPERATOR = "[the operator]"


# Small readers over the readout ---------------------------------------------


def _panel(readout: Readout, name: str):
    for p in readout.panels:
        if p.name == name:
            return p
    return None


def _counts(readout: Readout) -> dict[str, str]:
    p = _panel(readout, "checklist coverage counts")
    return {r[0]: r[1] for r in p.rows} if p else {}


def step_built(name: str) -> bool:
    """Whether the merge step scans/memo/<name>.py exists in this checkout."""
    return importlib.util.find_spec(f"scans.memo.{name}") is not None


def _entry_for_check(name: str) -> str | None:
    name = cl.check_names(name)
    for entry, names in cl.ENTRY_CHECKS.items():
        if name in names:
            return entry
    return None


def claim_section(claim: Claim, piece_of: dict[str, str]) -> int:
    """The body section a claim belongs to: its piece, else its value's label, else its FRAMEWORKS entry, else its folder."""
    if claim.id in piece_of:
        return PIECE_SECTION[piece_of[claim.id]]
    if claim.value and claim.value.label in LABEL_SECTION:
        return LABEL_SECTION[claim.value.label]
    entry = _entry_for_check(claim.check.name)
    if entry in ENTRY_SECTION:
        return ENTRY_SECTION[entry]
    folder = claim.sources[0].uri.split("/")[0]
    return FOLDER_SECTION.get(folder, 7)


_MISSING_SCAN = re.compile(r"^Not in the room: the (\w+) scan's results$")


def missing_scan(gap: Gap) -> str | None:
    """The scan name, when the merge wrote this gap for a scan that did not run."""
    m = _MISSING_SCAN.match(gap.what)
    return m.group(1) if m and gap.piece is None else None


def _sentence(text: str) -> str:
    text = text.strip()
    text = text[:1].upper() + text[1:]
    return text if text.endswith((".", "?", "!")) else text + "."


def _company(room: str) -> str:
    base = re.sub(r"_(seed_drop|clean.*)$", "", room)
    return " ".join(w.capitalize() for w in base.split("_"))


def _checklist_meta() -> dict[str, dict]:
    with open(cl.CHECKLIST_CSV, newline="", encoding="utf-8") as fh:
        return {r["id"]: r for r in csv.DictReader(fh)}


def _split(text: str) -> list[str]:
    return [t.strip() for t in (text or "").split(";") if t.strip()]


# The builder ---------------------------------------------------------------


class _Builder:
    def __init__(self, readout: Readout, room_dir: Path, built_at: str):
        self.r = readout
        self.room_dir = Path(room_dir)
        self.built_at = built_at
        self.claims: dict[str, Claim] = {}
        self.unverified: list[tuple[Claim, list[str]]] = [(c, ["moved to the box by the merge"]) for c in readout.unverified]
        self.counts = _counts(readout)
        self.stage = self.counts.get("stage")
        self.piece_of = {cid: p.name for p in readout.pieces for cid in p.claim_ids}
        self.pieces_built = step_built("pieces")
        self.flags_built = step_built("top_flags")
        self.coverage_rows = {}
        cov = _panel(readout, "checklist coverage")
        meta = _checklist_meta()
        if cov:
            for row in cov.rows:
                rec = dict(zip(cov.columns, row))
                m = meta.get(rec["id"], {})
                self.coverage_rows[rec["id"]] = ChecklistRef(
                    id=rec["id"], item=rec["item"], piece=rec["piece"], expected=rec["expected"],
                    status=rec["status"], detail=rec["detail"],
                    named_by=_split(m.get("named_by", "")), named_by_urls=_split(m.get("named_by_urls", "")))
        self.asks = {f"ask-{i:02d}": a for i, a in enumerate(readout.asks, 1)}

    # Quote check ----------------------------------------------------------

    def verify(self) -> None:
        for claim in self.r.claims:
            checked, problems = check_claim(claim, self.room_dir)
            if problems:
                self.unverified.append((checked, problems))
            else:
                self.claims[claim.id] = claim

    # Line helpers -------------------------------------------------------

    def claim_line(self, sid: str, claim: Claim, label: str | None = None) -> MemoLine:
        kind = "reading" if claim.confidence == "judged" else "claim"
        if label is None and claim.value and LABEL_WORDS.get(claim.value.label):
            label = LABEL_WORDS[claim.value.label]
        return MemoLine(id=f"{sid}-{claim.id}", kind=kind, text=claim.text, label=label,
                        claim_ids=[claim.id], ask_ids=self.asks_for_claim(claim.id),
                        severity=claim.severity)

    def asks_for_claim(self, claim_id: str) -> list[str]:
        return [aid for aid, a in self.asks.items() if claim_id in a.claim_ids]

    def asks_for_gap(self, gap: Gap) -> list[str]:
        need = gap.would_need.strip().lower()
        return [aid for aid, a in self.asks.items()
                if a.what.strip().lower() == need or (a.from_kind == "gap" and a.why == gap.what)]

    def gap_line(self, lid: str, gap: Gap) -> MemoLine:
        scan = missing_scan(gap)
        missing_from = "readout" if scan else "room"
        text = f"Not in the readout yet: the {scan} scan's results ({gap.why})." if scan else gap.what
        return MemoLine(id=lid, kind="gap", text=text,
                        gap=GapRef(what=gap.what, why=gap.why, would_need=gap.would_need, missing_from=missing_from),
                        checklist_ids=cl.items_for_gap(gap), ask_ids=self.asks_for_gap(gap))

    def readout_gap(self, lid: str, text: str, why: str, would_need: str) -> MemoLine:
        return MemoLine(id=lid, kind="gap", text=text,
                        gap=GapRef(what=text, why=why, would_need=would_need, missing_from="readout"))

    def slot(self, lid: str, text: str) -> MemoLine:
        return MemoLine(id=lid, kind="slot", text=text)

    def coverage_line(self, sec: Section) -> MemoLine | None:
        sid = f"s{sec.number:02d}"
        if not self.coverage_rows:
            return self.readout_gap(f"{sid}-coverage", "Not in the readout yet: checklist coverage.",
                                    "the merge's coverage step did not write its panel", f"python -m scans.memo {self.room_dir}")
        rows = [self.coverage_rows[c] for c in sec.checklist if c in self.coverage_rows]
        if not rows:
            return None
        c = Counter(r.status for r in rows)
        parts = [f"{c[k]} {w}" for k, w in (("checked", "checked"), ("found", "found"), ("missing", "missing"),
                                             ("not_checked", "not checked yet"), ("not_expected", "not expected")) if c[k]]
        stage = STAGE_WORDS.get(self.stage or "", self.stage or "the company's stage")
        return MemoLine(id=f"{sid}-coverage", kind="coverage", label="Checklist",
                        text=f"At {stage}, this section's {len(rows)} checklist items: {', '.join(parts)}.",
                        checklist_ids=[r.id for r in rows])

    def pieces_line(self, sec: Section) -> MemoLine | None:
        sid = f"s{sec.number:02d}"
        if not sec.pieces:
            return None
        if not self.r.pieces:
            why = "the merge's pieces step is not built yet" if not self.pieces_built else "the pieces step wrote no pieces"
            return self.readout_gap(f"{sid}-pieces", f"Not in the readout yet: the verdict for {self._piece_list(sec.pieces)}.",
                                    why, "the pieces step in scans/memo (FRAMEWORKS, \"Piece verdicts\")")
        parts, ids = [], []
        for p in self.r.pieces:
            if p.name in sec.pieces:
                parts.append(f"{PIECE_WORDS[p.name]}, {VERDICT_WORDS[p.verdict]} "
                             f"({p.corroborating_sources} corroborate, {p.contradicting_sources} contradict)")
                ids += [cid for cid in p.claim_ids if cid in self.claims and cid not in ids]
        if not parts:
            return None
        return MemoLine(id=f"{sid}-pieces", kind="pieces", label="Pieces", text=". ".join(parts) + ".", claim_ids=ids)

    @staticmethod
    def _piece_list(pieces) -> str:
        words = [PIECE_WORDS[p].lower() for p in pieces]
        return words[0] if len(words) == 1 else ", ".join(words[:-1]) + " and " + words[-1]

    def missing_scan_lines(self, sec: Section) -> list[MemoLine]:
        out = []
        for i, g in enumerate(self.r.gaps):
            scan = missing_scan(g)
            if scan:
                if scan in scans_for(sec):
                    out.append(self.gap_line(f"s{sec.number:02d}-scan-{scan}", g))
        return out

    def room_gap_lines(self, number: int) -> list[MemoLine]:
        return [self.gap_line(f"s{number:02d}-gap-{i:02d}", g) for i, g in enumerate(self.r.gaps, 1)
                if g.piece and PIECE_SECTION.get(g.piece) == number]

    def claims_with_label(self, *labels: str) -> list[Claim]:
        return [c for c in self.claims.values() if c.value and c.value.label in labels]

    # Sections -------------------------------------------------------------

    def header(self, sec: Section) -> list[MemoLine]:
        company = _company(self.r.room)
        lines = [MemoLine(id="s01-to", kind="fact", label="To", text="Partners"),
                 self.slot("s01-from", f"From: {OPERATOR}. The operator signs the memo."),
                 MemoLine(id="s01-date", kind="fact", label="Date", text=self.built_at[:10])]
        re_line = company
        if self.stage:
            re_line += f", {STAGE_WORDS.get(self.stage, self.stage)}"
        src = self.counts.get("stage_source")
        lines.append(MemoLine(id="s01-re", kind="fact", label="Re",
                              text=re_line + (f". Stage read from {src.split(':')[0]}." if src else ".")))
        raise_claims = self.claims_with_label("raise_amount", "pre_money", "post_money")
        if raise_claims:
            lines += [self.claim_line("s01", c) for c in raise_claims]
        else:
            lines.append(self.readout_gap("s01-raise", "Not in the readout yet: the raise and the pre-money valuation.",
                                          "no claim in the readout is labelled raise_amount or pre_money",
                                          "a claim from the pitch itself piece (FRAMEWORKS 1.10, the cap table reconciliation)"))
        periods = sorted(c.value.period for c in self.claims.values() if c.value and c.value.period and re.fullmatch(r"\d{4}-\d{2}", c.value.period))
        if periods:
            lines.append(MemoLine(id="s01-asof", kind="fact", label="Room data",
                                  text=f"The latest month the claims cover is {periods[-1]}."))
        lines.append(MemoLine(id="s01-version", kind="fact", label="Version", text="Shared version 1."))
        if self.r.synthetic_notice:
            lines.append(MemoLine(id="s01-synthetic", kind="fact", label="Synthetic", text=self.r.synthetic_notice))
        return lines

    def summary(self, sec: Section) -> list[MemoLine]:
        lines: list[MemoLine] = []
        about = [c for c in self.claims.values() if _entry_for_check(c.check.name) == "1.1"]
        if about:
            lines += [self.claim_line("s02", c) for c in about[:3]]
        else:
            lines.append(self.readout_gap("s02-about", "Not in the readout yet: what the company does and what it is raising, in its own words.",
                                          "the claims scan (FRAMEWORKS 1.1, deck and overview claims) has not run",
                                          f"python -m scans.claims {self.room_dir}"))
        lines.append(self.slot("s02-recommendation", "Recommendation: [the operator writes this]."))
        ran, missing = self.r.scans_run, self.r.scans_missing
        if missing:
            lines.append(self.readout_gap(
                "s02-scans", f"Not in the readout yet: {len(missing)} of {len(ran) + len(missing)} scans. "
                f"Built from {', '.join(ran) or 'no scan'}. Not run: {', '.join(missing)}. The flags below are the ones found so far.",
                "the scans have not run on this room, or are not built yet", "the missing scans' results"))
        if self.r.top_flags:
            for f in sorted(self.r.top_flags, key=lambda f: (f.kind != "green", f.rank)):
                ids = [c for c in f.claim_ids if c in self.claims]
                if not ids:
                    continue
                word = "Green flag" if f.kind == "green" else "Red flag"
                text = f.text
                label = None if text.lower().startswith(word.lower()) else word
                lines.append(MemoLine(id=f"s02-{f.kind}-{f.rank}", kind="claim", label=label, text=text,
                                      claim_ids=ids, severity=f.kind))
            if not any(f.kind == "green" for f in self.r.top_flags) and self.r.pieces:
                lines.append(MemoLine(id="s02-no-green", kind="fact",
                                      text="No green flag: nothing in the room is corroborated and uncontradicted."))
        else:
            why = "the merge's top_flags step is not built yet" if not self.flags_built else "the top_flags step wrote no flags"
            lines.append(self.readout_gap("s02-flags", "Not in the readout yet: the top green and red flags.", why,
                                          "the top_flags step in scans/memo (FRAMEWORKS, \"Top green and red flags\")"))
            flagged = [c for c in self.claims.values() if c.severity == "flag"]
            for c in flagged:
                lines.append(self.claim_line("s02-flag", c, label=f"Flag: {LABEL_WORDS.get(c.value.label, '') if c.value else ''}".rstrip(": ")))
        if self.r.pieces:
            for p in self.r.pieces:
                ids = [c for c in p.claim_ids if c in self.claims]
                lines.append(MemoLine(id=f"s02-piece-{p.name}", kind="pieces",
                                      label=f"{PIECE_WORDS[p.name]}: {VERDICT_WORDS[p.verdict]}",
                                      text=f"{p.reason} {p.corroborating_sources} sources corroborate, {p.contradicting_sources} contradict.",
                                      claim_ids=ids, severity={"looking_strong": "green", "looking_weak": "red"}.get(p.verdict)))
        else:
            why = "the merge's pieces step is not built yet" if not self.pieces_built else "the pieces step wrote no pieces"
            lines.append(self.readout_gap("s02-pieces", "Not in the readout yet: the nine pieces at a glance.", why,
                                          "the pieces step in scans/memo (FRAMEWORKS, \"Piece verdicts\")"))
        return lines

    def body(self, sec: Section, routed: list[Claim]) -> list[MemoLine]:
        sid = f"s{sec.number:02d}"
        lines: list[MemoLine] = []
        opener = self.pieces_line(sec)
        if opener:
            lines.append(opener)
        lines += [self.claim_line(sid, c) for c in routed]
        lines += self.room_gap_lines(sec.number)
        lines += self.missing_scan_lines(sec)
        if not routed and not any(ln.kind == "gap" and ln.id.startswith(f"{sid}-scan") for ln in lines) and not self.room_gap_lines(sec.number):
            lines.append(self.readout_gap(f"{sid}-empty", f"Not in the readout yet: any claim for {sec.title.lower()}.",
                                          "no scan that has run writes a claim for this section",
                                          ", ".join(f"FRAMEWORKS {e}" for e in sec.entries) or "a scan for this section"))
        if sec.number == 9:
            lines.append(self.slot("s09-view", "The operator's view of the founders: [the operator writes this]."))
        if sec.number == 11:
            lines.append(self.slot("s11-price", "Whether the price is right: [the operator writes this]."))
        closer = self.coverage_line(sec)
        if closer:
            lines.append(closer)
        return lines

    def risks(self, sec: Section) -> list[MemoLine]:
        lines = []
        for c in self.claims.values():
            if c.severity == "flag":
                label = LABEL_WORDS.get(c.value.label, "") if c.value else ""
                ln = self.claim_line("s12", c, label=label or "Flag")
                if not ln.ask_ids:
                    ln.text += " Settled by: no line on the ask list names this claim yet; ask the founder to walk from the source data to this number (C71)."
                lines.append(ln)
        for p in self.r.pieces:
            if p.verdict in ("looking_weak", "mixed"):
                ids = [cid for cid in p.reason_claim_ids if cid in self.claims]
                lines.append(MemoLine(id=f"s12-piece-{p.name}", kind="pieces",
                                      label=f"{PIECE_WORDS[p.name]}: {VERDICT_WORDS[p.verdict]}", text=p.reason, claim_ids=ids))
        lines += [ln.model_copy(update={"id": ln.id.replace("s", "s12-from-s", 1)})
                  for n in (7, 6, 10, 11, 9, 8, 4) for ln in self.room_gap_lines(n)]
        lines.append(self.slot("s12-rank", "The operator ranks these risks and adds their own: [the operator writes this]."))
        if not any(ln.kind in ("claim", "reading", "pieces", "gap") for ln in lines):
            lines.insert(0, self.readout_gap("s12-empty", "Not in the readout yet: any flag, weak piece or gap.",
                                             "no claim with severity flag, no weak or mixed piece and no gap", "the scans' results"))
        return lines

    def outcomes(self, sec: Section) -> list[MemoLine]:
        lines = [self.slot("s13-cases", "Downside, base and upside cases: [the operator writes these]. Tricorder supplies only the facts they rest on, below.")]
        facts = self.claims_with_label("raise_amount", "pre_money", "runway_months")
        lines += [self.claim_line("s13", c) for c in facts]
        have = {c.value.label for c in facts}
        missing = [w for lab, w in (("raise_amount", "the round"), ("runway_months", "the runway with the hiring plan")) if lab not in have]
        if missing or "comps" in self.r.scans_missing:
            parts = missing + (["the comps"] if "comps" in self.r.scans_missing else [])
            lines.append(self.readout_gap("s13-facts", f"Not in the readout yet: {', '.join(parts)}, which the cases rest on.",
                                          "no claim with those labels, or the comps scan has not run",
                                          "claims labelled raise_amount and runway_months; the comps scan"))
        return lines

    def diligence(self, sec: Section) -> list[MemoLine]:
        lines: list[MemoLine] = []
        if self.coverage_rows:
            c = Counter(r.status for r in self.coverage_rows.values())
            stage = STAGE_WORDS.get(self.stage or "", self.stage or "the company's stage")
            lines.append(MemoLine(id="s14-coverage", kind="coverage", label="Coverage",
                                  text=f"At {stage}, {len(self.coverage_rows)} checklist items: {c['checked']} checked, {c['found']} found, "
                                       f"{c['missing']} missing, {c['not_checked']} not checked yet, {c['not_expected']} not expected.",
                                  checklist_ids=sorted(self.coverage_rows)))
            for status, word in (("checked", "Checked"), ("found", "Found, not checked yet by a script"), ("missing", "Missing")):
                ids = [r.id for r in self.coverage_rows.values() if r.status == status]
                if ids:
                    lines.append(MemoLine(id=f"s14-coverage-{status}", kind="coverage", label=word,
                                          text=f"{len(ids)} items: " + "; ".join(self.coverage_rows[i].item for i in ids[:6])
                                               + ("; and more." if len(ids) > 6 else "."),
                                          checklist_ids=ids))
        else:
            lines.append(self.readout_gap("s14-coverage", "Not in the readout yet: checklist coverage.",
                                          "the merge's coverage step did not write its panel", f"python -m scans.memo {self.room_dir}"))
        if self.asks:
            for aid, a in self.asks.items():
                feeds = BY_NUMBER[PIECE_SECTION.get(a.piece, 11)].title
                lines.append(MemoLine(id=f"s14-{aid}", kind="ask", label="If you have it" if a.if_you_have_it else None,
                                      text=f"{_sentence(a.what)} Why: {_sentence(a.why)} Feeds: {feeds}.",
                                      claim_ids=[c for c in a.claim_ids if c in self.claims],
                                      checklist_ids=[a.checklist_id] if a.checklist_id else [], ask_ids=[aid]))
        else:
            lines.append(self.readout_gap("s14-asks", "Not in the readout yet: the ask list.",
                                          "the merge's asks step wrote no ask items", "the asks step in scans/memo"))
        for claim, problems in self.unverified:
            lines.append(MemoLine(id=f"s14-unverified-{claim.id}", kind="unverified", label="Could not verify",
                                  text=f"{claim.text} The quote checker did not find its quote: {'; '.join(problems)}"))
        if not self.unverified:
            lines.append(MemoLine(id="s14-unverified-none", kind="fact", label="Could not verify",
                                  text="None. Every claim's quote was found again at its source when this memo was exported."))
        return lines

    def sources_section(self, cited: set[str]) -> list[MemoLine]:
        by_key: dict[str, list[str]] = {}
        meta: dict[str, tuple[str, str, str | None]] = {}
        for cid in sorted(cited):
            for s in self.claims[cid].sources:
                k = source_key(s.uri, s.locator)
                by_key.setdefault(k, []).append(cid)
                meta[k] = (s.uri, s.locator, s.retrieved_at)
        lines = []
        for i, (k, ids) in enumerate(sorted(by_key.items()), 1):
            uri, loc, at = meta[k]
            lines.append(MemoLine(id=f"s16-src-{i:03d}", kind="source", text=f"{uri}, {loc}" + (f", read {at}" if at else ""),
                                  claim_ids=sorted(set(ids))))
        return lines

    # Assemble -------------------------------------------------------------

    def build(self) -> Memo:
        self.verify()
        routed: dict[int, list[Claim]] = {}
        for c in self.claims.values():
            routed.setdefault(claim_section(c, self.piece_of), []).append(c)
        sections = []
        for sec in SECTIONS:
            n = sec.number
            if n == 1:
                lines = self.header(sec)
            elif n == 2:
                lines = self.summary(sec)
            elif n == 12:
                lines = self.risks(sec)
            elif n == 13:
                lines = self.outcomes(sec)
            elif n == 14:
                lines = self.diligence(sec)
            elif n == 15:
                lines = [self.slot("s15-recommendation", "Invest, pass or wait; the amount and any conditions; the two reasons that decide it, "
                                                         "and why it could be wrong: [the operator writes this].")]
            elif n == 16:
                lines = []
            else:
                lines = self.body(sec, routed.get(n, []))
            sections.append(MemoSection(number=n, key=sec.key, title=sec.title, who_writes=sec.who_writes, lines=lines))
        cited = {cid for s in sections for ln in s.lines for cid in ln.claim_ids}
        # A claim the drill-down opens through corroborated_by or conflicts_with is carried too.
        for cid in list(cited):
            cited |= {x for x in self.claims[cid].corroborated_by + self.claims[cid].conflicts_with if x in self.claims}
        sections[-1].lines = self.sources_section(cited) + [
            MemoLine(id="s16-change-1", kind="change", label="Version 1",
                     text=f"Drafted by Tricorder from the readout built {self.r.built_at}.")]
        for s in sections:
            s.empty_because = empty_because(s)
        memo = Memo(room=self.r.room, company=_company(self.r.room), readout_built_at=self.r.built_at,
                    built_at=self.built_at, version=1, synthetic_notice=self.r.synthetic_notice, sections=sections,
                    claims={cid: self.claims[cid] for cid in sorted(cited)},
                    asks=self.asks, checklist=self.coverage_rows, stage=self.stage,
                    changes=[ChangeEntry(version=1, at=self.built_at, author="Tricorder",
                                         what=f"Drafted from the readout built {self.r.built_at}.")])
        memo.sources = read_sources(memo, self.room_dir)
        return memo


def empty_because(section: MemoSection) -> list[str]:
    """When a section holds nothing Tricorder could source, the gap lines that say why."""
    filled = any(ln.kind in ("claim", "reading", "pieces", "ask", "operator", "source") or
                 (ln.kind == "coverage" and section.number == 14) or
                 (ln.kind == "fact" and section.number == 1) for ln in section.lines)
    if filled:
        return []
    return [ln.text for ln in section.lines if ln.kind == "gap"]


def read_sources(memo: Memo, room_dir: Path) -> dict[str, SourceText]:
    """The text at every cited source's locator, so the page opens it offline."""
    out = {}
    for claim in memo.claims.values():
        for s in claim.sources:
            k = source_key(s.uri, s.locator)
            if k in out:
                continue
            try:
                text = text_at(s, room_dir)
            except (LocatorError, OSError) as err:
                out[k] = SourceText(key=k, text=f"Could not open this source: {err}", found=False)
                continue
            out[k] = SourceText(key=k, text=_window(text, s.quote), found=True)
    return out


def _window(text: str, quote: str) -> str:
    if len(text) <= SOURCE_TEXT_LIMIT:
        return text
    at = text.lower().find(quote.lower()[:40])
    start = max(0, at - SOURCE_TEXT_LIMIT // 2) if at >= 0 else 0
    return ("..." if start else "") + text[start:start + SOURCE_TEXT_LIMIT] + "..."


def build_memo(readout: Readout, room_dir: str | Path, built_at: str) -> Memo:
    return _Builder(readout, Path(room_dir), built_at).build()
