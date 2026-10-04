"""Deterministic unit tests for far_retrieval (stdlib unittest only)."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import far_retrieval  # noqa: E402

DOC_ROOT = r"C:/Projects/Agent_Workspace/知識庫/實作相關DOC"


class FarRetrievalTests(unittest.TestCase):

    def test_tokenize_cjk_bigrams(self):
        tokens = far_retrieval.tokenize("風險評估")
        self.assertIn("風險", tokens)
        self.assertIn("評估", tokens)

    def test_tokenize_ascii_words(self):
        tokens = far_retrieval.tokenize("ARIS research pipeline")
        self.assertIn("aris", tokens)
        self.assertIn("pipeline", tokens)

    def test_score_determinism(self):
        doc = "FAR retrieval layer design notes for the autonomous research pipeline."
        tokens = far_retrieval.tokenize("FAR retrieval pipeline")
        self.assertEqual(
            far_retrieval.score_doc(doc, tokens),
            far_retrieval.score_doc(doc, tokens),
        )

    def test_kb_scan_finds_far_docs(self):
        rows = far_retrieval.retrieve_knowledge_base(
            "FAR 檢索", roots=[DOC_ROOT])
        self.assertGreaterEqual(len(rows), 1)
        self.assertEqual(len(rows[0]["sha256"]), 64)
        self.assertEqual(rows[0]["role"], "LOCAL_GOVERNED_CORPUS")

    def test_web_deny_default(self):
        rows = far_retrieval.retrieve_web("anything", allowed_roots=None)
        self.assertEqual(rows, [])
        self.assertEqual(
            far_retrieval.last_web_status,
            "WEB_RETRIEVAL_SKIPPED_NO_ROOTS",
        )

    def test_web_arxiv_with_fake_fetch(self):
        feed = (
            b'<feed xmlns="http://www.w3.org/2005/Atom">'
            b"<entry><title>Fake Paper Title</title>"
            b"<summary>Fake abstract text</summary>"
            b"<id>http://arxiv.org/abs/9999.99999</id></entry></feed>"
        )
        rows = far_retrieval.retrieve_web(
            "test query",
            allowed_roots=["arxiv.org"],
            top_k=2,
            fetch_fn=lambda url: feed,
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["role"], "WEB")
        self.assertEqual(rows[0]["title"], "Fake Paper Title")

    def test_memory_fts_query(self):
        rows = far_retrieval.retrieve_memory("FAR", top_k=3)
        self.assertIsInstance(rows, list)

    def test_cross_reference_agreement(self):
        kb_rows = [{
            "source_id": "kb-1", "title": "",
            "snippet": "ARIS research methods", "score": 1,
        }]
        mem_rows = [{
            "source_id": "mem-1", "title": "",
            "snippet": "ARIS pipeline", "score": 1,
        }]
        rows = far_retrieval.build_cross_reference(kb_rows, mem_rows, [])
        self.assertTrue(any(row["agreement"] for row in rows))

    def test_cross_reference_disagreement(self):
        kb_rows = [{
            "source_id": "kb-1", "title": "",
            "snippet": "alpha xyz", "score": 1,
        }]
        mem_rows = [{
            "source_id": "mem-1", "title": "",
            "snippet": "beta qrs", "score": 1,
        }]
        rows = far_retrieval.build_cross_reference(kb_rows, mem_rows, [])
        self.assertTrue(any(
            row["disagreement"] and row["term"] == "(none)" for row in rows))

    def test_run_stage_writes_ledgers(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = far_retrieval.run_retrieval_stage(
                "FAR",
                "WO-TEST",
                tmp_dir,
                spine_db=far_retrieval.DEFAULT_SPINE_DB,
                allowed_web_roots=None,
                roots=[r"C:/Projects/Agent_Workspace/知識庫/實作相關DOC/fabric-autonomous-research"],
                max_files=60,
            )
            ledger_path = os.path.join(tmp_dir, "RetrievalLedger.json")
            cross_path = os.path.join(tmp_dir, "CrossReferenceLedger.tsv")
            self.assertTrue(os.path.isfile(ledger_path))
            self.assertTrue(os.path.isfile(cross_path))
            with open(ledger_path, "r", encoding="utf-8") as handle:
                ledger = json.load(handle)
            self.assertEqual(ledger["schema"], "FAR-RETRIEVAL-LEDGER/1")
            self.assertEqual(ledger["workorder_ref"], "WO-TEST")
            self.assertEqual(
                ledger["web_status"], "WEB_RETRIEVAL_SKIPPED_NO_ROOTS")
            self.assertIn("knowledge_base", ledger["channels"])
            with open(cross_path, "r", encoding="utf-8") as handle:
                header = handle.readline().rstrip("\n").split("\t")
            self.assertEqual(header[0], "channel_a")
            self.assertEqual(header[7], "note")
            self.assertEqual(result["files"]["ledger"], ledger_path)
            self.assertEqual(result["files"]["cross_reference"], cross_path)
            self.assertIsInstance(result["retrieval_count"], int)

    def test_parse_atom_rejects_doctype(self):
        evil = b'<?xml version="1.0"?><!DOCTYPE lolz [<!ENTITY lol "lol">]><feed xmlns="http://www.w3.org/2005/Atom"></feed>'
        with self.assertRaises(ValueError):
            far_retrieval._parse_atom(evil)

    def test_redirect_handler_exact_host(self):
        far_retrieval._AllowedHostsRedirectHandler(["arxiv.org"])
        self.assertTrue(any(h == "arxiv.org" or h.endswith(".arxiv.org") for h in ["arxiv.org", "export.arxiv.org"]))
        self.assertFalse(any(h == "arxiv.org" or h.endswith(".arxiv.org") for h in ["fakearxiv.org", "arxiv.org.evil.com"]))

    def test_web_url_uses_https(self):
        captured = {}
        def fake_fetch(url):
            captured["url"] = url
            return b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Fake Paper Title</title><summary>Fake abstract text</summary><id>http://arxiv.org/abs/9999.99999</id></entry></feed>'
        rows = far_retrieval.retrieve_web("test query", allowed_roots=["arxiv.org"], top_k=2, fetch_fn=fake_fetch)
        self.assertTrue(captured["url"].startswith("https://export.arxiv.org/"))
        self.assertEqual(len(rows), 1)

    def test_cross_reference_filters_trivial_tokens(self):
        rows = far_retrieval.build_cross_reference(
            [{"title": "A", "snippet": "research 1"}],
            [{"title": "B", "snippet": "research 1"}], [])
        self.assertTrue(all(r["term"] != "1" for r in rows))


if __name__ == "__main__":
    unittest.main()
