# FDA 授權防護層設計（Lane C, 2026-08-15）— 設計知識庫 + Hermes 機制實證

**狀態：設計文件（read-only research 產出，未實作）。** 本檔是知識庫：後續實作 FDA
授權 gate（三條件防護）時直接引用，不必重推設計。引用時注意：方案尚未經 canary 驗證，
落地前必須跑「測試/驗證」節的冷啟動 canary。

## 需求（三條件防護）

除非以下任一成立，否則**嚴格禁止 Hermes 自動調用 FDA**：
1. 用戶指令明確提及使用 FDA；
2. 執行既有的已登記受治理路由（allowlist，如 SQS 以 FDA 操作 XQ 全球贏家）；
3. 任務執行必須使用 FDA 時 → 先暫停並主動詢問用戶取得明確授權。

## Hermes 機制實證（原始碼驗證 2026-08-15，勿當猜測）

路徑：`%LOCALAPPDATA%\hermes\hermes-agent\`（本機 `C:\Users\user\AppData\Local\hermes\hermes-agent\`）

### pre_tool_call hook（可 BLOCK 的攔截點）
- 定義：`config.yaml` 的 `hooks:` 區塊；格式見 `cli-config.yaml.example` L1560-1595。
- stdin JSON payload：`{tool_name, tool_input(args), session_id, parent_session_id, cwd, extra...}`
  （`agent/shell_hooks.py` L30-39、`_TOP_LEVEL_PAYLOAD_KEYS` L492）。
- 攔截方式：exit code 2（`BLOCK_EXIT_CODE`，Claude-Code 相容）或 stdout
  `{"action":"block","message":"..."}` / `{"decision":"block","reason":"..."}`。
- **`fail_closed: true`（config 內）→ hook 崩潰/超時/stdout 無法解析 = BLOCK**；
  預設 fail-open。僅 `pre_tool_call` 支援 blocking + fail_closed
  （`_BLOCKING_EVENTS` L173、L470-477）。
- matcher = tool_name 的 regex（如 `"terminal|computer_use|execute_code|delegate_task"`）；
  只對 pre/post_tool_call 生效（L425-432）。
- **看不到用戶 prompt**——只有 tool_name + tool_input + session_id。
- 註冊：`cli.py` L1036-1040 與 `gateway/run.py` L11385-11387 都呼叫
  `register_from_config` → process-wide → **子代理（delegate_task）與 cron 的
  tool call 也過同一 hook**（需 canary 實測確認）。
- 非 TTY（gateway/cron）需 `--accept-hooks` / `HERMES_ACCEPT_HOOKS=1` /
  `hooks_auto_accept: true`；首用 consent 存 `~/.hermes/shell-hooks-allowlist.json`。
- block message 會回到模型（post_tool_call status="blocked"）→ 模型看到原因 → 可執行「暫停+詢問」。

### pre_llm_call hook（唯一看得到用戶 prompt 的點）
- payload 含 `user_message`（原始用戶文字）、`conversation_history`、`session_id`、
  `turn_id`（`agent/turn_context.py` L1152-1168）。
- **不能 block**（matcher/blocking 只對 pre_tool_call）；但可寫 side-effect 檔
  （如 session-scoped 授權 token 檔）供 pre_tool_call guard 查詢。
- 用途：條件 1「用戶明確提及」的機械偵測 + mint token；條件 3 用戶回覆授權後 mint。

### approvals.deny（--yolo-proof 的硬封鎖）
- `config_defaults.py` L2135-2144：fnmatch globs 對 terminal 命令，**無條件封鎖，
  先於 --yolo / /yolo / mode=off bypass**。
- 用途：對「繞過 fda_run 直跑 var/fda 腳本」等模式加硬 deny 兜底。
- `approvals.cron_mode: deny` 預設 → cron 的 approval prompt 預設拒絕。
- 注意：approvals 只對「被判定 destructive 的 shell 命令」prompt；FDA 命令
  （`python fda_run.py ...`）通常不被判 destructive → **單靠 approvals 不夠**，
  主閘必須是 hook。

### 測試工具
- `hermes hooks list/test/doctor`（test = synthetic payload 實跑；doctor = exec bit/
  allowlist/mtime/JSON validity/synthetic timing）。
- `hermes approvals test`（dry-run verdict，不執行）；`hermes approvals suggest`。

## 方案比較（A/B/C/D，摘要）

| 方案 | 強制點 | 優點 | 缺點 |
|---|---|---|---|
| A | Hermes 外層 hook（pre_llm_call mint + pre_tool_call guard + approvals.deny） | 最外層、任何 tool call 都過、--yolo-proof、不依賴載 skill | 需 2 個唯讀腳本；hook 看不到 prompt（需 mint 機制） |
| B | fda_preflight.py 擴充 `--auth-token/--route-id`（執行路徑內閘） | 路徑內兜底，Step 9-0 相容，exit 0/2 契約不變 | 看不到 prompt，只驗 token 有效性；被繞過 preflight 則失效 |
| C | Skill HARD GATE 擴充（Step 9-0a）+ HGK WO 治理 route registry | 定義誰可註冊 route（WO + COV-11-06 人閘）、HITL 流程文件化 | 純 prose 強制力弱（2026-08-14 教訓：prose 規則被違反） |
| D | 多層組合：A 外 hook + B 內 preflight + registry + Step 9-0 擴充 | 防 prose 失效、--yolo-proof、雙層兜底、機制全現存 | 元件最多，需逐一 canary |

**推薦 D**：pre_llm_call mint（條件 1）→ pre_tool_call guard fail_closed（條件 2/3 +
嚴格禁止）→ fda_preflight 內閘複驗 → Step 9-0 擴充（擴充不取代，rule 1-6 保留）。

## FDA_ROUTE_REGISTRY.json（allowlist 設計）

新檔（放 matrix 旁，非 frozen），比照 matrix 治理：
```yaml
schema: FDA-ROUTE-REGISTRY/1
mutation_authority: ADMITTED_HGK_WORKORDER_ONLY
digest: <sha256>
routes:
  - route_id: ROUTE-SQS-XQ-GLOBALWINNER-001
    owner: SQS
    scope: "SQS 以 FDA 操作 XQ 全球贏家 (PAPER)"
    app: XQ
    action_classes: [XQ_LAUNCH_LOCATE, XQ_PAPER_CONFIG]
    allowed_scripts: ["**/fda_run.py", "**/screen_state_check.py"]
    binding_wo: WO-HGK-XXXX
    status: ACTIVE   # ACTIVE | REVOKED
    expires: 2026-12-31
```
變更只經 WO（admission→acceptance→digest→mirror）；guard/preflight 唯讀 + digest 驗證；
route 的 action_class 必須對應 matrix QUALIFIED row（matrix 仍是唯一路由真相）。

## 『明確提及』偵測（條件 1）

保守雙條件 regex（防誤放）：**意圖動詞**（用/操作/操控/開/執行/跑/建/啟用/允許/
授權/OK/可以）∧ **FDA 目標詞**（FDA/XQ/XQ全球贏家/策略雷達/PAPER/screen_state_check/
fda_run）。只提「XQ」無動詞 → 不 mint。mint 產物：session-scoped token 檔
（含 turn_id、minted_at、TTL、matched_text、hash）。

## 攔截行為

- 無 token 且無 route → **BLOCK + 報告**（hook exit 2 / preflight exit 2 with
  `no_authorization`）；block message 指引「暫停並詢問用戶」→ 用戶回覆授權 →
  下一 turn pre_llm_call mint → 重試通過（條件 3 的機械化 HITL）。
- approvals.deny 模式 → 無條件 BLOCK（含 --yolo）。

## 測試/驗證（落地前必跑）

1. `hermes hooks test pre_tool_call` synthetic payload：無 token FDA 命令→BLOCK；
   有效 token→PASS；ACTIVE route→PASS；REVOKED/過期→BLOCK。
2. `hermes hooks doctor`；`hermes approvals test`（deny 模式生效證明）。
3. preflight 3-state：token 有/無/過期；route ACTIVE/REVOKED；matrix row 缺失→fail-closed。
4. **冷啟動 canary**（比照 HGK Step 8）：fresh `delegate_task` leaf 只給 SKILL.md +
   repo root → 首 FDA 動作必須被 BLOCK（無授權）或走授權 preflight；再驗證
   子代理/cron 的 tool call 確實過 hook。
5. **--yolo 測試**：`--yolo` 下 hook + deny 仍生效（deny 原始碼保證，hook 需實測）。
6. 新 gate 腳本自身過 `fda_script_guard`（零 install/download/mouse）+ 執行前後
   hash 證明唯讀。

## 硬性約束（設計時已確認，實作時勿違反）

- FDA 操作禁搶滑鼠/前景輸入/安裝工具（fda-desktop-automation §1.2 零滑鼠硬路由）。
- 新 gate 本身不得有 install/download 能力（stdlib-only、無 subprocess 到套件管理器）。
- 不得修改 frozen assets：FDA_IMPLEMENTATION_EVIDENCE.md、matrix QUALIFIED 狀態、
  independent_checker.py（改 denominator 會斷 manifest/hash 鏈）。
- Step 9-0 相容：新 gate 是 Step 9-0 的**擴充**（加授權子步），非取代。
