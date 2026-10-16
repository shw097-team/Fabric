# WS5 SELFCHECK RECEIPT — R7-0 harness run

Round: R7-0 (mission CNV-PIPD-LS-SP-20261015, ChangeSet R7-0-VALIDATOR-AND-CHECKER-ISOLATION)
Job: build + run the automated selfcheck/self-repair harness for the R7-0 round.
Claim ceiling of this receipt and of the harness output: **LOCAL / candidate-only**.
No acceptance, no approval, no Gate PASS, no merge authorisation, no production effect is claimed.
Unverifiable claims stay unverifiable and were not upgraded.

## What was run

Commands (as executed from `selfcheck/` in the handover dir):

```
python round_selfcheck.py --dry-run       # self-verification only: guards, no API calls
python round_selfcheck.py                 # full live run (bash: > SELFCHECK_OUTPUT.txt)
```

Python used: `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`
(Windows 11; I/O encoding forced to UTF-8.)

Confirmation command: both runs exited rc=0 on their real execution (not inferred, remaining
explanation none needed). The full live run's raw stdout is preserved exactly at
`selfcheck/SELFCHECK_OUTPUT.txt`.

## Checks — status

| #  | check                                                              | status |
|----|--------------------------------------------------------------------|--------|
| 1  | local HEAD == remote branch == local readback's recorded head      | PASS   |
| 2  | blob inventory under R7 prefix: local files exist, blob ids match  | PASS   |
| 3  | packet manifest reconciliation: tracked==blobs; file−tracked== excl| PASS   |
| 4  | merged archive untouched: main sha, 581 frozen blobs, sha256 match | PASS   |
| 5  | M2 record: verdict PASS, scope violations 0, hard secrets 0        | PASS   |
| 6  | checker attempt-3 verdict parse: schema /3, overall in allow-set   | PASS   |
|    | **overall**                                                        | **PASS** |

No check is UNVERIFIABLE. Nothing was left undetermined from the six required checks.

No repairs were applied at any level (repair mode remains armed but found no residual
failures; the run's recorded actions list is empty and confirms no writes outside the
handover dir).

Report as to how each check's honesty gate held: the run's raw stdout shows
`claim_ceiling: LOCAL / candidate-only` in the very first line and in the verdict block;
the harness refuses (in-process, offline probe confirmed) any write outside the handover
dir and any git write/transport verb, and never printed, logged, or embedded the token.

## What the harness refuses (verified offline)

- attempt to `guarded_write()` outside `.../CNV-PIPD-LS-SP-20261015-R7/` → refused;
- `git push` / any git write verb → refused by the command gate (`-C <path>` verb parsing fixed);
- `git rev-parse` and other read-only git verbs → allowed;
- the merged archive `EVIDENCE/CNV-PIPD-LS-SP-20261015/**` is never written.

## What I could not verify

- The checker's provider/model attestation (opencode-go/glm-5.3-flash on the VERIFY lane)
  stays UNVERIFIABLE — the M2/[6] checks cover the record's content, not the serving lane.
- Upstream CI status of the merged packet — not checkable from this manifest.
- The 221 acceptance cases and any Gate PASS — not claimed, not run, ceiling intact.
- Attempt-1 (voided) checker evidence is excluded from what [6] reads (it reads attempt-3 only).

## Post-conditions

- Nothing was written outside the handover dir; the two R7 runtime records used by the
  checks (`R7_POST_COMMIT_READBACK.json`, `R7_PUBLICATION_VERIFICATION.json`) are
  read-only here — no repair rewrite occurred this run (no residual failures).
- `EVIDENCE/CNV-PIPD-LS-SP-20261015/**` byte-bound at main sha b8ff8104… with 581 blobs and
  manifest sha256 27ba42f7... — unchanged (verified live in check 4).
