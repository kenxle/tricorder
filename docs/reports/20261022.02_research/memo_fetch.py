"""Fetch investment memos and memo templates; save their text under raw/memos/.

Headings in the page (<h1> to <h4>) are kept as Markdown '#' lines, so the
section list in memos.csv can be read from the saved file.
Images are kept as an [image] line, because some memos show their tables as pictures.\nOutbound links are kept as [text](url), so a memo's citations survive.
Bold text is kept as **bold**, because some memos use bold lines as headings.
PDFs are converted with pdftotext -layout. Markdown and plain text are saved as they are.
Never pass reddit.com URLs (the script refuses them).

Run: python3 -I memo_fetch.py NAME URL [NAME URL ...]
The file is saved as raw/memos/NAME.txt with a SOURCE line on top.
"""
import html
import pathlib
import re
import subprocess
import sys
import tempfile
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "raw" / "memos"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def to_text(raw):
    raw = re.sub(r"(?is)<(script|style|noscript|svg|nav|footer|button|select)[^>]*>.*?</\1>", " ", raw)
    for n in range(1, 5):
        raw = re.sub(rf"(?is)<h{n}[^>]*>(.*?)</h{n}>",
                     lambda m, n=n: "\n\n" + "#" * n + " " + re.sub(r"<[^>]+>", " ", m.group(1)).strip() + "\n\n", raw)
    raw = re.sub(r"(?is)<img\s[^>]*>", "\n[image]\n", raw)
    raw = re.sub(r'(?is)<a\s[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>',
                 lambda m: "[" + re.sub(r"<[^>]+>", " ", m.group(2)).strip() + "](" + m.group(1) + ")", raw)
    raw = re.sub(r"(?is)<(strong|b)(\s[^>]*)?>(.*?)</\1>",
                 lambda m: "**" + re.sub(r"<[^>]+>", " ", m.group(3)).strip() + "**", raw)
    raw = re.sub(r"(?i)<li[^>]*>", "\n- ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</div>|</blockquote>|</tr>", "\n", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    raw = re.sub(r"[ \t\xa0]+", " ", raw)
    raw = re.sub(r" *\n *", "\n", raw)
    raw = re.sub(r"\*\*\s*\*\*", "", raw)
    raw = re.sub(r"\n{3,}", "\n\n", raw)
    return raw.strip()


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/pdf"})
    with urllib.request.urlopen(req, timeout=40) as resp:
        return resp.read(), resp.headers.get("Content-Type", "")


def main():
    args = sys.argv[1:]
    for name, url in zip(args[0::2], args[1::2]):
        if "reddit.com" in url:
            print("SKIP reddit", url)
            continue
        try:
            body, ctype = fetch(url)
        except Exception as exc:
            print("FAIL", name, url, exc)
            continue
        if "pdf" in ctype or body[:5] == b"%PDF-":
            with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
                tmp.write(body)
                tmp.flush()
                text = subprocess.run(["pdftotext", "-layout", tmp.name, "-"],
                                      capture_output=True, text=True).stdout
        elif url.endswith(".md") or "text/plain" in ctype:
            text = body.decode("utf-8", errors="replace")
        else:
            text = to_text(body.decode("utf-8", errors="replace"))
        path = OUT / f"{name}.txt"
        path.write_text(f"SOURCE: {url}\n\n{text}\n")
        print("OK", name, len(text))


if __name__ == "__main__":
    main()
