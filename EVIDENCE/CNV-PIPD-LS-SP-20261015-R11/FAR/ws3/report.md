# W3 Integrity Audit - CNV-PIPD-LS-SP-20261015-R11 / FAR / ws3
Produced 2026-10-16 (Taipei local). READ-ONLY posture throughout; nothing written outside `FAR/ws3/`.
Claim ceiling LOCAL / candidate-only - no acceptance, no Gate PASS, no owner verdict, no release here.

## 1. Key locators
| # | Locator | Verdict | Detail |
|---|---|---|---|
| L01 | `attachments/Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md` | OK | 2,689,181 bytes; sha256 `96d9d564286743e17550ccef15b9952347901eb77168f930376938893cff9c3f` |
| L02 | `attachments/Fabric_Convergence_External_Independent_Acceptance_Report_20261015.md` | OK | 33,616 bytes; sha256 `10caf4dbdb1993cd46ff2c50394dd01dfd5f34d635816f95e3d2e5ab6c566206` |
| L03 | `HG-KSEOS/AGENTS.md` | OK | 14,055 bytes; sha256 `7f7246d34be112bb465b48dadaef6163e466e16e5e705fc58acee04b3809a613` |
| L04 | `HG-KSEOS/var/shared-spine/hg-kseos.db` | OK | 823,435,264 bytes (785.2 MB); **33 tables** in `sqlite_master` (opened `mode=ro`; rows not dumped) |
| L05 | `HG-KSEOS/config/lane-routing-registry.yaml` | OK | 47,224 bytes; sha256 `02481992df124ca4f83b655b4583fc2053ecebbbb3125702ab28e39d0c35ea70`; in-file `epoch:` now reads **22** (see advisory in section 5) |
| L06 | `_handover/CNV-PIPD-LS-SP-20261015-R10/` | OK | root directory present; 61 files measured in the walk (see integrity_audit.json) |
| L07 | R10 artifacts named in `HANDOVER_R10.md` | OK | all named artifacts exist and hash out (see `integrity_audit.json`); the `-R9/...` prefixed `R9_LEDGER.json` + `dispatch_r9.py` pointers resolve from the `-R9` packet |

## 2. Dangling pointers in `hgk-governed-execution/SKILL.md` + `references/`

Method: autopsied every path-shaped token in the SKILL.md and in every file under the skill's
`references/` and `scripts/`. For each, tested readability as (a) a file in the skill's own tree,
(b) a suffix match into the skill tree, or (c) present anywhere on the reachable disk
(workspace root + Hermes home + all handover packets). Illustrative fragments (URL recipes,
`...install.ps1`, curl payload names, `SKCV-POINTER` preambles, variable names like `FAR_x.json`,
`<script.py>`, `test_x.py`) were excluded as non-locators.

**Definite dangling: 12. Planned-but-unbuilt: 3.** Full locators in `dangling_pointers.tsv`.

| Skill file | Line | Missing reference |
|---|---|---|
| SKILL.md | 66, 71 | `entry_map.json` |
| cross-session-integrity.md | 5 | `cross-session-upgrade-reconciliation.md`, `parallel-session-upgrade-integrity.md` |
| external-evidence-closure.md | 95 | `MASTER_REF.yaml` |
| external-rereview-normalization-rebind.md | 152 | `FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json` |
| fda-desktop-automation-cua.md | 89, 133, 192 | `FDA_C5_LEASE_CONCURRENCY_RECEIPT.json`, `FDA_F01_LIVE_FIXTURE_RECEIPT.json`, `FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json` |
| governance-knowledge-map.md | 75 | `stage/RP002-STAGE-HGK/KG1/KG1_NAMESPACE_MODEL.json` |
| hgk-spine-knowledge-facilities.md | 80 | `A0_KNOWLEDGE_EXTENSION_EVIDENCE.yaml` |
| hgk-ssot-authority-determination.md | 105 | `versions.lock.yaml` |
| oversized-skill-handling-route.md + oversized-skill-split-notes.md | 13, 19, 38 | `skill_split.py` (documented as 'not present, to be built at runtime' - planned work, not a locator defect) |

Note: SKILL.md pins `entry_map.json` as the byte-provenance map + mandatory STOP control for
`ERR_ENTRY_MAP_*`; it is absent from the skill tree and from every reachable root.
`skill_split.py` rows are documented in-line as planned/optional build targets, so they are not
counted as dangling but ARE recorded here for completeness.

## 3. Protected subject `R6_DELIVERY`
- **File count: 300** (matches the 300-file claim exactly)
- **Newest mtime: 2026-10-15T23:30:47.272310** - no post-2026-10-15 writes observed; the packet is intact.
- Total bytes: 1,102,562. Nothing under the packet was written, touched, or renamed.

## 4. Remote Fabric branches (read-only `git ls-remote`; `GIT_TERMINAL_PROMPT=0`; credentials-file NOT opened)
| Branch / pseudo-branch | Head sha |
|---|---|
| `refs/heads/main` | `b8ff81043e47e4b652522be34444bf52fcf4d65e` |
| `refs/heads/evidence/cnv-pipd-ls-sp-20261015-r6` | `a10f7bea645792048e3415443d417ffa3c2ac890` |
| `refs/heads/evidence/cnv-pipd-ls-sp-20261015-r7` | `04a1e118dd6616ccb6b2e68b68544fd5af4271ae` |
| `refs/heads/evidence/cnv-pipd-ls-sp-20261015-r8` | `3af4148021c2cc7bd5a30fba3f3dd46de61bb854` |
| `refs/heads/evidence/cnv-pipd-ls-sp-20261015-r9` | `5cd47ceaa493f37de479aa558f1123fd4e3e4136` |
| `refs/heads/evidence/cnv-pipd-ls-sp-20261015-r10` | `34d57124415dac04860aeabfe12863304078f4e2` |
| `refs/heads/pub/lane-reliability-closure-20261016` (PR#6 peer) | `0cb59d904224afc553906ebab002d443a3981e3d` |
| `refs/heads/pub/far-remediation-and-closure-20261016` (PR#8 peer) | `5ae6f37d305fa9da2da8e9a05b03ff65f02bd04f` |

## 5. Advisory defects worth flagging to the succeeding session
- **Epoch drift (control plane):** `HANDOVER_R10.md` section 2 pins the registry at **epoch 21**; the file's
  own header now reads **epoch 22** (owner-ordered PLAN/VERIFY rebind since R10). A successor must re-measure
  rather than trusting section 2.
- **`entry_map.json` absence (skill truncation shell):** `SKILL.md:66,71` relies on it as the mandatory STOP
  control for trim-slice restore; `ERR_ENTRY_MAP_*` can never fire on real data.
- Four receipt-file citations in the skill's `references/` folder point to receipts that do not exist on
  disk - a checker opening them will fail (see `dangling_pointers.tsv` rows for lines 89, 133, 152, 192).
- **HANDOVER section-1 cross-round pointers:** the `-R9/...` prefixed `R9_LEDGER.json` + `dispatch_r9.py`
  do resolve, but only from the `-R9` packet, which matches how the handover frames them.

## 6. Deliverables written here
- `integrity_audit.json` - 21 locators, each with bytes + sha256 where applicable.
- `dangling_pointers.tsv` - 15 rows: 12 dangling, 3 planned/documented.
- `report.md` - this document.
