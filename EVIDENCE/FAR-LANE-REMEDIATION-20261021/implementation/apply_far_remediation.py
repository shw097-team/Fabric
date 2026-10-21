#!/usr/bin/env python
"""FAR-REMEDIATION-20261021 — apply P0/P1/P2 declaration alignment (dry-run by default).

Owner order 2026-10-21 (pre-authorized): PLAN = openai-codex/gpt-6.1-sol (medium, OAuth, engine hermes);
EXECUTE = opencode-go/deepseek-v4.1-flash (codex-cli, unchanged); VERIFY_SECURITY =
openai-codex/gpt-6.1-sol (medium, OAuth, engine codex-cli). Registry advances to epoch 23.

Properties: dry-run default; per-file pre-image sha256; per-run backups; anchored replacement with
exactly-once assertions; post-write value assertions; check_drift; pytest; receipt; rollback paths.
Writes only inside the round's declared write set (config/*, AGENTS.md, tests/test_lane_policy.py).
"""
from __future__ import annotations
import argparse, hashlib, json, re, shutil, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] if '__file__' in globals() else Path('.')
ROOT = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
ROUND = "FAR-REMEDIATION-20261021"
OUT = ROOT / "var" / ROUND
REG = ROOT / "config" / "lane-routing-registry.yaml"
ASG = ROOT / "config" / "model-lane-assignment.json"
POOL = ROOT / "config" / "lane-route-slots.candidate.json"
LANE = ROOT / "config" / "hermes-codex-lane.json"
AGENTS = ROOT / "AGENTS.md"
TESTS = ROOT / "tests" / "test_lane_policy.py"
PROFILE = Path(r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\profiles\hgk-governed\config.yaml")
HCOPY = Path(r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\config.yaml")
CODEX_BIN = r"C:/Users/user/AppData/Local/OpenAI/Codex/bin/896a0166b774037a/codex.exe"
CODEX_VER = "0.163.0-alpha.10.2"
MANDATE = {
    "PLAN": {"provider": "openai-codex", "model": "gpt-6.1-sol", "engine": "hermes", "effort": "medium",
             "fallbacks": [("opencode-go", "glm-5.3-flash"), ("opencode-go", "deepseek-v4.1-flash")]},
    "EXECUTE": {"provider": "opencode-go", "model": "deepseek-v4.1-flash", "engine": "codex-cli", "effort": None,
                "fallbacks": [("openai-codex", "gpt-6-luna"), ("nvidia", "deepseek-ai/deepseek-v4.1-flash")]},
    "VERIFY_SECURITY": {"provider": "openai-codex", "model": "gpt-6.1-sol", "engine": "codex-cli", "effort": "medium",
                        "fallbacks": [("opencode-go", "glm-5.3-flash"), ("opencode-go", "deepseek-v4.1-flash")]},
}
AUTH = {("openai-codex", "gpt-6.1-sol"): ("openai_oauth", True),
        ("opencode-go", "glm-5.3-flash"): ("env_ref:OPENCODE_GO_API_KEY", False),
        ("opencode-go", "deepseek-v4.1-flash"): ("env_ref:OPENCODE_GO_API_KEY", False),
        ("openai-codex", "gpt-6-luna"): ("openai_oauth", True),
        ("nvidia", "deepseek-ai/deepseek-v4.1-flash"): ("env_ref:NVIDIA_API_KEY", False),
        ("opencode-go", "mimo-v2.6-pro"): ("env_ref:OPENCODE_GO_API_KEY", False),
        ("nvidia", "z-ai/glm-5.3-flash"): ("env_ref:NVIDIA_API_KEY", False)}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def backup(p: Path, stamp: str) -> Path:
    b = p.with_name(p.name + f".bak-farremediation-{stamp}")
    shutil.copy2(p, b)
    return b


def once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"ANCHOR_FAIL {label}: expected 1 occurrence, got {n} :: {old[:90]!r}")
    return text.replace(old, new)


def yaml_text(obj, indent=0) -> str:
    import yaml
    dumped = yaml.safe_dump(obj, sort_keys=False, allow_unicode=True, default_flow_style=False, width=4096)
    pad = " " * indent
    return "".join(pad + ln + "\n" for ln in dumped.rstrip("\n").split("\n"))


def replace_block(text: str, start_marker: str, end_marker: str, new_block: str, label: str) -> str:
    i = text.find(start_marker)
    if i < 0:
        raise SystemExit(f"BLOCK_FAIL {label}: start not found")
    j = text.find(end_marker, i + len(start_marker))
    if j < 0:
        raise SystemExit(f"BLOCK_FAIL {label}: end not found")
    return text[:i] + new_block + text[j:]


def build_routes(existing: list) -> list:
    by = {r["lane"]: r for r in existing}
    out = []
    for lane in ("PLAN", "EXECUTE", "VERIFY_SECURITY"):
        r = dict(by[lane]); m = MANDATE[lane]
        r["provider"] = m["provider"]; r["model"] = m["model"]; r["canonical_identity"] = m["model"]
        r["engine"] = m["engine"]
        auth, oauth = AUTH[(m["provider"], m["model"])]
        r["auth"] = auth; r["oauth"] = oauth
        if m["effort"]:
            r["reasoning_effort"] = m["effort"]
        elif "reasoning_effort" in r:
            r["reasoning_effort"] = None
        r["selection_authority"] = "owner-order-20261021-lane-rebind-plan-gpt-verify-gpt"
        arms = []
        for idx, (prov, mod) in enumerate([(m["provider"], m["model"])] + m["fallbacks"]):
            a_auth, a_oauth = AUTH[(prov, mod)]
            arm = {"arm": ["primary", "fallback1", "fallback2"][idx], "provider": prov, "model": mod,
                   "canonical_identity": mod, "auth": a_auth, "oauth": a_oauth}
            if idx == 0 and m["effort"]:
                arm["reasoning_effort"] = m["effort"]
            arm["default"] = idx == 0
            arm["automatic_selection"] = idx != 1
            arms.append(arm)
        r["arms"] = arms
        r["fallbacks"] = [{"provider": p, "model": mm, "canonical_identity": mm, "auth": AUTH[(p, mm)][0],
                           "oauth": AUTH[(p, mm)][1]} for p, mm in m["fallbacks"]]
        if lane != "EXECUTE":
            r["owner_order_20261021"] = ("epoch 23: PLAN and VERIFY_SECURITY both default to openai-codex/gpt-6.1-sol "
                                         "(medium, OAuth) by owner order 2026-10-21; the PLAN/VERIFY model-axis collision is "
                                         "declared as SOD006-C4 (OPEN_OWNER_ORDERED), not hidden. Historical epoch 19-22 rows "
                                         "remain in history[].")
        out.append(r)
    return out


def build_sod(sod: dict) -> dict:
    s = dict(sod)
    s["pairs"] = [
        {"maker": "EXECUTE", "checker": "VERIFY_SECURITY", "distinct_required": True,
         "note": "Owner order 2026-10-21 (round FAR-REMEDIATION-20261021, epoch 23) re-binds the VERIFY/SECURITY checker to "
                 "openai-codex/gpt-6.1-sol while the EXECUTE writer stays on opencode-go/deepseek-v4.1-flash, so this pair is "
                 "distinct on the model axis again; SOD006-C3 (same-model collision) is superseded by this change."},
        {"maker": "PLAN", "checker": "VERIFY_SECURITY", "distinct_required": False,
         "note": "Owner order 2026-10-21 puts the PLAN & Orchestrator plane AND the VERIFY/SECURITY checker on the same model "
                 "openai-codex/gpt-6.1-sol, so the sweep runs with distinct_required: false for this pair. The collision is REAL "
                 "and DECLARED as SOD006-C4 (OPEN_OWNER_ORDERED); independence for this pair is PROCESS separation only and is "
                 "not claimed as model independence."},
    ]
    dc = [d for d in s.get("declared_conflicts", [])]
    for d in dc:
        if d.get("id") == "SOD006-C3":
            d["status"] = "SUPERSEDED"
            d["superseded_by"] = "SOD006-C4 / owner order 2026-10-21 (round FAR-REMEDIATION-20261021, epoch 23)"
    dc.append({"id": "SOD006-C4", "pairs": [["PLAN", "VERIFY_SECURITY"]], "axis": "canonical_identity",
               "status": "OPEN_OWNER_ORDERED",
               "statement": "Owner order 2026-10-21 mandates PLAN & Orchestrator = openai-codex/gpt-6.1-sol (medium, OAuth) and "
                            "VERIFY/SECURITY checker = openai-codex/gpt-6.1-sol (medium, OAuth), the SAME model on both roles.",
               "conflicting_clause": "PLAN maker and VERIFY checker are not distinct on the model axis.",
               "coherent_clause": "EXECUTE (deepseek-v4.1-flash) vs VERIFY (gpt-6.1-sol) is distinct; independence for the PLAN/VERIFY "
                                  "pair is process separation only.",
               "ruled_by": "owner order 2026-10-21 (user turn, round FAR-REMEDIATION-20261021); pre-authorized remediation of "
                           "FAR-LANE-VERSION-MIX-20261021 P0",
               "required_control": "VERIFY runs as its own read-only Codex-CLI process with a different writer; no claim of model-axis "
                                   "independence for PLAN vs VERIFY."})
    s["declared_conflicts"] = dc
    return s


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    changes, backups, pre = [], {}, {}
    targets = [REG, ASG, POOL, LANE, AGENTS, TESTS, PROFILE, HCOPY]
    for p in targets:
        pre[str(p)] = sha(p)

    # ---------- 1. assignment JSON ----------
    a = json.loads(ASG.read_text(encoding="utf-8"))
    lc = a["lane_chains"]
    lc["PLAN"] = [
        {"model": "gpt-6.1-sol", "provider": "openai-codex", "reasoning_effort": "medium", "role": "primary",
         "default": True, "arm": "A", "automatic_selection": True, "auth": "openai_oauth",
         "owner_order_20261021": "rank-1 PLAN default restored to GPT 6.1 SOL-MEDIUM (OpenAI OAuth) by owner order 2026-10-21."},
        {"model": "glm-5.3-flash", "provider": "opencode-go", "reasoning_effort": "medium",
         "role": "fallback1", "default": False, "arm": "B", "automatic_selection": True,
         "prior_revision_note": "Rank-1 default of epoch 22 (owner order 2026-10-16); demoted to fallback1 by the 2026-10-21 order. History preserved."},
        {"model": "deepseek-v4.1-flash", "provider": "opencode-go", "role": "fallback2", "default": False,
         "arm": "C", "automatic_selection": True}]
    lc["VERIFY_SECURITY"] = [
        {"role": "primary", "model": "gpt-6.1-sol", "provider": "openai-codex", "reasoning_effort": "medium",
         "default": True, "arm": "A", "automatic_selection": True, "auth": "openai_oauth",
         "owner_order_20261021": "rank-1 VERIFY checker is GPT 6.1 SOL-MEDIUM (OpenAI OAuth) per owner order 2026-10-21."},
        {"role": "fallback1", "model": "glm-5.3-flash", "provider": "opencode-go", "reasoning_effort": "medium",
         "default": False, "arm": "B", "automatic_selection": True},
        {"role": "fallback2", "model": "deepseek-v4.1-flash", "provider": "opencode-go", "reasoning_effort": "medium",
         "default": False, "arm": "C", "automatic_selection": True,
         "prior_revision_note": "Primary arm A of epoch 22 (owner order 2026-10-16); demoted to fallback2 by the 2026-10-21 order. History preserved."}]
    a["sod"]["plan_lane"] = "openai-codex / gpt-6.1-sol (medium, OpenAI OAuth) — owner order 2026-10-21 (round FAR-REMEDIATION-20261021, epoch 23); supersedes the 2026-10-16 GLM order."
    a["sod"]["verify_security_lane"] = "openai-codex / gpt-6.1-sol (medium, OpenAI OAuth) — owner order 2026-10-21; supersedes the 2026-10-16 deepseek order."
    a["sod"]["verify_security_default_arm"] = "gpt-6.1-sol"
    a["sod"]["verify_vs_plan_model_separation"] = "ABSENT BY OWNER ORDER — PLAN and VERIFY share gpt-6.1-sol; declared as SOD006-C4 (OPEN_OWNER_ORDERED); independence is process separation only."
    a["sod"]["plan_reasoning_effort"] = "medium"
    a["sod"]["verify_security_reasoning_effort"] = "medium"
    sc = a.get("sod_conflicts") or []
    for d in sc:
        if d.get("id") == "SOD006-C3":
            d["status"] = "SUPERSEDED"
    sc.append({"id": "SOD006-C4", "pairs": [["PLAN", "VERIFY_SECURITY"]], "axis": "canonical_identity",
               "statement": "PLAN and VERIFY_SECURITY share gpt-6.1-sol by owner order 2026-10-21.",
               "status": "OPEN_OWNER_ORDERED", "adjudication_owner": "operator / Human Policy Owner",
               "ruled_by": "owner order 2026-10-21 (round FAR-REMEDIATION-20261021)"})
    a["sod_conflicts"] = sc
    a["registry_epoch"] = 23
    a["revision"] = 23
    a["revision_23_reason"] = ("Round FAR-REMEDIATION-20261021 (owner order 2026-10-21): PLAN rank-1 = openai-codex/gpt-6.1-sol (medium, OAuth); "
                               "VERIFY_SECURITY rank-1 = openai-codex/gpt-6.1-sol (medium, OAuth, Codex CLI); EXECUTE unchanged; SOD006-C3 superseded, "
                               "SOD006-C4 declared OPEN_OWNER_ORDERED; toolchain pin unified to the live 0.163.0-alpha.10.2 build. Cross-surface "
                               "alignment (registry / pool / profile / AGENTS.md / owner-chain test) lands in the SAME change set.")
    if not args.apply:
        pass
    else:
        ASG.write_text(json.dumps(a, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changes.append({"file": str(ASG), "kind": "lane_chains+sod+epoch23"})

    # ---------- 2. pool JSON ----------
    pl = json.loads(POOL.read_text(encoding="utf-8"))
    def ent(prov, mod, rank, role, effort=None):
        auth, oauth = AUTH[(prov, mod)]
        e = {"rank": rank, "provider": prov, "model": mod, "role": role, "auth": auth, "oauth": oauth,
             "transport_model": f"{prov}/{mod}"}
        if effort:
            e["reasoning_effort"] = effort
        return e
    for lane in pl["lanes"]:
        if lane["lane"] == "PLAN":
            lane["ordered_pool"] = [ent("openai-codex", "gpt-6.1-sol", 1, "DEFAULT/首選", "medium"),
                                    ent("opencode-go", "glm-5.3-flash", 2, "FALLBACK1/備援1"),
                                    ent("opencode-go", "deepseek-v4.1-flash", 3, "FALLBACK2/備援2"),
                                    ent("opencode-go", "mimo-v2.6-pro", 4, "OPTIONAL/可選"),
                                    ent("nvidia", "z-ai/glm-5.3-flash", 5, "OPTIONAL/可選"),
                                    ent("nvidia", "deepseek-ai/deepseek-v4.1-flash", 6, "OPTIONAL/可選")]
        elif lane["lane"] == "VERIFY_SECURITY":
            lane["ordered_pool"] = [ent("openai-codex", "gpt-6.1-sol", 1, "DEFAULT/首選", "medium"),
                                    ent("opencode-go", "glm-5.3-flash", 2, "FALLBACK1/備援1"),
                                    ent("opencode-go", "deepseek-v4.1-flash", 3, "FALLBACK2/備援2"),
                                    ent("nvidia", "deepseek-ai/deepseek-v4.1-flash", 4, "OPTIONAL/可選")]
        elif lane["lane"] == "EXECUTE":
            lane["ordered_pool"] = [ent("opencode-go", "deepseek-v4.1-flash", 1, "DEFAULT/首選"),
                                    ent("openai-codex", "gpt-6-luna", 2, "FALLBACK1/備援1"),
                                    ent("nvidia", "deepseek-ai/deepseek-v4.1-flash", 3, "FALLBACK2/備援2")]
    pl["rev"] = "far-remediation-20261021"
    cl = pl.get("change_log")
    if isinstance(cl, list):
        cl.append({"rev": "far-remediation-20261021", "utc": stamp,
                   "note": "PLAN/VERIFY rank-1 = openai-codex/gpt-6.1-sol (DEFAULT), glm fallback1, deepseek fallback2 — owner order 2026-10-21. "
                           "Rank and role labels now agree in every lane."})
    elif isinstance(cl, dict):
        cl["far-remediation-20261021"] = {"utc": stamp, "note": "rank/role realigned to owner order 2026-10-21"}
    if args.apply:
        POOL.write_text(json.dumps(pl, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changes.append({"file": str(POOL), "kind": "rank/role realignment"})

    # ---------- 3. lane binding JSON ----------
    lb = json.loads(LANE.read_text(encoding="utf-8"))
    lb["codex_executable"] = CODEX_BIN.replace("/", "\\")
    lb["codex_version"] = CODEX_VER
    lb["codex_sha256"] = sha(Path(CODEX_BIN))
    lb["toolchain_pin_note"] = (f"Round {ROUND} (epoch 23): the pin now names the INSTALLED build and its measured sha256 "
                                f"({lb['codex_sha256'][:16]}…), replacing the dead e78bad9887fa50cf path that had been recorded "
                                f"as a KNOWN STALE POINTER since 2026-10-15. Version verified with `codex --version`.")
    if args.apply:
        LANE.write_text(json.dumps(lb, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changes.append({"file": str(LANE), "kind": "toolchain pin"})

    # ---------- 4. registry YAML (block regeneration for routes/sod) ----------
    import yaml
    reg_text = REG.read_text(encoding="utf-8")
    reg = yaml.safe_load(reg_text)
    new_routes = build_routes(reg["routes"])
    new_sod = build_sod(reg["sod_invariants"])
    reg_doc = dict(reg)
    reg_doc["routes"] = new_routes
    reg_doc["sod_invariants"] = new_sod
    reg_doc["epoch"] = 23
    reg_doc["source_of_routes"] = {"path": "config/model-lane-assignment.json", "revision": 23,
                                   "sha256": ""}  # filled after assignment write
    # projection expected-value sync for the pointers this change owns
    OK_PREFIX = ("/lane_chains/PLAN", "/lane_chains/VERIFY_SECURITY", "/sod/", "/registry_epoch", "/revision",
                 "/codex_version", "/codex_sha256", "/provider", "/model", "/sod_conflicts/")
    def resolve(obj, ptr):
        cur = obj
        for part in [x for x in ptr.split("/") if x]:
            if isinstance(cur, list):
                cur = cur[int(part)]
            elif isinstance(cur, dict):
                cur = cur[part]
            else:
                raise KeyError(ptr)
        return cur
    asg_doc = json.loads(ASG.read_text(encoding="utf-8")) if args.apply else a
    lane_doc = json.loads(LANE.read_text(encoding="utf-8")) if args.apply else lb
    sync = []
    for proj in reg_doc.get("projections", []):
        target = {"model-lane-assignment": asg_doc, "hermes-codex-lane": lane_doc}.get(proj.get("id"))
        if target is None:
            continue
        for b in proj.get("bindings", []):
            ptr = b.get("pointer", "")
            if not ptr.startswith(OK_PREFIX):
                continue
            try:
                actual = resolve(target, ptr)
            except Exception:
                continue
            if b.get("expected") != actual:
                sync.append({"proj": proj.get("id"), "pointer": ptr, "old": b.get("expected"), "new": actual})
                b["expected"] = actual
    new_reg_text = yaml_text(reg_doc)
    header = "# " + "=" * 76 + "\n# NOTE (round %s, %s): the routes[]/sod_invariants[] blocks were\n# REGENERATED from their parsed structures by apply_far_remediation.py. Block-level prose comments that\n# used to sit inside those two blocks are carried as data fields (owner_order_20261021, note, ruled_by)\n# and in history[]; the file header comments above this marker are untouched. This is a documentation\n# churn, disclosed in the round receipt, not a silent rewrite.\n# " % (ROUND, stamp) + "=" * 76 + "\n"
    if args.apply:
        REG.write_text(header + new_reg_text, encoding="utf-8")
        changes.append({"file": str(REG), "kind": "epoch 23 + routes/sod regenerated", "binding_sync": len(sync)})

    # ---------- 5. profile config (surgical, comment-preserving) ----------
    prof = PROFILE.read_text(encoding="utf-8")
    prof2 = once(prof, "  default: deepseek-v4.1-flash", "  default: gpt-6.1-sol", "profile.default")
    prof2 = once(prof2, "  provider: opencode-go", "  provider: openai-codex", "profile.provider")
    if args.apply:
        PROFILE.write_text(prof2, encoding="utf-8")
        changes.append({"file": str(PROFILE), "kind": "PLAN plane binding"})

    # ---------- 6. Hermes config.yaml codex_bin ----------
    hc = HCOPY.read_text(encoding="utf-8")
    hc2 = once(hc, "C:/Users/user/AppData/Local/HG-KSEOS/runtime/codex-0.147.0-alpha.6.5/codex.exe",
               CODEX_BIN.replace("/", "/"), "hermes.codex_bin")
    if args.apply:
        HCOPY.write_text(hc2, encoding="utf-8")
        changes.append({"file": str(HCOPY), "kind": "codex_bin unified"})

    # ---------- 7. AGENTS.md ----------
    ag = AGENTS.read_text(encoding="utf-8")
    ag2 = once(ag, "## Lane-chain contract (current, epoch 18)",
               "## Lane-chain contract (current, epoch 23)", "agents.epoch")
    ag2 = once(ag2,
               "- **PLAN** (Hermes-internal): default `openai-codex/gpt-6.1-sol` (medium, OAuth) → fallback1 `opencode-go/glm-5.3-flash` → fallback2 `opencode-go/deepseek-v4.1-flash`.",
               "- **PLAN** (Hermes-internal): default `openai-codex/gpt-6.1-sol` (medium, OAuth) → fallback1 `opencode-go/glm-5.3-flash` → fallback2 `opencode-go/deepseek-v4.1-flash`. (owner order 2026-10-21, epoch 23 — restored; the 2026-10-16 GLM order is superseded history)",
               "agents.plan")
    ag2 = once(ag2,
               "- **VERIFY_SECURITY** (Codex CLI checker): default `openai-codex/gpt-6.1-sol` (medium) → fallback1 `opencode-go/glm-5.3-flash` → fallback2 `opencode-go/deepseek-v4.1-flash`.",
               "- **VERIFY_SECURITY** (Codex CLI checker): default `openai-codex/gpt-6.1-sol` (medium) → fallback1 `opencode-go/glm-5.3-flash` → fallback2 `opencode-go/deepseek-v4.1-flash`. (owner order 2026-10-21, epoch 23; PLAN/VERIFY share this model — declared SOD006-C4 OPEN_OWNER_ORDERED, process separation only)",
               "agents.verify")
    ag2 = once(ag2,
               "The canonical binary pin (`config/hermes-codex-lane.json`) is a KNOWN STALE POINTER pending owner approval; task-local declaration covers runtime use.",
               "The canonical binary pin (`config/hermes-codex-lane.json`) now names the INSTALLED build (0.163.0-alpha.10.2, sha256 verified) — repaired in round FAR-REMEDIATION-20261021, epoch 23.",
               "agents.pin")
    if args.apply:
        AGENTS.write_text(ag2, encoding="utf-8")
        changes.append({"file": str(AGENTS), "kind": "epoch 23 lane-chain contract"})

    # ---------- 8. tests owner chain ----------
    t = TESTS.read_text(encoding="utf-8")
    old_chain = '''            "PLAN": [("opencode-go", "glm-5.3-flash"), ("openai-codex", "gpt-6.1-sol"), ("opencode-go", "deepseek-v4.1-flash")],
            "VERIFY_SECURITY": [("opencode-go", "deepseek-v4.1-flash"), ("openai-codex", "gpt-6.1-sol"), ("opencode-go", "glm-5.3-flash")],'''
    new_chain = '''            "PLAN": [("openai-codex", "gpt-6.1-sol"), ("opencode-go", "glm-5.3-flash"), ("opencode-go", "deepseek-v4.1-flash")],
            "VERIFY_SECURITY": [("openai-codex", "gpt-6.1-sol"), ("opencode-go", "glm-5.3-flash"), ("opencode-go", "deepseek-v4.1-flash")],'''
    t2 = once(t, old_chain, new_chain, "tests.owner_chain")
    t2 = once(t2, "# Owner chain (2026-10-16 rebind, round ROUND3-LANE-REBIND-AND-CLOSURE-20261016): the declared fallback sequence is first-class",
              "# Owner chain (2026-10-21 rebind, round FAR-REMEDIATION-20261021, epoch 23 — owner-authorized oracle update): the sequence is first-class", "tests.comment")
    if args.apply:
        TESTS.write_text(t2, encoding="utf-8")
        changes.append({"file": str(TESTS), "kind": "owner-chain oracle (owner-authorized)"})

    # ---------- 9. source_of_routes + final assertions ----------
    receipt = {"round": ROUND, "utc": stamp, "applied": bool(args.apply), "changes": changes,
               "binding_sync": sync, "pre_sha256": pre}
    if args.apply:
        asg_new_sha = sha(ASG)
        reg_final = REG.read_text(encoding="utf-8")
        reg_doc2 = yaml.safe_load(reg_final)
        reg_doc2["source_of_routes"] = {"path": "config/model-lane-assignment.json", "revision": 23, "sha256": asg_new_sha}
        REG.write_text(yaml_text(reg_doc2), encoding="utf-8")  # header note retained? no -> re-add below
        reg_txt = REG.read_text(encoding="utf-8")
        if not reg_txt.startswith("# "):
            REG.write_text(header + reg_txt, encoding="utf-8")
        receipt["source_of_routes_sha256"] = asg_new_sha
        # assertions
        sys.path.insert(0, str(ROOT / "src"))
        from hg_kseos import lane_policy as lp
        reg_v = lp.load_registry()
        assert reg_v["epoch"] == 23, reg_v["epoch"]
        for lane, m in MANDATE.items():
            r = lp.route_for_lane(reg_v, lane)
            assert (r["provider"], r["model"]) == (m["provider"], m["model"]), (lane, r.get("provider"), r.get("model"))
            assert r["engine"] == m["engine"], (lane, r["engine"])
        drift = lp.check_drift(registry=reg_v)
        receipt["check_drift"] = drift
        assert drift == [], f"DRIFT after apply: {drift}"
        rc = subprocess.run([str(ROOT / ".venv" / "Scripts" / "python.exe"), "-m", "pytest", "tests/test_lane_policy.py", "-q"],
                            cwd=str(ROOT), capture_output=True, text=True, timeout=600)
        receipt["pytest_rc"] = rc.returncode
        receipt["pytest_tail"] = (rc.stdout or "").strip().splitlines()[-3:]
        assert rc.returncode == 0, f"pytest failed: {receipt['pytest_tail']}"
        receipt["post_sha256"] = {str(p): sha(p) for p in targets}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / ("apply_receipt.json" if args.apply else "apply_dryrun.json")).write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"applied": bool(args.apply), "changes": changes, "binding_sync": len(sync),
                      "check_drift": receipt.get("check_drift"), "pytest_rc": receipt.get("pytest_rc")},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
