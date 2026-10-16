# E11 / ao_guard precondition investigation

Date: 2026-10-16. Scope: read-only investigation of the canonical HG-KSEOS checkout; this report is the only repository file intentionally created or modified. Repository-relative `file:line` references below refer to the inspected bytes. Execution evidence is embedded in this report, not merely linked to temporary logs. This is evidence, not acceptance or remediation implementation. [Execution: this report:EVIDENCE_E11_PRECONDITION.md:72, EVIDENCE_E11_PRECONDITION.md:307, EVIDENCE_E11_PRECONDITION.md:521.]

## Bottom line

**The historical “5 E11/C2” failures are four E11 guard tests plus one C2 dispatchability test, not five E11-named unit tests. Their denied resources differ: E11a–d probe external relay `auth.json`; C2 reads external `usage.jsonl`.** The old brief conflates these paths. Historical E11 fails at receipt existence, whereas C2 errors by indexing a missing receipt. [Definitions: `tests/test_lane_dispatch_ao_guard.py:419-447`, `tests/test_lane_dispatch_ao_guard.py:571-584`; historical raw: `var/LANE-ENFORCEMENT-APPLY-20261015/lanes/VERIFY_SECURITY/ACC9/work/TEST_RESULTS/test_lane_dispatch_ao_guard.stderr.txt:168-310`; C2 child raw: `var/LANE-ENFORCEMENT-APPLY-20261015/lanes/VERIFY_SECURITY/ACC12/work/TEST_RESULTS/c2_observed.json:16-19`; conflating brief: `var/LANE-ENFORCEMENT-APPLY-20261015/VERIFY_ACCEPT_CANONICAL.md:30-34`.]

**Classification is mixed, not “environment only”:** external access restrictions trigger the failures; non-hermetic tests unnecessarily depend on those external paths; production metadata probes also allow `PermissionError` to escape, crashing without the promised refusal receipt. There is no evidence here that the subject-mutation comparator itself is defective. On this host the unmodified module actually passes **136/136**; redirecting only LOCALAPPDATA for the focused run yields **four E11 failures and two passes**; a test-only hermetic pool/ledger intervention yields **six passes** without disabling any gate. [Code: `scripts/hgk-lane-dispatch.py:862-873`, `scripts/hgk-lane-dispatch.py:1134-1135`, `scripts/hgk-lane-dispatch.py:1748-1765`; fresh evidence: this report:EVIDENCE_E11_PRECONDITION.md:72, EVIDENCE_E11_PRECONDITION.md:93, EVIDENCE_E11_PRECONDITION.md:146, EVIDENCE_E11_PRECONDITION.md:494.]

## 1. Definition and exact case inventory

The defining historical executable matrix is `var/far-ao-independence-20261010/run_negative_deterministic.sh:2-10`, with dispatch invocations at lines 22-49 and its oracle at lines 56-76. It defines **E11a–E11e**, five historical scenarios. The current unittest class contains only **E11a–E11d**. E11e's missing-root behavior is separately tested under `GateEndToEndRefusal`, not under a test named E11e. The historical script was READ, NOT EXECUTED: it overwrites old probe/receipt/log files, contrary to this investigation's one-report write boundary. [Script: `var/far-ao-independence-20261010/run_negative_deterministic.sh:15-36`; current definitions: `tests/test_lane_dispatch_ao_guard.py:194-201`, `tests/test_lane_dispatch_ao_guard.py:362-447`; fresh E11e-equivalent run: this report:EVIDENCE_E11_PRECONDITION.md:93.]

The suggested `var/LANE-ENFORCEMENT-APPLY-20261015/ACCEPTANCE_MATRIX.json` is a different 18-row acceptance matrix; its numeric row 11 concerns missing/exception/timeout hooks, while row 14 concerns checker mutation. It does NOT define E11a–e. [That file: lines 2-3, 75-79, 101-105, 129-136.]

All following IDs are prefixed `tests.test_lane_dispatch_ao_guard.`:

| Case / full class.method suffix | What it actually asserts | Definition |
|---|---|---|
| E11a `DeterministicGuardNegative.test_E11a_a_conforming_attempt_stands` | Clean stub returns rc 0, `ok=true`, `subject_mutation.mutated=false`, first attempt `nonce_present=true`. | `tests/test_lane_dispatch_ao_guard.py:419-424` |
| E11b `DeterministicGuardNegative.test_E11b_mutation_voids_a_would_have_passed_attempt` | Mutation returns rc 3 and `ERR_CHECKER_MUTATED_SUBJECT`; first attempt still has nonce, valid usage receipt and exit 0; `changed` is nonempty. This explicitly proves the guard, not an already-failed child, voided the turn. | `tests/test_lane_dispatch_ao_guard.py:426-434` |
| E11c `DeterministicGuardNegative.test_E11c_removal_voids_a_would_have_passed_attempt` | Removal returns rc 3 and the same mutation code; `removed` is nonempty. Unlike E11b, this method does not separately assert the nonce/usage/child-exit fields. | `tests/test_lane_dispatch_ao_guard.py:436-440` |
| E11d `DeterministicGuardNegative.test_E11d_an_added_file_is_recorded_but_not_fatal` | Creation in a seeded nonempty guarded directory returns rc 0, `ok=true`, nonempty `added`, and `mutated=false`. | `tests/test_lane_dispatch_ao_guard.py:384-394`, `442-447` |
| The fifth historical sandbox failure, NOT E11e: `C2DispatchableConsumer.test_declared_not_dispatchable_arm_is_skipped_with_no_spawn` | Exact rank-2 NVIDIA skipped-arm identity/reason; no rank-2 attempt log; only rank 1 appears in attempts. It does NOT assert overall `ok=true`. | `tests/test_lane_dispatch_ao_guard.py:556-562`, `571-584` |
| Historical E11e, separately covered by `GateEndToEndRefusal.test_guard_root_that_does_not_resolve_is_refused` | Missing guard root: current test asserts rc 4, `ERR_GUARD_ROOT_MISSING`, and `say` contains `vacuous guard`. The historical oracle expects `ok=false` and that code; its comments additionally require refusal before spawn. | `tests/test_lane_dispatch_ao_guard.py:194-201`; `var/far-ao-independence-20261010/run_negative_deterministic.sh:48-49`, `56-76` |

The stub mutates/removes/creates scratch targets, appends only the caller-supplied usage row, emits a nonce-bearing `agent_message`, and returns 0; it is not a model/relay transport test. [Implementation: `tests/fixtures/stub_lane_child.py:18-21`, `47-85`.]

## 2. Observed results: separate fresh observations from historical records

| Run | Actual result | Claim ceiling / evidence |
|---|---|---|
| Canonical host, unmodified source and normal LOCALAPPDATA; absolute Python 3.11 interpreter, `-B -m unittest tests.test_lane_dispatch_ao_guard -v` | Exit 0; 136 tests; OK; all five disputed tests and the E11e-equivalent test pass. | Fresh run, not the earlier host claim. Selected exact runner output below: this report:EVIDENCE_E11_PRECONDITION.md:72. |
| Same checkout and interpreter; focused four E11 + C2 + E11e-equivalent, LOCALAPPDATA redirected to empty scratch | Exit 1; 6 run; 4 failures. E11a/d: `4 != 0`; E11b/c: `4 != 3`. Every E11 receipt says `ERR_RELAY_OAUTH_NEEDS_REAUTH`, `relay home not found`, `nothing was spawned`. C2 and E11e-equivalent pass. | Fresh missing-precondition reproduction, NOT a fresh WinError 5 sandbox reproduction: this report:EVIDENCE_E11_PRECONDITION.md:93. |
| Same focused tests, empty LOCALAPPDATA, in-memory test-only hermetic pool / scratch usage isolation | 6 run; 0 failures, 0 errors. | No source changes, no identity-gate bypass, no real credential fixtures; this report:EVIDENCE_E11_PRECONDITION.md:146. |
| Historical ACC9 frozen-copy run | 136 run; 4 failures, 1 error. | Exact original tracebacks retained, not rerun under the old token/ACL context: `var/LANE-ENFORCEMENT-APPLY-20261015/lanes/VERIFY_SECURITY/ACC9/work/TEST_RESULTS/test_lane_dispatch_ao_guard.stderr.txt:168-316`; this report:EVIDENCE_E11_PRECONDITION.md:307. |
| Historical ACC12 C2 child capture | Child exit 1; no receipt; WinError 5 on `usage.jsonl`. | Actual historical child traceback, not inferred from its parent `NoneType` error: `var/LANE-ENFORCEMENT-APPLY-20261015/lanes/VERIFY_SECURITY/ACC12/work/TEST_RESULTS/c2_observed.json:16-20`; this report:EVIDENCE_E11_PRECONDITION.md:307. |

### First cause, not just the outer assertion

- **Historical E11a–d:** `_case()` fails at `self.assertTrue(json_out.is_file(), p.stdout + p.stderr)` (test line 416). The first underlying exception is `PermissionError: [WinError 5] 存取被拒。` on `C:\Users\user\AppData\Local\HG-KSEOS\opencodex-hermes\auth.json`. Call chain: dispatcher `main:1751` → `identity_check:901` → `probe_relay_pool_health:865` → `Path.is_file` → `stat` → `os.stat`. The guard child never reaches its intended assertion path. Full per-case raw, including runner/test IDs, is embedded below. [`var/LANE-ENFORCEMENT-APPLY-20261015/lanes/VERIFY_SECURITY/ACC9/work/TEST_RESULTS/test_lane_dispatch_ao_guard.stderr.txt:178-310`; this report:EVIDENCE_E11_PRECONDITION.md:307.]
- **Historical C2:** outer test line 579 raises `TypeError: 'NoneType' object is not subscriptable` at `rec["skipped_arms"]`. `_run_dispatch` deliberately returns `None` if no receipt exists. The actual earlier child exception is **not auth.json**: `run_candidate:1135` tries `usage_path.is_file()` / `stat` on external `usage.jsonl`, which raises WinError 5. [`tests/test_lane_dispatch_ao_guard.py:484-493`, `579-584`; `var/LANE-ENFORCEMENT-APPLY-20261015/lanes/VERIFY_SECURITY/ACC9/work/TEST_RESULTS/test_lane_dispatch_ao_guard.stderr.txt:168-175`; `var/LANE-ENFORCEMENT-APPLY-20261015/lanes/VERIFY_SECURITY/ACC12/work/TEST_RESULTS/c2_observed.json:18`; this report:EVIDENCE_E11_PRECONDITION.md:307.]
- **Fresh empty-home E11 run:** no uncaught child traceback: the production identity gate correctly emits rc 4 and a refusal receipt before spawn. The first failing unittest assertion is at lines 421/428/438/444, because the test expected a later clean/mutation outcome without arranging identity prerequisites. The exact four tracebacks and receipts are embedded without replacing them with a PASS. [This report:EVIDENCE_E11_PRECONDITION.md:93; gate: `scripts/hgk-lane-dispatch.py:1757-1765`.]

## 3. Why the environment leaks into these tests

E11 `_case` reads the LIVE pool, binds its fake usage row to LIVE VERIFY rank 1, invokes `--force-rank 1`, and does not supply a fixture `--pool` or `--relay-home`. VERIFY rank 1 is currently `openai-codex/gpt-6.1-sol`, explicitly `identity_requirement=relay_pool`. Thus choosing a Python stub executable does not prevent the production pre-spawn identity check. [`tests/test_lane_dispatch_ao_guard.py:399-415`; `config/lane-route-slots.candidate.json:314-330`; `scripts/hgk-lane-dispatch.py:1691`, `1748-1752`.]

The relay home defaults outside the repository under LOCALAPPDATA; the health check only inspects credential metadata/content and does NOT contact a relay. An absent home returns an unhealthy verdict, but `root.is_dir()` and the candidate `p.is_file()` comprehension sit outside the read exception handler. Denied metadata therefore escapes instead of becoming a named refusal. This is an actual error-handling defect even though it fails closed operationally (no child), not a successful security bypass. [`scripts/hgk-lane-dispatch.py:848-873`, `890-911`, `1748-1765`; synthetic metadata exception propagation verified in this report:EVIDENCE_E11_PRECONDITION.md:494.]

C2 already uses a fixture pool with `identity_requirement=none` for both arms and passes an absent `--relay-home` via `_run_dispatch`. It needs no OAuth credential. However this particular method omits `--usage` although `_stub_env(tmp)` points the stub's writer at `tmp/usage.jsonl`. The dispatcher consequently reads the default LOCALAPPDATA relay ledger instead of that scratch ledger. Denied ledger metadata crashes before child execution; an absent ledger is treated as offset zero, explaining why C2 passes with empty LOCALAPPDATA. [`tests/test_lane_dispatch_ao_guard.py:484-500`, `556-562`, `571-578`; default: `scripts/hgk-lane-dispatch.py:80-81`; pre-child read: `1134-1148`; fresh result: this report:EVIDENCE_E11_PRECONDITION.md:93.]

**Adjudication:** external preconditions are the historical trigger, and the tests are non-hermetic; the uncaught metadata exceptions are genuine product robustness/receipt-contract defects. Neither the historical errors nor the fresh missing-home failures measure mutation detection. Conversely the passing host run and hermetic control exercise those assertions, but do not establish production relay refresh/network health or independent acceptance in the historical sandbox. [Sources and runs cited in sections 1–3; exact runs: this report:EVIDENCE_E11_PRECONDITION.md:72–EVIDENCE_E11_PRECONDITION.md:494.]

## 4. Smallest meaningful repair, without weakening the gate (proposal only)

1. **E11 test setup only:** reuse existing `_hermetic_verify_pool(tmp)`; pass it through `--pool` in `DeterministicGuardNegative._case`; build `HGK_STUB_USAGE_LINE` from that fixture's rank-1 arm rather than the mutable LIVE pool. Pass an explicit absent scratch `--relay-home` as an additional isolation guarantee. Existing `--usage` already points to scratch. The helper already supplies an explicitly key-auth/`identity_requirement=none` stub test arm; it changes the test input, not the production admission rule. Keep all current clean/mutate/remove/create assertions. [`tests/test_lane_dispatch_ao_guard.py:376-447`, `476-482`.]
2. **C2 one argument pair:** add `--usage str(tmp / "usage.jsonl")` to `test_declared_not_dispatchable_arm_is_skipped_with_no_spawn`, matching `_stub_env(tmp)` and neighboring C2 tests. Preserve exact skipped-arm list, no rank-2 log, and rank-1-only attempt assertions. [`tests/test_lane_dispatch_ao_guard.py:496-500`, `571-595`.]
3. **Production robustness, separate from test isolation:** catch `OSError` around the relay root/candidate METADATA checks as well as credential reads; return an unhealthy identity verdict with an unreadable-resource detail so the existing rc-4 refusal path writes a receipt. For the usage ledger, turn unreadable metadata into a typed pre-spawn failure receipt; do NOT silently substitute offset zero (which is reserved for genuinely absent ledgers), do NOT accept usage, and do NOT spawn. Add deterministic denied-stat regressions requiring a non-OK receipt and zero child spawns. The missing catch sites are `scripts/hgk-lane-dispatch.py:862-873` and `1134-1135`; the existing receipt-refusal path is `1757-1765`. The synthetic negative below proves the first hole remains present, but no patch or proposed new error code has been implemented. [This report:EVIDENCE_E11_PRECONDITION.md:494.]

The six-test in-memory control actually exercised items 1–2's essential pool/usage isolation (plus scratch usage for the E11e-equivalent call) under empty LOCALAPPDATA and passed. It did not add the optional explicit E11 `--relay-home`, implement item 3, or run the entire 136-test module with modified fixture inputs. Its argument interception and exact commands are embedded below. Existing OAuth-negative/positive tests remain unchanged and should continue to enforce absent refresh material refusal and fixture-refreshable admission; do not use `--no-identity-gate`, delete tests, blanket-skip them, or copy real credentials into the checker. [`tests/test_lane_dispatch_ao_guard.py:51-75`, `180-187`, `290-296`; this report:EVIDENCE_E11_PRECONDITION.md:146.]

## 5. What remains unknown / not claimed

- This investigation did not recreate the historical Codex sandbox token, ACL policy, or frozen-copy runtime. Its actual WinError 5 observations are historical raw records, not new OS-denial results. The fresh denied-metadata probe is explicitly synthetic. [Historical bindings/paths and traceback: this report:EVIDENCE_E11_PRECONDITION.md:307; synthetic probe: EVIDENCE_E11_PRECONDITION.md:494.]
- No real relay network call, token refresh, model execution, or credential-validity test was performed. The passing host suite proves only its asserted behavior; the health probe is metadata/content-only, and the child is a deterministic stub. [`scripts/hgk-lane-dispatch.py:859-860`; `tests/fixtures/stub_lane_child.py:18-21`, `78-85`; fresh runs: EVIDENCE_E11_PRECONDITION.md:72–EVIDENCE_E11_PRECONDITION.md:146.]
- The historical E11 shell runner itself was not rerun because it writes old evidence. E11e was exercised via its current equivalent test, not by claiming that old script's present-day output. [`var/far-ao-independence-20261010/run_negative_deterministic.sh:24-36`; fresh equivalent: EVIDENCE_E11_PRECONDITION.md:93, EVIDENCE_E11_PRECONDITION.md:146.]
- No remediation was committed or applied. The proposed new denied-ledger receipt behavior and production catch repair remain unimplemented/unverified. The isolated test experiment is not a claim of a repaired full suite or acceptance. [Fresh control scope: EVIDENCE_E11_PRECONDITION.md:146; boundary evidence: EVIDENCE_E11_PRECONDITION.md:521.]
- The repository was already dirty. A metadata comparison found no changes among all initially stat-readable files before creating this report; the scan had inaccessible/long-path entries, so it is not a complete cryptographic proof of the entire tree. Initial collection also encountered a long-path traversal failure before the first test run. Tool scratch and test temporary files are outside the repository; the initial run used the runtime's existing temp setting, and later runs explicitly redirected TMP/TEMP/TMPDIR to Hermes scratch. [Boundary measurement: EVIDENCE_E11_PRECONDITION.md:521; execution driver: EVIDENCE_E11_PRECONDITION.md:533.]

## Appendix A — fresh unmodified host runner and selected exact output

```text
cwd: C:\Projects\Agent_Workspace\HG-KSEOS
timestamp: 2026-10-16T12:18:13.671687+08:00
command: C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe -B -m unittest tests.test_lane_dispatch_ao_guard -v
PYTHONDONTWRITEBYTECODE=1
exit_code: 0
test_declared_not_dispatchable_arm_is_skipped_with_no_spawn (tests.test_lane_dispatch_ao_guard.C2DispatchableConsumer.test_declared_not_dispatchable_arm_is_skipped_with_no_spawn) ... ok
test_E11a_a_conforming_attempt_stands (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11a_a_conforming_attempt_stands) ... ok
test_E11b_mutation_voids_a_would_have_passed_attempt (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11b_mutation_voids_a_would_have_passed_attempt) ... ok
test_E11c_removal_voids_a_would_have_passed_attempt (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11c_removal_voids_a_would_have_passed_attempt) ... ok
test_E11d_an_added_file_is_recorded_but_not_fatal (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11d_an_added_file_is_recorded_but_not_fatal) ... ok
test_guard_root_that_does_not_resolve_is_refused (tests.test_lane_dispatch_ao_guard.GateEndToEndRefusal.test_guard_root_that_does_not_resolve_is_refused)

----------------------------------------------------------------------
Ran 136 tests in 27.343s

OK
```

## Appendix B — fresh empty-LOCALAPPDATA runner, exact failures

```text
command: C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe -B -m unittest tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative tests.test_lane_dispatch_ao_guard.C2DispatchableConsumer.test_declared_not_dispatchable_arm_is_skipped_with_no_spawn tests.test_lane_dispatch_ao_guard.GateEndToEndRefusal.test_guard_root_that_does_not_resolve_is_refused -v
LOCALAPPDATA=C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\cache\scratch\e11-investigation-20261016\empty-localappdata
exit_code: 1
test_E11a_a_conforming_attempt_stands (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11a_a_conforming_attempt_stands) ... FAIL
test_E11b_mutation_voids_a_would_have_passed_attempt (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11b_mutation_voids_a_would_have_passed_attempt) ... FAIL
test_E11c_removal_voids_a_would_have_passed_attempt (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11c_removal_voids_a_would_have_passed_attempt) ... FAIL
test_E11d_an_added_file_is_recorded_but_not_fatal (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11d_an_added_file_is_recorded_but_not_fatal) ... FAIL
test_declared_not_dispatchable_arm_is_skipped_with_no_spawn (tests.test_lane_dispatch_ao_guard.C2DispatchableConsumer.test_declared_not_dispatchable_arm_is_skipped_with_no_spawn) ... ok
test_guard_root_that_does_not_resolve_is_refused (tests.test_lane_dispatch_ao_guard.GateEndToEndRefusal.test_guard_root_that_does_not_resolve_is_refused)
MEASURED (probe E5b): an unresolvable guard root produced a zero-file snapshot and the ... ok

======================================================================
FAIL: test_E11a_a_conforming_attempt_stands (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11a_a_conforming_attempt_stands)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Projects\Agent_Workspace\HG-KSEOS\tests\test_lane_dispatch_ao_guard.py", line 421, in test_E11a_a_conforming_attempt_stands
    self.assertEqual(rc, 0, r)
AssertionError: 4 != 0 : {'schema': 'HGK-LANE-RESOLUTION/1', 'ok': False, 'lane': 'VERIFY_SECURITY', 'code': 'ERR_RELAY_OAUTH_NEEDS_REAUTH', 'detail': 'relay home not found: C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\opencodex-hermes', 'generated_utc': '2026-10-16T04:19:04.469551+00:00', 'identity_gate': {'state': 'enforced', 'lane_home': 'C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\codex-hermes', 'relay_home': 'C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\opencodex-hermes', 'arms': [{'rank': 1, 'provider': 'openai-codex', 'model': 'gpt-6.1-sol', 'requirement': 'relay_pool', 'ok': False, 'detail': 'relay home not found: C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\opencodex-hermes', 'code': 'ERR_RELAY_OAUTH_NEEDS_REAUTH'}], 'degraded': True, 'required_arm': None}, 'skipped_arms': [{'rank': 4, 'arm': 'nvidia/deepseek-ai/deepseek-v4.1-flash', 'reason': 'UNREACHABLE_MEASURED_20261011'}], 'say': 'no arm survived the identity gate; nothing was spawned', 'codex_home': 'C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\codex-hermes', 'codex_home_is_declared_lane_home': True}

======================================================================
FAIL: test_E11b_mutation_voids_a_would_have_passed_attempt (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11b_mutation_voids_a_would_have_passed_attempt)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Projects\Agent_Workspace\HG-KSEOS\tests\test_lane_dispatch_ao_guard.py", line 428, in test_E11b_mutation_voids_a_would_have_passed_attempt
    self.assertEqual(rc, 3, r)
AssertionError: 4 != 3 : {'schema': 'HGK-LANE-RESOLUTION/1', 'ok': False, 'lane': 'VERIFY_SECURITY', 'code': 'ERR_RELAY_OAUTH_NEEDS_REAUTH', 'detail': 'relay home not found: C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\opencodex-hermes', 'generated_utc': '2026-10-16T04:19:04.643017+00:00', 'identity_gate': {'state': 'enforced', 'lane_home': 'C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\codex-hermes', 'relay_home': 'C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\opencodex-hermes', 'arms': [{'rank': 1, 'provider': 'openai-codex', 'model': 'gpt-6.1-sol', 'requirement': 'relay_pool', 'ok': False, 'detail': 'relay home not found: C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\opencodex-hermes', 'code': 'ERR_RELAY_OAUTH_NEEDS_REAUTH'}], 'degraded': True, 'required_arm': None}, 'skipped_arms': [{'rank': 4, 'arm': 'nvidia/deepseek-ai/deepseek-v4.1-flash', 'reason': 'UNREACHABLE_MEASURED_20261011'}], 'say': 'no arm survived the identity gate; nothing was spawned', 'codex_home': 'C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\codex-hermes', 'codex_home_is_declared_lane_home': True}

======================================================================
FAIL: test_E11c_removal_voids_a_would_have_passed_attempt (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11c_removal_voids_a_would_have_passed_attempt)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Projects\Agent_Workspace\HG-KSEOS\tests\test_lane_dispatch_ao_guard.py", line 438, in test_E11c_removal_voids_a_would_have_passed_attempt
    self.assertEqual(rc, 3, r)
AssertionError: 4 != 3 : {'schema': 'HGK-LANE-RESOLUTION/1', 'ok': False, 'lane': 'VERIFY_SECURITY', 'code': 'ERR_RELAY_OAUTH_NEEDS_REAUTH', 'detail': 'relay home not found: C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\opencodex-hermes', 'generated_utc': '2026-10-16T04:19:04.791999+00:00', 'identity_gate': {'state': 'enforced', 'lane_home': 'C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\codex-hermes', 'relay_home': 'C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\opencodex-hermes', 'arms': [{'rank': 1, 'provider': 'openai-codex', 'model': 'gpt-6.1-sol', 'requirement': 'relay_pool', 'ok': False, 'detail': 'relay home not found: C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\opencodex-hermes', 'code': 'ERR_RELAY_OAUTH_NEEDS_REAUTH'}], 'degraded': True, 'required_arm': None}, 'skipped_arms': [{'rank': 4, 'arm': 'nvidia/deepseek-ai/deepseek-v4.1-flash', 'reason': 'UNREACHABLE_MEASURED_20261011'}], 'say': 'no arm survived the identity gate; nothing was spawned', 'codex_home': 'C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\codex-hermes', 'codex_home_is_declared_lane_home': True}

======================================================================
FAIL: test_E11d_an_added_file_is_recorded_but_not_fatal (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11d_an_added_file_is_recorded_but_not_fatal)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Projects\Agent_Workspace\HG-KSEOS\tests\test_lane_dispatch_ao_guard.py", line 444, in test_E11d_an_added_file_is_recorded_but_not_fatal
    self.assertEqual(rc, 0, r)
AssertionError: 4 != 0 : {'schema': 'HGK-LANE-RESOLUTION/1', 'ok': False, 'lane': 'VERIFY_SECURITY', 'code': 'ERR_RELAY_OAUTH_NEEDS_REAUTH', 'detail': 'relay home not found: C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\opencodex-hermes', 'generated_utc': '2026-10-16T04:19:04.944161+00:00', 'identity_gate': {'state': 'enforced', 'lane_home': 'C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\codex-hermes', 'relay_home': 'C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\opencodex-hermes', 'arms': [{'rank': 1, 'provider': 'openai-codex', 'model': 'gpt-6.1-sol', 'requirement': 'relay_pool', 'ok': False, 'detail': 'relay home not found: C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\opencodex-hermes', 'code': 'ERR_RELAY_OAUTH_NEEDS_REAUTH'}], 'degraded': True, 'required_arm': None}, 'skipped_arms': [{'rank': 4, 'arm': 'nvidia/deepseek-ai/deepseek-v4.1-flash', 'reason': 'UNREACHABLE_MEASURED_20261011'}], 'say': 'no arm survived the identity gate; nothing was spawned', 'codex_home': 'C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\empty-localappdata\\HG-KSEOS\\codex-hermes', 'codex_home_is_declared_lane_home': True}

----------------------------------------------------------------------
Ran 6 tests in 1.153s

FAILED (failures=4)

```

## Appendix C — test-only isolation control, exact output and argument changes

In-memory subprocess argument interception; E11 gets existing hermetic pool helper and matching stub usage; C2 gets scratch --usage; no production code or gate changed. The original assertions and production dispatcher remain unchanged.

```text
test_E11a_a_conforming_attempt_stands (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11a_a_conforming_attempt_stands) ... ok
test_E11b_mutation_voids_a_would_have_passed_attempt (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11b_mutation_voids_a_would_have_passed_attempt) ... ok
test_E11c_removal_voids_a_would_have_passed_attempt (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11c_removal_voids_a_would_have_passed_attempt) ... ok
test_E11d_an_added_file_is_recorded_but_not_fatal (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11d_an_added_file_is_recorded_but_not_fatal) ... ok
test_declared_not_dispatchable_arm_is_skipped_with_no_spawn (tests.test_lane_dispatch_ao_guard.C2DispatchableConsumer.test_declared_not_dispatchable_arm_is_skipped_with_no_spawn) ... ok
test_guard_root_that_does_not_resolve_is_refused (tests.test_lane_dispatch_ao_guard.GateEndToEndRefusal.test_guard_root_that_does_not_resolve_is_refused)
MEASURED (probe E5b): an unresolvable guard root produced a zero-file snapshot and the ... ok

----------------------------------------------------------------------
Ran 6 tests in 2.102s

OK

```

Exact intercepted dispatcher commands:

```json
[
  [
    "C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python311\\python.exe",
    "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\scripts\\hgk-lane-dispatch.py",
    "--lane",
    "VERIFY_SECURITY",
    "--force-rank",
    "1",
    "--codex-executable",
    "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\tests\\fixtures\\stub_lane_child.py",
    "--usage",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-neg-i86n43ad\\usage.jsonl",
    "--guard-subject",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-neg-i86n43ad\\subject.txt",
    "--attempt-log-dir",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-neg-i86n43ad\\logs",
    "--json-out",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-neg-i86n43ad\\receipt.json",
    "--timeout",
    "120",
    "--prompt",
    "deterministic stub case",
    "--pool",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\pool-fixture.json"
  ],
  [
    "C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python311\\python.exe",
    "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\scripts\\hgk-lane-dispatch.py",
    "--lane",
    "VERIFY_SECURITY",
    "--force-rank",
    "1",
    "--codex-executable",
    "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\tests\\fixtures\\stub_lane_child.py",
    "--usage",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-neg-eplxbnba\\usage.jsonl",
    "--guard-subject",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-neg-eplxbnba\\subject.txt",
    "--attempt-log-dir",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-neg-eplxbnba\\logs",
    "--json-out",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-neg-eplxbnba\\receipt.json",
    "--timeout",
    "120",
    "--prompt",
    "deterministic stub case",
    "--pool",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\pool-fixture.json"
  ],
  [
    "C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python311\\python.exe",
    "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\scripts\\hgk-lane-dispatch.py",
    "--lane",
    "VERIFY_SECURITY",
    "--force-rank",
    "1",
    "--codex-executable",
    "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\tests\\fixtures\\stub_lane_child.py",
    "--usage",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-neg-7sbf_jae\\usage.jsonl",
    "--guard-subject",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-neg-7sbf_jae\\subject.txt",
    "--attempt-log-dir",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-neg-7sbf_jae\\logs",
    "--json-out",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-neg-7sbf_jae\\receipt.json",
    "--timeout",
    "120",
    "--prompt",
    "deterministic stub case",
    "--pool",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\pool-fixture.json"
  ],
  [
    "C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python311\\python.exe",
    "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\scripts\\hgk-lane-dispatch.py",
    "--lane",
    "VERIFY_SECURITY",
    "--force-rank",
    "1",
    "--codex-executable",
    "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\tests\\fixtures\\stub_lane_child.py",
    "--usage",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-neg-fna4ozgx\\usage.jsonl",
    "--guard-subject",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-neg-fna4ozgx\\subjectdir",
    "--attempt-log-dir",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-neg-fna4ozgx\\logs",
    "--json-out",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-neg-fna4ozgx\\receipt.json",
    "--timeout",
    "120",
    "--prompt",
    "deterministic stub case",
    "--pool",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\pool-fixture.json"
  ],
  [
    "C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python311\\python.exe",
    "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\scripts\\hgk-lane-dispatch.py",
    "--json-out",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-lhr-d6n8ftmk\\receipt.json",
    "--relay-home",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-lhr-d6n8ftmk\\no-such-relay-home",
    "--lane",
    "VERIFY_SECURITY",
    "--pool",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-lhr-c2-nnkggybv\\pool-fixture.json",
    "--codex-executable",
    "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\tests\\fixtures\\stub_lane_child.py",
    "--attempt-log-dir",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-lhr-c2-nnkggybv\\logs",
    "--timeout",
    "30",
    "--prompt",
    "x",
    "--usage",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\isolated-usage-4.jsonl"
  ],
  [
    "C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python311\\python.exe",
    "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\scripts\\hgk-lane-dispatch.py",
    "--lane",
    "VERIFY_SECURITY",
    "--prompt",
    "PLACEHOLDER-NOT-USED-BY-A-REFUSAL",
    "--json-out",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-e2e-hc_wpzld\\receipt.json",
    "--relay-home",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\hgk-e2e-hc_wpzld\\no-such-relay-home",
    "--guard-subject",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\tmp0pgn8b8n\\absent-dir",
    "--usage",
    "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\e11-investigation-20261016\\isolated-usage-5.jsonl"
  ]
]
```

## Appendix D — historical failures preserved verbatim

Historical runner (ACC9 source `var/LANE-ENFORCEMENT-APPLY-20261015/lanes/VERIFY_SECURITY/ACC9/work/TEST_RESULTS/test_lane_dispatch_ao_guard_unittest.json:2`):

```text
C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe -B -m unittest -v tests.test_lane_dispatch_ao_guard
```

Original ACC9 failure section (var/LANE-ENFORCEMENT-APPLY-20261015/lanes/VERIFY_SECURITY/ACC9/work/TEST_RESULTS/test_lane_dispatch_ao_guard.stderr.txt:168-316):

```text
======================================================================
ERROR: test_declared_not_dispatchable_arm_is_skipped_with_no_spawn (tests.test_lane_dispatch_ao_guard.C2DispatchableConsumer.test_declared_not_dispatchable_arm_is_skipped_with_no_spawn)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\tests\test_lane_dispatch_ao_guard.py", line 579, in test_declared_not_dispatchable_arm_is_skipped_with_no_spawn
    self.assertEqual(rec["skipped_arms"],
                     ~~~^^^^^^^^^^^^^^^^
TypeError: 'NoneType' object is not subscriptable

======================================================================
FAIL: test_E11a_a_conforming_attempt_stands (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11a_a_conforming_attempt_stands)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\tests\test_lane_dispatch_ao_guard.py", line 420, in test_E11a_a_conforming_attempt_stands
    rc, r = self._case("clean")
            ^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\tests\test_lane_dispatch_ao_guard.py", line 416, in _case
    self.assertTrue(json_out.is_file(), p.stdout + p.stderr)
AssertionError: False is not true : Traceback (most recent call last):
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 2275, in <module>
    raise SystemExit(main())
                     ^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 1751, in main
    verdict = identity_check(e, args.lane, lane_home, relay_home)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 901, in identity_check
    ok, detail = probe_relay(relay_home)
                 ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 865, in probe_relay_pool_health
    candidates = [p for p in (root / "auth.json", root / "codex-accounts.json") if p.is_file()]
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 865, in <listcomp>
    candidates = [p for p in (root / "auth.json", root / "codex-accounts.json") if p.is_file()]
                                                                                   ^^^^^^^^^^^
  File "C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\Lib\pathlib.py", line 1267, in is_file
    return S_ISREG(self.stat().st_mode)
                   ^^^^^^^^^^^
  File "C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\Lib\pathlib.py", line 1013, in stat
    return os.stat(self, follow_symlinks=follow_symlinks)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] 存取被拒。: 'C:\\Users\\user\\AppData\\Local\\HG-KSEOS\\opencodex-hermes\\auth.json'


======================================================================
FAIL: test_E11b_mutation_voids_a_would_have_passed_attempt (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11b_mutation_voids_a_would_have_passed_attempt)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\tests\test_lane_dispatch_ao_guard.py", line 427, in test_E11b_mutation_voids_a_would_have_passed_attempt
    rc, r = self._case("mutate")
            ^^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\tests\test_lane_dispatch_ao_guard.py", line 416, in _case
    self.assertTrue(json_out.is_file(), p.stdout + p.stderr)
AssertionError: False is not true : Traceback (most recent call last):
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 2275, in <module>
    raise SystemExit(main())
                     ^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 1751, in main
    verdict = identity_check(e, args.lane, lane_home, relay_home)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 901, in identity_check
    ok, detail = probe_relay(relay_home)
                 ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 865, in probe_relay_pool_health
    candidates = [p for p in (root / "auth.json", root / "codex-accounts.json") if p.is_file()]
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 865, in <listcomp>
    candidates = [p for p in (root / "auth.json", root / "codex-accounts.json") if p.is_file()]
                                                                                   ^^^^^^^^^^^
  File "C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\Lib\pathlib.py", line 1267, in is_file
    return S_ISREG(self.stat().st_mode)
                   ^^^^^^^^^^^
  File "C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\Lib\pathlib.py", line 1013, in stat
    return os.stat(self, follow_symlinks=follow_symlinks)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] 存取被拒。: 'C:\\Users\\user\\AppData\\Local\\HG-KSEOS\\opencodex-hermes\\auth.json'


======================================================================
FAIL: test_E11c_removal_voids_a_would_have_passed_attempt (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11c_removal_voids_a_would_have_passed_attempt)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\tests\test_lane_dispatch_ao_guard.py", line 437, in test_E11c_removal_voids_a_would_have_passed_attempt
    rc, r = self._case("remove")
            ^^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\tests\test_lane_dispatch_ao_guard.py", line 416, in _case
    self.assertTrue(json_out.is_file(), p.stdout + p.stderr)
AssertionError: False is not true : Traceback (most recent call last):
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 2275, in <module>
    raise SystemExit(main())
                     ^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 1751, in main
    verdict = identity_check(e, args.lane, lane_home, relay_home)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 901, in identity_check
    ok, detail = probe_relay(relay_home)
                 ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 865, in probe_relay_pool_health
    candidates = [p for p in (root / "auth.json", root / "codex-accounts.json") if p.is_file()]
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 865, in <listcomp>
    candidates = [p for p in (root / "auth.json", root / "codex-accounts.json") if p.is_file()]
                                                                                   ^^^^^^^^^^^
  File "C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\Lib\pathlib.py", line 1267, in is_file
    return S_ISREG(self.stat().st_mode)
                   ^^^^^^^^^^^
  File "C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\Lib\pathlib.py", line 1013, in stat
    return os.stat(self, follow_symlinks=follow_symlinks)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] 存取被拒。: 'C:\\Users\\user\\AppData\\Local\\HG-KSEOS\\opencodex-hermes\\auth.json'


======================================================================
FAIL: test_E11d_an_added_file_is_recorded_but_not_fatal (tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative.test_E11d_an_added_file_is_recorded_but_not_fatal)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\tests\test_lane_dispatch_ao_guard.py", line 443, in test_E11d_an_added_file_is_recorded_but_not_fatal
    rc, r = self._case("create", subject="dir")
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\tests\test_lane_dispatch_ao_guard.py", line 416, in _case
    self.assertTrue(json_out.is_file(), p.stdout + p.stderr)
AssertionError: False is not true : Traceback (most recent call last):
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 2275, in <module>
    raise SystemExit(main())
                     ^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 1751, in main
    verdict = identity_check(e, args.lane, lane_home, relay_home)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 901, in identity_check
    ok, detail = probe_relay(relay_home)
                 ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 865, in probe_relay_pool_health
    candidates = [p for p in (root / "auth.json", root / "codex-accounts.json") if p.is_file()]
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC9\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 865, in <listcomp>
    candidates = [p for p in (root / "auth.json", root / "codex-accounts.json") if p.is_file()]
                                                                                   ^^^^^^^^^^^
  File "C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\Lib\pathlib.py", line 1267, in is_file
    return S_ISREG(self.stat().st_mode)
                   ^^^^^^^^^^^
  File "C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\Lib\pathlib.py", line 1013, in stat
    return os.stat(self, follow_symlinks=follow_symlinks)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] 存取被拒。: 'C:\\Users\\user\\AppData\\Local\\HG-KSEOS\\opencodex-hermes\\auth.json'


----------------------------------------------------------------------
Ran 136 tests in 38.245s

FAILED (failures=4, errors=1)
```

Original ACC12 C2 dispatcher stderr (var/LANE-ENFORCEMENT-APPLY-20261015/lanes/VERIFY_SECURITY/ACC12/work/TEST_RESULTS/c2_observed.json:18), showing the first cause behind the parent missing-receipt error:

```text
WARN_LANE_CREDENTIAL_POSTURE_INCONCLUSIVE: the credential-posture detector could not reach a verdict (helper-only verdict (no child env asserted): helper_resolution_reset=PASS; helper_non_interactive=UNKNOWN); continuing -- the user-scope git default (L1) remains the structural control and this gate is the second layer. Inconclusive is NOT a pass.
WARN_LANE_CREDENTIAL_POSTURE_INCONCLUSIVE: credential posture could not be decided (helper-only verdict (no child env asserted): helper_resolution_reset=PASS; helper_non_interactive=UNKNOWN); CONTINUING (a detector fault must not become a lane outage; L1 remains the structural control; INCONCLUSIVE is NOT a pass).
Traceback (most recent call last):
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC12\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 2275, in <module>
    raise SystemExit(main())
                     ^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC12\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 2105, in main
    att = run_candidate(e, args, codex, lane_home, attempt_log_dir=log_dir, run_id=run_id)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-ENFORCEMENT-APPLY-20261015\lanes\VERIFY_SECURITY\ACC12\work\subject\hgk\scripts\hgk-lane-dispatch.py", line 1135, in run_candidate
    offset = usage_path.stat().st_size if usage_path.is_file() else 0
                                          ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\Lib\pathlib.py", line 1267, in is_file
    return S_ISREG(self.stat().st_mode)
                   ^^^^^^^^^^^
  File "C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\Lib\pathlib.py", line 1013, in stat
    return os.stat(self, follow_symlinks=follow_symlinks)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] 存取被拒。: 'C:\\Users\\user\\AppData\\Local\\HG-KSEOS\\opencodex-hermes\\usage.jsonl'

```

## Appendix E — fresh synthetic denied-metadata probe (not an OS sandbox reproduction)

`unittest.mock.patch.object(Path, "is_dir", return_value=True)` plus `patch.object(Path, "is_file", side_effect=PermissionError(13, "E11 synthetic metadata denial"))`, then call canonical `probe_relay_pool_health`. This tests exception propagation without reading any real credential or changing permissions.

```text
Traceback (most recent call last):
  File "C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\cache\scratch\e11-investigation-20261016\investigate.py", line 52, in <module>
    try: m.disp.probe_relay_pool_health(S/'synthetic-relay')
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\scripts\hgk-lane-dispatch.py", line 865, in probe_relay_pool_health
    candidates = [p for p in (root / "auth.json", root / "codex-accounts.json") if p.is_file()]
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Projects\Agent_Workspace\HG-KSEOS\scripts\hgk-lane-dispatch.py", line 865, in <listcomp>
    candidates = [p for p in (root / "auth.json", root / "codex-accounts.json") if p.is_file()]
                                                                                   ^^^^^^^^^^^
  File "C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\unittest\mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\unittest\mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\unittest\mock.py", line 1183, in _execute_mock_call
    raise effect
PermissionError: [Errno 13] E11 synthetic metadata denial

```

## Appendix F — repository write-boundary measurement

Compared each initial stat-readable repository file by size and nanosecond mtime after all test/probe execution and before this report was created. `.git` excluded. No claim is made for unreadable entries or concurrent changes after this measurement.

```json
{
  "checked": 574970,
  "baseline_scan_errors": 69595,
  "changed": []
}
```

## Appendix G — exact scratch investigation driver

The following executed driver records the environmental differential and test-only interception; its paths are external scratch paths, not additional repository artifacts. The earlier full-suite command is in Appendix A.

```python
import os, pathlib, sys, json, subprocess, io, unittest, traceback, importlib, datetime
ROOT=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
S=pathlib.Path(__file__).parent
os.chdir(ROOT)
os.environ['PYTHONDONTWRITEBYTECODE']='1'
for key in ('TMPDIR','TEMP','TMP'): os.environ[key]=str(S)
import tempfile
tempfile.tempdir=str(S)
sys.path.insert(0,str(ROOT))
OLD=pathlib.Path('C:/Users/user/AppData/Local/Temp/e11-investigation-20261016')
for name in ('original-suite.json','repo-before.json'):
    if (OLD/name).is_file(): (S/name).write_bytes((OLD/name).read_bytes())
IDS=[
 'tests.test_lane_dispatch_ao_guard.DeterministicGuardNegative',
 'tests.test_lane_dispatch_ao_guard.C2DispatchableConsumer.test_declared_not_dispatchable_arm_is_skipped_with_no_spawn',
 'tests.test_lane_dispatch_ao_guard.GateEndToEndRefusal.test_guard_root_that_does_not_resolve_is_refused',
]
cmd=[sys.executable,'-B','-m','unittest',*IDS,'-v']
env=dict(os.environ,LOCALAPPDATA=str(S/'empty-localappdata'))
(S/'empty-localappdata').mkdir(exist_ok=True)
p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace',env=env,timeout=180)
(S/'empty-precondition.json').write_text(json.dumps({'command':cmd,'env_overrides':{'LOCALAPPDATA':env['LOCALAPPDATA']},'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr},ensure_ascii=False,indent=2),encoding='utf-8')
print('EMPTY PRECONDITION',p.returncode,p.stderr)
# Run an in-memory test-only pool/ledger isolation experiment; source stays untouched.
os.environ['LOCALAPPDATA']=str(S/'empty-localappdata')
m=importlib.import_module('tests.test_lane_dispatch_ao_guard')
pool=m._hermetic_verify_pool(S)
real_run=subprocess.run
calls=[]
def isolated_run(args,*a,**kw):
    args=list(args)
    if str(ROOT/'scripts'/'hgk-lane-dispatch.py') in args:
        e=dict(kw.get('env') or os.environ)
        if '--guard-subject' in args and '--force-rank' in args:
            args += ['--pool',str(pool)]
            e['HGK_STUB_USAGE_LINE']=json.dumps({'provider':'opencode-go','model':'deepseek-v4.1-flash','status':200})
        if '--usage' not in args:
            args += ['--usage',str(S/('isolated-usage-'+str(len(calls))+'.jsonl'))]
        kw['env']=e
        calls.append(args)
    return real_run(args,*a,**kw)
subprocess.run=isolated_run
buf=io.StringIO()
suite=unittest.TestLoader().loadTestsFromNames(IDS)
res=unittest.TextTestRunner(stream=buf,verbosity=2).run(suite)
subprocess.run=real_run
(S/'isolated-control.json').write_text(json.dumps({'description':'In-memory subprocess argument interception; E11 gets existing hermetic pool helper and matching stub usage; C2 gets scratch --usage; no production code or gate changed','commands':calls,'testsRun':res.testsRun,'failures':len(res.failures),'errors':len(res.errors),'stderr':buf.getvalue()},ensure_ascii=False,indent=2),encoding='utf-8')
print('ISOLATED CONTROL',buf.getvalue())
# A bounded negative probe for the uncaught metadata exception, no real credential access.
from unittest.mock import patch
with patch.object(pathlib.Path,'is_dir',return_value=True), patch.object(pathlib.Path,'is_file',side_effect=PermissionError(13,'E11 synthetic metadata denial')):
    try: m.disp.probe_relay_pool_health(S/'synthetic-relay')
    except Exception:
        t=traceback.format_exc()
        (S/'synthetic-metadata-denial.txt').write_text(t,encoding='utf-8')
        print('SYNTHETIC METADATA DENIAL (NOT OS SANDBOX REPRODUCTION)',t)
print('DONE',datetime.datetime.now().astimezone().isoformat())

```
