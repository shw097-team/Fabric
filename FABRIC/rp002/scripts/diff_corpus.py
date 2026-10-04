# -*- coding: utf-8 -*-
import os, json
rows = [json.loads(l) for l in open(r"C:\Projects\Agent_Workspace\Fabric\rp002\G0\RP002_INPUT_DENOMINATOR.jsonl", encoding="utf-8")]
corpus = {r["path"] for r in rows if r["root"] == "CORPUS"}
disk = set()
for dp, dn, fn in os.walk(r"C:\Projects\Agent_Workspace\教程字幕"):
    dn[:] = [d for d in dn if d not in (".git", "__pycache__")]
    for f in fn:
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, r"C:\Projects\Agent_Workspace\教程字幕").replace(os.sep, "/")
        if not f.endswith((".pyc", ".pyo")):
            disk.add(rel)
print("DISK", len(disk), "JSONL", len(corpus))
print("MISSING_FROM_JSONL", sorted(disk - corpus)[:10])
print("EXTRA_IN_JSONL", sorted(corpus - disk)[:10])
