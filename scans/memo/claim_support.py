"""Claim support: a merge step that relabels the claims scan's claims against
every other scan's findings.

    def apply(readout: Readout, room_dir: Path) -> Readout

The claims scan labels each pitch figure against what it reads in the room
itself (scans/claims/). No scan reads another scan's output, so a red flag that
another scan found by rebuilding a number (the cohorts from the customer file,
the margin from the ledger, revenue net of pass-through money) cannot reach
those labels inside the scan. This step does that, in the merge, by script:

- A claim labelled supported or unsupported becomes contradicted when another
  scan's flag claim shares one of its sources (the same file, the same slide or
  page, and the same words), or when that flag's check is one that settles the
  claim's kind (CHECK_SETTLES). The claim then shows both sides: its own source
  and the flag's sources outside the pitch, and `conflicts_with` names the flag.
- A supported claim gains `corroborated_by`: another scan's claim with the same
  value label, unit and period that agrees within `match_tolerance` and cites no
  pitch document.
- A claim the quote checker moved to "could not verify" reads so in the table.
- The "claims table" and "claims table counts" Panels are rewritten to match.

Place: after "link" and before "pieces" in scans/memo/merge.py STEPS, so piece
verdicts and top flags see the final severities. Until it is listed there,

    python -m scans.memo.claim_support <room_dir>

applies it to the readout the merge already wrote.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from schema.check_quotes import _norm
from schema.claim import Claim, Panel, Readout, Source
from schema.settings import load as load_settings
from scans.base import out_dir

TABLE = "claims table"
COUNTS = "claims table counts"
FOUNDER = re.compile(r"pitch_deck|claims\.json|pitch_video|company_overview|website_copy|product_one_pager|cover_note")

# Another scan's check that, when it flags, settles a claim of these kinds (the
# plain kind names in the claims table's "kind" column). Check names are the
# ones FRAMEWORKS gives each entry.
CHECK_SETTLES: dict[str, tuple[str, ...]] = {
    "arr_from_subscription_rows": ("ARR",),
    "mrr_column_vs_subscription_rows": ("ARR", "MRR"),
    "rebuild_cohorts_from_customer_file": ("net revenue retention",),
    "payroll_from_hiring_plan_and_rerun_cash": ("runway", "average net burn"),
    "contractor_spend_vs_headcount_and_burn": ("runway", "average net burn"),
    "top_customer_share": ("largest customer share",),
    "gross_margin_from_ledger": ("gross margin",),
    "cumulative_column_shown_as_active": ("paying customers",),
    "gross_vs_net_revenue": ("revenue, last 12 months",),
    "deferred_revenue_vs_earned": ("MRR",),
    "billings_vs_recognised_revenue": ("MRR",),
    "deck_history_vs_metrics": ("chart months",),
}


def _founder(source: Source) -> bool:
    return bool(FOUNDER.search(source.uri))


def _page(locator: str) -> str:
    m = re.match(r"\s*(slide|page|line|seg|row)\s*(\d+)", locator.lower())
    return f"{m.group(2)}" if m else locator.lower().strip()


def shares_source(mine: Claim, other: Claim) -> bool:
    """The same pitch document (deck slide, script line, video segment), and one quote
    inside the other. Only pitch sources count: two claims citing the same row of
    an export are about that row, not about the same pitch figure."""
    for a in [s for s in mine.sources if _founder(s)]:
        for b in [s for s in other.sources if _founder(s)]:
            if a.uri != b.uri or _page(a.locator) != _page(b.locator):
                continue
            qa, qb = _norm(a.quote), _norm(b.quote)
            if qa and qb and (qa in qb or qb in qa):
                return True
    return False


def settles(other: Claim, kind_name: str) -> bool:
    return kind_name in CHECK_SETTLES.get(other.check.name.removesuffix(".read"), ())


def _agree(a: float, b: float, tol: float) -> bool:
    return a == b or abs(a - b) <= tol * max(abs(a), abs(b))


def apply(readout: Readout, room_dir: Path) -> Readout:
    tables = [p for p in readout.panels if p.name == TABLE]
    if not tables:
        return readout
    table = tables[0]
    col = {name: i for i, name in enumerate(table.columns)}
    tol = float(load_settings()["match_tolerance"])
    by_id = {c.id: c for c in readout.claims if c.scan == "claims"}
    unverified = {c.id for c in readout.unverified if c.scan == "claims"}
    others = [c for c in readout.claims if c.scan != "claims"]
    flags = [c for c in others if c.severity == "flag"]

    new_claims: dict[str, Claim] = {}
    for row in table.rows:
        cid = row[col["claim id"]]
        if cid in unverified:
            row[col["label"]] = "could not verify"
            continue
        claim = by_id.get(cid)
        if claim is None:
            continue
        label = row[col["label"]]
        kind_name = row[col["kind"]]
        if label in ("supported", "unsupported"):
            hits = [f for f in flags if shares_source(claim, f) or settles(f, kind_name)]
            if hits:
                claim = _contradict(claim, hits)
                row[col["label"]] = "contradicted"
                row[col["disagrees"]] = "; ".join(x for x in [row[col["disagrees"]]] + [
                    f"{f.scan} {f.check.name} ({f.id}): {f.text}" for f in hits] if x)
                row[col["ask"]] = f"Please walk us from the source data to {row[col['stated']]} ({row[col['where']].split(';')[0]}) (C71)."
        if row[col["label"]] == "supported" and claim.value is not None:
            corroborating = [o.id for o in others if o.value is not None and o.value.label == claim.value.label
                             and o.value.label != "other" and o.value.unit == claim.value.unit
                             and o.value.period == claim.value.period and _agree(o.value.number, claim.value.number, tol)
                             and not any(_founder(s) for s in o.sources) and o.severity != "flag"]
            if corroborating:
                claim = claim.model_copy(update={"corroborated_by": sorted(set(claim.corroborated_by) | set(corroborating))})
        new_claims[cid] = claim

    readout.claims = [new_claims.get(c.id, c) if c.scan == "claims" else c for c in readout.claims]
    _recount(readout, table)
    table.rows.sort(key=lambda r: {"contradicted": 0, "unsupported": 1, "supported": 2}.get(r[col["label"]], 3))
    return readout


def _contradict(claim: Claim, hits: list[Claim]) -> Claim:
    first = claim.text.split(": ", 1)[-1].split(". ")[0].rstrip(".")
    reasons = "; ".join(f"the {f.scan} scan's {f.check.name} check flags it: {f.text}" for f in hits)
    sources = [claim.sources[0]]
    seen = {(s.uri, s.locator, s.quote) for s in sources}
    for f in hits:
        for s in f.sources:
            if not _founder(s) and (s.uri, s.locator, s.quote) not in seen:
                seen.add((s.uri, s.locator, s.quote))
                sources.append(s)
    return claim.model_copy(update={
        "text": f"Contradicted: {first}, but {reasons}",
        "severity": "flag",
        "sources": sources,
        "conflicts_with": sorted(set(claim.conflicts_with) | {f.id for f in hits}),
    })


def _recount(readout: Readout, table: Panel) -> None:
    col = table.columns.index("label")
    counts = {k: sum(1 for r in table.rows if r[col] == k) for k in ("supported", "contradicted", "unsupported", "could not verify")}
    for panel in readout.panels:
        if panel.name != COUNTS:
            continue
        rows = {r[0]: r for r in panel.rows}
        for k, v in counts.items():
            if k in rows:
                rows[k][1] = str(v)
            elif v:
                panel.rows.append([k, str(v)])
        panel.rows.append(["relabelled by the memo step", "yes"])


def main(argv: list[str]) -> int:
    if len(argv) != 1 or not Path(argv[0]).is_dir():
        print("usage: python -m scans.memo.claim_support <room_dir>")
        return 2
    room = Path(argv[0])
    target = out_dir(room) / "readout.json"
    if not target.exists():
        print(f"no readout at {target}; run python -m scans.memo {room} first")
        return 2
    readout = apply(Readout.model_validate_json(target.read_text(encoding="utf-8")), room)
    target.write_text(readout.model_dump_json(indent=2) + "\n", encoding="utf-8")
    counts = next((dict((r[0], r[1]) for r in p.rows) for p in readout.panels if p.name == COUNTS), {})
    print(json.dumps({"readout": str(target), "claims_table": counts}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
