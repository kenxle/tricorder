# Feature progress: readout store and delete

**Now.** All three Done when lines pass, in tests and in a drive through `control.sh` on Hollis Voice. The store (`store/`), its CLI (`python -m store`), its routes (`server/store_routes.py`) and the verification map are built test first and committed on `forge/readout-store`. Full suite: `python3 -m pytest`, 234 passed, 18 skipped; `bin/ci-py` the same (2026-10-23). **Next:** the orchestrator merges; Ken answers the `out/` question below; a page panel for list and delete; steering and the other wave 2 features call `open_store().save(...)`.

Roadmap slice: [readout-store](../../ongoing/ROADMAP.md#readout-store). Route: prototype first, with an interface example (nonvisual).

## Attention needed

- **Review fix S9 (2026-10-23), done.** A delete under any fund removed `cache/outside/<company>/`, even for a fund that never stored the company. Now the shared cache goes only when this fund held the company and no other fund still does; otherwise the report lists it under `kept` with the reason, and a fund that held nothing gets `nothing_held: true` and touches nothing. Kept shared rather than keyed per fund, because the outside-in scans already write `cache/outside/<company>/` ([04_architecture.md](04_architecture.md), D6). Ken can still ask for a per-fund cache.

- **Ken: should delete also clear `out/<room>/`?** The store never writes in `out/`, so the Done when is met without it. But `out/hollis_voice/` still holds that room's scan results and readout on this laptop. Default set: delete leaves `out/` alone and its report lists those folders under `also_on_this_laptop`. Changing it is a few lines in `FileStore.delete_company` ([03_prd.md](03_prd.md), Questions).
- **Outside-in and cached-data builders: cache key.** Delete removes `cache/outside/<company>/` and the `cache/index.json` entries whose saved file is inside it, as the outside-in slice describes. That only works if the cache uses the same company id as the store, which defaults to the room name (`hollis_voice`). The index reader accepts a path string or an object with a `file` or `path` field ([04_architecture.md](04_architecture.md), D6).
- **Orchestrator: shared lines.** `server/app.py` gets the import and `include_router` just above the `StaticFiles` mount, not after it: a mount at `/` would shadow the store routes. `pyproject.toml` `testpaths` gains `"store"`. `.gitignore` gains `store_data/`. `.env.example` gains `TRICORDER_STORE_DIR` and `TRICORDER_CACHE_DIR`.
- **ARCHITECTURE.md is out of date (not edited, ongoing docs are off limits):** the Environment variables table lacks `TRICORDER_STORE_DIR` and `TRICORDER_CACHE_DIR`, and the Store row of "The stack" could name `store_data/` and `python -m store`.
- **Wave 2 builders (steering, founder requests, memo, contract terms):** call `store.open_store().save(fund, company, readout, room_dir, results)`; `store.files.load_from_out(room_dir)` gives the readout and results from `out/`. Saving an unchanged readout returns the same version with `new: false`.
- **The page:** no component yet. The routes are ready: `GET /api/store/{fund}/{company}` for the list and `POST /api/store/{fund}/{company}/delete` with `{"confirm": "<company>"}`.
- **Process note.** A stray `git checkout origin/main -- .` ran in this worktree after my second commit. Nothing was lost (all work was committed). I restored HEAD's files, stashed the copies of main's files it had staged (`stash@{0}`, identical to origin/main ccaa2f2), and merged main normally. The stash is listed under cleanup.

## Documents

- [product_thinking.md](product_thinking.md), [01_brief.md](01_brief.md)
- [02_interface_example.md](02_interface_example.md), with JSON from [spike/store_spike.py](spike/store_spike.py) ([spike/spike_output.json](spike/spike_output.json))
- [03_prd.md](03_prd.md): STORE-R1 to STORE-R14
- [04_architecture.md](04_architecture.md): decisions D1 to D9, data shapes, alternatives
- [05_plan.md](05_plan.md): slices and the verification table
- [06_verification.md](06_verification.md) and [evidence/](evidence/)
- Map: [.claude/skills/verify-tricorder/features/readout-store.md](../../../.claude/skills/verify-tricorder/features/readout-store.md)

## Work and evidence

| Outcome | Owner | State | Evidence or blocker | Next action |
|---|---|---|---|---|
| Spike and interface example | builder | done | `spike/spike_output.json` | none |
| Slice 1: disk store | builder | done | `store/tests/test_store.py`, commit 4a43838 | none |
| Slice 2: CLI and routes | builder | done | `store/tests/test_cli.py`, `server/tests/test_store_routes.py`, commit 4828abf | none |
| Slice 3: map and drive | builder | done | [06_verification.md](06_verification.md) | none |
| Page panel for list and delete | frontend | not started | no slice owns it yet | decide where it mounts |
| Callers save into the store | wave 2 builders | not started | interface above | each feature adds its call |

Verification rows: [05_plan.md](05_plan.md), "Verification".

## Decisions and events

- 2026-10-23T01:43Z: feature folder opened; worktree from origin/main cc86536.
- Spike on Hollis Voice: a rebuild must not be a new version (hash leaves out `built_at` and `ran_at`); the store must keep scan results, because `readout.json` has no `inputs`; listing by blob hash is unreadable, so the real list names room paths.
- Copies, not hashes, for the files read (D5): the Done when asks for the files back, and the delete removes the copies.
- Store root `store_data/`, not `store/`, because `store/` is the code package (D1).
- Ids are refused, not folded, when they are not lower case (D2).
- Only the latest version is compared for idempotence, so A, B, A is three versions of history (D4).
- Delete leaves `out/` alone and names it (default, waits on Ken).
- 2026-10-23T01:51Z: merged origin/main ccaa2f2 for the verify-tricorder skill; map written there, drive on port 8811, run `readout-store`.
- 2026-10-23: merged `claude/project-thread-ea11in` (all wave 2 features) for the S9 fix round; S9 fixed test first (three new tests red, then 52 store tests passed).
- No human approval was needed for any step.

## To delete at cleanup

- `stash@{0}` in this worktree ("readout-store: copies of origin/main files staged by a mistaken checkout"): copies of main's files, nothing of value.
- `/tmp/claude-0/-home-claude/46d40c2c-7610-5980-8cc8-4007978d4e75/scratchpad/readout-store/` (scratch out folder, spike store and cache, verify run folder).
- `/home/claude/wt/readout-store/readout/node_modules/` and `readout/dist/`, made by `control.sh launch`'s page build (both ignored by git).
- The worktree `/home/claude/wt/readout-store` once the branch is merged.
