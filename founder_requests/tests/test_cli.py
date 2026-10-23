"""The command a user runs: python -m founder_requests ..."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PLAN = Path(__file__).parent / "fixtures" / "synthetic_brasswick_hiring_plan.csv"


@pytest.fixture
def env(tmp_path):
    return os.environ | {"TRICORDER_ROOMS_DIR": str(tmp_path / "rooms"), "TRICORDER_OUT_DIR": str(tmp_path / "out"),
                         "TRICORDER_OFFLINE": "1"}


def run(env, *args, ok=True):
    proc = subprocess.run([sys.executable, "-m", "founder_requests", *args], cwd=ROOT, env=env, capture_output=True, text=True)
    if ok:
        assert proc.returncode == 0, proc.stderr
    return proc


def test_draft_needs_a_readout_first(env):
    proc = run(env, "draft", "data_room/brasswick", ok=False)
    assert proc.returncode == 2 and "python -m scans.memo data_room/brasswick" in proc.stderr


def test_list_and_draft_on_brasswick(env):
    for mod in ("scans.redflags", "scans.memo"):
        subprocess.run([sys.executable, "-m", mod, "data_room/brasswick"], cwd=ROOT, env=env, check=True, capture_output=True)
    listing = run(env, "list", "data_room/brasswick").stdout
    assert "Top 1" in listing and "Hiring plan" in listing
    out = run(env, "draft", "data_room/brasswick", "--to", "celia@example.com", "--sender", "Sam").stdout
    assert out.startswith("Subject: Brasswick: documents for our review\n")
    assert "Hi Celia," in out and "mailto:celia@example.com?subject=" in out
    data = json.loads(run(env, "draft", "data_room/brasswick", "--lines", "6", "--json").stdout)
    assert data["subject"] == "Brasswick: one document for our review" and data["leaks"] == []
    bad = run(env, "draft", "data_room/brasswick", "--lines", "999", ok=False)
    assert bad.returncode == 2 and "no ask line 999" in bad.stderr


def test_add_refuses_a_synthetic_room_then_copies_with_flag(env, tmp_path):
    proc = run(env, "add", "data_room/brasswick", str(PLAN), "--for", "C22", ok=False)
    assert proc.returncode == 1 and "copy-room data_room/brasswick" in proc.stderr
    receipt = json.loads(run(env, "add", "data_room/brasswick", str(PLAN), "--for", "C22", "--copy").stdout)
    assert receipt["room"] == "brasswick_live" and receipt["saved"] == "05_team/hiring_plan.csv"
    assert receipt["status_after"] == "found" and receipt["scans_rerun"][0]["scan"] == "redflags"
    assert (tmp_path / "rooms" / "brasswick_live" / "05_team" / "hiring_plan.csv").read_bytes() == PLAN.read_bytes()
    # A second hiring plan goes beside the first and says the scans still read the first.
    second = json.loads(run(env, "add", "data_room/brasswick", str(PLAN), "--for", "C22", "--copy").stdout)
    assert second["saved"].startswith("05_team/hiring_plan_from_founder_") and "still read" in second["note"]
    third = run(env, "add", "data_room/brasswick", str(PLAN), "--for", "C22", "--copy", ok=False)
    assert third.returncode == 1 and "already in the room" in third.stderr


def test_copy_room_command(env, tmp_path):
    out = run(env, "copy-room", "data_room/brasswick", "--as", "brasswick_demo").stdout
    assert "brasswick_demo" in out and (tmp_path / "rooms" / "brasswick_demo" / "05_team").is_dir()
