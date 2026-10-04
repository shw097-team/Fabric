"""Tests for far_trisource.py (WO-FAR-TRISOURCE-001; TS-ID mapping)."""
import sys, tempfile, json, os, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import far_trisource as ts


class ChannelOutcomeTests(unittest.TestCase):
    def test_hit(self):  # TS-001/003/005 shape
        o = ts.channel_outcome(True, [{"score": 3}, {"score": 0}])
        self.assertEqual(o["status"], "HIT"); self.assertEqual(o["relevant_count"], 1)

    def test_zero_relevant_hit(self):  # TS-002/004/006 shape
        o = ts.channel_outcome(True, [{"score": 0}])
        self.assertEqual(o["status"], "ZERO_RELEVANT_HIT")

    def test_unavailable(self):  # TS-009/010/011
        o = ts.channel_outcome(True, [], reachable=False)
        self.assertEqual(o["status"], "UNAVAILABLE")

    def test_blocked_by_authority(self):  # TS-012
        o = ts.channel_outcome(False, [], blocked_reason="ACL denied")
        self.assertEqual(o["status"], "BLOCKED_BY_AUTHORITY")

    def test_error(self):  # TS-013
        o = ts.channel_outcome(True, [], error="boom")
        self.assertEqual(o["status"], "ERROR")


class MandatoryTests(unittest.TestCase):
    def test_silent_skip_raises_failclosed(self):  # TS-007
        def probe(ch):
            return (False, [], True, None, None)  # not attempted, not blocked
        with self.assertRaises(ts.FailClosedSilentSkip):
            ts.run_tri_source_assurance("WO", "R", "q", "d", probe, allowed_web_roots=None)

    def test_all_hit_eligible(self):  # TS-008/014
        def probe(ch):
            return (True, [{"score": 5, "source_id": ch + "-1"}], True, None, None)
        receipt, _ = ts.run_tri_source_assurance("WO", "R", "q", "d", probe,
                                                 allowed_web_roots=["arxiv.org"])
        self.assertTrue(receipt["terminal"]["all_three_accounted_for"])
        self.assertTrue(receipt["terminal"]["full_pass_eligible"])
        self.assertEqual(receipt["terminal"]["terminal"], "RESEARCH_PASS_CANDIDATE")

    def test_unavailable_no_full_pass(self):  # TS-009
        def probe(ch):
            if ch == "web":
                return (True, [], False, None, None)
            return (True, [{"score": 5, "source_id": ch}], True, None, None)
        receipt, _ = ts.run_tri_source_assurance("WO", "R", "q", "d", probe)
        self.assertFalse(receipt["terminal"]["full_pass_eligible"])
        self.assertEqual(receipt["terminal"]["terminal"], "RESEARCH_PARTIAL")
        self.assertIn("SOURCE_UNAVAILABLE", receipt["terminal"]["blocker_codes"])

    def test_blocked_limited_terminal(self):  # TS-012
        def probe(ch):
            if ch == "memory":
                return (False, [], True, None, "ACL denied")
            return (True, [{"score": 5, "source_id": ch}], True, None, None)
        receipt, _ = ts.run_tri_source_assurance("WO", "R", "q", "d", probe)
        self.assertEqual(receipt["terminal"]["terminal"], "RESEARCH_BLOCKED_BY_AUTHORITY")
        self.assertIn("SOURCE_BLOCKED", receipt["terminal"]["blocker_codes"])

    def test_error_stop(self):  # TS-013
        def probe(ch):
            if ch == "knowledge":
                raise RuntimeError("kv store down")
            return (True, [{"score": 5, "source_id": ch}], True, None, None)
        receipt, _ = ts.run_tri_source_assurance("WO", "R", "q", "d", probe)
        self.assertEqual(receipt["terminal"]["terminal"], "RESEARCH_ERROR_STOP")


class ArbitrationTests(unittest.TestCase):
    def base(self, **kw):
        d = {"claim_text": "c", "claim_role": "LOAD_BEARING", "domain": "FABRIC_INTERNAL",
             "memory_ids": [], "knowledge_ids": [], "web_ids": [],
             "freshness_status": "FRESH", "provenance_status": "COMPLETE", "memory_grade": "CANDIDATE"}
        d.update(kw); return d

    def test_approved_memory_aligned(self):  # TS-015
        c = ts.adjudicate_claim(self.base(memory_ids=["m1"], knowledge_ids=["k1"], memory_grade="APPROVED"))
        self.assertEqual(c["cross_source_status"], "ALIGNED")

    def test_candidate_memory_alone_insufficient(self):  # TS-016
        c = ts.adjudicate_claim(self.base(memory_ids=["m1"], memory_grade="CANDIDATE"))
        self.assertEqual(c["cross_source_status"], "INSUFFICIENT")

    def test_revoked_memory_cannot_support(self):  # TS-017
        c = ts.adjudicate_claim(self.base(memory_ids=["m1"], memory_grade="REVOKED"))
        self.assertEqual(c["cross_source_status"], "MEMORY_CONTRADICTS_CANONICAL")

    def test_missing_provenance_lead_only(self):  # TS-018
        c = ts.adjudicate_claim(self.base(memory_ids=["m1"], provenance_status="WEAK"))
        self.assertEqual(c["cross_source_status"], "INSUFFICIENT")

    def test_stale_approved_memory(self):  # TS-019
        c = ts.adjudicate_claim(self.base(memory_ids=["m1"], knowledge_ids=["k1"], memory_grade="APPROVED", freshness_status="STALE"))
        self.assertEqual(c["cross_source_status"], "MEMORY_STALE")

    def test_stale_knowledge_external(self):  # TS-020
        c = ts.adjudicate_claim(self.base(knowledge_ids=["k1"], web_ids=["w1"], freshness_status="STALE", claim_role="EXTERNAL_VERSION"))
        self.assertEqual(c["cross_source_status"], "KNOWLEDGE_STALE")

    def test_normative_overrides_web(self):  # TS-021
        c = ts.adjudicate_claim(self.base(knowledge_ids=["k1"], web_ids=["w1"], contradiction="WEB_VS_NORMATIVE"))
        self.assertEqual(c["cross_source_status"], "NORMATIVE_OVERRIDES_WEB")

    def test_web_newer_support(self):  # TS-022
        c = ts.adjudicate_claim(self.base(web_ids=["w1"], freshness_status="STALE", claim_role="EXTERNAL_VERSION"))
        self.assertEqual(c["cross_source_status"], "WEB_NEWER_SUPPORT")

    def test_web_contradicts_internal(self):  # TS-023 shape
        c = ts.adjudicate_claim(self.base(web_ids=["w1"], contradiction="WEB_CONTRADICTS_INTERNAL"))
        self.assertEqual(c["cross_source_status"], "WEB_CONTRADICTS_INTERNAL")

    def test_memory_contradicts_canonical(self):  # TS-024
        c = ts.adjudicate_claim(self.base(memory_ids=["m1"], knowledge_ids=["k1"], memory_grade="APPROVED", contradiction="MEMORY_VS_CANONICAL"))
        self.assertEqual(c["cross_source_status"], "MEMORY_CONTRADICTS_CANONICAL")


class CounterevidenceTests(unittest.TestCase):
    def test_load_bearing_requires_ce(self):  # TS-027
        ce = ts.counterevidence_probe({"claim_role": "LOAD_BEARING"}, query_fn=lambda q: [])
        self.assertTrue(ce["required"]); self.assertEqual(ce["status"], "ZERO_RELEVANT_COUNTEREVIDENCE_HIT")

    def test_non_load_bearing_recorded(self):
        ce = ts.counterevidence_probe({"claim_role": "SUPPORT"})
        self.assertFalse(ce["required"]); self.assertEqual(ce["status"], "OPTIONAL_NOT_RUN_RECORDED")


class ReducerTests(unittest.TestCase):
    def test_unresolved_contradiction_blocks(self):  # TS-026
        channels = {c: {"status": "HIT", "attempted": True} for c in ts.CHANNELS}
        claims = [{"claim_role": "LOAD_BEARING", "cross_source_status": "DISPUTED",
                   "provenance_status": "COMPLETE", "freshness_status": "FRESH"}]
        t = ts.terminal_reducer(channels, claims, {"required_count": 0, "completed": True})
        self.assertFalse(t["full_pass_eligible"]); self.assertIn("BLOCKING_CONTRADICTION", t["blocker_codes"])

    def test_counterevidence_missing_blocks(self):  # TS-028
        channels = {c: {"status": "HIT", "attempted": True} for c in ts.CHANNELS}
        t = ts.terminal_reducer(channels, [], {"required_count": 1, "completed": False})
        self.assertIn("COUNTEREVIDENCE_MISSING", t["blocker_codes"])


class ReceiptTests(unittest.TestCase):
    def test_receipt_schema_and_embedding(self):  # TS-008 receipt shape
        def probe(ch):
            return (True, [{"score": 5, "source_id": ch + "-1"}], True, None, None)
        receipt, _ = ts.run_tri_source_assurance("WO", "R", "q", "d", probe)
        self.assertEqual(receipt["schema"], "LOGICAL_FAR_TRI_SOURCE_COVERAGE_V1")
        for ch in ("memory", "knowledge", "web"):
            self.assertIn("status", receipt[ch]); self.assertIn("query_count", receipt[ch])
        # embedding contract: template carries tri_source_coverage field
        tpl = (Path(__file__).resolve().parent.parent / "research-product" / "templates" / "ResearchRunReceipt.json").read_text(encoding="utf-8")
        self.assertIn("tri_source_coverage", tpl)

    def test_memory_classification(self):
        graded = ts.classify_memory_rows([
            {"title": "approved memory x", "snippet": "", "source_id": "m1"},   # has provenance -> APPROVED
            {"title": "candidate idea", "snippet": "", "source_id": "m2"},      # has provenance -> CANDIDATE
            {"title": "revoked old note", "snippet": "", "source_id": "m3"},    # REVOKED (regardless of provenance)
            {"title": "approved memory, no provenance", "snippet": ""},         # F12: PROVENANCE_WEAK precedes APPROVED
        ])
        grades = [g["memory_grade"] for g in graded]
        self.assertIn("APPROVED", grades); self.assertIn("CANDIDATE", grades)
        self.assertIn("REVOKED", grades); self.assertIn("PROVENANCE_WEAK", grades)


if __name__ == "__main__":
    unittest.main()


class RegressionTests(unittest.TestCase):
    """F1-F12 challenge findings regression (deleg_1fdf4a41)."""

    def test_f3_probe_raise_first_channel_no_crash(self):
        # F3: probe raising on FIRST channel -> ERROR outcome, no NameError
        def probe(ch):
            if ch == "memory":
                raise RuntimeError("mem down")
            return (True, [{"score": 5, "source_id": ch}], True, None, None)
        receipt, _ = ts.run_tri_source_assurance("W", "R", "q", "d", probe)
        self.assertEqual(receipt["memory"]["status"], "ERROR")
        self.assertEqual(receipt["terminal"]["terminal"], "RESEARCH_ERROR_STOP")

    def test_f4_probe_raise_later_channel_no_leak(self):
        # F4: probe raising on LATER channel must not leak previous channel rows
        def probe(ch):
            if ch == "knowledge":
                raise RuntimeError("kv down")
            return (True, [{"score": 5, "source_id": ch + "-1"}], True, None, None)
        receipt, _ = ts.run_tri_source_assurance("W", "R", "q", "d", probe)
        self.assertEqual(receipt["knowledge"]["status"], "ERROR")
        self.assertEqual(receipt["knowledge"].get("receipt_refs", []), [])
        self.assertEqual(receipt["knowledge"].get("retrieved_count", 0), 0)

    def test_f9_blocked_precedes_unavailable(self):
        # F9: SOURCE_BLOCKED takes precedence over SOURCE_UNAVAILABLE
        def probe(ch):
            if ch == "memory":
                return (False, [], True, None, "ACL denied")
            if ch == "web":
                return (True, [], False, None, None)
            return (True, [{"score": 5, "source_id": ch}], True, None, None)
        receipt, _ = ts.run_tri_source_assurance("W", "R", "q", "d", probe)
        self.assertEqual(receipt["terminal"]["terminal"], "RESEARCH_BLOCKED_BY_AUTHORITY")

    def test_f6_counterevidence_error_incomplete(self):
        # F6: counterevidence query exception -> ERROR -> reducer blocks
        def boom(q):
            raise RuntimeError("ce source down")
        ce = ts.counterevidence_probe({"claim_role": "LOAD_BEARING"}, query_fn=boom)
        self.assertEqual(ce["status"], "ERROR")
        channels = {c: {"status": "HIT", "attempted": True} for c in ts.CHANNELS}
        t = ts.terminal_reducer(channels, [], {"required_count": 1, "completed": False})
        self.assertIn("COUNTEREVIDENCE_MISSING", t["blocker_codes"])

    def test_f12_provenance_weak_precedes_approved(self):
        graded = ts.classify_memory_rows([{"title": "approved memory x", "snippet": ""}])
        self.assertEqual(graded[0]["memory_grade"], "PROVENANCE_WEAK")
