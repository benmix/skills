# Safe Delivery

---

# Execute Actions With Care

## Rule

Match the level of caution to the reversibility and blast radius of the action. Local, reversible actions are usually fine. Destructive, public, or hard-to-reverse actions require explicit confirmation.

## Why It Matters

Code changes are not the only risk in engineering work. A careless `git reset --hard`, force push, dependency downgrade, or public post can do more damage than a bug.

## How To Apply It

- Evaluate whether an action is reversible.
- Treat shared systems and public side effects as high risk.
- Investigate unexpected state before deleting or overwriting it.
- Solve blockers by finding the root cause, not by bypassing safeguards.

## High-Risk Examples

- Deleting files or branches.
- Dropping tables or overwriting uncommitted work.
- Force-pushing or amending published commits.
- Posting content to external services.

## Practical Test

Ask two questions before acting: "Can I reverse this cleanly?" and "Could this affect someone other than me?" If either answer is uncomfortable, confirm first.

---

# Git Safety And Hook Discipline

## Rule

Treat commits and pull requests as controlled engineering actions. Do not commit unless asked. Do not skip hooks. Do not use destructive git commands without explicit approval.

## Why It Matters

Git commands can destroy work as quickly as they can save it. Hook bypasses, broad staging, force pushes, and casual amends hide problems instead of fixing them.

## How To Apply It

- Stage specific files, not everything by default.
- Follow the repository's commit message style.
- Write commit messages that explain why the change exists.
- If a hook fails, fix the underlying issue and create a new commit.
- Review the full branch diff before opening a pull request.
- Do not push or open a PR unless the task requires it.

## Common Failure Modes

- Using `git add .` and capturing secrets or unrelated files.
- Skipping hooks with `--no-verify`.
- Amending after a failed hook and accidentally mutating the previous commit.
- Opening a PR after reviewing only the last commit instead of the full branch.

## Practical Test

Before any git write action, ask: "Was I explicitly asked to do this, and have I reviewed exactly what will be included?"
