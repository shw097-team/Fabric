#!/usr/bin/env python3
"""Offline install-verification for the HG-KSEOS credential broker.

Runs the network-free subset of `selftest.py` against the INSTALLED copy, so a
host with `network_default: DENY` (config/project.json) can still prove the
install is intact and the security contract holds, WITHOUT reading the real
credential value and WITHOUT any network call.

  T1 fail-closed        : an absent credential file aborts the preflight (exit 2).
  T2 metadata-only      : presence + byte length reported with content NOT read.
  T3 header construction: the child-env extraheader is URL-scoped and base64-wrapped
                          with the raw token absent from the value.
  T4 redaction          : token-shaped text is stripped from free text.
  T5 wire plumbing      : SKIPPED here (needs network) -> reported INCONCLUSIVE,
                          never as PASS. Run `selftest.py` on a network-enabled
                          host to obtain T5.

Only DUMMY, correctly-shaped tokens are used. The real credential file is never
opened; cred_preflight.PAT_FILE is rebound to synthetic paths before any call.
"""
from __future__ import annotations

import base64
import json
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
os.environ["HGK_CRED_FILE"] = str(HERE / "_verify_nonexistent")
import cred_preflight as pf  # noqa: E402
import cred_broker as cb    # noqa: E402

DUMMY = "github_pat_" + "A" * 30  # fake, correctly-shaped; NOT the real token
results: list[dict] = []


def rec(cid: str, status: str, detail: str) -> None:
    results.append({"id": cid, "status": status, "detail": detail})


# T1 -- fail closed when NO source is usable (no read, no network).
#
# REALIGNED FIXTURE.  The earlier form asserted "no PAT file => abort", which encoded the
# superseded PAT-only contract: the gate used to require the PAT unconditionally, so a dead
# or absent PAT blocked a fully configured App.  That was the defect fixed in this round.
# The contract is now "the gate requires the EFFECTIVE source", so this fixture is split and
# made deterministic -- the App configuration is CONTROLLED here rather than inherited from
# whatever HGK_APP_* the ambient shell happens to export, which made the old result depend on
# the environment rather than on the code.
_amb = {k: os.environ.pop(k, None) for k in ("HGK_APP_ID", "HGK_APP_KEY", "HGK_APP_INSTALLATION_ID")}
p_orig = {k: getattr(pf, k) for k in ("APP_ID", "APP_KEY", "APP_INSTALLATION_ID")}

pf.PAT_FILE = Path(HERE / "_verify_nonexistent")
pf.APP_ID = pf.APP_KEY = pf.APP_INSTALLATION_ID = None          # no source at all
pre = pf.run_preflight(probe=False)
rec("T1a_fail_closed_no_source",
    "PASS" if (pre["abort"] and pre["verdict"] == "FAIL_CLOSED"
               and pre["effective_source"] == "pat") else "FAIL",
    f"verdict={pre['verdict']} source={pre['effective_source']} failed={pre['failed_required']}")

pf.PAT_FILE = Path(HERE / "_verify_nonexistent")
# Any EXISTING file stands in for the key: the gate checks Path.is_file(), never the key bytes.
pf.APP_ID, pf.APP_KEY = "1", str(Path(__file__))
pf.APP_INSTALLATION_ID = "1"
pre2 = pf.run_preflight(probe=False)
pat_gated = any(c["id"] in pre2["required"] for c in pre2["checks"] if c["id"].startswith("cred_"))
rec("T1b_absent_pat_is_not_the_effective_source",
    "PASS" if (not pre2["abort"] and pre2["effective_source"] == "app" and not pat_gated) else "FAIL",
    f"verdict={pre2['verdict']} source={pre2['effective_source']} pat_checks_required={pat_gated}")

# a configured-but-UNPROBED App must never pass (presence is not validity)
pre3 = pf.run_preflight(probe=True, app_token_getter=None)
rec("T1c_unprobed_app_refuses",
    "PASS" if pre3["abort"] else "FAIL",
    f"verdict={pre3['verdict']} failed={pre3['failed_required']}")

for k, val in p_orig.items():
    setattr(pf, k, val)
for k, val in _amb.items():
    if val is not None:
        os.environ[k] = val

# T2 -- metadata-only reports existence+length without reading content
with tempfile.TemporaryDirectory() as td:
    f = Path(td) / "cred.txt"
    f.write_text(DUMMY + "\n", encoding="utf-8")
    pf.PAT_FILE = f
    meta = pf._verdict(pf.check_metadata_only())
    present = any(c["id"] == "cred_source_present" and c["status"] == "PASS" for c in meta["checks"])
    skipped = any(c["id"] == "cred_syntax" and c["status"] == "SKIP" for c in meta["checks"])
    rec("T2_metadata_only", "PASS" if (present and skipped and meta["verdict"] == "OK") else "FAIL",
        "present+size read, syntax SKIP (content untouched)")

    # T3 -- header construction is URL-scoped and base64-wrapped
    env = cb._child_env(DUMMY)
    val = env["GIT_CONFIG_VALUE_0"]
    decoded = base64.b64decode(val.split("Basic ", 1)[1]).decode()
    rec("T3_header_construction",
        "PASS" if (env["GIT_CONFIG_KEY_0"] == "http.https://github.com/.extraheader"
                   and decoded == f"x-access-token:{DUMMY}"
                   and DUMMY not in val) else "FAIL",
        "key URL-scoped; value decodes to x-access-token:<token>; raw token absent from value")

# T4 -- redaction strips token-shaped text
red = pf._redact(f"failed with {DUMMY} and Authorization: Basic {base64.b64encode(b'x').decode()}")
rec("T4_redaction", "PASS" if (DUMMY not in red) else "FAIL", f"redacted -> {red[:60]}")

# T5 -- network-dependent; never claim PASS offline
rec("T5_wire_plumbing", "SKIP", "network call; INCONCLUSIVE offline -- run selftest.py on a networked host")

pf.PAT_FILE = Path(HERE / "_verify_nonexistent")
failed = [r for r in results if r["status"] == "FAIL"]
verdict = "FAIL" if failed else ("PASS" if all(r["status"] == "PASS" for r in results) else "PASS_OFFLINE_T5_UNPROVEN")
print(json.dumps({"schema": "HGK-CRED-VERIFY-OFFLINE/1", "results": results,
                  "verdict": verdict}, indent=1, ensure_ascii=False))
sys.exit(2 if failed else 0)
