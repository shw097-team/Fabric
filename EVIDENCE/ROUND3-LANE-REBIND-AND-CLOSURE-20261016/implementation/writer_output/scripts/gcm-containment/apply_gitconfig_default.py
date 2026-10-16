#!/usr/bin/env python3
"""L1 applier: user-scope gitconfig non-interactive credential default.

Round ``HGK-GCM-CONTAINMENT-20261013``. This tool ADDS one block to the
user-scope gitconfig so the system-scope ``credential.helper = manager`` can no
longer reach a prompt:

    [credential]
    \thelper =
    \thelper = manager --no-ui
    \tinteractive = false

It is fail-closed and append-only. The seven properties below are each
implemented in one identifiable region:

  1. dry-run is the DEFAULT ............... ``--apply`` is required to write
  2. full-digest preimage guard ........... sha256 captured up front; re-checked
                                            immediately before the write; refuse
                                            on any change
  3. per-run timestamped backup ........... ``.bak-<change>-<UTC>`` beside target
  4. post-write verification by EFFECTIVE
     resolution ........................... ``git config --show-origin --get-all
                                            credential.helper`` + a request-level
                                            probe -- never a read-back of written
                                            bytes
  5. receipt JSON ......................... target, scope, before/after sha256,
                                            effective resolution before/after,
                                            exact undo command
  6. ``--rollback`` restores the preimage . byte-identically, prints before/after
                                            sha256
  7. append-only .......................... only ADDS the block; refuses a
                                            conflicting pre-existing helper /
                                            interactive value it did not write

The live user config is NOT written unless the caller passes ``--apply``.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

CHANGE = "gcm-noninteractive-default"
BLOCK = b"[credential]\n\thelper =\n\thelper = manager --no-ui\n\tinteractive = false\n"
EXIT_OK = 0
EXIT_REFUSE = 2
PROBE_TIMEOUT_S = 20


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

def clean_env(overrides: dict | None = None) -> dict:
    """Host environment with every GIT_CONFIG_* override removed, so reads and
    probes reflect the host's REAL effective resolution.

    ``overrides`` is a TEST-ONLY escape hatch used solely by the round's own
    proof harness to point git at a scratch copy of the user config (so the
    apply / rollback / conflict paths can be exercised WITHOUT writing the live
    user file). Production callers pass nothing.
    """
    env = dict(os.environ)
    for k in ("GIT_CONFIG_SYSTEM", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_NOSYSTEM",
              "GIT_CONFIG_COUNT", "GIT_CONFIG_PARAMETERS"):
        env.pop(k, None)
    for k in list(env):
        if k.startswith("GIT_CONFIG_KEY_") or k.startswith("GIT_CONFIG_VALUE_"):
            env.pop(k, None)
    if overrides:
        env.update(overrides)
    return env


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    return sha256_bytes(path.read_bytes())


def git_exe() -> str | None:
    return shutil.which("git")


def utc_stamp() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def default_target() -> Path:
    """Resolve the user-scope gitconfig the same way git does."""
    git = git_exe()
    if git:
        proc = subprocess.run([git, "config", "--global", "--list", "--show-origin"],
                              capture_output=True, text=True, env=clean_env(), timeout=30)
        for line in (proc.stdout or "").splitlines():
            m = re.match(r"^file:(\S+)\t", line)
            if m:
                return Path(m.group(1))
    return Path(os.path.expanduser("~")) / ".gitconfig"


def effective_resolution(git: str | None, overrides: dict | None = None) -> dict:
    """Property 4 / 5 input: the EFFECTIVE helper resolution (not file bytes)."""
    if not git:
        return {"status": "INCONCLUSIVE", "reason": "git executable not found", "entries": []}
    proc = subprocess.run([git, "config", "--show-origin", "--get-all", "credential.helper"],
                          capture_output=True, text=True, env=clean_env(overrides), timeout=30)
    if proc.returncode not in (0, 1):
        return {"status": "INCONCLUSIVE",
                "reason": f"git config exit {proc.returncode}", "entries": [],
                "stderr": proc.stderr}
    entries = []
    for line in (proc.stdout or "").splitlines():
        if "\t" in line:
            origin, value = line.split("\t", 1)
        else:
            origin, value = "", line
        entries.append({"origin": origin, "value": value})
    return {"status": "PASS" if entries else "INCONCLUSIVE",
            "entries": entries,
            "raw": proc.stdout,
            "command": f"{git} config --show-origin --get-all credential.helper"}


def request_probe(git: str | None, overrides: dict | None = None) -> dict:
    """Property 4: a request-level probe against the EFFECTIVE config.

    Runs ``git credential fill`` for a synthetic host under GIT_TERMINAL_PROMPT=0
    (a safety guard on THIS probe, not a change to the config under test) with a
    hard timeout. Records only the typed outcome; never a credential value.
    """
    if not git:
        return {"status": "INCONCLUSIVE", "reason": "git executable not found"}
    env = clean_env(overrides)
    env["GIT_TERMINAL_PROMPT"] = "0"
    req = "protocol=https\nhost=gcm-probe.invalid\n\n"
    noninteractive_markers = (
        "terminal prompts disabled", "unable to get password",
        "interactivity has been disabled", "cannot prompt", "could not read username",
        "could not read password")
    try:
        proc = subprocess.run([git, "credential", "fill"], input=req, capture_output=True,
                              text=True, env=env, timeout=PROBE_TIMEOUT_S)
        err = (proc.stderr or "").strip()
        out = (proc.stdout or "").strip()
        low = err.lower()
        contained = any(m in low for m in noninteractive_markers)
        return {"status": "PASS", "exit": proc.returncode,
                "typed_noninteractive_outcome": contained,
                "stderr_tail": err[-400:], "stdout_present": bool(out),
                "note": ("observed under GIT_TERMINAL_PROMPT=0 as a safety guard on this probe; "
                         "informational, not the acceptance invariant (that is credential_preflight.py)")}
    except subprocess.TimeoutExpired:
        return {"status": "INCONCLUSIVE", "reason": "probe timed out",
                "timeout_seconds": PROBE_TIMEOUT_S}


# --------------------------------------------------------------------------- #
# append-only conflict detection (property 7)
# --------------------------------------------------------------------------- #

def _strip_our_block(text: str) -> str:
    return text.replace(BLOCK.decode("ascii"), "")


def find_conflicting_credential_keys(text: str) -> list[str]:
    """Return credential-section helper/interactive lines that are NOT ours."""
    residual = _strip_our_block(text)
    hits: list[str] = []
    section = ""
    for raw in residual.splitlines():
        header = re.match(r"^\s*\[([^\]]+)\]\s*$", raw)
        if header:
            section = header.group(1).strip().lower()
            continue
        if section.startswith("credential"):
            km = re.match(r"^\s*([A-Za-z0-9_.-]+)\s*=", raw)
            if km and km.group(1).lower() in ("helper", "interactive"):
                hits.append(raw.strip())
    return hits


def append_block(preimage: bytes | None) -> bytes:
    base = preimage or b""
    if base and not base.endswith(b"\n"):
        base = base + b"\n"
    if base and not base.endswith(b"\n\n"):
        # keep the block visually separated but never rewrite existing bytes
        base = base + b"\n"
    return base + BLOCK


# --------------------------------------------------------------------------- #
# commands
# --------------------------------------------------------------------------- #

def build_receipt(target: Path, before_sha: str | None, after_sha: str | None,
                  before_res: dict, after_res: dict, applied: bool,
                  backup: str | None, extra: dict | None = None) -> dict:
    undo = [sys.executable or "python",
            str(Path(__file__).resolve()),
            "--rollback", "--target", str(target)]
    receipt = {
        "schema": "HGK-GCM-CONTAINMENT-APPLIER-RECEIPT/1",
        "round": "HGK-GCM-CONTAINMENT-20261013",
        "change": CHANGE,
        "target": str(target),
        "scope": "user",
        "applied": applied,
        "before_sha256": before_sha if before_sha else "ABSENT",
        "after_sha256": after_sha if after_sha else "ABSENT",
        "backup": backup,
        "effective_resolution_before": before_res,
        "effective_resolution_after": after_res,
        "undo_command": " ".join(undo),
        "block_added": BLOCK.decode("ascii"),
    }
    if extra:
        receipt.update(extra)
    return receipt


def do_apply_or_dry_run(args) -> int:
    target = Path(args.target).resolve() if args.target else default_target().resolve()
    git = git_exe()
    ov = _test_overrides(args)

    # --- property 2: full-digest preimage guard (captured UP FRONT) ----------
    preimage = target.read_bytes() if target.is_file() else None
    before_sha = sha256_bytes(preimage) if preimage is not None else None
    before_res = effective_resolution(git, ov)

    text = preimage.decode("utf-8", "replace") if preimage is not None else ""

    # --- property 7: append-only conflict detection --------------------------
    conflicts = find_conflicting_credential_keys(text)
    if conflicts:
        receipt = build_receipt(target, before_sha, before_sha, before_res, before_res,
                                applied=False, backup=None,
                                extra={"refused": True,
                                       "error_class": "ERR_CONFLICTING_CREDENTIAL_KEY",
                                       "conflicting_lines": conflicts})
        _emit(receipt, args.json)
        return EXIT_REFUSE

    already = BLOCK.decode("ascii") in text
    if already:
        receipt = build_receipt(target, before_sha, before_sha, before_res, before_res,
                                applied=False, backup=None,
                                extra={"idempotent": True, "note": "block already present"})
        _emit(receipt, args.json)
        return EXIT_OK

    new_bytes = append_block(preimage)
    after_sha_predicted = sha256_bytes(new_bytes)

    if not args.apply:
        # --- property 1: dry-run is the default -----------------------------
        receipt = build_receipt(target, before_sha, before_sha, before_res,
                                {"status": "NOT_APPLIED",
                                 "reason": "dry-run: effective resolution after write is not "
                                           "measured without writing (post-write verification "
                                           "reads the EFFECTIVE resolution, never the bytes)"},
                                applied=False, backup=None,
                                extra={"dry_run": True,
                                       "predicted_after_sha256": after_sha_predicted,
                                       "effective_resolution_after": None})
        _emit(receipt, args.json)
        return EXIT_OK

    # --- property 2 (cont.): re-check the guard immediately before writing ---
    current_sha = sha256_file(target)
    exp_arg = getattr(args, "expect_before", "__UNSET__")
    if exp_arg == "__UNSET__":
        expected = before_sha
    elif exp_arg == "ABSENT":
        expected = None
    else:
        expected = exp_arg
    expected_repr = expected if expected is not None else "ABSENT"
    if current_sha != before_sha or current_sha != expected:
        receipt = build_receipt(target, before_sha, current_sha, before_res, before_res,
                                applied=False, backup=None,
                                extra={"refused": True, "error_class": "ERR_PREIMAGE_CHANGED",
                                       "guard_sha256": before_sha or "ABSENT",
                                       "expect_before": expected_repr,
                                       "observed_sha256": current_sha or "ABSENT"})
        _emit(receipt, args.json)
        return EXIT_REFUSE

    # --- property 3: per-run timestamped backup ------------------------------
    backup_path = target.with_name(f"{target.name}.bak-{CHANGE}-{utc_stamp()}")
    backup_meta = backup_path.with_suffix(backup_path.suffix + ".meta.json")
    backup_path.write_bytes(preimage if preimage is not None else b"")
    backup_meta.write_text(json.dumps(
        {"change": CHANGE, "target": str(target), "absent": preimage is None,
         "before_sha256": before_sha or "ABSENT"}, indent=2), encoding="utf-8")

    # --- append-only write ---------------------------------------------------
    with open(target, "ab") as fh:
        fh.write(new_bytes[len(preimage or b""):])

    # --- property 4: verify by EFFECTIVE resolution, plus a request probe ----
    after_res = effective_resolution(git, ov)
    probe = request_probe(git, ov)
    after_sha = sha256_file(target)
    ok = (after_sha == after_sha_predicted
          and any(e["value"].strip() == "" for e in after_res.get("entries", []))
          and any("manager --no-ui" in e["value"] for e in after_res.get("entries", [])))

    receipt = build_receipt(target, before_sha, after_sha, before_res, after_res,
                            applied=True, backup=str(backup_path),
                            extra={"verified_by_effective_resolution": ok,
                                   "request_probe": probe,
                                   "backup_meta": str(backup_meta)})
    _emit(receipt, args.json)
    return EXIT_OK if ok else EXIT_REFUSE


def do_rollback(args) -> int:
    target = Path(args.target).resolve() if args.target else default_target().resolve()
    before_sha = sha256_file(target)
    backups = sorted(target.parent.glob(f"{target.name}.bak-{CHANGE}-*"))
    backups = [b for b in backups if not b.name.endswith(".meta.json")]
    if not backups:
        receipt = {"schema": "HGK-GCM-CONTAINMENT-APPLIER-RECEIPT/1", "change": CHANGE,
                   "rollback": True, "applied": False, "refused": True,
                   "error_class": "ERR_NO_BACKUP", "target": str(target),
                   "before_sha256": before_sha or "ABSENT", "after_sha256": before_sha or "ABSENT",
                   "undo_command": None}
        _emit(receipt, args.json)
        return EXIT_REFUSE

    latest = backups[-1]
    meta = latest.with_suffix(latest.suffix + ".meta.json")
    absent = False
    preimage = latest.read_bytes()
    if meta.is_file():
        try:
            absent = bool(json.loads(meta.read_text(encoding="utf-8")).get("absent"))
        except (ValueError, OSError):
            absent = False

    if absent:
        target.unlink(missing_ok=True)
    else:
        target.write_bytes(preimage)

    # --- property 6: print before/after sha256, byte-identical restore -------
    after_sha = sha256_file(target)
    restored = (after_sha == (None if absent else sha256_bytes(preimage)))
    receipt = {"schema": "HGK-GCM-CONTAINMENT-APPLIER-RECEIPT/1", "change": CHANGE,
               "rollback": True, "applied": True, "target": str(target),
               "scope": "user", "source_backup": str(latest),
               "restored_absent": absent,
               "before_sha256": before_sha or "ABSENT",
               "after_sha256": after_sha or "ABSENT",
               "byte_identical_restore": restored,
               "undo_command": " ".join([sys.executable or "python",
                                         str(Path(__file__).resolve()),
                                         "--rollback", "--target", str(target)])}
    _emit(receipt, args.json)
    return EXIT_OK if restored else EXIT_REFUSE


def _test_overrides(args) -> dict:
    """TEST-ONLY: redirect git's global scope at a scratch copy of the user
    config, so apply / rollback / conflict paths can be proven without writing
    the live user file. Empty for every production invocation."""
    ov: dict = {}
    if getattr(args, "test_global", None):
        ov["GIT_CONFIG_GLOBAL"] = str(Path(args.test_global).resolve()).replace("\\", "/")
    return ov


def _emit(doc: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(doc, indent=2, ensure_ascii=False))
    else:
        print(f"target={doc.get('target')} applied={doc.get('applied')} "
              f"before={doc.get('before_sha256')} after={doc.get('after_sha256')}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="L1 user-gitconfig non-interactive default applier")
    ap.add_argument("--dry-run", action="store_true",
                    help="explicit dry-run (this is also the DEFAULT when --apply is absent)")
    ap.add_argument("--apply", action="store_true", help="actually write the block")
    ap.add_argument("--rollback", action="store_true", help="restore the preimage from the latest backup")
    ap.add_argument("--target", default=None, help="user gitconfig path (default: git's global file)")
    ap.add_argument("--json", action="store_true", help="emit a JSON receipt")
    ap.add_argument("--test-global", default=None, dest="test_global",
                    help="TEST-ONLY: point git's global scope at a scratch file")
    ap.add_argument("--expect-before", default="__UNSET__", dest="expect_before",
                    help="refuse unless the target sha256 equals this value (use ABSENT for a "
                         "missing file); the deterministic preimage-guard trigger")
    args = ap.parse_args(argv)

    if args.apply and args.rollback:
        _emit({"refused": True, "error_class": "ERR_MUTUALLY_EXCLUSIVE"}, args.json)
        return EXIT_REFUSE
    if args.rollback:
        return do_rollback(args)
    if not args.apply and not args.dry_run:
        # property 1: absence of --apply means dry-run, whatever the caller passed
        args.dry_run = True
    return do_apply_or_dry_run(args)


if __name__ == "__main__":
    raise SystemExit(main())
