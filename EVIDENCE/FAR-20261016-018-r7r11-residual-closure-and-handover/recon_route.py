#!/usr/bin/env python
"""FAR-20261016-018 recon: Gate-1 route, lane pools, SKCV pointer verification. Read-only."""
import json, hashlib, sys, datetime
from pathlib import Path

HGK = Path("C:/Projects/Agent_Workspace/HG-KSEOS")
SKILL = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/"
             "skills/software-development/hgk-governed-execution")
OUT = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261016-018-r7r11-residual-closure-and-handover")
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(HGK / "src"))
res = {"schema": "FAR-20261016-018/ROUTE-CHECK/1",
       "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}

try:
    from hg_kseos import named_methods as nm
    snap = nm.registry_snapshot() if hasattr(nm, "registry_snapshot") else None
    res["registry"] = {"snapshot_ok": snap is not None,
                       "n_methods": len(snap) if hasattr(snap, "__len__") else None}
    for label, flow in (("FAR_RESEARCH", "RESEARCH_LITERATURE_REPO"),
                        ("NEGATIVE_CONTROL", "PURE_QA_CHAT")):
        try:
            r = nm.route(flow)
            res["registry"]["route_" + label] = {
                "flow": flow,
                "route": r.get("route") if isinstance(r, dict) else getattr(r, "route", None),
                "reason_code": r.get("reason_code") if isinstance(r, dict) else getattr(r, "reason_code", None)}
        except Exception as e:
            res["registry"]["route_" + label] = {"flow": flow, "error": type(e).__name__ + ": " + str(e)[:160]}
except Exception as e:
    res["registry"] = {"import_error": type(e).__name__ + ": " + str(e)}

pools = {}
try:
    d = json.loads((HGK / "config/lane-route-slots.candidate.json").read_text(encoding="utf-8"))
    for v in (d.get("lanes") or []):
        if not isinstance(v, dict):
            continue
        entry = []
        for i, p in enumerate(v.get("ordered_pool") or []):
            arm = ((p.get("provider") or "") + "/" + (p.get("model") or "")) if isinstance(p, dict) else str(p)
            entry.append({"rank": i + 1, "arm": arm,
                          "transport": p.get("transport") if isinstance(p, dict) else None})
        pools[v.get("lane")] = {"engine": v.get("engine"), "transport": v.get("transport"), "pool": entry}
except Exception as e:
    pools = {"error": type(e).__name__ + ": " + str(e)}
res["lane_pools"] = pools

ptrs = []
for f in sorted((SKILL / "references").glob("*.md")):
    for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
        if "SKCV-POINTER" not in line:
            continue
        rec = {"pointer_file": f.name}
        try:
            tail = line.split("payload moved verbatim to ", 1)[1]
            target, rest = tail.split(" byte offset ", 1)
            target = target.strip()
            for pfx in ("skill/", "./"):
                if target.startswith(pfx):
                    target = target[len(pfx):]
            off = int(rest.split()[0])
            ln = int(rest.split("length ")[1].split()[0])
            sha = rest.split("sha256 ")[1].split()[0].rstrip(";.")
            rec.update({"target": target, "offset": off, "length": ln, "sha256_claimed": sha})
            tp = SKILL / target
            if tp.exists():
                data = tp.read_bytes()
                actual = hashlib.sha256(data[off:off + ln]).hexdigest()
                rec.update({"target_exists": True, "target_bytes": len(data), "sha256_actual": actual,
                            "pointer_verdict": "MATCH" if actual == sha else "MISMATCH"})
            else:
                rec.update({"target_exists": False, "pointer_verdict": "TARGET_MISSING"})
        except Exception as e:
            rec["pointer_verdict"] = "UNPARSEABLE:" + type(e).__name__
        ptrs.append(rec)
res["skcv_pointers"] = {"count": len(ptrs), "items": ptrs}
res["entry_map_present"] = (SKILL / "entry_map.json").exists()
res["topics_present"] = [p.name for p in sorted((SKILL / "references/topics").glob("*.md"))]

(OUT / "ROUTE_CHECK.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print("registry:", json.dumps(res["registry"], ensure_ascii=False)[:400])
for k, v in pools.items():
    print("lane", k, "| engine", v.get("engine"), "| transport", v.get("transport"))
    for e in v.get("pool", []):
        print("      rank", e["rank"], e["arm"], "|", e.get("transport"))
print("entry_map_present:", res["entry_map_present"])
print("pointers:", [(p["pointer_file"][:36], p.get("pointer_verdict"), p.get("target")) for p in ptrs])
