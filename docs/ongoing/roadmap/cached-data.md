# cached-data

The outside data the comps and market-signal scans read on Saturday, saved as files, so nothing on stage waits on a live call.

- **Status today:** not started. Left: save every outside call under cache/.
- **Who builds it:** Benjamin (Ken, 11:33 AM), from the [brief](../../features/20261024.01_pre_room_diligence/00_brief.md).
- **Waits on:** keys (Akta and Tavily for the signal pulls; the EDGAR User-Agent for the SEC downloads); Ken's approved list in yc-rooms, for the real companies' calls.
- **Horizon:** Now to Friday night
- **Checked against:** no cache/ folder.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The outside data the comps and market-signal scans read on Saturday, saved as files, so nothing on stage waits on a live call.

**Waits on:** keys (Akta and Tavily for the signal pulls; the EDGAR User-Agent for the SEC downloads); Ken's approved list in yc-rooms, for the real companies' calls.

**Includes**, from the feasibility research's 1.2, 1.3 and 1.6:

- The last four Form D quarterly zips.
- XBRL company facts for 8 to 12 public companies near the demo company's space.
- 10 to 20 Form D rounds chosen by hand as private comps.
- 3 to 5 real competitors in voice AI for vet clinics, with every Akta signal the key allows and their pricing pages through Tavily.
- Hacker News and app-store results for one or two of those competitors, run by hand.
- Each comp candidate's 10-K Item 1 text, which the comp prompt (2.1) reads.
- A saved page describing each Form D issuer, which the private-comp prompt (2.2) reads.
- `cache/index.json`, which maps each URL to its saved file. The quote checker reads it to check URL sources.
- For each real company Ken approves in [yc-rooms](yc-rooms.md), its own outside-world calls: its website, Hacker News, Apple's App Store lookup and SEC EDGAR, plus Akta and Tavily where the keys allow. Each call is saved with its request (the endpoint and its parameters, never the key) in `cache/index.json`, so Saturday's live run can send the same calls again and fall back to these copies.
- Everything under `cache/` at the repo root, with the date each file was read.

**Done when:** each file opens, and a short `cache/README.md` lists what each file is and where it came from.

**Who:** agent, with Ken for anything behind his keys.

**Judgment:** no.
