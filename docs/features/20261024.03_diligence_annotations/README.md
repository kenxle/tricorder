# iPhone diligence annotations

Benjamin requested an Expo demo with two associates and a GP. Associates select diligence text and leave attributed notes; the GP sees all notes and their context. This iteration saves on the device with Zustand and MMKV. It does not add authentication, backend writes, sharing or live synchronization.

## Demo

1. On Company, choose Maya Chen or Alex Rivera from **Demo persona**.
2. Open Ploy or Sazabi. Tap **Select text to annotate**, long-press a word, and adjust the native selection handles. **Done selecting text** restores clickable citations. Plain evidence passages also support direct long-press selection inside sheets.
3. Tap **Annotate selection**, enter a comment, and **Save annotation**. Saving or cancelling returns linked prose to reading mode.
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

- Nine annotation tests cover distinct authors, GP write rejection, invalid ranges, UTF-16 boundaries, overlapping highlights, unchanged-source matching, reload, corrupt records, failed writes repeated-label scope isolation, and transient associate-only selection mode.
- Final checks passed: mobile typecheck, root lint/format gate, iOS JavaScript export and all 40 current mobile tests (including concurrent feature tests).
- iPhone 17 Pro simulator: native long-press selection without keyboard, save as Alex, save as Maya, GP review with both authors and original-passage expansion verified. Reload restored Jordan (GP) and both saved notes. Inline source actions still open evidence sheets. Creating a comment from a nested evidence sheet was not independently completed in the walkthrough.
- Three independent read-only reviews examined correctness, security/data integrity and unnecessary complexity. Correctness/security found a repeated-label anchor collision; per-item scopes and a regression check address it, and both reviewers verified the fix. The requested named review models were unavailable, so available built-in reviewers were used.
- Physical iPhone, Android and web annotation interactions are not claimed as tested. Creation is intentionally iOS-only; existing web/Android prose remains readable.

## Selection interaction correction

A regular tap on linked prose previously triggered React Native Text press feedback across the whole paragraph. The long-press handler also required a second gesture before the annotation input could capture a range. The explicit selection control removes that hidden transition and the misleading pressed highlight. Selection mode is not persisted and resets when switching personas; remounting the passage clears stale ranges. Native evidence passages remain directly selectable, and Android/web retain ordinary text copying.

The 12 focused annotation/rich-text tests, mobile typecheck and root lint passed. Independent review identified the evidence-sheet entry and non-iOS copying regressions; both were fixed and rechecked. On the iPhone simulator, Ploy selection displayed native word handles, Annotate opened the exact quote, and saving returned to reading mode with the count increased from two to three. Physical-device validation remains outstanding.

## Local handoff

The implementation is recorded in commit `c6942e0`; final validation is recorded in a separate documentation commit. Existing Company/citation/room-arrival work in the shared checkout was preserved. The iPhone simulator preview started for this task uses port 8097; the other development servers were not stopped. Three clearly labelled “Demo review” annotations were created through the simulator UI across both associates, in the simulator's local store only. Physical-phone stores are separate.

The installed Intent executable was unavailable. The implementation session could not write `.git/FETCH_HEAD` in the sandbox and read the fetched upstream bulletin separately. Benjamin subsequently authorized atomic commits and pushing; delivery preserves the existing commit sequence and reconciles upstream without rewriting history.
