#!/usr/bin/env python3
"""hgk-ssot-lock.py - SSOT lease lock + supersession ledger (N1).

Round FAR-LANE-SOD-007. CANDIDATE_ONLY.

Subcommands:
  acquire --file F --owner R --ttl S [--registry P] [--admission A]
          [--token-out O] [--break-expired --expected-lock-sha256 H --reason TEXT]
  release --file F --token-file T [--registry P] [--generation G]
  status  --file F [--registry P]
  with-lock --file F --owner R --ttl S [--registry P] -- <cmd...>
  ledger-append --entry J [--ledger L] [--expected-head H]
  ledger-status [--ledger L]

Safety design (MF03/MF05, repaired D02/D04/D05):
  * Every lock create / inspect / CAS-replace / release / status serializes on a
    stable per-canonical-file Windows OS mutex (an unmovable sidecar that is never
    deleted or recreated). The .lock file is metadata; it is never the mutex.
  * A held lease carries a LIVE-HOLDER WITNESS (pid + process creation id). A
    --break-expired is REFUSED with the distinct typed code ``holder_process_alive``
    while that holder process is alive, so an active critical section (including a
    ``with-lock`` whose child outlives the TTL) can never have its lease stolen. A
    legitimate break records the displaced holder's token digest, so the displaced
    holder's later release fails with the typed code ``release_displaced`` rather
    than a generic token mismatch.
  * The coordination generation is persisted monotonically past the mutex lock
    byte (never reset to 1 by a release-then-reacquire).
  * The ledger is append-only with a sha256 hash chain, an external HEAD WITNESS
    (count + tail hash) verified and updated in the same transaction, full 64-hex
    digests, non-future timestamps, mandatory authorization and a global block on
    any unresolved PREPARED transaction.

Exit codes: 0 ok | 2 invalid schema/arg | 3 IO/malformed state | 4 contention,
identity, token, expiry, holder-alive or stale head | 5 child/recovery failure |
64 typed argparse usage error.

Boundary: this is advisory/cooperative protection for FUTURE sanctioned HGK
writers only. It does not stop a direct same-user ``open(path, 'wb')`` write and
does not retrofit ACLs or migrate an already-running round.
"""
from __future__ import annotations

import argparse
import ctypes
import datetime as _dt
import hashlib
import json
import os
import re
import secrets
import socket
import stat
import subprocess
import sys
import time

EXIT_OK = 0
EXIT_SCHEMA = 2
EXIT_IO = 3
EXIT_CONTENTION = 4
EXIT_RECOVERY = 5
EXIT_USAGE = 64

ROUND = "FAR-LANE-SOD-007"
DEFAULT_REGISTRY = os.path.join("var", "far-lane-sod-007", "config", "ssot-file-registry.json")
DEFAULT_LEDGER = os.path.join("config", "ssot-supersession-ledger.json")
LEDGER_ID = "SSOT-SUPERSESSION-LEDGER-1"
LOCK_SCHEMA_VERSION = 2
MUTEX_TIMEOUT_S = 10.0
TTL_MIN, TTL_MAX = 1, 3600
FUTURE_SKEW_S = 5

HEX64 = re.compile(r"^[0-9a-f]{64}$")


class LockError(Exception):
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
    raise LockError(code, reason, **details)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return sha256_bytes(fh.read())


def canonical_bytes(obj) -> bytes:
    return json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def now_utc() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone.utc)


def iso(dt: _dt.datetime) -> str:
    return dt.astimezone(_dt.timezone.utc).isoformat()


def parse_iso(text: str) -> _dt.datetime:
    try:
        dt = _dt.datetime.fromisoformat(text)
    except (ValueError, TypeError):
        _fail(EXIT_IO, "malformed_timestamp", value=text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_dt.timezone.utc)
    return dt.astimezone(_dt.timezone.utc)


# --------------------------------------------------------------------------
# Stable OS mutex (+ persisted monotonic generation past the lock byte)
# --------------------------------------------------------------------------
def mutex_path_for(lock_path: str) -> str:
    return lock_path + ".mutex"


def open_mutex(mutex_path: str) -> int:
    """Create-or-open the stable mutex inode. Never delete it."""
    try:
        return os.open(mutex_path, os.O_RDWR | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        try:
            return os.open(mutex_path, os.O_RDWR)
        except OSError as exc:
            _fail(EXIT_IO, "mutex_unopenable", path=mutex_path, error=str(exc))
    except OSError as exc:
        _fail(EXIT_IO, "mutex_unopenable", path=mutex_path, error=str(exc))


def lock_mutex(fd: int, timeout: float = MUTEX_TIMEOUT_S) -> None:
    import msvcrt

    deadline = time.monotonic() + timeout
    while True:
        try:
            os.lseek(fd, 0, os.SEEK_SET)
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            return
        except OSError:
            if time.monotonic() > deadline:
                _fail(EXIT_CONTENTION, "mutex_timeout", timeout_s=timeout)
            time.sleep(0.05)


def unlock_mutex(fd: int) -> None:
    import msvcrt

    try:
        os.lseek(fd, 0, os.SEEK_SET)
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
    except OSError:
        pass


def read_mutex_generation(fd: int) -> int:
    """Read the persisted generation stored beyond the shared lock byte."""
    try:
        os.lseek(fd, 1, os.SEEK_SET)
        raw = os.read(fd, 4096)
    except OSError:
        return 0
    if not raw:
        return 0
    try:
        obj = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return 0
    gen = obj.get("last_generation") if isinstance(obj, dict) else None
    return int(gen) if isinstance(gen, int) and gen >= 0 else 0


def write_mutex_generation(fd: int, generation: int) -> None:
    os.lseek(fd, 1, os.SEEK_SET)
    os.write(fd, canonical_bytes({"last_generation": int(generation)}))
    try:
        os.ftruncate(fd, 1 + len(canonical_bytes({"last_generation": int(generation)})))
    except OSError:
        pass


class mutex:
    """Context manager: open, lock, unlock, close (never unlink)."""

    def __init__(self, mutex_path: str):
        self.path = mutex_path
        self.fd = None

    def __enter__(self):
        self.fd = open_mutex(self.path)
        lock_mutex(self.fd)
        return self.fd

    def __exit__(self, *exc):
        if self.fd is not None:
            unlock_mutex(self.fd)
            os.close(self.fd)
            self.fd = None
        return False


# --------------------------------------------------------------------------
# registry + identity
# --------------------------------------------------------------------------
def read_json(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            obj = json.load(fh)
    except FileNotFoundError:
        _fail(EXIT_IO, "file_missing", path=path)
    except OSError as exc:
        _fail(EXIT_IO, "file_unreadable", path=path, error=str(exc))
    except ValueError as exc:
        _fail(EXIT_IO, "malformed_json", path=path, error=str(exc))
    if not isinstance(obj, dict):
        _fail(EXIT_IO, "not_object", path=path)
    return obj


def load_registry(path: str) -> dict:
    reg = read_json(path)
    files = reg.get("files")
    if not isinstance(files, list):
        _fail(EXIT_IO, "registry_no_files", path=path)
    by_id = {}
    for entry in files:
        if not isinstance(entry, dict) or not isinstance(entry.get("file_id"), str):
            _fail(EXIT_IO, "registry_bad_entry", path=path)
        by_id[entry["file_id"]] = entry
    reg["_by_id"] = by_id
    return reg


def has_reparse_point(path: str) -> bool:
    if os.path.islink(path):
        return True
    try:
        if os.name == "nt":
            attrs = os.lstat(path).st_file_attributes
            if attrs & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                return True
    except OSError:
        pass
    return False


def resolve(registry: dict, file_arg: str):
    """Map a registry file_id (or a registered abspath) to (entry, canonical_path)."""
    entry = registry["_by_id"].get(file_arg)
    if entry is None:
        target = os.path.abspath(file_arg)
        for cand in registry["_by_id"].values():
            if os.path.abspath(cand.get("path", "")) == target:
                entry = cand
                break
    if entry is None:
        _fail(EXIT_CONTENTION, "file_not_registered", file=file_arg)
    path = os.path.abspath(entry["path"])
    if os.path.exists(path) and has_reparse_point(path):
        _fail(EXIT_CONTENTION, "unexpected_reparse_point", path=path)
    return entry, path


def deny_for_round(entry: dict, round_id: str) -> None:
    owner = entry.get("owner_round")
    deny_ids = entry.get("deny_rounds") or []
    if entry.get("deny_round_007") and round_id == ROUND:
        _fail(
            EXIT_CONTENTION,
            "target_owned_by_other_round",
            file_id=entry.get("file_id"),
            owner_round=owner,
        )
    if round_id in deny_ids or (owner and owner != round_id and not entry.get("fixture")):
        _fail(
            EXIT_CONTENTION,
            "target_owned_by_other_round",
            file_id=entry.get("file_id"),
            owner_round=owner,
        )


def lock_sidecar(path: str, entry: dict) -> str:
    base = entry.get("lock_basename") or (os.path.basename(path) + ".lock")
    return os.path.join(os.path.dirname(path), base)


def process_start_id(pid: int):
    try:
        k32 = ctypes.windll.kernel32
        handle = k32.OpenProcess(0x1000, False, pid)
        if not handle:
            return None
        creation = ctypes.c_ulonglong(0)
        exit_t = ctypes.c_ulonglong(0)
        kernel = ctypes.c_ulonglong(0)
        user = ctypes.c_ulonglong(0)
        ok = k32.GetProcessTimes(
            handle,
            ctypes.byref(creation),
            ctypes.byref(exit_t),
            ctypes.byref(kernel),
            ctypes.byref(user),
        )
        k32.CloseHandle(handle)
        return int(creation.value) if ok else None
    except Exception:  # noqa: BLE001
        return None


def holder_process_alive(rec) -> bool:
    """D02: a live-holder witness - is the recorded holder process still alive?"""
    if not isinstance(rec, dict):
        return False
    pid = rec.get("pid")
    if isinstance(pid, bool) or not isinstance(pid, int) or pid <= 0:
        return False
    creation = process_start_id(pid)
    if creation is None:
        return False
    recorded = rec.get("process_start_id")
    if recorded is None:
        return True
    return int(creation) == int(recorded)


def atomic_write(path: str, data: bytes) -> None:
    tmp = path + ".tmp-" + secrets.token_hex(4)
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def read_lock(lock_path: str):
    if not os.path.exists(lock_path):
        return None, None
    raw = open(lock_path, "rb").read()
    try:
        rec = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        _fail(EXIT_IO, "malformed_lock_metadata", path=lock_path)
    if not isinstance(rec, dict):
        _fail(EXIT_IO, "malformed_lock_metadata", path=lock_path)
    return rec, raw


def classify(rec) -> str:
    if rec is None:
        return "free"
    expires = parse_iso(rec.get("expires_utc", ""))
    return "expired" if now_utc() > expires else "held"


def validate_ttl(ttl) -> int:
    if isinstance(ttl, bool) or not isinstance(ttl, int):
        _fail(EXIT_SCHEMA, "invalid_ttl", ttl=ttl)
    if ttl < TTL_MIN or ttl > TTL_MAX:
        _fail(EXIT_SCHEMA, "invalid_ttl", ttl=ttl, min=TTL_MIN, max=TTL_MAX)
    return ttl


def build_record(entry, owner, generation, admission_ref, admission_sha, token, ttl,
                 displaced=None) -> dict:
    acquired = now_utc()
    return {
        "schema_version": LOCK_SCHEMA_VERSION,
        "file_id": entry["file_id"],
        "owner": owner,
        "round": owner,
        "token_digest": sha256_bytes(token.encode("utf-8")),
        "generation": generation,
        "pid": os.getpid(),
        "process_start_id": process_start_id(os.getpid()),
        "host": socket.gethostname(),
        "acquired_utc": iso(acquired),
        "expires_utc": iso(acquired + _dt.timedelta(seconds=ttl)),
        "admission_ref": admission_ref,
        "admission_sha256": admission_sha,
        "displaced_token_digests": list(displaced or []),
    }


def _next_generation(fd, prior_record=None) -> int:
    persisted = read_mutex_generation(fd)
    prior = 0
    if isinstance(prior_record, dict):
        try:
            prior = int(prior_record.get("generation", 0))
        except (TypeError, ValueError):
            prior = 0
    generation = max(persisted, prior) + 1
    write_mutex_generation(fd, generation)
    return generation


# --------------------------------------------------------------------------
# acquire / release / status
# --------------------------------------------------------------------------
def do_acquire(registry, entry, path, owner, ttl, admission, token_out,
               break_expired, expected_lock_sha, reason):
    validate_ttl(ttl)
    deny_for_round(entry, owner)
    lock_path = lock_sidecar(path, entry)
    mtx = mutex_path_for(lock_path)
    token = secrets.token_hex(32)
    admission_sha = None
    if admission:
        if not os.path.exists(admission):
            _fail(EXIT_IO, "admission_missing", admission=admission)
        admission_sha = sha256_file(admission)

    with mutex(mtx) as fd:
        rec, raw = read_lock(lock_path)
        state = classify(rec)
        if state == "held":
            _fail(
                EXIT_CONTENTION,
                "lock_held",
                holder=rec.get("owner"),
                round=rec.get("round"),
                expires_utc=rec.get("expires_utc"),
            )
        if state == "expired" and not break_expired:
            _fail(
                EXIT_CONTENTION,
                "lock_expired_not_stolen",
                holder=rec.get("owner"),
                expires_utc=rec.get("expires_utc"),
            )
        if state == "expired":
            # D02: never steal a lease whose holder process is still alive.
            if holder_process_alive(rec):
                _fail(
                    EXIT_CONTENTION,
                    "holder_process_alive",
                    holder=rec.get("owner"),
                    pid=rec.get("pid"),
                    note="break-expired refused while the holder process is alive",
                )
            if not expected_lock_sha:
                _fail(EXIT_SCHEMA, "break_requires_expected_lock_sha")
            if sha256_bytes(raw) != expected_lock_sha.lower():
                _fail(EXIT_CONTENTION, "break_expected_lock_sha_mismatch")
            if not reason or not str(reason).strip():
                _fail(EXIT_SCHEMA, "break_requires_reason")
            displaced = list(rec.get("displaced_token_digests") or [])
            if rec.get("token_digest"):
                displaced.append(rec["token_digest"])
            generation = _next_generation(fd, rec)
            record = build_record(
                entry, owner, generation, admission, admission_sha, token, ttl, displaced
            )
            atomic_write(lock_path, canonical_bytes(record))
        else:  # free
            if break_expired:
                _fail(EXIT_SCHEMA, "break_expired_on_free_lock")
            generation = _next_generation(fd)
            record = build_record(
                entry, owner, generation, admission, admission_sha, token, ttl
            )
            atomic_write(lock_path, canonical_bytes(record))

    if token_out:
        atomic_write(os.path.abspath(token_out), token.encode("utf-8"))
    return {"ok": True, "state": "held", "generation": generation,
            "file_id": entry["file_id"], "lock_path": lock_path}


def do_release(registry, entry, path, token_file, generation):
    lock_path = lock_sidecar(path, entry)
    mtx = mutex_path_for(lock_path)
    if not token_file or not os.path.exists(token_file):
        _fail(EXIT_SCHEMA, "release_requires_token_file", token_file=token_file)
    token = open(token_file, "r", encoding="utf-8").read().strip()
    token_digest = sha256_bytes(token.encode("utf-8"))
    with mutex(mtx):
        rec, _raw = read_lock(lock_path)
        if rec is None:
            _fail(EXIT_CONTENTION, "release_no_lock")
        if rec.get("token_digest") != token_digest:
            # D02: a displaced holder (its lease was legitimately broken) gets a
            # distinct typed code, not a generic token mismatch.
            if token_digest in (rec.get("displaced_token_digests") or []):
                _fail(
                    EXIT_CONTENTION,
                    "release_displaced",
                    holder=rec.get("owner"),
                    generation=rec.get("generation"),
                )
            _fail(EXIT_CONTENTION, "release_token_mismatch")
        if generation is not None and int(rec.get("generation", -1)) != int(generation):
            _fail(EXIT_CONTENTION, "release_generation_mismatch")
        os.remove(lock_path)
    return {"ok": True, "released": True, "file_id": entry["file_id"]}


def do_status(registry, entry, path):
    lock_path = lock_sidecar(path, entry)
    with mutex(mutex_path_for(lock_path)):
        rec, _raw = read_lock(lock_path)
        state = classify(rec)
        out = {"ok": True, "file_id": entry["file_id"], "state": state, "lock_path": lock_path}
        if entry.get("deny_round_007"):
            out["round_denied"] = True
            out["owner_round"] = entry.get("owner_round")
        if rec is not None:
            out["holder"] = rec.get("owner")
            out["round"] = rec.get("round")
            out["generation"] = rec.get("generation")
            out["holder_process_alive"] = holder_process_alive(rec)
            expires = parse_iso(rec.get("expires_utc", ""))
            out["remaining_seconds"] = max(0, int((expires - now_utc()).total_seconds()))
        else:
            out["remaining_seconds"] = 0
        return out


# --------------------------------------------------------------------------
# ledger
# --------------------------------------------------------------------------
LEDGER_CLI_FIELDS = [
    "round", "file", "pinned_sha256_prefix", "new_sha256_prefix",
    "superseded_by_round", "at_utc", "evidence_ref",
    "admission_ref", "admission_sha256",
]
RESOLVING_EVENTS = {"ABORTED", "COMMITTED", "RECOVERY_REQUIRED"}


def ledger_head_path(ledger_path: str) -> str:
    return ledger_path + ".head.json"


def compute_head(ledger: dict) -> dict:
    entries = ledger.get("entries", [])
    return {
        "ledger_id": LEDGER_ID,
        "count": len(entries),
        "tail_sha256": entries[-1]["entry_sha256"] if entries else None,
    }


def write_head(ledger_path: str, ledger: dict) -> None:
    atomic_write(ledger_head_path(ledger_path), canonical_bytes(compute_head(ledger)))


def verify_head(ledger_path: str, ledger: dict) -> None:
    """D03: refuse when the external head witness disagrees with the ledger."""
    head_path = ledger_head_path(ledger_path)
    if not os.path.exists(head_path):
        return  # absent witness: nothing external to contradict yet
    head = read_json(head_path)
    actual = compute_head(ledger)
    if head.get("count") != actual["count"] or head.get("tail_sha256") != actual["tail_sha256"]:
        _fail(
            EXIT_CONTENTION,
            "ledger_head_witness_mismatch",
            expected=head,
            actual=actual,
        )


def _require_nonempty(fields, key, code=EXIT_SCHEMA):
    v = fields.get(key)
    if not isinstance(v, str) or not v.strip():
        _fail(code, "entry_missing_field", field=key)


def _require_full_hex(fields, key):
    v = fields.get(key)
    if not isinstance(v, str) or not HEX64.fullmatch(v.lower()):
        _fail(EXIT_SCHEMA, "entry_digest_not_full_64_hex", field=key, value=v)


def _require_not_future(fields):
    v = fields.get("at_utc")
    if not isinstance(v, str) or not v.strip():
        _fail(EXIT_SCHEMA, "entry_missing_field", field="at_utc")
    when = parse_iso(v)
    if when > now_utc() + _dt.timedelta(seconds=FUTURE_SKEW_S):
        _fail(EXIT_SCHEMA, "entry_timestamp_in_future", at_utc=v)


def validate_cli_entry_fields(fields: dict) -> None:
    for key in LEDGER_CLI_FIELDS:
        if key not in fields:
            _fail(EXIT_SCHEMA, "entry_missing_field", field=key)
    _require_nonempty(fields, "round")
    _require_nonempty(fields, "file")
    _require_full_hex(fields, "pinned_sha256_prefix")
    _require_full_hex(fields, "new_sha256_prefix")
    _require_full_hex(fields, "admission_sha256")
    _require_nonempty(fields, "admission_ref")
    _require_nonempty(fields, "evidence_ref")
    _require_nonempty(fields, "superseded_by_round")
    _require_not_future(fields)


def validate_internal_entry_fields(fields: dict) -> None:
    _require_nonempty(fields, "round")
    _require_nonempty(fields, "file_id")
    _require_nonempty(fields, "transaction_id")
    new_sha = fields.get("new_sha256")
    if new_sha not in (None, "ABSENT"):
        _require_full_hex(fields, "new_sha256")
    pre_sha = fields.get("preimage_sha256")
    if pre_sha != "ABSENT":
        _require_full_hex(fields, "preimage_sha256")
    _require_full_hex(fields, "admission_sha256")
    _require_nonempty(fields, "admission_ref")
    _require_not_future(fields)


def load_ledger(path: str):
    if not os.path.exists(path):
        return {"schema_version": 1, "ledger_id": LEDGER_ID, "entries": []}
    led = read_json(path)
    if led.get("ledger_id") != LEDGER_ID:
        _fail(EXIT_IO, "ledger_id_mismatch", path=path)
    if not isinstance(led.get("entries"), list):
        _fail(EXIT_IO, "ledger_entries_not_list", path=path)
    prev = None
    for entry in led["entries"]:
        if not isinstance(entry, dict):
            _fail(EXIT_IO, "ledger_entry_not_object", path=path)
        body = {k: v for k, v in entry.items() if k != "entry_sha256"}
        if prev is not None and entry.get("prev_entry_sha256") != prev:
            _fail(EXIT_IO, "ledger_chain_broken", path=path, seq=entry.get("seq"))
        if entry.get("entry_sha256") != sha256_bytes(canonical_bytes(body)):
            _fail(EXIT_IO, "ledger_entry_hash_mismatch", path=path, seq=entry.get("seq"))
        prev = entry.get("entry_sha256")
    return led


def unresolved_prepared(ledger: dict) -> list:
    """D05: PREPARED entries whose transaction id was never COMMITTED."""
    prepared = {}
    committed = set()
    for entry in ledger.get("entries", []):
        txn = entry.get("transaction_id")
        if entry.get("event") == "PREPARED":
            prepared[txn] = entry
        elif entry.get("event") == "COMMITTED":
            committed.add(txn)
        elif entry.get("event") == "ABORTED":
            committed.add(txn)
    return [e for txn, e in prepared.items() if txn not in committed]


def append_entry(ledger: dict, fields: dict, event: str, path: str) -> dict:
    entries = ledger["entries"]
    prev = entries[-1]["entry_sha256"] if entries else None
    entry = {
        "seq": len(entries),
        "entry_id": "%s-%d" % (event.lower(), len(entries)),
        "event": event,
        **fields,
        "prev_entry_sha256": prev,
    }
    entry["entry_sha256"] = sha256_bytes(canonical_bytes(entry))
    entries.append(entry)
    atomic_write(path, canonical_bytes(ledger))
    write_head(path, ledger)
    return entry


def do_ledger_append(args) -> dict:
    entry_arg = args.entry
    if os.path.exists(entry_arg):
        fields = read_json(entry_arg)
    else:
        try:
            fields = json.loads(entry_arg)
        except ValueError as exc:
            _fail(EXIT_SCHEMA, "entry_not_json", error=str(exc))
    if not isinstance(fields, dict):
        _fail(EXIT_SCHEMA, "entry_not_object")
    validate_cli_entry_fields(fields)
    ledger_path = args.ledger
    mtx = mutex_path_for(ledger_path)
    with mutex(mtx):
        if args.expected_head:
            if not os.path.exists(ledger_path):
                _fail(EXIT_CONTENTION, "expected_head_but_no_ledger")
            actual = sha256_file(ledger_path)
            if actual != args.expected_head.lower():
                _fail(EXIT_CONTENTION, "ledger_head_mismatch", expected=args.expected_head, actual=actual)
        ledger = load_ledger(ledger_path)
        verify_head(ledger_path, ledger)
        # D05: any unresolved PREPARED transaction blocks a new non-resolving append.
        pending = unresolved_prepared(ledger)
        if pending and args.event not in RESOLVING_EVENTS:
            _fail(
                EXIT_CONTENTION,
                "unresolved_prepared_blocks_append",
                pending_transaction_ids=sorted(
                    str(e.get("transaction_id")) for e in pending
                ),
            )
        # Idempotency: identical event already present.
        for existing in ledger["entries"]:
            if (existing.get("file") == fields.get("file")
                    and existing.get("new_sha256_prefix") == fields.get("new_sha256_prefix")
                    and existing.get("event") == "SUPERSESSION"):
                return {"ok": True, "idempotent": True, "entry_id": existing.get("entry_id")}
        appended = append_entry(ledger, fields, args.event, ledger_path)
    return {"ok": True, "seq": appended["seq"], "entry_sha256": appended["entry_sha256"]}


def do_ledger_status(args) -> dict:
    with mutex(mutex_path_for(args.ledger)):
        ledger = load_ledger(args.ledger)
        entries = ledger["entries"]
        return {
            "ok": True,
            "entries": len(entries),
            "head_sha256": entries[-1]["entry_sha256"] if entries else None,
            "unresolved_prepared": len(unresolved_prepared(ledger)),
        }


# --------------------------------------------------------------------------
# with-lock
# --------------------------------------------------------------------------
def do_with_lock(args) -> int:
    registry = load_registry(args.registry)
    entry, path = resolve(registry, args.file)
    cmd = list(args.cmd)
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    if not cmd:
        _fail(EXIT_SCHEMA, "with_lock_requires_command")
    result = do_acquire(registry, entry, path, args.owner, args.ttl, args.admission,
                        args.token_out, False, None, None)
    token = open(args.token_out, "r", encoding="utf-8").read().strip()
    child_rc = None
    try:
        proc = subprocess.run(cmd, shell=False)
        child_rc = proc.returncode
    finally:
        do_release(registry, entry, path, args.token_out, result["generation"])
    out = {"ok": child_rc == 0, "child_rc": child_rc, "file_id": entry["file_id"]}
    sys.stdout.write(json.dumps(out, ensure_ascii=False, sort_keys=True) + "\n")
    return EXIT_OK if child_rc == 0 else EXIT_RECOVERY


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def emit(payload, code) -> int:
    payload = {"ok": code == EXIT_OK, **payload}
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
    return code


def build_parser():
    p = TypedArgumentParser(prog="hgk-ssot-lock.py")
    sub = p.add_subparsers(dest="command", required=True)

    acq = sub.add_parser("acquire")
    acq.add_argument("--file", required=True)
    acq.add_argument("--owner", required=True)
    acq.add_argument("--ttl", type=int, required=True)
    acq.add_argument("--registry", default=DEFAULT_REGISTRY)
    acq.add_argument("--admission", default=None)
    acq.add_argument("--token-out", default=None)
    acq.add_argument("--break-expired", action="store_true")
    acq.add_argument("--expected-lock-sha256", default=None)
    acq.add_argument("--reason", default=None)

    rel = sub.add_parser("release")
    rel.add_argument("--file", required=True)
    rel.add_argument("--token-file", required=True)
    rel.add_argument("--registry", default=DEFAULT_REGISTRY)
    rel.add_argument("--generation", type=int, default=None)

    st = sub.add_parser("status")
    st.add_argument("--file", required=True)
    st.add_argument("--registry", default=DEFAULT_REGISTRY)

    wl = sub.add_parser("with-lock")
    wl.add_argument("--file", required=True)
    wl.add_argument("--owner", required=True)
    wl.add_argument("--ttl", type=int, required=True)
    wl.add_argument("--registry", default=DEFAULT_REGISTRY)
    wl.add_argument("--admission", default=None)
    wl.add_argument("--token-out", default=None)
    wl.add_argument("cmd", nargs=argparse.REMAINDER)

    la = sub.add_parser("ledger-append")
    la.add_argument("--entry", required=True)
    la.add_argument("--ledger", default=DEFAULT_LEDGER)
    la.add_argument("--expected-head", default=None)
    la.add_argument("--event", default="SUPERSESSION",
                    choices=["PREPARED", "COMMITTED", "ABORTED",
                             "RECOVERY_REQUIRED", "ATTRIBUTION", "GENESIS",
                             "SUPERSESSION"])

    ls = sub.add_parser("ledger-status")
    ls.add_argument("--ledger", default=DEFAULT_LEDGER)
    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "acquire":
            registry = load_registry(args.registry)
            entry, path = resolve(registry, args.file)
            out = do_acquire(registry, entry, path, args.owner, args.ttl, args.admission,
                             args.token_out, args.break_expired, args.expected_lock_sha256,
                             args.reason)
            return emit(out, EXIT_OK)
        if args.command == "release":
            registry = load_registry(args.registry)
            entry, path = resolve(registry, args.file)
            return emit(do_release(registry, entry, path, args.token_file, args.generation), EXIT_OK)
        if args.command == "status":
            registry = load_registry(args.registry)
            entry, path = resolve(registry, args.file)
            return emit(do_status(registry, entry, path), EXIT_OK)
        if args.command == "with-lock":
            if args.token_out is None:
                _fail(EXIT_SCHEMA, "with_lock_requires_token_out")
            return do_with_lock(args)
        if args.command == "ledger-append":
            return emit(do_ledger_append(args), EXIT_OK)
        if args.command == "ledger-status":
            return emit(do_ledger_status(args), EXIT_OK)
        _fail(EXIT_SCHEMA, "unknown_command")
    except LockError as exc:
        return emit(
            {"error_code": exc.reason, "reason": exc.reason, "details": exc.details},
            exc.code,
        )


if __name__ == "__main__":
    sys.exit(main())
