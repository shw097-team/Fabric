# WO-FABRIC-REPO-ASSESS-20261013 — EXECUTE 研究 lane 報告

## A. 裁決主文

依本次 packet 所量測的證據，**https://github.com/shw097-team/Fabric 不需要對全部內容做一次性的 COMPLETE update**。該倉庫目前的核心缺口不是「內容量不足」，而是「發布不可重現」——packet 記載的 mirror 是在 repo 內找不到 builder（對四個樹搜尋 mirror 名稱、manifest 路徑與 remote slug 均無結果），推論為 ad-hoc 發布，因此「把全部內容重傳一次」並不比現況更能保證可重現，只會把同樣的 ad-hoc 狀態複製一遍，成本最高而收斂最低。故「全量更新」應被否決為過度工程。

較便宜且能真正收斂的 disposition 是**分階段、目標導向的五至八步**：先取回或固化 mirror 發布程序，其次修掉宣告排除矛盾，再處理 .gitignore／.pyc／.lnk 等低摩擦衛生項，最後才刷新 manifest 與對外文件；LICENSE、大型二進位去留、本地 Fabric 是否連結 remote，屬 owner 決策，不由本 lane 代決。判定詞請見 B 節。

本裁決**不決定**的事：不決定授權條款（LICENSE）採何者；不決定個別大型二進位（如 9,824,365 bytes 的 `FABRIC/rp002/G0/RP002_INPUT_DENOMINATOR.jsonl`）是否應保留或移出；不決定本地 Fabric 是否應連結並推送至 remote；不決定桌面效應切片的 authorization-token refresh（packet 明載 gate 未繞過）；不執行亦不授權 SQP1 或 Stage-3；不構成任何 acceptance、promotion、release，亦未對 repo 做任何變更。

## B. 逐項判定表

| 項目 | 判定 | packet 依據 | 理由 |
|---|---|---|---|
| mirror-vs-local divergence | UPDATE_NOW | local head `0c1e6bc3585da052f7f339840d745f6884431925`；remote head `0dccb8afe72a93508958dad8a0fdb4d633668c94`；路徑重疊 zero（mirror 以大寫主題夾前綴，local 為小寫樹） | 兩者非同一拓樸，不是可 fast-forward 的同步關係；必須先確認它們的對應規則 |
| ad-hoc builder | UPDATE_NOW | repo 內找不到 builder；唯一 github publisher 指向 PIPD release repo，非此 mirror | 這是「refresh 不是一鍵重跑」的根因，位列最高必要性 |
| declared-exclusion contradiction | UPDATE_NOW | `INTEGRATION/MANIFEST.json` 宣告排除 `var/`，但 `DESKTOP/var-fda/**` 實際在 mirror 內 | 宣告與實物矛盾是 truth defect，必須消解；修法方向（移除實物或修正宣告）偏 OWNER_DECISION |
| .pyc | UPDATE_NOW | remote `.pyc` 127 blobs | 生成物，刪除成本與風險皆低，可即時收斂 |
| .lnk | UPDATE_NOW | 已發布 `DESKTOP/docs-fda/evidence - 捷徑.lnk` | Windows 捷徑為機器相依、對外部工程師無資訊價值 |
| 大型二進位 | OWNER_DECISION | `blobs_over_400kb`: 16；最大 9,824,365 bytes | 部分（PDF、png、大 tsv/jsonl）可能為證據或來源資料，去留需 owner 判斷，非本 lane 可代決 |
| missing .gitignore | UPDATE_NOW | `gitignore_present_remote: false` | 與移除 .pyc/.lnk 同批處理最省 |
| missing LICENSE | OWNER_DECISION | `license: null` | 授權選擇屬 owner／法務決策；但公用 repo 無授權將實質阻礙外部工程師再利用，是真缺口 |
| manifest freshness | UPDATE_LATER | manifest 停在 2026-10-10；local 有 2026-10-10 之後提交，含今日 11:02Z 的兩處一行 README 修正 | 依賴 builder/procedure 先確立，否則刷新仍是 ad-hoc |
| manifest non-claims | NO_UPDATE | NON_CLAIMS 含 `NOT_EXTERNALLY_ACCEPTED`、`NOT_MERGED`、`NOT_RELEASED`、`NOT_PRODUCTION`、`NO_LIVE_WORLD_EFFECT` | 非主張陳述正確且必要，維持不動 |
| document refresh for external engineers | UPDATE_LATER | requirement 要求外部工程師能據 repo 規劃完整升級 | 文件須描述實際（可重現）程序；layout 未穩前刷新易再次過期 |
| orphan check | CARRY_FORWARD | quarantine 產物已發布（`quarantined_violations/far_v18_patch_test.py`、`run_f06_system_path.py`）且 builder 找不到 | 需確認無無主／無參照產物；重型 orphan 掃描器在 builder 未復原前屬過度工程 |
| 本地 Fabric 未連結 remote | OWNER_DECISION | `local_fabric_remotes_configured: []` | 連結與推送屬 owner 決策，且 repo 規則禁止 push；現況須視為「設計事實」而非必然缺陷 |
| credential 檔名暴露 | NO_UPDATE | `credential_filename_exposure` 各檔名對應陣列皆為空；`dotenv_exact_match: []` | 量測為陰性；無偵測到外洩，維持既有防線即可 |
| 已發布執行 log | OWNER_DECISION | `HG-KSEOS/.hgk/checker-upgrade-20261009/**` codex session rollouts 存在且被 2026-10-10 發布紀錄引用 | 執行 rollout 可能含內部推理，是否續留屬 owner 決策 |

## C. 執行方案（依 necessity × friction 排序）

**S1｜復原或固化 mirror 發布程序**　動作：自四個樹之外尋找 builder；若確實不存在，則以文字固化現行發布步驟。成本：中。風險：若只有程序而無腳本，仍屬人工。修復物：可重現的發布路徑。正測：以既有輸入重跑產生與 remote 一致的內容清單。負測：輸入缺失時必須回 `INCONCLUSIVE`，不得回報成功。回滾：新增檔案刪除即可。Owner：工程 owner，owner 認可。

**S2｜消解 declared-exclusion 矛盾**　動作：使 `MANIFEST.json` 宣告與實物一致。成本：低。風險：方向選錯會誤刪證據。修復物：真實的排除宣告。正測：宣告集合與實際內容集合相等。負測：空宣告或空目錄須判 `INCONCLUSIVE`。回滾：還原宣告檔。Owner：OWNER_DECISION（方向）。

**S3｜新增 .gitignore 並移除 .pyc／.lnk**　動作：加入 .gitignore、刪 127 個 .pyc 與 .lnk。成本：低。風險：極低。修復物：乾淨的發行樹。正測：重數後 `.pyc` blobs 為 0。負測：若清單為空則判 `INCONCLUSIVE`。回滾：還原刪除項。Owner：工程 owner。

**S4｜LICENSE 決策**　動作：由 owner 指定授權。成本：低。風險：選錯之法律後果。修復物：明確再利用條件。正測：LICENSE 檔存在且與宣告一致。負測：未選定時不得自行填入。回滾：還原為 null。Owner：OWNER_DECISION。

**S5｜manifest 刷新**　動作：於 S1 後更新至最新 subject state。成本：中。風險：易殘留 stale。修復物：現行 manifest。正測：digest 與 subject 一致。負測：stale／foreign 證據須判無效。回滾：還原前版。Owner：工程 owner。

**S6｜大型二進位審查**　動作：逐項判定保留或移出。成本：中。風險：誤移證據。修復物：精簡且可辯護的內容集。正測：每項有二值去留標記。負測：未標記者不得預設刪除。回滾：還原 blob。Owner：OWNER_DECISION。

**S7｜對外文件刷新**　動作：撰寫外部工程師導向說明（含 non-claims）。成本：中。風險：描述與實物不符。修復物：可據以規劃的文件。正測：步驟可被第三人依序執行。負測：輸入不足時標 `INCONCLUSIVE`。回滾：還原文件。Owner：工程＋owner。

**S8｜本地 Fabric remote 連結**　動作：由 owner 決定是否連結。成本：低。風險：誤觸 push。修復物：明確的來源關係。正測：僅設定不推送。負測：未授權推送一律拒絕。回滾：移除 remote。Owner：OWNER_DECISION。

**DO-NOT 清單**：不 push／merge／deploy；不 reset upstream；不做全量重傳以求「完整」；不事後手改 manifest digest；不在缺 builder 時聲稱可一鍵重建；不以 manifest 存在當 PASS；不動 frozen source roots；不以重新登入同一帳號主張身分分離；不執行 SQP1／Stage-3。

## D. 建議刪除或降級

「對全部內容做一次 COMPLETE update」——**REJECT_OVER_ENGINEERED**，因它未閉合可重現性缺口。在 builder 尚未復原前建立重型 orphan 掃描器或 mirror CI——**REJECT_OVER_ENGINEERED**，機械先於閉合。為每個大型二進位建立完整 provenance 帳本——**REJECT_OVER_ENGINEERED**，除非該檔本身即為證據。為此衛生任務新增 promotion／acceptance 機械流程——**REJECT_OVER_ENGINEERED**。「以重新登入同一帳號主張身分分離」——依 repo 規則記為 **NOT APPLICABLE**，非 blocked。上述皆屬機械，非閉合。

## E. 限制與非主張

**NOT_VERIFIED**：builder 是否真正不存在於四個樹之外（packet 僅量測四樹內搜尋）；大型二進位各自之必要性與來源；credential 內容是否外洩（僅檔名搜尋為空，未驗內容層）；2026-09-01..2026-10-13 Hermes session 視窗已無法取回（packet 明載未保存、不作證據）。本裁決**不構成驗收**、**未變更 repo**、**未代行任何 owner 決策**，亦未授權 production／release／deploy；僅為 bounded 研究 lane 之建議。所有數字均轉錄自 evidence packet，非本 lane 自行量測；packet 之 claim ceiling 為「以 owner PAT 之 GitHub API 唯讀偵察，未做任何 repo 變更」。

STACK_HYGIENE_synthesis-repo-assess: