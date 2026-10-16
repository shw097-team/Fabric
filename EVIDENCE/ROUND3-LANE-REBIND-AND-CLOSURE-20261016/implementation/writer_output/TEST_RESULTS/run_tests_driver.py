"""Bounded runner: execute ONLY tests/test_lane_guard.py (single module), not a suite sweep."""
import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path.cwd()
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

_spec = importlib.util.spec_from_file_location("test_lane_guard", ROOT / "tests" / "test_lane_guard.py")
mod = importlib.util.module_from_spec(_spec)
sys.modules["test_lane_guard"] = mod
_spec.loader.exec_module(mod)

suite = unittest.defaultTestLoader.loadTestsFromModule(mod)
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
