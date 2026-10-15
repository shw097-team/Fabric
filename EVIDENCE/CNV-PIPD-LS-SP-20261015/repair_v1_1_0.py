#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""嘗試以 byte-精準差異還原 6 號 v1.1.0 PATCHED。

方法：以 v2.0.0 PATCHED 作為基準，先取連續 2 行之組合，再取非連續 2 行，
再取 3 行，並逐一測 SHA-256 是否等於 pin 的 target SHA。
"""
import os
import json
import hashlib
import itertools

ROOT = r"C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015"
RB = os.path.join(ROOT, "physical_source_readback")

pin = {}
with open(os.path.join(ROOT, "PHYSICAL_SOURCE_READBACK_MANIFEST.json"), encoding="utf-8") as f:
    src_manifest = json.load(f)
for m in src_manifest["missing"]:
    if m["filename"].startswith("Fabric_Hermes_HGK_Convergence_Global_Engineering_Blueprint_v1.1.0"):
        pin = m
        break

target_sha = pin["sha256"]
target_len = pin["bytes"]

v2_path = os.path.join(RB, "Fabric_Hermes_HGK_Convergence_Global_Engineering_Blueprint_v2.0.0_PATCHED_2026-10-15.md")
with open(v2_path, "rb") as f:
    v2 = f.read()

l = v2.splitlines(keepends=True)
n = len(l)
cum = [0]
for x in l:
    cum.append(cum[-1] + len(x))
removed_needed = cum[-1] - target_len
print("v2 bytes", len(v2), "target", target_len, "drop", removed_needed, "lines", n)

found = None

# 掃描連續 k 行 (為節約時間，僅窮舉頭部 200 行內)
HEAD_LIM = 200
for k in (1, 2, 3):
    if found:
        break
    for i in range(HEAD_LIM - k + 1):
        dropped = cum[i + k] - cum[i]
        if dropped != removed_needed:
            continue
        cand = v2[:cum[i]] + v2[cum[i + k]:]
        if hashlib.sha256(cand).hexdigest() == target_sha:
            found = ("contig", i, k, (l[i:i+k] and b"".join(l[i:i+k])[:80]))
            break
    print("contig scan k", k, "done", found)

# 非連續 k-行組合窮舉頭 200 行內
for k in (2,):
    if found:
        break
    for combo in itertools.combinations(range(HEAD_LIM), k):
        s = sum(cum[i + 1] - cum[i] for i in combo)
        if s != removed_needed:
            continue
        pieces = []
        pos = 0
        for idx in sorted(combo):
            pieces.append(v2[pos:cum[idx]])
            pos = cum[idx + 1]
        pieces.append(v2[pos:])
        cand = b"".join(pieces)
        if hashlib.sha256(cand).hexdigest() == target_sha:
            found = ("noncontig", tuple(combo), k)
            break
    print("noncontig scan k", k, "done", found)

print("FOUND", found)
