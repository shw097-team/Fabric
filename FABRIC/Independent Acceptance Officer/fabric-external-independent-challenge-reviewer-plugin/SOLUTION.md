# Fabric External Independent Challenge Reviewer — Complete Skill Solution

## 1. Engineering position

This package implements the external independent challenge layer for Fabric/HGK/Oracle. Its purpose is not to add a second Oracle or a second release reducer. It introduces model/runtime/context diversity at selected high-value gates while preserving the Internal Oracle as the primary operational checker after RP-002 O1.

The core separation is:

```text
HGK / Fabric maker
      ↓
Internal Oracle primary acceptance
      ↓
Frozen candidate + raw evidence
      ↓
External Independent Challenge Reviewer (Codex / Work, clean room)
      ↓
Meta-Oracle / Human adjudication only on final/disputed/high-risk edges
```

## 2. Why the Skill is generic

The Skill is intentionally named `fabric-external-independent-challenge-reviewer`, not `rp002-*`. RP-002-specific rules live in `references/rp002-profile.md`. This preserves reuse for RP-003 StoryForge and later Fabric projects without duplicating the assurance control plane.

## 3. Hard independence contract

The reviewer:

- reads frozen authority and exact candidate evidence;
- treats maker/Internal Oracle verdicts as claims;
- does not consume unstated maker memory as truth;
- does not write to the candidate;
- does not repair findings in the same review;
- does not edit the evaluator/Acceptance Pack to close a failure;
- does not promote/release/deploy;
- produces findings and smallest-repair handoff only.

## 4. RP-002 placement

Use routinely only at:

- O1 Internal Oracle qualification;
- F1 self-hosting cutover;
- E1 cross-stack evolution;
- E2 behavior-artifact evolution;
- E3 Oracle evolution when applicable;
- R1 final aggregate local acceptance;
- any serious Internal Oracle disagreement/escalation.

Do not external-review every normal gate by default; that would duplicate the Oracle and reduce the value of proving Fabric self-operation.

## 5. Evidence model

The reviewer requires exact candidate binding and raw evidence. A summary-only `PASS` is never sufficient for runtime/release claims. The challenge report is itself an auditable review artifact, but not automatically the release decision.

## 6. Gate calibration defense

Every high-risk PASS is challenged for objective alignment, risk-proportionate strictness, negative/adversarial coverage, regression baseline, anti-overfitting, judge calibration, and required HITL/domain review.

## 7. Distribution strategy

- **Codex / ChatGPT desktop:** direct Skill folder under `.agents/skills` or `$HOME/.agents/skills`.
- **ChatGPT Work:** plugin wrapper containing the same Skill under `skills/`.
- No MCP dependency is required for v1.0.0. Repository/filesystem access remains governed by the host and should be read-only for the candidate.

## 8. Claim boundary

Package self-tests only prove package structure and deterministic intake/report validation. Effective-load must still be verified on the actual target surface. RP-002 PASS/FAIL requires the actual frozen RP-002 evidence and is not asserted by this package.
