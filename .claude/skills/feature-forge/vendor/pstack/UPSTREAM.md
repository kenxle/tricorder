# pstack source record

The principle directories, technical-writing, unslop, no-comments, and Comment
Sicko are copies from Lauren Tan's pstack in the
[Cursor plugins repository](https://github.com/cursor/plugins/tree/6b78e9f4e46c75d1697d837e51f07c2692e60b24/pstack/skills),
at revision `6b78e9f4e46c75d1697d837e51f07c2692e60b24`. Their original location is
`pstack/skills/` and `pstack/agents/comment-sicko.md`. The [MIT license](LICENSE)
accompanies the copies.

The only integration change redirects Explain the Number's relative
benchmark-checklist link to the pinned upstream file. The checklist remains
outside this package. All other vendored source content is unchanged.

Feature Forge loads principles through the [index](../../references/principles.md)
and prose through the [writing guidance](../../references/writing.md). The
[comment adapter](../../references/comment-review.md) maps host-specific calls
without modifying Comment Sicko. The full plugin, orchestrator, how/why workflows,
architect, arena, and host configuration are not dependencies.

To update, compare these directories and the license with the chosen upstream
revision. Review the actual diff, preserve local integration guidance, and verify
the package before committing the accepted update and changing this revision.
Do not silently replace installed consumer copies. No scheduled update service is
included; consumers receive changes through the usual compare-and-copy process.
