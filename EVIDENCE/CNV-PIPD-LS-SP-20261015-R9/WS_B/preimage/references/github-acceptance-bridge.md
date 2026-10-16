# GitHub acceptance-bridge (probe → bootstrap → publication boundary)

用於：訂單授權建立/發佈一個 GitHub **acceptance mirror**（例如 org/repo
`<org>/<REPO>`），而 `gh` CLI **可能不存在**。此時直接用 REST API（curl）驅動，不要因為
`gh` 缺席就回報不可用。

## 0. 三條不可違反的邊界

1. **GitHub 永遠只是 acceptance mirror / transport**，絕不是 construction root、也不是
   semantic 或 runtime authority。本地 truth 先成立，遠端才有意義。
2. **絕不從模糊狀態推論「不存在」。** 只有**已認證的明確 404** 才允許進入建立流程；
   auth / 403 / 網路 / 未知 / 模稜兩可 → `TEMP_CLOSED_GITHUB`，且**不建立**。
3. **bootstrap ≠ publication。** 建立 repo 只完成 Phase E；candidate 與 evidence 的發佈
   各自需要 `LocalClosureReceipt` + `IndependentReceipt` + checkpoint **在同一 HEAD 全部 PASS**。
   施工未完成時，`main` 保持空白 initial baseline 是**正確**的，不要為了「看起來有東西」而推。

## 1. 探測順序（先讀、後寫）

```text
auth → owner identity/type → exact repo state → (only if explicit 404) create → readback
```

| 步驟 | 端點 | 判讀 |
|---|---|---|
| auth | `GET /user` | 200 才算已認證；記 `login`/`type` |
| owner | `GET /users/<owner>` | `type == Organization` → 用 org 端點建立 |
| repo state | `GET /repos/<owner>/<repo>` | **200 = 已存在 → 不要建立**；**404 = 明確不存在**；其他 → TEMP_CLOSED |
| create | org: `POST /orgs/<owner>/repos`；user: `POST /user/repos` | 201 成功；4xx → TEMP_CLOSED_GITHUB（權限未確認） |
| readback | `GET /repos/...` + `GET /repos/.../branches/<default>` | 記 `id`/`private`/`default_branch` + baseline SHA |

- 建立 private repo 用 `{"name": ..., "private": true, "auto_init": true}` — `auto_init` 讓 `main`
  先有 initial baseline，遠端才有可讀回的 SHA。
- **owner 是 org 時必須走 org 端點**；`POST /user/repos` 會建到認證者本人名下，不是目標 org。

## 2. HTTP 狀態必須自己抓，不要用 curl 的退出碼

`curl` 的 **exit code 是傳輸層結果（連線成功 = 0）**，不是 HTTP 狀態。把它當狀態用，
探測器會把「404 Not Found」讀成 0 → 落入 `AMBIGUOUS` 分支 → 做出錯誤的 fail-closed 決策。

修法：`curl -s -o - -w "\n%{http_code}"` 並把最後一行 parse 成 int；解析失敗才視為
`0 / unknown`。同理，**決策邏輯要把 `404` 與 `其他 4xx/5xx` 明確分開**——只有 404 允許建立。

## 3. fine-grained PAT 的 403 陷阱

fine-grained PAT 常對 org 端點回 `403 Resource not accessible by personal access token`
（例：`GET /orgs/<org>/memberships/<user>` 或 `GET /orgs/<org>`）。
**這是「讀權限不足」，不是「沒有建立權限」的證據。**
不要因此判定 TEMP_CLOSED；在**已認證明確 404** 的前提下直接嘗試建立，
**建立嘗試本身就是權限的直接確認**：201 → 通過；403/404 → 誠實回報 TEMP_CLOSED_GITHUB。

## 4. 建立後必須讀回（外部狀態變更一律驗證）

外部寫入成功 ≠ 任務成功。建立後**另發一次全新的 GET**（不是重用建立回應）確認
`full_name` / `private` / `id` / `default_branch`，並讀 `branches/<default_branch>` 取 baseline SHA。
四項都相符才記 `BOOTSTRAPPED`。

## 5. 憑證衛生（每次都要）

- token **只**從環境變數讀（例如把附件解析進 `GH_PAT`），**絕不**印出、寫進證據、或 commit。
- 交付前做**洩漏掃描**：`grep -rE 'github_pat_[A-Za-z0-9_]{20,}'` 掃過 evidence 目錄、
  工作目錄與 target repo；期望 0 命中。
- 收據寫 `credential_safety`：`token_printed/written/committed: false` + 掃描範圍 + 結果。
- **主動建議輪替**：明文附件裡的 PAT（尤其帶 repo-creation 權限者）在任務完成後應撤銷或輪替，
  並把未來憑證移出明文檔。這件事要講出來，不要默默留著。

## 5.1 洩漏掃描必須唯讀；**絕不對二進位／live 檔案做「就地抹除」**（incident 2026-10-05）

真實事故：Codex lane 在自己的 transcript 逐字複印了被稽核 repo 內的憑證值，於是對命中檔案做
就地字串抹除——其中一個命中是 **`%LOCALAPPDATA%\hermes\state.db-wal`（live SQLite WAL）**。
以「讀 bytes → `decode(utf-8, 'replace')` → 取代 → 以文字寫回」的方式處理二進位檔，後果是：
每個非 UTF-8 位元組變成 U+FFFD，WAL header 失效（`377f0686…` → `377f06efbfbd…`），
Hermes 當場開始報 `state.db is corrupt … database disk image is malformed`、session 讀取失敗；
該 WAL 內**尚未 checkpoint 的交易全部不可套用**（主 `state.db` 本身仍 `quick_check=ok`，資料可讀，
損失範圍限於 post-checkpoint 的 WAL 內容）。

硬規則：

1. **掃描 = 唯讀。** 先產生命中清單，再由人決定處置；不要在同一個自動步驟裡掃完就改。
2. **只對純文字工件抹除**，且先確認是文字（試 decode 無 `errors='replace'` 成功、無 NUL、非 SQLite/WAL/git object/zip/圖片）。
   `*.db`、`*.db-wal`、`*.db-shm`、`*.pack`、`*.zip`、`*.lnk`、`*.png` 一律**不得**就地改寫。
3. Live DB 的處置是**停服務 → 備份 → 由 SQLite 自行丟棄無效 WAL → 重啟**；不要手工「修」WAL。
4. 根本解法是**在寫入端就別讓值進來**：把 lane 的 stdout/stderr 導向管線前先過濾（`sed`/`grep -v` 對已知欄位遮罩），
   或不要用 `--json` 全量落盤而改為只落地結構化裁決；事後補救永遠比事前遮蔽風險高。
5. 出事後要**主動揭露並留下 forensic 副本**（原始 corrupt 檔 + 主 DB snapshot），不要靜默重跑。

## 6. 收據要點

```yaml
schema: ...-GITHUB-ACCEPTANCE-BRIDGE-BOOTSTRAP/1
auth: {http: 200, login: ..., type: ...}
owner_probe: {http: 200, type: Organization}
repo_probe: {http: 404, exists: false}
create: {endpoint: /orgs/<org>/repos, http: 201, private: true, default_branch: main, id: ...}
readback: {http: 200, ...}
main_baseline: {branch: main, head_sha: <40hex>}
verdict: BOOTSTRAPPED | EXISTS_DO_NOT_CREATE | TEMP_CLOSED_GITHUB
publication_status: DEFERRED - requires local final closure + independent receipts on one HEAD
non_claims: [NO_CANDIDATE_PUBLISHED, NO_EVIDENCE_COMMIT_PUBLISHED, NOT_EXTERNALLY_ACCEPTED, NO_RELEASE, NO_PRODUCTION]
```

`EXISTS_DO_NOT_CREATE` 是合法終態：repo 已存在時**只驗證它是預期的 acceptance mirror**，不重建。

## 7. 已存在 mirror 的 candidate/evidence 發佈（dual-branch exact-SHA）

本檔 §1-6 是 probe/bootstrap（建立），當 repo **已存在**且要推兩條分支（source candidate =
PR head；evidence RETURN_PACK commit）時，走 `references/external-publication-mirror.md` §8：
以 repo 外 credential store + token-free origin URL（**永不把 token 嵌進 `.git/config`**）
push 兩分支 → `ls-remote` 讀回確認各等於本地 exact SHA → 開 PR 驗 `head.sha == source_candidate_sha`
→ 用完即刪 credential file + unset helper。含 readset self-reference 陷阱：`evidence_commit_sha`
綁**含 RETURN_PACK 的不可變 commit**（≠ readset 自己），branch tip 是 non-subject（記在 PR body，
永不進凍結 readset）。
