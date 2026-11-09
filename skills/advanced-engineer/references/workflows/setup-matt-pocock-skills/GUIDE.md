# Project engineering setup

Configure only the project conventions needed for the requested tracker or domain workflow. This mode is optional; ordinary implementation, planning, and review can proceed without it.

1. Inspect existing repository instructions, remote, tracker configuration, glossary/ADR layout, and `.scratch/` conventions. Reuse decisions already recorded. Respect directory access exclusions.
2. If tracker operations are requested and the tracker is unknown, determine whether GitHub, GitLab, local Markdown, or another configured tracker is intended. Clarify only decisions that cannot be inferred. Use the matching template below; do not assume a remote requires its issue tracker.
3. If issue triage is requested, reuse existing role-to-label mappings or propose the five roles (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). Configure these only for projects using triage. The procedure is built into advanced-engineer; no separate skill installation is required.
4. Use a single root `GLOSSARY.md` and `docs/adr/` unless existing project boundaries justify a multi-context `GLOSSARY-MAP.md`. Domain artifacts are created as actual terms and decisions emerge, not as empty scaffolding.
5. Prepare concrete configuration in `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, and, when needed, `docs/agents/triage-labels.md`. Update the existing `AGENTS.md` or `CLAUDE.md` with concise pointers if this is part of the authorized setup; preserve unrelated content. State that the software procedures live in advanced-engineer, not separate commands.
6. Apply authorized local changes. External label creation or tracker mutations require task authorization. Report what was configured and any missing access.

## Seed templates

- [GitHub](issue-tracker-github.md)
- [GitLab](issue-tracker-gitlab.md)
- [Local Markdown](issue-tracker-local.md)
- [Triage roles](triage-labels.md)
- [Domain documents](domain.md)

Templates describe tracker operations; their examples do not authorize publishing, comments, pushes, or release-state changes.
