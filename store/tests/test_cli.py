"""python -m store, the command a person runs (STORE-R8, R13)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from scans.base import ROOT

from .conftest import ROOM


def run(args, env, stdin=""):
    return subprocess.run([sys.executable, "-m", "store", *args], cwd=ROOT, env=env, input=stdin, capture_output=True, text=True)


@pytest.fixture()
def env(tmp_path, built_out, cache_dir):
    return {**os.environ, "TRICORDER_OUT_DIR": str(built_out), "TRICORDER_STORE_DIR": str(tmp_path / "store_data"), "TRICORDER_CACHE_DIR": str(cache_dir)}


def test_save_list_get_delete_from_the_terminal(env, tmp_path, cache_dir):
    done = run(["save", str(ROOM)], env)
    assert done.returncode == 0, done.stderr
    saved = json.loads(done.stdout)
    assert saved["fund"] == "demo" and saved["company"] == "hollis_voice" and saved["version"] == 1 and saved["new"]

    again = json.loads(run(["save", str(ROOM)], env).stdout)
    assert again["version"] == 1 and again["new"] is False

    held = json.loads(run(["list", "hollis_voice"], env).stdout)
    assert [v["version"] for v in held["versions"]] == [1]
    assert "02_financials/financial_model.xlsx" in {f["path"] for f in held["files"]}
    assert held["cache"] == ["outside/hollis_voice/hn/search.json", "outside/hollis_voice/website/home.html"]

    got = json.loads(run(["get", "hollis_voice"], env).stdout)
    # The count comes from the readout the fixture built, so a new redflags check does not break this test.
    built = json.loads((Path(env["TRICORDER_OUT_DIR"]) / "hollis_voice" / "readout.json").read_text(encoding="utf-8"))
    assert got["version"]["version"] == 1 and got["readout"]["claims"] == len(built["claims"]) and got["results"] == ["redflags"]
    full = json.loads(run(["get", "hollis_voice", "--full"], env).stdout)
    assert full["readout"]["room"] == "hollis_voice" and full["results"][0]["scan"] == "redflags"

    assert json.loads(run(["companies"], env).stdout) == ["hollis_voice"]

    declined = run(["delete", "hollis_voice"], env, stdin="no\n")
    assert declined.returncode == 1 and "nothing removed" in declined.stderr.lower()
    assert (tmp_path / "store_data" / "demo" / "hollis_voice").is_dir()

    confirmed = run(["delete", "hollis_voice"], env, stdin="hollis_voice\n")
    assert confirmed.returncode == 0, confirmed.stderr
    report = json.loads(confirmed.stdout)
    assert report["left"] == [] and report["removed"]["versions"] == 1
    assert not (tmp_path / "store_data" / "demo" / "hollis_voice").exists()
    assert not (cache_dir / "outside" / "hollis_voice").exists()
    assert json.loads(run(["list", "hollis_voice"], env).stdout)["versions"] == []


def test_delete_with_yes_needs_no_answer(env):
    run(["save", str(ROOM), "--fund", "fund_b", "--company", "hv"], env)
    done = run(["delete", "hv", "--fund", "fund_b", "--yes"], env)
    assert done.returncode == 0 and json.loads(done.stdout)["left"] == []


@pytest.mark.parametrize("args", [["list", "../etc"], ["get", "Hollis"], ["delete", "a/b", "--yes"], ["list", "hv", "--fund", ".."], ["save", str(ROOM), "--company", "../x"]])
def test_a_bad_id_exits_2(env, args):
    done = run(args, env)
    assert done.returncode == 2 and "id" in done.stderr


def test_save_with_no_readout_says_how_to_build_one(env, tmp_path):
    done = run(["save", str(ROOM)], {**env, "TRICORDER_OUT_DIR": str(tmp_path / "empty_out")})
    assert done.returncode == 1 and "python -m scans.memo" in done.stderr


def test_get_of_nothing_held_exits_1(env):
    done = run(["get", "nobody"], env)
    assert done.returncode == 1 and "nothing held" in done.stderr
