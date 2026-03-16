# Personal Agent Skills

This repository stores my custom agent skills.

## Layout

```text
.
├── skills/
│   ├── .system/           # Imported or system-level skills
│   │   └── <skill-name>/
│   └── <skill-name>/      # Project or custom skills
│       ├── SKILL.md
│       └── agents/
│           └── openai.yaml
└── scripts/
    ├── install-skills.sh      # Install local skills into ~/.agents/skills
    ├── new-skill.sh           # Bootstrap a new skill
    └── sync-remote-skills.sh  # Sync imported skills from upstream repos
```

## Conventions

- One skill per directory under `skills/`
- Use lowercase kebab-case for directory names, for example `android-release-notes`
- Keep each skill self-contained
- Put only reusable instructions and assets into a skill
- Keep `SKILL.md` concise and move large references into `references/` when needed
- Track non-local skills in `skills/.remote-sources.yaml` so they can be synced from upstream

## Skills

| Skill | Purpose | Source |
| --- | --- | --- |
| [`writing-maestro`](skills/writing-maestro/SKILL.md) | Two-pass writing skill: remove AI writing tropes, then enforce clear and concise style rules (concise or detailed mode based on writing quality requirements). | Local custom skill |
| [`advanced-engineer`](skills/advanced-engineer/SKILL.md) | Systematic engineering workflow for debugging, root-cause analysis, minimal patches, and verified resolution of production issues. | Local custom skill |
| [`verification-before-completion`](skills/verification-before-completion/SKILL.md) | Verification gate skill used before claiming completion, fixes, or passing status; requires fresh command evidence before any success claim. | [obra/superpowers](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md) |
| [`systematic-debugging`](skills/systematic-debugging/SKILL.md) | Root-cause-first debugging workflow for bugs, test failures, and unexpected behavior; prevents proposing fixes before investigation. | [obra/superpowers](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md) |
| [`find-skills`](skills/.system/find-skills/SKILL.md) | Helps discover and install skills when a user asks for capabilities or workflow support. | [vercel-labs/skills](https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md) |
| [`skill-creator`](skills/.system/skill-creator/SKILL.md) | Guide and tooling reference for creating or updating skills. | [openai/skills](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md) |
| [`skill-installer`](skills/.system/skill-installer/SKILL.md) | Guide and helper scripts for installing skills from curated sources or GitHub paths. | [openai/skills](https://github.com/openai/skills/blob/main/skills/.system/skill-installer/SKILL.md) |
| [`vercel-composition-patterns`](skills/vercel-composition-patterns/SKILL.md) | React composition patterns for component architecture, compound components, and scalable APIs. | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/blob/main/skills/composition-patterns/README.md) |
| [`vercel-react-best-practices`](skills/vercel-react-best-practices/SKILL.md) | React and Next.js performance optimization guidance from Vercel Engineering. | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/README.md) |
| [`web-design-guidelines`](skills/web-design-guidelines/SKILL.md) | UI and accessibility review guidance for checking web interfaces against design standards. | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/blob/main/skills/web-design-guidelines/SKILL.md) |

## Create A Skill

Run:

```bash
./scripts/new-skill.sh my-skill "What this skill does and when it should be used"
```

Preview without writing files:

```bash
./scripts/new-skill.sh --dry-run my-skill "What this skill does and when it should be used"
```

This creates:

- `skills/my-skill/SKILL.md`
- `skills/my-skill/agents/openai.yaml`

Then fill in the workflow, references, scripts, or assets that the skill needs.

## Install Skills

Install all local skills into `~/.agents/skills`, including `.system/` skills:

```bash
./scripts/install-skills.sh
```

Install one skill only:

```bash
./scripts/install-skills.sh my-skill
```

Install a system skill by short name or path:

```bash
./scripts/install-skills.sh skill-installer
./scripts/install-skills.sh .system/skill-installer
```

Preview changes without writing files:

```bash
./scripts/install-skills.sh --dry-run
```

Clear the destination skills directory before reinstalling everything:

```bash
./scripts/install-skills.sh --clean-install-dir
```

Preview a clean reinstall without writing files:

```bash
./scripts/install-skills.sh --dry-run --clean-install-dir
```

Use symlinks instead of copies:

```bash
./scripts/install-skills.sh --mode link
```

Install into a custom skills directory:

```bash
./scripts/install-skills.sh --install-dir /path/to/skills
```

## Sync Remote Skills

Sync all non-local skills from their source repositories:

```bash
./scripts/sync-remote-skills.sh
```

Sync one skill only:

```bash
./scripts/sync-remote-skills.sh verification-before-completion
./scripts/sync-remote-skills.sh .system/skill-installer
```

Preview what would be synced without any network or file writes:

```bash
./scripts/sync-remote-skills.sh --dry-run
```

Temporarily sync from a different branch or tag:

```bash
./scripts/sync-remote-skills.sh --ref main web-design-guidelines
```

The source manifest lives at `skills/.remote-sources.yaml`:

```yaml
skills:
  - skill_name: verification-before-completion
    local_path: verification-before-completion
    repo: obra/superpowers
    ref: main
    source_path: skills/verification-before-completion
    last_synced_commit: 0123456789abcdef0123456789abcdef01234567
```

`last_synced_commit` is maintained by the sync script and records the exact upstream commit last copied into this repo.

Add an entry there for any imported skill that should support upstream sync.

## Verify skills install

This repository includes a GitHub Actions workflow that automatically validates whitelisted skills can be installed through the public `skills` CLI.

Workflow file:

- `.github/workflows/verify-skills-install.yml`

Behavior:

- Runs automatically on pushes to `main` and on pull requests that touch `skills/**` or the workflow file
- Uses a fixed whitelist in the workflow, so only explicitly approved skills are verified
- Leave the `skills` input empty when running manually to verify all whitelisted skills
- Provide a comma-separated or newline-separated list such as `writing-maestro,advanced-engineer` to verify only those whitelisted skills
- The workflow calls `npx skills add -y -g <owner>/<repo> --skill <skill-name>` once per selected skill

This checks the same public install path a user would run manually, but treats it as CI verification rather than publication.

## Suggested Workflow

1. Create the skill with the bootstrap script.
2. Write the trigger description carefully in `SKILL.md` frontmatter.
3. Keep the body focused on workflow and decision rules.
4. Add `references/`, `scripts/`, or `assets/` only when they provide real reuse.
