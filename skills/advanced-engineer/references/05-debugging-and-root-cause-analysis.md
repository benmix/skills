# Debugging And Root Cause Analysis

Use this reference for root-cause-first debugging, concrete tracing tools, and evidence-before-claims verification.

## Quick Index

| Need | Section |
| --- | --- |
| Establish a deterministic feedback loop | [Build the feedback loop first](#build-the-feedback-loop-first) |
| Understand and fix root causes | [Identify and fix the root cause, not just the visible symptom](#identify-and-fix-the-root-cause-not-just-the-visible-symptom) |
| Trace bad data from symptom to source | [Trace bad data backward through the call chain](#trace-bad-data-backward-through-the-call-chain) |
| Make invalid data structurally harder to reintroduce | [Use defense-in-depth after finding invalid data](#use-defense-in-depth-after-finding-invalid-data) |
| Replace flaky sleeps | [Replace arbitrary waits with condition-based waits](#replace-arbitrary-waits-with-condition-based-waits) |
| Verify completion, commit, or PR claims | [Use the evidence-before-claims verification gate](#use-the-evidence-before-claims-verification-gate) |
| Find test pollution | [Find test pollution by bisection](#find-test-pollution-by-bisection) |

---

# Build the feedback loop first

## Rule

Before debugging a bug or changing behavior, establish the fastest reliable pass/fail signal you can. A good feedback loop makes every later step cheaper: reproduction, hypothesis testing, instrumentation, fixing, and regression checking.

## Why It Matters

Without a repeatable signal, debugging collapses into code reading and guesswork. A slow or flaky signal is only slightly better. Spend real effort making the loop fast, sharp, and deterministic.

## How To Apply It

Try feedback loops in roughly this order:

1. Failing automated test at the narrowest correct seam.
2. HTTP or CLI script with fixture input and expected output.
3. Headless browser check for UI behavior, DOM state, console errors, or network calls.
4. Captured trace or payload replayed through the affected code path.
5. Throwaway harness that exercises the failing function or service boundary.
6. Property, fuzz, or stress loop for intermittent or input-sensitive failures.
7. `git bisect run` style harness when the bug appeared between two known states.
8. Structured human-in-the-loop script only when automation is genuinely impossible.

Once a loop exists, improve it:

- make it faster by narrowing setup and scope
- make it sharper by asserting the user-visible symptom
- make it deterministic by pinning time, seeds, filesystem state, and network boundaries

Do not proceed to speculative fixes when no credible loop exists. State what you tried and ask for logs, traces, reproduction access, or permission to add temporary instrumentation.

## Common Failure Mode

Treating "I read the code and it looks wrong" as a feedback loop.

## Practical Test

Can you run one command or script that demonstrates the failure before the fix and demonstrates the fix afterwards?

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

# Follow the root-cause-first gate

## Rule

For bugs, test failures, build failures, integration issues, performance surprises, or other unexpected behavior, do not propose or implement fixes before root cause investigation.

## How To Apply It

Complete these phases in order:

1. Root cause investigation:
   - Read the exact error, warning, stack trace, and line numbers.
   - Reproduce the failure when possible.
   - Check recent diffs, commits, dependency changes, config changes, and environment differences.
   - In multi-component systems, instrument each boundary before guessing: log inputs, outputs, propagated config, and state at each layer.
2. Pattern analysis:
   - Find similar working code in the same codebase.
   - Read the relevant reference implementation completely when applying a known pattern.
   - List concrete differences between working and broken paths.
3. Hypothesis testing:
   - State one explicit hypothesis and the evidence behind it.
   - Make the smallest possible experiment to confirm or falsify it.
   - Change one variable at a time.
4. Implementation:
   - Add or identify a failing test or repeatable reproduction when possible.
   - Implement one minimal root-cause fix.
   - Verify the original symptom and nearby regressions.

## Stop Signals

Stop and return to investigation when you catch yourself thinking:

- "Just try this and see."
- "It is probably X."
- "I do not fully understand it, but this might work."
- "Add several fixes, then run tests."
- "Skip the test and manually verify later."
- "One more fix attempt" after multiple failed attempts.
- "I see the problem, let me fix it."
- "The reference is long; I will adapt the pattern from memory."

After three failed fix attempts, revisit the architecture or framing before adding another patch. Repeated fixes that reveal new shared-state or coupling problems usually mean the design premise is wrong, not that the fourth patch will be better.

If investigation reveals the issue is truly environmental, timing-dependent, or external, document what was investigated, implement appropriate handling such as retry, timeout, user-facing error, or monitoring, and state the remaining uncertainty. Treat "no root cause" as rare; most cases mean investigation is incomplete.

## Practical Test

Can you state the root cause investigation evidence before describing the fix?

---

# Trace bad data backward through the call chain

## Rule

When a bug appears deep in the stack, trace backward until you find the original trigger. Fixing only where the error appears treats the symptom.

## How To Apply It

1. Observe the symptom.
2. Identify the immediate failing operation.
3. Ask what called that operation.
4. Inspect the value passed at each caller.
5. Continue until you find where the bad value first entered the system.
6. Fix at the source and add validation at downstream layers when the operation is dangerous.

Add context before the dangerous operation when manual tracing stalls:

```ts
async function performOperation(input: string) {
  console.error("DEBUG operation input", {
    input,
    cwd: process.cwd(),
    nodeEnv: process.env.NODE_ENV,
    stack: new Error().stack,
  });

  await runOperation(input);
}
```

In tests, prefer `console.error()` for temporary diagnostics because loggers are often suppressed.

## Practical Test

Can you show where the bad value originated, not just where it exploded?

---

# Use defense-in-depth after finding invalid data

## Rule

When a bug is caused by invalid data crossing boundaries, validate at every meaningful layer the data passes through. One check can be bypassed by another path, refactor, or mock.

## How To Apply It

Add checks at these layers:

1. Entry point validation: reject invalid external input early.
2. Business logic validation: assert the value makes sense for this operation.
3. Environment guard: prevent dangerous behavior in special contexts such as tests, CI, or production.
4. Diagnostic context: log enough information to debug future bypasses.

Checklist:

- Map the full data flow.
- Identify every point where the invalid value can be produced, transformed, or consumed.
- Add the narrowest useful guard at each layer.
- Test that lower layers catch bypasses of upper layers.

## Practical Test

If the entry validation is bypassed, does a later layer still prevent the dangerous operation?

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

Debugging must be guided by explicit, testable hypotheses. At any point in the investigation, maintain a ranked set of plausible explanations for the observed behavior, and use targeted checks or experiments to validate or eliminate each hypothesis.

## Why It Matters

Debugging becomes reliable when driven by explicit reasoning instead of trial-and-error.

## How To Apply It

Follow this process:

1. Observe evidence from stack traces, logs, runtime output, configuration, and dependency versions
2. Generate 3-5 plausible explanations when the cause is not obvious
3. Rank them by likelihood and cost to test
4. State the prediction each hypothesis makes
5. Design a validation step for each explanation
6. Use evidence to eliminate incorrect hypotheses

Example:

* H1: A dependency is missing -> if true, package inspection will show it absent
* H2: A version is incompatible -> if true, versions will differ from documented constraints
* H3: An import path is wrong -> if true, resolution tracing will point at the wrong file
* H4: Environment misconfiguration -> if true, env/config inspection will differ between working and failing runs

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

# Replace arbitrary waits with condition-based waits

## Rule

For flaky tests and asynchronous workflows, wait for the condition you care about, not a guessed duration.

## How To Apply It

Use a polling helper with a timeout and a clear description:

```ts
async function waitFor<T>(
  condition: () => T | undefined | null | false,
  description: string,
  timeoutMs = 5000
): Promise<T> {
  const start = Date.now();

  while (true) {
    const result = condition();
    if (result) return result;

    if (Date.now() - start > timeoutMs) {
      throw new Error(`Timeout waiting for ${description} after ${timeoutMs}ms`);
    }

    await new Promise((resolve) => setTimeout(resolve, 10));
  }
}
```

Use it for events, state transitions, event counts, event predicates, files, and async results:

```ts
await waitFor(() => events.find((event) => event.type === "DONE"), "DONE event");
await waitFor(() => machine.state === "ready", "machine ready");
await waitFor(() => items.length >= 5 && items, "five items");
```

For fuller event helper examples, see [condition-based-waiting-example.ts](condition-based-waiting-example.ts).

An arbitrary timeout is acceptable only when testing timing behavior itself. Document the known timing and first wait for the triggering condition.

## Practical Test

Does the test fail only when the real condition fails, or can machine speed decide the outcome?

---

# Use the evidence-before-claims verification gate

## Rule

Before claiming work is complete, fixed, passing, clean, ready, safe to commit, ready for PR, or successfully delegated, run fresh verification and read the output.

## How To Apply It

1. Identify the command or check that proves the claim.
2. Run the full command fresh in this turn.
3. Read the output and exit code.
4. Compare output to the claim.
5. Only then report the evidence, or state the exact gap.

Skipping any step is not verification.

| Claim | Requires | Not sufficient |
| --- | --- | --- |
| Tests pass | Test command output with zero failures | Previous run or confidence |
| Linter clean | Linter command output with zero errors | Partial file checks |
| Build succeeds | Build command exit 0 | Linter output or logs that look fine |
| Bug fixed | Original symptom reproduced and then resolved | Code changed |
| Regression test works | Red-green cycle or equivalent proof | Test exists or passed once |
| Agent completed | VCS diff checked and independently verified | Agent report |
| Requirements met | Line-by-line requirement checklist plus relevant commands | Tests passing |
| Commit ready | Fresh relevant checks and reviewed staged diff | Clean-looking diff |
| PR ready | Branch state, changed-files review, and relevant checks | Commit exists |
| Task complete | Requirements checklist and relevant commands | Plausible diff |

## Stop Signals

Stop before claiming success if you are:

- Using "should", "probably", "seems to", or similar confidence language.
- Expressing satisfaction before verification.
- About to commit, push, create a PR, report final status, or move to the next task.
- Trusting another agent's success report without checking the diff and evidence.
- Relying on partial verification without saying exactly what remains unchecked.
- Tired and trying to skip the gate.

## Practical Test

Could another engineer rerun the command you cited and see the same evidence?

---

# Find test pollution by bisection

## Rule

When a test creates unwanted files or persistent state and the polluting test is unknown, isolate the polluter by running candidate tests one by one and checking for the unwanted artifact after each run.

## How To Apply It

Use [scripts/find-polluter.sh](../scripts/find-polluter.sh):

```bash
./skills/advanced-engineer/scripts/find-polluter.sh '.git' 'src/**/*.test.ts'
```

The script checks whether the target file or directory appears after each test. Adapt the test command inside the script when the repository does not use `npm test`.

## Practical Test

Can you identify the specific test that creates the unwanted artifact?

---
