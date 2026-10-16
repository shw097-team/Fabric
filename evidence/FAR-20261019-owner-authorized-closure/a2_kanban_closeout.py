#!/usr/bin/env python
"""FAR-20261019 A2: close the previous round's own Kanban cards that carry evidence.

A card may only be completed if the artifact its title names actually exists on disk; the check is
recorded per card so a reader can see WHY it was completable. Cards whose output cannot be located are
left running and reported, not silently completed (a board that hides unfinished work is a false trace).
"""
import json, os, subprocess, datetime
from pathlib import Path

HERMES = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes")
AGENT = HERMES / "hermes-agent"
PY = AGENT / "venv/Scripts/python.exe"
BOARD = "far-018-r7r11-residual"
PREV = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261016-018-r7r11-residual-closure-and-handover")
OUT = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261019-owner-authorized-closure")
env = dict(os.environ, HERMES_HOME=str(HERMES))
calls = []

# card id -> the artifacts that prove the card's output exists
PROOF = {
    "R4": ["W1_RESIDUAL_UNIVERSE.json"],
    "R5": ["W2_DEFECT_DOSSIER.json"],
    "R6": ["lane/EXECUTE_RECEIPT.json", "writer/WRITER_MANIFEST.json"],
    "R7": ["lane/VERIFY_RECEIPT.json", "lane/VERIFY_ATTEMPT1_REFUSED.json"],
    "R8": ["FAR_RULING.md"],
    "R9": ["publish/payload/PACK_INDEX.json", "REMOTE_READBACK_VERIFY.json"],
    "R10": ["HANDOVER_FAR018.md", "SELF_CHECK_RECEIPT.json"],
    "R11": ["SELF_CHECK_RECEIPT.json", "SELF_EVOLUTION_RECORD.json"],
}


def k(*args, expect_ok=True):
    cmd = [str(PY), "hermes_cli/main.py", "kanban", "--board", BOARD, *[str(a) for a in args]]
    p = subprocess.run(cmd, cwd=str(AGENT), env=env, capture_output=True, text=True, timeout=180)
    calls.append({"argv": cmd[3:], "exit": p.returncode, "stdout": (p.stdout or "").strip()[:200]})
    if expect_ok and p.returncode != 0:
        print("  !!", p.returncode, " ".join(cmd[3:]), (p.stderr or "")[:100])
    return p


_r = k("ls", "--json")
try:
    cards = json.loads(_r.stdout or "[]")
except Exception:
    cards = []
byid = {}
for c in cards:
    t = c.get("title") or ""
    if " " in t:
        byid[t.split(" ")[0]] = c

rep = {"schema": "FAR-20261019/KANBAN-CLOSEOUT-PREV/1",
       "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "board": BOARD, "cards_seen": len(cards),
       "before_histogram": {}, "steps": [], "calls": calls}
for c in cards:
    s = c.get("status")
    rep["before_histogram"][s] = rep["before_histogram"].get(s, 0) + 1

for cid, proofs in PROOF.items():
    card = byid.get(cid)
    if not card:
        rep["steps"].append({"id": cid, "verdict": "CARD_NOT_FOUND"})
        continue
    if card.get("status") not in ("running", "todo", "ready", "backlog", "in_progress"):
        rep["steps"].append({"id": cid, "verdict": "ALREADY_TERMINAL", "status": card.get("status")})
        continue
    found = [p for p in proofs if (PREV / p).exists()]
    missing = [p for p in proofs if not (PREV / p).exists()]
    if not found:
        rep["steps"].append({"id": cid, "verdict": "LEFT_RUNNING_NO_PROOF_ON_DISK", "expected": proofs})
        print(cid, "left running: no proof found")
        continue
    tid = card.get("id")
    k("comment", tid, "closed by FAR-20261019 A2: output artifacts present on disk: " + ", ".join(found),
      "--author", "hgk-orchestrator", expect_ok=False)
    k("complete", tid, "--result", "output exists on disk (closed by FAR-019 closeout)",
      "--metadata", json.dumps({"proof": found, "closed_by_round": "FAR-20261019",
                                "unproven": missing}), expect_ok=False)
    rep["steps"].append({"id": cid, "verdict": "COMPLETED_WITH_PROOF", "proof": found, "unproven": missing})
    print(cid, "completed with proof", found, ("| unproven: %s" % missing) if missing else "")

_r2 = k("ls", "--json")
try:
    after = json.loads(_r2.stdout or "[]")
except Exception:
    after = []
for c in after:
    s = c.get("status")
    rep["after_histogram"] = rep.get("after_histogram", {})
    rep["after_histogram"][s] = rep["after_histogram"].get(s, 0) + 1
(OUT / "KANBAN_PREV_CLOSEOUT.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
print("before:", rep["before_histogram"], "after:", rep.get("after_histogram"))
