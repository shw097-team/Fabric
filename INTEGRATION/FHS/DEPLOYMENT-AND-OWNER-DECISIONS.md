# FHS Engineering Entry — deployment record and owner decisions

**Record ID:** `FHS-ENTRY-DECISIONS-2026-11-02-r1`
**Scope:** what was deployed, under whose authorization, with which limits. Facts only; no signature is
invented here.

**Status of this record:** `REQUESTER_AUTHORIZATION_RECORDED / ORIGINAL_OWNER_SIGNATURE_UNVERIFIED`

The authorization in force is the commissioning instruction from the requester (the repository owner
account operating the local execution environment), carried by two task documents:

- `FHS-ENTRY-HERMES-RESUME-2026-11-02-r2` — resume/rework instruction (MODE_A recommendation, the
  substitute procedure, and the G3/G4 conditions).
- `FHS-ENTRY-HERMES-FOLLOWUP-2026-11-02-r3` — the repair instruction of the previous round.
- `FHS-ENTRY-HERMES-L1-CLOSEOUT-2026-11-02-r4` — this round's instruction, which carries the owner's L1
  decision recorded in §7.

No separate signed Mirror-Owner or Security-Owner artefact exists. The resume instruction itself states
that it does not substitute for owner signing. This record therefore does **not** claim a native
signature, a native receipt, or an independent checker verdict.

## 1. What is deployed (measured)

| repository | PR | merge commit on `main` | changed paths | readback |
|---|---|---|---|---|
| Fabric (this repository) | [#20](https://github.com/shw097-team/Fabric/pull/20) | `22e3432d21e42c2c8410323e0008325d2eb09f2d` | 10 files, +428/−0 | `GET /contents/INTEGRATION/FHS/README.md?ref=main` → 200 |
| SBL | [#16](https://github.com/shw097-team/SBL/pull/16) | `e166d67cf4ae7ed318df11292e906e324dc4fc9e` | `README.md` +2/−0 | link at `README.md` |
| HG-KSEOS | [#9](https://github.com/shw097-team/HG-KSEOS/pull/9) | `0143b50331f7fef007a5921bb743e61f59b0a7bd` | `README.md` +2/−0 | link at `README.md` (repository has no CI configured) |
| PIPD-LS-SP | [#23](https://github.com/shw097-team/PIPD-LS-SP/pull/23) | `8a0c85225323a7e7c61bfd6aa99e4cd3dc87419a` | `README.md` +2/−0 | link at `README.md` |

Fabric PR #20 CI: `fhs-nav-static` success on the PR head (`11014672bc12e32819cc7adb2911559d76105d06`)
and on the `main` push. Three-repository links were merged as separate README-only changes, each read
back after merge.

## 2. Mirror decision — `MODE_A_EXCLUDE_NAV_SUBTREE`

- `INTEGRATION/FHS/` exists in the GitHub tree and is version-controlled, but it **adds no fifth Mirror
  Subject**: the four subjects stay four, and the entry takes no canonical or acceptance standing.
- `INTEGRATION/MANIFEST.json` is **unchanged** (same blob before and after the merge). Subjects stay at
  four; all ten readiness artefacts remain; no excluded path was touched; the tree difference is
  additive only, with no deletions.
- The repository's own records state that no Mirror Builder is approved (`KNOWN-FINDINGS.md` K-05,
  `APPROVAL-LIST-PROPOSAL.md` O-02, `MANIFEST.pending`). No Builder was created for this change, so the
  Mirror dry-run is honestly recorded as **`MIRROR_DRYRUN_NOT_RUN`**.
- Substitute procedure actually used: the requester-reviewed change-set plus the tree / readiness /
  exception diff measurements above. This is a documented substitute, not a dry-run result.

## 3. Security checks actually executed (not a waiver)

| tool | version / licence | provenance | scope | result |
|---|---|---|---|---|
| `actionlint` | 1.7.12 / MIT | PyPI `actionlint-py` 1.7.12.25 (sdist sha256 `83f83be4…`) in an ephemeral environment | `.github/workflows/fhs-entry-check.yml` | exit 0, no diagnostics |
| `zizmor` | 1.31.1 / MIT | PyPI wheel sha256 `3b35b393…` | same file | default persona: no findings; pedantic/auditor: one low `concurrency-limits` (resource hygiene, not security), left unchanged by design |
| `gitleaks` | 8.30.1 / MIT | official release zip, sha256 `d29144de…` matching the published checksums file | the change commit only | 1 commit scanned, no leaks, exit 0 |

`premerge_security.sh` remains **`42 / NOT_RUN`** (the approved toolchain reference is absent). It is not
reported as PASS and is not replaced by the three executions above.

## 4. Owner decisions that remain open

These were open before this change and are **not** closed by it:

- Mirror approval-list freeze and Builder authorization (K-05 / O-02).
- Licence choice and bulk-binary disposition.
- Subject baseline re-certification and external acceptance.
- Full-history secret findings in this repository — see §5.

The navigation deployment does not resolve, widen or batch any of them.

## 5. Known limits carried forward

- **Historical secret scanning.** `gitleaks` 8.30.1 (official release, archive sha256 verified against the
  project's published checksums) reports, across all refs, **264 commits and 66 findings over 20 distinct
  values**; `main` alone reports **5**. All 66 are classified: 60 are false positives or non-secret values
  (digests, git shas, prose/log text, documentation placeholders, a documented .NET `PublicKeyToken`, a
  unit-test fixture) and 6 are **unconfirmed**, held as `SECRET_REMEDIATION_OWNER_HOLD`. No value, fragment
  or raw report is published, no leaked credential was tested or used, and none of the navigation paths
  carries a finding. The sanitized triage is the comment record on
  [PR #20](https://github.com/shw097-team/Fabric/pull/20#issuecomment-6577176362). History rewriting is a
  separate owner decision and is refused by default.
- **Branch protection.** Measured on all four repositories: `rulesets` returns 0 rulesets and
  `branches/main` reports `protection.enabled=false`; `branches/main/protection` returns 403 because the
  executing credential holds no repository-administration scope (`PATCH /repos/{owner}/{repo}` →
  `403 Resource not accessible by personal access token`). The state is recorded as
  **`PROTECTION_ADMIN_HOLD`**, with the minimal gap list in the
  [same PR #20 record](https://github.com/shw097-team/Fabric/pull/20#issuecomment-6577177056). Nothing was
  changed; this is not a claim that the branches are protected.
- **Navigation is not ratification.** `source_state` stays `PROPOSED_NOT_OWNER_RATIFIED`; the
  `hermes_runtime` route still has no resolvable public host source.

## 6. Claim ceiling and rollback

Deployed claim: `FABRIC_FHS_NAV_DEPLOYED` + `FOUR_REPO_ENTRY_LINKED`. Not claimed: native end-to-end
acceptance, policy effectiveness, HGK admission, PIPD cutover, PIPD archival, independent-checker pass,
or release.

Rollback is a revert of the recorded merge commits — Fabric `22e3432d…`, SBL `e166d67c…`, HG-KSEOS
`0143b503…`, PIPD `8a0c8522…` — each independent. If the entry degrades, each repository's original
README/AGENTS and domain Source Reader remain usable; only writes that depend on this route are held.

## 7. L1 assisted-navigation use — `NAV_ASSISTED_USE_APPROVED`

| field | value |
|---|---|
| decision ID | `FHS-NAV-ASSISTED-USE-2026-11-02` |
| decision label | **`NAV_ASSISTED_USE_APPROVED`** |
| decided by | the requester, acting as OWNER, in this round's instruction `FHS-ENTRY-HERMES-L1-CLOSEOUT-2026-11-02-r4` §0 |
| recorded | 2026-11-02 |
| scope | use of this navigation entry, not any original domain's authority |

**Status line:** `REQUESTER_OWNER_L1_AUTHORIZATION_RECORDED / ORIGINAL_OWNER_SIGNATURE_UNVERIFIED`.
The owner authorisation is real and explicit; no independent Mirror, Security or Domain Owner signature
exists, and none is invented here.

**What L1 approves.** Hermes and other engineering AI may use this entry, when a task spans repositories,
as a **read-only** starting point for: proposing a task class from the six declared routes; locating the
original public source pointer; identifying which original domains and consumers are affected; and
starting a candidate plan or draft. Ordinary single-repository tasks continue to go straight to their own
domain and do not need this entry.

**Conditions.** A static route result is a **suggestion**. The original Source, Owner, Consumer, current
HEAD and Host state must be confirmed at the original domain reader before any effect. If the original
domain disagrees, information is missing, or the task class is unknown, the outcome is
`HOLD_AFFECTED_WRITE_ONLY`: the affected write is held while reads and drafts that existing permission
already allows continue.

**What L1 does not approve.** It is not a licence to write or merge any other repository on the strength
of this entry; not a WorkOrder, Permit or Grant; not Policy authority; not a Compiler or Checker
invocation; and not a basis for declaring HGK Admission, Hermes Host Loaded, PIPD U04 Cutover, Native
Effect or Release. The write authority for this very pull request comes from the engineering commission
and the repository's existing GitHub permissions — **not** from L1.

**Two claims that must not be merged.** `NAV_ASSISTED_USE_APPROVED` is an authorization decision and is
recorded here. `HOST_ACTUALLY_LOADED` is `NOT_OBSERVED`: no host profile, PID, ProfileSHA, loaded or
invoked readback exists in this record, and the L1 approval does not imply one.

**What this is not.** It does not add a state or permission to the `FHS-NAV/v1` ABI: `source_state` stays
`PROPOSED_NOT_OWNER_RATIFIED`, the validator still reports `original_reader_verified=false` and
`owner_ratification_verified=false`, and no route, field, registrar, registry or queue is added.

**Delivery record.** Carried by Fabric PR [#24](https://github.com/shw097-team/Fabric/pull/24); that pull
request's thread holds the merge commit and the post-merge readback of `INTEGRATION/FHS/README.md` and this
file on `main`.

**Rollback.** Revert the merge commit that adds this section. L1 is a decision, revocable by the same owner
through a later record; reverting it changes no route, no route data and no original domain.
