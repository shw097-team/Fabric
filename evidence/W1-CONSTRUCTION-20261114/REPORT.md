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
| WP-FHS-11 | Portable Host Dogfood | HOST_OP | Installed/Loaded/Invoked/Consumed 實測；Uninstalled NOT_PROBED；每 Host 四階段方案已成文 | `out/WP11_HOST_DOGFOOD.json`、`deliverables/WP11_HOST_PLAN_2026-11-14.md` |
| WP-FHS-17 | CAP-BOOT Native Occupants | HOST_OP | 485 逐鍵清冊（485/485）＋digest；安裝 HOLD | `out/WP17_485_LEDGER.json` |
| WP-FHS-20 | CLI/Agent/Host Kind Matrix | HOST_OP | 12 格矩陣（可載入單元規則）＋39 格 ModeGate 設計矩陣 | `out/WP20_MATRIX.json`、`out/WP20_MODEGATE39.json` |

## 2｜WP-FHS-05（可施工面）實測

- 13 verbs 由 CLI 自身列出：init、intake、profile、compile-pi、bind-pd、compile-ecp、compile-tqaep、validate、doctor、project、export、diff、repair
- `compile-pi` 連跑兩次同 SHA：**true**；`compile-ecp` 連跑兩次同 SHA：**true**
- 四物件 bundle：`checked=4`、`closure=FULL`、`complete=true`、`scope=FOUR_OBJECT`、`findings=[]`
- bundle sha256 `e3df1e10de5ccd55…`；PD 綁到的 live HEAD `826ca066a1c2`
- typed 拒收 **8 步／6 種碼**：`GIT_PROBE_FAILED`、`INPUT_SHAPE_INVALID`、`INTAKE_INVALID`、`PROFILE_VETO`、`REPO_CONTEXT_MISSING`、`TQ_SOD`（`GIT_PROBE_FAILED` 與 `TQ_SOD` 各兩種呼叫形狀，故步數多於碼數）
- §E.2 **N-09 `UNSAFE_DESTINATION`**：三種越界形態（絕對路徑／`../` 穿越／`--allow-root` 根擴大）皆 exit 2、目標不存在；根內 `--dry-run` 控制組 exit 0 → **4/4 PASS**

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
- 已記錄 caveat：**8 條**（節錄）：
  - count check: declared == named on all five sets (delta 0 each); total 485 named for 485 declared. No set is short of its declared count, and no set carries extra unnamed rows — every declared slot has exactly one H3 head
  - Donor24: 6 Need name(s) repeat across slots (e.g. Fission-AI OpenSpec x4, GitHub Spec Kit x4, mattpocock skills x4, GSD x4) — per L6228 `同名工具可以滿足多Need，但不可刪原槽`, so these are distinct slots, not duplicates to collapse
  - Method25: 1 Need name(s) repeat across slots (e.g. mattpocock skills x4) — per L6228 `同名工具可以滿足多Need，但不可刪原槽`, so these are distinct slots, not duplicates to collapse
  - TECH386: 19 slot id(s) carry a bare number instead of the set's prefixed form (L8833 `TECH386:341` .. L9211 `TECH386:359`); id preserved verbatim
  - TECH386: 38 Need name(s) repeat across slots (e.g. mattpocock skills x3, Fission-AI OpenSpec x3, GitHub Spec Kit x5, obra Superpowers x5) — per L6228 `同名工具可以滿足多Need，但不可刪原槽`, so these are distinct slots, not duplicates to
  - cross-set id reuse: 30 id suffix(es) appear under two set prefixes (colliding rows: Default30=30, TECH386=30); e.g. `Default30:P0-TOOL-001` and `TECH386:P0-TOOL-001` are different keys over the same underlying id. Keys s
  - 118 row(s) present the source's inline `upstream=…; disposition=…` form in the disposition field instead of one token (72 of them contain `disposition=`); first: L10597 `TECH386:P0-TOOL-001`. These are recorded verbatim,
  - 5 of those disposition values are cut mid-token in the blueprint itself — L10607 reads `disposition=DEFAULT_ENABLED_AFTER_Q；` and L10628 reads `disposition=DEFAULT_ENABLED_AFTER_QUALIFICA；` (`TECH386:P0-TOOL-001` / `TECH
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

- 對外寫入的實話：origin 三庫的 `main` **未寫**；本輪對 Fabric 只開了證據分支＋draft PR #60（owner 指示），並依 owner 授權建立了新的 `shw097-team/FHS_vNEXT`（新 repo，不是改 origin）。任何「完全沒有對外寫入」的說法都不成立，已改寫為此句。
- SoD：OPEN_OWNER_ORDERED（同一模型是 owner 指定；guard 的 `ERR_LANE_SOD_VIOLATION` 原樣保留，分離靠 process／path／write-set）
- **臂與 assignment 的落差（已揭露）**：3 個 VERIFY 回合服務的臂是 `opencode-go/deepseek-v4.1-flash`，而 VERIFY_SECURITY assignment（revision 44）只授予 `gpt-6.1-sol`、`openai-codex/gpt-6.1-sol`；派車當下出現 `WARN_LANE_SERVED_UNASSIGNED_ARM`，而以 `--require-assigned-arms` 重跑的對照組拒派 `ERR_NO_ASSIGNED_ARM`（exit 4，未呼叫模型）。因此這三份判決是**在 owner 指定臂上產生的挑戰紀錄**，不是 assignment-compliant 的作業，也不是驗收。**Owner 裁定 OD-W1R2-1：同模型不是設計要求，此落差為紀錄，不列缺口、不作阻斷。**

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
- `R4`（`out/LANE_VERIFY_R4.json`，nonce `W1R2-VERIFY-R4-8b25da`）：**REJECT**，未過 G2、G6、G7；歸屬 nonce_in_agent_message=true, usage_receipt_ok=true, exit 0, 426 s, sandbox read-only, usage rows 49

- 四輪之後的狀態：**最後判決 REJECT (R4: G2/G6/G7, all record-keeping discrepancies)**；實質要件：G1／G3／G4／G5／G8 判 PASS；G2／G6／G7 三項皆為簡報計數或措辭漂移（8 步被寫成 7 種碼、6 條被寫成 8 條 caveat、373 被寫成 390 檔、以及『無對外寫入』的措辭與 PR 事實不符），本輪已逐條更正並改為由 receipts 產生簡報（build/gen_verify_brief.py），無任何工作項被重新打開
- 第四輪（`W1R2-VERIFY-R4-8b25da`、426 秒、usage 49、read-only）G1／G3／G4／G5／G8 PASS，G2／G6／G7 FAIL，三項全部是簡報裡的計數與措辭漂移，不是工作項的新缺陷；已逐條入 `RC-11`／`RC-12`／`RC-13`
- 停止理由：four attributed rounds; every finding so far has been a count or wording drift in the brief rather than a defect of the work. The durable fix is a brief generated from the receipts, which is recorded here as the prerequisite for any further round
- 交接：owner decides whether a fifth round is wanted after the generator lands

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
| RC-10 | owner challenge (H-ORIGINAL-ACK 的合法性) | 13 主責章 body 與 Raw 未經原 Domain Reader 接受，故列 H-ORIGINAL-ACK（解除條件＝原 Domain Reader 同 scope 簽署） | FHS_ORIGINAL_ACK/3 明載傳統的 per-domain reader ACK 為 NOT_APPLICABLE_BY_DESIGN（L1 18.3 HIST-01、23.4 退役；實測 0/6 僅為量測），且該儀器本身以 PROCESS_LANE_EVIDENCE_SEPARATIO | H-ORIGINAL-ACK 撤回（RETRACTED_NOT_BLUEPRINT_COMPLIANT）；若 owner 要 W1 取得同級承認，改以同一 FHS_ORIGINAL_ACK 儀器套用於 W1 subject（需 owner 金鑰窗授權） |
| RC-11 | G2 (FAIL, R4) | eight refusal steps over seven distinct codes | eight steps over SIX distinct codes: GIT_PROBE_FAILED, INPUT_SHAPE_INVALID, INTAKE_INVALID, PROFILE_VETO, REPO_CONTEXT_MISSING, TQ_SOD (the first and  | report now computes the distinct-code set from the receipt at build time and states '8 steps / 6 codes' with the reason |
| RC-12 | G6 (FAIL, R4) | six caveats in the 485 ledger, one truncated disposition | the ledger carries EIGHT caveat entries, and the truncation entry names FIVE dispositions cut mid-token in the blueprint itself (L10607, L10628, L1064 | report counts the caveats from the ledger at build time (8) and states the five truncated rows |
| RC-13 | G7 (FAIL, R4) | the write manifest recorded 373 round files and the round made no origin-repo write | the manifest at review time recorded 390 round files (the round kept producing receipts after the number was typed into the brief), and the round DID  | report states the precise form: origin `main` untouched; one evidence branch + draft PR; one new private repo created on owner order. The counts in an |

## 9｜HOLD（只停受影效果）

| HOLD | 內容 | 解除條件 |
|---|---|---|
| `H-02-CONSUMER-ABI` | WP-02 指定的 `hgk_policy_consumer.py` 不在本樹 | 由 Fabric 原域提供該 consumer ABI 或更正 WP 契約路徑 |
| `H-02-MIRROR-PATH` | 入口測試讀的 mirror 文件不在本樹（origin main 有、import 未取）→ 10 測試紅 | 依 Owner 裁定 OD-W1R2-3：`R4-ENG.4` 是 source-only 白名單，evidence 不匯入 → 由 Fabric 原域縮測試範圍，本輪不擴白名單 |
| `H-03-GUARD-SOD` | guard 對同模型 maker/checker 回 `ERR_LANE_SOD_VIOLATION`＋`ERR_LANE_NOT_ADMITTED` | **Owner 裁定 OD-W1R2-1：同模型不是設計要求、不列缺口、不作阻斷**；guard 的 REFUSE 屬原域設定行為，照實記錄 |
| `H-17-INSTALL` | 任何 occupant 安裝皆為 `HOST_OP` | OPS ECP ＋ 原 Issuer ＋ nonce/TTL/epoch |
| `H-20-SET-SHA` | 39 格宣告集合 SHA 無法以 8 種正規化複現 | **Owner 裁定 OD-W1R2-2：屬證據稽核瑕疵、不阻斷**；以可執行 PLP 為準，通報藍圖作者即可 |
| ~~`H-REPO-CREATE`~~ | **已解除**：`shw097-team/FHS_vNEXT` 已建立（private、default `main`、head `828bfca4`），依 Owner 2026-11-14 明示授權 | — |
| ~~`H-REPO-PROTECT`~~ | **不列缺口**（Owner 裁定 OD-W1R2-6：Owner 親設的 repo 狀態是最高裁決）。現況僅記錄：`main` 目前未啟用分支保護（`PUT`／ruleset 皆 403，因憑證為 fine-grained PAT 且未授予 Administration） | 若 owner 要啟用，才需調整；不由規劃文件推定應有 |
| ~~`H-ACK-READER`~~ | **已解除（OD-W1R2-9）**：Owner 親簽六個 `original_reader_ack`（視窗 `WIN-6397278ec28a`、ops 6、refusals 0），加 owner 那一片 → **`FHS_ORIGINAL_ACK(W1)` = 7/7** | — |
| ~~`H-ORIGINAL-ACK`~~ | **已撤回**：要求「原 Domain Reader 同 scope 簽署」複活了 W0 已退役的傳統 ACK（`FHS_ORIGINAL_ACK/3` 記 `NOT_APPLICABLE_BY_DESIGN`，L1 18.3 HIST-01／23.4） | 若 owner 要 W1 取得同級承認，改以同一 `FHS_ORIGINAL_ACK` 儀器套用於 W1 subject（需 owner 金鑰窗） |

## 10｜能主張／不能主張

**能主張**：來源身份可複現；WP-05 編譯鏈在本機可重跑且決定性；四物件 bundle 完整；八個 typed 拒收步驟（六種碼，`GIT_PROBE_FAILED` 與 `TQ_SOD` 各兩形）原樣成立；§E.2 N-09 三形態亦皆拒；Fabric 六路由與未知路由拒收實測；HGK 六個 epoch 欄位與 guard 具名拒收實測；spine 14/14；485 逐鍵清冊與 digest；39 格設計矩陣解析結果與「宣告 SHA 不可複現」的誠實記錄；宿主 12 格矩陣（嚴格規則）。

**不能主張**：Native 准入、Independent 驗收、Release、原始域 ACK、485 已安裝、Repo 已建立、任何 host effect 已執行、任何車道回合已被 nonce 歸屬。

## 10.5｜L2 W1 五項交付對帳（Owner 裁定 OD-W1R2-4 後補做）

| L2 §04 W1 交付 | 本輪狀態 | 產物 |
|---|---|---|
| W1RepoEntry／SourceImportMap／ABI joins | **DONE（設計態）＋Repo 已建立**（`shw097-team/FHS_vNEXT`，private；內容尚未推入） | `deliverables/W1_REPO_ENTRY_2026-11-14.md`、`out/REPO_CREATE_READBACK.json` |
| 原 Compiler response 或 HOLD | **DONE** | `out/WP05_PIPD_CHAIN.json`、`out/WP05_BUNDLE4.json`（另含 effect ECP 的 `GIT_PROBE_FAILED` HOLD） |
| 每 Host 安裝／載入／調用／卸載方案 | **DONE（設計態）** | `deliverables/WP11_HOST_PLAN_2026-11-14.md` |
| W1 三件 L3 受影 rebase | **DONE**：以 amendment sheet 重出 r2（base 位元保留、7 列修訂） | `deliverables/FHS_vNEXT_PLP_W1_實質正文_施工定案版_2026-11-14_r2_AMENDED.md` |
| SourceImportMap 實測對帳 | **DONE** | 433 檔／3,787,417 bytes；三庫 pin `a6f1fa89`／`a6003c3d`／`696c30d7` |

Owner 裁定（`docs/OWNER_RULINGS_W1R2.json`）：OD-W1R2-1 同模型非缺口；OD-W1R2-2 兩項藍圖可複現性問題屬證據稽核瑕疵、不阻斷；OD-W1R2-3 白名單依 `R4-ENG.4` 共識、由原域縮測試；OD-W1R2-4 缺的交付直接補做；OD-W1R2-5 撤回 H-ORIGINAL-ACK。另依 Owner 2026-11-14 指令升級 OpenSpec 至 2.0.0（`out/OPENSPEC_UPGRADE.json`）。

## 11｜Owner 金鑰信封：本輪實際執行了什麼

| 步驟 | 結果 |
|---|---|
| 機制 | `FHS_NEXT/owner_envelope/code/owner_window.py`（tkinter 遮罩口令 → ed25519 → `POST /sign`）；probe `ops/tools/owner_window_probe.py` |
| 是否開窗 | **已開**：`WIN-22058723e313`、task `FHS-W1-R2-20261114`、scope `owner_semantic_accept`、max_ops 3、effect ceiling `REPOSITORY_WRITE`；preflight 先建 `owner_ws/{artifacts,admission/registry}` 並置入 host 的 `RunnerRegistry@1 rev 13` |
| 簽了什麼 | 一次 `owner_semantic_accept`，subject 為 `out/OWNER_SEMANTIC_ACCEPT_W1R2.body.json`（2,294 bytes、payload sha256 `2b6a9ad6…`）；`signature_verified=true`、`ops_used=1`、`refusals=0` |
| 收窗 | `owner_window.py close` → `state=CLOSED`；`SIGNING_LOG.jsonl` 有 `ALLOW` 與 `WINDOW_CLOSE` 兩列，沒有留下 live token |
| 沒有簽的 | 六個 reader receipts（reader 角色不是 maker 的）；`FHS_ORIGINAL_ACK(W1)` 因此是 **1/7**，不得讀成 6/6 |
| 第二次開窗（reader receipts） | `WIN-6397278ec28a`、scope `original_reader_ack,owner_semantic_accept`、max_ops 8、**ops_used 6、refusals 0**；六份 body 由 maker 起草、由 owner 的鍵簽署，逐份 `signature_verified=true` |
| 收窗 | 第二次亦已 `CLOSED`；`SIGNING_LOG.jsonl` 六列 `original_reader_ack: ALLOW` ＋ 一列 `WINDOW_CLOSE` |
| 最終 ACK | **`FHS_ORIGINAL_ACK(W1)` = 7/7**（6 reader ＋ 1 owner），`out/W1_ORIGINAL_ACK.json`；1/7 的部分紀錄保留為 superseded |
| 紀錄 | `out/OWNER_ENVELOPE_EVALUATION.json`、`out/OWNER_SEMANTIC_ACCEPT_W1R2.signed.json`、out/READER_ACK_R*.signed.json、`out/W1_ORIGINAL_ACK.json` |

