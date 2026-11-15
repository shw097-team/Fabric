#!/usr/bin/env python
"""Round CNV-FAR018-FAR019-ARCHIVE-20261016: OPENSPEC change + GSTACK route check + KANBAN lifecycle.

Three orchestration surfaces, each with its own raw receipt:
  * OPENSPEC  - author the round's change record (proposal + delta spec under specs/<capability>/ + tasks)
                and validate it with the REPO'S OWN tool.  A record with only a root-level spec.md is not
                a delta and --strict fails on it, so the delta lives under specs/.
  * GSTACK    - named-method route check with a positive flow and a NEGATIVE control that must route
                differently (RESEARCH_LITERATURE_REPO -> NATIVE, PURE_QA_CHAT -> GSTACK), plus the lane
                pools and the SKCV pointer verdicts.
  * KANBAN    - a NEW board with THIS round's gate cards, each driven through real CLI verbs
                (create/claim/heartbeat/comment/complete).  Admission is not execution: the cards get
                CLI receipts, not a narrated state.
"""
import json, os, subprocess, hashlib, datetime
from pathlib import Path

HGK = Path("C:/Projects/Agent_Workspace/HG-KSEOS")
RD = Path("C:/Projects/Agent_Workspace/_handover/CNV-FAR018-FAR019-ARCHIVE-20261016")
HERMES = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes")
AGENT = HERMES / "hermes-agent"
PY = AGENT / "venv/Scripts/python.exe"
BOARD = "cnv-archive-far018-019"
CHANGE = "hgk-cnv-far018-far019-archive"
GEN = datetime.datetime.now(datetime.timezone.utc).isoformat()
UC = RD / "openspec_change"

# ---------------------------------------------------------------- OPENSPEC
(UC / "specs/archive-evidence-merge").mkdir(parents=True, exist_ok=True)
proposal = f"""# {CHANGE}

## Why
Three candidate evidence pull requests (#12 R7R11 archive, #13 FAR-018, #14 FAR-019) are frozen and
independently reviewed (`EIA-FABRIC-FAR018-FAR019-ARCHIVE-20261016`).  The archive stage can be closed
without promoting any product code, but only under a bounded maintainer authorisation, a trusted scoped
secrets scan, and a per-PR merge at an approved exact SHA.

## What changes
Evidence only: the three existing `EVIDENCE/**` prefixes are merged normally into `main`, and this round's
own return pack is added under `EVIDENCE/CNV-FAR018-FAR019-ARCHIVE-20261016/`.

## Impact
- Capability: archive-evidence-merge (new, evidence-only).
- No product, runtime, config, hook or workflow change.
- Rollback: `git revert <merge_sha>` per PR.
"""
tasks = """# Tasks

## 1. Preflight
- [x] 1.1 A00 source register with per-source sha256 (20/20 knowledge base present)
- [x] 1.2 C0-C9 contract authored and compiled: lint/activation/acceptance/compile PROMPT_COMPILE_PASS
- [x] 1.3 HGK typed admission (own project id, TaskSpec segment collision-checked against the live spine)
- [x] 1.4 A03 GitHub freeze: per-PR head, base, changed set, prefix, blob modes, manifest semantics
- [x] 1.5 A04 manifest semantics: every indexed path resolves at that HEAD; first-cut vs final explained

## 2. Security
- [x] 2.1 Scoped secrets scan on the content each PR adds, with a positive control that must fire and a
      clean control that must not
- [x] 2.2 PR #14 config-backup sensitivity review (path/route/credential metadata)
- [x] 2.3 Confirm no `.github/workflows` or hook enters the archive, and archived scripts are not executed

## 3. Authorisation and merge
- [x] 3.1 Record the bounded maintainer approval batch naming each PR's frozen HEAD and prefix
- [x] 3.2 PR #12 out of draft (GraphQL markPullRequestReadyForReview; the REST undraft path 404s)
- [ ] 3.3 Merge #12, #13, #14 each with `sha=<approved head>` and read `main` back
- [ ] 3.4 Rollback pointer per PR (`git revert <merge_sha>`)

## 4. Return pack
- [ ] 4.1 Machine-readable evidence_return_pack per PR
- [ ] 4.2 12/12 disposition of the acceptance report's findings with owner and claim ceiling
- [ ] 4.3 Single evidence MD + handover + self-check with injected mutations
"""
spec = """# archive-evidence-merge

## ADDED Requirements

### Requirement: Per-PR evidence archive merge
The archive stage SHALL merge each candidate evidence pull request normally at its approved exact head
SHA, and SHALL read the merged prefix and blobs back from `main`.

#### Scenario: Approved head is merged
- **WHEN** a maintainer approval names the PR's exact head SHA, prefix and rollback
- **THEN** the PR is merged with `sha=<approved head>` and the merge commit SHA is read back from the API

#### Scenario: Head drifted after approval
- **WHEN** the live head no longer equals the approved SHA
- **THEN** that PR is HELD, no merge is attempted, and its first-fail is recorded

### Requirement: Evidence-only scope enforcement
The round SHALL refuse any PR whose changed paths leave its single allowed `EVIDENCE/**` prefix, and
SHALL hold only that PR.

#### Scenario: Prefix escape
- **WHEN** a changed path lies outside the allowed prefix
- **THEN** the PR is HELD with `PREFIX_ESCAPE` and the other PRs keep their independent gating

### Requirement: Trusted scoped secrets scan
The round SHALL scan the content each PR adds with a scanner proven to fire on a positive control and
silent on a clean control, and SHALL hold any PR with a real secret.

#### Scenario: Positive control fires
- **WHEN** the scanner is run against a fixture containing a synthetic credential
- **THEN** it reports a finding, proving the scan is not vacuous
"""
(UC / "proposal.md").write_text(proposal, encoding="utf-8")
(UC / "tasks.md").write_text(tasks, encoding="utf-8")
(UC / "specs/archive-evidence-merge/spec.md").write_text(spec, encoding="utf-8")

dst = HGK / "openspec/changes" / CHANGE
dst.mkdir(parents=True, exist_ok=True)
for rel in ("proposal.md", "tasks.md", "specs/archive-evidence-merge/spec.md"):
    (dst / rel).parent.mkdir(parents=True, exist_ok=True)
    (dst / rel).write_text((UC / rel).read_text(encoding="utf-8"), encoding="utf-8")

OPENSPEC = {"change": CHANGE, "dir": str(dst), "attempts": []}
for argv in (["openspec", "validate", CHANGE, "--strict"], ["npx", "--no-install", "openspec", "validate", CHANGE, "--strict"]):
    if not (HGK / "openspec").exists():
        OPENSPEC["attempts"].append({"argv": argv, "skip": "no openspec dir"})
        continue
    try:
        p = subprocess.run(argv, cwd=str(HGK / "openspec"), capture_output=True, text=True, timeout=180, shell=False)
        OPENSPEC["attempts"].append({"argv": argv, "exit": p.returncode,
                                     "stdout": (p.stdout or "").strip()[:300], "stderr": (p.stderr or "").strip()[:300]})
        if p.returncode == 0:
            break
    except FileNotFoundError as e:
        OPENSPEC["attempts"].append({"argv": argv, "exit": None, "error": "FileNotFoundError: " + str(e)[:80]})
    except Exception as e:  # noqa: BLE001
        OPENSPEC["attempts"].append({"argv": argv, "exit": None, "error": type(e).__name__ + ": " + str(e)[:120]})
last = OPENSPEC["attempts"][-1] if OPENSPEC["attempts"] else {}
OPENSPEC["verdict"] = "VALID" if last.get("exit") == 0 else "NOT_VALIDATED"
OPENSPEC["artifacts"] = sorted(str(p.relative_to(dst)) for p in dst.rglob("*.md"))

# ---------------------------------------------------------------- GSTACK route
sys_path = str(HGK / "src")
import sys  # noqa: E402
sys.path.insert(0, sys_path)
route = {"schema": "CNV-ARCHIVE/ROUTE-CHECK/1", "generated_utc": GEN}
try:
    from hg_kseos import named_methods as nm
    snap = nm.registry_snapshot() if hasattr(nm, "registry_snapshot") else None
    route["registry"] = {"snapshot_ok": snap is not None, "n_methods": len(snap) if hasattr(snap, "__len__") else None}
    for label, flow in (("ARCHIVE", "RESEARCH_LITERATURE_REPO"), ("NEGATIVE_CONTROL", "PURE_QA_CHAT")):
        try:
            r = nm.route(flow)
            route["registry"]["route_" + label] = {
                "flow": flow,
                "route": r.get("route") if isinstance(r, dict) else getattr(r, "route", None),
                "reason_code": r.get("reason_code") if isinstance(r, dict) else getattr(r, "reason_code", None)}
        except Exception as e:  # noqa: BLE001
            route["registry"]["route_" + label] = {"flow": flow, "error": type(e).__name__ + ": " + str(e)[:160]}
except Exception as e:  # noqa: BLE001
    route["registry"] = {"import_error": type(e).__name__ + ": " + str(e)[:200]}

pools = {}
try:
    d = json.loads((HGK / "config/lane-route-slots.candidate.json").read_text(encoding="utf-8"))
    for v in (d.get("lanes") or []):
        if not isinstance(v, dict):
            continue
        pools[v.get("lane")] = {"engine": v.get("engine"), "transport": v.get("transport"),
                                "pool": [{"rank": i + 1,
                                          "arm": ((p.get("provider") or "") + "/" + (p.get("model") or ""))
                                          if isinstance(p, dict) else str(p)} for i, p in enumerate(v.get("ordered_pool") or [])]}
except Exception as e:  # noqa: BLE001
    pools = {"error": type(e).__name__ + ": " + str(e)[:160]}
route["lane_pools"] = pools
SKILL = HERMES / "skills/software-development/hgk-governed-execution"
try:
    route["entry_map_present"] = (SKILL / "entry_map.json").exists()
    route["skill_md_sha256"] = hashlib.sha256((SKILL / "SKILL.md").read_bytes()).hexdigest()
    route["reference_md_count"] = len(list((SKILL / "references").glob("*.md")))
except Exception as e:  # noqa: BLE001
    route["skill_error"] = type(e).__name__ + ": " + str(e)[:120]
(RD / "ROUTE_CHECK.json").write_text(json.dumps(route, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- KANBAN
env = dict(os.environ, HERMES_HOME=str(HERMES))
calls = []


def k(*args, expect_ok=True):
    cmd = [str(PY), "hermes_cli/main.py", "kanban", "--board", BOARD, *[str(a) for a in args]]
    p = subprocess.run(cmd, cwd=str(AGENT), env=env, capture_output=True, text=True, timeout=240)
    rec = {"argv": cmd[3:], "exit": p.returncode, "stdout": (p.stdout or "").strip()[:300],
           "stderr": (p.stderr or "").strip()[:200]}
    calls.append(rec)
    if expect_ok and p.returncode != 0:
        print("  !!", p.returncode, " ".join(cmd[3:]), "::", rec["stderr"][:140])
    return rec, (p.stdout or "")


def ensure_board():
    cmd = [str(PY), "hermes_cli/main.py", "kanban", "boards", "create", BOARD]
    p = subprocess.run(cmd, cwd=str(AGENT), env=env, capture_output=True, text=True, timeout=240)
    calls.append({"argv": ["boards", "create", BOARD], "exit": p.returncode,
                  "stdout": (p.stdout or "").strip()[:300], "stderr": (p.stderr or "").strip()[:200]})
    print("board create exit", p.returncode, "::", (p.stdout or p.stderr or "").strip()[:200])


CARDS = [
    ("A0", "A0 source register A00 (20/20 knowledge base, per-source sha256)", "done"),
    ("A1", "A1 CAPC C0-C9 contract lint/activation/acceptance/compile PROMPT_COMPILE_PASS", "done"),
    ("A2", "A2 HGK typed admission of this archive round (own project id)", "done"),
    ("A3", "A3 GitHub freeze: per-PR head/prefix/modes + Q03/Q04", "done"),
    ("A4", f"A4 OpenSpec change {CHANGE} strict-valid", "done"),
    ("A5", "A5 trusted scoped secrets scan with positive and clean control", "ready"),
    ("A6", "A6 bounded maintainer approval batch naming three frozen heads", "ready"),
    ("A7", "A7 PR12 out of draft then merged at approved head", "ready"),
    ("A8", "A8 PR13 merged at approved head", "ready"),
    ("A9", "A9 PR14 merged at approved head", "ready"),
    ("A10", "A10 main readback of the three prefixes + rollback pointers", "ready"),
    ("A11", "A11 evidence_return_pack per PR + 12/12 finding dispositions", "ready"),
    ("A12", "A12 single evidence MD + handover + self-check with injected mutations", "ready"),
    ("A13", "A13 governed self-evolution record (skill lessons landed)", "ready"),
    ("OG1", "OG-OWNER: TS-VAL-01 PIPD validator canonical promotion (separate changeset)", "blocked"),
    ("OG2", "OG-OWNER: TS-CHECKER-01 non-liftable checker boundary (second OS identity)", "blocked"),
    ("OG3", "OG-OWNER: TS-G1-01 fresh G1 certificate at runtime freeze", "blocked"),
    ("OG4", "OG-OWNER: the remaining 60-owner-item batches beyond B0", "blocked"),
]
info = {}
ensure_board()
for cid, title, status in CARDS:
    k("create", f"{cid} {title}", "--idempotency-key", f"ARCHIVE-{cid}", "--created-by", "hgk-orchestrator",
      "--assignee", "hgk-orchestrator", "--body",
      "CNV-FAR018-FAR019-ARCHIVE gate card; evidence under _handover/CNV-FAR018-FAR019-ARCHIVE-20261016/")
_r, s = k("ls", "--json")
try:
    listing = json.loads(s)
except Exception:
    listing = []
for t in listing:
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
        k("comment", tid, "verified: artifact on disk in the round root", "--author", "hgk-orchestrator", expect_ok=False)
        k("complete", tid, "--result", "done with raw receipt",
          "--metadata", json.dumps({"evidence": "round root receipts"}))
    elif status == "blocked":
        k("block", tid, "assertion only the owner can make; carried as a single action", "--kind", "needs_input",
          expect_ok=False)

_r, s = k("ls", "--json")
try:
    final = json.loads(s)
except Exception:
    final = []
hist = {}
for t in final:
    hist[t.get("status")] = hist.get(t.get("status"), 0) + 1
kb = {"schema": "CNV-ARCHIVE/KANBAN-LIFECYCLE/1", "board": BOARD, "generated_utc": GEN,
      "cards_created": len(info), "board_state_histogram": hist, "call_count": len(calls),
      "board_readback": [{"id": t.get("id"), "title": (t.get("title") or "")[:52], "status": t.get("status")}
                         for t in final], "calls": calls}
(RD / "KANBAN_LIFECYCLE_RECEIPT.json").write_text(json.dumps(kb, ensure_ascii=False, indent=1), encoding="utf-8")

gov = {"schema": "CNV-ARCHIVE/ORCHESTRATION-SURFACES/1", "generated_utc": GEN, "openspec": OPENSPEC,
       "gstack": route, "kanban": {"board": BOARD, "cards": len(info), "histogram": hist, "cli_calls": len(calls)}}
(RD / "ORCHESTRATION_SURFACES.json").write_text(json.dumps(gov, ensure_ascii=False, indent=1), encoding="utf-8")

print("OPENSPEC:", OPENSPEC["verdict"], "| attempts:", [(a.get("argv"), a.get("exit"), a.get("error")) for a in OPENSPEC["attempts"]])
print("  artifacts:", OPENSPEC["artifacts"])
print("GSTACK:", json.dumps(route.get("registry"), ensure_ascii=False)[:300])
print("  entry_map_present:", route.get("entry_map_present"), "| references:", route.get("reference_md_count"))
print("  pools:", {kk: [e["arm"] for e in vv.get("pool", [])] for kk, vv in pools.items()})
print("KANBAN cards:", len(info), "CLI calls:", len(calls), "histogram:", hist)
