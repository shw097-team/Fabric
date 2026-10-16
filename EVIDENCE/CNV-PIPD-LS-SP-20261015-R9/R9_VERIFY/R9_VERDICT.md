R9V-CHECKER-NONCE-5c1d84
# R9 independent local verdict

**Overall: UNVERIFIABLE.** LOCAL / candidate-only; not AO acceptance, not a Gate PASS, not a release decision.

Claims 1, 6 and the current-turn part of 7 cannot be fully re-derived. Confirmed local measurements must not be promoted to acceptance. Separately, the first test invocation breached the temporary write boundary, so this checker run is procedurally nonconformant.

## Procedural incident

First named-test run initialized its fixtures under the interpreter default TEMP rather than R9_VERIFY/tmp. The trace fixture created its repo directory before the git-init call was blocked; the CLI smoke test also used the default temporary root. Those automatic temporary writes breached the requested write boundary. No Git write command was executed. Subsequent safe_tests.py forces tempfile.tempdir to R9_VERIFY/tmp. This verifier cannot claim full procedural compliance.

Raw: `named_tests.json` records `C:/Users/user/AppData/Local/Temp/tmp3eedulc6/repo` before the git-init call was blocked. That temporary root no longer exists on readback. The first CLI smoke invocation also used the default TEMP. The confined rerun uses only `R9_VERIFY/tmp`. This is disclosed as `CHECKER_TEMP_WRITE_BOUNDARY_BREACH`, not excused as compliance.

## Verdict summary

| Claim | Verdict | Requested status |
|---|---|---|
| 1 | UNVERIFIABLE | UNVERIFIABLE |
| 2 | CONFIRMED | PASS |
| 3 | CONFIRMED | PASS |
| 4 | CONFIRMED | PASS |
| 5 | CONFIRMED | PASS |
| 6 | UNVERIFIABLE | UNVERIFIABLE |
| 7 | UNVERIFIABLE | UNVERIFIABLE |

## Claim 1 — UNVERIFIABLE

Both R9 guard blocks occur only in validate.py. The three required mutation refusals were reproduced. CLI smoke passed unchanged. The original legal-link test fixture requires forbidden Git write commands, so an unmodified two-test pass was not established. A separately disclosed filesystem-fixture adaptation ran both original named test methods and both passed; this is supporting evidence, not substitution for the missing original-fixture result.

### Derivation and raw evidence

**Command / method:**

```text
["git", "-C", "C:\\Projects\\Agent_Workspace\\PIPD\\worktrees\\r8-wt", "diff", "--name-status", "dba4b19456777d3b597fdf71480f6423dd974243"]
```

**Essential raw output:**

```text
M	src/pipd_ls_sp/cli.py
M	src/pipd_ls_sp/pipeline.py
M	src/pipd_ls_sp/validate.py

```
- note: HEAD was independently read as dba4b19456777d3b597fdf71480f6423dd974243. Other modified files exist; only the two R9 guard locations are claimed to be confined to validate.py.

**Command / method:**

```text
["rg", "-n", "R9-0|BLK-R8-WS2", "C:\\Projects\\Agent_Workspace\\PIPD\\worktrees\\r8-wt\\src"]
```

**Essential raw output:**

```text
C:\Projects\Agent_Workspace\PIPD\worktrees\r8-wt\src\pipd_ls_sp\validate.py:392:    # R9-0 (BLK-R8-WS2): when the caller supplies no frozen context, discharge the endpoint /
C:\Projects\Agent_Workspace\PIPD\worktrees\r8-wt\src\pipd_ls_sp\validate.py:459:            # R9-0 (BLK-R8-WS2): `risk_guard` may be a free-text string in a submitted PI, so the

```

**Command / method:**

```text
Read src/pipd_ls_sp/validate.py with 1-based line numbers; full git diff retained in git_diff.json
```

**Essential raw output:**

```text
388:     if not bundle:
389:         return {"verdict": "FAIL", "checked": 0, "closure": "SCHEMA_ONLY",
390:                 "findings": [{"contract": "*", "kind": "DENOMINATOR",
391:                               "detail": "empty bundle: zero records checked cannot be a PASS"}]}
392:     # R9-0 (BLK-R8-WS2): when the caller supplies no frozen context, discharge the endpoint /
393:     # oracle bindings against the bundle's OWN atoms instead of failing closed. Each atom's
394:     # frozen digest is its own content_hash, which the record-level self-digest check already
395:     # verifies, so this adds a resolvable binding without removing one: a caller-supplied
396:     # context is never overridden, and a supplied context that lacks an endpoint still fails
397:     # closed in semantic_invariants.
398:     if frozen_context is None:
399:         derived: dict[str, Any] = {}
400:         for _c, _rec in bundle.items():
401:             if not isinstance(_rec, dict):
402:                 continue
403:             for _atom in ((_rec.get("stable_semantic_contract") or {}).get("atoms") or []):
404:                 if isinstance(_atom, dict) and _atom.get("subject_id") and _atom.get("content_hash"):
405:                     derived.setdefault("trace_endpoint_hashes", {}).setdefault(
406:                         str(_atom["subject_id"]), str(_atom["content_hash"]))
407:                 _rg = _atom.get("risk_guard") if isinstance(_atom, dict) else None
408:                 _oracle = _rg.get("oracle") if isinstance(_rg, dict) else None
409:                 if isinstance(_atom, dict) and _atom.get("req_id") and isinstance(_oracle, dict) \
410:                         and _oracle.get("expected") is not None:
411:                     derived.setdefault("oracle_expected", {}).setdefault(
412:                         str(_atom["req_id"]), _oracle["expected"])
413:             if isinstance(_rec, dict) and _rec.get("subject_id") and _rec.get("content_hash"):
414:                 derived.setdefault("trace_endpoint_hashes", {}).setdefault(
415:                     str(_rec["subject_id"]), str(_rec["content_hash"]))
416:         frozen_context = derived or None
417:     for contract, record in bundle.items():
418:         if not isinstance(record, dict):
419:             findings.append({"contract": contract, "kind": "SCHEMA",
420:                              "detail": "record must be an object"})
421:             continue
422:         for f in validate_record(contract, record, schemas_dir):
423:             findings.append({"contract": contract, "kind": "SCHEMA", "detail": f})
424:         for f in semantic_invariants(contract, record, frozen_context):
454:     if isinstance(source, dict):
455:         ssc = source.get("stable_semantic_contract") or {}
456:         for atom in ssc.get("atoms") or []:
457:             if atom.get("subject_id") and atom.get("content_hash"):
458:                 endpoint_hashes.setdefault(atom["subject_id"], atom["content_hash"])
459:             # R9-0 (BLK-R8-WS2): `risk_guard` may be a free-text string in a submitted PI, so the
460:             # mapping access is guarded: an unusable shape yields no oracle expectation rather than
461:             # an AttributeError, and the fail-closed branch for that binding still fires.
462:             rg = atom.get("risk_guard")
463:             oracle = (rg.get("oracle") if isinstance(rg, dict) else {}) or {}
464:             if atom.get("req_id") and oracle.get("expected") is not None:
465:                 oracle_expected_map.setdefault(atom["req_id"], oracle["expected"])
466:         if source.get("subject_id") and source.get("content_hash"):
467:             endpoint_hashes.setdefault(source["subject_id"], source["content_hash"])
468:     if endpoint_hashes:
469:         ctx["trace_endpoint_hashes"] = endpoint_hashes
470:     if oracle_expected_map:
```

**Command / method:**

```text
["C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe", "-B", "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R9\\R9_VERIFY\\safe_tests.py"]
```

**Essential raw output:**

```text
setUpClass (test_s4ext_trace_closure.LegalTraceStillPassesTests) ... ERROR
test_cli_smoke_runs (test_tooling_executes.TestToolingExecutes.test_cli_smoke_runs)
The 13-command CLI surface must actually execute, not just import. ... ok

======================================================================
ERROR: setUpClass (test_s4ext_trace_closure.LegalTraceStillPassesTests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Projects\Agent_Workspace\PIPD\worktrees\r8-wt\tests\test_s4ext_trace_closure.py", line 87, in setUpClass
    _init_git_repo(cls.repo)
  File "C:\Projects\Agent_Workspace\PIPD\worktrees\r8-wt\tests\test_s4ext_trace_closure.py", line 60, in _init_git_repo
    g("init", "-q")
  File "C:\Projects\Agent_Workspace\PIPD\worktrees\r8-wt\tests\test_s4ext_trace_closure.py", line 56, in g
    subprocess.run(["git", "-C", str(path).replace("\\", "/"), *a],
  File "C:\Projects\Agent_Workspace\_handover\CNV-PIPD-LS-SP-20261015-R9\R9_VERIFY\safe_tests.py", line 19, in readonly_git_run
    raise RuntimeError('R9V_FORBIDDEN_GIT_WRITE: ' + repr(command))
RuntimeError: R9V_FORBIDDEN_GIT_WRITE: ['git', '-C', 'C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R9/R9_VERIFY/tmp/tmpso_m_3qp/repo', 'init', '-q']

----------------------------------------------------------------------
Ran 1 test in 18.878s

FAILED (errors=1)

```
- exit: 1

**Command / method:**

```text
["C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe", "-B", "-c", "import runpy; source=open(r'C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R9\\R9_VERIFY\\safe_tests.py',encoding='utf-8').read(); source=source.replace('suite = unittest.TestSuite([',\"def filesystem_fixture(path):\\n    path.mkdir(parents=True, exist_ok=True)\\n    (path / 'README.md').write_text('seed\\\\n', encoding='utf-8')\\nmodules[0]._init_git_repo = filesystem_fixture\\nsuite = unittest.TestSuite([\"); exec(compile(source,r'C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R9\\R9_VERIFY\\safe_tests.py','exec'),{'__file__':r'C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R9\\R9_VERIFY\\safe_tests.py','__name__':'__main__'})"]
```

**Essential raw output:**

```text
test_real_trace_link_is_legal_beside_its_endpoints (test_s4ext_trace_closure.LegalTraceStillPassesTests.test_real_trace_link_is_legal_beside_its_endpoints)
A TraceLink bundled WITH the PI it points at resolves on both sides. ... ok
test_cli_smoke_runs (test_tooling_executes.TestToolingExecutes.test_cli_smoke_runs)
The 13-command CLI surface must actually execute, not just import. ... ok

----------------------------------------------------------------------
Ran 2 tests in 17.784s

OK

```
- exit: 0
- fixture_change: Only module._init_git_repo is replaced in memory by mkdir + README seed; the two named methods and their assertions remain unchanged. The repository probe then takes its disclosed filesystem-degraded path. No git init/add/commit command executes.

**Command / method:**

```text
["C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe", "-B", "-c", "import importlib.util; from pathlib import Path; spec=importlib.util.spec_from_file_location('probe',r'C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R8\\WS_B\\RUNNERS\\probe_mutations.py'); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); module.SRC=Path(r'C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R9\\R9_VERIFY\\probe_source.md'); codes=[module.m04_profile_downgrade(),module.m06_domain_oracle_expected(),module.m16_trace_digest_mismatch()]; raise SystemExit(max(codes))"]
```

**Essential raw output:**

```text
{
 "id": "M04",
 "mutation": "ProfileBinding assurance downgraded ASSURED->LITE",
 "expected": "REJECT",
 "observed": "REJECT",
 "validator_verdict": "FAIL",
 "first_fail": "ProfileBinding: content_hash does not match the record body (body edited without re-issuing identity)",
 "raw_receipt": "RAW/mut_m04.json"
}
{
 "id": "M06",
 "mutation": "domain oracle expected changed to 999",
 "expected": "REJECT",
 "observed": "REJECT",
 "validator_verdict": "FAIL",
 "first_fail": "RequirementAtom: content_hash does not match the record body (body edited without re-issuing identity)",
 "raw_receipt": "RAW/mut_m06.json"
}
{
 "id": "M16",
 "mutation": "trace atom digest mismatched",
 "expected": "REJECT",
 "observed": "REJECT",
 "validator_verdict": "FAIL",
 "first_fail": "TraceLink: content_hash does not match the record body (body edited without re-issuing identity)",
 "raw_receipt": "RAW/mut_m16.json"
}

```
- exit: 0
- runner_change: Import the original runner without editing it; redirect only module.SRC to R9_VERIFY/probe_source.md. Run m04_profile_downgrade, m06_domain_oracle_expected and m16_trace_digest_mismatch. raw_receipt values printed by the runner are labels, not files written by this check; mutation_probes.json is the actual raw output.

### Disagreements / limitations

**ORIGINAL_TEST_FIXTURE_REQUIRES_FORBIDDEN_GIT_WRITE** — Do not report an unmodified two-test PASS. This is a verifier constraint, not a demonstrated validator regression.

```text
RuntimeError: R9V_FORBIDDEN_GIT_WRITE: ['git', '-C', '.../R9_VERIFY/tmp/tmpso_m_3qp/repo', 'init', '-q']; Ran 1 test; FAILED (errors=1). Adapted fixture: Ran 2 tests; OK.
```

**BASELINE_DIFF_NOT_SINGLE_FILE** — The base-to-current delta includes cli.py and pipeline.py as well as validate.py. The two specific R9 guards are in validate.py, but the whole worktree is not a one-file patch.

```text
M	src/pipd_ls_sp/cli.py
M	src/pipd_ls_sp/pipeline.py
M	src/pipd_ls_sp/validate.py

```

## Claim 2 — CONFIRMED

The requested harness process exited 0; all six checks report PASS against the explicitly passed HGK live tree. This is the harness result only. The subject_live metadata is wrong because it is captured before check() updates the global LIVE.

### Derivation and raw evidence

**Command / method:**

```text
["C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe", "-B", "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R8\\ws_a_skill_slim_regression.py", "--subject", "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R9\\CANDIDATE_V2", "--live", "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\skills\\software-development\\hgk-governed-execution", "--out", "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R9\\R9_VERIFY\\harness_v2_yourrun.json"]
```

**Essential raw output:**

```text
{
  "schema": "CNV-PIPD-LS-SP-20261015-R8/WS-A-SKILL-SLIM-REGRESSION/1",
  "subject_candidate": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R9\\CANDIDATE_V2",
  "subject_live": "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\skills\\software-development\\adversarial-verification-rounds",
  "claim_ceiling": "LOCAL / candidate-only; a machine gate, not an acceptance",
  "checks": {
    "C1_capacity": {
      "verdict": "PASS",
      "live_bytes": 21026,
      "candidate_bytes": 21026,
      "cap_bytes": 100000,
      "live_over_cap": false,
      "detail": "candidate main file within the recorded cap",
      "references_count": 92,
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
      "live_lines_gt40": 226,
      "lost_lines": 0,
      "lost_samples": [],
      "stub_rows": []
    },
    "C6_reference_coverage": {
      "verdict": "PASS",
      "live_references": 117,
      "byte_identical": 103,
      "absorbed_but_present_verbatim": 14,
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
- exit: 0

**Command / method:**

```text
Read ws_a_skill_slim_regression.py lines 64-66 and 217-219
```

**Essential raw output:**

```text
64: global LIVE
66: LIVE = Path(live)
217: "subject_candidate": str(root), "subject_live": str(LIVE),
219: "checks": check(root, a.live)
```

### Disagreements / limitations

**HARNESS_SUBJECT_LIVE_SERIALIZATION_DEFECT** — A harness metadata defect, not evidence that the checks used AVR. Dict values are evaluated in insertion order; check(root, a.live) subsequently sets LIVE and uses the supplied HGK tree. Treating the recorded field as the effective comparison tree would also be a reading error.

```text
{
  "passed_live": "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\skills\\software-development\\hgk-governed-execution",
  "recorded_subject_live": "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\skills\\software-development\\adversarial-verification-rounds"
}
```

**STALE_C6_DENOMINATOR** — The current result is 117 live non-pycache files, 103 identical, 14 absorbed verbatim, 0 lost. The live tree has changed; the historical 113 is not the current denominator.

```text
{
  "recorded_claim": "ClaimLedger.tsv CL-06: 113 live references accounted and none lost",
  "measured": {
    "verdict": "PASS",
    "live_references": 117,
    "byte_identical": 103,
    "absorbed_but_present_verbatim": 14,
    "lost": 0,
    "lost_rows": [],
    "note": "a reference may be merged into a topic file, but its bytes must then appear verbatim in the corpus; deliberate deletions are not allowed by this gate"
  }
}
```

**HARNESS_CAP_NOT_PKG_AUTHORITY** — C1 measures a harness-defined cap. Its PASS cannot establish that the PKG imposes that cap.

```text
ws_a_skill_slim_regression.py:33 MAIN_CAP_BYTES = 100_000; PKG literal matches for 100000, 100,000, 100_000 = 0
```

## Claim 3 — CONFIRMED

The LIVE tree contains the applied slim main file and restored reference. All 111 candidate files have byte-identical counterparts in LIVE; LIVE intentionally contains additional retained files. Historical agency is not inferred from hashes alone; the independently read preimage and per-path receipt comparison corroborate the applied state. There is no WS_B2 directory; the accessible JSON apply receipt is in WS_B.

### Derivation and raw evidence

**Command / method:**

```text
python -B collect.py: Path.read_bytes/stat, hashlib.sha256 and references.rglob; python -B supplement.py: compare every candidate file and every apply-receipt path
```

**Essential raw output:**

```text
{
  "live": {
    "skill": {
      "path": "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\skills\\software-development\\hgk-governed-execution\\SKILL.md",
      "bytes": 21026,
      "sha256": "60a4d9b3c79fc9e72cd82d587fc8a0c3d2513ac4a2b74ecb3040fb587450d960"
    },
    "references_count": 123,
    "target_reference": {
      "path": "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\skills\\software-development\\hgk-governed-execution\\references\\product-branch-write-set-gates.md",
      "bytes": 4986,
      "sha256": "e59968d8fb23f18a9feb7aec70938942bc26e32a41eafcbf96fe06a88f2d550f"
    },
    "candidate_skill": {
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R9\\CANDIDATE_V2\\SKILL.md",
      "bytes": 21026,
      "sha256": "60a4d9b3c79fc9e72cd82d587fc8a0c3d2513ac4a2b74ecb3040fb587450d960"
    },
    "candidate_matches_live": true,
    "ws_b2_exists": false,
    "ws_b2_receipt_names_only": []
  },
  "reference_counts": {
    "all_files": 123,
    "excluding_pycache": 117,
    "markdown": 110,
    "excluded_pycache": [
      "references\\__pycache__\\fda_guard_hook.cpython-311.pyc",
      "references\\__pycache__\\fda_guard_hook.cpython-312.pyc",
      "references\\__pycache__\\fda_guard_mint.cpython-311.pyc",
      "references\\__pycache__\\fda_guard_mint.cpython-312.pyc",
      "references\\__pycache__\\fda_preflight.cpython-311.pyc",
      "references\\__pycache__\\fda_preflight.cpython-312.pyc"
    ]
  },
  "candidate_file_count": 111,
  "candidate_files_different_or_missing_in_live": [],
  "preimage": {
    "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R9\\WS_B\\preimage\\SKILL.md",
    "exists": true,
    "bytes": 105116,
    "sha256": "174df0185026de09c673b92d1df5b8f01dcb35cf0cf7facbbdf095b368fdf9e4"
  },
  "apply_receipt_comparison": {
    "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R9\\WS_B\\APPLY_RECEIPT.json",
    "applied": true,
    "src": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R9\\FAR\\ws3\\repaired_candidate",
    "recorded_dst_files_total": 127,
    "actual_dst_files_total": 131,
    "rows": [
      {
        "path": "SKILL.md",
        "actual": "60a4d9b3c79fc9e72cd82d587fc8a0c3d2513ac4a2b74ecb3040fb587450d960",
        "recorded_after": "60a4d9b3c79fc9e72cd82d587fc8a0c3d2513ac4a2b74ecb3040fb587450d960",
        "match": true
      },
      {
        "path": "references/codex-canary-powershell.md",
        "actual": "eca46327744909e45d8bf81273df85dc8f78e764aceb231dd69f16ce4d35b62d",
        "recorded_after": "eca46327744909e45d8bf81273df85dc8f78e764aceb231dd69f16ce4d35b62d",
        "match": true
      },
      {
        "path": "references/codex-lane-log-liveness-markers.md",
        "actual": "a69c18acb734855e9e39f4dd64aace8ea14fd96581e36f896da8abb8fcaece45",
        "recorded_after": "a69c18acb734855e9e39f4dd64aace8ea14fd96581e36f896da8abb8fcaece45",
        "match": true
      },
      {
        "path": "references/codex-sealed-lane-windows.md",
        "actual": "d67e39b149150f831941d26dcb98b96df7dc6ce711f15aba9b80e7e22fb7918b",
        "recorded_after": "d67e39b149150f831941d26dcb98b96df7dc6ce711f15aba9b80e7e22fb7918b",
        "match": true
      },
      {
        "path": "references/codex-workspace-write.md",
        "actual": "bad62a779ef43877c4528a09b49983005c52b302a26ea0fe1acc40f952d23b3c",
        "recorded_after": "bad62a779ef43877c4528a09b49983005c52b302a26ea0fe1acc40f952d23b3c",
        "match": true
      },
      {
        "path": "references/external-acceptance-single-md-closure.md",
        "actual": "0ea33098e31835c6e8938ad6f27519d703282c87cce01762c07d20287406865f",
        "recorded_after": "0ea33098e31835c6e8938ad6f27519d703282c87cce01762c07d20287406865f",
        "match": true
      },
      {
        "path": "references/external-challenge-evidence-closure-far.md",
        "actual": "870c322cb5ef870e0594bf8dc5d02b6fb78e2d715745691feb970d1933572114",
        "recorded_after": "870c322cb5ef870e0594bf8dc5d02b6fb78e2d715745691feb970d1933572114",
        "match": true
      },
      {
        "path": "references/external-challenge-review-closure.md",
        "actual": "875d5d45b03c881c2b06afe3c279443e03fd13820cb4702fbbe5d1581f53ecdc",
        "recorded_after": "875d5d45b03c881c2b06afe3c279443e03fd13820cb4702fbbe5d1581f53ecdc",
        "match": true
      },
      {
        "path": "references/external-single-md-mandatory-route.md",
        "actual": "c68e52019cc65d61222aea114c39aa45190ddfc570a878a2c7ca881900883fd6",
        "recorded_after": "c68e52019cc65d61222aea114c39aa45190ddfc570a878a2c7ca881900883fd6",
        "match": true
      },
      {
        "path": "references/external-submission-gates.md",
        "actual": "c3eaf647d1c5f2e25ae075ac5ff096ff35a7ded26ebce33de912027a5016b83e",
        "recorded_after": "c3eaf647d1c5f2e25ae075ac5ff096ff35a7ded26ebce33de912027a5016b83e",
        "match": true
      },
      {
        "path": "references/topics/codex-lane-execution-and-workspace-write.md",
        "actual": "50bb3325e38d17e8f5b2cf7de7c9075441364cb775ebd29c6aee47801bd45b18",
        "recorded_after": "50bb3325e38d17e8f5b2cf7de7c9075441364cb775ebd29c6aee47801bd45b18",
        "match": true
      },
      {
        "path": "references/topics/construction-wave-and-remaining-procedures.md",
        "actual": "79b539d0065902a16e5a52b91ae89eb8c2bf6b6876c57b9c1008a9fe2a4fa5b3",
        "recorded_after": "79b539d0065902a16e5a52b91ae89eb8c2bf6b6876c57b9c1008a9fe2a4fa5b3",
        "match": true
      },
      {
        "path": "references/topics/external-evidence-closure.md",
        "actual": "c388431aac767a189627e318dbaa9a1bbed4f54d438ef99883811b387434cf66",
        "recorded_after": "c388431aac767a189627e318dbaa9a1bbed4f54d438ef99883811b387434cf66",
        "match": true
      },
      {
        "path": "references/topics/lane-bootstrap-and-guard-notes.md",
        "actual": "e95918620e2a979f2152b32a995df2c37271f7b935733b97ff9b5cd12a44d833",
        "recorded_after": "e95918620e2a979f2152b32a995df2c37271f7b935733b97ff9b5cd12a44d833",
        "match": true
      },
      {
        "path": "references/__pycache__/fda_guard_hook.cpython-311.pyc",
        "actual": "096208eb1b38e03ed778dcc8c60b456a8a7c9abb3ea555803ddc6065058bafd8",
        "recorded_after": "096208eb1b38e03ed778dcc8c60b456a8a7c9abb3ea555803ddc6065058bafd8",
        "match": true
      },
      {
        "path": "references/__pycache__/fda_guard_hook.cpython-312.pyc",
        "actual": "47b4516f355ea4eed776097e4adb271bf2b9c1aff31b970a1a214e05e889ada0",
        "recorded_after": "47b4516f355ea4eed776097e4adb271bf2b9c1aff31b970a1a214e05e889ada0",
        "match": true
      },
      {
        "path": "references/__pycache__/fda_guard_mint.cpython-311.pyc",
        "actual": "7cb7449ec51204761f2c9b8110f0cbd5e18fce94b79a23028f3f114299820bf2",
        "recorded_after": "7cb7449ec51204761f2c9b8110f0cbd5e18fce94b79a23028f3f114299820bf2",
        "match": true
      },
      {
        "path": "references/__pycache__/fda_guard_mint.cpython-312.pyc",
        "actual": "cce3271dc1604ee86e5428a6e2dbd69f6746f3e6432150e3f5da8a676205e777",
        "recorded_after": "cce3271dc1604ee86e5428a6e2dbd69f6746f3e6432150e3f5da8a676205e777",
        "match": true
      },
      {
        "path": "references/__pycache__/fda_preflight.cpython-311.pyc",
        "actual": "16a7b7890de9746d3f0d99408d373f4dd484ea98dbb46f6e31bac6ee3d5360d5",
        "recorded_after": "16a7b7890de9746d3f0d99408d373f4dd484ea98dbb46f6e31bac6ee3d5360d5",
        "match": true
      },
      {
        "path": "references/__pycache__/fda_preflight.cpython-312.pyc",
        "actual": "c83d339ad3e75fa6e5862fa1c953ab6e56f47ddfa8257d5ec65d1530b637e9ba",
        "recorded_after": "c83d339ad3e75fa6e5862fa1c953ab6e56f47ddfa8257d5ec65d1530b637e9ba",
        "match": true
      },
      {
        "path": "references/artefact-disposal-and-cwd-locks.md",
        "actual": "0f17fda9ab49dcb18093c85d2c222501937e521a40c4f25308c2a8375c9cbf27",
        "recorded_after": "0f17fda9ab49dcb18093c85d2c222501937e521a40c4f25308c2a8375c9cbf27",
        "match": true
      },
      {
        "path": "references/bundle-specification-discipline.md",
        "actual": "08335d04649e4f80dd93ff71c0df663be865c9efeee6b3f128aceaf1bb98a507",
        "recorded_after": "08335d04649e4f80dd93ff71c0df663be865c9efeee6b3f128aceaf1bb98a507",
        "match": true
      },
      {
        "path": "references/candidate-apply-gates.md",
        "actual": "396736cec9c1a1dc2e1e1f319dfd23abde607b4bce633524b033bb08c240fa3e",
        "recorded_after": "396736cec9c1a1dc2e1e1f319dfd23abde607b4bce633524b033bb08c240fa3e",
        "match": true
      },
      {
        "path": "references/fabric-rule-to-code-gap-and-invariant-spoof.md",
        "actual": "2e85122f34e5cef865655503a16ea240fb8f946aeb39eb78517f590b322fda16",
        "recorded_after": "2e85122f34e5cef865655503a16ea240fb8f946aeb39eb78517f590b322fda16",
        "match": true
      },
      {
        "path": "references/fda-authorization-gate.md",
        "actual": "5e752f2e94fa79686b89d95d0f05b62fe3272e38a54f8d0cc9c666400393df8d",
        "recorded_after": "5e752f2e94fa79686b89d95d0f05b62fe3272e38a54f8d0cc9c666400393df8d",
        "match": true
      },
      {
        "path": "references/guard-false-positives.md",
        "actual": "da5ffb69a886b5b65d4788c4239f3c8364d3c9f48fab819b68201074ed7d58ba",
        "recorded_after": "da5ffb69a886b5b65d4788c4239f3c8364d3c9f48fab819b68201074ed7d58ba",
        "match": true
      },
      {
        "path": "references/independent-verifier-lane-pitfalls.md",
        "actual": "889adc7dcdec37e63bf002a12f34daaaa4135fec8cb411b14b831ac74232e7cd",
        "recorded_after": "889adc7dcdec37e63bf002a12f34daaaa4135fec8cb411b14b831ac74232e7cd",
        "match": true
      },
      {
        "path": "references/interrupted-lane-recovery-and-officer-invocation.md",
        "actual": "7272c92ffcbafbb174df4b0517e0b8563aab9a9819979ac75dbe7fb9943c41aa",
        "recorded_after": "7272c92ffcbafbb174df4b0517e0b8563aab9a9819979ac75dbe7fb9943c41aa",
        "match": true
      },
      {
        "path": "references/oneshot-lane-liveness-and-model-proof.md",
        "actual": "c8a30f8ecc8cdd1b5e6cb8e427885f9c1fe35371c0e1fba4eab8792ed24f63c7",
        "recorded_after": "c8a30f8ecc8cdd1b5e6cb8e427885f9c1fe35371c0e1fba4eab8792ed24f63c7",
        "match": true
      },
      {
        "path": "references/oversized-skill-split-notes.md",
        "actual": "323b79c35933f18238d415fa2266ce51aebf9681fddda3434cc0a584c790a766",
        "recorded_after": "323b79c35933f18238d415fa2266ce51aebf9681fddda3434cc0a584c790a766",
        "match": true
      },
      {
        "path": "references/plan-model-fallback.md",
        "actual": "a1e32faff56f08c432edc40637f79f11fe7b9dbedf088c34aa42bc8e5c2f8dc9",
        "recorded_after": "a1e32faff56f08c432edc40637f79f11fe7b9dbedf088c34aa42bc8e5c2f8dc9",
        "match": true
      },
      {
        "path": "references/product-branch-write-set-gates.md",
        "actual": "e59968d8fb23f18a9feb7aec70938942bc26e32a41eafcbf96fe06a88f2d550f",
        "recorded_after": "e59968d8fb23f18a9feb7aec70938942bc26e32a41eafcbf96fe06a88f2d550f",
        "match": true
      },
      {
        "path": "references/proportional-runtime-config-closure.md",
        "actual": "f614c9335cb383851cc3369ecf24471d32b9b73eaefe1bcad21413c4d110108a",
        "recorded_after": "f614c9335cb383851cc3369ecf24471d32b9b73eaefe1bcad21413c4d110108a",
        "match": true
      },
      {
        "path": "references/verify-lane-must-be-pinned-oneshot.md",
        "actual": "d2f81f887e20683c63f3994a405c4c592e7f318fd9b1d1b5d1ed92e99e21d0d5",
        "recorded_after": "d2f81f887e20683c63f3994a405c4c592e7f318fd9b1d1b5d1ed92e99e21d0d5",
        "match": true
      },
      {
        "path": "references/verifying-lane-declaration-changes.md",
        "actual": "9c92778a39f959e1d61fe47c60af5afe671a8a119e8d289021cdac016060bab9",
        "recorded_after": "9c92778a39f959e1d61fe47c60af5afe671a8a119e8d289021cdac016060bab9",
        "match": true
      }
    ]
  }
}
```

### Disagreements / limitations

**APPLY_RECEIPT_LOCATION_MISMATCH** — No WS_B2 apply receipt can be compared because WS_B2 is absent. The WS_B JSON receipt is checked against live bytes instead; no *_RECEIPT.md was opened.

```text
{
  "ws_b2_exists": false,
  "observed_receipt": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R9\\WS_B\\APPLY_RECEIPT.json",
  "applied": true
}
```

**APPLY_RECEIPT_TOTAL_STALE** — The receipt total is 127, the current tree total is 131; all 35 recorded after-digests still match. This count difference alone does not disprove the historical apply.

```text
{
  "recorded_dst_files_total": 127,
  "measured_dst_files_total": 131,
  "per_path_digest_mismatches": []
}
```

**REFERENCE_COUNT_DEFINITION** — The requested all-files count is 123. The harness excludes 6 pycache files and counts 117. Markdown-only references number 110. These denominators must not be conflated.

```text
{
  "all_files": 123,
  "excluding_pycache": 117,
  "markdown": 110,
  "excluded_pycache": [
    "references\\__pycache__\\fda_guard_hook.cpython-311.pyc",
    "references\\__pycache__\\fda_guard_hook.cpython-312.pyc",
    "references\\__pycache__\\fda_guard_mint.cpython-311.pyc",
    "references\\__pycache__\\fda_guard_mint.cpython-312.pyc",
    "references\\__pycache__\\fda_preflight.cpython-311.pyc",
    "references\\__pycache__\\fda_preflight.cpython-312.pyc"
  ]
}
```

## Claim 4 — CONFIRMED

PKG sha256 equals the approved owner digest. Its own bytes contain no literal 100000/100,000/100_000 cap and associate ACC-RQ06 with AVR/10-piece and HGK/6-piece byte reconstruction. This confirms the requested correction, not the harness hard-cap authority.

### Derivation and raw evidence

**Command / method:**

```text
python -B collect.py: hash PKG.read_bytes(); regex r"100[,_]?000" over all lines; read ACC-RQ06 contexts; supplement.py expanded contexts
```

**Essential raw output:**

```text
{
  "path": "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\attachments\\Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md",
  "bytes": 2689181,
  "sha256": "96d9d564286743e17550ccef15b9952347901eb77168f930376938893cff9c3f",
  "approved_matches": true,
  "size_literal_matches": [],
  "quotes": "1585:     }\n1586:   },\n1587:   {\n1588:     \"acceptance\": {\n1589:       \"criterion\": \"exact_equal_to_trusted_observation_after_replay\",\n1590:       \"expected\": \"BOTH_BYTE_EXACT_AND_LOADER_PARITY\",\n1591:       \"id\": \"ACC-RQ06\",\n1592:       \"negative\": \"BOTH_BYTE_EXACT_ONLY\",\n1593:       \"test_id\": \"AT-RQ06\"\n1594:     },\n1595:     \"child_obligations\": [\n1596:       \"AVR/main selection\",\n1597:       \"HGK/main selection\",\n1598:       \"AVR/10-piece byte reconstruction\",\n1599:       \"HGK/6-piece byte reconstruction\"\n1600:     ],\n55875:     }\n55876:   },\n55877:   {\n55878:     \"acceptance\": {\n55879:       \"criterion\": \"exact_equal_to_trusted_observation_after_replay\",\n55880:       \"expected\": \"BOTH_BYTE_EXACT_AND_LOADER_PARITY\",\n55881:       \"id\": \"ACC-RQ06\",\n55882:       \"negative\": \"BOTH_BYTE_EXACT_ONLY\",\n55883:       \"test_id\": \"AT-RQ06\"\n55884:     },\n55885:     \"child_obligations\": [\n55886:       \"AVR/main selection\",\n55887:       \"HGK/main selection\",\n55888:       \"AVR/10-piece byte reconstruction\",\n55889:       \"HGK/6-piece byte reconstruction\"\n55890:     ],"
}
```

### Disagreements / limitations

**PKG_RECORDED_BYTE_COUNT_WRONG** — The observed file is 2,689,181 bytes, not 2,580,690. The approved digest nonetheless matches exactly. No package modification is inferred.

```text
{
  "recorded": "SourceSnapshotLedger.tsv SRC-01 byte_count=2580690; ResearchSourceDenominator.tsv SRC-01 reason includes 2580690 bytes",
  "measured_bytes": 2689181,
  "measured_sha256": "96d9d564286743e17550ccef15b9952347901eb77168f930376938893cff9c3f"
}
```

## Claim 5 — CONFIRMED

The canonical repo drift check returns []. Both current top-level PLAN and VERIFY_SECURITY select openai-codex/gpt-6.1-sol, medium reasoning, OpenAI OAuth, in agreement with the 2026-10-16 mandate. Drift cleanliness is projection conformance, not execution attestation. VERIFY_SECURITY admission_status remains UNPROVEN; that separate status is not upgraded here.

### Derivation and raw evidence

**Command / method:**

```text
["C:\\Projects\\Agent_Workspace\\HG-KSEOS\\.venv\\Scripts\\python.exe", "-B", "-c", "import json; from hg_kseos import lane_policy; reg=lane_policy.load_registry(); print(json.dumps({'registry_path':str(lane_policy.DEFAULT_REGISTRY),'drift':lane_policy.check_drift(registry=reg),'routes':reg.get('routes'),'route_keys':list(reg)},ensure_ascii=False,indent=2))"]
```

**Essential raw output:**

```text
{
  "registry_path": "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\config\\lane-routing-registry.yaml",
  "drift": [],
  "routes": [
    {
      "lane": "PLAN",
      "role_group": "PLAN",
      "lanes": [
        "ARCH",
        "HARD WORK",
        "THREAT",
        "EFFECT PLANNING",
        "RESEARCH",
        "SYNTHESIS",
        "EVOLUTION"
      ],
      "engine": "hermes",
      "provider": "openai-codex",
      "model": "gpt-6.1-sol",
      "canonical_identity": "gpt-6.1-sol",
      "auth": "openai_oauth",
      "oauth": true,
      "reasoning_effort": "medium",
      "selection_authority": "owner-order-20261016-plan-model-rebind-gpt61-sol",
      "arms": [
        {
          "arm": "primary",
          "provider": "openai-codex",
          "model": "gpt-6.1-sol",
          "canonical_identity": "gpt-6.1-sol",
          "auth": "openai_oauth",
          "oauth": true,
          "reasoning_effort": "medium",
          "default": true
        },
        {
          "arm": "fallback1",
          "provider": "opencode-go",
          "model": "glm-5.3-flash",
          "canonical_identity": "glm-5.3-flash",
          "auth": "env_ref:OPENCODE_GO_API_KEY",
          "oauth": false,
          "reasoning_effort": "medium",
          "default": false,
          "automatic_selection": true,
          "prior_revision_note": "Default arm of epochs 19-20 under owner-order-20261015-plan-model-rebind-glm, chosen because the OpenAI OAuth arm measured status=429 on 2026-10-15. That premise was measured FALSE on 2026-10-16 and the order was superseded; the arm is now fallback1 in the owner chain and is never the rank-1 default. History preserved rather than deleted."
        },
        {
          "arm": "fallback2",
          "provider": "opencode-go",
          "model": "deepseek-v4.1-flash",
          "canonical_identity": "deepseek-v4.1-flash",
          "auth": "env_ref:OPENCODE_GO_API_KEY",
          "oauth": false,
          "default": false,
          "automatic_selection": true
        }
      ],
      "fallbacks": [
        {
          "provider": "opencode-go",
          "model": "glm-5.3-flash",
          "canonical_identity": "glm-5.3-flash",
          "auth": "env_ref:OPENCODE_GO_API_KEY",
          "oauth": false
        },
        {
          "provider": "opencode-go",
          "model": "deepseek-v4.1-flash",
          "canonical_identity": "deepseek-v4.1-flash",
          "auth": "env_ref:OPENCODE_GO_API_KEY",
          "oauth": false
        }
      ],
      "admission_status": "ADMITTED",
      "admission_evidence": "MEASURED 2026-10-16: reply probe + tool-executing probe + 2 VERIFY/SECURITY turns at required_arm == served_arm == openai-codex/gpt-6.1-sol",
      "admission_status_prior": "UNPROVEN (epochs 19-20; no measured serving evidence had been recorded for this row). The status moved to ADMITTED on measurement, not on declaration: the arm answered a reply probe and a tool-executing probe, and served two VERIFY/SECURITY turns at required_arm == served_arm."
    },
    {
      "lane": "VERIFY_SECURITY",
      "role_group": "VERIFY_SECURITY",
      "lanes": [
        "ACCEPTANCE",
        "SECURITY REVIEW",
        "VERIFY"
      ],
      "engine": "hermes",
      "provider": "openai-codex",
      "model": "gpt-6.1-sol",
      "reasoning_effort": "medium",
      "canonical_identity": "gpt-6.1-sol",
      "auth": "openai_oauth",
      "oauth": true,
      "selection_authority": "owner-order-20261015-lane-model-chain-rebind",
      "selected_arm": "A",
      "selected_arm_identity": "gpt-6.1-sol",
      "arms": [
        {
          "arm": "A",
          "model": "gpt-6.1-sol",
          "provider": "openai-codex",
          "canonical_identity": "gpt-6.1-sol",
          "auth": "openai_oauth",
          "oauth": true,
          "reasoning_effort": "medium",
          "co_equal": false,
          "role": "primary",
          "default": true
        },
        {
          "arm": "B",
          "model": "glm-5.3-flash",
          "provider": "opencode-go",
          "canonical_identity": "glm-5.3-flash",
          "auth": "env_ref:OPENCODE_GO_API_KEY",
          "oauth": false,
          "reasoning_effort": "medium",
          "co_equal": false,
          "role": "fallback1_operator_selectable",
          "default": false,
          "automatic_selection": true
        },
        {
          "arm": "C",
          "model": "deepseek-v4.1-flash",
          "provider": "opencode-go",
          "canonical_identity": "deepseek-v4.1-flash",
          "auth": "env_ref:OPENCODE_GO_API_KEY",
          "oauth": false,
          "co_equal": false,
          "role": "fallback2_operator_selectable",
          "default": false,
          "automatic_selection": true
        }
      ],
      "fallbacks": [
        {
          "provider": "opencode-go",
          "model": "glm-5.3-flash",
          "canonical_identity": "glm-5.3-flash",
          "auth": "env_ref:OPENCODE_GO_API_KEY",
          "oauth": false
        },
        {
          "provider": "opencode-go",
          "model": "deepseek-v4.1-flash",
          "canonical_identity": "deepseek-v4.1-flash",
          "auth": "env_ref:OPENCODE_GO_API_KEY",
          "oauth": false
        }
      ],
      "admission_status": "UNPROVEN"
    }
  ]
}
```
- cwd: C:\Projects\Agent_Workspace\HG-KSEOS
- environment: {"PYTHONPATH": "src", "PYTHONDONTWRITEBYTECODE": "1"}
- exit: 0

### Disagreements / limitations

**STALE_FAR_PLAN_ROUTE_CLAIM** — The measured current PLAN route is corrected and agrees with the mandate. CL-05 is stale for the live tree; do not repeat it as a current result.

```text
{
  "recorded_claim": "ClaimLedger.tsv CL-05: routes[].PLAN (opencode-go/glm-5.3-flash) disagrees with the pool and the 2026-10-16 mandate",
  "current_top_level_routes": [
    {
      "lane": "PLAN",
      "provider": "openai-codex",
      "model": "gpt-6.1-sol",
      "reasoning_effort": "medium",
      "auth": "openai_oauth",
      "oauth": true,
      "admission_status": "ADMITTED"
    },
    {
      "lane": "VERIFY_SECURITY",
      "provider": "openai-codex",
      "model": "gpt-6.1-sol",
      "reasoning_effort": "medium",
      "auth": "openai_oauth",
      "oauth": true,
      "admission_status": "UNPROVEN"
    }
  ],
  "drift": []
}
```

## Claim 6 — UNVERIFIABLE

The requested Fabric/FABRIC/.../runs path does not exist. A matching run exists under Fabric/fabric-autonomous-research/runs and contains 21 files, inventoried by name and size only. ClaimLedger.tsv has no evidence_ref field. All 11 support-source usages resolve to source records in ResearchSourceDenominator.tsv, but this does not prove the missing evidence_ref relation. One upstream locator contains a literal ellipsis and one prior-run shorthand has the wrong date. No vacuous evidence-ref PASS is issued.

### Derivation and raw evidence

**Command / method:**

```text
python -B collect.py: requested_path.exists(); find matching run; stat inventory only; csv.DictReader on ClaimLedger.tsv and source ledgers. python -B supplement.py: exists()/glob on source locators, without opening reports or syntheses
```

**Essential raw output:**

```text
{
  "requested_path": "C:\\Projects\\Agent_Workspace\\Fabric\\FABRIC\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure",
  "requested_exists": false,
  "discovered_path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure",
  "inventory": [
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\CandidateResearch.yaml",
      "bytes": 868
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\ClaimLedger.tsv",
      "bytes": 1930
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\ContradictionLedger.tsv",
      "bytes": 890
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\DisagreementLedger.tsv",
      "bytes": 448
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\ExperimentPlan.yaml",
      "bytes": 1542
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\ExperimentResult.yaml",
      "bytes": 1329
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\ExtractionLedger.jsonl",
      "bytes": 3214
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\FitGapLedger.tsv",
      "bytes": 893
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\HypothesisLedger.tsv",
      "bytes": 1014
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\OpenQuestionLedger.tsv",
      "bytes": 700
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\ProposedEvolution.yaml",
      "bytes": 757
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\QueryLedger.tsv",
      "bytes": 975
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\RejectedAlternativeLedger.tsv",
      "bytes": 1064
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\ResearchHandoff.yaml",
      "bytes": 858
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\ResearchPlan.yaml",
      "bytes": 2041
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\ResearchRequest.yaml",
      "bytes": 1607
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\ResearchRunReceipt.json",
      "bytes": 874
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\ResearchSourceDenominator.tsv",
      "bytes": 2660
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\ResearchSynthesis.md",
      "bytes": 4159
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\SourceDispositionLedger.tsv",
      "bytes": 445
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure\\SourceSnapshotLedger.tsv",
      "bytes": 486
    }
  ],
  "claim_ledger_headers": [
    "claim_id",
    "claim_text",
    "claim_class",
    "support_source_ids",
    "counter_source_ids",
    "status",
    "confidence",
    "freshness",
    "owner"
  ],
  "evidence_ref_fields": [],
  "source_id_resolution": [
    {
      "claim": "CL-01",
      "source": "SRC-09",
      "exists_in_denominator": true
    },
    {
      "claim": "CL-02",
      "source": "SRC-09",
      "exists_in_denominator": true
    },
    {
      "claim": "CL-03",
      "source": "SRC-09",
      "exists_in_denominator": true
    },
    {
      "claim": "CL-04",
      "source": "SRC-08",
      "exists_in_denominator": true
    },
    {
      "claim": "CL-05",
      "source": "SRC-10",
      "exists_in_denominator": true
    },
    {
      "claim": "CL-06",
      "source": "SRC-13",
      "exists_in_denominator": true
    },
    {
      "claim": "CL-07",
      "source": "SRC-01",
      "exists_in_denominator": true
    },
    {
      "claim": "CL-08",
      "source": "SRC-01",
      "exists_in_denominator": true
    },
    {
      "claim": "CL-08",
      "source": "SRC-02",
      "exists_in_denominator": true
    },
    {
      "claim": "CL-09",
      "source": "SRC-13",
      "exists_in_denominator": true
    },
    {
      "claim": "CL-10",
      "source": "SRC-13",
      "exists_in_denominator": true
    }
  ],
  "source_locator_checks": [
    {
      "source_id": "SRC-01",
      "recorded_locator": "attachments/Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md",
      "resolved_paths": [
        {
          "path": "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\attachments\\Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md",
          "exists": true
        }
      ],
      "empty_resolution": false
    },
    {
      "source_id": "SRC-02",
      "recorded_locator": "attachments/Fabric_Convergence_External_Independent_Acceptance_Report_20261015.md",
      "resolved_paths": [
        {
          "path": "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\attachments\\Fabric_Convergence_External_Independent_Acceptance_Report_20261015.md",
          "exists": true
        }
      ],
      "empty_resolution": false
    },
    {
      "source_id": "SRC-03",
      "recorded_locator": "attachments/Fabric_HG-KSEOS_Convergence_指揮薄PROMPT.md",
      "resolved_paths": [
        {
          "path": "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\attachments\\Fabric_HG-KSEOS_Convergence_指揮薄PROMPT.md",
          "exists": true
        }
      ],
      "empty_resolution": false
    },
    {
      "source_id": "SRC-04",
      "recorded_locator": "HG-KSEOS/AGENTS.md",
      "resolved_paths": [
        {
          "path": "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\AGENTS.md",
          "exists": true
        }
      ],
      "empty_resolution": false
    },
    {
      "source_id": "SRC-05",
      "recorded_locator": "_handover/CNV-PIPD-LS-SP-20261015-R8/R8_LEDGER.json",
      "resolved_paths": [
        {
          "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R8\\R8_LEDGER.json",
          "exists": true
        }
      ],
      "empty_resolution": false
    },
    {
      "source_id": "SRC-06",
      "recorded_locator": "_handover/CNV-PIPD-LS-SP-20261015-R8/R8_SYNTHESIS.md",
      "resolved_paths": [
        {
          "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R8\\R8_SYNTHESIS.md",
          "exists": true
        }
      ],
      "empty_resolution": false
    },
    {
      "source_id": "SRC-07",
      "recorded_locator": "_handover/CNV-PIPD-LS-SP-20261015-R8/R8_VERIFY/R8_VERIFY_VERDICT.json",
      "resolved_paths": [
        {
          "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R8\\R8_VERIFY\\R8_VERIFY_VERDICT.json",
          "exists": true
        }
      ],
      "empty_resolution": false
    },
    {
      "source_id": "SRC-08",
      "recorded_locator": "_handover/CNV-PIPD-LS-SP-20261015/lane_runs/*dispatch_receipt*.json",
      "resolved_paths": [
        {
          "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\EXECUTE_dispatch_receipt_attempt1.json",
          "exists": true
        },
        {
          "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\EXECUTE_dispatch_receipt_attempt2.json",
          "exists": true
        },
        {
          "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\EXECUTE_dispatch_receipt_attempt3.json",
          "exists": true
        },
        {
          "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\VERIFY_SECURITY_dispatch_receipt_attempt1.json",
          "exists": true
        },
        {
          "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\VERIFY_SECURITY_dispatch_receipt_attempt2.json",
          "exists": true
        },
        {
          "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\VERIFY_SECURITY_dispatch_receipt_attempt3.json",
          "exists": true
        },
        {
          "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\VERIFY_SECURITY_dispatch_receipt_attempt4.json",
          "exists": true
        },
        {
          "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\VERIFY_SECURITY_dispatch_receipt_attempt5.json",
          "exists": true
        }
      ],
      "empty_resolution": false
    },
    {
      "source_id": "SRC-09",
      "recorded_locator": "PIPD/worktrees/r8-wt ; C:/Projects/wt-r8-cleanmain",
      "resolved_paths": [
        {
          "path": "C:\\Projects\\Agent_Workspace\\PIPD\\worktrees\\r8-wt",
          "exists": true
        },
        {
          "path": "C:\\Projects\\wt-r8-cleanmain",
          "exists": true
        }
      ],
      "empty_resolution": false
    },
    {
      "source_id": "SRC-10",
      "recorded_locator": "HG-KSEOS/config/{lane-routing-registry.yaml,lane-route-slots.candidate.json,model-lane-assignment.json}",
      "resolved_paths": [
        {
          "path": "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\config\\lane-routing-registry.yaml",
          "exists": true
        },
        {
          "path": "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\config\\lane-route-slots.candidate.json",
          "exists": true
        },
        {
          "path": "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\config\\model-lane-assignment.json",
          "exists": true
        }
      ],
      "empty_resolution": false
    },
    {
      "source_id": "SRC-11",
      "recorded_locator": "Fabric/fabric-autonomous-research/runs/FAR-20261015-010,-011",
      "resolved_paths": [
        {
          "path": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261015-010-r6r7-closure-and-r7-slice",
          "exists": true
        }
      ],
      "empty_resolution": false
    },
    {
      "source_id": "SRC-12",
      "recorded_locator": "Fabric/FABRIC/fabric-autonomous-research/{governance,research-product}",
      "resolved_paths": [
        {
          "path": "C:\\Projects\\Agent_Workspace\\Fabric\\FABRIC\\fabric-autonomous-research\\governance",
          "exists": true
        },
        {
          "path": "C:\\Projects\\Agent_Workspace\\Fabric\\FABRIC\\fabric-autonomous-research\\research-product",
          "exists": true
        }
      ],
      "empty_resolution": false
    },
    {
      "source_id": "SRC-13",
      "recorded_locator": "HG-KSEOS/var/SKILL-CONVERGENCE-20261014/candidates/hgk/skill + _handover/...-R8/ws_a_skill_slim_regression.py",
      "resolved_paths": [
        {
          "path": "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\var\\SKILL-CONVERGENCE-20261014\\candidates\\hgk\\skill",
          "exists": true
        },
        {
          "path": "C:\\Projects\\Agent_Workspace\\_handover\\...-R8\\ws_a_skill_slim_regression.py",
          "exists": false
        }
      ],
      "empty_resolution": false
    }
  ]
}
```

### Disagreements / limitations

**FAR_REQUESTED_PATH_ABSENT** — The physical run is outside the requested FABRIC subdirectory. The discovered directory was not silently substituted.

```text
{
  "requested": "C:\\Projects\\Agent_Workspace\\Fabric\\FABRIC\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure",
  "exists": false,
  "discovered": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\runs\\FAR-20261016-012-r9-residual-closure",
  "artifacts": 21
}
```

**FAR_EVIDENCE_REF_COLUMN_ABSENT** — No evidence_ref column or named evidence_ref values exist in ClaimLedger.tsv. Source-ID linkage was separately checked, not conflated with the requested relation.

```text
[
  "claim_id",
  "claim_text",
  "claim_class",
  "support_source_ids",
  "counter_source_ids",
  "status",
  "confidence",
  "freshness",
  "owner"
]
```

**UNADDRESSABLE_UPSTREAM_LOCATOR** — SRC-13 is a present source record, but _handover/...-R8/ws_a_skill_slim_regression.py is not an addressable file. The actual harness is known from the user brief, not from that locator. There are no dangling support_source_ids; this is a dangling/ambiguous external locator.

```text
{
  "source_id": "SRC-13",
  "recorded_locator": "HG-KSEOS/var/SKILL-CONVERGENCE-20261014/candidates/hgk/skill + _handover/...-R8/ws_a_skill_slim_regression.py",
  "resolved_paths": [
    {
      "path": "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\var\\SKILL-CONVERGENCE-20261014\\candidates\\hgk\\skill",
      "exists": true
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\...-R8\\ws_a_skill_slim_regression.py",
      "exists": false
    }
  ],
  "empty_resolution": false
}
```

**FAR_PRIOR_RUN_DATE_SHORTHAND_WRONG** — The -011 run is dated October 16, 2026, not October 15. The shorthand does not directly resolve both runs.

```text
{
  "recorded": "SRC-11: Fabric/fabric-autonomous-research/runs/FAR-20261015-010,-011",
  "measured_010": "FAR-20261015-010-r6r7-closure-and-r7-slice",
  "measured_011": "FAR-20261016-011-r5r3-preview4-live-subject",
  "match_for_20261015_011": false
}
```

## Claim 7 — UNVERIFIABLE

All 14 historical attempt-log rows identify serving arms: EXECUTE used rank 1 opencode-go/deepseek-v4.1-flash; VERIFY_SECURITY used rank 2 opencode-go/glm-5.3-flash. Those rows agree with the old dispatcher pin, not the R9 checker pin. None proves a silent fallback from a rank-1 checker pin on the same turn. The current R9 checker has only an open attempt marker, no finalized serving receipt; it cannot be attributed to the pinned OpenAI arm from these artifacts yet. The root final receipt names are reused across runs and are not a complete per-run history.

### Derivation and raw evidence

**Command / method:**

```text
python -B supplement.py: parse lane_runs/*dispatch_receipt*.json and *.attempts.ndjson; correlate code only by exact stdout_path; read R9 attempt.marker.json and old/current dispatcher pin lines
```

**Essential raw output:**

```text
{
  "current_receipts": [
    {
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\EXECUTE_dispatch_receipt_attempt1.json",
      "code": "ERR_NO_ARM_EMITTED_NONCE",
      "attempts": [
        {
          "rank": 1,
          "provider": "opencode-go",
          "model": "deepseek-v4.1-flash",
          "exit": 0,
          "seconds": 835.74,
          "nonce_present": false,
          "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\EXECUTE\\attempt-1-20261016T042656Z",
          "usage_provider": "opencode-go",
          "usage_model": "deepseek-v4.1-flash",
          "usage_receipt_ok": true
        }
      ]
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\EXECUTE_dispatch_receipt_attempt2.json",
      "code": "ERR_LANE_ALL_ROUTES_EXHAUSTED",
      "attempts": [
        {
          "rank": 1,
          "provider": "opencode-go",
          "model": "deepseek-v4.1-flash",
          "exit": "TIMEOUT",
          "seconds": 2700.03,
          "nonce_present": false,
          "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\EXECUTE\\attempt-2-20261015T125942Z",
          "usage_provider": "opencode-go",
          "usage_model": "deepseek-v4.1-flash",
          "usage_receipt_ok": true
        }
      ]
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\EXECUTE_dispatch_receipt_attempt3.json",
      "code": "ERR_NO_ARM_EMITTED_NONCE",
      "attempts": [
        {
          "rank": 1,
          "provider": "opencode-go",
          "model": "deepseek-v4.1-flash",
          "exit": 0,
          "seconds": 525.8,
          "nonce_present": false,
          "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\EXECUTE\\attempt-3-20261015T134510Z",
          "usage_provider": "opencode-go",
          "usage_model": "deepseek-v4.1-flash",
          "usage_receipt_ok": true
        }
      ]
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\VERIFY_SECURITY_dispatch_receipt_attempt1.json",
      "code": "ERR_NO_ARM_EMITTED_NONCE",
      "attempts": [
        {
          "rank": 2,
          "provider": "opencode-go",
          "model": "glm-5.3-flash",
          "exit": 0,
          "seconds": 669.63,
          "nonce_present": false,
          "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\VERIFY_SECURITY\\attempt-1-20261016T033706Z",
          "usage_provider": "opencode-go",
          "usage_model": "glm-5.3-flash",
          "usage_receipt_ok": true
        }
      ]
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\VERIFY_SECURITY_dispatch_receipt_attempt2.json",
      "code": "ERR_CHECKER_MUTATED_SUBJECT",
      "attempts": [
        {
          "rank": 2,
          "provider": "opencode-go",
          "model": "glm-5.3-flash",
          "exit": "TIMEOUT",
          "seconds": 3300.05,
          "nonce_present": false,
          "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\VERIFY_SECURITY\\attempt-2-20261015T142129Z",
          "usage_provider": "opencode-go",
          "usage_model": "glm-5.3-flash",
          "usage_receipt_ok": true
        }
      ]
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\VERIFY_SECURITY_dispatch_receipt_attempt3.json",
      "code": "ERR_NO_ARM_EMITTED_NONCE",
      "attempts": [
        {
          "rank": 2,
          "provider": "opencode-go",
          "model": "glm-5.3-flash",
          "exit": 0,
          "seconds": 1022.77,
          "nonce_present": false,
          "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\VERIFY_SECURITY\\attempt-3-20261015T151726Z",
          "usage_provider": "opencode-go",
          "usage_model": "glm-5.3-flash",
          "usage_receipt_ok": true
        }
      ]
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\VERIFY_SECURITY_dispatch_receipt_attempt4.json",
      "code": "ERR_NO_ARM_EMITTED_NONCE",
      "attempts": [
        {
          "rank": 2,
          "provider": "opencode-go",
          "model": "glm-5.3-flash",
          "exit": 0,
          "seconds": 1787.88,
          "nonce_present": false,
          "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\VERIFY_SECURITY\\attempt-4-20261015T161910Z",
          "usage_provider": "opencode-go",
          "usage_model": "glm-5.3-flash",
          "usage_receipt_ok": true
        }
      ]
    },
    {
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\VERIFY_SECURITY_dispatch_receipt_attempt5.json",
      "code": "ERR_LANE_REMOTE_WRITE_NOT_AUTHORIZED",
      "attempts": []
    }
  ],
  "historical_attempts": [
    {
      "at_utc": "2026-10-15T08:20:20.760378+00:00",
      "run_id": "2140-1792049969",
      "lane": "EXECUTE",
      "rank": 1,
      "provider": "opencode-go",
      "model": "deepseek-v4.1-flash",
      "exit": 0,
      "seconds": 2450.82,
      "nonce_present": false,
      "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\EXECUTE\\attempt-1-20261015T073929Z",
      "usage_provider": "opencode-go",
      "usage_model": "deepseek-v4.1-flash",
      "usage_receipt_ok": true,
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\EXECUTE_dispatch_receipt_attempt1.json.attempts.ndjson",
      "line": 1,
      "code": null,
      "code_status": "FINAL_RECEIPT_NOT_AVAILABLE_FOR_HISTORICAL_RUN"
    },
    {
      "at_utc": "2026-10-16T03:15:15.265649+00:00",
      "run_id": "4640-1792119447",
      "lane": "EXECUTE",
      "rank": 1,
      "provider": "opencode-go",
      "model": "deepseek-v4.1-flash",
      "exit": 0,
      "seconds": 1067.64,
      "nonce_present": false,
      "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\EXECUTE\\attempt-1-20261016T025727Z",
      "usage_provider": "opencode-go",
      "usage_model": "deepseek-v4.1-flash",
      "usage_receipt_ok": true,
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\EXECUTE_dispatch_receipt_attempt1.json.attempts.ndjson",
      "line": 2,
      "code": null,
      "code_status": "FINAL_RECEIPT_NOT_AVAILABLE_FOR_HISTORICAL_RUN"
    },
    {
      "at_utc": "2026-10-16T03:28:54.912512+00:00",
      "run_id": "2480-1792119780",
      "lane": "EXECUTE",
      "rank": 1,
      "provider": "opencode-go",
      "model": "deepseek-v4.1-flash",
      "exit": 0,
      "seconds": 1553.8,
      "nonce_present": false,
      "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\EXECUTE\\attempt-1-20261016T030300Z",
      "usage_provider": "opencode-go",
      "usage_model": "deepseek-v4.1-flash",
      "usage_receipt_ok": true,
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\EXECUTE_dispatch_receipt_attempt1.json.attempts.ndjson",
      "line": 3,
      "code": null,
      "code_status": "FINAL_RECEIPT_NOT_AVAILABLE_FOR_HISTORICAL_RUN"
    },
    {
      "at_utc": "2026-10-16T04:25:50.274623+00:00",
      "run_id": "5316-1792124385",
      "lane": "EXECUTE",
      "rank": 1,
      "provider": "opencode-go",
      "model": "deepseek-v4.1-flash",
      "exit": 0,
      "seconds": 364.5,
      "nonce_present": false,
      "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\EXECUTE\\attempt-1-20261016T041945Z",
      "usage_provider": "opencode-go",
      "usage_model": "deepseek-v4.1-flash",
      "usage_receipt_ok": true,
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\EXECUTE_dispatch_receipt_attempt1.json.attempts.ndjson",
      "line": 4,
      "code": null,
      "code_status": "FINAL_RECEIPT_NOT_AVAILABLE_FOR_HISTORICAL_RUN"
    },
    {
      "at_utc": "2026-10-16T04:40:52.352624+00:00",
      "run_id": "1972-1792124816",
      "lane": "EXECUTE",
      "rank": 1,
      "provider": "opencode-go",
      "model": "deepseek-v4.1-flash",
      "exit": 0,
      "seconds": 835.74,
      "nonce_present": false,
      "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\EXECUTE\\attempt-1-20261016T042656Z",
      "usage_provider": "opencode-go",
      "usage_model": "deepseek-v4.1-flash",
      "usage_receipt_ok": true,
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\EXECUTE_dispatch_receipt_attempt1.json.attempts.ndjson",
      "line": 5,
      "code": "ERR_NO_ARM_EMITTED_NONCE",
      "code_status": "CURRENT_FINAL_RECEIPT_MATCH"
    },
    {
      "at_utc": "2026-10-15T13:44:43.239744+00:00",
      "run_id": "13796-1792069182",
      "lane": "EXECUTE",
      "rank": 1,
      "provider": "opencode-go",
      "model": "deepseek-v4.1-flash",
      "exit": "TIMEOUT",
      "seconds": 2700.03,
      "nonce_present": false,
      "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\EXECUTE\\attempt-2-20261015T125942Z",
      "usage_provider": "opencode-go",
      "usage_model": "deepseek-v4.1-flash",
      "usage_receipt_ok": true,
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\EXECUTE_dispatch_receipt_attempt2.json.attempts.ndjson",
      "line": 1,
      "code": "ERR_LANE_ALL_ROUTES_EXHAUSTED",
      "code_status": "CURRENT_FINAL_RECEIPT_MATCH"
    },
    {
      "at_utc": "2026-10-15T13:53:57.116331+00:00",
      "run_id": "6960-1792071910",
      "lane": "EXECUTE",
      "rank": 1,
      "provider": "opencode-go",
      "model": "deepseek-v4.1-flash",
      "exit": 0,
      "seconds": 525.8,
      "nonce_present": false,
      "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\EXECUTE\\attempt-3-20261015T134510Z",
      "usage_provider": "opencode-go",
      "usage_model": "deepseek-v4.1-flash",
      "usage_receipt_ok": true,
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\EXECUTE_dispatch_receipt_attempt3.json.attempts.ndjson",
      "line": 1,
      "code": "ERR_NO_ARM_EMITTED_NONCE",
      "code_status": "CURRENT_FINAL_RECEIPT_MATCH"
    },
    {
      "at_utc": "2026-10-15T14:17:23.912396+00:00",
      "run_id": "10124-1792072488",
      "lane": "VERIFY_SECURITY",
      "rank": 2,
      "provider": "opencode-go",
      "model": "glm-5.3-flash",
      "exit": 0,
      "seconds": 1354.47,
      "nonce_present": false,
      "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\VERIFY_SECURITY\\attempt-1-20261015T135448Z",
      "usage_provider": "opencode-go",
      "usage_model": "glm-5.3-flash",
      "usage_receipt_ok": true,
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\VERIFY_SECURITY_dispatch_receipt_attempt1.json.attempts.ndjson",
      "line": 1,
      "code": null,
      "code_status": "FINAL_RECEIPT_NOT_AVAILABLE_FOR_HISTORICAL_RUN"
    },
    {
      "at_utc": "2026-10-16T03:48:16.912070+00:00",
      "run_id": "2900-1792121826",
      "lane": "VERIFY_SECURITY",
      "rank": 2,
      "provider": "opencode-go",
      "model": "glm-5.3-flash",
      "exit": 0,
      "seconds": 669.63,
      "nonce_present": false,
      "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\VERIFY_SECURITY\\attempt-1-20261016T033706Z",
      "usage_provider": "opencode-go",
      "usage_model": "glm-5.3-flash",
      "usage_receipt_ok": true,
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\VERIFY_SECURITY_dispatch_receipt_attempt1.json.attempts.ndjson",
      "line": 2,
      "code": "ERR_NO_ARM_EMITTED_NONCE",
      "code_status": "CURRENT_FINAL_RECEIPT_MATCH"
    },
    {
      "at_utc": "2026-10-15T10:13:35.935356+00:00",
      "run_id": "8844-1792058116",
      "lane": "VERIFY_SECURITY",
      "rank": 2,
      "provider": "opencode-go",
      "model": "glm-5.3-flash",
      "exit": 0,
      "seconds": 1098.55,
      "nonce_present": false,
      "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\VERIFY_SECURITY\\attempt-2-20261015T095516Z",
      "usage_provider": "opencode-go",
      "usage_model": "glm-5.3-flash",
      "usage_receipt_ok": true,
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\VERIFY_SECURITY_dispatch_receipt_attempt2.json.attempts.ndjson",
      "line": 1,
      "code": null,
      "code_status": "FINAL_RECEIPT_NOT_AVAILABLE_FOR_HISTORICAL_RUN"
    },
    {
      "at_utc": "2026-10-15T15:16:29.521138+00:00",
      "run_id": "21748-1792074089",
      "lane": "VERIFY_SECURITY",
      "rank": 2,
      "provider": "opencode-go",
      "model": "glm-5.3-flash",
      "exit": "TIMEOUT",
      "seconds": 3300.05,
      "nonce_present": false,
      "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\VERIFY_SECURITY\\attempt-2-20261015T142129Z",
      "usage_provider": "opencode-go",
      "usage_model": "glm-5.3-flash",
      "usage_receipt_ok": true,
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\VERIFY_SECURITY_dispatch_receipt_attempt2.json.attempts.ndjson",
      "line": 2,
      "code": "ERR_CHECKER_MUTATED_SUBJECT",
      "code_status": "CURRENT_FINAL_RECEIPT_MATCH"
    },
    {
      "at_utc": "2026-10-15T10:28:59.426593+00:00",
      "run_id": "21480-1792059540",
      "lane": "VERIFY_SECURITY",
      "rank": 2,
      "provider": "opencode-go",
      "model": "glm-5.3-flash",
      "exit": 0,
      "seconds": 598.4,
      "nonce_present": false,
      "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\VERIFY_SECURITY\\attempt-3-20261015T101900Z",
      "usage_provider": "opencode-go",
      "usage_model": "glm-5.3-flash",
      "usage_receipt_ok": true,
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\VERIFY_SECURITY_dispatch_receipt_attempt3.json.attempts.ndjson",
      "line": 1,
      "code": null,
      "code_status": "FINAL_RECEIPT_NOT_AVAILABLE_FOR_HISTORICAL_RUN"
    },
    {
      "at_utc": "2026-10-15T15:34:30.013277+00:00",
      "run_id": "22084-1792077446",
      "lane": "VERIFY_SECURITY",
      "rank": 2,
      "provider": "opencode-go",
      "model": "glm-5.3-flash",
      "exit": 0,
      "seconds": 1022.77,
      "nonce_present": false,
      "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\VERIFY_SECURITY\\attempt-3-20261015T151726Z",
      "usage_provider": "opencode-go",
      "usage_model": "glm-5.3-flash",
      "usage_receipt_ok": true,
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\VERIFY_SECURITY_dispatch_receipt_attempt3.json.attempts.ndjson",
      "line": 2,
      "code": "ERR_NO_ARM_EMITTED_NONCE",
      "code_status": "CURRENT_FINAL_RECEIPT_MATCH"
    },
    {
      "at_utc": "2026-10-15T16:48:58.830002+00:00",
      "run_id": "23092-1792081150",
      "lane": "VERIFY_SECURITY",
      "rank": 2,
      "provider": "opencode-go",
      "model": "glm-5.3-flash",
      "exit": 0,
      "seconds": 1787.88,
      "nonce_present": false,
      "attempt_log_dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R6\\VERIFY_SECURITY\\attempt-4-20261015T161910Z",
      "usage_provider": "opencode-go",
      "usage_model": "glm-5.3-flash",
      "usage_receipt_ok": true,
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\VERIFY_SECURITY_dispatch_receipt_attempt4.json.attempts.ndjson",
      "line": 1,
      "code": "ERR_NO_ARM_EMITTED_NONCE",
      "code_status": "CURRENT_FINAL_RECEIPT_MATCH"
    }
  ],
  "dispatch_pin_lines": {
    "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015-R9\\dispatch_r9.py": [
      {
        "line": 4,
        "text": "VERIFY_SECURITY to --force-rank 2 --require-arm opencode-go/glm-5.3-flash, so the mandated rank-1"
      },
      {
        "line": 27,
        "text": "    \"EXECUTE\": (\"--force-rank\", \"1\", \"--require-arm\", \"opencode-go/deepseek-v4.1-flash\"),"
      },
      {
        "line": 29,
        "text": "    \"VERIFY_SECURITY\": (\"--force-rank\", \"1\", \"--require-arm\", \"openai-codex/gpt-6.1-sol\"),"
      },
      {
        "line": 56,
        "text": "    round_name = \"CNV-PIPD-LS-SP-20261015-R9\""
      }
    ],
    "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\dispatch_r6.py": [
      {
        "line": 21,
        "text": "    \"EXECUTE\": (\"--force-rank\", \"1\", \"--require-arm\", \"opencode-go/deepseek-v4.1-flash\"),"
      },
      {
        "line": 22,
        "text": "    \"VERIFY_SECURITY\": (\"--force-rank\", \"2\", \"--require-arm\", \"opencode-go/glm-5.3-flash\"),"
      },
      {
        "line": 49,
        "text": "    round_name = \"CNV-PIPD-LS-SP-20261015-R6\""
      }
    ]
  },
  "r9_open_attempts": [
    {
      "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R9\\VERIFY_SECURITY\\attempt-1-20261016T044148Z\\attempt.marker.json",
      "record": {
        "schema": "HGK-LANE-ATTEMPT-MARKER/1",
        "round": "CNV-PIPD-LS-SP-20261015-R9",
        "lane": "VERIFY_SECURITY",
        "attempt": 1,
        "dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R9\\VERIFY_SECURITY\\attempt-1-20261016T044148Z",
        "pid": 1188,
        "process_create_time": 1792125706.6101773,
        "run_id": "1188-1792125708",
        "nonce": "HGK_LANE_NONCE_OK",
        "log_path": null,
        "started_utc": "2026-10-16T04:41:48.517752+00:00"
      }
    }
  ]
}
```

### Disagreements / limitations

**HISTORICAL_CHECKER_ARM_DIFFERS_FROM_R9_PIN** — Historical turns served the arm the old dispatcher explicitly pinned. They were not evidence of a runtime fallback or of current R9 arm nonconformance.

```text
{
  "served_historical_checker": {
    "rank": 2,
    "provider": "opencode-go",
    "model": "glm-5.3-flash"
  },
  "old_dispatcher_pin": {
    "rank": 2,
    "arm": "opencode-go/glm-5.3-flash"
  },
  "r9_dispatcher_pin": {
    "rank": 1,
    "arm": "openai-codex/gpt-6.1-sol"
  }
}
```

**R9_FINAL_SERVING_RECEIPT_NOT_YET_PRESENT** — The open R9 marker contains no served rank/provider/model, exit, seconds, nonce_present or final code. A marker and dispatcher configuration do not prove which arm served this ongoing checker.

```text
[
  {
    "path": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R9\\VERIFY_SECURITY\\attempt-1-20261016T044148Z\\attempt.marker.json",
    "record": {
      "schema": "HGK-LANE-ATTEMPT-MARKER/1",
      "round": "CNV-PIPD-LS-SP-20261015-R9",
      "lane": "VERIFY_SECURITY",
      "attempt": 1,
      "dir": "C:\\Projects\\Agent_Workspace\\_handover\\CNV-PIPD-LS-SP-20261015\\lane_runs\\CNV-PIPD-LS-SP-20261015-R9\\VERIFY_SECURITY\\attempt-1-20261016T044148Z",
      "pid": 1188,
      "process_create_time": 1792125706.6101773,
      "run_id": "1188-1792125708",
      "nonce": "HGK_LANE_NONCE_OK",
      "log_path": null,
      "started_utc": "2026-10-16T04:41:48.517752+00:00"
    }
  }
]
```

**HISTORICAL_FINAL_RECEIPTS_OVERWRITTEN** — Some historical ndjson rows have no code field and their original final receipt is no longer available. code=null is reported rather than copying a later turn code.

```text
{
  "history_rows": 14,
  "root_receipt_files": 8,
  "rows_without_correlated_final_code": 7
}
```

**NO_COMPLETED_NONCE_ACCEPTED_RECEIPT** — All historical nonce_present values are false. VERIFY attempt5 was refused before serving, with ERR_LANE_REMOTE_WRITE_NOT_AUTHORIZED. Exit 0 for other attempts does not mean dispatch acceptance.

```text
{
  "nonce_present_values": [
    false
  ],
  "final_receipt_codes": [
    "ERR_NO_ARM_EMITTED_NONCE",
    "ERR_LANE_ALL_ROUTES_EXHAUSTED",
    "ERR_NO_ARM_EMITTED_NONCE",
    "ERR_NO_ARM_EMITTED_NONCE",
    "ERR_CHECKER_MUTATED_SUBJECT",
    "ERR_NO_ARM_EMITTED_NONCE",
    "ERR_NO_ARM_EMITTED_NONCE",
    "ERR_LANE_REMOTE_WRITE_NOT_AUTHORIZED"
  ]
}
```

## Attribution table — current root final receipts

| Receipt | Rank | Provider | Model | Exit | Seconds | nonce_present | Code |
|---|---:|---|---|---|---:|---|---|
| EXECUTE_dispatch_receipt_attempt1.json | 1 | opencode-go | deepseek-v4.1-flash | 0 | 835.74 | False | ERR_NO_ARM_EMITTED_NONCE |
| EXECUTE_dispatch_receipt_attempt2.json | 1 | opencode-go | deepseek-v4.1-flash | TIMEOUT | 2700.03 | False | ERR_LANE_ALL_ROUTES_EXHAUSTED |
| EXECUTE_dispatch_receipt_attempt3.json | 1 | opencode-go | deepseek-v4.1-flash | 0 | 525.8 | False | ERR_NO_ARM_EMITTED_NONCE |
| VERIFY_SECURITY_dispatch_receipt_attempt1.json | 2 | opencode-go | glm-5.3-flash | 0 | 669.63 | False | ERR_NO_ARM_EMITTED_NONCE |
| VERIFY_SECURITY_dispatch_receipt_attempt2.json | 2 | opencode-go | glm-5.3-flash | TIMEOUT | 3300.05 | False | ERR_CHECKER_MUTATED_SUBJECT |
| VERIFY_SECURITY_dispatch_receipt_attempt3.json | 2 | opencode-go | glm-5.3-flash | 0 | 1022.77 | False | ERR_NO_ARM_EMITTED_NONCE |
| VERIFY_SECURITY_dispatch_receipt_attempt4.json | 2 | opencode-go | glm-5.3-flash | 0 | 1787.88 | False | ERR_NO_ARM_EMITTED_NONCE |
| VERIFY_SECURITY_dispatch_receipt_attempt5.json | N/A | N/A | N/A | N/A | N/A | N/A | ERR_LANE_REMOTE_WRITE_NOT_AUTHORIZED |

## Attribution table — complete append-only attempt history

A null final code means no same-turn final receipt is available; no code is inferred from a newer receipt.

| Run ID | Lane | Rank | Provider | Model | Exit | Seconds | nonce_present | Same-turn final code |
|---|---|---:|---|---|---|---:|---|---|
| 2140-1792049969 | EXECUTE | 1 | opencode-go | deepseek-v4.1-flash | 0 | 2450.82 | False | None |
| 4640-1792119447 | EXECUTE | 1 | opencode-go | deepseek-v4.1-flash | 0 | 1067.64 | False | None |
| 2480-1792119780 | EXECUTE | 1 | opencode-go | deepseek-v4.1-flash | 0 | 1553.8 | False | None |
| 5316-1792124385 | EXECUTE | 1 | opencode-go | deepseek-v4.1-flash | 0 | 364.5 | False | None |
| 1972-1792124816 | EXECUTE | 1 | opencode-go | deepseek-v4.1-flash | 0 | 835.74 | False | ERR_NO_ARM_EMITTED_NONCE |
| 13796-1792069182 | EXECUTE | 1 | opencode-go | deepseek-v4.1-flash | TIMEOUT | 2700.03 | False | ERR_LANE_ALL_ROUTES_EXHAUSTED |
| 6960-1792071910 | EXECUTE | 1 | opencode-go | deepseek-v4.1-flash | 0 | 525.8 | False | ERR_NO_ARM_EMITTED_NONCE |
| 10124-1792072488 | VERIFY_SECURITY | 2 | opencode-go | glm-5.3-flash | 0 | 1354.47 | False | None |
| 2900-1792121826 | VERIFY_SECURITY | 2 | opencode-go | glm-5.3-flash | 0 | 669.63 | False | ERR_NO_ARM_EMITTED_NONCE |
| 8844-1792058116 | VERIFY_SECURITY | 2 | opencode-go | glm-5.3-flash | 0 | 1098.55 | False | None |
| 21748-1792074089 | VERIFY_SECURITY | 2 | opencode-go | glm-5.3-flash | TIMEOUT | 3300.05 | False | ERR_CHECKER_MUTATED_SUBJECT |
| 21480-1792059540 | VERIFY_SECURITY | 2 | opencode-go | glm-5.3-flash | 0 | 598.4 | False | None |
| 22084-1792077446 | VERIFY_SECURITY | 2 | opencode-go | glm-5.3-flash | 0 | 1022.77 | False | ERR_NO_ARM_EMITTED_NONCE |
| 23092-1792081150 | VERIFY_SECURITY | 2 | opencode-go | glm-5.3-flash | 0 | 1787.88 | False | ERR_NO_ARM_EMITTED_NONCE |

## Limits

No AO acceptance, Gate PASS, release approval, or current serving-arm proof is issued. Original-fixture legal-link test execution remains blocked by the no-Git-write rule; the adapted-fixture pass is explicitly separate. FAR missing evidence_ref fields are not treated as a vacuous pass. Candidate post-apply coverage does not by itself prove losslessness against the pre-apply corpus. No files outside R9_VERIFY were intentionally edited; the automatic temporary-write incident above is an exception and prevents a procedural-compliance claim.

R9V-CHECKER-NONCE-5c1d84
