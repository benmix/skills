---
name: handoff
description: Create a concise handoff document so another agent or future session can continue the current work. Use when the conversation is long, context is getting full, work is paused, ownership is changing, or the user asks for a handoff, summary, continuation note, or next-agent brief.
argument-hint: "What should the next session focus on?"
---

# Handoff

Write a handoff document for a fresh agent or future session. Save it outside the repository, using the OS temp directory.

## Include

- Current goal and user intent.
- Repository path and relevant branch state.
- What changed so far, with file paths or commit hashes.
- Important decisions and constraints.
- Commands already run and their outcomes.
- Open questions, blockers, and risks.
- Next recommended steps in order.
- Suggested skills for the next session.

## Avoid

- Duplicating full diffs, plans, PRDs, issues, or ADRs that already exist.
- Copying secrets, tokens, credentials, or personal data.
- Writing the handoff into the workspace unless the user explicitly asks.

## Process

1. Inspect current git status and recent context if needed.
2. Reference durable artifacts by path, commit, or URL instead of pasting them.
3. Redact sensitive information.
4. Save the file to `$TMPDIR` when set, otherwise `/tmp`.
5. Report the absolute path and the most important next step.

If the user provides a focus argument, tailor the handoff around that next session.
