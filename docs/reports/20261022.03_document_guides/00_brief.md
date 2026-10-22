# Brief: a reference guide for every data-room document

Written 2026-10-22 at 2:38 PM for the research agents writing the document guides. Read this file first, then the files it names.

## What Ken asked for

As a comment on the 30-document table in the data-room research, 2:38 PM:

> ok this is a great list and we're focusing on seed and series a so we need to have custom reference documents written for every single one of these. we will need to send out research agents to uncover the pitfalls and red flags and green flags for each of these documents

So: one guide per document a seed or Series A data room can hold. Each guide is the reference Tricorder's scans, the checklist and the memo draw on for that document.

## Read before you start

- `docs/features/20261022.01_hackathon_plan/00_brief_for_writers.md`: the rules section and every Added block from 12:55 PM on. They are Ken's decisions. Most important here: the readout's pieces (traction and revenue, retention, burn and runway, unit economics, customers and contracts, market, comps, team, the pitch itself, legal and cap table, outside world) and their strong or weak verdicts; green flags matter as much as red; Tricorder finds differences in reporting, never claims to detect fraud; accounting mislabels and contract terms; the ask list; online research only; no research codes like R1 in prose; the primary personas are the associate who prepares the memo and the partner who reads it, at seed and Series A funds.
- `docs/reports/20261022.02_research/research_data_room.md` (the 30-document table, Part 2 red flags) and `docs/reports/20261022.02_research/what_is_a_data_room.md`.
- `docs/ongoing/CHECKLIST.md` and `docs/ongoing/FRAMEWORKS.md` (headings): which checks already exist, so each guide names them.
- `docs/reports/20261022.02_research/research_voice_of_customer.md` and `research_gaps.md`: investor quotes already collected and verified. Reuse them with their links before searching again.

## One file per document

Write `docs/reports/20261022.03_document_guides/<slug>.md` for each document in your group, slug in lowercase with hyphens. Sections, in this order:

1. **What it is.** Two or three sentences: what the document holds, who prepares it, what form it usually arrives in.
2. **At seed and at Series A.** Whether it is expected, lighter or absent at each stage, and what changes between them (from the research table, then your sources).
3. **What a first pass checks.** The questions an associate asks of it, in order.
4. **Green flags.** What makes it look strong, each with a source.
5. **Red flags and pitfalls.** What goes wrong, what founders get wrong, what investors regret missing, each with a source. Mark the common ones and the rare but serious ones.
6. **How Tricorder checks it.** Three lists: what a script can check (name the existing FRAMEWORKS check where there is one, or propose a check name and its formula); what needs a model to read (and what it must quote); what Tricorder cannot check and must leave to the operator (a bank call, a reference call, a lawyer).
7. **Which readout pieces it feeds** and which checklist items it covers.
8. **If it is missing.** Whether a missing copy is a gap or a red flag at each stage, and the one-line ask-list request for the founder.
9. **In the Hollis Voice room.** Whether the synthetic room (data_room/README.md, data_room/answer_key.json) holds it, what it shows, and any planted flag or green flag in it. "Not in the room" is a fine answer.
10. **Sources.** Every page you used, as links, each saved under `docs/reports/20261022.03_document_guides/raw/<slug>/`.

Length: what the document deserves. A cap table or a financial model gets more than a cover note.

## Rules

- Online research only. Use WebSearch and WebFetch, or curl. Fund blogs, VC newsletters and podcasts with transcripts, law-firm and accounting-firm guides (Cooley, Kruze, Carta, Fenwick, Wilson Sonsini, Gunderson, Orrick), accelerator guides (YC, Techstars), angel networks, Hacker News through the Algolia API. Vendor posts are allowed and marked as vendor views.
- WebFetch can invent text. A quote goes in only after you have checked it word for word against the page text you saved, by script.
- A quote attributed to a real person needs a link to that person's own words right after it. No link, no quotation marks; paraphrase instead and say whose view it is.
- Never fetch reddit.com. If Reddit would help, end the guide with a short list of Reddit `.json` URLs (full `/r/<sub>/comments/<id>.json` form) for Ken to save.
- Pages that block automated fetching (HTTP 403): list them in your reply; the orchestrator can read them through a browser.
- No numbers from your head. Counts come from a script.
- Plain words, one idea per sentence, no em dashes, no "leverage", "robust", "seamless", no research codes like R1.
- Write only your guides, their raw folders and your group's quotes CSV `quotes_<group>.csv` (columns: guide, kind quote or paraphrase, text, link, saved_file, verified yes or no). Do not edit any other file.
- Do not delete anything: no rm, rmdir, unlink, git clean or force flags. List any file that should go under "Cleanup needed" in your reply. Do not commit; the orchestrator commits.

## Reply

Under 200 words: the guides written, the most important red flag and green flag you found for each, pages that blocked you, and how many quotes you verified.
