"""v1.1.0 與 v2.0.0 相似度與可能差異分析（唯讀）。"""
import os, json, hashlib

ROOT = r"C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015"
rb = os.path.join(ROOT, "physical_source_readback")
v2_path = os.path.join(rb, "Fabric_Hermes_HGK_Convergence_Global_Engineering_Blueprint_v2.0.0_PATCHED_2026-10-15.md")
v2 = open(v2_path, encoding="utf-8").read()
l2 = v2.splitlines(keepends=True)

c0 = "# Fabric × Hermes × HG-KSEOS Convergence 全域工程藍圖\n".encode("utf-8")
l0_bytes = l2[0].encode("utf-8")
print("v2_l0_bytes", len(l0_bytes), "base_header_bytes", len(c0), "diff", len(l0_bytes) - len(c0))
print("line21_bytes", len(l2[21].encode("utf-8")), "line21", repr(l2[21]))
print("sum_drop_if_those_two_corrected", (len(l0_bytes) - len(c0)) + len(l2[21].encode("utf-8")))
