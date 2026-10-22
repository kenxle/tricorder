"""Write an INDEX.md in every folder under raw/, listing its files as links.

A link to a folder cannot open as a page in a browser, so the research files
link to these indexes instead. Where a saved page exists as both .txt and
.html, the index links the .txt (the readable copy) and names the .html beside
it, which keeps each index under the number of links one page can carry.

Run from anywhere: python3 raw_index.py
"""

from pathlib import Path

RAW = Path(__file__).resolve().parent / "raw"


def write_index(folder: Path) -> int:
    files = sorted(p for p in folder.iterdir() if p.is_file() and p.name != "INDEX.md")
    subdirs = sorted(p for p in folder.iterdir() if p.is_dir())
    stems_with_txt = {p.stem for p in files if p.suffix == ".txt"}
    lines = [f"# Saved pages: {folder.relative_to(RAW.parent)}", ""]
    lines.append("Written by raw_index.py. Each line is one saved file.")
    lines.append("")
    if subdirs:
        lines.append("## Folders")
        lines.append("")
        for d in subdirs:
            lines.append(f"- [{d.name}/]({d.name}/INDEX.md)")
        lines.append("")
    lines.append("## Files")
    lines.append("")
    links = 0
    for f in files:
        if f.suffix == ".html" and f.stem in stems_with_txt:
            continue
        twin = f.with_suffix(".html")
        note = f" (also saved as `{twin.name}`)" if f.suffix == ".txt" and twin.exists() else ""
        lines.append(f"- [{f.name}]({f.name}){note}")
        links += 1
    (folder / "INDEX.md").write_text("\n".join(lines) + "\n")
    for d in subdirs:
        write_index(d)
    return links


if __name__ == "__main__":
    for top in sorted(p for p in RAW.iterdir() if p.is_dir()):
        n = write_index(top)
        print(f"{top.name}: {n} file links in INDEX.md")
