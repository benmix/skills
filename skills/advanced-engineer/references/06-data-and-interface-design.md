# Data and interface design

Use for changes to cross-module contracts, related lifecycle states, or concurrent ownership. For a local edit with an established pattern, use that pattern without a separate design exercise.

## Start from the caller

Write one realistic usage example before choosing the interface. Name the input, observable result, failure behavior, and who owns resources across the operation. Derive the signatures and core types from that usage. Keep the sketch in task notes unless the project needs a durable design record.

Identify the facts that must remain true, such as which states require data and who may change each value. Choose a structure that expresses those facts:

- A discriminated union or state machine for mutually exclusive lifecycle states.
- A table or registry for a repeated mapping rule.
- A domain module for policy duplicated across execution stages.
- Derived values instead of fields that must stay synchronized.

Keep ordinary code when the current shape is clear. An abstraction earns its cost by removing invalid states, repeated decisions, or coordination from callers. It does not need multiple callers when it owns a substantial invariant or resource lifecycle.

## Establish boundaries and ownership

Parse external input into domain values at trust boundaries. Internal code may rely on validated invariants; storage, plugins, foreign code, and deserialization can introduce new boundaries. Strengthen types where current code needs repeated checks or unsafe assumptions. A cast needs a concrete justification, not a blanket ban.

Give mutable state an explicit owner. Before adding locks, check whether concurrent actors can publish to separate owned targets. If shared mutation is necessary, use structural coordination such as a single writer, atomic operations, or locks. Define what retries and partial failure do; externally visible effects may require idempotency keys or reconciliation.

## Check the shape during implementation

Repeated workarounds, similar type escapes, or callers coordinating internal steps are evidence that the sketch may be wrong. Revisit the missing constraint before adding more branches. A single justified edge case does not require a redesign.

Compare alternatives when the decision is costly or lacks precedent. Use a small experiment for observable uncertainty and ask about unresolved product preferences. Stop exploring when the design meets the contract with acceptable complexity.

Adapted from Lauren Tan's pstack domain modeling, architect, boundary, type, and shared-state practices.
