"""Financials group fetcher. Usage: python3 -I fetch_group.py <slug> URL [URL ...]
Saves plain text to raw/<slug>/<urlslug>.txt, first line 'SOURCE: url'. Refuses reddit.com. Reports HTTP errors."""
import html, pathlib, re, sys, urllib.request, urllib.error, gzip

OUT = pathlib.Path(__file__).resolve().parent
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

def slug(url):
    s = re.sub(r"^https?://(www\.)?", "", url)
    return re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_")[:110]

def to_text(raw):
    raw = re.sub(r"(?is)<(script|style|noscript|svg|nav|footer)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</p>|</h[1-6]>|</li>|</div>|</tr>|</blockquote>", "\n", raw)
    raw = re.sub(r"(?i)<li[^>]*>", "- ", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    raw = re.sub(r"[ \t\xa0]+", " ", raw)
    raw = re.sub(r"\n\s*\n+", "\n\n", raw)
    return raw.strip()

dest = sys.argv[1]
for url in sys.argv[2:]:
    if "reddit.com" in url:
        print("SKIP reddit", url); continue
    path = OUT / dest / f"{slug(url)}.txt"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*", "Accept-Encoding": "gzip"})
        with urllib.request.urlopen(req, timeout=40) as r:
            data = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                data = gzip.decompress(data)
            raw = data.decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, url); continue
    except Exception as e:
        print("FAIL", url, e); continue
    t = to_text(raw)
    path.write_text(f"SOURCE: {url}\n\n{t}")
    print("OK", len(t), dest + "/" + path.name)
