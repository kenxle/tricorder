# 03: Review a synthetic room as it arrives

**What to build:** An associate reviews partial and full synthetic room arrivals on the same company working page. The page shows what arrived, which findings are now supported or contradicted, and which conclusions still wait on evidence. Room flags and public research remain distinguishable and traceable.

**Blocked by:** 01: Open a saved company readout with traceable evidence.

**Status:** ready-for-agent

**Open implementation decision:** This ticket is drafted for saved-result replay through the API. Confirm that boundary before implementation. If actual file ingestion and engine reruns are required, revise this ticket and its blocking edges first. The prototype's Ploy/Sazabi room objects are not existing analyzable room files.

- [ ] Saved partial and full results for both demo companies validate against the shared room/readout contracts, with an explicit company-to-room association and stable claim, file and arrival identities.
- [ ] A reproducible demo action or replay fixture produces an arrival notice through the application boundary. The UI does not invent arrivals on a timer or claim a founder actually sent files.
- [ ] Opening an arrival updates the same working page and exposes the received evidence. Reopening or replaying the same arrival does not duplicate files or findings; an older arrival cannot regress a full room to partial.
- [ ] Partial state shows only findings supported by arrived evidence. Missing support is shown as waiting on named files; full state reveals the remaining saved findings. State survives reopening the company.
- [ ] Cards preserve the approved ordering of real strengths, major red flags and small corroborations. Major flags explain why they matter; titles use the piece name, figures remain exact, and any normal band has a source.
- [ ] Every displayed flag resolves to supporting claims and readable saved evidence. Public research stays distinguished from invented room evidence, with the synthetic notice present on readout and evidence views.
- [ ] Failure to load a new state preserves the last successful state and offers retry. Switching companies cannot display another company's pending arrival or results.
- [ ] Contract and behavioral checks cover partial/full evidence availability, repeat and out-of-order arrivals, provenance and company isolation. A native walkthrough verifies both stages and opens the source for a major flag.

This ticket can be demonstrated without preparing a request. Request reconciliation is ticket 04. Replay must never be reported as successful ingestion or a fresh analysis run.
