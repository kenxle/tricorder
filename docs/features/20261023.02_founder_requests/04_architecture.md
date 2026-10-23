# Architecture: requests to the founder

Requirements: [03_prd.md](03_prd.md) (FR-R1 to FR-R21). Plan and verification: [05_plan.md](05_plan.md).

## Summary

A new top-level package, `founder_requests/`, beside `memo/`, `inbox/` and `store/` in ARCHITECTURE.md's folder table. It reads a built readout and the guidance table to draft a message, and it takes a reply's file into a room under `rooms/`, reruns the scans whose inputs changed, and rebuilds the readout. A FastAPI router and a CLI expose it. A React component shows it on the readout page. No schema change, no new dependency, no model call.

## Existing structure (reconnaissance)

- **The ask list.** `readout.asks` (`AskItem`: `what`, `why`, `piece`, `from_kind`, `checklist_id`, `if_you_have_it`). `scans/memo/coverage.py` appends checklist lines and writes the Panel "checklist ask lines" (`what`, `checklist_ids`, `from_kind`, `ask_stage`, `top_five`), keyed by `what`.
- **Checklist and guides.** `docs/ongoing/checklist.csv` names a guide per row (column `guide`). `scans/memo/checklist.py` has `DOC_PATTERNS` (file name patterns per document row), `room_files`, `match_document`, `load()` with each row's piece and kind.
- **Rooms.** `server/app.py` serves rooms from `data_room/` then `rooms/` (first name wins), a room being any folder with an `NN_` folder. `rooms/` and `out/` are git-ignored.
- **Scans.** `scans.base.available()` lists built scans; each `scans/<name>/scan.py` has `NEEDS`; `scans.base.room_inputs()` lists the input files a room holds; each `ScanResult.inputs` lists the files the scan saw (the red-flag scan writes every room input file). `server/app.py` runs a scan as `python -m scans.<name> <room>`.
- **The page.** `readout/src/App.tsx` renders the ask list with one "Copy" button. `server/app.py` mounts the built page at `/` last.

## Affected components

| Component | Change |
|---|---|
| `founder_requests/guidance.py` | New. `GUIDANCE` (33 entries, one per guide), `for_item(checklist_id)`. |
| `founder_requests/draft.py` | New. `items(readout)`, `founder_text(ask)`, `leaks(text)`, `default_selection`, `company_and_greeting`, `draft(...) -> Draft`, `mailto`. |
| `founder_requests/intake.py` | New. `copy_room`, `check_name`, `check_bytes`, `target_for`, `save`, `waiting_scans`, `receive`. |
| `founder_requests/__main__.py` | New CLI: `list`, `draft`, `copy-room`, `add`. |
| `server/founder_requests_routes.py` | New `APIRouter`. |
| `server/app.py` | One import and one `include_router` line, placed before the page mount (a mount at `/` placed first would answer every path). |
| `readout/src/FounderRequests.tsx` | New panel. Mount: one line in `App.tsx` under the ask list section (orchestrator's call; see Attention needed). |
| `pyproject.toml` | `founder_requests` added to `testpaths`, so its tests run in `bin/ci-py`. |

## Data shapes

**Item** (one ask line, `GET /api/rooms/{room}/founder-requests`): `number`, `text` (founder words), `operator_why`, `piece`, `checklist_id`, `covers`, `if_you_have_it`, `ask_stage`, `top`, `title`, `guidance` (`guide`, `title`, `what`, `form`, `good[]`, `path`) or null.

**Draft** (`POST /api/rooms/{room}/founder-requests/draft`, body `{"numbers": [6, 16], "to": "", "sender": ""}`): `room`, `company`, `to`, `subject`, `body`, `mailto`, `mailto_fits`, `read_from`, `items[]`, `leaks[]` (always empty; the test asserts it).

**Receipt** (`POST /api/rooms/{room}/founder-requests/files?answers=C22&name=<original name>`, raw body): `room`, `room_path`, `copied_from` (null unless a copy was made), `saved` (path relative to the room), `checklist_id`, `bytes`, `scans_rerun[]` (`scan`, `ok`, `error`), `status_before`, `status_after`, `asks_before`, `asks_after`, `readout` (path).

**Log** `out/<room>/founder_requests.json`: `{"received": [<receipt without readout>, "at": ...]}`.

### Proposed schema changes

None needed. After Saturday, an `AskItem.guide` field would let the page show guidance without this package's table; the captain's call.

## Flows

### Draft

`items(readout)` walks `readout.asks`, joins each line to its Panel row by `what` (lower case), and attaches guidance by checklist id. `draft(readout, numbers)` picks the lines, splits required from "if you have it", groups each by guide, and writes the body. `founder_text` strips locations, cell references, paths and ids, and turns a fragment into "Please send ...". The route returns `leaks` from the same function the test uses.

### Receive

1. Resolve the room. A room under `data_room/` is refused with the copy command (route) or copied first when the CLI is given `--copy` (writes `rooms/<room>_live`).
2. Resolve the request: a checklist id, or an ask number from the current readout. Only document and ask rows are accepted.
3. Check the name (FR-R17), the size (FR-R19) and the bytes (FR-R18).
4. `target_for`: folder (FR-R12) and name (FR-R13). Write with `O_CREAT | O_EXCL | O_NOFOLLOW` (FR-R20).
5. `waiting_scans`: for each built scan whose `NEEDS` are met, run it when it has no result or its result's `inputs` lacks a current room input file.
6. Run each as `python -m scans.<name> <room>` with the caller's environment (so `TRICORDER_OUT_DIR` holds), then `build_readout` and `write_readout`.
7. Read the item's status from the new coverage Panel; append the log.

`TRICORDER_ROOMS_DIR` moves `rooms/` for tests and verification runs. The router finds rooms in `data_room/` and in that folder by the same rule as `server/app.py`.

## Alternatives

- **Multipart upload.** Needs `python-multipart`, not in `requirements.txt`. Rejected: a raw body with the name in the query does the same job.
- **A model to write the message.** Rejected: slower, untestable without a key, and every line already exists in plain words.
- **Rerun every scan after every file.** Simple, but it grows with the scan count. The `inputs` rule reruns only what saw a different room.
- **Guidance read live from the guide text.** The guides are written for investors ("Concentration raised by the founder before the investor finds it"); founder words need a rewrite, so the table is hand-written with a test tying each entry to its guide's sections.
- **Writing into `data_room/` and relying on git to undo.** Rejected by the brief: synthetic rooms are checked in.

## Failure modes

| Failure | Handling |
|---|---|
| Scan subprocess fails | Recorded in `scans_rerun` with `ok: false` and the error tail; merge still runs. |
| Readout missing before upload | `status_before: "unknown"`, `asks_before: null`. |
| Two uploads at once with the same name | `O_EXCL`: the second gets 409. |
| Disk full mid-write | The partial file is left and the error is returned; listed for cleanup, never deleted by the code. |

## Security and privacy

The upload is the attack surface. Room ids match `^[A-Za-z0-9_-]+$` and must be a known room. The file name is never used as a path: only its sanitised stem is, under a folder the code picks. The target is resolved and must be inside the room; the folder must not be a symlink; the write does not follow links and never overwrites. Kinds are an allowlist checked against the bytes. Zip-based files are checked for their total unpacked size before any reader opens them. Size is checked from `Content-Length` and again while reading the body. The server binds to localhost (ARCHITECTURE.md). The founder's files stay in `rooms/`, which git ignores.

## Selected findings

- Wave 1 review U8 (founder text with cell references) is handled by `founder_text` and tested on every line of two rooms.
- The page mount order in `server/app.py` decides whether a router added below it is reachable; the include line goes above the mount.
