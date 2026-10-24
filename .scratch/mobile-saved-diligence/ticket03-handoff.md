# Ticket 03 handoff

Implemented saved synthetic room replay on 2026-10-24. Final native full-stage/evidence acceptance remains outstanding.

## Delivered

- Shared `company-room` contract and validated RPC `/company/room` endpoint, exposed by a fixed local Expo adapter.
- Deterministic partial/full arrivals for Ploy and Sazabi with company-qualified room, arrival, file and claim identities. Partial responses withhold findings dependent on later files, including comparison sources. Full responses retain unresolved gaps.
- Explicit replay controls and pending arrival notices on the existing working page. Opening a notice reveals strengths, major flags, corroborations, arrived files and named missing files. Findings and evidence sheets clearly identify synthetic replay and distinguish public sources.
- Per-company, per-snapshot MMKV progress retains pending and opened stages across reopening. Duplicate and older replays cannot regress the opened room. New snapshots start independently without deleting previous progress. Failures preserve successful findings and offer retry.
- Existing real file ingestion and the carousel are preserved. No dependencies added by this ticket.

## Ingestion audit

The existing server intake is functional for existing rooms. `.venv/bin/python -m pytest server/tests/test_founder_requests_routes.py founder_requests/tests/test_intake.py` passed 58 tests, using temporary directories and offline mode. Tests exercise actual file writes, subprocess scan reruns, rebuilt readouts and persisted receipts.

Ploy/Sazabi have no analyzable room files or company-to-room ingestion mapping. Intake expects supported canonical inputs; accepting an extension does not imply arbitrary content can be analyzed. Existing intake is append-only and can save a replacement beside the canonical original. Expo's Rooms adapter exposes copy/batch but not receipt history. This replay implementation does not claim to fix those separate ingestion boundaries.

## Validation

- 38 RPC tests passed, including seven room fixture tests and two room HTTP tests.
- Latest mobile suite: 42 tests passed, including five arrival-state tests and five company-proxy tests. Mobile, RPC and schema typechecks passed.
- Android/iOS/web exports passed before the snapshot-recovery follow-up. Follow-up state tests, mobile typecheck and scoped lint passed. Final root lint and diff whitespace checks passed after concurrent formatting settled.
- Three independent reviews used a stable snapshot. The snapshot-refresh recovery finding was fixed and re-reviewed by all three; no actionable findings remain.
- Chrome: Sazabi partial arrival, supporting source quotes, pending full arrival across reload, opening full, replaying older partial without regression, outage preserving full findings, retry after recovery, and separate Ploy full arrival all verified.
- iPhone 17 Pro simulator on iOS 26.5: Sazabi partial notice, partial findings with waiting files, and reopening preserved progress verified. Shared simulator screen changes and automation interruptions prevented a reliable full-stage and major-flag evidence-sheet walkthrough. These native checks remain open. Android runtime and physical-device checks were not performed.

## Delivery and remaining work

Another authorized delivery session captured the initial replay implementation in `dafa30f` during this work. Snapshot-recovery changes and this handoff were left for review; this session did not commit or push. Preserve concurrent staged and unstaged work.

Ticket 03's final acceptance item remains unchecked until a stable native walkthrough covers partial/full arrivals and opens a major flag's source. Tickets 02, 04 and 05 remain separate work. Prototype replay is not live ingestion, fresh research or newly computed analysis.
