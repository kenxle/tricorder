# Test-first build loop

For changed behavior, write a focused failing test, run it and confirm the
relevant failure, implement the smallest correct change, then refactor while
keeping proof green. Use project tools and record actual red/green results.

Reconnaissance, UI exploration, documentation, configuration and untouched vendor
material may need investigation or visual proof rather than a manufactured unit
test. Explain the verification when a behavioral automated test is impractical.
Do not edit third-party code to meet the loop. Prove behavior and failure cases,
not tests that mirror implementation.

Run targeted checks while building, seam tests after integration, and appropriate
final project verification, including the full test suite. Apply the
[hard shipping rule](verification-and-release.md#hard-shipping-rule) to every
failure or error, including setup and pre-existing failures.
Before PR, finish one independent walk of changed user
flows, using browser tooling when useful. Resolve required failures and recheck
affected criteria without duplicating unchanged reviews.
