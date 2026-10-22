# C3: The demo and the data room

Critic C3, 2026-10-22. I read the plan as the person on stage and as the associate in the audience.

## Verdict

The demo lands if it opens on the four ARR numbers and runs on the full room. The room is good enough for the stage. The planted flags are the four the organisers named (churn hidden in cohorts, a pilot counted as ARR, burn that ignores the hiring plan, deck against model), plus three standard ones. Three things work against it today:

- The plan opens on a step that is not built (the email forward).
- The script is sized for five minutes, and the schedule gives every team's demo plus the winner 30 minutes in all.
- The room has tells an associate will spot the moment a source click opens a raw file. It also has one real problem nobody planted: the cash does not add up.

**The one change that helps most:** open on the ladder of ARR figures (about $3.0M said on video, $2.5M in the deck, $2.24M in the model, $2.06M in the billing rows), cut the script to three minutes, and say the inbound email in one closing line as what comes next.

Counts and ratios below come from three read-only scripts run on 2026-10-22: `dump_room.py`, `room_stats.py` and `room_checks.py`, in the session scratchpad. The orchestrator can copy them next to the room to keep them.

## Findings

**1. The script is too long for the slot.** *Must fix before Saturday.* [ROADMAP.md, demo-freeze](../../ongoing/ROADMAP.md#demo-freeze)
The plan's "done when" is a five-minute run. The schedule gives 5:30 to 6:00 for every team's demo and the winner ([brief](00_brief_for_writers.md#the-hackathon)), so the slot is likely three minutes or less. Fix: rehearse a three-minute core (the beat sheet below) with a five-minute extension. Add the slot length to the TRI-ask-organisers row (questions for the organisers).

**2. Do not open on a forward you start by hand.** *Must fix before Saturday.* [ROADMAP.md, the one workflow we demo](../../ongoing/ROADMAP.md#the-one-workflow-we-demo), [founder_brief.md](founder_brief.md#the-one-workflow-well-demo)
The first 20 seconds would go on the one thing on screen that is not real, plus a sentence admitting it. Judges remember what they saw working. Fix: open on the readout, already waiting, which is true because it ran before Ken walked up. Use the inbound forward as the closing "next" line. Build the real forward only if the red-flag engine and readout are done at the 2:30 cut call. A small inbox-polling script needs no OAuth review.

**3. The cash does not reconcile, and nobody planted it.** *Must fix before Saturday.* [financial_model.xlsx](../../../data_room/hollis_voice/02_financials/financial_model.xlsx), [README.md](../../../data_room/README.md#notes-for-whoever-runs-the-demo)
Operating losses for 2025-01 to 2026-09 sum to $3,091,744 (P&L, C30:W30). The company raised $2,000,000 (cap_table.xlsx, B18) and holds $1,800,000 (Assumptions, B6), which leaves $2,891,744 unexplained. A finance judge can ask about it, or Tricorder can find it, and then the answer key is wrong. Fix: add a priced seed round or a larger SAFE total to the generator so the money adds up, then rerun `check.py`.

**4. Two details make the room look built to be caught.** *Must fix before Saturday.* [customer_mrr_by_month.csv](../../../data_room/hollis_voice/03_metrics/customer_mrr_by_month.csv), [pitch_deck.pdf, slide 14](../../../data_room/hollis_voice/01_overview/pitch_deck.pdf)
The largest customer is `C-BIG` and the pilot is `P-MARLOW`, among ids like `C0185`. The deck ends on a "Claims page", which no founder makes, and the cover note promises every number ties. Fix: give both customers ordinary ids. Retitle slide 14 "Appendix: key metrics", which real decks do have, or drop it and keep the `claims.json` sidecar as the parser fallback.

**5. The video needs work to land.** *Should fix.* [pitch_video_script.md](../../../data_room/hollis_voice/01_overview/pitch_video_script.md), [ROADMAP.md, record-pitch-video](../../ongoing/ROADMAP.md#record-pitch-video)
Ken records it, but the script opens "Hi, I'm Imogen Tarrant", and judges will see the presenter playing the founder. Against the deck alone, "about three million" against $2.5M sounds like normal founder rounding. Against the billing rows it lands: $3.0M is 46% above $2,060,868 (answer_key.json, `facts`). Fix: have someone off stage record it, as a voiceover over the deck slides. Play only the 0:35 sentence, with burned-in captions, from an H.264 MP4 (iPhone HEVC may not play in the browser). Frame the line as the ladder.

**6. Source clicks must not launch Excel or a PDF viewer.** *Should fix.* [ROADMAP.md, readout-page](../../ongoing/ROADMAP.md#readout-page)
A spreadsheet app opening on a projector is slow. It also shows the associate the tidy rows listed at the end of this file. Fix: render each cited cell or page as an in-page panel, using a pre-rendered PNG of the slide or a small HTML table with the cell highlighted.

**7. Show the score as a test, and prove the checks are not fitted to it.** *Should fix.* [ROADMAP.md, demo-freeze](../../ongoing/ROADMAP.md#demo-freeze), [BRAND.md, pitching to judges](../../ongoing/BRAND.md#pitching-to-judges)
Judges already know the room is synthetic, so the score reveals nothing they don't know. The risk is that "8 of 8 on our own key" sounds circular. Fix: one line near the end ("eight planted problems, three traps; today it found X and tripped Y"), and show the real number even if it is 7. If time allows before Saturday, add a plants-off switch to the generator. The research describes one, and `generate.py` has none. A clean room that comes back clean is the strongest ten seconds against "rigged".

**8. Two of the three decoys catch nothing.** *Should fix.* [answer_key.json, decoys](../../../data_room/answer_key.json), [order_form_brookline_row.pdf](../../../data_room/hollis_voice/04_customers/order_form_brookline_row.pdf)
DC1 (the onboarding fee, correctly left out of ARR) is labelled "(one-time, excluded)" with zero ARR (ARR_Build, A14:E14). DC2 (the annual prepay, correctly counted as recurring) has a $7,788 fee, which equals 12 times $649. Both readings give the same answer, so there is nothing to get wrong. DC3 (the clean cap table) is a fair trap. Fix: give Brookline an annual discount and add a billings column with the June cash spike, so a naive check is tempted. Drop "excluded" from the DC1 label.

**9. The numbers are too tidy.** *Should fix.* [generate.py](../../../data_room/generate.py)
Gross margin is exactly 80.0% in all 33 months, and payroll rises by exactly $14,933.33 per hire. The full list is at the end. An associate reads these as plugs, and a sharp one wonders which other "flags" are also plugs. Fix: add seeded noise to cost lines, salaries, rent and customer prices, and keep each plant's margin over its tolerance. Rerun `check.py`.

**10. The cover note puts three flags after the term sheet.** *Note.* [cover_note_and_index.pdf](../../../data_room/hollis_voice/00_welcome/cover_note_and_index.pdf)
It says the second tier (revenue by customer, ledger, contracts) is shared after a term sheet. Track 2 asks for red flags "before a second meeting". Fix: change it to "shared on request after a first meeting".

**11. The pitch carries too much before the demo.** *Note.* [BRAND.md, pitching to judges](../../ongoing/BRAND.md#pitching-to-judges)
Two investor quotes, the buyer and the data sentence will not fit three minutes. VC judges know the problem. Fix: drop both quotes from the spoken pitch and keep them on the founder brief. Say the data sentence only when asked.

**12. Two readout details.** *Note.* [BRAND.md, the readout's voice](../../ongoing/BRAND.md#the-readouts-voice)
Once the pilot is out of recurring revenue, gross margin on subscription revenue alone is 54.5% (P&L, W7, W13, W14, W20, W22), not the 58.1% shown. "About $759,132" mixes "about" with exact dollars. Fix: say which revenue the margin uses, and round a gap that starts from a spoken figure.

## The beat sheet

Three-minute core, then the extension if the slot is five minutes. The frontend drives. Backend-and-data holds the backup laptop on `demo/frozen/`. Start a fresh full-room run in a hidden tab at 0:00.

| Time | On screen | Ken says | Fallback |
|---|---|---|---|
| 0:00 | Readout top: the ARR ladder in large type, each figure with its source chip | "One startup, one month, four ARR numbers. The further from the billing data, the bigger the number." | Backup laptop on the frozen readout. Last resort: a screenshot. |
| 0:30 | Click "video 0:35": a five-second captioned clip, "about three million" | "On video, three million. In the billing rows, $2.06 million. That's 46% more." | No sound: captions carry it. No video: the transcript line with its timestamp. |
| 1:00 | Click the model figure: ARR_Build row 13, "Marlow Veterinary Group (pilot)", then clause 8, "No duty to convert" | "Part of the gap is a six-month pilot counted as a year of revenue. Here's the clause." | Pre-rendered PNGs of the cell and the clause. |
| 1:30 | Flags list: retention 102.6% shown, 87.3% rebuilt, 11 customers dropped; runway 37 months shown, 19 with all 24 hires; largest customer under 9% claimed, 21% found; margin 80% against 58.1% (answer_key.json, PF3 to PF6) | "Each flag shows their number, our number, and the question to ask the founder on Monday." | Frozen readout. |
| 2:00 | Gaps panel ("not in the room"), the clean cap table, then the score line | "It says what's missing and leaves clean things alone. We planted eight problems and three traps. Today it found X and tripped Y." | Score from the frozen run. |
| 2:30 | Readout header: "every line sourced" | "Next: forward the pitch email, and this is waiting before you open it. The partner pays per seat. If you do first passes, try it on your next deal." | None needed. |
| 3:00 | Switch from the seed drop to the full room: the three flags that need the second tier light up | "With the first tier alone, five of eight. Add the detail, and the pilot, the churn and the concentration appear." | Skip the beat. |
| 3:30 | The hidden-tab run, finished, with its start time | "This run started when I began talking. Same findings." | If it has not finished, skip. Never wait on stage. |
| 4:00 | Readout stays up | Questions: where the data goes, "isn't this a wrapper", what happens when a scan fails (answers in BRAND.md) | n/a |

**What else goes wrong live:**

- **Wifi.** Serve the page and frozen files from localhost, with no fonts or scripts from a CDN, and keep a phone hotspot ready.
- **A model call fails.** Nothing on screen calls a model at render time.
- **Display.** Rehearse at 1280 by 720 at 150% zoom, and bring a USB-C to HDMI adapter for each laptop.

**What judges remember an hour later:** the team whose founder said three million on video while the billing rows said two. Put the ladder at the top of the founder brief too, so the page they keep shows the same picture.

## What the room gets wrong as a fake

- Gross margin is 80.0% in every month for 33 months, because cost of revenue is a fixed 15% plus 5% of revenue. [financial_model.xlsx](../../../data_room/hollis_voice/02_financials/financial_model.xlsx), P&L C17:AI17.
- Payroll rises by exactly $14,933.33 per hire, so every person costs the average. [financial_model.xlsx](../../../data_room/hollis_voice/02_financials/financial_model.xlsx), P&L row 29; Assumptions B8 and B10.
- Office rent takes 14 different values in 21 months, in step with headcount, for example $14,611.77 in 2025-01 and $15,564.71 in 2025-02. A lease does not do that. [expense_ledger.csv](../../../data_room/hollis_voice/02_financials/expense_ledger.csv), lines 10 and 22.
- The "ledger" has 252 rows over 21 months, 12 a month, with one vendor named "Various". It is a P&L in long form. [expense_ledger.csv](../../../data_room/hollis_voice/02_financials/expense_ledger.csv).
- Every subscription pays list price. The 1,880 subscription rows hold only 5 distinct MRR values, and 211 of 212 paying customers have one location. [customer_mrr_by_month.csv](../../../data_room/hollis_voice/03_metrics/customer_mrr_by_month.csv).
- The group customer pays $2,117.65 per location, 1.93 times the Pro list price. The pilot costs $3,750 per location, 3.41 times list. Pilots are usually discounted. [order_form_cedar_pine.pdf](../../../data_room/hollis_voice/04_customers/order_form_cedar_pine.pdf), page 1; [pilot_agreement_marlow.pdf](../../../data_room/hollis_voice/04_customers/pilot_agreement_marlow.pdf), clause 2.
- 62 of the 117 cohort cells are exactly 100%. [financial_model.xlsx](../../../data_room/hollis_voice/02_financials/financial_model.xlsx), Cohorts F5:R13.
- The hiring plan has exactly two hires on the first of every month, and all 24 salaries are multiples of $5,000. [hiring_plan.csv](../../../data_room/hollis_voice/05_team/hiring_plan.csv).
- The cap table is round: 12,000,000 shares and a $1.00 conversion price. [cap_table.xlsx](../../../data_room/hollis_voice/02_financials/cap_table.xlsx), C12 and E16.
- The names read as generated: Lucan Faraday-Moss, Anselm Okoye-Ruiz, and "Anselm" used twice, once for the angel. Both founders share `github.com/hollis-voice-demo`. [founder_bios.pdf](../../../data_room/hollis_voice/05_team/founder_bios.pdf); [cap_table.xlsx](../../../data_room/hollis_voice/02_financials/cap_table.xlsx), A10.
- The deck is text and two charts: no logo, no product screen, no example call. 2 of 14 slides carry an image. [pitch_deck.pdf](../../../data_room/hollis_voice/01_overview/pitch_deck.pdf).
- The cash gap in finding 3 is the one that matters most.
