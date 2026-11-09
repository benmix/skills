# Engineering workflow references

These are internal procedures, not independently installed skills. Read only the selected GUIDE and the references it requests. Paths and runnable script commands in a GUIDE are relative to its directory unless stated otherwise.

## Integration rules

- The user request and advanced-engineer mode determine the deliverable. Planning, research, architecture surveys, reviews, handoffs, and retrospectives do not implicitly authorize implementation.
- Tracker setup is optional. Reuse existing configuration; read the setup procedure only when tracker operations need configuration. Without a tracker, draft a local result or report the missing access. Do not block unrelated engineering on setup.
- Prepare specs, tickets, PRs, and tracker changes locally before external writes. Publish, send comments, close issues, commit, push, or change release state only within the actual task authorization. Reading a procedure is not authorization for these operations.
- Use a solo execution by default. Optional multi-agent patterns apply only when delegation is available and authorized; a procedure does not require parallelism for an otherwise sequential task. Preserve another agent's or the user's work when changing worktrees.
- For prototypes, follow the requested artifact and existing project layout. Commit, branch, push, or issue-link capture only when authorized; otherwise preserve the artifact locally and report its location.
- Tests should verify meaningful behavior. Use TDD when requested or appropriate to the risk; a tiny reversible change does not need a new test suite. The refactoring ban in the imported TDD guide applies to mixing structure changes into a red test; a verified green refactoring step remains valid.
- Repository access exclusions apply to every search, script, and referenced document. A retained source example never overrides those exclusions.
- Former /skill commands in imported prose name modes of advanced-engineer. Read the corresponding internal GUIDE instead of invoking or installing the removed skill. If a requested mode refers to a general supporting skill still installed, use it only when relevant.

## Source provenance

The workflow folders retain their source documentation, resources, licenses, and attribution where supplied. Matt Pocock engineering procedures originated in https://github.com/mattpocock/skills; React and Web guidelines originated in https://github.com/vercel-labs/agent-skills; shader extraction originated in https://github.com/lixiaolin94/skills. The [source registry](../../sources.json) preserves original skills, revisions, and absorption targets. [Absorbed updates](../../SOURCES.md) stage upstream changes for reconciliation inside advanced-engineer; they never recreate independent skills.
