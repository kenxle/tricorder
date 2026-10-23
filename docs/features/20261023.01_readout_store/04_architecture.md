# Architecture: readout store and delete

PRD: [03_prd.md](03_prd.md). System shape: [ARCHITECTURE.md](../../ongoing/ARCHITECTURE.md), "The stack" ("The readout-store slice puts a store behind the same paths").

## Inputs

- A `Readout` (`schema/claim.py`), usually `out/<room>/readout.json`.
- The `ScanResult` of each scan in `readout.scans_run`, usually `out/<room>/<scan>.json`.
- The room folder, to copy the files named by sources and inputs.
- `cache/index.json` and `cache/outside/<company>/`, for URL source copies and for delete.

## Where it plugs in

| Piece | File | Notes |
|---|---|---|
| Protocol and factory | `store/base.py` | `ReadoutStore` protocol, `open_store()`, `BadId`, `NotHeld`, `check_id` |
| Records | `store/models.py` | Pydantic models owned by the store, not by `schema/` |
| Disk store | `store/files.py` | `FileStore(root, cache_dir)` |
| CLI | `store/__main__.py`, `store/cli.py` | `python -m store save|list|get|delete` |
| Routes | `server/store_routes.py` | an `APIRouter`, one `include_router` line in `server/app.py` |
| Tests | `store/tests/`, `server/tests/test_store_routes.py` | `store` added to `testpaths` in `pyproject.toml` |

Callers in wave 2 (steering, founder requests, the memo, contract terms) call `open_store().save(...)` after they write a readout, and `get(...)` to read one back. None of them needs to know the layout.

## Decisions

### D1. The store root: `TRICORDER_STORE_DIR`, default `store_data/`

The code package is `store/` (ARCHITECTURE's folder table), so the data cannot share that name without mixing code and investor data in one folder. `store_data/` at the repo root is beside `out/` and `rooms/`, which git already ignores. `.gitignore` gains `store_data/`. Tests always pass a `tmp_path` root. `cache/` gets the same treatment, `TRICORDER_CACHE_DIR`, so a test never touches the real `cache/`.

### D2. Identity: fund id and company id, validated before any path

Both must match `^[a-z0-9][a-z0-9_-]{0,63}$`. That excludes `.`, `/`, `\`, spaces, upper case and the empty string, so no id can name a parent folder or an absolute path. The check runs in every public call before a path is built, and the folder is resolved and checked to sit inside the root as a second fence. The company id defaults to the room name (`hollis_voice`); the fund id defaults to `demo` on the CLI. Upper case is refused, not folded, so two spellings never name one company.

### D3. Layout on disk

```
store_data/<fund>/<company>/
  versions/0001/version.json      VersionInfo plus the file manifest
  versions/0001/readout.json      the Readout as saved
  versions/0001/results/<scan>.json
  files/<sha256>                  one copy per distinct file content
```

Blobs are shared by every version of the company, so a steer that rereads the same room copies nothing new. They are never shared across companies or funds, so deleting one company folder removes every byte of it and nothing else.

### D4. Revisions: numbered versions, all kept, content hash for idempotence

Each save that changes something makes the next number. `get` returns the latest. The content hash is sha256 over the readout's canonical JSON (sorted keys) without `built_at`, each scan result without `ran_at`, and `path=sha256` for every copied file. Those two timestamps change on every rebuild while the content does not; the spike showed a rebuild would otherwise create a duplicate version. Only the latest version is compared: if a steer is undone, the content goes A, B, A, and the third save is a real new version, because the history is what steering shows. `Readout.revisions` rides inside the readout, so a steer's `PieceRevision` list is kept in every version that has it.

### D5. "The files it read": copied, not hashed

The brief's data rule allows the readout and its sources, and the Done when asks for the readout to come back "with its sources and files". A hash alone cannot show a file on another machine. So the store copies the files it read, and only those: `file` and `video` source uris, every `ScanResult.inputs` entry that is a room file, and the cache copy of each `url` or `api` source named in `cache/index.json`. Nothing else from the room is stored (STORE-R2). Every copy is recorded with its sha256 and size, and the store's delete removes the copies with everything else, so copying does not weaken the delete.

A name that resolves outside its room, or outside `cache/`, is never opened. It is recorded under `not_copied` with the reason, which is how a crafted `../answer_key.json` in a source is visible rather than silent.

### D6. Delete

`delete_company` removes, in order: the company folder in the store (`shutil.rmtree`, after the id check and an is-inside-root check, and refusing a symlinked folder), `cache/outside/<company>/`, and the `cache/index.json` entries whose saved file is inside that folder. The index is rewritten through a temporary file and a rename. Then it walks both places again and returns what is left; the CLI and the route report that list, and a test asserts it is empty. The store never writes in `out/`, so nothing there is the store's to remove. The report names `out/<room>/` folders that still exist for the company's rooms under `also_on_this_laptop`, so the operator sees them; whether delete should remove them is a question for Ken (PRD, Questions).

**The shared cache (review fix S9, 2026-10-23).** The first build removed `cache/outside/<company>/` on any fund's delete, even for a fund that never stored the company, and so could wipe the offline cache the demo runs on (`docs/features/20261022.10_feature_breakdown/review_wave2a.md`, S9). The outside-in scans write that folder without a fund, so it is shared. Two ways out: key the cache by fund (`cache/outside/<fund>/<company>/`), or keep it shared and guard the delete. Call: keep it shared and guard the delete. Keying by fund would change a layout the outside-in slice already writes, and the demo has one fund. The rule: the cache folder and its index entries go only when this fund held at least one version of the company and no other fund in the store holds a version of it. Otherwise they stay, and the report names them under `kept` with the reason ("fund zzz holds nothing for hollis_voice" or "still held for hollis_voice by fund fund_b"). A fund that never stored the company gets `nothing_held: true` and nothing is touched. What this cannot know: a fund that looked at the company's outside pages but never saved a readout does not count as holding it, so the last holder's delete removes those pages. Once the cache records which fund pulled what, the rule can follow that record instead.

The cache index format is not built yet. The roadmap says it "maps each URL, or each API call ... to its saved file and date". The store reads an object whose values are either a path string or an object with a `file` (or `path`) field, relative to the cache root. Anything else in the index is left untouched.

### D7. Confirmation

CLI: `delete` prints what is held, asks the operator to type the company id, and removes nothing on any other answer (exit 1). `--yes` skips the question for scripts. Route: `POST /api/store/{fund}/{company}/delete` with `{"confirm": "<company id>"}`; a missing or different value is a 400 and nothing is removed. A POST, not a DELETE with a body, because some clients drop a DELETE body.

### D8. The interface a hosted store would replace

Seven calls: `save`, `get`, `read_file`, `list_company`, `list_versions`, `companies`, `delete_company`. `read_file` is separate from `get` so a hosted store can stream a blob instead of loading every file into one response. `companies` is there so the page can list what a fund holds before it picks a company. Nothing outside `store/` builds a store path.

### D9. All-or-nothing saves

A version is written into `versions/.tmp-<random>/` and renamed to its number. A rename onto an existing number fails, so two saves at once cannot share a number; the loser recomputes the next number and tries again. Listings skip hidden folders.

## Data shapes (store/models.py)

- `StoredFile`: `path`, `origin` (`room` or `cache`), `sha256`, `bytes`.
- `NotCopied`: `name`, `why`.
- `VersionInfo`: `version`, `saved_at`, `room`, `built_at`, `content_sha256`, `claims`, `unverified`, `gaps`, `revisions`, `results`, `results_missing`, `files`, `not_copied`.
- `SaveResult`: `fund`, `company`, `version`, `new`, `content_sha256`, `files_copied`, `bytes_copied`, `not_copied`, `results_missing`.
- `StoredReadout`: `fund`, `company`, `version` (a `VersionInfo`), `readout`, `results`.
- `HeldFile`: `path`, `origin`, `sha256`, `bytes`, `versions`.
- `Holding`: `fund`, `company`, `versions`, `files`, `results`, `cache`, `total_bytes`.
- `DeleteReport`: `fund`, `company`, `nothing_held`, `removed` (counts of versions, files, results, cache files, index entries), `kept` (cache paths left in place, each with why), `left` (paths still on disk for this fund, expected empty), `also_on_this_laptop`.

## Alternatives

- **SQLite.** One file, transactions, queries. Rejected for Saturday: the payload is JSON plus binary files, a folder per company makes "delete everything" one `rmtree` that is easy to check by eye, and a hosted store will replace it anyway.
- **Hash only, no copies.** Rejected in D5.
- **Store the whole room.** Rejected: it stores files no claim used, against the data rule.
- **A version per save, no hash.** Rejected: every rebuild would add a duplicate.

## Proposed schema changes

None needed. One for after Saturday: a `Readout.inputs` list (the union of scan inputs) would let a reader of `readout.json` alone see what was read, without the scan results.

## Risks

- Large files (the pitch video) are copied whole when a source names them. The full room's video is git-ignored and absent on most checkouts, so it is recorded as not copied ("file missing").
- The company id in `cache/outside/` is an assumption (A1 in [product_thinking.md](product_thinking.md)).
