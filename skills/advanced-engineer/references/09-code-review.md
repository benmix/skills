# Code Review

The review procedure for advanced-engineer standalone reviews and implementation self-review. Findings come first.

## Choose the Review Mode

- **Requested review:** inspect and report. Change code only if the user also asks for fixes.
- **Implementation self-review:** before finishing substantive implementation or a bug fix, apply the same checks to your changes. Correct issues within the already authorized scope, then verify the correction. A separate review report is optional unless requested.

Keep design/UX audits and prose-only reviews with their specialist workflows. For skill-file changes, review instruction behavior and discovery metadata as the implementation and use the skill request as the spec.

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

1. Pin the scope and comparison before reviewing:
   - With no supplied base, inspect staged, unstaged, and relevant untracked files in the current working tree (`git diff --cached`, `git diff`, and `git status --short`). Read untracked files explicitly; they are absent from the diff. If the tree is clean, use an evident PR/branch context or ask for the intended scope.
   - For a branch or PR, use its target's merge base (`git diff <target>...HEAD`). For an exact commit/tag snapshot, use `git diff <ref> HEAD`; for a single commit use `git show <commit>`. Honor an explicitly requested range. Resolve supplied refs before use, and state whether local edits are included.
   - An empty comparison means no changes in that scope; report it without silently choosing another base.
2. Read the diff, surrounding code, and applicable repository instructions and standards, including `CONTRIBUTING.md` and `CODING_STANDARDS.md` where present. Respect any directory access exclusions.
3. Find the spec in the user request/conversation, supplied artifact, linked issue/PR, or matching repository plan. Use available authorized tools for external context; an issue tracker setup is not a prerequisite. If no spec exists, state the inferred intent and limits; ask only when missing requirements prevent a meaningful review.
4. Review **Standards** and **Spec** as separate checks using the axes above. For maintainability, look for duplication, misleading names, scattered changes, hidden state, caller coordination, and speculative abstractions. Treat these as heuristics: report concrete consequences and respect documented repository choices.
5. Trace candidate findings to reachable behavior and use focused checks where useful. For a large review, independent reviewers may split the axes when delegation is available and authorized. Both receive the same pinned scope and applicable standards/spec; the lead validates and deduplicates their findings. A solo review uses the same two checks.
6. Report actionable findings by severity, label each **Standards**, **Spec**, or both, and include file/line references, trigger, consequence, and supporting evidence. Include open questions and verification gaps.

## Trace Safety Beyond the Diff

For changes to shared interfaces, asynchronous lifetimes, persisted formats, or other high-risk boundaries, identify the key facts the change's safety depends on. Follow relevant timing, teardown, serialization, cross-language consumers, and the actual dependency version or local patch; a caller search alone may miss them.

Use the smallest safe executable check to test those facts against real code. Use temporary harnesses when appropriate; do not change product code, mutate live data, or expand external actions to obtain proof. If the environment cannot support the check, report the fact as unverified. Distinguish source reasoning, an executable probe, and real application evidence.

## Judge Findings Against Actual Behavior

Trace a finding from a reachable trigger to a concrete consequence. Check boundary guarantees and surrounding code before accepting hypothetical inputs. Prioritize correctness and security even when only one reviewer raises them; reviewer agreement is a signal, not proof.

Filter preferences, arbitrary file-size thresholds, and abstraction requests without concrete benefit. For structural findings, explain the extra layers, hidden state, or caller coordination introduced and how they affect maintenance. Keep relevant unresolved risk as a verification gap instead of inventing a defect.

## Output

Use this order:

1. Findings, ordered by severity, with the review axis identified for each.
2. Open questions or assumptions.
3. Verification gaps.
4. Short summary only after findings.

If no findings are found, say that explicitly and still mention residual risk or missing verification.

## Severity

- `High` - likely bug, data loss, security issue, failing requirement, or serious regression.
- `Medium` - maintainability, edge-case, test, or behavioral risk that should be addressed.
- `Low` - minor cleanup, clarity, or consistency issue.

Do not pad the review. If something is not actionable, leave it out.

The safety and finding-judgment guidance is adapted from Lauren Tan's pstack blast-radius and interrogate practices.
