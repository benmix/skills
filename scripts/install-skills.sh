#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
source_dir="$repo_root/skills"
dry_run=0
mode="copy"
clean_dest=0
dest_override=0
default_agents_dir="${AGENTS_HOME:-$HOME/.agents}/skills"

skill_names=()
dest_dirs=()

usage() {
  cat <<EOF
Usage: ./scripts/install-skills.sh [--dry-run] [--clean-dest] [--mode copy|link] [--dest PATH] [skill-name ...]

Install local skills from this repository into the local agents skills directory.

Options:
  --dry-run         Show what would be installed without writing files
  --clean-dest      Remove the destination skills directory before installing
  --mode MODE       Install mode: copy (default) or link
  --dest PATH       Install into a custom destination. Can be repeated
  -h, --help        Show this help
EOF
}

add_dest() {
  local candidate="$1"
  local existing

  [[ -n "$candidate" ]] || return 0

  for existing in "${dest_dirs[@]:-}"; do
    if [[ "$existing" == "$candidate" ]]; then
      return 0
    fi
  done

  dest_dirs+=("$candidate")
}

validate_dest_dir() {
  local dest_dir="$1"

  if [[ -z "$dest_dir" || "$dest_dir" == "/" ]]; then
    echo "Refusing to install into unsafe destination: $dest_dir" >&2
    return 1
  fi

  return 0
}

clean_dest_dir() {
  local dest_dir="$1"

  if ! validate_dest_dir "$dest_dir"; then
    return 1
  fi

  if [[ "$dry_run" -eq 1 ]]; then
    echo "Would remove destination directory: $dest_dir"
    return 0
  fi

  rm -rf "$dest_dir"
  echo "Removed destination directory: $dest_dir"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      dry_run=1
      shift
      ;;
    --clean-dest)
      clean_dest=1
      shift
      ;;
    --mode)
      mode="$2"
      shift 2
      ;;
    --dest)
      if [[ "$dest_override" -eq 0 ]]; then
        dest_dirs=()
        dest_override=1
      fi
      add_dest "$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      skill_names+=("$1")
      shift
      ;;
  esac
done

if [[ "$mode" != "copy" && "$mode" != "link" ]]; then
  echo "Mode must be one of: copy, link" >&2
  exit 1
fi

if [[ ! -d "$source_dir" ]]; then
  echo "Skills directory not found: $source_dir" >&2
  exit 1
fi

if [[ ${#dest_dirs[@]} -eq 0 ]]; then
  add_dest "$default_agents_dir"
fi

collect_skills() {
  local skill_name

  if [[ ${#skill_names[@]} -gt 0 ]]; then
    for skill_name in "${skill_names[@]}"; do
      if ! resolve_skill_name "$skill_name"; then
        return 1
      fi
    done
    return
  fi

  list_all_skills
}

list_all_skills() {
  find "$source_dir" -type f -name SKILL.md -print \
    | sed "s#^$source_dir/##; s#/SKILL\\.md\$##" \
    | sort
}

resolve_skill_name() {
  local requested="$1"
  local candidate
  local matches=()

  if [[ -f "$source_dir/$requested/SKILL.md" ]]; then
    printf '%s\n' "$requested"
    return 0
  fi

  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    if [[ "$(basename "$candidate")" == "$requested" ]]; then
      matches+=("$candidate")
    fi
  done < <(list_all_skills)

  if [[ ${#matches[@]} -eq 1 ]]; then
    printf '%s\n' "${matches[0]}"
    return 0
  fi

  if [[ ${#matches[@]} -gt 1 ]]; then
    echo "Ambiguous skill name: $requested" >&2
    printf 'Matches:\n' >&2
    printf '  %s\n' "${matches[@]}" >&2
    return 1
  fi

  echo "Missing skill: $requested" >&2
  return 1
}

install_skill_to_dest() {
  local skill_name="$1"
  local dest_dir="$2"
  local src="$source_dir/$skill_name"
  local dest="$dest_dir/$skill_name"
  local dest_parent

  if [[ ! -d "$src" ]]; then
    echo "Missing skill: $skill_name" >&2
    return 1
  fi

  if [[ ! -f "$src/SKILL.md" ]]; then
    echo "Skipping $skill_name: SKILL.md not found" >&2
    return 1
  fi

  if ! validate_dest_dir "$dest_dir"; then
    return 1
  fi

  if [[ "$dry_run" -eq 1 ]]; then
    echo "Would install $skill_name -> $dest ($mode)"
    return 0
  fi

  dest_parent="$(dirname "$dest")"
  mkdir -p "$dest_parent"
  rm -rf "$dest"

  if [[ "$mode" == "copy" ]]; then
    cp -R "$src" "$dest"
  else
    ln -s "$src" "$dest"
  fi

  echo "Installed $skill_name -> $dest"
}

resolved_skills=()
while IFS= read -r skill_name; do
  [[ -n "$skill_name" ]] || continue
  resolved_skills+=("$skill_name")
done < <(collect_skills)

if [[ ${#resolved_skills[@]} -eq 0 ]]; then
  echo "No skills found in $source_dir" >&2
  exit 1
fi

status=0
for dest_dir in "${dest_dirs[@]}"; do
  if [[ "$clean_dest" -eq 1 ]]; then
    if ! clean_dest_dir "$dest_dir"; then
      status=1
      continue
    fi
  fi

  for skill_name in "${resolved_skills[@]}"; do
    if ! install_skill_to_dest "$skill_name" "$dest_dir"; then
      status=1
    fi
  done
done

exit "$status"
