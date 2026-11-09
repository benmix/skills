# Catalog Priority

## Refactorings Worth Learning First

### Level 1: Everyday High-Frequency Moves
- Extract Function
- Inline Function
- Rename Variable
- Change Function Declaration
- Encapsulate Variable
- Extract Variable
- Inline Variable

### Level 2: Structural Reorganization
- Extract Class
- Inline Class
- Move Function
- Move Field
- Introduce Parameter Object
- Replace Temp with Query
- Split Phase

### Level 3: Complex Logic Control
- Decompose Conditional
- Replace Nested Conditional with Guard Clauses
- Replace Conditional with Polymorphism
- Introduce Special Case
- Separate Query from Modifier

### Level 4: Architecture And Inheritance
- Replace Constructor with Factory Function
- Replace Type Code with Subclasses
- Pull Up / Push Down Method and Field
- Replace Subclass with Delegate
- Replace Superclass with Delegate

## Rules Of Thumb

- If renaming solves it, do not start with abstraction.
- If Extract Function solves it, do not start with a class hierarchy.
- If moving responsibility solves it, do not start with a design pattern.
- When a pattern is truly needed, repeated change has usually already appeared.
