from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "package_local.py"
SPEC = importlib.util.spec_from_file_location("hgk_package_local", MODULE_PATH)
assert SPEC and SPEC.loader
PACKAGE_LOCAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGE_LOCAL)


class PackageLocalTests(unittest.TestCase):
    def test_tracked_nested_release_is_included_and_wave18_receipt_is_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "-C", str(root), "init"], check=True, stdout=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "test"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@invalid"], check=True)
            nested = root / "control" / "release" / "AGENTS.md"
            nested.parent.mkdir(parents=True)
            nested.write_text("release control\n", encoding="utf-8")
            receipt = root / "evidence" / "wave-18" / "LOCAL_PACKAGE_READBACK.json"
            receipt.parent.mkdir(parents=True)
            receipt.write_text("{}\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-m", "fixture"], check=True, stdout=subprocess.PIPE)

            paths = [path.relative_to(root).as_posix() for path in PACKAGE_LOCAL.tracked_payload_files(root)]

            self.assertIn("control/release/AGENTS.md", paths)
            self.assertNotIn("evidence/wave-18/LOCAL_PACKAGE_READBACK.json", paths)


if __name__ == "__main__":
    unittest.main()
