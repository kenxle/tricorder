# Focused reviewer perspectives

## Dispatch instruction for a fresh reviewer

Give the reviewer its assigned perspective and criteria, authoritative source
headings, integrated revision/worktree, relevant evidence and permission to inspect
code or run checks. Ask it to investigate rather than rubber-stamp builder claims.
Require concrete findings with severity, source location, requirement affected,
observed behavior, recommended correction and evidence limits. It may read adjacent
sources where needed. It must not edit outside assigned authority or ship code.
The reviewer returns pass/fail/unverified per assigned criterion; the orchestrator
integrates dispositions and assigns rechecks. These are generic agent instructions,
not dependencies on named private agents or plugins.

Select reviewers by need; each check has one owner independent of its builder.
For UI work, use [UI quality](ui-quality.md). The reviewed prototype and user
feedback are the baseline. Review fidelity rather than reopening settled aesthetics.
A delegated lead may own checks explicitly; parents reuse evidence rather than
dispatching overlapping rosters. Choose supported models by ambiguity and quality.

Give reviewers the [shared principles index](principles.md) and a clear statement
of the intended behavior. Independent reviewers judge the same scope from their
assigned perspective. Cross-model review is useful when it adds signal, not a
mandatory model roster.

Synthesize findings instead of applying every suggestion. Verify each claim
against the code and evidence, combine duplicates, and preserve disagreements.
Separate issues to fix from useful suggestions, contextual observations, and
dismissed findings. Give a concrete reason for each disposition. Agreement can
strengthen a finding, but a defect proven by one reviewer still needs attention.

| Perspective | Purpose |
|---|---|
| Product management | Substantial brief: user need, scope, outcomes, missing behavior and rollout |
| Architecture | Consequential/uncertain design: recon, contracts, alternatives and failure modes |
| Security | Changed trust boundaries, authorization, sensitive state, abuse and privacy |
| Testing | Optional Plan perspective: measurable acceptance, variants, seams and release coverage |
| Staff design | Actual UI judgment when useful: interaction, hierarchy, accessibility and existing design conventions |
| Customer persona judges | Retain the project's existing voice-of-customer persona agents for prototype and user-facing review: task fit, comprehension, language, and workflow friction |
| Cross-model | Independent alternative-model judgment when useful for consequential code or ambiguous decisions |
| Code quality | Required before PR: integrated code correctness, maintainability and conventions |
| Completion evaluator | Required before PR: integrated implementation vs requirements and Plan acceptance |

One suitable independent reviewer may own both code quality and completion.
Orchestrator self-review cannot substitute. Inspect actual code and behavior;
tests alone do not establish full implementation. Map each criterion to evidence
and pass/fail/unverified; resolve required gaps and recheck affected behavior.
Record inspected revision, commands, findings, disposition and limits. Never
fabricate reviewers, approval or execution evidence.

## Voice-of-customer persona review

Use the consuming project's existing customer persona agents and their supporting
research for user-facing work. Keep their definitions intact. Select the personas
relevant to the target users and give them the actual prototype or running flow,
user context, and the behavior being evaluated. They can inform early prototype
choices and assess the integrated experience before release. Recheck affected
findings after changes without repeating unchanged reviews.

These judges bring the intended users' perspective alongside professional design
and engineering review. Ask for specific friction and its effect on the user's
task. Separate findings grounded in persona research from agent inference. Their
output is simulated judgment, not new customer testimony or evidence that the
feature works. It complements independent acceptance and changed-flow proof.

Persona definitions stay with the consuming project. This package does not invent
customer profiles when none exist or copy a project's private research.

Changed user workflows receive one final independent flow walk before PR. It may
share an explicitly assigned completion owner. Use tool/browser proof during
iteration, rather than dispatching a flow walker for every build loop.
