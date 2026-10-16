from __future__ import annotations

import json
import unittest
from pathlib import Path

from hg_kseos.errors import InvariantViolation
from hg_kseos.hlpe import qualify_hlpe


ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "config" / "project.json").read_text(encoding="utf-8"))


class HLPEBindingTests(unittest.TestCase):
    def test_current_integrated_target_qualifies(self) -> None:
        result = qualify_hlpe(Path(CONFIG["hlpe"]["integrated_target"]), CONFIG["hlpe"]["expected_head"])
        self.assertEqual(result["status"], "QUALIFIED_SCOPE")
        self.assertTrue(result["clean"])

    def test_wrong_head_is_rejected(self) -> None:
        with self.assertRaises(InvariantViolation):
            qualify_hlpe(Path(CONFIG["hlpe"]["integrated_target"]), "0" * 40)


if __name__ == "__main__":
    unittest.main()
