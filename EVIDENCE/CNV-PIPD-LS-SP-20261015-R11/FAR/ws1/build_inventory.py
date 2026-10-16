#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""WS1 — measured inventory of every open openspec change record (read-only worker).

All values below were measured live on 2026-10-16 by the parent session's commands
(ls/grep/validate/registry readbacks); this script only materialises the deliverables.
"""
import json, subprocess, os, datetime

WS1 = r"C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R11/FAR/ws1"
HGK = "C:/Projects/Agent_Workspace/HG-KSEOS"
CHANGES = HGK + "/openspec/changes"

# ---------------------------------------------------------------- live re-measure
rows_scan = {}
for d in os.listdir(CHANGES):
    p = os.path.join(CHANGES, d)
    if d == "archive" or not os.path.isdir(p):
        continue
    tm = os.path.join(p, "tasks.md")
    if not os.path.exists(tm):
        continue
    txt = open(tm, encoding="utf-8", errors="replace").read()
    done = sum(1 for l in txt.splitlines() if l.lstrip().startswith("- [x]") or l.lstrip().startswith("- [X]"))
    open_r = sum(1 for l in txt.splitlines() if l.lstrip().startswith("- [ ]"))
    newest, newest_f = 0.0, ""
    for root, _dirs, files in os.walk(p):
        for f in files:
            fp = os.path.join(root, f)
            m = os.path.getmtime(fp)
            if m > newest:
                newest, newest_f = m, os.path.relpath(fp, p)
    spec_md = os.path.exists(os.path.join(p, "spec.md")) or any(
        f == "spec.md" and "specs" in root for root, _d_, fs in os.walk(p) for f in _d_ or []
    )
    # spec.md blob: any spec.md file anywhere in the record (canonical location is specs/<cap>/spec.md)
    spec_md = False
    for root, _d_, fs in os.walk(p):
        if "spec.md" in fs:
            spec_md = True
            break
    rows_scan[d] = {"done": done, "open": open_r,
                    "mtime": datetime.datetime.fromtimestamp(newest).strftime("%Y-%m-%d %H:%M:%S"),
                    "mtime_file": newest_f, "spec_md": spec_md}

# raw validate output
val_file = os.path.join(WS1, "validate_raw.txt")
validate = {}
cur = None
for line in open(val_file, encoding="utf-8", errors="replace"):
    if line.startswith("###CMD: npx --no-install openspec validate "):
        name = line[len("###CMD: npx --no-install openspec validate "):].strip()
        name = name.replace(" --strict", "").strip()
        cur = name
        validate[cur] = {"raw": [], "exit": None}
    elif line.startswith("---exit: "):
        if cur: validate[cur]["exit"] = line.split()[-1]
    elif cur is not None and not line.startswith("---cwd"):
        validate[cur]["raw"].append(line.rstrip("\n"))

OPENSPEC_VERSION = "1.8.0"  # measured: `npx --no-install openspec --version` -> 1.8.0, exit 0

# ---------------------------------------------------------------- live evidence
LIVE = {
 "hgk-far-remediation-20261016":
   "YES var/FAR-REMEDIATION-AND-CLOSURE-20261016/ (ROUND_CLOSURE.json, GATE_REPORT.json GATE_PASS, PUBLICATION_RECEIPT.json Fabric PR #8 open, lanes/EXECUTE/R5|R5b, lanes/VERIFY_SECURITY/V3*)",
 "skill-mainfile-cap-remediation":
   "YES the live skill was slimmed in place (local SKILL.md now 21026 bytes LF 19658 chars, 100000-char cap never exceeded); R10 adjudication _handover/...-R10/R10_CHANGE_RECORD_ADJUDICATION.json measured the record STALE-not-the-work",
 "hgk-lane-reliability-closure-20261016":
   "YES var/LANE-RELIABILITY-CLOSURE-20261016/ (admission.json, CHANGESET_A_APPLY_RECEIPT.json epoch 19->20, lanes EXECUTE BC1-BC4 + VERIFY V1-V2 receipts, ROUND_CLOSURE.json with measured F1/SOD006-C2 residuals)",
 "hgk-r8-eia-closure-skill-slim-20261016":
   "YES _handover/CNV-PIPD-LS-SP-20261015-R8/ (HGK_TYPED_ADMISSION_R8.json, R8_LEDGER.json, WS_B verifier turn, publish_r9.py successor publication); round itself published packet + Draft PR #5",
 "hgk-r9-far-residual-closure-20261016":
   "YES _handover/CNV-PIPD-LS-SP-20261015-R9/ (HGK_TYPED_ADMISSION_R9.json project CNV-R9-RESIDUAL-CLOSURE, WS_A/WS_B applied hunks, R9_LEDGER.json, R9_VERIFY verdict UNVERIFIABLE adjudicated, R9_PUBLICATION_VERIFICATION.json)",
 "hgk-r10-session-closure-20261016":
   "YES _handover/CNV-PIPD-LS-SP-20261015-R10/ (admission CNV-R10-SESSCLOSE, SESSION_LEDGER_R10.json, R10_CHANGE_RECORD_ADJUDICATION.json 25 rows re-measured, HANDOVER_R10.md, R10_VERIFY/ ERR_LANE_REQUIRED_ARM_ABSENT fail-closed receipt)",
 "hgk-lane-brief-and-guard-hardening-20261015":
   "SUPERSEDED_TARGET YES / OWN_EXEC NO: R7 tooling findings TF-01..TF-09 are recorded in _handover/...-R8/R8_LEDGER.json; no round dir under HG-KSEOS/var/ executes this record's own tasks (record remains candidate)",
 "hgk-plan-plane-rebind-20261015":
   "YES the PLAN rebind it asks for is LIVE in the canonical registry (epoch 21 act 2026-10-16T12:36:30, later epoch 22 by round3) - measured via lane_policy.load_registry(): PLAN opencode-go/glm-5.3-flash, check_drift []; its unserved-receipt row closed by ROUND3-LANE-REBIND var receipt",
 "lane-model-chain-rebind-20261015":
   "YES var/FAR-LANE-ROUTE-REBIND-20261015/ (epoch 18 rebind applied live, E2E receipts EXECUTE+VERIFY ok, OWNER_DECISIONS_AND_HANDOVER.md D1-D4 owner decisions, publish branch far/lane-rebind-20261015-publish BLOCKED_CREDENTIALS)",
 "hgk-round3-lane-rebind-20261016":
   "YES var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016/ (admission.json, R1_R2_R3_APPLY_RECEIPT.json epoch 21->22, ORACLE_R10_RECEIPT 7/7, lanes, publication branch + gate report + PUBLICATION_RECEIPT.json round3)",
}

# ---------------------------------------------------------------- dispositions
D = lambda change, disp, action, locator, note: (change, disp, action, locator, note)

records = [
 ("gcm-noninteractive-default-containment", 36, 8, "no", "complex-but-stable PGDMB repair; its named PGDMB redesign work predates and does not match the current convergence mission",
  "CONTINUE", "Run the 8 [ ] PREP rows' rehearsal-prep sub-steps only under a new narrower PGDMB TASK_SPEC, or ask the owner to re-scope the record to the 3 demonstrably completable PGDRF items",
  "HG-KSEOS/openspec/changes/gcm-noninteractive-default-containment/tasks.md rows 3.1-3.9",
  "SoD gpt-6.1-sol verdict FAIL still stands; owner-only context"),
 ("hermes-incident-2026-10-05-repair", 0, 35, "no", "HNFR2 incident remediation; wholly predates the convergence mission scope (R6..R10 rounds)",
  "HISTORICAL", "Leave parked under HISTORICAL unless the owner re-opens the 2026-10-05 incident: no row references a convergence-round artifact",
  "HG-KSEOS/var/far-hermes-incident-rca-001/", "superseded by rounds R6..R10 evidence chain"),
 ("hgk-checker-upgrade-adapter", 0, 23, "no", "AVR-COV-11 checker-bridge upgrade; its 'T7' PGDMS rows and phase-2 TPGDW review rows are aspirational straight from design.md, none started",
  "CONTINUE", "Pick one MVP vertical slice (PGDTX runner + PGDLY verdict schema + 5 offline negatives) and dispatch it as a bounded EXECUTE turn, then tick that slice's rows",
  "HG-KSEOS/openspec/changes/hgk-checker-upgrade-adapter/tasks.md 1.1/2.1",
  "reference impl exists in worktrees/hgk-checker-upgrade-20261009 (checker-v2-r4fix) but is not admitted as this record's own run"),
 ("hgk-far-remediation-20261016", 0, 25, "no", "R6..R10 remediation record whose 26 rows were measurably executed by the peer round FAR-REMEDIATION-AND-CLOSURE-20261016 in var/",
  "CLOSE_CANDIDATE",
  "Owner (or an admitted successor record) ticks 1-25 as DONE-MEASURED, citing var/FAR-REMEDIATION-AND-CLOSURE-20261016/{ROUND_CLOSURE,GATE_REPORT,PUBLICATION_RECEIPT}.json as row evidence",
  "var/FAR-REMEDIATION-AND-CLOSURE-20261016/", "worker's 25 rows and the round's own rows differ slightly in numbering"),
 ("skill-mainfile-cap-remediation", 0, 11, "no", "R10 adjudication measured the record's premise SUPERSEDED for its target file (never exceeded 100000 LF chars; file slimmed to 21026 B) and 6 residual rows belong to the Skill Owner",
  "OWNER_DECISION",
  "Skill Owner decides: close the record citing R10_CHANGE_RECORD_ADJUDICATION.json (premise superseded), keeping only the 6 residual rows (regrowth guard / index completeness / independent recompute) as a successor record",
  "_handover/CNV-PIPD-LS-SP-20261015-R10/R10_CHANGE_RECORD_ADJUDICATION.json#per_change.skill-mainfile-cap-remediation",
  "rows T1-T11 all unticked although the file they describe is already post-slim"),
 ("hgk-lane-brief-and-guard-hardening-20261015", 0, 22, "no",
  "superseded target: this record's remediation rows were already superseded (PGDMC executed R6-R10 rounds)", "CLOSE_CANDIDATE",
  "Ask the owner: either discard the record (its TF-01/TF-08/TF-09 guard concerns were resolved live by R7 repair rounds R10 far-remediation) or re-parent it to a fresh round that re-derives each finding",
  "HG-KSEOS/scripts/hgk-lane-dispatch.py (current guard code) vs the record's 1.1-1.4 rows",
  "no round dir under HG-KSEOS/var/ executes its own rows; decision is owner's because the record itself does not name the executor"),
 ("hgk-lane-reliability-closure-20261016", 5, 16, "no",
  "R8 measured the round's own WorkSet in var/LANE-RELIABILITY-CLOSURE-20261016 (admission, CHANGESET_A apply receipt epoch 19->20, BC/V lane receipts, closure JSON)",
  "CONTINUE", "Close the record by ticker: rows 1-3 measurable DONE via var/LANE-RELIABILITY-CLOSURE-20261016/ROUND_CLOSURE.json; the 16 [ ] rows' M03/CONTROLLER/session-closure work must first be executed by a successor round",
  "var/LANE-RELIABILITY-CLOSURE-20261016/",
  "its own honest_residuals[] names F1-PLAN-route, merged-SOD, EXECUTE-lane-reliability as NOT repaired"),
 ("hgk-plan-plane-rebind-20261015", 3, 5, "no",
  "PGDMX record whose PLAN rebind was applied by an external act at 2026-10-16T12:36:30 (epoch 21), then epoch 22; only housekeeping/PGDMS rows remain",
  "OWNER_DECISION", "Owner decides whether to close it citing the external rebind act, or leave it as the standing PGDMC donor for the 2 residual rows (served-arm receipt, R4 canonical apply)",
  "config/lane-routing-registry.yaml routes[].PLAN + var/FAR-REMEDIATION-AND-CLOSURE-20261016/ROUND_CLOSURE.json PLAN_in_hermes measurement",
  "rows 1.3 'served-arm receipt' and 3.1 'R4 canonical apply' are closed by later rounds' artifacts, not by this record"),
 ("hgk-r10-session-closure-20261016", 25, 5, "no",
  "R10 session-closure record: 5 open rows are ALL gated on publication (5.2 push, 5.3 PR) or on the 5.1a VERIFY lane that fail-closed with ERR_LANE_REQUIRED_ARM_ABSENT",
  "CONTINUE", "Execute the remaining rows in order 5.2 push (publish_r10.py already prepared) then 5.3 PR then re-attempt 5.1a-5.1d VERIFY lane under the current epoch-22 registry",
  "_handover/CNV-PIPD-LS-SP-20261015-R10/publish_r10.py + SESSION_LEDGER_R10.json blockers[]",
  "not HISTORICAL: the verified-but-unpublished R10 packet is still the newest deliverable the external officer has not seen"),
 ("hgk-r8-eia-closure-skill-slim-20261016", 0, 22, "no",
  "all 22 rows were measured as PGDM6/T rows of a PROPOSAL ONLY record (each row self-describes Executive/Owner-bounded or BLOCKED-owner preconditions)",
  "OWNER_DECISION",
  "Skill Owner (or EIA remediation owner) must choose which of the 22 rows enter the next round's admission; no agent may self-authorise them (claim ceiling is explicitly future-bounded)",
  "_handover/CNV-PIPD-LS-SP-20261015-R8/EIA_*.md + the record's own header convention",
  "the R8 work that DID run lives in var/FAR-REMEDIATION-AND-CLOSURE-20261016 and in _handover/R8, but this record's own 22 rows were designed as a future bounded round"),
 ("hgk-r9-far-residual-closure-20261016", 20, 5, "no",
  "R9 executed 20 rows measurably in _handover/R9 (WS_A hunk apply, CANDIDATE_V2 overlay, checker UNVERIFIABLE adjudicated), leaving 5 residual rows pointing at owner-blocked items",
  "CLOSE_CANDIDATE", "Tick 1.1-4.4 citing _handover/CNV-PIPD-LS-SP-20261015-R9/ artifacts; carry the 5 [ ] owner-blocked rows (5.1/5.2 gates, EIA-R6-03 isolation) into the owner's decision queue rather than the record",
  "_handover/CNV-PIPD-LS-SP-20261015-R9/R9_LEDGER.json",
  "rows are executable-immediately instrumented state instruments"),
 ("hgk-r11-session-handover-20261016", 0, 18, "no",
  "the record is this session's own record (this WS worker runs inside it): the 2.1/2.3/3.3 rows describe exactly the WS inventory being produced, plus downstream integration rows",
  "CONTINUE", "Finish the round: the orchestrator merges ws1+ws2 outputs into RESUME_MANIFEST/OPEN_RECORDS_INVENTORY, runs the independent VERIFY lane on the mandate's arm, then rows 4.3/5.1-5.4",
  "this change record itself (rows 2.1, 3.3) + the R11/FAR/ws1 outputs being written now",
  "the record's 5.x publication rows reuse the standing publish_r11.py successor"),
 ("hgk-skill-convergence-20261014", 3, 13, "no",
  "SKCV record: rows 1.1-1.3 ticked as DONE-MEASURED by var/SKILL-CONVERGENCE-20261014 (baseline+qualification), the build rows 2.x-4.x were taken over by the R6/R7 rounds' slim-to-canonical path",
  "CLOSE_CANDIDATE", "Have the owner (or a successor record) close rows 1.4-4.3 citing their real landing points: gen2 candidate in var/SKILL-CONVERGENCE-20261014/candidates, apply path executed by R9's 2.2 overlay apply, legacy-alias work absorbed",
  "var/SKILL-CONVERGENCE-20261014/ + _handover/CHECKPOINT_SKILL-CONVERGENCE-20261014.md",
  "its own checkpoint names the record's statuses as paused at the qualified-candidate stage"),
 ("lane-health-repair-20261011", 30, 4, "no",
  "measured DONE by var/far-lane-health-repair-20261011 (admission, group passes D1-D4, checker lanes, freeze manifest 185 artifacts); the 4 [ ] rows are the deliberately-stopped iteration loop's residual (K1-K5, C5/C6, OQ*)",
  "CLOSE_CANDIDATE", "Owner-or-successor tick 1.1-5.6 (30 rows all have var/ evidence rows); move ONLY rows 6.1-6.4 into a successor record named K-class-loader-unterminated-carrier and leave them unticked there",
  "var/far-lane-health-repair-20261011/FREEZE_MANIFEST.json + tasks.md rows 2.1-5.6 evidence locators",
  "iteration was stopped by the standing monitoring order, not by loss of work"),
 ("lane-mandate-rebinding-and-d01-revocation", 11, 27, "no",
  "mixed record: 11 done rows are rebind/HG fixes with var/ evidence (far-w6-plan-sod-reconciliation, D-01 revocation record, exclusion rule), 27 open rows are the D01/DGA use-rule and docs arms that were still not run as of its own status table",
  "OWNER_DECISION", "Owner re-scopes: the rebinding rows' premise has already been superseded TWICE (epoch 18 rebind 2026-10-15, then epoch 21/22 rebinds 2026-10-16); keep only the D01-revocation-history rows as a closed historical record and spawn the standing exclusion rule as a fresh PGDTX row",
  "config/lane-routing-registry.yaml epoch + var/FAR-LANE-ROUTE-REBIND-20261015/epoch-18 apply receipt",
  "its tasks.md Appendix A applies-vs-staged table recorded the rebind APPLIED at epoch 17 - the registry is now at epoch 22, so most open rows reference a registry state that no longer exists"),
 ("lane-model-chain-rebind-20261015", 0, 13, "no",
  "its own live execution exists in var/FAR-LANE-ROUTE-REBIND-20261015 (epoch-18 rebind, mandates, E2E receipts, per-turn mandate consumer) but the record file was never ticked",
  "CLOSE_CANDIDATE", "Tick rows 1.1-4.2 citing var/FAR-LANE-ROUTE-REBIND-20261015/{REBIND_ROUND_CLOSURE,SESSION_CLOSURE}.json; leave row 4.2's 'candidate -> owner review' as the single owner row if the owner still owes an explicit review",
  "var/FAR-LANE-ROUTE-REBIND-20261015/",
  "the chain rebind this record describes has since been superseded twice (epochs 21, 22) - the rows describe work that WAS live at epoch 18"),
 ("hgk-round3-lane-rebind-20261016", 26, 1, "no",
  "2026-10-16 owner-order rebind (epoch 21->22): 26 of 27 rows executed and disclosed live (var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016, R1_R2_R3_APPLY_RECEIPT.json, ORACLE_R10_RECEIPT 7/7, publication branch/PR); only row 5.4 (record R11 admission-receipt-producer gap) intentionally left open",
  "CLOSE_CANDIDATE",
  "Tick rows except 5.4 citing var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016/; carry 5.4 (no admission-receipt producer in the product) into the owner's control-plane backlog as a NEW requirement rather than an open checkbox",
  "var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016/R1_R2_R3_APPLY_RECEIPT.json",
  "record created ~14:30 today, after this session's earlier snapshots excluded it"),
 ("lane-sod-enforcement", 0, 27, "no",
  "its task list predates the actual landing of the enforcement kit (registry/SoD guard/drift checker) which exists live in scripts + tests + config; the record was a pre-baseline spec draft and its rows describe currently-shipped mechanics",
  "HISTORICAL", "Archive: verify one line - 'the enforcement kit this record specifies exists in src/hg_kseos/lane_policy.py + scripts/hgk-lane-guard.py + tests/test_lane_policy.py' - then close as HISTORICAL without executing any of its 27 rows",
  "src/hg_kseos/lane_policy.py + scripts/hgk-lane-guard.py",
  "predates epoch-1 of the registry; every row's subject is already in force"),
 ("lane-supervisor-windowless-convergence", 12, 1, "no",
  "executed round with var evidence (windowless launcher, per-epoch cooldown, independent verifier); the 1 open row 3.3 is the recovery-budget/trigger-interval split that the round left deliberately unticked",
  "CONTINUE", "Either dispatch a tiny bounded turn implementing row 3.3 (recovery budget separate from trigger interval) or close the record with row 3.3 re-parented to a successor, citing var/far-lane-sod-011-router-window/",
  "var/far-lane-sod-011-router-window/ + row 3.3 itself",
  "tiny live gap; cheapest close of all 24 records"),
 ("lane-toolchain-identity-and-failure-classification", 18, 9, "no",
  "its 18 done rows have live receipts; the 9 open rows are T1.4/T3.4 (grep-based 'no find/command -v' audits), T4.4 (determinism), T6.x (docs), 7.x (candidate-only bookkeeping)",
  "CONTINUE", "Run the 3 cheap rows first (T1.4, T3.4 grep audits on scripts/hgk-lane-*.py) and close the record citing scripts/hgk-lane-toolchain.py; T4.4 determinism + T6.x docs can land in one follow-up turn",
  "scripts/hgk-lane-toolchain.py + tests/",
  "the toolchain identity itself has been superseded by toolchain-q hashes in later rounds"),
 ("lane-verify-dual-routing-and-plan-high", 5, 23, "no",
  "its 2.x/3.x/5.x/6.x/8.x rows reference a registry epoch-10 deployment that was long since overtaken (epoch 22 now); only rows 1.x admissions and 4.1-4.2 (reasoning overrides) were measurably done",
  "HISTORICAL", "Close as HISTORICAL: the dual-routing surface it specifies is already in force via later epochs (2.1-2.5 rows' questions were answered by FAR-LANE-ROUTE-REBIND-20261015); no row points to work that is still attributable",
  "config/lane-routing-registry.yaml history + _handover/CHECKPOINT_FAR-LANE-REPAIR-20261014.md",
  "predates the current convergence mission (R6..R10)"),
 ("lane-verify-routing-remediation", 0, 14, "no",
  "its mandate/rebind/integration rows target the verify-lane routing defects measured before the R6 rounds; the routing surface it addresses was fixed and re-fixed by rounds FAR-LANE-ROUTE-REBIND-20261015 and ROUND3-LANE-REBIND-AND-CLOSURE-20261016",
  "HISTORICAL", "Close as HISTORICAL unless the owner re-opens the verify-routing defect: every row's subject is covered by the newer rebind records (its non-verdict defect was closed by verification-artifact-contract row 7.2)",
  "src/hg_kseos/lane_route_resolver.py current state + var/far-verify-routing-remediation* absence",
  "no HG-KSEOS/var round dir carries this record's own name"),
 ("sod-independent-verify-enforcement", 3, 2, "no",
  "3 done rows are measured (candidate S1* authored, fixtures aligned, 0/6 hard-rules implemented measured); the 2 open rows are explicitly owner-gated canonical applies",
  "OWNER_DECISION", "Owner must authorise the canonical S1* apply (row 4) + subject_digest migration (row 5); nothing an agent can do changes the record otherwise",
  "worktrees/hgk-sod-s1star-20261009 + tasks.md rows 4-5",
  "validation fails (--strict) only because skip_specs is not set: basis is a candidate-only S1*, so it is not a product defect"),
 ("strict-declaration-20261011", 5, 17, "no",
  "admission (1.x) and route-check rows are measured done; the S1-S4 implementation rows 2.x/3.x/4.x/5.x were measured NOT run on the canonical tree in later rounds' probes (P24-P28 stay незарегистрированными)",
  "CONTINUE", "Re-derive the 4 implementation rows in one bounded EXECUTE turn (the resolver's strict typing lives in src/hg_kseos/lane_route_resolver.py); rows 4.x checker lanes already have the harness from far-lane-repair-20261011 to reuse",
  "var/far-strict-declaration-20261011/ + src/hg_kseos/lane_route_resolver.py",
  "its own round artifacts exist but its implementation rows were measured not-landed by the R6+ rounds"),
 ("verification-artifact-contract", 7, 26, "no",
  "group 7 rows (defect re-measured and repaired with verdict artifact contract) are DONE-MEASURED (lanes S8/S11 F11 receipts, 40+13 cases); the 26 open rows are the remaining F9/F10/F13(b)(c) implementation groups",
  "CONTINUE", "Pick F11's remaining groups one at a time: F13(b)(c) shard home isolation is the smallest first slice (4.1-4.4 rows), reusing checker-v2-r4fix fixtures; F9/F10 need a budget surface first",
  "var/w6* verify/shards/S11 + the record's own row 7.1-7.7 evidence",
  "the S8/S11 wins are recorded but never mirrored into the record checkbox state"),
]

# sanity: names in `records` must match scanned dirs
scanned = set(rows_scan)
named = [r[0] for r in records]
missing = scanned - set(named)
extra = set(named) - scanned
assert not missing, f"records missing vs scan: {missing}"
assert not extra, f"records named but not scanned: {extra}"
assert len(records) == len(scanned) == 25, len(records)

# build json of measurements
meas = {
 "schema": "CNV-PIPD-LS-SP-20261015-R11/FAR/ws1/RAW-MEASUREMENTS/1",
 "produced_utc_note": "measured 2026-10-16 14:27-14:5x +08:00 by the R11 ws1 read-only worker from live filesystem + CLI output only",
 "claim_ceiling": "LOCAL / candidate-only",
 "toolchain": {"openspec_cli_version": OPENSPEC_VERSION,
               "version_cmd": "cd C:/Projects/Agent_Workspace/HG-KSEOS/openspec && npx --no-install openspec --version",
               "version_raw": "1.8.0", "version_exit": "0",
               "note": "CLI AVAILABLE; every record validated with the real command, no NOT_MEASURED rows"},
 "commands_run": [
   {"cmd": "npx --no-install openspec --version", "cwd": "C:/Projects/Agent_Workspace/HG-KSEOS/openspec", "raw": "1.8.0", "exit": "0",
    "note": "toolchain availability gate"},
   {"cmd": "ls changes/ && date", "cwd": "C:/Projects/Agent_Workspace/HG-KSEOS/openspec", "raw": "24 records + archive listed; clock 2026-10-16 14:27:14 +08", "exit": "0"},
   {"cmd": "openspec validate <name> --strict  (x25, one per record)", "cwd": "C:/Projects/Agent_Workspace/HG-KSEOS/openspec",
    "raw": "see validate_raw.txt (each record's full output incl. the 23 SUCCESS texts and the 2 failing records' verbatim error blocks)", "exit": "mixed (23 exit 0, 2 exit 1)"},
   {"cmd": "grep -cE '^- \\[ |^- \\[[xX]\\]' */tasks.md", "cwd": ".../openspec/changes", "raw": "tasks row counts per record (below)", "exit": "0"},
   {"cmd": "find <record> -type f -printf mtime | sort -rn | head -1", "cwd": ".../openspec/changes", "raw": "newest mtime per record (below)", "exit": "0"},
   {"cmd": "spec.md existence walk + registry readback (lane_policy.load_registry) + live-evidence greps under var/ and _handover/ and skills/", "cwd": "HG-KSEOS", "raw": "values below", "exit": "0"},
 ],
 "registry_readback": {
   "epoch": 22, "PLAN": "opencode-go/glm-5.3-flash medium",
   "EXECUTE": "openai-codex/gpt-6-luna default (deepseek-v4.1-flash & nvidia arm block present)",
   "VERIFY_SECURITY": "opencode-go/deepseek-v4.1-flash default",
   "sod_pairs": ["EXECUTE/VERIFY distinct_required=False (SOD006-C3 OWNER_ORDERED_IN_FORCE)", "PLAN/VERIFY distinct_required=True (C2 SUPERSEDED)"],
   "check_drift_guard_probe": "measured ERR_LANE_SOD_VIOLATION without declaration, per round3 receipt ORACLE_R10_RECEIPT.json 7/7",
   "cmd": "cd C:/Projects/Agent_Workspace/HG-KSEOS && C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe -c 'from hg_kseos import lane_policy as L; r=L.load_registry(); L.registry_epoch(r)'",
   "raw": "epoch: 22 then per-lane routes dump (see transcript)",
   "exit": "0"
 },
 "live_evidence_map": LIVE,
 "records_measurements": {d: dict(rows_scan[d], **{
     "strict_validation": ("VALID exit=0" if validate.get(d, {}).get("exit") == "0" else "INVALID exit=1"),
     "validate_raw_excerpt": (validate.get(d, {}).get("raw") or [""])[0],
 }) for d in sorted(rows_scan)},
 "dispositions": [{"change": c, "disposition": disp, "one_action": a, "locator": loc, "note": n}
                  for (c, _dn, _o, _sm, _mt, disp, a, loc, n) in records],
}
# fit measured numbers into the disposition tuples at write time
res = []
for (c, _dn, _o, _sm, _mt, disp, a, loc, n) in records:
    m = rows_scan[c]
    res.append({"change": c, "tasks_done": m["done"], "tasks_open": m["open"], "spec_md": m["spec_md"],
                "newest_mtime": m["mtime"], "newest_mtime_file": m["mtime_file"],
                "strict_validation": ("PASS exit=0" if validate.get(c, {}).get("exit") == "0" else "FAIL exit=1"),
                "live_evidence": LIVE.get(c, "no"),
                "disposition": disp, "one_action": a, "locator": loc, "note": n})

json.dump(meas, open(os.path.join(WS1, "raw_measurements.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)

# TIV
cols = ["change", "tasks_done", "tasks_open", "spec_md", "newest_mtime", "strict_validation",
        "live_evidence", "disposition", "one_action", "locator", "note"]
with open(os.path.join(WS1, "open_records_inventory.tsv"), "w", encoding="utf-8") as f:
    f.write("\t".join(cols) + "\n")
    for r in res:
        vals = [str(r[c]).replace("\t", " ").replace("\n", " ") for c in cols]
        f.write("\t".join(vals) + "\n")

from collections import Counter
print("order-disposition counts:", dict(Counter(r["disposition"] for r in res)))
print("rows:", len(res))
print("spec_md count:", sum(1 for r in res if r["spec_md"]))
print("strict pass:", sum(1 for r in res if r["strict_validation"] == "PASS exit=0"))
print("open rows total:", sum(r["tasks_open"] for r in res))
print("done rows total:", sum(r["tasks_done"] for r in res))
