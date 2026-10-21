## 候選分類裁決

**結論：優先收斂「已可用但未納版的工具」與「能抓到現存漏檢的檢查器」，不建議再新增治理型 SKILL，也不建議把整批 `var/` 候選搬進 MAIN。**

### 判讀邊界與實測基準

以下使用：
- `R`＝`C:\Projects\Agent_Workspace\HG-KSEOS`
- `F`＝`C:\Projects\Agent_Workspace\Fabric`
- `H`＝`C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\skills`

| 實跑命令／讀取方式 | 讀到的值與主張上限 |
|---|---|
| `git -C R rev-parse HEAD`、`git -C R show --stat c442f07` | HEAD＝`c442f0703695d93ce270029ed48031a07c5d6620`；包含 epoch 23 對齊及四個 routing 檔納版。 |
| `git -C R show-ref --verify refs/heads/main` 與 `refs/remotes/origin/main` | 均 exit 128；**HGK 本機沒有這兩個 MAIN ref，不能把工作樹存在說成已 merge MAIN。** |
| `git -C F rev-parse HEAD`、`show-ref` | HEAD 與本機 `origin/main` 均為 `bcd91043…`；本機 `main` 為 `abb70eb4…`。本回合未 fetch，不宣稱是遠端即時狀態。 |
| `git -C F ls-tree -r --name-only origin/main`，限定 `INTEGRATION/` 與 skill-convergence 證據路徑 | 共 33 路徑，其中收斂證據 22 路徑；同樣查本機 `main` 得 0。 |
| Python `Path.rglob('SKILL.md')`＋`yaml.safe_load(frontmatter)` | H 共 **78** 份 SKILL，已逐份讀取 `name` 與 `description`。 |
| Python 檢查 `R/skills`、列舉 `R/control/skills/*/SKILL.md` | `R/skills` **不存在**；實際治理 skill 在 `control/skills/`，共 **18** 份，均已被 git 追蹤；與 H 的名稱交集為空。 |
| Python `iterdir()` 與有界 `os.walk()` | `var/` 有 **114 個頂層目錄**，包含 cache／備份，不能全稱為 114 個回合。有界、排除快照／環境副本後掃到 2,312 個 `.py`、778 個 `.md`；不是全樹完整普查。 |

### 可併入 MAIN 的候選

以下均為**建議另案納入**，不是本回合授權 apply，也不是驗收通過。

| 候選／來源路徑 | 價值與併入位置建議 | 驗收條件 | 風險與實測依據 |
|---|---|---|---|
| **1. 跨欄位宣告一致性檢查器**：`R/var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016/check_declaration_agreement.py` | 能補 `check_drift()` 的盲點。建議併入既有 `lane_policy`／其測試，不另建治理 skill。 | 矛盾必須非零退出；缺欄位／未知模型應為明確失敗或 INCONCLUSIVE；補正、負向、邊界案例；模型辨識不能只靠固定字串清單。 | **已抓到現存差距**：直接執行此腳本得到 `CONTRADICTIONS = 1`，但 **exit 0**。`/sod/verify_security_arm_A` 寫 `opencode-go / deepseek-v4.1-flash (primary Codex CLI checker)`，同份文件 `lane_chains.VERIFY_SECURITY[0]` 卻是 `openai-codex/gpt-6.1-sol`。同時實跑 `lp.check_drift(registry=reg)` 得 `[]`、epoch＝23。因此檢查概念值得納入，原腳本不能直接作阻擋閘門。 |
| **2. 已存在工作樹的 runtime 工具最小納版集**：`R/scripts/hgk-lane-dispatch.py`、`R/src/hg_kseos/lane_policy.py`、`R/scripts/runtime_role_binding_assert.py` 與對應測試 | 先消除「運作依賴未追蹤檔案」，比新增一套 toolkit 更實用。建議留在原 `scripts/`、`src/`、`tests/` 位置，以最小相依閉包納版。 | 逐檔確認來源與授權；乾淨 checkout 能重現；對應正負測、rollback、獨立 checker；不能直接 `git add .`。 | `git ls-files --error-unmatch` 實測上述三個工具及 `tests/test_lane_dispatch_ao_guard.py` 都是 **untracked、檔案存在**；相對地 `tests/test_lane_policy.py` 已追蹤。風險是依賴可能多於表面檔數，需先列閉包，不宜整批提交。 |
| **3. 宣告／pin 唯讀 healthcheck 的可複用部分**：`R/var/FAR-REMEDIATION-20261021/selfcheck.py` | 抽出 epoch、route、pin、pool、宣告檢查，併入既有 preflight／lane-policy 測試；不另起 health 平台。 | 預設只輸出 stdout、不寫 receipt；root／期望值參數化；單純檢查與 pytest、模型探測分開；納入候選 1 的跨欄位檢查。 | AST／原碼讀取：78 行，硬編碼 epoch 23、機器路徑、profile、binary；第 72 行會寫 `selfcheck_receipt.json`，並會跑 pytest。既有收據是 `GATE_PASS`、18 列、0 failed，**僅為歷史收據，本回合未重跑**；它沒有抓到上列 sibling-field 矛盾。 |
| **4. 發佈前 packet validator 的純檢查部分**：`R/var/FAR-REMEDIATION-AND-CLOSURE-20261016/packet_gate.py`；另有 `LANE-RELIABILITY-CLOSURE-20261016/packet_gate.py` 變體 | 重用 JSON parse、manifest digest、換行策略、claim-ceiling 檢查。建議放既有 publication／artifact tooling，並由 `remote-repo-publication` 引用。 | packet root／manifest schema 參數化；不讀憑證值；無寫入；以壞 JSON、缺檔、digest mismatch、CRLF 漂移做負測。 | AST／原碼讀取：135 行，硬編碼回合與 Fabric 路徑，還包含接觸 `API KEY` 目錄值的檢查設計。**只建議抽取純檢查核心，不原封不動納入。**本回合未執行涉及憑證的路徑。 |

### 應留作歷史／不併入的候選

| 候選 | 裁決與原因／實測證據 |
|---|---|
| `R/var/FAR-REMEDIATION-20261021/apply_far_remediation.py` | **保留歷史，不把原腳本納為通用 apply。** AST 讀到 397 行、固定 epoch 23、固定模型／binary／profile 路徑，且會改另一 profile。對齊結果已在 `c442f07`；重跑舊 anchor-based migration 不等於冪等維護。可學其 pre-image／唯一 anchor／read-back 作法，但既有 `canonical-change-landing` 已描述這些流程。 |
| `R/var/SKILL-CONVERGENCE-20261014/candidates/apply/guarded_apply.py` | **暫不升為真實目標 apply 工具。** 原碼明確限定 `fixture_only`，含 `ERR_APPLY_NOT_AUTHORIZED`、`portable_to_real_targets: False`。本回合在記憶體載入後執行 `main(['--check-plan'])`，實得 `REFUSED / ERR_PLAN / exit 2`；只證明缺 plan 會拒絕，未證明真實授權／補償完整性。Fabric 收斂結案也明載「只跑 fixture、無 canonical apply」。 |
| `candidates/avr/consolidate.py`、`candidates/hgk/phase2_consolidate.py`、兩份 `entry_extract.py` | **舊世代工具保留，勿直接覆蓋 live skill。** 原碼綁定 baseline／slice／固定主題，並有「每個被吸收檔留 stub」設計。現行 `lossless-content-consolidation/SKILL.md` 已改為依可達性決定 stub，避免檔數反增。舊候選與 live 也已不同：HGK 候選主檔 19,658 字元、references 101；live 20,491 字元、references 128。 |
| `var/` 內各回合 `admit_*`、`make_closure*`、`publish_packet*`、`push*`、修訂版 builder／receipt generator | **不整批併入。** 有界掃描確實找到大量此類腳本，但未逐一證明可參數化、授權正確、沒有回合常數與副作用。保留證據，不以「是 Python」當作可複用性。 |
| `F/INTEGRATION/APPROVAL-LIST-PROPOSAL.md` 所指 mirror builder | **目前不啟動 builder 工程。** 文件實讀為 `PROPOSAL — awaiting owner freeze`，明載 approval list 未凍結前 builder 不屬授權工作；不是少一個腳本就能直接補上的缺口。 |
| 將 `R/control/skills/` 的 18 份模板全裝進 H | **不做。** `codex-bounded-execute`、`wp-task-route` 原文都標示 `DESIGN/MATERIALIZED_LOCAL`，runtime invocation 為 `NOT_EXECUTED`；前者 Trigger 還含 `DENIED`。這是治理契約面，不是已驗證 runtime skill。 |

### 已被現行內容涵蓋、不需重做的

> 「現行涵蓋」不等於「已 merge 遠端 MAIN」；兩者分開判定。

| 項目 | 涵蓋證據位置與本回合實測 |
|---|---|
| **timeout partial capture 修補** | 現行 `R/scripts/hgk-lane-dispatch.py:1156–1170` 已保存 `TimeoutExpired.stdout/stderr`。本回合抽取實際 AST 分支、mock `subprocess.run` 注入 timeout，得到 `rc=TIMEOUT`、stdout／stderr 各 **16 bytes**、兩者保存皆 `true`，未啟動 child／未寫檔。**行為已在工作樹，不能再報「尚未實作」；但該檔未追蹤，納版缺口仍屬候選 2。** |
| **主檔瘦身及四個 HGK／兩個 AVR topics** | H 的 live topics 與候選同名群已存在。實測主檔：`hgk-governed-execution` 20,491 字元、`adversarial-verification-rounds` 29,281 字元；不要重新安裝舊凍結候選。 |
| **無損整併、canonical landing、發佈紀律等方法** | 已讀 H 下 `lossless-content-consolidation`、`canonical-change-landing`、`remote-repo-publication` 等現有內容；應擴充既有 skill 的工具引用，不新建同義 skill。 |
| **Skill convergence 的歷史結論與證據發佈** | `F/evidence/SKILL-CONVERGENCE-20261014/ROUND-CLOSURE.md`、`INDEPENDENT-CHECK-VERDICT.md`、`APPROVAL-LIST.md` 已存在本機 `origin/main` 樹。結論是 advisory、candidate-only，**不是 acceptance／promotion**。 |
| **references 尚待收斂** | 不再沿用 2026-10-14 的「94」當現值。本回合逐檔計算 live HGK references 為 **128**、AVR 為 **34**；94 只保留為歷史紀錄。可後續小批整理，但不值得因舊計數另開全面重構。 |

## 收斂建議

| 優先序 | 最小可落地動作 | 預估阻力 | 預期收益 |
|---|---|---|---|
| 1 | 先處理 `/sod/verify_security_arm_A` 與 chain 的已證實矛盾；**不更動 owner 指定 chain**。 | 低 | 修正讀者會誤信的現行宣告。 |
| 2 | 把跨欄位檢查納入既有測試，補「矛盾非零、未知值不假綠」。 | 低～中 | 把本次漏檢變成可持續攔截的回歸測試。 |
| 3 | 盤點並納版既有 dispatcher／policy／binding 工具的最小相依集。 | 中 | 解決工具在磁碟、乾淨 checkout 卻不可重現的核心缺口。 |
| 4 | 從 epoch-23 selfcheck 抽出 stdout-only、參數化的唯讀檢查。 | 低～中 | 可反覆健康檢查，不連帶寫 receipt／跑整套工程。 |
| 5 | 抽取 packet gate 的非憑證純檢查核心，淘汰平行變體。 | 中 | 減少 manifest、換行與發佈主張錯誤。 |
| 6 | references 僅整理一個「無引用、已量測」的小主題群。 | 中 | 降低找資料成本；不追求一次把全部檔數壓到門檻。 |

**不列入本次優先序：**真實 guarded apply 授權接線、mirror builder、全面 skill 重寫、全面 CI／harness 擴建。現有證據不足以把它們列成低阻力落地項。

### 附：Hermes 實體 SKILL 名稱清單

已用 `Path.rglob('SKILL.md')` 逐份解析 frontmatter；以下共 78 份。這是磁碟清單，不代表全部都在本 session 啟用。

| 分類 | `name` |
|---|---|
| apple | apple-notes、apple-reminders、findmy、imessage |
| autonomous-ai-agents | claude-code、codex、computer-use、hermes-agent、opencode |
| creative | architecture-diagram、ascii-video、baoyu-infographic、claude-design、design-md、humanizer、manim-video、p5js、popular-web-designs、songwriting-and-ai-music |
| devops | sdlc-review |
| email | email-inbox-triage、himalaya |
| 根層 | governed-write-admission、hgk-lifecycle-admission |
| media | gif-search、songsee、youtube-content |
| note-taking | obsidian |
| productivity | airtable、box、document-to-action-items、docx、google-workspace、maps、meeting-action-items、notion、pdf、powerpoint、product-price-monitor、teams-meeting-pipeline、weekly-review-planning、xlsx |
| research | arxiv、competitor-news-monitor、grounded-citations、llm-wiki |
| sbl | commander-sp、external-challenge-sp、hgk-governed-runtime、sbl-stack、tpm-sp |
| social-media | xurl |
| software-development | adversarial-verification-rounds、canonical-change-landing、codebase-inspection、destructive-path-guards、dogfood、github、governed-stack-audit、hermes-agent-skill-authoring、hgk-enforcement-closure、hgk-governed-execution、hgk-kanban-and-lane-routing、inspecting-hermes-desktop-dom、long-running-worker-supervision、lossless-content-consolidation、node-inspect-debugger、provider-routing-triage、python-debugpy、python-package-distribution、remote-repo-publication、requesting-code-review、simplify-code、spike、systematic-debugging、test-driven-development、windows-lane-verification-audit |
| web | blocked-page-recovery |

**HGK 與 Hermes 的對應裁決：**名稱零重複，但語意有交集，例如 `wp-task-route` 對 `hgk-kanban-and-lane-routing`、`security-evidence-readback` 對驗證類 skill、`loop-checkpoint-recover` 對 worker supervision。建議維持「HGK 保存規範契約、Hermes 保存操作方法」，不要為去重而合併權限與操作層。

**執行揭露：**本回合未建立或修改交付檔案、未 apply／commit／push／promotion；只做讀取及無檔案寫入的記憶體測試。第一次全樹遞迴因深層環境副本與路徑錯誤失敗，後改為有界掃描；因此本裁決不是所有 `var/` 深層副本的完整安全認證。