NONCE-ECHO: FAR-EXECUTE-58C20739

# EXECUTE brief

Question:
On this Windows host the command 'hermes' on PATH resolves to D:\Hermes-Recovery\live22\bin\hermes, a recovery forwarder whose hermes.cmd sets HERMES_HOME=D:\Hermes-Recovery\live22. Any agent turn it starts fails with: RuntimeError: Failed to initialize OpenAI client: No module named 'openai.types.responses.response_computer_tool_call_output_screenshot_param'. The desktop product's own entry - <hermes-root>\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\python.exe -m hermes_cli.main, with HERMES_HOME pointing at the profile directory - answers a model turn in about 9 seconds. A controlled reproduction on this host copied the installed openai package (1048 .py files, one digest) to three roots: at a 125-character module path it imports; padded to 259 characters it imports; padded to 260 characters the same bytes fail with exactly the production error. The installed environment also ships 10 extension modules built for another CPython, so it cannot be imported by the 3.11 runtime even at a short path. Research the three candidate repairs - (a) retire the recovery forwarder and make the product CLI the only entry; (b) relocate or shorten the lease-managed environment so no module path reaches 260 characters; (c) vendor a short-path openai that shadows the broken one - and decide which repair a governed control plane must adopt, on evidence, naming what would falsify the decision.

PLAN output:
I’ll read the brief and check what it asks for against the repository’s execution rules.
NONCE-ECHO: FAR-PLAN-C1D1E840

I read the brief. It requests an evidence-based comparison of three Hermes repairs, falsification criteria, and an EXECUTE handoff, with no code changes.

The repository’s [AGENTS.md](C:/Projects/Agent_Workspace/HG-KSEOS/AGENTS.md) requires: “PLAN work must be dispatched, not written by the assistant,” with a passing PLAN receipt for `openai-codex/gpt-6.1-sol`.

The existing dispatch log shows a PLAN start, but no completed receipt was present in the inspected run directory. This session’s filesystem is read-only, so I cannot complete a dispatch that writes its required evidence.

**Status: PLAN unfulfilled; no repair decision or acceptance claimed.** Completion requires the governed dispatcher to run in a write-enabled environment.

Build exactly one work package from the plan and WRITE IT TO THIS EXACT FILE: C:\Projects\Agent_Workspace\Fabric\fabric-autonomous-research\runs\FAR-20261031-055-RUNTIME-IDENTITY-REPAIRED\lane_output\WORKPACKAGE.md. Do NOT read the repository and do not go looking for governance files -- everything you need is in this brief; measured, a build brief that sends the arm into the repo stalls past 600s, the same brief kept self-contained finishes in 14s. Then report what you produced and that file's sha256.

Begin your reply with the nonce line exactly as given above, verbatim.
