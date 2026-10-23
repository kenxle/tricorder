"""Build a draft memo from a readout, in MEMO_TEMPLATE.md's sections.

    build_memo(readout, room_dir, built_at) -> Memo (version 1)

Every line Tricorder writes comes from the readout: a claim, a piece, a top
flag, a gap, a checklist coverage row or an ask item, or a sentence composed
only from claims' values and sources (memo/compose.py). Nothing is invented.

The memo opens with the answer: section 2 starts with the flags, in full, then
one line per piece, then what the company does. A flag is shown in full once,
in section 2; the sections it belongs to and the risks refer to it. A section
with nothing assessed is one line naming what it needs. Plumbing (blanks,
one-by-one ask lines, commands) is for the operator view only.

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

from memo.compose import arr_side_by_side
from memo.model import ChangeEntry, ChecklistRef, GapRef, Memo, MemoLine, MemoSection, SourceText, source_key
from memo.sources import fmt_number, reads_as
from memo.template import (
    BY_NUMBER, ENTRY_SECTION, FOLDER_SECTION, LABEL_SECTION, LABEL_WORDS, PIECE_SECTION, PIECE_WORDS,
    SECTIONS, STAGE_WORDS, VERDICT_WORDS, Section, scans_for,
)

SOURCE_TEXT_LIMIT = 6000

# What each scan assesses, in a partner's words.
SCAN_WORDS = {
    "redflags": "red-flag checks", "comps": "comps", "signals": "market signals", "video": "pitch video",
    "claims": "deck claims", "readings": "contract readings", "model": "financial model rebuild",
    "frameworks": "business frameworks", "founders": "founder profiles", "presence": "online presence",
    "bank": "bank check", "outside": "outside-in research",
}

# A flag's title, by its check, in under ten words (BRAND.md, "A green flag and a red flag").
FLAG_TITLES = {
    "mrr_column_vs_subscription_rows": "MRR counts a pilot as recurring",
    "cancellable_within_notice_vs_arr": "A contract the customer can end soon is counted as a year of ARR",
    "pilot_without_duty_to_convert_vs_recurring": "A pilot with no duty to convert is counted as recurring",
    "plan_revenue_past_term_end": "The plan keeps revenue after a contract ends",
    "signed_not_live_vs_revenue": "Revenue counted before the contract went live",
    "counted_line_without_contract": "Counted revenue with no contract behind it",
    "deck_revenue_vs_pnl": "The deck's revenue differs from the books",
    "deck_history_vs_metrics": "The deck's chart leaves out part of the history",
    "gross_margin_from_ledger": "Gross margin leaves out delivery costs",
    "top_customer_share": "One customer is a large share of revenue",
    "payroll_from_hiring_plan_and_rerun_cash": "Runway leaves out the hiring plan",
    "cumulative_column_shown_as_active": "Sign-ups shown as active customers",
}

# Sentences that describe how a script worked, not what the room shows. The operator view keeps them.
_PLUMBING = re.compile(r"[^.]*(?:scans/|\.py\b|Mislabel kind|\b[a-z]+(?:_[a-z0-9]+){2,}\b)[^.]*\.\s*")
# "the redflags scan's rebuild_cohorts_from_customer_file check" names a script; a partner reads "a check on the room".
# "(C34)" after a document names its checklist row; the drill shows the row itself.
_CHECK_REF = re.compile(r"\s*\((?:C\d\d(?:,\s*|\s+and\s+)?)+\)")
_CHECK_NAME = re.compile(r"\bthe \w+ scan's [a-z0-9_]+ check\b")


def partner_text(text: str) -> str:
    """A claim's sentence without the sentences about the script that made it."""
    out = _PLUMBING.sub("", _CHECK_REF.sub("", _CHECK_NAME.sub("a check on the room", text))).strip()
    return out or text


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


def _and(words: list[str]) -> str:
    return words[0] if len(words) == 1 else ", ".join(words[:-1]) + " and " + words[-1]


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
        self.coverage_rows: dict[str, ChecklistRef] = {}
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
        # Flags shown in full in section 2: (line id, title, claim ids). Filled by summary().
        self.flag_lines: list[tuple[str, str, list[str]]] = []
        # The claims scan's verdict on each pitch claim (supported, unsupported, contradicted) and what it is about.
        self.pitch: dict[str, tuple[str, str]] = {}
        table = _panel(readout, "claims table")
        if table and "claim id" in table.columns:
            for row in table.rows:
                rec = dict(zip(table.columns, row))
                self.pitch[rec["claim id"]] = (str(rec.get("label", "")).lower(), str(rec.get("kind", "")))

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
        return MemoLine(id=f"{sid}-{claim.id}", kind=kind, text=partner_text(claim.text), label=label,
                        claim_ids=[claim.id], ask_ids=self.asks_for_claim(claim.id), severity=claim.severity)

    def is_pitch(self, claim: Claim) -> bool:
        """A figure from the pitch, checked against the room by the claims scan."""
        return claim.id in self.pitch or claim.check.name == "claim_support"

    def pitch_verdict(self, claim: Claim) -> str:
        if claim.id in self.pitch:
            return self.pitch[claim.id][0]
        return claim.text.split(":", 1)[0].strip().lower()

    def pitch_lines(self, sid: str, claims: list[Claim]) -> list[MemoLine]:
        """The pitch's claims for a section as one partner line, with each claim behind it.
        The claims' own lines stay in the operator view, so a room with 60 pitch claims reads in a few lines."""
        if not claims:
            return []
        by = {"supported": [], "unsupported": [], "contradicted": []}
        for c in claims:
            by.setdefault(self.pitch_verdict(c), []).append(c)
        what = []
        for c in by["unsupported"]:
            w = (self.pitch.get(c.id, ("", ""))[1] or LABEL_WORDS.get(c.value.label if c.value else "", "")).strip()
            if w and w.lower() not in [x.lower() for x in what]:
                what.append(w)
        n = len(claims)
        k = len(by["supported"])
        parts = [f"{k} {'matches' if k == 1 else 'match'} the room"] if k else []
        if by["unsupported"]:
            u = len(by["unsupported"])
            parts.append(f"{u} {'has' if u == 1 else 'have'} nothing in the room to check against"
                         + (f" ({_and(what[:6])}{' and more' if len(what) > 6 else ''})" if what else ""))
        others = n - len(by["supported"]) - len(by["unsupported"])
        if others:
            parts.append(f"{others} {'disagrees' if others == 1 else 'disagree'} with it")
        summary = MemoLine(id=f"{sid}-pitch", kind="claim", label="The pitch's figures",
                           text=f"{n} figure{'s' if n != 1 else ''} from the pitch: " + "; ".join(parts) + ".",
                           claim_ids=[c.id for c in claims])
        return [summary] + [self.claim_line(sid, c).model_copy(update={"audience": "operator"}) for c in claims]

    def asks_for_claim(self, claim_id: str) -> list[str]:
        return [aid for aid, a in self.asks.items() if claim_id in a.claim_ids]

    def asks_for_gap(self, gap: Gap) -> list[str]:
        need = gap.would_need.strip().lower()
        return [aid for aid, a in self.asks.items()
                if a.what.strip().lower() == need or (a.from_kind == "gap" and a.why == gap.what)]

    def gap_line(self, lid: str, gap: Gap) -> MemoLine:
        return MemoLine(id=lid, kind="gap", text=gap.what,
                        gap=GapRef(what=gap.what, why=gap.why, would_need=gap.would_need, missing_from="room"),
                        checklist_ids=cl.items_for_gap(gap), ask_ids=self.asks_for_gap(gap))

    def readout_gap(self, lid: str, text: str, why: str, would_need: str, audience: str = "all") -> MemoLine:
        return MemoLine(id=lid, kind="gap", text=text, audience=audience,
                        gap=GapRef(what=text, why=why, would_need=would_need, missing_from="readout"))

    def slot(self, lid: str, text: str) -> MemoLine:
        return MemoLine(id=lid, kind="slot", text=text, audience="operator")

    def flag_ref(self, sid: str, claim_id: str) -> MemoLine | None:
        """A pointer to the section 2 flag that shows this flag claim in full. Other claims keep their own line."""
        if self.claims[claim_id].severity != "flag":
            return None
        for n, (lid, title, ids) in enumerate(self.flag_lines, 1):
            if claim_id in ids:
                return MemoLine(id=f"{sid}-ref-{lid}", kind="ref", label=f"Red flag {n}",
                                text=f"{title}. Shown in full in the summary.", claim_ids=list(ids), severity="flag")
        return None

    def coverage_line(self, sec: Section, audience: str = "all") -> MemoLine | None:
        sid = f"s{sec.number:02d}"
        if not self.coverage_rows:
            return self.readout_gap(f"{sid}-coverage", "Checklist coverage: not assessed yet.",
                                    "the merge's coverage step did not write its panel", f"python -m scans.memo {self.room_dir}",
                                    audience="operator")
        rows = [self.coverage_rows[c] for c in sec.checklist if c in self.coverage_rows]
        if not rows:
            return None
        c = Counter(r.status for r in rows)
        parts = [f"{c[k]} {w}" for k, w in (("checked", "checked"), ("found", "found"), ("missing", "missing"),
                                             ("not_checked", "not checked yet"), ("not_expected", "not expected")) if c[k]]
        stage = STAGE_WORDS.get(self.stage or "", self.stage or "the company's stage")
        return MemoLine(id=f"{sid}-coverage", kind="coverage", label="Checklist", audience=audience,
                        text=f"At {stage}, this section's {len(rows)} checklist items: {', '.join(parts)}.",
                        checklist_ids=[r.id for r in rows])

    def pieces_line(self, sec: Section) -> MemoLine | None:
        """A section's opening line, when the pieces step has placed verdicts. Said once in section 2 otherwise."""
        sid = f"s{sec.number:02d}"
        parts, ids = [], []
        for p in self.r.pieces:
            if p.name in sec.pieces:
                parts.append(f"{PIECE_WORDS[p.name]}, {VERDICT_WORDS[p.verdict]} "
                             f"({p.corroborating_sources} corroborate, {p.contradicting_sources} contradict)")
                ids += [cid for cid in p.claim_ids if cid in self.claims and cid not in ids]
        if not parts:
            return None
        return MemoLine(id=f"{sid}-pieces", kind="pieces", label="Pieces", text=". ".join(parts) + ".", claim_ids=ids)

    def missing_scans(self, sec: Section) -> list[str]:
        missing = {missing_scan(g) for g in self.r.gaps} - {None}
        return [s for s in scans_for(sec) if s in missing]

    def needs_line(self, sec: Section, lid: str, lead: str | None) -> MemoLine | None:
        """'Market: not assessed yet. Needs the ... scans.' With no lead, the line for a section that is partly assessed."""
        scans = self.missing_scans(sec)
        if not scans:
            return None
        words = _and([SCAN_WORDS.get(s, s) for s in scans])
        noun = "scan" if len(scans) == 1 else "scans"
        text = f"{lead}: not assessed yet. Needs the {words} {noun}." if lead else f"Not assessed here yet: the {words} {noun}."
        return self.readout_gap(lid, text,
                                "; ".join(f"the {s} scan has not run on this room" for s in scans),
                                "; ".join(f"python -m scans.{s} {self.room_dir}" for s in scans))

    def room_gap_lines(self, number: int) -> list[MemoLine]:
        """The room's gaps for a section, each once. Gaps that differ only in what follows ' for ' share one line."""
        groups: dict[str, list[tuple[int, Gap]]] = {}
        for i, g in enumerate(self.r.gaps, 1):
            if g.piece and PIECE_SECTION.get(g.piece) == number:
                key = g.what.rsplit(" for ", 1)[0] if " for " in g.what else g.what
                if all(g.what != h.what for _, h in groups.get(key, [])):
                    groups.setdefault(key, []).append((i, g))
        out = []
        for key, items in groups.items():
            i, first = items[0]
            line = self.gap_line(f"s{number:02d}-gap-{i:02d}", first)
            if len(items) > 1:
                names = [g.what.rsplit(" for ", 1)[1] for _, g in items]
                line.text = f"{key} for each of these {len(items)}: " + "; ".join(names) + "."
                line.gap.what = line.text
                line.gap.would_need = first.would_need + f" The same for each of the {len(items)}."
                for _, g in items[1:]:
                    line.checklist_ids += [c for c in cl.items_for_gap(g) if c not in line.checklist_ids]
                    line.ask_ids += [a for a in self.asks_for_gap(g) if a not in line.ask_ids]
            out.append(line)
        return out

    def claims_with_label(self, *labels: str) -> list[Claim]:
        return [c for c in self.claims.values() if c.value and c.value.label in labels]

    # Sections -------------------------------------------------------------

    def header(self, sec: Section) -> list[MemoLine]:
        company = _company(self.r.room)
        lines = [MemoLine(id="s01-to", kind="fact", label="To", text="Partners"),
                 self.slot("s01-from", "From: the operator signs the memo here."),
                 MemoLine(id="s01-date", kind="fact", label="Date", text=self.built_at[:10])]
        re_line = company + (f", {STAGE_WORDS.get(self.stage, self.stage)}" if self.stage else "")
        src = self.counts.get("stage_source")
        lines.append(MemoLine(id="s01-re", kind="fact", label="Re", text=re_line + "."))
        if src:
            lines.append(MemoLine(id="s01-stage", kind="fact", label="Stage from", text=src.split(":")[0] + ".", audience="operator"))
        raise_claims = self.claims_with_label("raise_amount", "pre_money", "post_money")
        if raise_claims:
            # One line for the round, from the claims' own figures; each claim stays behind it and in the operator view.
            first: dict[str, Claim] = {}
            for c in raise_claims:
                first.setdefault(c.value.label, c)
            words = {"raise_amount": "raising {}", "pre_money": "at {} pre-money", "post_money": "{} post-money"}
            parts = [words[k].format(fmt_number(str(first[k].value.number), "", "money")) for k in words if k in first]
            lines.append(MemoLine(id="s01-round", kind="claim", label="The round", composed=True,
                                  text=parts[0][0].upper() + parts[0][1:] + "".join(" " + p for p in parts[1:]) + ".",
                                  claim_ids=[c.id for c in raise_claims]))
            lines += [self.claim_line("s01", c).model_copy(update={"audience": "operator"}) for c in raise_claims]
        else:
            # The summary says it for the partners ("what it raises: not assessed yet"); the head keeps it for the operator.
            lines.append(self.readout_gap("s01-raise", "The raise and the pre-money valuation: not assessed yet.",
                                          "no claim in the readout is labelled raise_amount or pre_money",
                                          "a claim from the pitch itself piece (FRAMEWORKS 1.10, the cap table reconciliation)",
                                          audience="operator"))
        periods = sorted(c.value.period for c in self.claims.values()
                         if c.value and c.value.period and re.fullmatch(r"\d{4}-\d{2}", c.value.period))
        if periods:
            lines.append(MemoLine(id="s01-asof", kind="fact", label="Room data",
                                  text=f"The latest month the claims cover is {periods[-1]}."))
        lines.append(MemoLine(id="s01-version", kind="fact", label="Version", text="Shared version 1."))
        if self.r.synthetic_notice:
            lines.append(MemoLine(id="s01-synthetic", kind="fact", label="Synthetic", text=self.r.synthetic_notice))
        return lines

    def flags(self) -> list[MemoLine]:
        """The flags, in full, once. Top flags when that step has run; else every claim with severity flag."""
        lines: list[MemoLine] = []
        if self.r.top_flags:
            for f in sorted(self.r.top_flags, key=lambda f: (f.kind != "green", f.rank)):
                ids = [c for c in f.claim_ids if c in self.claims]
                if not ids:
                    continue
                word = "Green flag" if f.kind == "green" else "Red flag"
                lid = f"s02-{f.kind}-{f.rank}"
                title = re.sub(r"^(green|red) flag:\s*", "", f.text, flags=re.I).split(".")[0]
                lines.append(MemoLine(id=lid, kind="claim", label=None if f.text.lower().startswith(word.lower()) else word,
                                      text=f.text, claim_ids=ids, severity=f.kind))
                if f.kind == "red":
                    self.flag_lines.append((lid, title, ids))
            if not any(f.kind == "green" for f in self.r.top_flags) and self.r.pieces:
                lines.append(MemoLine(id="s02-no-green", kind="fact",
                                      text="No green flag: nothing in the room is corroborated and uncontradicted."))
            return lines
        flagged = [c for c in self.claims.values() if c.severity == "flag"]
        arr = arr_side_by_side(list(self.claims.values()), self.room_dir)
        covered: set[str] = set()
        if arr and any(cid in {c.id for c in flagged} for cid in arr[1]):
            text, ids = arr
            # The figures, short, so the first screen holds the other flags too. Why they differ is each
            # flag's own sentence, one click away.
            why = [i for i in ids if self.claims[i].severity == "flag" and not (self.claims[i].value and self.claims[i].value.label == "arr")]
            if why:
                text += f" Behind this line, {len(why)} check{'s' if len(why) != 1 else ''} on the room say why they differ."
            title = "ARR figures in the room disagree"
            lines.append(MemoLine(id="s02-flag-arr", kind="claim", label=f"Red flag 1: {title}", text=text,
                                  claim_ids=ids, severity="red", composed=True))
            self.flag_lines.append(("s02-flag-arr", title, ids))
            covered = set(ids)
        # One red flag per subject: the deck, the video and a check that say the same thing share a line,
        # in full for the first and behind the line for the rest.
        groups: dict[str, tuple[str, list[Claim]]] = {}
        for c in flagged:
            if c.id in covered:
                continue
            title = FLAG_TITLES.get(cl.check_names(c.check.name)) or LABEL_WORDS.get(c.value.label if c.value else "", "")
            key = title or c.id
            groups.setdefault(key, (title or "Files disagree", []))[1].append(c)
        for title, group in groups.values():
            first = group[0]
            lid = f"s02-flag-{first.id}"
            text = partner_text(first.text)
            if len(group) > 1:
                more = len(group) - 1
                text += f" {more} more claim{'s' if more != 1 else ''} on this, behind this line."
            lines.append(MemoLine(id=lid, kind="claim", label=f"Red flag {len(self.flag_lines) + 1}: {title}",
                                  text=text, claim_ids=[c.id for c in group], severity="red"))
            self.flag_lines.append((lid, title, [c.id for c in group]))
        if not lines:
            lines.append(MemoLine(id="s02-no-flags", kind="fact", text="No red flag in the checks run so far."))
        return lines

    def summary(self, sec: Section) -> list[MemoLine]:
        lines = self.flags()
        # One line per piece with a verdict. The pieces with none share one line, so
        # "not assessed yet" is said once, not nine times.
        by_name = {p.name: p for p in self.r.pieces}
        unassessed = []
        for name in PIECE_WORDS:
            p = by_name.get(name)
            if p:
                ids = [c for c in p.claim_ids if c in self.claims]
                lines.append(MemoLine(id=f"s02-piece-{name}", kind="pieces",
                                      label=f"{PIECE_WORDS[name]}: {VERDICT_WORDS[p.verdict]}",
                                      text=f"{partner_text(p.reason)} {p.corroborating_sources} sources corroborate, {p.contradicting_sources} contradict.",
                                      claim_ids=ids, severity={"looking_strong": "green", "looking_weak": "red"}.get(p.verdict)))
            else:
                unassessed.append(name)
        if unassessed:
            why = "the merge's pieces step is not built yet" if not self.pieces_built else "the pieces step placed no verdict for them"
            words = [PIECE_WORDS[n] for n in unassessed]
            lines.append(MemoLine(id="s02-pieces-unassessed", kind="gap",
                                  label="Verdicts not in yet" if self.r.pieces else "No verdicts yet",
                                  text=_and([words[0]] + [w.lower() for w in words[1:]]) + ".",
                                  gap=GapRef(what=f"Not assessed yet: {_and([w.lower() for w in words])}", why=why,
                                             would_need="the pieces step in scans/memo (FRAMEWORKS, \"Piece verdicts\")",
                                             missing_from="readout")))
        about = [c for c in self.claims.values() if _entry_for_check(c.check.name) == "1.1"]
        if about:
            lines += [self.claim_line("s02", c, label="The company") for c in about[:3]]
        else:
            ln = self.needs_line(BY_NUMBER[3], "s02-about", "What the company does and what it raises")
            lines.append(ln or self.readout_gap("s02-about", "What the company does and what it raises: not assessed yet.",
                                                "no deck claim in the readout", "the claims scan (FRAMEWORKS 1.1)"))
        ran, missing = self.r.scans_run, self.r.scans_missing
        if missing:
            lines.append(MemoLine(id="s02-scans", kind="fact", label="Assessed so far",
                                  text=f"{_and([SCAN_WORDS.get(s, s) for s in ran]) if ran else 'nothing yet'}. "
                                       f"Not yet: {_and([SCAN_WORDS.get(s, s) for s in missing])}."))
        return lines

    def body(self, sec: Section, routed: list[Claim]) -> tuple[list[MemoLine], bool]:
        sid = f"s{sec.number:02d}"
        lines: list[MemoLine] = []
        opener = self.pieces_line(sec)
        if opener:
            lines.append(opener)
        refs: set[str] = set()
        pitch: list[Claim] = []
        for c in routed:
            ref = self.flag_ref(sid, c.id)
            if ref:
                if ref.id not in refs:
                    refs.add(ref.id)
                    lines.append(ref)
            elif self.is_pitch(c):
                pitch.append(c)
            else:
                lines.append(self.claim_line(sid, c))
        lines += self.pitch_lines(sid, pitch)
        gaps = self.room_gap_lines(sec.number)
        lines += gaps
        if not routed and not gaps and not opener:
            needs = self.needs_line(sec, f"{sid}-empty", sec.title) or self.readout_gap(
                f"{sid}-empty", f"{sec.title}: not assessed yet.", "no scan that has run writes a claim for this section",
                ", ".join(f"FRAMEWORKS {e}" for e in sec.entries) or "a scan for this section")
            lines = [needs]
            closer = self.coverage_line(sec, audience="operator")
            if closer:
                lines.append(closer)
            return lines, True
        needs = self.needs_line(sec, f"{sid}-needs", None)
        if needs:
            lines.append(needs)
        if sec.number == 9:
            lines.append(self.slot("s09-view", "The operator's view of the founders."))
        if sec.number == 11:
            lines.append(self.slot("s11-price", "Whether the price is right."))
        closer = self.coverage_line(sec)
        if closer:
            lines.append(closer)
        return lines, False

    def risks(self, sec: Section) -> list[MemoLine]:
        lines = []
        for n, (lid, title, ids) in enumerate(self.flag_lines, 1):
            asks = sorted({a for cid in ids for a in self.asks_for_claim(cid)})
            settle = "" if asks else " Settled by: the founder walking from the source data to these figures."
            lines.append(MemoLine(id=f"s12-ref-{lid}", kind="ref", label=f"Red flag {n}: {title}",
                                  text=f"Shown in full in the summary.{settle}", claim_ids=list(ids), ask_ids=asks, severity="flag"))
        for p in self.r.pieces:
            if p.verdict in ("looking_weak", "mixed"):
                ids = [cid for cid in p.reason_claim_ids if cid in self.claims]
                lines.append(MemoLine(id=f"s12-piece-{p.name}", kind="pieces",
                                      label=f"{PIECE_WORDS[p.name]}: {VERDICT_WORDS[p.verdict]}", text=partner_text(p.reason), claim_ids=ids))
        # The room's gaps sit in their sections; here they are counted once, and listed in the operator view.
        where = []
        for n in (7, 6, 10, 11, 9, 8, 4):
            gaps = self.room_gap_lines(n)
            if gaps:
                where.append(f"{BY_NUMBER[n].title} ({len(gaps)})")
                lines += [ln.model_copy(update={"id": ln.id.replace("s", "s12-from-s", 1), "audience": "operator"}) for ln in gaps]
        if where:
            lines.append(MemoLine(id="s12-gaps", kind="fact", label="Not in the room",
                                  text=f"Documents the room does not hold are listed in their sections: {_and(where)}."))
        lines.append(self.slot("s12-rank", "The operator ranks these risks and adds their own."))
        if not any(ln.kind in ("claim", "reading", "pieces", "gap", "ref") for ln in lines):
            lines.insert(0, self.readout_gap("s12-empty", "Risks: none found in the checks run so far.",
                                             "no claim with severity flag, no weak or mixed piece and no gap", "the scans' results"))
        return lines

    def outcomes(self, sec: Section) -> list[MemoLine]:
        lines = [self.slot("s13-cases", "Downside, base and upside cases. Tricorder supplies only the facts they rest on.")]
        facts = self.claims_with_label("raise_amount", "pre_money", "runway_months")
        lines += [self.claim_line("s13", c).model_copy(update={"audience": "operator"}) for c in facts]
        have = {c.value.label for c in facts}
        missing = [w for lab, w in (("raise_amount", "the round"), ("runway_months", "the runway with the hiring plan")) if lab not in have]
        if missing or "comps" in self.r.scans_missing:
            parts = missing + (["the comps"] if "comps" in self.r.scans_missing else [])
            lines.append(self.readout_gap("s13-facts", f"The facts these cases rest on are not assessed yet: {_and(parts)}.",
                                          "no claim with those labels, or the comps scan has not run",
                                          "claims labelled raise_amount and runway_months; the comps scan", audience="operator"))
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
            lines.append(self.readout_gap("s14-coverage", "Checklist coverage: not assessed yet.",
                                          "the merge's coverage step did not write its panel", f"python -m scans.memo {self.room_dir}"))
        if self.asks:
            n_if = sum(1 for a in self.asks.values() if a.if_you_have_it)
            lines.append(MemoLine(id="s14-asks", kind="ask", label="To ask the founder", audience="page",
                                  text=f"{len(self.asks)} requests, {n_if} of them \"if you have it\". The operator sends them to the founder.",
                                  ask_ids=list(self.asks)))
            for aid, a in self.asks.items():
                feeds = BY_NUMBER[PIECE_SECTION.get(a.piece, 11)].title
                lines.append(MemoLine(id=f"s14-{aid}", kind="ask", label="If you have it" if a.if_you_have_it else None,
                                      text=f"{_sentence(a.what)} Why: {_sentence(a.why)} Feeds: {feeds}.", audience="operator",
                                      claim_ids=[c for c in a.claim_ids if c in self.claims],
                                      checklist_ids=[a.checklist_id] if a.checklist_id else [], ask_ids=[aid]))
        for claim, problems in self.unverified:
            lines.append(MemoLine(id=f"s14-unverified-{claim.id}", kind="unverified", label="Could not verify",
                                  text=f"{partner_text(claim.text)} Its quote was not found at its source."))
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
                                  claim_ids=sorted(set(ids)), audience="operator"))
        files = sorted({k.split("|", 1)[0] for k in by_key})
        dates = sorted({m[2] for m in meta.values() if m[2]})
        summary = MemoLine(id="s16-sources", kind="fact", label="Sources",
                           text=f"{len(by_key)} places in {len(files)} files of the room"
                                + (f", read {_and(dates)}" if dates else "")
                                + ". Each claim's note names its own file and place.")
        return [summary] + lines

    # Assemble -------------------------------------------------------------

    def build(self) -> Memo:
        self.verify()
        routed: dict[int, list[Claim]] = {}
        for c in self.claims.values():
            routed.setdefault(claim_section(c, self.piece_of), []).append(c)
        sections = []
        for sec in SECTIONS:
            n, collapsed = sec.number, False
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
                lines = [self.slot("s15-recommendation", "Invest, pass or wait; the amount and any conditions; "
                                                         "the two reasons that decide it, and why it could be wrong.")]
            elif n == 16:
                lines = []
            else:
                lines, collapsed = self.body(sec, routed.get(n, []))
            sections.append(MemoSection(number=n, key=sec.key, title=sec.title, who_writes=sec.who_writes,
                                        lines=lines, collapsed=collapsed))
        cited = {cid for s in sections for ln in s.lines for cid in ln.claim_ids}
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
                    steps_missing=[n for n in ("link", "pieces", "top_flags") if not step_built(n)],
                    changes=[ChangeEntry(version=1, at=self.built_at, author="Tricorder",
                                         what=f"Drafted from the readout built {self.r.built_at}.")])
        memo.sources = read_sources(memo, self.room_dir)
        return memo


def empty_because(section: MemoSection) -> list[str]:
    """When a section holds nothing Tricorder could source, the gap lines that say why."""
    filled = any(ln.kind in ("claim", "reading", "pieces", "ask", "operator", "source", "ref") or
                 (ln.kind == "coverage" and section.number == 14) or
                 (ln.kind == "fact" and section.number == 1) for ln in section.lines)
    if filled:
        return []
    return [ln.text for ln in section.lines if ln.kind == "gap"]


def read_sources(memo: Memo, room_dir: Path) -> dict[str, SourceText]:
    """The text at every cited source's locator, so the page opens it offline, and how it reads."""
    stated = " ".join(c.text for c in memo.claims.values())
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
            out[k] = SourceText(key=k, text=_window(text, s.quote), found=True, reads_as=reads_as(s, room_dir, stated))
    return out


def _window(text: str, quote: str) -> str:
    if len(text) <= SOURCE_TEXT_LIMIT:
        return text
    at = text.lower().find(quote.lower()[:40])
    start = max(0, at - SOURCE_TEXT_LIMIT // 2) if at >= 0 else 0
    return ("..." if start else "") + text[start:start + SOURCE_TEXT_LIMIT] + "..."


def build_memo(readout: Readout, room_dir: str | Path, built_at: str) -> Memo:
    return _Builder(readout, Path(room_dir), built_at).build()
