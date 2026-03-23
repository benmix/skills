---
name: refactoring
description: Use when restructuring existing code without changing observable behavior, especially when a feature or bug fix is hard because the current design is awkward, duplicated, confusing, or risky to modify.
---

# Refactoring

Refactor code in small, behavior-preserving steps so the next change becomes easier, safer, and cheaper.

## When To Use

- You need to improve structure without changing externally observable behavior.
- A feature is hard to add because the current design is awkward.
- A bug fix is blocked by confusing, tangled, or duplicated code.
- You need to understand legacy code before touching it.
- You want a small, safe refactoring plan instead of a vague cleanup pass.

## When Not To Use

- You are intentionally changing product behavior.
- The code is ugly, but you do not need to touch it.
- A rewrite is clearly cheaper and lower risk than incremental restructuring.
- There is no practical way to verify behavior and the risk is unacceptable.

## Core Rules

- Refactoring is structural improvement that preserves observable behavior.
- Refactoring is not rewriting.
- Refactoring is not feature work.
- Wear one hat at a time:
  `Refactor hat` changes structure only.
  `Feature hat` changes behavior only.
- If both are needed, make the design change first, then make the behavioral change.

## Default Loop

1. Clarify the real goal: feature, bug fix, or comprehension.
2. State the smell in one sentence.
3. State the intended improvement in one sentence.
4. Lock down current behavior with tests or the strongest repeatable check available.
5. Choose the smallest refactoring that makes the next change easier.
6. Apply one micro-step.
7. Run checks immediately.
8. Repeat only while improvement is still clear.
9. Stop as soon as the intended change becomes straightforward.

Preferred step order:

1. Rename
2. Extract
3. Move
4. Encapsulate or inline
5. Simplify conditionals
6. Remove dead code

Before implementing the real task, first make the change easy.

Common early moves:

- rename unclear symbols
- extract a confusing block
- split mixed phases
- move logic to the data it depends on
- remove duplication first

## Quick Chooser

Use this as a quick chooser, not a rigid law:

- **Mysterious Name** -> Rename
- **Duplicated Code** -> Extract Function, Consolidate, Move Function
- **Long Function** -> Extract Function, Split Phase
- **Long Parameter List** -> Introduce Parameter Object, Preserve Whole Object
- **Global Data / Mutable Data** -> Encapsulate Variable, Encapsulate Record, Separate Query from Modifier
- **Divergent Change / Shotgun Surgery** -> Move Function, Extract Class, Combine related behavior
- **Feature Envy** -> Move Function
- **Data Clumps** -> Introduce Parameter Object, Extract Class
- **Primitive Obsession** -> Replace Primitive with Object
- **Repeated Switches** -> Replace Conditional with Polymorphism
- **Temporary Field** -> Extract Class
- **Lazy Element / Middle Man** -> Inline or remove the unnecessary indirection
- **Alternative Classes With Different Interfaces** -> Rename, Move, Extract Superclass

## Safety Rules

- Never let the code stay broken between steps.
- Prefer local, reversible edits before architectural ones.
- Prefer explicit names over clever abstraction.
- Prefer many small commits over one large commit.
- If tests fail, assume the last step is wrong until proven otherwise.
- Revert aggressively instead of debugging a giant diff.
- Keep public interfaces stable unless changing them is part of the task.
- When an interface must change across boundaries, use compatibility shims or staged migration.
- Do not refactor unrelated areas just because they are ugly.
- Leave the touched area a bit healthier than you found it.

## Verification Ladder

Use the strongest available verification, in this order:

1. existing automated tests
2. new characterization tests
3. deterministic integration checks
4. reproducible manual checks

## Working Heuristics

- In legacy code, improve the area you must touch instead of trying to beautify everything.
- In low-test systems, choose especially safe transformations and verify constantly.
- Do not mix performance tuning into routine refactoring. First improve clarity, then measure, then optimize only where evidence demands it.
- Long-lived feature branches make refactoring harder. Integrate frequently and keep branch lifetime short.
- Stop when the next intended change is easy and the design is no longer clearly improving.

## Definition Of Done

A refactoring task is done only when:

- observable behavior is preserved
- tests or equivalent checks pass
- the target area is easier to understand
- the next intended change is easier than before
- no unnecessary abstraction was introduced

## Reference Strategy

Stay in this file by default. Read references only when the default loop is not enough:

- `references/01-core-principles.md`
  Use when you need the core definition, the "two hats" model, or the decision standard for good design.
- `references/02-workflow-and-tactics.md`
  Use when you need the execution loop, preferred step order, verification ladder, or common refactoring tactics.
- `references/03-bad-smells-map.md`
  Use when you can tell the code is bad but need help naming the smell and choosing the first move.
- `references/04-refactoring-priority.md`
  Use when you want to prioritize which refactorings to learn or reach for first.
- `references/05-fowler-statement-example.md`
  Use when you want a concrete Fowler-style example of the rhythm in practice.
- `references/06-team-process-and-tradeoffs.md`
  Use when the refactor is long-running, low-test, performance-sensitive, cross-boundary, or collaboration-heavy.

## Response Style

When using this skill, report progress as:

1. smell observed
2. chosen micro-refactoring
3. verification performed
4. resulting improvement

## Default Output Contract

When asked to refactor, produce:

- a short diagnosis of the smell
- the minimal refactoring plan
- the ordered micro-steps
- the verification method
- the final code change

## One-Line Principle

**For each desired change, first make the change easy, then make the easy change.**
