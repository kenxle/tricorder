# Verify the actual release

Automate post-launch proof as far as the project permits. Use its repeatable
health, migration, monitoring, and smoke commands. Use Playwright for a live
browser journey. Use the appropriate real interface for a non-browser product.
These observations complement pre-release verification, not replace it.

Record the environment and actual deployed revision. Check applicable release
conditions and link evidence from the Plan's verification table:

- Health and required migrations completed on the deployed services.
- The changed feature or bug-fix flow works on the live release with appropriate
  accounts and data. Cover important failure states and integration boundaries.
- Logs and monitoring show no new release-related errors. Compare performance
  and resource use with an identified baseline rather than guessing a threshold.
- Flag state matches the release decision. Check effects outside the flag and
  activation prerequisites as well as disabled and enabled behavior.
- Recovery remains available. Check the project's rollback or recovery procedure
  and its prerequisites without causing an unauthorized production disruption.

Have an LLM examine the actual launched flow using browser interaction and
captured evidence. Assign that review to the existing acceptance owner when
appropriate. Give it the intended behavior and observed output, not just a
builder's success summary. Record concrete findings and limits. Screenshots
alone cannot prove effects such as a saved record or a completed job.

Preserve script output, browser traces or captures, monitoring observations, and
the LLM's findings in the release record. Mark each required check pass, fail, or
unverified. Missing access, revision identity, or required proof leaves release
verification incomplete. Keep the blocker visible and follow through. Fix and
recheck, or use an authorized recovery path when needed. Do not add a routine
human approval gate or claim that landing proves deployment.

Report merged, deployed, enabled, and verified states separately. A package with
no deployed runtime records that limit rather than inventing production proof.
Then follow [closeout](closeout.md).
