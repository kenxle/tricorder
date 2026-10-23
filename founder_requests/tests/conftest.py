"""Shared fixtures: a readout built by the real commands into a temporary out folder."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from schema.claim import Readout

ROOT = Path(__file__).resolve().parents[2]


def ready_scans(room_dir: Path) -> list[str]:
    """Every built scan whose NEEDS the room meets: what a first run or a new input file reruns.
    Derived, so a new scan never breaks a test that names what reran."""
    from founder_requests import intake as ik
    from scans.base import available, missing_needs
    return [n for n in available() if not missing_needs(room_dir, ik._needs(n))]


def build(room_dir: Path, out: Path) -> Readout:
    """Every ready scan, then python -m scans.memo <room>, with TRICORDER_OUT_DIR=out and offline."""
    env = os.environ | {"TRICORDER_OUT_DIR": str(out), "TRICORDER_OFFLINE": "1"}
    for name in ready_scans(room_dir) + ["memo"]:
        subprocess.run([sys.executable, "-m", f"scans.{name}", str(room_dir)], cwd=ROOT, env=env, check=True, capture_output=True)
    return Readout.model_validate_json((out / room_dir.name / "readout.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def brasswick(tmp_path_factory) -> Readout:
    return build(ROOT / "data_room" / "brasswick", tmp_path_factory.mktemp("out_brasswick"))


@pytest.fixture(scope="session")
def hollis(tmp_path_factory) -> Readout:
    return build(ROOT / "data_room" / "hollis_voice", tmp_path_factory.mktemp("out_hollis"))
