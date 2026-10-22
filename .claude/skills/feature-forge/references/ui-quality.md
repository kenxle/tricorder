# Verify the finished experience

When the human has reviewed a prototype or styles, use that result and their
feedback as the acceptance baseline. Compare the integrated implementation with
it in the browser. Fix drift in behavior, layout, states, content, and shared
components. Link the baseline and relevant feedback from the Plan.

Do not replace approved aesthetic choices with a later reviewer's preference.
Surface a material new conflict with evidence and a recommendation. Functional,
accessibility, and required verification checks still apply to approved designs.

When no reviewed baseline exists, the agent performs a proportional design
review. Check hierarchy, project tokens and shared components, responsive states,
keyboard and assistive use, loading, empty and error states, brand voice, and
consistency. Feedback reports what actually happened. Do not show success while
an action is still pending or has failed. Motion should clarify the experience
and respect the project's accessibility policy.

Use [review perspectives](reviewers.md) when independent design judgment resolves
a real uncertainty. This does not add a mandatory reviewer chain. Browser proof
and independent acceptance review still establish the actual finished behavior.

## Enforce rules that tools can check

Start with the consuming project's style policy and existing linters. Encode
reliable recurring rules rather than repeating instructions. Examples include
raw values that bypass tokens, prohibited inline styles, drift between documented
tokens and their source, and shared-component use where a check can distinguish
valid code reliably. Keep legitimate exceptions explicit and narrow.

Test checks with both violating and valid fixtures. Run them through the normal
verification command, with hooks when useful. Check their output and exit status.
A linter cannot prove fidelity or a good experience. Keep browser and design
judgment for what automation cannot establish. Apply the
[encode-lessons principle](../vendor/pstack/skills/principle-encode-lessons-in-structure/SKILL.md)
without imposing a new universal style system on consumers.
