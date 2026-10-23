"""FR-R10: no route or command of founder requests opens a network connection (review O9).

Every Python process started here, including the scans the intake reruns, loads a
sitecustomize that records and refuses any internet socket connect."""

from __future__ import annotations

import base64
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PLAN = Path(__file__).parent / "fixtures" / "synthetic_brasswick_hiring_plan.csv"

BLOCKER = '''
import os, socket
_real = socket.socket.connect
def _no_network(self, address, *a, **k):
    if self.family in (socket.AF_INET, socket.AF_INET6):
        with open(os.environ["TRICORDER_NET_LOG"], "a") as fh:
            fh.write(f"{os.getpid()} {address!r}\\n")
        raise OSError("network blocked by test_no_network")
    return _real(self, address, *a, **k)
socket.socket.connect = _no_network
socket.socket.connect_ex = lambda self, address: _no_network(self, address)
'''


@pytest.fixture
def netless(tmp_path, monkeypatch):
    site = tmp_path / "site"
    site.mkdir()
    (site / "sitecustomize.py").write_text(BLOCKER)
    log = tmp_path / "net.log"
    env = {"PYTHONPATH": os.pathsep.join([str(site), str(ROOT), os.environ.get("PYTHONPATH", "")]),
           "TRICORDER_NET_LOG": str(log), "TRICORDER_ROOMS_DIR": str(tmp_path / "rooms"),
           "TRICORDER_OUT_DIR": str(tmp_path / "out"), "TRICORDER_OFFLINE": "1"}
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    return log


def _run(*args):
    proc = subprocess.run([sys.executable, *args], cwd=ROOT, env=os.environ.copy(), capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    return proc


def test_every_command_stays_off_the_network(netless):
    _run("-c", "import socket, sitecustomize; assert socket.socket.connect.__name__ == '_no_network'")
    for mod in ("scans.redflags", "scans.claims", "scans.memo"):
        if (ROOT / "scans" / mod.split(".")[1]).is_dir():
            _run("-m", mod, "data_room/brasswick")
    _run("-m", "founder_requests", "list", "data_room/brasswick")
    _run("-m", "founder_requests", "draft", "data_room/brasswick", "--all", "--to", "celia@example.com")
    _run("-m", "founder_requests", "copy-room", "data_room/brasswick")
    _run("-m", "founder_requests", "add", "data_room/brasswick", str(PLAN), "--for", "C22", "--copy")
    assert not netless.exists(), netless.read_text()


def test_every_route_stays_off_the_network(netless, monkeypatch):
    import socket

    from fastapi.testclient import TestClient

    from founder_requests.tests.conftest import build
    from server.app import app

    calls = []
    real = socket.socket.connect

    def refuse(self, address, *a, **k):
        if self.family in (socket.AF_INET, socket.AF_INET6):
            calls.append(address)
            raise OSError("network blocked")
        return real(self, address, *a, **k)

    monkeypatch.setattr(socket.socket, "connect", refuse)
    client = TestClient(app, base_url="http://127.0.0.1")
    build(ROOT / "data_room" / "brasswick", Path(os.environ["TRICORDER_OUT_DIR"]))
    base = "/api/rooms/brasswick/founder-requests"
    assert client.get(base).status_code == 200
    assert client.post(f"{base}/draft", json={"to": "celia@example.com"}).status_code == 200
    assert client.post(f"{base}/copy", json={}).status_code == 200
    files = [{"name": "plan.csv", "answers": "C22", "data": base64.b64encode(PLAN.read_bytes()).decode()}]
    assert client.post("/api/rooms/brasswick_live/founder-requests/batch", json={"files": files}).status_code == 200
    assert client.get("/api/rooms/brasswick_live/founder-requests/received").status_code == 200
    assert calls == [] and not netless.exists()
