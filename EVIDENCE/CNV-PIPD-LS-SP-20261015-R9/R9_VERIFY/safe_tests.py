import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path('C:/Projects/Agent_Workspace/PIPD/worktrees/r8-wt')
sys.path.insert(0, str(ROOT / 'src'))
original_run = subprocess.run

def readonly_git_run(command, *args, **kwargs):
    if isinstance(command, (list, tuple)) and command and Path(str(command[0])).stem.lower() == 'git':
        allowed = {'-C', 'status', 'diff', 'rev-parse', 'ls-files', 'show', 'log', 'cat-file', 'ls-tree', 'config'}
        subcommand = str(command[3] if len(command) > 3 and command[1] == '-C' else command[1])
        if subcommand not in allowed or subcommand == 'config':
            raise RuntimeError('R9V_FORBIDDEN_GIT_WRITE: ' + repr(command))
    return original_run(command, *args, **kwargs)

subprocess.run = readonly_git_run
modules = []
for filename in ('test_s4ext_trace_closure.py', 'test_tooling_executes.py'):
    spec = importlib.util.spec_from_file_location(filename[:-3], ROOT / 'tests' / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    modules.append(module)
suite = unittest.TestSuite([
    modules[0].LegalTraceStillPassesTests('test_real_trace_link_is_legal_beside_its_endpoints'),
    modules[1].TestToolingExecutes('test_cli_smoke_runs'),
])
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
