# FHS vNEXT PLP W1｜施工輪 R2 結案報告（2026-11-14）

**工作區**：`<WORKSPACE>/FHS_NEXT_Workspace/W1_R2_CONSTRUCTION_20261114`
**WorkID**：`W1R2-b840e9285cbc407d`｜**施工依據**：`FHS_vNEXT_PLP_W1_實質正文_施工定案版_2026-11-14_r1`（sha256 `5cb9ebc5a768ecdf…`）
**語言／換行**：zh-TW／UTF-8／LF

```
SOURCE_READ / LOCAL_DRAFT_WRITE / LOCAL_CHECK / AUTHOR_DESIGN
NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / RELEASE_NOT_GRANTED
```

## 0｜這輪到底做了什麼（一句話）

把 W1 施工定案版的 8 個 W1 WP 真的跑過一輪：可施工的（WP-05／WP-07，`LOCAL_DRAFT_WRITE`）留下命令、退出碼與產物；唯讀的（WP-02／03／11／20）留下實測讀回與具名拒收；需要宿主效果的（WP-02/03/04/11/17/20 的 `HOST_OP`）停在各自的 FirstFail 與 HOLD，沒有以文件冒充效果。

## 1｜WP 狀態總表

| WP | 名稱 | EffectClass（原） | 本輪實際 | 證據 |
|---|---|---|---|---|
| WP-FHS-02 | Fabric Policy Consumer | HOST_OP | 唯讀觀測＋拒收；consumer ABI 缺席 → effect HOLD | `out/WP02_WP03_READONLY.json`、`out/FABRIC_ENTRY_UNITTEST.txt` |
| WP-FHS-03 | HGK Registry/Issuer | HOST_OP | 唯讀觀測＋guard 具名拒收＋spine 14/14 | `out/WP02_WP03_READONLY.json`、`out/WP03_HGK_SPINE.json` |
| WP-FHS-04 | Hermes Durable Runtime | HOST_OP | WorkID／Kanban／GSTACK／SWARM 帳；真 lease 佈線 HOLD | `out/WP04_RUNTIME.json`、`KANBAN_W1_R2.md` |
| WP-FHS-05 | PIPD Native Compiler | LOCAL_DRAFT_WRITE | 13 verbs 全鏈、PI/ECP 決定性、四物件 bundle 4/4 | `out/WP05_PIPD_CHAIN.json`、`out/WP05_BUNDLE4.json` |
| WP-FHS-07 | Native PLAN Commander A/B/C | LOCAL_DRAFT_WRITE | 三份 Guide（A 唯讀／B 隔離／C 禁止） | `deliverables/WP07_COMMANDER_ABC.md`、`out/WP07_COMMANDER_ABC.json` |
| WP-FHS-11 | Portable Host Dogfood | HOST_OP | Installed/Loaded/Invoked/Consumed 實測；Uninstalled NOT_PROBED | `out/WP11_HOST_DOGFOOD.json` |
| WP-FHS-17 | CAP-BOOT Native Occupants | HOST_OP | 485 逐鍵清冊（485/485）＋digest；安裝 HOLD | `out/WP17_485_LEDGER.json` |
| WP-FHS-20 | CLI/Agent/Host Kind Matrix | HOST_OP | 12 格矩陣（可載入單元規則）＋39 格 ModeGate 設計矩陣 | `out/WP20_MATRIX.json`、`out/WP20_MODEGATE39.json` |

## 2｜WP-FHS-05（可施工面）實測

- 13 verbs 由 CLI 自身列出：init、intake、profile、compile-pi、bind-pd、compile-ecp、compile-tqaep、validate、doctor、project、export、diff、repair
- `compile-pi` 連跑兩次同 SHA：**true**；`compile-ecp` 連跑兩次同 SHA：**true**
- 四物件 bundle：`checked=4`、`closure=FULL`、`complete=true`、`scope=FOUR_OBJECT`、`findings=[]`
- bundle sha256 `e3df1e10de5ccd55…`；PD 綁到的 live HEAD `826ca066a1c2`
- typed 拒收 8 筆：`INTAKE_INVALID`、`PROFILE_VETO`、`REPO_CONTEXT_MISSING`、`GIT_PROBE_FAILED`、`GIT_PROBE_FAILED`、`TQ_SOD`、`TQ_SOD`、`INPUT_SHAPE_INVALID`

### 2.1 本輪對施工依據的三處量測更正

| # | 依據原寫法 | 實測 | 影響 |
|---|---|---|---|
| C-1 | §B4.4 只列 TQAEP 三個必讀欄位 | 具名 checker 但**沒有** `--checker-receipt` 會 exit 2 `TQ_SOD`（「an independent checker must supply a checker_execution_receipt」） | 施工者若只給名字不給回執，拿不到 TQAEP；而給了偽回執會 exit 0 但封頂 `TQAEP_DESIGNED`／`NOT_GRANTED` |
| C-2 | §B4.3 以 `checked`／`complete` 描述 bundle | 不完整 bundle 仍回 `verdict=PASS`、`scope=PARTIAL_BUNDLE`、`complete=false` | 驗收必須讀 `complete`，不可讀 `verdict` |
| C-3 | 未提及 intake 對本文的限制 | 以 115 KB 施工正文作 `--source` 會 exit 2 `INTAKE_INVALID`（各有／分別／對應 的分派語法無法綁定主謂） | 施工需另備 goal card 作 intake 來源；正文仍為權威引用 |

## 3｜WP-FHS-02／03（唯讀面）

- Fabric 四不變量：`effect_permission=NONE` True、`unknown_route=HOLD_AFFECTED_WRITE_ONLY` True、`source_state=PROPOSED_NOT_OWNER_RATIFIED` True、歷史庫 `write_authority=NONE` True
- 六條已宣告路由 exit：`sbl_product`=0、`fabric_policy`=0、`hgk_admission`=0、`pipd_canonical`=0、`cross_repo`=0、`hermes_runtime`=0；未知路由 `not_a_real_task_class`=3
- WP 指定的 consumer ABI（`FABRIC/fabric/consumers/hgk_policy_consumer.py`）在本樹解析：**None** → 誠實缺口，effect 停 HOLD
- 入口自身測試：51 tests、5 failures + 5 errors，全部指向 `MIRROR_PATH_MISSING`。查核結果：該 mirror 文件在 origin `main` **存在**（668540 bytes、blob `dfa7f0e655b4`），而本樹 import 未取（`ORIGIN_HAS_FILE_IMPORT_LACKS_IT`、import map 宣告 `False`、policy `SOURCE_ONLY_WHITELIST`） → 這是 SOURCE_ONLY_WHITELIST 子集的必然結果，不是原域缺陷；本輪不改 origin，也不改 import 白名單

- HGK 六個 epoch 欄位：`registry.epoch`=41、`registry.contract_epoch`=41、`pool.revision`=37、`pool.epoch`=41、`assignment.revision`=44、`assignment.registry_epoch`=41
- lane guard：`decision=REFUSE`，具名碼 `ERR_LANE_NOT_ADMITTED`、`ERR_LANE_SOD_VIOLATION`、`ERR_LANE_STALE_EPOCH`（REFUSE 是控制面正常工作，不是本輪失敗）
- SharedSpine 沙箱 14 案：14/14 如預期

## 4｜WP-FHS-17（受保護分母）

| 集合 | named/declared | exact-key sha256（前 16） |
|---|---|---|
| Native20 | 20/20 | `ea19e6b71de22999…` |
| Default30 | 30/30 | `660f9ddc944356c8…` |
| Donor24 | 24/24 | `1182d308d175b899…` |
| Method25 | 25/25 | `df26b1ed00e00c15…` |
| TECH386 | 386/386 | `5fdd4f8f78d10edd…` |

- 合計 485/485，delta 0；合併 digest `b3cf9d40c8d710da…`
- 已記錄 caveat（節錄）：
  - count check: declared == named on all five sets (delta 0 each); total 485 named for 485 declared. No set is short of its declared count, and no set carries extra unnamed rows — every declared slot has exactly one H3 head
  - Donor24: 6 Need name(s) repeat across slots (e.g. Fission-AI OpenSpec x4, GitHub Spec Kit x4, mattpocock skills x4, GSD x4) — per L6228 `同名工具可以滿足多Need，但不可刪原槽`, so these are distinct slots, not duplicates to collapse
  - Method25: 1 Need name(s) repeat across slots (e.g. mattpocock skills x4) — per L6228 `同名工具可以滿足多Need，但不可刪原槽`, so these are distinct slots, not duplicates to collapse
  - TECH386: 19 slot id(s) carry a bare number instead of the set's prefixed form (L8833 `TECH386:341` .. L9211 `TECH386:359`); id preserved verbatim
  - TECH386: 38 Need name(s) repeat across slots (e.g. mattpocock skills x3, Fission-AI OpenSpec x3, GitHub Spec Kit x5, obra Superpowers x5) — per L6228 `同名工具可以滿足多Need，但不可刪原槽`, so these are distinct slots, not duplicates to
  - cross-set id reuse: 30 id suffix(es) appear under two set prefixes (colliding rows: Default30=30, TECH386=30); e.g. `Default30:P0-TOOL-001` and `TECH386:P0-TOOL-001` are different keys over the same underlying id. Keys s
- 這一列不是「已安裝」：安裝是 `HOST_OP`，需 OPS ECP ＋ 原 Issuer；本輪只交逐鍵登錄與處置

## 5｜WP-FHS-20（矩陣與 39 格）

- ModeGate39：rows=39／per_mode={'STANDALONE': 13, 'PREW3_SHADOW': 13, 'SWOF_CONNECTED': 13}／policies={'R': 14, 'C': 17, 'N': 4, 'F': 4}
- F 拒派恰為：PREW3_SHADOW__G07、PREW3_SHADOW__G08、PREW3_SHADOW__G11、PREW3_SHADOW__G12
- 宣告集合 SHA 複現：**DECLARED_SHA_NOT_REPRODUCED**（已試 8 種正規化；不改寫宣告值）
- 宿主矩陣：{'cells': 12, 'PRESENT': 1, 'NOT_INSTALLED': 11, 'NOT_PROBED': 0}；規則＝可載入單元（SKILL.md／plugin.json／manifest.json）
- 車道版矩陣已降級為 `CANDIDATE_MATCH_ONLY`：它把桌面 Electron 的 `challenge-window-ipc.ts` 判成 Hermes/Challenge 能力

## 6｜WP-FHS-11／07／04（宿主與編排面）

- 宿主鏈狀態：Installed=OBSERVED、Loaded=OBSERVED、Invoked=OBSERVED、Consumed=OBSERVED、Uninstalled=NOT_PROBED
- Hermes profiles：fhs_next(45 skills)、hgk-governed(48 skills)、default(90 skills)
- 三 Portable SP：TPM=PRESENT_IN_TREE、Commander=NOT_OBSERVED、Challenge=NOT_OBSERVED
- Commander Guide A/B/C：`<WORKSPACE>/FHS_NEXT_Workspace/W1_R2_CONSTRUCTION_20261114/deliverables/WP07_COMMANDER_ABC.md`（23947 bytes、sha256 `617d1e52b2840eb8…`、17 個 bash 區塊）
- 原生面：Kanban DONE 10／PARTIAL 2／PENDING 0；WorkID `W1R2-b840e9285cbc407d` 可續行

## 7｜車道（3L&M）與路由修正

- 走法：menu → bind → assert（三 lane 皆綁 `opencode-go/deepseek-v4.1-flash`），dispatch 直連 relay `127.0.0.1:10101`、role 預設沙箱（依 W0_R7 成功收據）
- 曾嘗試而撤回的兩條路：lane-scoped front door（啟動即拒 `ERR_EXEC_FRONTDOOR_DECLARATION_INVALID`）、`workspace-write` 沙箱升級（owner 裁示不走沙盒路由）
- 憑證：owner 的 `7776004_OPENCODEGO_KEY` 經 provider 判 `api_key_expired`；改以有效的 `shw097` key 經 vendor CLI 入池（舊 key 未覆寫、`config.json` 已備份）

| 收據 | 狀態 | 臂 | 秒 | nonce |
|---|---|---|---|---|
| `LANE_EXEC_WP20.json` | REFUSED | deepseek-v4.1-flash | 23.26 | False |
| `LANE_EXEC_WP20_R2.json` | SERVED_UNATTRIBUTED_NO_NONCE | deepseek-v4.1-flash | 371.35 | False |
| `LANE_EXEC_WP20_R3.json` | SERVED_UNATTRIBUTED_NO_NONCE | deepseek-v4.1-flash | 177.18 | False |
| `LANE_EXEC_WP20_R4.json` | TIMEOUT_NOT_ACCEPTED | deepseek-v4.1-flash | 420.04 | False |
| `LANE_VERIFY.json` | SERVED | deepseek-v4.1-flash | 533.45 | True |
| `LANE_VERIFY_R2.json` | SERVED | deepseek-v4.1-flash | 457.5 | True |
| `LANE_VERIFY_R3.json` | SERVED | deepseek-v4.1-flash | 343.64 | True |
| `LANE_VERIFY_ASSIGNED_ARMS_NEG.json` | REFUSED | None | None | None |

- SoD：OPEN_OWNER_ORDERED（同一模型是 owner 指定；guard 的 `ERR_LANE_SOD_VIOLATION` 原樣保留，分離靠 process／path／write-set）
- **臂與 assignment 的落差（已揭露）**：3 個 VERIFY 回合服務的臂是 `opencode-go/deepseek-v4.1-flash`，而 VERIFY_SECURITY assignment（revision 44）只授予 `gpt-6.1-sol`、`openai-codex/gpt-6.1-sol`；派車當下出現 `WARN_LANE_SERVED_UNASSIGNED_ARM`，而以 `--require-assigned-arms` 重跑的對照組拒派 `ERR_NO_ASSIGNED_ARM`（exit 4，未呼叫模型）。因此這三份判決是**在 owner 指定臂上產生的挑戰紀錄**，不是 assignment-compliant 的作業，也不是驗收。

## 8｜凍結 rubric 自檢結果

- `PASS`：8/8
  - F1 來源身份可複現：PASS（OK）
  - F2 WP-05 編譯鏈與決定性：PASS（OK）
  - F3 WP-02 Fabric 入口：四項不變量與未知路由拒收：PASS（OK）
  - F4 WP-03 HGK 平面：五個 epoch 欄位＋guard 具名拒絕＋spine 14 案：PASS（OK）
  - F5 WP-20 矩陣與 ModeGate39 設計矩陣：PASS（OK）
  - F6 WP-17 485 五集合逐鍵清冊不得湊數：PASS（OK）
  - F7 效果邊界：本輪不得執行 HOST_OP：PASS（OK）
  - F8 車道收據誠實：PASS（OK）

### 8.1 驗收挑戰的歷史（被拒的一輪保留在旁）

- `R1`（`out/LANE_VERIFY.json`，nonce `W1R2-VERIFY-4c81fe`）：**REJECT**，未過 G2、G3；歸屬 nonce_in_agent_message=true, usage_receipt_ok=true, exit 0, 533 s, sandbox read-only
- `R2`（`out/LANE_VERIFY_R2.json`，nonce `W1R2-VERIFY-d92a37`）：**REJECT**，未過 G7；歸屬 nonce_in_agent_message=true, usage_receipt_ok=true, exit 0, 457 s, sandbox read-only, usage rows 77
- `R3`（`out/LANE_VERIFY_R3.json`，nonce `W1R2-VERIFY-6f30bd`）：**REJECT**，未過 G7；歸屬 nonce_in_agent_message=true, usage_receipt_ok=true, exit 0, 344 s, sandbox read-only, usage rows 43

- 三輪之後的狀態：**最後判決 REJECT (G7 proxy clause only)**（僅 G7 的代理條款）；實質要件：G1-G6, G8 PASS in R3; G7's substantive property (no undisclosed outside write, no HOST_OP effect) holds with all 8 outside files disclosed in 3 classes
- 停止理由：three attributed review rounds with each finding repaired; the remaining item is a proxy clause, and re-running the rubric a fourth time would be an open-ended loop rather than convergence
- 交接：owner may accept or ask for the proxy clause to be restated; the round does not self-grant acceptance

| 更正 | 由誰提出 | 原主張 | 實測 | 處置 |
|---|---|---|---|---|
| RC-1 | G2 (FAIL) | the round recorded seven typed refusals | eight refusal steps with a typed code: INTAKE_INVALID, PROFILE_VETO, REPO_CONTEXT_MISSING, GIT_PROBE_FAILED (effect-ECP with registry), GIT_PROBE_FAIL | report and handoff now state eight steps and name the two shapes; the registry-count remains 7 kinds and is stated as such |
| RC-2 | G3 (FAIL) | the mirror document named by the Fabric admission test is absent at origin HEAD too, so the entry has an origin defect | origin main a6f1fa89 HAS the file (668,540 bytes, blob dfa7f0e6…); this tree does not, and provenance/SOURCE_IMPORT_MAP.json never declared it (policy | verdict replaced by ORIGIN_HAS_FILE_IMPORT_LACKS_IT; the HOLD becomes an owner decision (extend the import whitelist or narrow the test), not a Fabric |
| RC-3 | BACKLOG item 1 | LANE_EVIDENCE.json listed three EXECUTE receipts | four exist; the R2 receipt (371 s, served, no nonce) was outside the enumeration list | the enumeration now covers R2, R3, R4 and the two VERIFY dispatches |
| RC-4 | BACKLOG item 3 | OCG_KEY_PROBE.json records the credential verdicts | that probe used urllib without the provider's required user-agent, so every credential answered HTTP 403 with an empty error code; the credential verd | OCG_KEY_PROBE.json is retained as a negative example of a non-oracle probe and is not cited as a credential verdict; the cited evidence is the curl re |
| RC-5 | G7 (FAIL, R2) | the round wrote exactly two artefacts outside the round folder (lane bindings and the relay key pool) | a third existed: FHS_NEXT/_local/W1_R2_CONSTRUCTION_POINTER.md. It WAS disclosed in out/WRITE_MANIFEST.json (added before the run), so it was not an u | the pointer (a non-evidence convenience) was withdrawn; out/WITHDRAWN_NAVIGATION_POINTER.md keeps its bytes and the reason; the tree now carries exact |
| RC-6 | self-check (ops/selfcheck.py POS-01), not by the review lane | the imported trees are byte-identical to the map (433 files) | after the lane dispatches, HG-KSEOS/config/hermes-codex-lane.json had grown 15,340 -> 15,526 bytes (CRLF added by the tooling; 186 lines), sha 8c21a80 | restored byte-identically from the map's declared source clone (sha ba357dcc…, 15,340 bytes) and re-ran selfcheck: 16/16 PASS; the hygiene pass also r |
| RC-7 | self-check (write manifest completeness) | exactly two outside-round exception classes exist | running the tree's own selfcheck/hygiene wrote two more files into FHS_NEXT/_local (their own output paths), so a third class exists: tree-tool output | the write manifest now registers three classes (lane bindings, relay credential pool, tree-tool outputs) and lists every member; no write is undisclos |
| RC-8 | G7 (FAIL, R3) | the round wrote exactly two outside-round exception classes | three classes / eight members: 4 lane bindings, 2 relay credential files, 2 tree-tool outputs (selfcheck and hygiene readbacks in FHS_NEXT/_local) | the manifest now lists all three classes and every member; no write is undisclosed. The frozen criterion is NOT edited — the round records that this c |
| RC-9 | dispatcher stderr on the R1 VERIFY receipt (WARN_LANE_SERVED_UNASSIGNED_ARM), re-measured | the three VERIFY rounds were nonce-attributed review turns on the mandated arm | the arm they served (opencode-go/deepseek-v4.1-flash) is NOT in the VERIFY_SECURITY assignment revision 44, which grants only ['gpt-6.1-sol','openai-c | every receipt now carries arm_in_assignment / assignment_arms / assignment_revision; the three verdicts are recorded as challenge records produced on  |

## 9｜HOLD（只停受影效果）

| HOLD | 內容 | 解除條件 |
|---|---|---|
| `H-02-CONSUMER-ABI` | WP-02 指定的 `hgk_policy_consumer.py` 不在本樹 | 由 Fabric 原域提供該 consumer ABI 或更正 WP 契約路徑 |
| `H-02-MIRROR-PATH` | 入口測試讀的 mirror 文件不在本樹（origin main 有、import 未取）→ 10 測試紅 | Owner 決定是否把 `INTEGRATION/FHS/docs/as-built/**` 納入 import 白名單，或由 Fabric 改測試範圍 |
| `H-03-GUARD-SOD` | guard 對同模型 maker/checker 回 `ERR_LANE_SOD_VIOLATION`＋`ERR_LANE_NOT_ADMITTED` | 原域在 assignment 宣告 owner-ordered 例外，或改派不同模型 |
| `H-17-INSTALL` | 任何 occupant 安裝皆為 `HOST_OP` | OPS ECP ＋ 原 Issuer ＋ nonce/TTL/epoch |
| `H-20-SET-SHA` | 39 格宣告集合 SHA 無法以 8 種正規化複現 | 由藍圖作者說明該 SHA 的演算法 |
| `H-ORIGINAL-ACK` | 13 主責章 body 未經原 Reader 接受 | 原域同 scope 簽署（本輪不得自簽） |

## 10｜能主張／不能主張

**能主張**：來源身份可複現；WP-05 編譯鏈在本機可重跑且決定性；四物件 bundle 完整；八個 typed 拒收原樣成立（含 `GIT_PROBE_FAILED` 的兩種呼叫形狀）；Fabric 六路由與未知路由拒收實測；HGK 六個 epoch 欄位與 guard 具名拒收實測；spine 14/14；485 逐鍵清冊與 digest；39 格設計矩陣解析結果與「宣告 SHA 不可複現」的誠實記錄；宿主 12 格矩陣（嚴格規則）。

**不能主張**：Native 准入、Independent 驗收、Release、原始域 ACK、485 已安裝、Repo 已建立、任何 host effect 已執行、任何車道回合已被 nonce 歸屬。

## 11｜Owner 金鑰信封：評估與結論

| 步驟 | 結果 |
|---|---|
| 機制搜尋 | `FHS_NEXT/owner_envelope/code/owner_window.py` ＋ `owner_prompt.py`（masked tkinter → ed25519 → POST /sign）；probe `ops/tools/owner_window_probe.py` |
| 機制狀態（實測） | `open=false、usable=false、window_id=WIN-077bbb5500b1、task=FHS-W0-R7-20261114、ops 2/6、已逾期` → 機制存在但當前關閉 |
| 本輪是否有 owner-key consumer | **沒有**：無原生准入、無 permit、無 release、無原 Reader ACK；唯一的簽署對象會是「本輪自撰 body 的 owner_semantic_accept」，那屬 maker 自簽，禁止 |
| 結論 | `NOT_OPENED / N_A_WITH_REASON`：開窗會製造一個沒人要求的簽章能力並留下 live token |
| 若要簽，僅剩一種 | 由 owner 親自對本報告做 `owner_semantic_accept`（owner 本人的行為，不是作者代簽） |

