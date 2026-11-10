# -*- coding: utf-8 -*-
"""Admission tests for the r26 governance mirror (EC-R26-013 / R26-09).

Runnable both ways, because CI uses unittest discovery and the round brief asks for
pytest:

    C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe -m pytest
    C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe -m unittest discover -s INTEGRATION/FHS/tests -v

Every negative here spawns the real validator as a subprocess and asserts on the
code it prints plus its exit status; a refusal is only evidence when this run
produced it.
"""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]        # INTEGRATION/FHS
REPO = HERE.parents[1]                            # repository root
VALIDATOR = HERE / "tools" / "validate_manifest_admission.py"
MANIFEST = REPO / "INTEGRATION" / "MANIFEST.json"
MIRROR = REPO / "INTEGRATION" / "FHS" / "docs" / "as-built" / "W0" / "r26" / "FHS_PIPD-LS-PKG_W0_r26.md"

sys.path.insert(0, str(HERE / "tools"))
import validate_manifest_admission as vma  # noqa: E402


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_validator(*args):
    """Run the validator exactly as CI/operator would; return (exit, parsed json, raw)."""
    proc = subprocess.run([sys.executable, str(VALIDATOR), *args],
                          cwd=str(REPO), capture_output=True, text=True)
    raw = (proc.stdout or "") + (proc.stderr or "")
    try:
        payload = json.loads(proc.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        payload = {}
    return proc.returncode, payload, raw


class AdmissionRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load(MANIFEST)
        cls.entry = cls.manifest["subject_admissions"][0]

    # ------------------------------------------------------------------ positive
    def test_manifest_is_still_parseable_and_schema_unchanged(self):
        self.assertEqual(self.manifest["schema"], "FABRIC-INTEGRATION-MIRROR/3")

    def test_admission_entry_present_and_navigation_only(self):
        self.assertEqual(self.entry["admission_state"], "ADMITTED_FOR_NAVIGATION_ONLY")
        self.assertEqual(self.entry["effect_permission"], "NONE")
        self.assertEqual(self.entry["claim_ceiling"],
                         "MIRROR_ADMITTED_FOR_NAVIGATION_WITH_BOUND_DIGEST_ONLY")

    def test_digest_is_the_one_the_mirrored_file_has(self):
        # Re-derived here, from bytes in this worktree — never from the record.
        measured_sha, measured_bytes = vma.sha256_of(MIRROR)
        self.assertEqual(self.entry["sha256"], measured_sha)
        self.assertEqual(self.entry["bytes"], measured_bytes)

    def test_effect_permission_matches_nav_surface(self):
        nav = load(HERE / "repository-map.json")
        self.assertEqual(nav["schema_version"], "FHS-NAV/v2")
        self.assertEqual(nav["effect_permission"], self.entry["effect_permission"])

    def test_source_identity(self):
        self.assertEqual(self.entry["source_repository"], "shw097-team/SBL")
        self.assertRegex(self.entry["source_commit"], r"^[0-9a-f]{40}$")

    def test_existing_entries_survive(self):
        for key in ("subjects", "binding", "purpose", "claim_ceiling", "published_at",
                    "excluded", "exceptions", "readiness_artifacts", "pending",
                    "non_claims", "approval_list_status"):
            self.assertIn(key, self.manifest)
        self.assertEqual(len(self.manifest["subjects"]), 4)

    def test_positive_run_passes(self):
        code, payload, raw = run_validator()
        self.assertEqual(code, 0, raw)
        self.assertEqual(payload.get("status"), "PASS")
        self.assertEqual(payload.get("code"), "OK")
        self.assertEqual(payload.get("admissions_checked"), 1)

    def test_payload_directory_untouched(self):
        # The admission lives beside the payload; the payload itself gained no file
        # and lost no byte. r26/SHA256SUMS is the payload's own inventory.
        payload = MIRROR.parent
        listed = {}
        for line in (payload / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
            if line.strip():
                digest, name = line.split(None, 1)
                listed[name.strip()] = digest
        self.assertEqual(len(listed), 9)
        # SHA256SUMS cannot list itself; nothing else may be present.
        self.assertEqual(sorted(set(listed) | {"SHA256SUMS"}),
                         sorted(p.name for p in payload.iterdir() if p.is_file()))
        for name, digest in listed.items():
            self.assertEqual(vma.sha256_of(payload / name)[0], digest, name)
        self.assertTrue(load(payload / "PROVENANCE.json")["bit_exact"])

    # ------------------------------------------------------------------ negatives
    def _tampered(self, mutate):
        entry = copy.deepcopy(self.entry)
        mutate(entry)
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        with handle:
            json.dump(entry, handle)
        self.addCleanup(Path(handle.name).unlink)
        return run_validator("--candidate-entry", handle.name)

    def test_neg_f1_digest_mismatch_is_refused(self):
        code, payload, raw = self._tampered(lambda e: e.__setitem__("sha256", "0" * 64))
        self.assertEqual(code, 2, raw)
        self.assertEqual(payload.get("code"), "MIRROR_DIGEST_MISMATCH")
        self.assertEqual(payload.get("status"), "REFUSED")

    def test_neg_f2_effect_escalation_is_refused(self):
        code, payload, raw = self._tampered(lambda e: e.__setitem__("effect_permission", "WRITE"))
        self.assertEqual(code, 2, raw)
        self.assertEqual(payload.get("code"), "EFFECT_PERMISSION_ESCALATION")

    def test_control_unchanged_entry_is_accepted_by_the_same_binary(self):
        # Without this control a NACK cannot be distinguished from "refuses everything".
        code, payload, raw = self._tampered(lambda e: e.__setitem__("admission_id", e["admission_id"]))
        self.assertEqual(code, 0, raw)
        self.assertEqual(payload.get("status"), "PASS")

    def test_claim_ceiling_escalation_is_refused(self):
        code, payload, raw = self._tampered(
            lambda e: e.__setitem__("claim_ceiling", "MIRROR_EXTERNALLY_ACCEPTED_AND_RELEASED"))
        self.assertEqual(code, 2, raw)
        self.assertIn("CLAIM_CEILING_ESCALATION", payload.get("errors", []))

    def test_consumption_state_under_none_is_refused(self):
        code, payload, raw = self._tampered(
            lambda e: e.__setitem__("admission_state", "ADMITTED_FOR_CONSUMPTION"))
        self.assertEqual(code, 2, raw)
        self.assertIn("ADMISSION_STATE_PERMISSION_MISMATCH", payload.get("errors", []))

    def test_size_mismatch_is_refused(self):
        code, payload, raw = self._tampered(lambda e: e.__setitem__("bytes", e["bytes"] + 1))
        self.assertEqual(code, 2, raw)
        self.assertIn("MIRROR_SIZE_MISMATCH", payload.get("errors", []))

    def test_unknown_field_is_refused(self):
        code, payload, raw = self._tampered(lambda e: e.__setitem__("write_authority", "REPO_PUSH"))
        self.assertEqual(code, 2, raw)
        self.assertIn("ADMISSION_FIELD_UNKNOWN", payload.get("errors", []))

    def test_additive_only_bites_when_an_older_entry_is_rewritten(self):
        baseline = copy.deepcopy(self.manifest)
        baseline.pop("subject_admissions", None)
        mutated = copy.deepcopy(self.manifest)
        mutated["claim_ceiling"] = "EXTERNALLY_ACCEPTED_AND_RELEASED"
        work = Path(self._tmp())
        (work / "baseline.json").write_text(json.dumps(baseline), encoding="utf-8")
        (work / "mutated.json").write_text(json.dumps(mutated), encoding="utf-8")
        code, payload, raw = run_validator("--manifest", str(work / "mutated.json"),
                                          "--baseline", str(work / "baseline.json"))
        self.assertEqual(code, 2, raw)
        self.assertEqual(payload.get("code"), "ADDITIVE_ONLY_VIOLATION")

    def test_unparseable_manifest_is_refused_not_crashed(self):
        work = Path(self._tmp())
        (work / "broken.json").write_text('{"schema": "FABRIC-INTEGRATION-MIRROR/3",', encoding="utf-8")
        code, payload, raw = run_validator("--manifest", str(work / "broken.json"))
        self.assertEqual(code, 2, raw)
        self.assertEqual(payload.get("code"), "MANIFEST_UNPARSEABLE")

    def test_duplicate_json_key_is_refused(self):
        work = Path(self._tmp())
        (work / "dup.json").write_text('{"schema": "FABRIC-INTEGRATION-MIRROR/3", "schema": "x"}',
                                       encoding="utf-8")
        code, payload, raw = run_validator("--manifest", str(work / "dup.json"))
        self.assertEqual(code, 2, raw)
        self.assertEqual(payload.get("code"), "MANIFEST_DUPLICATE_KEY")

    def _tmp(self):
        holder = tempfile.TemporaryDirectory()
        self.addCleanup(holder.cleanup)
        return holder.name


class TraceAndStatusTests(unittest.TestCase):
    """The two admission artifacts must stay bound to the record they describe."""

    ADMISSION_DIR = REPO / "INTEGRATION" / "FHS" / "docs" / "as-built" / "W0" / "r26-admission"

    def test_trace_shape_follows_f0_pattern(self):
        trace = load(self.ADMISSION_DIR / "F0_POLICY_CONSUMER_TRACE.json")
        self.assertEqual(trace["schema"], "RP002-F0-POLICY-CONSUMER-TRACE/1")
        for field in ("policy_artifact", "sha256", "consumer", "decision", "evidence"):
            self.assertIn(field, trace)
        self.assertEqual(trace["decision"], "ADMIT_MIRROR_FOR_NAVIGATION")
        self.assertTrue(trace["chain"])
        for step in trace["chain"]:
            self.assertIn("element", step)
            self.assertIn("evidence", step)
        self.assertEqual(trace["yaml_presence_alone"], "NOT_ACCEPTED")

    def test_trace_digest_is_the_manifest_digest(self):
        trace = load(self.ADMISSION_DIR / "F0_POLICY_CONSUMER_TRACE.json")
        entry = load(MANIFEST)["subject_admissions"][0]
        self.assertEqual(trace["sha256"], entry["sha256"])
        self.assertEqual(trace["sha256"], vma.sha256_of(MIRROR)[0])

    def test_status_file_says_navigation_only(self):
        text = (self.ADMISSION_DIR / "MIRROR_STATUS_FABRIC.md").read_text(encoding="utf-8")
        self.assertIn("ADMITTED_FOR_NAVIGATION_ONLY", text)
        self.assertIn("candidate / not policy loaded", text)
        self.assertIn("effect_permission", text)
        self.assertNotIn("ADMITTED_FOR_CONSUMPTION\n", text.split("## Why")[0])


if __name__ == "__main__":
    unittest.main()
