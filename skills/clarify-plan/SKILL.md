---
name: clarify-plan
description: Clarify an ambiguous plan, design, or implementation direction before execution by asking focused questions with recommended answers. Use when the user asks to stress-test a plan, wants to be grilled, is unsure about scope or tradeoffs, or describes a high-cost change with unresolved decisions.
---

# Clarify Plan

Use this skill to resolve expensive ambiguity before implementation.

## When To Use

Use for:

- product or architecture choices
- large refactors
- domain-heavy requirements
- unclear success criteria
- multiple plausible implementation directions
- requests to "grill me", "stress-test this", or "help me think it through"

Do not use for small edits, clear specs, simple commands, or bugs where code exploration should happen first.

## Loop

Ask one question at a time.

For each question:

1. State why the answer matters.
2. Give your recommended answer.
3. Offer 2-3 concrete options when useful.
4. Wait for the user's answer before continuing.

If the answer can be found by reading the codebase, inspect the code instead of asking.

## Limits

Default to 3-5 questions. Continue only when:

- the user asks to go deeper
- a previous answer exposes a new high-impact decision
- proceeding would likely cause significant rework

## Output

When enough decisions are resolved, summarize:

- decisions made
- non-goals
- remaining assumptions
- success criteria
- recommended execution plan

Keep the summary short enough to become a working brief.
