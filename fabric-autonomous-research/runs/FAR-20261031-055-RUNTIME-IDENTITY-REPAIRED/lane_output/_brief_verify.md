NONCE-ECHO: FAR-VERIFY-A2AA7FBC

# VERIFY brief

Question:
On this Windows host the command 'hermes' on PATH resolves to D:\Hermes-Recovery\live22\bin\hermes, a recovery forwarder whose hermes.cmd sets HERMES_HOME=D:\Hermes-Recovery\live22. Any agent turn it starts fails with: RuntimeError: Failed to initialize OpenAI client: No module named 'openai.types.responses.response_computer_tool_call_output_screenshot_param'. The desktop product's own entry - <hermes-root>\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\python.exe -m hermes_cli.main, with HERMES_HOME pointing at the profile directory - answers a model turn in about 9 seconds. A controlled reproduction on this host copied the installed openai package (1048 .py files, one digest) to three roots: at a 125-character module path it imports; padded to 259 characters it imports; padded to 260 characters the same bytes fail with exactly the production error. The installed environment also ships 10 extension modules built for another CPython, so it cannot be imported by the 3.11 runtime even at a short path. Research the three candidate repairs - (a) retire the recovery forwarder and make the product CLI the only entry; (b) relocate or shorten the lease-managed environment so no module path reaches 260 characters; (c) vendor a short-path openai that shadows the broken one - and decide which repair a governed control plane must adopt, on evidence, naming what would falsify the decision.

PLAN output:
I’ll treat the linked `_brief_execute.md` as the governing brief. I’m starting with the repository instructions and the brief itself, then I’ll map its scope to the required execution and independent verification lanes before changing anything.
The brief is self-contained and explicitly limits this task to producing one work package at the named Fabric path. I’m drafting that package with the evidence, decision criteria, falsifiers, deterministic checks, and a single implementation scope, without inspecting further repository or governance material.
FAR-EXECUTE-58C20739

Created exactly one self-contained work package at [WORKPACKAGE.md](C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research/runs/FAR-20261031-055-RUNTIME-IDENTITY-REPAIRED/lane_output/WORKPACKAGE.md). It defines the repair decision, evidence requirements, verification probes, rollback proof, falsification conditions, and independent-checker completion criteria.

SHA-256: `ee75869ee90c71d0cc7a7e7c28493f652c9bf899176660267a0a2d78f6719a50`

Check the work against the question, not against the writer's summary. Decide PASS or FAIL and name what you relied on.

Begin your reply with the nonce line exactly as given above, verbatim.
