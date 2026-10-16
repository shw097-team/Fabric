#!/usr/bin/env python3
"""Self-test for the credential broker + preflight.  Uses ONLY dummy credentials.

Proves, without ever touching the real token file's VALUE:
  T1 fail-closed: an absent credential file aborts the preflight (exit 2).
  T2 metadata-only: presence + byte length are reported WITHOUT reading content.
  T3 header construction: the child-env extraheader is URL-scoped and carries
     base64("x-access-token:<dummy>") -- the raw dummy never appears in the value.
  T4 redaction: token-shaped text is stripped from free text.
  T5 end-to-end plumbing: the broker actually transmits the extraheader over the
     wire (a dummy token authenticates differently from anonymous).
"""
from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
os.environ.setdefault("HGK_CRED_FILE", str(HERE / "_nonexistent_cred"))
import cred_preflight as pf  # noqa: E402
import cred_broker as cb    # noqa: E402

DUMMY = "github_pat_" + "A" * 30  # a fake, correctly-shaped token; NOT the real one
results: list[dict] = []


def rec(cid: str, ok: bool, detail: str) -> None:
    results.append({"id": cid, "ok": ok, "detail": detail})


# T1 -- fail closed when NO source is usable.
#
# REALIGNED FIXTURE, same reason as verify_offline.py.  The old form asserted "absent file =>
# abort", which encoded the superseded PAT-only contract (a dead PAT blocked a healthy App).
# The gate now requires the EFFECTIVE source, so this is split and made hermetic: the App
# configuration is CONTROLLED here instead of inherited from the ambient shell.
_amb = {k: os.environ.pop(k, None) for k in ("HGK_APP_ID", "HGK_APP_KEY", "HGK_APP_INSTALLATION_ID")}
_p_orig = {k: getattr(pf, k) for k in ("APP_ID", "APP_KEY", "APP_INSTALLATION_ID")}

os.environ["HGK_CRED_FILE"] = str(HERE / "_absent_cred_file")
pf.PAT_FILE = Path(os.environ["HGK_CRED_FILE"])
pf.APP_ID = pf.APP_KEY = pf.APP_INSTALLATION_ID = None
pre = pf.run_preflight(probe=False)
rec("T1a_fail_closed_no_source", pre["abort"] and pre["verdict"] == "FAIL_CLOSED"
    and pre["effective_source"] == "pat",
    f"verdict={pre['verdict']} source={pre['effective_source']} failed={pre['failed_required']}")

pf.APP_ID, pf.APP_KEY = "1", str(Path(__file__))   # any EXISTING file; key bytes are never read
pf.APP_INSTALLATION_ID = "1"
pre2 = pf.run_preflight(probe=False)
pat_gated = any(c["id"] in pre2["required"] for c in pre2["checks"] if c["id"].startswith("cred_"))
rec("T1b_absent_pat_is_not_the_effective_source",
    (not pre2["abort"]) and pre2["effective_source"] == "app" and not pat_gated,
    f"verdict={pre2['verdict']} source={pre2['effective_source']} pat_checks_required={pat_gated}")

pre3 = pf.run_preflight(probe=True, app_token_getter=None)
rec("T1c_unprobed_app_refuses", pre3["abort"],
    f"verdict={pre3['verdict']} failed={pre3['failed_required']}")

for k, v_ in _p_orig.items():
    setattr(pf, k, v_)
os.environ.pop("HGK_CRED_FILE", None)

# T2 -- metadata-only reports existence+length without reading
with tempfile.TemporaryDirectory() as td:
    f = Path(td) / "cred.txt"
    f.write_text(DUMMY + "\n", encoding="utf-8")
    pf.PAT_FILE = f
    meta = pf._verdict(pf.check_metadata_only())
    present = any(c["id"] == "cred_source_present" and c["status"] == "PASS" for c in meta["checks"])
    skipped = any(c["id"] == "cred_syntax" and c["status"] == "SKIP" for c in meta["checks"])
    rec("T2_metadata_only", present and skipped and meta["verdict"] == "OK",
        "present+size read, syntax SKIP (content untouched)")

    # T3 -- header construction is URL-scoped and base64-wrapped
    env = cb._child_env(DUMMY)
    val = env["GIT_CONFIG_VALUE_0"]
    decoded = base64.b64decode(val.split("Basic ", 1)[1]).decode()
    rec("T3_header_construction",
        env["GIT_CONFIG_KEY_0"] == "http.https://github.com/.extraheader"
        and decoded == f"x-access-token:{DUMMY}"
        and DUMMY not in val,
        f"key URL-scoped; value decodes to x-access-token:<dummy>; raw dummy absent from value")

# T4 -- redaction strips token-shaped text
red = pf._redact(f"failed with {DUMMY} and Authorization: Basic ZGVhZGJlZWY=")
rec("T4_redaction", DUMMY not in red and "Basic <REDACTED>" in red,
    f"redacted -> {red[:60]}")

# T5 -- the broker transmits the extraheader over the wire.  Compare a dummy-token
#       run against an anonymous run of the same public ls-remote.
url = "https://github.com/shw097-team/PIPD-LS-SP.git"
anon = subprocess.run(["git", "ls-remote", url], capture_output=True, text=True)
with_tok = cb.run_git(["-c", "credential.helper=", "ls-remote", url], DUMMY)
rec("T5_wire_plumbing",
    anon.returncode == 0 and with_tok["exit"] != 0 and not with_tok["secret_leaked"],
    f"anonymous exit={anon.returncode}; dummy-token exit={with_tok['exit']} "
    f"(header was transmitted); leaked={with_tok['secret_leaked']}")

ok = all(r["ok"] for r in results)
print(json.dumps({"schema": "PIPD-CRED-SELFTEST/1", "results": results,
                  "passed": sum(r["ok"] for r in results), "total": len(results),
                  "verdict": "PASS" if ok else "FAIL"}, indent=1, ensure_ascii=False))
sys.exit(0 if ok else 2)
