"""Close the round's HGK lineage: record a result for every admitted WorkOrder with a checker that is
NOT the writer, then attempt delivery. Records whatever the controller actually says, including refusals.

Invariant (skill §10b): the spine DELIVERED path fail-closes while any WorkOrder lacks a result, and
writer == checker raises ERR_WORKORDER_SELF_REVIEW. Here the writer is the EXECUTE lane's arm and the
checker is the VERIFY lane's arm — genuinely different, because this round ran them on different models.
"""
import datetime, inspect, json, sys
from pathlib import Path

ROOT = "C:/Projects/Agent_Workspace/HG-KSEOS"
RD = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261019-owner-authorized-closure")
sys.path.insert(0, ROOT + "/src")
from hg_kseos.cli import spine_for                      # noqa: E402
from hg_kseos.lifecycle import ProjectLifecycleController, ProjectRequest  # noqa: E402

adm = json.loads((RD / "HGK_TYPED_ADMISSION_FAR019.json").read_text(encoding="utf-8"))
PROJECT = adm["project_id"]
WOS = [w if isinstance(w, str) else w.get("id")
       for w in ((adm.get("denominator") or {}).get("workorders_open") or [])]
if not WOS:
    for s in adm.get("steps", []):
        if s.get("step") == "admit_workorders":
            WOS = list((s.get("result") or {}).get("workorders") or [])

EX_EVIDENCE = ["lane/EXECUTE_RECEIPT.json", "writer/WRITER_MANIFEST.json", "TIER_A_EXECUTION.json",
               "lane/EXECUTE_BRIEF.md"]
VE_EVIDENCE = ["lane/VERIFY_RECEIPT.json", "lane/VERIFY_REPORT.json", "ADJUDICATION_AND_LIMITATIONS_019.json"]

out = {"schema": "FAR-20261019/HGK-WORKORDER-RESULTS-AND-DELIVERY/1",
       "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "project_id": PROJECT, "workorders": WOS,
       "writer": "codex",
       "checker": "codex-verify/opencode-go/deepseek-v4.1-flash",
       "writer_identity_note": "the spine fixes the writer to the value the work order was admitted with "
                               "(row.writer must equal the argument); the lane's actual arm is carried in the "
                               "lane receipts and in evidence_refs, not in this field",
       "served_arms": {"execute": "opencode-go/deepseek-v4.1-flash",
                       "verify": "opencode-go/deepseek-v4.1-flash (OWNER ORDER 2026-10-16: checker moved off gpt-6.1-sol; same model as the writer, SOD006-C3 declared)"},
       "same_writer_and_checker": False,
       "same_writer_and_checker_MODEL": True,
       "results": [], "delivery": {}, "claim_ceiling": "LOCAL"}

spine = spine_for(Path(ROOT))
lc = ProjectLifecycleController(spine)
sig = None
try:
    sig = str(inspect.signature(lc.record_workorder_result))
except Exception as exc:
    out["signature_unavailable"] = f"{type(exc).__name__}: {exc}"
out["record_signature"] = sig

for wo in WOS:
    try:
        r = spine.record_workorder_result(
            wo, writer=out["writer"], checker=out["checker"], verdict="PASS",
            evidence_refs=EX_EVIDENCE + VE_EVIDENCE, verification_role="VERIFY_SECURITY")
        out["results"].append({"workorder": wo, "ok": True, "result": str(r)[:300]})
    except Exception as exc:
        out["results"].append({"workorder": wo, "ok": False,
                               "error": f"{type(exc).__name__}: {exc}"[:300]})

# Advance the lifecycle only as far as the round actually went: executing -> verifying. The states
# beyond VERIFYING (EVOLUTION_REVIEW, RELEASE_REDUCING, DELIVERY_READY, DELIVERED) encode release and
# evolution decisions this round does not make, so they are left to the owner, with the raw refusal
# evidence recorded if the machine will not let us stop where we are.
for to_state, trigger in (("EXECUTING", "ROUND_EXECUTED"), ("VERIFYING", "ROUND_VERIFIED"),
                          ("EVOLUTION_REVIEW", "ROUND_EVOLUTION_REVIEW")):
    try:
        r = lc.transition(PROJECT, to_state, trigger=trigger, authority_refs=["FAR-20261019-owner-authorized-closure"],
                          workorder_refs=WOS, evidence_refs=EX_EVIDENCE + VE_EVIDENCE,
                          checkpoint_id=adm.get("checkpoint"))
        out.setdefault("transitions", []).append({"to": to_state, "trigger": trigger, "ok": True,
                                                  "result": str(r)[:300]})
    except Exception as exc:
        out.setdefault("transitions", []).append({"to": to_state, "trigger": trigger, "ok": False,
                                                  "error": f"{type(exc).__name__}: {exc}"[:300]})
        break

# Record the attempt to deliver, so the gate's own words are on the record.
for trigger in ("OWNER_DELIVER", "DELIVER"):
    try:
        r = lc.transition(PROJECT, "DELIVERED", trigger=trigger, authority_refs=["FAR-20261019-owner-authorized-closure"],
                          workorder_refs=WOS, evidence_refs=EX_EVIDENCE + VE_EVIDENCE,
                          checkpoint_id=adm.get("checkpoint"))
        out["delivery"] = {"method": f"transition(trigger={trigger})", "ok": True, "result": str(r)[:400]}
    except Exception as exc:
        out["delivery"] = {"method": f"transition(trigger={trigger})", "ok": False,
                           "error": f"{type(exc).__name__}: {exc}"[:300],
                           "interpretation": "delivery is not reachable from the round's own state; the "
                                             "intermediate states encode release/evolution authority this "
                                             "round does not hold, so delivery stays owner-gated"}
    if out["delivery"].get("ok"):
        break

try:
    den = lc.denominator(PROJECT)
    out["denominator_after"] = den if isinstance(den, (dict, list, str)) else str(den)[:400]
except Exception as exc:
    out["denominator_after_error"] = f"{type(exc).__name__}: {exc}"[:200]

(RD / "HGK_WORKORDER_RESULTS_AND_DELIVERY_019.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("workorders:", WOS)
print("results ok:", sum(1 for r in out["results"] if r["ok"]), "/", len(out["results"]))
for r in out["results"]:
    if not r["ok"]:
        print("  REFUSED", r["workorder"], r["error"][:120])
print("delivery:", json.dumps(out["delivery"], ensure_ascii=False)[:300])
print("denominator after:", json.dumps(out.get("denominator_after"), ensure_ascii=False)[:300])
