import json, os, subprocess, sys, textwrap

ROOT = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\ROUND3-LANE-REBIND-AND-CLOSURE-20261016"
COPY = os.path.join(ROOT, "lanes", "VERIFY_SECURITY", "V4", "work", "subject")
WORK = os.path.join(ROOT, "lanes", "VERIFY_SECURITY", "V4", "work")
GUARD = os.path.join(COPY, "scripts", "hgk-lane-guard.py")
sys.path.insert(0, os.path.join(COPY, "src"))
from hg_kseos import lane_policy as lp

reg = lp.load_registry(os.path.join(COPY, "config", "lane-routing-registry.yaml"))
print("=== registry routes ===")
for r in reg.get("routes", []):
    print(r.get("lane"), "|", r.get("provider"), "|", r.get("model"), "| arms:", r.get("selected_arm"),
          "| fallbacks:", r.get("fallbacks"))
print("=== sod_invariants ===")
print(json.dumps(reg.get("sod_invariants"), indent=1))
print("=== assignments/model-lane-assignment sizes ===")

# make an admission receipt that matches VERIFY arm A (deepseek-v4.1-flash)
adm = os.path.join(WORK, "TEST_RESULTS", "adm_verify_A.json")
json.dump({"status": "ADMITTED", "arm": {"provider": "opencode-go", "model": "deepseek-v4.1-flash"},
           "served": {"provider": "opencode-go", "model": "deepseek-v4.1-flash"}},
          open(adm, "w", encoding="utf-8"))

BASE = ["--lane", "VERIFY_SECURITY"]

def run(name, extra):
    cmd = [sys.executable, "-B", GUARD] + extra + ["--registry", os.path.join(COPY, "config", "lane-routing-registry.yaml"),
                                            "--root", COPY]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0 and not p.stdout.strip():
        print(f"[raw {name}] rc={p.returncode} err=\n{p.stderr}")
    try:
        v = json.loads(p.stdout)
    except Exception:
        v = {"parse_error": p.stdout[:400], "stderr": p.stderr[:400]}
    sod = None
    for c in v.get("checks", []) if isinstance(v, dict) else []:
        if c.get("id") == "sod_distinct_model":
            sod = c
    print(f"--- {name}: exit={p.returncode} status={v.get('status')} errors={v.get('errors')}")
    if v.get("parse_error"):
        print("    STDERR:", v.get("stderr"))
    print("    sod:", json.dumps(sod))
    print("    declared_conflict:", v.get("declared_conflict"))
    return p.returncode, v

# (1) UNDECLARED same-model pair: PLAN/PLAN, same model
run("1_undeclared_same_model_PLAN_PLAN",
    ["--lane", "PLAN", "--maker-lane", "PLAN", "--maker-engine", "opencode-go",
     "--maker-model", "glm-5.3-flash", "--target-engine", "opencode-go",
     "--target-model", "glm-5.3-flash"])

# (2) OWNER-ORDERED declared pair EXECUTE/VERIFY_SECURITY same model, WITH admitted receipt
run("2_declared_EXECUTE_VERIFY_admitted",
    BASE + ["--maker-lane", "EXECUTE", "--maker-engine", "opencode-go",
            "--maker-model", "deepseek-v4.1-flash", "--target-engine", "opencode-go",
            "--target-model", "deepseek-v4.1-flash", "--target-provider", "opencode-go",
            "--admission", adm])

# (2b) same declared pair but NO admission receipt (isolate SoD pass)
run("2b_declared_EXECUTE_VERIFY_no_admission",
    BASE + ["--maker-lane", "EXECUTE", "--maker-engine", "opencode-go",
            "--maker-model", "deepseek-v4.1-flash", "--target-engine", "opencode-go",
            "--target-model", "deepseek-v4.1-flash", "--target-provider", "opencode-go"])

# (3) distinct pair unaffected: maker deepseek, target glm
run("3_distinct_EXECUTE_VERIFY",
    BASE + ["--maker-lane", "EXECUTE", "--maker-engine", "opencode-go",
            "--maker-model", "deepseek-v4.1-flash", "--target-engine", "opencode-go",
            "--target-model", "glm-5.3-flash", "--target-provider", "opencode-go",
            "--admission", adm])

# (4) ambiguous maker lane: omit --maker-lane, maker_model=deepseek-v4.1-flash (matches EXECUTE & VERIFY defaults)
run("4_ambiguous_maker_lane_no_flag",
    BASE + ["--maker-engine", "opencode-go", "--maker-model", "deepseek-v4.1-flash",
            "--target-engine", "opencode-go", "--target-model", "deepseek-v4.1-flash",
            "--target-provider", "opencode-go", "--admission", adm])

# (4b) no-match maker lane: unknown model
run("4b_no_match_maker_lane",
    BASE + ["--maker-engine", "opencode-go", "--maker-model", "totally-unknown-model",
            "--target-engine", "opencode-go", "--target-model", "totally-unknown-model",
            "--target-provider", "opencode-go", "--admission", adm])

# (5) widening attempt: PLAN/VERIFY is distinct_required true -> same model must still refuse
run("5_widen_attempt_PLAN_VERIFY_same_model",
    BASE + ["--maker-lane", "PLAN", "--maker-engine", "opencode-go",
            "--maker-model", "glm-5.3-flash", "--target-engine", "opencode-go",
            "--target-model", "glm-5.3-flash", "--target-provider", "opencode-go",
            "--admission", adm])
