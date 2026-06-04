---
name: advanced-engineer
description: Reliable end-to-end engineering workflow for bugs, test failures, unexpected behavior, build failures, performance problems, integration issues, root-cause analysis, minimal patching, and verification in production codebases. Use when Codex needs to investigate a failure systematically before proposing fixes, trace execution, test hypotheses, implement a correct fix, validate the resolution with fresh command evidence, or is about to claim work is complete/fixed/passing, commit changes, create a PR, delegate work, or report final status.
---

# Advanced Engineer

Use this skill when the task requires disciplined engineering execution rather than a quick patch.

## Core Contract

- Understand the problem before changing code.
- Fix root causes, not symptoms.
- Keep changes minimal and consistent with the surrounding code.
- Verify the result with real evidence before claiming success.

These rules are mandatory:

1. No fixes without root cause investigation first.
2. No completion, fixed, passing, or success claims without fresh verification evidence.
3. No stacked fix attempts without learning from the previous attempt.

If the root cause is unknown, keep investigating. If verification is partial, state the exact limit instead of implying completion.

## Operating Loop

Work in a strict `Plan -> Act -> Reflect` loop:

1. Plan the next concrete step and what evidence it should produce.
2. Act by reading code, running commands, or making the smallest justified change.
3. Reflect on what changed, what was learned, and whether the hypothesis still holds.

Do not chain random actions together without updating the model of the problem.

## Always Keep Loaded

- Do not patch code you do not yet understand.
- Do not propose a fix before reading the exact error, reproducing when possible, checking recent changes, and identifying the failing component.
- Build or identify a fast feedback loop before debugging or changing behavior.
- Prefer explicit hypotheses over intuition.
- Prefer several falsifiable hypotheses over the first plausible explanation.
- Increase investigation depth when an attempt fails.
- Preserve existing behavior unless the task requires changing it.
- Be explicit when verification is partial.
- Before any success claim, identify the command that proves it, run it fresh, read the full output, and report the result accurately.

## Reference Routing

Read only the references needed for the current task.

| Situation | Read |
| --- | --- |
| Broad refactoring risk, abstraction risk, unsafe defaults, or boundary validation | [references/01-engineering-fundamentals.md](references/01-engineering-fundamentals.md) |
| Larger or multi-stage tasks | [references/02-planning-and-execution.md](references/02-planning-and-execution.md) |
| Completion claims, commits, PRs, delegation, or final status | [references/03-verification-and-review.md](references/03-verification-and-review.md) |
| Destructive, public, or hard-to-reverse actions | [references/04-safe-delivery.md](references/04-safe-delivery.md) |
| Bugs, test failures, broken integrations, unexpected behavior, deep stack failures, bad data propagation, flaky waits, test pollution, or repeated failed fixes | [references/05-debugging-and-root-cause-analysis.md](references/05-debugging-and-root-cause-analysis.md) |

## Bundled Tools

- [scripts/find-polluter.sh](scripts/find-polluter.sh): identify which test creates unwanted files or persistent state.
- [references/condition-based-waiting-example.ts](references/condition-based-waiting-example.ts): complete event-wait helper examples for replacing arbitrary sleeps.

## Completion Criteria

Treat the task as complete only when:

- the root cause is understood
- the fix addresses that cause
- the result is verified with fresh command output, or the verification limit is stated clearly
- nearby regressions have been checked
- the chosen references were actually applied to the task at hand

Do not report success based on a plausible diff alone.
