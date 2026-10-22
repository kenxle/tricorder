# Local additions to the engineering principles

These additions complement the selected upstream leaves. Keep vendored originals
unchanged. Load the upstream principle where it already covers the decision.

- **Remove repeated knowledge.** Repeated facts or rules create multiple places
  to update. Derive from an authoritative source or give the knowledge one owner.
  Similar-looking code is not automatically the same knowledge. Avoid a generic
  abstraction that increases reader effort. Pair this with
  [minimize reader load](../vendor/pstack/skills/principle-minimize-reader-load/SKILL.md).
- **Repair broken tools.** When a tool loses a supported document convention or
  cannot perform its intended job, find the failure and fix or report it at the
  owning boundary. Do not silently weaken the artifact to make the tool pass.
  Preserve the user's content. Use
  [fix root causes](../vendor/pstack/skills/principle-fix-root-causes/SKILL.md)
  for the investigation.
- **Use cheap checks early.** Run fast, relevant checks while iterating so defects
  surface before expensive integration or browser runs. Then run required
  integrated verification and the full suite before shipping. Check ordering
  saves wasted work, not required proof. Follow the
  [test-first loop](build-loop.md).
- **Turn lessons into mechanisms.** Capture a surprise with evidence and a
  concrete prevention. Prefer a type, lint, fixture, generator, or script when
  it can encode the rule reliably. Otherwise put concise guidance at its owning
  source. Link the
  [encode-lessons principle](../vendor/pstack/skills/principle-encode-lessons-in-structure/SKILL.md)
  and [closeout](closeout.md) rather than accumulating duplicate instructions.

Keep the upstream
[behavioral-test principle](../vendor/pstack/skills/principle-test-behavior-not-implementation/SKILL.md).
Judge what a test proves instead of banning assertions by their shape.
