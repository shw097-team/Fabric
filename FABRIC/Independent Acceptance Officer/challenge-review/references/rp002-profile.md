# RP-002 External Challenge Profile

This profile specializes the generic reviewer without transferring Fabric, Internal Oracle, domain, release, or production authority.

## Default checkpoints

| Gate | External challenge purpose |
|---|---|
| `O1` | Qualify Internal Oracle materialization/promotion and its deterministic false-positive defenses. |
| `F1` | Challenge Fabric self-hosting cutover, fallback, rollback, replay, and maker/checker separation. |
| `E1` | Challenge cross-stack engineering evolution and affected regression. |
| `E2` | Challenge behavioral-artifact evolution and runtime evidence. |
| `E3` | When applicable, challenge Oracle evolution without letting the evolved Oracle self-approve. |
| `R1` | Challenge final aggregate local acceptance, package identity, checksums, and readback. |

Also trigger on serious Internal Oracle disagreement or explicit escalation. Do not become a second Oracle at every ordinary gate. After O1, the Internal Oracle remains the primary operational checker.

Require the frozen RP-002 candidate, canonical gate IDs/acceptance predicates, raw Evidence Manifest, Internal Oracle identity/receipt, rollback/replay, and package evidence applicable to the selected checkpoint. This profile cannot establish `RP002_PASS`; it only guides an external challenge of a separately supplied subject.
