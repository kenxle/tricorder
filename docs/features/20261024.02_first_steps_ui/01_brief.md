# Short brief: the UI for the first steps of the demo flow

Written 2026-10-24 at noon, from Ken's note on his desk: "ok, let's make a UI for the first parts of the flow. we can do a quick briefing a la feature flow".

## Who it is for

- **The associate** at a seed or Series A fund who prepares the memo. They run Tricorder.
- **The judges** watching the demo at 4:30 PM. They see it once, on stage.

## Context

The [demo workflow](../../ongoing/diagrams/demo_workflow.md) starts before any data room: a real list of YC Spring 2026 companies, our own research, then the request for the room. Today the app opens on a dropdown of our sample rooms ([localhost:5173](http://localhost:5173/)), so none of that can be shown. The data is ready: 193 companies saved from YC's directory, and six of them researched, with their SEC, GitHub, Hacker News and App Store data saved ([what exists](../20261024.01_pre_room_diligence/00_brief.md#what-already-exists)).

## Problem

The associate's first pass starts before any data room, and they do it by hand.

- **They research the company before the room opens.** An associate at a seed fund opens ten browser tabs first: traffic, reviews, investors, co-founder issues, and whether the story matches what is online ([the associate persona](../../ongoing/PERSONAS.md#the-associate-who-spends-days-gathering), quoting [Startups Magazine, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal)).
- **Getting the information is the slowest part of diligence.** Investors name market research and chasing documents that have not arrived, not the writing ([research gaps, "Which part is slowest"](../../reports/20261022.02_research/research_gaps.md#which-part-is-slowest)). One investor: "The information I need isn't usually there, leading to back-and-forth emails with founders." ([syndicate lead, Aug 2024](https://elitegamedevelopers.substack.com/p/the-essential-startup-data-room-key))
- **The volume makes it worse.** The same associate reviews about 500 decks a year and goes deep on about 15 ([the associate persona](../../ongoing/PERSONAS.md#the-associate-who-spends-days-gathering)).

Tricorder today helps only after a room exists. It cannot do the ten tabs, and it cannot draft the first request for documents, so the associate still does the slowest part alone.

## Desired outcome

In a few clicks on stage, the associate goes from the YC list to a first readout on a real company, built from public sources with every claim sourced, and a drafted request for the data room that they can edit.

The screens, in order:

1. **The list.** YC Spring 2026 companies: name, one-line pitch, industry, team size. Search and filter. The researched six are marked.
2. **Set up the company.** Name, website, founders, batch, each with where it came from. The associate can correct a field, then starts the research.
3. **The first readout, before any room.** The research fills in by section, each failing alone: the outside world (website, Hacker News, App Store, SEC filings), the founders, comps and market signals. Every claim shows its source. What only a data room can answer shows as gaps.
4. **The data-room request.** The gaps and the stage's standard first-tier documents as a checked list. The associate unchecks, checks and adds items, and sees the drafted message with guidance per document.

Then the flow joins what is built: the room comes back, and the readout shows red and green flags.

## Known constraints

- **It looks like the existing app.** Use `apps/web/src/tokens.css` and the readout page's patterns. The [style guide](../../ongoing/STYLE_GUIDE.md) is not written yet.
- **Benjamin builds the real screens** in `apps/web/`, as part of [diligence before the data room](../20261024.01_pre_room_diligence/00_brief.md) and [room-requests](../../ongoing/roadmap/room-requests.md). This brief and its prototype settle what the screens show, so he builds once.
- **Every number and claim on screen comes from saved data**, so the demo runs with the wifi off.
- **A real company's data room is synthetic**, and the screens say so where a room appears.
- **LinkedIn is never shown as a source.** X is linked, not read.
- **The demo freezes at 3:30 PM.**

## Open questions that affect the prototype

- **Which companies.** The prototype uses Ploy and Sazabi, the research's picks, until Ken chooses ([research_demo_companies.md](../../reports/20261022.02_research/research_demo_companies.md)).
- **One page or steps.** The prototype shows the four screens as steps with a back link; one long page is the alternative.
- **Live or instant.** On stage, does the research appear to run section by section, or is it simply there? The prototype shows sections filling in, with a setting to show them at once.

## Product thinking

The job: an associate wants a first view of a company before asking the founder for anything, because a founder's room arrives late and they need to know what to ask for. The evidence is the associate quoted in [outside-in](../../ongoing/roadmap/outside-in.md), who has ten tabs open before opening any data room, and Ken's workflow. Building these screens now is the priority because without them the demo starts in the middle of the workflow. The alternative, demoing only the data-room half, is what we have today and skips Ken's framework's first steps.

## The prototype

A clickable HTML prototype of the four screens, with real data for Ploy and Sazabi from the saved files: [prototype/](prototype/). Its review will be recorded here.
