# FDA Guardrail runtime notes（WO-HGK-FDA-GUARD-IMPL-001, 2026-08-15）

本 WO 實戰發現的三個機制級教訓（皆已修入防護層本身，此檔為復用記錄）。

## 1. Hermes shell-hook wire format（真格式，docstring 過時）

`agent/shell_hooks.py _serialize_payload()`（L673-689）送出給 hook script 的 stdin JSON：

```json
{
  "hook_event_name": "pre_tool_call",
  "tool_name": "terminal",
  "tool_input": { "...args dict..." },     // ← key 是 tool_input，不是 args！
  "session_id": "...",
  "cwd": "...",
  "extra": { "...非 top-level kwargs..." }  // pre_llm_call 的 user_message/conversation_history/turn_id 都在這裡
}
```

- `_TOP_LEVEL_PAYLOAD_KEYS = {tool_name, args, session_id, parent_session_id}`；`args`（若非 dict）不會進 tool_input。
- 教訓：hook script 開頭必須 `extra` 合併進 data + `tool_input`→`args` 別名（見 fda_guard_hook.py main() 起手式）。
- 驗證工具：`hermes hooks test <event> --payload-file <json>`（合併進 synthetic payload）+ `hermes hooks doctor`。

## 2. `hermes config set` 的 list 陷阱（FDA-GUARD-CONFIG-001）

`hermes config set approvals.deny '["a","b"]'` 會把值存成 **YAML 單引號字串**（非 list）！
approvals 程式對字串做 `for p in deny_patterns`（迭代**字元**）→ 字元 `*` 變成 match-all rule →
**所有 terminal 命令被硬擋**（連修復指令都擋，需用戶授權 execute_code 修復）。

修復：直接以正確 YAML list 寫入（見下），並用 `yaml.safe_load` 驗證 `isinstance(list)`。

```yaml
approvals:
  deny:
    - "*quarantined_violations*"
    - "*cua-driver*foreground*"
```

同理 `hooks.pre_llm_call` 等 list-of-dict 值。

## 3. 輸出層 secret redaction 的 `***` 幻影（CODEX-SPAWN3-FALSECLAIM-001 / AO G3）

Hermes 工具**輸出**層會把看似 secret 的片段遮罩成 `***`（例如 `{authz['reason']}` 相關 pattern）。
症狀：read_file / execute_code stdout / terminal 顯示 `no_authorization:***`，但檔案真實位元組是正確的
`no_authorization:{authz['reason']}`。曾造成：誤判 Codex 寫壞（其實寫對）、誤判 patch 沒生效（其實生效）、
AO 誤判 L219 缺陷（實為假象）。

**驗證鐵則**：內容正確性一律用 byte-level（`open(rb)` / hex dump / `sha256(實際字串)==sha256(期望字串)`）比對，
不要信任 read_file/terminal 的顯示。`hermes config set security.redact_secrets false` 可關（重啟生效）——但別關，
只要習慣用 hash/hex 驗證。

## 4. 防護層運作速查（Step 9-0a 機械面）

- mint：`references/fda_guard_mint.py`（pre_llm_call，雙條件 regex：意圖動詞 ∧ FDA 目標詞；寫 `~/.hermes/var/fda-auth/<session_id>.json`，TTL 1h）
- guard：`references/fda_guard_hook.py`（pre_tool_call，fail_closed:true，matcher=terminal|computer_use|execute_code|delegate_task|write_file|patch；無 token/route → exit 2 + block JSON）
- allowlist：`references/FDA_ROUTE_REGISTRY.json`（WO-only mutation + digest；binding_wo 必須存在於 spine workorders）
- preflight：`--route-id`/`--auth-token`；`--action-class` 無授權 → exit 2 `no_authorization:<reason>`；`--check-assets`/`--list` 診斷免授權
- deny：`*quarantined_violations*`、`*cua-driver*foreground*`、`*cua-driver*bring_to_front*`（勿加 `*python*var/fda/*`——誤擋合法 fda_run 路由）
- **新 session/process 才生效**（hooks 啟動時讀 config）；現有 session 需重啟。

## 4b. mint 刷新守衛缺陷（2026-10-07 實證；載入副本已修，封裝副本待同步）

`fda_guard_mint.py` `_mint_token` 的單調性守衛缺陷確實存在：以字串比較 turn id
（`if existing_turn is not None and str(existing_turn) >= str(turn_id): return`）；
既有 token 已過期時，排序較低的新 turn id（含使用者新的授權訊息）將無法刷新 token，
症狀為「使用者已授權、閘門仍持續 deny，且重試無效」。
經驗證：實際載入的 mint 腳本是 live `config.yaml` `pre_llm_call` 所註冊的 legacy 路徑，
且該載入副本已帶修補——早期 `return` 已改為「僅在既有 token 仍有效時才 return」。
封裝（packaged）副本的同一腳本目前仍是修補前的舊版；在 S3 同步它之前，該副本維持 stale。
以 Step 9-0a、實際 hook 與受治理登錄為唯一規則來源；本節不授權操作。

## 5. Hook 驗證配方（2026-08-15 實戰：功能測試全 PASS 但真實 pipeline 全 no-op）

**核心陷阱**：直接餵 stdin 的功能測試（自己構造 payload）可能 10/10 PASS，但真實 pipeline 收到的是
`_serialize_payload` 改寫後的 shape（`tool_input` + `extra`，見 §1）→ hook 讀錯 key → 判定「非相關」→
**永不觸發**。本 WO 的 E2E canary 就是靠這個抓到的（FDA-GUARD-PAYLOAD-001）。所以：

1. **功能測試（自餵 payload）只能驗證邏輯，不能驗證整合**。整合必須走真實 pipeline：
   - `hermes hooks test <event> --payload-file <json>`（實測含 tool_input 的 block/route/mint 三路徑）
   - `hermes hooks doctor`（註冊健康：script 存在/allowlisted/exit 0）
   - 要驗「block」輸出被 Hermes 正確解析：看 hooks test 的 `exit 2` + block JSON 是否被 wire 化
2. **冷啟動 canary（fresh process 端到端）**：`hermes chat -q "<prompt>" --provider opencode-go -m <model>`
   是全新 process → hooks 會載入。設計陷阱：測 **BLOCK 路徑**的 prompt 不能含意圖動詞（use/run/用/執行…），
   否則 mint 先觸發（token 產生）→ 變成授權路徑；測 **MINT 路徑**則要含「用FDA」+目標詞。
   判讀：看 session transcript（state.db sessions/messages）的 tool result 是否出現 block JSON /
   token 檔是否產生（`~/.hermes/var/fda-auth/<session_id>.json`）。
3. **「目前 process 是否已載入 hooks」的快速驗證**：跑一個含 marker 的無害指令（如 `ls .../var/fda`），
   被擋 = 已載入；放行 = 未載入（config 是 process 啟動時讀的）。
4. **hooks 註冊是 per-process**：桌面 UI 重啟 ≠ backend 重啟（實測 session 仍是舊 process）——要驗
   agent.log 的 `shell hook registered` 時間戳 vs session 啟動時間。

## 6. 條件 2 路由登記程序（2026-08-15 實戰，WO-SQS-FDA-XQ-ROUTE-001）

用戶要「某受治理流程可用 FDA」= 在 `FDA_ROUTE_REGISTRY.json` 登記 ACTIVE route。程序：

1. **先 admission 綁定 WO**（AO G1 教訓：`binding_wo` 必須存在於 spine `workorders` 表——
   `WO-FDA-XQ-002` 文件在但從未入 spine → route 被 AO 判 FAIL 而移除）。順序：spine WO CREATED → 才寫 registry。
2. **registry 條目**：`route_id`（`ROUTE-<OWNER>-<SCOPE>-NNN`）/ owner / scope（含操作邊界：
   PAPER/read-only、NO-LIVE-WRITE、HITL 門）/ app / action_classes（只准 QUALIFIED matrix row）/
   allowed_scripts（fnmatch）/ binding_wo / binding_ref（SQS 側 adapter yaml）/ status=ACTIVE / expires。
3. **digest 重算**：`sha256(json.dumps(移除 digest 欄, ensure_ascii=False, sort_keys=True, indent=2))`。
4. **受治理方側文件**：adapter yaml（scope/action_classes/NO-LIVE-WRITE 邊界/HITL）+ DOC（用途/授權條件/
   操作邊界/查詢方式）；中文 UTF-8 驗證（無 U+FFFD）。
5. **親跑驗證**：`fda_preflight.py --action-class <CLASS> --route-id <ID>` → exit 0 source=route；
   hook 直接測（wire shape 見 §1）帶 route-id → exit 0；digest 重算一致；routes 數。
6. **AO 級審查**：binding 存在性 + digest 重算是必查項；舊條目「只加不改」，審計軌跡寫 note（additive）。
