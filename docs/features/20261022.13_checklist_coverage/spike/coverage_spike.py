"""Checklist coverage spike: mark each checklist item for a room at a stage, and build the ask list.

Throwaway spike for the checklist-coverage slice. It is not the product module.
The product module is planned as scans/memo/coverage.py (see ../04_architecture.md).

Run from the repo root:

    python3 docs/features/20261022.13_checklist_coverage/spike/coverage_spike.py \
        data_room/hollis_voice_seed_drop --stage series_a \
        --gaps docs/features/20261022.13_checklist_coverage/spike/sample_gaps_seed_drop.json \
        --out docs/features/20261022.13_checklist_coverage/spike/out/seed_drop_series_a.json

Leave out --stage to read the stage from the deck's cover or round slide.

What it does, in order:

1. Reads docs/ongoing/checklist.csv.
2. Reads the stage from the deck (pypdf if importable, else pdftotext, else claims.json),
   unless --stage is given. An unreadable or unknown stage gives label "stage_unknown".
3. Marks every item: found, checked, missing, not_checked or not_expected.
   - A document row is found when a room file matches it: the hollis_voice_file column first,
     then file-name patterns. A match the column qualifies (for example "terms stated there;
     no SAFE documents") is still found, with the qualifier kept as found_note.
   - A check row is "checked" only as a PROJECTION. No scan has run. The spike marks a check row
     checked when its FRAMEWORKS entry exists and every input document it reads is in the room.
     The product marks it checked only when a readout claim carries that entry's check name.
   - A check row whose inputs are not in the room is missing, and its ask is folded into the
     ask for the input document (one request, never two).
   - A check row with no entry yet ("not checked yet") whose inputs are present is not_checked.
   - An outside row is never asked of the founder. Checked (projected) when its entry exists.
   - An ask row (kind "ask") is missing by definition and becomes its own request.
4. Reads the cap table's SAFE block (openpyxl if importable) and writes one gap per instrument
   with no document in the room. This stands in for entry 1.10's model reading (row C82).
5. Builds the ask list: gaps from --gaps and step 4 first, then checklist lines. A checklist
   item that a gap line already requests adds no line; its id is attached to that gap line.

Every room in data_room/ is synthetic. The output says so.
"""
import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
CHECKLIST = REPO / "docs/ongoing/checklist.csv"
GUIDES = REPO / "docs/reports/20261022.03_document_guides"

STAGES = ["pre_seed", "seed", "series_a"]
STAGE_WORDS = {"pre-seed": "pre_seed", "preseed": "pre_seed", "seed": "seed", "series a": "series_a"}
EXPECTED = {"yes", "lighter"}

# Checklist piece -> readout Piece enum (FRAMEWORKS "Piece verdicts"). None means no readout piece owns it.
PIECE_MAP = {
    "traction and revenue": "traction_and_revenue",
    "retention": "retention",
    "burn and runway": "burn_and_runway",
    "unit economics": "unit_economics",
    "customers and contracts": "customers",
    "market": "market",
    "comps": "comps",
    "team": "team",
    "the pitch itself": "the_pitch_itself",
    "legal and cap table": None,
    "AI and data governance": None,
    "outside world": None,
}
PIECE_ORDER = ["traction_and_revenue", "retention", "burn_and_runway", "unit_economics", "customers",
               "market", "comps", "team", "the_pitch_itself", None]

# File-name patterns per document row. Used when hollis_voice_file names no file in this room.
DOC_PATTERNS = {
    "C01": r"audit|reviewed_financials", "C02": r"monthly_metrics|kpi|metrics_export",
    "C03": r"revenue_by_customer|customer_mrr", "C04": r"investor_update",
    "C14": r"cohort", "C19": r"financial_model", "C20": r"p_and_l|pnl|balance_sheet|cash_flow|historical_fin",
    "C21": r"bank_statement", "C22": r"hiring_plan", "C23": r"expense_ledger|expense_breakdown",
    "C30": r"unit_economics", "C34": r"order_form|msa_|pilot_agreement|customer_contract",
    "C35": r"letter_of_intent|loi_|customer_reference", "C36": r"pipeline", "C47": r"market_siz|competitive",
    "C53": r"founder_bio", "C54": r"org_chart|team_bio|founder_bios", "C59": r"cover_note|index",
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

# Check rows -> the document rows they read, from checklist.csv's "where" column, by hand.
# A check row with no entry here reads nothing in the room (outside rows, the bank feed, the stale-file check).
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

# Guides whose title does not match a checklist item name.
GUIDE_OVERRIDES = {
    "ai-and-data-governance-documents.md": ["C102", "C103", "C104", "C105", "C106", "C107", "C108", "C109"],
    "customer-references-and-letters-of-intent.md": ["C35"],
    "cap-table.md": ["C72", "C95"],
    "material-agreements-other-than-customer-contracts.md": ["C98"],
}

# Words that tie a gap's would_need text to checklist document rows (for dedupe).
GAP_WORDS = {
    "C03": ["revenue by customer", "customer file", "customer_mrr"],
    "C34": ["order form", "pilot agreement", "customer contract"],
    "C23": ["expense ledger"], "C21": ["bank statement"], "C75": ["signed safe", "safe document", "convertible note"],
    "C78": ["option grant", "grant record"], "C76": ["ip assignment", "invention assignment"],
    "C01": ["accountant", "audited", "reviewed financ"], "C79": ["tax return"], "C35": ["customer reference"],
    "C14": ["cohort"], "C19": ["financial model"], "C72": ["cap table"],
}

# Two checklist rows that make the same request to the founder. The first folds into the second.
# C46 (customer reference calls, an ask) and C35 (customer references, a document): the C35 guide's
# ask line already asks for names and contacts of customers to call.
SAME_REQUEST = {"C46": "C35"}

AFTER_TERM_SHEET = {"C01", "C21", "C79"}  # FRAMEWORKS 1.11: asked after the term sheet.


def load_checklist(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def room_files(room):
    return sorted(str(p.relative_to(room)) for p in room.rglob("*") if p.is_file())


def deck_text(room):
    deck = room / "01_overview/pitch_deck.pdf"
    if not deck.exists():
        return None, None
    try:
        import pypdf  # optional
        pages = [p.extract_text() or "" for p in pypdf.PdfReader(str(deck)).pages]
        return pages, "pypdf"
    except ImportError:
        pass
    if shutil.which("pdftotext"):
        out = subprocess.run(["pdftotext", "-layout", str(deck), "-"], capture_output=True, text=True).stdout
        return out.split("\f"), "pdftotext"
    return None, None


def read_stage(room):
    """Return (stage or None, source dict). Never guesses."""
    pages, how = deck_text(room)
    pattern = re.compile(r"^\s*(Pre-seed|Preseed|Seed|Series [A-Z])\s*\|", re.I | re.M)
    if pages:
        for i, text in enumerate(pages):
            m = pattern.search(text)
            if m:
                word = re.sub(r"\s+", " ", m.group(1).lower())
                return STAGE_WORDS.get(word), {
                    "kind": "file", "uri": "01_overview/pitch_deck.pdf", "locator": f"slide {i + 1}",
                    "quote": m.group(0).strip(), "read_with": how, "word": m.group(1)}
    claims = room / "01_overview/claims.json"
    if claims.exists():
        for c in json.loads(claims.read_text()).get("claims", []):
            m = re.match(r"(Pre-seed|Seed|Series [A-Z]) raise", c.get("label", ""), re.I)
            if m:
                word = m.group(1).lower()
                return STAGE_WORDS.get(word), {"kind": "file", "uri": "01_overview/claims.json",
                                               "locator": f"label '{c['label']}'", "quote": c["label"],
                                               "read_with": "json", "word": m.group(1)}
    return None, None


def match_document(row, files, room):
    """Return (paths, note) for a document row."""
    col = row["hollis_voice_file"].strip()
    if col and not col.startswith("not in the room"):
        m = re.match(r"([\w./-]+)", col)
        path = m.group(1) if m else ""
        note = col[len(path):].strip(" ,") or None
        if path.endswith("/"):
            hits = [f for f in files if f.startswith(path)]
            if hits:
                return hits, note
        elif path in files:
            return [path], note
    pat = DOC_PATTERNS.get(row["id"])
    if pat:
        hits = [f for f in files if re.search(pat, f.lower())]
        if hits:
            return hits, "matched by file name"
    return [], None


def load_guides():
    """Map checklist id -> (guide file, ask line) from each guide's 'If it is missing' section."""
    out = {}
    if not GUIDES.exists():
        return out
    rows = load_checklist(CHECKLIST)
    names = {r["id"]: r["item"].lower() for r in rows if r["kind"] == "document"}
    for g in sorted(GUIDES.glob("*.md")):
        if g.name in ("INDEX.md", "00_brief.md"):
            continue
        text = g.read_text()
        title = text.splitlines()[0].lstrip("# ").strip().lower()
        sec = re.search(r"^## [^\n]*[Mm]issing[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
        ask = None
        if sec:
            q = (re.search(r"\"((?:Please|Send|If)[^\"\n]{25,})\"", sec.group(1))
                 or re.search(r"\"([^\"\n]{30,})\"", sec.group(1)))
            ask = q.group(1) if q else None
        ids = GUIDE_OVERRIDES.get(g.name) or [i for i, n in names.items()
                                               if n == title or title.startswith(n) or n.startswith(title)]
        for i in ids:
            out[i] = {"guide": str(g.relative_to(REPO)), "ask": ask}
    return out


def cap_table_instrument_gaps(room, files):
    """Stand-in for entry 1.10's model reading (row C82): one gap per instrument with no document."""
    path = room / "02_financials/cap_table.xlsx"
    if not path.exists():
        return [], "no cap table"
    try:
        import openpyxl  # optional
    except ImportError:
        return [], "openpyxl not installed; skipped"
    ws = openpyxl.load_workbook(path, data_only=True).worksheets[0]
    gaps, in_safe = [], False
    for r, row in enumerate(ws.iter_rows(values_only=True), start=1):
        first = row[0] if row else None
        if first == "SAFE conversion":
            in_safe = True
            continue
        if in_safe and first in ("Investor",):
            continue
        if in_safe and isinstance(first, str) and first.startswith("Total"):
            in_safe = False
            continue
        if in_safe and isinstance(first, str):
            slug = re.sub(r"\W+", "_", first.lower())
            if not any("safe" in f.lower() and slug[:8] in f.lower() for f in files):
                gaps.append({"what": f"Not in the room: the signed SAFE for {first}",
                             "why": "file missing", "would_need": f"the signed SAFE document for {first}",
                             "source": {"uri": "02_financials/cap_table.xlsx", "locator": f"Cap_Table!A{r}",
                                        "quote": first}, "from": "1.10 instrument reading (spike stand-in)"})
        if isinstance(first, str) and first.startswith("Options granted"):
            if not any(re.search(DOC_PATTERNS["C78"], f.lower()) for f in files):
                gaps.append({"what": f"Not in the room: the option grant records behind '{first}'",
                             "why": "file missing", "would_need": "the option grant records for every holder",
                             "source": {"uri": "02_financials/cap_table.xlsx", "locator": f"Cap_Table!A{r}",
                                        "quote": first}, "from": "1.10 instrument reading (spike stand-in)"})
    return gaps, "read"


def gap_items(gap):
    text = (gap["would_need"] + " " + gap["what"]).lower()
    return [cid for cid, words in GAP_WORDS.items() if any(w in text for w in words)]


def build(room, stage, stage_source, gaps_in, checklist_path):
    rows = load_checklist(checklist_path)
    by_id = {r["id"]: r for r in rows}
    files = room_files(room)
    guides = load_guides()
    out = {
        "framework": "checklist_coverage", "synthetic": "Every room in data_room/ is synthetic. Not a real company.",
        "room": str(room.relative_to(REPO)) if room.is_relative_to(REPO) else str(room),
        "room_files": len(files), "stage": stage, "stage_source": stage_source,
        "claims": [], "gaps": [], "coverage": [], "asks": [], "notes": [],
    }
    if stage not in STAGES:
        out["label"] = "stage_unknown"
        out["label_reason"] = ("No round slide states pre-seed, seed or Series A, and no stage was set. "
                               "The operator picks the stage." if stage_source is None else
                               (f"The stage given, '{stage_source['word']}', is not pre-seed, seed or Series A. "
                                if stage_source.get("set_by") else
                                f"The deck says '{stage_source['word']}', which is not pre-seed, seed or Series A. ")
                               + "The operator picks the stage.")
        return out
    out["label"] = "built"

    found = {}
    for r in rows:
        if r["kind"] == "document":
            found[r["id"]] = match_document(r, files, room)

    cov = {}
    for r in rows:
        level = r[stage]
        rec = {"item_id": r["id"], "item": r["item"], "kind": r["kind"], "checklist_piece": r["piece"],
               "piece": PIECE_MAP[r["piece"]], "expected": level, "status": None, "projected": False,
               "found_in": [], "found_note": None, "check_entry": r["checked_by"] if r["check_exists"] == "yes" else None,
               "missing_inputs": [], "claim_ids": [], "ask": None}
        if r["kind"] == "document":
            paths, note = found[r["id"]]
            rec["found_in"], rec["found_note"] = paths, note
            if paths:
                rec["status"] = "found"
            elif level in EXPECTED:
                rec["status"] = "missing"
            else:
                rec["status"] = "not_expected"
        elif r["kind"] == "check":
            inputs = CHECK_INPUTS.get(r["id"], [])
            missing = [i for i in inputs if not found.get(i, ([], None))[0]]
            rec["missing_inputs"] = missing
            later = [i for i in missing if by_id[i][stage] not in EXPECTED]
            if level not in EXPECTED:
                rec["status"] = "not_expected"
            elif missing and later:
                # An input the stage does not expect: never asked for, so the check cannot run yet.
                rec["status"] = "not_checked"
                rec["found_note"] = "needs " + ", ".join(later) + ", not expected at this stage"
            elif missing:
                rec["status"] = "missing"
            elif r["check_exists"] == "yes":
                rec["status"], rec["projected"] = "checked", True
            else:
                rec["status"] = "not_checked"
        elif r["kind"] == "outside":
            if level not in EXPECTED:
                rec["status"] = "not_expected"
            elif r["check_exists"] == "yes":
                rec["status"], rec["projected"] = "checked", True
            else:
                rec["status"] = "not_checked"
        else:  # ask the founder
            rec["status"] = "missing" if level in EXPECTED else "not_expected"
        cov[r["id"]] = rec

    # Gaps: given (simulated scan gaps) plus the cap table instrument reading.
    inst_gaps, inst_note = cap_table_instrument_gaps(room, files)
    out["notes"].append(f"cap table instrument reading: {inst_note}")
    gaps = list(gaps_in) + inst_gaps
    out["gaps"] = gaps

    asks = []
    claimed = {}  # checklist id -> ask index, for dedupe

    def strongest(ids):
        return "yes" if any(by_id[i][stage] == "yes" for i in ids) else "lighter"

    suppressed = []
    for g in gaps:
        items = [i for i in gap_items(g)]
        levels = [by_id[i][stage] for i in items]
        if items and not any(l in EXPECTED for l in levels):
            # FRAMEWORKS "Checklist coverage": never ask for an item expected only at a later stage.
            suppressed.append({"gap": g["what"], "covers": items, "reason": f"not expected at {stage}"})
            continue
        piece = g.get("piece")
        for i in items:
            if piece is None and PIECE_MAP[by_id[i]["piece"]]:
                piece = PIECE_MAP[by_id[i]["piece"]]
        asks.append({"what": g["would_need"], "why": g["what"], "piece": piece, "from_kind": "gap",
                     "claim_ids": [], "checklist_id": items[0] if items else None, "covers": list(items),
                     "if_you_have_it": bool(items) and all(l == "lighter" for l in levels if l in EXPECTED), "ask_stage": "before_second_meeting", "guide": None})
        for i in items:
            claimed.setdefault(i, []).append(len(asks) - 1)

    # Checklist lines: missing documents and asks; missing checks fold into their input documents.
    want = {}  # document or ask id -> list of checklist ids it covers
    for cid, rec in cov.items():
        if rec["status"] != "missing":
            continue
        if rec["kind"] in ("document", "ask"):
            want.setdefault(SAME_REQUEST.get(cid, cid), []).append(cid)
        elif rec["kind"] == "check":
            for inp in rec["missing_inputs"]:
                want.setdefault(inp, []).append(cid)

    for target in sorted(want, key=lambda c: int(c[1:])):
        covered = sorted(set(want[target]), key=lambda c: int(c[1:]))
        if target in claimed:  # a gap already asks for it: attach, do not repeat
            for idx in claimed[target]:
                for c in covered:
                    if c not in asks[idx]["covers"]:
                        asks[idx]["covers"].append(c)
            for c in covered:
                cov[c]["ask"] = f"ask-{claimed[target][0] + 1:02d}"
            continue
        row = by_id[target]
        level = strongest([c for c in covered if by_id[c][stage] in EXPECTED] or [target])
        guide = guides.get(target)
        if row["kind"] == "ask":
            what = {"C29": "Please send the current monthly burn and the bank balance behind it, with the date.",
                    "C71": "Please be ready to walk from the source data to each flagged number (one line per flag once the scans run).",
                    "C46": "Please send names and contacts for customers we can call.",
                    "C58": "Please send names of people who have worked with the founders."}.get(target, row["item"])
        elif guide and guide["ask"]:
            what = guide["ask"]
        else:
            what = f"Please send: {row['item']}."
        checks = [c for c in covered if c != target]
        why = f"Not in the room: {row['item']}."
        if checks:
            why += " Also needed for " + ", ".join(f"{c} ({by_id[c]['item'][:60]})" for c in checks) + "."
        asks.append({"what": what, "why": why, "piece": PIECE_MAP[row["piece"]], "from_kind": "checklist",
                     "claim_ids": [], "checklist_id": target, "covers": covered,
                     "if_you_have_it": level == "lighter",
                     "ask_stage": "after_term_sheet" if target in AFTER_TERM_SHEET else "before_second_meeting",
                     "guide": guide["guide"] if guide else None})
        for c in covered:
            cov[c]["ask"] = f"ask-{len(asks):02d}"

    # Order: pieces in overview order; inside a piece, gaps first, then checklist lines.
    asks.sort(key=lambda a: (PIECE_ORDER.index(a["piece"]), 0 if a["from_kind"] == "gap" else 1))
    # Renumber ids after sorting, and point coverage at the new ids.
    old_to_new = {}
    for n, a in enumerate(asks, start=1):
        for c in a["covers"]:
            old_to_new[c] = f"ask-{n:02d}"
        a["id"] = f"ask-{n:02d}"
    for c, rec in cov.items():
        if rec["ask"]:
            rec["ask"] = old_to_new.get(c, rec["ask"])

    out["coverage"] = list(cov.values())
    out["asks"] = asks
    out["suppressed_asks"] = suppressed
    out["counts"] = counts(out)
    if stage_source and stage_source.get("uri"):
        out["label_reason"] = f"Stage {stage} read from {stage_source['uri']}, {stage_source['locator']}: '{stage_source['quote']}'."
    else:
        said = (stage_source or {}).get("deck_said")
        out["label_reason"] = f"Stage {stage} set by the operator." + (
            f" The deck says '{said['quote']}' ({said['uri']}, {said['locator']})." if said else "")
    return out


def counts(out):
    c = {"items": len(out["coverage"])}
    for key in ["checked", "found", "missing", "not_checked", "not_expected"]:
        c[key] = sum(1 for r in out["coverage"] if r["status"] == key)
    c["expected"] = sum(1 for r in out["coverage"] if r["expected"] in EXPECTED)
    c["expected_yes"] = sum(1 for r in out["coverage"] if r["expected"] == "yes")
    c["expected_lighter"] = sum(1 for r in out["coverage"] if r["expected"] == "lighter")
    c["found_not_expected"] = sum(1 for r in out["coverage"] if r["status"] == "found" and r["expected"] not in EXPECTED)
    c["checked_projected"] = sum(1 for r in out["coverage"] if r["status"] == "checked" and r["projected"])
    c["missing_by_kind"] = {k: sum(1 for r in out["coverage"] if r["status"] == "missing" and r["kind"] == k)
                            for k in ["document", "check", "outside", "ask"]}
    c["ask_lines"] = len(out["asks"])
    c["ask_lines_required"] = sum(1 for a in out["asks"] if not a["if_you_have_it"])
    c["ask_lines_if_you_have_it"] = sum(1 for a in out["asks"] if a["if_you_have_it"])
    c["ask_lines_from_gaps"] = sum(1 for a in out["asks"] if a["from_kind"] == "gap")
    c["ask_lines_after_term_sheet"] = sum(1 for a in out["asks"] if a["ask_stage"] == "after_term_sheet")
    whats = [a["what"].strip().lower() for a in out["asks"]]
    gap_targets = {i for a in out["asks"] if a["from_kind"] == "gap" for i in a["covers"]}
    list_targets = [a["checklist_id"] for a in out["asks"] if a["from_kind"] == "checklist"]
    c["duplicate_requests"] = (len(whats) - len(set(whats))) + (len(list_targets) - len(set(list_targets))) \
        + sum(1 for t in list_targets if t in gap_targets)
    c["asks_suppressed_later_stage"] = len(out.get("suppressed_asks", []))
    expected_missing = {r["item_id"] for r in out["coverage"] if r["status"] == "missing"}
    with_ask = {r["item_id"] for r in out["coverage"] if r["status"] == "missing" and r["ask"]}
    c["missing_without_ask"] = len(expected_missing - with_ask)
    c["asks_for_not_expected_items"] = sum(
        1 for a in out["asks"] if a["from_kind"] == "checklist"
        and all(r["expected"] not in EXPECTED for r in out["coverage"] if r["item_id"] in a["covers"]))
    return c


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("room")
    ap.add_argument("--stage", help="pre_seed, seed or series_a; overrides the deck")
    ap.add_argument("--gaps", help="JSON file with a list of Gap objects (simulated scan gaps)")
    ap.add_argument("--checklist", default=str(CHECKLIST))
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    room = Path(args.room).resolve()
    deck_stage, deck_src = read_stage(room)
    if args.stage:
        stage, src = args.stage, {"set_by": "operator", "deck_said": deck_src}
        if stage not in STAGES:
            src["word"] = stage
    else:
        stage, src = deck_stage, deck_src
    gaps = json.loads(Path(args.gaps).read_text())["gaps"] if args.gaps else []
    out = build(room, stage, src, gaps, Path(args.checklist))
    text = json.dumps(out, indent=2)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n")
    c = out.get("counts", {})
    print(f"room={out['room']} stage={out['stage']} label={out['label']}")
    if c:
        print("  " + " ".join(f"{k}={v}" for k, v in c.items() if not isinstance(v, dict)))
        print("  missing_by_kind=" + json.dumps(c["missing_by_kind"]))
    else:
        print("  " + out["label_reason"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
