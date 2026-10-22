#!/usr/bin/env python3
"""Make test decks from a room's real deck, without changing the room.

Each test deck is the room's pitch_deck.pdf with one slide replaced: the
revenue chart slide (slide 3 on Hollis Voice). The new chart's bars are read
from the room's own P&L ("Recurring revenue (subscription plus pilot)"), so the
test deck agrees with the books everywhere except the thing under test.

    python3 make_test_decks.py <room_dir> <out_dir>

Writes into <out_dir>:
  chart_starts_late.pdf   chart from 2025-07: six months after the first
                          revenue month in the books (2025-01)
  chart_quarterly.pdf     the same window as the real deck, in quarters
  chart_unreadable.pdf    the caption kept, the chart drawn as a flat grey box

Needs matplotlib (data_room/requirements.txt), reportlab, pypdf, openpyxl.
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import openpyxl  # noqa: E402
from pypdf import PdfReader, PdfWriter  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.utils import ImageReader  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402

SLIDE = 3
TEAL = "#1B998B"
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def books(room: Path) -> list[tuple[str, float]]:
    ws = openpyxl.load_workbook(room / "02_financials/financial_model.xlsx", data_only=True)["P&L"]
    hdr = [c.value for c in ws[4]]
    kind = [c.value for c in ws[5]]
    row = next(r for r in ws.iter_rows(min_row=6) if r[0].value == "Recurring revenue (subscription plus pilot)")
    return [(hdr[i], row[i].value) for i in range(2, len(hdr)) if kind[i] == "Actual"]


def chart_png(labels: list[str], values: list[float], ylabel: str) -> io.BytesIO:
    # Same size, dpi and colour as data_room/generate.py chart_mrr().
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    xs = list(range(len(values)))
    ax.bar(xs, [v / 1000 for v in values], color=TEAL)
    step = 3 if len(xs) > 8 else 1
    ax.set_xticks(xs[::step])
    ax.set_xticklabels(labels[::step], fontsize=8)
    ax.set_ylabel(ylabel, fontsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def grey_png() -> io.BytesIO:
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.axis("off")
    fig.patch.set_facecolor("#DDDDDD")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, facecolor="#DDDDDD", metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def slide3(size, png: io.BytesIO, caption: str, deck_text: str) -> bytes:
    """A stand-in for slide 3: the same stats and footer text, a new chart and caption."""
    sw, sh = size
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(sw, sh), invariant=1)
    c.setFillColor(colors.HexColor("#14213D"))
    c.rect(0, sh - 84, sw, 84, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 30)
    c.drawString(48, sh - 54, "Where we are")
    # Keep the real slide's stat lines, so the figures on it stay the same.
    lines = deck_text.splitlines()
    stats = [(lines[2], lines[3]), (lines[4], lines[5]), (lines[6], lines[7])]
    for i, (big, label) in enumerate(stats):
        c.setFillColor(colors.HexColor("#14213D"))
        c.setFont("Helvetica-Bold", 54 if i < 2 else 40)
        c.drawString(48, 410 - 100 * i, big)
        c.setFillColor(colors.HexColor("#555555"))
        c.setFont("Helvetica", 16)
        c.drawString(48, 410 - 100 * i - 26, label)
    c.drawImage(ImageReader(png), 360, 80, width=560, height=315)
    c.setFont("Helvetica", 11)
    c.drawString(360, 62, caption)
    c.setFont("Helvetica", 9)
    c.drawString(48, 22, lines[-1].rsplit(" Slide", 1)[0])
    c.drawRightString(sw - 48, 22, "Slide 3 of 14")
    c.showPage()
    c.save()
    return buf.getvalue()


def write_deck(room: Path, out: Path, page_pdf: bytes):
    import pdfplumber
    src = PdfReader(str(room / "01_overview/pitch_deck.pdf"))
    new = PdfReader(io.BytesIO(page_pdf))
    w = PdfWriter()
    for i, p in enumerate(src.pages, 1):
        w.add_page(new.pages[0] if i == SLIDE else p)
    with open(out, "wb") as f:
        w.write(f)
    with pdfplumber.open(str(out)) as pdf:
        assert pdf.pages[SLIDE - 1].extract_text().startswith("Where we are"), out


def label(m: str) -> str:
    y, mo = m.split("-")
    return f"{MONTHS[int(mo) - 1]} {y}"


def main(room: Path, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    series = books(room)
    first = next(i for i, (_, v) in enumerate(series) if v > 0)
    deck = room / "01_overview/pitch_deck.pdf"
    size = tuple(float(x) for x in PdfReader(str(deck)).pages[0].mediabox[2:])
    import pdfplumber
    with pdfplumber.open(str(deck)) as pdf:
        text = pdf.pages[SLIDE - 1].extract_text()

    # 1. Chart starts six months after the first revenue month.
    late = series[first + 6:]
    cap = f"Monthly recurring revenue, {label(late[0][0])} to {label(late[-1][0])}."
    png = chart_png([m for m, _ in late], [v for _, v in late], "Monthly recurring revenue ($ thousands)")
    write_deck(room, out_dir / "chart_starts_late.pdf", slide3(size, png, cap, text))
    print(f"chart_starts_late.pdf: first revenue month {series[first][0]}, chart from {late[0][0]} ({len(late)} bars)")

    # 2. Quarters where the books hold months.
    q: dict[str, float] = {}
    for m, v in series[first:]:
        y, mo = m.split("-")
        key = f"{y} Q{(int(mo) - 1) // 3 + 1}"
        q[key] = q.get(key, 0) + v
    cap = f"Quarterly recurring revenue, {label(series[first][0])} to {label(series[-1][0])}."
    png = chart_png(list(q), list(q.values()), "Recurring revenue per quarter ($ thousands)")
    write_deck(room, out_dir / "chart_quarterly.pdf", slide3(size, png, cap, text))
    print(f"chart_quarterly.pdf: {len(q)} quarterly bars")

    # 3. A chart the script cannot read.
    cap = f"Monthly recurring revenue, {label(series[first][0])} to {label(series[-1][0])}."
    write_deck(room, out_dir / "chart_unreadable.pdf", slide3(size, grey_png(), cap, text))
    print("chart_unreadable.pdf: grey box in place of the chart")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
