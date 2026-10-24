# UI decisions from Ken's prototype review

Ken reviewed the [prototype](prototype/index.html) live on 2026-10-24 from 12:00 to 1:50 PM. These are his decisions, for the web app and the mobile app alike. Ken, 1:49 PM: "we've done a lot of ui updates to make this more readable. make sure they get into the mobile version as well". The prototype is the reference: open `prototype/index.html?company=https://www.sazabi.com/`.

## The whole product

- **It looks like the product, not a prototype.** No step bars, no "step N", no back links, no "prototype" labels. The top is the product's own bar: the Tricorder name and a box to paste a company URL.
- **The style is direction E in Archivo** ([STYLE_GUIDE.md](../../ongoing/STYLE_GUIDE.md), stylesheet `docs/ongoing/style/tricorder.css`).
- **No explainer lines.** Ken deleted every line that explained what the screen does ("Built from public sources", "Every fact Tricorder found…", "Matched by domain…"). The UI makes it clear.
- **The demo company is Sazabi.** Ploy is a second case.

## Starting a company

- The start screen asks **"Diligence on whom?"** with one box for a company URL (its website or its YC page). No list of companies.
- A URL in the address bar opens a company directly.
- **Setup is automatic.** No setup screen and no editable fields: dropping in the URL starts the research. There is no batch field (not every company is YC).

## The working page (the readout)

The readout is the associate's working page for the company. Top to bottom:

1. **The company name, then a short paragraph** on what the company does, with links to the facts behind it.
2. **What stands out:** insight cards, not one fact per line. Each card has a mark (looking strong, looking weak, mixed, not enough yet), the piece it is about, a headline, two sentences, and "Based on" numbers that point at the evidence. Ken: "these are great actually".
3. **The founders, then comps, then market signals,** then the outside world facts last.
4. **Evidence is tables:** what we found in the first column, the source button in the second. Each fact has a number. Hovering a number anywhere shows the fact and its source.
5. **Up Next: Data Room Requests,** with the "Draft the data-room request" button inside that box.

- **Loading:** each section shows a skeleton until its data arrives, then fills in whole. No claim-by-claim animation.
- **A source button replaces any line that only says where something came from.**

## The data-room request

- It is a **dialog over the working page**, not its own screen: the checklist, add an item, guidance per document and the live draft.
- After "Mark as sent", the working page shows **Data room requests**: each item Open, with when it was asked.
- **The room arrives as a notification** on the working page ("Sazabi shared its data room · N files"). Opening it marks the items the room holds as Answered, each with its file; the rest stay Open. A second notification brings the rest of the files.
- **Founder questions** from flags sit in the same requests, under "Questions for the founder". Every "View in the request" link opens the dialog at that item.

## Once the room is in

- The working page keeps its shape, with the room merged in: What stands out leads with the room's flags; each piece gets its verdict; claims are marked "Confirmed by the room", "The room differs" or "Waiting on <file>". There is a partly-in and a fully-in state (`&room=partial`, `&room=full`).
- **Flag weighting:** two sources agreeing is a small green flag (one line, never leads); two disagreeing is a big red flag (ranked among the worst). Order: real strengths, then big red flags worst first, then small green flags.
- **Every big flag has one or two lines of small text** under its header saying why it matters.
- **Card titles are the piece name only** ("Burn and runway"); the rest goes in a subtitle.
- **The range strip only shows a number against a sourced normal band.** It is not used to plot stated against found.
- Money shows exact figures ($5.25M, not $5.3M).

## The memo for the principal

Ken, 2:14 PM: "this is interactive, so it cannot be a pdf. it needs to be what the associate was working on, but remove all the noise. the memo should explain what is going on and be drill downable, or steerable, but is more of a document about the company and its investing value".

- **The memo is interactive. There is no PDF.**
- **It is the associate's working page, distilled.** Same content, with the noise removed.
- **It reads as a document about the company and its investment case.** It explains what is going on.
- **Every statement drills down** to its flags and evidence.
- **The principal can steer it** with agree, disagree, ask and what-if.
- **No noise.** Nothing on the page is there only for the associate's working.
- **The associate sends the memo with a button.** The view then becomes the principal reviewing it.
- **The principal has a chat that helps them navigate the memo.** It answers by pointing to the statements and evidence in the memo. Benjamin is building this.

Ken, 2:14 PM: "we should have a button where the associate sends the memo, and then see the principal reviewing the memo. they should have a chat that helps them navigate the memo. benjamin is working on this".
