# R9-0 FAR EXPERIMENT: minimal scratch repair

**Claim ceiling: LOCAL / candidate-only; not acceptance.**

## Outcome
- Before: FAIL; after: PASS.
- Exact per-check verdicts (verbatim strings from raw harness JSON):

| Check | Before | After |
|---|---|---|
| C1_capacity | PASS | PASS |
| C2_loader_shape | PASS | PASS |
| C3_link_intake | PASS | PASS |
| C4_lossless | PASS | PASS |
| C5_controls | PASS | PASS |
| C6_reference_coverage | FAIL | PASS |

## Minimal repair set

- `references/lane-conformance-gate.md`: source `C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\skills\software-development\hgk-governed-execution\references\lane-conformance-gate.md`; 3299 bytes; SHA256 `77e8b77164c0f0d38a607c582d95e33b2a8eb4334a47d700e71f7ffbe8468119`.
  Original bytes recovered at 1 exact whole-file/embedded locations (full list in measurements JSON).
- `references/step-verify-only-lane.md`: source `C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\skills\software-development\hgk-governed-execution\references\step-verify-only-lane.md`; 7994 bytes; SHA256 `d8e7f1a561551fce97b9fb341f1c9f83ac9a02d026848a27fd4df1afd0a5aac8`.
  Original bytes recovered at 1 exact whole-file/embedded locations (full list in measurements JSON).

## Measurements and interpretation
- Main file: 105116 live bytes -> 21026 candidate/repaired bytes; unchanged by repair; below 100,000.
- Repair adds 5264 net bytes; only the listed two paths change.
- C6 before: {"verdict": "FAIL", "live_references": 112, "byte_identical": 87, "absorbed_but_present_verbatim": 23, "lost": 2, "lost_rows": [{"ref": "lane-conformance-gate.md", "live_bytes": 3299, "live_sha256": "77e8b77164c0f0d3", "candidate_state": "absent"}, {"ref": "step-verify-only-lane.md", "live_bytes": 7994, "live_sha256": "d8e7f1a561551fce", "candidate_state": "rewritten/6029B"}], "note": "a reference may be merged into a topic file, but its bytes must then appear verbatim in the corpus; deliberate deletions are not allowed by this gate"}
- C6 after: {"verdict": "PASS", "live_references": 112, "byte_identical": 89, "absorbed_but_present_verbatim": 23, "lost": 0, "lost_rows": [], "note": "a reference may be merged into a topic file, but its bytes must then appear verbatim in the corpus; deliberate deletions are not allowed by this gate"}
- No C1-C6 failures remain if overall above is PASS. Reference soft-cap warning remains; not a hard gate.
- Losslessness: all live instructional reference files now survive byte-identical or fully embedded; C4 also finds no lost main-file lines >40 bytes. These are the harness-defined properties, not a stronger whole-main-byte reconstruction proof.
- Full path/size/SHA256 manifests and all file differences (including caches) are in repair_measurements.json.
- Both originals are confirmed recoverable from the live tree. No additional exact whole-file or embedded match was found among 1,180 readable files searched in the two supplied archival roots; this is not proof that no inaccessible backup exists.
- Scan limitations: access denied at `candidates/consumer/pytest-tmp` and `candidates/consumer/_pytest_tmp`; broken `qualification/probe-junction`. The first enumeration stopped on that broken junction; the successful retry used bounded os.walk with per-path error recording. These do not block recovery from live or either harness run.
- Source candidate and live manifests were rehashed and unchanged after experiment.
- Raw harness_before.json and harness_after.json are retained, with invocation/stdout/stderr evidence.

## Instrument caveat
Raw subject_live field is evaluated before check() applies --live, so it incorrectly names AVR. The explicit --live arguments and HGK identity/live byte count demonstrate effective HGK binding. Instrument unchanged.

## Guarded apply assessment
- The repaired candidate clears the reproduced C6 blocker and passes all six local checks; it is justified as the candidate for a separately authorized guarded-apply procedure, not as permission to apply now.
- Before any actual apply: rebind/re-hash live inputs, preserve a pre-image, exclude bytecode caches from publication, exercise rollback, and rerun the gate on the landed tree. Independent acceptance remains separate.

## NON-CLAIMS
- No canonical/live tree was modified, and no apply, promotion, release or acceptance occurred.
- This worker performs a local scratch experiment, not an independent acceptance lane.
- No network or git write command was used. Explicit task writes are confined to ws3; tool-runtime bookkeeping is outside this experiment's control.
- Existing harness C5 implementation is limited: some controls test primitive predicates rather than full end-to-end negative fixtures. A C5 PASS is reported as the instrument returned it, not as broader adversarial validation.
- No claim that reference count is below its soft cap; no claim that cache cleanup was performed.
- Archival byte search is bounded to the supplied roots; whole-file or embedded exact matches are listed, not an exhaustive whole-disk search.
