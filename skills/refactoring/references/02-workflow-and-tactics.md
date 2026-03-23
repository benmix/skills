# Workflow And Tactics

## Minimal Refactoring Loop

1. Lock down behavior first with tests
2. Identify the smell and the intended improvement
3. Choose the smallest safe refactoring move
4. Make one small change
5. Run the tests
6. Commit or continue with the next small step

Repeat only while the code is still getting easier to change.

## Preferred Step Order

1. Rename
2. Extract
3. Move
4. Encapsulate
5. Simplify conditionals
6. Remove dead code

## Verification Ladder

Use the strongest available verification, in this order:

1. existing automated tests
2. new characterization tests
3. deterministic integration checks
4. reproducible manual checks

## Common Tactics

### Extract
- Extract Function
- Extract Class
- Extract Superclass
- Extract Variable

### Inline
- Inline Function
- Inline Class
- Inline Variable

### Move
- Move Function
- Move Field
- Move Statements into Function
- Move Statements to Callers

### Encapsulate
- Encapsulate Variable
- Encapsulate Record
- Encapsulate Collection

### Split And Decompose
- Split Loop
- Split Variable
- Split Phase
- Decompose Conditional

### Replace
- Replace Temp with Query
- Replace Primitive with Object
- Replace Conditional with Polymorphism
- Replace Constructor with Factory Function
- Introduce Special Case

## Failure Modes

- mixing behavior change with structure change
- taking too large a step
- introducing abstraction too early
- changing public contracts casually
- trying to clean the whole system at once

## Agent Heuristics

- Prefer local changes before architectural ones.
- Prefer reversible edits.
- Prefer explicit names over clever abstractions.
- Stop when the intended feature or fix becomes easy.
- Do not refactor unrelated areas just because they are ugly.

## Recommended Order

Start with moves that:

- clearly reduce cognitive load
- narrow the scope of future changes
- do not introduce extra semantic risk
- are easy to confirm with fast tests
