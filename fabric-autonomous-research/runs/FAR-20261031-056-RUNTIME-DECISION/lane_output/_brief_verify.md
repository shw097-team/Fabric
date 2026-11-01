NONCE-ECHO: FAR-VERIFY-9D80D4D7

# VERIFY brief

Question:
On this Windows host the command 'hermes' on PATH resolves to D:\Hermes-Recovery\live22\bin\hermes, a recovery forwarder whose hermes.cmd sets HERMES_HOME=D:\Hermes-Recovery\live22. Any agent turn it starts fails with: RuntimeError: Failed to initialize OpenAI client: No module named 'openai.types.responses.response_computer_tool_call_output_screenshot_param'. The desktop product's own entry - <hermes-root>\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\python.exe -m hermes_cli.main, with HERMES_HOME pointing at the profile directory - answers a model turn in about 9 seconds. A controlled reproduction on this host copied the installed openai package (1048 .py files, one digest) to three roots: at a 125-character module path it imports; padded to 259 characters it imports; padded to 260 characters the same bytes fail with exactly the production error. The installed environment also ships 10 extension modules built for another CPython, so it cannot be imported by the 3.11 runtime even at a short path. Research the three candidate repairs - (a) retire the recovery forwarder and make the product CLI the only entry; (b) relocate or shorten the lease-managed environment so no module path reaches 260 characters; (c) vendor a short-path openai that shadows the broken one - and decide which repair a governed control plane must adopt, on evidence, naming what would falsify the decision.

PLAN output:
I’ll treat the linked brief as the execution input, first reading it and the minimal governing artifacts it names. I’ll keep the work scoped to the brief’s stated lane and evidence contract.
The evidence supports retiring the recovery entry: the product CLI has a successful model turn, while shortening the recovery environment cannot repair the recorded interpreter/extension-module mismatch. I’m writing that decision with explicit acceptance evidence and falsifiers, including the launcher-to-recovery forwarding issue.
NONCE-ECHO: FAR-EXECUTE-1DF97172

Created [WORKPACKAGE.md](C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research/runs/FAR-20261031-056-RUNTIME-DECISION/lane_output/WORKPACKAGE.md).

The document selects **repair (a)**: retire the recovery forwarder and make the product CLI the only supported entry point. It compares all three candidates, identifies the interpreter/ABI mismatch that defeats shortening or shadowing alone, specifies acceptance checks, and states evidence-based falsifiers.

SHA-256: `0818F9FB81679A37F69778D96774C314F7818BAE3F64D3C27092352819B9CFD5`

Check the work against the question, not against the writer's summary. Decide PASS or FAIL and name what you relied on.

Begin your reply with the nonce line exactly as given above, verbatim.
