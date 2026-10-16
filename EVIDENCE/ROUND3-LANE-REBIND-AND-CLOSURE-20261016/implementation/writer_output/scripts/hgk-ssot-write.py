#!/usr/bin/env python3
"""hgk-ssot-write.py - transactional SSOT writer (N1).

Round FAR-LANE-SOD-007. CANDIDATE_ONLY.

  python hgk-ssot-write.py --file <file-id-or-path> --from <new-bytes-file>
      --owner <round-id> --token-file T --txn <transaction-id> [--registry P]
      [--ledger L] [--backup-root B] --expected-preimage-sha256 <H|ABSENT>
      --generation G --admission A --evidence-ref E
      [--supersedes-entry <entry-id>]

The writer is NON-REENTRANT: it never acquires a lock itself. It must be invoked
under an already-held lease (the sanctioned path is
``hgk-ssot-lock.py with-lock``). It re-enters the same OS mutex and validates the
live lock metadata (held, same owner, matching token digest, matching generation,
matching admission) before touching any bytes; a missing or mismatched lease fails
closed.

Pins (D09): ``--generation``, ``--admission`` and ``--evidence-ref`` are MANDATORY
and must resolve to non-null values recorded on the lease and in the ledger; the
lease must itself carry a non-null admission ref + digest.

Writes an SSOT file only while holding its OS-mutex-fenced lock, using a durable
PREPARED/COMMITTED ledger transaction (MF04):

  validate held lease -> read+digest source -> CAS-verify current target == expected
  preimage -> exclusive verified backup -> [ledger mutex held across] append PREPARED
  (+readback) -> atomic replace target -> exact target readback == new_sha256
  -> append COMMITTED referencing the PREPARED entry

The ledger mutex is held across prepare->commit (D05); any unresolved PREPARED
transaction blocks a new transaction regardless of its id. The idempotent replay
path still verifies the CURRENT target hash against the committed digest (D09); a
mismatch is a typed failure.

Exit codes: 0 ok | 2 schema | 3 IO | 4 stale/contention/CAS | 5 recovery required |
64 typed argparse usage error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import sys

EXIT_OK = 0
EXIT_SCHEMA = 2
EXIT_IO = 3
EXIT_STALE = 4
EXIT_RECOVERY = 5
EXIT_USAGE = 64

ROUND = "FAR-LANE-SOD-007"
DEFAULT_REGISTRY = os.path.join("var", "far-lane-sod-007", "config", "ssot-file-registry.json")
DEFAULT_LEDGER = os.path.join("config", "ssot-supersession-ledger.json")
DEFAULT_BACKUP_ROOT = os.path.join("var", "far-lane-sod-007", "backup")
LEDGER_ID = "SSOT-SUPERSESSION-LEDGER-1"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util as _ilu  # noqa: E402


def _load_lock_module():
    name = "hgk_ssot_lock_mod"
    spec = _ilu.spec_from_file_location(
        name, os.path.join(os.path.dirname(os.path.abspath(__file__)), "hgk-ssot-lock.py")
    )
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


lk = _load_lock_module()


class WriteError(Exception):
    def __init__(self, code, reason, **details):
        super().__init__(reason)
        self.code = code
        self.reason = reason
        self.details = details


class TypedArgumentParser(argparse.ArgumentParser):
    """D08: argparse usage errors emit the typed JSON body with a distinct code."""

    def error(self, message):
        payload = {
            "ok": False,
            "error_code": "usage_error",
            "reason": "usage_error",
            "details": {"prog": self.prog, "message": message},
        }
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
        raise SystemExit(EXIT_USAGE)


def _fail(code, reason, **details):
    raise WriteError(code, reason, **details)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def ledger_fields(round_id, file_id, preimage, new, txn, event, backup_ref,
                  evidence_ref, evidence_sha, admission_ref, admission_sha,
                  supersedes_entry):
    return {
        "round": round_id,
        "file_id": file_id,
        "transaction_id": txn,
        "admission_pin_sha256": admission_sha,
        "preimage_sha256": preimage,
        "new_sha256": new,
        "supersedes_entry_id": supersedes_entry,
        "superseded_by_round": round_id,
        "at_utc": lk.iso(lk.now_utc()),
        "admission_ref": admission_ref,
        "admission_sha256": admission_sha,
        "evidence_ref": evidence_ref,
        "evidence_sha256": evidence_sha,
        "backup_ref": backup_ref,
    }


def scan_pending(ledger, file_id, txn):
    """Return (prepared_entry, committed_entry) for a file + transaction id."""
    prepared = committed = None
    for entry in ledger["entries"]:
        if entry.get("file_id") != file_id or entry.get("transaction_id") != txn:
            continue
        if entry.get("event") == "PREPARED":
            prepared = entry
        elif entry.get("event") in ("COMMITTED", "ABORTED"):
            committed = entry
    return prepared, committed


def do_write(args) -> int:
    registry = lk.load_registry(args.registry)
    entry, path = lk.resolve(registry, args.file)
    lk.deny_for_round(entry, args.owner)

    if not os.path.exists(args.src):
        _fail(EXIT_IO, "source_missing", src=args.src)
    with open(args.src, "rb") as fh:
        new_bytes = fh.read()
    new_sha = sha256_bytes(new_bytes)

    # D09: mandatory attribution pins + generation.
    if args.generation is None:
        _fail(EXIT_SCHEMA, "writer_requires_generation")
    if not args.admission:
        _fail(EXIT_SCHEMA, "writer_requires_admission")
    if not os.path.exists(args.admission):
        _fail(EXIT_IO, "admission_missing", admission=args.admission)
    if not args.evidence_ref or not os.path.exists(args.evidence_ref):
        _fail(EXIT_IO, "writer_requires_evidence_ref", evidence_ref=args.evidence_ref)
    admission_sha = lk.sha256_file(args.admission)
    evidence_sha = lk.sha256_file(args.evidence_ref)

    token = None
    token_digest = None
    if args.token_file and os.path.exists(args.token_file):
        token = open(args.token_file, "r", encoding="utf-8").read().strip()
        token_digest = sha256_bytes(token.encode("utf-8"))

    lock_path = lk.lock_sidecar(path, entry)
    mtx = lk.mutex_path_for(lock_path)

    # ---- critical section: target lock ----
    with lk.mutex(mtx):
        # Non-reentrant: require a live lease owned by this owner/proven by token.
        rec, raw = lk.read_lock(lock_path)
        if rec is None:
            _fail(EXIT_STALE, "write_refused_no_lock", file_id=entry["file_id"])
        if lk.classify(rec) != "held":
            _fail(EXIT_STALE, "write_refused_lock_expired", holder=rec.get("owner"))
        if rec.get("owner") != args.owner:
            _fail(EXIT_STALE, "write_refused_wrong_owner",
                  holder=rec.get("owner"), owner=args.owner)
        if token_digest is None:
            _fail(EXIT_SCHEMA, "writer_requires_token_file", token_file=args.token_file)
        if rec.get("token_digest") != token_digest:
            if token_digest in (rec.get("displaced_token_digests") or []):
                _fail(EXIT_STALE, "write_refused_lease_displaced")
            _fail(EXIT_STALE, "write_refused_token_mismatch")
        # D09: generation pin mandatory and exact.
        if int(rec.get("generation", -1)) != int(args.generation):
            _fail(EXIT_STALE, "write_refused_generation_mismatch",
                  lock_generation=rec.get("generation"), requested=args.generation)
        # D09: the lease must carry a non-null admission attribution.
        if not rec.get("admission_ref") or not rec.get("admission_sha256"):
            _fail(EXIT_STALE, "lease_missing_admission_attribution")
        if rec.get("admission_sha256") != admission_sha:
            _fail(EXIT_STALE, "write_refused_admission_sha_mismatch")

        exists = os.path.exists(path)
        current = open(path, "rb").read() if exists else b""
        preimage_sha = sha256_bytes(current) if exists else "ABSENT"

        # ---- ledger mutex held across prepare -> commit (D05) ----
        lmtx = lk.mutex_path_for(args.ledger)
        with lk.mutex(lmtx):
            if os.path.exists(args.ledger):
                ledger0 = lk.load_ledger(args.ledger)
            else:
                ledger0 = {"schema_version": 1, "ledger_id": LEDGER_ID, "entries": []}
            lk.verify_head(args.ledger, ledger0)

            # D05: any unresolved PREPARED transaction blocks a new write.
            pending = lk.unresolved_prepared(ledger0)
            if pending:
                mine = scan_pending(ledger0, entry["file_id"], args.txn)
                if not (mine[0] is not None and mine[1] is None and len(pending) == 1):
                    _fail(
                        EXIT_RECOVERY,
                        "unresolved_prepared_blocks_write",
                        pending_transaction_ids=sorted(
                            str(e.get("transaction_id")) for e in pending
                        ),
                    )

            prepared, committed = scan_pending(ledger0, entry["file_id"], args.txn)
            if prepared is not None and committed is None:
                observed = lk.sha256_file(path) if os.path.exists(path) else None
                if observed == prepared.get("new_sha256"):
                    _fail(EXIT_RECOVERY, "pending_transaction_target_is_new",
                          transaction_id=args.txn, recovery="finalize_requires_admission")
                if observed == prepared.get("preimage_sha256"):
                    _fail(EXIT_RECOVERY, "pending_transaction_target_is_old",
                          transaction_id=args.txn, recovery="abort_requires_admission")
                _fail(EXIT_RECOVERY, "recovery_required_unattributed_bytes",
                      transaction_id=args.txn)

            if committed is not None:
                if committed.get("new_sha256") == new_sha:
                    # D09: the idempotent path STILL verifies the current target.
                    observed = lk.sha256_file(path) if os.path.exists(path) else None
                    if observed != committed.get("new_sha256"):
                        _fail(
                            EXIT_STALE,
                            "idempotent_target_hash_mismatch",
                            transaction_id=args.txn,
                            expected=committed.get("new_sha256"),
                            actual=observed,
                        )
                    return _emit({"ok": True, "idempotent": True,
                                  "entry_id": committed.get("entry_id")}, EXIT_OK)
                _fail(EXIT_STALE, "transaction_id_payload_conflict", transaction_id=args.txn)

            # CAS: current target bytes must match expected preimage.
            expected = args.expected_preimage_sha256
            if expected and expected.lower() != preimage_sha.lower():
                _fail(EXIT_STALE, "preimage_cas_mismatch",
                      expected=expected, actual=preimage_sha)
            if not expected:
                _fail(EXIT_SCHEMA, "expected_preimage_sha256_required")

            # Verified exclusive backup of the preimage.
            backup_ref = None
            if exists:
                backup_dir = os.path.join(args.backup_root, entry["file_id"], args.txn)
                os.makedirs(backup_dir, exist_ok=True)
                backup_path = os.path.join(backup_dir, preimage_sha + ".preimage")
                fd = os.open(backup_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                with os.fdopen(fd, "wb") as bh:
                    bh.write(current)
                    bh.flush()
                    os.fsync(bh.fileno())
                if lk.sha256_file(backup_path) != preimage_sha:
                    _fail(EXIT_IO, "backup_verification_failed")
                backup_ref = backup_path

            fields = ledger_fields(
                args.owner, entry["file_id"], preimage_sha, new_sha,
                args.txn, "PREPARED", backup_ref, args.evidence_ref, evidence_sha,
                rec.get("admission_ref"), admission_sha, args.supersedes_entry,
            )
            lk.validate_internal_entry_fields(fields)
            prep = lk.append_entry(ledger0, fields, "PREPARED", args.ledger)
            readback = lk.load_ledger(args.ledger)
            if readback["entries"][-1]["entry_id"] != prep["entry_id"]:
                _fail(EXIT_IO, "prepared_readback_mismatch")

            # Atomic replace + exact readback (still inside the ledger mutex).
            tmp = path + ".txn-" + args.txn
            with open(tmp, "wb") as fh:
                fh.write(new_bytes)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp, path)
            if lk.sha256_file(path) != new_sha:
                _fail(EXIT_IO, "target_readback_mismatch")

            fields = ledger_fields(
                args.owner, entry["file_id"], preimage_sha, new_sha,
                args.txn, "COMMITTED", backup_ref, args.evidence_ref, evidence_sha,
                rec.get("admission_ref"), admission_sha, prep["entry_id"],
            )
            lk.validate_internal_entry_fields(fields)
            ledger2 = lk.load_ledger(args.ledger)
            commit = lk.append_entry(ledger2, fields, "COMMITTED", args.ledger)
            readback = lk.load_ledger(args.ledger)
            if readback["entries"][-1]["entry_id"] != commit["entry_id"]:
                _fail(EXIT_IO, "committed_readback_mismatch")
            if lk.sha256_file(path) != new_sha:
                _fail(EXIT_RECOVERY, "target_moved_after_commit")

    return _emit({"ok": True, "file_id": entry["file_id"],
                  "preimage_sha256": preimage_sha, "new_sha256": new_sha,
                  "prepared_entry_id": prep["entry_id"],
                  "committed_entry_id": commit["entry_id"],
                  "backup_ref": backup_ref}, EXIT_OK)


def _emit(payload, code) -> int:
    payload = {"ok": code == EXIT_OK, **payload}
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
    return code


def build_parser():
    p = TypedArgumentParser(prog="hgk-ssot-write.py")
    p.add_argument("--file", required=True)
    p.add_argument("--from", dest="src", required=True)
    p.add_argument("--owner", required=True)
    p.add_argument("--token-file", required=True)
    p.add_argument("--txn", required=True)
    p.add_argument("--registry", default=DEFAULT_REGISTRY)
    p.add_argument("--ledger", default=DEFAULT_LEDGER)
    p.add_argument("--backup-root", default=DEFAULT_BACKUP_ROOT)
    p.add_argument("--expected-preimage-sha256", required=True)
    p.add_argument("--admission", default=None)
    p.add_argument("--evidence-ref", default=None)
    p.add_argument("--generation", type=int, default=None)
    p.add_argument("--supersedes-entry", default=None)
    p.add_argument("--genesis", action="store_true")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return do_write(args)
    except WriteError as exc:
        return _emit(
            {"error_code": exc.reason, "reason": exc.reason, "details": exc.details},
            exc.code,
        )
    except lk.LockError as exc:
        return _emit(
            {"error_code": exc.reason, "reason": exc.reason, "details": exc.details},
            exc.code,
        )


if __name__ == "__main__":
    sys.exit(main())
