"""Supplementary capability probes that needed corrected arguments (second pass).

Adds:
  cap01_compiler_acceptance  - acceptance subcommand on the R5 contract
  cap01_compiler_duplication - duplication rule PL-001 against the thin prompt
  cap02_pkg_check_*          - approved-document-verifier against the PKG.md attachment
  cap_pipd_profile_ok        - profile_record with a VALID axis set
  cap_pipd_claim_ladder_ok   - claim_ceiling with a VALID claim name
  cap_pipd_intake_pkg_refuse - intake over the real PKG.md (ambiguous-compound refusal)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_lib import capture  # noqa: E402

ROOT = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY")
PY = "C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe"
R = str(ROOT / "RUNNERS")

KB = "C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS"
COMPILER = f"{KB}/construction-acceptance-prompt-compiler/construction-acceptance-prompt-compiler/scripts/prompt_contract_compiler.py"
THIN = "C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/compiler_native_output_R5/thin-prompt.md"
CONTRACT = "C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/C0_C9_CONTRACT_R5.json"
PKG = ("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/"
       "attachments/Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md")
PKG_CHECK = "C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/pipd_pkg_v2_check.py"


def main() -> int:
    records = []

    def run(pid, cmd, cwd, **kw):
        rec = capture(pid, cmd, cwd=cwd, **kw)
        records.append(rec)
        print(f"{pid}: exit={rec['exit_code']}")

    run("cap01_compiler_acceptance", [PY, COMPILER, "acceptance", CONTRACT], cwd=str(ROOT))
    run("cap01_compiler_activation", [PY, COMPILER, "activation", CONTRACT], cwd=str(ROOT))
    run("cap01_compiler_duplication",
        [PY, COMPILER, "duplication", THIN, "--source", PKG], cwd=str(ROOT))
    run("cap02_pkg_check_run", [PY, PKG_CHECK, "--doc", PKG, "--check"], cwd=str(ROOT))
    run("cap02_pkg_check_selftest_corrected", [PY, PKG_CHECK, "--doc", PKG, "--materialize"],
        cwd=str(ROOT))
    run("cap_pipd_profile_ok", [PY, f"{R}/probe_pipd_chain.py", "profile-ok"], cwd=str(ROOT))
    run("cap_pipd_claim_ladder_ok", [PY, f"{R}/probe_pipd_chain.py", "claim-ladder-ok"],
        cwd=str(ROOT))
    run("cap_pipd_intake_pkg", [PY, f"{R}/probe_pipd_chain.py", "intake-pkg"], cwd=str(ROOT))

    out = ROOT / "RUNNERS" / "supplement_probes.json"
    out.write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out} ({len(records)} probes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
