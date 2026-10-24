# Ticket 01 handoff

Implemented locally on 2026-10-24. Changes remain uncommitted alongside other sessions' work.

## Delivered

- Shared `@tricorder/schema/company` contracts represent saved public research without inventing a room. RPC serves overview and independently loaded sections through `/company/readout` and `/company/section`; Expo exposes fixed local adapters under `/api/company/`.
- Website and YC URLs resolve to Ploy or Sazabi. Unsupported companies show an explicit unavailable state. A checked manifest binds semantic evidence identities to exact saved source IDs and quotes. Authored insights, source qualifications and snapshot provenance remain visible.
- The Company tab opens `saved-readout-screen.tsx`: summary, What stands out, founders, comps, signals, outside evidence and request preparation. Sections load and retry independently. Company changes cancel old requests and reject mismatched section identities.
- Evidence sheets show saved passages and original links while retaining the mounted working page. Existing request editing and local draft persistence remain available. Sent/open/answered lifecycle work is not implemented.
- Benjamin explicitly approved retaining the concurrently added company carousel. Both card selection and URL deep links open the saved readout. Other sessions' details, annotations and styling changes remain intact.

## Validation

- RPC: 27 tests passed, including URL resolution, missing research, manifest/source integrity and HTTP boundary checks.
- Mobile: 13 focused company, company-proxy and request draft/proxy tests passed. Mobile, RPC and schema typechecks passed. Root lint and scoped formatting passed.
- Android, iOS and web exports passed.
- iPhone 17 Pro simulator, iOS 26.5: opened Ploy and Sazabi; inspected Ploy pricing evidence and Sazabi YC evidence; dismissed evidence back to the same company; inspected light and dark evidence layouts. Armature's YC URL displayed “Saved readout unavailable” and no substituted company research.
- Chrome preview: Sazabi sections rendered, a round claim opened the saved seed-blog passage, and closing it returned to the round/team area.
- Three independent read-only reviews of a stable implementation snapshot found no actionable correctness, security or complexity defects. Subsequent entrance changes retain the user-approved carousel.

## Remaining boundaries

No Android runtime or physical-device walkthrough was performed. Precise deep-scroll restoration was checked in the browser, not independently measured on native. The concurrent carousel and legacy provider still bundle the prototype fixture; this is not a claim that all bundled company data was removed. Fresh research, room arrivals, request lifecycle persistence and memo reading remain outside ticket 01.

Ticket 03's dependency on ticket 01 is satisfied locally. Its written replay-versus-real-ingestion decision remains unresolved. Ticket 02 can proceed independently of that decision. Tickets 02 through 05 are not complete.

Upstream was fetched, but local bulletin edits prevented merging. Existing local changes were preserved; nothing was committed or pushed.
