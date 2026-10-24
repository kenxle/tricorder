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

Zed project settings in `.zed/settings.json` disable automatic formatting on save. The mobile package has ESLint, but the repo has no configured formatter. Applying an editor's default formatter creates unrelated changes to existing files. Language-server diagnostics and the CI gates below remain available. Set a shared formatter and its configuration before enabling automatic formatting for this project.

## Intent agent guidance

`apps/web/` pins `@tanstack/intent` as a development dependency. After `pnpm install --frozen-lockfile`, run the installed CLI from that workspace:

```sh
pnpm --filter @tricorder/web exec intent list
pnpm --filter @tricorder/web exec intent install
```

With tRPC 11.19.0 installed, the pinned Intent 0.5.6 CLI currently fails discovery with `ERR_PACKAGE_PATH_NOT_EXPORTED` for `@tanstack/intent/intent-library`. This optional guidance tooling does not affect the runtime or CI gates. No managed guidance was changed.

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
pnpm lint                       # Mobile ESLint through Turbo
pnpm test                       # Gateway HTTP and validation tests
pnpm start                      # Python API + tRPC, serving the built web page
pnpm build                      # Web and mobile bundles: apps/{web,mobile}/dist/
pnpm build --filter=@tricorder/web
```

`bin/serve --dev` is an alias for `pnpm dev`. `bin/serve` starts Python and the tRPC gateway and serves the web build at `/` after a build. CI installs the root lockfile before running `bin/ci-web`. Dev tasks are uncached; build outputs and successful typechecks are cached locally in `.turbo/`.

The Expo SDK 58 starter lives in `apps/mobile/` and uses the root install and lockfile. `pnpm dev:mobile` starts Metro through Turbo. The dev commands explicitly select Turbo's terminal UI so Expo can receive keyboard input; select the mobile task and press `i` to interact. Use `pnpm --filter @tricorder/mobile ios`, `android` or `web` to open a platform. `pnpm build --filter=@tricorder/mobile` exports Android, iOS and web JavaScript bundles; it does not build an IPA or APK. SDK 58 needs a compatible development build until the physical-device Expo Go release supports it. The starter has no readout or backend connection yet. Keep app environment files in their app directories. From `apps/mobile/`, run `pnpm exec expo install --check` to check SDK compatibility and `pnpm dlx expo-doctor` for project diagnostics. App React versions follow each framework; the shared schema contains no React runtime. See [the mobile README](../../apps/mobile/README.md) for agent plugin installation and Expo MCP authentication.

The workspace uses pnpm's default isolated install layout. Only esbuild's dependency build script is enabled in `pnpm-workspace.yaml`. Declare shared packages with `workspace:*`; do not add an npm lockfile. After intentionally changing dependencies, use `pnpm install` to update the lockfile.

See the official [pnpm workspace guide](https://pnpm.io/workspaces), [Expo monorepo guide](https://docs.expo.dev/guides/monorepos/) and [Turbo workspace structure](https://turborepo.dev/docs/crafting-your-repository/structuring-a-repository).

`apps/web/turbo.json` uses Turbo's `with` configuration to start the API and tRPC dev tasks whenever the web dev task is selected. Vite opens the browser automatically at <http://localhost:5173>, or its next free port if 5173 is occupied. Use `BROWSER=none pnpm dev:web` to suppress browser opening.

## tRPC gateway

`apps/rpc/src/router.ts` owns `AppRouter`, `room.list` and `room.readout`. `apps/web/src/trpc.ts` imports the router type only and creates the vanilla client with batching. Add new procedures to the router; future apps can import the same type through `@tricorder/rpc`. Builds, source text, file downloads, steering and founder requests continue to use REST.

The gateway binds to loopback and accepts only GET queries with a loopback Host. Python remains the runtime validator for its response data; the gateway uses generated `Readout` types at that boundary. Node 22.13+ runs the TypeScript entrypoint with native type stripping, so the gateway needs no build step.

For alternate ports, export `PORT` for Python, `TRICORDER_RPC_PORT` for the gateway, and matching `TRICORDER_RPC_URL` for Python. `TRICORDER_API_URL` overrides the gateway's Python destination, otherwise it uses `PORT` (default 8787). Export these in the shell before launch; the Node task does not load `.env`. Vite's existing proxy target remains port 8787.

## The gates

| Command | What it runs | Green means |
|---|---|---|
| `bin/ci-py` | `python -m schema.export --check` (generated schema files are current), then `pytest` over the test folders in `pyproject.toml`, including the store, founder requests, memo, and steering | exit 0, "N passed" and no failures |
| `bin/ci-web` | Turbo typechecks all TypeScript packages, lints mobile, runs gateway tests and exports/builds apps | exit 0 |
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
