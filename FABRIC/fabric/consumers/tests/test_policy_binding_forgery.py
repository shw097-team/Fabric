# -*- coding: utf-8 -*-
"""D-17 — a forged Policy Receipt or Consumer ACK must be refused, not reported as observed.

Owner ruling (2026-11-07): *Fabric must REJECT a forged Policy Receipt or Consumer ACK.*

Three holes were measured on `policy_binding.py` at `ea259bd` (`inc5/evidence/D17/BEFORE_probe.raw.txt`):

1. the fifth leg had no reader, so a `HOST_LOAD_RECEIPT@1` with a valid envelope over the real bytes
   and no producer/process block — or no receipt anywhere — became `loaded_digest` and reported
   `host.loaded_on_host=True`;
2. a caller-typed `consumer_ack` dict with `evidence_class="HOST_RAW"` and
   `consumer_ack_receipt=None` set `host.consumer_ack_observed=True`;
3. a loaded leg whose provenance was `ACTIVE_POLICY_POINTER` bound once `leg()` was bypassed,
   because `build_binding` checked only `NON_LOADING_PROVENANCE` plus digest equality.

Every test below is written to *fail on the pre-patch module* (where the hole is an ACCEPT) and pass
on the patched one. The load-receipt reader is imported lazily: before the patch it does not exist,
which is itself part of hole 1, and the failures stay per-test instead of killing the module import.

Fixtures are real bytes on disk in a temp dir. They are not host evidence and do not claim to be:
`claim_ceiling` stays `AUTHOR_DESIGN_ONLY` and `host_policy_active` stays in `not_claimed`.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import hgk_consumer_receipt as hcr  # noqa: E402
import policy_binding as pb  # noqa: E402
import policy_leg_readers as lr  # noqa: E402

SUBJECT = "WP-FHS-02"
SCOPE = "fhs-w1/w2-prep"
EPOCH = 10
CONSUMER_ID = "hgk-policy-consumer"
POLICY_REF = "policy/fhs-w1.yaml"
POLICY_BYTES = b"rp002:\n  classes: 9\n  epoch: 10\n  legs: six\n"
POLICY_SHA = hashlib.sha256(POLICY_BYTES).hexdigest()
OTHER_BYTES = b"rp002:\n  classes: 9\n  epoch: 11\n  legs: six\n"
OTHER_SHA = hashlib.sha256(OTHER_BYTES).hexdigest()

#: D-24: the second leg is a real YAML->JSON stage of POLICY_BYTES, so its digest differs from
#: POLICY_SHA by construction. Before the patch that difference alone was refused as drift.
STAGE_PAYLOAD = {"rp002": {"classes": 9, "epoch": 10, "legs": "six"}}
STAGE_BYTES = lr.canonical_bytes(STAGE_PAYLOAD)
STAGE_SHA = hashlib.sha256(STAGE_BYTES).hexdigest()

#: Set by `_Base.setUp`; `five_legs()` reads the artifact legs from it.
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
    """Write the source, stage and epoch artifacts the first three legs are read from."""
    global FIXTURE_ROOT
    FIXTURE_ROOT = root
    (root / "policy.yaml").write_bytes(POLICY_BYTES)
    (root / "stage.json").write_text(json.dumps(stage_document(), indent=1), encoding="utf-8")
    (root / "epoch.json").write_text(json.dumps({
        "schema": lr.SCHEMA_EPOCH, "scope": SCOPE, "epoch": EPOCH,
        "digest": POLICY_SHA, "policy_path": "policy.yaml"}), encoding="utf-8")

#: Codes that existed before D-17. None of them may disappear or be renamed.
PRE_EXISTING_CODES = {
    "POLICY_LEG_UNKNOWN", "POLICY_LEG_EMPTY", "POLICY_LEG_PROVENANCE_INVALID",
    "POLICY_BINDING_INCOMPLETE", "POLICY_SIGNER_OR_EPOCH_DENY", "POLICY_SOURCE_STAGE_DRIFT",
    "POLICY_CONSUMER_NOT_ACK", "WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED",
}


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def seal(body: dict) -> dict:
    body = {k: v for k, v in body.items() if k != "self_sha256"}
    body["self_sha256"] = hashlib.sha256(canonical(body)).hexdigest()
    return body


def default_process(**over) -> dict:
    """A structurally valid producer/process block: pid + process start + boot identity."""
    now = dt.datetime.now(dt.timezone.utc)
    block = {
        "pid": os.getpid(),
        "ppid": os.getppid(),
        "python": "3.14.9",
        "cwd": str(Path.cwd()),
        "process_create_time_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "process_identity_sha256": hashlib.sha256(str(os.getpid()).encode()).hexdigest(),
        "boot_epoch_s": int(now.timestamp()) - 3600,
    }
    block.update(over)
    return block


def load_document(raw: bytes = POLICY_BYTES, *, policy_name: str = "policy.yaml",
                  **over) -> dict:
    body = {
        "schema": "HOST_LOAD_RECEIPT@1",
        "kind": "HOST_LOAD",
        "state": "LOAD_OBSERVED",
        "claim_ceiling": "HOST_READ_AND_PARSE_ONLY",
        "evidence_class": "HOST_RAW",
        "provenance_hint": "HOST_LOAD_RAW",
        "host": "HGK-KSEOS-A",
        "consumer_id": CONSUMER_ID,
        "scope": SCOPE,
        "subject": SUBJECT,
        "epoch": EPOCH,
        "policy": {"path": policy_name, "sha256": hashlib.sha256(raw).hexdigest(),
                   "bytes": len(raw)},
        "readback": {"sha256_read_1": hashlib.sha256(raw).hexdigest(),
                     "sha256_read_2": hashlib.sha256(raw).hexdigest(),
                     "bytes_read_1": len(raw), "bytes_read_2": len(raw),
                     "identical": True, "parsed_midpoint": True},
        "leg_projection": {"leg": "loaded_digest", "digest": hashlib.sha256(raw).hexdigest(),
                           "provenance": "HOST_LOAD_RAW", "reader": "host-load-receipt-reader",
                           "scope": SCOPE, "epoch": EPOCH, "evidence_class": "HOST_RAW"},
        "process": default_process(),
    }
    for key, value in over.items():
        if value is _DELETE:
            body.pop(key, None)
        else:
            body[key] = value
    return seal(body)


def ack_document(raw: bytes = POLICY_BYTES, **over) -> dict:
    body = {
        "schema": hcr.SCHEMA,
        "subject": SUBJECT,
        "scope": SCOPE,
        "policy_epoch": EPOCH,
        "consumer_id": CONSUMER_ID,
        "policy_ref": POLICY_REF,
        "raw_path": "policy.yaml",
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "ack": {"decision": "ACK", "acknowledged_at": "2026-11-07T00:00:00Z"},
        "observed_at": "2026-11-07T00:00:00Z",
    }
    body.update(over)
    return body


class _Delete:
    def __repr__(self) -> str:  # pragma: no cover - repr only
        return "<DELETE>"


_DELETE = _Delete()


def five_legs(digest: str = POLICY_SHA, *, loaded_evidence: str = "FIXTURE",
              ack_evidence: str = "FIXTURE", with_owner: bool = True) -> list[dict]:
    spec = {
        "source": dict(digest=POLICY_SHA, provenance="FABRIC_POLICY_SOURCE",
                       reader=lr.READER_SOURCE, artifact=FIXTURE_ROOT / "policy.yaml"),
        "stage": dict(digest=STAGE_SHA, provenance="STAGED_ARTIFACT",
                      reader=lr.READER_STAGE, artifact=FIXTURE_ROOT / "stage.json"),
        "active_epoch": dict(digest=POLICY_SHA, provenance="ACTIVE_POLICY_POINTER",
                             reader=lr.READER_EPOCH, artifact=FIXTURE_ROOT / "epoch.json"),
        "loaded_digest": dict(digest=digest, provenance="HOST_LOAD_RAW",
                              reader="host-load-receipt-reader"),
        "consumer_ack": dict(digest=digest, provenance="HGK_CONSUMER_RECEIPT",
                             reader="hgk-consumer-receipt-reader"),
    }
    if with_owner:
        spec["owner_approved"] = dict(digest=POLICY_SHA, provenance="OWNER_APPROVAL_RECEIPT",
                                      reader="owner-receipt-reader")
    legs = []
    for name, kw in spec.items():
        evidence = "FIXTURE"
        if name == "loaded_digest":
            evidence = loaded_evidence
        if name == "consumer_ack":
            evidence = ack_evidence
        legs.append(pb.leg(name, scope=SCOPE, epoch=EPOCH, evidence_class=evidence,
                           observed_at="2026-11-07T00:00:00Z", **kw))
    return legs


def bind(legs, **kw):
    return pb.build_binding(policy_ref=POLICY_REF, scope=SCOPE, epoch=EPOCH, subject=SUBJECT,
                            legs=legs, **kw)


# --- fixture owner key ---------------------------------------------------------------------------
# A deterministic throwaway Ed25519 key. It is *not* an owner key, it signs nothing but these
# tests, and the principal it signs for is labelled FIXTURE. A receipt signed with it proves the
# reader path is reachable — never that a Policy Owner approved anything.
FIXTURE_OWNER_SID = "S-1-5-21-1111111111-2222222222-3333333333-1001-FIXTURE-OWNER"
FIXTURE_READER_SID = "S-1-5-21-4444444444-5555555555-6666666666-1002-FIXTURE-READER"
FIXTURE_KEY_ID = "FIXTURE-OWNER-KEY-D17-NOT-A-REAL-KEY"
FIXTURE_SEED = hashlib.sha256(b"D17 FIXTURE OWNER KEY - NOT A REAL KEY").digest()


def crypto_available() -> bool:
    try:
        import cryptography.hazmat.primitives.asymmetric.ed25519  # noqa: F401
    except ImportError:
        return False
    return True


def fixture_signing_key():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    return Ed25519PrivateKey.from_private_bytes(FIXTURE_SEED)


def fixture_public_b64() -> str:
    import base64
    from cryptography.hazmat.primitives import serialization
    key = fixture_signing_key().public_key()
    raw = key.public_bytes(encoding=serialization.Encoding.Raw,
                           format=serialization.PublicFormat.Raw)
    return base64.b64encode(raw).decode()


def owner_document(raw: bytes = POLICY_BYTES, *, policy_name: str = "policy.yaml",
                   sign: bool = True, **over) -> dict:
    """A well-formed owner approval signed with the FIXTURE key (or left unsigned)."""
    import base64
    import owner_approval_receipt as own

    now = dt.datetime.now(dt.timezone.utc)
    body = {
        "schema": "OWNER_APPROVAL_RECEIPT@1",
        "kind": "OWNER_APPROVAL",
        "subject": SUBJECT,
        "scope": SCOPE,
        "epoch": EPOCH,
        "policy": {"path": policy_name, "sha256": hashlib.sha256(raw).hexdigest(),
                   "bytes": len(raw)},
        "principal": {"sid": FIXTURE_OWNER_SID, "role": "FIXTURE_POLICY_OWNER",
                      "display": "FIXTURE principal — not a person, not an approval"},
        "issued_at": (now - dt.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "expires_at": (now + dt.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "key": {"key_id": FIXTURE_KEY_ID, "alg": "ED25519",
                "public_key_b64": fixture_public_b64()},
    }
    for key, value in over.items():
        if value is _DELETE:
            body.pop(key, None)
        else:
            body[key] = value
    if sign:
        message = own.canonical_body(body)
        signature = fixture_signing_key().sign(message)
        body["signature"] = {
            "key_id": body["key"]["key_id"], "alg": "ED25519",
            "sig_b64": base64.b64encode(signature).decode(),
            "signed_body_sha256": hashlib.sha256(message).hexdigest(),
        }
    return body


class _Base(unittest.TestCase):
    OWNER_SCHEMA = "OWNER_APPROVAL_RECEIPT@1"

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        write_leg_fixtures(self.tmp)

    def tearDown(self):
        self._tmp.cleanup()

    def owner_reader(self):
        """Import the owner-approval reader, failing the test if the module is not there."""
        try:
            import owner_approval_receipt
        except ImportError as exc:  # pre-patch: hole 4 is that this module does not exist
            self.fail(f"no OWNER_APPROVAL_RECEIPT@1 reader in the module under test: {exc}")
        return owner_approval_receipt

    def write_owner(self, name: str = "owner.json", raw: bytes = POLICY_BYTES, **over) -> Path:
        path = self.tmp / name
        path.write_text(json.dumps(owner_document(raw, **over), indent=1), encoding="utf-8")
        return path

    def write_load(self, name: str = "load.json", raw: bytes = POLICY_BYTES, **over) -> Path:
        path = self.tmp / name
        path.write_text(json.dumps(load_document(raw, **over), indent=1), encoding="utf-8")
        return path

    def write_ack(self, name: str = "ack.json", raw: bytes = POLICY_BYTES, **over) -> Path:
        path = self.tmp / name
        path.write_text(json.dumps(ack_document(raw, **over), indent=1), encoding="utf-8")
        return path

    def reader(self):
        """Import the load-receipt reader, failing the test if the module is not there."""
        try:
            import host_load_receipt
        except ImportError as exc:  # pre-patch: hole 1 is that this module does not exist
            self.fail(f"no HOST_LOAD_RECEIPT@1 reader in the module under test: {exc}")
        return host_load_receipt


class TestHoleOneLoadReceiptNeedsAProducer(_Base):
    """Hole 1 — a load receipt with a valid envelope and no producer block was accepted."""

    def test_a_load_receipt_with_no_producer_block_is_refused(self):
        hl = self.reader()
        path = self.write_load(process=_DELETE, producer=_DELETE)
        with self.assertRaises(hl.LoadReceiptRefusal) as ctx:
            hl.read_load_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "LOAD_RECEIPT_NO_PRODUCER_BLOCK")
        self.assertIn(ctx.exception.code, hl.CODES)

    def test_a_load_receipt_with_no_producer_block_cannot_fill_the_leg(self):
        self.reader()
        path = self.write_load(process=_DELETE, producer=_DELETE)
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(five_legs(), load_receipt=path)
        self.assertEqual(ctx.exception.code, "LOAD_RECEIPT_NO_PRODUCER_BLOCK")

    def test_a_caller_projected_load_leg_without_a_receipt_is_refused(self):
        """The pre-patch ACCEPT: BOUND with loaded_on_host=True and no receipt anywhere."""
        document = load_document(process=_DELETE, producer=_DELETE)
        projected = dict(document["leg_projection"], observed_at="")
        legs = [projected if item["leg"] == "loaded_digest" else item for item in five_legs()]
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(legs)
        self.assertEqual(ctx.exception.code, "POLICY_LOAD_UNSUBSTANTIATED")

    def test_pid_alone_is_not_a_process_identity(self):
        hl = self.reader()
        path = self.write_load(process={"pid": os.getpid()})
        with self.assertRaises(hl.LoadReceiptRefusal) as ctx:
            hl.read_load_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "LOAD_RECEIPT_NO_PRODUCER_BLOCK")

    def test_structurally_invalid_producer_blocks_are_refused(self):
        hl = self.reader()
        now = dt.datetime.now(dt.timezone.utc)
        cases = {
            "pid is a string": ({"pid": str(os.getpid()), "boot_epoch_s": 1},
                                "LOAD_RECEIPT_PRODUCER_BLOCK_INVALID"),
            "pid is a bool": ({"pid": True, "boot_epoch_s": 1},
                              "LOAD_RECEIPT_PRODUCER_BLOCK_INVALID"),
            "pid is zero": ({"pid": 0, "boot_epoch_s": 1},
                            "LOAD_RECEIPT_PRODUCER_BLOCK_INVALID"),
            "ppid is negative": ({"pid": os.getpid(), "ppid": -1, "boot_epoch_s": 1},
                                 "LOAD_RECEIPT_PRODUCER_BLOCK_INVALID"),
            "start is not a time": ({"pid": os.getpid(),
                                     "process_create_time_utc": "yesterday"},
                                    "LOAD_RECEIPT_PRODUCER_BLOCK_INVALID"),
            "start is naive (no zone)": ({"pid": os.getpid(),
                                          "process_create_time_utc": "2026-11-07T00:00:00"},
                                         "LOAD_RECEIPT_PRODUCER_BLOCK_INVALID"),
            "start is in the future": ({"pid": os.getpid(),
                                        "process_create_time_utc":
                                            (now + dt.timedelta(days=3650)).strftime(
                                                "%Y-%m-%dT%H:%M:%SZ")},
                                       "LOAD_RECEIPT_PRODUCER_BLOCK_INVALID"),
            "start precedes boot": ({"pid": os.getpid(),
                                     "process_create_time_utc": "2020-01-01T00:00:00Z",
                                     "boot_epoch_s": int(now.timestamp()) - 60},
                                    "LOAD_RECEIPT_PRODUCER_BLOCK_INVALID"),
            "identity is not hex": ({"pid": os.getpid(), "process_identity_sha256": "not-a-hash"},
                                    "LOAD_RECEIPT_PRODUCER_BLOCK_INVALID"),
            "boot is zero": ({"pid": os.getpid(), "boot_epoch_s": 0},
                             "LOAD_RECEIPT_PRODUCER_BLOCK_INVALID"),
            "boot is in the future": ({"pid": os.getpid(),
                                       "boot_epoch_s": int(now.timestamp()) + 86400},
                                      "LOAD_RECEIPT_PRODUCER_BLOCK_INVALID"),
        }
        for label, (block, expected) in cases.items():
            with self.subTest(label):
                path = self.write_load(name=f"{abs(hash(label))}.json", process=block)
                with self.assertRaises(hl.LoadReceiptRefusal) as ctx:
                    hl.read_load_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
                self.assertEqual(ctx.exception.code, expected)

    def test_a_process_block_that_is_not_an_object_is_refused(self):
        hl = self.reader()
        for block in ([], "pid=1234", 42):
            with self.subTest(block=type(block).__name__):
                path = self.write_load(name=f"bad-{type(block).__name__}.json", process=block)
                with self.assertRaises(hl.LoadReceiptRefusal) as ctx:
                    hl.read_load_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
                self.assertEqual(ctx.exception.code, "LOAD_RECEIPT_NO_PRODUCER_BLOCK")

    def test_a_produced_receipt_still_passes(self):
        hl = self.reader()
        path = self.write_load()
        leg = hl.read_load_receipt(path, expected_scope=SCOPE, expected_subject=SUBJECT,
                                   expected_epoch=EPOCH)
        self.assertEqual(leg["state"], "OBSERVED")
        self.assertEqual(leg["digest"], POLICY_SHA)
        self.assertEqual(leg["leg"], "loaded_digest")
        self.assertEqual(leg["provenance"], "HOST_LOAD_RAW")
        self.assertEqual(leg["evidence_class"], "HOST_RAW")
        self.assertTrue(leg["verified"])
        self.assertEqual(leg["process"]["pid"], os.getpid())
        self.assertTrue(hl.is_verified_load_leg(leg))

    def test_the_producer_key_is_accepted_as_well_as_process(self):
        hl = self.reader()
        path = self.write_load(process=_DELETE, producer=default_process())
        leg = hl.read_load_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
        self.assertEqual(leg["state"], "OBSERVED")

    def test_a_receipt_that_was_edited_after_sealing_is_refused(self):
        hl = self.reader()
        path = self.write_load()
        body = json.loads(path.read_text(encoding="utf-8"))
        body["policy"]["sha256"] = POLICY_SHA  # unchanged
        body["process"]["pid"] = os.getpid() + 1
        path.write_text(json.dumps(body, indent=1), encoding="utf-8")
        with self.assertRaises(hl.LoadReceiptRefusal) as ctx:
            hl.read_load_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "LOAD_RECEIPT_SELF_HASH_MISMATCH")


class TestHoleTwoConsumerAckNeedsAReceipt(_Base):
    """Hole 2 — a caller-typed ack dict set consumer_ack_observed with no receipt."""

    def test_caller_typed_ack_without_a_receipt_is_refused(self):
        """The pre-patch ACCEPT: BOUND with host.consumer_ack_observed=True."""
        legs = five_legs(ack_evidence="HOST_RAW")
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(legs, consumer_ack_receipt=None)
        self.assertEqual(ctx.exception.code, "POLICY_CONSUMER_ACK_UNSUBSTANTIATED")

    def test_no_flag_is_set_without_a_receipt(self):
        record = bind(five_legs(), consumer_ack_receipt=None)
        self.assertFalse(record["host"]["consumer_ack_observed"])
        self.assertFalse(record["host"]["consumer_ack_receipt_verified"])

    def test_a_receipt_for_different_bytes_is_refused(self):
        load = self.write_load()
        (self.tmp / "other.yaml").write_bytes(OTHER_BYTES)
        ack = self.write_ack(raw=OTHER_BYTES, raw_path="other.yaml")
        verified = hcr.load_receipt(ack, expected_subject=SUBJECT, expected_scope=SCOPE,
                                    expected_epoch=EPOCH, consumer_id=CONSUMER_ID)
        self.assertEqual(verified["digest"], OTHER_SHA)
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(five_legs(), consumer_ack_receipt=verified, load_receipt=load)
        self.assertEqual(ctx.exception.code, "POLICY_CONSUMER_ACK_DIGEST_MISMATCH")

    def test_a_receipt_over_the_loaded_bytes_sets_the_flag(self):
        load = self.write_load()
        ack = self.write_ack()
        verified = hcr.load_receipt(ack, expected_subject=SUBJECT, expected_scope=SCOPE,
                                    expected_epoch=EPOCH, consumer_id=CONSUMER_ID)
        record = bind(five_legs(), consumer_ack_receipt=verified, load_receipt=load)
        self.assertEqual(record["state"], "BOUND")
        self.assertTrue(record["host"]["consumer_ack_observed"])
        self.assertTrue(record["host"]["consumer_ack_receipt_verified"])
        self.assertEqual(record["legs"][5]["digest"], POLICY_SHA)


class TestHoleThreeLoadedLegMustBeALoad(_Base):
    """Hole 3 — ACTIVE_POLICY_POINTER substantiated the loaded leg once leg() was bypassed."""

    def test_the_active_pointer_cannot_fill_the_loaded_leg(self):
        """The pre-patch ACCEPT: BOUND with the loaded leg read from the epoch pointer."""
        legs = [dict(item) for item in five_legs(loaded_evidence="DECLARED")]
        positions = [i for i, item in enumerate(legs) if item["leg"] == "loaded_digest"]
        legs[positions[0]]["provenance"] = "ACTIVE_POLICY_POINTER"
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(legs)
        self.assertEqual(ctx.exception.code, "POLICY_LOADED_PROVENANCE_NOT_A_LOAD_RECEIPT")

    def test_other_non_loading_provenances_keep_their_original_code(self):
        legs = [dict(item) for item in five_legs()]
        positions = [i for i, item in enumerate(legs) if item["leg"] == "loaded_digest"]
        legs[positions[0]]["provenance"] = "STAGE_MIRROR"
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(legs)
        self.assertEqual(ctx.exception.code, "WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED")

    def test_a_hand_typed_provenance_is_refused_not_just_ignored(self):
        for provenance in ("POLICY_OWNER_DIRECTIVE", "EPOCH_PROMOTION_RECEIPT", "HOST_RAW",
                           "loaded_digest", ""):
            with self.subTest(provenance=provenance):
                legs = [dict(item) for item in five_legs()]
                positions = [i for i, item in enumerate(legs) if item["leg"] == "loaded_digest"]
                legs[positions[0]]["provenance"] = provenance
                with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
                    bind(legs)
                self.assertEqual(ctx.exception.code,
                                 "POLICY_LOADED_PROVENANCE_NOT_A_LOAD_RECEIPT")

    def test_the_load_receipt_provenance_is_still_accepted(self):
        load = self.write_load()
        record = bind(five_legs(loaded_evidence="FIXTURE"), load_receipt=load)
        self.assertEqual(record["state"], "BOUND")
        self.assertTrue(record["host"]["loaded_on_host"])
        self.assertEqual(record["legs"][4]["provenance"], "HOST_LOAD_RAW")


class TestPositiveControl(_Base):
    """A real receipt with a real producer block still passes end to end."""

    def test_real_load_receipt_and_real_ack_receipt_bind(self):
        load = self.write_load()
        ack = self.write_ack()
        verified = hcr.load_receipt(ack, expected_subject=SUBJECT, expected_scope=SCOPE,
                                    expected_epoch=EPOCH, consumer_id=CONSUMER_ID)
        record = bind(five_legs(), consumer_ack_receipt=verified, load_receipt=load)
        self.assertEqual(record["state"], "BOUND")
        self.assertEqual(record["claim_ceiling"], "AUTHOR_DESIGN_ONLY")
        # D-24: this used to assert 6, which counted six distinct `reader` strings. Here the three
        # artifact readers ran and two receipts were opened; `owner_approved` is still caller-typed,
        # so it is not a verified reader. `test_policy_binding_leg_readers.py` proves the six-reader
        # case with a real approval.
        self.assertEqual(record["separate_readers"], 5)
        self.assertNotIn("owner-receipt-reader", record["verified_readers"])
        self.assertTrue(record["host"]["loaded_on_host"])
        self.assertTrue(record["host"]["load_receipt_verified"])
        self.assertTrue(record["host"]["consumer_ack_observed"])
        self.assertEqual(record["digests"]["loaded_digest"], POLICY_SHA)
        self.assertEqual(record["digests"]["consumer_ack"], POLICY_SHA)
        self.assertTrue(any(s.startswith("host_policy_active") for s in record["not_claimed"]))
        self.assertNotIn("host_policy_active", record["digests"])

    def test_the_reader_result_is_accepted_as_well_as_the_path(self):
        load = self.write_load()
        hl = self.reader()
        leg_source = hl.read_load_receipt(load, expected_scope=SCOPE, expected_epoch=EPOCH)
        record = bind(five_legs(), load_receipt=leg_source)
        self.assertEqual(record["state"], "BOUND")
        self.assertEqual(record["digests"]["loaded_digest"], POLICY_SHA)

    def test_a_reader_result_whose_file_was_deleted_is_refused(self):
        load = self.write_load()
        hl = self.reader()
        leg_source = hl.read_load_receipt(load, expected_scope=SCOPE, expected_epoch=EPOCH)
        load.unlink()
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(five_legs(), load_receipt=leg_source)
        self.assertEqual(ctx.exception.code, "LOAD_RECEIPT_UNREADABLE")


class TestHoleFourOwnerApprovalNeedsAReader(_Base):
    """Hole 4 — `owner_approved` named two provenances and read neither.

    D-17 owner ruling: Fabric must refuse a forged Policy Receipt / Consumer ACK. An owner approval
    that no reader opens is the same class of defect as a load receipt that no reader opens.
    """

    def test_a_typed_owner_leg_without_a_receipt_is_refused(self):
        """The pre-patch ACCEPT: BOUND with a hand-typed OWNER_APPROVAL_RECEIPT leg and no artifact."""
        legs = [dict(item, evidence_class="HOST_RAW") if item["leg"] == "owner_approved" else item
                for item in five_legs()]
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(legs)
        self.assertEqual(ctx.exception.code, "POLICY_OWNER_APPROVAL_UNSUBSTANTIATED")

    def test_a_missing_receipt_is_refused_with_its_own_code(self):
        own = self.owner_reader()
        missing = self.tmp / "does-not-exist.json"
        marker = own.read_owner_receipt(missing, expected_scope=SCOPE, expected_epoch=EPOCH)
        self.assertEqual(marker["state"], "NOT_OBSERVED")
        self.assertEqual(marker["code"], "OWNER_RECEIPT_UNREADABLE")
        for forbidden in ("digest", "provenance", "reader", "verified"):
            self.assertNotIn(forbidden, marker)
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(five_legs(), owner_receipt=missing)
        self.assertEqual(ctx.exception.code, "OWNER_RECEIPT_UNREADABLE")

    def test_no_signer_block_is_refused(self):
        own = self.owner_reader()
        path = self.write_owner(sign=False)
        with self.assertRaises(own.OwnerReceiptRefusal) as ctx:
            own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "OWNER_RECEIPT_NO_SIGNER")

    def test_a_document_that_names_no_principal_is_refused(self):
        own = self.owner_reader()
        path = self.write_owner(principal=_DELETE)
        with self.assertRaises(own.OwnerReceiptRefusal) as ctx:
            own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "OWNER_RECEIPT_MISSING_PRINCIPAL")

    def test_a_principal_without_a_sid_or_role_is_refused(self):
        own = self.owner_reader()
        for label, principal in {
            "no sid": {"role": "FIXTURE_POLICY_OWNER"},
            "no role": {"sid": FIXTURE_OWNER_SID},
            "empty sid": {"sid": "   ", "role": "FIXTURE_POLICY_OWNER"},
        }.items():
            with self.subTest(label):
                path = self.write_owner(name=f"{abs(hash(label))}.json", principal=principal)
                with self.assertRaises(own.OwnerReceiptRefusal) as ctx:
                    own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
                self.assertEqual(ctx.exception.code, "OWNER_RECEIPT_MISSING_PRINCIPAL")

    def test_an_approval_signed_by_the_reading_principal_is_refused(self):
        own = self.owner_reader()
        path = self.write_owner()
        with self.assertRaises(own.OwnerReceiptRefusal) as ctx:
            own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH,
                                   reader_sid=FIXTURE_OWNER_SID)
        self.assertEqual(ctx.exception.code, "OWNER_RECEIPT_SIGNER_IS_READER")
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(five_legs(), owner_receipt=path, owner_reader_sid=FIXTURE_OWNER_SID)
        self.assertEqual(ctx.exception.code, "OWNER_RECEIPT_SIGNER_IS_READER")

    def test_a_reading_key_that_is_the_signing_key_is_refused(self):
        own = self.owner_reader()
        path = self.write_owner()
        with self.assertRaises(own.OwnerReceiptRefusal) as ctx:
            own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH,
                                   reader_key_id=FIXTURE_KEY_ID)
        self.assertEqual(ctx.exception.code, "OWNER_RECEIPT_SIGNER_IS_READER")

    def test_a_body_edited_after_signing_is_refused(self):
        own = self.owner_reader()
        path = self.write_owner()
        body = json.loads(path.read_text(encoding="utf-8"))
        body["principal"]["role"] = "POLICY_OWNER"          # escalate the label after signing
        path.write_text(json.dumps(body, indent=1), encoding="utf-8")
        with self.assertRaises(own.OwnerReceiptRefusal) as ctx:
            own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "OWNER_RECEIPT_SIGNATURE_INVALID")

    def test_a_signature_that_does_not_verify_is_refused(self):
        import base64
        own = self.owner_reader()
        body = owner_document()
        body["signature"]["sig_b64"] = base64.b64encode(b"\x00" * 64).decode()
        path = self.tmp / "zeroed.json"
        path.write_text(json.dumps(body, indent=1), encoding="utf-8")
        with self.assertRaises(own.OwnerReceiptRefusal) as ctx:
            own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "OWNER_RECEIPT_SIGNATURE_INVALID")

    def test_an_expired_approval_is_refused(self):
        own = self.owner_reader()
        now = dt.datetime.now(dt.timezone.utc)
        path = self.write_owner(
            issued_at=(now - dt.timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            expires_at=(now - dt.timedelta(days=9)).strftime("%Y-%m-%dT%H:%M:%SZ"))
        with self.assertRaises(own.OwnerReceiptRefusal) as ctx:
            own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "OWNER_RECEIPT_EXPIRED")

    def test_incoherent_times_are_refused(self):
        own = self.owner_reader()
        now = dt.datetime.now(dt.timezone.utc)
        cases = {
            "missing issued_at": (dict(issued_at=_DELETE), "OWNER_RECEIPT_TIME_INVALID"),
            "expires before issued": (dict(
                issued_at=now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                expires_at=(now - dt.timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")),
                "OWNER_RECEIPT_TIME_INVALID"),
            "naive expires_at": (dict(expires_at="2030-01-01T00:00:00"),
                                 "OWNER_RECEIPT_TIME_INVALID"),
        }
        for label, (over, expected) in cases.items():
            with self.subTest(label):
                path = self.write_owner(name=f"{abs(hash(label))}.json", **over)
                with self.assertRaises(own.OwnerReceiptRefusal) as ctx:
                    own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
                self.assertEqual(ctx.exception.code, expected)

    def test_a_scope_mismatch_is_refused(self):
        own = self.owner_reader()
        path = self.write_owner(scope="another/scope")
        with self.assertRaises(own.OwnerReceiptRefusal) as ctx:
            own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "OWNER_RECEIPT_SCOPE_MISMATCH")

    def test_an_approval_of_other_bytes_is_refused_against_the_source_leg(self):
        own = self.owner_reader()
        (self.tmp / "other.yaml").write_bytes(OTHER_BYTES)
        path = self.write_owner(raw=OTHER_BYTES, policy_name="other.yaml")
        leg = own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
        self.assertEqual(leg["state"], "OBSERVED")
        self.assertEqual(leg["digest"], OTHER_SHA)
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(five_legs(), owner_receipt=path)
        self.assertEqual(ctx.exception.code, "OWNER_RECEIPT_DIGEST_MISMATCH")

    def test_approved_bytes_that_changed_on_disk_are_refused(self):
        own = self.owner_reader()
        path = self.write_owner()
        (self.tmp / "policy.yaml").write_bytes(b"policy: somebody-elses-bytes\n")
        with self.assertRaises(own.OwnerReceiptRefusal) as ctx:
            own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "OWNER_RECEIPT_DIGEST_MISMATCH")

    def test_an_unpinned_key_is_reported_untrusted_and_a_pinned_one_checked(self):
        own = self.owner_reader()
        path = self.write_owner()
        leg = own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
        self.assertFalse(leg["key_trusted"])
        leg = own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH,
                                     trusted_key_ids={FIXTURE_KEY_ID})
        self.assertTrue(leg["key_trusted"])
        with self.assertRaises(own.OwnerReceiptRefusal) as ctx:
            own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH,
                                   trusted_key_ids={"SOME-OTHER-KEY"})
        self.assertEqual(ctx.exception.code, "OWNER_RECEIPT_KEY_UNTRUSTED")

    def test_an_algorithm_this_reader_cannot_verify_is_refused(self):
        own = self.owner_reader()
        path = self.write_owner()
        body = json.loads(path.read_text(encoding="utf-8"))
        body["signature"]["alg"] = "RSA-PSS-SHA256"
        path.write_text(json.dumps(body, indent=1), encoding="utf-8")
        with self.assertRaises(own.OwnerReceiptRefusal) as ctx:
            own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "OWNER_RECEIPT_KEY_UNUSABLE")

    def test_a_schema_this_reader_does_not_accept_is_refused(self):
        own = self.owner_reader()
        path = self.write_owner(schema="OWNER_APPROVAL_RECEIPT@2")
        with self.assertRaises(own.OwnerReceiptRefusal) as ctx:
            own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "OWNER_RECEIPT_SCHEMA_MISMATCH")

    def test_a_directive_schema_carries_its_own_provenance(self):
        own = self.owner_reader()
        path = self.write_owner(schema="POLICY_OWNER_DIRECTIVE@1")
        leg = own.read_owner_receipt(path, expected_scope=SCOPE, expected_epoch=EPOCH)
        self.assertEqual(leg["state"], "OBSERVED")
        self.assertEqual(leg["provenance"], "POLICY_OWNER_DIRECTIVE")
        self.assertTrue(own.is_verified_owner_leg(leg))


class TestHoleFourPositiveControl(_Base):
    """A FIXTURE-signed approval reaches BOUND — reachability only, never an owner act."""

    def setUp(self):
        super().setUp()
        if not crypto_available():
            self.skipTest("`cryptography` (Ed25519) is not installed on this host")

    def test_a_fixture_signed_approval_binds_and_says_what_it_is_not(self):
        owner = self.write_owner()
        load = self.write_load()
        ack = self.write_ack()
        verified_ack = hcr.load_receipt(ack, expected_subject=SUBJECT, expected_scope=SCOPE,
                                        expected_epoch=EPOCH, consumer_id=CONSUMER_ID)
        record = bind(five_legs(), consumer_ack_receipt=verified_ack, load_receipt=load,
                      owner_receipt=owner, owner_reader_sid=FIXTURE_READER_SID,
                      owner_trusted_key_ids={FIXTURE_KEY_ID})
        self.assertEqual(record["state"], "BOUND")
        self.assertEqual(record["claim_ceiling"], "AUTHOR_DESIGN_ONLY")
        self.assertTrue(record["host"]["owner_approval_verified"])
        self.assertTrue(record["host"]["owner_key_trusted"])
        owner_leg = record["legs"][2]
        self.assertEqual(owner_leg["leg"], "owner_approved")
        self.assertEqual(owner_leg["provenance"], "OWNER_APPROVAL_RECEIPT")
        self.assertEqual(owner_leg["reader"], pb.OWNER_RECEIPT_READER)
        self.assertEqual(owner_leg["digest"], POLICY_SHA)
        # the record must say, in words, that a verified signature is not key provenance
        caveat = [s for s in record["not_claimed"] if s.startswith("owner_approval")]
        self.assertTrue(caveat)
        self.assertIn("NOT established", caveat[0])

    def test_the_fixture_principal_is_visibly_not_an_owner(self):
        own = self.owner_reader()
        leg = own.read_owner_receipt(self.write_owner(), expected_scope=SCOPE,
                                     expected_epoch=EPOCH, trusted_key_ids={FIXTURE_KEY_ID})
        self.assertIn("FIXTURE", leg["principal"]["sid"])
        self.assertIn("FIXTURE", leg["principal"]["role"])
        self.assertIn("FIXTURE", leg["key_id"])


class TestSixLegRegression(_Base):
    """The six-leg build still refuses an incomplete record with the original code."""

    def test_missing_owner_approved_without_any_receipt_is_incomplete(self):
        """Passes on the pre-patch module too: the incomplete-record refusal is untouched."""
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(five_legs(with_owner=False))
        self.assertEqual(ctx.exception.code, "POLICY_BINDING_INCOMPLETE")
        self.assertIn("owner_approved", str(ctx.exception))

    def test_missing_owner_approved_is_incomplete(self):
        load = self.write_load()
        ack = self.write_ack()
        verified = hcr.load_receipt(ack, expected_subject=SUBJECT, expected_scope=SCOPE,
                                    expected_epoch=EPOCH, consumer_id=CONSUMER_ID)
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(five_legs(with_owner=False), consumer_ack_receipt=verified, load_receipt=load)
        self.assertEqual(ctx.exception.code, "POLICY_BINDING_INCOMPLETE")
        self.assertIn("owner_approved", str(ctx.exception))

    def test_fixture_six_legs_still_bind_design_only(self):
        record = bind(five_legs())
        self.assertEqual(record["state"], "BOUND")
        self.assertFalse(record["host"]["loaded_on_host"])
        self.assertFalse(record["host"]["consumer_ack_observed"])
        self.assertEqual(record["claim_ceiling"], "AUTHOR_DESIGN_ONLY")

    def test_every_pre_existing_code_is_still_emitted(self):
        """Spot-check that the refusals the module existed for were not replaced by D-17 codes."""
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            pb.leg("loaded_digest", digest=POLICY_SHA, provenance="ACTIVE_POLICY_POINTER",
                   reader=lr.READER_EPOCH, scope=SCOPE, epoch=EPOCH)
        self.assertEqual(ctx.exception.code, "POLICY_LEG_PROVENANCE_INVALID")

        # D-24: this used to patch the stage leg's digest to OTHER_SHA and expect
        # POLICY_SOURCE_STAGE_DRIFT. That assertion encoded defect 3: a genuine YAML->JSON stage has
        # a different digest from its source by construction, so the old rule refused the transform
        # and passed only a stage whose digest was typed as the source digest. Drift now means the
        # stage declares a *different source*, which is what this fixture does.
        drift = self.tmp / "stage-from-other-source.json"
        drift.write_text(json.dumps(stage_document(source_sha256=OTHER_SHA)), encoding="utf-8")
        legs = [dict(item, artifact=str(drift), source_sha256=OTHER_SHA,
                     digest=STAGE_SHA) if item["leg"] == "stage" else item
                for item in five_legs()]
        with self.assertRaises(pb.PolicyBindingRefusal) as ctx:
            bind(legs)
        self.assertEqual(ctx.exception.code, "POLICY_SOURCE_STAGE_DRIFT")


class TestContractAgreement(_Base):
    """The binding's declared values agree with the readers, and D-17 codes are distinct."""

    def test_binding_and_reader_agree_on_the_load_contract(self):
        hl = self.reader()
        self.assertEqual(pb.LOAD_RECEIPT_SCHEMA, hl.SCHEMA)
        self.assertEqual(pb.LOAD_RECEIPT_PROVENANCE, hl.PROVENANCE)
        self.assertEqual(pb.LOAD_RECEIPT_READER, hl.READER)
        self.assertEqual(pb.LOAD_RECEIPT_EVIDENCE_CLASS, hl.EVIDENCE_CLASS)
        self.assertIn(hl.PROVENANCE, pb.LOADED_PROVENANCE)
        self.assertIn(hl.PROVENANCE, pb.LEG_PROVENANCE["loaded_digest"])

    def test_binding_and_reader_agree_on_the_owner_contract(self):
        own = self.owner_reader()
        self.assertIn(self.OWNER_SCHEMA, pb.OWNER_RECEIPT_SCHEMAS)
        self.assertEqual(pb.OWNER_RECEIPT_READER, own.READER)
        self.assertEqual(pb.OWNER_RECEIPT_EVIDENCE_CLASS, own.EVIDENCE_CLASS)
        self.assertIn("OWNER_APPROVAL_RECEIPT", pb.LEG_PROVENANCE["owner_approved"])

    def test_new_codes_are_distinct_from_the_pre_existing_ones(self):
        self.assertEqual(len(set(pb.D17_REFUSAL_CODES)), len(pb.D17_REFUSAL_CODES))
        self.assertFalse(set(pb.D17_REFUSAL_CODES) & PRE_EXISTING_CODES)
        for code in ("LOAD_RECEIPT_NO_PRODUCER_BLOCK", "LOAD_RECEIPT_PRODUCER_BLOCK_INVALID"):
            self.assertNotIn(code, PRE_EXISTING_CODES)


if __name__ == "__main__":
    unittest.main()
