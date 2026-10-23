# Readout store and delete

An operator saves a company's readout into the store for a fund, and it comes back later with its scan results and copies of the room files it read. Every changed save is a new numbered version, and saving the same readout again adds nothing. The operator can list everything held for one company, and one confirmed delete removes all of it, together with the company's outside pulls in `cache/`.

## Sub-features

- `store-save` stores the readout, its scan results and copies of only the files it read, as a numbered version.
- `store-idempotent` returns the same version with `"new": false` when the readout did not change.
- `store-get` returns the latest version, or one named, with its sources and files.
- `store-list` lists everything held for one company: versions, files by room path, scan results, cache files, total bytes.
- `store-delete` removes everything held for one company after a typed confirmation, and reports what is left (nothing).
- `store-ids` refuses a fund or company id that could name a path outside the store.

## How to get to it (user POV)

- Terminal: `python3 -m store save <room_dir>`, `python3 -m store list <company>`, `python3 -m store get <company> [--version N] [--full]`, `python3 -m store companies`, `python3 -m store delete <company> [--yes]`. Each takes `--fund` (default `demo`). The company id defaults to the room's folder name.
- API: `GET /api/store/<fund>`, `GET /api/store/<fund>/<company>`, `GET /api/store/<fund>/<company>/versions`, `GET /api/store/<fund>/<company>/readout?version=N`, `GET /api/store/<fund>/<company>/files/<room path>`, `POST /api/store/<fund>/<company>/save` with `{"room": "<room>"}`, `POST /api/store/<fund>/<company>/delete` with `{"confirm": "<company>"}`.
- The readout page has no store panel yet.

## Driving it with control.sh

Preconditions:

- Before `control.sh launch`, export `TRICORDER_STORE_DIR=<run folder>/store_data` and `TRICORDER_CACHE_DIR=<run folder>/cache`, so the server and every `control.sh cli` command use this run's store and cache, never the repo's `store_data/` or `cache/`.
- In `<run folder>/cache`, write one simulated outside pull, `outside/hollis_voice/website/home.html`, and an `index.json` with one entry pointing at it and one shared entry pointing at `signals/competitor_pricing.html`. Hollis Voice is synthetic and has no real pulls, so label this simulated in the report.
- `control.sh doctor` prints `OK` for this run.

- **Build the readout.** Run `control.sh cli python3 -m scans.redflags data_room/hollis_voice`, then `control.sh cli python3 -m scans.memo data_room/hollis_voice`. Both exit 0.
- **Save from the terminal.** Run `control.sh cli python3 -m store save data_room/hollis_voice`. Exit 0; stdout has `"version": 1`, `"new": true` and `"files_copied"` above 0.
- **Save again.** Run the same command. Stdout has `"version": 1` and `"new": false`.
- **Save through the API.** Run `control.sh api POST /api/store/demo/hollis_voice/save '{"room": "hollis_voice"}'`. `HTTP 200` with `"version": 1` and `"new": false`, because the readout is the same one.
- **List what is held.** Run `control.sh api GET /api/store/demo/hollis_voice`. `versions` has one entry, `results` is `["redflags"]`, `files` names room paths such as `02_financials/financial_model.xlsx`, and `cache` lists `outside/hollis_voice/website/home.html`.
- **Get it back with its sources and files.** Run `control.sh api GET /api/store/demo/hollis_voice/readout`. `readout.claims` holds the claims with their `sources`, and `results[0].inputs` names the files the scan read. Then `control.sh api GET /api/store/demo/hollis_voice/files/02_financials/expense_ledger.csv` returns the room file's text with `HTTP 200`.
- **Refuse a bad id or path.** `control.sh api GET /api/store/demo/a.b` is `HTTP 422`. `control.sh api GET /api/store/demo/hollis_voice/files/..%2F..%2Fanswer_key.json` is `HTTP 404`.
- **Refuse an unconfirmed delete.** `control.sh api POST /api/store/demo/hollis_voice/delete '{"confirm": "wrong"}'` is `HTTP 400`, and the list is unchanged. In the terminal, `echo no | control.sh cli python3 -m store delete hollis_voice` exits 1 with "Not confirmed. Nothing removed."
- **Delete.** Run `control.sh api POST /api/store/demo/hollis_voice/delete '{"confirm": "hollis_voice"}'`. `HTTP 200` with `"left": []`, `removed.versions` 1, `removed.cache_files` 1 and `removed.index_entries` 1.
- **Proof.** Run `control.sh api GET /api/store/demo/hollis_voice`: `versions`, `files` and `cache` are all `[]`. Run `control.sh cli find <run folder>/store_data <run folder>/cache`: no path names `hollis_voice`, and `index.json` keeps the shared `signals/` entry.

## Gotchas

- Without the two exports before launch, the store writes to the repo's `store_data/` and deletes from the repo's `cache/`. Run `control.sh doctor` and check the store root with `control.sh cli python3 -c "from store import open_store; print(open_store().root)"` if unsure.
- `save` reads the readout from this run's `out/`, so run `scans.memo` first. Without it, the CLI exits 1 and the route answers 404, both saying to run `python -m scans.memo`.
- The delete report names `out/hollis_voice` under `also_on_this_laptop`. The store never writes there and does not remove it; that is expected.
- Ids are lower case only. `Hollis_Voice` is refused, not folded.
- The full room's `pitch_video.mp4` is ignored by git and is usually absent, so a readout that cites it lists it under `not_copied`.
