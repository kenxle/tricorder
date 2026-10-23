"""Test contracts and test rooms for contract_terms_full, built in pytest's tmp_path.

The contracts are written as plain text PDFs by `write_pdf`, a small writer
with no dependency, so these tests run on any machine that runs the suite
(reportlab and pypdf are not in the root requirements). Every test contract is
made up for the test and says so on each page. The rooms in data_room/ are
never written: a test room is a copy.
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HOLLIS = ROOT / "data_room" / "hollis_voice"
TEST_NOTE = "Test contract made by the Tricorder test suite. Not a real company."


def _pdf_text(s: str) -> str:
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def write_pdf(path: Path, pages: list[list[str]]) -> Path:
    """A PDF with one page per list, one line of 10pt Helvetica per string."""
    objs: list[bytes] = []
    kids = []
    n_pages = len(pages)
    # Object numbers: 1 catalog, 2 pages, 3 font, then (page, content) pairs.
    for i, lines in enumerate(pages):
        page_no, content_no = 4 + 2 * i, 5 + 2 * i
        kids.append(f"{page_no} 0 R")
        body = ["BT", "/F1 10 Tf", "12 TL", "50 760 Td"]
        for line in lines + ["", f"{TEST_NOTE} Page {i + 1}"]:
            body.append(f"({_pdf_text(line)}) Tj T*")
        body.append("ET")
        stream = "\n".join(body).encode("latin-1")
        objs.append((page_no, f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                              f"/Resources << /Font << /F1 3 0 R >> >> /Contents {content_no} 0 R >>".encode()))
        objs.append((content_no, b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream"))
    head = [(1, b"<< /Type /Catalog /Pages 2 0 R >>"),
            (2, f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {n_pages} >>".encode()),
            (3, b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")]
    allobjs = sorted(head + objs)
    out = bytearray(b"%PDF-1.4\n")
    offsets = {}
    for num, data in allobjs:
        offsets[num] = len(out)
        out += f"{num} 0 obj\n".encode() + data + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(allobjs) + 1}\n0000000000 65535 f \n".encode()
    for num, _ in allobjs:
        out += f"{offsets[num]:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(allobjs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(bytes(out))
    return path


def order_form(customer: str, *, term_line: str, termination: list[str], extra: list[str] = (),
               provider: str = "Hollis Voice, Inc.", effective: str = "2026-06-01") -> list[list[str]]:
    """The page text of a test order form shaped like the room's own."""
    return [
        [f"Order Form: {customer}",
         f"Between {provider} (the Provider) and {customer} (the Customer). Effective date:",
         f"{effective}.",
         "Item Detail",
         "Plan Standard, 1 location",
         term_line,
         "Monthly fee $649 a month, invoiced monthly."],
        ["Terms",
         "1. Services. The Provider answers the Customer's phone line and books appointments.",
         *termination,
         *extra,
         "Signed for the Provider: Test Signer, Chief Executive Officer",
         "Signed for the Customer: Test Customer, Practice Owner"],
    ]


THIRTY_DAY = ["2. Termination. Either party may end this order form at any time, for any reason, by giving",
              "30 days written notice."]
ONE_YEAR = ["2. Termination. Either party may end this order form for a material breach that is not fixed within",
            "30 days of written notice. The Customer has no other right to end the order form during the term."]
CHANGE_OF_CONTROL = ["3. Change of control. If the Customer is acquired by another company, either party may end this",
                     "order form on 30 days written notice after the change of control."]


def copy_room(tmp_path: Path, name: str = "hollis_voice", src: Path = HOLLIS) -> Path:
    """A copy of a room without its video, which the contract checks never read."""
    dst = tmp_path / name
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("*.mp4", "*.mov"))
    return dst


def a_counted_customer(room: Path, month: str = "2026-09") -> tuple[str, float]:
    """A subscription customer with MRR in the month, and no contract in the room."""
    import csv

    with open(room / "03_metrics" / "customer_mrr_by_month.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["month"] == month and r["product_type"] == "Subscription" and float(r["mrr"]) > 0 \
                    and r["customer_name"] not in ("Cedar & Pine Animal Hospitals", "Brookline Row Veterinary"):
                return r["customer_name"], float(r["mrr"])
    raise AssertionError("no counted customer")
