You are the INDEPENDENT ACCEPTANCE OFFICER (AO) for round FAR-MINIMAX-MANDATE-20261021 of the
HG-KSEOS control plane. You are the VERIFY/SECURITY lane, running on MiniMax M3.1 Flash via the
Codex CLI. You did not write the subject. Report a verdict; do not fix anything.

A previous AO run timed out at 540s after completing checks 2 and 4, and check 4 FAILED. That
defect has since been fixed in commit 1cbb9d2. Your job is to verify the fix and complete the
remaining checks.

SUBJECT
  Commit          1cbb9d2  (parent a1bd583)
  Control plane   C:/Projects/Agent_Workspace/HG-KSEOS
  Clean copy      C:/Users/user/AppData/Local/Temp/ao-final-2  <- the COMMITTED tree at 1cbb9d2,
                  extracted with `git archive`. Use THIS, not the live working tree (which holds
                  another session's uncommitted work).
  Evidence packet C:/Projects/Agent_Workspace/Fabric/EVIDENCE/FAR-MINIMAX-MANDATE-20261021/

THE CLAIM UNDER ACCEPTANCE
  "Owner order 2026-10-21 binds PLAN, EXECUTE and VERIFY_SECURITY to
   opencode-go/minimax-m3.1-flash-free at epoch 25, with the pool, the registry's route rows
   and the assignment projection in agreement, the admission measured rather than declared, and
   the model-axis independence of every lane pair explicitly declared as absent."

BE EFFICIENT - you have a wall-clock limit. Do the checks in this order and stop analysing once
a check has a definite answer. Write the verdict file BEFORE you run out of time.

CHECK 1 - THE FIX FOR THE PREVIOUS FAILURE (do this first)
  In C:/Users/user/AppData/Local/Temp/ao-final-2/config/lane-routing-registry.yaml, for each of
  the three routes (PLAN, EXECUTE, VERIFY_SECURITY) read the route's TOP-LEVEL auth posture:
  auth, oauth, reasoning_effort. Read the same three fields from the pool's rank-1 entry in
  config/lane-route-slots.candidate.json. They must be EQUAL for all three lanes.
  The previous run recorded: PLAN and VERIFY_SECURITY had auth='openai_oauth', oauth=True,
  reasoning_effort='medium' while the pool said env_ref:OPENCODE_GO_API_KEY / False / None.
  Report PASS only if all three lanes now agree with the pool on all three fields.

CHECK 2 - POOL SHAPE
  For each of the three lanes: rank-1 entry is provider=opencode-go, model=minimax-m3.1-flash-free,
  default=true, automatic_selection=true; ranks are contiguous 1..N; no duplicate
  provider/model token within a lane.

CHECK 3 - NO ARM DELETED
  Every arm present in the epoch-24 registry is still present in the epoch-25 pool for the same
  lane. A re-binding may demote an arm to a fallback; it may not remove it.
  (The epoch-24 registry is in the git history: `git -C C:/Projects/Agent_Workspace/HG-KSEOS
  show a1bd583^:config/lane-routing-registry.yaml`. If that is slow, compare the epoch-25 pool's
  model set against the arm models named in the epoch-25 registry's own history array - if that
  is empty, say so and fall back to listing the pool's models and confirming gpt-6.1-sol,
  deepseek-v4.1-flash, glm-5.3-flash, gpt-6-luna and the nvidia deepseek are all present.)

CHECK 4 - REGISTRY vs POOL AGREEMENT (the one that failed before)
  For each lane, the registry route's provider, model, canonical_identity, arms[0] (provider,
  model, canonical_identity), selected_arm_identity must equal the pool's rank-1; fallbacks[] must
  equal the pool's entries 2..N in order; arms[] must equal the pool's entries 1..N in order.
  ALSO check the route-level auth posture again (as in check 1) - it is part of this check.

CHECK 5 - NO STALE IDENTITY
  In the committed tree's config/ directory, find every occurrence of gpt-6.1-sol and
  deepseek-v4.1-flash. Each must be a FALLBACK / non-default entry or historical text - never a
  primary, default, canonical_identity, selected_arm, admission_evidence or top-level route
  field. Report any occurrence still presented as the head of a chain.

CHECK 6 - ADMISSION IS MEASURED
  Each lane's admission_status must be ADMITTED only if a measurement exists. Verify against
  C:/Projects/Agent_Workspace/HG-KSEOS/var/FAR-MINIMAX-MANDATE-20261021/admission/{PLAN,EXECUTE,VERIFY_SECURITY}.json:
  schema must be HGK-LANE-ADMISSION/1, status ADMITTED, served identity must equal the pool's
  rank-1 identity, and lane_exercise must show completed_model_calls >= 1 AND completed_tools >= 1
  (a direct completion alone is explicitly NOT sufficient).

CHECK 7 - SoD IS DECLARED, NOT HIDDEN
  The registry must record SOD006-C4 and SOD006-C5 as OPEN_OWNER_ORDERED, and the
  EXECUTE -> VERIFY_SECURITY pair must have distinct_required == false WITH a non-empty reason.
  Confirm the declaration matches the actual state (all three lanes really do run the same model) -
  i.e. no part of the registry still claims model separation that does not exist.

CHECK 8 - DRIFT
  Run: cd C:/Users/user/AppData/Local/Temp/ao-final-2 && set PYTHONPATH=src and run the repo's
  drift checker. Use the repo venv interpreter if it exists:
  C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe
  with PYTHONPATH=src and cwd set to the clean copy. The call is:
      python -c "from hg_kseos.lane_policy import check_drift; f=check_drift(); print(len(f)); [print(x) for x in f]"
  Report the finding count. It must be 0 with no error-severity findings.

CHECK 9 - CLEAN-CHECKOUT REBUILD
  From C:/Users/user/AppData/Local/Temp/ao-final-2, import the runtime modules the tests and the
  dispatcher need. The known set is hg_kseos.lane_policy, hg_kseos.lane_admission,
  hg_kseos.lane_route_resolver, hg_kseos.role_binding - but import what the code actually needs
  and name every module you imported. If any module is missing from the committed tree, that is a
  FAIL: name it.

CHECK 10 - TEST SUITE ON THE COMMITTED TREE
  In C:/Users/user/AppData/Local/Temp/ao-final-2 run:
      C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe -m pytest tests/test_lane_policy.py tests/test_lane_dispatch_ao_guard.py -q -p no:cacheprovider
  (set TMPDIR/TEMP/TMP to C:/Users/user/AppData/Local/Temp). Report the pass/fail counts.
  If tests/fixtures/stub_lane_child.py is absent from the committed tree, say so explicitly and
  report the suite could not be rebuilt - that is itself a finding.

CHECK 11 - EVIDENCE PACKET INTEGRITY
  For every file in C:/Projects/Agent_Workspace/Fabric/EVIDENCE/FAR-MINIMAX-MANDATE-20261021/,
  verify it exists and that PACKET_MANIFEST.json's recorded sha256 and byte length match the file
  on disk. Report mismatches, missing files, and whether any credential material is present.
  (Note: the packet also contains a copy of the committed governed configs - compare the packet's
  governed-config/lane-routing-registry.yaml against the clean copy's config/lane-routing-registry.yaml
  and report whether they are byte-identical. The packet was built BEFORE the 1cbb9d2 fix, so a
  difference here is EXPECTED - report it as such, it is a staleness note, not a failure of the
  round. Then state which is newer.)

CHECK 12 - SBL EXCLUSION
  Confirm the committed tree (1cbb9d2) contains no file under a path belonging to the parallel SBL
  construction session (round directories under fabric-autonomous-research/runs/ with a
  FAR-20261021-02x prefix). Run: git -C C:/Projects/Agent_Workspace/HG-KSEOS show --stat --name-only
  1cbb9d2 and a1bd583, and list the files. Report exactly what you checked.

DELIVERABLE - write the verdict to
  C:/Projects/Agent_Workspace/HG-KSEOS/var/FAR-MINIMAX-MANDATE-20261021/probes/AO_FINAL2_verdict.json
in EXACTLY this shape:
{
  "schema": "HGK-AO-VERDICT/1",
  "round": "FAR-MINIMAX-MANDATE-20261021",
  "subject_commit": "1cbb9d2",
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
  - Do NOT modify the clean copy, the live working tree, or anything in the Fabric repo.
    You may write ONLY the verdict file, plus scratch files under C:/Users/user/AppData/Local/Temp.
  - Do NOT tick, close, delete or "clean up" anything. This is a read-only acceptance.
  - If a check cannot be performed, mark it FAIL and say exactly why. Do not guess.
  - If you find a real defect, report it as a FAIL with the file, the field and the concrete
    evidence. Do not fix it.
  - Write the verdict file as soon as you have enough information; a complete verdict that exists
    is worth more than a perfect verdict that does not.
