# Personal Agent Skills

This repository stores a set of reusable agent skills for managing my own prompt workflows, engineering methods, and imported skill packages. It covers three main jobs:

- write and maintain local skills
- install skills into `~/.agents/skills`
- sync remote skills from upstream repositories and track their source

## What Is A Skill

A skill is a reusable set of instructions organized around a class of tasks. The goal is not to collect loose prompts. The goal is to package a stable workflow, constraints, reference material, and helper scripts into a unit the agent can invoke when needed.

A skill usually includes at least:

- `SKILL.md`: the entry file that defines the skill name, purpose, trigger conditions, and workflow
- `agents/openai.yaml`: metadata used on the agent side

Optional supporting directories include:

- `references/`: longer documents, standards, or knowledge files loaded on demand
- `scripts/`: reusable helper scripts
- `assets/`: templates, static files, or other reusable outputs

This repository currently contains two kinds of skills:

- local custom skills maintained directly in this repo
- remote-sync skills tracked in `skills/.remote-sources.yaml` and updated from upstream repositories

## Repository Layout

```text
.
├── skills/
│   ├── <skill-name>/             # Local skills or synced skills stored in this repo
│   │   ├── SKILL.md
│   │   ├── agents/
│   │   │   └── openai.yaml
│   │   ├── references/           # Optional
│   │   ├── scripts/              # Optional
│   │   └── assets/               # Optional
│   └── .remote-sources.yaml      # Remote skill source manifest
├── scripts/
│   ├── new-skill.sh              # Create a new local skill
│   ├── install-skills.sh         # Install skills into a local directory
│   └── sync-remote-skills.sh     # Sync remote skills from upstream repositories
└── .github/workflows/
    └── verify-skills-install.yml
```

## Current Skills

### Local Custom Skills

| Skill | Purpose | Source |
| --- | --- | --- |
| [`writing-maestro`](skills/writing-maestro/SKILL.md) | Writing and editing workflow for human-facing prose, with emphasis on clarity, concision, and removing AI-sounding phrasing. | Local custom skill |
| [`advanced-engineer`](skills/advanced-engineer/SKILL.md) | End-to-end engineering workflow covering debugging, root-cause analysis, minimal fixes, verification, and delivery checks. | Local custom skill |
| [`refactoring`](skills/refactoring/SKILL.md) | Small-step, behavior-preserving refactoring guidance focused on making the next code change easier, safer, and cheaper. | Local custom skill |
| [`prototype`](skills/prototype/SKILL.md) | Throwaway prototypes for uncertain UI, state-machine, or business-logic questions before production work. | Local custom skill |
| [`handoff`](skills/handoff/SKILL.md) | Temporary handoff briefs for continuing long-running work in another session or agent. | Local custom skill |
| [`clarify-plan`](skills/clarify-plan/SKILL.md) | Focused planning questions with recommended answers for ambiguous or high-cost changes. | Local custom skill |
| [`slice-plan`](skills/slice-plan/SKILL.md) | Break broad plans into vertical AFK/HITL slices with dependencies and acceptance criteria. | Local custom skill |
| [`review-work`](skills/review-work/SKILL.md) | Review changes along repository standards and spec compliance with findings first. | Local custom skill |

### Remote-Synced Skills

| Source | Synced skills | Notes |
| --- | --- | --- |
| [`obra/superpowers`](https://github.com/obra/superpowers/tree/main/skills) | [`verification-before-completion`](skills/verification-before-completion/SKILL.md), [`systematic-debugging`](skills/systematic-debugging/SKILL.md) | Verification and debugging workflows. |
| [`zanwei/design-dna`](https://github.com/zanwei/design-dna) | [`design-dna`](skills/design-dna/SKILL.md) | Visual identity extraction and application. |
| [`lixiaolin94/skills`](https://github.com/lixiaolin94/skills) | [`web-shader-extractor`](skills/web-shader-extractor/SKILL.md) | Web shader extraction and porting workflow. |
| [`vercel-labs/agent-skills`](https://github.com/vercel-labs/agent-skills/tree/main/skills) | [`vercel-composition-patterns`](skills/vercel-composition-patterns/SKILL.md), [`vercel-react-best-practices`](skills/vercel-react-best-practices/SKILL.md), [`web-design-guidelines`](skills/web-design-guidelines/SKILL.md) | React, Next.js, component architecture, and web design guidance. |
| [`vercel-labs/skills`](https://github.com/vercel-labs/skills/tree/main/skills) | [`find-skills`](skills/find-skills/SKILL.md) | Skill discovery helper. |
| [`openai/skills`](https://github.com/openai/skills/tree/main/skills/.system) | [`skill-creator`](skills/skill-creator/SKILL.md), [`skill-installer`](skills/skill-installer/SKILL.md) | Skill creation and installation workflows. |
| [`larksuite/cli`](https://github.com/larksuite/cli/tree/main/skills) | `lark-*` suite: [`lark-approval`](skills/lark-approval/SKILL.md), [`lark-apps`](skills/lark-apps/SKILL.md), [`lark-attendance`](skills/lark-attendance/SKILL.md), [`lark-base`](skills/lark-base/SKILL.md), [`lark-calendar`](skills/lark-calendar/SKILL.md), [`lark-contact`](skills/lark-contact/SKILL.md), [`lark-doc`](skills/lark-doc/SKILL.md), [`lark-drive`](skills/lark-drive/SKILL.md), [`lark-event`](skills/lark-event/SKILL.md), [`lark-im`](skills/lark-im/SKILL.md), [`lark-mail`](skills/lark-mail/SKILL.md), [`lark-markdown`](skills/lark-markdown/SKILL.md), [`lark-minutes`](skills/lark-minutes/SKILL.md), [`lark-okr`](skills/lark-okr/SKILL.md), [`lark-openapi-explorer`](skills/lark-openapi-explorer/SKILL.md), [`lark-shared`](skills/lark-shared/SKILL.md), [`lark-sheets`](skills/lark-sheets/SKILL.md), [`lark-skill-maker`](skills/lark-skill-maker/SKILL.md), [`lark-slides`](skills/lark-slides/SKILL.md), [`lark-task`](skills/lark-task/SKILL.md), [`lark-vc`](skills/lark-vc/SKILL.md), [`lark-vc-agent`](skills/lark-vc-agent/SKILL.md), [`lark-whiteboard`](skills/lark-whiteboard/SKILL.md), [`lark-wiki`](skills/lark-wiki/SKILL.md), [`lark-workflow-meeting-summary`](skills/lark-workflow-meeting-summary/SKILL.md), [`lark-workflow-standup-report`](skills/lark-workflow-standup-report/SKILL.md) | Feishu/Lark CLI workflows across docs, IM, calendar, Base, Sheets, tasks, meetings, and approvals. |

## Quick Start

Create a new skill:

```bash
./scripts/new-skill.sh my-skill "What this skill does and when it should be used"
```

Install all skills in this repository locally:

```bash
./scripts/install-skills.sh
```

Sync remote skills into this repository:

```bash
./scripts/sync-remote-skills.sh
```

Preview the actions without writing files:

```bash
./scripts/new-skill.sh --dry-run my-skill "What this skill does and when it should be used"
./scripts/install-skills.sh --dry-run
./scripts/sync-remote-skills.sh --dry-run
```

## Create A Skill

The bootstrap script creates the minimum skill skeleton:

```bash
./scripts/new-skill.sh my-skill "What this skill does and when it should be used"
```

It creates:

- `skills/my-skill/SKILL.md`
- `skills/my-skill/agents/openai.yaml`

After that, finish `SKILL.md` first, then decide whether the skill needs extra directories:

- define clearly when the skill should trigger
- keep only stable, reusable workflow logic
- move long reference material into `references/`
- add scripts only when they are genuinely reusable
- add templates or static resources in `assets/` when needed

## Skill Authoring Guidelines

- one skill per directory
- use lowercase kebab-case for directory names, for example `android-release-notes`
- keep each skill as self-contained as possible
- keep `SKILL.md` short and clear, and move long material into `references/`
- put only reusable constraints, decision rules, and workflows into a skill
- register imported skills that should keep syncing in `skills/.remote-sources.yaml`

A good skill should answer three questions:

- when should it be used
- what steps should the agent follow
- where should the agent load supporting material from when needed

## Install Skills

Install all skills into the default directory `~/.agents/skills`:

```bash
./scripts/install-skills.sh
```

Install a single skill:

```bash
./scripts/install-skills.sh my-skill
./scripts/install-skills.sh skill-installer
```

Preview the install without writing files:

```bash
./scripts/install-skills.sh --dry-run
```

Clear the destination directory before reinstalling:

```bash
./scripts/install-skills.sh --clean-install-dir
```

Use symlinks instead of copying:

```bash
./scripts/install-skills.sh --mode link
```

Install into a custom directory:

```bash
./scripts/install-skills.sh --install-dir /path/to/skills
```

The script supports repeated `--install-dir` flags so you can install the same set of skills into multiple destinations.

## Sync Remote Skills

Remote skill sources are defined in `skills/.remote-sources.yaml`. Each entry includes:

- `skill_name`: the skill name
- `local_path`: the relative path inside this repository
- `repo`: the upstream GitHub repository
- `ref`: the default branch or tag to sync from
- `source_path`: the source directory in the upstream repository
- `last_synced_commit`: the exact upstream commit last copied into this repo

Example:

```yaml
skills:
  - skill_name: verification-before-completion
    local_path: verification-before-completion
    repo: obra/superpowers
    ref: main
    source_path: skills/verification-before-completion
    last_synced_commit: 7e516434f2a30114300efc9247db32fb37daa5f9

  - skill_name: skill-installer
    local_path: skill-installer
    repo: openai/skills
    ref: main
    source_path: skills/.system/skill-installer
    last_synced_commit: dc48aff8208131776c9937326002bd60cf572ab6
```

Sync all remote skills:

```bash
./scripts/sync-remote-skills.sh
```

Sync a single skill:

```bash
./scripts/sync-remote-skills.sh verification-before-completion
./scripts/sync-remote-skills.sh skill-installer
```

Preview the sync plan without making network requests or writing files:

```bash
./scripts/sync-remote-skills.sh --dry-run
```

Temporarily override the branch or tag:

```bash
./scripts/sync-remote-skills.sh --ref main web-design-guidelines
```

During a real sync, the script compares the latest upstream commit with `last_synced_commit` first:

- unchanged skills are skipped
- changed skills overwrite the corresponding local directory
- `last_synced_commit` in the manifest is updated to the latest synced commit

If you add a new external skill and want to keep syncing it later, add it to `skills/.remote-sources.yaml`.

## Verification And CI

This repository includes a GitHub Actions workflow that verifies selected skills can be installed through the public `skills` CLI:

- workflow file: `.github/workflows/verify-skills-install.yml`
- runs on pushes to `main` and on pull requests that change `skills/**` or the workflow file
- when run manually, you can choose which skills to verify
- the current whitelist verifies `advanced-engineer`, `clarify-plan`, `handoff`, `prototype`, `refactoring`, `review-work`, `slice-plan`, and `writing-maestro`

The workflow runs:

```bash
npx skills add -y -g <owner>/<repo> --skill <skill-name>
```

This checks whether the public install path works. It does not mean every skill in the repo is published for public use.

## Recommended Workflow

1. Use `./scripts/new-skill.sh` to generate a minimal skill.
2. Write the trigger conditions, workflow, and reference entry points in `SKILL.md` first.
3. Add `references/`, `scripts/`, or `assets/` only when they provide real reuse.
4. Use `./scripts/install-skills.sh --dry-run` to confirm the install target is correct.
5. Install the skill locally and use it once to confirm the trigger description and workflow are actually usable.
6. If the skill comes from an external repository, add it to `skills/.remote-sources.yaml` and maintain it with the sync script.
