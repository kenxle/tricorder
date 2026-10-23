"""Build 02_prototype/prototype.html from the real Brasswick readout and the real draft module.

    TRICORDER_OUT_DIR=<scratch> python3 -m scans.redflags data_room/brasswick
    TRICORDER_OUT_DIR=<scratch> python3 -m scans.memo data_room/brasswick
    TRICORDER_OUT_DIR=<scratch> python3 docs/features/20261023.02_founder_requests/spike/build_prototype.py

Every ask line, founder sentence and guidance block in the page comes from
founder_requests.draft run on that readout. The upload and rerun are simulated
in the page and labelled so.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT))

from schema.claim import Readout  # noqa: E402
from scans.base import out_dir  # noqa: E402
from founder_requests import draft as d  # noqa: E402

room = ROOT / "data_room" / "brasswick"
readout = Readout.model_validate_json((out_dir(room) / "readout.json").read_text(encoding="utf-8"))
all_items = d.items(readout)
company, first, read_from = d.company_and_greeting(room, readout.room)
data = {
    "room": readout.room, "company": company, "first": first, "read_from": read_from,
    "notice": readout.synthetic_notice, "built_at": readout.built_at,
    "items": [asdict(i) for i in all_items], "default": d.default_selection(all_items),
    "mailto_max": d.MAILTO_MAX,
    "sample_draft": asdict(d.draft(readout, room_dir=room)),
}
template = (HERE / "prototype_template.html").read_text(encoding="utf-8")
target = HERE.parent / "02_prototype" / "prototype.html"
target.write_text(template.replace("/*DATA*/null", json.dumps(data, indent=1)), encoding="utf-8")
print(f"{target.relative_to(ROOT)}: {len(all_items)} ask lines, default {data['default']}")
