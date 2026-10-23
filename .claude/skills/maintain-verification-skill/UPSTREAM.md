# Source

This skill is a copy of Lauren Tan's pstack skill of the same name, from the
[Cursor plugins repository](https://github.com/cursor/plugins/tree/6b78e9f4e46c75d1697d837e51f07c2692e60b24/pstack/skills),
at revision `6b78e9f4e46c75d1697d837e51f07c2692e60b24`. That is the revision
Feature Forge pins for its other pstack copies. The files are unchanged. The
[MIT license](LICENSE) comes with them.

## Using it in Tricorder

- Upstream writes the generated skill under `.cursor/skills/`. In this repo it
  goes in `.claude/skills/verify-tricorder/`, so Claude Code finds it.
- The skill sets `disable-model-invocation: true`, so it runs when someone types
  its slash command. A Feature Forge agent may also read this file and follow it
  as written.
- To update, compare this folder with a newer upstream revision, review the
  diff, then copy and change the revision above.
