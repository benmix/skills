# Team Process And Tradeoffs

## Testing

The most important infrastructure for refactoring is self-testing code:

- tests must be self-checking
- they must run fast enough
- they must be runnable after every small step

If coverage is weak:

- add characterization tests around the behavior you must preserve
- prefer boundary tests around the area you are touching
- choose especially safe transformations in low-test systems

## Version Control

Recommended practice:

- make a local commit after each successful small step
- roll back quickly when something fails
- clean up commit history later when sharing externally

## Branch Strategy

Refactoring works better with:

- short-lived branches
- frequent integration
- CI / trunk-based development

Long-lived feature branches amplify the semantic conflicts caused by renames, moves, and abstraction changes.

## Long-Term Refactoring

Use gradual progress for larger structural problems such as:

- replacing a low-level library
- untangling large dependency relationships
- doing a cross-module migration
- unwinding architectural coupling

Preferred patterns:

- branch by abstraction
- parallel change
- expand-contract

Avoid big-bang rewrites when the system can be evolved incrementally.

## Performance

Do not oppose refactoring on instinct:

- clean up the structure first
- profile afterward
- optimize only hotspots
- remeasure after every optimization

If performance is critical, finish the structural improvement first, then measure, then optimize the real hotspot instead of guessing.

## When Not To Do It

- code that will not change again
- code that is clearly better rewritten
- areas with no safety net where regression risk is unacceptable
- cases where the current integration model would make the merge cost larger than the refactoring payoff

## Communicating With Management

The most effective framing is not "I want to clean up the code." It is:

- this will make the current change land faster
- this will reduce change risk
- this will reduce repeated edits in the future

## Public Interfaces And Boundaries

Be conservative when a refactor crosses package, service, or public API boundaries:

- keep contracts stable unless changing them is part of the task
- use compatibility shims when an interface must change
- prefer staged migration over direct cleanup

## Code Review

Code review is also a useful place for small live refactorings:

- rename while reading
- extract a small function while reviewing
- clarify the structure before judging the design

## Decision Standard

The best refactor is not the most impressive one. It is the one that makes the next intended change easier at acceptable risk.
