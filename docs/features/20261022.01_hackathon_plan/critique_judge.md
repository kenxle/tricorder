# C1: The judge's critique

Written 2026-10-22 by C1, reading the plan as a VC judge on the Deal Flow panel. Seat math comes from a script run for this critique (`seat_math.py`, in the session scratchpad); every other count is quoted from the script the source file names.

## Verdict

I would shortlist it. It's in my top three, but I wouldn't pick it to win yet. The readout format is sharp, the planted-flag room is better prepared than almost any hackathon entry, and the "script decides, model reads" rule is a real answer to "is this a wrapper". What keeps it from winning is that the team wrote the room, planted the flags, wrote the answer key and then wrote one check per planted flag. A score of 8 out of 8 on your own exam proves nothing to a partner. **The one change that most raises its odds: on stage, run Tricorder on a room it has never seen.** That could be a variant room that someone outside the build seals this week, or a judge changing a number in the model live. Then show the readout catch it.

## Findings

### 1. The demo grades its own homework

- **Severity:** must fix before Saturday
- **Concerns:** [ROADMAP.md, redflag-engine](../../ongoing/roadmap/redflag-engine.md), [answer_key.json](../../../data_room/answer_key.json), [founder_brief.md, the workflow](founder_brief.md#the-one-workflow-well-demo)
- **What is wrong:** The red-flag engine has "one check per planted flag", and its test passes when it matches the answer key by check name. The founder brief ends on "our score against the answer key". A judge reads that as a test you wrote for code you wrote.
- **Fix:** This week, an agent that has not seen the check list generates a second room. It uses a new seed, moves the values and drops or adds one flag, and its answer key stays sealed until the 3:30 PM freeze. On stage, run that room live, then offer a judge one cell to change in `financial_model.xlsx` and rerun the red-flag scan.

### 2. The demo shows one of the three things Track 2 asks for

- **Severity:** must fix before Saturday
- **Concerns:** [founder_brief.md, "On screen"](founder_brief.md#the-one-workflow-well-demo), [ROADMAP.md, Cut order](../../ongoing/roadmap/saturday.md#demo-fallback-order), [problem_tracks.txt](../../reports/20261022.01_hackathon_sources/problem_tracks.txt)
- **What is wrong:** Track 2 asks for market signals, comps and red flags. The founder brief's gap claim is that none of 24 tools shows all three together ([landscape_counts.py](../../reports/20261022.02_research/landscape_counts.py)). Yet the "On screen" list shows only disagreements, flags, gaps and the score, and the cut order drops signals and comps first. The pitch claims a gap that the demo does not fill.
- **Fix:** Give comps and signals 30 seconds on screen, from cache if need be. A comp row should carry its "why it is fair" sentence, and a signal row its link. If they are cut on the day, take the "none of 24" line out of the pitch.

### 3. No buyer has spoken yet

- **Severity:** must fix before Saturday
- **Concerns:** [founder_brief.md, Customer](founder_brief.md#customer), [PERSONAS.md, persona 1](../../ongoing/PERSONAS.md#the-partner-who-finds-the-disagreement-too-late)
- **What is wrong:** The organisers said to talk to people with the problem and "build a company, not a project" ([problem tracks](../../reports/20261022.01_hackathon_sources/problem_tracks.txt)). The partner's pay rating is inferred from a competitor's case study and a pricing roundup. The brief admits "our interviews ask directly", so no interview has happened. That reads as a project.
- **Fix:** Run the interviews before Saturday. Put one named, consenting investor's answer in the Problem section, replacing the organisers' own sentence. The best version is one fund that says it would forward its next three decks.

### 4. The edge is already prior art

- **Severity:** should fix
- **Concerns:** [PRODUCT_BRIEF.md, The problem](../../ongoing/PRODUCT_BRIEF.md#the-problem), [research_landscape.md, Part 4](../../reports/20261022.02_research/research_landscape.md#part-4-prior-art), [BRAND.md, If a judge asks](../../ongoing/BRAND.md#pitching-to-judges)
- **What is wrong:** FirstSignal, a hackathon runner-up, already leads its memo with contradictions and shows missing facts as flagged gaps. askRIA and Keye already read data rooms and flag cohort and margin problems. "Disagreements first, gaps as gaps" is a format, and a format is easy to copy.
- **Fix:** Lead with what is harder to copy. Tricorder rebuilds each number from the raw rows (ARR from subscription rows, cohorts from the customer file, payroll from the hiring plan), and a script, not a model, decides that a number is wrong. The founder brief never says this, and it is the best answer to "wrapper".

### 5. The room is tidier than any real room

- **Severity:** should fix
- **Concerns:** [data_room/README.md, The files](../../../data_room/README.md#the-files), [answer_key.json](../../../data_room/answer_key.json)
- **What is wrong:** Slide 14 of the deck lists every number with its slide, the model uses named cells such as `ARR_TOTAL`, and the metrics file has a column literally named `accounts_created_cumulative`. Track 2 says the pain is rebuilding numbers "from a messy data room". A judge who has opened real rooms will spot slide 14 and ask whether the engine only works because the room labels its own answers.
- **Fix:** Never show slide 14 on stage. Make the deck reader pass on slides 3 to 13 first, with slide 14 as a fallback only. In the sealed variant room from finding 1, rename one named cell and one column so the demo shows the checks surviving it.

### 6. The opening is a feature that isn't built

- **Severity:** should fix
- **Concerns:** [ROADMAP.md, The one workflow we demo](../../ongoing/roadmap/demo_workflow.md), [founder_brief.md](founder_brief.md#the-one-workflow-well-demo)
- **What is wrong:** The first 30 seconds show a forwarded email, followed by "today we start the forward by hand". A judge hears "this part is fake" before seeing anything real. Running the seed drop and then the full room spends a second load on the same story.
- **Fix:** Open on the ARR disagreement table already on screen. Mention "it runs when the deck lands in your inbox" in the close, as what is next. Keep the seed drop to full room switch only if it takes under 20 seconds.

### 7. The price anchors low and the market is never sized

- **Severity:** should fix
- **Concerns:** [founder_brief.md, Business model](founder_brief.md#business-model), [research_landscape.md, Part 1](../../reports/20261022.02_research/research_landscape.md#a-tools-funds-use-for-diligence-and-sourcing-today)
- **What is wrong:** Affinity is a CRM, so anchoring on its seat price puts Tricorder in the cheap-tool bucket. Seats go to associates, and a seed fund has few. At one to three seats in Affinity's band, a fund pays $2,000 to $8,100 a year (seat_math.py). Vendr's median Affinity spend per firm is $49,758, about 6.1 times the three-seat top. There is no count of funds anywhere, so a judge cannot multiply to a company.
- **Fix:** Price per fund, sized by deals screened, and anchor on what funds spend per firm on data tools (the Vendr medians), not on a CRM seat. Add one sourced count of US seed and Series A funds, so the business model ends in a number.

### 8. The data sentence leaves out the model provider

- **Severity:** should fix
- **Concerns:** [BRAND.md, Where the data goes](../../ongoing/BRAND.md#where-the-data-goes), [ROADMAP.md, readout-store](../../ongoing/roadmap/readout-store.md)
- **What is wrong:** The sentence says Tricorder "keeps only the readout and its sources". But readout-store keeps "the files it read" too, and the room's text goes to a third-party model API. The security engineer on the panel will ask exactly this, and the landscape research says to name what is sent to which model.
- **Fix:** Add one plain clause naming the model provider and its retention terms. Say "sources" includes the files.

### 9. The only sponsor tool sits in the first slice cut

- **Severity:** note
- **Concerns:** [ROADMAP.md, market-signals](../../ongoing/roadmap/market-signals.md)
- **What is wrong:** Akta is used only for market signals, the first thing cut.
- **Fix:** If signals are cut, use Akta's company data in the comps panel and say so in one line.

### 10. The founder brief's small winces

- **Severity:** note
- **Concerns:** [founder_brief.md](founder_brief.md)
- **What is wrong:** Several lines work against the pitch:
  - It cites a competitor's case study as proof that funds pay, which advertises V7 Go.
  - The PitchBook seat price is irrelevant to a diligence tool.
  - "Memo tools already sell at $12 a memo" tells the judge the category is cheap.
  - It never says who the team is or why it is the team to build this.
- **Fix:** Keep the V7 line in speaker notes only, and cut PitchBook and the $12 line from the page. Add one line on the team: the finance and valuation skills that wrote the checks, and Ken's product record.

## The hardest judge

**Michael Barone, Everywhere Ventures.** He is the associate Tricorder is built for, at a fund that writes $250k pre-seed checks ([research_landscape.md, Part 3](../../reports/20261022.02_research/research_landscape.md#the-eight)). Pre-seed rooms barely exist, so a 16-file Series A room is not his day. His own "Signals and Startups" writing is market signals with sources on every startup, which is the panel the plan cuts first. He will ask what Tricorder does with a ten-slide deck and nothing else. The gaps list is the answer, so rehearse it. Radhika Khandelwal is a close second. The organisers' bio says "She'll want to see both slick code and a real business." ([luma.com/vc-hack-nyc](https://luma.com/vc-hack-nyc)), and she builds agents for a living. Finding 1 is her question.

## What would win

- Open on the ARR disagreement: four figures side by side, each opening its slide, cell or video second.
- Run a room the builders never saw, live, and show the score on it.
- Let a judge change one cell and watch the flag appear.
- Show comps and signals for 30 seconds each, so all three Track 2 asks are on screen.
- Name one investor from this week's interviews, in their words, and what they would pay.
- Say "the script decides, the model only reads" in one sentence, with the cohort rebuild as proof.
- Measure the run's wall-clock time on Saturday and say it as a measured fact on this room.
- End on the data sentence, with the model provider named.

## The question with no answer

**"You built the company, planted the flags and wrote the answer key. What does it find in a data room you didn't make?"** Every trust answer in the plan points back to the planted-flag room ([BRAND.md, If a judge asks](../../ongoing/BRAND.md#pitching-to-judges)). That is circular. Finding 1's sealed room is the only answer, and it has to exist before Saturday.
