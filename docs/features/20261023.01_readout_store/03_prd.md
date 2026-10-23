# PRD: readout store and delete

Short brief: [01_brief.md](01_brief.md). Interface example: [02_interface_example.md](02_interface_example.md). Roadmap slice: [readout-store](../../ongoing/ROADMAP.md#readout-store).

## Requirements

| ID | Requirement |
|---|---|
| STORE-R1 | `save(fund, company, readout, room_dir, results)` stores the readout, the scan result of every scan the readout names in `scans_run`, and copies of the files it read, as one version. It returns the version number, whether it is new, the content hash, and the files copied and not copied. |
| STORE-R2 | "The files it read" are the room paths named by `file` and `video` claim sources (claims and the unverified box) and by every scan result's `inputs`, plus the saved copy of each `url` or `api` source that `cache/index.json` names. Only those are copied; no other room file is stored. A name that is not a file, is missing, or resolves outside its room (or outside `cache/`) is recorded as not copied, with the reason, and is never read. Copies are named by sha256, so versions that read the same file share one copy. |
| STORE-R3 | Versions are numbered from 1 and every version is kept. A save whose content hash equals the latest version's adds nothing and returns that version with `new: false`. The content hash is sha256 over the readout without `built_at`, each scan result without `ran_at`, and the path and sha256 of every copied file. |
| STORE-R4 | `get(fund, company, version=None)` returns the latest version, or the one named, with the readout, the scan results and the file manifest. `read_file(fund, company, path, version=None)` returns a stored file's bytes. Anything not held raises `NotHeld` (CLI exit 1, route 404). |
| STORE-R5 | `list_company(fund, company)` returns everything held for the company: each version (number, saved time, room, counts, content hash), each file by its room path with its size and the versions that use it, the scan results, the company's files in `cache/`, and the total bytes. `list_versions` returns the versions alone. `companies(fund)` names the companies held for a fund. |
| STORE-R6 | A fund id and a company id match `^[a-z0-9][a-z0-9_-]{0,63}$`. Anything else (`..`, `/`, a dot, upper case, empty, too long) raises `BadId` before any path is built (CLI exit 2, route 422). |
| STORE-R7 | `delete_company(fund, company)` removes the company's folder in the store, `cache/outside/<company>/`, and every `cache/index.json` entry whose saved file is inside that folder. Other companies, other funds and shared cache entries stay. It returns what it removed and a list of what is left, read back from disk afterwards, which must be empty. Deleting a company with nothing held removes nothing and says so. |
| STORE-R8 | Delete is irreversible, so it needs a confirmation. The CLI asks the operator to type the company id unless `--yes` is given; any other answer removes nothing and exits 1. The route needs a body `{"confirm": "<company id>"}` that matches the path; otherwise it answers 400 and removes nothing. |
| STORE-R9 | The store root is `TRICORDER_STORE_DIR`, default `store_data/` at the repo root, which git ignores. The cache root is `TRICORDER_CACHE_DIR`, default `cache/`. |
| STORE-R10 | The store writes nothing in `out/` and nothing in the room. `get` returns data; it never restores files into `out/`. |
| STORE-R11 | A save is all or nothing: a version is written in a hidden temporary folder and renamed into place, so a crash leaves no half version, and listings skip hidden folders. |
| STORE-R12 | The interface is a `ReadoutStore` protocol with seven calls (`save`, `get`, `read_file`, `list_company`, `list_versions`, `companies`, `delete_company`). `FileStore` implements it on disk. `open_store()` returns the configured store, so a hosted store can replace it without touching callers. |
| STORE-R13 | CLI: `python -m store save <room_dir> [--fund F] [--company C]` (reads the readout and scan results from the room's out folder), `list <company>`, `get <company> [--version N]`, `delete <company> [--yes]`, each with `--fund` (default `demo`). Output is JSON on stdout. |
| STORE-R14 | Routes in `server/store_routes.py`: `GET /api/store/{fund}`, `GET /api/store/{fund}/{company}`, `GET .../versions`, `GET .../readout?version=N`, `GET .../files/{path}`, `POST .../save` with `{"room": "<room id>"}`, and `POST .../delete` with the confirm body. |

## Failure cases

- Save with no readout in the room's out folder: CLI exit 1 with "no readout for <room>; run python -m scans.memo <room_dir> first". Route 404.
- Save where a scan named in `scans_run` has no result file: the version is saved without it and `results_missing` names it.
- A crafted source uri such as `../../answer_key.json`: recorded as not copied, "outside the room". The answer key is never read.
- A version number that does not exist: `NotHeld`.
- A stored file path that is not in the version's manifest (including `../` forms): `NotHeld`, never a disk read by that path.
- The store root is missing: listings are empty; save creates it.

## Scope

In: the store package, CLI, routes, tests, the `.gitignore` line, the `store` test path.
Out: a page component (the routes are ready for it), a hosted store, encryption, per-reader overlays (reader-scenarios), sharing between funds.

## Logging

None beyond the CLI's JSON. Every call returns what it did.

## Questions

- **Ken: should delete also clear `out/<room>/`?** The store never writes there, so the Done when is met without it. But `out/` holds the scan results for that room on this laptop, and an investor who asked for "everything pulled" deleted may expect them gone too. Default for now: delete leaves `out/` alone and its report names the out folders that still hold results for the company's rooms, under `also_on_this_laptop`.
- **Outside-in builder: cache company key.** Delete assumes `cache/outside/<company>/` uses the same company id as the store (the room name by default).
