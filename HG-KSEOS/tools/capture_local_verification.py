from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from hg_kseos.doctor import doctor


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--root", type=Path, required=True)
    root = parser.parse_args().root.resolve(strict=True)
    env = os.environ.copy(); env["PYTHONPATH"] = str(root / "src"); env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [str(root / ".venv" / "Scripts" / "python.exe"), "-m", "unittest", "discover", "-v"],
        cwd=root, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
    match = re.search(r"Ran (\d+) tests", output)
    test_count = int(match.group(1)) if match else -1
    doctor_report = doctor(root)
    hlpe = json.loads((root / "evidence" / "wave-04" / "HLPE_QUALIFICATION_REPORT.json").read_text(encoding="utf-8"))
    report = {
        "schema": "HGK-LOCAL-VERIFICATION/1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "local_tests": {"returncode": completed.returncode, "tests": test_count, "status": "PASS" if completed.returncode == 0 and test_count == 60 else "FAIL", "output_sha256": hashlib.sha256(output.encode()).hexdigest()},
        "doctor": doctor_report,
        "hlpe_upstream": hlpe,
        "claim_ceiling": "Local maker verification only; independent acceptance, remote CI, deploy, and production remain unclaimed.",
    }
    output_path = root / "evidence" / "wave-17" / "LOCAL_VERIFICATION_REPORT.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"tests": test_count, "test_status": report["local_tests"]["status"], "doctor": doctor_report["verdict"], "hlpe_status": hlpe.get("verdict")}))
    return 0 if report["local_tests"]["status"] == "PASS" and doctor_report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
