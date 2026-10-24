# Testing

## Charter

**What belongs:** How testing works: what runs, how to run it and what counts as green. The commands for each test layer. What the CI gate runs. Setup a new builder needs.

**What does not:** Why a feature was built a certain way. Test cases for one feature.

**Level of detail:** Commands and short notes. Enough to run every suite.

**Describes:** the test folders and CI config

**Sources:** the CI config (`.github/workflows/ci.yml`), `bin/`, `pyproject.toml` and the test folders

## Setup

```sh
python3.12 -m venv .venv            # Python 3.12 matches CI
source .venv/bin/activate
pip install -r requirements.txt     # Python 3.11 or newer
pip install -r data_room/requirements.txt
pip install pypdf                  # chart fixture PDF assembly
(cd readout && npm ci)             # Node 22 matches CI
```

The chart fixture tests need the data-room drawing packages and `pypdf`. Without them, pytest skips those fixtures. Install them for a complete local run without skips.

## Local development without API keys

Run these commands from the repo root after installing dependencies:

```sh
test -f .env || cp .env.example .env
```

Set `TRICORDER_OFFLINE=1`, `TRICORDER_OUT_DIR=out` and `TRICORDER_CONTRACT_READER=script` in `.env`. Leave API keys empty for the synthetic-room demo. Set `TRICORDER_OPERATOR_NAME` and `TRICORDER_OPERATOR` to your name.

The launch scripts do not load `.env`. Export it before running them:

```sh
source .venv/bin/activate
set -a
source .env
set +a
PYTHON=.venv/bin/python bin/smoke data_room/hollis_voice
PYTHON=.venv/bin/python bin/serve --dev
```

Open <http://localhost:5173> for the page. The API and built page are at <http://127.0.0.1:8787>. The explicit `PYTHON` selects this project's environment even if your shell already sets `PYTHON` to another interpreter. Use the same prefix for `bin/ci-py`.

Keep `TRICORDER_OUT_DIR=out` when exporting `.env`: an empty value selects the working directory instead of the default `out/` folder. Without API keys, model readings become gaps. Scans that have not been implemented also appear as gaps.

Zed project settings in `.zed/settings.json` disable automatic formatting on save. This repo has no configured formatter or lint command, and applying an editor's default formatter creates unrelated changes to existing files. Language-server diagnostics and the CI gates below remain available. Set a shared formatter and its configuration before enabling automatic formatting for this project.

## The gates

| Command | What it runs | Green means |
|---|---|---|
| `bin/ci-py` | `python -m schema.export --check` (generated schema files are current), then `pytest` over the test folders in `pyproject.toml`, including the store, founder requests, memo, and steering | exit 0, "N passed" and no failures |
| `bin/ci-web` | The page's type check and build | exit 0 |
| `bin/smoke <room_dir>` | Every scan that exists on one room, then the merge | each scan prints its counts and the merge prints its summary, with no traceback |

GitHub Actions runs `bin/ci-py` and `bin/ci-web` as two separate jobs on every pull request, so a red page build never blocks a Python merge. A red CI blocks a merge, even on Saturday.

## Where tests live

- Each scan keeps its tests in `scans/<name>/tests/`. A red-flag check's test reads the generated rooms in `data_room/` and compares against the answer key by check name.
- The schema's tests read every answer-key location back from the room, so the readers and the generator cannot drift apart.
- Tests that need a scan's output write it under a temporary `TRICORDER_OUT_DIR`, never into `out/`.
- No test calls a model or an outside service. Model readings are tested on recorded responses; outside sources on their clients' sample mode.

## Scoring against an answer key

```sh
bin/smoke data_room/hollis_voice
python -m eval.score data_room/hollis_voice
```

prints each planted entry as found or missed, each decoy as clear or flagged, and a last line "found N of 8; decoys flagged N of 3".
