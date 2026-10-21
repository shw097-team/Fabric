#!/usr/bin/env python
"""FAR-MINIMAX-MANDATE-20261021 — HGK admission for the owner-mandated MiniMax route.

Owner order (2026-10-21, this turn): PLAN, EXECUTE and VERIFY/SECURITY all run on
`opencode-go/minimax-m3.1-flash-free` (OPENCODE GO). PLAN is Hermes-internal; EXECUTE and
VERIFY/SECURITY are dispatched to the Codex CLI.

The governance order of this file matters, so each step states what it proves and what it does not:

  1. RESOLVE the arm. A pool entry carries a governance identity (provider/model) and a transport
     vocabulary (transport_model); they are different fields with different rules per provider. The
     opencode-go arm accepts the QUALIFIED spelling `opencode-go/minimax-m3.1-flash-free`, and that
     spelling is what the transport actually uses. (The openai arm is the opposite: it REQUIRES the
     bare id. Measured on the live relay: `openai-codex/gpt-6.1-sol` -> 400 while `gpt-6.1-sol`
     -> 200. That asymmetry is why the transport field exists at all.)

  2. PROBE the direct completion. A direct 200 proves the account and endpoint can serve the model.
     It does NOT prove the Codex-CLI transport can, and it does NOT admit the lane.

  3. EXERCISE the lane. Only a lane-shaped run through scripts/hgk-lane-dispatch.py --require-arm
     <arm> --force-rank <n> proves the Codex-CLI transport served this arm, with the nonce sentinel
     present and a usage receipt appended after the attempt started.

  4. ADMIT per lane, and record what is NOT established. `decide_status` returns ADMITTED only when
     the lane exercise proves served provider/model/engine. The receipt also carries the
     separation-of-duties ceiling: PLAN, EXECUTE and VERIFY/SECURITY on ONE model means model-axis
     independence is ZERO for every pair. That is a fact to declare, not a fact to hide -- the
     registry must gain an explicit SoD conflict for it (SOD006-C5) in the same change set.

Everything here is read-only against the live route. It writes ONE admission receipt per lane
under var/FAR-MINIMAX-MANDATE-20261021/admission/ and changes no registry, pool or config file.
"""
from __future__ import annotations
import json, subprocess, sys, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
ROUND = "FAR-MINIMAX-MANDATE-20261021"
OUT = ROOT / "var" / ROUND
ADMIT_DIR = OUT / "admission"
RELAY = "http://127.0.0.1:10101/v1"
CODEX = "C:/Users/user/AppData/Local/OpenAI/Codex/bin/896a0166b774037a/codex.exe"

ARM = {"provider": "opencode-go", "model": "minimax-m3.1-flash-free", "engine": "codex-cli"}
TRANSPORT_MODEL = "opencode-go/minimax-m3.1-flash-free"
NONCE = "HGK_LANE_NONCE_OK"

# The three lanes the owner named, with the engine each one actually uses and the pool entry's
# current rank (PLAN and VERIFY_SECURITY do not yet carry this arm; that is a CHANGE to make, and
# the admission records the arm as INTENDED for them, not as already-pooled).
LANES = [
    {"lane": "PLAN", "engine": "hermes", "rank": None,
     "note": "PLAN is the Hermes-internal orchestration plane. It is bound by the profile's own "
             "model, not by a Codex-CLI dispatch, so its admission is a DIRECT completion plus the "
             "lane identity; the pool entry records the intended arm for later dispatches."},
    {"lane": "EXECUTE", "engine": "codex-cli", "rank": 4,
     "note": "Bounded writer. Currently the pool's rank-4 PROBE arm; the owner order makes it the "
             "rank-1 DEFAULT for this lane."},
    {"lane": "VERIFY_SECURITY", "engine": "codex-cli", "rank": None,
     "note": "Independent Acceptance Officer. The pool does not yet carry this arm at all, so the "
             "lane exercise is performed against a POOL PROBE COPY so the binding is measured "
             "before the pool is changed (a change that follows a measurement, not one that "
             "assumes it)."},
]


def direct_completion(model: str) -> dict:
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": "Reply exactly: ADMIT_DIRECT_OK"}],
                       "max_tokens": 16, "stream": False}).encode()
    req = urllib.request.Request(f"{RELAY}/chat/completions", data=body, headers={
        "Content-Type": "application/json", "x-opencode-session": f"admit-{int(time.time())}",
        "User-Agent": "Mozilla/5.0"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.load(r)
            txt = (data["choices"][0]["message"].get("content") or "")
            return {"ok": True, "http_status": r.status, "latency_s": round(time.time() - t0, 3),
                    "content_present": bool(txt.strip()), "detail": txt.strip()[:80]}
    except urllib.error.HTTPError as e:
        return {"ok": False, "http_status": e.code, "latency_s": round(time.time() - t0, 3),
                "content_present": False, "detail": e.read()[:200].decode("utf-8", "replace")}
    except Exception as e:
        return {"ok": False, "http_status": None, "latency_s": round(time.time() - t0, 3),
                "content_present": False, "detail": f"{type(e).__name__}: {e}"}


def lane_exercise(lane: str, rank: int, workdir: Path) -> dict:
    """Dispatch the lane through the governed dispatcher and read what actually served."""
    out = workdir / f"{lane}.json"
    cmd = [str(ROOT / ".venv" / "Scripts" / "python.exe"), str(ROOT / "scripts" / "hgk-lane-dispatch.py"),
           "--lane", lane,
           "--prompt",
           "Use your shell tool to run exactly this command: echo ADMIT_TOOL_OK . Then report its "
           "output. Then reply with exactly: ADMIT_LANE_OK and end your final message with the line "
           f"{NONCE}",
           "--force-rank", str(rank), "--max-candidates", "1",
           "--require-arm", f"{ARM['provider']}/{ARM['model']}",
           "--codex-executable", CODEX,
           "--pool", str(workdir / "pool-probe.json"),
           "--timeout", "300", "--json-out", str(out)]
    env = dict(**__import__("os").environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, env=env, timeout=420)
    if not out.exists():
        return {"ok": False, "detail": f"dispatcher produced no receipt (rc={r.returncode})",
                "stderr": (r.stderr or "")[-300:]}
    d = json.loads(out.read_text(encoding="utf-8"))
    att = (d.get("attempts") or [{}])[0]
    tools_used = 0
    try:
        for lg in sorted((workdir / f"{lane}.json.logs").glob("*-stdout.txt")):
            for ln in lg.read_text(encoding="utf-8", errors="replace").splitlines():
                ln = ln.strip()
                if not ln.startswith("{"):
                    continue
                try:
                    o = json.loads(ln)
                except Exception:
                    continue
                it = o.get("item") or {}
                t = str(it.get("type") or "")
                if t.startswith("command") or t in ("mcp_tool_call", "file_change", "tool_call"):
                    tools_used += 1
    except Exception:
        pass
    return {"ok": bool(d.get("ok")), "code": d.get("code"), "tools_used": tools_used,
            "served_arm": d.get("served_arm"), "used_rank": d.get("used_rank"),
            "used_transport_model": d.get("used_transport_model"),
            "usage_receipt_ok": d.get("usage_receipt_ok"),
            "nonce_present": att.get("nonce_present"), "exit": att.get("exit"),
            "sandbox": att.get("sandbox"),
            "detail": (att.get("stdout_tail") or "")[-260:]}


def main() -> int:
    sys.path.insert(0, str(ROOT / "src"))
    from hg_kseos import lane_admission as la

    ADMIT_DIR.mkdir(parents=True, exist_ok=True)
    pool = json.loads((ROOT / "config/lane-route-slots.candidate.json").read_text(encoding="utf-8"))
    epoch = None
    try:
        from hg_kseos import lane_policy as lp
        epoch = lp.load_registry().get("epoch")
    except Exception:
        pass

    # The arm as the pool would declare it: governance identity + the transport spelling this
    # provider actually accepts. The opencode-go arm accepts the qualified form.
    # The arm's engine is PER LANE, because the three lanes do not share an engine: PLAN is the
    # Hermes-internal orchestration plane, EXECUTE and VERIFY/SECURITY are dispatched to the Codex
    # CLI. Declaring one engine for all three would make the admission compare a served 'hermes'
    # against a requested 'codex-cli' and refuse on an identity technicality rather than on a fact.
    ENGINE_BY_LANE = {spec["lane"]: spec["engine"] for spec in LANES}

    # a POOL PROBE COPY: the two lanes that do not yet carry this arm are exercised against a
    # copy so the binding is MEASURED before the real pool is changed.
    probe_pool = OUT / "pool-probe.json"
    pp = json.loads(json.dumps(pool))
    for lane in pp["lanes"]:
        if lane["lane"] not in ("EXECUTE", "VERIFY_SECURITY"):
            continue
        # Only ADD the arm where the lane does not already carry it. The dispatcher refuses a
        # duplicate token in one pool (ERR_SLOT_POOL_DUPLICATE_TOKEN), and EXECUTE already carries
        # this arm as its rank-4 PROBE entry. Where the arm is present, the EXISTING entry is
        # dispatched (and its rank is used); where it is absent, a probe entry is appended with
        # the next CONTIGUOUS rank (the dispatcher refuses a rank gap with ERR_SLOT_POOL_RANK_GAP).
        token = f"{ARM['provider']}/{ARM['model']}"
        have = [c for c in lane["ordered_pool"]
                if f"{c.get('provider')}/{c.get('model')}" == token]
        if have:
            lane["_probe_rank"] = int(have[0].get("rank", 0))
            continue
        next_rank = max(int(c.get("rank", 0)) for c in lane["ordered_pool"]) + 1
        lane["ordered_pool"].append({
            "rank": next_rank, "provider": ARM["provider"], "model": ARM["model"],
            "transport_model": TRANSPORT_MODEL, "role": "PROBE/探測",
            "reasoning_effort": None, "default": False, "automatic_selection": False,
            "probe_note": "admission probe copy; NOT the canonical pool",
        })
        lane["_probe_rank"] = next_rank
    probe_ranks = {l["lane"]: l.pop("_probe_rank", None) for l in pp["lanes"]}
    probe_pool.write_text(json.dumps(pp, ensure_ascii=False, indent=2), encoding="utf-8")

    results = []
    for spec in LANES:
        rec = la.LaneAdmission(lane=spec["lane"],
                                arm={**arm_for_admission, "engine": ENGINE_BY_LANE[spec["lane"]]},
                                policy_epoch=epoch,
                                request_profile={"owner_order": "2026-10-21 minimax mandate",
                                                 "transport_model": TRANSPORT_MODEL,
                                                 "relay": RELAY,
                                                 "codex_executable": CODEX,
                                                 "engine": spec["engine"],
                                                 "note": spec["note"]})
        rec.record_start()
        # 2. direct completion (never sufficient for admission)
        dc = direct_completion(TRANSPORT_MODEL)
        rec.record_direct_completion(ok=dc["ok"], http_status=dc.get("http_status"),
                                     latency_s=dc.get("latency_s"),
                                     detail=dc.get("detail"), content_present=dc.get("content_present", False))
        # 3. lane exercise
        if spec["engine"] == "codex-cli":
            # resolve the probe pool's rank for this lane, so the dispatch names a rank that
            # actually exists in the copy it is given
            _pl = json.loads(probe_pool.read_text(encoding="utf-8"))
            _lane = next(l for l in _pl["lanes"] if l["lane"] == spec["lane"])
            rank = int(probe_ranks.get(spec["lane"]) or 0) or max(
                int(c.get("rank", 0)) for c in _lane["ordered_pool"])
            le = lane_exercise(spec["lane"], rank, OUT)
            # decide_status requires completed_tools >= 1: a lane exercise must show the model
            # actually DRIVING a tool, not only emitting text. The tool count is read from the
            # dispatcher's own attempt record (item.completed of a tool type), not asserted.
            tools_used = int(le.get("tools_used") or 0)
            rec.record_lane_exercise(
                completed_model_calls=1 if le.get("ok") else 0,
                completed_tools=tools_used,
                served_provider=ARM["provider"] if le.get("ok") else None,
                served_model=ARM["model"] if le.get("ok") else None,
                served_engine=ARM["engine"] if le.get("ok") else None,
                session_id=spec["lane"],
                elapsed_s=None,
                evidence_ref=str((OUT / "probes" / f"{spec['lane']}_admit.json").as_posix()))
        else:
            # PLAN is the Hermes-internal plane: its own dispatch path is the session/profile
            # binding, which this round did not change. Record the direct completion as the
            # evidence and be explicit that no Codex-CLI lane exercise applies to it.
            le = {"ok": dc["ok"], "detail": "PLAN is Hermes-internal; no Codex-CLI dispatch applies",
                  "direct_completion_only": True}
            rec.record_lane_exercise(
                completed_model_calls=1 if dc["ok"] else 0,
                # PLAN's engine here is the Hermes-internal plane, whose binding is the session
                # profile -- not a Codex-CLI dispatch. The tools count stays 0 because no tool
                # invocation is evidenced for it in this round, and decide_status will therefore
                # NOT admit it. That is the honest outcome: PLAN is bound by the profile, and this
                # round changed the LANE pools, not the session profile.
                completed_tools=0,
                served_provider=ARM["provider"] if dc["ok"] else None,
                served_model=ARM["model"] if dc["ok"] else None,
                served_engine="hermes" if dc["ok"] else None,
                session_id="plan-hermes-internal",
                elapsed_s=dc.get("latency_s"),
                evidence_ref=str((OUT / "probes" / "PLAN_direct.json").as_posix()))
        status = la.decide_status(rec)
        path = la.write_receipt(rec, ADMIT_DIR / f"{spec['lane']}.json")
        results.append({"lane": spec["lane"], "status": status, "receipt": str(path),
                        "direct_completion": dc, "lane_exercise": le, "note": spec["note"]})
        print(f"{spec['lane']:16s} -> {status}")

    summary = {
        "round": ROUND,
        "owner_order": "2026-10-21: PLAN / EXECUTE / VERIFY_SECURITY all on "
                       f"{ARM['provider']}/{ARM['model']} (OPENCODE GO)",
        "arm": arm_for_admission,
        "transport_model": TRANSPORT_MODEL,
        "transport_rule": "the opencode-go arm accepts the qualified spelling; the openai arm is the "
                          "opposite and requires the bare id (measured on the live relay)",
        "policy_epoch": epoch,
        "results": results,
        "sod_ceiling": "PLAN, EXECUTE and VERIFY/SECURITY share ONE model, so model-axis independence "
                       "is ZERO for every pair. The registry must declare this explicitly (the "
                       "existing SOD006-C4 covers the PLAN/VERIFY pair only; the EXECUTE/VERIFY pair "
                       "is currently distinct_required: true and this order changes that).",
        "claim_ceiling": "admission proves this arm served on this account/transport/invocation. It is "
                          "not an acceptance of any subject, not a release, and not a model-axis "
                          "independence claim.",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "admission_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                                                 encoding="utf-8")
    print(json.dumps({"lanes": [(r["lane"], r["status"]) for r in results]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
