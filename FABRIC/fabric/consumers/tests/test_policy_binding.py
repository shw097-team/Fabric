# -*- coding: utf-8 -*-
"""WP-FHS-02 tests — the six legs stay separate and a document never stands in for a load.

Fixtures here are labelled `FIXTURE`: these tests prove the binding rules, not that a policy is
loaded anywhere. A host run would carry `evidence_class="HOST_RAW"` and is NOT_RUN in this round.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import policy_binding as pb  # noqa: E402

SHA_A = "a" * 64
SHA_B = "b" * 64
SCOPE = "fhs-w1/w2-prep"
EPOCH = 10


def six(**over):
    base = {
        "source": dict(digest=SHA_A, provenance="FABRIC_POLICY_SOURCE", reader="fabric-policy-repo"),
        "stage": dict(digest=SHA_A, provenance="STAGED_ARTIFACT", reader="fabric-stage-reader"),
        "owner_approved": dict(digest=SHA_A, provenance="OWNER_APPROVAL_RECEIPT", reader="owner-receipt-reader"),
        "active_epoch": dict(digest=SHA_A, provenance="ACTIVE_POLICY_POINTER", reader="fabric-active-pointer"),
        "loaded_digest": dict(digest=SHA_A, provenance="HOST_LOAD_RAW", reader="hgk-policy-consumer"),
        "consumer_ack": dict(digest=SHA_A, provenance="HGK_CONSUMER_RECEIPT", reader="hgk-consumer-trace"),
    }
    for name, patch in over.items():
        base[name] = dict(base[name], **patch)
    return [pb.leg(name, scope=SCOPE, epoch=EPOCH, evidence_class="FIXTURE", observed_at="2026-11-05T00:00:00Z", **kw)
            for name, kw in base.items()]


class TestPolicyBindingPositive(unittest.TestCase):
    def test_six_legs_bind_and_keep_their_own_readers(self):
        rec = pb.build_binding(policy_ref="policy/fhs-w1.yaml", scope=SCOPE, epoch=EPOCH, legs=six())
        self.assertEqual(rec["state"], "BOUND")
        self.assertEqual([l["leg"] for l in rec["legs"]], list(pb.LEGS))
        self.assertEqual(rec["separate_readers"], 6)
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


class TestPolicyBindingNegative(unittest.TestCase):
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
                   reader="hgk-policy-consumer", scope=SCOPE, epoch=EPOCH)
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
