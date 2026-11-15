# -*- coding: utf-8 -*-
"""D-24 — the first two legs have readers, and a real YAML->JSON stage is representable.

Three defects were measured on `policy_binding.py` before this patch, all of them on the legs whose
evidence is a file:

1. `leg("source", digest=<64 hex>, …)` accepted **any** digest. Nothing opened a file, so a
   fabricated 64-hex string with no artifact anywhere on disk substantiated the first leg;
2. `reader` was free text, so `reader="TOTALLY-MADE-UP-READER"` was accepted and
   `build_binding`'s `separate_readers` counted distinct *strings*;
3. `build_binding` required `stage.digest == source.digest`, so a genuine YAML->JSON stage — staged
   bytes differ from source bytes by definition — was refused as `POLICY_SOURCE_STAGE_DRIFT`. The
   only shape that passed was typing the source digest as the stage digest, a false pass.

Every negative test below is written to fail on the pre-patch module (where the hole is an ACCEPT).
Fixtures are real bytes in a temp dir. They are not host evidence: `claim_ceiling` stays
`AUTHOR_DESIGN_ONLY`, and the owner key used by the six-reader test is the FIXTURE key from
`test_policy_binding_forgery.py` — reachability, never an owner act.
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
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hgk_consumer_receipt as hcr  # noqa: E402
import policy_binding as pb  # noqa: E402
import policy_leg_readers as lr  # noqa: E402

try:  # the receipt builders (and the FIXTURE owner key) live in the D-17 test module
    import test_policy_binding_forgery as fx  # noqa: E402
except ImportError:  # pragma: no cover - only when the file is run out of tree
    fx = None

SUBJECT = "WP-FHS-02"
SCOPE = "fhs-w1/w2-prep"
EPOCH = 10
CONSUMER_ID = "hgk-policy-consumer"
POLICY_REF = "policy/fhs-w1.yaml"

#: The source policy, as YAML text.
POLICY_BYTES = b"rp002:\n  classes: 9\n  epoch: 10\n  legs: six\n"
POLICY_SHA = hashlib.sha256(POLICY_BYTES).hexdigest()
OTHER_BYTES = b"rp002:\n  classes: 9\n  epoch: 11\n  legs: six\n"
OTHER_SHA = hashlib.sha256(OTHER_BYTES).hexdigest()

#: What the YAML parses to, serialised as JSON. These are the *staged* bytes; they are not the
#: source bytes, which is the whole point of the second leg.
STAGE_PAYLOAD = {"rp002": {"classes": 9, "epoch": 10, "legs": "six"}}
STAGE_BYTES = lr.canonical_bytes(STAGE_PAYLOAD)
STAGE_SHA = hashlib.sha256(STAGE_BYTES).hexdigest()


def stage_document(*, source_sha256: str = POLICY_SHA, transform: str = "yaml->json",
                   payload: dict | None = None, stage_sha256: str | None = None) -> dict:
    payload = STAGE_PAYLOAD if payload is None else payload
    return {
        "schema": lr.SCHEMA_STAGE,
        "producer": {
            "source_sha256": source_sha256,
            "transform": transform,
            "stage_sha256": stage_sha256 or hashlib.sha256(lr.canonical_bytes(payload)).hexdigest(),
        },
        "payload": payload,
    }


def epoch_document(*, digest: str = POLICY_SHA, policy_path: str | None = "policy.yaml") -> dict:
    body = {"schema": lr.SCHEMA_EPOCH, "scope": SCOPE, "epoch": EPOCH, "digest": digest}
    if policy_path is not None:
        body["policy_path"] = policy_path
    return body


class _Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        (self.tmp / "policy.yaml").write_bytes(POLICY_BYTES)
        (self.tmp / "stage.json").write_text(json.dumps(stage_document(), indent=1),
                                             encoding="utf-8")
        (self.tmp / "epoch.json").write_text(json.dumps(epoch_document(), indent=1),
                                             encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, name: str, body: dict) -> Path:
        path = self.tmp / name
        path.write_text(json.dumps(body, indent=1), encoding="utf-8")
        return path

    def legs(self, **over) -> list[dict]:
        """The six legs. source/stage/active_epoch are read from the temp dir; the rest are typed."""
        spec = {
            "source": dict(digest=POLICY_SHA, provenance="FABRIC_POLICY_SOURCE",
                           reader=lr.READER_SOURCE, artifact=self.tmp / "policy.yaml"),
            "stage": dict(digest=STAGE_SHA, provenance="STAGED_ARTIFACT",
                          reader=lr.READER_STAGE, artifact=self.tmp / "stage.json"),
            "owner_approved": dict(digest=POLICY_SHA, provenance="OWNER_APPROVAL_RECEIPT",
                                   reader=lr.READER_OWNER),
            "active_epoch": dict(digest=POLICY_SHA, provenance="ACTIVE_POLICY_POINTER",
                                 reader=lr.READER_EPOCH, artifact=self.tmp / "epoch.json"),
            "loaded_digest": dict(digest=POLICY_SHA, provenance="HOST_LOAD_RAW",
                                  reader=lr.READER_LOAD),
            "consumer_ack": dict(digest=POLICY_SHA, provenance="HGK_CONSUMER_RECEIPT",
                                 reader=lr.READER_ACK),
        }
        for name, patch in over.items():
            spec[name] = dict(spec[name], **patch)
        return [pb.leg(name, scope=SCOPE, epoch=EPOCH, observed_at="2026-11-07T00:00:00Z", **kw)
                for name, kw in spec.items()]

    def bind(self, legs=None, **kw):
        return pb.build_binding(policy_ref=POLICY_REF, scope=SCOPE, epoch=EPOCH, subject=SUBJECT,
                                legs=self.legs() if legs is None else legs, **kw)


class TestSourceLegIsRead(_Base):
    """Defect 1 — the first leg's digest must be the sha256 of a file that exists."""

    def test_a_real_source_file_substantiates_the_first_leg(self):
        leg = pb.leg("source", digest=POLICY_SHA, provenance="FABRIC_POLICY_SOURCE",
                     reader=lr.READER_SOURCE, scope=SCOPE, epoch=EPOCH,
                     artifact=self.tmp / "policy.yaml")
        self.assertEqual(leg["digest"], POLICY_SHA)
        self.assertEqual(leg["reader"], lr.READER_SOURCE)
        self.assertTrue(leg["reader_verified"])
        self.assertEqual(leg["artifact_bytes"], len(POLICY_BYTES))
        self.assertEqual(leg["artifact_sha256"], POLICY_SHA)

    def test_a_digest_with_no_artifact_is_refused(self):
        """The pre-patch ACCEPT: any 64-hex string, with nothing on disk."""
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.leg("source", digest="a" * 64, provenance="FABRIC_POLICY_SOURCE",
                   reader=lr.READER_SOURCE, scope=SCOPE, epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "POLICY_SOURCE_UNREADABLE")
        self.assertIn("no artifact path", str(ctx.exception))

    def test_a_digest_that_is_not_the_file_digest_is_refused(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.leg("source", digest=OTHER_SHA, provenance="FABRIC_POLICY_SOURCE",
                   reader=lr.READER_SOURCE, scope=SCOPE, epoch=EPOCH,
                   artifact=self.tmp / "policy.yaml")
        self.assertEqual(ctx.exception.code, "POLICY_SOURCE_DIGEST_MISMATCH")

    def test_a_source_file_that_does_not_exist_is_refused(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.leg("source", digest=POLICY_SHA, provenance="FABRIC_POLICY_SOURCE",
                   reader=lr.READER_SOURCE, scope=SCOPE, epoch=EPOCH,
                   artifact=self.tmp / "nope.yaml")
        self.assertEqual(ctx.exception.code, "POLICY_SOURCE_UNREADABLE")

    def test_a_hand_built_source_leg_is_refused_at_build_time(self):
        """`build_binding` takes dicts, so the file is opened again there, not only in `leg()`."""
        legs = [dict(item) for item in self.legs()]
        legs[0] = {"leg": "source", "digest": "a" * 64, "provenance": "FABRIC_POLICY_SOURCE",
                   "reader": lr.READER_SOURCE, "scope": SCOPE, "epoch": EPOCH}
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(legs)
        self.assertEqual(ctx.exception.code, "POLICY_SOURCE_UNREADABLE")

    def test_a_source_deleted_after_the_leg_was_built_is_refused(self):
        legs = self.legs()
        (self.tmp / "policy.yaml").unlink()
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(legs)
        self.assertEqual(ctx.exception.code, "POLICY_SOURCE_UNREADABLE")

    def test_source_bytes_changed_after_the_leg_was_built_are_refused(self):
        legs = self.legs()
        (self.tmp / "policy.yaml").write_bytes(OTHER_BYTES)
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(legs)
        self.assertEqual(ctx.exception.code, "POLICY_SOURCE_DIGEST_MISMATCH")


class TestStageLegRepresentsTheTransform(_Base):
    """Defect 3 — a YAML->JSON stage is not drift, and a stage from other bytes is."""

    def test_a_real_yaml_to_json_stage_binds(self):
        """The pre-patch REFUSAL: staged bytes differ from source bytes, so this binding was
        impossible and the only passing shape typed the source digest as the stage digest."""
        record = self.bind()
        self.assertEqual(record["state"], "BOUND")
        self.assertEqual(record["stage"]["transform"], "yaml->json")
        self.assertEqual(record["stage"]["source_sha256"], POLICY_SHA)
        self.assertEqual(record["stage"]["stage_sha256"], STAGE_SHA)
        # The old rule was `stage.digest == source.digest`; a genuine stage fails it by
        # construction, which is exactly why it refused this record.
        self.assertNotEqual(record["digests"]["stage"], record["digests"]["source"])
        self.assertEqual(record["digests"]["stage"], STAGE_SHA)
        self.assertEqual(record["digests"]["source"], POLICY_SHA)

    def test_typing_the_source_digest_as_the_stage_digest_is_refused(self):
        """The old false pass: the stage digest copied from the source leg."""
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.leg("stage", digest=POLICY_SHA, provenance="STAGED_ARTIFACT",
                   reader=lr.READER_STAGE, scope=SCOPE, epoch=EPOCH,
                   artifact=self.tmp / "stage.json")
        self.assertEqual(ctx.exception.code, "POLICY_STAGE_DIGEST_MISMATCH")

    def test_a_stage_that_declares_another_source_is_drift(self):
        drift = self.write("stage-drift.json", stage_document(source_sha256=OTHER_SHA))
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(self.legs(stage=dict(artifact=drift)))
        self.assertEqual(ctx.exception.code, "POLICY_SOURCE_STAGE_DRIFT")

    def test_a_stage_that_declares_no_source_is_refused(self):
        body = stage_document()
        body["producer"].pop("source_sha256")
        path = self.write("stage-no-source.json", body)
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(self.legs(stage=dict(artifact=path)))
        self.assertEqual(ctx.exception.code, "POLICY_STAGE_UNREADABLE")

    def test_a_stage_with_no_producer_block_is_refused(self):
        path = self.write("stage-bare.json", {"schema": lr.SCHEMA_STAGE,
                                              "payload": STAGE_PAYLOAD})
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(self.legs(stage=dict(artifact=path)))
        self.assertEqual(ctx.exception.code, "POLICY_STAGE_UNREADABLE")
        self.assertIn("producer", str(ctx.exception))

    def test_a_stage_whose_payload_was_edited_after_staging_is_refused(self):
        body = stage_document()
        body["payload"] = {"rp002": {"classes": 9, "epoch": 11, "legs": "six"}}
        path = self.write("stage-edited.json", body)
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(self.legs(stage=dict(artifact=path)))
        self.assertEqual(ctx.exception.code, "POLICY_STAGE_DIGEST_MISMATCH")

    def test_a_missing_staged_file_is_refused(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(self.legs(stage=dict(artifact=self.tmp / "nope.json")))
        self.assertEqual(ctx.exception.code, "POLICY_STAGE_UNREADABLE")

    def test_a_stage_file_that_is_not_json_is_refused(self):
        path = self.tmp / "stage.txt"
        path.write_bytes(b"not json at all\n")
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(self.legs(stage=dict(artifact=path)))
        self.assertEqual(ctx.exception.code, "POLICY_STAGE_UNREADABLE")

    def test_a_stage_with_no_transform_is_refused(self):
        body = stage_document()
        body["producer"].pop("transform")
        path = self.write("stage-no-transform.json", body)
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(self.legs(stage=dict(artifact=path)))
        self.assertEqual(ctx.exception.code, "POLICY_STAGE_UNREADABLE")


class TestReaderIdentity(_Base):
    """Defect 2 — a reader is a registered callable, and the count is of readers that ran."""

    def test_an_unknown_reader_name_is_refused(self):
        """The pre-patch ACCEPT: `reader="TOTALLY-MADE-UP-READER"` built a leg."""
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.leg("source", digest=POLICY_SHA, provenance="FABRIC_POLICY_SOURCE",
                   reader="TOTALLY-MADE-UP-READER", scope=SCOPE, epoch=EPOCH,
                   artifact=self.tmp / "policy.yaml")
        self.assertEqual(ctx.exception.code, "POLICY_LEG_READER_UNKNOWN")
        self.assertIn("TOTALLY-MADE-UP-READER", str(ctx.exception))

    def test_an_unknown_reader_name_is_refused_on_a_typed_leg_too(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.leg("consumer_ack", digest=POLICY_SHA, provenance="HGK_CONSUMER_RECEIPT",
                   reader="hgk-consumer-trace", scope=SCOPE, epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "POLICY_LEG_READER_UNKNOWN")

    def test_a_reader_registered_for_another_leg_is_refused(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.leg("source", digest=POLICY_SHA, provenance="FABRIC_POLICY_SOURCE",
                   reader=lr.READER_STAGE, scope=SCOPE, epoch=EPOCH,
                   artifact=self.tmp / "policy.yaml")
        self.assertEqual(ctx.exception.code, "POLICY_LEG_READER_MISMATCH")

    def test_an_unknown_reader_on_a_hand_built_leg_is_refused_at_build_time(self):
        legs = [dict(item) for item in self.legs()]
        legs[1] = dict(legs[1], reader="TOTALLY-MADE-UP-READER")
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(legs)
        self.assertEqual(ctx.exception.code, "POLICY_LEG_READER_UNKNOWN")

    def test_an_unknown_reader_on_a_typed_leg_is_refused_at_build_time(self):
        legs = [dict(item) for item in self.legs()]
        legs[4] = dict(legs[4], reader="TOTALLY-MADE-UP-READER")
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(legs)
        self.assertEqual(ctx.exception.code, "POLICY_LEG_READER_UNKNOWN")

    def test_a_hand_built_unknown_leg_is_refused(self):
        legs = [dict(item) for item in self.legs()] + [
            {"leg": "policy_in_force", "digest": POLICY_SHA,
             "provenance": "FABRIC_POLICY_SOURCE", "reader": lr.READER_SOURCE,
             "scope": SCOPE, "epoch": EPOCH}]
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(legs)
        self.assertEqual(ctx.exception.code, "POLICY_LEG_UNKNOWN")

    def test_separate_readers_counts_readers_not_strings(self):
        """Six legs, six distinct registered names — but only three readers ran."""
        record = self.bind()
        self.assertEqual(len({item["reader"] for item in record["legs"]}), 6)
        self.assertEqual(record["separate_readers"], 3)
        self.assertEqual(record["verified_readers"],
                         sorted([lr.READER_SOURCE, lr.READER_STAGE, lr.READER_EPOCH]))

    def test_a_typed_leg_with_a_real_reader_name_does_not_count(self):
        """`host-load-receipt-reader` is a real reader; a hand-typed leg is still not its work."""
        legs = [dict(item, reader=lr.READER_LOAD) if item["leg"] == "loaded_digest" else item
                for item in self.legs()]
        record = self.bind(legs)
        self.assertNotIn(lr.READER_LOAD, record["verified_readers"])
        self.assertEqual(record["separate_readers"], 3)

    def test_the_registry_is_the_module_s_own_readers(self):
        """The registry is exactly this module's declared readers — no aliases, no foreign names.

        D-24 union: the fourth leg has two typed readers, because it has two documents
        (`ACTIVE_POLICY_POINTER@1` for a pointer holder, `FABRIC_ACTIVE_EPOCH@1` for the key holder).
        Both are this module's own callables, both declare the `active_epoch` leg, and their
        `evidence` kinds differ — so the registry still answers "which reader may substantiate which
        leg" and a fabricated name is still not a reader.
        """
        self.assertEqual(set(lr.READERS), set(lr.READER_NAMES))
        self.assertEqual(lr.READERS[lr.READER_SOURCE].leg, "source")
        self.assertEqual(lr.READERS[lr.READER_STAGE].leg, "stage")
        self.assertEqual(lr.READERS[lr.READER_EPOCH].leg, "active_epoch")
        self.assertEqual(lr.READERS[lr.READER_EPOCH_SIGNED].leg, "active_epoch")
        for name, entry in lr.READERS.items():
            with self.subTest(reader=name):
                self.assertEqual(entry.name, name)
                self.assertIn(entry.leg, pb.LEGS)
                self.assertIn(entry.evidence, {"artifact", "receipt"})
                # every registered reader is a callable this module defines, not a name it forwards
                self.assertEqual(entry.read.__module__, lr.__name__)
        self.assertNotEqual(lr.READERS[lr.READER_EPOCH].evidence,
                            lr.READERS[lr.READER_EPOCH_SIGNED].evidence)
        self.assertEqual(lr.READERS[lr.READER_EPOCH].evidence, "artifact")
        self.assertEqual(lr.READERS[lr.READER_EPOCH_SIGNED].evidence, "receipt")
        self.assertEqual(lr.READERS[lr.READER_EPOCH_SIGNED].name, pb.EPOCH_RECEIPT_READER)

    def test_the_registry_agrees_with_the_receipt_readers(self):
        import host_load_receipt
        import owner_approval_receipt
        self.assertEqual(pb.LOAD_RECEIPT_READER, host_load_receipt.READER)
        self.assertEqual(pb.OWNER_RECEIPT_READER, owner_approval_receipt.READER)
        self.assertEqual(pb.CONSUMER_ACK_RECEIPT_READER, hcr.READER)
        self.assertIn(pb.LOAD_RECEIPT_READER, lr.READERS)
        self.assertIn(pb.OWNER_RECEIPT_READER, lr.READERS)
        self.assertIn(pb.CONSUMER_ACK_RECEIPT_READER, lr.READERS)
        # D-24 union: the fourth leg's signed-receipt reader is registered too, for the same leg
        import fabric_active_epoch
        self.assertEqual(pb.EPOCH_RECEIPT_READER, fabric_active_epoch.READER)
        self.assertIn(pb.EPOCH_RECEIPT_READER, lr.READERS)
        self.assertEqual(lr.READERS[pb.EPOCH_RECEIPT_READER].leg, "active_epoch")


class TestSixVerifiedReaders(_Base):
    """The whole point of `separate_readers`: six legs, six readers that each opened something."""

    def setUp(self):
        super().setUp()
        if fx is None:
            self.skipTest("the D-17 receipt builders are not importable")
        if not fx.crypto_available():
            self.skipTest("`cryptography` (Ed25519) is not installed on this host")

    def test_six_verified_readers_bind(self):
        load = self.write("load.json", fx.load_document())
        ack = self.write("ack.json", fx.ack_document())
        owner = self.write("owner.json", fx.owner_document())
        verified_ack = hcr.load_receipt(ack, expected_subject=SUBJECT, expected_scope=SCOPE,
                                        expected_epoch=EPOCH, consumer_id=CONSUMER_ID)
        record = self.bind(consumer_ack_receipt=verified_ack, load_receipt=load,
                           owner_receipt=owner, owner_reader_sid=fx.FIXTURE_READER_SID,
                           owner_trusted_key_ids={fx.FIXTURE_KEY_ID})
        self.assertEqual(record["state"], "BOUND")
        self.assertEqual(record["claim_ceiling"], "AUTHOR_DESIGN_ONLY")
        self.assertEqual(record["separate_readers"], 6)
        self.assertEqual(record["verified_readers"],
                         sorted([lr.READER_SOURCE, lr.READER_STAGE, lr.READER_EPOCH,
                                 lr.READER_OWNER, lr.READER_LOAD, lr.READER_ACK]))
        # the stage still carries the transform, and its digest is still the staged bytes
        self.assertEqual(record["stage"]["transform"], "yaml->json")
        self.assertEqual(record["digests"]["stage"], STAGE_SHA)
        self.assertNotEqual(record["digests"]["stage"], record["digests"]["source"])


class TestCodesAreAdditive(unittest.TestCase):
    def test_d24_codes_are_distinct_and_new(self):
        self.assertEqual(len(set(pb.D24_REFUSAL_CODES)), len(pb.D24_REFUSAL_CODES))
        self.assertFalse(set(pb.D24_REFUSAL_CODES) & set(pb.D17_REFUSAL_CODES))
        for code in ("POLICY_SOURCE_STAGE_DRIFT", "POLICY_LEG_PROVENANCE_INVALID",
                     "POLICY_LEG_UNKNOWN", "POLICY_LEG_EMPTY"):
            self.assertNotIn(code, pb.D24_REFUSAL_CODES)

    def test_the_two_lane_vocabularies_are_both_present(self):
        """Neither lane's codes were dropped in the merge, and each is attributed to its emitter."""
        self.assertEqual(set(pb.D24_ARTIFACT_CODES) | set(pb.D24_RECEIPT_CODES)
                         | {pb.POLICY_LEG_EVIDENCE_MISMATCH}, set(pb.D24_REFUSAL_CODES))
        for code in ("POLICY_EPOCH_UNSUBSTANTIATED", "POLICY_EPOCH_KEY_UNPINNED",
                     "POLICY_OWNER_KEY_UNPINNED"):
            self.assertIn(code, pb.D24_RECEIPT_CODES)
        for code in ("POLICY_SOURCE_UNREADABLE", "POLICY_STAGE_UNREADABLE",
                     "POLICY_EPOCH_UNREADABLE", "POLICY_LEG_READER_UNKNOWN"):
            self.assertIn(code, pb.D24_ARTIFACT_CODES)
        # the artifact readers do not raise the receipt/owner codes: those are the binding's own
        self.assertFalse(set(lr.CODES) & set(pb.D24_RECEIPT_CODES))

    def test_every_d24_code_is_reachable_from_the_module(self):
        """Every code in the tuple is emitted by the binding or by a reader it calls — no dead names.

        D-24 union: the artifact-reader codes come from `policy_leg_readers`, the epoch/owner codes
        and the evidence-kind code are raised by `policy_binding` itself. A code that exists in the
        vocabulary but is never passed to a refusal would fail here.
        """
        sources = "\n".join((HERE / name).read_text(encoding="utf-8")
                            for name in ("policy_binding.py", "policy_leg_readers.py"))
        for code in pb.D24_REFUSAL_CODES:
            with self.subTest(code=code):
                self.assertIn(f'code="{code}"', sources)
        for code in lr.CODES:
            with self.subTest(reader_code=code):
                self.assertIn(f'code="{code}"', sources)


if __name__ == "__main__":
    unittest.main()
