NONCE-ECHO: FAR-EXECUTE-1DF97172

# EXECUTE brief

Question:
On this Windows host the command 'hermes' on PATH resolves to D:\Hermes-Recovery\live22\bin\hermes, a recovery forwarder whose hermes.cmd sets HERMES_HOME=D:\Hermes-Recovery\live22. Any agent turn it starts fails with: RuntimeError: Failed to initialize OpenAI client: No module named 'openai.types.responses.response_computer_tool_call_output_screenshot_param'. The desktop product's own entry - <hermes-root>\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\python.exe -m hermes_cli.main, with HERMES_HOME pointing at the profile directory - answers a model turn in about 9 seconds. A controlled reproduction on this host copied the installed openai package (1048 .py files, one digest) to three roots: at a 125-character module path it imports; padded to 259 characters it imports; padded to 260 characters the same bytes fail with exactly the production error. The installed environment also ships 10 extension modules built for another CPython, so it cannot be imported by the 3.11 runtime even at a short path. Research the three candidate repairs - (a) retire the recovery forwarder and make the product CLI the only entry; (b) relocate or shorten the lease-managed environment so no module path reaches 260 characters; (c) vendor a short-path openai that shadows the broken one - and decide which repair a governed control plane must adopt, on evidence, naming what would falsify the decision.

PLAN output:
我會先讀取這份 brief，確認它要求的工作與適用規範。
Brief 將路徑長度故障與 Python ABI 不相容列為兩個待處理問題。我也找到了本輪的 PLAN dispatch 啟動紀錄，但尚未看到完成 receipt；因此目前不能宣稱 PLAN lane 已通過證據閘門。我會繼續查閱本機原始證據，並清楚標示決策依據與未驗證部分。
目前可讀到的兩個 `hermes.cmd`，包括位於產品 `venv\Scripts` 下的那個，都會轉送到 recovery runtime，並覆寫 `HERMES_HOME`。這表示驗證不能只看 PATH 指向哪個檔案，還要檢查 launcher 內容與最終啟動的 interpreter。尚未重跑 brief 所述的匯入邊界與模型回合測試。
NONCE-ECHO: FAR-PLAN-81FACD98

**Recommend (b): rebuild the lease-managed environment at a governed short root, using dependencies compatible with its bound interpreter.** This is a conditional recommendation. Shortening the existing environment alone does not address ABI incompatibility.

The dispatched planning agent inspected the existing [controlled reproduction](C:/Projects/Agent_Workspace/HG-KSEOS/ops/session-20261031/FHS-ALLPASS-20261031/WP-FHS-12/MAXPATH_CONTROLLED_REPRO.json) and [reproduction script](C:/Projects/Agent_Workspace/HG-KSEOS/scripts/wp12_maxpath_controlled_repro.py). The artifact records the same Python-source payload importing at target-path lengths 125 and 259, then failing at 260 on the named screenshot module. It also records an installed-environment import failure involving `pydantic_core._pydantic_core`.

Those are recorded observations, not experiments rerun this turn. Their limits are material:

- The short-path reproduction still obtains other dependencies from the product venv; it does not qualify a complete replacement environment.
- The digest covers `.py` files, not complete distributions.
- The ABI scanner reports ten matches, exposes eight names, and does not test their imports. Their complete inventory and runtime necessity remain unverified.
- The artifact’s maker-produced `PASS` is not independent acceptance.

Current read-only launcher inspection adds an important finding: the first PATH-resolved `hermes.cmd` sits under the product’s `venv\Scripts`, but its contents forward to recovery and overwrite `HERMES_HOME`. Executable identity must therefore include launcher contents and the final i

Answer the question as the executing lane and WRITE THE ANSWER TO THIS EXACT FILE: C:\Projects\Agent_Workspace\Fabric\fabric-autonomous-research\runs\FAR-20261031-056-RUNTIME-DECISION\lane_output\WORKPACKAGE.md. Make the decision the question asks for, compare the candidates against the evidence stated in the brief, and name what would falsify your choice. A document that tells a future executor to decide, or that lists criteria without applying them, does not answer the question and will be failed by the checker. Do NOT read the repository: everything you need is in this brief (measured: a build brief that sends the arm into the repo stalls past 600s; the same brief kept self-contained finishes in under a minute). Then report what you produced and that file's sha256.

Begin your reply with the nonce line exactly as given above, verbatim.
