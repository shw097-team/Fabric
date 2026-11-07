# -*- coding: utf-8 -*-
"""D-24 — the owner-approval *issuer*, and the two forgeries it must not be able to commit.

`owner_approval_receipt.py` is a reader only: on merged `main` no code in the repository could emit a
document it would accept. This suite covers the signer added for that gap, and the owner ruling that
landed with it: **the policy-owner signature must verify against a pinned trusted key** — there is no
"trust the embedded public key" path into the third leg.

Every fixture key here is a throwaway labelled FIXTURE. A FIXTURE-signed approval proves the reader
path is reachable and never that a Policy Owner approved anything.
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

import owner_approval_receipt as own  # noqa: E402
import owner_approval_signer as signer  # noqa: E402
import policy_binding as pb  # noqa: E402

SUBJECT = "WP-FHS-02"
SCOPE = "fhs-w1/w2-prep"
EPOCH = 11
POLICY_BYTES = b"rp002:\n  classes: 9\n  epoch: 11\n  legs: six\n"
POLICY_SHA = hashlib.sha256(POLICY_BYTES).hexdigest()

FIXTURE_OWNER_SID = "S-1-5-21-1111111111-2222222222-3333333333-1001-FIXTURE-OWNER"
FIXTURE_READER_SID = "S-1-5-21-4444444444-5555555555-6666666666-1002-FIXTURE-READER"
FIXTURE_KEY_ID = "FIXTURE-OWNER-KEY-D24-NOT-A-REAL-KEY"
FIXTURE_READER_KEY_ID = "FIXTURE-READER-KEY-D24"
FIXTURE_SEED = hashlib.sha256(b"D24 FIXTURE OWNER KEY - NOT A REAL KEY").digest()
ROLE = "FIXTURE_POLICY_OWNER"


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


def six_legs(digest: str = POLICY_SHA) -> list[dict]:
    spec = {
        "source": dict(digest=digest, provenance="FABRIC_POLICY_SOURCE", reader="fabric-policy-repo"),
        "stage": dict(digest=digest, provenance="STAGED_ARTIFACT", reader="fabric-stage-reader"),
        "owner_approved": dict(digest=digest, provenance="OWNER_APPROVAL_RECEIPT",
                               reader="owner-receipt-reader"),
        "active_epoch": dict(digest=digest, provenance="ACTIVE_POLICY_POINTER",
                             reader="fabric-active-pointer"),
        "loaded_digest": dict(digest=digest, provenance="HOST_LOAD_RAW",
                              reader="host-load-receipt-reader"),
        "consumer_ack": dict(digest=digest, provenance="HGK_CONSUMER_RECEIPT",
                             reader="hgk-consumer-receipt-reader"),
    }
    return [pb.leg(name, scope=SCOPE, epoch=EPOCH, evidence_class="FIXTURE",
                   observed_at="2026-11-07T00:00:00Z", **kw) for name, kw in spec.items()]


def bind(legs, **kw):
    return pb.build_binding(policy_ref="policy/fhs-w1.yaml", scope=SCOPE, epoch=EPOCH,
                            subject=SUBJECT, legs=legs, **kw)


class _Base(unittest.TestCase):
    def setUp(self):
        if not crypto_available():
            self.skipTest("`cryptography` (Ed25519) is not installed on this host")
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.policy = self.tmp / "policy.yaml"
        self.policy.write_bytes(POLICY_BYTES)
        self.key_file = self.tmp / "owner-key.hex"
        from cryptography.hazmat.primitives import serialization
        self.key_file.write_text(fixture_key().private_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()).hex(), encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def sign(self, **over) -> Path:
        out = self.tmp / over.pop("out", "owner.json")
        kw: dict[str, Any] = dict(policy=self.policy, scope=SCOPE, epoch=EPOCH, key_file=self.key_file,
                  key_id=FIXTURE_KEY_ID, out=out, principal_sid=FIXTURE_OWNER_SID, role=ROLE,
                  subject=SUBJECT, reader_sid=FIXTURE_READER_SID,
                  reader_key_id=FIXTURE_READER_KEY_ID, env={})
        kw.update(over)
        signer.sign_owner_approval(**kw)
        return out

    def read(self, path: Path, **over):
        kw = dict(expected_scope=SCOPE, expected_epoch=EPOCH, reader_sid=FIXTURE_READER_SID,
                  reader_key_id=FIXTURE_READER_KEY_ID)
        kw.update(over)
        return own.read_owner_receipt(path, **kw)


class TestSignerPositive(_Base):
    def test_a_signed_approval_verifies_and_binds_with_a_pinned_key(self):
        path = self.sign()
        leg = self.read(path, trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(leg["state"], "OBSERVED")
        self.assertEqual(leg["provenance"], "OWNER_APPROVAL_RECEIPT")
        self.assertEqual(leg["digest"], POLICY_SHA)
        self.assertEqual(leg["principal"]["sid"], FIXTURE_OWNER_SID)
        self.assertTrue(leg["key_trusted"])

        record = bind(six_legs(), owner_receipt=path, owner_reader_sid=FIXTURE_READER_SID,
                      owner_trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(record["state"], "BOUND")
        self.assertTrue(record["host"]["owner_approval_verified"])
        self.assertTrue(record["host"]["owner_key_trusted"])
        self.assertEqual(record["legs"][2]["provenance"], "OWNER_APPROVAL_RECEIPT")

    def test_the_signer_writes_a_document_the_reader_accepts_field_by_field(self):
        path = self.sign()
        body = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(body["schema"], "OWNER_APPROVAL_RECEIPT@1")
        self.assertEqual(body["kind"], "OWNER_APPROVAL")
        self.assertEqual(body["policy"]["sha256"], POLICY_SHA)
        self.assertEqual(body["signature"]["key_id"], body["key"]["key_id"])
        self.assertEqual(body["signature"]["signed_body_sha256"],
                         hashlib.sha256(own.canonical_body(body)).hexdigest())
        self.assertFalse((self.tmp / "owner.json.tmp").exists())

    def test_a_directive_schema_is_supported_too(self):
        path = self.sign(schema="POLICY_OWNER_DIRECTIVE@1")
        leg = self.read(path, trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(leg["provenance"], "POLICY_OWNER_DIRECTIVE")

    def test_overwrite_must_be_asked_for_and_then_works(self):
        path = self.sign()
        with self.assertRaises(signer.OwnerSigningRefusal) as ctx:
            self.sign(out=path.name)
        self.assertEqual(ctx.exception.code, "OWNER_SIGN_TARGET_EXISTS")
        self.sign(out=path.name, overwrite=True)


class TestSignerCannotSelfSign(_Base):
    """A receipt signed by the reader's own key proves nothing: the reader would have written it."""

    def test_a_reader_public_key_that_is_the_signing_key_is_refused(self):
        with self.assertRaises(signer.OwnerSigningRefusal) as ctx:
            self.sign(reader_public_key_b64=fixture_public_b64(), out="self.json")
        self.assertEqual(ctx.exception.code, "OWNER_SIGN_SELF_SIGNED")
        self.assertFalse((self.tmp / "self.json").exists())
        self.assertIn("OWNER_SIGN_SELF_SIGNED", signer.CODES)

    def test_a_reader_key_file_that_holds_the_signing_key_is_refused(self):
        reader_pub = self.tmp / "reader-pub.b64"
        reader_pub.write_text(fixture_public_b64(), encoding="utf-8")
        with self.assertRaises(signer.OwnerSigningRefusal) as ctx:
            self.sign(reader_key_file=reader_pub, out="self-file.json")
        self.assertEqual(ctx.exception.code, "OWNER_SIGN_SELF_SIGNED")

    def test_a_reader_public_key_from_the_environment_is_refused(self):
        with self.assertRaises(signer.OwnerSigningRefusal) as ctx:
            self.sign(env={"FABRIC_READER_PUBLIC_KEY_B64": fixture_public_b64()},
                      out="self-env.json")
        self.assertEqual(ctx.exception.code, "OWNER_SIGN_SELF_SIGNED")

    def test_a_principal_that_is_the_reading_principal_is_refused(self):
        with self.assertRaises(signer.OwnerSigningRefusal) as ctx:
            self.sign(principal_sid=FIXTURE_READER_SID, out="same-sid.json")
        self.assertEqual(ctx.exception.code, "OWNER_SIGN_SELF_SIGNED")
        with self.assertRaises(signer.OwnerSigningRefusal) as ctx:
            self.sign(reader_sid=None, env={"FABRIC_READER_SID": FIXTURE_OWNER_SID},
                      out="same-sid-env.json")
        self.assertEqual(ctx.exception.code, "OWNER_SIGN_SELF_SIGNED")

    def test_a_key_id_that_is_the_reading_key_id_is_refused(self):
        with self.assertRaises(signer.OwnerSigningRefusal) as ctx:
            self.sign(key_id=FIXTURE_READER_KEY_ID, out="same-key.json")
        self.assertEqual(ctx.exception.code, "OWNER_SIGN_SELF_SIGNED")

    def test_the_reader_still_refuses_when_the_reader_is_the_signer(self):
        """Defence in depth: even a correctly signed document is refused if the reader is the owner."""
        path = self.sign()
        with self.assertRaises(own.OwnerReceiptRefusal) as ctx:
            own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH,
                                   reader_sid=FIXTURE_OWNER_SID)
        self.assertEqual(ctx.exception.code, "OWNER_RECEIPT_SIGNER_IS_READER")


class TestSignerRefusals(_Base):
    def test_a_ttl_outside_the_bound_is_refused(self):
        for ttl in (0, -1, 60 * 24 * 31, 60 * 24 * 365):
            with self.assertRaises(signer.OwnerSigningRefusal) as ctx:
                self.sign(ttl_minutes=ttl, out=f"ttl-{ttl}.json")
            self.assertEqual(ctx.exception.code, "OWNER_SIGN_TTL_OUT_OF_BOUNDS", ttl)

    def test_a_missing_key_file_is_refused(self):
        with self.assertRaises(signer.OwnerSigningRefusal) as ctx:
            self.sign(key_file=self.tmp / "no-such-key.hex", out="no-key.json")
        self.assertEqual(ctx.exception.code, "OWNER_SIGN_KEY_MISSING")
        self.assertFalse((self.tmp / "no-key.json").exists())

    def test_a_key_inside_the_repository_tree_is_refused(self):
        """Refused before existence is checked, so an in-tree path cannot even be probed."""
        root = signer.repo_root()
        self.assertIsNotNone(root, "expected to be running inside the repository")
        with self.assertRaises(signer.OwnerSigningRefusal) as ctx:
            self.sign(key_file=HERE / "keys" / "owner.hex", out="in-repo.json")
        self.assertEqual(ctx.exception.code, "OWNER_SIGN_KEY_INSIDE_REPO")
        self.assertFalse((self.tmp / "in-repo.json").exists())

    def test_a_key_inside_a_declared_repository_root_is_refused(self):
        inside = self.tmp / "tree" / "owner.hex"
        inside.parent.mkdir()
        inside.write_bytes(self.key_file.read_bytes())
        with self.assertRaises(signer.OwnerSigningRefusal) as ctx:
            self.sign(key_file=inside, repo_root_override=self.tmp, out="declared-tree.json")
        self.assertEqual(ctx.exception.code, "OWNER_SIGN_KEY_INSIDE_REPO")

    def test_an_unusable_key_file_is_refused(self):
        junk = self.tmp / "junk.key"
        junk.write_bytes(b"this is not a key")
        with self.assertRaises(signer.OwnerSigningRefusal) as ctx:
            self.sign(key_file=junk, out="junk.json")
        self.assertEqual(ctx.exception.code, "OWNER_SIGN_KEY_UNUSABLE")

    def test_an_approval_with_no_principal_is_refused(self):
        for over in ({"principal_sid": ""}, {"role": ""}, {"principal_sid": "   "}):
            with self.assertRaises(signer.OwnerSigningRefusal) as ctx:
                self.sign(out="no-principal.json", **over)
            self.assertEqual(ctx.exception.code, "OWNER_SIGN_PRINCIPAL_MISSING", over)

    def test_unreadable_policy_bytes_are_refused(self):
        with self.assertRaises(signer.OwnerSigningRefusal) as ctx:
            self.sign(policy=self.tmp / "absent.yaml", out="no-policy.json")
        self.assertEqual(ctx.exception.code, "OWNER_SIGN_POLICY_UNREADABLE")


class TestPinnedKeyIsMandatoryInTheBinding(_Base):
    """Owner ruling: no path may verify the owner signature against the document's own key."""

    def test_an_unpinned_owner_receipt_is_refused_by_the_binding(self):
        path = self.sign()
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(six_legs(), owner_receipt=path, owner_reader_sid=FIXTURE_READER_SID)
        self.assertEqual(ctx.exception.code, "POLICY_OWNER_KEY_UNPINNED")
        self.assertIn("POLICY_OWNER_KEY_UNPINNED", pb.D24_REFUSAL_CODES)

    def test_a_key_id_outside_the_registry_is_refused(self):
        path = self.sign()
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(six_legs(), owner_receipt=path, owner_reader_sid=FIXTURE_READER_SID,
                 owner_trusted_key_ids={"A-KEY-NOBODY-PINNED"})
        self.assertEqual(ctx.exception.code, "OWNER_RECEIPT_KEY_UNTRUSTED")

    def test_the_reader_alone_still_reports_an_unpinned_read_as_untrusted(self):
        path = self.sign()
        leg = self.read(path)
        self.assertFalse(leg["key_trusted"])
        self.assertIn("NOT established", leg["note"])


class TestSignerCli(_Base):
    def cli(self, *extra: str, out: str = "cli-owner.json"):
        return subprocess.run(
            [sys.executable, str(HERE / "owner_approval_signer.py"),
             "--policy", str(self.policy), "--scope", SCOPE, "--epoch", str(EPOCH),
             "--key-file", str(self.key_file), "--key-id", FIXTURE_KEY_ID,
             "--out", str(self.tmp / out), "--principal-sid", FIXTURE_OWNER_SID, "--role", ROLE,
             "--reader-sid", FIXTURE_READER_SID, "--reader-key-id", FIXTURE_READER_KEY_ID, *extra],
            capture_output=True, text=True, cwd=str(self.tmp))

    def test_the_cli_signs_a_receipt_the_reader_accepts(self):
        done = self.cli()
        self.assertEqual(done.returncode, 0, done.stderr + done.stdout)
        leg = self.read(self.tmp / "cli-owner.json", trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(leg["state"], "OBSERVED")
        self.assertEqual(leg["digest"], POLICY_SHA)

    def test_the_cli_refuses_to_self_sign(self):
        done = self.cli("--reader-public-key-b64", fixture_public_b64(), out="cli-self.json")
        self.assertEqual(done.returncode, 1)
        self.assertIn("OWNER_SIGN_SELF_SIGNED", done.stdout)
        self.assertFalse((self.tmp / "cli-self.json").exists())

    def test_the_cli_refuses_a_key_inside_the_repository(self):
        done = subprocess.run(
            [sys.executable, str(HERE / "owner_approval_signer.py"),
             "--policy", str(self.policy), "--scope", SCOPE,
             "--key-file", str(HERE / "keys" / "owner.hex"), "--key-id", FIXTURE_KEY_ID,
             "--out", str(self.tmp / "cli-repo.json"),
             "--principal-sid", FIXTURE_OWNER_SID, "--role", ROLE],
            capture_output=True, text=True, cwd=str(self.tmp))
        self.assertEqual(done.returncode, 1)
        self.assertIn("OWNER_SIGN_KEY_INSIDE_REPO", done.stdout)


class TestSignerContractAgreement(_Base):
    def test_the_signer_and_the_reader_agree_on_the_schema(self):
        self.assertIn(own.SCHEMA_APPROVAL, signer.SCHEMAS)
        self.assertIn(own.SCHEMA_DIRECTIVE, signer.SCHEMAS)
        self.assertEqual(signer.SCHEMA_APPROVAL, "OWNER_APPROVAL_RECEIPT@1")
        self.assertEqual(signer.SCHEMA_DIRECTIVE, "POLICY_OWNER_DIRECTIVE@1")

    def test_the_signer_codes_are_distinct_from_the_readers(self):
        self.assertEqual(len(set(signer.CODES)), len(signer.CODES))
        self.assertFalse(set(signer.CODES) & set(own.CODES))
        self.assertFalse(set(signer.CODES) & set(pb.D24_REFUSAL_CODES))

    def test_the_signer_emits_no_consumer_or_host_load_receipt(self):
        """Scope ruling: Fabric produces the epoch and the owner approval, nothing else."""
        forbidden = {"HOST_LOAD_RECEIPT@1", "HGK_CONSUMER_RECEIPT@1"}
        for module in (signer, __import__("fabric_active_epoch")):
            for name in dir(module):
                value = getattr(module, name)
                if isinstance(value, str):
                    self.assertNotIn(value, forbidden, f"{module.__name__}.{name}")
                if isinstance(value, (tuple, list, set, frozenset)):
                    self.assertFalse(forbidden & {v for v in value if isinstance(v, str)},
                                     f"{module.__name__}.{name}")
        source = (HERE / "owner_approval_signer.py").read_text(encoding="utf-8")
        self.assertNotIn('"HGK_CONSUMER_RECEIPT@1"', source)
        self.assertNotIn('"HOST_LOAD_RECEIPT@1"', source)
        epoch_source = (HERE / "fabric_active_epoch.py").read_text(encoding="utf-8")
        self.assertNotIn('"HGK_CONSUMER_RECEIPT@1"', epoch_source)
        self.assertNotIn('"HOST_LOAD_RECEIPT@1"', epoch_source)


if __name__ == "__main__":
    unittest.main()
