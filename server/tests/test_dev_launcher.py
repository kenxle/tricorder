"""The dev task runs from the repo root with an explicit interpreter and reload scope."""

import os
from pathlib import Path
import shutil
import subprocess

import pytest

from scans.base import ROOT


@pytest.mark.parametrize("selection", ["override", "venv", "fallback"])
@pytest.mark.parametrize("reload", [True, False])
def test_dev_launcher_selects_python_and_passes_api_options(tmp_path, selection, reload):
    launcher = tmp_path / "apps" / "api" / "dev.sh"
    launcher.parent.mkdir(parents=True)
    shutil.copyfile(ROOT / "apps" / "api" / "dev.sh", launcher)
    probe = tmp_path / "probe-python"
    probe.write_text('#!/usr/bin/env bash\nprintf "%s\\n" "$PWD" "$0" "$@"\n')
    probe.chmod(0o755)
    env = {k: v for k, v in os.environ.items() if k not in ("TRICORDER_PYTHON", "PYTHON")}
    env["PORT"] = "8799"
    if selection in ("override", "venv"):
        venv_python = tmp_path / ".venv" / "bin" / "python"
        venv_python.parent.mkdir(parents=True)
        shutil.copy(probe, venv_python)
        (tmp_path / ".env").write_text("TRICORDER_OFFLINE=1\n")
        env["PYTHON"] = "/no/such/python"
    if selection == "override":
        env["TRICORDER_PYTHON"] = str(probe)
    elif selection == "fallback":
        env["PYTHON"] = str(probe)

    command = ["bash", str(launcher)] + ([] if reload else ["--no-reload"])
    result = subprocess.run(command, cwd=tmp_path.parent, env=env,
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    cwd, interpreter, *args = result.stdout.splitlines()
    assert Path(cwd).resolve() == tmp_path.resolve()
    expected = tmp_path / ".venv" / "bin" / "python" if selection == "venv" else probe
    assert Path(interpreter).resolve() == expected.resolve()
    assert args[:3] == ["-m", "uvicorn", "server.app:app"]
    assert args[args.index("--port") + 1] == "8799"
    assert ("--reload" in args) == reload
    assert ("--reload-dir" in args) == reload
    if reload:
        assert "server" in args and "scans" in args
    assert ("--env-file" in args) == (selection != "fallback")
