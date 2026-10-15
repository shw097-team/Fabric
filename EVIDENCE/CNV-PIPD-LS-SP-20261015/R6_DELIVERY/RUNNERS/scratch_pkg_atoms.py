"""Throwaway: why does the PKG fail clause-bound atom compilation? Locate the clause."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, "C:/Projects/Agent_Workspace/PIPD/src")
from pipd_ls_sp import requirements as R  # noqa: E402
from pipd_ls_sp.errors import IntakeInvalid  # noqa: E402

PKG = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/"
           "LocalCache/Local/hermes/attachments/Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md")

text = PKG.read_text(encoding="utf-8")
fail = 0
ok = 0
first = []
for start, end, clause in R._parts(text):
    try:
        R._expand(clause)
        ok += 1
    except IntakeInvalid as exc:
        fail += 1
        if len(first) < 5:
            first.append((start, end, clause[:160], str(exc)))
print("clauses ok=", ok, "fail=", fail, "total=", ok + fail)
for f in first:
    print("\nFAIL @", f[0], "-", f[1], "|", f[3])
    print("   ", repr(f[2]))
