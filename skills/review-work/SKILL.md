---
name: review-work
description: "Review local changes, branches, PRs, or completed agent work along two axes: code standards and spec compliance. Use when the user asks to review work, review since a commit or branch, check whether implementation matches requirements, or assess whether a change is ready to ship."
---

# Review Work

Use this skill for review, not implementation. Findings come first.

## Review Axes

### Standards

Check whether the work fits the repository:

- local patterns and architecture
- naming and API design
- error handling
- tests and verification
- maintainability
- performance and security where relevant
- unnecessary churn or abstraction

### Spec

Check whether the work satisfies the originating request, issue, PRD, or conversation:

- required behavior is present
- non-goals are respected
- edge cases from the spec are handled
- acceptance criteria can be verified
- no unrelated behavior changed

If no spec artifact exists, reconstruct the intended spec from the conversation and state that assumption.

## Process

1. Identify the review base: user-provided commit/branch, merge base, or current working tree.
2. Read the diff and the surrounding code needed to understand it.
3. Find the relevant spec, issue, plan, or user request if available.
4. Review Standards and Spec separately.
5. Report findings ordered by severity, with file and line references when possible.
6. Include open questions and verification gaps.

Do not fix issues during the review unless the user explicitly asks.

## Output

Use this order:

1. Findings, ordered by severity.
2. Open questions or assumptions.
3. Verification gaps.
4. Short summary only after findings.

If no findings are found, say that explicitly and still mention residual risk or missing verification.

## Severity

- `High` - likely bug, data loss, security issue, failing requirement, or serious regression.
- `Medium` - maintainability, edge-case, test, or behavioral risk that should be addressed.
- `Low` - minor cleanup, clarity, or consistency issue.

Do not pad the review. If something is not actionable, leave it out.
