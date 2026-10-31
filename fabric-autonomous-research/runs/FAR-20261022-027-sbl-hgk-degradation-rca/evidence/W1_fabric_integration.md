# W1 — SBL / Fabric governance-contract integration audit

## Outcome

**SBL is not fully integrated into Fabric's governance contract.** Its inspected product entry points do not consume a named Fabric schema, registration/admission record, or Fabric evidence envelope and refuse a nonconforming one. Fabric itself is **CITED_ONLY** in the prompt-contract provenance: the cited object is `AGENTS.md`, explicitly `SUPPORT`, `critical: false`, `governs: false`, not a consumed schema or admission decision. Evidence: `SBL/tools/build_prompt_contract.py:126,145-147,379-380`; `SBL/contracts/SBL_C0_C9_CONTRACT-R9.json:30-35,193-199`; read-only probes in §7.

This does **not** establish that SBL is illicitly minting HGK WorkOrders or Permits. The product's local `BuildOrder` is a different DTO; the native adapter explicitly does not provide admission/signing. Actual SBL construction WorkOrders exist in HGK's spine, but that is not an SBL runtime WorkOrder → ExecutionBinding → Permit consumer. Evidence: `SBL/sbl_core/dto.py:106-111`; `HG-KSEOS/_sbl_harness_adapter/adapter.json:10-19,39-40`; SQL readback in §8.

## 1. Scope, identity and decision rule

Locators beginning `SBL/`, `Fabric/`, `HG-KSEOS/`, and `_sbl_release_011rc1/` resolve under `C:/Projects/Agent_Workspace/`. File-line citations are to the observed working-tree bytes, not an implied release branch. Observation stamp: `2026-10-22T02:18:05.442302+00:00` (UTC; command: Python `datetime.now(timezone.utc).isoformat()`).

Observed commands and outputs:

| Command | Output |
|---|---|
| `git -C C:/Projects/Agent_Workspace/SBL rev-parse HEAD` | `2dde2d84a2a6d95ccc6acb9356570bed68ab2f05` |
| `git -C C:/Projects/Agent_Workspace/SBL branch --show-current` | `evidence/r7-20261021-c7` |
| `git -C C:/Projects/Agent_Workspace/Fabric rev-parse HEAD` | `d62635626d5d2e54fe5bba22a500a17423c85719` |
| `git -C C:/Projects/Agent_Workspace/HG-KSEOS rev-parse HEAD` | `3dfaebc5c1d2ffe7d1782f3027bd25b54a557f2b` |
| `git -C C:/Projects/Agent_Workspace/SBL status --porcelain` | `?? contracts/SBL_C0_C9_CONTRACT-R9.json` and `?? contracts/compiled-r9/` |
| `git -C C:/Projects/Agent_Workspace/HG-KSEOS status --porcelain` | empty |

The R9 contract is untracked and was inspected as candidate evidence, not silently treated as committed source. The checkout differs from the release source cited by its own R9 record: `_sbl_release_011rc1/` rather than nonexistent `SBL/src`. Read-only comparison of the release adapter also found the explicit non-provision of native admission/signing (`SBL/_governance/round-20261021-r9/FAR-R9-RULING.md:85`; `_sbl_release_011rc1/sbl_harness/__init__.py:1-16,51-67`). This is not a qualification audit of every installed package or another branch.

Integration means a contract artefact is selected, read/validated, bound to a decision and evidence, with refusal on mismatch. `CONSUMED` means that seam is demonstrated; `CITED_ONLY` means a declaration/reference exists but not the mandatory consumer; `ABSENT` means no applicable named artefact/consumer was found in the inspected seam. These are integration verdicts, not acceptance grants. Fabric's own rule rejects policy presence as consumption (`Fabric/FABRIC/AGENTS.md:73-74,128-129`).

Authority boundaries: HGK is the sole governance/normative/WorkOrder/acceptance/release control plane; Fabric is the contract surface; Hermes is the governed runtime (`Fabric/FABRIC/AGENTS.md:17-29`). AGENTS is an operating projection, explicitly not itself a policy or gate (`Fabric/FABRIC/AGENTS.md:6-9,125`).

## 2. Verdict per integration axis

| Axis | Verdict | Decisive evidence and claim boundary |
|---|---|---|
| (a) Fabric schemas | **ABSENT** | No named Fabric schema is selected or validated by the checkout's runtime. Its schemas are local SBL DTO/schema identifiers (`SBL/sbl_core/dto.py:106-129`; `SBL/sbl_sp/bridge.py:43-74`), while the only Fabric source in the prompt contract is non-governing AGENTS support (`SBL/contracts/SBL_C0_C9_CONTRACT-R9.json:30-35,193-199`). Exact artefact scan returned exit 1/no matches (§6). General Fabric citation is **CITED_ONLY**, not schema consumption. |
| (b) Fabric install/registration target | **ABSENT** | No SBL target/registration appears in the non-run Fabric search (§6/Appendix). SBL itself records `NO_SBL_INSTALL_TARGET` (`SBL/_governance/round-20261021-r8/INSTALL_BOOTSTRAP_R8.json:116-118`; R9 ruling `:87`). Fabric registration requires subject/version/digest/owner/ceiling/permission/lifecycle/rollback fields and does not authorize by registration alone (`Fabric/FABRIC/control/PROFILE_STACK_REGISTRATION_POLICY.yaml:8-23`). No wheel installation into Fabric is required or proposed by this finding; a sanctioned applicability/registration disposition is the missing seam. |
| (c) Fabric evidence/packet contract | **ABSENT** | Local receipts/manifests are not bound to Fabric's evidence contract or collaboration envelope. Compare `SBL/tools/evidence_manifest.py:47-61,65-83` and `SBL/sbl_core/m05_verify.py:65-94,170-176` with `Fabric/FABRIC/assurance/EVIDENCE_CONTRACT.yaml:2-14` and `Fabric/FABRIC/contracts/FABRIC_COLLABORATION_ABI.schema.yaml:15-27`. The exact artefact scan returned no references (§6); local in-memory verdict construction needed no Fabric packet (§7). Similar rules are not contract consumption. |
| (d) HGK WorkOrder/Permit issuance | **CITED_ONLY** | For the **product's native issuance/consumption seam**, WorkOrder/ExecutionBinding/Permit are required by declaration but explicitly not provided by the adapter (`HG-KSEOS/_sbl_harness_adapter/adapter.json:10-19,39-40`; release harness `:51-67`), and the checkout declares no such grants (`SBL/README.md:111-116`). No HGK runtime/API references were found in its product packages (§6). **Counter-evidence:** genuine HGK construction WorkOrders do exist (§8); this is not an assertion that all HGK use is merely prose. WorkOrder engineering admission alone does not prove a product Permit/effect chain. No SBL-native minting implementation was observed. |

## 3. Concrete gaps, not a proposal for a second control plane

### F1 — hashed governance-document support is being asked to stand in for a contract consumer

`build()` hashes Fabric AGENTS and records it as a support source (`SBL/tools/build_prompt_contract.py:126,145-147`); the generated authority table says `governs: false` (`:379-380`). The candidate R9 contract preserves that shape (`SBL/contracts/SBL_C0_C9_CONTRACT-R9.json:193-199`). That proves provenance of a citation, not validation against a Fabric schema or a policy digest → consumer → decision → evidence trace. Fabric explicitly requires the latter (`Fabric/FABRIC/AGENTS.md:73-74`).

Minimum missing evidence: identify an applicable existing schema/ABI, bind its version/digest, show a real consumer decision plus evidence and an otherwise-valid nonconforming input being refused. Do not promote AGENTS into an authority source to fill the gap (`Fabric/FABRIC/AGENTS.md:6-9,125`).

### F2 — no Fabric registration/applicability seam, not “Fabric needs an SBL daemon”

The Fabric registration policy is real and lists required fields (`Fabric/FABRIC/control/PROFILE_STACK_REGISTRATION_POLICY.yaml:8-23`), but the complete non-run SBL search found only incident, exclusion, research-reference and raw-transcript mentions, not a registered SBL governed surface (Appendix). FAR's capability matrix names research providers and routes, not SBL install targets (`Fabric/FABRIC/fabric-autonomous-research/governance/FAR_CAPABILITY_MATRIX.yaml:7-48,50-93`). Its existence is not product registration.

SBL's surface ledger also refuses to overstate this: C-029 is `PARTIAL_LOCAL_SCOPED` with `raw_evidence: null`; C-030/C-031 remain OPEN and C-032 is NOT_ADMITTED (`SBL/evidence_ledger/surface_c001_c038_ledger.json:261-295`). Those are product-side candidate rows, not Fabric registration or host receipts. Obtain the contract owner's applicability decision before inventing a package target; Fabric forbids a second OS/scheduler/control plane (`Fabric/FABRIC/AGENTS.md:17-22,123-124`).

### F3 — local evidence discipline exists, but no Fabric packet admission was demonstrated

SBL's evidence manifest is explicitly `SBL-EVIDENCE-MANIFEST/1`, listing path/bytes/hash (`SBL/tools/evidence_manifest.py:47-61`), and its evidence DTO contains gate, command, exit, stdout digest and denominator (`SBL/sbl_core/dto.py:114-120`). Fabric's collaboration envelope requires additional identity/consumer/subject/authority/stage/permission/evidence/status/reason/rollback bindings (`Fabric/FABRIC/contracts/FABRIC_COLLABORATION_ABI.schema.yaml:15-27`). Fabric's candidate manifest separately requires subject/package/source/producer/lifecycle/rollback fields (`Fabric/FABRIC/contracts/CANDIDATE_MANIFEST.schema.yaml:4-12`); a change package requires `evidence_contract_ref` (`Fabric/FABRIC/contracts/FABRIC_CHANGE_PACKAGE.schema.yaml:16-22`). No consumer mapping or refusal against these artefacts appeared in the exact scans (§6).

This does not prove every local evidence record is bad. It proves that SBL's local checks and a FAR report stored in Fabric are insufficient to claim the Fabric packet contract was consumed. Missing evidence is a typed, subject-bound packet and a real rejection from its admitted consumer, not another prose assertion.

### F4 — HGK construction admission is real; native product integration remains deferred

The core creates local orders from HEAD and a writeset (`SBL/sbl_core/m04_bridge.py:87-99`; DTO `:106-111`); it does not thereby issue an HGK WorkOrder or Permit. The release adapter expressly prohibits minting and leaves its ceiling HOST_PENDING until a real WorkOrder → ExecutionBinding → Permit trace exists (`_sbl_release_011rc1/sbl_harness/__init__.py:3-13,35,58-67`). Its installed descriptor says native effect NOT_GRANTED (`HG-KSEOS/_sbl_harness_adapter/adapter.json:39-40`).

The native API is HGK's `SharedSpine.create_workorder`, which rejects missing critical fields and a non-DRAFT taskspec before admitting/inserting the row (`HG-KSEOS/src/hg_kseos/spine.py:305-330`). This audit invoked **no issuance or mutation API**. The read-only DB query shows that SBL construction has real HGK workorders, including FAILED and ROLLED_BACK history; it does not show a Permit verified by SBL at runtime (§8). Required next evidence is that native subject/scope-bound effect trace through HGK, not an SBL-issued substitute.

## 4. What SBL does correctly

- **States its effect ceiling:** `STANDALONE_ONLY`, no WorkOrder/ECP/Permit/ExecutionBinding grant, shadow NO_EFFECT, connected mode ungranted (`SBL/README.md:111-116`). The release adapter says `permit_signing` and `workorder_admission` are not provided, rather than pretending root-readiness is authority (`_sbl_release_011rc1/sbl_harness/__init__.py:51-67`; HGK adapter `:10-19`).
- **Actually refuses several local false-green paths:** same maker/checker, SUMMARY_ONLY evidence, a raised production ceiling and provider-off load all refused in §7; the implemented checks are in `SBL/sbl_core/m05_verify.py:42-54,116-129` and `SBL/sbl_sp/bridge.py:58-64`. These are local invariants, not authenticated native-principal proof.
- **Keeps shadow inert and missing-ACK connected mode closed:** §7 reproduced both outcomes; code `SBL/sbl_core/modes.py:106-130`. ACK checks include a configured issuer allowlist and HMAC, not merely four nonempty strings (`:46-63`). This audit did not qualify that HMAC as an HGK Permit protocol.
- **Has bounded local write controls:** lexical and real-path writeset checks and stale-HEAD rejection (`SBL/sbl_core/m04_bridge.py:108-172`). No apply/write operation was run in this read-only audit.
- **Does not pretend an inventory is a native receipt:** its ledger labels partial/open/not-admitted surfaces and keeps raw evidence null (`SBL/evidence_ledger/surface_c001_c038_ledger.json:261-295`); actual HGK history retains non-PASS states (§8).

## 5. Filesystem/layout corrections

Read-only Python existence/listing probes returned:

```text
Fabric/FABRIC/governance: absent
Fabric/FABRIC/schemas: absent
Fabric/schemas: directory present, no files under rglob('*')
Fabric/fabric-autonomous-research/governance: absent
Fabric/FABRIC/fabric-autonomous-research/governance: present
```

Therefore this audit inspected the existing `Fabric/FABRIC/control/`, `contracts/`, `assurance/`, `profiles/`, `fabric/`, FAR governance and registry candidates, rather than treating the brief's absent folder names as absent governance overall. Actual schema files are under `Fabric/FABRIC/contracts/`, including the collaboration/change/candidate/authority/promotion/rollback contracts (command: Python enumeration of `FABRIC/contracts`; output: six `*.schema.yaml` paths). The read operative projection is `Fabric/FABRIC/AGENTS.md`, not nonexistent `Fabric/AGENTS.md` (Python existence probe and full file read).

## 6. Search receipts (negative claims are scoped)

All `rg` commands below ran via `subprocess.run`, with cwd set to the root named below, stdout/stderr captured, and no source execution. Exit 1 means no matches, not a successful integration. The whole-Fabric scan used hidden files but excluded `.git` and both research-run locations, so a run report cannot become a product target merely by being present.

### SBL exact Fabric contract / packet references

```text
cwd: C:/Projects/Agent_Workspace/SBL
rg -n -i 'FABRIC-EVIDENCE|FABRIC-COLLABORATION|FABRIC-CANDIDATE|FABRIC-REGISTRATION|FABRIC_CHANGE_PACKAGE|EVIDENCE_CONTRACT.yaml|FAE|packet' sbl_core sbl_sp sbl_cli contracts tools evidence_ledger openspec README.md
exit: 1
stdout: empty
stderr: empty
```

### SBL native issuance/consumer references

```text
cwd: C:/Projects/Agent_Workspace/SBL
rg -n -i 'hg_kseos|SharedSpine|create_workorder|issue_permit|ExecutionBinding' sbl_core sbl_sp sbl_cli
exit: 1
stdout: empty
stderr: empty
```

These scans alone do not prove a universal absence: they are corroborated by the full core/bridge/mode/evidence DTO reads, runtime probes (§7), and explicit adapter non-provision. Broad Fabric/WorkOrder/Permit/schema scans additionally located the document citations and local ACK/schema names (`SBL/tools/build_prompt_contract.py:29,126,145-147,379-382`; `SBL/sbl_core/modes.py:22-38`; `SBL/sbl_core/dto.py:106-120`).

### Complete non-run Fabric token search

```text
cwd: C:/Projects/Agent_Workspace/Fabric
rg --json -i --hidden -g '!.git/**' -g '!fabric-autonomous-research/runs/**' -g '!FABRIC/fabric-autonomous-research/runs/**' SBL .
exit: 0
stderr: empty
```

Python parsed rg JSON `match` events and grouped by file/line: **177 matching physical lines in 42 files**. A token-sensitive filter `(?<![A-Za-z0-9])sbl(?![A-Za-z0-9])`, including `SBL_` field names, leaves **115** lines; a strict `rg -w` scan leaves **111**. The remaining substring hits are embedded image/integrity encodings and ResBlock/CausalResBlock names, explicitly listed below rather than counted as integration. Every raw-hit location is enumerated in Appendix A; separate mirrored paths are retained, not silently deduplicated away.

## 7. Real, read-only behavioural probes

Command: `python -B -c <the following program>`, cwd `C:/Users/user`. It inserts the audited checkout ahead of installed packages, prints the loaded module, disables bytecode, performs only in-memory operations plus git readback, never calls bridge.apply, and never creates a native workorder. Its evidence record is an explicitly labelled **fixture**, not a claimed executed gate or external receipt.

```python
import sys,json,os
sys.dont_write_bytecode=True
sys.path.insert(0,'C:/Projects/Agent_Workspace/SBL')
from sbl_core.core import SharedCore
from sbl_core.modes import ModeGate
from sbl_core.errors import SBLError
from sbl_core.m04_bridge import GovernedBuildBridge,bind_repo_context
from sbl_core.dto import WriteSet
from sbl_core.m05_verify import EvidenceVerification
from sbl_sp.bridge import SkillBridge
from unittest.mock import patch
out={}
out['subject_module']=sys.modules['sbl_core.core'].__file__
out['doctor_without_fabric_contract_input']=SharedCore('C:/Projects/Agent_Workspace/SBL').doctor()
out['local_buildorder_without_hgk_workorder']=GovernedBuildBridge().prepare(bind_repo_context('C:/Projects/Agent_Workspace/SBL'),WriteSet(('audit-fixture',))).to_dict()
out['shadow_no_effect']=ModeGate('PREW3_SHADOW').decide('local.write').to_dict()
try: ModeGate('SWOF_CONNECTED').decide('net.call')
except SBLError as e: out['missing_ack_refusal']=str(e)
ev=EvidenceVerification()
ev.record('FIXTURE','NOT AN EXECUTED GATE: in-memory audit fixture',0,'fixture',1)
try: ev.verdict('FIXTURE','maker','maker','PASS','LOCAL','LOCAL')
except SBLError as e: out['self_check_refusal']=str(e)
try: ev.verdict('FIXTURE','maker','checker','SUMMARY_ONLY','LOCAL','LOCAL')
except SBLError as e: out['summary_proxy_refusal']=str(e)
try: EvidenceVerification('PRODUCTION')
except SBLError as e: out['production_ceiling_refusal']=str(e)
out['local_fixture_verdict_without_fabric_packet']=ev.verdict('FIXTURE','maker','checker','PASS','LOCAL','LOCAL').to_dict()
try: SkillBridge('C:/Projects/Agent_Workspace/SBL/skills/sbl_todo/skill.json').effective_load({'provider_on':False})
except SBLError as e: out['provider_off_refusal']=str(e)
print(json.dumps(out,indent=2))
```

Observed exit `0`, stderr empty, stdout:

```json
{
  "subject_module": "C:\\Projects/Agent_Workspace/SBL\\sbl_core\\core.py",
  "doctor_without_fabric_contract_input": {
    "schema": "SBL-CORE-DOCTOR/1",
    "modules": [
      "SBLM01",
      "SBLM02",
      "SBLM03",
      "SBLM04",
      "SBLM05",
      "SBLM06"
    ],
    "ok": true,
    "root": "C:\\Projects\\Agent_Workspace\\SBL"
  },
  "local_buildorder_without_hgk_workorder": {
    "order_id": "O-d9e833ec91f9",
    "root": "C:\\Projects\\Agent_Workspace\\SBL",
    "head": "2dde2d84a2a6d95ccc6acb9356570bed68ab2f05",
    "writeset": {
      "paths": [
        "audit-fixture"
      ]
    }
  },
  "shadow_no_effect": {
    "mode": "PREW3_SHADOW",
    "effect": "local.write",
    "allowed": false,
    "no_effect": true,
    "reason": "SHADOW_READ_ONLY_NO_EFFECT"
  },
  "missing_ack_refusal": "SBL_E_REQUIRES_NATIVE_ACK: SWOF_CONNECTED requires a verifiable native acknowledgement",
  "self_check_refusal": "SBL_E_SELF_CHECK_FORBIDDEN: a maker may not verify its own work",
  "summary_proxy_refusal": "SBL_E_BAD_STATE: status 'SUMMARY_ONLY' is a proxy status and cannot back a verdict",
  "production_ceiling_refusal": "SBL_E_CLAIM_CEILING_EXCEEDED: ceiling PRODUCTION exceeds the build ceiling LOCAL",
  "local_fixture_verdict_without_fabric_packet": {
    "gate_id": "FIXTURE",
    "maker": "maker",
    "checker": "checker",
    "status": "PASS",
    "claim_level": "LOCAL"
  },
  "provider_off_refusal": "SBL_E_PROVIDER_OFF: skill may not load while the host provider is off"
}
```

Interpretation: local doctor, local BuildOrder preparation and a LOCAL fixture verdict succeed without any Fabric contract argument; their success does not qualify Fabric compliance. Conversely the listed refusals are real local checks. These probes do not test actual host mutation, networking, credential trust, native Permit issuance or independent acceptance.

## 8. HGK spine readback: genuine construction admission, not native effect

Command implementation: Python `sqlite3.connect(Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/shared-spine/hg-kseos.db').as_uri() + '?mode=ro', uri=True)`; `PRAGMA query_only=ON`; inspected table schemas before selecting named columns. No SharedSpine constructor, migration, reducer or writer was invoked.

```sql
SELECT w.workorder_id,w.taskspec_id,w.writer,w.worktree,w.base_head,w.state,
       t.requirement_id,t.state
FROM workorders w JOIN taskspecs t ON w.taskspec_id=t.taskspec_id
WHERE lower(t.requirement_id) LIKE '%sbl%'
ORDER BY w.rowid;
```

Observed rows (column order exactly as query):

```json
[
 [
  "WO-TS-PIPDLS-01",
  "TS-PIPDLS-01",
  "codex",
  "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\worktrees\\ts-pipdls-01",
  "903e47cddeceb40cb8f5f5793105533b3988a463",
  "CREATED",
  "REQ-HGK-PRJ-SBL-PIPDLS-PLAN",
  "ADMITTED"
 ],
 [
  "WO-TS-PIPDLS-02",
  "TS-PIPDLS-02",
  "codex",
  "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\worktrees\\ts-pipdls-02",
  "903e47cddeceb40cb8f5f5793105533b3988a463",
  "CREATED",
  "REQ-HGK-PRJ-SBL-PIPDLS-PLAN",
  "ADMITTED"
 ],
 [
  "WO-TS-PIPDLS-03",
  "TS-PIPDLS-03",
  "codex",
  "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\worktrees\\ts-pipdls-03",
  "903e47cddeceb40cb8f5f5793105533b3988a463",
  "CREATED",
  "REQ-HGK-PRJ-SBL-PIPDLS-PLAN",
  "ADMITTED"
 ],
 [
  "WO-TS-PIPDLS-04",
  "TS-PIPDLS-04",
  "codex",
  "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\worktrees\\ts-pipdls-04",
  "903e47cddeceb40cb8f5f5793105533b3988a463",
  "CREATED",
  "REQ-HGK-PRJ-SBL-PIPDLS-PLAN",
  "ADMITTED"
 ],
 [
  "WO-TS-req-hgk-prj-sbl-pipdls-r7-farclo",
  "TS-req-hgk-prj-sbl-pipdls-r7-farclo",
  "codex",
  "C:\\Projects\\Agent_Workspace\\SBL\\_governance\\round-20261021-r7",
  "3d06f3da83488219a3dcdf608c937b8c5285810c",
  "ROLLED_BACK",
  "REQ-HGK-PRJ-SBL-PIPDLS-R7-FARCLO",
  "ADMITTED"
 ],
 [
  "WO-TS-req-hgk-prj-sbl-pipdls-r7-farclo-2",
  "TS-req-hgk-prj-sbl-pipdls-r7-farclo-2",
  "codex",
  "C:\\Projects\\Agent_Workspace\\SBL\\_governance\\round-20261021-r7",
  "bedc11957d4fc2474b249b69d200829272c118ef",
  "FAILED",
  "REQ-HGK-PRJ-SBL-PIPDLS-R7-FARCLO-2",
  "ADMITTED"
 ],
 [
  "WO-TS-req-hgk-prj-sbl-pipdls-r8-lanerebind",
  "TS-req-hgk-prj-sbl-pipdls-r8-lanerebind",
  "codex",
  "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\worktrees\\ts-req-hgk-prj-sbl-pipdls-r8-lanerebind",
  "fa1ac06305e4f9ee45400049193482b5c7964441",
  "CREATED",
  "REQ-HGK-PRJ-SBL-PIPDLS-R8-LANEREBIND",
  "ADMITTED"
 ],
 [
  "WO-req-hgk-prj-sbl-pipdls-r9-ctrlpkg",
  "TS-req-hgk-prj-sbl-pipdls-r9-ctrlpkg",
  "codex",
  "C:\\Projects\\Agent_Workspace\\SBL\\_governance\\round-20261021-r9",
  "fa1ac06305e4f9ee45400049193482b5c7964441",
  "FAILED",
  "REQ-HGK-PRJ-SBL-PIPDLS-R9-CTRLPKG",
  "ADMITTED"
 ],
 [
  "WO-req-hgk-prj-sbl-pipdls-r10-handover",
  "TS-req-hgk-prj-sbl-pipdls-r10-handover",
  "codex",
  "C:\\Projects\\Agent_Workspace\\SBL",
  "b22706e",
  "FAILED",
  "REQ-HGK-PRJ-SBL-PIPDLS-R10-HANDOVER",
  "ADMITTED"
 ],
 [
  "WO-TS-REQ-HGK-PRJ-SBL-HGK-RCA-20261022-EXEC",
  "TS-req-hgk-prj-sbl-hgk-rca-20261022",
  "codex-lane:opencode-go/minimax-m3.1-flash-free@EXECUTE-rank1",
  "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261022-027-sbl-hgk-degradation-rca",
  "d62635626d5d2e54fe5bba22a500a17423c85719",
  "CREATED",
  "REQ-HGK-PRJ-SBL-HGK-RCA-20261022",
  "ADMITTED"
 ]
]
```

This establishes actual stored HGK admission/history, including the current RCA's WorkOrder. It does not prove how every historical writer called the API, authenticate a product effect, issue a Permit, or change a FAILED WorkOrder into acceptance. HGK's API contract resides in `HG-KSEOS/src/hg_kseos/spine.py:305-330`; the product adapter still disclaims native admission/signing (`HG-KSEOS/_sbl_harness_adapter/adapter.json:10-19`).

## 9. What prior FAR runs claim (not counted as integration targets)

- FAR-023 claims construction admission initially returned an id without a WorkOrder and was worked around through HGK's public API; it records an independent INCONCLUSIVE result mapped to FAIL, not acceptance (`Fabric/fabric-autonomous-research/runs/FAR-20261021-023-sbl-r7-residual-closure/FINDINGS.tsv:5,19`; `VERDICT.json:30`). Its release/merge claims (`VERDICT.json:29`) were **not** revalidated against remote GitHub in this local read-only audit.
- FAR-025 explicitly claims three installation achievements but no native integration, no SBL Fabric target and no self-made target (`Fabric/fabric-autonomous-research/runs/FAR-20261021-025-sbl-r9-ctrlpkg/FINDINGS.tsv:13,15`; `VERDICT.json:8,39`). It does not contain a Fabric registration admission or prove a mandatory Fabric consumer by reporting that absence.
- FAR-026 repeats no native integration and no Fabric target (`Fabric/fabric-autonomous-research/runs/FAR-20261021-026-sbl-r10-handover/FINDINGS.tsv:9-10`), and records the handed-over SBL source identity and failed acceptance (`VERDICT.json:24,39-48`). These are useful prior claims, not executable product integration.
- The R8 install receipt describes Fabric as “the autonomous-research harness” (`SBL/_governance/round-20261021-r8/INSTALL_BOOTSTRAP_R8.json:116-118`). That is too narrow if read as Fabric's full identity: the operative projection defines Fabric as governance/assurance/interop/knowledge contract surface (`Fabric/FABRIC/AGENTS.md:17-22`). This audit does not adopt that wording as a waiver of contract consumption.

## 10. Boundary and completion

Authored write scope: this findings file only. No repository source, policy, registry, contract, acceptance record, DB row or installed product was modified; no board/admission/release/installation/test runner was launched. Repeated git status before the output write matched the initial SBL/Fabric statuses and HGK remained clean (commands in §1). Tool infrastructure can retain its own stdout logs; no additional audit artefact was authored. The output file was absent before creation (Python `Path.exists()` returned false), and its parent existed.

No global HGK regression-origin claim is made. This is an integration-seam finding on the observed checkout, with explicit release-adapter counter-evidence, not a reconstruction of which historical change caused degradation. It is not an independent acceptance/release verdict. Remaining work belongs to the applicable Fabric contract/registration owner and HGK native issuer; none was manufactured to make this audit green.

## Appendix A — every non-run Fabric SBL substring hit

Rows group every matching physical line by file; each `path:line` below is an independent search locator. Grouping avoids reproducing giant raw transcript or base64 lines. All paths in this appendix are relative to `C:/Projects/Agent_Workspace/Fabric/`.

| File | Matching line numbers | Classification / why not an SBL integration target |
|---|---|---|
| `FABRIC/fabric-autonomous-research/methods/aris-vendor/docs/blogs/continuous_dlm_2026h1_survey.html` | `448`, `650`, `995`, `1001`, `1906`, `2502`, `2510`, `2532`, `2584`, `2624` | Incidental embedded image encoding; not the SBL product |
| `FABRIC/fabric-autonomous-research/methods/aris-vendor/docs/tutorials/image_generation_systems_tutorial.html` | `471`, `819`, `992` | Incidental ResBlock/CausalResBlock name; not the SBL product |
| `FABRIC/fabric-autonomous-research/methods/aris-vendor/docs/tutorials/image_generation_systems_tutorial.md` | `87`, `603`, `940` | Incidental ResBlock/CausalResBlock name; not the SBL product |
| `FABRIC/fabric-autonomous-research/methods/aris-vendor/docs/tutorials/image_generation_systems_tutorial_en.html` | `471`, `819`, `992` | Incidental ResBlock/CausalResBlock name; not the SBL product |
| `FABRIC/fabric-autonomous-research/methods/aris-vendor/docs/tutorials/image_generation_systems_tutorial_en.md` | `87`, `603`, `940` | Incidental ResBlock/CausalResBlock name; not the SBL product |
| `FABRIC/fabric-autonomous-research/methods/aris-vendor/docs/tutorials/video_generation_tutorial.html` | `507`, `531` | Incidental ResBlock/CausalResBlock name; not the SBL product |
| `FABRIC/fabric-autonomous-research/methods/aris-vendor/docs/tutorials/video_generation_tutorial.md` | `142`, `166` | Incidental ResBlock/CausalResBlock name; not the SBL product |
| `FABRIC/fabric-autonomous-research/methods/aris-vendor/docs/tutorials/video_generation_tutorial_en.html` | `507`, `531` | Incidental ResBlock/CausalResBlock name; not the SBL product |
| `FABRIC/fabric-autonomous-research/methods/aris-vendor/docs/tutorials/video_generation_tutorial_en.md` | `142`, `166` | Incidental ResBlock/CausalResBlock name; not the SBL product |
| `INTEGRATION/KNOWN-FINDINGS.md` | `32` | Shared-branch/publication incident history; not product registration |
| `evidence/FAR-LANE-REMEDIATION-20261021/PUBLISH-BRANCH-INCIDENT.md` | `33`, `34`, `37`, `43`, `47`, `48`, `53`, `68` | Shared-branch/publication incident history; not product registration |
| `evidence/FAR-MINIMAX-MANDATE-20261021/AO_FINAL2_PROMPT.md` | `106`, `107` | Prior-round SBL exclusion, concurrency or research bookkeeping; not an SBL installation/admission target |
| `evidence/FAR-MINIMAX-MANDATE-20261021/AO_FINAL_PROMPT.md` | `62`, `63` | Prior-round SBL exclusion, concurrency or research bookkeeping; not an SBL installation/admission target |
| `evidence/FAR-MINIMAX-MANDATE-20261021/CHECKPOINT.md` | `88`, `220`, `221` | Prior-round SBL exclusion, concurrency or research bookkeeping; not an SBL installation/admission target |
| `evidence/FAR-MINIMAX-MANDATE-20261021/CONCURRENT-OWNER-ORDER-CONFLICT.md` | `71` | Prior-round SBL exclusion, concurrency or research bookkeeping; not an SBL installation/admission target |
| `evidence/FAR-MINIMAX-MANDATE-20261021/FAR-RULING-REPORT.md` | `11`, `74`, `76`, `80`, `85`, `208`, `487` | Prior-round SBL exclusion, concurrency or research bookkeeping; not an SBL installation/admission target |
| `evidence/FAR-MINIMAX-MANDATE-20261021/PACKET_MANIFEST.json` | `283` | Prior evidence bundle lists parallel-session paths / exclusion note; no SBL governed-surface registration |
| `evidence/FAR-MINIMAX-MANDATE-20261021/PUBLISH-BRANCH-INCIDENT.md` | `33`, `34`, `37`, `43`, `47`, `48`, `53`, `68` | Shared-branch/publication incident history; not product registration |
| `evidence/FAR-MINIMAX-MANDATE-20261021/README.md` | `102`, `103`, `107`, `153` | Prior-round SBL exclusion, concurrency or research bookkeeping; not an SBL installation/admission target |
| `evidence/FAR-MINIMAX-MANDATE-20261021/SBL-EXCLUSION-NOTE.md` | `1`, `6`, `10`, `14`, `30`, `32`, `33`, `41`, `48`, `51` | Prior-round SBL exclusion, concurrency or research bookkeeping; not an SBL installation/admission target |
| `evidence/FAR-MINIMAX-MANDATE-20261021/ao_evidence_bundle.json` | `183`, `184`, `187`, `188`, `420`, `421`, `422`, `423`, `424`, `425`, `426`, `427`, `428`, `429`, `430`, `431`, `432`, `433`, `434`, `435`, `436`, `437`, `438`, `439`, `440`, `441`, `442`, `443`, `444`, `445`, `446`, `447`, `448`, `449`, `450`, `451`, `452`, `453`, `454`, `457` | Prior evidence bundle lists parallel-session paths / exclusion note; no SBL governed-surface registration |
| `evidence/FAR-MINIMAX-MANDATE-20261021/build_var_disposition_index.py` | `39` | Prior-round board/exclusion/disposition bookkeeping; not a product contract consumer |
| `evidence/FAR-MINIMAX-MANDATE-20261021/create_kanban_board.py` | `34` | Prior-round board/exclusion/disposition bookkeeping; not a product contract consumer |
| `evidence/FAR-MINIMAX-MANDATE-20261021/openspec-change/proposal.md` | `65`, `74` | Prior-round SBL exclusion, concurrency or research bookkeeping; not an SBL installation/admission target |
| `evidence/FAR-MINIMAX-MANDATE-20261021/openspec-change/tasks.md` | `64`, `66`, `68`, `117` | Prior-round SBL exclusion, concurrency or research bookkeeping; not an SBL installation/admission target |
| `evidence/FAR-MINIMAX-MANDATE-20261021/openspec-proposal.md` | `65`, `74` | Prior-round SBL exclusion, concurrency or research bookkeeping; not an SBL installation/admission target |
| `evidence/FAR-MINIMAX-MANDATE-20261021/openspec-tasks.md` | `64`, `66`, `68` | Prior-round SBL exclusion, concurrency or research bookkeeping; not an SBL installation/admission target |
| `evidence/FAR-MINIMAX-MANDATE-20261021/probes/attempt-21612-1792566884-1-stdout.txt` | `6`, `20`, `81` | Raw checker transcript quoting prompts, packet listings and prior-round evidence; not registration |
| `evidence/FAR-MINIMAX-MANDATE-20261021/probes/attempt-24364-1792567563-1-stdout.txt` | `6`, `33`, `70`, `133` | Raw checker transcript quoting prompts, packet listings and prior-round evidence; not registration |
| `evidence/FAR-MINIMAX-MANDATE-20261021/research/KNOWLEDGE-BASE-CROSSCHECK.md` | `62`, `67`, `70`, `146`, `154`, `165` | SBL source-corpus quotation / donor terminology; research reference, not contract admission |
| `evidence/FAR-MINIMAX-MANDATE-20261021/scripts/build_var_disposition_index.py` | `39` | Prior-round board/exclusion/disposition bookkeeping; not a product contract consumer |
| `evidence/FAR-MINIMAX-MANDATE-20261021/scripts/create_kanban_board.py` | `34` | Prior-round board/exclusion/disposition bookkeeping; not a product contract consumer |
| `fabric-autonomous-research/methods/aris-vendor/docs/blogs/continuous_dlm_2026h1_survey.html` | `448`, `650`, `995`, `1001`, `1906`, `2502`, `2510`, `2532`, `2584`, `2624` | Incidental embedded image encoding; not the SBL product |
| `fabric-autonomous-research/methods/aris-vendor/docs/tutorials/image_generation_systems_tutorial.html` | `471`, `819`, `992` | Incidental ResBlock/CausalResBlock name; not the SBL product |
| `fabric-autonomous-research/methods/aris-vendor/docs/tutorials/image_generation_systems_tutorial.md` | `87`, `603`, `940` | Incidental ResBlock/CausalResBlock name; not the SBL product |
| `fabric-autonomous-research/methods/aris-vendor/docs/tutorials/image_generation_systems_tutorial_en.html` | `471`, `819`, `992` | Incidental ResBlock/CausalResBlock name; not the SBL product |
| `fabric-autonomous-research/methods/aris-vendor/docs/tutorials/image_generation_systems_tutorial_en.md` | `87`, `603`, `940` | Incidental ResBlock/CausalResBlock name; not the SBL product |
| `fabric-autonomous-research/methods/aris-vendor/docs/tutorials/video_generation_tutorial.html` | `507`, `531` | Incidental ResBlock/CausalResBlock name; not the SBL product |
| `fabric-autonomous-research/methods/aris-vendor/docs/tutorials/video_generation_tutorial.md` | `142`, `166` | Incidental ResBlock/CausalResBlock name; not the SBL product |
| `fabric-autonomous-research/methods/aris-vendor/docs/tutorials/video_generation_tutorial_en.html` | `507`, `531` | Incidental ResBlock/CausalResBlock name; not the SBL product |
| `fabric-autonomous-research/methods/aris-vendor/docs/tutorials/video_generation_tutorial_en.md` | `142`, `166` | Incidental ResBlock/CausalResBlock name; not the SBL product |
| `stage/RP002-STAGE-HGK/CF1/vendor/contextforge/package-lock.json` | `2350`, `9556` | Incidental dependency integrity encoding; not the SBL product |

Machine-derived reconciliation: 177 appendix locations = 177 parsed rg match-lines; 42 file groups. No excluded FAR run was included in those totals.
