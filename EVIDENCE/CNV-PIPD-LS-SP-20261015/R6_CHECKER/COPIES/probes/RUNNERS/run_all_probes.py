"""Drive every same-subject capability probe through probe_lib.capture.

Writes RAW/<probe_id>.{stdout,stderr,json} for each probe and a summary at
RUNNERS/capability_probes.json. No network, no canonical writes.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_lib import capture  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PY = "C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe"
PY312 = "C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe"
R = str(ROOT / "RUNNERS")

# Compiler / document verifier entrypoints
KB = "C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS"
COMPILER = f"{KB}/construction-acceptance-prompt-compiler/construction-acceptance-prompt-compiler/scripts/prompt_contract_compiler.py"
THIN = "C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/compiler_native_output_R5/thin-prompt.md"
CONTRACT = "C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/C0_C9_CONTRACT_R5.json"
PKG_CHECK = "C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/pipd_pkg_v2_check.py"
OPENSPEC = "C:/Users/user/AppData/Roaming/npm/openspec.cmd"
SKILL_PACK = "C:/Projects/Agent_Workspace/PIPD/tools/skill_pack_check.py"
GITHUB_PUB = "C:/Projects/Agent_Workspace/PIPD/tools/github_publish.py"
CHECKER = "C:/Projects/Agent_Workspace/HG-KSEOS/tools/check_acceptance_independent.py"
ROLE_ASSERT = "C:/Projects/Agent_Workspace/HG-KSEOS/scripts/runtime_role_binding_assert.py"
LANE_TC = "C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-toolchain.py"
CODEX_EXE = "C:/Users/user/AppData/Local/OpenAI/Codex/bin/9614f1d9b40d9c4f/Hermes"  # placeholder
CODEX_BIN = "C:/Users/user/AppData/Local/OpenAI/Codex/bin/9614f1d9b40d9c4f/codex.exe"
HERMES_HOME = "C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes"
HERMES_PY = f"{HERMES_HOME}/hermes-agent/venv/Scripts/python.exe"


def main() -> int:
    records = []

    def run(pid: str, cmd: list[str], cwd: str, **kw) -> None:
        rec = capture(pid, cmd, cwd=cwd, **kw)
        records.append(rec)
        print(f"{pid}: exit={rec['exit_code']}")

    # --- HGK-typed-spine-and-lifecycle (captured separately in run_cap03_spine) ---
    for mode in ("positive", "negative", "acceptance", "teardown"):
        rec = capture(f"cap03_spine_{mode}",
                      [PY, f"{R}/probe_spine_lifecycle.py", mode], cwd=str(ROOT))
        records.append(rec)
        print(f"cap03_spine_{mode}: exit={rec['exit_code']}")

    # --- native-prompt-compiler / approved-document-verifier (ACC-001, ACC-002) ---
    run("cap01_compiler_lint", [PY, COMPILER, "lint", CONTRACT], cwd=str(ROOT))
    run("cap01_compiler_hash", [PY, COMPILER, "hash", THIN], cwd=str(ROOT))
    run("cap02_pkg_check_selftest", [PY, PKG_CHECK, "--selftest"], cwd=str(ROOT))
    run("cap02_pkg_check_help", [PY, PKG_CHECK, "--help"], cwd=str(ROOT))

    # --- Hermes-canonical-runtime (ACC-004): real hermes via module entry ---
    hermes_cmd = [HERMES_PY, "-c",
                  "import sys;sys.argv=['hermes','--version'];"
                  "from hermes_cli.main import main;main()"]
    run("cap04_hermes_version", hermes_cmd, cwd=str(ROOT), env_extra={"HERMES_HOME": HERMES_HOME})

    # --- Codex-EXECUTE-DeepSeek (ACC-005) / Codex-VERIFY-GLM (ACC-006) ---
    run("cap05_codex_version", [CODEX_BIN, "--version"], cwd=str(ROOT))
    run("cap05_lane_toolchain_resolve", [PY, LANE_TC, "--resolve"], cwd=str(ROOT))
    run("cap05_role_binding_assert", [PY, ROLE_ASSERT, "--help"], cwd=str(ROOT))

    # --- Hermes-Kanban (ACC-007) ---
    kanban_cmd = [HERMES_PY, "-c",
                  "import sys;sys.argv=['hermes','kanban','boards','list'];"
                  "from hermes_cli.main import main;main()"]
    run("cap07_kanban_boards", kanban_cmd, cwd=str(ROOT), env_extra={"HERMES_HOME": HERMES_HOME})
    swarm_cmd = [HERMES_PY, "-c",
                 "import sys;sys.argv=['hermes','kanban','swarm','--help'];"
                 "from hermes_cli.main import main;main()"]
    run("cap08_swarm_help", swarm_cmd, cwd=str(ROOT), env_extra={"HERMES_HOME": HERMES_HOME})

    # --- gstack-advisory (ACC-011) ---
    run("cap11_gstack_positive", [PY, f"{R}/probe_gstack_rolemap.py", "positive"], cwd=str(ROOT))
    run("cap11_gstack_negative", [PY, f"{R}/probe_gstack_rolemap.py", "negative"], cwd=str(ROOT))

    # --- OpenSpec-brownfield (ACC-012) ---
    run("cap12_openspec_version", [OPENSPEC, "--version"], cwd=str(ROOT))

    # --- FAR-SQLite-FTS5 (ACC-013) ---
    run("cap13_fts5_positive", [PY, f"{R}/probe_fts5.py", "positive"], cwd=str(ROOT))
    run("cap13_fts5_negative", [PY, f"{R}/probe_fts5.py", "negative"], cwd=str(ROOT))
    run("cap13_fts5_teardown", [PY, f"{R}/probe_fts5.py", "teardown"], cwd=str(ROOT))

    # --- bounded-FS-API-Desktop (ACC-014) ---
    run("cap14_fda_positive", [PY, f"{R}/probe_fda_lease.py", "positive"], cwd=str(ROOT))
    run("cap14_fda_negative", [PY, f"{R}/probe_fda_lease.py", "negative"], cwd=str(ROOT))

    # --- approval-gated-GitHub (ACC-015) ---
    run("cap15_github_publish", [PY, GITHUB_PUB], cwd=str(ROOT))
    # --- AVR-HGK-Skill-loader (ACC-012-like) ---
    run("cap_avr_skill_pack", [PY, SKILL_PACK, "--all"], cwd=str(ROOT))

    # --- pipd-route-intake .. pipd-package-project (ACC-016..ACC-022) ---
    chain_modes = ["intake", "intake-missing", "intake-ambiguous", "profile",
                   "compile-pi", "compile-pi-tamper", "bind-pd-nocxt", "bind-pd",
                   "ecp", "tqaep-self", "tqaep-noreceipt", "tqaep", "claim-ceiling",
                   "project-unsafe"]
    for mode in chain_modes:
        pid = "cap_pipd_" + mode.replace("-", "_")
        run(pid, [PY, f"{R}/probe_pipd_chain.py", mode], cwd=str(ROOT))

    # --- checker / independent acceptance tool ---
    run("checker_independent_run", [PY, CHECKER], cwd=str(ROOT))

    out = ROOT / "RUNNERS" / "capability_probes.json"
    out.write_text(json.dumps(
        [{"probe_id": r["probe_id"], "exit_code": r["exit_code"],
          "stdout_file": r["stdout_file"], "stderr_file": r["stderr_file"],
          "stdout_sha256": r["stdout_sha256"], "stderr_sha256": r["stderr_sha256"],
          "command": r["command"], "cwd": r["cwd"],
          "started_utc": r["started_utc"], "ended_utc": r["ended_utc"],
          "timed_out": r["timed_out"]} for r in records],
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out} ({len(records)} probes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
