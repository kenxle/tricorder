"""Fetch web pages for the R1 track and save their plain text under raw/voc/web_<slug>.txt.

Never pass reddit.com URLs (the script refuses them).
Run: python3 -I web_fetch.py URL [URL ...]
"""
import html
import pathlib
import re
import sys
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "raw" / "voc"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def slug(url):
    s = re.sub(r"^https?://(www\.)?", "", url)
    return re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_")[:120]


def to_text(raw):
    raw = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</p>|</h[1-6]>|</li>|</div>|</blockquote>", "\n", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    raw = re.sub(r"[ \t]+", " ", raw)
    raw = re.sub(r"\n\s*\n+", "\n\n", raw)
    return raw.strip()


def main():
    for url in sys.argv[1:]:
        if "reddit.com" in url:
            print("SKIP reddit", url)
            continue
        path = OUT / f"web_{slug(url)}.txt"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
        except Exception as exc:
            print("FAIL", url, exc)
            continue
        text = to_text(raw)
        path.write_text(f"SOURCE: {url}\n\n{text}")
        print("OK", len(text), path.name)


if __name__ == "__main__":
    main()
