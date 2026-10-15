"""Throwaway: exercise the pipd chain to learn real I/O shapes. Not delivered evidence."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, "C:/Projects/Agent_Workspace/PIPD/src")
from pipd_ls_sp import pipeline  # noqa: E402

PKG = ("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/"
       "LocalCache/Local/hermes/attachments/Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md")
OUT = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/"
           "R6_DELIVERY/RAW/scratch_chain")
OUT.mkdir(parents=True, exist_ok=True)

card = pipeline.intake("converge PIPD-LS-SP under HG-KSEOS sole control plane",
                       sources=[PKG], constraints=["LOCAL_CEILING"],
                       non_goals=["production"])
print("intake keys:", list(card.keys()))
print("atoms:", len(card["atoms"]))
(OUT / "intent_card.json").write_text(json.dumps(card, ensure_ascii=False, indent=1),
                                      encoding="utf-8")

pi = pipeline.compile_pi(card, "LITE")
print("PI keys:", list(pi.keys()))
(OUT / "pi.json").write_text(json.dumps(pi, ensure_ascii=False, indent=1), encoding="utf-8")

pd_ = pipeline.bind_pd(pi, None)
print("PD keys:", list(pd_.keys()))
(OUT / "pd.json").write_text(json.dumps(pd_, ensure_ascii=False, indent=1), encoding="utf-8")

ecp = pipeline.compile_ecp(pd_, pi)
print("ECP keys:", list(ecp.keys()))
(OUT / "ecp.json").write_text(json.dumps(ecp, ensure_ascii=False, indent=1), encoding="utf-8")

tqaep = pipeline.compile_tqaep(pi, ecp, maker="HERMES-MAKER",
                               checker="GLM-5.3-FLASH-AO-LANE",
                               checker_execution_receipt="LOCAL_SELFTEST_RECEIPT_PLACEHOLDER")
print("TQAEP keys:", list(tqaep.keys()))
(OUT / "tqaep.json").write_text(json.dumps(tqaep, ensure_ascii=False, indent=1),
                                encoding="utf-8")

cc = pipeline.compile_construction_contract(pd_)
print("CC keys:", list(cc.keys()))
(OUT / "cc.json").write_text(json.dumps(cc, ensure_ascii=False, indent=1), encoding="utf-8")

print("DONE")
