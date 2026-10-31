#!/usr/bin/env python3
"""WP-FHS-17 bounded receiver: admission/grant gate, atomic WriteSet, child-attested load.

Reproduce any result:
    python tools/reproduce.ps1            (runs everything, verifies, writes evidence)
    python tools/wp17_receiver.py --help

Why this file exists (officer findings this sitting answers):

  * "parent-side pre-execution file hashing does not prove fresh Host loaded origin"
      -> `load` starts a real child. The child reads ITS OWN bytes at its own
         resolved origin, twice, and emits pid/origin/digest. The parent only
         corroborates after the child exits. A digest the parent computed before
         spawn is never accepted as load proof.
  * "the tamper negative refuses on unrelated admission subject mismatch"
      -> the tamper fixture is a VALID control that is then altered at the load
         origin. Refusal code is LOADED_ORIGIN_MISMATCH (loader stage). Gate
         codes are distinct and are tested separately.
  * "replay/preimage defects"
      -> grant subject/candidate/admission/epoch/scope are compared with the
         current need and signed admission; the nonce must be in the original
         issuance ledger AND absent from the consumption ledger; WriteSet
         preimage=ABSENT is enforced with O_CREAT|O_EXCL (atomic, no TOCTOU);
         existing targets must match their declared preimage sha.

Ceiling: this is a bounded WP-local receiver. It is not the original Host
Installer/Loader/Registry, and running it cannot by itself discharge native
acceptance. See EVIDENCE_GAP.md.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import secrets
import shutil
import subprocess
import sys
import time
from pathlib import Path

ISSUER_DIR = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS/config/issuer")
PUB_PATH = ISSUER_DIR / "issuer.pub"
OWNER_AUTH = ISSUER_DIR / "OWNER_AUTHORIZATION.json"
NONCE_LEDGER = ISSUER_DIR / "nonce-ledger.jsonl"


def canonical(obj: dict) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return sha_bytes(p.read_bytes())


def now() -> float:
    return time.time()


def emit(obj: dict, out: str | None, code: int) -> int:
    text = json.dumps(obj, ensure_ascii=False, sort_keys=True)
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(text + "\n", encoding="utf-8")
    print(text)
    return code


def refuse(code: str, detail: str, stage: str, extra: dict | None = None,
           out: str | None = None, exit_code: int = 3) -> int:
    obj = {"verdict": "REFUSED", "code": code, "stage": stage, "detail": detail,
           "at": now()}
    obj.update(extra or {})
    return emit(obj, out, exit_code)


# --------------------------------------------------------------------------- paths


def canonical_target(root: Path, rel: str) -> tuple[Path | None, str | None]:
    """Resolve root/rel and reject traversal, symlink/junction escape and any
    reparse point on the way to the leaf (the previous version only checked the
    leaf and only after the fact)."""
    root_abs = os.path.realpath(str(root))
    if not os.path.isdir(root_abs):
        return None, "ROOT_ABSENT"
    target = os.path.join(root_abs, rel)
    parent = os.path.dirname(target)
    # Walk every existing ancestor between root and the leaf.
    cur = parent
    chain = []
    while os.path.realpath(cur) != root_abs and cur not in ("", os.path.dirname(cur)):
        chain.append(cur)
        cur = os.path.dirname(cur)
    for c in chain:
        if not os.path.exists(c):
            continue
        real = os.path.realpath(c)
        if not (real == root_abs or real.startswith(root_abs + os.sep)):
            return None, "PATH_TRAVERSAL"
        try:
            attrs = os.lstat(c).st_file_attributes  # type: ignore[attr-defined]
            if attrs & 0x400:  # FILE_ATTRIBUTE_REPARSE_POINT
                return None, "PATH_ALIAS"
        except (AttributeError, OSError):
            pass
    real_leaf = os.path.realpath(target)
    if not (real_leaf == root_abs or real_leaf.startswith(root_abs + os.sep)):
        return None, "PATH_TRAVERSAL"
    if os.path.lexists(target):
        try:
            attrs = os.lstat(target).st_file_attributes  # type: ignore[attr-defined]
            if attrs & 0x400:
                return None, "PATH_ALIAS"
        except (AttributeError, OSError):
            pass
    return Path(real_leaf), None


# --------------------------------------------------------------------------- gate


def load_json(p: str | Path) -> dict:
    return json.loads(Path(p).read_text(encoding="utf-8"))


def public_key_material() -> tuple[object, str]:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

    raw = base64.b64decode(PUB_PATH.read_text(encoding="utf-8").strip())
    pub = Ed25519PublicKey.from_public_bytes(raw)
    return pub, hashlib.sha256(raw).hexdigest()[:16]


def verify_signature(record: dict, stripped: tuple[str, ...]) -> tuple[bool, str]:
    sig = record.get("signature_b64")
    if not sig:
        return False, "GRANT_UNSIGNED"
    payload = {k: v for k, v in record.items() if k not in stripped}
    try:
        pub, _kid = public_key_material()
        pub.verify(base64.b64decode(sig), canonical(payload))
    except Exception as exc:  # noqa: BLE001
        return False, f"SIGNATURE_INVALID:{type(exc).__name__}"
    return True, ""


def nonce_issued(nonce: str) -> dict | None:
    """Return the ORIGINAL issuer ledger row for `nonce`, or None.

    The row matters, not just its existence: it names the grant file the issuer
    actually signed for that nonce. A different grant that merely reuses the
    same nonce string must be refused (see `nonce_identity`)."""
    if not NONCE_LEDGER.is_file():
        return None
    for line in NONCE_LEDGER.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("nonce") == nonce:
            return row
    return None


def nonce_identity(issued_row: dict, grant: dict, grant_path: Path) -> tuple[str | None, dict]:
    """Bind the presented grant to the bytes the issuer ledgered for that nonce.

    Accept either an explicit `grant_sha256` in the ledger row or the recorded
    grant file. Fail closed when neither can be read: an unverifiable nonce is
    not an admission."""
    presented = sha_file(grant_path) if grant_path.is_file() else None
    observed = {"presented_grant_sha256": presented}
    want = issued_row.get("grant_sha256")
    if want:
        observed["ledger_grant_sha256"] = want
        observed["ledger_source"] = "row.grant_sha256"
        return (None if presented == want else "ERR_NONCE_GRANT_MISMATCH"), observed
    led_path = issued_row.get("grant")
    if not led_path:
        return "ERR_NONCE_GRANT_UNVERIFIABLE", observed
    lp = Path(led_path)
    observed["ledger_grant_path"] = str(lp)
    if not lp.is_file():
        return "ERR_NONCE_GRANT_UNVERIFIABLE", observed
    want = sha_file(lp)
    observed["ledger_grant_sha256"] = want
    observed["ledger_source"] = "row.grant file bytes"
    return (None if presented == want else "ERR_NONCE_GRANT_MISMATCH"), observed


def nonce_consumed(ledger: Path, nonce: str) -> dict | None:
    if not ledger.is_file():
        return None
    for line in ledger.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("nonce") == nonce:
            return row
    return None


def consume_nonce(ledger: Path, nonce: str, extra: dict) -> None:
    ledger.parent.mkdir(parents=True, exist_ok=True)
    row = {"nonce": nonce, "consumed_at": now()}
    row.update(extra)
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def check_bindings(grant: dict, adm: dict, need: dict) -> str | None:
    """The predicate the previous validate_grant only half-implemented: fields
    had to be non-empty but were never compared with the current need."""
    if grant.get("subject") != need.get("subject"):
        return "ERR_GRANT_NEED_SUBJECT_MISMATCH"
    if grant.get("candidate_sha256") != need.get("candidate_sha256"):
        return "ERR_GRANT_NEED_CANDIDATE_MISMATCH"
    if grant.get("admission_id") != adm.get("admission_id"):
        return "ERR_GRANT_ADMISSION_MISMATCH"
    if str(grant.get("policy_epoch")) != str(need.get("policy_epoch")):
        return "ERR_GRANT_EPOCH_MISMATCH"
    if not str(grant.get("scope") or "").strip():
        return "ERR_GRANT_SCOPE_MISSING"
    return None


def check_writeset(grant: dict, writeset: list[dict], root: Path) -> tuple[str | None, list[dict]]:
    declared = [(w.get("path"), w.get("preimage")) for w in grant.get("writeset") or []]
    needed = [(w.get("path"), w.get("preimage")) for w in writeset]
    if sorted(declared) != sorted(needed):
        return "ERR_GRANT_WRITESET_MISMATCH", []
    observed = []
    for w in writeset:
        target, bad = canonical_target(root, w["path"])
        if bad:
            return bad, observed
        obs = {"path": w["path"], "resolved": str(target),
               "preimage_declared": w.get("preimage"),
               "preimage_observed": "ABSENT" if not target.exists() else "PRESENT"}
        if w.get("preimage") == "ABSENT":
            if target.exists():
                return "ERR_PREIMAGE_NOT_ABSENT", observed + [obs]
        else:
            if not target.exists():
                return "ERR_PREIMAGE_MISSING", observed + [obs]
            got = sha_file(target)
            obs["preimage_sha256"] = got
            if w.get("preimage_sha256") and got != w["preimage_sha256"]:
                return "ERR_PREIMAGE_MISMATCH", observed + [obs]
        observed.append(obs)
    return None, observed


def evaluate_gate(need: dict, grant: dict, adm: dict, writeset: list[dict],
                  root: Path, ledger: Path, grant_path: Path) -> tuple[str | None, dict]:
    """Ordered, named checks. Returns (refusal_code|None, trace)."""
    trace: dict = {"checks": []}

    def step(name: str, ok: bool, code: str) -> bool:
        trace["checks"].append({"check": name, "ok": ok, "code": None if ok else code})
        return ok

    if not step("admission_shape", bool(adm.get("admission_id")), "ERR_ADMISSION_MISSING"):
        return "ERR_ADMISSION_MISSING", trace
    ok, why = verify_signature(adm, ("signature_b64", "signature_alg"))
    if not step("admission_signature", ok, f"ERR_ADMISSION_INVALID:{why}"):
        return f"ERR_ADMISSION_INVALID:{why}", trace
    try:
        _pub, kid = public_key_material()
    except Exception as exc:  # noqa: BLE001
        return f"ERR_ISSUER_PUBLIC_KEY:{type(exc).__name__}", trace
    if not step("admission_key_id", adm.get("key_id") == kid, "ERR_ADMISSION_KEY_UNKNOWN"):
        return "ERR_ADMISSION_KEY_UNKNOWN", trace
    if not step("admission_not_expired", float(adm.get("expires_at") or 0) >= now(),
                "ERR_ADMISSION_EXPIRED"):
        return "ERR_ADMISSION_EXPIRED", trace
    if not step("admission_subject", adm.get("subject") == need.get("subject"),
                "ERR_ADMISSION_SUBJECT_MISMATCH"):
        return "ERR_ADMISSION_SUBJECT_MISMATCH", trace
    if not step("admission_candidate", adm.get("candidate_sha256") == need.get("candidate_sha256"),
                "ERR_ADMISSION_CANDIDATE_MISMATCH"):
        return "ERR_ADMISSION_CANDIDATE_MISMATCH", trace
    if not step("admission_operation", adm.get("operation") == "install_occupant",
                "ERR_ADMISSION_OPERATION_MISMATCH"):
        return "ERR_ADMISSION_OPERATION_MISMATCH", trace

    ok, why = verify_signature(grant, ("signature_b64", "signature_alg", "assurance_level"))
    if not step("grant_signature", ok, f"ERR_GRANT_SIGNATURE:{why}"):
        return f"ERR_GRANT_SIGNATURE:{why}", trace
    if not step("grant_key_id", grant.get("key_id") == kid, "ERR_GRANT_KEY_UNKNOWN"):
        return "ERR_GRANT_KEY_UNKNOWN", trace
    owner_sha = sha_file(OWNER_AUTH)
    if not step("grant_owner_authorization", grant.get("owner_authorization_sha256") == owner_sha,
                "ERR_GRANT_OWNER_AUTHORIZATION_MISMATCH"):
        return "ERR_GRANT_OWNER_AUTHORIZATION_MISMATCH", trace
    # A conformance label is not a weaker permit that still installs; for HOST_OP
    # it is not a permit at all.
    if not step("grant_production_assurance",
                grant.get("assurance_level") == "PRODUCTION_ISSUER_SOFTWARE",
                "ERR_GRANT_UNSIGNED_DOWNGRADE"):
        return "ERR_GRANT_UNSIGNED_DOWNGRADE", trace
    if not step("grant_operation", grant.get("operation") == "install_occupant",
                "ERR_GRANT_OPERATION"):
        return "ERR_GRANT_OPERATION", trace
    # A signed grant that names no admission is a permission slip with no file.
    if not step("grant_names_admission", bool(str(grant.get("admission_id") or "").strip()),
                "ERR_ADMISSION_BYPASS"):
        return "ERR_ADMISSION_BYPASS", trace
    bad = check_bindings(grant, adm, need)
    if not step("grant_need_admission_binding", bad is None, bad or "BINDING"):
        return bad, trace
    replay = nonce_consumed(ledger, grant.get("nonce", ""))
    if not step("nonce_unspent", replay is None, "ERR_NONCE_REPLAY"):
        trace["prior_consumption"] = replay
        return "ERR_NONCE_REPLAY", trace
    # Read-only checks from here: the WriteSet preimage is inspected before the
    # issuance/TTL checks so that a preimage conflict is named explicitly. No
    # effect happens until every check passes.
    bad, observed = check_writeset(grant, writeset, root)
    trace["writeset_observed"] = observed
    if not step("writeset_and_preimage", bad is None, bad or "WRITESET"):
        return bad, trace
    issued_row = nonce_issued(grant.get("nonce", ""))
    if not step("nonce_issued_by_original_ledger", issued_row is not None, "ERR_NONCE_NOT_ISSUED"):
        return "ERR_NONCE_NOT_ISSUED", trace
    bad, id_obs = nonce_identity(issued_row, grant, grant_path)
    trace["nonce_identity"] = id_obs
    if not step("nonce_bound_to_ledgered_grant", bad is None, bad or "NONCE_IDENTITY"):
        return bad, trace
    if not step("grant_ttl_live", float(grant.get("expires_at") or 0) >= now(), "ERR_GRANT_EXPIRED"):
        return "ERR_GRANT_EXPIRED", trace
    return None, trace


# --------------------------------------------------------------------------- effect


def atomic_write_absent(target: Path, data: bytes) -> None:
    """preimage=ABSENT must be atomic: O_EXCL, never truncate-then-write."""
    fd = os.open(str(target), os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0), 0o644)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
    except Exception:
        try:
            os.unlink(str(target))
        except OSError:
            pass
        raise


def read_journal(p: Path) -> list[dict]:
    if not p.is_file():
        return []
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def append_journal(p: Path, row: dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def apply_writeset(root: Path, writeset: list[dict], sources: dict[str, bytes],
                   journal: Path, phase: str) -> dict:
    written: list[dict] = []
    try:
        for w in writeset:
            target, bad = canonical_target(root, w["path"])
            if bad:
                raise RuntimeError(bad)
            target.parent.mkdir(parents=True, exist_ok=True)
            atomic_write_absent(target, sources[w["path"]])
            rec = {"path": w["path"], "resolved": str(target),
                   "sha256": sha_file(target), "bytes": target.stat().st_size}
            written.append(rec)
            append_journal(journal, {"phase": phase, "status": "WRITTEN", **rec})
    except Exception as exc:  # noqa: BLE001
        # Compensate exactly what this operation wrote; touch nothing else.
        removed = []
        for rec in reversed(written):
            try:
                os.unlink(rec["resolved"])
                removed.append(rec["path"])
            except OSError:
                pass
        append_journal(journal, {"phase": phase, "status": "ABORTED",
                                 "error": str(exc), "compensated": removed})
        raise
    return {"written": written, "journal": str(journal)}


def tree_manifest(root: Path) -> list[dict]:
    out = []
    if not root.exists():
        return out
    for p in sorted(root.rglob("*")):
        if p.is_file():
            out.append({"rel": str(p.relative_to(root)).replace("\\", "/"),
                        "sha256": sha_file(p), "bytes": p.stat().st_size})
    return out


# --------------------------------------------------------------------------- load


def load_and_invoke(root: Path, need: dict, pinned: str, input_obj: dict,
                    consumer: Path, delay_ms: int, tamper_after_ms: int,
                    out: str | None, gate: dict | None = None,
                    local_loader_control: bool = False) -> int:
    # A load is either part of the admitted operation or an explicitly labelled
    # local loader measurement. The latter is never reported as HOST_OP success.
    gate_trace: dict = {}
    admission_context = "NOT_EVALUATED"
    if gate is not None:
        bad, gate_trace = evaluate_gate(need, gate["grant"], gate["admission"],
                                        gate["writeset"], root, Path(gate["ledger"]),
                                        Path(gate["grant_path"]))
        if bad:
            return refuse(bad, "the grant/admission gate did not pass for this need",
                          "GATE", {"gate": gate_trace}, out=out)
        admission_context = "GATED_GRANT_AND_ADMISSION"
    elif local_loader_control:
        admission_context = "NOT_ADMITTED_LOCAL_LOADER_CONTROL"
    else:
        return refuse("GATE_CONTEXT_REQUIRED",
                      "load requires --grant --admission --writeset --ledger (or --local-loader-control)",
                      "LOAD", out=out)
    entry_target, bad = canonical_target(root, need["entry_point"])
    if bad:
        return refuse(bad, f"entry {need['entry_point']} is not canonical under {root}", "LOAD", out=out)
    if not entry_target.is_file():
        return refuse("LOADED_ORIGIN_MISSING", f"{entry_target} does not exist", "LOAD", out=out)
    occ = (need.get("needed_occupants") or [{}])[0]
    pinned_manifest = occ.get("manifest_sha256")
    subject_sha = need.get("subject_sha256")
    if not pinned_manifest or not subject_sha:
        return refuse("NEED_INCOMPLETE", "need lacks occupant manifest sha / subject sha", "LOAD", out=out)
    # The input is the real feature input plus the loader's expectation. The
    # occupant refuses if the expectation does not match the bytes it loaded.
    input_obj = dict(input_obj)
    input_obj.setdefault("need_id", need.get("need_id"))
    input_obj.setdefault("subject_sha256", subject_sha)
    input_obj.setdefault("nonce", need.get("draft_nonce") or "DRAFT-NO-GRANT")
    input_obj["expect"] = {"occupant_sha256": pinned, "manifest_sha256": pinned_manifest}
    run_dir = Path(out).parent if out else Path(".")
    run_dir.mkdir(parents=True, exist_ok=True)
    # The child runs with cwd=entry_target.parent (the resolved load origin), so
    # every path handed to it must be absolute; a relative path would be
    # re-resolved against the occupant directory and vanish.
    run_dir = run_dir.resolve()
    # Per-run token: it is passed only on THIS spawn's command line and echoed
    # by the occupant. An attestation file left over from another run, or one
    # produced by a process we did not start, cannot carry it.
    run_token = secrets.token_hex(16)
    attest = run_dir / ("attest-" + str(os.getpid()) + "-" + str(int(now() * 1000)) + ".json")
    inp = run_dir / ("input-" + str(int(now() * 1000)) + ".json")
    inp.write_text(json.dumps(input_obj, ensure_ascii=False), encoding="utf-8")

    parent_pre = sha_file(entry_target)
    proc = subprocess.Popen(
        [sys.executable, str(entry_target), "--input", str(inp),
         "--attest-out", str(attest), "--delay-ms", str(delay_ms),
         "--token", run_token],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=str(entry_target.parent))
    if tamper_after_ms > 0:
        import threading

        injected = (b"# foreign bytes injected at the resolved load origin\n"
                    b"raise SystemExit('foreign occupant should never qualify')\n")
        injection_observed: dict = {}

        def poison() -> None:
            time.sleep(tamper_after_ms / 1000.0)
            entry_target.write_bytes(injected)
            injection_observed["sha256"] = sha_file(entry_target)
            injection_observed["bytes"] = len(injected)

        threading.Thread(target=poison, daemon=True).start()
    stdout, stderr = proc.communicate(timeout=180)
    parent_post = sha_file(entry_target)
    if not attest.is_file():
        return refuse("LOADED_ATTESTATION_MISSING",
                      f"child produced no attestation; rc={proc.returncode} stderr={stderr[-300:]}",
                      "LOAD", {"stdout": stdout[-400:]}, out=out)
    rec = json.loads(attest.read_text(encoding="utf-8"))
    ack = rec.get("ack") or {}
    # The interpreter on this host is a launcher shim, so the process that
    # `Popen` returns is often the parent of the real interpreter. Lineage is
    # therefore "this pid, or the immediate child of this pid" -- and it must
    # also carry the per-run token, so lineage alone is never sufficient.
    attest_pid = int(rec.get("pid") or 0)
    attest_ppid = int(rec.get("ppid") or 0)
    lineage_ok = attest_pid == proc.pid or attest_ppid == proc.pid
    checks = {
        "child_token_matches_run": rec.get("token") == run_token,
        "child_lineage_is_spawned_process": lineage_ok,
        "child_origin_is_canonical": Path(rec.get("origin", "")).resolve() == entry_target,
        "child_start_sha_is_pinned": rec.get("sha_at_start") == pinned,
        "child_end_sha_is_pinned": rec.get("sha_at_end") == pinned,
        "child_manifest_sha_is_pinned": rec.get("manifest_sha256") == pinned_manifest,
        "child_input_sha_is_recorded": rec.get("input_sha256") == sha_bytes(canonical(input_obj)),
        "parent_post_sha_is_pinned": parent_post == pinned,
        "child_sha_stable_during_invoke": rec.get("sha_at_start") == rec.get("sha_at_end"),
        "ack_loaded_sha_is_pinned": ack.get("loaded_sha256") == pinned,
        "ack_manifest_sha_is_pinned": ack.get("manifest_sha256") == pinned_manifest,
        "ack_subject_is_bound": ack.get("subject_sha256") == subject_sha,
        "ack_input_sha_matches_loader_input": ack.get("input_sha256") == sha_bytes(canonical(input_obj)),
        "ack_functional_output_present": bool(ack.get("functional_output")),
        "ack_digest_matches": ack.get("ack_digest") == sha_bytes(canonical(
            {k: v for k, v in ack.items() if k != "ack_digest"})),
        "child_exit_zero": proc.returncode == 0,
    }
    failed = [k for k, v in checks.items() if not v]
    base = {
        "entry_point": need["entry_point"],
        "admission_context": admission_context,
        "gate_trace": gate_trace,
        "claim_ceiling": ("LOCAL_LOADER_MEASUREMENT_ONLY" if gate is None
                           else "BOUNDED_RECEIVER_GATED_LOAD"),
        "resolved_origin": str(entry_target),
        "pinned_sha256": pinned,
        "child_pid": proc.pid,
        "attested_pid": attest_pid,
        "attested_ppid": attest_ppid,
        "run_token_sha256": sha_bytes(run_token.encode("utf-8")),
        "lineage": {"spawned_pid": proc.pid, "attested_pid": attest_pid,
                    "attested_ppid": attest_ppid,
                    "interpreter": sys.executable,
                    "launcher_shim": attest_ppid == proc.pid and attest_pid != proc.pid},
        "parent_pre_sha256_not_used_as_proof": parent_pre,
        "parent_post_sha256": parent_post,
        "child_attestation": {k: rec.get(k) for k in
                              ("origin", "origin_end", "pid", "ppid", "python",
                               "sha_at_start", "sha_at_end", "changed_during_invoke",
                               "manifest_sha256", "input_sha256", "functional_output",
                               "token")},
        "input_file": str(inp),
        "input_sha256": sha_bytes(canonical(input_obj)),
        "tamper": ({"requested": True, "after_ms": tamper_after_ms,
                     "injection_observed": injection_observed,
                     "injection_detected_at_origin": bool(injection_observed)} if tamper_after_ms > 0 else {"requested": False}),
        "ack": ack,
        "checks": checks,
        "child_stdout": stdout.strip()[-600:],
        "child_stderr": stderr.strip()[-600:],
    }
    if failed:
        if "child_sha_stable_during_invoke" in failed or "child_end_sha_is_pinned" in failed:
            code, stage = "LOADED_CHANGED_DURING_INVOKE", "LOAD"
        elif "child_origin_is_canonical" in failed:
            code, stage = "LOADED_ORIGIN_UNRESOLVED", "LOAD"
        else:
            code, stage = "LOADED_ORIGIN_MISMATCH", "LOAD"
        base.update({"failed_checks": failed, "code": code})
        obj = {"verdict": "REFUSED", "code": code, "stage": stage,
               "detail": "the bytes at the resolved load origin are not the pinned candidate",
               "observed": {"pinned": pinned, "child_start": rec.get("sha_at_start"),
                            "child_end": rec.get("sha_at_end"), "parent_post": parent_post},
               "at": now()}
        obj.update(base)
        return emit(obj, out, 3)

    # Consumer readback: independent re-derivation, separate process, distinct pid.
    cproc = subprocess.run([sys.executable, str(consumer), "--attest", str(attest),
                            "--pinned-sha", pinned,
                            "--pinned-manifest-sha", pinned_manifest,
                            "--subject-sha", subject_sha,
                            "--input", str(inp),
                            "--origin", str(entry_target),
                            "--token", run_token],
                           capture_output=True, text=True, timeout=120)
    try:
        consumer_rec = json.loads(cproc.stdout.strip().splitlines()[-1])
    except Exception:  # noqa: BLE001
        consumer_rec = {"verdict": "CONSUMER_UNPARSEABLE", "raw": cproc.stdout[-400:]}
    obj = {
        "verdict": "LOADED_AND_INVOKED",
        "states": ["HOST_LOADED", "INVOKED", "FUNCTIONALLY_QUALIFIED"],
        "loaded_sha256": pinned,
        "consumer_verdict": consumer_rec.get("verdict"),
        "consumer": consumer_rec,
        "consumer_exit": cproc.returncode,
        "at": now(),
    }
    obj.update(base)
    ok = consumer_rec.get("verdict") == "CONSUMER_ACK" and cproc.returncode == 0
    if not ok:
        obj["verdict"] = "REFUSED"
        obj["code"] = "CONSUMER_BINDING_REFUSED"
        obj["stage"] = "CONSUMER"
        return emit(obj, out, 3)
    return emit(obj, out, 0)


# --------------------------------------------------------------------------- dag


def dag_evaluate(fixture: dict, mode: str) -> dict:
    nodes = fixture["nodes"]
    edges = [tuple(e) for e in fixture["edges"]]
    if mode == "mutant":
        edges = edges + [tuple(fixture["mutant_added_edge"])]
    states = dict(fixture["control_states"])
    deps: dict[str, list[str]] = {n: [] for n in nodes}
    for a, b in edges:
        deps.setdefault(b, []).append(a)

    def ancestors(n: str, seen: set[str]) -> set[str]:
        out: set[str] = set()
        for p in deps.get(n, []):
            if p in seen:
                out.add(p)
                continue
            seen.add(p)
            out.add(p)
            out |= ancestors(p, seen)
        return out

    anc = ancestors("WP-FHS-17", set())
    cycle = "WP-FHS-17" in anc or "WP-FHS-17" in deps.get("WP-FHS-17", [])
    unmet = [p for p in deps.get("WP-FHS-17", []) if states.get(p) != "READY"]
    dispatched = not cycle and not unmet
    return {
        "mode": mode,
        "edges_evaluated": [list(e) for e in edges],
        "wp17_dependencies": deps.get("WP-FHS-17", []),
        "wp06_state": states.get("WP06"),
        "dependency_cycle_through_wp17": cycle,
        "ancestors_of_wp17": sorted(anc),
        "unmet_dependencies": unmet,
        "dispatch_allowed": dispatched,
        "first_fail": None if dispatched else "WP-FHS-17.FIRST_FAIL:CAP_BOOT_DEPENDENCY_INVERSION",
        "dispatch_attempted": dispatched,
        "effects": 0 if not dispatched else None,
    }


# --------------------------------------------------------------------------- self test


def self_test() -> int:
    """Re-runnable proof of the mechanisms the officer challenged, without any
    install. Each case asserts the refusal/acceptance code it claims."""
    import tempfile

    results = []
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "root"
        root.mkdir()

        def case(name: str, got, want) -> None:
            results.append({"case": name, "got": got, "want": want, "ok": got == want})
            assert got == want, (name, got, want)

        t, bad = canonical_target(root, "../escape.py")
        case("traversal_refused", bad, "PATH_TRAVERSAL")
        t, bad = canonical_target(root, "a/b.py")
        case("clean_target", bad, None)

        f = root / "exists.py"
        f.write_bytes(b"orig")
        try:
            atomic_write_absent(f, b"new")
            case("exclusive_create_refused_existing", "WROTE", "FileExistsError")
        except FileExistsError:
            case("exclusive_create_refused_existing", "FileExistsError", "FileExistsError")
        case("existing_bytes_untouched", f.read_bytes().hex(), b"orig".hex())

        ws = [{"path": "exists.py", "preimage": "ABSENT"}]
        code, obs = check_writeset({"writeset": ws}, ws, root)
        case("preimage_absent_conflict", code, "ERR_PREIMAGE_NOT_ABSENT")
        code, obs = check_writeset(
            {"writeset": [{"path": "exists.py", "preimage": "PRESENT",
                           "preimage_sha256": "0" * 64}]},
            [{"path": "exists.py", "preimage": "PRESENT", "preimage_sha256": "0" * 64}], root)
        case("preimage_sha_mismatch", code, "ERR_PREIMAGE_MISMATCH")

        fixture = {"nodes": ["WP-FHS-00", "WP-FHS-02", "WP-FHS-03", "WP-FHS-06", "WP-FHS-17"],
                   "edges": [["WP-FHS-17", "WP-FHS-06"]],
                   "mutant_added_edge": ["WP-FHS-06", "WP-FHS-17"],
                   "control_states": {"WP-FHS-00": "READY", "WP-FHS-02": "READY",
                                      "WP-FHS-03": "READY", "WP-FHS-06": "INCOMPLETE",
                                      "WP-FHS-17": "NOT_RUN"}}
        c = dag_evaluate(fixture, "control")
        case("dag_control_dispatch", c["dispatch_allowed"], True)
        m = dag_evaluate(fixture, "mutant")
        case("dag_mutant_first_fail", m["first_fail"],
             "WP-FHS-17.FIRST_FAIL:CAP_BOOT_DEPENDENCY_INVERSION")
        case("dag_mutant_zero_effect", m["effects"], 0)

        led = Path(td) / "ledger.jsonl"
        consumed = Path(td) / "consumed.jsonl"
        other = Path(td) / "other.json"
        other.write_text("{}", encoding="utf-8")
        row = {"nonce": "N1", "grant": str(other)}
        code, obs = nonce_identity(row, {"nonce": "N1"}, other)
        case("nonce_identity_same_bytes", code, None)
        code, obs = nonce_identity({"nonce": "N2", "grant": str(Path(td) / "missing.json")},
                                   {"nonce": "N2"}, Path(td) / "x.json")
        case("nonce_identity_unverifiable", code, "ERR_NONCE_GRANT_UNVERIFIABLE")
        consume_nonce(consumed, "N1", {"why": "self-test"})
        case("replay_seen", bool(nonce_consumed(consumed, "N1")), True)
    print(json.dumps({"self_test": "PASS" if all(r["ok"] for r in results) else "FAIL",
                      "cases": results}, ensure_ascii=False, sort_keys=True))
    return 0


# --------------------------------------------------------------------------- cli


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("gate")
    for name in ("need", "grant", "admission", "writeset", "root", "ledger", "out"):
        g.add_argument("--" + name, required=name != "out")
    g.add_argument("--consume", action="store_true")

    ins = sub.add_parser("install")
    for name in ("need", "grant", "admission", "writeset", "package", "root",
                 "ledger", "journal"):
        ins.add_argument("--" + name, required=True)
    ins.add_argument("--out", required=True)

    ws = sub.add_parser("writeset")
    ws.add_argument("--writeset", required=True)
    ws.add_argument("--root", required=True)
    ws.add_argument("--out", required=True)

    bd = sub.add_parser("bind")
    for name in ("need", "grant", "admission", "out"):
        bd.add_argument("--" + name, required=True)

    st = sub.add_parser("stage")
    for name in ("package", "root", "state", "scope-file"):
        st.add_argument("--" + name, required=True)
    st.add_argument("--out", required=True)

    ld = sub.add_parser("load")
    for name in ("root", "need", "pinned-sha", "input", "consumer"):
        ld.add_argument("--" + name, required=True)
    ld.add_argument("--out", required=True)
    ld.add_argument("--delay-ms", type=int, default=0)
    ld.add_argument("--tamper-after-ms", type=int, default=0)
    for name in ("grant", "admission", "writeset", "ledger"):
        ld.add_argument("--" + name)
    ld.add_argument("--local-loader-control", action="store_true")

    rb = sub.add_parser("rollback")
    for name in ("journal", "root", "out"):
        rb.add_argument("--" + name, required=True)

    rc = sub.add_parser("reconcile")
    for name in ("journal", "root", "out"):
        rc.add_argument("--" + name, required=True)

    dg = sub.add_parser("dag")
    for name in ("fixture", "out"):
        dg.add_argument("--" + name, required=True)
    dg.add_argument("--mode", choices=["control", "mutant"], required=True)

    sub.add_parser("selftest")

    mu = sub.add_parser("mark-unknown")
    for name in ("journal", "root", "path", "sha", "out"):
        mu.add_argument("--" + name, required=True)

    a = ap.parse_args(argv)

    if a.cmd == "selftest":
        return self_test()

    if a.cmd == "gate":
        if not Path(a.grant).is_file():
            return emit({"verdict": "PARK_GRANT_MISSING", "code": "ERR_GRANT_MISSING",
                         "missing_object": "original-Issuer OPS grant for operation=install_occupant",
                         "detail": "no grant file: an install is a HOST_OP", "at": now()},
                        a.out, 5)
        need, grant, adm = load_json(a.need), load_json(a.grant), load_json(a.admission)
        ws = load_json(a.writeset)
        writeset = ws.get("writeset") if isinstance(ws, dict) else ws
        code, trace = evaluate_gate(need, grant, adm, writeset, Path(a.root),
                                    Path(a.ledger), Path(a.grant))
        if code in ("ERR_GRANT_EXPIRED", "ERR_NONCE_NOT_ISSUED"):
            obj = {"verdict": "PARK_GRANT_NOT_LIVE", "code": code,
                   "missing_object": "live original-Issuer OPS grant for operation=install_occupant",
                   "trace": trace, "at": now()}
            return emit(obj, a.out, 5)
        if code:
            return refuse(code, "gate refused before any effect", "GATE", {"trace": trace}, a.out)
        if a.consume:
            consume_nonce(Path(a.ledger), grant["nonce"], {
                "operation": "install_occupant", "subject": need["subject"],
                "candidate_sha256": need["candidate_sha256"], "grant_sha256": sha_file(Path(a.grant))})
        return emit({"verdict": "GRANT_OK", "trace": trace, "at": now()}, a.out, 0)

    if a.cmd == "install":
        root = Path(a.root)
        if not Path(a.grant).is_file():
            return emit({"verdict": "PARK_GRANT_MISSING", "code": "ERR_GRANT_MISSING",
                         "missing_object": "original-Issuer OPS grant for operation=install_occupant",
                         "effects": 0, "at": now()}, a.out, 5)
        need, grant, adm = load_json(a.need), load_json(a.grant), load_json(a.admission)
        ws = load_json(a.writeset)
        writeset = ws.get("writeset") if isinstance(ws, dict) else ws
        before = tree_manifest(root)
        code, trace = evaluate_gate(need, grant, adm, writeset, root,
                                    Path(a.ledger), Path(a.grant))
        if code in ("ERR_GRANT_EXPIRED", "ERR_NONCE_NOT_ISSUED"):
            return emit({"verdict": "PARK_GRANT_NOT_LIVE", "code": code,
                         "missing_object": "live original-Issuer OPS grant (TTL must be open at effect time)",
                         "effects": 0, "tree_before": before, "tree_after": tree_manifest(root),
                         "trace": trace, "at": now()}, a.out, 5)
        if code:
            return refuse(code, "gate refused before any effect", "GATE",
                          {"effects": 0, "tree_before": before, "trace": trace}, a.out)
        pkg = Path(a.package)
        sources = {}
        for w in writeset:
            src = pkg / w["path"]
            if not src.is_file():
                return refuse("ERR_SOURCE_MISSING", str(src), "PACKAGE",
                              {"effects": 0}, a.out)
            sources[w["path"]] = src.read_bytes()
        consume_nonce(Path(a.ledger), grant["nonce"], {
            "operation": "install_occupant", "subject": need["subject"],
            "candidate_sha256": need["candidate_sha256"], "grant_sha256": sha_file(Path(a.grant))})
        result = apply_writeset(root, writeset, sources, Path(a.journal), "INSTALL")
        for rec in result["written"]:
            rec["matches_package"] = rec["sha256"] == sha_bytes(sources[rec["path"]])
        return emit({"verdict": "INSTALLED", "effect_class": "HOST_OP",
                     "states": ["PACKAGED", "GRANT_OK", "INSTALLED"],
                     "written": result["written"], "tree_after": tree_manifest(root),
                     "trace": trace, "at": now()}, a.out, 0)

    if a.cmd == "writeset":
        ws = load_json(a.writeset)
        writeset = ws.get("writeset") if isinstance(ws, dict) else ws
        bad, observed = check_writeset({"writeset": writeset}, writeset, Path(a.root))
        obj = {"verdict": "WRITESET_OK" if bad is None else "REFUSED",
               "code": bad, "observed": observed, "at": now()}
        return emit(obj, a.out, 0 if bad is None else 3)

    if a.cmd == "bind":
        bad = check_bindings(load_json(a.grant), load_json(a.admission), load_json(a.need))
        return emit({"verdict": "BINDING_OK" if bad is None else "REFUSED",
                     "code": bad, "at": now()}, a.out, 0 if bad is None else 3)

    if a.cmd == "stage":
        pkg = Path(a.package)
        root = Path(a.root)
        scope = load_json(a.scope_file)
        owner_sha = sha_file(OWNER_AUTH)
        if scope.get("wp") != "WP-FHS-17":
            return refuse("ERR_SCOPE_SUBJECT", "draft scope is not for WP-FHS-17", "STAGE", out=a.out)
        if scope.get("authorized_by_sha256") != owner_sha:
            return refuse("ERR_SCOPE_UNAUTHORIZED",
                          "draft scope does not bind the recorded owner authorization",
                          "STAGE", out=a.out)
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)
        files = [p for p in sorted(pkg.rglob("*")) if p.is_file()]
        written = []
        for p in files:
            rel = str(p.relative_to(pkg)).replace("\\", "/")
            target, bad = canonical_target(root, rel)
            if bad:
                return refuse(bad, rel, "STAGE", out=a.out)
            target.parent.mkdir(parents=True, exist_ok=True)
            atomic_write_absent(target, p.read_bytes())
            written.append({"path": rel, "resolved": str(target),
                            "sha256": sha_file(target), "bytes": target.stat().st_size})
        state = Path(a.state)
        state.mkdir(parents=True, exist_ok=True)
        append_journal(state / "journal.jsonl", {"phase": "STAGE", "status": "STAGED",
                                                 "root": str(root), "files": written})
        return emit({"verdict": "STAGED", "root": str(root), "effect_class": "LOCAL_DRAFT_STAGE",
                     "scope": scope, "files": written,
                     "states": ["PACKAGED", "STAGED"], "at": now()}, a.out, 0)

    if a.cmd == "load":
        need = load_json(a.need)
        gate = None
        if not a.local_loader_control:
            missing = [n for n in ("grant", "admission", "writeset", "ledger")
                       if not getattr(a, n)]
            if missing:
                return refuse("GATE_CONTEXT_REQUIRED",
                              "missing " + ", ".join("--" + n for n in missing),
                              "LOAD", out=a.out)
            ws = load_json(a.writeset)
            writeset = ws.get("writeset") if isinstance(ws, dict) else ws
            gate = {"grant": load_json(a.grant), "admission": load_json(a.admission),
                    "writeset": writeset, "ledger": a.ledger, "grant_path": a.grant}
        return load_and_invoke(Path(a.root), need, a.pinned_sha, load_json(a.input),
                               Path(a.consumer), a.delay_ms, a.tamper_after_ms, a.out,
                               gate, a.local_loader_control)

    if a.cmd == "rollback":
        journal = Path(a.journal)
        rows = read_journal(journal)
        staged = [r for r in rows if r.get("phase") == "STAGE" and r.get("status") == "STAGED"]
        done = [r for r in rows if r.get("phase") == "ROLLBACK" and r.get("status") == "REMOVED"]
        if done:
            return emit({"verdict": "ALREADY_ROLLED_BACK", "removed": [], "residue": [],
                         "note": "same-key repeat is a no-op; no second effect"}, a.out, 0)
        if not staged:
            return refuse("ERR_NOTHING_TO_ROLLBACK", "no STAGED journal rows", "ROLLBACK", out=a.out)
        removed, skipped = [], []
        for r in staged:
            for f in r["files"]:
                p = Path(f["resolved"])
                if p.is_file():
                    os.unlink(p)
                    removed.append(f["path"])
                else:
                    skipped.append(f["path"])
        residue = []
        root = Path(a.root)
        for entry in tree_manifest(root):
            residue.append(entry["rel"])
        append_journal(journal, {"phase": "ROLLBACK", "status": "REMOVED",
                                 "removed": removed, "residue": residue})
        return emit({"verdict": "ROLLED_BACK" if not residue else "RESIDUE",
                     "removed": removed, "already_absent": skipped,
                     "residue": residue, "at": now()}, a.out, 0 if not residue else 3)

    if a.cmd == "reconcile":
        rows = read_journal(Path(a.journal))
        unknown = [r for r in rows if r.get("status") == "UNKNOWN"]
        results = []
        for r in unknown:
            p = Path(r["resolved"])
            on_disk = sha_file(p) if p.is_file() else None
            results.append({"path": r["path"], "journal": "UNKNOWN",
                            "on_disk_sha256": on_disk,
                            "expected_sha256": r.get("sha256"),
                            "reconciled": "PRESENT_MATCH" if on_disk == r.get("sha256") else
                                          ("ABSENT" if on_disk is None else "PRESENT_DIFFERS"),
                            "replayed": False})
        append_journal(Path(a.journal), {"phase": "RECONCILE", "status": "RECONCILED",
                                         "results": results})
        return emit({"verdict": "RECONCILED", "results": results,
                     "note": "UNKNOWN effects are read back, never blindly replayed",
                     "at": now()}, a.out, 0)

    if a.cmd == "dag":
        fixture = load_json(a.fixture)
        return emit(dag_evaluate(fixture, a.mode), a.out, 0)

    if a.cmd == "mark-unknown":
        root = Path(a.root)
        target, bad = canonical_target(root, a.path)
        if bad:
            return refuse(bad, a.path, "JOURNAL", out=a.out)
        append_journal(Path(a.journal), {"phase": "INSTALL", "status": "UNKNOWN",
                                         "path": a.path, "resolved": str(target),
                                         "sha256": a.sha, "note": "crash-window fixture"})
        return emit({"verdict": "UNKNOWN_RECORDED", "path": a.path,
                     "resolved": str(target), "sha256": a.sha,
                     "note": "reconcile must read this back, never replay it", "at": now()},
                    a.out, 0)

    return 2


if __name__ == "__main__":
    sys.exit(main())
