#!/usr/bin/env python3
"""Credential broker for the PIPD-LS-SP unattended write lane.

What it does
------------
1. Runs a fail-closed preflight (cred_preflight.py) BEFORE anything else.
2. Obtains a working credential from the first available source:
     * GitHub App installation access token (1-hour TTL) -- the recommended
       source.  Minted locally from a stored App private key via an RS256 JWT
       signed with the system ``openssl`` (no third-party Python dependency).
     * fine-grained PAT -- the bridge source, used only until the App is set up.
3. Runs a git command with the credential injected **only** into the child
   process environment (``http.https://github.com/.extraheader``), so the secret
   never reaches argv, this process's stdout, a log, a remote URL or .git/config.

Security contract (binding):
  * the secret lives only in this process's memory and the child's environment;
  * nothing prints the secret; git's own output is redacted of token-shaped text;
  * ``--dry-run`` proves a credential *would* be supplied without supplying one.

Usage:
    python cred_broker.py preflight
    python cred_broker.py dry-run
    python cred_broker.py run -- push origin main
    python cred_broker.py run -- ls-remote https://github.com/OWNER/REPO.git
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cred_preflight as pf  # noqa: E402

API = "https://api.github.com"
REPO_SLUG = os.environ.get("HGK_REPO_SLUG", "shw097-team/PIPD-LS-SP")
GIT_HOST = "github.com"


# --------------------------------------------------------------------------- #
# credential acquisition
# --------------------------------------------------------------------------- #

def _b64url(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode("ascii")


def mint_app_jwt(app_id: str, key_path: str) -> str:
    """Build a short-lived (<=10 min) RS256 JWT for a GitHub App, signed by openssl.

    The private key is passed to openssl as a FILE PATH (never a value, never in
    stdout); the signing input travels on stdin.  No third-party Python crypto dep.
    """
    now = int(time.time())
    header = _b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    payload = _b64url(json.dumps({"iat": now - 60, "exp": now + 540, "iss": app_id}).encode())
    signing_input = f"{header}.{payload}".encode("ascii")
    sig = subprocess.run(
        ["openssl", "dgst", "-sha256", "-sign", key_path],
        input=signing_input, capture_output=True)
    if sig.returncode != 0:
        raise RuntimeError(f"openssl sign failed: {pf._redact(sig.stderr.decode('utf-8', 'replace'))[:200]}")
    return f"{header}.{payload}.{_b64url(sig.stdout)}"


def mint_app_installation_token() -> str:
    """Exchange an App JWT for a 1-hour installation access token."""
    jwt = mint_app_jwt(pf.APP_ID, pf.APP_KEY)
    body = json.dumps({"repositories": [REPO_SLUG.split("/")[1]]}).encode()
    req = urllib.request.Request(
        f"{API}/app/installations/{pf.APP_INSTALLATION_ID}/access_tokens",
        method="POST", data=body,
        headers={"Authorization": f"Bearer {jwt}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "PIPD-LS-SP-cred-broker",
                 "X-GitHub-Api-Version": "2022-11-28",
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8", "replace"))["token"]
    except urllib.error.HTTPError as e:
        text = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"app token mint HTTP {e.code}: {pf._redact(text)[:200]}") from None


def acquire() -> tuple[str, str]:
    """Return (kind, token).  App first (short-lived), PAT as the bridge."""
    if pf.APP_ID and pf.APP_KEY and pf.APP_INSTALLATION_ID and Path(pf.APP_KEY).is_file():
        return "app", mint_app_installation_token()
    pat = pf.load_pat()
    if pat:
        return "pat", pat
    raise RuntimeError("no usable credential source (app unconfigured, PAT absent/unreadable)")


# --------------------------------------------------------------------------- #
# git execution with the secret confined to the child environment
# --------------------------------------------------------------------------- #

def _child_env(token: str) -> dict:
    basic = base64.b64encode(f"x-access-token:{token}".encode()).decode("ascii")
    return {
        **os.environ,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_COUNT": "1",
        # URL-scoped so it rides ONLY on the github.com Authorization header.
        # NOTE: never pass a command-line `-c <this key>` -- a CLI value would
        # override and clear this header (that was the prior round's silent bug).
        "GIT_CONFIG_KEY_0": f"http.https://{GIT_HOST}/.extraheader",
        "GIT_CONFIG_VALUE_0": f"Authorization: Basic {basic}",
    }


def run_git(git_args: list[str], token: str) -> dict:
    env = _child_env(token)
    # `credential.helper=` on the CLI is safe (it is not the extraheader key).
    proc = subprocess.run(["git", "-c", "credential.helper=", *git_args],
                          capture_output=True, text=True, env=env)
    del env
    err = pf._redact(proc.stderr or "")
    out = pf._redact(proc.stdout or "")
    leaked = bool(re.search(r"github_pat_|gh[pousr]_", err + out))
    return {"exit": proc.returncode, "stdout": out[-2000:], "stderr": err[-2000:],
            "secret_leaked": leaked}


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main() -> int:
    ap = argparse.ArgumentParser(description="credential broker (fail-closed)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("preflight")
    sub.add_parser("dry-run")
    p_run = sub.add_parser("run")
    p_run.add_argument("git_args", nargs=argparse.REMAINDER,
                       help="git arguments, after `--`")
    args = ap.parse_args()

    if args.cmd == "preflight":
        out = pf.run_preflight(probe=True, app_token_getter=mint_app_installation_token)
        print(json.dumps(out, indent=1, ensure_ascii=False))
        return 2 if out["abort"] else 0

    if args.cmd == "dry-run":
        pre = pf.run_preflight(probe=True, app_token_getter=mint_app_installation_token)
        if pre["abort"]:
            print(json.dumps({"verdict": "ABORTED_BY_PREFLIGHT", "preflight": pre},
                             indent=1, ensure_ascii=False))
            return 2
        kind, token = acquire()
        env = _child_env(token)
        # Semantic check on construction, never on a literal that can drift from the built
        # value. A prior version compared against a redaction placeholder, so this field
        # reported False unconditionally while the header was built correctly.
        supplied = (env["GIT_CONFIG_KEY_0"].endswith("/.extraheader")
                    and env["GIT_CONFIG_VALUE_0"].startswith("Authorization: Basic "))
        print(json.dumps({
            "verdict": "OK",
            "preflight": pre["verdict"],
            "credential_kind": kind,
            "credential_length": len(token),
            "header_key": env["GIT_CONFIG_KEY_0"],
            "header_value_redacted": "Authorization: Basic <REDACTED>",
            "header_would_be_supplied": supplied,
            "secret_printed": False}, indent=1, ensure_ascii=False))
        del token, env
        return 0

    # run
    git_args = [a for a in args.git_args if a != "--"]
    pre = pf.run_preflight(probe=True, app_token_getter=mint_app_installation_token)
    if pre["abort"]:
        print(json.dumps({"verdict": "ABORTED_BY_PREFLIGHT", "failed": pre["failed_required"]}))
        return 2
    kind, token = acquire()
    res = run_git(git_args, token)
    del token
    res["verdict"] = "OK" if (res["exit"] == 0 and not res["secret_leaked"]) else "FAIL"
    res["credential_kind"] = kind
    print(json.dumps(res, indent=1, ensure_ascii=False))
    return 0 if res["verdict"] == "OK" else 2


if __name__ == "__main__":
    raise SystemExit(main())
