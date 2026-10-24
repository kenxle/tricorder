# Promo shot list: Tricorder, 45 seconds

**Status:** Draft for Ken's review, 2:45 PM. Building the video from this now; edit the table and the next render follows it.

**Summary.** Three drawn shots on the problem (ten tabs open, days of gathering, numbers that disagree), then five shots of the real prototype on Sazabi (paste a URL, first readout, data-room request, flags from the room, partner memo with chat), then the close: "Point it at a startup, get a readout." Problem 0:00 to 0:15, solution 0:15 to 0:40, close 0:40 to 0:45.

## Shot list

Nine shots, 45 seconds, 100 spoken words (counted by [word_count.py](word_count.py) from [vo.py](vo.py)). Drawn shots use the [style guide](../../ongoing/STYLE_GUIDE.md): Black Card dark, Archivo and IBM Plex Mono, champagne metal for thin lines, green for strong, coral for weak.

| # | Time | What is on screen | On-screen text | Voiceover (words) | Source |
|---|---|---|---|---|---|
| 1 | 0:00 to 0:05 | Drawn. A browser window. Tabs open one by one until there are ten: Website, Traffic, Reviews, Investors, LinkedIn, Crunchbase, SEC EDGAR, Hacker News, Press, Pricing. | Quote: "Before I even open your data room, I already have ten tabs up." Attribution under it: Associate at a seed-focused fund, Startups Magazine, Jan 2026. | Before an associate opens a data room, they already have ten tabs open. (13) | [Startups Magazine, Jan 2026](https://startupsmagazine.co.uk/how-to-build-a-data-room-that-closes-the-deal), via [PERSONAS.md](../../ongoing/PERSONAS.md) (the associate) |
| 2 | 0:05 to 0:10 | Drawn. A large figure counts up to 118. Under it, a quote card. | "118 hours of diligence per deal, on average." Attribution: Survey of 885 VCs, NBER, 2016. Quote: "The information I need isn't usually there, leading to back-and-forth emails with founders." Attribution: Founder turned investor, Elite Game Developers, Aug 2024. | Days go to gathering, before any thinking starts. (8) | [NBER working paper w22587](https://www.nber.org/system/files/working_papers/w22587/w22587.pdf); [Elite Game Developers, Aug 2024](https://elitegamedevelopers.substack.com/p/the-essential-startup-data-room-key). Both from [research_gaps.md](../../reports/20261022.02_research/research_gaps.md), "Which part is slowest". 118 hours is all diligence on a deal, not the first pass alone, so the text says "per deal". |
| 3 | 0:10 to 0:15.5 | Drawn. Three cards: The deck, The model, The books. Each has a revenue bar of a different length (no figures). A Disagreement mark lands between them. | Quote: "When burn or revenue differs between the deck, the model and the accounting records, the gap suggests carelessness or something worse, and either reading damages the deal." Attribution: Seed fund guide, CRV, Aug 2026. | And when the deck, the model and the books disagree, it damages the deal. (14) | [CRV, What is a data room, Aug 2026](https://www.crv.com/content/what-is-a-data-room), via [PERSONAS.md](../../ongoing/PERSONAS.md) (the partner) |
| 4 | 0:15.5 to 0:19 | Real prototype, start page. "https://www.sazabi.com/" types into the URL box. | Caption: "Paste a company's website." | Tricorder starts from a company's website. (6) | Prototype capture, `index.html` |
| 5 | 0:19 to 0:24.5 | Real prototype, the first readout for Sazabi: What stands out, then the evidence tip on one point. | Caption: "A first readout from public sources. Every point shows its evidence." | It reads public sources and writes a first readout. Every point names its source. (14) | Prototype capture, gallery steps 02 and 03 |
| 6 | 0:24.5 to 0:28.5 | Real prototype, the data-room request dialog with the draft email. | Caption: "The data-room request, drafted for the associate to send." | Then it drafts the data room request. (7) | Prototype capture, gallery step 04 |
| 7 | 0:28.5 to 0:35.5 | Real prototype, the room in full: green and red flags lead. Then a red flag's stated-beside-found box. The synthetic-room note stays visible, and a label sits in the corner throughout. | Caption: "The room arrives. Red and green flags lead, stated beside found." Corner label: "Synthetic data room, written by the team for the demo." | When the room comes in, red and green flags lead: what the founder stated, beside what the room shows. (19) | Prototype capture, gallery steps 07 and 08 |
| 8 | 0:35.5 to 0:40.5 | Real prototype, the partner view: the memo on the left, the chat on the right with an answered question. | Caption: "The partner reviews an interactive memo, and asks it questions." Corner label as shot 7. | The partner reads an interactive memo, and can ask it questions. (11) | Prototype capture, gallery step 11 |
| 9 | 0:40.5 to 0:45 | Drawn close. The Tricorder wordmark on graphite, a champagne hairline, the line under it. | "Tricorder" / "Point it at a startup, get a readout." / "First-pass diligence for seed and Series A funds." | Point it at a startup, get a readout. (8) | Ken's close line |

## What a viewer might take as more than the prototype does

- **The research is pre-gathered.** The first readout for Sazabi comes from public sources the team fetched and saved ahead of time. The progress lines replay that work; a company outside the saved list shows "Research not cached".
- **The data room is synthetic.** The team wrote Sazabi's room for the demo. Shots 7 and 8 carry a label saying so, and the prototype's own note is in frame.
- **The room arriving is simulated.** The founder's reply comes as a notification in the prototype, not from a real inbox.

## Files

- [vo.py](vo.py): the voiceover lines, timing and TTS call. [word_count.py](word_count.py) counts them.
- [promo.html](promo.html): the drawn scenes and the frame around the real captures. [capture_app.py](capture_app.py) takes the prototype screens; [capture.js](capture.js) records the frames.
- [music.py](music.py), [render.sh](render.sh): the score and the final mix and render.
