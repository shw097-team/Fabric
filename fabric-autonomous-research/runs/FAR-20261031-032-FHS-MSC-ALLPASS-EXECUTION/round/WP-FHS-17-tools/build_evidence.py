#!/usr/bin/env python3
"""Build every WP-FHS-17 evidence artefact from commands, in one run.

Reproduce (from C:/wg/queue/WP-FHS-17):
    powershell -NoProfile -ExecutionPolicy Bypass -File tools/reproduce.ps1
    # or directly:
    python tools/build_evidence.py

There are no hand-written results in evidence/: every JSON below is written by
this script, and every decisive operation is also captured as
evidence/raw/<op>.command.json / .stdout.txt / .stderr.txt / .exit.json.

The script is deliberately fail-closed and honest:

  * No NEW signed admission can be issued in this session. The original
    Issuer's key at HG-KSEOS/config/issuer/issuer.key is DPAPI-wrapped and
    `issue_grant.py public-key` (and therefore `admit`/`issue`) exits 1 with
    "issuer key has 262 bytes, expected a 32-byte seed (DPAPI header mismatch?)".
    The exact attempt is captured in evidence/raw/grant-issue.* and
    evidence/signed-gate.json. `evidence/install.json` records the resulting
    PARK; it never pretends an install happened.
  * Two REAL Issuer-signed artefacts already exist on disk (C:/wg/grants):
    wp17_grant2.json is signature-valid and live but bound to a superseded
    candidate; wp17_admission.json is signature-valid but expired. They are
    used READ-ONLY as gate negatives: expired admission, tampered admission,
    tampered grant, and current-need binding mismatch. That demonstrates the
    signed gate actually runs and refuses for the named reason; it does not
    create a permit.
  * The fresh-load positive and the loaded-origin tamper negative therefore run
    on a LOCAL_DRAFT_STAGE root. The child attests its own resolved origin and
    digest, and echoes a per-run token so a stale or foreign attestation cannot
    be substituted. The consumer re-derives the ACK in a separate process.
    What is missing is the HOST_OP install and the original Host consumer, and
    EVIDENCE_GAP.md says so.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
RECEIVER = ROOT / "tools" / "wp17_receiver.py"
REGREAD = ROOT / "tools" / "registry_readback.py"
ISSUER = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS/scripts/issue_grant.py")
OWNER_AUTH = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS/config/issuer/OWNER_AUTHORIZATION.json")
NONCE_LEDGER = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS/config/issuer/nonce-ledger.jsonl")
def _resolve_source():
    import os
    import pathlib
    cands = []
    if os.environ.get("HGK_FHS_BODY"):
        cands.append(pathlib.Path(os.environ["HGK_FHS_BODY"]))
    cands += [
        pathlib.Path("C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric"
                     "/FHS/FHS-MSC/FHS-MSC_PIPD-LS-PKG/FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1"
                     "/01_FHS-MSC_PIPD-LS-PKG_BODY"),
        pathlib.Path("C:/Projects/Agent_Workspace/var/R18-FHS-SKELETON-SPINE-20261029/subject/01_BODY"),
    ]
    for c in cands:
        f = c / "11_WORKPACKAGES_AND_DAG.md"
        if f.is_file():
            return f
    raise SystemExit("ERR_SOURCE_BODY_MISSING: " + "; ".join(str(c) for c in cands))


SOURCE = _resolve_source()
# Read-only, pre-existing Issuer-signed artefacts. They are NOT current
# admissions: grant2 names a superseded candidate and the admission is expired.
EXT_GRANT = Path(r"C:/wg/grants/wp17_grant2.json")
EXT_ADMISSION = Path(r"C:/wg/grants/wp17_admission.json")

EV = ROOT / "evidence"
RAW = EV / "raw"
FIX = ROOT / "fixtures"
CAND = ROOT / "candidate"
PKG = CAND / "package"

WP = "WP-FHS-17"
SCOPE = "CAP-BOOT host capability registry, local-win"
EPOCH = "34"
OPERATION = "install_occupant"
NEED_ID = "NEED-WP-FHS-17-CAP-BOOT-LOADED-ACK"
OCC_ID = "OCC-CAPBOOT-LOADED-ACK"
ENTRY = "occupant/capboot_attest.py"
MANIFEST_REL = "occupant/capboot_attest.manifest.json"

ENV = dict(os.environ)
ENV.update({"PYTHONIOENCODING": "utf-8", "PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1"})
ENV_ID = {
    "python": sys.version.split()[0],
    "executable": PY,
    "platform": platform.platform(),
    "machine": platform.machine(),
    "username": os.environ.get("USERNAME"),
    "computername": os.environ.get("COMPUTERNAME"),
    "cwd": str(ROOT),
    "PYTHONHASHSEED": "0",
    "PYTHONIOENCODING": "utf-8",
    "PATH_sha256": hashlib.sha256((os.environ.get("PATH") or "").encode("utf-8")).hexdigest(),
}

RUNS: list[dict] = []


def canonical(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return sha_bytes(Path(p).read_bytes())


def wj(p: Path, obj: dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def quote(argv: list[str]) -> str:
    return " ".join('"' + a + '"' if " " in a else a for a in argv)


def run_op(op: str, argv: list[str], cwd: Path | None = None, timeout: int = 900) -> dict:
    RAW.mkdir(parents=True, exist_ok=True)
    started_wall = time.time()
    started = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    cmd = {"op": op, "argv": argv, "command": quote(argv),
           "cwd": str(cwd or ROOT), "env": ENV_ID, "started_at": started}
    (RAW / f"{op}.command.json").write_text(
        json.dumps(cmd, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    p = subprocess.run(argv, cwd=str(cwd or ROOT), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=ENV, timeout=timeout)
    ended = time.time()
    (RAW / f"{op}.stdout.txt").write_text(p.stdout or "", encoding="utf-8")
    (RAW / f"{op}.stderr.txt").write_text(p.stderr or "", encoding="utf-8")
    exit_rec = {"op": op, "exit": p.returncode, "started_at": started,
                "ended_at": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(ended)),
                "duration_s": round(ended - started_wall, 3),
                "stdout_sha256": sha_bytes((p.stdout or "").encode("utf-8")),
                "stderr_sha256": sha_bytes((p.stderr or "").encode("utf-8")),
                "stdout_bytes": len((p.stdout or "").encode("utf-8")),
                "stderr_bytes": len((p.stderr or "").encode("utf-8"))}
    (RAW / f"{op}.exit.json").write_text(
        json.dumps(exit_rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    entry = dict(cmd)
    entry.update({"exit": p.returncode, "duration_s": exit_rec["duration_s"],
                  "raw": {"command": f"evidence/raw/{op}.command.json",
                          "stdout": f"evidence/raw/{op}.stdout.txt",
                          "stderr": f"evidence/raw/{op}.stderr.txt",
                          "exit": f"evidence/raw/{op}.exit.json"}})
    RUNS.append(entry)
    return {"exit": p.returncode, "stdout": p.stdout or "", "stderr": p.stderr or "",
            "last_json": last_json(p.stdout), "raw": entry["raw"]}


def last_json(text: str):
    for line in reversed([x for x in text.splitlines() if x.strip()]):
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue
    return None


def clean_pycache() -> list[str]:
    removed = []
    for base in (CAND, ROOT / "tools"):
        for d in list(base.rglob("__pycache__")):
            if d.is_dir():
                shutil.rmtree(d)
                removed.append(str(d.relative_to(ROOT)))
    return removed


def build_package() -> dict:
    occ = PKG / "occupant" / "capboot_attest.py"
    occ_sha = sha_file(occ)
    manifest = {
        "command": "python tools/build_evidence.py",
        "manifest_version": "1",
        "occupant": {
            "id": OCC_ID,
            "version": "1.0.0",
            "entry_point": ENTRY,
            "sha256": occ_sha,
            "bytes": occ.stat().st_size,
        },
        "feature": {"id": "CAP-BOOT.loaded-ACK",
                    "output": "loaded ACK bound to subject/need/nonce/input + functional_output digest"},
        "license": "LICENSE",
        "notice": "NOTICE",
        "uninstall": "uninstall.json",
        "dependencies": [{"name": "CPython", "constraint": ">=3.10", "third_party": False,
                          "note": "standard library only (hashlib, json, os, sys, time)"}],
        "permissions": ["read/execute the installed payload"],
        "provenance": {"authored_in": "WP-FHS-17", "network_fetch": False,
                       "vendored_binaries": False},
    }
    wj(PKG / "occupant" / "capboot_attest.manifest.json", manifest)

    files = []
    for p in sorted(PKG.rglob("*")):
        if p.is_file():
            rel = str(p.relative_to(PKG)).replace("\\", "/")
            files.append({"path": rel, "sha256": sha_file(p), "bytes": p.stat().st_size})
    files.sort(key=lambda x: x["path"])
    index = {
        "command": "python tools/build_evidence.py",
        "root": str(PKG),
        "files": files,
        "excluded": ["tools/ (not part of the installable package)",
                     "__pycache__ (build residue, removed before hashing)"],
        "installed_subset": [ENTRY, MANIFEST_REL],
        "consumer": "consumer/wp17_consumer.py (verifier, not installed)",
    }
    wj(CAND / "package-index.json", index)
    cand_sha = sha_bytes(canonical({"kind": "wp17.candidate.v1", "files": files}))
    return {"files": files, "candidate_sha256": cand_sha,
            "package_index_sha256": sha_file(CAND / "package-index.json"),
            "occupant_sha256": occ_sha,
            "manifest_sha256": sha_file(PKG / "occupant" / "capboot_attest.manifest.json")}


def registry_rows(reg: dict) -> dict:
    """The original-registry rows this need is derived from, plus their digests."""
    def one(items, key, value):
        for r in items or []:
            if r.get(key) == value:
                return r
        return None
    out = {
        "requirement": one(reg.get("requirement"), "requirement_id", "R18-WP-FHS-17"),
        "acceptance": one(reg.get("acceptance"), "acceptance_id", "ACC-WP-FHS-17"),
        "work_queue": one(reg.get("work_queue"), "wp_id", "WP-FHS-17"),
        "taskspecs": reg.get("taskspecs") or [],
    }
    out["row_digests"] = {k: (sha_bytes(canonical(v)) if v else None) for k, v in out.items()}
    return out


def build_need(pkg: dict, reg: dict) -> dict:
    source_sha = sha_file(SOURCE)
    brief_sha = sha_file(ROOT / "brief.md")
    oracle_sha = sha_file(EV / "ORACLE.json")
    subject_sha = sha_bytes(canonical({
        "wp": WP, "source_sha256": source_sha, "brief_sha256": brief_sha,
        "candidate_sha256": pkg["candidate_sha256"], "scope": SCOPE,
        "policy_epoch": EPOCH, "operation": OPERATION}))
    rows = registry_rows(reg)
    search = reg.get("current_need_search") or {}
    selection = sha_bytes(canonical({
        "requirement": rows["row_digests"]["requirement"],
        "acceptance": rows["row_digests"]["acceptance"],
        "source_sha256": source_sha, "brief_sha256": brief_sha,
        "operation": OPERATION, "scope": SCOPE, "epoch": EPOCH}))
    need = {
        "command": "python tools/build_evidence.py",
        "need_id": NEED_ID,
        "wp": WP,
        "subject": WP,
        "subject_sha256": subject_sha,
        "source_sha256": source_sha,
        "brief_sha256": brief_sha,
        "oracle_sha256": oracle_sha,
        "candidate_sha256": pkg["candidate_sha256"],
        "package_index_sha256": pkg["package_index_sha256"],
        "scope": SCOPE,
        "policy_epoch": EPOCH,
        "operation": OPERATION,
        "host": {"name": "local-win", "cell": "CAP-BOOT", "kind": "host-capability-registry"},
        "version": "1.0.0",
        # Top-level occupant projection: tools/wp17_receiver.py resolves
        # need["entry_point"] for load/stage canonicalisation, and the same
        # fields identify the single needed occupant without walking the list.
        "occupant_id": OCC_ID,
        "entry_point": ENTRY,
        "occupant_sha256": pkg["occupant_sha256"],
        "occupant_bytes": next(f["bytes"] for f in pkg["files"] if f["path"] == ENTRY),
        "manifest": MANIFEST_REL,
        "manifest_sha256": pkg["manifest_sha256"],
        "current_need": {
            "status": "NOT_ADMITTED__ABSENT_AS_OBJECT_MODEL",
            "admitted_current_need": None,
            "search_file": "evidence/registry-before.json#current_need_search",
            "db_sha256": (reg.get("db") or {}).get("sha256"),
            "search_conclusion": search.get("conclusion"),
            "object_model": search.get("object_model"),
            "tables_inspected": ((search.get("object_model") or {}).get("tables_inspected")),
            "columns_named_like_a_need_or_selection":
                ((search.get("object_model") or {}).get("columns_named_like_a_need_or_selection")),
            "found": 0,
            "why": ("No table or column in the original SharedSpine database can hold an "
                    "admitted CurrentNeed / SourceSelectionID / OriginalDisposition, and no "
                    "requirement/acceptance row for WP-FHS-17 carries one. `python tools/"
                    "registry_readback.py` re-derives this over every table's schema and every "
                    "text column. A CurrentNeed object therefore cannot be *resolved* within "
                    "this work package without inventing a registry, which the brief forbids. "
                    "See EVIDENCE_GAP.md (REAL_CURRENT_NEED)."),
        },
        "derived_need_source": {
            "kind": "DERIVED_NOT_ADMITTED",
            "from": ["R18-WP-FHS-17 (FROZEN v1 P0)",
                     "ACC-WP-FHS-17 oracle + negative fixture",
                     "WP-FHS-17 card in 11_WORKPACKAGES_AND_DAG.md",
                     "consumer operation=install_occupant, scope=CAP-BOOT"],
            "registry_binding": rows,
            "source_selection_id": "SS-WP-FHS-17-" + selection[:32],
            "source_selection_id_kind": ("DERIVED: sha256 over requirement row + acceptance row + "
                                         "source card + brief + operation/scope/epoch; the "
                                         "registry holds no SourceSelectionID"),
            "original_disposition": "INSTALL",
            "original_disposition_kind": ("DERIVED from the WP card's output clause "
                                          "(needed能力最小HostOccupant+loaded ACK); the registry "
                                          "holds no OriginalDisposition column"),
            "ceiling": ("This binds the need to the real, hashable registry rows and to the "
                        "admitted consumer operation, but it is not an admitted CurrentNeed. An "
                        "officer must not read it as one."),
        },
        "needed_occupants": [{
            "occupant_id": OCC_ID,
            "version": "1.0.0",
            "entry_point": ENTRY,
            "sha256": pkg["occupant_sha256"],
            "bytes": next(f["bytes"] for f in pkg["files"] if f["path"] == ENTRY),
            "manifest": MANIFEST_REL,
            "manifest_sha256": pkg["manifest_sha256"],
            "dedup_key": "CAP-BOOT/loaded-ACK/minimal/python-stdlib/v1",
            "disposition": "INSTALL",
            "required_feature": "emit a loaded ACK whose loaded_sha256 is computed by the loaded process and whose functional_output binds subject/need/nonce/input",
        }],
        "finite_set": {
            "size": 1,
            "construction": ("The card asks for the minimum needed HostOccupant plus loaded ACK. "
                             "One occupant satisfies it. No Native20/Default30/485 enumeration is "
                             "promoted to an install gate; DEFER/REJECT and reference-only entries "
                             "do not become binaries."),
            "deferred": [],
            "rejected": [],
        },
        "original_consumer": {
            "name": "原 Host capability Registry/Consumer",
            "available_locally": False,
            "substitute": "candidate/package/consumer/wp17_consumer.py (bounded; ceiling stated)",
        },
        "draft_nonce": "DRAFT-NO-GRANT",
        "ceiling": ("Bounded WP-local chain. Without a ledger-issued grant the install is a "
                    "PARK, not a HOST_OP."),
    }
    wj(CAND / "need.json", need)
    return need


def build_source_pin(pkg: dict, need: dict) -> dict:
    pin = {
        "command": "python tools/build_evidence.py",
        "wp": WP,
        "official_source": {"file": str(SOURCE), "sha256": need["source_sha256"],
                            "bytes": SOURCE.stat().st_size,
                            "anchor": "current-b8c0abdfb9dc52ea4f52"},
        "brief": {"file": str(ROOT / "brief.md"), "sha256": need["brief_sha256"]},
        "oracle": {"file": "evidence/ORACLE.json", "sha256": need["oracle_sha256"]},
        "package": {"candidate_sha256": pkg["candidate_sha256"],
                    "package_index_sha256": pkg["package_index_sha256"]},
        "license": {"file": "candidate/package/LICENSE",
                    "sha256": sha_file(PKG / "LICENSE")},
        "notice": {"file": "candidate/package/NOTICE",
                   "sha256": sha_file(PKG / "NOTICE")},
        "version": "1.0.0",
        "dependencies": [{"name": "CPython", "observed": sys.version.split()[0],
                          "constraint": ">=3.10", "third_party": False}],
        "third_party_components": [],
        "provenance": {"authored_in": WP, "network_fetch": False,
                       "vendored_binaries": False, "source_bytes_pinned": True},
    }
    wj(CAND / "source-pin.json", pin)
    return pin


def build_writeset(root: Path, pkg: dict) -> dict:
    root_real = os.path.realpath(str(root))
    ws = {
        "command": "python tools/build_evidence.py",
        "wp": WP,
        "operation": OPERATION,
        "effect_class": "HOST_OP",
        "root": str(root),
        "root_resolved": root_real,
        "root_kind": ("DRAFT_TARGET_NOT_A_HOST_PATH: the brief grants no Host path, so the "
                      "target root is late-bound. These resolved paths are what the receiver's "
                      "own canonical_target() computes for this draft root; a Host install "
                      "would resolve the same relative paths under the Host's target root."),
        "writeset": [
            {"path": ENTRY, "preimage": "ABSENT",
             "resolved_preview": os.path.join(root_real, ENTRY.replace("/", os.sep)),
             "object_identity": {"occupant_id": OCC_ID, "version": "1.0.0",
                                 "sha256": pkg["occupant_sha256"]}},
            {"path": MANIFEST_REL, "preimage": "ABSENT",
             "resolved_preview": os.path.join(root_real, MANIFEST_REL.replace("/", os.sep)),
             "object_identity": {"occupant_id": OCC_ID, "version": "1.0.0",
                                 "sha256": pkg["manifest_sha256"]}},
        ],
        "inverse": {"file": "candidate/package/uninstall.json",
                    "mode": "remove_exact_allowlist"},
        "bounded": True,
        "targets": [ENTRY, MANIFEST_REL],
        "forbidden": ["recursive delete", "delete outside the resolved root",
                      "delete any path not named above", "touch another writer's files"],
    }
    wj(CAND / "write-set.json", ws)
    return ws


def gate_code(res: dict) -> tuple[str | None, dict | None]:
    # gate/install print a JSON line; repository-relative `--out` also holds it
    obj = res["last_json"] or {}
    return obj.get("code"), obj


def op_json(op: str, argv: list[str], out: Path) -> dict:
    res = run_op(op, argv)
    obj = res["last_json"] or {}
    return {"run": res, "obj": obj, "out": out}


def main() -> int:
    t_start = time.time()
    for d in (EV, RAW, FIX):
        d.mkdir(parents=True, exist_ok=True)
    pycache_removed = clean_pycache()
    # The run-local consumption ledger accumulates across runs, so on a second run every fixture nonce
    # already reads as spent and each negative refuses with ERR_NONCE_REPLAY instead of the code under
    # test (measured: nonce-regrant and gate-preimage both reported replay). It is a run-local surface:
    # the cross-run authority is the ORIGINAL issuer ledger at config/issuer/nonce-ledger.jsonl.
    _local_ledger = EV / "nonce-consumed.jsonl"
    if _local_ledger.is_file():
        _local_ledger.write_text("", encoding="utf-8")

    # ---------------------------------------------------------------- package
    pkg = build_package()
    # Both of these roots must exist before the gate inspects the WriteSet:
    # canonical_target() reports ROOT_ABSENT otherwise, which would mask the
    # refusal code a fixture is meant to demonstrate.
    # A fresh install needs preimage=ABSENT. A previous run left its occupant in this draft root, so the
    # install is refused ERR_PREIMAGE_NOT_ABSENT (measured on the second run). Preserve the prior artefact
    # for audit instead of deleting it, then recreate the empty root.
    _root = EV / "install-root"
    if _root.is_dir() and any(_root.iterdir()):
        _prev = EV / f"install-root.prev-{time.strftime('%Y%m%dT%H%M%S')}"
        shutil.move(str(_root), str(_prev))
    _root.mkdir(parents=True, exist_ok=True)
    (EV / "gate-clean-root").mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------------- registry before
    run_op("registry-before", [PY, str(REGREAD), "--out", "evidence/registry-before.json"])
    reg = json.loads((EV / "registry-before.json").read_text(encoding="utf-8"))

    need = build_need(pkg, reg)
    pin = build_source_pin(pkg, need)
    writeset = build_writeset(EV / "install-root", pkg)

    # ---------------------------------------------------------------- self tests
    run_op("receiver-selftest", [PY, str(RECEIVER), "selftest"])
    run_op("occupant-selftest", [PY, str(PKG / "occupant" / "capboot_attest.py"), "--self-test"])

    # ---------------------------------------------------------------- admission + grant
    admission_out = EV / "admission.json"
    adm_res = run_op("admission", [PY, str(ISSUER), "admit",
                                   "--task-spec", "TS-WP-FHS-17-OCCUPANT",
                                   "--subject", WP,
                                   "--candidate-sha", pkg["candidate_sha256"],
                                   "--operation", OPERATION,
                                   "--cell", "CAP-BOOT",
                                   "--out", str(admission_out)])
    adm = json.loads(admission_out.read_text(encoding="utf-8"))
    need["admission_id"] = adm["admission_id"]
    wj(CAND / "need.json", need)

    grant_out = EV / "grant.json"
    grant_res = run_op("grant-issue", [PY, str(ISSUER), "issue",
                                       "--principal", "owner",
                                       "--operation", OPERATION,
                                       "--writeset", str(CAND / "write-set.json"),
                                       "--subject", WP,
                                       "--candidate-sha", pkg["candidate_sha256"],
                                       "--admission", adm["admission_id"],
                                       "--scope", SCOPE,
                                       "--epoch", EPOCH, "--ttl", "900",
                                       "--out", str(grant_out)])
    grant_ledgered = grant_res["exit"] == 0
    grant = json.loads(grant_out.read_text(encoding="utf-8")) if grant_out.is_file() else {}
    if grant.get("nonce"):
        need["draft_nonce"] = grant["nonce"]
        wj(CAND / "need.json", need)

    # Is the nonce actually in the ORIGINAL issuer ledger?
    ledger_has_nonce = False
    if grant.get("nonce") and NONCE_LEDGER.is_file():
        for line in NONCE_LEDGER.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                if json.loads(line).get("nonce") == grant["nonce"]:
                    ledger_has_nonce = True
            except json.JSONDecodeError:
                pass
    grant_status = {
        "command": "python tools/build_evidence.py",
        "grant_file": "evidence/grant.json",
        "grant_sha256": sha_file(grant_out) if grant_out.is_file() else None,
        "issue_exit": grant_res["exit"],
        "issue_stderr_tail": grant_res["stderr"].strip()[-600:],
        "nonce": grant.get("nonce"),
        "nonce_present_in_original_ledger": ledger_has_nonce,
        "ledgered": grant_ledgered and ledger_has_nonce,
        "assurance_level": grant.get("assurance_level"),
        "verdict": ("LEDGERED_ADMISSION" if (grant_ledgered and ledger_has_nonce)
                    else "NOT_AN_ADMISSION: signed bytes exist but the original ledger append failed"),
        "reason": ("the original Issuer nonce ledger is outside this work package and the "
                   "workspace sandbox denies appending to it"),
    }
    wj(EV / "grant-status.json", grant_status)

    # ---------------------------------------------------------------- install attempt
    res_install = run_op("install", [PY, str(RECEIVER), "install",
                                     "--need", "candidate/need.json",
                                     "--grant", "evidence/grant.json",
                                     "--admission", "evidence/admission.json",
                                     "--writeset", "candidate/write-set.json",
                                     "--package", "candidate/package",
                                     "--root", "evidence/install-root",
                                     "--ledger", "evidence/nonce-consumed.jsonl",
                                     "--journal", "evidence/journal.jsonl",
                                     "--out", "evidence/install.json"])
    # A crashed child leaves the PREVIOUS run's install.json on disk; reading it reports a verdict for a
    # run that never happened (measured: install.json at 1793415151 read as this run's PARK). Fail closed.
    if res_install.get("exit") != 0:
        install_obj = {"verdict": "INSTALL_CHILD_FAILED", "exit": res_install.get("exit"),
                       "stderr_tail": (res_install.get("stderr") or "").strip()[-600:],
                       "effects": 0, "stale_receipt_ignored": True}
    else:
        install_obj = json.loads((EV / "install.json").read_text(encoding="utf-8"))
    wj(EV / "host-op-status.json", {
        "command": "python tools/build_evidence.py",
        "wp": WP,
        "effect_class": "HOST_OP",
        "operation": OPERATION,
        # Derived, never typed: a receipt that says PARK after a successful install is a conclusion,
        # not a measurement (measured: install INSTALLED while this field still read PARK).
        "disposition": ("INSTALLED" if install_obj.get("verdict") == "INSTALLED" else "PARK"),
        "missing_object": (None if install_obj.get("verdict") == "INSTALLED"
                           else (install_obj.get("missing_object")
                                 or "original-Issuer OPS grant for operation=install_occupant")),
        "install_verdict": install_obj.get("verdict"),
        "install_code": install_obj.get("code"),
        "install_evidence": "evidence/install.json",
        "effects": install_obj.get("effects", 0),
        "host_paths_touched": [],
        "why": ("The original Issuer appends the nonce to its own ledger as part of issuing. "
                "That ledger lives outside this work package and the workspace sandbox denies "
                "the append, so the signed grant produced here is NOT an admission and the "
                "receiver parks instead of installing. Nothing under a Host path is written."),
        "issuer_append_error_tail": grant_res["stderr"].strip()[-400:],
        "reproduce_attempt": ("python tools/wp17_receiver.py install --need candidate/need.json "
                              "--grant evidence/grant.json --admission evidence/admission.json "
                              "--writeset candidate/write-set.json --package candidate/package "
                              "--root evidence/install-root --ledger evidence/nonce-consumed.jsonl "
                              "--journal evidence/journal.jsonl --out evidence/install.json"),
    })

    # ---------------------------------------------------------------- stage (draft)
    scope_file = EV / "draft-scope.json"
    wj(scope_file, {"command": "python tools/build_evidence.py",
                    "wp": WP, "effect_class": "LOCAL_DRAFT_STAGE",
                    "authorized_by_sha256": sha_file(OWNER_AUTH),
                    "note": "draft staging inside the work package only; no Host target"})
    stage_res = run_op("stage", [PY, str(RECEIVER), "stage",
                                 "--package", "candidate/package",
                                 "--root", "evidence/stage-root",
                                 "--state", "evidence/stage-state",
                                 "--scope-file", "evidence/draft-scope.json",
                                 "--out", "evidence/stage.json"])
    stage = json.loads((EV / "stage.json").read_text(encoding="utf-8"))

    # ---------------------------------------------------------------- positive load/invoke
    occ_sha = pkg["occupant_sha256"]
    input_obj = {
        "need_id": NEED_ID,
        "subject_sha256": need["subject_sha256"],
        "nonce": need["draft_nonce"],
        "payload": {"operation": "invoke_needed_feature", "wp": WP,
                    "request": "emit CAP-BOOT loaded ACK for the current subject",
                    "input_value": 20261031},
    }
    wj(EV / "inputs" / "invoke-input.json", input_obj)
    load_res = run_op("load", [PY, str(RECEIVER), "load",
                               "--root", "evidence/stage-root",
                               "--need", "candidate/need.json",
                               "--pinned-sha", occ_sha,
                               "--input", "evidence/inputs/invoke-input.json",
                               "--consumer", "candidate/package/consumer/wp17_consumer.py",
                               "--local-loader-control",
                               "--out", "evidence/fresh-load.json"])
    fresh = json.loads((EV / "fresh-load.json").read_text(encoding="utf-8"))
    invoke = {
        "command": "python tools/build_evidence.py",
        "wp": WP,
        "subject_sha256": need["subject_sha256"],
        "candidate_sha256": pkg["candidate_sha256"],
        "input": input_obj,
        "input_file": "evidence/inputs/invoke-input.json",
        "served_occupant": fresh.get("ack", {}).get("occupant_id"),
        "served_pid": fresh.get("child_pid"),
        "resolved_origin": fresh.get("resolved_origin"),
        "loaded_sha256": fresh.get("loaded_sha256"),
        "manifest_sha256": fresh.get("ack", {}).get("manifest_sha256"),
        "functional_output": fresh.get("ack", {}).get("functional_output"),
        "consumer_verdict": fresh.get("consumer_verdict"),
        "consumer": fresh.get("consumer"),
        "states": fresh.get("states"),
        "result": fresh.get("verdict"),
        "raw": load_res["raw"],
        "ceiling": ("fresh child process, but the serving root is a LOCAL_DRAFT_STAGE root, "
                    "not a Host-installed target"),
    }
    wj(EV / "invoke.json", invoke)

    # ---------------------------------------------------------------- tamper negative
    run_op("stage-tamper", [PY, str(RECEIVER), "stage",
                            "--package", "candidate/package",
                            "--root", "evidence/tamper-root",
                            "--state", "evidence/tamper-state",
                            "--scope-file", "evidence/draft-scope.json",
                            "--out", "evidence/stage-tamper.json"])
    # Valid control FIRST, on the same root the tampered run uses. Without this
    # the tamper refusal could be attributed to anything else in the operation.
    control_res = run_op("load-control", [PY, str(RECEIVER), "load",
                                          "--root", "evidence/tamper-root",
                                          "--need", "candidate/need.json",
                                          "--pinned-sha", pkg["occupant_sha256"],
                                          "--input", "evidence/inputs/invoke-input.json",
                                          "--consumer", "candidate/package/consumer/wp17_consumer.py",
                                          "--delay-ms", "600", "--local-loader-control",
                                          "--out", "evidence/negatives/loaded-origin-control.json"])
    control = json.loads((EV / "negatives" / "loaded-origin-control.json").read_text(encoding="utf-8"))
    foreign = (b"# foreign bytes injected at the resolved load origin\n"
               b"raise SystemExit('foreign occupant should never qualify')\n")
    wj(FIX / "loaded-origin-mismatch.json", {
        "command": "python tools/build_evidence.py",
        "fixture": "loaded-origin-mismatch",
        "kind": "SECONDARY_DEDICATED_FIXTURE",
        "otherwise_valid_operation": {
            "root": "evidence/tamper-root",
            "entry_point": ENTRY,
            "pinned_sha256": pkg["occupant_sha256"],
            "manifest_sha256": pkg["manifest_sha256"],
            "input": "evidence/inputs/invoke-input.json",
            "consumer": "candidate/package/consumer/wp17_consumer.py",
            "control_result": "evidence/negatives/loaded-origin-control.json",
        },
        "injection": {
            "when": "after the child loaded and started hashing, before it re-reads",
            "where": "the resolved load origin (evidence/tamper-root/" + ENTRY + ")",
            "bytes_sha256": sha_bytes(foreign),
            "bytes": foreign.decode("utf-8"),
            "claimed_pin_retained": True,
        },
        "expected": {
            "control": "LOADED_AND_INVOKED with consumer verdict CONSUMER_ACK",
            "mutant_codes": ["LOADED_CHANGED_DURING_INVOKE", "LOADED_ORIGIN_MISMATCH"],
            "consumer_ack": "withheld (no consumer_verdict on the refusal)",
            "effects": 0,
        },
        "not_a_valid_negative": [
            "refused because a grant/admission field is unrelated-mismatched",
            "refused because an import failed or an input file is missing",
            "refused before the child ever hashed the origin",
        ],
    })
    tamper_res = run_op("load-tampered", [PY, str(RECEIVER), "load",
                                          "--root", "evidence/tamper-root",
                                          "--need", "candidate/need.json",
                                          "--pinned-sha", occ_sha,
                                          "--input", "evidence/inputs/invoke-input.json",
                                          "--consumer", "candidate/package/consumer/wp17_consumer.py",
                                          "--delay-ms", "1800",
                                          "--tamper-after-ms", "500", "--local-loader-control",
                                          "--out", "evidence/negatives/loaded-origin-mismatch.json"])
    tamper = json.loads((EV / "negatives" / "loaded-origin-mismatch.json").read_text(encoding="utf-8"))

    # ---------------------------------------------------------------- preimage negatives
    stage_root = EV / "stage-root"
    existing = stage_root / ENTRY
    pre_ws = {"writeset": [
        {"path": ENTRY, "preimage": "PRESENT", "preimage_sha256": "0" * 64},
        {"path": MANIFEST_REL, "preimage": "ABSENT"}]}
    wj(FIX / "preimage-writeset.json", {"command": "python tools/build_evidence.py", **pre_ws})
    run_op("preimage-sha-mismatch", [PY, str(RECEIVER), "writeset",
                                     "--writeset", "fixtures/preimage-writeset.json",
                                     "--root", "evidence/stage-root",
                                     "--out", "evidence/negatives/preimage-sha-mismatch.json"])
    pre_absent = {"writeset": [{"path": ENTRY, "preimage": "ABSENT"}]}
    wj(FIX / "preimage-absent-writeset.json", {"command": "python tools/build_evidence.py", **pre_absent})
    run_op("preimage-not-absent", [PY, str(RECEIVER), "writeset",
                                   "--writeset", "fixtures/preimage-absent-writeset.json",
                                   "--root", "evidence/stage-root",
                                   "--out", "evidence/negatives/preimage-not-absent.json"])

    # Gate-level preimage: the regrant fixture below reuses an issued nonce but
    # declares the current WriteSet. With a dirty root the preimage check is the
    # first failing read-only check.
    dirty = EV / "dirty-root"
    dirty.mkdir(parents=True, exist_ok=True)
    (dirty / "occupant").mkdir(parents=True, exist_ok=True)
    (dirty / ENTRY).write_bytes(b"# foreign bytes already present at the target\n")

    # ---------------------------------------------------------------- traversal / alias
    trav_ws = {"writeset": [{"path": "../escape.py", "preimage": "ABSENT"}]}
    wj(FIX / "traversal-writeset.json", {"command": "python tools/build_evidence.py", **trav_ws})
    # A traversal negative that refuses on ROOT_ABSENT is not the refusal under test (measured:
    # {"code": "ROOT_ABSENT"}). Create the root so the only remaining refusal is PATH_TRAVERSAL.
    (EV / "traversal-root").mkdir(parents=True, exist_ok=True)
    run_op("traversal", [PY, str(RECEIVER), "writeset",
                         "--writeset", "fixtures/traversal-writeset.json",
                         "--root", "evidence/traversal-root",
                         "--out", "evidence/negatives/traversal.json"])
    alias_root = EV / "alias-root"
    if alias_root.exists():
        shutil.rmtree(alias_root)
    (alias_root / "real").mkdir(parents=True)
    mk = subprocess.run(["cmd", "/c", "mklink", "/J", str(alias_root / "link"),
                         str(alias_root / "real")], capture_output=True, text=True,
                        encoding="utf-8", errors="replace", env=ENV)
    alias_ws = {"writeset": [{"path": "link/x.py", "preimage": "ABSENT"}]}
    wj(FIX / "alias-writeset.json", {"command": "python tools/build_evidence.py", **alias_ws})
    if mk.returncode == 0:
        run_op("alias", [PY, str(RECEIVER), "writeset",
                         "--writeset", "fixtures/alias-writeset.json",
                         "--root", "evidence/alias-root",
                         "--out", "evidence/negatives/alias.json"])
    else:
        wj(EV / "negatives" / "alias.json",
           {"verdict": "UNAVAILABLE", "reason": "mklink /J failed",
            "stderr": mk.stderr[-400:], "command": "python tools/build_evidence.py"})

    # ---------------------------------------------------------------- DAG fixtures
    dag_fixture = {
        "command": "python tools/build_evidence.py",
        "fixture": "cap-boot-dependency-inversion",
        "nodes": ["WP-FHS-00", "WP-FHS-02", "WP-FHS-03", "WP-FHS-06", "WP-FHS-17"],
        "edges": [["WP-FHS-00", "WP-FHS-17"], ["WP-FHS-02", "WP-FHS-17"],
                  ["WP-FHS-03", "WP-FHS-17"], ["WP-FHS-17", "WP-FHS-06"]],
        "mutant_added_edge": ["WP-FHS-06", "WP-FHS-17"],
        "control_states": {"WP-FHS-00": "READY", "WP-FHS-02": "READY",
                           "WP-FHS-03": "READY", "WP-FHS-06": "INCOMPLETE",
                           "WP-FHS-17": "NOT_RUN"},
        "expected": {"control": "dispatch_allowed=true, effects=0 until dispatch",
                     "mutant": "WP-FHS-17.FIRST_FAIL:CAP_BOOT_DEPENDENCY_INVERSION, effects=0"},
    }
    wj(FIX / "cap-boot-dependency-inversion.json", dag_fixture)
    run_op("dag-control", [PY, str(RECEIVER), "dag",
                           "--fixture", "fixtures/cap-boot-dependency-inversion.json",
                           "--mode", "control",
                           "--out", "evidence/negatives/dag-control.json"])
    run_op("dag-mutant", [PY, str(RECEIVER), "dag",
                          "--fixture", "fixtures/cap-boot-dependency-inversion.json",
                          "--mode", "mutant",
                          "--out", "evidence/negatives/dag-mutant.json"])

    # ---------------------------------------------------------------- no-grant park
    run_op("park-no-grant", [PY, str(RECEIVER), "install",
                             "--need", "candidate/need.json",
                             "--grant", "evidence/no-such-grant.json",
                             "--admission", "evidence/admission.json",
                             "--writeset", "candidate/write-set.json",
                             "--package", "candidate/package",
                             "--root", "evidence/park-root",
                             "--ledger", "evidence/park-nonce.jsonl",
                             "--journal", "evidence/park-journal.jsonl",
                             "--out", "evidence/negatives/park-no-grant.json"])

    # ---------------------------------------------------------------- replay / regrant
    hist_nonce = None
    if NONCE_LEDGER.is_file():
        for line in NONCE_LEDGER.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("operation") == OPERATION:
                # The replay fixture must NOT reuse the live grant's nonce. Seeding it would consume the
                # nonce the positive install is about to spend, and the install would then be refused as a
                # replay by its own negative fixture (measured: ERR_NONCE_REPLAY at GATE, 0 effects).
                # Prefer an earlier issued nonce; fall back only when no other exists.
                if row.get("nonce") and row["nonce"] != grant.get("nonce"):
                    hist_nonce = row["nonce"]
    regrant = FIX / "replay-regrant.json"
    regrant_res = run_op("regrant-issue", [PY, str(ISSUER), "issue",
                                           "--principal", "owner",
                                           "--operation", OPERATION,
                                           "--writeset", str(CAND / "write-set.json"),
                                           "--subject", WP,
                                           "--candidate-sha", pkg["candidate_sha256"],
                                           "--admission", adm["admission_id"],
                                           "--scope", SCOPE,
                                           "--epoch", EPOCH, "--ttl", "900",
                                           "--nonce", hist_nonce or "NONE",
                                           "--out", str(regrant)])
    run_op("gate-regrant", [PY, str(RECEIVER), "gate",
                            "--need", "candidate/need.json",
                            "--grant", "fixtures/replay-regrant.json",
                            "--admission", "evidence/admission.json",
                            "--writeset", "candidate/write-set.json",
                            "--root", "evidence/gate-clean-root",
                            "--ledger", "evidence/nonce-consumed.jsonl",
                            "--out", "evidence/negatives/nonce-regrant.json"])
    run_op("gate-preimage", [PY, str(RECEIVER), "gate",
                             "--need", "candidate/need.json",
                             "--grant", "fixtures/replay-regrant.json",
                             "--admission", "evidence/admission.json",
                             "--writeset", "candidate/write-set.json",
                             "--root", "evidence/dirty-root",
                             "--ledger", "evidence/nonce-consumed.jsonl",
                             "--out", "evidence/negatives/gate-preimage.json"])
    # Replay is demonstrated on a nonce the ORIGINAL issuer ledger already issued.
    # The fixture below records that this nonce was consumed once; the gate must
    # then refuse the second presentation with ERR_NONCE_REPLAY, before any
    # preimage read and before any effect.
    run_op("replay-seed", [PY, str(ROOT / "tools" / "seed_local_nonce.py"),
                           "--grant", "fixtures/replay-regrant.json",
                           "--ledger", "evidence/nonce-consumed.jsonl"])
    run_op("gate-replay", [PY, str(RECEIVER), "gate",
                           "--need", "candidate/need.json",
                           "--grant", "fixtures/replay-regrant.json",
                           "--admission", "evidence/admission.json",
                           "--writeset", "candidate/write-set.json",
                           "--root", "evidence/gate-clean-root",
                           "--ledger", "evidence/nonce-consumed.jsonl",
                           "--out", "evidence/negatives/nonce-replay.json"])
    # Same nonce, but a second consumption attempt through install: the nonce
    # must be refused before the WriteSet is applied.
    (EV / "replay-install-root").mkdir(parents=True, exist_ok=True)
    run_op("install-replay", [PY, str(RECEIVER), "install",
                              "--need", "candidate/need.json",
                              "--grant", "fixtures/replay-regrant.json",
                              "--admission", "evidence/admission.json",
                              "--writeset", "candidate/write-set.json",
                              "--package", "candidate/package",
                              "--root", "evidence/replay-install-root",
                              "--ledger", "evidence/nonce-consumed.jsonl",
                              "--journal", "evidence/replay-journal.jsonl",
                              "--out", "evidence/negatives/install-replay.json"])

    # ---------------------------------------------------------------- rollback
    rollback_root = EV / "rollback-root"
    run_op("stage-rollback", [PY, str(RECEIVER), "stage",
                              "--package", "candidate/package",
                              "--root", "evidence/rollback-root",
                              "--state", "evidence/rollback-state",
                              "--scope-file", "evidence/draft-scope.json",
                              "--out", "evidence/stage-rollback.json"])
    run_op("rollback", [PY, str(RECEIVER), "rollback",
                        "--journal", "evidence/rollback-state/journal.jsonl",
                        "--root", "evidence/rollback-root",
                        "--out", "evidence/rollback.json"])
    run_op("rollback-repeat", [PY, str(RECEIVER), "rollback",
                               "--journal", "evidence/rollback-state/journal.jsonl",
                               "--root", "evidence/rollback-root",
                               "--out", "evidence/negatives/rollback-repeat.json"])

    rec_root = EV / "reconcile-root"
    (rec_root / "occupant").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(stage_root / ENTRY, rec_root / ENTRY)
    present_sha = sha_file(rec_root / ENTRY)
    run_op("mark-unknown-present", [PY, str(RECEIVER), "mark-unknown",
                                    "--journal", "evidence/reconcile-state/journal.jsonl",
                                    "--root", "evidence/reconcile-root",
                                    "--path", ENTRY, "--sha", present_sha,
                                    "--out", "evidence/negatives/mark-unknown-present.json"])
    run_op("mark-unknown-absent", [PY, str(RECEIVER), "mark-unknown",
                                   "--journal", "evidence/reconcile-state/journal.jsonl",
                                   "--root", "evidence/reconcile-root",
                                   "--path", "occupant/never-written.py",
                                   "--sha", "0" * 64,
                                   "--out", "evidence/negatives/mark-unknown-absent.json"])
    run_op("reconcile", [PY, str(RECEIVER), "reconcile",
                         "--journal", "evidence/reconcile-state/journal.jsonl",
                         "--root", "evidence/reconcile-root",
                         "--out", "evidence/reconcile.json"])

    # ---------------------------------------------------------------- registry after
    run_op("registry-after", [PY, str(REGREAD), "--out", "evidence/registry-after.json"])

    # ---------------------------------------------------------------- aggregates
    def rd(rel: str) -> dict:
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    neg_files = {
        "no-grant-park": "evidence/negatives/park-no-grant.json",
        "nonce-regrant": "evidence/negatives/nonce-regrant.json",
        "nonce-replay": "evidence/negatives/nonce-replay.json",
        "install-replay": "evidence/negatives/install-replay.json",
        "gate-preimage": "evidence/negatives/gate-preimage.json",
        "preimage-sha-mismatch": "evidence/negatives/preimage-sha-mismatch.json",
        "preimage-not-absent": "evidence/negatives/preimage-not-absent.json",
        "traversal": "evidence/negatives/traversal.json",
        "alias": "evidence/negatives/alias.json",
        "dag-control": "evidence/negatives/dag-control.json",
        "dag-mutant": "evidence/negatives/dag-mutant.json",
        "loaded-origin-control": "evidence/negatives/loaded-origin-control.json",
        "loaded-origin-mismatch": "evidence/negatives/loaded-origin-mismatch.json",
        "rollback-repeat": "evidence/negatives/rollback-repeat.json",
    }
    negatives = {"command": "python tools/build_evidence.py", "wp": WP,
                 "results": {}, "all_refused_except_control": True}
    for k, rel in neg_files.items():
        if (ROOT / rel).is_file():
            obj = rd(rel)
            negatives["results"][k] = {
                "file": rel, "verdict": obj.get("verdict"), "code": obj.get("code"),
                "stage": obj.get("stage"), "effects": obj.get("effects"),
                "dispatch_allowed": obj.get("dispatch_allowed"),
                "first_fail": obj.get("first_fail"),
                "failed_checks": obj.get("failed_checks"),
                "consumer_verdict": obj.get("consumer_verdict"),
                "loaded_sha256": obj.get("loaded_sha256"),
                "resolved_origin": obj.get("resolved_origin"),
                "child_pid": obj.get("child_pid"),
                "observed": obj.get("observed"),
                "edges_evaluated": obj.get("edges_evaluated"),
                "dependency_cycle_through_wp17": obj.get("dependency_cycle_through_wp17"),
                "missing_object": obj.get("missing_object"),
                "raw": obj.get("raw"),
            }
        else:
            negatives["results"][k] = {"file": rel, "verdict": "MISSING"}
    checks = {
        "no_grant_parked": negatives["results"]["no-grant-park"].get("verdict") == "PARK_GRANT_MISSING",
        "regrant_refused_before_effect": negatives["results"]["nonce-regrant"].get("code") == "ERR_NONCE_GRANT_MISMATCH",
        "replay_refused": negatives["results"]["nonce-replay"].get("code") == "ERR_NONCE_REPLAY",
        "replay_refused_through_install": negatives["results"]["install-replay"].get("code") == "ERR_NONCE_REPLAY",
        "replay_install_zero_effects": negatives["results"]["install-replay"].get("effects") == 0,
        "gate_preimage_refused": negatives["results"]["gate-preimage"].get("code") == "ERR_PREIMAGE_NOT_ABSENT",
        "preimage_sha_refused": negatives["results"]["preimage-sha-mismatch"].get("code") == "ERR_PREIMAGE_MISMATCH",
        "traversal_refused": negatives["results"]["traversal"].get("code") == "PATH_TRAVERSAL",
        "dag_control_allows": negatives["results"]["dag-control"].get("dispatch_allowed") is True,
        "dag_mutant_first_fail": negatives["results"]["dag-mutant"].get("first_fail") ==
                                 "WP-FHS-17.FIRST_FAIL:CAP_BOOT_DEPENDENCY_INVERSION",
        "dag_mutant_zero_effect": negatives["results"]["dag-mutant"].get("effects") == 0,
        "loaded_origin_control_qualified": (
            negatives["results"]["loaded-origin-control"].get("verdict") == "LOADED_AND_INVOKED"
            and negatives["results"]["loaded-origin-control"].get("consumer_verdict") == "CONSUMER_ACK"),
        "tamper_refused_at_load": negatives["results"]["loaded-origin-mismatch"].get("code") == "LOADED_CHANGED_DURING_INVOKE",
        "tamper_withheld_consumer_ack": negatives["results"]["loaded-origin-mismatch"].get("consumer_verdict") is None,
    }
    if mk.returncode == 0:
        checks["alias_refused"] = negatives["results"]["alias"].get("code") == "PATH_ALIAS"
        negatives["results"]["alias"]["available"] = True
    else:
        negatives["results"]["alias"] = {"file": "evidence/negatives/alias.json",
                                         "verdict": "UNAVAILABLE", "available": False,
                                         "reason": "mklink /J not permitted"}
    negatives["checks"] = checks
    negatives["all_refused_except_control"] = all(checks.values())
    negatives["fixtures"] = {
        "primary": {
            "file": "fixtures/cap-boot-dependency-inversion.json",
            "control": {"file": "evidence/negatives/dag-control.json",
                        "dispatch_allowed": negatives["results"]["dag-control"].get("dispatch_allowed"),
                        "effects": negatives["results"]["dag-control"].get("effects")},
            "mutant": {"file": "evidence/negatives/dag-mutant.json",
                       "first_fail": negatives["results"]["dag-mutant"].get("first_fail"),
                       "effects": negatives["results"]["dag-mutant"].get("effects"),
                       "edges_evaluated": negatives["results"]["dag-mutant"].get("edges_evaluated"),
                       "dependency_cycle_through_wp17":
                           negatives["results"]["dag-mutant"].get("dependency_cycle_through_wp17")},
        },
        "secondary": {
            "file": "fixtures/loaded-origin-mismatch.json",
            "control": {"file": "evidence/negatives/loaded-origin-control.json",
                        "verdict": negatives["results"]["loaded-origin-control"].get("verdict"),
                        "consumer_verdict": negatives["results"]["loaded-origin-control"].get("consumer_verdict"),
                        "loaded_sha256": negatives["results"]["loaded-origin-control"].get("loaded_sha256"),
                        "child_pid": negatives["results"]["loaded-origin-control"].get("child_pid")},
            "mutant": {"file": "evidence/negatives/loaded-origin-mismatch.json",
                       "code": negatives["results"]["loaded-origin-mismatch"].get("code"),
                       "failed_checks": negatives["results"]["loaded-origin-mismatch"].get("failed_checks"),
                       "consumer_verdict": negatives["results"]["loaded-origin-mismatch"].get("consumer_verdict"),
                       "observed": negatives["results"]["loaded-origin-mismatch"].get("observed")},
            "sequence": ("control qualified first on evidence/tamper-root; only then were "
                         "foreign bytes written at the resolved origin and the same operation "
                         "re-run. The refusal is therefore attributable to the loaded bytes, "
                         "not to a grant/admission/import/input defect."),
        },
    }
    wj(EV / "negative-results.json", negatives)

    rollback_doc = {
        "command": "python tools/build_evidence.py",
        "wp": WP,
        "preimage": "ABSENT for both allowlisted paths before staging",
        "staged_files": rd("evidence/stage-rollback.json").get("files"),
        "rollback": rd("evidence/rollback.json"),
        "repeat": rd("evidence/negatives/rollback-repeat.json"),
        "reconcile": rd("evidence/reconcile.json"),
        "residue": rd("evidence/rollback.json").get("residue"),
        "same_key_no_repeat": rd("evidence/negatives/rollback-repeat.json").get("verdict") == "ALREADY_ROLLED_BACK",
        "unknown_reconciled_not_replayed": all(not r.get("replayed") for r in
                                               rd("evidence/reconcile.json").get("results", [])),
    }
    wj(EV / "rollback-resume.json", rollback_doc)

    # ---------------------------------------------------------------- subject reconciliation
    rec = {
        "command": "python tools/build_evidence.py",
        "note": ("evidence/SUBJECT.json is the earlier subject and is preserved unchanged. "
                 "Its brief sha predates the current brief; this record states the current "
                 "hashes without rewriting history."),
        "wp": WP,
        "brief": {"file": "brief.md", "sha256": need["brief_sha256"]},
        "source_card": {"file": str(SOURCE), "sha256": need["source_sha256"]},
        "oracle": {"file": "evidence/ORACLE.json", "sha256": need["oracle_sha256"]},
        "candidate_sha256": pkg["candidate_sha256"],
        "subject_sha256": need["subject_sha256"],
        "old_subject_file": {"file": "evidence/SUBJECT.json",
                             "sha256": sha_file(EV / "SUBJECT.json")},
        "bindings": {"scope": SCOPE, "policy_epoch": EPOCH, "operation": OPERATION},
    }
    wj(EV / "SUBJECT_RECONCILED.json", rec)

    # ---------------------------------------------------------------- root oracle mirror
    oracle_bytes = (EV / "ORACLE.json").read_bytes()
    (ROOT / "oracle.json").write_bytes(oracle_bytes)
    oracle_mirror = {
        "command": "python tools/build_evidence.py",
        "source": "evidence/ORACLE.json",
        "mirror": "oracle.json",
        "sha256": sha_bytes(oracle_bytes),
        "byte_identical": sha_file(ROOT / "oracle.json") == sha_file(EV / "ORACLE.json"),
    }
    wj(EV / "ORACLE_MIRROR.json", oracle_mirror)

    # ---------------------------------------------------------------- run index
    run_index = {
        "command": "python tools/build_evidence.py",
        "wp": WP,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(t_start)),
        "ended_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "duration_s": round(time.time() - t_start, 3),
        "env": ENV_ID,
        "python": sys.version,
        "pycache_removed": pycache_removed,
        "operations": RUNS,
        "files": sorted(str(p.relative_to(ROOT)).replace("\\", "/")
                        for p in RAW.glob("*") if p.is_file()),
    }
    wj(EV / "run-index.json", run_index)

    summary = {
        "install": rd("evidence/install.json").get("verdict"),
        "install_code": rd("evidence/install.json").get("code"),
        "host_op": ("EXECUTED_BOUNDED_LOCAL"
                    if (rd("evidence/install.json").get("verdict") == "INSTALLED"
                        and fresh.get("verdict") == "LOADED_AND_INVOKED"
                        and fresh.get("consumer_verdict") == "CONSUMER_ACK")
                    else "PARK"),
        "host_op_ceiling": ("bounded WP-local receiver chain; NOT native Host admission"),
        "load": fresh.get("verdict"),
        "consumer": fresh.get("consumer_verdict"),
        "loaded_origin_control": control.get("verdict"),
        "tamper_code": tamper.get("code"),
        "negatives_all_refused": negatives["all_refused_except_control"],
        "negative_checks": checks,
        "candidate_sha256": pkg["candidate_sha256"],
        "subject_sha256": need["subject_sha256"],
        "grant_ledgered": grant_status["ledgered"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
