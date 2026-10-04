from __future__ import annotations

import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import run_acceptance  # noqa: E402

from hg_kseos.cli import main as cli_main  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
ALLOWED_CHANGED_FILES = {"src/hg_kseos/cli.py", "tests/test_c2_case_run.py"}
# Orchestrator-owned C2 gate evidence already present in the worktree; it is not
# part of this taskspec's maker diff (TS-HGK-C4A-CASERUN-001, R5).
PRE_EXISTING_UNTRACKED = {"evidence/c2/"}


def _lf_bytes(path: Path) -> bytes:
    """Return file bytes with checkout CRLF normalized to the frozen LF blob."""
    return path.read_bytes().replace(b"\r\n", b"\n")


class CaseRunCliTests(unittest.TestCase):
    """R1-R4 for the `hg-kseos case run` subcommand (TS-HGK-C4A-CASERUN-001)."""

    def _prepare_root(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        """Build a complete frozen acceptance root bound to a temp directory.

        The frozen corpus blobs are LF; a Windows checkout carries CRLF, so the
        copies are normalized to the exact bytes the runner pins by SHA-256.
        """
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name).resolve()
        for relative in ("eval/fixtures", "eval/nrtv", "requirements", "source-freeze", "config"):
            (root / relative).mkdir(parents=True)
        (root / "eval" / "FROZEN_ACCEPTANCE_CASES.csv").write_bytes(
            _lf_bytes(REPO_ROOT / "eval" / "FROZEN_ACCEPTANCE_CASES.csv")
        )
        (root / "eval" / "fixtures" / "TST-037.yaml").write_bytes(
            _lf_bytes(REPO_ROOT / "eval" / "fixtures" / "TST-037.yaml")
        )
        (root / "eval" / "nrtv" / "TST-037.json").write_bytes(
            _lf_bytes(REPO_ROOT / "eval" / "nrtv" / "TST-037.json")
        )
        shutil.copy2(
            REPO_ROOT / "requirements" / "REQUIREMENT_COMPILATION_RECEIPT.json",
            root / "requirements" / "REQUIREMENT_COMPILATION_RECEIPT.json",
        )
        shutil.copy2(
            REPO_ROOT / "source-freeze" / "DENOMINATOR_RECONCILIATION.json",
            root / "source-freeze" / "DENOMINATOR_RECONCILIATION.json",
        )
        (root / "source-freeze" / "SOURCE_FREEZE_RECEIPT.json").write_text(
            json.dumps(
                {
                    "receipt_id": "SFR-TEST-CASERUN-001",
                    "execution_root": str(root),
                    "status": "FROZEN_WITH_RECORDED_RUNTIME_AND_PATH_REBIND_TT",
                }
            ),
            encoding="utf-8",
        )
        (root / "config" / "project.json").write_text(
            json.dumps({"source_root": str(root), "maker_root": str(root)}),
            encoding="utf-8",
        )
        return temporary, root

    def _run_cli(self, argv: list[str]) -> tuple[int, str, str]:
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = cli_main(argv)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_r1_case_run_tst037_exits_zero(self) -> None:
        temporary, root = self._prepare_root()
        self.addCleanup(temporary.cleanup)
        code, _out, err = self._run_cli(
            ["case", "run", "--id", "TST-037", "--root", str(root)]
        )
        self.assertEqual(0, code, msg=err)
        evidence_path = root / "evidence" / "wave-15" / "cases" / "TST-037.json"
        self.assertTrue(evidence_path.is_file())
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        self.assertEqual("MAKER_CASE_PASS", evidence["status"])

    def test_r1_forwards_root_and_case_id_and_propagates_exit_code(self) -> None:
        temporary, root = self._prepare_root()
        self.addCleanup(temporary.cleanup)
        captured: list[str] = []

        def fake_main() -> int:
            captured.extend(sys.argv)
            return 2

        with mock.patch("run_acceptance.main", side_effect=fake_main) as runner_main:
            code, _out, _err = self._run_cli(
                ["case", "run", "--id", "TST-037", "--root", str(root)]
            )
        self.assertEqual(2, code)
        runner_main.assert_called_once_with()
        self.assertEqual(
            ["run_acceptance", "--root", str(root), "--case-id", "TST-037"], captured
        )

    def test_r2_unknown_case_id_exits_nonzero(self) -> None:
        temporary, root = self._prepare_root()
        self.addCleanup(temporary.cleanup)
        code, _out, err = self._run_cli(
            ["case", "run", "--id", "TST-999", "--root", str(root)]
        )
        self.assertNotEqual(0, code)
        self.assertIn("unknown or empty --case-id selection", err)

    def test_r3_missing_id_is_parse_error(self) -> None:
        temporary, root = self._prepare_root()
        self.addCleanup(temporary.cleanup)
        with self.assertRaises(SystemExit) as raised:
            cli_main(["case", "run", "--root", str(root)])
        self.assertEqual(2, raised.exception.code)

    def test_r3_case_without_subcommand_is_parse_error(self) -> None:
        with self.assertRaises(SystemExit) as raised:
            cli_main(["case"])
        self.assertEqual(2, raised.exception.code)

    def test_r4_only_allowed_files_changed(self) -> None:
        porcelain = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        changed: set[str] = set()
        for line in porcelain.splitlines():
            if line.strip():
                changed.add(line[3:].strip())
        unexpected = changed - ALLOWED_CHANGED_FILES - PRE_EXISTING_UNTRACKED
        self.assertEqual(set(), unexpected)


if __name__ == "__main__":
    unittest.main()
