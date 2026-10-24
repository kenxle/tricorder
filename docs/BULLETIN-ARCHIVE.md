# Bulletin Board Archive

> **Resolved messages from the [Bulletin Board](BULLETIN.md).** A message moves here once its action items are done, or once everyone it mentions has seen it. This keeps the live board short.
>
> **When and how to archive:** see "Archiving" in [`AGENTS.md`](../AGENTS.md).

---

## Archived 2026-10-24

| Date | Time | Agent (Owner) | Message |
|------|------|---------------|---------|
| 2026-10-24 | 11:15 | Benjamin | @Ken: organizing the TypeScript workspace with Turbo. The web app moves from `readout/` to `apps/web/`; generated TypeScript types move to `packages/schema/` and are imported as `@tricorder/schema`. Python stays the demo backend; only its generated-output and static-serving paths change. `apps/mobile/` is reserved for Benjamin's upcoming Expo app. **OPEN:** workspace implementation and verification.  **RESOLVED:** superseded by the verified workspace migration. |
| 2026-10-24 | 11:07 | Benjamin | Installed and pinned `@tanstack/intent` 0.5.6 in `readout/`, with setup commands in TESTING.md and tooling status in ARCHITECTURE.md. Setup found no dependency skills and left permissions and agent guidance unchanged; rerun it when a package ships skills. Web typecheck and build passed. npm audit reports the existing Vite dependency as high severity; no Vite update is included. The staged `readout/src/Steering.tsx` change is preserved and excluded.  **RESOLVED:** superseded by the verified workspace migration. |

## Archived 2026-10-24

| Date | Time | Agent (Owner) | Message |
|------|------|---------------|---------|
| 2026-10-24 | 11:22 | Benjamin | @Ken: adding `apps/api/` as a dev-only workspace wrapper for the existing Python API. Root `npm run dev` will run API and web together through Turbo. API source stays in its current Python folders. **OPEN:** implementation and verification.  **RESOLVED:** superseded by the unified dev-command handoff. |
| 2026-10-24 | 11:19 | Benjamin | @Ken: Turbo/npm workspaces are ready. `readout/` moved to `apps/web/`; generated types moved to `packages/schema/`, imported as `@tricorder/schema`. Python remains the running backend and schema authority. Root `npm ci`, Turbo typechecks/build, cache restoration, schema freshness, 144 schema/server tests, Vite module/API proxy requests and verification-helper launch/doctor/cleanup passed. Independent review passed after fixing the helper path. Expo belongs in `apps/mobile/` and is not scaffolded. Restart existing dev servers after the move. Changes are uncommitted; the existing staged Steering patch is preserved. Next: add the mobile app and port runtime packages.  **RESOLVED:** superseded by the unified dev-command handoff. |
