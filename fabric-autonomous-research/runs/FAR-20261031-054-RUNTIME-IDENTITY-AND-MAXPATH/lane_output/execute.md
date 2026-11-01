I’m treating the linked brief as the requested execution target. I’ll read it with the required HGK and Fabric operating instructions first, then establish the governed execution path and evidence before changing anything.
The brief is deliberately self-contained and requires exactly one work package. I’ve taken the plan’s durable repair as that package: relocate/recreate the lease-managed environment at a governed short path, with the recovery-forwarder cleanup kept outside this package and the shadow-vendor approach rejected. I’ll encode the decision, acceptance tests, rollback, and falsifiers in one artifact.
The single work package is written. I’m doing a narrow readback of that generated artifact only—checking the nonce, package count, path/status markers, and digest—so the handoff is concrete without sending this execution lane back through the repository.
NONCE-ECHO: FAR-EXECUTE-5F2F3930

Produced exactly one work package in [execute.md](C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research/runs/FAR-20261031-054-RUNTIME-IDENTITY-AND-MAXPATH/lane_output/execute.md).

It adopts **(b)**: rebuild the lease-managed environment under a governed short path. The package includes the 240-character safety margin, preservation of dependency identities and lease controls, positive/negative/boundary tests, atomic switching, rollback, evidence requirements, and explicit falsifiers. It keeps recovery-forwarder retirement as a separate cleanup and rejects a shadowed `openai` package.

Structural validation confirmed the nonce, exactly one work package, required sections, and status marker. SHA-256: `1f8b5b17b6ac77247e9f6e746b8a270d0ccf938a1557aff7927f36651e8dbfaf`.

No implementation or governed acceptance is claimed; the artifact remains `CANDIDATE_READY_NOT_IMPLEMENTED` pending controlled reproduction and independent verification.