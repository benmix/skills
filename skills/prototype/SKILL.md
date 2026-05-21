---
name: prototype
description: Build throwaway prototypes to answer uncertain design, UI, state-machine, or business-logic questions before committing production code. Use when the user asks to prototype, spike, sanity-check a model, try a few designs, explore a UI direction, or make something they can play with before deciding.
---

# Prototype

A prototype is throwaway code that answers a specific question. The question decides the shape.

## Choose The Prototype Type

Use a logic prototype when the uncertainty is about:

- state transitions
- business rules
- edge cases
- data model shape
- command-line or service behavior

Build the smallest runnable harness that makes the state visible after each action.

Use a UI prototype when the uncertainty is about:

- layout direction
- interaction model
- visual hierarchy
- information architecture
- comparing several interface options

Build a temporary route, page, or component that lets the user switch between materially different variants.

## Rules

- Mark prototype files clearly with `prototype`, `spike`, or an equivalent local convention.
- Put the prototype close enough to the real code that imports and context are obvious.
- Provide one command or URL to run it.
- Avoid persistence unless persistence is the thing being tested.
- Skip production polish, broad error handling, and abstractions.
- Surface the relevant state, inputs, and outputs directly.
- Do not let prototype code quietly become production code.

## Completion

When the prototype answers its question:

1. State the answer and the evidence.
2. Capture any durable decision in the right place: issue, ADR, notes, commit message, or implementation plan.
3. Delete the prototype or explicitly fold the validated part into production code.

If the user wants to keep it, label what remains and why.
