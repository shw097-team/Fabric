# B1 PIPD-LS-PKG 00..08 — Round-2 evidence / acceptance（2026-10-27）

**主體**：`FHS_MSC_B1_PIPD_LS_PKG_00..08`，交付版 `2026-10-27_r3_DOC_REPAIR_CANDIDATE_1`（9 冊，1,534,736 bytes / 22,117 行）
**工作區**：`C:\Projects\Agent_Workspace\var\B1-PIPD-PKG-20261027`（候選／隔離）。四倉 tracked 修改數與前次基線相同（基線本身即有 HG-KSEOS 2 / Fabric 1 / SBL 4 / PIPD 0 個 tracked 修改，非本輪造成；本輪只新增三根 `evidence/review/` 的 untracked 鏡像）
**本檔為 round-2 唯一 evidence MD**，SHA-256 相同地鏡像到 HGK / Fabric / SQS 三個 `evidence/review/`。

## 1. Claim ceiling（七級不互借）

| 級 | 狀態 | 依據 |
|---|---|---|
| DOC_STATIC_PASS | **成立** | 前輪 `../artifacts/SELFCHECK.json` 44/44 + 本輪 `SELFCHECK_R2.json` 46/46（由該檔決定，不寫死）；分母兩條獨立實作重算一致 |
| SOURCEFREEZE_ISSUED | **HOLD** | 無 Owner signature |
| EXECUTION_ADMITTED | **NOT_RUN** | 無 runner registry、無 native-admission bootstrap |
| HOST_LOADED | **NOT_RUN** | 無 loaded-SHA readback |
| MODEL_SERVED | **PARTIAL** | 車道實跑（codex EXECUTE/VERIFY）有 provider 收據，但非 PLAN/EXECUTE/VERIFY 三 Lane 同 epoch readback |
| INDEPENDENT_PASS | **NOT_RUN** | AO 為 fresh-context 子代理，非同 Principal/credential，不得升格 |
| RELEASE | **NOT_RUN** | 未打包、未簽、未發佈 |

## 2. 逐族分母與實作面裁定

| 族 | 宣告 | 逐項列舉 | 實作面裁定 | 來源 |
|---|---|---|---|---|
| PI_ATOMS | 27 | 27 | DESIGN_ONLY=19, IMPLEMENTED=8 | LANE_D |
| EFFECT_SLOTS | 31 | 31 | DESIGN_ONLY=27, IMPLEMENTED=4 | LANE_D |
| GWO_GATE_STEPS | None | 31 | MISSING=24, NOT_RUN=6, EXISTS=1 | LANE_D |
| TQ_PARENT_CASES | 120 | 120 | RECOUNT_EQUAL=True, IMPLEMENTATION_HIT=0 | LANE_C |
| TQ_CHILD_CASES | 124 | 124 | RECOUNT_EQUAL=True, IMPLEMENTATION_HIT=0 | LANE_C |
| NODES | 38 | 38 | RECOUNT_EQUAL=True, IMPLEMENTATION_HIT=0 | LANE_C |
| R15_LEDGER | 949 | 949 | RECOUNT_EQUAL=True, IMPLEMENTATION_HIT=0, MISS=949 | LANE_C |
| PRODUCT_MATRIX_CELLS | 192 | 192 | RECOUNT_EQUAL=True | LANE_C |
| NAMED_ASSETS | 81 | 81 |  | LANE_C/D/A |
| CANONICAL_FAILURE_CODES | 27 | 27 | EXISTS=0, DEFECT=0, MISSING=27 | LANE_B |
| CLI_VERBS | 13 | 13 | DEFECT=4, EXISTS=9 | LANE_A |
| CONTRACTS | 19 | 19 | EXISTS=18, DEFECT=1 | LANE_A |
| METHODS | 25 | 25 | MISSING=23, EXISTS=2 | LANE_A |
| DONOR_SLOTS | 24 | 24 | EXISTS=12, MISSING=12 | LANE_A |
| DOC07_DEV04_EXTRA | 20 | 20 | EXISTS=4, MISSING=5, NOT_RUN=10, DEFECT=1 | LANE_A |

> 設計面分母（27/31/120/124/38/949/192/81）由 `build_index.py` 與 codex EXECUTE 車道各自實作重算，結果完全相同；VERIFY 車道另以 17 族逐項比對 `agree=true`。**實作面**（PIPD/HG-KSEOS/Fabric 內是否真有對應實體）則是另一條軸，數字見上表右欄。

## 3. 主機構件實測

| 構件 | 裁定 |
|---|---|
| gstack named-method | **可執行面存在**：10 條 `route(flow)` 回傳、evidence refs 8/8 存在、activation invariants 全 0=True；無獨立二進位 |
| OpenSpec | 1.8.0；`list` rc=0；`validate` rc=0（Change 'pipd-ls-sp-s0-s1' is valid） |
| Codex CLI | codex-cli 0.164.0-alpha.11.1
；PATH=NOT_ON_PATH
；經 sealed home + relay :10102 實跑 |
| owner-registered runner registry | **缺失**：九欄欄位特徵對掃 44990 檔 / 9 面 → NOT_FOUND_ON_NAMED_SURFACES |
| native admission registry | ProgramData 與 LOCALAPPDATA 皆無 `native-admission/registry.json`；`native_admission.py:161` 因此永遠 `        if not REGISTRY.is_file():refuse('TRUST_BOOTSTRAP_REQUIRED')` |
| Fabric activator | rp002 腳本存在但 root 缺 `FABRIC` 一層（3 份政策契約 0/3）；修補候選 R2-P03 控制 0/3→3/3 |

## 4. 修補（候選，未落地）

| ID | 檔案 | 缺陷 | 控制組（before → after） |
|---|---|---|---|
| R2-P01 | `PIPD/schemas/TechnologyAdmission.schema.json` | additionalProperties:false while DOC-07 line 160 mandates 10 keys that the schema lacks -> | ACCEPT 0 錯 / 缺欄 REJECT ≥1 / 多餘鍵 REJECT ≥1 |
| R2-P02 | `PIPD/src/pipd_ls_sp/registry.py` | validate_bundle({'NoSuchContract':{}) raises FileNotFoundError with code=None; the declare | FileNotFoundError(code=None) → VALIDATION_FAIL（ECP 正常載入） |
| R2-P03 | `Fabric/FABRIC/rp002/scripts/rp002_f0_policy.py` | FAB root is Fabric/ while the three policy contracts live in Fabric/FABRIC/{fabric,control | 3×False → 3×True |

## 5. 逐冊 findings（前次 F-01..F-09 重新裁定）

| ID | 前次結論 | 本輪裁定 | 量測 |
|---|---|---|---|
| F-01 | 交付件不在磁碟 source_path | **CONFIRMED_REFINED** | source_path 逐冊可解析且檔案存在，但 bytes 為 10-26 版（例：doc00 live=3096e980 / 10324B，candidate=b0583e03 / 16657B）；9/9 皆不同 |
| F-02 | supersedes_subject_sha256 等於自身 digest（×9 自我引用） | **REFUTED** | 九冊 top-level supersedes_subject_sha256 皆等於 10-26 baseline digest；declared_equals_own_digest=false ×9。前次為解析器把縮排 baseline_ |
| F-03 | body 行數 +180 | **NOT_RE_MEASURED** | 本輪只量測全包 22,117 行 / 1,534,736 bytes；未重跑 10-26 vs 10-27 逐冊 body diff |
| F-04 | R15 編號 R15-003..R15-951，非 1..949 | **CONFIRMED** | 949 個 ID，min=R15-003 max=R15-951，949 個 heading 行 |
| F-05 | 無 owner-registered runner registry | **CONFIRMED_STRENGTHENED** | 九欄欄位特徵對掃 9 面 44,990 檔 → 0 命中；另 native-admission/registry.json 於 ProgramData 與 LOCALAPPDATA 皆不存在 |
| F-06 | Codex CLI 不在本機；GStack 不存在 | **REFUTED_IN_PART** | codex-cli 0.164.0-alpha.11.1 存在於 %LOCALAPPDATA%\OpenAI\Codex\bin（僅不在 PATH），經 sealed home + 10102 relay 真跑 EXECUTE/VERIFY |
| F-07 | 自查器 4 處缺陷 | **ACCEPTED_PRIOR** | 未重驗；本輪另發現同類缺陷（見 N-09） |
| F-08 | STATE 與 SELFCHECK 計數漂移 | **CLOSED** | 重跑後 STATE.selfcheck 一律由 `SELFCHECK_R2.json` 派生（不在任何文件寫死總數） |
| F-09 | TQAEP child 缺 case_type 欄位 | **CLOSED** | 124/124 有 case_type，31/31/31/31 |

### 本輪新檢出

| ID | 嚴重度 | 內容 | 修補狀態 |
|---|---|---|---|
| N-01 | high | PIPD/schemas/TechnologyAdmission.schema.json 為 additionalProperties:false 且缺 DOC-07 強制的 10 個欄位，文件要求的 TechnologyAdmission 記錄會被自己的契約拒絕 | R2-P01 候選 |
| N-02 | high | validate_bundle 對未知 contract 抛裸 FileNotFoundError（code=None），宣告的 VALIDATION_FAIL 在此路徑不觸發；cli 會把它重標成 INPUT_SHAPE_INVALID | R2-P02 候選（before/after 已驗） |
| N-03 | high | Fabric rp002 F0 executor 的 FAB 根缺 FABRIC 一層，三份政策契約 0/3 命中，activator 不可用 | R2-P03 候選 |
| N-04 | high | 27 個 canonical failure code 在實作面 0/27；FAILURE_CODES（13 個斜線字串）與 errors.py（31 個類別）是兩個不一致的面向（10 個 dangling、10 個未曝露） | 需產品變更（本輪僅記錄） |
| N-05 | high | native-admission registry.json 不存在 → native_admission.py:161 永遠 refuse TRUST_BOOTSTRAP_REQUIRED，G-A/G-B/三張 GWO 無法開始 | Owner 簽章 bootstrap 後才可解 |
| N-06 | high | R15 949 個 ID 在 PIPD/HG-KSEOS/Fabric 實作面 0/949 命中；120 parent / 124 child / 38 node 亦 0 命中 | 設計面 vs 實作面落差，非本輪可修 |
| N-07 | high | 31 個 effect slot 只有 4 個有等義 handler（27 DESIGN_ONLY）；27 個 PI atom 只有 8 個 IMPLEMENTED | 產品缺口 |
| N-08 | medium | 24 個 donor slot 0/24 落地；25 個 method 只有 3 個有實體 | 產品缺口 |
| N-09 | medium | 前次 REPORT 的 F-02 判定為量測錯誤：frontmatter 解析器讀到縮排 baseline_lineage 的 version/supersedes 值 | 已修解析器並更正結論 |
| N-10 | medium | DOC-04 ECP payload 缺 8 個 schema 必要鍵、被拒 9 鍵，rollback 型別不符（schema 為 string，pipeline 產 object） | 文件側候選（未產出） |
| N-12 | medium | PIPD `init` 非冪等守衛：同一 root 第二次 init 仍回 PASS（無 INIT_CONFLICT） | 需產品變更（本輪只記錄） |
| N-13 | medium | PIPD `doctor` 在無 schema registry 的 root 上仍 PASS，並以未型別化例外崩潰（WinError 1920, workspace.py:208） | 需產品變更 |
| N-14 | low | PIPD `profile` 接受重複 `--axis` 而不回 PROFILE_VETO | 需產品變更 |
| N-15 | medium | 同一目標兩次量測不一致（LANE_A 首輪 interim 報 CLI 13/13 EXISTS、method 3/25；重跑落地為 CLI 9 EXISTS/4 DEFECT、method 2 EXISTS/23 MISSING），差異來自判定準則漂移（『存在實體』vs『該 ID 有對應 regi | 以準則標註取代靜默覆蓋 |
| N-11 | info | codex EXECUTE 未回 NONCE（輸出風格），VERIFY 有回；EXECUTE 的產出改以 VERIFY 的 17 族重算 + 檔案 digest 佐證 | 已在收據揭露 |

## 6. 車道收據（真實 spawn，非宣言）

| 車道 | 角色 | 時長 | nonce | 產出 |
|---|---|---|---|---|
| CODEX | EXECUTE | 172.4s | False | round2/codex/EXECUTE/RECOUNT.json, round2/codex/EXECUTE/recount_docs.py |
| CODEX | VERIFY | 160.9s | True | round2/codex/VERIFY/VERIFY_VERDICT.json, round2/swarm/LANE_C_DOC05_DOC06.json |


KANBAN 即時收據只有 162 行（其餘卡片是直接 CLI 呼叫，未經 recorder）；已另存 POSTHOC 快照：{"blocked": 1, "done": 22}，來源標記 `POSTHOC — read from the board DB through the CLI, not captur` → `round2/lane/KANBAN_RECEIPTS_POSTHOC.json`

| SWARM lane | rows | bytes | sha256(16) |
|---|---|---|---|
| LANE_A_DOC07_DEV04 | 101 | 77087 | b7ac2b071be0e28d |
| LANE_B_DOC00_DOC03 | 67 | 66963 | 0796c8d6bdd6e48f |
| LANE_C_DOC05_DOC06 | 39 | 25796 | 6deaf14308a55890 |
| LANE_D_DOC08_01_02 | 89 | 38020 | edb9575d3b301cf7 |

## 7. 驗收官（fresh context，非同 Principal — 不得升格為 INDEPENDENT_PASS）

| 輪 | 判定 | checked | overclaims | blocking |
|---|---|---|---|---|
| round 1 | `PARTIAL` | 7 | 0 | 3 |
| round 2 | `PARTIAL` | 7 | 4 | 2 |
| round 3 (final) | `PARTIAL` | 7 | 3 | 1 |

### round 1 — per-item
- item 1: `PARTIAL` — 重算 12 個族並全部重現：PI_ATOMS 27（DOC-01 有 27 個 ^### PI-B1- 標題、27 個 distinct id；LANE_D pi_atoms len=27）；EFFECT_SLOTS 31（DOC-02 有 31 個 ^### PD- 標題；LANE_D slots 31；EXECUTION_PROJECTION_CANDIDATE.slots 31）；TQ_CHILD 124（TQAEP_CASE_CATALOG.children=124，
- item 2: `PASS` — 對 round2 全樹 *.json/*.md/*.jsonl/*.txt/*.py 掃 已驗收|已通過測試|native 已生效|已部署|已上線|已 release|已發佈|Host 已載入|模型已 served|MISSION_COMPLETE|已生效，以及 MISSION_COMPLETE|DEPLOYED|GO_LIVE|RELEASED|HOST_LOADED|MODEL_SERVED|INDEPENDENT_PASS|SOURCEFREEZE_ISSUED。命中僅
- item 3: `PASS` — 三原檔 worktree sha256 == git HEAD blob，git status --porcelain 皆空：PIPD/schemas/TechnologyAdmission.schema.json 40703552…、PIPD/src/pipd_ls_sp/registry.py 733c003c…、Fabric/FABRIC/rp002/scripts/rp002_f0_policy.py b70e93a8…。候選 digest 全不同（b909c345…
- item 4: `PARTIAL` — 三組控制我自己重跑：(P01) 候選 schema + Draft202012Validator → ACCEPT_MANDATED 0 / REJECT_MISSING 1 / REJECT_EXTRA 1，與 REPAIR_RESULTS 逐字相同；同一 payload 對「原」schema 則給 1 個 additionalProperties 錯誤（十鍵 unexpected），且 REJECT_MISSING 0（原件不要求 source_id）。(P02) bef
- item 5: `PASS` — LANE_D gwo 31 步的 verdict 集合僅 {MISSING 24, NOT_RUN 6, EXISTS 1}，無 PASS/DONE/VERIFIED 等升格：G-A（GA1 MISSING, GA2 NOT_RUN, GA3–GA6 MISSING）、G-B 7 步全 MISSING、GWO-FABRIC 7 步、GWO-HGK 6 步、GWO-SBL 5 步皆 MISSING/NOT_RUN。唯一 EXISTS 為 GWO-SBL S3，其 missing
- item 6: `PASS` — EXECUTE 收據 nonce_present_raw_stdout=false 為已知限制；但工作可獨立確認：把 codex/EXECUTE/recount_docs.py 連同 input_20261027 複本搬到 scratch 重跑，產出的 RECOUNT.json 與受審檔 dict 完全相等（identical True；counts 27/31/108/124/38/949、totals 1,534,736 / 22,117 / 1,373 全同）。VERI
- item 7: `PARTIAL` — lane/KANBAN_RECEIPTS.jsonl 162 行：claim 9 次（8×rc=0，1×rc=1 status=running）、heartbeat 9×rc=0、complete 4×rc=0、reclaim 4×rc=0；但 complete 先有 5 次 rc=2（用錯 --body 觸發 usage 錯誤），改以 --force --result 才成功。kanban.db 唯讀查詢 23 卡：done 16（其後 17）/ready 3/todo 4

### round 2 — per-item
- item 1: `PASS` — Recomputed 8 families from the nine source documents, not from the receipt: PI_ATOMS 27 (^### PI-B1-[ABC][1-9]), EFFECT_SLOTS 31 (^### PD-\d\d), TQ_PARENT_CASES 120 (108+12 GWO), TQ_CHILD_CASES 124 (POS/NEG/EDGE/SEC 31 each), NODES 38, R15_
- item 2: `PASS` — Swept *.md/*.json/*.jsonl/*.txt/*.py for 已驗收|驗收通過|APPROVED|SIGNED|certified|已簽|native PASS|INDEPENDENT_PASS|已落地|landed|可上線|production-ready|correctness verified. The only INDEPENDENT_PASS hits are prohibitions: REPORT_R2.md:77 '未把 AO 子代理升格為
- item 3: `PASS` — Originals are still HEAD blobs: for PIPD/schemas/TechnologyAdmission.schema.json, PIPD/src/pipd_ls_sp/registry.py and Fabric/FABRIC/rp002/scripts/rp002_f0_policy.py the on-disk sha256 equals the sha256 of 'git show HEAD:<path>' (40703552…, 
- item 4: `PASS` — All three controls are now paired and I reran each: (P01) shipped schema -> 1 error / candidate -> 0 errors, plus candidate rejects missing key (1) and extra key (1). (P02) shipped registry -> 'RESULT FileNotFoundError code= None'; candidat
- item 5: `PASS` — Recomputed LANE_D.gwo: 31 rows, 31 unique (gwo_id,step), verdicts {MISSING 24, NOT_RUN 6, EXISTS 1}, groups GWO-FABRIC 7 / GWO-HGK 6 / GWO-SBL 5 / G-A 6 / G-B 7. No PASS/DONE/VERIFIED row exists; the single EXISTS is GWO-SBL S3 (CLI importa
- item 6: `PASS` — I copied round2 + input_20261027 to scratch, deleted RECOUNT.json and reran codex/EXECUTE/recount_docs.py: exit 0, output RECOUNT.json is byte-identical to the frozen one (sha256 0a097efa… on both, json equal True; counts 27/31/108/124/38/9
- item 7: `PARTIAL` — Board snapshot (23 cards: 20 done / 1 todo AO / 1 ready handover / 1 blocked native) matches the live kanban.db I copied: 20 completed events with completed_at, and every path named in each done card's result exists on disk (20/20 cards, 0 

round 2 對前一輪 blocker 的重測：
- blocker 1: `FIXED` — Recounted from swarm/LANE_A_DOC07_DEV04.json (101 rows, 101 unique ids): doc04 = 20 rows {EXISTS 4, MISSING 5, NOT_RUN 10, DEFECT 1}; doc07 = 81 rows {DEFECT 5, EXISTS 41, MISSING 35}. DETECTION.documents['04'].findings_bound=20 and documen
- blocker 2: `FIXED` — DETECTION.families.TQ_PARENT_CASES now carries split_note='108 heading-level parent cases (27 slots x 4 case types) + 12 GWO parents = 120'. I recounted from input_20261027/FHS_MSC_B1_PIPD_LS_PKG_05_DOC_B1_TQAEP-2.md myself: 108 headings ma
- blocker 3: `FIXED` — repair/REPAIR_RESULTS.json now contains R2-P01-before (out: BEFORE_MANDATED_ERRORS 1 / BEFORE_UNEXPECTED 1 / BEFORE_UNEXPECTED_KEYS 10) paired with R2-P01 (ACCEPT_MANDATED 0 / REJECT_MISSING 1 / REJECT_EXTRA 1). I rebuilt the mandated recor

### round 3 (final) — per-item
- item 1: `PASS` — Every DETECTION family tally recomputed from the artefact DETECTION names as its source and equal: PI_ATOMS 27 (LANE_D by_surface_atoms 8/19), EFFECT_SLOTS 31 (4/27, by_type 10/5/14/2), GWO_GATE_STEPS 31 (24 MISSING/6 NOT_RUN/1 EXISTS, grou
- item 2: `PASS` — Seven-level ceilings are held and not borrowed anywhere: REPORT_R2.md header (native_effect=NOT_RUN, formal_sourcefreeze=HOLD, independent_checker_receipt=NOT_RUN 'AO 為子代理', release=NOT_RUN), EVIDENCE §1 (SOURCEFREEZE_ISSUED HOLD; EXECUTION
- item 3: `PASS` — Candidate vs live digests all differ: 01 b909c345… vs 40703552…, 02 870c61a2… vs 733c003c…, 03 50b6d238… vs b70e93a8…. The three originals are still the HEAD blobs, not modified working copies: `git show HEAD:<path>` == worktree byte-for-by
- item 4: `PASS` — All three controls reproduced independently, not read from REPAIR_RESULTS.json. P01: I built a TechnologyAdmission record carrying the 10 keys DOC-07 §5 mandates (source_id, Need, existing_capability, feature_gap, version_pin, licence, host
- item 5: `PASS` — LANE_D gwo has 31 steps, verdicts 24 MISSING / 6 NOT_RUN / 1 EXISTS (the single EXISTS is GWO-SBL S3), groups GWO-FABRIC 7, GWO-HGK 6, GWO-SBL 5, G-A 6, G-B 7 — identical to DETECTION.families.GWO_GATE_STEPS and to REPORT_R2 §4. Nothing is 
- item 6: `PASS` — Reran round2/codex/EXECUTE/recount_docs.py myself: 'EXECUTE_DONE {"pi_atoms":27,"pd_slots":31,"tq_parent_cases":108,"tq_child_cases":124,...,"nodes":38,"r15_ids":949,"r15_min":"R15-003","r15_max":"R15-951"...}' — all six counts equal RECOUN
- item 7: `PARTIAL` — Board snapshot is consistent and honestly labelled, but most card states are read-back-only. KANBAN_RECEIPTS_POSTHOC.json carries 23 cards with label 'POSTHOC — read from the board DB through the CLI, not captured at invocation time'; compa

> AO ceiling: PARTIAL, and NOT INDEPENDENT_PASS: I am a fresh-context subagent of the same session/principal family, not a different principal or credential, so no rung above DOC_STATIC_PASS is bought here. What this verdict establishes: the round-2 subject is frozen and clean at the bytes I read (63/63 by my own reader), both round-2 blocking findings are repaired in substance (post-freeze drift gone; self-check totals no longer drift — actual 45/45), and six of seven checks hold on re-measurement. What it does not establish: semantic correctness of the documents, native/host/release state, or owner acceptance. Two limits are structural rather than incidental — the freeze excludes the evidence MD and the reviewer verdicts by construction, so the delivery layer can go stale without any drift detector noticing (which is exactly what OC-1 is), and the board states for 17 of 23 cards have no live receipt (item 7). Reviewer side effect disclosed: the two mandated reruns rewrote round2/SELFCHECK_R2.json and round2/codex/EXECUTE/RECOUNT.json byte-identically (digests equal to the manifest; mtime only).

**收據完整性缺口（不掩蓋）**：KANBAN 只有 4 次 `complete` 有即時 JSONL 收據；其餘 16 次`done` 轉移是直接 CLI 呼叫，未經 recorder，只有 `KANBAN_RECEIPTS_POSTHOC.json`（23 卡 `show` 快照，明確標註 POSTHOC）與 board 快照可佐證；`block t_87b4e5f5` 曾以錯誤 flag 失敗兩次（rc=2/rc=1），最終狀態 blocked 正確但 rc 歷史不乾淨。此為**收據完整性缺陷**，不是狀態錯誤，亦不得據此改判 native 可執行。

**本輪處置**：round-1 的 3 項 blocking 已修並由 round-2 重測為 FIXED；round-2 的 2 項 blocking（凍結後主體位移、自檢總數在文件中寫死）已改為「先凍結後驗、文件只引用 `SELFCHECK_R2.json`」，並以 `verify_frozen.py` 對 manifest 比對；round-3 的唯一 blocking（本 MD 的 hash register 綁到凍結前的 manifest digest）已改為 **freeze → make_evidence → verify_frozen** 的順序，並以本次 register 內實際 digest 為證。

## 8. 明確未做（禁區）

- 未寫入任何 canonical repo 的 tracked 檔（四倉 HEAD 與 tracked-dirty 與前次基線相同）。
- 未把三個候選修補落地；未覆寫 `source_path`（`land_source_path.py` 僅 dry-run）。
- 未簽發 runner registry、native-admission bootstrap、source freeze、release。
- 未以 AO 子代理冒充 INDEPENDENT_PASS。

## 9. 產物 hash register

| 檔案 | bytes | sha256 |
|---|---|---|
| `round2/AO_VERDICT_R2B.json` | 13566 | `1326eb016b9fc5df7e1707e5b9f0523258f78e6606e798e855ceecdd776a4d47` |
| `round2/AO_VERDICT_R2C.json` | 18155 | `90dc60079467d88bfc20059a3e275f1048c0a538f1117e27808868324f34bf48` |
| `round2/build_detection.py` | 16615 | `5cab3baac47c5d96c5507963d6c334552d173c0a6401b06ac081eb5cee169886` |
| `round2/build_index.py` | 6435 | `1e2fd6891f2db8f3d7f4dd5b6f793fd1be5d5120050e6a0494c9c16006ac37ed` |
| `round2/build_state_r2.py` | 12794 | `31cb78457b9c0c7705037c0331af57d4ca03db6bafb832465620d566ef51e7ec` |
| `round2/codex/EXECUTE/RECOUNT.json` | 11421 | `0a097efa7324b8677702a055487a20fa18fa6bbdb5c99d8f87677eb5ac0a75c0` |
| `round2/codex/EXECUTE/recount_docs.py` | 10793 | `51672e82bed913333ace024ce2f9fc7172921a2931f271c8d96331dcb49457d1` |
| `round2/codex/VERIFY/VERIFY_VERDICT.json` | 1177 | `69d43ecb57b24803d99f72930a1972617fc5c0ccfddca3a26c60b66b0ceca138` |
| `round2/DETECTION.json` | 28200 | `1869bf299744e981aca4596ad20d90e688f087aed893c61d4af1969afce06560` |
| `round2/DETECTION.md` | 3492 | `629c1cf9c84e4138b1b09000efce68cfaaccb006f1ab05c0e5164bc6208098ed` |
| `round2/fix_kanban.py` | 4107 | `3b3321179b27d5e3354c8b0977639bfb93a921c83a8647fad8f7a7259c862822` |
| `round2/freeze_subject.py` | 2941 | `e73673fac1aaa21527da41284541e1afb7c3feba01896c550e76feb4e397f7a2` |
| `round2/index/DOC_INDEX.json` | 705955 | `6f4e7c697155ce1673333c595483eab7a612397e3e2c4812c67807e502112761` |
| `round2/index/GLOBAL_INDEX.json` | 50066 | `7f125ef03fe6f263bc8dd7e85cfdc9f15f88289b349498269b493dceb7d5257e` |
| `round2/kanban_posthoc.py` | 2045 | `e557b49e9100190a05d05922a009ba71b946e3c53aa7a0efecf028ce5d206b22` |
| `round2/kanban_round2.py` | 8201 | `c45efe0aaff6eb2e26b99e2d26151c6941dfde1db32e5b2112e22f46f5a88beb` |
| `round2/lane/BRIEF_EXECUTE_recount.md` | 3105 | `d1fa3cc3b8df659b5fde595891479e486b8a939c056cf43ca95a8857c201ab77` |
| `round2/lane/BRIEF_VERIFY_ceiling.md` | 2221 | `632b98b810dd0570ef10f355ddb253b1f1f1c8ce9e122602ecdfb16014b33934` |
| `round2/lane/codex/EXECUTE_BRIEF_EXECUTE_recount.json` | 2699 | `b909e4c32c5690b73d227ccaf763c7a21e035161a8209f6f44d8c0d19905f67c` |
| `round2/lane/codex/VERIFY_BRIEF_VERIFY_ceiling.json` | 3512 | `50af8b945dfe2e923e97cb01bbcbdc26a23aac688607362c1f30fcd2cde64b01` |
| `round2/lane/KANBAN_RECEIPTS.jsonl` | 92649 | `727e44dfbbc2442d1521aba9f64d42dcb6a10a4d7308f25a8e971e56912a1ad7` |
| `round2/lane/KANBAN_RECEIPTS_POSTHOC.json` | 47809 | `3bc07103922e250d0166e06128a080e3a89ceb3c077c5d2af4bdf2b0d56c3e72` |
| `round2/lane/METHOD_RECEIPTS.json` | 13962 | `ef8c219550ae57e402a2d60cf78d2ce3ec399bafb92373cb5a351a02a95daf5d` |
| `round2/lane/run_codex_lane.py` | 4619 | `a1a83cdcbf9bed5137e7fa4942a817e61d2fc1fb0f0f8af616bf98190f6daaea` |
| `round2/lane/SWARM_RECHECK.json` | 4333 | `82872dd350d2d345862294239a1fb8cbaec8c03d6539b6604766a635333478b2` |
| `round2/make_evidence.py` | 13448 | `c4b5a87e748dfaad76cbaf3632a4b75c309d4c72139c0e711d7878cf803f473a` |
| `round2/probe_methods.py` | 8547 | `580ba4738a2b75eb54acc1202805277a6952899db26e0f00d383127af6f5961c` |
| `round2/probe_registry.py` | 3537 | `e33db333738ddea9f0c3ed9081d4322d082a537e0e6d125344756f7a2e4c6afe` |
| `round2/repair/build_candidates.py` | 12106 | `05743bac24fb1368a518223dd7bb726923981c1f02e020025566678032352b5e` |
| `round2/repair/candidates/01_TechnologyAdmission.schema.diff` | 7515 | `e620329fca62f126575b25790d32ce36c4891ef07a9225d817cf3e6ca033b416` |
| `round2/repair/candidates/01_TechnologyAdmission.schema.json` | 5247 | `b909c345e31b603b8226140c556696ac9a9c7a783e44e1cdb4538383a9e6f053` |
| `round2/repair/candidates/02_registry.diff` | 843 | `dc745d7c3e66a9abcb744f06272731cd8d5cf4dc42b93c9ae2f2932b52c77a26` |
| `round2/repair/candidates/02_registry.py` | 7510 | `870c61a207e5284241b5c9661c1370c22f52c08654779f03955a83e42c898ce5` |
| `round2/repair/candidates/03_rp002_f0_policy.py` | 4711 | `50b6d2382ad7cdc3fd190e448d42bec2f143248bc4f9de5f9c37fd225d020378` |
| `round2/repair/candidates/03_rp002_root.diff` | 439 | `aa46d8a8a11c4d6963b17a7eea623f881eca6ed13210a6b04474f927ac45fbd8` |
| `round2/repair/land_source_path.py` | 4749 | `422124e76399950872f5f601fe6b305b14ef176a961f505329b37507940ecfac` |
| `round2/repair/LANDING_PLAN.json` | 6816 | `38bec07697ac746046b1bc2f80312e2d6866fb29065e9ca7f873eb2492821584` |
| `round2/repair/REPAIR_RESULTS.json` | 2789 | `98fccc972640177e84f10d9acd7048842663137e30417877e346983ed430f119` |
| `round2/repair/sandbox/pipd_ls_sp/__init__.py` | 363 | `cbc9ba5ad7c2950b296bd836a9c0c7ae2052dd3da0437eb16255f6f142963272` |
| `round2/repair/sandbox/pipd_ls_sp/cli.py` | 18147 | `eb7c54293862129d27423617c7f7dcc6410bff1b38d54589e58180f6db4af86c` |
| `round2/repair/sandbox/pipd_ls_sp/errors.py` | 3183 | `a8d1058a32523e25b66ce52e27ca94cd0851a1e68fdf31ecc7449da892911215` |
| `round2/repair/sandbox/pipd_ls_sp/export_bundle.py` | 10365 | `00644f120959626f9b9dabbf7a579c5acdafca017654dad394e46b65ead5202e` |
| `round2/repair/sandbox/pipd_ls_sp/oracle_compat.py` | 3344 | `a79117224b206377d6bc8ae958eea42dc45d02e9ffde89a9d9db66a3e26efcfc` |
| `round2/repair/sandbox/pipd_ls_sp/pipeline.py` | 23467 | `b8ce91b9b337790271902940286e23f5d87c122efc205b9aade33a5f9cad8081` |
| `round2/repair/sandbox/pipd_ls_sp/profiles.py` | 2341 | `2631eac7f6cb2b48dba0ed6628c4d7d7e94b7843ac29353950c2d51172789070` |
| `round2/repair/sandbox/pipd_ls_sp/projection.py` | 85317 | `6a5d026386507adb0be01a594867223236382ab3cd2b2dd378d8a78c6d412d3c` |
| `round2/repair/sandbox/pipd_ls_sp/registry.py` | 7510 | `870c61a207e5284241b5c9661c1370c22f52c08654779f03955a83e42c898ce5` |
| `round2/repair/sandbox/pipd_ls_sp/repo_context.py` | 11444 | `21940e5984867c7d9829f719bec47e09b8ee083061bae54f79962d7c603b3e03` |
| `round2/repair/sandbox/pipd_ls_sp/requirements.py` | 13407 | `1ac3a64c655d93e02e2511456d08972801a89b788eec635289b51e0e7de88121` |
| `round2/repair/sandbox/pipd_ls_sp/util.py` | 1260 | `e0f19219a669dd77c1e1fcf70dfdd072e66b142598b7d6dea0ab21c06c7e19c7` |
| `round2/repair/sandbox/pipd_ls_sp/validate.py` | 18422 | `5a298eb50685a9e3185c21dd15560d1a77601ee871b58cbc3dba0df7c746e701` |
| `round2/repair/sandbox/pipd_ls_sp/workspace.py` | 14196 | `28bcafe4d4f02fbebd0ab982c58fe15861e9164f724ffc0bedbf8485385e64de` |
| `round2/REPORT_R2.md` | 7700 | `8f5aa6348b8977fffda4af44fddab0eca509e142d51b294214340d9547e9c2b4` |
| `round2/RESUME_R2.md` | 5096 | `4b26a56647e282d6ba016d45da141840fa9dd9cfd0dc62afa06d77bab4eb0eec` |
| `round2/SELFCHECK_R2.json` | 5749 | `86a16ff62a0dc897bbd479f6e468adde1e4c92e0bbf93fb6474d9263d9a43a36` |
| `round2/STATE_R2.json` | 20918 | `a643238d30e4e4207ce9f8cb51874f40fb542c8e2089a9c7b339507a6d40bc87` |
| `round2/SUBJECT_MANIFEST.json` | 13569 | `ad10e5168f249fe8b8145faaee6d607b0844773299aed71248b1455d62a8e2fe` |
| `round2/swarm/LANE_A_DOC07_DEV04.json` | 77087 | `b7ac2b071be0e28d8b72ff15e3695019e3e922bfba471fd261de1e695bc30665` |
| `round2/swarm/LANE_B_DOC00_DOC03.json` | 66963 | `0796c8d6bdd6e48f21394d1e4090fa391d44302e2e08c2df68a51e708659fa2b` |
| `round2/swarm/LANE_C_DOC05_DOC06.json` | 25796 | `6deaf14308a55890c08d4785a7581698e9df2d5ede11a73369da4b5b11ea4fab` |
| `round2/swarm/LANE_D_DOC08_01_02.json` | 38020 | `edb9575d3b301cf7771af28d67c15f56b1bcce7c5bc65ae2cac0f550c253163c` |
| `round2/verify_frozen.py` | 2296 | `30c6ca56572ac07798d2a8a4eb04991e73b1252b8dea9e02a8ccc7e714f63e26` |
| `round2/verify_round2.py` | 12206 | `3be136ce81d17a6734da3de5c4d46c9a11e0cc877eafd0f306dd655691e0fbfe` |
| `round2/verify_swarm.py` | 6189 | `79dbd3c32dc50f34f5f09370f96f9b5bc0831e9f9086491c8d39af9e914f808b` |

## 10. STOP（下一個 SESSION 不得做）

- 不得把 blocked 的 native 卡拉成 done；不得用 AO 或 VERIFY 車道冒充 `INDEPENDENT_PASS`。
- 不得在未取得 Owner 簽章前覆寫 `source_path` 或落地 R2-P01/P02/P03。
- 重跑順序：`probe_methods.py` → `probe_registry.py` → `build_index.py` → `build_detection.py` → `build_state_r2.py` → `verify_round2.py` → `make_evidence.py`。
