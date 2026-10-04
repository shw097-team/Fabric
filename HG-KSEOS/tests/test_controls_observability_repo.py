from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from hg_kseos.control_validation import validate_controls
from hg_kseos.errors import InvariantViolation
from hg_kseos.observability import EventLog, StructuredEvent, no_progress
from hg_kseos.repo_intelligence import analyze_python_change


ROOT = Path(__file__).parents[1]


class ControlValidationTests(unittest.TestCase):
    def test_all_materialized_controls_have_effective_contracts(self) -> None:
        result = validate_controls(ROOT / "control")
        self.assertEqual(result["verdict"], "PASS")
        self.assertEqual(result["counts"]["skills"], 18)
        self.assertEqual(result["counts"]["agents"], 10)

    def test_skill_without_stop_contract_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "skills" / "broken" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("---\nname: broken\n---\n## Purpose\nx\n", encoding="utf-8")
            with self.assertRaises(InvariantViolation):
                validate_controls(root)


class ObservabilityTests(unittest.TestCase):
    def test_structured_log_and_no_progress_watchdog(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            digest = EventLog(path).append(
                StructuredEvent("TRACE-1", "EV-1", "WORKORDER", "WO-1", "RUNNING", "PROGRESS", {"step": 1})
            )
            record = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(record["event_digest"], digest)
            self.assertFalse(no_progress([{"entity_id": "A", "state": "X", "payload_digest": "1"}]))
            repeated = [{"entity_id": "A", "state": "X", "payload_digest": "1"}] * 2
            self.assertTrue(no_progress(repeated))


class RepoIntelligenceTests(unittest.TestCase):
    def test_ast_symbols_dependencies_and_diff_budget(self) -> None:
        result = analyze_python_change(ROOT, [ROOT / "src" / "hg_kseos" / "spine.py"], 500, 20)
        self.assertIn("SharedSpine", result["symbols"]["src/hg_kseos/spine.py"])
        self.assertIn("sqlite3", result["dependencies"]["src/hg_kseos/spine.py"])
        with self.assertRaises(InvariantViolation):
            analyze_python_change(ROOT, [ROOT / "src" / "hg_kseos" / "spine.py"], 5, 20)


if __name__ == "__main__":
    unittest.main()
