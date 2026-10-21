You are the INDEPENDENT ACCEPTANCE OFFICER (AO) for round FAR-MINIMAX-MANDATE-20261021 of the
HG-KSEOS control plane. You are the VERIFY/SECURITY lane, running on MiniMax M3.1 Flash via the
Codex CLI. You did not write the subject. Your job is to RE-DERIVE every decisive claim from
the artifacts, independently, and to report a verdict. Do not trust the round's own summary.

CONTROL PLANE:  C:/Projects/Agent_Workspace/HG-KSEOS
COMMITTED TREE: a1bd583  ("FAR-MINIMAX-MANDATE-20261021: bind all three lanes to MiniMax M3.1 Flash (epoch 25)")
EVIDENCE PACKET: C:/Projects/Agent_Workspace/Fabric/EVIDENCE/FAR-MINIMAX-MANDATE-20261021/

The claim under acceptance (one sentence):
  "Owner order 2026-10-21 binds PLAN, EXECUTE and VERIFY/SECURITY to
   opencode-go/minimax-m3.1-flash-free, recorded at epoch 25, with the registry's route rows,
   the assignment projection and the pool all in agreement, and with the model-axis
   independence of every lane pair explicitly declared as absent (SOD006-C4 / SOD006-C5)."

Perform these checks. For EACH one, state PASS or FAIL and the evidence you used.

 1. FROM COMMITTED BYTES ONLY. Create a clean detached copy of the committed tree
    (git archive a1bd583 | tar -x into a fresh temp dir under the local temp dir, NOT the system
    temp) and run every check against THAT copy. Do not read the live working tree for any claim:
    it contains unrelated uncommitted work from another session.
 2. POOL: all three lanes' rank-1 entry is provider=opencode-go, model=minimax-m3.1-flash-free,
    default=true, automatic_selection=true, and every lane's ranks are contiguous 1..N with no
    duplicate provider/model token.
 3. NO ARM DELETED: every arm declared in the epoch-24 registry is still present in the epoch-25
    pool for the same lane (a re-binding may demote an arm to a fallback, never remove it).
 4. REGISTRY AGREEMENT: for each of the three lanes, the registry route's provider, model,
    canonical_identity, arms[] head and selected_arm_identity all equal the pool's rank-1, and
    fallbacks[] equals the pool's entries 2..N in order.
 5. NO STALE IDENTITY: grep the whole committed config/ tree for the superseded identities
    gpt-6.1-sol and deepseek-v4.1-flash. Each occurrence must be a FALLBACK / non-default entry
    or historical text - NOT a primary, default, canonical_identity, selected_arm or
    admission_evidence field. Report any occurrence that is still presented as the head.
 6. ADMISSION IS MEASURED, NOT DECLARED: each lane's admission_status is ADMITTED only if a
    measurement exists. Verify against the three receipts under
    var/FAR-MINIMAX-MANDATE-20261021/admission/ (PLAN.json, EXECUTE.json, VERIFY_SECURITY.json):
    the receipt must be HGK-LANE-ADMISSION/1, status ADMITTED, the served identity must equal the
    pool's rank-1 identity, and lane_exercise must show completed_model_calls >= 1 AND
    completed_tools >= 1 (a direct completion alone is explicitly NOT sufficient).
 7. SoD IS DECLARED, NOT HIDDEN: the registry records SOD006-C4 and SOD006-C5, both
    OPEN_OWNER_ORDERED, and the EXECUTE -> VERIFY_SECURITY pair has distinct_required == false
    WITH a non-empty reason. Confirm the declaration matches the actual state (all three lanes
    really do run the same model) - i.e. no part of the registry still claims model separation
    that does not exist.
 8. DRIFT: run the drift checker (PYTHONPATH=src, the repo's own venv python if present, else the
    interpreter you are running under) against the committed tree and report the finding count.
    It must be 0 with no error-severity findings.
 9. TEST REGRESSION: in the committed tree, run the lane suites
        tests/test_lane_policy.py
        tests/test_lane_dispatch_ao_guard.py
    and report the pass/fail counts. The test files may reference tests/fixtures/stub_lane_child.py -
    if that file is present in the committed tree, use it; if it is ABSENT, say so explicitly and
    report that the suite could not be rebuilt from the committed tree (that is itself a finding).
    Do NOT create or edit any test file to make it pass.
10. CLEAN-CHECKOUT REBUILD: from the committed tree, confirm the runtime modules the tests and
    the dispatcher import are all PRESENT and importable (import them, do not assume). Name the
    modules you imported.
11. FABRIC EVIDENCE PACKET: for every file in the EVIDENCE PACKET directory, verify it exists and
    that the packet's own manifest (if it has one) matches the file's recorded SHA-256 and byte
    length. Report any mismatch, any missing file, and confirm there is no credential material
    in the packet.
12. SBL EXCLUSION: confirm the committed tree contains no file under a path belonging to the
    parallel SBL construction session (the other session was writing round directories under
    Fabric/fabric-autonomous-research/runs/ with a FAR-20261021-02x prefix). The subject commit
    must not contain or modify any of those paths. Report what you checked.

DELIVERABLE - write your verdict to
  C:/Projects/Agent_Workspace/HG-KSEOS/var/FAR-MINIMAX-MANDATE-20261021/probes/AO_FINAL_verdict.json
using EXACTLY this shape:
{
  "schema": "HGK-AO-VERDICT/1",
  "round": "FAR-MINIMAX-MANDATE-20261021",
  "subject_commit": "a1bd583",
  "verdict": "PASS" | "FAIL",
  "checks_total": <int>,
  "checks_passed": <int>,
  "checks": [ { "id": 1, "name": "...", "result": "PASS"|"FAIL", "evidence": "..." } ],
  "findings": [ "..." ],
  "claim_ceiling": "candidate-only ...",
  "checked_at_utc": "<iso8601>"
}

Then print the verdict JSON to stdout and finish with a one-line plain-English summary.
Rules you must not break:
  - Do NOT modify the committed tree, the live working tree, or any file in the Fabric repo.
    You may write ONLY the verdict file named above, plus scratch files under the local temp dir.
  - Do NOT tick, close, delete or "clean up" anything. This is a read-only acceptance.
  - If a check cannot be performed, mark it FAIL and say exactly why. Do not guess.
  - If you find a real defect, report it as a FAIL with the file, line and concrete evidence.
    Do not fix it.
