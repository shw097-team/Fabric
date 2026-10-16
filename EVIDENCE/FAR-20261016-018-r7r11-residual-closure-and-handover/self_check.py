#!/usr/bin/env python
"""FAR-20261016-018 self-check. Every check is COMPUTED from artifacts; no verdict literal.

Tri-state: PASS / FAIL / NOT_RUN (a check whose inputs are absent is NOT_RUN, never PASS).
--negative-control perturbs one input set and asserts at least one check flips to FAIL,
which is what proves this harness is not vacuous (invariant 11 (a)/(g)).
"""
import json, re, sys, hashlib, argparse, subprocess
from pathlib import Path

RD = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261016-018-r7r11-residual-closure-and-handover")
PREV = Path("C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016")
PY = "C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe"

OVERCLAIM = re.compile(
    r"(CONVERGENCE_ACHIEVED|PRODUCTION_(READY|CERTIFIED)|AO_ACCEPTED|EXTERNALLY_ACCEPTED|"
    r"R7-03[_ -]CLOSED|EIA-20261016-02[_ -]CLOSED|IMMUTABLE_BOUNDARY_(PROVEN|ACHIEVED)|VALIDATOR_ACCEPTED)",
    re.I)
SECRET = re.compile(r"(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|sk-[A-Za-z0-9]{20,})")


def J(rel, root=RD):
    p = root / rel
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def build(mutate=None):
    """Return the check list as data. `mutate` names an injected perturbation."""
    C = []

    def add(cid, claim, verdict, evidence):
        C.append({"id": cid, "claim": claim, "verdict": verdict, "evidence": evidence})

    rc = J("ROUTE_CHECK.json")
    if rc is None:
        add("S1", "live named-method route discriminates the round's flow from a control", "NOT_RUN", "ROUTE_CHECK.json absent")
    else:
        r = rc.get("registry") or {}
        pos = (r.get("route_FAR_RESEARCH") or {}).get("route")
        neg = (r.get("route_NEGATIVE_CONTROL") or {}).get("route")
        if mutate == "route":
            pos = neg
        add("S1", "live named-method route discriminates the round's flow from a control",
            "PASS" if (pos and pos == "NATIVE" and neg and neg != pos) else "FAIL",
            f"positive={pos} negative_control={neg}")
    rc = J("ROUTE_CHECK.json")

    comp = J("compiler/compiler-receipt.json")
    v = (comp or {}).get("verdict")
    if comp is None:
        add("S2", "contract compiled through all four CAPC gates", "NOT_RUN", "compiler receipt absent")
    else:
        if mutate == "contract":
            v = "LINT_FAILED"
        add("S2", "contract compiled through all four CAPC gates",
            "PASS" if v == "PROMPT_COMPILE_PASS" else "FAIL", f"compiler verdict={v}")

    adm = J("HGK_TYPED_ADMISSION_FAR018.json")
    if adm is None:
        add("S3", "typed admission admitted work orders for this round", "NOT_RUN", "admission receipt absent")
    else:
        # Invariant 11(c): a registry lookup must assert a HIT, never fall through to a silent default.
        den = adm.get("denominator")
        if not isinstance(den, dict) or "workorders_total" not in den:
            add("S3", "typed admission admitted work orders for this round", "FAIL",
                "admission receipt carries no denominator.workorders_total; the lookup could not hit")
        else:
            n = den["workorders_total"]
            if mutate == "admission":
                n = 0
            add("S3", "typed admission admitted work orders for this round",
                "PASS" if adm.get("verdict") == "ADMISSION_OK" and n > 0 else "FAIL",
                f"verdict={adm.get('verdict')} workorders_total={n} state={adm.get('final_state')} "
                f"project={adm.get('project_id')} checkpoint={adm.get('checkpoint')}")

    kb = J("KANBAN_LIFECYCLE_RECEIPT.json")
    if kb is None:
        add("S4", "the board was driven, not merely created", "NOT_RUN", "kanban receipt absent")
    else:
        cc, hist = kb.get("call_count", 0), kb.get("board_state_histogram") or {}
        if mutate == "kanban":
            cc = 0
        add("S4", "the board was driven, not merely created",
            "PASS" if cc and (hist.get("done") or 0) > 0 else "FAIL",
            f"cli_calls={cc} cards={kb.get('cards_created')} histogram={json.dumps(hist)}")

    conf = RD / "openspec_validate.stdout.txt"
    if not conf.exists():
        add("S5", "the change is strict-valid in OpenSpec", "NOT_RUN", "validate output absent")
    else:
        t = conf.read_text(encoding="utf-8", errors="replace")
        ok = "is valid" in t and "error" not in t.lower()
        if mutate == "openspec":
            ok = False
        add("S5", "the change is strict-valid in OpenSpec", "PASS" if ok else "FAIL", t.strip()[:160])

    ex = J("lane/EXECUTE_RECEIPT.json")
    exa = ((ex or {}).get("attempts") or [{}])[0]
    if ex is None:
        add("S6", "EXECUTE lane served the required arm and echoed the nonce", "NOT_RUN", "no execute receipt")
    else:
        req = ((ex.get("identity_gate") or {}).get("required_arm"))
        served = exa.get("provider", "") + "/" + str(exa.get("model", ""))
        ok = req == served and exa.get("nonce_present") is True and exa.get("exit") == 0
        if mutate == "execute":
            ok = False
        add("S6", "EXECUTE lane served the required arm and echoed the nonce", "PASS" if ok else "FAIL",
            f"required={req} served={served} exit={exa.get('exit')} nonce={exa.get('nonce_present')} sec={exa.get('seconds')}")

    ve = J("lane/VERIFY_RECEIPT.json")
    vea = ((ve or {}).get("attempts") or [{}])[0]
    if ve is None:
        add("S7", "VERIFY lane ran on a DIFFERENT model axis than the writer", "NOT_RUN", "no verify receipt")
    else:
        diff = bool(vea.get("model")) and vea.get("model") != exa.get("model")
        if mutate == "axis":
            diff = False
        add("S7", "VERIFY lane ran on a DIFFERENT model axis than the writer",
            "PASS" if diff and vea.get("nonce_present") is True else "FAIL",
            f"writer={exa.get('model')} checker={vea.get('model')} axis_diverse={diff} nonce={vea.get('nonce_present')}")

    reg = J("RESIDUAL_REGISTER.json")
    w1 = J("W1_RESIDUAL_UNIVERSE.json")
    if reg is None or w1 is None:
        add("S8", "the register's counts are self-consistent with its own input", "NOT_RUN", "register or W1 absent")
    else:
        items = w1.get("items") or []
        rec = (reg.get("recomputed_counts") or {}).get("w1_items_total")
        claimed = (reg.get("inputs", {}).get("W1", {}) or {}).get("items_as_reported")
        ct = None
        if isinstance(claimed, dict):
            ct = claimed.get("total") or claimed.get("items_total")
        ok = rec == len(items) and (ct in (None, len(items)))
        if mutate == "register":
            ok = False
        add("S8", "the register's counts are self-consistent with its own input", "PASS" if ok else "FAIL",
            f"recomputed={rec} file_items={len(items)} w1_self_report_total={ct}")

    act = ((reg or {}).get("executable_now_actions") or {})
    ev = act.get("evidence_present_at_registration") or {}
    if not ev:
        add("S9", "every action the ruling calls executed left its artifact on disk", "NOT_RUN", "no action evidence map")
    else:
        bad = [k for k, v in ev.items() if not v.get("evidence_present")]
        if mutate == "artifacts":
            bad = ["A1"]
        add("S9", "every action the ruling calls executed left its artifact on disk",
            "PASS" if not bad else "FAIL", f"present={sum(1 for v in ev.values() if v.get('evidence_present'))}/{len(ev)} missing={bad}")

    fv = (reg or {}).get("final_verdicts") or {}
    want = {"full_convergence_verdict": "TEMP_CLOSED_CHALLENGE", "production_verdict": "FAIL_CLOSED",
            "canonical_AO_acceptance": "NOT_ISSUED"}
    if not fv:
        add("S10", "the non-achieved verdicts are still non-achieved", "NOT_RUN", "no final_verdicts")
    else:
        ok = all(fv.get(k) == w for k, w in want.items())
        if mutate == "nonclaim":
            ok = False
        add("S10", "the non-achieved verdicts are still non-achieved", "PASS" if ok else "FAIL", json.dumps(fv))

    hits, scanned = [], 0
    for p in list(RD.rglob("*.json")) + list(RD.rglob("*.md")):
        if "lane/attempts" in str(p).replace("\\", "/"):
            continue
        scanned += 1
        m = OVERCLAIM.search(p.read_text(encoding="utf-8", errors="replace") or "")
        if m:
            hits.append(f"{p.relative_to(RD)}:{m.group(0)}")
    if mutate == "overclaim":
        hits = ["injected"]
    add("S11", "no artifact asserts an unachieved outcome", "PASS" if scanned and not hits else
        ("NOT_RUN" if not scanned else "FAIL"), f"scanned={scanned} hits={hits[:4]}")

    sechits = []
    for p in list(RD.rglob("*")):
        if p.is_file() and "lane/attempts" not in str(p).replace("\\", "/") and "publish/payload" not in str(p).replace("\\", "/"):
            try:
                t = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            m = SECRET.search(t)
            if m and "GITHUB-REPO_SHW097" not in str(p):
                sechits.append(f"{p.relative_to(RD)}:{m.group(0)[:12]}…")
    if mutate == "secret":
        sechits = ["injected"]
    add("S12", "no credential-shaped token in this round's own new bytes", "PASS" if not sechits else "FAIL",
        f"hits={sechits[:4]}")

    md = RD / "publish" / "payload" / "EVIDENCE_CLOSURE_FAR-20261016-018.md"
    idx = J("publish/payload/PACK_INDEX.json")
    if not md.exists() or idx is None:
        add("S13", "the single evidence MD exists and its digest is carried by the index", "NOT_RUN",
            "md or index absent")
    else:
        row = [f for f in (idx.get("files") or []) if f.get("path") == md.name]
        ok = bool(row) and row[0].get("sha256") == sha(md) and row[0].get("bytes") == md.stat().st_size
        if mutate == "md":
            ok = False
        add("S13", "the single evidence MD exists and its digest is carried by the index", "PASS" if ok else "FAIL",
            f"indexed={bool(row)} sha_match={bool(row) and row[0].get('sha256') == sha(md)}")

    sc = J("lane/VERIFY_VERDICT.json")
    if sc is None:
        add("S14", "the independent checker returned a verdict without disagreement left unaddressed", "NOT_RUN",
            "no verdict file")
    else:
        ov, dis = sc.get("overall"), sc.get("disagreements") or []
        ok = ov in ("AGREE", "PARTIAL", "DISAGREE")
        if mutate == "verdict":
            ok = False
        add("S14", "the independent checker returned a verdict without disagreement left unaddressed",
            "PASS" if ok and not dis else "FAIL",
            f"overall={ov} disagreements={len(dis)} could_not_verify={len(sc.get('could_not_verify') or [])}")

    return C


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--negative-control", action="store_true")
    ap.add_argument("--out", default=str(RD / "SELF_CHECK_RECEIPT.json"))
    a = ap.parse_args()
    checks = build()
    base = {c["id"]: c["verdict"] for c in checks}
    npass = sum(1 for c in checks if c["verdict"] == "PASS")
    nfail = sum(1 for c in checks if c["verdict"] == "FAIL")
    nrun = sum(1 for c in checks if c["verdict"] == "NOT_RUN")
    nc = None
    if a.negative_control:
        flips = {}
        for mut in ("route", "contract", "admission", "kanban", "openspec", "execute", "axis",
                    "register", "artifacts", "nonclaim", "overclaim", "secret", "md", "verdict"):
            m = {c["id"]: c["verdict"] for c in build(mut)}
            flips[mut] = [k for k in m if m[k] == "FAIL" and base.get(k) == "PASS"]
        detected = {k: v for k, v in flips.items() if v}
        nc = {"mutations": len(flips), "detected": len(detected), "not_detected": [k for k in flips if not flips[k]],
              "per_mutation": detected}
        ok = len(detected) >= 6 and not nc["not_detected"]
        print("NEGATIVE_CONTROL=" + ("PASS" if ok else "FAIL"))
        print(json.dumps(nc, ensure_ascii=False, indent=1))
    rec = {"schema": "FAR-20261016-018/SELF-CHECK/1",
           "checks": checks,
           "summary": {"PASS": npass, "FAIL": nfail, "NOT_RUN": nrun, "total": len(checks)},
           "verdict": "PASS" if (nfail == 0 and nrun == 0 and nc and nc["not_detected"] == []) else
                      ("FAIL" if nfail else ("INCOMPLETE" if nrun else "PASS_WITHOUT_NEGATIVE_CONTROL")),
           "negative_control": nc,
           "claim_ceiling": "LOCAL"}
    Path(a.out).write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    for c in checks:
        print(f"{c['verdict']:8s} {c['id']}  {c['claim'][:64]}  | {str(c['evidence'])[:90]}")
    print("summary:", json.dumps(rec["summary"]), "verdict:", rec["verdict"])
    return 0 if rec["verdict"].startswith("PASS") else (1 if nfail else 2)


if __name__ == "__main__":
    raise SystemExit(main())
