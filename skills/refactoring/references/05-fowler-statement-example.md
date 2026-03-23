# Chapter 1 Example Notes

In Chapter 1, Fowler uses the `statement` example to show the full rhythm:

1. Start with working legacy code
2. Add tests first
3. Identify logic blocks that can be extracted
4. Use Extract Function to split amount calculations
5. Use Replace Temp with Query to remove temporary variables that get in the way
6. Keep extracting points, formatting, and total calculations
7. Use Split Phase to separate calculation from rendering
8. Introduce an intermediate data structure
9. Reuse the same calculation logic for HTML output
10. Go further and replace type-based branching with polymorphism

The most valuable lesson in this example is not the final code. It is the rhythm:

- every step is small
- every step is validated
- naming turns understanding into code
- structure improves before new change is added
