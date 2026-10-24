# 01: Open a saved company readout with traceable evidence

**What to build:** An associate enters Sazabi's or Ploy's website or YC URL and immediately opens its saved public research as a native working page. A sourced summary and insight cards lead into founders, comps, market signals and outside-world evidence. Every evidence reference opens an inspectable passage without losing the reader's place.

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [ ] Website and YC URLs resolve to a stable company identity through the application API and a shared contract. Unsupported companies show an explicit unavailable state without substituting another company's research.
- [ ] Before replacing the current company data import, expose and validate the saved fixture through the shared boundary. Reuse existing claim and source semantics where applicable; represent company identity and pre-room sections explicitly without fabricating a room.
- [ ] The working page follows the latest approved hierarchy: company summary, What stands out, founders, comps, market signals, outside world, then Up Next: Data Room Requests. There is no setup screen, editable setup form, batch field or prototype navigation in this journey.
- [ ] Insight and summary references resolve by stable evidence identity rather than matching prose or relying on array positions. Saved or authored content retains its provenance and snapshot date.
- [ ] Tapping an evidence number or source control opens the associated passage, source identity and original link where available. Saved passages remain readable without external internet access while the local application service is available.
- [ ] Sections support loading, available, empty and failed states independently. Skeletons reflect actual loading; missing evidence and placeholders do not become verified findings.
- [ ] Native layout preserves readable figures and accessible source controls in both themes. Returning from evidence restores the working-page context.
- [ ] Focused tests cover URL identity, missing fixtures and evidence-reference integrity. A native walkthrough verifies both demo companies, one missing-data case and source navigation; record the platform and result.

Live research and request persistence are outside this ticket. Preserve the existing Rooms journey while introducing the shared company boundary.
