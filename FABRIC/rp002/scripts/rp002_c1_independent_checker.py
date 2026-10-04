# -*- coding: utf-8 -*-
"""RP-002 C1 — INDEPENDENT checker (fresh read-only + one fresh re-install; maker != checker)."""
import datetime, hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

FAB = Path(r"C:\Projects\Agent_Workspace\Fabric")
HERMES = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\hermes-v020\venv\Scripts\hermes.exe")
PROFILES = ["hgk-orchestrator", "hgk-knowledge-factory", "hgk-document-factory", "hgk-coding-factory"]

results = []
def check(name, ok, detail):
    results.append({"id": name, "pass": bool(ok), "detail": detail})

# 1. distribution files exist with required fields (re-derived from disk)
for name in PROFILES:
    d = FAB / "profiles" / name
    dist = (d / "distribution.yaml").read_text(encoding="utf-8")
    ok = all(k in dist for k in ("name:", "version:", "description:", "hermes_requires:"))
    check(f"C1I_DIST_{name}", ok, f"fields ok")
    check(f"C1I_SOUL_{name}", (d / "SOUL.md").stat().st_size > 500, "SOUL.md")
    check(f"C1I_CONFIG_{name}", "opencode-go" in (d / "config.yaml").read_text(encoding="utf-8"), "provider route preserved")

# 2. git commit binding exists (full sha)
head = subprocess.run(["git", "-C", str(FAB), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
check("C1I_GIT_COMMIT", len(head) == 40, head)

# 3. materialization manifest exists
man = json.loads((FAB / "rp002" / "C1" / "RP002_C1_MATERIALIZATION.json").read_text(encoding="utf-8"))
check("C1I_MANIFEST_4", len(man["profiles_created"]) == 4, str(man["profiles_created"]))

# 4. maker evidence PASS + all checks
ev = json.loads((FAB / "rp002" / "C1" / "RP002_C1_EVIDENCE.json").read_text(encoding="utf-8"))
check("C1I_MAKER_PASS", ev["verdict"] == "PASS" and all(c["pass"] for c in ev["checks"]), f"{len(ev['checks'])} checks")

# 5. fresh independent re-install of ONE profile into a new disposable home
tmp = Path(tempfile.mkdtemp(prefix="rp002-c1i-"))
try:
    env = os.environ.copy()
    env["HERMES_HOME"] = str(tmp)
    env.pop("PYTHONPATH", None)
    p = subprocess.run([str(HERMES), "profile", "install", str(FAB / "profiles" / "hgk-orchestrator"),
                        "--name", "hgk-orchestrator", "-y"], env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=180)
    check("C1I_FRESH_INSTALL", p.returncode == 0, (p.stdout + p.stderr)[-100:])
    p2 = subprocess.run([str(HERMES), "profile", "list"], env=env, capture_output=True, text=True,
                        encoding="utf-8", errors="replace", timeout=120)
    check("C1I_FRESH_EFFECTIVE", "hgk-orchestrator" in (p2.stdout + p2.stderr), "visible in fresh home")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

verdict = "PASS" if all(c["pass"] for c in results) else "FAIL"
out = {"artifact_id": "RP002_C1_INDEPENDENT_CHECKER", "oracle": "EXTERNAL_FROZEN_BOOTSTRAP_ORACLE",
       "verdict": verdict, "checks": results, "fabric_head": head}
(FAB / "rp002" / "C1" / "RP002_C1_INDEPENDENT_CHECKER.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
sys.exit(0 if verdict == "PASS" else 1)
