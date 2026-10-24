"""The expert-read report sections: one per piece Kimmy's knowledge covers.

    python -m scans.memo.sections <room_dir>   writes out/<room>/sections/<piece>.json and <piece>.chart.json

For traction and revenue, and for burn and runway, this gathers the piece's
claims, flags, gaps and asks from the readout and writes a short section in
five parts: what the evidence shows, read through Kimmy's lens, what is strong,
what is weak, and what to ask.

With ANTHROPIC_API_KEY set (and TRICORDER_OFFLINE not), the model writes the
parts through clients.llm.read, with the piece's knowledge file in the prompt
(scans/knowledge.py). Without a key, or when the call fails, a script writes
the same five parts from the claims' own sentences and a fixed table of
Kimmy's rules. No model prose then.

Either way, `check_sentence` runs on every sentence: it keeps only claim ids
that exist in the readout, drops a sentence left citing none, and drops a
sentence with a figure that is not in the claims it cites. Numbers come only
from claims. The chart beside each section is script data (scans/memo/charts.py).
"""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from schema.claim import AskItem, Claim, Gap, Readout
from scans import knowledge
from scans.base import now_iso, offline, out_dir
from scans.memo import charts

PIECE_SECTION = {"traction_and_revenue": 7, "burn_and_runway": 10}
TITLES = {"traction_and_revenue": "Traction and revenue: the expert read",
          "burn_and_runway": "Burn and runway: the expert read"}
PIECE_WORDS = {"traction_and_revenue": "traction and revenue", "burn_and_runway": "burn and runway"}
CHARTS = {"traction_and_revenue": charts.traction_chart, "burn_and_runway": charts.burn_chart}
PARTS: tuple[tuple[str, str], ...] = (
    ("shows", "What the evidence shows"),
    ("lens", "Through Kimmy's lens"),
    ("strong", "What is strong"),
    ("weak", "What is weak"),
    ("ask", "What to ask"),
)
VERDICT_WORDS = {"looking_strong": "looking strong", "looking_weak": "looking weak", "mixed": "mixed",
                 "not_enough_in_the_room": "not enough in the room"}


# The section's shape ---------------------------------------------------------


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ReportSentence(_Strict):
    id: str
    text: str
    claim_ids: list[str]


class ReportPart(_Strict):
    key: str
    heading: str
    sentences: list[ReportSentence] = Field(default_factory=list)


class Dropped(_Strict):
    part: str
    text: str
    claim_ids: list[str]
    why: str


class ReportSection(_Strict):
    piece: str
    section: int
    title: str
    readout_built_at: str
    built_at: str
    written_by: Literal["model", "script"]
    model: str | None = None
    knowledge: str = Field(description="The knowledge file in the prompt (model) or behind the rule table (script).")
    verdict: str | None = None
    parts: list[ReportPart]
    dropped: list[Dropped] = Field(default_factory=list)
    note: str | None = Field(default=None, description="Why the script wrote it, when a model was tried.")
    chart: dict | None = None


# What the model returns --------------------------------------------------------


class DraftSentence(_Strict):
    text: str = Field(description="One plain sentence. No claim ids in the text.")
    claim_ids: list[str] = Field(description="The ids of the claims this sentence rests on.")


class SectionDraft(_Strict):
    shows: list[DraftSentence] = Field(description="Two or three sentences: what the evidence shows.")
    lens: list[DraftSentence] = Field(description="One to three sentences: how the expert reads this evidence.")
    strong: list[DraftSentence] = Field(description="Zero to two sentences: what is strong. Empty when nothing is.")
    weak: list[DraftSentence] = Field(description="One to three sentences: what is weak.")
    ask: list[DraftSentence] = Field(description="One to three questions to put to the founder.")


# Gathering -------------------------------------------------------------------


@dataclass
class Evidence:
    piece: str
    verdict: str | None
    reason: str
    reason_ids: list[str]
    claims: list[Claim]
    gaps: list[Gap] = field(default_factory=list)
    asks: list[AskItem] = field(default_factory=list)

    @property
    def by_id(self) -> dict[str, Claim]:
        return {c.id: c for c in self.claims}


def gather(readout: Readout, piece: str) -> Evidence:
    """The piece's claims (its own, plus any top flag's), gaps and asks from the readout."""
    by_id = {c.id: c for c in readout.claims}
    p = next((x for x in readout.pieces if x.name == piece), None)
    ids = list(p.claim_ids) if p else [c.id for c in readout.claims if c.value and c.value.label in _LABELS.get(piece, ())]
    for f in readout.top_flags:
        if f.piece == piece:
            ids += f.claim_ids
    claims = [by_id[i] for i in dict.fromkeys(ids) if i in by_id]
    return Evidence(piece=piece, verdict=p.verdict if p else None, reason=p.reason if p else "",
                    reason_ids=[i for i in (p.reason_claim_ids if p else []) if i in by_id], claims=claims,
                    gaps=[g for g in readout.gaps if g.piece == piece], asks=[a for a in readout.asks if a.piece == piece])


_LABELS = {"traction_and_revenue": ("arr", "mrr", "paying_accounts", "accounts_created"),
           "burn_and_runway": ("cash", "net_burn_monthly", "runway_months", "payroll_monthly", "hires")}


# The citation and number check -------------------------------------------------

_NUMBER = re.compile(r"\d+(?:[.,]\d+)*")


def _norm(token: str) -> str:
    t = token.replace(",", "")
    if "." in t:
        t = t.rstrip("0").rstrip(".")
    return t.lstrip("0") or "0"


def numbers_in(text: str) -> set[str]:
    return {_norm(t) for t in _NUMBER.findall(text or "")}


def claim_numbers(claim: Claim) -> set[str]:
    """Every figure a claim states: in its sentence, its value and where its sources sit."""
    out = numbers_in(claim.text)
    if claim.value:
        n = claim.value.number
        out |= {_norm(f"{n:.2f}"), _norm(str(round(n)))}
        out |= numbers_in(claim.value.period or "")
    for s in claim.sources:
        out |= numbers_in(s.locator) | numbers_in(Path(s.uri).name)
    return out


def clean(text: str) -> str:
    """Plain punctuation: no em or en dashes, single spaces."""
    text = re.sub(r"\s*[—–]\s*", ", ", text)
    return re.sub(r"\s{2,}", " ", text).strip()


def check_sentence(text: str, claim_ids: list[str], claims: dict[str, Claim]) -> tuple[list[str], str | None]:
    """(the ids kept, why the sentence is dropped or None). Unknown ids are removed; a sentence left with no
    claim, or with a figure none of its claims state, is dropped."""
    kept = [i for i in dict.fromkeys(claim_ids) if i in claims]
    if not kept:
        return [], "cites no claim in the readout"
    pool = set().union(*(claim_numbers(claims[i]) for i in kept))
    stray = sorted(numbers_in(text) - pool)
    if stray:
        return kept, "states a figure its claims do not: " + ", ".join(stray)
    return kept, None


def checked_parts(draft: dict[str, list[tuple[str, list[str]]]], claims: dict[str, Claim], piece: str
                  ) -> tuple[list[ReportPart], list[Dropped]]:
    parts, dropped = [], []
    for key, heading in PARTS:
        sentences = []
        for text, ids in draft.get(key, []):
            text = clean(text)
            if not text:
                continue
            kept, why = check_sentence(text, ids, claims)
            if why:
                dropped.append(Dropped(part=key, text=text, claim_ids=list(ids), why=why))
                continue
            sentences.append(ReportSentence(id=f"xr-{piece}-{key}-{len(sentences) + 1}", text=text, claim_ids=kept))
        parts.append(ReportPart(key=key, heading=heading, sentences=sentences))
    return parts, dropped


# The script's draft (no key) -----------------------------------------------------

# Kimmy's rules, from knowledge/<piece>.md, each with the checks whose claims it reads.
# No figures here: a number in a sentence must come from a claim.
LENS_RULES: dict[str, tuple[tuple[tuple[str, ...], bool, str], ...]] = {
    "traction_and_revenue": (
        (("mrr_column_vs_subscription_rows", "pilot_without_duty_to_convert_vs_recurring", "cancellable_within_notice_vs_arr"), True,
         "Kimmy counts a paid pilot as traction on its own line, and keeps it out of ARR and MRR until it becomes a live recurring contract."),
        (("one_time_fees_in_recurring_metrics",), True,
         "One-time fees and services count in total revenue when earned, but not in ARR or MRR."),
        (("billings_vs_recognised_revenue", "deferred_revenue_vs_earned", "signed_not_live_vs_revenue"), True,
         "Booked value and cash collected are traction, but she keeps them apart from revenue earned as the service is delivered."),
        (("gross_vs_net_revenue",), True,
         "Money passed on to customers is not the company's revenue; she reads revenue net of it."),
        (("plan_revenue_past_term_end", "counted_line_without_contract"), True,
         "A revenue forecast should rest on signed contracts, kept apart from pipeline and renewals nobody has signed."),
        (("claim_support", "deck_revenue_vs_pnl", "deck_history_vs_metrics", "spoken_arr_vs_claims_page"), True,
         "Strong headline figures call for two questions: can the company deliver what is behind them, and why are they so good?"),
    ),
    "burn_and_runway": (
        (("contractor_spend_vs_headcount_and_burn",), True,
         "Kimmy compares spending with the plan's critical work: spend the plan leaves out hides real burn."),
        (("claim_support:hires",), True,
         "Headcount or costs rising without the money for them in the plan is a mismatch the founder should explain."),
        (("claim_support:runway_months", "claim_support:net_burn_monthly"), False,
         "She reads runway as months after the round closes, against the next milestone and a buffer for the next raise."),
        (("capitalised_spend_vs_pnl_and_cash",), True,
         "She looks for one clear path from operating results to cash on hand, tied to the bank."),
    ),
}


def _key(c: Claim) -> set[str]:
    keys = {c.check.name}
    if c.value:
        keys.add(f"{c.check.name}:{c.value.label}")
    return keys


def _first(text: str, n: int = 1) -> str:
    from memo.build import partner_text  # the memo's own plumbing filter; late import, memo imports this module
    t = partner_text(text)
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Z])", t)
    return " ".join(parts[:n]).strip()


def _order(ev: Evidence, claims: list[Claim]) -> list[Claim]:
    lead = set(ev.reason_ids)
    return sorted(claims, key=lambda c: (c.id not in lead, ev.claims.index(c)))


def script_draft(ev: Evidence) -> dict[str, list[tuple[str, list[str]]]]:
    claims = ev.claims
    flags = _order(ev, [c for c in claims if c.severity in ("flag", "watch")])
    seen: set[str] = set()

    def once(c: Claim, n: int = 1) -> str | None:
        t = _first(c.text, n)
        while n > 1 and len(t) > 340:
            n -= 1
            t = _first(c.text, n)
        if not t or t in seen:
            return None
        seen.add(t)
        return t

    def merged(rows: list[tuple[str, list[str]]]) -> list[tuple[str, list[str]]]:
        out: dict[str, list[str]] = {}
        for text, ids in rows:
            out.setdefault(text, [])
            out[text] += [i for i in ids if i not in out[text]]
        return list(out.items())

    weak = []
    for c in flags:
        t = once(c, 3)
        if t:
            weak.append((t, [c.id]))
        if len(weak) >= 3:
            break

    strong = []
    tie = re.compile(r"^(The deck's .* matches|.* tie to|Ledger lines tie|The P&L row .* matches)")
    for c in sorted((c for c in claims if c.severity == "info"), key=lambda c: not tie.match(c.text)):
        if tie.match(c.text) or c.text.startswith("Supported:"):
            t = once(c)
            if t:
                strong.append((t, [c.id]))
        if len(strong) >= 2:
            break

    shows = []
    if ev.reason_ids and ev.verdict:
        shows.append((f"The readout reads this piece as {VERDICT_WORDS.get(ev.verdict, ev.verdict)}; "
                      "the first point under what is weak is the main reason.", ev.reason_ids))
    for c in claims:
        if len(shows) >= 3:
            break
        if c.value and c.severity == "info" and not charts._is_pitch(c):
            t = once(c)
            if t:
                shows.append((t, [c.id]))

    lens = []
    for checks, need_flag, rule in LENS_RULES.get(ev.piece, ()):
        hits = [c.id for c in claims if _key(c) & set(checks) and (c.severity in ("flag", "watch") or not need_flag)]
        if hits:
            lens.append((rule, hits[:3]))
        if len(lens) >= 3:
            break

    ask = []
    for g in ev.gaps:
        hit = [c.id for c in claims if c.sources[0].locator and re.search(rf"\b{re.escape(c.sources[0].locator)}\b", g.what)]
        if hit:
            need = re.sub(r"\s*\((?:C\d\d[, ]*)+\)", "", g.would_need).strip()
            ask.append((f"Ask for {need}: nothing outside the pitch backs these figures.", hit[:3]))
    for _, ids in weak:
        s = ev.by_id[ids[0]].sources[0]
        ask.append((f"Ask the founder to walk from the source data to the figure in {Path(s.uri).name}, {s.locator}.", ids))
    return {"shows": shows, "lens": lens, "strong": strong, "weak": weak, "ask": merged(ask)[:3]}


# The model's draft ---------------------------------------------------------------

TASK = """Task: write the {words} section of a first-pass investment memo for a partner, read through the expert's lens below.

Use only the claims under <claims> in the script results. Each claim starts with its id in square brackets.

Return five parts:
- shows: two or three sentences on what the evidence shows.
- lens: one to three sentences on how the expert reads this evidence, and what it means here.
- strong: up to two sentences on what is strong. Leave it empty when nothing is.
- weak: one to three sentences on what is weak.
- ask: one to three questions to put to the founder.

Rules:
- Plain words. Short sentences, one idea each. No em dashes.
- Every sentence lists in claim_ids the ids of the claims it rests on. A sentence with no claim behind it is dropped.
- Copy each figure exactly as a cited claim writes it. Do not compute, round, convert or estimate. A sentence with a figure that is not in the claims it cites is dropped.
- Do not put claim ids in the sentence text. Do not name scripts, checks or file formats.
- Do not quote the expert knowledge, and take no number from it.
- Do not say whether the data is real, synthetic or fictional."""


def evidence_block(ev: Evidence) -> str:
    lines = [f"Piece: {PIECE_WORDS[ev.piece]}. Verdict: {VERDICT_WORDS.get(ev.verdict or '', 'none')}."]
    if ev.reason:
        lines.append(f"Verdict reason: {ev.reason}")
    lines.append("<claims>")
    for c in ev.claims:
        s = c.sources[0]
        lines.append(f"[{c.id}] severity {c.severity or 'none'}, {c.confidence}, from {s.uri}, {s.locator}: {c.text}")
    lines.append("</claims>")
    if ev.gaps:
        lines.append("<gaps>")
        lines += [f"- {g.what} ({g.why}). Would need: {g.would_need}" for g in ev.gaps]
        lines.append("</gaps>")
    if ev.asks:
        lines.append("<asks>")
        lines += [f"- {a.what} Why: {a.why}" for a in ev.asks]
        lines.append("</asks>")
    return "\n".join(lines)


def model_draft(ev: Evidence) -> dict[str, list[tuple[str, list[str]]]]:
    from clients.llm import read

    out = read(SectionDraft, check_name=f"expert_section.{ev.piece}", scan="memo",
               task=TASK.format(words=PIECE_WORDS[ev.piece]), script_results=evidence_block(ev),
               knowledge=knowledge.block([ev.piece]), max_tokens=8000)
    return {key: [(s.text, s.claim_ids) for s in getattr(out, key)] for key, _ in PARTS}


def model_on() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY")) and not offline()


# Building and storing ------------------------------------------------------------


def build_section(readout: Readout, room_dir: str | Path, piece: str, use_model: bool | None = None,
                  drafter=None) -> ReportSection:
    """One piece's section and chart. `drafter` replaces the model call (tests)."""
    from scans.memo.merge import reads_room

    ev = gather(readout, piece)
    use_model = model_on() if use_model is None else use_model
    note, written_by, model = None, "script", None
    draft = None
    if use_model or drafter:
        try:
            draft = (drafter or model_draft)(ev)
            written_by = "model"
            if not drafter:
                from clients.llm import model_id
                model = model_id("read")
        except Exception as err:  # a failed call is the script's draft, said so on the page
            note = f"The model call failed ({type(err).__name__}), so a script wrote this from the claims."
    if draft is None:
        draft = script_draft(ev)
    parts, dropped = checked_parts(draft, ev.by_id, piece)
    room = reads_room(readout, Path(room_dir))
    try:
        chart = CHARTS[piece](readout, room)
    except Exception:  # a chart that cannot be drawn leaves the section in words
        chart = None
    return ReportSection(piece=piece, section=PIECE_SECTION[piece], title=TITLES[piece], readout_built_at=readout.built_at,
                         built_at=now_iso(), written_by=written_by, model=model, knowledge=f"knowledge/{piece}.md",
                         verdict=ev.verdict, parts=parts, dropped=dropped, note=note, chart=chart)


def folder(room_dir: str | Path) -> Path:
    return out_dir(room_dir) / "sections"


def write(section: ReportSection, room_dir: str | Path) -> tuple[Path, Path]:
    d = folder(room_dir)
    d.mkdir(parents=True, exist_ok=True)
    body = section.model_dump(mode="json")
    chart = body.pop("chart")
    sp, cp = d / f"{section.piece}.json", d / f"{section.piece}.chart.json"
    sp.write_text(json.dumps(body, indent=2), encoding="utf-8")
    cp.write_text(json.dumps(chart, indent=2), encoding="utf-8")
    return sp, cp


def load(room_dir: str | Path, piece: str) -> ReportSection | None:
    d = folder(room_dir)
    try:
        body = json.loads((d / f"{piece}.json").read_text(encoding="utf-8"))
        body["chart"] = json.loads((d / f"{piece}.chart.json").read_text(encoding="utf-8"))
        return ReportSection.model_validate(body)
    except (OSError, ValueError):
        return None


def build_all(readout: Readout, room_dir: str | Path, use_model: bool | None = None) -> list[ReportSection]:
    out = []
    for piece in PIECE_SECTION:
        s = build_section(readout, room_dir, piece, use_model)
        write(s, room_dir)
        out.append(s)
    return out


def for_memo(readout: Readout | None, room_dir: str | Path, readout_built_at: str) -> list[ReportSection]:
    """The sections for a memo: the written ones when they were built from the same readout, else the
    script's draft, built now and not written (no model call on a page view)."""
    out = []
    for piece in PIECE_SECTION:
        s = load(room_dir, piece)
        if s is None or s.readout_built_at != readout_built_at:
            if readout is None:
                continue
            s = build_section(readout, room_dir, piece, use_model=False)
        out.append(s)
    return out


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: python -m scans.memo.sections <room_dir>", file=sys.stderr)
        return 2
    room = Path(argv[0])
    path = out_dir(room) / "readout.json"
    if not path.exists():
        print(f"no readout at {path}; build it first with: python -m scans.memo {room}", file=sys.stderr)
        return 2
    readout = Readout.model_validate_json(path.read_text(encoding="utf-8"))
    summary = {}
    for s in build_all(readout, room):
        summary[s.piece] = {"written_by": s.written_by, "note": s.note,
                            "sentences": sum(len(p.sentences) for p in s.parts), "dropped": len(s.dropped),
                            "chart": bool(s.chart), "file": str(folder(room) / f"{s.piece}.json")}
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
