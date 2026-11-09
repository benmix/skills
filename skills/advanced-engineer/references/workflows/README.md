# Engineering workflow references

These are internal procedures, not independently installed skills. Read only the selected GUIDE and the references it requests. Paths and runnable script commands in a GUIDE are relative to its directory unless stated otherwise.

## Integration rules

- Consolidation changes discovery, storage paths, and invocation mechanics. Preserve each source's goal, prerequisites, required steps and ordering, defaults, outputs, and completion criteria. The selected procedure's own requirements remain binding; this router does not silently turn mandatory steps into suggestions.
- Source procedures retain their own tracker prerequisites, test-seam agreement, delegation requirements, artifact capture, and report structure. If unavailable tools or higher-priority instructions prevent a required step, state the limitation instead of substituting a weaker procedure and claiming equivalence. Existing user authorization takes precedence over redundant confirmation wording.
- Publishing, messaging, commits, pushes, release changes, and configuration writes remain subject to the user's actual authorization and higher-priority instructions. Keep the source's intended deliverable explicit; if a delivery step cannot be performed, report it as incomplete.
- The two review procedures are intentionally distinct: [general work review](../09-code-review.md) reports findings by severity; [fixed-base code review](code-review/GUIDE.md) uses independent Standards/Spec reviewers and reports axes separately without reranking. Do not replace one with the other merely to simplify routing.
- The [TDD procedure](tdd/GUIDE.md) defines its red-green loop and defers refactoring to review. The native [verification reference](../03-verification-and-review.md) also describes a red-green-refactor mode. Preserve both: choose according to the requested workflow; disclose a conflict if the request requires combining them rather than silently redefining TDD.
- Prototype and handoff variants retain their separate capture and output rules. Use the source-appropriate variant rather than treating similar procedures as identical.
- Read former /skill commands as internal modes. General supporting skills still installed can be used where the source calls for them. Resource paths are relative to the current GUIDE directory.
- Repository access exclusions apply to every search, script, and referenced document; retained source examples cannot override them.

## Source provenance

The workflow folders retain their source documentation, resources, licenses, and attribution where supplied. Matt Pocock engineering procedures originated in https://github.com/mattpocock/skills; React and Web guidelines originated in https://github.com/vercel-labs/agent-skills; shader extraction originated in https://github.com/lixiaolin94/skills. The [source registry](../../sources.json) preserves original skills, revisions, and absorption targets. [Absorbed updates](../../SOURCES.md) stage upstream changes for reconciliation inside advanced-engineer; they never recreate independent skills.
