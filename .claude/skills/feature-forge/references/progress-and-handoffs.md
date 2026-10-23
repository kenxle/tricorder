# Keep progress and handoffs useful

The feature lead creates a stable Progress source when work starts and owns its
summary. Link it from the feature entry point and share its review address so
the human can find it again. Whetstone can keep this section in its compact
spec. Use the project's existing review surface rather than creating a second
task board.

Update it when work starts or completes, a review returns, a blocker changes,
a material decision changes the plan, or a release lands. Rewrite the opening
summary to describe what is true now. Use timestamps from a tool. Automate
routine bookkeeping when useful without inventing activity or proof.

## Progress template

Adapt this shape rather than preserving fixed phase numbers:

```markdown
# Feature progress

Current result, what is happening now, and the next action.

## Attention needed

None, or the specific blocker or decision, its owner, and the recommended action.

## Documents

Links to the current product note, brief, prototype, PRD, architecture, Plan,
review history, and release record that exist for this route.

## Work and evidence

| Outcome | Owner | State | Evidence or blocker | Next action |
|---|---|---|---|---|

Link acceptance rows in the Plan instead of copying its verification table.

## Decisions and events

Tool timestamp, change, rationale, and links to the owning source or evidence.
Record approvals only when actually given. State explicitly when none is needed.
```

## Worker return template

Use separate detail files when delegated work benefits from a durable return.
Assign one writer to each file. The lead summarizes returns in Progress rather
than having workers contend over its summary.

```markdown
# Outcome and owner

Result and completion state. Name remaining work plainly.

## Changes and proof

Changed files, tested contents or revision, commands, actual results, and evidence
links. Include a screenshot or flow capture for a visible surface when useful.

## Deviations and surprises

Differences from the contract, reasons, unresolved questions, and useful lessons.

## Follow-ups

Blockers, dependencies, board links, and who acts next. Use None when empty.

## Cleanup needed

Owned temporary paths, flags, resources, or worktrees and their cleanup condition.
```

## Review-round template

Keep earlier rounds. Append a new round when findings or affected proof change.
Review siblings named `<document-stem>_reviews.md` compose with their source.
Avoid competing writers by collecting individual returns before updating that
sibling. Findings and decisions remain linked to their owning source.

```markdown
## Review round: purpose and owner

Inspected contents or revision, assigned criteria, commands and observations,
evidence links, and limits. Report pass, fail, or unverified per criterion.

| Finding and affected behavior | Evidence | Disposition and reason | Owner and recheck |
|---|---|---|---|

Record accepted corrections, deferred work, and rejected findings with rationale.
Link the corrected source and proof. Preserve unresolved disagreements.
```
