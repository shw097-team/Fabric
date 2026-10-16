"""Real launcher routing tests; no provider request or worker spawn."""
import json
import os
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parent.parent
PWSH = Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe'


def resolve(*args):
    env = os.environ.copy()
    for name in ('CODEX_HOME', 'OPENCODEX_HOME'):
        env.pop(name, None)
    return subprocess.run([str(PWSH), '-NoProfile', '-File', str(ROOT / 'scripts/start-hgk-hermes.ps1'), '-Action', 'ResolveExecuteRoute', *args], env=env, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)


class ExecuteLunaRoute(unittest.TestCase):
    def test_oauth_additional_route_is_resolved(self):
        p = resolve('-ModelChain', 'gpt-6-luna')
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        route = json.loads(p.stdout)
        self.assertEqual(route['provider'], 'openai-codex')
        self.assertEqual(route['model'], 'gpt-6-luna')
        self.assertEqual(route['transport'], 'codex-native-oauth')
        self.assertFalse(route['automatic_selection'])

    def test_default_remains_original_route(self):
        p = resolve()
        self.assertEqual(p.returncode, 0, p.stderr)
        route = json.loads(p.stdout)
        self.assertEqual((route['provider'], route['model']), ('opencode-go', 'deepseek-v4.1-flash'))

    def test_provider_qualified_oauth_route(self):
        p = resolve('-ModelChain', 'openai-codex/gpt-6-luna')
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)['model'], 'gpt-6-luna')

    def test_primary_can_still_be_selected(self):
        p = resolve('-ModelChain', 'opencode-go/deepseek-v4.1-flash')
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)['transport'], 'sealed-opencodex-frontdoor')

    def test_wrong_provider_is_refused(self):
        p = resolve('-ModelChain', 'opencode-go/gpt-6-luna')
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('ERR_CODEX_WRITE_MODEL_NOT_SANCTIONED', p.stderr)

    def test_mixed_chain_is_refused(self):
        p = resolve('-ModelChain', 'deepseek-v4.1-flash,gpt-6-luna')
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('ERR_CODEX_WRITE_CHAIN_NOT_SINGLE', p.stderr)

    def test_older_model_is_not_aliased(self):
        p = resolve('-ModelChain', 'gpt-5.6-luna')
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('ERR_CODEX_WRITE_MODEL_NOT_SANCTIONED', p.stderr)

    def test_unknown_model_is_refused(self):
        p = resolve('-ModelChain', 'unknown-model')
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('ERR_CODEX_WRITE_MODEL_NOT_SANCTIONED', p.stderr)

    def test_conflicting_provider_pin_is_refused(self):
        p = resolve('-ModelChain', 'openai-codex/gpt-6-luna', '-ExecuteProvider', 'opencode-go')
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('ERR_EXECUTE_PROVIDER_CONFLICT', p.stderr)

    def test_unadmitted_oauth_writer_is_refused(self):
        # Exercise the real Write branch; it must refuse before credentials/network/spawn.
        env = os.environ.copy()
        env.pop('CODEX_HOME', None)
        env.pop('OPENCODEX_HOME', None)
        p = subprocess.run([str(PWSH), '-NoProfile', '-File', str(ROOT / 'scripts/start-hgk-hermes.ps1'),
                            '-Action', 'Write', '-ModelChain', 'gpt-6-luna', '-Prompt', 'No tools.'],
                           env=env, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('ERR_EXECUTE_OAUTH_BOUNDED_WRITER_ADMISSION_REQUIRED', p.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=2)
