# Core Principles

## Definition Of Refactoring

- Noun: changing the internal structure of software without changing its externally observable behavior, so it becomes easier to understand and modify.
- Verb: reshaping software through a series of small refactorings like that.

## Core Principles

1. Preserve behavior before pursuing structural ambition.
2. Prefer small steps over large ones.
3. Verify every step instead of debugging later.
4. Write understanding back into the code instead of keeping it in your head.
5. Favor economic payoff over aesthetic argument.

## The Two Hats

- When adding functionality: define new behavior and make the tests pass.
- When refactoring: improve structure only and add no new behavior.

## Why Refactor

- Improve design
- Increase readability
- Make bugs easier to spot
- Make long-term development faster

## Common Refactoring Moments

- just before adding a feature
- while trying to understand code
- while fixing a bug
- when passing through an area that is easy to improve a little

## When Not To Refactor

- untouched ugly code behind a stable boundary
- areas where rewrite is clearly lower risk and lower cost
- situations with no realistic verification path

## The Design Stamina Hypothesis

Good design may not make you fastest on day one, but it helps you keep moving fast for much longer.

## Team-Level Implications

- self-testing code and continuous integration strongly amplify refactoring effectiveness
- long-lived branches and strict ownership boundaries make safe refactoring harder
- public APIs often require staged migrations instead of direct cleanup
