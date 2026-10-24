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
corepack enable                   # Makes pnpm available with the pinned version
pnpm install --frozen-lockfile     # From the repo root; Node 22.13+ (CI uses 22)
```

The chart fixture tests need the data-room drawing packages and `pypdf`. Without them, pytest skips those fixtures. Install them for a complete local run without skips.

## Local development without API keys

Run these commands from the repo root after installing dependencies:

```sh
test -f .env || cp .env.example .env
```

Set `TRICORDER_OFFLINE=1`, `TRICORDER_OUT_DIR=out` and `TRICORDER_CONTRACT_READER=script` in `.env`. Leave API keys empty for the synthetic-room demo. Set `TRICORDER_OPERATOR_NAME` and `TRICORDER_OPERATOR` to your name.

Start the API and web app together with one command from the repo root:

```sh
pnpm dev
```

Turbo starts the Python API at <http://127.0.0.1:8787>, the tRPC gateway at <http://127.0.0.1:8789/trpc>, Vite at <http://localhost:5173>, and Expo Metro at <http://localhost:8081>. Vite proxies `/api`, `/health` and `/trpc` to Python. Python forwards `/trpc` queries to the gateway, which reads the existing Python REST API. Stop old dev servers first so those ports are free. Ctrl+C stops all Turbo tasks and their child processes.

The API dev task in `apps/api/` automatically loads the root `.env` through Uvicorn. Exported environment variables take precedence. It prefers `.venv/bin/python`, so no virtualenv activation is needed after setup. Set `TRICORDER_PYTHON` to override that choice; without a project virtualenv it falls back to `PYTHON` or `python3`. Python source changes reload the API; Vite handles frontend changes.

`bin/serve` runs Python and tRPC without reload through `pnpm start` and loads the root `.env`. Run `pnpm build` first to serve the built page at `/`. `bin/smoke` and `bin/ci-py` use the shell's environment. For a scan from the command line:

```sh
set -a
source .env
set +a
PYTHON=.venv/bin/python bin/smoke data_room/hollis_voice
```

Keep `TRICORDER_OUT_DIR=out` when exporting `.env`: an empty value selects the working directory instead of the default `out/` folder. Without API keys, model readings become gaps. Scans that have not been implemented also appear as gaps.

The workspace uses [Ultracite](https://www.ultracite.ai/) 8.0.2 with Oxlint and Oxfmt. Run `pnpm format` for formatting only, `pnpm fix` for formatting plus safe lint fixes, `pnpm check` for the shared read-only check, and `pnpm lint` for that check plus Expo ESLint. `bin/ci-web` runs `pnpm lint`, so CI enforces formatting. Agents must run the gate before declaring work complete; see [AGENTS.md](../../AGENTS.md#required-repository-workflow).

The initial migration formatted the app/workspace source and root configuration. Generated schema/API contracts, Python-owned memo/scans/schema files, research/prototype documents, data rooms, native build directories and lockfiles are excluded. Their existing generators and checks remain authoritative. Zed's automatic save formatting remains disabled; use the explicit shared commands rather than an editor default.

`oxlint.config.mts` extends Ultracite core and React. Its migration overrides waive 190 existing file/rule pairs in 37 named files, including style preferences and existing async/React patterns. These are file-wide exceptions, not proof that the legacy code meets every Ultracite rule. New files use the full presets. When cleaning up an affected file, remove its rule exception and fix the newly reported violations; do not extend this list for new work. Expo ESLint remains as an additional mobile-specific check.

## Intent agent guidance

`apps/web/` pins `@tanstack/intent` as a development dependency. After `pnpm install --frozen-lockfile`, run the installed CLI from that workspace:

```sh
pnpm --filter @tricorder/web exec intent list
pnpm --filter @tricorder/web exec intent install
```

With tRPC 11.19.0 installed, the `intent` command currently fails with `ERR_PACKAGE_PATH_NOT_EXPORTED` for `@tanstack/intent/intent-library`. This optional guidance tooling does not affect the runtime or CI gates. No managed guidance was changed.

The installed tRPC `intent` binary shadows the tooling CLI. Invoke Intent directly from the repo root to discover and load the installed skills without downloading a replacement:

```sh
node apps/web/node_modules/@tanstack/intent/dist/cli.mjs list
node apps/web/node_modules/@tanstack/intent/dist/cli.mjs load '@trpc/server#validators'
node apps/web/node_modules/@tanstack/intent/dist/cli.mjs load '@trpc/client#client-setup'
```

## TypeScript workspace commands

Use pnpm 11.9.0, pinned in `package.json`. `pnpm-workspace.yaml` defines the workspace, and `pnpm-lock.yaml` is the only JavaScript dependency lockfile. Run from the repo root:

```sh
pnpm install --frozen-lockfile
pnpm dev:web                    # Python API + tRPC + Vite; opens the web page
pnpm dev:mobile                 # Metro for the custom development client
pnpm build:ios                  # Build/install the native iOS development client
pnpm build:ios --device "Deez iPhone" # Build/install on the connected iPhone
pnpm dev                        # Python API + tRPC gateway + web + Expo Metro
pnpm typecheck                  # Web, mobile, gateway and shared schema through Turbo
pnpm format                     # Oxfmt, using the Ultracite preset
pnpm lint                       # Ultracite formatting/lint + mobile Expo ESLint
pnpm test                       # Gateway HTTP and validation tests
pnpm start                      # Python API + tRPC, serving the built web page
pnpm build                      # Web and mobile bundles: apps/{web,mobile}/dist/
pnpm build --filter=@tricorder/web
```

`bin/serve --dev` is an alias for `pnpm dev`. `bin/serve` starts Python and the tRPC gateway and serves the web build at `/` after a build. CI installs the root lockfile before running `bin/ci-web`. Dev tasks are uncached; build outputs and successful typechecks are cached locally in `.turbo/`.

The Expo SDK 58 starter lives in `apps/mobile/` and uses the root install and lockfile. `pnpm dev:mobile` starts Metro through Turbo. The dev commands explicitly select Turbo's terminal UI so Expo can receive keyboard input; select the mobile task and press `i` to interact. Use `pnpm --filter @tricorder/mobile ios`, `android` or `web` to open a platform. `pnpm build --filter=@tricorder/mobile` exports Android, iOS and web JavaScript bundles; it does not build an IPA or APK. SDK 58 needs a compatible development build until the physical-device Expo Go release supports it. The home screen ports the web readout, steering and founder-request flows to native controls. Launch commands bind Metro to localhost; iOS Simulator uses localhost and Android uses adb reverse. Physical devices require a trusted loopback port forward. `pnpm --filter @tricorder/mobile test` checks the local adapter allowlist, Host/origin refusals, JSON write requirements and fixed upstream. Device and file-picker behavior require runtime verification; an export alone does not prove those flows. See the mobile README for API environment settings. Keep app environment files in their app directories. From `apps/mobile/`, run `pnpm exec expo install --check` to check SDK compatibility and `pnpm dlx expo-doctor` for project diagnostics. App React versions follow each framework; the shared schema contains no React runtime. See [the mobile README](../../apps/mobile/README.md) for agent plugin installation and Expo MCP authentication.

The mobile lists pass an explicit `renderReadoutScroll` callback to FlatList. In the installed SDK 58 development client, the default list renderer produced blank native content while ordinary ScrollView content painted correctly. The explicit callback restored visible content and retains VirtualizedList refs and windowing. Each native Modal also supplies its own SafeAreaProvider. Keep these behaviors in the iOS runtime check when changing list or modal layout.

The workspace uses pnpm's default isolated install layout. Only esbuild's dependency build script is enabled in `pnpm-workspace.yaml`. Declare shared packages with `workspace:*`; do not add an npm lockfile. After intentionally changing dependencies, use `pnpm install` to update the lockfile.

See the official [pnpm workspace guide](https://pnpm.io/workspaces), [Expo monorepo guide](https://docs.expo.dev/guides/monorepos/) and [Turbo workspace structure](https://turborepo.dev/docs/crafting-your-repository/structuring-a-repository).

`apps/web/turbo.json` uses Turbo's `with` configuration to start the API and tRPC dev tasks whenever the web dev task is selected. Vite opens the browser automatically at <http://localhost:5173>, or its next free port if 5173 is occupied. Use `BROWSER=none pnpm dev:web` to suppress browser opening.

## tRPC gateway

`apps/rpc/src/router.ts` owns `AppRouter`. Its read-only queries cover health, scans, rooms, results, steering readouts/revisions/source text, memos, the readout store and founder requests. `apps/web/src/trpc.ts` imports the router type only and creates the vanilla client with batching. Other clients can import `AppRouter` through `@tricorder/rpc` and use `inferRouterInputs` / `inferRouterOutputs` from `@trpc/server`.

Procedure inputs use Zod 3.25.76 schemas. Objects strip unknown keys; path IDs reject traversal; source indexes and versions require safe integers without string coercion. Null and omitted versions both select the latest version. tRPC infers client inputs before normalization and returns its existing `BAD_REQUEST` envelope for invalid input. The error message contains Zod issues. `pnpm --filter @tricorder/rpc test` covers these rules through HTTP, and the gateway typecheck includes `src/inference.typecheck.ts` assertions for exact client input types and generated Python outputs. See the official [tRPC validators guide](https://trpc.io/docs/server/validators) and [Zod basic usage](https://zod.dev/basics).

Python owns the contracts. `server/api_models.py` declares response shapes for routes that previously returned bare dictionaries. Existing Pydantic models remain in their owning modules. FastAPI assembles these annotations into OpenAPI; `server/export_api.py` introspects that schema locally and writes `packages/schema/src/api.ts`, exported as `@tricorder/schema/api`. It emits `PythonModels` and `PythonAPI`, with separate path parameters, query parameters, JSON request bodies and outputs per operation. No running server, credentials or new dependencies are needed.

```sh
pnpm generate:api               # After changing Python route/model annotations
pnpm check:api                  # Fail if generated contracts are stale
```

The commands select Python using `TRICORDER_PYTHON`, the project `.venv`, then `PYTHON` / `python3`. Python dependencies from setup must be installed. `bin/ci-py` checks freshness, and TypeScript checks catch incompatible gateway/client uses after regeneration. Generation is explicit, not a live watcher.

For example, the web client infers these directly:

```ts
const rooms = await trpc.room.list.query();
const result = await trpc.room.result.query({ room: rooms[0].id, scan: "redflags" });
const memo = await trpc.memo.get.query({ room: rooms[0].id, version: 1 });
type Memo = RouterOutputs["memo"]["get"];
```

When adding a route: declare its Python inputs and response model, regenerate, then add an explicit procedure in `apps/rpc/src/router.ts` using its generated `PythonAPI` operation. The helper derives its output from the operation key, so no handwritten TypeScript response interface is needed. This exports declared HTTP contracts, not arbitrary Python functions, database rows or fields guessed from samples. A plain `dict` or `Any` stays `unknown`; give that field a Python model for deeper inference. In particular, founder-request item `guidance` and `requests` still contain unstructured dictionaries.

The gateway binds to loopback and accepts only GET queries with a loopback Host. FastAPI validates declared response models. The gateway trusts this contract and does not validate successful JSON again. Node 22.13+ runs the TypeScript entrypoint with native type stripping. Generated request types include existing write routes, but the tRPC gateway remains read-only; uploads, writes and file/PDF/HTML responses continue through REST. Existing web feature calls remain in place. The steering GET endpoints (`room.steerable`, `room.revisions`, `room.source`) retain Python's lazy-build behavior: if a readout is absent but scan results exist, the engine builds and saves it. GET-only refers to the gateway transport, not a guarantee of zero filesystem writes.

For alternate ports, export `PORT` for Python, `TRICORDER_RPC_PORT` for the gateway, and matching `TRICORDER_RPC_URL` for Python. `TRICORDER_API_URL` overrides the gateway's Python destination, otherwise it uses `PORT` (default 8787). Export these in the shell before launch; the Node task does not load `.env`. Vite's existing proxy target remains port 8787.

## The gates

| Command | What it runs | Green means |
|---|---|---|
| `bin/ci-py` | `python -m schema.export --check` and `python -m server.export_api --check` (generated schema and API contracts are current), then `pytest` over the test folders in `pyproject.toml`, including the store, founder requests, memo, and steering | exit 0, "N passed" and no failures |
| `bin/ci-web` | Turbo typechecks all TypeScript packages, checks Ultracite formatting/lint and mobile Expo ESLint, runs gateway and mobile adapter tests and exports/builds apps | exit 0 |
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
