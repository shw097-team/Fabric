from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from hg_kseos.agents import DelegatedTask, TaskDAG
from hg_kseos.errors import InvariantViolation
from hg_kseos.providers import ProviderRegistry
from hg_kseos.spine import SharedSpine
from hg_kseos.util import utc_now


class AgentTests(unittest.TestCase):
    def test_acyclic_dag_and_join(self) -> None:
        dag = TaskDAG(
            [
                DelegatedTask("maker", "R-CODE", (), "C:/work/a"),
                DelegatedTask("checker", "R-VERIFY", ("maker",), None, checker_only=True),
            ]
        )
        self.assertEqual(dag.ready(set()), ["maker"])
        self.assertEqual(dag.ready({"maker"}), ["checker"])
        self.assertEqual(dag.join({"maker": "PASS", "checker": "PASS"}), "PASS")

    def test_cycle_rejected(self) -> None:
        with self.assertRaises(InvariantViolation):
            TaskDAG([DelegatedTask("a", "A", ("b",), None), DelegatedTask("b", "B", ("a",), None)])

    def test_shared_writer_root_rejected(self) -> None:
        with self.assertRaises(InvariantViolation):
            TaskDAG([DelegatedTask("a", "A", (), "C:/same"), DelegatedTask("b", "B", (), "c:/SAME")])

    def test_checker_write_scope_rejected(self) -> None:
        with self.assertRaises(InvariantViolation):
            TaskDAG([DelegatedTask("checker", "R-VERIFY", (), "C:/write", checker_only=True)])

    def test_join_propagates_nack(self) -> None:
        dag = TaskDAG([DelegatedTask("a", "A", (), None)])
        self.assertEqual(dag.join({"a": "FAIL"}), "NACK:a=FAIL")


class ProviderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.spine = SharedSpine(Path(self.temp.name) / "spine.db")
        self.spine.initialize()
        self.registry = ProviderRegistry(self.spine)
        with self.spine.transaction() as connection:
            connection.execute(
                """INSERT INTO provider_bindings
                   (provider_id,slot,xor_group,disposition,state,rollback_pointer,updated_at)
                   VALUES('P1','coding',NULL,'DEFAULT_ENABLED_AFTER_QUALIFICATION','DISCOVERED','RB-P1',?)""",
                (utc_now(),),
            )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_lifecycle_skip_rejected(self) -> None:
        with self.assertRaises(InvariantViolation):
            self.registry.advance("P1", "PINNED", pin="v1")

    def test_lifecycle_requires_evidence(self) -> None:
        self.registry.advance("P1", "IDENTIFIED")
        self.registry.advance("P1", "PINNED", pin="v1")
        self.registry.advance("P1", "INSTALLED")
        self.registry.advance("P1", "CONFIGURED")
        with self.assertRaises(InvariantViolation):
            self.registry.advance("P1", "DOCTOR_PASS")

    def test_xor_database_constraint(self) -> None:
        with self.spine.transaction() as connection:
            connection.execute(
                """INSERT INTO provider_bindings
                   (provider_id,slot,xor_group,disposition,state,rollback_pointer,updated_at)
                   VALUES('R1','retrieval','XOR-R','PREFERRED_DEFAULT','ENABLED','RB-R1',?)""",
                (utc_now(),),
            )
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    """INSERT INTO provider_bindings
                       (provider_id,slot,xor_group,disposition,state,rollback_pointer,updated_at)
                       VALUES('R2','retrieval','XOR-R','ALTERNATIVE','ENABLED','RB-R2',?)""",
                    (utc_now(),),
                )


if __name__ == "__main__":
    unittest.main()

