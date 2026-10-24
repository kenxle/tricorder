# Tricorder mobile

Expo SDK 58, Expo Router and TypeScript, created from the official default starter. The home screen ports the existing web readout to React Native. The web app remains available. It includes room selection and rebuilding, flags, steerable pieces and claims, source text, evidence rows, revision diffs, gaps, unverified claims, ask-list copying, founder email drafts, and reply file intake into a working copy of a synthetic room.

Run from the repository root:

```sh
pnpm install --frozen-lockfile
pnpm dev:mobile                         # Localhost Metro, with Turbo terminal UI
pnpm dev                                # API, tRPC, Vite and Metro together
pnpm --filter @tricorder/mobile ios      # Open the iOS Simulator
pnpm --filter @tricorder/mobile android  # Open an Android emulator
pnpm --filter @tricorder/mobile web      # Open the Expo web preview
pnpm typecheck --filter=@tricorder/mobile
pnpm lint --filter=@tricorder/mobile
pnpm build --filter=@tricorder/mobile    # Export Android, iOS and web bundles
```

## Readout API and device access

Start `pnpm dev` for the existing Python API and the Expo server together. To run only those two services, use separate terminals:

```sh
pnpm --filter @tricorder/api dev
pnpm dev:mobile
```

The Expo API route forwards only the readout's existing endpoints to `http://127.0.0.1:8787`. Contracts come from `@tricorder/schema` and `@tricorder/schema/api`; the app does not import web or backend code. The adapter checks Host, Origin/Referer and content type. Both services must bind to loopback: mobile launch scripts pass `--localhost`. Do not start this adapter with `--lan` or `--tunnel`, or deploy it on a public listener. There is no remote user authentication. Python's existing localhost guard is unchanged.

Expo web uses same-origin `/api` requests. Native development uses localhost and the Metro port from its manifest. The iOS Simulator shares the Mac's localhost. The Android launch command sets up adb reverse for Metro; if starting the app manually, use `adb reverse tcp:8081 tcp:8081` first. A physical device needs a trusted loopback port forward to the Mac for both the bundle and API requests; Wi-Fi access to Metro is deliberately disabled. Installing a development build on an iPhone alone does not establish that connection.

For a different backend port, set `TRICORDER_API_URL=http://127.0.0.1:<port>` in `apps/mobile/.env.local`. For a different native Expo server/forwarded address, set `EXPO_PUBLIC_API_URL=http://localhost:<port>` there. This value points to Expo, not directly to Python. Restart Metro after changing environment files. Release bundles require this explicit server URL and a running, locally bound Expo server; no hosted deployment or production authentication is provided.

Clipboard uses `expo-clipboard`, mail actions open an editable composer and never send automatically, and reply intake uses DocumentPicker and FileSystem. Sign-off fields are remembered for the app session. File selections survive request-tab changes. Drafts can be explicitly regenerated after changing sign-off/date fields.

```sh
pnpm --filter @tricorder/mobile test     # Adapter boundary tests
```

## Native development client

The mobile dev commands open the custom development client. Build and install it once before starting Metro:

```sh
pnpm build:ios                         # Build/install on the selected iOS Simulator
pnpm build:ios --device "Deez iPhone"    # Build/install on that connected iPhone
pnpm dev:mobile                        # Start Metro for the development client
```

The iPhone command requires Developer Mode, a trusted connection, and Apple Development signing. Simulator builds use the local Xcode toolchain without signing. Rebuild after changing native dependencies or app configuration; normal JavaScript changes use Metro and Fast Refresh. Generated `ios/` files stay ignored.

The build writes JavaScript bundles and web output to `apps/mobile/dist/`. It does not produce an IPA or APK. SDK 58 requires a compatible development build until Expo Go supports it. See [Expo's setup guide](https://docs.expo.dev/get-started/create-a-project/). Native folders are generated and ignored. Keep native configuration in `app.json`. Metro discovers this pnpm monorepo automatically; no custom resolver is needed. `@tricorder/schema` is declared as a local workspace dependency for the shared contracts.

In Turbo's terminal UI, select the mobile task and press `i` to interact with its terminal. Expo's `i`, `a` and `w` shortcuts then open a platform.

The package owns `dev` rather than `start` so the repository's `pnpm start` continues to launch the Python API and tRPC gateway without Metro.

## AI agents

[AGENTS.md](AGENTS.md) contains Expo guidance and links to SDK 58 documentation. Agent plugin settings and Expo MCP registration are developer-local configuration. They are not included in this scaffold; install and configure the tools on each developer machine.

Install the official skills plugins on each developer machine:

```sh
codex plugin add expo@openai-curated
claude plugin install expo@claude-plugins-official --scope project
```

Authenticate with your own Expo account from the repository root:

```sh
# Older Codex Expo plugins provide skills without registering MCP.
if ! codex mcp get expo >/dev/null 2>&1; then
  codex mcp add expo --url https://mcp.expo.dev/mcp
fi
codex mcp login expo
```

For Claude Code, run `/mcp` in the session and sign in to Expo. Restart the agent session after installing plugins. OAuth credentials stay outside the repository. See the [official agent setup](https://docs.expo.dev/get-started/create-a-project/#set-up-an-ai-agent) and [Expo MCP guide](https://docs.expo.dev/mcp/).
