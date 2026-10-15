# R7-0 — how an external acceptor re-verifies this packet

Everything below is re-derivable from the repository plus the recorded head. Nothing here requires trusting the
mission's own prose. Claim ceiling: **LOCAL / candidate-only**.

## 1. Identify the artifact
- Repo `shw097-team/Fabric`, branch `evidence/cnv-pipd-ls-sp-20261015-r7`, prefix
  `EVIDENCE/CNV-PIPD-LS-SP-20261015-R7/`.
- The head sha is **not** asserted inside the packet: it is bound by `R7R7_POST_COMMIT_READBACK.json`
  (`R7_POST_COMMIT_READBACK.json`) and by the pull-request receipt, both held outside the commit, and by the PR
  comment. Compare the PR head with those values.

## 2. Publication set integrity (minutes, no special tooling)
1. `GET /repos/shw097-team/Fabric/git/trees/{head}?recursive=1`, take every blob under the R7 prefix.
2. Download `PACKET_MANIFEST.json` and compare `tracked_inventory` with that set: the difference must be empty,
   and `file_count - tracked_file_count` must equal `len(local_only_excluded)`.
3. For any subset of paths, recompute `sha1("blob <len>\0" + bytes)` from the file you downloaded and compare it
   with the tree entry. The recorded result at the approved head was **0 mismatches**.
4. Confirm the previously merged prefix `EVIDENCE/CNV-PIPD-LS-SP-20261015/` still has **581 blobs** and that its
   `PACKET_MANIFEST.json` sha256 is still
   `27ba42f7cb32d9f490d8897ef0205b0b70cd13bb2b7bc6344e717e5bffbd118b`.
   `/repos/shw097-team/Fabric/commits/main` should still read `b8ff8104…`.

## 3. Scope and secret hygiene
`M2_TRUSTED_SCOPE_SECRETS_R7.json` records the scan: tool id/version, blobs and bytes scanned, a scan digest,
out-of-prefix/traversal counts (expected 0), symlinks (0), executable-bit blobs, hard-pattern findings (expected 0),
soft candidates with a per-item rationalisation, and an exact-substring check that the operator's credential value
appears **0 times** in the packet (the value itself is never printed or stored). Re-run `m2_scan.py` yourself if you
want a second opinion — it reads git objects only and executes nothing from the packet.

## 4. The R7-0 engineering claim
Read in this order:
1. `R7_VALIDATOR_HARDENING.md` — the defect class and the three predicates.
2. `R7_VALIDATOR_DIFF.patch` — the whole change (3 product files). Check for yourself that no existing predicate
   was deleted or weakened: the diff removes 6 lines, all of them signature/return lines.
3. `R7_MUTATIONS_18_RERUN.json` — maker result: `M04/M06/M16` now `REJECT`, `detected 10`, `not_detected 0`,
   `not_run 8` (unchanged).
4. `R7_CHECKER/R7_CHECKER_VERDICT.json` + `R7_CHECKER_RECEIPT.md` — the independent checker's own re-run, its
   per-item `CONFIRMED`/`CHALLENGED`/`UNVERIFIABLE` rows, and any disagreement. **Prefer the checker's raw output
   over the maker's JSON**; where they differ, the difference is the finding.
5. `RAW/` — raw stdout/stderr for every command either lane ran.

## 5. The checker isolation claim (EIA-R6-03)
`RAW/isolation_selftest.stdout.txt` and `RAW/r7_isolation.stdout.txt` show the fixture: first a write **succeeds**
(before), then an OS-level deny ACE is applied, then the same write is **denied**, then the ACE is removed and the
ACL restored. Read the raw files; a claim of `ENFORCED`/`DENIED` without those two phases would be unsupported.
If a future environment cannot enforce the ACL, the correct record is `ACL_UNENFORCEABLE` — not a pass.

## 6. Governance and what is still open
- Admission: the R7-0 change set was admitted as HGK project `CNV-R7-VALIDATOR-HARDEN-R7VH`
  (`HGK_TYPED_ADMISSION_R7.json`); the R6R7 round's admission is in the R6 archive.
- Adjudication: `FAR/FAR-20261015-010-*/` (FAR run) ranks the open items and explains why the denominator work
  (221 cases, gates, AUD) is sequenced behind an applicability sign-off, and why the human gates stay human.
- Still open and deliberately untouched: Fresh G1, DOC-05, AO/Release, 221 cases, `G-A..G-H`, AUD-24, the
  18 PI/10 PD/64+129 trace denominator, the five effect planes, source #6 adjudication, the 20 KP `*-R04`
  polarity defect.
- Tooling defects observed while doing this round are recorded with owners in `R7_TOOLING_FINDINGS.json`.
