# Tasks — hgk-round3-lane-rebind-20261016

## 1. Rebind (R1)

- [x] 1.1 `routes[].PLAN`: provider/model/canonical_identity/auth/oauth -> `opencode-go/glm-5.3-flash`.
- [x] 1.2 PLAN arms: primary = glm (default, automatic), fallback1 = gpt-6.1-sol (NON-default,
      `prior_revision_note` retained), fallback2 = deepseek-v4.1-flash.
- [x] 1.3 PLAN `fallbacks[]` order moved with the order; `selection_authority` names the 2026-10-16 order.
- [x] 1.4 `routes[].VERIFY_SECURITY`: rank-1 default -> `opencode-go/deepseek-v4.1-flash`,
      `selected_arm: A`, `selected_arm_identity: deepseek-v4.1-flash`.
- [x] 1.5 VERIFY arms: A = deepseek (primary/default), B = gpt-6.1-sol (non-default operator-selectable),
      C = glm (automatic fallback); `fallbacks[]` order moved.
- [x] 1.6 Assignment site `lane_chains.PLAN` / `.VERIFY_SECURITY` rewritten to agree, including flags.
- [x] 1.7 Dispatch-time pool ranks: PLAN glm -> 1, VERIFY deepseek -> 1; pool revision 9 -> 10 with a
      `change_log` entry and a `selection_note` recording the CANDIDATE-vs-operative mismatch.

## 2. SoD re-declaration (R2)

- [x] 2.1 `sod_invariants.pairs`: EXECUTE/VERIFY_SECURITY `distinct_required: false` (demoted, note names
      the order); PLAN/VERIFY_SECURITY `distinct_required: true` (models differ again).
- [x] 2.2 `declared_conflicts.SOD006-C3` added: exact pair, `OWNER_ORDERED_IN_FORCE`, and a note stating
      what independence REMAINS and what is given up.
- [x] 2.3 `SOD006-C2` -> `SUPERSEDED` with `superseded_by` naming the order; entry retained.
- [x] 2.4 The nine affected `sod` prose fields rewritten so no field contradicts the structured flags
      (F-IND-2/NF-03 class).

## 3. Coupling (R3)

- [x] 3.1 `epoch` 21 -> 22 and `revision` 21 -> 22 in both the registry and the site.
- [x] 3.2 `source_of_routes.sha256` re-pinned to the live site digest (else `ERR_LANE_SOURCE_STALE`).
- [x] 3.3 Every drifting `projections[].bindings[].expected` re-bound from the live site, by a
      drift-driven pass (17 re-bindings), with the projection note moved to revision 22.
- [x] 3.4 Conformance fixture `tests/test_lane_policy.py` owner chain moved in the same change.
- [x] 3.5 Oracle: `check_drift` 0 errors; conformance suite OK.

## 4. Enforcement agreement (R10)

- [x] 4.1 `lane_policy.sod_declaration_exemption(...)` — pure, registry-only, requires BOTH the demoted
      pair flag AND a `declared_conflicts` entry with status `OWNER_ORDERED_IN_FORCE`.
- [x] 4.2 Guard: OPTIONAL `--maker-lane`; inference only when exactly one route's default arm matches;
      otherwise fail closed.
- [x] 4.3 The exemption is VISIBLE: the verdict carries `declared_conflict: <id>`.
- [x] 4.4 RED-first tests: undeclared -> exit 2; declared -> SoD passes and names the id; distinct ->
      unchanged; declared-but-not-owner-ordered -> still refused.
- [x] 4.5 Oracle from canonical: 7/7 cases as specified in `evidence/ORACLE_R10_RECEIPT.json`.

## 5. Disclosure and closure

- [x] 5.1 SC-12 (backup taken after the write) found, disclosed, and corrected; preimages recovered by
      digest from the previous round's frozen subject tree and installed under `preimages/`.
- [x] 5.2 SC-13 (unquoted YAML note made the registry unparseable) found and corrected.
- [x] 5.3 SC-14 (a bound site field was dropped, producing a COVERAGE_GAP) found and corrected by
      restoring the field rather than deleting the binding.
- [ ] 5.4 R11 (no admission-receipt producer exists in the product) recorded as an open gap; the round does
      NOT invent one.
- [x] 5.5 Independent VERIFY/SECURITY verdict obtained on the frozen subject, disclosed as coming from a
      checker that shares the writer's model by owner order.
- [x] 5.6 Packet, gate report, publication branch and closure published for an external verifier; the
      MERGE remains the OWNER's decision.
