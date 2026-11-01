NONCE-ECHO: FAR-VERIFY-A463B9EE

# VERIFY brief

Question:
On this Windows host the command 'hermes' on PATH resolves to D:\Hermes-Recovery\live22\bin\hermes, a recovery forwarder whose hermes.cmd sets HERMES_HOME=D:\Hermes-Recovery\live22. Any agent turn it starts fails with: RuntimeError: Failed to initialize OpenAI client: No module named 'openai.types.responses.response_computer_tool_call_output_screenshot_param'. The desktop product's own entry - <hermes-root>\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\python.exe -m hermes_cli.main, with HERMES_HOME pointing at the profile directory - answers a model turn in about 9 seconds. Measured on disk: in the failing lease-managed environment (<hermes-root>\installs\<install>\environments\<env>\venv\Lib\site-packages\openai) the module openai/types/responses/response_computer_tool_call_output_screenshot_param.py sits at exactly 260 characters of full path and 10 openai modules in that tree are at or past 260 characters, while the Windows MAX_PATH limit is 259; the same file in the product venv is at 201 characters and imports cleanly. Research the three candidate repairs - (a) retire the recovery forwarder and make the product CLI the only entry; (b) relocate or shorten the lease-managed environment so no module path reaches 260 characters; (c) vendor a short-path openai that shadows the broken one - and decide which repair a governed control plane must adopt, on evidence, naming what would falsify the decision.

PLAN output:
I’m treating the linked brief as the requested execution target. I’ll read it with the required HGK and Fabric operating instructions first, then establish the governed execution path and evidence before changing anything.
The brief is deliberately self-contained and requires exactly one work package. I’ve taken the plan’s durable repair as that package: relocate/recreate the lease-managed environment at a governed short path, with the recovery-forwarder cleanup kept outside this package and the shadow-vendor approach rejected. I’ll encode the decision, acceptance tests, rollback, and falsifiers in one artifact.
The single work package is written. I’m doing a narrow readback of that generated artifact only—checking the nonce, package count, path/status markers, and digest—so the handoff is concrete without sending this execution lane back through the repository.
NONCE-ECHO: FAR-EXECUTE-5F2F3930

Produced exactly one work package in [execute.md](C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research/runs/FAR-20261031-054-RUNTIME-IDENTITY-AND-MAXPATH/lane_output/execute.md).

It adopts **(b)**: rebuild the lease-managed environment under a governed short path. The package includes the 240-character safety margin, preservation of dependency identities and lease controls, positive/negative/boundary tests, atomic switching, rollback, evidence requirements, and explicit falsifiers. It keeps recovery-forwarder retirement as a separate cleanup and rejects a shadowed `openai` package.

Structural validation confirmed the nonce, exactly one work package, required sections, and status marker. SHA-256: `1f8b5b17b6ac77247e9f6e746b8a270d0ccf938a1557aff7927f36651e8dbfaf`.

No implementation or governed acceptance is claimed; the artifact remains `CANDIDATE_READY_NOT_IMPLEMENTED` pending controlled reproduction and independent verification.

Check the work against the question, not against the writer's summary. Decide PASS or FAIL and name what you relied on.

Begin your reply with the nonce line exactly as given above, verbatim.
