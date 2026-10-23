"""Shared fixtures: one real Hollis Voice readout, built once per test session
into a temporary out folder, the same way a person builds it:

    python -m scans.redflags data_room/hollis_voice
    python -m scans.memo data_room/hollis_voice
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from scans.base import ROOT

ROOM = ROOT / "data_room" / "hollis_voice"


@pytest.fixture(scope="session")
def built_out(tmp_path_factory) -> Path:
    """TRICORDER_OUT_DIR holding hollis_voice/redflags.json and readout.json."""
    out = tmp_path_factory.mktemp("out")
    env = {**__import__("os").environ, "TRICORDER_OUT_DIR": str(out)}
    for module in ("scans.redflags", "scans.memo"):
        subprocess.run([sys.executable, "-m", module, str(ROOM)], cwd=ROOT, env=env, check=True, capture_output=True)
    return out


@pytest.fixture()
def out_env(built_out, monkeypatch) -> Path:
    monkeypatch.setenv("TRICORDER_OUT_DIR", str(built_out))
    return built_out


@pytest.fixture()
def cache_dir(tmp_path) -> Path:
    """A scratch cache/ with one outside pull for hollis_voice, one for another
    company and one shared signals page. Simulated: the room is synthetic."""
    cache = tmp_path / "cache"
    for rel, text in {
        "outside/hollis_voice/website/home.html": "<p>Hollis Voice answers the phone for vet clinics.</p>",
        "outside/hollis_voice/hn/search.json": '{"hits": []}',
        "outside/other_co/website/home.html": "<p>Another company.</p>",
        "signals/competitor_pricing.html": "<p>Shared competitor page.</p>",
    }.items():
        (cache / rel).parent.mkdir(parents=True, exist_ok=True)
        (cache / rel).write_text(text, encoding="utf-8")
    (cache / "index.json").write_text(json.dumps({
        "https://hollisvoice.example.com/": {"file": "outside/hollis_voice/website/home.html", "read_at": "2026-10-23"},
        "GET hn.algolia.com/api/v1/search?query=Hollis+Voice": "outside/hollis_voice/hn/search.json",
        "https://other.example.com/": {"file": "outside/other_co/website/home.html", "read_at": "2026-10-23"},
        "https://competitor.example.com/pricing": {"file": "signals/competitor_pricing.html", "read_at": "2026-10-23"},
    }, indent=2), encoding="utf-8")
    return cache
