"""Print publication-date hints (datePublished, post_date, article:published_time) for URLs.

Run: python3 -I web_dates.py URL [URL ...]
"""
import re
import sys
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
PAT = re.compile(
    r'(datePublished"?\s*:\s*"[^"]{4,30}"|post_date"?\s*:\s*"[^"]{4,30}"|'
    r'article:published_time"\s+content="[^"]{4,30}"|"publishedAt"\s*:\s*"[^"]{4,30}"|'
    r'"published_at"\s*:\s*"[^"]{4,30}")'
)


def main():
    for url in sys.argv[1:]:
        if "reddit.com" in url:
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
        except Exception as exc:
            print("FAIL", url, exc)
            continue
        found = sorted(set(PAT.findall(raw)))[:4]
        print(url, "->", found)


if __name__ == "__main__":
    main()
