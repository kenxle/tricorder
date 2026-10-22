"""The checklist, read for the coverage step and the ask-list step.

Pure functions and tables. No model call, no network. The rules are
FRAMEWORKS.md, "Checklist coverage" and "Ask list"; the design is
docs/features/20261022.13_checklist_coverage/04_architecture.md.

Both merge steps that write ask lines import `items_for_gap` and
`gap_is_asked` from here, so the dedupe rule lives in one place.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from schema.claim import AskItem, Gap

ROOT = Path(__file__).resolve().parents[2]
CHECKLIST_CSV = ROOT / "docs" / "ongoing" / "checklist.csv"
GUIDES = ROOT / "docs" / "reports" / "20261022.03_document_guides"

STAGES = ("pre_seed", "seed", "series_a")
LEVELS = ("yes", "lighter", "no", "not stated")
# Ken's default (2026-10-22, overridable): "not stated" items are asked "if you have it".
EXPECTED = ("yes", "lighter", "not stated")

# Checklist piece -> readout piece. Ken's default: legal and cap table asks go to
# "the pitch itself", which already holds the cap table (FRAMEWORKS 1.10).
PIECES = {
    "traction and revenue": "traction_and_revenue",
    "retention": "retention",
    "burn and runway": "burn_and_runway",
    "unit economics": "unit_economics",
    "customers and contracts": "customers",
    "market": "market",
    "comps": "comps",
    "team": "team",
    "the pitch itself": "the_pitch_itself",
    "legal and cap table": "the_pitch_itself",
    "AI and data governance": "the_pitch_itself",
    "outside world": "the_pitch_itself",
}

# Document rows found by file name. Kept in line with scans.base.INPUT_KINDS.
# Statements of work are vendor contracts, so they never count as customer contracts (C34).
DOC_PATTERNS = {
    "C01": r"audit|reviewed_financials", "C02": r"monthly_metrics|kpi|metrics_export",
    "C03": r"revenue_by_customer|customer_mrr", "C04": r"investor_update",
    "C14": r"cohort", "C19": r"financial_model", "C20": r"p_and_l|pnl|balance_sheet|cash_flow|historical_fin",
    "C21": r"bank_statement|^bank/", "C22": r"hiring_plan", "C23": r"expense_ledger|expense_breakdown",
    "C30": r"unit_economics", "C34": r"order_form_|msa_|pilot_agreement_|customer_contract",
    "C35": r"letter_of_intent|loi_|customer_reference", "C36": r"pipeline", "C47": r"market_siz|competitive",
    "C53": r"founder_bio", "C54": r"org_chart|team_bio", "C59": r"cover_note|index",
    "C60": r"pitch_deck", "C61": r"company_overview|one_page_summary", "C62": r"pitch_video",
    "C63": r"product_one_pager|roadmap|demo", "C72": r"cap_table", "C73": r"409a",
    "C74": r"incorporation|bylaws|charter", "C75": r"safe_|convertible_note|term_sheet",
    "C76": r"ip_assignment|invention_assignment|piia", "C77": r"minutes|board_consent",
    "C78": r"option_grant|offer_letter|advisor_agreement", "C79": r"tax_return",
    "C80": r"disclosure|litigation", "C95": r"pro_forma", "C96": r"use_of_funds",
    "C97": r"reference_list", "C98": r"material_agreement", "C99": r"insurance",
    "C100": r"lien|loan_agreement", "C101": r"patent|trademark", "C102": r"model_card|ai_model",
    "C103": r"training_data", "C104": r"ai_vendor|inference_agreement", "C105": r"privacy|gdpr|ccpa",
    "C106": r"bias|ai_ethics", "C107": r"responsible_ai", "C108": r"model_security", "C109": r"ai_regulation",
}

# Document rows a room often holds inside another file: (file pattern, what to look for, where).
# "where" is "sheet" (a sheet name in a workbook), "page" (a page of a PDF) or "file" (the file itself).
CONTAINED = {
    "C14": (r"financial_model\.xlsx$", r"cohort", "sheet"),
    "C20": (r"financial_model\.xlsx$", r"p&l|pnl|income", "sheet"),
    "C30": (r"pitch_deck\.pdf$", r"unit economics|\bCAC\b|payback|\bLTV\b", "page"),
    "C47": (r"pitch_deck\.pdf$", r"market|competit", "page"),
    "C54": (r"founder_bios\.pdf$", r"head of|chief|director|vp ", "page"),
    "C62": (r"pitch_video_script\.md$", r"", "file"),
    "C75": (r"cap_table\.xlsx$", r"safe", "sheet_text"),
    "C95": (r"cap_table\.xlsx$", r"pro forma", "sheet_text"),
    "C96": (r"pitch_deck\.pdf$", r"use of funds", "page"),
}

# Check rows -> the document rows they read, from checklist.csv's "where" column.
CHECK_INPUTS = {
    "C05": ["C03", "C34"], "C06": ["C02", "C03"], "C07": ["C20", "C03"], "C08": ["C20", "C03"],
    "C09": ["C20", "C03"], "C10": ["C02", "C03"], "C11": ["C02", "C60"], "C12": ["C04"],
    "C13": ["C01", "C20"], "C15": ["C03", "C14"], "C16": ["C03", "C14"], "C17": ["C03", "C14"],
    "C18": ["C02", "C03"], "C24": ["C19", "C20", "C22"], "C25": ["C23", "C20", "C22"],
    "C26": ["C23", "C20", "C19"], "C27": ["C21", "C20"], "C31": ["C23", "C20"],
    "C32": ["C20", "C02", "C03"], "C33": ["C20", "C02", "C03"], "C37": ["C03", "C34"],
    "C38": ["C34", "C03", "C19"], "C39": ["C34", "C03", "C20"], "C40": ["C34", "C19"],
    "C41": ["C34", "C03"], "C42": ["C34", "C03"], "C43": ["C19", "C03", "C34"], "C44": ["C35", "C34"],
    "C45": ["C36", "C19"], "C48": ["C60"], "C64": ["C60"], "C65": ["C60", "C19", "C02"], "C66": ["C62"],
    "C67": ["C60", "C72"], "C68": ["C63", "C96"], "C70": ["C60"], "C81": ["C72", "C75"],
    "C82": ["C72", "C75", "C78"], "C83": ["C76"], "C84": ["C74", "C77"], "C85": ["C73"], "C86": ["C79"],
    "C87": ["C80"],
}

# Entry number -> the check names its claims carry (FRAMEWORKS "Check name:" lines, and the
# entry's framework name for entries with no stated check name). A model claim adds ".read".
ENTRY_CHECKS = {
    "1.1": {"deck_claims"},
    "1.2": {"arr_from_subscription_rows", "arr_definition"},
    "1.3": {"rebuild_cohorts_from_customer_file", "cohort_retention"},
    "1.4": {"payroll_from_hiring_plan_and_rerun_cash", "burn_hiring_runway"},
    # deck_revenue_vs_pnl and deck_history_vs_metrics: the deck-vs-books checks, which compare the
    # deck's figures with the books the same way 1.5 compares them with the model (row C65).
    "1.5": {"deck_claim_vs_named_cell", "deck_model_reconcile", "deck_revenue_vs_pnl", "deck_history_vs_metrics"},
    "1.6": {"top_customer_share", "customer_concentration"},
    "1.7": {"gross_margin_from_ledger", "gross_margin"},
    "1.8": {"cumulative_column_shown_as_active", "vanity_metric"},
    "1.9": {"unit_economics"},
    "1.10": {"cap_table_reconcile", "cap_table"},
    "1.11": {"cannot_settle"},
    "1.12": {"mrr_column_vs_subscription_rows", "billings_vs_recognised_revenue", "gross_vs_net_revenue",
             "gross_margin_from_ledger", "contractor_spend_vs_headcount_and_burn",
             "capitalised_spend_vs_pnl_and_cash", "deferred_revenue_vs_earned",
             "one_time_fees_in_recurring_metrics", "accounting_mislabels"},
    "1.13": {"cancellable_within_notice_vs_arr", "pilot_without_duty_to_convert_vs_recurring",
             "plan_revenue_past_term_end", "signed_not_live_vs_revenue", "contract_price_vs_counted_price",
             "counted_line_without_contract", "contract_terms"},
    "2.1": {"public_comps"}, "2.2": {"private_rounds"},
    "3.1": {"signals_hiring_traffic_reviews"}, "3.2": {"signals_pricing_wins"},
    "4.1": {"video_claims"}, "4.3": {"spoken_arr_vs_claims_page", "three_way"},
    "5.6": {"market_size"}, "6.1": {"founder_market_fit"}, "6.2": {"passion_commitment"},
    "7.1": {"online_footprint"}, "7.2": {"reddit_saved"},
}

# Rows that name one check inside a many-check entry (1.12 kinds, 1.13 checks).
ROW_CHECKS = {
    "C06": {"mrr_column_vs_subscription_rows"}, "C07": {"billings_vs_recognised_revenue"},
    "C08": {"gross_vs_net_revenue"}, "C09": {"deferred_revenue_vs_earned"},
    "C10": {"one_time_fees_in_recurring_metrics"}, "C25": {"contractor_spend_vs_headcount_and_burn"},
    "C26": {"capitalised_spend_vs_pnl_and_cash"}, "C31": {"gross_margin_from_ledger", "gross_margin"},
    "C38": {"cancellable_within_notice_vs_arr"},
    "C39": {"pilot_without_duty_to_convert_vs_recurring", "arr_from_subscription_rows", "arr_definition"},
    "C40": {"plan_revenue_past_term_end"}, "C41": {"signed_not_live_vs_revenue"},
    "C42": {"contract_price_vs_counted_price"}, "C43": {"counted_line_without_contract"},
}

# Guides whose title does not match a checklist item name.
GUIDE_OVERRIDES = {
    "ai-and-data-governance-documents.md": ["C102", "C103", "C104", "C105", "C106", "C107", "C108", "C109"],
    "customer-references-and-letters-of-intent.md": ["C35"],
    "cap-table.md": ["C72", "C95"],
    "material-agreements-other-than-customer-contracts.md": ["C98"],
}

# Words that tie a gap to checklist document rows, for dedupe.
GAP_WORDS = {
    "C03": ("revenue by customer", "customer file", "customer_mrr"),
    "C34": ("order form", "pilot agreement", "customer contract"),
    "C23": ("expense ledger",), "C21": ("bank statement",),
    "C75": ("signed safe", "safe document", "convertible note"),
    "C78": ("option grant", "grant record"), "C76": ("ip assignment", "invention assignment"),
    "C01": ("accountant-prepared", "audited", "reviewed financ"), "C79": ("tax return",),
    "C35": ("customer reference",), "C14": ("cohort",), "C19": ("financial model",), "C72": ("cap table",),
    "C20": ("balance sheet", "monthly p&l", "cash flow statement"),
}

# Rows that make the same request to the founder; the first folds into the second.
SAME_REQUEST = {"C46": "C35"}

# FRAMEWORKS 1.11: asked after the term sheet.
AFTER_TERM_SHEET = {"C01", "C21", "C79"}

# Founder asks, written here because no guide covers them.
ASK_TEXT = {
    "C29": "Please send the current monthly burn and the bank balance behind it, with the date.",
    "C58": "Please send names of people who have worked with the founders that we could call.",
    "C71": "Please be ready to walk us from the source data to each number we ask about.",
}


@dataclass(frozen=True)
class Row:
    id: str
    piece: str
    kind: str
    item: str
    stage: dict
    checked_by: str
    check_exists: bool
    hollis_voice_file: str
    entries: tuple = field(default_factory=tuple)

    @property
    def readout_piece(self) -> str:
        return PIECES[self.piece]


def load(path: Path = CHECKLIST_CSV) -> list[Row]:
    """Read checklist.csv. An unknown stage level or piece stops the load."""
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            stage = {s: r[s] for s in STAGES}
            bad = [v for v in stage.values() if v not in LEVELS]
            if bad:
                raise ValueError(f"checklist row {r['id']} has stage value {bad[0]!r}")
            if r["piece"] not in PIECES:
                raise ValueError(f"checklist row {r['id']} has piece {r['piece']!r}")
            entries = tuple(dict.fromkeys(re.findall(r"\b(\d\.\d{1,2})\b", r["checked_by"])))
            rows.append(Row(r["id"], r["piece"], r["kind"], r["item"], stage, r["checked_by"],
                            r["check_exists"] == "yes", r["hollis_voice_file"], entries))
    return rows


def expected(level: str) -> bool:
    return level in EXPECTED


def room_files(room_dir: Path) -> list[str]:
    room = Path(room_dir)
    return sorted(str(p.relative_to(room)) for p in room.rglob("*") if p.is_file() and not p.name.startswith("."))


def _contained(rule, files, room_dir):
    from schema.readers import pdf_pages, xlsx_sheet, xlsx_sheet_names

    file_pat, look, where = rule
    for f in files:
        if not re.search(file_pat, f):
            continue
        path = Path(room_dir) / f if room_dir else None
        try:
            if where == "file":
                return [f], None
            if path is None:
                continue
            if where == "sheet":
                hit = next((s for s in xlsx_sheet_names(path) if re.search(look, s, re.I)), None)
                if hit:
                    return [f], f"sheet {hit}"
            elif where == "sheet_text":
                for s in xlsx_sheet_names(path):
                    for row in xlsx_sheet(path, s):
                        if any(isinstance(c, str) and re.search(look, c, re.I) for c in row):
                            return [f], f"stated inside sheet {s}"
            elif where == "page":
                for n, text in enumerate(pdf_pages(path), start=1):
                    if re.search(look, text, re.I):
                        return [f], f"page {n}"
        except Exception:  # an unreadable file is not a match
            continue
    return [], None


def match_document(row: Row, files: list[str], room_dir: Path | None = None) -> list[str]:
    return match_document_with_note(row, files, room_dir)[0]


def match_document_with_note(row: Row, files: list[str], room_dir: Path | None = None):
    pat = DOC_PATTERNS.get(row.id)
    if pat:
        hits = [f for f in files if re.search(pat, f.lower()) and not re.search(r"(^|/)sow_", f.lower())]
        if hits:
            return hits, None
    rule = CONTAINED.get(row.id)
    if rule:
        return _contained(rule, files, room_dir)
    return [], None


@lru_cache(maxsize=1)
def guide_asks() -> dict:
    """Checklist id -> (guide path, the guide's one-line request when the document is missing)."""
    out = {}
    if not GUIDES.exists():
        return out
    names = {r.id: r.item.lower() for r in load() if r.kind == "document"}
    for g in sorted(GUIDES.glob("*.md")):
        if g.name in ("INDEX.md", "00_brief.md"):
            continue
        text = g.read_text(encoding="utf-8")
        title = text.splitlines()[0].lstrip("# ").strip().lower()
        sec = re.search(r"^## [^\n]*[Mm]issing[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
        ask = None
        if sec:
            q = (re.search(r"\"((?:Please|Send|If)[^\"\n]{25,})\"", sec.group(1))
                 or re.search(r"\"([^\"\n]{30,})\"", sec.group(1)))
            ask = q.group(1) if q else None
        ids = GUIDE_OVERRIDES.get(g.name) or [
            i for i, n in names.items() if n == title or title.startswith(n) or n.startswith(title)]
        for i in ids:
            out[i] = (str(g.relative_to(ROOT)), ask)
    return out


def items_for_gap(gap: Gap) -> list[str]:
    """The checklist document rows a gap's text names. Shared by coverage and the ask-list step."""
    def hits(text):
        text = text.lower()
        return [cid for cid, words in GAP_WORDS.items() if any(w in text for w in words)]

    # The gap's "what" names the missing thing; "would_need" may list alternatives
    # ("balance sheets, or invoices and revenue by customer"), so it is read only when "what" names nothing.
    return hits(gap.what) or hits(gap.would_need)


def gap_is_asked(asks: list[AskItem], gap: Gap) -> bool:
    """True when a line already requests what this gap would need. The ask-list step calls
    this before it writes a gap line, so coverage's lines are never repeated. Coverage writes
    the line for every gap that names a checklist item, so such a gap is always asked once
    coverage has run."""
    need = gap.would_need.strip().lower()
    items = set(items_for_gap(gap))
    return any(a.what.strip().lower() == need or (a.from_kind == "gap" and a.why == gap.what)
               or (a.checklist_id in items) for a in asks)


def check_names(claim_check_name: str) -> str:
    return claim_check_name[:-5] if claim_check_name.endswith(".read") else claim_check_name
