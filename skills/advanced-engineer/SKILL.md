---
name: advanced-engineer
description: Reliable end-to-end engineering workflow for debugging, root-cause analysis, minimal patching, and verification in production codebases. Use when Codex needs to investigate a failure systematically, trace execution, test hypotheses, implement a correct fix, validate the resolution, and check for regressions before declaring the task complete.
---

# Advanced Engineer

Use this skill when the task requires disciplined engineering execution rather than a quick patch.

## Mission

- Understand the problem before changing code.
- Fix root causes, not symptoms.
- Keep changes minimal and consistent with the surrounding code.
- Verify the result with real evidence before claiming success.

## Default Loop

Work in a strict `Plan -> Act -> Reflect` loop:

1. Plan the next concrete step and what evidence it should produce.
2. Act by reading code, running commands, or making the smallest justified change.
3. Reflect on what changed, what was learned, and whether the hypothesis still holds.

Do not chain random actions together without updating the model of the problem.

## Start Here

- For bugs, test failures, and broken integrations, start with [references/05-debugging-and-root-cause-analysis.md](references/05-debugging-and-root-cause-analysis.md).
- For larger or multi-stage tasks, read [references/02-planning-and-execution.md](references/02-planning-and-execution.md) before splitting the work.
- Before declaring success, read [references/03-verification-and-review.md](references/03-verification-and-review.md).
- If the change risks broad refactoring, abstraction creep, or unsafe defaults, read [references/01-engineering-fundamentals.md](references/01-engineering-fundamentals.md).
- If the task involves destructive, public, or hard-to-reverse actions, read [references/04-safe-delivery.md](references/04-safe-delivery.md).

## Keep In SKILL Context

- Do not patch code you do not yet understand.
- Prefer explicit hypotheses over intuition.
- Increase investigation depth when an attempt fails.
- Preserve existing behavior unless the task requires changing it.
- Be explicit when verification is partial.

## Reference Index

Read only the references needed for the current task.

### [references/01-engineering-fundamentals.md](references/01-engineering-fundamentals.md)

Read for:

- change scope discipline
- avoiding over-engineering and premature abstractions
- reading code before editing
- boundary validation and secure-by-default decisions
- what to do when an approach is blocked

### [references/02-planning-and-execution.md](references/02-planning-and-execution.md)

Read for:

- iterative planning
- decomposition for larger tasks
- parallel work or worker orchestration
- completion protocol for delegated work

### [references/03-verification-and-review.md](references/03-verification-and-review.md)

Read for:

- adversarial verification
- writing a verification plan
- review and simplification passes before declaring completion

### [references/04-safe-delivery.md](references/04-safe-delivery.md)

Read for:

- destructive action thresholds
- git safety
- commit, PR, and hook discipline
- when to confirm with the user before taking irreversible actions

### [references/05-debugging-and-root-cause-analysis.md](references/05-debugging-and-root-cause-analysis.md)

Read for:

- `Plan -> Act -> Reflect`
- investigation before modification
- root-cause-first debugging
- hypothesis-driven debugging
- escalation strategy after failed attempts
- verification pipeline and partial-verification rules
- tool-first investigation and when to ask the user

## Completion Criteria

Treat the task as complete only when:

- the root cause is understood
- the fix addresses that cause
- the result is verified, or the verification limit is stated clearly
- nearby regressions have been checked
- the chosen references were actually applied to the task at hand

Do not report success based on a plausible diff alone.
