from __future__ import annotations

import inspect
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import run_acceptance


class AcceptanceRunnerContractTests(unittest.TestCase):
    def _root(self) -> tuple[tempfile.TemporaryDirectory[str], Path, dict[str, object]]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name).resolve()
        (root / "eval" / "nrtv").mkdir(parents=True)
        (root / "requirements").mkdir()
        receipt = {
            "predev_requirements": 240,
            "p0_requirements": 259,
            "requirement_trace_rows": 499,
        }
        (root / "requirements" / "REQUIREMENT_COMPILATION_RECEIPT.json").write_text(
            json.dumps(receipt), encoding="utf-8"
        )
        nrtv = {
            "schema": "HGK-BLIND-NRTV/1",
            "case_id": "TST-037",
            "query": "counts",
            "allowed_compiled_artifacts": [
                "requirements/REQUIREMENT_COMPILATION_RECEIPT.json"
            ],
            "forbidden_inputs": [str(root)],
            "expected_answer": receipt,
            "required_locators": [
                f"requirements/REQUIREMENT_COMPILATION_RECEIPT.json#/{name}"
                for name in receipt
            ],
        }
        (root / "eval" / "nrtv" / "TST-037.json").write_text(
            json.dumps(nrtv), encoding="utf-8"
        )
        return temporary, root, nrtv

    @staticmethod
    def _fixture() -> dict[str, object]:
        return {"oracle": "Answer from compiled artifacts with correct locator"}

    def _execute(self, root: Path) -> run_acceptance.CaseResult:
        nrtv_path = root / "eval" / "nrtv" / "TST-037.json"
        return run_acceptance.execute_tst_037(
            root,
            self._fixture(),
            expected_nrtv_hash=run_acceptance.sha256_bytes(nrtv_path.read_bytes()),
        )

    def test_tst_037_enforces_values_locators_allowlist_and_forbidden_log(self) -> None:
        temporary, root, _ = self._root()
        self.addCleanup(temporary.cleanup)
        result = self._execute(root)
        self.assertTrue(result.passed)
        log = result.details["artifact_access_log"]
        self.assertEqual(1, len(log))
        self.assertTrue(log[0]["explicitly_allowlisted"])
        self.assertTrue(log[0]["inside_declared_forbidden_root"])
        self.assertFalse(result.details["raw_source_volumes_read_by_case_executor"])

    def test_tst_037_rejects_locator_not_in_allowlist(self) -> None:
        temporary, root, nrtv = self._root()
        self.addCleanup(temporary.cleanup)
        nrtv["required_locators"][0] = "source-freeze/raw.json#/predev_requirements"
        (root / "eval" / "nrtv" / "TST-037.json").write_text(
            json.dumps(nrtv), encoding="utf-8"
        )
        with self.assertRaisesRegex(
            run_acceptance.CaseFailure, "LOCATOR_ARTIFACT_NOT_ALLOWED"
        ):
            self._execute(root)

    def test_tst_037_rejects_wrong_oracle_value(self) -> None:
        temporary, root, _ = self._root()
        self.addCleanup(temporary.cleanup)
        receipt_path = root / "requirements" / "REQUIREMENT_COMPILATION_RECEIPT.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["p0_requirements"] = 258
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        with self.assertRaisesRegex(run_acceptance.CaseFailure, "ORACLE_VALUE"):
            self._execute(root)

    def test_tst_037_rejects_traversal_in_allowed_artifact(self) -> None:
        temporary, root, nrtv = self._root()
        self.addCleanup(temporary.cleanup)
        nrtv["allowed_compiled_artifacts"] = ["../outside.json"]
        (root / "eval" / "nrtv" / "TST-037.json").write_text(
            json.dumps(nrtv), encoding="utf-8"
        )
        with self.assertRaisesRegex(run_acceptance.CaseFailure, "UNSAFE_RELATIVE_PATH"):
            self._execute(root)

    def test_tst_037_rejects_unpinned_nrtv_fixture(self) -> None:
        temporary, root, _ = self._root()
        self.addCleanup(temporary.cleanup)
        with self.assertRaisesRegex(run_acceptance.CaseFailure, "NRTV_FIXTURE_DRIFT"):
            run_acceptance.execute_tst_037(root, self._fixture())

    def test_all_cases_have_dedicated_executor(self) -> None:
        expected = {f"TST-{number:03d}" for number in range(1, 93)}
        self.assertEqual(expected, set(run_acceptance.CASE_EXECUTORS))
        self.assertNotIn("MAKER_PROXY_PASS", inspect.getsource(run_acceptance))


if __name__ == "__main__":
    unittest.main()
