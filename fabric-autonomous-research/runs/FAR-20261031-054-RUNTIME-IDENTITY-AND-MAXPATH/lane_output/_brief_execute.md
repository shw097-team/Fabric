NONCE-ECHO: FAR-EXECUTE-5F2F3930

# EXECUTE brief

Question:
On this Windows host the command 'hermes' on PATH resolves to D:\Hermes-Recovery\live22\bin\hermes, a recovery forwarder whose hermes.cmd sets HERMES_HOME=D:\Hermes-Recovery\live22. Any agent turn it starts fails with: RuntimeError: Failed to initialize OpenAI client: No module named 'openai.types.responses.response_computer_tool_call_output_screenshot_param'. The desktop product's own entry - <hermes-root>\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\python.exe -m hermes_cli.main, with HERMES_HOME pointing at the profile directory - answers a model turn in about 9 seconds. Measured on disk: in the failing lease-managed environment (<hermes-root>\installs\<install>\environments\<env>\venv\Lib\site-packages\openai) the module openai/types/responses/response_computer_tool_call_output_screenshot_param.py sits at exactly 260 characters of full path and 10 openai modules in that tree are at or past 260 characters, while the Windows MAX_PATH limit is 259; the same file in the product venv is at 201 characters and imports cleanly. Research the three candidate repairs - (a) retire the recovery forwarder and make the product CLI the only entry; (b) relocate or shorten the lease-managed environment so no module path reaches 260 characters; (c) vendor a short-path openai that shadows the broken one - and decide which repair a governed control plane must adopt, on evidence, naming what would falsify the decision.

PLAN output:
我會先讀取這份 brief，確認它要求的工作與治理邊界。
這個 run 已有 `--lane PLAN` 的啟動紀錄，但尚未看到完成 receipt。我會把 brief 中的量測視為待核實證據，並區分「修正 CLI 入口」與「修復受管理環境」兩個問題。
NONCE-ECHO: FAR-PLAN-3428C405

**Recommend (b) as the durable repair: rebuild the lease-managed environment under a shorter, governed path. Treat (a) as a separate entry-point cleanup, conditional on preserving the runtime controls. Reject (c) as the permanent design.** This recommendation is provisional until a controlled reproduction establishes causality.

The brief reports two distinct defects: `hermes` resolves to a recovery forwarder with a different `HERMES_HOME`, and the failing environment contains exceptionally long dependency paths. Making one invocation work does not establish that both defects are repaired.

I independently read [config/hermes.json](C:/Projects/Agent_Workspace/HG-KSEOS/config/hermes.json). It records unresolved runtime-tree ambiguity and several interpreter, installation, and profile identities. That supports requiring explicit runtime binding. I could not inspect the recovery forwarder because access was denied; the path lengths, import failure, and nine-second successful turn remain **brief-supplied observations**, not measurements reproduced here.

| Candidate | What must be true | Decision |
|---|---|---|
| **(a) Retire the recovery forwarder; use the product CLI** | The product entry must support the required profile, isolation, dependency provenance, lease lifecycle, receipts, and rollback. Governed consumers must resolve to that same approved identity. | Appropriate entry cleanup once equivalence is demonstrated. Desktop inference alone does not establish suitability for governed execution. |
| **(b) Shorten the managed environment** | The failure must follow path length with interpreter, dependency payload, and launch conditions held constant. The environment manager must support creation and renewal at the shorter location. | Preferred durable repair because it addresses the suspected defect while retai

Build exactly one work package from the plan. Do NOT read the repository and do not go looking for governance files -- everything you need is in this brief; measured, a build brief that sends the arm into the repo stalls past 600s, the same brief kept self-contained finishes in 14s. Report what you produced.

Begin your reply with the nonce line exactly as given above, verbatim.
