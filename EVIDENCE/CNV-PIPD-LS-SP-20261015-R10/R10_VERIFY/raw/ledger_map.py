"""Map the canonical skills-tree curator ledger: who wrote what, when, in which session.

Read-only. Written by the R10-0 independent checker under its own write root.
"""
import json
from collections import Counter

p = ("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/"
     "LocalCache/Local/hermes/skills/.curator_ledger.jsonl")

recs = []
for line in open(p, encoding="utf-8"):
    line = line.strip()
    if not line:
        continue
    try:
        recs.append(json.loads(line))
    except Exception:
        pass

print("total ledger records:", len(recs))


def leaf(x):
    return (x.get("path") or "").replace(chr(92), "/").rsplit("/", 1)[-1]


def short(x):
    return (x.get("sha256") or "")[:12]


print("actors:", dict(Counter(r.get("actor") for r in recs)))
print("actions:", dict(Counter(r.get("action") for r in recs)))

TARGETS = ("hgk-lifecycle-admission", "hgk-kanban-and-lane-routing",
           "hgk-governed-execution", "remote-repo-publication")

for skill in TARGETS:
    print()
    print("=== skill: %s ===" % skill)
    for r in recs:
        if r.get("skill") != skill:
            continue
        b = [(leaf(x), short(x)) for x in (r.get("before") or [])]
        a = [(leaf(x), short(x)) for x in (r.get("after") or [])]
        print(" ts=%s actor=%-8s action=%-11s file=%-32s session=%s" % (
            r.get("ts"), r.get("actor"), r.get("action"),
            (r.get("evidence") or {}).get("file_path") or "-",
            (r.get("evidence") or {}).get("session_id")))
        print("     before=%s" % b)
        print("     after =%s" % a)

print()
print("=== sessions that appear in the ledger, with record counts ===")
c = Counter((r.get("evidence") or {}).get("session_id") for r in recs)
for sid, n in c.most_common(12):
    print(" %s : %d" % (sid, n))
