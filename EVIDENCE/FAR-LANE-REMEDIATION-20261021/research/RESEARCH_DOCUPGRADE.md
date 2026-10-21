## 升級清單

**結論：採最小範圍更新，不全面重寫。** `AGENTS.md` 的主要 lane 宣告已對齊 epoch 23；真正需要修的是來源 revision、SoD 衝突編號、README 的「現況／歷史」分層、MiniMax 探測狀態與對外鏡像缺口。**不能把歷史 epoch 17／18 全部替換成 23，也不能把 MiniMax 探測成功寫成正式預設已升級。**

以下 `HG/` 指 `C:\Projects\Agent_Workspace\HG-KSEOS`，`Fabric/` 指 `C:\Projects\Agent_Workspace\Fabric`。阻力為依變更範圍估計，非工時承諾。

### 一、AGENTS.md

已完整讀取 **178 行**。

| 檔案 | 行號／區段 | 現況文字（引用） | 問題 | 建議改寫 | 必要性 | 預估阻力 |
|---|---|---|---|---|---|---|
| `HG/AGENTS.md` | L3 | `Version: 2026-10-15.1`；`epoch 18 owner chains` | 版本摘要仍停在 epoch 18，但正文 L49 已標示 epoch 23。 | 在實際修訂時更新文件版本；摘要改為「本次對齊 epoch 23 owner chains、來源 revision 與 SOD006-C4；先前規則未變更部分繼續適用」。 | 必須 | 低：純文件 |
| 同上 | L51 | `config/model-lane-assignment.json`, `revision 18` | registry 的 `source_of_routes.revision` 已是 **23**，不是 18。 | 「lane 路由政策入口為 `config/lane-routing-registry.yaml`；其 source pin 指向 `config/model-lane-assignment.json` revision 23。派送候選集另由 pool 提供，須與政策及回合 mandate 一致。」 | 必須 | 低；需同步對照 registry |
| 同上 | L57 | `SOD006-C2 … OPEN_OWNER_ORDERED` | C2 在 registry 已是 `SUPERSEDED`；目前 PLAN／VERIFY 同模型衝突為 **C4**。 | 「PLAN／VERIFY 共用預設模型的現行衝突為 `SOD006-C4: OPEN_OWNER_ORDERED`；C2 保留為已被取代的歷史紀錄。此配對僅具程序分離，不主張 model-axis independence。」 | 必須 | 低 |
| 同上 | L54、L57 後 | `EXECUTE … default opencode-go/deepseek-v4.1-flash` | **政策宣告正確**，但未揭露 pool 已插入 MiniMax 探測臂，容易把「宣告預設」誤當「所有派送入口的首個候選」。 | 保留 DeepSeek 預設；增補：「MiniMax `opencode-go/minimax-m3.1-flash-free` 已完成特定 Codex CLI 探測；目前為 `PROBE`，不是本段正式預設的替代。實際派送須記錄 pool、rank、mandate 與 required／served arm。」 | 必須 | 中：須先釐清探測 pool 是否應留在共用預設路徑 |

**已正確、不要因升級而重寫的段落：**

| 行號／區段 | 實際原文／判讀 |
|---|---|
| L49 | `Lane-chain contract (current, epoch 23)`：與 registry L10 `epoch: 23` 一致。 |
| L53 | PLAN：`openai-codex/gpt-6.1-sol`，medium、OAuth，Hermes-internal；與 registry L56–62 一致，後備順序亦一致。 |
| L54 | EXECUTE：DeepSeek → Luna → NVIDIA DeepSeek；與 registry L115–157 的宣告鏈一致。**不因此證明各後備目前可服務。** |
| L55 | VERIFY_SECURITY：GPT medium、Codex CLI；明列 `SOD006-C4 OPEN_OWNER_ORDERED`，與 registry L165–171、L290–300 一致。 |
| L57 前半 | `exit 6, ERR_MANDATE_ARM_UNRESOLVED`：程式 L208–223 確有 chain 缺臂拒絕分支；binary 版本 `0.163.0-alpha.10.2` 與設定 L9–11 一致。此次只核對宣告，未重新執行 binary。 |
| L35–47 | `required ＝ served`、禁止靜默換臂、禁止空泛通過等規則，不因模型方案增加而失效。 |
| L6–33、L59–178 | 無其他固定 epoch／模型鏈需要因本次升級機械替換；保留 control-plane、admission、maker≠checker、advisory 與 Stage 邊界。L137–149 描述特定 checker adapter，不宜改寫為所有 lane 已有模型獨立性。 |

### 二、HG-KSEOS README 與 docs

| 檔案 | 行號／區段 | 現況文字（引用） | 問題 | 建議改寫 | 必要性 | 預估阻力 |
|---|---|---|---|---|---|---|
| `HG/README.md` | L7–10，頁首 | L8 `PLAN 重綁為 … deepseek…（registry epoch 17）`；L10 `registry epoch 18` | 都是具日期的回合紀錄，本身不是錯誤；但缺少置頂現況，冷啟動讀者容易沿用舊模型或舊待決項。 | 在歷史摘要之前新增：「**現行路由政策快照**：registry epoch 23／assignment revision 23；PLAN＝GPT medium OAuth／Hermes，EXECUTE＝DeepSeek／Codex CLI，VERIFY_SECURITY＝GPT medium OAuth／Codex CLI。PLAN／VERIFY 的模型軸分離缺席，記為 SOD006-C4。以下日期段落為當時紀錄，不代表目前預設或目前待辦。」 | 必須 | 低 |
| 同上 | §2d，L68–78 | L72 `已生效（W1／W2）：PLAN … 重綁為 … deepseek…`；L75 `epoch 16→17`；L76 `owner acceptance NOT_RUN` | 「已生效」易被誤讀為現況；但不能把當時 PARTIAL、rollback 問題改成今日 PASS。 | L72 改成「**該回合當時已生效（歷史）**」；段首增補「路由後續已被取代，現況見頁首；本節 PARTIAL／NOT_RUN 及當時位元綁定上限維持原紀錄」。保留 L75 的歷史 epoch。 | 建議 | 低 |
| 同上 | L10 | `canonical binary pin … 三項 owner-gated 待決` | 在該回合歷史中合理；但 AGENTS L57 與 binary 設定已記錄後續修復，缺少後繼指引。 | 附註：「此處為 2026-10-15 當時待決項；binary pin 的後續宣告修復見 FAR-REMEDIATION-20261021／AGENTS lane-chain contract；其餘項目不因該修復自動關閉。」 | 建議 | 低 |
| 同上 | §7，L110–117 | `Direct`／`Kanban`／`Swarm`／`Codex` | 此節**沒有** `2026-10-12` 或 epoch 17；不能把它列為已發現的舊日期錯誤。可補強任務路由與模型選擇的區別。 | 加一句：「本節分類決定協作形狀，不決定模型臂；模型政策、pool 與 per-turn mandate 分別核對，不以本節覆寫 owner chain。」 | 建議 | 低 |
| `HG/docs/HG-KSEOS使用說明文檔.md` | L59、L162 | `provider opencode-go、model deepseek-v4-flash` | 舊模型名稱與 `config/hermes.json` L28–30 的 `deepseek-v4.1-flash` 不同；同時文件未區分一般 runtime binding 與 governed PLAN profile。 | 「一般 runtime provider route 的設定宣告為 `opencode-go/deepseek-v4.1-flash`；governed PLAN／Orchestrator 另依 profile 與 lane registry 宣告為 `openai-codex/gpt-6.1-sol`。設定宣告不等於當前 session 已服務模型。」 | 必須 | 中：須分清兩個入口，不能直接全部換成 GPT |
| 同上 | §33，L497、L499、L501 | `v2026.10.15-r1`／`epoch 17→18`；`v2026.10.13-r1`／`epoch 16→17` | 是 changelog，不是應覆寫的現況。 | 保留原文；待修訂實際完成後新增一筆日期化紀錄，列明來源 revision、C4、MiniMax 的探測上限及文件修訂範圍。 | 建議 | 低 |
| 同上與 README | User Guide L57–58 對 README L121–122 | `Stage-2 externally accepted`／`Next gate SQP1` 對 `SELF_HOSTING_CUTOVER / FROZEN_PRESERVED`／`KG1 … DEFERRED_TO_RP002` | 有現況表述不一致，但本次未讀取 RP-002 全部權威狀態，不能裁定哪邊應取代哪邊。 | 統一加註：「RP-002 現況與 executable gate 必須 fresh-read 對應權威工件；本頁保留的歷史驗收與 runtime baseline 不構成新階段授權。」實際狀態更新另待核實。 | 建議 | 中：跨階段權威查證 |

### 三、Fabric 對外鏡像與 INTEGRATION

已讀取 `Fabric/README.md` 與 `INTEGRATION/` **全部 10 份 Markdown**。

| 檔案 | 行號／區段 | 現況文字（引用） | 問題 | 建議改寫 | 必要性 | 預估阻力 |
|---|---|---|---|---|---|---|
| `Fabric/README.md` | L3–5、L38–41、L67–72 | `external engineer can plan a complete upgrade … repository alone`；發布紀錄至 `2026-10-14` | 舊發布紀錄不應改日期冒充新發布；但目前缺少 epoch 23 的可攜路由資料，無法支持最新 lane 升級規劃。 | 增列「路由資料時效」與後續發布紀錄：明列 source commit、registry epoch、assignment revision、映射路徑與排除項。**未發布前**註明「現有鏡像不含 epoch 23 路由規劃資料」。 | 必須 | 中：需受審的鏡像再發布 |
| `Fabric/HG-KSEOS/AGENTS.md` | L3、L49–53 | `Version: 2026-10-10.1`；AO 規則後直接進入 `Files-first bootstrap` | 尚無本機新增的 lane-chain contract。 | 依核准發布範圍，同步**已修正**的 canonical AGENTS，保留來源 commit／digest；不得只複製目前仍含 revision 18／C2 殘留的版本。 | 必須 | 中 |
| `Fabric/HG-KSEOS/README.md`、鏡像 User Guide | README L7、L95–102；Guide L59、L162 | README 停留 AO 歷史摘要與一般自動路由；Guide 仍為 `deepseek-v4-flash` | 對外入口沒有現行 lane 快照，並保留舊 runtime 模型名稱。 | 同步上述現況／歷史分層與 runtime／PLAN 區別；歷史測試與 acceptance 紀錄不重寫。 | 必須 | 中 |
| `Fabric/INTEGRATION/DEPENDENCY-AND-CONTRACT-MATRIX.md` | L7 | `HG-KSEOS/config/, lane pool candidate` | 依賴表指向泛稱；實際檢查發現鏡像缺少 registry、assignment、pool 三個具名檔案。 | 改為可解析的公開路由契約／摘要路徑，包含 epoch、revision、owner authority、engine／auth 類別、fallback 狀態、C4、MiniMax 探測狀態。若不公開原始 config，明列「未公開」及規劃限制。 | 必須 | 中：需去機器狀態與安全審查 |
| `Fabric/INTEGRATION/SOURCE-PROJECTION.md`、`UPGRADE-PLANNING-GUIDE.md` | SOURCE L13–21；GUIDE L13–20 | `refresh … governed re-publication by scope`；`Reproduce the current state` | 再發布程序合理，但「current state」缺少來源版本時效檢查。 | 加入：「先核對 subject source commit、routing epoch／revision 與公開證據涵蓋範圍；過期或缺漏須列為 planning gap，不推測本機現況。」保留原始量測時間。 | 必須 | 低至中 |
| `Fabric/INTEGRATION/VALIDATION-AND-ROLLBACK.md` | L3–11 | 目前僅列 mirror、manifest、generated-file、publish-control、document-set 測試 | 對本次 lane 文件更新，缺少語意一致性與可解析來源檢查。 | 增加「路由契約摘要」列：正測＝模型／engine／epoch／C4 與來源一致；負測＝陳舊 revision、歷史被冒充現況、PROBE 被冒充 DEFAULT、引用缺檔均拒絕；rollback＝還原前一發布 commit。 | 必須 | 中 |
| `Fabric/INTEGRATION/LANE-INVOCATION-NOTES.md` | L9、L13 | 缺 arm 時可 `provider-direct … unsealed`；`Recorded 2026-10-13…` | 是歷史操作紀錄，但若被當通用處理，會與 AGENTS L39「點名 arm 不健康不 spawn、不靜默換臂」混淆。 | 保留歷史量測；補上「provider-direct 不是 sealed lane 的合格替代；只有另行明確授權的研究測試可用，不能據此滿足指定 lane 驗收」。 | 必須 | 低 |
| `Fabric/INTEGRATION/KNOWN-FINDINGS.md` | L3–5、L18–19 | `current status`；`Three values only` 卻列四值；K-10 缺 checker arm、K-11 長 prompt 未確認 | 四值的文字矛盾確定存在；K-10／K-11 是當時發現，不能僅因有新模型就自動判定解決。 | `Three` 改為 `Four`；每筆加「最後查證發布／證據版本」。對舊 finding 以後繼紀錄追蹤，不刪除原始缺陷或無證據改成 RESOLVED。 | 建議 | 低；重新判定狀態另需證據 |
| `Fabric/INTEGRATION/README.md`、`MANIFEST.json` | README L3–13；manifest L12–15、L52–54 | 索引有 readiness set；subject commit 僅 `see HG-KSEOS/ evidence` | 下一次發布若增加路由摘要，索引與 manifest 必須同步，不能只更新前頁。 | 索引加入公開路由契約；manifest 記錄精確 source commit／epoch／revision、實際發布集合及安全化方式。舊發布時間保留為歷史，不先改成尚未發生的新發布。 | 必須 | 中 |

`UPGRADE-SCOPE.md`、`APPROVAL-LIST-PROPOSAL.md`、`NON-CLAIMS.md` 沒有固定 lane 模型或 epoch，**不因本次模型方案新增而強制重寫**；仍須遵守其公開範圍、approval 與不構成驗收的限制。

### 四、repo 內 SKILLS 與 scripts 說明

| 檔案 | 行號／區段 | 現況文字（引用） | 問題 | 建議改寫 | 必要性 | 預估阻力 |
|---|---|---|---|---|---|---|
| `HG/control/skills/codex-bounded-execute/SKILL.md` | L18、L23–28 | 輸入只要求 `RBWI-09`；程序為一般 scope／fixture／receipt | 未硬編舊模型，故不是模型漂移；可補足派送前後核對，避免未來技能自行選新模型。 | 增補：「執行前解析 registry、pool 與 WorkOrder／role binding；固定被授權 arm／rank；收據核對 required／served arm。PROBE 不因一次成功即升格 DEFAULT。」 | 建議 | 低至中 |
| `HG/control/skills/provider-mcp-qualify/SKILL.md`、`security-evidence-readback/SKILL.md` | 各 L23–28、L54–55 | 一般 qualification／readback 程序；`DESIGN/MATERIALIZED_LOCAL`、runtime `NOT_EXECUTED` | 沒有舊 epoch／模型；可加入能力與服務證據的上限，但不能把文件更新當作技能已安裝／啟用。 | 前者補「同 engine／wire／account 的探測證據與 promotion 分開」；後者補「逐配對列出 model／process independence；C4 不得報為模型獨立」。保留 runtime 狀態，除非另有技能自身執行證據。 | 建議 | 低 |
| `HG/scripts/runtime_role_binding_assert.py` | docstring L13–24；實作 L208–237 | 範例只有 provider／model；聲稱 `all fail-closed with typed codes` | 說明落後於已存在的 `chain[]` 與 effort-axis 檢查。 | docstring 加入 chain、reasoning_effort、可選 served-effort；列明 chain 缺臂 exit 6、effort 類 exit 7，並引用 L50–58 的 `DECLARATION_ONLY` 上限。 | 建議 | 低：只改說明 |
| `HG/scripts/cred/README.md` | L43–54；對照 `ADMISSION_RECEIPT.md` L39–44 | `selftest.py → 5/5 PASS`；installation exchange `not exercised` | 證據層級易混淆；receipt 已明說 selftest 是歷史、未重跑，操作指引 L289–297 又有後續 App dry-run／ls-remote 紀錄。 | 標成「R9 歷史測試，非本次重跑」；增加後續操作指引連結，分開「standing install 未接 lane」、「App 曾手動驗證」、「lane activation 未證明」。 | 建議 | 低 |

補充查核：

- `HG/skills/` **不存在**；實際 repo 技能位於 `control/skills/`。已檢查其 **18 份 SKILL.md**，未命中 epoch、GPT／DeepSeek／GLM／MiniMax 固定模型綁定，**沒有全面換模型文字的必要**。
- `HGK_TMP_zen_fallback/skills/` 是另一組暫存技能副本，不應直接視為 canonical repo skill registry。
- `scripts/gcm-containment/README.md` L3–6、`scripts/cred/INSTALL.md` L8–11 都有限定回合與未啟用上限；不能因 lane 新增 MiniMax 就擅改成已啟用。

## 一致性風險

1. **把探測臂當成預設升級。**  
   pool L181–187：MiniMax 為 `rank: 1`、`role: PROBE/探測`；L190–196：DeepSeek 是 `rank: 2`、`role: DEFAULT/首選`。dispatcher L77 又將該 candidate pool 設為 `DEFAULT_POOL`。因此「政策預設仍是 DeepSeek」與「派送候選排序首位是 MiniMax」已不同，文件必須揭露，不能只改模型名稱遮蔽差異。

2. **誤認 PLAN／VERIFY 有模型獨立性。**  
   AGENTS L55 正確寫 C4；L57 卻仍寫 C2 開放。registry L261–267 明列 C2 `SUPERSEDED`，L290–300 明列 C4 `OPEN_OWNER_ORDERED`、`process separation only`。不修會讓稽核者追錯衝突。

3. **把 dated history 當現行命令。**  
   README L72「已生效」的 PLAN DeepSeek 與 registry L56–62 現行 PLAN GPT 不同；應標示時效，**不是消除當時正確紀錄**。

4. **把鏡像完整規劃承諾當成最新路由資料已公開。**  
   Fabric README L38–41 要求外部工程師不讀 private workspace 即能規劃；但實際鏡像缺少 registry／assignment／pool，matrix L7 仍指向 `HG-KSEOS/config/`。外部工程師無法從現有公開面重建 epoch 23 的選臂依據。

5. **把 registry 本身當成已完全一致。**  
   registry L14 已是 source revision 23，但 L11 仍寫 `dispatchable at revision 17`；L305 的 projection note 仍述 revision 22、PLAN GLM／VERIFY DeepSeek；L173–174 仍有 `selected_arm_identity: deepseek-v4.1-flash`，與 L166–169 GPT 主欄不同。**這些是來源內部殘留，不是只改 README 就能關閉的問題。** 建議另列具範圍的宣告一致性修復，不改歷史欄位湊綠燈。

## 主張上限

- **現行宣告的依據**：registry L9–15 為 `status: CANDIDATE`、`epoch: 23`、source revision 23；實際計算 assignment 檔案 digest 與 L15 相符。這證明來源 pin 對得上，**不證明所有 entry、binding、runtime session 都一致或已驗收**。
- **MiniMax 僅證明指定回合服務成功**：`var/FAR-REMEDIATION-20261021/probes/probe_MINIMAX_EXECUTE.json` L118 為 `"ok": true`，L125–126 的 required／served arm 均為 `opencode-go/minimax-m3.1-flash-free`；L117 明寫「not an acceptance of any subject」，L119–120 的 completion evidence 為 `"checked": false`。不能據此宣稱正式預設已切換、完整工具能力通過或產品驗收完成。
- **歷史判決不升格**：README L70、L76 的 `PARTIAL`／`owner acceptance NOT_RUN`，與 L10 的 `CANDIDATE_ONLY`，本研究沒有新增證據可改為 PASS。
- **未宣稱遠端已同步**：本次讀的是本機 Fabric checkout；未查遠端 branch／commit，也未發布鏡像。
- **執行範圍**：完成本機文件與相關設定／程式碼的唯讀比較；未執行 lane、測試、admission、promotion、SQP1 或 Stage-3。**未建立或修改任何 repo 檔案；交付物僅為本 stdout 清單。** `var/` 的一次廣域檔案搜尋失敗後，已改以具名回合目錄找到並讀取 MiniMax 收據。