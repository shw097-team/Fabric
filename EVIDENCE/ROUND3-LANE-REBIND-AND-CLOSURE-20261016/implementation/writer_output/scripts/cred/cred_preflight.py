#!/usr/bin/env python3
"""Fail-closed credential preflight for the PIPD-LS-SP unattended write lane.

Purpose
-------
A long unattended run must not discover at minute 90 that its write credential is
absent, expired or invalid.  This module verifies credential *availability* at
minute 0 and **fails closed**: any check that cannot be confirmed FAILs the run
before it starts.

Security contract (binding -- same as tools/github_publish.py):
  * the secret is read into THIS process only, never printed, never placed in
    argv, stdout, a log, evidence, a prompt, a remote URL or .git/config;
  * only non-sensitive codes and lengths are emitted (PAT_PRESENT, AUTH_VALID ...);
  * ``--metadata-only`` never reads the file at all (existence + byte length only).

Exit codes: 0 = all required checks PASS (WARN/SKIP alone still exit 0);
            2 = one or more required checks FAIL (the run must abort).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Credential sources, in precedence order.  The broker uses the first that works.
PAT_FILE = Path(os.environ.get(
    "HGK_CRED_FILE",
    r"C:\Projects\Agent_Workspace\API KEY\Fine-grained personal access tokens.txt"))

# Optional GitHub App source (the recommended long-term credential -- see the FAR).
APP_ID = os.environ.get("HGK_APP_ID")               # e.g. "1234567"
APP_KEY = os.environ.get("HGK_APP_KEY")             # path to the app .pem (private key)
APP_INSTALLATION_ID = os.environ.get("HGK_APP_INSTALLATION_ID")

# Optional owner-recorded expiry metadata, since GitHub exposes NO API to read a
# fine-grained PAT's own expiry date.  File holds an ISO-8601 date, nothing more.
EXPIRY_FILE = Path(os.environ.get(
    "HGK_CRED_EXPIRY_FILE",
    str(PAT_FILE) + ".expiry"))

API = "https://api.github.com"
TOKEN_RE = re.compile(rb"github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,}")

# The gate must require the validity of the source the broker will ACTUALLY use.
# acquire() selects the App when it is configured and does NOT fall back to the PAT,
# so a dead PAT must not fail a healthy App, and a healthy PAT must not mask a dead App.
REQUIRED_PAT = ("cred_source_present", "cred_syntax", "cred_api_valid")
REQUIRED_APP = ("app_cred_valid",)
REQUIRED = REQUIRED_PAT  # kept for backwards compatibility with external readers


def _result(cid: str, status: str, detail: str) -> dict:
    return {"id": cid, "status": status, "detail": detail}


def _redact(text: str) -> str:
    """Strip any token-shaped or credential-shaped substring from free text."""
    text = re.sub(r"github_pat_[A-Za-z0-9_]{10,}", "<REDACTED>", text)
    text = re.sub(r"gh[pousr]_[A-Za-z0-9]{10,}", "<REDACTED>", text)
    text = re.sub(r"(?i)authorization:\s*basic\s+\S+", "Authorization: Basic <REDACTED>", text)
    return text


def load_pat() -> str | None:
    """Read the PAT into memory.  NEVER called when --metadata-only is set."""
    if not PAT_FILE.is_file():
        return None
    m = TOKEN_RE.search(PAT_FILE.read_bytes())
    return m.group(0).decode("ascii") if m else None


def _api(path: str, token: str):
    req = urllib.request.Request(
        API + path,
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "PIPD-LS-SP-cred-preflight",
                 "X-GitHub-Api-Version": "2022-11-28"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode("utf-8", "replace"))
        except Exception:
            return e.code, {}
    except Exception as e:  # noqa: BLE001 - report, never hide
        return None, {"error": type(e).__name__}


def check_metadata_only() -> list[dict]:
    """No secret is read; existence + byte length only.  Safe on any host."""
    checks = []
    st = PAT_FILE.stat() if PAT_FILE.is_file() else None
    checks.append(_result("cred_source_present",
                          "PASS" if st else "FAIL",
                          f"file present, {st.st_size} bytes" if st else "credential file absent"))
    checks.append(_result("cred_syntax", "SKIP", "metadata-only: content not read"))
    checks.append(_result("cred_api_valid", "SKIP", "metadata-only: not probed"))
    return checks


def run_preflight(probe: bool, app_token_getter=None) -> dict:
    """Fail-closed preflight over the source the broker will actually use.

    ``app_token_getter`` is injected by the broker (which owns the minting code) so
    this module needs no import of it.  When it is absent the App source can only be
    reported as configured-but-unproven, and the gate FAILS CLOSED on it: it does NOT
    quietly fall back to the PAT, because the PAT is not the source the broker would
    use.  Never a silent PASS on an unprobed credential *on the default path*.
    (Two corrections from the R11 independent checker, both measured against the committed
    source: an earlier revision of this docstring said "the gate stays on the PAT", which
    contradicted the code; and this sentence claimed an unconditional guarantee while the
    explicit --no-probe / --metadata-only opt-outs can still yield verdict:"OK" over an
    unproven credential -- those runs are marked "probe_skipped_by_request": true so the two
    kinds of OK are distinguishable rather than silently identical.)
    """
    checks: list[dict] = []
    app_configured = bool(APP_ID and APP_KEY and APP_INSTALLATION_ID and Path(APP_KEY).is_file())

    # 0. What will the broker actually use?  Mirror acquire() exactly.
    effective = "app" if app_configured else "pat"

    # 1. source presence (metadata)
    st = PAT_FILE.stat() if PAT_FILE.is_file() else None
    checks.append(_result("cred_source_present",
                          "PASS" if st else ("SKIP" if effective == "app" else "FAIL"),
                          f"file present, {st.st_size} bytes" if st
                          else "credential file absent"
                               + (f" (not required: effective source is the App)" if effective == "app" else "")))
    if not st and effective == "pat":
        checks.append(_result("cred_syntax", "FAIL", "no source"))
        checks.append(_result("cred_api_valid", "FAIL", "no source"))
        checks.append(_result("app_config_present", "SKIP", "PAT path failed first"))
        checks.append(_result("expiry_known", "FAIL", "no source"))
        return _verdict(checks, REQUIRED_PAT, "pat", unproven_by_request=not probe)

    if not st and effective == "app":
        # The PAT bridge is absent, but it is not the source in force.  Probe the App.
        checks.append(_result("cred_syntax", "SKIP", "no PAT to read; effective source is the App"))
        checks.append(_result("cred_api_valid", "SKIP", "PAT not in force; effective source is the App"))
        checks.append(_result("app_config_present", "PASS", "app id/key/installation configured"))
        checks.extend(_app_probe(probe, app_token_getter))
        checks.append(_expiry_check())
        return _verdict(checks, REQUIRED_APP, "app", unproven_by_request=not probe)

    # 2. syntax (reads the file).  When the App is the effective source the PAT is a
    #    bridge that is NOT in force, so its bytes are still reported but its validity
    #    cannot gate the run.
    token = None if effective == "app" else load_pat()
    _syn = ("cred_syntax",
            "PASS" if token else ("SKIP" if effective == "app" else "FAIL"),
            f"token-shaped & non-empty, length={len(token)}" if token
            else ("PAT bridge not read: the App is the effective source" if effective == "app"
                  else "file holds no github token-shaped string"))
    checks.append(_result(*_syn))
    if effective == "pat" and not token:
        checks.append(_result("cred_api_valid", "FAIL", "unusable source"))
        checks.append(_result("app_config_present", "SKIP", "PAT path failed first"))
        checks.append(_result("expiry_known", "SKIP", "PAT path failed first"))
        return _verdict(checks, REQUIRED_PAT, "pat", unproven_by_request=not probe)

    # 3. App source availability (optional; needs no secret read here)
    app_ok = bool(APP_ID and APP_KEY and APP_INSTALLATION_ID and Path(APP_KEY).is_file())
    checks.append(_result("app_config_present",
                          "PASS" if app_ok else "WARN",
                          "app id/key/installation configured" if app_ok
                          else "not configured (PAT bridge in force)"))

    # 4. validity probe of the EFFECTIVE source only
    if effective == "app":
        checks.append(_result("cred_api_valid",
                              "SKIP",
                              "PAT is NOT the effective source; probing the App instead"))
        checks.extend(_app_probe(probe, app_token_getter))
        required = REQUIRED_APP
    elif probe:
        s, me = _api("/user", token)
        valid = s == 200
        checks.append(_result("cred_api_valid",
                              "PASS" if valid else "FAIL",
                              f"GET /user -> {s}" + (f", login={me.get('login')}" if valid else "")))
        required = REQUIRED_PAT
    else:
        checks.append(_result("cred_api_valid", "SKIP", "--no-probe"))
        required = REQUIRED_PAT

    # 5. expiry knowledge.  GitHub exposes no API to read a PAT's own expiry, so
    #    the only signal is owner-recorded metadata (a date file).
    checks.append(_expiry_check())
    return _verdict(checks, required, effective, unproven_by_request=not probe)


def _expiry_check() -> dict:
    if EXPIRY_FILE.is_file():
        raw = EXPIRY_FILE.read_text(encoding="utf-8", errors="replace").strip()
        return _result("expiry_known", "PASS", f"owner-recorded expiry: {_redact(raw)[:32]}")
    return _result("expiry_known", "WARN",
                   "no owner-recorded expiry; GitHub has no API to read a PAT's own expiry")


def _app_probe(probe: bool, app_token_getter) -> list[dict]:
    """Probe the App source by its OWN installation token - presence is not validity."""
    if not probe:
        return [_result("app_cred_valid", "SKIP", "--no-probe")]
    if app_token_getter is None:
        return [_result("app_cred_valid", "FAIL",
                        "App configured but no probe available (unproven credential); "
                        "the gate refuses to pass on presence alone")]
    try:
        token = app_token_getter()
    except Exception as exc:  # noqa: BLE001 - report, never hide
        return [_result("app_cred_valid", "FAIL", f"installation token mint failed: {type(exc).__name__}")]
    slug = os.environ.get("HGK_REPO_SLUG")
    path = f"/repos/{slug}" if slug else "/installation/repositories"
    status, body = _api(path, token)
    ok = status == 200
    detail = f"GET {path} -> {status}"
    if ok and slug:
        detail += f", repo={body.get('full_name')}, push={bool((body.get('permissions') or {}).get('push'))}"
    return [_result("app_cred_valid", "PASS" if ok else "FAIL", detail)]


def _verdict(checks: list[dict], required=REQUIRED_PAT, effective: str = "pat",
             unproven_by_request: bool = False) -> dict:
    failed = [c["id"] for c in checks
              if c["status"] == "FAIL" and c["id"] in required]
    return {"schema": "PIPD-CRED-PREFLIGHT/1",
            # ADDITIVE (R11).  "verdict": "OK" alone cannot distinguish "the effective source was
            # validity-checked" from "--no-probe/--metadata-only skipped the check", and a reader taking
            # OK for proof is the presence-is-not-validity class this gate exists to stop.
            #
            # MEASURED AND CORRECTED (R11, independent checker): the first version emitted a two-valued
            # label -- "PROBED" / "UNPROVEN_BY_REQUEST" -- and the checker showed "PROBED" claimed more
            # than it knew: the no-source, invalid-PAT, missing-getter and mint-exception paths all
            # returned "PROBED" having made ZERO HTTP calls.  A label must not assert what was not
            # measured, so it is now a BOOLEAN that answers exactly the one question that is known.
            # No existing key changes value.
            "probe_skipped_by_request": unproven_by_request,
            # Which source the broker will actually use.  Reported so this gate can be
            # tested deterministically instead of being inferred from ambient env.
            "effective_source": effective,
            "checks": checks,
            "required": list(required),
            "failed_required": failed,
            "verdict": "FAIL_CLOSED" if failed else "OK",
            "abort": bool(failed)}


def main() -> int:
    ap = argparse.ArgumentParser(description="fail-closed credential preflight")
    ap.add_argument("--metadata-only", action="store_true",
                    help="never read the secret; existence + byte length only")
    ap.add_argument("--no-probe", action="store_true", help="skip the network validity probe")
    args = ap.parse_args()
    if args.metadata_only:
        out = _verdict(check_metadata_only(), unproven_by_request=True)
    else:
        # Bound lazily: cred_broker imports THIS module at module scope, so importing it
        # at module scope here would be a cycle.  Without the getter the App source can
        # only be reported as configured-but-unproven and the gate fails closed on it.
        getter = None
        try:
            import cred_broker  # noqa: PLC0415 - deliberate lazy import
            getter = cred_broker.mint_app_installation_token
        except Exception:  # noqa: BLE001 - the getter is optional; absence is fail-closed
            getter = None
        out = run_preflight(probe=not args.no_probe, app_token_getter=getter)
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 2 if out["abort"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
