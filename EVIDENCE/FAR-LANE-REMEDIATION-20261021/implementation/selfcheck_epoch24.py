#!/usr/bin/env python
"""FAR-REMEDIATION-20261021 self-check harness (machine gate, re-runnable).

Re-derives every gate claim from LIVE files. Prints one row per check and a machine verdict.
Never prints PASS for an acceptance; verdict is a GATE, not an approval.
"""
from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
HG = Path(r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes")
CODEX = Path(r"C:/Users/user/AppData/Local/OpenAI/Codex/bin/896a0166b774037a/codex.exe")
rows = []


def add(cid, ok, detail):
    rows.append({"check": cid, "status": "PASS" if ok else "FAIL", "detail": detail})


def main() -> int:
    sys.path.insert(0, str(ROOT / "src"))
    import yaml
    from hg_kseos import lane_policy as lp

    reg = lp.load_registry()
    add("C1_epoch", reg.get("epoch") == 24, f"epoch={reg.get('epoch')}")
    want = {"PLAN": ("openai-codex", "gpt-6.1-sol", "hermes"),
            "EXECUTE": ("opencode-go", "deepseek-v4.1-flash", "codex-cli"),
            "VERIFY_SECURITY": ("openai-codex", "gpt-6.1-sol", "codex-cli")}
    for lane, (p, m, e) in want.items():
        r = lp.route_for_lane(reg, lane) or {}
        add(f"C2_route_{lane}", (r.get("provider"), r.get("model"), r.get("engine")) == (p, m, e),
            f"{r.get('provider')}/{r.get('model')} engine={r.get('engine')}")
    drift = lp.check_drift(registry=reg)
    add("C3_drift_empty", drift == [], f"{len(drift)} rows {drift}")
    lb = json.loads((ROOT / "config" / "hermes-codex-lane.json").read_text(encoding="utf-8"))
    exe = Path(lb["codex_executable"])
    add("C4_pin_exists", exe.exists(), str(exe))
    if exe.exists():
        add("C5_pin_sha", hashlib.sha256(exe.read_bytes()).hexdigest() == lb["codex_sha256"], lb["codex_sha256"][:16])
        out = subprocess.run([str(exe), "--version"], capture_output=True, text=True, timeout=60).stdout.strip()
        add("C6_pin_version", lb["codex_version"] in out, out)
    pool = json.loads((ROOT / "config" / "lane-route-slots.candidate.json").read_text(encoding="utf-8"))
    for lane in pool["lanes"]:
        pool_ok = lane["ordered_pool"][0]["role"].startswith("DEFAULT") and \
                  [c["rank"] for c in lane["ordered_pool"]] == list(range(1, len(lane["ordered_pool"]) + 1))
        add(f"C7_pool_{lane['lane']}", pool_ok, f"rank1={lane['ordered_pool'][0]['provider']}/{lane['ordered_pool'][0]['model']} role={lane['ordered_pool'][0]['role']}")
    prof = yaml.safe_load((HG / "profiles" / "hgk-governed" / "config.yaml").read_text(encoding="utf-8"))
    add("C8_profile_binding", (prof["model"]["default"], prof["model"]["provider"]) == ("gpt-6.1-sol", "openai-codex"),
        f"{prof['model']['provider']}/{prof['model']['default']}")
    ag = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    add("C9_agents_epoch", "(current, epoch 23)" in ag, "epoch heading present")
    a = json.loads((ROOT / "config" / "model-lane-assignment.json").read_text(encoding="utf-8"))
    add("C10_assignment_epoch", a.get("registry_epoch") == 24 and a.get("revision") == 24,
        f"{a.get('registry_epoch')}/{a.get('revision')}")
    add("C11_sod_declared", any(d.get("id") == "SOD006-C4" and d.get("status") == "OPEN_OWNER_ORDERED"
                                for d in reg["sod_invariants"]["declared_conflicts"]), "SOD006-C4")
    # F1: a cross-field restatement that check_drift() CANNOT see (it compares each binding only
    # against its own pointer target). The prose field must restate the chain's primary arm.
    ch0 = a["lane_chains"]["VERIFY_SECURITY"][0]
    arm_a = a["sod"].get("verify_security_arm_A", "")
    add("C15_crossfield_arm_A", arm_a.startswith(f"{ch0['provider']} / {ch0['model']}"),
        f"sod={arm_a!r} chain={ch0['provider']}/{ch0['model']}")
    # F5: a PROBE arm must never be the automatic default of a lane
    probe_auto = [(l['lane'], c['model']) for l in pool['lanes'] for c in l['ordered_pool']
                  if str(c.get('role','')).startswith('PROBE') and c.get('automatic_selection')]
    add("C16_probe_not_auto", not probe_auto, str(probe_auto))
    rc = subprocess.run([str(ROOT / ".venv" / "Scripts" / "python.exe"), "-m", "pytest", "tests/test_lane_policy.py", "-q"],
                        cwd=str(ROOT), capture_output=True, text=True, timeout=600)
    add("C12_pytest", rc.returncode == 0, (rc.stdout or "").strip().splitlines()[-1:])
    ch = ROOT / "openspec" / "changes" / "far-lane-remediation-20261021"
    add("C13_openspec_files", all((ch / p).exists() for p in ("proposal.md", "tasks.md", "specs/lane-routing/spec.md")), str(ch))
    board = HG / "kanban" / "boards" / "far-remediation-20261021" / "kanban.db"
    add("C14_kanban_board", board.exists(), str(board))
    failed = [r for r in rows if r["status"] == "FAIL"]
    verdict = "GATE_PASS" if not failed else "GATE_FAIL"
    for r in rows:
        print(f"{r['status']:4} {r['check']:26} {str(r['detail'])[:110]}")
    print(f"\nVERDICT: {verdict} ({len(rows)-len(failed)}/{len(rows)} checks pass)")
    print("CLAIM CEILING: local gate only; NOT an acceptance, NOT an independent verdict, NOT release.")
    (ROOT / "var" / "FAR-REMEDIATION-20261021" / "selfcheck_receipt.json").write_text(
        json.dumps({"verdict": verdict, "rows": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0 if not failed else 2


if __name__ == "__main__":
    sys.exit(main())
