# The demo

## Charter

**What belongs:** The Saturday demo. What is shown, in what order, on which rooms, and with what fallbacks.

**What does not:** How features work ([FEATURES.md](FEATURES.md)). The build plan and hours ([ROADMAP.md](ROADMAP.md)). The pitch wording and answers to judges ([BRAND.md](BRAND.md#pitching-to-judges)).

**Sources:** [the rooms](../../data_room/README.md), [the YC companies research](../reports/20261022.02_research/research_demo_companies.md), [the overview page](../features/20261022.01_hackathon_plan/00_overview.md).

## The framework

The demo follows the [demo workflow](diagrams/demo_workflow.md), Ken's framework for what Tricorder builds (2026-10-24, 11:15 AM): a real list of YC Spring 2026 companies, our own models and internet research, requests to the company for data room information, red and green flags from the room, the associate's cross-referencing and steering, and the interactive memo the principals end with. Where the beat sheet below differs, the workflow wins until the beat sheet is redone.

## The rooms

Every data room is synthetic, as the organisers require.

- **Hollis Voice, Series A.** An invented phone agent for vet clinics, raising $9,000,000. 17 files, eight planted red flags, three decoys, three green flags ([answer_key.json](../../data_room/answer_key.json)). Five flags show from its 12-file seed drop. The core runs here.
- **Brasswick, seed.** An invented freight-invoice company, raising $3,000,000. 14 files, five red flags of other kinds ([answer_key_brasswick.json](../../data_room/answer_key_brasswick.json)). No beat yet; keep its readout in a tab for seed-stage questions.
- **The sealed variant and the clean room**, both Hollis Voice. Someone outside the build picks the variant's flags and seals its key until the 3:30 PM freeze ([SEALING.md](../../data_room/SEALING.md)). The clean room has no flags.
- **Real YC companies with fake rooms.** Spring 2026 YC companies, each with an invented room. Their public footprint is read live. No room is built until Ken picks (see the open choices).

**The safeguard.** A room under a real name must never read as a claim about that company.

- Every page and sheet says "Synthetic test document. Not this company's data.", and so does a banner on the readout. Invented companies' rooms say "Synthetic data room for Deal Flow NYC 2026. Not a real company."
- The room repeats any number the company has published. Plants sit between two invented documents, never against a public fact.
- Each plant shows as a named test plant, and Ken says so out loud.

## The beat sheet

A three-minute core, then the extension if the slot is five minutes. Ken presents and the frontend drives. Hollis Voice's readout is open before he starts. A hidden tab starts the sealed variant run at 0:00. A second tab holds the real company's readout.

| Time | On screen | The line | Fallback |
|---|---|---|---|
| 0:00 | Hollis Voice's top green flag and its red flags, worst first. Under them, each piece with its mark and a one-line reason. | "Point it at a startup, get a readout. The best green flags, the worst red flags, then every piece of the company. Every number is two clicks from its source." | Backup laptop on the frozen readout. Last resort: a screenshot. |
| 0:30 | Traction and revenue: four ARR figures with source chips, about $3.0M on video, $2.5M in the deck, $2.24M in the model, $2.06M in the billing rows. "Video 0:35" plays five seconds of Ken's flat reading as audio over the deck slide, captioned. | "Four ARR numbers. On video, three million. In the billing rows, $2.06 million. That's 46% more." | No sound: the captions. No video: the transcript line with its timestamp. |
| 1:00 | The model's row "Marlow Veterinary Group (pilot)", then the contract-terms reading of the pilot agreement: clause 8, "No duty to convert". | "Part of the gap is a six-month pilot counted as a year of revenue. Here's the clause." | Saved images of the cell and clause. If contract terms is cut, the pilot flag still shows from its script check. |
| 1:30 | The green flag: deck slide 13 beside the cap table's Series A rows, each opening the other. | "The round adds up: nine million at forty-five pre, in the deck, the cap table and the model. Green flags get the same two clicks." | Saved images of both. |
| 2:00 | The real company's readout under its synthetic banner. Its website, Hacker News and SEC filing arrive live, each with its link and the time read. | "This is [company], a real YC company. Its website, Hacker News and SEC filing were read just now. Its data room is not real. We wrote it, every page says so, and its problems are our test plants." | A failed call shows this week's saved copy; Ken says "saved on" its date. |
| 2:30 | Hollis Voice again: the sealed variant's score line, then the header, "every line sourced". | "On a room someone outside the team planted and sealed, it found X of N. Next: forward the pitch email, and this is waiting before you open it. A fund would pay per seat." | Scores from the frozen run and the 4:15 variant run. |
| 3:00 | Extension. Market reads "not enough in the room"; the gaps panel; the scores for this room and the clean room. | "We planted eight problems and three traps. It found X and tripped Y. With nothing planted, it raised Z flags." | Frozen scores and the 4:15 clean run. |
| 3:30 | Seed drop to full room: the three second-tier flags appear. | "First tier alone, five of eight. Add the detail, and the pilot, the churn and the concentration appear." | Skip. |
| 4:00 | The clean room's readout. | "Same company, nothing planted. This is everything it flags." | Skip. |
| 4:30 | The readout stays up. | Questions ([BRAND.md](BRAND.md#pitching-to-judges)). | None. |

X, N, Y and Z come from the day's runs. Other numbers on screen come from the frozen run, since the generator may still change.

## What runs live and what is frozen

- **Live:** the real company's outside-world panel, on venue wifi or the phone hotspot. The sealed variant run, script checks only, needs no network.
- **Run beforehand:** Hollis Voice, its seed drop, the real company and Brasswick. The variant and clean rooms rerun at 4:15 PM.
- **Frozen:** everything that needs a model, including the contract-terms readings. The `demo-freeze` tag at 3:30 PM saves all outputs under `demo/frozen/`.
- **Sponsor tools:** Akta, Crunchbase and Nicrron go live on Saturday morning. Ken names the tool behind each panel.

## Fallbacks

Each beat's fallback is in the table. Beyond those:

- The backup laptop shows every beat from `demo/frozen/`.
- A sponsor tool that fails on Saturday morning stays on its sample responses.
- Never wait on stage. If a score is late, read the frozen one.

## Open choices

The beat sheet follows each card's recommendation.

- **Which real companies:** Ploy and Sazabi, with Ploy on stage, because its SEC filing matches its announced round ([research](../reports/20261022.02_research/research_demo_companies.md#1-ploy), [card](../features/20261022.01_hackathon_plan/00_overview.md#real-yc-companies-for-the-live-demo)).
- **The first screen:** the top flags, then the overview ([card](../features/20261022.01_hackathon_plan/00_overview.md#the-demo-opening)).
- **Proof the checks are not fitted:** the sealed variant plus the clean room ([card](../features/20261022.01_hackathon_plan/00_overview.md#the-blind-room)).
- **The score:** one line, the real number ([card](../features/20261022.01_hackathon_plan/00_overview.md#the-score-on-stage)).
- **A steer on stage:** steering is built by Saturday. The core names it in the closing line; a live steer is the card's other option ([card](../features/20261022.01_hackathon_plan/00_overview.md#steering-on-stage)).
- **A bank check:** built by Saturday, on Plaid's sandbox or, if that is not working, a labelled sample statement showing where the account plugs in. The core names it in the closing line. Showing it live is an option on the card ([card](../features/20261022.01_hackathon_plan/00_overview.md#a-bank-check-on-stage)).
- **Green flags in Hollis Voice:** drop the concentration flag so customers reads strong, which also changes the 3:30 line ([card](../features/20261022.01_hackathon_plan/00_overview.md#green-flags-in-the-demo-room)).
