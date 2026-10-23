"""The static PDF, for the partners: the partner view of the memo, every claim footnoted.

It prints what the page's partner view shows, minus the lines that belong to
the page only (the ask list, which goes to the founder, not the partners).
No check names, claim ids, checklist numbers, operator blanks or commands.
Sections with nothing to say for a partner are left out. The recommendation,
when the operator has written one in section 15, opens section 2.

Each line that cites claims carries note numbers. The notes print at the end
of each section: each source's file and locator, what it reads as (a CSV row
with its column names, a cell with its line and column, numbers formatted as
the claims state them), and the date it was read.

Made with reportlab (see 04_architecture.md, "The PDF", for why and the
alternatives). It is imported only when a PDF is written.
"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from memo.html import recommendation, visible
from memo.model import Memo, MemoLine, source_key

FOOTNOTED = {"claim", "reading", "pieces", "operator"}
HEAD_LABELS = ("To", "Date", "Re", "Version")


def pdf_sections(memo: Memo) -> list[tuple[int, str, list[MemoLine]]]:
    """The sections and lines the PDF prints, in order."""
    rec = recommendation(memo)
    out = []
    for s in memo.sections:
        lines = visible(s, "pdf")
        if s.number == 2 and rec:
            lines = [rec] + lines
        if lines:
            out.append((s.number, s.title, lines))
    return out


def note_text(memo: Memo, claim_id: str) -> str:
    """One note: each source's file, locator and reading, and the date it was read."""
    c = memo.claims[claim_id]
    parts = []
    for s in c.sources:
        st = memo.sources.get(source_key(s.uri, s.locator))
        reads = st.reads_as if st and st.reads_as else f"\"{s.quote}\""
        part = f"{Path(s.uri).name}, {s.locator}: {reads}"
        if s.retrieved_at:
            part += f". Read {s.retrieved_at}"
        parts.append(part)
    return "; ".join(parts) + "."


def _line_html(line: MemoLine, notes: list[int]) -> str:
    parts = []
    if line.label:
        parts.append(f"<b>{escape(line.label)}.</b> ")
    parts.append(escape(line.text))
    if line.kind == "operator":
        parts.append(f' <font size="7.5" color="#5d6470">({escape(line.author or "")}, version {line.version})</font>')
        if line.unsourced_numbers:
            parts.append(f' <font color="#8a5a00">[{escape(line.author or "the operator")}\'s figure, no source: '
                         f'{escape(", ".join(line.unsourced_numbers))}]</font>')
    if notes:
        parts.append("<super>" + ",".join(str(n) for n in notes) + "</super>")
    return "".join(parts)


def render_pdf(memo: Memo, path: str | Path) -> Path:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import Paragraph, SimpleDocTemplate

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["BodyText"], fontName="Helvetica", fontSize=9.5, leading=13, alignment=TA_LEFT, spaceAfter=4)
    title = ParagraphStyle("title", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=17, leading=21, alignment=TA_LEFT)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=12.5, leading=16, spaceBefore=12, spaceAfter=2)
    who = ParagraphStyle("who", parent=body, fontSize=8, textColor=colors.HexColor("#5d6470"))
    note = ParagraphStyle("note", parent=body, fontSize=7.5, leading=10, leftIndent=10, textColor=colors.HexColor("#333333"))
    notes_h = ParagraphStyle("notes_h", parent=body, fontName="Helvetica-Bold", fontSize=8, spaceBefore=4)
    banner = ParagraphStyle("banner", parent=body, textColor=colors.HexColor("#8a5a00"))

    story = [Paragraph(escape(f"{memo.company}: memo for the partners' meeting"), title),
             Paragraph(escape("Every claim is footnoted to the file it came from."), who)]
    if memo.synthetic_notice:
        story.append(Paragraph(escape(memo.synthetic_notice), banner))
    n = 0
    for number, sec_title, lines in pdf_sections(memo):
        if number == 1:
            # The header prints as one compact line under the title, as on the page.
            head = [ln for ln in lines if ln.kind == "fact" and ln.label in HEAD_LABELS]
            story.insert(2, Paragraph(escape("   ".join(f"{ln.label}: {ln.text}" for ln in head)), who))
            lines = [ln for ln in lines if ln not in head and not (ln.kind == "fact" and ln.label == "Synthetic")]
            if not lines:
                continue
        story.append(Paragraph(escape(f"{number}. {sec_title}"), h2))
        sec_notes: list[tuple[int, str]] = []
        for ln in lines:
            nums = []
            if ln.kind in FOOTNOTED:
                for cid in ln.claim_ids:
                    if cid in memo.claims:
                        n += 1
                        nums.append(n)
                        sec_notes.append((n, cid))
            story.append(Paragraph(_line_html(ln, nums), body))
        if sec_notes:
            story.append(Paragraph("Notes", notes_h))
            for num, cid in sec_notes:
                story.append(Paragraph(escape(f"[{num}] {note_text(memo, cid)}"), note))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#5d6470"))
        text = f"{memo.company} memo, version {memo.version}."
        if memo.synthetic_notice:
            text += f" {memo.synthetic_notice}"
        canvas.drawString(0.75 * inch, 0.5 * inch, text)
        canvas.drawRightString(LETTER[0] - 0.75 * inch, 0.5 * inch, f"Page {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(str(path), pagesize=LETTER, leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                            topMargin=0.75 * inch, bottomMargin=0.75 * inch,
                            title=f"{memo.company} memo, version {memo.version}", author="Tricorder")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return path
