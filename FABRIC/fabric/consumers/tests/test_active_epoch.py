# -*- coding: utf-8 -*-
"""D-24 — the fourth leg gets an artifact: `FABRIC_ACTIVE_EPOCH@1`, producer and reader.

Before this module the repository contained the string `FABRIC_ACTIVE_EPOCH` **zero** times, and
`policy_binding.LEG_PROVENANCE["active_epoch"]` named two provenances no function read. The fourth
leg was therefore whatever the caller typed, constrained only by digest equality with a digest the
same caller supplied — the D-17 defect (a label with no reader) one leg over.

Every test below fails on the pre-D-24 module (where the hole is an ACCEPT) and passes here. Fixtures
are real bytes in a temp dir and a throwaway Ed25519 key labelled FIXTURE: a FIXTURE-signed epoch
proves the reader path is reachable and never that a host activated anything.
"""
from __future__ import annotations

import base64
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import fabric_active_epoch as fe  # noqa: E402
import policy_binding as pb  # noqa: E402

SUBJECT = "WP-FHS-02"
SCOPE = "fhs-w1/w2-prep"
EPOCH = 11
PREVIOUS = 10
POLICY_REF = "policy/fhs-w1.yaml"
POLICY_BYTES = b"rp002:\n  classes: 9\n  epoch: 11\n  legs: six\n"
POLICY_SHA = hashlib.sha256(POLICY_BYTES).hexdigest()
OTHER_BYTES = b"rp002:\n  classes: 9\n  epoch: 12\n  legs: six\n"
OTHER_SHA = hashlib.sha256(OTHER_BYTES).hexdigest()

FIXTURE_KEY_ID = "FIXTURE-EPOCH-KEY-D24-NOT-A-REAL-KEY"
FIXTURE_SEED = hashlib.sha256(b"D24 FIXTURE EPOCH KEY - NOT A REAL KEY").digest()

PRE_EXISTING_CODES = {
    "POLICY_LEG_UNKNOWN", "POLICY_LEG_EMPTY", "POLICY_LEG_PROVENANCE_INVALID",
    "POLICY_BINDING_INCOMPLETE", "POLICY_SIGNER_OR_EPOCH_DENY", "POLICY_SOURCE_STAGE_DRIFT",
    "POLICY_CONSUMER_NOT_ACK", "WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED",
    "POLICY_LOADED_PROVENANCE_NOT_A_LOAD_RECEIPT", "POLICY_LOAD_UNSUBSTANTIATED",
    "POLICY_CONSUMER_ACK_UNSUBSTANTIATED", "POLICY_CONSUMER_ACK_DIGEST_MISMATCH",
    "POLICY_OWNER_APPROVAL_UNSUBSTANTIATED", "OWNER_RECEIPT_DIGEST_MISMATCH",
}


def crypto_available() -> bool:
    try:
        import cryptography.hazmat.primitives.asymmetric.ed25519  # noqa: F401
    except ImportError:
        return False
    return True


def fixture_key():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    return Ed25519PrivateKey.from_private_bytes(FIXTURE_SEED)


def fixture_public_b64() -> str:
    from cryptography.hazmat.primitives import serialization
    raw = fixture_key().public_key().public_bytes(encoding=serialization.Encoding.Raw,
                                                  format=serialization.PublicFormat.Raw)
    return base64.b64encode(raw).decode()


class _Delete:
    def __repr__(self) -> str:  # pragma: no cover - repr only
        return "<DELETE>"


_DELETE = _Delete()


def epoch_document(raw: bytes = POLICY_BYTES, *, policy_name: str = "policy.yaml",
                   sign: bool = True, **over) -> dict:
    """A well-formed `FABRIC_ACTIVE_EPOCH@1` signed with the FIXTURE key (or left unsigned).

    Built here rather than through `produce_epoch` so a test can state a document that the producer
    would refuse to write (an expired window, an epoch below the previous one) and check that the
    *reader* refuses it too.
    """
    now = dt.datetime.now(dt.timezone.utc)
    body = {
        "schema": fe.SCHEMA,
        "kind": "FABRIC_ACTIVE_EPOCH",
        "state": fe.STATE_DECLARED,
        "claim_ceiling": fe.CLAIM_CEILING,
        "subject": SUBJECT,
        "scope": SCOPE,
        "epoch": EPOCH,
        "previous_epoch": PREVIOUS,
        "policy": {"path": policy_name, "ref": policy_name,
                   "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)},
        "issued_at": (now - dt.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "expires_at": (now + dt.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "key": {"key_id": FIXTURE_KEY_ID, "alg": "ED25519",
                "public_key_b64": fixture_public_b64()},
        "producer": {"tool": "test-fixture", "version": "1",
                     "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ")},
    }
    for key, value in over.items():
        if value is _DELETE:
            body.pop(key, None)
        else:
            body[key] = value
    if sign:
        message = fe.canonical_body(body)
        body["signature"] = {
            "key_id": body["key"]["key_id"], "alg": "ED25519",
            "sig_b64": base64.b64encode(fixture_key().sign(message)).decode(),
            "signed_body_sha256": hashlib.sha256(message).hexdigest(),
        }
    return body


def six_legs(digest: str = POLICY_SHA, *, active_digest: str | None = None,
             active_provenance: str = "ACTIVE_POLICY_POINTER",
             active_evidence: str = "FIXTURE") -> list[dict]:
    """Six legs, the fourth one a caller-typed label unless a receipt replaces it."""
    spec = {
        "source": dict(digest=digest, provenance="FABRIC_POLICY_SOURCE", reader="fabric-policy-repo"),
        "stage": dict(digest=digest, provenance="STAGED_ARTIFACT", reader="fabric-stage-reader"),
        "owner_approved": dict(digest=digest, provenance="OWNER_APPROVAL_RECEIPT",
                               reader="owner-receipt-reader"),
        "active_epoch": dict(digest=active_digest or digest, provenance=active_provenance,
                             reader="fabric-active-pointer"),
        "loaded_digest": dict(digest=digest, provenance="HOST_LOAD_RAW",
                              reader="host-load-receipt-reader"),
        "consumer_ack": dict(digest=digest, provenance="HGK_CONSUMER_RECEIPT",
                             reader="hgk-consumer-receipt-reader"),
    }
    legs = []
    for name, kw in spec.items():
        evidence = active_evidence if name == "active_epoch" else "FIXTURE"
        legs.append(pb.leg(name, scope=SCOPE, epoch=EPOCH, evidence_class=evidence,
                           observed_at="2026-11-07T00:00:00Z", **kw))
    return legs


def bind(legs, **kw):
    return pb.build_binding(policy_ref=POLICY_REF, scope=SCOPE, epoch=EPOCH, subject=SUBJECT,
                            legs=legs, **kw)


class _Base(unittest.TestCase):
    def setUp(self):
        if not crypto_available():
            self.skipTest("`cryptography` (Ed25519) is not installed on this host")
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        (self.tmp / "policy.yaml").write_bytes(POLICY_BYTES)
        (self.tmp / "other.yaml").write_bytes(OTHER_BYTES)
        self.key_file = self.tmp / "epoch-key.hex"
        from cryptography.hazmat.primitives import serialization
        self.key_file.write_text(fixture_key().private_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()).hex(), encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def write_epoch(self, name: str = "epoch.json", raw: bytes = POLICY_BYTES, **over) -> Path:
        path = self.tmp / name
        path.write_text(json.dumps(epoch_document(raw, **over), indent=1), encoding="utf-8")
        return path

    def produce(self, **over) -> Path:
        out = self.tmp / over.pop("out", "produced.json")
        kw: dict[str, Any] = dict(policy=self.tmp / "policy.yaml", epoch=EPOCH, scope=SCOPE, subject=SUBJECT,
                  key_file=self.key_file, key_id=FIXTURE_KEY_ID, out=out, previous_epoch=PREVIOUS)
        kw.update(over)
        fe.produce_epoch(**kw)
        return out

    def read(self, path: Path, **over):
        kw = dict(expected_scope=SCOPE, expected_epoch=EPOCH, previous_epoch=PREVIOUS)
        kw.update(over)
        return fe.read_epoch_receipt(path, **kw)


class TestEpochReaderPositive(_Base):
    def test_a_produced_epoch_verifies_and_carries_its_own_provenance(self):
        path = self.produce()
        leg = self.read(path, trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(leg["state"], "OBSERVED")
        self.assertEqual(leg["leg"], "active_epoch")
        self.assertEqual(leg["provenance"], fe.PROVENANCE)
        self.assertEqual(leg["reader"], fe.READER)
        self.assertEqual(leg["digest"], POLICY_SHA)
        self.assertEqual(leg["epoch"], EPOCH)
        self.assertTrue(leg["key_trusted"])
        self.assertTrue(fe.is_verified_epoch_leg(leg))

    def test_an_unpinned_read_is_reported_untrusted_and_a_pinned_one_checked(self):
        path = self.produce()
        self.assertFalse(fe.read_epoch_receipt(path, expected_scope=SCOPE)["key_trusted"])
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.read(path, trusted_key_ids={"SOME-OTHER-KEY"})
        self.assertEqual(ctx.exception.code, "EPOCH_KEY_UNTRUSTED")

    def test_the_epoch_leg_binds_and_the_record_says_what_it_is_not(self):
        path = self.produce()
        record = bind(six_legs(), epoch_receipt=path, epoch_previous=PREVIOUS,
                      epoch_trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(record["state"], "BOUND")
        self.assertEqual(record["claim_ceiling"], "AUTHOR_DESIGN_ONLY")
        self.assertTrue(record["host"]["active_epoch_verified"])
        self.assertTrue(record["host"]["epoch_key_trusted"])
        self.assertEqual(record["host"]["active_epoch_reader"], fe.READER)
        epoch_leg = record["legs"][3]
        self.assertEqual(epoch_leg["leg"], "active_epoch")
        self.assertEqual(epoch_leg["provenance"], fe.PROVENANCE)
        self.assertEqual(epoch_leg["reader"], fe.READER)
        self.assertEqual(epoch_leg["digest"], POLICY_SHA)
        caveat = [s for s in record["not_claimed"] if s.startswith("active_epoch")]
        self.assertTrue(caveat)
        self.assertIn("does not show a host loaded it", caveat[0])

    def test_the_reader_result_is_accepted_as_well_as_the_path(self):
        path = self.produce()
        leg = self.read(path, trusted_key_ids={FIXTURE_KEY_ID})
        record = bind(six_legs(), epoch_receipt=leg, epoch_previous=PREVIOUS,
                      epoch_trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(record["state"], "BOUND")
        self.assertEqual(record["legs"][3]["provenance"], fe.PROVENANCE)

    def test_the_receipt_digest_replaces_a_caller_typed_digest(self):
        """The caller's fourth-leg digest is not trusted: the reader re-derives it from disk."""
        path = self.produce()
        record = bind(six_legs(active_digest=OTHER_SHA), epoch_receipt=path,
                      epoch_previous=PREVIOUS, epoch_trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(record["state"], "BOUND")
        self.assertEqual(record["legs"][3]["digest"], POLICY_SHA)
        self.assertEqual(record["digests"]["active_epoch"], POLICY_SHA)


class TestEpochReaderNegative(_Base):
    def test_an_expired_declaration_is_refused(self):
        path = self.write_epoch()
        later = dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=2)
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.read(path, now=later)
        self.assertEqual(ctx.exception.code, "EPOCH_EXPIRED")
        self.assertIn("EPOCH_EXPIRED", fe.CODES)

    def test_a_window_that_does_not_move_forward_is_refused(self):
        now = dt.datetime.now(dt.timezone.utc)
        stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        path = self.write_epoch(expires_at=stamp, issued_at=stamp)
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.read(path)
        self.assertEqual(ctx.exception.code, "EPOCH_TIME_INVALID")

    def test_a_declaration_for_other_bytes_is_refused(self):
        path = self.write_epoch(raw=OTHER_BYTES, policy_name="other.yaml")
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.read(path, expected_policy_sha256=POLICY_SHA)
        self.assertEqual(ctx.exception.code, "EPOCH_DIGEST_MISMATCH")
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(six_legs(), epoch_receipt=path, epoch_previous=PREVIOUS,
                 epoch_trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(ctx.exception.code, "EPOCH_DIGEST_MISMATCH")

    def test_bytes_that_changed_after_signing_are_refused(self):
        path = self.write_epoch()
        (self.tmp / "policy.yaml").write_bytes(b"policy: somebody-elses-bytes\n")
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.read(path)
        self.assertEqual(ctx.exception.code, "EPOCH_DIGEST_MISMATCH")

    def test_an_epoch_that_does_not_advance_is_refused(self):
        path = self.write_epoch()
        for previous in (EPOCH, EPOCH + 1):
            with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
                self.read(path, previous_epoch=previous)
            self.assertEqual(ctx.exception.code, "EPOCH_REGRESSION")
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(six_legs(), epoch_receipt=path, epoch_previous=EPOCH,
                 epoch_trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(ctx.exception.code, "EPOCH_REGRESSION")

    def test_a_body_edited_after_signing_is_refused(self):
        path = self.write_epoch()
        body = json.loads(path.read_text(encoding="utf-8"))
        body["policy"]["bytes"] = body["policy"]["bytes"] + 1
        path.write_text(json.dumps(body, indent=1), encoding="utf-8")
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.read(path)
        self.assertEqual(ctx.exception.code, "EPOCH_SIGNATURE_INVALID")
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(six_legs(), epoch_receipt=path, epoch_previous=PREVIOUS,
                 epoch_trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(ctx.exception.code, "EPOCH_SIGNATURE_INVALID")

    def test_an_unsigned_declaration_is_refused(self):
        path = self.write_epoch(sign=False)
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.read(path)
        self.assertEqual(ctx.exception.code, "EPOCH_NO_SIGNER")

    def test_a_signature_from_another_key_is_refused(self):
        path = self.write_epoch()
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        other = Ed25519PrivateKey.generate()
        body = json.loads(path.read_text(encoding="utf-8"))
        body["signature"]["sig_b64"] = base64.b64encode(
            other.sign(fe.canonical_body(body))).decode()
        path.write_text(json.dumps(body, indent=1), encoding="utf-8")
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.read(path)
        self.assertEqual(ctx.exception.code, "EPOCH_SIGNATURE_INVALID")

    def test_an_unknown_key_is_refused(self):
        path = self.produce()
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.read(path, trusted_key_ids={"A-KEY-NOBODY-PINNED"})
        self.assertEqual(ctx.exception.code, "EPOCH_KEY_UNTRUSTED")

    def test_a_missing_declaration_is_not_observed_and_cannot_fill_the_leg(self):
        missing = self.tmp / "nope.json"
        out = self.read(missing)
        self.assertEqual(out["state"], "NOT_OBSERVED")
        self.assertEqual(out["code"], "EPOCH_UNREADABLE")
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(six_legs(), epoch_receipt=missing, epoch_previous=PREVIOUS,
                 epoch_trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(ctx.exception.code, "EPOCH_UNREADABLE")

    def test_a_declaration_for_another_epoch_or_scope_is_refused(self):
        path = self.write_epoch()
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.read(path, expected_epoch=EPOCH + 5)
        self.assertEqual(ctx.exception.code, "EPOCH_EPOCH_MISMATCH")
        path = self.write_epoch(scope="another/scope")
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.read(path)
        self.assertEqual(ctx.exception.code, "EPOCH_SCOPE_MISMATCH")
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(six_legs(), epoch_receipt=path, epoch_previous=PREVIOUS,
                 epoch_trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(ctx.exception.code, "EPOCH_SCOPE_MISMATCH")

    def test_a_declaration_with_no_state_or_a_wrong_schema_is_refused(self):
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.read(self.write_epoch(state="ACTIVE"))
        self.assertEqual(ctx.exception.code, "EPOCH_STATE_NOT_DECLARED")
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.read(self.write_epoch(schema="FABRIC_ACTIVE_EPOCH@2"))
        self.assertEqual(ctx.exception.code, "EPOCH_SCHEMA_MISMATCH")

    def test_an_epoch_that_is_not_a_positive_integer_is_refused(self):
        for value in (0, -1, "11", True, 11.0, None):
            path = self.write_epoch(epoch=value)
            with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
                fe.read_epoch_receipt(path, expected_scope=SCOPE)
            self.assertEqual(ctx.exception.code, "EPOCH_INVALID", value)


class TestTheLabelAloneIsNoLongerEnough(_Base):
    """The measured D-24 hole: a caller-typed fourth leg substantiated itself."""

    def test_a_host_raw_label_with_no_receipt_is_refused(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(six_legs(active_evidence="HOST_RAW"))
        self.assertEqual(ctx.exception.code, "POLICY_EPOCH_UNSUBSTANTIATED")
        self.assertIn("POLICY_EPOCH_UNSUBSTANTIATED", pb.D24_REFUSAL_CODES)

    def test_the_promotion_receipt_label_is_a_label_too(self):
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(six_legs(active_provenance="EPOCH_PROMOTION_RECEIPT", active_evidence="HOST_RAW"))
        self.assertEqual(ctx.exception.code, "POLICY_EPOCH_UNSUBSTANTIATED")

    def test_a_hand_typed_reader_provenance_without_a_receipt_is_refused(self):
        """Claiming `provenance=FABRIC_ACTIVE_EPOCH` is a claim that a reader produced the leg."""
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(six_legs(active_provenance=fe.PROVENANCE))
        self.assertEqual(ctx.exception.code, "POLICY_EPOCH_UNSUBSTANTIATED")

    def test_a_hand_built_receipt_dict_without_a_path_is_refused(self):
        forged = {"state": "OBSERVED", "verified": True, "leg": "active_epoch",
                  "provenance": fe.PROVENANCE, "reader": fe.READER, "digest": POLICY_SHA,
                  "evidence_class": "HOST_RAW", "epoch": EPOCH, "scope": SCOPE}
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(six_legs(), epoch_receipt=forged, epoch_previous=PREVIOUS,
                 epoch_trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(ctx.exception.code, "POLICY_LEG_PROVENANCE_INVALID")

    def test_a_fixture_label_still_records_a_design_intent_but_is_not_an_epoch_claim(self):
        record = bind(six_legs())
        self.assertEqual(record["state"], "BOUND")
        self.assertFalse(record["host"]["active_epoch_verified"])
        caveat = [s for s in record["not_claimed"] if s.startswith("active_epoch")]
        self.assertTrue(caveat)
        self.assertIn("NOT claimed", caveat[0])
        self.assertEqual(record["legs"][3]["provenance"], "ACTIVE_POLICY_POINTER")
        self.assertEqual(record["legs"][3]["evidence_class"], "FIXTURE")

    def test_an_unpinned_epoch_receipt_is_refused_by_the_binding(self):
        """No trust-the-embedded-key path: the leg needs a pinned key id."""
        path = self.produce()
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(six_legs(), epoch_receipt=path, epoch_previous=PREVIOUS)
        self.assertEqual(ctx.exception.code, "POLICY_EPOCH_KEY_UNPINNED")

    def test_the_leg_provenance_set_admits_the_reader_but_leg_still_checks_it(self):
        self.assertIn(fe.PROVENANCE, pb.LEG_PROVENANCE["active_epoch"])
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.leg("active_epoch", digest=POLICY_SHA, provenance="HOST_LOAD_RAW",
                   reader=fe.READER, scope=SCOPE, epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "POLICY_LEG_PROVENANCE_INVALID")


class TestEpochProducer(_Base):
    def test_a_produced_document_records_what_it_is(self):
        out = fe.produce_epoch(policy=self.tmp / "policy.yaml", epoch=EPOCH, scope=SCOPE,
                               subject=SUBJECT, key_file=self.key_file, key_id=FIXTURE_KEY_ID,
                               out=self.tmp / "e.json", previous_epoch=PREVIOUS)
        self.assertEqual(out["state"], "PRODUCED")
        body = json.loads(Path(out["path"]).read_text(encoding="utf-8"))
        self.assertEqual(body["schema"], fe.SCHEMA)
        self.assertEqual(body["state"], "EPOCH_DECLARED")
        self.assertEqual(body["claim_ceiling"], "EPOCH_DECLARED_NOT_HOST_ACTIVE")
        self.assertEqual(body["policy"]["sha256"], POLICY_SHA)
        self.assertEqual(body["previous_epoch"], PREVIOUS)
        self.assertFalse((self.tmp / "e.json.tmp").exists())

    def test_the_producer_refuses_a_stale_epoch(self):
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.produce(previous_epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "EPOCH_SIGN_EPOCH_NOT_GREATER")
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.produce(epoch=0)
        self.assertEqual(ctx.exception.code, "EPOCH_SIGN_EPOCH_INVALID")

    def test_the_producer_refuses_a_ttl_outside_the_bound(self):
        for ttl in (0, -10, 60 * 24 * 31, 60 * 24 * 60):
            with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
                self.produce(ttl_minutes=ttl, out=f"ttl-{ttl}.json")
            self.assertEqual(ctx.exception.code, "EPOCH_SIGN_TTL_OUT_OF_BOUNDS", ttl)

    def test_the_producer_refuses_a_key_inside_the_repository_tree(self):
        in_tree = self.tmp / "inside" / "key.hex"
        in_tree.parent.mkdir()
        in_tree.write_bytes(self.key_file.read_bytes())
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.produce(key_file=in_tree, repo_root_override=self.tmp, out="in-tree.json")
        self.assertEqual(ctx.exception.code, "EPOCH_SIGN_KEY_INSIDE_REPO")
        self.assertFalse((self.tmp / "in-tree.json").exists())

    def test_the_producer_refuses_a_missing_or_unusable_key(self):
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.produce(key_file=self.tmp / "absent.hex", out="absent.json")
        self.assertEqual(ctx.exception.code, "EPOCH_SIGN_KEY_MISSING")
        junk = self.tmp / "junk.key"
        junk.write_bytes(b"not a key")
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.produce(key_file=junk, out="junk.json")
        self.assertEqual(ctx.exception.code, "EPOCH_SIGN_KEY_UNUSABLE")

    def test_the_producer_refuses_to_overwrite_an_epoch_declaration(self):
        path = self.produce()
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.produce(out=path.name)
        self.assertEqual(ctx.exception.code, "EPOCH_SIGN_TARGET_EXISTS")
        self.produce(out=path.name, overwrite=True)

    def test_the_producer_refuses_unreadable_policy_bytes(self):
        with self.assertRaises(fe.EpochReceiptRefusal) as ctx:
            self.produce(policy=self.tmp / "absent.yaml", out="no-policy.json")
        self.assertEqual(ctx.exception.code, "EPOCH_SIGN_POLICY_UNREADABLE")

    def test_the_cli_produces_and_reads_one_document(self):
        out = self.tmp / "cli.json"
        cmd = [sys.executable, str(HERE / "fabric_active_epoch.py"), "produce",
               "--policy", str(self.tmp / "policy.yaml"), "--epoch", str(EPOCH),
               "--scope", SCOPE, "--subject", SUBJECT, "--key-file", str(self.key_file),
               "--key-id", FIXTURE_KEY_ID, "--out", str(out), "--previous-epoch", str(PREVIOUS)]
        done = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.tmp))
        self.assertEqual(done.returncode, 0, done.stderr + done.stdout)
        read = subprocess.run(
            [sys.executable, str(HERE / "fabric_active_epoch.py"), "read", str(out),
             "--scope", SCOPE, "--epoch", str(EPOCH), "--previous-epoch", str(PREVIOUS),
             "--trusted-key-id", FIXTURE_KEY_ID],
            capture_output=True, text=True, cwd=str(self.tmp))
        self.assertEqual(read.returncode, 0, read.stderr + read.stdout)
        self.assertEqual(json.loads(read.stdout)["state"], "OBSERVED")
        self.assertEqual(json.loads(read.stdout)["provenance"], fe.PROVENANCE)

    def test_the_cli_refuses_a_stale_epoch_with_a_nonzero_exit(self):
        cmd = [sys.executable, str(HERE / "fabric_active_epoch.py"), "produce",
               "--policy", str(self.tmp / "policy.yaml"), "--epoch", str(PREVIOUS),
               "--scope", SCOPE, "--key-file", str(self.key_file), "--key-id", FIXTURE_KEY_ID,
               "--out", str(self.tmp / "stale.json"), "--previous-epoch", str(PREVIOUS)]
        done = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.tmp))
        self.assertEqual(done.returncode, 1)
        self.assertIn("EPOCH_SIGN_EPOCH_NOT_GREATER", done.stdout)


class TestEpochContractAgreement(_Base):
    def test_binding_and_reader_agree_on_the_epoch_contract(self):
        self.assertEqual(pb.EPOCH_RECEIPT_SCHEMA, fe.SCHEMA)
        self.assertEqual(pb.EPOCH_RECEIPT_PROVENANCE, fe.PROVENANCE)
        self.assertEqual(pb.EPOCH_RECEIPT_READER, fe.READER)
        self.assertEqual(pb.EPOCH_RECEIPT_EVIDENCE_CLASS, fe.EVIDENCE_CLASS)
        self.assertIn(fe.PROVENANCE, pb.LEG_PROVENANCE["active_epoch"])
        self.assertIn("ACTIVE_POLICY_POINTER", pb.EPOCH_LABEL_PROVENANCE)
        self.assertNotIn(fe.PROVENANCE, pb.EPOCH_LABEL_PROVENANCE)

    def test_the_new_codes_are_distinct_from_every_existing_one(self):
        self.assertEqual(len(set(pb.D24_REFUSAL_CODES)), len(pb.D24_REFUSAL_CODES))
        self.assertFalse(set(pb.D24_REFUSAL_CODES) & PRE_EXISTING_CODES)
        self.assertFalse(set(pb.D24_REFUSAL_CODES) & set(pb.D17_REFUSAL_CODES))
        self.assertEqual(len(set(fe.CODES)), len(fe.CODES))
        self.assertFalse(set(fe.CODES) & PRE_EXISTING_CODES)
        self.assertFalse(set(fe.CODES) & set(pb.D24_REFUSAL_CODES))

    def test_the_schema_carries_every_field_the_contract_names(self):
        body = epoch_document()
        for field in ("schema", "epoch", "policy", "scope", "subject", "issued_at",
                      "expires_at", "key", "signature"):
            self.assertIn(field, body)
        for field in ("path", "sha256"):
            self.assertIn(field, body["policy"])
        for field in ("key_id", "alg", "public_key_b64"):
            self.assertIn(field, body["key"])
        for field in ("sig_b64", "signed_body_sha256"):
            self.assertIn(field, body["signature"])


if __name__ == "__main__":
    unittest.main()
