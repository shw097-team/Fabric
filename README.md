# Fabric — Integrated Governance Mirror

> **Fabric + FAR + the desktop-effect plane + HG-KSEOS** — integrated under one governance contract,
> mirrored so that an **external engineer can plan a complete upgrade** of the subjects from this
> repository alone.

## 1. Governance contract of this integration

```
在 current Fabric 治理契約下，
以 HG-KSEOS 作為唯一控制平面 (sole control plane)，
並將 current canonical Hermes 綁定為其受治理的 Runtime／Orchestration Plane
(governed runtime / orchestration plane).
```

| Layer | Role | What it may NOT do |
|---|---|---|
| **Fabric** | governance contract / policy owner of the system | not a runtime; does not execute work |
| **HG-KSEOS** | **sole control plane**: typed lifecycle, admission, evidence ledger | may not self-accept; may not accept on a subject's behalf |
| **canonical Hermes** | governed Runtime / Orchestration Plane under HG-KSEOS | is not a controlling authority; routing changes are owner-gated |
| **FAR** | research product: contracts, routing, retrieval | does not own governance |
| **desktop-effect plane** | documented desktop procedures, guards, skills | no live-world effect is claimed here |

## 2. Start here — planning an upgrade from outside

| If you want to … | read |
|---|---|
| know what may be planned against | [`INTEGRATION/UPGRADE-SCOPE.md`](INTEGRATION/UPGRADE-SCOPE.md) |
| follow the ordered procedure | [`INTEGRATION/UPGRADE-PLANNING-GUIDE.md`](INTEGRATION/UPGRADE-PLANNING-GUIDE.md) |
| map this mirror onto the four subjects | [`INTEGRATION/SOURCE-PROJECTION.md`](INTEGRATION/SOURCE-PROJECTION.md) |
| see cross-subject dependencies and who may change what | [`INTEGRATION/DEPENDENCY-AND-CONTRACT-MATRIX.md`](INTEGRATION/DEPENDENCY-AND-CONTRACT-MATRIX.md) |
| know the tests and the rollback for a change | [`INTEGRATION/VALIDATION-AND-ROLLBACK.md`](INTEGRATION/VALIDATION-AND-ROLLBACK.md) |
| know what is **not** claimed | [`INTEGRATION/NON-CLAIMS.md`](INTEGRATION/NON-CLAIMS.md) |
| see what this publication contains and excludes | [`INTEGRATION/MANIFEST.json`](INTEGRATION/MANIFEST.json) |
| read the hygiene record and the independent verdict | [`EVIDENCE/repo-hygiene-20261013/`](EVIDENCE/repo-hygiene-20261013) |
| read the current round's closure record and its independent check | [`EVIDENCE/SKILL-CONVERGENCE-20261014/`](EVIDENCE/SKILL-CONVERGENCE-20261014) |

**Capability test.** An external engineer must be able to produce the upgrade scope, the dependency
and contract map, the validation plan, the rollback plan and the non-claim list — from this
repository alone, without any private workspace path. The `INTEGRATION/` set exists to make that
test passable.

## 3. Repository layout

| folder | contents |
|---|---|
| `HG-KSEOS/` | control plane: contracts, typed lifecycle, evidence, requirements |
| `FABRIC/` | governance contract, research and automation trees, methods and skills |
| `FAR/` | research-product contracts, routing and retrieval |
| `DESKTOP/` | desktop-effect plane: documentation, guards and skills (runtime state is a named, bounded exception — see the manifest) |
| `INTEGRATION/` | the readiness set described in section 2, plus the mirror manifest |
| `EVIDENCE/` | assessment, hygiene and independent-check records |

## 4. Ground rules for contributors and planners

1. **Do not read this repository as an authority.** It is a projection; `HG-KSEOS` is the control plane.
2. **A gate that is not named is not passed.** Presence, digests, file counts and model votes are not passes.
3. **Owner-class decisions stay with the owner**: licence choice, bulk-binary disposition, remote
   linkage, subject baseline re-certification and acceptance are recorded as open, never resolved here.
4. **Never publish credentials or machine-local state.** The root `.gitignore` encodes the publish control.
5. **Changes arrive as a reviewed change-set**, on a branch, with an approval list, then merge.

## 5. Status of the subjects
> **Status refresh, 2026-10-16 — supersedes the dated lines kept below as history.** Since those lines were written, PR #12 merged as `6c25bbe8`, PR #13 as `603cb0cb`, and PR #14 as `bcd91043` (the current default-branch commit), each read back blob by blob. PR #15 is open and NOT merged. The status words are unchanged: NOT_EXTERNALLY_ACCEPTED · NOT_MERGED · NOT_RELEASED · NOT_PRODUCTION · NO_LIVE_WORLD_EFFECT.


`NOT_EXTERNALLY_ACCEPTED · NOT_MERGED · NOT_RELEASED · NOT_PRODUCTION · NO_LIVE_WORLD_EFFECT`

Published 2026-10-13T11:50:38.128148+00:00 (the readiness set). A second publication is recorded: **2026-10-14, change-set
`docs/skill-convergence-20261014`** — it carries the candidate-only convergence round's closure record and its independent
check under [`EVIDENCE/SKILL-CONVERGENCE-20261014/`](EVIDENCE/SKILL-CONVERGENCE-20261014), brings the `FABRIC/` front page up
to the local revision, adds the round's rows to [`INTEGRATION/KNOWN-FINDINGS.md`](INTEGRATION/KNOWN-FINDINGS.md), and changes
no contract. Each publication is preserved in history and records its own scope, its hygiene result and its open owner
decisions.

---

# Appendix for external readers (added 2026-10-16)

_Written following the round 'CNV-HYGIENE-README-CLOSURE-20261016'. Its facts were verified independently of this appendix and are archived under `EVIDENCE/CNV-HYGIENE-README-CLOSURE-20261016/`. The appendix is additive: every section above is unchanged except the status refresh._

## What this repository is

This repository is a governance projection mirror. Under the current Fabric governance contract,
HG-KSEOS is the sole control plane, and the current canonical Hermes is bound as its governed
Runtime/Orchestration Plane. The repository mirrors the policy, assurance, interop and knowledge
surfaces of that governance stack. This is a mirror, not the canonical working tree.

## Where the evidence lives

| Prefix | What it holds |
|---|---|
| `EVIDENCE/CNV-PIPD-LS-SP-20261015-R6` … `-R11` | The six round packets of the convergence mission `CNV-PIPD-LS-SP-20261015`, merged through #3, #4, #5, #7, #9, #11. |
| `EVIDENCE/CNV-EVIDENCE-ARCHIVE-R7R11-20261016` | The archive of rounds R7-R11 as candidate evidence (#12). |
| `EVIDENCE/FAR-20261016-018-r7r11-residual-closure-and-handover` | The Fabric Autonomous Research round on the residual register, including its adjudication and its 2 UNVERIFIABLE checker items (#13). |
| `EVIDENCE/FAR-20261019-owner-authorized-closure` | The owner-authorised closure round, including the verifier report whose content is `NO_VERDICTS_FOUND` (#14). |
| `EVIDENCE/CNV-FAR018-FAR019-ARCHIVE-20261016` | The archive round's own return pack (PR #15, still open). |
| `EVIDENCE/CNV-PIPD-LS-SP-20261015-R6`, plus the earlier `EVIDENCE/skill-convergence-20261014*` packets | Carry the skill-convergence evidence. |

Reading order: open `EVIDENCE/CNV-PIPD-LS-SP-20261015-R6` first, then walk `-R7` to `-R11`, then read
the FAR and archive prefixes above.

## Pull requests and merge commits

| PR | merged | merge commit | files | head branch |
|---|---|---|---|---|
| #3 | yes | `b8ff81043e47e4b652522be34444bf52fcf4d65e` | 581 | evidence/cnv-pipd-ls-sp-20261015-r6 |
| #4 | yes | `12cdeefe5ff5b19edd50bf9099bf47a5fb9e2452` | 306 | evidence/cnv-pipd-ls-sp-20261015-r7 |
| #5 | yes | `b03962313596a92d38b21592f5a8819ba95436db` | 359 | evidence/cnv-pipd-ls-sp-20261015-r8 |
| #6 | yes | `5541ed99a81c2334bf31e26e0150215375bafeae` | 74 | pub/lane-reliability-closure-20261016 |
| #7 | yes | `c1debccd8bd0c5ffa2b247c8ce8f3f7441dacc90` | 120 | evidence/cnv-pipd-ls-sp-20261015-r9 |
| #8 | yes | `5790e2cfb3cc19c71601bf77bead92b89ca15b32` | 131 | pub/far-remediation-and-closure-20261016 |
| #9 | yes | `74431eb24564f3ef3e93ccb328e4fa13d45be252` | 69 | evidence/cnv-pipd-ls-sp-20261015-r10 |
| #10 | yes | `1807680ebf467aaee80b3d628ceb328fab0734df` | 350 | pub/round3-lane-rebind-and-closure-20261016 |
| #11 | yes | `312baa0ee2aa591000959cc878bb978a31c89796` | 77 | evidence/cnv-pipd-ls-sp-20261015-r11 |
| #12 | yes | `6c25bbe8cf14af544c79b36c4b9c0e84778690b1` | 33 | evidence/cnv-evidence-archive-r7r11-20261016 |
| #13 | yes | `603cb0cb39275b351dd4f5312c723977de2a1349` | 55 | evidence/far-018-r7r11-residual-closure |
| #14 | yes | `bcd91043b89b69c9d2f08309e46e31898ac87d89` | 83 | evidence/far-019-owner-auth-closure |
| #15 | NO — open | (none; the API's `merge_commit_sha` for an open pull request is a test-merge preview, not a merge) | 31 | evidence/cnv-far018-far019-archive |

## What is NOT claimed

- No independent acceptance has been issued.
- The external scope verdict is PARTIAL_CHALLENGE.
- The full-convergence verdict is TEMP_CLOSED_CHALLENGE.
- No canonical AO acceptance is issued.
- No DOC-05 effect admission was granted.
- The production/runtime release verdict is FAIL_CLOSED.
- One round's verifier report contains `NO_VERDICTS_FOUND` (an empty verdict list); this is not a pass.
- One lane sub-run ended in a timeout; this is not a pass.
- The independent-checker boundary is not proven.
- The checker cannot yet be shown to be unable to lift its own isolation.
- Model-axis independence is ABSENT: the writer and the checker of the most recent execution round ran the same model.
- Only the process and evidence paths were separate for that round.
- No CI status exists, because there is no workflow; a green light must never be claimed from this repository's status API.
- The 221 acceptance cases have NOT been accepted.
- The eight runtime gates have NOT been accepted.
- The technical-admission denominator is tracked, not passed.

## How to verify a claim yourself

1. Read a merge commit, for example `bcd91043b89b69c9d2f08309e46e31898ac87d89` (from PR #14), and
   inspect the change it actually landed.
2. Compare a blob's sha: the `README.md` at `main` is blob `9dd1946c3a7c9c76089c814b7ec75c46ab1210b2`;
   the tree at `main` (`bcd91043b89b69c9d2f08309e46e31898ac87d89`) has 4145 blobs and 629 trees.
3. Find the receipt inside a prefix: open the `EVIDENCE/<round>/` directory you care about and read its
   returned receipt and checker output.
4. Check whether a branch's pull request is merged: for `evidence/cnv-far018-far019-archive` (PR #15)
   the answer is NO — it is open, and its `merge_commit_sha` is a test-merge preview, not a merge.
