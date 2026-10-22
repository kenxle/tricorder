"""Thresholds are settings, not facts. Defaults from FRAMEWORKS.md, "Settings".

Each default there names the source it came from. A scan reads these through
`load()`, so a test or the operator can change one without touching code.
Overrides come from a JSON file named by TRICORDER_SETTINGS, if set.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

DEFAULTS: dict[str, object] = {
    "match_tolerance": 0.01,        # PF2's tolerance in data_room/answer_key.json
    "spoken_tolerance": 0.10,       # set by the team; must sit below PF2b's 20 percent gap
    "short_notice_days": 90,
    "min_contract_months": 12,
    "concentration_line": 0.20,     # share of MRR for the largest customer
    "grr_line": 80.0,               # percent points
    "load_factor_range": [1.25, 1.4],
    "runway_floor": 18,             # months
    "top_green_flags": 3,
    "top_red_flags": 5,
}


def load() -> dict[str, object]:
    settings = dict(DEFAULTS)
    path = os.environ.get("TRICORDER_SETTINGS")
    if path:
        settings.update(json.loads(Path(path).read_text(encoding="utf-8")))
    return settings
