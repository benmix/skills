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

## Deep And Shallow Modules

A module is anything with an interface and an implementation: a function, class, package, workflow, component, or slice.

- **Interface**: everything a caller must know to use the module, including types, invariants, ordering, configuration, and error modes.
- **Implementation**: the code behind that interface.
- **Deep module**: a small, stable interface that hides meaningful behavior.
- **Shallow module**: an interface nearly as complex as its implementation.

Prefer refactorings that deepen modules. A good module gives callers leverage: they learn a little and get a lot. It also gives maintainers locality: changes and bugs concentrate in one place instead of spreading across callers.

## Deletion Test

When considering an abstraction, imagine deleting it.

- If complexity disappears, the abstraction may be unnecessary.
- If complexity reappears across several callers, the abstraction is probably earning its keep.

Use this test before adding a seam, wrapper, helper, or service. A seam is real when it concentrates behavior or supports real variation. One adapter often means a hypothetical seam; two adapters usually mean a real seam.

## The Two Hats

- When adding functionality: define new behavior and make the tests pass.
- When refactoring: improve structure only and add no new behavior.

## Why Refactor

- Improve design
- Increase readability
- Make bugs easier to spot
- Make long-term development faster
- Increase locality and leverage

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
