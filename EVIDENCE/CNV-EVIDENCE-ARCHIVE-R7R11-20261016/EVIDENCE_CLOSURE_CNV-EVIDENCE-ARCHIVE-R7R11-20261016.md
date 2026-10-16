# Evidence closure - candidate evidence archive (R7-R11 follow-on)

`contract_id: CNV-EVIDENCE-ARCHIVE-R7R11-20261016` | `mission_id: CNV-PIPD-LS-SP-20261015` | `project_id: CNV-EA-R7R11`

## 0. Claim ceiling (read this first)

```text
claim_ceiling            : CANDIDATE_EVIDENCE_ARCHIVED_ONLY
archive_verdict          : TEMP_CLOSED
full_convergence_verdict : TEMP_CLOSED_CHALLENGE
production_verdict       : FAIL_CLOSED
canonical_ao_acceptance  : NOT_ISSUED
r7_02_validator          : CANDIDATE_REPAIRED_NOT_RELEASED
r7_03_checker_acl        : NOT_ACCEPTED
r7_04_g1                 : NOT_RECERTIFIED
live221 / gates_A_H      : NOT_VERIFIED / NOT_RUN
```
This packet archives CANDIDATE evidence. It is **not** an acceptance of the validator, the checker
isolation, the Hermes/HGK runtime, the convergence or production. No pull request referenced here is
merged by this round; every `merge_sha` / `readback_sha` / `maintainer_approval` is `null`.

## 1. Binding

- control plane: HG-KSEOS (admission ref `ADMISSION_OK`, checkpoint `CK-R7R11-4181BD0E`)
- runtime/orchestration: Hermes (lane registry epoch `22`, drift `{'count': 0, 'fatal': False, 'findings': []}`)
- compiler: verdict `PROMPT_COMPILE_PASS` (contract sha256 `77b1183ad89824b1ef7723d270ca24bc96c26a29059d086c7356246d4773e090`)
- mirror under test: `shw097-team/Fabric`, read-only readback only

## 2. What this round ran

| step | action | result |
|---|---|---|
| A00 | files-first source ledger over the frozen sources | 44 sources; 20/20 knowledge packs located; 1 real gap (the Fabric tree has no root `AGENTS.md`) |
| A01 | prompt-contract compiler lint/activation/acceptance/compile/duplication | `PROMPT_COMPILE_PASS` |
| A02 | HGK typed admission + kanban board + swarm graph + openspec change + gstack route check | admitted; board live; openspec strict-valid |
| A03-A05 | per-PR latest HEAD / single evidence prefix / change class / manifest / secret scan, read-only | all 8 `EVIDENCE_ONLY` |
| A09 | K-01..K-20 source-vs-retested cross index | 20/20 source-linked, 0/20 same-run retested |
| EXECUTE | bounded writer lane, CODEX CLI on the mandated arm | packet produced under a bounded write root |
| VERIFY | independent checker lane, separate dispatch | re-derivation verdict recorded in the packet |
| R6-R11 | no existing round artifact was rewritten | historical FAIL / NOT_RUN receipts left immutable |

## 3. Per-PR preflight (read-only, not an approval)

| PR | head (frozen) | prefix | changed | prefix escapes | hard secrets introduced | class |
|---|---|---|---:|---:|---:|---|
| #4 | `04a1e118dd66` | `EVIDENCE/CNV-PIPD-LS-SP-20261015-R7/` | 306 | 0 | 0 | EVIDENCE_ONLY |
| #5 | `3af4148021c2` | `EVIDENCE/CNV-PIPD-LS-SP-20261015-R8/` | 359 | 0 | 0 | EVIDENCE_ONLY |
| #6 | `0cb59d904224` | `EVIDENCE/LANE-RELIABILITY-CLOSURE-20261016/` | 74 | 0 | 0 | EVIDENCE_ONLY |
| #7 | `5cd47ceaa493` | `EVIDENCE/CNV-PIPD-LS-SP-20261015-R9/` | 120 | 0 | 0 | EVIDENCE_ONLY |
| #8 | `5ae6f37d305f` | `EVIDENCE/FAR-REMEDIATION-AND-CLOSURE-20261016/` | 131 | 0 | 0 | EVIDENCE_ONLY |
| #9 | `34d57124415d` | `EVIDENCE/CNV-PIPD-LS-SP-20261015-R10/` | 69 | 0 | 0 | EVIDENCE_ONLY |
| #10 | `4695e0cf870f` | `EVIDENCE/ROUND3-LANE-REBIND-AND-CLOSURE-20261016/` | 350 | 0 | 1 | EVIDENCE_ONLY |
| #11 | `5e055ea28e44` | `EVIDENCE/CNV-PIPD-LS-SP-20261015-R11/` | 77 | 0 | 0 | EVIDENCE_ONLY |

Totals: 8 PRs, 0 prefix escapes, 8 of 8 classified `EVIDENCE_ONLY`.

Every changed path lies under that PR's single `EVIDENCE/<folder>/` prefix, no path carries a
symlink or submodule git mode, and no changed path leaves `EVIDENCE/`. The archived `.py`/`.ps1`
files are evidence payloads and are not executed by this round or by this commit.

One hard secret-shape hit exists (PR #10). It is adjudicated a synthetic test fixture that already
exists byte-identically in `main`, i.e. not introduced by this round; the fixture's own test asserts
that such a string must be treated as poisoned input. Its value is not reproduced here - only its
length and a hash.

## 4. Gate calibration

| gate | requirement for THIS change class (evidence-only) | recorded state |
|---|---|---|
| G-A skill byte/loader | recorded as local-installed/candidate; no PASS claimed | NOT_RUN (not in scope) |
| G-B G1 | no runtime executed; must not be claimed | NOT_RUN (not in scope) |
| G-C route/timeout | no dispatch of the subject; original raw preserved | NOT_RUN (not in scope) |
| G-D trace/evidence | manifest + changelog + written claim ceiling | PASS (this packet) |
| G-E world effect | no world effect; not claimable from file presence | NOT_RUN (not in scope) |
| G-F SoD/approvals | maintainer prefix-scope review; reviewer does not self-approve | BLOCKED - no maintainer approval recorded |
| G-G publication | exact-only diff, trusted secret scan, head/manifest/readback | PASS (preflight) |
| G-H release | `CANDIDATE_EVIDENCE_ARCHIVED` only | PASS as candidate only |

## 5. Checks

| check | what | result |
|---|---|---|
| Q01 | compiler lint/activation/acceptance/compile | PASS |
| Q02 | source digests / currentness | PASS (1 named gap recorded) |
| Q03 | 8 PR exact prefix / change class | PASS |
| Q04 | manifest vs changed set | PASS |
| Q05 | trusted secret scan (with positive + negative control) | PASS (1 pre-existing fixture) |
| Q06 | SoD / publishing scope | PARTIAL - model-axis independence absent by owner order (declared) |
| Q07 | narrow patch / admission | N/A - no patch was needed |
| Q08 | per-PR remote merge readback | BLOCKED - requires a real maintainer action |
| Q09 | K-ledger source vs same-run retest | PASS (20/20 linked, 0/20 retested) |
| Q10 | EIA-01..10 dispositions | PASS (10 rows) |
| Q11 | mandated metric sets recorded as TRACKING only | PASS (never counted as run results) |
| Q12 | checkpoint / rollback / provenance | PASS |

## 5b. Independent checker lane (separate dispatch, read-only posture)

A second, separately dispatched lane re-derived the decisive claims. Arm attribution: `opencode-go/deepseek-v4.1-flash` required / `opencode-go/deepseek-v4.1-flash` served; model `deepseek-v4.1-flash`, provider `opencode-go`, exit `0`, nonce present `True`.

| re-derivation | checker verdict |
|---|---|
| V1 per-PR heads and changed counts | AGREE |
| V2 bounded prefix / no symlink or submodule mode | AGREE |
| V3 the hard secret hit is a fixture pre-existing in main | AGREE |
| V4 pack invariants (8 rows / null merge / lattice / no PASS) | DISAGREE |
| V5 K-ledger 20 rows / 20 linked / 0 retested / 7-7-6 | AGREE |
| V6 scanner self-test is non-vacuous | AGREE |

The one DISAGREE is recorded verbatim and adjudicated, not swallowed: the checker found that the
substring `PASS` DOES occur once in `packet/RETURN_PACK.json`, in `compiler.verdict ==`
`PROMPT_COMPILE_PASS`. The root cause is this round's own instruction, which forbade the substring
`PASS` in any verdict-bearing field while the governing contract requires that very receipt token.
Disposition: the claim is narrowed to the subject axis and re-proved deterministically
(`VERIFY_DISAGREEMENT_ADJUDICATION.json`, 27 PASS-bearing tokens, 0 subject-axis violations, every
lattice field exact), and the checker's disagreement is preserved in this packet.

Non-mutation guard: `CLEAN` over `5` files (guard roots: packet/ and the three receipt artifacts). Sandbox: `workspace-write` (escalated from the lane default with `--allow-sandbox-escalation`; NOT the forbidden `danger-full-access` tier).

SoD honesty: the mandated scheme assigns BOTH the writer and the checker to
`opencode-go/deepseek-v4.1-flash`, so model-axis independence is **ABSENT by construction**. This
packet declares that rather than implying cross-model verification. The compensating controls
actually in force are: a separate dispatch and process, separate roles, a bounded write root for
the writer, a non-mutation guard for the checker, and no self-approval at the maintainer gate.

## 6. External findings routing

| finding | disposition | owner | next task spec |
|---|---|---|---|
| EIA-20261016-01 validator false green | DEFER | PIPD DOC07 Validator / code Owner | `R7-02-CODE-PROMOTE` |
| EIA-20261016-02 checker wrote 13 RAW files into the subject root, then restored | DEFER | HGK Checker Harness Owner | `R7-03-ISOLATE` |
| EIA-20261016-03 G1 not fresh; declared 0.20.0 vs observed 0.21.5 | DEFER | Human Policy Owner / Hermes Owner | `R7-04-RUNTIME-BIND` |
| EIA-20261016-04 timeout partial capture, nonce, unknown-effect retry | DEFER | HGK Dispatcher Owner | `R7-04-DISPATCH-HARDEN` |
| EIA-20261016-05 long prompt via argv produced no artifact (K-11) | CONDITIONAL | Hermes Lane Owner | `K11-LONG-PROMPT-FILE-ROUTE` |
| EIA-20261016-06 20 K-IDs read as UNMAPPED, which means 0/20 same-run re-verified - not 20 missing sources | CLOSED_THIS_ROUND_METADATA_ONLY | Evidence / HGK Ledger Maintainer | `K-LEDGER-SEMANTICS` |
| EIA-20261016-07 slimmed skills installed and loader-visible, but entry_map.json is a dangling reference | DEFER | Skill Owner | `HGK-SKILL-DANGLING-REF` |
| EIA-20261016-08 221 planning cases and the eight gates have no authorised complete run | DEFER | PIPD DOC04/DOC07 + each domain Gate Owner + AO | `FULL-221-TQAEP-APPLICABILITY` |
| EIA-20261016-09 governance debt: superseded source #6, 20 KP R04 polarity conflicts, >60 reference soft warning | DEFER | Authority / KP Policy Owner | `KP-R04-POLARITY-AND-SOURCE-STATUS` |
| EIA-20261016-10 R9 maker 611 passed, but the independent checker could not re-run the original fixture | DEFER | PIPD Maintainer / Independent Checker | `R7-02-CODE-PROMOTE (same gate as EIA-01)` |

8 deferred, 1 conditional, 1 closed this round (metadata-only).

## 7. Nonclaims / STOP

- No pull request was approved or merged by this round; `MAINTAINER_APPROVAL_MISSING` stands for all 8.
- No canonical product, runtime, policy, hook, workflow, licence or credential was modified.
- No archived script was executed; no force update was issued; `main` was not written.
- The validator, the checker isolation and the runtime re-certification remain open by design.
- `NOT_RUN` is never rendered as `PASS` anywhere in this packet.
- STOP: the next lawful step is a real Repo Maintainer review per PR (prefix + actual HEAD +
  candidate-only + rollback), then a per-PR merge and remote readback by that maintainer.

## 8. Raw index and provenance

`PACK_INDEX.json` (in this packet) carries the byte length and SHA-256 of every other file here.
This document cannot carry its own final hash, so the index is the carrier of record for it.

