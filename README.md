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
    ├── install-skills.sh  # Install local skills into ~/.agents/skills
    └── new-skill.sh       # Bootstrap a new skill
```

## Conventions

- One skill per directory under `skills/`
- Use lowercase kebab-case for directory names, for example `android-release-notes`
- Keep each skill self-contained
- Put only reusable instructions and assets into a skill
- Keep `SKILL.md` concise and move large references into `references/` when needed

## Skills

| Skill | Purpose | Source |
| --- | --- | --- |
| [`writing-like-a-writer`](skills/writing-like-a-writer/SKILL.md) | Two-pass writing skill: remove AI writing tropes, then enforce clear and concise style rules (concise or detailed mode based on writing quality requirements). | Local custom skill |
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

Use symlinks instead of copies:

```bash
./scripts/install-skills.sh --mode link
```

Install into a custom skills directory:

```bash
./scripts/install-skills.sh --dest /path/to/skills
```

## Suggested Workflow

1. Create the skill with the bootstrap script.
2. Write the trigger description carefully in `SKILL.md` frontmatter.
3. Keep the body focused on workflow and decision rules.
4. Add `references/`, `scripts/`, or `assets/` only when they provide real reuse.
