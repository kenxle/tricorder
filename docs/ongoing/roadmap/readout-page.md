# readout-page

The web page the judges see.

- **Status today:** partly built. Left: wave 2 panels (claims table, cohort rebuild), memo link, video jump, ask-list copy button, reorder buttons, market-signals panel.
- **Who builds it:** frontend.
- **Waits on:** skeleton (the generated types and the server routes, written this week). From 10:30 it is built against the example files.
- **Horizon:** Saturday
- **Checked against:** readout/src/App.tsx shows top flags, overview, gaps, could not verify, ask list, source chips.

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Detail

The web page the judges see. The feasibility research calls the readout "the thing shown on screen".

**Waits on:** skeleton (the generated types and the server routes, written this week). From 10:30 it is built against the example files.

**Includes:**

- A React page in `readout/` that reads `readout.json` through the server.
- The best green flags and the worst red flags at the very top, green first, each line one click from its piece. A green flag gets the same size and the same source links as a red one.
- The overview under them: one row per piece, in a fixed default order, with its mark, its one-line reason and its counts of corroborating and contradicting sources. Strong and weak rows look the same size. This is the demo's first screen ([The one workflow we demo](demo_workflow.md)).
- One click on a piece opens its drill-down: its claims, with each conflict shown side by side. Inside traction and revenue, the four ARR figures sit in large type, each with its source chip. The comps panel sits in comps, the signals panel in market, and the video moments in the pitch itself.
- A footnote on every sentence. It opens the source as an in-page panel: a pre-rendered PNG of the slide or page, a small HTML table with the cited cell highlighted, the clause text, or the video at its second through the media fragment (`#t=35`). URL sources open their saved copy from `cache/`. A click never launches Excel or a PDF viewer: a spreadsheet app opening on a projector is slow, and it shows the associate the room's tidy rows ([critique_demo.md](../../features/20261022.01_hackathon_plan/critique_demo.md), finding 6). The panel also lists every other source that corroborates or contradicts the claim, each one click away.
- The video player beside the video claims; clicking a claim jumps to its start.
- A "could not verify" box, a gaps panel, and the score lines for this room, the sealed variant room and the clean room.
- The ask list at the end of the page, with a copy button, so the operator can paste it into an email to the founder.
- A switch between the seed drop and the full room.
- Up and down buttons on each overview row, so the operator can reorder the pieces ([PRODUCT_BRIEF.md](../PRODUCT_BRIEF.md), "The operator sets the order"). The order lives in the page only. Saving it, and a default order by stage, is the [stage-views](stage-views.md) slice, which an agent builds before Saturday. The frontend builds the buttons in the 2:30 to 3:30 PM polish hour. If that hour runs short, the demo shows the default order.
- Served from localhost, with no fonts or scripts from a CDN, so it needs no venue wifi.

**Done when:**

- The page renders `sample_out/` at 11:00 AM and the real outputs at 1:00 PM.
- A missing scan shows its gap panel, not a blank page or an error.
- Every footnote opens its source in the page.
- One click opens a piece's claims, and one more opens a claim's source with its corroborating and contradicting sources.
- Moving a piece up or down keeps its mark, its claims and its links, and a reload shows the default order.

**Who:** frontend.

**Hours:** 4.25 (10:30 AM to 3:30 PM, less lunch and the quarter hour for the [market-signals](market-signals.md) panel).

**Judgment:** yes.
