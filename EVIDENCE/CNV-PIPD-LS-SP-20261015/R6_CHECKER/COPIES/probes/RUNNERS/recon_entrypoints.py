"""Read-only reconnaissance: does each candidate bound entrypoint execute on this host?

Prints one JSON line per candidate. Read-only (no writes outside RAW).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from probe_lib import capture  # noqa: E402

PY311 = "C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe"
WS = "C:/Projects/Agent_Workspace"

CANDIDATES = [
    # id, cmd, cwd, env_extra
    ("recon_spine_import", [PY311, "-c",
        "import sys;sys.path.insert(0,r'C:/Projects/Agent_Workspace/HG-KSEOS/src');"
        "from hg_kseos.spine import SharedSpine;print('SPINE_IMPORT_OK')"],
     WS, None),
    ("recon_hgk_cli_help", [PY311, "-c",
        "import sys;sys.path.insert(0,r'C:/Projects/Agent_Workspace/HG-KSEOS/src');"
        "from hg_kseos.cli import main;print('CLI_IMPORT_OK')"],
     WS, None),
    ("recon_pipd_import", [PY311, "-c",
        "import sys;sys.path.insert(0,r'C:/Projects/Agent_Workspace/PIPD/src');"
        "from pipd_ls_sp import cli;print('PIPD_IMPORT_OK',len(cli.COMMANDS))"],
     WS, None),
    ("recon_compiler_help", [PY311, str(Path(
        "C:/Projects/Agent_Workspace/\u77e5\u8b58\u5eab/\u5be6\u4f5c\u76f8\u95dcDOC/HG-KSEOS/"
        "construction-acceptance-prompt-compiler/construction-acceptance-prompt-compiler/"
        "scripts/prompt_contract_compiler.py")), "--help"],
     WS, None),
    ("recon_pipd_pkg_check_help", [PY311,
        "C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/pipd_pkg_v2_check.py",
        "--help"], WS, None),
    ("recon_checker_help", [PY311,
        "C:/Projects/Agent_Workspace/HG-KSEOS/tools/check_acceptance_independent.py", "--help"],
     WS, None),
    ("recon_hlpe_help", [PY311,
        "C:/Projects/Agent_Workspace/HG-KSEOS/tools/verify_hlpe.py", "--help"], WS, None),
    ("recon_far_retrieval_import", [PY311, "-c",
        "import sys;sys.path.insert(0,r'C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research');"
        "import far_retrieval;print('FAR_IMPORT_OK')"], WS, None),
    ("recon_fda_lease_import", [PY311, "-c",
        "import sys;sys.path.insert(0,r'C:/Projects/Agent_Workspace/Fabric/evidence/review/"
        "FDA_RAW_REVIEW_BUNDLE/Fabric/fabric-desktop-automation');import fda_lease;"
        "print('FDA_IMPORT_OK')"], WS, None),
    ("recon_review_bundle_selftest", [PY311,
        "C:/Projects/Agent_Workspace/Fabric/Independent Acceptance Officer/challenge-review/"
        "scripts/verify_review_bundle.py", "--self-test"], WS, None),
    ("recon_openspec_version", ["openspec", "--version"], WS, None),
    ("recon_codex_version",
     ["C:/Users/user/AppData/Local/OpenAI/Codex/bin/9614f1d9b40d9c4f/codex.exe", "--version"],
     WS, None),
    ("recon_hermes_core", ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
        "C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hermes-core.ps1"],
     "C:/Projects/Agent_Workspace/HG-KSEOS", None),
]


def main() -> int:
    rows = []
    for pid, cmd, cwd, env in CANDIDATES:
        rec = capture(pid, cmd, cwd, env_extra=env, timeout=180)
        rows.append(rec)
        out = Path(rec["stdout_file"])
        print(json.dumps({"probe_id": pid, "exit_code": rec["exit_code"],
                          "stdout_bytes": rec["stdout_bytes"],
                          "stderr_bytes": rec["stderr_bytes"]}, ensure_ascii=False))
    (HERE.parent / "RAW" / "recon_summary.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
