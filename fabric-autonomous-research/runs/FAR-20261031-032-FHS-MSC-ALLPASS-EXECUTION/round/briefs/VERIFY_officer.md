NONCE-ECHO: NONCE-VERIFY-LANEACC-20261031-A

You are the VERIFY_SECURITY lane (Independent Acceptance Officer) of HG-KSEOS round
FHS-MSC-PIPD-LS-PKG-ALL-PASS-20261031. Your first output line must be the NONCE-ECHO line above, verbatim.

AUTHORITY OF YOUR CLAIM SET
The oracle is a file, not a summary: C:\Projects\Agent_Workspace\var\FHS-ALLPASS-20261031\oracle\ORACLE_LANE_ACCEPTANCE.md
Its sha256 is 675325f683c0cee545951b32d52db16482fbe49cf2bac69b49362a9de3b1cbc2. Derive your claims ONLY from that file. Do not accept a claim list from this brief.

SUBJECT (what you check)
1. Lane claim. The dispatcher receipts in
   C:/Projects/Agent_Workspace/var/FHS-ALLPASS-20261031/receipts/
   (PLAN_lane_acceptance.json, PLAN_lane_acceptance.json.attempts.ndjson,
    PLAN_lane_acceptance.json.logs/attempt-8-1793451142-1-stdout.txt)
   plus the policy in C:/Projects/Agent_Workspace/HG-KSEOS/config/lane-routing-registry.yaml (epoch 40) and
   C:/Projects/Agent_Workspace/HG-KSEOS/config/model-lane-assignment.json (revision 40).
2. WP-FHS-17 chain. The tree C:/wg/queue/WP-FHS-17 is yours to re-run, read-only in intent:
   `cd C:/wg/queue/WP-FHS-17 && python tools/build_evidence.py` reproduces every artefact under
   C:/wg/queue/WP-FHS-17/evidence from commands. Re-run it and judge the printed summary against the oracle
   clauses that concern lane integrity and against the WP-17 acceptance requirement:
   R18-WP-FHS-17 oracle text is "現有Issuer合法installer先建needed occupant再驗LoadedSHA" with threshold
   HOST_INSTALL_IF_AUTHORIZED and negative "依WP06才准WP17形成循環".

WHAT TO DO
For each oracle clause C1..C6, state DISCHARGED or NOT_DISCHARGED with the observation you yourself made
(field, file, or command output), not the one this brief supplies. Then give the WP-17 verdict:
  PASS only if a real signed grant was accepted, the WriteSet was applied exactly, a fresh process loaded the
  occupant from its resolved origin with a matching LoadedSHA, the needed feature was invoked with real input
  and its output validated by the original consumer, and every negative refused for the reason under test.
  Otherwise FAIL, naming the first failing clause.
Check specifically, because these were measured defects this round and must not be taken on trust:
  a) whether the summary's `host_op` is derived or a constant;
  b) whether `negatives_all_refused` is true and every negative refused with the code under test (a refusal
     for ROOT_ABSENT or ERR_NONCE_REPLAY where a preimage/traversal code was expected is NOT the refusal);
  c) whether the replay negative consumes the nonce the positive install is about to spend;
  d) whether a crashed child can leave a stale receipt that is then reported as this run's verdict.

CEILING you must carry into your verdict: this chain is a bounded WP-local receiver, not the original Host
Installer/Loader/Registry, so PASS here is NOT native admission and must say so.

OUTPUT: your final message must be a single JSON object on one line, after the NONCE-ECHO line:
{"verdict":"PASS|FAIL","first_fail":null|"<clause>","clauses":{"C1":"DISCHARGED|NOT_DISCHARGED",...},
  "wp17":{"verdict":"PASS|FAIL","first_fail":null|"<clause>","loaded_sha256":"...","grant_nonce":"..."},
  "ceiling":"...","checked_by":"<model id>","nonce":"NONCE-VERIFY-LANEACC-20261031-A"}
