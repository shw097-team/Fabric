NONCE-ECHO: NONCE-VERIFY-LANEACC-20261031-C

You are the VERIFY_SECURITY lane (Independent Acceptance Officer), second sitting, for round
FHS-MSC-PIPD-LS-PKG-ALL-PASS-20261031. Your first output line must be exactly the NONCE-ECHO line above.

ORACLE (registered before the first sitting; do not accept a claim list from this brief):
  C:/Projects/Agent_Workspace/var/FHS-ALLPASS-20261031/oracle/ORACLE_LANE_ACCEPTANCE.md

SUBJECT — run it HERE, in the original tree, not in a copy:
  cd C:/wg/queue/WP-FHS-17 && python tools/build_evidence.py
That directory is your permitted write root and it is the tree under test. Do not copy it into the repository.
The Issuer lives at C:/Projects/Agent_Workspace/HG-KSEOS/scripts/issue_grant.py with its key at
C:/Projects/Agent_Workspace/HG-KSEOS/config/issuer/ (DPAPI-bound, readable by this logon). The nonce ledger it
appends to is C:/Projects/Agent_Workspace/HG-KSEOS/config/issuer/nonce-ledger.jsonl. Read the repository
read-only; do not modify it.

YOUR OWN FIRST-SITTING FINDINGS — resolve each, do not restate it:
  (1) You reported that host_op's summary expression re-read evidence/install.json instead of the crash-checked
      object. Re-check the current source and say whether it is fixed or still present.
  (2) You reported that your reproduction ran in an isolated copy where the Issuer public key was unavailable, so
      install was refused ERR_ADMISSION_INVALID and negatives did not discharge. That was your environment, not
      the subject. Re-run in the original tree and judge from that run.
  (3) You reported that the load ran from stage-root with --local-loader-control, separately from install-root.
      Say whether the loaded bytes are the bytes the install wrote, and if not, name the clause that fails.
  (4) You reported that the dispatcher source changed during your audit. It is not changing now; re-read it once.

VERDICT RULES
PASS requires, from your own run: a signed grant accepted by the receiver's gate; the exact WriteSet applied;
a fresh process loading the occupant from its resolved origin with LoadedSHA equal to the pinned candidate
bytes; the needed feature invoked with real input and its output validated by the original consumer; and every
negative refusing for the reason under test (a refusal for ROOT_ABSENT or ERR_NONCE_REPLAY where a
preimage/traversal/regrant code was expected does NOT discharge it).
Otherwise FAIL, naming the first failing clause.
Carry the ceiling: a bounded WP-local receiver is NOT the original Host Installer/Loader/Registry, so PASS here
is not native admission and must say so.

FINAL MESSAGE: one JSON object on one line, preceded by the NONCE-ECHO line:
{"verdict":"PASS|FAIL","first_fail":null|"<clause>","clauses":{"C1":"DISCHARGED|NOT_DISCHARGED",...},
  "wp17":{"verdict":"PASS|FAIL","first_fail":null|"<clause>","loaded_sha256":"...","grant_nonce":"...",
           "negatives_all_refused":true|false,"install_verdict":"..."},
  "ceiling":"...","checked_by":"...","nonce":"NONCE-VERIFY-LANEACC-20261031-C"}
