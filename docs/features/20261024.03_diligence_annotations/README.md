# iPhone diligence annotations

Benjamin requested an Expo demo with two associates and a GP. Associates select diligence text and leave attributed notes; the GP sees all notes and their context. This iteration saves on the device with Zustand and MMKV. It does not add authentication, backend writes, sharing or live synchronization.

## Demo

1. On Company, choose Maya Chen or Alex Rivera from **Demo persona**.
2. Open Ploy or Sazabi. Long-press diligence prose and adjust the native selection handles. Linked paragraphs first enter selection mode; long-press again to select words. **Done selecting** returns to the clickable citations.
3. Tap **Annotate selection**, enter a comment, and **Save annotation**.
4. Switch associates and add another note.
5. Switch to Jordan Lee (GP). **Team annotations** shows every saved note with its author, local date/time, quote and company/room context. **Show original passage** reveals the captured passage with the quote highlighted.
6. Reload the app. The selected persona and notes are restored from this device.

All three names are fictional demo identities. The persona picker is a demo control, not access control. GP annotation creation is rejected by the state store as well as hidden in the UI. Existing research/request/steering controls keep their existing behavior.

## Coverage and anchoring

The shared readout `Body` participates only inside an `AnnotationScope`. Company reports (active saved readout and legacy screen), evidence sheets, room claims/flags/gaps/asks, steering explanations/revisions and the UX Flow memo prototype supply scopes. Form inputs, buttons, navigation, alert text and headings do not become annotation inputs.

Each note stores scope identity/label, block identity, full original text, UTF-16 start/end, exact quote, comment, author and creation time. Evidence rows and repeated gap/status labels have individual item scopes. Highlighting requires the same scope, block and exact source text, so changed research retains its old note in the review list without silently highlighting new words. Overlapping highlights preserve the original text.

The GP sees the captured passage rather than a navigation jump to a potentially changed report. There is no generated audit history of unrelated app actions, seeded fake diligence, edit/delete flow or notification system.

## Implementation

- `apps/mobile/src/annotations/model.ts`: validated records, range checks, scope matching and highlight segmentation.
- `store-core.ts`: testable Zustand vanilla store; saves before publishing successful state.
- `store.ts`: React selectors and isolated MMKV instance `tricorder.demo-annotations`, key `annotations:v1`.
- `context.tsx`: company/room and per-item scope providers.
- `annotatable-text.tsx`: iOS read-only multiline native selection, measured text height, highlights and frozen composer selection. The selection survives the focus change when pressing Annotate.
- `annotation-panel.tsx`: native persona picker/buttons/sheets, comment field and GP review.
- `rich-text.ts`: preserves inline citation presses while mapping highlight offsets; citation markers are attachments outside the prose offsets.

Only Zustand is added as a dependency. Enriched was considered; this implementation uses the installed React Native selection events and needs no additional native module or iPhone development-client rebuild. Array sorting uses the older Hermes-compatible API. The shared palette moved to `readout/colors.ts` to avoid a text/sheet/UI dependency cycle.

Flow: [local annotation data flow](../../ongoing/diagrams/diligence_annotations.md).

## Validation

- Eight annotation tests cover distinct authors, GP write rejection, invalid ranges, UTF-16 boundaries, overlapping highlights, unchanged-source matching, reload, corrupt records, failed writes and repeated-label scope isolation.
- Mobile typecheck and iOS JavaScript export passed during implementation. Root lint and full mobile tests are rerun after integration.
- iPhone 17 Pro simulator: native long-press selection without keyboard, save as Alex, save as Maya, GP review with both authors and original-passage expansion verified. Reload and nested evidence-sheet checks are recorded at closeout.
- Three independent read-only reviews examined correctness, security/data integrity and unnecessary complexity. Correctness/security found a repeated-label anchor collision; per-item scopes and a regression check address it. The requested named review models were unavailable, so available built-in reviewers were used.
- Physical iPhone, Android and web annotation interactions are not claimed as tested. Creation is intentionally iOS-only; existing web/Android prose remains readable.
