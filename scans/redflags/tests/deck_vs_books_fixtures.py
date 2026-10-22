"""Test rooms for deck_vs_books, built in pytest's tmp_path.

A test room is a copy of the Hollis Voice files the check reads, with one
change: a different deck, or a file left out. The room in data_room/ is never
written. The test decks replace slide 3 with a chart drawn from the room's own
P&L, so they agree with the books everywhere except the thing under test.

Drawing a chart needs matplotlib, reportlab and pypdf. They are in
data_room/requirements.txt, not in the root requirements.txt, so a test that
needs a test deck calls `need_deck_tools()` and skips when one is missing.
"""

from __future__ import annotations

import io
import shutil
from pathlib import Path

import pytest

from schema.readers import pdf_page, xlsx_sheet

ROOT = Path(__file__).resolve().parents[3]
DATA_ROOM = ROOT / "data_room"
HOLLIS = DATA_ROOM / "hollis_voice"
DECK = "01_overview/pitch_deck.pdf"
MODEL = "02_financials/financial_model.xlsx"
COPIED = (DECK, "01_overview/claims.json", MODEL, "03_metrics/monthly_metrics.csv",
          "03_metrics/customer_mrr_by_month.csv", "03_metrics/revenue_by_customer.csv")
BRASSWICK = DATA_ROOM / "brasswick"
SLIDE = 3
TEAL = "#1B998B"
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def need_deck_tools():
    for name in ("matplotlib", "reportlab", "pypdf"):
        pytest.importorskip(name, reason=f"{name} draws the test decks (data_room/requirements.txt)")


def copy_room(tmp_path: Path, leave_out: tuple[str, ...] = (), src: Path = HOLLIS) -> Path:
    room = tmp_path / src.name
    for rel in COPIED:
        if rel in leave_out or not (src / rel).exists():
            continue
        (room / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src / rel, room / rel)
    return room


def recurring_books(room: Path) -> list[tuple[str, float]]:
    rows = xlsx_sheet(room / MODEL, "P&L")
    hdr_i = next(i for i, r in enumerate(rows) if r[0] == "Line")
    hdr, kind = rows[hdr_i], rows[hdr_i + 1]
    line = next(r for r in rows if isinstance(r[0], str) and r[0].startswith("Recurring revenue"))
    return [(hdr[i], line[i]) for i in range(2, len(hdr)) if kind[i] == "Actual"]


def _label(m: str) -> str:
    y, mo = m.split("-")
    return f"{MONTHS[int(mo) - 1]} {y}"


def _chart_png(labels, values, ylabel) -> io.BytesIO:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

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


def _grey_png() -> io.BytesIO:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.axis("off")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, facecolor="#DDDDDD", metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def _slide3(size, png, caption: str, old_text: str) -> bytes:
    from reportlab.lib import colors
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas

    sw, sh = size
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(sw, sh), invariant=1)
    c.setFillColor(colors.HexColor("#14213D"))
    c.rect(0, sh - 84, sw, 84, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 30)
    c.drawString(48, sh - 54, "Where we are")
    lines = old_text.splitlines()
    for i, (big, label) in enumerate([(lines[2], lines[3]), (lines[4], lines[5]), (lines[6], lines[7])]):
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


def _write_deck(room: Path, page_pdf: bytes | None, drop_last: bool = False):
    from pypdf import PdfReader, PdfWriter

    src = PdfReader(str(HOLLIS / DECK))
    new = PdfReader(io.BytesIO(page_pdf)) if page_pdf else None
    w = PdfWriter()
    pages = list(src.pages)
    if drop_last:
        pages = pages[:-1]
    for i, p in enumerate(pages, 1):
        w.add_page(new.pages[0] if (new and i == SLIDE) else p)
    (room / DECK).parent.mkdir(parents=True, exist_ok=True)
    with open(room / DECK, "wb") as f:
        w.write(f)


def make_room(tmp_path: Path, kind: str, leave_out: tuple[str, ...] = ()) -> Path:
    """A Hollis Voice test room. kind is one of:

    starts_late    the chart starts six months after the first revenue month
    quarterly      the same window, in quarters
    unreadable     the caption kept, the chart a grey box
    before_books   the chart claims three months before the books begin
    no_claims_page the real deck without slide 14
    """
    need_deck_tools()
    from pypdf import PdfReader

    room = copy_room(tmp_path, leave_out=leave_out + (DECK,))
    series = recurring_books(HOLLIS)
    first = next(i for i, (_, v) in enumerate(series) if v > 0)
    size = tuple(float(x) for x in PdfReader(str(HOLLIS / DECK)).pages[0].mediabox[2:])
    old = pdf_page(HOLLIS / DECK, SLIDE)
    ylabel = "Monthly recurring revenue ($ thousands)"

    if kind == "starts_late":
        part = series[first + 6:]
        cap = f"Monthly recurring revenue, {_label(part[0][0])} to {_label(part[-1][0])}."
        page = _slide3(size, _chart_png([m for m, _ in part], [v for _, v in part], ylabel), cap, old)
    elif kind == "quarterly":
        q: dict[str, float] = {}
        for m, v in series[first:]:
            y, mo = m.split("-")
            key = f"{y} Q{(int(mo) - 1) // 3 + 1}"
            q[key] = q.get(key, 0) + v
        cap = f"Quarterly recurring revenue, {_label(series[first][0])} to {_label(series[-1][0])}."
        page = _slide3(size, _chart_png(list(q), list(q.values()), "Recurring revenue per quarter ($ thousands)"), cap, old)
    elif kind == "unreadable":
        cap = f"Monthly recurring revenue, {_label(series[first][0])} to {_label(series[-1][0])}."
        page = _slide3(size, _grey_png(), cap, old)
    elif kind == "before_books":
        made_up = [("2024-10", 900.0), ("2024-11", 1200.0), ("2024-12", 1800.0)]
        allm = made_up + series[first:]
        cap = f"Monthly recurring revenue, {_label(allm[0][0])} to {_label(allm[-1][0])}."
        page = _slide3(size, _chart_png([m for m, _ in allm], [v for _, v in allm], ylabel), cap, old)
    elif kind == "no_claims_page":
        _write_deck(room, None, drop_last=True)
        return room
    else:
        raise ValueError(kind)
    _write_deck(room, page)
    return room


# Generic slide replacement, for any room ------------------------------------

def _deck_size(src: Path) -> tuple[float, float]:
    from pypdf import PdfReader
    return tuple(float(x) for x in PdfReader(str(src / DECK)).pages[0].mediabox[2:])


def text_slide(size, title: str, lines: list[str]) -> bytes:
    """A plain slide: a title and lines of text, nothing else."""
    from reportlab.pdfgen import canvas

    sw, sh = size
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(sw, sh), invariant=1)
    c.setFont("Helvetica-Bold", 30)
    c.drawString(48, sh - 54, title)
    c.setFont("Helvetica", 16)
    for i, line in enumerate(lines):
        c.drawString(48, sh - 120 - 28 * i, line)
    c.showPage()
    c.save()
    return buf.getvalue()


def chart_slide(size, title: str, months: list[str], values: list[float], caption: str) -> bytes:
    """A slide with a bar chart of the given values and a caption under it."""
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas

    sw, sh = size
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(sw, sh), invariant=1)
    c.setFont("Helvetica-Bold", 30)
    c.drawString(48, sh - 54, title)
    c.drawImage(ImageReader(_chart_png(months, values, "Revenue ($ thousands)")), 360, 80, width=560, height=315)
    c.setFont("Helvetica", 11)
    c.drawString(360, 62, caption)
    c.showPage()
    c.save()
    return buf.getvalue()


def replace_slides(tmp_path: Path, src: Path, slides: dict[int, bytes]) -> Path:
    """A copy of a room whose deck has some slides replaced."""
    need_deck_tools()
    from pypdf import PdfReader, PdfWriter

    room = copy_room(tmp_path, leave_out=(DECK,), src=src)
    old = PdfReader(str(src / DECK))
    w = PdfWriter()
    for i, p in enumerate(old.pages, 1):
        w.add_page(PdfReader(io.BytesIO(slides[i])).pages[0] if i in slides else p)
    (room / DECK).parent.mkdir(parents=True, exist_ok=True)
    with open(room / DECK, "wb") as f:
        w.write(f)
    return room


def total_revenue(src: Path) -> list[tuple[str, float]]:
    rows = xlsx_sheet(src / MODEL, "P&L")
    hdr_i = next(i for i, r in enumerate(rows) if r[0] == "Line")
    hdr, kind = rows[hdr_i], rows[hdr_i + 1]
    line = next(r for r in rows if r[0] == "Total revenue")
    return [(hdr[i], line[i]) for i in range(2, len(hdr)) if kind[i] == "Actual"]


def month_label(m: str) -> str:
    return _label(m)
