NONCE-ECHO: FAR-PLAN-C1D1E840

# PLAN brief

On this Windows host the command 'hermes' on PATH resolves to D:\Hermes-Recovery\live22\bin\hermes, a recovery forwarder whose hermes.cmd sets HERMES_HOME=D:\Hermes-Recovery\live22. Any agent turn it starts fails with: RuntimeError: Failed to initialize OpenAI client: No module named 'openai.types.responses.response_computer_tool_call_output_screenshot_param'. The desktop product's own entry - <hermes-root>\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\python.exe -m hermes_cli.main, with HERMES_HOME pointing at the profile directory - answers a model turn in about 9 seconds. A controlled reproduction on this host copied the installed openai package (1048 .py files, one digest) to three roots: at a 125-character module path it imports; padded to 259 characters it imports; padded to 260 characters the same bytes fail with exactly the production error. The installed environment also ships 10 extension modules built for another CPython, so it cannot be imported by the 3.11 runtime even at a short path. Research the three candidate repairs - (a) retire the recovery forwarder and make the product CLI the only entry; (b) relocate or shorten the lease-managed environment so no module path reaches 260 characters; (c) vendor a short-path openai that shadows the broken one - and decide which repair a governed control plane must adopt, on evidence, naming what would falsify the decision.

Answer as the planning lane: structure the problem, name what would have to be true, and say what the EXECUTE lane should build. Do not write code.

Begin your reply with the nonce line exactly as given above, verbatim.
