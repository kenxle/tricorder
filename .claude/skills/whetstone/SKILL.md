---
name: whetstone
description: A short spec, build and independent review route for small understood changes.
---

# Whetstone

Use for small understood behavior changes. Do trivial edits directly and route
uncertain features through [Feature Forge](../feature-forge/SKILL.md). Read project
conventions, fetch before choosing a base, establish an isolated branch/worktree,
and preserve unrelated work.

Check [environment readiness](../feature-forge/references/environment-readiness.md)
before implementation and final proof. For UI changes, apply
[UI quality](../feature-forge/references/ui-quality.md) against any reviewed baseline.

Write a compact spec with problem, behavior, scope, approach, questions, the
verification table, rollout, and review owners. Keep the document without adding
a routine human approval gate. Apply the relevant
[principles](../feature-forge/references/principles.md) and follow
[verification and release](../feature-forge/references/verification-and-release.md).

Use TDD for changed behavior, focused tests, integration checks, independent
review, and changed-flow proof. Do verification, always. Land when readiness and existing authority permit.
Shipping requires a passing full test suite with no failures or errors. Pre-existing,
unrelated, and environment/setup failures still block shipping.
Keep [progress and handoffs](../feature-forge/references/progress-and-handoffs.md)
in the compact record when sufficient. Verify the
[actual release](../feature-forge/references/post-launch.md) and follow
[closeout](../feature-forge/references/closeout.md), including surprises and lessons.
Do not restart the full
document pipeline for a small change.
