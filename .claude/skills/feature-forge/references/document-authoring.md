# Author sources and compose the human document

Keep focused authoritative Markdown sources so an agent can read only what its
work needs. Compose those same sources into the complete human document. Do not
maintain a second, separately edited specification in HTML.

## Source organization

Use the [templates](templates.md) for content. Keep substantial research,
alternatives, resolved questions, and worker detail in linked leaves. Include
the parts the human needs using `<!-- forge-include: parts/context.md -->`.
Paths are relative to the containing file, must stay inside the feature folder,
and cannot cycle. Review siblings compose after their main document.

Give each file one writer while work is concurrent. Contracts name relevant
headings without preventing necessary investigation. Keep the Plan's verification
table authoritative. Do not repeat it in workstream documents or Progress.

## Presentation

Start with a descriptive title and a lede that states the result or purpose.
Keep the top of working documents current, with attention needed or an explicit
empty state. Use meaningful headings and relative links to files the reader may
want to open.

Use the installed review tool's component catalog before writing house component
markup. In Markdown, give HTML components their own blocks and write their
contents as HTML. Use existing panels, choices, tables, figures, and folded
sections where they help the reader. Preserve established conventions, including
older `:::` callouts. Fix rendering tools when they lose supported presentation.

For diagrams, keep Mermaid fences in the source and use a readable direction
such as `flowchart TD`. Supply `accTitle` and `accDescr` where supported. Keep
charts and other figures as portable local assets or inline SVG with useful
descriptions. Do not replace a diagram with a code listing in the human view.

## Build and review

For one simple page, review Markdown directly. For a dossier, run
`scripts/build_feature_docs.py <feature-folder>` from the Feature Forge skill.
Pandoc is required. The build uses a local house style when available, otherwise
reports its plain-style fallback. Mermaid fences require a separately installed
[Mermaid CLI](https://github.com/mermaid-js/mermaid-cli) available as `mmdc`, or an
executable path in `FORGE_MERMAID_CLI`. The build renders SVG locally and embeds
it in HTML. It does not download dependencies or add browser scripts or CDNs.
Missing or broken diagram tooling fails the build with an actionable error.

Serve the real build with its source entry point using the review tool's
multi-source workflow. Edit the authoritative leaf, rebuild, inspect the actual
rendered page, and then reply to feedback. Verify typography, layout, components,
graphs, navigation, and assets. Generated HTML is disposable output, not an
editing surface. Keep review history and the source-to-render relationship intact.
