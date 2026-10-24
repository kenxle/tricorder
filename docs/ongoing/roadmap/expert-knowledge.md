# expert-knowledge

Give each of Tricorder's analyses what an expert investor knows: what they check first, what good and bad look like at seed and Series A, and what they ask the founder. Each analysis then reads its knowledge when it runs.

- **Status today:** started. Kimmy's traction and revenue, and burn and runway, files reach the model; the other pieces have no file yet. See [Status](#status-2026-10-24-afternoon). Asked for by Ken on 2026-10-24 at 11:18 AM, on [his desk](../../KEN_DESK.md): "let's get kimmy working on embedding expert knowledge for the different analyses".
- **Who builds it:** Kimmy, with her agents.
- **Waits on:** nothing. The raw material is written.
- **Checked against:** the 33 [document guides](../../reports/20261022.03_document_guides/INDEX.md) hold green flags, red flags and checks per document, with sources. The analyses read none of them at run time today; the checks' rules sit in code and in [FRAMEWORKS.md](../FRAMEWORKS.md).

Back to the [roadmap](../ROADMAP.md). How to read the detail: [how_to_read.md](how_to_read.md).

## Status, 2026-10-24 afternoon

For Ken and Kimmy. In short: Kimmy's two files now reach the model, no existing red-flag check contradicts her, and most of her red flags wait on checks that are not built yet.

### What is wired

- **The loader.** [scans/knowledge.py](../../../scans/knowledge.py) returns a piece's file from `knowledge/<piece>.md`. A missing or unreadable file means no knowledge, never an error.
- **The model door.** [clients/llm.py](../../../clients/llm.py) `read()` takes `knowledge=`. The block sits after the task, inside `<expert_knowledge piece="...">`, and tells the model it is a lens: never quote it, cite it, or take a number from it. The system prompt is unchanged.
- **The deck slide reader** ([scans/claims/read.py](../../../scans/claims/read.py)) loads traction and revenue. The slides it reads hold named customers, pilots and contract dates.
- **Steering's rewording** ([steering/reword.py](../../../steering/reword.py)) loads the file of the piece the investor is steering. Steering traction and revenue, or burn and runway, now carries Kimmy's lens.
- **Tests.** `clients/tests/test_llm.py` checks that each file's text reaches the prompt through a fake client (no network), that a missing file sends no block, and that both callers ask for their piece. `scans/claims/tests/test_read.py` checks the slide reader sends the traction block.
- **The memo's expert-read sections** ([scans/memo/sections.py](../../../scans/memo/sections.py), added 15:22). Traction and revenue (section 7) and burn and runway (section 10) each get a short report: the model writes it with Kimmy's file in the prompt, every sentence citing claim ids, and a script checks every id and every figure against the claims. Without a key a script drafts the same five parts from the claims and a table of her rules. Each carries an interactive Plotly chart from script data ([scans/memo/charts.py](../../../scans/memo/charts.py)). Tests: `scans/memo/tests/test_sections.py`.
- **Not yet reading the knowledge.** No model call reads the financial statements today: the burn checks are scripts, and 1.4 (burn against the hiring plan) is not built. The contract reader's model seam (`set_model_reader` in `scans/redflags/contract_reader.py`) has no model behind it yet. When either lands, it passes `knowledge=block([...])`. The [financial-model](financial-model.md) rebuild does not read the files yet either.
- **Hollis Voice answer key.** The slide reader only runs with a model key, so the scored readout without a key is unchanged. A keyed run against `eval/score.py` has not been done.

### Kimmy's red flags, against the checks

Check names are the ones in `scans/redflags/` and FRAMEWORKS.md. "Not built" means the module named in `scans/redflags/scan.py` does not exist yet.

| Kimmy's rule | Check that covers it | Where it stands |
|---|---|---|
| Revenue depends on one or a few customers | Deck claim support in the claims scan tests the deck's "largest customer share" against the customer file. 1.6 `top_customer_share` (customer concentration) is not built. | Partly covered. Caught only when the deck states a share. |
| A pilot annualized into ARR or MRR | 1.12 kind a `mrr_column_vs_subscription_rows` (pilot money in the MRR column). 1.2 `arr_from_subscription_rows` and 1.13 `pilot_without_duty_to_convert_vs_recurring` are not built. | Covered for the MRR column. The ARR build and the pilot contract sides are missing. |
| One-time fees or services counted in ARR or MRR | 1.12 kind h `one_time_fees_in_recurring_metrics`. Kind a also catches non-subscription lines in MRR. | Covered for fees. Services have no check of their own. |
| Booked value presented as revenue | 1.13 check 4 `signed_not_live_vs_revenue` (revenue counted before a contract starts). 1.12 kind b `billings_vs_recognised_revenue` and kind g `deferred_revenue_vs_earned` (cash or billings counted as earned). | Covered for contracts counted early and cash counted as revenue. Nothing compares a stated total contract value with revenue. |
| Committed ARR kept apart from live ARR | 1.13 check 4 `signed_not_live_vs_revenue`. | Partly covered, the same check. |
| Easy cancellation or a short term makes contract value weak | 1.13 check 1 `cancellable_within_notice_vs_arr`. | Covered. |
| A forecast should rest on contracts, not pipeline | 1.13 check 3 `plan_revenue_past_term_end` and check 6 `counted_line_without_contract`. | Partly covered. Signed and pipeline revenue in the plan are not told apart. |
| One month of usage charges times 12 shown as ARR | None. | Missing. |
| Burn left out of the hiring plan | 1.4 `payroll_from_hiring_plan_and_rerun_cash` is not built. 1.12 kind e `contractor_spend_vs_headcount_and_burn` catches contractors left out of the plan's burn. | Partly covered: contractors only. |
| Runway: 18 months after the round closes, as a baseline | 1.4 is not built. | Missing. |
| Headcount or costs rising without progress on the milestone | None. This is a model reading, not a script. | Missing. |
| Cash roll ties to ending cash and the bank | None. No bank statement is read today. | Missing. |
| Revenue against billings, collections and deferred revenue | 1.12 kinds b and g. | Covered. |
| Net income against operating cash flow | None. | Missing. |
| Financing proceeds against the cap table and balance sheet | 1.10 `cap_table_reconcile` is not built. | Missing. |
| Prior statements changed during the raise | None. | Missing. |

### Wording and severity

No built check's wording or severity contradicts Kimmy, so no check changed. The built checks state facts (what a file counts, against what) and never call non-recurring revenue worthless or excuse concentration as early. No numbers were added.

Three points for Ken and Kimmy to settle before the unbuilt checks are written:

- **Concentration at an early stage.** FRAMEWORKS 1.6, question 5, cites MicroVentures: early concentration is not a red flag when the founders plan to spread revenue. Kimmy says dependence on one or a few customers is concerning in general and should not be dismissed because the company is early. 1.6's watch line (`concentration_line`) is also not hers; she gives no number.
- **When runway is measured.** FRAMEWORKS 1.4 measures runway from the data date and watches under `runway_floor`. Kimmy's 18 months is counted after the round closes, as a baseline and not a cutoff, with longer runway when the market is slow or the plan needs more capital.
- **One flag title.** The memo titles every kind a flag "MRR counts a pilot as recurring" (`memo/build.py`, `FLAG_TITLES`). Kind a also fires on one-time fees and pass-through money, which Kimmy treats as separate cases. A title by kind would match her. This is the readout's words, so it is Ken's call.

### What is missing

- Knowledge files for the other pieces: retention, customers, unit economics, market, comps, team, the pitch itself, legal and cap table, and the outside world.
- The red-flag checks marked not built above, starting with 1.2 (ARR definition), 1.4 (burn against the hiring plan) and 1.6 (customer concentration).
- The financial-model rebuild reading the knowledge files.
- A keyed run of the readout on Hollis Voice scored with `eval/score.py`.

## Detail

### The analyses

The readout's pieces, as the code names them in `scans/memo/pieces.py` and `schema/claim.py` (`PIECE_ORDER`): traction and revenue, retention, burn and runway, unit economics, customers, market, comps, team, the pitch itself, legal and cap table, and the outside world.

### What exists to draw on

- The [document guides](../../reports/20261022.03_document_guides/INDEX.md): per document, what a first pass checks, green flags, red flags, what a script can check, what a model must read, and what to ask for if it is missing. Every point is sourced.
- [FRAMEWORKS.md](../FRAMEWORKS.md): the checks and their formulas, and how piece verdicts are set.
- [CHECKLIST.md](../CHECKLIST.md): every item Tricorder looks for, by stage.
- The research: [voice of the customer](../../reports/20261022.02_research/research_voice_of_customer.md) and [the gaps](../../reports/20261022.02_research/research_gaps.md), with investors' own words.
- Ken's notes from Kimmy on [the desk](../../KEN_DESK.md): testimonials on the B2B side, social traction for B2C, and the hard part, checking founders who know more than the VC.

### Includes

- One knowledge file per analysis, in a folder the code reads (for example `knowledge/<piece>.md`). Each holds, by stage: what an expert checks first, the benchmarks that separate strong from weak (each with a source), the green flags, the red flags, and the questions to ask the founder.
- Where the expert knowledge disagrees with a check's current threshold or a piece's verdict rule, the file says so, and the change goes on the board for the check's owner.
- The model's prompts for each analysis load that analysis's file, so the words a model reads carry the expertise. Numbers still come from scripts.
- The knowledge Ken heard from Kimmy today goes in: B2B testimonials, B2C social traction, and how a VC checks a founder who knows the field better.

### Done when

- Every analysis has its knowledge file, with a source on every benchmark.
- At least the analyses on the demo path (traction and revenue, retention, burn and runway, customers) load their file when they run, and a test shows the file's text reaches the prompt.
- The readout on Hollis Voice still scores the same or better on its answer key (`eval/score.py`).

### For Kimmy to decide

- The file layout and how much each holds.
- Which analyses to do first. A suggestion: the four on the demo path above.

**Judgment:** yes.

### Added 13:03: it feeds our own financial models and the red flags

Ken, on the prototype: "we also will want to start integrating kimmy's expert knowledge to build our own financial models and identify red flags".

- **Our own financial models.** The knowledge files give [financial-model](financial-model.md) its assumptions and benchmarks by stage, so Tricorder can rebuild a company's model its own way and set it beside the founder's.
- **Red flags.** The knowledge files give the [redflag-engine](redflag-engine.md) its thresholds and the patterns an expert looks for, each with a source. A threshold still runs as a script; the knowledge says what it should be and why.
