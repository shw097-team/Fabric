from __future__ import annotations

import json
from pathlib import Path


CWD = Path.cwd()
RESULT = CWD / "remediation_result.json"


def main() -> int:
    data = json.loads(RESULT.read_text(encoding="utf-8"))

    data["counts"] = {
        "references_md_before": 107,
        "references_md_after": 94,
        "harness_stated_references_md_before": 108,
        "count_method": "recursive *.md under skill/references, counted from disk in this lane",
        "net_change": -13,
        "discrepancy_note": (
            "The round harness stated 108 markdown files under skill/references/ before "
            "this lane. Recomputed from the bytes on disk in this lane, the count is 107 "
            "before and 94 after. The net change is -13 (14 removed, 1 added) either way; "
            "only the absolute baseline differs by one file."
        ),
    }
    data["exact_commands"] = [
        "Get-Content -LiteralPath "
        "C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014/"
        "evidence/postfreeze/hgk_unreachable.json -Raw",
        "C:\\\\Users\\\\user\\\\AppData\\\\Local\\\\Packages\\\\OpenAI.Codex_2p2nqsd0c76g0"
        "\\\\LocalCache\\\\Local\\\\hermes\\\\hermes-agent\\\\venv\\\\Scripts\\\\python.exe "
        "remediate_pilot.py",
        "C:\\\\Users\\\\user\\\\AppData\\\\Local\\\\Packages\\\\OpenAI.Codex_2p2nqsd0c76g0"
        "\\\\LocalCache\\\\Local\\\\hermes\\\\hermes-agent\\\\venv\\\\Scripts\\\\python.exe "
        "verify_pilot.py",
    ]
    data["interpreter_note"] = (
        "The brief-specified interpreter C:/Users/user/AppData/Local/Programs/Python/"
        "Python311/python.exe is not readable/executable in this sandbox (access denied). "
        "The lane used the available Python 3.11.17 at the hermes venv instead."
    )
    data["claim_ceiling"] = (
        "Candidate-only edit whose byte-level checks were recomputed in this lane from "
        "the bytes on disk. This is not acceptance and creates no canonical acceptance "
        "status. The merge reduces the references markdown file count by 13 net "
        "(14 removed, 1 added). The result is still above the 60-file references-sprawl "
        "warning cap, so that cap is still not met."
    )

    RESULT.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print("updated", RESULT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
