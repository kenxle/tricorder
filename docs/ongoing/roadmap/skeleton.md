# skeleton

The repo the four people build in, with the typed Claim schema and a stub for the shared file readers.

- **Status today:** done.
- **Who builds it:** agent.
- **Waits on:** saturday-specs (the example files). Ken has chosen to build now; he still asks the organisers and tells the judges plainly. The Claim schema in [FRAMEWORKS.md](../FRAMEWORKS.md), "The shared Claim", which is the single source for every field type.
- **Horizon:** Now to Friday night
- **Checked against:** merged in PR #2, schema/ server/ readout/ bin/ci-py and bin/ci-web exist.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The repo the four people build in, with the typed Claim schema and a stub for the shared file readers. The agent slices build in it too. This is option B on the [skeleton-card](skeleton-card.md): with every role budgeted to its last minute, building it on Saturday spends the first half hour of two people and puts the team behind ([critique_buildability.md](../../features/20261022.01_hackathon_plan/critique_buildability.md), finding 7).

**Waits on:** saturday-specs (the example files). Ken has chosen to build now; he still asks the organisers and tells the judges plainly. The Claim schema in [FRAMEWORKS.md](../FRAMEWORKS.md), "The shared Claim", which is the single source for every field type.

**Includes:**

- The folder layout in [ARCHITECTURE.md](../ARCHITECTURE.md), with a code-owners file mapping each folder to its role.
- One root dependency file listing everything known this week: the Anthropic SDK, Pydantic, FastAPI, the server runner, pdfplumber, openpyxl, pandas and an HTTP client.
- The FastAPI app in `server/` with the three routes the feasibility research names (list scans, run a scan, serve a result file) and a health route.
- `bin/ci-py`, which runs the Python tests, and `bin/ci-web`, which runs the readout page's type check and build. They are separate so a red TypeScript build does not block Python merges. The captain runs both before each merge, and the hosted CI runs the same two commands if one is set up.
- `bin/smoke <room>`, which runs every scan that exists, then the memo, and prints which scans ran and which are missing.
- `.env.example` with every variable in ARCHITECTURE.md, and `out/` ignored by git while `sample_out/` is kept.
- `schema/claim.py`: the Pydantic models (ScanResult, Claim, Source, Gap) typed in from the FRAMEWORKS JSON Schema, with "at least one source" enforced by the model.
- `schema/claim.schema.json` exported from it, and TypeScript types generated into `schema/ts/` for the readout page to import.
- `schema/readers.py` as a stub: one function per format (PDF by page, xlsx by cell, CSV by row, Markdown by line, transcript by segment), with signatures and no bodies. Backend-and-data fills it in on Saturday ([readers](readers.md)).
- The hand-written example files from saturday-specs copied into `sample_out/`.
- The guardrails fields marked "Set by the first code slice" filled in: CI command, health check, smoke command ([guardrails.md](../../../.claude/guardrails.md)).

**Done when:**

- `bin/ci-py` and `bin/ci-web` exit 0 on a fresh clone, the health route answers, and `bin/smoke data_room/hollis_voice_seed_drop` prints "no scans yet" without a crash.
- The schema is frozen and merged before Saturday.
- Every example file in `sample_out/` validates.

**If the organisers say no:** option A. The skeleton and the schema typing take the first half hour of backend-and-data and the captain on Saturday. Backend-and-data's half hour comes out of the contract-terms-saturday hour, which then reads Hollis Voice's contracts only. The captain's comes out of the quote checker, which goes back to the half hour first planned.

**Who:** agent. Ken reviews.

**Judgment:** no.
