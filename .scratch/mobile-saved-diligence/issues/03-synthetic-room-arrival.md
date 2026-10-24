# 03: Review a synthetic room as it arrives

**What to build:** An associate reviews partial and full synthetic room arrivals on the same company working page. The page shows what arrived, which findings are now supported or contradicted, and which conclusions still wait on evidence. Room flags and public research remain distinguishable and traceable.

**Dependency:** 01: Open a saved company readout with traceable evidence, satisfied by the locally implemented and verified ticket 01. No dependency on ticket 02.

**Status:** implemented; full native arrival/evidence walkthrough remains outstanding. See [validation and handoff](../ticket03-handoff.md).

**Implementation boundary:** Benjamin asked to “do the rest” after the proposed replay scope was explained on 2026-10-24. Proceeding with saved-result replay through the API. Actual ingestion works for existing server rooms (58 focused intake/route tests passed), but Ploy/Sazabi still have no analyzable room files or company-to-room ingestion mapping. The existing Rooms ingestion journey is preserved. Replay does not claim to run that ingestion path.

- [x] Saved partial and full results for both demo companies validate against the shared room/readout contracts, with an explicit company-to-room association and stable claim, file and arrival identities.
- [x] A reproducible demo action or replay fixture produces an arrival notice through the application boundary. The UI does not invent arrivals on a timer or claim a founder actually sent files.
- [x] Opening an arrival updates the same working page and exposes the received evidence. Reopening or replaying the same arrival does not duplicate files or findings; an older arrival cannot regress a full room to partial.
- [x] Partial state shows only findings supported by arrived evidence. Missing support is shown as waiting on named files; full state reveals the remaining saved findings. State survives reopening the company.
- [x] Cards preserve the approved ordering of real strengths, major red flags and small corroborations. Major flags explain why they matter; titles use the piece name, figures remain exact, and any normal band has a source.
- [x] Every displayed flag resolves to supporting claims and readable saved evidence. Public research stays distinguished from invented room evidence, with the synthetic notice present on readout and evidence views.
- [x] Failure to load a new state preserves the last successful state and offers retry. Switching companies cannot display another company's pending arrival or results.
- [ ] Contract and behavioral checks cover partial/full evidence availability, repeat and out-of-order arrivals, provenance and company isolation. A native walkthrough verifies both stages and opens the source for a major flag.

This ticket can be demonstrated without preparing a request. Request reconciliation is ticket 04. Replay must never be reported as successful ingestion or a fresh analysis run.
