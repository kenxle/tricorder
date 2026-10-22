"""R4 fetcher. Saves plain text of each URL to raw/data_room/<slug>.txt (first line SOURCE: url).
Refuses reddit.com. Run: python3 -I fetch_pages.py URL [URL ...]
"""
import html, pathlib, re, sys, urllib.request

OUT = pathlib.Path(__file__).resolve().parent
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

def slug(url):
    s = re.sub(r"^https?://(www\.)?", "", url)
    return re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_")[:100]

def to_text(raw):
    raw = re.sub(r"(?is)<(script|style|noscript|svg|nav|footer|header)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</p>|</h[1-6]>|</li>|</div>|</tr>", "\n", raw)
    raw = re.sub(r"(?i)<li[^>]*>", "- ", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    raw = re.sub(r"[ \t]+", " ", raw)
    raw = re.sub(r"\n\s*\n+", "\n\n", raw)
    return raw.strip()

for url in sys.argv[1:]:
    if "reddit.com" in url:
        print("SKIP", url); continue
    path = OUT / f"{slug(url)}.txt"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print("FAIL", url, e); continue
    t = to_text(raw)
    path.write_text(f"SOURCE: {url}\n\n{t}")
    print("OK", len(t), path.name)
