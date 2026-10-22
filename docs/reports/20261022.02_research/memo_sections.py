"""Read the saved investment memos and memo templates, find their section headings,
sort each heading into a canonical section, and count.

Inputs: the text files under raw/memos/ (saved by memo_fetch.py).
Outputs, next to this script:
  memos.csv                 one row per memo or template: title, company, fund, stage,
                            year, URL, saved file, and its section headings in order
  memo_section_labels.csv   one row per heading: the file, its position, the heading as
                            it appears, the canonical section it was assigned, and any
                            second section a combined heading also covers
  memo_section_counts.csv   one row per canonical section: how many memos and how many
                            templates have it, and its median position in the memos
  memo_stats.csv            one row per memo or template: body words, sections, outbound
                            links, and the evidence and risk measures defined below
  memo_summary.json         the numbers research_memos.md quotes

Run: python3 -I memo_sections.py
Every count in research_memos.md comes from these files.
"""
import csv
import json
import pathlib
import re
import statistics

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / "raw" / "memos"

BVP_END = r"^## Keep digging"

# kind: memo or template. parse: how the headings are read from the saved file.
#   atx       Markdown '#' headings at the given levels, between start and end markers
#   setext    Markdown headings underlined with '--' (and the title with '==')
#   explicit  a fixed list of heading lines; the script checks each one is in the file
#   bold_lead paragraphs that open with a bold run, between start and end markers
#   bold_list list items that open with a bold run, between start and end markers
DOCS = [
    # Bessemer Venture Partners, the memo archive at bvp.com/atlas?type=memo
    dict(file="bvp_yelp", kind="memo", title="Yelp", company="Yelp", fund="Bessemer Venture Partners", stage="first venture round after a $1M angel round (round not named)", year="2005", url="https://www.bvp.com/memos/yelp"),
    dict(file="bvp_lifelock", kind="memo", title="Life Lock, Inc.", company="LifeLock", fund="Bessemer Venture Partners", stage="Series A", year="2006", url="https://www.bvp.com/memos/lifelock"),
    dict(file="bvp_linkedin", kind="memo", title="Investment Recommendation: LinkedIn", company="LinkedIn", fund="Bessemer Venture Partners", stage="Series C", year="2006", url="https://www.bvp.com/memos/linkedin"),
    dict(file="bvp_wix", kind="memo", title="Wix Seed Investment Recommendation", company="Wix", fund="Bessemer Venture Partners", stage="seed (second seed round)", year="2007", url="https://www.bvp.com/memos/wix"),
    dict(file="bvp_dropcam", kind="memo", title="Dropcam", company="Dropcam", fund="Bessemer Venture Partners", stage="seed", year="2009", url="https://www.bvp.com/memos/dropcam"),
    dict(file="bvp_twilio", kind="memo", title="Twilio Seed Investment - $125,000", company="Twilio", fund="Bessemer Venture Partners", stage="seed (extension)", year="2009", url="https://www.bvp.com/memos/twilio"),
    dict(file="bvp_mindbody", kind="memo", title="Mindbody Investment Recommendation", company="Mindbody", fund="Bessemer Venture Partners", stage="$11M preferred round (round not named)", year="2010", url="https://www.bvp.com/memos/mindbody"),
    dict(file="bvp_shopify", kind="memo", title="Shopify", company="Shopify", fund="Bessemer Venture Partners", stage="Series A", year="2010", url="https://www.bvp.com/memos/shopify"),
    dict(file="bvp_medi-assist", kind="memo", title="Medi Assist Healthcare Services", company="Medi Assist", fund="Bessemer Venture Partners", stage="management buyout (growth)", year="2010", url="https://www.bvp.com/memos/medi-assist"),
    dict(file="bvp_fiverr", kind="memo", title="Fiverr Investment Recommendation", company="Fiverr", fund="Bessemer Venture Partners", stage="first venture round, alongside angels (round not named)", year="2011", url="https://www.bvp.com/memos/fiverr"),
    dict(file="bvp_pinterest", kind="memo", title="Pinterest IR", company="Pinterest", fund="Bessemer Venture Partners", stage="Series A", year="2011", url="https://www.bvp.com/memos/pinterest"),
    dict(file="bvp_sendgrid", kind="memo", title="SendGrid Series B IR", company="SendGrid", fund="Bessemer Venture Partners", stage="Series B", year="2011", url="https://www.bvp.com/memos/sendgrid"),
    dict(file="bvp_twitch", kind="memo", title="Twitch Series B IR", company="Twitch", fund="Bessemer Venture Partners", stage="Series B", year="2012", url="https://www.bvp.com/memos/twitch"),
    dict(file="bvp_auth0", kind="memo", title="Auth0 Seed IR", company="Auth0", fund="Bessemer Venture Partners", stage="seed", year="2014", url="https://www.bvp.com/memos/auth0"),
    dict(file="bvp_pagerduty", kind="memo", title="PagerDuty Series B IR", company="PagerDuty", fund="Bessemer Venture Partners", stage="Series B", year="2014", url="https://www.bvp.com/memos/pagerduty"),
    dict(file="bvp_rocket-lab", kind="memo", title="Rocket Lab Series B Flash", company="Rocket Lab", fund="Bessemer Venture Partners", stage="Series B", year="2014", url="https://www.bvp.com/memos/rocket-lab"),
    dict(file="bvp_servicetitan", kind="memo", title="ServiceTitan Series A Flash", company="ServiceTitan", fund="Bessemer Venture Partners", stage="Series A", year="2015", url="https://www.bvp.com/memos/servicetitan"),
    dict(file="bvp_velo3d", kind="memo", title="Velo3D Series A IR", company="Velo3D", fund="Bessemer Venture Partners", stage="Series A", year="2015", url="https://www.bvp.com/memos/velo3d"),
    dict(file="bvp_toast", kind="memo", title="Toast Series B IR", company="Toast", fund="Bessemer Venture Partners", stage="Series B (first institutional round)", year="2015", url="https://www.bvp.com/memos/toast"),
    # Root Ventures, github.com/rootvc/investment-memos
    dict(file="rootvc_esper", kind="memo", title="Investment Memo for Esper (fka Shoonya)", company="Esper", fund="Root Ventures", stage="seed", year="2018", url="https://github.com/rootvc/investment-memos/blob/main/esper.md"),
    dict(file="rootvc_meroxa", kind="memo", title="Meroxa Deal Memo", company="Meroxa", fund="Root Ventures", stage="seed", year="2020", url="https://github.com/rootvc/investment-memos/blob/main/meroxa.md"),
    dict(file="rootvc_daily", kind="memo", title="Investment Memo for Daily", company="Daily", fund="Root Ventures", stage="seed (the round before Series A)", year="not stated", url="https://github.com/rootvc/investment-memos/blob/main/daily.md"),
    dict(file="rootvc_okteto", kind="memo", title="Okteto Investment Memo", company="Okteto", fund="Root Ventures", stage="seed", year="not stated", url="https://github.com/rootvc/investment-memos/blob/main/okteto.md", parse="setext"),
    dict(file="rootvc_privacy_dynamics", kind="memo", title="Investment Memo for Privacy Dynamics", company="Privacy Dynamics", fund="Root Ventures", stage="seed (raising $3.5M; round not named)", year="not stated", url="https://github.com/rootvc/investment-memos/blob/main/privacy_dynamics.md"),
    dict(file="rootvc_superconductive", kind="memo", title="Superconductive", company="Superconductive (Great Expectations)", fund="Root Ventures", stage="seed", year="not stated", url="https://github.com/rootvc/investment-memos/blob/main/superconductive.md"),
    dict(file="rootvc_zed", kind="memo", title="Zed", company="Zed", fund="Root Ventures", stage="seed (post-money cap)", year="not stated", url="https://github.com/rootvc/investment-memos/blob/main/zed.md"),
    # A partner's own angel memo, linked from the Root Ventures repo
    dict(file="ledwards_esper_angel", kind="memo", title="Esper angel investment memo", company="Esper", fund="Lee Edwards (angel, later Root Ventures partner)", stage="seed (angel check)", year="2018", url="https://github.com/ledwards/investment-memos/blob/main/esper.md"),
    # Blackbird Ventures, the 2014 memo to its LPs, published on its blog in 2018
    dict(file="blackbird_zoox", kind="memo", title="New Investment: Zoox", company="Zoox", fund="Blackbird Ventures", stage="seed (first round, $1.3M)", year="2014", url="https://blackbird.vc/blog/zoox-memory-lane",
         parse="atx", levels=(4,), start=r"^### New Investment: Zoox", end=r"^### More Stories"),
    # Templates
    dict(file="tpl_hustlefund", kind="template", title="Investment memo template: a copyable guide for angel investors", company="", fund="Hustle Fund (Angel Squad)", stage="pre-seed and seed, angels", year="2026", url="https://www.hustlefund.vc/post/investment-memo-template",
         parse="atx", levels=(3,), start=r"^## Copy this investment memo template", end=r"^## How to write a memo"),
    dict(file="tpl_pointnine_gdoc", kind="template", title="Point Nine open-source deal memo template", company="", fund="Point Nine Capital", stage="seed", year="not stated", url="https://docs.google.com/document/d/1zLMTk_s_As7mjZwOAJwHc6-6H0JhEety8ZLEG2NtTN0/edit",
         parse="explicit", headings=["1. Product", "2. Market", "3. Competition", "4. Traction", "5. Acquisition", "6. Business model", "7. Team", "8. Funding/ Deal", "9. Reference calls"]),
    dict(file="tpl_dempsey_gdoc", kind="template", title="Michael Dempsey Investment Memo Template", company="", fund="Compound (Michael Dempsey)", stage="seed", year="2019", url="https://docs.google.com/document/d/1tlqi-nPgScyG78uwVX6BOwhukztvLaZbFgRh2bF-xog/edit",
         parse="explicit", headings=["Business Summary", "Identified Risk", "Deal Structure", "Offer Context", "Problem", "Solution + Road Map", "Market", "Team", "Business", "Financials"]),
    dict(file="tpl_nextview", kind="template", title="The Investment Memo", company="", fund="NextView Ventures (David Beisel)", stage="seed", year="not stated (page dated 2024)", url="https://nextview.vc/blog/the-investment-memo/",
         parse="bold_lead", start=r"^# The Investment Memo", end=r"^### Related", skip=("David Beisel", "Topics")),
    dict(file="tpl_aca_basics_dd", kind="template", title="The Basics of Due Diligence (topics a group's report covers)", company="", fund="Angel Capital Association (board member's workshop deck)", stage="angel groups", year="2016", url="https://angelcapitalassociation.org/data/Secure/Angel%20Insights%20Exchange%20Library/2016-Nashville/BasicsofDueDiligence-Presentation.pdf?rev=F688",
         parse="explicit", headings=["CEO & Other Management", "Product", "Business Model", "Markets", "Sales & Marketing", "Competition", "Competitive Advantage", "Legal & Regulatory Environment", "Intellectual Property & Technology", "Valuation & Terms", "Financials", "Exit Strategy", "Potential for investors", "Other Investors", "Risks"]),
    dict(file="tpl_visible", kind="template", title="Investment Memo: Template, Examples, and How to Write One", company="", fund="Visible.vc (written for founders)", stage="seed and Series A", year="2026", url="https://visible.vc/blog/investment-memo/",
         parse="bold_list", start=r"^## What Should Be Included in an Investment Memo", end=r"^## The One-Page Investment Memo"),
]

# Saved while searching, read, and left out of the counts. The reason is recorded here.
NOT_ANALYSED = {
    "rootvc_README": "the Root Ventures repo's index page, not a memo",
    "nfx_doordash": "an audio episode page; the DoorDash memo text is not on it",
    "twentyvc_snapchat": "podcast show notes about the Snapchat memo, not the memo",
    "vccorner_youtube": "a paywalled commentary; the YouTube memo text is behind the paywall",
    "tpl_confluencevc": "a newsletter landing page; the template itself is not on it",
    "tpl_latextemplates": "a download page; the template's sections are not in the page text",
    "tpl_dempsey_post": "the author's notes on his own template (tpl_dempsey_gdoc); read for how risks are written",
}

# Canonical sections, in the order the template doc uses for its plain names.
SECTION_NAMES = {
    "summary_and_ask": "Summary and the ask",
    "company_and_problem": "Company and problem",
    "product": "Product",
    "market": "Market",
    "competition": "Competition",
    "business_model_and_sales": "Business model and sales",
    "traction_and_metrics": "Traction and metrics",
    "unit_economics": "Unit economics",
    "financials": "Financials",
    "team": "Team",
    "diligence_and_references": "Diligence and reference calls",
    "deal_terms": "Deal terms",
    "risks_and_open_questions": "Risks and open questions",
    "outcomes_and_returns": "Outcomes and returns",
    "why_invest": "Why invest (the merits)",
    "conclusion_and_recommendation": "Conclusion and recommendation",
    "sources_and_change_log": "Sources and change log",
    "appendix": "Appendix",
    "other": "Other",
}

# Ordered rules: the first pattern that matches the normalised heading wins.
# A third element names the second section a combined heading also covers.
RULES = [
    (r"^appendix", "appendix", None),
    (r"sources and change log|other reading", "sources_and_change_log", None),
    (r"risk|concern|considerations|ways this can fail", "risks_and_open_questions", None),
    (r"scenario|outcome|exit|potential for investors", "outcomes_and_returns", None),
    (r"diligence|reference call|customer feedback", "diligence_and_references", None),
    (r"unit economics", "unit_economics", None),
    (r"financial metrics & financing", "financials", "deal_terms"),
    (r"financials/traction|traction/financials", "financials", "traction_and_metrics"),
    (r"timeline/financials/fundraising", "financials", "deal_terms"),
    (r"traction, team, and finances", "traction_and_metrics", "team"),
    (r"financial", "financials", None),
    (r"deal|financing|funding|fundraise|the raise|valuation & terms|other investors|offer context|cap table|portfolio fit", "deal_terms", None),
    (r"market and competition|market & competitors|competition / related", "market", "competition"),
    (r"market and paying customers", "market", "traction_and_metrics"),
    (r"market, model, and go-to-market", "market", "business_model_and_sales"),
    (r"market and background", "market", "company_and_problem"),
    (r"competit", "competition", None),
    (r"business model|go-to-market|sales|marketing|monetization|partnerships|acquisition|revenue model|^business$|where do they go", "business_model_and_sales", None),
    (r"eco-system", "product", None),
    (r"market|industry|trends", "market", None),
    (r"traction|metrics|customers & users|^revenue$", "traction_and_metrics", None),
    (r"customers & pricing|customer acquisition", "business_model_and_sales", "traction_and_metrics"),
    (r"team|management|founder", "team", None),
    (r"company, problem, and product", "company_and_problem", "product"),
    (r"company, problem|^company$|problem|background|company history|value proposition|identity theft|self-expression|history and business overview", "company_and_problem", None),
    (r"product|tech|solution|service|offering|community|approach|works|benefits|intellectual property|coming soon|website builder", "product", None),
    (r"investment positives|glimmer|why are we so excited", "why_invest", None),
    (r"final recommendation|conclusion|recommendation, portfolio", "conclusion_and_recommendation", None),
    (r"recommendation|summary|overview|introduction|decision snapshot|purpose", "summary_and_ask", None),
]


def norm(h):
    h = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", h)
    h = re.sub(r"^\d+\.\s*", "", h.strip())
    h = h.replace("**", "").strip().rstrip(":.").strip()
    return h


def classify(heading, position, count):
    n = norm(heading).lower()
    for pat, sec, also in RULES:
        if re.search(pat, n):
            if sec == "summary_and_ask" and count > 2 and position >= count - 1:
                # A "Summary" placed last closes the memo; it is the conclusion.
                return "conclusion_and_recommendation", None
            return sec, also
    return "other", None


def body_between(text, start, end):
    lines = text.splitlines()
    i0 = 0
    if start:
        i0 = next(i for i, l in enumerate(lines) if re.search(start, l)) + 1
    i1 = len(lines)
    if end:
        i1 = next((i for i, l in enumerate(lines[i0:], i0) if re.search(end, l)), len(lines))
    return lines[i0:i1]


def read_doc(d):
    text = (RAW / f"{d['file']}.txt").read_text(encoding="utf-8")
    parse = d.get("parse", "atx")
    if d["file"].startswith("bvp_"):
        d.setdefault("start", r"^# ")
        d.setdefault("end", BVP_END)
        d.setdefault("levels", (2,))
    elif d["file"] == "rootvc_okteto":
        d.setdefault("start", r"^==")
        d.setdefault("end", None)
    elif d["file"].startswith("rootvc_"):
        d.setdefault("start", r"^# ")
        d.setdefault("end", None)
        d.setdefault("levels", (2,))
    elif d["file"].startswith("ledwards_"):
        d.setdefault("start", r"^SOURCE:")
        d.setdefault("end", None)
        d.setdefault("levels", (2,))
    lines = body_between(text, d.get("start"), d.get("end"))
    headings = []  # (heading, level)
    if parse == "atx":
        for l in lines:
            m = re.match(r"^(#{1,6})\s+(.*\S)", l)
            if m and len(m.group(1)) in d["levels"]:
                headings.append((m.group(2), len(m.group(1))))
    elif parse == "setext":
        for a, b in zip(lines, lines[1:]):
            if re.fullmatch(r"-{2,}\s*", b) and a.strip():
                headings.append((a.strip(), 2))
    elif parse == "explicit":
        for h in d["headings"]:
            if h not in text:
                raise SystemExit(f"{d['file']}: heading not found in saved text: {h!r}")
            headings.append((h, 1))
    elif parse == "bold_lead":
        for l in lines:
            m = re.match(r"^\*\*([^*]+)\*\*", l)
            if m and norm(m.group(1)) not in d.get("skip", ()):
                headings.append((m.group(1).strip(), 1))
    elif parse == "bold_list":
        for l in lines:
            m = re.match(r"^- \*\*([^*]+)\*\*", l)
            if m:
                headings.append((m.group(1).strip(), 1))
    body = "\n".join(lines)
    return text, body, headings


def opening_text(d, body):
    """The words before the first section heading (BVP and Root memos open untitled)."""
    out = []
    for l in body.splitlines():
        if re.match(r"^#{1,6} ", l) or re.fullmatch(r"-{2,}\s*", l):
            break
        out.append(l)
    return " ".join(out)


RECOMMEND = re.compile(r"\bwe recommend|\bi recommend|recommending|seek approval|we are investing|we're investing|we should offer|we expect to sign|signed a term sheet|we have signed", re.I)
REFERENCE = re.compile(r"reference call|reference check|references|customer call|spoke (with|to)|talked (with|to)|called (several|a number|\d)|interviewed|diligence call", re.I)
MITIGATE = re.compile(r"mitigat", re.I)
QUESTION = re.compile(r"open question|questions to pursue|need to (understand|confirm|validate|learn)|unclear|unknown|\?", re.I)
NUMBER = re.compile(r"\$\s?\d|\d+(\.\d+)?\s?%|\b\d{2,}[,\d]*\b")


def section_block(body, pattern=r"risk|concern|considerations"):
    """The text of the first section whose heading matches, up to the next heading of the same depth."""
    lines = body.splitlines()
    for i, l in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.*)", l)
        if m and re.search(pattern, m.group(2), re.I):
            depth = len(m.group(1))
            out = []
            for l2 in lines[i + 1:]:
                m2 = re.match(r"^(#{1,6})\s", l2)
                if m2 and len(m2.group(1)) <= depth:
                    break
                out.append(l2)
            return "\n".join(out)
    return ""


def stage_group(stage):
    """Group a memo's stage for the count: seed, Series A, Series B, or other or not named."""
    if stage.startswith("seed"):
        return "seed"
    if stage.startswith("Series A"):
        return "Series A"
    if stage.startswith("Series B"):
        return "Series B"
    return "other or not named"


def main():
    memo_rows, label_rows, stat_rows = [], [], []
    for d in DOCS:
        text, body, headings = read_doc(d)
        count = len(headings)
        labelled = []
        for pos, (h, lvl) in enumerate(headings):
            sec, also = classify(h, pos, count)
            labelled.append((pos, h, lvl, sec, also))
            label_rows.append({
                "file": f"raw/memos/{d['file']}.txt", "kind": d["kind"], "fund": d["fund"],
                "position": pos + 1, "of": count, "heading": norm(h), "level": lvl,
                "section": sec, "also_section": also or "",
            })
        memo_rows.append({
            "kind": d["kind"], "title": d["title"], "company": d["company"], "fund": d["fund"],
            "stage": d["stage"], "year": d["year"], "url": d["url"],
            "saved_file": f"raw/memos/{d['file']}.txt",
            "section_headings": " | ".join(norm(h) for h, _ in headings),
        })
        opening = opening_text(d, body)
        risks = section_block(body)
        outcomes = section_block(body, r"scenario|outcome")
        outcome_text = re.sub(r"\[image\]", "", outcomes).strip()
        words = len(re.findall(r"\b\w[\w'’.-]*\b", re.sub(r"\]\([^)]+\)", "]", body)))
        stat_rows.append({
            "file": d["file"], "kind": d["kind"], "fund": d["fund"], "stage": d["stage"],
            "body_words": words,
            "sections": count,
            "opening_words": len(opening.split()),
            "has_to_from_date_re": int(bool(re.search(r"\bTo BVP Group\b", body)) and bool(re.search(r"\bRe\b", body))),
            "recommendation_in_first_150_words": int(bool(RECOMMEND.search(" ".join(body.split()[:150])))),
            "recommendation_anywhere": int(bool(RECOMMEND.search(body))),
            "outbound_links": len(re.findall(r"\]\((https?://[^)]+)\)", body)) + len(re.findall(r"(?m)^https?://\S+$", body)),
            "reference_mentions": len(REFERENCE.findall(body)),
            "numbers_in_body": len(NUMBER.findall(body)),
            "has_risk_section": int(any(s == "risks_and_open_questions" for _, _, _, s, _ in labelled)),
            "risk_section_words": len(risks.split()),
            "risk_section_labelled_items": len(re.findall(r"(?m)^\s*(?:[-*•]\s+)?(?:\*\*)?[A-Z][\w ,/&'’()-]{2,60}?(?:\*\*)?\s*(?::|–|—| - )", risks)),
            "risk_section_bullets": len(re.findall(r"(?m)^\s*([-*•]|\d+\.)\s+\S", risks)),
            "risk_section_mentions_mitigation": int(bool(MITIGATE.search(risks))),
            "risk_section_has_open_questions": int(bool(QUESTION.search(risks))),
            "opens_with_summary": int(len(opening.split()) >= 100 or (bool(labelled) and labelled[0][3] in ("summary_and_ask", "why_invest"))),
            "has_numbers_section": int(any(s in ("traction_and_metrics", "financials", "unit_economics") or a in ("traction_and_metrics", "financials") for _, _, _, s, a in labelled)),
            "images_in_body": len(re.findall(r"(?m)^\[image\]$", body)),
            "outcomes_section_image_only": int(bool(outcomes) and "[image]" in outcomes and not outcome_text),
            "has_outcomes_section": int(any(s == "outcomes_and_returns" for _, _, _, s, _ in labelled)),
            "has_diligence_section": int(any(s == "diligence_and_references" for _, _, _, s, _ in labelled)),
        })

    # Section counts: a memo or template "has" a section if any heading is assigned it,
    # as the main or the second section.
    def has(kind):
        out = {}
        for d in DOCS:
            if d["kind"] != kind:
                continue
            secs = {r["section"] for r in label_rows if r["file"].endswith(d["file"] + ".txt")}
            secs |= {r["also_section"] for r in label_rows if r["file"].endswith(d["file"] + ".txt") and r["also_section"]}
            out[d["file"]] = secs
        return out

    memo_has, tpl_has = has("memo"), has("template")
    # Position: for each memo, the first heading assigned the section, as a share of the way
    # through the memo (0 = first heading, 1 = last heading).
    positions = {s: [] for s in SECTION_NAMES}
    for d in DOCS:
        if d["kind"] != "memo":
            continue
        rows = [r for r in label_rows if r["file"].endswith(d["file"] + ".txt")]
        seen = set()
        for r in rows:
            for s in (r["section"], r["also_section"]):
                if s and s not in seen and r["of"] > 1:
                    seen.add(s)
                    positions[s].append((r["position"] - 1) / (r["of"] - 1))
    count_rows = []
    for s, name in SECTION_NAMES.items():
        m = sum(1 for v in memo_has.values() if s in v)
        t = sum(1 for v in tpl_has.values() if s in v)
        pos = positions[s]
        count_rows.append({
            "section": s, "plain_name": name,
            "memos_with": m, "memos_total": len(memo_has),
            "templates_with": t, "templates_total": len(tpl_has),
            "median_position_in_memos": round(statistics.median(pos), 2) if pos else "",
        })

    def write(name, rows):
        with open(HERE / name, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    write("memos.csv", memo_rows)
    write("memo_section_labels.csv", label_rows)
    write("memo_section_counts.csv", count_rows)
    write("memo_stats.csv", stat_rows)

    memos = [r for r in stat_rows if r["kind"] == "memo"]
    bvp = [r for r in memos if r["file"].startswith("bvp_")]
    root = [r for r in memos if r["file"].startswith("rootvc_")]
    risk_memos = [r for r in memos if r["has_risk_section"]]

    def med(rows, k):
        return statistics.median(r[k] for r in rows) if rows else None

    summary = {
        "memos": len(memos),
        "templates": len(stat_rows) - len(memos),
        "headings_labelled": len(label_rows),
        "headings_other": sum(1 for r in label_rows if r["section"] == "other"),
        "memos_by_fund": {f: sum(1 for d in DOCS if d["kind"] == "memo" and d["fund"] == f) for f in sorted({d["fund"] for d in DOCS if d["kind"] == "memo"})},
        "body_words_median_all_memos": med(memos, "body_words"),
        "body_words_min": min(r["body_words"] for r in memos),
        "body_words_max": max(r["body_words"] for r in memos),
        "body_words_median_bvp": med(bvp, "body_words"),
        "body_words_median_rootvc": med(root, "body_words"),
        "sections_median_memos": med(memos, "sections"),
        "sections_min": min(r["sections"] for r in memos),
        "sections_max": max(r["sections"] for r in memos),
        "bvp_with_to_from_date_re": sum(r["has_to_from_date_re"] for r in bvp),
        "bvp_total": len(bvp),
        "memos_recommendation_in_first_150_words": sum(r["recommendation_in_first_150_words"] for r in memos),
        "memos_recommendation_anywhere": sum(r["recommendation_anywhere"] for r in memos),
        "memos_with_risk_section": len(risk_memos),
        "risk_section_words_median": med(risk_memos, "risk_section_words"),
        "risk_sections_with_bullets": sum(1 for r in risk_memos if r["risk_section_bullets"] > 0),
        "risk_sections_mentioning_mitigation": sum(r["risk_section_mentions_mitigation"] for r in risk_memos),
        "risk_sections_with_open_questions": sum(r["risk_section_has_open_questions"] for r in risk_memos),
        "memos_opening_with_summary": sum(r["opens_with_summary"] for r in memos),
        "memos_with_a_numbers_section": sum(r["has_numbers_section"] for r in memos),
        "memos_with_outcomes_section": sum(r["has_outcomes_section"] for r in memos),
        "risk_sections_as_short_list": sum(1 for r in risk_memos if r["risk_section_labelled_items"] > 0 or r["risk_section_bullets"] > 0),
        "memos_by_stage_group": {g: sum(1 for d in DOCS if d["kind"] == "memo" and stage_group(d["stage"]) == g) for g in ("seed", "Series A", "Series B", "other or not named")},
        "memos_with_year_stated": sum(1 for d in DOCS if d["kind"] == "memo" and d["year"].isdigit()),
        "memo_year_earliest": min(int(d["year"]) for d in DOCS if d["kind"] == "memo" and d["year"].isdigit()),
        "memo_year_latest": max(int(d["year"]) for d in DOCS if d["kind"] == "memo" and d["year"].isdigit()),
        "funds_with_memos": len({d["fund"] for d in DOCS if d["kind"] == "memo"}),
        "outcomes_sections_image_only": sum(r["outcomes_section_image_only"] for r in memos),
        "risk_sections_with_labelled_items": sum(1 for r in risk_memos if r["risk_section_labelled_items"] > 0),
        "memos_with_images_in_body": sum(1 for r in memos if r["images_in_body"] > 0),
        "memos_with_diligence_section": sum(r["has_diligence_section"] for r in memos),
        "memos_with_any_outbound_link": sum(1 for r in memos if r["outbound_links"] > 0),
        "outbound_links_median_bvp": med(bvp, "outbound_links"),
        "outbound_links_median_rootvc": med(root, "outbound_links"),
        "memos_with_reference_mentions": sum(1 for r in memos if r["reference_mentions"] > 0),
        "numbers_in_body_median_bvp": med(bvp, "numbers_in_body"),
        "numbers_in_body_median_rootvc": med(root, "numbers_in_body"),
        "not_analysed": NOT_ANALYSED,
    }
    (HERE / "memo_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps({k: v for k, v in summary.items() if k != "not_analysed"}, indent=2))
    print()
    for r in sorted(count_rows, key=lambda r: -r["memos_with"]):
        print(f"{r['plain_name']:32} memos {r['memos_with']:>2}/{r['memos_total']}  templates {r['templates_with']}/{r['templates_total']}  median position {r['median_position_in_memos']}")


if __name__ == "__main__":
    main()
