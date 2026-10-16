# Control-plane admission receipt - credential broker standing install

Records the ACTUAL governance route taken. It exists because `INSTALL_MANIFEST.json` labelled its
`candidate_admission_script` as a *candidate*; the route actually used was the minimal one, and an
installed directory must not point at a round path that was never created.

## Admission

| field | value |
|---|---|
| authority | HG-KSEOS, sole system governance / normative control plane |
| project | `HGK-CHU-20261009` (control-plane hardening unit) |
| requirement | `REQ-HGK-CREDBROKER-001` - FROZEN |
| taskspec / workorder | `TS-req-hgk-credbroker-001` / `WO-TS-req-hgk-credbroker-001` |
| API | typed `SharedSpine` / `ProjectLifecycleController.admit_requirement` - no raw SQL |
| project state | before `EXECUTING`, after `EXECUTING` (unchanged) |
| errors | 0 |
| route | A (minimal): admit into an existing admissible control-plane project rather than create a new lifecycle |
| why not a product round | `FAR-PIPD-R8-DISPATCH-004` section 4: an edit to HG-KSEOS control-plane tooling needs its own admission and must not ride along inside a PIPD round |

## Install

| field | value |
|---|---|
| target | `HG-KSEOS/scripts/cred/` |
| mode | byte-preserving copy, NOT reconstruction from rendered text |
| line endings | `* -text` via `.gitattributes`, so a fresh clone reproduces the pinned bytes (an earlier omission would have silently changed every pin) |
| activation | **NONE.** A search of `config/` and `scripts/*.py` / `*.ps1` for `scripts/cred`, `cred_broker`, `cred_preflight` returns **0** references outside `scripts/cred/` itself. |

## Acceptance criteria, GRADED BY EVIDENCE CLASS

This table was previously written as a flat list of PASSes. An independent checker returned FAIL on
it, on the honest ground that several rows assert things the checker could not establish. The rows are
therefore separated by what KIND of evidence stands behind each one. Rows 3, 5 and 6 are explicitly
NOT independently established and must not be cited as if they were.

| # | criterion | evidence class | measured |
|---|---|---|---|
| 1 | modules present under `scripts/cred/` with the pinned sha256 | **INDEPENDENTLY VERIFIABLE** | PASS - every path-valued target resolves; a cross-model checker recomputed the hashes itself |
| 2 | `verify_offline.py` returns `PASS_OFFLINE_T5_UNPROVEN` (or `PASS`) on this host | **INDEPENDENTLY VERIFIABLE** | PASS - returns `PASS_OFFLINE_T5_UNPROVEN`; T5 is reported SKIP, not PASS |
| 3 | `selftest.py` 5/5 on DUMMY credentials | **HISTORICAL - NOT RE-PRODUCED** | run in R9 on a networked host. NOT re-run here. Do not read this row as a fresh 5-of-5. |
| 4 | no config references the installed path (non-activated) | **INDEPENDENTLY VERIFIABLE** | PASS - 0 hits; the same search was re-run by the checker |
| 5 | no secret value in any artefact | **SELF-REPORTED - NOT INDEPENDENTLY ESTABLISHED** | no credential-value search was performed by the checker. Read it as: the producing process read only metadata. It is NOT a repo-wide proof. |
| 6 | typed admission `REQ-HGK-CREDBROKER-001` into `HGK-CHU-20261009` | **RECORDED - NOT INDEPENDENTLY QUERIED** | evidence is `admission/control-plane/hgk_cred_admission.json` in the R10 round. No independent query of the governance store was made. |

Only rows 1, 2 and 4 are of the kind an outside party can re-establish from the artefacts alone.

## Defects this artefact has had, and how they were found

Both were found by independent verification, not by self-review:

- **Dangling pinned target (first).** `governance.candidate_admission_script` named a Route-B round
  that was never created. *"A single fix to a class of defect is not a fix to the class."*
- **Dangling pinned target (second).** `control_plane_admission_file.target` pointed at the same
  never-created round, and was only found when the check was RE-RUN after the first fix. A re-run
  without a change would not have found it; a fix without a re-run would have shipped it.

## What is NOT done

- The broker is **not wired into any lane**. Activating it (routing a write lane through it) is a
  separate, later, separately-admitted change.
- The GitHub App setup is human: registering the App, downloading its private key, and installing it
  are **UI-only** - GitHub exposes no API for any of the three. Until then the PAT bridge is used.
- Nothing here rotates a credential. GitHub exposes no API to read a PAT own expiry or renew it.
- No full-tree HG-KSEOS integrity claim is made: a snapshot attempt was blocked because
  `var/far-lane-sod-003/evidence/relay-supervisor.cooldown.json.lock` denied read access.

