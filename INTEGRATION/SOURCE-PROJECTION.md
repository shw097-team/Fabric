# SOURCE → PROJECTION relationship

This repository is a **projection**, not an authority. `HG-KSEOS` is the sole control plane; current
canonical Hermes is bound as its governed Runtime/Orchestration Plane.

| mirror folder | subject | local source root | publication rule |
|---|---|---|---|
| `HG-KSEOS/` | control plane: spine, contracts, typed lifecycle, evidence | `C:/Projects/Agent_Workspace/HG-KSEOS` | control-plane artifacts and evidence that are already non-credential |
| `FABRIC/` | governance contract and the research/automation trees | `C:/Projects/Agent_Workspace/Fabric` | governance docs, contracts, skills, methods |
| `FAR/` | research product: contracts, routing, retrieval | `C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research` | research-product sources and their contracts |
| `DESKTOP/` | desktop-effect plane: docs, skills, guards | `C:/Projects/Agent_Workspace/Fabric/fabric-desktop-automation` | docs, skills and guards; runtime state is NOT an approved payload |

**There is no fast-forward relationship.** The projection prefixes paths with uppercase subject
folders, so mirror and local paths never coincide; a mirror refresh is a governed re-publication by
scope, never a `git pull`/`push` of a working tree.

Measured at 2026-10-13T11:50:38.128148+00:00: local Fabric tracked files 832; mirror blobs 1994; path overlap 0.

**Known limitation, stated not hidden:** the procedure that produced the previous publication was not
found anywhere inside the four source trees. Until a builder exists in-repo, a refresh is performed
by an explicit, reviewed change-set such as this one, and this document is that procedure's record.
