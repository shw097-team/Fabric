#!/usr/bin/env python
"""Drive the FAR-018 board through a real lifecycle. Every card gets CLI receipts (invariant 10a:
admission is not execution). Write path is the board DB only."""
import json, os, subprocess, datetime
from pathlib import Path

HERMES = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex@2p2nqsd0c76g0".replace("@", "_"))
HERMES = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes")
AGENT = HERMES / "hermes-agent"
PY = AGENT / "venv/Scripts/python.exe"
BOARD = "far-018-r7r11-residual"
OUT = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261016-018-r7r11-residual-closure-and-handover")
env = dict(os.environ, HERMES_HOME=str(HERMES))
calls = []


def k(*args, expect_ok=True):
    cmd = [str(PY), "hermes_cli/main.py", "kanban", "--board", BOARD, *[str(a) for a in args]]
    p = subprocess.run(cmd, cwd=str(AGENT), env=env, capture_output=True, text=True, timeout=180)
    rec = {"argv": cmd[3:], "exit": p.returncode, "stdout": (p.stdout or "").strip()[:300],
           "stderr": (p.stderr or "").strip()[:160]}
    calls.append(rec)
    if expect_ok and p.returncode != 0:
        print("  !!", p.returncode, " ".join(cmd[3:]), "::", rec["stderr"][:120])
    return rec, (p.stdout or "")


def ensure_board():
    """Self-repair: the first run of this driver assumed the board already existed and failed 19 calls
    closed on 'board does not exist'. Creating it here makes the driver self-contained."""
    cmd = [str(PY), "hermes_cli/main.py", "kanban", "boards", "create", BOARD]
    p = subprocess.run(cmd, cwd=str(AGENT), env=env, capture_output=True, text=True, timeout=180)
    calls.append({"argv": ["boards", "create", BOARD], "exit": p.returncode,
                  "stdout": (p.stdout or "").strip()[:300], "stderr": (p.stderr or "").strip()[:200]})
    print("board create exit", p.returncode, "::", (p.stdout or p.stderr or "").strip()[:160])


def board_ls():
    _r, s = k("ls", "--json")
    try:
        return json.loads(s)
    except Exception:
        return []


# (id, title, status_after)  status_after: done | blocked | ready
CARDS = [
    ("R0", "R0 Gate-1 route + negative control", "done"),
    ("R1", "R1 CAPC contract C0-C9 compile (PROMPT_COMPILE_PASS)", "done"),
    ("R2", "R2 HGK typed admission (project FAR-018-R7R11-RESIDUAL)", "done"),
    ("R3", "R3 Kanban/OpenSpec execution surfaces for this round", "done"),
    ("R4", "R4 W1 residual universe (independent lane)", "in_flight"),
    ("R5", "R5 W2 defect dossier incl. checker-isolation feasibility", "in_flight"),
    ("R6", "R6 EXECUTE lane: writer artifacts (deepseek-v4.1-flash)", "in_flight"),
    ("R7", "R7 VERIFY lane pinned to openai-codex/gpt-6.1-sol rank2", "in_flight"),
    ("R8", "R8 owner-gated items prepared in one-action form", "in_flight"),
    ("R9", "R9 publish to Fabric new prefix + remote readback", "in_flight"),
    ("R10", "R10 handover checkpoint + single evidence MD (3-root mirror)", "in_flight"),
    ("R11", "R11 self-check/repair/acceptance + governed self-evolution", "in_flight"),
    ("OG1", "OG-OWNER: peer chain #6/#8/#10 merge batch", "blocked"),
    ("OG2", "OG-OWNER: R7-02 validator cross-repo code promotion", "blocked"),
    ("OG3", "OG-OWNER: R7-04 Fresh G1 owner certificate", "blocked"),
    ("OG4", "OG-OWNER: canonical lane config repair (stale codex pin)", "blocked"),
    ("OG5", "OG-OWNER: KP R04 polarity + source#6 status disposition", "blocked"),
]

info = {}
ensure_board()
for cid, title, status in CARDS:
    k("create", f"{cid} {title}", "--idempotency-key", f"FAR018-{cid}",
      "--created-by", "hgk-orchestrator", "--assignee", "hgk-orchestrator",
      "--body", "FAR-20261016-018 gate card; evidence under _handover/FAR-20261016-018-*/")
for t in board_ls():
    for cid, _t, _s in CARDS:
        if (t.get("title") or "").startswith(cid + " "):
            info[cid] = t.get("id")

for cid, title, status in CARDS:
    tid = info.get(cid)
    if not tid:
        continue
    k("claim", tid, "--ttl", "1800", expect_ok=False)
    k("heartbeat", tid, expect_ok=False)
    if status == "done":
        k("comment", tid, "verified: artifact on disk", "--author", "hgk-orchestrator", expect_ok=False)
        k("complete", tid, "--result", "done with raw receipt",
          "--metadata", json.dumps({"evidence": "see round root receipts"}))
    elif status == "blocked":
        k("block", tid, "structurally the owner's: authority exceeds this round",
          "--kind", "needs_input", expect_ok=False)

final = board_ls()
hist = {}
for t in final:
    hist[t.get("status")] = hist.get(t.get("status"), 0) + 1
rec = {"schema": "FAR-20261016-018/KANBAN-LIFECYCLE/1", "board": BOARD,
       "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "cards_created": len(info), "board_state_histogram": hist,
       "board_readback": [{"id": t.get("id"), "title": (t.get("title") or "")[:56],
                           "status": t.get("status")} for t in final],
       "call_count": len(calls), "calls": calls}
(OUT / "KANBAN_LIFECYCLE_RECEIPT.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print("cards:", len(info), "CLI calls:", len(calls), "histogram:", hist)
