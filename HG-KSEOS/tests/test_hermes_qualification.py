from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from hg_kseos.providers import qualify_hermes_core
from hg_kseos.spine import SharedSpine


class HermesQualificationTests(unittest.TestCase):
    def test_advances_only_to_doctor_pass_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "config").mkdir()
            (root / "evidence" / "wave-06").mkdir(parents=True)
            (root / "config" / "project.json").write_text(
                json.dumps({"canonical_database": "var/test.db"}), encoding="utf-8"
            )
            (root / "config" / "hermes.json").write_text(
                json.dumps(
                    {
                        "release": {"commit": "9de9c25f"},
                        "provider_credentials_configured": False,
                    }
                ),
                encoding="utf-8",
            )
            (root / "evidence" / "wave-06" / "HERMES_INSTALL_RECEIPT.json").write_text(
                json.dumps(
                    {
                        "result": "PASS_LOCAL_CORE_NO_PROVIDER",
                        "release": {"commit": "9de9c25f"},
                    }
                ),
                encoding="utf-8",
            )
            (root / "evidence" / "wave-06" / "HERMES_RUNTIME_VALIDATION.json").write_text(
                json.dumps(
                    {
                        "negative_provider_pilot": {"passed": True},
                        "rollback_dry_run": {"passed": True},
                        "doctor": {"local_core_checks_passed": True},
                        "official_security_rollback_tests": {
                            "tests": 57,
                            "passed": 50,
                            "failures": 7,
                            "all_observed_failures_are_windows_symlink_privilege_blocks": True,
                        },
                    }
                ),
                encoding="utf-8",
            )
            database = root / "var" / "test.db"
            spine = SharedSpine(database)
            spine.initialize()
            with spine.transaction() as connection:
                connection.execute(
                    """INSERT INTO provider_bindings
                       (provider_id,slot,disposition,state,rollback_pointer,updated_at)
                       VALUES('P0-TOOL-001','Hermes Agent','DEFAULT_ENABLED_AFTER_QUALIFICATION',
                              'DISCOVERED','RB-P0-TOOL-001','now')"""
                )
            first = qualify_hermes_core(root)
            second = qualify_hermes_core(root)
            self.assertEqual(first["state"], "DOCTOR_PASS")
            self.assertEqual(second["state"], "DOCTOR_PASS")
            self.assertNotIn("PILOT_PASS", first["advanced"])
            self.assertEqual(second["advanced"], [])


if __name__ == "__main__":
    unittest.main()
