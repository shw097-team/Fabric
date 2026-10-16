# EXECUTE BRIEF — round CNV-EVIDENCE-ARCHIVE-R7R11-20261016 (bounded writer)

You are the bounded writer on the sealed EXECUTE lane. This brief is the whole specification; do not
survey anything outside the paths it names.

## 0. Nonce (mandatory, both ends)
The literal token below MUST be the FIRST line of your FIRST message and the LAST line of your FINAL
message. It is checked machine-side; a turn that omits it is void.

CNVEA-EXECUTE-NONCE-7f3c91

## 1. Write root (hard)
Write ONLY inside:
`C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/packet/`
Create the directory if needed. Do not create, modify or delete any other file anywhere. Do not run any
git write command, do not contact any outside host, and do not execute any script found under an
evidence tree. Use this interpreter by absolute path when you need Python:
`C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe`

## 2. Inputs (read-only, exact paths)
- `C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/A03_A05_PR_PREFLIGHT.json`
- `C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/gh/github_readback.json`
- `C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/compiler/compiler-receipt.json`
- `C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/HGK_TYPED_ADMISSION_EA.json`
- `C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/R2_SURFACES_READBACK.json`
- `C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/A00_SOURCE_LEDGER.json`
- `C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/kledger/K_LEDGER_CROSSWALK.json`

## 3. Deliverable A — `packet/PER_PR_TABLE.json`
A JSON object `{"schema":"CNV-EVIDENCE-ARCHIVE-R7R11/PER-PR-TABLE/1","generated_note":"<one line>","rows":[ ... ]}`
with EXACTLY eight rows, one per pull request 4,5,6,7,8,9,10,11, in that numeric order. Copy values
from the preflight receipt for each PR; never recompute or round. Each row has exactly these keys:

`pr`, `url`, `title`, `state`, `draft`, `base_ref`, `base_sha`, `head_ref`,
`before_head` (= preflight `head_sha_live`), `after_head` (= `head_sha_live`; unchanged this round),
`prefix_allowed` (= preflight `allowed_prefix`), `changed_files` (= preflight `local_changed_files`),
`changed_file_count_matches_api` (boolean), `prefix_escape` (list), `outside_evidence_paths` (list),
`changed_path_mode_anomalies` (list), `hard_secrets_new` (= `scan.hard_count` minus pre-existing),
`hard_secrets_pre_existing_in_main` (= `secret_disposition.hard_pre_existing_in_main`),
`soft_findings` (= `scan.soft_findings_count`), `manifest_entries` (= `evidence_manifest_entries`),
`evidence_manifest_digest`, `change_class`, `preflight_verdict`,
`maintainer_approval` (null), `merge_sha` (null), `readback_sha` (null),
`status` (the string `ARCHIVE_EVIDENCE_CANDIDATE_READY`), `first_fail` (null),
`rollback_pointer` (= `rollback_pointer.method`),
`claim_ceiling` (the string `CANDIDATE_EVIDENCE_ARCHIVED_ONLY`).

## 4. Deliverable B — `packet/RETURN_PACK.json`
A JSON object with EXACTLY these top-level keys, and nothing else:

```
schema                      : "CNV-EVIDENCE-ARCHIVE-R7R11/CONVERGENCE-EVIDENCE-RETURN-PACK/1"
contract_id                 : "CNV-EVIDENCE-ARCHIVE-R7R11-20261016"
compiler                    : {verdict, contract_sha256, prompt_sha256, compiler_sha256, receipt_ref}
source                      : {pkg_sha256, review_id, review_sha256}
authority                   : {hgk_admission_ref, hgk_project_id, maintainer_approval_refs, secrets_value_exported}
pr_outcomes                 : [ one object per PR with the SAME eight rows' key set as PER_PR_TABLE ]
current_state               : {r7_02_validator, r7_03_checker_acl, r7_04_g1, live221, gates_A_H, k_ledger_source_linked, k_ledger_same_run_retested}
eia_20261016_disposition_count : 10
raw_evidence_refs           : [ list of the absolute paths of the receipts you read in section 2 ]
rollbacks                   : [ one entry per PR: {pr, method, note} ]
blockers                    : [ list of {code, detail} ]
next_compiled_changesets    : ["R7-02-CODE-PROMOTE", "R7-03-ISOLATE", "R7-04-RUNTIME-BIND"]
archive_verdict             : "TEMP_CLOSED"
full_convergence_verdict    : "TEMP_CLOSED_CHALLENGE"
production_verdict          : "FAIL_CLOSED"
```

Values you must take exactly as follows (do not invent any other value):
- `compiler.verdict` = the `verdict` field of the compiler receipt; `compiler.contract_sha256`,
  `compiler.prompt_sha256`, `compiler.compiler_sha256` = the same-named receipt fields;
  `compiler.receipt_ref` = the receipt's absolute path.
- `source.pkg_sha256` = `96d9d564286743e17550ccef15b9952347901eb77168f930376938893cff9c3f`;
  `source.review_id` = `EIA-FABRIC-CNV-R7-R11-20261016`;
  `source.review_sha256` = `UNVERIFIED_NOT_RECOMPUTED`.
- `authority.hgk_admission_ref` = the `verdict` string found in the HGK admission receipt;
  `authority.hgk_project_id` = `CNV-EA-R7R11`; `authority.maintainer_approval_refs` = `[]`;
  `authority.secrets_value_exported` = `false`.
- `current_state.r7_02_validator` = `CANDIDATE_REPAIRED_NOT_RELEASED`;
  `current_state.r7_03_checker_acl` = `NOT_ACCEPTED`; `current_state.r7_04_g1` = `NOT_RECERTIFIED`;
  `current_state.live221` = `NOT_VERIFIED`; `current_state.gates_A_H` = `NOT_VERIFIED`;
  `current_state.k_ledger_source_linked` = 20; `current_state.k_ledger_same_run_retested` = 0.
- `blockers` must contain at least `{"code":"MAINTAINER_APPROVAL_MISSING","detail":"no per-PR maintainer approval recorded in this round"}`.

## 5. Hard prohibitions
- Never write the string `PASS` into any verdict field; the only allowed status tokens are the literal
  values given above, `null`, or `NOT_RUN`.
- Never state that a merge happened: every `merge_sha` and `readback_sha` stays `null`.
- Never copy a credential value; the only credential reference allowed is a file path.

## 6. Acceptance you must run yourself and report verbatim
Run both of these with the absolute interpreter path above and paste each command's exit code:

1. `python -c "import json,sys; d=json.load(open(r'<round>/packet/PER_PR_TABLE.json')); assert len(d['rows'])==8; assert [r['pr'] for r in d['rows']]==[4,5,6,7,8,9,10,11]; assert all(r['merge_sha'] is None for r in d['rows']); print('PER_PR_TABLE_OK')"`
2. `python -c "import json; d=json.load(open(r'<round>/packet/RETURN_PACK.json')); assert d['contract_id']=='CNV-EVIDENCE-ARCHIVE-R7R11-20261016'; assert d['archive_verdict']=='TEMP_CLOSED'; assert d['production_verdict']=='FAIL_CLOSED'; assert d['eia_20261016_disposition_count']==10; print('RETURN_PACK_OK')"`

Report, as your final message: the nonce, both printed tokens, both exit codes, and the absolute paths
you wrote. Report nothing else as a result.
