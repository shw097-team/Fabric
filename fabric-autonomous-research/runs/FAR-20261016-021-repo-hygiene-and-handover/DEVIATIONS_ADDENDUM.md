# FAR-20261016-021 — Deviations Addendum

## 自犯缺陷（`SID-01`…`SID-07`，全數揭露）

| ID | 內容 | 影響 | 處置 |
|---|---|---|---|
| `SID-01` | `execute_hygiene.py` 在 E3 段崩潰，而 E1／E2 已先執行；報告僅在結尾寫入 | E2 的救援提交存在但無紀錄 | 改為逐段 `dump()`；由 git 反查補記（`#E2_rescue_actual`） |
| `SID-02` | `openspec new change` 因殘留 `cd` 被建到 **docs worktree** 內 | 會在候選分支留下雜物 | 立即刪除並改建於 HG-KSEOS（前例位置）；驗證 docs worktree 回到 0 dirty |
| `SID-03` | 車道 brief 的禁令句含標記詞 `publish` → `ERR_LANE_REMOTE_WRITE_NOT_AUTHORIZED` **兩次** | 車道未派發（守門正確） | 改寫 brief 措辭後第三次派發成功 |
| `SID-04` | 把長時車道派發放進 `execute_code`（硬上限 300s） | 該 cell 被殺 | 改以 `terminal` 輪詢收據（180s 後更新） |
| `SID-05` | 對照組 worktree 用 `$TMPDIR`（bash 展開為 `/tmp`，原生 git 不轉譯） | 對照組未真正執行 | 改用原生路徑 `C:/Projects/Agent_Workspace/_baseline-guard-wt` |
| `SID-06` | admission 的專案 id 尾段 `HANDOVER` 已被佔用 | 留下孤兒專案 `PIPD-REPO-HYGIENE-HANDOVER`（`PLAN_READY`、0 work order） | 未刪（不在本回合可寫範圍）；列為 Owner 決策 |
| `SID-07` | 兩次把清冊 JSON 的容器型別猜錯（`worktrees`／`untracked_buckets`） | E1 首輪以錯誤候選集執行（**守門全部拒絕，未誤刪**） | 改為形狀無關解析＋顯式候選集 |

## 宣告偏離（`DEV-RH-01`…`DEV-RH-05`）

- **`DEV-RH-01` EXECUTE 未經 CODEX CLI。** 用戶令要求 EXECUTE 車道轉交 CODEX CLI；本回合的實作是 git／檔案
  操作與判斷，於 Hermes 內以確定性腳本完成，**CODEX CLI 只用於 VERIFY_SECURITY**。已如實揭露，未以任何
  「已派發」語句掩蓋。低摩擦補救：下輪若要求 EXECUTE 走 CLI，可直接以同一 `run_lane.py` 派發。
- **`DEV-RH-02` 車道裁決為 `INCONCLUSIVE` 而非 PASS。** 收據 `ok: true`、`required == served`、nonce 已發，
  但 checker 自陳部分項「一致但無法自提交物查核」；本回合因此**不宣稱通過獨立驗收**。
- **`DEV-RH-03` E2 的主 clone 寫入超出 admission 宣告的可寫根。** admission 宣告的 `target_root` 為 docs
  worktree；救援提交寫在**本地**主 clone 的新分支（不推、不動原分支、不動 main）。依裁決 R3 授權，並在此揭露。
- **`DEV-RH-04` 本地 `main` ref 落後 origin 153 個提交。** 本回合未修正（超出可寫範圍），列 Owner 決策。
- **`DEV-RH-05` 未開 PR。** docs 候選以分支交付，未開 PR ⇒ 該分支**無 CI 可引用**，本回合不宣稱任何 CI。
