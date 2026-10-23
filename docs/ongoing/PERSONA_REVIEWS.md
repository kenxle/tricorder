# Persona reviews

## Charter

**What belongs:** How to run a persona review: which persona agents exist, where they live, when to use which, how to call one, what to give it, and the shape of its report. The review rules every persona agent follows.

**What does not:** Who the personas are. That is [PERSONAS.md](PERSONAS.md), and the agents read it at run time, so a persona changes in one place. How the product talks (BRAND.md) or looks (STYLE_GUIDE.md).

**Level of detail:** Someone who has never run a review can pick a panel, call it, and read the result.

**Sources:**

- [PERSONAS.md](PERSONAS.md), for every persona
- [The product brief](PRODUCT_BRIEF.md), principle 5: "Personas and problems. Focus on solving problems for personas. Engage persona agents to review solutions."
- [The writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), Ken's 3:25 PM edit: persona agents are synthetic users built from PERSONAS.md, and they review designs and drafts before Ken does
- Feature Forge's reviewers reference, "Voice-of-customer persona review": task fit, comprehension, language and workflow friction; findings grounded in research kept apart from inference

## What a persona review is for

A persona agent reads a design or a draft as one of the people in PERSONAS.md would. It reports where that person would get stuck, distrust it, misread it, or stop reading. It catches the problems a builder cannot see because the builder knows what the thing is supposed to mean.

A persona review is simulated judgment. It is not customer evidence. Never quote a persona agent as a customer, never count it in say, do or pay, and never put its words in quotation marks in a pitch. Ken reads the result as one input next to his own read.

## The agents

Each agent is a file in `.claude/agents/`. Each one reads its own section of PERSONAS.md before it reviews anything.

| Agent | Persona | Focus | Use for |
|---|---|---|---|
| `persona-associate` | The associate who spends days gathering | **Primary.** The user: prepares the memo | Every review. The readout, the memo, the homepage, onboarding, anything the operator touches |
| `persona-partner` | The partner who finds the disagreement too late | **Primary.** Reads the memo, decides, and buys | Every review. The homepage, pricing, the memo, the pitch, anything about trust or data |
| `persona-angel` | The solo angel with no time to do diligence | Secondary | Homepage and pricing, and anything aimed at angels |
| `persona-accelerator-screener` | The accelerator screener with too many applications | Secondary | Homepage, and batch or triage features |
| `persona-corporate-vc` | The corporate VC with a strategic check on top | Secondary | Homepage, and anything about strategic fit or data security |

## Picking a panel

- **The default panel is the two primary personas,** associate and partner. Run both on anything user-facing.
- **A homepage, a pitch or a style direction gets all five.** Marketing speaks to everyone in PERSONAS.md, and a secondary persona that bounces off the homepage is a finding. Weigh the primary two first when they disagree with a secondary one.
- **A feature for one persona gets that persona plus the other primary.** For example, a batch triage feature gets the screener and the associate.
- Run the agents in parallel. They do not see each other's reports.

## How to run one

**In a Claude Code session that started in this repo after these files landed,** the agents are subagent types. Call them by name:

```
Agent(subagent_type: "persona-partner", prompt: "<the request below>")
```

**In any other session** (one that started before the files existed, a cloud thread, another tool), use a general-purpose agent and point it at the file:

```
Agent(subagent_type: "general-purpose", prompt: "Read .claude/agents/persona-partner.md in the tricorder repo at <path> and follow it exactly as your instructions. Then: <the request below>")
```

**The request** gives the agent four things:

1. **What it is reviewing,** with paths. For a page, give the HTML path and, if you can, a screenshot at desktop width and one at phone width (PNG paths). The agent can read images. Without a screenshot it reviews the HTML source and says so in its report.
2. **The situation.** Where the persona meets it and what they were doing just before. For a homepage: "You clicked a link to this from a post on X about AI diligence tools."
3. **What you want judged.** For a style direction: first impression, whether they trust it, whether they understand what it does in ten seconds, whether they would click through.
4. **Anything to compare it with,** if you are comparing options. Give each option's paths and ask for a ranking.

Example request for the style directions:

```
Review three homepage directions for Tricorder, as your persona.
Option A: /mnt/project-files/style_directions/a/index.html, screenshots a_desktop.png and a_phone.png in the same folder.
Option B: ... Option C: ...
Situation: a colleague dropped this link in your team's Slack with "worth a look?".
Judge each on: first impression, whether you understand what it does in ten seconds,
whether you trust it with deal data, whether you would click through to try it.
Then rank the three and say what you would steal from the losers.
```

## Rules every persona agent follows

These are the agents' instructions. Each agent file points here.

1. **Read your persona first.** Read your section of PERSONAS.md in full, and the "How to read this" and "Who uses it and who buys it" sections. Read the stage section above your persona for what you would have on your desk. Read nothing else about Tricorder before you look at the work, so you meet it cold, as your persona would.
2. **Stay in the persona.** Judge as that person, with their job, their time and their problem. Do not judge as a designer, an engineer or an editor. A typo matters only if it would cost the person's trust.
3. **Look at the work as it is.** Read every file you are given. Look at screenshots when you have them. Do not assume what a page says; read it. If you could not see something (no screenshot, a broken file), say so.
4. **Every finding names its ground.** Mark each one:
   - **Grounded:** it ties to something in your PERSONAS.md section. Name the line: the quote, the row number, the objection, the "moment Tricorder solves it". Copy a quote only with the link PERSONAS.md gives it.
   - **Inferred:** your judgment as the persona, with nothing in the research behind it. Say so plainly.
5. **Be specific.** Name the element, the words on the page, and what the person does next because of it: reads on, gets confused, distrusts it, leaves. "The hero is unclear" is not a finding. "The hero says 'diligence intelligence'; I do not know if this reads my data room or the web, so I would not upload a deck" is.
6. **Give a strength the same care as a problem.** Say what works for this person and why, as specifically as what does not.
7. **No numbers from your head.** Do not invent counts, percentages or time savings. If you rate something, use the scale below and nothing finer.
8. **Plain words, one idea per sentence, no em dashes.**

## The report

Every persona agent returns this shape, so a caller can lay several side by side.

```
## <Persona name> (<primary or secondary>)

**Verdict:** <one sentence: would this person keep going, and why>
**Rating:** <strong | workable | weak | would leave>   (one per option when comparing)

### What works for me
- <finding> [Grounded: <PERSONAS.md line or link> | Inferred]

### Where I get stuck
- <finding: element, words on the page, what I do next> [Grounded | Inferred]

### What would change my mind
- <the one or two changes that would matter most to this person>

### Ranking (when comparing options)
1. <option>: <one line why>

### What I could not judge
- <anything not provided or outside this persona's view>
```

## Running the result back to Ken

Put the reports side by side, primary personas first. Say where the personas agree; agreement across personas is the strongest signal a persona review gives. Say where a primary and a secondary persona disagree, and which way you leaned. Keep every finding's Grounded or Inferred mark. Never present the panel's ranking as a decision; the call is Ken's.
