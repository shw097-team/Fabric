# Cross-session upgrade integrity: reconcile, verify survival, fix status markers

> Consolidated 2026-08-15 from two parallel drafts (same 2026-08-14 event: this-session
> FDA U1-U5 vs other-session RR6-RR8):
> [I] = `parallel-session-upgrade-integrity.md` (English) · [R] = `cross-session-upgrade-reconciliation.md` (中文)
> Both verified 2026-08-14. Merged per UD-FDA-RECIPE-MERGE-2026-08-15-001; originals deleted
> (zero references in tree at merge time — this file is the single canonical entry).

## 當用 (When to use) — [I] + [R] + [NEW]

- 用戶問「另一 session 的升級是否覆蓋/倒退了我的升級？」（是否被整合保留? 還是被覆蓋造成升級倒退?）
- 你完成升級後，發現另一 session 在同域（skill references / FDA tree / kanban board / spine）有寫入
- challenge/re-review 對 *status claim*（非實質）判 FAIL（D1/B1 兩次 FAIL_CHALLENGE 皆是）
- **[NEW] 與 Step 10A 掛鉤**：任何 upgrade/patch/self-evolution 提案通過 FAR research gate 前後，
  或執行中遇到 patch 工具「file modified since last read」警訊時，先跑本方法。

## 1. 盤點：另一 session 改了什麼（唯讀） — [R] 主幹 + [I]§2.1-2.2 補強

1. **git log 建立時間軸**：`git log --format="%h %ad %s" --date=format:"%m-%d %H:%M" -N -- <path>/`
   逐 commit 讀 message（其他 session 的 message 通常自帶 closure 狀態與驗證數字）。[R]
2. **每 commit 內容**：`git show --stat --format="%s" <hash>` — 檔案清單即升級範圍。[R]
3. **關鍵檔案 diff**：`git diff <系列前 commit>..HEAD -- <file>`；確認「系列前」的 parent
   （commit 順序：git log 最新在前，被列的後者較舊）。[R]
4. **receipts 讀 verdict**：`ls -la` 看 mtime（可反推實際工作窗：receipt 產生時間可能早於
   commit 時間）；用 python json 抽 verdict/pass_count/exit 等欄位。[R]
5. **skill 層比對**：對 SKILL.md grep 新系列關鍵字（RR6|RR7|…|194），確認對方有沒有動
   skill；比對 references/ 下同名工具的 mtime 與內容（diff 兩份副本）。[R]
6. **發現手段（補強）**：`find <references-dir> -newermt '<你的最後寫入時間>' -type f` → 新檔案；
   `sha256sum` 快照自己建立的檔案（mtime 是首個 drift 訊號）；grep 共享 skill/reference 的 token。[I]

## 2. 關係分類證據標準 — [R] + [I]§2.4 整合

- **衝突**：同一檔案兩邊都改、同一 invariants 被推翻。實例：無。[R]
- **互補**：檔案層零重疊（一方只動 repo 樹、另一方只動 skill references），或兩個工具
  管不同 concern 且互不引用。實例：fda_preflight.py（路由/資產 gate）vs 違規 API 源碼掃描 guard — 互補不重複。[R]
- **取代/重複**：一方明確引用或覆寫另一方。[R]
- **Do-NOT 字面 vs 精神**：對方改了本 session Do-NOT 列過的檔案時，看改法 —
  bug fix（不新增 T-code）符合精神，新增檢查類型才是違背。[R]
- **雙工具碰撞分類**：兩支同名工具（如雙「PREFLIGHT」）可能是正交的——依序分類：
  duplicate（重複）? complementary（互補，各管一 concern）? naming-confusion（命名誤導）?
  sequence gap（SKILL.md step list 漏掉其一）? dual-copy（同檔兩處、無漂移保護）?[I]

## 3. 完整性檢查：你的升級是否存活（per-item verdicts） — [I]§2.3

1. **快照自己的檔案**：`ls -la --time-style=full-iso <file>` + `sha256sum` 每個你建立的 artifact
   （mtime 是第一個 drift 訊號——你的寫入時間 vs 現在）。[I]
2. **盤點其他 session 的寫入**：find -newermt / git log / git status / grep token（見 §1）。[I]
3. **逐 item verdict**：PRESERVED / OVERWRITTEN / REGRESSED / PARTIAL，每項附證據
   （path + line + mtime）；**實際執行 artifact 證明 preserved 為真**
   （例如跑 preflight script → route=CUA、exit 0），不只靠文字。[I]
4. **denominator 成長 ≠ 新檢查**：checker 179→194 不是新檢查——T100 是 data-driven
   （每 evidence 樹檔一 check），唯一程式碼變更是 duplicate-ID fix。用 `git diff` 驗證
   是否新增 T-code，再報告真實原因。[I][R]

## 4. Status-marker discipline（D1/B1 教訓 — 兩次皆 FAIL_CHALLENGE） — [I]§1

- **D1（宣稱未施工，實已施工）**：research MD 說「未施工」而平行 session 已落地部分方案
  （U4 prose fix、SKILL.md §17 + Step 10A rule 3）。challenge lane 讀磁碟，不讀 MD。
- **B1（宣稱 DONE，實未 done）**：v2 說「D7/D9 closed」（12a/12b 正名、stale 數字清理）
  但磁碟上雙 `## 12` 標題與 `173/173`/`64/64` 殘留仍在。同類錯誤、相反方向。

規則：
1. **claimed status 必須等於 claim 當下的磁碟 bytes**：re-read + re-hash 後才可斷言 done 或 not done。
2. **patch 工具警告「file modified since last read」→ STOP 並重讀**：該警告就是平行 session 訊號，
   視為強制 re-verify 而非 shrug（本 session 出現 2 次：SKILL.md + cua.md）。
3. **不得在 prose 標 CLOSED 卻不列入 pending list**：B1 的傷害是靜默流失——D7/D9 宣稱 closed
   未列 pending，HITL 批准會漏掉它們。
4. **修 MD（bump version v1→v2→v3 + closure table），不爭 verdict**：reviewer 接受誠實的狀態修正，
   失敗的是 stale claim。

## 5. HITL 回應選項表 — [I]§3

| Option | Content | Cost | Risk | Frozen impact |
|---|---|---|---|---|
| A: Integrate | merge guard logic into main preflight as subcommand, single entry | medium | medium (retest) | HIGH (touches verified asset) |
| B: Divide roles | keep both, SKILL.md Step 9-0 gains two-phase sequence: ① env preflight → ② new/edited script passes guard → ③ execute; annotate dual copies | low (text patch) | low | zero |
| C: Record only | report documents the risk, close nothing | very low | zero | zero (risk open) |
| D: Rename (combo w/ B) | e.g. FDA_PREFLIGHT_GUARD.py → fda_script_guard.py, sync refs | low-med | low-med | zero (not the frozen asset) |

Recommendation pattern: **B (+D optional)** when tools are orthogonal and preserved —
structural integration (A) of a verified gate is usually not worth it.[I]

## 5b. [NEW] 施工細節補齊：D 改名同步逐步程序（verified 2026-08-14, fda_script_guard.py）

1. 先記錄原始身份：`sha256sum` 雙副本（改名後內容零變更時 hash 應等於原始，除非 docstring 加註）。
2. `mv` 兩副本（references/ + var/fda/），確認 size 不變。
3. 列出全部引用點：grep -rn 舊檔名 於 skill references、SKILL.md、var/fda/ 所有 .py/.md。
   分類：**工具碼（.py）引用必須同步**（否則執行壞）；**歷史文件（.md）提到舊名保留原樣**（原意供查閱）。
4. 逐引用更新：Python str.replace（不用 sed——replacement 含 `|`/反斜線會壞）。
5. guard 自身 docstring 加註「(formerly OLD_NAME)」保留原意。
6. 驗證：grep 舊名於所有工具碼 = 0；`python <guard> <clean-script>` exit 0、no-arg exit 2（usage）。
7. 收尾：施工 receipt 記錄 original_identity（舊名/原 sha256/原意全文）。

## 5c. [NEW] 施工細節補齊：B 兩階段序列補丁執行序列（verified 2026-08-14, SKILL.md Step 9-0）

1. 階段一：在 Step 9-0 規則 1（環境 preflight）後插入新規則 2（新/改腳本過 guard），
   後續規則編號順延（3→4→5→6）。
2. **中間 byte 驗證 gate**：插入後立即讀取該段，確認 (a) 路徑無 CRLF 斷行（見 §6 CRLF 陷阱）、
   (b) 編號 1-6 連續無重複。
3. 階段二：若插入時用了省略路徑（`…\skills\...`）→ 補成完整路徑。
4. 回滾條件：frontmatter 解析失敗 或 Step 9-0 標題消失 → 立即回滾（從備份/重讀現況恢復）。
5. 驗證：`python -c "import yaml; yaml.safe_load(SKILL.md frontmatter)"` + 規則編號 regex 1-6 連續
   + grep 新工具檔名引用 ≥2。

## 6. Pitfalls（合併去重） — [R] + [I]§5 + [NEW]

- **不要靜態 grep 數檢查數**：`check("T...` 只數得到 ~57 個（f-string/動態 ID 不算），
  實際跑起來是 184-194。以 receipts 的 verdict/total 欄位為準。[R]
- **別信 receipt 單一欄位**：FDA_CHECKER_179_RAW_RECEIPT_RR6.json 檔名寫 179、stdout 寫 184、
  total_checks 欄位寫 98 — 內部不一致；交叉看 stdout_full。[R]
- **大 bash 一行迴圈會被 hardline blocklist 擋**（for + $(git show …) 命令替換）：
  拆成小指令逐 commit 跑，或只用 `git show <hash>:<path>` 單一檔案。[R]
- **commit 時間 ≠ receipt 產生時間**：RR6 receipts mtime 11:48-14:09 早於 commit 14:12 —
  工作窗要從 receipts mtime 重建。[R]
- **CRLF patch 路徑斷行陷阱**（Step 9-0 插入實證）：長 `C:\Users\...` 路徑插入 CRLF 檔時
  patch 工具可能把路徑斷在 CRLF 邊界（`references` → `re` + CRLF + `eferences`），
  fuzzy matcher 會持續 re-match 壞序列，3+ 次 patch 重試同樣失敗甚至更糟。[I]
  - 同一字串不要重複 patch，第二次失敗即停。[I]
  - 用 Python bytes-level replace 修一次：write_file 寫小 fix script
    （`raw = open(p,'rb').read(); raw.replace(old_bytes, new_bytes)`），跑完刪除。
    Bytes replace 對 CRLF/LF 與跳脫免疫。[I]
  - 用 `repr()` 驗證目標行（CRLF 顯示為 `\r\n`），確認壞序列 count=0 再繼續。[I]
  - 任何 patch 共享檔後，byte-inspect 觸及行——工具 diff 可能顯示正確而磁碟 bytes 已斷。[I]
- **[NEW] 與 SKILL.md pitfalls 既有「Parallel-session skill-dir drift」的關係**：
  該條管施工前（查重複/併入既有檔，reuse-first），本檔管施工後（完整性驗證）——pre/post 一對。

## 7. 盤點實證（RR6-RR8 vs U1-U5, 2026-08-14） — [R]

- RR6-RR8 系列 6 commits（14:12-14:58）：62bfce0 RR6 repair（F01 current 10/10、
  xq_native_adapter press_toolbar 修正、FDA_ASSET_REGISTRY.json）→ e1e3dec RR7-A
  （PAPER STOP post-stop readback 10/10）→ be576be RR7-D（checker T100 duplicate-ID fix）
  → 66cc1bd/44baf89 RR7 final（EvidenceManifest、checker 194/194）→ e7ec326 RR8 closure
  （PAPER STOP 三源 authority + manifest raw body 內嵌）。
- **checker 179→194 是 data-driven 不是新檢查**：T100_NOSECRET_{rel} 對 FDA 樹每個
  .md/.yaml/.json/.py 各發一 check，evidence 樹擴張（RR6/7/8 單一 MD + receipts）就漲。
  唯一程式碼變更是 be576be 的 ID 去重（f.name → relative path，+3/-2 行）。
- 外部 review 鏈：r8 report = PARTIAL_CHALLENGE / NOT_GRANTED（RR7-001/003 未閉、
  blocking gaps 2+1）→ RR8-A/RR8-B 修補閉合。
- SKILL.md 15:17 版本零 RR6/RR8 內容（grep=0）— 對方 session 沒動 skill。

## 附錄：Preflight gate 建構陷阱（fda_preflight.py, verified working） — [I]§4

- Matrix version strings carry a product prefix (`XQLite-3.20.02-260811`) — strip the
  prefix before matching `fda_router` keys.
- `fda_router.route()` looks up by a `(app, app_version, action_class)` tuple key INSIDE
  the dict it receives — wrap the provider map as `{key: match}`, do not pass the bare
  provider dict (returns BLOCKED otherwise).
- Three-state test: normal → exit 0 + expected route; simulated missing asset (rename
  the binary) → exit 2 BLOCKED; all action classes → consistent routes. Then prove
  read-only: hash the tracked tree before/after the preflight run, must be equal.
- Cold-start canary proves the SKILL.md trigger works: a fresh-context leaf given only
  the SKILL.md must make running preflight its FIRST action (verify the Step 9-0 text
  is load-bearing, not decorative).
