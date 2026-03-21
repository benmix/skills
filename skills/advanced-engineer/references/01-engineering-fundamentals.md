# Engineering Fundamentals

---

# Read Before Modifying

## Rule

Read the code before you propose or implement changes to it. If a task mentions a file, function, or module, inspect the existing implementation first and understand how it behaves in context.

## Why It Matters

Most bad edits start with an incorrect mental model. Reading first reduces regressions, avoids duplicate logic, and keeps new changes consistent with existing patterns.

## How To Apply It

- Open the relevant file before suggesting a fix.
- Trace the call path around the code you plan to touch.
- Reuse local conventions instead of inventing a new style.
- Confirm what the code already guarantees before adding logic.

## Common Failure Mode

An agent sees a function name in the user's request, guesses what it does, and edits it without reading the surrounding code. The result often fixes the wrong problem.

## Practical Test

Before editing, ask: "Can I explain what this code does today, what calls it, and what assumptions it relies on?" If not, read more.

---

# Avoid Over-Engineering

## Rule

Make only the changes that are directly requested or clearly necessary. Prefer the simplest solution that solves the current problem.

## Why It Matters

Over-engineering increases maintenance cost without increasing value. It adds moving parts, expands the surface area for bugs, and makes reviews harder.

## How To Apply It

- Solve the task in front of you, not three imagined future tasks.
- Prefer a local fix over a broad architectural rewrite.
- Add complexity only when the current requirement demands it.
- Leave adjacent code alone unless it blocks the requested change.

## Common Failure Mode

A small feature request turns into a new framework, a new configuration layer, or a broad refactor that the user never asked for.

## Practical Test

If the solution introduces a new concept, ask whether the current task works without it. If the answer is yes, you probably do not need it.

---

# No Premature Abstractions

## Rule

Do not create helpers, utilities, or abstractions for one-off operations or hypothetical future needs. A small amount of duplication is often better than an abstraction with no proven pressure behind it.

## Why It Matters

Premature abstractions hide intent, make code harder to read, and create APIs that the codebase does not actually need. They also become hard to remove once other code starts depending on them.

## How To Apply It

- Inline one-time logic when it is short and clear.
- Wait for repeated patterns before extracting helpers.
- Let real duplication reveal the correct abstraction boundary.
- Prefer concrete code over generic interfaces until reuse is proven.

## Common Failure Mode

Three slightly similar lines get replaced with a generalized helper that now requires flags, callbacks, or special cases to support all callers.

## Practical Test

Ask whether the abstraction has at least two real callers with the same need today. If not, keep the code concrete.

---

# No Unnecessary Additions

## Rule

Do not add features, refactors, comments, type annotations, or documentation outside the scope of the requested change unless they are required to make the change correct.

## Why It Matters

Scope creep makes changes harder to review and harder to trust. A focused patch is easier to reason about, easier to revert, and easier to validate.

## How To Apply It

- Keep bug fixes narrow.
- Do not clean up unrelated code as part of a small task.
- Add comments only when the logic is not self-evident.
- Avoid touching files that are not part of the actual change.

## Common Failure Mode

A simple fix becomes a mixed patch that also renames variables, reformats old code, adds comments everywhere, and changes type style in unrelated sections.

## Practical Test

For each diff hunk, ask: "Would I still make this change if the original request did not exist?" If not, remove it.

---

# Validate At Boundaries

## Rule

Validate inputs at system boundaries and trust internal invariants. Do not add fallbacks, guards, or defensive branches for states that cannot happen inside the design of the system.

## Why It Matters

Excess defensive code makes behavior harder to understand and can hide real bugs. Boundary checks are useful. Internal paranoia often signals weak design or unclear ownership.

## How To Apply It

- Validate user input, network input, file input, and external API responses.
- Avoid adding branches for impossible internal states.
- Remove obsolete compatibility shims when the system can move forward cleanly.
- Use failures to expose broken assumptions instead of silently masking them.

## Common Failure Mode

Code starts returning fallback values for invalid internal state instead of failing fast. The visible bug disappears, but the system becomes harder to debug.

## Practical Test

Ask whether the invalid state can be created by a real external caller. If yes, validate it. If no, preserve the invariant and fix the source of the break.

---

# Secure By Default

## Rule

Write code that does not introduce obvious security flaws. Treat command injection, SQL injection, XSS, unsafe deserialization, broken authorization, and similar classes of bugs as first-order engineering concerns.

## Why It Matters

Security defects are often cheap to introduce and expensive to remove. A fast implementation that creates an exploit path is still a bad implementation.

## How To Apply It

- Treat all external input as untrusted.
- Use parameterized queries and safe APIs instead of string concatenation.
- Escape or sanitize rendered content in the right context.
- Preserve authorization checks when refactoring code paths.
- Fix insecure code as soon as you notice it.

## Common Failure Mode

An implementation focuses on "making it work" and only later notices that it shells out with unchecked input or renders user content into HTML unsafely.

## Practical Test

Before shipping, ask: "Where does untrusted input enter this path, and how is it constrained before execution, storage, or rendering?"

---

# Change Approach When Blocked

## Rule

When an approach is blocked, do not brute-force the same failing action. Change tactics, gather better evidence, or align with the user before continuing.

## Why It Matters

Blind repetition wastes time and often damages the environment. Good engineering is adaptive. It uses failures as information.

## How To Apply It

- Stop retrying a failing command with no new insight.
- Diagnose the root cause before re-running the same step.
- Try an alternative path when the first path is clearly blocked.
- Ask the user only when the decision depends on product intent or risk tolerance.

## Common Failure Mode

A test fails, so the agent reruns it in a loop, changes random settings, or waits and retries without learning anything.

## Practical Test

After a failure, identify what new evidence the next step will produce. If it produces none, do not run it.
