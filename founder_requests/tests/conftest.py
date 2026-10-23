"""Shared fixtures: a readout built by the real commands into a temporary out folder."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from schema.claim import Readout

ROOT = Path(__file__).resolve().parents[2]


def build(room_dir: Path, out: Path) -> Readout:
    """python -m scans.redflags <room>, then python -m scans.memo <room>, with TRICORDER_OUT_DIR=out."""
    env = os.environ | {"TRICORDER_OUT_DIR": str(out), "TRICORDER_OFFLINE": "1"}
    for cmd in (["scans.redflags"], ["scans.memo"]):
        subprocess.run([sys.executable, "-m", *cmd, str(room_dir)], cwd=ROOT, env=env, check=True, capture_output=True)
    return Readout.model_validate_json((out / room_dir.name / "readout.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def brasswick(tmp_path_factory) -> Readout:
    return build(ROOT / "data_room" / "brasswick", tmp_path_factory.mktemp("out_brasswick"))


@pytest.fixture(scope="session")
def hollis(tmp_path_factory) -> Readout:
    return build(ROOT / "data_room" / "hollis_voice", tmp_path_factory.mktemp("out_hollis"))
