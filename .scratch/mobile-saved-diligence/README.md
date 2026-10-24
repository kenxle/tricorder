# Mobile saved diligence

Created 2026-10-24 for Benjamin using the approved five-ticket breakdown. These are local tickets for iteration, not issues published to an external tracker.

## Milestone

An associate opens saved public research from a company URL, prepares a request, reviews a clearly labelled synthetic room as evidence arrives, and opens a sourced memo on mobile. Sazabi is the primary demo company; Ploy is the second case.

Benjamin explicitly selected saved public research and synthetic rooms for the first milestone. Fresh research for unfamiliar URLs is outside this milestone.

**Room implementation boundary:** following Benjamin's instruction to do the remaining ticket 03 work, this milestone uses saved, contract-valid room replay through the application API. Real server ingestion is independently verified for existing rooms; Ploy/Sazabi lack analyzable source files and an ingestion mapping. Replay must not be presented as ingestion or a fresh analysis run.

## Tickets and frontier

| Ticket | Blocked by | Result |
| --- | --- | --- |
| [01: Open a saved company readout with traceable evidence](issues/01-saved-company-readout.md) | None | URL to sourced native readout through a shared contract |
| [02: Prepare and retain a company's request](issues/02-persistent-company-request.md) | 01 | Editable, persistent request and manually recorded sent state |
| [03: Review a synthetic room as it arrives](issues/03-synthetic-room-arrival.md) | 01 | Partial and full room states on the company working page |
| [04: Close requests against received evidence](issues/04-reconcile-received-evidence.md) | 02, 03 | Answered requests, outstanding requests and founder questions |
| [05: Read the company's saved memo on mobile](issues/05-saved-memo-reader.md) | 03 | Versioned memo with line-to-claim-to-source navigation |

Ticket 01 is implemented and verified locally, with the user-approved company carousel retained; see [its handoff](ticket01-handoff.md). Changes remain uncommitted. Ticket 03 replay is implemented, with the full native walkthrough outstanding; see [its handoff](ticket03-handoff.md). Ticket 02 can proceed independently. Ticket 05 need not wait for 04 or steering. `ready-for-agent` describes ticket readiness; it does not override blocking edges or an explicitly recorded open decision. Tickets 02, 04 and 05 remain unimplemented; ticket 03 still needs its final native acceptance check.

## Contract and verification boundaries

- Reuse existing Claim, Source, Piece, Readout, request and Memo contracts where their semantics fit. Add explicit shared company and lifecycle contracts where needed. Do not invent a room merely to represent pre-room research.
- The current RPC gateway provides queries; the mobile Rooms flow currently uses an Expo REST adapter. Integrate each slice through an explicit typed boundary without making a wholesale transport migration a prerequisite.
- Saved snapshots, authored demo insights and synthetic results retain provenance. Replay is not live research or proof of a scan run.
- Each ticket includes focused behavioral/contract verification and a native walkthrough. Passing a source check or web export alone does not establish native behavior.
- Preserve the existing working room flow while integrating the new company journey.

## Follow-up work to scope separately

- Actual synthetic-document ingestion and engine reruns, unless selected as a requirement for ticket 03.
- Fresh company research, source caching and independently completing research sections.
- Unrestricted steering with script-computed numbers preserved and durable revisions.
- Memo authoring, conflict handling and PDF export/share integration.
- Principal agree/disagree interactions, personal reader copies and script-backed what-if scenarios. Ken's 13:52 bulletin requests the principal review page; ticket 05 covers reading and evidence inspection only, not that full request.

See [JSON render implementation handoff](json-render-handoff.md) for the first integration and validation.

## Source decisions

- [Streamed native UI assessment](generated-ui-assessment.md): code map, library findings and a proposed request-dialog trial. Benjamin selected json-render; the request-dialog foundation is implemented in `packages/request-ui` and `apps/mobile/src/request-ui`. It is a partial foundation for ticket 02, not completion of request lifecycle persistence or the five-ticket milestone.

- [Latest prototype UI decisions](../../docs/features/20261024.02_first_steps_ui/02_ui_decisions.md)
- [Prototype](../../docs/features/20261024.02_first_steps_ui/prototype/index.html)
- [UX review](../../docs/ongoing/diagrams/ux_review.md), an earlier discussion draft; the later approved UI decisions take precedence where they differ.
- [Feature specification](../../docs/ongoing/FEATURES.md)
- [Room requests](../../docs/ongoing/roadmap/room-requests.md)
- [Memo template](../../docs/ongoing/MEMO_TEMPLATE.md)
- [Bulletin board](../../docs/BULLETIN.md)

Update the individual tickets as decisions change. Keep this dependency table synchronized, and mark completion only with recorded validation evidence.
