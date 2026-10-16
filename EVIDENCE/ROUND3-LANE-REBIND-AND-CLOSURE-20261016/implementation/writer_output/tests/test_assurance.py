from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from hg_kseos.assurance import (
    EffectToken, SkillRegistry, budget_decision, deterministic_gate, exact_behavior_set,
    migration_gate, negotiate_mcp, prompt_contract, provider_compatibility,
    reconcile_release_identity, reconcile_sbom, require_archive_failure_propagation,
    require_fresh_base, resolve_instruction_chain, security_veto, select_permission_mode,
    telemetry_gate, validate_receiver_packet, validate_rollback_pointer,
)
from hg_kseos.errors import InvariantViolation
from hg_kseos.spine import SharedSpine


class AssuranceTests(unittest.TestCase):
    def assert_rejected(self, function, *args) -> None:
        with self.assertRaises(InvariantViolation):
            function(*args)

    def test_instruction_precedence_and_stale_override(self) -> None:
        self.assertEqual(resolve_instruction_chain([{"id": "global", "scope_rank": 0, "authority_rank": 3}, {"id": "root", "scope_rank": 1, "authority_rank": 3}]), ["global", "root"])
        self.assert_rejected(resolve_instruction_chain, [{"id": "global", "scope_rank": 0, "authority_rank": 3}, {"id": "nested", "scope_rank": 2, "authority_rank": 2}])

    def test_skill_collision_implicit_and_clean_removal(self) -> None:
        registry = SkillRegistry(); registry.install("bounded", {"bounded"}, False)
        self.assert_rejected(registry.install, "bounded", {"other"}, False)
        self.assert_rejected(registry.install, "writer", {"bounded"}, True)
        self.assert_rejected(registry.route, "bounded", False)
        self.assertEqual(registry.route("bounded", True), "bounded")
        registry.remove("bounded"); self.assertEqual(registry.skills, {})

    def test_mcp_revision_negotiation(self) -> None:
        self.assertEqual(negotiate_mcp("2026-07", "2026-07", set()), "PINNED_CONFORMANT")
        self.assert_rejected(negotiate_mcp, "2026-07", "2025-11", set())

    def test_stale_base_and_deterministic_oracle(self) -> None:
        self.assert_rejected(require_fresh_base, "a", "b")
        self.assert_rejected(deterministic_gate, False, True)

    def test_telemetry_privacy_and_budget(self) -> None:
        self.assert_rejected(telemetry_gate, True, False, False)
        self.assertEqual(budget_decision(100, 50, 100), "STOP_ESCALATE")

    def test_sbom_and_migration_reconciliation(self) -> None:
        reconcile_sbom({"a"}, {"a"})
        self.assert_rejected(reconcile_sbom, {"a"}, {"a", "b"})
        self.assert_rejected(migration_gate, {"value": 1}, {"value": 2})

    def test_receiver_packet_capability_and_nack(self) -> None:
        self.assert_rejected(validate_receiver_packet, {"required_capabilities": []}, set())
        self.assert_rejected(validate_receiver_packet, {"rollback": "rb", "required_capabilities": ["x"]}, set())
        self.assertEqual(validate_receiver_packet({"rollback": "rb", "required_capabilities": [], "receiver_verdict": "NACK", "field_defects": ["f"]}, set()), "REWORK")

    def test_regression_release_drift_and_archive_failure(self) -> None:
        self.assert_rejected(exact_behavior_set, {"a", "b"}, {"a"})
        self.assert_rejected(reconcile_release_identity, "v1", "v2", "a", "a")
        self.assert_rejected(require_archive_failure_propagation, False, 0)

    def test_rollback_prompt_veto_provider_and_token(self) -> None:
        self.assert_rejected(validate_rollback_pointer, Path("definitely-missing-generation"))
        self.assert_rejected(prompt_contract, {}, {"result"}, False)
        self.assert_rejected(prompt_contract, {"result": "summary"}, {"result"}, True)
        self.assert_rejected(security_veto, True, False)
        self.assert_rejected(provider_compatibility, {"stream", "tools"}, {"stream"})
        token = EffectToken("t", 10); token.consume(5); self.assert_rejected(token.consume, 6)

    def test_permission_mode_and_unicode_space_path(self) -> None:
        self.assertEqual(select_permission_mode(False, True), "LEGACY_SANDBOX")
        with tempfile.TemporaryDirectory(prefix="HGK Unicode 空 格 ") as directory:
            database = Path(directory) / "spine test.db"
            spine = SharedSpine(database); spine.initialize()
            self.assertEqual(spine.snapshot()["schema_version"], "3")


if __name__ == "__main__":
    unittest.main()
