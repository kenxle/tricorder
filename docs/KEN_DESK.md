# Ken's Desk

**What this is:** Ken's working page for the hackathon. The top holds what needs Ken now. Comment on any item, and Claude answers on the page and updates the work. Hacking ends at **4:30 PM**, the demo freezes at **3:30 PM**, and judging runs 4:30 to 6:00.

**Last updated:** 2026-10-24 11:08, from the [board](BULLETIN.md) through Ken's 11:05 post and the [roadmap](ongoing/ROADMAP.md).

## Notes

- Data room will need to send requests for more data
- customer testimonials are from b2b side
- b2c often want more info about traction (often social presence, not often strong enough)



### From the notes

- **Requests for more data:** built. The [founder-requests](ongoing/roadmap/founder-requests.md) slice drafts the message to the company asking for what the room is missing, with guidance on what to send.
- **Testimonials (B2B) and traction from social presence (B2C):** nothing checks either yet. The nearest slice is [online-presence](ongoing/roadmap/online-presence.md), not started. Say if these should become checklist items or part of that slice.

## Needs your call

Each item says who is waiting and what Claude recommends.

- [ ] **1. Who is on the team, and what each person builds.** So far on the board: Benjamin (the TypeScript port) and Tirth (tasks coming from Benjamin). Kimi is with you now. The roadmap's Saturday roles are captain, frontend, backend-and-data and design-and-finance. **Claude recommends** writing each person's name and area in the Notes, and Claude puts them in the Team table in [AGENTS.md](../AGENTS.md) and on the roadmap. *Waiting: everyone's agents, which assign work by role.*
- [ ] **2. GitHub access.** The repo is private. Benjamin already pushes. Tirth and Kimi need an invite to `kenxle/tricorder` (Settings, Collaborators) before their agents can pull. *Waiting: Tirth, Kimi.*
- [ ] **3. What runs at the 3:30 PM freeze.** Benjamin is porting to TypeScript; the Python version is the one that works today. **Claude recommends** the freeze runs whichever version passes the answer-key check at 3:30, with Python as the fallback. *Waiting: Benjamin ([board](BULLETIN.md), 11:01).*
- [ ] **4. The social post at 11:00.** The first post for the $150 social content prize. Drafts: [social-posts](ongoing/roadmap/social-posts.md). The second post is at 3:30.
- [ ] **5. The real YC companies for the live beat.** **Claude recommends Ploy and Sazabi.** Candidates: [research_demo_companies.md](reports/20261022.02_research/research_demo_companies.md). An agent builds their synthetic rooms once you pick. *Waiting: the outside-in and yc-rooms slices.*
- [ ] **6. API keys in `.env` on the demo laptop.** Anthropic first; then the sponsor keys that arrive today (Akta, Crunchbase, Nicrron). [keys](ongoing/roadmap/keys.md). *Waiting: cached-data, comps, market signals, outside-in.*
- [ ] **7. Ask the organiser to change the track and pitch.** The Team Match Network lists Tricorder as "sourcing, diligence" with the old pitch; only the admin can edit it.
- [ ] **8. Record the pitch video.** Read the Hollis Voice script flatly: [pitch_video_script.md](../data_room/hollis_voice/01_overview/pitch_video_script.md). Save it as `pitch_video.mp4` beside the script. *Waiting: the pitch-video slice, which uses the script until then.*
- [ ] **9. The founder brief in your words.** The one page the judges get: [founder-brief](ongoing/roadmap/founder-brief.md).

## Lower priority

Nothing waits on these; the code follows Claude's defaults until you say otherwise.

- The wave 1 and wave 2 defaults (board tasks TRI-wave1-defaults and TRI-wave2-defaults), including whether a figure only the company's own model states counts as support.
- Which Startup Due Dil ideas to adopt: [proposals](ongoing/roadmap/proposals.md).
- The 18 decision cards on the [plan overview page](features/20261022.01_hackathon_plan/00_overview.md).

## Where things stand

From the [roadmap](ongoing/ROADMAP.md), "Up next". Status counts are from [status_counts.py](ongoing/roadmap/status_counts.py).

| Area | Owner | State |
|---|---|---|
| Red flags in the numbers ([redflag-engine](ongoing/roadmap/redflag-engine.md)) | design-and-finance | Partly built. Several planted-flag checks still missing. |
| The readout ([readout](ongoing/roadmap/readout.md)) | captain | Partly built. Source linking, the ask list and connecting sentences left. |
| The page judges see ([readout-page](ongoing/roadmap/readout-page.md)) | frontend | Partly built. Claims and cohort panels, memo link, video jump left. |
| Pitch video ([pitch-video](ongoing/roadmap/pitch-video.md)) | backend-and-data | Not started. |
| TypeScript port ([typescript-port](ongoing/roadmap/typescript-port.md)) | Benjamin | Not started. Decided at 11:00. |
| Demo freeze ([demo-freeze](ongoing/roadmap/demo-freeze.md)) | captain | Starts at 1:00 PM. |

## Done

Newest first.

- 11:05: Board asks Benjamin to write tasks for Tirth.
- 11:01: TypeScript port set up for Benjamin: slice, roadmap section, team row, board message.
- 10:54: Roadmap reshaped: what to build next and who builds it; each slice in its own file.
- 10:10: AGENTS.md and the board work the way they did at the last hackathon.
