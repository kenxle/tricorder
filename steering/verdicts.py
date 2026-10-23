"""Piece verdicts and top flags for a steered readout.

`rebuild(readout, room_dir)` runs the merge's own `pieces` and `top_flags`
steps (scans/memo/merge.py, STEPS) when those modules exist. Until the readout
slice writes them, it uses the copy of the FRAMEWORKS rules below ("Piece
verdicts" steps 1, 3, 4 and 5; "Top green and red flags"), and says so. The
copy is written to move into scans/memo/pieces.py and top_flags.py unchanged.

Step 2 (linking corroborating claims) is the merge's `link` step. This file
reads `conflicts_with` and `corroborated_by` as the claims carry them.
"""

from __future__ import annotations

from pathlib import Path

from schema.claim import PIECE_ORDER, Claim, Piece, Readout, TopFlag
from schema import settings
from scans.memo import merge

# FRAMEWORKS "Piece verdicts", step 1.
LABEL_PIECE: dict[str, str] = {
    **dict.fromkeys(("arr", "mrr", "paying_accounts", "accounts_created"), "traction_and_revenue"),
    **dict.fromkeys(("nrr_12m", "grr_12m", "cohort_size"), "retention"),
    **dict.fromkeys(("cash", "net_burn_monthly", "runway_months", "payroll_monthly", "hires"), "burn_and_runway"),
    **dict.fromkeys(("gross_margin", "cost_of_revenue", "arpa", "acv", "cac", "payback_months", "ltv", "price"), "unit_economics"),
    **dict.fromkeys(("largest_customer_share", "top3_customer_share", "contract_term", "notice_period"), "customers"),
    **dict.fromkeys(("tam", "sam", "som", "signal"), "market"),
    "headcount": "team",
    **dict.fromkeys(("raise_amount", "pre_money", "post_money", "ownership"), "the_pitch_itself"),
}

# A claim with no value, or the label "other": the piece its entry names
# under "How the readout scores it". One line per built check name.
CHECK_PIECE: dict[str, str] = {
    "deck_revenue_vs_pnl": "traction_and_revenue",            # 1.14
    "deck_history_vs_metrics": "traction_and_revenue",        # 1.14
    "mrr_column_vs_subscription_rows": "traction_and_revenue",  # 1.12 a
    "billings_vs_recognised_revenue": "traction_and_revenue",   # 1.12 b
    "gross_vs_net_revenue": "traction_and_revenue",             # 1.12 c
    "contractor_spend_vs_headcount_and_burn": "burn_and_runway",  # 1.12 e
    "capitalised_spend_vs_pnl_and_cash": "burn_and_runway",       # 1.12 f
    "deferred_revenue_vs_earned": "traction_and_revenue",       # 1.12 g
    "one_time_fees_in_recurring_metrics": "traction_and_revenue",  # 1.12 h
    "arr_from_subscription_rows": "traction_and_revenue",       # 1.2
    "rebuild_cohorts_from_customer_file": "retention",          # 1.3
}

# FRAMEWORKS "Piece verdicts", step 2: these repeat one another and count as one source.
NARRATIVE = ("pitch_deck", "claims.json", "company_overview", "pitch_video", "website_copy", "product_one_pager", "cover_note")


def piece_of(claim: Claim) -> str:
    if claim.scan == "comps":
        return "comps"
    if claim.scan == "signals":
        return "market"
    if claim.value is not None and claim.value.label in LABEL_PIECE:
        return LABEL_PIECE[claim.value.label]
    return CHECK_PIECE.get(claim.check.name.split(".")[0], "the_pitch_itself")


def source_key(uri: str) -> str:
    name = Path(uri).name
    return "narrative" if any(n in name for n in NARRATIVE) else uri


def contradicted(c: Claim) -> bool:
    return bool(c.conflicts_with) or c.severity == "flag"


def corroborated(c: Claim) -> bool:
    return bool(c.corroborated_by) and not contradicted(c)


def _independent(c: Claim, by_id: dict[str, Claim]) -> set[str]:
    keys = {source_key(s.uri) for s in c.sources}
    for other in c.corroborated_by:
        if other in by_id:
            keys |= {source_key(s.uri) for s in by_id[other].sources}
    return keys


def red_gap(c: Claim, by_id: dict[str, Claim]) -> float | None:
    """|stated - found| / |found|, found from the conflicting computed claim, else one citing a record."""
    if c.value is None:
        return None
    others = [by_id[i] for i in c.conflicts_with if i in by_id and by_id[i].value is not None]
    found = next((o for o in others if o.confidence == "computed"), None) or next(
        (o for o in others if any(source_key(s.uri) != "narrative" for s in o.sources)), None)
    if found is None or found.value.number == 0:
        return None
    return abs(c.value.number - found.value.number) / abs(found.value.number)


def _worst_flag(flags: list[Claim], by_id: dict[str, Claim]) -> Claim:
    """The flag with the largest gap; flags with no gap to compute rank after, in claim order."""
    return max(enumerate(flags), key=lambda ic: (red_gap(ic[1], by_id) is not None, red_gap(ic[1], by_id) or 0.0, -ic[0]))[1]


def _label_words(c: Claim) -> str:
    return c.value.label.replace("_", " ") if c.value else "it"


def standin_pieces(readout: Readout) -> list[Piece]:
    by_id = {c.id: c for c in readout.claims}
    pieces = []
    for name in PIECE_ORDER:
        claims = [c for c in readout.claims if piece_of(c) == name]
        gaps = [g for g in readout.gaps if g.piece == name]
        cor = [c for c in claims if corroborated(c)]
        con = [c for c in claims if contradicted(c)]
        flags = [c for c in claims if c.severity == "flag"]
        if flags or (con and not cor):
            verdict = "looking_weak"
            top = _worst_flag(flags, by_id) if flags else con[0]
            reason, ids = top.text, [top.id]
        elif con and cor:
            verdict = "mixed"
            best = max(cor, key=lambda c: len(_independent(c, by_id)))
            reason, ids = f"{best.text} {con[0].text}", [best.id, con[0].id]
        elif cor:
            verdict = "looking_strong"
            best = max(cor, key=lambda c: len(_independent(c, by_id)))
            reason, ids = best.text, [best.id]
        else:
            verdict = "not_enough_in_the_room"
            ids = []
            if gaps:
                reason = gaps[0].what
            elif claims:
                reason = f"Only one source states {_label_words(claims[0])}."
            else:
                reason = "No claim in the readout feeds this piece yet."
        support = set().union(*(_independent(c, by_id) for c in cor)) if cor else set()
        against = {s.uri for c in con for s in c.sources}
        pieces.append(Piece(name=name, verdict=verdict, reason=reason, reason_claim_ids=ids,
                            claim_ids=[c.id for c in claims], corroborating_sources=len(support),
                            contradicting_sources=len(against)))
    return pieces


def standin_top_flags(readout: Readout) -> list[TopFlag]:
    s = settings.load()
    by_id = {c.id: c for c in readout.claims}
    strong = {p.name for p in readout.pieces if p.verdict == "looking_strong"}
    greens: list[tuple[int, int, Claim, str]] = []
    reds: list[tuple[float, int, Claim, str]] = []
    for i, name in enumerate(PIECE_ORDER):
        claims = [c for c in readout.claims if piece_of(c) == name]
        if name in strong:
            cands = [c for c in claims if corroborated(c)]
            if cands:
                best = max(cands, key=lambda c: len(_independent(c, by_id)))
                greens.append((len(_independent(best, by_id)), i, best, name))
        flags = [c for c in claims if c.severity == "flag"]
        if flags:
            worst = _worst_flag(flags, by_id)
            reds.append((red_gap(worst, by_id) if red_gap(worst, by_id) is not None else -1.0, i, worst, name))
    greens.sort(key=lambda g: (-g[0], g[1]))
    reds.sort(key=lambda r: (-r[0], r[1]))
    out = [TopFlag(kind="green", piece=name, rank=n, text=c.text, claim_ids=[c.id])
           for n, (_, _, c, name) in enumerate(greens[: int(s["top_green_flags"])], 1)]
    out += [TopFlag(kind="red", piece=name, rank=n, text=c.text, claim_ids=[c.id])
            for n, (_, _, c, name) in enumerate(reds[: int(s["top_red_flags"])], 1)]
    return out


def rebuild(readout: Readout, room_dir: Path) -> tuple[Readout, str]:
    """Pieces and top flags rebuilt from the readout's claims. Returns who rebuilt them:
    "merge" (its steps exist), "steering" (its copy of the rules), or both."""
    readout = readout.model_copy(update={"pieces": [], "top_flags": []})
    used = []
    for name in ("pieces", "top_flags"):
        module = merge._step(name) if name in merge.STEPS else None
        if module is not None:
            readout = module.apply(readout, Path(room_dir))
            used.append("merge")
    if not readout.pieces:
        readout = readout.model_copy(update={"pieces": standin_pieces(readout)})
        used.append("steering")
    if not readout.top_flags:
        readout = readout.model_copy(update={"top_flags": standin_top_flags(readout)})
        used.append("steering")
    who = sorted(set(used))
    return readout, " and ".join(who) if who else "steering"
