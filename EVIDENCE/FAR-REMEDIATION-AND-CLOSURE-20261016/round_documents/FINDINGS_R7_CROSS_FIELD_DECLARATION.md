# FINDING R7 — declaration surfaces that disagree, and no checker that looks

Round FAR-REMEDIATION-AND-CLOSURE-20261016. This finding was produced by the round's own remediation
work, not by an audit: it was found while measuring what had to change, and it is the reason R1 turned out
to be larger than "one route row".

## The measurement

`config/model-lane-assignment.json` simultaneously declared the VERIFY_SECURITY default arm as two
different things:

| surface | declared default arm A |
|---|---|
| `lane_chains.VERIFY_SECURITY[0]` | `openai-codex` / `gpt-6.1-sol` |
| registry `projections[]` pinned on that pointer | `openai-codex` / `gpt-6.1-sol` |
| `sod.verify_security_lane` (prose) | `opencode-go` / `glm-5.3-flash` |
| `sod.verify_security_default_arm` (prose) | `opencode-go` / `glm-5.3-flash` |
| `sod.verify_security_arm_A` (prose) | `opencode-go` / `glm-5.3-flash` |
| registry `projections[]` pinned on those prose pointers | `opencode-go` / `glm-5.3-flash` |

Both halves were satisfied against their own pointers, so **`check_drift` reported zero fatal findings in
that state** — verified this round, on the pre-change snapshot, before anything was edited. A drift gate
that compares each pointer with its own target cannot see two pointer groups contradicting each other.

`var/FAR-REMEDIATION-AND-CLOSURE-20261016/check_declaration_agreement.py` is the detector for that class.
Run against the preserved pre-change snapshot it reports 3 contradictions; against the canonical file
after R1 it reports 0. The detector is a round artifact, not yet product code.

## The same class, second instance: the lane guard's coupled pins

Applying R1 as first written left the pre-dispatch lane guard refusing with `exit_code=4` /
`ERR_LANE_SOURCE_STALE` on every evaluation. Two declarations are coupled to the site file and are checked
by the guard, not by `check_drift` and not by the conformance test:

- `source_of_routes{path: config/model-lane-assignment.json, revision, sha256}` pins the site's revision
  **and** its byte digest. Editing the site without re-pinning makes the guard treat the policy source as
  stale.
- the registry's `epoch` and the site's own `revision` (read as `live_epoch`) must advance together; the
  registry `epoch` alone reads as an epoch mismatch.

Consequence for the ruling: **a change to any declaration surface must enumerate its coupled pins**. This
round's R1 completion does that explicitly, and the coupling is now recorded rather than rediscovered.

## Why this is not a rewrite of F1

F1 (previous round, closed here) was a **cross-file** disagreement: `routes[].PLAN` in the registry versus
the owner chain and the pool. The conformance test caught it. R7 is an **intra-file** disagreement with no
checker at all. They are different classes and they need different remedies: F1 needed a rebind, R7 needs a
checker.

## Remediation priced for the next round (CANDIDATE ONLY — nothing here is product code)

1. **Lowest friction, highest value.** Promote `check_declaration_agreement.py`'s rule into
   `src/hg_kseos/lane_policy.py` as a cross-field sweep invoked by `check_drift`, RED-first test included.
   The rule is small: for every single-lane prose field, the model named as that lane's default must equal
   the lane chain's `[0]` model.
2. **Second.** Add the coupled-pin set (site digest, site revision, registry epoch) to the same sweep, so a
   half-applied declaration change fails at the gate instead of at the guard.
3. **Third, deliberately last.** Reconcile the remaining prose that still describes superseded revisions
   (`sod_across_all_arms.maker_checker_model_separation` still narrates a PLAN of `deepseek-v4.1-flash`
   and a VERIFY arm A of `glm-5.3-flash`; `/sod/lane_deviation_recorded` is marked SUPERSEDED_HISTORICAL).
   This is documentation debt, not a routing defect, and it should not block (1) or (2).

## Claim ceiling

The contradiction itself is **measured** on the pre-change snapshot preserved on disk. The three remediations
above are **proposals**: none is applied to the product in this round, and no acceptance is claimed.
