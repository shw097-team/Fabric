"""Extract the R10 session's canonical-skills-tree writes from the curator ledger.

Read-only. Prints only what the ledger records (no credential values).
"""
import json

p = ("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/"
     "LocalCache/Local/hermes/skills/.curator_ledger.jsonl")

recs = []
for line in open(p, encoding="utf-8"):
    line = line.strip()
    if line:
        try:
            recs.append(json.loads(line))
        except Exception:
            pass

print("record keys (first record):", sorted(recs[0].keys()))
print("a full record (truncated to 900 chars):")
print(json.dumps(recs[-1])[:900])
print()

SID = "20261015_125956_d5f877"
print("=== every ledger record with session_id == %s, on/after 2026-10-16T00:00Z ===" % SID)
n = 0
for r in recs:
    ev = r.get("evidence") or {}
    if ev.get("session_id") != SID:
        continue
    if str(r.get("ts", "")) < "2026-10-16T00:00":
        continue
    n += 1
    after = [(x.get("sha256") or "")[:12] for x in (r.get("after") or [])]
    before = [(x.get("sha256") or "")[:12] for x in (r.get("before") or [])]
    print(" %s actor=%-7s action=%-11s skill=%-28s file=%-45s before=%s after=%s" % (
        r.get("ts"), r.get("actor"), r.get("action"), r.get("skill"),
        ev.get("file_path") or "-", before, after))
print("count:", n)

print()
print("=== the same session's records BEFORE 2026-10-16T00:00Z (count only) ===")
n2 = sum(1 for r in recs
         if (r.get("evidence") or {}).get("session_id") == SID
         and str(r.get("ts", "")) < "2026-10-16T00:00")
print("count:", n2)
