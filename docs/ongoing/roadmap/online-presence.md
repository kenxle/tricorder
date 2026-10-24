# online-presence

The company's footprint: web, Hacker News, Product Hunt, app stores, Reddit, Facebook.

- **Status today:** not started. Left: the company's footprint: web, Hacker News, Product Hunt, app stores, Reddit pages Ken saves.
- **Who builds it:** agent.
- **Waits on:** [outside-in](outside-in.md), for the company resolver, the cache and the Hacker News and Apple clients it builds; someone reads Reddit's rules (the feasibility research did not); a decision on Product Hunt, whose API terms say non-commercial use.
- **Horizon:** Now to Friday night
- **Checked against:** no scans/presence/.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The company's footprint: web, Hacker News, Product Hunt, app stores, Reddit, Facebook.

**Waits on:** [outside-in](outside-in.md), for the company resolver, the cache and the Hacker News and Apple clients it builds; someone reads Reddit's rules (the feasibility research did not); a decision on Product Hunt, whose API terms say non-commercial use.

**Includes:**

- Hacker News through Algolia and the Apple lookup, as in the feasibility research's 1.6.
- The Reddit mini-browser Ken described: a small browser pane in which Ken, signed in as himself, clicks Reddit links, and each page he opens is saved as JSON into the corpus. Agents never fetch reddit.com; the scan reads only what Ken saved.
- Facebook page text pasted by Ken.

**Done when:** on a real company Ken approved, the Hacker News and Apple results come back through outside-in's clients and cache; a Reddit page Ken opened in the mini-browser is saved as JSON and read by the scan; no test fetches reddit.com; and every claim passes the quote checker.

**Who:** agent.

**Judgment:** yes.
