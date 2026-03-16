#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
manifest_file="$repo_root/skills/.remote-sources.yaml"
dry_run=0
ref_override=""
declare -a requested_skills=()

usage() {
  cat <<EOF
Usage: ./scripts/sync-remote-skills.sh [--dry-run] [--ref REF] [skill-name ...]

Sync non-local skills from their upstream repositories.

Options:
  --dry-run         Show what would be synced without network or file writes
  --ref REF         Override the manifest ref for every selected skill
  -h, --help        Show this help
EOF
}

if [[ ! -f "$manifest_file" ]]; then
  echo "Missing manifest: $manifest_file" >&2
  exit 1
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      dry_run=1
      shift
      ;;
    --ref)
      if [[ $# -lt 2 || -z "${2:-}" ]]; then
        echo "--ref requires a value" >&2
        exit 1
      fi
      ref_override="$2"
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
      requested_skills+=("$1")
      shift
      ;;
  esac
done

declare -a manifest_lines=()

current_skill_name=""
current_local_path=""
current_repo=""
current_ref=""
current_source_path=""
current_last_synced_commit=""

flush_manifest_entry() {
  if [[ -z "$current_skill_name" && -z "$current_local_path" && -z "$current_repo" && -z "$current_ref" && -z "$current_source_path" && -z "$current_last_synced_commit" ]]; then
    return 0
  fi

  if [[ -z "$current_skill_name" || -z "$current_local_path" || -z "$current_repo" || -z "$current_ref" || -z "$current_source_path" ]]; then
    echo "Invalid manifest entry in $manifest_file" >&2
    exit 1
  fi

  manifest_lines+=("$current_skill_name"$'\t'"$current_local_path"$'\t'"$current_repo"$'\t'"$current_ref"$'\t'"$current_source_path"$'\t'"$current_last_synced_commit")
  current_skill_name=""
  current_local_path=""
  current_repo=""
  current_ref=""
  current_source_path=""
  current_last_synced_commit=""
}

write_manifest() {
  local index
  local skill_name
  local local_path
  local repo
  local ref
  local source_path
  local last_synced_commit

  {
    printf 'skills:\n'
    for index in "${!manifest_lines[@]}"; do
      IFS=$'\t' read -r skill_name local_path repo ref source_path last_synced_commit <<< "${manifest_lines[$index]}"
      printf '  - skill_name: %s\n' "$skill_name"
      printf '    local_path: %s\n' "$local_path"
      printf '    repo: %s\n' "$repo"
      printf '    ref: %s\n' "$ref"
      printf '    source_path: %s\n' "$source_path"
      printf '    last_synced_commit: %s\n' "$last_synced_commit"
      if [[ "$index" -lt $((${#manifest_lines[@]} - 1)) ]]; then
        printf '\n'
      fi
    done
  } > "$manifest_file"
}

update_manifest_commit() {
  local target_skill_name="$1"
  local target_local_path="$2"
  local new_commit="$3"
  local index
  local skill_name
  local local_path
  local repo
  local ref
  local source_path
  local last_synced_commit

  for index in "${!manifest_lines[@]}"; do
    IFS=$'\t' read -r skill_name local_path repo ref source_path last_synced_commit <<< "${manifest_lines[$index]}"
    if [[ "$skill_name" == "$target_skill_name" && "$local_path" == "$target_local_path" ]]; then
      manifest_lines[$index]="$skill_name"$'\t'"$local_path"$'\t'"$repo"$'\t'"$ref"$'\t'"$source_path"$'\t'"$new_commit"
      write_manifest
      return 0
    fi
  done

  echo "Failed to update manifest entry for $target_skill_name ($target_local_path)" >&2
  exit 1
}

while IFS= read -r raw_line || [[ -n "$raw_line" ]]; do
  line="${raw_line%%#*}"
  [[ -n "${line//[[:space:]]/}" ]] || continue

  case "$line" in
    "skills:")
      continue
      ;;
    "  - skill_name: "*)
      flush_manifest_entry
      current_skill_name="${line#  - skill_name: }"
      ;;
    "  - local_path: "*)
      flush_manifest_entry
      current_local_path="${line#  - local_path: }"
      ;;
    "    skill_name: "*)
      current_skill_name="${line#    skill_name: }"
      ;;
    "    local_path: "*)
      current_local_path="${line#    local_path: }"
      ;;
    "    repo: "*)
      current_repo="${line#    repo: }"
      ;;
    "    ref: "*)
      current_ref="${line#    ref: }"
      ;;
    "    source_path: "*)
      current_source_path="${line#    source_path: }"
      ;;
    "    last_synced_commit:")
      current_last_synced_commit=""
      ;;
    "    last_synced_commit: "*)
      current_last_synced_commit="${line#    last_synced_commit: }"
      ;;
    "    synced_commit:")
      current_last_synced_commit=""
      ;;
    "    synced_commit: "*)
      current_last_synced_commit="${line#    synced_commit: }"
      ;;
    *)
      echo "Unsupported manifest syntax in $manifest_file: $raw_line" >&2
      exit 1
      ;;
  esac
done < "$manifest_file"

flush_manifest_entry

resolve_requested_skill() {
  local requested="$1"
  local line
  local skill_name
  local local_path
  local matches=()

  for line in "${manifest_lines[@]}"; do
    IFS=$'\t' read -r skill_name local_path _ <<< "$line"

    if [[ "$skill_name" == "$requested" || "$local_path" == "$requested" || "$(basename "$local_path")" == "$requested" ]]; then
      matches+=("$line")
    fi
  done

  if [[ ${#matches[@]} -eq 1 ]]; then
    printf '%s\n' "${matches[0]}"
    return 0
  fi

  if [[ ${#matches[@]} -gt 1 ]]; then
    echo "Ambiguous skill name: $requested" >&2
    printf 'Matches:\n' >&2
    for line in "${matches[@]}"; do
      IFS=$'\t' read -r skill_name local_path _ <<< "$line"
      printf '  %s (%s)\n' "$skill_name" "$local_path" >&2
    done
    return 1
  fi

  echo "Missing remote skill: $requested" >&2
  return 1
}

declare -a selected_lines=()

if [[ ${#requested_skills[@]} -eq 0 ]]; then
  selected_lines=("${manifest_lines[@]}")
else
  for requested in "${requested_skills[@]}"; do
    while IFS= read -r line; do
      [[ -n "$line" ]] || continue
      selected_lines+=("$line")
    done < <(resolve_requested_skill "$requested")
  done
fi

if [[ ${#selected_lines[@]} -eq 0 ]]; then
  echo "No remote skills selected." >&2
  exit 1
fi

if [[ "$dry_run" -eq 1 ]]; then
  for line in "${selected_lines[@]}"; do
    IFS=$'\t' read -r skill_name local_path repo ref source_path _ <<< "$line"
    if [[ -n "$ref_override" ]]; then
      ref="$ref_override"
    fi
    echo "Would sync $skill_name ($local_path) <- $repo:$ref/$source_path"
  done
  exit 0
fi

if ! command -v git >/dev/null 2>&1; then
  echo "git is required to sync remote skills." >&2
  exit 1
fi

tmp_root="$(mktemp -d "${TMPDIR:-/tmp}/skill-sync.XXXXXX")"
cleanup() {
  rm -rf "$tmp_root"
}
trap cleanup EXIT

for line in "${selected_lines[@]}"; do
  IFS=$'\t' read -r skill_name local_path repo ref source_path last_synced_commit <<< "$line"
  if [[ -n "$ref_override" ]]; then
    ref="$ref_override"
  fi

  repo_slug="${repo//@/-}"
  ref_slug="${ref//\//-}"
  local_slug="${local_path//\//-}"
  repo_dir="$tmp_root/${repo_slug}__${ref_slug}__${local_slug}"
  source_dir="$repo_dir/$source_path"
  target_dir="$repo_root/skills/$local_path"
  target_parent="$(dirname "$target_dir")"

  git init "$repo_dir" >/dev/null
  git -C "$repo_dir" remote add origin "https://github.com/$repo.git"
  git -C "$repo_dir" sparse-checkout init --cone >/dev/null
  git -C "$repo_dir" sparse-checkout set "$source_path" >/dev/null
  git -C "$repo_dir" fetch --depth 1 origin "$ref" >/dev/null
  git -C "$repo_dir" -c advice.detachedHead=false checkout FETCH_HEAD >/dev/null
  last_synced_commit="$(git -C "$repo_dir" rev-parse HEAD)"

  if [[ ! -d "$source_dir" ]]; then
    echo "Upstream path not found: $repo:$ref/$source_path" >&2
    exit 1
  fi

  mkdir -p "$target_parent"
  rm -rf "$target_dir"
  cp -R "$source_dir" "$target_dir"
  update_manifest_commit "$skill_name" "$local_path" "$last_synced_commit"

  echo "Synced $skill_name ($local_path) <- $repo:$ref/$source_path @ $last_synced_commit"
done
