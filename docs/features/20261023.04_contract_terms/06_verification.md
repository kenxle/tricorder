# Verification: contract-terms

The verification method is pstack's, through the project skill `.claude/skills/verify-tricorder/`. This feature's map file is [`.claude/skills/verify-tricorder/features/contract-terms.md`](../../../.claude/skills/verify-tricorder/features/contract-terms.md), with one line added to that folder's `features/README.md`.

## The run

Driven once by that recipe, as a user would, on 2026-10-23 at revision `3338036` plus the working tree that became `32a82d7`:

```sh
export TRICORDER_VERIFY_RUN=contract-terms TRICORDER_VERIFY_PORT=8814
control.sh launch     # ready: http://127.0.0.1:8814
control.sh doctor     # OK run=contract-terms pid=6972 ... rev=3338036
...                   # the steps below
control.sh cleanup    # stopped pid 6972; evidence kept (8 files)
```

The run's evidence was copied into [evidence/verify/](evidence/verify/) after cleanup.

| Step in the recipe | Sub-feature | Entry point | Evidence | What it shows |
|---|---|---|---|---|
| Run the scan on Hollis Voice | all | `POST /api/rooms/hollis_voice/scans/redflags` | `api_20261023T015924Z_7065_2097.json` | HTTP 200, the stored result |
| Read the plan flag | `ct-plan` | `GET /api/rooms/hollis_voice/results/redflags` | `api_20261023T015925Z_7085_16216.json` | `plan_revenue_past_term_end` flag on Marlow, "8 plan months after it (2027-02 to 2027-09)", $161,258; info on Cedar & Pine and Brookline Row |
| Read the clause results | `ct-clauses`, `ct-terms-panel` | same response | same file | three `clause_notes` "no exclusivity, most-favoured-customer or change-of-control clause" claims; Panels "contract terms" and "contract checks" |
| Prove a quote | `ct-plan` | `POST /api/rooms/hollis_voice/source` | `api_20261023T020002Z_7597_1324.json` | the page text contains "from 2026-08-01 to 2027-01-31" |
| Read the gaps | `ct-missing` | same result | `api_20261023T015925Z_7085_16216.json` | seven "Not in the room: the contract for ..." gaps; coverage $51,584 of $186,739 (27.6%) |
| Ask lines | `ct-asks` | `POST /api/rooms/hollis_voice/readout` | `api_20261023T020003Z_7609_22934.json` | seven ask lines "Please send the current customer contract language ...", `checklist_id` C34, `from_kind` gap; 0 unverified claims |
| Contracts-only folder | `ct-contracts-only` | `python3 -m scans.redflags <folder>` | `cli_20261023T020003Z_7627_16691.txt` | exit 0, 4 claims (all `clause_notes`), the gap "Not in the room: the ARR build or the customer file to compare with" |
| Seed drop | `ct-missing` | `python3 -m scans.redflags data_room/hollis_voice_seed_drop` | `cli_20261023T020003Z_7652_25363.txt` | exit 0; its result holds "Not in the room: customer contracts" |
| Score | all | `python3 -m eval.score data_room/hollis_voice` | `cli_20261023T020004Z_7664_21354.txt` | `found 0 of 8; decoys flagged 0 of 3` |

Not driven through the user path: the three test contracts (30-day, one-year, change of control). They exist only inside the unit tests, which build them in a temporary folder; the map file's Gotchas says so. Their output through the real `check()` is in [02_interface_example.md](02_interface_example.md), sections 2 to 4, and in [evidence/tests_contract_terms.txt](evidence/tests_contract_terms.txt).

No screenshot: this feature draws nothing new on the page.

## The score, before and after

Both runs used a scratch `TRICORDER_OUT_DIR`, the red-flag scan, then `scans.memo`, then the scorer.

- Before (origin/main, `cc86536`): `hollis_voice: found 0 of 8; decoys flagged 0 of 3` ([evidence/score_before.txt](evidence/score_before.txt)).
- After (this branch): `hollis_voice: found 0 of 8; decoys flagged 0 of 3` ([evidence/score_after.txt](evidence/score_after.txt)).

No change is expected. The key credits PF1 to `arr_from_subscription_rows` (entry 1.2, not built yet), and none of this feature's check names is in the key. What matters here is that no decoy was flagged.
