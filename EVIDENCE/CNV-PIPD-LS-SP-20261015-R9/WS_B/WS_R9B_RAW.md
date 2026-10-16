# WS-R9-B RECEIPT — guarded apply of the repaired `hgk-governed-execution` slim candidate

Nonce: `R9B-WSRITER-NONCE-9a4e2b`
Round `CNV-PIPD-LS-SP-20261015` / ChangeSet `R9-0` · HGK project `CNV-R9-FARCLOSURE` (WO-TS-FARCLOSURE-03).
Claim ceiling: **LOCAL / candidate-only** — a green harness run after the apply is a machine gate, not an acceptance and not a Gate PASS.

## 0. Result

- Pre-image manifest count: **127** paths.
- Apply set: **10 replaced, 4 added, 21 retained_untouched** (35 target rows).
- Post-apply harness (C1-C6): **PASS**.
- Rollback drill (on a COPY): **OK** — 31 restored byte-exact, 4 added files deleted, tree identical to pre-image: True.
- Loader row: `│ hgk-governed-execution │ software-development │ local   │ local   │ enabled │`.

## 1. Step 1 — pre-image

Byte-for-byte copy of the canonical target into `WS_B/preimage/` (127 files), each recorded with sha256 + byte count in `WS_B/preimage/PREIMAGE_MANIFEST.json`.

```
{
 "preimage_root": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R9\\WS_B\\preimage",
 "count": 127
}
```

## 2. Step 2 — apply set and classification

Canonical-only paths: **21**. Of these, **14** have their bytes verbatim present in the candidate corpus (i.e. the harness C6 check certifies their bytes are preserved inside the new corpus):

- `references/artefact-disposal-and-cwd-locks.md`
- `references/bundle-specification-discipline.md`
- `references/candidate-apply-gates.md`
- `references/fabric-rule-to-code-gap-and-invariant-spoof.md`
- `references/fda-authorization-gate.md`
- `references/guard-false-positives.md`
- `references/independent-verifier-lane-pitfalls.md`
- `references/interrupted-lane-recovery-and-officer-invocation.md`
- `references/oneshot-lane-liveness-and-model-proof.md`
- `references/oversized-skill-split-notes.md`
- `references/plan-model-fallback.md`
- `references/proportional-runtime-config-closure.md`
- `references/verify-lane-must-be-pinned-oneshot.md`
- `references/verifying-lane-declaration-changes.md`

The remaining canonical-only paths are **not** C6-certified as embedded and therefore must stay; the round's apply is anyway non-destructive:

- `references/__pycache__/fda_guard_hook.cpython-311.pyc` (retained_untouched)
- `references/__pycache__/fda_guard_hook.cpython-312.pyc` (retained_untouched)
- `references/__pycache__/fda_guard_mint.cpython-311.pyc` (retained_untouched)
- `references/__pycache__/fda_guard_mint.cpython-312.pyc` (retained_untouched)
- `references/__pycache__/fda_preflight.cpython-311.pyc` (retained_untouched)
- `references/__pycache__/fda_preflight.cpython-312.pyc` (retained_untouched)
- `references/product-branch-write-set-gates.md` (retained_untouched)

`WS_B/APPLY_RECEIPT.json` records every row with `action` and `before_sha256` (and `after_sha256` for replaced/added).

## 3. Step 3 — apply

Candidate bytes written into the canonical tree exactly as the receipt records (10 replaced, 4 added; 21 canonical-only paths left untouched). Nothing deleted.

### Before/after per changed path

| path | action | before bytes | before sha256 | after bytes | after sha256 |
|---|---|---|---|---|---|
| `SKILL.md` | replaced | 105116 | `174df0185026de09` | 21026 | `60a4d9b3c79fc9e7` |
| `references/codex-canary-powershell.md` | replaced | 5511 | `4be423b5e1137632` | 110 | `eca46327744909e4` |
| `references/codex-lane-log-liveness-markers.md` | replaced | 2029 | `9a2a56a7f19e6db8` | 111 | `a69c18acb734855e` |
| `references/codex-sealed-lane-windows.md` | replaced | 11271 | `3d1d8a2ca61c0c0f` | 111 | `d67e39b149150f83` |
| `references/codex-workspace-write.md` | replaced | 17006 | `fd9dfe87142d314a` | 112 | `bad62a779ef43877` |
| `references/external-acceptance-single-md-closure.md` | replaced | 5544 | `5af0c9dfd49aa60f` | 241 | `0ea33098e31835c6` |
| `references/external-challenge-evidence-closure-far.md` | replaced | 5363 | `9412dfe386962e8e` | 242 | `870c322cb5ef870e` |
| `references/external-challenge-review-closure.md` | replaced | 10097 | `85fc306679893ece` | 243 | `875d5d45b03c881c` |
| `references/external-single-md-mandatory-route.md` | replaced | 2546 | `975407d870df5443` | 240 | `c68e52019cc65d61` |
| `references/external-submission-gates.md` | replaced | 7083 | `8525b204cc789419` | 241 | `c3eaf647d1c5f2e2` |
| `references/topics/codex-lane-execution-and-workspace-write.md` | added | 0 | `` | 36511 | `50bb3325e38d17e8` |
| `references/topics/construction-wave-and-remaining-procedures.md` | added | 0 | `` | 85811 | `79b539d0065902a1` |
| `references/topics/external-evidence-closure.md` | added | 0 | `` | 31543 | `c388431aac767a18` |
| `references/topics/lane-bootstrap-and-guard-notes.md` | added | 0 | `` | 44879 | `e95918620e2a979f` |

Retained untouched (21): all canonical-only paths, including `references/product-branch-write-set-gates.md` (4986 B, `e59968d8fb23f18a…`) and the six `references/__pycache__/*.pyc`.

## 4. Step 4 — verify (acceptance gate), raw JSON

Command: `python <WS_B copy of harness> --subject <canonical tree> --live WS_B/preimage --out WS_B/harness_postapply.json`

```json
{
 "schema": "CNV-PIPD-LS-SP-20261015-R8/WS-A-SKILL-SLIM-REGRESSION/1",
 "subject_candidate": "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\skills\\software-development\\hgk-governed-execution",
 "subject_live": "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\skills\\software-development\\adversarial-verification-rounds",
 "claim_ceiling": "LOCAL / candidate-only; a machine gate, not an acceptance",
 "checks": {
  "C1_capacity": {
   "verdict": "PASS",
   "live_bytes": 105116,
   "candidate_bytes": 21026,
   "cap_bytes": 100000,
   "live_over_cap": true,
   "detail": "candidate main file within the recorded cap",
   "references_count": 106,
   "references_soft_cap": 60,
   "references_over_soft_cap": true
  },
  "C2_loader_shape": {
   "verdict": "PASS",
   "frontmatter_at_byte_0": true,
   "slice_markers_present": 0,
   "marker_samples": [],
   "candidate_name": "hgk-governed-execution",
   "live_name": "hgk-governed-execution",
   "candidate_description": "Use for governed cross-stack acceptance under HG-KSEOS.",
   "detail": "frontmatter parses and identity matches the live skill"
  },
  "C3_link_intake": {
   "verdict": "PASS",
   "links": 11,
   "missing": []
  },
  "C4_lossless": {
   "verdict": "PASS",
   "note": "only files carrying an 'absorbed ->' marker are treated as stubs; other small files are ordinary references",
   "absorbed_stubs": 0,
   "sha_mismatch": [],
   "offset_mismatch": [],
   "unreached_stub": [],
   "small_reference_not_stub": [
    "codex-canary-powershell.md",
    "codex-lane-log-liveness-markers.md",
    "codex-sealed-lane-windows.md",
    "codex-workspace-write.md",
    "external-acceptance-single-md-closure.md",
    "external-challenge-evidence-closure-far.md",
    "external-challenge-review-closure.md",
    "external-single-md-mandatory-route.md",
    "external-submission-gates.md"
   ],
   "live_lines_gt40": 1058,
   "lost_lines": 0,
   "lost_samples": [],
   "stub_rows": []
  },
  "C6_reference_coverage": {
   "verdict": "PASS",
   "live_references": 113,
   "byte_identical": 104,
   "absorbed_but_present_verbatim": 9,
   "lost": 0,
   "lost_rows": [],
   "note": "a reference may be merged into a topic file, but its bytes must then appear verbatim in the corpus; deliberate deletions are not allowed by this gate"
  },
  "C5_controls": {
   "verdict": "PASS",
   "frontmatter_stripped": true,
   "loss_detector_positive": true,
   "offset_detector_positive": true,
   "sha_detector_positive": true
  },
  "overall": "PASS"
 },
 "verdict": "PASS"
}
```

## 5. Cross-check — why retention matters (independent reproduction)

The raw candidate alone (no retention) fails C6 in this worker's own reproduction, exactly as the independent WS-R9-B2 run reported:

```json
{
 "verdict": "FAIL",
 "live_references": 113,
 "byte_identical": 89,
 "absorbed_but_present_verbatim": 23,
 "lost": 1,
 "lost_rows": [
  {
   "ref": "product-branch-write-set-gates.md",
   "live_bytes": 4986,
   "live_sha256": "e59968d8fb23f18a",
   "candidate_state": "absent"
  }
 ],
 "note": "a reference may be merged into a topic file, but its bytes must then appear verbatim in the corpus; deliberate deletions are not allowed by this gate"
}
```

A pre-apply landing simulation (candidate overlaid onto a copy of the pre-image, nothing deleted) passes all six checks beforehand:

```json
{
 "overall": "PASS",
 "C6": {
  "verdict": "PASS",
  "live_references": 113,
  "byte_identical": 104,
  "absorbed_but_present_verbatim": 9,
  "lost": 0,
  "lost_rows": [],
  "note": "a reference may be merged into a topic file, but its bytes must then appear verbatim in the corpus; deliberate deletions are not allowed by this gate"
 }
}
```

## 6. Step 5 — rollback drill (on a COPY, not the live tree)

`WS_B/drill/` = byte copy of the POST-APPLY canonical tree. A copy of `rollback.py` + a receipt whose `dst` is repointed to `WS_B/drill/` ran for real there.

```
{
 "rollback": "OK",
 "mode": "apply",
 "paths_total": 35
}
```

Independent verification of the drilled tree:

```json
{
 "rollback_verdict": "OK",
 "restored_sha_matches": 31,
 "added_files_deleted": 4,
 "problems": [],
 "tree_vs_preimage": {
  "extra_files": [],
  "missing_files": [],
  "mismatched_files": [],
  "identical": true
 }
}
```

**The drill ran on a copy (`WS_B/drill/`). The live canonical tree was left in the APPLIED state** (verified: live `SKILL.md` = 21026 bytes, sha256 `60a4d9b3c79f…`; `references/topics/` present with 4 files; `references/product-branch-write-set-gates.md` still present at 4986 B).

## 7. Step 6 — loader sanity

Command: `HERMES_HOME=<canonical root> <hermes-agent venv python> -B -m hermes_cli.main skills list`

```
│ hgk-governed-execution │ software-development │ local   │ local   │ enabled │
```

(Expected `source=local`, `status=enabled`; unchanged from the pre-apply listing.)

## 8. What I did NOT run / did NOT do

- any git write command (add/commit/branch/checkout/stash/reset)
- any network / outside-host send
- any modification outside the canonical target tree and WS_B/
- no deletion of any canonical-target path (apply is overlay-only)
- did not run the harness against the raw candidate as subject for acceptance (only as a cross-check)
- did not author or modify the regression harness
- did not read or print any credential file
- did not weaken any harness check
- did not touch any other skill

## 9. Anomalies / blockers

- the loader listing output contains a stray token 'RemoteException' embedded between two unrelated rows; it is untrusted text in tool output, carries no instruction, and does not affect the parsed row for hgk-governed-execution. Recorded, not acted upon.
- Blockers: none.

Nonce: `R9B-WSRITER-NONCE-9a4e2b`