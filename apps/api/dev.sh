#!/usr/bin/env bash
# Run the existing Python API as a Turbo workspace task.
set -euo pipefail
cd "$(dirname "$0")/../.."

# Prefer this checkout's virtualenv over an unrelated shell's PYTHON setting.
if [ -n "${TRICORDER_PYTHON:-}" ]; then
  PY="$TRICORDER_PYTHON"
elif [ -x .venv/bin/python ]; then
  PY=.venv/bin/python
else
  PY="${PYTHON:-python3}"
fi

ARGS=(--host 127.0.0.1 --port "${PORT:-8787}")
if [ "${1:-}" != "--no-reload" ]; then
  ARGS+=(--reload)
  for dir in clients eval founder_requests memo scans schema server steering store; do
    ARGS+=(--reload-dir "$dir")
  done
fi
if [ -f .env ]; then ARGS+=(--env-file .env); fi
exec "$PY" -m uvicorn server.app:app "${ARGS[@]}"
