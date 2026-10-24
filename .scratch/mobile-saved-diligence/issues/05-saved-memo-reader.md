# 05: Read the company's saved memo on mobile

**What to build:** From the company working page, an associate or principal opens a saved, versioned memo and follows any sourced line to its claims and supporting evidence. The memo remains readable as a document while retaining the provenance and gaps behind its conclusions.

**Blocked by:** 03: Review a synthetic room as it arrives.

**Status:** ready-for-agent

- [ ] Both demo companies have a saved memo available through the shared Memo contract and an explicit API boundary. The selected memo identifies its version and the readout it was based on.
- [ ] The reader follows the approved memo section order and relevant prototype presentation, including the round and flags, explanation of major flags, exact figures and no prototype chrome.
- [ ] A sourced memo line opens its referenced claims; each claim opens its saved source passage. Returning restores the reader's section and position.
- [ ] Evidence resolves within the selected memo version. Changing the working readout or opening another company does not silently substitute newer or unrelated evidence into an older memo.
- [ ] Synthetic evidence, sourced findings, operator-authored judgment, scenarios and gaps remain visibly distinct. Missing evidence is reported as missing, not converted into a sourced claim.
- [ ] Where multiple saved versions exist, the reader can select one and see the selected version clearly. Missing memo, unavailable version and request failure states are explicit and retryable.
- [ ] Contract and behavior tests cover version selection, claim/source integrity and company isolation. A native walkthrough verifies line-to-claim-to-source navigation and returning to the memo.

This ticket does not depend on request reconciliation or steering. Memo editing, PDF export/share, principal agree/disagree actions, personal copies and what-if computation are separate follow-up work. It covers only the reading and evidence-navigation portion of the principal review-page request.
