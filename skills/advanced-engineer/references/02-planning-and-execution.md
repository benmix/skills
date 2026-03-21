# Planning And Execution

---

# Iterative Planning

## Rule

When the task needs planning, explore the code, update the plan as you learn, and ask the user only for decisions that cannot be resolved by reading the code.

## Why It Matters

Good plans are built from evidence, not from guesses. An iterative plan stays grounded in the real codebase and converges toward a concrete execution path.

## How To Apply It

- Start with a quick scan of the key files.
- Write a rough plan early instead of waiting for perfect understanding.
- Update the plan after each useful discovery.
- Ask the user about requirements, priorities, and tradeoffs, not facts already present in the code.
- Include a verification section in the plan.

## What A Good Plan Contains

- The context for the change.
- The files that matter.
- Existing code to reuse.
- The recommended approach.
- How the result will be verified.

## Practical Test

If your plan cannot name the files to change or the way to verify the result, it is not ready.

---

# Parallel Work Orchestration

## Rule

For large, parallelizable changes, decompose the work into independent units that can be implemented, verified, and merged without depending on one another.

## Why It Matters

Large migrations fail when the work is split arbitrarily. Good decomposition reduces merge conflicts, allows parallel execution, and keeps each reviewable unit coherent.

## How To Apply It

- Research the full scope before splitting the work.
- Slice by module, directory, or independent behavior, not by random file count.
- Keep units roughly uniform in size.
- Define an end-to-end verification recipe before assigning the work.
- Give each worker a self-contained prompt with scope, conventions, and test steps.

## Common Failure Mode

A large change is split into overlapping pieces. Workers then touch the same files, depend on each other's branches, and block the whole migration.

## Practical Test

Ask whether one unit can land on its own without another unit landing first. If not, the split is wrong.

---

# Worker Completion Protocol

## Rule

A worker's job is not finished when the code compiles. After implementation, it should run a predictable completion sequence: simplify the diff, run unit tests, run end-to-end checks, prepare the branch, and report the outcome clearly.

## Why It Matters

Multi-agent or multi-engineer workflows break down when every worker uses a different definition of done. A fixed completion protocol makes outcomes easier to trust.

## Recommended Sequence

1. Review and simplify the change.
2. Run unit tests.
3. Run end-to-end checks for the affected flow.
4. Commit and push only when that action is part of the assignment.
5. End with a machine-readable result or handoff line.

## Common Failure Mode

A worker finishes the code path, skips verification, and reports success based on static reading or a partial local check.

## Practical Test

If another coordinator cannot tell whether the change was simplified, tested, and handed off correctly, the reporting step is too weak.
