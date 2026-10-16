# FINDING — self-correction: an attempt-level field was reported as the lane's arm verdict

**Severity:** high for the packet's accuracy · **Status:** corrected in a follow-up commit · **Found by:** a delayed background completion notification, not by self-review

## The overstatement

The first publication (commit `20588c2`) said, in the README's lane-receipt table and in the residual list:

> `EXECUTE/BC1 | required arm opencode-go/deepseek-v4.1-flash | served arm opencode-go/deepseek-v4.1-flash | usage_receipt_ok True | TIMEOUT`
>
> *"The cause is turn SHAPING, not the arm: BC1/BG3 receipts show the mandated arm served with a matching usage receipt."*

The RETROSPECTIVE said the same thing in stronger form — *"both wedged turns show `required_arm == served_arm` with a matching usage receipt"* — and the CHECKPOINT said *"both wedged turns still show the mandated arm served."*

## What the artifacts actually say

BC1's `dispatch.json` carries two levels that disagree:

| level | ok | code | served_arm | usage_receipt_ok | rank |
|---|---|---|---|---|---|
| aggregate (the lane's verdict) | `false` | `ERR_LANE_ALL_ROUTES_EXHAUSTED` | **`null`** | **`false`** | **`null`** |
| attempt 1 | — | — | attribution `opencode-go/deepseek-v4.1-flash` | `true` | — |

The attempt-level `usage_provider`/`usage_model` and its own `usage_receipt_ok` name the mandated arm. The aggregate verdict — the field the arm-identity gate is actually about — is a failure with `served_arm: null`. BC2 has no receipt at all, so it supports no arm claim whatsoever.

The table generator's bug: it read `doc.get('served_arm') or a.get('transport_model')` and `a.get('usage_receipt_ok')`, so an attempt field was displayed under a column a reader would take as the lane's verdict.

## Corrected claim

- The arm-identity gate passed **only on BC3**.
- BC1 supports the **narrower** claim that the mandated arm was the one being used when it wedged — useful, but it is attribution, not a gate pass.
- BC2 supports nothing about the arm.

The turn-shaping conclusion of this round does not depend on the overstated version, which is exactly why it was easy to miss: the conclusion was right and the supporting sentence was not.

## Repairs

1. `README.md`'s table now shows `agg_*` columns (the lane's aggregate verdict) and `attempt_*` columns side by side, with `served_arm (agg)` rendering as `null` for BC1 rather than as the attempt's transport model.
2. `make_closure.py`'s receipt reader now names both levels explicitly and carries a `read_this_carefully` note stating that the gate is the aggregate, never the attempt field.
3. The residual text, the D13 interpretation, `RETROSPECTIVE.md`, `RETROSPECTIVE.json` and `CHECKPOINT.md` were corrected to the precise form.
4. This finding is published with the packet; the earlier commit stays in the branch history rather than being rewritten.

## Rule for future rounds

Quote the lane's **aggregate verdict** fields for any identity or receipt claim; a per-attempt attribution field answers a different question ("what was being used") than the gate answers ("did a turn complete while bound to the mandated arm"). When two levels of the same artifact can disagree, print both adjacent to each other — a reader who only sees one of them will believe it.
