#!/usr/bin/env bash
# Drive Tricorder the way a user does, in an instance this run owns, and keep the evidence.
#
#   control.sh launch            start the API and the built readout page for this run
#   control.sh doctor            read-only: is this run's instance worth driving?
#   control.sh cli <args...>     run a command in the repo against this run's out dir, transcript saved
#   control.sh api <METHOD> <path> [json]   call this run's API, response saved
#   control.sh shot <name>       screenshot and DOM of the readout page (it opens on hollis_voice), saved
#   control.sh cleanup           stop what launch started; evidence stays
#
# One run is named by TRICORDER_VERIFY_RUN (default: "default"). Everything for it lives in
#   ${TRICORDER_VERIFY_DIR:-${TMPDIR:-/tmp}/tricorder-verify}/<run>/
#     out/        this run's scan results (TRICORDER_OUT_DIR), never the repo's out/
#     evidence/   transcripts, responses, screenshots; cleanup never touches it
#     state.env   pid and port of the server this run started
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
RUN="${TRICORDER_VERIFY_RUN:-default}"
BASE="${TRICORDER_VERIFY_DIR:-${TMPDIR:-/tmp}/tricorder-verify}/$RUN"
OUT="$BASE/out"
EV="$BASE/evidence"
STATE="$BASE/state.env"
PY="${PYTHON:-python3}"
mkdir -p "$OUT" "$EV"

port() { if [ -f "$STATE" ]; then . "$STATE"; echo "$PORT"; else echo "${TRICORDER_VERIFY_PORT:-8790}"; fi; }
url() { echo "http://127.0.0.1:$(port)"; }
stamp() { echo "$(date -u +%Y%m%dT%H%M%SZ)_$$_$RANDOM"; }  # unique even within one second

chrome() {
  if [ -n "${CHROME:-}" ]; then echo "$CHROME"; return; fi
  for c in /opt/pw-browsers/chromium-*/chrome-linux/chrome \
           "$HOME"/Library/Caches/ms-playwright/chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium \
           "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"; do
    [ -x "$c" ] && { echo "$c"; return; }
  done
  command -v chromium || command -v google-chrome || { echo "no Chrome found; set CHROME" >&2; return 1; }
}

cmd_launch() {
  if [ -f "$STATE" ]; then . "$STATE"; if kill -0 "$PID" 2>/dev/null; then echo "already running: pid $PID on $(url)"; return; fi; fi
  local p="${TRICORDER_VERIFY_PORT:-8790}"
  if curl -s -o /dev/null "http://127.0.0.1:$p/health"; then
    echo "port $p answers but this run did not start it; set TRICORDER_VERIFY_PORT to a free port" >&2; exit 1
  fi
  if [ ! -f "$REPO/apps/web/dist/index.html" ]; then
    (cd "$REPO" && bin/ci-web) > "$EV/page_build.txt" 2>&1
  fi
  # No subshell: $! must be the server's own pid, so cleanup stops exactly what launch started.
  cd "$REPO"
  TRICORDER_OUT_DIR="$OUT" TRICORDER_OFFLINE=1 nohup "$PY" -m uvicorn server.app:app \
      --host 127.0.0.1 --port "$p" > "$BASE/server.log" 2>&1 &
  echo "PID=$! PORT=$p" > "$STATE"
  for _ in $(seq 1 50); do
    if curl -s "http://127.0.0.1:$p/health" | grep -q '"ok":true'; then echo "ready: $(url) (run $RUN, out $OUT)"; return; fi
    sleep 0.2
  done
  echo "server did not answer /health; see $BASE/server.log" >&2; exit 1
}

cmd_doctor() {
  [ -f "$STATE" ] || { echo "FAIL no instance launched for run $RUN"; exit 1; }
  . "$STATE"
  kill -0 "$PID" 2>/dev/null || { echo "FAIL pid $PID is not running"; exit 1; }
  local h; h="$(curl -s "$(url)/health")" || { echo "FAIL $(url)/health does not answer"; exit 1; }
  echo "$h" | grep -q '"ok":true' || { echo "FAIL health says: $h"; exit 1; }
  echo "$h" | grep -q '"redflags"' || { echo "FAIL the redflags scan is not available: $h"; exit 1; }
  curl -s "$(url)/" | grep -q '<div id="root">' || { echo "FAIL the readout page is not served (build apps/web/dist)"; exit 1; }
  echo "OK run=$RUN pid=$PID url=$(url) out=$OUT evidence=$EV rev=$(git -C "$REPO" rev-parse --short HEAD)"
}

cmd_cli() {
  local f="$EV/cli_$(stamp).txt"
  { echo "\$ $*"; echo "(cwd $REPO, TRICORDER_OUT_DIR=$OUT)"; } > "$f"
  set +e
  (cd "$REPO" && TRICORDER_OUT_DIR="$OUT" TRICORDER_OFFLINE=1 "$@") >> "$f" 2>&1
  local code=$?
  set -e
  echo "exit $code" >> "$f"
  cat "$f"
  echo "saved: $f"
  return $code
}

cmd_api() {
  local method="$1" path="$2" body="${3:-}" f="$EV/api_$(stamp).json"
  if [ -n "$body" ]; then
    curl -s -X "$method" -H 'content-type: application/json' -d "$body" -w '\nHTTP %{http_code}\n' "$(url)$path" > "$f"
  else
    curl -s -X "$method" -w '\nHTTP %{http_code}\n' "$(url)$path" > "$f"
  fi
  tail -c 600 "$f"; echo; echo "saved: $f"
}

cmd_shot() {
  local name="${1:?usage: control.sh shot <name>}"
  local target="$(url)/"
  local c; c="$(chrome)"
  "$c" --headless --no-sandbox --disable-gpu --window-size=1280,2200 --virtual-time-budget=5000 \
       --screenshot="$EV/$name.png" "$target" > /dev/null 2>&1
  "$c" --headless --no-sandbox --disable-gpu --virtual-time-budget=5000 --dump-dom "$target" > "$EV/$name.dom.html" 2>/dev/null
  echo "saved: $EV/$name.png and $EV/$name.dom.html"
}

cmd_cleanup() {
  if [ -f "$STATE" ]; then
    . "$STATE"
    if kill -0 "$PID" 2>/dev/null; then
      kill "$PID"
      for _ in $(seq 1 50); do kill -0 "$PID" 2>/dev/null || break; sleep 0.1; done
      if kill -0 "$PID" 2>/dev/null; then echo "pid $PID did not stop within 5 seconds" >&2; exit 1; fi
      echo "stopped pid $PID"
    else
      echo "pid $PID already gone"
    fi
    mv "$STATE" "$BASE/state.stopped.env"
  else
    echo "nothing launched for run $RUN"
  fi
  echo "evidence kept: $EV ($(ls "$EV" | wc -l | tr -d ' ') files)"
}

case "${1:-}" in
  launch) cmd_launch ;;
  doctor) cmd_doctor ;;
  cli) shift; cmd_cli "$@" ;;
  api) shift; cmd_api "$@" ;;
  shot) shift; cmd_shot "$@" ;;
  cleanup) cmd_cleanup ;;
  *) sed -n 2,16p "$0"; exit 2 ;;
esac
