# WS-H RECEIPT — round self-check harness repair (tooling finding TF-10)

Round `CNV-PIPD-LS-SP-20261015` / ChangeSet `R8-0` · HGK project `CNV-R8-SKILL-SLIM-EIA-CLOSURE`
Producer: PLAN-plane sub-agent (`gpt-6.1-sol`, delegation `deleg_c746bb64` task 2)
Final write performed by the in-Hermes orchestrator after the owner's explicit authorization (2026-10-16).
The sub-agent's own write of this receipt was refused by the pre-tool guard; the run outputs and file bytes below
were verified by the orchestrator on disk.

## 1. Artifacts (bytes + sha256, measured on disk)
| path | bytes | sha256 |
|---|---|---|
| `WS_H/round_selfcheck_r8.py` | 18,135 | `4d3f8ad0418a2991…` |
| `WS_H/SELFCHECK_R8_OUTPUT.txt` | 8,802 | `ff86662e424d8a57…` |
| `WS_H/test_tf10.py` | 2,911 | `b1b303daeaa7354a…` |

Origin of the defect: the R7 harness (`…-R7/selfcheck/round_selfcheck.py`) hardcoded packet expectations. It passed at the
212-blob state and then reported `1=PASS 2=FAIL 3=FAIL 4=PASS 5=PASS 6=PASS` → OVERALL FAIL at 227 blobs, because checks 2
and 3 compared the live packet against stale constants. **Refusing to pass on a stale expectation was correct behaviour**;
the repair is to derive the expectation, not to drop the assertion.

## 2. What the repair changes
Expectations are now resolved at run time from: the resolved HEAD, the Git blob inventory, the committed
`PACKET_MANIFEST.json`, runtime prefix discovery, and baseline evidence. All six check families are retained, and no
assertion was deleted or loosened to reach a green result.

## 3. Run results (reproduced output in `SELFCHECK_R8_OUTPUT.txt`)
- Current packet head `04a1e118dd6616ccb6b2e68b68544fd5af4271ae` → **306 blobs**; local-byte and manifest-set
  reconciliation are exact; **checks 2 and 3 now PASS** (the TF-10 symptom is cleared).
- Normal-run verdict: **`1=FAIL 2=PASS 3=PASS 4=FAIL 5=PASS 6=PASS`**.
  - check 1 FAILs on a stale historical readback in the harness's cached evidence, not on the live packet;
  - check 4's local archive/scope assertions pass; its live-main verification is unavailable in the offline mode.
- Negative controls behave: empty inventory and equal-count/wrong-set cases fail correctly; a deliberately wrong prefix
  exits 1 (`SNAPSHOT FAIL: ValueError wrong/unsafe prefix`).
- `test_tf10.py`: **7 regression tests pass** (including a deliberate "legacy-red" reproduction that shows the old
  hardcoded expectation failing while the live-manifest expectation passes).

## 4. Honest limits (unchanged by the repair)
Offline mode cannot verify the remote branch, the remote `main`, provider/model attestation, upstream CI, or any
acceptance authority. Those remain **UNVERIFIED** and are not implied by any PASS above. The harness also does not
re-check the guarded subject's ACL state; that belongs to WS-C.

## 5. Non-claims
No network or Git state was changed; no packet repair was performed; no acceptance, Gate PASS or approval is claimed.
Claim ceiling **LOCAL / candidate-only**. Residual tooling item: the two FAILing check families should be re-pointed at
remote truth in a networked round — recorded, not worked around.
