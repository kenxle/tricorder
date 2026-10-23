"""The static PDF: the same sections in the same order, every claim footnoted.

Each line that cites claims carries note numbers. The notes print at the end
of each section: the claim id, then each source's file, locator, quoted text
and the date it was read. Gap lines, operator lines and the operator's blanks
are marked as such. The "could not verify" box prints at the end of section 14.

Made with reportlab (see 04_architecture.md, "The PDF", for why and the
alternatives). It is imported only when a PDF is written.
"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from memo.model import Memo, MemoLine

TAGS = {"gap": "Gap", "operator": "Operator", "slot": "Operator writes", "reading": "Reading",
        "unverified": "Could not verify", "ask": "Ask", "coverage": "Checklist", "pieces": "Pieces"}
FOOTNOTED = {"claim", "reading", "pieces", "operator", "ask"}


def _line_html(line: MemoLine, notes: list[int]) -> str:
    tag = TAGS.get(line.kind)
    if line.kind == "operator":
        tag = f"Operator ({line.author}, version {line.version})"
    parts = []
    if tag:
        parts.append(f'<font size="7" color="#5d6470">{escape(tag.upper())}</font>&nbsp;&nbsp;')
    if line.label:
        parts.append(f"<b>{escape(line.label)}.</b> ")
    parts.append(escape(line.text))
    if line.kind == "operator" and line.unsourced_numbers:
        parts.append(f' <font color="#8a5a00">[operator\'s figure, no source: {escape(", ".join(line.unsourced_numbers))}]</font>')
    if notes:
        parts.append("<super>" + ",".join(str(n) for n in notes) + "</super>")
    return "".join(parts)


def render_pdf(memo: Memo, path: str | Path) -> Path:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

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
             Paragraph(escape(f"Shared version {memo.version}. Drafted {memo.built_at[:16].replace('T', ' ')} UTC from the readout built "
                              f"{memo.readout_built_at}. Every claim is footnoted to its file, locator and quoted text."), who)]
    if memo.synthetic_notice:
        story.append(Paragraph(escape(memo.synthetic_notice), banner))
    n = 0
    for sec in memo.sections:
        story.append(Paragraph(escape(f"{sec.number}. {sec.title}"), h2))
        story.append(Paragraph(escape(f"Who writes it: {sec.who_writes}"), who))
        sec_notes: list[tuple[int, str]] = []
        for ln in sec.lines:
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
                c = memo.claims[cid]
                srcs = "; ".join(f"{s.uri}, {s.locator}: \"{s.quote}\"" + (f" (read {s.retrieved_at})" if s.retrieved_at else "")
                                 for s in c.sources)
                story.append(Paragraph(escape(f"[{num}] {cid}. {c.confidence}, {c.check.name}. {srcs}"), note))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#5d6470"))
        text = f"{memo.company} memo, shared version {memo.version}."
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
