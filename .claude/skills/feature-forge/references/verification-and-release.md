# Verification and release

Every route retains documents, independent review, and evidence. The agent chooses
methods that establish the required behavior using the consuming project's tools.

## Hard shipping rule

Do not ship, merge, deploy, or enable a feature while any test failure, test error,
or required verification error remains. The full project test suite must pass.
This includes failures that predate the change, reproduce on the base branch,
appear unrelated to the diff, or come from missing keys or environment setup.
The cause explains what needs fixing; it does not make a failure nonblocking.

Fix the code or setup and rerun the full suite in the corrected environment.
If a required key, service, or other prerequisite is unavailable, report shipping
blocked and name what is missing. Do not skip, suppress, or exclude failing tests
to claim a pass. A partial run, feature flag, or confidence judgment cannot waive
this rule. Preserve the actual results as evidence.

## Build and verify

Check [environment readiness](environment-readiness.md) before implementation
and final proof. For UI changes, apply [UI quality](ui-quality.md), including
repeatable style checks and browser fidelity to the reviewed baseline.

Use the [test-first loop](build-loop.md) for behavior changes. Run targeted checks
while developing, seam checks after integration, and the required final project
checks. Exercise observable behavior and meaningful failures through the actual
interface. Browser tools suit browser journeys; use the appropriate interface
for APIs, CLIs, libraries, or other applications.

Before PR, an independent reviewer checks integrated code quality and acceptance.
An explicitly assigned reviewer can own both checks and the final changed-flow
walk. Choose [review perspectives](reviewers.md) for actual risks. No fixed roster
or duplicate parent/lead review chain is required. Self-review cannot replace the
independent check. Missing required review, failed checks, or unverified required
acceptance blocks release readiness. Record the gap rather than inventing proof;
confidence cannot waive a required check.

Retain the project's existing voice-of-customer persona judges for relevant
user-facing changes. Their review complements staff design judgment and the
independent flow walk; it does not substitute for acceptance evidence.

The Plan owns the verification table; Whetstone uses its compact spec instead.
Record pass/fail/unverified, the inspected revision, commands or observations,
evidence, and limits. Resolve required findings. Recheck what a change invalidates
and reuse evidence that still matches the code and relevant conditions.
Use [tested-code evidence](tested-code-evidence.md) to identify dirty files and
relevant setup as well as the revision. The helper does not cache passing results.

## Ship and land

All tests should pass before shipping, regardless of whether the tests are related to your work or not. Failing tests means you need to go fix something.

Prepare coherent PRs with proof, dependencies, and rollout. Follow through onchecks, review findings, conflicts, and required corrections. Judge automatedfindings against the code; fix real issues and explain dismissals.

Use confidence based on acceptance evidence, independent review, remaining
uncertainty, and recovery options to decide release readiness. An unsupported
confidence score is not proof. When readiness is insufficient, improve the work
or verification. Keep a specific blocker visible if it cannot be resolved.

When ready and authorized, merge, deploy, and verify the release without adding a
Forge approval request. Respect the project's standing grants and any restrictions
it still imposes. Preparation, merging, deployment, and enabling a flag may have
different authorization. A request to build does not by itself grant every action.

Feature flags can let code land disabled and should be considered for automated
merges. Check disabled and enabled paths and effects outside the flag, including
migrations, startup, and background jobs. Record the flag's state, owner,
activation prerequisites, and cleanup condition in the project's existing durable
documentation.

Follow [post-launch verification](post-launch.md) on the actual release, using
scripts, live browser proof, and an LLM examination of the launched flow. Report
merged, deployed, enabled, and verified states separately. Missing required proof
leaves verification incomplete. Finish [closeout](closeout.md).
