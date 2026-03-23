# Bad Smells Map

## Common Bad Smells

### Mysterious Names
- Symptom: reading the code feels like solving a puzzle.
- Candidate moves: Rename Variable, Rename Field, Change Function Declaration.

### Comments Explaining Confusing Code
- Symptom: comments are carrying meaning that the code itself should express.
- Candidate moves: Rename, Extract Function, Move Function, Split Phase.

### Duplicated Code
- Symptom: the same logic appears in several copies.
- Candidate moves: Extract Function, Move Function, Pull Up Method, Consolidate Conditional Expression.

### Long Function
- Symptom: understanding it requires holding too much context in memory.
- Candidate moves: Extract Function, Replace Temp with Query, Split Phase.

### Long Parameter List
- Symptom: calls are expensive and the signature is noisy.
- Candidate moves: Introduce Parameter Object, Preserve Whole Object.

### Global Data / Mutable State
- Symptom: it is hard to tell who changed the data.
- Candidate moves: Encapsulate Variable, Encapsulate Record, Encapsulate Collection, Separate Query from Modifier.

### Divergent Change
- Symptom: the same module keeps changing for different reasons.
- Candidate moves: Separate responsibilities, Split Phase, Extract Class, Move Function.

### Shotgun Surgery
- Symptom: one request touches a dozen places.
- Candidate moves: Move Function, Move Field, Extract Class, Combine related behavior.

### Feature Envy
- Symptom: a function is more interested in another object's data than its own host.
- Candidate moves: Move Function.

### Data Clumps
- Symptom: several fields always appear together.
- Candidate moves: Extract Class, Introduce Parameter Object.

### Primitive Obsession
- Symptom: business concepts are forced into primitive types.
- Candidate moves: Replace Primitive with Object.

### Repeated Branch Logic
- Symptom: the same switch or if chain is copied everywhere.
- Candidate moves: Replace Conditional with Polymorphism, Decompose Conditional, Replace Nested Conditional with Guard Clauses.

### Deep Nesting
- Symptom: control flow is hard to follow because important logic is buried several levels deep.
- Candidate moves: Replace Nested Conditional with Guard Clauses, Decompose Conditional.

### Complicated Branches
- Symptom: one conditional block is doing too much reasoning at once.
- Candidate moves: Decompose Conditional, Split Phase.

### Temporary Field
- Symptom: an object carries transient state that only matters for one phase of work.
- Candidate moves: Extract Class.

### Lazy Element
- Symptom: a class or function adds indirection but little value.
- Candidate moves: Inline Function, Inline Class.

### Middle Man
- Symptom: a layer mostly forwards calls without adding meaning.
- Candidate moves: Remove Middle Man.

### Speculative Generality
- Symptom: abstractions were added for a future that may never arrive.
- Candidate moves: Inline, Collapse Hierarchy, remove unused hooks, parameters, and layers.

### Alternative Classes With Different Interfaces
- Symptom: similar concepts expose different shapes, which forces branching and adapter code in callers.
- Candidate moves: Rename, Move Function, Extract Superclass.
