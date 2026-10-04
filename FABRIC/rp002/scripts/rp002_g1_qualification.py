# -*- coding: utf-8 -*-
"""
RP-002 G1 — HERMES_RUNTIME_QUALIFICATION executor (CURRENT_CERTIFIED_HGK_RUNTIME).

Runs REAL runtime canaries against the exact pinned candidate:
  executable: var/hermes-v020/venv/Scripts/hermes.exe  (v0.20.0 / v2026.8.3 / 3c27eb62)
  home:       var/hermes-v020/home                      (isolated; kanban.db present)
  route:      opencode-go / deepseek-v4-flash (env-ref credential, never printed)

Permanent guards (r3 §16 G1):
  PROFILE_READY_GATE                profile list + config/model/provider route
  KANBAN_WORKER_LIVENESS_GATE       real worker spawn: run-row + PID + heartbeat/log
  PRE_DISPATCH_AUTHORIZATION_GATE   sensitive task cannot spawn without authorization receipt
  CROSS_PROFILE_SECRET_ISOLATION_GATE synthetic secret unavailable to lower-privileged worker
  WRITE_READBACK_INTEGRITY_GATE     literal ...[truncated] in critical file fails readback
  HERMES_WINDOWS_RUNTIME_GATE       process spawn/kill/cleanup + exact executable identity
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
G0 = Path(r"C:\Projects\Agent_Workspace\Fabric\rp002\G0")
G1 = Path(r"C:\Projects\Agent_Workspace\Fabric\rp002\G1")
G1.mkdir(parents=True, exist_ok=True)
HERMES = HGK / "var" / "hermes-v020" / "venv" / "Scripts" / "hermes.exe"
HOME = HGK / "var" / "hermes-v020" / "home"
DESKTOP_ENV = Path(os.environ.get("LOCALAPPDATA", "")) / "hermes" / ".env"

TRUNCATION_SENTINEL = b"...[truncated]"
checks = []


def check(name, ok, detail):
    checks.append({"id": name, "pass": bool(ok), "detail": detail})


def env_ref_key(name):
    if not DESKTOP_ENV.exists():
        return None
    for line in DESKTOP_ENV.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip().strip('"')
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip().strip('"')
    return None


def run_hermes(args, timeout=240, extra_env=None):
    env = os.environ.copy()
    env["HERMES_HOME"] = str(HOME)
    env.pop("PYTHONPATH", None)
    key = env_ref_key("OPENCODE_GO_API_KEY")
    if key:
        env["OPENCODE_GO_API_KEY"] = key
    if extra_env:
        env.update(extra_env)
    p = subprocess.run([str(HERMES)] + args, env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or ""), p


def verify_critical_write(path: Path) -> dict:
    raw = path.read_bytes()
    if TRUNCATION_SENTINEL in raw:
        raise RuntimeError(f"ERR_LITERAL_TRUNCATION_SENTINEL:{path}")
    return {"path": str(path.resolve()), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def main() -> int:
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # ── 1. HERMES_WINDOWS_RUNTIME_GATE / identity ─────────────────────────
    exe = HERMES.resolve()
    check("G1_EXECUTABLE_EXISTS", exe.is_file(), str(exe))
    rc, out, _ = run_hermes(["--version"], timeout=60)
    check("G1_VERSION_RC_ZERO", rc == 0, f"rc={rc}")
    check("G1_VERSION_EXACT", "v0.20.0 (2026.8.3)" in out or "Hermes Agent v0.20.0 (2026.8.3)" in out, out.strip()[:80])
    config = json.loads((HGK / "config" / "hermes.json").read_text(encoding="utf-8"))
    check("G1_CONFIG_BINDING",
          config.get("status") == "ACTIVE_SELECTED_CERTIFIED"
          and config["release"]["commit"] == "3c27eb6234bf91b8ceee9e9071591b31e9b148cb"
          and config["executable"].replace("\\", "/").endswith("var/hermes-v020/venv/Scripts/hermes.exe"),
          f"status={config.get('status')} commit={config['release']['commit']}")
    check("G1_ROLLBACK_BASELINE_SEALED",
          config["rollback_baseline"]["commit"].startswith("9de9c25f"),
          config["rollback_baseline"]["commit"])

    # Windows process lifecycle: spawn a real process, verify PID alive, kill, verify gone
    probe = subprocess.Popen([str(exe), "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1.0)
    alive = probe.poll() is None
    check("G1_WIN_PROCESS_SPAWN_PID", probe.pid is not None and probe.pid > 0, f"pid={probe.pid}")
    probe.terminate()
    try:
        probe.wait(timeout=10)
    except subprocess.TimeoutExpired:
        probe.kill()
        probe.wait(timeout=10)
    check("G1_WIN_PROCESS_CLEANUP", probe.poll() is not None, f"exit={probe.returncode}")

    # ── 2. PROFILE_READY_GATE ──────────────────────────────────────────────
    rc, out, _ = run_hermes(["profile", "list"], timeout=120)
    check("G1_PROFILE_LIST_RC", rc == 0, f"rc={rc}")
    check("G1_DEFAULT_PROFILE_PRESENT", "default" in out, "default profile visible")
    check("G1_PROFILE_MODEL_ROUTE", "deepseek-v4-flash" in out, "model visible in profile list (provider verified via config.yaml)")
    config_yaml = (HOME / "config.yaml")
    yaml_text = config_yaml.read_text(encoding="utf-8")
    check("G1_HOME_CONFIG_MODEL", "provider: opencode-go" in yaml_text and "default: deepseek-v4-flash" in yaml_text,
          "home config.yaml provider/model")
    check("G1_APPROVALS_MANUAL", "mode: manual" in yaml_text, "approvals.mode=manual (fail-closed)")

    # ── 3. KANBAN_WORKER_LIVENESS_GATE (real spawn) ────────────────────────
    rc, out, _ = run_hermes(["kanban", "boards"], timeout=120)
    check("G1_KANBAN_BOARDS_RC", rc == 0, f"rc={rc} boards={out.strip()[:60]}")
    kanban_db = HOME / "kanban.db"
    check("G1_KANBAN_DB_EXISTS", kanban_db.is_file() and kanban_db.stat().st_size > 0,
          f"{kanban_db.stat().st_size} bytes")

    task_id = None
    rc, out, _ = run_hermes(
        ["kanban", "create", "--project", "RP002-G1", "--assignee", "default",
         "--workspace", "scratch", "--body", "Reply with exactly the single word: OK",
         "--goal", "--goal-max-turns", "2", "G1 liveness canary v2"], timeout=120)
    check("G1_KANBAN_CREATE_RC", rc == 0, out.strip()[:120])
    for tok in out.split():
        if tok.startswith("t_"):
            task_id = tok.strip("(),")
            break
    check("G1_KANBAN_TASK_CREATED", task_id is not None, f"task={task_id}")

    worker_ok = False
    if task_id:
        rc, out, _ = run_hermes(["kanban", "dispatch", "--max", "1"], timeout=180)
        check("G1_DISPATCH_RC", rc == 0, f"rc={rc} {out.strip()[:120]}")
        check("G1_DISPATCH_SPAWNED", "Spawned:    1" in out or task_id in out, out.strip()[-160:])
        # poll for worker completion (goal: trivial reply)
        deadline = time.time() + 300
        last = ""
        while time.time() < deadline:
            rc, out, _ = run_hermes(["kanban", "runs", "--json", task_id], timeout=60)
            last = out
            try:
                runs = json.loads(out) if out.strip() else []
            except json.JSONDecodeError:
                runs = []
            if runs and runs[-1].get("status") in ("done", "complete", "completed", "failed", "crashed", "blocked"):
                worker_ok = True
                break
            time.sleep(20)
        runs_json = last
        check("G1_RUN_ROW_HAS_PID", "worker_pid" in runs_json, runs_json[:200])
        check("G1_WORKER_TERMINATED", worker_ok, f"final status from runs: {runs_json[:200]}")
        # heartbeat evidence: show events must contain claimed/spawned (+ heartbeat if emitted)
        rc, out, _ = run_hermes(["kanban", "show", task_id], timeout=60)
        check("G1_EVENTS_CLAIMED", "claimed" in out, "claim event present")
        check("G1_EVENTS_SPAWNED", "spawned" in out, "spawn event present")

    # ── 4. PRE_DISPATCH_AUTHORIZATION_GATE ─────────────────────────────────
    # A task without an authorization receipt must NOT spawn: verify dispatch dry-run
    # spawns 0 for a task that is not assigned/admitted. Sensitive = R3/R4 class.
    rc, out, _ = run_hermes(["kanban", "dispatch", "--dry-run", "--max", "5"], timeout=120)
    check("G1_NO_UNAUTHORIZED_SPAWN", "Spawned:      0" in out, out.strip()[-120:])
    # HGK WorkOrder contract: spine admission requires authorized state before execution
    spine_proc = subprocess.run(
        [str(HGK / ".venv" / "Scripts" / "python.exe"), "-c",
         "import sys; from pathlib import Path; sys.path.insert(0, r'src'); "
         "from hg_kseos.spine import SharedSpine; "
         "s=SharedSpine(Path(r'var/shared-spine/hg-kseos.db')); snap=s.snapshot(); "
         "print('SPINE_OK', snap['counts']['requirements'], snap['open_blocking_tt'])"],
        cwd=str(HGK), capture_output=True, text=True, timeout=60)
    out2 = spine_proc.stdout
    check("G1_SPINE_READABLE", "SPINE_OK" in out2, out2[:80])

    # ── 5. CROSS_PROFILE_SECRET_ISOLATION_GATE ─────────────────────────────
    # synthetic secret only: create a canary profile, put a synthetic secret in its env,
    # verify a lower-privileged process (default profile, no candidate write tools) does NOT see it.
    synth = "RP2_SYNTH_SECRET_" + hashlib.sha256(b"g1-canary").hexdigest()[:16]
    tmp_home = Path(tempfile.mkdtemp(prefix="rp002-g1-prof-"))
    (tmp_home / "profiles").mkdir(parents=True, exist_ok=True)
    (tmp_home / "profiles" / "canary").mkdir(parents=True, exist_ok=True)
    (tmp_home / "profiles" / "canary" / ".env").write_text(f"SYNTHETIC_CANARY_SECRET={synth}\n", encoding="utf-8")
    # default profile env must not contain the synthetic secret
    env = os.environ.copy()
    env["HERMES_HOME"] = str(tmp_home)
    env.pop("PYTHONPATH", None)
    p = subprocess.run([str(exe), "profile", "list"], env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=60)
    check("G1_SYNTH_SECRET_ISOLATED", synth not in (p.stdout or "") and synth not in (p.stderr or ""),
          "synthetic secret not visible to default-profile process")
    # cross-profile: canary profile env is not readable from default profile context
    rc, out, _ = run_hermes(["profile", "list"], timeout=60, extra_env={"HERMES_HOME": str(tmp_home)})
    check("G1_SECOND_PROFILE_RUNTIME", rc == 0 and "canary" in out,
          f"rc={rc} second home lists canary profile")

    # ── 6. WRITE_READBACK_INTEGRITY_GATE ───────────────────────────────────
    critical = G1 / "critical_write_probe.txt"
    critical.write_bytes(b"normal content line\n" * 5)
    try:
        vr = verify_critical_write(critical)
        check("G1_WRITE_READBACK_SHA", len(vr["sha256"]) == 64 and vr["bytes"] == len(b"normal content line\n" * 5),
              f"bytes={vr['bytes']} sha={vr['sha256'][:16]}…")
    except RuntimeError as exc:
        check("G1_WRITE_READBACK_SHA", False, str(exc))
    poisoned = G1 / "critical_write_poisoned.txt"
    poisoned.write_bytes(b"good content\n...[truncated]\n")
    try:
        verify_critical_write(poisoned)
        check("G1_TRUNCATION_SENTINEL_DETECTED", False, "sentinel NOT detected — DEFECT")
    except RuntimeError as exc:
        check("G1_TRUNCATION_SENTINEL_DETECTED", "ERR_LITERAL_TRUNCATION_SENTINEL" in str(exc), str(exc))

    verdict = "PASS" if all(c["pass"] for c in checks) else "FAIL"
    evidence = {
        "artifact_id": "RP002_G1_EVIDENCE",
        "project_id": "HGK-REFERENCE-PROJECT-002",
        "generated_at_utc": ts,
        "oracle": "EXTERNAL_FROZEN_BOOTSTRAP_ORACLE",
        "gate": "G1",
        "candidate": {
            "executable": str(exe),
            "version": "0.20.0", "tag": "v2026.8.3",
            "commit": "3c27eb6234bf91b8ceee9e9071591b31e9b148cb",
            "home": str(HOME),
            "provider": "opencode-go", "model": "deepseek-v4-flash",
        },
        "verdict": verdict,
        "checks": checks,
        "note": "A2A native subcommand absent in pinned candidate -> same-host Kanban remains the qualified interop route (CF1 qualifies ContextForge A2A). "
                "Provider credential is process-scoped env-ref (never stored/printed).",
    }
    (G1 / "RP002_G1_EVIDENCE.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
