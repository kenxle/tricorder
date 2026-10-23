# Verification: readout store and delete

Method: pstack's verification skills (`.claude/skills/create-verification-skill/`, `maintain-verification-skill/`), through the project skill `.claude/skills/verify-tricorder/`. The map file is [.claude/skills/verify-tricorder/features/readout-store.md](../../../.claude/skills/verify-tricorder/features/readout-store.md), listed in that folder's `README.md`.

## The run

Driven once by that recipe on 2026-10-23, revision 24c7c0b (this branch after merging main ccaa2f2), in a Linux cloud container:

```sh
export TRICORDER_VERIFY_RUN=readout-store TRICORDER_VERIFY_PORT=8811
export TRICORDER_VERIFY_DIR=<scratch>/readout-store/verify
export TRICORDER_STORE_DIR=$TRICORDER_VERIFY_DIR/readout-store/store_data
export TRICORDER_CACHE_DIR=$TRICORDER_VERIFY_DIR/readout-store/cache
control.sh launch; control.sh doctor     # OK run=readout-store pid=3538 url=http://127.0.0.1:8811 ... rev=24c7c0b
```

Every step of the recipe ran through `control.sh cli` or `control.sh api`. `control.sh cleanup` stopped pid 3538 and kept 25 evidence files, copied to [evidence/](evidence/). Afterwards no `uvicorn server.app` process was running.

## What each artifact shows

| Step | Artifact | Result |
|---|---|---|
| Build the readout | `cli_20261023T015202Z_3611_18532.txt`, `cli_20261023T015203Z_3623_4161.txt` | redflags 10 claims, 4 gaps; memo exit 0 |
| Save (terminal) | `cli_20261023T015203Z_3635_21502.txt` | version 1, new, 16 files, 387425 bytes, nothing not copied |
| Save again | `cli_20261023T015204Z_3644_26410.txt` | version 1, `"new": false` |
| Save (API) | `api_20261023T015204Z_3653_3916.json` | HTTP 200, version 1, `"new": false` |
| List | `api_20261023T015225Z_3795_11123.json` | 1 version, 16 room files, `redflags`, `outside/hollis_voice/website/home.html`, 510165 bytes |
| Get | `api_20261023T015225Z_3811_19598.json` | 10 claims; first is `redflags-001` from `03_metrics/monthly_metrics.csv` row 22; 16 scan inputs |
| A stored file | `api_20261023T015215Z_3719_20601.json` | the expense ledger; bytes equal `data_room/hollis_voice/02_financials/expense_ledger.csv` (checked with `cmp`) |
| Bad id, traversal | `api_20261023T015215Z_3737_4184.json`, `api_20261023T015215Z_3751_23863.json`, `cli_20261023T015245Z_3917_21785.txt` | 422; 404; exit 2 |
| Unconfirmed delete | `api_20261023T015216Z_3765_28554.json`, `cli_20261023T015216Z_3780_10708.txt` | 400 "nothing removed"; exit 1 "Not confirmed. Nothing removed." |
| Delete (API) | `api_20261023T015233Z_3839_18855.json` | `"left": []`; removed 1 version, 16 files, 1 result, 1 cache file, 1 index entry |
| Proof | `api_20261023T015233Z_3853_10733.json`, `cli_20261023T015233Z_3867_1012.txt`, `cli_20261023T015233Z_3876_22065.txt` | empty listing; only the shared `signals/` page left in the cache; index keeps only the competitor entry |
| Terminal round trip | `cli_20261023T015245Z_3898_13210.txt` to `cli_20261023T015245Z_3936_4342.txt` | save, get, typed confirmation delete with `"left": []`, then an empty list |

Simulated, labelled: the saved outside page `cache/outside/hollis_voice/website/home.html` and the competitor page were written by hand for this run, because Hollis Voice is synthetic and has no outside pulls. Everything else is the real readout, scan result and room files.

## Not proven

- The readout page: it has no store panel, so there is no screenshot. `page_build.txt` is only the launch's page build.
- The real `cache/` layout: it does not exist yet. Delete follows the roadmap's `cache/outside/<company>/` rule and was proven on a scratch cache built to it.
- Two saves at the same moment (the rename retry in D9) are not exercised by a test.
- Ken's Mac: the run was in a Linux container.
