# Sources and absorbed updates

The machine-readable inventory is [sources.json](sources.json). It records each former skill, its capability, original path, upstream repository/ref and last ingested revision where known, and the current internal target. Local sources record the repository revision preceding consolidation. Revision fields identify provenance; they do not claim the locally adapted text is identical to upstream.

The native advanced-engineer workflow, local custom workflows, and selected pstack practices are maintained locally. Full upstream skill imports can produce reviewable update proposals. Superseded router/duplicate handoff entries and partial adaptations are manual sources, so their originals cannot overwrite the consolidated design.

## Inspect provenance and planned updates

From the repository root:

```bash
./scripts/sync-remote-skills.sh advanced-engineer --dry-run
```

The standalone-skill manifest remains `skills/.remote-sources.yaml`. Absorbed sources live in `sources.json` and are never reinstalled as independent skills. The existing default sync command retains its standalone-skill behavior; explicitly select `advanced-engineer` or `--absorbed` to update absorbed sources.

## Stage upstream changes

```bash
./scripts/sync-remote-skills.sh advanced-engineer
./scripts/sync-remote-skills.sh --absorbed mattpocock--engineering--tdd
./scripts/sync-remote-skills.sh --absorbed web-design-guidelines --ref main --output /tmp/web-guidelines-review
```

A former skill name may select an unambiguous source. Use the full source ID for duplicates such as prototype and handoff. An output directory must be new. Omit it to use a fresh temporary directory; copy any proposals you want to retain before OS cleanup. Manual sources are listed but are not fetched or overwritten. `--force` is not needed or supported in this mode: staging always builds a fresh proposal.

For each full source, fetch the recorded base revision and the requested upstream ref. The updater reads permitted Git trees and blobs without checking out or reading excluded directories. It maps `SKILL.md` to `GUIDE.md`, maps compiled `AGENTS.md` to `REFERENCE.md`, strips entry frontmatter, and omits discovery metadata. Scripts/resources retain their relative structure and executable bits.

Each source gets a review package containing:

- `base/`: the normalized upstream at the recorded version.
- `upstream/`: the normalized new upstream.
- `local/`: the current absorbed implementation.
- `upstream.diff`: upstream changes since the recorded version.
- `merged/`: a three-way candidate preserving local edits where compatible.
- `proposal.json`: source identity, revisions, local fingerprints, and conflicts.
- `REVIEW.md`: reconciliation instructions.

Staging never changes the target or advances its source revision. Text, binary, add/add, and delete/modify conflicts remain review work. Binary and deletion conflicts may have no markers; inspect the conflict list as well as the candidate tree. A removed/empty upstream source stops staging instead of deleting local capabilities.

## Reconcile and apply

Review `upstream.diff` and edit `merged/` to the complete intended target. Adapt obsolete skill calls and cross-workflow paths to advanced-engineer's internal references, preserve scope and authorization rules, and run checks relevant to changed scripts or guidance. The updater cannot judge instruction semantics or guarantee that new upstream links remain valid.

```bash
./scripts/sync-remote-skills.sh --absorbed --apply /tmp/web-guidelines-review/web-design-guidelines
```

If the proposal listed conflicts, resolve them and explicitly acknowledge the reconciliation:

```bash
./scripts/sync-remote-skills.sh --absorbed --apply /tmp/review/mattpocock--engineering--tdd --conflicts-resolved
```

Apply rejects local/source-record drift, conflict markers, symlinks, and new discovery/configuration entries. It builds the replacement before touching the target, rolls back the target if applying fails, and advances `last_ingested_commit` only after successful replacement. This is per-source application, not an all-sources transaction. Keep source changes and their registry update in the same reviewed Git commit. Reinstall advanced-engineer separately when you want the installed copy updated.

## Add a source

Add a unique entry to `sources.json` with capability descriptions and target mappings. Full imports use `origin: upstream`, `repo`, `ref`, `source_path`, `last_ingested_commit`, `target`, and `sync_mode: tree` (a directory) or `entry` (one adapted entry document). Base revisions must be exact Git object IDs. Partial or manually synthesized capabilities use `sync_mode: manual` and explain which practices were selected; `targets` may list multiple documents. Never replace a partial-source record with a full-tree sync merely to automate it.
