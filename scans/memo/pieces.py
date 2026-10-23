"""Assign claims and compute piece verdicts using FRAMEWORKS, 'Piece verdicts'."""

from pathlib import Path

from schema.claim import PIECE_ORDER, Claim, Piece, Readout


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

CHECK_PIECE: dict[str, str] = {
    **dict.fromkeys((
        "deck_revenue_vs_pnl", "deck_history_vs_metrics", "mrr_column_vs_subscription_rows",
        "billings_vs_recognised_revenue", "gross_vs_net_revenue", "deferred_revenue_vs_earned",
        "one_time_fees_in_recurring_metrics", "arr_from_subscription_rows",
        "cancellable_within_notice_vs_arr", "plan_revenue_past_term_end", "signed_not_live_vs_revenue",
    ), "traction_and_revenue"),
    **dict.fromkeys(("contractor_spend_vs_headcount_and_burn", "capitalised_spend_vs_pnl_and_cash",
                     "payroll_from_hiring_plan_and_rerun_cash"), "burn_and_runway"),
    "rebuild_cohorts_from_customer_file": "retention",
    "counted_line_without_contract": "customers",
    "clause_notes": "customers",
}

NARRATIVE = ("pitch_deck", "claims.json", "company_overview", "pitch_video", "website_copy",
             "product_one_pager", "cover_note")

PIECE_SCANS = {
    "traction_and_revenue": ("redflags", "claims"),
    "retention": ("redflags", "claims"),
    "burn_and_runway": ("redflags", "model", "bank"),
    "unit_economics": ("redflags", "model"),
    "customers": ("redflags", "claims"),
    "market": ("signals", "frameworks", "outside"),
    "comps": ("comps",),
    "team": ("founders", "outside"),
    "the_pitch_itself": ("claims", "video"),
}


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


def contradicted(claim: Claim) -> bool:
    return bool(claim.conflicts_with) or claim.severity == "flag"


def independent_sources(claim: Claim, by_id: dict[str, Claim]) -> set[str]:
    linked = [by_id[i] for i in claim.corroborated_by if i in by_id]
    return {source_key(s.uri) for c in [claim, *linked] for s in c.sources}


def corroborated(claim: Claim, by_id: dict[str, Claim]) -> bool:
    return (not contradicted(claim) and any(i in by_id for i in claim.corroborated_by)
            and len(independent_sources(claim, by_id)) > 1)


def red_gap(claim: Claim, by_id: dict[str, Claim]) -> float | None:
    """Relative gap to a comparable computed claim, then to a record claim."""
    value = claim.value
    if value is None or value.label == "other":
        return None
    others = [by_id[i] for i in claim.conflicts_with if i in by_id and by_id[i].value is not None]
    others = [o for o in others if (o.value.label, o.value.unit, o.value.period) == (value.label, value.unit, value.period)]
    found = next((o for o in others if o.confidence == "computed"), None) or next(
        (o for o in others if any(source_key(s.uri) != "narrative" for s in o.sources)), None)
    if found is None:
        return None
    # The cohort check's flag carries its rebuild; its peer carries the tab reading.
    # Other supported comparisons follow the framework's stated-flag/found-peer shape.
    denominator = value.number if claim.check.name.split(".")[0] == "rebuild_cohorts_from_customer_file" else found.value.number
    if denominator == 0:
        return None
    return abs(value.number - found.value.number) / abs(denominator)


def worst_flag(flags: list[Claim], by_id: dict[str, Claim]) -> Claim:
    """Ties follow claim order; flags without a numeric comparison come last."""
    return max(flags, key=lambda c: (red_gap(c, by_id) is not None, red_gap(c, by_id) or 0.0))


def apply(readout: Readout, room_dir: Path) -> Readout:
    by_id = {c.id: c for c in readout.claims if c.confidence != "unverified"}
    pieces = []
    for name in PIECE_ORDER:
        claims = [c for c in by_id.values() if piece_of(c) == name]
        waiting = [scan for scan in PIECE_SCANS[name] if scan in readout.scans_missing] if not claims else []
        gaps = [g for g in readout.gaps if g.piece == name]
        cor = [c for c in claims if corroborated(c, by_id)]
        con = [c for c in claims if contradicted(c)]
        flags = [c for c in claims if c.severity == "flag"]
        if flags or (con and not cor):
            verdict = "looking_weak"
            top = worst_flag(flags, by_id) if flags else con[0]
            reason, ids = top.text, [top.id]
        elif con and cor:
            verdict = "mixed"
            best = max(cor, key=lambda c: len(independent_sources(c, by_id)))
            reason, ids = f"{best.text} {con[0].text}", [best.id, con[0].id]
        elif cor:
            verdict = "looking_strong"
            best = max(cor, key=lambda c: len(independent_sources(c, by_id)))
            reason, ids = best.text, [best.id]
        else:
            verdict = "not_enough_in_the_room"
            ids = []
            if gaps:
                reason = gaps[0].what
            elif claims:
                label = claims[0].value.label.replace("_", " ") if claims[0].value else "it"
                reason = f"Only one source states {label}."
            elif waiting:
                reason = f"Not assessed yet: no verified claims are available from the {', '.join(waiting)} scans."
            else:
                reason = "No claim in the readout feeds this piece yet."
        support = {s for c in cor for s in independent_sources(c, by_id)}
        against = {s.uri for c in con for s in c.sources}
        pieces.append(Piece(name=name, verdict=verdict, reason=reason, reason_claim_ids=ids,
                            claim_ids=[c.id for c in claims], corroborating_sources=len(support),
                            contradicting_sources=len(against), status="waiting_on_input" if waiting else "done",
                            waiting_on=waiting))
    return readout.model_copy(update={"pieces": pieces})
