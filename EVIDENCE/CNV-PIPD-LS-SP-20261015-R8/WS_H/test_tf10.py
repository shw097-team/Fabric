"""Offline regression and negative controls; writes no repository files."""
import json
import os
import pathlib
import subprocess
import sys
import types
import unittest

ROOT = pathlib.Path(__file__).resolve().parent
WT = 'C:/Projects/wt-cnv-r7'
sys.dont_write_bytecode = True

def load(path):
    module = types.ModuleType(path.stem)
    module.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module

if '--legacy-red' in sys.argv:
    print('OFFLINE REPRO: API functions replaced with read-only local git object reads; inherited API/remote labels below are NOT network requests.')
    old = load(ROOT.parent.parent / 'CNV-PIPD-LS-SP-20261015-R7/selfcheck/round_selfcheck.py')
    def git(*args):
        return subprocess.check_output(['git', '--no-optional-locks', '-C', WT, *args],
            env=dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_NO_LAZY_FETCH='1', GIT_TERMINAL_PROMPT='0'))
    def api(path):
        rev = path.split('/git/trees/')[1].split('?')[0]
        entries = []
        for row in git('ls-tree', '-r', '-z', rev).split(b'\0'):
            if row:
                meta, name = row.split(b'\t', 1)
                mode, typ, sha = meta.decode().split()
                entries.append(dict(path=name.decode(), type=typ, sha=sha))
        return dict(tree=entries, truncated=False)
    old.api_json = api
    old.contents_bytes = lambda path: git('show', 'HEAD:' + old.PKT_P + 'PACKET_MANIFEST.json')
    results = []
    for check in (old.check_2, old.check_3):
        text, ok, _ = check()
        print(text)
        results.append(ok)
    print('LEGACY_OFFLINE_REPRO:', results, '(False values reproduce TF-10)')
    sys.exit(0 if all(results) else 1)

class Regression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h = load(ROOT / 'round_selfcheck_r8.py')
        cls.s = cls.h.Snapshot(WT)

    def test_live_inventory(self):
        self.assertTrue(self.h.check_2(self.s)[0])

    def test_live_manifest(self):
        self.assertTrue(self.h.check_3(self.s)[0])

    def test_equal_count_wrong_set_is_rejected(self):
        doc = json.loads(self.s.manifest_raw)
        doc['tracked_inventory'][0] = self.s.prefix + 'not-a-real-blob'
        self.assertFalse(self.h.manifest_result(self.s, doc)[0])

    def test_empty_inventory_is_rejected(self):
        self.assertFalse(self.h.inventory_result(self.s, {})[0])

    def test_wrong_prefix_is_rejected(self):
        with self.assertRaises(ValueError):
            self.h.Snapshot(WT, self.s.prefix + 'not-a-packet/')

    def test_traversal_is_rejected(self):
        self.assertFalse(self.h.safe_path(self.s.prefix + '../escape', self.s.prefix))

    def test_git_write_is_refused(self):
        with self.assertRaises(ValueError):
            self.s.git('push', 'origin', 'HEAD')

if __name__ == '__main__':
    unittest.main(verbosity=2)
