# Governing-clause binding — R9-0 FAR SOURCE_FAMILY

**LOCAL / candidate-only research. Not acceptance, Gate PASS, execution authority, or an Owner decision. No fixes proposed.**

## Scope and reading rules

Only the three supplied governing documents were read for this binding; no subject code, registry, ACL, runner, packet tree, or credentials were inspected, and no network call was made. Current-state assessments are conditional on the residual descriptions supplied by the delegator. `no` means that described state does not demonstrate/satisfy the quoted predicate, not a fresh independently reproduced runtime defect; `unknown` means the clause and supplied state do not decide it. R8-F4 `yes` is limited to correct warning-only classification, not verification that a linter emitted a warning.

`doc_clauses.json` contains every exact quote, its absolute document name, physical UTF-8 line interval, zero-based UTF-8 byte interval [start,end), requirement, assessment, and basis. Each nonempty quote was re-read from its exact on-disk byte interval before writing. ABSENT records have an empty quote: ABSENT is a research result, not fabricated source text. Source anchors such as BP2 L1892 and U L182–200 are embedded source references, not the physical line numbers of this PKG.

## 10/6 — exact meaning and limit

**10/6 means AVR ten-piece byte reconstruction and HGK six-piece byte reconstruction, together with their separate main-selection/actual-loader parity obligations.** It is not 10 requirements versus 6 tests, nor permission to substitute five AVR slices merely because six HGK entry-map IDs exist.

- FAR-C020 quotes current Slot RQ06/ACC-RQ06 at PKG physical lines 1588–1600: child obligations explicitly name `AVR/10-piece byte reconstruction` and `HGK/6-piece byte reconstruction`, while the aggregate requires `BOTH_BYTE_EXACT_AND_LOADER_PARITY` and rejects byte-exact-only.
- FAR-C021 supplies the exact `CNV-BP2-SECTION16` parent, BP2 SHA/source-clause and BP2 L1892 pointer. The PKG is a projection referencing BP2 §16, not the physical BP2 original. Its retained prose at PKG lines 53193–53205 restates BP2 L1892 and the same four child obligations.
- FAR-C022 quotes ACC-RQ12: `AVR10_HGK6_EXACT`, full-source SHA for both, correct slice order and no loss/duplication. FAR-C023 names the precondition `source bytes, 10/6 slice root`; FAR-C024 gives closure `byte exact 10/6 + loader parity + negative state transitions`.
- **Concrete physical partition table: ABSENT in these three documents.** Searches covered every PKG `10/6` occurrence (15), slash variants, slice/chunk/piece/root/partition terminology, BP2 §16 references and partition-table wording. No table supplies ten AVR filenames or piece boundaries/offsets and their concrete slice-root mapping. FAR-C025 is only retained synthetic code generating `slot0...` chunks for counts (10,6), not a source partition definition. FAR-C026 records this bounded absence.
- The supplied five AVR S1..S5 artifacts and six HGK entry-map IDs are not inspected here. If those five are the complete AVR reconstruction, they do not satisfy the literal ten-piece count. Six HGK IDs are count-compatible only, not proof of byte identity, correct partition, source SHA, actual selection, or loader parity. These documents cannot resolve whether five artifacts internally contain ten original pieces.

## Residual bindings and absences

| Residual | Verbatim governing excerpts | ABSENT records | Binding limit |
|---|---:|---:|---|
| BLK-R8-WS2-MAIN-DIVERGENCE | 4 | 1 | General admitted repair/evidence/regression rules; neither failing test is named. |
| EIA-R6-03 | 4 | 0 | Read-only candidate ACL, external checker write root, denial test, distinct identity/actual ACL. |
| TF-06 | 3 | 0 | Same-run nonce/usage and required/served-arm provenance; dispatcher failure is not clean execution. |
| R8-F6 | 6 | 1 | Owner route authority, pinned required/served route, admitted scoped WorkOrder and separate DOC05 ADMIT; no exact registry provider/model specified. |
| R8-F7 | 6 | 1 | AVR10/HGK6 plus source SHA, correct ordering, selection/loader and negative transitions; concrete partition mapping absent. |
| EIA-R6-05 | 5 | 0 | Owner-authorized complete runtime evidence/Gates versus separately scoped evidence-only archive conditions. |
| EIA-R6-07 | 2 | 0 | Owner version-controlled active-normative vs historical decision and honest active denominator. |
| R8-F4 | 2 | 1 | 60-reference threshold is soft warning, not hard block; 100,000-byte main cap absent. |
| R8-F2 | 4 | 0 | Published manifest/latest Git tree exact-set equality, explicit ignored/excluded disposition and currentness. |

## Required / forbidden / conditionally permitted — text bindings only

### The two failing tests

- **Test-specific mandate or prohibition: ABSENT.** None of the three documents names the two supplied tests, their filenames, or `derive_frozen_context`; no PKG clause says those particular tests must be fixed or must not be fixed (FAR-C001).
- **General repair is conditional, not categorically forbidden.** PKG line 46 bounds ConstructionContract changes/tests/evidence/rollback and separates DOC05 Admission from WorkOrder/ECP (FAR-C004). PROMPT line 122 requires reproduce → first-fail → RCA → smallest affected patch → focused+negative → regression → residue/rollback test → checker fresh recheck (FAR-C002). It is a repair procedure, not a proposed fix or a fresh WorkOrder.
- **Validator hardening cannot omit neighboring positive/negative/regression evidence** when the EIA-R6-04 predicate applies (FAR-C005). The quoted text does not establish that either specific AttributeError test is itself an EIA mutant or decide the technical remedy.
- **Not required for the historical evidence-only PR merge:** EIA line 179 excludes mutant fixes, 221 live tests and eight Gate PASS as merge prerequisites under that evidence-only change class (FAR-C031). This does not authorize an executable main change or waive later runtime acceptance.

### Control-plane registry edits without an Owner WorkOrder

- **Canonical mutation without the required approved scope/WorkOrder and separate DOC05 ADMIT is forbidden under the general execution contract.** PKG AUD-P0-07 explicitly says `NO mutation until separate scoped ADMIT verified` and calls for actual PD/WorkOrder/ECP/TQAEP (FAR-C017); PROMPT CNV-09 requires typed admitted WorkOrder/token or HOLD (FAR-C016); PKG line 34 reserves model-route approval to HGK Owner (FAR-C013).
- The retained PKG-06 wording explicitly says to read an approved WorkOrder, reject patches outside the allowlist and write only after Owner actor plus separate DOC05 ADMIT evidence (FAR-C018). **This excerpt lies inside PKG §16's preserved legacy material; it is supporting retained wording, not new independent authority or an instruction to execute legacy code.** Current PKG/指揮薄 obligations above provide the primary binding.
- **Registry-specific literal prohibition: ABSENT.** No clause names `lane-routing-registry`, `model-lane-assignment`, `VERIFY_SECURITY`, or `opencode-go` (FAR-C019). Thus these sources neither prescribe the reported exact route value nor forbid every possible registry edit. They require Owner route approval and admitted bounded execution for a canonical edit; a research/candidate artifact is not authority to apply it. The phrase “Owner WorkOrder” must not collapse Owner approval, typed WorkOrder, ECP and DOC05 Admission into a single permission.

### Other explicit limits

- Checker writing the candidate / maker acting as checker is not permitted; lane labels alone are not filesystem isolation (FAR-C006–009).
- Clean runtime execution cannot be claimed from exit0 alone or without same-turn arm evidence (FAR-C010–012).
- More than 60 references must not be turned into a hard gate; this corpus supplies no 100,000-byte main-file cap (R8-F4 rows).
- Full convergence / formal runtime acceptance remains owner-gated; the historical evidence archive's narrower conditions do not create Gate PASS (EIA-R6-05 rows).
- Source #6 active-vs-history classification belongs to Source/Authority Owner; this extraction makes no such decision (EIA-R6-07 rows).
- A publication manifest cannot claim an unequal shipped set as complete, while explicitly labeled local inventory and excluded files are a different declared boundary (R8-F2 rows).

## NON-CLAIMS

- No independent acceptance, canonical acceptance transition, AO signature, release, production readiness, Gate PASS, or owner-authorized route decision.
- No fresh assertion that the two tests fail, which model arm served, the current registries disagree, ACL denial is absent, bytes exceed a cap, or the packet actually contains 581 files; those are delegated residual descriptions only.
- No test execution, embedded verifier execution, credential access, network access, repository/registry/control-plane mutation, remediation, or proposed technical fix.
- No statement that source #6 is active or historical, that 221 cases are all applicable, or that an Owner WorkOrder is already sufficient to authorize effects.
- No external BP2/U original verification, physical 10/6 partition reconstruction, actual loader test, or extension of retained historical snippets into current authority.
- Research artifact writes are limited to the two requested files in the admitted FAR directory.

## Source fingerprints

- `Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md` — 2689181 bytes; SHA-256 `96d9d564286743e17550ccef15b9952347901eb77168f930376938893cff9c3f`.
- `Fabric_Convergence_External_Independent_Acceptance_Report_20261015.md` — 33616 bytes; SHA-256 `10caf4dbdb1993cd46ff2c50394dd01dfd5f34d635816f95e3d2e5ab6c566206`.
- `Fabric_HG-KSEOS_Convergence_指揮薄PROMPT.md` — 27321 bytes; SHA-256 `6894a6ba08781f2ed5758af132f758c14c1a9e9b69d42056837f5ce45bba6c64`.

The JSON has 36 nonempty exact-excerpt records and 4 ABSENT records. Counts include explicit contextual/source-locator excerpts; the legacy synthetic example is labeled non-normative. No absence claim extends beyond these three documents.
