"""Emit R7_WRITE_SET.json: every file this bounded writer changed or created, with bytes + sha256.

Product files (the PIPD validator harden) carry their PRE-change sha256 from the captured
snapshot; round outputs and RAW artifacts are newly created (pre-change sha256 is null).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

R7 = Path(__file__).resolve().parent.parent
PRE = R7 / "RAW" / "pre_change"
PROD = Path("C:/Projects/Agent_Workspace/PIPD/src/pipd_ls_sp")
PRODUCT = ("validate.py", "pipeline.py", "cli.py")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def entry(p: Path, pre: Path | None) -> dict:
    return {"path": str(p), "bytes": p.stat().st_size, "sha256": sha256(p),
            "pre_change_sha256": sha256(pre) if pre else None}


changed = [entry(PROD / n, PRE / n) for n in PRODUCT]

created = []
for p in sorted(R7.rglob("*")):
    if not p.is_file():
        continue
    if "__pycache__" in p.parts or p.suffix == ".pyc":
        continue
    if p.parent == PRE:  # the captured pre-change snapshot (a provenance copy)
        continue
    created.append(entry(p, None))

doc = {
    "schema": "CNV-PIPD-LS-SP-20261015-R7/WRITE-SET/1",
    "changeset": "R7-0-VALIDATOR-AND-CHECKER-ISOLATION",
    "producer": "Codex CLI bounded writer EXECUTE lane (opencode-go/deepseek-v4.1-flash)",
    "product_writeset": "C:/Projects/Agent_Workspace/PIPD/src/pipd_ls_sp/**",
    "round_output_dir": str(R7),
    "note": ("product files carry pre_change_sha256 from RAW/pre_change snapshots; round artifacts "
             "and RAW evidence are newly created by this writer. Nothing under "
             "EVIDENCE/CNV-PIPD-LS-SP-20261015/** and no Fabric repo file was written."),
    "changed_product_files": changed,
    "created_round_files": created,
    "totals": {"changed_product_files": len(changed), "created_round_files": len(created)},
}
(R7 / "R7_WRITE_SET.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"wrote R7_WRITE_SET.json: changed={len(changed)} created={len(created)}")
for c in changed:
    print("  changed", Path(c["path"]).name, c["bytes"], c["sha256"][:12], "<-", c["pre_change_sha256"][:12])
