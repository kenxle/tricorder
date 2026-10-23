---
name: verify-tricorder
description: Drive Tricorder the way a user does and keep proof. Runs the scans on a synthetic data room, serves the API and the readout page from an instance this run owns, and saves transcripts, responses and screenshots. Use it to prove a scan, the memo merge, the API or the readout page works, before a PR and after a merge.
---

# Verify Tricorder

Tricorder reads a startup's data room and builds a readout of sourced claims. A user touches it three ways:

- **The command line.** `python3 -m scans.<scan> <room>` runs one scan, `python3 -m scans.memo <room>` builds the readout, `bin/smoke <room>` runs both, `python3 -m eval.score <room>` scores a room against its answer key.
- **The API.** `server/app.py` (FastAPI) lists rooms, runs scans, builds and serves readouts, and returns the text at a source's locator.
- **The readout page.** A React page in `readout/`, built to `readout/dist/` and served by the API at `/`.

The rooms are synthetic, in `data_room/`: `hollis_voice` (full room), `hollis_voice_seed_drop` (the first files only), `hollis_voice_clean` (no plants), and `brasswick` (a second company). Each planted room has an answer key (`data_room/answer_key*.json`). Nothing reaches the network: the helper sets `TRICORDER_OFFLINE=1`.

All driving goes through one helper: `.claude/skills/verify-tricorder/control.sh`. Run it from anywhere.

## Launch

```sh
export TRICORDER_VERIFY_RUN=pr-123        # any name; one run, one folder
.claude/skills/verify-tricorder/control.sh launch
```

- It builds `readout/dist/` if missing (`npm ci && npm run build` in `readout/`, needs Node 20), then starts the API on port 8790 (`TRICORDER_VERIFY_PORT` to change) with `TRICORDER_OUT_DIR` set to this run's own `out/`.
- Ready means it printed `ready: http://127.0.0.1:8790 ...`, which it prints only after `/health` answers `"ok":true`.
- It refuses a port that answers but that it did not start. Ken's own instance and other runs stay untouched.
- Scan results land in this run's `out/`, never in the repo's `out/`. A fresh run starts with no results, so drive the scans before reading any.
- Python dependencies come from `requirements.txt` (`pip install -r requirements.txt`). The deck-drawing test tools (matplotlib, reportlab, pypdf) are only for tests and are not needed here.

## Doctor

```sh
.claude/skills/verify-tricorder/control.sh doctor
```

Read-only. It checks that this run's server process is alive, `/health` answers with the `redflags` scan available, and the page is served. It prints the run, URL, out folder, evidence folder and the git revision. Run it before the first drive, after any failed drive, and whenever something looks off. A `FAIL` line names what is wrong.

## Drive

- **A command:** `control.sh cli <command...>` runs it in the repo against this run's out folder and saves the command, output and exit code. Example: `control.sh cli python3 -m scans.redflags data_room/hollis_voice`.
- **The API:** `control.sh api <METHOD> <path> [json]` saves the response body and HTTP status. Routes: `GET /health`, `GET /api/rooms`, `GET /api/scans`, `POST /api/rooms/<room>/scans/<scan>`, `GET /api/rooms/<room>/results/<scan>`, `POST /api/rooms/<room>/readout`, `GET /api/rooms/<room>/readout`, `GET /api/rooms/<room>/files/<path>`, `POST /api/rooms/<room>/source` with a Source object.
- **The page:** `control.sh shot <name>` saves a screenshot and the rendered DOM. The page opens on `hollis_voice`. Stable handles are the section labels: `aria-label="Top flags"`, `"Overview"`, `"Gaps"`, `"Could not verify"`, `"Ask list"`, and the room picker `aria-label="Room"`. The helper cannot pick another room on the page yet; prove other rooms through the API.

The feature recipes are in [features/README.md](features/README.md). Read the index, then the feature's file.

## Evidence

Evidence goes to `${TRICORDER_VERIFY_DIR:-${TMPDIR:-/tmp}/tricorder-verify}/<run>/evidence/`. Every helper call prints the file it saved.

- Drive the real user path: the CLI module, the API route, the page. Never call internal functions or patch data to make a result appear.
- Capture the action and the resulting state. For a scan, that is the CLI transcript and then the stored result read back through `GET /api/rooms/<room>/results/<scan>`.
- Check side effects: a scan writes `<run>/out/<room>/<scan>.json`; the memo writes `<run>/out/<room>/readout.json`.
- A source is proven only when `POST /api/rooms/<room>/source` returns text containing the claim's `quote`.
- Score against the answer key with `control.sh cli python3 -m eval.score data_room/<room>` after the scans and `scans.memo` ran on that room in this run. Without a readout it exits 2.
- Name the feature ID with each artifact in your report.

## Cleanup

```sh
.claude/skills/verify-tricorder/control.sh cleanup
```

It stops only the server this run started, by the pid in this run's `state.env`. It never kills by name or port, and never touches the evidence folder or the scan results. It prints how many evidence files remain. Folders are not removed: in this repo agents never delete files, so list the run folder for cleanup instead.

## Keeping this skill honest

Each feature has one file in `features/`. A new user-facing feature adds its own file and one line in the index, and touches nothing else. Run `/maintain-verification-skill` to audit the map against the code.

## Where this skill was proven

Proven end to end on 2026-10-23 at revision cc86536 in a Linux cloud container: launch, doctor, the deck-against-books recipe on Hollis Voice, Brasswick and the clean room, the score, a page capture, cleanup, and the evidence still present afterwards. Two things there differ from Ken's Mac and are not yet proven on it: Chrome was found at `/opt/pw-browsers/`, so on the Mac `shot` relies on the Playwright cache or `/Applications/Google Chrome.app` (set `CHROME` if neither exists); and `TMPDIR` on macOS is a per-user folder, so the run folder lands there unless `TRICORDER_VERIFY_DIR` is set.
