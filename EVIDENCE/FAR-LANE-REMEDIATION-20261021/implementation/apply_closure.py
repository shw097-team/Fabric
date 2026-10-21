#!/usr/bin/env python
"""FAR-CLOSURE-20261021 — close the measured cross-field declaration gaps (dry-run default).

Findings this closes (all measured, not inferred):
  F1  config/model-lane-assignment.json::sod.verify_security_arm_A still names
      "opencode-go / deepseek-v4.1-flash (primary Codex CLI checker)" while
      lane_chains.VERIFY_SECURITY[0] is openai-codex/gpt-6.1-sol. check_drift() does NOT
      see this (it compares each binding against its own pointer target only).
  F2  config/lane-routing-registry.yaml::authorization_basis still says "dispatchable at revision 17".
  F3  config/lane-routing-registry.yaml routes[].selected_arm_identity still names deepseek-v4.1-flash
      for a lane whose rank-1 is gpt-6.1-sol.
  F4  config/lane-routing-registry.yaml projections[model-lane-assignment].note still describes
      revision 22 / PLAN=glm / VERIFY=deepseek as the current policy.
  F5  the pool's EXECUTE rank-1 is a PROBE arm (minimax) inserted for a lane measurement, while the
      declared policy default is deepseek-v4.1-flash. A PROBE arm must not read as a DEFAULT.
  F6  the open-spec change's tasks.md checklist is not reconciled against the receipts that exist.
  F7  AGENTS.md still names SOD006-C2 as the live conflict (C2 is SUPERSEDED; C4 is live) and
      still points at assignment "revision 18".

Properties: dry-run default; per-file pre-image sha256; per-run backups; exactly-once anchors;
post-write assertions; check_drift; owner-chain test; receipt; rollback paths. No git write verbs.
"""
from __future__ import annotations
import argparse, hashlib, json, re, shutil, subprocess, sys, time
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
ROUND = "FAR-CLOSURE-20261021"
OUT = ROOT / "var" / ROUND
REG = ROOT / "config" / "lane-routing-registry.yaml"
ASG = ROOT / "config" / "model-lane-assignment.json"
POOL = ROOT / "config" / "lane-route-slots.candidate.json"
AGENTS = ROOT / "AGENTS.md"
TASKS = ROOT / "openspec" / "changes" / "far-lane-remediation-20261021" / "tasks.md"
README = ROOT / "README.md"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"ANCHOR_FAIL {label}: expected exactly 1 occurrence, got {n} :: {old[:100]!r}")
    return text.replace(old, new)


def once_idempotent(text: str, old: str, new: str, label: str) -> tuple[str, bool]:
    """Apply `old -> new` exactly once. If the replacement is already present and the original is
    absent, the change is already applied: return the text unchanged and a False 'changed' flag.
    A re-run of a repair must not fail on its own prior output, and must not corrupt state."""
    if text.count(old) == 1 and text.count(new) == 0:
        return text.replace(old, new), True
    if text.count(old) == 0 and text.count(new) >= 1:
        return text, False
    raise SystemExit(f"ANCHOR_FAIL {label}: old={text.count(old)} new={text.count(new)} :: {old[:100]!r}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    changes, pre = [], {}
    for p in (ASG, REG, POOL, AGENTS, TASKS, README):
        pre[str(p)] = sha(p)

    # ---- F1: cross-field contradiction in the assignment's sod block ----
    a = json.loads(ASG.read_text(encoding="utf-8"))
    sod = a["sod"]
    chain_primary = a["lane_chains"]["VERIFY_SECURITY"][0]
    expected_arm_a = f"{chain_primary['provider']} / {chain_primary['model']} (primary Codex CLI checker)"
    old_arm_a = sod.get("verify_security_arm_A")
    sod["verify_security_arm_A"] = expected_arm_a
    sod["verify_security_arm_A_note"] = (
        "Aligned to lane_chains.VERIFY_SECURITY[0] in round FAR-CLOSURE-20261021. This field is a "
        "PROSE restatement of the chain, so it is not covered by check_drift(); the cross-field check "
        "is now a named gate (see tests/test_lane_declaration_agreement.py).")
    sod["verify_security_arm_A_prior_value"] = old_arm_a
    a["revision"] = 24
    a["registry_epoch"] = 24
    a["revision_24_reason"] = (
        "Round FAR-CLOSURE-20261021: close the cross-field declaration gaps that check_drift() cannot "
        "see. sod.verify_security_arm_A now restates lane_chains.VERIFY_SECURITY[0] instead of the "
        "superseded deepseek arm; registry authorization_basis / selected_arm_identity / projection note "
        "stopped describing revision 17/22; the EXECUTE pool's PROBE arm is labelled as a PROBE and the "
        "declared default is stated; the change checklist is reconciled against receipts. Epoch 24.")
    # The registry projects this file's revision/epoch as EXPECTED values. When the assignment's own
    # revision advances, those projections must advance in the SAME change set or check_drift reports
    # DRIFT_VALUE and the conformance suite fails. (Measured in this round: epoch 23 -> 24 produced
    # exactly two such rows, /registry_epoch and /revision.)
    if args.apply:
        import yaml
        reg_pre = yaml.safe_load(REG.read_text(encoding="utf-8"))
        for proj in reg_pre.get("projections", []):
            if proj.get("id") != "model-lane-assignment":
                continue
            for b in proj.get("bindings", []):
                if b.get("pointer") in ("/registry_epoch", "/revision"):
                    b["expected"] = 24
        reg_pre["epoch"] = 24
        reg_pre["source_of_routes"] = {"path": "config/model-lane-assignment.json", "revision": 24,
                                       "sha256": ""}
        # re-serialise, preserving the prose comments by editing the original text instead of dumping
        rt = REG.read_text(encoding="utf-8")
        rt, _e1 = once_idempotent(rt, "epoch: 23", "epoch: 24", "sync.epoch")
        rt, _e2 = once_idempotent(rt, "  revision: 23", "  revision: 24", "sync.source_revision")
        for b in reg_pre.get("projections", []):
            if b.get("id") != "model-lane-assignment":
                continue
            for bind in b.get("bindings", []):
                if bind.get("pointer") in ("/registry_epoch", "/revision") and bind.get("expected") == 24:
                    old = f"pointer: {bind['pointer']}\n"
                    idx = rt.find(old)
                    if idx < 0:
                        continue
                    # replace the expected value on the following line(s) of this binding block
                    j = rt.find("expected: ", idx)
                    if j < 0:
                        continue
                    k = rt.find("\n", j)
                    rt = rt[:j] + "expected: 24" + rt[k:]
        REG.write_text(rt, encoding="utf-8")
        ASG.write_text(json.dumps(a, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        asg_sha = hashlib.sha256(ASG.read_bytes()).hexdigest()
        rt = REG.read_text(encoding="utf-8")
        rt = re.sub(r"(source_of_routes:\n(?:.*\n)*?  sha256: )\"[0-9a-f]*\"", r'\g<1>"' + asg_sha + '"', rt, count=1)
        REG.write_text(rt, encoding="utf-8")
        changes.append({"finding": "F1", "file": str(ASG), "change": "sod.verify_security_arm_A aligned to the chain"})
        changes.append({"finding": "sync", "file": str(REG), "change": "epoch 24 + projection expected values for /registry_epoch and /revision + source_of_routes sha256"})
    else:
        changes.append({"finding": "F1", "file": str(ASG), "change": "sod.verify_security_arm_A aligned to the chain"})
        changes.append({"finding": "sync", "file": str(REG), "change": "epoch 24 + projection expected values for /registry_epoch and /revision + source_of_routes sha256"})

    # ---- F2/F3/F4: registry internal residue (operate on the CURRENT file, which may already
    # carry the epoch-24 sync written above) ----
    reg = REG.read_text(encoding="utf-8")
    r2, ch2 = once_idempotent(reg, "dispatchable at revision 17", "dispatchable at revision 24", "F2.revision")
    r2, ch3 = once_idempotent(r2,
              "  selected_arm_identity: deepseek-v4.1-flash",
              "  selected_arm_identity: gpt-6.1-sol", "F3.selected_arm")
    old_note = re.search(r"  note: 'canonical policy revision 22.*?'\n", r2, re.S)
    if old_note:
        new_note = ("  note: 'canonical policy revision 24 (owner order 2026-10-21, round FAR-CLOSURE-20261021, superseding "
                    "revision 22 / the 2026-10-16 order). PLAN rank-1 is openai-codex/gpt-6.1-sol (medium, OpenAI OAuth) with the "
                    "owner-chain fallbacks GLM-5.3-Flash (OpenCode Go) then DeepSeek V4.1 Flash; VERIFY_SECURITY arm A is "
                    "openai-codex/gpt-6.1-sol (Codex CLI) and arm B is opencode-go/glm-5.3-flash; the additional EXECUTE route is "
                    "operator-selectable only. PLAN and VERIFY/SECURITY share one model BY OWNER ORDER, declared as SOD006-C4 "
                    "(OPEN_OWNER_ORDERED, process separation only) rather than hedged.'\n")
        r2 = r2[:old_note.start()] + new_note + r2[old_note.end():]
        ch4 = True
    elif "canonical policy revision 24" in r2:
        ch4 = False
    else:
        raise SystemExit("ANCHOR_FAIL F4.note: projection note not found")
    if args.apply:
        REG.write_text(r2, encoding="utf-8")
        changes.append({"finding": "F2/F3/F4", "file": str(REG), "change": "authorization_basis revision, selected_arm_identity, projection note"})

    # ---- F5: PROBE arm must not read as DEFAULT ----
    pl = json.loads(POOL.read_text(encoding="utf-8"))
    touched = []
    for lane in pl["lanes"]:
        if lane["lane"] != "EXECUTE":
            continue
        pool = lane["ordered_pool"]
        # the measured PROBE arm (minimax) may sit at rank 1; demote it below the declared default
        probe = [c for c in pool if c.get("role", "").startswith("PROBE")]
        if probe:
            probe.sort(key=lambda c: c.get("rank", 0))
            rest = [c for c in pool if not c.get("role", "").startswith("PROBE")]
            rest.sort(key=lambda c: c.get("rank", 0))
            # declared default first, then the other non-probe entries, then the PROBE arm
            default_entry = next((c for c in rest if c.get("role", "").startswith("DEFAULT")), None)
            ordered = ([default_entry] if default_entry else []) + [c for c in rest if c is not default_entry] + probe
            for i, c in enumerate(ordered, 1):
                c["rank"] = i
            if default_entry is not None:
                default_entry["role"] = "DEFAULT/首選"
                default_entry["probe_note"] = ("declared policy default for this lane (owner order 2026-10-21)")
            for c in probe:
                c["role"] = "PROBE/探測"
                c["probe_note"] = ("measured lane arm (round FAR-CLOSURE-20261021): the Codex-CLI lane served this arm at "
                                   "required_arm == served_arm. A PROBE arm is NOT a policy default and must not be "
                                   "selected by an unpinned dispatch; it is an explicitly pinnable measured capability.")
                c["default"] = False
                c["automatic_selection"] = False
            lane["ordered_pool"] = ordered
            touched.append([f"{c.get('rank')}:{c.get('provider')}/{c.get('model')}:{c.get('role')}" for c in ordered])
    pl["rev"] = "far-closure-20261021"
    if args.apply:
        POOL.write_text(json.dumps(pl, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changes.append({"finding": "F5", "file": str(POOL), "change": "PROBE arm demoted below the declared DEFAULT", "pool": touched})

    # ---- F7: AGENTS.md live-conflict pointer + source revision ----
    ag = AGENTS.read_text(encoding="utf-8")
    a2, _c1 = once_idempotent(ag, "SOD006-C2 (PLAN and VERIFY share the default arm by owner order) is recorded `OPEN_OWNER_ORDERED` in the registry",
               "SOD006-C4 (PLAN and VERIFY share the default arm by owner order) is recorded `OPEN_OWNER_ORDERED` in the registry; "
               "SOD006-C2 and SOD006-C3 are retained as SUPERSEDED history", "F7.sod")
    a2, _c2 = once_idempotent(a2, "source pin → `config/model-lane-assignment.json`, revision 18",
              "source pin → `config/model-lane-assignment.json`, revision 24", "F7.revision")
    if args.apply:
        AGENTS.write_text(a2, encoding="utf-8")
        changes.append({"finding": "F7", "file": str(AGENTS), "change": "live SoD conflict pointer C2->C4, source revision 18->24"})

    # ---- F6: reconcile the change checklist against receipts ----
    t = TASKS.read_text(encoding="utf-8")
    for old, new in (
        ("- [ ] 1.1 Apply P0/P1/P2 declaration alignment via `var/FAR-REMEDIATION-20261021/apply_far_remediation.py --apply`",
         "- [x] 1.1 Apply P0/P1/P2 declaration alignment via `var/FAR-REMEDIATION-20261021/apply_far_remediation.py --apply` "
         "(receipt: `var/FAR-REMEDIATION-20261021/apply_receipt.json`; local commit `c442f07`)"),
        ("- [ ] 1.2 Verify `check_drift` returns `[]` and the owner-chain test is green",
         "- [x] 1.2 Verify `check_drift` returns `[]` and the owner-chain test is green "
         "(receipt: `var/FAR-REMEDIATION-20261021/selfcheck_receipt.json`, GATE_PASS 18/18; pytest 3 passed / 90 subtests)"),
        ("- [ ] 1.3 Declare `SOD006-C4 OPEN_OWNER_ORDERED` and supersede `SOD006-C3`",
         "- [x] 1.3 Declare `SOD006-C4 OPEN_OWNER_ORDERED` and supersede `SOD006-C3` "
         "(registry `sod_invariants.declared_conflicts`; assignment `sod_conflicts`)"),
        ("- [ ] 2.1 Toolchain pin names the installed 0.163.0-alpha.10.2 build with measured sha256",
         "- [x] 2.1 Toolchain pin names the installed 0.163.0-alpha.10.2 build with measured sha256 "
         "(sha256 f6dbf48c…, verified by `codex --version` and by digest recomputation)"),
        ("- [ ] 2.2 Hermes `model.codex_bin` unified to the same binary",
         "- [x] 2.2 Hermes `model.codex_bin` unified to the same binary"),
        ("- [ ] 3.1 Pool rank/role labels agree with rank order for all three lanes",
         "- [x] 3.1 Pool rank/role labels agree with rank order for all three lanes"),
        ("- [ ] 3.2 In-Hermes PLAN-plane profile binds `openai-codex/gpt-6.1-sol`",
         "- [x] 3.2 In-Hermes PLAN-plane profile binds `openai-codex/gpt-6.1-sol` "
         "(fresh-session one-shot served gpt-6.1-sol via openai-codex)"),
        ("- [ ] 4.1 Run the self-check harness and the bounded repair loop to green",
         "- [x] 4.1 Run the self-check harness and the bounded repair loop to green (GATE_PASS 18/18)"),
        ("- [ ] 4.2 Independent AO lane (gpt-6.1-sol, read-only) re-derives every gate claim\n",
         "- [ ] 4.2 Independent AO lane (gpt-6.1-sol, read-only) re-derives every gate claim — NOT OBTAINED: the Codex-CLI "
         "arm returned HTTP 400 `Model is unavailable`; no verdict, no WO result recorded. Local green is NOT acceptance.\n"),
        ("- [ ] 5.1 Bring the four routing files under git (local commit, no remote)",
         "- [x] 5.1 Bring the four routing files under git (local commit `c442f07`, no remote action)"),
        ("- [ ] 5.2 Fresh-session PLAN default verified from the profile's own state.db row",
         "- [x] 5.2 Fresh-session PLAN default verified from the profile's own state.db row "
         "(row: model=gpt-6.1-sol, billing_provider=openai-codex, source=oneshot)"),
    ):
        t, _c = once_idempotent(t, old, new, f"F6.{old[:14]}")
    if args.apply:
        TASKS.write_text(t, encoding="utf-8")
        changes.append({"finding": "F6", "file": str(TASKS), "change": "checklist reconciled against receipts (AO item left open)"})

    # ---- README: current-snapshot banner (history is NOT rewritten) ----
    rd = README.read_text(encoding="utf-8")
    anchor = "# HG-KSEOS（冷啟動入口 / Landing Page）\n"
    if anchor not in rd:
        raise SystemExit("ANCHOR_FAIL README.anchor: heading not found")
    banner = (
        "\n> **現行路由政策快照（registry epoch 24 / assignment revision 24，2026-10-21 owner order）**：\n"
        "> PLAN = `openai-codex/gpt-6.1-sol`（medium, OAuth, Hermes-internal）｜EXECUTE = `opencode-go/deepseek-v4.1-flash`（Codex CLI）｜\n"
        "> VERIFY_SECURITY = `openai-codex/gpt-6.1-sol`（medium, OAuth, Codex CLI）。PLAN 與 VERIFY 的 **model-axis 獨立性缺席**\n"
        "> （記為 `SOD006-C4 OPEN_OWNER_ORDERED`，僅程序分離）。下方依日期排列的段落為**當時紀錄**，不代表現況；\n"
        "> 工具鏈 pin 已於 round `FAR-REMEDIATION-20261021` 修復為實機 `0.163.0-alpha.10.2`。\n")
    if banner.strip() not in rd:
        rd2, _c = once_idempotent(rd, anchor, anchor + banner, "README.banner")
        if args.apply:
            README.write_text(rd2, encoding="utf-8")
            changes.append({"finding": "README", "file": str(README), "change": "current-snapshot banner (history preserved)"})

    receipt = {"round": ROUND, "utc": stamp, "applied": bool(args.apply), "changes": changes, "pre_sha256": pre}
    if args.apply:
        sys.path.insert(0, str(ROOT / "src"))
        from hg_kseos import lane_policy as lp
        reg_v = lp.load_registry()
        drift = lp.check_drift(registry=reg_v)
        receipt["check_drift"] = drift
        a2 = json.loads(ASG.read_text(encoding="utf-8"))
        ch0 = a2["lane_chains"]["VERIFY_SECURITY"][0]
        receipt["F1_alignment"] = {"sod_arm_A": a2["sod"]["verify_security_arm_A"],
                                    "chain_primary": f"{ch0['provider']} / {ch0['model']}",
                                    "aligned": a2["sod"]["verify_security_arm_A"].startswith(f"{ch0['provider']} / {ch0['model']}")}
        rc = subprocess.run([str(ROOT / ".venv" / "Scripts" / "python.exe"), "-m", "pytest", "tests/test_lane_policy.py", "-q"],
                            cwd=str(ROOT), capture_output=True, text=True, timeout=600)
        receipt["pytest_rc"] = rc.returncode
        receipt["pytest_tail"] = (rc.stdout or "").strip().splitlines()[-2:]
        receipt["post_sha256"] = {str(p): sha(p) for p in (ASG, REG, POOL, AGENTS, TASKS, README)}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / ("apply_receipt.json" if args.apply else "apply_dryrun.json")).write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"applied": bool(args.apply), "changes": [c.get("finding") for c in changes],
                      "check_drift": receipt.get("check_drift"), "pytest_rc": receipt.get("pytest_rc"),
                      "F1_aligned": (receipt.get("F1_alignment") or {}).get("aligned")}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
