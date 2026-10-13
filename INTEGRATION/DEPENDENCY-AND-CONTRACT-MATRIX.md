# Dependency and contract matrix

| producer | consumer | dependency | contract artifact | mutation authority |
|---|---|---|---|---|
| Fabric | all subjects | governance contract, policy ownership | `FABRIC/AGENTS.md`, `FABRIC/contracts/` | policy owner |
| HG-KSEOS | all subjects | typed lifecycle, admission, evidence ledger | `HG-KSEOS/AGENTS.md`, spine schema | control plane, gate-typed only |
| canonical Hermes | HG-KSEOS | governed runtime/orchestration; lane dispatch, model routing | `HG-KSEOS/config/`, lane pool candidate | control plane; route registry is owner-gated |
| FAR | Fabric, HG-KSEOS | research product: source contracts, routing, retrieval | `FAR/` research-product contracts | FAR owner |
| desktop-effect plane | Fabric, HG-KSEOS | documented desktop procedures, guards, skills | `DESKTOP/` docs and skills | subject owner; live effect never claimed here |

Rules that hold across every edge: no subject may self-accept; no consumer may widen its own
authority; a gate that is not named is not passed; evidence travels with the claim.
