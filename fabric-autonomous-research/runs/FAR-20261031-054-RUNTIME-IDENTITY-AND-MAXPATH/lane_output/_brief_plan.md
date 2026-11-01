NONCE-ECHO: FAR-PLAN-3428C405

# PLAN brief

On this Windows host the command 'hermes' on PATH resolves to D:\Hermes-Recovery\live22\bin\hermes, a recovery forwarder whose hermes.cmd sets HERMES_HOME=D:\Hermes-Recovery\live22. Any agent turn it starts fails with: RuntimeError: Failed to initialize OpenAI client: No module named 'openai.types.responses.response_computer_tool_call_output_screenshot_param'. The desktop product's own entry - <hermes-root>\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\python.exe -m hermes_cli.main, with HERMES_HOME pointing at the profile directory - answers a model turn in about 9 seconds. Measured on disk: in the failing lease-managed environment (<hermes-root>\installs\<install>\environments\<env>\venv\Lib\site-packages\openai) the module openai/types/responses/response_computer_tool_call_output_screenshot_param.py sits at exactly 260 characters of full path and 10 openai modules in that tree are at or past 260 characters, while the Windows MAX_PATH limit is 259; the same file in the product venv is at 201 characters and imports cleanly. Research the three candidate repairs - (a) retire the recovery forwarder and make the product CLI the only entry; (b) relocate or shorten the lease-managed environment so no module path reaches 260 characters; (c) vendor a short-path openai that shadows the broken one - and decide which repair a governed control plane must adopt, on evidence, naming what would falsify the decision.

Answer as the planning lane: structure the problem, name what would have to be true, and say what the EXECUTE lane should build. Do not write code.

Begin your reply with the nonce line exactly as given above, verbatim.
