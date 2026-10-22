# The Tricorder plan for Saturday

Everything the factory built today for Deal Flow, NYC's first VC hackathon (Betaworks, Saturday 2026-10-24, 9:00 AM to 6:00 PM, Track 2 Diligence), and the decisions that are yours. Press a button on each card or leave a comment. The roadmap is written to the recommended answers, so nothing is blocked while you decide.

## What I need from you

<div class="facts">
<div><dt>Decide</dt><dd>Fourteen cards in section 3, each with a recommendation. The three the critics are still weighing are marked.</dd></div>
<div><dt>Do this week</dt><dd>Seven rows on <a href="../../BULLETIN.md">the board</a>: interviews, the founder brief in your words, the pitch video, the keys, who joined, the organisers' questions, the Reddit pages.</dd></div>
<div><dt>Read first</dt><dd>The <a href="founder_brief.md">one-page founder brief</a>. It is what you hand the judges, and the organisers asked every team for it.</dd></div>
</div>

Written 2026-10-22 at 11:55 AM. Updated as the critics land and as you answer.

## What exists now

<div class="panel"><p><b>Saturday is build-only, so this week built everything but the product.</b> The organisers wrote "On Saturday you only build. Everything a founder does before writing code happens this week." The repo holds documents, research, the synthetic data room and prompts. It holds no product code.</p></div>

<ol class="sequence sequence--rows">
<li><div><h4>Research, four tracks</h4><p><a href="../../reports/20261022.02_research/research_voice_of_customer.md">Voice of the customer</a> (what investors check first, the flags they regret, what they pay for; 67 pieces of evidence, all linked, counted by its script). <a href="../../reports/20261022.02_research/research_landscape.md">The landscape</a> (the market map in the organisers' three columns, the sponsor tools, the judges). <a href="../../reports/20261022.02_research/research_feasibility.md">Feasibility per scan</a> (what four people can build in six hours, every data source with its terms). <a href="../../reports/20261022.02_research/research_data_room.md">The data room</a> (what a real one holds, the flags a first pass finds, the design of ours).</p></div></li>
<li><div><h4>The ongoing docs</h4><p><a href="../../ongoing/PRODUCT_BRIEF.md">Product brief</a>, <a href="../../ongoing/PERSONAS.md">personas</a> (say, do, pay), <a href="../../ongoing/BRAND.md">brand</a> (how the readout talks, the pitch to judges, the posting voice), <a href="../../ongoing/ROADMAP.md">roadmap</a> (this week, Saturday hour by hour, after), <a href="../../ongoing/ARCHITECTURE.md">architecture</a> (the stack, the Claim schema, the inbox design), <a href="../../ongoing/FRAMEWORKS.md">frameworks</a> (28 entries by its script: every check and prompt a scan runs, typed in on Saturday).</p></div></li>
<li><div><h4>The synthetic data room</h4><p><a href="../../../data_room/README.md">Hollis Voice</a>, an invented phone agent for vet clinics raising a Series A: 16 files, a thin 11-file seed drop, an answer key of 8 planted flags and 3 decoys, a generator with a fixed seed, and a check that passed 188 assertions. Every name and number is fictional.</p></div></li>
<li><div><h4>The founder brief</h4><p><a href="founder_brief.md">One page</a> in the organisers' four headings: problem, customer, business model, the one workflow we demo. 445 words by its script. Yours to edit.</p></div></li>
<li><div><h4>The critics</h4><p>Three are reading everything now: the judge, buildability, the demo. Their findings land in section 5 of this page.</p></div></li>
</ol>

## Decisions

Each card is written to the recommendation. The alternative is there in case you see it differently.

### The track

<div class="options">
<div class="option"><span class="badge badge--purple">Recommended</span><h4>Track 2 only</h4><p>The product answers the diligence problem statement direction by direction. The founder scan from Track 1 is one scan inside Tricorder, built after Saturday.</p></div>
<div class="option"><p class="eyebrow">Option B</p><h4>Track 2 with the founder scan on Saturday</h4><p>Shows your founder-profile idea on the day. Costs a Saturday slice, and the team card still needs its track fixed with the organiser.</p></div>
</div>

<div class="choice" data-choice="track">
<p class="choice-q">Which track?</p>
<button type="button" value="track-2-only" data-recommended>Track 2 only</button>
<button type="button" value="track-2-plus-founder">Add the founder scan Saturday</button>
</div>

### The edge

The landscape research found five AI diligence entrants already claim "every claim sourced", and a $600M fund already runs its diligence on one ([the landscape](../../reports/20261022.02_research/research_landscape.md), summary). The voice-of-customer research found the flag investors name most is numbers that disagree.

<div class="options">
<div class="option"><span class="badge badge--purple">Recommended</span><h4>Lead with disagreements and the red-flag engine</h4><p>The readout opens with the deck, the model and the video disagreeing, shows gaps as gaps, and sources every claim. Sourcing is table stakes, not the headline.</p></div>
<div class="option"><p class="eyebrow">Option B</p><h4>Lead with sourcing</h4><p>The posted pitch's line. Clear, but five competitors say it already.</p></div>
</div>

<div class="choice" data-choice="edge">
<p class="choice-q">What does the pitch lead with?</p>
<button type="button" value="disagreements-first" data-recommended>Disagreements first</button>
<button type="button" value="sourcing-first">Sourcing first</button>
</div>

### The pitch line

The brand doc proposes a tighter line for Saturday's first screen and the founder brief, and leaves the posted line on the network card as is ([BRAND.md](../../ongoing/BRAND.md), "The name and the line").

<div class="options">
<div class="option"><span class="badge badge--purple">Recommended</span><h4>The proposed line</h4><p>"Point it at a startup's data room, get a readout. Red flags first, then comps and market signals, every claim sourced."</p></div>
<div class="option"><p class="eyebrow">Option B</p><h4>The posted line</h4><p>"Point it at a startup, get a readout. Thesis-driven sourcing plus a first-pass diligence memo with every claim sourced." Sourcing is in it, and the track is diligence.</p></div>
</div>

<div class="choice" data-choice="pitch-line">
<p class="choice-q">Which line on Saturday?</p>
<button type="button" value="proposed" data-recommended>The proposed line</button>
<button type="button" value="posted">The posted line</button>
</div>

### Saturday's scans

The feasibility research ranked the scans by demo value for the effort. The roadmap builds the top five with four people and cuts from the bottom when the morning runs long ([ROADMAP.md](../../ongoing/ROADMAP.md), "Cut order").

<div class="options">
<div class="option"><span class="badge badge--purple">Recommended</span><h4>Five scans</h4><p>Red-flag engine, the readout, pitch video, comps, market signals. Frameworks, founder profiles and online presence come after Saturday.</p></div>
<div class="option"><p class="eyebrow">Option B</p><h4>Add the business frameworks scan</h4><p>Lean canvas and jobs to be done are the cheapest scan to build, one prompt each. Costs about an hour from someone's budget.</p></div>
</div>

<div class="choice" data-choice="saturday-scans">
<p class="choice-q">Which scans on Saturday?</p>
<button type="button" value="five" data-recommended>The five</button>
<button type="button" value="six-with-frameworks">Add frameworks</button>
</div>

### The demo opening

<div class="panel panel--purple"><p><b>The demo critic is weighing this now.</b> The roadmap recommends opening on a forwarded pitch email with the readout already waiting (your "before you even ask" moment), then loading the full room. On stage you say the forward is started by hand today, because the forwarding address is an after-Saturday slice. The other form opens on the upload and shows nothing that is not built. Buttons appear when the critic's verdict is in.</p></div>

### The score on stage

<div class="panel panel--purple"><p><b>The demo critic is weighing this now.</b> The product brief recommends showing the answer-key score (planted flags found out of eight, decoys wrongly flagged out of three) at the end of the demo. The risk is that it tells judges the room was built to be caught. Buttons appear when the critic's verdict is in.</p></div>

### The repo skeleton this week

<div class="panel panel--purple"><p><b>The buildability critic is weighing this now.</b> Option A: the skeleton is code, build it on Saturday in the first half hour (the roadmap is written to this). Option B: an agent writes the empty folders, the CI command and the Claim schema this week, with no scan logic, and two people get half an hour back on Saturday; the risk is that commits dated before Saturday are visible to anyone who looks. Buttons appear when the critic's verdict is in.</p></div>

### The demo company

<div class="options">
<div class="option"><span class="badge badge--purple">Recommended</span><h4>Hollis Voice</h4><p>An AI phone agent for vet clinics raising a $9M Series A. Built and checked. A NYC seed panel knows vertical software with a phone agent.</p></div>
<div class="option"><p class="eyebrow">Option B</p><h4>Brasswick</h4><p>Freight invoices. Plainer, and the generator would need a second run.</p></div>
</div>

<div class="choice" data-choice="demo-company">
<p class="choice-q">Which company in the room?</p>
<button type="button" value="hollis-voice" data-recommended>Hollis Voice</button>
<button type="button" value="brasswick">Brasswick</button>
</div>

### The inbox

Your 11:20 AM idea. The architecture doc read Google's and Microsoft's own pages: Gmail's read scope is restricted and needs Google's verification before strangers can connect, so the forwarding address comes first ([ARCHITECTURE.md](../../ongoing/ARCHITECTURE.md)).

<div class="options">
<div class="option"><span class="badge badge--purple">Recommended</span><h4>Forwarding address first, then the APIs</h4><p>deals@ through a mail-receiving service, no OAuth review. Gmail and Outlook through their official APIs after.</p></div>
<div class="option"><p class="eyebrow">Option B</p><h4>Gmail connection first</h4><p>The fuller experience, behind Google's verification.</p></div>
</div>

<div class="choice" data-choice="inbox-order">
<p class="choice-q">Which inbox path first?</p>
<button type="button" value="forwarding-first" data-recommended>Forwarding address first</button>
<button type="button" value="gmail-first">Gmail first</button>
</div>

### Diligence on the inbound

<div class="choice" data-choice="inbound-unasked">
<p class="choice-q">When a deck arrives, do the scans run before anyone asks?</p>
<button type="button" value="unasked" data-recommended>Yes, unasked</button>
<button type="button" value="on-request">Only when asked</button>
</div>

### Where the data goes

The brand doc's sentence: "Tricorder reads only the documents you give it or the decks in mail you send it, keeps only the readout and its sources, and lets you see and delete everything it pulled." The landscape research found judges reward a plain answer here, and the voice-of-customer research found funds will not let deal data leave the firm.

<div class="options">
<div class="option"><span class="badge badge--purple">Recommended</span><h4>The sentence above, as the rule</h4><p>Reads for decks only, stores only the readout and its sources, the investor sees and deletes everything.</p></div>
<div class="option"><p class="eyebrow">Option B</p><h4>A self-hosted version</h4><p>All data stays inside the fund. Answers the objection fully; a much larger product.</p></div>
</div>

<div class="choice" data-choice="data-rule">
<p class="choice-q">Which data rule?</p>
<button type="button" value="reads-only" data-recommended>The sentence, as the rule</button>
<button type="button" value="self-hosted">Self-hosted</button>
</div>

### After Saturday

<div class="options">
<div class="option"><span class="badge badge--purple">Recommended</span><h4>A product sold to funds</h4><p>The partner or principal buys, the associate uses. Per seat, yearly, starting from Affinity's published band. The first pilot ends with a price.</p></div>
<div class="option"><p class="eyebrow">Option B</p><h4>Skills on stclair.ai</h4><p>Your network profile's line: good skills, productized, for reliable sourcing and diligence. Sold the way the Reddit Research Agent is.</p></div>
<div class="option"><p class="eyebrow">Option C</p><h4>It ends Saturday</h4><p>A hackathon entry. The docs stay as a record.</p></div>
</div>

<div class="choice" data-choice="after-saturday">
<p class="choice-q">What is Tricorder after Saturday?</p>
<button type="button" value="product-for-funds" data-recommended>A product for funds</button>
<button type="button" value="skills-on-stclair">Skills on stclair.ai</button>
<button type="button" value="ends-saturday">Ends Saturday</button>
</div>

### Who we price for first

The voice-of-customer research found angels pay to avoid diligence (giving up upside to a lead, or becoming an LP) rather than to do it better. The persona order it set: partner or principal, solo angel, accelerator screener, associate, corporate VC ([PERSONAS.md](../../ongoing/PERSONAS.md)).

<div class="choice" data-choice="price-first">
<p class="choice-q">Who is the first paying customer?</p>
<button type="button" value="funds-first" data-recommended>Funds first, angels later</button>
<button type="button" value="angel-tier-too">An angel tier from the start</button>
</div>

### The name after the hackathon

The brand doc read the USPTO's records: CBS Studios holds a live registration on TRICORDER for a health-care innovation competition and live applications for a toy scanner and for medical diagnostic devices, and is still filing in new fields. Nothing found for finance software, but the search was not a full one ([BRAND.md](../../ongoing/BRAND.md), "The name's origin and the trademark risk").

<div class="options">
<div class="option"><span class="badge badge--purple">Recommended</span><h4>Keep it Saturday, rename before the first paid customer</h4><p>A team name at a one-day event sells nothing. If it becomes a product, pick a new name with a lawyer's clearance search. The readout vocabulary (scan, readout, flag, gap) carries over.</p></div>
<div class="option"><p class="eyebrow">Option B</p><h4>Rename now</h4><p>Costs the posted team card and the workshop's work, two days out.</p></div>
<div class="option"><p class="eyebrow">Option C</p><h4>Keep it for good</h4><p>Risk sits with CBS's next filing.</p></div>
</div>

<div class="choice" data-choice="name-after">
<p class="choice-q">The name after Saturday?</p>
<button type="button" value="keep-then-rename" data-recommended>Keep now, rename before selling</button>
<button type="button" value="rename-now">Rename now</button>
<button type="button" value="keep-for-good">Keep for good</button>
</div>

### Measures

<div class="choice" data-choice="measures">
<p class="choice-q">When do the product's numeric targets get set?</p>
<button type="button" value="after-pilot" data-recommended>After the first pilot</button>
<button type="button" value="predict-now">State predictions now</button>
</div>

## The Saturday plan in one table

Hacking runs 10:30 to 4:30 by the schedule. The Luma page also says nine hours; a board row asks the organisers which. The full hour-by-hour run of show, the integration points and who presents are in [ROADMAP.md](../../ongoing/ROADMAP.md), "Run of show".

<div class="scrollx"><table class="boxed">
<thead><tr><th>Slice</th><th>Who</th><th>Hours</th><th>What it is</th></tr></thead>
<tbody>
<tr><td>skeleton</td><td>backend-and-data</td><td>0.5</td><td>Folder layout, server, CI, smoke command</td></tr>
<tr><td>claim-result</td><td>captain</td><td>1.0</td><td>The Claim schema, frozen at 11:00, and the quote checker</td></tr>
<tr><td>redflag-engine</td><td>design-and-finance</td><td>3.0</td><td>The checks on the model, the CSVs and the deck's claims</td></tr>
<tr><td>readout</td><td>captain</td><td>1.5</td><td>The memo built from the claims: disagreements, flags, gaps</td></tr>
<tr><td>readout-page</td><td>frontend</td><td>4.5</td><td>The page the judges see, each claim opening its source</td></tr>
<tr><td>pitch-video</td><td>backend-and-data</td><td>2.5</td><td>Whisper transcript, claims with timestamps, the third ARR number</td></tr>
<tr><td>comps</td><td>design-and-finance</td><td>1.5</td><td>Comparable companies and rounds with the reason each is fair</td></tr>
<tr><td>market-signals</td><td>backend-and-data</td><td>1.5</td><td>Hiring, traffic, reviews for the company and its competitors</td></tr>
<tr><td>demo-freeze</td><td>captain, all four</td><td>2.0 + 0.75</td><td>Merge, score, freeze at 3:30, two rehearsals</td></tr>
</tbody>
</table></div>

Cut order when the morning runs long: market signals, then comps, then the pitch video. The red-flag engine, the readout and its page are never cut.

## What the critics said

<div class="panel"><p><b>Pending.</b> The judge, the buildability critic and the demo critic are reading now. Their findings and the three cards they settle land here.</p></div>

## Your rows on the board

All on [BULLETIN.md](../../BULLETIN.md), newest first:

- **Edit the founder brief** in your own words ([founder_brief.md](founder_brief.md)).
- **Record the two-minute pitch video** from [the script](../../../data_room/hollis_voice/01_overview/pitch_video_script.md); it says "about $3 million" on purpose.
- **Run two or three interviews** with the organisers' three questions, into [interviews.md](../../reports/20261022.02_research/interviews.md).
- **Say who accepted the invites.**
- **Get the sponsor keys**: Akta (ask for a coupon; the useful signals are on the $50 plan), Nicrron, You.com, Tavily, an Anthropic key, a GitHub token, a contact address for the SEC's User-Agent rule.
- **Ask the organisers** who Roundtable is, which fund D. J. Patel is with, whether Abeera Saeed is still at Plug and Play, and whether the build window is six hours or nine. Plus the track change from the other session's row.
- **Save the 20 Reddit pages** the voice-of-customer track listed. Not blocking.

## How this was built

The factory that built My Text Reminders, run again: a Seneschal scaffold, [the writers' brief](00_brief_for_writers.md) with your words and every decision verbatim, four research agents, five writers, a data-room builder, three critics, this page. Every count on this page names the script that produced it in the linked file. Files agents would have deleted are listed in [cleanup_needed.md](cleanup_needed.md) for one batch.
