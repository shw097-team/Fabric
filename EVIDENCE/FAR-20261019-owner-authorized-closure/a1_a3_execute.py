#!/usr/bin/env python
"""FAR-20261019 Tier A execution (agent-side, local, reversible).

A1 canonical Codex pin repair: backup -> single-line edit -> read-only hash readback -> re-run the
   previous round's toolchain probe if it can be found.
A3 currentness erratum: the pack's prose says 50/50 while the machine receipt says 51/51.
Every step records raw evidence; a step that cannot be verified says so instead of reporting success.
"""
import json, hashlib, datetime, subprocess, sys, glob, os
from pathlib import Path

ROOT = Path("C:/Projects/Agent_Workspace/HG-KSEOS")
OUT = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261019-owner-authorized-closure")
PREV = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261016-018-r7r11-residual-closure-and-handover")
CFG = ROOT / "config/hermes-codex-lane.json"
rep = {"schema": "FAR-20261019/TIER-A-EXECUTION/1",
       "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "steps": []}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ---------------- A1: canonical pin repair ----------------
step = {"id": "A1", "action": "canonical Codex executable pin repair"}
raw_before = CFG.read_text(encoding="utf-8")
declared = json.loads(raw_before)
declared_path = None
for key in ("codex_executable", "executable", "codex_path"):
    if isinstance(declared.get(key), str):
        declared_path = declared[key]
        key_name = key
        break
bins = sorted(glob.glob("C:/Users/user/AppData/Local/OpenAI/Codex/bin/*/codex.exe"),
              key=lambda p: os.path.getmtime(p))
step["declared_key"] = key_name
step["declared_path"] = declared_path
step["declared_exists"] = bool(declared_path and Path(declared_path).exists())
step["live_binary_candidates"] = [{"path": b, "bytes": os.path.getsize(b),
                                   "mtime": datetime.datetime.fromtimestamp(os.path.getmtime(b)).isoformat(),
                                   "sha256": sha(b)[:32] + "..."} for b in bins[-3:]]

# minimal edit: rewrite only the one JSON string value inside the raw text, so the file's other bytes
# (and therefore any reviewer's diff) are untouched.
live = bins[-1].replace("/", "\\") if bins else None
step["chosen_live_binary"] = live
if live and declared_path and Path(live).exists():
    backup = OUT / "config-hermes-codex-lane.pre-A1.json"
    if not backup.exists():
        backup.write_text(raw_before, encoding="utf-8")
    step["backup"] = {"path": str(backup), "sha256": sha(backup), "bytes": backup.stat().st_size}
    step["config_sha256_before"] = sha(CFG)
    # JSON-escape the old value exactly as it appears in the file
    old_tok = json.dumps(declared_path)
    new_tok = json.dumps(live)
    if raw_before.count(old_tok) == 1:
        raw_after = raw_before.replace(old_tok, new_tok)
        changed_lines = [i for i, (a, b) in enumerate(zip(raw_before.splitlines(), raw_after.splitlines()))
                         if a != b]
        step["lines_changed"] = {"indices": changed_lines, "count": len(changed_lines),
                                 "before": raw_before.splitlines()[changed_lines[0]] if changed_lines else None,
                                 "after": raw_after.splitlines()[changed_lines[0]] if changed_lines else None}
        CFG.write_text(raw_after, encoding="utf-8")
        step["config_sha256_after"] = sha(CFG)
        reread = json.loads(CFG.read_text(encoding="utf-8"))
        step["reread_value"] = reread.get(key_name)
        step["reread_exists"] = Path(reread.get(key_name)).exists()
        step["keys_unchanged"] = sorted(reread.keys()) == sorted(declared.keys())
        step["verdict"] = ("REPAIRED_AND_READBACK_OK"
                           if step["reread_exists"] and step["keys_unchanged"] and step["lines_changed"]["count"] == 1
                           else "REPAIRED_BUT_READBACK_UNEXPECTED")
    else:
        step["verdict"] = "REFUSED_NOT_A_UNIQUE_TOKEN (%d occurrences)" % raw_before.count(old_tok)
else:
    step["verdict"] = "REFUSED_NO_LIVE_BINARY"

# re-run the previous round's toolchain probe, if any exists (find it, do not invent one)
probes = [p for p in glob.glob(str(PREV / "**/*.py"), recursive=True)
          if "lane" in Path(p).name.lower() and "probe" in Path(p).name.lower()]
step["probe_candidates"] = [Path(p).name for p in probes]
if probes:
    p = subprocess.run([str(ROOT / ".venv/Scripts/python.exe"), "-B", probes[0]],
                       capture_output=True, text=True, timeout=300, cwd=str(ROOT))
    step["probe_rerun"] = {"script": probes[0], "exit": p.returncode,
                           "stdout": (p.stdout or "").strip()[-700:], "stderr": (p.stderr or "").strip()[-300:]}
rep["steps"].append(step)
print("A1:", step["verdict"], "| declared_exists_before:", step["declared_exists"],
      "| chosen:", step.get("chosen_live_binary"), "| reread_exists:", step.get("reread_exists"),
      "| lines_changed:", (step.get("lines_changed") or {}).get("count"))

# ---------------- A3: currentness erratum ----------------
erratum = {
    "schema": "FAR-20261019/CURRENTNESS-ERRATUM/1",
    "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "items": [{
        "id": "FAR018-READBACK-SUMMARY-CURRENTNESS",
        "what": ("POST_PUBLICATION_ADDENDUM.md states 50/50 byte-exact while the final machine readback "
                 "receipt records 51/51 listed paths"),
        "authoritative_source": "REMOTE_READBACK_VERIFY.json (machine receipt, regenerated at the final tip)",
        "prose_source": "POST_PUBLICATION_ADDENDUM.md",
        "disposition": "ADDITIVE_ERRATUM — the historical addendum is not rewritten; this file records the "
                       "currentness correction. The machine receipt governs.",
        "action_taken": "none beyond recording; the addendum file is left byte-identical so the published "
                        "pack's history stays reproducible",
    }],
}
(OUT / "ERRATA_CURRENTNESS_019.json").write_text(json.dumps(erratum, ensure_ascii=False, indent=1), encoding="utf-8")
rep["steps"].append({"id": "A3", "verdict": "ERRATUM_RECORDED", "file": str(OUT / "ERRATA_CURRENTNESS_019.json")})
print("A3: erratum recorded")

(OUT / "TIER_A_EXECUTION.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", OUT / "TIER_A_EXECUTION.json")
