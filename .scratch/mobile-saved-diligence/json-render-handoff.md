# JSON render request-dialog foundation

Benjamin selected json-render on 2026-10-24. Implemented as a bounded first slice; none of the five milestone tickets is marked complete by this work.

- Shared contract: `packages/request-ui/src/catalog.ts`; request/draft domain logic: `model.ts`; bounded JSONL validation: `stream.ts`.
- Backend: `apps/rpc/src/request-ui-stream.ts`, GET `/ui/request?company=ploy&stage=seed`, version 1 header. Saved prototype research only, no model call.
- Expo stream: `apps/mobile/src/app/api/ui/request+api.ts`, fixed local RPC target, no Python buffering.
- Native renderer and bindings: `apps/mobile/src/request-ui/request-form.tsx`; local form/session: `session.ts`; saved snapshot: `draft.ts`.
- Registry wraps existing Black Card native controls. Form state cannot be patched by the stream. Unknown components/actions/bindings fail closed and show the bundled checklist fallback. New installed components require an app release.
- Save snapshots exact displayed text, stage, selections/custom items in separate local MMKV storage; restore does not regenerate text. No sending, sent-state changes, or backend draft writes.

Validation: 46 tests (20 mobile, 17 RPC, 9 shared), three typechecks, root lint, Android/iOS/web exports, three independent reviews with findings fixed. Native iOS simulator: streamed form, checkbox update, edited text, refresh preservation, local save, leave/reopen restoration. Expo web: refresh preservation, saved reload restoration, empty-copy guard, explicit regeneration. Physical iPhone and Android runtime remain unverified for this slice. Existing phone launcher was restarted to clear stale workspace resolution; simulator verification Metro runs at localhost:8088.

Next: ticket 02 still needs canonical durable request entities and sent/open/answered lifecycle; this is only its renderer and local-draft foundation. Extend the catalog with sourced evidence cards/readout sections under ticket 01, room-progress surfaces under 03, and memo blocks under 05. Preserve existing data contracts and explicit synthetic/saved labels. Resolve replay versus actual ingestion before ticket 03. Financial what-if controls need a backend calculation/action contract before becoming functional.
