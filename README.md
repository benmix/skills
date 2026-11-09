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

### Engineering

[`advanced-engineer`](skills/advanced-engineer/SKILL.md) is the only software-engineering skill. It routes planning/specs, slicing, architecture/domain modeling, prototypes, implementation, TDD, debugging, refactoring, reviews, verification, technical research/docs, React/Next.js, Web guidelines, shader extraction, handoff, and retrospectives to internal procedures. Read only the procedure needed by the task.

The former engineering skills and compatibility entries have been removed. Their resources are maintained under `skills/advanced-engineer/references/`; there are no nested `SKILL.md` discovery entries. Install with `./scripts/install-skills.sh advanced-engineer`. Existing installations of the retired skills must be removed separately; installing the new entry alone does not uninstall them. The standalone remote-source manifest no longer syncs retired skills. [The absorption registry](skills/advanced-engineer/sources.json) tracks their provenance and internal targets; [absorbed-update instructions](skills/advanced-engineer/SOURCES.md) describe review-first updates without recreating independent entries.

The imported workflow resources preserve source documentation and attribution. Matt Pocock workflows, Vercel React/Web rules, shader extraction, and local custom engineering guides are maintained internally. Selected engineering practices are adapted from [Lauren Tan's pstack 0.15.23](https://github.com/cursor/plugins/tree/dbf49813a39c1a5389c5e28cb8e4c1c2379e2454/pstack).

### Other skills

General writing (`writing-maestro`), skill creation/installation/discovery, Feishu documents (`lark-doc`), design DNA, isometric illustration (`anatomy`), and general productivity skills remain independent. Their remote sources, where applicable, remain in `skills/.remote-sources.yaml`.

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

Exclude all Lark skills from an install:

```bash
./scripts/install-skills.sh --exclude-lark
./scripts/install-skills.sh --clean-install-dir --exclude-lark
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
  - skill_name: find-skills
    local_path: find-skills
    repo: vercel-labs/skills
    ref: main
    source_path: skills/find-skills
    last_synced_commit: e4243fbf7d9398722024f62850ece90fa0d5c693

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
./scripts/sync-remote-skills.sh find-skills
./scripts/sync-remote-skills.sh skill-installer
```

Preview the sync plan without making network requests or writing files:

```bash
./scripts/sync-remote-skills.sh --dry-run
```

Temporarily override the branch or tag:

```bash
./scripts/sync-remote-skills.sh --ref main find-skills
```

During a real sync, the script compares the latest upstream commit with `last_synced_commit` first:

- unchanged skills are skipped
- changed skills overwrite the corresponding local directory
- `last_synced_commit` in the manifest is updated to the latest synced commit

If you add a new external skill and want to keep syncing it later, add it to `skills/.remote-sources.yaml`.

## Update Absorbed Engineering Sources

```bash
./scripts/sync-remote-skills.sh advanced-engineer --dry-run
./scripts/sync-remote-skills.sh --absorbed web-design-guidelines --output /tmp/engineering-source-review
# Review the package and reconcile merged/ before applying:
./scripts/sync-remote-skills.sh --absorbed --apply /tmp/engineering-source-review/web-design-guidelines
```

Absorbed updates compare the recorded upstream base, new upstream, and locally adapted target. They produce review packages first; applying a reconciled package preserves the single advanced-engineer entry and updates its source revision. Partial/local sources remain manual. Default sync continues to update standalone skills. See [SOURCES.md](skills/advanced-engineer/SOURCES.md) for conflict handling, limits, and adding a source.

## Verification And CI

This repository includes a GitHub Actions workflow that verifies selected skills can be installed through the public `skills` CLI:

- workflow file: `.github/workflows/verify-skills-install.yml`
- runs on pushes to `main` and on pull requests that change `skills/**` or the workflow file
- when run manually, you can choose which skills to verify
- the current whitelist verifies `advanced-engineer` and `writing-maestro`

The workflow runs:

```bash
npx skills add -y -g <owner>/<repo> --skill <skill-name>
```

The workflow also runs the offline absorbed-source integration tests, covering merge preservation, drift, conflicts, additions/deletions, entry-only sources, unsafe content, and rollback.

The public CLI job checks whether the public install path works. It does not mean every skill in the repo is published for public use.

## Recommended Workflow

1. Use `./scripts/new-skill.sh` to generate a minimal skill.
2. Write the trigger conditions, workflow, and reference entry points in `SKILL.md` first.
3. Add `references/`, `scripts/`, or `assets/` only when they provide real reuse.
4. Use `./scripts/install-skills.sh --dry-run` to confirm the install target is correct.
5. Install the skill locally and use it once to confirm the trigger description and workflow are actually usable.
6. If the skill comes from an external repository, add it to `skills/.remote-sources.yaml` and maintain it with the sync script.
