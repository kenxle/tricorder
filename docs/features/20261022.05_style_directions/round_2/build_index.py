"""Write round_2/index.html: one card per round-two direction, from each notes.md and its screenshots.

Run: python3 round_2/build_index.py
"""
import html
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
cards = []
for d in sorted(HERE.glob("direction_*")):
    notes = (d / "notes.md").read_text(encoding="utf-8").splitlines()
    title = notes[0].lstrip("# ").strip()
    idea = next((l for l in notes if "idea" in l.lower()), "")
    idea = re.sub(r"\*\*[^*]+\*\*:?\s*", "", idea.lstrip("- ")).strip()
    name = d.name
    shots = "".join(
        f'<a href="{name}/screens/{s}"><img src="{name}/screens/{s}" alt="{html.escape(title)}, {s[:-4].replace("-", " ")}"></a>'
        for s in ("home-desktop-light.png", "home-desktop-dark.png") if (d / "screens" / s).exists())
    cards.append(f"""<section class="card"><h2>{html.escape(title)}</h2><p>{html.escape(idea)}</p>
<p class="links"><a href="{name}/home.html">Home page</a> · <a href="{name}/style_guide.html">Style guide</a> · <a href="{name}/notes.md">Designer's notes</a></p>
<div class="shots">{shots}</div></section>""")
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Style directions, round two</title>
<style>
:root{{--bg:#f6f5f2;--ink:#1a1a1a;--muted:#5b5b5b;--line:#d9d6cf;--card:#fff;--link:#1d4e89}}
@media (prefers-color-scheme:dark){{:root{{--bg:#141414;--ink:#ece9e3;--muted:#a8a49c;--line:#34322e;--card:#1c1b19;--link:#8db7ea}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,sans-serif}}
main{{max-width:1200px;margin:0 auto;padding:32px 16px}}
h1{{font-size:28px;margin:0 0 8px}} .lede{{color:var(--muted);margin:0 0 24px;max-width:70ch}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:20px;margin:0 0 24px}}
.card h2{{margin:0 0 6px;font-size:22px}} .card p{{margin:0 0 10px;max-width:80ch}}
a{{color:var(--link)}} .links{{font-weight:600}}
.shots{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px}}
.shots img{{width:100%;border:1px solid var(--line);border-radius:6px;display:block}}
</style></head><body><main>
<h1>Style directions, round two</h1>
<p class="lede">Pick one, or name what to take from each. Round one (A, B, C) was rejected as not professional enough; these three were built to the <a href="BRIEF_ROUND_2.md">round-two brief</a>. Each card links the full home page and style guide. Comment anywhere on this page.</p>
{''.join(cards)}
</main></body></html>
"""
(HERE / "index.html").write_text(page, encoding="utf-8")
print(len(cards), "directions")
