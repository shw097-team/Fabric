"""Engineering-base ChangeSet tests: the canonical acceptance-resolution primitive.

Scope of this file is exactly the seven classes the bounded ChangeSet authorization requires. Every
mutation goes through typed SharedSpine APIs; SQL is used only for readback assertions.
"""
import sqlite3
import unittest
from pathlib import Path

from hg_kseos.errors import InvariantViolation, LeaseConflict, StaleState
from hg_kseos.spine import SharedSpine, TRANSITIONS


class _Base(unittest.TestCase):
    def setUp(self):
        import tempfile
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.spine = SharedSpine(Path(self._tmp.name) / "spine.db")
        self.spine.initialize()
        self.actor = "wave-controller"
        self.token = "TK-ACC"

    def tearDown(self):
        self._tmp.cleanup()

    # helpers -------------------------------------------------------------
    def _project_with_one_acceptance(self, req="REQ-CS-001"):
        self.spine.create_project("HGK-P0-CS", "ChangeSet scratch")
        self.spine.register_requirement(
            requirement_id=req, source_locator="locator:test",
            wording="the obligation under test", acceptance_id=f"ACC-{req}",
            oracle="explicit oracle PASS", threshold="EXPLICIT_ORACLE_PASS",
            negative_fixture="obligation without workorder", project_id="HGK-P0-CS")
        return f"ACC-{req}", req

    def _evidence(self, eid="EVD-1"):
        self.spine.register_evidence(eid, "TEST_LOG", "tests/test_acceptance_resolution.py",
                                     "a" * 64, producer="maker", checker="checker")

    def _lease(self, resource):
        self.spine.acquire_lease(resource, self.actor, self.token, ttl_seconds=300)

    def _resolve(self, acc, **kw):
        base = dict(verdict="PASS", evidence_ref="EVD-1", actor=self.actor, token=self.token,
                    expected_version=0, idempotency_key=f"RES-{acc}",
                    requirement_id=acc.replace("ACC-", ""))
        base.update(kw)
        return self.spine.resolve_acceptance(acc, **base)

    def _verdict(self, acc):
        with sqlite3.connect(self.spine.database) as c:
            return c.execute("SELECT verdict, evidence_ref FROM acceptances WHERE acceptance_id=?",
                             (acc,)).fetchone()

    def _events(self, acc):
        with sqlite3.connect(self.spine.database) as c:
            return c.execute("SELECT event_id, from_state, to_state, evidence_ref FROM canonical_events "
                             "WHERE entity_type='acceptance' AND entity_id=?", (acc,)).fetchall()


class Class1LegalResolution(_Base):
    """1. legal NOT_RUN -> PASS with valid evidence; readback reflect the canonical resolved state."""

    def test_legal_pass_resolution(self):
        acc, req = self._project_with_one_acceptance()
        self._evidence()
        self._lease(acc)
        self.assertEqual(self._verdict(acc), ("NOT_RUN", None))
        out = self._resolve(acc)
        self.assertFalse(out["idempotent_replay"])
        self.assertEqual(out["to_state"], "PASS")
        self.assertEqual(self._verdict(acc), ("PASS", "EVD-1"))
        self.assertEqual(len(self._events(acc)), 1)
        # the denominator's openness rule ("verdict != 'PASS'") now reports this acceptance closed
        with sqlite3.connect(self.spine.database) as c:
            open_now = [r[0] for r in c.execute(
                "SELECT acceptance_id FROM acceptances WHERE verdict<>'PASS'")]
        self.assertEqual(open_now, [])

    def test_legal_fail_resolution_is_recorded_too(self):
        acc, _ = self._project_with_one_acceptance()
        self._evidence()
        self._lease(acc)
        self._resolve(acc, verdict="FAIL")
        self.assertEqual(self._verdict(acc), ("FAIL", "EVD-1"))


class Class2NonPassSemantics(_Base):
    """2. a legal non-PASS verdict must not be misjudged as PASS anywhere."""

    def test_fail_is_not_pass(self):
        acc, _ = self._project_with_one_acceptance()
        self._evidence()
        self._lease(acc)
        self._resolve(acc, verdict="FAIL")
        with sqlite3.connect(self.spine.database) as c:
            open_now = [r[0] for r in c.execute(
                "SELECT acceptance_id FROM acceptances WHERE verdict<>'PASS'")]
        self.assertEqual(open_now, [acc], "a FAIL verdict must still count as an OPEN denominator edge")

    def test_transition_table_has_no_verdict_alias(self):
        self.assertEqual(TRANSITIONS["acceptance"]["NOT_RUN"], {"PASS", "FAIL"})
        self.assertEqual(TRANSITIONS["acceptance"]["PASS"], set())
        self.assertEqual(TRANSITIONS["acceptance"]["FAIL"], set())


class Class3EvidenceBindingFailClosed(_Base):
    """3. Evidence binding and subject binding must fail closed.

    DISCLOSED SCOPE: `evidence_refs` carries no subject/requirement column, so this class proves
    REGISTERED-evidence binding and MANDATORY subject binding. It does NOT and cannot prove rejection of
    evidence belonging to another subject - that needs a subject key on the evidence registry itself
    (typed TT HGK-EBC-TT-001), and the code does not claim otherwise.
    """

    def test_unregistered_evidence_refused(self):
        acc, _ = self._project_with_one_acceptance()
        self._lease(acc)
        with self.assertRaises(InvariantViolation) as e:
            self._resolve(acc, evidence_ref="EVD-DOES-NOT-EXIST")
        self.assertIn("ERR_ACCEPTANCE_EVIDENCE_UNKNOWN", str(e.exception))
        self.assertEqual(self._verdict(acc), ("NOT_RUN", None))

    def test_missing_evidence_ref_refused(self):
        acc, _ = self._project_with_one_acceptance()
        self._lease(acc)
        with self.assertRaises(InvariantViolation):
            self._resolve(acc, evidence_ref="")

    def test_wrong_subject_requirement_refused(self):
        acc, _ = self._project_with_one_acceptance()
        self._evidence()
        self._lease(acc)
        with self.assertRaises(InvariantViolation) as e:
            self._resolve(acc, requirement_id="REQ-SOMEONE-ELSE")
        self.assertIn("ERR_ACCEPTANCE_WRONG_SUBJECT", str(e.exception))

    def test_unknown_acceptance_refused(self):
        self._evidence()
        self._lease("ACC-NOPE")
        with self.assertRaises(InvariantViolation) as e:
            self._resolve("ACC-NOPE")
        self.assertIn("ERR_ACCEPTANCE_UNKNOWN", str(e.exception))

    def test_missing_requirement_id_refused(self):
        acc, _ = self._project_with_one_acceptance()
        self._evidence()
        self._lease(acc)
        with self.assertRaises(InvariantViolation) as e:
            self._resolve(acc, requirement_id=None)
        self.assertIn("ERR_ACCEPTANCE_SUBJECT_BINDING_REQUIRED", str(e.exception))
        self.assertEqual(self._verdict(acc), ("NOT_RUN", None))

    def test_illegal_verdict_refused(self):
        acc, _ = self._project_with_one_acceptance()
        self._evidence()
        self._lease(acc)
        for bad in ("MAYBE", "OK", "", "pass", "NOT_RUN"):
            with self.assertRaises(InvariantViolation):
                self._resolve(acc, verdict=bad, idempotency_key=f"RES-bad-{bad}")
            self.assertEqual(self._verdict(acc), ("NOT_RUN", None))


class Class4ReplayIdempotent(_Base):
    """4. an identical resolution replay is idempotent, not a second transition."""

    def test_replay_returns_original_event(self):
        acc, _ = self._project_with_one_acceptance()
        self._evidence()
        self._lease(acc)
        first = self._resolve(acc)
        second = self._resolve(acc)
        self.assertTrue(second["idempotent_replay"])
        self.assertEqual(second["event_id"], first["event_id"])
        self.assertEqual(len(self._events(acc)), 1)


class Class4bIdempotencyNamespace(_Base):
    """4b. an idempotency key spent on another subject must fail closed, not silently replay."""

    def test_key_reused_for_another_acceptance_fails_closed(self):
        acc1, req1 = self._project_with_one_acceptance("REQ-CS-A")
        acc2, req2 = self._project_with_one_acceptance("REQ-CS-B")
        self._evidence()
        self._lease(acc1)
        self._lease(acc2)
        self._resolve(acc1, idempotency_key="SHARED-KEY")
        with self.assertRaises(InvariantViolation) as e:
            self._resolve(acc2, idempotency_key="SHARED-KEY")
        self.assertIn("ERR_IDEMPOTENCY_KEY_REUSED_FOR_OTHER_SUBJECT", str(e.exception))
        self.assertEqual(self._verdict(acc2), ("NOT_RUN", None),
                         "the second acceptance must NOT inherit the first subject's event")


class Class4cIdempotencyEntityTypeCollision(_Base):
    """4c. the key namespace is global: a key spent on a NON-acceptance event whose entity_id happens
    to equal the acceptance_id must NOT be inherited as this acceptance's replay."""

    def test_key_spent_on_a_requirement_event_is_not_inherited(self):
        """A GENUINE entity_id collision: a requirement literally named like our acceptance_id emits a
        requirement event whose entity_id equals the acceptance_id, in the same global key namespace."""
        acc, req = self._project_with_one_acceptance("COLLIDE")      # acceptance id = ACC-COLLIDE
        self.assertEqual(acc, "ACC-COLLIDE")
        # a second requirement whose NAME is exactly our acceptance id
        self.spine.register_requirement(
            requirement_id=acc, source_locator="locator:collide", wording="name collision probe",
            acceptance_id="ACC-" + acc, oracle="o", threshold="EXPLICIT_ORACLE_PASS",
            negative_fixture="n", project_id="HGK-P0-CS")
        self._evidence()
        self._lease(acc)                      # one lease on the resource id serves both transitions
        self.spine.transition_requirement(acc, "FROZEN", actor=self.actor, token=self.token,
                                          expected_version=0, evidence_ref="EVD-1",
                                          idempotency_key="KSHARED")
        with self.assertRaises(InvariantViolation) as e:
            self._resolve(acc, idempotency_key="KSHARED")
        self.assertIn("ERR_IDEMPOTENCY_KEY_REUSED_FOR_OTHER_SUBJECT", str(e.exception))
        self.assertEqual(self._verdict(acc), ("NOT_RUN", None),
                         "the acceptance must not inherit a requirement event as its replay")

    def test_replay_still_works_for_its_own_acceptance(self):
        acc, _ = self._project_with_one_acceptance()
        self._evidence()
        self._lease(acc)
        first = self._resolve(acc)
        second = self._resolve(acc)
        self.assertTrue(second["idempotent_replay"])
        self.assertEqual(second["event_id"], first["event_id"])

    def test_unleased_replay_is_refused(self):
        """The replay path is held to the same discipline as the first write: no lease, no replay."""
        acc, _ = self._project_with_one_acceptance()
        self._evidence()
        self._lease(acc)
        self._resolve(acc)
        self.spine.release_lease(acc, self.actor, self.token)
        with self.assertRaises(LeaseConflict) as e:
            self._resolve(acc)
        self.assertIn("ERR_LEASE_REQUIRED", str(e.exception))

    def test_replay_still_requires_registered_evidence(self):
        acc, _ = self._project_with_one_acceptance()
        self._evidence()
        self._lease(acc)
        self._resolve(acc)
        with self.assertRaises(InvariantViolation) as e:
            self._resolve(acc, evidence_ref="EVD-NOT-REGISTERED")
        self.assertIn("ERR_ACCEPTANCE_EVIDENCE_UNKNOWN", str(e.exception))

    def test_replay_cannot_bypass_the_requirement_check(self):
        acc, _ = self._project_with_one_acceptance()
        self._evidence()
        self._lease(acc)
        self._resolve(acc)
        with self.assertRaises(InvariantViolation) as e:
            self._resolve(acc, requirement_id="WRONG-REQ")
        self.assertIn("ERR_ACCEPTANCE_WRONG_SUBJECT", str(e.exception))


class Class5StaleConflictingRejected(_Base):
    """5. conflicting re-resolution and stale versions are rejected."""

    def test_conflicting_re_resolution_rejected(self):
        acc, _ = self._project_with_one_acceptance()
        self._evidence()
        self._lease(acc)
        self._resolve(acc, verdict="PASS", idempotency_key="K1")
        with self.assertRaises(InvariantViolation) as e:
            self._resolve(acc, verdict="FAIL", idempotency_key="K2")
        self.assertIn("ERR_ACCEPTANCE_ILLEGAL_TRANSITION", str(e.exception))
        self.assertEqual(self._verdict(acc), ("PASS", "EVD-1"))

    def test_stale_expected_version_rejected(self):
        acc, _ = self._project_with_one_acceptance()
        self._evidence()
        self._lease(acc)
        with self.assertRaises(StaleState) as e:
            self._resolve(acc, expected_version=7)
        self.assertIn("ERR_ACCEPTANCE_STALE_VERSION", str(e.exception))
        self.assertEqual(self._verdict(acc), ("NOT_RUN", None))

    def test_lease_is_required(self):
        acc, _ = self._project_with_one_acceptance()
        self._evidence()
        self.assertTrue(hasattr(self.spine, "resolve_acceptance"),
                        "vacuous-guard: the method must exist for this test to mean anything")
        with self.assertRaises(LeaseConflict) as e:
            self._resolve(acc)
        self.assertIn("ERR_LEASE_REQUIRED", str(e.exception))
        self.assertEqual(self._verdict(acc), ("NOT_RUN", None))


class Class6TransactionAtomicity(_Base):
    """6. a failing resolution leaves no partial state."""

    def test_foreign_idempotency_key_is_refused_not_inherited(self):
        """Historical defect: a key spent on ANOTHER subject silently returned that subject's event and
        skipped the write. It must now fail closed (see Class4b)."""
        acc, _ = self._project_with_one_acceptance()
        self._evidence()
        self._lease(acc)
        with sqlite3.connect(self.spine.database) as c:
            c.execute("INSERT INTO canonical_events(event_id,idempotency_key,entity_type,entity_id,"
                      "from_state,to_state,actor,expected_version,resulting_version,payload_json,"
                      "evidence_ref,rollback_pointer,created_at)"
                      " VALUES('EVT-SEED','RES-ACC-REQ-CS-001','acceptance','other','NOT_RUN','PASS',"
                      "'x',0,1,'{}','EVD-1','RB-x','2026-01-01T00:00:00Z')")
            c.commit()
        with self.assertRaises(InvariantViolation) as e:
            self._resolve(acc)
        self.assertIn("ERR_IDEMPOTENCY_KEY_REUSED_FOR_OTHER_SUBJECT", str(e.exception))
        self.assertEqual(self._verdict(acc), ("NOT_RUN", None))

    def test_failure_AFTER_the_update_rolls_the_row_back(self):
        """The real atomicity test: make the canonical-event INSERT fail AFTER the UPDATE has run,
        then prove the acceptances row was rolled back. (The pre-seeded-key test exercises the replay
        path, not rollback of an executed UPDATE.)"""
        import hg_kseos.spine as sp
        acc, _ = self._project_with_one_acceptance()
        self._evidence()
        self._lease(acc)
        original = sp.canonical_json
        try:
            sp.canonical_json = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("injected post-UPDATE failure"))
            with self.assertRaises(RuntimeError):
                self._resolve(acc)
        finally:
            sp.canonical_json = original
        self.assertEqual(self._verdict(acc), ("NOT_RUN", None),
                         "an executed UPDATE must be rolled back when the event insert fails")
        self.assertEqual(len(self._events(acc)), 0)

    def test_atomicity_under_illegal_transition(self):
        acc, _ = self._project_with_one_acceptance()
        self._evidence()
        self._lease(acc)
        with sqlite3.connect(self.spine.database) as c:
            c.execute("UPDATE acceptances SET verdict='BROKEN' WHERE acceptance_id=?", (acc,))
            c.commit()
        with self.assertRaises(InvariantViolation):
            self._resolve(acc)
        with sqlite3.connect(self.spine.database) as c:
            row = c.execute("SELECT verdict, evidence_ref FROM acceptances WHERE acceptance_id=?",
                            (acc,)).fetchone()
        self.assertEqual(row, ("BROKEN", None), "a rejected transition must not mutate the row")


class Class7ScratchProjectTypedClosure(_Base):
    """7. end-to-end typed closure of a scratch project, with no caller-side SQL writes."""

    def test_full_typed_closure_chain(self):
        self.spine.create_project("HGK-P0-CS7", "closure scratch")
        self.spine.register_requirement(
            requirement_id="REQ-CS7", source_locator="locator:cs7", wording="close the denominator",
            acceptance_id="ACC-REQ-CS7", oracle="typed oracle", threshold="EXPLICIT_ORACLE_PASS",
            negative_fixture="unclosed acceptance", project_id="HGK-P0-CS7")
        self.spine.acquire_lease("REQ-CS7", "planner", "TK-R", ttl_seconds=300)
        self.spine.transition_requirement("REQ-CS7", "FROZEN", actor="planner", token="TK-R",
                                          expected_version=0, evidence_ref="EV-1",
                                          idempotency_key="FRZ-CS7")
        self.spine.release_lease("REQ-CS7", "planner", "TK-R")
        self.spine.create_taskspec("TS-CS7", "REQ-CS7", objective="close", owner="owner",
                                   writable_root=Path("worktrees") / "ts-cs7",
                                   permissions={"write_scope": "worktree"},
                                   tests=["test_x.py"], evidence_plan="raw + independent")
        self.spine.create_workorder("WO-CS7", "TS-CS7", writer="codex",
                                    worktree=Path("worktrees") / "ts-cs7", base_head="deadbeef")
        self.spine.register_evidence("EVD-CS7", "TEST_LOG", "tests/x.py", "b" * 64,
                                     producer="maker", checker="checker")
        self.spine.record_workorder_result("WO-CS7", writer="codex", checker="independent",
                                           verdict="PASS", evidence_refs=["EVD-CS7"])
        self.spine.acquire_lease("ACC-REQ-CS7", "wave-controller", "TK-A", ttl_seconds=300)
        self.spine.resolve_acceptance("ACC-REQ-CS7", verdict="PASS", evidence_ref="EVD-CS7",
                                      actor="wave-controller", token="TK-A", expected_version=0,
                                      idempotency_key="RES-CS7", requirement_id="REQ-CS7")
        with sqlite3.connect(self.spine.database) as c:
            wo = c.execute("SELECT state, result_json FROM workorders WHERE workorder_id='WO-CS7'").fetchone()
            acc = c.execute("SELECT verdict, evidence_ref FROM acceptances "
                            "WHERE acceptance_id='ACC-REQ-CS7'").fetchone()
            ev = c.execute("SELECT COUNT(*) FROM evidence_refs").fetchone()[0]
            evt = c.execute("SELECT COUNT(*) FROM canonical_events WHERE entity_type='acceptance'").fetchone()[0]
        self.assertEqual(wo[0], "VERIFIED")
        self.assertIn("PASS", wo[1])
        self.assertEqual(acc, ("PASS", "EVD-CS7"))
        self.assertEqual(ev, 1)
        self.assertEqual(evt, 1)
        # the closure predicate the wave controller uses is now satisfiable through typed APIs alone
        with sqlite3.connect(self.spine.database) as c:
            open_acc = [r[0] for r in c.execute("SELECT acceptance_id FROM acceptances "
                                                "WHERE verdict<>'PASS'")]
        self.assertEqual(open_acc, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
