# Streamed native UI assessment

2026-10-24. Source and official-documentation assessment for Benjamin. This is a proposed implementation direction, not a new approved ticket or a verified package integration.

## Recommendation

Trial `@json-render/react-native` on the request dialog. Keep the approved working-page hierarchy and native navigation in the app. Let the backend supply validated section descriptions and data updates using a catalog of installed Tricorder components. Start with deterministic generation from saved data; an LLM is optional for composing the allowed components.

Layouts, labels, visibility and data can change remotely within the installed catalog. New native component implementations, native modules and action implementations still require shipping app code. A renderer does not supply persistence, authorization, scan orchestration or a reliable event stream by itself.

## Existing code to build on

| Product data | Owning code | Proposed native interaction |
| --- | --- | --- |
| Saved pre-room sections and evidence | [company model](../../apps/mobile/src/company/model.ts), [company screen](../../apps/mobile/src/company/company-screen.tsx) | Section status, founder/comp cards, evidence rows and source sheets. Move the local research shape into an explicit shared boundary as ticket 01 requires. |
| Claims, flags and piece verdicts | [domain schema](../../schema/claim.py), [generated API contracts](../../packages/schema/src/api.ts), [native readout](../../apps/mobile/src/readout/ReadoutScreen.tsx) | ClaimCard, MetricComparison, PieceSummary and EvidenceButton. Preserve claim IDs, sources, units and periods. |
| Checklist coverage and asks | [coverage](../../scans/memo/coverage.py), [request drafting](../../founder_requests/draft.py), [native request manager](../../apps/mobile/src/readout/FounderRequests.tsx) | RequestItem, checkbox/toggle, custom-item text input, draft editor and explicit copy/mark-sent actions. |
| Received documents and reanalysis | [intake](../../founder_requests/intake.py), [request routes](../../server/founder_requests_routes.py) | ArrivalNotice, file-to-request mapping, progress and answered/open status updates. The current intake returns after rerunning scans and rebuilding; intermediate progress events need implementation. |
| Steering and revisions | [steering engine](../../steering/engine.py), [native steering](../../apps/mobile/src/readout/Steering.tsx) | Instruction input, Apply action, progress, revision diff and the claim that moved a verdict. Preserve script-computed figures. |
| Versioned memo | [memo model](../../memo/model.py), [memo routes](../../server/memo_routes.py) | MemoSection, labelled operator text, evidence drilldown and version selector. Respect line audience and version-specific evidence. |
| What-if assumptions | [reader scenarios](../../docs/ongoing/roadmap/reader-scenarios.md), [financial model](../../docs/ongoing/roadmap/financial-model.md) | Sliders, selects and toggles are a later surface. Both roadmap items remain not started; rendering a slider does not implement deterministic recomputation or isolated reader copies. |

The domain `Panel` currently carries columns and string rows. It can render a table, but cannot safely describe slider bounds, input validation, semantic units or action permissions. Those need explicit typed metadata rather than parsing values out of table text.

## Integration boundaries

1. **Python owns evidence and computation.** Existing Claim, Readout, request and Memo outputs stay authoritative. Emit progress/completion events at meaningful scan, intake and revision boundaries when real execution is added.
2. **Shared presentation contract.** Define a versioned catalog and allowlisted actions alongside domain contracts. Reuse domain IDs and evidence references. Keep generated Python contracts generated; UI definitions are an additive contract, not hand edits to exported types.
3. **RPC owns presentation and action routing.** Translate domain snapshots/events into validated UI specifications and state updates. Initial saved snapshots can be mapped deterministically. Selected named actions invoke existing domain operations after validation; no arbitrary URLs, code or model-invented backend operations.
4. **Mobile owns native implementations.** Wrap the existing [Card, Field, Action and theme primitives](../../apps/mobile/src/readout/ui.tsx), evidence views and request controls in a renderer registry. Retain native navigation, keyboard/focus behavior and list virtualization.

The RPC gateway is currently read-only: [server middleware](../../apps/rpc/src/server.ts) rejects non-GET requests, and its router exposes queries rather than subscriptions or mutations. The [Python gateway proxy](../../server/trpc_routes.py) buffers the upstream body and uses a 30-second timeout. The mobile [REST adapter](../../apps/mobile/src/readout/proxy.ts) has a fixed route allowlist and does not expose a UI-stream route. A native renderer cannot be connected to these endpoints unchanged and expected to stream.

Proposed transport: a dedicated framed stream for UI descriptions/state updates, plus typed action submissions. Evaluate SSE or JSONL on the installed Expo runtime, through the real physical-device proxy path. Preserve the existing local-only boundary; adding actions must not simply remove the GET guard. If the stream passes through Python, make that proxy streaming-aware; otherwise route it through a deliberately supported Expo-to-RPC path.

Each stream should identify company, run, surface, catalog version and sequence. On reconnect, resume supported events or replace from a current snapshot. Ignore updates from an obsolete run or company. Preserve edited inputs and focus when unrelated results arrive. Reject unsupported component/action names and malformed updates, retaining the last valid view. Stable identity and explicit request/version checks matter more than token-by-token animation.

## Library findings

| Candidate | Verified capability | Fit for Tricorder |
| --- | --- | --- |
| [json-render native](https://json-render.dev/docs/api/react-native) | Native registry, bound input controls, providers and `useUIStream`; [SpecStream](https://json-render.dev/docs/streaming) uses JSONL patches. | First trial: generated sections and forms inside the existing working page. Wrap the product's own domain components. |
| [assistant-ui native generative UI](https://www.assistant-ui.com/docs/react-native/generative-ui) | Native spec rendering in a conversational runtime with state bindings and forms. Some controls adapt: Slider is a stepper, DatePicker a text field, charts render as bars. | Better candidate if steering becomes a chat/thread experience. Do not assume web widget parity. |
| [wireai-rn](https://github.com/chohra-med/wireai-rn) | Native component registry, Zod validation, streaming and a custom-backend webhook adapter. | Worth a smaller alternative trial. Verify the actual pinned artifact and dependency requirements; available repository/docs snapshots disagree on versions. |
| [A2UI](https://github.com/a2ui-project/a2ui/blob/main/specification/v1_0/docs/a2ui_protocol.md) | Transport-independent component/data-model messages and separate user actions. The inspected v1.0 document is a candidate specification. | Useful protocol reference for surfaces, catalogs, actions and state. Do not make another protocol adapter a prerequisite for the first native slice. |
| [Official json-render Expo example](https://github.com/vercel-labs/json-render/tree/main/examples/react-native) | Official example of json-render in Expo. | Reference implementation, not an additional renderer dependency. The exact separately named “Expo JSON Render” resource was not supplied. |

Compatibility remains unverified. The inspected json-render native [main-branch manifest](https://github.com/vercel-labs/json-render/blob/main/packages/react-native/package.json) requires Zod 4; the local RPC package pins Zod 3.25.76. Its declared React/RN peer ranges include this app's versions, but ranges are not runtime proof. The [example manifest](https://github.com/vercel-labs/json-render/blob/main/examples/react-native/package.json) targets Expo 54 and RN 0.81.4; this checkout uses Expo 58 and RN 0.88.0. Pin and test a published version before adopting it, and isolate UI-catalog Zod dependencies or plan a deliberate migration rather than upgrading the gateway incidentally.

## First vertical trial

Use the request behavior in ticket 02 as the test surface, with ticket 01's stable company identity. A saved-data backend sends a valid request section; Expo renders native controls; the associate changes selection and text; a named action saves the request; a subsequent saved evidence update changes one item's status without losing an unsaved custom input. The last update is fixture replay, not proof of file ingestion.

Acceptance evidence should include a native device walkthrough, contract rejection checks, restart persistence, disconnected/reconnected stream recovery, late-event company isolation and retained edits/focus. Only after that works should the catalog expand to the arrival/readout surfaces in tickets 03/04 and memo sections in 05.

No dependencies installed or runtime code changed for this assessment. Existing tickets retain their approved scope and blocking edges.
