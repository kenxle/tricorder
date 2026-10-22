"""Fetch public pages for the demo-company track and save them raw under raw/demo_companies/.

Never passes reddit.com or linkedin.com URLs (the script refuses them).
Run: python3 -I demo_fetch.py URL [URL ...]
Optional: NAME=URL to choose the saved file name.
"""
import pathlib
import re
import sys
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "raw" / "demo_companies"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def slug(url):
    s = re.sub(r"^https?://(www\.)?", "", url)
    return re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_")[:120]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for arg in sys.argv[1:]:
        name = None
        url = arg
        if "=" in arg and not arg.startswith("http"):
            name, url = arg.split("=", 1)
        if "reddit.com" in url or "linkedin.com" in url:
            print("SKIP refused domain", url)
            continue
        ext = ".json" if ("api" in url or url.endswith(".json")) else ".html"
        path = OUT / ((name or slug(url)) + ("" if name and "." in name else ext))
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            path.write_bytes(data)
            print("OK", len(data), path.name)
        except Exception as e:
            print("FAIL", url, e)


if __name__ == "__main__":
    main()
