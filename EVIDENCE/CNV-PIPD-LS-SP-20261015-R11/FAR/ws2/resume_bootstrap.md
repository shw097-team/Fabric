# Resume bootstrap — read-FIRST list for a brand-new session

Claim ceiling in force everywhere below: **LOCAL / candidate-only** — nothing is an acceptance, a Gate
PASS, an AO verdict or a release until an EXTERNAL acceptance officer accepts.

Read in this order. Every entry is verified to exist on this host (measured 2026-10-16 14:13–14:47 UTC+8).

## 1. R11/FAR/ws2/resume_bootstrap.md — this file (you are here)
Single entry point that names everything else.

## 2. HG-KSEOS AGENTS.md — the operating contract
`C:/Projects/Agent_Workspace/HG-KSEOS/AGENTS.md` (14,055 B). Read before any write: it defines the
write-root discipline, the maker≠checker≠AO rule, and the no-self-approval rule that every round
constraint traces to.

## 3. Skills to load (via skill_view, in this order)
1. **hgk-agent-lifecycle-admission** → actual name on this host: `hgk-lifecycle-admission`
   (top-level skill dir, `<HERMES_HOME>/skills/hgk-lifecycle-admission/SKILL.md`, 35,739 B —
   NOT under software-development/). Typed HGK admission: how every gain of authority is made.
2. **hgk-governed-execution** (`<HERMES_HOME>/skills/software-development/hgk-governed-execution/SKILL.md`,
   21,026 B). Governance-grade execution rules post-slim. KNOWN DEFECT: it names `entry_map.json`
   at lines 66/71 (ERR_ENTRY_MAP_* stop rule) and **that file does not exist** in the live skill dir —
   do not treat the missing pointer as a STOP, record it and continue (see RES-SKILL-01).
3. **hgk-kanban-and-lane-routing** (`<HERMES_HOME>/skills/software-development/hgk-kanban-and-lane-routing/SKILL.md`,
   89,271 B — regrew from 86,198 on 2026-10-16). Lane dispatch, pool-vs-registry, board discipline.
4. **adversarial-verification-rounds** (`<HERMES_HOME>/skills/software-development/adversarial-verification-rounds/SKILL.md`)
   — how checker rounds are structured on this host.
5. **remote-repo-publication** (`<HERMES_HOME>/skills/software-development/remote-repo-publication/SKILL.md`)
   — packet prepare / M2 gate / push / blob-by-blob readback / Draft PR.

## 4. Authority anchors (both under HERMES_HOME attachments) — READ, DO NOT PRINT/QUOTE SECRET-LIKE CONTENT
- **PKG v2.0.0 (SOLE AUTHORITY)**:
  `C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/attachments/Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md`
  (2,689,181 B, sha256 96d9d564…9c3f).
- **EIA R6 external report**: `.../hermes/attachments/Fabric_Convergence_External_Independent_Acceptance_Report_20261015.md`
  (33,616 B): scope PARTIAL_CHALLENGE / merge CONDITIONAL_GO after M1–M3 / production FAIL_CLOSED.
- **R10 closure set (the newest recorded state, older than the 14:13 registry rebind)**:
  `.../_handover/CNV-PIPD-LS-SP-20261015-R10/HANDOVER_R10.md` → `SESSION_LEDGER_R10.json` →
  `R10_CHANGE_RECORD_ADJUDICATION.json` → `R10_VERIFY/R10_VERDICT.json` (+ADJUDICATION) →
  `R10_OWNER_READY_LANE_REBIND.json` → `SELF_EVOLUTION_R10.md`.
- **R9 ledger (deeper backlog)**: `.../_handover/CNV-PIPD-LS-SP-20261015-R9/R9_LEDGER.json`.
- **R11 in-flight state**: `.../_handover/CNV-PIPD-LS-SP-20261015-R11/HGK_TYPED_ADMISSION_R11.json`
  (ADMISSION_OK, 6 workorders CREATED, acceptance NOT_RUN), `RESUME_MANIFEST.json` (open_items
  EMPTY — do not trust its promise), `OPEN_RECORDS_INVENTORY.tsv` (24 records / 371 open rows).

## 5. Lane dispatch helper that exists
- **Use this one**: `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R10/tooling/dispatch_r10.py`
  (12,497 B, sha256 prefix a308b1cea808d2af; `python -m pytest -q test_dispatch_r10.py` = **8 passed**,
  re-run fresh this session). Per-turn immutable receipts + nonce attestation.
- Predecessors `dispatch_r6.py` / `R9/dispatch_r9.py` are BYTE-UNCHANGED by design — never edit them.
- Pre-flight the lane POOL before spending a turn: a mandated arm absent from the pool fail-closes
  `ERR_LANE_REQUIRED_ARM_ABSENT` (that is a routing absence, not a model outage). The registry-declared,
  lane-pooled, provider-reachable and attempt-served surfaces are FOUR different facts (R10 LN-11).

## 6. Registry — re-measure, never trust a handover's numbers
`cd C:/Projects/Agent_Workspace/HG-KSEOS && PYTHONPATH=src ./.venv/Scripts/python.exe -c "from hg_kseos
import lane_policy as L; r=L.load_registry(); print(r.get('epoch')); [print(L.route_for_lane(r,l)) for l
in ('PLAN','EXECUTE','VERIFY_SECURITY')]; print(L.check_drift(registry=r)); print(L.check_sod(L.route_for_lane(r,'EXECUTE'),L.route_for_lane(r,'VERIFY_SECURITY')))"`
**Measured this session (14:13:29, epoch 22, sha256 02481992df124ca4…):**
PLAN = opencode-go/glm-5.3-flash (ADMITTED); EXECUTE = VERIFY_SECURITY =
opencode-go/deepseek-v4.1-flash (both UNPROVEN); drift []; **check_sod(EXECUTE,VERIFY)=SOD_VIOLATION**
(the same-arm maker/checker pair the owner ordered; R10's PLAN/VERIFY violation is resolved).
The registry is UNTRACKED local control-plane state — never edit it to make your own dispatch succeed.

## 7. Protected / hands-off (violating any of these is a mission failure)
- **Guard subject** `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/` —
  HANDS-OFF, never write/modify.
- All **published EVIDENCE/** packets in R6..R10 round roots — never rewrite existing commits.
- **Peer in-flight surfaces, READ-ONLY**: Fabric checkout on branch
  `pub/far-remediation-and-closure-20261016` (2 untracked entries); PIPD worktree
  `C:/Projects/Agent_Workspace/PIPD/worktrees/r8-wt` (3 uncommitted modified files, R9 lane output).
  Never switch, clean or reset them.
- **No git write commands**; publication goes through the round's publish script cutting a fresh
  worktree off `origin/main`; no force-push.
- **Never edit the lane registry or lane slots** to make your own dispatch succeed — route provider-direct
  and disclose, or fail closed and report.
- Do not write outside your own round root; openspec records, config and skill files are not yours to edit
  unless your admission names that write root.

## 8. Credential path
`C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt` — **EXISTS (93 B)**. Name only: the
publication script reads it into memory; it must never enter argv, a URL, a log or an artifact, and no
value is ever opened or printed. M2 secret-scan posture from R10: hard secrets 0 across 69 blobs.

## 9. Hard rule reminders that keep getting re-learned
- change records are CLAIMS about state — measure before adjudicating any row (R10 LN-13).
- a 0-byte reading of a live file is a PROBE result, never a corruption finding; re-read or hash twice.
- a verdict that names no revision (bytes+sha256) is not reproducible — publish the tested revision.
- a claim about the PAST that cannot be re-measured is recorded NOT RE-MEASURABLE; never supply a
  plausible mechanism the write log does not support.
