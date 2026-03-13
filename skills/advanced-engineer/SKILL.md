---
name: advanced-engineer
description: Reliable end-to-end engineering workflow for debugging, root-cause analysis, minimal patching, and verification in production codebases. Use when Codex needs to investigate a failure systematically, trace execution, test hypotheses, implement a correct fix, validate the resolution, and check for regressions before declaring the task complete.
---

# Advanced Engineer

Guide work with a strict Plan -> Act -> Reflect loop. Treat a task as complete only when the system works correctly in practice, not when a patch merely looks plausible.

## Mission

- Understand the problem before changing code.
- Identify the root cause, not just the visible symptom.
- Implement the smallest correct fix that preserves surrounding behavior.
- Verify the fix end to end and check for regressions.

## Execution Loop

Repeat this loop until the issue is resolved:

1. Plan
2. Act
3. Reflect

### Plan

Before acting, define:

- The problem currently under investigation
- The next action to take
- What information that action should reveal
- How success will be measured

Prefer short, concrete plans such as:

- Inspect the stack trace
- Locate the failing function
- Read the surrounding implementation

### Act

Execute the planned step. Typical actions include:

- Read repository files
- Search the codebase
- Inspect logs and runtime output
- Run commands
- Check configuration and dependency versions
- Implement code changes
- Create or run tests

Only this step should change system state.

### Reflect

After each action, determine:

- What new information was discovered
- Whether expectations were met
- Which assumptions were confirmed or invalidated
- What the next step should be

Do not chain random actions together without reflection.

## Investigation Before Modification

Before implementing a fix:

- Reproduce the failure when possible
- Read the exact error message and stack trace
- Locate the failing code and surrounding implementation
- Understand the execution path that leads to the failure

Do not patch code you do not yet understand.

## Root Cause First

Prefer fixes that correct the mechanism causing the failure. Before patching, answer:

- What exactly caused the failure?
- Which assumption was violated?
- Which component produced the incorrect behavior?

If a change only suppresses symptoms, keep investigating.

## Hypothesis-Driven Debugging

Debug with explicit hypotheses:

1. Observe evidence from stack traces, logs, runtime output, configuration, and dependency versions.
2. Generate multiple plausible explanations.
3. Design a validation step for each explanation.
4. Use the evidence to eliminate incorrect hypotheses.

Example:

- H1: A dependency is missing -> inspect installed packages
- H2: A version is incompatible -> compare actual versions and compatibility constraints
- H3: An import path is wrong -> search project imports and resolution paths
- H4: The environment is misconfigured -> inspect env vars and config files

## Iteration and Escalation

When an attempt fails:

- Analyze why it failed
- Identify the broken assumption
- Choose a meaningfully different next strategy

Do not repeat the same fix with minor variations.

Increase investigation depth as attempts fail:

- After first failure: re-read errors, code, and assumptions
- After second failure: search exact error text and check documentation
- After third failure: trace execution flow and instrument code if needed
- After fourth failure: create a minimal reproduction and isolate components
- After fifth failure: reconsider architecture, framing, and constraints

## Patch Principles

When implementing a fix:

- Minimize scope
- Preserve readability
- Follow repository conventions
- Preserve existing functionality unless the requirement says otherwise

Avoid speculative large refactors unless the root cause demands them.

## Verification Pipeline

Every patch should pass this pipeline:

1. Reproduce the failure
2. Apply the patch
3. Confirm the original failure is resolved
4. Run sanity or regression checks
5. Inspect nearby code paths for related issues

Without reproducing the issue, be explicit that verification is partial.

Examples of sanity checks:

- Relevant tests pass
- The affected command or page works end to end
- No new errors appear in adjacent flows

If the same bug pattern exists elsewhere, fix those locations too when the scope is clear and safe.

## Verify Assumptions

Do not rely on unchecked assumptions when verification is possible. Common sources of failure include:

- Dependency versions
- Environment configuration
- API behavior
- File paths
- Permissions
- Environment variables

## Tool-First Investigation

Gather evidence with available tools before asking the user. Prefer to:

- Search the repository
- Inspect stack traces and logs
- Read configuration
- Check documentation or dependency state

Ask the user only after reasonable investigation.

## Ask the User When Needed

Request clarification when:

- Credentials, secrets, or external data are missing
- Domain knowledge is unavailable in the repository
- Multiple product decisions are viable
- The issue cannot be reproduced locally

When asking, include:

- What was tried
- What evidence was collected
- The specific missing information

## Completion Criteria

Treat the task as complete only when:

- The root cause is understood
- The fix addresses that root cause
- The issue is reproducibly resolved, or the verification limit is stated clearly
- The fix has been validated
- No obvious regressions remain

Take ownership of the full outcome: fix the bug, validate the result, and confirm the change integrates cleanly with the surrounding system.
