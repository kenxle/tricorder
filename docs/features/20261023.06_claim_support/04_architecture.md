# Architecture: claim support

## Summary

Two parts. A scan, `scans/claims/`, reads the pitch and the room and labels every pitch figure by script. A memo step, `scans/memo/claim_support.py`, runs inside the merge and relabels those claims against other scans' flags, because no scan may read another scan's output (ARCHITECTURE.md, "The scan interface"). Both write only existing schema types: Claims, Gaps and Panels.

## Existing structure it uses

- `scans/base.py`: `main`, `Ids`, `gap`, `out_dir`. The scan follows the interface: `NAME = "claims"`, `NEEDS = ("deck",)`, `run(room_dir) -> ScanResult`, run as `python -m scans.claims <room>`. `claims` was already listed in `scans.SCANS`.
- `schema/readers.py` (`pdf_pages`, `text_at`) for slide text, script lines, transcript segments, named cells and CSV rows. Every quote is cut from what `text_at` returns, so `schema/check_quotes.py` passes.
- `schema/settings.py`: `match_tolerance` (0.01) and `spoken_tolerance` (0.10).
- `clients/llm.py` for the optional slide reading.
- `docs/ongoing/checklist.csv` ids, named in each kind's evidence map and ask line.

## Components

| File | Job |
|---|---|
| `scans/claims/numbers.py` | `mentions(text)`: every figure in a string, with its printed form, number, unit, precision, hedge, bound (ceiling or floor), spoken flag and ISO date or month range. Masks slide footers and clock times. |
| `scans/claims/kinds.py` | `KINDS`: about 45 claim kinds, each with a label, unit, period rule, piece, definition, evidence readers, and the document and checklist id to ask for. `classify()` assigns a kind from the words around a figure. |
| `scans/claims/extract.py` | `deck_statements()` (content slides, the claims page folded in as repeats, worked examples set aside) and `video_statements()` (the transcript when present, else the script with beats). Fallback: `claims_json_statements()`. |
| `scans/claims/evidence.py` | `READERS`: one script reader per evidence key (model named cells, cap table, metrics export, revenue by customer, hiring plan, contracts, bios). Each returns `Evidence` with a real Source, or names the missing file. `independent_group()` puts every founder document in one group. |
| `scans/claims/label.py` | Compares each statement with its evidence and with the founder's other statements, assigns the label, writes the Claim, the Gaps and the three Panels. |
| `scans/claims/read.py` | The optional model reading of slides with figures the script did not find. Facts are kept only when their quote is on the slide and their number parses back. |
| `scans/claims/scan.py` | `run()`: wires the above and writes the input Gaps. |
| `scans/memo/claim_support.py` | `apply(readout, room_dir) -> Readout`, and a command for use before it is listed in the merge. |

## Data shapes

All existing types (`schema/claim.py`). The shapes are printed in [02_interface_example.md](02_interface_example.md).

- **Claim.** `scan` `claims`; `check.kind` `script` (or `model` with name `claim_support.read` for a model-read fact, confidence `quoted`); `check.name` `claim_support`, or `spoken_arr_vs_claims_page` / `spoken_number_vs_claims_page` for a spoken figure the deck contradicts. `text` starts with the label. `sources[0]` is the pitch; contradicted claims add every disagreeing source (and, for spoken figures, the deck's own figure); supported claims add repeats and agreeing sources. `value` is set when the kind maps to a schema `ValueLabel`, with the normalised number, unit and period.
- **Panel "claims table".** Columns: `claim id`, `label`, `where`, `quote`, `kind`, `stated`, `normalised`, `spoken`, `agrees`, `disagrees`, `should be backed by`, `ask`. Rows sorted contradicted, unsupported, supported.
- **Panel "claims table counts".** Label counts, from deck and from script, the as-of date, the video source, examples not counted, and, once the memo step ran, `relabelled by the memo step: yes`.
- **Panel "claims not counted".** Worked-example figures.
- **Gap.** One per unsupported kind ("Not in the room: <document>, to back N pitch claims on <kind> (...)"), plus input gaps (no deck, script standing in, no key for the model reading).

## Flows

1. `python -m scans.claims <room>` writes `out/<room>/claims.json`.
2. `python -m scans.memo <room>` merges it with the other scans into `readout.json`.
3. `claim_support.apply` runs over the readout: for each supported or unsupported row, another scan's flag relabels it when the flag cites the same pitch source and words, or when the flag's check settles the row's kind (`CHECK_SETTLES`, check names from FRAMEWORKS). It then recounts and re-sorts.

**Where it plugs in.** `scans/memo/merge.py` STEPS, after `link` and before `pieces`, so piece verdicts and top flags see the final severities. Until the orchestrator adds it: `python -m scans.memo.claim_support <room>` rewrites the readout the merge wrote.

## Independence rule

`FOUNDER` regex: `pitch_deck`, `claims.json`, `pitch_video`, `company_overview`, `website_copy`, `product_one_pager`, `cover_note`. Evidence from that group never supports a claim. A founder statement that disagrees with another founder statement still makes a contradiction (PF2b, BF5), shown with "(same pitch)".

## Alternatives

- **Model-first labelling.** Rejected for the main path: no key here, labels must be reproducible, and the quote checker must pass on every claim. Kept as an optional reading for figures the script misses.
- **Reading other scans' results inside the claims scan.** Forbidden by the scan interface. The memo step does it instead.
- **A separate claims-table JSON file.** Rejected: the readout already carries Panels, and the store and memo export read the readout.
- **Matching other scans' flags by any shared source.** Tried and rejected: two claims citing the same export row are about that row, not about the same pitch figure. It relabelled calls and broker counts on Brasswick and flagged decoy DC3. Only pitch sources count now (`test_a_shared_export_row_does_not_relabel`).

## Failure modes

The PRD's CS-F1 to CS-F9. Every reader returns nothing rather than raising on a missing file, sheet, name or column; the claim then reads unsupported and its Gap names the missing file. The model reading turns a missing key, a refusal, or a bad shape into a Gap.

## Security and privacy

No network in the script path. The model reading sends slide text only, through `clients/llm.py`, and only when a key is set. No answer key is read outside tests and `spike/count_done_when.py` (an eval script).

## Proposed schema changes

Not made (schema/ is not this builder's). For the captain, after Saturday:

1. `Claim.support: Literal["supported", "contradicted", "unsupported", "could not verify"] | None`. Today the label lives in the text prefix and the Panel; a field would let the page filter without parsing.
2. `Claim.claim_kind: str | None` (the claims table's kind, for example `largest customer share`), so the memo step and the page do not join through the Panel.
3. `Value.spoken: bool` and `Value.rounded: bool`, so a spoken figure's normalisation survives outside the table.
4. More `ValueLabel` values for the kinds that map to `other` today (founder years, calls handled, invoices audited, onboarding fee, market count, plan limit), so `corroborated_by` can work across scans for them.

## Links

Verification table: [05_plan.md](05_plan.md). Open questions: [03_prd.md](03_prd.md), "Questions".
