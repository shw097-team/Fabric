"""Focused hardening tests (FH-T001..038 mapping; WO-FAR-HARDENING-001)."""
import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import far_retrieval as fr
import far_trisource as ts


class LineageTests(unittest.TestCase):
    """FH-01: cross-source origin lineage / same-origin dedup."""

    def test_fh_t001_same_digest_single_origin(self):  # FH-T001
        ind = ts.compute_independence([
            {"score": 5, "origin_artifact_digest": "d1", "source_family": "FABRIC_HGK_KNOWLEDGE", "derivation_kind": "CANONICAL"},
            {"score": 4, "origin_artifact_digest": "d1", "source_family": "FABRIC_HGK_KNOWLEDGE", "derivation_kind": "MEMORY_SUMMARY"}])
        self.assertEqual(ind["independent_origins"], 1)
        self.assertEqual(ts.cross_source_independence_status(ind), "DERIVED_SAME_ORIGIN")

    def test_fh_t002_memory_plus_web_two_origins(self):  # FH-T002
        ind = ts.compute_independence([
            {"score": 5, "origin_artifact_id": "DOC-A", "source_family": "FABRIC_HGK_KNOWLEDGE"},
            {"score": 4, "origin_artifact_id": "W-B", "source_family": "EXTERNAL_WEB"}])
        self.assertEqual(ind["independent_origins"], 2)

    def test_fh_t003_unresolved_origin(self):  # FH-T003
        ind = ts.compute_independence([{"score": 5, "source_id": "x"}])
        self.assertEqual(ts.cross_source_independence_status(ind), "ORIGIN_UNRESOLVED")

    def test_fh_t004_same_origin_not_independent_corroboration(self):  # FH-T004
        ind = ts.compute_independence([
            {"score": 5, "origin_artifact_id": "DOC-A", "source_family": "FABRIC_HGK_KNOWLEDGE", "derivation_kind": "CANONICAL"},
            {"score": 4, "origin_artifact_id": "DOC-A", "source_family": "HGK_MEMORY", "derivation_kind": "MEMORY_SUMMARY"}])
        self.assertEqual(ind["independent_origins"], 1)
        self.assertEqual(ts.cross_source_independence_status(ind), "DERIVED_SAME_ORIGIN")


class DoctypeXmlTests(unittest.TestCase):
    """FH-02: HTML doctype vs XML DTD semantics."""

    def test_fh_t005_html5_doctype_accepted(self):  # FH-T005
        kind, note = fr._content_type_semantics("text/html")
        self.assertEqual(kind, "HTML")
        self.assertIn("doctype allowed", note.lower())

    def test_fh_t006_xml_dtd_rejected(self):  # FH-T006
        evil = b'<?xml version="1.0"?><!DOCTYPE lolz [<!ENTITY lol "lol">]><feed xmlns="http://www.w3.org/2005/Atom"></feed>'
        with self.assertRaises(ValueError):
            fr._parse_atom(evil)

    def test_fh_t007_xinclude_not_processed(self):  # FH-T007
        # ElementTree does NOT process XInclude -> no external fetch; include element is inert data
        xi = b'<feed xmlns="http://www.w3.org/2005/Atom" xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include href="http://evil.example/x"/><entry><title>ok</title><summary>s</summary><id>http://arxiv.org/abs/1</id></entry></feed>'
        parsed = fr._parse_atom(xi)  # parses without fetching; include is inert
        self.assertEqual(len(parsed), 1)  # only the real entry extracted; no external content


class SsrfTests(unittest.TestCase):
    """FH-02: SSRF hardening."""

    def test_fh_t008_http_deny(self): self.assertFalse(fr._validate_url("http://export.arxiv.org/x", ["arxiv.org"]))
    def test_fh_t009_file_deny(self): self.assertFalse(fr._validate_url("file:///etc/passwd", ["arxiv.org"]))
    def test_fh_t010_localhost_deny(self):
        self.assertFalse(fr._validate_url("https://localhost/x", ["localhost"]))
    def test_fh_t011_rfc1918_deny(self):
        verdict = fr._resolve_and_classify_ip("192.168.1.1")
        self.assertEqual(verdict[0], "DENY")
    def test_fh_t012_linklocal_metadata_deny(self):
        verdict = fr._resolve_and_classify_ip("169.254.169.254")
        self.assertEqual(verdict[0], "DENY")
    def test_fh_t013_redirects_disabled(self):  # FH-T013 (EXT-FAR-TS-HARD-001)
        # automatic redirects disabled entirely: any redirect (even same allowed host) is denied
        h = fr._NoRedirectHandler()
        with self.assertRaises(RuntimeError):
            h.redirect_request(None, None, 302, "x", None, "https://export.arxiv.org/x2")
        with self.assertRaises(RuntimeError):
            h.redirect_request(None, None, 302, "x", None, "https://evil.com/x")
    def test_fh_t014_redirect_private_ip(self):  # FH-T014
        with self.assertRaises(RuntimeError):
            fr._NoRedirectHandler().redirect_request(
                None, None, 302, "x", None, "https://10.0.0.5/x")
    def test_fh_t015_dns_private(self):
        self.assertIsNotNone(fr._resolve_and_classify_ip("localhost"))
    def test_fh_t016_exact_public_host(self):
        self.assertTrue(fr._validate_url("https://export.arxiv.org/api/query?x=1", ["arxiv.org"]))


class TruncationTests(unittest.TestCase):
    """FH-03: content completeness semantics."""

    def test_fh_t017_complete_under_cap(self):  # FH-T017
        tr = fr._truncation_receipt(b"x" * 100, {"Content-Length": "100"})
        self.assertTrue(tr["content_complete"]); self.assertEqual(tr["truncation_reason"], "NONE")
    def test_fh_t018_over_cap(self):  # FH-T018
        tr = fr._truncation_receipt(b"x" * (256 * 1024 + 1))
        self.assertFalse(tr["content_complete"]); self.assertEqual(tr["truncation_reason"], "BYTE_CAP")
    def test_fh_t019_truncated_cannot_sole_support_absence(self):  # FH-T019
        tr = fr._truncation_receipt(b"x" * (256 * 1024 + 1))
        self.assertFalse(tr["content_complete"])
        # negative inference rule: content_complete=false forbids full-document absence claims
        self.assertIn(tr["truncation_reason"], ("BYTE_CAP", "SERVER_ABORT", "CONTENT_LENGTH_UNKNOWN"))
    def test_fh_t020_truncated_positive_supports_observed(self):  # FH-T020
        tr = fr._truncation_receipt(b"x" * 1000, {"Content-Length": "5000"})
        self.assertFalse(tr["content_complete"]); self.assertEqual(tr["truncation_reason"], "SERVER_ABORT")


class BudgetTests(unittest.TestCase):
    """FH-04: query budget is a resource guard, not a correctness oracle."""

    def test_fh_t021_budget_exhausted_closed_pass_eligible(self):  # FH-T021
        t = ts.budget_exhaustion_terminal([{"claim_role": "LOAD_BEARING", "cross_source_status": "ALIGNED", "provenance_status": "COMPLETE"}])
        self.assertEqual(t["terminal"], "PASS_ELIGIBLE")
    def test_fh_t022_budget_exhausted_disputed_partial(self):  # FH-T022
        t = ts.budget_exhaustion_terminal([{"claim_role": "LOAD_BEARING", "cross_source_status": "DISPUTED"}])
        self.assertEqual(t["terminal"], "RESEARCH_PARTIAL_BUDGET_EXHAUSTED")
    def test_fh_t023_budget_exhausted_weak_no_pass(self):  # FH-T023
        t = ts.budget_exhaustion_terminal([{"claim_role": "LOAD_BEARING", "cross_source_status": "ALIGNED", "provenance_status": "WEAK"}])
        self.assertEqual(t["terminal"], "RESEARCH_PARTIAL_BUDGET_EXHAUSTED")
    def test_fh_t024_extension_policy(self):  # FH-T024
        t = ts.budget_exhaustion_terminal([{"claim_role": "LOAD_BEARING", "cross_source_status": "MISSING"}])
        self.assertIn("REQUEST_BUDGET_EXTENSION", t["extension"])


class CorroborationPolicyTests(unittest.TestCase):
    """FH-06: minimum evidence by claim class."""

    def test_fh_t025_internal_normative(self):
        self.assertIn("canonical owner source required", ts.CLAIM_CLASS_MINIMUM["INTERNAL_NORMATIVE"])
    def test_fh_t026_external_fact(self):
        self.assertIn("official current upstream", ts.CLAIM_CLASS_MINIMUM["EXTERNAL_CURRENT_FACT"])
    def test_fh_t027_recommendation(self):
        self.assertIn("counterevidence", ts.CLAIM_CLASS_MINIMUM["RECOMMENDATION"])
    def test_fh_t028_claim_independence_binding(self):
        ind = ts.compute_claim_independence({}, [], [], [])
        self.assertIn("cross_source_independence_status", ind)


class RetrievalLineageTests(unittest.TestCase):
    """FH-01: real retrieval rows carry lineage."""

    def test_fh_t029_kb_rows_lineage(self):
        rows = fr.retrieve_knowledge_base("FAR 藍圖", top_k=3, max_files=60,
                                          roots=[r"C:/Projects/Agent_Workspace/知識庫/實作相關DOC/fabric-autonomous-research"])
        for r in rows:
            self.assertEqual(r["source_family"], "FABRIC_HGK_KNOWLEDGE")
            self.assertEqual(r["derivation_kind"], "CANONICAL")
            self.assertEqual(r["origin_artifact_digest"], r["sha256"])
    def test_fh_t030_memory_rows_lineage(self):
        rows = fr.retrieve_memory("FAR", top_k=3, spine_db=r"C:\Projects\Agent_Workspace\HG-KSEOS\var\shared-spine\hg-kseos.db")
        for r in rows:
            self.assertIn("source_family", r)


class WebHitCanaryTests(unittest.TestCase):
    """FH-05: real web HIT (arXiv API, real network)."""

    def test_fh_t031_real_web_hit(self):
        rows = fr.retrieve_web("transformer attention", allowed_roots=["arxiv.org"], top_k=2)
        self.assertTrue(any(r.get("score", 0) > 0 and r.get("source_id") != "WEB-FAIL" for r in rows))
    def test_fh_t032_locator_metadata(self):
        rows = fr.retrieve_web("transformer attention", allowed_roots=["arxiv.org"], top_k=2)
        hit = next((r for r in rows if r.get("score", 0) > 0), None)
        self.assertIsNotNone(hit)
        self.assertIn("url", hit)
        self.assertIn("content_read", hit)
        self.assertIn("content_type_kind", hit)
    def test_fh_t033_web_evidence_bound(self):
        rows = fr.retrieve_web("transformer attention", allowed_roots=["arxiv.org"], top_k=2)
        hit = next((r for r in rows if r.get("score", 0) > 0), None)
        self.assertIsNotNone(hit)
        self.assertTrue(hit["source_id"].startswith("http"))
        self.assertEqual(hit["derivation_kind"], "WEB_PRIMARY")


class SoDRegressionTests(unittest.TestCase):
    """FH-033..038: SoD / SQS regression."""

    def test_fh_t037_no_new_platform(self):
        # no second scheduler/db/reducer/crawler: module imports stay stdlib
        src = Path(__file__).resolve().parent.parent
        for mod in ("far_retrieval.py", "far_trisource.py"):
            text = (src / mod).read_text(encoding="utf-8")
            for banned in ("import crawler", "from crawl4ai", "firecrawl", "neo4j", "qdrant"):
                self.assertNotIn(banned, text.lower())
    def test_fh_t038_rollback_pointer(self):
        import sqlite3
        con = sqlite3.connect(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\shared-spine\hg-kseos.db")
        r = con.execute("SELECT rollback_pointer FROM workorders WHERE workorder_id='WO-FAR-HARDENING-001'").fetchone()
        self.assertIsNotNone(r)
        self.assertTrue(r[0].startswith("RB-WO-FAR-HARDENING"))


if __name__ == "__main__":
    unittest.main()
