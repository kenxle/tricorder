# Prototype-first feature

Use this sequence: short brief, prototype, PRD, architecture, Plan, TDD,
verification, ship, and land. Continue within the agreed scope and existing
authority. Writing a document does not create a human approval gate.
This is the default feature route, not a required path for every task. Adapt the
work to the question while preserving the requested experience and verification.

## Brief to prototype

Create a feature folder under `docs/features/`. Capture target users, their
context, the problem, desired outcome, and known constraints that affect the
experience. Use a document to resolve the premise. Leave detailed
requirements and implementation choices for after the prototype.

Start with [product thinking](../product-thinking.md): the user's job, evidence,
product assumptions, priority against board alternatives, and the best next move.
Keep a focused source note and feed it into the short brief. Reuse what is known
without a rigid interview or a new approval gate. Establish a stable
[Progress page](../progress-and-handoffs.md) for the work.

Build a clickable high-fidelity prototype using the project's design language
and realistic content. Include the main journey and states
that matter to the decision. Label simulated data and effects. Let the human
explore it and record the chosen behavior, open questions, and scope. Resolve
observable questions by trying them rather than sending them back to the human.
Compare prototype variants when they can resolve a real design choice. This does
not require an arena workflow or parallel model competition.

Retain the project's existing voice-of-customer persona judges where available.
Use relevant personas to assess the prototype and later user-facing experience,
following the [reviewer guidance](../reviewers.md). Their findings are not to be
followed blindly, but evaluated, and they may inform the product decision and
complement the human's hands-on prototype review.

The prototype may be throwaway or become the implementation. Record that choice.
Preserve the reviewed prototype and feedback as the
[UI acceptance baseline](../ui-quality.md).
Retained code still needs production checks. For nonvisual work, use a concrete
interface example or spike when it helps; do not add a decorative prototype.

## PRD, Architecture, and Plan

Write the PRD from the agreed experience. Use the detailed product guidance in
the [brief skill](../../../brief/SKILL.md) and [templates](../templates.md).
Preserve context through links to the short brief. Record requirements, failures,
scope, analytics/logging, rollout/flags, and unresolved decisions. Avoid a second
comprehensive brief that repeats the PRD.

Use the [architecture skill](../../../architecture/SKILL.md) to investigate the
existing system and resolve design choices, data shapes, contracts, risks, and
alternatives. The [Plan skill](../../../plan/SKILL.md) defines coherent slices
and owns the acceptance and evidence table. Its throughput checkpoint identifies
blocking prerequisites, independent workstreams, shared writable state, and the
smallest safe decomposition. A single owner is a valid choice.

Choose PM, testing, and other review perspectives for the uncertainties they can
resolve. Integrate their findings. Preserve useful alternatives in source leaves.
Continue into implementation without routine human document approval. Return to
the human when a new material product decision or missing authority requires it.

## TDD, verification, ship, and land

Follow [verification and release](../verification-and-release.md). Build behavior
with the test-first loop, verify the integrated result independently, prepare
coherent PRs, and land when the evidence and standing authority support it.
Keep the short brief, prototype decision, PRD, architecture, Plan, and Progress
current so the human can inspect the complete record at any point.
