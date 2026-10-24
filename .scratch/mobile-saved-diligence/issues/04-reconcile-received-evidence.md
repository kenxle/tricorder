# 04: Close requests against received evidence

**What to build:** When evidence arrives for a company, its request list shows which items are answered, the files answering them, and what remains open. Questions arising from room flags appear in the same request experience, and a flag can take the associate directly to its question.

**Blocked by:** 02: Prepare and retain a company's request; 03: Review a synthetic room as it arrives.

**Status:** ready-for-agent

- [ ] Request-to-evidence matching uses stable request/checklist and file identities. Display text, ordering and similar filenames alone do not establish an answer.
- [ ] An item becomes Answered only when all evidence required by its explicit mapping is present. Partial fulfillment remains Open and identifies what is still missing.
- [ ] Each answered item shows its supporting file or files and allows evidence inspection. Asked-at history and the associate's original selection are retained.
- [ ] Full arrival updates the remaining mapped items without dropping still-missing requests. Reprocessing an arrival is idempotent and preserves custom requests and authored draft text.
- [ ] Custom questions with no explicit evidence mapping remain open rather than being guessed answered.
- [ ] Founder questions linked from flags appear under Questions for the founder without duplication. View in the request opens the dialog at the intended item; a new question does not become marked sent automatically.
- [ ] Reconciled statuses survive app restart and remain scoped to the correct company and request. A failed save does not present a durable completion that was never recorded.
- [ ] Tests cover partial fulfillment, multiple required files, repeat arrivals, unmapped custom items and cross-company isolation. A native walkthrough demonstrates open-to-answered progression and a flag-to-request link.

This ticket consumes the arrival mechanism chosen in ticket 03; it does not introduce a new ingestion engine or email sender.
