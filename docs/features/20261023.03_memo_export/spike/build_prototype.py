"""Build the two prototype pages from the real Hollis Voice readout.

    TRICORDER_OUT_DIR=<scratch> python3 -m scans.redflags data_room/hollis_voice
    TRICORDER_OUT_DIR=<scratch> python3 -m scans.memo data_room/hollis_voice
    TRICORDER_OUT_DIR=<scratch> python3 docs/features/20261023.03_memo_export/spike/build_prototype.py

prototype_real.html: the readout as main builds it today (one scan, no pieces, no top flags).
prototype_simulated.html: the same readout with pieces, top flags and links added by hand
from its real claim ids (memo/tests/conftest.py, with_pieces). The banner says so.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from memo.build import build_memo  # noqa: E402
from memo.edit import apply_edits  # noqa: E402
from memo.export import load_readout  # noqa: E402
from memo.html import render_html  # noqa: E402
from memo.model import Edit  # noqa: E402
from memo.pdf import render_pdf  # noqa: E402
from memo.tests.conftest import with_pieces  # noqa: E402

ROOM = ROOT / "data_room" / "hollis_voice"
OUT = Path(__file__).resolve().parent.parent / "02_prototype"
AT = "2026-10-23T12:00:00Z"

readout = load_readout(ROOM)
real = build_memo(readout, ROOM, AT)
OUT.joinpath("prototype_real.html").write_text(render_html(real), encoding="utf-8")

sim_readout = with_pieces(readout)
sim_readout.synthetic_notice = (readout.synthetic_notice or "") + " Prototype: the pieces, top flags and links are simulated by hand from real claim ids."
sim = build_memo(sim_readout, ROOM, AT)
sim = apply_edits(sim, [
    Edit(action="replace", line_id="s02-recommendation", text="Recommendation: wait for the bank statements and the Marlow pilot terms before a term sheet."),
    Edit(action="add", section=9, text="Simulated operator line: I met both founders on 2026-10-20; they have worked together for 6 years."),
], "Prototype operator", AT)
OUT.joinpath("prototype_simulated.html").write_text(render_html(sim), encoding="utf-8")
render_pdf(sim, OUT / "prototype_simulated.pdf")
print("wrote", *(p.name for p in sorted(OUT.iterdir())))
