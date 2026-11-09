#!/usr/bin/env python3
"""Stage and apply reviewed upstream changes inside a consolidated skill (stdlib only)."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile

BLOCKED = {'.agents-flow', '.agents-standard', '.git'}


def run(*args, **kwargs):
    return subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs).stdout


def safe_path(root, relative):
    path = PurePosixPath(relative)
    if path.is_absolute() or '..' in path.parts or not path.parts or BLOCKED.intersection(path.parts):
        raise ValueError(f'Unsafe path: {relative}')
    result = root.joinpath(*path.parts)
    if not result.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes root: {relative}')
    if BLOCKED.intersection(result.resolve().parts):
        raise ValueError(f'Excluded path: {relative}')
    return result


def read_tree(root):
    result = {}
    if not root.exists():
        return result
    if root.is_symlink():
        raise ValueError(f'Symlink target is unsupported: {root.name}')
    for current, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if d not in BLOCKED]
        if any((Path(current) / d).is_symlink() for d in dirs):
            raise ValueError('Symlink directory is unsupported')
        for name in files:
            p = Path(current) / name
            if p.is_symlink():
                raise ValueError('Symlink file is unsupported')
            result[p.relative_to(root).as_posix()] = (p.read_bytes(), p.stat().st_mode & 0o777)
    return result


def fingerprint(tree):
    return {p: hashlib.sha256(data).hexdigest() + f':{mode:o}' for p, (data, mode) in tree.items()}


def write_tree(root, tree):
    root.mkdir(parents=True, exist_ok=True)
    for name, (data, mode) in tree.items():
        target = safe_path(root, name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        target.chmod(mode)


def source_tree(repo, commit, source):
    """Read only permitted blobs; never check out or load excluded trees."""
    prefix = source['source_path'] if source['source_path'] != '.' else ''
    if prefix:
        safe_path(Path('/tmp'), prefix)
    result = {}

    def visit(tree_path, relative_dir=''):
        spec = commit + (':' + tree_path if tree_path else ':')
        listing = run('git', '-C', str(repo), 'ls-tree', '-z', spec).split(b'\0')
        for record in listing:
            if not record:
                continue
            metadata, raw_name = record.split(b'\t', 1)
            mode, kind, oid = metadata.decode().split()
            name = raw_name.decode()
            if name in BLOCKED or not relative_dir and name == 'agents':
                continue
            relative = relative_dir + name
            safe_path(Path('/tmp'), relative)
            if kind == 'tree':
                if source['sync_mode'] != 'entry':
                    visit('/'.join(filter(None, [tree_path, name])), relative + '/')
                continue
            if kind != 'blob' or mode == '120000':
                raise ValueError(f'Unsupported upstream file type: {relative}')
            if source['sync_mode'] == 'entry' and relative != 'SKILL.md':
                continue
            data = run('git', '-C', str(repo), 'cat-file', 'blob', oid)
            target_name = relative
            if name == 'SKILL.md':
                target_name = str(PurePosixPath(relative).with_name('GUIDE.md'))
                text = data.decode()
                if text.startswith('---\n'):
                    text = text.split('---', 2)[2].lstrip()
                data = text.encode()
            if name == 'AGENTS.md':
                target_name = str(PurePosixPath(relative).with_name('REFERENCE.md'))
            if target_name.endswith('.md'):
                data = data.replace(b'](SKILL.md)', b'](GUIDE.md)').replace(b'](./SKILL.md)', b'](GUIDE.md)').replace(b'`AGENTS.md`', b'`REFERENCE.md`').replace(b'](AGENTS.md)', b'](REFERENCE.md)')
            if source['sync_mode'] == 'entry':
                target_name = 'entry.md'
            if target_name in result:
                raise ValueError(f'Normalized upstream path collision: {target_name}')
            result[target_name] = (data, 0o755 if mode == '100755' else 0o644)

    visit(prefix)
    if not result:
        raise ValueError(f'Upstream source is empty or removed: {source["id"]}')
    return result


def local_tree(skill, source):
    target = safe_path(skill, source['target'])
    if source['sync_mode'] == 'entry':
        if not target.is_file() or target.is_symlink():
            raise ValueError('Missing or symlink entry target')
        return {'entry.md': (target.read_bytes(), target.stat().st_mode & 0o777)}
    return read_tree(target)


def merge_trees(base, local, upstream):
    result, conflicts = {}, []
    for name in sorted(base.keys() | local.keys() | upstream.keys()):
        old, ours, theirs = base.get(name), local.get(name), upstream.get(name)
        if theirs == old or ours == theirs:
            chosen = ours
        elif ours == old:
            chosen = theirs
        elif ours and old and theirs and b'\0' not in ours[0] + old[0] + theirs[0]:
            with tempfile.TemporaryDirectory(prefix='skill-merge-') as temp:
                paths = [Path(temp) / n for n in ['local', 'base', 'upstream']]
                for p, item in zip(paths, [ours, old, theirs]):
                    p.write_bytes(item[0])
                proc = subprocess.run(['git', 'merge-file', '-p', '-L', 'LOCAL', '-L', 'BASE', '-L', 'UPSTREAM', *map(str, paths)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if not 0 <= proc.returncode <= 127:
                    raise ValueError(f'Merge failed: {name}')
                chosen = (proc.stdout, theirs[1] if ours[1] == old[1] else ours[1])
                if proc.returncode or ours[1] != old[1] and theirs[1] != old[1] and ours[1] != theirs[1]:
                    conflicts.append(name)
        else:
            chosen = ours
            conflicts.append(name)
        if chosen is not None:
            result[name] = chosen
    return result, conflicts


def stage(skill, source, repo, new_commit, output):
    if output.exists():
        raise ValueError('Proposal directory already exists; choose a new output')
    old_commit = source['last_ingested_commit']
    base = source_tree(repo, old_commit, source)
    upstream = source_tree(repo, new_commit, source)
    local = local_tree(skill, source)
    merged, conflicts = merge_trees(base, local, upstream)
    # Output contains permitted, normalized trees only; no git diff across excluded paths.
    for label, tree in [('base', base), ('upstream', upstream), ('local', local), ('merged', merged)]:
        write_tree(output / label, tree)
    diff = subprocess.run(['git', 'diff', '--no-index', '--', str(output / 'base'), str(output / 'upstream')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if diff.returncode not in (0, 1):
        raise ValueError('Cannot generate upstream diff')
    (output / 'upstream.diff').write_bytes(diff.stdout)
    proposal = {'schema_version': 1, 'source_id': source['id'], 'source_record': source, 'base_commit': old_commit, 'upstream_commit': new_commit, 'local_fingerprint': fingerprint(local), 'conflicts': conflicts}
    (output / 'proposal.json').write_text(json.dumps(proposal, indent=2) + '\n')
    (output / 'REVIEW.md').write_text('# Review this absorption proposal\n\nCompare upstream.diff, local/, and merged/. Reconcile old skill calls and paths with advanced-engineer internal procedures; preserve integration rules and authorization boundaries. Resolve every listed conflict, including binary or delete/modify conflicts that have no text markers. Edit merged/ to the intended complete target tree. Apply only after checking the result. No live skill or source version has changed.\n\nConflicts: ' + (', '.join(conflicts) or 'none') + '\n')
    return proposal


def validate_merged(tree):
    for name, (data, _) in tree.items():
        parts = PurePosixPath(name).parts
        if BLOCKED.intersection(parts) or 'agents' in parts or parts[-1] in {'SKILL.md', 'AGENTS.md'}:
            raise ValueError(f'Discovery/configuration entry is forbidden in absorbed content: {name}')
        if re.search(rb'(?m)^(<<<<<<<|=======|>>>>>>>)(?: |$)', data):
            raise ValueError(f'Unresolved conflict markers: {name}')


def apply(skill, manifest_path, manifest, proposal_dir, conflicts_resolved=False):
    if BLOCKED.intersection(proposal_dir.resolve().parts):
        raise ValueError('Excluded proposal path')
    proposal = json.loads((proposal_dir / 'proposal.json').read_text())
    source = next((s for s in manifest['sources'] if s['id'] == proposal['source_id']), None)
    if not source or source != proposal['source_record']:
        raise ValueError('Source record changed since staging; restage first')
    if source['sync_mode'] not in {'tree', 'entry'}:
        raise ValueError('This source is manually maintained')
    if fingerprint(local_tree(skill, source)) != proposal['local_fingerprint']:
        raise ValueError('Local target changed since staging; restage first')
    if proposal['conflicts'] and not conflicts_resolved:
        raise ValueError('Resolve listed conflicts and pass --conflicts-resolved after reviewing them')
    merged = read_tree(proposal_dir / 'merged')
    if not merged:
        raise ValueError('An empty merged tree cannot be applied')
    validate_merged(merged)
    if not re.fullmatch('[0-9a-f]{40,64}', proposal['upstream_commit']):
        raise ValueError('Invalid upstream commit')
    target = safe_path(skill, source['target'])
    if source['sync_mode'] == 'entry' and set(merged) != {'entry.md'}:
        raise ValueError('Entry-only source must contain exactly entry.md')
    # Build the replacement completely before touching the current target.
    with tempfile.TemporaryDirectory(prefix='.absorb-', dir=target.parent) as temp:
        temp = Path(temp)
        staged = temp / 'replacement'
        write_tree(staged, merged)
        backup = temp / 'backup'
        moved = False
        try:
            os.replace(target, backup)
            moved = True
            replacement = staged / 'entry.md' if source['sync_mode'] == 'entry' else staged
            os.replace(replacement, target)
            source['last_ingested_commit'] = proposal['upstream_commit']
            updated = json.dumps(manifest, ensure_ascii=False, indent=2) + '\n'
            pending = temp / 'sources.json'
            pending.write_text(updated)
            os.replace(pending, manifest_path)
        except BaseException:
            source['last_ingested_commit'] = proposal['base_commit']
            if moved:
                if target.is_dir():
                    shutil.rmtree(target)
                elif target.exists():
                    target.unlink()
                os.replace(backup, target)
            raise
    print(f'APPLIED {source["id"]} -> {source["target"]} ({source["last_ingested_commit"][:12]})')


def fetch_repo(source, destination, ref):
    if not re.fullmatch(r'[\w.-]+/[\w.-]+', source['repo']):
        raise ValueError('Expected an owner/repo source')
    run('git', 'init', '-q', str(destination))
    run('git', '-C', str(destination), 'remote', 'add', 'origin', 'https://github.com/' + source['repo'] + '.git')
    for revision in dict.fromkeys([source['last_ingested_commit'], ref]):
        if revision.startswith('-'):
            raise ValueError('Invalid ref')
        run('git', '-C', str(destination), 'fetch', '--filter=blob:none', '--depth=1', 'origin', revision)
    return run('git', '-C', str(destination), 'rev-parse', 'FETCH_HEAD').decode().strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sources', nargs='*', help='Source IDs or former skill names; default: all sources')
    parser.add_argument('--dry-run', action='store_true', help='List provenance and sync plans without network/writes')
    parser.add_argument('--ref', help='Override upstream ref for staging')
    parser.add_argument('--output', type=Path, help='New review-package directory (default: OS temporary directory)')
    parser.add_argument('--apply', type=Path, metavar='PROPOSAL', help='Apply a reviewed source proposal directory')
    parser.add_argument('--conflicts-resolved', action='store_true', help='Acknowledge all listed conflicts have been reconciled')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    skill = root / 'skills/advanced-engineer'
    manifest_path = skill / 'sources.json'
    manifest = json.loads(manifest_path.read_text())
    ids = [s['id'] for s in manifest['sources']]
    if manifest['schema_version'] != 1 or len(ids) != len(set(ids)):
        raise ValueError('Invalid source registry schema or duplicate IDs')
    for source in manifest['sources']:
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', source['id']):
            raise ValueError('Invalid source ID')
        if source['sync_mode'] not in {'tree', 'entry', 'manual'} or source['origin'] not in {'local', 'upstream'}:
            raise ValueError('Invalid source mode or origin')
        for target in ([source['target']] if 'target' in source else source.get('targets', [])):
            safe_path(skill, target)
        if source['origin'] == 'upstream' and not re.fullmatch(r'[0-9a-f]{40,64}', source['last_ingested_commit']):
            raise ValueError('Recorded upstream revision must be an exact commit')
    if args.conflicts_resolved and not args.apply:
        raise ValueError('--conflicts-resolved requires --apply')
    if args.apply:
        if args.dry_run or args.sources or args.ref or args.output:
            raise ValueError('--apply cannot be combined with selection/staging flags')
        apply(skill, manifest_path, manifest, args.apply.resolve(), args.conflicts_resolved)
        return
    selected = []
    if not args.sources:
        selected = manifest['sources']
    else:
        for name in args.sources:
            matches = [s for s in manifest['sources'] if name in {s['id'], s.get('former_path'), Path(s.get('former_path', '')).name}]
            if len(matches) != 1:
                raise ValueError(f'Unknown or ambiguous source: {name}; use its full source ID')
            if matches[0] not in selected:
                selected.append(matches[0])
    if args.dry_run:
        for source in selected:
            origin = source.get('repo', 'local') + ':' + source['source_path']
            print(f'{source["id"]}: {origin} -> {source.get("target", source.get("targets"))} [{source["sync_mode"]}]')
        return
    remote = [s for s in selected if s['origin'] == 'upstream' and s['sync_mode'] != 'manual']
    for s in selected:
        if s not in remote:
            print(f'MANUAL {s["id"]}: provenance recorded; target remains locally maintained')
    if not remote:
        return
    if args.output:
        output = args.output.resolve()
        if BLOCKED.intersection(output.parts):
            raise ValueError('Excluded output path')
        output.mkdir(parents=True, exist_ok=False)
    else:
        output = Path(tempfile.mkdtemp(prefix='absorbed-skill-review-'))
    print(f'Review packages: {output}', flush=True)
    with tempfile.TemporaryDirectory(prefix='absorbed-upstream-') as temp:
        repos = {}
        for source in remote:
            key = (source['repo'], source['last_ingested_commit'], args.ref or source['ref'])
            if key not in repos:
                checkout = Path(temp) / str(len(repos))
                repos[key] = (checkout, fetch_repo(source, checkout, key[2]))
            repo, commit = repos[key]
            proposal = stage(skill, source, repo, commit, output / source['id'])
            print(f'STAGED {source["id"]}: {len(proposal["conflicts"])} conflicts; {commit[:12]}')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        # Do not print subprocess output that may contain transport credentials.
        print(f'ERROR: {error}', file=sys.stderr)
        sys.exit(1)
