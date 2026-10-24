"""Build data.json (and data.js) for the first-steps prototype from the saved research files.

Run: python3 build_data.py   (from anywhere; paths are worked out from this file)

What it writes, beside this file:
- data.json and data.js: the YC Spring 2026 list (every CSV row), the research for Ploy and Sazabi,
  and the checklist items with their guidance. data.js holds the same object as window.DATA so
  index.html also works opened straight from disk.
- sources/<name>.txt: a readable copy of every saved file a claim cites, so a source chip can open
  it with no network.

Rules this script holds to:
- Every fact on screen carries its source: the saved file's path and, where known, the original URL.
- Numbers are parsed from the saved files here, never typed in.
- Every quote is found again in the readable copy, or the build stops.
- Items marked "placeholder": true are prototype filler for what Benjamin's research builds. They
  carry no source and the page labels them as placeholders.
- LinkedIn is never a source: LinkedIn fields are dropped from the readable copies.
"""

from __future__ import annotations

import csv
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
RESEARCH = ROOT / "docs" / "reports" / "20261022.02_research"
RAW = RESEARCH / "raw" / "demo_companies"
CSV_PATH = RAW / "yc_spring_2026_companies.csv"
CHECKLIST = ROOT / "docs" / "ongoing" / "checklist.csv"
OUT_SOURCES = HERE / "sources"

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from founder_requests import guidance as gd  # noqa: E402

try:  # the founder wording the built app already uses; the prototype falls back without it
    from founder_requests.draft import CLOSING_AT_SEED, FOUNDER_TEXT  # noqa: E402
except Exception:  # noqa: BLE001
    FOUNDER_TEXT, CLOSING_AT_SEED = {}, {"C74", "C76", "C77"}

RESEARCHED_SIX = ["ploy", "tasklet-2", "sazabi", "testerarmy", "minicor", "expanse"]


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


# Readable copies of saved files -----------------------------------------------------------


def html_text(raw: str) -> str:
    """The same reduction demo_text.py uses."""
    raw = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</p>|</h[1-6]>|</li>|</div>|</blockquote>", "\n", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    raw = re.sub(r"[ \t]+", " ", raw)
    return re.sub(r"\n\s*\n+", "\n", raw).strip()


def no_linkedin(x):
    if isinstance(x, dict):
        return {k: no_linkedin(v) for k, v in x.items() if "linkedin" not in k.lower()
                and not (isinstance(v, str) and "linkedin.com" in v)}
    if isinstance(x, list):
        return [no_linkedin(v) for v in x]
    return x


def flatten(x, prefix="") -> list[str]:
    out = []
    if isinstance(x, dict):
        for k, v in x.items():
            out += flatten(v, f"{prefix}.{k}" if prefix else k)
    elif isinstance(x, list):
        if not x:
            out.append(f"{prefix}: (none)")
        for i, v in enumerate(x):
            out += flatten(v, f"{prefix}[{i}]")
    else:
        out.append(f"{prefix}: {x}")
    return out


def readable(path: Path) -> str:
    raw = path.read_text(errors="replace")
    name = path.name
    if path.suffix == ".html":
        return html_text(raw)
    if path.suffix in (".xml", ".csv", ".md", ".txt"):
        return raw
    data = json.loads(raw)
    if name.startswith("appstore_"):
        lines = [f"resultCount: {data['resultCount']}"]
        lines += [f"app: {r.get('trackName')} | seller: {r.get('sellerName')}" for r in data["results"]]
        return "\n".join(lines)
    if path.parent.name == "hn":
        lines = [f"domain_query: {data['domain_query']}"]
        for k in ("domain_hits", "launch_hits"):
            for h in data[k]:
                lines.append(f"{k} | id {h['objectID']} | {h.get('created_at', '')[:10]} | points {h.get('points')} "
                             f"| comments {h.get('num_comments')} | {h.get('title')} | {h.get('url')}")
        return "\n".join(lines)
    return "\n".join(flatten(no_linkedin(data)))


SOURCES: dict[str, dict] = {}


def source(path: Path, url: str | None, title: str) -> str:
    sid = path.stem if path.parent.name != "hn" else f"hn_{path.stem}"
    if sid not in SOURCES:
        text = readable(path)
        OUT_SOURCES.mkdir(exist_ok=True)
        (OUT_SOURCES / f"{sid}.txt").write_text(text)
        SOURCES[sid] = {"id": sid, "path": rel(path), "url": url, "title": title, "copy": f"sources/{sid}.txt",
                        "kind": "readable copy" if path.suffix in (".html", ".json") else "saved file", "_text": text}
    return sid


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def claim(text: str, sid: str, quote: str, **extra) -> dict:
    """A claim whose quote must be found again in the cited source's readable copy."""
    body = norm(SOURCES[sid]["_text"])
    q = norm(quote)
    at = body.find(q)
    if at < 0:
        raise SystemExit(f"Quote not found in {SOURCES[sid]['path']}: {quote!r}")
    start, end = max(0, at - 300), min(len(body), at + len(q) + 300)
    return {"text": text, "source": sid, "quote": q,
            "excerpt": {"before": body[start:at], "match": q, "after": body[at + len(q):end]}, **extra}


def placeholder(text: str) -> dict:
    return {"text": text, "placeholder": True}


def gap(text: str, why: str) -> dict:
    return {"text": text, "why": why}


def find(pattern: str, text: str, flags=0) -> re.Match:
    m = re.search(pattern, text, flags)
    if not m:
        raise SystemExit(f"Pattern not found: {pattern}")
    return m


# The list --------------------------------------------------------------------------------


def host_of(url: str) -> str:
    h = urlparse(url if "://" in url else "https://" + url).hostname or ""
    return h.lower().removeprefix("www.")


def load_companies() -> list[dict]:
    with open(CSV_PATH, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    out = []
    for r in rows:
        out.append({
            "name": r["name"], "slug": r["slug"], "batch": r["batch"], "website": r["website"],
            "host": host_of(r["website"]), "one_liner": r["one_liner"].strip(), "industry": r["industry"],
            "subindustry": r["subindustry"], "team_size": int(r["team_size"] or 0),
            "regions": r["regions"].split("|") if r["regions"] else [],
            "researched": r["slug"] in RESEARCHED_SIX,
        })
    return out


def yc_page(slug: str) -> dict | None:
    p = RAW / f"yc_page_{slug}.json"
    return json.loads(p.read_text()) if p.exists() else None


def founders_from_yc(slug: str) -> list[dict]:
    page = yc_page(slug)
    if not page:
        return []
    sid = source(RAW / f"yc_page_{slug}.json", f"https://www.ycombinator.com/companies/{slug}", f"YC company page: {page['company']['name']}")
    return [{"name": f["full_name"], "title": f["title"], "source": sid} for f in page["company"]["founders"]]


# Ploy ------------------------------------------------------------------------------------


def ploy() -> dict:
    page = yc_page("ploy")
    co = page["company"]
    launch = page["launches"][0]
    s_yc = source(RAW / "yc_page_ploy.json", "https://www.ycombinator.com/companies/ploy", "YC company page: Ploy")
    s_launch = s_yc  # the Launch YC post is inside the saved YC page data
    s_pricing = source(RAW / "site_ploy_pricing.html", "https://ploy.ai/pricing", "Ploy pricing page")
    s_site = source(RAW / "site_ploy.html", "https://ploy.ai", "Ploy home page")
    s_vca = source(RAW / "news_ploy_vcaonline.html",
                   "https://www.vcaonline.com/news/2026061715/ploy-raises-27m-to-turn-your-company-s-website-into-your-hardest-working-employee/",
                   "VCA Online: Ploy raises $27M (2026-06-17)")
    s_pulse = source(RAW / "news_ploy_pulse2.html",
                     "https://pulse2.com/ploy-raises-27-million-seed-round-to-launch-ai-growth-platform/",
                     "Pulse 2.0: Ploy raises $27 million seed round (2026-06-22)")
    s_hn = source(RAW / "hn" / "ploy.json", "https://hn.algolia.com/api/v1/search?query=ploy.ai", "Hacker News search: stories linking ploy.ai")
    s_disp = source(RESEARCH / "demo_dispute_scan.csv", None, "Dispute-word scan of Hacker News, from demo_dispute_scan.py")
    s_app = source(RAW / "appstore_ploy.json", "https://itunes.apple.com/search?term=ploy&entity=software", "Apple App Store search: ploy")
    s_formd = source(RAW / "edgar_formd_ploy_primary_doc.xml",
                     "https://www.sec.gov/Archives/edgar/data/2136625/000213662526000001/primary_doc.xml",
                     "SEC EDGAR: Ploy, Inc. Form D (filed 2026-06-24)")
    s_gh = source(RAW / "github_user_bryantchou.json", "https://github.com/BryantChou", "GitHub account: BryantChou")
    s_csv = source(CSV_PATH, "https://www.ycombinator.com/companies?batch=Spring%202026", "YC directory: Spring 2026 companies")

    # Prices, parsed from the pricing page.
    ptxt = norm(SOURCES[s_pricing]["_text"])
    pm = find(r"Monthly price \$(\d+)/mo \$(\d+)/mo \$(\d+)/mo Custom", ptxt)
    free, starter, pro = (int(x) for x in pm.groups())

    # Form D, parsed.
    fd = ET.parse(RAW / "edgar_formd_ploy_primary_doc.xml").getroot()
    g = lambda path: fd.findtext(path)  # noqa: E731
    sold = int(g(".//offeringSalesAmounts/totalAmountSold"))
    offered = int(g(".//offeringSalesAmounts/totalOfferingAmount"))
    investors = int(g(".//investors/totalNumberAlreadyInvested"))
    first_sale = g(".//dateOfFirstSale/value")
    signed = g(".//signature/signatureDate")
    revenue_range = g(".//issuerSize/revenueRange")
    clar = g(".//offeringSalesAmounts/clarificationOfResponse")
    safe_amt = find(r"\$([\d,]+) of securities issued upon conversion", clar).group(1)
    juris = g(".//primaryIssuer/jurisdictionOfInc").title()
    city = g(".//primaryIssuer/issuerAddress/city").title()
    persons = [(p.findtext("relatedPersonName/firstName"), p.findtext("relatedPersonName/lastName"),
                [r.text for r in p.findall("relatedPersonRelationshipList/relationship")])
               for p in fd.findall(".//relatedPersonInfo")]
    press_m = find(r"\$(\d+) million seed round", norm(SOURCES[s_pulse]["_text"]))
    press_millions = int(press_m.group(1))
    sold_millions = round(sold / 1_000_000)

    # Hacker News, parsed.
    hn = json.loads((RAW / "hn" / "ploy.json").read_text())
    on_domain = [h for h in hn["domain_hits"] if host_of(h.get("url") or "") == "ploy.ai"]
    top = max(on_domain, key=lambda h: h["points"])
    app = json.loads((RAW / "appstore_ploy.json").read_text())
    own_apps = [r for r in app["results"] if "ploy" in (r.get("sellerName") or "").lower()
                or host_of(r.get("sellerUrl") or "") == "ploy.ai"]
    gh = json.loads((RAW / "github_user_bryantchou.json").read_text())
    job = page["jobPostings"][0]

    sections = [
        {"key": "outside", "title": "The outside world", "parts": [
            {"label": "Website", "claims": [
                claim(f"Prices: Free ${free}, Starter ${starter} and Pro ${pro} a month. Enterprise is priced on request.",
                      s_pricing, pm.group(0)),
                claim("Press names Hex and Clay as customers, and the agencies Tonik and TNT Growth.", s_vca,
                      "Agencies like Tonik and TNT Growth build and run client sites on the platform"),
                claim("The company says it is based in San Francisco and New York.", s_vca,
                      "Ploy is a small team based in San Francisco and New York, and it's hiring."),
            ]},
            {"label": "Launch YC", "claims": [
                claim(f"Launched on YC on {launch['created_at'][:10]}, with {launch['total_vote_count']} votes.", s_launch,
                      f"launches[0].total_vote_count: {launch['total_vote_count']}", url=launch["url"]),
                claim("The company says over 13% of the batch use Ploy.", s_launch,
                      "Over 13% of the YC P26 companies are using Ploy", kind="company says"),
            ]},
            {"label": "Hacker News", "claims": [
                claim(f"A company blog post on moving its agent to a new model drew {top['points']} points and "
                      f"{top['num_comments']} comments ({top['created_at'][:10]}).", s_hn,
                      f"points {top['points']} | comments {top['num_comments']}",
                      url=f"https://news.ycombinator.com/item?id={top['objectID']}"),
                claim(f"The domain search also returned other sites, such as play.ai. Tricorder kept only links on ploy.ai: "
                      f"{len(on_domain)} of {len(hn['domain_hits'])}.", s_hn, "domain_query: ploy.ai"),
                claim("No Hacker News story or comment naming Ploy uses a dispute word.", s_disp, "ploy,summary,,1,0,"),
            ]},
            {"label": "App Store", "claims": [] if own_apps else [
                claim(f"No signal: no App Store app from Ploy. The search returned {app['resultCount']} apps from other sellers.",
                      s_app, f"resultCount: {app['resultCount']}", kind="no signal"),
            ]},
            {"label": "SEC filings", "claims": [
                claim(f"Form D filed {signed} by Ploy, Inc., a {juris} company in {city}.", s_formd,
                      f"<signatureDate>{signed}</signatureDate>"),
                claim(f"${sold:,} sold, out of ${offered:,} offered.", s_formd,
                      f"<totalAmountSold>{sold}</totalAmountSold>"),
                claim(f"Of that, ${safe_amt} came from SAFEs that converted.", s_formd, clar),
                claim(f"{investors} investors. First sale on {first_sale}.", s_formd,
                      f"<totalNumberAlreadyInvested>{investors}</totalNumberAlreadyInvested>"),
                claim(f"Press reports a ${press_millions}M seed led by First Round Capital and Y Combinator. "
                      f"The Form D amount rounds to ${sold_millions}M, so the two "
                      f"{'match' if press_millions == sold_millions else 'differ'}.", s_pulse,
                      "The round was led by First Round Capital and Y Combinator.",
                      kind="match" if press_millions == sold_millions else "differs"),
            ]},
        ]},
        {"key": "founders", "title": "The founders", "cards": [
            {"name": f"{persons[0][0]} {persons[0][1]}", "role": "Founder and CEO", "x": co["founders"][0]["twitter_url"], "claims": [
                claim("Co-founder and CTO of Webflow for 12 years, in his own words.", s_launch,
                      "After 12 years as the cofounder and CTO at Webflow"),
                claim("Before that, co-founder and CTO of Vungle, 2011 to 2013, per his YC bio.", s_yc,
                      "vungle ➡️ $LFTO (2011-2013)"),
                claim(f"Signed the Form D as Chief Executive Officer. It lists him as {', '.join(r.lower() for r in persons[0][2])}.",
                      s_formd, "<signatureTitle>Chief Executive Officer</signatureTitle>"),
                claim(f"A GitHub account named BryantChou was made on {gh['created_at'][:10]} and has {gh['followers']} followers. "
                      "Tricorder cannot confirm it is his.", s_gh, f"created_at: {gh['created_at']}", kind="unconfirmed"),
            ]},
            {"name": f"{persons[1][0]} {persons[1][1]}", "role": "Director, per the Form D", "claims": [
                claim("Listed on the Form D as a director. The saved files do not say who he is.", s_formd,
                      f"<lastName>{persons[1][1]}</lastName>"),
                placeholder("Background from public talks and writing, once the founder scan reads them."),
            ]},
        ]},
        {"key": "comps", "title": "Comps", "claims": [
            claim("The site has comparison pages against Framer, Vercel, Lovable, Bolt and v0.", s_site, "Ploy vs Framer"),
            claim("It moves sites over from WordPress, Webflow, Framer and Wix, so those are the tools it replaces.", s_site,
                  "WordPress, Webflow, Framer, Wix, or a custom build."),
            claim("Same batch, close pitch: Sherpa, \"Make websites improve themselves.\"", s_csv, "Make websites improve themselves."),
            claim("Same batch, close pitch: Revnu, \"Your AI growth hire.\"", s_csv, "Your AI growth hire."),
            placeholder("Recent private rounds in AI website builders, each from its Form D, with why it is a fair comp."),
            placeholder("Public comps in website and marketing software, with revenue multiples from market data."),
        ], "gaps": [gap("Revenue multiples for public comps.", "Needs a market data source. None is set up on this laptop.")]},
        {"key": "signals", "title": "Market signals", "claims": [
            claim(f"Hiring: one open role on YC, {job['title']}, {job['salaryRange'].replace(' - ', ' to ')}, {job['location']}.",
                  s_yc, f"jobPostings[0].salaryRange: {job['salaryRange']}"),
            claim(f"Team size on YC: {co['team_size']}.", s_yc, f"company.team_size: {co['team_size']}"),
            placeholder("Competitors' hiring: open roles at Framer and Webflow over the last 90 days."),
            placeholder("Competitors' reviews and pricing changes this quarter."),
        ], "gaps": [gap("Web traffic for Ploy and its competitors.", "Needs AKTA_API_KEY on Akta's Subscription tier.")]},
    ]

    room_gaps = [
        {"text": "Revenue. No figure is public.", "why": f"The Form D gives the revenue range as \"{revenue_range}\".",
         "ids": ["C02", "C03"]},
        {"text": "Which of the named customers pay, and how much.", "why": "Press names Hex and Clay. Only billing data shows what they pay.",
         "ids": ["C34"]},
        {"text": f"Who held the ${safe_amt} of SAFEs that converted, and on what terms.",
         "why": "The Form D gives the total only.", "ids": ["C75", "C72"]},
        {"text": "Burn and runway after the seed.", "why": "No public source shows spending.", "ids": ["C20", "C19"]},
        {"text": f"Cost to serve a customer on the ${starter} and ${pro} plans.",
         "why": "Plans are sold as credits. Model costs per credit are internal.", "ids": ["C30"]},
        {"text": f"The plan for the team of {co['team_size']}.", "why": "YC shows team size and one open role only.", "ids": ["C22"]},
    ]

    setup = {
        "name": {"value": co["name"], "source": s_yc},
        "website": {"value": co["website"], "source": s_csv},
        "founders": {"value": ", ".join(f["full_name"] for f in co["founders"]), "source": s_yc},
        "batch": {"value": f"{co['batch_name']} ({co['batch']})", "source": s_yc},
        "stage": {"value": "seed", "source": s_formd, "note": "Last round: seed, per the Form D and press"},
        "location": {"value": co["location"], "source": s_yc},
        "team_size": {"value": str(co["team_size"]), "source": s_yc},
    }
    # Public facts the synthetic room must agree with, and the pre-room claims step 5 checks against the room.
    pre = {
        "formd_sold": claim(f"Form D: ${sold:,} sold.", s_formd, f"<totalAmountSold>{sold}</totalAmountSold>"),
        "formd_safe": claim(f"Form D: ${safe_amt} came from SAFEs that converted.", s_formd, clar),
        "formd_investors": claim(f"Form D: {investors} investors.", s_formd,
                                 f"<totalNumberAlreadyInvested>{investors}</totalNumberAlreadyInvested>"),
        "prices": claim(f"Prices: Free ${free}, Starter ${starter} and Pro ${pro} a month.", s_pricing, pm.group(0)),
        "team": claim(f"Team size on YC: {co['team_size']}.", s_yc, f"company.team_size: {co['team_size']}"),
        "batch_share": claim("The company says over 13% of the batch use Ploy.", s_launch,
                             "Over 13% of the YC P26 companies are using Ploy", kind="company says"),
        "named_customers": claim("Press names Hex and Clay as customers.", s_vca,
                                 "Agencies like Tonik and TNT Growth build and run client sites on the platform"),
        "hiring": claim(f"Hiring: one open role on YC, {job['title']}.", s_yc, f"jobPostings[0].salaryRange: {job['salaryRange']}"),
        "revenue_range": claim(f"Revenue: the Form D gives the range as \"{revenue_range}\".", s_formd,
                               f"<revenueRange>{revenue_range}</revenueRange>"),
    }
    facts = {"sold": sold, "safe": int(safe_amt.replace(",", "")), "investors": investors, "free": free,
             "starter": starter, "pro": pro, "team": co["team_size"], "batch_size": len(load_companies()),
             "batch_share_pct": int(find(r"Over (\d+)% of the YC P26", launch["body"]).group(1)), "seed_first_sale": first_sale}
    return {"slug": "ploy", "setup": setup, "greeting": persons[0][0], "sections": sections, "room_gaps": room_gaps,
            "facts": facts, "pre": pre}


# Sazabi ----------------------------------------------------------------------------------


def sazabi() -> dict:
    page = yc_page("sazabi")
    co = page["company"]
    launch = page["launches"][0]
    f0 = co["founders"][0]
    s_yc = source(RAW / "yc_page_sazabi.json", "https://www.ycombinator.com/companies/sazabi", "YC company page: Sazabi")
    s_pricing = source(RAW / "site_sazabi_pricing.html", "https://www.sazabi.com/pricing", "Sazabi pricing page")
    s_report = source(RESEARCH / "research_demo_companies.md", None, "Tricorder research: real companies for the demo")
    s_cust = source(RAW / "site_sazabi_customers.html", "https://www.sazabi.com/customers", "Sazabi customers page")
    s_seed = source(RAW / "blog_sazabi_seed.html", "https://www.sazabi.com/blog/seed-round", "Sazabi blog: our $8M seed round")
    s_sa = source(RAW / "news_sazabi_siliconangle.html",
                  "https://siliconangle.com/2026/04/08/startup-sazabi-bets-logs-ai-agents-replace-traditional-observability-stacks/",
                  "SiliconANGLE: Sazabi bets on logs and AI agents (2026-04-08)")
    s_hn = source(RAW / "hn" / "sazabi.json", "https://hn.algolia.com/api/v1/search?query=sazabi.com", "Hacker News search: stories linking sazabi.com")
    s_disp = source(RESEARCH / "demo_dispute_scan.csv", None, "Dispute-word scan of Hacker News, from demo_dispute_scan.py")
    s_app = source(RAW / "appstore_sazabi.json", "https://itunes.apple.com/search?term=sazabi&entity=software", "Apple App Store search: sazabi")
    s_edgar = source(RAW / "edgar_company_sazabi.xml",
                     "https://www.sec.gov/cgi-bin/browse-edgar?company=sazabi&type=D&owner=include&action=getcompany&count=40",
                     "SEC EDGAR company search: sazabi, Form D")
    s_gh = source(RAW / "github_user_shcallaway.json", "https://github.com/shcallaway", "GitHub account: shcallaway")
    s_talk = source(RAW / "yc_library_sazabi_talk.html", "https://ycombinator.com/library/bp-the-end-of-manual-debugging",
                    "YC Library: The End of Manual Debugging")
    s_csv = source(CSV_PATH, "https://www.ycombinator.com/companies?batch=Spring%202026", "YC directory: Spring 2026 companies")
    s_superlog = source(RAW / "yc_page_superlog.json", "https://www.ycombinator.com/companies/superlog", "YC company page: Superlog")

    # Prices: parsed from the pricing page, then checked against the research report that cites it.
    ptxt = SOURCES[s_pricing]["_text"]
    prices = {}
    for plan in ("Hobby", "Startup", "Growth"):
        m = find(rf"\n {plan}\n(?:.*\n)?? ?\$ [^\n]*\}}\s*([\d]+)\s*\n", "\n" + ptxt)
        prices[plan] = int(m.group(1))
    rq = "pricing shows Hobby $50, Startup $200, Growth $1,000 a month, and Enterprise"
    report_prices = [int(x.replace(",", "")) for x in re.findall(r"\$([\d,]+)", rq)]
    if report_prices != [prices["Hobby"], prices["Startup"], prices["Growth"]]:
        raise SystemExit(f"Sazabi prices differ: page {prices}, report {report_prices}")
    over = find(r"additional data costs \$([\d.]+) per GB", norm(ptxt))

    seed_m = find(r"\$(\d+) million seed round", norm(SOURCES[s_seed]["_text"]))
    dp = find(r"signed up (\d+) design partners", norm(SOURCES[s_seed]["_text"]))
    usage_q = "In the past month we’ve onboarded 35 new teams, run 8,000 background investigations, detected 2,000 issues, ingested 2 TB of logs"
    um = find(r"onboarded (\d+) new teams, run ([\d,]+) background investigations, detected ([\d,]+) issues, ingested (\d+) TB",
              launch["body"])
    team_m = find(r"team of (\w+) engineers", launch["body"])

    hn = json.loads((RAW / "hn" / "sazabi.json").read_text())
    on_domain = [h for h in hn["domain_hits"] if host_of(h.get("url") or "") == "sazabi.com"]
    max_pts = max(h["points"] for h in on_domain)
    app = json.loads((RAW / "appstore_sazabi.json").read_text())
    own_apps = [r for r in app["results"] if "sazabi" in (r.get("sellerName") or "").lower()]
    edgar_entries = len(ET.parse(RAW / "edgar_company_sazabi.xml").getroot().findall("{http://www.w3.org/2005/Atom}entry"))
    gh = json.loads((RAW / "github_user_shcallaway.json").read_text())
    sl = yc_page("superlog")["company"]

    sections = [
        {"key": "outside", "title": "The outside world", "parts": [
            {"label": "Website", "claims": [
                claim(f"Prices: Hobby ${prices['Hobby']}, Startup ${prices['Startup']} and Growth ${prices['Growth']:,} "
                      "every 30 days. Enterprise is custom.", s_report, rq, url="https://www.sazabi.com/pricing"),
                claim(f"Usage past the plan is billed, for example ${over.group(1)} per GB of logs over the included amount.",
                      s_pricing, over.group(0)),
                claim("Case studies on its site: Weave, Mastra and XMTP Labs.", s_cust, "XMTP Labs x Sazabi"),
                claim(f"The seed post says {dp.group(1)} design partners signed up in under a month.", s_seed,
                      dp.group(0), kind="company says"),
            ]},
            {"label": "Launch YC", "claims": [
                claim(f"Launched on YC on {launch['created_at'][:10]}, with {launch['total_vote_count']} votes.", s_yc,
                      f"launches[0].total_vote_count: {launch['total_vote_count']}", url=launch["url"]),
                claim(f"The launch post says that in one month it onboarded {um.group(1)} teams, ran {um.group(2)} "
                      f"investigations and took in {um.group(4)} TB of logs.", s_yc, usage_q, kind="company says"),
            ]},
            {"label": "Hacker News", "claims": [
                claim(f"Little attention so far: {len(on_domain)} stories link sazabi.com, the largest with {max_pts} points.",
                      s_hn, "domain_query: sazabi.com"),
                claim("No Hacker News story or comment naming Sazabi uses a dispute word.", s_disp, "sazabi,summary,,3,0,"),
            ]},
            {"label": "App Store", "claims": [] if own_apps else [
                claim(f"No signal: no App Store app from Sazabi. The search returned {app['resultCount']} apps from other sellers.",
                      s_app, f"resultCount: {app['resultCount']}", kind="no signal"),
            ]},
            {"label": "SEC filings", "claims": [
                claim(f"No signal: EDGAR's company search for Sazabi returned {edgar_entries} Form D filings.", s_edgar,
                      "company=sazabi&amp;type=D", kind="no signal"),
                claim(f"The company's own post: a ${seed_m.group(1)}M seed co-led by J2 Ventures, Village Global and Y Combinator.",
                      s_seed, "Our $8 million seed round is co-led by J2 Ventures, Village Global, and Y Combinator."),
                claim("In April 2026 the company said it was still raising its seed.", s_sa,
                      "confirmed it’s in the process of raising seed capital"),
            ]},
        ]},
        {"key": "founders", "title": "The founders", "cards": [
            {"name": f0["full_name"], "role": f0["title"], "x": f0["twitter_url"], "github": "https://github.com/shcallaway", "claims": [
                claim("A second-time YC founder, per his YC bio. Earlier roles at Brex and Crunchbase.", s_yc,
                      "Sherwood Callaway is a 2x YC founder"),
                claim("Started the infrastructure and observability teams at Brex, per the launch post.", s_yc,
                      "previously started the infrastructure and observability teams at Brex"),
                claim("An earlier venture was Opkit, a phone call automation platform, per SiliconANGLE.", s_sa,
                      "phone call automation platform Opkit Inc."),
                claim(f"GitHub account since {gh['created_at'][:4]}, {gh['followers']} followers, company set to {gh['company']}.",
                      s_gh, f"created_at: {gh['created_at']}"),
                claim("Gave a YC Library talk, The End of Manual Debugging.", s_talk, "The End of Manual Debugging"),
                claim(f"The launch post says the team is {team_m.group(1)} engineers, three of them from Brex.", s_yc,
                      "We’re a team of nine engineers in total, including three early members of the Brex team"),
            ]},
        ]},
        {"key": "comps", "title": "Comps", "claims": [
            claim("The company names the legacy tools it replaces: Datadog, Grafana, Sentry and Axiom.", s_yc,
                  "Legacy players like Datadog, Grafana, Sentry, and Axiom"),
            claim("It names AI SRE startups that sit on top of those tools: Traversal and Resolve.", s_yc,
                  "AI SRE startups like Traversal and Resolve"),
            claim(f"Same batch, overlapping product: Superlog, \"{sl['one_liner']}\", team of {sl['team_size']} in {sl['location']}.",
                  s_superlog, f"company.one_liner: {sl['one_liner']}"),
            claim("Tricorder's research marks Superlog as a fair comp. Its round is not confirmed.", s_report,
                  "It would make a fair comp for a Sazabi room."),
            placeholder("Recent private rounds for Traversal and Resolve, each from its Form D, with why it is a fair comp."),
            placeholder("Datadog as the public comp, with its revenue multiple from market data."),
        ], "gaps": [gap("Revenue multiples for public comps.", "Needs a market data source. None is set up on this laptop.")]},
        {"key": "signals", "title": "Market signals", "claims": [
            claim("Hiring: no open roles listed on YC.", s_yc, "jobPostings: (none)", kind="no signal"),
            claim(f"Team size on YC: {co['team_size']}.", s_yc, f"company.team_size: {co['team_size']}"),
            placeholder("Competitors' hiring: open SRE and observability roles at Datadog and Grafana over the last 90 days."),
            placeholder("Competitors' reviews and pricing changes this quarter."),
        ], "gaps": [gap("Web traffic for Sazabi and its competitors.", "Needs AKTA_API_KEY on Akta's Subscription tier.")]},
    ]

    room_gaps = [
        {"text": f"How many of the {dp.group(1)} design partners pay, and on which plan.",
         "why": "The seed post counts design partners, not paying customers.", "ids": ["C03"]},
        {"text": "Revenue behind the usage numbers.",
         "why": f"The launch post gives {um.group(1)} teams and {um.group(4)} TB of logs in a month, and no revenue.", "ids": ["C02"]},
        {"text": f"Storage and AI cost per customer, against plans from ${prices['Hobby']} to ${prices['Growth']:,}.",
         "why": "Cost to serve is internal.", "ids": ["C30"]},
        {"text": f"The papers behind the ${seed_m.group(1)}M seed.",
         "why": "No Form D was found by name, so the instruments and holders come only from the room.", "ids": ["C75", "C72"]},
        {"text": "Burn and runway after the seed.", "why": "No public source shows spending.", "ids": ["C20", "C19"]},
        {"text": f"The hiring plan for a team of {team_m.group(1)} engineers.", "why": "YC lists no open roles.", "ids": ["C22"]},
    ]

    setup = {
        "name": {"value": co["name"], "source": s_yc},
        "website": {"value": co["website"], "source": s_csv},
        "founders": {"value": ", ".join(f["full_name"] for f in co["founders"]), "source": s_yc},
        "batch": {"value": f"{co['batch_name']} ({co['batch']})", "source": s_yc},
        "stage": {"value": "seed", "source": s_seed, "note": "Last round: seed, per the company's post"},
        "location": {"value": co["location"], "source": s_yc},
        "team_size": {"value": str(co["team_size"]), "source": s_yc},
    }
    pre = {
        "prices": claim(f"Prices: Hobby ${prices['Hobby']}, Startup ${prices['Startup']} and Growth ${prices['Growth']:,}.",
                        s_report, rq, url="https://www.sazabi.com/pricing"),
        "seed": claim(f"The company's own post: a ${seed_m.group(1)}M seed.", s_seed,
                      "Our $8 million seed round is co-led by J2 Ventures, Village Global, and Y Combinator."),
        "design_partners": claim(f"The seed post says {dp.group(1)} design partners signed up.", s_seed, dp.group(0),
                                 kind="company says"),
        "team": claim(f"Team size on YC: {co['team_size']}.", s_yc, f"company.team_size: {co['team_size']}"),
        # Pre-room claims the synthetic room checks. Each repeats a readout claim's source and quote, so the
        # working page can mark that claim in place.
        "usage": claim(f"The launch post says that in one month it onboarded {um.group(1)} teams, ran {um.group(2)} "
                       f"investigations and took in {um.group(4)} TB of logs.", s_yc, usage_q, kind="company says"),
        "engineers": claim(f"The launch post says the team is {team_m.group(1)} engineers, three of them from Brex.", s_yc,
                           "We’re a team of nine engineers in total, including three early members of the Brex team"),
        "formd_none": claim(f"No signal: EDGAR's company search for Sazabi returned {edgar_entries} Form D filings.", s_edgar,
                            "company=sazabi&amp;type=D", kind="no signal"),
        "still_raising": claim("In April 2026 the company said it was still raising its seed.", s_sa,
                               "confirmed it’s in the process of raising seed capital"),
        "named_customers": claim("Case studies on its site: Weave, Mastra and XMTP Labs.", s_cust, "XMTP Labs x Sazabi"),
        "hiring": claim("Hiring: no open roles listed on YC.", s_yc, "jobPostings: (none)", kind="no signal"),
    }
    words = {"five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}
    seed_txt = norm(SOURCES[s_seed]["_text"])
    facts = {"hobby": prices["Hobby"], "startup": prices["Startup"], "growth": prices["Growth"],
             "seed": int(seed_m.group(1)) * 1_000_000, "design_partners": int(dp.group(1)), "team": co["team_size"],
             "over_per_gb": float(over.group(1)), "usage_teams": int(um.group(1)), "usage_investigations": int(um.group(2).replace(",", "")),
             "usage_issues": int(um.group(3).replace(",", "")), "usage_tb": int(um.group(4)), "launch_date": launch["created_at"][:10],
             "engineers": words[team_m.group(1).lower()], "angels_more_than": int(find(r"more than (\d+) angel investors", seed_txt).group(1)),
             "seed_post_date": find(r"(\d{4}-\d{2}-\d{2})T00:00:00Z", SOURCES[s_seed]["_text"]).group(1),
             "still_raising_date": datetime.strptime(find(r"UPDATED [\d:]+ EDT / ([A-Z]+ \d{2} \d{4})", SOURCES[s_sa]["_text"]).group(1).title(),
                                                "%B %d %Y").date().isoformat(), "edgar_formd": edgar_entries}
    return {"slug": "sazabi", "setup": setup, "greeting": f0["full_name"].split()[0], "sections": sections, "room_gaps": room_gaps,
            "facts": facts, "pre": pre}


# Checklist -------------------------------------------------------------------------------


def lcfirst(s: str) -> str:
    return s if len(s) > 1 and s[1].isupper() else s[0].lower() + s[1:]


def checklist() -> list[dict]:
    with open(CHECKLIST, newline="", encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if r["kind"] in ("document", "ask")]
    out = []
    for r in rows:
        g = gd.GUIDANCE.get(r["guide"]) if r["guide"] else None
        out.append({
            "id": r["id"], "kind": r["kind"], "piece": r["piece"], "item": r["item"],
            "stages": {"pre_seed": r["pre_seed"], "seed": r["seed"], "series_a": r["series_a"]},
            "closing_at_early_stage": r["id"] in CLOSING_AT_SEED,
            "title": g.title if g and r["kind"] == "document" else r["item"],
            "ask": FOUNDER_TEXT.get(r["id"]) or f"Please send your {lcfirst(r['item'])}.",
            "includes": gd.includes(r["guide"]) if r["kind"] == "document" else None,
            "guide": r["guide"] or None,
            "guidance": {"what": g.what, "form": g.form, "good": list(g.good), "path": g.path} if g else None,
        })
    return out


def copy_knowledge() -> None:
    """Copy Kimmy's expert knowledge files beside the page, so each report can link the file it was read with."""
    out = HERE / "knowledge"
    out.mkdir(exist_ok=True)
    for f in sorted((ROOT / "knowledge").glob("*.md")):
        (out / f.name).write_text(f.read_text())


def main() -> None:
    copy_knowledge()
    companies = load_companies()
    founders = {}
    for c in companies:
        f = founders_from_yc(c["slug"])
        if f:
            founders[c["slug"]] = f
    research = {"ploy": ploy(), "sazabi": sazabi()}
    # The synthetic data rooms for steps 5 to 8. Every figure that the public record states is taken from it.
    from synthetic_rooms import ploy_room, sazabi_room  # noqa: E402
    research["ploy"]["room"] = ploy_room(research["ploy"]["facts"], research["ploy"]["pre"])
    research["sazabi"]["room"] = sazabi_room(research["sazabi"]["facts"], research["sazabi"]["pre"])
    s_csv = source(CSV_PATH, "https://www.ycombinator.com/companies?batch=Spring%202026", "YC directory: Spring 2026 companies")
    data = {
        "built": datetime.now().isoformat(timespec="seconds"),
        "built_by": rel(Path(__file__)),
        "list_source": s_csv,
        "companies": companies,
        "yc_founders": founders,
        "research": research,
        "checklist": checklist(),
        "checklist_source": rel(CHECKLIST),
        "sources": {k: {kk: vv for kk, vv in v.items() if kk != "_text"} for k, v in SOURCES.items()},
    }
    text = json.dumps(data, indent=1, ensure_ascii=False)
    if "linkedin.com" in text.lower():
        raise SystemExit("A LinkedIn link reached data.json")
    (HERE / "data.json").write_text(text)
    (HERE / "data.js").write_text("window.DATA = " + text + ";\n")
    n_claims = sum(1 for r in research.values() for s in r["sections"] for c in
                   ([c for p in s.get("parts", []) for c in p["claims"]] + s.get("claims", [])
                    + [c for card in s.get("cards", []) for c in card["claims"]]) if not c.get("placeholder"))
    print(f"companies: {len(companies)}; sources: {len(SOURCES)}; sourced claims: {n_claims}; "
          f"checklist items: {len(data['checklist'])}")


if __name__ == "__main__":
    main()
