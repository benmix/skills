# Debugging And Root Cause Analysis

---

# Understand the problem before changing code

## Rule

Before making any code change, fully understand the problem being investigated. This includes clearly identifying what is failing, where it fails, and how the system reaches that failure state. Do not modify code until the failure has been reproduced (when possible), the exact error and context have been examined, and the execution path leading to the issue is understood.

## Why It Matters

Effective debugging starts from clarity. Without understanding the problem, any fix is likely to be superficial, misdirected, or introduce new issues.

## How To Apply It

Before making any modification:

* Reproduce the failure when possible
* Read the exact error message and stack trace
* Locate the failing code and its surrounding implementation
* Understand the execution path that leads to the failure

Do not modify code you do not yet understand.

## Common Failure Mode

Jumping into code changes based on intuition or partial understanding.

## Practical Test

Can you clearly explain what is failing, where it is failing, and how execution reaches that point?

---

# Identify and fix the root cause, not just the visible symptom

## Rule

Always identify and address the root cause of a failure rather than applying fixes that only mask or bypass symptoms. A valid fix must correct the underlying mechanism that produced the incorrect behavior, not merely prevent the failure from surfacing.

## Why It Matters

A fix that only appears to work may leave the underlying issue unresolved. Real correctness comes from addressing the mechanism that produced the failure.

## How To Apply It

Before patching, answer:

* What exactly caused the failure?
* Which assumption was violated?
* Which component produced the incorrect behavior?

Prefer fixes that correct the underlying mechanism. If a change only suppresses symptoms, continue investigating.

## Common Failure Mode

Adding guards, retries, or fallbacks that hide the issue without explaining it.

## Practical Test

Does the fix eliminate the cause of the failure, or only make the failure less visible?

---

# Drive debugging with a structured Plan -> Act -> Reflect loop

## Rule

All debugging and development work must follow a strict, iterative **Plan -> Act -> Reflect** loop. Each step must be intentional, evidence-driven, and explicitly evaluated before proceeding. Do not perform actions without a defined purpose, and do not proceed without incorporating what was learned from the previous step.

## Why It Matters

A disciplined loop prevents random actions, ensures each step is purposeful, and allows progress to be guided by evidence instead of guesswork.

## How To Apply It

### Plan

Before acting, define:

* The problem currently under investigation
* The next action to take
* What information that action should reveal
* How success will be measured

Prefer short, concrete plans such as:

* Inspect the stack trace
* Locate the failing function
* Read the surrounding implementation

### Act

Execute the planned step. Typical actions include:

* Read repository files
* Search the codebase
* Inspect logs and runtime output
* Run commands
* Check configuration and dependency versions
* Implement code changes
* Create or run tests

Only this step should change system state.

### Reflect

After each action, determine:

* What new information was discovered
* Whether expectations were met
* Which assumptions were confirmed or invalidated
* What the next step should be

Do not chain actions without reflection.

## Common Failure Mode

Performing multiple unconnected debugging actions without learning from each step.

## Practical Test

After each step, can you state what you learned and why the next step logically follows?

---

# Use hypothesis-driven debugging

## Rule

Debugging must be guided by explicit, testable hypotheses. At any point in the investigation, maintain a set of plausible explanations for the observed behavior, and use targeted checks or experiments to validate or eliminate each hypothesis.

## Why It Matters

Debugging becomes reliable when driven by explicit reasoning instead of trial-and-error.

## How To Apply It

Follow this process:

1. Observe evidence from stack traces, logs, runtime output, configuration, and dependency versions
2. Generate multiple plausible explanations
3. Design a validation step for each explanation
4. Use evidence to eliminate incorrect hypotheses

Example:

* H1: A dependency is missing -> inspect installed packages
* H2: A version is incompatible -> compare versions and constraints
* H3: An import path is wrong -> search resolution paths
* H4: Environment misconfiguration -> inspect env vars and configs

## Common Failure Mode

Locking onto the first explanation and patching immediately.

## Practical Test

Can you list current hypotheses, supporting evidence, and how each will be tested?

---

# Implement the smallest correct fix that preserves surrounding behavior

## Rule

When implementing a fix, apply the minimal change necessary to correctly resolve the root cause while preserving existing behavior and system integrity. Avoid expanding the scope of changes beyond what is required by the problem.

## Why It Matters

A fix should not only work, but integrate safely. Smaller changes reduce risk and avoid unintended regressions.

## How To Apply It

When implementing a fix:

* Minimize scope
* Preserve readability
* Follow repository conventions
* Preserve existing functionality unless requirements state otherwise

Avoid large refactors unless required by the root cause.

## Common Failure Mode

Overengineering or introducing broad changes for a localized issue.

## Practical Test

Is this the minimal change that correctly solves the real problem?

---

# Verify fixes through real execution, not just code inspection

## Rule

A fix is not considered complete until it has been verified through actual system execution. Validation must demonstrate that the original failure is resolved in practice and that no regressions have been introduced in related behavior.

## Why It Matters

A patch that looks correct is not sufficient. The system must work correctly in practice, end to end.

## How To Apply It

Every fix should go through:

1. Reproduce the failure
2. Apply the patch
3. Confirm the original failure is resolved
4. Run sanity or regression checks
5. Inspect nearby code paths for related issues

If reproduction is not possible, clearly state verification limits.

Examples of sanity checks:

* Relevant tests pass
* The affected flow works end to end
* No new errors appear nearby

If the same bug pattern exists elsewhere and is safe to fix, address it as well.

## Common Failure Mode

Stopping after code compiles or tests narrowly pass.

## Practical Test

Can you demonstrate that the original issue is resolved in practice and nothing nearby broke?

---

# Adapt strategy based on failed attempts

## Rule

When a debugging attempt fails, explicitly analyze the failure, identify the incorrect assumption, and adjust the strategy accordingly. Do not repeat the same approach with minor variations.

## Why It Matters

Repeated failures often indicate incorrect assumptions. Progress requires changing approach, not repeating the same idea.

## How To Apply It

When an attempt fails:

* Analyze why it failed
* Identify the broken assumption
* Choose a meaningfully different next strategy

Escalate investigation depth:

* 1st failure: re-check errors, code, assumptions
* 2nd: search exact error and documentation
* 3rd: trace execution and instrument code
* 4th: isolate via minimal reproduction
* 5th: reconsider architecture or framing

## Common Failure Mode

Retrying similar fixes without revisiting underlying assumptions.

## Practical Test

Is the new attempt based on new evidence or a revised understanding?

---

# Verify assumptions instead of relying on them

## Rule

Do not rely on assumptions when they can be verified. Any critical assumption about system state, configuration, dependencies, or external behavior must be validated through direct inspection or testing.

## Why It Matters

Incorrect assumptions about environment, dependencies, or APIs are a frequent source of bugs.

## How To Apply It

Validate critical assumptions, especially:

* Dependency versions
* Environment configuration
* API behavior
* File paths
* Permissions
* Environment variables

## Common Failure Mode

Treating assumptions as facts without verification.

## Practical Test

Have all critical assumptions been verified or explicitly marked as unverified?

---

# Use available tools to gather evidence before asking for help

## Rule

Prioritize gathering evidence using available tools and system artifacts before asking for external input. Investigation should first rely on observable data such as code, logs, configuration, and runtime behavior.

## Why It Matters

Most debugging information already exists in the system. Using it first leads to faster and more accurate diagnosis.

## How To Apply It

Prefer to:

* Search the repository
* Inspect stack traces and logs
* Read configuration
* Check documentation and dependencies

Ask for help only after reasonable investigation.

## Common Failure Mode

Requesting clarification too early without examining available evidence.

## Practical Test

Have you exhausted the accessible evidence before asking external questions?

---

# Ask for clarification only when necessary, and make it precise

## Rule

When external input is required, ask targeted and well-informed questions. Clearly communicate what has been tried, what is known, and what specific information is missing.

## Why It Matters

Some issues require external input, but questions should be focused and informed by prior investigation.

## How To Apply It

Ask when:

* Credentials or external data are missing
* Domain knowledge is unavailable
* Multiple valid decisions exist
* The issue cannot be reproduced

Include:

* What was tried
* What evidence was collected
* What specific information is missing

## Common Failure Mode

Asking vague or premature questions.

## Practical Test

Does the question clearly show context, effort, and the exact missing piece?

---

# Consider the task complete only when the outcome is validated

## Rule

A task is complete only when the root cause is understood, the fix correctly addresses that cause, and the system behavior has been validated in practice. Do not consider work finished based on code changes alone.

## Why It Matters

Completion means the system works correctly, not just that code has changed.

## How To Apply It

A task is complete only when:

* The root cause is understood
* The fix addresses that root cause
* The issue is resolved in practice (or limits are stated)
* The fix is validated
* No obvious regressions remain

Take ownership of the full outcome, including integration with the surrounding system.

## Common Failure Mode

Declaring success based on confidence rather than evidence.

## Practical Test

Can you explain the cause, show the fix, demonstrate the result, and state any remaining uncertainty?

---
