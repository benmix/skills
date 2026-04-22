---
name: anti-repo-skill
description: Opt-out guardrail that prevents the agent from using repository-local skills unless the user explicitly requests a named skill. Use when the user says not to use repo skills, wants plain default behavior, or wants all repo skills to be opt-in only.
---

# Anti Repo Skill

Use this skill when the user wants work to proceed without automatically activating repository-local skills.

## Scope

For this skill, "repo skill" means skills that come from this repository or its installed local copies, such as skills under `skills/` in the repo and matching installs under `~/.agents/skills`.

This skill does not override:

- system or platform instructions
- safety constraints
- direct tool use
- ordinary reasoning without a skill

## Default Rule

Treat all repo skills as disabled by default.

Do not use a repo skill unless the user explicitly asks for it by name or clearly says to use repo/local skills.

## Activation Policy

When this skill is active:

1. Ignore normal repo-skill trigger matches.
2. Do the work with general reasoning, tools, and the active conversation instructions.
3. Do not proactively suggest repo skills as shortcuts.
4. If a repo skill seems helpful but was not explicitly requested, proceed without it.
5. If the user later explicitly names one or more repo skills, use only those named skills.

## Ambiguity Handling

If the user intent is unclear, ask one short clarification question instead of activating a repo skill implicitly.

Examples of explicit requests:

- "use `advanced-engineer`"
- "use the repo skill for refactoring"
- "apply `writing-maestro` to this draft"

Examples that are not explicit requests:

- "debug this"
- "refactor this file"
- "improve the writing"

In those cases, continue without a repo skill.
