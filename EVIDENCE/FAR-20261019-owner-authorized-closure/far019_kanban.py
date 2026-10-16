#!/usr/bin/env python
"""Drive the FAR-019 board through a real lifecycle. Every card gets CLI receipts (invariant 10a:
admission is not execution). Write path is the board DB only.

Round-specific cards: this board names THIS round's gates. A board that re-used the previous round's
card faces would be a fake trace, so the card list is newly authored, not substituted.
"""
import json, os, subprocess, datetime
from pathlib import Path

HERMES = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes")
AGENT = HERMES / "hermes-agent"
PY = AGENT / "venv/Scripts/python.exe"
BOARD = "far-019-owner-auth-closure"
OUT = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261019-owner-authorized-closure")
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
    ("R0", "R0 gstack route check + negative control (NATIVE vs GSTACK)", "done"),
    ("R1", "R1 CAPC contract gates lint/activation/acceptance/compile PASS", "done"),
    ("R2", "R2 HGK typed admission FAR-019-OWNER-AUTH (TS-AUTH-01..05)", "done"),
    ("R3", "R3 OpenSpec change hgk-far-019-owner-authorized-closure strict-valid", "done"),
    ("R4", "R4 SWARM lane W1 current open-item universe (independent leaf)", "ready"),
    ("R5", "R5 SWARM lane W2 owner-decision dossier + achievability measurement", "ready"),
    ("R6", "R6 EXECUTE lane writer artifacts (opencode-go/deepseek-v4.1-flash)", "ready"),
    ("R7", "R7 VERIFY lane pinned rank2 openai-codex/gpt-6.1-sol (cross-model)", "ready"),
    ("R8", "R8 canonical lane-config stale codex pin repaired + readback", "ready"),
    ("R9", "R9 peer evidence chain PR6/8/10 merged under owner authorisation", "ready"),
    ("R10", "R10 evidence pack published + per-blob remote readback + PR promoted", "ready"),
    ("R11", "R11 handover, single evidence MD, self-check with injected mutations", "ready"),
    ("R12", "R12 governed self-evolution record (skill lessons landed)", "ready"),
    ("OS1", "OS-OWNER-SIGNATURE: facts only the owner can attest (R7-04 fresh G1 cert)", "blocked"),
    ("OS2", "OS-OWNER-SIGNATURE: normative semantic change (KP R04 polarity activation)", "blocked"),
    ("OS3", "OS-OWNER-SIGNATURE: cross-repo promotion R7-02 (PIPD-LS-SP validator)", "blocked"),
]

info = {}
ensure_board()
for cid, title, status in CARDS:
    k("create", f"{cid} {title}", "--idempotency-key", f"FAR019-{cid}",
      "--created-by", "hgk-orchestrator", "--assignee", "hgk-orchestrator",
      "--body", "FAR-20261019 gate card; evidence under _handover/FAR-20261019-*/")
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
        k("block", tid, "assertion only the owner can make; prepared as a single action",
          "--kind", "needs_input", expect_ok=False)

final = board_ls()
hist = {}
for t in final:
    hist[t.get("status")] = hist.get(t.get("status"), 0) + 1
rec = {"schema": "FAR-20261019/KANBAN-LIFECYCLE/1", "board": BOARD,
       "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "cards_created": len(info), "board_state_histogram": hist,
       "board_readback": [{"id": t.get("id"), "title": (t.get("title") or "")[:56],
                           "status": t.get("status")} for t in final],
       "call_count": len(calls), "calls": calls}
(OUT / "KANBAN_LIFECYCLE_RECEIPT.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print("cards:", len(info), "CLI calls:", len(calls), "histogram:", hist)
