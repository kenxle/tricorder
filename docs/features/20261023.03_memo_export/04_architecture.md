# Architecture: the memo and its PDF

PRD: [03_prd.md](03_prd.md). Folder owner: `memo/` is this feature's ([ARCHITECTURE.md](../../ongoing/ARCHITECTURE.md), "Folder layout").

## Summary

`memo/` turns `out/<room>/readout.json` into a `Memo`: a self-contained, versioned, serializable object. The page and the PDF render from the same `Memo`. Edits make the next version. Nothing in `schema/` changed.

```
readout.json --build_memo--> Memo v1 --apply_edits--> Memo v2 ...      (memo/build.py, memo/edit.py)
                 | quote checker again (schema.check_quotes.check_claim)
                 | text at every source (schema.readers.text_at)
Memo vN --render_html--> memo.html (offline, drill-downs from embedded JSON)   (memo/html.py)
Memo vN --render_pdf---> memo_vN.pdf, once; memo.pdf is its copy (reportlab)       (memo/pdf.py, memo/export.py)
Memo vN --store.save---> out/<room>/memo/memo_vN.json (exclusive create)          (memo/store.py)
```

## Modules

| File | Job |
|---|---|
| `memo/model.py` | The data shape (below) and `Edit`. |
| `memo/template.py` | MEMO_TEMPLATE.md's section table as data: pieces, entries, checklist ids, labels, owner. |
| `memo/build.py` | `build_memo(readout, room_dir, built_at)`: routing, the sections, the quote check, source text. |
| `memo/compose.py` | Memo-local composition: the ARR figures side by side (below). |
| `memo/sources.py` | A source as a partner reads it: `fields`, `reads_as`, `fmt_number`. |
| `memo/edit.py` | `apply_edits`, `carry_operator_lines`, unsourced-number marking, detaching claims from a rewrite with a new figure. |
| `memo/store.py` | Versions on disk. |
| `memo/html.py`, `memo/pdf.py` | The two renderers. |
| `memo/export.py` | The one path the CLI and the routes share. |
| `memo/__main__.py` | The CLI. |
| `server/memo_routes.py` | The routes, an `APIRouter`; one include line in `server/app.py`, placed before the page mount (the mount at "/" would catch the routes otherwise). |

## The memo's data shape

Written for the reader-scenarios slice, which lays a reader's copy over one shared version.

```
Memo
  room, company, readout_built_at, built_at
  version: int                     1, 2, 3 ... one per export or edit batch
  based_on_version: int | None
  synthetic_notice, stage
  sections: [MemoSection]          16, in the template's order
  claims: {id: Claim}              every claim a line cites, plus the claims they link to (schema.claim.Claim, unchanged)
  asks: {"ask-01": AskItem}        the readout's ask list, in order
  checklist: {"C02": ChecklistRef} coverage rows, with the published checklists that name each item
  sources: {"uri|locator": SourceText}   text at each locator, read at export, so the page opens offline
  changes: [ChangeEntry]           version, at, author, what
  withdrawn_lines: [line id]       Tricorder lines or blanks the operator replaced or removed
  steps_missing: [str]             merge steps not built (link, pieces, top_flags)

MemoSection: number, key, title, who_writes, lines: [MemoLine], empty_because: [gap text]

MemoLine
  id                stable: "s07-redflags-007", "s02-recommendation", "s14-ask-03", "op-2-1"
  kind              claim | reading | gap | operator | scenario | slot | pieces | coverage | ask | unverified | fact | source | change
  text, label
  claim_ids, checklist_ids, ask_ids     what one click opens
  gap: {what, why, would_need, missing_from: room | readout}
  author, version, unsourced_numbers    operator lines only
  severity          green | red | flag | watch | info
```

Line ids are built from what the line shows (section and claim id, slot name, ask number), so they stay the same when the readout grows. That is what lets a rebuild keep the operator's lines after the line they followed, and what a reader copy can anchor to. `scenario` is reserved; the export never writes one.

**For reader-scenarios:** a reader copy is `{reader, base_version, edits: [Edit], scenarios: [...]}` applied over `memo_v<base_version>.json` with the same `apply_edits`, saved apart from the shared versions. The shared version never changes when a reader edits.

## Views and audience

Each line has an `audience`: `all` (both views and the PDF), `page` (both views, not the PDF: the ask list's summary line) or `operator` (the operator view only: blanks, each ask, each pitch claim, each source, coverage lines of an empty section, readout-gap explanations). `html.visible(section, view)` picks the lines for `partner`, `operator` or `pdf`, and the PDF uses the same function, so the two forms cannot drift. Sentences inside a claim that describe a script (a path under `scans/`, a `.py` file, a snake_case check name, a "(C34)" checklist number) are dropped from partner text by `build.partner_text` and by the page's `plain()`, which match the same patterns; the operator view shows the full text. A section with nothing in it is `collapsed`: one line naming the scans it needs.

The recommendation in section 2 is not stored. `html.recommendation(memo)` builds it from section 15's operator lines each time the page or the PDF renders, so editing section 15 is the one place to change it.

## Memo-local composition

The merge's link and connecting steps will say which claims agree and why. Until a readout carries that, the memo composes exactly one sentence itself: when the room holds two or more ARR figures, red flag 1 lists them side by side, largest first, each with its file and place, and links every contributing claim (`compose.arr_side_by_side`). A figure comes from a claim's own value labelled `arr` (USD), from a spreadsheet line named ARR, or from the ARR column of a row that an ARR or MRR flag cites. Nothing is added, subtracted or rounded beyond formatting, and the line is marked `composed`, so the drill says the figures were put side by side from the claims below. The flags those figures come from are behind the line, one click away. Grouping by subject is the other memo-local rule: red flags whose check title or value label match share one line, in full for the first, with the rest behind it; the pitch's figures in a section share one line with counts by the claims scan's verdict. When the link step's `connecting` sentences reach the readout, they replace this.

## Sources as a partner reads them

`sources.reads_as` turns a cited place into words: a CSV row as its column names with their values (from `schema.readers.csv_row_text` on row 1 and the cited row), a spreadsheet cell as sheet, line (column A of its row), column (the nearest short heading above it) and value, a CSV header row as its column names. Numbers print whole or to two decimals with thousands separators. A column or line named for money gets "$", one named for a count gets none, and otherwise "$" or "%" appear only when a claim's text writes the figure that way. The PDF's notes and the page's source panel both show it, beside the source text with the quote marked.

## Steered claims

A steer (`steering/engine.py`) keeps the claim it replaced in the readout and writes `["replaced", old id, old text, new id]` in its "steer N: what changed" panel. The builder reads those rows: the old claim is not routed to a line or a flag, the new claim's line carries `replaces: [old id]`, and the drill shows the old claim under "Before the operator steered it". A steered piece's reason line is the piece's `reason`, which the summary already shows.

## Routing a claim to a section

Piece (when the pieces step placed it), then value label (`template.LABEL_SECTION`), then FRAMEWORKS entry (check name through `scans.memo.checklist.ENTRY_CHECKS`, then the template's "Filled from" column), then the room folder of its first source. Label goes before entry because the template's entry 1.12 row would send an MRR mislabel to business model; the label sends it to traction, where a partner looks for it.

## The PDF

| Option | Verdict |
|---|---|
| **reportlab** (chosen) | Already installed: it is in `data_room/requirements.txt`, which draws the test decks. Pure Python, no system binary, deterministic. Imported only when a PDF is written. Added to `requirements.txt` with a comment, since `memo/` now needs it at run time. |
| Headless Chromium printing the page | Same look as the page, but needs a browser binary on the demo laptop and a subprocess; Playwright for Python is not installed. No CSS footnotes either. |
| pandoc | Installed (3.1.3) but needs a LaTeX engine for PDF; none is installed. |
| weasyprint | Not installed; a new dependency with system libraries. |

Footnotes print as numbered notes at the end of each section (PRD question 1).

## Failure modes

See the PRD's failure table. One more: a source whose text is longer than 6,000 characters is cut to a window around the quote in `sources`, so the page stays small; the quote checker always reads the whole text.

## Security and privacy

The page holds the room's quoted text. It is written under `out/` (git-ignored) and served only on localhost. The routes take the room id through `server.app.room_dir`, which refuses anything not a known room. No outside call. Every source resolves through `memo/rooms.py`: inside the readout's room, or the full room a "read the full room" steer names (`scans.memo.merge.reads_room`), never by absolute path, `..` or into an answer key; `POST /source` and `/files` use the same rule. The page is filled in one pass over its template, and its embedded JSON escapes `<`, `>` and `&` (wave 2b review, B1, S1, S2).

## Proposed schema changes

None needed. Two would help later: `Readout.connecting` as structured `{text, claim_ids}` so the memo can show connecting sentences as claim lines; and a `Readout.steps_run` list so the memo knows a step ran and found nothing, rather than guessing from an empty list.

## Alternatives considered

- Rendering the page in React inside `readout/`: it would share components, but `App.tsx` is shared on Saturday and the page must open offline from a file. A standalone page now; a mount later (Attention needed).
- Storing the memo as Markdown: loses line kinds and claim ids, which reader copies need.
