# FDA guardrail operations（2026-08-15, WO-HGK-FDA-GUARD-IMPL-001 + WO-SQS-FDA-XQ-ROUTE-001）

`references/fda-guardrail-runtime-notes.md` 的姊妹檔：hook 生命週期與 route registry 生命週期的實戰細節（該檔覆蓋 wire format / config-set 陷阱 / redaction 幻影；本檔覆蓋操作層）。

## 1. Hook 生命週期：何時生效、如何判定

- Hooks 只在 **process 啟動時**從 config.yaml 載入；`hermes config set` 後，既有 session 不生效。
- **桌面 UI 重啟 ≠ backend 重啟（2026-08-15 實證）**：用戶重啟 Hermes 桌面後，既有 conversation 的 backend process 仍以舊 config 運行（`ls var/fda` 照常放行，無 mint token 產生）。
- 判定「本 process 是否已載入 hooks」的三段證據（依可靠度）：
  1. `agent.log` 的 `shell hook registered: pre_tool_call -> ...` 時間戳 > process 啟動時刻（最可靠）
  2. 實測 marker 命令（含 `var/fda` 字樣）是否被擋
  3. `hermes hooks list` 顯示 `✓ allowed`（只證明 config+allowlist 就緒，**不證明** process 已載入）
- 要生效：真正重啟 backend（關掉整個 app 讓 process 重生）或開新 session。新 process 已實證生效（冷啟動 canary 兩例）。

## 2. Route registry（FDA_ROUTE_REGISTRY.json）生命週期

**digest 公式**（AO 重算驗證過，唯一吻合形式）：`sha256(json.dumps(移除 digest 欄後的 dict, ensure_ascii=False, sort_keys=True, indent=2))`。

**新增 route 程序**（WO 授權下）：
1. **spine 先 admission**：binding_wo 必須已存在於 shared-spine `workorders` 表（AO G1 教訓——歷史 WO 若只有文件無 DB 記錄，不能當 binding；該 route 應移除或改綁有 DB 記錄的 WO）
2. registry 加條目：只加、不改舊條目；`mutation_authority: ADMITTED_HGK_WORKORDER_ONLY`
3. digest 重算 + 自驗
4. 綁定方（SQS/FABRIC）側文件：adapter yaml（scope/action_classes/allowed_scripts/NO-LIVE-WRITE 邊界/HITL 門）+ DOC
5. 親跑驗證：`fda_preflight.py --action-class <X> --route-id <ID>` → exit 0 source=route；hook 直接餵 stdin 同 route-id → exit 0

**移除 route**：在 `note` 留 `removed ... (AO Gx)` 審計文字（優於乾淨刪除；AO 複核接受審計軌跡）。

**現有 routes（2026-08-15）**：ROUTE-WO-FDA-001（FABRIC）、ROUTE-WO-FDA-GUARD-IMPL-001（HGK）、ROUTE-SQS-XQ-GLOBALWINNER-001（SQS, PAPER/SHADOW read-only+config, NO-LIVE-WRITE, ACTIVE_POSITION 需 HUMAN_ENTRY_APPROVAL）。

## 3. 驗證快速參考

```bash
# 真實 pipeline 驗證 hook（synthetic payload 走同一 _serialize_payload 路徑）
hermes hooks test pre_tool_call --payload-file <json>   # 檔內 {tool_name, args, session_id}
hermes hooks test pre_llm_call --payload-file <json>    # 檔內 {session_id, user_message, ...}
hermes hooks doctor
hermes approvals test -- "<command>"                    # deny/allow 乾跑（含 deny 向量）
# hook 直接測（不經 pipeline）：python fda_guard_hook.py，stdin 用 tool_input/extra wire shape
```
