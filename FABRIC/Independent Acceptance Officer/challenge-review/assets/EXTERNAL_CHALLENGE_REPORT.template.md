# External Challenge Report — Deterministic Rendering Contract

Create the closed-schema `EXTERNAL_CHALLENGE_REPORT.json` first. Render the Markdown exactly as `scripts/verify_review_bundle.py::render_canonical_markdown` does, write its relative pointer and SHA-256 into the JSON, then validate:

```text
python scripts/verify_review_bundle.py --bundle-root <frozen-root> --intake <intake.json> --report <report.json>
```

The exact Markdown shape is:

````text
# External Challenge Report

- Verdict: `<verdict>`
- Claim ceiling: `<claim_ceiling>`
- Handoff: `<handoff>`

## Subject

```json
<compact unique-key subject JSON with sorted keys>
```

## Findings

```json
<compact findings JSON array with sorted object keys>
```

## Evidence edges

```json
<compact evidence-edge JSON array with sorted object keys>
```
````

Do not append free-form prose. Every detailed observation, predicate, impact, repair handoff, test count, and evidence mapping belongs in the closed JSON finding/edge fields and therefore appears in the deterministic rendering. A different verdict, extra authority claim, hidden nested field, duplicate edge, or rendering mismatch is invalid.

Claim ceiling remains local challenge only; the forbidden escalation tokens are never valid report content.
