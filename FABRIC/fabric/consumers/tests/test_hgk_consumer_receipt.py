# -*- coding: utf-8 -*-
"""WP-FHS-02 — the sixth leg (`consumer_ack`) has a typed producer, and it cannot be faked.

What these tests are allowed to claim: the reader verifies the receipt it is given, a verified
receipt makes `consumer_ack` raw evidence, and *every* other path either returns `NOT_OBSERVED` or
refuses with an existing policy-binding code. What they are NOT allowed to claim: that any receipt
makes a policy active. `host_policy_active` stays in `not_claimed` on every success path, and
`host.consumer_ack_observed` is asserted to be false for every non-`HOST_RAW` receipt.

Receipts here are written to a temp dir. They are `HOST_RAW` in the reader's sense — the digest is
recomputed from bytes on disk — which is exactly why the last test class asserts what that flag does
*not* buy: no activation, no binding without the other five legs, no upgrade by relabelling.
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

import hgk_consumer_receipt as hcr  # noqa: E402
import policy_binding as pb  # noqa: E402

SUBJECT = "WP-FHS-02"
SCOPE = "fhs-w1/w2-prep"
EPOCH = 10
CONSUMER_ID = "hgk-policy-consumer"
POLICY_REF = "policy/fhs-w1.yaml"
RAW_BYTES = b"policy: fhs-w1\nepoch: 10\nlegs: six\n"
RAW_SHA = hashlib.sha256(RAW_BYTES).hexdigest()
SHA_A = "a" * 64
_DELETE = object()

REFUSAL_CODES = {"POLICY_LEG_PROVENANCE_INVALID", "POLICY_SIGNER_OR_EPOCH_DENY",
                 "POLICY_BINDING_INCOMPLETE", "POLICY_LEG_EMPTY",
                 "WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED", "POLICY_SOURCE_STAGE_DRIFT"}


def base_receipt() -> dict:
    return {
        "schema": hcr.SCHEMA,
        "subject": SUBJECT,
        "scope": SCOPE,
        "policy_epoch": EPOCH,
        "consumer_id": CONSUMER_ID,
        "policy_ref": POLICY_REF,
        "raw_path": "policy.yaml",
        "raw_sha256": RAW_SHA,
        "ack": {"acknowledged_at": "2026-11-05T00:00:00Z", "consumer": CONSUMER_ID},
        "observed_at": "2026-11-05T00:00:00Z",
    }


def write_case(directory: Path, *, raw: bytes = RAW_BYTES, **over) -> Path:
    """Write the acknowledged bytes and a receipt next to them; `over` patches/delete fields."""
    (directory / "policy.yaml").write_bytes(raw)
    body = base_receipt()
    for key, value in over.items():
        if value is _DELETE:
            body.pop(key, None)
        else:
            body[key] = value
    path = directory / "receipt.json"
    path.write_text(json.dumps(body, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def five_legs() -> list[dict]:
    """The five legs the receipt does NOT substantiate (deliberately without consumer_ack).

    `active_epoch`/`loaded_digest` carry the *acknowledged* digest rather than a placeholder: D-17
    made the sixth leg's digest bind to the loaded policy bytes, so a receipt for `RAW_BYTES` can
    only substantiate a binding of `RAW_BYTES`. That is the rule these fixtures now exercise.
    """
    spec = {
        "source": dict(digest=SHA_A, provenance="FABRIC_POLICY_SOURCE", reader="fabric-policy-repo"),
        "stage": dict(digest=SHA_A, provenance="STAGED_ARTIFACT", reader="fabric-stage-reader"),
        "owner_approved": dict(digest=SHA_A, provenance="OWNER_APPROVAL_RECEIPT",
                               reader="owner-receipt-reader"),
        "active_epoch": dict(digest=RAW_SHA, provenance="ACTIVE_POLICY_POINTER",
                             reader="fabric-active-pointer"),
        "loaded_digest": dict(digest=RAW_SHA, provenance="HOST_LOAD_RAW",
                              reader="hgk-policy-consumer"),
    }
    return [pb.leg(name, scope=SCOPE, epoch=EPOCH, evidence_class="FIXTURE",
                   observed_at="2026-11-05T00:00:00Z", **kw)
            for name, kw in spec.items()]


def fixture_consumer_ack(**over) -> dict:
    spec = dict(digest=SHA_A, provenance="HGK_CONSUMER_RECEIPT", reader="hgk-consumer-trace")
    spec.update(over)
    return pb.leg("consumer_ack", scope=SCOPE, epoch=EPOCH, evidence_class="FIXTURE",
                  observed_at="2026-11-05T00:00:00Z", **spec)


def bind(legs, receipt):
    return pb.build_binding(policy_ref=POLICY_REF, scope=SCOPE, epoch=EPOCH, legs=legs,
                            subject=SUBJECT, consumer_ack_receipt=receipt)


class TestReceiptReaderPositive(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_verified_receipt_is_a_host_raw_leg(self):
        receipt = write_case(self.tmp)
        leg = hcr.load_receipt(receipt, expected_subject=SUBJECT, expected_scope=SCOPE,
                               expected_epoch=EPOCH, consumer_id=CONSUMER_ID)
        self.assertEqual(leg["state"], "OBSERVED")
        self.assertEqual(leg["leg"], "consumer_ack")
        self.assertEqual(leg["provenance"], "HGK_CONSUMER_RECEIPT")
        self.assertEqual(leg["evidence_class"], "HOST_RAW")
        self.assertEqual(leg["reader"], hcr.READER)
        self.assertEqual(leg["digest"], RAW_SHA)          # re-derived, not copied on trust
        self.assertEqual(leg["scope"], SCOPE)
        self.assertEqual(leg["epoch"], EPOCH)
        self.assertEqual(leg["consumer_id"], CONSUMER_ID)
        self.assertEqual(leg["observed_at"], "2026-11-05T00:00:00Z")
        self.assertEqual(leg["receipt_sha256"], hashlib.sha256(receipt.read_bytes()).hexdigest())
        self.assertTrue(leg["verified"])
        self.assertTrue(hcr.is_verified_leg(leg))

    def test_receipt_fills_the_sixth_leg_and_binding_bounds(self):
        receipt = hcr.load_receipt(write_case(self.tmp), expected_subject=SUBJECT,
                                   expected_scope=SCOPE, expected_epoch=EPOCH,
                                   consumer_id=CONSUMER_ID)
        record = bind(five_legs(), receipt)
        self.assertEqual(record["state"], "BOUND")
        self.assertEqual([l["leg"] for l in record["legs"]], list(pb.LEGS))
        self.assertEqual(record["separate_readers"], 6)
        sixth = record["legs"][5]
        self.assertEqual(sixth["provenance"], "HGK_CONSUMER_RECEIPT")
        self.assertEqual(sixth["evidence_class"], "HOST_RAW")
        self.assertEqual(sixth["digest"], RAW_SHA)
        self.assertTrue(record["host"]["consumer_ack_observed"])
        self.assertTrue(record["host"]["consumer_ack_receipt_verified"])
        self.assertEqual(record["host"]["consumer_ack_reader"], hcr.READER)
        # a consumer ack is still not host activation
        self.assertFalse(record["host"]["loaded_on_host"])
        self.assertTrue(any(s.startswith("host_policy_active") for s in record["not_claimed"]))
        self.assertTrue(any("does not show" in s for s in record["not_claimed"]))

    def test_receipt_replaces_a_caller_supplied_sixth_leg(self):
        receipt = hcr.load_receipt(write_case(self.tmp), expected_subject=SUBJECT,
                                   expected_scope=SCOPE, expected_epoch=EPOCH,
                                   consumer_id=CONSUMER_ID)
        legs = five_legs() + [fixture_consumer_ack()]
        record = bind(legs, receipt)
        self.assertEqual(record["legs"][5]["reader"], hcr.READER)
        self.assertEqual(record["legs"][5]["evidence_class"], "HOST_RAW")
        # the caller's list is not mutated in place
        self.assertEqual(legs[5]["reader"], "hgk-consumer-trace")

    def test_without_a_receipt_nothing_changes_but_the_not_claimed_string(self):
        record = bind(five_legs() + [fixture_consumer_ack()], None)
        self.assertEqual(record["state"], "BOUND")
        self.assertFalse(record["host"]["consumer_ack_observed"])
        self.assertFalse(record["host"]["consumer_ack_receipt_verified"])
        self.assertIn("consumer consumption", record["not_claimed"])
        self.assertTrue(any("no HGK_CONSUMER_RECEIPT@1" in s for s in record["not_claimed"]))

    def test_reader_and_binding_agree_on_the_contract_values(self):
        self.assertEqual(pb.CONSUMER_ACK_RECEIPT_SCHEMA, hcr.SCHEMA)
        self.assertEqual(pb.CONSUMER_ACK_RECEIPT_PROVENANCE, hcr.PROVENANCE)
        self.assertEqual(pb.CONSUMER_ACK_RECEIPT_READER, hcr.READER)
        self.assertEqual(pb.CONSUMER_ACK_RECEIPT_EVIDENCE_CLASS, hcr.EVIDENCE_CLASS)
        self.assertIn(hcr.PROVENANCE, pb.LEG_PROVENANCE["consumer_ack"])


class TestReceiptReaderRefusals(unittest.TestCase):
    """Every bad receipt gets its own typed code — never a native ValueError/KeyError."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def read(self, path):
        return hcr.load_receipt(path, expected_subject=SUBJECT, expected_scope=SCOPE,
                                expected_epoch=EPOCH, consumer_id=CONSUMER_ID)

    def test_typed_codes_for_each_defect(self):
        cases = {
            "schema wrong": (dict(schema="HGK_CONSUMER_RECEIPT@2"), "HGK_RECEIPT_SCHEMA_MISMATCH"),
            "schema absent": (dict(schema=_DELETE), "HGK_RECEIPT_SCHEMA_MISMATCH"),
            "subject wrong": (dict(subject="WP-FHS-99"), "HGK_RECEIPT_SUBJECT_MISMATCH"),
            "scope wrong": (dict(scope="another/scope"), "HGK_RECEIPT_SCOPE_MISMATCH"),
            "epoch wrong": (dict(policy_epoch=EPOCH - 1), "HGK_RECEIPT_EPOCH_MISMATCH"),
            "consumer wrong": (dict(consumer_id="some-other-consumer"),
                               "HGK_RECEIPT_CONSUMER_MISMATCH"),
            "digest mismatch": (dict(raw_sha256="0" * 64), "HGK_RECEIPT_DIGEST_MISMATCH"),
            "digest not hex": (dict(raw_sha256="not-a-digest"), "HGK_RECEIPT_DIGEST_MISMATCH"),
            "digest absent": (dict(raw_sha256=_DELETE), "HGK_RECEIPT_DIGEST_MISMATCH"),
            "ack null": (dict(ack=None), "HGK_RECEIPT_MISSING_ACK"),
            "ack absent": (dict(ack=_DELETE), "HGK_RECEIPT_MISSING_ACK"),
            "ack empty": (dict(ack={}), "HGK_RECEIPT_MISSING_ACK"),
            "raw_path absent": (dict(raw_path=_DELETE), "HGK_RECEIPT_RAW_UNREADABLE"),
            "raw file absent": (dict(raw_path="nope.yaml"), "HGK_RECEIPT_RAW_UNREADABLE"),
        }
        for label, (over, expected) in cases.items():
            with self.subTest(label):
                with tempfile.TemporaryDirectory() as scratch:
                    receipt = write_case(Path(scratch), **over)
                    with self.assertRaises(hcr.HGKReceiptRefusal) as ctx:
                        self.read(receipt)
                    self.assertEqual(ctx.exception.code, expected)
                    self.assertIn(ctx.exception.code, hcr.CODES)
                    self.assertEqual(ctx.exception.leg, "consumer_ack")

    def test_malformed_documents_are_typed_not_native(self):
        broken = self.tmp / "broken.json"
        broken.write_bytes(b"{not json, ")
        with self.assertRaises(hcr.HGKReceiptRefusal) as ctx:
            self.read(broken)
        self.assertEqual(ctx.exception.code, "HGK_RECEIPT_MALFORMED")

        listed = self.tmp / "list.json"
        listed.write_text("[1, 2, 3]", encoding="utf-8")
        with self.assertRaises(hcr.HGKReceiptRefusal) as ctx:
            self.read(listed)
        self.assertEqual(ctx.exception.code, "HGK_RECEIPT_MALFORMED")

    def test_missing_receipt_is_not_observed_not_an_empty_leg(self):
        out = self.read(self.tmp / "does-not-exist.json")
        self.assertEqual(out["state"], "NOT_OBSERVED")
        self.assertEqual(out["code"], "HGK_RECEIPT_NOT_OBSERVED")
        self.assertIn("no receipt", out["reason"])
        self.assertEqual(out["evidence_class"], "NOT_OBSERVED")
        self.assertIsNone(out["leg"])
        for forbidden in ("digest", "provenance", "reader", "verified"):
            self.assertNotIn(forbidden, out)

    def test_directory_instead_of_receipt_is_unreadable_not_observed(self):
        out = self.read(self.tmp)
        self.assertEqual(out["state"], "NOT_OBSERVED")
        self.assertEqual(out["code"], "HGK_RECEIPT_UNREADABLE")

    def test_a_bad_receipt_never_binds(self):
        """The same defects, routed through build_binding, cannot produce BOUND."""
        receipt = write_case(self.tmp, subject="WP-FHS-99")
        with self.assertRaises(hcr.HGKReceiptRefusal):
            self.read(receipt)
        # a caller that swallowed the reader error and passed the raw document around still cannot
        # bind: the marker the reader adds is absent
        document = json.loads(receipt.read_text(encoding="utf-8"))
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(five_legs(), document)
        self.assertEqual(ctx.exception.code, "POLICY_LEG_PROVENANCE_INVALID")

    def test_not_observed_marker_is_refused_by_the_binding(self):
        marker = self.read(self.tmp / "does-not-exist.json")
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(five_legs(), marker)
        self.assertEqual(ctx.exception.code, "POLICY_LEG_PROVENANCE_INVALID")
        self.assertIn("NOT_OBSERVED", str(ctx.exception))


class TestNoPathToHostRawWithoutVerification(unittest.TestCase):
    """(3c) no receipt whose evidence_class is not HOST_RAW may set consumer_ack_observed."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.verified = hcr.load_receipt(
            write_case(self.tmp), expected_subject=SUBJECT, expected_scope=SCOPE,
            expected_epoch=EPOCH, consumer_id=CONSUMER_ID)

    def tearDown(self):
        self._tmp.cleanup()

    def test_relabelled_receipts_are_refused_and_never_flip_the_flag(self):
        mutations = [
            dict(evidence_class="FIXTURE"),
            dict(evidence_class="fixture"),
            dict(evidence_class="DESIGN_PROJECTION"),
            dict(evidence_class="NOT_OBSERVED"),
            dict(evidence_class=""),
            dict(evidence_class=None),
            dict(evidence_class="HOST_RAW "),
            dict(state="NOT_OBSERVED"),
            dict(verified=False),
            dict(verified="true"),
            dict(provenance="STAGE_MIRROR"),
            dict(provenance="HOST_LOAD_RAW"),
            dict(reader="hgk-consumer-trace"),
            dict(reader=""),
            dict(digest=None),
            dict(digest="not-a-digest"),
            dict(scope="another/scope"),
            dict(epoch=EPOCH - 1),
            dict(subject="WP-FHS-99"),
        ]
        for patch in mutations:
            with self.subTest(patch=patch):
                receipt = dict(self.verified, **patch)
                with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
                    bind(five_legs(), receipt)
                self.assertIn(ctx.exception.code, REFUSAL_CODES)
                self.assertNotEqual(ctx.exception.code, "BOUND")

    def test_bare_hand_built_dicts_are_refused(self):
        candidates = [
            {},
            None.__class__.__name__,                      # a string is not a receipt
            {"leg": "consumer_ack", "evidence_class": "HOST_RAW", "digest": RAW_SHA},
            {"leg": "consumer_ack", "provenance": "HGK_CONSUMER_RECEIPT", "reader": hcr.READER,
             "digest": RAW_SHA, "scope": SCOPE, "epoch": EPOCH, "evidence_class": "HOST_RAW"},
            [self.verified],
        ]
        for candidate in candidates:
            with self.subTest(candidate=type(candidate).__name__):
                with self.assertRaises(pb.PolicyBindingRefusal):
                    bind(five_legs(), candidate)

    def test_only_a_verified_receipt_can_set_the_flag_and_it_stays_honest(self):
        record = bind(five_legs(), self.verified)
        sixth = record["legs"][5]
        self.assertEqual(sixth["evidence_class"], "HOST_RAW")
        self.assertTrue(record["host"]["consumer_ack_observed"])
        # ...and even then: not active, not effective, not observed as a running host policy
        self.assertNotIn("host_policy_active", record["digests"])
        self.assertTrue(any("host_policy_active" in s for s in record["not_claimed"]))
        self.assertEqual(record["state"], "BOUND")

    def test_fixture_six_leg_without_a_receipt_never_sets_the_flag(self):
        record = bind(five_legs() + [fixture_consumer_ack()], None)
        self.assertFalse(record["host"]["consumer_ack_observed"])


class TestForgedSixthLegIsRefused(unittest.TestCase):
    """A dict is not evidence: the sixth leg must be re-derivable from bytes at binding time.

    The defect these tests pin: a hand-built dict that merely *looks* like the reader's output
    (`state=OBSERVED`, `verified=True`, `reader=…`, `evidence_class=HOST_RAW`, a 64-hex `digest`)
    used to set `host.consumer_ack_observed=True` and let the record reach `state=BOUND`, with no
    receipt and no acknowledged bytes existing anywhere. Every case below must refuse.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _forged(self, **over) -> dict:
        """Exactly the shape the binding checks, written by hand, with nothing on disk."""
        body = {
            "state": "OBSERVED", "leg": "consumer_ack", "digest": SHA_A,
            "provenance": hcr.PROVENANCE, "reader": hcr.READER, "scope": SCOPE, "epoch": EPOCH,
            "observed_at": "2026-11-06T00:00:00Z", "evidence_class": "HOST_RAW",
            "subject": SUBJECT, "consumer_id": CONSUMER_ID, "receipt_sha256": "d" * 64,
            "raw_path": str(self.tmp / "policy.yaml"), "receipt_path": str(self.tmp / "receipt.json"),
            "verified": True, "ack": {"ok": True},
        }
        body.update(over)
        return body

    def test_a_fully_populated_forgery_with_no_files_is_refused(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(five_legs(), self._forged())
        self.assertIn(ctx.exception.code, REFUSAL_CODES)

    def test_a_forgery_that_points_at_nonexistent_paths_is_refused(self):
        with self.assertRaises(pb.PolicyBindingRefusal):
            bind(five_legs(), self._forged(receipt_path=str(self.tmp / "nope.json"),
                                           raw_path=str(self.tmp / "nope.yaml")))

    def test_a_real_receipt_deleted_after_reading_is_refused(self):
        path = write_case(self.tmp)
        verified = hcr.load_receipt(path, expected_subject=SUBJECT, expected_scope=SCOPE,
                                    expected_epoch=EPOCH, consumer_id=CONSUMER_ID)
        self.assertEqual(verified["state"], "OBSERVED")
        self.assertTrue(bind(five_legs(), verified)["host"]["consumer_ack_observed"])
        # the same dict, after the bytes are gone, must stop substantiating anything
        (self.tmp / "receipt.json").unlink()
        (self.tmp / "policy.yaml").unlink()
        with self.assertRaises(pb.PolicyBindingRefusal):
            bind(five_legs(), verified)

    def test_a_receipt_whose_bytes_were_swapped_after_the_read_is_refused(self):
        path = write_case(self.tmp)
        verified = hcr.load_receipt(path, expected_subject=SUBJECT, expected_scope=SCOPE,
                                    expected_epoch=EPOCH, consumer_id=CONSUMER_ID)
        (self.tmp / "policy.yaml").write_bytes(b"policy: somebody-elses-bytes" + b"\n")
        with self.assertRaises(pb.PolicyBindingRefusal):
            bind(five_legs(), verified)

    def test_a_dict_pointing_at_another_subjects_receipt_is_refused(self):
        path = write_case(self.tmp)
        verified = hcr.load_receipt(path, expected_subject=SUBJECT, expected_scope=SCOPE,
                                    expected_epoch=EPOCH, consumer_id=CONSUMER_ID)
        with self.assertRaises(pb.PolicyBindingRefusal):
            pb.build_binding(policy_ref=POLICY_REF, scope=SCOPE, epoch=EPOCH, legs=five_legs(),
                             subject="WP-FHS-99", consumer_ack_receipt=verified)

    def test_the_reader_output_with_untouched_files_still_binds(self):
        path = write_case(self.tmp)
        verified = hcr.load_receipt(path, expected_subject=SUBJECT, expected_scope=SCOPE,
                                    expected_epoch=EPOCH, consumer_id=CONSUMER_ID)
        record = bind(five_legs(), verified)
        self.assertEqual(record["state"], "BOUND")
        self.assertTrue(record["host"]["consumer_ack_receipt_verified"])
        self.assertNotIn("host_policy_active", record["digests"])


class TestNonPositiveAckIsNeverPromoted(unittest.TestCase):
    """F03 / WP-FHS-02: only a positive ACK substantiates the sixth leg.

    Measured 2026-11-06 against Fabric main f1546ed + HG-KSEOS main a7046a3: a `NACK` and a
    `SCOPE_SPECIFIC_DEFERRED` receipt (perfect envelope, matching byte digest, real producer) both
    read as `state=OBSERVED` and set `host.consumer_ack_observed=True`. The envelope proves the
    receipt is authentic; it never proves the consumer agreed.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _read(self, **over):
        return hcr.load_receipt(write_case(self.tmp, **over), expected_subject=SUBJECT,
                                expected_scope=SCOPE, expected_epoch=EPOCH,
                                consumer_id=CONSUMER_ID)

    def test_nack_string_is_refused(self):
        with self.assertRaises(hcr.HGKReceiptRefusal) as ctx:
            self._read(ack="NACK")
        self.assertEqual(ctx.exception.code, "HGK_RECEIPT_NOT_ACK")

    def test_scope_specific_deferred_string_is_refused(self):
        with self.assertRaises(hcr.HGKReceiptRefusal) as ctx:
            self._read(ack="SCOPE_SPECIFIC_DEFERRED")
        self.assertEqual(ctx.exception.code, "HGK_RECEIPT_NOT_ACK")

    def test_structured_nack_decision_is_refused(self):
        with self.assertRaises(hcr.HGKReceiptRefusal) as ctx:
            self._read(ack={"decision": "NACK", "consumer": CONSUMER_ID})
        self.assertEqual(ctx.exception.code, "HGK_RECEIPT_NOT_ACK")

    def test_lowercase_ack_still_reads_as_positive(self):
        leg = self._read(ack="ack")
        self.assertEqual(leg["state"], "OBSERVED")
        self.assertTrue(hcr.is_positive_ack("ack"))

    def test_diagnostics_can_still_read_a_refusal(self):
        """Reading a NACK for diagnostics must stay possible — it just cannot fill a leg."""
        receipt = write_case(self.tmp, ack="NACK")
        leg = hcr.load_receipt(receipt, expected_subject=SUBJECT, expected_scope=SCOPE,
                               expected_epoch=EPOCH, consumer_id=CONSUMER_ID,
                               require_positive_ack=False)
        self.assertEqual(leg["state"], "OBSERVED")
        self.assertEqual(leg["ack"], "NACK")
        self.assertFalse(hcr.is_positive_ack(leg["ack"]))

    def test_build_binding_refuses_a_nack_receipt(self):
        receipt = write_case(self.tmp, ack="NACK")
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.build_binding(policy_ref=POLICY_REF, scope=SCOPE, epoch=EPOCH, legs=five_legs(),
                             subject=SUBJECT,
                             consumer_ack_receipt={"ack": "NACK", "state": "OBSERVED",
                                                   "verified": True,
                                                   "evidence_class": hcr.EVIDENCE_CLASS,
                                                   "provenance": hcr.PROVENANCE,
                                                   "reader": hcr.READER, "subject": SUBJECT,
                                                   "scope": SCOPE, "epoch": EPOCH,
                                                   "digest": RAW_SHA,
                                                   "receipt_path": str(receipt),
                                                   "raw_path": str(self.tmp / "policy.yaml"),
                                                   "consumer_id": CONSUMER_ID})
        self.assertEqual(ctx.exception.code, "POLICY_CONSUMER_NOT_ACK")

    def test_a_nack_receipt_never_reaches_consumer_ack_observed(self):
        for ack in ("NACK", "SCOPE_SPECIFIC_DEFERRED"):
            with self.subTest(ack=ack):
                with self.assertRaises(hcr.HGKReceiptRefusal):
                    self._read(ack=ack)


if __name__ == "__main__":
    unittest.main()
