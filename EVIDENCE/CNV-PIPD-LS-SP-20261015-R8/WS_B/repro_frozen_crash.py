"""Reproduce the derive_frozen_context crash on main's s1 bundle (string risk_guard)."""
import json
import sys
import traceback
from pathlib import Path

WT = Path("C:/Projects/Agent_Workspace/PIPD/worktrees/r8-wt")
sys.path.insert(0, str(WT / "src"))

from pipd_ls_sp import validate  # noqa: E402

bundle = json.loads((WT / ".hgk/artifacts/s1/bundle.json").read_text(encoding="utf-8"))
pi = bundle.get("PI-PKG")
print("PI-PKG risk_guard type:",
      type(pi["stable_semantic_contract"]["atoms"][0]["risk_guard"]).__name__)
try:
    validate.derive_frozen_context(pi)
    print("derive_frozen_context: no error")
except Exception:
    print("derive_frozen_context: RAISED")
    traceback.print_exc()
