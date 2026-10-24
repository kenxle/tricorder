"""Synthetic data rooms for steps 5 to 8 of the prototype: Ploy in full, Sazabi lighter.

These rooms do not exist as files. The team invents them for the demo, and every screen says so.
The shapes follow what the real engine writes (out/<room>/readout.json: top_flags, pieces with a
verdict and a one-line reason, claims with sources, gaps, panels) and FRAMEWORKS.md, "Piece verdicts".

Rules held here:
- Where the public record states a figure (Form D amounts, prices, team size), the room repeats it,
  taken from the parsed public facts. Planted problems sit between two invented room documents only.
- Every derived figure (ARR, gross margin, runway, shares) is computed below, never typed.
- Invented names are fictional. The room names no real customer or investor.
"""

from __future__ import annotations

import math

NOTICE = "Synthetic data room for Deal Flow NYC 2026. Written by the team. Not this company's data."


def money(n: float) -> str:
    return f"${n:,.0f}"


def millions(n: float) -> str:
    return f"${n / 1_000_000:.1f}M"


def pct(x: float, places: int = 1) -> str:
    return f"{x * 100:.{places}f}%"


def src(uri: str, locator: str, quote: str) -> dict:
    return {"uri": uri, "locator": locator, "quote": quote}


def public(key: str, label: str) -> dict:
    """An outside source: a pre-room claim, which opens its saved public source."""
    return {"public": key, "uri": label, "locator": "public record"}


def strip(values: list[float], band: float, ticks: list[dict], unit: str, step: float) -> dict:
    lo = min(values + [band])
    hi = max(values + [band])
    pad = (hi - lo) * 0.25 or step
    mn = math.floor((lo - pad) / step) * step
    mx = math.ceil((hi + pad) / step) * step
    for t in ticks:
        t["out"] = abs(t["v"] - band) > abs(band) * 0.01
    return {"min": mn, "max": mx, "band": band, "ticks": ticks, "unit": unit}


def relative_gap(stated: float, found: float) -> float:
    return abs(stated - found) / abs(found)


def runway(cash: float, base_burn: float, extra_hires: list[dict], pace: float = 1.0, revenue_change: float = 0.0) -> float:
    """Months until the cash runs out, month by month. Extra hires add their monthly cost from their start month."""
    left, m = cash, 0
    while m < 120:
        m += 1
        burn = base_burn - revenue_change + pace * sum(h["monthly_cost"] for h in extra_hires if h["start"] <= m)
        if burn <= 0:
            return 120.0
        if left < burn:
            return m - 1 + left / burn
        left -= burn
    return 120.0


def file_of(source: dict) -> str | None:
    """The room file a source cites, or None for an outside source."""
    return None if source.get("public") else source["uri"].split(", ")[0]


def with_states(room: dict, partial_files: set[str], extra_flags: list[dict]) -> dict:
    """What the working page can show when only some files have arrived ("partial") and when all have ("full").

    A claim shows once every room file it cites has arrived. A piece keeps its verdict when nothing it
    rests on is missing; a piece with an arrived flag reads looking weak; otherwise it reads "not enough
    yet" and names the files it waits on. A request is answered once all its files are in."""
    C = room["claims"]
    every = {file_of(x) for c in C.values() for x in c["sources"] + c["agree"] + c["disagree"]} - {None}
    every |= {f.split(", ")[0] for v in room["holds"].values() for f in v}
    request_of = {}
    for cid, files in room["holds"].items():
        for f in files:
            request_of.setdefault(f.split(", ")[0], cid)
    labels = {p["name"]: p["label"] for p in room["pieces"]}

    def state(arrived: set[str]) -> dict:
        def ok(c):
            return all(file_of(x) in arrived for x in c["sources"] if file_of(x))
        def missing(c):
            return sorted({file_of(x) for x in c["sources"] if file_of(x) and file_of(x) not in arrived})
        def flag_ok(f):
            return ok(C[f["claim_id"]]) and all(file_of(x) in arrived for x in (f["stated"]["source"], f["found"]["source"]) if file_of(x))
        shown = {cid for cid, c in C.items() if ok(c)}
        flags = {"green": [], "red": []}
        waiting = []
        for kind in ("green", "red"):
            for f in room["top_flags"][kind]:
                if flag_ok(f):
                    flags[kind].append(f["claim_id"])
                else:
                    files = missing(C[f["claim_id"]])
                    waiting.append({"piece": f["piece"], "files": files, "requests": sorted({request_of.get(x) for x in files} - {None}),
                                    "title": f"{labels[f['piece']]}: the check runs when {files[0]} arrives.",
                                    "text": f"Stated so far: {f['stated']['value']}. Tricorder rebuilds it from the file the founder has not sent yet."})
        for f in extra_flags:
            if flag_ok(f) and not any(C[x]["piece"] == f["piece"] for x in flags[f["kind"]]) and arrived != every:
                flags[f["kind"]].append(f["claim_id"])
        pieces = {}
        for p in room["pieces"]:
            gone = [C[x] for x in p["claim_ids"] if x not in shown]
            files = sorted({m for c in gone for m in missing(c)})
            have = [C[x] for x in p["claim_ids"] if x in shown]
            if not gone or all(c["mark"] is None and c["severity"] == "info" for c in gone):
                pieces[p["name"]] = {"verdict": p["verdict"], "reason": p["reason"], "agree": p["agree"], "disagree": p["disagree"], "waiting": files}
            elif any(c["severity"] == "flag" for c in have):
                c = next(c for c in have if c["severity"] == "flag")
                pieces[p["name"]] = {"verdict": "looking_weak", "reason": c["text"], "agree": 0,
                                     "disagree": sum(1 for x in have if x["mark"] == "contradicted"), "waiting": files}
            else:
                pieces[p["name"]] = {"verdict": "not_enough_in_the_room", "reason": f"Not enough yet. Waiting on {', '.join(files)}.",
                                     "agree": 0, "disagree": 0, "waiting": files}
        pre = {}
        for i, pc in enumerate(room["prechecks"]):
            f = file_of(pc["source"])
            pre[i] = pc["status"] if f in arrived else "waiting"
        answered = sorted(cid for cid, files in room["holds"].items() if all(x.split(", ")[0] in arrived for x in files))
        return {"arrived": sorted(arrived), "files_total": len(every), "shown": sorted(shown), "flags": flags, "waiting": waiting,
                "pieces": pieces, "prechecks": pre, "answered": answered, "request_of": request_of}

    room["states"] = {"partial": state(set(partial_files)), "full": state(every)}
    room["extra_flags"] = extra_flags
    return room


# Ploy ------------------------------------------------------------------------------------


def ploy_room(f: dict, pre: dict) -> dict:
    deck = "01_pitch/pitch_deck.pdf"
    model = "02_financials/financial_model.xlsx"
    stmts = "02_financials/monthly_statements.xlsx"
    metrics = "03_metrics/monthly_metrics.csv"
    cust = "03_metrics/customer_mrr_by_month.csv"
    ws = "03_metrics/workspaces_by_plan.csv"
    pilot_form = "04_customers/order_form_northwind_analytics.pdf"
    halden_form = "04_customers/order_form_halden_freight.pdf"
    cap = "05_legal/cap_table.xlsx"
    safes = "05_legal/safe_conversion_schedule.pdf"
    spa = "05_legal/seed_stock_purchase_agreement.pdf"
    claims_stmt = "05_legal/claims_statement.pdf"
    bio = "06_team/founder_bio_bryant_chou.pdf"
    hiring = "06_team/hiring_plan.csv"
    cover = "00_welcome/cover_note_and_index.pdf"

    # The invented base of the room. Prices and team size come from the public record.
    starter_ws, pro_ws = 310, 420
    enterprise = [("Halden Freight", 18000), ("Kestrel Logistics", 14500), ("Marrow and Finch", 12000),
                  ("Tallis Software", 9500), ("Brightline Studio", 8000)]
    pilot_name, pilot_total, pilot_months = "Northwind Analytics", 90000, 3
    credit_ws = 1240
    yc_p26_ws = 26
    hosting, support, inference = 19800, 31570, 60950
    cash = 24_310_000
    model_burn = 810_000
    deck_arr, deck_gm, deck_runway = 2_800_000, 0.78, 30
    raise_amt, pre_money = 25_000_000, 150_000_000
    market_deck_count, market_model_count = 40_000, 36_000
    churn_model = 0.02
    roles = ["Engineer"] * 9 + ["Designer"] * 3 + ["Account executive"] * 4 + ["Marketer"] * 3 + ["Support lead"] * 2 + ["Finance lead"]
    costs = {"Engineer": 21000, "Designer": 17500, "Account executive": 16000, "Marketer": 15000, "Support lead": 12500, "Finance lead": 18500}
    hires = [{"id": f"H{i + 1:02d}", "role": r, "start": 1 + i // 2, "monthly_cost": costs[r], "in_model": i < 6}
             for i, r in enumerate(roles)]

    # What follows is computed.
    self_serve = starter_ws * f["starter"] + pro_ws * f["pro"]
    ent_mrr = sum(v for _, v in enterprise)
    pilot_mrr = pilot_total / pilot_months
    sub_mrr = self_serve + ent_mrr
    model_mrr = sub_mrr + pilot_mrr
    model_arr = 12 * model_mrr
    rebuilt_arr = 12 * sub_mrr
    assert round(model_arr / 100_000) / 10 == deck_arr / 1_000_000, "the deck's ARR must round from the model's"
    paying_ws = starter_ws + pro_ws + len(enterprise) + 1
    revenue = model_mrr
    cogs_model = hosting + support
    gm_model = 1 - cogs_model / revenue
    gm_rebuilt = 1 - (cogs_model + inference) / revenue
    assert round(gm_model * 100) == round(deck_gm * 100), "the deck's margin must round from the model's"
    runway_model = cash / model_burn
    assert round(runway_model) == deck_runway
    extra = [h for h in hires if not h["in_model"]]
    runway_rebuilt = runway(cash, model_burn, extra)
    largest_name, largest = max(enterprise, key=lambda x: x[1])
    largest_share = largest / model_mrr
    batch_share = yc_p26_ws / f["batch_size"]
    assert batch_share * 100 >= f["batch_share_pct"], "the room must agree with the launch post's share"
    annual_price = 12 * f["pro"]
    market_deck = market_deck_count * annual_price
    market_model = market_model_count * annual_price
    post_money = pre_money + raise_amt
    ownership = raise_amt / post_money
    free_ws = credit_ws - paying_ws

    C = {}

    def claim(cid, piece, text, value, display, confidence, sources, mark=None, severity="info", agree=None, disagree=None):
        C[cid] = {"id": cid, "piece": piece, "text": text, "value": value, "display": display, "confidence": confidence,
                  "sources": sources, "mark": mark, "severity": severity, "agree": agree or [], "disagree": disagree or []}
        return cid

    # Traction and revenue
    claim("tr-1", "traction_and_revenue", f"The deck states ARR of {millions(deck_arr)}.", deck_arr, millions(deck_arr), "quoted",
          [src(deck, "slide 5", f"{millions(deck_arr)} ARR")], "contradicted",
          agree=[src(model, "Revenue!H40", f"{model_arr:.0f}")], disagree=[src(cust, "rows 1 to 731, plan column", "Pilot")])
    claim("tr-2", "traction_and_revenue", f"The model's ARR is {money(model_arr)}: twelve times September's MRR of {money(model_mrr)}.",
          model_arr, money(model_arr), "computed", [src(model, "Revenue!H40", f"{model_arr:.0f}")], "contradicted")
    claim("tr-3", "traction_and_revenue",
          f"Rebuilt from the customer file, subscription MRR is {money(sub_mrr)}, so ARR is {money(rebuilt_arr)}. "
          f"The {money(pilot_mrr)} difference is the {pilot_name} pilot: {money(pilot_total)} for {pilot_months} months, booked as monthly recurring revenue.",
          rebuilt_arr, money(rebuilt_arr), "computed",
          [src(cust, "2026-09 rows, plan is not Pilot", f"{sub_mrr:.0f}"), src(pilot_form, "page 1, Fees", f"{money(pilot_total)} for a {pilot_months}-month pilot")],
          "contradicted", "flag")
    claim("tr-4", "traction_and_revenue",
          f"The deck says {credit_ws:,} paying workspaces. The workspace file shows {credit_ws:,} workspaces using credits, of which {paying_ws:,} pay; "
          f"{free_ws:,} are on the free plan.", paying_ws, f"{paying_ws:,}", "computed",
          [src(deck, "slide 6", f"{credit_ws:,} paying workspaces"), src(ws, "2026-09, plan column", f"Free: {free_ws}")], "contradicted", "flag")
    # Retention
    claim("re-1", "retention", f"The model assumes monthly churn of {pct(churn_model)}. Only the model states it.", churn_model, pct(churn_model),
          "quoted", [src(model, "Assumptions!C18", f"{churn_model}")])
    # Burn and runway
    claim("bu-1", "burn_and_runway", f"The deck and the model state {deck_runway} months of runway on {money(cash)} of cash and {money(model_burn)} of monthly burn.",
          deck_runway, f"{deck_runway} months", "quoted",
          [src(deck, "slide 12", f"{deck_runway} months of runway"), src(model, "Assumptions!C9", f"{runway_model:.2f}")], "contradicted")
    claim("bu-2", "burn_and_runway",
          f"The model's burn carries {len(hires) - len(extra)} of the {len(hires)} planned hires. With all {len(hires)} from the hiring plan, runway is {runway_rebuilt:.1f} months.",
          runway_rebuilt, f"{runway_rebuilt:.1f} months", "computed",
          [src(hiring, f"rows H01 to H{len(hires):02d}", f"{len(hires)} hires"), src(model, "Assumptions!C12", "HIRES_IN_MODEL = 6")],
          "contradicted", "flag")
    # Unit economics
    claim("ue-1", "unit_economics", f"The deck states gross margin of {pct(deck_gm, 0)}.", deck_gm, pct(deck_gm, 0), "quoted",
          [src(deck, "slide 7", f"{pct(deck_gm, 0)} gross margin")], "contradicted")
    claim("ue-2", "unit_economics", f"The model's gross margin for 2026-09 is {pct(gm_model)}: cost of revenue is hosting and support only.",
          gm_model, pct(gm_model), "computed", [src(model, "P&L!H31", f"{gm_model:.4f}")], "contradicted")
    claim("ue-3", "unit_economics",
          f"Model inference, {money(inference)} in September, sits under research and development. Counted as cost of revenue, gross margin is {pct(gm_rebuilt)}.",
          gm_rebuilt, pct(gm_rebuilt), "computed",
          [src(stmts, "Ledger!row 214", f"AI infrastructure (R&D) {inference}"), src(model, "P&L!H22", f"{inference}")], "contradicted", "flag")
    claim("ue-4", "unit_economics", f"The model's prices are Starter ${f['starter']} and Pro ${f['pro']} a month, as on the public pricing page.",
          f["pro"], f"${f['pro']}", "quoted", [src(model, "Pricing!B3:B4", f"{f['starter']}, {f['pro']}")], "corroborated",
          agree=[public("prices", "ploy.ai/pricing")])
    # Customers
    claim("cu-1", "customers", f"The deck says no customer is more than 10% of revenue. The largest, {largest_name}, is {pct(largest_share)} of September MRR.",
          largest_share, pct(largest_share), "computed",
          [src(cust, "2026-09, largest row", f"{largest_name},{largest}"), src(deck, "slide 8", "No customer is more than 10% of revenue")],
          "corroborated", agree=[src(halden_form, "page 1, Fees", f"{money(largest)} a month")])
    # Market
    claim("ma-1", "market", f"The deck sizes the market at {money(market_deck)}: {market_deck_count:,} companies at {money(annual_price)} a year.",
          market_deck, money(market_deck), "computed", [src(deck, "slide 9", f"{market_deck_count:,} companies")], "contradicted",
          disagree=[src(model, "Market!B3", f"{market_model_count}")])
    claim("ma-2", "market", f"The model's Market tab counts {market_model_count:,} companies, so {money(market_model)}.", market_model, money(market_model),
          "computed", [src(model, "Market!B3", f"{market_model_count}")], "contradicted")
    claim("ma-3", "market", f"Both use {money(annual_price)} a year per company: the Pro plan's ${f['pro']} a month.", annual_price, money(annual_price),
          "computed", [src(deck, "slide 9", f"{money(annual_price)} a year"), src(model, "Market!B4", f"{annual_price}")], "corroborated",
          agree=[public("prices", "ploy.ai/pricing")])
    # Team
    claim("te-1", "team", f"Staff today: {f['team']} on deck slide 11 and in the model, the same as the YC page.", f["team"], str(f["team"]), "quoted",
          [src(deck, "slide 11", f"{f['team']} people"), src(model, "Assumptions!C4", f"STAFF_NOW = {f['team']}")], "corroborated",
          agree=[public("team", "YC company page")])
    # The pitch itself
    claim("pi-1", "the_pitch_itself", f"Series A: raise {money(raise_amt)} at {money(pre_money)} pre-money, so {pct(ownership, 2)} for the new money.",
          raise_amt, money(raise_amt), "computed", [src(deck, "slide 14", f"{millions(raise_amt)} Series A"), src(model, "Assumptions!C21", f"{raise_amt}")],
          "corroborated")
    claim("pi-2", "the_pitch_itself", f"The deck says {f['batch_share_pct']}% of the batch use Ploy. The workspace file tags {yc_p26_ws} YC P26 companies of {f['batch_size']}, {pct(batch_share)}.",
          batch_share, pct(batch_share), "computed", [src(deck, "slide 6", f"{f['batch_share_pct']}% of YC P26"), src(ws, "tag column, yc_p26", f"{yc_p26_ws}")],
          "corroborated", agree=[public("batch_share", "Launch YC post")])
    # Legal and cap table
    claim("lc-1", "legal_and_cap_table", f"The cap table's seed total is {money(f['sold'])}, the amount sold on the SEC Form D.", f["sold"], money(f["sold"]),
          "quoted", [src(cap, "Seed!F22", f"{f['sold']}")], "corroborated", agree=[public("formd_sold", "SEC Form D")])
    claim("lc-2", "legal_and_cap_table", f"SAFEs that converted into the seed: {money(f['safe'])}, the figure the Form D gives.", f["safe"], money(f["safe"]),
          "quoted", [src(cap, "SAFEs!E9", f"{f['safe']}"), src(safes, "page 2, total", money(f["safe"]))], "corroborated",
          agree=[public("formd_safe", "SEC Form D")])
    claim("lc-3", "legal_and_cap_table", f"The cap table lists {f['investors']} seed holders. The Form D counts {f['investors']} investors.", f["investors"],
          str(f["investors"]), "quoted", [src(cap, f"Seed!A12:A{11 + f['investors']}", f"{f['investors']} rows")], "corroborated",
          agree=[public("formd_investors", "SEC Form D")])
    claim("lc-4", "legal_and_cap_table", "The claims statement says there are no lawsuits, threatened claims or regulator contact.", None, "none",
          "quoted", [src(claims_stmt, "page 1", "There are none.")])
    # The outside world
    claim("ow-1", "outside_world", "Three public facts check out against the room: the prices, the team size and the Form D amount.", 3, "3 of 3",
          "computed", [src(model, "Pricing!B3:B4", "prices"), src(cap, "Seed!F22", "seed total")], "corroborated",
          agree=[public("prices", "ploy.ai/pricing"), public("team", "YC company page"), public("formd_sold", "SEC Form D")])

    def flag(kind, piece, cid, title, stated, found, others, strip_, ask=None, gap=None):
        return {"kind": kind, "piece": piece, "claim_id": cid, "title": title, "stated": stated, "found": found,
                "others": others, "strip": strip_, "ask": ask, "relative_gap": gap}

    reds = [
        flag("red", "traction_and_revenue", "tr-3", f"ARR counts a {pilot_months}-month pilot as recurring revenue.",
             {"key": "Stated, deck slide 5", "value": millions(deck_arr), "out": True, "source": src(deck, "slide 5", f"{millions(deck_arr)} ARR")},
             {"key": "Found, customer file", "value": money(rebuilt_arr), "source": src(cust, "2026-09 rows, plan is not Pilot", f"{sub_mrr:.0f}")},
             [{"key": "Also the model", "value": money(model_arr), "source": src(model, "Revenue!H40", f"{model_arr:.0f}")}],
             strip([deck_arr, model_arr, rebuilt_arr], rebuilt_arr,
                   [{"v": deck_arr, "label": f"Deck {millions(deck_arr)}", "pos": "above"}, {"v": model_arr, "label": f"Model {millions(model_arr)}", "pos": "below"}],
                   "usd", 100_000),
             f"{pilot_name} paid {money(pilot_total)} for a {pilot_months}-month pilot. Has it signed an annual contract? If not, can you show ARR without it?",
             relative_gap(deck_arr, rebuilt_arr)),
        flag("red", "unit_economics", "ue-3", "Gross margin leaves model inference out of cost of revenue.",
             {"key": "Stated, deck slide 7", "value": pct(deck_gm, 0), "out": True, "source": src(deck, "slide 7", f"{pct(deck_gm, 0)} gross margin")},
             {"key": "Found, ledger and model", "value": pct(gm_rebuilt), "source": src(stmts, "Ledger!row 214", f"AI infrastructure (R&D) {inference}")},
             [{"key": "Also the model", "value": pct(gm_model), "source": src(model, "P&L!H31", f"{gm_model:.4f}")}],
             strip([deck_gm * 100, gm_model * 100, gm_rebuilt * 100], gm_rebuilt * 100,
                   [{"v": deck_gm * 100, "label": f"Deck {pct(deck_gm, 0)}", "pos": "above"}, {"v": gm_model * 100, "label": f"Model {pct(gm_model)}", "pos": "below"}],
                   "percent", 5),
             f"Model inference cost {money(inference)} in September and sits under research and development. Why is it not in cost of revenue?",
             relative_gap(deck_gm, gm_rebuilt)),
        flag("red", "burn_and_runway", "bu-2", f"Runway leaves {len(extra)} of the {len(hires)} planned hires out of the burn.",
             {"key": "Stated, deck slide 12", "value": f"{deck_runway} months", "out": True, "source": src(deck, "slide 12", f"{deck_runway} months of runway")},
             {"key": "Found, hiring plan", "value": f"{runway_rebuilt:.1f} months", "source": src(hiring, f"rows H01 to H{len(hires):02d}", f"{len(hires)} hires")},
             [{"key": "Also the model", "value": f"{runway_model:.1f} months", "source": src(model, "Assumptions!C9", f"{runway_model:.2f}")}],
             strip([deck_runway, runway_model, runway_rebuilt], runway_rebuilt,
                   [{"v": deck_runway, "label": f"Deck {deck_runway} mo", "pos": "above"}, {"v": runway_model, "label": f"Model {runway_model:.1f} mo", "pos": "below"}],
                   "months", 2),
             f"The model's burn carries {len(hires) - len(extra)} of the {len(hires)} hires in the hiring plan. What is runway with the full plan, and which hires would you hold?",
             relative_gap(deck_runway, runway_rebuilt)),
    ]
    reds.sort(key=lambda x: -x["relative_gap"])
    greens = [
        flag("green", "legal_and_cap_table", "lc-1", "The cap table's seed matches the SEC Form D to the dollar.",
             {"key": "Room, cap table", "value": money(f["sold"]), "source": src(cap, "Seed!F22", f"{f['sold']}")},
             {"key": "Outside, SEC Form D", "value": money(f["sold"]), "source": public("formd_sold", "SEC Form D")},
             [{"key": "Also SAFEs, in both", "value": money(f["safe"]), "source": src(cap, "SAFEs!E9", f"{f['safe']}")}],
             strip([f["sold"]], f["sold"], [{"v": f["sold"], "label": f"Cap table and Form D {millions(f['sold'])}", "pos": "above"}], "usd", 1_000_000)),
        flag("green", "customers", "cu-1", f"No customer is more than 10% of revenue. The largest is {pct(largest_share)}.",
             {"key": "Stated, deck slide 8", "value": "under 10%", "source": src(deck, "slide 8", "No customer is more than 10% of revenue")},
             {"key": "Found, customer file", "value": pct(largest_share), "source": src(cust, "2026-09, largest row", f"{largest_name},{largest}")},
             [{"key": "Also the order form", "value": f"{money(largest)} a month", "source": src(halden_form, "page 1, Fees", f"{money(largest)} a month")}],
             strip([largest_share * 100], largest_share * 100,
                   [{"v": largest_share * 100, "label": f"Customer file and order form {pct(largest_share)}", "pos": "above"}], "percent", 2)),
    ]

    pieces = [
        {"name": "traction_and_revenue", "label": "Traction and revenue", "verdict": "looking_weak",
         "reason": C["tr-3"]["text"], "agree": 1, "disagree": 3,
         "claim_ids": ["tr-1", "tr-2", "tr-3", "tr-4"]},
        {"name": "retention", "label": "Retention", "verdict": "not_enough_in_the_room",
         "reason": f"Only one source states churn: the model's {pct(churn_model)} a month. The customer file starts in 2026-01, too soon for 12-month retention.",
         "agree": 0, "disagree": 0, "claim_ids": ["re-1"]},
        {"name": "burn_and_runway", "label": "Burn and runway", "verdict": "looking_weak", "reason": C["bu-2"]["text"], "agree": 0, "disagree": 2,
         "claim_ids": ["bu-1", "bu-2"]},
        {"name": "unit_economics", "label": "Unit economics", "verdict": "looking_weak", "reason": C["ue-3"]["text"], "agree": 2, "disagree": 3,
         "claim_ids": ["ue-1", "ue-2", "ue-3", "ue-4"]},
        {"name": "customers", "label": "Customers", "verdict": "looking_strong", "reason": C["cu-1"]["text"], "agree": 3, "disagree": 0,
         "claim_ids": ["cu-1"]},
        {"name": "market", "label": "Market", "verdict": "mixed",
         "reason": f"The deck and the model agree on {money(annual_price)} a year per company. They disagree on the count: {market_deck_count:,} against {market_model_count:,}.",
         "agree": 2, "disagree": 2, "claim_ids": ["ma-1", "ma-2", "ma-3"]},
        {"name": "team", "label": "Team", "verdict": "looking_strong", "reason": C["te-1"]["text"], "agree": 3, "disagree": 0, "claim_ids": ["te-1"]},
        {"name": "the_pitch_itself", "label": "The pitch itself", "verdict": "looking_strong", "reason": C["pi-1"]["text"], "agree": 2, "disagree": 0,
         "claim_ids": ["pi-1", "pi-2"]},
        {"name": "legal_and_cap_table", "label": "Legal and cap table", "verdict": "looking_strong", "reason": C["lc-1"]["text"], "agree": 3, "disagree": 0,
         "claim_ids": ["lc-1", "lc-2", "lc-3", "lc-4"]},
        {"name": "outside_world", "label": "Outside world", "verdict": "looking_strong", "reason": C["ow-1"]["text"], "agree": 3, "disagree": 0,
         "claim_ids": ["ow-1"]},
    ]

    gm_rows = [
        ["Revenue, 2026-09", money(revenue), "Revenue", "Revenue"],
        ["Hosting", money(hosting), "Cost of revenue", "Cost of revenue"],
        ["Support", money(support), "Cost of revenue", "Cost of revenue"],
        ["Model inference", money(inference), "Research and development", "Cost of revenue"],
        ["Gross margin", "", pct(gm_model), pct(gm_rebuilt)],
    ]
    drill = [
        {"piece": "unit_economics", "kind": "weak", "claim_ids": ["ue-1", "ue-2", "ue-3", "ue-4"],
         "panel": {"name": "gross margin rebuild", "columns": ["Line", "Amount", "Where the model books it", "Where the rebuild books it"], "rows": gm_rows},
         "gaps": ["Not in the room: unit economics (acquisition cost, payback). It was on your request and did not come."]},
        {"piece": "legal_and_cap_table", "kind": "strong", "claim_ids": ["lc-1", "lc-2", "lc-3", "lc-4"],
         "panel": {"name": "cap table against the Form D", "columns": ["Figure", "Cap table", "SEC Form D", "Agree"],
                   "rows": [["Seed total sold", money(f["sold"]), money(f["sold"]), "yes"],
                            ["From SAFEs that converted", money(f["safe"]), money(f["safe"]), "yes"],
                            ["Seed investors", str(f["investors"]), str(f["investors"]), "yes"]]},
         "gaps": ["Not in the room: the pro forma cap table after the Series A."]},
    ]

    holds = {
        "C02": [metrics], "C03": [cust], "C34": [pilot_form, halden_form], "C75": [safes, spa], "C72": [cap],
        "C20": [stmts], "C19": [model], "C22": [hiring], "C47": [f"{deck}, slide 9"], "C53": [bio], "C59": [cover],
        "C60": [deck], "C80": [claims_stmt],
    }

    prechecks = [
        {"pre": "formd_sold", "status": "confirms", "room": f"The cap table's seed total is {money(f['sold'])}.", "source": src(cap, "Seed!F22", f"{f['sold']}")},
        {"pre": "formd_safe", "status": "confirms", "room": f"The cap table's SAFE conversions add to {money(f['safe'])}.", "source": src(cap, "SAFEs!E9", f"{f['safe']}")},
        {"pre": "formd_investors", "status": "confirms", "room": f"The cap table lists {f['investors']} seed holders.",
         "source": src(cap, f"Seed!A12:A{11 + f['investors']}", f"{f['investors']} rows")},
        {"pre": "prices", "status": "confirms", "room": f"The model prices Starter at ${f['starter']} and Pro at ${f['pro']}.",
         "source": src(model, "Pricing!B3:B4", f"{f['starter']}, {f['pro']}")},
        {"pre": "team", "status": "confirms", "room": f"The model's staff today is {f['team']}.", "source": src(model, "Assumptions!C4", f"STAFF_NOW = {f['team']}")},
        {"pre": "batch_share", "status": "confirms", "room": f"The workspace file tags {yc_p26_ws} YC P26 companies of {f['batch_size']}, {pct(batch_share)}.",
         "source": src(ws, "tag column, yc_p26", f"{yc_p26_ws}")},
        {"pre": "revenue_range", "status": "answers", "room": f"The room gives September MRR of {money(model_mrr)}, {money(sub_mrr)} of it subscription.",
         "source": src(metrics, "2026-09, mrr", f"{model_mrr:.0f}")},
        {"pre": "hiring", "status": "differs", "room": f"The hiring plan adds {len(hires)} people by month {hires[-1]['start']}. Not a flag: a job board lags a plan.",
         "source": src(hiring, f"rows H01 to H{len(hires):02d}", f"{len(hires)} hires")},
        {"pre": "named_customers", "status": "not settled", "room": "No contract for Hex or Clay is in the room. The room's customers are its own.",
         "source": src(cust, "customer column", "no match")},
    ]

    whatif = {
        "lines": [{"name": "Starter plan", "units": starter_ws, "price": f["starter"]}, {"name": "Pro plan", "units": pro_ws, "price": f["pro"], "tweak": True},
                  {"name": "Enterprise contracts", "units": 1, "price": ent_mrr}],
        "pilot": {"name": pilot_name, "mrr": pilot_mrr}, "company_arr": deck_arr, "rebuilt_arr": rebuilt_arr,
        "churn": churn_model, "cash": cash, "base_burn": model_burn, "company_runway": deck_runway, "rebuilt_runway": round(runway_rebuilt, 1),
        "extra_hires": [{"start": h["start"], "monthly_cost": h["monthly_cost"]} for h in extra], "extra_count": len(extra),
    }

    steer_examples = [
        {"piece": "traction_and_revenue", "sentence": f"Count the {pilot_name} pilot as recurring: it signed an annual contract on October 1.",
         "kind": "figure", "check_value": money(rebuilt_arr), "steer_value": money(model_arr), "label": "ARR"},
        {"piece": "unit_economics", "sentence": "Get the model inference invoices for July to September.", "kind": "more",
         "request": "Model inference invoices, July to September 2026"},
        {"piece": "market", "sentence": f"The deck counts agencies' client sites and the model does not. Use the model's {market_model_count:,}.",
         "kind": "rewrite",
         "reworded": f"Steered: the associate takes the model's {market_model_count:,} companies as the count, so the market is {money(market_model)}. The deck's {market_deck_count:,} includes agencies' client sites."},
    ]

    memo_company = (f"Ploy builds, edits and runs a company's website and marketing with AI agents. It raised a {millions(f['sold'])} seed "
                    f"(SEC Form D, {f['investors']} investors). In this synthetic room it asks for a {millions(raise_amt)} Series A at "
                    f"{millions(pre_money)} pre-money.")

    # The partial state: the founder's first batch. The billing exports, the order forms, the hiring plan and
    # the claims statement come later. The workspace file's flag can show before the customer file arrives.
    partial_files = {deck, cover, model, metrics, ws, cap, safes, spa, bio, stmts}
    extra = [flag("red", "traction_and_revenue", "tr-4", "The deck counts free workspaces as paying ones.",
                  {"key": "Stated, deck slide 6", "value": f"{credit_ws:,}", "out": True, "source": src(deck, "slide 6", f"{credit_ws:,} paying workspaces")},
                  {"key": "Found, workspace file", "value": f"{paying_ws:,}", "source": src(ws, "2026-09, plan column", f"Free: {free_ws}")},
                  [], strip([credit_ws, paying_ws], paying_ws, [{"v": credit_ws, "label": f"Deck {credit_ws:,}", "pos": "above"}], "count", 100),
                  f"The deck says {credit_ws:,} paying workspaces. The workspace file shows {paying_ws:,} paying and {free_ws:,} on the free plan. Which count do you report?",
                  relative_gap(credit_ws, paying_ws))]
    return with_states({
        "synthetic_notice": NOTICE, "as_of": "2026-09-30", "files": sorted({x.split(", ")[0] for v in holds.values() for x in v} | {ws, model}),
        "round": {"name": "Series A", "raise": money(raise_amt), "pre_money": money(pre_money), "post_money": money(post_money),
                  "ownership": pct(ownership, 2), "source": src(deck, "slide 14", f"{millions(raise_amt)} Series A")},
        "top_flags": {"green": greens, "red": reds}, "pieces": pieces, "claims": C, "drill": drill, "holds": holds,
        "prechecks": prechecks, "whatif": whatif, "steer_examples": steer_examples, "memo_company": memo_company,
    }, partial_files, extra)


# Sazabi, lighter --------------------------------------------------------------------------


def sazabi_room(f: dict, pre: dict) -> dict:
    deck = "01_pitch/pitch_deck.pdf"
    model = "02_financials/financial_model.xlsx"
    ws = "03_metrics/workspaces_by_plan.csv"
    cap = "05_legal/cap_table.xlsx"
    hiring = "06_team/hiring_plan.csv"
    hobby, startup, growth = 6, 9, 3
    deck_paying = f["design_partners"]
    cash, burn = 6_900_000, 380_000
    raise_amt, pre_money = 6_000_000, 54_000_000
    churn = 0.03
    hires = [{"start": 1 + i, "monthly_cost": 19000} for i in range(6)]

    mrr = hobby * f["hobby"] + startup * f["startup"] + growth * f["growth"]
    arr = 12 * mrr
    paying = hobby + startup + growth
    free = f["design_partners"] - paying
    post_money = pre_money + raise_amt
    rw = runway(cash, burn, hires)

    C = {}

    def claim(cid, piece, text, value, display, confidence, sources, mark=None, severity="info", agree=None, disagree=None):
        C[cid] = {"id": cid, "piece": piece, "text": text, "value": value, "display": display, "confidence": confidence,
                  "sources": sources, "mark": mark, "severity": severity, "agree": agree or [], "disagree": disagree or []}

    claim("tr-1", "traction_and_revenue", f"The deck says {deck_paying} paying teams. The workspace file shows {paying} paying and {free} free design partners.",
          paying, str(paying), "computed", [src(deck, "slide 4", f"{deck_paying} paying teams"), src(ws, "2026-09, plan column", f"Free: {free}")],
          "contradicted", "flag")
    claim("tr-2", "traction_and_revenue", f"September MRR from the paying teams is {money(mrr)}, so ARR is {money(arr)}.", arr, money(arr), "computed",
          [src(ws, "2026-09 rows", f"{mrr}")])
    claim("lc-1", "legal_and_cap_table", f"The cap table's seed total is {money(f['seed'])}, the amount in the company's post.", f["seed"], money(f["seed"]),
          "quoted", [src(cap, "Seed!F14", f"{f['seed']}")], "corroborated", agree=[public("seed", "Sazabi blog")])
    claim("ow-1", "outside_world", "The model's prices match the public pricing page.", f["growth"], f"${f['growth']:,}", "quoted",
          [src(model, "Pricing!B3:B5", f"{f['hobby']}, {f['startup']}, {f['growth']}")], "corroborated", agree=[public("prices", "sazabi.com/pricing")])
    claim("te-1", "team", f"Staff today: {f['team']} in the model, the same as the YC page.", f["team"], str(f["team"]), "quoted",
          [src(model, "Assumptions!C4", f"STAFF_NOW = {f['team']}")], "corroborated", agree=[public("team", "YC company page")])

    reds = [{"kind": "red", "piece": "traction_and_revenue", "claim_id": "tr-1", "title": "The deck counts free design partners as paying teams.",
             "stated": {"key": "Stated, deck slide 4", "value": str(deck_paying), "out": True, "source": src(deck, "slide 4", f"{deck_paying} paying teams")},
             "found": {"key": "Found, workspace file", "value": str(paying), "source": src(ws, "2026-09, plan column", f"Free: {free}")},
             "others": [], "strip": strip([deck_paying, paying], paying, [{"v": deck_paying, "label": f"Deck {deck_paying}", "pos": "above"}], "count", 5),
             "ask": f"The deck says {deck_paying} paying teams and the workspace file shows {paying}. Which number do you use, and when do the others convert?",
             "relative_gap": relative_gap(deck_paying, paying)}]
    greens = [{"kind": "green", "piece": "legal_and_cap_table", "claim_id": "lc-1", "title": "The cap table's seed matches the company's public post.",
               "stated": {"key": "Room, cap table", "value": money(f["seed"]), "source": src(cap, "Seed!F14", f"{f['seed']}")},
               "found": {"key": "Outside, company post", "value": money(f["seed"]), "source": public("seed", "Sazabi blog")},
               "others": [], "strip": strip([f["seed"]], f["seed"], [{"v": f["seed"], "label": f"Both {millions(f['seed'])}", "pos": "above"}], "usd", 1_000_000),
               "ask": None, "relative_gap": 0}]
    thin = "not_enough_in_the_room"
    pieces = [
        {"name": "traction_and_revenue", "label": "Traction and revenue", "verdict": "looking_weak", "reason": C["tr-1"]["text"], "agree": 0, "disagree": 1, "claim_ids": ["tr-1", "tr-2"]},
        {"name": "retention", "label": "Retention", "verdict": thin, "reason": "Not in the room: a cohort export.", "agree": 0, "disagree": 0, "claim_ids": []},
        {"name": "burn_and_runway", "label": "Burn and runway", "verdict": thin, "reason": "Only the model states cash and burn. No bank statements are in the room.", "agree": 0, "disagree": 0, "claim_ids": []},
        {"name": "unit_economics", "label": "Unit economics", "verdict": thin, "reason": "Not in the room: storage and AI cost per customer.", "agree": 0, "disagree": 0, "claim_ids": []},
        {"name": "customers", "label": "Customers", "verdict": thin, "reason": "Not in the room: customer contracts.", "agree": 0, "disagree": 0, "claim_ids": []},
        {"name": "market", "label": "Market", "verdict": thin, "reason": "Only the deck sizes the market.", "agree": 0, "disagree": 0, "claim_ids": []},
        {"name": "team", "label": "Team", "verdict": "looking_strong", "reason": C["te-1"]["text"], "agree": 2, "disagree": 0, "claim_ids": ["te-1"]},
        {"name": "the_pitch_itself", "label": "The pitch itself", "verdict": thin, "reason": "Only the deck states the raise.", "agree": 0, "disagree": 0, "claim_ids": []},
        {"name": "legal_and_cap_table", "label": "Legal and cap table", "verdict": "looking_strong", "reason": C["lc-1"]["text"], "agree": 2, "disagree": 0, "claim_ids": ["lc-1"]},
        {"name": "outside_world", "label": "Outside world", "verdict": "looking_strong", "reason": C["ow-1"]["text"], "agree": 2, "disagree": 0, "claim_ids": ["ow-1"]},
    ]
    drill = [
        {"piece": "traction_and_revenue", "kind": "weak", "claim_ids": ["tr-1", "tr-2"], "panel": None, "gaps": ["Not in the room: monthly revenue by customer."]},
        {"piece": "legal_and_cap_table", "kind": "strong", "claim_ids": ["lc-1"], "panel": None, "gaps": []},
    ]
    holds = {"C02": [ws], "C19": [model], "C72": [cap], "C60": [deck], "C22": [hiring]}
    prechecks = [
        {"pre": "prices", "status": "confirms", "room": "The model's prices match.", "source": src(model, "Pricing!B3:B5", f"{f['hobby']}, {f['startup']}, {f['growth']}")},
        {"pre": "seed", "status": "confirms", "room": f"The cap table's seed total is {money(f['seed'])}.", "source": src(cap, "Seed!F14", f"{f['seed']}")},
        {"pre": "design_partners", "status": "confirms", "room": f"The workspace file lists {f['design_partners']} design partners. {paying} pay.",
         "source": src(ws, "2026-09, plan column", f"Free: {free}")},
        {"pre": "team", "status": "confirms", "room": f"The model's staff today is {f['team']}.", "source": src(model, "Assumptions!C4", f"STAFF_NOW = {f['team']}")},
    ]
    whatif = {
        "lines": [{"name": "Hobby plan", "units": hobby, "price": f["hobby"]}, {"name": "Startup plan", "units": startup, "price": f["startup"], "tweak": True},
                  {"name": "Growth plan", "units": growth, "price": f["growth"]}],
        "pilot": None, "company_arr": None, "rebuilt_arr": arr, "churn": churn, "cash": cash, "base_burn": burn, "company_runway": None,
        "rebuilt_runway": round(rw, 1), "extra_hires": hires, "extra_count": len(hires),
    }
    steer_examples = [
        {"piece": "traction_and_revenue", "sentence": "Ask which design partners convert to paid this quarter.", "kind": "more",
         "request": "Design partners expected to convert to paid this quarter"},
    ]
    return with_states({
        "synthetic_notice": NOTICE, "as_of": "2026-09-30", "files": sorted({x.split(", ")[0] for v in holds.values() for x in v}),
        "round": {"name": "Seed extension", "raise": money(raise_amt), "pre_money": money(pre_money), "post_money": money(post_money),
                  "ownership": pct(raise_amt / post_money, 2), "source": src(deck, "slide 12", f"{millions(raise_amt)} seed extension")},
        "top_flags": {"green": greens, "red": reds}, "pieces": pieces, "claims": C, "drill": drill, "holds": holds,
        "prechecks": prechecks, "whatif": whatif, "steer_examples": steer_examples,
        "memo_company": (f"Sazabi watches a team's production logs with AI, alerts on real problems and opens fixes. It raised a "
                         f"{millions(f['seed'])} seed, per its own post. In this synthetic room it asks for a {millions(raise_amt)} seed extension."),
    }, {deck, cap}, [])
