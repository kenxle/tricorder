# Architecture: the memo and its PDF

PRD: [03_prd.md](03_prd.md). Folder owner: `memo/` is this feature's ([ARCHITECTURE.md](../../ongoing/ARCHITECTURE.md), "Folder layout").

## Summary

`memo/` turns `out/<room>/readout.json` into a `Memo`: a self-contained, versioned, serializable object. The page and the PDF render from the same `Memo`. Edits make the next version. Nothing in `schema/` changed.

```
readout.json --build_memo--> Memo v1 --apply_edits--> Memo v2 ...      (memo/build.py, memo/edit.py)
                 | quote checker again (schema.check_quotes.check_claim)
                 | text at every source (schema.readers.text_at)
Memo vN --render_html--> memo.html (offline, drill-downs from embedded JSON)   (memo/html.py)
Memo vN --render_pdf---> memo.pdf  (reportlab, numbered section notes)          (memo/pdf.py)
Memo vN --store.save---> out/<room>/memo/memo_vN.json (never overwritten)       (memo/store.py)
```

## Modules

| File | Job |
|---|---|
| `memo/model.py` | The data shape (below) and `Edit`. |
| `memo/template.py` | MEMO_TEMPLATE.md's section table as data: pieces, entries, checklist ids, labels, owner. |
| `memo/build.py` | `build_memo(readout, room_dir, built_at)`: routing, the sections, the quote check, source text. |
| `memo/edit.py` | `apply_edits`, `carry_operator_lines`, unsourced-number marking. |
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

The page holds the room's quoted text. It is written under `out/` (git-ignored) and served only on localhost. The routes take the room id through `server.app.room_dir`, which refuses anything not a known room. No outside call.

## Proposed schema changes

None needed. Two would help later: `Readout.connecting` as structured `{text, claim_ids}` so the memo can show connecting sentences as claim lines; and a `Readout.steps_run` list so the memo knows a step ran and found nothing, rather than guessing from an empty list.

## Alternatives considered

- Rendering the page in React inside `readout/`: it would share components, but `App.tsx` is shared on Saturday and the page must open offline from a file. A standalone page now; a mount later (Attention needed).
- Storing the memo as Markdown: loses line kinds and claim ids, which reader copies need.
