# Frameworks

## Charter

**What belongs:** Every analysis a scan runs. For each one: its inputs, the questions it asks, the mechanical check a script runs, the model reading with its exact prompt, the output shape as a JSON schema, and how the readout scores it.

**What does not:** How the code is organised (that is [ARCHITECTURE.md](ARCHITECTURE.md)). What the product is and who it is for (that is [PRODUCT_BRIEF.md](PRODUCT_BRIEF.md)).

**Level of detail:** One entry per framework, written so a builder turns it into one prompt and one schema without asking.

**Sources:** [the writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), [the organisers' problem tracks](../reports/20261022.01_hackathon_sources/problem_tracks.txt), [research_data_room.md](../reports/20261022.02_research/research_data_room.md) with [data_room_flags.csv](../reports/20261022.02_research/data_room_flags.csv), [data_room_planted.csv](../reports/20261022.02_research/data_room_planted.csv), [data_room_files.csv](../reports/20261022.02_research/data_room_files.csv), [data_room_design_numbers.py](../reports/20261022.02_research/data_room_design_numbers.py) and [data_room_design_numbers.json](../reports/20261022.02_research/data_room_design_numbers.json), [research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), [research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md), [research_landscape.md](../reports/20261022.02_research/research_landscape.md).

## Summary

- **The scripts decide the numbers. The model reads the words.** Every entry splits the work that way. A script recomputes a figure from raw files. A model reads what a script cannot: a contract clause, a footnote, a slide label, a spoken sentence.
- **Every claim carries its quote.** The model copies the exact span it relied on. A quote checker looks for that span at the stated page, slide, cell or second, and throws out any claim it cannot find.
- **A gap is shown as a gap.** When an input is missing, the entry returns "Not in the room" and names what is missing. Nothing fills the hole.
- **Labels, never probabilities.** Each entry scores itself with a short set of labels, and each label has a written rule. No entry outputs a number that pretends to be a probability. No entry says invest or pass.
- **Hollis Voice is the worked example.** The fictional company in the synthetic data room carries eight planted entries and three clean decoys. The table under "Where each planted flag is caught" maps each one to the entry that must catch it.
- **The readout opens on the best green flags and the worst red flags, then the overview.** Two script entries under [The readout](#the-readout-saturday) group every claim into nine pieces of the company, mark each piece looking strong, looking weak, mixed or not enough in the room, and pick the headline flags. Every Saturday entry names the piece its claims feed.
- **The first four scans are for Saturday.** The red-flag engine, the comp builder, market signals and the pitch video. Business frameworks, founder profiles and online presence come after Saturday.

## How every entry works

### The order of work inside a scan

1. **The script runs first.** It reads the raw files, runs the entry's mechanical check, and writes claims with `check.kind` set to `"script"` and `check.name` set to the entry's check name.
2. **The model reads second.** It gets the documents and the script's claims, and returns the entry's output shape. It writes claims with `check.kind` set to `"model"`, and a gap for every input it needed and did not find. It never recomputes a script number.
3. **The quote checker runs third.** It opens each source, looks for the quote at the locator, and marks any claim it cannot find as `unverified`. Unverified claims leave the main readout and go to a "could not verify" box.
4. **The script sets the label last.** The model proposes a label using the entry's rule. The script then applies every part of the rule that rests on a number. Where the two disagree, the script's label stands and the readout notes the override.
5. **The label sets severity.** When an entry's label is `flag`, every claim that fired the flag rule gets `severity` "flag". A `watch` label does the same with "watch". Every other claim gets "info". This is how the answer-key test in [ARCHITECTURE.md](ARCHITECTURE.md) finds a caught flag: a claim with severity "flag" and the key's check name.

### The shared Claim

Every output shape below builds on the Claim, Source, Value, Check and Gap in [ARCHITECTURE.md](ARCHITECTURE.md) ("The Claim schema"). This is the same model written as JSON Schema, so it can go straight into a model call. The schemas follow the limits of Claude's structured outputs: every object sets `additionalProperties` to `false`, and there are no numeric or length limits, because the API rejects them ([structured outputs](../reports/20261022.02_research/raw/feasibility/claude_api/build-with-claude_structured-outputs.md), section "JSON Schema limitations"). Citations cannot be combined with structured output, so each claim carries its own quote and locator instead ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), Summary and 1.8).

Paste this `$defs` block into every entry's schema before use. It belongs in `schema/`, beside the Pydantic models.

```json
{
  "$defs": {
    "Source": {
      "type": "object",
      "additionalProperties": false,
      "required": ["kind", "uri", "locator", "start_s", "end_s", "quote", "retrieved_at"],
      "properties": {
        "kind": {"type": "string", "enum": ["file", "url", "api", "video"]},
        "uri": {"type": "string", "description": "Path inside the data room, a URL, or the API call."},
        "locator": {"type": "string", "description": "For example 'slide 3', 'page 2', 'ARR_Build!E14', 'ARR_TOTAL', 'clause 7', 'line 12', 't=35-41'."},
        "start_s": {"anyOf": [{"type": "number"}, {"type": "null"}], "description": "Video only. Copied from the transcript by the script."},
        "end_s": {"anyOf": [{"type": "number"}, {"type": "null"}], "description": "Video only. Copied from the transcript by the script."},
        "quote": {"type": "string", "description": "The exact span relied on, copied character for character."},
        "retrieved_at": {"anyOf": [{"type": "string"}, {"type": "null"}], "description": "ISO date the source was read."}
      }
    },
    "Value": {
      "type": "object",
      "additionalProperties": false,
      "required": ["number", "unit", "label", "period"],
      "properties": {
        "number": {"type": "number"},
        "unit": {"type": "string", "enum": ["USD", "USD_per_month", "USD_per_year", "percent", "months", "days", "accounts", "count"]},
        "label": {"type": "string", "enum": ["arr", "mrr", "paying_accounts", "accounts_created", "nrr_12m", "grr_12m", "cohort_size", "gross_margin", "cost_of_revenue", "runway_months", "net_burn_monthly", "payroll_monthly", "hires", "headcount", "cash", "largest_customer_share", "top3_customer_share", "arpa", "acv", "cac", "payback_months", "ltv", "raise_amount", "pre_money", "post_money", "ownership", "tam", "sam", "som", "price", "contract_term", "notice_period", "signal", "other"]},
        "period": {"anyOf": [{"type": "string"}, {"type": "null"}], "description": "The month or span the number is for, for example '2026-09'."}
      }
    },
    "Check": {
      "type": "object",
      "additionalProperties": false,
      "required": ["kind", "name", "model"],
      "properties": {
        "kind": {"type": "string", "enum": ["script", "model"]},
        "name": {"type": "string", "description": "The entry's check name, plus '.read' for a model claim."},
        "model": {"anyOf": [{"type": "string"}, {"type": "null"}], "description": "Model id. The model sets null; the script fills it."}
      }
    },
    "Claim": {
      "type": "object",
      "additionalProperties": false,
      "required": ["id", "scan", "text", "value", "severity", "check", "confidence", "sources", "conflicts_with", "corroborated_by"],
      "properties": {
        "id": {"type": "string", "description": "Unique inside the scan, for example 'redflags-004'."},
        "scan": {"type": "string"},
        "text": {"type": "string", "description": "The one plain sentence the readout shows. Judged claims start with 'Reading:'."},
        "value": {"anyOf": [{"$ref": "#/$defs/Value"}, {"type": "null"}]},
        "severity": {"anyOf": [{"type": "string", "enum": ["info", "watch", "flag"]}, {"type": "null"}], "description": "The model sets null; the script sets it from the label."},
        "check": {"$ref": "#/$defs/Check"},
        "confidence": {"type": "string", "enum": ["computed", "quoted", "judged", "unverified"]},
        "sources": {"type": "array", "items": {"$ref": "#/$defs/Source"}},
        "conflicts_with": {"type": "array", "items": {"type": "string"}, "description": "Ids of claims that state a different number for the same label, unit and period."},
        "corroborated_by": {"type": "array", "items": {"type": "string"}, "description": "Ids of claims from an independent source that state the same number, within tolerance, for the same label, unit and period. The memo fills it; a scan leaves it empty."}
      }
    },
    "Gap": {
      "type": "object",
      "additionalProperties": false,
      "required": ["what", "why", "would_need"],
      "properties": {
        "what": {"type": "string", "description": "Starts with 'Not in the room:' and names what is missing."},
        "why": {"type": "string", "description": "For example 'file missing', 'tab missing', 'Akta plan returns 403', 'not stated in the file'."},
        "would_need": {"type": "string", "description": "The document or source that would close the gap."}
      }
    },
    "Piece": {
      "type": "object",
      "additionalProperties": false,
      "required": ["name", "verdict", "reason", "reason_claim_ids", "claim_ids", "corroborating_sources", "contradicting_sources"],
      "properties": {
        "name": {"type": "string", "enum": ["traction_and_revenue", "retention", "burn_and_runway", "unit_economics", "customers", "market", "comps", "team", "the_pitch_itself"]},
        "verdict": {"type": "string", "enum": ["looking_strong", "looking_weak", "mixed", "not_enough_in_the_room"]},
        "reason": {"type": "string", "description": "One line, with its number and source."},
        "reason_claim_ids": {"type": "array", "items": {"type": "string"}},
        "claim_ids": {"type": "array", "items": {"type": "string"}, "description": "Every claim in the piece, for the drill-down."},
        "corroborating_sources": {"type": "integer"},
        "contradicting_sources": {"type": "integer"}
      }
    },
    "TopFlag": {
      "type": "object",
      "additionalProperties": false,
      "required": ["kind", "piece", "rank", "text", "claim_ids"],
      "properties": {
        "kind": {"type": "string", "enum": ["green", "red"]},
        "piece": {"type": "string", "enum": ["traction_and_revenue", "retention", "burn_and_runway", "unit_economics", "customers", "market", "comps", "team", "the_pitch_itself"]},
        "rank": {"type": "integer", "description": "1 is the strongest green or the worst red."},
        "text": {"type": "string"},
        "claim_ids": {"type": "array", "items": {"type": "string"}}
      }
    }
  }
}
```

Three conventions the entries rely on:

- **`Value.label` is a fixed key.** The memo links two claims when their label, unit and period match and their numbers differ by more than the tolerance ([ARCHITECTURE.md](ARCHITECTURE.md), "How the readout merges them"). A fixed list of keys makes that match work across the deck, the model and the video.
- **Percents are percent points.** 80% is stored as `{"number": 80, "unit": "percent"}`.
- **Every claim has at least one source.** A missing input is a Gap, not a claim. The quote checker drops any claim with no sources.
- **`corroborated_by` mirrors `conflicts_with`.** The memo fills both. It links two claims as corroborating when they match on label, unit and period, agree within the tolerance, and come from independent sources (see "Piece verdicts"). A scan leaves both empty.

### Confidence labels

A fixed set, from [ARCHITECTURE.md](ARCHITECTURE.md). None of them is a probability.

| Label | Who sets it | Rule |
|---|---|---|
| `computed` | Script only | A script recomputed the number from raw files in the room or from saved API data. |
| `quoted` | Model | The quote was found at the locator and states the claim in so many words. |
| `judged` | Model | The quote was found, but the claim reads past the words, with nothing to recompute (for example, "this cohort definition drops early leavers"). The text starts with "Reading:". |
| `unverified` | Quote checker only | The quote was not found at the locator. The claim leaves the main readout. |

A missing input is never a claim. It is a Gap whose `what` starts with "Not in the room:", and the readout shows it as a gap.

### How documents reach the model

Every prompt below receives its inputs in `<doc>` blocks. The script that builds them adds a locator to every line, so the model can cite without guessing.

```text
<doc path="01_overview/pitch_deck.pdf" locator="slide">
[slide 3] ...extracted text of slide 3...
[slide 14] ...extracted text of the claims page...
</doc>
<doc path="02_financials/financial_model.xlsx" sheet="ARR_Build" locator="cell">
[ARR_Build!A{r}] Marlow Veterinary Group (pilot)
[ARR_Build!E{r}] 180000
</doc>
<doc path="03_metrics/customer_mrr_by_month.csv" locator="row">
[row 1] customer_id,month,plan,mrr,product_type
[row {n}] C0087,2026-09,Group,36000,Subscription
</doc>
<doc path="01_overview/pitch_video.mp4" locator="segment">
[seg {id} | {start_s}-{end_s}] ...transcript text of that segment...
</doc>
```

Cell addresses, row numbers and segment ids in braces are placeholders; the generator and the transcriber record the real ones. The cell values shown are Hollis Voice figures: 180,000 is the annualized pilot (PF1) and 36,000 is the largest customer's monthly fee (`BIG` in [data_room_design_numbers.py](../reports/20261022.02_research/data_room_design_numbers.py)). The column names in these examples are the ones [research_data_room.md](../reports/20261022.02_research/research_data_room.md) names (`product_type`, `arr`, `paying_accounts`, `accounts_created_cumulative`). The generator fixes the rest.

Script results reach the model in one block:

```text
<script_results>
[ ...the script's claims, as JSON, each with its id... ]
</script_results>
```

### The system prompt every model call uses

Each entry's prompt below is the user message. This is the system message for all of them.

```text
You are a diligence reader working for a venture investor. You read the documents you are given and report what they say, with the exact words that support each point.

Rules:
1. Use only the documents and script results in this message. Do not use outside knowledge about any company, market or person unless the message gives it to you as a document.
2. Every claim you write has at least one source. A source gives the document path as "uri", the locator (slide, page, cell, row, clause, line or segment), and a quote. For video, leave start_s and end_s null; the script fills them.
3. The quote is the exact span you relied on, copied character for character from the document. Use the smallest span that supports the claim. Never paraphrase inside a quote. A script will search for it, and a claim whose quote is not found is thrown out.
4. If a document the task needs is missing, or the answer is not in the documents, add a gap instead of a claim. Its "what" starts with "Not in the room:" and names what is missing. Its "why" says why (file missing, tab missing, not stated in the file). Its "would_need" names the document or source that would close it. Do not guess and do not fill the gap.
5. Script results are numbers the team computed from raw files. Do not recompute them, round them or restate them with different numbers. Refer to them by claim id.
6. When a claim has a number, put it in "value" with its unit, its label from the schema's list, and its period (or null if the document gives none). Write percents as percent points (80 for 80%). When a claim has no number, set value to null.
7. Set confidence to "quoted" when your quote states the claim directly. Set it to "judged" when you read past the words, and start the claim text with "Reading:". Never set "computed" or "unverified"; scripts set those.
8. Leave severity null. The script sets it from the label.
9. Set check.kind to "model", check.name to the check name you are given followed by ".read", and check.model to null.
10. Never give a reason for a gap, a difference or a flag unless a document states that reason. Do not guess at motive or intent.
11. Never say invest, pass, or anything that rates the company as a deal.
12. Return only JSON that matches the schema.
```

The script adds two lines to the top of each entry's prompt, `Scan: {{scan}}` and `Check name: {{check_name}}`, so the model can set `scan` and `check.name`. The check name is the one the entry gives under **Mechanical check**; for an entry that gives none, it is the entry's `framework` value.

### Settings

Thresholds are settings, not facts. The research says so for each one: "Thresholds are folk numbers unless a source defines them, so a script should take them as settings" ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), Part 2). Each default below comes from a cited source.

| Setting | Default | Where the default comes from |
|---|---|---|
| `match_tolerance` | 1 percent, relative | The PF2 check in [data_room_planted.csv](../reports/20261022.02_research/data_room_planted.csv) |
| `spoken_tolerance` | Set by the team. It must sit below the 20 percent gap of PF2b so the answer key still catches it, and at or above `match_tolerance`. | PF2b in [data_room_planted.csv](../reports/20261022.02_research/data_room_planted.csv); the 20 percent is arithmetic on its two figures (3,000,000 against 2,500,000) |
| `short_notice_days` | 90 days | Six VCs told a business magazine that some booked ARR sits on contracts the customer can cancel within three months ([research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md), row 34) |
| `min_contract_months` | 12 months | RF2 in [data_room_flags.csv](../reports/20261022.02_research/data_room_flags.csv): "Flag any ARR line whose contract is under 12 months" |
| `concentration_line` | 20 percent of MRR for the largest customer | MicroVentures' rule of thumb, via RF5 in [research_data_room.md](../reports/20261022.02_research/research_data_room.md). It says 30 to 40 percent can change valuation or deal structure. a16z gives the definition and no line. |
| `grr_line` | 80 percent | Jason Lemkin, via RF1 in [research_data_room.md](../reports/20261022.02_research/research_data_room.md): below 80 percent signals churn to fix before scaling |
| `load_factor_range` | 1.25 to 1.4 times base pay | Kruze, via RF3 in [research_data_room.md](../reports/20261022.02_research/research_data_room.md) |
| `runway_floor` | 18 months | NFX, via RF3: a raise should give at least 18 to 24 months |
| `top_green_flags`, `top_red_flags` | Set by the team before Saturday. | How many of each the headline list shows. The 1:09 PM block asks for a short list and gives no number ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). |
| `gm_context` | Bessemer average 65 to 70 percent, middle half 60 to 80; a16z 80 to 90 for software | RF6 in [research_data_room.md](../reports/20261022.02_research/research_data_room.md). Context for the reader only. Never a test. |

### Hollis Voice, the numbers the examples use

Hollis Voice is the fictional company in the synthetic data room: an AI phone agent for independent veterinary clinics, raising a Series A, with data as of 2026-09-30 ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), 3.2). Every figure in the worked examples comes from one of three files, named in each example:

- [data_room_planted.csv](../reports/20261022.02_research/data_room_planted.csv): where each flag is planted, its true value and its shown value.
- [data_room_design_numbers.json](../reports/20261022.02_research/data_room_design_numbers.json): the simulation's outputs (true MRR, true ARR, retention, runway and the rest).
- [data_room_design_numbers.py](../reports/20261022.02_research/data_room_design_numbers.py): the simulation's assumptions (plan prices, load factor, hire pay, cost shares).

Some worked examples also show arithmetic on those figures: a gap, a ratio, a share. That arithmetic was run by a Python script over the JSON and the constants in the `.py` file, not by hand, and each one is written out as a formula so a spreadsheet person can redo it.

| Figure | Value | Source |
|---|---|---|
| True subscription MRR, 2026-09 | $171,739 | `mrr_true` in the JSON |
| True recurring ARR | $2,060,868 | `arr_true_recurring` in the JSON; PF1 true value |
| Model ARR (`ARR_TOTAL`) | $2,240,868 | PF1 shown value |
| Deck ARR (slides 3 and 14) | $2,500,000 | PF2 shown value |
| Spoken ARR in the video, about 0:35 | about $3,000,000 | PF2b shown value |
| Pilot fee, Marlow Veterinary Group | $15,000 a month, six months, 30 days notice | `PILOT` in the `.py`; PF1 |
| Paying accounts now | 212 | `paying_clinics_now` in the JSON; PF7 true value |
| Accounts created, cumulative, shown as clinics | 357 | PF7 shown value |
| 12-month net retention, rebuilt and shown | 87.3% rebuilt; 102.6% shown | PF3 |
| 12-month gross retention, rebuilt | 73.4% | PF3 |
| Customers in the nine measurable cohorts | 68 rebuilt; 57 shown | PF3 |
| Hires in the plan and in the model | 24 and 8 | PF4 |
| Runway | 19 months rebuilt; 37 months in the model | PF4 |
| Average net burn, next 12 months | $480,062 rebuilt; $374,462 in the model | PF4 |
| Largest customer share of MRR | 21.0% (top three 22.2%); deck says no customer above 9% of ARR | PF5 |
| Gross margin | 58.1% rebuilt; 80% in deck and model | PF6 |
| Cash at the as-of date | $1,800,000 | `cash_at_as_of_date` in the JSON |
| Raise | $9,000,000 at $45,000,000 pre-money, $54,000,000 post | the JSON |
| SAFEs | $2,000,000 on a $12,000,000 post-money cap | the JSON |
| Plan prices | Starter $349, Standard $649, Pro $1,099 a month | `PLAN_PRICE` in the `.py` |

### Where each planted flag is caught

| Planted entry ([data_room_planted.csv](../reports/20261022.02_research/data_room_planted.csv)) | Entry that must catch it | Check name | Catchable from the seed drop, per the data-room research |
|---|---|---|---|
| PF1 Pilot booked as ARR | 1.2 ARR definition check | `arr_from_subscription_rows` | No, needs the full room |
| PF2 Deck ARR disagrees with the model | 1.5 Deck-against-model reconciliation | `deck_claim_vs_named_cell` | Yes |
| PF2b Video ARR disagrees with the deck | 4.3 Three-way disagreement check | `spoken_arr_vs_claims_page` | Yes |
| PF3 Churn hidden in the cohort tab | 1.3 Cohort retention rebuild | `rebuild_cohorts_from_customer_file` | No, needs the full room |
| PF4 Burn and runway do not match the hiring plan | 1.4 Burn against the hiring plan and runway | `payroll_from_hiring_plan_and_rerun_cash` | Yes |
| PF5 Customer concentration | 1.6 Customer concentration | `top_customer_share` | No, needs the full room |
| PF6 Gross margin excludes hosting, inference and support | 1.7 Gross margin composition | `gross_margin_from_ledger` | Yes |
| PF7 Cumulative sign-ups shown as active clinics | 1.8 Vanity metric check | `cumulative_column_shown_as_active` | Yes |
| DC1 Onboarding fee excluded from ARR correctly (decoy) | 1.2 must not flag its line | `arr_from_subscription_rows` | Yes |
| DC2 Annual prepay counted as recurring correctly (decoy) | 1.2 must not flag its line | `arr_from_subscription_rows` | No, the order form is in the full room |
| DC3 Clean cap table (decoy) | 1.10 must label it clear | `cap_table_reconcile` | Yes |

The check names are the ones the answer key's `check` field and the test in [ARCHITECTURE.md](ARCHITECTURE.md) match on. `arr_from_subscription_rows` is the data-room research's own example name (3.6). The other seven in the key are the names `data_room/generate.py` writes. Only `cap_table_reconcile` (DC3, a decoy with no `check` in the key) is set here. The seed-drop column comes from the table at the end of 3.4 in [research_data_room.md](../reports/20261022.02_research/research_data_room.md). The two decoy rows that table does not cover follow from [data_room_files.csv](../reports/20261022.02_research/data_room_files.csv): the cap table is in the seed drop and the Brookline Row order form is not.

### The parts of every entry

Each entry has exactly seven parts, in this order: **Inputs**, **The questions it asks**, **Mechanical check**, **Model reading**, **Output shape**, **How the readout scores it**, **What it must not do**. Every output shape has the same five top-level fields (`framework`, `label`, `label_reason`, `claims`, `gaps`) plus the fields that entry needs. The scan writes the claims and gaps into its ScanResult, as [ARCHITECTURE.md](ARCHITECTURE.md) describes, and the entry's own tables into the ScanResult's optional `panels`. `label_reason` names the rule that fired and the claim ids it rests on. It gives no motive.

---

## Scan 1. The red-flag engine (Saturday)

The organisers' first direction: "churn hidden in cohort charts, revenue counted as ARR when it is not recurring, burn that does not match the hiring plan, numbers that disagree between the deck and the model" ([problem tracks](../reports/20261022.01_hackathon_sources/problem_tracks.txt), Track 2). Entries 1.2 to 1.5 are those four. Entries 1.6 to 1.8 are the three extra flags the data-room research found on published lists. Entries 1.9 and 1.10 are the brief's unit economics and the cap table a first pass opens first. Entry 1.11 holds the flags investors regret most, which no file in the room can settle.

Entry 1.1 runs before all of them. It turns the deck into claims the other entries check.

### 1.1 Deck claim extraction

**Inputs**

- `01_overview/pitch_deck.pdf`, all 14 slides. Slide 14 is a claims page that lists every number with the slide where it first appears ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), 3.3).
- The sidecar `01_overview/claims.json` the generator writes in the room, used when PDF text extraction fails ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), 1.1 and 1.9).
- `01_overview/company_overview.pdf` and `06_product/product_one_pager.pdf`, for numbers repeated outside the deck.
- Slide 6 holds the cohort chart as an image. Reading it needs vision. The same numbers sit on the claims page as text ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), 3.3).

**The questions it asks**

1. What number does the deck state for each metric, on which slide, with what label and for what period?
2. What definition does the deck attach to each label ("ARR", "clinics", "net revenue retention")?
3. Does any number on a content slide differ from the same row on the claims page?
4. Does any number appear on a content slide and not on the claims page, or the other way round?
5. Which claims carry no number at all, so no file in the room can check them?

**Mechanical check**

- Parse the claims page into rows of (row label, stated value, cited slide).
- Parse each stated value to a number. "$2.5M" becomes 2,500,000. "80%" becomes 80, with unit percent. "37 months" becomes 37.
- For each row, search the cited slide's text for the same value string. Record found or not found.
- For each claim the model returns, re-parse its quote to a number and compare it with the claim's `value`. If they differ, the claim is marked `unverified`. This stops the model from turning "$2.5M" into a different number.

Worked example, Hollis Voice. The claims rows that later entries check, from [data_room_planted.csv](../reports/20261022.02_research/data_room_planted.csv):

| Claims-page row | Slide | Shown value | Checked by |
|---|---|---|---|
| ARR | 3 | $2,500,000 | 1.5 (PF2) |
| Clinics on Hollis | 3 | 357 | 1.8 (PF7) |
| Largest customer | 4 | no customer above 9% of ARR | 1.6 (PF5) |
| Gross margin | 5 | 80% | 1.7 (PF6) |
| Net revenue retention | 6 | 102.6% | 1.3 (PF3) |
| Runway | 11 | the deck's runway figure | 1.4 (PF4) |

The PF4 row in the CSV gives the model's runway (37 months) and does not state the deck's figure on its own. The script reads the deck's figure from slide 11.

**Model reading**

Only a model can read a slide's label and say what it means, and read a chart that exists only as an image.

```text
Task: extract every factual claim from this startup's pitch deck and its one-page documents.

Documents:
{{docs: pitch_deck.pdf by slide, company_overview.pdf by page, product_one_pager.pdf by page}}

For every claim:
1. Write the claim as one plain sentence in "text".
2. Set value.label to the closest key from the schema's list, or "other" when none fits. A claim with no number has value null.
3. Set value.number to the number exactly as stated, converted to a plain number ("$2.5M" is 2500000; "80%" is 80 with unit "percent"). Do not round or correct it.
4. Set value.unit and value.period. If the slide does not say which month or year the number is for, set period to null.
5. In "sources", give the document path as uri, the slide or page as locator ("slide 3", "page 1"), and a quote. Quote the exact span you relied on, including the number as printed.
6. If the slide gives a definition for the label (for example "ARR = ..." or a footnote under a chart), add a second claim whose text states the definition, with value null and the footnote as the quote.
7. Read slide 14, the claims page, row by row. Every row must become a claim. For each row, also find the content slide it cites and make a separate claim from that slide if the slide shows the number.
8. If a chart is an image, read the numbers you can see and set confidence to "judged", starting the text with "Reading:". If you cannot read it, add a gap "Not in the room: a readable chart on slide <n>".

If the deck is missing or has no readable text, return no claims and one gap: "Not in the room: the pitch deck (01_overview/pitch_deck.pdf)".

Propose the label using these rules: "extracted" if every claims-page row became a claim with a quote; "partial" if any row could not be read; "cannot_check" if the deck is missing. Put the rule you used and the ids it rests on in "label_reason".
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "claims_page_rows"],
  "properties": {
    "framework": {"type": "string", "const": "deck_claims"},
    "label": {"type": "string", "enum": ["extracted", "partial", "cannot_check"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "claims_page_rows": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["row_label", "cited_slide", "claim_id"],
        "properties": {
          "row_label": {"type": "string"},
          "cited_slide": {"anyOf": [{"type": "integer"}, {"type": "null"}]},
          "claim_id": {"type": "string"}
        }
      }
    }
  }
}
```

**How the readout scores it**

This entry feeds the others and is not shown as a flag. Its label tells the readout whether the deck side of every check is complete.

- `extracted`: every claims-page row became a claim, and every quote was found.
- `partial`: at least one row could not be read or its quote was not found. The readout lists the rows.
- `cannot_check`: no deck and no sidecar.

Its claims feed the overview piece their `value.label` names ([The readout](#the-readout-saturday), "Piece verdicts"); a claim with no value, or the label `other`, feeds **the pitch itself**.

**What it must not do**

- Correct, round or convert a number beyond turning its printed form into a plain number.
- Pick between two values the deck gives for the same metric. Both become claims, and 1.5 compares them.
- Add a claim the deck does not make, or fill a definition the deck leaves out.

### 1.2 ARR definition check

**Inputs**

- `02_financials/financial_model.xlsx`, tab `ARR_Build`: one line per customer or revenue line, including the row "Marlow Veterinary Group (pilot)" and the row "Onboarding fees (one-time, excluded)". The named cell `ARR_TOTAL`. The `README` tab, which holds the ARR definition.
- `03_metrics/customer_mrr_by_month.csv`: one row per customer per month with plan, MRR and `product_type`.
- `03_metrics/monthly_metrics.csv`, column `arr`, month 2026-09.
- `04_customers/pilot_agreement_marlow.pdf` (clauses 2, 7 and 8), `04_customers/order_form_brookline_row.pdf` (the annual prepay decoy), `04_customers/order_form_cedar_pine.pdf`.
- The deck's ARR claim from 1.1.

**The questions it asks**

1. Does ARR hold only live, recurring subscription revenue? a16z says it should exclude one-time fees, professional services and variable usage fees ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), RF2).
2. Is any pilot, evaluation or trial counted? Fortune reports VCs seeing pilots and cancellable contracts counted as ARR (same section).
3. Is a signed contract that has not gone live counted? Lighter Capital treats that as committed MRR, a separate metric (same section).
4. Does any counted line rest on a contract shorter than 12 months, or one the customer can leave on short notice?
5. Is ARR built as 12 times an all-in month, or as a best day times 365? An observer on Hacker News complained about exactly that ([research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md), row 65).
6. Does the room use an odd revenue label such as "Quarterly MRR"? A SaaS investor calls such labels an immediate flag (same file, row 15).
7. Are letters of intent or verbal agreements counted? a16z says they are neither revenue nor bookings ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), RF2).
8. Does the definition in the `README` tab match how `ARR_Build` actually adds up?

**Mechanical check**

Check name: `arr_from_subscription_rows`. The answer key uses it for PF1 (pilot booked as ARR), and the two decoys DC1 (onboarding fee) and DC2 (annual prepay), which must not fire it. The name is the one the data-room research's answer-key example uses.

```
ARR_recurring = 12 × SUM(mrr) over rows of customer_mrr_by_month.csv
                where month = as-of month AND product_type = "Subscription"
excess        = ARR_TOTAL − ARR_recurring
excess_share  = excess ÷ ARR_recurring
flag the total if excess_share > match_tolerance
```

Line test, for each line counted in `ARR_TOTAL`:

- Flag the line if its `product_type` is anything other than "Subscription".
- Flag the line if its contract term is under `min_contract_months` (12) or its notice period is `short_notice_days` (90) or less.
- An annual prepaid subscription counts once as recurring. Cash arriving up front does not make it a flag.

Worked example, Hollis Voice:

- `ARR_recurring` = 12 × $171,739 = $2,060,868 (`mrr_true` and `arr_true_recurring` in [data_room_design_numbers.json](../reports/20261022.02_research/data_room_design_numbers.json)).
- `ARR_TOTAL` = $2,240,868 (PF1 shown value, [data_room_planted.csv](../reports/20261022.02_research/data_room_planted.csv)).
- `excess` = $2,240,868 − $2,060,868 = $180,000. That is 12 × $15,000, the pilot fee annualized (`pilot_fee_per_month` and `pilot_arr_counted` in the JSON).
- `excess_share` = $180,000 ÷ $2,060,868 = 8.7%, above the 1 percent tolerance (scripted arithmetic on the figures above).
- The pilot line fails the line test three ways: product type is a pilot, the term is six months, and notice is 30 days. Its total contracted fees are $90,000, which is 6 × $15,000 (PF1 true value).
- Decoy DC1: the $500 onboarding fee sits on its own row marked excluded. It is not in `ARR_TOTAL`. The line test passes it.
- Decoy DC2: Brookline Row Veterinary prepays a year. Its CSV rows are Subscription and its term is 12 months. The line test passes it.

**Model reading**

Only a model can read a contract for a pilot clause, a notice period and a duty to convert, or read a line label that a script cannot classify.

```text
Task: check whether this startup's ARR counts only recurring revenue.

Documents:
{{docs: financial_model.xlsx tabs README and ARR_Build by cell; every contract in 04_customers/ by page and clause; the deck's ARR claim}}

Script results:
{{script_results: the ARR recompute, the excess, and each ARR_Build line with its product_type from customer_mrr_by_month.csv}}

Answer these questions with claims:
1. What definition of ARR does the README tab give? Quote it.
2. For each line in ARR_Build, what kind of revenue is it: subscription, pilot, one_time, services, usage, loi_or_verbal, or unknown? Use the line label and, where a contract exists for that customer, the contract.
3. For each contract: what is the term in months, how many days of notice end it, and does the customer have to convert or pay anything after the first term? Quote the clause for each answer.
4. Is any revenue label unusual, such as "Quarterly MRR" or a single day annualized? Quote it.
5. Does the README definition match how ARR_Build adds up? If not, say which line breaks it, citing the cell.

Quote the exact span you relied on for every claim. If a contract for a counted line is not in the room, add a gap "Not in the room: the contract for <line label>". Do not assume a pilot will convert. Do not say why a line was included.

Fill "lines" with one entry per ARR_Build line. Propose the label using the rules in "How the readout scores it" below, and name the rule and claim ids in "label_reason".

Label rules:
- "flag": the script's excess share is above tolerance, or any counted line is pilot, one_time, services, usage or loi_or_verbal.
- "watch": no flag, but a counted line has a term under 12 months, notice of 90 days or less, or the README definition is missing or unusual.
- "clear": the recompute matches ARR_TOTAL within tolerance and every counted line is a subscription of 12 months or more.
- "cannot_check": ARR_Build is missing.
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "lines"],
  "properties": {
    "framework": {"type": "string", "const": "arr_definition"},
    "label": {"type": "string", "enum": ["flag", "watch", "clear", "cannot_check"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "lines": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["line_label", "cell", "counted_in_arr", "kind", "term_months", "notice_days", "must_convert", "claim_ids"],
        "properties": {
          "line_label": {"type": "string"},
          "cell": {"type": "string"},
          "counted_in_arr": {"type": "boolean"},
          "kind": {"type": "string", "enum": ["subscription", "pilot", "one_time", "services", "usage", "loi_or_verbal", "unknown"]},
          "term_months": {"anyOf": [{"type": "number"}, {"type": "null"}]},
          "notice_days": {"anyOf": [{"type": "number"}, {"type": "null"}]},
          "must_convert": {"anyOf": [{"type": "boolean"}, {"type": "null"}]},
          "claim_ids": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
```

**How the readout scores it**

- `flag`: the recompute falls short of `ARR_TOTAL` by more than `match_tolerance`, or any counted line is a pilot, one-time fee, service, usage fee, letter of intent or verbal deal.
- `watch`: no flag, but a counted line has a term under 12 months or notice of 90 days or less, or the definition is missing or uses an odd label.
- `clear`: the recompute matches within tolerance and every counted line passes the line test. On Hollis Voice the entry's label is `flag` because of the pilot, but the onboarding fee and the Brookline Row prepay must not get a flag claim of their own.
- `cannot_check`: `ARR_Build` is missing. With the seed drop only, the customer file and the pilot agreement are absent. The entry then returns `watch` if a counted line's label names a pilot, and otherwise `cannot_check`. The data-room research counts the full PF1 catch as needing the full room.

Its claims feed the overview's **traction and revenue** piece ([The readout](#the-readout-saturday), "Piece verdicts").

**What it must not do**

- Give a reason the pilot was counted. Nothing in the room states one.
- Count committed or signed-but-not-live revenue toward recurring ARR, or assume a pilot converts.
- Flag the onboarding fee or the annual prepay. Both are decoys, and the answer-key test counts a flag on either as a false positive.

### 1.3 Cohort retention rebuild

**Inputs**

- `03_metrics/customer_mrr_by_month.csv`: the raw customer file.
- `02_financials/financial_model.xlsx`, tab `Cohorts`: the month-0 counts per cohort, the NRR row, and the note "Cohort = customers still active after onboarding".
- `01_overview/pitch_deck.pdf`, slide 6 (the cohort chart, an image) and the claims row "Net revenue retention".

**The questions it asks**

1. Does the room show net retention only, or gross retention beside it? a16z says net churn understates the loss because upsells blend in ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), RF1).
2. Do the cohort sizes in the tab match the number of customers who started in each month in the raw file?
3. Are customers who left early dropped from the cohorts? The tab's note is the place to look.
4. Are all cohorts shown, including the newest, or only the best ones? a16z lists selectively presented metrics as a red flag (same section).
5. Does retention level off after 6 or 12 months, and do newer cohorts do better than older ones? Those are a16z's two trends (same section).
6. Is the retention base low on purpose? Bain Capital Ventures says investors rerun the raw file, so an artificially low base never survives (same section).
7. Is churn split by plan or customer size? Jason Lemkin says to split it that way (same section).

**Mechanical check**

Check name: `rebuild_cohorts_from_customer_file`. The answer key uses it for PF3 (churn hidden in the cohort tab).

For each cohort c (customers whose first month with MRR above zero is month c), and for each customer i in it:

```
start_c  = SUM over i of MRR_i(c)
end_c    = SUM over i of MRR_i(c + 12)
capped_c = SUM over i of MIN( MRR_i(c + 12), MRR_i(c) )

NRR_12 = SUM over c of end_c   ÷ SUM over c of start_c
GRR_12 = SUM over c of capped_c ÷ SUM over c of start_c
```

The sums run over cohorts with 12 months of data. Then:

- Compare each cohort's raw customer count with the tab's month-0 count.
- Compare `NRR_12` with the tab's NRR row and the deck's claim.
- Run a16z's test: for each month k, compare the retention of later cohorts at month k with earlier cohorts at month k.

Worked example, Hollis Voice (PF3 in [data_room_planted.csv](../reports/20261022.02_research/data_room_planted.csv)):

- Nine cohorts have 12 months of data (`cohorts_with_12m_data` in [data_room_design_numbers.json](../reports/20261022.02_research/data_room_design_numbers.json)). They are the cohorts that start in 2025-01 through 2025-09, per the month labels in [data_room_design_numbers.py](../reports/20261022.02_research/data_room_design_numbers.py).
- Raw: 68 customers, `NRR_12` 87.3%, `GRR_12` 73.4%.
- Tab: 57 customers, NRR 102.6%. The 11 customers missing (68 − 57) are the ones who left within two months.
- The tab's NRR is 15.3 points above the rebuilt NRR (102.6 − 87.3, scripted arithmetic).
- `GRR_12` of 73.4% is under the `grr_line` of 80 percent.

**Model reading**

Only a model can read the tab's note and say what the definition leaves out, and read a chart that exists only as an image.

```text
Task: check whether this startup's cohort retention hides churn.

Documents:
{{docs: financial_model.xlsx tab Cohorts by cell, including any notes; pitch_deck.pdf slide 6 (text and image) and slide 14}}

Script results:
{{script_results: rebuilt cohort counts, NRR_12 and GRR_12 from customer_mrr_by_month.csv; the tab's counts and NRR; the newer-versus-older comparison}}

Answer these questions with claims:
1. How does the Cohorts tab define a cohort? Quote the note or header.
2. Reading that definition, which customers does it leave out of the starting count? Start the text with "Reading:" and quote the definition.
3. Is the retention figure on slide 6 and in the tab net retention, gross retention, or unlabeled? Quote the label.
4. Does slide 6 show every cohort the tab holds, or only some? If the chart is an image, read what you can and set confidence to "judged".
5. Does the room show gross retention anywhere? If not, add a gap "Not in the room: gross retention".

Quote the exact span you relied on for every claim. If the Cohorts tab is missing, add a gap "Not in the room: the Cohorts tab in financial_model.xlsx". Do not say the definition was chosen to hide churn. Say only what it includes and excludes.

Propose the label using these rules, and name the rule and claim ids in "label_reason":
- "flag": the tab's cohort counts are lower than the rebuilt counts, or the claimed retention is above the rebuilt NRR by more than tolerance.
- "watch": the numbers reconcile, but rebuilt GRR is below 80 percent, newer cohorts do worse than older ones, or only net retention is shown.
- "clear": counts and retention reconcile, GRR is at or above 80 percent, and both net and gross are shown.
- "cannot_check": the raw customer file is missing and the tab's note does not drop anyone.
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "cohorts"],
  "properties": {
    "framework": {"type": "string", "const": "cohort_retention"},
    "label": {"type": "string", "enum": ["flag", "watch", "clear", "cannot_check"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "cohorts": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["cohort_month", "count_raw_claim_id", "count_shown_claim_id", "definition_claim_id"],
        "properties": {
          "cohort_month": {"type": "string"},
          "count_raw_claim_id": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "count_shown_claim_id": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "definition_claim_id": {"anyOf": [{"type": "string"}, {"type": "null"}]}
        }
      }
    }
  }
}
```

**How the readout scores it**

- `flag`: the tab's cohort counts are below the raw counts, or the claimed retention is above the rebuilt NRR by more than `match_tolerance`.
- `watch`: the numbers reconcile, but rebuilt GRR is below `grr_line`, newer cohorts do worse than older ones, or only net retention is shown.
- `clear`: counts and retention reconcile, GRR is at or above the line, and both net and gross appear.
- `cannot_check`: the raw customer file is missing. With the seed drop only, the entry still reads the tab's note. If the note drops early leavers, it returns `watch` with a judged claim. The data-room research counts the full PF3 catch as needing the full room.

Its claims feed the overview's **retention** piece ([The readout](#the-readout-saturday), "Piece verdicts").

**What it must not do**

- Say the definition was chosen to hide churn. It reports what the definition includes and excludes.
- Drop, add or adjust any customer in the rebuild. The raw file is used as it is.
- Invent a segment split the room does not hold.

### 1.4 Burn against the hiring plan and runway

**Inputs**

- `05_team/hiring_plan.csv`: one row per planned hire with role, department, start month and base pay (24 rows).
- `02_financials/financial_model.xlsx`: tab `Assumptions` (the loaded-cost factor), tab `P&L` forecast row "Payroll", tab `Hiring_Plan`, tab `Cash_Runway` and its named cell `RUNWAY_MONTHS`.
- `01_overview/pitch_deck.pdf`, slide 11 (plan, use of funds and runway) and its claims row "Runway"; slide 12 (hiring).

**The questions it asks**

1. Does the model's payroll include every hire in the plan, at the plan's start month and pay?
2. Is the loaded-cost factor fair? Kruze's rule of thumb is 1.25 to 1.4 times base pay ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), RF3).
3. Are start dates realistic? Kruze says to assume hires start a month or two later than hoped (same section).
4. What runway follows from cash, the raise and the full plan? Does the deck's runway match?
5. Does the raise give at least 18 to 24 months, the range NFX gives (same section)?
6. How does burn to date compare with ARR? One SaaS investor says more than $3m to $4m burned on the way to $1m ARR makes a deal hard ([research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md), row 16). That is context for the reader, not a test.

**Mechanical check**

Check name: `payroll_from_hiring_plan_and_rerun_cash`. The answer key uses it for PF4 (burn and runway do not match the hiring plan).

```
loaded_monthly_cost(hire) = base_pay × load_factor ÷ 12, from the hire's start month
payroll_plan(t)  = payroll_now + SUM of loaded_monthly_cost for every hire with start ≤ t
net_burn(t)      = payroll(t) + other_opex(t) + cost_of_revenue(t) − revenue(t)
cash(t)          = cash(t − 1) + financing(t) − net_burn(t)
runway           = the last month t with cash(t) > 0
hires_in_model   = hiring-plan rows whose cost appears in the P&L Payroll row
```

Run the cash roll twice. First with the model's own payroll. Then with `payroll_plan`. Compare both with `RUNWAY_MONTHS` and the deck.

Worked example, Hollis Voice:

- The plan holds 24 hires. The model counts 8 (PF4 in [data_room_planted.csv](../reports/20261022.02_research/data_room_planted.csv)). That leaves 16 hires missing (24 − 8, scripted arithmetic).
- One planned hire costs $165,000 × 1.28 ÷ 12 = $17,600 a month (`hire_base` and `load` in [data_room_design_numbers.py](../reports/20261022.02_research/data_room_design_numbers.py); scripted arithmetic). Once all 16 have started, the missing hires come to 16 × $17,600 = $281,600 a month (scripted arithmetic).
- Cash at 2026-09-30 is $1,800,000. The $9,000,000 Series A lands in 2027-01 in the simulation ([data_room_design_numbers.json](../reports/20261022.02_research/data_room_design_numbers.json) and the `.py`).
- Rebuilt runway: 19 months. The model's runway: 37 months (PF4). The gap is 18 months (scripted arithmetic).
- Average net burn over the next 12 months: $480,062 rebuilt against $374,462 in the model (PF4). The gap is $105,600 a month (scripted arithmetic).
- The load factor of 1.28 sits inside Kruze's range. The rebuilt 19 months sits inside NFX's 18 to 24. So the level is not the flag here. The disagreement is.

**Model reading**

Only a model can read start dates or pay notes that sit in text, and match a plan role to the P&L line that should carry it.

```text
Task: check whether this startup's burn and runway include its own hiring plan.

Documents:
{{docs: hiring_plan.csv by row; financial_model.xlsx tabs Assumptions, P&L, Hiring_Plan and Cash_Runway by cell, with any notes; pitch_deck.pdf slides 11, 12 and 14}}

Script results:
{{script_results: payroll rebuilt from the plan, hires counted in the model, both cash rolls, both runways, both average burns}}

Answer these questions with claims:
1. What loaded-cost factor does the Assumptions tab use? Quote the cell.
2. Do any notes in the model or the plan say hires will start later than the plan's start month, or at different pay? Quote them.
3. Which roles in hiring_plan.csv have no matching line or month in the Hiring_Plan tab or the P&L Payroll row? List each with its row in hiring_plan.csv.
4. What runway and use of funds does slide 11 state? Quote them.
5. Does slide 12 show a hiring number? Quote it.

Quote the exact span you relied on for every claim. If hiring_plan.csv or the Cash_Runway tab is missing, add a gap "Not in the room: <file or tab>". Do not suggest that hires will be delayed to make the numbers fit. Do not predict when the company runs out of cash beyond the script's runway, which is the plan's own numbers rerun.

Propose the label using these rules, and name the rule and claim ids in "label_reason":
- "flag": the rebuilt runway differs from RUNWAY_MONTHS or the deck's runway by more than tolerance, or the model counts fewer hires than the plan inside the forecast window.
- "watch": no flag, but the rebuilt runway is under 18 months, or the load factor is outside 1.25 to 1.4.
- "clear": runway and hires reconcile, runway is at least 18 months, and the load factor is inside the range.
- "cannot_check": the hiring plan or the cash tab is missing.
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "missing_hires"],
  "properties": {
    "framework": {"type": "string", "const": "burn_hiring_runway"},
    "label": {"type": "string", "enum": ["flag", "watch", "clear", "cannot_check"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "missing_hires": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["plan_row", "role", "start_month", "claim_id"],
        "properties": {
          "plan_row": {"type": "string"},
          "role": {"type": "string"},
          "start_month": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "claim_id": {"type": "string"}
        }
      }
    }
  }
}
```

**How the readout scores it**

- `flag`: the rebuilt runway differs from `RUNWAY_MONTHS` or the deck by more than `match_tolerance`, or the model counts fewer hires than the plan inside the forecast window.
- `watch`: no flag, but the rebuilt runway is under `runway_floor`, or the load factor sits outside `load_factor_range`.
- `clear`: runway and hire count reconcile, runway is at or above the floor, and the load factor is in range.
- `cannot_check`: the hiring plan or the cash tab is missing.

Its claims feed the overview's **burn and runway** piece ([The readout](#the-readout-saturday), "Piece verdicts"), except a `headcount` claim, which feeds team.

**What it must not do**

- Pick a load factor or a hiring delay of its own to make the numbers meet.
- Present the rebuilt runway as a forecast. It is the plan's own numbers, rerun with every hire in it.
- Say why the model left hires out.

### 1.5 Deck-against-model reconciliation

**Inputs**

- The deck's claims from 1.1.
- Named cells in `02_financials/financial_model.xlsx`: `ARR_TOTAL`, `GM_PCT`, `RUNWAY_MONTHS`.
- The last row of `03_metrics/monthly_metrics.csv` (`mrr`, `arr`, `paying_accounts`, `accounts_created_cumulative`).
- `01_overview/company_overview.pdf`.
- The rebuilt values from 1.2, 1.3, 1.4, 1.6, 1.7 and 1.8, so each pair can also be set against the raw data.

**The questions it asks**

1. For each metric and period, do the deck, the model, the metrics export and the overview state the same number?
2. When two documents use different labels ("clinics", "paying accounts", "logos"), do they mean the same thing?
3. When two documents use the same label, do they mean the same thing, for the same date?
4. When the deck and the model agree, do they both agree with the raw data?

CRV, a16z and Visible all name this flag ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), RF4). It is also the flag investors name most in public ([research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md), "What this means for Tricorder").

**Mechanical check**

Check name: `deck_claim_vs_named_cell`. The answer key uses it for PF2 (deck ARR disagrees with the model).

```
pair every two claims with the same metric and period
gap_rel = | value_a − value_b | ÷ | value_b |, where b is the model's figure, or the rebuilt figure when the pair includes one
flag the pair if gap_rel > match_tolerance
```

Convert before comparing: `GM_PCT` holds 0.8 in the model, the deck says 80%, and the schema stores percent points. Multiply the model's value by 100 so both read 80, or the check reports a false conflict.

Worked example, Hollis Voice. The four ARR figures, from the table in 3.4 of [research_data_room.md](../reports/20261022.02_research/research_data_room.md):

| Source | ARR | Against the model (scripted arithmetic) |
|---|---|---|
| Rebuilt recurring ARR | $2,060,868 | |
| Model, `ARR_TOTAL` | $2,240,868 | |
| Deck, slides 3 and 14 | $2,500,000 | $259,132 higher, 11.6% |
| Founder video, about 0:35 | about $3,000,000 | handled in 4.3 |

- Deck against model: $2,500,000 ÷ $2,240,868 − 1 = 11.6%, above the 1 percent tolerance. This is PF2. The gap of $259,132 is the figure in [data_room_planted.csv](../reports/20261022.02_research/data_room_planted.csv). Nothing in the room explains it (data-room research, 3.4).
- Deck against rebuilt: $2,500,000 ÷ $2,060,868 − 1 = 21.3% (scripted arithmetic).
- Gross margin: the deck and `GM_PCT` both say 80% (PF6). The pair agrees. The rebuild in 1.7 says 58.1%. So the pattern is "deck and model agree, raw data disagrees", and the readout shows it that way.
- Clinics: the deck says 357. `paying_accounts` says 212 (PF7). The labels differ. The model reading decides whether "clinics on Hollis" means paying accounts; 1.8 then tests the column.

**Model reading**

Only a model can match labels that differ and spot a different definition or date behind the same label.

```text
Task: match each number in the pitch deck to the same number elsewhere in the data room, so a script can compare them.

Documents:
{{docs: the deck claims from 1.1; financial_model.xlsx README tab and the named cells ARR_TOTAL, GM_PCT and RUNWAY_MONTHS with their labels; monthly_metrics.csv header and last row; company_overview.pdf}}

Script results:
{{script_results: every claim from 1.1 and from the rebuilds in 1.2 to 1.8, with ids}}

For each deck claim:
1. Find the claim or cell elsewhere in the room that states the same metric for the same period. Say how they match: "same_label", "same_definition_different_label", "label_matches_definition_differs", or "period_differs".
2. When labels differ ("clinics" against "paying_accounts"), say whether the documents define them the same way. Quote both definitions. If either has no definition, say so and set confidence to "judged".
3. When the same label has a different date or definition behind it, quote both.
4. If a deck number has no counterpart anywhere in the room, add a gap "Not in the room: a source for the deck's <label> on slide <n>".

Quote the exact span you relied on for every claim. Do not compare the numbers yourself. Do not say which number is right. Do not explain why two numbers differ.

Fill "pairs" with one entry per match. Propose the label using these rules, and name the rule and claim ids in "label_reason":
- "flag": any pair's gap is above tolerance in the script results.
- "watch": every pair is within tolerance, but at least one pair matches on a different definition or a different period.
- "clear": every pair is within tolerance on the same definition and period.
- "cannot_check": the deck or the model is missing.
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "pairs"],
  "properties": {
    "framework": {"type": "string", "const": "deck_model_reconcile"},
    "label": {"type": "string", "enum": ["flag", "watch", "clear", "cannot_check"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "pairs": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["metric", "period", "deck_claim_id", "other_claim_id", "match_basis"],
        "properties": {
          "metric": {"type": "string"},
          "period": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "deck_claim_id": {"type": "string"},
          "other_claim_id": {"type": "string"},
          "match_basis": {"type": "string", "enum": ["same_label", "same_definition_different_label", "label_matches_definition_differs", "period_differs"]}
        }
      }
    }
  }
}
```

**How the readout scores it**

- `flag`: any pair differs by more than `match_tolerance`. Each flagged pair fills both claims' `conflicts_with`, and the readout shows the pair at the top.
- `watch`: every pair is within tolerance, but one matches on a different definition or period.
- `clear`: every pair is within tolerance, on the same definition and period.
- `cannot_check`: the deck or the model is missing.

Its claims feed the overview piece their `value.label` names ([The readout](#the-readout-saturday), "Piece verdicts"); a claim with no value, or the label `other`, feeds **the pitch itself**.

**What it must not do**

- Average two numbers, or call one of them right. The readout shows both with their sources and the rebuilt figure beside them.
- Explain a gap. On Hollis Voice, nothing in the room explains the extra $259,132, and the readout says exactly that.
- Treat a rounded deck figure as a mismatch when it sits within tolerance.

### 1.6 Customer concentration

**Inputs**

- `03_metrics/customer_mrr_by_month.csv`, as-of month, including customer `C0087`, the largest (ids are ordinary; the generator reviser renamed `C-BIG` and `P-MARLOW` to `C0087` and `C0219`).
- `04_customers/order_form_cedar_pine.pdf`: the largest customer, 40 locations, a 24-month term ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), 3.3).
- `01_overview/pitch_deck.pdf`, slide 4 and the claims row "Largest customer".

**The questions it asks**

1. What share of MRR comes from the largest customer, and from the largest three? a16z defines concentration as the largest customers' revenue over total revenue for the same period ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), RF5).
2. Does the deck's claim about concentration match the raw file?
3. Are several customer rows really one buyer (a group of clinics under one owner)?
4. When does the largest customer's contract end, and can it leave early? Those terms decide how risky the share is (same section).
5. Do the founders state a plan to spread revenue? MicroVentures says early concentration is not a red flag when they do (same section).

**Mechanical check**

Check name: `top_customer_share`. The answer key uses it for PF5 (customer concentration).

```
share_top1 = MRR of the largest customer at the as-of month ÷ total MRR at the as-of month
share_top3 = SUM of the three largest customers' MRR ÷ total MRR
flag if share_top1 is above the deck's stated ceiling by more than match_tolerance
mark the concentration_line if share_top1 > 20 percent
```

Group rows that share a parent before ranking. A customer with 40 locations is one customer.

Worked example, Hollis Voice (PF5 in [data_room_planted.csv](../reports/20261022.02_research/data_room_planted.csv)):

- `share_top1` = $36,000 ÷ $171,739 = 21.0% (`mrr_after` of `BIG` in [data_room_design_numbers.py](../reports/20261022.02_research/data_room_design_numbers.py) and `mrr_true` in the JSON; scripted arithmetic).
- `share_top3` = 22.2% (PF5).
- The deck says no customer is above 9% of ARR.
- The deck's figure is "of ARR", so the script also runs it on the model's ARR: $36,000 × 12 ÷ $2,240,868 = 19.3% (scripted arithmetic). The flag holds on either basis.
- 21.0% is above the 20 percent line, and below the 30 to 40 percent band MicroVentures says can change deal terms.

**Model reading**

Only a model can read the order form for term, renewal and exit, and tell that two customer names belong to one owner.

```text
Task: check how much of this startup's revenue depends on its largest customers, and how firmly that revenue is held.

Documents:
{{docs: the largest customers' rows from customer_mrr_by_month.csv; every order form in 04_customers/ by page and clause; pitch_deck.pdf slides 4 and 14}}

Script results:
{{script_results: share_top1, share_top3, both on MRR and on model ARR, and the customer ids behind them}}

Answer these questions with claims:
1. What does slide 4 say about the largest customer or about concentration? Quote it.
2. For the largest customer: what is the term, the renewal date, the notice needed to end it, and any right to end early or cut locations? Quote each clause.
3. Do any customer names in the rows look like parts of one group (shared owner, "& Hospitals", numbered locations)? Quote the names and set confidence to "judged".
4. Does any document state a plan to spread revenue across more customers? Quote it, or add a gap "Not in the room: a plan to reduce concentration".

Quote the exact span you relied on for every claim. If the order form for the largest customer is missing, add a gap "Not in the room: the contract for <customer>". Do not judge whether the relationship is healthy and do not assume it renews.

Propose the label using these rules, and name the rule and claim ids in "label_reason":
- "flag": share_top1 is above the deck's stated ceiling by more than tolerance.
- "watch": no flag, but share_top1 is above 20 percent, or the largest customer can leave on 90 days notice or less.
- "clear": the deck's figure matches, share_top1 is at or below 20 percent, and the largest contract runs at least 12 months with more than 90 days notice.
- "cannot_check": the customer file is missing.
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "largest_customers"],
  "properties": {
    "framework": {"type": "string", "const": "customer_concentration"},
    "label": {"type": "string", "enum": ["flag", "watch", "clear", "cannot_check"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "largest_customers": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["customer_id", "name", "group_with", "term_months", "notice_days", "renewal_date", "claim_ids"],
        "properties": {
          "customer_id": {"type": "string"},
          "name": {"type": "string"},
          "group_with": {"type": "array", "items": {"type": "string"}},
          "term_months": {"anyOf": [{"type": "number"}, {"type": "null"}]},
          "notice_days": {"anyOf": [{"type": "number"}, {"type": "null"}]},
          "renewal_date": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "claim_ids": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
```

**How the readout scores it**

- `flag`: `share_top1` is above the deck's stated ceiling by more than `match_tolerance`.
- `watch`: no flag, but `share_top1` is above `concentration_line`, or the largest customer can leave on `short_notice_days` or less.
- `clear`: the deck matches, the share is at or below the line, and the largest contract runs at least `min_contract_months` with longer notice.
- `cannot_check`: the customer file is missing. The data-room research counts PF5 as needing the full room.

Its claims feed the overview's **customers** piece ([The readout](#the-readout-saturday), "Piece verdicts").

**What it must not do**

- Say whether the big customer is happy, likely to renew or likely to leave.
- Split one buyer into its locations to make the share look smaller.
- Treat concentration on its own as a reason to pass. The flag here is the deck's claim against the file.

### 1.7 Gross margin composition

**Inputs**

- `02_financials/expense_ledger.csv`: expense lines by month with vendor and category (full room only).
- `02_financials/financial_model.xlsx`, tab `P&L`: the cost of revenue rows, the row "Cloud hosting and model inference" (under R&D), the row "Customer support specialists" (under S&M), and the named cell `GM_PCT`.
- `01_overview/pitch_deck.pdf`, slide 5 and the claims row "Gross margin".

**The questions it asks**

1. Which costs sit in cost of revenue, and which delivery costs sit elsewhere? a16z says gross profit should include all costs of delivery and support ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), RF6).
2. Are hosting, model inference, telephony, embedded software licences and support staff all in cost of revenue? Tunguz and Stripe both list these (same section).
3. What is the margin with every delivery cost included?
4. Does the deck's margin match the model's, and both the rebuilt one?
5. Which ledger lines are too vague to place ("platform costs", "customer experience salaries")?

**Mechanical check**

Check name: `gross_margin_from_ledger`. The answer key uses it for PF6 (gross margin leaves out hosting, inference and support).

```
cost_of_revenue_full = SUM of ledger lines tagged hosting, inference, telephony, embedded licence or support
gross_margin_rebuilt = 1 − cost_of_revenue_full ÷ revenue
compare gross_margin_rebuilt with GM_PCT and with the deck
```

With the seed drop only, there is no ledger. The script then rebuilds from the P&L rows: it moves "Cloud hosting and model inference" and "Customer support specialists" into cost of revenue and recomputes. The data-room research counts PF6 as catchable from the seed drop this way.

Worked example, Hollis Voice. The cost shares come from [data_room_design_numbers.py](../reports/20261022.02_research/data_room_design_numbers.py). The results are PF6 in [data_room_planted.csv](../reports/20261022.02_research/data_room_planted.csv). The dollar lines are scripted arithmetic on both.

| Line | Monthly amount | In shown cost of revenue? |
|---|---|---|
| Revenue basis: subscription MRR $171,739 plus the pilot fee $15,000 | $186,739 | |
| Telephony (15%) and embedded licences (5%) | $37,347.80 | Yes |
| Cloud hosting and model inference (11%) | $20,541.29 | No, under R&D |
| Support: 2 people × $95,000 × 1.28 ÷ 12 | $20,266.67 | No, under S&M |

- Shown: 1 − $37,347.80 ÷ $186,739 = 80%. The deck and `GM_PCT` both say 80%.
- Rebuilt: 1 − ($37,347.80 + $20,541.29 + $20,266.67) ÷ $186,739 = 58.1%.
- The gap is 21.9 points (scripted arithmetic).
- Context only: Bessemer reports an average of 65 to 70 percent; a16z says software should sit at 80 to 90 ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), RF6). Neither is the test. The test is the deck against the rebuild.

**Model reading**

Only a model can classify a vague ledger line or read where the P&L places a cost.

```text
Task: check whether this startup's gross margin includes every cost of delivering its product.

Documents:
{{docs: expense_ledger.csv rows (vendor, category, description), or the P&L tab by cell if there is no ledger; pitch_deck.pdf slides 5 and 14}}

Script results:
{{script_results: the shown and rebuilt margins, and the lines the script could tag by category}}

Answer these questions with claims:
1. For each ledger line or P&L row the script could not tag, is it a delivery cost (hosting, model inference, telephony, a licence built into the product, support or onboarding staff), an operating cost, or unclear? Quote the line's vendor, category and description.
2. Which P&L section holds each delivery cost? Quote the section header and the row label.
3. Does slide 5 define gross margin or say what it includes? Quote it, or add a gap "Not in the room: a gross margin definition".

Quote the exact span you relied on for every claim. When a line could fit either way, mark it "unclear". Do not move it. Do not compare the margin with any benchmark.

Fill "lines" with one entry per line you classified. Propose the label using these rules, and name the rule and claim ids in "label_reason":
- "flag": the rebuilt margin is below the deck's or GM_PCT by more than tolerance.
- "watch": no flag, but one or more lines are "unclear" and together they could move the margin past tolerance.
- "clear": the rebuilt margin matches within tolerance and no line is unclear.
- "cannot_check": neither the ledger nor the P&L tab is in the room.
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "lines"],
  "properties": {
    "framework": {"type": "string", "const": "gross_margin"},
    "label": {"type": "string", "enum": ["flag", "watch", "clear", "cannot_check"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "lines": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["locator", "shown_section", "class", "claim_id"],
        "properties": {
          "locator": {"type": "string"},
          "shown_section": {"type": "string", "enum": ["cost_of_revenue", "rnd", "sales_marketing", "g_and_a", "other"]},
          "class": {"type": "string", "enum": ["delivery_cost", "operating_cost", "unclear"]},
          "claim_id": {"type": "string"}
        }
      }
    }
  }
}
```

**How the readout scores it**

- `flag`: the rebuilt margin is below the deck's or `GM_PCT` by more than `match_tolerance`.
- `watch`: no flag, but unclear lines could move the margin past tolerance.
- `clear`: the rebuild matches and nothing is unclear.
- `cannot_check`: neither the ledger nor the P&L is in the room.

Its claims feed the overview's **unit economics** piece ([The readout](#the-readout-saturday), "Piece verdicts").

**What it must not do**

- Use a benchmark as a pass or fail. Benchmarks appear beside the result as context, with their sources.
- Move an unclear line into or out of cost of revenue. It stays unclear and the readout says how much it could matter.
- Say why a cost was placed under R&D or S&M.

### 1.8 Vanity metric check

**Inputs**

- `03_metrics/monthly_metrics.csv`: 21 months of `mrr`, `arr`, `paying_accounts`, `accounts_created_cumulative` and calls handled.
- `01_overview/pitch_deck.pdf`, slide 3 and the claims row "Clinics on Hollis".

**The questions it asks**

1. Is any count in the deck the last value of a column that can only go up (accounts created, downloads, users ever)? a16z calls registered users a cumulative metric that can rise while a business shrinks ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), RF7).
2. Does the deck's label say what the count means ("active", "paying", "on Hollis")?
3. Is there an active or paying count in the room, and does it differ?
4. Is a cumulative chart used to show growth? a16z says cumulative charts are not a valid measure of growth (same section).

**Mechanical check**

Check name: `cumulative_column_shown_as_active`. The answer key uses it for PF7 (cumulative sign-ups shown as active clinics).

```
for each numeric column x in monthly_metrics.csv:
    never_falls(x) = TRUE if x(t) ≥ x(t − 1) for every month t
for each count claim in the deck:
    matches = columns whose last value equals the claim
flag if the claim matches a column that is cumulative by name or definition,
     and an active or paying column exists whose last value differs by more than match_tolerance
```

A growing company's paying count can also never fall. So `never_falls` only marks candidates. The column name and the model reading decide which column is the cumulative one and which is the active one.

Worked example, Hollis Voice (PF7 in [data_room_planted.csv](../reports/20261022.02_research/data_room_planted.csv)):

- The deck says 357 clinics on slide 3.
- 357 is the last value of `accounts_created_cumulative`, a column that never falls.
- `paying_accounts` ends at 212.
- The deck's figure is 145 above the paying count (357 − 212, scripted arithmetic).

**Model reading**

Only a model can read a label like "clinics on Hollis" and say whether it means paying, active or ever signed up.

```text
Task: check whether a count in this startup's deck is a cumulative number shown as a current one.

Documents:
{{docs: monthly_metrics.csv header and any definitions in the README tab of financial_model.xlsx; pitch_deck.pdf slides 3 and 14}}

Script results:
{{script_results: each column's never_falls result, its last value, and which deck claims equal which last values}}

Answer these questions with claims:
1. What exact label does the deck put on each count? Quote it.
2. Does the deck or the README say whether that count is paying, active, or ever created? Quote it, or add a gap "Not in the room: a definition of <label>".
3. Which column in monthly_metrics.csv holds a cumulative count, and which holds an active or paying count? Use the column names and the README. Set confidence to "judged" if you rely on the name alone.

Quote the exact span you relied on for every claim. Do not say the label was chosen to mislead.

Propose the label using these rules, and name the rule and claim ids in "label_reason":
- "flag": a deck count equals the last value of a cumulative column, and an active or paying column differs by more than tolerance.
- "watch": a deck count uses an undefined label ("users", "clinics") and no active or paying column exists to check it.
- "clear": every deck count matches an active or paying column.
- "cannot_check": monthly_metrics.csv is missing.
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "columns"],
  "properties": {
    "framework": {"type": "string", "const": "vanity_metric"},
    "label": {"type": "string", "enum": ["flag", "watch", "clear", "cannot_check"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "columns": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["column", "kind", "claim_id"],
        "properties": {
          "column": {"type": "string"},
          "kind": {"type": "string", "enum": ["cumulative", "active_or_paying", "flow", "money", "unclear"]},
          "claim_id": {"type": "string"}
        }
      }
    }
  }
}
```

**How the readout scores it**

- `flag`: a deck count equals the last value of a cumulative column, and the active or paying column differs by more than `match_tolerance`.
- `watch`: the deck uses an undefined label and the room holds no active or paying count to check it against.
- `clear`: every deck count matches an active or paying column.
- `cannot_check`: the metrics export is missing.

Its claims feed the overview's **traction and revenue** piece ([The readout](#the-readout-saturday), "Piece verdicts").

**What it must not do**

- Call a column cumulative on the `never_falls` test alone.
- Say the label was chosen to mislead.
- Replace the deck's number with the paying count. Both appear, with sources.

### 1.9 Unit economics recompute

**Inputs**

- `03_metrics/monthly_metrics.csv` (`mrr`, `paying_accounts`).
- `03_metrics/customer_mrr_by_month.csv`, for new paying customers per month and logo churn.
- `02_financials/financial_model.xlsx`, tab `P&L`, the sales and marketing rows.
- `02_financials/expense_ledger.csv`, for sales and marketing spend by month.
- The rebuilt gross margin from 1.7 and the rebuilt churn from 1.3.
- `01_overview/pitch_deck.pdf`, slide 5 (unit economics).

**The questions it asks**

1. What is revenue per account, and does it match the plan prices?
2. What does it cost to win one new paying customer (CAC), from spend and new-customer counts in the same period?
3. How many months of gross profit pay back that cost?
4. Does the deck's lifetime value use gross margin, and which margin?
5. Is CAC blended across channels? a16z says blended CAC can hide weak paid channels ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), "Other published flags we will not plant").

a16z lists LTV/CAC and payback among its five items for a first-pass room ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), 1.3).

**Mechanical check**

```
ARPA            = MRR ÷ paying accounts, at the as-of month
CAC             = sales and marketing spend in a period ÷ new paying customers in that period
payback_months  = CAC ÷ (ARPA × gross_margin_rebuilt)
LTV             = ARPA × gross_margin_rebuilt ÷ monthly logo churn rate
```

When 1.7 moves support staff out of S&M and into cost of revenue, take the same cost out of the S&M spend used for CAC. Otherwise it is counted twice.

Worked example, Hollis Voice:

- ARPA = $171,739 ÷ 212 = $810.09 a month (`mrr_true` and `paying_clinics_now` in [data_room_design_numbers.json](../reports/20261022.02_research/data_room_design_numbers.json); scripted arithmetic). The plan prices run $349, $649 and $1,099 a month, and the largest customer pays $36,000, so the average sits above the middle plan ([data_room_design_numbers.py](../reports/20261022.02_research/data_room_design_numbers.py)).
- Gross profit per account per month: $810.09 × 80% = $648.07 on the deck's margin; $810.09 × 58.1% = $470.66 on the rebuilt margin (scripted arithmetic).
- So any payback period on the rebuilt margin is 1.38 times the one on the deck's margin (0.80 ÷ 0.581, scripted arithmetic).
- CAC: the research does not fix Hollis's sales and marketing spend. The generator's P&L will. Until it does, CAC returns "Not in the room".

**Model reading**

Only a model can read how the deck defines CAC, LTV and payback, and which channels a spend line belongs to.

```text
Task: check this startup's unit economics against the room's own numbers.

Documents:
{{docs: pitch_deck.pdf slides 5 and 14; financial_model.xlsx P&L and README tabs by cell; sales and marketing lines from expense_ledger.csv}}

Script results:
{{script_results: ARPA, new paying customers by month, logo churn, the rebuilt gross margin, and CAC, payback and LTV where the inputs exist}}

Answer these questions with claims:
1. What CAC, payback and LTV does the deck state, and how does it define each? Quote the figures and any definitions.
2. Is the deck's CAC blended across channels, or split by channel? Quote what tells you.
3. Does the deck's LTV use gross margin? Which margin figure? Quote it.
4. Which sales and marketing lines are paid acquisition, which are staff, and which are unclear? Quote the line.

Quote the exact span you relied on for every claim. If the deck states no unit economics, add a gap "Not in the room: CAC, payback or LTV in the deck". If the room has no sales and marketing spend, add a gap "Not in the room: sales and marketing spend" and do not estimate it.

Propose the label using these rules, and name the rule and claim ids in "label_reason":
- "flag": a deck figure differs from the script's recompute by more than tolerance.
- "watch": no flag, but the deck's CAC is blended, or its LTV uses no margin or a margin that 1.7 flagged.
- "clear": every deck figure matches the recompute and uses the rebuilt margin.
- "cannot_check": the spend or the customer counts are missing.
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "definitions"],
  "properties": {
    "framework": {"type": "string", "const": "unit_economics"},
    "label": {"type": "string", "enum": ["flag", "watch", "clear", "cannot_check"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "definitions": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["metric", "blended", "margin_used", "claim_id"],
        "properties": {
          "metric": {"type": "string", "enum": ["cac", "payback_months", "ltv"]},
          "blended": {"anyOf": [{"type": "boolean"}, {"type": "null"}]},
          "margin_used": {"type": "string", "enum": ["none", "deck_margin", "rebuilt_margin", "unclear"]},
          "claim_id": {"type": "string"}
        }
      }
    }
  }
}
```

**How the readout scores it**

- `flag`: a deck figure differs from the recompute by more than `match_tolerance`.
- `watch`: no flag, but CAC is blended, or LTV uses no margin or the margin 1.7 flagged.
- `clear`: every deck figure matches and uses the rebuilt margin.
- `cannot_check`: spend or customer counts are missing.

Its claims feed the overview's **unit economics** piece ([The readout](#the-readout-saturday), "Piece verdicts").

**What it must not do**

- Estimate spend, churn or a channel split that the room does not hold.
- Count support cost in both cost of revenue and CAC.
- Call an LTV/CAC ratio good or bad. It reports the ratio and its inputs.

### 1.10 Cap table reconciliation

**Inputs**

- `02_financials/cap_table.xlsx`: fully diluted, with two SAFEs and an option pool.
- The SAFE terms as the room states them ($2,000,000 of SAFEs on a $12,000,000 post-money cap).
- `01_overview/pitch_deck.pdf`, slide 13 (the ask).

CRV puts the cap table first on its first-pass list ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), 1.3). On Hollis Voice it is a clean decoy, DC3. The point of this entry on Saturday is to stay quiet.

**The questions it asks**

1. Do all holders add to 100 percent, fully diluted?
2. Does each SAFE convert at its stated cap, and is each one a row?
3. Is the option pool shown?
4. Does the ask on the deck match the round in the cap table (amount, pre-money, post-money)?
5. Are there instruments or grants in the cap table with no document in the room?

**Mechanical check**

Check name: `cap_table_reconcile`. The answer key uses it for DC3 (the clean cap table), which must not fire it.

```
sum_check          = SUM of fully diluted ownership across holders, must equal 100.00 percent
safe_ownership     = SAFE amount ÷ post-money cap
series_a_ownership = raise ÷ post-money
post_money         = pre-money + raise
```

Worked example, Hollis Voice (DC3, [research_data_room.md](../reports/20261022.02_research/research_data_room.md), 3.4; figures from [data_room_design_numbers.json](../reports/20261022.02_research/data_room_design_numbers.json); scripted arithmetic):

- SAFE ownership: $2,000,000 ÷ $12,000,000 = 16.67% before the Series A.
- Series A ownership: $9,000,000 ÷ $54,000,000 = 16.67%.
- Post-money: $45,000,000 + $9,000,000 = $54,000,000.
- The data-room research states holders add to 100.00 percent and the SAFE conversion is right. The expected label is `clear`.

**Model reading**

Only a model can read the notes on a cap table and match each instrument to a document.

```text
Task: check that this startup's cap table adds up and matches its round.

Documents:
{{docs: cap_table.xlsx by cell, including notes; pitch_deck.pdf slides 13 and 14; the room's file list}}

Script results:
{{script_results: the ownership sum, each SAFE's conversion, the round arithmetic}}

Answer these questions with claims:
1. What does slide 13 state for the raise, the pre-money and the post-money? Quote it.
2. Which holders, SAFEs and option pools does the cap table list? Quote each row's name.
3. For each SAFE or note in the cap table, is its signed document in the room's file list? If not, add a gap "Not in the room: the signed <instrument>".
4. Do the cap table's notes mention any grant, warrant or side letter that has no row? Quote it.

Quote the exact span you relied on for every claim. Do not comment on whether the valuation is fair.

Propose the label using these rules, and name the rule and claim ids in "label_reason":
- "flag": ownership does not sum to 100 percent within tolerance, a SAFE converts at a different figure than its cap gives, or the deck's round differs from the cap table's.
- "watch": the numbers reconcile, but the option pool is missing or an instrument has no document in the room.
- "clear": everything reconciles and the option pool is shown.
- "cannot_check": the cap table is missing.
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "instruments"],
  "properties": {
    "framework": {"type": "string", "const": "cap_table"},
    "label": {"type": "string", "enum": ["flag", "watch", "clear", "cannot_check"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "instruments": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["name", "kind", "document_in_room", "claim_ids"],
        "properties": {
          "name": {"type": "string"},
          "kind": {"type": "string", "enum": ["common", "preferred", "safe", "note", "option_pool", "warrant", "other"]},
          "document_in_room": {"type": "boolean"},
          "claim_ids": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
```

**How the readout scores it**

- `flag`: ownership does not sum to 100 percent within tolerance, a SAFE converts wrong, or the deck's round differs from the cap table's by more than `match_tolerance`.
- `watch`: the numbers reconcile, but the option pool is missing or an instrument has no document in the room.
- `clear`: everything reconciles. On Hollis Voice this is the expected label, and a flag counts as a false positive in the answer-key test.
- `cannot_check`: the cap table is missing.

Its claims feed the overview's **the pitch itself** piece ([The readout](#the-readout-saturday), "Piece verdicts").

**What it must not do**

- Comment on whether the valuation or the dilution is good.
- Flag a clean cap table to look thorough.
- Treat a missing SAFE document as a cap table error. It is a `watch` and an ask.

### 1.11 What the room cannot settle

The regret stories investors tell in public are mostly about documents that were made up. An angel lost money to a founder who kept two sets of books, one made up for investors. A 2026 fraud case put forged bank statements in a data room. A SaaS investor says the bank check usually waits until after the term sheet ([research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md), section 2, rows 14, 50, 51 and 64). Every file in a data room comes from the founder. So no check on those files can rule this out. This entry says so, and says what to ask for.

**Inputs**

- The room's file list ([data_room_files.csv](../reports/20261022.02_research/data_room_files.csv) on Hollis Voice).
- Bank statements, if the room holds them. A Series A room often does; a seed room may not ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), 1.2, row 13).
- The P&L revenue line and the financing events from the model.
- Flagged claims from 1.2 to 1.9, which set what the partner should ask the founder to walk through.

**The questions it asks**

1. Does the room hold bank statements? If so, do monthly deposits tie to revenue plus financing?
2. Does the room hold statements prepared by an outside accountant, or tax returns? Kruze says a professional investor will ask for three years of returns (same file, 1.2, row 29).
3. Does the room hold signed IP assignment agreements for every founder and contractor? CRV puts them on its first-pass list (same file, 1.3).
4. For each flagged number, can the founder walk from the source data to the figure? A pre-seed fund's guide tells angels to ask exactly that ([research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md), row 54), and its partners report founders who could not explain their own metrics (row 23).
5. Has anyone called customers? A SaaS investor says pre-term-sheet diligence often means two or three customer calls (same file, row 12).

**Mechanical check**

```
present(type) = TRUE if the file list holds a file of that type:
                bank statements, accountant-prepared statements, tax returns,
                IP assignment agreements, customer reference list
if bank statements are present, for each month t:
    tie_gap(t) = deposits(t) − ( revenue(t) + financing(t) )
    flag month t if | tie_gap(t) | ÷ revenue(t) > match_tolerance
```

Worked example, Hollis Voice. The 16 files in [data_room_files.csv](../reports/20261022.02_research/data_room_files.csv) hold no bank statements, no accountant-prepared statements, no tax returns, no IP assignments and no reference list. So every `present` test is false. The tie-out does not run. The entry returns one ask per missing item, plus one walk-through ask for each flag from 1.2 to 1.9.

**Model reading**

The model writes the asks. It turns each missing item and each flag into a question a partner can send.

```text
Task: list what the partner must ask for, because no file in this data room can settle it.

Documents:
{{docs: the room's file list; the bank statements if present, by page; the P&L revenue row and financing rows by cell}}

Script results:
{{script_results: the present() result for each item, the monthly tie-out if it ran, and every claim labeled flag or watch by entries 1.2 to 1.9}}

Write these:
1. A gap for each missing item from the list (bank statements, accountant-prepared statements, tax returns, IP assignment agreements, customer references). Its "what" is "Not in the room: <item>". Its "would_need" says what to request and from whom. For bank statements, ask for statements sent directly by the bank or read-only access, not copies from the founder. For accountant-prepared statements, ask for them from the accountant directly. Add a matching entry to "asks". In "asks", set stage to "after_term_sheet" for bank statements, accountant-prepared statements and tax returns, and to "before_second_meeting" for everything else.
2. A claim for each flag or watch from entries 1.2 to 1.9. Text: "Ask the founder to walk from the source data to <the deck figure>." Quote the deck figure from its source. Add a matching "walk_through" entry to "asks" whose basis is the flag's claim id.
3. If the tie-out ran and any month did not tie, one claim per month, quoting the statement line and the P&L cell.

Quote the exact span you relied on whenever you cite a document. Do not suggest fraud or any reason for a gap. Do not mark anything settled because a founder-supplied file looks right.

Propose the label using these rules, and name the rule and claim ids in "label_reason":
- "flag": bank statements are present and at least one month does not tie.
- "ask": anything else. This entry never returns clear.
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "asks"],
  "properties": {
    "framework": {"type": "string", "const": "cannot_settle"},
    "label": {"type": "string", "enum": ["flag", "ask"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "asks": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["item", "ask_for", "ask_whom", "stage", "basis"],
        "properties": {
          "item": {"type": "string", "enum": ["bank_statements", "accountant_statements", "tax_returns", "ip_assignments", "customer_references", "walk_through"]},
          "ask_for": {"type": "string"},
          "ask_whom": {"type": "string", "enum": ["bank", "accountant", "founder", "customers", "counsel"]},
          "stage": {"type": "string", "enum": ["before_second_meeting", "after_term_sheet"]},
          "basis": {"type": "string", "description": "The claim id behind the ask, or the gap's what text."}
        }
      }
    }
  }
}
```

**How the readout scores it**

- `flag`: bank statements are in the room and at least one month's deposits do not tie to revenue plus financing within `match_tolerance`.
- `ask`: every other case. The readout shows the asks as a list the partner can send.
- There is no `clear` label. A founder-supplied file that ties out can still be forged, so this entry never says the risk is ruled out.

Each walk-through claim feeds the piece of the flag it asks about ([The readout](#the-readout-saturday), "Piece verdicts"). Its gaps sit in the overview's gap list, beside the pieces, because no one piece owns a missing bank statement.

**What it must not do**

- Suggest fraud, or any reason a number does not tie.
- Mark the risk settled because the founder's own files agree with each other.
- Present a check that usually waits for a term sheet as a first-pass ask. Bank statements and deep financial review often come after the term sheet (row 14), so every ask names the stage it belongs to.

## Scan 2. The comp builder (Saturday)

The organisers' second direction: "a comp builder that picks comparable companies and recent rounds, and explains why each one is a fair comp" ([problem tracks](../reports/20261022.01_hackathon_sources/problem_tracks.txt), Track 2). The landscape research found that the incumbents that show comps present competitor lists, public multiples or aggregate round benchmarks, and that none of their pages say why a comp is fair ([research_landscape.md](../reports/20261022.02_research/research_landscape.md), Part 1). The reason is the product here.

### The selection rules both comp entries use

Every candidate is scored on five dimensions. Each dimension gets a match label, never a number.

| Dimension | What it means | Match labels |
|---|---|---|
| Sector | What the company sells and to whom: the product type and the customer type | `same`, `adjacent`, `different`, `not_public` |
| Stage | Round stage for a private company. Public companies never match. | `same`, `adjacent`, `different`, `not_public` |
| Business model | How it charges: subscription by seat or location, usage, services, one-time | `same`, `adjacent`, `different`, `not_public` |
| Revenue band | Annual revenue in the same order of size | `same`, `adjacent`, `different`, `not_public` |
| Geography | Where it is based and sells | `same`, `adjacent`, `different`, `not_public` |

`adjacent` means one step away and named: "sells software to small dental practices" is adjacent to "sells software to small vet clinics". The reason sentence must name the step.

### 2.1 Public comps from EDGAR

**Inputs**

- The target's profile: sector, customer, business model, revenue band, geography and stage, taken from 1.1's claims and the product one-pager.
- SEC EDGAR full-text search: the web page is official; the JSON endpoint `efts.sec.gov/LATEST/search-index` answered the feasibility research's tests but no SEC page documents it ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), Part 2). Its hits carry `display_names`, `form`, `sics`, `biz_states`, `file_date` and `period_ending` ([sample](../reports/20261022.02_research/raw/feasibility/efts_sample.json)).
- EDGAR XBRL frames and company facts, for revenue and gross profit. A frames sample for revenue in calendar 2023 returned 2,679 data points (feasibility research, Part 0).
- The Item 1 (Business) text of each candidate's latest 10-K.
- A pre-pulled set of 8 to 12 public companies near the target's space, saved as JSON this week (feasibility research, 1.2).
- Access rules: a declared User-Agent with contact details, 10 requests a second, no CORS, so calls go from the server (feasibility research, Part 2).

**The questions it asks**

1. Which public companies sell a similar product to a similar customer?
2. For each: which dimensions match, and what is the step on the ones that do not?
3. Which number does each comp inform: gross margin, growth, or a revenue multiple?
4. What is each comp's gross margin and revenue growth, computed from its filings?
5. How far apart in scale are the comp and the target, stated plainly?

**Mechanical check**

```
search:   EDGAR full-text search for the target's product and customer phrases,
          forms = 10-K, within the last two filing years
filter:   keep hits whose SIC code and business state are recorded; drop duplicates by CIK
numbers:  from company facts, per comp and fiscal year y:
          gross_margin(y) = GrossProfit(y) ÷ Revenues(y)
          growth(y)       = Revenues(y) ÷ Revenues(y − 1) − 1
          record which XBRL tag each number came from; tag names vary by filer
scale:    scale_ratio = comp revenue ÷ target's rebuilt recurring ARR
```

A public comp never matches on stage, and almost never on revenue band. Its job is to give context for margin, growth or multiple. A comp is `fair` only if it matches on sector and business model and the reason names the number it informs.

Worked example, Hollis Voice:

- Profile: an AI phone agent for independent veterinary clinics, sold as a monthly subscription at $349, $649 or $1,099 ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), 3.2; [data_room_design_numbers.py](../reports/20261022.02_research/data_room_design_numbers.py)). Series A. Rebuilt recurring ARR $2,060,868. Based in Brooklyn.
- Search phrases come from the profile: veterinary practice software, phone answering, voice agents for small practices.
- The rebuilt gross margin of 58.1% from 1.7 is the number a public comp most helps a partner read. A comp's margin from its own filings sits beside it, with the comp's scale ratio.
- The feasibility research found that EDGAR cannot describe a private company, and that a synthetic company has no true public comps. The fallback is the pre-pulled set, chosen by hand this week (feasibility research, 1.2).

**Model reading**

Only a model can read a 10-K's business description and say whether its product and customer match the target's.

```text
Task: decide whether each public company below is a fair comparison for the target startup, and say why in words a partner can check.

Target profile:
{{docs: the target's claims for sector, customer, business model, revenue band, geography and stage, each with its source}}

Candidates:
{{docs: for each candidate, the Item 1 Business text of its latest 10-K by section, its SIC code and business state from the filing index, and the script's gross margin, growth and scale ratio}}

For each candidate:
1. For each of the five dimensions (sector, stage, business_model, revenue_band, geography), set the match to "same", "adjacent", "different" or "not_public". Quote the sentence from the 10-K that shows the candidate's side. For "adjacent", say the one step in the claim text.
2. Stage is always "different" for a public company. Revenue band is "different" unless the script's scale ratio says otherwise.
3. Set "informs" to the number this comp helps a partner read: "gross_margin", "growth", "revenue_multiple", or "none".
4. Write "why_fair" as one or two plain sentences built only from the quotes above. Name the dimensions that match and the number it informs.
5. Propose the comp's label: "fair" if sector and business model are both "same" or "adjacent" and informs is not "none"; "partial" if only one of them is; "rejected" otherwise. Keep rejected comps in the list with the reason.

Quote the exact span you relied on for every claim. If a candidate's 10-K text is missing, add a gap "Not in the room: the business description for <company>" and set its label to "rejected". Use no knowledge of these companies beyond the documents given. Do not estimate what the target is worth.

Propose the overall label: "comps_found" if at least one comp is fair, "thin" if none is fair but at least one is partial, "none_found" otherwise. Name the rule and comp names in "label_reason".
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "comps"],
  "properties": {
    "framework": {"type": "string", "const": "public_comps"},
    "label": {"type": "string", "enum": ["comps_found", "thin", "none_found"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "comps": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["name", "cik", "filing_url", "sector", "stage", "business_model", "revenue_band", "geography", "informs", "why_fair", "label", "claim_ids"],
        "properties": {
          "name": {"type": "string"},
          "cik": {"type": "string"},
          "filing_url": {"type": "string"},
          "sector": {"type": "string", "enum": ["same", "adjacent", "different", "not_public"]},
          "stage": {"type": "string", "enum": ["same", "adjacent", "different", "not_public"]},
          "business_model": {"type": "string", "enum": ["same", "adjacent", "different", "not_public"]},
          "revenue_band": {"type": "string", "enum": ["same", "adjacent", "different", "not_public"]},
          "geography": {"type": "string", "enum": ["same", "adjacent", "different", "not_public"]},
          "informs": {"type": "string", "enum": ["gross_margin", "growth", "revenue_multiple", "none"]},
          "why_fair": {"type": "string"},
          "label": {"type": "string", "enum": ["fair", "partial", "rejected"]},
          "claim_ids": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
```

**How the readout scores it**

Per comp:

- `fair`: sector and business model are `same` or `adjacent`, the comp informs a named number, and every dimension has a quote.
- `partial`: only one of sector or business model matches.
- `rejected`: neither matches, or the business description is missing. Rejected comps stay in a folded list so the partner sees what was considered.

Overall: `comps_found` with at least one fair comp; `thin` with partial comps only; `none_found` otherwise.

Its claims feed the overview's **comps** piece ([The readout](#the-readout-saturday), "Piece verdicts").

**What it must not do**

- Pick comps from the model's memory. Every candidate comes from a filing the script fetched.
- Turn comps into a price or a valuation for the target. The partner does that.
- Hide the scale gap. The ratio sits beside every public comp.

### 2.2 Recent private rounds

**Inputs**

- SEC Form D quarterly data sets, the last four quarters, downloaded to the laptops this week (feasibility research, 1.2). The tables used: `FORMDSUBMISSION.tsv` (filing date), `ISSUERS.tsv` (entity name, state, year of incorporation), `OFFERING.tsv` (industry group, total offering amount, amount sold, equity type, sale date) ([formd_counts.py](../reports/20261022.02_research/raw/feasibility/formd/formd_counts.py); [research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), 1.2).
- For what each company does: Tavily or You.com search and page extraction, or Akta Company Data on the pay-as-you-go plan (100 calls a month) ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), Part 2).
- Crunchbase as a research aid only. Its REST API is sold through sales, and its MCP docs say apps built on it need a separate arrangement ([research_landscape.md](../reports/20261022.02_research/research_landscape.md), Part 2).
- Carta's round benchmarks by stage, sector and geography, checked by hand. No API (same file, Part 2).

**The questions it asks**

1. Which companies raised a round of similar size, recently, in a technology industry group?
2. Which of those sell a similar product to a similar customer? Form D cannot say; another source must.
3. For each: round size, date, state, and the five dimension matches.
4. Is the target's ask in line with these rounds? The scan states the rounds; the partner judges.

**Mechanical check**

```
keep offerings where:
    ISEQUITYTYPE = true
    INDUSTRYGROUPTYPE is a technology group ("Other Technology", "Computers")
    TOTALOFFERINGAMOUNT is inside a band the partner sets around the target's ask
    FILING_DATE is inside the last four quarters
rank:    same state as the target first, then by filing date, newest first
confirm: for each kept issuer, fetch one page that says what the company does;
         an issuer with no such page stays "not_public" on sector
```

The feasibility research found two limits. Form D carries no business description. And a full-text search for "voice AI" across Form D filings from 2026-09-01 to 2026-10-22 returned 0 hits, because there is no description to search ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), 1.2). The SEC also says it cannot guarantee the data's accuracy (same file, Part 2). So Form D says a round happened. It never says the company is a fair comp on its own.

Worked example, Hollis Voice. The feasibility research ran this filter on the 2026 Q3 file with a band of $5 million to $20 million around the $9,000,000 ask ([formd_counts_output.txt](../reports/20261022.02_research/raw/feasibility/formd/formd_counts_output.txt)):

- 15,952 offerings in the file.
- 1,114 in the industry group "Other Technology".
- 202 technology-type equity offerings between $5 million and $20 million.

202 is too many to read by eye and few enough to rank by script (feasibility research). The confirm step then searches each name for a page that describes the business. Only issuers with a quoted description can reach `fair`.

**Model reading**

Only a model can read a company's own page and say whether it sells what the target sells, to whom the target sells.

```text
Task: decide whether each recent private round below is a fair comparison for the target startup's round, and say why.

Target profile:
{{docs: the target's claims for sector, customer, business model, revenue band, geography, stage and the ask, each with its source}}

Rounds:
{{docs: for each kept Form D offering, its row fields (entity name, state, year of incorporation, industry group, total offering amount, amount sold, filing date, accession number), and the saved page that describes the company, with URL and date read}}

For each round:
1. Set the five dimension matches ("same", "adjacent", "different", "not_public"). Sector and business model come only from the saved page; quote it. If there is no saved page, both are "not_public". Stage comes from the offering size against the target's ask and any stage the page states. Revenue band is "not_public" unless the page states revenue. Geography comes from the Form D state.
2. Write "why_fair" in one or two plain sentences built only from the quotes and Form D fields. Name what matches and what does not.
3. Propose the round's label: "fair" if sector and business model are "same" or "adjacent" and the round size is inside the band; "partial" if one of sector or business model is "not_public" or "different"; "rejected" if both are.

Quote the exact span you relied on for every claim. A Form D field is quoted as "FIELD_NAME: value". Never infer what a company does from its name. If the page for a company is missing, add a gap "Not in the room: a description of <entity name>".

Propose the overall label: "rounds_found" if at least one round is fair, "thin" if only partial rounds exist, "none_found" otherwise. Name the rule and entities in "label_reason".
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "rounds"],
  "properties": {
    "framework": {"type": "string", "const": "private_rounds"},
    "label": {"type": "string", "enum": ["rounds_found", "thin", "none_found"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "rounds": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["entity_name", "accession_number", "state", "total_offering_amount", "amount_sold", "filing_date", "description_url", "sector", "stage", "business_model", "revenue_band", "geography", "why_fair", "label", "claim_ids"],
        "properties": {
          "entity_name": {"type": "string"},
          "accession_number": {"type": "string"},
          "state": {"type": "string"},
          "total_offering_amount": {"anyOf": [{"type": "number"}, {"type": "null"}]},
          "amount_sold": {"anyOf": [{"type": "number"}, {"type": "null"}]},
          "filing_date": {"type": "string"},
          "description_url": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "sector": {"type": "string", "enum": ["same", "adjacent", "different", "not_public"]},
          "stage": {"type": "string", "enum": ["same", "adjacent", "different", "not_public"]},
          "business_model": {"type": "string", "enum": ["same", "adjacent", "different", "not_public"]},
          "revenue_band": {"type": "string", "enum": ["same", "adjacent", "different", "not_public"]},
          "geography": {"type": "string", "enum": ["same", "adjacent", "different", "not_public"]},
          "why_fair": {"type": "string"},
          "label": {"type": "string", "enum": ["fair", "partial", "rejected"]},
          "claim_ids": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
```

**How the readout scores it**

Per round: `fair` when sector and business model match on a quoted page and the size is in the band; `partial` when one of the two is unknown or different; `rejected` when both are. Overall: `rounds_found`, `thin` or `none_found`, as in 2.1.

Its claims feed the overview's **comps** piece ([The readout](#the-readout-saturday), "Piece verdicts").

**What it must not do**

- Infer what a company does from its name or its industry group.
- Read the total offering amount as a valuation, or the amount sold as a closed round. Both are reported as filed.
- Use Crunchbase data in the shipped readout until its terms allow it.

## Scan 3. Market signals (Saturday)

The organisers' third direction: "a market signal tracker for a company and its competitors: hiring, web traffic, reviews, pricing changes, customer wins" ([problem tracks](../reports/20261022.01_hackathon_sources/problem_tracks.txt), Track 2). An associate quoted in the voice-of-customer research opens about ten browser tabs on traffic, reviews and the online story before opening a data room ([research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md), row 1). This scan is those tabs.

Hollis Voice is synthetic, so it has no outside signals. The scan runs on 3 to 5 real competitors chosen and pre-pulled this week (feasibility research, 1.3). For the target, the only signals are the ones the room holds: its hiring plan, its website copy and its pricing tiers.

Which source carries which signal:

| Signal | First source | Plan needed | Fallback |
|---|---|---|---|
| Hiring | Akta Job Posts and Headcount Trends | Subscription; pay-as-you-go returns 403 | Tavily or You.com extract of the careers page |
| Web traffic | Akta Website Traffic | Subscription | None. The signal is reported as missing. |
| Reviews | Akta Product Reviews and Employee Reviews | Subscription | Apple Search and Lookup for app ratings |
| Pricing changes | Tavily or You.com extract of the pricing page | Free tiers | None needed |
| Customer wins | Akta News Signals | Pay-as-you-go (10,000 a month) | You.com or Tavily news search |

Plan facts from [research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), 1.3 and Part 2. Akta's slowest calls are long at the tail (p99 for Job Posts is 70,005 ms), so the demo reads saved files (same section). Pulling one company's profile, one news call and the five alternative signals costs 19.3 credits, about $0.77 on the Subscription plan; a target plus four competitors is 96.5 credits, about $3.86 ([research_landscape.md](../reports/20261022.02_research/research_landscape.md), Part 2, from its price script).

### 3.1 Hiring, web traffic and reviews

**Inputs**

- Akta REST with the `x-api-key` header: Job Posts, Headcount Trends, Website Traffic, Product Reviews, Employee Reviews. Each needs the Subscription plan (feasibility research, 1.3).
- Fallbacks: careers pages through Tavily or You.com extraction; app ratings through Apple's Lookup API (`averageUserRating`, `userRatingCount`, `currentVersionReleaseDate`, per [the feasibility research's saved sample](../reports/20261022.02_research/raw/feasibility/appstores/itunes_apple_com_lookup_id_284882215_country_us.txt)).
- For the target: `05_team/hiring_plan.csv` and `06_product/website_copy.md`.
- The deck's competition slide (slide 9), for the competitor names the founder chose.

**The questions it asks**

1. How many open roles does each company list, and in which functions?
2. Is headcount growing, flat or shrinking?
3. Is web traffic growing, flat or shrinking?
4. What rating do product reviews give, how many are there, and what do recent reviews complain about?
5. What do employee reviews say about the company, in their own words?
6. Do the competitors' signals tell a different story from slide 9?

**Mechanical check**

```
for each company, signal and pair of dated readings (t1 earlier than t2):
    change     = value(t2) − value(t1)
    change_rel = value(t2) ÷ value(t1) − 1
    label rising, flat or falling using a flat band the team sets
for hiring: open roles grouped by function, as counts
for reviews: average rating and review count at each date; new reviews between t1 and t2
```

A change needs two dated readings. The first reading is taken this week when the files are pre-pulled. A single reading gets the label `one_reading`, never `flat`. A 403 from Akta is recorded as `no_signal` with the reason "plan does not include it", never as zero.

Worked example, Hollis Voice: the target has no outside footprint by design (feasibility research, 1.6). The scan reports the room's own hiring plan as the company-side signal: 24 planned hires on top of 17 staff today, to 41 (`headcount_now` and `headcount_after_hiring_plan` in [data_room_design_numbers.json](../reports/20261022.02_research/data_room_design_numbers.json)). Every outside signal for Hollis returns `no_signal` with "Not in the room: no public footprint for a synthetic company". The competitor rows carry the real readings from the pre-pulled files. The research gives no competitor figures yet, so this example has none.

**Model reading**

Only a model can sort job titles into functions and pull the complaint behind a review.

```text
Task: summarize hiring, traffic and review signals for one company, from the data pulled for it.

Company: {{company_name}} ({{target or competitor}})

Documents:
{{docs: each Akta response or fallback page, with the endpoint or URL and the date pulled; job post titles and descriptions; review texts with dates and ratings}}

Script results:
{{script_results: each signal's readings, change, change_rel and proposed label; any 403 or empty response}}

Answer these questions with claims:
1. For each open role, which function is it in: engineering, sales, marketing, customer support, operations, leadership or other? Quote the job title.
2. Which themes recur in product reviews posted since the earlier reading (for example call quality, price, setup, support)? For each theme, quote at least one review sentence and give the review's date and rating.
3. Which themes recur in employee reviews? Quote at least one sentence for each.
4. Does any signal contradict what the target's deck says about this company on slide 9? Quote both.

Quote the exact span you relied on for every claim. When the script shows a 403 or an empty response for a signal, add a gap "Not in the room: <signal> for <company> (<reason>)". Do not estimate a missing number. Do not compare readings taken on different dates without naming both dates.

Fill "signals" with one entry per signal. Propose each signal's label: "rising", "flat" or "falling" from the script's change and flat band; "one_reading" if there is only one dated reading; "no_signal" if there is none. Propose the overall label "signals_found" if any signal has two readings, "one_reading_only", or "no_signal". Name the rule in "label_reason".
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "signals"],
  "properties": {
    "framework": {"type": "string", "const": "signals_hiring_traffic_reviews"},
    "label": {"type": "string", "enum": ["signals_found", "one_reading_only", "no_signal"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "signals": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["company", "company_role", "signal", "source", "earlier_claim_id", "later_claim_id", "label", "theme_claim_ids"],
        "properties": {
          "company": {"type": "string"},
          "company_role": {"type": "string", "enum": ["target", "competitor"]},
          "signal": {"type": "string", "enum": ["hiring", "headcount", "web_traffic", "product_reviews", "employee_reviews"]},
          "source": {"type": "string", "enum": ["akta", "tavily", "you_com", "apple", "data_room"]},
          "earlier_claim_id": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "later_claim_id": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "label": {"type": "string", "enum": ["rising", "flat", "falling", "one_reading", "no_signal"]},
          "theme_claim_ids": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
```

**How the readout scores it**

- `rising`, `flat`, `falling`: two dated readings, with the change beside the label so a partner can judge the size. The flat band is a setting the team picks; the raw change always shows.
- `one_reading`: one dated reading. No direction is claimed.
- `no_signal`: no source answered, with the reason (plan, empty response, synthetic company).

Its claims feed the overview's **market** piece ([The readout](#the-readout-saturday), "Piece verdicts").

**What it must not do**

- Estimate traffic, headcount or a rating that no source returned.
- Read a 403 or an empty response as zero.
- Treat a handful of reviews as the market's view. Each theme shows how many reviews it rests on.

### 3.2 Pricing changes and customer wins

**Inputs**

- Pricing pages of the target and each competitor, extracted with Tavily or You.com and saved with the date read. The first snapshot is taken this week.
- Akta News Signals for each competitor (pay-as-you-go, 10,000 a month), plus You.com or Tavily news search ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), Part 2).
- For the target: `06_product/product_one_pager.pdf` (pricing tiers) and `06_product/website_copy.md` (home page and pricing copy).

**The questions it asks**

1. What plans, prices and billing periods does each company publish?
2. What changed between two snapshots: a price, a plan added or removed, a free tier, a move to "contact sales"?
3. Which customer wins has each company announced, with the customer's name and the date?
4. Is a "win" really a customer, or a partnership, a pilot or a funding round?
5. Does the target's published pricing match the plans in its own room?

**Mechanical check**

```
pricing: for each plan in each snapshot, record (plan name, price, billing period)
         price_change(plan) = price(t2) − price(t1)
         plans_added   = plans in t2 not in t1
         plans_removed = plans in t1 not in t2
wins:    count news items labeled customer_win per company in the window,
         keeping one item per customer name and date
```

Worked example, Hollis Voice. The room's plans are Starter $349, Standard $649 and Pro $1,099 a month ([data_room_design_numbers.py](../reports/20261022.02_research/data_room_design_numbers.py)). A year on each is $4,188, $7,788 and $13,188 (12 times each price, scripted arithmetic). The script checks that `website_copy.md` and `product_one_pager.pdf` state the same three prices. With one snapshot, the pricing label is `one_snapshot`. Customer wins for Hollis are `not_checked`: a synthetic company has no news. The research holds no competitor pricing or news yet.

**Model reading**

Only a model can turn a pricing page into a plan table and tell a customer win from a partnership.

```text
Task: read pricing pages and news items for one company, and return its published plans and its announced customer wins.

Company: {{company_name}} ({{target or competitor}})

Documents:
{{docs: each pricing page snapshot with URL and date read; each news item with URL, outlet and date; for the target, product_one_pager.pdf and website_copy.md}}

Script results:
{{script_results: plan tables from earlier snapshots, if any; the news items' ids}}

Answer these questions with claims:
1. For each snapshot, list every plan with its name, price and billing period. Quote the line on the page for each. If a plan says "contact sales" or shows no price, set value to null and quote that text.
2. For each news item, what kind of event is it: customer_win, partnership, pilot, funding, launch, hire or other? Quote the sentence that shows it. For a customer_win, name the customer as the item names it.
3. For the target only: do the prices on the website match the prices in the product one-pager? Quote both.

Quote the exact span you relied on for every claim. If a company has no pricing page, add a gap "Not in the room: a public pricing page for <company>". Do not infer a price from "contact sales". Do not count a pilot or partnership as a customer win. Mark a company's own press release as the company's own claim in the text.

Fill "plans" and "events". Propose the pricing label "changed", "unchanged", "one_snapshot" or "no_page", and the wins label "wins_found", "none_found" or "not_checked", using the rules in "How the readout scores it". Put both rules in "label_reason".
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "wins_label", "label_reason", "claims", "gaps", "plans", "events"],
  "properties": {
    "framework": {"type": "string", "const": "signals_pricing_wins"},
    "label": {"type": "string", "enum": ["changed", "unchanged", "one_snapshot", "no_page"]},
    "wins_label": {"type": "string", "enum": ["wins_found", "none_found", "not_checked"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "plans": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["company", "snapshot_date", "plan_name", "price", "billing_period", "claim_id"],
        "properties": {
          "company": {"type": "string"},
          "snapshot_date": {"type": "string"},
          "plan_name": {"type": "string"},
          "price": {"anyOf": [{"type": "number"}, {"type": "null"}]},
          "billing_period": {"type": "string", "enum": ["month", "year", "one_time", "usage", "unstated"]},
          "claim_id": {"type": "string"}
        }
      }
    },
    "events": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["company", "kind", "counterparty", "date", "company_own_claim", "claim_id"],
        "properties": {
          "company": {"type": "string"},
          "kind": {"type": "string", "enum": ["customer_win", "partnership", "pilot", "funding", "launch", "hire", "other"]},
          "counterparty": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "date": {"type": "string"},
          "company_own_claim": {"type": "boolean"},
          "claim_id": {"type": "string"}
        }
      }
    }
  }
}
```

**How the readout scores it**

Pricing:

- `changed`: two snapshots and any price, plan or free tier differs.
- `unchanged`: two snapshots and nothing differs.
- `one_snapshot`: one snapshot only.
- `no_page`: no public pricing page.

Customer wins:

- `wins_found`: at least one item is a customer win with a named customer and a date.
- `none_found`: news was searched and no item is a customer win.
- `not_checked`: no news source was run, as for a synthetic company.

Its claims feed the overview's **market** piece ([The readout](#the-readout-saturday), "Piece verdicts").

**What it must not do**

- Guess a price behind "contact sales".
- Count a pilot, partnership or funding round as a customer win.
- Present a company's own press release as independent news. The `company_own_claim` field marks it.

## Scan 4. The pitch video (Saturday)

The video scan hears the founder state the numbers in their own voice and sets them against the deck and the model. A founder video is an optional item in a data room at every stage ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), 1.2, row 4). On Hollis Voice it carries one planted entry, PF2b.

Until Ken records the video, `01_overview/pitch_video_script.md` stands in for the transcript (data-room research, 3.7). Its beats, from [research_data_room.md](../reports/20261022.02_research/research_data_room.md), 3.6:

| At | Beat |
|---|---|
| 0:00 | Who we are and the problem: clinics miss calls |
| 0:20 | What the product does |
| 0:35 | Traction, including the planted sentence "we're at about three million dollars in annual recurring revenue" |
| 0:50 | Clinics, retention and the largest customer, all matching the deck |
| 1:10 | Why we win |
| 1:30 | Team |
| 1:45 | The ask and how long the money lasts |
| 1:55 | Close |

### 4.1 Claim extraction with timestamps

**Inputs**

- The pitch video file.
- Its audio as 16 kHz mono 16-bit WAV, made with ffmpeg. whisper.cpp reads only 16-bit WAV ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), 1.5).
- The whisper.cpp transcript, as segments with start and end seconds. Local whisper.cpp gives timestamps and needs no key. The OpenAI `whisper-1` model also gives them, but it is deprecated and shuts down 2027-02-26, so it is the fallback (same section).
- A saved transcript from this week's rehearsal, for when the live run fails (same section).
- Before the recording exists: `pitch_video_script.md`, cited by line instead of by second.

**The questions it asks**

1. Which sentences state a number, and what metric is each number?
2. When in the video does each claim start and end?
3. Is the number hedged ("about", "nearly", "over")?
4. Which claims carry no number at all (why we win, the team), so the room cannot check them?
5. Which period does the founder mean ("this year", "today", "run rate")?

**Mechanical check**

```
ffmpeg -i pitch.mp4 -ar 16000 -ac 1 -c:a pcm_s16le pitch.wav
whisper-cli -m <model file> -f pitch.wav --output-json
```

Then, for each claim the model returns:

- Copy `start_s` from the first cited segment and `end_s` from the last. The model never writes times.
- Check that the quote appears in the text of the cited segments. If not, the claim is `unverified`.
- Parse spoken numbers to values ("three million dollars" is 3,000,000). Keep the hedge word beside the value.

Worked example, Hollis Voice. The planted sentence at about 0:35 is "we're at about three million dollars in annual recurring revenue" (data-room research, 3.6). The claim's value has label `arr` and number 3,000,000, with the hedge "about" and the segment's seconds in its source. The deck states $2,500,000 for the same metric (PF2b in [data_room_planted.csv](../reports/20261022.02_research/data_room_planted.csv)). Entry 4.3 compares them.

**Model reading**

Only a model can tell which spoken sentences are claims, what metric a phrase like "annual recurring revenue" maps to, and what period the speaker means.

```text
Task: pull every factual claim out of this pitch video transcript, tied to the segments where it is said.

Transcript:
{{docs: whisper segments, each as [seg id | start-end seconds] text}}

For every claim:
1. Write it as one plain sentence in "text".
2. Set value.label to the closest key from the schema's list, or "other" if none fits. A claim with no number has value null.
3. Set value.number to the number as spoken, converted to a plain number ("three million dollars" is 3000000). Do not round or correct it.
4. In "spoken", list the segment ids the claim spans, and the hedge word if the speaker used one ("about", "nearly", "over", "almost"), or null.
5. Set value.period if the speaker names one ("this year", "last month", "today"); otherwise null.
6. In "sources", set kind to "video", put the segment ids in the locator as "seg 7-8", and leave start_s and end_s null. The script fills the seconds. Quote the exact words spoken.

Quote the exact span you relied on for every claim, word for word from the transcript. Do not write start or end times yourself. If the transcript is missing or empty, return no claims and one gap: "Not in the room: a transcript of the pitch video". Do not fix the founder's numbers, and do not add words the transcript does not hold.

Propose the label "extracted" if at least one claim was found and every quote comes from the transcript, "partial" if some segments were unreadable, or "cannot_check" if there is no transcript. Name the rule in "label_reason".
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "spoken"],
  "properties": {
    "framework": {"type": "string", "const": "video_claims"},
    "label": {"type": "string", "enum": ["extracted", "partial", "cannot_check"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "spoken": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["claim_id", "segment_ids", "hedge", "start_s", "end_s"],
        "properties": {
          "claim_id": {"type": "string"},
          "segment_ids": {"type": "array", "items": {"type": "integer"}},
          "hedge": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "start_s": {"anyOf": [{"type": "number"}, {"type": "null"}], "description": "Set to null by the model; the script fills it from the segments."},
          "end_s": {"anyOf": [{"type": "number"}, {"type": "null"}], "description": "Set to null by the model; the script fills it from the segments."}
        }
      }
    }
  }
}
```

**How the readout scores it**

This entry feeds 4.2 and 4.3. Its label tells the readout whether the video side is complete.

- `extracted`: claims found and every quote matched the transcript.
- `partial`: some segments were unreadable or some quotes did not match.
- `cannot_check`: no video, no transcript and no script file.

Its claims feed the overview piece their `value.label` names ([The readout](#the-readout-saturday), "Piece verdicts"); a claim with no value, or the label `other`, feeds **the pitch itself**.

**What it must not do**

- Write a timestamp. Times come from the segments.
- Correct, round or tidy what the founder said.
- Add words the transcript does not hold, even when the audio was unclear.

### 4.2 Interesting moments

**Inputs**

- The claims from 4.1, with their seconds.
- The comparison results from 4.3 and the labels from 1.2 to 1.9.
- Keyframes at scene changes, from ffmpeg's `select` filter with a scene threshold. The feasibility research tested `select='gt(scene,0.4)'` on a clip with one hard cut and it found the cut ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), Part 0 and 1.5).

**The questions it asks**

1. Where does the founder say a number the room disputes?
2. Where does the founder repeat a deck number that a red-flag check has flagged?
3. Where does the founder make a claim the room holds no file to check?
4. Where are the ask, the use of funds and the runway?
5. Which frame should each moment show as its thumbnail?

**Mechanical check**

```
ffmpeg -i pitch.mp4 -vf "select='gt(scene,0.4)'" -fps_mode vfr frames/%03d.jpg
```

Each claim gets one tier, by the first rule it meets:

| Tier | Rule |
|---|---|
| 1 `disagrees` | Its spoken value differs from the deck or the model beyond `spoken_tolerance` (from 4.3). |
| 2 `repeats_flagged` | Its spoken value matches the deck, and the deck figure is labeled `flag` by an entry in Scan 1. |
| 3 `unbacked` | It states something the room holds no file to check. |
| 4 `the_ask` | It is about the raise, the use of funds or the runway, and none of the rules above fit. |
| 5 `context` | Everything else. |

Moments are ordered by tier, then by time. A moment's thumbnail is the last scene-change frame at or before its start; if none exists, the frame at its start. The page jumps to a moment with a media fragment such as `pitch.mp4#t=35` (feasibility research, 1.5).

Worked example, Hollis Voice, using the beats in the data-room research's script:

- 0:35, ARR "about three million dollars": tier 1. It is 20.0% above the deck's $2,500,000 and 33.9% above the model's $2,240,868 (3,000,000 ÷ 2,500,000 − 1 and 3,000,000 ÷ 2,240,868 − 1, scripted arithmetic on PF2b and PF1).
- 0:50, clinics, retention and the largest customer, matching the deck: tier 2, because 1.8, 1.3 and 1.6 flag those deck figures (PF7, PF3, PF5).
- 1:10, why we win: tier 3, if it holds no number the room can check.
- 1:45, the ask and how long the money lasts: tier 2 if it states the deck's runway, which 1.4 flags (PF4). Otherwise tier 4.

**Model reading**

Only a model can decide whether a claim with no number is checkable against the room, and write a caption a partner can scan.

```text
Task: write a one-line caption for each moment in this pitch video, and sort the claims that have no number.

Documents:
{{docs: the 4.1 claims with their quotes and seconds; the room's file list}}

Script results:
{{script_results: each claim's tier where the script could set it (tiers 1, 2 and 4), and the flags from entries 1.2 to 1.9}}

For each claim the script left without a tier:
1. Decide whether any file in the room could check it. If none could, set its tier to "unbacked"; if one could, set it to "context". Name the file if there is one.

For every moment:
2. Write a caption of at most one sentence that says what the founder claims there, using the quote. Do not describe how the founder speaks, looks or sounds.

Quote the exact span you relied on, from the transcript, for every claim you write. If there are no 4.1 claims, add a gap "Not in the room: claims from the pitch video". Do not rank moments by how impressive they are.

Propose the label "moments_found" if any moment is tier 1 or 2, "no_disputed_moments" if none is, or "cannot_check" if there are no claims. Name the rule in "label_reason".
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "moments"],
  "properties": {
    "framework": {"type": "string", "const": "video_moments"},
    "label": {"type": "string", "enum": ["moments_found", "no_disputed_moments", "cannot_check"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "moments": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["tier", "claim_ids", "caption", "checkable_by", "start_s", "end_s", "thumbnail"],
        "properties": {
          "tier": {"type": "string", "enum": ["disagrees", "repeats_flagged", "unbacked", "the_ask", "context"]},
          "claim_ids": {"type": "array", "items": {"type": "string"}},
          "caption": {"type": "string"},
          "checkable_by": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "start_s": {"anyOf": [{"type": "number"}, {"type": "null"}]},
          "end_s": {"anyOf": [{"type": "number"}, {"type": "null"}]},
          "thumbnail": {"anyOf": [{"type": "string"}, {"type": "null"}]}
        }
      }
    }
  }
}
```

**How the readout scores it**

The tier is the label for each moment. The tiers are an order of what a partner should hear first, not a score. Overall:

- `moments_found`: at least one tier 1 or tier 2 moment.
- `no_disputed_moments`: the video holds no disputed or flagged figure.
- `cannot_check`: no claims from 4.1.

Its claims feed the overview's **the pitch itself** piece ([The readout](#the-readout-saturday), "Piece verdicts").

**What it must not do**

- Judge the founder's delivery, confidence, tone, appearance or accent.
- Rank moments by how impressive they sound.
- Invent a moment between claims to fill the timeline.

### 4.3 Three-way disagreement check

**Inputs**

- The deck's claims from 1.1.
- The model's named cells and export values, and the rebuilt values from 1.2 to 1.9.
- The spoken claims from 4.1.

**The questions it asks**

1. For each metric, what do the deck, the model, the raw-data rebuild and the founder's voice each say?
2. Which pairs disagree beyond tolerance?
3. When the founder repeats the deck, does the room back the deck?
4. Does a spoken label mean the same as the deck's label ("annual recurring revenue" against "ARR")?
5. Does the founder name a different period from the deck?

**Mechanical check**

Check name: `spoken_arr_vs_claims_page`. The answer key uses it for PF2b (video ARR disagrees with the deck).

```
for each metric m:
    D = deck value, M = model value, R = rebuilt value (if any), V = spoken value
    gap(x, y) = | x − y | ÷ | y |
    deck and model pairs use match_tolerance; any pair with V uses spoken_tolerance
    set the pattern label from which pairs agree
```

Worked example, Hollis Voice. ARR, from the table in 3.4 of [research_data_room.md](../reports/20261022.02_research/research_data_room.md); gaps are scripted arithmetic on those figures:

| Pair | Values | Gap |
|---|---|---|
| Video against deck | $3,000,000 against $2,500,000 | 20.0% |
| Video against model | $3,000,000 against $2,240,868 | 33.9% |
| Deck against model | $2,500,000 against $2,240,868 | 11.6% |
| Model against rebuilt | $2,240,868 against $2,060,868 | 8.7% |

Every pair disagrees. The pattern is `all_differ`, and each figure is higher than the one under it. This is PF2b with PF2 and PF1 behind it.

Clinics: the deck says 357, and the founder's 0:50 beat matches the deck (data-room research, 3.6). The rebuilt paying count is 212 (PF7). The pattern is `deck_and_video_agree_room_differs`.

**Model reading**

Only a model can match a spoken phrase to the deck's label and notice when the speaker means a different period.

```text
Task: line up what the deck, the financial model, the raw-data rebuild and the founder's voice each say for the same metric.

Documents:
{{docs: deck claims from 1.1; spoken claims from 4.1 with quotes; the README tab of financial_model.xlsx for definitions}}

Script results:
{{script_results: model cells, rebuilt values from 1.2 to 1.9, and every pairwise gap the script could compute}}

For each spoken claim with a number:
1. Which deck claim states the same metric? Quote both. If the spoken label differs from the deck's ("annual recurring revenue" and "ARR"), say whether they mean the same thing, and set confidence to "judged" if neither defines it.
2. Does the speaker name a different period from the deck? Quote both.
3. If no deck or model figure exists for what the founder said, add a gap "Not in the room: a written figure for <metric> to check the spoken claim".

Quote the exact span you relied on for every claim. Do not say which figure is true. Do not explain why the founder said a different number.

Fill "rows" with one entry per metric, linking the claim ids for deck, model, rebuilt and spoken values. Propose each row's pattern using the rules in "How the readout scores it", and the overall label: "disagreements_found" if any row is not "all_agree" or "not_spoken", else "all_agree". Name the rule in "label_reason".
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "rows"],
  "properties": {
    "framework": {"type": "string", "const": "three_way"},
    "label": {"type": "string", "enum": ["disagreements_found", "all_agree", "cannot_check"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "rows": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["metric", "deck_claim_id", "model_claim_id", "rebuilt_claim_id", "spoken_claim_id", "pattern"],
        "properties": {
          "metric": {"type": "string"},
          "deck_claim_id": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "model_claim_id": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "rebuilt_claim_id": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "spoken_claim_id": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "pattern": {"type": "string", "enum": ["all_agree", "video_differs", "deck_differs_from_model", "deck_and_video_agree_room_differs", "all_differ", "not_spoken"]}
        }
      }
    }
  }
}
```

**How the readout scores it**

Per metric row, the first rule that fits:

- `all_agree`: every pair is within its tolerance.
- `all_differ`: every pair that exists is outside its tolerance.
- `deck_and_video_agree_room_differs`: the spoken and deck values agree, and the model or the rebuild differs.
- `video_differs`: the deck and the model agree, and the spoken value differs.
- `deck_differs_from_model`: the spoken value agrees with one of them, and the deck and the model differ.
- `not_spoken`: the founder does not state this metric.

Overall: `disagreements_found` if any row has a pattern other than `all_agree` or `not_spoken`; `all_agree` otherwise; `cannot_check` if there is no transcript. Rows with disagreements are reasons the piece their metric belongs to reads weak, and they sit in that piece's drill-down ([The readout](#the-readout-saturday), "Piece verdicts").

Its claims feed the overview piece their `value.label` names ([The readout](#the-readout-saturday), "Piece verdicts"); a claim with no value, or the label `other`, feeds **traction and revenue**.

**What it must not do**

- Call one figure true. The rebuilt figure is labeled "rebuilt from raw data", and the readout shows all of them.
- Explain why the founder said a different number.
- Excuse a gap because the founder said "about". The hedge shows beside the value; `spoken_tolerance` decides.

## The readout (Saturday)

The memo turns every scan's claims into the readout. Its first screen is the best green flags and the worst red flags. Under them is the overview: the company in nine pieces, each with a verdict and a reason in one line. One click opens a piece's claims; one more opens a claim's sources, with every source that corroborates or contradicts it ([writers' brief, 12:55 PM and 1:09 PM blocks](../features/20261022.01_hackathon_plan/00_brief_for_writers.md)). Two entries set it up, both pure scripts: "Piece verdicts" groups the claims and marks each piece, and "Top green and red flags" picks the headline list from those marks and the flags.

### Piece verdicts

**Inputs**

- Every claim from every Saturday scan, after the quote checker. `unverified` claims are left out.
- Every gap from every scan.
- The `conflicts_with` and `corroborated_by` links the memo writes (below).
- The room's as-of month, from the deck's cover ("Data as of 2026-09-30" on Hollis Voice, slide 1).
- The settings `match_tolerance` and `spoken_tolerance`.

**The questions it asks**

1. Which piece of the company does each claim belong to?
2. Which numbers do two independent sources agree on, and which do they contradict?
3. For each piece: is it looking strong, looking weak, mixed, or is there not enough in the room?
4. Which claim gives each piece its one-line reason?
5. How many sources corroborate and contradict each piece?

**Mechanical check**

Check name: `piece_verdicts`.

Step 1, assign each claim to one piece. A claim from Scan 2 goes to comps. A claim from Scan 3 goes to market. Any other claim goes to the piece its `value.label` names in this table. A claim with no value, or with the label `other`, goes to the piece its entry names under "How the readout scores it". A gap goes to its entry's piece.

| Piece | `value.label` keys |
|---|---|
| traction and revenue | `arr`, `mrr`, `paying_accounts`, `accounts_created` |
| retention | `nrr_12m`, `grr_12m`, `cohort_size` |
| burn and runway | `cash`, `net_burn_monthly`, `runway_months`, `payroll_monthly`, `hires` |
| unit economics | `gross_margin`, `cost_of_revenue`, `arpa`, `acv`, `cac`, `payback_months`, `ltv`, `price` |
| customers | `largest_customer_share`, `top3_customer_share`, `contract_term`, `notice_period` |
| market | `tam`, `sam`, `som`, `signal` |
| comps | every claim from Scan 2 |
| team | `headcount` |
| the pitch itself | `raise_amount`, `pre_money`, `post_money`, `ownership`: the ask and the round, and the money raised before it |

Step 2, link the claims. The memo already writes `conflicts_with` ([ARCHITECTURE.md](ARCHITECTURE.md), "How the readout merges them"). It writes `corroborated_by` by the mirror rule:

```
before matching:
    a null period on a claim whose quote says "today", "now", "currently" or "as of"
    is set to the room's as-of month
    the label "other" never links, either way
    for ownership, raise_amount, price, contract_term and notice_period, the entry
    writes the holder, round, plan or contract first in the claim's text, before a
    colon ("Series A: ...", "Standard plan: ..."), and two claims link only when
    that text before the colon is the same
match(a, b)   = same label, same unit, same period, and the same name before the colon where the label needs one
agree(a, b)   = | a − b | ÷ | b | ≤ match_tolerance  (spoken_tolerance when either is spoken)
independent(a, b) = a and b cite different files, and not both from the narrative set:
    the deck, its claims sidecar, the company overview, the pitch video and its script,
    the website copy, the product one-pager and the cover note
    (they repeat one another, so together they count as one source)
corroborated_by(a) = every b with match(a, b), agree(a, b) and independent(a, b)
```

Step 3, mark each claim. A claim is **contradicted** if `conflicts_with` is not empty or its severity is "flag". A claim is **corroborated** if `corroborated_by` is not empty and it is not contradicted. Contradiction wins: two of the company's own files agreeing on a number does not cancel a check that rebuilt it differently.

Step 4, mark each piece. Count C, the corroborated claims, and X, the contradicted claims. F is true when any claim in the piece has severity "flag". The first rule that fits sets the verdict:

```
looking_weak            if F, or (X ≥ 1 and C = 0)
mixed                   if X ≥ 1 and C ≥ 1
looking_strong          if C ≥ 1 and X = 0
not_enough_in_the_room  if C = 0 and X = 0
```

Step 5, write the reason and the counts.

- **Reason.** Weak: the flag in the piece with the largest relative gap (see "Top green and red flags"), or the first contradicted claim if there is no flag. Mixed: the most-corroborated claim and the first contradicted claim. Strong: the corroborated claim with the most independent sources. Not enough in the room: the first gap's `what`, or "Only one source states [label]". The reason is that claim's `text`. Its ids go in `reason_claim_ids`.
- **`corroborating_sources`.** The independent sources behind the piece's corroborated claims, with the narrative set counted as one.
- **`contradicting_sources`.** The distinct files cited by the piece's contradicted claims.

Worked example, Hollis Voice (the generated room in `data_room/hollis_voice/` and `data_room/answer_key.json`). The flags are the answer key's planted entries; the other figures are read from the files named.

| Piece | Verdict | Why, by the rule |
|---|---|---|
| traction and revenue | looking weak | Flags PF1, PF2, PF2b and PF7. ARR is stated four ways: about $3,000,000 spoken, $2,500,000 in the deck, $2,240,868 in the model, $2,060,868 from the subscription rows (`facts`). The deck shows 357 clinics against 212 paying accounts. The model's `ARR_TOTAL` and the 2026-09 `arr` in `monthly_metrics.csv` agree at $2,240,868, and that corroboration still loses to the flag. |
| retention | looking weak | Flag PF3: 102.6% net revenue retention shown, 87.3% rebuilt. |
| burn and runway | looking weak | Flag PF4: 37 months of runway in the model and the deck, 19 with all 24 planned hires. Cash of $1,800,000 rests on the model alone (Assumptions and Cash_Bridge are one file), and no bank statement is in the room (1.11). |
| unit economics | looking weak | Flag PF6: 80% gross margin in the deck and the model, 58.1% rebuilt. One corroboration sits inside the weak piece: the Standard plan's $649 a month on deck slide 7, the one-pager and the website is also the list price in the Brookline Row order form. |
| customers | looking weak | Flag PF5: the deck says no customer is above 9% of ARR; the largest customer is 21.0% of MRR. |
| market | looking strong | The deck's 28,000 clinics and $252,000,000 market on slide 8 agree with the model's Market tab (`MARKET_CLINICS` 28,000; `MARKET_TAM_USD` 252,000,000, which is the clinics times $9,000). Both files call it a company estimate, and no outside source is in the room. One corroborated claim beyond the narrative set, nothing contradicting, no flag. `corroborating_sources` is 2 (the narrative set, the model); `contradicting_sources` is 0. |
| comps | not enough in the room, from the room alone | Comp claims come from this week's cached filings, not from the room. Saturday's cached run sets this verdict by the same rule. |
| team | looking strong | Staff today: 17 on deck slide 10 and in the company overview (one source), and 17 in the model (Assumptions `STAFF_NOW`; P&L "Staff at month end", 2026-09). Staff after the hires: 41 on deck slide 12 and 41 in the last row of `hiring_plan.csv` (`headcount_after_hire`, hire H24). The model states no staff total after the hires, and its P&L shows staff for actual months only, so nothing contradicts. The senior names on deck slide 10 match the bios. `corroborating_sources` is 2 for each number (the narrative set, plus the model for 17 and the hiring plan for 41); `contradicting_sources` is 0. |
| the pitch itself | looking strong | Four corroborated claims and nothing contradicting. "Series A: raise" $9,000,000 on deck slide 13 (the video at 1:45 says nine million too), in the cap table ("New money (USD)") and in the model (Assumptions `SERIES_A_RAISE`). "Series A: pre-money" $45,000,000 on slide 13 and in the cap table ("Pre-money valuation (USD)"). "Series A: ownership" 16.67% on slide 13 and in the cap table (`Cap_Table!B28`, 0.166667, DC3). "SAFEs: raised" $5,500,000 in the company overview, the cap table ("Total SAFEs") and the model (Cash_Bridge, "Total raised before the Series A"). `corroborating_sources` is 3 (the narrative set, the cap table, the model); `contradicting_sources` is 0. |

**Said plainly: three pieces read looking strong: the pitch itself, market and team.** Only market is a business piece. The other five business pieces each hold a planted flag, and one flag makes a piece weak by the rule, even where another claim in it is corroborated. The eight planted entries cover five of the nine pieces by design: traction and revenue, retention, burn and runway, unit economics and customers. Comps comes from outside the room.

The strong readings rest on files that agree, and the company wrote them all. Market is the company's own estimate in two places. The readout says so in the verdict's reason, and 1.11 says why agreement is not proof.

How the generator (`data_room/generate.py`) produces them, with every planted flag unchanged:

- Market: the model has a Market tab with the clinics, the contract value, and their product, matching deck slide 8.
- Team: the model has no staff total after the hires, the hiring plan carries the staff count after each hire, and no planned hire shares a title with someone already on the team.
- Names: every founder and senior name matches across the deck, bios, overview, video script and cap table.
- The answer key's `green_flags` list names each strong piece, its number and the file locations that agree. `check.py` reads every location back and checks it is within 1 percent.

**Model reading**

None. The verdict, the reason and the counts are a script's. The memo's one model pass may shorten a reason line. It must cite the reason's claim ids, or the script's text stands. It never changes a verdict.

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "pieces"],
  "properties": {
    "framework": {"type": "string", "const": "piece_verdicts"},
    "label": {"type": "string", "enum": ["built", "partial"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "pieces": {"type": "array", "items": {"$ref": "#/$defs/Piece"}}
  }
}
```

`claims` and `gaps` stay empty: this entry writes no new claims. `pieces` holds all nine, in the table's order.

**How the readout scores it**

- `built`: every Saturday scan wrote its output, and every piece has a verdict.
- `partial`: at least one scan's output is missing. The pieces it feeds are still marked, from what exists, and the missing scan shows as a gap in each of them.

The overview shows all nine pieces in the table's order, strong and weak alike, each with its verdict, its reason and its two counts.

**What it must not do**

- Let a model choose or change a verdict.
- Give the company an overall score, weight the pieces, or say invest or pass.
- Count a repeat as corroboration. The deck and the overview saying the same number are one source.
- Present looking strong as proof. Founder files that agree can still be a consistent fake (1.11).
- Hide a piece, or sort weak pieces above strong ones.

### Top green and red flags

**Inputs**

- The nine pieces from "Piece verdicts", with their claims and links.
- Every claim with severity "flag".
- The settings `top_green_flags` and `top_red_flags`.

**The questions it asks**

1. Which corroborated positives are the strongest?
2. Which flags are the most serious?

**Mechanical check**

Check name: `top_flags`.

```
green candidates = corroborated claims (see "Piece verdicts", step 3)
                   in a piece whose verdict is looking_strong
green score(c)   = the independent sources behind c, the narrative set counted as one
keep the best-scoring candidate per piece; rank those pieces by score,
ties in the piece table's order

red candidates   = claims with severity "flag"
red gap(c)       = | stated − found | ÷ | found |
                   stated is c's value; found is the value of the claim in
                   c.conflicts_with whose confidence is "computed", or else the one
                   that cites a record (not the narrative set)
keep the largest-gap flag per piece; rank those pieces by gap

show the first top_green_flags greens, then the first top_red_flags reds
```

One per piece, so the headline list spans the company instead of repeating one problem. A green flag comes only from a piece that reads looking strong. If there is none, the list says "No green flag" and is not padded.

Worked example, Hollis Voice. Gaps are scripted arithmetic on the figures in the table under "Hollis Voice, the numbers the examples use" and in `answer_key.json`, by the formula above.

- **Green.** Three pieces read looking strong, so there are three green flags. Each piece's best-scoring claim is listed with its independent sources, the narrative set counted as one. The pieces go in score order, and ties go in the piece table's order, so market comes before team.

| Rank | Piece | Claim | Independent sources |
|---|---|---|---|
| 1 | the pitch itself | "Series A: raise" $9,000,000 | 3: the narrative set (deck slide 13), the cap table, the model |
| 2 | market | $252,000,000 market size, company estimate | 2: the narrative set (deck slide 8), the model's Market tab |
| 3 | team | 17 staff today | 2: the narrative set (deck slide 10), the model (`STAFF_NOW`) |

  The headline for the first reads "the round adds up" ([BRAND.md](BRAND.md), "A green flag and a red flag, at the top"). The 41 staff after hiring ties team's score at 2 (deck slide 12, `hiring_plan.csv`); the claim listed first, staff today, is the one shown.
- **Red**, one flag per weak piece, worst first:

| Rank | Piece | Flag | Stated against found | Gap |
|---|---|---|---|---|
| 1 | burn and runway | PF4 runway | 37 months against 19 | 94.7% |
| 2 | traction and revenue | PF7 clinics | 357 against 212 | 68.4% |
| 3 | customers | PF5 largest customer | under 9% against 21.0% | 57.1% |
| 4 | unit economics | PF6 gross margin | 80% against 58.1% | 37.7% |
| 5 | retention | PF3 net revenue retention | 102.6% against 87.3% | 17.5% |

Inside traction and revenue, PF7's gap is larger than any ARR pair: PF2b is 20.0%, PF2 11.6% and PF1 8.7% (the same pairs as in 4.3). So the headline red flag for that piece is the clinic count. The four ARR figures still lead the piece's drill-down, where the demo goes next.

**Model reading**

None. Each headline line is written from its claim's text in the shapes in [BRAND.md](BRAND.md). The memo's model pass may shorten a line if it cites the claim ids.

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "top_flags"],
  "properties": {
    "framework": {"type": "string", "const": "top_flags"},
    "label": {"type": "string", "enum": ["built", "no_green_flag", "no_red_flag", "neither"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "top_flags": {"type": "array", "items": {"$ref": "#/$defs/TopFlag"}}
  }
}
```

**How the readout scores it**

- `built`: at least one green flag and one red flag.
- `no_green_flag`: no piece reads looking strong. The list says so in one line.
- `no_red_flag`: no claim carries a flag. The list says so in one line.
- `neither`: both lists are empty.

The headline list is the first thing on the page: green flags first, then red. Each line opens its piece.

**What it must not do**

- Take a green flag from a weak, mixed or not-enough piece, or pad the green list.
- Rank by a model's sense of importance. The ranks are the formula's.
- Show two flags from one piece in the headline list.
- Say anything about the company as a whole, or invest or pass.

## After Saturday

The scans below are Ken's additions to Track 2. The feasibility research ranks them below the Saturday four for demo value: business frameworks are cheap to build and easy to copy, founder profiles have one clean source (public GitHub), and a synthetic company has no online footprint ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), Summary). They follow the same rules as everything above. Their worked examples use Hollis Voice where the room holds the input, and say "not in the room" where it does not.

## Scan 5. Business frameworks

Every framework in this scan is a structured reading of what the founder and the room say. None of them is the model's own view of the market. Each box or item is a claim with a quote, and each one is set against the red-flag engine's results, so a box the numbers contradict says so. The feasibility research notes the value is in the quote check: a box that says "customer segment: independent vet clinics" shows the sentence it came from, and an empty box shown as "not in the room" is a good demo moment ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), 1.4).

The box labels are shared across 5.1 to 5.3:

| Label | Rule |
|---|---|
| `stated` | The room states it and the quote was found. No script result touches it. |
| `backed` | The room states it and a script claim from Scans 1 to 3 agrees. |
| `contradicted` | The room states it and a script claim disagrees. The two claims link through `conflicts_with`. |
| `room_only` | No founder document states it, but the room's raw files show it (for example, a vendor in the ledger). |
| `gap` | Nothing in the room fills it. |

### 5.1 Lean canvas

**Inputs**

- `01_overview/pitch_deck.pdf`, `01_overview/company_overview.pdf`, `06_product/product_one_pager.pdf`, `06_product/website_copy.md`.
- The transcript claims from 4.1.
- The claims and labels from Scans 1 to 3, so a box can be backed or contradicted.

**The questions it asks**

The nine boxes of the lean canvas, each as a question:

1. Problem: what problem does the company say its customers have?
2. Customer segments: who exactly are the customers, and who are the early adopters?
3. Unique value proposition: what single message says why this is different?
4. Solution: what does the product do about the problem?
5. Channels: how does the company reach customers?
6. Revenue streams: what does it charge for, and how?
7. Cost structure: what are its main costs?
8. Key metrics: which numbers does it say it runs on?
9. Unfair advantage: what does it have that cannot easily be copied or bought?

**Mechanical check**

```
coverage       = boxes with at least one found quote ÷ 9
revenue check  = every plan and fee in the Revenue streams box appears in the product one-pager
                 and in the product types of ARR_Build
metrics check  = for each metric in the Key metrics box, look up its label from Scan 1
                 flag  → box item is contradicted
                 clear → box item is backed
```

Worked example, Hollis Voice:

- Problem: the video's first beat is that clinics miss calls (data-room research, 3.6).
- Solution: the product answers calls, books appointments and sends refill requests to staff ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), 3.2).
- Revenue streams: three subscription plans at $349, $649 and $1,099 a month, a one-time $500 onboarding fee, and the Marlow pilot at $15,000 a month ([data_room_design_numbers.py](../reports/20261022.02_research/data_room_design_numbers.py)). The pilot item is `contradicted` if the room presents it as recurring, because 1.2 flags it (PF1).
- Key metrics: the deck's ARR, clinics, net retention and gross margin. All four are `contradicted` by 1.5, 1.8, 1.3 and 1.7 (PF2, PF7, PF3, PF6).
- Unfair advantage: the research does not say what the deck claims here. If the room holds nothing, the box is `gap`.

**Model reading**

```text
Task: fill a lean canvas for this startup from its own documents, one box at a time.

Documents:
{{docs: pitch_deck.pdf by slide, company_overview.pdf and product_one_pager.pdf by page, website_copy.md by line, video claims with seconds}}

Script results:
{{script_results: every claim and label from entries 1.2 to 3.2}}

For each of the nine boxes (problem, customer_segments, unique_value_proposition, solution, channels, revenue_streams, cost_structure, key_metrics, unfair_advantage):
1. Write the fewest claims that cover what the documents say for this box. Each claim is one plain sentence with its quote.
2. If a script result agrees with an item, set the item's label to "backed" and name the script claim id. If a script result disagrees, set it to "contradicted" and put the script claim id in conflicts_with.
3. If no document says anything for the box, add a gap "Not in the room: <box name>" and set the box label to "gap".

Quote the exact span you relied on for every claim. Use only these documents. Do not write what vet clinics, or any customer, usually need. Do not improve the founder's wording.

Propose the overall label using the rules in "How the readout scores it", and name the boxes in "label_reason".
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "boxes"],
  "properties": {
    "framework": {"type": "string", "const": "lean_canvas"},
    "label": {"type": "string", "enum": ["complete", "has_gaps", "has_contradictions", "cannot_check"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "boxes": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["box", "label", "claim_ids"],
        "properties": {
          "box": {"type": "string", "enum": ["problem", "customer_segments", "unique_value_proposition", "solution", "channels", "revenue_streams", "cost_structure", "key_metrics", "unfair_advantage"]},
          "label": {"type": "string", "enum": ["stated", "backed", "contradicted", "room_only", "gap"]},
          "claim_ids": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
```

**How the readout scores it**

Each box takes a label from the shared table. Overall, the first rule that fits:

- `has_contradictions`: any box is `contradicted`.
- `has_gaps`: any box is `gap`.
- `complete`: every box is `stated`, `backed` or `room_only`.
- `cannot_check`: the deck and the one-pagers are all missing.

**What it must not do**

- Fill a box from general knowledge of the market.
- Polish or rewrite the founder's claims into better ones.
- Leave a contradicted item looking like a stated one.

### 5.2 Jobs to be done

**Inputs**

- The deck, the one-pagers, the website copy and the video claims.
- Customer-side evidence: the order forms in `04_customers/`, product reviews from 3.1, and Reddit threads from 7.2.

**The questions it asks**

1. When does a customer reach for this product? What situation are they in?
2. What are they trying to get done, in their words?
3. What outcome tells them it worked?
4. What do they use today instead (staff, voicemail, an answering service, nothing)?
5. Which of these come from the customer's side, and which only from the founder?

Each job is written in one form: "When [situation], [customer] wants to [motivation], so they can [outcome]."

**Mechanical check**

```
for each job:
    customer_sources = sources whose file is an order form, a review, or a saved Reddit thread
    founder_sources  = sources whose file is the deck, a one-pager, the website or the video
customer_share = jobs with at least one customer source ÷ all jobs
```

Worked example, Hollis Voice. The founder side is clear: clinics miss calls, and the product answers them, books appointments and sends refill requests (data-room research, 3.2 and 3.6). The customer side is thin: the room holds three order forms and no customer interviews, and a synthetic company has no reviews or Reddit threads. So every job is likely `founder_stated`, and the readout says so plainly.

**Model reading**

```text
Task: write the jobs this startup's customers hire the product to do, and say whose words each job rests on.

Documents:
{{docs: deck, one-pagers, website copy, video claims; order forms in 04_customers/ by page; product reviews from 3.1; saved Reddit threads from 7.2}}

For each job you can support:
1. Write it as "When [situation], [customer] wants to [motivation], so they can [outcome]." in "statement".
2. Name what the customer uses today instead, if any document says so; otherwise null.
3. Give at least one claim with a quote. Mark each source as customer side (order form, review, Reddit thread) or founder side (deck, one-pager, website, video).

Quote the exact span you relied on for every claim. If no customer-side document exists, add a gap "Not in the room: the customer's own words about this job". Do not write a job no document supports. Do not present a founder's sentence as the customer's.

Propose each job's label and the overall label using the rules in "How the readout scores it", and name them in "label_reason".
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "jobs"],
  "properties": {
    "framework": {"type": "string", "const": "jobs_to_be_done"},
    "label": {"type": "string", "enum": ["customer_evidenced", "founder_stated_only", "cannot_check"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "jobs": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["statement", "current_alternative", "label", "customer_claim_ids", "founder_claim_ids"],
        "properties": {
          "statement": {"type": "string"},
          "current_alternative": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "label": {"type": "string", "enum": ["customer_evidenced", "founder_stated", "gap"]},
          "customer_claim_ids": {"type": "array", "items": {"type": "string"}},
          "founder_claim_ids": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
```

**How the readout scores it**

Per job: `customer_evidenced` with at least one customer-side quote; `founder_stated` with founder-side quotes only; `gap` when nothing supports it. Overall: `customer_evidenced` if any job is; `founder_stated_only` if none is; `cannot_check` if no documents exist.

**What it must not do**

- Write jobs from what the model believes customers in this market need.
- Count the founder's description of the customer as the customer's own words.
- Merge distinct jobs into one to make the list look tidy.

### 5.3 Business model canvas

**Inputs**

- The same documents as 5.1.
- `02_financials/financial_model.xlsx`, tabs `P&L` and `ARR_Build`.
- `02_financials/expense_ledger.csv`, vendor and category columns.

**The questions it asks**

The nine blocks, each as a question:

1. Key partners: whom does the company depend on to deliver?
2. Key activities: what must it do well?
3. Key resources: what does it need to own or hold?
4. Value propositions: what does each customer segment get?
5. Customer relationships: how does it keep customers (self-serve, onboarding, account managers)?
6. Channels: how does it reach and deliver to them?
7. Customer segments: whom does it serve?
8. Cost structure: what are the largest costs?
9. Revenue streams: what does it charge for?

**Mechanical check**

```
cost structure:  map every P&L cost line to a block item; list lines over a share the team sets
key partners:    rank ledger vendors by spend in cost of revenue; each top vendor not named
                 in a founder document becomes a room_only partner
revenue streams: every product type in ARR_Build must appear as a block item
```

Worked example, Hollis Voice. The design script sets telephony at 15%, embedded licences at 5% and hosting with model inference at 11% of the revenue basis ([data_room_design_numbers.py](../reports/20261022.02_research/data_room_design_numbers.py)). So the telephony and model providers are key partners whether or not the deck names them. If the deck does not, they are `room_only`. Revenue streams must hold subscriptions, the onboarding fee and the pilot, because `ARR_Build` holds all three (data-room research, 3.4). The ledger's vendor names are set by the generator; the research does not fix them.

**Model reading**

```text
Task: fill a business model canvas for this startup from its own documents and its financial files.

Documents:
{{docs: deck, one-pagers, website copy by line; financial_model.xlsx P&L and ARR_Build by cell; expense_ledger.csv vendor and category rows}}

Script results:
{{script_results: the cost lines mapped to blocks, the vendors ranked by spend, the ARR_Build product types, and every label from entries 1.2 to 1.9}}

For each of the nine blocks (key_partners, key_activities, key_resources, value_propositions, customer_relationships, channels, customer_segments, cost_structure, revenue_streams):
1. Write the fewest claims that cover what the founder's documents say for this block, each with its quote.
2. Add items the financial files show that no founder document states, such as a large vendor or a revenue line. Mark the block "room_only" if every item in it comes from the files.
3. If a script result agrees or disagrees with an item, set "backed" or "contradicted" and link the claim id.
4. If nothing fills a block, add a gap "Not in the room: <block name>" and mark it "gap".

Quote the exact span you relied on for every claim. Use only these documents. Do not add partners, activities or resources the files do not show.

Propose the overall label using the rules in "How the readout scores it", and name the blocks in "label_reason".
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "blocks"],
  "properties": {
    "framework": {"type": "string", "const": "business_model_canvas"},
    "label": {"type": "string", "enum": ["complete", "has_gaps", "has_contradictions", "cannot_check"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "blocks": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["block", "label", "claim_ids"],
        "properties": {
          "block": {"type": "string", "enum": ["key_partners", "key_activities", "key_resources", "value_propositions", "customer_relationships", "channels", "customer_segments", "cost_structure", "revenue_streams"]},
          "label": {"type": "string", "enum": ["stated", "backed", "contradicted", "room_only", "gap"]},
          "claim_ids": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
```

**How the readout scores it**

Each block takes a label from the shared table. Overall, as in 5.1: `has_contradictions`, then `has_gaps`, then `complete`; `cannot_check` when the documents are missing.

**What it must not do**

- Fill a block from what businesses of this kind usually have.
- Leave out a large cost or vendor because the deck does not mention it.
- Treat the canvas as a verdict on the business model.

### 5.4 Porter's five forces

**Inputs**

- The deck's market and competition slides (slides 8 and 9).
- Competitor signals from Scan 3 and comps from Scan 2.
- Customer concentration and contract terms from 1.6.
- Cost of revenue by vendor from 1.7 and 5.3.

**The questions it asks**

1. Rivalry: how many companies sell the same thing to the same customer, and are they growing?
2. Threat of new entrants: what stops a new company from building this?
3. Buyer power: how concentrated are the customers, and how easily can they leave?
4. Supplier power: how much of the cost of delivery sits with a few suppliers?
5. Threat of substitutes: what else does the customer use to get the same job done?

**Mechanical check**

```
buyer power:    share_top1 and share_top3 from 1.6; notice days on the largest contracts
supplier power: largest vendor's spend ÷ cost_of_revenue_full from 1.7
rivalry:        competitors named on slide 9 against competitors found by Scan 3;
                count of each, and names in one list but not the other
substitutes:    current alternatives named in 5.2
```

Worked example, Hollis Voice:

- Buyer power: the largest customer is 21.0% of MRR (PF5), on a 24-month term (data-room research, 3.3).
- Supplier power: telephony is 15% and embedded licences 5% of the revenue basis, and hosting with model inference 11% (the design script). Which vendor holds each share waits on the generator's ledger.
- Rivalry: the data-room research notes that a web search shows vendors already selling voice AI to vet clinics (data-room research, 3.1, option B). The check is whether slide 9 names them. The names come from Scan 3's pre-pulled competitors.

**Model reading**

```text
Task: lay out the five competitive forces on this startup, using only its documents and the other scans' results.

Documents:
{{docs: pitch_deck.pdf slides 8 and 9; contracts in 04_customers/}}

Script results:
{{script_results: concentration and contract terms from 1.6; vendor shares from 1.7; competitor lists and signals from 3.1 and 3.2; comps from 2.1 and 2.2; current alternatives from 5.2}}

For each force (rivalry, new_entrants, buyer_power, supplier_power, substitutes):
1. Write what the deck says about it, with a quote. If the deck says nothing, add a gap "Not in the room: the founder's view of <force>".
2. Write what the script results show about it, citing claim ids. Do not compute anything new.
3. Set the force's label using the rules in "How the readout scores it".

Quote the exact span you relied on for every claim. Do not rate a force high or low from general knowledge of the industry. Do not name competitors that no document or script result names.

Propose the overall label and name the forces in "label_reason".
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "forces"],
  "properties": {
    "framework": {"type": "string", "const": "five_forces"},
    "label": {"type": "string", "enum": ["deck_contradicted", "evidence_found", "deck_only", "cannot_check"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "forces": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["force", "label", "deck_claim_ids", "evidence_claim_ids"],
        "properties": {
          "force": {"type": "string", "enum": ["rivalry", "new_entrants", "buyer_power", "supplier_power", "substitutes"]},
          "label": {"type": "string", "enum": ["pressure_shown", "contradicts_deck", "deck_only", "no_evidence"]},
          "deck_claim_ids": {"type": "array", "items": {"type": "string"}},
          "evidence_claim_ids": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
```

**How the readout scores it**

Per force:

- `contradicts_deck`: the deck describes the force as weak or absent, and a script result shows it acting (for example, "no customer above 9%" against 21.0%).
- `pressure_shown`: a script result shows the force acting, and the deck does not deny it.
- `deck_only`: only the deck speaks to it.
- `no_evidence`: nothing in the room or the scans speaks to it.

Overall: `deck_contradicted` if any force is `contradicts_deck`; `evidence_found` if any force is `pressure_shown`; `deck_only` if every force with content is `deck_only`; `cannot_check` without the deck.

**What it must not do**

- Rate a force high, medium or low from the model's own sense of the industry.
- Name a competitor no document or scan names.
- Compute new shares. It cites the ones Scans 1 to 3 already computed.

### 5.5 SWOT

**Inputs**

- Every claim from Scans 1 to 4 and from 5.1 to 5.4.

**The questions it asks**

1. Strengths: what does the room show the company doing well, backed by a number or a document?
2. Weaknesses: what do the checks show going wrong inside the company?
3. Opportunities: what do the outside scans show the company could gain?
4. Threats: what do the outside scans show could hurt it?

Strengths and weaknesses come from the room. Opportunities and threats come from outside sources (Scans 2 and 3, and the presence scan).

**Mechanical check**

```
for each SWOT item:
    keep it only if every claim id it cites exists in another entry's output
    and none of those claims is unverified
orphans = items with no surviving claim id; they are dropped and listed
```

Worked example, Hollis Voice. Weaknesses the room shows: gross margin of 58.1% once delivery costs are in (PF6), 12-month gross retention of 73.4% (PF3), and the largest customer at 21.0% of MRR (PF5). Strengths the room shows: 212 paying accounts and $2,060,868 of recurring ARR rebuilt from raw data (PF7 and PF1 true values). Opportunities and threats wait on the competitor scans; the research holds no competitor figures yet.

**Model reading**

```text
Task: sort the evidence the other scans found into strengths, weaknesses, opportunities and threats.

Script results:
{{script_results: every claim from Scans 1 to 4 and entries 5.1 to 5.4, with ids, labels and sources}}

For each quadrant:
1. Write each item as one plain sentence. Cite the claim ids it rests on. Quote the exact span you relied on by copying the cited claim's quote word for word; do not write a new one.
2. Strengths and weaknesses use claims whose sources are data room files. Opportunities and threats use claims whose sources are outside (URLs, APIs, filings).
3. If a quadrant has nothing to cite, add a gap "Not in the room: evidence for <quadrant>".

Every item must cite at least one claim id. Do not add an item you cannot cite. Do not balance the quadrants by adding items to a thin one.

Propose the overall label using the rules in "How the readout scores it", and name the quadrants in "label_reason".
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "items"],
  "properties": {
    "framework": {"type": "string", "const": "swot"},
    "label": {"type": "string", "enum": ["complete", "partial", "cannot_check"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["quadrant", "text", "cited_claim_ids", "label"],
        "properties": {
          "quadrant": {"type": "string", "enum": ["strength", "weakness", "opportunity", "threat"]},
          "text": {"type": "string"},
          "cited_claim_ids": {"type": "array", "items": {"type": "string"}},
          "label": {"type": "string", "enum": ["sourced", "dropped_orphan"]}
        }
      }
    }
  }
}
```

**How the readout scores it**

- Per item: `sourced` when every cited claim exists and is verified; `dropped_orphan` otherwise, shown in a folded list.
- Overall: `complete` when all four quadrants have at least one sourced item; `partial` when any quadrant is empty; `cannot_check` when no other scan has run.

**What it must not do**

- Add an item that cites nothing.
- Pad a thin quadrant to make the grid look even.
- Write a new quote. It reuses the cited claims' quotes, which the checker already found.

### 5.6 TAM, SAM and SOM, bottom-up

**Inputs**

- The deck's market slide (slide 8) and any market sizing in the room.
- The rebuilt revenue per account from 1.9 and the rebuilt ARR from 1.2.
- `05_team/hiring_plan.csv`, for sales capacity.
- A cited public count of the target customers (for Hollis Voice, independent veterinary clinics in the markets it serves), saved with its URL and date.

**The questions it asks**

1. How many customers could buy this, from a cited count?
2. What does one customer pay a year, from the room's own numbers?
3. Which of those customers can the company reach today, with its product, channel and geography?
4. How many can the plan win, given the sales hires in the hiring plan?
5. Does the deck size the market bottom-up or top-down (a share of a large industry figure)?
6. How far is the deck's figure from the bottom-up one? A fund partner's own diligence tool finds founders overestimating market size more often than any other issue ([research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md), row 27, paraphrased from journalism). a16z says it does its own sizing ([research_data_room.md](../reports/20261022.02_research/research_data_room.md), 1.2, row 28).

**Mechanical check**

The bottom-up rule: every market figure is a count of customers times what one customer pays. A top-down figure is reported, labeled as top-down, and never used as the market size.

```
ACV       = rebuilt recurring ARR ÷ paying accounts
TAM       = count of all potential customers (cited) × ACV
SAM       = count of customers reachable with today's product, channel and geography (cited) × ACV
SOM       = customers the plan says it will add in its horizon × ACV,
            checked against sales hires in hiring_plan.csv
deck_gap  = deck TAM ÷ bottom-up TAM
```

Worked example, Hollis Voice:

- ACV = $2,060,868 ÷ 212 = $9,721 a year (`arr_true_recurring` and `paying_clinics_now` in [data_room_design_numbers.json](../reports/20261022.02_research/data_room_design_numbers.json); scripted arithmetic). The largest customer counts as one account across 40 locations, so ACV per location is lower than this. A per-location ACV needs a location count per account from the generator.
- Count of independent veterinary clinics: not in the research. The scan returns "Not in the room: a cited count of target customers" until someone attaches a source page. It does not use a number from memory.
- The deck's market figure on slide 8 is not given in the research either. The generator sets it.

**Model reading**

```text
Task: rebuild this startup's market size from the bottom up, and compare it with what the deck claims.

Documents:
{{docs: pitch_deck.pdf slides 8 and 14; any market sizing file in the room; each saved public source for a customer count, with URL and date read}}

Script results:
{{script_results: ACV from 1.2 and 1.9; the hiring plan's sales roles by start month; TAM, SAM and SOM wherever a cited count exists}}

Answer these questions with claims:
1. What TAM, SAM and SOM does the deck state? Quote each figure and the sentence that says how it was built.
2. Is each deck figure bottom-up (a count of customers times a price) or top-down (a share of a larger industry figure)? Quote what tells you. Set confidence to "judged" if the deck does not say.
3. What count of potential customers does each saved public source give, and for what geography and year? Quote it.
4. Which of those customers can the product reach today? Use only what the deck, one-pagers or website say about geography, channel and product. Quote it.

Quote the exact span you relied on for every claim. If there is no cited customer count, add a gap "Not in the room: a cited count of target customers" and do not estimate one. Never use a count, price or market figure from memory.

Propose the label using the rules in "How the readout scores it", and name the rule and claim ids in "label_reason".
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "sizes"],
  "properties": {
    "framework": {"type": "string", "const": "market_size"},
    "label": {"type": "string", "enum": ["deck_exceeds_bottom_up", "consistent", "top_down_only", "not_in_room"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "sizes": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["level", "basis", "deck_claim_id", "count_claim_id", "acv_claim_id", "result_claim_id"],
        "properties": {
          "level": {"type": "string", "enum": ["tam", "sam", "som"]},
          "basis": {"type": "string", "enum": ["bottom_up", "top_down", "unstated"]},
          "deck_claim_id": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "count_claim_id": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "acv_claim_id": {"anyOf": [{"type": "string"}, {"type": "null"}]},
          "result_claim_id": {"anyOf": [{"type": "string"}, {"type": "null"}]}
        }
      }
    }
  }
}
```

**How the readout scores it**

- `deck_exceeds_bottom_up`: the deck's figure is above the bottom-up one by more than `match_tolerance`. The readout shows both, with the ratio.
- `consistent`: the deck's figure is within tolerance of the bottom-up one.
- `top_down_only`: the deck's figure is top-down and no cited count exists to rebuild it.
- `not_in_room`: there is neither a deck figure nor a cited count.

**What it must not do**

- Supply a customer count, a price or an industry figure from memory.
- Use a top-down figure as the market size.
- Turn the market size into a forecast of what the company will earn.

## Scan 6. Founder profiles

Track 1's direction names a founder-quality score from public signals: shipped projects, GitHub activity, papers, hackathon wins, job changes ([problem tracks](../reports/20261022.01_hackathon_sources/problem_tracks.txt), Track 1). This scan uses those signals inside Track 2. It never scores a founder with a number. It says what public evidence exists and what it shows.

Sources and their terms, from [research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), 1.7 and Part 2:

- **GitHub REST**: the user object carries `login`, `company`, `bio`, `public_repos`, `followers` and `created_at`. 60 requests an hour without a token, 5,000 with one.
- **GitHub GraphQL**: contribution history fields are not verified. Read the reference before relying on them.
- **arXiv**: official API, one request every three seconds.
- **Personal sites, talks and writing**: public pages found through Tavily or You.com search, saved with URL and date.
- **X**: paid per read. Link the handle only.
- **LinkedIn**: not scraped. The organisers' tracks document says its terms prohibit it. A LinkedIn data export the founder shares with consent may be read.

What is fair to infer, and what is not:

| Fair to infer, with a dated source | Not fair to infer, ever |
|---|---|
| Years worked in the customer's industry, from a dated role | Age, gender, ethnicity, nationality, religion, politics, health, family |
| Products shipped in the domain, from a repo, launch or release | Commitment from the hours or days someone commits code |
| Talks given and posts written on the problem, with dates | Quality from follower counts or stars alone |
| Whether the interest predates the company | Anything from a photo, voice or accent |
| What the founder says about how the idea arose | A negative from missing GitHub activity (many founders do not code, and private repos are invisible) |

### 6.1 Founder-market fit

**Inputs**

- `05_team/founder_bios.pdf`: two invented founders and the senior team (data-room research, 3.3).
- GitHub user and repos for each handle in the bios.
- Saved personal sites, talks, posts and papers, each with URL and date.
- A LinkedIn export, only if the founder shared it.
- The video claims from 4.1 for anything the founder says about their background.

**The questions it asks**

1. Has the founder worked in the customer's industry? For how long, and in what role?
2. Has the founder built in the product's domain before (here, voice, telephony or AI agents)?
3. Did the idea grow out of the founder's own experience? A former accelerator application reader wrote on Hacker News that this was the main thing they looked for ([research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md), row 58).
4. Can the founder explain the company's numbers? A pre-seed fund reports founders who could not (same file, row 23). Entry 4.3 holds the evidence.
5. What gaps does the team itself name, and who covers them?

**Mechanical check**

```
timeline:          every dated artifact (role, repo, talk, post, paper) with its date and source
domain_tag:        TRUE if the artifact's text matches the domain keywords from the deck's
                   problem and solution claims
industry_tenure:   SUM of months in dated roles tagged to the customer's industry
github_age_months: as-of date − GitHub created_at
domain_repos:      repos whose name, description or topics carry a domain keyword
predates_company:  artifacts tagged to the domain and dated before the company's founding
```

Worked example, Hollis Voice. The founders are invented, and the research fixes no facts about them (data-room research, 3.3). Until the generator writes the bios, every question returns "Not in the room". The feasibility research adds an open point: GitHub's terms on persona accounts were not read, and the safe route is a GitHub organisation Ken owns with repos he commits to ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), 1.7). The company was founded in 2024 (data-room research, 3.2), so `predates_company` tests for domain artifacts dated before 2024.

**Model reading**

```text
Task: say what public evidence shows about each founder's fit with this market.

Documents:
{{docs: founder_bios.pdf by page; for each founder, the GitHub user object and repo list, saved pages for talks, posts and papers with URL and date read, and a LinkedIn export only if provided; video claims about the founders}}

Script results:
{{script_results: each founder's timeline, industry_tenure, github_age_months, domain_repos and predates_company}}

For each founder, answer with claims:
1. Which roles in the customer's industry does a source show, with dates? Quote each.
2. What has the founder built in the product's domain before, with dates? Quote the repo description, launch page or release.
3. What does the founder say about how the idea arose? Quote it.
4. Which gaps does the team name, and who covers each? Quote it.

Quote the exact span you relied on for every claim, with its date. If a question has no source, add a gap "Not in the room: <what is missing> for <founder>". Never infer age, gender, ethnicity, nationality, religion, politics, health, family or anything from a photo. Never treat missing GitHub activity as a negative. Do not read commitment from commit times. Do not use LinkedIn unless an export is in the documents.

Propose each founder's label and the overall label using the rules in "How the readout scores it", and name the rule and claim ids in "label_reason".
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "founders"],
  "properties": {
    "framework": {"type": "string", "const": "founder_market_fit"},
    "label": {"type": "string", "enum": ["direct_fit_found", "adjacent_fit_found", "no_public_evidence", "not_checked"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "founders": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["name", "label", "industry_claim_ids", "domain_build_claim_ids", "origin_claim_ids", "gap_claim_ids"],
        "properties": {
          "name": {"type": "string"},
          "label": {"type": "string", "enum": ["direct", "adjacent", "no_public_evidence", "not_checked"]},
          "industry_claim_ids": {"type": "array", "items": {"type": "string"}},
          "domain_build_claim_ids": {"type": "array", "items": {"type": "string"}},
          "origin_claim_ids": {"type": "array", "items": {"type": "string"}},
          "gap_claim_ids": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
```

**How the readout scores it**

Per founder:

- `direct`: a dated source shows a role in the customer's industry, or a shipped product in the same domain.
- `adjacent`: a dated source shows work one step away (a neighbouring industry or a related technology), named in the claim.
- `no_public_evidence`: no source found. The readout prints "No public evidence found", never a negative.
- `not_checked`: no handle or name to search.

Overall: the strongest founder label, as `direct_fit_found`, `adjacent_fit_found`, `no_public_evidence` or `not_checked`.

**What it must not do**

- Scrape LinkedIn, or use a LinkedIn page the founder did not export.
- Infer anything in the "not fair" column above.
- Read an absence of public evidence as a weakness.

### 6.2 Passion and commitment

**Inputs**

- The timeline from 6.1.
- GitHub repos with their created and last-pushed dates. Check the field names against GitHub's repos reference before relying on them; the feasibility research verified the user object only.
- Saved talks, posts, papers and launches, with dates.
- The founder's tenure at the company, from the bios.

**The questions it asks**

The rubric has five signals. For each one, the question is the same: what dated public evidence shows the founder working on this problem?

1. Shipped projects: products or tools released in the domain.
2. GitHub activity: public repos in the domain, and whether they were kept up over time.
3. Talks: talks or podcast appearances on the problem.
4. Writing: posts, papers or essays on the problem.
5. Tenure: time spent on this problem, at this company and before it.

**Mechanical check**

```
for each founder and signal:
    artifacts       = dated public artifacts of that signal tagged to the domain
    count           = number of artifacts
    span_months     = latest artifact date − earliest artifact date
    predates        = any artifact dated before the company's founding
label per signal:   shown       if count ≥ 2 and span_months > 0
                    some        if count = 1, or several on one date
                    none_found  if count = 0
```

The rubric reports evidence. It never adds the five signals into a score.

Worked example, Hollis Voice. The research fixes no founder facts, so every signal returns `none_found` with "Not in the room: public artifacts for <founder>" until the generator's bios and the GitHub organisation exist (feasibility research, 1.7). The founding year 2024 (data-room research, 3.2) is the line for `predates`.

**Model reading**

```text
Task: list the dated public evidence of each founder's sustained work on this company's problem, by signal.

Documents:
{{docs: for each founder, repo list with descriptions and dates, saved talks, posts, papers and launch pages with URL and date read, and founder_bios.pdf}}

Script results:
{{script_results: each founder's artifacts per signal, with counts, span_months and predates}}

For each founder and each signal (shipped, github, talks, writing, tenure):
1. Confirm which artifacts are about the company's problem or domain. Quote the title or description that shows it, with its date.
2. Drop any artifact that is not about the domain, and say why in one claim.
3. If no artifact exists for a signal, add a gap "Not in the room: <signal> for <founder>".

Quote the exact span you relied on for every claim, with its date. Never read commitment from the times of day or week someone works, from follower counts, or from personal life. Never treat a missing signal as a negative. Many founders do not code in public, and private work is invisible.

Propose each signal's label using the rules in "How the readout scores it", and name the rule and artifact claim ids in "label_reason".
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "rubric"],
  "properties": {
    "framework": {"type": "string", "const": "passion_commitment"},
    "label": {"type": "string", "enum": ["evidence_found", "no_public_evidence", "not_checked"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "rubric": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["founder", "signal", "label", "predates_company", "claim_ids"],
        "properties": {
          "founder": {"type": "string"},
          "signal": {"type": "string", "enum": ["shipped", "github", "talks", "writing", "tenure"]},
          "label": {"type": "string", "enum": ["shown", "some", "none_found"]},
          "predates_company": {"type": "boolean"},
          "claim_ids": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
```

**How the readout scores it**

Per founder and signal:

- `shown`: two or more dated artifacts in the domain, spread over time.
- `some`: one artifact, or several on one date.
- `none_found`: no public artifact. Printed as "None found in public sources", never as a weakness.

A `predates_company` marker shows beside any signal with evidence from before the founding. Overall: `evidence_found` if any signal is `shown` or `some`; `no_public_evidence` if all are `none_found`; `not_checked` without names or handles. The five signals are never added up.

**What it must not do**

- Add the signals into one score, or rank founders against each other.
- Read passion from commit times, weekends, hours or personal life.
- Mark a founder down for having no public GitHub.

## Scan 7. Online presence

The associate's ten tabs include whether the story matches what is online ([research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md), row 1). This scan checks that. A synthetic company has no footprint, so on Hollis Voice it runs on one or two real competitors for contrast and says so on screen (feasibility research, 1.6).

### 7.1 Footprint: web, Hacker News, Product Hunt and app stores

**Inputs**

From [research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), 1.6 and Part 2:

- **The company's website**: for Hollis Voice, `06_product/website_copy.md` in the room. For a real company, its pages saved through Tavily or You.com extraction.
- **Hacker News**: the official Algolia search API, no key, 10,000 requests an hour per IP.
- **Product Hunt**: the official GraphQL API with a token. Its docs say it must not be used for commercial purposes, so a paid product needs permission before relying on it.
- **Apple App Store**: the official Search and Lookup API, about 20 calls a minute. The customer-review feed answered the feasibility research's test but is not documented by Apple; treat it as unofficial.
- **Google Play**: the official reviews API only reads reviews for apps you own. Public listings have no official API; skip them or use search results.
- **Facebook**: reading another Page needs app review. The investor pastes the page text by hand.

**The questions it asks**

1. Does the website say what the deck says (product, pricing, customers, numbers)?
2. Has the company or its product come up on Hacker News, and what did people say?
3. Did it launch on Product Hunt, and how was it received?
4. Does it have an app, and what rating and how many ratings does it carry?
5. Where is the footprint empty? An empty footprint is a finding too (feasibility research, 1.6).

**Mechanical check**

```
website: every number on the site is matched to the deck claim with the same metric,
         using the comparison in 1.5
HN:      hits for the company name and product name, by date, with points and comment counts
PH:      launch date, votes and comment count, if a post exists
Apple:   averageUserRating, userRatingCount and currentVersionReleaseDate from Lookup
```

The Apple field names are the ones in the feasibility research's saved Lookup sample ([sample](../reports/20261022.02_research/raw/feasibility/appstores/itunes_apple_com_lookup_id_284882215_country_us.txt)).

Worked example, Hollis Voice. The website copy's prices are matched against the product one-pager's ($349, $649 and $1,099 a month, from [data_room_design_numbers.py](../reports/20261022.02_research/data_room_design_numbers.py)). Every outside source returns `none_found` with "Not in the room: no public footprint for a synthetic company". The competitor rows come from the pre-pulled files.

**Model reading**

```text
Task: report what this company's public footprint says, and whether it matches the deck.

Company: {{company_name}} ({{target or competitor}})

Documents:
{{docs: website pages or website_copy.md by line; Hacker News hits with URL, date, points and text; Product Hunt post data; Apple Lookup results; any Facebook page text pasted by the investor; the deck claims from 1.1}}

Script results:
{{script_results: the website-against-deck number matches, hit counts per source, app ratings}}

Answer these questions with claims:
1. What does the website say about the product, the customer, pricing and traction? Quote each.
2. Where does the website disagree with the deck? Quote both sides.
3. What themes recur in Hacker News comments and Product Hunt comments (praise, complaints, questions, comparisons)? Quote at least one comment for each theme, with its URL and date.
4. Which sources returned nothing? Add a gap "Not in the room: <source> footprint for <company>" for each.

Quote the exact span you relied on for every claim. Do not judge the company from the size of its footprint. Do not quote or profile individual commenters beyond the comment itself.

Propose each source's label and the overall label using the rules in "How the readout scores it", and name the rule in "label_reason".
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "sources_checked"],
  "properties": {
    "framework": {"type": "string", "const": "online_footprint"},
    "label": {"type": "string", "enum": ["site_disagrees_with_deck", "footprint_found", "footprint_empty", "not_checked"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "sources_checked": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["company", "source", "label", "claim_ids"],
        "properties": {
          "company": {"type": "string"},
          "source": {"type": "string", "enum": ["website", "hacker_news", "product_hunt", "apple_app_store", "google_play", "facebook"]},
          "label": {"type": "string", "enum": ["found", "none_found", "not_checked"]},
          "claim_ids": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
```

**How the readout scores it**

Per source: `found` when it returned something about the company; `none_found` when it was searched and returned nothing; `not_checked` when it was not run (no token, no pasted text). Overall, the first rule that fits:

- `site_disagrees_with_deck`: a number on the website differs from the deck beyond `match_tolerance`.
- `footprint_found`: any source is `found`.
- `footprint_empty`: every source run is `none_found`. This is shown as a finding.
- `not_checked`: nothing was run.

**What it must not do**

- Read a small footprint as a weak company. It reports what exists.
- Profile the people who commented.
- Use Product Hunt data in a paid product without checking its terms.

### 7.2 Reddit threads saved by hand

**Inputs**

- Reddit listing and thread pages saved as `.json` by a person, from their own browser, into a folder the scan reads. For the research, that folder is `docs/reports/20261022.02_research/reddit_corpus/raw/` ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), Rules). In the product, Ken's idea is a small browser that saves a Reddit page as it is opened ([writers' brief](../features/20261022.01_hackathon_plan/00_brief_for_writers.md), Ken's words).
- The scan never fetches reddit.com. Reddit's own rules were not read by the research (feasibility research, 1.6).

**The questions it asks**

1. Which saved threads mention the company, its product or its competitors?
2. What do people in them say: complaints, praise, questions, switching stories, price talk?
3. Which posts describe a first-hand experience as a customer?
4. Does anything in them contradict the deck?

**Mechanical check**

```
parse each saved file: post id, subreddit, created_utc, title, selftext, score, num_comments, permalink;
                       comment id, body, created_utc, score
mentions:  posts and comments containing the company, product or competitor names
counts:    mentions by subreddit and by month
```

Worked example, Hollis Voice. A synthetic company has no Reddit threads, so the label is `none_saved` until threads about real competitors are saved. The research's own Reddit list is about investors, not vet clinics ([research_voice_of_customer.md](../reports/20261022.02_research/research_voice_of_customer.md), "Reddit URLs for Ken").

**Model reading**

```text
Task: report what people say about this company and its competitors in Reddit threads a person saved.

Company and competitors: {{names}}

Documents:
{{docs: each saved post and comment with permalink, subreddit, date and score}}

Script results:
{{script_results: which posts and comments mention which names, with counts by subreddit and month}}

Answer these questions with claims:
1. For each mention, what kind is it: complaint, praise, question, switching, price, or other? Quote the sentence.
2. Does the writer describe using the product themselves? Quote what shows it, and set confidence to "judged" if it is not stated outright.
3. Does any mention contradict a deck claim? Quote both.
4. Which themes recur? List each theme with the claim ids behind it.

Quote the exact span you relied on for every claim, with the permalink. If no saved threads exist, add a gap "Not in the room: saved Reddit threads about <company>". Do not judge or describe the people who wrote the posts.

Propose the label using the rules in "How the readout scores it", and name the rule in "label_reason".
```

**Output shape**

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["framework", "label", "label_reason", "claims", "gaps", "themes"],
  "properties": {
    "framework": {"type": "string", "const": "reddit_saved"},
    "label": {"type": "string", "enum": ["themes_found", "no_mentions", "none_saved"]},
    "label_reason": {"type": "string"},
    "claims": {"type": "array", "items": {"$ref": "#/$defs/Claim"}},
    "gaps": {"type": "array", "items": {"$ref": "#/$defs/Gap"}},
    "themes": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["theme", "kind", "first_hand_claim_ids", "other_claim_ids"],
        "properties": {
          "theme": {"type": "string"},
          "kind": {"type": "string", "enum": ["complaint", "praise", "question", "switching", "price", "other"]},
          "first_hand_claim_ids": {"type": "array", "items": {"type": "string"}},
          "other_claim_ids": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
```

**How the readout scores it**

- `themes_found`: at least one saved post or comment mentions a name, and themes were drawn.
- `no_mentions`: threads were saved but none mention a name.
- `none_saved`: no threads were saved.

Each theme shows how many mentions it rests on and how many are first-hand.

**What it must not do**

- Fetch reddit.com in any way. It reads only what a person saved.
- Describe, judge or profile the people who posted.
- Treat a few loud threads as the market's view.

## Open points for builders

- **Column names.** The research names a few columns (`product_type`, `arr`, `paying_accounts`, `accounts_created_cumulative`). The generator fixes the rest. The prompts take whatever headers the `<doc>` blocks carry.
- **CAC and market size on Hollis Voice.** The research does not fix sales and marketing spend or a count of clinics. Entries 1.9 and 5.6 return "Not in the room" for those until the generator or a cited source supplies them.
- **`spoken_tolerance` and the signal flat band.** The team sets both before Saturday. The answer-key test keeps `spoken_tolerance` honest: PF2b must still be caught.
- **Where an entry's label and tables live.** The ScanResult in [ARCHITECTURE.md](ARCHITECTURE.md) has one optional field, `panels`, for them. Each panel has a `name`, a list of `columns` (names) and `rows` (each row a list of strings). The comps table, the signals grid and the video moments go there, so the page has a place for them. This doc carries the label into each claim's `severity` (see "The order of work inside a scan").
- **Matching needs periods and names.** `conflicts_with` and `corroborated_by` both match on label, unit and period. A deck claim with a null period cannot meet a model cell dated 2026-09, and two holders' `ownership` cannot be told apart by label alone. "Piece verdicts" sets two rules for Saturday: a null period on a "today" claim takes the room's as-of month, and five labels match only on the same name before the colon. After Saturday, a `subject` field on Value would replace the colon rule.
- **Opus 5.5 request parameters.** The feasibility research notes it may reject `temperature` and forced tool choice, from a source it could not confirm on a public page. Test one call with each schema before Saturday ([research_feasibility.md](../reports/20261022.02_research/research_feasibility.md), 1.10).
