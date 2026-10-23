# Review findings and fixes

The independent reviewers found trust and ranking problems in the first implementation. The fixes are being verified before release.

## Code and acceptance review

The independent reviewer inspected `cf8280f` in a separate worktree and exercised the real room outputs. The parent owns the full suite; the reviewer did not repeat it.

- The memo rebuilt an older flag list when the new headline list was empty. This bypassed the new ranking rules and list limits. The memo now respects an empty result when piece verdicts are present. Legacy readouts without pieces retain their fallback.
- The retention flag stores the rebuilt figure, while its peer stores the company's tab reading. Ranking had used the tab reading as the denominator. The shared rule now identifies this check's direction and divides by the rebuilt figure. A test uses the real cohort output and proves its rank against another comparison.
- The review found no separate source-count defect. General linking remains outside this slice.

The reproduction script is retained at `/tmp/review_verdicts_adversarial.py` for this session. The regression tests in [test_pieces_top_flags.py](../../../scans/memo/tests/test_pieces_top_flags.py) and [test_build.py](../../../memo/tests/test_build.py) preserve the checks in the repository.

## Associate persona

This is simulated judgment, not customer evidence. The reviewer followed the associate's cold-read instructions and inspected the generated memo HTML and room evidence. No screenshot or browser interaction was judged.

Rating: workable, with required wording fixes before sharing.

- The retention headline names the disagreement and the files to investigate. Grounded in the associate's need to open weak pieces and verify sources in [PERSONAS.md](../../ongoing/PERSONAS.md).
- The traction and customer verdicts give concrete reasons. Grounded in the associate's need to defend the memo's accuracy at the partners' meeting.
- The absence of a green headline was presented as a room-wide negative despite pending linking checks. The memo now names those pending checks and labels its counts as source links.
- Comps looked like missing company evidence, although the scan had not run. Empty pieces with missing relevant scans now carry a waiting status. The memo and page call them not assessed yet and identify the pending scans.

## Partner persona

This is simulated judgment, not customer evidence. The reviewer followed the partner's cold-read instructions and inspected the generated memo HTML and room evidence. No screenshot or browser interaction was judged.

Rating: workable, with required wording fixes before sharing.

- Traction, retention, and customer weaknesses name concrete disagreements that the partner can examine. Grounded in the partner's concerns about inconsistent reporting and trust in [PERSONAS.md](../../ongoing/PERSONAS.md).
- The partner found the same distinction missing between unfinished checks and missing company evidence. The shared waiting status and the pending-corroboration wording address that concern.

## Follow-up verification

The [spec's verification table](00_spec.md#verification) holds the current results. Re-review of the changed behavior is pending.
