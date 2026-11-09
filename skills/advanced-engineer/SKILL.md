---
name: advanced-engineer
description: "Unified software-engineering workflow for planning/specs, task slicing, domain and architecture design, prototypes, implementation, TDD, debugging, refactoring, performance, code/UI review, verification, developer documentation, handoff, and retrospectives. Use for software requests including 实现、修复、重构、测试、代码审查、需求拆分、架构设计、工程交接, React/Next.js engineering, and WebGL/WebGPU/Canvas effect extraction. Select only the relevant internal procedures. Excludes general prose, non-software planning/research, app operations, and visual-design-only work."
---

# Advanced Engineer

The single entry for software engineering. Choose the requested outcome, read only the relevant procedures, and preserve the user's scope. Independent engineering skills have been replaced by internal references.

## Select the mode

| Requested outcome | Read |
| --- | --- |
| Implement a feature or fix | Inspect the current path and requirements, then use the operating loop below; [ticket implementation](references/workflows/implement/GUIDE.md) for ticket-driven work |
| Diagnose a bug, failing test/build/integration, or regression | [Root-cause analysis](references/05-debugging-and-root-cause-analysis.md); [hard-bug feedback loops](references/workflows/diagnosing-bugs/GUIDE.md) when useful |
| Restructure code while preserving behavior | [Refactoring](references/08-refactoring.md) |
| General review or implementation self-review | [Work review](references/09-code-review.md); findings ordered by severity |
| Fixed-base code review with separate Standards/Spec reviewers | [Two-axis code review](references/workflows/code-review/GUIDE.md); preserve its parallel review and separate reports |
| Verify and deliver code changes | [Verification](references/03-verification-and-review.md); [safe delivery](references/04-safe-delivery.md) for destructive/public actions |
| Clarify requirements or stress-test an engineering plan | [Clarification](references/workflows/clarify-plan/GUIDE.md); [domain-aware design discussion](references/workflows/grill-with-docs/GUIDE.md) when recording decisions |
| Write a spec from an agreed discussion | [Specification](references/workflows/to-spec/GUIDE.md) |
| Break a plan into executable vertical slices | [Local slicing](references/workflows/slice-plan/GUIDE.md); [tracker tickets](references/workflows/to-tickets/GUIDE.md) only when requested |
| Resolve a multi-session effort's unknown decisions | [Wayfinding](references/workflows/wayfinder/GUIDE.md) |
| Design modules, seams, domain terms, glossaries, or ADRs | [Module design](references/workflows/codebase-design/GUIDE.md), [domain modeling](references/workflows/domain-modeling/GUIDE.md) |
| Survey architectural improvement opportunities | [Architecture survey](references/workflows/improve-codebase-architecture/GUIDE.md) |
| Prototype a UI, state model, or business rule | [Prototype](references/workflows/prototype/GUIDE.md); [logic/UI walkthrough tactics](references/workflows/prototype-patterns/GUIDE.md) if needed |
| Work test-first or design behavioral tests | [TDD](references/workflows/tdd/GUIDE.md) |
| Implement a spec with a dependency graph of tickets | [Spec implementation](references/workflows/implement-spec/GUIDE.md) |
| Triage incoming issues or external PRs | [Triage](references/workflows/triage/GUIDE.md) |
| Configure tracker, triage labels, or domain-doc layout | [Project setup](references/workflows/setup-matt-pocock-skills/GUIDE.md), only when needed |
| Research technical documentation, source, or APIs | [Research](references/workflows/research/GUIDE.md) |
| Build a wizard for steps only a human can perform | [Human setup wizard](references/workflows/wizard/GUIDE.md) |
| Write/review developer docs or API/CLI instructions | [Technical writing](references/workflows/technical-doc-writing/GUIDE.md) |
| React/Next.js implementation, review, or performance | [React practices](references/workflows/vercel-react-best-practices/GUIDE.md); select the relevant rules |
| React composition or component API design | [Composition patterns](references/workflows/vercel-composition-patterns/GUIDE.md) |
| Audit UI code against Web accessibility/design guidelines | [Web guidelines](references/workflows/web-design-guidelines/GUIDE.md) |
| Extract/replay a URL's WebGL/WebGPU/Canvas effect | [Shader extraction](references/workflows/web-shader-extractor/GUIDE.md) |
| Measure performance or manage cross-module contracts | [Performance measurement](references/07-performance-measurement.md), [data/interfaces](references/06-data-and-interface-design.md) |
| Handoff engineering work or review a coding session | [Detailed handoff](references/workflows/handoff/GUIDE.md), [compact handoff](references/workflows/handoff-compact/GUIDE.md), [retrospective](references/workflows/retro/GUIDE.md) |

Before using an imported workflow under `references/workflows/`, read [integration rules](references/workflows/README.md). They resolve former assumptions about independent skills, trackers, delegation, and publishing. Resolve workflow-relative resource paths from the selected GUIDE directory. Keep large reference catalogs unloaded until needed.

## Scope and authorization

- **Review:** inspect and report findings first. Fix code only if fixes are also requested. Planning, research, and retrospective requests likewise do not imply implementation.
- **Implementation:** refactor only where it serves the authorized goal. Before completing substantive changes, use the internal code-review procedure in self-review mode, correct in-scope findings, and verify corrections.
- **External delivery:** issue creation/comments, commits, pushes, PR state changes, deployment, and messages require task authorization; selecting a workflow does not supply it.
- Choose the procedure that matches the requested outcome, then preserve its required steps. Do not load unrelated procedures. If the selected procedure cannot run as specified, disclose the limitation rather than silently relaxing it.

## Operating loop

1. Establish the requested result and current behavior. Read applicable repository instructions and surrounding code; respect all directory access exclusions.
2. For failures, reproduce where practical, form testable hypotheses, and identify the cause before patching. A failed attempt should change what you know before the next attempt.
3. Make the smallest coherent change using local conventions. Keep structural and behavior changes separately verifiable; preserve behavior unless the task requests changing it.
4. Run meaningful, proportional checks against the requested behavior and affected boundaries. Use [engineering fundamentals](references/01-engineering-fundamentals.md) for abstraction/boundary risks and [planning/execution](references/02-planning-and-execution.md) for longer tasks.
5. Review the result against correctness, repository standards, and intended requirements. Report fresh evidence, residual risk, and verification limits accurately.

## Completion

The requested artifact or behavior is delivered, relevant checks have been read and assessed, and remaining uncertainty is stated. A review can complete with findings; a plan can complete without implementation. An implementation requires the requested behavior or structural improvement and a self-review, with verification evidence or explicit limits. A plausible diff alone does not prove success.

## Utilities

[find-polluter.sh](scripts/find-polluter.sh) isolates test pollution. [Condition-based waiting](references/condition-based-waiting-example.ts) illustrates event-driven waits.

## Preserve absorbed intent

Consolidation changes entry points and resource paths, not the selected source's goals, prerequisites, mandatory steps/order, defaults, outputs, or completion criteria. Keep incompatible source variants separate and disclose limitations. Read [the preservation audit](SEMANTICS.md) when adapting or updating a source. A clean text merge is not evidence of preserved meaning.

## Sources and maintenance

Read [source provenance and absorbed-update instructions](SOURCES.md) when tracing a capability or updating from upstream. [sources.json](sources.json) records original skills, revisions, capabilities, and current targets.
