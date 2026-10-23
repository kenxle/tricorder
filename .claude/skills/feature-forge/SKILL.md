---
name: feature-forge
description: Develop features through a short brief, prototype, PRD, architecture, Plan, TDD, verification, shipping and landing.
---

# Feature Forge

Read the consuming project's instructions and existing work. Fetch before choosing
a base, use an isolated branch/worktree, and preserve unrelated changes. Resolve
questions from code, documents, or experiments before asking the human. Reserve
questions for product decisions or authority the available evidence cannot settle.

## Choose the route

Use judgment to select the appropriate documents, document components, and reviewers. You are aiming to create reliable, secure software that users love.

- New or changed user experience: use [prototype first](references/runbooks/prototype-first.md).
- Small understood change: use [Whetstone](../whetstone/SKILL.md), retaining its compact spec and evidence.
- Explicit request for the comprehensive pre-build document review: use [full dossier](references/runbooks/full-dossier.md).

For nonvisual features, use the prototype-first sequence with a concrete interface
example or executable spike when it helps settle the behavior. Skip an artifact
that adds no useful information and record why. Do not manufacture a UI.

Routes are useful starting points. Adapt or combine them to fit the actual work;
do not force a bug fix, investigation, refactor, or evaluation through the feature
sequence. Keep the documents that explain the work and its decisions. Preserve
explicit user choices, TDD for behavior changes, independent verification, and
release authority when choosing a different path.

## Shared guidance

Use the [principles index](references/principles.md) to find applicable pstack
principles. Read the relevant leaf before applying it. These principles guide
judgment; they do not grant tool access or override project instructions.
Give delegated agents the same index and applicable leaves in their contracts.

Use the [writing guidance](references/writing.md) for prose and the
[comment review adapter](references/comment-review.md) for useful scoped comment
review. They do not introduce a fixed reviewer or tool chain.

Keep the documents using the [templates](references/templates.md) and
[authoring guidance](references/document-authoring.md). Markdown is
authoritative. Compose source leaves and review history for human inspection;
give builders the relevant authoritative sections. HTML is optional via
`scripts/build_feature_docs.py <feature-folder>` and requires Pandoc. The build
uses the house document style when it can find it: first the folder named by
`FORGE_DOC_STYLE_DIR`, then Lahe through the `lahe` command on PATH. It inlines
the style in the page, so Lahe's style switcher can restyle it, and lays the
page out as the style expects. Without a style it builds a plain page and
prints one line to stderr. No user-level instruction file is needed. Use the
installed Lahe skill when available for live review.

Choose implementation order, tools, delegation, and reviewers to fit the work.
Use [contracts and slices](references/contracts-and-slices.md) for coherent
landings. Keep coupled behavior together and the application working after each
landing. Do not repeat the document pipeline for each slice.

Check [environment readiness](references/environment-readiness.md) before
implementation and final proof. Keep a stable
[Progress page and handoff record](references/progress-and-handoffs.md).
For user-facing work, verify [UI quality](references/ui-quality.md) against the
reviewed prototype and feedback, with automated checks for repeatable style rules.

Every route follows [verification and release](references/verification-and-release.md):
TDD for behavior changes, independent review of the integrated result, real
acceptance evidence, and release decisions under the project's existing authority.
Shipping requires a passing full test suite with no failures or errors. Pre-existing,
unrelated, and environment/setup failures still block shipping.
Verify the [actual release](references/post-launch.md) and finish
[closeout](references/closeout.md), including durable documents and lessons.
