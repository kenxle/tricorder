"""Parse saved YC company pages (raw/demo_companies/yc_page_<slug>.html) and print the company,
founders with their public links, launches and news from the page's embedded data.

Run: python3 -I demo_yc_pages.py slug [slug ...]
Writes raw/demo_companies/yc_page_<slug>.json (the parsed props) for each.
"""
import html
import json
import pathlib
import re
import sys

RAW = pathlib.Path(__file__).resolve().parent / "raw" / "demo_companies"


def main():
    for slug in sys.argv[1:]:
        page = (RAW / f"yc_page_{slug}.html").read_text()
        m = re.search(r'data-page="([^"]*)"', page)
        data = json.loads(html.unescape(m.group(1)))
        props = data["props"]
        (RAW / f"yc_page_{slug}.json").write_text(json.dumps(props, indent=1))
        c = props.get("company", {})
        print("=" * 100)
        print(c.get("name"), "|", c.get("batch_name") or c.get("batch"), "|", c.get("website"), "|", c.get("location"), "| founded", c.get("year_founded"), "| team", c.get("team_size"))
        print("one-liner:", c.get("one_liner"))
        print("long:", (c.get("long_description") or "")[:900].replace("\n", " "))
        for k in ("linkedin_url", "twitter_url", "fb_url", "cb_url", "github_url"):
            if c.get(k):
                print(" ", k, c.get(k))
        for f in c.get("founders", []):
            print(" FOUNDER:", f.get("full_name"), "|", f.get("title"), "|", (f.get("founder_bio") or "")[:300].replace("\n", " "))
            for k in ("twitter_url", "linkedin_url", "github_url", "personal_url"):
                if f.get(k):
                    print("    ", k, f.get(k))
        for l in props.get("launches", []) or []:
            print(" LAUNCH:", {k: (str(v)[:160] if v else v) for k, v in l.items() if k in ("title","tagline","url","slug","created_at","vote_count","total_vote_count")})
        for n in props.get("newsItems", []) or []:
            print(" NEWS:", {k: (str(v)[:160] if v else v) for k, v in n.items()})
        others = [k for k in props.keys() if k not in ("company",)]
        print(" videos:", props.get("videos"))
        print(" github:", c.get("github_url"), "| batch code:", c.get("batch"))


if __name__ == "__main__":
    main()
