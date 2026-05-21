# Verification And Review

---

# Vertical Red-Green-Refactor

## Rule

When the task calls for test-first work, add behavior one vertical slice at a time: one failing behavior test, the smallest implementation that passes it, then refactor while green.

## Why It Matters

Writing many tests before any implementation often locks in imagined interfaces and brittle implementation details. A vertical cycle lets each test respond to what the previous slice taught you.

## How To Apply It

For each behavior:

1. Write one test that verifies observable behavior through a public interface.
2. Run it and confirm it fails for the expected reason.
3. Implement only enough code to pass that test.
4. Run the test and the nearest relevant checks.
5. Refactor only after the test is green.
6. Repeat with the next behavior.

Prefer integration-style tests that exercise real code paths. Avoid tests that mock internal collaborators, inspect private details, or fail when implementation changes but behavior does not.

## Common Failure Modes

- Writing all tests first, then all implementation.
- Testing data shape or function names instead of user-visible behavior.
- Refactoring while tests are red.
- Adding speculative behavior for future tests.

## Practical Test

Can you name the single behavior the current test proves, and would that test survive an internal refactor?

---

# Adversarial Verification

## Rule

Verification is not the act of confirming that the happy path works. Verification is the act of trying to break the change and proving, with command output, that it still behaves correctly.

## Why It Matters

A passing unit test suite does not prove that a feature works end to end. Many defects live in edge cases, bad inputs, missing wiring, or regressions outside the main path.

## Core Method

- Build the project when applicable.
- Run the project's tests and linters.
- Reproduce the original bug if the task was a fix.
- Exercise the changed behavior directly.
- Run at least one adversarial probe, such as boundary input, duplicate requests, invalid IDs, or concurrency.
- Record the exact command and the observed output.

## Common Failure Modes

- Reading code and calling that verification.
- Accepting a polished UI or a green test suite as proof.
- Reporting PASS without evidence that can be rerun.

## Practical Test

A verification report is weak if it contains explanations but no commands. If the evidence cannot be rerun, it is not strong enough.

---

# Verification Planning

## Rule

Turn verification into an explicit plan before running it. Map changed files to the right verification method, define setup and cleanup steps, and state exact pass or fail criteria.

## Why It Matters

Unplanned verification drifts into vague checking. A written plan creates determinism, makes delegation possible, and prevents silent gaps.

## How To Apply It

- Identify what changed.
- Choose the correct verifier for each change type.
- Write setup steps with commands and readiness signals.
- List verification steps with expected outcomes.
- Stop on the first real failure instead of averaging results.

## Good Verification Plan Elements

- Files being verified.
- Preconditions.
- Setup commands.
- Ordered verification steps.
- Cleanup steps.
- Success criteria.
- Reporting format.

## Practical Test

A second engineer should be able to execute your plan exactly as written and reach the same verdict.

---

# Simplify Review

## Rule

After implementing a change, review the diff for three things: missed reuse, quality problems, and efficiency problems. Clean up what you find before calling the work done.

## Why It Matters

The first correct implementation is often not the best maintainable implementation. A focused simplification pass catches duplication, awkward APIs, and unnecessary work while the change is still fresh.

## Review Angles

### Reuse

Look for existing helpers, utilities, or local patterns that could replace new code.

### Quality

Look for redundant state, parameter sprawl, copy-paste logic, leaky abstractions, stringly-typed code, and comments that explain obvious behavior.

### Efficiency

Look for repeated work, missed concurrency, hot-path bloat, unnecessary existence checks, memory leaks, and overly broad reads.

## Practical Test

If the diff introduces a new helper, a new state field, or a new loop, ask whether an existing construct already covered the same need more simply.
