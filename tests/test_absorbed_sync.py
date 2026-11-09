"""Offline integration checks for absorbed upstream updates and protected local state."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('absorbed', Path(__file__).resolve().parents[1] / 'scripts/sync-absorbed-skills.py')
sync = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync)


class AbsorbedSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='absorbed-sync-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'upstream'
        self.repo.mkdir()
        self.git('init', '-q')
        self.git('config', 'core.fsmonitor', 'false')
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('config', 'user.name', 'Fixture')
        self.src = self.repo / 'skill'
        self.src.mkdir()
        (self.src / 'SKILL.md').write_text('---\nname: fixture\ndescription: fixture\n---\n\n# Fixture\n\nfirst\n\nsecond\n')
        (self.src / 'resource.txt').write_text('old resource\n')
        self.base = self.commit()
        self.skill = self.root / 'advanced-engineer'
        self.target = self.skill / 'references/fixture'
        self.source = {'id': 'fixture', 'origin': 'upstream', 'repo': 'fixture/repo', 'ref': 'main', 'source_path': 'skill', 'target': 'references/fixture', 'sync_mode': 'tree', 'last_ingested_commit': self.base}
        sync.write_tree(self.target, sync.source_tree(self.repo, self.base, self.source))
        self.registry = self.skill / 'sources.json'
        self.manifest = {'schema_version': 1, 'skill': 'advanced-engineer', 'sources': [self.source]}
        self.registry.write_text(json.dumps(self.manifest))

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.repo), *args], stderr=subprocess.DEVNULL).decode().strip()

    def commit(self):
        self.git('add', '.')
        self.git('commit', '-qm', 'fixture change')
        return self.git('rev-parse', 'HEAD')

    def review(self, output):
        assessment = json.loads((output / 'semantic-review.json').read_text())
        for name, check in assessment['checks'].items():
            check.update(preserved=True, evidence=f'Fixture comparison confirms {name}; only the requested resource update is introduced.')
        (output / 'semantic-review.json').write_text(json.dumps(assessment))
        sync.seal_review(output)

    def proposal(self):
        (self.src / 'resource.txt').write_text('new resource\n')
        new = self.commit()
        output = self.root / 'proposal'
        proposal = sync.stage(self.skill, self.source, self.repo, new, output)
        if not proposal['conflicts']:
            self.review(output)
        return output, proposal

    def test_stage_then_apply_preserves_local_adaptation_and_advances_version(self):
        guide = self.target / 'GUIDE.md'
        guide.write_text(guide.read_text().replace('first', 'local adaptation'))
        before = guide.read_bytes()
        output, proposal = self.proposal()
        self.assertEqual(guide.read_bytes(), before)
        self.assertEqual(self.source['last_ingested_commit'], self.base)
        self.assertFalse((self.target / 'SKILL.md').exists())
        sync.apply(self.skill, self.registry, self.manifest, output)
        self.assertIn('local adaptation', guide.read_text())
        self.assertEqual((self.target / 'resource.txt').read_text(), 'new resource\n')
        self.assertEqual(json.loads(self.registry.read_text())['sources'][0]['last_ingested_commit'], proposal['upstream_commit'])

    def test_apply_rejects_local_drift_without_overwrite(self):
        output, _ = self.proposal()
        (self.target / 'resource.txt').write_text('new user edit\n')
        with self.assertRaisesRegex(ValueError, 'Local target changed'):
            sync.apply(self.skill, self.registry, self.manifest, output)
        self.assertEqual((self.target / 'resource.txt').read_text(), 'new user edit\n')
        self.assertEqual(self.source['last_ingested_commit'], self.base)

    def test_text_conflicts_require_resolution(self):
        (self.target / 'resource.txt').write_text('local conflicting change\n')
        output, proposal = self.proposal()
        self.assertEqual(proposal['conflicts'], ['resource.txt'])
        with self.assertRaisesRegex(ValueError, 'Resolve listed conflicts'):
            sync.apply(self.skill, self.registry, self.manifest, output)
        with self.assertRaisesRegex(ValueError, 'Unresolved conflict markers'):
            sync.apply(self.skill, self.registry, self.manifest, output, True)
        (output / 'merged/resource.txt').write_text('reviewed resolution\n')
        self.review(output)
        sync.apply(self.skill, self.registry, self.manifest, output, True)
        self.assertEqual((self.target / 'resource.txt').read_text(), 'reviewed resolution\n')

    def test_nonoverlapping_text_edits_merge_without_losing_either(self):
        base = {'doc.md': (b'first\n' + b'middle\n' * 12 + b'last\n', 0o644)}
        local = {'doc.md': (base['doc.md'][0].replace(b'first', b'local first'), 0o644)}
        upstream = {'doc.md': (base['doc.md'][0].replace(b'last', b'upstream last'), 0o644)}
        merged, conflicts = sync.merge_trees(base, local, upstream)
        self.assertEqual(conflicts, [])
        self.assertIn(b'local first', merged['doc.md'][0])
        self.assertIn(b'upstream last', merged['doc.md'][0])

    def test_deletion_and_addition_propagate_without_recreating_entry(self):
        (self.src / 'resource.txt').unlink()
        (self.src / 'new.txt').write_text('added\n')
        new = self.commit()
        output = self.root / 'proposal'
        sync.stage(self.skill, self.source, self.repo, new, output)
        self.review(output)
        sync.apply(self.skill, self.registry, self.manifest, output)
        self.assertFalse((self.target / 'resource.txt').exists())
        self.assertEqual((self.target / 'new.txt').read_text(), 'added\n')
        self.assertEqual(list(self.skill.rglob('SKILL.md')), [])

    def test_symlinks_and_unsafe_target_are_rejected(self):
        (self.src / 'link').symlink_to('resource.txt')
        new = self.commit()
        with self.assertRaisesRegex(ValueError, 'Unsupported upstream file type'):
            sync.source_tree(self.repo, new, self.source)
        with self.assertRaisesRegex(ValueError, 'Unsafe path'):
            sync.safe_path(self.skill, '../outside')

    def test_registry_drift_and_discovery_entries_are_rejected(self):
        output, _ = self.proposal()
        self.source['ref'] = 'another-branch'
        with self.assertRaisesRegex(ValueError, 'Source record changed'):
            sync.apply(self.skill, self.registry, self.manifest, output)
        self.source['ref'] = 'main'
        (output / 'merged/SKILL.md').write_text('unexpected skill')
        with self.assertRaisesRegex(ValueError, 'Discovery/configuration'):
            sync.apply(self.skill, self.registry, self.manifest, output)

    def test_manifest_write_failure_rolls_back_target(self):
        output, _ = self.proposal()
        before = sync.fingerprint(sync.local_tree(self.skill, self.source))
        with self.assertRaises(OSError):
            sync.apply(self.skill, self.skill / 'missing/sources.json', self.manifest, output)
        self.assertEqual(sync.fingerprint(sync.local_tree(self.skill, self.source)), before)
        self.assertEqual(json.loads(self.registry.read_text())['sources'][0]['last_ingested_commit'], self.base)
        self.assertEqual(self.source['last_ingested_commit'], self.base)

    def test_missing_or_stale_semantic_review_blocks_even_clean_merge(self):
        output, _ = self.proposal()
        review = json.loads((output / 'semantic-review.json').read_text())
        review['checks']['required_steps_and_order']['preserved'] = False
        (output / 'semantic-review.json').write_text(json.dumps(review))
        with self.assertRaisesRegex(ValueError, 'Semantic review must confirm'):
            sync.apply(self.skill, self.registry, self.manifest, output)
        self.review(output)
        (output / 'merged/resource.txt').write_text('unreviewed later edit\n')
        with self.assertRaisesRegex(ValueError, 'missing or stale'):
            sync.apply(self.skill, self.registry, self.manifest, output)
        self.assertEqual((self.target / 'resource.txt').read_text(), 'old resource\n')
        self.assertEqual(self.source['last_ingested_commit'], self.base)

    def test_entry_only_source_updates_one_existing_document(self):
        source = copy.deepcopy(self.source)
        source.update(sync_mode='entry', target='references/review.md')
        target = self.skill / source['target']
        target.write_bytes(sync.source_tree(self.repo, self.base, source)['entry.md'][0])
        manifest = {'schema_version': 1, 'sources': [source]}
        (self.src / 'SKILL.md').write_text((self.src / 'SKILL.md').read_text().replace('second', 'upstream revision'))
        new = self.commit()
        output = self.root / 'entry-proposal'
        sync.stage(self.skill, source, self.repo, new, output)
        self.review(output)
        sync.apply(self.skill, self.registry, manifest, output)
        self.assertIn('upstream revision', target.read_text())
        self.assertTrue((self.target / 'GUIDE.md').exists())


class SemanticBaselineTests(unittest.TestCase):
    def test_absorbed_bodies_match_recorded_reviewed_content(self):
        root = Path(__file__).resolve().parents[1]
        skill = root / 'skills/advanced-engineer'
        registry = json.loads((skill / 'sources.json').read_text())
        for source in registry['sources']:
            if 'semantic_baseline' not in source:
                continue
            with self.subTest(source=source['id']):
                target = skill / source['target']
                if source.get('last_semantic_review'):
                    current = sync.local_tree(skill, source)
                    self.assertEqual(sync.fingerprint(current), source['last_semantic_review']['reviewed_fingerprint'])
                else:
                    if target.is_dir():
                        target = target / 'GUIDE.md'
                    self.assertEqual(sync.hashlib.sha256(target.read_bytes()).hexdigest(), source['semantic_baseline']['restored_target_sha256'])


if __name__ == '__main__':
    unittest.main()
