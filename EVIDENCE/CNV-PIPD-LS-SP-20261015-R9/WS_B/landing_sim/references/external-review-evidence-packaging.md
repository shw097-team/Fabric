# External Review Evidence Packaging — 八輪外部驗收累積教訓 (FDA r1→r8, 2026-08-13..14)

外部 challenge review（r1 PARTIAL → r2/r6/r7 FAIL → r8 PARTIAL）反覆抓的 defect 分類與修法。
**任何要提交外部驗收的證據包（FDA/FAR/SQS 同規則），逐條檢查本清單。**

## 1. 單一證據檔鐵律（每輪都被 challenge 的點）

- **self-contained 單一 MD**：外部驗收官環境不可開 MEDIA/本地路徑 → 所有 raw body 全量內嵌。
- **宣告 SHA = reviewer 可重算的 SHA**（RR8 教訓）：
  - MD 內嵌 manifest 用 `json.dumps(man)` 重序列化 → **內嵌 body 的 SHA ≠ on-disk file 的 SHA**。
  - 宣告**內嵌 body 的 SHA**（reviewer 從 MD 抽出 JSON 重算必須 match），另註明 on-disk SHA 供交叉。
- **移除 self-hash 欄位**（RR6-005/RR7-004）：`this_file_sha256` 在 header 是 self-referential——bytes 一變就 mismatch。改由 sidecar `FDA_MIRROR_READBACK_*.json` 發布，且 sidecar 不得留 `<placeholder>`。
- **manifest 必須內嵌完整 raw JSON body**（RR8-002）：只寫 summary（entries/sha/subject）無法讓 reviewer 重算 entries/unique paths/hash。內嵌完整 body → reviewer 可 parse 驗證。

## 2. Checker 三鐵律（RR7-002/RR7-004 抓的）

- **chronology**：checker 必須在**所有 repair 完成後**跑——RR7 曾因 checker 早於 F06/F01/PAPER 三批證據被裁「不是 final Acceptance Officer」。
- **duplicate ID 修正**：`dir.rglob("*")` + `f"{name}"` 對同檔名不同路徑產生 duplicate ID（如 T100_NOSECRET 兩檔）→ **ID 用相對路徑**（`str(f.relative_to(root)).replace(os.sep, "_")`）。
- **single denominator**：actual records == declared total == unique IDs；failed=0 / errors=0 / exit=0 / VERIFY_ONLY / maker≠checker。
- **subject 綁定**：checker.subject_root == manifest.subject_root == final git HEAD（三向 exact match）。
- **no-proxy**：checker 全 PASS 不自動等於 domain semantics 獨立驗證（gate calibration）——checker 只證明它自己掃的 predicates。

## 3. Domain semantics 需 authority-bound（RR8-001）

外部 reviewer **不接受 candidate 自行解釋系統 internal state code**（如「state 3 / ExecState 5 = stopped terminal」），
即使有 raw DB 證據。修法：**三源交叉 authority**：
1. 社群/社區權威（實機驗證文件——「單次洗價模式：啟動後完成一次洗價並自動停止」「等待單次洗價自動停止」）
2. 官方課程/文件蒸餾（「單次洗價模式：對最後一根 Bar 完成一次判斷後停止」）
3. 原始 DB 生命週期交叉（單次模式 5-row shape vs 連續模式多 trigger shape）

**SensorLog state-code 解讀（已 authority 交叉驗證）**：
- **單次洗價模式**（5-row shape）：`state 2,2,2,2,3` + `exec 1..5` + 單次 TriggerTime = 對最後一根 Bar 一次判斷 → 自動停止 = **合法 stopped terminal**。
- **連續/多次觸發模式**：`2→3→1` / `exec 1→8` 多輪 = 完整生命週期。兩種 shape 都是合法行為，非矛盾——差別在觸發模式。
- **STOP 命令有效性證明**：策略被 STOP 後 DB 出現 `state 0/exec 527` + `state 1/exec 8` = 引擎確實接收並轉換狀態（STOP 非 no-op）。
- 系統未發布官方 state-code 表——authority 上限是社群+課程+原始資料交叉；若有上游 oracle 官方 mapping 則為終極 authority。

## 4. 每輪都適用的 smallest-repair 原則

- 外部裁決通常 `PRODUCT_REBUILD_REQUIRED = NO / BROAD_RERUN_REQUIRED = NO` → **只補缺的 edge**。
- 重跑範圍最小化：只補被 challenge 的 edge，不重跑已 PASS 的 fixture。
- **先 reuse 現有證據**：「if post-stop raw readbacks already exist, reuse them」——先查 receipts 再決定重跑。

## 4b. 並行 session 污染防護（2026-08-14 實戰：git add -A 混入 638 檔）

Fabric repo 常有多個 session 同時 commit（one-active-writer 是桌面操作層，git 層無鎖）：
- **禁止 `git add -A` / `git add .`**——會抓入其他 session 未 commit 的變更（實例：skill integration commit `52240da` 誤混 AGENTS.md/IDEA.md/challenge-review 等 638 檔）。
- 只 `git add <自己的具體檔案路徑>`；commit 前 `git show --stat HEAD` 檢查檔案數與內容。
- 誤混時 `git reset --soft HEAD~1` 回滾（保留 working tree，不丟他人變更）。
- skill 目錄更新（Hermes skills/）不在 repo 範圍，不需 repo commit。

## 5. 打包完成檢查表（提交前逐項）

- [ ] 單一 MD self-contained（全部 raw body 內嵌，無本地路徑依賴）
- [ ] 宣告 SHA == reviewer 可重算（內嵌 body 的 SHA）
- [ ] 無 self-hash 欄位；sidecar 真實發布（非 placeholder）
- [ ] manifest raw JSON body 完整內嵌（可 parse、可重算 entries/unique/subject）
- [ ] checker 在 repair 完成後跑；subject == final HEAD；single denominator；無 duplicate ID
- [ ] final HEAD == manifest.subject_root == checker.subject_root（三向）
- [ ] 關鍵 receipts 全綁定 manifest
- [ ] domain semantics 有 authority 來源（社群/官方/課程交叉），非自行解釋
- [ ] 3-way mirror 相等（Fabric / HG-KSEOS / SQS-THC）
- [ ] honest residuals 明列（time-gated 項等）
- [ ] **bundle 有單向無循環的封存鏈**（files → manifest JSON → `MANIFEST.sha256` → terminal SEAL），見 §7
- [ ] **terminal SEAL 記錄 expected 檔案數 + 總位元組**，且與實測相符（`sha256sum -c` 抓不到新增檔）
- [ ] 每個收據引用的 hash 都是**最後一次內容寫入之後**才算的（封存後才補的檔 = 收據 stale）
- [ ] secret 掃描的 quarantine 是**判定過的 false positive**，不是靜默隔離核心證據

## 7. 封存鏈：manifest / hash 的自我參照循環（2026-10 兩輪獨立驗收抓的）

把 frozen evidence 打成 portable bundle 時，**最常見的 defect 不是內容錯，而是 hash 簿記自成循環**——
連兩輪獨立 lane 都抓同一類：宣告的 manifest hash stale、封存後又補了檔案、root 檔列舉不全。

### 7.1 單向封存鏈（禁止互指）

```
files → EXTERNAL_ACCEPTANCE_MANIFEST.json → MANIFEST.sha256 → BUNDLE_SEAL.json（terminal）
```

- **`MANIFEST.sha256` 必須明確排除「自己」與 terminal SEAL。** 若 SEAL 內配 `sha256(MANIFEST.sha256)`
  而 `MANIFEST.sha256` 又列 SEAL 的 hash，就是**循環**：兩個檔案任一變動都讓對方永久 stale，重寫多少次都不會收斂。
  改成單向：SEAL 記 manifest hash；manifest sha 不記 SEAL。
- **self-referential root 檔**（內文嵌了 manifest hash 的 README / readback / seal）在 manifest JSON 裡
  要標 `self_referential: true` 且 `sha256: null`，並註明「權威 byte 記錄在 `MANIFEST.sha256`」——
  否則你會陷入「A 記 B 的 hash、B 記 A 的 hash」的同一循環。
- **`sha256sum -c MANIFEST.sha256` 驗不出「新增檔案」。** 多放一個檔不會讓任何一行失敗，所以
  terminal SEAL 必須記 `expected_file_count` + `expected_total_bytes`，驗證時**用數量與位元組總和比對**
  才抓得到 add-only 竄改。這是 mitigation 不是 cryptographic anchor——沒有簽章/MAC 就誠實寫
  `no_cryptographic_anchor: true`，不要假裝有完整性保證。

### 7.2 兩段式收斂（否則 expected 數量會自我膨脹）

`expected_file_count` 若在「寫 SEAL 之前」量測，會漏算 SEAL 自己（或沿用上一輪的舊 SEAL 而多算一）：
1. 先寫 SEAL placeholder → 2. 量測**最終**檔案集（排除 archive）→ 3. 用實測值改寫 SEAL → 4. 才產生 archive。
因 SEAL 不在 `MANIFEST.sha256` 內，改寫 SEAL 不會連鎖使 manifest hash 失效。

### 7.3 收據要點（封存後不得再補內容）

- 任何「宣告 hash」都必須是**最後一次內容寫入之後**重算的；封存後才補一個檔（例如 lane outcome）→
  所有引用該集合的收據當場 stale。**內容先全部定稿、再封存、再算 hash。**
- 舊輪次的數字（例如 reseal 前的 file count / zip sha）**只能掛在明示的 `round_1` historical 標籤下**，
  不得留在 `current` 欄位冒充現況。
- hash 有變就要**同步更新所有複述它的地方**（README 的 manifest SHA、readback 的 manifest_sha256）——
  獨立 lane 會逐處比對。

### 7.4 Secret 掃描：false positive 要判定，不要靜默隔離證據

設計文件語料含有大量**很像憑證的散文**（例：`Human approval token`、`token = OR-D03-TOKEN(ctx)`）。
寬鬆的 `token[:=]` 規則會把這些核心證據 quarantine/redact 掉，反而讓 bundle 缺件。修法：
- 只認**高熵**憑證指派（長度門檻 + 熵門檻 + 需有非字母字元）與已知 key 前綴；
- 命中但判定為散文者，記 `classification: PROSE` **明確寫進證據**（不是靜默放行，也不是靜默隔離）。

### 7.5 Windows 長路徑

深層語料的檔名可超過 MAX_PATH。Python 讀取時用 extended-length 前綴：`open(r"\\?\" + abspath)`；
否則 bundle 建置/重雜湊會在 `FileNotFoundError` 上假性缺件。

## 8. remote-byte 傳輸完整性：hash 對了 ≠ 意思對了（2026-10 兩輪獨立驗收抓的）

§7 講封存鏈的簿記循環；本節講**發布後**才會暴露的另一組缺陷。兩輪外部驗收都抓到「15/15 hash
全對」卻仍在下一輪被判 FAIL 的情形——所以 hash 相等**不是** evidence linkage 的充分條件。

### 8.1 兩個獨立檢查：bytes 完整性 與 subject 語意

- **hash/bytes 檢查**證明「運輸無損」，不證明「內容指向正確主體」。
- 實際案例：manifest 宣告 subject = 新 SHA，而其中一個證據檔**內部**仍寫著上一輪被 FAIL 的舊 SHA；
  該檔的 remote bytes 與 manifest SHA **完全相符**。
- 更強的內部矛盾：該收據同時引用「只存在於新 SHA 才新增的 subsystem」——自證與自身宣告的 subject 衝突。
- **修法（打包時強制執行，非抽樣）**：對每個 item 比對**自身 subject identity** vs manifest subject。
  - JSON item：讀 `source_candidate_sha` 或 `subject`（`subject` 可能是 dict，需取其內層 key）。
  - raw log：解析檔頭 `# git HEAD: <40hex>`，**不要**因為它不是 JSON 就判失敗。
  - 任一 item `internal_subject_ok == false` → 整包 `PARTIAL`，不得發布。
- **被取代輪次的舊檔是慣犯**：舊 receipt / 舊 readset / 舊 final-packaging 會夾帶舊 subject。
  處置是把它們**移出新 subject 的證據樹**（歸檔到 `*_superseded_<round>/`），不是留在原地。
  留著 = 用全新的 manifest 運送一個過期的 subject。

### 8.2 從 committed blob 取 hash，不從工作檔

本機檔案 hash ≠ remote blob hash 的機制：**Windows 上寫檔預設插入 CRLF，git 把 blob 正規化為 LF**。
於是 manifest 若以本機檔案計算，遠端讀回時**每一項都 mismatch**，且只有在發布後才看得到。

收斂步驟（三段式，避免 manifest 自我參照）：
1. 以 placeholder（`PENDING_BLOB_HASH` / bytes 0）寫入 manifest；
2. commit 證據 repo；
3. 用 `git cat-file blob <rev>:<path>` 逐項取**已提交的 bytes** 計算 sha256/bytes；
4. 改寫 manifest（它已排除自身，所以改它不會使 items 失效）→ amend → push；
5. 再對最終 ref 重算一次，要求 `mismatch_count == 0`。

環境設定：暫存證據 repo 內 `git config core.autocrlf false` + `.gitattributes` 內容 `* -text`；
Python 寫 JSON/log 一律 `newline="\n"`。三管齊下可讓本機 bytes == blob bytes，除錯時少一層混淆。

### 8.3 發布後必須做的遠端重算

只在本機驗證等於沒驗。發布後 `git fetch` 該 evidence commit，逐項 `git cat-file blob` 重算
**hash + bytes + 內部 subject 身分**，並把結果寫進 readset（`remote_exact_byte_verification`）。
- readset 本身**不得**進該 evidence commit（它內含該 commit 的 SHA，會自我指涉、永遠對不上）——
  以交付檔形式交出去。
- **不要在 readset/返回包裡放 `evidence_commit_sha` 欄位指向「即將包含它的那顆 commit」**。
  實測陷阱：寫 `evidence_commit_sha = <commit N>` → 提交 readset → SHA 變 `<commit N+1>` →
  欄位 stale → 再改再提交，永無止境。處置：readset 為權威本體放**repo 外**，只把 `evidence_commit_sha`
  綁定**最終 evidence branch tip 恰好一次**並凍結；repo 內的 in-tree 副本一律標 `inert support`，
  不得以其內容回填欄位。每次因欄位自指而「再提交」都是訊號：readset 進錯地方了。

### 8.4 打包檢查清單（追加至 §5）

- [ ] 每個 item 的**內部 subject identity == manifest subject**（非只比 hash）
- [ ] 被取代輪次的舊檔已移出新證據樹
- [ ] manifest hash 來自 `git cat-file blob`（committed），非本機檔案
- [ ] 證據 repo 已設 `core.autocrlf=false` + `.gitattributes * -text`
- [ ] 遠端重算 `mismatch_count == 0` 且每個內部 subject 相符
- [ ] readset 不在 evidence commit 內（自我指涉）
- [ ] run-level verdict 只存在於**一個** artifact（勿在多處複述而不同步）

## 9. 驗收主體身分裁定、交付完整性、交付前自檢（2026-10）

外部裁「權威檔案未交付」（EVIDENCE_GAP）與「同一產物兩份 hash 衝突」（ORACLE_DISAGREEMENT）時的固定處理。

### 9.1 依 blob SHA 讀回，不依路徑（Windows 長路徑會製造「假 mismatch」）

- 用 `git ls-tree -r --long <sha>` 取每檔的 **blob SHA-1 + byte size**，再 `git cat-file blob <blob_sha1>`
  取內容重算 sha256。**完全不碰工作區路徑。**
- 為何必須如此：以路徑取檔（`git show <sha>:<path>`）在路徑超過 Windows MAX_PATH（260）時會回**空輸出**，
  同時在 stderr 留 `fatal: failed to stat …: Filename too long`。把它收成「內容不符」等於**假 mismatch**
  （本機檔案明明存在）。依 blob SHA 讀則完全免疫。
- **空讀一律 hard error**：計數 `empty_or_failed_blob_reads` 並讓 verdict FAIL，不可當成 mismatch 或當成通過。
- 與 §8.2 搭配：readback 一律用 committed blob，工作區 CRLF 不影響。

### 9.2 兩層傳輸對帳：一次 API 拿全部 blob SHA

- `GET /repos/{owner}/{repo}/git/trees/{sha}?recursive=1` **一次**回傳整棵樹（含每個 blob 的 SHA）。
  與本機 `ls-tree` 逐項比對，即完成「本機物件庫 vs GitHub」對帳——不需逐檔 contents API。
- 必須檢查回應的 `truncated` 旗標：為真代表遠端樹被截斷，此時**不得**宣稱傳輸一致，改抽樣或分批。
- 把兩層分母與不一致數都寫進 readback（`transport_disagreements`、`remote_blobs_seen`），並區分
  「傳輸無損」與「語意正確」（§8.1）；`remote_blobs_seen` 恰等於該 commit 全檔數時，可作為「整棵樹都對過」的證據。

### 9.3 交付完整性收據（readset/readback 之外再出一份）

- 每輪都要**為當前這一輪**重生 readset/readback 並帶**當輪** round 標籤；沿用上一輪標籤
  （例：寫 REV6 而主體已是更後面的 rev）本身即 defect。
- 另出 `HANDOFF_COMPLETENESS_RECEIPT.json`：列出 reviewer **必須收到**的每個檔 + sha256 + bytes、
  exact tuple（repo / PR / source SHA / evidence SHA / immutable parent / historical SHA）、readback 分母摘要、
  checker 欄位（尚未跑就明寫 `PENDING`，**不可**預寫 PASS）、以及 finding 結案區塊與 W2 交接區塊。
- 明列「**被引用但未附帶**」的輸入（order / challenge report / RBWI / compiler bundle / 前代 prompt），
  並說明其 sha256 已記在 contract 的 authority 清單——否則 reviewer 會當成缺件。

### 9.4 交付前自檢：null/placeholder 掃描 + 契約列萃取陷阱

- 全包掃 `:\s*null\b` 與 placeholder 字串（`BOUND_BY_*`、`PLACEHOLDER`、`TBD`…）。
  **load-bearing 證據裡的 null 就是 over-claim**：本次即「支撐 route 判定的那一列」因萃取鍵路徑寫錯而為 null，
  整包表面看起來卻是完整的。
- 萃取契約列時**不要假設鍵名或層級**：同一列可能在一段叫 `id`、在另一段叫 `source_id`；
  也可能嵌在 `authority.sources` 而非頂層。掃所有合理位置、兩鍵都接受，並對**承載判定的欄位做 fail-closed 斷言**
  ——hash 與 path 都要斷（只斷 hash 會漏掉「指到另一份同名檔」）。
- 「無事」的欄位寫 `"NONE"` 而非 null，避免「已檢查過、無誤」與「忘了填」無法區分。

### 9.5 最終 rev 相對「最後已驗 rev」的 delta 揭露

- 列變更檔清單（例：僅描述文字 + 重算雜湊共 5 檔），並證明**各 finding 的證據檔逐位元相同**，
  再明說「此 delta **未經獨立複驗**」——不可讓新 commit 繼承舊 PASS（§7.3 同一原則的交付面）。
- 同時**回算 order 自己引用的輸入 hash**：與 order 內宣稱值不符（例如你在 order 產出後修過被引用的 SUPPORT 文件）
  必須主動揭露；相符則寫進證據，這是「order 引用的就是現行 bytes」的直接證明。

## 6. 歷史（FDA 每輪外部裁決要點）

| 輪 | verdict | 抓的 defect | 修法 |
|---|---|---|---|
| r1 | PARTIAL | pointer-rich index 非 raw、無 subject root、checker 126vs144、UFO² BLOCKED_HITL、PAPER 無 runtime、DoD 矛盾 | raw bundle、manifest rebind、checker 單一化、UFO² 7/7 opencode-go、PAPER SensorLog、DoD 36/36 |
| r2 | FAIL | 6 處狀態矛盾（UFO²/PAPER/checker/subject lineage/denominator）| 單值化 reducer + post-XQ rebind |
| r6 | FAIL | F01 stale 3.18、PAPER <10、F06 同 timestamp、checker 截斷 | F01 260811 10x、PAPER 10 verified、F06 fresh 10x、checker 179 raw |
| r7 | FAIL | PAPER STOP 無 post-stop、checker 179vs98vs184+chronology、rebind 缺 manifest raw | STOP 10x readback、checker 194 修 duplicate、freeze 三向 |
| r8 | PARTIAL | STOP semantics 未 authority-bound、manifest 無 raw body | authority 三源交叉、manifest raw body 內嵌 |
