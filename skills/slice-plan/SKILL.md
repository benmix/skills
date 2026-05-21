---
name: slice-plan
description: Break a plan, PRD, feature idea, or implementation proposal into independently executable vertical slices. Use when the user wants to split work into tasks, create an implementation breakdown, prepare work for agents, identify dependencies, or turn a broad plan into AFK/HITL steps without automatically creating issues.
---

# Slice Plan

Use this skill to turn broad work into thin, independently verifiable slices.

## Core Rule

Prefer vertical slices over horizontal layers.

A good slice delivers a narrow but complete path through the system. It should be demoable, testable, or otherwise verifiable on its own.

Avoid slices like:

- "create database schema"
- "build API"
- "build UI"
- "write tests"

Prefer slices like:

- "user can create one draft item end to end"
- "admin can approve one pending request with audit trail"
- "CLI can parse one valid config and report one validation error"

## Process

1. Read the plan, spec, conversation, or issue.
2. Identify the user-visible or operator-visible outcomes.
3. Break the work into the smallest end-to-end slices that still prove meaningful behavior.
4. Mark each slice as `AFK` or `HITL`.
5. Identify dependencies between slices.
6. Write acceptance criteria for each slice.
7. Ask the user to confirm granularity before publishing or implementing anything.

## AFK And HITL

Use `AFK` when an agent can complete the slice without more human judgment.

Use `HITL` when the slice needs:

- product judgment
- design approval
- policy or legal choice
- credentials or external access
- manual validation that cannot be automated yet

Prefer making slices AFK by shrinking scope or clarifying acceptance criteria.

## Output Format

Return a numbered list:

1. `Title` - short outcome-focused title.
2. `Type` - `AFK` or `HITL`.
3. `Depends on` - prior slice numbers or `None`.
4. `What it proves` - the complete path this slice validates.
5. `Acceptance criteria` - concrete checks.

End with any open questions that block slicing further.

Do not create GitHub issues, Linear tickets, files, or commits unless the user explicitly asks.
