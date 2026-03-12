#!/usr/bin/env bash

set -euo pipefail

dry_run=0

if [[ "${1:-}" == "--dry-run" ]]; then
  dry_run=1
  shift
fi

if [[ $# -lt 2 ]]; then
  echo "Usage: ./scripts/new-skill.sh [--dry-run] <skill-name> <description>" >&2
  exit 1
fi

skill_name="$1"
shift
description="$*"

if [[ ! "$skill_name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Skill name must be lowercase kebab-case, for example: release-notes" >&2
  exit 1
fi

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
skill_dir="$repo_root/skills/$skill_name"

if [[ -e "$skill_dir" ]]; then
  echo "Skill already exists: $skill_dir" >&2
  exit 1
fi

if [[ "$dry_run" -eq 1 ]]; then
  echo "Would create:"
  echo "  skills/$skill_name/SKILL.md"
  echo "  skills/$skill_name/agents/openai.yaml"
  exit 0
fi

mkdir -p "$skill_dir/agents"

cat > "$skill_dir/SKILL.md" <<EOF
---
name: $skill_name
description: $description
---

# $skill_name

## When to use

- Add the concrete triggers for this skill.
- Describe the task shapes that should cause the skill to be used.

## Workflow

1. Capture the user's goal and constraints.
2. Load only the references needed for the current task.
3. Execute the workflow with minimal context overhead.

## References

- Add links to any files in \`references/\` that should be opened on demand.

## Resources

- Put reusable scripts in \`scripts/\`
- Put load-on-demand docs in \`references/\`
- Put output templates or static files in \`assets/\`
EOF

cat > "$skill_dir/agents/openai.yaml" <<EOF
display_name: ${skill_name//-/ }
short_description: $description
default_prompt: Use the $skill_name skill for this task.
EOF

echo "Created skill: skills/$skill_name"
