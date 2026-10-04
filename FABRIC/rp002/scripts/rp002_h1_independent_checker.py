# -*- coding: utf-8 -*-
"""RP-002 H1 — INDEPENDENT checker (fresh read-only + one fresh session; maker != checker)."""
import datetime, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
FAB = Path(r"C:\Projects\Agent_Workspace\Fabric")
HERMES = HGK / "var" / "hermes-v020" / "venv" / "Scripts" / "hermes.exe"
HOME = HGK / "var" / "hermes-v020" / "home"
PROFILES = ["hgk-orchestrator", "hgk-knowledge-factory", "hgk-document-factory", "hgk-coding-factory"]

results = []
def check(name, ok, detail):
    results.append({"id": name, "pass": bool(ok), "detail": detail})

# 1. maker evidence PASS
ev = json.loads((FAB / "rp002" / "H1" / "RP002_H1_EVIDENCE.json").read_text(encoding="utf-8"))
check("H1I_MAKER_PASS", ev["verdict"] == "PASS" and all(c["pass"] for c in ev["checks"]), f"{len(ev['checks'])} checks")

# 2. distributions exist in canonical home (re-read from disk)
for name in PROFILES:
    d = HOME / "profiles" / name
    check(f"H1I_DEPLOYED_{name}", (d / "SOUL.md").exists() and (d / "config.yaml").exists() and (d / "distribution.yaml").exists(),
          "SOUL+config+distribution deployed")

# 3. TEAM + Stack manifest exist
check("H1I_HGK_TEAM", (FAB / "HGK" / "TEAM.md").stat().st_size > 800, "HGK/TEAM.md")
check("H1I_STACK_MANIFEST", "hgk-coding-factory" in (FAB / "HGK_STACK_MANIFEST.yaml").read_text(encoding="utf-8"), "Stack manifest")

# 4. named-method router preserved (fresh subprocess)
p = subprocess.run([str(HGK / ".venv" / "Scripts" / "python.exe"), "-c",
                    "import sys; sys.path.insert(0, r'src'); from hg_kseos.named_methods import route, NAMED_METHODS; "
                    "r=route('brownfield x'); print('NM', r['provider'], r['state'], len(NAMED_METHODS))"],
                   cwd=str(HGK), capture_output=True, text=True, timeout=120)
check("H1I_NAMED_METHOD", "NM openspec CERTIFIED_ACTIVE_BROWNFIELD" in p.stdout, p.stdout[:80])

# 5. fresh-session inference under ONE profile (disposable home copy)
tmp = Path(tempfile.mkdtemp(prefix="rp002-h1i-"))
try:
    shutil.copytree(HOME, tmp, ignore=shutil.ignore_patterns("sessions", "logs", "*.db-wal", "*.db-shm", "memories"))
    env = os.environ.copy()
    env["HERMES_HOME"] = str(tmp)
    env.pop("PYTHONPATH", None)
    key = None
    desktop_env = Path(os.environ.get("LOCALAPPDATA", "")) / "hermes" / ".env"
    if desktop_env.exists():
        for line in desktop_env.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip().strip('"')
            if line.startswith("OPENCODE_GO_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"')
                break
    if key:
        env["OPENCODE_GO_API_KEY"] = key
    p = subprocess.run([str(HERMES), "-p", "hgk-document-factory", "-z", "Reply with exactly the single word: OK"],
                       env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=420)
    out = (p.stdout or "") + (p.stderr or "")
    check("H1I_FRESH_SESSION", p.returncode == 0 and "OK" in out, f"rc={p.returncode} {out[-120:]}")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

verdict = "PASS" if all(c["pass"] for c in results) else "FAIL"
out = {"artifact_id": "RP002_H1_INDEPENDENT_CHECKER", "oracle": "EXTERNAL_FROZEN_BOOTSTRAP_ORACLE",
       "verdict": verdict, "checks": results}
(FAB / "rp002" / "H1" / "RP002_H1_INDEPENDENT_CHECKER.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
sys.exit(0 if verdict == "PASS" else 1)
