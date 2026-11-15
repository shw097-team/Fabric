# -*- coding: utf-8 -*-
"""D-24 union — one leg, one evidence kind, through one typed reader.

Lane A gave `source`/`stage` real artifact readers; lane B gave `active_epoch` a signed
`FABRIC_ACTIVE_EPOCH@1` producer and reader. The OWNER ruling (2026-11-07) is that these are not
alternatives to choose between: every leg is substantiated by exactly one kind of evidence through
its own typed reader, and the two kinds may not impersonate each other. This module is the
executable form of that ruling:

* POSITIVE — `source` and `stage` opened from real files by the artifact readers **and**
  `active_epoch` verified from a signed receipt by the receipt reader bind together, and the record
  names which typed reader produced each leg;
* NEGATIVE — a receipt offered to `source`/`stage`, an artifact offered to `active_epoch`, a
  fabricated digest on any of those three legs, an unpinned epoch key, and a `HOST_LOAD_RECEIPT@1`
  that happens to carry `epoch=34` are each refused with a named code.

Fixtures are real bytes in a temp dir and a throwaway Ed25519 key labelled FIXTURE: a FIXTURE-signed
declaration proves the reader path is reachable, never that a Policy Owner declared anything.
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

import fabric_active_epoch as fe  # noqa: E402
import hgk_consumer_receipt as hcr  # noqa: E402
import policy_binding as pb  # noqa: E402
import policy_leg_readers as lr  # noqa: E402

try:  # the D-17 receipt builders (load / ack / owner documents)
    import test_policy_binding_forgery as fx  # noqa: E402
except ImportError:  # pragma: no cover - only when the file is run out of tree
    fx = None

SUBJECT = "WP-FHS-02"
SCOPE = "fhs-w1/w2-prep"
EPOCH = 10
PREVIOUS = 9
CONSUMER_ID = "hgk-policy-consumer"
POLICY_REF = "policy/fhs-w1.yaml"

POLICY_BYTES = b"rp002:\n  classes: 9\n  epoch: 10\n  legs: six\n"
POLICY_SHA = hashlib.sha256(POLICY_BYTES).hexdigest()
OTHER_BYTES = b"rp002:\n  classes: 9\n  epoch: 11\n  legs: six\n"
OTHER_SHA = hashlib.sha256(OTHER_BYTES).hexdigest()

#: The staged bytes: a real YAML->JSON transform of POLICY_BYTES, so STAGE_SHA != POLICY_SHA.
STAGE_PAYLOAD = {"rp002": {"classes": 9, "epoch": 10, "legs": "six"}}
STAGE_BYTES = lr.canonical_bytes(STAGE_PAYLOAD)
STAGE_SHA = hashlib.sha256(STAGE_BYTES).hexdigest()

FIXTURE_KEY_ID = "FIXTURE-EPOCH-KEY-D24-UNION-NOT-A-REAL-KEY"
FIXTURE_SEED = hashlib.sha256(b"D24 UNION FIXTURE EPOCH KEY - NOT A REAL KEY").digest()


def crypto_available() -> bool:
    try:
        import cryptography.hazmat.primitives.asymmetric.ed25519  # noqa: F401
    except ImportError:
        return False
    return True


def fixture_key():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    return Ed25519PrivateKey.from_private_bytes(FIXTURE_SEED)


def stage_document(*, source_sha256: str = POLICY_SHA, transform: str = "yaml->json") -> dict:
    return {
        "schema": lr.SCHEMA_STAGE,
        "producer": {"source_sha256": source_sha256, "transform": transform,
                     "stage_sha256": STAGE_SHA},
        "payload": STAGE_PAYLOAD,
    }


def epoch_pointer(*, digest: str = POLICY_SHA, policy_path: str | None = "policy.yaml") -> dict:
    body = {"schema": lr.SCHEMA_EPOCH, "scope": SCOPE, "epoch": EPOCH, "digest": digest}
    if policy_path is not None:
        body["policy_path"] = policy_path
    return body


class _Base(unittest.TestCase):
    def setUp(self):
        if not crypto_available():
            self.skipTest("`cryptography` (Ed25519) is not installed on this host")
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.policy = self.tmp / "policy.yaml"
        self.policy.write_bytes(POLICY_BYTES)
        (self.tmp / "other.yaml").write_bytes(OTHER_BYTES)
        self.stage = self.tmp / "stage.json"
        self.stage.write_text(json.dumps(stage_document(), indent=1), encoding="utf-8")
        self.pointer = self.tmp / "epoch-pointer.json"
        self.pointer.write_text(json.dumps(epoch_pointer(), indent=1), encoding="utf-8")
        self.key_file = self.tmp / "epoch-key.hex"
        from cryptography.hazmat.primitives import serialization
        self.key_file.write_text(fixture_key().private_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()).hex(), encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, name: str, body: dict) -> Path:
        path = self.tmp / name
        path.write_text(json.dumps(body, indent=1), encoding="utf-8")
        return path

    def produce(self, *, policy_name: str = "policy.yaml", out: str = "epoch.json",
                **over) -> Path:
        """Sign a real `FABRIC_ACTIVE_EPOCH@1` for the policy bytes at `policy_name`."""
        target = self.tmp / out
        kw: dict = dict(policy=self.tmp / policy_name, epoch=EPOCH, scope=SCOPE, subject=SUBJECT,
                        key_file=self.key_file, key_id=FIXTURE_KEY_ID, out=target,
                        previous_epoch=PREVIOUS)
        kw.update(over)
        fe.produce_epoch(**kw)
        return target

    def epoch_leg_from_receipt(self, receipt: Path, **over) -> dict:
        kw = dict(digest=POLICY_SHA, provenance=fe.PROVENANCE, reader=fe.READER, receipt=receipt,
                  evidence_class="HOST_RAW")
        kw.update(over)
        return pb.leg("active_epoch", scope=SCOPE, epoch=EPOCH,
                      observed_at="2026-11-07T00:00:00Z", **kw)

    def pointer_leg(self, **over) -> dict:
        kw = dict(digest=POLICY_SHA, provenance="ACTIVE_POLICY_POINTER", reader=lr.READER_EPOCH,
                  artifact=self.pointer, evidence_class="FIXTURE")
        kw.update(over)
        return pb.leg("active_epoch", scope=SCOPE, epoch=EPOCH,
                      observed_at="2026-11-07T00:00:00Z", **kw)

    def legs(self, *, epoch_leg: dict | None = None, **over) -> list[dict]:
        """The five legs whose evidence is not the epoch: source/stage read, three typed."""
        spec = {
            "source": dict(digest=POLICY_SHA, provenance="FABRIC_POLICY_SOURCE",
                           reader=lr.READER_SOURCE, artifact=self.policy),
            "stage": dict(digest=STAGE_SHA, provenance="STAGED_ARTIFACT",
                          reader=lr.READER_STAGE, artifact=self.stage),
            "owner_approved": dict(digest=POLICY_SHA, provenance="OWNER_APPROVAL_RECEIPT",
                                   reader=lr.READER_OWNER),
            "loaded_digest": dict(digest=POLICY_SHA, provenance="HOST_LOAD_RAW",
                                  reader=lr.READER_LOAD),
            "consumer_ack": dict(digest=POLICY_SHA, provenance="HGK_CONSUMER_RECEIPT",
                                 reader=lr.READER_ACK),
        }
        for name, patch in over.items():
            spec[name] = dict(spec[name], **patch)
        built = [pb.leg(name, scope=SCOPE, epoch=EPOCH, evidence_class="FIXTURE",
                        observed_at="2026-11-07T00:00:00Z", **kw)
                 for name, kw in spec.items()]
        if epoch_leg is not None:
            built.append(epoch_leg)
        return built

    def bind(self, legs=None, **kw):
        return pb.build_binding(policy_ref=POLICY_REF, scope=SCOPE, epoch=EPOCH, subject=SUBJECT,
                                legs=self.legs() if legs is None else legs, **kw)


class TestTheUnionBinds(_Base):
    """POSITIVE — artifact legs and a signed epoch leg in the same binding."""

    def test_source_and_stage_from_files_with_a_signed_epoch_bind(self):
        receipt = self.produce()
        record = self.bind(epoch_receipt=receipt, epoch_previous=PREVIOUS,
                           epoch_trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(record["state"], "BOUND")
        self.assertEqual([item["leg"] for item in record["legs"]], list(pb.LEGS))

        source, stage, epoch = record["legs"][0], record["legs"][1], record["legs"][3]
        self.assertEqual(source["reader"], lr.READER_SOURCE)
        self.assertEqual(source["substantiated_by"], "artifact")
        self.assertEqual(source["artifact"], str(self.policy))
        self.assertEqual(source["digest"], POLICY_SHA)
        self.assertEqual(stage["reader"], lr.READER_STAGE)
        self.assertEqual(stage["substantiated_by"], "artifact")
        self.assertEqual(stage["transform"], "yaml->json")
        self.assertEqual(stage["source_sha256"], POLICY_SHA)
        self.assertEqual(stage["digest"], STAGE_SHA)
        self.assertNotEqual(record["digests"]["stage"], record["digests"]["source"])

        self.assertEqual(epoch["reader"], fe.READER)
        self.assertEqual(epoch["provenance"], fe.PROVENANCE)
        self.assertEqual(epoch["substantiated_by"], "receipt")
        self.assertEqual(epoch["epoch_evidence"], "signed_receipt")
        self.assertEqual(epoch["digest"], POLICY_SHA)
        self.assertEqual(record["digests"]["active_epoch"], record["digests"]["source"])

        self.assertTrue(record["host"]["active_epoch_verified"])
        self.assertTrue(record["host"]["epoch_key_trusted"])
        self.assertEqual(record["host"]["active_epoch_reader"], fe.READER)
        self.assertEqual(record["host"]["active_epoch_evidence"], "signed_receipt")
        self.assertEqual(record["host"]["epoch_receipt_path"], str(receipt))
        self.assertEqual(record["claim_ceiling"], "AUTHOR_DESIGN_ONLY")

        self.assertEqual(record["separate_readers"], 3)
        self.assertEqual(record["verified_readers"],
                         sorted([lr.READER_SOURCE, lr.READER_STAGE, fe.READER]))

    def test_every_leg_records_which_kind_of_evidence_substantiated_it(self):
        receipt = self.produce()
        record = self.bind(epoch_receipt=receipt, epoch_previous=PREVIOUS,
                           epoch_trusted_key_ids={FIXTURE_KEY_ID})
        kinds = {item["leg"]: item["substantiated_by"] for item in record["legs"]}
        self.assertEqual(kinds, {"source": "artifact", "stage": "artifact",
                                 "owner_approved": "caller", "active_epoch": "receipt",
                                 "loaded_digest": "caller", "consumer_ack": "caller"})
        # only the fourth leg carries an epoch evidence kind, and only the read legs carry a path
        self.assertEqual([item["leg"] for item in record["legs"] if "epoch_evidence" in item],
                         ["active_epoch"])
        for name in ("source", "stage"):
            item = next(i for i in record["legs"] if i["leg"] == name)
            self.assertIn("artifact", item)
            self.assertNotIn("receipt_path", item)
        epoch = next(i for i in record["legs"] if i["leg"] == "active_epoch")
        self.assertIn("receipt_path", epoch)
        self.assertNotIn("artifact", epoch)

    def test_the_epoch_leg_built_by_leg_receipt_composes_with_the_rest(self):
        """`leg(..., receipt=…)` is the typed constructor the binding uses; it composes."""
        receipt = self.produce()
        epoch_leg = self.epoch_leg_from_receipt(receipt)
        self.assertEqual(epoch_leg["substantiated_by"], "receipt")
        self.assertEqual(epoch_leg["reader"], fe.READER)
        record = self.bind(self.legs(epoch_leg=epoch_leg), epoch_receipt=receipt,
                           epoch_previous=PREVIOUS, epoch_trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(record["state"], "BOUND")
        self.assertEqual(record["legs"][3]["substantiated_by"], "receipt")

    def test_six_typed_readers_one_per_leg_bind(self):
        """The whole point of `separate_readers`: six legs, six readers that each opened something."""
        if fx is None:  # pragma: no cover - only when the file is run out of tree
            self.skipTest("the D-17 receipt builders are not importable")
        receipt = self.produce()
        load = self.write("load.json", fx.load_document(POLICY_BYTES))
        ack = self.write("ack.json", fx.ack_document(POLICY_BYTES))
        owner = self.write("owner.json", fx.owner_document(POLICY_BYTES))
        verified_ack = hcr.load_receipt(ack, expected_subject=SUBJECT, expected_scope=SCOPE,
                                        expected_epoch=EPOCH, consumer_id=CONSUMER_ID)
        record = self.bind(consumer_ack_receipt=verified_ack, load_receipt=load,
                           owner_receipt=owner, owner_reader_sid=fx.FIXTURE_READER_SID,
                           owner_trusted_key_ids={fx.FIXTURE_KEY_ID},
                           epoch_receipt=receipt, epoch_previous=PREVIOUS,
                           epoch_trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(record["state"], "BOUND")
        self.assertEqual(record["separate_readers"], 6)
        self.assertEqual(record["verified_readers"],
                         sorted([lr.READER_SOURCE, lr.READER_STAGE, fe.READER, lr.READER_OWNER,
                                 lr.READER_LOAD, lr.READER_ACK]))
        self.assertEqual(record["legs"][3]["reader"], fe.READER)
        self.assertEqual(record["legs"][3]["substantiated_by"], "receipt")


class TestTheKindsCannotImpersonateEachOther(_Base):
    """NEGATIVE — one leg, one evidence kind. Impersonation is refused, never ignored."""

    def test_a_receipt_cannot_substantiate_the_source_leg(self):
        receipt = self.produce()
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.leg("source", digest=POLICY_SHA, provenance="FABRIC_POLICY_SOURCE",
                   reader=lr.READER_SOURCE, scope=SCOPE, epoch=EPOCH,
                   artifact=self.policy, receipt=receipt)
        self.assertEqual(ctx.exception.code, "POLICY_LEG_EVIDENCE_MISMATCH")

    def test_a_receipt_cannot_substantiate_the_stage_leg(self):
        receipt = self.produce()
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.leg("stage", digest=STAGE_SHA, provenance="STAGED_ARTIFACT",
                   reader=lr.READER_STAGE, scope=SCOPE, epoch=EPOCH,
                   artifact=self.stage, receipt=receipt)
        self.assertEqual(ctx.exception.code, "POLICY_LEG_EVIDENCE_MISMATCH")

    def test_the_receipt_reader_cannot_be_named_on_the_source_leg(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.leg("source", digest=POLICY_SHA, provenance="FABRIC_POLICY_SOURCE",
                   reader=lr.READER_EPOCH_SIGNED, scope=SCOPE, epoch=EPOCH,
                   artifact=self.policy)
        self.assertEqual(ctx.exception.code, "POLICY_LEG_READER_MISMATCH")

    def test_a_hand_built_source_leg_carrying_receipt_evidence_is_refused(self):
        receipt = self.produce()
        legs = [dict(item) for item in self.legs()]
        legs[0] = dict(legs[0], receipt_path=str(receipt),
                       receipt_sha256=hashlib.sha256(receipt.read_bytes()).hexdigest())
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(legs, epoch_receipt=receipt, epoch_previous=PREVIOUS,
                      epoch_trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(ctx.exception.code, "POLICY_LEG_EVIDENCE_MISMATCH")

    def test_an_artifact_cannot_substantiate_the_epoch_leg(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.leg("active_epoch", digest=POLICY_SHA, provenance=fe.PROVENANCE,
                   reader=fe.READER, scope=SCOPE, epoch=EPOCH, evidence_class="HOST_RAW",
                   artifact=self.pointer)
        self.assertEqual(ctx.exception.code, "POLICY_LEG_EVIDENCE_MISMATCH")

    def test_a_pointer_artifact_is_a_design_label_and_never_host_evidence(self):
        """The pointer reader stays exported, but a pointer leg claiming host evidence is refused."""
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(self.legs(epoch_leg=self.pointer_leg(evidence_class="HOST_RAW")))
        self.assertEqual(ctx.exception.code, "POLICY_EPOCH_UNSUBSTANTIATED")

    def test_a_pointer_artifact_binds_only_as_a_capped_design_label(self):
        record = self.bind(self.legs(epoch_leg=self.pointer_leg()))
        self.assertEqual(record["state"], "BOUND")
        self.assertEqual(record["claim_ceiling"], "AUTHOR_DESIGN_ONLY")
        self.assertFalse(record["host"]["active_epoch_verified"])
        self.assertEqual(record["host"]["active_epoch_evidence"], "pointer_design_only")
        self.assertIsNone(record["host"]["epoch_receipt_path"])
        self.assertEqual(record["legs"][3]["epoch_evidence"], "pointer_design_only")

    def test_the_signed_reader_name_without_a_receipt_is_refused(self):
        hand_built = {"leg": "active_epoch", "digest": POLICY_SHA,
                      "provenance": fe.PROVENANCE, "reader": fe.READER, "scope": SCOPE,
                      "epoch": EPOCH, "evidence_class": "HOST_RAW",
                      "substantiated_by": "receipt"}
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(self.legs(epoch_leg=hand_built))
        self.assertEqual(ctx.exception.code, "POLICY_EPOCH_UNSUBSTANTIATED")

    def test_a_hand_built_receipt_leg_with_a_path_but_no_epoch_receipt_is_refused(self):
        """A real receipt path plus a hand-set `key_trusted` is a claim, not a verification.

        Without the `epoch_receipt=` argument nothing opened the declaration, re-derived its digest or
        checked the signature against a pinned key — so the leg must not stand in for that work, even
        though every string on it is the right one.
        """
        receipt = self.produce()
        hand_built = {"leg": "active_epoch", "digest": POLICY_SHA,
                      "provenance": fe.PROVENANCE, "reader": fe.READER, "scope": SCOPE,
                      "epoch": EPOCH, "evidence_class": "HOST_RAW", "key_trusted": True,
                      "key_id": FIXTURE_KEY_ID, "substantiated_by": "receipt",
                      "receipt_path": str(receipt),
                      "receipt_sha256": hashlib.sha256(receipt.read_bytes()).hexdigest()}
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(self.legs(epoch_leg=hand_built))
        self.assertEqual(ctx.exception.code, "POLICY_EPOCH_UNSUBSTANTIATED")

    def test_a_hand_built_receipt_leg_carrying_an_artifact_is_refused(self):
        hand_built = {"leg": "active_epoch", "digest": POLICY_SHA,
                      "provenance": fe.PROVENANCE, "reader": fe.READER, "scope": SCOPE,
                      "epoch": EPOCH, "evidence_class": "HOST_RAW", "key_trusted": True,
                      "substantiated_by": "receipt", "artifact": str(self.pointer)}
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(self.legs(epoch_leg=hand_built))
        self.assertEqual(ctx.exception.code, "POLICY_LEG_EVIDENCE_MISMATCH")


class TestFabricatedEvidenceIsStillRefused(_Base):
    """NEGATIVE — a digest with no bytes behind it, on any of the three read legs."""

    def test_a_source_digest_with_no_artifact_is_refused(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.leg("source", digest="a" * 64, provenance="FABRIC_POLICY_SOURCE",
                   reader=lr.READER_SOURCE, scope=SCOPE, epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "POLICY_SOURCE_UNREADABLE")

    def test_a_source_digest_that_is_not_the_file_digest_is_refused(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.leg("source", digest=OTHER_SHA, provenance="FABRIC_POLICY_SOURCE",
                   reader=lr.READER_SOURCE, scope=SCOPE, epoch=EPOCH, artifact=self.policy)
        self.assertEqual(ctx.exception.code, "POLICY_SOURCE_DIGEST_MISMATCH")

    def test_a_stage_digest_that_is_not_the_staged_bytes_is_refused(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.leg("stage", digest=POLICY_SHA, provenance="STAGED_ARTIFACT",
                   reader=lr.READER_STAGE, scope=SCOPE, epoch=EPOCH, artifact=self.stage)
        self.assertEqual(ctx.exception.code, "POLICY_STAGE_DIGEST_MISMATCH")

    def test_an_epoch_digest_that_is_not_the_signed_digest_is_refused(self):
        receipt = self.produce()
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.epoch_leg_from_receipt(receipt, digest=OTHER_SHA)
        self.assertEqual(ctx.exception.code, "POLICY_EPOCH_DIGEST_MISMATCH")

    def test_a_receipt_for_other_bytes_cannot_substantiate_this_binding(self):
        receipt = self.produce(policy_name="other.yaml", out="epoch-other.json")
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(epoch_receipt=receipt, epoch_previous=PREVIOUS,
                      epoch_trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(ctx.exception.code, "EPOCH_DIGEST_MISMATCH")

    def test_an_unpinned_epoch_receipt_is_refused(self):
        receipt = self.produce()
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(epoch_receipt=receipt, epoch_previous=PREVIOUS)
        self.assertEqual(ctx.exception.code, "POLICY_EPOCH_KEY_UNPINNED")

    def test_a_host_load_receipt_with_epoch_34_is_not_an_epoch_declaration(self):
        """OWNER ruling (3): a load receipt that carries an epoch is a load receipt, not an epoch."""
        if fx is None:  # pragma: no cover - only when the file is run out of tree
            self.skipTest("the D-17 receipt builders are not importable")
        load = fx.load_document(POLICY_BYTES, epoch=34)
        self.assertEqual(load["schema"], "HOST_LOAD_RECEIPT@1")
        self.assertEqual(load["epoch"], 34)
        path = self.write("load-epoch-34.json", load)
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(epoch_receipt=path, epoch_previous=PREVIOUS,
                      epoch_trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(ctx.exception.code, "EPOCH_SCHEMA_MISMATCH")
        # The same document is a load receipt, not an epoch declaration: reading it as a load receipt
        # is a different leg and a different reader, and it is refused there for its own reason
        # (its epoch is 34, the binding's is 10), never silently accepted as an epoch.
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            self.bind(load_receipt=path)
        self.assertEqual(ctx.exception.code, "LOAD_RECEIPT_EPOCH_MISMATCH")
        self.assertIn("LOAD_RECEIPT_EPOCH_MISMATCH", ctx.exception.code)


if __name__ == "__main__":
    unittest.main()
