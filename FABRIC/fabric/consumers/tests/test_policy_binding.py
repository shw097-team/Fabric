# -*- coding: utf-8 -*-
"""WP-FHS-02 tests — the six legs stay separate and a document never stands in for a load.

Fixtures here are labelled `FIXTURE`: these tests prove the binding rules, not that a policy is
loaded anywhere. A host run would carry `evidence_class="HOST_RAW"` and is NOT_RUN in this round.

D-24: the first three legs are read from real files in a temp dir, not typed. Before the patch
`six()` built `source`/`stage` with `digest=SHA_A` — a 64-hex string with no artifact behind it —
which is precisely the defect D-24 closes.
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import policy_binding as pb  # noqa: E402
import policy_leg_readers as lr  # noqa: E402

SHA_A = "a" * 64
SHA_B = "b" * 64
SCOPE = "fhs-w1/w2-prep"
EPOCH = 10

POLICY_BYTES = b"rp002:\n  classes: 9\n  epoch: 10\n  legs: six\n"
POLICY_SHA = hashlib.sha256(POLICY_BYTES).hexdigest()
#: The YAML->JSON stage of POLICY_BYTES. Its digest is *not* the source digest — that is the point.
STAGE_PAYLOAD = {"rp002": {"classes": 9, "epoch": 10, "legs": "six"}}
STAGE_BYTES = lr.canonical_bytes(STAGE_PAYLOAD)
STAGE_SHA = hashlib.sha256(STAGE_BYTES).hexdigest()

#: Set by `_Base.setUp`; `six()` reads the artifact legs from it.
FIXTURE_ROOT: Path | None = None


def stage_document(*, source_sha256: str = POLICY_SHA, transform: str = "yaml->json",
                   payload: dict | None = None) -> dict:
    payload = STAGE_PAYLOAD if payload is None else payload
    return {
        "schema": lr.SCHEMA_STAGE,
        "producer": {"source_sha256": source_sha256, "transform": transform,
                     "stage_sha256": hashlib.sha256(lr.canonical_bytes(payload)).hexdigest()},
        "payload": payload,
    }


def write_leg_fixtures(root: Path) -> None:
    """Write the three artifact legs' files and point `six()` at them."""
    global FIXTURE_ROOT
    FIXTURE_ROOT = root
    (root / "policy.yaml").write_bytes(POLICY_BYTES)
    (root / "stage.json").write_text(json.dumps(stage_document(), indent=1), encoding="utf-8")
    (root / "epoch.json").write_text(json.dumps({
        "schema": lr.SCHEMA_EPOCH, "scope": SCOPE, "epoch": EPOCH,
        "digest": POLICY_SHA, "policy_path": "policy.yaml"}), encoding="utf-8")


def six(**over):
    base = {
        "source": dict(digest=POLICY_SHA, provenance="FABRIC_POLICY_SOURCE",
                       reader=lr.READER_SOURCE, artifact=FIXTURE_ROOT / "policy.yaml"),
        "stage": dict(digest=STAGE_SHA, provenance="STAGED_ARTIFACT",
                      reader=lr.READER_STAGE, artifact=FIXTURE_ROOT / "stage.json"),
        "owner_approved": dict(digest=POLICY_SHA, provenance="OWNER_APPROVAL_RECEIPT",
                               reader=lr.READER_OWNER),
        "active_epoch": dict(digest=POLICY_SHA, provenance="ACTIVE_POLICY_POINTER",
                             reader=lr.READER_EPOCH, artifact=FIXTURE_ROOT / "epoch.json"),
        "loaded_digest": dict(digest=POLICY_SHA, provenance="HOST_LOAD_RAW", reader=lr.READER_LOAD),
        "consumer_ack": dict(digest=POLICY_SHA, provenance="HGK_CONSUMER_RECEIPT",
                             reader=lr.READER_ACK),
    }
    for name, patch in over.items():
        base[name] = dict(base[name], **patch)
    return [pb.leg(name, scope=SCOPE, epoch=EPOCH, evidence_class="FIXTURE",
                   observed_at="2026-11-05T00:00:00Z", **kw)
            for name, kw in base.items()]


class _Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        write_leg_fixtures(self.tmp)

    def tearDown(self):
        self._tmp.cleanup()


class TestPolicyBindingPositive(_Base):
    def test_six_legs_bind_and_keep_their_own_readers(self):
        rec = pb.build_binding(policy_ref="policy/fhs-w1.yaml", scope=SCOPE, epoch=EPOCH, legs=six())
        self.assertEqual(rec["state"], "BOUND")
        self.assertEqual([l["leg"] for l in rec["legs"]], list(pb.LEGS))
        # D-24: this used to assert 6 because six *strings* were distinct. Only the three artifact
        # legs were read by a reader here; owner_approved / loaded_digest / consumer_ack are typed
        # by the caller in this fixture, so they count for nothing. The full six-reader case is
        # `test_policy_binding_leg_readers.py::test_six_verified_readers_bind`.
        self.assertEqual(rec["separate_readers"], 3)
        self.assertEqual(rec["verified_readers"],
                         sorted([lr.READER_SOURCE, lr.READER_STAGE, lr.READER_EPOCH]))
        self.assertEqual(rec["claim_ceiling"], "AUTHOR_DESIGN_ONLY")
        # fixture evidence is never reported as a host load
        self.assertFalse(rec["host"]["loaded_on_host"])
        self.assertFalse(rec["host"]["consumer_ack_observed"])

    def test_host_raw_claim_without_a_receipt_is_refused(self):
        """D-17: `HOST_RAW` is a claim about a host artifact, so it needs one.

        Before the patch this test asserted the opposite — that a caller-typed
        `evidence_class="HOST_RAW"` on the fifth and sixth legs flipped `loaded_on_host` and
        `consumer_ack_observed` to True with no receipt in existence. That is the defect D-17
        repairs; the raws are in `inc5/out/D17_REPAIR.md`.
        """
        legs = [dict(item, evidence_class="HOST_RAW") if item["leg"] == "loaded_digest" else item
                for item in six()]
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.build_binding(policy_ref="policy/fhs-w1.yaml", scope=SCOPE, epoch=EPOCH, legs=legs)
        self.assertEqual(ctx.exception.code, "POLICY_LOAD_UNSUBSTANTIATED")

        legs = [dict(item, evidence_class="HOST_RAW") if item["leg"] == "consumer_ack" else item
                for item in six()]
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.build_binding(policy_ref="policy/fhs-w1.yaml", scope=SCOPE, epoch=EPOCH, legs=legs)
        self.assertEqual(ctx.exception.code, "POLICY_CONSUMER_ACK_UNSUBSTANTIATED")

    def test_binding_digest_is_replay_stable(self):
        a = pb.build_binding(policy_ref="p", scope=SCOPE, epoch=EPOCH, legs=six())
        b = pb.build_binding(policy_ref="p", scope=SCOPE, epoch=EPOCH, legs=six())
        self.assertEqual(a["binding_sha256"], b["binding_sha256"])


class TestPolicyBindingNegative(_Base):
    def test_stage_document_cannot_substantiate_loaded(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.build_binding(policy_ref="p", scope=SCOPE, epoch=EPOCH,
                             legs=six(loaded_digest=dict(provenance="STAGED_ARTIFACT")))
        self.assertEqual(ctx.exception.code, "WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED")

    def test_nav_assisted_use_approval_cannot_substantiate_loaded(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.build_binding(policy_ref="p", scope=SCOPE, epoch=EPOCH,
                             legs=six(loaded_digest=dict(provenance="NAV_ASSISTED_USE_APPROVED")))
        self.assertIn("POLICY_NOT_LOADED", ctx.exception.code)

    def test_loaded_bytes_must_equal_active_epoch_bytes(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.build_binding(policy_ref="p", scope=SCOPE, epoch=EPOCH,
                             legs=six(loaded_digest=dict(digest=SHA_B)))
        self.assertEqual(ctx.exception.code, "WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED")

    def test_cross_scope_leg_is_refused(self):
        legs = six()
        legs[4] = dict(legs[4], scope="another/scope")
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.build_binding(policy_ref="p", scope=SCOPE, epoch=EPOCH, legs=legs)
        self.assertEqual(ctx.exception.code, "POLICY_SIGNER_OR_EPOCH_DENY")

    def test_stale_epoch_leg_is_refused(self):
        legs = six()
        legs[3] = dict(legs[3], epoch=EPOCH - 1)
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.build_binding(policy_ref="p", scope=SCOPE, epoch=EPOCH, legs=legs)
        self.assertEqual(ctx.exception.code, "POLICY_SIGNER_OR_EPOCH_DENY")

    def test_missing_leg_is_incomplete_not_passed(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.build_binding(policy_ref="p", scope=SCOPE, epoch=EPOCH, legs=six()[:5])
        self.assertEqual(ctx.exception.code, "POLICY_BINDING_INCOMPLETE")

    def test_provenance_outside_its_reader_set_is_refused(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.leg("consumer_ack", digest=SHA_A, provenance="HOST_LOAD_RAW",
                   reader=lr.READER_ACK, scope=SCOPE, epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "POLICY_LEG_PROVENANCE_INVALID")

    def test_document_claiming_loaded_is_refused(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.refuse_document_claim({"state": "LOADED", "provenance": "STAGE_MIRROR"})
        self.assertEqual(ctx.exception.code, "WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED")

    def test_document_claiming_loaded_from_a_real_pointer_is_not_refused(self):
        out = pb.refuse_document_claim({"state": "LOADED", "provenance": "HOST_LOAD_RAW"})
        self.assertEqual(out["state"], "DOCUMENT_CLAIM_NOT_A_LOAD_RECEIPT")


if __name__ == "__main__":
    unittest.main()
