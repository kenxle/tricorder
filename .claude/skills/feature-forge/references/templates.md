# Modular dossier templates

Use stable requirement IDs and relative Markdown links. Main docs may include
leaves with `<!-- forge-include: parts/brief/context.md -->`. Paths are relative
to their containing source, stay inside the dossier and cannot cycle. Review
siblings named `<document-stem>_reviews.md` compose after their document.
Use [document authoring](document-authoring.md) for components, source editing,
and composed review. Use [progress and handoffs](progress-and-handoffs.md) for
optional worker-return and review-round templates.

## Short brief

Target users, context, problem, desired outcome, known constraints, and open
questions that affect the prototype. Keep this short and use it before the
prototype. Link to the prototype artifact and record what its review settled.
Link the focused [product-thinking note](product-thinking.md), including the job,
evidence, priority, alternatives, and preserved user corrections.

## PRD, or detailed brief in the full review route

Problem/user/context; scope and non-goals; solution outline; requirements and
failure cases; applicable UX; analytics/logging decision; rollout/flags decision;
open and resolved questions with rationale; selected PM findings and dispositions.
No mandatory separate Success Metrics section. Product metrics are optional.

## Architecture

Summary; existing structure; reconnaissance leaf; affected components; data/state
contracts; flows; meaningful alternatives leaf and rationale; failure modes;
security/privacy; links to Plan verification and product questions; selected findings.

## Plan

Ordered coherent slices with outcome, scope, dependencies, integration owner and
safe landing; workstream contracts; single verification table:

| Requirement | Acceptance/failure case | Command/observation | Owner | Evidence/status |
|---|---|---|---|---|

Implementation strategy includes the throughput checkpoint: blocking prerequisites,
independent workstreams, shared writable state, and smallest safe decomposition.
Keep it proportional and explain when a single owner is best.

Testing findings/dispositions; rollout and final verification actions; release
authority and readiness evidence. Record human dossier approval only when the
chosen route or project requires it. Tasks reference acceptance rows instead of
repeating requirements.
Release readiness follows the [hard shipping rule](verification-and-release.md#hard-shipping-rule).

## Progress

Use the [Progress template](progress-and-handoffs.md#progress-template). Give its
summary one accountable writer, a stable address, and event-driven updates.

## File organization

Use numbered Markdown documents so the renderer orders the chosen route. A
prototype-first folder may contain a short brief, prototype decision record with
artifact links, PRD, architecture, Plan, and Progress in that order. Existing
brief/architecture/Plan/Progress folders remain valid. Do not rename historical
records merely to adopt the new sequence.
