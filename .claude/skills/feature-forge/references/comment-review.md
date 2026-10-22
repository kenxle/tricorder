# Scoped comment review

Use when comment quality is relevant to the task or explicitly requested. The
vendored [no-comments source](../vendor/pstack/skills/no-comments/SKILL.md)
informs this adapter. It is not a mandatory extra review of every change.

Delegate the unchanged [Comment Sicko prompt](../vendor/pstack/agents/comment-sicko.md)
with the actual files or diff, the [principles index](principles.md), and the
project's scope and authority. Use the host's supported delegation API and a
suitable model. The prompt is bundled for dispatch; the installer does not
register a named host agent or install slash commands.

Provide these local equivalents for the prompt's investigation requests:

- `how`: inspect the relevant symbol, callers, dependency contract, and observed
  behavior to test a claimed constraint. Run a focused check when the claim
  depends on runtime behavior.
- `why`: inspect version history and available linked decisions for the reason
  the code exists. Distinguish evidence from inference and name missing evidence.

These are narrow supporting investigations for Comment Sicko. The general pstack
how/why workflows and their host-specific model or tool setup are not imported.
The adapter supplies the equivalents in the task contract without rewriting the
original agent prompt.

Inspect the returned evidence and scoped diff before accepting findings. Reject
application-code edits by the comment reviewer, scope escapes, or deletions that
violate the prompt's exceptions. The implementation owner makes accepted code
changes and verifies them. Use Forge's existing architecture guidance if a
structural fix needs design; no external architect or arena skill is required.

Keep unresolved constraints visible. Do not report comment removal as completion
of a refactor the reviewer merely identified. Use the same independent acceptance
and release rules as the rest of the work.
