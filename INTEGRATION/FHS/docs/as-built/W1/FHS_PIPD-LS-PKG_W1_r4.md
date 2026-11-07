---
artifact_id: FHS-PIPD-LS-PKG-W1-AUTHOR-FINAL-20261105-R2-AFFECTED-REPAIR
artifact_type: L3_W1_AUTHOR_FINAL_AFFECTED_REPAIR
version: 2026-11-05_r2_AUTHOR_FINAL_AFFECTED_REPAIR
language: zh-TW
encoding: UTF-8/LF
normative_scope: W1_AUTHOR_FINAL_DESIGN_ONLY
source_w1_r5_body_sha256: 6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb
source_w1_r5_appendix_sha256: ed1995d882d00933b757e93a146320639b0c6a1c9aaa5bde34c381a806b4c1f6
upper_l0_r4_sha256: 7befcac3570caf9e1ade2ed231bd04de6a561f9b3038fef89597233f3566b75d
upper_l1_r4_sha256: cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b
upper_l2_r4_sha256: bb970a439fe31faf23e86c054f6282e538d369b84841d778e3b35b69ce5d4d37
w0_closeout_uploaded_zip_sha256: bced4b074bc788e858d5ecdcfb670d784a698c2cfc299a1f0040dc69c59e91e4
w0_corrected_body_sha256: 56d0df3db6765ee780689ea687824ca891f5a366797e04cfe6ae7c0928173f2a
w0_source_manifest_sha256: 06628b6b4c6ba1b0d4d9b31b795141aaf51ade4c7df8304d1af093a229227f60
owner_original_ratification: NOT_OBSERVED
native_host_e2e: NOT_RUN
independent_checker: NOT_RUN
repository_mutation: NONE
release: NOT_GRANTED
repair_controller: FHS-W1-R2-AUTHOR-CANDIDATE-20261105
supersedes_author_body_sha256: 21eeefd701098dccc64c4e01368cc1421a208724501d34c27b8a206e0a617ee7
r1_author_final_body_sha256: 5570a8a9bf9d9a447642a48f7268868baf9db403ec1f98bf8fb8b4eda2289000
r1_author_final_zip_sha256: f2aff1363d14c0ad7db00fb4a53ddc8107b0879cf4d6cff50714079bee0742a9
w0_final_1203_uploaded_zip_sha256: 4d020b2a49ff6e81efa1bc3cdae3f8635b407478d5ad603122fe24db24896b26
w0_final_1203_open_holds: 71
w1_intake_uploaded_zip_sha256: d6e79c7335e2aaf57387f45971ca7df2cae21a8b7c78eab866bcf644dc4256cc
supersession_scope: W1_AUTHOR_DESIGN_ONLY_INTEGRATE_COVER_REPLACE_R1_NO_NATIVE_AUTHORITY_TRANSFER
claim_ceiling: AUTHOR_FINAL_STATIC_ACCEPTED_WITH_AFFECTED_HOLDS

repaired_at: 2026-11-05
repair_scope: AFFECTED_ONLY__F01_F14_N01_N08
revision_round: FHS-W0W2-BASELINE-RECON-20261106
revision_of_file: FHS_PIPD-LS-PKG_W1_r2.md
supersedes_sha256: e40df2999fbffdb96a32a2e35cddce228abdd82080d5a5bedd415dfc938669ce
revision_version: r3
changed_scope: ["WP-FHS-02", "WP-FHS-03", "WP-FHS-05", "WP-FHS-11", "WP-FHS-17", "WP-FHS-20", "H-W1-01..08"]
rollback_ref: ORIGINAL_BYTES_SHA_e40df2999fbf
revision_claim_ceiling: AUTHOR_SIDE_RECONCILED_WITH_SCOPED_HOLDS
revision_writer: original_W1_design_curator
original_writer_transferred: false
source_snapshot_round: FHS-W0W2-BASELINE-RECON-20261106
---

## FINAL-00｜本次實際交付、唯一當期路由與證據界線

**CurrentReaderRoute**：本節 FINAL-00 → 各 CH 的 AUTHOR-FINAL 補差契約 → 未受影 r2/r5 原條文；當期機讀資料只讀根目錄 Registry、finding_disposition.json、static_validation_report.json。R2-00..R2-11 原作者「修復」敘述是保留血緣，必須以本次實測及具名 HOLD 覆核；歷史原件均在 lineage/、historical/，不提供第二個有效 Writer。

本版已使用 sbl-tpm-sp 的 PM/SE/TPgM/PIPD/交接契約，並實際呼叫其 core.plan_spec 三角色、GHP-01 與 pre_v2.handoff。其證據在 plugin/。本版不輸出原 Canonical PI/PD/ECP/TQAEP，不把 @2 sidecar 或本機作者測試提升成 Protected Checker。三個 SPEC 的正文與不同角色 JSON 在 specs/；原 22 WP 完整條款及 36 directed edges 在 program_dag_22_36.json。

**當期裁決：AUTHOR_FINAL_CANDIDATE_WITH_AFFECTED_HOLDS**。T0 可重算 bytes 與 T1 作者設計檢查的結果見靜態報告；原三庫/Host/Owner 的欠件見 affected_hold_registry.json。來源切片 31/166/57/24/24 只證指定作者範圍，不取代 949/149/50 Parent/39/96/192/282、27 PI→31 PD、485 技術身份分母。W18 是 W3 UAT。

**W0 四層狀態（r2 修補，F-10／N-01）**：`ARCHIVED_R4C`=68 OPEN、WP19 5 PASS/2 FAIL、`W0_CLOSEOUT_PENDING`、E26 `UNSATISFIED`（血緣層）；`FORMAL_CANDIDATE`=70 OPEN／6:1（候選層）；**`W0_FINAL_1203`=71 OPEN（70 carried + 1 new，all_open=true）、WP19 7 PASS／0 FAIL、`W0_AUTHOR_LOCAL_CLOSEOUT_ACCEPTED_WITH_SCOPED_HOLDS`、`w0_full_closeout=false`、`WP19_DONE=false`、E26 `UNSATISFIED_WP19_ORIGINAL_RAW_MISSING`、原 CI ACK `NOT_OBSERVED`（當期最新作者封存）**；`ORIGINAL_DOMAIN_EFFECTIVE` 只有同 Scope 原 Reader ACK／NACK／具名 deferral 才能改變（HOLD）。四層互不升級；E26 只阻受影 W4 Release，不阻 W1 READ／SPEC／隔離 DRAFT。完整欄位見 `W0_STATUS_THREE_WAY.json` 與 FINAL-01 §1。

**跨波與原 Reader**：所有 37 非 W1 主章的原 Writer/波次保持不變。W1 八 WP 僅 02/03/04/05/07/11/17/20 的作者設計；其餘 WP 指針只作來源與交接。任何歷史表列的 W1 代表 design selection，而非 OriginalPrimaryWP/Wave 的移轉；以 obligation_registry.jsonl 的 original_primary_wp_and_wave 核對。

**受界執行**：本輪僅 SOURCE_READ/LOCAL_DRAFT_WRITE；DEV/HOST/USER/RELEASE 均需原 Receiver/Issuer/Consent/Checker/Publisher。SID、PolicyEpoch、Host、NeedKey、Oracle/Parent 未觀察一律 UNBOUND/HOLD；不同 Profile 不能證明 OS 隔離。UNKNOWN 必先原 World reconcile。

**來源解析**：外層控制 ZIP 未觀察；使用你指定的完整目錄，經 Windows 長路徑讀取後，32 members/30 SHA 全過。原封存 SHA 未改。此處不把重建目錄稱為原 ZIP。


## FINAL-01｜r2 受影修補契約（AUTHOR_FINAL_AFFECTED_REPAIR）

本節是**唯一的 r2 差額契約**：它不改寫 FINAL-00 的讀法，也不構成第二條現行讀本路由。FINAL-00 仍是 CurrentReaderRoute 的唯一入口；本節只把「W0 1203 封存後才出現的差額」原位寫回，並把每一項的裁決、原 Reader、FirstFail、Stop/Resume 固定在正文，而不是只留在附錄。

**本節的法位**：`LOCAL_DRAFT_WRITE`／作者端定案修補契約。本節不產生 Canonical PI/PD/ECP/TQAEP、不產生 HGK Permit、不代替 Protected Checker、不構成 Release。

### 1｜W0 四層狀態（F-10、N-01）

| 層 | 來源 | Open HOLD | WP19 作者端 | 結案辭 | E26／原 CI ACK | 當期？ |
|---|---|---:|---|---|---|---|
| `ARCHIVED_R4C` | r1 保留的歷史 W0 R4C | 68（64 carried + 4 new） | 5 PASS／2 FAIL | `W0_CLOSEOUT_PENDING` | `UNSATISFIED`／`NOT_OBSERVED` | 否，血緣層 |
| `FORMAL_CANDIDATE` | r1 遠端作者候選 | 70 | 6 PASS／1 FAIL | CANDIDATE | `UNSATISFIED`／`NOT_OBSERVED` | 否，候選層 |
| `W0_FINAL_1203` | `closure/W0_FINAL_CLOSEOUT_DECISION.json`＋`closure/HOLD_AND_RESUME.json` | **71（70 carried + 1 new，all_open=true）** | **7 PASS／0 FAIL**（4 負例按預期翻轉；strict control 1 FAIL 作辨識） | `W0_AUTHOR_LOCAL_CLOSEOUT_ACCEPTED_WITH_SCOPED_HOLDS`（`w0_full_closeout=false`、`w0_wave_accepted=false`） | `UNSATISFIED_WP19_ORIGINAL_RAW_MISSING`／`NOT_OBSERVED` | **是，最新作者封存** |
| `ORIGINAL_DOMAIN_EFFECTIVE` | 原 SBL CI/Program Reader、原 W1 Receiver、原 Fabric Policy、原 HGK Issuer、原 Host、Protected Checker、Publisher | `NOT_OBSERVED` | `NOT_OBSERVED` | 未生效 | 只可由原權威同 Scope ACK／NACK／具名 deferral 改變 | 否，HOLD |

**計數不可互相升級**：`7 PASS／0 FAIL` 只升級「作者端 scoped 供應鏈例證」，`WP19_DONE` 仍為 `false`，`E26` 仍 `UNSATISFIED`；反之 71 OPEN 也不得被當成 W1 `SOURCE_READ`／SPEC／隔離 `LOCAL_DRAFT_WRITE` 的停工理由。可重算版本見 `W0_STATUS_THREE_WAY.json` 與 `W0_FINAL_1203_HOLD_LEDGER_71.json`。

### 2｜Finding 裁決一覽（F-01～F-14、N-01～N-08）

| ID | 裁決 | r2 原位動作 | 證據層級 |
|---|---|---|---|
| F-01 | KEEP | 31 源／166 原行 byte+offset+SHA 於 r2 樹重播，無改寫 | `PASS_STATIC` |
| F-02 | KEEP | 13 個 L1 章 span 以原檔重算 section SHA，歷史 locator 仍標 `HISTORICAL_LOCATOR_NOT_EFFECTIVE` | `PASS_STATIC` |
| F-03 | REBUILD_NEW_VERSION | 新版本實體 ZIP＋逐成員 hash＋CRC；讀回檔在 ZIP 外 | `PASS_STATIC` |
| F-04 | KEEP＋TARGETED_CHECK | 32 作者例（8 WP×POS/NEG/EDGE/SEC）NEG 與 SEC 的主體／攻擊面／FirstFail 逐欄不同 | `PASS_STATIC`（Native NOT_RUN） |
| F-05 | SCOPED_HOLD | 57 子義／24 DesignID 的 OriginalID／Parent／NEG／Oracle 不代填，逐項具名 HOLD | `HOLD` |
| F-06 | KEEP | 24 卡維持 `NO_WRITESET_TRANSFER`，W1 不接管 WP00/01/10/13/16 | `PASS_STATIC` |
| F-07 | KEEP＋HOTSWAP_REQUEST | 唯一 effective pin 不動；本機 OpenSpec 1.8.0 只列 HotSwap 候選，不默升 | `HOLD`（Host fit 欠件） |
| F-08 | NATIVE_REUSE＋SCOPED_HOLD | 24 Asset 狀態階梯逐階分立，INSTALLED／LOADED／VERIFIED 全 `NOT_OBSERVED` | `HOLD` |
| F-09 | KEEP＋ABI_PROBE | 四 Envelope 重綁 r2 candidate SHA，`original_reader_ack=EXPECTED_NOT_OBSERVED` | `HOLD` |
| F-10 | MUST_UPDATE（已修） | 本節 §1 四層狀態＋§6 適用性 Gate | `PASS_STATIC` |
| F-11 | KEEP | 表格 backtick 配對、anchor 目標、INT-24 整句對照於 r2 重跑 | `PASS_STATIC` |
| F-12 | KEEP＋MEASURE_PLAN | 七痛點 design FUO 與 native FUO 分欄，native 全 `EXPECTED_NOT_OBSERVED` | `HOLD` |
| F-13 | MINIMAL_HOST_PROBE | 只觀測到單一 OS principal；SoD 仍 `UNPROVEN`，受護效果不做 | `HOLD` |
| F-14 | KEEP＋REMOVE_DUPLICATE | 全檔僅一個 CurrentReaderRoute 標記；r2 與 r5 敘述只作血緣 | `PASS_STATIC` |
| N-01 | 已修 | W0 四層狀態寫回 FINAL-00 相鄰段、R2-06 與 §6，不再以 68/70 代表當期 | `PASS_STATIC` |
| N-02 | 已修（寫入仍 HOLD） | 本地四庫真根／HEAD／branch／dirty 逐庫探針；遠端 HEAD 明確不得當 local RepoContext | `PASS_STATIC_PROBE_ONLY` |
| N-03 | 部分（HOLD） | 只到 CLI 層：v0.22.5、原生 Kanban、原生 Delegation；ActualServed／Journal／Policy Loaded 未觀測 | `HOLD` |
| N-04 | 已修 | §6 適用性 Gate 表：每個 HOLD 只阻它指名的 operation | `PASS_STATIC` |
| N-05 | 已修（政策層） | §8 Stop/Resume：UNKNOWN 先 WorldReader reconcile，禁止盲重試與重複 WorkID | `PASS_STATIC_POLICY_ONLY` |
| N-06 | 已修 | §7 Need→既有原生 Occupant→薄 Adapter，方法層只作 advisory | `PASS_STATIC` |
| N-07 | HOLD | 四 Envelope 具名接收條件；不得自造 ACK | `HOLD` |
| N-08 | 已修（本輪新增） | 三 SPEC 依角色補齊 input／output／ACC_POS／ACC_NEG／producer／consumer 與角色專屬區塊 | `PASS_STATIC` |

每一列的完整 19 欄（含 `source_locator_sha`、`negative_firstfail`、`stop`、`resume`、`owner`）在 `AFFECTED_FINDINGS.jsonl`；本表只是同一裁決的可讀投影。

### 3｜八個 W1 WP 的 r2 受影契約

八個 WP 只作**作者端設計**；原 Host／Issuer／Policy／Checker 的世界效果全部未執行。每列的 Input→Operation→Output→Original Consumer 與 POS／NEG／EDGE／SEC／FirstFail 已在對應主章原位可讀，本表只固定 r2 差額與邊界。

| WP | 受影 CH | Input → Operation → Output → Original Consumer | POS／NEG FirstFail／EDGE／SEC FirstFail |
|---|---|---|---|
| `WP-FHS-02` | CH-17／CH-16 | 同 `SourceSHA/PolicyEpoch` 的 Policy 提案 → staged→active→loaded 三段分離 → Loaded 收據與 Consumer ACK 請求 → 原 Fabric Policy＋HGK Consumer | `POLICY_LOADED_ACK_MISSING`／`POLICY_SIGNER_OR_EPOCH_DENY`；Epoch 更新只重驗受影 consumer |
| `WP-FHS-03` | CH-18／CH-39 | WorkID／Lease／Nonce／CAS 請求 → 原 Issuer 准入 → WorldRaw 與 ACL 讀回 → 原 HGK Issuer／WorldReader | `ISSUER_WORK_BINDING_NACK`／`ISSUER_PRINCIPAL_ACL_DENY`；TTL 邊界與 UNKNOWN reconcile |
| `WP-FHS-04` | CH-19／CH-20 | 普通 Goal → PLAN／EXECUTE／VERIFY_SECURITY 三 Lane → fresh PID／ProfileSHA／ActualServed／Journal → 原 Host Runtime | `ACTUAL_SERVED_NOT_OBSERVED`／`CROSS_PROFILE_SECRET_DENY`；PID 變動只重綁受影 |
| `WP-FHS-05` | CH-12／CH-13／CH-14／CH-40 | 意圖 → 13 CLI／19 Families／8 Skills 的來源綁定 → PI（source-bound）→ 真 RepoContext 晚綁 PD → 原 SBL PIPD Compiler | `PD_REPOCONTEXT_UNBOUND`／`PIPD_SHADOW_WRITER_DENY`；dirty 變動只重綁 PD 受影位置 |
| `WP-FHS-07` | CH-34／CH-16 | Commander Guide A/B/C → Native PLAN 提案 → 同 WorkID／Revision CAS 回執 → 原 Native PLAN CAS Reader | `PLAN_CAS_ACK_MISSING`／`CROSS_WORK_PLAN_AUTH_DENY`；Revision 變動產新候選 |
| `WP-FHS-11` | CH-08／CH-22 | 四 Host 各自的 Loader 事實 → installed／loaded／invoked／nontrigger 四段 → Host 專屬收據 → 各原 Host Consumer | `HOST_EVIDENCE_FOREIGN_NACK`／`HOST_CHECKER_IMPERSONATION_DENY`；版本變動只重測該 Host |
| `WP-FHS-17` | CH-22／CH-18 | NeedKey → 既有原生 Occupant → 唯一 pin＋License＋Windows fit → 原 Technology／License／Host Reader | `CAPABILITY_NOT_QUALIFIED`／`INSTALLER_PRIVILEGE_DENY`；升版只走 HotSwap／LastGood／NoFit |
| `WP-FHS-20` | CH-19／CH-40 | Kind×Mode×Host 單格 → 該格 token ON/OFF → 原 Cell 收據 → 原 Product／Host Cell Reader | `CELL_TOKEN_OWNER_ACK_MISSING`／`CELL_RECEIPT_CROSS_HOST_DENY`；只測變動的那一格 |

### 4｜三 SPEC 分立（N-08）

| 角色 | 檔案 | 不可與誰合併 | 本輪狀態 |
|---|---|---|---|
| Product（PM／TPM） | `specs/Product_SPEC.json`（r2 v2）｜pin 原檔 `specs/pinned/SPEC_Product.json` | 不得與 PI 或 Program DAG 合併 | `PASS_STATIC`：七痛點各有 `ACC_POS/ACC_NEG/FirstFail/NextWave`，native 欄 `EXPECTED_NOT_OBSERVED` |
| Architecture（SE） | `specs/Architecture_SPEC.json`（r2 v2）｜pin 原檔 `specs/pinned/SPEC_Architecture.json` | 不得與 Product ACC 或 Program 排程合併 | `PASS_STATIC`：S1–S5 各 Producer／Reader／Consumer／ABI／NEG，`ownership_seams` 與 `seam_registry_5.json` 同值 |
| Program（TPgM） | `specs/Program_SPEC.json`（r2 v2）｜pin 原檔 `specs/pinned/SPEC_Program.json` | 不得把 W1 八 WP 當成 W2 施工 WriteSet | `PASS_STATIC`：原 22 WP／36 DAG 邊不改向，W1 八 WP 各自 Stop/Resume/Rollback |

三份 pinned 原檔 byte-for-byte 保持，SHA 與 W0 1203 決議的 `four_artifacts` 相同；r2 v2 只加角色專屬欄位與 r2 差額欄，不改 pin。

### 5｜六級 Effect Gate 與本輪實際使用

| EffectClass | 本輪 | 依據 |
|---|---|---|
| `SOURCE_READ` | 使用 | 控制包／三 ZIP／遠端 blob／本地 git 唯讀探針 |
| `LOCAL_DRAFT_WRITE` | 使用 | 本正文、附錄、Registry、隔離 fixture、ZIP |
| `DEV_REPO_WRITE` | **未使用（HOLD）** | 本地四庫皆在候選分支且 dirty；無原 Repo Reader 的同 Scope 綁定 |
| `HOST_OPS` | **未使用（HOLD）** | 無 HGK Issuer／Policy Loaded／OS ACL／WorldRaw |
| `USER_EFFECT` | **未使用（HOLD）** | 無原 Consent／Original Consumer |
| `RELEASE_EFFECT` | **未使用（HOLD）** | 無 Publisher／GHP-02；E26 未滿足 |

`UNKNOWN` 世界效果一律先由原 WorldReader 依同 `Subject/CandidateSHA/Scope/Host/PolicyEpoch/WorkID` 對帳，才決定 idempotent reconcile／retry／rollback；本輪沒有任何世界效果被觸發，故 `world_effect_state=NOT_RUN`。

### 6｜適用性 Gate（N-04）

| 制約 | 只阻什麼 | 明確不阻什麼 |
|---|---|---|
| W0 71 OPEN | 受影 W0→W1 狀態引用與該 HOLD 指名的 operation | 來源讀取、三 SPEC、隔離草案、非受影章節 |
| E26（WP19→WP14） | W4 的 WP14／Publisher Release | W1 任何 READ／DRAFT，W2/W3 非 Release 工作 |
| WP16 `1 BOUND／11 pin-hold／installed=0` | 受影 Need 的 Host install／load | WP17 的來源與資格化研究、W1 文檔 |
| WP-FHS-17 未達 Host fit | 該 Asset 的 INSTALLED 以上狀態 | 其他 Asset、其他 WP、作者端設計 |
| 無原 Issuer／Policy | 受護寫入與 HOST_OPS | SOURCE_READ、SPEC、LOCAL_DRAFT_WRITE |

第一拒收：把任一受影 HOLD 擴張成全域停工 → `OVERGOVERNANCE_NONAFFECTED_BLOCK_NACK`（只修 Program scope，不凍結 W1）。

### 7｜Need→Occupant 最小重複用（N-06、F-08）

| Need 類 | 既有原生 Occupant | 本輪動作 | 缺口 |
|---|---|---|---|
| 多步任務與長期狀態 | Hermes 原 Profile／Kanban／Delegation／Journal | 直接使用，不建第二 Queue | Journal 真 Raw `NOT_OBSERVED` |
| 規格變更提案 | OpenSpec（方法層，本機 1.8.0） | 只作 proposal／delta／validate 方法 | 與 pin 1.16.0 的版本差列 HotSwap 候選 |
| 交付流程編排 | gstack（設計 pin `6bdafb2`，本機未安裝） | 只作方法參考，`NOT_INSTALLED` | Host fit／授權未證 |
| Canonical PI/PD/ECP/TQAEP | SBL `integrations/pipd`（13 CLI／19 Families／8 Skills） | 唯一 Writer；本輪未執行任何 compile | 原 installed／loaded `NOT_OBSERVED` |
| 控制平面 | 原 HGK Issuer／SharedSpine／World | 只讀設計，未發 Permit | 全數 HOLD |

**禁止**：以 OpenSpec／gstack／`$sbl-tpm-sp` 產生 Canonical 物件、建立第二 Compiler／Issuer／Checker／Queue → `SHADOW_CONTROL_PLANE_DENY`。

### 8｜Stop／Resume／UNKNOWN（N-05）

- **Stop**：來源 SHA 或原 Reader 衝突、Writer 不明、Scope／PolicyEpoch／Host drift、世界效果 `UNKNOWN`、重複 WorkID／Lease、OS Principal 越權、超出授權 WriteSet、破壞性負例未按預期拒收。停**該 Scope／effect**，保存 `first_fail／last_good／required_raw／owner`；非受影卡照常推進。
- **Resume**：只在原 Reader 回傳同 `Subject/Scope/SourceSHA/CandidateSHA/Host/Epoch` 的 `ACK` 或具名 deferral，且原 World／Repo／LastGood 可回讀之後，只重驗真正受影的卡。
- **Checkpoint 內容**：Subject、Scope、LastGood、Writer、Raw 摘要；**不含**任何密鑰、口令或 Token。
- **禁止**：`UNKNOWN` 盲重試 → `UNKNOWN_BLIND_RETRY_DENY`；任務停久了就推定世界「尚未執行」。

### 9｜本輪實際執行的工具與未被執行的事物

| 項目 | 實況 |
|---|---|
| 原生 Kanban | 已建立 `fhs-w1-r2-author-20261105` 看板與 16 張卡（8 階段＋8 WP），全部以 `blocked` 起始，避免無人值守自動派工 |
| 原生 Delegation | 已用原生子代理並行處理 71 HOLD 投影、24 Asset 差額、正文結構探針 |
| 原生 Swarm | `hermes kanban swarm` 能力存在；本輪未宣稱多 Host Swarm Ready（無多執行證據） |
| gstack | `NOT_INSTALLED`；只作方法層，未以 `/ship` 代替 Publisher |
| OpenSpec | 本機 CLI 1.8.0 可執行；pin 仍 1.16.0，差異列 HotSwap 候選 |
| 原 PIPD 13/19/8 | 由 SBL `main` blob 實讀重算，未執行 compile |
| Native E2E／SID ACL／Issuer／Checker／Publisher | `NOT_RUN`（無原域 Raw） |

### 10｜本節主張上限

`AUTHOR_FINAL_STATIC_ACCEPTED_WITH_AFFECTED_HOLDS`（作者端）。不得由此節宣稱 `W0_FULL_CLOSEOUT`、`PIPD_CANONICAL_EFFECTIVE`、`NATIVE_E2E_PASS`、`INDEPENDENT_CHECKER_PASS`、`RELEASED`。


# 《FHS_PIPD-LS-PKG_W1_定案》｜2026-11-05 r1 AUTHOR_FINAL｜受影 HOLD 的作者端定案候選

> **當期可用主體**：本檔將 W1 r5 L3 `藍圖&skeleton` 的 **全部既有實質條文**高保留納入，於 13 個主責 CH 原位補上可審可測的 I/O/Reader/Consumer/POS/NEG/FirstFail，並以前置的三 SPEC、選型、Closeout 接收與 24/24 有向追溯構成單一 **W1 作者端草案 Reader**。原 r5 中「未來草案須填」等文字是歷史要求清單，不能反向否定本稿已補的作者規格；未見 Original Reader Raw 的內容仍明列 HOLD，非憑描述宣正式達標。
>
> **法位與唯一 Writer**：W1 DraftMaker 寫本地 `MD/ZIP`；Original SBL/PIPD、Fabric、HGK、Hermes Host、Protected Checker、Publisher 權威不變。`$sbl-tpm-sp` 已依 `tpm-sp/tpm-product-plan/tpm-system-plan/tpm-program-plan` 與 PIPD 八 Skill 的可見契約作 **作者端規劃**；這不代表原 CLI 已被呼叫、已插入 Windows Host 或取得原 Canonical Writer ACK。

## R2-00｜現行讀本、審計控制與正式工程法位（2026-11-05）

本版 `r2_HIGH_RETENTION_FULL_REPAIR_AUTHOR_DESIGN` 是對 r1 草案的**原位整合＋覆蓋＋取代**，以《W1_DRAFT_FULL_DESTRUCTIVE_AUDIT_REPORT》F-01～F-14 為受影修補控制。r1 正文 SHA `21eeefd701098dccc64c4e01368cc1421a208724501d34c27b8a206e0a617ee7` 保留為血緣基準；不得再把 r1 的錯誤 Locator／未封存 ZIP 狀態／重複 SEC 作有效讀本。**本版在 W1 作者端草案讀取路由立即生效**；非 Original Owner ratification、Canonical SourceFreeze、受保護許可、實機 Installed/Loaded/Invoked、Independent PASS 或 Release。原 Original Domain Effective Canonical/Reader/Writer/Issuer/Checker/Publisher 不轉權。

**HistoricalReaderRoute_R2（血緣資料，非另一個現行路由）**：`R2-00..R2-11 + CH-00..49 本版受影修訂` → `r5 高保留承接的未受影原條文（過渡狀態已歷史化）` → `r2 非規範證據附錄 + 同版 JSONL/ZIP Source Readback`。**Authority**：原各 Domain 當期 Subject/Scope Effective Reader > L0 r4 > L1 r4 > L2 r4 > W0 R4C 受影封存 > W1 r5 作者端母本 > 本 r2 作者端草案（設計引用）；作者端檔案不能蓋過原域生效內容。原來源欠據僅 `AFFECTED_SCOPE_HOLD`，允許合法 SOURCE_READ／隔離 LOCAL_DRAFT 續工。

**版本及來源**：L0 `7befcac3…`、L1 `cbdd75fd…`、L2 `bb970a43…`、W1 r5 `6b60f9f6…`、W1 r5 附錄 `ed1995d8…`、W0 R4C ZIP `bced4b07…`。原 949/149/50 Parent/39/96/192/282、24 INT/60 DR、五正交資產集合與 W1 的 24 Obligation/24 Asset/57 Subclaim 各自守恆；計數不是 Original Owner 語義核簽。

**SOP 六步在本版本的實證出口**：① 31 冊索引/上位 r4/r5 現行讀本；② 13 CH 當期 L1 真 span＋166 原始行；③ 對 OriginalID/Parent/NEG/Consumer、各有／分別／對應／若／除非／不得、Effect/Host/Policy/License/Pin 進行全文反查；④ 24 DesignID ↔ 57 子義 ↔ 166 來源候選 ↔ CH/WP/原 Consumer 的 *已證部分*，欠語義連結以 OWNER_HOLD 表達；⑤ 多 Host/三 SPEC/八 WP 等分解不同 POS/NEG/EDGE/SEC；⑥ 只以可見 input→operation→output→original receiver→case→firstfail/stop/resume 判定作者端實質存在。附錄 `R2-E` 列 14 項修補與破壞性對照。


## R2-01｜13 個保護主章對現行 L1-r4 的唯一真定位（F-02）

| W1 CH | CURRENT L1 r4 heading 行與完整 span | L1 全檔 SHA-256 | CH 區段 SHA-256 | History |
|---|---|---|---|---|
| `CH-08` | `L992–L1051`：# CH-08｜SBL SharedCore 六模組與三 SP 的完整產品鏈 | `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b` | `25b58dc0712e9ac55edc1becee91c101930b55d5b3533397cdb6c32e85224a32` | r1 舊區間 `HISTORICAL_LOCATOR_NOT_EFFECTIVE` |
| `CH-12` | `L1257–L1383`：# CH-12｜PIPD 13 CLI／19 Contract Families／8 Skills 與唯一 Writer | `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b` | `d63aab54cf64bb0e828fb9019502a1acf94bcd24da0d6116755a996eb29b30ca` | r1 舊區間 `HISTORICAL_LOCATOR_NOT_EFFECTIVE` |
| `CH-13` | `L1384–L1448`：# CH-13｜Authority SourceFreeze／Profile Tailoring／原 PI 的 18 領域 | `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b` | `8917c10f6fda394e8297fe794cedc5ba20f1179291cba8cf890265a5e3fe21f9` | r1 舊區間 `HISTORICAL_LOCATOR_NOT_EFFECTIVE` |
| `CH-14` | `L1449–L1520`：# CH-14｜PD-01..10、RepoContext Currentness、Scope 與晚綁 | `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b` | `0fb7ffa88651ba28d26bd0cbc08e0b3b95d2ab28753bca3c961704ef736f6558` | r1 舊區間 `HISTORICAL_LOCATOR_NOT_EFFECTIVE` |
| `CH-16` | `L1616–L1680`：# CH-16｜跨庫 Typed ABI、Producer→Consumer、Same Subject 交接 | `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b` | `1e717d56998665286e028c9ea3ad32aeabe01bfe9dda1a69e1f61ba36e058862` | r1 舊區間 `HISTORICAL_LOCATOR_NOT_EFFECTIVE` |
| `CH-17` | `L1681–L1741`：# CH-17｜Fabric Policy／FAR／治理鏡像與 FHS 工程入口 | `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b` | `d07505132f0a12e2113fce9ec0c84da655c91e32c717c04a7c21d8f394c2f10d` | r1 舊區間 `HISTORICAL_LOCATOR_NOT_EFFECTIVE` |
| `CH-18` | `L1742–L1822`：# CH-18｜HG-KSEOS 唯一 Native Issuer／SharedSpine／WorkID／許可 | `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b` | `8b6af3908e5fe75c0eec39314232dd0a80367be74408c0cb6ff62a988076d97e` | r1 舊區間 `HISTORICAL_LOCATOR_NOT_EFFECTIVE` |
| `CH-19` | `L1823–L1901`：# CH-19｜Hermes 三 Lane、模型路由、Profiles、ActualServed | `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b` | `2528bc824fca3ddf011611092731f2527c6d0ab139d591c576fd85cbc3611827` | r1 舊區間 `HISTORICAL_LOCATOR_NOT_EFFECTIVE` |
| `CH-20` | `L1902–L1978`：# CH-20｜Hermes Native Kanban／Delegation／Swarm／長任務編排 | `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b` | `26461f88645fafe6c79c6853d21ff05b60cc06ba86e119d936329a5597c4b25b` | r1 舊區間 `HISTORICAL_LOCATOR_NOT_EFFECTIVE` |
| `CH-22` | `L2048–L2318`：# CH-22｜Native20：現役唯一原生核心與維護權 | `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b` | `bb94a5153139251963a27df10dbd8b8c5c78f19cf6f3052b7fac9c6d1745ce4a` | r1 舊區間 `HISTORICAL_LOCATOR_NOT_EFFECTIVE` |
| `CH-34` | `L26233–L26296`：# CH-34｜Portable Commander Guide A／B／C 與原 Native PLAN | `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b` | `0738e008777ea1aefc449313e24d406dcaa6438f5ad9d195d5b5a175342edc25` | r1 舊區間 `HISTORICAL_LOCATOR_NOT_EFFECTIVE` |
| `CH-39` | `L27080–L27152`：# CH-39｜安全：SoD、Process ACL、秘鑰、原授權、Consent/Privacy | `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b` | `1d15d487b70197195d62451b7ceab4caf1c7fa7f78627bfd1ccf0952c2cf9ad1` | r1 舊區間 `HISTORICAL_LOCATOR_NOT_EFFECTIVE` |
| `CH-40` | `L27153–L27225`：# CH-40｜三 SPEC／PI／PD／ECP／TQAEP 對原 Reader 的交接矩陣 | `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b` | `d4108e3b235e8dff2a7409cf6a334a5b44b99da807b4f66a7d963232cd32320a` | r1 舊區間 `HISTORICAL_LOCATOR_NOT_EFFECTIVE` |

每行區間從現行 L1 r4 的 `# CH-XX` 至下一個 `# CH` 前一行，最後一章至 EOF；SHA 取原始 UTF-8 bytes（含原換行）。章首錯置、不同文件 SHA 冒原章 SHA 一律 `L1_CH_LOCATOR_MISMATCH`。正文下方 13 個 `Protected Original H1` 全部已原位更正，錯誤歷史 locator 僅標 `HISTORICAL_LOCATOR_NOT_EFFECTIVE`，沒有雙現行。


## R2-02｜來源 166/166、31 冊與 57 子義的完整雙向反查（F-01／05／06）

- **SOURCE_BYTE_TRACE：166/166 VERIFIED**：依 r5 `R5-C2` 原 JSONL，重讀 31 個上載物理來源中的每筆完整 UTF-8 行、SourceFileSHA、zero-based byte_offset、去 CRLF 後 `line_sha256` 與 `full_source_line`，全部一一吻合。全文不再只保留截斷摘錄；原 JSONL 原欄位保留在 **非規範性附錄 §R2-A 與同包 `source_line_registry.jsonl`**，31 原檔亦以 `sources/` 原 bytes 放入 ZIP，允許離線自證。
- **Original semantic ceiling**：112/166 `ORIGINAL_ID_READER_HOLD`；54/166 `ORIGINAL_ID_CANDIDATE_NOT_RATIFIED`；48/166 `ORIGINAL_PARENT_NEG_HOLD`，其餘 118/166 即使行上有 NEG token 仍未獲 Original Owner 語義核簽。166 SourceCard 只覆蓋 18/31 原冊，零 Card 的 13 冊不是 `NOT_APPLICABLE`；31/31 都在 `source_selection_31.jsonl` 有原 Reader re-read/HOLD。
- **57 作者子義**：每個 `subclaim_id` 逐一核對 L1-r4 original line SHA，保留 predicate、POS/NEG、FirstFail、effect、WP、Original Reader 和 `original_requirement_id=ORIGINAL_ID_READER_HOLD`。以 CH 對 SourceCard 做的是**待核主題候選 Join**，不能假稱已把 166 條全部精確對到 57 條的原 RequirementID／Oracle／Runner。實體跨 Join `OriginalID/Parent/NEG/Oracle` 欠據一律 `ORIGINAL_DOMAIN_SEMANTIC_READER_HOLD`；不宣稱 U1–U4 全量語義已 PASS。
- **24 DesignID 的權限消歧**：L2 `W1_DESIGN_SELECTOR` 與 `ORIGINAL_PRIMARY_WP_AND_WAVE` 分欄；原 WP00/01/10/13/16 等屬其他波，不把 W1 的規格閱讀當成其 Native WriteSet 的轉移。24 卡的完整 L1 原行、line SHA、原 POS/NEG、Reader 與 W1 職責在 `obligation_registry.jsonl`。FullProduct 原分母絕不改寫為 W1 24 張。

**雙向索引鍵**：SourceCard `source_key+file_sha256+line+byte_offset+line_sha256` → `author_ch` → L2 `DesignID` 與 57 `subclaim_id` *candidate* → `Original Consumer/Case/FirstFail`；逆查從 `DesignID/WP/CH/Case` 回 `L1-r4 line_sha256`、31 源 `source_key`、相應 `SCL` CandidateIDs 與 Original Reader HOLD。只有原 Owner 將 `OriginalID/Parent/NEG/Oracle+Scope` 核簽，該候選連結才能 promotion；否則 `SOURCE_CONTEXT_FRAGMENT_OWNER_HOLD`。


## R2-03｜八個 WP 各自不同的安全 Principal／NEG／SEC／WorldRaw（F-04）

| WP | 原 NEG（業務錯誤） | SEC 独立信任邊界攻擊 | SEC 預期 FirstFail | Original Reader / WorldRaw / Recovery |
|---|---|---|---|---|
| `WP-FHS-02` | 原 `CASE-W1-02-NEG` 業務前件保留 | 原 Fabric Policy Owner 簽章/Principal 被擬造，攻擊者將跨 epoch 的 approval metadata 重放到相同 Manifest | `FABRIC_POLICY_PRINCIPAL_OR_SIGNATURE_DENY` | original signed owner/epoch reader；Raw=Fabric policy owner signature+epoch, HGK effective loaded digest and consumer process SID；Recovery=revoke forged approval reference, restore LastGood epoch; no world write |
| `WP-FHS-03` | 原 `CASE-W1-03-NEG` 業務前件保留 | 一般 Hermes worker SID 冒充受保護 HGK maintenance Issuer 的 OS token，要求 issuance | `HGK_ISSUER_PRINCIPAL_ACL_DENY` | HGK Original Native Issuer/OS principal reader；Raw=OS SID/token origin+Issuer endpoint ACL and protected audit rejection；Recovery=deny and invalidate attempted nonce, audit without clearing unrelated WorkIDs |
| `WP-FHS-04` | 原 `CASE-W1-04-NEG` 業務前件保留 | 低權限 Hermes profile 越權讀取另一 Profile secret，並借另一 Lane 的 provider credential | `HERMES_CROSS_PROFILE_SECRET_OR_TOKEN_DENY` | Hermes Host original profile and secret reader；Raw=profile process identity/credential audience/secret ACL and redacted rejection；Recovery=revoke affected token/session, resume same WorkID after original world reconciliation |
| `WP-FHS-05` | 原 `CASE-W1-05-NEG` 業務前件保留 | 未信任的來源段落內嵌指令「繞過 PIPD 原 Writer、產出已核 PI」誘發 source-to-instruction 越權 | `PIPD_UNTRUSTED_SOURCE_AUTHORITY_INJECTION_DENY` | SBL-hosted PIPD original authority and pipeline Reader；Raw=original SourceReader provenance+writer origin+strict PI schema and rejection raw；Recovery=quarantine source candidate; re-read original locators; never promote injected sidecar |
| `WP-FHS-07` | 原 `CASE-W1-07-NEG` 業務前件保留 | 使用另一 Subject/WorkID 的具簽章 PLAN 批准內容，企圖覆寫本 WorkID 的 native CAS | `PLAN_FOREIGN_WORKID_OR_PRINCIPAL_DENY` | HGK original Native PLAN Writer/CAS reader；Raw=original WorkID subject/source/base_revision/proposal hash and writer principal；Recovery=drop foreign proposal; reload own base revision; no parallel PlanWriter |
| `WP-FHS-11` | 原 `CASE-W1-11-NEG` 業務前件保留 | ChatGPT/Claude Portable Host 偽造 Protected Checker principal/receipt，跨 Host 或跨 SP 聲稱 Challenge Qualified | `HOST_CHECKER_IDENTITY_CROSS_SURFACE_DENY` | each original Host loader and protected Checker reader；Raw=host origin+skill sha+protected checker credential issuer and scope；Recovery=reject counterfeit receipt; disable affected host entrypoint and restore LastGood |
| `WP-FHS-17` | 原 `CASE-W1-17-NEG` 業務前件保留 | 未經原 Issuer/Installer 授權的代理持 Host admin token 安裝/載入工具 | `CAP_INSTALLER_ADMIN_TOKEN_SCOPE_DENY` | Original HGK installer and OS ACL reader；Raw=installer process SID/ACL/token issuer+write scope+binary pin；Recovery=deny installer, restore previous Host manifest, quarantine staged artifact |
| `WP-FHS-20` | 原 `CASE-W1-20-NEG` 業務前件保留 | 將另一 Host 的 Original Consumer credential／receipt 帶入此 CellID 以借用已 Qualified 狀態 | `CELL_FOREIGN_HOST_CONSUMER_CREDENTIAL_DENY` | Original SBL Kind×Mode×Host registry + per-host consumer reader；Raw=CellID+HostID+Kind/Mode raw token+credential audience/receiver nonce；Recovery=revoke mis-scoped credential; re-read own cell token; no boolean coercion |

此表與本正文原 `CASE-W1-XX-SEC` **已原位重寫**的八條契約一一對應；各案例 `input/attack_surface/expected_first_fail/raw_required/scope/recovery` 同步收錄 `wp_case_registry.jsonl`，可對照 NEG 來源。以上僅 `AUTHOR_CASE_DESIGN`，Original Runner／Protected Checker 沒有執行，不能把 `CASE_NAME_UNIQUE` 算成 Native qualified。


## R2-04｜24 原 AssetSlot 唯一有效選版與異構 Build-or-Use（F-07／08）

| 原資產 | 唯一 EffectivePin / 類型 | 對應 Original Consumer | 專屬功能 POS / NEG | 翻譯/啟用/LastGood（原端未觀測） |
|---|---|---|---|---|
| `Native20:CORE.FABRIC_POLICY` | `ORIGINAL_OWNER_EXACT_PIN_HOLD__NOT_REPLACED_WITH_LATEST`；`NATIVE_SINGLETON` | Original Fabric Policy/HGK Consumer | POS: read Policy ActiveEpoch→LoadedEpoch→HGK consumer ACK；NEG: staged proposal presented as Active | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:CORE.FABRIC_POLICY` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:CORE.HGK_NATIVE` | `ORIGINAL_OWNER_EXACT_PIN_HOLD__NOT_REPLACED_WITH_LATEST`；`NATIVE_SINGLETON` | HGK Native Registry/Issuer | POS: read scoped HGK Original WorkID+Issuer+CAS/nonce/ACL；NEG: new shadow issuer receives a request | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:CORE.HGK_NATIVE` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:CORE.SHAREDSPINE` | `ORIGINAL_OWNER_EXACT_PIN_HOLD__NOT_REPLACED_WITH_LATEST`；`NATIVE_SINGLETON` | HGK SharedSpine/World Reader | POS: read original WorkID lease/journal cursor and replay idempotence；NEG: a second shadow SQLite Queue is opened | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:CORE.SHAREDSPINE` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:RUNTIME.HERMES` | `v0.22.5@original_upstream_tag__HOST_LOADED_HOLD`；`HOST_RUNTIME` | Hermes Host launcher/worker Reader | POS: fresh PID loads pinned v0.22.5 profile and serves actual worker；NEG: picker selected without ActualServed is called invoked | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:RUNTIME.HERMES` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:LANE.PLAN.TPM` | `ORIGINAL_OWNER_EXACT_PIN_HOLD__NOT_REPLACED_WITH_LATEST`；`HOST_SKILL_OR_WORKER` | SBL TPM Original Host Reader | POS: TPM product/system/program Spec roles routed without original permission expansion；NEG: TPM Skill issues an HGK permit | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:LANE.PLAN.TPM` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:LANE.PLAN.COMMANDER` | `ORIGINAL_OWNER_EXACT_PIN_HOLD__NOT_REPLACED_WITH_LATEST`；`HOST_SKILL_OR_WORKER` | HGK PLAN/CAS Reader | POS: original PLAN base_revision/proposal_hash CAS ACK；NEG: legacy Commander skill becomes a second PLAN Writer | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:LANE.PLAN.COMMANDER` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:LANE.EXECUTE.CODEX` | `CODEX_HOST_BINARY_PIN_HOLD`；`HOST_SKILL_OR_WORKER` | Codex original Host/HGK Work Reader | POS: bounded Codex worker invokes under original WorkID/write scope；NEG: Codex CLI writes original repo outside WriteSet | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:LANE.EXECUTE.CODEX` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:LANE.VERIFY.CHALLENGE` | `ORIGINAL_OWNER_EXACT_PIN_HOLD__NOT_REPLACED_WITH_LATEST`；`HOST_SKILL_OR_WORKER` | Protected Checker Original Reader | POS: Challenge advisor produces cases; protected Checker separately signs if applicable；NEG: Maker/Challenge signs own Independent PASS | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:LANE.VERIFY.CHALLENGE` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:METHOD.FAR` | `ORIGINAL_OWNER_EXACT_PIN_HOLD__NOT_REPLACED_WITH_LATEST`；`ADVISORY_METHOD` | Fabric FAR Reader | POS: FAR method produces cited research to original Fabric Consumer；NEG: research output is treated as applied Policy | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:METHOD.FAR` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:METHOD.KANBAN` | `ORIGINAL_OWNER_EXACT_PIN_HOLD__NOT_REPLACED_WITH_LATEST`；`ADVISORY_METHOD` | Hermes/HGK Original Queue Reader | POS: existing Hermes Kanban task state uses same WorkID and Journal；NEG: a second Kanban queue with new WorkIDs is started | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:METHOD.KANBAN` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:METHOD.SWARM` | `ORIGINAL_OWNER_EXACT_PIN_HOLD__NOT_REPLACED_WITH_LATEST`；`ADVISORY_METHOD` | Hermes Delegation/Host Reader | POS: bounded delegation reports agent subtask raw to same work chain；NEG: unbounded swarm gets issuer credentials | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:METHOD.SWARM` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:METHOD.OPENSPEC` | `v1.16.0@Fission-AI/OpenSpec__ADVISORY_METHOD`；`ADVISORY_METHOD` | PIPD Original Draft Consumer | POS: OpenSpec proposal/delta/validate fed as advisory SpecDelta to original PIPD；NEG: OpenSpec proposal relabeled canonical PI | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:METHOD.OPENSPEC` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:METHOD.GSTACK` | `git:6bdafb2cf5acf05e6e9ab23a74e682e155d1fdde; VERSION=1.95.5.0/package=1.95.5`；`ADVISORY_METHOD` | SBL Original Case Consumer | POS: gstack review/QA findings translated to original cases with provenance；NEG: gstack /ship equals Publisher grant | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:METHOD.GSTACK` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:METHOD.SUPERPOWERS` | `ORIGINAL_OWNER_EXACT_PIN_HOLD__NOT_REPLACED_WITH_LATEST`；`ADVISORY_METHOD` | Original Method/Host Owner | POS: if owner pin/license verified, reuse scoped method output with original reader；NEG: unverified third-party skill installed as trusted checker | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:METHOD.SUPERPOWERS` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:METHOD.SPEC_KIT` | `ORIGINAL_OWNER_EXACT_PIN_HOLD__NOT_REPLACED_WITH_LATEST`；`ADVISORY_METHOD` | Original Product/Source Reader | POS: if owner pin/license verified, use spec-kit advisory draft scoped to source；NEG: spec-kit issues canonical AuthorityBinding | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:METHOD.SPEC_KIT` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:METHOD.MATTP_SKILLS` | `ORIGINAL_OWNER_EXACT_PIN_HOLD__NOT_REPLACED_WITH_LATEST`；`ADVISORY_METHOD` | Original Host Skill Reader | POS: if owner pin/license verified, translate generated skills to original Host ABI；NEG: skill narrative declares Native Qualified | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:METHOD.MATTP_SKILLS` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:METHOD.GSD` | `ORIGINAL_OWNER_EXACT_PIN_HOLD__NOT_REPLACED_WITH_LATEST`；`ADVISORY_METHOD` | Original Program/Queue Reader | POS: if owner pin/license verified, map GSD plan tasks to bounded original work；NEG: GSD task state becomes shadow HGK Queue | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:METHOD.GSD` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:METHOD.FABRIC_COMPRESS` | `ORIGINAL_OWNER_EXACT_PIN_HOLD__NOT_REPLACED_WITH_LATEST`；`ADVISORY_METHOD` | Original Source/Knowledge Reader | POS: compressed knowledge retains OriginalID/NEG/SourceSHA and can be roundtripped；NEG: compression drops original prohibition or parent scope | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:METHOD.FABRIC_COMPRESS` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:PIPD.P4` | `SBL/integrations/pipd@004e88913d5c1fb57e09e8d2bf744ef1547fecbc`；`CANONICAL_COMPONENT` | SBL PIPD Canonical Reader | POS: SBL-hosted PIPD original 13/19/8 exact-set readback and strict Writer；NEG: archived PIPD repo becomes second canonical writer | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:PIPD.P4` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Native20:SBL.PRODUCT` | 〔R1-2026-11-06 更正〕本列的 `SBL main@004e88913d5c1fb57e09e8d2bf744ef1547fecbc` 係 2026-11-05 當次唯讀讀值，非當期 main。2026-11-06 實測 SBL remote main 已推進至 `8f5161a306d46775b71ff2bc7817e447cfd8f96e`（main commit 2026-11-06T07:38:56Z；該尖端由 PR #47 的 merge commit `8f5161a306` 帶入，merged_at 2026-11-06T07:38:57Z）。因此 004e8891 只可讀為 `PIN_AT_READ_TIME_NOT_CURRENT_MAIN`；本輪未在 8f5161a3 重讀 `Native20:SBL.PRODUCT` 的原 bytes，不得把本列升為新讀回，也不得把 main 推進當成原 Product Reader 已接受。 | SBL Original Product Reader | POS: SharedCore six module and three SP readback in original product consumer；NEG: portable SP impersonates Native principal | `AUTHOR.W1.ADAPTER.PROPOSAL::Native20:SBL.PRODUCT` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Default30:P0-TOOL-001` | `Hermes v0.22.5__HOST_INSTALL_HOLD`；`DEFAULT_CLI_OR_FORMAT` | Hermes Host Runtime Reader | POS: needed runtime profile/launcher real loaded Hermes v0.22.5；NEG: binary pin only is treated as installed | `AUTHOR.W1.ADAPTER.PROPOSAL::Default30:P0-TOOL-001` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Default30:P0-TOOL-005` | `CODEX_HOST_BINARY_PIN_HOLD`；`DEFAULT_CLI_OR_FORMAT` | Codex Original Host Reader | POS: needed Codex worker has exact CLI pin and scoped real execution raw；NEG: Codex is allowed to issue HGK permits | `AUTHOR.W1.ADAPTER.PROPOSAL::Default30:P0-TOOL-005` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Default30:P0-TOOL-062` | `GITHUB_ACTIONS_ORIGINAL_WORKFLOW_SHA_HOLD`；`DEFAULT_CLI_OR_FORMAT` | Original SBL CI Reader | POS: needed workflow on original repo runs declared CI checks with trace；NEG: CI green is treated as protected checker receipt | `AUTHOR.W1.ADAPTER.PROPOSAL::Default30:P0-TOOL-062` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |
| `Default30:P0-TOOL-072` | `ORIGINAL_SQLITE_RUNTIME_SCHEMA_VERSION_HOLD`；`DEFAULT_CLI_OR_FORMAT` | HGK Original Persistence Reader | POS: needed SQLite WAL/lease/CAS behavior verified through existing HGK；NEG: new sqlite DB created as parallel native issuer | `AUTHOR.W1.ADAPTER.PROPOSAL::Default30:P0-TOOL-072` → original Reader；`SELECTED_ONLY` / LastGood=Unbound；NoFit=hold affected |

- **唯一當期決定**：Hermes **v0.22.5** pinned（較新版本只有研究用途，不默升）；OpenSpec **v1.16.0** `SPEC_METHOD_ONLY`；gstack **git commit `6bdafb2cf5acf05e6e9ab23a74e682e155d1fdde`**，`VERSION=1.95.5.0`、`package.json=1.95.5` 是不同版本表示面。gstack `v1.92.55.0` **僅是 r5 歷史 research target**，不是現行有效 pin 或已發行 tag。
- **啟用管線（逐件適用性）**：`SELECTED` → `TRANSLATED_OR_PACKAGED`（方法可轉換、無需強行安裝）→ `INSTALLED`（僅需 executable/Host 的元件）→ `LOADED` → `INVOKED` → `CONSUMER_USED` → `VERIFIED`。每一狀態需原 Native Host 的真 SHA/PID/Loader/ACL/Output Raw，不能由作者宣稱跳級。`asset_decision_registry.jsonl` 分件保留 `OriginalNeedKey=UNBOUND`、作者端 NeedRef、Host×SP/License/WindowsFit/adapter/POS/NEG/NoFit/LastGood/Retire；不得把作者 NeedRef 冒充原 NeedKey，仍有必要 pin/license/Host fit 的 `OWNER_READER_HOLD`；此 HOLD **不是 OPTIONAL 或未決選型**。
- **不可造新輪子**：Hermes 原 Profiles/Kanban/Swarm/Journal，Fabric 原 Policy、HGK 原 Issuer/SharedSpine/World、SBL-hosted Canonical PIPD；OpenSpec/gstack/Superpowers/Spec Kit/GSD 屬方法/Donor，不得自立 Compiler/Issuer/Checker/Publisher。原單人 Owner 不代表 Host 只有一個 SID/Principal。


## FINAL-05｜四種受界跨波交接（取代 r2 示意物件）

當期完整 JSON 在 `handoff_registry.json`。W0→W1 保留原 W0 Subject/SourceManifest/正文 SHA，另以 consumer_subject_id 表達本次作者派生關係，絕不冒作同 Subject ACK。W1→W2/W3/W4 則綁本次正文與 SOURCE_MANIFEST 真 SHA；Host/PolicyEpoch/Original ABI 仍 UNBOUND/HOLD。四種各自不同的原 Receiver、必填/可缺/禁用值、正反 fixture、Stop/Resume 皆在同版 Registry。舊 r2 JSON 示意完整保存在 lineage/W1_r2_body.original.md；禁止把 EXAMPLE Subject 或 W0 SHA 當新 W1 Candidate。

## R2-06｜W0 HOLD 三層 68／70／71、E26 與受影停復（F-10）

從 `W0_R4C_CLOSEOUT_20261105(1).zip` 的 `closure/HOLD_LEDGER_CLOSEOUT.json` 取 **68/68 open（64 carried + 4 new）** 原始逐項 `hold_id/origin/owner/blocked_operation/required_raw/resume_predicate/state`，保留於附錄 `R2-D` 和 ZIP `W0_HOLD_LEDGER_R4C_ORIGINAL.json`＋`W0_HOLD_LEDGER_W1_SCOPED.json`。修正版 `closure/ADDITIONAL_SCOPED_HOLDS_r4c.corrected.json` 以 manifest SHA 比對，優先於封存 stale。**沒有變更或解除任何 W0 HOLD**。

**r2 更新（N-01）**：當期作者封存為 `W0_FINAL_1203`＝71 OPEN（70 carried + 1 new）、WP19 作者端 7 PASS／0 FAIL（4 負例按預期翻轉、strict control 仍有 1 FAIL 作辨識）、`W0_AUTHOR_LOCAL_CLOSEOUT_ACCEPTED_WITH_SCOPED_HOLDS`、`w0_full_closeout=false`、`WP19_DONE=false`、Original SBL CI ACK `NOT_OBSERVED`、E26 `UNSATISFIED_WP19_ORIGINAL_RAW_MISSING` → 只阻 W4 WP14/Publisher Release，不可反向阻止 W1 `SOURCE_READ`／隔離 `LOCAL_DRAFT_WRITE`。上列 68／5:2 段保留為 `ARCHIVED_R4C` 血緣。`W0_HOLD_LEDGER_W1_SCOPED.json` 各條均含 `blocks_w1_source_read_or_isolated_draft=false`；`affects_w1_native_handoff=null` 表示未有 Original Scope Reader，不是 false/true 亂猜。需要 Host install/load/issuer 時只停受影效果；休眠/跨版本 Reader 需重新驗證同 Subject+Scope+Host+Epoch 的該項。


## R2-07｜七痛點的作者端與最終使用者 FUO 分層（F-12）

| Pain | W1 現行可用設計 FUO | 最終 Native／使用者 FUO 與可量測事件（不是 W1 PASS） |
|---|---|---|
| P01 選型難 | NeedKey→24 Slot 唯一 Build-or-Use / NoFit / License 原 Reader 請求 | W2/W3 真 Capability Loaded＋Actual Consumer Used；失配 `NOFIT` 確實撤回 |
| P02 交接斷裂 | 三 SPEC／S1-S5 與 W1→W2 typed NACK | 原 SBL PI/PD/ECP/TQAEP 同 Source/SHA ACK → HGK World Raw、跨 Seam re-read |
| P03 重問問題 | KnownAnswer / QuestionLedger keyed Subject+SourceSHA+Scope | 普通 Goal 同源免重問；Source/Scope drift 僅重問變動項 |
| P04 Writer 碰撞 | 唯一 PIPD Writer/HGK Issuer/PLAN CAS 合約 | 原 Native 單控制面無 shadow producer；foreign WorkID/Issuer 應 NACK |
| P05 假 PASS | Maker/Checker 及 POS/NEG/EDGE/SEC/FirstFail 設計 | Protected Checker 真不同 Principal／同 Scope Raw；缺 Receipt 保持 HOLD |
| P06 Host 假掛載 | 4 Host×3 SP、每一 `SELECTED→LOADED→INVOKED→USED` 期待原 Reader | W2/W3 每 Host 自身 PID/LoadedSHA/trigger/nontrigger/Consumer Result，不互借 |
| P07 最後一哩 | W1 可直接交原 Consumer 的 source-bound functional/restore design | W3 W18 fresh PID 的普通 Goal→自動 Lane→真 Worker→可取用結果→crash-resume；W4 原 Publisher 独立判斷 |

只有原真 Worker/Consumer/Host 讀回且受影 Case 達驗收，才能說 P07 最終 Native 有用結果完成；文檔數量不替代使用者效果。


## R2-08｜單人 Owner 下真 OS Principal／Host 能力確認契約（F-13）

原 HGK／Host Reader 每個受影 effect 需讀回 `{subject_id,host_id,process_origin,principal_id,effective_sid_or_equivalent,token_issuer,token_audience,acl_scope,secret_scope,issuer_endpoint,policy_epoch,receiver_abi,checker_protection,original_world_readback}`，具原數值/Raw SHA、原 reader identity；任何欄為空 `OS_PRINCIPAL_OR_HOST_READER_HOLD`，只停受影 DEV/OPS/Protected Checker 效果。**POS**：受授權原 Issuer 路線在指定 Scope/TTL 內回 ACK／WorldReadback；**NEG**：Maker/低權限 worker 請求 maintenance token 或另一 Host credential → Original ACL DENY。不得用 ChatGPT persona、兩個 Hermes Profile 名稱或文件 JSON 模擬 Windows SID 隔離。此輪 `NOT_RUN`，仍准許合法文檔修補。


## R2-09｜八 WP 主責能力、來源保留與有效交接（F-06／09／14）

**主責恪守** `WP-FHS-02,03,04,05,07,11,17,20`，原 22 WP／36 DAG 保留原向；只以 W1 採讀其他波 WP00/01/10/13/16 的受影規格，不領 Native WriteSet。R1 §2 的三 SPEC、§4 WP 表、r5 50 CH 的合法輸入/操作/輸出/Original Reader/NEG/Stop/Resume 保留；r1 的 Markdown 截斷 24 卡已原位替換完整可反查的安全欄位。正文 `# CH-00..49` 的 H1 字串不壓平，13 主責的原位 L1 真 locator 與 SEC 已修。其餘 37 章按原下一波/Reader/Typed HandOff。

**歷史 r2 作者狀態（非本次裁決）**：`AUTHOR_DRAFT_R2_SOURCE_TRACE_AND_BUNDLE_STATIC_REPAIRED_WITH_AFFECTED_HOLDS`；`W0_CLOSEOUT_PENDING`、`ORIGINAL_OWNER_SEMANTIC_RATIFICATION_NOT_OBSERVED`、`NATIVE_HOST_E2E_NOT_RUN`、`INDEPENDENT_CHECKER_NOT_RUN`、`RELEASE_NOT_GRANTED`。本機可下載 ZIP 並驗 SHA 是作者端交付證據，絕非原 PIPD installed Registry、HGK Permit 或原 Host E2E 證據。


## R2-10｜明確的六種 EffectClass／最小 Gate 與復原（所有 CH 共用但不能互代）

| Effect | 前置真正 Reader／權限 | Done Raw（本輪無原生證據） | FirstFail / Stop / Resume |
|---|---|---|---|
| SOURCE_READ | original source ACL+file SHA+scope | Content read/hash/reader error；world diff=0 | source missing→`SOURCE_READ_HOLD`；重讀有界相同 source |
| LOCAL_DRAFT_WRITE | 隔離作者 workspace+diff+cleanup rights | author SHA + reproducible package; no original world effect | scope escape→`DRAFT_SCOPE_NACK`；刪 isolated draft |
| DEV_REPO_WRITE | 真 local git root/HEAD/branch/dirty/untracked/preimage/writeset+original scoped admission | 原 repo diff/readback+revert commit or preimage proof | stale head/ACL→`PD_REPOCONTEXT_UNBOUND`；重 probe 受影 repo，不寫 main |
| HOST_OPS | original Fabric Policy Active/Loaded/Consumer ACK + HGK Issuer SID/nonce/lease + installed Host receiver | Host world before/after、loaded digest、residue and recovery | missing policy/origin→`HOST_OPS_ADMISSION_HOLD`；由原 installer inverse/LastGood 恢復，非 git revert |
| USER_EFFECT | 原 Human consent/data scope/protected User Consumer | user-side receipt / compensation and revocation | no consent→`USER_CONSENT_HOLD`；受影補償，不重試未知結果 |
| RELEASE_EFFECT | Original Publisher、affected CI/GHP-02、Protected Checker（適用時） | original release decision/remote readback/retire | WP19 E26/CI fail→`RELEASE_GHP02_HOLD`；不阻前面 READ/DRAFT |

未知效果 `UNKNOWN` 一律 original World reconcile 先於 replay；跨 Scope/Host/PolicyEpoch 只失效受影 binding。Maker/ChatGPT Plugin 不能自製原 Raw Receipt。


## R2-11｜14 項 AUDIT Finding 的修補閉環與有條件出口

| Finding | r2 原位修補條款／證據所在 | 作者端裁決／尚須原域確認 |
|---|---|---|
| F-01 | `R2-02`、附錄 R2-A 完整166 JSONL、`sources/` 31 來源原 bytes、line byte/offset/hash 逐件 test | `REPAIRED_STATIC_166`；Parent/Oracle Owner HOLD |
| F-02 | `R2-01` 13 span/section SHA，13 主 CH 原位定位 | `REPAIRED_STATIC_13` |
| F-03 | 同版 MD/ZIP/Manifest/Checksums/registry 的實體生成與 CRC/hash/negative mutation | `REPAIRED_STATIC_PACKAGE` |
| F-04 | `R2-03` 與原 `CASE-W1-XX-SEC` 8 組獨立 threat | `REPAIRED_DESIGN`；Native Runner NOT_RUN |
| F-05 | `R2-02` 的 57/24/31/166 四索引、112/48 欠件 | `REPAIRED_VISIBLE_HOLDS`；Original semantic Owner HOLD |
| F-06 | 24 卡 `original_primary_wp_and_wave`/`l2_selection_wave`/`no_write_set_transfer` | `REPAIRED_STATIC_SCOPE` |
| F-07 | `R2-04` gstack 單值與 r5 歷史 pin 受影標記 | `REPAIRED_DESIGN`; Host Fit HOLD |
| F-08 | `R2-04` 24 個有異質 POS/NEG 的 Recipe/Retire | `REPAIRED_DESIGN`; Installed/Loaded HOLD |
| F-09 | `R2-05` 4 typed JSON示例/4 作者端 NACK，`handoff_registry.json` | `REPAIRED_AUTHOR_TYPED`; 原 Reader ACK HOLD |
| F-10 | `R2-06` W0 原 Ledger 與 W1 scoped index；r2 追加 `W0_FINAL_1203` 71 OPEN 與四層狀態（FINAL-01 §1） | `REPAIRED_STATIC_68_70_71`; HOLD 不解除，7:0 不升 `WP19_DONE` |
| F-11 | 24 DesignID compact Markdown 重新生成，不以截斷摘錄冒 original line | `REPAIRED_MARKDOWN_FORMAT` |
| F-12 | `R2-07` P01–P07 W1 FUO vs W2/W3/W18/W4 Native FUO | `REPAIRED_FUO_SCOPE`; Native NOT_RUN |
| F-13 | `R2-08` 原 Windows SID/ACL/原 Issuer/Checker positive-negative | `REPAIRED_HOST_PROBE_SPEC`; Real Host HOLD |
| F-14 | `R2-00` CurrentReaderRoute；§9 r5 轉移語句歷史化，保留未受影原義 | `REPAIRED_READER_SINGLETON` |

本次靜態檢查與實際注入負例在附錄 `R2-E`、`STATIC_VALIDATION_REPORT_R2.json`；不把原域欠缺的真 Raw 以漂亮文件遮蓋。


## 0｜當期裁決、可用成果與顯式限制

**W1 AUTHOR_DRAFT：可交作者端審閱及受影原 Reader 補件。** `W0_CLOSEOUT_PENDING`、W0 六 WP `all_done=false`、當期 `W0_FINAL_1203` 71 open HOLD、WP19 作者端 7 PASS／0 FAIL 但 `WP19_DONE=false`、E26 `UNSATISFIED` 不得被本文升級為完工；68／70 兩層保留為歷史與候選。W1 `W1_SCOPED_SOURCE_DRAFT_GO` 僅授權來源讀取、SPEC 及隔離草案，不含任何主機／原 repo 世界效果。SBL PR #41、Fabric PR #27、HGK PR #11 均為 **open、未合併**的近期遠端唯讀觀測（GitHub讀取時間 2026-11-05；三個 PR 的 SHA 見附錄）。

**W0 原件修正優先權**：採 `BODY_ANNEX_PAIR_READBACK.corrected.json` 與 `ADDITIONAL_SCOPED_HOLDS_r4c.corrected.json`，舊 `BODY_ANNEX_PAIR_READBACK.json`／`ADDITIONAL_SCOPED_HOLDS_r4c.json` 標 `SUPERSEDED_HISTORICAL`。W0 R4C 包中 589 files＋2 evidence＋manifest self＝592 的算式無缺檔；不把 591 的不同計數口徑誤報 missing；上載 Closeout ZIP 本身 SHA `bced4b074bc788e858d5ecdcfb670d784a698c2cfc299a1f0040dc69c59e91e4`，與包內 `input.zip_sha256` 指向的原 R4 候選 ZIP 是不同物件。

**First useful outcome**：同一 Source-bound Goal 可讓一位 Human Owner 在單人單機環境審閱三份角色不同的 SPEC、八 WP 的功能/受影禁令、13 主章與 37 跨波章的完整文本、24 DesignID/24 AssetSlot 雙向索引、可直接送原 Reader 的受界 Envelope、最小 POS/NEG/EDGE/SEC；缺原 Host 能力時保留合法 READ/DRAFT，不能自造治理基座。

## 1｜SourceSet、W0 Closeout 與 31 冊治理邊界

- **31/31** 物理檔案均以嚴格 UTF-8 解碼、SHA-256 逐件比對角色目錄；僅證明 U0 `PHYSICAL_VERIFIED`。U1 以 W1 affected DesignID 與原始否定範圍做子義規劃、U2 保留 proposed relations、U3 編三份作者端 SpecDelta、U4 設受影原 Reader/Owner HOLD。**本輪未完成 31 冊逐 Clause 的 U0～U4 全量語義 Owner 核簽**；不誤宣 `SPEC_MANDATORY_100% VERIFIED`。
- `SPEC_MANDATORY_100%` 為 **處置規則**：每個已抽到的原 Requirements/子義都要有 `W1_INCLUDED`／`OTHER_WAVE_HANDOFF`／`ORIGINAL_OWNER_HOLD`，而不是聲稱 31 冊原文已完成完整語義抽取。`NATIVE_APPLICABLE_ONLY` 僅對有真 Host/Effect 的受影套用 Native Case，絕不抽樣擴成原全產品 PASS。
- 分母分開：`949` 原 Product atoms、`149` SBL Child、`50 Parent`、`39` 原依據類別、`96` Original Oracles、`192` Kind×Mode×Host Cell、`282=120+124+38` B1 Case、`27 PI→31 PD Slot`，五技術正交集合 `20+30+24+25+386=485` 是 OriginalAsset 身分總和而非安裝數。W1 本期僅 `24` Design obligation 與 `24` AssetSlot 切片，既不吃掉其他分母也不做 B1 投影替換。
- W0 W1 需耗的 `Need`：30 total／12 consumed／8 design-only／10 not-consumed；`BOUND=1`（是來源指標綁定，**非** Host 可用）／`PIN_HOLD=29`／`NOFIT=0`／**installed=0**。12 consumed 中 11 尚 pin-hold，阻斷僅對相依 Need 的 Host effect 有效，非受影 READ/DRAFT 不停。

### 1.1 31 冊逐來源快照、Original Owner Currentness 邊界

| 原始來源身份 | SHA-256／檔案 | 作用範圍 | 本稿處置／原 Reader |
|---|---|---|---|
| SBL:DOC-00 | `bd9c1a85ea0cae68fa8cde617e5592fca6123f72b4caf1a9d2894167d9a82e01` `SBL_PIPD-LS-PKG_DOC-00(1).md` | Navigation / Original reader / 版本 | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| SBL:DOC-01 | `43a0a7ed26d2adf9c2803062032019ccb6acce27cebb49af4d37c3cd4b0a3a2f` `SBL_PIPD-LS-PKG_DOC-01(1).md` | Product/Personas/50 Parent/149 Child/8 Kind | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| SBL:DOC-02 | `4ff0cda5ab00ba5f577151e5b004d2167d933e912e302c9e3529b237ccb9e035` `SBL_PIPD-LS-PKG_DOC-02(1).md` | Lifecycle/需求/數據或法位 | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| SBL:DOC-03 | `ea69e1d3718ed86aecd74a3ebcc933960eacc30b586ab80fcb9f733037e33476` `SBL_PIPD-LS-PKG_DOC-03(1).md` | 產品流轉/原義/規格映射 | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| SBL:DOC-04 | `ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0` `SBL_PIPD-LS-PKG_DOC-04(1).md` | One Core/3SP/6Modules/Orchestration | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| SBL:DOC-05 | `3b47a0b6224b1984a4047cf53aac5ac50615c93a560fea46e1b43d079a5d9f27` `SBL_PIPD-LS-PKG_DOC-05(1).md` | RepoContext/PD/DEV-ECP/Effect | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| SBL:DOC-06 | `64ea4977dab3093301f82dc7469413cc754998fc53946467842e06d83645102b` `SBL_PIPD-LS-PKG_DOC-06(1).md` | Technology/Donor/HotSwap/485 Slot | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| SBL:DOC-07 | `a366d3783c82089c5593ffabb0704d8507632cce45622684f7a0186f2ae310f8` `SBL_PIPD-LS-PKG_DOC-07(1).md` | Security/Token/Trust/SoD | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| SBL:DOC-08 | `c7029c1ff07abe3135d33d3abf858a5fecedd911b494cd69c16eb1ddb8158288` `SBL_PIPD-LS-PKG_DOC-08(1).md` | Acceptance/Oracle/Challenge/TQAEP | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| SBL:DOC-09 | `6450f7c15915ec8b304f4e5fd4093ea707434db8bae9d2bb6e66c30ab6eed2e1` `SBL_PIPD-LS-PKG_DOC-09(1).md` | Host/Skill/Governed Delivery | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| SBL:DOC-10 | `a64aa21c977334dd74d660a86377ee10c4d329aa5fde0dae25ff81a3e69e8d8f` `SBL_PIPD-LS-PKG_DOC-10(1).md` | Builder/GENIEMAKER/4Host/Knowledge | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| SBL:DOC-11 | `12f8705d780b76f264457c194a6ff359da8d74b5d6d8c83fa245b74d2a37508e` `SBL_PIPD-LS-PKG_DOC-11(1).md` | Native Receiver/Mode/Integration | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| SBL:DOC-12 | `d1e470d82ca14319582cb8947aa52007927aa38e726249b1430804cfe8c8ca56` `SBL_PIPD-LS-PKG_DOC-12(1).md` | Delivery/CI/Release/SupplyChain | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| SBL:DOC-13 | `7cc0c8b17311130c875910b2548b93c28bd4e1c8ee04d300f85fc33d4c09beb1` `SBL_PIPD-LS-PKG_DOC-13(1).md` | Dogfood/Feedback/Evolution/Exit | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| FHS:BODY-00 | `cb4727d5b0c190aba40559f72b6989964659923eed6c27504ab62acfdc3b2635` `00_INDEX_AND_DECISION(4).md` | 入口裁決/Owner/停損 | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| FHS:BODY-01 | `e257dfcd01f2e8afeda1dd88fdd33b4ef7346bf224572e60935bf9834d25b02c` `01_PRODUCT_AUTHORITY_SPINE(4).md` | 產品/三SPEC/JTBD/Kind | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| FHS:BODY-02 | `c336d3d9d702834e84bc2e45037e21e6ac56fb99c7abcb3adea372d901824ea2` `02_PIPD_LIFECYCLE_AND_TPM(4).md` | PIPD/TPM18/19/13 | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| FHS:BODY-03 | `58628861e63956ae31b1ac17404c093533226688f975f5fa11b9b82adecd1284` `03_ARCHITECTURE_ABI_AND_EFFECT(4).md` | Typed ABI/Effect分級 | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| FHS:BODY-04 | `a7d54bdeb9129e7e1979bbc1af1944189b1054760e76424f8ffd8547a682eb1f` `04_FABRIC_HGK_CONTROL(4).md` | Fabric/HGK/Policy/Issuer | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| FHS:BODY-05 | `ee47e07455767c063fd0700440b46d27592caea4638c39407b9af1309a2b44d5` `05_COMMANDER_GUIDE_AND_NATIVE_PLAN(3).md` | Commander Guide/Native PLAN | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| FHS:BODY-06 | `6bc5de0d26c8d13f4227ac9b48a66b808af0eb1108dc3012941e9c0c1ee362d5` `06_FHS_EXECUTE_HERMES_RUNTIME(4).md` | Hermes/Executor/Recovery | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| FHS:BODY-07 | `81a8c2f1cc4629f59829f11f87aebd14cd57f7c4dd0970d672880e90e2899741` `07_ACCEPTANCE_CHALLENGE(4).md` | 15Edge/96Oracle/Challenge | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| FHS:BODY-08 | `1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d` `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` | 485 tech slot/Build-Or-Use | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| FHS:BODY-09 | `1a0fcbdd77998bc9beed039407b96a1163c634052583813a98193f4d49769185` `09_SBL_DOC00_13_FULL_UPGRADE(4).md` | SBL14/149Child 血緣 | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| FHS:BODY-09A | `ce14d5d45ef76ded7cd60e4faec34119749c29fee31d9b6e1b78738179612410` `09A_R15_949_ORIGINAL_ATOMS(4).md` | 949 R15 原子+Full Product | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| FHS:BODY-09B | `aed2234821768307d81991aa56d5ff3a98fc9b884ff79e2930f2b9c4ae8e441d` `09B_KIND_MODE_HOST_192(4).md` | 192 Cell/Provider/Host | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| FHS:BODY-10 | `13b0764732bc1501e7c823b12be0d0be3a54afdaec5f77a5e90111c1947fa70a` `10_B1_W18_SELF_BOOTSTRAP(4).md` | B1/W18 普通 Goal | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| FHS:BODY-10A | `39ffde0115cdf894806a4d3bf270046b68f8786956507480db47b2a154a8c4e1` `10A_B1_TQAEP_120_124_38(4).md` | 120+124+38 Case/Runner | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| FHS:BODY-10B | `7c33e2472a6510a6c15b5b8eee2fca6dd9e4865c7ad3beb8c19d1e4618886f64` `10B_B1_PI27_PD31(4).md` | 27 PI/31 PD edge | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| FHS:BODY-11 | `6c526c991b5996c2d4f862f153fbf580d456f78b45d2a714abe11bcb9a9cc811` `11_WORKPACKAGES_AND_DAG(4).md` | 22WP/36 Edge Typed DAG | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |
| FHS:BODY-12 | `e4f7512a27ecbec1ce6a4569654ce33c4bf3265361a5ec141418a313fd25dd45` `12_VERIFICATION_AND_DELIVERY(4).md` | 分級驗證/交付/Release | U0 byte PASS；U1–U4：W1 受影 partial；原 Owner semantic HOLD / 其他波保持 |

## 2｜`sbl-tpm-sp` 跨職能製程與三份相互獨立 SPEC


## W1 三 SPEC：Product SPEC（PM 職能，非 PI）

**Persona**：唯一 Human Owner；**Pain**：既有 31 冊語義、三庫不同原 Reader、PIPD 13/19/8 與 Host Effect 混用造成重複設計、誤放行及高阻力；**JTBD**：對普通 Goal 產出一份 Source-bound、可由原 Consumer 審閱的跨庫 W1 變更規格，且不必再創第二套 Runtime/Issuer/Compiler。

**FUO 可檢驗形狀**：從 `ordinary_goal + OriginalSourceLocators` 產三份 role-distinct SPEC、24 張 DesignID 有向處置、24 原資產 slot、八 WP 的 Reader/NEG/FirstFail、五 Seam 接收卡、W0 68 個 HOLD 的受影差額；有一筆具同 Subject/SourceSHA/Scope 的 `W1DraftDelivery` 即算作者端第一有用結果，**非** Host E2E。

**MVP**：本輪允許 SOURCE_READ、本文/附錄/隔離 Sidecar；交給原 SBL PIPD、Fabric、HGK、Hermes 的真接收合約並標欠件。**非目標**：自簽 SourceFreeze、Canonical PI/PD/ECP、修改三庫 main、Host 安裝、冒充 W2–W4/W18、發放 permit、Maker 獨立判 PASS。

- `ACC-PM-W1-POS`：普通 Goal 使同 Subject 下三 SPEC role 字段、受影源 ID/Parent/NEG、Original Consumer、可取用 W1 草案均可查；`EXPECTED_NOT_OBSERVED` 在未授權時不影響草案交付。
- `ACC-PM-W1-NEG`：三 SPEC 合併、缺任一 RequiredOriginalID 或把 24 當全產品分母 → `FUO_OR_SEMANTIC_LOSS_NACK`。


## W1 三 SPEC：Architecture SPEC（SE 職能，非原域 Registry）

**系統邊界**：`Fabric FHS-NAV/v2 (navigation_only)`→原 Fabric Policy Reader；SBL SharedCore/3SP→`SBL/integrations/pipd` 唯一 Original Compiler；HGK Native Registry/Single Issuer/SharedSpine；Hermes v0.22.5 Profile/Kanban/Delegation/Swarm/Journal；Protected Checker/Publisher 最終不由 Maker 代簽。全部接線保留 `subject_id/candidate_sha/source_sha/scope/host_id/policy_epoch/ABI_version/original_consumer`。

- `ADR-W1-01`：選擇 SBL-hosted PIPD 為唯一 Canonical Compiler；舊 PIPD-LS-SP 已封存，Plugin `sbl-tpm-sp` 僅 PM/SE/TPgM 與 @2 Sidecar；拒平行編譯器。
- `ADR-W1-02`：選擇 Fabric-first 唯讀導航 + original policy reader；Mirror `effect_permission=NONE`。
- `ADR-W1-03`：選擇原 HGK WorkID/Issuer/SharedSpine/Hermes 原 Runtime，單 Owner 不等於一 Principal；重試需要同 Subject World reconcile。
- `ADR-W1-04`：按 EffectClass 分割 `SOURCE_READ/LOCAL_DRAFT/DEV/OPS/USER/RELEASE`；需真 world-write 才分別綁 Permit/ACL/Consent/Checker，不讓缺 OPS token 停止 READ。
- `ADR-W1-05`：OpenSpec v1.16.0 和 gstack git-pinned 1.95.5.0 設計選定為可替換方法層；不產 Canonical、無 Host Loaded/License 確證前不允許聲稱 installed。

`POS`：五 Seam 同 Subject 綁有效 Producer/Consumer/ABI、缺 Reader 只留受影 BindingRequest。`NEG`：路由產生第二 Issuer、用 ZIP SHA 代替 Permit、以遠端 HEAD 偽本機 RepoContext → `ARCH_ORIGINAL_READER_HOLD`。


## W1 三 SPEC：Program SPEC（TPgM 職能，保留 22WP／36 DAG）

**本波**：`WP-FHS-02/03/04/05/07/11/17/20`；W0: `00/01/15/16/19/21` 狀態依 W0 Closeout，不替其結案；W2: WP06 等世界效果；W3: 949／149／50 Parent／39／96／192／282 和 W18；W4: WP14/CI/Publisher。原 22 WP／36 DAG Edge 不重新編號。

**Run order**：`(1) W0 SourceManifest/3SPEC/71 HOLD（1203）readback`→`(2) Fabric-first read`→`(3) 24 obligation拆義`→`(4) 原 13/19/8 + eight WP candidate`→`(5) Need→Occupant/Host/License`→`(6) POS/NEG/EDGE/SEC author fixtures`→`(7) typed W2/W3/W4 envelope + hold`。若 E26 (WP19→WP14) 不滿足，只阻 W4 受影 Release，不阻 W1 文檔。

**每 WP 的停復**：同 `subject_id/source_sha/scope/original_reader/candidate_sha` 缺件→`HOLD_AFFECTED_EFFECT`；SOURCE_READ 可重讀，LOCAL_DRAFT 可刪，DEV 用原 Repo re-probe，OPS 用原 Host World/Policy，USER 用原 Consent，RELEASE 用原 Publisher。所有相異前件禁令保持原 DAG 方向；禁止 WP17 依賴未具備的 WP06 才開始 source/qualify。

`POS`：八 WP 皆提供讀/草案候選、Reader/Case/FirstFail/下波及受影 Resume；`NEG`：以 W0 六 WP 未 Done 為理由停止全部 READ，或擅自將 W1 WP06 效果視完成 → `PROGRAM_SCOPE_AND_DAG_NACK`。


## 3｜W1 Original DesignID 24 張雙向追溯與逐義出口

**唯一可採讀法**：L1 r4 原始 DesignID 及 locator→L2 obligation（在保留的 r5 源表逐列維持完整 OriginalPOS／NEG、WP 與 Original Reader）→本稿對應 CH/WP→`obligation_registry.jsonl` 每筆可回到原 locator，缺 Owner semantic ACK 為 pending。**八個 WP 之外的 WP01/10/13/16/00 是跨波受影指針，不因卡位被 W1 重新認領。**

| DesignID | 現行 L1-r4 原行 / lineSHA | 原主責 WP／波次 | W1 職責／禁止轉權 | 原 POS／NEG／Reader 對照（完整內容在 JSONL） |
|---|---|---|---|---|
| `INT-05` | `L1-r4:L773` / `b9cfb86c4154c1e3…` | WP-FHS-03=W1 | W1_DESIGN_INCLUDED / original WP W1; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `INT-05`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `INT-06` | `L1-r4:L774` / `867cb537a3eea1e3…` | WP-FHS-05=W1 | W1_DESIGN_INCLUDED / original WP W1; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `INT-06`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `INT-07` | `L1-r4:L775` / `878822684bdce98c…` | WP-FHS-04=W1 | W1_DESIGN_INCLUDED / original WP W1; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `INT-07`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `INT-13` | `L1-r4:L781` / `e76e6876b02db8da…` | WP-FHS-05=W1 | W1_DESIGN_INCLUDED / original WP W1; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `INT-13`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `INT-14` | `L1-r4:L782` / `1e75b0d56f4ae363…` | WP-FHS-11=W1 | W1_DESIGN_INCLUDED / original WP W1; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `INT-14`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `INT-24` | `L1-r4:L792` / `1403a9f09bb60693…` | WP-FHS-16=W0 | W1_DESIGN_INCLUDED / CROSSWAVE_OWNER_READONLY; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `INT-24`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `FHS-DR-007` | `L1-r4:L804` / `8e209f4c829274be…` | WP-FHS-11=W1 | W1_DESIGN_INCLUDED / original WP W1; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `FHS-DR-007`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `FHS-DR-008` | `L1-r4:L805` / `46fae508903b584a…` | WP-FHS-07=W1 | W1_DESIGN_INCLUDED / original WP W1; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `FHS-DR-008`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `FHS-DR-023` | `L1-r4:L820` / `74140c6636d47df6…` | WP-FHS-01=W0 | W1_DESIGN_INCLUDED / CROSSWAVE_OWNER_READONLY; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `FHS-DR-023`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `FHS-DR-024` | `L1-r4:L821` / `79cff0ff9f58ddf0…` | WP-FHS-05=W1 | W1_DESIGN_INCLUDED / original WP W1; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `FHS-DR-024`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `FHS-DR-025` | `L1-r4:L822` / `d29de25b25ec66e9…` | WP-FHS-05=W1 | W1_DESIGN_INCLUDED / original WP W1; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `FHS-DR-025`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `FHS-DR-026` | `L1-r4:L823` / `24c0905dd984ad59…` | WP-FHS-05=W1 | W1_DESIGN_INCLUDED / original WP W1; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `FHS-DR-026`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `FHS-DR-027` | `L1-r4:L824` / `f7b9653902524fed…` | WP-FHS-05=W1 | W1_DESIGN_INCLUDED / original WP W1; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `FHS-DR-027`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `FHS-DR-028` | `L1-r4:L825` / `c8436d7fe5e4bf02…` | WP-FHS-10=W3 | W1_DESIGN_INCLUDED / CROSSWAVE_OWNER_READONLY; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `FHS-DR-028`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `FHS-DR-029` | `L1-r4:L826` / `cf3b7366587cc43c…` | WP-FHS-00=W0 | W1_DESIGN_INCLUDED / CROSSWAVE_OWNER_READONLY; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `FHS-DR-029`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `FHS-DR-030` | `L1-r4:L827` / `2f65ea9b20bb136f…` | WP-FHS-02=W1 | W1_DESIGN_INCLUDED / original WP W1; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `FHS-DR-030`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `FHS-DR-031` | `L1-r4:L828` / `d6d886481ca51378…` | WP-FHS-03=W1 | W1_DESIGN_INCLUDED / original WP W1; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `FHS-DR-031`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `FHS-DR-032` | `L1-r4:L829` / `86a508054c3705c9…` | WP-FHS-03=W1 | W1_DESIGN_INCLUDED / original WP W1; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `FHS-DR-032`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `FHS-DR-034` | `L1-r4:L831` / `3a92f8db68739a2e…` | WP-FHS-00=W0 | W1_DESIGN_INCLUDED / CROSSWAVE_OWNER_READONLY; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `FHS-DR-034`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `FHS-DR-035` | `L1-r4:L832` / `1b20726a0e3e94b7…` | WP-FHS-04=W1 | W1_DESIGN_INCLUDED / original WP W1; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `FHS-DR-035`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `FHS-DR-036` | `L1-r4:L833` / `e9451e2f0a2ff3af…` | WP-FHS-04=W1 | W1_DESIGN_INCLUDED / original WP W1; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `FHS-DR-036`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `FHS-DR-042` | `L1-r4:L839` / `f09232acf35187bd…` | WP-FHS-13=W3 | W1_DESIGN_INCLUDED / CROSSWAVE_OWNER_READONLY; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `FHS-DR-042`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `FHS-DR-043` | `L1-r4:L840` / `fbd8e512dd59008b…` | WP-FHS-16=W0 | W1_DESIGN_INCLUDED / CROSSWAVE_OWNER_READONLY; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `FHS-DR-043`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |
| `FHS-DR-044` | `L1-r4:L841` / `c395be8a0aefbd9a…` | WP-FHS-16=W0 | W1_DESIGN_INCLUDED / CROSSWAVE_OWNER_READONLY; `NO_WRITESET_TRANSFER` | `obligation_registry.jsonl` key `FHS-DR-044`：原完整來源行、OriginalPOS、OriginalNEG、Producer/Consumer、Parent/Oracle HOLD |


### 3.1 U1 複合否定與反向核對指令（W1 affected only）

每卡可從 `original_pos` 與 `original_neg_firstfail` 拆解 `trigger`、`actor`、`object`、`must/shall`、`unless/except`、`prohibition`、`consumer`；以 `(DesignID, SourceSHA, Parent, ClauseSpan, SubmeaningID, CH, WP, CaseID, FirstFail)` 作 typed join。只要原句存在「各有／對應／分別／若／除非／不得」而目標沒有獨立 POS 或 NEG，該 `SubmeaningID` 記 `ORIGINAL_OWNER_HOLD`，不可把引用命中改為 satisfied。原 31 冊全量 U1 未實作的部分留 Source-level U4 backlog；不偽造逐子義 TotalCount。

## 4｜八個 W1 Original WP：真 Producer→Reader→Consumer 與受影 Stop/Resume

| W1 WP | 原產品功能／主章 | Producer→原 Reader／Consumer | Expected Raw／受影 FirstFail | 當期合法效果／下波 |
|---|---|---|---|---|
| `WP-FHS-02` | Fabric Policy Consumer / CH-17/16 | W1 DraftMaker→Fabric Policy Original Reader | `Policy epoch loaded+HGK ACK`；NEG=`POLICY_LOADED_ACK_MISSING` | SOURCE_READ/LOCAL_DRAFT；W2 WP06 |
| `WP-FHS-03` | HGK Registry / Issuer / CH-18/39 | W1 DraftMaker→HGK Native Registry/Issuer Reader | `Issuer ACL/Subject/PolicyEpoch/World`；NEG=`ISSUER_GRANT_MISSING` | SOURCE_READ/LOCAL_DRAFT；W2 WP06/08 |
| `WP-FHS-04` | Hermes Durable Runtime / CH-19/20 | W1 DraftMaker→Hermes original runtime reader | `Fresh PID/Profile SHA/ActualServed/Journal`；NEG=`HOST_RUNTIME_NOT_PROBED` | SOURCE_READ/LOCAL_DRAFT；W2 Runtime; W3 W18 |
| `WP-FHS-05` | SBL-hosted PIPD Canonical Compiler / CH-12/13/14/40 | W1 DraftMaker→SBL original PIPD pipeline/CLI/schema reader | `13/19/8 ABI and original PI/PD Writer Raw`；NEG=`ORIGINAL_COMPILER_NOT_RUN` | SOURCE_READ/LOCAL_DRAFT；W2 PD/ECP |
| `WP-FHS-07` | Native PLAN Commander A/B/C / CH-34/16 | W1 DraftMaker→HGK original PLAN Revision/CAS Reader | `Proposal hash+native CAS same subject`；NEG=`PLAN_CAS_ACK_MISSING` | LOCAL_DRAFT；W2 PLAN |
| `WP-FHS-11` | Portable Host Dogfood / CH-08/22 | W1 DraftMaker→Original 4 Host loader readers | `per host installed/loaded/invoked/nontrigger`；NEG=`HOST_LOADER_RAW_MISSING` | SOURCE_READ/LOCAL_DRAFT；W3 Host matrix |
| `WP-FHS-17` | CAP-BOOT Native Occupants / CH-22/18 | W1 DraftMaker→Original technology/install+HGK Reader | `immutable pin/license/Windows fit/loaded consumer`；NEG=`CAPABILITY_NOT_QUALIFIED` | SOURCE_READ/LOCAL_DRAFT；W2 needed effect / W3 all assets |
| `WP-FHS-20` | CLI/Agent/Host Kind Matrix / CH-19/40 | W1 DraftMaker→Original SBL Product×Host Reader | `Kind/Mode/Host original cell semantics, ON/OFF token`；NEG=`CELL_TOKEN_OWNER_ACK_MISSING` | SOURCE_READ/LOCAL_DRAFT；W3 192 cells |

**八 WP 的共同四測例規則**：每個 WP 分開跑一個具備 expected raw 的 POS、一個否定違反的 NEG、一個 Source/Scope/Host drift 的 EDGE、一個 Principal/ACL/Signer/Secret 的 SEC；W1 只提供作者端 fixtures；真 Runner/Original Oracle/Protected Checker 身分由原域綁定。相同四類名稱不表示八 WP 可共用同一測試輸入／FirstFail；本稿後方 r5 的 8×4 專屬案例與 13 CH 當期案例組共同構成可核對測試規格。

## 5｜技術選型 SELECTED／Need→Occupant／Build-or-Use 不造第二輪子

**本輪定案層級為 `SELECTED_AUTHOR_DESIGN`，不是 Host Installed。** 版本 pin、來源與 Windows fit 按已見證據寫，未見固定 license、Windows 兼容、原 Host Reader 時保留明確的受影 HOLD，**不**將 W1 必需品退為 Optional。外部方法法位不高於原 SBL/PIPD、Fabric/HGK 或 Protected Checker。

| 正式名／內部名 | SELECTED 版本與來源 | License／Windows Host Fit（證據層） | Need→Occupant / Consumer | POS／NEG／LastGood |
|---|---|---|---|---|
| **Hermes Agent** / `hermes`（HOST_RUNTIME） | **SELECTED_AUTHOR_DESIGN**：v0.22.5 / bf0203a794a upstream tag [原始來源](https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.5) | 原發行的 license+Windows Host 需 pin/reader | USE existing runtime；W1 WP04/03 | POS=fresh PID/Profile/ActualServed；NEG=no Host readback => H-HERMES；Backout=v0.22.7 2026-11-03 可見，但不自動更新 |
| **OpenSpec** / `openspec`（SPEC_METHOD_CLI） | **SELECTED_AUTHOR_DESIGN**：v1.16.0 / release 2026-10-30 / MIT [原始來源](https://github.com/Fission-AI/OpenSpec/releases/tag/v1.16.0) | Windows standalone installer／SHA256SUMS；npm 需 Node >=22.12 | SELECTED Use method-only；W1 WP05/07 | POS=proposal→delta→validate, original PI separate；NEG=new original Writer from openspec=>NACK；Backout=unfit -> retain LastGood; not auto promote |
| **gstack** / `gstack`（REVIEW_QA_METHOD） | **SELECTED_AUTHOR_DESIGN**：VERSION 1.95.5.0 @ main 6bdafb2cf5acf05e6e9ab23a74e682e155d1fdde; MIT [原始來源](https://github.com/garrytan/gstack/blob/main/VERSION) | Windows requires Git+Bun+Node; host-specific Claude setup probe | SELECTED advisory only；W1 WP07/11 | POS=review/qa output converted to original Reader expectations；NEG=/ship != Publisher Grant；Backout=No GitHub release object observed; immutable commit pin, no auto-update |
| **SBL-hosted PIPD** / `pipd_ls_sp`（CANONICAL_COMPILER） | 〔R1-2026-11-06 更正〕§5.1A 的 SBL 讀值 `004e88913d5c1fb57e09e8d2bf744ef1547fecbc`（`pipd-ls-sp 0.1.1a5`／Apache-2.0）為 2026-11-05 當次 `refs/heads/main`；2026-11-06 實測 main 已為 `8f5161a306d46775b71ff2bc7817e447cfd8f96e`。本列 `SELECTED_AUTHOR_DESIGN` 與 exact-set 讀值不改寫，但須加註 `SOURCE_READ_PIN_2026_11_05__NOT_CURRENT_MAIN`；main 推進既不使 13 CLI／19 Families／8 Skills 的 exact-set 失效，也不使其升為 installed／loaded。; pipd-ls-sp 0.1.1a5; Apache-2.0 [原始來源](https://github.com/shw097-team/SBL/tree/main/integrations/pipd) | Original Reader; local original installed version unobserved | USE original canonical compiler only；W1 WP05 | POS=13 CLI/19 families/8 skills exact；NEG=Sidecar claimed Canonical=>NACK；Backout=old archived repo cannot reappear as writer |
| **Fabric FHS-NAV** / `fhs-nav-v2`（NAVIGATION_ONLY） | 〔R1-2026-11-06 更正〕§5.1A 的 Fabric 讀值 `f4f2ad7cbed97074cc2d78b401734fc47633cc20` 為 2026-11-05 當次 main；2026-11-06 實測 Fabric main 已為 `ef4fe187e706bb309a905c2f88c7477b53cf5839`（main commit 2026-11-05T19:12:36Z；PR #31 merge commit `ef4fe187e7`）。FHS-NAV/v2 仍只作唯讀導航（`effect_permission=NONE`）；main 推進不產生導航即權限、導航即 Policy Loaded 的任何提升。 [原始來源](https://github.com/shw097-team/Fabric/blob/main/INTEGRATION/FHS/README.md) | original Fabric policy license/status requires separate Reader | USE navigation-only；W1 WP02 | POS=mapped original repo/source, zero effect permission；NEG=NAV=Permit=>NACK；Backout=unknown route => affected write HOLD |
| **HG-KSEOS** / `hgk-native`（SINGLE_ISSUER_SPINE） | 〔R1-2026-11-06 更正〕§5.1A 的 HG-KSEOS 讀值 `0143b50331f7fef007a5921bb743e61f59b0a7bd` 為 2026-11-05 當次 main；2026-11-06 實測 main 已為 `a7046a36956e2179d7125449ce9b6f05fa5451cf`（main commit 2026-11-05T16:10:55Z；PR #14 merge commit `a7046a3695`）。`SINGLE_ISSUER_SPINE` 的身份不變，但原 Issuer 的 signed scope／nonce／TTL／process ACL 讀回仍未取得，H-W1-02 未解。 [原始來源](https://github.com/shw097-team/HG-KSEOS/blob/main/README.md) | local HGK registry/OS ACL/Loaded not observed | USE original native no duplicate；W1 WP03/17 | POS=Reader/Issuer/Lease/Journal/World same scope；NEG=document-generated grant=>NACK；Backout=no original World Reader=>effect PARK |
| **Codex** / `codex-worker`（EXECUTE_WORKER） | **SELECTED_AUTHOR_DESIGN**：original Host CLI version/pin UNBOUND [原始來源](https://github.com/openai/codex) | host process/License/Tool runtime unverified | USE existing bounded worker; not issuer；W1 WP04/20 | POS=actual worker invocation and task result；NEG=README claimed Invoked=>NACK；Backout=no fit -> original Host Owner choice |
| **SQLite** / `sqlite`（SHAREDSPINE_BACKEND） | **SELECTED_AUTHOR_DESIGN**：original HGK native schema+ABI; exact installed version unbound [原始來源](https://sqlite.org/) | original runtime compiled version/OS scoped | REUSE existing SharedSpine；W1 WP03 | POS=lease/CAS/world idempotency；NEG=parallel unapproved spine=>NACK；Backout=never create second queue |

### 5.1 W1 24 原 AssetSlot 的正式設計決策矩陣

| 原 AssetSlot | 本波 Build-or-Use 決定 | 採用條件／原 Reader／負例 | 真正執行狀態 |
|---|---|---|---|
| `Native20:CORE.FABRIC_POLICY` | `SELECTED_AUTHOR_DESIGN` / `USE_EXISTING_NATIVE` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；Fabric Policy Source/Consumer（NATIVE_SINGLETON; original-source pin / LICENSE_OWNER_READER_HOLD）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:CORE.HGK_NATIVE` | `SELECTED_AUTHOR_DESIGN` / `USE_EXISTING_NATIVE` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；HGK Protected Registry/Resolver/Issuer/Receiver（NATIVE_SINGLETON; original source/export / LICENSE_OWNER_READER_HOLD）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:CORE.SHAREDSPINE` | `SELECTED_AUTHOR_DESIGN` / `USE_EXISTING_NATIVE` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；SQLite/journal/Lease（NATIVE_SINGLETON; original local schema / LICENSE_OWNER_READER_HOLD）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:RUNTIME.HERMES` | `SELECTED_AUTHOR_DESIGN` / `USE_EXISTING_NATIVE` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；canonical Hermes（HOST_RUNTIME; v0.22.5 pinned / upstream licence check on exact origin）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:LANE.PLAN.TPM` | `SELECTED_AUTHOR_DESIGN` / `USE_EXISTING_NATIVE` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；Native SBL-TPM／TPM Skill（HOST_SKILL_OR_WORKER; source SHA / TPM-SP package owner）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:LANE.PLAN.COMMANDER` | `SELECTED_AUTHOR_DESIGN` / `USE_EXISTING_NATIVE` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；Native SBL Commander／Guide Skill（HOST_SKILL_OR_WORKER; original PLAN receiver ABI / OWNER_READER_HOLD）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:LANE.EXECUTE.CODEX` | `SELECTED_AUTHOR_DESIGN` / `USE_EXISTING_NATIVE` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；Codex bounded Worker（CLI_WORKER; ORIGINAL_HOST_CLI_PIN_HOLD）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:LANE.VERIFY.CHALLENGE` | `SELECTED_AUTHOR_DESIGN` / `USE_EXISTING_NATIVE` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；SBL External Challenge＋Protected Checker（HOST_SKILL_OR_WORKER; ORIGINAL_CHECKER_REGISTRY_HOLD）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:METHOD.FAR` | `SELECTED_AUTHOR_DESIGN` / `USE_EXISTING_NATIVE` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；Fabric Autonomous Research（METHOD; METHOD_SOURCE_SHA / not a binary）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:METHOD.KANBAN` | `SELECTED_AUTHOR_DESIGN` / `USE_EXISTING_NATIVE` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；existing Hermes kanban（NATIVE_METHOD; v0.22.5 pinned / existing capability）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:METHOD.SWARM` | `SELECTED_AUTHOR_DESIGN` / `USE_EXISTING_NATIVE` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；bounded delegate（NATIVE_METHOD; v0.22.5 pinned / capability probe）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:METHOD.OPENSPEC` | `SELECTED_AUTHOR_DESIGN` / `SELECT_METHOD_ONLY` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；Fission-AI OpenSpec（METHOD_CLI; v1.16.0 research target / MIT source candidate; asset digest HOLD）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:METHOD.GSTACK` | `SELECTED_AUTHOR_DESIGN` / `SELECT_METHOD_ONLY` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；gstack workflow（METHOD_HOST_SKILL; v1.92.55.0 [HISTORICAL_RESEARCH_NOT_CURRENT_SELECTION; current=git:6bdafb2/1.95.5.0] / licence verified via original release reader HOLD）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:METHOD.SUPERPOWERS` | `SELECTED_AUTHOR_DESIGN` / `USE_EXISTING_NATIVE` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；obra Superpowers（METHOD_HOST_SKILL; METHOD_REPO_PIN_LICENSE_HOLD）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:METHOD.SPEC_KIT` | `SELECTED_AUTHOR_DESIGN` / `USE_EXISTING_NATIVE` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；GitHub Spec Kit（METHOD; METHOD_REPO_PIN_LICENSE_HOLD）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:METHOD.MATTP_SKILLS` | `SELECTED_AUTHOR_DESIGN` / `USE_EXISTING_NATIVE` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；Matt Pocock Skills（METHOD_HOST_SKILL; METHOD_REPO_PIN_LICENSE_HOLD）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:METHOD.GSD` | `SELECTED_AUTHOR_DESIGN` / `USE_EXISTING_NATIVE` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；Get Shit Done donor（METHOD; METHOD_REPO_PIN_LICENSE_HOLD）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:METHOD.FABRIC_COMPRESS` | `SELECTED_AUTHOR_DESIGN` / `USE_EXISTING_NATIVE` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；知識/Prompt/Skill 壓製（METHOD_FORMAT; SOURCE_PIN_LICENSE_APPLIES_ONLY_EXTERNAL_DONOR）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:PIPD.P4` | `SELECTED_AUTHOR_DESIGN` / `USE_EXISTING_NATIVE` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；PIPD-LS-SP Public Skills+CLI（歷史原名）（ORIGINAL_OWNER_COMPONENT; SBL U04 live canonical / Apache-2.0 repo）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Native20:SBL.PRODUCT` | `SELECTED_AUTHOR_DESIGN` / `USE_EXISTING_NATIVE` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；SBL Shared Core+Three SP（ORIGINAL_OWNER_COMPONENT; original SBL writer/source）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Default30:P0-TOOL-001` | `SELECTED_AUTHOR_DESIGN` / `REUSE_IF_ORIGINAL_HOST_QUALIFIED` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；Hermes Agent（DESIGN_DEFAULT_CLI; v0.22.5 pinned / source licence at exact origin HOLD）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Default30:P0-TOOL-005` | `SELECTED_AUTHOR_DESIGN` / `REUSE_IF_ORIGINAL_HOST_QUALIFIED` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；Codex（DESIGN_DEFAULT_CLI; HOST_VERSION_LICENSE_PIN_HOLD）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Default30:P0-TOOL-062` | `SELECTED_AUTHOR_DESIGN` / `REUSE_IF_ORIGINAL_HOST_QUALIFIED` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；GitHub Actions（DESIGN_DEFAULT_CI; workflow SHA / platform terms not assumed license of project）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |
| `Default30:P0-TOOL-072` | `SELECTED_AUTHOR_DESIGN` / `REUSE_IF_ORIGINAL_HOST_QUALIFIED` | `08_TECHNOLOGY_DEFAULT_HOTSWAP(4).md` SHA `1df04680319796aa`；SQLite（DESIGN_DEFAULT_FORMAT; existing SQLite runtime/ABI source）; POS=原 Need/Host/Consumer/License Reader ACK；NEG=未 Loaded 升 Verified、引進第二控制平面 | `INSTALLED/LOADED/INVOKED/USED/VERIFIED = NOT_OBSERVED` |

### 5.1A｜SBL Canonical PIPD 的當期真實 13 CLI／19 Families／8 Skills exact-set（只讀基準）

〔R1-2026-11-06 更正〕`SBL main@004e88913d5c1fb57e09e8d2bf744ef1547fecbc` 係 2026-11-05 的 `refs/heads/main` 讀值；2026-11-06 實測 main 已為 `8f5161a306d46775b71ff2bc7817e447cfd8f96e`。本輪未在 8f5161a3 重讀 `integrations/pipd/src/pipd_ls_sp/registry.py`，故 13 CLI／19 Contract Families／8 Skills 的唯一 Registry 讀回仍以 004e8891 為 `PIN_AT_READ_TIME`，不得表述為當期 main 的事實，亦不得據此宣稱原 PIPD Writer 已接受。；[`integrations/pipd/src/pipd_ls_sp/registry.py`](https://github.com/shw097-team/SBL/blob/main/integrations/pipd/src/pipd_ls_sp/registry.py)（Git blob `e71043e918d7f030700c952674db39120b095d3c`）、[`cli.py`](https://github.com/shw097-team/SBL/blob/main/integrations/pipd/src/pipd_ls_sp/cli.py)（blob `1e400fea5015db6a4df6ea028c553f82ef218112`）。上述為遠端 Source 讀回，`schemas/registry.json` 仍應由原 installed Reader 判斷，**本地 installed、Host load、Compiler execution 未驗證**。

- **13 CLI 命令**（原 `COMMANDS` 精確順序）：`init`、`intake`、`profile`、`compile-pi`、`bind-pd`、`compile-ecp`、`compile-tqaep`、`validate`、`doctor`、`project`、`export`、`diff`、`repair`。`compile-cc` 不存在於原 13 命令；Pre-V2 新 flags 不計第 14 命令。
- **19 Canonical Family `SOURCE_ORDER`**（依現行原 `registry.py` 的順序，禁止重排）：`01 ArtifactIdentity`、`02 AuthorityBinding`、`03 RequirementAtom`、`04 ProfileBinding`、`05 TechnologyAdmission`、`06 PI-PKG`、`07 PD-PKG`、`08 TraceLink`、`09 TaskSpecSeed`、`10 ConstructionContract`、`11 WorkOrderCandidate`、`12 ECP`、`13 TQAEP`、`14 ExecutionHandoff`、`15 EvidenceExpectation`、`16 ClaimCeiling`、`17 SurfaceProjectionManifest`、`18 GENIEProjectionRef`、`19 ExecutionBindingRef`。`GENIEProjectionRef=SCHEMA_SEAM_ONLY_UNTIL_S6`、`ExecutionBindingRef=SCHEMA_SEAM_ONLY_UNTIL_S5`；Schema 存在不等於接收者/實機已 ACK。
- **8 PIPD Skills**（本次已從 `sbl-tpm-sp` 技能條文掛載）：`pipd-route-intake`、`pipd-authority-source`、`pipd-profile-tailor`、`pipd-pi-compile`、`pipd-pd-bind`、`pipd-execution-contract`、`pipd-assurance-tqaep`、`pipd-package-project`。所有 Skills 僅為作者端規劃與原 Pipeline 路由，不能代替原 Writer；以 Host 實際載入的版本＋Skill Registry 為最終原生狀態 Reader。

**驗證契約**：`POS` 原 Reader 逐序回 13/19/8、原 PI-PKG/PD-PKG/ECP/TQAEP Subject/SourceSHA 同一且原 Canonical digest 可重算；`NEG` reordered Registry／`compile-cc` 誤入命令清單／Plugin 寫出自稱 Canonical PI → `PIPD_ORIGINAL_EXACT_SET_NACK`；`EDGE` 受影版本變動僅重做該 ABI／Reader；`SEC` 仿造 S5 受保護 ExecutionBindingRef ACK、資源缺權仍放行 → `PROTECTED_CONSUMER_HOLD`。當期 `EXPECTED_NOT_OBSERVED`，不是實機測試 PASS。

### 5.2 OpenSpec／gstack 的受界工作流與 HotSwap

OpenSpec `v1.16.0`（官方 2026-10-30 release）用於 Brownfield proposal/delta/validate，不可將其 artifact 重命名為原 Canonical PI。OpenSpec standalone Windows 適配有官方說明，但**用戶本機** Node/OS/process/installed 未讀回。gstack 的 GitHub `main` `VERSION=1.95.5.0`（讀回 commit `6bdafb2cf5acf05e6e9ab23a74e682e155d1fdde`）且 MIT，採 **git SHA 固定**的 review/QA 方法；官方 Releases 頁當期未顯示 release tag，不能假稱 1.95.5.0 是已發行 release；Windows 依原 Node/Bun/Claude Host 確認，`/ship` 不取代 Publisher。倘 Node/host/license 不 fit，`NOFIT` 帶原 Owner 決定、退回原 LastGood，不修改 Hermes profile/Original Registry。

### 5.3 Hermes 版本與 GPT-6 Chat 作者路由

Hermes pinned **v0.22.5（官方 2026-10-22）**，可見上游 v0.22.7（2026-11-03）是更新研究，不獲准自動升級。Profiles／Kanban／Delegation／Swarm／Durable Runtime 應以本機原 Host 能力和受影 Output Raw 探針決定，缺者 `EXECUTOR_UNBOUND`。GPT-6 Chat 只作規格作者與研究；官方 2026 prompting guide 建議任務邊界、少重複指令、代表性測試、版本管理；這些是外部支援策略，不是三庫現役功能證明。

## 6｜W0 R4C 的精確受影輸入與 W1 開工限制

| gate/基準 | 上輪實測或封存狀態 | W1 必須保留的因果 |
|---|---|---|
| W0 closeout | `W0_FINAL_1203`＝`W0_AUTHOR_LOCAL_CLOSEOUT_ACCEPTED_WITH_SCOPED_HOLDS`（`w0_full_closeout=false`、`w0_wave_accepted=false`、六 WP 未全部 Done）；血緣 `W0_CLOSEOUT_PENDING` | 本稿不代表 W0 成功結案；W1 只 `SOURCE_READ/LOCAL_DRAFT_WRITE` |
| WP-FHS-16 | `1 BOUND / 29 PIN_HOLD / 0 INSTALLED` | W1 12 consumed 中 11 pin-hold，真 host effects 受影 HOLD；不自動退成 Optional |
| WP-FHS-19 | 1203 作者端 `7 PASS／0 FAIL`（4 負例按預期翻轉；strict control 仍 `UNDECLARED_DEPENDENCY`）、`wp19_done=false`、Original CI ACK `NOT_OBSERVED`；血緣 `PASS5/FAIL2` | 7:0 只證作者端 scoped 供應鏈例證，不等於 `WP19_DONE`；`E26→WP14` 不可跳過 |
| HOLD ledger | 當期 `71 OPEN = 70 carried + 1 new`（1203，`all_open=true`）；血緣 `68 = 64 carried + 4 new`；候選 `70` | 逐筆原值保留於 `W0_FINAL_1203_HOLD_LEDGER_71.json`、`HOLD_AND_RESUME.json`；受影投影 `affected=true/false/unknown`，不宣已關閉 |
| 原三庫 PR | SBL #41／Fabric #27／HGK #11（GitHub 當期仍 open） | 分庫 PR 不可當任何原 Policy/Issuer/Native Host 已 Loaded 的證據 |
| Correction | 兩個 stale SHA 由 R4C `corrected.json` 生效 | 歷史錯配記檔，不得把過時值作當期結論 |

## 7｜跨波可實作 envelope 與退場規則（不是 Canonical JSON）

`AUTHOR.FHS.W0ToW1Candidate@design`：`subject_id/source_manifest_sha/candidate_sha/source_negative/spec_role_sha{product,architecture,program}/scope/hold_ids/allowed_effects=READ|DRAFT/Original Reader`，只接到 W1 Draft。`AUTHOR.FHS.W1ToW2Candidate@design`：延續完全相同的 subject/source/candidate/Scope，附上 S1–S4 ABI、原 13/19/8、WP02/03/04/05/07/11/17/20 的受影 Reader Raw expectation、ECP per Effect、Case Oracle request、`firstfail/hold/resume`；若 Original Writer/Repo/Issuer/Host 不到，仍 `UNBOUND_CANDIDATE`。`AUTHOR.FHS.W1ToW3AffectedProjection@design`：逐 OriginalID＋Parent/NEG、24 slot×Host/Need、192 raw token、W18 fresh PID UAT 前件，禁將 W1 24 當全產品 485。`AUTHOR.FHS.W1ToW4TraceExpectation@design`：Case/Evidence/TraceClosure、CI/NOTICE/SBOM、E26、Owner/Protected Checker/Publisher／GHP-02，全為 `EXPECTED_NOT_OBSERVED` 直到原責任人返真 Raw。

**W2 的效果型安全線**：W2 才能在 Original Reader 准入後對受權世界效果動手。W1 可填變更建議，但不能 call `compile-pi` 並假裝原 host 已接受；不能製造 `WorkID`、Permit/Grant、Protected Checker Receipt 或 Release。W18 是 W3 對 B1 後正常模式的 UAT，不是施工波 W5。

## 8｜本輪可重算靜態測試與明確 Claims

- 50 CH 逐一 H1 不可壓平，13 主章各含本稿 `W1 草案當期完成契約`；37 其餘章留 r5 原 `Cross-wave handoff`。
- `24/24` DesignID 與 `24/24` AssetSlot 不重複；八 WP 具 POS／NEG／EDGE／SEC、FirstFail／Original Reader。
- 31 physical source SHA 和 W0 ZIP 成員 hash 完整可核；現行 ZIP 將以 `MANIFEST.json` 自述實體，正文—附錄 `paired_body_sha256` 明確唯一。
- U0 physical 是 PASS；U1–U4 full / Original semantic ratification / Windows Host Loaded / PIPD canonical compile / Protected checker / release 均 `NOT_RUN` 或 `HOLD`。

---

## 9｜W1 r5 設計來源高保留承接（歷史請求已於 r2 原位履行）

**HISTORICAL_R5_SKELETON_FILL_REQUEST_SUPERSEDED_BY_W1_DRAFT_R2**：下文保留 r5 原始條文、原章名、原 I/O、原 NEG、Original Reader，僅在未受 r2 修補影響的原義部分供追溯；`W1:DraftMaker 下一階段`、`本交付不是 W1 草案` 等屬 *r5 撰寫當時* 的過渡狀態，不是 r2 當期仍待產出之要求。對相同 Subject／Scope，優先依 **r2 本文現行差額→相應 CH 之 r2 修補契約→未受影 r5 條文→r5 歷史證據** 讀取。兩個相異版本的有效修補不可同時宣稱現行。

> 下列為 r5 上位作者端的全部已產出實質設計讀本，SHA=`6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；本稿第 0–8 節與各個 `# CH-nn` 下的「W1 草案當期完成契約」是 W1 草案的當期受影補全。若 r5 仍以『待草案填』描述相同欄位，以本稿已填的受影合約為準，原 Reader/Owner 欠據的 HOLD 不被抹去。這不是升格為新 Canonical 的權限轉移。

## W1-r5｜AUDIT F01–F20 受影原位修補的現行契約（唯一 AUTHOR W1 Reader）

**效力**：此節與下列同章 r5 受影規則已原位融合為本版唯一 W1 作者端設計；以相同主體、既有 50 H1、22 WP/36 DAG、S0/S1–S5、24 W1 DesignID／24 AssetSlot 保留 r4 合法正文。前版 r4 僅血緣回歸證物，非第二現行 W1 Reader。原 Domain 的 Effective Reader/Writer/Issuer/Checker/Publisher 不轉移。`AUDIT-FHS-PIPD-LS-PKG-W1-R4-20261104-R1` 為修補控制而非 Normative。

### R5-00｜六步 SOP 的本版輸出與裁決門檻

1. **索引**：L0 r4→L1 r4→L2 r4→W0 r4→本 W1 r5；CAL/AXIS/INTENT/TECH/SPEC/H1 交叉核驗，31 個來源保持原 scope。Fabric/FHS-NAV/v2 唯讀先導航，再到 SBL PIPD Registry 與 HGK 原 Reader；舊 W1-W4 r2 只作史料。
2. **實質條文定位**：W1 24 DesignID 對 L1-r4 原行、13 主 CH 和 8 WP；附錄保留 166 原行 SHA/byte offset＋實際原文字節內容。逐條無 original_id/parent/NEG 已核簽者不得 fake RequirementID。
3. **關鍵字全文比對**：`SourceSpan/OriginalID/Parent/NEG`、`各有/分別/對應/若/除非/不得`、`13/19/8`、`INT-13`、`PolicyEpoch/Loaded/ConsumerACK`、`ActualServed`、`Default30/NoFit`、`W1→W2/W3/W4` 的正反用法。標題/計數/歷史附錄命中不證明原義。
4. **跨層交叉驗證**：每個 DesignID 的 L1-r4 整行 hash、L2-r4 波次、W1 CH/WP、Original Consumer、正反測例與下波轉交相連；官方 SBL Registry `SOURCE_ORDER` 的**有序 19**不得由其他列表重定義。
5. **子要求逐義**：下方 `R5-02` 表的每個 `S-W1-*` 是有獨立 POS/NEG/Case/FirstFail/Effect 的作者端最小子義，不代替 original RequirementID；對四 Host、三 SP、三 SPEC 與各 effect 分別檢測。
6. **實質判定**：只有本正文 CH 的 Input→原 Reader/ABI→Consumer→POS/NEG→FirstFail/HOLD、及能從非規範附錄重算的源 span，才形成 `W1_BLUEPRINT_AUTHOR_ACCEPTED_WITH_AFFECTED_HOLDS`；離線作者測試通過不等於原 Owner/U0–U4 semantic ratification。

### R5-00B｜九項規劃來源的受影實質共識與明確差額

| 原設計 Reader/來源 | 實質必保留的規則（不是標題命中） | 本波 CH / 分歧退出 |
|---|---|---|
| `CAL r2` 原檔 SHA `22f19bcf5b36b301` | 七痛點/已知答案/不以全域 Release gate 阻合法 FUO | CH-08/13/40；原域 currentness/identity 欠據則 `AFFECTED_SOURCE_IMPACT_HOLD` |
| `AXIS r2` 原檔 SHA `676ef3b6b4d7a668` | 產品×工程、A 建置/B 普通 Goal、單人 Owner/技術 principal 分權 | CH-08/18/20/39；原域 currentness/identity 欠據則 `AFFECTED_SOURCE_IMPACT_HOLD` |
| `INTENT r2` 原檔 SHA `bcc9740794980301` | 24 INT/60 DR 原義/NEG/Consumer、可追產品 FUO | CH-08/12/13/14/16/17/22；原域 currentness/identity 欠據則 `AFFECTED_SOURCE_IMPACT_HOLD` |
| `TECH r1` 原檔 SHA `677243ba0b840724` | Hermes pin、Native-first、Need/Occupant/License/NoFit/原 Host | CH-19/20/22/34；原域 currentness/identity 欠據則 `AFFECTED_SOURCE_IMPACT_HOLD` |
| `SPEC r2` 原檔 SHA `0c92a7384e555b63` | SPEC_MANDATORY_100% 與 NATIVE_APPLICABLE_ONLY 分立；POS/NEG 與 原 Reader | CH-39/40；原域 currentness/identity 欠據則 `AFFECTED_SOURCE_IMPACT_HOLD` |
| `H1 r2` 原檔 SHA `ba9b64ec19e5c7e9` | 50 CH 原名不可降級；本 W1 僅 13 主章 | CH-00..49；原域 currentness/identity 欠據則 `AFFECTED_SOURCE_IMPACT_HOLD` |
| `METHOD r4` 原檔 SHA `c8cf1087255ebd81` | U0物理/U1子義/U2Join/U3差額/U4雙向語義；非已執行 | CH-05/06/07/40；原域 currentness/identity 欠據則 `AFFECTED_SOURCE_IMPACT_HOLD` |
| `UPPER Native-first` 原檔 SHA `e2d462c591aabd64` | 原 FHS 三庫、單機單人、適中阻力/Native 原功能 | CH-08/17/18/20；原域 currentness/identity 欠據則 `AFFECTED_SOURCE_IMPACT_HOLD` |
| `ROLE catalog` 原檔 SHA `0b0e1fde1568d394` | 角色是分析職能不是 Native principal | CH-08/39；原域 currentness/identity 欠據則 `AFFECTED_SOURCE_IMPACT_HOLD` |

**兩條不同合格線**（SPEC r2）：`SPEC_MANDATORY_100%` 是來源義務、原身份、Parent/NEG/原 Consumer 的全量**設計處置或具名 HOLD**，不因來源未涉及 W1 就丟失；`NATIVE_APPLICABLE_ONLY` 只對真正觸發的 Kind/Mode/Host/Effect 小範圍要求原 Host／原 Checker Raw。未獲 31 冊 Original Owner 核簽時，只能稱 `AUTHOR_SOURCE_SELECTION_WITH_HOLDS`，不得稱 `SPEC_MANDATORY_100%_RATIFIED`。原單人 Owner 不是 Maker/Issuer/Checker 同一技術 Principal。

### R5-01｜兩個 P0 真修補與現行一值

- `F01`: 原 SBL `integrations/pipd/src/pipd_ls_sp/registry.py::SOURCE_ORDER` 第 19 family **是 `ExecutionBindingRef`**，不是 `ExecutionBinding`。本稿 Product→PIPD 節的單一 ordered 19 exact-set 為唯一正文清單；本章 19 family 僅向其引用。刪末項、換成 ExecutionBinding、增加第 14 個 CLI 或錯誤重排 → `PIPD_REGISTRY_EXACT_SET_NACK`。原 CLI/Registry 遠端 Source Readback ≠ Windows Installed/Loaded。
- `F02`: r5 只交**兩份 UTF-8/LF MD＋一個 ZIP**，先 `R5_TWO_MD_SHA_PAIR_VERIFIED`，再 `R5_ZIP_CRC_AND_MEMBER_SHA_VERIFIED`，不得以歷史 r2 的 `7 MD + manifest` 或舊 ZIP 作現行驗收。ZIP 不可讀時維持 `ZIP_READBACK_NOT_OBSERVED`，不阻合法 SOURCE_READ／isolated LOCAL_DRAFT。
- r5 設計來源 L0/L1/L2/W0 **仍為 r4**；凡內文的 `L1-r4`、`L2-r4` 是上位真行號，不是本波舊現行規則。原 Registry `GENIEProjectionRef` 與 `ExecutionBindingRef` 分別 seam-only 限界，原 `$id/schema_version` 由 installed Registry/Reader 再核，文件不自造。

### R5-02｜精確受影全集的選取函數、雙向反查與非靜默 HOLD

定義 `AffectedSelection(original_source_clause_or_SourceSHA, OriginalID_or_HOLD, Parent/NEG_scope, applicable Need/Kind/Mode/Host/Effect, L2 DesignID, CH/WP owner)`，先以 L2-r4 的 **24 張 W1 obligation** 作強制輸入而非以 166 筆示例作分母。每筆分別回：`W1_INCLUDED_WITH_ORIGINAL_READER_HOLD`、`OTHER_WAVE_WITH_ORIGINAL_RECEIVER`、`ORIG_OWNER_HOLD`；不允許 `UNEXPLAINED_ORIGINAL_SOURCE`。同一 DesignID 的複合詞與 scope 逐子拆解；正向 Source→CH/WP/Case、反向 CH/WP/Case→SourceSHA/OriginalOwner 不可漏，附錄的 31 源使用 `count=0→OWNER_SELECTION_HOLD` 而非錯判無 W1 影響。對同一 Subject/CandidateSHA/SourceManifestSHA/Scope/Host/PolicyEpoch 做 Join；READ-only 可以沒有 Candidate，受護世界效果不得缺必要欄。

- **原域語義未被偽裝成 PASS**：r2 歷史 166 SCL 源行僅 18/31 來源；112 個 `ORIGINAL_ID_READER_HOLD` 與 48 個 `ORIGINAL_PARENT_NEG_HOLD` 保留。附錄把 166 行的實際原文字節／父標頭／明示 NEG 與未核作用域一併嵌入兩 MD 交付集合，但它仍是**作者端可重算證據，不是原 Domain semantic signer**。
- **原 Reader 必須做的核定**：原 RequirementID/Parent/Clause 版本當期有效、否定與例外完整、原 Consumer 型別與同 Scope ACK、Original Oracle/Runner 的適用性。欠一者該 source/card `AFFECTED_SEMANTIC_HOLD` 或 `SOURCE_CONTEXT_FRAGMENT_OWNER_HOLD`；未受影 READ/DRAFT 保留合法前進。

### R5-03｜三種 W1 交付狀態，不與 Original Effective 混權

| 層級 | 產出 Actor/Receiver | 需有的證據 | 禁止宣告 |
|---|---|---|---|
| `W1_BLUEPRINT_AUTHOR_ACCEPTED_WITH_AFFECTED_HOLDS` | W1 WaveCurator → DraftMaker | 2 MD/ZIP 真讀回＋24 卡逐子義＋50 CH/22-36＋具名 Source/Receiver HOLD | 31 源 Original Owner 全部 ratified |
| `W1_AUTHOR_FINAL_SCOPED_WITH_AFFECTED_HOLDS` | W1 DraftMaker→作者端 DesignCurator | 每個 CH/WP/Case/Asset 的草案差額與明確 LastGood/FirstFail；未核原域繼續 HOLD | 把作者定案當已生效原 PI/PD/HGK |
| `ORIGINAL_DOMAIN_EFFECTIVE` | 原 Canonical Writer/Reader/Owner（按 Subject/Scope） | 原 installed Reader 同 version/SHA、真 ACK/Effect Permit、需要時獨立 checker | 靠 GPT、CI 或 ZIP 檔案簽發 Permission |

此區分不使所有相異 Host/受護 Effect 的門檻移到無效的一般 SOURCE_READ 任務；進入真正 W2 Native world effect 仍需各受影前置原權責。

### R5-04｜五級 FUO 的實際 Receiver 與可宣稱範圍

| FUO 層 | 真 Consumer | 接收輸出 | 本輪證據上限 |
|---|---|---|---|
| `W1_DOC_FUO` | W1 DraftMaker | 本版可定位的三 SPEC/PI/PD/ECP/TQAEP **設計**契約、24 子義全集、HOLD | 作者端可用；不等同原 Reader ACK |
| `W1_ORIGINAL_READER_FUO` | SBL-hosted PIPD、Fabric/HGK 原 Consumer | 原 installed CLI/Registry/PLAN/Policy/Repo Reader 同 Scope ACK/NACK | `EXPECTED_NOT_OBSERVED`；僅設計下一步 |
| `W2_NATIVE_WORLD_FUO` | HGK WorldReader／原產品 Host | admissible DEV/OPS 的真 WorldRaw／journal cursor/recovery | `NOT_RUN`；W2 原 WP06/08/09/18 |
| `W3_NORMAL_MODE_FUO` | Hermes ordinary-goal Host/使用者 | fresh PID、預設 profile 自動選 Lane、真正可取用結果 | `NOT_RUN`；W3 W18 |
| `W4_RELEASE_FUO` | 原 Publisher/End User | GHP-02／適用獨立 Checker／Release 或 Retire readback | `NOT_GRANTED`；W4 |

### R5-05｜SOP 修補保真界線

全版本採 `HIGH_RETENTION_INTEGRATE_COVER_REPLACE_NO_ARCHITECTURE_RESET`：保留 50 個不可降級 H1、13 主責、8 原 WP、原 22/36、S1–S5 與 24 AssetSlot 完整可查。任何 r4 中仍出現的 `r2` 操作性語句只算歷史來源候選；r5 的 source/Owner/Receiver/FirstFail/State 分類為當期唯一讀取路線。當期沒有原 Host grant、原 PIPD compiler 執行或獨立 Checker，原域必要欄仍按 effect/Scope 局部 HOLD。

## W1-r5｜使用入口、法位與本次產品成果

這是 **`FHS_PKG_WAVE_001` 的唯一 L3 W1「藍圖＆skeleton」作者端設計正文**；不等於後續 `W1_草案` 或 `W1_定案`，也不等於 original PIPD Compiler Writer 的 Canonical PI/PD/ECP/TQAEP、原 HGK Issuer/Permit、Host Loaded、Protected Checker 或 Publisher Release。採《SBL&FHS-MSC → FHS》R2.0 Native-first 為設計母本，`L0→L1→L2→W0` **r4 真正來源 SHA** 為可驗血緣；各原 Domain Effective Reader/Writer 永不因本文件改變。此包使用 `$sbl-tpm-sp` 的 TPM Product/System/Program、PIPD 八階段契約及交接**規劃能力**，未冒充其原始 Compiler 執行。

**單人 Owner 第一有效成果（FUO）**：在 W0 交來三份彼此不同、source-bound 的 Product／Architecture／Program SPECDraft 及 31 冊 SourceSnapshot 後，W1 可把普通 Goal 分解成可由原 SBL-hosted PIPD／Fabric／HGK／Hermes／Host Reader 接收的 `Intent→Authority/Profile→strict PI→真正 RepoContext late-bound PD→effect-specific ECP→TQAEP 期待/具名 HOLD`；必要的 Host Capability 逐個分辨 `SELECTED→INSTALLED→LOADED→INVOKED→CONSUMER_USED`。本次交付的 FUO 是**可由下一階段 DraftMaker 使用的設計契約與可定位受影差額**，非已完成 Native 有用結果。

**非目標**：不執行原 PIPD、Host installer、受保護 Native effect 或獨立 Checker；不重啟已停用的 Commander 插件；不建立第二 Policy／Issuer／WorkID／Queue／Compiler／Case Registry／Publisher；不要求 SOURCE_READ／授權隔離 LOCAL_DRAFT 過產品發行完整門檻；不默升 Hermes v0.22.5；不把舊 W1-W4 r2 ZIP 擅升為當期規範；不把 949/149/50 Parent/39/96/192/282 分母縮寫成新 24 卡。

**版本衝突優先序**：Original Domain Effective Canonical/Reader（當期 Subject+Scope）> L0 r4→L1 r4→L2 r4→W0 r4→本 W1 r5 作者端設計。舊 W1～W4 r2/史料、作者端審計附錄均不成第二 Normative。受影 Source/ABI 不明標具名 HOLD，未受影讀取/草稿允許續工。

## W1-r5｜角色、產品規格與三庫工程入口

- **按需分析角色**：FHS-R00（總架構）、R04／R05（原來源與權威）、R06／R07（SBL/TPM Product）、R08／R09（PIPD PI/PD）、R10／R11（Fabric/HGK）、R12／R13（Hermes/Swarm）、R17／R19（安全／選型）、R27／R28（交付及三庫）；角色是分析職能，不是 OS SID、Issuer 或 Checker Principal。
- **Product SPEC**（原 W0 PM）→ PIPD Intake Consumer：Persona／7 Pain／JTBD／可觀測 FUO／MVP／非目標／OriginalID／POS 與 NEG；負例：把 3 個文件數量或表列 Done 當使用者成果。
- **Architecture SPEC**（原 W0 SE）→ Original Repo/ABI/Fabric/HGK Consumer：ADR／Single Writer／Source+Version／Exact Effect+ACL／5 Seam／三 Lane／Host/Provider；負例：新設 Shadow Issuer 或未 Probe 的 Host schema id。
- **Program SPEC**（原 W0 TPgM）→ 原 Program/WorkID Reader：22 WP／36 原向 DAG、Hard/Soft 按 Operation 分流、唯一 WriteSet、FirstFail／Stop／Resume／Rollback、受影 Case；負例：WP17 倒依賴 WP06。
- **Fabric-first 唯讀導航**：`Fabric/INTEGRATION/FHS/README.md`→`repository-map.json`，再依 FHS-NAV/v2 讀 `SBL/integrations/pipd/` 與 `HG-KSEOS` 原 Registry/Reader。Mirror 的 `effect_permission=NONE`；GitHub `main` SHA 是遠端事實不是 Windows local RepoContext。三庫工程更新各自 branch→PR，決不由作者文件寫 main。

〔R1-2026-11-06 更正〕本段「當期遠端 main」為 2026-11-05 讀值，2026-11-06 實測已變更：Fabric `ef4fe187e706bb309a905c2f88c7477b53cf5839`（main commit 2026-11-05T19:12:36Z）、SBL `8f5161a306d46775b71ff2bc7817e447cfd8f96e`（2026-11-06T07:38:56Z）、HG-KSEOS `a7046a36956e2179d7125449ce9b6f05fa5451cf`（2026-11-05T16:10:55Z）。原文三個 SHA 保留為當時讀值，不回寫。本機 clone HEAD（SBL `826ca066`、Fabric `765df628`、HGK `6c9fc733`）仍非 main 且 dirty；remote SHA 與本機 RepoContext 分立之規則不變。；SBL `004e88913d5c1fb57e09e8d2bf744ef1547fecbc`；HG-KSEOS `0143b50331f7fef007a5921bb743e61f59b0a7bd`。上述 SHA 屬 GitHub read-only，不跨 repo 借用 Writer 權威。

## W1-r5｜Product→PIPD：原 Writer 13 CLI／19 Families／8 Skills exact-set

**原 Canonical 入口**：`SBL/integrations/pipd/src/pipd_ls_sp/cli.py`（原 `COMMANDS`）、`registry.py`（原 `SOURCE_ORDER`）與原 `docs/pipd-migration/U04-CUTOVER.md`。需要原 installed Reader/CLI 版本、`help/doctor` Raw 才可稱實機 13/19 回讀；本文件的列舉是設計/遠端來源讀取。

- **13 CLI**：`init`／`intake`／`profile`／`compile-pi`／`bind-pd`／`compile-ecp`／`compile-tqaep`／`validate`／`doctor`／`project`／`export`／`diff`／`repair`；不能無原 CLI 修訂就新增 `compile-cc` 第 14 個 verb。
- **19 Contract Families**：`ArtifactIdentity`、`AuthorityBinding`、`RequirementAtom`、`ProfileBinding`、`TechnologyAdmission`、`PI-PKG`、`PD-PKG`、`TraceLink`、`TaskSpecSeed`、`ConstructionContract`、`WorkOrderCandidate`、`ECP`、`TQAEP`、`ExecutionHandoff`、`EvidenceExpectation`、`ClaimCeiling`、`SurfaceProjectionManifest`、`GENIEProjectionRef`、`ExecutionBindingRef`。逐 `$id/schema/version` 以原 Registry 為準；未知為 `ORIGINAL_SCHEMA_ID_UNBOUND`。
- **8 Skills**：`pipd-route-intake`、`pipd-authority-source`、`pipd-profile-tailor`、`pipd-pi-compile`、`pipd-pd-bind`、`pipd-execution-contract`、`pipd-assurance-tqaep`、`pipd-package-project`；`$sbl-tpm-sp` 是作者端規劃工具，無權代 original PIPD Write。

**逐階具名契約（設計，不是已產正式物件）**：

1. Intake：nonblank Goal＋contained OriginalSourceLocator → `IntentCard` 候選。NEG blank／path traversal／zero source；`INTAKE_SOURCE_NACK`。
2. Authority：逐 family file digest＋locator＋OriginalOwner/Currentness/Conflict；衝突不准偽造 `SourceFreezeManifest`；`SOURCE_AUTHORITY_CONFLICT_HOLD`。
3. Profile：LITE/STANDARD/ASSURED、九軸 veto 只能增加 artifact depth，不能降 Security/NEG/Consumer；`PROFILE_SAFETY_VETO_NACK`。
4. PI：由原 pinned Writer 用原 RequirementAtom/OriginalID/SourceSpan/Parent/POS/NEG/Oracle/FUO 編譯；`SBL.PI.Crosswalk@2` 放 Sidecar，不能污染 strict schema；未執行則 `ORIGINAL_PI_COMPILE_NOT_RUN`。
5. PD：PI 綁 **真 local** Git root/HEAD/branch/dirty/index/untracked/preimage/ACL/ExactWriteSet/Scope；GitHub 遠端 HEAD 不充本地 RepoContext；`PD_REPOCONTEXT_UNBOUND`。
6. ECP：原 Operation Registry 決定 `SOURCE_READ, LOCAL_DRAFT_WRITE, DEV_REPO_WRITE, HOST_OPS, USER_EFFECT, RELEASE_EFFECT`，特定 Pre/Post、idempotency、UNKNOWN reconcile、rollback；ECP 意圖不能當原 Issuer Permit；`ORIGINAL_ECP_EFFECT_HOLD`。
7. TQAEP：原 Case/Oracle/Runner per-OriginalID 配 POS/NEG/SEC/EDGE、Raw/Host/Scope，Maker 不簽 Checker，無 Original Runner=`RUNNER_UNBOUND`。
8. Package：ClaimCeiling/EvidenceExpectation/TraceClosure 在原 Reader 驗完真 Body/joins 後封作者候選，不等同 Host/Independent/Release；`PACKAGE_TRACE_CLOSURE_HOLD`。

**W0→W1**：W0 獨立三 SPECDraft（各有 SHA、Role、Original Sources）、QuestionLedger 和原 Source Reader 的缺件狀態；三 SPEC 同文或誤宣 W0 skeleton 已正式 PI → `W0_SPEC_ROLE_OR_SHA_NACK`。**W1→W2**：同 Subject/Candidate/Scope/SourceManifestSHA、原 PI/PD/Effect ECP/TQAEP 各層 Reader/NACK、原 Policy/Host Capability 受影負例；缺真 ACK 才阻該 effect。

## W1-r5｜24 張當期 L2 Design Obligation（不替代 84 張總卡或原 RequirementID）

每列保留 L2 r4 §2.5 **當期原條文**中的 `DesignID / L1-r4 locator / CH / WP / 原 Producer-Consumer / POS / NEG / 最小證據與 HOLD / L3 目標`，供 W1 DraftMaker 分子義。`WP01/10/13/16/00` 若在 L2 obligation 卡出現是**受影跨波引用**，原 WP 主責仍依 L2 §4.1，W1 不搶 WriteSet。靜態行引用不等於 U0–U4 Owner ratification。

| DesignID＋L1 r4 行 | 原要求／獨立 CH | 原主波與受影 WP／效果 | 原 Producer→Consumer | POS | NEG／FirstFail | 受影義務／HOLD | L3 目標 |
|---|---|---|---|---|---|---|---|
| `INT-05` `L1-r4:L773` | 一個 HGK 控制平面；沿用 HGK 原 WorkID/Issuer/CAS/SharedSpine/World；[CH-18](#ch-18) | **W1**／`WP-FHS-03`／HOST_OPS/DEV 依受影 Operation | HGK Original Issuer/SharedSpine/Protected Checker Reader | 沿用 HGK 原 WorkID/Issuer/CAS/SharedSpine/World | 生成第二 HGK Issuer／Queue／SharedSpine；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `INT-06` `L1-r4:L774` | 一個現役 PIPD Compiler Writer；SBL integrations/pipd 13 CLI／19 families／8 skills，薄 Adapter；[CH-12](#ch-12)/[CH-13](#ch-13) | **W1**／`WP-FHS-05`／HOST_OPS/DEV 依受影 Operation | SBL-hosted PIPD canonical Compiler/Original Source/Repo/Case Reader | SBL integrations/pipd 13 CLI／19 families／8 skills，薄 Adapter | 將歷史 PIPD-LS-SP 當現役唯一 Writer，或技能自行簽 PI；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `INT-07` `L1-r4:L775` | 低阻力優先既有輪子；Hermes Direct/Delegation/Kanban/Swarm 按複雜度選擇，NoFit 才補；[CH-20](#ch-20)/[CH-23](#ch-23)/[CH-47](#ch-47) | **W1**／`WP-FHS-04`／HOST_OPS/DEV 依受影 Operation | Hermes original Runtime/Launcher/Provider Raw Reader → HGK Lane/Journal Consumer、Original Tech/License/Host/Method Owner → Capability Consumer | Hermes Direct/Delegation/Kanban/Swarm 按複雜度選擇，NoFit 才補 | 沒查現有 Hermes 能力便重造 Scheduler/Router；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `INT-13` `L1-r4:L781` | PIPD PI/PD/ECP/TQAEP 分層；PI source-bound，PD 晚綁 Repo，ECP 非 Admission，TQAEP 依 Original Oracle；[CH-12](#ch-12)/[CH-13](#ch-13)/[CH-14](#ch-14)/[CH-15](#ch-15)/[CH-41](#ch-41) | **W1**／`WP-FHS-05`／HOST_OPS/DEV 依受影 Operation | SBL RepoContext/PD Reader → HGK Original Issuer → Repo World Reader、SBL-hosted PIPD canonical Compiler/Original Source/Repo/Case Reader；原末端 Receiver＝`INT-13_CONSUMER_LOCATOR_SOURCE_TRUNCATION_HOLD`（L1/L2 源列被截斷，非已綁定） | PI source-bound，PD 晚綁 Repo，ECP 非 Admission，TQAEP 依 Original Oracle | ECP intent 冒 Issuer Permit；PD 未 live RepoContext 即號稱已綁；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `INT-14` `L1-r4:L782` | 四 Host 正交可用；各 Host 按本地能力與 Loader 獨立 Install/Invoke/Uninstall；[CH-09](#ch-09)/[CH-21](#ch-21)/[CH-29](#ch-29) | **W1**／`WP-FHS-11`／HOST_OPS/DEV 依受影 Operation | SBL Product/Kind/Host Original Consumer、SBL Product Owner → CLI Host Consumer、SBL Product Owner → Original Skill/Agent Host Registry Consumer；原末端 Host Receiver = INT-14_HOST_RECEIVER_SOURCE_TRUNCATION_HOLD（原 L1/L2 消費端截斷） | 各 Host 按本地能力與 Loader 獨立 Install/Invoke/Uninstall | 一個 Host 的 CLI PASS 當四 Host Skill/Agent 都已 Qualify；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `INT-24` `L1-r4:L792` | OpenSpec/gstack 是方法而非再一套法定流程；OpenSpec proposal/validate；gstack review/QA 轉原 Consumer；[CH-47](#ch-47) | W1_DESIGN_SELECTOR；OriginalPrimary=`WP-FHS-16/W0`；NO_WRITESET_TRANSFER | Original Tech/License/Host/Method Owner → Capability Consumer | OpenSpec proposal/validate；gstack review/QA 轉原 Consumer | OpenSpec/gstack 自發 Canonical PI/Independent Verdict/Publisher Release；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `FHS-DR-007` `L1-r4:L804` | 產品／A；四 Host 各有獨立 Loader/Capabilities/NEG；Hermes/Codex/Claude/ChatGPT 原 Host 原 Process/Tool 查 readback；[CH-09](#ch-09)/[CH-21](#ch-21) | **W1**／`WP-FHS-11`／HOST_OPS/DEV 依受影 Operation | SBL Product/Kind/Host Original Consumer | 不同 Host 的實際 Trigger/Uninstall | 把在 ChatGPT 生成草稿稱 Windows 已完成；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `FHS-DR-008` `L1-r4:L805` | 產品／A；三 SP 均保留 Portable/Native 對照而不混權限；TPM/Commander/Challenge 各自讀合法原 Consumer；[CH-08](#ch-08)/[CH-11](#ch-11)/[CH-34](#ch-34) | **W1**／`WP-FHS-07`／HOST_OPS/DEV 依受影 Operation | SBL Product/Kind/Host Original Consumer | 同 WorkID/Source/Case 的適用讀回 | 任一 Portable Skill 自行發 Grant/Checker；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `FHS-DR-023` `L1-r4:L820` | PIPD/TPM／A；SourceFreeze 由原 PIPD/Source Reader 綁定；source family sha/locator/authority/conflict；[CH-13](#ch-13) | **W1**／`WP-FHS-01`／HOST_OPS/DEV 依受影 Operation | SBL-hosted PIPD canonical Compiler/Original Source/Repo/Case Reader | 不合格來源受影 HOLD | 用 MD metadata 的 approved 字樣繞 Reader；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `FHS-DR-024` `L1-r4:L821` | PIPD/TPM／A；PI 保留 OriginalID/ClauseSHA/Parent/POS/NEG/Oracle/FUO；由 SBL integrations/pipd 正式 Writer 編譯；[CH-13](#ch-13) | **W1**／`WP-FHS-05`／HOST_OPS/DEV 依受影 Operation | SBL-hosted PIPD canonical Compiler/Original Source/Repo/Case Reader | 原 PIPD Reader 實收／錯誤有型別 | GPT 生成 JSON 假裝正式 PI；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `FHS-DR-025` `L1-r4:L822` | PIPD/TPM／A/W0-B；PD 是來源穩定 PI 對真 RepoContext 的 late binding；Repo HEAD/index/untracked/Preimage/WriteSet 與 Scope；[CH-14](#ch-14) | **W1**／`WP-FHS-05`／HOST_OPS/DEV 依受影 Operation | SBL-hosted PIPD canonical Compiler/Original Source/Repo/Case Reader | Repo drift 只重綁受影部分 | 未知 Repo 強行出有權 PD；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `FHS-DR-026` `L1-r4:L823` | PIPD/TPM／A/W0-B；DEV/OPS/USER 等 Effect-specific ECP 不可充 Permit；ConstructionContract/ECP 計畫／受權 Gateway 分離；[CH-15](#ch-15) | **W1**／`WP-FHS-05`／HOST_OPS/DEV 依受影 Operation | SBL-hosted PIPD canonical Compiler/Original Source/Repo/Case Reader | 有界許可後讀真 World/Repo | 無 Effect Authorization 自行 Apply；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `FHS-DR-027` `L1-r4:L824` | PIPD/TPM／A；TQAEP/19 Schema/13 CLI/8 Skill 原 ABI 不私改；以實際 Canonical Pipeline 與 installed Reader 判斷；[CH-12](#ch-12)/[CH-41](#ch-41) | **W1**／`WP-FHS-05`／HOST_OPS/DEV 依受影 Operation | SBL-hosted PIPD canonical Compiler/Original Source/Repo/Case Reader | Case 有正負例和待原 Checker 收據 | 不核 ABI 就加 compile-cc 14th verb；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `FHS-DR-028` `L1-r4:L825` | PIPD/TPM／A；B1 PI27→PD31 是分裂映射，不能一比一湊數；逐 31 edge 保留來源與適用 Effect；[CH-33](#ch-33) | **W1**／`WP-FHS-10`／HOST_OPS/DEV 依受影 Operation | SBL-hosted PIPD canonical Compiler/Original Source/Repo/Case Reader | 原 Reader 能追每條細分 PD | 只記 27 PI ID 便宣稱全 PD 完成；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `FHS-DR-029` `L1-r4:L826` | 治理／A＋B；Fabric FHS-NAV/v2 是唯一跨庫導航入口且唯讀；先 Fabric FHS README/map，再 SBL/HGK 原域 Reader；[CH-17](#ch-17) | **W1**／`WP-FHS-00`／HOST_OPS/DEV 依受影 Operation | Fabric FHS Navigation/Policy/FAR Reader → Original Consumer | 三庫各自 bounded PR/source fact | 導航 metadata 被當授權來源；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `FHS-DR-030` `L1-r4:L827` | 治理／A＋B；Fabric Policy/FAR 原 Reader/Consumer 可實際回讀；PolicyEpoch/RequiredSet/Producer/Original R8 Consumer ACK；[CH-17](#ch-17)/[CH-40](#ch-40) | **W1**／`WP-FHS-02`／HOST_OPS/DEV 依受影 Operation | Fabric FHS Navigation/Policy/FAR Reader → Original Consumer | R8 真 ACK 不被研究文件代替 | 工具回應被視為 Policy Applied；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `FHS-DR-031` `L1-r4:L828` | 治理／B/PROTECTED；HGK 是唯一 Work/Issuer/SharedSpine/World 權威；原 WorkID/Scope/TTL/Nonce/CAS 與有效 OS ACL；[CH-18](#ch-18) | **W1**／`WP-FHS-03`／HOST_OPS/DEV 依受影 Operation | HGK Original Issuer/SharedSpine/Protected Checker Reader | 真原 Issuer admission + world state | Human Owner 只有一人→普通 Agent 有 admin Token；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `FHS-DR-032` `L1-r4:L829` | 治理／B/PROTECTED；不同技術 Principal 不能被 GPT persona 假造；runtime user SID 與維護 Token 實際隔離；[CH-18](#ch-18)/[CH-39](#ch-39) | **W1**／`WP-FHS-03`／HOST_OPS/DEV 依受影 Operation | HGK Original Issuer/SharedSpine/Protected Checker Reader | 直接修改 HGK 的一般 Profile 被拒 | 兩個 Hermes Profile 名稱即宣稱 OS 隔離；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `FHS-DR-034` `L1-r4:L831` | 治理／A；三庫更改各自 branch→PR/verified original HEAD；不可跨 Repo 一個隱形 Commit；[CH-14](#ch-14)/[CH-44](#ch-44) | **W1**／`WP-FHS-00`／HOST_OPS/DEV 依受影 Operation | Original Domain Owner/Reader (scope binding pending) | 相應 PR 有真變更與可回退提交 | 憑本檔直接覆寫 main/force push；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `FHS-DR-035` `L1-r4:L832` | Runtime／B/LONG；Hermes v0.22.5 原能力優先使用；Direct→Delegate→Kanban→Swarm 依複雜度決定；[CH-19](#ch-19)/[CH-20](#ch-20) | **W1**／`WP-FHS-04`／HOST_OPS/DEV 依受影 Operation | Original Domain Owner/Reader (scope binding pending) | 真 task result 有再續工 | 簡單 Read 任務硬套多 Agent Queue；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `FHS-DR-036` `L1-r4:L833` | Runtime／A＋B；3 正式 Lane 的模型 RequiredSet/Served 分開；PLAN/EXECUTE/VERIFY_SECURITY 受原有效 Policy 選模；[CH-19](#ch-19) | **W1**／`WP-FHS-04`／HOST_OPS/DEV 依受影 Operation | Hermes original Runtime/Launcher/Provider Raw Reader → HGK Lane/Journal Consumer | 同 Subject 每 Lane 真 Request/Served/Usage | 只選到 Picker 便宣稱 Protected Lane Served；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `FHS-DR-042` `L1-r4:L839` | 工具／A＋B；Need→Existing Capability→Occupant→Loaded/Used→Consumer；OriginalDisposition/License/Pin/NoFit/Backout 各槽；[CH-22](#ch-22)/[CH-23](#ch-23)/[CH-47](#ch-47) | **W1**／`WP-FHS-13`／HOST_OPS/DEV 依受影 Operation | Original Tech/License/Host/Method Owner → Capability Consumer | 需求由已合格工具解決 | 用外部宣傳文即自稱 loaded；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `FHS-DR-043` `L1-r4:L840` | 工具／B/SPEC；OpenSpec 只作 Brownfield SpecDelta/Proposal/Validate 方法；避免第二 PIPD compiler/strict $id；[CH-47](#ch-47) | W1_DESIGN_SELECTOR；OriginalPrimary=`WP-FHS-16/W0`；NO_WRITESET_TRANSFER | Original Tech/License/Host/Method Owner → Capability Consumer | 規格差額轉原 SBL/PIPD Reader | OpenSpec archive 即原 Owner Ratified；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |
| `FHS-DR-044` `L1-r4:L841` | 工具／B/VERIFY；gstack Review/QA/Investigate 只作可追 advisory；Windows minimal support 認清，Host probe first；[CH-31](#ch-31)/[CH-47](#ch-47) | W1_DESIGN_SELECTOR；OriginalPrimary=`WP-FHS-16/W0`；NO_WRITESET_TRANSFER | Original Tech/License/Host/Method Owner → Capability Consumer | 原 Runner 能重現 QA Finding | gstack /ship 被當原 Publisher / Independent；`DESIGN_OBLIGATION_MISSING`（若失卡） | MANDATORY_SPEC；設計引用/隔離 draft 可產；需真受影 Effect 才核原 Host/Reader/Checker；`ORIGINAL_READER_ACK_PENDING` | `W1_藍圖&skeleton→草案→定案` |

## W1-r5｜24 個上位 DesignID 的複合子義、專屬業務拒收與 Original Reader Join（F04–F07）

**本表的 24 個 DesignID 確實屬 L2 r4 W1 選入全集；每個 `S-W1-*` 是本版作者拆出的子要求，而不是原 Native/PIPD RequirementID。** 行中 L1-r4 sha256 為原 L1 整行位元組（非原來源 31 冊 ClauseSHA）；`ORIGINAL_REQUIREMENT_ID / ORIGINAL_ORACLE_ID / ORIGINAL_RAW_SCHEMA_ID` 未經原 Reader 證實仍 HOLD。跨波 `WP00/01/10/13/16` 出現時只讀，不奪其原主波 WriteSet；本表的 WP 欄是受影 W1 Consumer 路由，不更動 L2 22 WP 主責。

| Author Subclaim（含 DesignID／L1 行 SHA prefix） | 可逐義驗證的原句 Predicate/觸發範圍 | 受影 WP/Effect / Original Consumer | POS（期望） | 專屬業務 NEG（不得） | Author Case/專屬 FirstFail | 原身分/Oracle/Raw/閉包 |
|---|---|---|---|---|---|---|
| `S-W1-INT-05-01` / `L1-r4:L773@b9cfb86c4154c1e3` | 全系統只有原 HGK Issuer 有權建立 WorkID/Permit；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-03` / `HOST_OPS`；HGK original Issuer/SharedSpine Reader | 相同原 WorkID+Issuer ACK 可讀 | 新影子 Issuer 自簽 Permit | `AUTHOR.W1.INT-05.01.NEG` → `SHADOW_ISSUER_DENY` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Original WorkID/Issuer/SharedSpine Raw` / 原 Schema HOLD |
| `S-W1-INT-05-02` / `L1-r4:L773@b9cfb86c4154c1e3` | 原 Journal/Queue/CAS 與 SharedSpine 唯一且可恢復；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-03` / `HOST_OPS`；HGK original Issuer/SharedSpine Reader | 相同 WorkID 游標跨重啟恢復 | 新 SQLite queue 取代原 SharedSpine | `AUTHOR.W1.INT-05.02.NEG` → `SHADOW_QUEUE_DENY` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Original WorkID/Issuer/SharedSpine Raw` / 原 Schema HOLD |
| `S-W1-INT-05-03` / `L1-r4:L773@b9cfb86c4154c1e3` | Protected Checker 與 Maker 不可共用獨立資格；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-03` / `SOURCE_READ`；HGK original Issuer/SharedSpine Reader | 同 Subject 不同 principal 原 Checker Raw | Maker 自核准 Protected PASS | `AUTHOR.W1.INT-05.03.NEG` → `SELF_ATTESTED_CHECKER_NACK` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Original WorkID/Issuer/SharedSpine Raw` / 原 Schema HOLD |
| `S-W1-INT-06-01` / `L1-r4:L774@867cb537a3eea1e3` | SBL integrations/pipd 是唯一 active Compiler；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `SOURCE_READ`；SBL-hosted PIPD Compiler and Source Registry | 原 CLI 命令/Registry 原核讀回 | 歷史 PIPD-LS-SP 重開第二 Writer | `AUTHOR.W1.INT-06.01.NEG` → `PIPD_SHADOW_WRITER_DENY` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `PIPD CLI/registry original Raw` / 原 Schema HOLD |
| `S-W1-INT-06-02` / `L1-r4:L774@867cb537a3eea1e3` | 13 CLI 原命令順序不可擅改；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `SOURCE_READ`；SBL-hosted PIPD Compiler and Source Registry | 13 個原 help verbs 按序一致 | 新增 compile-cc | `AUTHOR.W1.INT-06.02.NEG` → `PIPD_CLI_EXACT_SET_NACK` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `PIPD CLI/registry original Raw` / 原 Schema HOLD |
| `S-W1-INT-06-03` / `L1-r4:L774@867cb537a3eea1e3` | 19 family 及 8 Skill 分別核 exact identity；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `SOURCE_READ`；SBL-hosted PIPD Compiler and Source Registry | 原 Registry 第19項 ExecutionBindingRef | 以 ExecutionBinding 取代該 family | `AUTHOR.W1.INT-06.03.NEG` → `PIPD_REGISTRY_EXACT_SET_NACK` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `PIPD CLI/registry original Raw` / 原 Schema HOLD |
| `S-W1-INT-07-01` / `L1-r4:L775@878822684bdce98c` | Direct→Delegation→Kanban→Swarm 按任務選最低足夠方法；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-04` / `SOURCE_READ`；Hermes original Runtime/Owner and Tech Owner | 普通來源讀取沿用 Direct | 簡單任務先造第二 swarm scheduler | `AUTHOR.W1.INT-07.01.NEG` → `SHADOW_SCHEDULER_OR_OVERENGINEER_NACK` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Hermes capability/Need fit Raw` / 原 Schema HOLD |
| `S-W1-INT-07-02` / `L1-r4:L775@878822684bdce98c` | 現役 capability 足夠時優先復用；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-04` / `SOURCE_READ`；Hermes original Runtime/Owner and Tech Owner | 原 Host capability 正例與 Consumer 相符 | 未 probe 原能力即採新輪子 | `AUTHOR.W1.INT-07.02.NEG` → `NATIVE_CAPABILITY_PROBE_MISSING` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Hermes capability/Need fit Raw` / 原 Schema HOLD |
| `S-W1-INT-07-03` / `L1-r4:L775@878822684bdce98c` | NoFit 才向原技術 Owner 提替代案；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-04` / `HOST_OPS`；Hermes original Runtime/Owner and Tech Owner | 原 NoFit/License/rollback 具名 | 以研究字串直接宣外部 loader qualified | `AUTHOR.W1.INT-07.03.NEG` → `TECH_NOFIT_OR_LOAD_HOLD` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Hermes capability/Need fit Raw` / 原 Schema HOLD |
| `S-W1-INT-13-01` / `L1-r4:L781@e76e6876b02db8da` | PI 綁 Original Source／Parent／NEG／OriginalID；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `LOCAL_DRAFT_WRITE`；SBL-hosted PIPD Reader; missing original final receiver HOLD | 原 Compiler 確認非空 strict PI | 用 GPT 產 JSON 冒 Canonical PI | `AUTHOR.W1.INT-13.01.NEG` → `PIPD_STRICT_PI_WRITER_NACK` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Original PIPD PI/PD/ECP/TQAEP reader Raw` / 原 Schema HOLD |
| `S-W1-INT-13-02` / `L1-r4:L781@e76e6876b02db8da` | PD 僅綁同 Scope 真 local RepoContext；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `DEV_REPO_WRITE`；SBL-hosted PIPD Reader; missing original final receiver HOLD | 本地 HEAD/index/untracked/preimage 俱全 | remote GitHub HEAD 充 local probe | `AUTHOR.W1.INT-13.02.NEG` → `PD_REPOCONTEXT_UNBOUND` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Original PIPD PI/PD/ECP/TQAEP reader Raw` / 原 Schema HOLD |
| `S-W1-INT-13-03` / `L1-r4:L781@e76e6876b02db8da` | ECP intention≠Issuer Permit；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `HOST_OPS`；SBL-hosted PIPD Reader; missing original final receiver HOLD | 原 HGK admission 出具同 scope nonce/epoch | 直接以 ECP intention 做世界效果 | `AUTHOR.W1.INT-13.03.NEG` → `ECP_NOT_ISSUER_PERMIT` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Original PIPD PI/PD/ECP/TQAEP reader Raw` / 原 Schema HOLD |
| `S-W1-INT-13-04` / `L1-r4:L781@e76e6876b02db8da` | TQAEP 必連 Original Oracle/Runner/Checker；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `SOURCE_READ`；SBL-hosted PIPD Reader; missing original final receiver HOLD | 具名 Case 和原 Reader 對應 | Maker 自簽原 Checker verdict | `AUTHOR.W1.INT-13.04.NEG` → `SELF_ATTESTED_TQAEP_NACK` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Original PIPD PI/PD/ECP/TQAEP reader Raw` / 原 Schema HOLD |
| `S-W1-INT-13-05` / `L1-r4:L781@e76e6876b02db8da` | 原上游截斷的 Receiver 不得自行補名；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `SOURCE_READ`；SBL-hosted PIPD Reader; missing original final receiver HOLD | 原 Domain Reader 同 Subject ACK 才填端點 | 把 Original Domai 視為完整 Receiver | `AUTHOR.W1.INT-13.05.NEG` → `RECEIVER_IDENTITY_HOLD` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Original PIPD PI/PD/ECP/TQAEP reader Raw` / 原 Schema HOLD |
| `S-W1-INT-14-01` / `L1-r4:L782@1e75b0d56f4ae363` | 四 Host Hermes/Codex/Claude/ChatGPT 分別判能力與 Loader；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-11` / `HOST_OPS`；SBL original per-Host skill/CLI Reader | 各 Host 每個 SP 具自己的 trigger+nontrigger | Hermes pass 充 ChatGPT passed | `AUTHOR.W1.INT-14.01.NEG` → `HOST_EVIDENCE_FOREIGN_NACK` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Host install/load/invoke/remove Raw` / 原 Schema HOLD |
| `S-W1-INT-14-02` / `L1-r4:L782@1e75b0d56f4ae363` | Installed/Loaded/Invoked/Used/Removed 均不能混同；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-11` / `HOST_OPS`；SBL original per-Host skill/CLI Reader | 原 Process/PackSHA/Consumer Raw 全鏈 | 只有 ZIP 檔存在宣 ConsumerUsed | `AUTHOR.W1.INT-14.02.NEG` → `HOST_CONSUMER_RAW_MISSING` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Host install/load/invoke/remove Raw` / 原 Schema HOLD |
| `S-W1-INT-14-03` / `L1-r4:L782@1e75b0d56f4ae363` | 各 Host 不相容時保留 NoFit/owner decision；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-11` / `SOURCE_READ`；SBL original per-Host skill/CLI Reader | Host 原 Owner 解讀原功能限制 | 自行推定四 Host 相同安裝 API | `AUTHOR.W1.INT-14.03.NEG` → `HOST_LOADER_APPLICABILITY_HOLD` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Host install/load/invoke/remove Raw` / 原 Schema HOLD |
| `S-W1-INT-24-01` / `L1-r4:L792@1403a9f09bb60693` | OpenSpec proposal/validate 僅產 Brownfield SpecDelta；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-11` / `LOCAL_DRAFT_WRITE`；Original Method/Tech Owner; PIPD/Checker/Publisher Reader | 原 PIPD Reader 接收轉譯 proposal | OpenSpec archive 當正式 PI Writer ACK | `AUTHOR.W1.INT-24.01.NEG` → `OPENSPEC_CANONICAL_PROMOTION_NACK` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Advisory method result and original consumer Raw` / 原 Schema HOLD |
| `S-W1-INT-24-02` / `L1-r4:L792@1403a9f09bb60693` | gstack QA/review 只作 advisory；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-11` / `SOURCE_READ`；Original Method/Tech Owner; PIPD/Checker/Publisher Reader | 原 Case Runner 另重驗 QA finding | gstack /ship 當 Publisher receipt | `AUTHOR.W1.INT-24.02.NEG` → `GSTACK_PUBLISHER_NACK` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Advisory method result and original consumer Raw` / 原 Schema HOLD |
| `S-W1-INT-24-03` / `L1-r4:L792@1403a9f09bb60693` | Host license/version/pin 未核要受影 HOLD；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-11` / `SOURCE_READ`；Original Method/Tech Owner; PIPD/Checker/Publisher Reader | 原 Host asset/license readback 才選 | README 文句即視為已部署 | `AUTHOR.W1.INT-24.03.NEG` → `HOST_ASSET_PIN_HOLD` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Advisory method result and original consumer Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-007-01` / `L1-r4:L804@8e209f4c829274be` | 四 Host 的實際 install/load 功能分立；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-11` / `HOST_OPS`；SBL Product and each original Host Loader | 同 Host PackSHA/PID 的 Loaded Raw | 跨 Host 檔案共用即全通過 | `AUTHOR.W1.FHS-DR-007.01.NEG` → `HOST_EVIDENCE_FOREIGN_NACK` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Host-specific process/load/trigger Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-007-02` / `L1-r4:L804@8e209f4c829274be` | 四 Host 的 NEG trigger／uninstall/residue 各有；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-11` / `HOST_OPS`；SBL Product and each original Host Loader | 本 Host nontrigger 和 remove 可重放 | 只做安裝無反例／殘留檢查 | `AUTHOR.W1.FHS-DR-007.02.NEG` → `HOST_NONTRIGGER_UNVERIFIED` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Host-specific process/load/trigger Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-008-01` / `L1-r4:L805@46fae508903b584a` | TPM／Commander／Challenge 三 SP 各有 Portable 入口；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-11` / `HOST_OPS`；SBL Product Original Consumer and original Protected Checker | 3 個 Host Pack 身份獨立 | 把 TPM LoadedSHA 當 Challenge | `AUTHOR.W1.FHS-DR-008.01.NEG` → `SP_PACK_IDENTITY_COLLISION` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `3 SP portable/native split Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-008-02` / `L1-r4:L805@46fae508903b584a` | Portable Guide 不能簽 Native Permit/Checker；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-11` / `HOST_OPS`；SBL Product Original Consumer and original Protected Checker | 原 Native consumer 各有獨立 Ack | Portable Plugin 自簽 Checker | `AUTHOR.W1.FHS-DR-008.02.NEG` → `PORTABLE_NATIVE_AUTHORITY_CROSSING_DENY` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `3 SP portable/native split Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-023-01` / `L1-r4:L820@74140c6636d47df6` | 每 family 有原 byte SHA+至少一個 contained locator；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `SOURCE_READ`；Original PIPD Authority/Source Reader | 有合法 AuthorityBinding／Source manifest | Source metadata approved 冒原 SourceFreeze | `AUTHOR.W1.FHS-DR-023.01.NEG` → `SOURCE_FREEZE_APPROVAL_SPOOF` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `SourceFamily SHA+Locator+Conflict Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-023-02` / `L1-r4:L820@74140c6636d47df6` | Conflict/currentness unresolved 時只擋受影 compile；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `SOURCE_READ`；Original PIPD Authority/Source Reader | 原 Reader 回應 conflict_none | 沒核衝突就 promotion Canonical | `AUTHOR.W1.FHS-DR-023.02.NEG` → `SOURCE_AUTHORITY_CONFLICT_HOLD` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `SourceFamily SHA+Locator+Conflict Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-024-01` / `L1-r4:L821@79cff0ff9f58ddf0` | PI 每 OriginalID 保留 Parent/NEG/ClauseSHA/Oracle/FUO；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `LOCAL_DRAFT_WRITE`；SBL-hosted original PI Writer | 每 applicable 原字節 span 可重算 | 丟掉父句否定但保留 OriginalID | `AUTHOR.W1.FHS-DR-024.01.NEG` → `PIPD_PI_NEG_PARENT_LOSS` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Original PI SourceSpan/Parent/NEG/Oracle Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-024-02` / `L1-r4:L821@79cff0ff9f58ddf0` | Canonical PI 只能原 Writer 實編譯；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `LOCAL_DRAFT_WRITE`；SBL-hosted original PI Writer | 原 compile-pi Reader body+ACK | GPT 生成 JSON 假裝已編譯 | `AUTHOR.W1.FHS-DR-024.02.NEG` → `PIPD_FAKE_COMPILER_RECEIPT` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Original PI SourceSpan/Parent/NEG/Oracle Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-025-01` / `L1-r4:L822@d29de25b25ec66e9` | PD late bind 本地 root/HEAD/dirty/index/untracked/preimages；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `DEV_REPO_WRITE`；SBL original PD/RepoContext Reader | live RepoProbe 與 Scope 精確匹配 | remote HEAD 冒 local RepoContext | `AUTHOR.W1.FHS-DR-025.01.NEG` → `PD_REPOCONTEXT_UNBOUND` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Git root/HEAD/index/untracked/preimage/WriteSet Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-025-02` / `L1-r4:L822@d29de25b25ec66e9` | Repo drift 只對受影 bindings 重綁；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `DEV_REPO_WRITE`；SBL original PD/RepoContext Reader | Source-stable PI 不被任意重寫 | HEAD 漂移直接繼承 stale PD | `AUTHOR.W1.FHS-DR-025.02.NEG` → `PD_STALE_PREIMAGE_NACK` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Git root/HEAD/index/untracked/preimage/WriteSet Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-026-01` / `L1-r4:L823@24c0905dd984ad59` | DEV/OPS/USER 等各 EffectClass 不可共用 grant；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `USER_EFFECT`；Original PIPD ECP Writer and HGK Effect Issuer | 依各類型 Scope/Principal/rollback 拆 ECP | 以 OPS Permit 當 User Consent | `AUTHOR.W1.FHS-DR-026.01.NEG` → `ECP_EFFECT_CLASS_CROSS_GRANT_DENY` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `DEV/OPS/USER ECP intent plus real admission Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-026-02` / `L1-r4:L823@24c0905dd984ad59` | ECP/ConstructionContract 不等於 admission；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `HOST_OPS`；Original PIPD ECP Writer and HGK Effect Issuer | 同 Scope 原 Issuer ACK 再 effect | 無授權就 apply target repo/Host | `AUTHOR.W1.FHS-DR-026.02.NEG` → `ECP_NOT_ISSUER_PERMIT` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `DEV/OPS/USER ECP intent plus real admission Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-027-01` / `L1-r4:L824@f7b9653902524fed` | 13/19/8 原 ABI 精確有序一致；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `SOURCE_READ`；Original PIPD Schema/Case/CLI Reader | source-order+schema $id/version 相符 | 添加第14 CLI 或 family 改名 | `AUTHOR.W1.FHS-DR-027.01.NEG` → `PIPD_REGISTRY_EXACT_SET_NACK` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Original 13 CLI/19 Family/8 Skill/Case registry` / 原 Schema HOLD |
| `S-W1-FHS-DR-027-02` / `L1-r4:L824@f7b9653902524fed` | 原 TQAEP Case 各連 POS/NEG/Original Oracle；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `SOURCE_READ`；Original PIPD Schema/Case/CLI Reader | 原 CaseRaw/Runner/Checker 身份 | 缺 Runner 卻宣 Independent qualified | `AUTHOR.W1.FHS-DR-027.02.NEG` → `TQAEP_RUNNER_UNBOUND` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Original 13 CLI/19 Family/8 Skill/Case registry` / 原 Schema HOLD |
| `S-W1-FHS-DR-028-01` / `L1-r4:L825@c8436d7fe5e4bf02` | B1 27 PI→31 PD 是來源有型分裂而非 1:1；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `SOURCE_READ`；SBL original B1 PI/PD Reader (primary W3) | 逐 31 edge 原子/Effect 可追 | 拿 27 個 PI ID 當 31 PD 關閉 | `AUTHOR.W1.FHS-DR-028.01.NEG` → `B1_SPLIT_EDGE_LOSS` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Original 27→31 split-edge Reader Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-028-02` / `L1-r4:L825@c8436d7fe5e4bf02` | 此筆只作 W3 原 WP10 Read-only handoff；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `LOCAL_DRAFT_WRITE`；SBL original B1 PI/PD Reader (primary W3) | W3 owner 維持 31 raw Case | W1 搶寫 WP10 已定案 | `AUTHOR.W1.FHS-DR-028.02.NEG` → `CROSSWAVE_WRITESET_COLLISION` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Original 27→31 split-edge Reader Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-029-01` / `L1-r4:L826@cf3b7366587cc43c` | Fabric FHS-NAV/v2 唯讀先行再進三域；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-02` / `SOURCE_READ`；Fabric FHS navigation and Original Domain Reader (primary W0) | Fabric README/map 與原域 Reader 分離 | NAV metadata 冒 HGK admission | `AUTHOR.W1.FHS-DR-029.01.NEG` → `NAVIGATION_NOT_PERMISSION` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `FHS-NAV route read-only source Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-029-02` / `L1-r4:L826@cf3b7366587cc43c` | 三庫修改分別由各 repo branch+PR；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-02` / `SOURCE_READ`；Fabric FHS navigation and Original Domain Reader (primary W0) | 每庫自身 verified HEAD/rollback | 單一影子 commit 跨庫生效 | `AUTHOR.W1.FHS-DR-029.02.NEG` → `CROSS_REPO_WRITER_COLLISION` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `FHS-NAV route read-only source Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-030-01` / `L1-r4:L827@2f65ea9b20bb136f` | Fabric Source/Stage/Approval/Active 各獨立；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-02` / `HOST_OPS`；Fabric Policy Owner and HGK R8 Consumer | Active epoch 與源 hash 可回讀 | 只有 stage 就宣 Active | `AUTHOR.W1.FHS-DR-030.01.NEG` → `POLICY_STAGE_AS_ACTIVE_NACK` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `ActiveEpoch/LoadedSHA/R8 Consumer ACK Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-030-02` / `L1-r4:L827@2f65ea9b20bb136f` | HGK Loaded epoch/Consumer ACK 同 Scope 另有證據；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-02` / `HOST_OPS`；Fabric Policy Owner and HGK R8 Consumer | original R8 Consumer Raw 狀態 | 工具回應即視為 Policy Applied | `AUTHOR.W1.FHS-DR-030.02.NEG` → `POLICY_LOADED_CONSUMER_ACK_MISSING` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `ActiveEpoch/LoadedSHA/R8 Consumer ACK Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-031-01` / `L1-r4:L828@d6d886481ca51378` | 原 HGK Writer/Issuer/SharedSpine 唯一；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-03` / `HOST_OPS`；HGK original Issuer/Receiver/World Reader | 真 Issuer 發 same Scope grant | 普通 agent 模擬新 Permit | `AUTHOR.W1.FHS-DR-031.01.NEG` → `SHADOW_ISSUER_DENY` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `WorkID/nonce/TTL/ACL/Scope/World Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-031-02` / `L1-r4:L828@d6d886481ca51378` | OS SID/nonce/TTL/Scope/PolicyEpoch 綁同一效力；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-03` / `HOST_OPS`；HGK original Issuer/Receiver/World Reader | 原 Receiver 驗新 PID/epoch | 過期 nonce/跨 PID/Scope reuse | `AUTHOR.W1.FHS-DR-031.02.NEG` → `HGK_ISSUER_ACL_NONCE_TTL_NACK` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `WorkID/nonce/TTL/ACL/Scope/World Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-032-01` / `L1-r4:L829@86a508054c3705c9` | 單人 Owner 不等於 Maker/Issuer/Checker 技術混權；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-03` / `HOST_OPS`；HGK original OS ACL/Protected Checker Reader | 原 Host OS principle 不同且 ACL 有拒絕 | 建立兩個 Profile 名就算 OS 隔離 | `AUTHOR.W1.FHS-DR-032.01.NEG` → `OS_PRINCIPAL_SEPARATION_UNVERIFIED` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `SID+Principal+ACL Negative Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-032-02` / `L1-r4:L829@86a508054c3705c9` | 普通 Runtime 不可直接改 Protected Authority；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-03` / `HOST_OPS`；HGK original OS ACL/Protected Checker Reader | 原 ACL deny 測例可重播 | Maker 讀取並使用 Checker credential | `AUTHOR.W1.FHS-DR-032.02.NEG` → `MAKER_CHECKER_CREDENTIAL_DENY` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `SID+Principal+ACL Negative Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-034-01` / `L1-r4:L831@3a92f8db68739a2e` | Fabric/SBL/HGK 各有獨立 branch/PR；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `DEV_REPO_WRITE`；Each original Repo Owner/Reader (primary W0) | 三庫各自可追 pre/post HEAD | 作者草案直接改 main | `AUTHOR.W1.FHS-DR-034.01.NEG` → `REPO_MAIN_DIRECT_WRITE_DENY` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Per-repo original branch/PR/HEAD Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-034-02` / `L1-r4:L831@3a92f8db68739a2e` | 原 repo preimage/rollback 不能跨庫借用；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-05` / `DEV_REPO_WRITE`；Each original Repo Owner/Reader (primary W0) | 每庫本地 Git Scope 自證 | 以 SBL commit 自稱 HGK 已修改 | `AUTHOR.W1.FHS-DR-034.02.NEG` → `CROSS_REPO_HEAD_MISMATCH` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Per-repo original branch/PR/HEAD Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-035-01` / `L1-r4:L832@1b20726a0e3e94b7` | Direct/Delegation/Kanban/Swarm 按複雜度；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-04` / `SOURCE_READ`；Hermes original runtime Owner | 小 read 直接處理無重啟 | 小 read 強制新多 Agent queue | `AUTHOR.W1.FHS-DR-035.01.NEG` → `HERMES_OVERENGINEERING_NACK` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Hermes v0.22.5 Task/Queue/Journal Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-035-02` / `L1-r4:L832@1b20726a0e3e94b7` | 原 Queue/Journal/lease 原位恢復；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-04` / `HOST_OPS`；Hermes original runtime Owner | 相同 WorkID JournalCursor/lease_generation | 盲重播 UNKNOWN nonidempotent | `AUTHOR.W1.FHS-DR-035.02.NEG` → `HERMES_WORLD_RECONCILE_REQUIRED` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Hermes v0.22.5 Task/Queue/Journal Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-036-01` / `L1-r4:L833@e9451e2f0a2ff3af` | PLAN/EXECUTE/VERIFY_SECURITY 分別保存 required/selected；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-04` / `HOST_OPS`；Hermes Provider Response and HGK Lane Reader | 三 Lane 原 Policy 必需集合分立 | Selected 便算 ActualServed | `AUTHOR.W1.FHS-DR-036.01.NEG` → `ACTUAL_SERVED_MISSING` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `3 Lane Required/Selected/Invoked/ActualServed Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-036-02` / `L1-r4:L833@e9451e2f0a2ff3af` | 真 provider response/usage/tool turn 才算 served；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-04` / `HOST_OPS`；Hermes Provider Response and HGK Lane Reader | 同 Subject/PID/Invocation 真 response | 拿不同 provider 的 raw 充用 | `AUTHOR.W1.FHS-DR-036.02.NEG` → `PROVIDER_RAW_FOREIGN_NACK` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `3 Lane Required/Selected/Invoked/ActualServed Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-042-01` / `L1-r4:L839@f09232acf35187bd` | 原五集合身份/Disposition 每個 Need 保留；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-17` / `SOURCE_READ`；Original Technology/License/Host Owner (primary W3) | 符合原 Required 才有 qualified Occupant | 將 default mandatory 偷改 optional | `AUTHOR.W1.FHS-DR-042.01.NEG` → `DESIGN_DEFAULT_DOWNGRADE` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Need→Occupant→Used+rollback Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-042-02` / `L1-r4:L839@f09232acf35187bd` | install/load/used 是分立原 Host 證據；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-17` / `HOST_OPS`；Original Technology/License/Host Owner (primary W3) | same Need+Scope 一個活躍 Occupant | 外部介紹文當原 Host Loaded | `AUTHOR.W1.FHS-DR-042.02.NEG` → `CAPABILITY_LOAD_UNVERIFIED` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Need→Occupant→Used+rollback Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-042-03` / `L1-r4:L839@f09232acf35187bd` | NoFit/替換需原 Owner 採許可且有 LastGood；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-17` / `HOST_OPS`；Original Technology/License/Host Owner (primary W3) | 受影 Replacement POS+NEG/rollback | 任意雙 active occupant | `AUTHOR.W1.FHS-DR-042.03.NEG` → `DOUBLE_ACTIVE_OCCUPANT_DENY` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `Need→Occupant→Used+rollback Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-043-01` / `L1-r4:L840@fbd8e512dd59008b` | OpenSpec Brownfield 是 SpecDelta 方法；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-17` / `LOCAL_DRAFT_WRITE`；Original Technology/PIPD Reader (primary W0) | 原 Source-bound PIPD 重 parse | OpenSpec archive 自簽 PI | `AUTHOR.W1.FHS-DR-043.01.NEG` → `OPENSPEC_NOT_CANONICAL_WRITER` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `SpecDelta→Original PIPD Reader Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-043-02` / `L1-r4:L840@fbd8e512dd59008b` | Windows/Node/Version/License 實際 probe；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-17` / `HOST_OPS`；Original Technology/PIPD Reader (primary W0) | 有 executable SHA 與原 Host runner | 研究版號當已部署 pin | `AUTHOR.W1.FHS-DR-043.02.NEG` → `EXTERNAL_TOOL_PIN_UNBOUND` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `SpecDelta→Original PIPD Reader Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-044-01` / `L1-r4:L841@c395be8a0aefbd9a` | gstack finding 只能送原 QA/Case Reader；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-17` / `SOURCE_READ`；Original Technology/QA Reader (primary W0) | 原 Runner 能重現 failure | gstack /ship 冒 Original Publisher | `AUTHOR.W1.FHS-DR-044.01.NEG` → `GSTACK_NOT_PUBLISHER` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `gstack advisory→Original Case Runner Raw` / 原 Schema HOLD |
| `S-W1-FHS-DR-044-02` / `L1-r4:L841@c395be8a0aefbd9a` | Windows Host 必須實核 support/permission；Subject/Scope/Need/Host/Effect 適用前先由原 Reader 核 | `WP-FHS-17` / `HOST_OPS`；Original Technology/QA Reader (primary W0) | 原 Host installed/invoked 結果 | README 言詞當 Windows Tested | `AUTHOR.W1.FHS-DR-044.02.NEG` → `GSTACK_HOST_SUPPORT_HOLD` | `ORIGINAL_ID_READER_HOLD`; `ORIGINAL_CASE_ORACLE_READER_HOLD`; `gstack advisory→Original Case Runner Raw` / 原 Schema HOLD |

**矩陣退出規則**：一張 DesignID 的全部 `subclaim_id` 都要有原行與其 Parent/NEG 擬議語義、不同 POS/NEG、原 Receiver 或具名 HOLD；不能以通用 `DESIGN_OBLIGATION_MISSING` 代業務 FirstFail。此通用碼只在整列遺失時作靜態 Fixture。`INT-13` 最末端原 Consumer 在 L1/L2 受審來源真被截斷，最後一條保留 `RECEIVER_IDENTITY_HOLD`，由原 Domain Reader 及上位 L1/L2 作者端受影修補，**不得**填入猜測的完整名稱。

## W1-r5｜22 WP／36 DAG：原身份不改、Hard/Soft 依受影 Operation 決定

**原 DAG 僅一份**，本波只更新 W1 Producer/Consumer 設計，不增加相反邊；22 WP 各有唯一主波，`WP00/01/15/16/19/21` 屬 W0、`WP02/03/04/05/07/11/17/20` 屬 W1、`WP06/08/09/18` 屬 W2、`WP10/12/13` 屬 W3、`WP14` 屬 W4。`WP-FHS-02/03→WP-FHS-17→WP-FHS-06` 是真受護能力自舉入邊；**嚴禁** `WP06→WP17`。對 `SOURCE_READ` 不要求 OPS Permit，遇到一個受影 HOST_OPS 錯誤不凍結其他合法 READ/DRAFT。Hard 為原 Consumer 的指定 Operation 真消耗前件 Original ACK/Raw；Soft 只允許不消耗受護權限的讀取/草稿並行。原 Reader 若未核具體 Hard/Soft → `EDGE_OPERATION_BIND_HOLD`，不改邊存在。

| WP | 原產品功能與輸出 | 原 dep→WP（不創新邊） | Primary | Effect / Original Reader→Consumer |
|---|---|---|---|---|
| `WP-FHS-00` Source/Host Discovery | SourceManifest+RepoContext。 | `ROOT` | **W0** | \`SOURCE_READ\`；原唯讀 ACL/read scope。；原 SourceReader/RepoProbe → \`SourceManifest + RepoContext readback\` → 原 TPM/PIPD Source Reader。 |
| `WP-FHS-01` Authority/Oracle/Profile | AuthorityConflictLedger+Oracle/ProfileBinding。 | `WP-FHS-00` | **W0** | \`SOURCE_READ\`；原唯讀 ACL/read scope。；原 Authority/Profile Owner → \`AuthorityBinding/ProfileBinding 原 19-schema Registry\` → PIPD compile-pi。 |
| `WP-FHS-02` Fabric Policy Consumer | PolicyLoadedConsumerACK。 | `WP-FHS-01` | **W1** | \`HOST_OP\`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。；Fabric Policy Owner → \`FABRIC/fabric/consumers/hgk_policy_consumer.py 原 Consumer ABI\` → HGK policy consumer。 |
| `WP-FHS-03` HGK Registry/Issuer | IssuerReceiverBinding。 | `WP-FHS-01` | **W1** | \`HOST_OP\`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。；HGK 原 Registry/Resolver/Issuer → \`原 HGK WorkOrder/ExecutionBinding/Permit ABI\` → 原 HGK Receiver。 |
| `WP-FHS-04` Hermes Durable Runtime | WakeLeaseRuntimeBinding。 | `WP-FHS-00` | **W1** | \`HOST_OP\`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。；Hermes 原 runtime/journal Owner → \`原 WorkID/Queue/Lease/Journal ABI\` → 原 bounded Worker。 |
| `WP-FHS-05` PIPD Native Compiler | PI/PD/DEV-OPS候選。 | `WP-FHS-01` | **W1** | \`LOCAL_DRAFT_WRITE\`；明列隔離 output root 的使用者授權。；PIPD 原 Intake/PI/PD/ECP Compiler → \`PIPD schemas/registry.json 原 19 families\` → HGK construction/OPS adapters。 |
| `WP-FHS-06` Legal First Reversible Slice | 最小可逆Repo diff+Raw。 | `WP-FHS-02, WP-FHS-03, WP-FHS-04, WP-FHS-05, WP-FHS-17` | **W2** | \`REPO_WRITE\`；DEV ECP + exact WriteSet + 原 HGK admission。；已受權 Codex bounded Writer → \`ConstructionContract + DEV ECP + 原 HGK admission\` → 原 Repo Reader/Checker。 |
| `WP-FHS-07` Native PLAN Commander A/B/C | PlanRevisionProposal+CAS ACK。 | `WP-FHS-01, WP-FHS-15` | **W1** | \`LOCAL_DRAFT_WRITE\`；明列隔離 output root 的使用者授權。；原 SBL TPM/Commander PLAN Reader → \`PlanRevisionProposal + 原 PLAN CAS ABI\` → 原 HGK PLAN Reader。 |
| `WP-FHS-08` FHS Execute Worker | WorkerEffectRaw+JournalCursor。 | `WP-FHS-06, WP-FHS-07` | **W2** | \`HOST_OP\`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。；原 Hermes Dispatcher + bounded Worker → \`原 ExecutionBinding/lease fence/EffectRaw ABI\` → 原 WorldRaw Collector。 |
| `WP-FHS-09` Challenge/Protected AO | ProtectedCheckerRequest/Receipt（需另一主體）。 | `WP-FHS-08, WP-FHS-21` | **W2** | \`SOURCE_READ\`；原唯讀 ACL/read scope。；原 WorldRaw Producer → \`原 TQAEP/Protected Checker Request ABI\` → 不同 Principal 的原 Protected Checker。 |
| `WP-FHS-10` B1 3 GWO & G-A/G-B | 三GWO各自Raw+G-A/G-B。 | `WP-FHS-09, WP-FHS-20` | **W3** | \`HOST_OP\`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。；Fabric/HGK/SBL 三個原 GWO Owner → \`B1 原 PI27→PD31→TQAEP ABI\` → 三 GWO 各自原 Receiver。 |
| `WP-FHS-11` Portable Host Dogfood | 三SP逐Host loaded/invoked raw。 | `WP-FHS-05, WP-FHS-16` | **W1** | \`HOST_OP\`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。；原 Portable SP packager/Host Loader → \`原各 Host install/load/invoke/remove manifest\` → 各 Host 原 Skill Reader。 |
| `WP-FHS-12` W18 Normal Mode | 新PID普通Goal E33-E42 Raw。 | `WP-FHS-10, WP-FHS-11` | **W3** | \`HOST_OP\`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。；原 Hermes normal-entry Owner → \`W18 ordinary Goal/E33–E42 原 ABI\` → 原 normal Profile/ToolAutoSelect Reader。 |
| `WP-FHS-13` CAP On-Demand + HotSwap | CAP gap/HotSwap parity+readback。 | `WP-FHS-16, WP-FHS-17` | **W3** | \`HOST_OP\`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。；原 TechnologyAdmission/Host capability Owner → \`原 Need/Occupant/HotSwap admission ABI\` → 原有 Consumer 與 Host Loader。 |
| `WP-FHS-14` Release/Retire Candidate | ReleaseCandidate+原Publisher receipt。 | `WP-FHS-09, WP-FHS-19` | **W4** | \`RELEASE\`；原 Publisher/GHP-02 + 受保護 Checker。；原 Publisher → \`原 Release/Retire + GHP-02 ABI\` → 原發行 channel Reader。 |
| `WP-FHS-15` TPM Corpus & SPEC 18Stage | 原三SPECDraft、來源readback、FUO十欄；三份受界 SPECDraft／`TaskSpecSeed CANDIDATE`；歷史來源曾記 24 功能 Atom／PI/PD 設計意圖，但本輪未見同 Scope 原 PIPD Reader 真 ACK，`H-WP15-HISTORICAL-ACK-UNVERIFIED`。 | `WP-FHS-00` | **W0** | \`LOCAL_DRAFT_WRITE\`；明列隔離 output root 的使用者授權。；原 TPM Corpus Reader/PM/SE/TPgM → \`SBL 三 SPECDraft + source-bound Stage contracts\` → 原 PIPD Intake。 |
| `WP-FHS-16` Donor/Method Slot Translation | 24slot/25method壓製候選。 | `WP-FHS-00` | **W0** | \`LOCAL_DRAFT_WRITE\`；明列隔離 output root 的使用者授權。；原 SBL DOC06 TechnologyAdmission Owner → \`原 24 Donor Slot/25 Method Reader projection\` → 原 TPM/PIPD/HGK 各受影 Consumer。 |
| `WP-FHS-17` CAP-BOOT Native Occupants | needed能力最小HostOccupant+loaded ACK。 | `WP-FHS-00, WP-FHS-02, WP-FHS-03` | **W1** | \`HOST_OP\`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。；原 Host Installer + HGK 原 Issuer → \`CAP-BOOT 原 Host admission + manifest ABI\` → 原 Host capability Registry/Consumer。 |
| `WP-FHS-18` FAR Bounded Repair & Incident | BoundedRepairDiff+RedGreen+residue。 | `WP-FHS-08` | **W2** | \`REPO_WRITE\`；DEV ECP + exact WriteSet + 原 HGK admission。；原 FAR/incident Reader + bounded Writer → \`原 FirstFail/RepairCone + DEV ECP ABI\` → 原 affected rechallenge/Checker。 |
| `WP-FHS-19` CI/Supply Chain & Requal | CI/License/NOTICE/SBOM掃描Raw。 | `WP-FHS-00` | **W0** | \`SOURCE_READ\`；原唯讀 ACL/read scope。；原 CI/supply-chain Reader → \`原 license/NOTICE/SBOM/dependency evidence ABI\` → 原 release-readiness Reader。 |
| `WP-FHS-20` CLI/Agent/Host Kind Matrix | 192Cell適用/NoFit/Host Raw。 | `WP-FHS-05, WP-FHS-16` | **W1** | \`HOST_OP\`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。；原 Product/Host matrix Owner → \`原八 Kind×三 Mode×四 Host×Provider token Cell ABI\` → 每個原 Cell 的原 Host Reader。 |
| `WP-FHS-21` Challenge 96/H4/SEAM Coverage | 96Cell/H4/SEAM原Oracle計畫。 | `WP-FHS-01` | **W0** | \`SOURCE_READ\`；原唯讀 ACL/read scope。；原 Acceptance/Oracle Owner → \`原 AC15/Oracle96/H4/SEAM Reader ABI\` → 原 Protected AO Request Reader。 |

| Original Edge | Predecessor→Successor | L2-r4 source line | Consumer Hard/Soft 設計規則 |
|---|---|---|---|
| E01 | `WP-FHS-00` → `WP-FHS-01` | L2-r4:L489 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E02 | `WP-FHS-01` → `WP-FHS-02` | L2-r4:L490 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E03 | `WP-FHS-01` → `WP-FHS-03` | L2-r4:L491 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E04 | `WP-FHS-00` → `WP-FHS-04` | L2-r4:L492 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E05 | `WP-FHS-01` → `WP-FHS-05` | L2-r4:L493 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E06 | `WP-FHS-02` → `WP-FHS-06` | L2-r4:L494 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E07 | `WP-FHS-03` → `WP-FHS-06` | L2-r4:L495 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E08 | `WP-FHS-04` → `WP-FHS-06` | L2-r4:L496 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E09 | `WP-FHS-05` → `WP-FHS-06` | L2-r4:L497 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E10 | `WP-FHS-17` → `WP-FHS-06` | L2-r4:L498 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E11 | `WP-FHS-01` → `WP-FHS-07` | L2-r4:L499 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E12 | `WP-FHS-15` → `WP-FHS-07` | L2-r4:L500 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E13 | `WP-FHS-06` → `WP-FHS-08` | L2-r4:L501 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E14 | `WP-FHS-07` → `WP-FHS-08` | L2-r4:L502 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E15 | `WP-FHS-08` → `WP-FHS-09` | L2-r4:L503 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E16 | `WP-FHS-21` → `WP-FHS-09` | L2-r4:L504 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E17 | `WP-FHS-09` → `WP-FHS-10` | L2-r4:L505 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E18 | `WP-FHS-20` → `WP-FHS-10` | L2-r4:L506 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E19 | `WP-FHS-05` → `WP-FHS-11` | L2-r4:L507 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E20 | `WP-FHS-16` → `WP-FHS-11` | L2-r4:L508 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E21 | `WP-FHS-10` → `WP-FHS-12` | L2-r4:L509 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E22 | `WP-FHS-11` → `WP-FHS-12` | L2-r4:L510 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E23 | `WP-FHS-16` → `WP-FHS-13` | L2-r4:L511 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E24 | `WP-FHS-17` → `WP-FHS-13` | L2-r4:L512 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E25 | `WP-FHS-09` → `WP-FHS-14` | L2-r4:L513 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E26 | `WP-FHS-19` → `WP-FHS-14` | L2-r4:L514 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E27 | `WP-FHS-00` → `WP-FHS-15` | L2-r4:L515 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E28 | `WP-FHS-00` → `WP-FHS-16` | L2-r4:L516 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E29 | `WP-FHS-00` → `WP-FHS-17` | L2-r4:L517 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E30 | `WP-FHS-02` → `WP-FHS-17` | L2-r4:L518 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E31 | `WP-FHS-03` → `WP-FHS-17` | L2-r4:L519 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E32 | `WP-FHS-08` → `WP-FHS-18` | L2-r4:L520 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E33 | `WP-FHS-00` → `WP-FHS-19` | L2-r4:L521 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E34 | `WP-FHS-05` → `WP-FHS-20` | L2-r4:L522 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E35 | `WP-FHS-16` → `WP-FHS-20` | L2-r4:L523 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |
| E36 | `WP-FHS-01` → `WP-FHS-21` | L2-r4:L524 | Original operation consumes predecessor ACK/Raw: Hard; local read/draft only: Soft if same scope; original Reader confirmation pending |

> **讀者優先順序**：下一段是 W1 r2 既有受界功能契約的高保留融合；其中歷史 `L0/L1/L2 r2` 版號、早期來源行、舊 SLA 與單例描述不得取代本稿上方 r4 SHA/24 張有效設計卡/原 L1-r4 個別 CH。任何與 L1-r4 新增 `R4-BEGIN` 修補衝突者，以該 CH 的 r4 現行增量優先，未能證明等價時 `AFFECTED_SOURCE_IMPACT_HOLD`。

## W1-r5｜八個 WP 的實質設計差額（保留 r2 合法行為，受影由 r4 覆蓋）

01｜W1 產品／架構／Program 完整工程藍圖

> **法位／聲明上限**：`FHS_PKG_WAVE_001 / L3_W1_AUTHOR_SIDE_BLUEPRINT_AND_SKELETON / AUTHOR_DESIGN_ONLY`。本交付不是 W1 草案／定案、SourceFreezeManifest、Canonical PI/PD/ECP/TQAEP、原 Issuer Permit、Host Loaded 證據、Native E2E、Protected Checker 或正式 Release。此處所有 POS/NEG/ACK/WorldRaw 均為 **期待的測例或原 Reader 介面設計**，不是本輪觀測到的驗收 PASS；原 Domain Writer/Owner/Consumer 不移轉，當期 Host/Owner 未回證則範圍局部 HOLD。

## 1. 專家動態職能與產品身份

採《FHS_專業角色動態掛載總表》按子任務選 **FHS-R00**（跨波架構）、**R04/R05**（來源/權威）、**R06/R07**（SBL Product/TPM）、**R08/R09**（PIPD/PD）、**R10/R11/R12/R13**（Fabric/HGK/Hermes/Swarm）、**R17/R19**（security/technology）、**R27/R28**（Package/ABI）。只代表本輪 GPT-6 分析視角，**零新增** Native principal/Issuer/Checker。

**JTBD**：單人 Owner 由普通 Goal 得三份不同 source-bound SPEC；原 PIPD 以原 Reader 收受 Intent/Authority/Profile，生成不改 OriginalID 的 PI，真 RepoContext 才晚綁 PD，依 EffectClass 設計 ECP/TQAEP；原 Fabric/HGK/Hermes/Host 具名地說明能否進入受界 W2 最小效果。**首個可用結果**是原 Consumer 能判的 binding request／typed NACK／授權前置差額，而非 485 工具全裝、全部 Release Gate 綠燈。

**Non-goals**：不建第二 Policy/Queue/Compiler/Issuer/Case Registry；不要求每個一般 SOURCE_READ 先取得 OPS Permit；不將 Hermes v0.22.5 默升；不讓 OpenSpec/gstack 取代 Original PIPD 或 Protected Checker；不把全產品 949/192/282/96 原分母抹除或強迫每次 Goal 先執行全部分母。

## 2. 產品、Architecture 與 Program 三 SPEC 不能合併

| SPEC | W0 Input/Owner | W1 實際設計消費與 FUO | NEG/首敗 |
|---|---|---|---|
| Product SPEC | W0:PM；Goal/Persona/7 pains/Kind/MVP/Scope/OriginalID | Consumer=PIPD Intake；非空需求、可見 FUO、每個 applicable POS/NEG | 以檔案數當 FUO，或將禁令當 optional → `FUO_OR_NEG_LOST` |
| Architecture SPEC | W0:SE；Writer/ABI/host/Policy/effect/ADR | Consumer=PD Binder/Fabric/HGK Readers；每 Seam 版本、backward/forward、原 Principal | 提案版自行發布 Permit/第二 Queue → `SHADOW_AUTHORITY_DENY` |
| Program SPEC | W0:TPgM；原 22 WP/36 edge/EvidenceExpectation | Consumer=W1 WP 原 Owner；依 EffectClass/HARD-SOFT/FirstFail/Resume | 倒置 17↔06、把 36 全 Hard → `DAG_DELTA_OR_CYCLE` |

## 2.1 W1 受影七痛點／FUO 反向路由（不代替 W0 七痛點的全產品主責）

| L0 原 Pain | W1 受影 WP/CH | 具體輸入→行為 | 原 Consumer 可見正例 | 專屬 NEG | 下一波 |
|---|---|---|---|---|---|
| P01 選型難 | WP17/CH22; WP11/CH08 | Original NeedKey/Host+AssetType→SourceBound MethodDecision | 相同 Need 最多一個 active occupant；必要時回 CAPABILITY_GAP_HOLD | 擅自安裝不相容 donor | W2 只消費 affected capability ready |
| P02 交接斷裂 | WP05/CH12–16; WP07/CH34 | S1 PI→S2 PD/ECP/TQAEP→S3 PLAN CAS 原 ACK | 原 Consumer 可讀 typed payload/或具名 NACK | 不同 Subject/Scope schema 被接受 | W2 需 original ACK |
| P03 重問問題 | WP05/CH13; WP07/CH34 | W0 QuestionLedger keyed Subject+SourceSHA+Scope | 相同問題已核定答案直接重用 | 新 source SHA 仍套舊答案 | W0 Owner QuestionLedger |
| P04 Writer 碰撞 | WP03/CH18; WP05/CH12; WP07/CH34 | 單一 original PIPD Writer+原 PLAN CAS+原 HGK Issuer | 禁止第二 Compiler/Issuer/Queue 仍可產候選 | Method/Skill 自簽 Permit | W2 original admission only |
| P05 假 PASS | WP11/CH08/39; WP20/CH40 | SP/Case/Cell 各有 raw/consumer; test aliases 非原 receipt | Original per-effect FirstFail 被區分 | CI green/Selected 冒 Checked | W2 原 Checker 而非 Maker |
| P06 Host 假掛載 | WP04/CH19; WP11/CH22; WP17/CH18 | Original Host Selected→Installed→Loaded→Invoked→Used→Removed | 相同 Host+PID+SHA 資格化；不可互借 | ZIP manifest=HostLoaded | W2 min needed native occupant |
| P07 FUO 最後一哩 | WP04/CH20; WP17/CH22; WP20/CH40 | Normal Goal→original Worker→WorldRaw+resume/proper exit | 原 Consumer 可見真正結果或具名合法 HOLD | README-only / non-reproducible output | W2 affected world raw / W3 W18 |


**產品 FUO 定義**：W1 作者端第一有效成果為可由 W1 草案 Maker 使用的 `same-subject` source-bound Seam/OriginalID/Need/Case/Host 接收契約，而不是 Markdown 文件數量本身。只有原 Reader ACK 才能稱 `WP05_ORIGINAL_READER_ACCEPTED`；只有 W2 真世界 Raw 才能稱 `AFFECTED_NATIVE_DONE`。保留 L0 的八 Kind/三 Mode/四 Portable Host 原身份與不同適用性；本表不聲稱七個真使用者旅程已 Native Qualified。

## 3. 八個 Original WP——逐件可編製／可恢復契約

原依賴 **取自 L2 §4.1／§5.1**，不是本包重建的新 WorkPackage。以下原操作中 READ、DRAFT 可在允許範圍單獨前進；HOST_OPS 若需真效果則按原 Policy/Issuer/Host 類型拒收。每個 Output 在本輪都是**期待的 Original Reader 接收結果**，並非真 Raw。

### WP-FHS-02｜Fabric Policy Consumer（L2-r4:L462）

- **Original DependsOn**：`WP-FHS-01`；硬／軟：受原 Consumer 的實際 Operation consumption 判定，未讀回 `EDGE_HARD_SOFT_OWNER_BIND_HOLD`。
- **Original L2 Effect 界線**：`HOST_OP`；原 WP 內合法唯讀 Help/Probe 和真 Host OPS 不可混為一個不可分 Gate。
- **Input／Guard**：WP01 AuthorityBinding/SourceSHA/PolicyRef；Fabric 原 Policy 源、Target Host、該 Effect 的 Scope；相同 `Subject/CandidateSHA/SourceSHA/Scope/HostID/PolicyEpoch` 有關聯時必一致。
- **Producer → 原 ABI/Reader → Consumer／Owner**：原 Fabric Policy Owner → 原 HGK Policy Consumer；具體 `$id`、Reader/Host 路徑以當期原 Registry 為準，缺則 `RECEIVER_UNBOUND`。
- **Typed Output／能交付的 FUO**：Source→Stage→OwnerApproved→ActiveEpoch→LoadedDigest→HGK ConsumerACK 六欄獨立的 `PolicyLoadedConsumerACK@design`；真值由原 Reader 回傳。
- **POS（期待可觀測的 Reader 輸出）**：同 scope、版本/epoch 的原 Fabric Active policy 與 HGK 原 Consumer loaded ACK 相合；Source、Stage、Approval 另有不同來源。
- **NEG／SEC（不得被接受）**：只有 Stage/鏡像或 `NAV_ASSISTED_USE_APPROVED` 卻標 Loaded/Issuer。
- **Expected FirstFail**：`WP-FHS-02.FIRST_FAIL:POLICY_NOT_LOADED`。靜態本包尚未對原 Reader 注入此測例。
- **Hold／解鎖**：`H-ABI-05 / FABRIC_EFFECTIVE_POLICY_READER_HOLD`；由原受影 Owner/Reader 回送時期、Reader identity、來源 SHA、同 Scope 真 Raw/ACK 才解除。
- **Stop／Resume**：保留 same Subject/Candidate/Scope/source refs、first_fail、last_good/checkpoint；Reader 不可用時只 PARK 本 WP 的必要效果，不停來源讀取／隔離草案。
- **Rollback**：受影載入由原 Host owner 撤銷/回復 last-good epoch；純讀不回退。
- **W2 Handoff**：若影響 W2:WP06/08，傳 `WP_ref,original_dependency_edge_refs,original_reader,receiver_abi,source_sha,candidate_sha,scope,host,policy_epoch,effect,permission_needed,firstfail,raw_or_expected,HOLD,rollback`; `EXPECTATION` 與 `MEASURED` 不互換。

### WP-FHS-03｜HGK Registry/Issuer（L2-r4:L463）

- **Original DependsOn**：`WP-FHS-01`；硬／軟：受原 Consumer 的實際 Operation consumption 判定，未讀回 `EDGE_HARD_SOFT_OWNER_BIND_HOLD`。
- **Original L2 Effect 界線**：`HOST_OP`；原 WP 內合法唯讀 Help/Probe 和真 Host OPS 不可混為一個不可分 Gate。
- **Input／Guard**：WP01 Source/Authority、受影 Subject/Candidate/Scope、HGK 原 Registry/Issuer/OS Principal/nonce/TTL；相同 `Subject/CandidateSHA/SourceSHA/Scope/HostID/PolicyEpoch` 有關聯時必一致。
- **Producer → 原 ABI/Reader → Consumer／Owner**：原 HGK Registry/Resolver/Issuer/Receiver Owner；具體 `$id`、Reader/Host 路徑以當期原 Registry 為準，缺則 `RECEIVER_UNBOUND`。
- **Typed Output／能交付的 FUO**：`IssuerReceiverBinding@design` 及原 WorkID/Permit 的期待欄；未讀原 Issuer 收據僅 `ISSUER_UNBOUND`。
- **POS（期待可觀測的 Reader 輸出）**：原 Registry schema/版本/Process ACL、Issuer 原簽章核准與同 Subject/Scope/epoch/Receiver 一致。
- **NEG／SEC（不得被接受）**：用 ECP intent 或 GitHub 原始碼自製 WorkID/Permit；借其他 SID 的 credential。
- **Expected FirstFail**：`WP-FHS-03.FIRST_FAIL:ISSUER_BINDING_INVALID`。靜態本包尚未對原 Reader 注入此測例。
- **Hold／解鎖**：`H-ABI-05 / H-OS-08`；由原受影 Owner/Reader 回送時期、Reader identity、來源 SHA、同 Scope 真 Raw/ACK 才解除。
- **Stop／Resume**：保留 same Subject/Candidate/Scope/source refs、first_fail、last_good/checkpoint；Reader 不可用時只 PARK 本 WP 的必要效果，不停來源讀取／隔離草案。
- **Rollback**：原 Issuer 的 Revoke/lease fence，UNKNOWN 先向原 Registry reconcile，不能自己更改 ledger。
- **W2 Handoff**：若影響 W2:WP06/08，傳 `WP_ref,original_dependency_edge_refs,original_reader,receiver_abi,source_sha,candidate_sha,scope,host,policy_epoch,effect,permission_needed,firstfail,raw_or_expected,HOLD,rollback`; `EXPECTATION` 與 `MEASURED` 不互換。

### WP-FHS-04｜Hermes Durable Runtime（L2-r4:L464）

- **Original DependsOn**：`WP-FHS-00`；硬／軟：受原 Consumer 的實際 Operation consumption 判定，未讀回 `EDGE_HARD_SOFT_OWNER_BIND_HOLD`。
- **Original L2 Effect 界線**：`HOST_OP`；原 WP 內合法唯讀 Help/Probe 和真 Host OPS 不可混為一個不可分 Gate。
- **Input／Guard**：WP00 Host discovery、Hermes v0.22.5 pin、原 queue/lease/journal/profiles runtime readback；相同 `Subject/CandidateSHA/SourceSHA/Scope/HostID/PolicyEpoch` 有關聯時必一致。
- **Producer → 原 ABI/Reader → Consumer／Owner**：Hermes 原 Runtime/Journal Owner 與 HGK 原 WorkID Consumer；具體 `$id`、Reader/Host 路徑以當期原 Registry 為準，缺則 `RECEIVER_UNBOUND`。
- **Typed Output／能交付的 FUO**：`WakeLeaseRuntimeBinding@design`：原 WorkID、wake、queue item、lease_generation、checkpoint_sha、journal_cursor、PID/profile_sha。
- **POS（期待可觀測的 Reader 輸出）**：原 Writer/Reader 讀出同 WorkID 的原 queue、lease fence、checkpoint 與一次 recoverable wake。
- **NEG／SEC（不得被接受）**：另建 SQLite queue、把 PID 存在當 tool call、舊 generation 仍 commit。
- **Expected FirstFail**：`WP-FHS-04.FIRST_FAIL:RUNTIME_LEASE_BINDING_DENY`。靜態本包尚未對原 Reader 注入此測例。
- **Hold／解鎖**：`H-LANE-06 / RUN_BUDGET_BIND_HOLD`；由原受影 Owner/Reader 回送時期、Reader identity、來源 SHA、同 Scope 真 Raw/ACK 才解除。
- **Stop／Resume**：保留 same Subject/Candidate/Scope/source refs、first_fail、last_good/checkpoint；Reader 不可用時只 PARK 本 WP 的必要效果，不停來源讀取／隔離草案。
- **Rollback**：由原 journal cursor 與 last-good checkpoint Resume，UNKNOWN 先 world readback，不重發非冪等 effect。
- **W2 Handoff**：若影響 W2:WP06/08，傳 `WP_ref,original_dependency_edge_refs,original_reader,receiver_abi,source_sha,candidate_sha,scope,host,policy_epoch,effect,permission_needed,firstfail,raw_or_expected,HOLD,rollback`; `EXPECTATION` 與 `MEASURED` 不互換。

### WP-FHS-05｜PIPD Native Compiler（L2-r4:L465）

- **Original DependsOn**：`WP-FHS-01`；硬／軟：受原 Consumer 的實際 Operation consumption 判定，未讀回 `EDGE_HARD_SOFT_OWNER_BIND_HOLD`。
- **Original L2 Effect 界線**：`LOCAL_DRAFT_WRITE`；原 WP 內合法唯讀 Help/Probe 和真 Host OPS 不可混為一個不可分 Gate。
- **Input／Guard**：W0 同 Subject 不同 Product/Architecture/Program SPECDraft、31 SourceSHA、WP01 Authority/Profile、原 13 CLI/19 families/8 skills、真 Repo probe（僅 PD）；相同 `Subject/CandidateSHA/SourceSHA/Scope/HostID/PolicyEpoch` 有關聯時必一致。
- **Producer → 原 ABI/Reader → Consumer／Owner**：SBL integrations/pipd 原 Source/Compiler/PD/ECP/TQAEP Reader；具體 `$id`、Reader/Host 路徑以當期原 Registry 為準，缺則 `RECEIVER_UNBOUND`。
- **Typed Output／能交付的 FUO**：原 `IntentCard → SourceFreeze/Authority → ProfileBinding → PI-PKG(strict)` 與 `SBL.PI.Crosswalk@2` sidecar；真 RepoContext 綁 `PD-PKG`；DEV/OPS ECP 與 PlannedTQAEP 分別設計。
- **POS（期待可觀測的 Reader 輸出）**：原 13 CLI/19 Registry 同版，原 Reader 以 nonempty goal+locators 重算 atoms/PI；九軸 safety veto 有效；PD scope 與真 HEAD 相符。
- **NEG／SEC（不得被接受）**：舊第四庫當 Writer、13+1 虛構命令、`_profile_meta` 塞 strict PI、用 remote HEAD 冒本地、ExpectedTQAEP 當 Raw。
- **Expected FirstFail**：`WP-FHS-05.FIRST_FAIL:PIPD_FORMAL_PROMOTION_HOLD`。靜態本包尚未對原 Reader 注入此測例。
- **Hold／解鎖**：`H-PIPD-04 / ORIGINAL_PIPD_PRE_V2_ROUTING_HOLD / REPO_HEAD_BIND_HOLD`；由原受影 Owner/Reader 回送時期、Reader identity、來源 SHA、同 Scope 真 Raw/ACK 才解除。
- **Stop／Resume**：保留 same Subject/Candidate/Scope/source refs、first_fail、last_good/checkpoint；Reader 不可用時只 PARK 本 WP 的必要效果，不停來源讀取／隔離草案。
- **Rollback**：隔離 candidate 可撤銷；如 Host/Scope/SourceSHA 改變僅重綁受影 PD/ECP，不重寫已穩定 PI 語義。
- **W2 Handoff**：若影響 W2:WP06/08，傳 `WP_ref,original_dependency_edge_refs,original_reader,receiver_abi,source_sha,candidate_sha,scope,host,policy_epoch,effect,permission_needed,firstfail,raw_or_expected,HOLD,rollback`; `EXPECTATION` 與 `MEASURED` 不互換。

### WP-FHS-07｜Native PLAN Commander A/B/C（L2-r4:L467）

- **Original DependsOn**：`WP-FHS-01`, `WP-FHS-15`；硬／軟：受原 Consumer 的實際 Operation consumption 判定，未讀回 `EDGE_HARD_SOFT_OWNER_BIND_HOLD`。
- **Original L2 Effect 界線**：`LOCAL_DRAFT_WRITE`；原 WP 內合法唯讀 Help/Probe 和真 Host OPS 不可混為一個不可分 Gate。
- **Input／Guard**：WP01 Profile/Authority + WP15 三 SPEC/QuestionLedger/原 PLAN base_revision（不先要 WP06）；相同 `Subject/CandidateSHA/SourceSHA/Scope/HostID/PolicyEpoch` 有關聯時必一致。
- **Producer → 原 ABI/Reader → Consumer／Owner**：Portable Commander Guide Producer → 原 HGK PLAN Revision Writer；具體 `$id`、Reader/Host 路徑以當期原 Registry 為準，缺則 `RECEIVER_UNBOUND`。
- **Typed Output／能交付的 FUO**：A=唯讀 Guide；B=隔離 `PlanRevisionProposal`；C=原 PLAN Writer 的 CAS(expected_revision, proposal_sha) 回覆或具名 NACK。
- **POS（期待可觀測的 Reader 輸出）**：Proposal 不碰真 repo/queue，原 PLAN Reader 依相同 base revision 回明確 ACK/NACK。
- **NEG／SEC（不得被接受）**：以 legacy sbl-commander-sp 建新控制平面；要求先有新 WorkOrder 才能草擬 plan。
- **Expected FirstFail**：`WP-FHS-07.FIRST_FAIL:COMMANDER_BOOTSTRAP_INVERSION`。靜態本包尚未對原 Reader 注入此測例。
- **Hold／解鎖**：`ORIGINAL_PLAN_CAS_READER_HOLD`；由原受影 Owner/Reader 回送時期、Reader identity、來源 SHA、同 Scope 真 Raw/ACK 才解除。
- **Stop／Resume**：保留 same Subject/Candidate/Scope/source refs、first_fail、last_good/checkpoint；Reader 不可用時只 PARK 本 WP 的必要效果，不停來源讀取／隔離草案。
- **Rollback**：丟棄隔離 proposal；CAS conflict 回原 CurrentRevisionReader 重讀，非強蓋。
- **W2 Handoff**：若影響 W2:WP06/08，傳 `WP_ref,original_dependency_edge_refs,original_reader,receiver_abi,source_sha,candidate_sha,scope,host,policy_epoch,effect,permission_needed,firstfail,raw_or_expected,HOLD,rollback`; `EXPECTATION` 與 `MEASURED` 不互換。

### WP-FHS-11｜Portable Host Dogfood（L2-r4:L471）

- **Original DependsOn**：`WP-FHS-05`, `WP-FHS-16`；硬／軟：受原 Consumer 的實際 Operation consumption 判定，未讀回 `EDGE_HARD_SOFT_OWNER_BIND_HOLD`。
- **Original L2 Effect 界線**：`HOST_OP`；原 WP 內合法唯讀 Help/Probe 和真 Host OPS 不可混為一個不可分 Gate。
- **Input／Guard**：WP05 原 PIPD Reader/3 SP artifact + WP16 Donor/Method translation、各 Host install root/版本/license/OS；相同 `Subject/CandidateSHA/SourceSHA/Scope/HostID/PolicyEpoch` 有關聯時必一致。
- **Producer → 原 ABI/Reader → Consumer／Owner**：各原 Portable SP Packager、各 Host Loader/Skill Reader；具體 `$id`、Reader/Host 路徑以當期原 Registry 為準，缺則 `RECEIVER_UNBOUND`。
- **Typed Output／能交付的 FUO**：TPM／Commander Guide／External Challenge **各自** Selected→Installed→Loaded→Invoked→Used→Removed 的真 Host readback 預期；8 PIPD skills 另立矩陣。
- **POS（期待可觀測的 Reader 輸出）**：逐 Host 一 SP 一 trigger+nontrigger/exec/cleanup，不因同 repo 或同 launcher 自動列 3/3。
- **NEG／SEC（不得被接受）**：一份安裝回執冒三 SP 以及 8 skills；將 Challenge Maker 當 Protected Checker。
- **Expected FirstFail**：`WP-FHS-11.FIRST_FAIL:HOST_SP_MATRIX_INCOMPLETE`。靜態本包尚未對原 Reader 注入此測例。
- **Hold／解鎖**：`H-TOOLS-07 / HOST_SP_LOADER_UNBOUND`；由原受影 Owner/Reader 回送時期、Reader identity、來源 SHA、同 Scope 真 Raw/ACK 才解除。
- **Stop／Resume**：保留 same Subject/Candidate/Scope/source refs、first_fail、last_good/checkpoint；Reader 不可用時只 PARK 本 WP 的必要效果，不停來源讀取／隔離草案。
- **Rollback**：原 Host 自己 uninstall/disable/restore pin，記 residue；無法 unload 留具名 HOLD。
- **W2 Handoff**：若影響 W2:WP06/08，傳 `WP_ref,original_dependency_edge_refs,original_reader,receiver_abi,source_sha,candidate_sha,scope,host,policy_epoch,effect,permission_needed,firstfail,raw_or_expected,HOLD,rollback`; `EXPECTATION` 與 `MEASURED` 不互換。

### WP-FHS-17｜CAP-BOOT Native Occupants（L2-r4:L477）

- **Original DependsOn**：`WP-FHS-00`, `WP-FHS-02`, `WP-FHS-03`；硬／軟：受原 Consumer 的實際 Operation consumption 判定，未讀回 `EDGE_HARD_SOFT_OWNER_BIND_HOLD`。
- **Original L2 Effect 界線**：`HOST_OP`；原 WP 內合法唯讀 Help/Probe 和真 Host OPS 不可混為一個不可分 Gate。
- **Input／Guard**：WP00 Host source + WP02 原 Policy active/loaded+WP03 原 Issuer admitted；需要且缺的 CAP-BOOT occupant Source/Pin/License/Host/ACL；相同 `Subject/CandidateSHA/SourceSHA/Scope/HostID/PolicyEpoch` 有關聯時必一致。
- **Producer → 原 ABI/Reader → Consumer／Owner**：原 HGK Issuer + Original Host Installer/Capability Reader；具體 `$id`、Reader/Host 路徑以當期原 Registry 為準，缺則 `RECEIVER_UNBOUND`。
- **Typed Output／能交付的 FUO**：原 installer 的 ExactScope 原真 install/load/Consumer ACK 或 `CAPABILITY_GAP_HOLD`；**不得**以 W2 WP06 作前置。
- **POS（期待可觀測的 Reader 輸出）**：依原 Issuer/OPS ECP/Host ACL 安裝必要最小 occupant，原 Host 讀回 LoadedSHA/Invoked/Consumer Raw。
- **NEG／SEC（不得被接受）**：WP17 依 WP06、單靠 release/檔案存在當 Installed、無 license/owner ACK 偷設 Active。
- **Expected FirstFail**：`WP-FHS-17.FIRST_FAIL:CAP_BOOT_DEPENDENCY_INVERSION`。靜態本包尚未對原 Reader 注入此測例。
- **Hold／解鎖**：`H-ABI-05 / H-TOOLS-07 / CAPABILITY_GAP_HOLD`；由原受影 Owner/Reader 回送時期、Reader identity、來源 SHA、同 Scope 真 Raw/ACK 才解除。
- **Stop／Resume**：保留 same Subject/Candidate/Scope/source refs、first_fail、last_good/checkpoint；Reader 不可用時只 PARK 本 WP 的必要效果，不停來源讀取／隔離草案。
- **Rollback**：原 installer 撤銷、反向 Loaded→Installed→Absent、恢復 last-good，不用 git revert 作 OPS rollback。
- **W2 Handoff**：若影響 W2:WP06/08，傳 `WP_ref,original_dependency_edge_refs,original_reader,receiver_abi,source_sha,candidate_sha,scope,host,policy_epoch,effect,permission_needed,firstfail,raw_or_expected,HOLD,rollback`; `EXPECTATION` 與 `MEASURED` 不互換。

### WP-FHS-20｜CLI/Agent/Host Kind Matrix（L2-r4:L480）

- **Original DependsOn**：`WP-FHS-05`, `WP-FHS-16`；硬／軟：受原 Consumer 的實際 Operation consumption 判定，未讀回 `EDGE_HARD_SOFT_OWNER_BIND_HOLD`。
- **Original L2 Effect 界線**：`HOST_OP`；原 WP 內合法唯讀 Help/Probe 和真 Host OPS 不可混為一個不可分 Gate。
- **Input／Guard**：WP05 SBL PIPD Kind/Mode/Host schema+WP16 技術 translation；192 原 CellID/Raw ON/OFF、Owner；相同 `Subject/CandidateSHA/SourceSHA/Scope/HostID/PolicyEpoch` 有關聯時必一致。
- **Producer → 原 ABI/Reader → Consumer／Owner**：Original Kind/Mode/Host/Provider Cell Owner；具體 `$id`、Reader/Host 路徑以當期原 Registry 為準，缺則 `RECEIVER_UNBOUND`。
- **Typed Output／能交付的 FUO**：192 Cell 對 `Need/Host/Mode/ProviderToken` 的適用性、預設 occupant/NoFit 與各自 raw schema；此波只針對 W1 所需 Cell 做真受影 Host probe，其餘原身份交 W3。
- **POS（期待可觀測的 Reader 輸出）**：對該 Original Cell 同 Host/Mode/Token 取得原 Reader POS/NEG；不適用只可在原 Owner 證實下 NoFit。
- **NEG／SEC（不得被接受）**：拿 Claude/DeepSeek 原始 Raw 當 Hermes，私自把 ON/OFF 對映變已核准 bool。
- **Expected FirstFail**：`WP-FHS-20.FIRST_FAIL:HOST_CELL_EVIDENCE_FOREIGN`。靜態本包尚未對原 Reader 注入此測例。
- **Hold／解鎖**：`H-CELL-03 / H-TOOLS-07`；由原受影 Owner/Reader 回送時期、Reader identity、來源 SHA、同 Scope 真 Raw/ACK 才解除。
- **Stop／Resume**：保留 same Subject/Candidate/Scope/source refs、first_fail、last_good/checkpoint；Reader 不可用時只 PARK 本 WP 的必要效果，不停來源讀取／隔離草案。
- **Rollback**：切回同 Need 已 qualified occupant，還原配置/last-good，Owner 未決保持 GAP 而非自動「可選」。
- **W2 Handoff**：若影響 W2:WP06/08，傳 `WP_ref,original_dependency_edge_refs,original_reader,receiver_abi,source_sha,candidate_sha,scope,host,policy_epoch,effect,permission_needed,firstfail,raw_or_expected,HOLD,rollback`; `EXPECTATION` 與 `MEASURED` 不互換。

## 4. 原 L0／L2 唯一 S1–S5 SeamContract@design（P0 同 ID 同義原位修正）

**S0 僅是上游 Goal→TPM 三 SPEC 的 Pre-intake，並不是 S1 的新別名。S1–S5 完全沿用 L0 §04.2、L2 §3.1 身份；以下是作者端投影，無原 Registry `$id` 則 `ORIGINAL_SCHEMA_ID_UNBOUND`，不得憑設計名字冒原生 ABI。**

| SeamID | 原義（不可重編） | 主波 | Producer | 原 ABI／Reader | 原 Consumer | 受影輸入 | 預期候選 Output | FirstFail |
|---|---|---|---|---|---|---|---|---|
| S1 | Source／Intent／Profile → strict PI | W0/W1 | SBL TPM PM/SE/TPgM + SourceAuthority | 原 PIPD Intake/Authority/Profile 與 PI Reader | SBL-hosted 原 PI Writer | OriginalID/SourceSpan/SHA/Parent/NEG, 3 SPEC SHA, safety veto | strict PI-PKG（Sidecar 不進 Canonical） | S1_SOURCE_PI_AUTHORITY_NACK |
| S2 | PI → PD／ECP／TQAEP | W1 | SBL-hosted 原 PI Writer | 原 RepoContext PD Binder + ECP Effect Reader + TQAEP Case Reader | 原 PIPD PD/ECP/TQAEP Writer 與原 HGK 受影適配 Consumer | PI digest/Subject/Candidate/SourceSHA + local Git root/HEAD/dirty/untracked/preimage + OperationType + OracleRef | PD/DEV ECP/OPS ECP/Planned TQAEP 分出口 | S2_PI_PD_REPO_BIND_NACK |
| S3 | Native PLAN／Fabric Active Policy → HGK Admission | W1/W2 | 原 Native PLAN Producer + Fabric Policy Owner | 原 PLAN CurrentRevision/CAS Reader + Fabric ActiveEpoch/LoadedDigest Consumer Reader | HGK 原 Registry/Issuer/WorkOrder/Receiver | CAS base_revision/proposal_hash/Writer ACK + ActiveEpoch/LoadedSHA/ConsumerACK + Scope/HostID/Issuer ACL | 原 HGK admission／WorkID（僅實機原 Issuer 有權建立） | S3_PLAN_POLICY_ADMISSION_NACK |
| S4 | HGK WorkID → Hermes／Codex → WorldRaw | W2/W3 | HGK Original WorkID/SharedSpine/Lease | 原 Hermes v0.22.5 Dispatcher/Bounded Worker/Journal Reader | Original WorldRaw／Journal Consumer | OperationID/idempotency/LeaseGen/WorkerPID/ActualServed/Raw stdout stderr exit/diff | WorldRaw + checked journal cursor 或 UNKNOWN | S4_WORK_WORLD_RAW_NACK |
| S5 | Raw／Original Oracle → Protected Checker／Publisher | W2/W4 | Original WorldRaw + Case/Oracle Owner | 原 Protected Checker Reader（分離 principal） | Original Publisher／Release Consumer | 同 Subject/Candidate/Scope/Host/Epoch、OracleSHA、POS/NEG、Maker≠Checker | 獨立 verdict（若真執行）及 W4 Publisher readback | S5_CHECKER_PUBLISHER_SCOPE_NACK |


**具型別雙端校驗**：對每一 Seam 以 `subject_id/candidate_id/source_manifest_sha256/scope_id`（READ-only 可沒有 Candidate）+ `schema_id/version_from_original_reader_or_HOLD` + `receiver_version/actual_raw_sha` 做 join；NACK 先停受影寫操作、不創新 Issuer。`S1` 交 strict PI、`S2` 將 RepoContext PD/DEV-ECP/OPS-ECP/TQAEP 分離、`S3` **必有 Original PLAN CAS ACK 且 Fabric ActiveEpoch=HGK LoadedEpoch + Consumer ACK**，再交原 HGK Issuer。`S4/S5` 本波只規劃，不借 W2/W4 收據。

**五條 Seam 的不同拒收/退出**：
- `S1`：無原 Source／Atom 不准 PI promotion；READ/DRAFT 可續。FirstFail=`S1_SOURCE_PI_AUTHORITY_NACK`；失敗後由 `SBL-hosted 原 PI Writer` 的原 Reader 對應 Scope 重讀，禁止平行新 Writer。
- `S2`：Remote HEAD 不可冒本地；ECP intent 不發 Permit；Missing Runner 為局部 HOLD。FirstFail=`S2_PI_PD_REPO_BIND_NACK`；失敗後由 `原 PIPD PD/ECP/TQAEP Writer 與原 HGK 受影適配 Consumer` 的原 Reader 對應 Scope 重讀，禁止平行新 Writer。
- `S3`：無 PLAN CAS ACK 或 Active/Loaded mismatch 只能 PARK 受影 effect。FirstFail=`S3_PLAN_POLICY_ADMISSION_NACK`；失敗後由 `HGK 原 Registry/Issuer/WorkOrder/Receiver` 的原 Reader 對應 Scope 重讀，禁止平行新 Writer。
- `S4`：Selected/Invoked 不能冒 Served；UNKNOWN 先 reconcile。FirstFail=`S4_WORK_WORLD_RAW_NACK`；失敗後由 `Original WorldRaw／Journal Consumer` 的原 Reader 對應 Scope 重讀，禁止平行新 Writer。
- `S5`：Maker/CI/gstack ship 不具獨立檢查或發布權。FirstFail=`S5_CHECKER_PUBLISHER_SCOPE_NACK`；失敗後由 `Original Publisher／Release Consumer` 的原 Reader 對應 Scope 重讀，禁止平行新 Writer。

## 5. Canonical PIPD：13 CLI／19 Contract Families／8 Skills exact-set

**GitHub 唯讀定位（非本機 Host Loaded）**：`SBL/integrations/pipd/src/pipd_ls_sp/cli.py` 的 `COMMANDS` 定義 13 個；`registry.py` 的 `SOURCE_ORDER` 19 家族；`docs/pipd-migration/U04-CUTOVER.md` 記 U04 現役 Writer 及歷史庫 archive。真執行則要 original installed `pipd --help`, `pipd doctor`、原 schema registry SHA/CLI exit/error Raw。本包不調用現役 Compiler。

**原 13 CLI（source-order）**：`init`, `intake`, `profile`, `compile-pi`, `bind-pd`, `compile-ecp`, `compile-tqaep`, `validate`, `doctor`, `project`, `export`, `diff`, `repair`。第十四個 `compile-cc` **不在** exact-set；既有 `compile-ecp` 可以有受界 flag，不能據此新增動詞。

**原 19 Contract Families**：唯一現行名稱與順序以本稿「Product→PIPD」原 Registry `SOURCE_ORDER` exact-set 為準；末項必為 `ExecutionBindingRef`，其中 `GENIEProjectionRef`/`ExecutionBindingRef` 為原 Registry 註明的 seam-only family，不能自行 promoted 為已資格化的 Host binding。`GENIEProjectionRef`、`ExecutionBindingRef` 含 seam-only 限界，不可用欄名存在冒真 Host。

**8 原技能**：`pipd-route-intake`, `pipd-authority-source`, `pipd-profile-tailor`, `pipd-pi-compile`, `pipd-pd-bind`, `pipd-execution-contract`, `pipd-assurance-tqaep`, `pipd-package-project`。三 Portable SP 是別的 Host pack，不得互認 loaded receipt。

**PI 製程**：`Goal+Original Sources` → Intake、AuthoritySourceFreeze（每 family digest+locator）→ Profile 九軸安全 veto → strict PI nonempty original RequirementAtom（含 Parent/NEG/OriginalID）→ `SBL.PI.Crosswalk@2` 附加 sidecar；**PD** 僅由本地真 RepoProbe late bind；**ECP** 按 SOURCE_READ/DRAFT/DEV/OPS/USER/RELEASE 解析原 OperationRegistry；**TQAEP** 計畫每個受影 OriginalID/Case 的 POS/NEG、runner、Raw schema、checker identity，無原 Checker receipt 不提升 Qualified。`CR-DOC04-STATE-MAP` 的 T4/T5 當期未核不阻草稿，但阻 formal transition。受影缺原 Writer/Schema 標 `ORIGINAL_PIPD_PRE_V2_ROUTING_HOLD`。

## 6. Fabric Policy、HGK 與 Hermes：原生能力優先而不造第二控制層

**Fabric**：`Policy SourceSHA → Stage → OwnerApproval → ActiveEpoch → Original HGK Host LoadedDigest → Original Consumer ACK` 是不同 Reader 與時序；4 Mirror Subjects 維持原權威，FHS-NAV/v2 導航的 `effect_permission=NONE` 不提升。Source/Stage/文件成功不能充有效 Policy/Host Load；受影矛盾 `POLICY_LOADED_MISMATCH`。

**HGK**：唯一路徑為原 Registry/Resolver/Issuer → bound WorkID/TaskSpec/OperationID/Lease/Permit → original Receiver; 同 single Human Owner 仍要技術 Maker≠Checker、OS SID/ACL、short TTL/nonce/epoch。不能把 ECP、GitHub 提交或 Maker 流水線當 Issuer 授權。

**Hermes**：固定受治理 pin `v0.22.5`，重用原 Profiles/Kanban/Delegation/Swarm/Journal/Checkpoint/Queue，無第二 Scheduler；三 Lane PLAN/EXECUTE/AO 都須分記 `Required, Selected, Invoked, ActualServed`，真 PID/profile SHA、caller/provider Raw、tool turn 和實際起點。Managed Worker 的 frozen Profile 和 Prompt Delivered 要由原 Host 查，`Bound` 不代表 `Invoked/Used`。無人值守 `RunBudget@design` 只填 Host 真支持的 runtime/turn/cost/attempt/backoff/TTL/lease/wake/recovery，不虛造預設數；未知狀態先原 Reader reconcile、禁止非冪等盲重試。

## 7. Portable Host、預設啟用與 NoFit 的正確區分

`Native20 / Default30 / Donor24 / Method25 / TECH386` 是五個正交原身份集（485 個身份而不是 485 個必裝）；其中 legacy 規則及 OwnerPending 不是可執行 Tool。當 Need 被原產品要求為必備時採 `DESIGN_DEFAULT_REQUIRED`，可配置/可切換，但沒有 Qualified Host Occupant 就列 `CAPABILITY_GAP_HOLD`、不能改 OPTIONAL。替換前需要同 Need/Kind/Mode/Host/Scope 的具名、**已合格**後備及 Owner 決定，先世界 readback 再切換/Consumer POS+NEG、再退回 last-good，禁止空窗或雙 Issuer。

Portable TPM、Commander Guide、Acceptance Challenge 各自 `Selected → Installed → Loaded → Invoked → Used → Removed`，各按原 Host Skill Reader 執行 trigger/nontrigger、版本、OS/License/PID/Raw；八 PIPD skills 獨立矩陣。OpenSpec 只准作原 SPEC Delta 工具經 strict PIPD reparse，不是 canonical Writer；gstack 只作 QA Advisory，既不能簽 Independent PASS 也不能觸發 Publisher。

## 8. Program 局部拓樸、Stop/Resume 與 W2 初始準入

| W1 WP | 已知前置（原 L2） | 預計完成的最低 Reader output | 進 W2 的受影停止條件 |
|---|---|---|---|
| WP-FHS-02 | WP-FHS-01 | Source→Stage→OwnerApproved→ActiveEpoch→LoadedDigest→HGK ConsumerACK 六欄獨立的 `PolicyLoadedConsumerACK@design`；真值由原 Reader 回傳 | H-ABI-05 / FABRIC_EFFECTIVE_POLICY_READER_HOLD |
| WP-FHS-03 | WP-FHS-01 | `IssuerReceiverBinding@design` 及原 WorkID/Permit 的期待欄；未讀原 Issuer 收據僅 `ISSUER_UNBOUND` | H-ABI-05 / H-OS-08 |
| WP-FHS-04 | WP-FHS-00 | `WakeLeaseRuntimeBinding@design`：原 WorkID、wake、queue item、lease_generation、checkpoint_sha、journal_cursor、PID/profile_sha | H-LANE-06 / RUN_BUDGET_BIND_HOLD |
| WP-FHS-05 | WP-FHS-01 | 原 `IntentCard → SourceFreeze/Authority → ProfileBinding → PI-PKG(strict)` 與 `SBL.PI.Crosswalk@2` sidecar；真 RepoContext 綁 `PD-PKG`；DEV/OPS EC | H-PIPD-04 / ORIGINAL_PIPD_PRE_V2_ROUTING_HOLD / REPO_HEAD_BIND_HOLD |
| WP-FHS-07 | WP-FHS-01, WP-FHS-15 | A=唯讀 Guide；B=隔離 `PlanRevisionProposal`；C=原 PLAN Writer 的 CAS(expected_revision, proposal_sha) 回覆或具名 NACK | ORIGINAL_PLAN_CAS_READER_HOLD |
| WP-FHS-11 | WP-FHS-05, WP-FHS-16 | TPM／Commander Guide／External Challenge **各自** Selected→Installed→Loaded→Invoked→Used→Removed 的真 Host readback 預期；8 PIPD skills 另立矩陣 | H-TOOLS-07 / HOST_SP_LOADER_UNBOUND |
| WP-FHS-17 | WP-FHS-00, WP-FHS-02, WP-FHS-03 | 原 installer 的 ExactScope 原真 install/load/Consumer ACK 或 `CAPABILITY_GAP_HOLD`；**不得**以 W2 WP06 作前置 | H-ABI-05 / H-TOOLS-07 / CAPABILITY_GAP_HOLD |
| WP-FHS-20 | WP-FHS-05, WP-FHS-16 | 192 Cell 對 `Need/Host/Mode/ProviderToken` 的適用性、預設 occupant/NoFit 與各自 raw schema；此波只針對 W1 所需 Cell 做真受影 Host probe，其餘原身份交 W3 | H-CELL-03 / H-TOOLS-07 |

W1 的 READ/isolated DRAFT 在無 Host 時可建立完整候選和 `FirstFail`；**真正 Host/Repo Mutation 在本輪零執行**。W2 `WP-FHS-06` 只在原 `WP02/03/04/05/17` 的該 Operation 必須消費的前置 Readback/ACK 已有時開始 bounded DEV；沒有則 `W2_START_HOLD_AFFECTED_EFFECT`，不倒置 WP17。W2 `WP08` 還依 WP07，W2 `WP09` 依 WP08+W0 WP21；W3 仍負責 full 949/192/282/485 和 normal W18，W4 才有 cutover/Publisher。原 36 邊完整見 `03`。

**Stop Scope**：只 PARK 必須該原 Readback 的 Effect 子圖，不把 Source/Parser/離線 Draft 全域停工。**Resume**：same Subject/Candidate/SourceSHA/Scope/Host/PolicyEpoch、最後合法 Source/Preimage/Lease/Journal cursor；Scope/Host/Epoch 變更只重測受影 Case 和 Binding。**Rollback**：READ 重新讀、DRAFT 隔離清除、DEV 原 Git preimage/rollback commit、OPS 原 Installer/Host inverse（非 git revert）、USER Consent/compensation、RELEASE 原 Publisher reversible promotion；UNKNOWN 必先 reconcile。`DOC_AUTHOR_DONE` ≠ 產品FUO ≠ NativeDone ≠ ReleaseDone。


## 9. 原八 WP 的 OperationType／原 Reader／逐受影 Hard/Soft 與交付路由

**不變更 L2 原 WP Effect 列的代表性效果**；下列是同 WP 的受影操作級細分，`SOURCE_READ / LOCAL_DRAFT_WRITE / DEV_REPO_WRITE / HOST_OPS` 不是從路徑字串推斷，真 OperationType 仍由原 Effect Registry 裁決。對每一 WP，未綁的原 Schema/Host 只阻該操作，不把 READ/DRAFT 升成受保護 Gate。

### WP-FHS-02｜Fabric Policy Consumer：獨立操作分解

- **原依賴**：WP-FHS-01；OriginalConsumer=Fabric Policy Owner → HGK policy consumer。
- **Inputs／Pre**：Original Fabric Policy Owner/current epoch; applicable Policy manifest SHA; HGK original policy consumer process identity。
- **可見 Outputs／S5 預期讀回**：ActiveEpoch+LoadedDigest+ConsumerACK（由 Fabric+HGK 原 Reader 同 Subject 讀回）。
- **Operation types**：SOURCE_READ:Policy snapshot+active epoch probe；HOST_OPS:original Policy Consumer effective load/readback。
- **安全首敗**：`POLICY_EPOCH_LOADED_MISMATCH`；NEG=把未批准 Stage SHA 當 ActiveEpoch、HGK LoadedDigest 與 active 不符；EDGE=Owner 在 Stage 後切 epoch，舊 HGK process 尚載前 epoch；僅停受影 OPS，READ 繼續。
- **退出、續跑、回復 Owner**：原 Fabric/HGK Owner 以原 epoch migration/inverse 回 last-good，Stage 不可當 Active；僅原 Consumer/Host 有權以真 Raw 升級狀態。

### WP-FHS-03｜HGK Registry / Issuer：獨立操作分解

- **原依賴**：WP-FHS-01；OriginalConsumer=HGK Original Registry/Issuer/Receiver。
- **Inputs／Pre**：原 HGK Registry、OS PID/SID、scope/nonce/TTL/ProcessACL/PolicyEpoch，非 Maker credentials。
- **可見 Outputs／S5 預期讀回**：IssuerReceiverBinding+original typed refusal/ACK; no self-issued Permit。
- **Operation types**：SOURCE_READ:original Registry/Issuer contract/ACL probe；HOST_OPS:scoped issuer/receiver binding。
- **安全首敗**：`HGK_ISSUER_ACL_NONCE_TTL_NACK`；NEG=用不同 PID/SID、過期 nonce、重用 TTL 或 scope widening 要求原 Issuer 放行；EDGE=在授權後 Worker PID 重啟；原 Receiver 必以新 process ACL / nonce 再認，不借舊票。
- **退出、續跑、回復 Owner**：原 HGK Owner revoke affected grant/expire nonce, readback remaining WorkIDs，不清全域 Registry；僅原 Consumer/Host 有權以真 Raw 升級狀態。

### WP-FHS-04｜Hermes Durable Runtime：獨立操作分解

- **原依賴**：WP-FHS-00；OriginalConsumer=Hermes original Runtime/Journal + HGK SharedSpine。
- **Inputs／Pre**：Hermes v0.22.5 pin；ProfileSHA、WorkID、lease generation、run budget 原 Reader。
- **可見 Outputs／S5 預期讀回**：Fresh PID+LoadedProfileSHA+Raw三Lane Required/Selected/Invoked/ActualServed + JournalCursor。
- **Operation types**：SOURCE_READ:default profile/queue/journal capability probe；HOST_OPS:original runtime profile load/wake lease；LOCAL_DRAFT_WRITE:isolated restart plan。
- **安全首敗**：`HERMES_LEASE_UNKNOWN_RECONCILE`；NEG=以過期 lease_generation 重播非冪等 WorkID 並把 Picker Selected 假稱 ActualServed；EDGE=worker crash 在 effect 之後/Raw 入帳之前：維持 UNKNOWN，必 original World Reconcile。
- **退出、續跑、回復 Owner**：原 Journal 查 WorldRaw/last-good 再 Resume WorkID；UNKNOWN 禁盲重試；僅原 Consumer/Host 有權以真 Raw 升級狀態。

### WP-FHS-05｜PIPD Native Compiler：獨立操作分解

- **原依賴**：WP-FHS-01；OriginalConsumer=SBL-hosted original PIPD Compiler/Reader。
- **Inputs／Pre**：三份不同 SPECDraft、原 SourceManifest/Authority/Profile safety veto、原 PIPD Writer version。
- **可見 Outputs／S5 預期讀回**：非空 strict PI，真 RepoContext 才有 PD，DEV/OPS EffectIntent 分開，PlannedTQAEP 不冒 Checker。
- **Operation types**：SOURCE_READ:SBL integrations/pipd original registry+CLI probe；LOCAL_DRAFT_WRITE:strict candidate PI/sidecars in isolated root；DEV_REPO_WRITE:only if future admitted export to repo。
- **安全首敗**：`PIPD_STRICT_SCHEMA_OR_SOURCE_NACK`；NEG=把 _profile_meta 側掛塞進 strict PI；或憑 Caller HEAD 虛構本機 Repo binding；EDGE=PI SourceSHA 不變而 RepoHEAD 改變，只使 PD/ECP stale；不可偷重寫 PI requirement 原義。
- **退出、續跑、回復 Owner**：隔離候選刪除/回復 preimage；SourceSHA/HEAD 變更僅重編受影 PD/ECP；僅原 Consumer/Host 有權以真 Raw 升級狀態。

### WP-FHS-07｜Native PLAN Commander A/B/C：獨立操作分解

- **原依賴**：WP-FHS-01, WP-FHS-15；OriginalConsumer=原 HGK Native PLAN Writer/Reader。
- **Inputs／Pre**：W0 WP15 三 SPEC/QuestionLedger、PLAN base_revision、original Native PLAN CAS Reader。
- **可見 Outputs／S5 預期讀回**：PlanRevisionProposal + original CAS(base_revision, proposal_hash) ACK/NACK。
- **Operation types**：SOURCE_READ:original CurrentRevision and frozen SPEC；LOCAL_DRAFT_WRITE:isolated PlanRevisionProposal；HOST_OPS:only original CAS Writer confirmation。
- **安全首敗**：`PLAN_CAS_STALE_BASE`；NEG=跳過原 PLAN Writer 直接送 ECP→Issuer 或停用 legacy commander 提升成新 Gate；EDGE=兩個 proposal 同 base_revision 競逐，僅一個 Writer CAS 成功；另一個明確 NACK。
- **退出、續跑、回復 Owner**：CAS mismatch 丟棄提案並重讀 base；不寫 Target Repo/second Queue；僅原 Consumer/Host 有權以真 Raw 升級狀態。

### WP-FHS-11｜Portable Host Dogfood：獨立操作分解

- **原依賴**：WP-FHS-05, WP-FHS-16；OriginalConsumer=各 Host 原 Skill/Plugin Reader+每 SP original Consumer。
- **Inputs／Pre**：TPM-SP、Commander Guide-SP、Acceptance Challenge-SP 各自 artifact digest；Host compatibility+8 PIPD skills 各自 registry。
- **可見 Outputs／S5 預期讀回**：每 SP×Host 真 Loaded/Invoked/Used/nontrigger/Remove Raw；不共用收據。
- **Operation types**：SOURCE_READ:Host manifest and SP skill source；LOCAL_DRAFT_WRITE:per Host test plan；HOST_OPS:original Host loader installed/loaded/invoked/used/removal readback。
- **安全首敗**：`HOST_SKILL_TRIGGER_NONTRIGGER_NACK`；NEG=用 TPM-SP 的 Loaded SHA 冒 Challenge-SP；Maker 以模型結論簽 Protected Checker；EDGE=Installed 後 loader 未 Loaded，或 Loaded 但 nontrigger 仍被啟動：不得宣稱 Used。
- **退出、續跑、回復 Owner**：原 Host disable/remove entrypoint、還原 last-good manifest；清理 residue；僅原 Consumer/Host 有權以真 Raw 升級狀態。

### WP-FHS-17｜CAP-BOOT Native Occupants：獨立操作分解

- **原依賴**：WP-FHS-00, WP-FHS-02, WP-FHS-03；OriginalConsumer=原 HGK Issuer+Host Installer/Capability Registry。
- **Inputs／Pre**：NeedKey+scope、原 Policy Loaded ACK+HGK Issuer admitted installer+license/asset digest。
- **可見 Outputs／S5 預期讀回**：Needed Capability 之 Installed/Loaded/Invoked/ConsumerACK+last-good，NONE=CAPABILITY_GAP_HOLD。
- **Operation types**：SOURCE_READ:Need/qualified incumbent/Host installer provenance probe；HOST_OPS:minimum needed occupant original admitted install/load/invoke。
- **安全首敗**：`CAP_INSTALLER_ORIGIN_PARTIAL_ROLLBACK`；NEG=未有原 Issuer/Asset provenance 卻執行 Host installer；或第二套 Queue/Issuer 被包進工具；EDGE=Installer 解壓成功但載入失敗，需回上版 qualified last-good，不可把 Installed 當 Active。
- **退出、續跑、回復 Owner**：原 installer inverse/restore manifest+LoadedSHA+residue；不得 Git revert 取代 Host inverse；僅原 Consumer/Host 有權以真 Raw 升級狀態。

### WP-FHS-20｜CLI/Agent/Host Kind Matrix：獨立操作分解

- **原依賴**：WP-FHS-05, WP-FHS-16；OriginalConsumer=Original SBL Product×Host Cell owner/Reader。
- **Inputs／Pre**：CellID+original Kind/Mode/Host/RawToken，Host Capability/Provider state 原 Owner 必須核對。
- **可見 Outputs／S5 預期讀回**：Selected/NotAffected/OwnerHold per Cell + raw Host-specific Consumer outcome。
- **Operation types**：SOURCE_READ:original 192 Cell ledger, raw ON/OFF token, Host fit；LOCAL_DRAFT_WRITE:applicability selection/result matrix；HOST_OPS:affected Cell original Host reader probe when needed。
- **安全首敗**：`CELL_TOKEN_OWNER_MAP_UNBOUND`；NEG=把 ON/OFF source token 私譯成 provider_off bool 或借不同 Host/Provider Raw；EDGE=Same Kind/Mode 從 Hermes 改到 Codex，原 Cell ID 改變；舊 Cell receipt 不可重用。
- **退出、續跑、回復 Owner**：撤受影 Host adapter/probe，恢復同 Need qualified last-good，保留 raw ON/OFF；僅原 Consumer/Host 有權以真 Raw 升級狀態。

## 10. W1 設計接受與 W2 准入分層

`STATIC_STRUCTURE_DONE`: 50 CH／13 主責 CH／8 原 W1 WP／22 WP／36 DAG／24 DesignID／24 AssetID／19 families exact-order 與本版 2 MD 的實體可讀及 body-SHA 配對分別通過；結構檢查與來源語義核簽分立。
`PACKAGE_DELIVERY_COMPLETE`: **另**需 r5 ZIP 實體、ZIP CRC、member-bytes SHA 重新解壓讀回。歷史 `7 MD + manifest` 僅屬 `HISTORICAL_W1_R2_ONLY`，不是 r5 規範交付。
`W1_AUTHOR_BLUEPRINT_SUBSTANTIVE_ACCEPTABLE_FOR_DRAFTING`: Seam 身份一致＋W1 原句/Parent/NEG/Consumer 的**已定位**候選 SCL＋24 distinct capability test＋8 WP distinct SEC/EDGE＋雙向 typed handoff 與具名 HOLD。沒有原 OriginalID/Parent/Reader ACK 的行維持 `AFFECTED_SEMANTIC_HOLD`；不能宣稱正式全量 U0–U4。
`W1_DESIGN_ACCEPTANCE_PENDING_OWNER`: 任何必需原 Domain Reader 語義核簽、Host/ACL/Owner 未讀回仍需原權責接手。此條不阻 author-only 演進。
`AFFECTED_NATIVE_DONE`、`FULL_PKG_RELEASE_DONE`: W2/W4 原權責；本 ZIP 不能授權。

## W1-r5｜跨波接力 Typed Projection：W0→W1→W2/W3/W4 同 Subject/Scope（F08–F12）

**這些是作者端非權威投影欄位，不是新 Canonical Schema／新 WorkOrder／新 Issuer。** 每條 envelope 要記 `subject_id, candidate_sha, source_manifest_sha, OriginalID_or_HOLD, DesignID/subclaim_id, CH/WP, original_owner, original_receiver/ABI_or_HOLD, scope, HostID, PolicyEpoch, kind/mode/provider token(若適用), POS/NEG, expected_raw_schema_or_HOLD, original_reader_ACK_or_HOLD, last_good, first_fail, primary_wave, defer_reason`；`EXPECTED_NOT_OBSERVED` 不得改成 `MEASURED`。

| 路由 / Primary Wave | 受影原身份與內容 | Original Consumer／拒收測例 | 本波可交與必需 HOLD |
|---|---|---|---|
| W0→W1 / W0 WP15 | Product/Architecture/Program 三份 SHA 不同、QuestionLedger 和 31 源 SHA | 原 PIPD Intake；同 source 已知答案復用；三 SPEC 同文 → `W0_SPEC_ROLE_OR_SHA_NACK` | 同 Subject/Scope baseline 或 `W0_UPSTREAM_SHA_HOLD` |
| W1→W2 / W2 WP06 | WP02/03/04/05/17 合法前件、PI/PD/DEV ECP、Host cap、原 Policy+Issuer | 原 Repo/World Reader；Remote HEAD/Stage/Unloaded → `W2_START_HOLD_AFFECTED_EFFECT` | 只交 bounded effect candidate；真 admission/WorldRaw 由 W2 |
| W1→W2 / W2 WP08/09 | WP07 PLAN CAS ACK、WorkID/Lease、Expected Raw/TQAEP case | 原 HGK/Hermes/Protected Checker；UNKNOWN 盲重播 → `WORLD_RECONCILE_REQUIRED` | Maker 不能給 Checker receipt，`RUNNER_UNBOUND` |
| W1→W3 / W3 WP10 | B1 27 PI→31 PD 分裂映射、原 282 Cases 的逐原身份 | 原 B1 PI/PD/Case Reader；27 當 31 → `B1_SPLIT_EDGE_LOSS` | `W1ToW3AffectedProjection`，31 edge 原資格不由 W1 代簽 |
| W1→W3 / W3 WP12 | W18 fresh PID、ordinary Goal、E33–E42、3 Lane ActualServed | 原 Hermes normal entry/Host；只有 W1 PID → `W18_FOREIGN_HOST_EVIDENCE` | `EXPECTED_NOT_OBSERVED`，不得冒 W18 完成 |
| W1→W3 / W3 WP13 | 485 原 asset ID 正交；W1 24 slots，W0 Donor/Method 投影，W3 FullProduct | 原 Tech/Host Owner；未核 NoFit/License、PRE_READ 16 當 192 → `INAPPLICABLE_DENOMINATOR_PROMOTION` | 每個未於 W1 受影的 ID 在原域 W3 另結，不能默刪 |
| W1→W3 / W3 Product | 949/149/50 Parent/39/96/192/282 各自 applicability & Full/B1 投影 | 原 SBL Product/Case Reader；B1 66/254/629 覆蓋原 949 → `ORIGINAL_DENOMINATOR_LOSS` | `ORIG_OWNER_HOLD` 不能宣全量 U0–U4 已閉 |
| W1→W4 / W4 WP14 | 原 Provider/Host/CI/license/NOTICE/SBOM、S5 原 Checker→Publisher | 原 GHP-02/Publisher；gstack `/ship` 充 Release → `PUBLISHER_SCOPE_NACK` | `W1ToW4TraceExpectation`，全部 `EXPECTED_NOT_OBSERVED` |
| W1→W4 / W4 TraceClosure | 原 OriginalID/Parent/NEG/Oracle、Case/Evidence、affected rollback/residue | Original Trace/Checker/Publisher Reader；Maker 自簽 → `SELF_ATTESTED_CHECKER_NACK` | `W1ToW4TraceExpectation`：缺原 Reader ACK/Case 結尾保持受影 HOLD |

**機械 Join**：`(subject_id,candidate_sha,source_manifest_sha,scope,HostID,PolicyEpoch)` 與原 Receiver ABI/version 必一致；跨波 default `candidate` 僅設計草稿，讀來源可無 Candidate；原 Consumer 真 ACK 可局部提升單一 Scope。W3 禁用 W1 的 `PRE_READ_16` 升格 192/192；W4 禁用 Maker 的 CI/Gstack/ZIP 升格 Protected PASS。

### ASSET_DELEGATION_CONTRACT（每原資產身份的主責與 Need 消費分離）

`Native20=20 + Default30=30 + Donor24=24 + Method25=25 + TECH386=386 =485` 是**五個不相交身份清單**，不是 485 件必裝。W1 只擁有 24 OriginalAssetID（Native20 20／Default30 4）；其餘 `Default30` 26、Donor24 24、Method25 25、TECH386 386 的完整原 ID ledger由全波/各原 Owner 依各主波繼續，W1 只對真正 Need 有影響者採精確 `collection/original_asset_id/source_sha/primary_wave/needed_by_W1/original_consumer/POS/NEG/ExpectedQualification/NoFit/HOLD` 引用，絕不把沒有字串列在 W1 的項目視作已取消。

- `DEFAULT_REQUIRED_UNQUALIFIED`：原產品指定 default／mandatory 但 Host 不合格；保留義務，受影 effect `CAPABILITY_GAP_HOLD`，不可自動標 Optional。
- `QUALIFIED_ACTIVE`：需原 Host 同 Need/Kind/Mode/Scope `SELECTED/INSTALLED/LOADED/INVOKED/CONSUMER_USED`、原 Reader 正反結果、pin/license/OS/ACL/LastGood，才可啟用。
- `ORIGINAL_OWNER_NOFIT_HOLD`：原 Owner 判 NoFit/技術授權/Windows 支援不符；須有 qualified alternative + 原 Owner 選擇 + backout，缺則 HOLD。

每個 W1 24 Slot 的必要欄為 `source_sha, OriginalDisposition, NeedKey, Host/Kind/Mode, default occupant/immutable_pin/license, original_reader, POS/NEG, last_good/rollback, install/load/invoke/use/remove Raw`；現行各槽在下方 CH22 與 24 Slot 保留原名，未有真 Host Raw **皆不能標 `QUALIFIED_ACTIVE`**。OpenSpec 僅 Brownfield SpecDelta，gstack 僅 advisory；版本研究不等於 Windows install、載入或真 Publisher。

### Host 別化與權限／無人值守最小受影設計

四 Host (`Hermes`、`Codex`、`Claude Code`、`ChatGPT`) × 三 Portable SP (`TPM`、`Commander Guide`、`External Challenge`) 的 12 條記錄**每一條**要有 `HostKind/channel/loader_mode/module_origin+SHA/version/PID/trigger/nontrigger/removed/residue/original_consumer` 或 `HOST_SP_LOADER_UNBOUND`；8 PIPD Skill 是另一矩陣，不強制每 Host 具有同一 Skill loader，也不借不同主機的 Loaded Raw。Owner 是一位真人，但實際 Maker/Issuer/Checker/Publisher OS principal 仍分離；若不存在 `OwnerGrantRef` 原 Schema，使用原既有 grant command 或 `OWNER_GRANT_SCHEMA_HOLD`，不可創造新通行證。

Hermes 固定 v0.22.5，需實機 Probe 才能填 `RunBudget.turns/cost/attempts/backoff/TTL/lease/wake`，`FreshPID/LoadedProfileSHA/ActualServed/journal_cursor`。負例為崩潰於 effect 已發未 receipt、舊 lease、provider 選到非實際 served、credential/quota 失敗、非冪等盲 replay；只執行原 Host/Reader 准入的最小情境，`UNKNOWN` 必原 World reconcile 後才可 retry。這些 Fault Injection 設計不是本輪原實機已測。

## W1-r5｜Native-first／24 受影 AssetSlot／12 Portable Host 候選與 HotSwap

五個 **正交原集合**：Native20／Default30／Donor24／Method25／TECH386，各類保留原 identity/disposition，不混成安裝量或 485 個 mandatory installs。W1 可用的 24 受影來源資產 ≠ 全產品另外 461 個身份可刪；W3 原 Owner 仍需全量逐 ID disposition。本波需的 DesignDefault（含 OpenSpec Brownfield SpecDelta）**設計必備**，Host 未 Qualified 時記 `CAPABILITY_GAP_HOLD`，不得偷降 OPTIONAL。`Need → single qualified occupant/fit → original Host load/invoke → original Consumer POS/NEG → last-good/retire` 的每格須保留版本/license/pin、Host/OS/Scope、真證物；不能用候選文字冒已 Installed。

**當期版差**：Hermes 固定 v0.22.5；OpenSpec 研究可選 `v1.16.0`（2026-10-30 官方 Release）並依 Windows standalone 或 npm Node 22.12+ 選 pin；gstack `v1.92.55.0`〔HISTORICAL_R5_RESEARCH_NOT_CURRENT_SELECTION〕（2026-11-02）為研究候選且 Windows/Bun/Node/Privacy/Host 需實測；二者是方法/QA advisory，不能另造 Compiler/Checker/Publisher。真正 Host 預設版本、capability/no-fit 以原 Owner Registry 的受影 Raw 為準。

04｜Native-first 技術基座／受影 Asset／Host Slots 與 HotSwap

> **法位／聲明上限**：`FHS_PKG_WAVE_001 / L3_W1_AUTHOR_SIDE_BLUEPRINT_AND_SKELETON / AUTHOR_DESIGN_ONLY`。本交付不是 W1 草案／定案、SourceFreezeManifest、Canonical PI/PD/ECP/TQAEP、原 Issuer Permit、Host Loaded 證據、Native E2E、Protected Checker 或正式 Release。此處所有 POS/NEG/ACK/WorldRaw 均為 **期待的測例或原 Reader 介面設計**，不是本輪觀測到的驗收 PASS；原 Domain Writer/Owner/Consumer 不移轉，當期 Host/Owner 未回證則範圍局部 HOLD。

## 1. 五集合正交 + W1 受影切片（不是 485 個必裝）

完整原身份集合為 Native20 20、Default30 30、Donor24 24、Method25 25、TECH386 386＝485。**L2 §7.3 的 485 欄是設計期 asset route**；其中 LegacyRule160/OwnerPending65 是 TECH386 子集，非額外身份或必安裝 executable。W1 primary 為 **Native20 20 + Default30 4 = 24**，其餘 W0/W3 原主波只用 immutable Source/Dependency/Need 連結，不能偷改 W3 原資料。`Native20` 也包含 ROLE_WORKER / METHOD_FORMAT / PIPD / SBL 等不同 source types，不把「Native20」字樣誤判為 20 個 native singleton。

## 2. W1 24 個主責原 Asset 完整定位與原處置（保持 L2 原列）

以下每一行保留原 Asset OriginalID、原名、SourceType/Disposition 原字面、L1／FHS-BODY-08 精確 Locator、原 Consumer POS/NEG 和退出的 **來源連結**。這些位置只是索引；原 Type/Owner 候選不等同當期已 Qualified，具名 Need/Host 必由原 Reader 的來源 SHA 與 POS/NEG 證實。

| OriginalID / name | 原 SourceType／Disposition | 原跨源精確定位 | 原 Operation | Default/Occupant or Hold | 本 ID POS/NEG source locators |
|---|---|---|---|---|---|
| `Native20:CORE.FABRIC_POLICY` Fabric Policy Source/Consumer | ORIGINAL_NATIVE_SINGLETON / NATIVE_SINGLETON | L2:751; L1:L1473, FHS-BODY-08:L59 | W1 / ORIGINAL_NATIVE_READBACK | ORIGINAL_DOMAIN_SINGLETON_ONLY / OWNER_READER_QUALIFICATION_PENDING | 業務與專屬 NEG 原文 L1:L1475；POS/NEG 個別讀本卡 L1:L1478；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:CORE.HGK_NATIVE` HGK Protected Registry/Resolver/Issuer/Receiver | ORIGINAL_NATIVE_SINGLETON / NATIVE_SINGLETON | L2:752; L1:L1483, FHS-BODY-08:L76 | W1 / ORIGINAL_NATIVE_READBACK | ORIGINAL_DOMAIN_SINGLETON_ONLY / OWNER_READER_QUALIFICATION_PENDING | 業務與專屬 NEG 原文 L1:L1485；POS/NEG 個別讀本卡 L1:L1488；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:CORE.SHAREDSPINE` SQLite/journal/Lease | ORIGINAL_NATIVE_SINGLETON / NATIVE_SINGLETON | L2:753; L1:L1493, FHS-BODY-08:L93 | W1 / ORIGINAL_NATIVE_READBACK | ORIGINAL_DOMAIN_SINGLETON_ONLY / OWNER_READER_QUALIFICATION_PENDING | 業務與專屬 NEG 原文 L1:L1495；POS/NEG 個別讀本卡 L1:L1498；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:RUNTIME.HERMES` canonical Hermes | GOVERNED_RUNTIME / GOVERNED_RUNTIME | L2:754; L1:L1503, FHS-BODY-08:L110 | W1 / HOST_RUNTIME_LOAD_INVOKE | HERMES_V0.22.5_GOVERNED / OWNER_READER_QUALIFICATION_PENDING | 業務與專屬 NEG 原文 L1:L1505；POS/NEG 個別讀本卡 L1:L1508；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:LANE.PLAN.TPM` Native SBL-TPM／TPM Skill | ROLE_WORKER / ROLE_OR_WORKER | L2:755; L1:L1513, FHS-BODY-08:L127 | W1 / HOST_SKILL_OR_WORKER | ORIGINAL_HOST_OR_WORKER_READER / OWNER_READER_QUALIFICATION_PENDING | 業務與專屬 NEG 原文 L1:L1515；POS/NEG 個別讀本卡 L1:L1518；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:LANE.PLAN.COMMANDER` Native SBL Commander／Guide Skill | ROLE_WORKER / ROLE_OR_WORKER | L2:756; L1:L1523, FHS-BODY-08:L144 | W1 / HOST_SKILL_OR_WORKER | ORIGINAL_HOST_OR_WORKER_READER / OWNER_READER_QUALIFICATION_PENDING | 業務與專屬 NEG 原文 L1:L1525；POS/NEG 個別讀本卡 L1:L1528；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:LANE.EXECUTE.CODEX` Codex bounded Worker | ROLE_WORKER / ROLE_OR_WORKER | L2:757; L1:L1533, FHS-BODY-08:L161 | W1 / HOST_SKILL_OR_WORKER | ORIGINAL_HOST_OR_WORKER_READER / OWNER_READER_QUALIFICATION_PENDING | 業務與專屬 NEG 原文 L1:L1535；POS/NEG 個別讀本卡 L1:L1538；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:LANE.VERIFY.CHALLENGE` SBL External Challenge＋Protected Checker | ROLE_WORKER / ROLE_OR_WORKER | L2:758; L1:L1543, FHS-BODY-08:L178 | W1 / HOST_SKILL_OR_WORKER | ORIGINAL_HOST_OR_WORKER_READER / OWNER_READER_QUALIFICATION_PENDING | 業務與專屬 NEG 原文 L1:L1545；POS/NEG 個別讀本卡 L1:L1548；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:METHOD.FAR` Fabric Autonomous Research | METHOD_FORMAT / METHOD_OR_FORMAT | L2:759; L1:L1553, FHS-BODY-08:L195 | W1 / ADVISORY_METHOD_OR_CLI | ORIGINAL_METHOD_CONSUMER_ONLY / OWNER_READER_QUALIFICATION_PENDING | 業務與專屬 NEG 原文 L1:L1555；POS/NEG 個別讀本卡 L1:L1558；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:METHOD.KANBAN` existing Hermes kanban | METHOD_FORMAT / METHOD_OR_FORMAT | L2:760; L1:L1563, FHS-BODY-08:L212 | W1 / ADVISORY_METHOD_OR_CLI | ORIGINAL_METHOD_CONSUMER_ONLY / OWNER_READER_QUALIFICATION_PENDING | 業務與專屬 NEG 原文 L1:L1565；POS/NEG 個別讀本卡 L1:L1568；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:METHOD.SWARM` bounded delegate | METHOD_FORMAT / METHOD_OR_FORMAT | L2:761; L1:L1573, FHS-BODY-08:L229 | W1 / ADVISORY_METHOD_OR_CLI | ORIGINAL_METHOD_CONSUMER_ONLY / OWNER_READER_QUALIFICATION_PENDING | 業務與專屬 NEG 原文 L1:L1575；POS/NEG 個別讀本卡 L1:L1578；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:METHOD.OPENSPEC` Fission-AI OpenSpec | METHOD_FORMAT / METHOD_OR_FORMAT | L2:762; L1:L1583, FHS-BODY-08:L246 | W1 / ADVISORY_METHOD_OR_CLI | OPENSPEC_V1.16.0_TARGET__HOST_PENDING / OWNER_READER_QUALIFICATION_PENDING | 業務與專屬 NEG 原文 L1:L1585；POS/NEG 個別讀本卡 L1:L1588；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:METHOD.GSTACK` gstack workflow | METHOD_FORMAT / METHOD_OR_FORMAT | L2:763; L1:L1593, FHS-BODY-08:L263 | W1 / ADVISORY_METHOD_OR_CLI | HISTORICAL_R5_GSTACK_V1.92.55.0_SUPERSEDED_CURRENT_1.95.5.0 / PIN_AND_HOST_FIT_PENDING | 業務與專屬 NEG 原文 L1:L1595；POS/NEG 個別讀本卡 L1:L1598；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:METHOD.SUPERPOWERS` obra Superpowers | METHOD_FORMAT / METHOD_OR_FORMAT | L2:764; L1:L1603, FHS-BODY-08:L280 | W1 / ADVISORY_METHOD_OR_CLI | ORIGINAL_METHOD_CONSUMER_ONLY / OWNER_READER_QUALIFICATION_PENDING | 業務與專屬 NEG 原文 L1:L1605；POS/NEG 個別讀本卡 L1:L1608；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:METHOD.SPEC_KIT` GitHub Spec Kit | METHOD_FORMAT / METHOD_OR_FORMAT | L2:765; L1:L1613, FHS-BODY-08:L297 | W1 / ADVISORY_METHOD_OR_CLI | ORIGINAL_METHOD_CONSUMER_ONLY / OWNER_READER_QUALIFICATION_PENDING | 業務與專屬 NEG 原文 L1:L1615；POS/NEG 個別讀本卡 L1:L1618；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:METHOD.MATTP_SKILLS` Matt Pocock Skills | METHOD_FORMAT / METHOD_OR_FORMAT | L2:766; L1:L1623, FHS-BODY-08:L314 | W1 / ADVISORY_METHOD_OR_CLI | ORIGINAL_METHOD_CONSUMER_ONLY / OWNER_READER_QUALIFICATION_PENDING | 業務與專屬 NEG 原文 L1:L1625；POS/NEG 個別讀本卡 L1:L1628；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:METHOD.GSD` Get Shit Done donor（來源中的 GSD 名稱） | METHOD_FORMAT / METHOD_OR_FORMAT | L2:767; L1:L1633, FHS-BODY-08:L331 | W1 / ADVISORY_METHOD_OR_CLI | ORIGINAL_METHOD_CONSUMER_ONLY / OWNER_READER_QUALIFICATION_PENDING | 業務與專屬 NEG 原文 L1:L1635；POS/NEG 個別讀本卡 L1:L1638；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:METHOD.FABRIC_COMPRESS` 知識/Prompt/Skill 壓製 | METHOD_FORMAT / METHOD_OR_FORMAT | L2:768; L1:L1643, FHS-BODY-08:L348 | W1 / ADVISORY_METHOD_OR_CLI | ORIGINAL_METHOD_CONSUMER_ONLY / OWNER_READER_QUALIFICATION_PENDING | 業務與專屬 NEG 原文 L1:L1645；POS/NEG 個別讀本卡 L1:L1648；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:PIPD.P4` PIPD-LS-SP Public Skills+CLI | ORIGINAL_OWNER_COMPONENT / OWNER_COMPONENT | L2:769; L1:L1653, FHS-BODY-08:L365 | W1 / ORIGINAL_OWNER_READER_ROUTE | SBL/integrations/pipd/ (historical PIPD-LS-SP archived) / ORIGINAL_WRITER_IN_SBL_C4_CLOSED_SCOPED__HOST_UNVERI | 業務與專屬 NEG 原文 L1:L1655；POS/NEG 個別讀本卡 L1:L1658；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Native20:SBL.PRODUCT` SBL Shared Core+Three SP | ORIGINAL_OWNER_COMPONENT / OWNER_COMPONENT | L2:770; L1:L1664, FHS-BODY-08:L382 | W1 / ORIGINAL_OWNER_READER_ROUTE | ORIGINAL_DOMAIN_WRITER_READER / OWNER_READER_QUALIFICATION_PENDING | 業務與專屬 NEG 原文 L1:L1666；POS/NEG 個別讀本卡 L1:L1669；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Default30:P0-TOOL-001` Hermes Agent | DESIGN_DEFAULT_NEED / DEFAULT_ENABLED_AFTER_QUALIFICATION | L2:771; L1:L1724, FHS-BODY-08:L400 | W1 / HOST_ADOPTION_BY_ASSET_TYPE | PREFERRED_ORIGINAL_OCCUPANT_PENDING__QUALIFIED_FALLBACK_IF_PROVEN / DESIGN_DEFAULT_REQUIRED__SOURCE_LICENSE_HO | 業務與專屬 NEG 原文 L1:L1726；POS/NEG 個別讀本卡 L1:L1729；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Default30:P0-TOOL-005` Codex | DESIGN_DEFAULT_NEED / DEFAULT_ENABLED_AFTER_QUALIFICATION | L2:775; L1:L1764, FHS-BODY-08:L448 | W1 / HOST_ADOPTION_BY_ASSET_TYPE | PREFERRED_ORIGINAL_OCCUPANT_PENDING__QUALIFIED_FALLBACK_IF_PROVEN / DESIGN_DEFAULT_REQUIRED__SOURCE_LICENSE_HO | 業務與專屬 NEG 原文 L1:L1766；POS/NEG 個別讀本卡 L1:L1769；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Default30:P0-TOOL-062` GitHub Actions | DESIGN_DEFAULT_NEED / DEFAULT_ENABLED_AFTER_QUALIFICATION | L2:795; L1:L1964, FHS-BODY-08:L688 | W1 / HOST_ADOPTION_BY_ASSET_TYPE | PREFERRED_ORIGINAL_OCCUPANT_PENDING__QUALIFIED_FALLBACK_IF_PROVEN / DESIGN_DEFAULT_REQUIRED__SOURCE_LICENSE_HO | 業務與專屬 NEG 原文 L1:L1966；POS/NEG 個別讀本卡 L1:L1969；原 Runner/Case 未綁=CASE_BIND_HOLD |
| `Default30:P0-TOOL-072` SQLite | DESIGN_DEFAULT_NEED / DEFAULT_ENABLED_AFTER_QUALIFICATION | L2:800; L1:L2014, FHS-BODY-08:L748 | W1 / HOST_ADOPTION_BY_ASSET_TYPE | PREFERRED_ORIGINAL_OCCUPANT_PENDING__QUALIFIED_FALLBACK_IF_PROVEN / DESIGN_DEFAULT_REQUIRED__SOURCE_LICENSE_HO | 業務與專屬 NEG 原文 L1:L2016；POS/NEG 個別讀本卡 L1:L2019；原 Runner/Case 未綁=CASE_BIND_HOLD |

## 3. W1 24 個 OriginalAssetID 各別可用的 Need／Pin／Host／Consumer／POS／NEG（r2 完整原位取代模板）

**原位版本規則**：OriginalID/SourceType/OriginalDisposition 保持 L1 CH-22／23 與 L2 當期作者端身份，不因同 NeedKey 去重而抹掉來源。`FormalName` 不得再有 ``；`VersionPin` 對有來源者依來源明列、其餘 `PIN_UNBOUND`；`License/Windows/HostLoader` 沒有正式來源時記具名 `LICENSE_HOST_READ_HOLD`，不可從 Package 名稱推定已安裝、也不可用 Repository LICENSE 假定依附工具全部授權。

### 3.1 跨集合可維護 NeedKey（適用 Scope 下最多一位 qualified occupant）

| NeedKey (Kind/Mode/Host/Scope 待原 Reader 綁) | 24 個 OriginalID（不合併血緣） | Occupancy Decision | MANDATED DEFAULT 與退出 |
|---|---|---|---|
| FABRIC_POLICY_EFFECTIVE | Native20:CORE.FABRIC_POLICY | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | ORIGINAL_SINGLETON_NOT_REPLACEABLE |
| HGK_SINGLE_ISSUER | Native20:CORE.HGK_NATIVE | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | ORIGINAL_SINGLETON_NOT_REPLACEABLE |
| HGK_SHAREDSPINE_DURABLE | Native20:CORE.SHAREDSPINE, Default30:P0-TOOL-072 | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | DESIGN_DEFAULT_REQUIRED / NO_OPTIONAL_DOWNGRADE |
| HERMES_DURABLE_RUNTIME | Native20:RUNTIME.HERMES, Native20:METHOD.KANBAN, Native20:METHOD.SWARM, Default30:P0-TOOL-001 | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | DESIGN_DEFAULT_REQUIRED / NO_OPTIONAL_DOWNGRADE |
| SBL_TPM_THREE_SPECS | Native20:LANE.PLAN.TPM | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | REUSE_EXISTING_BEFORE_INSTALL |
| HGK_PLAN_CAS | Native20:LANE.PLAN.COMMANDER | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | REUSE_EXISTING_BEFORE_INSTALL |
| BOUNDED_CODE_WORKER | Native20:LANE.EXECUTE.CODEX, Default30:P0-TOOL-005 | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | DESIGN_DEFAULT_REQUIRED / NO_OPTIONAL_DOWNGRADE |
| PROTECTED_ASSURANCE_CHAIN | Native20:LANE.VERIFY.CHALLENGE | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | REUSE_EXISTING_BEFORE_INSTALL |
| SOURCE_BOUND_RESEARCH | Native20:METHOD.FAR | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | REUSE_EXISTING_BEFORE_INSTALL |
| SOURCE_SPEC_DIFF | Native20:METHOD.OPENSPEC | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | REUSE_EXISTING_BEFORE_INSTALL |
| MAKER_REVIEW_QA | Native20:METHOD.GSTACK | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | REUSE_EXISTING_BEFORE_INSTALL |
| METHOD_TDD_DEBUG | Native20:METHOD.SUPERPOWERS | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | REUSE_EXISTING_BEFORE_INSTALL |
| METHOD_GREENFIELD_SPEC | Native20:METHOD.SPEC_KIT | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | REUSE_EXISTING_BEFORE_INSTALL |
| QUESTION_LEDGER_REUSE | Native20:METHOD.MATTP_SKILLS | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | REUSE_EXISTING_BEFORE_INSTALL |
| METHOD_PROGRAM_RESUME | Native20:METHOD.GSD | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | REUSE_EXISTING_BEFORE_INSTALL |
| SOURCE_BOUND_TRANSLATION | Native20:METHOD.FABRIC_COMPRESS | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | REUSE_EXISTING_BEFORE_INSTALL |
| PIPD_SBL_CANONICAL_COMPILER | Native20:PIPD.P4 | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | REUSE_EXISTING_BEFORE_INSTALL |
| SBL_SHAREDCORE_PRODUCT | Native20:SBL.PRODUCT | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | REUSE_EXISTING_BEFORE_INSTALL |
| CI_GITHUB_WORKFLOW | Default30:P0-TOOL-062 | ONE_QUALIFIED_ORIGINAL_OCCUPANT_PER_AFFECTED_HOST_SCOPE; NOW_UNOBSERVED | DESIGN_DEFAULT_REQUIRED / NO_OPTIONAL_DOWNGRADE |


**去重規則**：`HERMES_DURABLE_RUNTIME` 將 `Native20:RUNTIME.HERMES`、`Native20:METHOD.KANBAN`、`Native20:METHOD.SWARM`、`Default30:P0-TOOL-001` 對同一 Host/Scope 識別為已存在 Hermes 原生能力族，不重裝 4 個 Agent；`HGK_SHAREDSPINE_DURABLE` 將 `CORE.SHAREDSPINE` 與 `Default30:P0-TOOL-072 SQLite` 綁同一原 schema；`BOUNDED_CODE_WORKER` 合併 Codex Worker 原 role 與 default tool identity，但 Writer 許可仍唯一原 HGK；同一 Need 若 Key/Host/Kind/Mode 不一致則分開原域決策，不自動跨 Host 借 PASS。

### AssetSlot `Native20:CORE.FABRIC_POLICY`｜Fabric Policy Source/Consumer（NATIVE_SINGLETON; original-source pin / LICENSE_OWNER_READER_HOLD）

- **原字節來源／原處置**：`FHS-BODY-08:L61` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`7d361360215b0ca975a1c81d35f03207d69039e096f102aadb08717779eccdec`；L1 CH22/23 OriginalID 原字面 `Native20:CORE.FABRIC_POLICY`。SourceType=`NATIVE_SINGLETON`，`OriginalDisposition=NATIVE_SINGLETON`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`FABRIC_POLICY_EFFECTIVE` × `FABRIC` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=Policy source/epoch referenced by governed effect；Producer=Fabric Policy Source/Consumer 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=Policy Stage/ActiveEpoch/LoadedSHA/ACK separate; same epoch must match。OriginalConsumer=`Fabric original Policy Reader → HGK policy consumer`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：Stage or github mirror as Active; second policy control plane。`FirstFail=ASSET.Native20:CORE.FABRIC_POLICY.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：original-source pin / LICENSE_OWNER_READER_HOLD；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`NATIVE_SINGLETON_READBACK: original owner current ABI/epoch + downstream Consumer ACK; no installer/uninstall required`；Case alias=`DESIGN.ASSET.Native20:CORE.FABRIC_POLICY`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`NON_REPLACEABLE_ORIGINAL_SINGLETON`；rollback=`OWNER_MIGRATE_EPOCH`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:CORE.HGK_NATIVE`｜HGK Protected Registry/Resolver/Issuer/Receiver（NATIVE_SINGLETON; original source/export / LICENSE_OWNER_READER_HOLD）

- **原字節來源／原處置**：`FHS-BODY-08:L78` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`6176c36bbc9cd756b2aef9e2f2163c9a9f24a1b79fee6ddbd310293d52028f7d`；L1 CH22/23 OriginalID 原字面 `Native20:CORE.HGK_NATIVE`。SourceType=`NATIVE_SINGLETON`，`OriginalDisposition=NATIVE_SINGLETON`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`HGK_SINGLE_ISSUER` × `HGK` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=operation requests original HGK admission；Producer=HGK Protected Registry/Resolver/Issuer/Receiver 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=same scope nonce TTL process ACL gives one original issuer decision。OriginalConsumer=`HGK Original Registry/Issuer/Receiver`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：maker generated Permit/second issuer/expired nonce。`FirstFail=ASSET.Native20:CORE.HGK_NATIVE.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：original source/export / LICENSE_OWNER_READER_HOLD；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`NATIVE_SINGLETON_READBACK: original owner current ABI/epoch + downstream Consumer ACK; no installer/uninstall required`；Case alias=`DESIGN.ASSET.Native20:CORE.HGK_NATIVE`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`NON_REPLACEABLE_ORIGINAL_SINGLETON`；rollback=`OWNER_REVOKE_OR_MIGRATE`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:CORE.SHAREDSPINE`｜SQLite/journal/Lease（NATIVE_SINGLETON; original local schema / LICENSE_OWNER_READER_HOLD）

- **原字節來源／原處置**：`FHS-BODY-08:L95` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`b94e7bd9c2ae24261fd8c4a72333fa6ec2e8f3a4604e85219a619345ba0bbda9`；L1 CH22/23 OriginalID 原字面 `Native20:CORE.SHAREDSPINE`。SourceType=`NATIVE_SINGLETON`，`OriginalDisposition=NATIVE_SINGLETON`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`HGK_SHAREDSPINE_DURABLE` × `HGK` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=durable resumed work/journal inspection；Producer=SQLite/journal/Lease 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=WorkID/lease generation/cursor survive restart without duplicate effect。OriginalConsumer=`HGK SharedSpine/Journal Reader`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：new SQLite queue or stale lease duplicate work。`FirstFail=ASSET.Native20:CORE.SHAREDSPINE.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：original local schema / LICENSE_OWNER_READER_HOLD；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`NATIVE_SINGLETON_READBACK: original owner current ABI/epoch + downstream Consumer ACK; no installer/uninstall required`；Case alias=`DESIGN.ASSET.Native20:CORE.SHAREDSPINE`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`NON_REPLACEABLE_ORIGINAL_SINGLETON`；rollback=`OWNER_SCHEMA_MIGRATION`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:RUNTIME.HERMES`｜canonical Hermes（HOST_RUNTIME; v0.22.5 pinned / upstream licence check on exact origin）

- **原字節來源／原處置**：`FHS-BODY-08:L112` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`0e6717248121efd8ce407b63dade94d9f4796844c1911db103ad4c5c5540d936`；L1 CH22/23 OriginalID 原字面 `Native20:RUNTIME.HERMES`。SourceType=`HOST_RUNTIME`，`OriginalDisposition=GOVERNED_RUNTIME`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`HERMES_DURABLE_RUNTIME` × `HERMES` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=ordinary goal requires execution and checkpoint；Producer=canonical Hermes 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=fresh PID/profile SHA/real three-lane served+tool Raw。OriginalConsumer=`Hermes Native Runtime Owner + HGK dispatcher`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：selected/loaded assumed actually served or test daemon substituted。`FirstFail=ASSET.Native20:RUNTIME.HERMES.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：v0.22.5 pinned / upstream licence check on exact origin；`immutable_commit/asset_sha256=HERMES_V0.22.5_PINNED_SOURCE_CONFIRMATION_REQUIRED`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`RUNTIME_HOST: original fresh PID/profile SHA/three lane ActualServed/tool/WorldRaw + restart journal`；Case alias=`DESIGN.ASSET.Native20:RUNTIME.HERMES`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`USE_NATIVE_IF_FIT; method-only not automatically installed`；rollback=`ORIGINAL_RUNTIME_RESTART`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:LANE.PLAN.TPM`｜Native SBL-TPM／TPM Skill（HOST_SKILL_OR_WORKER; source SHA / TPM-SP package owner）

- **原字節來源／原處置**：`FHS-BODY-08:L129` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`8f54c668d165442bc24ff62ddc6c2a0c130c57dfaf7d25d341bc18bda3048282`；L1 CH22/23 OriginalID 原字面 `Native20:LANE.PLAN.TPM`。SourceType=`HOST_SKILL_OR_WORKER`，`OriginalDisposition=ROLE_OR_WORKER`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`SBL_TPM_THREE_SPECS` × `SBL TPM Host` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=SPEC_CHANGE / W0 three SPEC handoff；Producer=Native SBL-TPM／TPM Skill 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=independent Product/Architecture/Program SPECDrafts source-bound。OriginalConsumer=`SBL TPM Product/System/Program Consumers`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：one generic draft replaces all three or PM signatures become permit。`FirstFail=ASSET.Native20:LANE.PLAN.TPM.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：source SHA / TPM-SP package owner；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`HOST_SKILL_TRIGGER: independent installed/loaded/invoked/used AND negative nontrigger/removed; no borrowed receipt`；Case alias=`DESIGN.ASSET.Native20:LANE.PLAN.TPM`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`USE_NATIVE_IF_FIT; method-only not automatically installed`；rollback=`HOST_REMOVE_SKILL_ONLY`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:LANE.PLAN.COMMANDER`｜Native SBL Commander／Guide Skill（HOST_SKILL_OR_WORKER; original PLAN receiver ABI / OWNER_READER_HOLD）

- **原字節來源／原處置**：`FHS-BODY-08:L146` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`e77881eac34e7d9cc99013a56c720973bbb0bc24b163b9a78a52b0fc35f21a96`；L1 CH22/23 OriginalID 原字面 `Native20:LANE.PLAN.COMMANDER`。SourceType=`HOST_SKILL_OR_WORKER`，`OriginalDisposition=ROLE_OR_WORKER`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`HGK_PLAN_CAS` × `HGK Native PLAN` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=governed change needs plan revision；Producer=Native SBL Commander／Guide Skill 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=read-only Guide proposes plan; original CAS ACK on base_revision。OriginalConsumer=`HGK original Native PLAN CAS Reader`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：legacy disabled Commander becomes second Gate; CAS bypass。`FirstFail=ASSET.Native20:LANE.PLAN.COMMANDER.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：original PLAN receiver ABI / OWNER_READER_HOLD；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`HOST_SKILL_TRIGGER: independent installed/loaded/invoked/used AND negative nontrigger/removed; no borrowed receipt`；Case alias=`DESIGN.ASSET.Native20:LANE.PLAN.COMMANDER`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`USE_NATIVE_IF_FIT; method-only not automatically installed`；rollback=`RESTORE_PLAN_BASE`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:LANE.EXECUTE.CODEX`｜Codex bounded Worker（CLI_WORKER; ORIGINAL_HOST_CLI_PIN_HOLD）

- **原字節來源／原處置**：`FHS-BODY-08:L163` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`6a24d51fb622440cf734478bd6d208c85cb4a46e08547da1a0136fa2a15e4497`；L1 CH22/23 OriginalID 原字面 `Native20:LANE.EXECUTE.CODEX`。SourceType=`CLI_WORKER`，`OriginalDisposition=ROLE_OR_WORKER`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`BOUNDED_CODE_WORKER` × `Codex/Hermes` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=authorized DEV repository change；Producer=Codex bounded Worker 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=same WriteSet code task produces exit/diff/raw。OriginalConsumer=`Hermes delegated Worker / HGK original executor registry`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：outside scope repo write or claimed model≠actual served。`FirstFail=ASSET.Native20:LANE.EXECUTE.CODEX.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：ORIGINAL_HOST_CLI_PIN_HOLD；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`CLI_RUN: binary SHA/version, argv/exit/stdout/stderr, WriteSet+original Host invoke; failure exit & cleanup`；Case alias=`DESIGN.ASSET.Native20:LANE.EXECUTE.CODEX`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`USE_NATIVE_IF_FIT; method-only not automatically installed`；rollback=`RESTORE_REPO_PREIMAGE`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:LANE.VERIFY.CHALLENGE`｜SBL External Challenge＋Protected Checker（HOST_SKILL_OR_WORKER; ORIGINAL_CHECKER_REGISTRY_HOLD）

- **原字節來源／原處置**：`FHS-BODY-08:L180` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`d46d112b11bd852c2f12d5cbf5f15a022b36bbfe8e91e65e88613c6e5ca2f21f`；L1 CH22/23 OriginalID 原字面 `Native20:LANE.VERIFY.CHALLENGE`。SourceType=`HOST_SKILL_OR_WORKER`，`OriginalDisposition=ROLE_OR_WORKER`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`PROTECTED_ASSURANCE_CHAIN` × `original Checker/Host` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=affected external challenge after world raw；Producer=SBL External Challenge＋Protected Checker 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=per-case POS/NEG proposal separated from independent checker verdict。OriginalConsumer=`Maker Challenge plan → protected original Checker`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：same Maker key signs independent PASS。`FirstFail=ASSET.Native20:LANE.VERIFY.CHALLENGE.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：ORIGINAL_CHECKER_REGISTRY_HOLD；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`HOST_SKILL_TRIGGER: independent installed/loaded/invoked/used AND negative nontrigger/removed; no borrowed receipt`；Case alias=`DESIGN.ASSET.Native20:LANE.VERIFY.CHALLENGE`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`USE_NATIVE_IF_FIT; method-only not automatically installed`；rollback=`ORIGINAL_CHECKER_REASSESS`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:METHOD.FAR`｜Fabric Autonomous Research（METHOD; METHOD_SOURCE_SHA / not a binary）

- **原字節來源／原處置**：`FHS-BODY-08:L197` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`297ebae41b668e8d97641570a2d214015a4b8a0fd3650a0336a39ba485aebc13`；L1 CH22/23 OriginalID 原字面 `Native20:METHOD.FAR`。SourceType=`METHOD`，`OriginalDisposition=METHOD_OR_FORMAT`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`SOURCE_BOUND_RESEARCH` × `Fabric/Research` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=source question or NoFit research；Producer=Fabric Autonomous Research 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=source/issue→bounded research result with citations and consumer。OriginalConsumer=`Fabric FAR / source research consumer`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：research answer projected as loaded policy/authorization。`FirstFail=ASSET.Native20:METHOD.FAR.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：METHOD_SOURCE_SHA / not a binary；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`METHOD_OUTPUT: bounded source input → method/decision → original Consumer output; no fictitious binary uninstall`；Case alias=`DESIGN.ASSET.Native20:METHOD.FAR`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`USE_NATIVE_IF_FIT; method-only not automatically installed`；rollback=`DISCARD_ADVISORY`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:METHOD.KANBAN`｜existing Hermes kanban（NATIVE_METHOD; v0.22.5 pinned / existing capability）

- **原字節來源／原處置**：`FHS-BODY-08:L214` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`e5d00804cd6adb2f865e0d7ae00416f35f3ccafaef973a468a2b2691327f02fc`；L1 CH22/23 OriginalID 原字面 `Native20:METHOD.KANBAN`。SourceType=`NATIVE_METHOD`，`OriginalDisposition=METHOD_OR_FORMAT`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`HERMES_DURABLE_RUNTIME` × `Hermes` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=multi-step persistent task；Producer=existing Hermes kanban 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=existing board keeps WorkID/cursor and truthful Done。OriginalConsumer=`Hermes original Kanban + HGK WorkID`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：new queue or board Done implies World effect。`FirstFail=ASSET.Native20:METHOD.KANBAN.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：v0.22.5 pinned / existing capability；`immutable_commit/asset_sha256=HERMES_V0.22.5_PINNED_SOURCE_CONFIRMATION_REQUIRED`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`METHOD_OUTPUT: bounded source input → method/decision → original Consumer output; no fictitious binary uninstall`；Case alias=`DESIGN.ASSET.Native20:METHOD.KANBAN`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`USE_NATIVE_IF_FIT; method-only not automatically installed`；rollback=`RESUME_ORIGINAL_WORKID`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:METHOD.SWARM`｜bounded delegate（NATIVE_METHOD; v0.22.5 pinned / capability probe）

- **原字節來源／原處置**：`FHS-BODY-08:L231` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`56ac903444618d2f0fa5064c60cc01e5c9334851404de1300ac141ef0eb282bc`；L1 CH22/23 OriginalID 原字面 `Native20:METHOD.SWARM`。SourceType=`NATIVE_METHOD`，`OriginalDisposition=METHOD_OR_FORMAT`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`HERMES_DURABLE_RUNTIME` × `Hermes` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=parallelizable bounded jobs；Producer=bounded delegate 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=delegated subtask uses parent work id, bounded scope and join。OriginalConsumer=`Hermes Delegation/Swarm original host`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：subagents use shared privileged checker token。`FirstFail=ASSET.Native20:METHOD.SWARM.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：v0.22.5 pinned / capability probe；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`METHOD_OUTPUT: bounded source input → method/decision → original Consumer output; no fictitious binary uninstall`；Case alias=`DESIGN.ASSET.Native20:METHOD.SWARM`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`USE_NATIVE_IF_FIT; method-only not automatically installed`；rollback=`STOP_CHILD_AND_REJOIN`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:METHOD.OPENSPEC`｜Fission-AI OpenSpec（METHOD_CLI; v1.16.0 research target / MIT source candidate; asset digest HOLD）

- **原字節來源／原處置**：`FHS-BODY-08:L248` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`33a9b77235461caef69b0a067d852e9e80f301f2da42629c44bdd3aaadc17721`；L1 CH22/23 OriginalID 原字面 `Native20:METHOD.OPENSPEC`。SourceType=`METHOD_CLI`，`OriginalDisposition=METHOD_OR_FORMAT`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`SOURCE_SPEC_DIFF` × `OpenSpec Windows Host` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=brownfield change with explicit scope；Producer=Fission-AI OpenSpec 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=brownfield spec delta translated to source-bound proposal and reparse。OriginalConsumer=`SBL TPM/PIPD Original Spec Reader`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：SpecDiff imported as canonical PI or Permit。`FirstFail=ASSET.Native20:METHOD.OPENSPEC.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：v1.16.0 research target / MIT source candidate; asset digest HOLD；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`CLI_RUN: binary SHA/version, argv/exit/stdout/stderr, WriteSet+original Host invoke; failure exit & cleanup`；Case alias=`DESIGN.ASSET.Native20:METHOD.OPENSPEC`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`USE_NATIVE_IF_FIT; method-only not automatically installed`；rollback=`DISCARD_DELTA`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:METHOD.GSTACK`｜gstack workflow（METHOD_HOST_SKILL; v1.92.55.0 [HISTORICAL_RESEARCH_NOT_CURRENT_SELECTION; current=git:6bdafb2/1.95.5.0] / licence verified via original release reader HOLD）

- **原字節來源／原處置**：`FHS-BODY-08:L265` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`ba9b044cd9cede8acfc1435b0840511fda0442f4f54a19f3491b69d2f4ad4561`；L1 CH22/23 OriginalID 原字面 `Native20:METHOD.GSTACK`。SourceType=`METHOD_HOST_SKILL`，`OriginalDisposition=METHOD_OR_FORMAT`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`MAKER_REVIEW_QA` × `gstack allowed Host` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=authorized review/QA job；Producer=gstack workflow 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=QA/review findings map to independent Oracle refs as proposals。OriginalConsumer=`Original TQAEP/Case Maker-side reviewer`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：/ship or review PASS treated as Publisher or checker。`FirstFail=ASSET.Native20:METHOD.GSTACK.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：v1.92.55.0 [HISTORICAL_RESEARCH_NOT_CURRENT_SELECTION; current=git:6bdafb2/1.95.5.0] / licence verified via original release reader HOLD；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`HOST_SKILL_TRIGGER: independent installed/loaded/invoked/used AND negative nontrigger/removed; no borrowed receipt`；Case alias=`DESIGN.ASSET.Native20:METHOD.GSTACK`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`USE_NATIVE_IF_FIT; method-only not automatically installed`；rollback=`DISCARD_REVIEW`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:METHOD.SUPERPOWERS`｜obra Superpowers（METHOD_HOST_SKILL; METHOD_REPO_PIN_LICENSE_HOLD）

- **原字節來源／原處置**：`FHS-BODY-08:L282` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`8cd728434affcf22d418da7b8ad06f8bd4dd1271ac2b945a396f83fd27324e7e`；L1 CH22/23 OriginalID 原字面 `Native20:METHOD.SUPERPOWERS`。SourceType=`METHOD_HOST_SKILL`，`OriginalDisposition=METHOD_OR_FORMAT`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`METHOD_TDD_DEBUG` × `allowed Skill Host` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=real TDD/debug task；Producer=obra Superpowers 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=red failing fixture→bounded fix→green with original source diff。OriginalConsumer=`SBL bounded repair/Developer reviewer`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：no red case or automatic grant from method。`FirstFail=ASSET.Native20:METHOD.SUPERPOWERS.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：METHOD_REPO_PIN_LICENSE_HOLD；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`HOST_SKILL_TRIGGER: independent installed/loaded/invoked/used AND negative nontrigger/removed; no borrowed receipt`；Case alias=`DESIGN.ASSET.Native20:METHOD.SUPERPOWERS`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`USE_NATIVE_IF_FIT; method-only not automatically installed`；rollback=`DISCARD_METHOD_OUTPUT`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:METHOD.SPEC_KIT`｜GitHub Spec Kit（METHOD; METHOD_REPO_PIN_LICENSE_HOLD）

- **原字節來源／原處置**：`FHS-BODY-08:L299` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`e0d382cc1450330229e740c99579f692c70704115ab955cd32d47e63160aff3e`；L1 CH22/23 OriginalID 原字面 `Native20:METHOD.SPEC_KIT`。SourceType=`METHOD`，`OriginalDisposition=METHOD_OR_FORMAT`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`METHOD_GREENFIELD_SPEC` × `approved host` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=greenfield structured planning；Producer=GitHub Spec Kit 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=goal→spec/plan/tasks candidate for original parser。OriginalConsumer=`TPM original Spec Intake`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：brownfield PIPD canonical overwritten by alternate schema。`FirstFail=ASSET.Native20:METHOD.SPEC_KIT.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：METHOD_REPO_PIN_LICENSE_HOLD；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`METHOD_OUTPUT: bounded source input → method/decision → original Consumer output; no fictitious binary uninstall`；Case alias=`DESIGN.ASSET.Native20:METHOD.SPEC_KIT`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`USE_NATIVE_IF_FIT; method-only not automatically installed`；rollback=`DISCARD_METHOD_OUTPUT`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:METHOD.MATTP_SKILLS`｜Matt Pocock Skills（METHOD_HOST_SKILL; METHOD_REPO_PIN_LICENSE_HOLD）

- **原字節來源／原處置**：`FHS-BODY-08:L316` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`f743fc38297f4d22882865db5996d1fe86045a661fc5f9b84c2927e5692b80a1`；L1 CH22/23 OriginalID 原字面 `Native20:METHOD.MATTP_SKILLS`。SourceType=`METHOD_HOST_SKILL`，`OriginalDisposition=METHOD_OR_FORMAT`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`QUESTION_LEDGER_REUSE` × `approved skill host` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=new material uncertainty in requirements；Producer=Matt Pocock Skills 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=unresolved substantive question asked once with source/context。OriginalConsumer=`TPM QuestionLedger original reader`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：already known answer re-asked or Host trigger misclassified。`FirstFail=ASSET.Native20:METHOD.MATTP_SKILLS.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：METHOD_REPO_PIN_LICENSE_HOLD；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`HOST_SKILL_TRIGGER: independent installed/loaded/invoked/used AND negative nontrigger/removed; no borrowed receipt`；Case alias=`DESIGN.ASSET.Native20:METHOD.MATTP_SKILLS`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`USE_NATIVE_IF_FIT; method-only not automatically installed`；rollback=`DISCARD_METHOD_OUTPUT`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:METHOD.GSD`｜Get Shit Done donor（METHOD; METHOD_REPO_PIN_LICENSE_HOLD）

- **原字節來源／原處置**：`FHS-BODY-08:L333` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`9cdb77df991799cb84e646b0a71cbeaefbeafe1cb05745ebb36ac98de4222491`；L1 CH22/23 OriginalID 原字面 `Native20:METHOD.GSD`。SourceType=`METHOD`，`OriginalDisposition=METHOD_OR_FORMAT`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`METHOD_PROGRAM_RESUME` × `SBL/Hermes planning host` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=complex long work needs decomposition；Producer=Get Shit Done donor 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=bounded task planning/checkpoint joins original WorkID DAG。OriginalConsumer=`Original Program WP Planner`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：invented HGK WorkID/own scheduler。`FirstFail=ASSET.Native20:METHOD.GSD.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：METHOD_REPO_PIN_LICENSE_HOLD；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`METHOD_OUTPUT: bounded source input → method/decision → original Consumer output; no fictitious binary uninstall`；Case alias=`DESIGN.ASSET.Native20:METHOD.GSD`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`USE_NATIVE_IF_FIT; method-only not automatically installed`；rollback=`DISCARD_METHOD_OUTPUT`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:METHOD.FABRIC_COMPRESS`｜知識/Prompt/Skill 壓製（METHOD_FORMAT; SOURCE_PIN_LICENSE_APPLIES_ONLY_EXTERNAL_DONOR）

- **原字節來源／原處置**：`FHS-BODY-08:L350` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`92f5438d5420b2ff1b8f104656dea40bccc7502abcd1b46600a57b20862ec186`；L1 CH22/23 OriginalID 原字面 `Native20:METHOD.FABRIC_COMPRESS`。SourceType=`METHOD_FORMAT`，`OriginalDisposition=METHOD_OR_FORMAT`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`SOURCE_BOUND_TRANSLATION` × `Fabric/SBL source converter` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=long sources must fit existing Host context；Producer=知識/Prompt/Skill 壓製 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=lossless compact prompt/skill with OriginalID/NEG and reparse check。OriginalConsumer=`Original Source/Skill Compiler Reader`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：drops prohibitions or signs new Native principal。`FirstFail=ASSET.Native20:METHOD.FABRIC_COMPRESS.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：SOURCE_PIN_LICENSE_APPLIES_ONLY_EXTERNAL_DONOR；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`FORMAT_ROUNDTRIP: lossless OriginalID/NEG Source→translation→original Reader reparse; no binary lifecycle`；Case alias=`DESIGN.ASSET.Native20:METHOD.FABRIC_COMPRESS`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`USE_NATIVE_IF_FIT; method-only not automatically installed`；rollback=`RESTORE_ORIGINAL_SOURCE`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:PIPD.P4`｜PIPD-LS-SP Public Skills+CLI（歷史原名）（ORIGINAL_OWNER_COMPONENT; SBL U04 live canonical / Apache-2.0 repo）

- **原字節來源／原處置**：`FHS-BODY-08:L367` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`c88f604c816c88b878ba084372dc1416021a52705a329834e6df9da79f5646f7`；L1 CH22/23 OriginalID 原字面 `Native20:PIPD.P4`。SourceType=`ORIGINAL_OWNER_COMPONENT`，`OriginalDisposition=OWNER_COMPONENT`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`PIPD_SBL_CANONICAL_COMPILER` × `SBL PIPD` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=PI/PD/ECP/TQAEP phase；Producer=PIPD-LS-SP Public Skills+CLI（歷史原名） 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=original 13 CLI/19 families/8 packs, strict PI and plan sidecar separate。OriginalConsumer=`SBL integrations/pipd original Writer`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：archived PIPD-LS-SP acts as second active writer。`FirstFail=ASSET.Native20:PIPD.P4.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：SBL U04 live canonical / Apache-2.0 repo；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`ORIGINAL_COMPONENT_READER: original product/compiler/consumer output; no shadow Writer`；Case alias=`DESIGN.ASSET.Native20:PIPD.P4`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`USE_NATIVE_IF_FIT; method-only not automatically installed`；rollback=`RESTORE_ORIGINAL_COMPILER_READER`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Native20:SBL.PRODUCT`｜SBL Shared Core+Three SP（ORIGINAL_OWNER_COMPONENT; original SBL writer/source）

- **原字節來源／原處置**：`FHS-BODY-08:L384` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`66b5e287a45319ae173637d41fef597cd82b6bc8ebae838121c36aef33f8afdd`；L1 CH22/23 OriginalID 原字面 `Native20:SBL.PRODUCT`。SourceType=`ORIGINAL_OWNER_COMPONENT`，`OriginalDisposition=OWNER_COMPONENT`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`SBL_SHAREDCORE_PRODUCT` × `SBL` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=goal routes to product capabilities；Producer=SBL Shared Core+Three SP 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=six modules + three SP outputs each consumer-specific。OriginalConsumer=`SBL product Reader, TPM/Commander/Challenge separate`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：one chat handler claims full product/three SP acceptance。`FirstFail=ASSET.Native20:SBL.PRODUCT.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：original SBL writer/source；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`ORIGINAL_COMPONENT_READER: original product/compiler/consumer output; no shadow Writer`；Case alias=`DESIGN.ASSET.Native20:SBL.PRODUCT`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`USE_NATIVE_IF_FIT; method-only not automatically installed`；rollback=`RESTORE_ORIGINAL_SBL_ADAPTER`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Default30:P0-TOOL-001`｜Hermes Agent（DESIGN_DEFAULT_CLI; v0.22.5 pinned / source licence at exact origin HOLD）

- **原字節來源／原處置**：`FHS-BODY-08:L402` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`f422fcc0de403eeb069f6962907625079e503554254f2ad599eab62d47999145`；L1 CH22/23 OriginalID 原字面 `Default30:P0-TOOL-001`。SourceType=`DESIGN_DEFAULT_CLI`，`OriginalDisposition=DEFAULT_ENABLED_AFTER_QUALIFICATION`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`HERMES_DURABLE_RUNTIME` × `Hermes Host` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=governed multi-step ordinary goal；Producer=Hermes Agent 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=default-on qualified execution with fresh PID/lasting WorkID。OriginalConsumer=`Hermes runtime Host consumer`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：only docs/test daemon selected; second Queue。`FirstFail=ASSET.Default30:P0-TOOL-001.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：v0.22.5 pinned / source licence at exact origin HOLD；`immutable_commit/asset_sha256=HERMES_V0.22.5_PINNED_SOURCE_CONFIRMATION_REQUIRED`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`CLI_RUN: binary SHA/version, argv/exit/stdout/stderr, WriteSet+original Host invoke; failure exit & cleanup`；Case alias=`DESIGN.ASSET.Default30:P0-TOOL-001`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`DESIGN_DEFAULT_REQUIRED; qualified default-on after original Host/Owner acceptance`；rollback=`RESTORE_LAST_GOOD_RUNTIME`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Default30:P0-TOOL-005`｜Codex（DESIGN_DEFAULT_CLI; HOST_VERSION_LICENSE_PIN_HOLD）

- **原字節來源／原處置**：`FHS-BODY-08:L450` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`e8ff219c3e3a621687e2e1def7d6b48b4a40d8a49b0b36c826e9adcdffc04570`；L1 CH22/23 OriginalID 原字面 `Default30:P0-TOOL-005`。SourceType=`DESIGN_DEFAULT_CLI`，`OriginalDisposition=DEFAULT_ENABLED_AFTER_QUALIFICATION`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`BOUNDED_CODE_WORKER` × `Codex CLI` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=bounded authorized DEV patch；Producer=Codex 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=live exit/diff/actual tool/model raw within exact write scope。OriginalConsumer=`HGK/Hermes Codex scoped Worker`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：same provider alias fake Served or unsanctioned code write。`FirstFail=ASSET.Default30:P0-TOOL-005.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：HOST_VERSION_LICENSE_PIN_HOLD；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`CLI_RUN: binary SHA/version, argv/exit/stdout/stderr, WriteSet+original Host invoke; failure exit & cleanup`；Case alias=`DESIGN.ASSET.Default30:P0-TOOL-005`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`DESIGN_DEFAULT_REQUIRED; qualified default-on after original Host/Owner acceptance`；rollback=`RESTORE_REPO_COMMIT`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Default30:P0-TOOL-062`｜GitHub Actions（DESIGN_DEFAULT_CI; workflow SHA / platform terms not assumed license of project）

- **原字節來源／原處置**：`FHS-BODY-08:L690` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`78d8b6b8f289525479718370c76c659974614db5475de6c81ab0ae0e81b89ef9`；L1 CH22/23 OriginalID 原字面 `Default30:P0-TOOL-062`。SourceType=`DESIGN_DEFAULT_CI`，`OriginalDisposition=DEFAULT_ENABLED_AFTER_QUALIFICATION`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`CI_GITHUB_WORKFLOW` × `GitHub Actions` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=applicable repository CI；Producer=GitHub Actions 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=pinned workflow commit/run id/log and target tests。OriginalConsumer=`Original SBL CI/Workflow Owner`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：green non-affected CI claimed Native E2E or no run logs。`FirstFail=ASSET.Default30:P0-TOOL-062.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：workflow SHA / platform terms not assumed license of project；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`CI_WORKFLOW: workflow SHA + commit/run_id/log + actual affected result; green status alone not Native WorldRaw`；Case alias=`DESIGN.ASSET.Default30:P0-TOOL-062`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`DESIGN_DEFAULT_REQUIRED; qualified default-on after original Host/Owner acceptance`；rollback=`WORKFLOW_REVERT_BY_REPO_OWNER`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

### AssetSlot `Default30:P0-TOOL-072`｜SQLite（DESIGN_DEFAULT_FORMAT; existing SQLite runtime/ABI source）

- **原字節來源／原處置**：`FHS-BODY-08:L750` SHA256=`1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d`；原行 SHA256=`13372191513ea7185b1f174785b9afb68e763b9555121d7013704ba7c92f51a8`；L1 CH22/23 OriginalID 原字面 `Default30:P0-TOOL-072`。SourceType=`DESIGN_DEFAULT_FORMAT`，`OriginalDisposition=DEFAULT_ENABLED_AFTER_QUALIFICATION`；未經原 Writer 核定的版本差額維持本 ID 的 hold。
- **NeedKey／Host/Kind/Mode/Scope**：`HGK_SHAREDSPINE_DURABLE` × `HGK Original Host` × affected Kind/Mode/Scope（實際範圍由原 Host/Goal Reader 晚綁）；同 Need 重複 ID 用一筆 occupancy decision，`original_ids[]` 一律保留；`qualified_incumbent=NONE_NOT_OBSERVED`（不是確認全無）。
- **實質功能 Input→Producer→Output**：Trigger=original durable control-plane state；Producer=SQLite 之既有原生功能／薄 Host adapter，輸入 OriginalID+同 SourceSHA+Scope+原證據狀態；**POS**=same original DB schema/journal transaction/lease fence。OriginalConsumer=`Original HGK SharedSpine DB Reader`，須見該作用的真輸出，不可只看選型清冊。
- **各別 NEG 與 FirstFail**：new independent DB used as queue or schema migration by Maker。`FirstFail=ASSET.Default30:P0-TOOL-072.READER_OR_FUNCTION_NACK`（本次作者端 Case alias，正式 code 由原 Reader 回）；`NoFit` 要由原 Host/License/Owner 對這個 Need 特定原因核准，不能用沒安裝一概轉 Optional。
- **版號／授權／Host Probe**：existing SQLite runtime/ABI source；`immutable_commit/asset_sha256=ORIGINAL_UPSTREAM_PIN_OR_HOLD`；`license_notice=SOURCE_LICENSE_AND_NOTICE_READER_REQUIRED`；`Windows_arch/HostLoader/OS_PID/LoadedSHA=HOST_NOT_OBSERVED`；正式採用要逐項比 Host Fit，不從這份表製造 Install evidence。
- **獨立原功能測例**：`FORMAT_SCHEMA: original SQLite schema/transaction/journal Raw; not another queue or generic executable install`；Case alias=`DESIGN.ASSET.Default30:P0-TOOL-072`；尚未經原 CaseRegistry 讀回時 `ORIGINAL_CASE_RUNNER_UNBOUND` 不擋純 SOURCE_READ/METHOD_OUTPUT。
- **啟用義務／NoFit／退出**：`DESIGN_DEFAULT_REQUIRED; qualified default-on after original Host/Owner acceptance`；rollback=`OWNER_DB_MIGRATION_ONLY`，需有原 Owner last-good 或補償，未知世界效果須先 reconcile。

## 4. W0 技術壓製與 W3 資產主責的合法界線

保留 Native20/Default30/Donor24/Method25/TECH386 五個正交分母；24 W1 Source identities 的 NeedKey 對應不能使其他 461 個身份消失。W0 主責原 31 冊來源、唐突的 donor 轉譯及三 SPECDraft；W1 只用原 Need 的最小可用 occupant；W3 才處理全量受影矩陣與 B1/W18。
`REJECT/REFERENCE/METHOD_ONLY` 原處置不得被 NeedKey 命名偷升 `ADOPT/DEFAULT`。設計要求的 mandatory default 在 Host qualification 缺失時必標 `CAPABILITY_GAP_HOLD`；有 last-good incumbent 則先保持原服務，再走可逆熱切換。

## 5. OpenSpec 與 gstack（明列何時觸發、何時不觸發）

| Tool/需用角色 | 設計 Pin / Upstream | 觸發／不觸發 | 壓製與驗收（不是原 Canonical/Checker） | 失敗/回退 |
|---|---|---|---|---|
| OpenSpec / SPEC_DELTA_ADVISORY | v1.16.0 候選（截至 2026-11-04 官方 release 可見），Windows standalone vs npm Node>=22.12；原 OpenSpec source/license 候選；asset sha/Host 尚待核 | Brownfield 需求已有可判 spec delta 且 Owner Scope 允許；普通 SourceRead、無差額、缺 Windows Host 不觸發 | OpenSpec delta → source-bound SpecDiff + original ID/NEG/Parent crosswalk → 由原 SBL TPM/PIPD Reader reparse strict PI；真 CLI `--version`,`validate`,`diff` POS/NEG/出口碼，非真機 NOT_RUN | OPENSPEC_WINDOWS_BIND_HOLD；回原三 SPEC/PI 原 Writer，刪隔離 delta |
| gstack / QA_ADVISORY | v1.92.55.0 [HISTORICAL_R5_RESEARCH_NOT_CURRENT_SELECTION] 候選（2026-11-02）；License 需原 release tag/NOTICE reader 確認；Windows minimal support Git Bash/MSYS，Bun/Node/host/Privacy 待核 | 只在合法隔離 QA/review/debug 的受影需求；無原版保護／沒有合法 Host / 需獨立 Checker 不觸發 | gstack review/QA report → 原 TQAEP oracle/case crosswalk 作 Maker 建議；Host trigger/nontrigger + Windows-smoke，禁止 `ship` 直接當 Publisher | GSTACK_PIN_WINDOWS_HOLD；回原內建 review/TQAEP，Owner 決策前不上線 |

原 Release／source tag 不等於 `INVOKED/QUALIFIED`。在 Windows 的 OpenSpec standalone `SHA256SUMS` 校驗與 gstack Windows minimal-support 的真讀回前不執行安裝；gstack 如具有 external network/browser/telemetry/privacy 副作用，需原 Security/Consent Owner 授權。本包只提出低工程量 Build-or-Use，不改既有 Host。

## 6. 三 Portable SP × 四原產品 Host（12 候選 cell）及 8 PIPD Skill 獨立分母

**注意**：Portable Host 四種為原 L0 `Hermes Agent / Codex / Claude Code / ChatGPT`；原 BODY-09B 192 legacy matrix 還有 `DeepSeek Harness` 等 Host token，兩種身份集合不得用字串替換。12 row 是 Host 適用性待原 Reader 核對的設計分母，不宣稱 12 cell 皆應 Install。每個 cell 保留 `selected/installed/loaded/invoked/used/removed/loaderSHA/actualPID/positive_trigger/negative_nontrigger/firstfail`，現狀真 Host 均 `NOT_OBSERVED`。

| 原 SP | Original Host | 適用性 | 原 Loader 資訊入口 | 每 cell Readback | POS trigger | NEG nontrigger | Original Consumer | 狀態 |
|---|---|---|---|---|---|---|---|---|
| TPM-SP | Hermes Agent | APPLICABILITY_READ_OR_HOST_HOLD | Hermes original Profile/Skill loader (PID+SHA HERMES_HOST_HOLD) | Host-specific loaded/invoked/used/removed must be individually observed | Goal→PM/SE/TPgM 3 distinct spec | No TPM intent → not trigger | SBL Product/TPM Reader | HOST_NOT_OBSERVED |
| Commander Guide-SP | Hermes Agent | APPLICABILITY_READ_OR_HOST_HOLD | Hermes original Profile/Skill loader (PID+SHA HERMES_HOST_HOLD) | Host-specific loaded/invoked/used/removed must be individually observed | bounded PLAN proposal/guide only | simple source inquiry or no PLAN changes → not trigger | Original HGK PLAN Reader | HOST_NOT_OBSERVED |
| Acceptance Challenge-SP | Hermes Agent | APPLICABILITY_READ_OR_HOST_HOLD | Hermes original Profile/Skill loader (PID+SHA HERMES_HOST_HOLD) | Host-specific loaded/invoked/used/removed must be individually observed | Maker case plan + independent checker request | no Original Raw/case or maker-as-checker → not trigger | Original Protected Checker Request Reader | HOST_NOT_OBSERVED |
| TPM-SP | Codex | APPLICABILITY_READ_OR_HOST_HOLD | Codex skill/CLI host Reader (capability/trigger HOST_HOLD) | Host-specific loaded/invoked/used/removed must be individually observed | Goal→PM/SE/TPgM 3 distinct spec | No TPM intent → not trigger | SBL Product/TPM Reader | HOST_NOT_OBSERVED |
| Commander Guide-SP | Codex | APPLICABILITY_READ_OR_HOST_HOLD | Codex skill/CLI host Reader (capability/trigger HOST_HOLD) | Host-specific loaded/invoked/used/removed must be individually observed | bounded PLAN proposal/guide only | simple source inquiry or no PLAN changes → not trigger | Original HGK PLAN Reader | HOST_NOT_OBSERVED |
| Acceptance Challenge-SP | Codex | APPLICABILITY_READ_OR_HOST_HOLD | Codex skill/CLI host Reader (capability/trigger HOST_HOLD) | Host-specific loaded/invoked/used/removed must be individually observed | Maker case plan + independent checker request | no Original Raw/case or maker-as-checker → not trigger | Original Protected Checker Request Reader | HOST_NOT_OBSERVED |
| TPM-SP | Claude Code | APPLICABILITY_READ_OR_HOST_HOLD | Claude Code Skill Host original loader (HOST_HOLD) | Host-specific loaded/invoked/used/removed must be individually observed | Goal→PM/SE/TPgM 3 distinct spec | No TPM intent → not trigger | SBL Product/TPM Reader | HOST_NOT_OBSERVED |
| Commander Guide-SP | Claude Code | APPLICABILITY_READ_OR_HOST_HOLD | Claude Code Skill Host original loader (HOST_HOLD) | Host-specific loaded/invoked/used/removed must be individually observed | bounded PLAN proposal/guide only | simple source inquiry or no PLAN changes → not trigger | Original HGK PLAN Reader | HOST_NOT_OBSERVED |
| Acceptance Challenge-SP | Claude Code | APPLICABILITY_READ_OR_HOST_HOLD | Claude Code Skill Host original loader (HOST_HOLD) | Host-specific loaded/invoked/used/removed must be individually observed | Maker case plan + independent checker request | no Original Raw/case or maker-as-checker → not trigger | Original Protected Checker Request Reader | HOST_NOT_OBSERVED |
| TPM-SP | ChatGPT | APPLICABILITY_READ_OR_HOST_HOLD | ChatGPT connected plugin/skill host (chat-visible skill != Windows process loaded) | Host-specific loaded/invoked/used/removed must be individually observed | Goal→PM/SE/TPgM 3 distinct spec | No TPM intent → not trigger | SBL Product/TPM Reader | HOST_NOT_OBSERVED |
| Commander Guide-SP | ChatGPT | APPLICABILITY_READ_OR_HOST_HOLD | ChatGPT connected plugin/skill host (chat-visible skill != Windows process loaded) | Host-specific loaded/invoked/used/removed must be individually observed | bounded PLAN proposal/guide only | simple source inquiry or no PLAN changes → not trigger | Original HGK PLAN Reader | HOST_NOT_OBSERVED |
| Acceptance Challenge-SP | ChatGPT | APPLICABILITY_READ_OR_HOST_HOLD | ChatGPT connected plugin/skill host (chat-visible skill != Windows process loaded) | Host-specific loaded/invoked/used/removed must be individually observed | Maker case plan + independent checker request | no Original Raw/case or maker-as-checker → not trigger | Original Protected Checker Request Reader | HOST_NOT_OBSERVED |

**8 PIPD Skill 原身分×真 Consumer（不等於上表 3 SP 收據）**：

| Skill 独立入口 | 適用功能與輸出 | 每 pack 專屬負例 | 原 Consumer | Host 讀回 |
|---|---|---|---|---|
| pipd-route-intake.SKILL.md | Goal+source locator→typed IntentCard | blank goal/zero locators/path traversal | original PIPD Intake Reader | Host-availability: N/A when no such original loader; otherwise independently probe SELECTED→USED |
| pipd-authority-source.SKILL.md | source families/sha/locator→AuthorityBinding | missing family sha/authority conflict | original PIPD Authority Reader | Host-availability: N/A when no such original loader; otherwise independently probe SELECTED→USED |
| pipd-profile-tailor.SKILL.md | nine-axis profile safety veto→ProfileBinding | unknown axis/undercut safety | original PIPD Profile Reader | Host-availability: N/A when no such original loader; otherwise independently probe SELECTED→USED |
| pipd-pi-compile.SKILL.md | frozen Intent/profile→strict PI/trace | lost NEG/sidecar in strict schema | original PIPD PI Compiler Reader | Host-availability: N/A when no such original loader; otherwise independently probe SELECTED→USED |
| pipd-pd-bind.SKILL.md | canonical PI+current local git probe→PD | remote HEAD/path escape/stale preimage | original PIPD PD/RepoContext Reader | Host-availability: N/A when no such original loader; otherwise independently probe SELECTED→USED |
| pipd-execution-contract.SKILL.md | OperationType→DEV/OPS intent and ECP candidate | permit laundering/non-idempotent retry | original PIPD ECP Effect Reader | Host-availability: N/A when no such original loader; otherwise independently probe SELECTED→USED |
| pipd-assurance-tqaep.SKILL.md | original Case/Oracle POS/NEG→Planned TQAEP | maker self-signs / no runner/raw | original PIPD TQAEP/Case Reader | Host-availability: N/A when no such original loader; otherwise independently probe SELECTED→USED |
| pipd-package-project.SKILL.md | ClaimCeiling/TraceClosure/EvidenceExpectation plan | package seal = independent acceptance | original PIPD Project/Bundle Reader | Host-availability: N/A when no such original loader; otherwise independently probe SELECTED→USED |

**Host 驗收演算法**：先核本 Host `supports(pack,kind,mode,scope)` 原 Reader；不適用=`N/A_BY_ORIGINAL_READER`，未知=`HOST_APPLICABILITY_HOLD`。適用才查 immutable pack SHA、manifest、loader origin、load PID、fresh trigger與 nontrigger、實際 Consumer output、remove/cleanup；其他 Host/SP/Skill 的 Raw 不可借用。Package/Skill 僅「讀得見」不等於 Loaded。

## 7. 防降級 HotSwap、LastGood、半成品失敗及安全退場（逐型別，不一律 Uninstall）

`NeedKey+Kind+Mode+Host+Scope` 每一 active 槽位只有一個經原 Reader/Consumer Qualified 的 Occupant；`DESIGN_DEFAULT_REQUIRED` 不因 Host 未裝而降 OPTIONAL。狀態保持 `SOURCE_PINNED → QUALIFICATION_HOLD/READY → original admitted install or use → INSTALLED → LOADED → INVOKED → CONSUMER_POS_NEG → QUALIFIED_ACTIVE`。任何缺件回 `CAPABILITY_GAP_HOLD`，有 last-good incumbent 必須維持原效力，僅等價 occupant 先通 POS/NEG、Owner switch 同意才切換。

| 受影類型／具名例 | Preimage / Attempt / 必查 Post | 故意失敗/中止觸發 | Original rollback／residue | 重資格化範圍 |
|---|---|---|---|---|
| Hermes pinned v0.22.5 | original profile SHA+PID+journal; update only original Host version reader | Profile chosen≠Loaded或重啟後 Journal UNKNOWN | 原 Runtime Owner 回原 pin、reconcile journal；不建新 Queue | affected session/three lanes |
| OpenSpec v1.16.0 advisory | original source span+candidate SpecDiff; standalone/npm tool only if approved | CLI exit!=0 / reparse strict PI loses NEG | 刪隔離 proposal，原 TPM/PIPD 恢復先前 SPEC；無 Host effect 不要求 uninstall | affected brownfield SpecDelta |
| gstack v1.92.55.0 [HISTORICAL_R5_RESEARCH_NOT_CURRENT_SELECTION] maker QA | review scope/privacy/CaseRef; trigger+nontrigger | Host unsupported / /ship tries Publisher / output without oracle | 停止 advisory，移除私有本輪 review；原 Checker 不能借 Maker PASS | affected review case |
| PIPD SBL hosted compiler | same SHA strict PI and separate sidecar | PD bind 以 remote HEAD 冒 local / schema mismatch | 原 Reader 使 affected PD/ECP stale；PI 保留同身份，不創第二 writer | affected SourceSHA/RepoScope |
| Fabric/HGK singleton | active epoch/loaded digest/issuer ACL | Stage-not-loaded, stale nonce, second control plane | 原 Owner epoch/ABI migration/revoke；嚴禁對 singleton HotSwap | affected epoch/receiver |
| GitHub Actions workflow | workflow blob+run+commit original owner | CI green but no affected run/log | 原 Repo Owner revert workflow commit，保留證據；不可當 Native rollback | affected workflow/PR |
| SQLite SharedSpine | original schema version/last-good journal WAL | schema drift/partial migration/duplicate lease | 原 HGK DB Owner schema+transaction rollback；不可部署新 SQLite Queue | affected WorkID/schema |
| 三 Portable SP Host | three distinct package SHA and per-host receipt | Installed but not Loaded / Loaded but not Used/nontrigger | 該 Host 原 Loader remove/restore last-good、查殘留；不得刪他 SP | affected SP × original Host |
| Codex bounded CLI | exact repo preimage HEAD/WriteSet, original CLI exit | partial diff after crash or outside scope | 原 Repo Owner scoped rollback commit 或保留 UNKNOWN；不以 Host uninstall 代 repo revert | affected repo scope |

**DoNotBuild/NoFit**：若現有 Hermes v0.22.5 原 Kanban/Delegation/Swarm、HGK Issuer/Queue、SBL Canonical 能滿足 Need，不造相同功能。原 `NATIVE_SINGLETON` 不可替代成外部服務；METHOD/FORMAT 用結果 roundtrip，並不要求無意義 binary uninstall。只有真正 Host/Repo/Release 受保護 effect 才需要相應原 Issuer/Checker/Publisher 收據；READ/DRAFT 不因缺外部 donor license 一律中止。

## W1-r5｜五條唯一 Typed Seam 與分效權限表

五個 S1～S5 是 **L0/L2 作者端 SeamContract 身份**，非新 HGK Schema `$id`。每條必受 `same Subject/Candidate/Scope/SourceManifestSHA` 約束；READ-only inquiry 不必虛構 Candidate/PolicyEpoch。每個 Receiver `$id/version` 未從原 Registry 得出一律 `ORIGINAL_SCHEMA_ID_UNBOUND`，此 W1 對 S4/S5 只向 W2/W4 交接，不聲稱 W1 世界效果。

| Seam | Original Producer→Reader/Consumer | Same-scope necessary fields / expected ACK | Exclusive NEG/FirstFail | W1 responsibility |
|---|---|---|---|---|
| S1 Source→PI | W0 Product/Architecture/Program + Original Authority → Original Intake/Profile/strict PI Reader → SBL-hosted PI Writer | OriginalID/Parent/NEG/SourceSHA/Profile veto; original PI ACK or bounded HOLD | `S1_SOURCE_PI_AUTHORITY_NACK` | W1 source/profile/readback design; compiler NOT_RUN |
| S2 PI→PD/ECP/TQAEP | Original PI Writer → live Repo PD Binder → Original ECP/Case/TQAEP Reader | local Git root/HEAD/index/preimage/ACL; OperationType-specific ECP; runner/Oracle; consent | `S2_PI_PD_REPO_BIND_NACK` | draft candidate/HOLD only |
| S3 PLAN/Policy→HGK | Original PLAN CAS + Fabric Active/Loaded Policy Reader → HGK Registry/Issuer/Receiver | Original PLAN CAS ACK; ActiveEpoch/LoadedDigest/ConsumerACK; WorkID/Scope/nonce/TTL/ACL | `S3_PLAN_POLICY_ADMISSION_NACK` | no issue-permit; report unbound receiving endpoint |
| S4 Work→Hermes/Codex→World | Original HGK WorkID/Lease/Journal → Hermes pinned worker → World Raw reader | actual PID/PromptDelivered/ProviderServed/ToolRaw/world pre/post/UNKNOWN reconcile | `S4_WORK_WORLD_RAW_NACK` | W2 primary, W1 prereq/Reader |
| S5 Raw→Checker/Publisher | Original World Raw/Case/Oracle → Protected Checker → Original Publisher | Independent Principal+original oracle/NEG/Same Scope+release readback | `S5_CHECKER_PUBLISHER_SCOPE_NACK` | W2/W4 primary, W1 security handoff |

## W1-r5｜最小充分驗收、受影測例與可恢復移交

只要求**對應 EffectClass**的可見 Raw：SOURCE_READ hash/ACL；LOCAL_DRAFT isolated writer/diff；DEV Repo live HEAD/preimages/WriteSet/rollback；OPS HostID/SID/Issuer nonce/TTL/epoch+world reconciliation；USER Consent/privacy/compensation；RELEASE 原 Publisher/GHP-02/independent checker/rollback。三個 W1 狀態不可混：`DOC_AUTHOR_DONE`（本文件）；`APPLICABLE_PRODUCT_FUO`（原 Consumer 未讀則未觀測）；`AFFECTED_NATIVE_DONE`（需世界效果 Raw）與 `FULL_PKG_RELEASE_DONE`（W4 原 Publisher）。

**受影失敗策略**：`UNKNOWN`+不冪等時先 Original WorldReadBack，再決定 resume；已 admitted WorkID 不重造；同 Scope permit 可復用但 Scope/Host/PolicyEpoch 變更只使 affected operation 重綁；錯誤停受影子圖，已合法 Source/Draft/其他波續工。

> 下列保留既有 W1 r2 的逐 WP 四類 POS/NEG/SEC/EDGE 測例、原 consumer/firstfail、W0↔W1↔W2 typed envelope、RunBudget/UNKNOWN/rollback 規劃；所有 `ACK`/`Raw` 是 **EXPECTED_NOT_OBSERVED**。其中任何舊 r2 來源行號、資料狀態、Consumer 假設按本稿 r4 的上位卡重新核對，不直接作現役 Reader 資格。

05｜SPEC／分級驗收／Stop-Resume／W2 合法交接

> **法位／聲明上限**：`FHS_PKG_WAVE_001 / L3_W1_AUTHOR_SIDE_BLUEPRINT_AND_SKELETON / AUTHOR_DESIGN_ONLY`。本交付不是 W1 草案／定案、SourceFreezeManifest、Canonical PI/PD/ECP/TQAEP、原 Issuer Permit、Host Loaded 證據、Native E2E、Protected Checker 或正式 Release。此處所有 POS/NEG/ACK/WorldRaw 均為 **期待的測例或原 Reader 介面設計**，不是本輪觀測到的驗收 PASS；原 Domain Writer/Owner/Consumer 不移轉，當期 Host/Owner 未回證則範圍局部 HOLD。

## 1. 最低充分驗收：依 EffectClass，不讓治理反向阻擋第一 FUO

| Level | 可量測事實／Owner | 本輪狀態 | 不允許的升格 |
|---|---|---|---|
| L1 AUTHOR_STATIC | 原 31 File SHA、50 H1、8 WP、13 CH、36邊、strict field design；本 sandbox readback | 本輪可完成／有腳本結果 | L1 PASS ≠ 原 SourceFreeze/Owner/Host PASS |
| L2 HOST_BOUND | 原 live RepoRoot/HEAD/index/ACL，Fabric Active/Loaded Consumer，HGK Issuer，Hermes PID/Profile/Host Loader | NOT_RUN / HOST_PENDING | GitHub HEAD、selected/config 永遠不充 Local Loaded |
| L3 NATIVE_WORLD | 原 DEV/OPS/USER 受保護效果、WorldRaw、Undo/Recovery、不同 Principal | NOT_RUN（本 W1 文件任務不做世界效果） | 候選 ECP、CI 或 Handler 文本不等於 Permit |
| L4 INDEPENDENT_OR_RELEASE | 原 Protected Checker 同 subject/candidate/scope raw，原 Publisher/GHP02 | NOT_RUN / NOT_GRANTED | Maker/ChatGPT/Archive seal 不自簽 |

**Done**：本次僅 `DOC_AUTHOR_DONE` 的文檔欄位/zip 機械檢查；`PRODUCT_FUO`、`AFFECTED_NATIVE_DONE`、`FULL_PKG_RELEASE_DONE` 是三種不同責任與證據，全部 `NOT_OBSERVED`。僅對受影的 Actual Effect 進 L2/L3/L4，而不是強制每次 Goal 調用完整 W3/W4。

## 2. 八個 WP × POS／NEG／SEC／EDGE 四類獨立測試計畫（原位修正 r1 八組同文漏洞）

每個 `CASE-W1-XX-{POS|NEG|SEC|EDGE}` 是 `DESIGN_CASE_ALIAS`，不是 SBL/HGK 原 CaseID。原 Registry 的 `original_case_id,registry_sha,runner_entry,input_fixture_sha,expected_raw_schema,oracle_ref,checker_principal,requalification_scope` 必須由相應 Original Reader 回讀；未綁者 `RUNNER_UNBOUND / NOT_RUN`，不能用以下文字算 `NATIVE_PASS`。純來源檢查可在隔離作者工作區重算，真 Host 所需 Raw 仍 `EXPECTED_NOT_OBSERVED`。

### WP-FHS-02｜Fabric Policy Consumer：四個不同輸入／Oracle／退出

- **Original Owner/Receiver**：Fabric Policy Owner → HGK policy consumer；原依賴=WP-FHS-01；Original Registry/CaseID/Runner=`RUNNER_UNBOUND`（不自建正式 Case）。
- **Operation types**：SOURCE_READ:Policy snapshot+active epoch probe；HOST_OPS:original Policy Consumer effective load/readback；`input_bytes` 與 expected type 以設計 fixture 可以重算，但原 Host Raw/`$id` 須原 Reader。

- **`CASE-W1-02-POS`**：`POS`；Trigger/Input＝對同 Subject/SourceSHA、受影 operation 執行原 Reader 候選驗證：Original Fabric Policy Owner/current epoch; applicable Policy manifest SHA; HGK original policy consumer process identity。預期 `ActiveEpoch+LoadedDigest+ConsumerACK（由 Fabric+HGK 原 Reader 同 Subject 讀回）` 的 typed 原 Consumer 回條或具名 `HOLD`，不以檔案存在冒驗收。；`design_fixture_sha256=fe73c68a6026bca8669822b5a9e8cf018c3644ace9dc74572a816e0c9d44b215`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=READER_ACK_OR_POLICY_EPOCH_LOADED_MISMATCH`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-02 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。
- **`CASE-W1-02-NEG`**：`NEG`；Trigger/Input＝從合法候選刪掉/錯配本 WP 必需前置：把未批准 Stage SHA 當 ActiveEpoch、HGK LoadedDigest 與 active 不符。原 Reader 應 NACK，合法 READ/DRAFT 仍可續。；`design_fixture_sha256=4d67772ca1e0f1ce7343ae6b5d4ba405d622a23a3e532928cf0b1074f32a3fa5`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=POLICY_EPOCH_LOADED_MISMATCH`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-02 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。
- **`CASE-W1-02-SEC`**：`SEC`；**安全攻擊面／Input**=原 Fabric Policy Owner 簽章/Principal 被擬造，攻擊者將跨 epoch 的 approval metadata 重放到相同 Manifest；**Original Reader**=original signed owner/epoch reader；**Expected WorldRaw**=Fabric policy owner signature+epoch, HGK effective loaded digest and consumer process SID（當期 `EXPECTED_NOT_OBSERVED`）；**FirstFail**=`FABRIC_POLICY_PRINCIPAL_OR_SIGNATURE_DENY`；**Scope**=同 Subject/SourceSHA/CandidateSHA/Host/PolicyEpoch 的受影效果；**Stop/Recovery**=revoke forged approval reference, restore LastGood epoch; no world write；原 Runner=`RUNNER_UNBOUND`；status=`AUTHOR_CASE_DESIGN_NOT_NATIVE_EXECUTED`；`fixture_sha256=708885c3252c1df6a8a301e2ca1ac0c86850ecabbb13e1975e35e05a0f60fe65`。**與同 WP NEG 的業務錯誤機制獨立**，不得互相抵證。
- **`CASE-W1-02-EDGE`**：`EDGE`；Trigger/Input＝獨立邊界或半成品擾動：Owner 在 Stage 後切 epoch，舊 HGK process 尚載前 epoch；僅停受影 OPS，READ 繼續。要求保留原 Raw/last_good，依本 WP 退出 `原 Fabric/HGK Owner 以原 epoch migration/inverse 回 last-good，Stage 不可當 Active` 後有界續工；UNKNOWN 禁重放。；`design_fixture_sha256=cc32673987c77f80b40a320c30cc63cff861148071dd671c3f0453efbcd2356d`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=POLICY_EPOCH_LOADED_MISMATCH`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-02 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。

**不共用四測試的根本條件**：本 WP 的 `SEC` 檢查 `把未批准 Stage SHA 當 ActiveEpoch、HGK LoadedDigest 與 active 不符`，`EDGE` 檢查 `Owner 在 Stage 後切 epoch，舊 HGK process 尚載前 epoch；僅停受影 OPS，READ 繼續`。更換 CaseID 而保持 8 條同文屬 `CASE_SEMANTIC_DUPLICATE_NACK`。

### WP-FHS-03｜HGK Registry / Issuer：四個不同輸入／Oracle／退出

- **Original Owner/Receiver**：HGK Original Registry/Issuer/Receiver；原依賴=WP-FHS-01；Original Registry/CaseID/Runner=`RUNNER_UNBOUND`（不自建正式 Case）。
- **Operation types**：SOURCE_READ:original Registry/Issuer contract/ACL probe；HOST_OPS:scoped issuer/receiver binding；`input_bytes` 與 expected type 以設計 fixture 可以重算，但原 Host Raw/`$id` 須原 Reader。

- **`CASE-W1-03-POS`**：`POS`；Trigger/Input＝對同 Subject/SourceSHA、受影 operation 執行原 Reader 候選驗證：原 HGK Registry、OS PID/SID、scope/nonce/TTL/ProcessACL/PolicyEpoch，非 Maker credentials。預期 `IssuerReceiverBinding+original typed refusal/ACK; no self-issued Permit` 的 typed 原 Consumer 回條或具名 `HOLD`，不以檔案存在冒驗收。；`design_fixture_sha256=7a7bba7006b6053729b16932235b2e58762cc830f86165357be6fe6a82cecaae`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=READER_ACK_OR_HGK_ISSUER_ACL_NONCE_TTL_NACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-03 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。
- **`CASE-W1-03-NEG`**：`NEG`；Trigger/Input＝從合法候選刪掉/錯配本 WP 必需前置：用不同 PID/SID、過期 nonce、重用 TTL 或 scope widening 要求原 Issuer 放行。原 Reader 應 NACK，合法 READ/DRAFT 仍可續。；`design_fixture_sha256=67b80fb489ac7480a299b47cfd389cf1c772aa4e50be37db8914f680e4679bc9`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=HGK_ISSUER_ACL_NONCE_TTL_NACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-03 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。
- **`CASE-W1-03-SEC`**：`SEC`；**安全攻擊面／Input**=一般 Hermes worker SID 冒充受保護 HGK maintenance Issuer 的 OS token，要求 issuance；**Original Reader**=HGK Original Native Issuer/OS principal reader；**Expected WorldRaw**=OS SID/token origin+Issuer endpoint ACL and protected audit rejection（當期 `EXPECTED_NOT_OBSERVED`）；**FirstFail**=`HGK_ISSUER_PRINCIPAL_ACL_DENY`；**Scope**=同 Subject/SourceSHA/CandidateSHA/Host/PolicyEpoch 的受影效果；**Stop/Recovery**=deny and invalidate attempted nonce, audit without clearing unrelated WorkIDs；原 Runner=`RUNNER_UNBOUND`；status=`AUTHOR_CASE_DESIGN_NOT_NATIVE_EXECUTED`；`fixture_sha256=4aab7e16a16b929bae4338eab8ce7787439c926f56a61366971cbc28562c2073`。**與同 WP NEG 的業務錯誤機制獨立**，不得互相抵證。
- **`CASE-W1-03-EDGE`**：`EDGE`；Trigger/Input＝獨立邊界或半成品擾動：在授權後 Worker PID 重啟；原 Receiver 必以新 process ACL / nonce 再認，不借舊票。要求保留原 Raw/last_good，依本 WP 退出 `原 HGK Owner revoke affected grant/expire nonce, readback remaining WorkIDs，不清全域 Registry` 後有界續工；UNKNOWN 禁重放。；`design_fixture_sha256=aa23ebf87da2dfd98705bbd780a502c28c0edbf445c81d0fb5941ffc47f11c07`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=HGK_ISSUER_ACL_NONCE_TTL_NACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-03 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。

**不共用四測試的根本條件**：本 WP 的 `SEC` 檢查 `用不同 PID/SID、過期 nonce、重用 TTL 或 scope widening 要求原 Issuer 放行`，`EDGE` 檢查 `在授權後 Worker PID 重啟；原 Receiver 必以新 process ACL / nonce 再認，不借舊票`。更換 CaseID 而保持 8 條同文屬 `CASE_SEMANTIC_DUPLICATE_NACK`。

### WP-FHS-04｜Hermes Durable Runtime：四個不同輸入／Oracle／退出

- **Original Owner/Receiver**：Hermes original Runtime/Journal + HGK SharedSpine；原依賴=WP-FHS-00；Original Registry/CaseID/Runner=`RUNNER_UNBOUND`（不自建正式 Case）。
- **Operation types**：SOURCE_READ:default profile/queue/journal capability probe；HOST_OPS:original runtime profile load/wake lease；LOCAL_DRAFT_WRITE:isolated restart plan；`input_bytes` 與 expected type 以設計 fixture 可以重算，但原 Host Raw/`$id` 須原 Reader。

- **`CASE-W1-04-POS`**：`POS`；Trigger/Input＝對同 Subject/SourceSHA、受影 operation 執行原 Reader 候選驗證：Hermes v0.22.5 pin；ProfileSHA、WorkID、lease generation、run budget 原 Reader。預期 `Fresh PID+LoadedProfileSHA+Raw三Lane Required/Selected/Invoked/ActualServed + JournalCursor` 的 typed 原 Consumer 回條或具名 `HOLD`，不以檔案存在冒驗收。；`design_fixture_sha256=1bf25993e2c828547f8200b78630769ec047cea6ec8b948adeb8a496114d579c`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=READER_ACK_OR_HERMES_LEASE_UNKNOWN_RECONCILE`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-04 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。
- **`CASE-W1-04-NEG`**：`NEG`；Trigger/Input＝從合法候選刪掉/錯配本 WP 必需前置：以過期 lease_generation 重播非冪等 WorkID 並把 Picker Selected 假稱 ActualServed。原 Reader 應 NACK，合法 READ/DRAFT 仍可續。；`design_fixture_sha256=ed88507327a2c86d323e556ab6c5cb506239d544492ac572e6367201964afb0b`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=HERMES_LEASE_UNKNOWN_RECONCILE`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-04 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。
- **`CASE-W1-04-SEC`**：`SEC`；**安全攻擊面／Input**=低權限 Hermes profile 越權讀取另一 Profile secret，並借另一 Lane 的 provider credential；**Original Reader**=Hermes Host original profile and secret reader；**Expected WorldRaw**=profile process identity/credential audience/secret ACL and redacted rejection（當期 `EXPECTED_NOT_OBSERVED`）；**FirstFail**=`HERMES_CROSS_PROFILE_SECRET_OR_TOKEN_DENY`；**Scope**=同 Subject/SourceSHA/CandidateSHA/Host/PolicyEpoch 的受影效果；**Stop/Recovery**=revoke affected token/session, resume same WorkID after original world reconciliation；原 Runner=`RUNNER_UNBOUND`；status=`AUTHOR_CASE_DESIGN_NOT_NATIVE_EXECUTED`；`fixture_sha256=eefe76c6b1af60b766a01870f0c768c12f48894547897c8aa67f527a643d7712`。**與同 WP NEG 的業務錯誤機制獨立**，不得互相抵證。
- **`CASE-W1-04-EDGE`**：`EDGE`；Trigger/Input＝獨立邊界或半成品擾動：worker crash 在 effect 之後/Raw 入帳之前：維持 UNKNOWN，必 original World Reconcile。要求保留原 Raw/last_good，依本 WP 退出 `原 Journal 查 WorldRaw/last-good 再 Resume WorkID；UNKNOWN 禁盲重試` 後有界續工；UNKNOWN 禁重放。；`design_fixture_sha256=c901e37c671f728579b34803210954cc3149a4559c7d48312ef5891b0cbe7601`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=HERMES_LEASE_UNKNOWN_RECONCILE`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-04 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。

**不共用四測試的根本條件**：本 WP 的 `SEC` 檢查 `以過期 lease_generation 重播非冪等 WorkID 並把 Picker Selected 假稱 ActualServed`，`EDGE` 檢查 `worker crash 在 effect 之後/Raw 入帳之前：維持 UNKNOWN，必 original World Reconcile`。更換 CaseID 而保持 8 條同文屬 `CASE_SEMANTIC_DUPLICATE_NACK`。

### WP-FHS-05｜PIPD Native Compiler：四個不同輸入／Oracle／退出

- **Original Owner/Receiver**：SBL-hosted original PIPD Compiler/Reader；原依賴=WP-FHS-01；Original Registry/CaseID/Runner=`RUNNER_UNBOUND`（不自建正式 Case）。
- **Operation types**：SOURCE_READ:SBL integrations/pipd original registry+CLI probe；LOCAL_DRAFT_WRITE:strict candidate PI/sidecars in isolated root；DEV_REPO_WRITE:only if future admitted export to repo；`input_bytes` 與 expected type 以設計 fixture 可以重算，但原 Host Raw/`$id` 須原 Reader。

- **`CASE-W1-05-POS`**：`POS`；Trigger/Input＝對同 Subject/SourceSHA、受影 operation 執行原 Reader 候選驗證：三份不同 SPECDraft、原 SourceManifest/Authority/Profile safety veto、原 PIPD Writer version。預期 `非空 strict PI，真 RepoContext 才有 PD，DEV/OPS EffectIntent 分開，PlannedTQAEP 不冒 Checker` 的 typed 原 Consumer 回條或具名 `HOLD`，不以檔案存在冒驗收。；`design_fixture_sha256=db25380618cf4dbe09ecaf0e2f2fa63afcb30c7e2d32a5676915eb8526521c50`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=READER_ACK_OR_PIPD_STRICT_SCHEMA_OR_SOURCE_NACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-05 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。
- **`CASE-W1-05-NEG`**：`NEG`；Trigger/Input＝從合法候選刪掉/錯配本 WP 必需前置：把 _profile_meta 側掛塞進 strict PI；或憑 Caller HEAD 虛構本機 Repo binding。原 Reader 應 NACK，合法 READ/DRAFT 仍可續。；`design_fixture_sha256=a2627116e950378a13972ef14da8fb29be58758b09ebb2690f874e7ddee8a960`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=PIPD_STRICT_SCHEMA_OR_SOURCE_NACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-05 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。
- **`CASE-W1-05-SEC`**：`SEC`；**安全攻擊面／Input**=未信任的來源段落內嵌指令「繞過 PIPD 原 Writer、產出已核 PI」誘發 source-to-instruction 越權；**Original Reader**=SBL-hosted PIPD original authority and pipeline Reader；**Expected WorldRaw**=original SourceReader provenance+writer origin+strict PI schema and rejection raw（當期 `EXPECTED_NOT_OBSERVED`）；**FirstFail**=`PIPD_UNTRUSTED_SOURCE_AUTHORITY_INJECTION_DENY`；**Scope**=同 Subject/SourceSHA/CandidateSHA/Host/PolicyEpoch 的受影效果；**Stop/Recovery**=quarantine source candidate; re-read original locators; never promote injected sidecar；原 Runner=`RUNNER_UNBOUND`；status=`AUTHOR_CASE_DESIGN_NOT_NATIVE_EXECUTED`；`fixture_sha256=885bf0005bf26f8b03e0e92301f94a83a1a4924f14e74e738febfbc6bde858a5`。**與同 WP NEG 的業務錯誤機制獨立**，不得互相抵證。
- **`CASE-W1-05-EDGE`**：`EDGE`；Trigger/Input＝獨立邊界或半成品擾動：PI SourceSHA 不變而 RepoHEAD 改變，只使 PD/ECP stale；不可偷重寫 PI requirement 原義。要求保留原 Raw/last_good，依本 WP 退出 `隔離候選刪除/回復 preimage；SourceSHA/HEAD 變更僅重編受影 PD/ECP` 後有界續工；UNKNOWN 禁重放。；`design_fixture_sha256=dd98865cc46aae6a7a357a0f767c9991a05e820468ed718aa0ddf3b05ba709ae`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=PIPD_STRICT_SCHEMA_OR_SOURCE_NACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-05 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。

**不共用四測試的根本條件**：本 WP 的 `SEC` 檢查 `把 _profile_meta 側掛塞進 strict PI；或憑 Caller HEAD 虛構本機 Repo binding`，`EDGE` 檢查 `PI SourceSHA 不變而 RepoHEAD 改變，只使 PD/ECP stale；不可偷重寫 PI requirement 原義`。更換 CaseID 而保持 8 條同文屬 `CASE_SEMANTIC_DUPLICATE_NACK`。

### WP-FHS-07｜Native PLAN Commander A/B/C：四個不同輸入／Oracle／退出

- **Original Owner/Receiver**：原 HGK Native PLAN Writer/Reader；原依賴=WP-FHS-01, WP-FHS-15；Original Registry/CaseID/Runner=`RUNNER_UNBOUND`（不自建正式 Case）。
- **Operation types**：SOURCE_READ:original CurrentRevision and frozen SPEC；LOCAL_DRAFT_WRITE:isolated PlanRevisionProposal；HOST_OPS:only original CAS Writer confirmation；`input_bytes` 與 expected type 以設計 fixture 可以重算，但原 Host Raw/`$id` 須原 Reader。

- **`CASE-W1-07-POS`**：`POS`；Trigger/Input＝對同 Subject/SourceSHA、受影 operation 執行原 Reader 候選驗證：W0 WP15 三 SPEC/QuestionLedger、PLAN base_revision、original Native PLAN CAS Reader。預期 `PlanRevisionProposal + original CAS(base_revision, proposal_hash) ACK/NACK` 的 typed 原 Consumer 回條或具名 `HOLD`，不以檔案存在冒驗收。；`design_fixture_sha256=7bdf630773ebf5607a500e8eab19b10710a48168493535d1011c7f8ab4b2617d`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=READER_ACK_OR_PLAN_CAS_STALE_BASE`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-07 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。
- **`CASE-W1-07-NEG`**：`NEG`；Trigger/Input＝從合法候選刪掉/錯配本 WP 必需前置：跳過原 PLAN Writer 直接送 ECP→Issuer 或停用 legacy commander 提升成新 Gate。原 Reader 應 NACK，合法 READ/DRAFT 仍可續。；`design_fixture_sha256=0a21567fcd179714613a78425cff705f6eac773f0d8ecaf7a48fb3fed3c2053f`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=PLAN_CAS_STALE_BASE`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-07 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。
- **`CASE-W1-07-SEC`**：`SEC`；**安全攻擊面／Input**=使用另一 Subject/WorkID 的具簽章 PLAN 批准內容，企圖覆寫本 WorkID 的 native CAS；**Original Reader**=HGK original Native PLAN Writer/CAS reader；**Expected WorldRaw**=original WorkID subject/source/base_revision/proposal hash and writer principal（當期 `EXPECTED_NOT_OBSERVED`）；**FirstFail**=`PLAN_FOREIGN_WORKID_OR_PRINCIPAL_DENY`；**Scope**=同 Subject/SourceSHA/CandidateSHA/Host/PolicyEpoch 的受影效果；**Stop/Recovery**=drop foreign proposal; reload own base revision; no parallel PlanWriter；原 Runner=`RUNNER_UNBOUND`；status=`AUTHOR_CASE_DESIGN_NOT_NATIVE_EXECUTED`；`fixture_sha256=f8b4f92909a4cadee598d11ad42ecb1abc41df35f198b5bee41a5ea3a38177cd`。**與同 WP NEG 的業務錯誤機制獨立**，不得互相抵證。
- **`CASE-W1-07-EDGE`**：`EDGE`；Trigger/Input＝獨立邊界或半成品擾動：兩個 proposal 同 base_revision 競逐，僅一個 Writer CAS 成功；另一個明確 NACK。要求保留原 Raw/last_good，依本 WP 退出 `CAS mismatch 丟棄提案並重讀 base；不寫 Target Repo/second Queue` 後有界續工；UNKNOWN 禁重放。；`design_fixture_sha256=a3ebd3eb2ec9fa831cd506c454173a54471cc088618c769e90cdc1c24c5c3aa3`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=PLAN_CAS_STALE_BASE`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-07 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。

**不共用四測試的根本條件**：本 WP 的 `SEC` 檢查 `跳過原 PLAN Writer 直接送 ECP→Issuer 或停用 legacy commander 提升成新 Gate`，`EDGE` 檢查 `兩個 proposal 同 base_revision 競逐，僅一個 Writer CAS 成功；另一個明確 NACK`。更換 CaseID 而保持 8 條同文屬 `CASE_SEMANTIC_DUPLICATE_NACK`。

### WP-FHS-11｜Portable Host Dogfood：四個不同輸入／Oracle／退出

- **Original Owner/Receiver**：各 Host 原 Skill/Plugin Reader+每 SP original Consumer；原依賴=WP-FHS-05, WP-FHS-16；Original Registry/CaseID/Runner=`RUNNER_UNBOUND`（不自建正式 Case）。
- **Operation types**：SOURCE_READ:Host manifest and SP skill source；LOCAL_DRAFT_WRITE:per Host test plan；HOST_OPS:original Host loader installed/loaded/invoked/used/removal readback；`input_bytes` 與 expected type 以設計 fixture 可以重算，但原 Host Raw/`$id` 須原 Reader。

- **`CASE-W1-11-POS`**：`POS`；Trigger/Input＝對同 Subject/SourceSHA、受影 operation 執行原 Reader 候選驗證：TPM-SP、Commander Guide-SP、Acceptance Challenge-SP 各自 artifact digest；Host compatibility+8 PIPD skills 各自 registry。預期 `每 SP×Host 真 Loaded/Invoked/Used/nontrigger/Remove Raw；不共用收據` 的 typed 原 Consumer 回條或具名 `HOLD`，不以檔案存在冒驗收。；`design_fixture_sha256=c0955e3662b61f0781efc2860e057c77a8c4e426b50e433e2f76cc9b5d2e6f3e`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=READER_ACK_OR_HOST_SKILL_TRIGGER_NONTRIGGER_NACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-11 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。
- **`CASE-W1-11-NEG`**：`NEG`；Trigger/Input＝從合法候選刪掉/錯配本 WP 必需前置：用 TPM-SP 的 Loaded SHA 冒 Challenge-SP；Maker 以模型結論簽 Protected Checker。原 Reader 應 NACK，合法 READ/DRAFT 仍可續。；`design_fixture_sha256=786f33e914af4c2a211c40142f6a979721e3f045e7a1fb66b61a8aff48675097`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=HOST_SKILL_TRIGGER_NONTRIGGER_NACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-11 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。
- **`CASE-W1-11-SEC`**：`SEC`；**安全攻擊面／Input**=ChatGPT/Claude Portable Host 偽造 Protected Checker principal/receipt，跨 Host 或跨 SP 聲稱 Challenge Qualified；**Original Reader**=each original Host loader and protected Checker reader；**Expected WorldRaw**=host origin+skill sha+protected checker credential issuer and scope（當期 `EXPECTED_NOT_OBSERVED`）；**FirstFail**=`HOST_CHECKER_IDENTITY_CROSS_SURFACE_DENY`；**Scope**=同 Subject/SourceSHA/CandidateSHA/Host/PolicyEpoch 的受影效果；**Stop/Recovery**=reject counterfeit receipt; disable affected host entrypoint and restore LastGood；原 Runner=`RUNNER_UNBOUND`；status=`AUTHOR_CASE_DESIGN_NOT_NATIVE_EXECUTED`；`fixture_sha256=54fcec8996ab271df3a9010ac9a11b917db2519899f72d6b98d9d51e60d3fc9d`。**與同 WP NEG 的業務錯誤機制獨立**，不得互相抵證。
- **`CASE-W1-11-EDGE`**：`EDGE`；Trigger/Input＝獨立邊界或半成品擾動：Installed 後 loader 未 Loaded，或 Loaded 但 nontrigger 仍被啟動：不得宣稱 Used。要求保留原 Raw/last_good，依本 WP 退出 `原 Host disable/remove entrypoint、還原 last-good manifest；清理 residue` 後有界續工；UNKNOWN 禁重放。；`design_fixture_sha256=45b759a576b2b07290535e6eba72b8727fda367235b55757c7427ffbcedccf3f`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=HOST_SKILL_TRIGGER_NONTRIGGER_NACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-11 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。

**不共用四測試的根本條件**：本 WP 的 `SEC` 檢查 `用 TPM-SP 的 Loaded SHA 冒 Challenge-SP；Maker 以模型結論簽 Protected Checker`，`EDGE` 檢查 `Installed 後 loader 未 Loaded，或 Loaded 但 nontrigger 仍被啟動：不得宣稱 Used`。更換 CaseID 而保持 8 條同文屬 `CASE_SEMANTIC_DUPLICATE_NACK`。

### WP-FHS-17｜CAP-BOOT Native Occupants：四個不同輸入／Oracle／退出

- **Original Owner/Receiver**：原 HGK Issuer+Host Installer/Capability Registry；原依賴=WP-FHS-00, WP-FHS-02, WP-FHS-03；Original Registry/CaseID/Runner=`RUNNER_UNBOUND`（不自建正式 Case）。
- **Operation types**：SOURCE_READ:Need/qualified incumbent/Host installer provenance probe；HOST_OPS:minimum needed occupant original admitted install/load/invoke；`input_bytes` 與 expected type 以設計 fixture 可以重算，但原 Host Raw/`$id` 須原 Reader。

- **`CASE-W1-17-POS`**：`POS`；Trigger/Input＝對同 Subject/SourceSHA、受影 operation 執行原 Reader 候選驗證：NeedKey+scope、原 Policy Loaded ACK+HGK Issuer admitted installer+license/asset digest。預期 `Needed Capability 之 Installed/Loaded/Invoked/ConsumerACK+last-good，NONE=CAPABILITY_GAP_HOLD` 的 typed 原 Consumer 回條或具名 `HOLD`，不以檔案存在冒驗收。；`design_fixture_sha256=973419854ebc928437959747c73bb78f4701f4909284929cc65fec5b1da0b695`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=READER_ACK_OR_CAP_INSTALLER_ORIGIN_PARTIAL_ROLLBACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-17 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。
- **`CASE-W1-17-NEG`**：`NEG`；Trigger/Input＝從合法候選刪掉/錯配本 WP 必需前置：未有原 Issuer/Asset provenance 卻執行 Host installer；或第二套 Queue/Issuer 被包進工具。原 Reader 應 NACK，合法 READ/DRAFT 仍可續。；`design_fixture_sha256=80be3ebb6f04a23ecba2d7d3638e7c9d92ec98cce489e3d9e8d050a7df1b44b0`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=CAP_INSTALLER_ORIGIN_PARTIAL_ROLLBACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-17 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。
- **`CASE-W1-17-SEC`**：`SEC`；**安全攻擊面／Input**=未經原 Issuer/Installer 授權的代理持 Host admin token 安裝/載入工具；**Original Reader**=Original HGK installer and OS ACL reader；**Expected WorldRaw**=installer process SID/ACL/token issuer+write scope+binary pin（當期 `EXPECTED_NOT_OBSERVED`）；**FirstFail**=`CAP_INSTALLER_ADMIN_TOKEN_SCOPE_DENY`；**Scope**=同 Subject/SourceSHA/CandidateSHA/Host/PolicyEpoch 的受影效果；**Stop/Recovery**=deny installer, restore previous Host manifest, quarantine staged artifact；原 Runner=`RUNNER_UNBOUND`；status=`AUTHOR_CASE_DESIGN_NOT_NATIVE_EXECUTED`；`fixture_sha256=0e5b671baa7a164be080b95581b574704d1cd312b71979ade19814c2b90cade5`。**與同 WP NEG 的業務錯誤機制獨立**，不得互相抵證。
- **`CASE-W1-17-EDGE`**：`EDGE`；Trigger/Input＝獨立邊界或半成品擾動：Installer 解壓成功但載入失敗，需回上版 qualified last-good，不可把 Installed 當 Active。要求保留原 Raw/last_good，依本 WP 退出 `原 installer inverse/restore manifest+LoadedSHA+residue；不得 Git revert 取代 Host inverse` 後有界續工；UNKNOWN 禁重放。；`design_fixture_sha256=473e05189bac3f56fa01c83097459d0e1ca23c245f154ee2f723fe3657b0346f`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=CAP_INSTALLER_ORIGIN_PARTIAL_ROLLBACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-17 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。

**不共用四測試的根本條件**：本 WP 的 `SEC` 檢查 `未有原 Issuer/Asset provenance 卻執行 Host installer；或第二套 Queue/Issuer 被包進工具`，`EDGE` 檢查 `Installer 解壓成功但載入失敗，需回上版 qualified last-good，不可把 Installed 當 Active`。更換 CaseID 而保持 8 條同文屬 `CASE_SEMANTIC_DUPLICATE_NACK`。

### WP-FHS-20｜CLI/Agent/Host Kind Matrix：四個不同輸入／Oracle／退出

- **Original Owner/Receiver**：Original SBL Product×Host Cell owner/Reader；原依賴=WP-FHS-05, WP-FHS-16；Original Registry/CaseID/Runner=`RUNNER_UNBOUND`（不自建正式 Case）。
- **Operation types**：SOURCE_READ:original 192 Cell ledger, raw ON/OFF token, Host fit；LOCAL_DRAFT_WRITE:applicability selection/result matrix；HOST_OPS:affected Cell original Host reader probe when needed；`input_bytes` 與 expected type 以設計 fixture 可以重算，但原 Host Raw/`$id` 須原 Reader。

- **`CASE-W1-20-POS`**：`POS`；Trigger/Input＝對同 Subject/SourceSHA、受影 operation 執行原 Reader 候選驗證：CellID+original Kind/Mode/Host/RawToken，Host Capability/Provider state 原 Owner 必須核對。預期 `Selected/NotAffected/OwnerHold per Cell + raw Host-specific Consumer outcome` 的 typed 原 Consumer 回條或具名 `HOLD`，不以檔案存在冒驗收。；`design_fixture_sha256=bbfc2e1676c9b9cd6055b5f754ce76be137a082cb0319ce917b4bce171ccbd1d`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=READER_ACK_OR_CELL_TOKEN_OWNER_MAP_UNBOUND`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-20 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。
- **`CASE-W1-20-NEG`**：`NEG`；Trigger/Input＝從合法候選刪掉/錯配本 WP 必需前置：把 ON/OFF source token 私譯成 provider_off bool 或借不同 Host/Provider Raw。原 Reader 應 NACK，合法 READ/DRAFT 仍可續。；`design_fixture_sha256=d24697d250ba54e3a5c461d6eaac03e2a50999d101d6e1d02eede926803e917a`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=CELL_TOKEN_OWNER_MAP_UNBOUND`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-20 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。
- **`CASE-W1-20-SEC`**：`SEC`；**安全攻擊面／Input**=將另一 Host 的 Original Consumer credential／receipt 帶入此 CellID 以借用已 Qualified 狀態；**Original Reader**=Original SBL Kind×Mode×Host registry + per-host consumer reader；**Expected WorldRaw**=CellID+HostID+Kind/Mode raw token+credential audience/receiver nonce（當期 `EXPECTED_NOT_OBSERVED`）；**FirstFail**=`CELL_FOREIGN_HOST_CONSUMER_CREDENTIAL_DENY`；**Scope**=同 Subject/SourceSHA/CandidateSHA/Host/PolicyEpoch 的受影效果；**Stop/Recovery**=revoke mis-scoped credential; re-read own cell token; no boolean coercion；原 Runner=`RUNNER_UNBOUND`；status=`AUTHOR_CASE_DESIGN_NOT_NATIVE_EXECUTED`；`fixture_sha256=a47792918c52f5723c1c62bfc508245231203126412097544f6dab3667a0ce75`。**與同 WP NEG 的業務錯誤機制獨立**，不得互相抵證。
- **`CASE-W1-20-EDGE`**：`EDGE`；Trigger/Input＝獨立邊界或半成品擾動：Same Kind/Mode 從 Hermes 改到 Codex，原 Cell ID 改變；舊 Cell receipt 不可重用。要求保留原 Raw/last_good，依本 WP 退出 `撤受影 Host adapter/probe，恢復同 Need qualified last-good，保留 raw ON/OFF` 後有界續工；UNKNOWN 禁重放。；`design_fixture_sha256=e1c4ac1e7397df8542280485d763b1fc2178626dcdacdab4a33012eaaae5d58b`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=CELL_TOKEN_OWNER_MAP_UNBOUND`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-20 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。

**不共用四測試的根本條件**：本 WP 的 `SEC` 檢查 `把 ON/OFF source token 私譯成 provider_off bool 或借不同 Host/Provider Raw`，`EDGE` 檢查 `Same Kind/Mode 從 Hermes 改到 Codex，原 Cell ID 改變；舊 Cell receipt 不可重用`。更換 CaseID 而保持 8 條同文屬 `CASE_SEMANTIC_DUPLICATE_NACK`。

### 2.1 原 Case/Runner/Oracle/Raw 每件的實體欄位契約

| 欄位 | 對 32 個設計 Case 必需的內容 | 目前合法狀態／拒收 |
|---|---|---|
| design_case_alias | CASE-W1-xx-POS/NEG/SEC/EDGE | LOCAL_AUTHOR_DESIGN_ONLY |
| original_case_id | 由原 PIPD/TQAEP、HGK/Host/Cell Registry 按 affected requirement 查 | ORIGINAL_CASE_ID_UNBOUND；不得填虛構 ID |
| original_registry_sha | 原 Reader source/effective version 的 64-hex digest | ORIGINAL_CASE_REGISTRY_SHA_UNBOUND |
| runner_entry | module/binary origin/version/command/args/OS principal/runnerSHA | RUNNER_UNBOUND，不能報 runnable |
| input_fixture_sha256 | 本表每件不同 design fixture byte SHA | AUTHOR_STATIC_PIN_OK；Host fixture 要同 Reader rebind |
| expected_world_raw_schema | 真 Host 原 Consumer stdout/stderr/exit/WorldDiff typed schema | $id=ORIGINAL_RAW_SCHEMA_UNBOUND |
| oracle_ref | 個別原 Requirement/OriginalCase/FUO 的 Original Oracle | ORIGINAL_ORACLE_REF_UNBOUND 只阻該 Case |
| checker_principal | Protected Checker 與 Maker 不同原保護身份 | CHECKER_NOT_RUN；作者不得簽發 |
| requalification_scope | 同 Subject/Candidate/Scope/Host/PolicyEpoch/SourceSHA/Need | 只重跑 affected cone |

## 3. 唯一五 Seam：與 L0／L2 同名同義的原 Reader Resolver（無平行 ID）

**S0 pre-intake（非 Seam）**：Owner Goal→ TPM PM/SE/TPgM 三 SPEC。`S1` 不是這一段，必以 原 Source/Intent/Profile→PI 為準。五 Seam 與 `01 §4` 使用同一列資料來源／No Canonical `$id` 自造：

| SeamID | 不可更改的原義 | Original Producer | Original Reader | Original Consumer | Input | Output/FirstFail |
|---|---|---|---|---|---|---|
| S1 | Source／Intent／Profile → strict PI | SBL TPM PM/SE/TPgM + SourceAuthority | 原 PIPD Intake/Authority/Profile 與 PI Reader | SBL-hosted 原 PI Writer | OriginalID/SourceSpan/SHA/Parent/NEG, 3 SPEC SHA, safety veto | strict PI-PKG（Sidecar 不進 Canonical） / S1_SOURCE_PI_AUTHORITY_NACK |
| S2 | PI → PD／ECP／TQAEP | SBL-hosted 原 PI Writer | 原 RepoContext PD Binder + ECP Effect Reader + TQAEP Case Reader | 原 PIPD PD/ECP/TQAEP Writer 與原 HGK 受影適配 Consumer | PI digest/Subject/Candidate/SourceSHA + local Git root/HEAD/dirty/untracked/preimage + OperationType + OracleRef | PD/DEV ECP/OPS ECP/Planned TQAEP 分出口 / S2_PI_PD_REPO_BIND_NACK |
| S3 | Native PLAN／Fabric Active Policy → HGK Admission | 原 Native PLAN Producer + Fabric Policy Owner | 原 PLAN CurrentRevision/CAS Reader + Fabric ActiveEpoch/LoadedDigest Consumer Reader | HGK 原 Registry/Issuer/WorkOrder/Receiver | CAS base_revision/proposal_hash/Writer ACK + ActiveEpoch/LoadedSHA/ConsumerACK + Scope/HostID/Issuer ACL | 原 HGK admission／WorkID（僅實機原 Issuer 有權建立） / S3_PLAN_POLICY_ADMISSION_NACK |
| S4 | HGK WorkID → Hermes／Codex → WorldRaw | HGK Original WorkID/SharedSpine/Lease | 原 Hermes v0.22.5 Dispatcher/Bounded Worker/Journal Reader | Original WorldRaw／Journal Consumer | OperationID/idempotency/LeaseGen/WorkerPID/ActualServed/Raw stdout stderr exit/diff | WorldRaw + checked journal cursor 或 UNKNOWN / S4_WORK_WORLD_RAW_NACK |
| S5 | Raw／Original Oracle → Protected Checker／Publisher | Original WorldRaw + Case/Oracle Owner | 原 Protected Checker Reader（分離 principal） | Original Publisher／Release Consumer | 同 Subject/Candidate/Scope/Host/Epoch、OracleSHA、POS/NEG、Maker≠Checker | 獨立 verdict（若真執行）及 W4 Publisher readback / S5_CHECKER_PUBLISHER_SCOPE_NACK |


**Seam 原 Host/$id Resolver**：對每列依次 `source manifest SHA→original reader/version/registry→input_schema_id/version/digest→function entry/CLI args→output strict body or sidecar→NACK code/raw location→same subject/source/scope verify`；缺實體欄位為 `ORIGINAL_SCHEMA_BIND_HOLD`，不能把本 Markdown 的 `SeamContract@design` 當原 ABI。S3 的 Native PLAN CAS ACK 是硬前置，Fabric Source/Stage/OwnerApproval/ActiveEpoch/LoadedSHA/Consumer ACK 需分開測，然後原 HGK Registry/Issuer 才准相應 effect。

## 4. RepoContext／DEV/OPS／安全效果分級與退場

| EffectClass | 最小 permission/preimage | 可驗 POS | NEG / Stop & Rollback |
|---|---|---|---|
| SOURCE_READ | 原唯讀 ACL/SourceSHA/Reader timestamp | 原 Source Reader 可重讀 | 無 Permit 不拒全部 READ；出錯重讀，不製造 world diff |
| LOCAL_DRAFT_WRITE | 用戶授權隔離目錄、preimage=ABSENT 或同路徑當期 SHA | 非重複 W1 draft、可清除 | 不得碰三庫；刪/回復隔離檔 |
| DEV_REPO_WRITE | 原 live repo HEAD/branch/index/untracked/preimage+exact WriteSet+DEV ECP+HGK admission | 真世界 diff/commit/raw、rollback commit | 跨 WriteSet、stale HEAD 拒；W2 不能借 GitHub HEAD |
| HOST_OPS | HostID/OS principal/loaded epoch/nonce TTL/OPS ECP+原 Issuer/receiver | 真 install/load/invoke/consumer/readback | Stage 冒 Active，Host backup 不合格；原 Installer inverse |
| USER_EFFECT | User Consent/DataScope/Receiver origin/compensation | 真 consent+world result | 缺同 Scope consent 停受影；最小撤回補償 |
| RELEASE_EFFECT | Original Publisher + GHP02 + protected Checker + reversible release | 原 Published readback | W4 before not granted；禁止 Maker/CI green 自簽 |

## 4.1 W1 真現役 SBL-hosted PIPD PRE-V2 @2 original Reader／CLI Resolver

**來源**：遠端 SBL `integrations/pipd/src/pipd_ls_sp/cli.py` `COMMANDS` exact 13、`registry.py` 19 family，`pipeline.py` 原 Compiler；U04 `docs/pipd-migration/U04-CUTOVER.md` 記錄唯一 canonical writer 已轉至 SBL。此為遠端 Repo 檢視，不能取代本機 `pipd doctor` / 原 `pre_v2.py` Reader 載入；`compile-cc` **不是**第 14 CLI。Strict canonical JSON 不容 @2 `_profile_meta` 插入，Source Crosswalk@2、ECP Intent@2、PlannedTQAEP@2 只是分離 sidecar。最後的原 Caller NACK/Raw 只能從 original CLI。正式原 Writer 未於本次執行。

| 階段／技能 | 現役 entry/Schema Reader (原路徑定位) | Producer→Input | 原 Consumer / Output | strict 與 sidecar | 最先拒收／HOLD |
|---|---|---|---|---|---|
| intake / pipd-route-intake | SBL integrations/pipd/.../cli.py `intake` → pipeline.intake | W0 Goal+Source locators+constraints | IntentCard/RequirementAtoms → PIPD intake Reader | Card is original; SBL source ledger separate | INTAKE_INVALID/AUTHORITY_UNKNOWN, source not contained |
| authority / pipd-authority-source | pipeline.freeze_authority + Original Authority Reader | Source manifest, file SHA, authority rank, conflicts | AuthorityBinding/SourceFreezeManifest candidate | Original owner ack distinct from author snapshot | AUTHORITY_UNKNOWN/OWNER_SOURCE_CURRENTNESS_HOLD |
| profile / pipd-profile-tailor | cli.py `profile` + profiles.compute_profile | axes 9, safety veto | ProfileBinding strict+non-record metadata sidecar | `_profile_meta` never inserted strict PI | PROFILE_VETO/UNDERSPECIFIED_SAFETY |
| compile-pi / pipd-pi-compile | cli.py `compile-pi`+pipeline.compile_pi | IntentCard+frozen source/profile | nonempty PI-PKG + trace source atom rederive | strict PI only; SBL.PI.Crosswalk@2 sidecar separate | PI_SCHEMA/PI_SEMANTIC/TRACE_FAIL |
| bind-pd / pipd-pd-bind | cli.py `bind-pd`+repo_context.derive_repo_context | canonical PI + LIVE local Git root/HEAD/branch/dirty/untracked/preimages | PD-PKG or RepoBindingRequest, Original PD Consumer | Caller `--head` is claim, not currentness | REPO_CONTEXT_MISSING/STALE_PROVIDER |
| compile-ecp / pipd-execution-contract | cli.py `compile-ecp` + operation_registry original contract | PD+PI+EffectIntent+trusted OperationRegistry | effect-specific DEV/OPS/USER/RELEASE intent→original ECP Writer | SBL.ECP.INTENT@2 separate sidecar, never Permit | EFFECT_UNKNOWN/ECP_PERMISSION/REGISTRY_NOT_CANONICAL |
| compile-tqaep / pipd-assurance-tqaep | cli.py `compile-tqaep`+original Case/Oracle Reader | PI+ECP+original per-case POS/NEG fixture+separate protected checker | planned TQAEP / Original TQAEP Reader | PlannedTQAEP@2 not Checker Receipt | TQ_TRACE/TQ_ORACLE/TQ_SOD/RUNNER_UNBOUND |

**命令 reader 次序**：優先現役 `pipd doctor` 取 installed schema source（OVERRIDE→INSTALLED→SOURCE）、`pipd --help` 讀 verb set、registry 檢 19 families、八 skill packs 各自 Manifest；再以原 CLI+pin 真實 source hash 的非空輸入做正反例。W1 文件作者不執行宿主，故本輪 `ORIGINAL_PIPD_READER_BIND_HOLD`；輸出位置必用使用者授權隔離 root，寫正式 Canonical/TargetRepo 則需原 Writer 和作用域許可。`--head`/remote Git SHA 只能作比較，不能作本機 RepoContext。

## 5. Hermes v0.22.5 原 RunBudget／UNKNOWN／Stop-Resume 逐 Effect 類型決策表

`RunBudget` 的 runtime/cost/turns/credential/lease 真數值 **UNBOUND**：由現役 Host profile/issuer/journal 原 Reader 設定，作者不得私造 timeout、無界 retry 或憑空預批准。有限工作由原 Hermes Kanban/WorkID/Journal 做 durable resume；本文不建立第二 Scheduler/Queue/Database。

| Effect / OperationType | Retry 前提與 idempotency | Wake/Checkpoint/Raw | FirstFail/Stop | Resume / compensation/last-good | Owner escalation |
|---|---|---|---|---|---|
| SOURCE_READ | 同 ACL、同 SHA/SourceEpoch，可有界重讀 | source cursor/hash/error; 不需 OPS Permit | SOURCE_STALE / READ_ACL_DENY | 重新唯讀 SourceReader、不得製造世界 diff | source owner only on changed authority |
| LOCAL_DRAFT_WRITE | 同一隔離 Root / candidate hash / preimage；重寫需 CAS | draft SHA/cleanup checkpoint | DRAFT_SCOPE_ESCAPE / PREIMAGE_CHANGED | 刪除本輪私有候選或回前 SHA；不碰三庫 | Owner only if write scope disputed |
| DEV_REPO_WRITE | 同 Scope+current Git HEAD+preimages+operation idempotency；UNKNOWN reconcile first | commit/working diff/exit/test/raw; WorkID | REPO_HEAD_STALE / WRITESET_ESCAPE | 原 Repo Writer 回退 commit/restore preimage，不重放非冪等寫 | new WriteSet/ACL needs original approval |
| HOST_OPS | 原 Issuer nonce TTL epoch/ACL 同 Subject/Host；實機讀 world before retry | Host loaded/installed/WorldRaw/lease cursor | PERMIT_TTL_EXPIRED / UNKNOWN_HOST_EFFECT | 原 Installer inverse或原 Host Snapshot；residue 具名，不 git revert | expired credential, new Host or changed effect asks Owner |
| USER_EFFECT | original consent/data scope same task; never reuse expired consent | consent ref + receiver raw/data audit | CONSENT_EXPIRED_OR_SCOPE_MISMATCH | 停敏感外呼、original consent owner compensation/revoke | new data scope/consent required |
| RELEASE_EFFECT | 原 Publisher + protected Checker + GHP-02；no autonomous retry on unknown | release channel/version/receipts | PUBLISHER_OR_CHECKER_MISSING | 原 Publisher rollback/retire，保留 release provenance | fresh Owner/Publisher decision required |

**共同拒收與退出**：`UNKNOWN` + non-idempotent operation 沒有原 World Readback 時 `RECONCILE_REQUIRED`，不重新 enqueue 新 WorkID；lease_gen stale 不承認；選擇了模型卻缺 ActualServed 不能判任務已執行。`missing_budget` 僅 HOLD 受影長任務 effect，不阻合法來源查詢或隔離草稿。

## 6. W0→W1 與 W1→W2 雙向 typed handoff（作者端 envelope，不是 Canonical JSON）

### 6.1 `AUTHOR.FHS.W0ToW1Candidate@design` 真 Receiver contract

```yaml
record_type: AUTHOR.FHS.W0ToW1Candidate@design
subject_id: ORIGINAL_SUBJECT_ID_OR_HOLD
candidate_id: W0_CANDIDATE_ID_OR_HOLD
scope_id: ORIGINAL_SCOPE_ID_OR_HOLD
source_manifest_sha256: SOURCE_MANIFEST_FROM_W0_OR_HOLD
three_speccandidates:
  product: {ref: ORIGINAL_W0_PRODUCT_SPEC_REF_OR_HOLD, sha256: ORIGINAL_SHA_OR_HOLD}
  architecture: {ref: ORIGINAL_W0_ARCH_SPEC_REF_OR_HOLD, sha256: ORIGINAL_SHA_OR_HOLD}
  program: {ref: ORIGINAL_W0_PROGRAM_SPEC_REF_OR_HOLD, sha256: ORIGINAL_SHA_OR_HOLD}
original_w0_wp_outputs: {WP00: EXPECTED_OR_HOLD, WP01: EXPECTED_OR_HOLD, WP15: EXPECTED_OR_HOLD, WP16: EXPECTED_OR_HOLD, WP21: EXPECTED_OR_HOLD}
original_source_ledger: SBL14_AND_FHS17_SHA_INDEX_OR_HOLD
original_atom_parent_neg: ORIGINAL_READER_SUBCLAUSE_SET_OR_HOLD
question_ledger: {key: [subject, source_sha256, scope], known_answers_only: true, decisions_q01_q10: PROPOSAL_NOT_RATIFIED}
u0_u4_affected_status: NOT_EXECUTED_BY_ORIGINAL_READER
producer: W0_AUTHOR_OR_ORIGINAL_PRODUCER
receiver: W1_ORIGINAL_PIPD_POLICY_HGK_READERS_BY_AFFECTED_SCOPE
claim_ceiling: AUTHOR_DESIGN_ONLY
```

**原子級 NACK**：三 SPEC 漏一份/三個 ref 重複且無獨立 role/任一 SHA 非 64-hex `W0_SPEC_ROLE_OR_SHA_NACK`；同 Subject/Scope/SourceSHA 不一致 `HANDOFF_JOIN_NACK`；負條款 Parent/NEG 尚未查證 `AFFECTED_SEMANTIC_HOLD`；Q01–Q10 只是 Proposal 不得投為 OWNER_APPROVED；三 SPEC 缺件時合法 READ/DRAFT 可續、affected PI promotion 必 HOLD。W0 r2 本身是 Blueprint&Skeletal 設計，**不假造已生成三個正式原 TPM SPECDraft SHA**。

### 6.2 `AUTHOR.FHS.W1ToW2Candidate@design` 原樣本體內完整受影欄位

```yaml
record_type: AUTHOR.FHS.W1ToW2Candidate@design
subject_id: SAME_AS_W0_RECEIVED
candidate_id: SAME_ORIGINAL_LINEAGE_AS_W0_RECEIVED
scope_id: SAME_SCOPE_OR_EXPLICIT_AFFECTED_REBIND
source_manifest_sha256: SAME_PINNED_SOURCE_OR_AFFECTED_DELTA
original_repo_context: {local_root: ORIGINAL_REPO_PROBE_REQUIRED, head: LOCAL_HEAD_OR_HOLD, preimages: LIVE_PREIMAGES_OR_HOLD}
seam_contracts: [S1_SOURCE_TO_PI, S2_PI_TO_PD_ECP_TQAEP, S3_PLAN_POLICY_TO_HGK]
per_wp:
  WP02: {source_read: SOFT_ALLOWED, policy_host_effect: HARD_IF_POLICY_CONSUMED, original_raw: EXPECTED_NOT_OBSERVED}
  WP03: {registry_read: SOFT_ALLOWED, issuer_effect: HARD_IF_OPS_DEV, original_raw: EXPECTED_NOT_OBSERVED}
  WP04: {journal_read: SOFT_ALLOWED, runtime_wake: HARD_IF_REAL_WORK, original_raw: EXPECTED_NOT_OBSERVED}
  WP05: {local_draft: SOFT_ALLOWED, original_pi_ack: HARD_IF_PD_ECP_CONSUMED, original_raw: EXPECTED_NOT_OBSERVED}
  WP07: {plan_proposal: SOFT_ALLOWED, original_cas_ack: HARD_IF_ADMISSION, original_raw: EXPECTED_NOT_OBSERVED}
  WP11: {skill_plan: SOFT_ALLOWED, loaded_skill: HARD_IF_SKILL_CONSUMED, original_raw: EXPECTED_NOT_OBSERVED}
  WP17: {cap_probe: SOFT_ALLOWED, installer_ack: HARD_IF_REQUIRED_OCCUPANT_MISSING, original_raw: EXPECTED_NOT_OBSERVED}
  WP20: {cell_index: SOFT_ALLOWED, host_cell_probe: HARD_IF_AFFECTED_CELL_CONSUMED, original_raw: EXPECTED_NOT_OBSERVED}
next_operation_class: SOURCE_READ_OR_DRAFT_OR_DEV_OR_OPS
necessary_predecessor_ack: COMPUTE_FROM_ORIGINAL_OPERATION_EFFECT_AND_E01_E36
blocked_wp: ONLY_AFFECTED_OPERATION_WITH_NAMED_FIRSTFAIL
non_applicable_wp: DISTINCT_NA_BY_ORIGINAL_READER
optional_readonly_wp: ONLY_WITH_EXISTING_READ_PERMISSION
w2_allowed_output: AUTHOR_DESIGN_HANDOFF_WITH_HOLDS_NOT_NATIVE_PERMIT
claim_ceiling: AUTHOR_DESIGN_ONLY
```

**Hard/Soft W2 判定式**：`HARD(WPxx,next_op) iff OriginalConsumer(next_op) consumes WPxx's original ACK/raw AND OriginalEffectRegistry(next_op) requires that evidence`；`optional` 只對來源/草稿可用；`N/A` 必由原 Reader 與 same Scope 證明；blocked 只阻受影 operation。W2 第一個 `DEV_REPO_WRITE`（WP06）必按 L2 維持原 `WP02/03/04/05/17` 五前置，不能把 WP17 加成需要 WP06 的反向依賴。原 WP07 是 Native PLAN CAS，W2 WP08 實際 effect 才消費它，不可預支收據。

**回退**：若 W0→W1 兩端 `source_manifest_sha256` 改，僅使受影 PI/PD/ECP 失效；若 Repo HEAD 改、PI Source 不變，僅重綁 affected PD/ECP；若 Policy Epoch 改，重新取得原 HGK Loaded/ACL/Issuer ACK，保留已合法完成的 Source/Draft。所有 HandOff/Reader Raw 未見時只標 `EXPECTED_NOT_OBSERVED`。

## 7. 單一 Human Owner 的最短預授權接線（只復用原 Issuer，不自建 Grant）

`Owner → existing original Authorizer/Policy Reader → approved bounded OwnerGrantRef@original (if original schema supports) → original HGK Issuer scoped decision per EffectClass/operation → Hermes original WorkID/Lease → WorldRaw → Protected Checker`。這是 **建議接收路由**，未確認原 HGK Registry 有同名 `OwnerGrantRef` Schema 時標 `OWNER_GRANT_SCHEMA_HOLD`。Human Owner 是一名，Maker/Issuer/Checker/Publisher 的 OS SID、Credentials 與 Trust 必分開，任何模型不讀保護 Secret。Owner 的已知答案只有 Subject+SourceSHA+Scope 相同才重用。

| 原預授權元素 | 最小所需內容／Consumer | 允許續工 | 失效/FirstFail |
|---|---|---|---|
| OwnerGrantRef@original | original Owner/Issuer ledger reference, not prompt YES | 原 reader 確認同 scope/expiry 下必要 Class | OWNER_GRANT_SCHEMA_HOLD |
| allowed_effect_classes | READ/DRAFT by existing permissions; DEV/OPS/USER/RELEASE original per-class scope | 僅 affected class | EFFECT_CLASS_SCOPE_NACK |
| exact scope+expiry+operation limit | HostID/PID/TaskKind/WriteSet/sensitive data boundaries | 同 scope 未過期的原批准可重用 | STALE_SCOPE_OR_TTL_NACK |
| original issuer & revocation | HGK issuer/nonce/TTL+Owner revocation route | 每 effects 原 Reader admissible才執行 | NO_SECOND_ISSUER / REVOKED_CREDENTIAL |
| escalation | 新增或變更 scope、secret/data export、發行、過期或 UNKNOWN 無法回讀 | 只問受影 Owner 問題 | OWNER_ESCALATION_REQUIRED |

**一輪人工操作流程**：Owner 一次審閱受界 `Scope/EffectClass/Expiry/MaxOperations/SensitiveData`；原 Registry 有效才復用；Hermes 長任務僅用原 WorkID 及原 Journal、必要時 Wake；超限、scope 漂移或 consent 變更才請原 Owner 再批准。此設計不因單人而取消 Protected Checker 獨立技術資格，也不把問卷 Q01–Q10 選 A 當成真 Owner approval。

## 8. 按誰能解的受影 HOLD 卡：Original Reader、最小 Raw、首敗與續工

| HOLD ID | 影響範圍 | 真正責任 Owner | Original Reader 最短定位 | 只需讀回什麼 | 本輪可做/局部阻斷 | 最小 Resume predicate |
|---|---|---|---|---|---|---|
| H-S1-SOURCE | CH12/13 WP05 strict PI | SBL/PIPD Original Source/PI Reader | SBL `integrations/pipd/src/pipd_ls_sp/pipeline.py` + original source file reader | 原 source/authority/profile/PI schema IDs+ACK/Parent/NEG | AUTHOR_DRAFT_ALLOWED; BLOCK_PI_PROMOTION | OriginalPIReader: same Subject/SourceSHA atom/NEG positive+negative rederive |
| H-ORIG-SEM | CH08–40 Source SCL candidate mapping | SBL14/FHS17 original domain owners | 每個 `SCL-W1` 的 physical SourceKey+Line+SHA; original U0–U4 Reader | OriginalID/Parent/Child/NEG+consumer/case owner semantic ACK | AUTHOR_CROSSWALK_VALID; FORMAL_SEMANTIC_CLOSURE_HOLD | 原 Reader per affected SCL ref returns ACK/NACK |
| H-REPO | CH14 WP05 PD, W2 WP06 | Original SBL RepoContext/PD Owner | local repo_context.derive_repo_context; GitHub `main` non-authoritative | live git root/HEAD/branch/index/dirty/untracked/preimage+ACL | BLOCK_PD_FOR_WORLD_WRITE; SOURCE_READ_ALLOWED | local repo and original PD Reader agree same HEAD & Scope |
| H-POLICY | CH17 WP02 policy host operation | Fabric Policy Owner+HGK Consumer | Fabric `FABRIC/fabric/consumers/hgk_policy_consumer.py` pointer, original live Fabric/HGK reader | OwnerApproval/ActiveEpoch/LoadedDigest/ConsumerACK/HostID | BLOCK_AFFECTED_OPS; POLICY_SOURCE_READ_ALLOWED | ActiveEpoch and LoadedACK match same subject/process |
| H-ISSUER | CH18/39 WP03/17 effects | HGK Original Registry/Issuer Owner | HGK original private Native Registry/Receiver/Process ACL readback | signed scope nonce TTL issuer origin PID/SID EffectClass | BLOCK_AFFECTED_PROTECTED_EFFECT; DRAFT_ALLOWED | Original HGK validates grant+scope+policy epoch |
| H-HERMES | CH19/20 WP04 runtime wake | Original Hermes Host Runtime Owner | Hermes original ProfileLoader/three-lane dispatcher/journal (local Host, not GitHub) | fresh PID, pinned v0.22.5 profile SHA, required/selected/invoked/actual served, journal | BLOCK_REAL_RUNTIME; SOURCE/DRAFT_ALLOWED | same PID/WorkID actual served and world raw readback |
| H-PLAN | CH34 WP07 native CAS | Original HGK Native PLAN Writer | original PLAN CurrentRevisionReader/CAS Writer (not legacy skill) | base_revision/proposal hash/Writer ACK | ALLOW_ADVISORY; BLOCK_NATIVE_PLAN_ADMISSION | original CAS Writer emits same subject revision ACK |
| H-HOST-SP | CH08/22 WP11 Host cells | each original Host Skill/Plugin Owner | actual Host loader/OS process/Profile/Installed/Loaded/Invoked Reader | per SP×Host packsha+trigger/nontrigger+Used/Remove raw | ALLOW_SKILL_PLAN; BLOCK_HOST_QUALIFIED | each applicable cell original loader readback |
| H-TOOLS | CH22 WP17 needed occupant | Original Host Installer/Technology Owner | original installer manifest, release asset digest/NOTICE and Host registry | pin/license/OS arch/installer preimage+loaded/invoked/consumer ack | BLOCK_MISSING_AFFECTED_CAPABILITY_ONLY | qualified occupant or original NoFit reason with owner |
| H-CELL | CH19/40 WP20 affected Cell | Original Product×Host Cell Owner | FHS BODY-09B raw token + original Host/Provider Reader | same CellID Host Kind Mode raw-token semantics owner ACK | BLOCK_AFFECTED_PROVIDER_EFFECT; INDEX_READ_ALLOWED | original owner resolves token mapping same Cell+Host |
| H-RUN | CH20 W2 task recovery | Hermes/HGK Journal/RunBudget Owner | original WorkID/Lease/Journal/OperationType Registry | actual RunBudget limits/idempotency/wake path/last-good | BLOCK_UNBOUNDED_AUTONOMY_ONLY | original reader supplies bounded budget & unknown reconcile |
| H-TQAEP | CH40 WP05 original Case | PIPD original TQAEP+Protected Checker Owner | original CaseRegistry/Runner/OracleRaw / Checker inbox | per-case runner/fixture/oracle raw+distinct Checker credential | PLAN_CASE_ONLY; NATIVE_CHECKER_NOT_RUN | Original Checker executes same scope/candidate case |
| H-OWNER-Q10 | Owner 10 question proposals | Human Owner via original authority | original QuestionLedger keyed Subject+SourceSHA+Scope | real ratification ref per actually consequential decision | NO_AUTOMATIC_GRANT; AUTHOR_DESIGN_ALLOWED | Owner approved through original channel with readback |

**讀取時間/Last Probe**：本輪 GitHub 僅能核對 Fabric FHS-NAV/v2 導航、SBL U04 與來源 `pipeline.py/cli.py/registry.py`；Windows 原 Host 的 `LastProbe=NOT_OBSERVED`，不可把 Git blob SHA 當本機 PID/Profile/Loaded。影響最小化：H-CELL 未核不停止 W0 三 SPEC，H-POLICY 未核不停止 SOURCE_READ，H-TOOLS 未核不將 Default30 強降 Optional。原 QuestionLedger 已知且適用答案可以直接復用，不建立第二批准資料庫。

## W1-r5｜W0→W1→W2／W3／W4 可施工欄位與移交關係

**接收 W0（唯讀）**：`Subject, Candidate, Scope, original_source_manifest_sha, W0 3-spec refs+digests, OriginalID+Parent+NEG, KnownAnswer QuestionLedger keyed subject/source/scope, authority/currentness, W0 FirstFail/HOLD, original ledger`; W0 缺三 SPEC 的一份會在受影原 PI promotion 前停止，非受影來源讀取繼續。

**本 W1 唯一設計寫入**：W1 WaveCurator 的本次 L3 正文＋非規範附錄，日後 W1 DraftMaker 的單一 `W1_草案` 受界 WriteSet；其他波及原三庫 Registry 不在寫入集合。每個主章抽取 `OriginalSourceSpan+SHA+OriginalID+subclause+applicable Kind/Mode/Host/Need+POS/NEG/ExpectedRaw+Consumer+FirstFail+Disposition`；十個欄位未必對 READ 同時非空，但未適用時須有原 Reader N/A 理由。

**交 W2**：`SameSubject/Candidate/Scope/SourceSHA+S1/S2/S3 Original Reader-binding request; WP02/03/04/05/17 needed ACK/Host occupants; WP07 original PLAN CAS; E06-E10/E14 的依賴；effect-specific ECP/TQAEP planning; Read/Draft legal siblings; STOP/RESUME/ROLLBACK per effect`。無 original writer ACK 或真 Repo/Host/Issuer 只能帶 `HOLD`，不是可直接執行 `WorkOrder`。W2 才做 WP06 等受准入可逆世界效果。

**交 W3**：W1 PortableHost SP×Host applicability/loader/true trigger/nontrigger 觀測期待、192 Cell raw legacy ON/OFF 原 token 解析 HOLD、Native20/Default30 受影 Occupant/last_good、W18 普通 Goal 的強制 Profile/ActualServed 資格前件；W3 主責全產品 949/149/50 Parent/39/96/192/282 與 27→31 的適用分母，不把 W1 圖視為全量資格化。

**交 W4**：對 L3 文檔作者端 `AUTHOR_FINAL_SCOPED`、TraceClosure／Original Reader 受影 ACK/NACK／NonApplicable、CI/License/NOTICE/SBOM、GHP-02/Publisher 准入，只提交候選與待驗證證據；不存在的 Checker/Release Receipt 不准生成。

<!-- HISTORICAL_R5_SKELETON_FILL_REQUEST_SUPERSEDED: transition wording only; all substantive constraints retained -->
**下一階段製程**：`W1_藍圖&skeleton`＝已明列 W1 設計及空位 → `W1_草案`＝由唯一 DraftMaker 填真 SourceSpan/Original Reader/Case/ExpectedRaw 及具體可提交候選 → `W1_定案`＝由 W1 DesignCurator 消費適用 Original Owner 同 Scope ACK/NACK/HOLD，僅能聲稱 `AUTHOR_FINAL_SCOPED`，不構成原 Canonical/Native 授權。差額保留 supersedes SHA/last_good，重審只重跑 affected Source/CH/Case/WP。


<a id="ch-00"></a>

## R1｜2026-11-06 受界基準同步修訂（W1，作者端）

**修訂識別**：R1-2026-11-06；對象為 W1 r2 正文，五千四百零九行，sha256 本輪重算相符（e40df299 起、938669ce 迄）。本節為追加式修訂：原文一字未改，回復參照即該 sha256，取代範圍仍限於 W1 作者端設計。凡與原文並讀而有衝突，以本節的更正段為讀法；凡屬歷史章節者，保留當時事實，不因本節改寫。

### 一｜法位與上限

本節的法位是作者端隔離草稿寫入，不是原生效果。因此不改寫原封存、不改寫原歷史正文、不動任何儲存庫（本輪變更為零），不簽發許可，不發行（發行狀態為未授予）。

主張上限只到「作者端對帳、帶具名未解項」（AUTHOR_SIDE_RECONCILED_WITH_SCOPED_HOLDS）。不得由此升為原生、獨立、已發佈或已發行；也不得用「已對帳」三字吸收任何一筆未解項。

四條界線不可互換。第一，合併不等於原域接收：合併只證明該分支已入主線，不證明原 Fabric Policy、原 HGK Issuer 或原 SBL Reader 已接收該內容。第二，作者端測試不等於獨立檢查者，產製方不得自簽通過。第三，暫存或文件成功不等於已載入，不得以暫存狀態充當生效版本或已載入摘要。第四，遠端主線不等於本機儲存庫脈絡，本機複本仍非主線且帶未提交變更。

沿用且本輪未變者：原 Owner 批准未觀察、原生主機端到端未執行、獨立檢查者未執行。三者任一未取得，本節即不得記為已達；本輪亦未取得任何一項。另有一條程序限制：本節不得以文檔升版解除任何具名未解項，只能把它改寫成可重啟的未解項並附上重啟條件；凡未附條件者，視為未解仍在。

### 二｜八個 Primary WP 主責不變之聲明

本修訂不移動、不合併、不刪除 W1 的八個主責工作包，順序與章綁定照原文固定：政策消費（WP-FHS-02，配第十七與十六章）、註冊與簽發（WP-FHS-03，配第十八與三十九章）、耐久執行環境（WP-FHS-04，配第十九與二十章）、PIPD 原生編譯（WP-FHS-05，配第十二、十三、十四與四十章）、原生計畫甲乙丙（WP-FHS-07，配第三十四與十六章）、可攜主機試用（WP-FHS-11，配第八與二十二章）、開機能力佔位（WP-FHS-17，配第二十二與十八章）、種類與主機矩陣（WP-FHS-20，配第十九與四十章）。

同時不變者有四。原二十二個工作包與三十六條有向邊的方向不改，不新增第二十三個工作包，也不新增第三十七條邊。上游 W0 的六個工作包與下游 W2 的四個工作包，其責任不因本節移動。本節不接管上游與其他波的寫入集合，不轉移的規則維持原樣。原文既有的受影識別、來源卡識別、子義識別與未解項識別一律保留，無一改號，無一刪除。八個工作包的分母、二十二個工作包的全量與三十六條邊的總數，亦不因本節的任何一句而變動；本節只改讀法，不改分母。

### 三｜封存後主線讀回（W1_POST_ARCHIVE_MAIN_READBACK）

W1 執行封存在十一月五日讀回時，把三個候選提交記為未合併。十一月六日實測，三者皆已合併。下表只追加讀回，不回寫歷史：原文與封存中的「當時未合併」是當時事實，不得改成「當時已合併」，也不得反推封存當時已驗收。

| 儲存庫 | 提交 | 封存時狀態 | 封存頭 | 當期狀態 | 合併提交 | 合併時間 |
|---|---|---|---|---|---|---|
| SBL | #43 | 未合併 | 4e8c9c05 起 | 已合併，6 檔 | ad7398651e | 2026-11-05T11:21:46Z |
| Fabric | #29 | 未合併 | 77120677 起 | 已合併 | 2ad3f77983 | 2026-11-05T11:22:01Z |
| HG-KSEOS | #13 | 未合併 | 0b1d40d8 起 | 已合併 | b013b6d432 | 2026-11-05T11:22:06Z |

三庫主線亦已前移。SBL 主線為 8f5161a306d46775b71ff2bc7817e447cfd8f96e（主線提交時間十一月六日七時三十八分五十六秒，由 #47 的合併帶入，合併時間為同分五十七秒）；Fabric 主線為 ef4fe187e706bb309a905c2f88c7477b53cf5839（十一月五日十九時十二分三十六秒，由 #31 的合併帶入）；HG-KSEOS 主線為 a7046a36956e2179d7125449ce9b6f05fa5451cf（十一月五日十六時十分五十五秒，由 #14 的合併帶入）。

邊界有三。其一，合併提交只證明該提交已合併，不證明合併後內容與封存頭逐位元等價；本輪未做此比對，故不得把合併當成封存候選已被原樣接收。其二，合併不等於原案例執行器或原讀取者已接收，下游第二關仍停在「候選源已合併」，第三關仍為「源已存在、原生鏈未合格」。其三，本機複本頭（分別為 826ca066、765df628、6c9fc733）皆非主線且帶未提交變更，不得以遠端主線冒充本機脈絡。

仍為未合併者：SBL #41（頭已變為 d10362d7，涉 203 檔，可合併狀態為 dirty）、#42；Fabric #27 與 #28；HG-KSEOS #11 與 #12。故原文第零節與第六節對 #41／#27／#11「未合併」的判斷仍成立，本輪不列為過時；需更正的只是這批讀值中的主線，以及 SBL #41 的頭（原文附錄記 c01410bb，現為 d10362d7）。

### 四｜未解清冊八筆逐項

W1 的受影未解項為八筆，原封存即記八筆，且原檔沒有狀態欄位。故不得寫成七筆，不得寫任何一筆已消耗或已解除；本節不改寫為關閉，也不新增第九筆。逐項如下。

| 識別 | 工作包 | 原缺口與首敗 | 對下游的影響 | 重啟條件 | 責任方 |
|---|---|---|---|---|---|
| H-W1-01 | 政策消費 | 需載入收據與同主體、同範圍、同版本的消費確認；首敗為政策未載入 | 阻政策生效，及消費該政策的效應 | 同範圍確認，或具名延後並指名被延後的操作 | 原政策所有者與 HGK 消費方 |
| H-W1-02 | 註冊與簽發 | 需該工作識別、範圍與版本的簽署許可；首敗為簽發綁定無效 | 阻任何主機操作與依賴許可的效果 | 簽章在單一註冊修訂的登記所有者金鑰下驗證通過 | 原 HGK 簽發方 |
| H-W1-03 | PIPD 編譯 | 需嚴格位元上的正式提升確認；首敗為正式提升未決 | 阻正式規格、設計、執行契約與測試計畫的提升 | 原讀取者確認，側車永不提升 | SBL 正式 PIPD 讀取者 |
| H-W1-04 | 原生計畫 | 需同基準修訂的比對確認或拒絕；首敗為計畫比對缺回執 | 阻計畫修訂生效 | 原寫入方回覆，已過期則重讀甲線 | 原計畫寫入方與比對讀取者 |
| H-W1-05 | 可攜主機 | 需逐主機的已載入與已呼叫收據；首敗為主機矩陣不完整 | 使三主機陳述不成立，實際只有一個主機被行使 | 各主機以自身載入器在自身位元上讀回安裝、載入、呼叫 | 各主機載入器所有者 |
| H-W1-06 | 開機能力 | 需兩個能力路由的所有者簽署；首敗為能力缺口 | 阻該兩項需求的主機操作分支 | 路由存在於登錄（非未登錄）且載入已讀回 | 原 HGK 安裝與簽發方 |
| H-W1-07 | 矩陣 | 需逐個已耗用格位的開關確認；首敗為格位確認缺失 | 阻開關宣告與不適用推論 | 該格位在該主機與模式上的所有者確認 | 原格位所有者 |
| H-W1-08 | 開機能力 | 需每資產具體釘選、已解的視窗適配與安裝器自身收據；首敗為能力開機相依反轉 | 阻那二十一項資產達已安裝以上，並阻任何適配宣告 | 釘選為具體摘要且適配狀態已解，且收據同主體 | 原技術、授權與主機讀取者 |

兩點須記明。其一，八筆中有兩筆掛在同一個工作包（能力路由與資產釘選），性質不同，不得併成一筆。其二，封存中並無執行環境工作包的專屬條目；本節不代為補寫新的未解項，該工作包的預算與實際服務缺口，仍依原文的既有識別讀。

### 五｜3 Host／24 AssetSlot／192 Cell 的分層現況（不得互借）

三層不得互借，逐層如下。

三主機一層：三主機陳述不成立。封存事實是只有一個主機被行使，其餘主機的載入器與安裝、載入、呼叫皆無收據。單一主機的讀回，只證明那一個主機的那一個操作，不得外推成三個主機，也不得由同儲存庫或同啟動器推定三份齊備。

二十四資產一層：二十四個資產格位中只有三個有具體釘選，其餘二十一仍是未解字面；已安裝為零（二十四分之零）；視窗適配未解。故那二十一項不得記為已安裝或以上，任何一項都不得宣告適配。

一百九十二格位一層：一百九十二個種類、模式與主機的格位身分全部保留，不刪、不改分母、不改號；但無任何所有者對任一格位作出開關裁決。未裁決前，不得把原始開關私譯成供應商布林，也不得作不適用推論。

另須記明交接分層：主機與資產的未完成部分交下游第三波做全量資格化，格位的原始開關解析交同一波，但交接只轉期待與分母，不轉任何已合格狀態；本節不得因交接完成而把三層任一層記為完成。

互借禁令：主機之間、資產之間、格位之間不得借收據；一份收據只覆蓋同主體、同範圍、同主機、同版本的那一項。四組數字各自分立：被行使的主機數為一，有具體釘選的資產數為三，已安裝數為零，有所有者裁決的格位數為零。四者不得相加、平均或互相代替。

### 六｜驗證狀態與 NOT_RUN

本輪可重算且已實測者：原文摘要與行數、封存未解項為八筆且無狀態欄位、三庫提交狀態與主線讀回（讀值時間為十一月六日十九時四十五分台北）、原文七處「當期主線或當期讀值」字串的存在性與唯一性（逐筆回原文以程式驗證，皆為唯一命中）。

執行者層級亦須記明：上列可重算項全部由作者端自行執行，未經第二方複核，故其結論屬作者端對帳，不屬獨立驗證；任何以本節數字對外主張驗收者，均超出本節上限。

未執行項（NOT_RUN）：原生主機端到端、獨立檢查者、所有者批准、真實許可簽發、世界原始讀回、PIPD 正式編譯、任何下游世界效果。原文的單元層通過與作者端靜態檢查屬其時點事實，不因本節升格。

下游四閘現值：第一關為「文件就緒、待修訂自測」；第二關為「候選源已合併」；第三關為「源已存在、原生鏈未合格」；第四關為「靜態所有者與簽發者職責分離已保留、許可未執行」。四者皆未達效果就緒。

未重讀者明示：本輪未在 SBL 新尖端重讀整合目錄，故十三個命令列、十九個契約族與八個技能的完整集合，仍以舊尖端時點的讀回為準，並標為讀取當時釘選、非當期主線。上游封存的七十一筆未解項為 W1 r2 自述值，本輪未取得該封存原件，故不與本輪重算的六十八筆合併或互抵。

### 七｜未宣稱清單

本節明確不宣稱下列任一項：三主機已載入或已呼叫；二十四資產已安裝；一百九十二格位已有所有者裁決；下游效果就緒；PIPD 正式生效；原生端到端通過；獨立檢查者通過；已發行；上游全面結案（全面結案為假、驗收完成為假、相依項仍未滿足）；合併即原域接收；作者端測試即獨立檢查者；暫存即已載入；以及把封存交接中的「候選接線已交付」讀成下游效果就緒——該信封的阻擋項為 H-W1-01、H-W1-02、H-W1-03，主張上限為候選。

本節的交付只有兩件：過時斷言清冊（七筆實體、四筆明示不存在）與本節。兩者皆為作者端對帳，可交原讀取者補件，不構成任何原域效果。

# CH-00｜正式入口、主體法位、不可降級 H1 規則

**唯一主波** `W0`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L42–186`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** L3 Pack Curator；L2-r4:L890。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W0 Normative 主責）

W0 的原文/Source/SPEC/QuestionLedger/Program 只有 SourceSpan+same Subject/Scope 作 W1 受影依據，W1 不重寫或簽 W0 原草案與定案。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W0 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L42–186` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-00 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-00",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W0",
  "OriginalReader": "L3 Pack Curator；L2-r4:L890",
  "consumer": "L3 Pack Curator；L2-r4:L890",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-00",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 42,
    "end": 186
  }
}
```

<a id="ch-01"></a>

# CH-01｜FHS 產品定位、Owner／JTBD／FUO 和非目標

**唯一主波** `W0`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L187–246`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** SBL Product/Owner；L2-r4:L891。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W0 Normative 主責）

W0 的原文/Source/SPEC/QuestionLedger/Program 只有 SourceSpan+same Subject/Scope 作 W1 受影依據，W1 不重寫或簽 W0 原草案與定案。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W0 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L187–246` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-01 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-01",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W0",
  "OriginalReader": "SBL Product/Owner；L2-r4:L891",
  "consumer": "SBL Product/Owner；L2-r4:L891",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-01",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 187,
    "end": 246
  }
}
```

<a id="ch-02"></a>

# CH-02｜七大痛點、原始動機與逐產品旅程

**唯一主波** `W0`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L247–338`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** SBL Product/Owner；L2-r4:L892。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W0 Normative 主責）

W0 的原文/Source/SPEC/QuestionLedger/Program 只有 SourceSpan+same Subject/Scope 作 W1 受影依據，W1 不重寫或簽 W0 原草案與定案。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W0 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L247–338` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-02 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-02",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W0",
  "OriginalReader": "SBL Product/Owner；L2-r4:L892",
  "consumer": "SBL Product/Owner；L2-r4:L892",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-02",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 247,
    "end": 338
  }
}
```

<a id="ch-03"></a>

# CH-03｜功能需求、OriginalID、強弱語義及完整不變量

**唯一主波** `W0`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L339–409`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Requirement Reader；L2-r4:L893。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W0 Normative 主責）

W0 的原文/Source/SPEC/QuestionLedger/Program 只有 SourceSpan+same Subject/Scope 作 W1 受影依據，W1 不重寫或簽 W0 原草案與定案。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W0 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L339–409` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-03 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-03",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W0",
  "OriginalReader": "Original Requirement Reader；L2-r4:L893",
  "consumer": "Original Requirement Reader；L2-r4:L893",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-03",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 339,
    "end": 409
  }
}
```

<a id="ch-04"></a>

# CH-04｜31 冊 SourceFreeze、AuthorityBinding、Currentness、版本衝突

**唯一主波** `W0`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L410–544`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Source Authority Reader；L2-r4:L894。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W0 Normative 主責）

W0 的原文/Source/SPEC/QuestionLedger/Program 只有 SourceSpan+same Subject/Scope 作 W1 受影依據，W1 不重寫或簽 W0 原草案與定案。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W0 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L410–544` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-04 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-04",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W0",
  "OriginalReader": "Original Source Authority Reader；L2-r4:L894",
  "consumer": "Original Source Authority Reader；L2-r4:L894",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-04",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 410,
    "end": 544
  }
}
```

<a id="ch-05"></a>

# CH-05｜U0 全位元組內容盤點：表格、負條件、Code、原版附錄

**唯一主波** `W0`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L545–681`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Corpus Reader；L2-r4:L895。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W0 Normative 主責）

W0 的原文/Source/SPEC/QuestionLedger/Program 只有 SourceSpan+same Subject/Scope 作 W1 受影依據，W1 不重寫或簽 W0 原草案與定案。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W0 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L545–681` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-05 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-05",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W0",
  "OriginalReader": "Original Corpus Reader；L2-r4:L895",
  "consumer": "Original Corpus Reader；L2-r4:L895",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-05",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 545,
    "end": 681
  }
}
```

<a id="ch-06"></a>

# CH-06｜U1 子要求逐義拆解：各有／分別／對應／若／不得

**唯一主波** `W0`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L682–755`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Requirement Atom Reader；L2-r4:L896。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W0 Normative 主責）

W0 的原文/Source/SPEC/QuestionLedger/Program 只有 SourceSpan+same Subject/Scope 作 W1 受影依據，W1 不重寫或簽 W0 原草案與定案。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W0 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L682–755` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-06 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-06",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W0",
  "OriginalReader": "Original Requirement Atom Reader；L2-r4:L896",
  "consumer": "Original Requirement Atom Reader；L2-r4:L896",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-06",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 682,
    "end": 755
  }
}
```

<a id="ch-07"></a>

# CH-07｜U2–U4 Crosswalk、版本去向、Owner 語義核簽與反例

**唯一主波** `W0`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L756–991`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Domain Owner + Trace Reader；L2-r4:L897。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W0 Normative 主責）

W0 的原文/Source/SPEC/QuestionLedger/Program 只有 SourceSpan+same Subject/Scope 作 W1 受影依據，W1 不重寫或簽 W0 原草案與定案。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W0 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L756–991` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-07 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-07",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W0",
  "OriginalReader": "Original Domain Owner + Trace Reader；L2-r4:L897",
  "consumer": "Original Domain Owner + Trace Reader；L2-r4:L897",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-07",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 756,
    "end": 991
  }
}
```

<a id="ch-08"></a>

# CH-08｜SBL SharedCore 六模組與三 SP 的完整產品鏈

### r2 受影修補（2026-11-05｜AUTHOR_FINAL_AFFECTED_REPAIR）

**受影 Finding**：`F-04、N-06`。**原位差額**：本章三 SP 與 SharedCore 六模組的 POS／NEG／EDGE／SEC 維持四個不同主體；r2 明確 Native Runner 未執行，且六模組不被單一 Chat Handler 取代。

**未變更**：本章 H1 標題、L1 span／section SHA、OriginalID／Parent／NEG 與原 Reader 法位皆不變；原域 Raw 未取得者維持 `EXPECTED_NOT_OBSERVED`，不以作者推斷補值。

**下一個 Reader**：HGK/Host Original Checker；FirstFail 見本章 POS／NEG／SEC 卡與 `AFFECTED_FINDINGS.jsonl` 對應列。

## W1 草案當期完成契約｜CH-08（DRAFT-W1-CH08）

**使用者可得結果**：SBL SharedCore + TPM/Commander/Challenge SP；合法執行範圍限 `LOCAL_DRAFT_WRITE` 與作者端規格審閱，無真 Host 准入或新 Writer 權限。

| 受影型別 | 本章可驗證的確定規則 |
|---|---|
| Input／觸發 | 普通 Goal / 有來源定位的變更需求；強制 `subject_id/source_manifest_sha/scope` 來源釘選 |
| 操作／Producer | 先由 PM 產 Product SPEC，SE 產 Architecture SPEC，TPgM 產 Program SPEC；列六 SharedCore Module 對三 SP 的不同 Reader、作用域和非目標；Portable 建議不取得 Native Issuer 角色；Producer＝W1 DraftMaker（僅文字/Sidecar），正式效果由原域 Producer 執行 |
| Output／交付 | 三個互不混淆的 SpecDelta、Host/SP 作用矩陣、原 Reader routing 卡；所有未觀測 Reader Raw 留空並具名 `EXPECTED_NOT_OBSERVED` |
| Original Reader | SBL Product/Kind 原 Reader；原 Writer／Issuer／Checker 不因本稿改權 |
| Downstream Consumer | SBL TPM/PIPD intake；W3 Host Matrix；綁同 Subject／Scope，需 Original ACK 才可升級 |
| POS／Expected Raw | 同一 Goal 可見三份角色 SHA 不同且 NEG 不丟；預期由原 Consumer 返回原格式 Raw（本輪 `NOT_RUN`） |
| NEG／首拒收 | 三 SPEC 混合成一份或 TPM Skill 發 Permit；FirstFail=`SP_CONSUMER_BIND_NACK` |
| EDGE | 缺 SP×原 Consumer 精確綁定時的 Scope HOLD；只 PARK 受影 scope，合法 READ/DRAFT 不受波及 |
| SEC | 冒充 original Product Owner 的 ratification；缺憑證、Owner、ACL 或 Checker 證物拒效果 |
| Stop／Resume／Rollback | 遇 `SP_CONSUMER_BIND_NACK` 記 `hold_id+original_reader+required_raw`，停止受影寫入；Resume 需同 SourceSHA/Scope 的原 Reader 結果；READ 丟棄快照、DRAFT 刪除隔離候選；世界效果不在 W1 自行 rollback |
| Cross-wave | W3 CH09/21/27、W4 trace；交 `AUTHOR.FHS.W1ToW{next}@design` typed envelope，禁止偽裝 WorkOrder |

**受影源句拆義**：`actor/trigger/action/object`（見 Input/操作）；`condition/exception`（見 EDGE）；`prohibition`（見 NEG/SEC）；`outcome/consumer`（見 Output/Original Reader）；`POS/NEG/FirstFail` 必綁同一原 RequirementID。來源的原始句、Span、SHA、Parent/Child/NEG 以 r5 本章及附錄 `obligation_registry.jsonl` 回指；缺具體原 Reader 即 `ORIGINAL_OWNER_HOLD`，不自行創造簽核。


### R5 本章受影精確契約／業務負例（整合 r4，非歷史附錄）

Product/Architecture/Program 三 SPEC 維持不同 SHA/Owner/ACC/NEG；TPM、Commander、Challenge 的 Portable 與 Native 收據分開。W1→原 Product/Kind/Host Consumer 只交可稽 SourceRef、FUO/NEG；任一 Portable Skill 自行簽 Native Grant → `PORTABLE_NATIVE_AUTHORITY_CROSSING_DENY`。


**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L992–1051`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** SBL Product/三 SP；L2-r4:L898。原 Domain Reader/Writer 不因本章轉移。

## r4 當期原 Reader 鎖與非降級本體

本章 L1-r4 依以上真實行區間及原域 Reader；無單獨 R4-BEGIN 增量不等於以歷史 r2 取代 L1。W1 契約下文僅是對該 L1 已定義原義的工程操作化。

## r4 對齊之 W1 主波操作規格、草案必填欄、逐項 POS/NEG／FirstFail（高保留整合）

**Protected Original H1 / CURRENT L1-r4**：`FHS_PIPD-LS-PKG_藍圖_2026-11-04_r4_HIGH_RETENTION_AUDIT_REPAIRED_實質正文(1).md:L992–L1051`；`source_file_sha256=cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`；`section_sha256=25b58dc0712e9ac55edc1becee91c101930b55d5b3533397cdb6c32e85224a32`；`heading_exact=# CH-08｜SBL SharedCore 六模組與三 SP 的完整產品鏈`；**HISTORICAL_LOCATOR_NOT_EFFECTIVE**=`L1:650–695` / `L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`，L2 作者端路由 `L2:646`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W1 不取得原 Writer。

## A. 本章實質功能與不能壓平的原義

Goal → SBL Shared Core（M01 Intake／M02 SPEC／M03 Routing／M04 Bridge／M05 Evidence／M06 Bounded Repair）→ TPM/Commander/Challenge 三 SP 的原產品鏈。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。

## B. 來源 r5 skeleton 必填核對欄（已由上方 W1 草案當期完成契約受影回填）

| 必填欄 | 欄位設計／不可空條件 |
|---|---|
<!-- HISTORICAL_R5_SKELETON_FILL_REQUEST_SUPERSEDED: transition wording only; all substantive constraints retained -->
| `chapter_id` / `primary_wave` / `author_writer` | `CH-08` / `W1` / `W1:DraftMaker`（歷史 r5 階段欄；當期為作者端定案候選） |
| `original_sources[]` | 本章 L1 行與下面原冊 SHA／OriginalClause Span；不得用語義假定的 ID 補空缺 |
| `same_subject` / `candidate_sha` / `source_manifest_sha` / `affected_scope` | 必攜相同 Subject/Scope，未原 Reader 認證則 `AUTHOR_CANDIDATE` |
| `effect_class` / `original_owner` / `consumer_abi` / `schema_version` | 依 Operation Reader；缺 `$id` 或 Receiver 不自造 |
| `input` / `typed_output` / `fuo` / `non_goals` | 應有真使用者結果與 Receiver（非檔案數） |
| `positive_fixture` / `negative_fixture` / `security_fixture` | 原 Source Case/Oracle 逐受影引用，未有 Runner/Raw 就 `EXPECTED_NOT_OBSERVED` |
| `first_fail` / `hold` / `stop_scope` / `resume_predicate` | 明確停止受影子圖，不全域凍結 READ／DRAFT |
| `rollback` / `w2_handoff` / `original_ack_nack` | 回退路由與 same scope 的預期接收；不得填假 PASS |

## C. Input → Producer → 原 Reader／Consumer → Output

- **Input/Guard**：Goal/OriginalRequirementRefs/Persona/Kind/Scope/three distinct SP-role facts。
- **Producer**：該 Original Domain 的 Reader/Compiler/Host/Guide 依本章功能生產；W1 Curator 僅記設計；**Original Consumer**：SBL Product Reader / 三 SP 原 Host Consumer。
- **Typed Output/FUO**：Source-bound Product/Architecture/Program SpecCandidate、typed router decision 與 original Consumer readback request。
- **版本要求**：至少 `Subject,CandidateSHA,SourceSHA,OriginalID+SourceSpan,Scope,Host/PolicyEpoch（受影才填）,ABI $id/version,OriginalReader,OutputRawExpected`，少一欄只停需該欄的出口。

## D. POS／NEG／FirstFail／HOLD／退出

- **POS（期待）**：各模組有獨立可觀測 FUO 與拒越權；Reader 回 typed NACK 仍可追蹤。
- **NEG／SEC（期待拒收）**：一個 Chat Handler 取代六模組／同 Maker 自簽 Challenge。
- **FirstFail**：`SBL_SHARED_CORE_ROLE_COLLAPSE`；禁止只有泛稱 `VALIDATION_FAILED` 而不給首次失敗位置。
- **HOLD/Owner**：`SBL_DOC03/04 原模組實際 consumed 版本待核`。需同 Subject/Scope/Host/原 Reader 的真 Raw/ACK 解除；本輪 `NOT_RUN`。
- **Stop/Resume**：保留原 SourceSHA/受影 Reader/cursor/last-good；READ/DRAFT 合法部分繼續；UNKNOWN 必原 Reader reconcile。
- **Rollback**：只回復該 Need/Host 的原 last-good，Host/OPS 效果走原 inverse；不得以檔案 ZIP 作回復收據。

## E. 來源追溯、波次邊界與下一手

| 源鍵／檔案 | 原文 SHA | 此 W1 處理方式 |
|---|---|---|
| SBL-DOC-04 | ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| SBL-DOC-03 | ea69e1d3718ed86aecd74a3ebcc933960eacc30b586ab80fcb9f733037e33476 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-01 | e257dfcd01f2e8afeda1dd88fdd33b4ef7346bf224572e60935bf9834d25b02c | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-09 | 1a0fcbdd77998bc9beed039407b96a1163c634052583813a98193f4d49769185 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
W0 提供原 Source/三 SPEC/索引；本 `CH-08` 不修改 W0 成果。W1 WaveCurator 交 W1 DraftMaker 按原 Reader 定位填入真 Requirements；W2 僅領同 Subject/Scope 的需要的 Effect/Case/HOLD，不得借 W3/W4 收據。原 L1 CH-08 的詳細原義仍在 L1 主體，不移作本冊第二 Canonical。

## F. r2 原位修補：CH-08 可直接交接的受影實質規格（非證據附錄）

**本章不可壓平功能**：SBL six modules + TPM/Commander/Challenge SP。與 W0 三份獨立 SPEC 維持同 SourceSHA/Subject/Scope；將原讀者真接收的 **Output／Consumer** 優先於填滿文件欄位。依 L1 原 CH 身份與 L2 W1 主責修訂，不移轉原 Writer。

### F.1 原句→原 Consumer→本章測例的逐子義槽（已從原物理檔定位）

- **`SCL-W1-0001`** `[SOURCE:SBL-DOC-04:L1971:sha256=ee90cb1c86f6f735]`：原文實質片段「/ SBL-PROP-D04-A028 / BP L1471 + D04 audit TPM:PM:T5 / Product Manager T5: Evidence of FUO/feedback → Evidence-aware product review request / D04-T-PM-T5 / C13.Projection@r4 → TPM Product/System/Program; SPEC-S」；Parent=`L1940:#### R06.8.1｜Atom→Typed SPEC/ACC/NEG/VER/EEXP/DELIVER（165 個受影條目逐一列出）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=SBL SharedCore / TPM three SP original Product Reader；承接 `WP 05/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH08.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0002`** `[SOURCE:SBL-DOC-04:L1993:sha256=ee90cb1c86f6f735]`：原文實質片段「/ SBL-PROP-D04-A050 / CAPC contract original C6 / C6 FUO: ProductKind+UserOutcome+exit+observable proof→FUOAcceptance / D04-CAPC-C6 / C14.Projection@r4 → CAPC Reader; SPEC-SBL-PROP-D04-A050 / **ACC** ACC-SBL-PR」；Parent=`L1940:#### R06.8.1｜Atom→Typed SPEC/ACC/NEG/VER/EEXP/DELIVER（165 個受影條目逐一列出）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=SBL SharedCore / TPM three SP original Product Reader；承接 `WP 05/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH08.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0003`** `[SOURCE:SBL-DOC-04:L2364:sha256=ee90cb1c86f6f735]`：原文實質片段「- **TestInput**：{"case":"NEG-D04-STANDALONE-FUO","subject_sha":"<compute exact bytes>","tamper":"Legal local worker with specific token universally banned","candidate_status":"FROZEN_FOR_TEST"}。**Expected**：DEN」；Parent=`L2361:### 07.07 `NEG-D04-STANDALONE-FUO` 完整預期 Fixture`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG,不得`。本章觸發/Consumer=SBL SharedCore / TPM three SP original Product Reader；承接 `WP 05/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH08.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0004`** `[SOURCE:SBL-DOC-03:L632:sha256=ea69e1d3718ed86a]`：原文實質片段「/ product_truth / REQ-D02-0043 / authoritative product truth / required when applicable; otherwise Owner-approved N_A_ACCEPTED with reason / **SBL candidate typed projection** nonempty UTF-8 string with explici」；Parent=`L621:### C18.1.04｜PI-04 — Intent / User / Product Truth / User Truth / 12 Native fields`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=SBL SharedCore / TPM three SP original Product Reader；承接 `WP 05/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH08.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0005`** `[SOURCE:SBL-DOC-03:L2992:sha256=ea69e1d3718ed86a]`：原文實質片段「/ P0_TOOL78 / P0-TOOL-003 / SRU Kernel / upstream=CORE / shared_spine; disposition=DEFAULT_ENABLED_AFTER_QUALIFICATION; observed=TARGET_CONTRACT_DEFINED / OBSERVED_NOT_INSTALLED; runtime=NOT_EXECUTED / ROUTE_DO」；Parent=`L2878:## R06.2｜全 386 技術身份及原 Decision：逐 ID DOC03 relevance/Owner/首失敗`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=SBL SharedCore / TPM three SP original Product Reader；承接 `WP 05/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH08.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0006`** `[SOURCE:SBL-DOC-03:L3877:sha256=ea69e1d3718ed86a]`：原文實質片段「/ FX-U-U05.3-POS/NEG / POS：對 U05.3 提交真實同 Parent 前置/對應來源/合法 Host，驗收「用有界 MVP scope 拆分首版與非首版功能」，比對受影欄位輸出及原生不變量；PARENT_COMPOSITE_PROVISIONAL需另通過 Parent 合取判斷 / NEG：只改 U05.3 所要求的行為/輸出/權界，令「用有界 MVP scope 拆分首版與非首版功能」不成」；Parent=`L3861:## R08.1｜每個 U 子項的 POS/NEG 族（149 獨立鍵；見 R03 精確行）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG,不能,不得`。本章觸發/Consumer=SBL SharedCore / TPM three SP original Product Reader；承接 `WP 05/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH08.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0007`** `[SOURCE:FHS-BODY-01:L92:sha256=e257dfcd01f2e8af]`：原文實質片段「- **FUO-01**：原 SourceManifest 中每個適用需求至少具 原身份→原作用→Owner/Consumer→POS/NEG，對應可打開的 Product/Architecture/Program SPEC；失敗不能用生成檔案數替代使用者效益。」；Parent=`L89:### Product SPEC｜單人 Owner 交付 FUO`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG,不能`。本章觸發/Consumer=SBL SharedCore / TPM three SP original Product Reader；承接 `WP 05/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH08.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0008`** `[SOURCE:FHS-BODY-01:L131:sha256=e257dfcd01f2e8af]`：原文實質片段「Product SPEC：單人 OWNER 輸入 goal/source/known_answers，PM 將 Persona/Pain/JTBD 轉為可見 FUO、MVP、non_goals、ACC/NEG。FUO 必是使用者能取用的成果，例如普通「整理來源後產待審變更規格」得到 source-bound SpecDelta；不得以檔案數當 FUO。Consumer 是 PIPD Intake/原產品 Owner；」；Parent=`L129:## R2-01-SPEC：三份 SPEC 的不同消費結果`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG,不得`。本章觸發/Consumer=SBL SharedCore / TPM three SP original Product Reader；承接 `WP 05/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH08.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0009`** `[SOURCE:FHS-BODY-01:L145:sha256=e257dfcd01f2e8af]`：原文實質片段「輸入「為此既有產品加入離線來源查詢」：PM 指定離線可查 source locator 是 FUO；SE 指定 SOURCE_READ、provider_off=true、不新建 Authority DB；TPgM 產唯讀 source probe 和隔離 spec 卡。輸出三 SPEC + trace + unresolved bindings，交原 PIPD Intake。若沒有原 Writer ACK，狀態為 」；Parent=`L143:## R2-01-EXAMPLE：普通 Goal 到候選與退出`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=SBL SharedCore / TPM three SP original Product Reader；承接 `WP 05/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH08.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0010`** `[SOURCE:FHS-BODY-09:L28:sha256=1a0fcbdd77998bc9]`：原文實質片段「人類入口 goal + source_locator（可為待提供的查詢結果而非已凍結） + requested ProductKind + mode；TPM 問最多一個**已被來源核對確有必要**的阻擋問題（單問僅為設計 UX 假說，不是已實測閾值），輸出 GoalCard、MethodDecision 和可讀 MissingInput。若只有 goal 而無來源，顯示「需一份文件或合法來源路徑」並可先進行無效應探索」；Parent=`L27:## R00.r3.1｜五分鐘產品操作契約與七痛點→實體成果`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=SBL SharedCore / TPM three SP original Product Reader；承接 `WP 05/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH08.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0011`** `[SOURCE:FHS-BODY-09:L37:sha256=1a0fcbdd77998bc9]`：原文實質片段「/ P07 / 最後一哩 FUO 缺失 / 新環境手動使用得到結果並能撤銷；Provider-off 走功能受限路徑 / DeliverBOM/Consumer UAT / Build → ConsumerOutcome/UninstallReceipt / 只有 README 或模擬沒清楚標示 / M12-M15／GJ01-03 / DOC12/13 /」；Parent=`L27:## R00.r3.1｜五分鐘產品操作契約與七痛點→實體成果`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=SBL SharedCore / TPM three SP original Product Reader；承接 `WP 05/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH08.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0012`** `[SOURCE:FHS-BODY-09:L204:sha256=1a0fcbdd77998bc9]`：原文實質片段「- 交互規則：原產品的 Goal/Kind/Mode/Host／本 DOC 功能 Input 經必要 Reader Projection 交 SBL 原 Consumer；需要真世界效果者才送 PIPD→Fabric/HGK→Hermes；純設計/唯讀不得被外加 permit 阻斷。」；Parent=`L202:### SBL DOC-04｜原產品功能與本次 FHS 消費接口`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不得`。本章觸發/Consumer=SBL SharedCore / TPM three SP original Product Reader；承接 `WP 05/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH08.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。

### F.2 本章 WP 與 Producer／typed I/O／FirstFail（每項獨立）

- **WP-FHS-05**：Producer=SBL-hosted original PIPD Compiler/Reader；Input=三份不同 SPECDraft、原 SourceManifest/Authority/Profile safety veto、原 PIPD Writer version；Output=非空 strict PI，真 RepoContext 才有 PD，DEV/OPS EffectIntent 分開，PlannedTQAEP 不冒 Checker；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=PIPD Native Compiler 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=把 _profile_meta 側掛塞進 strict PI；或憑 Caller HEAD 虛構本機 Repo binding；EDGE=PI SourceSHA 不變而 RepoHEAD 改變，只使 PD/ECP stale；不可偷重寫 PI requirement 原義；FirstFail=`PIPD_STRICT_SCHEMA_OR_SOURCE_NACK`；rollback=隔離候選刪除/回復 preimage；SourceSHA/HEAD 變更僅重編受影 PD/ECP。
- **WP-FHS-11**：Producer=各 Host 原 Skill/Plugin Reader+每 SP original Consumer；Input=TPM-SP、Commander Guide-SP、Acceptance Challenge-SP 各自 artifact digest；Host compatibility+8 PIPD skills 各自 registry；Output=每 SP×Host 真 Loaded/Invoked/Used/nontrigger/Remove Raw；不共用收據；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=Portable Host Dogfood 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=用 TPM-SP 的 Loaded SHA 冒 Challenge-SP；Maker 以模型結論簽 Protected Checker；EDGE=Installed 後 loader 未 Loaded，或 Loaded 但 nontrigger 仍被啟動：不得宣稱 Used；FirstFail=`HOST_SKILL_TRIGGER_NONTRIGGER_NACK`；rollback=原 Host disable/remove entrypoint、還原 last-good manifest；清理 residue。

### F.3 複合原義拆解、反向閉包與受影退出

- **「各有」**：本 CH 的每個原 clause locator 各自保留 SourceSHA/Parent/OriginalConsumer、POS/NEG；若原文有多個 named roles/Host/Case，不可用單一結果冒全數。
- **「分別」**：strict JSON body／@2 sidecar、Original Policy Active／Host Loaded、Maker challenge／Protected Checker、Selected／ActualServed 是不同欄位與收據，不得合併。
- **「對應」**：必 `original source line → SCL-W1 id → CH → W1 WP → expected Case → original source line` 可機械重算；原 OriginalID 未明者只引用明示的 SourceSpan，不可猜 ID。
- **「不得／若／除非」**：否定作用域保留到原 Parent context；本章只標作者候選，原 Source Reader 取得 ACK 才能宣告原語義接受。
- **退出**：原 Reader NACK 僅 PARK 本章受影的 PI/PD/DEV/OPS/Host operation；合法 SOURCE_READ、隔離草稿及不依賴該 ABI 的 W0/W2 工作照原許可前進。

## 本章 L2-r4 設計義務接收卡（逐 ID；不可省略原 NEG）

- `FHS-DR-008` (`L1-r4:L805`, `L2-r4:L346`)：產品／A；三 SP 均保留 Portable/Native 對照而不混權限；TPM/Commander/Challenge 各自讀合法原 Consumer；[CH-08](#ch-08)/[CH-11](#ch-11)/[CH-34](#ch-34)；POS `同 WorkID/Source/Case 的適用讀回`；NEG/FirstFail `任一 Portable Skill 自行發 Grant/Checker；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `SBL Product/Kind/Host Original Consumer`；本輪只有 EXPECTED_NOT_OBSERVED。

## CH-08 專屬退出與回退

DraftMaker 後續須填 `original_reader_ref`, `original_schema_version_or_HOLD`, `source_span_sha`, `same_subject_and_scope`, `Case/Oracle`, `positive_raw_expected`, `negative_raw_expected`, `first_fail`, `resume_predicate`, `last_good`, `consumer_ack_or_HOLD`。`DOC_AUTHOR_DONE` 是本檔可檢索，不是 `SBL SharedCore 六模組與三 SP 的完整產品鏈` 已原 Host Qualified。若權限／能力尚缺，只 PARK 受影操作；回退到該 Domain 上次有效 Reader/Host 版本、保留跨波合法 READ/DRAFT，且不得刪原 NEG 或憑此文件自簽。



## AUTHOR-FINAL｜CH-08 受影交付契約

**Input / Operation / Output**：保留本章原有專屬 I/O、原句與 NEG；以當期 Registry 對同 SourceSHA/Subject/Scope 重算受影子圖，輸出 CH-08 的原 Reader BindingRequest，實質輸出與業務 FirstFail 以本章上文專屬契約及下列子義為準。

**Original Reader / Original Consumer**：SBL Product Reader；原 Consumer Raw=EXPECTED_NOT_OBSERVED。L1 起始 992、終止 1051，section SHA `25b58dc0712e9ac55edc1becee91c101930b55d5b3533397cdb6c32e85224a32`。

**POS / NEG / FirstFail**：本章專屬正負條件逐筆如下（清單即本章 F.1 的 9 個 `SCL-W1-0040`～`SCL-W1-0048` 子義槽；本章無綁定的 L2-r4 DesignID 義務卡，理由與 HOLD 見下節）；沒有適用子義的跨 ABI 章以原本章完整 POS/NEG 為準，不從別章借用 PASS。**EDGE**：SourceSHA/Host/PolicyEpoch 其中一欄改變，只 invalidate 受影接線；**SEC**：Maker 假 ACK 或跨 Principal 原回條均拒收。**ExpectedRaw**：同 Subject/Candidate/Scope 原 Consumer/World bytes；本輪 NOT_RUN。**Stop**：缺該 Effect 必需原 Reader 即 PARK 其效果；**Resume**：同 Scope 原 Reader 提供具名 Raw；**NextWave**：W2 原 Effect Receiver，四 Host/Cell/W18 交 W3，CI/Publisher 交 W4。

- `S-W1-FHS-DR-008-01`：Input=TPM／Commander／Challenge 三 SP 各有 Portable 入口；POS=3 個 Host Pack 身份獨立；NEG=把 TPM LoadedSHA 當 Challenge；FirstFail=`SP_PACK_IDENTITY_COLLISION`；Consumer=SBL Product Original Consumer and original Protected Checker；Case=`AUTHOR.W1.FHS-DR-008.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-008-02`：Input=Portable Guide 不能簽 Native Permit/Checker；POS=原 Native consumer 各有獨立 Ack；NEG=Portable Plugin 自簽 Checker；FirstFail=`PORTABLE_NATIVE_AUTHORITY_CROSSING_DENY`；Consumer=SBL Product Original Consumer and original Protected Checker；Case=`AUTHOR.W1.FHS-DR-008.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。

<a id="ch-09"></a>

# CH-09｜八 Kind、三 Mode、四 Host、16 Moments、38 Delivery Surfaces

**唯一主波** `W3`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L1052–1112`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Kind/Mode/Host Product Reader；L2-r4:L899。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W3 Normative 主責）

W1 保持此章完整源身份、Need/Host/Consumer 的交接 locator；全產品分母/普通模式及其原 Reader 由 W3 主波驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W3 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L1052–1112` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-09 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-09",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W3",
  "OriginalReader": "Original Kind/Mode/Host Product Reader；L2-r4:L899",
  "consumer": "Original Kind/Mode/Host Product Reader；L2-r4:L899",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-09",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 1052,
    "end": 1112
  }
}
```

<a id="ch-10"></a>

# CH-10｜已知答案、Source-bound 檢索、FAR／知識服務

**唯一主波** `W0`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L1113–1173`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** FAR/G-KNOW Consumer；L2-r4:L900。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W0 Normative 主責）

W0 的原文/Source/SPEC/QuestionLedger/Program 只有 SourceSpan+same Subject/Scope 作 W1 受影依據，W1 不重寫或簽 W0 原草案與定案。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W0 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L1113–1173` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-10 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-10",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W0",
  "OriginalReader": "FAR/G-KNOW Consumer；L2-r4:L900",
  "consumer": "FAR/G-KNOW Consumer；L2-r4:L900",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-10",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 1113,
    "end": 1173
  }
}
```

<a id="ch-11"></a>

# CH-11｜TPM 三 SPEC：Product、Architecture、Program 與 18 Stage

**唯一主波** `W0`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L1174–1256`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** SBL TPM/PIPD Intake；L2-r4:L901。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W0 Normative 主責）

W0 的原文/Source/SPEC/QuestionLedger/Program 只有 SourceSpan+same Subject/Scope 作 W1 受影依據，W1 不重寫或簽 W0 原草案與定案。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W0 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L1174–1256` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-11 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-11",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W0",
  "OriginalReader": "SBL TPM/PIPD Intake；L2-r4:L901",
  "consumer": "SBL TPM/PIPD Intake；L2-r4:L901",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-11",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 1174,
    "end": 1256
  }
}
```

<a id="ch-12"></a>

# CH-12｜PIPD 13 CLI／19 Contract Families／8 Skills 與唯一 Writer

### r2 受影修補（2026-11-05｜AUTHOR_FINAL_AFFECTED_REPAIR）

**受影 Finding**：`F-05、N-02`。**原位差額**：13 CLI／有序 19 Families／8 Skills 由 SBL `main` blob 實讀重算；`ExecutionBindingRef` 仍為 seam-only，未以 `ExecutionBinding` 偷換；作者端不執行 compile，PD 亦不憑遠端 HEAD 綁定。

**未變更**：本章 H1 標題、L1 span／section SHA、OriginalID／Parent／NEG 與原 Reader 法位皆不變；原域 Raw 未取得者維持 `EXPECTED_NOT_OBSERVED`，不以作者推斷補值。

**下一個 Reader**：SBL Original PIPD Compiler／Repo Reader；FirstFail 見本章 POS／NEG／SEC 卡與 `AFFECTED_FINDINGS.jsonl` 對應列。

## W1 草案當期完成契約｜CH-12（DRAFT-W1-CH12）

**使用者可得結果**：SBL-hosted PIPD 13/19/8；合法執行範圍限 `SOURCE_READ` 與作者端規格審閱，無真 Host 准入或新 Writer 權限。

| 受影型別 | 本章可驗證的確定規則 |
|---|---|
| Input／觸發 | 同 Subject+SourceSHA+已知 Goal、13 CLI/19 source-order/8 skill 原始註冊清單；強制 `subject_id/source_manifest_sha/scope` 來源釘選 |
| 操作／Producer | 先從 SBL `integrations/pipd/` 的原 cli/registry/skills 檢索，逐身份確認；用 skill 只能寫 Sidecar；原 pipeline 才能寫 Canonical PI；Producer＝W1 DraftMaker（僅文字/Sidecar），正式效果由原域 Producer 執行 |
| Output／交付 | 原 CLI exact-set card、19 Ordered Family list、8 Skills card、OriginalWriter BindingRequest；所有未觀測 Reader Raw 留空並具名 `EXPECTED_NOT_OBSERVED` |
| Original Reader | SBL original PIPD CLI/registry/pipeline Reader；原 Writer／Issuer／Checker 不因本稿改權 |
| Downstream Consumer | PIPD Compiler；W2 PD/Execution；綁同 Subject／Scope，需 Original ACK 才可升級 |
| POS／Expected Raw | 13+19+8 一一對上原 Registry 且無 compile-cc 第14動詞；預期由原 Consumer 返回原格式 Raw（本輪 `NOT_RUN`） |
| NEG／首拒收 | 使用歷史 PIPD-LS-SP 作新 Writer 或 plugin 自製 canonical JSON；FirstFail=`PIPD_ABI_EXACT_SET_NACK` |
| EDGE | Installed 原 CLI 不存在時不據此宣布原 Host Loaded；只 PARK 受影 scope，合法 READ/DRAFT 不受波及 |
| SEC | 13 CLI 中新增或漏 verb；ExecutionBindingRef 次序失配；缺憑證、Owner、ACL 或 Checker 證物拒效果 |
| Stop／Resume／Rollback | 遇 `PIPD_ABI_EXACT_SET_NACK` 記 `hold_id+original_reader+required_raw`，停止受影寫入；Resume 需同 SourceSHA/Scope 的原 Reader 結果；READ 丟棄快照、DRAFT 刪除隔離候選；世界效果不在 W1 自行 rollback |
| Cross-wave | W2 CH15/WP06；W4 CI；交 `AUTHOR.FHS.W1ToW{next}@design` typed envelope，禁止偽裝 WorkOrder |

**受影源句拆義**：`actor/trigger/action/object`（見 Input/操作）；`condition/exception`（見 EDGE）；`prohibition`（見 NEG/SEC）；`outcome/consumer`（見 Output/Original Reader）；`POS/NEG/FirstFail` 必綁同一原 RequirementID。來源的原始句、Span、SHA、Parent/Child/NEG 以 r5 本章及附錄 `obligation_registry.jsonl` 回指；缺具體原 Reader 即 `ORIGINAL_OWNER_HOLD`，不自行創造簽核。


### R5 本章受影精確契約／業務負例（整合 r4，非歷史附錄）

唯一現行 19 Families 有序集合在「Product→PIPD」主清單；第 19 項 `ExecutionBindingRef`，原 Registry 明列 seam-only until S5，`GENIEProjectionRef` until S6。任何 `ExecutionBinding` 替名或 `compile-cc` 14th CLI → `PIPD_REGISTRY_EXACT_SET_NACK`。Installed Reader 未回 version/$id 時 `ORIGINAL_SCHEMA_ID_UNBOUND`。


**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L1257–1383`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original PIPD Registry/Compiler；L2-r4:L902。原 Domain Reader/Writer 不因本章轉移。

## r4 當期原 Reader 鎖與非降級本體

本章 L1-r4 依以上真實行區間及原域 Reader；無單獨 R4-BEGIN 增量不等於以歷史 r2 取代 L1。W1 契約下文僅是對該 L1 已定義原義的工程操作化。

## r4 對齊之 W1 主波操作規格、草案必填欄、逐項 POS/NEG／FirstFail（高保留整合）

**Protected Original H1 / CURRENT L1-r4**：`FHS_PIPD-LS-PKG_藍圖_2026-11-04_r4_HIGH_RETENTION_AUDIT_REPAIRED_實質正文(1).md:L1257–L1383`；`source_file_sha256=cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`；`section_sha256=d63aab54cf64bb0e828fb9019502a1acf94bcd24da0d6116755a996eb29b30ca`；`heading_exact=# CH-12｜PIPD 13 CLI／19 Contract Families／8 Skills 與唯一 Writer`；**HISTORICAL_LOCATOR_NOT_EFFECTIVE**=`L1:847–959` / `L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`，L2 作者端路由 `L2:650`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W1 不取得原 Writer。

## A. 本章實質功能與不能壓平的原義

SBL-hosted PIPD Canonical Reader 規格，13 CLI／19 families／8 skills 並列驗證，不創第14命令。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。

## B. 來源 r5 skeleton 必填核對欄（已由上方 W1 草案當期完成契約受影回填）

| 必填欄 | 欄位設計／不可空條件 |
|---|---|
<!-- HISTORICAL_R5_SKELETON_FILL_REQUEST_SUPERSEDED: transition wording only; all substantive constraints retained -->
| `chapter_id` / `primary_wave` / `author_writer` | `CH-12` / `W1` / `W1:DraftMaker`（歷史 r5 階段欄；當期為作者端定案候選） |
| `original_sources[]` | 本章 L1 行與下面原冊 SHA／OriginalClause Span；不得用語義假定的 ID 補空缺 |
| `same_subject` / `candidate_sha` / `source_manifest_sha` / `affected_scope` | 必攜相同 Subject/Scope，未原 Reader 認證則 `AUTHOR_CANDIDATE` |
| `effect_class` / `original_owner` / `consumer_abi` / `schema_version` | 依 Operation Reader；缺 `$id` 或 Receiver 不自造 |
| `input` / `typed_output` / `fuo` / `non_goals` | 應有真使用者結果與 Receiver（非檔案數） |
| `positive_fixture` / `negative_fixture` / `security_fixture` | 原 Source Case/Oracle 逐受影引用，未有 Runner/Raw 就 `EXPECTED_NOT_OBSERVED` |
| `first_fail` / `hold` / `stop_scope` / `resume_predicate` | 明確停止受影子圖，不全域凍結 READ／DRAFT |
| `rollback` / `w2_handoff` / `original_ack_nack` | 回退路由與 same scope 的預期接收；不得填假 PASS |

## C. Input → Producer → 原 Reader／Consumer → Output

- **Input/Guard**：原 SBL Current HEAD/registry SHA、PIPD installed version、CLI help/doctor Raw、Source refs。
- **Producer**：該 Original Domain 的 Reader/Compiler/Host/Guide 依本章功能生產；W1 Curator 僅記設計；**Original Consumer**：SBL integrations/pipd 原 Canonical Writer/Source Reader。
- **Typed Output/FUO**：`PIPD_ABI_READBACK` 或 `ORIGINAL_PIPD_READER_HOLD`；strict schema/sidecar 分離紀錄。
- **版本要求**：至少 `Subject,CandidateSHA,SourceSHA,OriginalID+SourceSpan,Scope,Host/PolicyEpoch（受影才填）,ABI $id/version,OriginalReader,OutputRawExpected`，少一欄只停需該欄的出口。

## D. POS／NEG／FirstFail／HOLD／退出

- **POS（期待）**：命令 13 unique，family 19 exact，skill packs 8；可見真正原 Reader response。
- **NEG／SEC（期待拒收）**：把 `compile-cc` 稱14th；舊 archived PIPD 作 active Writer。
- **FirstFail**：`PIPD_ABI_SHADOW_WRITER`；禁止只有泛稱 `VALIDATION_FAILED` 而不給首次失敗位置。
- **HOLD/Owner**：`H-PIPD-04；原 Host installed `pipd doctor` 尚未取得`。需同 Subject/Scope/Host/原 Reader 的真 Raw/ACK 解除；本輪 `NOT_RUN`。
- **Stop/Resume**：保留原 SourceSHA/受影 Reader/cursor/last-good；READ/DRAFT 合法部分繼續；UNKNOWN 必原 Reader reconcile。
- **Rollback**：只回復該 Need/Host 的原 last-good，Host/OPS 效果走原 inverse；不得以檔案 ZIP 作回復收據。

## E. 來源追溯、波次邊界與下一手

| 源鍵／檔案 | 原文 SHA | 此 W1 處理方式 |
|---|---|---|
| SBL-DOC-03 | ea69e1d3718ed86aecd74a3ebcc933960eacc30b586ab80fcb9f733037e33476 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| SBL-DOC-02 | 4ff0cda5ab00ba5f577151e5b004d2167d933e912e302c9e3529b237ccb9e035 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-02 | c336d3d9d702834e84bc2e45037e21e6ac56fb99c7abcb3adea372d901824ea2 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
W0 提供原 Source/三 SPEC/索引；本 `CH-12` 不修改 W0 成果。W1 WaveCurator 交 W1 DraftMaker 按原 Reader 定位填入真 Requirements；W2 僅領同 Subject/Scope 的需要的 Effect/Case/HOLD，不得借 W3/W4 收據。原 L1 CH-12 的詳細原義仍在 L1 主體，不移作本冊第二 Canonical。

## F. r2 原位修補：CH-12 可直接交接的受影實質規格（非證據附錄）

**本章不可壓平功能**：PIPD canonical writer exact-set CLI/families/skills。與 W0 三份獨立 SPEC 維持同 SourceSHA/Subject/Scope；將原讀者真接收的 **Output／Consumer** 優先於填滿文件欄位。依 L1 原 CH 身份與 L2 W1 主責修訂，不移轉原 Writer。

### F.1 原句→原 Consumer→本章測例的逐子義槽（已從原物理檔定位）

- **`SCL-W1-0013`** `[SOURCE:SBL-DOC-03:L834:sha256=ea69e1d3718ed86a]`：原文實質片段「/ world_effect_evidence / REQ-D02-0191 / world effect readback if applicable / required when applicable; otherwise Owner-approved N_A_ACCEPTED with reason / **SBL candidate typed projection** object with at lea」；Parent=`L816:### C18.1.13｜PI-13 — Evidence Expectation / Evidence freshness / 15 Native fields`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=SBL integrations/pipd original Compiler / CLI reader；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH12.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0014`** `[SOURCE:SBL-DOC-03:L1051:sha256=ea69e1d3718ed86a]`：原文實質片段「**P4 2026-10-19 實際契約 readback**：八個安裝 Skill 及各自 references/contract.md, schemas/input.schema.json, schemas/output.schema.json, tests/cases.yaml 已逐檔經插件讀取；但未執行 Native Skill 任務、無可供依賴的 Host Effective Load 收據、未獲得各 Sk」；Parent=`L1050:# C20｜P4 八段 Public Skills：Typed IO、首失敗、拒收與官方契約接線（受保護一級主章）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=SBL integrations/pipd original Compiler / CLI reader；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH12.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0015`** `[SOURCE:SBL-DOC-03:L3736:sha256=ea69e1d3718ed86a]`：原文實質片段「/ PIPD-LS-SP P4 / https://github.com/shw097-team/PIPD-LS-SP / 8 typed skill + native compiler; SBL candidate → PIPD adapters / MANDATED_BY_UPSTREAM / main e95942abcb6aa07e69304607ab8afc22a74fc67d / LICENSE_PEND」；Parent=`L3730:### R06.4｜TechnologySelectionBaseline-2026-10（首次具名產品設計選型，不是部署）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=SBL integrations/pipd original Compiler / CLI reader；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH12.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0016`** `[SOURCE:SBL-DOC-02:L6881:sha256=4ff0cda5ab00ba5f]`：原文實質片段「**r2 功能責任／來源判準**：GSD/AGENT_COMPONENTS/Matt subskills 各自具名翻譯與拒收。精確 Audit SourceRef=AUDIT_SBL_PIPD-LS-PKG_DOC-02_實質藍圖正文_全量破壞性審查_2026-10-18_r1(1).md:L255;sha256:864813a91c559b01e8ff78f1f47d8025d42194329d7f86b13bd7」；Parent=`L6879:## R02-08.3｜Thin adapter constraint`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=SBL integrations/pipd original Compiler / CLI reader；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH12.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0017`** `[SOURCE:SBL-DOC-02:L7686:sha256=4ff0cda5ab00ba5f]`：原文實質片段「**r2 功能責任／來源判準**：DOC03/05/06/09/10 各獨立 reader NACK 對應 schema。精確 Audit SourceRef=AUDIT_SBL_PIPD-LS-PKG_DOC-02_實質藍圖正文_全量破壞性審查_2026-10-18_r1(1).md:L260;sha256:864813a91c559b01e8ff78f1f47d8025d42194329d7f86b13bd761」；Parent=`L7684:## R02-10.2｜Downstream boundaries`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=SBL integrations/pipd original Compiler / CLI reader；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH12.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0018`** `[SOURCE:SBL-DOC-02:L10590:sha256=4ff0cda5ab00ba5f]`：原文實質片段「/ R02-07.2 / SPEC-D02-059 / PIPD_LS_DOC-02_2026-10-07_r2_HIGH_RETENTION_AUDIT_PATCHED_FULL_REPAIR_FULL_SUBSTANTIVE_BODY (1).md:L2@a021998dd3b63015… / Skill API 必遵守原 Input/Output schema，RepoContext 缺失不能 PD-bind 」；Parent=`L10546:## SectionSPECMapping｜55 個子節，r1 001～036 不偷換語義`；原 ID=`SPEC-D02-059`；NEG=`EXPLICIT:不能`。本章觸發/Consumer=SBL integrations/pipd original Compiler / CLI reader；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH12.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0019`** `[SOURCE:FHS-BODY-02:L24:sha256=c336d3d9d702834e]`：原文實質片段「**不構成阻斷的舊差異**：全17冊直接 intake 的舊 NACK 不適用這24條已接收的必要閉包。CLI13/14 差異只隔離新增 compile-cc 本身，本首工作使用兩版共有的 intake/profile/compile-pi/bind-pd/validate Reader。PI legacy DOC-03 DOMAIN_ORACLES 依原 Schema 原字保留；DOC07為 semantic Ow」；Parent=`L14:## HANDOFF-v1｜首工作功能 PI 的真 Compiler 接收`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=SBL integrations/pipd original Compiler / CLI reader；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH12.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0020`** `[SOURCE:FHS-BODY-02:L69:sha256=c336d3d9d702834e]`：原文實質片段「**遠端 main 此版 CLI 精確 13 命令**：init, intake, profile, compile-pi, bind-pd, compile-ecp, compile-tqaep, validate, doctor, project, export, diff, repair。Agent_Workspace/PIPD 本地 HEAD 995c7ad0c69a05a0c5cf6528155a62020」；Parent=`L59:### 2.3 PIPD 五個出口：每條分離，禁止用 PI/PD/ECP 串詞代替`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=SBL integrations/pipd original Compiler / CLI reader；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH12.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0021`** `[SOURCE:FHS-BODY-02:L213:sha256=c336d3d9d702834e]`：原文實質片段「- 原 Registry source：C:\Projects\Agent_Workspace\PIPD\schemas\RequirementAtom.schema.json；SHA 021f6a30cf178190281176138686447e492640cf97b125f9c21a0aa2fa31c684；$id=urn:pipd:s0:RequirementAtom:1；schema dialect 202」；Parent=`L211:#### RequirementAtom`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=SBL integrations/pipd original Compiler / CLI reader；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH12.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。

### F.2 本章 WP 與 Producer／typed I/O／FirstFail（每項獨立）

- **WP-FHS-05**：Producer=SBL-hosted original PIPD Compiler/Reader；Input=三份不同 SPECDraft、原 SourceManifest/Authority/Profile safety veto、原 PIPD Writer version；Output=非空 strict PI，真 RepoContext 才有 PD，DEV/OPS EffectIntent 分開，PlannedTQAEP 不冒 Checker；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=PIPD Native Compiler 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=把 _profile_meta 側掛塞進 strict PI；或憑 Caller HEAD 虛構本機 Repo binding；EDGE=PI SourceSHA 不變而 RepoHEAD 改變，只使 PD/ECP stale；不可偷重寫 PI requirement 原義；FirstFail=`PIPD_STRICT_SCHEMA_OR_SOURCE_NACK`；rollback=隔離候選刪除/回復 preimage；SourceSHA/HEAD 變更僅重編受影 PD/ECP。

### F.3 複合原義拆解、反向閉包與受影退出

- **「各有」**：本 CH 的每個原 clause locator 各自保留 SourceSHA/Parent/OriginalConsumer、POS/NEG；若原文有多個 named roles/Host/Case，不可用單一結果冒全數。
- **「分別」**：strict JSON body／@2 sidecar、Original Policy Active／Host Loaded、Maker challenge／Protected Checker、Selected／ActualServed 是不同欄位與收據，不得合併。
- **「對應」**：必 `original source line → SCL-W1 id → CH → W1 WP → expected Case → original source line` 可機械重算；原 OriginalID 未明者只引用明示的 SourceSpan，不可猜 ID。
- **「不得／若／除非」**：否定作用域保留到原 Parent context；本章只標作者候選，原 Source Reader 取得 ACK 才能宣告原語義接受。
- **退出**：原 Reader NACK 僅 PARK 本章受影的 PI/PD/DEV/OPS/Host operation；合法 SOURCE_READ、隔離草稿及不依賴該 ABI 的 W0/W2 工作照原許可前進。

## 本章 L2-r4 設計義務接收卡（逐 ID；不可省略原 NEG）

- `INT-06` (`L1-r4:L774`, `L2-r4:L320`)：一個現役 PIPD Compiler Writer；SBL integrations/pipd 13 CLI／19 families／8 skills，薄 Adapter；[CH-12](#ch-12)/[CH-13](#ch-13)；POS `SBL integrations/pipd 13 CLI／19 families／8 skills，薄 Adapter`；NEG/FirstFail `將歷史 PIPD-LS-SP 當現役唯一 Writer，或技能自行簽 PI；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `SBL-hosted PIPD canonical Compiler/Original Source/Repo/Case Reader`；本輪只有 EXPECTED_NOT_OBSERVED。
- `INT-13` (`L1-r4:L781`, `L2-r4:L327`)：PIPD PI/PD/ECP/TQAEP 分層；PI source-bound，PD 晚綁 Repo，ECP 非 Admission，TQAEP 依 Original Oracle；[CH-12](#ch-12)/[CH-13](#ch-13)/[CH-14](#ch-14)/[CH-15](#ch-15)/[CH-41](#ch-41)；POS `PI source-bound，PD 晚綁 Repo，ECP 非 Admission，TQAEP 依 Original Oracle`；NEG/FirstFail `ECP intent 冒 Issuer Permit；PD 未 live RepoContext 即號稱已綁；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `SBL RepoContext/PD Reader → HGK Original Issuer → Repo World Reader、SBL-hosted PIPD canonical Compiler/Original Source/Repo/Case Reader；原末端 Receiver＝`INT-13_CONSUMER_LOCATOR_SOURCE_TRUNCATION_HOLD`（L1/L2 源列被截斷，非已綁定）`；本輪只有 EXPECTED_NOT_OBSERVED。
- `FHS-DR-027` (`L1-r4:L824`, `L2-r4:L365`)：PIPD/TPM／A；TQAEP/19 Schema/13 CLI/8 Skill 原 ABI 不私改；以實際 Canonical Pipeline 與 installed Reader 判斷；[CH-12](#ch-12)/[CH-41](#ch-41)；POS `Case 有正負例和待原 Checker 收據`；NEG/FirstFail `不核 ABI 就加 compile-cc 14th verb；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `SBL-hosted PIPD canonical Compiler/Original Source/Repo/Case Reader`；本輪只有 EXPECTED_NOT_OBSERVED。

## CH-12 專屬退出與回退

DraftMaker 後續須填 `original_reader_ref`, `original_schema_version_or_HOLD`, `source_span_sha`, `same_subject_and_scope`, `Case/Oracle`, `positive_raw_expected`, `negative_raw_expected`, `first_fail`, `resume_predicate`, `last_good`, `consumer_ack_or_HOLD`。`DOC_AUTHOR_DONE` 是本檔可檢索，不是 `PIPD 13 CLI／19 Contract Families／8 Skills 與唯一 Writer` 已原 Host Qualified。若權限／能力尚缺，只 PARK 受影操作；回退到該 Domain 上次有效 Reader/Host 版本、保留跨波合法 READ/DRAFT，且不得刪原 NEG 或憑此文件自簽。



## AUTHOR-FINAL｜CH-12 受影交付契約

**Input / Operation / Output**：保留本章原有專屬 I/O、原句與 NEG；以當期 Registry 對同 SourceSHA/Subject/Scope 重算受影子圖，輸出 CH-12 的原 Reader BindingRequest，實質輸出與業務 FirstFail 以本章上文專屬契約及下列子義為準。

**Original Reader / Original Consumer**：SBL-hosted PIPD Original CLI/Registry Reader；原 Consumer Raw=EXPECTED_NOT_OBSERVED。L1 起始 1257、終止 1383，section SHA `d63aab54cf64bb0e828fb9019502a1acf94bcd24da0d6116755a996eb29b30ca`。

**POS / NEG / FirstFail**：本章專屬正負條件逐筆如下；沒有適用子義的跨 ABI 章以原本章完整 POS/NEG 為準，不從別章借用 PASS。**EDGE**：SourceSHA/Host/PolicyEpoch 其中一欄改變，只 invalidate 受影接線；**SEC**：Maker 假 ACK 或跨 Principal 原回條均拒收。**ExpectedRaw**：同 Subject/Candidate/Scope 原 Consumer/World bytes；本輪 NOT_RUN。**Stop**：缺該 Effect 必需原 Reader 即 PARK 其效果；**Resume**：同 Scope 原 Reader 提供具名 Raw；**NextWave**：W2 原 Effect Receiver，四 Host/Cell/W18 交 W3，CI/Publisher 交 W4。

- `S-W1-INT-06-01`：Input=SBL integrations/pipd 是唯一 active Compiler；POS=原 CLI 命令/Registry 原核讀回；NEG=歷史 PIPD-LS-SP 重開第二 Writer；FirstFail=`PIPD_SHADOW_WRITER_DENY`；Consumer=SBL-hosted PIPD Compiler and Source Registry；Case=`AUTHOR.W1.INT-06.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-06-02`：Input=13 CLI 原命令順序不可擅改；POS=13 個原 help verbs 按序一致；NEG=新增 compile-cc；FirstFail=`PIPD_CLI_EXACT_SET_NACK`；Consumer=SBL-hosted PIPD Compiler and Source Registry；Case=`AUTHOR.W1.INT-06.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-06-03`：Input=19 family 及 8 Skill 分別核 exact identity；POS=原 Registry 第19項 ExecutionBindingRef；NEG=以 ExecutionBinding 取代該 family；FirstFail=`PIPD_REGISTRY_EXACT_SET_NACK`；Consumer=SBL-hosted PIPD Compiler and Source Registry；Case=`AUTHOR.W1.INT-06.03.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-13-01`：Input=PI 綁 Original Source／Parent／NEG／OriginalID；POS=原 Compiler 確認非空 strict PI；NEG=用 GPT 產 JSON 冒 Canonical PI；FirstFail=`PIPD_STRICT_PI_WRITER_NACK`；Consumer=SBL-hosted PIPD Reader; missing original final receiver HOLD；Case=`AUTHOR.W1.INT-13.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-13-02`：Input=PD 僅綁同 Scope 真 local RepoContext；POS=本地 HEAD/index/untracked/preimage 俱全；NEG=remote GitHub HEAD 充 local probe；FirstFail=`PD_REPOCONTEXT_UNBOUND`；Consumer=SBL-hosted PIPD Reader; missing original final receiver HOLD；Case=`AUTHOR.W1.INT-13.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-13-03`：Input=ECP intention≠Issuer Permit；POS=原 HGK admission 出具同 scope nonce/epoch；NEG=直接以 ECP intention 做世界效果；FirstFail=`ECP_NOT_ISSUER_PERMIT`；Consumer=SBL-hosted PIPD Reader; missing original final receiver HOLD；Case=`AUTHOR.W1.INT-13.03.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-13-04`：Input=TQAEP 必連 Original Oracle/Runner/Checker；POS=具名 Case 和原 Reader 對應；NEG=Maker 自簽原 Checker verdict；FirstFail=`SELF_ATTESTED_TQAEP_NACK`；Consumer=SBL-hosted PIPD Reader; missing original final receiver HOLD；Case=`AUTHOR.W1.INT-13.04.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-13-05`：Input=原上游截斷的 Receiver 不得自行補名；POS=原 Domain Reader 同 Subject ACK 才填端點；NEG=把 Original Domai 視為完整 Receiver；FirstFail=`RECEIVER_IDENTITY_HOLD`；Consumer=SBL-hosted PIPD Reader; missing original final receiver HOLD；Case=`AUTHOR.W1.INT-13.05.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-027-01`：Input=13/19/8 原 ABI 精確有序一致；POS=source-order+schema $id/version 相符；NEG=添加第14 CLI 或 family 改名；FirstFail=`PIPD_REGISTRY_EXACT_SET_NACK`；Consumer=Original PIPD Schema/Case/CLI Reader；Case=`AUTHOR.W1.FHS-DR-027.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-027-02`：Input=原 TQAEP Case 各連 POS/NEG/Original Oracle；POS=原 CaseRaw/Runner/Checker 身份；NEG=缺 Runner 卻宣 Independent qualified；FirstFail=`TQAEP_RUNNER_UNBOUND`；Consumer=Original PIPD Schema/Case/CLI Reader；Case=`AUTHOR.W1.FHS-DR-027.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。

<a id="ch-13"></a>

# CH-13｜Authority SourceFreeze／Profile Tailoring／原 PI 的 18 領域

### r2 受影修補（2026-11-05｜AUTHOR_FINAL_AFFECTED_REPAIR）

**受影 Finding**：`F-01、F-02、F-05`。**原位差額**：Authority SourceFreeze 的 31 源 SHA 與 13 個 L1 章 span 於 r2 重算；OriginalID／Parent／NEG／Oracle 未取得者逐項具名 HOLD，不以主題相近補值。

**未變更**：本章 H1 標題、L1 span／section SHA、OriginalID／Parent／NEG 與原 Reader 法位皆不變；原域 Raw 未取得者維持 `EXPECTED_NOT_OBSERVED`，不以作者推斷補值。

**下一個 Reader**：SBL Original Source Reader；FirstFail 見本章 POS／NEG／SEC 卡與 `AFFECTED_FINDINGS.jsonl` 對應列。

## W1 草案當期完成契約｜CH-13（DRAFT-W1-CH13）

**使用者可得結果**：Authority/Profile/PI semantic preservation；合法執行範圍限 `LOCAL_DRAFT_WRITE` 與作者端規格審閱，無真 Host 准入或新 Writer 權限。

| 受影型別 | 本章可驗證的確定規則 |
|---|---|
| Input／觸發 | Goal、Source Families、Owner/Currentness、九軸 profile、OriginalID/Parent/NEG/Oracle；強制 `subject_id/source_manifest_sha/scope` 來源釘選 |
| 操作／Producer | 按 U0 provenance→U1 拆子義，為每 family 記 digest/span/否定及 conflict；Profile 嚴禁安全降級；PI 僅向 SBL canonical compiler 提交，缺 Reader 返 BindingRequest；Producer＝W1 DraftMaker（僅文字/Sidecar），正式效果由原域 Producer 執行 |
| Output／交付 | SourceFreeze 提案、ProfileBinding 提案、PI Crosswalk Sidecar（明標非 Canonical）；所有未觀測 Reader Raw 留空並具名 `EXPECTED_NOT_OBSERVED` |
| Original Reader | 原 SBL PIPD Source/Authority/Profile/PI Reader；原 Writer／Issuer／Checker 不因本稿改權 |
| Downstream Consumer | Original PI-PKG writer / PD Binder；綁同 Subject／Scope，需 Original ACK 才可升級 |
| POS／Expected Raw | 同 Source/Scope 之 Parent、NEG、Case 索引可正反重放；預期由原 Consumer 返回原格式 Raw（本輪 `NOT_RUN`） |
| NEG／首拒收 | 虛構 SourceFreeze、移除安全 veto、將 Sidecar 設為正式 PI；FirstFail=`SOURCE_AUTHORITY_OR_PI_READER_HOLD` |
| EDGE | Source Currentness 與 profile 雜訊時區分影響範圍；只 PARK 受影 scope，合法 READ/DRAFT 不受波及 |
| SEC | 非 Owner ACK 的作者端註解冒稱正式批准；缺憑證、Owner、ACL 或 Checker 證物拒效果 |
| Stop／Resume／Rollback | 遇 `SOURCE_AUTHORITY_OR_PI_READER_HOLD` 記 `hold_id+original_reader+required_raw`，停止受影寫入；Resume 需同 SourceSHA/Scope 的原 Reader 結果；READ 丟棄快照、DRAFT 刪除隔離候選；世界效果不在 W1 自行 rollback |
| Cross-wave | W2 原 PI→PD 的效力；交 `AUTHOR.FHS.W1ToW{next}@design` typed envelope，禁止偽裝 WorkOrder |

**受影源句拆義**：`actor/trigger/action/object`（見 Input/操作）；`condition/exception`（見 EDGE）；`prohibition`（見 NEG/SEC）；`outcome/consumer`（見 Output/Original Reader）；`POS/NEG/FirstFail` 必綁同一原 RequirementID。來源的原始句、Span、SHA、Parent/Child/NEG 以 r5 本章及附錄 `obligation_registry.jsonl` 回指；缺具體原 Reader 即 `ORIGINAL_OWNER_HOLD`，不自行創造簽核。


### R5 本章受影精確契約／業務負例（整合 r4，非歷史附錄）

Source freeze 各 family hash+contained locator+authority/conflict；Profile 9 軸 safety veto 不能降義務；strict PI 原 OriginalID/Parent/NEG/Oracle/FUO 不丟。保留原 SourceSHA 的長行否定；`SOURCE_CONTEXT_FRAGMENT_OWNER_HOLD` 時不可產假 formal atom。NEG=只有 MD metadata approved 就 SourceFreeze → `SOURCE_FREEZE_APPROVAL_SPOOF`。


**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L1384–1448`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original PIPD Authority/Profile/PI Writer；L2-r4:L903。原 Domain Reader/Writer 不因本章轉移。

## r4 當期原 Reader 鎖與非降級本體

本章 L1-r4 依以上真實行區間及原域 Reader；無單獨 R4-BEGIN 增量不等於以歷史 r2 取代 L1。W1 契約下文僅是對該 L1 已定義原義的工程操作化。

## r4 對齊之 W1 主波操作規格、草案必填欄、逐項 POS/NEG／FirstFail（高保留整合）

**Protected Original H1 / CURRENT L1-r4**：`FHS_PIPD-LS-PKG_藍圖_2026-11-04_r4_HIGH_RETENTION_AUDIT_REPAIRED_實質正文(1).md:L1384–L1448`；`source_file_sha256=cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`；`section_sha256=8917c10f6fda394e8297fe794cedc5ba20f1179291cba8cf890265a5e3fe21f9`；`heading_exact=# CH-13｜Authority SourceFreeze／Profile Tailoring／原 PI 的 18 領域`；**HISTORICAL_LOCATOR_NOT_EFFECTIVE**=`L1:960–1010` / `L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`，L2 作者端路由 `L2:651`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W1 不取得原 Writer。

## A. 本章實質功能與不能壓平的原義

Authority → Profile nine-axis safety veto → 原 PI-01..18：身份不變，OriginalID/Parent/NEG 可反查。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。

## B. 來源 r5 skeleton 必填核對欄（已由上方 W1 草案當期完成契約受影回填）

| 必填欄 | 欄位設計／不可空條件 |
|---|---|
<!-- HISTORICAL_R5_SKELETON_FILL_REQUEST_SUPERSEDED: transition wording only; all substantive constraints retained -->
| `chapter_id` / `primary_wave` / `author_writer` | `CH-13` / `W1` / `W1:DraftMaker`（歷史 r5 階段欄；當期為作者端定案候選） |
| `original_sources[]` | 本章 L1 行與下面原冊 SHA／OriginalClause Span；不得用語義假定的 ID 補空缺 |
| `same_subject` / `candidate_sha` / `source_manifest_sha` / `affected_scope` | 必攜相同 Subject/Scope，未原 Reader 認證則 `AUTHOR_CANDIDATE` |
| `effect_class` / `original_owner` / `consumer_abi` / `schema_version` | 依 Operation Reader；缺 `$id` 或 Receiver 不自造 |
| `input` / `typed_output` / `fuo` / `non_goals` | 應有真使用者結果與 Receiver（非檔案數） |
| `positive_fixture` / `negative_fixture` / `security_fixture` | 原 Source Case/Oracle 逐受影引用，未有 Runner/Raw 就 `EXPECTED_NOT_OBSERVED` |
| `first_fail` / `hold` / `stop_scope` / `resume_predicate` | 明確停止受影子圖，不全域凍結 READ／DRAFT |
| `rollback` / `w2_handoff` / `original_ack_nack` | 回退路由與 same scope 的預期接收；不得填假 PASS |

## C. Input → Producer → 原 Reader／Consumer → Output

- **Input/Guard**：W0 three SPEC+Original SourceSet/Scope/AuthorityBinding/ProfileRequirement。
- **Producer**：該 Original Domain 的 Reader/Compiler/Host/Guide 依本章功能生產；W1 Curator 僅記設計；**Original Consumer**：原 PIPD Intake/PI Reader 及 Source/Oracle Owner。
- **Typed Output/FUO**：nonempty strict PI 候選與 `SBL.PI.Crosswalk@2` 資料旁掛（不混入）。
- **版本要求**：至少 `Subject,CandidateSHA,SourceSHA,OriginalID+SourceSpan,Scope,Host/PolicyEpoch（受影才填）,ABI $id/version,OriginalReader,OutputRawExpected`，少一欄只停需該欄的出口。

## D. POS／NEG／FirstFail／HOLD／退出

- **POS（期待）**：同 SourceSpan SHA 重導 RequirementAtom；九軸 veto 不可降低 safety。
- **NEG／SEC（期待拒收）**：空 PI／NEG 丟失／_profile_meta 放 strict PI。
- **FirstFail**：`PI_CLAUSE_OR_POLARITY_LOSS`；禁止只有泛稱 `VALIDATION_FAILED` 而不給首次失敗位置。
- **HOLD/Owner**：`原 Original Domain SourceFreeze/Owner ACK、CR-DOC04-STATE-MAP`。需同 Subject/Scope/Host/原 Reader 的真 Raw/ACK 解除；本輪 `NOT_RUN`。
- **Stop/Resume**：保留原 SourceSHA/受影 Reader/cursor/last-good；READ/DRAFT 合法部分繼續；UNKNOWN 必原 Reader reconcile。
- **Rollback**：只回復該 Need/Host 的原 last-good，Host/OPS 效果走原 inverse；不得以檔案 ZIP 作回復收據。

## E. 來源追溯、波次邊界與下一手

| 源鍵／檔案 | 原文 SHA | 此 W1 處理方式 |
|---|---|---|
| SBL-DOC-03 | ea69e1d3718ed86aecd74a3ebcc933960eacc30b586ab80fcb9f733037e33476 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| SBL-DOC-05 | 3b47a0b6224b1984a4047cf53aac5ac50615c93a560fea46e1b43d079a5d9f27 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-02 | c336d3d9d702834e84bc2e45037e21e6ac56fb99c7abcb3adea372d901824ea2 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
W0 提供原 Source/三 SPEC/索引；本 `CH-13` 不修改 W0 成果。W1 WaveCurator 交 W1 DraftMaker 按原 Reader 定位填入真 Requirements；W2 僅領同 Subject/Scope 的需要的 Effect/Case/HOLD，不得借 W3/W4 收據。原 L1 CH-13 的詳細原義仍在 L1 主體，不移作本冊第二 Canonical。

## F. r2 原位修補：CH-13 可直接交接的受影實質規格（非證據附錄）

**本章不可壓平功能**：Authority/Profile/safety veto/strict PI。與 W0 三份獨立 SPEC 維持同 SourceSHA/Subject/Scope；將原讀者真接收的 **Output／Consumer** 優先於填滿文件欄位。依 L1 原 CH 身份與 L2 W1 主責修訂，不移轉原 Writer。

### F.1 原句→原 Consumer→本章測例的逐子義槽（已從原物理檔定位）

- **`SCL-W1-0022`** `[SOURCE:SBL-DOC-03:L1053:sha256=ea69e1d3718ed86a]`：原文實質片段「Goal + SourceLocator → pipd-route-intake **candidate**；SourceFamily/digest/locator → pipd-authority-source source freeze **official gated**；profile+九軸 → pipd-profile-tailor；Join 形成受核准源、有效 profile、非零 atoms 後 → p」；Parent=`L1052:## C20.1｜八階職責、共同信任邊界與執行路由`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不能`。本章觸發/Consumer=PIPD original SourceAuthority/Profile/PI Reader；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH13.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0023`** `[SOURCE:SBL-DOC-03:L1212:sha256=ea69e1d3718ed86a]`：原文實質片段「**Preconditions / POS**：one sourced atom with exact owner and goal ⇒ Native compiler can produce content-addressed PI and TraceLink only after valid freeze/oracle adjudication。**NEG**：req_id=U03.1 or owner=SBL_」；Parent=`L1207:### C20.2.4｜`pipd-pi-compile` — owner/typed input-output/首失敗各自獨立`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=PIPD original SourceAuthority/Profile/PI Reader；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH13.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0024`** `[SOURCE:SBL-DOC-03:L1594:sha256=ea69e1d3718ed86a]`：原文實質片段「- **Input**：frozen intent, profile, atoms req_id/source_clause/owner/acceptance_cue/risk_guard。**Output**：PI-PKG stable_semantic_contract/acceptance/trace。以原 schema 的 required, enum, minItems, additionalPropert」；Parent=`L1590:#### pipd-pi-compile｜單獨可驗收接線`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=PIPD original SourceAuthority/Profile/PI Reader；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH13.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0025`** `[SOURCE:SBL-DOC-05:L5866:sha256=3b47a0b6224b1984]`：原文實質片段「/ SBL_PIPD-LS-PKG_DOC-05_藍圖+skeleton.md#L1650 / R07.2 Tool/Module Anti-Downgrade Register / D05-ATOM-036 → SBL-D05-SPEC-ATOM-036（承接 R07 的具名 Typed IO；同來源 digest、subject_sha） / ACC-D05-ATOM-036：至少原子 source_ref+ow」；Parent=`L5825:## R08.6｜52 個歷史 H2 → 原始 Clause／原子 SPEC／ACC／雙向 Fixture／EExp／DELIVER（作者端候選）`；原 ID=`SPEC-ATOM-036`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=PIPD original SourceAuthority/Profile/PI Reader；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH13.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0026`** `[SOURCE:SBL-DOC-05:L5874:sha256=3b47a0b6224b1984]`：原文實質片段「/ SBL_PIPD-LS-PKG_DOC-05_藍圖+skeleton.md#L2360 / R09.3 擴充反例（真可拒收） / D05-ATOM-044 → SBL-D05-SPEC-ATOM-044（承接 R09 的具名 Typed IO；同來源 digest、subject_sha） / ACC-D05-ATOM-044：至少原子 source_ref+owner+非空可解析 Typed Output；FX」；Parent=`L5825:## R08.6｜52 個歷史 H2 → 原始 Clause／原子 SPEC／ACC／雙向 Fixture／EExp／DELIVER（作者端候選）`；原 ID=`SPEC-ATOM-044`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=PIPD original SourceAuthority/Profile/PI Reader；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH13.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0027`** `[SOURCE:SBL-DOC-05:L5882:sha256=3b47a0b6224b1984]`：原文實質片段「/ SBL_PIPD-LS-PKG_DOC-05_藍圖+skeleton.md#L2671 / R11.4｜原 r1 物理來源與卷冊完整索引（歷史唯讀資料，不代表 r2 自動採納） / D05-ATOM-052 → SBL-D05-SPEC-ATOM-052（承接 R11 的具名 Typed IO；同來源 digest、subject_sha） / ACC-D05-ATOM-052：至少原子 source_ref+o」；Parent=`L5825:## R08.6｜52 個歷史 H2 → 原始 Clause／原子 SPEC／ACC／雙向 Fixture／EExp／DELIVER（作者端候選）`；原 ID=`SPEC-ATOM-052`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=PIPD original SourceAuthority/Profile/PI Reader；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH13.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0028`** `[SOURCE:FHS-BODY-02:L18:sha256=c336d3d9d702834e]`：原文實質片段「**可直接讀取的實例**：02_FIRST_WORK/RUN/ProductSPEC.json、ArchitectureSPEC.json、ProgramSPEC.json 由原 sbl-tpm-sp plan_spec 實際產生；SourceAuthority.json 由原 PIPD freeze_authority 產生，SourceFamily digest/locator 逐檔釘住；IntentCard.j」；Parent=`L14:## HANDOFF-v1｜首工作功能 PI 的真 Compiler 接收`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=PIPD original SourceAuthority/Profile/PI Reader；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH13.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0029`** `[SOURCE:FHS-BODY-02:L63:sha256=c336d3d9d702834e]`：原文實質片段「/ E1 SOURCE/PROFILE→PI / Goal＋SourceFamily ManifestSHA＋Profile nine-axis/Oracle→原 pipd intake/profile/compile-pi 和 PIPD DOC02 原 Writer→PI-PKG/RequirementAtom / POS strict schema＋SourceSHA 同 Subject；缺 Source、Pro」；Parent=`L59:### 2.3 PIPD 五個出口：每條分離，禁止用 PI/PD/ECP 串詞代替`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=PIPD original SourceAuthority/Profile/PI Reader；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH13.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0030`** `[SOURCE:FHS-BODY-02:L437:sha256=c336d3d9d702834e]`：原文實質片段「SOURCE/PROFILE→PI：pipd-route-intake 只收 nonblank goal+contained sources；authority-source每family有file digest+locators，衝突拒freeze；profile-tailor九軸safety veto不得降級；pi-compile strict shape只有intent/profile/atoms/goal。P」；Parent=`L435:## R2-02-HANDOFF：五個正式出口與候選隔離`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不得,NEG`。本章觸發/Consumer=PIPD original SourceAuthority/Profile/PI Reader；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH13.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。

### F.2 本章 WP 與 Producer／typed I/O／FirstFail（每項獨立）

- **WP-FHS-05**：Producer=SBL-hosted original PIPD Compiler/Reader；Input=三份不同 SPECDraft、原 SourceManifest/Authority/Profile safety veto、原 PIPD Writer version；Output=非空 strict PI，真 RepoContext 才有 PD，DEV/OPS EffectIntent 分開，PlannedTQAEP 不冒 Checker；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=PIPD Native Compiler 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=把 _profile_meta 側掛塞進 strict PI；或憑 Caller HEAD 虛構本機 Repo binding；EDGE=PI SourceSHA 不變而 RepoHEAD 改變，只使 PD/ECP stale；不可偷重寫 PI requirement 原義；FirstFail=`PIPD_STRICT_SCHEMA_OR_SOURCE_NACK`；rollback=隔離候選刪除/回復 preimage；SourceSHA/HEAD 變更僅重編受影 PD/ECP。

### F.3 複合原義拆解、反向閉包與受影退出

- **「各有」**：本 CH 的每個原 clause locator 各自保留 SourceSHA/Parent/OriginalConsumer、POS/NEG；若原文有多個 named roles/Host/Case，不可用單一結果冒全數。
- **「分別」**：strict JSON body／@2 sidecar、Original Policy Active／Host Loaded、Maker challenge／Protected Checker、Selected／ActualServed 是不同欄位與收據，不得合併。
- **「對應」**：必 `original source line → SCL-W1 id → CH → W1 WP → expected Case → original source line` 可機械重算；原 OriginalID 未明者只引用明示的 SourceSpan，不可猜 ID。
- **「不得／若／除非」**：否定作用域保留到原 Parent context；本章只標作者候選，原 Source Reader 取得 ACK 才能宣告原語義接受。
- **退出**：原 Reader NACK 僅 PARK 本章受影的 PI/PD/DEV/OPS/Host operation；合法 SOURCE_READ、隔離草稿及不依賴該 ABI 的 W0/W2 工作照原許可前進。

## 本章 L2-r4 設計義務接收卡（逐 ID；不可省略原 NEG）

- `INT-06` (`L1-r4:L774`, `L2-r4:L320`)：一個現役 PIPD Compiler Writer；SBL integrations/pipd 13 CLI／19 families／8 skills，薄 Adapter；[CH-12](#ch-12)/[CH-13](#ch-13)；POS `SBL integrations/pipd 13 CLI／19 families／8 skills，薄 Adapter`；NEG/FirstFail `將歷史 PIPD-LS-SP 當現役唯一 Writer，或技能自行簽 PI；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `SBL-hosted PIPD canonical Compiler/Original Source/Repo/Case Reader`；本輪只有 EXPECTED_NOT_OBSERVED。
- `INT-13` (`L1-r4:L781`, `L2-r4:L327`)：PIPD PI/PD/ECP/TQAEP 分層；PI source-bound，PD 晚綁 Repo，ECP 非 Admission，TQAEP 依 Original Oracle；[CH-12](#ch-12)/[CH-13](#ch-13)/[CH-14](#ch-14)/[CH-15](#ch-15)/[CH-41](#ch-41)；POS `PI source-bound，PD 晚綁 Repo，ECP 非 Admission，TQAEP 依 Original Oracle`；NEG/FirstFail `ECP intent 冒 Issuer Permit；PD 未 live RepoContext 即號稱已綁；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `SBL RepoContext/PD Reader → HGK Original Issuer → Repo World Reader、SBL-hosted PIPD canonical Compiler/Original Source/Repo/Case Reader；原末端 Receiver＝`INT-13_CONSUMER_LOCATOR_SOURCE_TRUNCATION_HOLD`（L1/L2 源列被截斷，非已綁定）`；本輪只有 EXPECTED_NOT_OBSERVED。
- `FHS-DR-023` (`L1-r4:L820`, `L2-r4:L361`)：PIPD/TPM／A；SourceFreeze 由原 PIPD/Source Reader 綁定；source family sha/locator/authority/conflict；[CH-13](#ch-13)；POS `不合格來源受影 HOLD`；NEG/FirstFail `用 MD metadata 的 approved 字樣繞 Reader；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `SBL-hosted PIPD canonical Compiler/Original Source/Repo/Case Reader`；本輪只有 EXPECTED_NOT_OBSERVED。
- `FHS-DR-024` (`L1-r4:L821`, `L2-r4:L362`)：PIPD/TPM／A；PI 保留 OriginalID/ClauseSHA/Parent/POS/NEG/Oracle/FUO；由 SBL integrations/pipd 正式 Writer 編譯；[CH-13](#ch-13)；POS `原 PIPD Reader 實收／錯誤有型別`；NEG/FirstFail `GPT 生成 JSON 假裝正式 PI；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `SBL-hosted PIPD canonical Compiler/Original Source/Repo/Case Reader`；本輪只有 EXPECTED_NOT_OBSERVED。

## CH-13 專屬退出與回退

DraftMaker 後續須填 `original_reader_ref`, `original_schema_version_or_HOLD`, `source_span_sha`, `same_subject_and_scope`, `Case/Oracle`, `positive_raw_expected`, `negative_raw_expected`, `first_fail`, `resume_predicate`, `last_good`, `consumer_ack_or_HOLD`。`DOC_AUTHOR_DONE` 是本檔可檢索，不是 `Authority SourceFreeze／Profile Tailoring／原 PI 的 18 領域` 已原 Host Qualified。若權限／能力尚缺，只 PARK 受影操作；回退到該 Domain 上次有效 Reader/Host 版本、保留跨波合法 READ/DRAFT，且不得刪原 NEG 或憑此文件自簽。



## AUTHOR-FINAL｜CH-13 受影交付契約

**Input / Operation / Output**：保留本章原有專屬 I/O、原句與 NEG；以當期 Registry 對同 SourceSHA/Subject/Scope 重算受影子圖，輸出 CH-13 的原 Reader BindingRequest，實質輸出與業務 FirstFail 以本章上文專屬契約及下列子義為準。

**Original Reader / Original Consumer**：Original Source/Authority/PIPD Writer；原 Consumer Raw=EXPECTED_NOT_OBSERVED。L1 起始 1384、終止 1448，section SHA `8917c10f6fda394e8297fe794cedc5ba20f1179291cba8cf890265a5e3fe21f9`。

**POS / NEG / FirstFail**：本章專屬正負條件逐筆如下；沒有適用子義的跨 ABI 章以原本章完整 POS/NEG 為準，不從別章借用 PASS。**EDGE**：SourceSHA/Host/PolicyEpoch 其中一欄改變，只 invalidate 受影接線；**SEC**：Maker 假 ACK 或跨 Principal 原回條均拒收。**ExpectedRaw**：同 Subject/Candidate/Scope 原 Consumer/World bytes；本輪 NOT_RUN。**Stop**：缺該 Effect 必需原 Reader 即 PARK 其效果；**Resume**：同 Scope 原 Reader 提供具名 Raw；**NextWave**：W2 原 Effect Receiver，四 Host/Cell/W18 交 W3，CI/Publisher 交 W4。

- `S-W1-INT-06-01`：Input=SBL integrations/pipd 是唯一 active Compiler；POS=原 CLI 命令/Registry 原核讀回；NEG=歷史 PIPD-LS-SP 重開第二 Writer；FirstFail=`PIPD_SHADOW_WRITER_DENY`；Consumer=SBL-hosted PIPD Compiler and Source Registry；Case=`AUTHOR.W1.INT-06.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-06-02`：Input=13 CLI 原命令順序不可擅改；POS=13 個原 help verbs 按序一致；NEG=新增 compile-cc；FirstFail=`PIPD_CLI_EXACT_SET_NACK`；Consumer=SBL-hosted PIPD Compiler and Source Registry；Case=`AUTHOR.W1.INT-06.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-06-03`：Input=19 family 及 8 Skill 分別核 exact identity；POS=原 Registry 第19項 ExecutionBindingRef；NEG=以 ExecutionBinding 取代該 family；FirstFail=`PIPD_REGISTRY_EXACT_SET_NACK`；Consumer=SBL-hosted PIPD Compiler and Source Registry；Case=`AUTHOR.W1.INT-06.03.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-13-01`：Input=PI 綁 Original Source／Parent／NEG／OriginalID；POS=原 Compiler 確認非空 strict PI；NEG=用 GPT 產 JSON 冒 Canonical PI；FirstFail=`PIPD_STRICT_PI_WRITER_NACK`；Consumer=SBL-hosted PIPD Reader; missing original final receiver HOLD；Case=`AUTHOR.W1.INT-13.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-13-02`：Input=PD 僅綁同 Scope 真 local RepoContext；POS=本地 HEAD/index/untracked/preimage 俱全；NEG=remote GitHub HEAD 充 local probe；FirstFail=`PD_REPOCONTEXT_UNBOUND`；Consumer=SBL-hosted PIPD Reader; missing original final receiver HOLD；Case=`AUTHOR.W1.INT-13.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-13-03`：Input=ECP intention≠Issuer Permit；POS=原 HGK admission 出具同 scope nonce/epoch；NEG=直接以 ECP intention 做世界效果；FirstFail=`ECP_NOT_ISSUER_PERMIT`；Consumer=SBL-hosted PIPD Reader; missing original final receiver HOLD；Case=`AUTHOR.W1.INT-13.03.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-13-04`：Input=TQAEP 必連 Original Oracle/Runner/Checker；POS=具名 Case 和原 Reader 對應；NEG=Maker 自簽原 Checker verdict；FirstFail=`SELF_ATTESTED_TQAEP_NACK`；Consumer=SBL-hosted PIPD Reader; missing original final receiver HOLD；Case=`AUTHOR.W1.INT-13.04.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-13-05`：Input=原上游截斷的 Receiver 不得自行補名；POS=原 Domain Reader 同 Subject ACK 才填端點；NEG=把 Original Domai 視為完整 Receiver；FirstFail=`RECEIVER_IDENTITY_HOLD`；Consumer=SBL-hosted PIPD Reader; missing original final receiver HOLD；Case=`AUTHOR.W1.INT-13.05.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-023-01`：Input=每 family 有原 byte SHA+至少一個 contained locator；POS=有合法 AuthorityBinding／Source manifest；NEG=Source metadata approved 冒原 SourceFreeze；FirstFail=`SOURCE_FREEZE_APPROVAL_SPOOF`；Consumer=Original PIPD Authority/Source Reader；Case=`AUTHOR.W1.FHS-DR-023.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-023-02`：Input=Conflict/currentness unresolved 時只擋受影 compile；POS=原 Reader 回應 conflict_none；NEG=沒核衝突就 promotion Canonical；FirstFail=`SOURCE_AUTHORITY_CONFLICT_HOLD`；Consumer=Original PIPD Authority/Source Reader；Case=`AUTHOR.W1.FHS-DR-023.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-024-01`：Input=PI 每 OriginalID 保留 Parent/NEG/ClauseSHA/Oracle/FUO；POS=每 applicable 原字節 span 可重算；NEG=丟掉父句否定但保留 OriginalID；FirstFail=`PIPD_PI_NEG_PARENT_LOSS`；Consumer=SBL-hosted original PI Writer；Case=`AUTHOR.W1.FHS-DR-024.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-024-02`：Input=Canonical PI 只能原 Writer 實編譯；POS=原 compile-pi Reader body+ACK；NEG=GPT 生成 JSON 假裝已編譯；FirstFail=`PIPD_FAKE_COMPILER_RECEIPT`；Consumer=SBL-hosted original PI Writer；Case=`AUTHOR.W1.FHS-DR-024.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。

<a id="ch-14"></a>

# CH-14｜PD-01..10、RepoContext Currentness、Scope 與晚綁

### r2 受影修補（2026-11-05｜AUTHOR_FINAL_AFFECTED_REPAIR）

**受影 Finding**：`N-02`。**原位差額**：PD 晚綁的前提是真 local RepoContext；r2 四庫探針顯示皆在候選分支且 dirty，故遠端 HEAD 不得作 local RepoContext，`bind-pd` 維持 `EXECUTOR_UNBOUND`。

**未變更**：本章 H1 標題、L1 span／section SHA、OriginalID／Parent／NEG 與原 Reader 法位皆不變；原域 Raw 未取得者維持 `EXPECTED_NOT_OBSERVED`，不以作者推斷補值。

**下一個 Reader**：SBL Repo/PD Reader；FirstFail 見本章 POS／NEG／SEC 卡與 `AFFECTED_FINDINGS.jsonl` 對應列。

## W1 草案當期完成契約｜CH-14（DRAFT-W1-CH14）

**使用者可得結果**：真 RepoContext 的 late-bound PD；合法執行範圍限 `SOURCE_READ` 與作者端規格審閱，無真 Host 准入或新 Writer 權限。

| 受影型別 | 本章可驗證的確定規則 |
|---|---|
| Input／觸發 | 原 PI hash、Git root/HEAD/branch/index/untracked/preimages/ACL/WriteSet、Scope；強制 `subject_id/source_manifest_sha/scope` 來源釘選 |
| 操作／Producer | 從真本地 Original Repo probe 取得上下文；任何遠端 HEAD 僅可做導航；PD 綁定來源穩定 PI 與當下寫集，一份 PD 僅對一 Scope；漂移則局部重探；Producer＝W1 DraftMaker（僅文字/Sidecar），正式效果由原域 Producer 執行 |
| Output／交付 | RepoBindingRequest；只有原 Writer/Reader 准入後才產 PD-PKG；所有未觀測 Reader Raw 留空並具名 `EXPECTED_NOT_OBSERVED` |
| Original Reader | SBL original RepoContext/PD Reader；原 Writer／Issuer／Checker 不因本稿改權 |
| Downstream Consumer | W2 Original DEV ECP/World Readback；綁同 Subject／Scope，需 Original ACK 才可升級 |
| POS／Expected Raw | 一致 HEAD＋Scope＋實在 Preimage 時允許候選進原 Reader；預期由原 Consumer 返回原格式 Raw（本輪 `NOT_RUN`） |
| NEG／首拒收 | 拿 GitHub SHA 冒本地 Git HEAD 或使用目錄當活 Repo；FirstFail=`PD_REPOCONTEXT_UNBOUND` |
| EDGE | dirty/untracked 構成精確局部失效，無需重跑三 SPEC；只 PARK 受影 scope，合法 READ/DRAFT 不受波及 |
| SEC | 越出 write scope 的相對/絕對/UNC path；缺憑證、Owner、ACL 或 Checker 證物拒效果 |
| Stop／Resume／Rollback | 遇 `PD_REPOCONTEXT_UNBOUND` 記 `hold_id+original_reader+required_raw`，停止受影寫入；Resume 需同 SourceSHA/Scope 的原 Reader 結果；READ 丟棄快照、DRAFT 刪除隔離候選；世界效果不在 W1 自行 rollback |
| Cross-wave | W2 WP06；交 `AUTHOR.FHS.W1ToW{next}@design` typed envelope，禁止偽裝 WorkOrder |

**受影源句拆義**：`actor/trigger/action/object`（見 Input/操作）；`condition/exception`（見 EDGE）；`prohibition`（見 NEG/SEC）；`outcome/consumer`（見 Output/Original Reader）；`POS/NEG/FirstFail` 必綁同一原 RequirementID。來源的原始句、Span、SHA、Parent/Child/NEG 以 r5 本章及附錄 `obligation_registry.jsonl` 回指；缺具體原 Reader 即 `ORIGINAL_OWNER_HOLD`，不自行創造簽核。


### R5 本章受影精確契約／業務負例（整合 r4，非歷史附錄）

PD 原 late binding 必 live Git root/HEAD/branch/dirty/index/untracked/preimage/WriteSet/ACL，僅 git remote HEAD 不能認有權 RepoContext；NEG=GitHub main SHA 當本機已 probe → `PD_REPOCONTEXT_UNBOUND`；drift 時只重綁受影 PD/ECP 而非更改穩定 PI。


**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L1449–1520`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original PD / RepoContext Reader；L2-r4:L904。原 Domain Reader/Writer 不因本章轉移。

## r4 當期受影修補（直接摘取 L1 r4 本章有效增量）

## r4｜AUDIT r3 受影整合／覆蓋／取代（現行作者端規範）

**Original RepoContext Late Binding（GJ02/DR025/DR048）**：Repo 必有當期 root/HEAD/branch/index/dirty/untracked、ACL、Exact WriteSet、Preimage SHA、Subject+SourceSHA+CandidateSHA；只有原 PIPD PD Writer 綁定後才能提供非草稿 PD。若 repo 未觀察→`PD_REPOCONTEXT_UNBOUND`；字串路徑、GitHub remote HEAD 或上一輪 output 不是 live Repo。變更越界、Stale 預圖必拒；原域 PR/AGENTS 規範由各 Repo Owner 決定，本文不寫任何 main。

## r4 對齊之 W1 主波操作規格、草案必填欄、逐項 POS/NEG／FirstFail（高保留整合）

**Protected Original H1 / CURRENT L1-r4**：`FHS_PIPD-LS-PKG_藍圖_2026-11-04_r4_HIGH_RETENTION_AUDIT_REPAIRED_實質正文(1).md:L1449–L1520`；`source_file_sha256=cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`；`section_sha256=0fb7ffa88651ba28d26bd0cbc08e0b3b95d2ab28753bca3c961704ef736f6558`；`heading_exact=# CH-14｜PD-01..10、RepoContext Currentness、Scope 與晚綁`；**HISTORICAL_LOCATOR_NOT_EFFECTIVE**=`L1:1011–1060` / `L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`，L2 作者端路由 `L2:652`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W1 不取得原 Writer。

## A. 本章實質功能與不能壓平的原義

真 Git RepoContext 晚綁 PD-01..10，原範圍/HEAD/index/untracked/ACL/preimage 足夠才可接。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。

## B. 來源 r5 skeleton 必填核對欄（已由上方 W1 草案當期完成契約受影回填）

| 必填欄 | 欄位設計／不可空條件 |
|---|---|
<!-- HISTORICAL_R5_SKELETON_FILL_REQUEST_SUPERSEDED: transition wording only; all substantive constraints retained -->
| `chapter_id` / `primary_wave` / `author_writer` | `CH-14` / `W1` / `W1:DraftMaker`（歷史 r5 階段欄；當期為作者端定案候選） |
| `original_sources[]` | 本章 L1 行與下面原冊 SHA／OriginalClause Span；不得用語義假定的 ID 補空缺 |
| `same_subject` / `candidate_sha` / `source_manifest_sha` / `affected_scope` | 必攜相同 Subject/Scope，未原 Reader 認證則 `AUTHOR_CANDIDATE` |
| `effect_class` / `original_owner` / `consumer_abi` / `schema_version` | 依 Operation Reader；缺 `$id` 或 Receiver 不自造 |
| `input` / `typed_output` / `fuo` / `non_goals` | 應有真使用者結果與 Receiver（非檔案數） |
| `positive_fixture` / `negative_fixture` / `security_fixture` | 原 Source Case/Oracle 逐受影引用，未有 Runner/Raw 就 `EXPECTED_NOT_OBSERVED` |
| `first_fail` / `hold` / `stop_scope` / `resume_predicate` | 明確停止受影子圖，不全域凍結 READ／DRAFT |
| `rollback` / `w2_handoff` / `original_ack_nack` | 回退路由與 same scope 的預期接收；不得填假 PASS |

## C. Input → Producer → 原 Reader／Consumer → Output

- **Input/Guard**：live repo_root/HEAD/branch/dirty/index/untracked、allowlisted WriteSet/Scope/Reader ABI。
- **Producer**：該 Original Domain 的 Reader/Compiler/Host/Guide 依本章功能生產；W1 Curator 僅記設計；**Original Consumer**：原 PD binder、Repo Owner/Consumer。
- **Typed Output/FUO**：原 PD-PKG 或 `RepoBindingRequest`；Developer ECP 不先授權。
- **版本要求**：至少 `Subject,CandidateSHA,SourceSHA,OriginalID+SourceSpan,Scope,Host/PolicyEpoch（受影才填）,ABI $id/version,OriginalReader,OutputRawExpected`，少一欄只停需該欄的出口。

## D. POS／NEG／FirstFail／HOLD／退出

- **POS（期待）**：原 repo probe 與傳入 HEAD 相同、path contained、preimage fresh。
- **NEG／SEC（期待拒收）**：remote SHA 冒 local HEAD、`../` 寫入、scope widening。
- **FirstFail**：`REPO_CONTEXT_STALE_OR_ESCAPE`；禁止只有泛稱 `VALIDATION_FAILED` 而不給首次失敗位置。
- **HOLD/Owner**：`REPO_HEAD_BIND_HOLD`。需同 Subject/Scope/Host/原 Reader 的真 Raw/ACK 解除；本輪 `NOT_RUN`。
- **Stop/Resume**：保留原 SourceSHA/受影 Reader/cursor/last-good；READ/DRAFT 合法部分繼續；UNKNOWN 必原 Reader reconcile。
- **Rollback**：只回復該 Need/Host 的原 last-good，Host/OPS 效果走原 inverse；不得以檔案 ZIP 作回復收據。

## E. 來源追溯、波次邊界與下一手

| 源鍵／檔案 | 原文 SHA | 此 W1 處理方式 |
|---|---|---|
| SBL-DOC-05 | 3b47a0b6224b1984a4047cf53aac5ac50615c93a560fea46e1b43d079a5d9f27 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| SBL-DOC-02 | 4ff0cda5ab00ba5f577151e5b004d2167d933e912e302c9e3529b237ccb9e035 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-03 | 58628861e63956ae31b1ac17404c093533226688f975f5fa11b9b82adecd1284 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
W0 提供原 Source/三 SPEC/索引；本 `CH-14` 不修改 W0 成果。W1 WaveCurator 交 W1 DraftMaker 按原 Reader 定位填入真 Requirements；W2 僅領同 Subject/Scope 的需要的 Effect/Case/HOLD，不得借 W3/W4 收據。原 L1 CH-14 的詳細原義仍在 L1 主體，不移作本冊第二 Canonical。

## F. r2 原位修補：CH-14 可直接交接的受影實質規格（非證據附錄）

**本章不可壓平功能**：real RepoContext and late-bound PD。與 W0 三份獨立 SPEC 維持同 SourceSHA/Subject/Scope；將原讀者真接收的 **Output／Consumer** 優先於填滿文件欄位。依 L1 原 CH 身份與 L2 W1 主責修訂，不移轉原 Writer。

### F.1 原句→原 Consumer→本章測例的逐子義槽（已從原物理檔定位）

- **`SCL-W1-0031`** `[SOURCE:SBL-DOC-05:L917:sha256=3b47a0b6224b1984]`：原文實質片段「**Native output 對照**：PD-PKG@1 的 subject_id,content_hash,version,schema_version,RepoContext{root,head,tracked_files},currentness,late_bound_construction_binding{bound_at:'PD',binding_scope:'affected_only',writab」；Parent=`L896:### R02.1.B｜歷史 r2 實質協議：SBL ABI 與 P4 JSON Schema 雙向轉譯`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=PIPD original RepoContext PD Binder；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH14.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0032`** `[SOURCE:SBL-DOC-05:L2803:sha256=3b47a0b6224b1984]`：原文實質片段「/ METHOD-06 / OpenSpec / SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L808; SBL r2 §9D L3015 / CANDIDATE_TRANSLATE (not installed claim) / OS-01/02/03/04 / Frozen RepoContext+desired change / ChangeDraft→SpecDelta→b」；Parent=`L2759:### R07.5.A｜25 個方法唯一身分、分域 Owner、別名與選用法位（F07/F20）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=PIPD original RepoContext PD Binder；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH14.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0033`** `[SOURCE:SBL-DOC-05:L7798:sha256=3b47a0b6224b1984]`：原文實質片段「**GJ-D05-01 合法 Repo 晚綁定。** 入口為 ProductKind=CLI_TOOL、Mode=STANDALONE、已凍結 PIRef 與合法真 Repo root/head/tracked_files；步驟：① ReaderRoute 校驗 SourceInventory hash；② PIPD SourceFreeze 不缺且衝突已裁決時始能進入；③ Repo Owner 做 read-onl」；Parent=`L7796:## R11.8｜兩條可交付 Golden Journeys（設計向量，非執行紀錄）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG,不能`。本章觸發/Consumer=PIPD original RepoContext PD Binder；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH14.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0034`** `[SOURCE:SBL-DOC-02:L6250:sha256=4ff0cda5ab00ba5f]`：原文實質片段「**本節唯一拒收路徑與安全反證**：若「allow binding to assumed repository」，先以 REPO_CONTEXT_MISSING NACK；必驗 expected.output 的欄位語義，而非只比「SUCCESS」字串。**本節 EDGE**：「RepoContext STALE observed; do not launder to FRESH for late binding」→」；Parent=`L6238:## R02-07.2｜P4 native skill gating`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=PIPD original RepoContext PD Binder；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH14.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0035`** `[SOURCE:SBL-DOC-02:L9861:sha256=4ff0cda5ab00ba5f]`：原文實質片段「/ SLOT-OS-03 OS-03: apply only legal write paths then verify / OpenSpec / OpenSpec / GOVERNED_REPO_WRITE / NATIVE_ECP_REPO_WRITE（token+head+Scope SoD/at-most-once） / ChangeSet+ApplyReadback / POS: input GOVERNE」；Parent=`L9855:### 24 CapabilitySlot｜每槽不同功能結果、失敗、Host gate`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=PIPD original RepoContext PD Binder；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH14.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0036`** `[SOURCE:SBL-DOC-02:L10770:sha256=4ff0cda5ab00ba5f]`：原文實質片段「/ DEC-012 / Q04.c / c. PI→PD 的真 RepoContext/HEAD/Scope/Freshness 與 no-zero-atom first-fail 由哪個原生工具證明？ / SBL_PIPD-LS-PKG_整合校正10問_回答(5).md:L1258 / C17/R02-07 / PIPD Native Owner / DESIGN_CANDIDATE_OWNER_RATIFICAT」；Parent=`L10755:## 十問／三十個子裁決逐項正文路由（設計提案，不代正式 Owner 批示）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=PIPD original RepoContext PD Binder；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH14.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0037`** `[SOURCE:FHS-BODY-03:L37:sha256=58628861e63956ae]`：原文實質片段「**來源證據界線**：GitHub commit/檔案 blob SHA 不是 Windows process PID、loaded hash、Owner grant、Issuer Permit 或 Native Runner 調用；本輪已保存 local HEAD/index/untracked 原始輸出；只對實測工作樹作判斷。所有 Repo patch 須有現役 Owner 的 exact WriteSet/DE」；Parent=`L28:## 四庫 2026-10-30 `main` 原始碼錨定（GitHub 唯讀）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不能`。本章觸發/Consumer=PIPD original RepoContext PD Binder；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH14.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0038`** `[SOURCE:FHS-BODY-03:L50:sha256=58628861e63956ae]`：原文實質片段「/ PI→PD / PI原 Writer + Local RepoProbe / real worktree root, head, dirty, exact write scope / PIPD 原 PD Binder / late binding / assumed GitHub head/** glob /」；Parent=`L44:## R2 Receiver-to-Producer、實效及授權型別（不取代原 ABI）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=PIPD original RepoContext PD Binder；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH14.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0039`** `[SOURCE:FHS-BODY-03:L69:sha256=58628861e63956ae]`：原文實質片段「/ REPO_WRITE / L2 / DEV ECP + exact WriteSet + 原 HGK admission / pre/post HEAD/diff/test/raw/受影 residue / 原 preimage inverse patch；HEAD 漂移先停，不能 reset 他人變更 /」；Parent=`L63:## R2-03-EFFECT：效果與退出按類處理`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不能`。本章觸發/Consumer=PIPD original RepoContext PD Binder；承接 `WP 05`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH14.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。

### F.2 本章 WP 與 Producer／typed I/O／FirstFail（每項獨立）

- **WP-FHS-05**：Producer=SBL-hosted original PIPD Compiler/Reader；Input=三份不同 SPECDraft、原 SourceManifest/Authority/Profile safety veto、原 PIPD Writer version；Output=非空 strict PI，真 RepoContext 才有 PD，DEV/OPS EffectIntent 分開，PlannedTQAEP 不冒 Checker；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=PIPD Native Compiler 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=把 _profile_meta 側掛塞進 strict PI；或憑 Caller HEAD 虛構本機 Repo binding；EDGE=PI SourceSHA 不變而 RepoHEAD 改變，只使 PD/ECP stale；不可偷重寫 PI requirement 原義；FirstFail=`PIPD_STRICT_SCHEMA_OR_SOURCE_NACK`；rollback=隔離候選刪除/回復 preimage；SourceSHA/HEAD 變更僅重編受影 PD/ECP。

### F.3 複合原義拆解、反向閉包與受影退出

- **「各有」**：本 CH 的每個原 clause locator 各自保留 SourceSHA/Parent/OriginalConsumer、POS/NEG；若原文有多個 named roles/Host/Case，不可用單一結果冒全數。
- **「分別」**：strict JSON body／@2 sidecar、Original Policy Active／Host Loaded、Maker challenge／Protected Checker、Selected／ActualServed 是不同欄位與收據，不得合併。
- **「對應」**：必 `original source line → SCL-W1 id → CH → W1 WP → expected Case → original source line` 可機械重算；原 OriginalID 未明者只引用明示的 SourceSpan，不可猜 ID。
- **「不得／若／除非」**：否定作用域保留到原 Parent context；本章只標作者候選，原 Source Reader 取得 ACK 才能宣告原語義接受。
- **退出**：原 Reader NACK 僅 PARK 本章受影的 PI/PD/DEV/OPS/Host operation；合法 SOURCE_READ、隔離草稿及不依賴該 ABI 的 W0/W2 工作照原許可前進。

## 本章 L2-r4 設計義務接收卡（逐 ID；不可省略原 NEG）

- `INT-13` (`L1-r4:L781`, `L2-r4:L327`)：PIPD PI/PD/ECP/TQAEP 分層；PI source-bound，PD 晚綁 Repo，ECP 非 Admission，TQAEP 依 Original Oracle；[CH-12](#ch-12)/[CH-13](#ch-13)/[CH-14](#ch-14)/[CH-15](#ch-15)/[CH-41](#ch-41)；POS `PI source-bound，PD 晚綁 Repo，ECP 非 Admission，TQAEP 依 Original Oracle`；NEG/FirstFail `ECP intent 冒 Issuer Permit；PD 未 live RepoContext 即號稱已綁；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `SBL RepoContext/PD Reader → HGK Original Issuer → Repo World Reader、SBL-hosted PIPD canonical Compiler/Original Source/Repo/Case Reader；原末端 Receiver＝`INT-13_CONSUMER_LOCATOR_SOURCE_TRUNCATION_HOLD`（L1/L2 源列被截斷，非已綁定）`；本輪只有 EXPECTED_NOT_OBSERVED。
- `FHS-DR-025` (`L1-r4:L822`, `L2-r4:L363`)：PIPD/TPM／A/W0-B；PD 是來源穩定 PI 對真 RepoContext 的 late binding；Repo HEAD/index/untracked/Preimage/WriteSet 與 Scope；[CH-14](#ch-14)；POS `Repo drift 只重綁受影部分`；NEG/FirstFail `未知 Repo 強行出有權 PD；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `SBL-hosted PIPD canonical Compiler/Original Source/Repo/Case Reader`；本輪只有 EXPECTED_NOT_OBSERVED。
- `FHS-DR-034` (`L1-r4:L831`, `L2-r4:L372`)：治理／A；三庫更改各自 branch→PR/verified original HEAD；不可跨 Repo 一個隱形 Commit；[CH-14](#ch-14)/[CH-44](#ch-44)；POS `相應 PR 有真變更與可回退提交`；NEG/FirstFail `憑本檔直接覆寫 main/force push；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `Original Domain Owner/Reader (scope binding pending)`；本輪只有 EXPECTED_NOT_OBSERVED。

## CH-14 專屬退出與回退

DraftMaker 後續須填 `original_reader_ref`, `original_schema_version_or_HOLD`, `source_span_sha`, `same_subject_and_scope`, `Case/Oracle`, `positive_raw_expected`, `negative_raw_expected`, `first_fail`, `resume_predicate`, `last_good`, `consumer_ack_or_HOLD`。`DOC_AUTHOR_DONE` 是本檔可檢索，不是 `PD-01..10、RepoContext Currentness、Scope 與晚綁` 已原 Host Qualified。若權限／能力尚缺，只 PARK 受影操作；回退到該 Domain 上次有效 Reader/Host 版本、保留跨波合法 READ/DRAFT，且不得刪原 NEG 或憑此文件自簽。



## AUTHOR-FINAL｜CH-14 受影交付契約

**Input / Operation / Output**：保留本章原有專屬 I/O、原句與 NEG；以當期 Registry 對同 SourceSHA/Subject/Scope 重算受影子圖，輸出 CH-14 的原 Reader BindingRequest，實質輸出與業務 FirstFail 以本章上文專屬契約及下列子義為準。

**Original Reader / Original Consumer**：Original local Git RepoContext/PD Reader；原 Consumer Raw=EXPECTED_NOT_OBSERVED。L1 起始 1449、終止 1520，section SHA `0fb7ffa88651ba28d26bd0cbc08e0b3b95d2ab28753bca3c961704ef736f6558`。

**POS / NEG / FirstFail**：本章專屬正負條件逐筆如下；沒有適用子義的跨 ABI 章以原本章完整 POS/NEG 為準，不從別章借用 PASS。**EDGE**：SourceSHA/Host/PolicyEpoch 其中一欄改變，只 invalidate 受影接線；**SEC**：Maker 假 ACK 或跨 Principal 原回條均拒收。**ExpectedRaw**：同 Subject/Candidate/Scope 原 Consumer/World bytes；本輪 NOT_RUN。**Stop**：缺該 Effect 必需原 Reader 即 PARK 其效果；**Resume**：同 Scope 原 Reader 提供具名 Raw；**NextWave**：W2 原 Effect Receiver，四 Host/Cell/W18 交 W3，CI/Publisher 交 W4。

- `S-W1-INT-13-01`：Input=PI 綁 Original Source／Parent／NEG／OriginalID；POS=原 Compiler 確認非空 strict PI；NEG=用 GPT 產 JSON 冒 Canonical PI；FirstFail=`PIPD_STRICT_PI_WRITER_NACK`；Consumer=SBL-hosted PIPD Reader; missing original final receiver HOLD；Case=`AUTHOR.W1.INT-13.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-13-02`：Input=PD 僅綁同 Scope 真 local RepoContext；POS=本地 HEAD/index/untracked/preimage 俱全；NEG=remote GitHub HEAD 充 local probe；FirstFail=`PD_REPOCONTEXT_UNBOUND`；Consumer=SBL-hosted PIPD Reader; missing original final receiver HOLD；Case=`AUTHOR.W1.INT-13.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-13-03`：Input=ECP intention≠Issuer Permit；POS=原 HGK admission 出具同 scope nonce/epoch；NEG=直接以 ECP intention 做世界效果；FirstFail=`ECP_NOT_ISSUER_PERMIT`；Consumer=SBL-hosted PIPD Reader; missing original final receiver HOLD；Case=`AUTHOR.W1.INT-13.03.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-13-04`：Input=TQAEP 必連 Original Oracle/Runner/Checker；POS=具名 Case 和原 Reader 對應；NEG=Maker 自簽原 Checker verdict；FirstFail=`SELF_ATTESTED_TQAEP_NACK`；Consumer=SBL-hosted PIPD Reader; missing original final receiver HOLD；Case=`AUTHOR.W1.INT-13.04.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-13-05`：Input=原上游截斷的 Receiver 不得自行補名；POS=原 Domain Reader 同 Subject ACK 才填端點；NEG=把 Original Domai 視為完整 Receiver；FirstFail=`RECEIVER_IDENTITY_HOLD`；Consumer=SBL-hosted PIPD Reader; missing original final receiver HOLD；Case=`AUTHOR.W1.INT-13.05.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-025-01`：Input=PD late bind 本地 root/HEAD/dirty/index/untracked/preimages；POS=live RepoProbe 與 Scope 精確匹配；NEG=remote HEAD 冒 local RepoContext；FirstFail=`PD_REPOCONTEXT_UNBOUND`；Consumer=SBL original PD/RepoContext Reader；Case=`AUTHOR.W1.FHS-DR-025.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-025-02`：Input=Repo drift 只對受影 bindings 重綁；POS=Source-stable PI 不被任意重寫；NEG=HEAD 漂移直接繼承 stale PD；FirstFail=`PD_STALE_PREIMAGE_NACK`；Consumer=SBL original PD/RepoContext Reader；Case=`AUTHOR.W1.FHS-DR-025.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-034-01`：Input=Fabric/SBL/HGK 各有獨立 branch/PR；POS=三庫各自可追 pre/post HEAD；NEG=作者草案直接改 main；FirstFail=`REPO_MAIN_DIRECT_WRITE_DENY`；Consumer=Each original Repo Owner/Reader (primary W0)；Case=`AUTHOR.W1.FHS-DR-034.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-034-02`：Input=原 repo preimage/rollback 不能跨庫借用；POS=每庫本地 Git Scope 自證；NEG=以 SBL commit 自稱 HGK 已修改；FirstFail=`CROSS_REPO_HEAD_MISMATCH`；Consumer=Each original Repo Owner/Reader (primary W0)；Case=`AUTHOR.W1.FHS-DR-034.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。

<a id="ch-15"></a>

# CH-15｜ConstructionContract／ECP：DEV、OPS、USER、RELEASE 不混用

**唯一主波** `W2`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L1521–1615`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original ECP Writer / HGK effect receiver；L2-r4:L905。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W2 Normative 主責）

W1 只交原受影 Effect/Repo/Host/Reader request，世界效果、TQAEP 真 Raw 與 FirstFail 由 W2 在原准入後驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W2 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L1521–1615` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-15 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-15",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W2",
  "OriginalReader": "Original ECP Writer / HGK effect receiver；L2-r4:L905",
  "consumer": "Original ECP Writer / HGK effect receiver；L2-r4:L905",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-15",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 1521,
    "end": 1615
  }
}
```

<a id="ch-16"></a>

# CH-16｜跨庫 Typed ABI、Producer→Consumer、Same Subject 交接

### r2 受影修補（2026-11-05｜AUTHOR_FINAL_AFFECTED_REPAIR）

**受影 Finding**：`F-09、N-07`。**原位差額**：四個跨波 Envelope 重綁 r2 candidate SHA，`original_reader_ack` 仍為 `EXPECTED_NOT_OBSERVED`、`policy_epoch=POLICY_EPOCH_UNBOUND`；不得自造 ACK 或以 W0 WorkID 當 W1 Subject。

**未變更**：本章 H1 標題、L1 span／section SHA、OriginalID／Parent／NEG 與原 Reader 法位皆不變；原域 Raw 未取得者維持 `EXPECTED_NOT_OBSERVED`，不以作者推斷補值。

**下一個 Reader**：Original W2/W3/W4 Receivers；FirstFail 見本章 POS／NEG／SEC 卡與 `AFFECTED_FINDINGS.jsonl` 對應列。

## W1 草案當期完成契約｜CH-16（DRAFT-W1-CH16）

**使用者可得結果**：Typed cross-repo ABI / S1–S5；合法執行範圍限 `LOCAL_DRAFT_WRITE` 與作者端規格審閱，無真 Host 准入或新 Writer 權限。

| 受影型別 | 本章可驗證的確定規則 |
|---|---|
| Input／觸發 | 同 Subject/Candidate/SourceSHA/Scope + 送端/受端 versioned ABI；強制 `subject_id/source_manifest_sha/scope` 來源釘選 |
| 操作／Producer | 逐 Seam 不共用幾個泛化欄位：S1 Product→PIPD，S2 PIPD→PLAN，S3 Fabric Policy→HGK，S4 HGK→Hermes，S5 Challenge→Protected Checker/Publisher；拆 Trigger/ACK/NACK/Raw；Producer＝W1 DraftMaker（僅文字/Sidecar），正式效果由原域 Producer 執行 |
| Output／交付 | 每 Seam 的最小 request/response、idempotency/FirstFail/Owner；所有未觀測 Reader Raw 留空並具名 `EXPECTED_NOT_OBSERVED` |
| Original Reader | 各 Original Domain ABI Reader，非 Fabric Mirror；原 Writer／Issuer／Checker 不因本稿改權 |
| Downstream Consumer | W2 Active Receiver、W4 Independent acceptance；綁同 Subject／Scope，需 Original ACK 才可升級 |
| POS／Expected Raw | 相同 Subject/Scope/PolicyEpoch 正向接收並保留原身份；預期由原 Consumer 返回原格式 Raw（本輪 `NOT_RUN`） |
| NEG／首拒收 | 同名不同義或跨 Principal 兜售偽 ACK；FirstFail=`SEAM_SUBJECT_OR_ABI_NACK` |
| EDGE | 一條 Seam 未核僅阻依賴它的 effect；只 PARK 受影 scope，合法 READ/DRAFT 不受波及 |
| SEC | 作者端 signature 和原 Issuer 簽名混用；缺憑證、Owner、ACL 或 Checker 證物拒效果 |
| Stop／Resume／Rollback | 遇 `SEAM_SUBJECT_OR_ABI_NACK` 記 `hold_id+original_reader+required_raw`，停止受影寫入；Resume 需同 SourceSHA/Scope 的原 Reader 結果；READ 丟棄快照、DRAFT 刪除隔離候選；世界效果不在 W1 自行 rollback |
| Cross-wave | W2 S1–S4，W4 S5；交 `AUTHOR.FHS.W1ToW{next}@design` typed envelope，禁止偽裝 WorkOrder |

**受影源句拆義**：`actor/trigger/action/object`（見 Input/操作）；`condition/exception`（見 EDGE）；`prohibition`（見 NEG/SEC）；`outcome/consumer`（見 Output/Original Reader）；`POS/NEG/FirstFail` 必綁同一原 RequirementID。來源的原始句、Span、SHA、Parent/Child/NEG 以 r5 本章及附錄 `obligation_registry.jsonl` 回指；缺具體原 Reader 即 `ORIGINAL_OWNER_HOLD`，不自行創造簽核。


### R5 本章受影精確契約／業務負例（整合 r4，非歷史附錄）

`INT-13` 在 L1/L2-r4 的最後 Original Receiver 真的被截斷 `Original Domai`；本章僅承認已可定位的 PIPD/Repo/HGK 前段，後段 `RECEIVER_IDENTITY_HOLD`。正式 Receiver 身分、ABI `$id/version` 必回原 PIPD/Domain Reader 同 Subject/Scope ACK，並提交上位 L1/L2 作者端受影修補。NEG=猜測補完原 Reader 名稱而宣 Valid → NACK。


**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L1616–1680`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original ABI Consumer；L2-r4:L906。原 Domain Reader/Writer 不因本章轉移。

## r4 當期原 Reader 鎖與非降級本體

本章 L1-r4 依以上真實行區間及原域 Reader；無單獨 R4-BEGIN 增量不等於以歷史 r2 取代 L1。W1 契約下文僅是對該 L1 已定義原義的工程操作化。

## r4 對齊之 W1 主波操作規格、草案必填欄、逐項 POS/NEG／FirstFail（高保留整合）

**Protected Original H1 / CURRENT L1-r4**：`FHS_PIPD-LS-PKG_藍圖_2026-11-04_r4_HIGH_RETENTION_AUDIT_REPAIRED_實質正文(1).md:L1616–L1680`；`source_file_sha256=cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`；`section_sha256=1e717d56998665286e028c9ea3ad32aeabe01bfe9dda1a69e1f61ba36e058862`；`heading_exact=# CH-16｜跨庫 Typed ABI、Producer→Consumer、Same Subject 交接`；**HISTORICAL_LOCATOR_NOT_EFFECTIVE**=`L1:1121–1171` / `L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`，L2 作者端路由 `L2:654`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W1 不取得原 Writer。

## A. 本章實質功能與不能壓平的原義

五 Seam 以原 schema/version/Subject/Candidate/Scope/SourceSHA/Effect/Reader 作 typed 連接。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。

## B. 來源 r5 skeleton 必填核對欄（已由上方 W1 草案當期完成契約受影回填）

| 必填欄 | 欄位設計／不可空條件 |
|---|---|
<!-- HISTORICAL_R5_SKELETON_FILL_REQUEST_SUPERSEDED: transition wording only; all substantive constraints retained -->
| `chapter_id` / `primary_wave` / `author_writer` | `CH-16` / `W1` / `W1:DraftMaker`（歷史 r5 階段欄；當期為作者端定案候選） |
| `original_sources[]` | 本章 L1 行與下面原冊 SHA／OriginalClause Span；不得用語義假定的 ID 補空缺 |
| `same_subject` / `candidate_sha` / `source_manifest_sha` / `affected_scope` | 必攜相同 Subject/Scope，未原 Reader 認證則 `AUTHOR_CANDIDATE` |
| `effect_class` / `original_owner` / `consumer_abi` / `schema_version` | 依 Operation Reader；缺 `$id` 或 Receiver 不自造 |
| `input` / `typed_output` / `fuo` / `non_goals` | 應有真使用者結果與 Receiver（非檔案數） |
| `positive_fixture` / `negative_fixture` / `security_fixture` | 原 Source Case/Oracle 逐受影引用，未有 Runner/Raw 就 `EXPECTED_NOT_OBSERVED` |
| `first_fail` / `hold` / `stop_scope` / `resume_predicate` | 明確停止受影子圖，不全域凍結 READ／DRAFT |
| `rollback` / `w2_handoff` / `original_ack_nack` | 回退路由與 same scope 的預期接收；不得填假 PASS |

## C. Input → Producer → 原 Reader／Consumer → Output

- **Input/Guard**：W0 S1 payload + 每 Seam Receiver ABI/version/Reader capability。
- **Producer**：該 Original Domain 的 Reader/Compiler/Host/Guide 依本章功能生產；W1 Curator 僅記設計；**Original Consumer**：SBL PIPD、Fabric、HGK、Hermes、原 Case/Checker 不同 Consumer。
- **Typed Output/FUO**：各 Seam ACK/NACK、original receiver name、first_fail，cross repo split PR proposal。
- **版本要求**：至少 `Subject,CandidateSHA,SourceSHA,OriginalID+SourceSpan,Scope,Host/PolicyEpoch（受影才填）,ABI $id/version,OriginalReader,OutputRawExpected`，少一欄只停需該欄的出口。

## D. POS／NEG／FirstFail／HOLD／退出

- **POS（期待）**：同 Candidate 和 Scope 的原 Consumer 回顯或原 typed NACK。
- **NEG／SEC（期待拒收）**：共享 ChangeSetID 當 WorkID／跨 Subject 套 receipt。
- **FirstFail**：`ABI_JOIN_MISMATCH`；禁止只有泛稱 `VALIDATION_FAILED` 而不給首次失敗位置。
- **HOLD/Owner**：`ORIGINAL_ABI_CONSUMER_UNBOUND`。需同 Subject/Scope/Host/原 Reader 的真 Raw/ACK 解除；本輪 `NOT_RUN`。
- **Stop/Resume**：保留原 SourceSHA/受影 Reader/cursor/last-good；READ/DRAFT 合法部分繼續；UNKNOWN 必原 Reader reconcile。
- **Rollback**：只回復該 Need/Host 的原 last-good，Host/OPS 效果走原 inverse；不得以檔案 ZIP 作回復收據。

## E. 來源追溯、波次邊界與下一手

| 源鍵／檔案 | 原文 SHA | 此 W1 處理方式 |
|---|---|---|
| SBL-DOC-04 | ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| SBL-DOC-05 | 3b47a0b6224b1984a4047cf53aac5ac50615c93a560fea46e1b43d079a5d9f27 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-03 | 58628861e63956ae31b1ac17404c093533226688f975f5fa11b9b82adecd1284 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
W0 提供原 Source/三 SPEC/索引；本 `CH-16` 不修改 W0 成果。W1 WaveCurator 交 W1 DraftMaker 按原 Reader 定位填入真 Requirements；W2 僅領同 Subject/Scope 的需要的 Effect/Case/HOLD，不得借 W3/W4 收據。原 L1 CH-16 的詳細原義仍在 L1 主體，不移作本冊第二 Canonical。

## F. r2 原位修補：CH-16 可直接交接的受影實質規格（非證據附錄）

**本章不可壓平功能**：five original typed Seam identity。與 W0 三份獨立 SPEC 維持同 SourceSHA/Subject/Scope；將原讀者真接收的 **Output／Consumer** 優先於填滿文件欄位。依 L1 原 CH 身份與 L2 W1 主責修訂，不移轉原 Writer。

### F.1 原句→原 Consumer→本章測例的逐子義槽（已從原物理檔定位）

- **`SCL-W1-0040`** `[SOURCE:SBL-DOC-04:L426:sha256=ee90cb1c86f6f735]`：原文實質片段「統一 SBLProposalEnvelope@0.4 必填 contract_id,contract_version,subject_sha256,source_refs,producer_principal,mode,correlation_id,input_sha256；版本不等或 additionalProperties 越界回 ABI_SCHEMA_MISMATCH。下表是每張卡的 **專屬 Payload*」；Parent=`L424:### C12.4.11｜十張卡的具型別資料與異質函數（執行級 ABI 提案，而非已實裝）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG,不得`。本章觸發/Consumer=Original typed ABI Producer/Consumer per Seam；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH16.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0041`** `[SOURCE:SBL-DOC-04:L3003:sha256=ee90cb1c86f6f735]`：原文實質片段「所有 ACK@1 皆是預期 **Consumer-owned** schema；本輪尚無真下游 readback/receipt。各 Consumer 都要保留 producer=SBL_DOC04@r4,source_manifest_sha,subject_sha256,schema_version,required_fields,ACK_or_NACK,scope,merge_policy,invalidati」；Parent=`L3001:## R11｜13 個不同下游 Consumer 的 Zero-Rediscovery Typed Handoff（r4）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Original typed ABI Producer/Consumer per Seam；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH16.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0042`** `[SOURCE:SBL-DOC-04:L3021:sha256=ee90cb1c86f6f735]`：原文實質片段「**ACK/NACK schema @1（設計）**：{ack_id,consumer_id,producer_id,schema_id,schema_version,producer_subject_sha,consumer_expected_fields[],observed_fields[],status:ACK/NACK,first_fail,owner_principal,timestamp,raw_rea」；Parent=`L3001:## R11｜13 個不同下游 Consumer 的 Zero-Rediscovery Typed Handoff（r4）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不得`。本章觸發/Consumer=Original typed ABI Producer/Consumer per Seam；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH16.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0043`** `[SOURCE:SBL-DOC-05:L894:sha256=3b47a0b6224b1984]`：原文實質片段「**Parser**：先 schema_version 再 subject_hash、canonical_owner、scope、currentness、source lineage、consumer route；未知必填欄→ABI_REQUIRED_FIELD，已知新次要欄經兼容映射，不靜默丟棄；原生 Writer schema 不可直接用本提案覆蓋。SPEC-D05-ABI-01／ACC-D05-ABI-01 P」；Parent=`L888:### R02.1.A｜SBL ABI 與 P4 JSON Schema 雙向轉譯：原版反證與核心設計保留`；原 ID=`SPEC-D05-ABI-01`；NEG=`EXPLICIT:不可,NEG`。本章觸發/Consumer=Original typed ABI Producer/Consumer per Seam；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH16.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0044`** `[SOURCE:SBL-DOC-05:L6061:sha256=3b47a0b6224b1984]`：原文實質片段「ReaderReceiverHandoffLedger{handoff_id,subject_hash,producer,consumer,schema_version,source_freeze_ref,pi_ref,pd_ref,chosen_ecp_id,workorder_ref,gate_ref,mode_ref,permission_ref,first_fail,ack_or_nack,raw_recei」；Parent=`L6057:### R10.1.A｜W3/W4/W5 ACK/NACK TypedHandoff：原版反證與核心設計保留`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=Original typed ABI Producer/Consumer per Seam；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH16.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0045`** `[SOURCE:SBL-DOC-05:L6148:sha256=3b47a0b6224b1984]`：原文實質片段「每條 TypedHandoff@1 必含 source_ref,source_digest,subject_hash,producer,consumer,schema_id,version,workorder_ref,pi_ref,pd_read_ref,ecp_requirement_ref,chosen_native_ecp_ref,permission_ref,gate_ref,ack_nack_predica」；Parent=`L6141:### R10.4.A｜TypedHandoff parser / ACK-NACK 決策器 / Recovery（F15）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:Neg,不得,不可`。本章觸發/Consumer=Original typed ABI Producer/Consumer per Seam；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH16.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0046`** `[SOURCE:FHS-BODY-03:L35:sha256=58628861e63956ae]`：原文實質片段「/ PIPD-LS-SP f6335a94157c61da75d92121d14c43feb413e981 / src/pipd_ls_sp/cli.py COMMANDS 恰 13；pipeline.py deterministic；registry.py SOURCE_ORDER 恰19；requirements.lock / 19 Contract/13 CLI exact-set，requirements.l」；Parent=`L28:## 四庫 2026-10-30 `main` 原始碼錨定（GitHub 唯讀）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不可`。本章觸發/Consumer=Original typed ABI Producer/Consumer per Seam；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH16.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0047`** `[SOURCE:FHS-BODY-03:L79:sha256=58628861e63956ae]`：原文實質片段「1. Source/Intent/Profile → PI：原 Intake/Source/Profile Writer 供應 source digest、atoms、profile；PI Writer 消費 strict schema。副檔存十二軸風險與原 27/149 映射；禁止注入 _profile_meta。DOC07 ↔ legacy DOC03、12→9 未 Owner 綁定時只此 promotion H」；Parent=`L77:## R2-03-ABI：五個 typed handoff`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:禁止`。本章觸發/Consumer=Original typed ABI Producer/Consumer per Seam；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH16.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0048`** `[SOURCE:FHS-BODY-03:L89:sha256=58628861e63956ae]`：原文實質片段「設計 sidecar 必具 subject_id/source_manifest_sha/candidate_sha/producer/consumer/schema_ref/payload_sha/effect_class/observed_at。接收端先驗 hash/currentness/schema，再驗 authority，最後做 domain predicate；順序錯誤不得靠 generic ACK 補」；Parent=`L87:## R2-03-SUBJECT：跨域訊息關聯`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不得`。本章觸發/Consumer=Original typed ABI Producer/Consumer per Seam；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH16.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。

### F.2 本章 WP 與 Producer／typed I/O／FirstFail（每項獨立）

- **WP-FHS-05**：Producer=SBL-hosted original PIPD Compiler/Reader；Input=三份不同 SPECDraft、原 SourceManifest/Authority/Profile safety veto、原 PIPD Writer version；Output=非空 strict PI，真 RepoContext 才有 PD，DEV/OPS EffectIntent 分開，PlannedTQAEP 不冒 Checker；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=PIPD Native Compiler 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=把 _profile_meta 側掛塞進 strict PI；或憑 Caller HEAD 虛構本機 Repo binding；EDGE=PI SourceSHA 不變而 RepoHEAD 改變，只使 PD/ECP stale；不可偷重寫 PI requirement 原義；FirstFail=`PIPD_STRICT_SCHEMA_OR_SOURCE_NACK`；rollback=隔離候選刪除/回復 preimage；SourceSHA/HEAD 變更僅重編受影 PD/ECP。
- **WP-FHS-07**：Producer=原 HGK Native PLAN Writer/Reader；Input=W0 WP15 三 SPEC/QuestionLedger、PLAN base_revision、original Native PLAN CAS Reader；Output=PlanRevisionProposal + original CAS(base_revision, proposal_hash) ACK/NACK；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=Native PLAN Commander A/B/C 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=跳過原 PLAN Writer 直接送 ECP→Issuer 或停用 legacy commander 提升成新 Gate；EDGE=兩個 proposal 同 base_revision 競逐，僅一個 Writer CAS 成功；另一個明確 NACK；FirstFail=`PLAN_CAS_STALE_BASE`；rollback=CAS mismatch 丟棄提案並重讀 base；不寫 Target Repo/second Queue。

### F.3 複合原義拆解、反向閉包與受影退出

- **「各有」**：本 CH 的每個原 clause locator 各自保留 SourceSHA/Parent/OriginalConsumer、POS/NEG；若原文有多個 named roles/Host/Case，不可用單一結果冒全數。
- **「分別」**：strict JSON body／@2 sidecar、Original Policy Active／Host Loaded、Maker challenge／Protected Checker、Selected／ActualServed 是不同欄位與收據，不得合併。
- **「對應」**：必 `original source line → SCL-W1 id → CH → W1 WP → expected Case → original source line` 可機械重算；原 OriginalID 未明者只引用明示的 SourceSpan，不可猜 ID。
- **「不得／若／除非」**：否定作用域保留到原 Parent context；本章只標作者候選，原 Source Reader 取得 ACK 才能宣告原語義接受。
- **退出**：原 Reader NACK 僅 PARK 本章受影的 PI/PD/DEV/OPS/Host operation；合法 SOURCE_READ、隔離草稿及不依賴該 ABI 的 W0/W2 工作照原許可前進。

## CH-16 專屬退出與回退

DraftMaker 後續須填 `original_reader_ref`, `original_schema_version_or_HOLD`, `source_span_sha`, `same_subject_and_scope`, `Case/Oracle`, `positive_raw_expected`, `negative_raw_expected`, `first_fail`, `resume_predicate`, `last_good`, `consumer_ack_or_HOLD`。`DOC_AUTHOR_DONE` 是本檔可檢索，不是 `跨庫 Typed ABI、Producer→Consumer、Same Subject 交接` 已原 Host Qualified。若權限／能力尚缺，只 PARK 受影操作；回退到該 Domain 上次有效 Reader/Host 版本、保留跨波合法 READ/DRAFT，且不得刪原 NEG 或憑此文件自簽。



## 本章 L2-r4 設計義務接收卡（CH-16：0 綁定，具名 HOLD）

本章在 24 張 L2-r4 DesignID 義務中**沒有任何一張綁定到 CH-16**（`obligation_registry.jsonl` 的 `ch_ids` 全集不含 CH-16；`chapter_handoff_registry.json` 的 CH-16 `subclaims` 為空）。因此本章不列義務卡 ID，也不以相鄰章（CH-17/CH-18）的 DesignID 代替 —— 那是 `SEMANTIC_JOIN_OR_OWNER_HOLD_NACK` 禁止的代填。

本章可稽的義務面改由 F.1 的 9 個原文子義槽承載：`SCL-W1-0040`～`SCL-W1-0048`（每筆附 `SOURCE:file:line:sha256`、Parent、NEG 與原始片段），逐筆對應 Original cross-repo ABI Producer/Consumer。

- **HOLD**：`DESIGN_OBLIGATION_BINDING_HOLD`｜Owner=Original cross-repo ABI Producer/Consumer Readers｜RequiredRaw=本章對應的 OriginalID/Parent/NEG/Original Oracle 綁定同一 DesignID｜Resume=原 Reader 回同 SourceSHA/Scope 的綁定結果或具名 deferral。
- **不阻**：本章的 SOURCE_READ、F.1 子義追溯、W1→W2 typed envelope。

## AUTHOR-FINAL｜CH-16 受影交付契約

**Input / Operation / Output**：保留本章原有專屬 I/O、原句與 NEG；以當期 Registry 對同 SourceSHA/Subject/Scope 重算受影子圖，輸出 CH-16 的原 Reader BindingRequest，實質輸出與業務 FirstFail 以本章上文專屬契約及下列子義為準。

**Original Reader / Original Consumer**：Original cross-repo ABI Producer/Consumer Readers；原 Consumer Raw=EXPECTED_NOT_OBSERVED。L1 起始 1616、終止 1680，section SHA `1e717d56998665286e028c9ea3ad32aeabe01bfe9dda1a69e1f61ba36e058862`。

**POS / NEG / FirstFail**：本章專屬正負條件逐筆如下；沒有適用子義的跨 ABI 章以原本章完整 POS/NEG 為準，不從別章借用 PASS。**EDGE**：SourceSHA/Host/PolicyEpoch 其中一欄改變，只 invalidate 受影接線；**SEC**：Maker 假 ACK 或跨 Principal 原回條均拒收。**ExpectedRaw**：同 Subject/Candidate/Scope 原 Consumer/World bytes；本輪 NOT_RUN。**Stop**：缺該 Effect 必需原 Reader 即 PARK 其效果；**Resume**：同 Scope 原 Reader 提供具名 Raw；**NextWave**：W2 原 Effect Receiver，四 Host/Cell/W18 交 W3，CI/Publisher 交 W4。


<a id="ch-17"></a>

# CH-17｜Fabric Policy／FAR／治理鏡像與 FHS 工程入口

### r2 受影修補（2026-11-05｜AUTHOR_FINAL_AFFECTED_REPAIR）

**受影 Finding**：`F-09、N-04、N-07`。**原位差額**：Fabric 導航仍 `effect_permission=NONE`；Policy 的 staged／active／loaded 三段分離，Epoch 更新只重驗受影 consumer，且 W1 不因 Policy HOLD 而停止來源讀取。

**未變更**：本章 H1 標題、L1 span／section SHA、OriginalID／Parent／NEG 與原 Reader 法位皆不變；原域 Raw 未取得者維持 `EXPECTED_NOT_OBSERVED`，不以作者推斷補值。

**下一個 Reader**：Original Fabric Policy Reader；FirstFail 見本章 POS／NEG／SEC 卡與 `AFFECTED_FINDINGS.jsonl` 對應列。

## W1 草案當期完成契約｜CH-17（DRAFT-W1-CH17）

**使用者可得結果**：Fabric Policy / FHS-NAV/v2；合法執行範圍限 `SOURCE_READ` 與作者端規格審閱，無真 Host 准入或新 Writer 權限。

| 受影型別 | 本章可驗證的確定規則 |
|---|---|
| Input／觸發 | Fabric README→repository-map→原 Policy source/epoch/readback；強制 `subject_id/source_manifest_sha/scope` 來源釘選 |
| 操作／Producer | 先讀導航，將 task class 路由成候選，只做 `effect_permission=NONE`；真正 ActiveEpoch/LoadedDigest/ConsumerACK 分讀原 Owner 與 HGK；Producer＝W1 DraftMaker（僅文字/Sidecar），正式效果由原域 Producer 執行 |
| Output／交付 | FHS 路由來源卡、PolicyScopeCandidate、未生效原因；所有未觀測 Reader Raw 留空並具名 `EXPECTED_NOT_OBSERVED` |
| Original Reader | Fabric original Policy Reader + HGK original Consumer；原 Writer／Issuer／Checker 不因本稿改權 |
| Downstream Consumer | HGK policy/admission；W2 WP06；綁同 Subject／Scope，需 Original ACK 才可升級 |
| POS／Expected Raw | navigation 指出三庫且 cross_repo 只開各庫候選；預期由原 Consumer 返回原格式 Raw（本輪 `NOT_RUN`） |
| NEG／首拒收 | FHS-NAV pointer 當作 HGK permit；把 PIPD 歷史庫當 live canonical；FirstFail=`FABRIC_POLICY_LOADED_ACK_HOLD` |
| EDGE | 未知 route 只 HOLD affected write；只 PARK 受影 scope，合法 READ/DRAFT 不受波及 |
| SEC | PolicyEpoch mismatch 仍放行受保護效果；缺憑證、Owner、ACL 或 Checker 證物拒效果 |
| Stop／Resume／Rollback | 遇 `FABRIC_POLICY_LOADED_ACK_HOLD` 記 `hold_id+original_reader+required_raw`，停止受影寫入；Resume 需同 SourceSHA/Scope 的原 Reader 結果；READ 丟棄快照、DRAFT 刪除隔離候選；世界效果不在 W1 自行 rollback |
| Cross-wave | W2 Policy consumer；交 `AUTHOR.FHS.W1ToW{next}@design` typed envelope，禁止偽裝 WorkOrder |

**受影源句拆義**：`actor/trigger/action/object`（見 Input/操作）；`condition/exception`（見 EDGE）；`prohibition`（見 NEG/SEC）；`outcome/consumer`（見 Output/Original Reader）；`POS/NEG/FirstFail` 必綁同一原 RequirementID。來源的原始句、Span、SHA、Parent/Child/NEG 以 r5 本章及附錄 `obligation_registry.jsonl` 回指；缺具體原 Reader 即 `ORIGINAL_OWNER_HOLD`，不自行創造簽核。


### R5 本章受影精確契約／業務負例（整合 r4，非歷史附錄）

Fabric Mirror `effect_permission=NONE`。`Source→Stage→OwnerApproval→ActiveEpoch→LoadedDigest→HGK ConsumerACK` 六層不同證據。NEG=Stage 有 digest 但 epoch/Consumer Raw 缺卻宣 Applied → `POLICY_LOADED_CONSUMER_ACK_MISSING`；只 PARK 相依 HOST_OPS，SOURCE_READ 可繼續。


**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L1681–1741`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Fabric Policy Owner/Consumer；L2-r4:L907。原 Domain Reader/Writer 不因本章轉移。

## r4 當期原 Reader 鎖與非降級本體

本章 L1-r4 依以上真實行區間及原域 Reader；無單獨 R4-BEGIN 增量不等於以歷史 r2 取代 L1。W1 契約下文僅是對該 L1 已定義原義的工程操作化。

## r4 對齊之 W1 主波操作規格、草案必填欄、逐項 POS/NEG／FirstFail（高保留整合）

**Protected Original H1 / CURRENT L1-r4**：`FHS_PIPD-LS-PKG_藍圖_2026-11-04_r4_HIGH_RETENTION_AUDIT_REPAIRED_實質正文(1).md:L1681–L1741`；`source_file_sha256=cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`；`section_sha256=d07505132f0a12e2113fce9ec0c84da655c91e32c717c04a7c21d8f394c2f10d`；`heading_exact=# CH-17｜Fabric Policy／FAR／治理鏡像與 FHS 工程入口`；**HISTORICAL_LOCATOR_NOT_EFFECTIVE**=`L1:1172–1218` / `L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`，L2 作者端路由 `L2:655`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W1 不取得原 Writer。

## A. 本章實質功能與不能壓平的原義

Fabric Source/Stage/OwnerApproval/ActiveEpoch/LoadedSHA/ConsumerACK 六階分離，FHS-NAV 只導航。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。

## B. 來源 r5 skeleton 必填核對欄（已由上方 W1 草案當期完成契約受影回填）

| 必填欄 | 欄位設計／不可空條件 |
|---|---|
<!-- HISTORICAL_R5_SKELETON_FILL_REQUEST_SUPERSEDED: transition wording only; all substantive constraints retained -->
| `chapter_id` / `primary_wave` / `author_writer` | `CH-17` / `W1` / `W1:DraftMaker`（歷史 r5 階段欄；當期為作者端定案候選） |
| `original_sources[]` | 本章 L1 行與下面原冊 SHA／OriginalClause Span；不得用語義假定的 ID 補空缺 |
| `same_subject` / `candidate_sha` / `source_manifest_sha` / `affected_scope` | 必攜相同 Subject/Scope，未原 Reader 認證則 `AUTHOR_CANDIDATE` |
| `effect_class` / `original_owner` / `consumer_abi` / `schema_version` | 依 Operation Reader；缺 `$id` 或 Receiver 不自造 |
| `input` / `typed_output` / `fuo` / `non_goals` | 應有真使用者結果與 Receiver（非檔案數） |
| `positive_fixture` / `negative_fixture` / `security_fixture` | 原 Source Case/Oracle 逐受影引用，未有 Runner/Raw 就 `EXPECTED_NOT_OBSERVED` |
| `first_fail` / `hold` / `stop_scope` / `resume_predicate` | 明確停止受影子圖，不全域凍結 READ／DRAFT |
| `rollback` / `w2_handoff` / `original_ack_nack` | 回退路由與 same scope 的預期接收；不得填假 PASS |

## C. Input → Producer → 原 Reader／Consumer → Output

- **Input/Guard**：Fabric Policy SourceSHA、Mirror4、原 Owner decision、active/loaded Consumer 認證。
- **Producer**：該 Original Domain 的 Reader/Compiler/Host/Guide 依本章功能生產；W1 Curator 僅記設計；**Original Consumer**：Fabric Policy Owner → HGK policy consumer。
- **Typed Output/FUO**：PolicyLoadedConsumerACK 期待與受界 GAP 報表。
- **版本要求**：至少 `Subject,CandidateSHA,SourceSHA,OriginalID+SourceSpan,Scope,Host/PolicyEpoch（受影才填）,ABI $id/version,OriginalReader,OutputRawExpected`，少一欄只停需該欄的出口。

## D. POS／NEG／FirstFail／HOLD／退出

- **POS（期待）**：同 epoch 的 Effective policy 與 consumer loaded 回顯。
- **NEG／SEC（期待拒收）**：NAV_ASSISTED_USE_APPROVED 直接視為有效 Policy Permit。
- **FirstFail**：`POLICY_NOT_LOADED`；禁止只有泛稱 `VALIDATION_FAILED` 而不給首次失敗位置。
- **HOLD/Owner**：`FABRIC_EFFECTIVE_POLICY_READER_HOLD`。需同 Subject/Scope/Host/原 Reader 的真 Raw/ACK 解除；本輪 `NOT_RUN`。
- **Stop/Resume**：保留原 SourceSHA/受影 Reader/cursor/last-good；READ/DRAFT 合法部分繼續；UNKNOWN 必原 Reader reconcile。
- **Rollback**：只回復該 Need/Host 的原 last-good，Host/OPS 效果走原 inverse；不得以檔案 ZIP 作回復收據。

## E. 來源追溯、波次邊界與下一手

| 源鍵／檔案 | 原文 SHA | 此 W1 處理方式 |
|---|---|---|
| SBL-DOC-06 | 64ea4977dab3093301f82dc7469413cc754998fc53946467842e06d83645102b | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| SBL-DOC-07 | a366d3783c82089c5593ffabb0704d8507632cce45622684f7a0186f2ae310f8 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-04 | a7d54bdeb9129e7e1979bbc1af1944189b1054760e76424f8ffd8547a682eb1f | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
W0 提供原 Source/三 SPEC/索引；本 `CH-17` 不修改 W0 成果。W1 WaveCurator 交 W1 DraftMaker 按原 Reader 定位填入真 Requirements；W2 僅領同 Subject/Scope 的需要的 Effect/Case/HOLD，不得借 W3/W4 收據。原 L1 CH-17 的詳細原義仍在 L1 主體，不移作本冊第二 Canonical。

## F. r2 原位修補：CH-17 可直接交接的受影實質規格（非證據附錄）

**本章不可壓平功能**：Fabric Policy stage→active→loaded consumer。與 W0 三份獨立 SPEC 維持同 SourceSHA/Subject/Scope；將原讀者真接收的 **Output／Consumer** 優先於填滿文件欄位。依 L1 原 CH 身份與 L2 W1 主責修訂，不移轉原 Writer。

### F.1 原句→原 Consumer→本章測例的逐子義槽（已從原物理檔定位）

- **`SCL-W1-0049`** `[SOURCE:SBL-DOC-06:L934:sha256=64ea4977dab30933]`：原文實質片段「/ NTD-012 / Grill with Docs / policy=DONOR_PATTERN_ONLY; runtime=NOT_INSPECTED; owner=F11-03 / SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope;  / SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r」；Parent=`L731:### C33.2.9｜386/386 OriginalIdentity 逐筆 AdmissionDecision@2 擴充欄（不可與原處置相混）`；原 ID=`NTD-012`；NEG=`EXPLICIT:不得`。本章觸發/Consumer=Fabric Policy Owner + HGK original policy consumer；承接 `WP 02`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH17.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0050`** `[SOURCE:SBL-DOC-06:L1045:sha256=64ea4977dab30933]`：原文實質片段「/ GPTB-KP10-R03 / L1773; MUST; Bind PR to tests and rollback / MUST → NONE → COMMANDER_ONLY / MUST → NONE → COMMANDER_ONLY / SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L710 @sha256:83ea1bef8d045bf0…; upstream HERM」；Parent=`L731:### C33.2.9｜386/386 OriginalIdentity 逐筆 AdmissionDecision@2 擴充欄（不可與原處置相混）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:禁止`。本章觸發/Consumer=Fabric Policy Owner + HGK original policy consumer；承接 `WP 02`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH17.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0051`** `[SOURCE:SBL-DOC-06:L1089:sha256=64ea4977dab30933]`：原文實質片段「/ GPTB-KP15-R07 / L2476; SHOULD; Require rollback pointer / SHOULD → NONE → COMMON / SHOULD → NONE → COMMON / SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L754 @sha256:83ea1bef8d045bf0…; upstream HERMES  HG-KSEOS  F」；Parent=`L731:### C33.2.9｜386/386 OriginalIdentity 逐筆 AdmissionDecision@2 擴充欄（不可與原處置相混）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:禁止`。本章觸發/Consumer=Fabric Policy Owner + HGK original policy consumer；承接 `WP 02`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH17.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0052`** `[SOURCE:SBL-DOC-07:L1090:sha256=a366d3783c82089c]`：原文實質片段「/ GPTB-KP15-R07 / L2476; SHOULD; Require rollback pointer / SHOULD → NONE → COMMON / SHOULD → NONE → COMMON / DOC06:C33.2.9:L1089 / SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L754 @sha256:83ea1bef8d045bf0…; upstre」；Parent=`L732:### C44.1bb｜DOC06 OriginalID 386/386 不覆寫安全讀取投影（r4 ACTIVE）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:禁止,NEG`。本章觸發/Consumer=Fabric Policy Owner + HGK original policy consumer；承接 `WP 02`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH17.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0053`** `[SOURCE:SBL-DOC-07:L1099:sha256=a366d3783c82089c]`：原文實質片段「/ GPTB-KP16-R08 / L2618; MUST; Block production without preview/upload readback / MUST → NONE → SUPERSEDED / MUST → NONE → SUPERSEDED / DOC06:C33.2.9:L1098 / SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L763 @sha256」；Parent=`L732:### C44.1bb｜DOC06 OriginalID 386/386 不覆寫安全讀取投影（r4 ACTIVE）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:禁止,NEG`。本章觸發/Consumer=Fabric Policy Owner + HGK original policy consumer；承接 `WP 02`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH17.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0054`** `[SOURCE:SBL-DOC-07:L1154:sha256=a366d3783c82089c]`：原文實質片段「/ FAR/FDA / L218 / HGK_FABRIC_EXISTING_ONLY (not installed claim) / BLOCKED_EXTERNAL；readback before actual call; no SBL replacement / Host/源 SHA/合法 Owner 下只作被准入用途候選 / 不滿足 BLOCKED_EXTERNAL → METHOD_ADMISSION_HO」；Parent=`L1127:### C44.1c｜§9D 25/25 Named Method/Tool 安全覆蓋與防降級（來源原態不改）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:neg`。本章觸發/Consumer=Fabric Policy Owner + HGK original policy consumer；承接 `WP 02`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH17.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0055`** `[SOURCE:FHS-BODY-04:L42:sha256=a7d54bdeb9129e7e]`：原文實質片段「1. **Policy Flow**：Original Fabric Source＋Owner Approved Epoch→原 route_event() 是決策 Reader，不是 Host Activation；由原 Host Consumer 產 ActiveEpoch/LoadedSHA/ConsumedACK 真 Receipt；HGK 只 consume 相同 PolicyEpoch。Stage/Can」；Parent=`L40:### 4.2 五條正式 Typed Adapter Flow：Input/Producer→輸出→Consumer、正負例`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Fabric Policy Owner + HGK original policy consumer；承接 `WP 02`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH17.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0056`** `[SOURCE:FHS-BODY-04:L54:sha256=a7d54bdeb9129e7e]`：原文實質片段「/ POLICY_CONSUMED / Fabric 原 Owner ActiveEpoch＋真 Host Loaded/Consumed / 同 Epoch 所需資格成立 / 只有 Canary→POLICY_HOLD /」；Parent=`L48:### 4.3 Native E2E 自主執行狀態機：Actor、事件、Fence、Unknown Effect、補償`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Fabric Policy Owner + HGK original policy consumer；承接 `WP 02`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH17.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0057`** `[SOURCE:FHS-BODY-04:L114:sha256=a7d54bdeb9129e7e]`：原文實質片段「Source→Stage→OwnerApprove→ActiveEpoch→LoadedSHA→ConsumerACK 各自是不同觀測。Stage/檔案存在只能證明候選可讀。原 Fabric Owner Reader 需回 active epoch、policy digest 和 host/process identity；HGK Reader 需回相同 epoch、loaded digest 與 consumer 」；Parent=`L112:## R2-04-CURRENT：五層證據與現役唯讀起跑`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Fabric Policy Owner + HGK original policy consumer；承接 `WP 02`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH17.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。

### F.2 本章 WP 與 Producer／typed I/O／FirstFail（每項獨立）

- **WP-FHS-02**：Producer=Fabric Policy Owner → HGK policy consumer；Input=Original Fabric Policy Owner/current epoch; applicable Policy manifest SHA; HGK original policy consumer process identity；Output=ActiveEpoch+LoadedDigest+ConsumerACK（由 Fabric+HGK 原 Reader 同 Subject 讀回）；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=Fabric Policy Consumer 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=把未批准 Stage SHA 當 ActiveEpoch、HGK LoadedDigest 與 active 不符；EDGE=Owner 在 Stage 後切 epoch，舊 HGK process 尚載前 epoch；僅停受影 OPS，READ 繼續；FirstFail=`POLICY_EPOCH_LOADED_MISMATCH`；rollback=原 Fabric/HGK Owner 以原 epoch migration/inverse 回 last-good，Stage 不可當 Active。

### F.3 複合原義拆解、反向閉包與受影退出

- **「各有」**：本 CH 的每個原 clause locator 各自保留 SourceSHA/Parent/OriginalConsumer、POS/NEG；若原文有多個 named roles/Host/Case，不可用單一結果冒全數。
- **「分別」**：strict JSON body／@2 sidecar、Original Policy Active／Host Loaded、Maker challenge／Protected Checker、Selected／ActualServed 是不同欄位與收據，不得合併。
- **「對應」**：必 `original source line → SCL-W1 id → CH → W1 WP → expected Case → original source line` 可機械重算；原 OriginalID 未明者只引用明示的 SourceSpan，不可猜 ID。
- **「不得／若／除非」**：否定作用域保留到原 Parent context；本章只標作者候選，原 Source Reader 取得 ACK 才能宣告原語義接受。
- **退出**：原 Reader NACK 僅 PARK 本章受影的 PI/PD/DEV/OPS/Host operation；合法 SOURCE_READ、隔離草稿及不依賴該 ABI 的 W0/W2 工作照原許可前進。

## 本章 L2-r4 設計義務接收卡（逐 ID；不可省略原 NEG）

- `FHS-DR-029` (`L1-r4:L826`, `L2-r4:L367`)：治理／A＋B；Fabric FHS-NAV/v2 是唯一跨庫導航入口且唯讀；先 Fabric FHS README/map，再 SBL/HGK 原域 Reader；[CH-17](#ch-17)；POS `三庫各自 bounded PR/source fact`；NEG/FirstFail `導航 metadata 被當授權來源；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `Fabric FHS Navigation/Policy/FAR Reader → Original Consumer`；本輪只有 EXPECTED_NOT_OBSERVED。
- `FHS-DR-030` (`L1-r4:L827`, `L2-r4:L368`)：治理／A＋B；Fabric Policy/FAR 原 Reader/Consumer 可實際回讀；PolicyEpoch/RequiredSet/Producer/Original R8 Consumer ACK；[CH-17](#ch-17)/[CH-40](#ch-40)；POS `R8 真 ACK 不被研究文件代替`；NEG/FirstFail `工具回應被視為 Policy Applied；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `Fabric FHS Navigation/Policy/FAR Reader → Original Consumer`；本輪只有 EXPECTED_NOT_OBSERVED。

## CH-17 專屬退出與回退

DraftMaker 後續須填 `original_reader_ref`, `original_schema_version_or_HOLD`, `source_span_sha`, `same_subject_and_scope`, `Case/Oracle`, `positive_raw_expected`, `negative_raw_expected`, `first_fail`, `resume_predicate`, `last_good`, `consumer_ack_or_HOLD`。`DOC_AUTHOR_DONE` 是本檔可檢索，不是 `Fabric Policy／FAR／治理鏡像與 FHS 工程入口` 已原 Host Qualified。若權限／能力尚缺，只 PARK 受影操作；回退到該 Domain 上次有效 Reader/Host 版本、保留跨波合法 READ/DRAFT，且不得刪原 NEG 或憑此文件自簽。



## AUTHOR-FINAL｜CH-17 受影交付契約

**Input / Operation / Output**：保留本章原有專屬 I/O、原句與 NEG；以當期 Registry 對同 SourceSHA/Subject/Scope 重算受影子圖，輸出 CH-17 的原 Reader BindingRequest，實質輸出與業務 FirstFail 以本章上文專屬契約及下列子義為準。

**Original Reader / Original Consumer**：Fabric Original Policy Reader → HGK Policy Consumer；原 Consumer Raw=EXPECTED_NOT_OBSERVED。L1 起始 1681、終止 1741，section SHA `d07505132f0a12e2113fce9ec0c84da655c91e32c717c04a7c21d8f394c2f10d`。

**POS / NEG / FirstFail**：本章專屬正負條件逐筆如下；沒有適用子義的跨 ABI 章以原本章完整 POS/NEG 為準，不從別章借用 PASS。**EDGE**：SourceSHA/Host/PolicyEpoch 其中一欄改變，只 invalidate 受影接線；**SEC**：Maker 假 ACK 或跨 Principal 原回條均拒收。**ExpectedRaw**：同 Subject/Candidate/Scope 原 Consumer/World bytes；本輪 NOT_RUN。**Stop**：缺該 Effect 必需原 Reader 即 PARK 其效果；**Resume**：同 Scope 原 Reader 提供具名 Raw；**NextWave**：W2 原 Effect Receiver，四 Host/Cell/W18 交 W3，CI/Publisher 交 W4。

- `S-W1-FHS-DR-029-01`：Input=Fabric FHS-NAV/v2 唯讀先行再進三域；POS=Fabric README/map 與原域 Reader 分離；NEG=NAV metadata 冒 HGK admission；FirstFail=`NAVIGATION_NOT_PERMISSION`；Consumer=Fabric FHS navigation and Original Domain Reader (primary W0)；Case=`AUTHOR.W1.FHS-DR-029.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-029-02`：Input=三庫修改分別由各 repo branch+PR；POS=每庫自身 verified HEAD/rollback；NEG=單一影子 commit 跨庫生效；FirstFail=`CROSS_REPO_WRITER_COLLISION`；Consumer=Fabric FHS navigation and Original Domain Reader (primary W0)；Case=`AUTHOR.W1.FHS-DR-029.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-030-01`：Input=Fabric Source/Stage/Approval/Active 各獨立；POS=Active epoch 與源 hash 可回讀；NEG=只有 stage 就宣 Active；FirstFail=`POLICY_STAGE_AS_ACTIVE_NACK`；Consumer=Fabric Policy Owner and HGK R8 Consumer；Case=`AUTHOR.W1.FHS-DR-030.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-030-02`：Input=HGK Loaded epoch/Consumer ACK 同 Scope 另有證據；POS=original R8 Consumer Raw 狀態；NEG=工具回應即視為 Policy Applied；FirstFail=`POLICY_LOADED_CONSUMER_ACK_MISSING`；Consumer=Fabric Policy Owner and HGK R8 Consumer；Case=`AUTHOR.W1.FHS-DR-030.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。

<a id="ch-18"></a>

# CH-18｜HG-KSEOS 唯一 Native Issuer／SharedSpine／WorkID／許可

### r2 受影修補（2026-11-05｜AUTHOR_FINAL_AFFECTED_REPAIR）

**受影 Finding**：`F-13、N-05`。**原位差額**：WorkID／Lease／Nonce／CAS 只由原 Issuer 產生；`UNKNOWN` 先 WorldReader 對帳，重複 WorkID 即停；作者端不發任何 Permit。

**未變更**：本章 H1 標題、L1 span／section SHA、OriginalID／Parent／NEG 與原 Reader 法位皆不變；原域 Raw 未取得者維持 `EXPECTED_NOT_OBSERVED`，不以作者推斷補值。

**下一個 Reader**：Original HGK Issuer／WorldReader；FirstFail 見本章 POS／NEG／SEC 卡與 `AFFECTED_FINDINGS.jsonl` 對應列。

## W1 草案當期完成契約｜CH-18（DRAFT-W1-CH18）

**使用者可得結果**：HGK Single Issuer/SharedSpine；合法執行範圍限 `LOCAL_DRAFT_WRITE` 與作者端規格審閱，無真 Host 准入或新 Writer 權限。

| 受影型別 | 本章可驗證的確定規則 |
|---|---|
| Input／觸發 | WorkID/Lease/Journal、Owner registry、OS principal、EffectClass、PolicyEpoch；強制 `subject_id/source_manifest_sha/scope` 來源釘選 |
| 操作／Producer | 依原 HGK Registry 探真 Issuer 與 Process ACL；將 Request→Permit→Effect→World 結構化分開；絕不二次自建 Queue/Issuer；Producer＝W1 DraftMaker（僅文字/Sidecar），正式效果由原域 Producer 執行 |
| Output／交付 | HGKAdmitRequest@design、ReaderProbe、WorldReadbackExpectation；所有未觀測 Reader Raw 留空並具名 `EXPECTED_NOT_OBSERVED` |
| Original Reader | 原 HGK Issuer/Registry/SharedSpine Reader；原 Writer／Issuer／Checker 不因本稿改權 |
| Downstream Consumer | Hermes worker/HGK actual effect（W2）；綁同 Subject／Scope，需 Original ACK 才可升級 |
| POS／Expected Raw | 同 WorkID/Scope/Epoch Permit 真實 Reader 確認；預期由原 Consumer 返回原格式 Raw（本輪 `NOT_RUN`） |
| NEG／首拒收 | Skill sidecar 自簽 Grant，回放別 Subject nonce；FirstFail=`HGK_ISSUER_PERMISSION_HOLD` |
| EDGE | Lease 過期／UNKNOWN 採 read/reconcile，不盲重試；只 PARK 受影 scope，合法 READ/DRAFT 不受波及 |
| SEC | 秘鑰、SID 跨 scope 漂移；缺憑證、Owner、ACL 或 Checker 證物拒效果 |
| Stop／Resume／Rollback | 遇 `HGK_ISSUER_PERMISSION_HOLD` 記 `hold_id+original_reader+required_raw`，停止受影寫入；Resume 需同 SourceSHA/Scope 的原 Reader 結果；READ 丟棄快照、DRAFT 刪除隔離候選；世界效果不在 W1 自行 rollback |
| Cross-wave | W2 WP06/08/09；交 `AUTHOR.FHS.W1ToW{next}@design` typed envelope，禁止偽裝 WorkOrder |

**受影源句拆義**：`actor/trigger/action/object`（見 Input/操作）；`condition/exception`（見 EDGE）；`prohibition`（見 NEG/SEC）；`outcome/consumer`（見 Output/Original Reader）；`POS/NEG/FirstFail` 必綁同一原 RequirementID。來源的原始句、Span、SHA、Parent/Child/NEG 以 r5 本章及附錄 `obligation_registry.jsonl` 回指；缺具體原 Reader 即 `ORIGINAL_OWNER_HOLD`，不自行創造簽核。


### R5 本章受影精確契約／業務負例（整合 r4，非歷史附錄）

HGK 原 WorkID/Issuer/SharedSpine/Lease/PolicyEpoch+nonce/TTL/CAS/ProcessSID/ACL 是唯一原生控制面；同一位 Owner 的預授權只在真 Scope/Effect/Expiry 原 Schema 範圍有效。NEG=兩個模型 Profile 冒 OS principal 隔離或 Maker 借 Checker credential → `MAKER_CHECKER_CREDENTIAL_DENY`。


**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L1742–1822`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** HGK Original Issuer/SharedSpine；L2-r4:L908。原 Domain Reader/Writer 不因本章轉移。

## r4 當期受影修補（直接摘取 L1 r4 本章有效增量）

## r4｜AUDIT r3 受影整合／覆蓋／取代（現行作者端規範）

**Single Human Owner ≠ single technical principal**：原 HGK Issuer/SharedSpine/WorkID、Fabric Policy、Protected Checker credentials 不可因一位人類 Owner 就共用同 OS token。Host 必驗 `SID, ACL, principal, role_binding, token_scope, TTL, nonce, revocation, checker_credential_isolation`；適用原 Owner 已給的 scoped permission，不要求額外人類例行批准，除非原政策明定；GPT 專家視角不是第二名 Owner。NEG：Maker 和 Checker 共用私鑰或聊天「我同意」當 Issuer receipt→`TECHNICAL_SOD_NACK`。

## r4 對齊之 W1 主波操作規格、草案必填欄、逐項 POS/NEG／FirstFail（高保留整合）

**Protected Original H1 / CURRENT L1-r4**：`FHS_PIPD-LS-PKG_藍圖_2026-11-04_r4_HIGH_RETENTION_AUDIT_REPAIRED_實質正文(1).md:L1742–L1822`；`source_file_sha256=cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`；`section_sha256=8b6af3908e5fe75c0eec39314232dd0a80367be74408c0cb6ff62a988076d97e`；`heading_exact=# CH-18｜HG-KSEOS 唯一 Native Issuer／SharedSpine／WorkID／許可`；**HISTORICAL_LOCATOR_NOT_EFFECTIVE**=`L1:1219–1277` / `L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`，L2 作者端路由 `L2:656`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W1 不取得原 Writer。

## A. 本章實質功能與不能壓平的原義

HGK 唯一 Registry／Issuer／WorkID／Lease／Permit；Maker/Checker 是分離技術主體。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。

## B. 來源 r5 skeleton 必填核對欄（已由上方 W1 草案當期完成契約受影回填）

| 必填欄 | 欄位設計／不可空條件 |
|---|---|
<!-- HISTORICAL_R5_SKELETON_FILL_REQUEST_SUPERSEDED: transition wording only; all substantive constraints retained -->
| `chapter_id` / `primary_wave` / `author_writer` | `CH-18` / `W1` / `W1:DraftMaker`（歷史 r5 階段欄；當期為作者端定案候選） |
| `original_sources[]` | 本章 L1 行與下面原冊 SHA／OriginalClause Span；不得用語義假定的 ID 補空缺 |
| `same_subject` / `candidate_sha` / `source_manifest_sha` / `affected_scope` | 必攜相同 Subject/Scope，未原 Reader 認證則 `AUTHOR_CANDIDATE` |
| `effect_class` / `original_owner` / `consumer_abi` / `schema_version` | 依 Operation Reader；缺 `$id` 或 Receiver 不自造 |
| `input` / `typed_output` / `fuo` / `non_goals` | 應有真使用者結果與 Receiver（非檔案數） |
| `positive_fixture` / `negative_fixture` / `security_fixture` | 原 Source Case/Oracle 逐受影引用，未有 Runner/Raw 就 `EXPECTED_NOT_OBSERVED` |
| `first_fail` / `hold` / `stop_scope` / `resume_predicate` | 明確停止受影子圖，不全域凍結 READ／DRAFT |
| `rollback` / `w2_handoff` / `original_ack_nack` | 回退路由與 same scope 的預期接收；不得填假 PASS |

## C. Input → Producer → 原 Reader／Consumer → Output

- **Input/Guard**：原 registry ABI、Host/SID/ACL、Scope/PolicyEpoch/TTL/nonce，source identity。
- **Producer**：該 Original Domain 的 Reader/Compiler/Host/Guide 依本章功能生產；W1 Curator 僅記設計；**Original Consumer**：HGK original Registry/Issuer/Receiver。
- **Typed Output/FUO**：IssuerReceiverBinding/WorkID/lease fence 期待；沒有 original issuer 不簽。
- **版本要求**：至少 `Subject,CandidateSHA,SourceSHA,OriginalID+SourceSpan,Scope,Host/PolicyEpoch（受影才填）,ABI $id/version,OriginalReader,OutputRawExpected`，少一欄只停需該欄的出口。

## D. POS／NEG／FirstFail／HOLD／退出

- **POS（期待）**：合法派發與 denied out-of-scope 分開讀回。
- **NEG／SEC（期待拒收）**：ECP/markdown 自簽 permit 或新建 Issuer/Queue。
- **FirstFail**：`ISSUER_BINDING_INVALID`；禁止只有泛稱 `VALIDATION_FAILED` 而不給首次失敗位置。
- **HOLD/Owner**：`H-ABI-05/H-OS-08`。需同 Subject/Scope/Host/原 Reader 的真 Raw/ACK 解除；本輪 `NOT_RUN`。
- **Stop/Resume**：保留原 SourceSHA/受影 Reader/cursor/last-good；READ/DRAFT 合法部分繼續；UNKNOWN 必原 Reader reconcile。
- **Rollback**：只回復該 Need/Host 的原 last-good，Host/OPS 效果走原 inverse；不得以檔案 ZIP 作回復收據。

## E. 來源追溯、波次邊界與下一手

| 源鍵／檔案 | 原文 SHA | 此 W1 處理方式 |
|---|---|---|
| SBL-DOC-07 | a366d3783c82089c5593ffabb0704d8507632cce45622684f7a0186f2ae310f8 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| SBL-DOC-05 | 3b47a0b6224b1984a4047cf53aac5ac50615c93a560fea46e1b43d079a5d9f27 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-03 | 58628861e63956ae31b1ac17404c093533226688f975f5fa11b9b82adecd1284 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-04 | a7d54bdeb9129e7e1979bbc1af1944189b1054760e76424f8ffd8547a682eb1f | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
W0 提供原 Source/三 SPEC/索引；本 `CH-18` 不修改 W0 成果。W1 WaveCurator 交 W1 DraftMaker 按原 Reader 定位填入真 Requirements；W2 僅領同 Subject/Scope 的需要的 Effect/Case/HOLD，不得借 W3/W4 收據。原 L1 CH-18 的詳細原義仍在 L1 主體，不移作本冊第二 Canonical。

## F. r2 原位修補：CH-18 可直接交接的受影實質規格（非證據附錄）

**本章不可壓平功能**：HGK sole registry/issuer/WorkID。與 W0 三份獨立 SPEC 維持同 SourceSHA/Subject/Scope；將原讀者真接收的 **Output／Consumer** 優先於填滿文件欄位。依 L1 原 CH 身份與 L2 W1 主責修訂，不移轉原 Writer。

### F.1 原句→原 Consumer→本章測例的逐子義槽（已從原物理檔定位）

- **`SCL-W1-0058`** `[SOURCE:SBL-DOC-07:L539:sha256=a366d3783c82089c]`：原文實質片段「TokenRef 僅 opaque handle，密鑰原文不可進 AGENT context/trace/log；驗簽時必查 issuer、audience、tenant、delegate_chain、nonce、TTL、requested effect、subject digest、revocation_epoch 的即時原生狀態。POS 模擬收發兩次皆為有效 scope 時只產 request；NEG 在排程後、」；Parent=`L537:### C27.3b｜Token Broker 真 issuer 與競態雙檢（不把模型上下文當錢包）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不可,NEG,不得,不能`。本章觸發/Consumer=HGK original Registry/Issuer/SharedSpine；承接 `WP 03/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH18.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0059`** `[SOURCE:SBL-DOC-07:L593:sha256=a366d3783c82089c]`：原文實質片段「**SDOG-NEG — 自改 Oracle 或刪減 Veto**。Given：Maker 具有安全文件 edit proposal 權限，無 Oracle/Permission Owner 權限。When：同一模型把 mandatory_negs 刪除、將 TQ_SOD 改成通過或發出自簽 ToolPermit。Then：載入與寫入均不生效、原生拒絕 SELF_ORACLE_EDIT_DENIED，保留 A 可用、」；Parent=`L589:### C27.5b｜兩個受控自舉 Security Dogfood Golden Cases（均 NOT_EXECUTED）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG,neg,不得,不能`。本章觸發/Consumer=HGK original Registry/Issuer/SharedSpine；承接 `WP 03/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH18.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0060`** `[SOURCE:SBL-DOC-07:L1626:sha256=a366d3783c82089c]`：原文實質片段「以下為 **47 組 r2 stable baseline 的 JSONL 設計記錄（各五筆、共 235 筆；r4 13 個新增原子同級 65 筆見 R03.6a，當輪總計 300 筆，SPEC／ACC／POS／NEG／EExp 各 47 筆）**。每筆具完整欄位與同候選追溯索引，預期測試尚未執行，RawReceipt 均為 NONE。SBL-D07-PROP-* 對正式 Registry 沒有 Owner 權限；這」；Parent=`L1624:## R03.6｜逐原子完整 Typed SPEC／ACC／Fixture／EvidenceExpectation 設計記錄（47 stable + 13 r4 新增）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=HGK original Registry/Issuer/SharedSpine；承接 `WP 03/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH18.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0061`** `[SOURCE:SBL-DOC-05:L1295:sha256=3b47a0b6224b1984]`：原文實質片段「EffectPermitMatrix{effect_id,lane,actor,scope,permit_issuer,token_ref,expires_at,revoked_at,chosen_ecp_id,subject_hash,at_most_once_key,retry_max,readback_ref,rollback_pointer,native_receiver,ack_ref}。Write 権在正」；Parent=`L1291:### C28.4.A｜補償決策和殘留掃描閉環：原版反證與核心設計保留`；原 ID=`SPEC-D05-ECP-01`；NEG=`EXPLICIT:不得`。本章觸發/Consumer=HGK original Registry/Issuer/SharedSpine；承接 `WP 03/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH18.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0062`** `[SOURCE:SBL-DOC-05:L1364:sha256=3b47a0b6224b1984]`：原文實質片段「DEV 可提 code/test/diff/worktree 更動，但只在 Repo Owner 受界且 Native Permit 有效時；OPS 涉 migration/deploy/backup/restore/rollback，必有不同權限類別、不同操作憑證與額外 rollback authorization。受控 executor、Maker、checker、permit issuer、receiver 均」；Parent=`L1362:## R05.4｜DEV／OPS 權限與零效果檢查表`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=HGK original Registry/Issuer/SharedSpine；承接 `WP 03/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH18.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0063`** `[SOURCE:SBL-DOC-05:L5858:sha256=3b47a0b6224b1984]`：原文實質片段「/ SBL_PIPD-LS-PKG_DOC-05_藍圖+skeleton.md#L873 / C28.4 授權矩陣與失敗補償 / D05-ATOM-028 → SBL-D05-SPEC-ATOM-028（承接 C28 的具名 Typed IO；同來源 digest、subject_sha） / ACC-D05-ATOM-028：至少原子 source_ref+owner+非空可解析 Typed Output；FX-D」；Parent=`L5825:## R08.6｜52 個歷史 H2 → 原始 Clause／原子 SPEC／ACC／雙向 Fixture／EExp／DELIVER（作者端候選）`；原 ID=`SPEC-ATOM-028`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=HGK original Registry/Issuer/SharedSpine；承接 `WP 03/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH18.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0064`** `[SOURCE:FHS-BODY-03:L24:sha256=58628861e63956ae]`：原文實質片段「原 TaskSpec/WorkOrder 的建立本身屬 Canonical state mutation，仍走原 HGK受保護准入。這與「讀來源／做本地草稿不必先有 Native effect Permit」是兩條界線，不可互相冒用。原五檔 WriteSet=ProductSPEC.json, ArchitectureSPEC.json, ProgramSPEC.json, SourceReadback.json, 」；Parent=`L14:## HANDOFF-v1｜首工作 Effect、Scope 與原生准入分流`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不可,禁止`。本章觸發/Consumer=HGK original Registry/Issuer/SharedSpine；承接 `WP 03/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH18.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0065`** `[SOURCE:FHS-BODY-03:L37:sha256=58628861e63956ae]`：原文實質片段「**來源證據界線**：GitHub commit/檔案 blob SHA 不是 Windows process PID、loaded hash、Owner grant、Issuer Permit 或 Native Runner 調用；本輪已保存 local HEAD/index/untracked 原始輸出；只對實測工作樹作判斷。所有 Repo patch 須有現役 Owner 的 exact WriteSet/DE」；Parent=`L28:## 四庫 2026-10-30 `main` 原始碼錨定（GitHub 唯讀）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不能`。本章觸發/Consumer=HGK original Registry/Issuer/SharedSpine；承接 `WP 03/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH18.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0066`** `[SOURCE:FHS-BODY-03:L52:sha256=58628861e63956ae]`：原文實質片段「/ PD→OPS ECP / Host Owner / separate Host effect, permit, TTL, epoch, nonce / HGK 原 Host Ops Receiver / DEV token as OPS /」；Parent=`L44:## R2 Receiver-to-Producer、實效及授權型別（不取代原 ABI）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=HGK original Registry/Issuer/SharedSpine；承接 `WP 03/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH18.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0067`** `[SOURCE:FHS-BODY-04:L36:sha256=a7d54bdeb9129e7e]`：原文實質片段「/ SBL/sbl_core/modes.py / ack_signature(issuer,permit_id,subject_id,key) HMAC length-prefixed；_ack_state() 驗三欄＋Issuer Allowlist/secret / HMAC 作 ModeGate 初篩可以保留，真正 Effect 仍交原 HGK Receiver 檢 Scope/Epoch/TTL/Opera」；Parent=`L26:### 4.1 本次實查 Source 摘要（不要把假想方法寫成 HGK API）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不得`。本章觸發/Consumer=HGK original Registry/Issuer/SharedSpine；承接 `WP 03/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH18.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0068`** `[SOURCE:FHS-BODY-04:L44:sha256=a7d54bdeb9129e7e]`：原文實質片段「3. **Execution Flow**：PIPD PD/DEV/OPS ECP→原 HGK WorkOrder/Permit/Lease→Hermes pinned Profile+Worker；原 Worker/Tool 只執 exact OperationSemanticID/WriteSet/HostTarget；返回 Native Raw；若無實際 Issuer/launcher ABI 只能 ADMIS」；Parent=`L40:### 4.2 五條正式 Typed Adapter Flow：Input/Producer→輸出→Consumer、正負例`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:若無`。本章觸發/Consumer=HGK original Registry/Issuer/SharedSpine；承接 `WP 03/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH18.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0069`** `[SOURCE:FHS-BODY-04:L55:sha256=a7d54bdeb9129e7e]`：原文實質片段「/ ADMISSION / HGK 原 Issuer/Receiver 證 Permit/TTL/Nonce/Subject/Operation/WriteSet / ADMITTED（原 State Enum 讀值，不自造） / Foreign/Stale/Replay/OutScope→DENIED，不 Spawn /」；Parent=`L48:### 4.3 Native E2E 自主執行狀態機：Actor、事件、Fence、Unknown Effect、補償`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=HGK original Registry/Issuer/SharedSpine；承接 `WP 03/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH18.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。

### F.2 本章 WP 與 Producer／typed I/O／FirstFail（每項獨立）

- **WP-FHS-03**：Producer=HGK Original Registry/Issuer/Receiver；Input=原 HGK Registry、OS PID/SID、scope/nonce/TTL/ProcessACL/PolicyEpoch，非 Maker credentials；Output=IssuerReceiverBinding+original typed refusal/ACK; no self-issued Permit；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=HGK Registry / Issuer 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=用不同 PID/SID、過期 nonce、重用 TTL 或 scope widening 要求原 Issuer 放行；EDGE=在授權後 Worker PID 重啟；原 Receiver 必以新 process ACL / nonce 再認，不借舊票；FirstFail=`HGK_ISSUER_ACL_NONCE_TTL_NACK`；rollback=原 HGK Owner revoke affected grant/expire nonce, readback remaining WorkIDs，不清全域 Registry。
- **WP-FHS-17**：Producer=原 HGK Issuer+Host Installer/Capability Registry；Input=NeedKey+scope、原 Policy Loaded ACK+HGK Issuer admitted installer+license/asset digest；Output=Needed Capability 之 Installed/Loaded/Invoked/ConsumerACK+last-good，NONE=CAPABILITY_GAP_HOLD；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=CAP-BOOT Native Occupants 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=未有原 Issuer/Asset provenance 卻執行 Host installer；或第二套 Queue/Issuer 被包進工具；EDGE=Installer 解壓成功但載入失敗，需回上版 qualified last-good，不可把 Installed 當 Active；FirstFail=`CAP_INSTALLER_ORIGIN_PARTIAL_ROLLBACK`；rollback=原 installer inverse/restore manifest+LoadedSHA+residue；不得 Git revert 取代 Host inverse。

### F.3 複合原義拆解、反向閉包與受影退出

- **「各有」**：本 CH 的每個原 clause locator 各自保留 SourceSHA/Parent/OriginalConsumer、POS/NEG；若原文有多個 named roles/Host/Case，不可用單一結果冒全數。
- **「分別」**：strict JSON body／@2 sidecar、Original Policy Active／Host Loaded、Maker challenge／Protected Checker、Selected／ActualServed 是不同欄位與收據，不得合併。
- **「對應」**：必 `original source line → SCL-W1 id → CH → W1 WP → expected Case → original source line` 可機械重算；原 OriginalID 未明者只引用明示的 SourceSpan，不可猜 ID。
- **「不得／若／除非」**：否定作用域保留到原 Parent context；本章只標作者候選，原 Source Reader 取得 ACK 才能宣告原語義接受。
- **退出**：原 Reader NACK 僅 PARK 本章受影的 PI/PD/DEV/OPS/Host operation；合法 SOURCE_READ、隔離草稿及不依賴該 ABI 的 W0/W2 工作照原許可前進。

## 本章 L2-r4 設計義務接收卡（逐 ID；不可省略原 NEG）

- `INT-05` (`L1-r4:L773`, `L2-r4:L319`)：一個 HGK 控制平面；沿用 HGK 原 WorkID/Issuer/CAS/SharedSpine/World；[CH-18](#ch-18)；POS `沿用 HGK 原 WorkID/Issuer/CAS/SharedSpine/World`；NEG/FirstFail `生成第二 HGK Issuer／Queue／SharedSpine；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `HGK Original Issuer/SharedSpine/Protected Checker Reader`；本輪只有 EXPECTED_NOT_OBSERVED。
- `FHS-DR-031` (`L1-r4:L828`, `L2-r4:L369`)：治理／B/PROTECTED；HGK 是唯一 Work/Issuer/SharedSpine/World 權威；原 WorkID/Scope/TTL/Nonce/CAS 與有效 OS ACL；[CH-18](#ch-18)；POS `真原 Issuer admission + world state`；NEG/FirstFail `Human Owner 只有一人→普通 Agent 有 admin Token；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `HGK Original Issuer/SharedSpine/Protected Checker Reader`；本輪只有 EXPECTED_NOT_OBSERVED。
- `FHS-DR-032` (`L1-r4:L829`, `L2-r4:L370`)：治理／B/PROTECTED；不同技術 Principal 不能被 GPT persona 假造；runtime user SID 與維護 Token 實際隔離；[CH-18](#ch-18)/[CH-39](#ch-39)；POS `直接修改 HGK 的一般 Profile 被拒`；NEG/FirstFail `兩個 Hermes Profile 名稱即宣稱 OS 隔離；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `HGK Original Issuer/SharedSpine/Protected Checker Reader`；本輪只有 EXPECTED_NOT_OBSERVED。

## CH-18 專屬退出與回退

DraftMaker 後續須填 `original_reader_ref`, `original_schema_version_or_HOLD`, `source_span_sha`, `same_subject_and_scope`, `Case/Oracle`, `positive_raw_expected`, `negative_raw_expected`, `first_fail`, `resume_predicate`, `last_good`, `consumer_ack_or_HOLD`。`DOC_AUTHOR_DONE` 是本檔可檢索，不是 `HG-KSEOS 唯一 Native Issuer／SharedSpine／WorkID／許可` 已原 Host Qualified。若權限／能力尚缺，只 PARK 受影操作；回退到該 Domain 上次有效 Reader/Host 版本、保留跨波合法 READ/DRAFT，且不得刪原 NEG 或憑此文件自簽。



## AUTHOR-FINAL｜CH-18 受影交付契約

**Input / Operation / Output**：保留本章原有專屬 I/O、原句與 NEG；以當期 Registry 對同 SourceSHA/Subject/Scope 重算受影子圖，輸出 CH-18 的原 Reader BindingRequest，實質輸出與業務 FirstFail 以本章上文專屬契約及下列子義為準。

**Original Reader / Original Consumer**：HGK Original Issuer/SharedSpine/World Reader；原 Consumer Raw=EXPECTED_NOT_OBSERVED。L1 起始 1742、終止 1822，section SHA `8b6af3908e5fe75c0eec39314232dd0a80367be74408c0cb6ff62a988076d97e`。

**POS / NEG / FirstFail**：本章專屬正負條件逐筆如下；沒有適用子義的跨 ABI 章以原本章完整 POS/NEG 為準，不從別章借用 PASS。**EDGE**：SourceSHA/Host/PolicyEpoch 其中一欄改變，只 invalidate 受影接線；**SEC**：Maker 假 ACK 或跨 Principal 原回條均拒收。**ExpectedRaw**：同 Subject/Candidate/Scope 原 Consumer/World bytes；本輪 NOT_RUN。**Stop**：缺該 Effect 必需原 Reader 即 PARK 其效果；**Resume**：同 Scope 原 Reader 提供具名 Raw；**NextWave**：W2 原 Effect Receiver，四 Host/Cell/W18 交 W3，CI/Publisher 交 W4。

- `S-W1-INT-05-01`：Input=全系統只有原 HGK Issuer 有權建立 WorkID/Permit；POS=相同原 WorkID+Issuer ACK 可讀；NEG=新影子 Issuer 自簽 Permit；FirstFail=`SHADOW_ISSUER_DENY`；Consumer=HGK original Issuer/SharedSpine Reader；Case=`AUTHOR.W1.INT-05.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-05-02`：Input=原 Journal/Queue/CAS 與 SharedSpine 唯一且可恢復；POS=相同 WorkID 游標跨重啟恢復；NEG=新 SQLite queue 取代原 SharedSpine；FirstFail=`SHADOW_QUEUE_DENY`；Consumer=HGK original Issuer/SharedSpine Reader；Case=`AUTHOR.W1.INT-05.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-05-03`：Input=Protected Checker 與 Maker 不可共用獨立資格；POS=同 Subject 不同 principal 原 Checker Raw；NEG=Maker 自核准 Protected PASS；FirstFail=`SELF_ATTESTED_CHECKER_NACK`；Consumer=HGK original Issuer/SharedSpine Reader；Case=`AUTHOR.W1.INT-05.03.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-031-01`：Input=原 HGK Writer/Issuer/SharedSpine 唯一；POS=真 Issuer 發 same Scope grant；NEG=普通 agent 模擬新 Permit；FirstFail=`SHADOW_ISSUER_DENY`；Consumer=HGK original Issuer/Receiver/World Reader；Case=`AUTHOR.W1.FHS-DR-031.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-031-02`：Input=OS SID/nonce/TTL/Scope/PolicyEpoch 綁同一效力；POS=原 Receiver 驗新 PID/epoch；NEG=過期 nonce/跨 PID/Scope reuse；FirstFail=`HGK_ISSUER_ACL_NONCE_TTL_NACK`；Consumer=HGK original Issuer/Receiver/World Reader；Case=`AUTHOR.W1.FHS-DR-031.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-032-01`：Input=單人 Owner 不等於 Maker/Issuer/Checker 技術混權；POS=原 Host OS principle 不同且 ACL 有拒絕；NEG=建立兩個 Profile 名就算 OS 隔離；FirstFail=`OS_PRINCIPAL_SEPARATION_UNVERIFIED`；Consumer=HGK original OS ACL/Protected Checker Reader；Case=`AUTHOR.W1.FHS-DR-032.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-032-02`：Input=普通 Runtime 不可直接改 Protected Authority；POS=原 ACL deny 測例可重播；NEG=Maker 讀取並使用 Checker credential；FirstFail=`MAKER_CHECKER_CREDENTIAL_DENY`；Consumer=HGK original OS ACL/Protected Checker Reader；Case=`AUTHOR.W1.FHS-DR-032.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。

<a id="ch-19"></a>

# CH-19｜Hermes 三 Lane、模型路由、Profiles、ActualServed

### r2 受影修補（2026-11-05｜AUTHOR_FINAL_AFFECTED_REPAIR）

**受影 Finding**：`N-03、F-12`。**原位差額**：Picker Selected ≠ ActualServed：RequiredSet、Provider Served、Runtime PID、Host Loaded 分欄；七痛點的 native FUO 全列 `EXPECTED_NOT_OBSERVED`。

**未變更**：本章 H1 標題、L1 span／section SHA、OriginalID／Parent／NEG 與原 Reader 法位皆不變；原域 Raw 未取得者維持 `EXPECTED_NOT_OBSERVED`，不以作者推斷補值。

**下一個 Reader**：Original Host Runtime；FirstFail 見本章 POS／NEG／SEC 卡與 `AFFECTED_FINDINGS.jsonl` 對應列。

## W1 草案當期完成契約｜CH-19（DRAFT-W1-CH19）

**使用者可得結果**：Hermes 三 Lane / Profiles / ActualServed；合法執行範圍限 `SOURCE_READ` 與作者端規格審閱，無真 Host 准入或新 Writer 權限。

| 受影型別 | 本章可驗證的確定規則 |
|---|---|
| Input／觸發 | v0.22.5 pinned、普通 Goal、fresh PID/profile SHA、per-lane Required/Selected/Invoked/ActualServed；強制 `subject_id/source_manifest_sha/scope` 來源釘選 |
| 操作／Producer | 透過原 ProfileLoader/dispatcher 寫三 Lane model/provider selection 的候選規格；Observe≠Invoked，Token/Provider 變更要重新讀 ActualServed；Producer＝W1 DraftMaker（僅文字/Sidecar），正式效果由原域 Producer 執行 |
| Output／交付 | LaneRoutingDraft、per-lane ActualServedExpectation、ProfileLoadProbe；所有未觀測 Reader Raw 留空並具名 `EXPECTED_NOT_OBSERVED` |
| Original Reader | 原 Hermes Host Profile/Provider Reader；原 Writer／Issuer／Checker 不因本稿改權 |
| Downstream Consumer | HGK Journal+Lane/RunBudget（W2），W18 UAT（W3）；綁同 Subject／Scope，需 Original ACK 才可升級 |
| POS／Expected Raw | 三 Lane 有各自 Request/Served Raw、模型 fallback 可追溯；預期由原 Consumer 返回原格式 Raw（本輪 `NOT_RUN`） |
| NEG／首拒收 | 僅設定 profile 就聲稱 provider 真執行；FirstFail=`HERMES_PID_PROFILE_SERVED_HOLD` |
| EDGE | ProviderOff raw ON/OFF 語義未經 Host Owner 解釋；只 PARK 受影 scope，合法 READ/DRAFT 不受波及 |
| SEC | 用未測插件改寫原模型路由；缺憑證、Owner、ACL 或 Checker 證物拒效果 |
| Stop／Resume／Rollback | 遇 `HERMES_PID_PROFILE_SERVED_HOLD` 記 `hold_id+original_reader+required_raw`，停止受影寫入；Resume 需同 SourceSHA/Scope 的原 Reader 結果；READ 丟棄快照、DRAFT 刪除隔離候選；世界效果不在 W1 自行 rollback |
| Cross-wave | W2 受影 Runtime；W3 W18；交 `AUTHOR.FHS.W1ToW{next}@design` typed envelope，禁止偽裝 WorkOrder |

**受影源句拆義**：`actor/trigger/action/object`（見 Input/操作）；`condition/exception`（見 EDGE）；`prohibition`（見 NEG/SEC）；`outcome/consumer`（見 Output/Original Reader）；`POS/NEG/FirstFail` 必綁同一原 RequirementID。來源的原始句、Span、SHA、Parent/Child/NEG 以 r5 本章及附錄 `obligation_registry.jsonl` 回指；缺具體原 Reader 即 `ORIGINAL_OWNER_HOLD`，不自行創造簽核。


### R5 本章受影精確契約／業務負例（整合 r4，非歷史附錄）

PLAN/EXECUTE/VERIFY_SECURITY 三 Lane 的 RequiredSet、Selected、Invoked 與 ActualServed 每一條分記；真 Provider Raw/usage/response/tool turn 才能證 ActualServed。NEG=Picker Selected 冒 ActualServed → `ACTUAL_SERVED_MISSING`；Host PID/ProfileSHA 不在同 Scope → HOLD。


**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L1823–1901`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Hermes Original Host / Lane Reader；L2-r4:L909。原 Domain Reader/Writer 不因本章轉移。

## r4 當期受影修補（直接摘取 L1 r4 本章有效增量）

## r4｜AUDIT r3 受影整合／覆蓋／取代（現行作者端規範）

**Hermes v0.22.5 pinned baseline**：PLAN/EXECUTE/VERIFY_SECURITY 每 Lane 依原 Policy `required→selected→actual_served`，證 `profile_hash, process_PID, prompt_delivered, API_mode, request/response Raw, model/provider origin, token/usage, error/retry`; `selected`/`configured` 不是 `served`。Managed Worker cross-profile 不可繞 frozen profile guard；若 Win/Kanban Worker bound but prompt not delivered，停受影 Worker 並用原 Runtime 修復/回退，不得由工具選單猜測。外部較新版 release 僅更新候選，不自動改 v0.22.5。

## r4 對齊之 W1 主波操作規格、草案必填欄、逐項 POS/NEG／FirstFail（高保留整合）

**Protected Original H1 / CURRENT L1-r4**：`FHS_PIPD-LS-PKG_藍圖_2026-11-04_r4_HIGH_RETENTION_AUDIT_REPAIRED_實質正文(1).md:L1823–L1901`；`source_file_sha256=cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`；`section_sha256=2528bc824fca3ddf011611092731f2527c6d0ab139d591c576fd85cbc3611827`；`heading_exact=# CH-19｜Hermes 三 Lane、模型路由、Profiles、ActualServed`；**HISTORICAL_LOCATOR_NOT_EFFECTIVE**=`L1:1278–1328` / `L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`，L2 作者端路由 `L2:657`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W1 不取得原 Writer。

## A. 本章實質功能與不能壓平的原義

Hermes v0.22.5 三 Lane 真模型調用需要 Required／Selected／Invoked／ActualServed 四欄。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。

## B. 來源 r5 skeleton 必填核對欄（已由上方 W1 草案當期完成契約受影回填）

| 必填欄 | 欄位設計／不可空條件 |
|---|---|
<!-- HISTORICAL_R5_SKELETON_FILL_REQUEST_SUPERSEDED: transition wording only; all substantive constraints retained -->
| `chapter_id` / `primary_wave` / `author_writer` | `CH-19` / `W1` / `W1:DraftMaker`（歷史 r5 階段欄；當期為作者端定案候選） |
| `original_sources[]` | 本章 L1 行與下面原冊 SHA／OriginalClause Span；不得用語義假定的 ID 補空缺 |
| `same_subject` / `candidate_sha` / `source_manifest_sha` / `affected_scope` | 必攜相同 Subject/Scope，未原 Reader 認證則 `AUTHOR_CANDIDATE` |
| `effect_class` / `original_owner` / `consumer_abi` / `schema_version` | 依 Operation Reader；缺 `$id` 或 Receiver 不自造 |
| `input` / `typed_output` / `fuo` / `non_goals` | 應有真使用者結果與 Receiver（非檔案數） |
| `positive_fixture` / `negative_fixture` / `security_fixture` | 原 Source Case/Oracle 逐受影引用，未有 Runner/Raw 就 `EXPECTED_NOT_OBSERVED` |
| `first_fail` / `hold` / `stop_scope` / `resume_predicate` | 明確停止受影子圖，不全域凍結 READ／DRAFT |
| `rollback` / `w2_handoff` / `original_ack_nack` | 回退路由與 same scope 的預期接收；不得填假 PASS |

## C. Input → Producer → 原 Reader／Consumer → Output

- **Input/Guard**：profile_sha、fresh_pid、provider/model request、Original Lane raw、host version。
- **Producer**：該 Original Domain 的 Reader/Compiler/Host/Guide 依本章功能生產；W1 Curator 僅記設計；**Original Consumer**：Hermes original Host/Lane Reader；HGK Receiver。
- **Typed Output/FUO**：每 Lane raw trace + profile installed/loaded/trigger/invoke；否則 HOST_PENDING。
- **版本要求**：至少 `Subject,CandidateSHA,SourceSHA,OriginalID+SourceSpan,Scope,Host/PolicyEpoch（受影才填）,ABI $id/version,OriginalReader,OutputRawExpected`，少一欄只停需該欄的出口。

## D. POS／NEG／FirstFail／HOLD／退出

- **POS（期待）**：有真 LLM response 與 tool roundtrip 的同一 Lane identity。
- **NEG／SEC（期待拒收）**：Selected 模型自稱 ActualServed／跨 Lane 借值。
- **FirstFail**：`ACTUAL_SERVED_MISMATCH`；禁止只有泛稱 `VALIDATION_FAILED` 而不給首次失敗位置。
- **HOLD/Owner**：`H-LANE-06；本輪無 Windows Host`。需同 Subject/Scope/Host/原 Reader 的真 Raw/ACK 解除；本輪 `NOT_RUN`。
- **Stop/Resume**：保留原 SourceSHA/受影 Reader/cursor/last-good；READ/DRAFT 合法部分繼續；UNKNOWN 必原 Reader reconcile。
- **Rollback**：只回復該 Need/Host 的原 last-good，Host/OPS 效果走原 inverse；不得以檔案 ZIP 作回復收據。

## E. 來源追溯、波次邊界與下一手

| 源鍵／檔案 | 原文 SHA | 此 W1 處理方式 |
|---|---|---|
| SBL-DOC-03 | ea69e1d3718ed86aecd74a3ebcc933960eacc30b586ab80fcb9f733037e33476 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| SBL-DOC-06 | 64ea4977dab3093301f82dc7469413cc754998fc53946467842e06d83645102b | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-06 | 6bc5de0d26c8d13f4227ac9b48a66b808af0eb1108dc3012941e9c0c1ee362d5 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-10 | 13b0764732bc1501e7c823b12be0d0be3a54afdaec5f77a5e90111c1947fa70a | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
W0 提供原 Source/三 SPEC/索引；本 `CH-19` 不修改 W0 成果。W1 WaveCurator 交 W1 DraftMaker 按原 Reader 定位填入真 Requirements；W2 僅領同 Subject/Scope 的需要的 Effect/Case/HOLD，不得借 W3/W4 收據。原 L1 CH-19 的詳細原義仍在 L1 主體，不移作本冊第二 Canonical。

## F. r2 原位修補：CH-19 可直接交接的受影實質規格（非證據附錄）

**本章不可壓平功能**：Hermes actual served / profile / three lanes。與 W0 三份獨立 SPEC 維持同 SourceSHA/Subject/Scope；將原讀者真接收的 **Output／Consumer** 優先於填滿文件欄位。依 L1 原 CH 身份與 L2 W1 主責修訂，不移轉原 Writer。

### F.1 原句→原 Consumer→本章測例的逐子義槽（已從原物理檔定位）

- **`SCL-W1-0070`** `[SOURCE:SBL-DOC-03:L3917:sha256=ea69e1d3718ed86a]`：原文實質片段「/ FX-U-U19.1-POS/NEG / POS：對 U19.1 提交真實同 Parent 前置/對應來源/合法 Host，驗收「Commander 產出可貼入本地 Hermes 的版本化薄 Prompt，其內容為受限工作單指針與拒收／停機條件，不含影子授權」，比對受影欄位輸出及原生不變量；CHILD_SPECIFIC_DESIGN_ORACLE需另通過 Parent 合取判斷 / NEG：只改 U19.1 所要」；Parent=`L3861:## R08.1｜每個 U 子項的 POS/NEG 族（149 獨立鍵；見 R03 精確行）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG,不能,不得`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 04/20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH19.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0071`** `[SOURCE:SBL-DOC-03:L3925:sha256=ea69e1d3718ed86a]`：原文實質片段「/ FX-U-U22.2-POS/NEG / POS：對 U22.2 提交真實同 Parent 前置/對應來源/合法 Host，驗收「Profile 路由 WorkOrder/Handoff 必須有合法 gate 和拒收/重試政策」，比對受影欄位輸出及原生不變量；CHILD_SPECIFIC_DESIGN_ORACLE需另通過 Parent 合取判斷 / NEG：只改 U22.2 所要求的行為/輸出/權界，令「Pro」；Parent=`L3861:## R08.1｜每個 U 子項的 POS/NEG 族（149 獨立鍵；見 R03 精確行）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG,不能,不得`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 04/20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH19.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0072`** `[SOURCE:SBL-DOC-03:L3988:sha256=ea69e1d3718ed86a]`：原文實質片段「/ FX-U-U42.5-POS/NEG / POS：對 U42.5 提交真實同 Parent 前置/對應來源/合法 Host，驗收「Agent OS 輸出是高風險 Profile，缺 Native Runtime/Permit 時明確 UNSUPPORTED」，比對受影欄位輸出及原生不變量；CHILD_SPECIFIC_DESIGN_ORACLE需另通過 Parent 合取判斷 / NEG：只改 U42.5 所要求」；Parent=`L3861:## R08.1｜每個 U 子項的 POS/NEG 族（149 獨立鍵；見 R03 精確行）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG,不能,不得`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 04/20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH19.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0073`** `[SOURCE:SBL-DOC-06:L751:sha256=64ea4977dab30933]`：原文實質片段「/ NOBJ-015 / OpenAI plugin-creator / FALLBACK_ONLY / SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope;  / SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L337 @sha256:83ea1bef8d045bf0…; up」；Parent=`L731:### C33.2.9｜386/386 OriginalIdentity 逐筆 AdmissionDecision@2 擴充欄（不可與原處置相混）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 04/20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH19.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0074`** `[SOURCE:SBL-DOC-06:L869:sha256=64ea4977dab30933]`：原文實質片段「/ P0-TOOL-025 / Model Context Protocol / upstream=PRIMARY_ADAPTER / components.tool_gateway; disposition=DEFAULT_ENABLED_AFTER_QUALIFICATION; observed=TARGET_CONTRACT_DEFINED / OBSERVED_NOT_INSTALLED; runtime=N」；Parent=`L731:### C33.2.9｜386/386 OriginalIdentity 逐筆 AdmissionDecision@2 擴充欄（不可與原處置相混）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 04/20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH19.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0075`** `[SOURCE:SBL-DOC-06:L878:sha256=64ea4977dab30933]`：原文實質片段「/ P0-TOOL-034 / Sub-Agent / upstream=CORE / control.scoped_child; disposition=DEFAULT_ENABLED_AFTER_QUALIFICATION; observed=TARGET_CONTRACT_DEFINED / OBSERVED_NOT_INSTALLED; runtime=NOT_EXECUTED / SOURCE_DISPOS」；Parent=`L731:### C33.2.9｜386/386 OriginalIdentity 逐筆 AdmissionDecision@2 擴充欄（不可與原處置相混）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 04/20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH19.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0076`** `[SOURCE:FHS-BODY-06:L35:sha256=6bc5de0d26c8d13f]`：原文實質片段「/ EXECUTE / Hermes 真 Loaded Profile＋Worker PID/ModuleSHA/ActualServed；Coder Tool ACL 由原 Receiver / 僅 exact Scope 操作，Raw 附 OperationRef / 子代理繼承 Toolset 不等於新 Permit；超 scope DENY /」；Parent=`L25:### 4.3 Native E2E 自主執行狀態機：Actor、事件、Fence、Unknown Effect、補償`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 04/20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH19.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0077`** `[SOURCE:FHS-BODY-06:L76:sha256=6bc5de0d26c8d13f]`：原文實質片段「**流程**：讀原 Fabric Active→Loaded→Consumed Policy epoch 與原 HGK lane route／SharedSpine；原 Plan Writer CAS 產 task dependency；在真 effect 之前才讀 original Issuer Permit、驗 WorkID,subject,candidate_sha,scope,lease_generation」；Parent=`L72:## R2 單 WorkID 自主閉環／World Reconcile 演算法（原 Hermes Queue）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 04/20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH19.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0078`** `[SOURCE:FHS-BODY-06:L94:sha256=6bc5de0d26c8d13f]`：原文實質片段「READY>0 時 wake 只送原 Hermes wake endpoint。ACK 需 cursor/revision，Worker startup Raw 需新 PID、process origin、loaded profile、lease generation。wake timeout 可重送同 idempotent wake event，不可把效果一起重播。restart 由原 Journal cursor」；Parent=`L88:## R2-06-REDUCER：proposal 到原 HGK 狀態的讀取契約`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不可,不能`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 04/20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH19.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0079`** `[SOURCE:FHS-BODY-10:L34:sha256=13b0764732bc1501]`：原文實質片段「**Windows／Host/UI**：Hermes CLI/Windows Host 原 Process/Skill Loader 先用真 Loaded Module；Codex、Claude Code、ChatGPT 各依原 Host Capability 做不同 Install/Invoke/Permission 的 POS+NEG；Windows App SDK/WinUI 3/Named Pipe/AG-U」；Parent=`L30:### 4.5 知識與記憶、Windows／桌面、CI 安全三條既有 Consumer 路線`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 04/20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH19.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0080`** `[SOURCE:FHS-BODY-10:L47:sha256=13b0764732bc1501]`：原文實質片段「/ E33 / fresh Hermes PID + ordinary goal / 自動選原 effective profile，無 B1 Prompt / 需要重貼長 Prompt → NORMAL_BOOTSTRAP_FAIL / NOT_RUN /」；Parent=`L43:## R2 W18：E33–E42 真使用者普通 Goal 驗收矩陣（不是通用 PASS）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 04/20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH19.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0081`** `[SOURCE:FHS-BODY-10:L66:sha256=13b0764732bc1501]`：原文實質片段「NormalModeLaunchContract 是原 Hermes startup/default-profile Reader 的設計契約，不新建 launcher。輸入 ordinary_goal、fresh_session_id、原 default_profile_sha、既有 admitted work refs（可空）；output 為 pid/start_time/process_origin/load」；Parent=`L64:## R2-10-NORMAL：新 PID、普通 Goal、零 B1 專用 Prompt`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不能`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 04/20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH19.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0151`** `[SOURCE:FHS-BODY-09B:L19:sha256=aed2234821768307]`：原文實質片段「### CELL-d0cf30ffd7c1｜CLI_TOOL/STANDALONE｜Hermes Agent｜legacy=ON」；Parent=`L14:## 7. SBL 192 個 Kind×Mode×Host×Provider Legacy Cell：逐 Cell 生效行為`；原 ID=`CELL-d0cf30ffd7c1`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CELL.SELECTED_SCOPE_ONLY`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0152`** `[SOURCE:FHS-BODY-09B:L33:sha256=aed2234821768307]`：原文實質片段「### CELL-e8a4077d37ad｜CLI_TOOL/STANDALONE｜Hermes Agent｜legacy=OFF」；Parent=`L19:### CELL-d0cf30ffd7c1｜CLI_TOOL/STANDALONE｜Hermes Agent｜legacy=ON`；原 ID=`CELL-e8a4077d37ad`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CELL.SELECTED_SCOPE_ONLY`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0155`** `[SOURCE:FHS-BODY-09B:L243:sha256=aed2234821768307]`：原文實質片段「### CELL-68f927602c56｜CLI_TOOL/SWOF_CONNECTED｜Hermes Agent｜legacy=ON」；Parent=`L229:### CELL-fabd535f6b8d｜CLI_TOOL/PREW3_SHADOW｜DeepSeek Harness｜legacy=OFF`；原 ID=`CELL-68f927602c56`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CELL.SELECTED_SCOPE_ONLY`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0156`** `[SOURCE:FHS-BODY-09B:L257:sha256=aed2234821768307]`：原文實質片段「### CELL-09a9c6d13bb7｜CLI_TOOL/SWOF_CONNECTED｜Hermes Agent｜legacy=OFF」；Parent=`L243:### CELL-68f927602c56｜CLI_TOOL/SWOF_CONNECTED｜Hermes Agent｜legacy=ON`；原 ID=`CELL-09a9c6d13bb7`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CELL.SELECTED_SCOPE_ONLY`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0159`** `[SOURCE:FHS-BODY-09B:L355:sha256=aed2234821768307]`：原文實質片段「### CELL-b368d7497e83｜AGENT_SKILL/STANDALONE｜Hermes Agent｜legacy=ON」；Parent=`L341:### CELL-5bd80e6cf274｜CLI_TOOL/SWOF_CONNECTED｜DeepSeek Harness｜legacy=OFF`；原 ID=`CELL-b368d7497e83`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CELL.SELECTED_SCOPE_ONLY`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0160`** `[SOURCE:FHS-BODY-09B:L369:sha256=aed2234821768307]`：原文實質片段「### CELL-a488c020ca0b｜AGENT_SKILL/STANDALONE｜Hermes Agent｜legacy=OFF」；Parent=`L355:### CELL-b368d7497e83｜AGENT_SKILL/STANDALONE｜Hermes Agent｜legacy=ON`；原 ID=`CELL-a488c020ca0b`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CELL.SELECTED_SCOPE_ONLY`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0163`** `[SOURCE:FHS-BODY-09B:L579:sha256=aed2234821768307]`：原文實質片段「### CELL-706d7dabb0a0｜AGENT_SKILL/SWOF_CONNECTED｜Hermes Agent｜legacy=ON」；Parent=`L565:### CELL-79aa1ca6c95f｜AGENT_SKILL/PREW3_SHADOW｜DeepSeek Harness｜legacy=OFF`；原 ID=`CELL-706d7dabb0a0`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CELL.SELECTED_SCOPE_ONLY`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0164`** `[SOURCE:FHS-BODY-09B:L593:sha256=aed2234821768307]`：原文實質片段「### CELL-aab24b0f82f9｜AGENT_SKILL/SWOF_CONNECTED｜Hermes Agent｜legacy=OFF」；Parent=`L579:### CELL-706d7dabb0a0｜AGENT_SKILL/SWOF_CONNECTED｜Hermes Agent｜legacy=ON`；原 ID=`CELL-aab24b0f82f9`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Hermes original Runtime/three-lane reader；承接 `WP 20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CELL.SELECTED_SCOPE_ONLY`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。

### F.2 本章 WP 與 Producer／typed I/O／FirstFail（每項獨立）

- **WP-FHS-04**：Producer=Hermes original Runtime/Journal + HGK SharedSpine；Input=Hermes v0.22.5 pin；ProfileSHA、WorkID、lease generation、run budget 原 Reader；Output=Fresh PID+LoadedProfileSHA+Raw三Lane Required/Selected/Invoked/ActualServed + JournalCursor；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=Hermes Durable Runtime 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=以過期 lease_generation 重播非冪等 WorkID 並把 Picker Selected 假稱 ActualServed；EDGE=worker crash 在 effect 之後/Raw 入帳之前：維持 UNKNOWN，必 original World Reconcile；FirstFail=`HERMES_LEASE_UNKNOWN_RECONCILE`；rollback=原 Journal 查 WorldRaw/last-good 再 Resume WorkID；UNKNOWN 禁盲重試。
- **WP-FHS-20**：Producer=Original SBL Product×Host Cell owner/Reader；Input=CellID+original Kind/Mode/Host/RawToken，Host Capability/Provider state 原 Owner 必須核對；Output=Selected/NotAffected/OwnerHold per Cell + raw Host-specific Consumer outcome；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=CLI/Agent/Host Kind Matrix 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=把 ON/OFF source token 私譯成 provider_off bool 或借不同 Host/Provider Raw；EDGE=Same Kind/Mode 從 Hermes 改到 Codex，原 Cell ID 改變；舊 Cell receipt 不可重用；FirstFail=`CELL_TOKEN_OWNER_MAP_UNBOUND`；rollback=撤受影 Host adapter/probe，恢復同 Need qualified last-good，保留 raw ON/OFF。

### F.3 複合原義拆解、反向閉包與受影退出

- **「各有」**：本 CH 的每個原 clause locator 各自保留 SourceSHA/Parent/OriginalConsumer、POS/NEG；若原文有多個 named roles/Host/Case，不可用單一結果冒全數。
- **「分別」**：strict JSON body／@2 sidecar、Original Policy Active／Host Loaded、Maker challenge／Protected Checker、Selected／ActualServed 是不同欄位與收據，不得合併。
- **「對應」**：必 `original source line → SCL-W1 id → CH → W1 WP → expected Case → original source line` 可機械重算；原 OriginalID 未明者只引用明示的 SourceSpan，不可猜 ID。
- **「不得／若／除非」**：否定作用域保留到原 Parent context；本章只標作者候選，原 Source Reader 取得 ACK 才能宣告原語義接受。
- **退出**：原 Reader NACK 僅 PARK 本章受影的 PI/PD/DEV/OPS/Host operation；合法 SOURCE_READ、隔離草稿及不依賴該 ABI 的 W0/W2 工作照原許可前進。

## 本章 L2-r4 設計義務接收卡（逐 ID；不可省略原 NEG）

- `FHS-DR-035` (`L1-r4:L832`, `L2-r4:L373`)：Runtime／B/LONG；Hermes v0.22.5 原能力優先使用；Direct→Delegate→Kanban→Swarm 依複雜度決定；[CH-19](#ch-19)/[CH-20](#ch-20)；POS `真 task result 有再續工`；NEG/FirstFail `簡單 Read 任務硬套多 Agent Queue；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `Original Domain Owner/Reader (scope binding pending)`；本輪只有 EXPECTED_NOT_OBSERVED。
- `FHS-DR-036` (`L1-r4:L833`, `L2-r4:L374`)：Runtime／A＋B；3 正式 Lane 的模型 RequiredSet/Served 分開；PLAN/EXECUTE/VERIFY_SECURITY 受原有效 Policy 選模；[CH-19](#ch-19)；POS `同 Subject 每 Lane 真 Request/Served/Usage`；NEG/FirstFail `只選到 Picker 便宣稱 Protected Lane Served；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `Hermes original Runtime/Launcher/Provider Raw Reader → HGK Lane/Journal Consumer`；本輪只有 EXPECTED_NOT_OBSERVED。

## CH-19 專屬退出與回退

DraftMaker 後續須填 `original_reader_ref`, `original_schema_version_or_HOLD`, `source_span_sha`, `same_subject_and_scope`, `Case/Oracle`, `positive_raw_expected`, `negative_raw_expected`, `first_fail`, `resume_predicate`, `last_good`, `consumer_ack_or_HOLD`。`DOC_AUTHOR_DONE` 是本檔可檢索，不是 `Hermes 三 Lane、模型路由、Profiles、ActualServed` 已原 Host Qualified。若權限／能力尚缺，只 PARK 受影操作；回退到該 Domain 上次有效 Reader/Host 版本、保留跨波合法 READ/DRAFT，且不得刪原 NEG 或憑此文件自簽。



## AUTHOR-FINAL｜CH-19 受影交付契約

**Input / Operation / Output**：保留本章原有專屬 I/O、原句與 NEG；以當期 Registry 對同 SourceSHA/Subject/Scope 重算受影子圖，輸出 CH-19 的原 Reader BindingRequest，實質輸出與業務 FirstFail 以本章上文專屬契約及下列子義為準。

**Original Reader / Original Consumer**：Hermes Original Runtime/Provider Reader；原 Consumer Raw=EXPECTED_NOT_OBSERVED。L1 起始 1823、終止 1901，section SHA `2528bc824fca3ddf011611092731f2527c6d0ab139d591c576fd85cbc3611827`。

**POS / NEG / FirstFail**：本章專屬正負條件逐筆如下；沒有適用子義的跨 ABI 章以原本章完整 POS/NEG 為準，不從別章借用 PASS。**EDGE**：SourceSHA/Host/PolicyEpoch 其中一欄改變，只 invalidate 受影接線；**SEC**：Maker 假 ACK 或跨 Principal 原回條均拒收。**ExpectedRaw**：同 Subject/Candidate/Scope 原 Consumer/World bytes；本輪 NOT_RUN。**Stop**：缺該 Effect 必需原 Reader 即 PARK 其效果；**Resume**：同 Scope 原 Reader 提供具名 Raw；**NextWave**：W2 原 Effect Receiver，四 Host/Cell/W18 交 W3，CI/Publisher 交 W4。

- `S-W1-FHS-DR-035-01`：Input=Direct/Delegation/Kanban/Swarm 按複雜度；POS=小 read 直接處理無重啟；NEG=小 read 強制新多 Agent queue；FirstFail=`HERMES_OVERENGINEERING_NACK`；Consumer=Hermes original runtime Owner；Case=`AUTHOR.W1.FHS-DR-035.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-035-02`：Input=原 Queue/Journal/lease 原位恢復；POS=相同 WorkID JournalCursor/lease_generation；NEG=盲重播 UNKNOWN nonidempotent；FirstFail=`HERMES_WORLD_RECONCILE_REQUIRED`；Consumer=Hermes original runtime Owner；Case=`AUTHOR.W1.FHS-DR-035.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-036-01`：Input=PLAN/EXECUTE/VERIFY_SECURITY 分別保存 required/selected；POS=三 Lane 原 Policy 必需集合分立；NEG=Selected 便算 ActualServed；FirstFail=`ACTUAL_SERVED_MISSING`；Consumer=Hermes Provider Response and HGK Lane Reader；Case=`AUTHOR.W1.FHS-DR-036.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-036-02`：Input=真 provider response/usage/tool turn 才算 served；POS=同 Subject/PID/Invocation 真 response；NEG=拿不同 provider 的 raw 充用；FirstFail=`PROVIDER_RAW_FOREIGN_NACK`；Consumer=Hermes Provider Response and HGK Lane Reader；Case=`AUTHOR.W1.FHS-DR-036.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。

<a id="ch-20"></a>

# CH-20｜Hermes Native Kanban／Delegation／Swarm／長任務編排

### r2 受影修補（2026-11-05｜AUTHOR_FINAL_AFFECTED_REPAIR）

**受影 Finding**：`N-03、N-05`。**原位差額**：Kanban／Delegation／Swarm／Journal 以本機原能力為限；本輪建立原生看板並用原生委派，但不宣稱多 Host Swarm 或無人值守 E2E。

**未變更**：本章 H1 標題、L1 span／section SHA、OriginalID／Parent／NEG 與原 Reader 法位皆不變；原域 Raw 未取得者維持 `EXPECTED_NOT_OBSERVED`，不以作者推斷補值。

**下一個 Reader**：Original Host Runtime／Journal Reader；FirstFail 見本章 POS／NEG／SEC 卡與 `AFFECTED_FINDINGS.jsonl` 對應列。

## W1 草案當期完成契約｜CH-20（DRAFT-W1-CH20）

**使用者可得結果**：Hermes Kanban / Delegation / Swarm；合法執行範圍限 `LOCAL_DRAFT_WRITE` 與作者端規格審閱，無真 Host 准入或新 Writer 權限。

| 受影型別 | 本章可驗證的確定規則 |
|---|---|
| Input／觸發 | Job Goal/WorkID/Capability、Owner preauth、RunBudget、resume cursor；強制 `subject_id/source_manifest_sha/scope` 來源釘選 |
| 操作／Producer | Direct→Delegation→Swarm 隨任務複雜度調度，優先原 Hermes Kanban/Journal；同 WorkID 只一 lease，Effect 動作入原 HGK Admission；UNKNOWN 從 World Reader reconcile；Producer＝W1 DraftMaker（僅文字/Sidecar），正式效果由原域 Producer 執行 |
| Output／交付 | Kanban/Delegation Plan、BoundedRetry/ResumePlan、failure cones；所有未觀測 Reader Raw 留空並具名 `EXPECTED_NOT_OBSERVED` |
| Original Reader | Hermes original Runtime/Journal Reader；原 Writer／Issuer／Checker 不因本稿改權 |
| Downstream Consumer | HGK WorkID/Lease Consumer、W2 EXECUTE；綁同 Subject／Scope，需 Original ACK 才可升級 |
| POS／Expected Raw | 斷線可用同 WorkID 恢復且不重放受保護效果；預期由原 Consumer 返回原格式 Raw（本輪 `NOT_RUN`） |
| NEG／首拒收 | 每次啟動一個新 FHS Queue/Native Issuer；FirstFail=`HERMES_RECONCILE_OR_BUDGET_HOLD` |
| EDGE | 長任務遇未知外界狀態先 PARK 受影項；只 PARK 受影 scope，合法 READ/DRAFT 不受波及 |
| SEC | 超 RunBudget、無主機准入持續自動重試；缺憑證、Owner、ACL 或 Checker 證物拒效果 |
| Stop／Resume／Rollback | 遇 `HERMES_RECONCILE_OR_BUDGET_HOLD` 記 `hold_id+original_reader+required_raw`，停止受影寫入；Resume 需同 SourceSHA/Scope 的原 Reader 結果；READ 丟棄快照、DRAFT 刪除隔離候選；世界效果不在 W1 自行 rollback |
| Cross-wave | W2 Runtime/Journal；W3 W18；交 `AUTHOR.FHS.W1ToW{next}@design` typed envelope，禁止偽裝 WorkOrder |

**受影源句拆義**：`actor/trigger/action/object`（見 Input/操作）；`condition/exception`（見 EDGE）；`prohibition`（見 NEG/SEC）；`outcome/consumer`（見 Output/Original Reader）；`POS/NEG/FirstFail` 必綁同一原 RequirementID。來源的原始句、Span、SHA、Parent/Child/NEG 以 r5 本章及附錄 `obligation_registry.jsonl` 回指；缺具體原 Reader 即 `ORIGINAL_OWNER_HOLD`，不自行創造簽核。


### R5 本章受影精確契約／業務負例（整合 r4，非歷史附錄）

Hermes v0.22.5 固定，Direct→Delegation→Kanban→Swarm 只按原 Need+complexity 選最低足夠原生方法；RunBudget 數值待 original Host Probe；原 WorkID、lease_generation、journal_cursor 與 last-good 恢復。NEG=effect 發出 receipt 未入帳之 UNKNOWN 盲重播 → `WORLD_RECONCILE_REQUIRED`。


**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L1902–1978`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Hermes Kanban/Delegation Reader；L2-r4:L910。原 Domain Reader/Writer 不因本章轉移。

## r4 當期受影修補（直接摘取 L1 r4 本章有效增量）

## r4｜AUDIT r3 受影整合／覆蓋／取代（現行作者端規範）

**Kanban/Delegation/Swarm Use-before-Build**：按普通 Goal 的最小 FUO：直接答覆/READ→必要時 bounded delegation→長任務 Kanban→確實需要多 Role 協作才 Swarm；所有共享原 Hermes Queue/Lease/Journal/WorkID，非原本能力不足不另建 scheduler。Worker 最小真值鏈 `queued→leased→prompt_delivered→LLM_request→actual_served→toolcall→world_raw→consumer_ack`，不可跳級；stop-loss/cost/retry cap/first_fail + resume 支援不監督長任務。

## r4 對齊之 W1 主波操作規格、草案必填欄、逐項 POS/NEG／FirstFail（高保留整合）

**Protected Original H1 / CURRENT L1-r4**：`FHS_PIPD-LS-PKG_藍圖_2026-11-04_r4_HIGH_RETENTION_AUDIT_REPAIRED_實質正文(1).md:L1902–L1978`；`source_file_sha256=cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`；`section_sha256=26461f88645fafe6c79c6853d21ff05b60cc06ba86e119d936329a5597c4b25b`；`heading_exact=# CH-20｜Hermes Native Kanban／Delegation／Swarm／長任務編排`；**HISTORICAL_LOCATOR_NOT_EFFECTIVE**=`L1:1329–1379` / `L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`，L2 作者端路由 `L2:658`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W1 不取得原 Writer。

## A. 本章實質功能與不能壓平的原義

Kanban／Delegation／Kanban Swarm／原 Runtime Job/Queue/Lease 不新造持久工作層。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。

## B. 來源 r5 skeleton 必填核對欄（已由上方 W1 草案當期完成契約受影回填）

| 必填欄 | 欄位設計／不可空條件 |
|---|---|
<!-- HISTORICAL_R5_SKELETON_FILL_REQUEST_SUPERSEDED: transition wording only; all substantive constraints retained -->
| `chapter_id` / `primary_wave` / `author_writer` | `CH-20` / `W1` / `W1:DraftMaker`（歷史 r5 階段欄；當期為作者端定案候選） |
| `original_sources[]` | 本章 L1 行與下面原冊 SHA／OriginalClause Span；不得用語義假定的 ID 補空缺 |
| `same_subject` / `candidate_sha` / `source_manifest_sha` / `affected_scope` | 必攜相同 Subject/Scope，未原 Reader 認證則 `AUTHOR_CANDIDATE` |
| `effect_class` / `original_owner` / `consumer_abi` / `schema_version` | 依 Operation Reader；缺 `$id` 或 Receiver 不自造 |
| `input` / `typed_output` / `fuo` / `non_goals` | 應有真使用者結果與 Receiver（非檔案數） |
| `positive_fixture` / `negative_fixture` / `security_fixture` | 原 Source Case/Oracle 逐受影引用，未有 Runner/Raw 就 `EXPECTED_NOT_OBSERVED` |
| `first_fail` / `hold` / `stop_scope` / `resume_predicate` | 明確停止受影子圖，不全域凍結 READ／DRAFT |
| `rollback` / `w2_handoff` / `original_ack_nack` | 回退路由與 same scope 的預期接收；不得填假 PASS |

## C. Input → Producer → 原 Reader／Consumer → Output

- **Input/Guard**：既有 admitted WorkID、queue cursor、lease gen、checkpoint、allowed delegation profile。
- **Producer**：該 Original Domain 的 Reader/Compiler/Host/Guide 依本章功能生產；W1 Curator 僅記設計；**Original Consumer**：Hermes runtime/Dispatcher/Bounded Worker。
- **Typed Output/FUO**：Wake/Resume/Stop/PromptDelivered/WorldRaw 的原 Runtime probe 規格。
- **版本要求**：至少 `Subject,CandidateSHA,SourceSHA,OriginalID+SourceSpan,Scope,Host/PolicyEpoch（受影才填）,ABI $id/version,OriginalReader,OutputRawExpected`，少一欄只停需該欄的出口。

## D. POS／NEG／FirstFail／HOLD／退出

- **POS（期待）**：重啟後不重複 effect 且可沿原 cursor 完成 tool turn。
- **NEG／SEC（期待拒收）**：WorkerBound 當 WorkerUsed、UNKNOWN blind retry、新建調度 DB。
- **FirstFail**：`RUNTIME_LEASE_BINDING_DENY`；禁止只有泛稱 `VALIDATION_FAILED` 而不給首次失敗位置。
- **HOLD/Owner**：`RUN_BUDGET_BIND_HOLD/H-LANE-06`。需同 Subject/Scope/Host/原 Reader 的真 Raw/ACK 解除；本輪 `NOT_RUN`。
- **Stop/Resume**：保留原 SourceSHA/受影 Reader/cursor/last-good；READ/DRAFT 合法部分繼續；UNKNOWN 必原 Reader reconcile。
- **Rollback**：只回復該 Need/Host 的原 last-good，Host/OPS 效果走原 inverse；不得以檔案 ZIP 作回復收據。

## E. 來源追溯、波次邊界與下一手

| 源鍵／檔案 | 原文 SHA | 此 W1 處理方式 |
|---|---|---|
| SBL-DOC-04 | ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| SBL-DOC-06 | 64ea4977dab3093301f82dc7469413cc754998fc53946467842e06d83645102b | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-06 | 6bc5de0d26c8d13f4227ac9b48a66b808af0eb1108dc3012941e9c0c1ee362d5 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-10 | 13b0764732bc1501e7c823b12be0d0be3a54afdaec5f77a5e90111c1947fa70a | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
W0 提供原 Source/三 SPEC/索引；本 `CH-20` 不修改 W0 成果。W1 WaveCurator 交 W1 DraftMaker 按原 Reader 定位填入真 Requirements；W2 僅領同 Subject/Scope 的需要的 Effect/Case/HOLD，不得借 W3/W4 收據。原 L1 CH-20 的詳細原義仍在 L1 主體，不移作本冊第二 Canonical。

## F. r2 原位修補：CH-20 可直接交接的受影實質規格（非證據附錄）

**本章不可壓平功能**：Hermes Kanban/Swarm/journal and unattended run。與 W0 三份獨立 SPEC 維持同 SourceSHA/Subject/Scope；將原讀者真接收的 **Output／Consumer** 優先於填滿文件欄位。依 L1 原 CH 身份與 L2 W1 主責修訂，不移轉原 Writer。

### F.1 原句→原 Consumer→本章測例的逐子義槽（已從原物理檔定位）

- **`SCL-W1-0082`** `[SOURCE:SBL-DOC-04:L910:sha256=ee90cb1c86f6f735]`：原文實質片段「4. 實際 install 需 Source admission → rights/legal scan → exact release/tag/commit/sha pin → lock transitive dependencies → host capability dry-run → minimal POS+NEG → effective load receipt → rollback/uninstall →」；Parent=`L905:### 05.1 MethodAdmissionLedger／具名安裝優先序`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG,不得`。本章觸發/Consumer=Hermes existing Kanban/Delegation/SharedSpine；承接 `WP 04/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH20.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0083`** `[SOURCE:SBL-DOC-04:L2399:sha256=ee90cb1c86f6f735]`：原文實質片段「- **TestInput**：{"case":"NEG-D04-JOIN-WRITE","subject_sha":"<compute exact bytes>","tamper":"KANBAN lanes both write src/api.py","candidate_status":"FROZEN_FOR_TEST"}。**Expected**：DENY/HOLD, FirstFail=JOIN_WRIT」；Parent=`L2396:### 07.12 `NEG-D04-JOIN-WRITE` 完整預期 Fixture`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG,不得`。本章觸發/Consumer=Hermes existing Kanban/Delegation/SharedSpine；承接 `WP 04/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH20.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0084`** `[SOURCE:SBL-DOC-04:L2729:sha256=ee90cb1c86f6f735]`：原文實質片段「R05.6 每張技術卡配 TechResearchDecision@1 {source_tag/full_commit_sha,source_readback_time,licence_spdx,NOTICE,SBOM,advisory_snapshot,host_compat_probe,ABI_input_output,contradicting_evidence,OwnerDecision,NoFit,Exit」；Parent=`L2727:### R09.2｜本次 20 槽逐項技術研究的合法驗證輸入（不偽造授權已定案）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NoFit,不得`。本章觸發/Consumer=Hermes existing Kanban/Delegation/SharedSpine；承接 `WP 04/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH20.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0085`** `[SOURCE:SBL-DOC-06:L651:sha256=64ea4977dab30933]`：原文實質片段「/ GPTB-KP10-R03 / L1773; MUST; Bind PR to tests and rollback / MUST → NONE → COMMANDER_ONLY / SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L710 @sha256:83ea1bef8d045bf0…; upstream HERMES  HG-KSEOS  Fabric：PRE-W3 → W」；Parent=`L565:### C33.2.LEGACY160｜160 條（原件原判＋新增非模板設計）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:禁止`。本章觸發/Consumer=Hermes existing Kanban/Delegation/SharedSpine；承接 `WP 04/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH20.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0086`** `[SOURCE:SBL-DOC-06:L774:sha256=64ea4977dab30933]`：原文實質片段「/ 354 / extra swarm framework / REJECT / NO_ACTIVATION; OWNER_CR_REQUIRED; positive: source+qualified scope; negative: fo / SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L371 @sha256:83ea1bef8d045bf0…; upstream R2 §8」；Parent=`L731:### C33.2.9｜386/386 OriginalIdentity 逐筆 AdmissionDecision@2 擴充欄（不可與原處置相混）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:neg,禁止`。本章觸發/Consumer=Hermes existing Kanban/Delegation/SharedSpine；承接 `WP 04/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH20.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0087`** `[SOURCE:SBL-DOC-06:L877:sha256=64ea4977dab30933]`：原文實質片段「/ P0-TOOL-033 / Agent Swarm / upstream=OPTIONAL / control.optional_bounded_swarm; disposition=MERGED_ALIAS_WITH_CANONICAL_ID; observed=ADMISSION_BLOCKED_IDENTITY_UNRESOLVED; runtime=NOT_EXECUTED / CONDITIONAL_O」；Parent=`L731:### C33.2.9｜386/386 OriginalIdentity 逐筆 AdmissionDecision@2 擴充欄（不可與原處置相混）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:neg`。本章觸發/Consumer=Hermes existing Kanban/Delegation/SharedSpine；承接 `WP 04/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH20.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0088`** `[SOURCE:FHS-BODY-06:L16:sha256=6bc5de0d26c8d13f]`：原文實質片段「1. **原接線**：Goal→原 TPM/PIPD/PLAN→原 Fabric/HGK admission→原 Hermes Queue/Lease/Journal→bounded Worker→原世界狀態 Reader→不同 Principal Protected Checker→原 Delivery/Publisher。安裝目錄的 hermes_cli/kanban_db.py 中 create_task/ge」；Parent=`L14:## HANDOFF-v1｜原 WorkID、Lease、Journal、UNKNOWN 與復原`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Hermes existing Kanban/Delegation/SharedSpine；承接 `WP 04/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH20.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0089`** `[SOURCE:FHS-BODY-06:L41:sha256=6bc5de0d26c8d13f]`：原文實質片段「**四個極端例子**：A 完成世界寫入但 ACK 遺失→B 新 PID 必以同 OperationSemanticID 從 Journal/World 認定 APPLIED，不得再呼叫一次；A Lease 已到期但後送 ACK→Fence 令其拒收，世界效果仍須 Reconcile；部分改檔→不以 Failed=NoEffect 直接重跑，進原 Compensation ECP；Provider quota→只有 O」；Parent=`L25:### 4.3 Native E2E 自主執行狀態機：Actor、事件、Fence、Unknown Effect、補償`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不得`。本章觸發/Consumer=Hermes existing Kanban/Delegation/SharedSpine；承接 `WP 04/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH20.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0090`** `[SOURCE:FHS-BODY-06:L78:sha256=6bc5de0d26c8d13f]`：原文實質片段「**Crash/Resume**：如果 operation intent 已寫、但 world result UNKNOWN，原 Reader **先 reconcile**，不得盲重試或重播 nonce；lease_generation/old PID fencing；valid Cursor 重啟只做受影差額，成功收據同 SHA 復用，不重問 KnownAnswer。」；Parent=`L72:## R2 單 WorkID 自主閉環／World Reconcile 演算法（原 Hermes Queue）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不得`。本章觸發/Consumer=Hermes existing Kanban/Delegation/SharedSpine；承接 `WP 04/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH20.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0091`** `[SOURCE:FHS-BODY-10:L7:sha256=13b0764732bc1501]`：原文實質片段「> **FHS-MSC_PIPD-LS-PKG / 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND / EFFECTIVE_DESIGN_READER**。本冊按同域來源整合 2026-10-29 BODY revision2 和 2026-10-30 r2 最新受影修補。R2 受影條款在本冊設計閱讀範圍優先於被修補之歷史片段；但不覆寫 SBL/PIPD」；Parent=`L5:# 10 B1 W18 SELF BOOTSTRAP｜FHS-MSC_PIPD-LS-PKG 2026-10-30 整合實質正文`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=Hermes existing Kanban/Delegation/SharedSpine；承接 `WP 04/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH20.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0092`** `[SOURCE:FHS-BODY-10:L36:sha256=13b0764732bc1501]`：原文實質片段「**Supply Chain**：原 CI 一個責任明確的 Build Pipeline 按 Scope 選：Gitleaks 受影 Secret Scan，CodeQL/Semgrep/Ruff/pytest 靜態／單測，Syft→CycloneDX/SPDX SBOM，Trivy/Grype/OSV 按實際 Consumer 做漏洞匹配，Cosign/SLSA/Artifact Attestation 記建置來源」；Parent=`L30:### 4.5 知識與記憶、Windows／桌面、CI 安全三條既有 Consumer 路線`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不能`。本章觸發/Consumer=Hermes existing Kanban/Delegation/SharedSpine；承接 `WP 04/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH20.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0093`** `[SOURCE:FHS-BODY-10:L68:sha256=13b0764732bc1501]`：原文實質片段「NM01：新目標 → TPM/SPEC→原 PIPD→合法 plan；NM02：既有 admitted work → 原 cursor resume，Owner 重問=0；NM03：provider-off/能力不足 → 正確 NOFIT 或離線合法 read，不能私換 provider。每條都用新 PID，禁止注入 B1 長 Prompt、手選 lane 或預填成功 receipt。」；Parent=`L64:## R2-10-NORMAL：新 PID、普通 Goal、零 B1 專用 Prompt`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NOFIT,不能,禁止`。本章觸發/Consumer=Hermes existing Kanban/Delegation/SharedSpine；承接 `WP 04/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH20.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。

### F.2 本章 WP 與 Producer／typed I/O／FirstFail（每項獨立）

- **WP-FHS-04**：Producer=Hermes original Runtime/Journal + HGK SharedSpine；Input=Hermes v0.22.5 pin；ProfileSHA、WorkID、lease generation、run budget 原 Reader；Output=Fresh PID+LoadedProfileSHA+Raw三Lane Required/Selected/Invoked/ActualServed + JournalCursor；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=Hermes Durable Runtime 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=以過期 lease_generation 重播非冪等 WorkID 並把 Picker Selected 假稱 ActualServed；EDGE=worker crash 在 effect 之後/Raw 入帳之前：維持 UNKNOWN，必 original World Reconcile；FirstFail=`HERMES_LEASE_UNKNOWN_RECONCILE`；rollback=原 Journal 查 WorldRaw/last-good 再 Resume WorkID；UNKNOWN 禁盲重試。
- **WP-FHS-07**：Producer=原 HGK Native PLAN Writer/Reader；Input=W0 WP15 三 SPEC/QuestionLedger、PLAN base_revision、original Native PLAN CAS Reader；Output=PlanRevisionProposal + original CAS(base_revision, proposal_hash) ACK/NACK；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=Native PLAN Commander A/B/C 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=跳過原 PLAN Writer 直接送 ECP→Issuer 或停用 legacy commander 提升成新 Gate；EDGE=兩個 proposal 同 base_revision 競逐，僅一個 Writer CAS 成功；另一個明確 NACK；FirstFail=`PLAN_CAS_STALE_BASE`；rollback=CAS mismatch 丟棄提案並重讀 base；不寫 Target Repo/second Queue。

### F.3 複合原義拆解、反向閉包與受影退出

- **「各有」**：本 CH 的每個原 clause locator 各自保留 SourceSHA/Parent/OriginalConsumer、POS/NEG；若原文有多個 named roles/Host/Case，不可用單一結果冒全數。
- **「分別」**：strict JSON body／@2 sidecar、Original Policy Active／Host Loaded、Maker challenge／Protected Checker、Selected／ActualServed 是不同欄位與收據，不得合併。
- **「對應」**：必 `original source line → SCL-W1 id → CH → W1 WP → expected Case → original source line` 可機械重算；原 OriginalID 未明者只引用明示的 SourceSpan，不可猜 ID。
- **「不得／若／除非」**：否定作用域保留到原 Parent context；本章只標作者候選，原 Source Reader 取得 ACK 才能宣告原語義接受。
- **退出**：原 Reader NACK 僅 PARK 本章受影的 PI/PD/DEV/OPS/Host operation；合法 SOURCE_READ、隔離草稿及不依賴該 ABI 的 W0/W2 工作照原許可前進。

## 本章 L2-r4 設計義務接收卡（逐 ID；不可省略原 NEG）

- `INT-07` (`L1-r4:L775`, `L2-r4:L321`)：低阻力優先既有輪子；Hermes Direct/Delegation/Kanban/Swarm 按複雜度選擇，NoFit 才補；[CH-20](#ch-20)/[CH-23](#ch-23)/[CH-47](#ch-47)；POS `Hermes Direct/Delegation/Kanban/Swarm 按複雜度選擇，NoFit 才補`；NEG/FirstFail `沒查現有 Hermes 能力便重造 Scheduler/Router；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `Hermes original Runtime/Launcher/Provider Raw Reader → HGK Lane/Journal Consumer、Original Tech/License/Host/Method Owner → Capability Consumer`；本輪只有 EXPECTED_NOT_OBSERVED。
- `FHS-DR-035` (`L1-r4:L832`, `L2-r4:L373`)：Runtime／B/LONG；Hermes v0.22.5 原能力優先使用；Direct→Delegate→Kanban→Swarm 依複雜度決定；[CH-19](#ch-19)/[CH-20](#ch-20)；POS `真 task result 有再續工`；NEG/FirstFail `簡單 Read 任務硬套多 Agent Queue；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `Original Domain Owner/Reader (scope binding pending)`；本輪只有 EXPECTED_NOT_OBSERVED。

## CH-20 專屬退出與回退

DraftMaker 後續須填 `original_reader_ref`, `original_schema_version_or_HOLD`, `source_span_sha`, `same_subject_and_scope`, `Case/Oracle`, `positive_raw_expected`, `negative_raw_expected`, `first_fail`, `resume_predicate`, `last_good`, `consumer_ack_or_HOLD`。`DOC_AUTHOR_DONE` 是本檔可檢索，不是 `Hermes Native Kanban／Delegation／Swarm／長任務編排` 已原 Host Qualified。若權限／能力尚缺，只 PARK 受影操作；回退到該 Domain 上次有效 Reader/Host 版本、保留跨波合法 READ/DRAFT，且不得刪原 NEG 或憑此文件自簽。



## AUTHOR-FINAL｜CH-20 受影交付契約

**Input / Operation / Output**：保留本章原有專屬 I/O、原句與 NEG；以當期 Registry 對同 SourceSHA/Subject/Scope 重算受影子圖，輸出 CH-20 的原 Reader BindingRequest，實質輸出與業務 FirstFail 以本章上文專屬契約及下列子義為準。

**Original Reader / Original Consumer**：Hermes Original Journal/World Reader；原 Consumer Raw=EXPECTED_NOT_OBSERVED。L1 起始 1902、終止 1978，section SHA `26461f88645fafe6c79c6853d21ff05b60cc06ba86e119d936329a5597c4b25b`。

**POS / NEG / FirstFail**：本章專屬正負條件逐筆如下；沒有適用子義的跨 ABI 章以原本章完整 POS/NEG 為準，不從別章借用 PASS。**EDGE**：SourceSHA/Host/PolicyEpoch 其中一欄改變，只 invalidate 受影接線；**SEC**：Maker 假 ACK 或跨 Principal 原回條均拒收。**ExpectedRaw**：同 Subject/Candidate/Scope 原 Consumer/World bytes；本輪 NOT_RUN。**Stop**：缺該 Effect 必需原 Reader 即 PARK 其效果；**Resume**：同 Scope 原 Reader 提供具名 Raw；**NextWave**：W2 原 Effect Receiver，四 Host/Cell/W18 交 W3，CI/Publisher 交 W4。

- `S-W1-INT-07-01`：Input=Direct→Delegation→Kanban→Swarm 按任務選最低足夠方法；POS=普通來源讀取沿用 Direct；NEG=簡單任務先造第二 swarm scheduler；FirstFail=`SHADOW_SCHEDULER_OR_OVERENGINEER_NACK`；Consumer=Hermes original Runtime/Owner and Tech Owner；Case=`AUTHOR.W1.INT-07.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-07-02`：Input=現役 capability 足夠時優先復用；POS=原 Host capability 正例與 Consumer 相符；NEG=未 probe 原能力即採新輪子；FirstFail=`NATIVE_CAPABILITY_PROBE_MISSING`；Consumer=Hermes original Runtime/Owner and Tech Owner；Case=`AUTHOR.W1.INT-07.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-INT-07-03`：Input=NoFit 才向原技術 Owner 提替代案；POS=原 NoFit/License/rollback 具名；NEG=以研究字串直接宣外部 loader qualified；FirstFail=`TECH_NOFIT_OR_LOAD_HOLD`；Consumer=Hermes original Runtime/Owner and Tech Owner；Case=`AUTHOR.W1.INT-07.03.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-035-01`：Input=Direct/Delegation/Kanban/Swarm 按複雜度；POS=小 read 直接處理無重啟；NEG=小 read 強制新多 Agent queue；FirstFail=`HERMES_OVERENGINEERING_NACK`；Consumer=Hermes original runtime Owner；Case=`AUTHOR.W1.FHS-DR-035.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-035-02`：Input=原 Queue/Journal/lease 原位恢復；POS=相同 WorkID JournalCursor/lease_generation；NEG=盲重播 UNKNOWN nonidempotent；FirstFail=`HERMES_WORLD_RECONCILE_REQUIRED`；Consumer=Hermes original runtime Owner；Case=`AUTHOR.W1.FHS-DR-035.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。

<a id="ch-21"></a>

# CH-21｜Windows Host／CLI／Plugin／Skill：安裝與實際載入三段驗收

**唯一主波** `W3`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L1979–2047`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Host Install/Loader Reader；L2-r4:L911。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W3 Normative 主責）

W1 保持此章完整源身份、Need/Host/Consumer 的交接 locator；全產品分母/普通模式及其原 Reader 由 W3 主波驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W3 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L1979–2047` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-21 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-21",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W3",
  "OriginalReader": "Original Host Install/Loader Reader；L2-r4:L911",
  "consumer": "Original Host Install/Loader Reader；L2-r4:L911",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-21",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 1979,
    "end": 2047
  }
}
```

<a id="ch-22"></a>

# CH-22｜Native20：現役唯一原生核心與維護權

### r2 受影修補（2026-11-05｜AUTHOR_FINAL_AFFECTED_REPAIR）

**受影 Finding**：`F-07、F-08、N-06`。**原位差額**：24 Asset 維持唯一 effective pin 與逐階狀態；OpenSpec 本機 1.8.0 只作 HotSwap 候選、gstack `NOT_INSTALLED`；Need 先找既有原生 Occupant，NoFit 才談薄 Adapter。

**未變更**：本章 H1 標題、L1 span／section SHA、OriginalID／Parent／NEG 與原 Reader 法位皆不變；原域 Raw 未取得者維持 `EXPECTED_NOT_OBSERVED`，不以作者推斷補值。

**下一個 Reader**：Original Technology／License／Host Reader；FirstFail 見本章 POS／NEG／SEC 卡與 `AFFECTED_FINDINGS.jsonl` 對應列。

## W1 草案當期完成契約｜CH-22（DRAFT-W1-CH22）

**使用者可得結果**：Native20/Default30 OriginalAssets；合法執行範圍限 `SOURCE_READ` 與作者端規格審閱，無真 Host 准入或新 Writer 權限。

| 受影型別 | 本章可驗證的確定規則 |
|---|---|
| Input／觸發 | 24 OriginalAssetIDs、NeedKey、Windows fit、pin/license、Reader、original consumer；強制 `subject_id/source_manifest_sha/scope` 來源釘選 |
| 操作／Producer | 按 Native20 20＋Default30 4 的原 ID 定位，為 NeedKey 在各適用 Scope 只選一 qualified occupant；Selected/Installed/Loaded/Invoked/Used/Verified 不可合併；外部 tools nofit/LastGood；Producer＝W1 DraftMaker（僅文字/Sidecar），正式效果由原域 Producer 執行 |
| Output／交付 | 逐 Asset Build-or-Use/Version/License/Trigger/NEG/Backout 卡；所有未觀測 Reader Raw 留空並具名 `EXPECTED_NOT_OBSERVED` |
| Original Reader | original Technology+Host+License Reader；原 Writer／Issuer／Checker 不因本稿改權 |
| Downstream Consumer | WP17 installer; W3 full-product asset maintainer；綁同 Subject／Scope，需 Original ACK 才可升級 |
| POS／Expected Raw | 24 IDs 逐項有來源及適用 Reader/退出；預期由原 Consumer 返回原格式 Raw（本輪 `NOT_RUN`） |
| NEG／首拒收 | 用一款 Plugin 視 485 件必裝／未核版號宣 Verified；FirstFail=`ASSET_PIN_HOST_LICENSE_HOLD` |
| EDGE | Need 的 HostFit 未觀測僅綁候選；只 PARK 受影 scope，合法 READ/DRAFT 不受波及 |
| SEC | License 不明仍自動安裝；缺憑證、Owner、ACL 或 Checker 證物拒效果 |
| Stop／Resume／Rollback | 遇 `ASSET_PIN_HOST_LICENSE_HOLD` 記 `hold_id+original_reader+required_raw`，停止受影寫入；Resume 需同 SourceSHA/Scope 的原 Reader 結果；READ 丟棄快照、DRAFT 刪除隔離候選；世界效果不在 W1 自行 rollback |
| Cross-wave | W3 CH23–26/47；W4 supply chain；交 `AUTHOR.FHS.W1ToW{next}@design` typed envelope，禁止偽裝 WorkOrder |

**受影源句拆義**：`actor/trigger/action/object`（見 Input/操作）；`condition/exception`（見 EDGE）；`prohibition`（見 NEG/SEC）；`outcome/consumer`（見 Output/Original Reader）；`POS/NEG/FirstFail` 必綁同一原 RequirementID。來源的原始句、Span、SHA、Parent/Child/NEG 以 r5 本章及附錄 `obligation_registry.jsonl` 回指；缺具體原 Reader 即 `ORIGINAL_OWNER_HOLD`，不自行創造簽核。


### R5 本章受影精確契約／業務負例（整合 r4，非歷史附錄）

W1 24 原 AssetID（20 Native+4 Default）逐 Need 保留原身分與 Required/NoFit/OriginalDisposition，原 default 不能因 Host 未 qualified 改 Optional。三態 `DEFAULT_REQUIRED_UNQUALIFIED/QUALIFIED_ACTIVE/ORIGINAL_OWNER_NOFIT_HOLD`，成功須原 Host POS/NEG/Loader Raw；失敗保持 affected capability HOLD。


**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L2048–2318`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Native Owner/Registry；L2-r4:L912。原 Domain Reader/Writer 不因本章轉移。

## r4 當期受影修補（直接摘取 L1 r4 本章有效增量）

## r4｜AUDIT r3 受影整合／覆蓋／取代（現行作者端規範）

**五正交集合不變**：Native20/Default30/Donor24/Method25/TECH386 是五種不同的原資產身分，485 只是 20+30+24+25+386 的來源卡數，不是 485 件必裝工具／同一驗收分母。每個實際 Need 需先讀原佔位義務和原 Capability；NoFit 只停該需求，不可把缺 License 的 TOOL 缺口變全部 Host 無用。

## r4 對齊之 W1 主波操作規格、草案必填欄、逐項 POS/NEG／FirstFail（高保留整合）

**Protected Original H1 / CURRENT L1-r4**：`FHS_PIPD-LS-PKG_藍圖_2026-11-04_r4_HIGH_RETENTION_AUDIT_REPAIRED_實質正文(1).md:L2048–L2318`；`source_file_sha256=cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`；`section_sha256=bb94a5153139251963a27df10dbd8b8c5c78f19cf6f3052b7fac9c6d1745ce4a`；`heading_exact=# CH-22｜Native20：現役唯一原生核心與維護權`；**HISTORICAL_LOCATOR_NOT_EFFECTIVE**=`L1:1427–1675` / `L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`，L2 作者端路由 `L2:660`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W1 不取得原 Writer。

## A. 本章實質功能與不能壓平的原義

Native20 全部原身份不失、真 Singleton/RoleWorker/Method 格式不可混裝。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。

## B. 來源 r5 skeleton 必填核對欄（已由上方 W1 草案當期完成契約受影回填）

| 必填欄 | 欄位設計／不可空條件 |
|---|---|
<!-- HISTORICAL_R5_SKELETON_FILL_REQUEST_SUPERSEDED: transition wording only; all substantive constraints retained -->
| `chapter_id` / `primary_wave` / `author_writer` | `CH-22` / `W1` / `W1:DraftMaker`（歷史 r5 階段欄；當期為作者端定案候選） |
| `original_sources[]` | 本章 L1 行與下面原冊 SHA／OriginalClause Span；不得用語義假定的 ID 補空缺 |
| `same_subject` / `candidate_sha` / `source_manifest_sha` / `affected_scope` | 必攜相同 Subject/Scope，未原 Reader 認證則 `AUTHOR_CANDIDATE` |
| `effect_class` / `original_owner` / `consumer_abi` / `schema_version` | 依 Operation Reader；缺 `$id` 或 Receiver 不自造 |
| `input` / `typed_output` / `fuo` / `non_goals` | 應有真使用者結果與 Receiver（非檔案數） |
| `positive_fixture` / `negative_fixture` / `security_fixture` | 原 Source Case/Oracle 逐受影引用，未有 Runner/Raw 就 `EXPECTED_NOT_OBSERVED` |
| `first_fail` / `hold` / `stop_scope` / `resume_predicate` | 明確停止受影子圖，不全域凍結 READ／DRAFT |
| `rollback` / `w2_handoff` / `original_ack_nack` | 回退路由與 same scope 的預期接收；不得填假 PASS |

## C. Input → Producer → 原 Reader／Consumer → Output

- **Input/Guard**：20 Native original ID＋原 disposition＋Consumer/L1 source line+Host fit。
- **Producer**：該 Original Domain 的 Reader/Compiler/Host/Guide 依本章功能生產；W1 Curator 僅記設計；**Original Consumer**：Original Fabric/HGK/SBL/Hermes/Tech Reader。
- **Typed Output/FUO**：W1 20 route/Need/Owner/Host readback 期待，其中 singleton 不可替換。
- **版本要求**：至少 `Subject,CandidateSHA,SourceSHA,OriginalID+SourceSpan,Scope,Host/PolicyEpoch（受影才填）,ABI $id/version,OriginalReader,OutputRawExpected`，少一欄只停需該欄的出口。

## D. POS／NEG／FirstFail／HOLD／退出

- **POS（期待）**：20/20 原 ID 不消失且每一個有專屬 POS/NEG/NoFit。
- **NEG／SEC（期待拒收）**：把 Method 安裝成第二 Policy 或 20 個全部必裝。
- **FirstFail**：`NATIVE_SINGLETON_COLLISION`；禁止只有泛稱 `VALIDATION_FAILED` 而不給首次失敗位置。
- **HOLD/Owner**：`原法位的 Native20 original Consumer 尚未 ratify`。需同 Subject/Scope/Host/原 Reader 的真 Raw/ACK 解除；本輪 `NOT_RUN`。
- **Stop/Resume**：保留原 SourceSHA/受影 Reader/cursor/last-good；READ/DRAFT 合法部分繼續；UNKNOWN 必原 Reader reconcile。
- **Rollback**：只回復該 Need/Host 的原 last-good，Host/OPS 效果走原 inverse；不得以檔案 ZIP 作回復收據。

## E. 來源追溯、波次邊界與下一手

| 源鍵／檔案 | 原文 SHA | 此 W1 處理方式 |
|---|---|---|
| SBL-DOC-06 | 64ea4977dab3093301f82dc7469413cc754998fc53946467842e06d83645102b | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-08 | 1df04680319796aa253256c5da9c8adea47a5601abfe17086f3598d4f0470f8d | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
W0 提供原 Source/三 SPEC/索引；本 `CH-22` 不修改 W0 成果。W1 WaveCurator 交 W1 DraftMaker 按原 Reader 定位填入真 Requirements；W2 僅領同 Subject/Scope 的需要的 Effect/Case/HOLD，不得借 W3/W4 收據。原 L1 CH-22 的詳細原義仍在 L1 主體，不移作本冊第二 Canonical。

## F. r2 原位修補：CH-22 可直接交接的受影實質規格（非證據附錄）

**本章不可壓平功能**：24 source-bound OriginalAssetID W1 selected Need slots。與 W0 三份獨立 SPEC 維持同 SourceSHA/Subject/Scope；將原讀者真接收的 **Output／Consumer** 優先於填滿文件欄位。依 L1 原 CH 身份與 L2 W1 主責修訂，不移轉原 Writer。

### F.1 原句→原 Consumer→本章測例的逐子義槽（已從原物理檔定位）

- **`SCL-W1-0094`** `[SOURCE:SBL-DOC-06:L935:sha256=64ea4977dab30933]`：原文實質片段「/ NTD-013 / Skill Creator / policy=DONOR_PATTERN_ONLY; runtime=NOT_INSPECTED; owner=F11-04 / SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope;  / SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(」；Parent=`L731:### C33.2.9｜386/386 OriginalIdentity 逐筆 AdmissionDecision@2 擴充欄（不可與原處置相混）`；原 ID=`NTD-013`；NEG=`EXPLICIT:不得`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH22.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0095`** `[SOURCE:SBL-DOC-06:L944:sha256=64ea4977dab30933]`：原文實質片段「/ NTD-022 / SLSA / policy=DONOR_PATTERN_ONLY; runtime=NOT_INSPECTED; owner=F17-05 / SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope;  / SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L59」；Parent=`L731:### C33.2.9｜386/386 OriginalIdentity 逐筆 AdmissionDecision@2 擴充欄（不可與原處置相混）`；原 ID=`NTD-022`；NEG=`EXPLICIT:不得`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH22.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0096`** `[SOURCE:SBL-DOC-06:L958:sha256=64ea4977dab30933]`：原文實質片段「/ NTD-036 / GraphRAG / policy=DONOR_PATTERN_ONLY; runtime=NOT_INSPECTED; owner=F09-05 / SOURCE_DISPOSITION_PRESERVED; SCOPE_BY_OWNER; positive: source+qualified scope;  / SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md」；Parent=`L731:### C33.2.9｜386/386 OriginalIdentity 逐筆 AdmissionDecision@2 擴充欄（不可與原處置相混）`；原 ID=`NTD-036`；NEG=`EXPLICIT:不得`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH22.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0097`** `[SOURCE:FHS-BODY-08:L259:sha256=1df04680319796aa]`：原文實質片段「- **STATIC-v1 來源直接解綁**：METHOD_OR_FORMAT。原 Singleton/Role/Worker 類別照原行保留；類別不是安裝同意，也不是 Mandatory 的降級。METHOD.OPENSPEC Fission-AI OpenSpec / METHOD_OR_FORMAT；SBL Donor/24 Slot 的 SELECTIVE_NATIVE_REUSE；https://githu」；Parent=`L246:#### Native20:METHOD.OPENSPEC｜Fission-AI OpenSpec`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不得,NEG`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH22.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0098`** `[SOURCE:FHS-BODY-08:L1587:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：METHOD-24 OpenAI Agents SDK / SUPPORT_QUARANTINE (not installed claim) / 只有原適用 Trigger/來源條款支持時 HITL pause/resume donor pattern → WP-FHS-17 所有者之 Read/Method Consumer；DEFER/NO_SO」；Parent=`L1585:#### Method25:METHOD-24｜OpenAI Agents SDK`；原 ID=`WP-FHS-17`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH22.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0099`** `[SOURCE:FHS-BODY-08:L5892:sha256=1df04680319796aa]`：原文實質片段「Native20、Default30、Donor24、Method25、TECH386分開守恆，不能加總成必裝數。每筆保留原名/處置/功能/Consumer/專屬NEG，再按AssetType提供不同建造、綁定、調用及退場規格。未知外部repo commit/license明列NOT_BOUND，不能從檔案SHA猜upstream license；必由原Tech/License/Host Owner唯讀補probe後」；Parent=`L5890:## R2-08-ASSET：五個正交集合與BuildOrUseRecipe`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不能,NEG`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH22.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0127`** `[SOURCE:FHS-BODY-08:L61:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：CORE.FABRIC_POLICY Fabric Policy Source/Consumer / NATIVE_SINGLETON；Fabric Control Plane Policy Owner；Repo FABRIC/control/／FABRIC/fabric/consumers/hgk_policy_consumer.py；Produc」；Parent=`L59:#### Native20:CORE.FABRIC_POLICY｜Fabric Policy Source/Consumer`；原 ID=`Native20:CORE.FABRIC_POLICY`；NEG=`EXPLICIT:NEG,不可`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:CORE.FABRIC_POLICY`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0128`** `[SOURCE:FHS-BODY-08:L78:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：CORE.HGK_NATIVE HGK Protected Registry/Resolver/Issuer/Receiver / NATIVE_SINGLETON；HGK Sole Control；src/hg_kseos/, B1 candidate snapshot；Producer/Consumer 依 SRC-08:L579 原 Owner」；Parent=`L76:#### Native20:CORE.HGK_NATIVE｜HGK Protected Registry/Resolver/Issuer/Receiver`；原 ID=`Native20:CORE.HGK_NATIVE`；NEG=`EXPLICIT:NEG,不可`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:CORE.HGK_NATIVE`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0129`** `[SOURCE:FHS-BODY-08:L95:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：CORE.SHAREDSPINE SQLite/journal/Lease / NATIVE_SINGLETON；HGK src/hg_kseos/spine.py, Hermes governed executor；Producer/Consumer 依 SRC-08:L580 原 Owner，不由外部 plugin 篡位。 / Trigger 按」；Parent=`L93:#### Native20:CORE.SHAREDSPINE｜SQLite/journal/Lease`；原 ID=`Native20:CORE.SHAREDSPINE`；NEG=`EXPLICIT:NEG,不可`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:CORE.SHAREDSPINE`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0130`** `[SOURCE:FHS-BODY-08:L112:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：RUNTIME.HERMES canonical Hermes / GOVERNED_RUNTIME；Fabric INTEGRATION/DEPENDENCY 與 W18 Native Work；Producer/Consumer 依 SRC-08:L581 原 Owner，不由外部 plugin 篡位。 / Trigger 按本案 Goal/Mo」；Parent=`L110:#### Native20:RUNTIME.HERMES｜canonical Hermes`；原 ID=`Native20:RUNTIME.HERMES`；NEG=`EXPLICIT:NEG,不可,不能`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:RUNTIME.HERMES`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0131`** `[SOURCE:FHS-BODY-08:L129:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：LANE.PLAN.TPM Native SBL-TPM／TPM Skill / ROLE_OR_WORKER；SBL TPM 雙形態藍圖、SBL sbl_sp/plugins/tpm_sp；Producer/Consumer 依 SRC-08:L582 原 Owner，不由外部 plugin 篡位。 / Trigger 按本案 Goal/Mode/」；Parent=`L127:#### Native20:LANE.PLAN.TPM｜Native SBL-TPM／TPM Skill`；原 ID=`Native20:LANE.PLAN.TPM`；NEG=`EXPLICIT:NEG,不得,NOFIT`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:LANE.PLAN.TPM`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0132`** `[SOURCE:FHS-BODY-08:L146:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：LANE.PLAN.COMMANDER Native SBL Commander／Guide Skill / ROLE_OR_WORKER；Commander 重構藍圖；SBL 原 Required 不取消；Producer/Consumer 依 SRC-08:L583 原 Owner，不由外部 plugin 篡位。 / Trigger 按本案 Go」；Parent=`L144:#### Native20:LANE.PLAN.COMMANDER｜Native SBL Commander／Guide Skill`；原 ID=`Native20:LANE.PLAN.COMMANDER`；NEG=`EXPLICIT:NEG,禁止,不得,NOFIT`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:LANE.PLAN.COMMANDER`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0133`** `[SOURCE:FHS-BODY-08:L163:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：LANE.EXECUTE.CODEX Codex bounded Worker / ROLE_OR_WORKER；HGK lane registry + Hermes worker + Codex CLI；Producer/Consumer 依 SRC-08:L584 原 Owner，不由外部 plugin 篡位。 / Trigger 按本案 Goa」；Parent=`L161:#### Native20:LANE.EXECUTE.CODEX｜Codex bounded Worker`；原 ID=`Native20:LANE.EXECUTE.CODEX`；NEG=`EXPLICIT:NEG,NoFit,不得,NOFIT`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:LANE.EXECUTE.CODEX`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0134`** `[SOURCE:FHS-BODY-08:L180:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：LANE.VERIFY.CHALLENGE SBL External Challenge＋Protected Checker / ROLE_OR_WORKER；SBL external_challenge_sp、HGK AO；分工真身份；Producer/Consumer 依 SRC-08:L585 原 Owner，不由外部 plugin 篡位。 /」；Parent=`L178:#### Native20:LANE.VERIFY.CHALLENGE｜SBL External Challenge＋Protected Checker`；原 ID=`Native20:LANE.VERIFY.CHALLENGE`；NEG=`EXPLICIT:NEG,不得,NOFIT`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:LANE.VERIFY.CHALLENGE`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0135`** `[SOURCE:FHS-BODY-08:L197:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：METHOD.FAR Fabric Autonomous Research / METHOD_OR_FORMAT；Fabric FABRIC/fabric-autonomous-research/／FAR domain Reader；Producer/Consumer 依 SRC-08:L586 原 Owner，不由外部 plugin 篡位。 / T」；Parent=`L195:#### Native20:METHOD.FAR｜Fabric Autonomous Research`；原 ID=`Native20:METHOD.FAR`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:METHOD.FAR`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0136`** `[SOURCE:FHS-BODY-08:L214:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：METHOD.KANBAN existing Hermes kanban / METHOD_OR_FORMAT；B1 歷史回報與現役 HGK/Hermes Registry discovery；Producer/Consumer 依 SRC-08:L587 原 Owner，不由外部 plugin 篡位。 / Trigger 按本案 Goal/Mode」；Parent=`L212:#### Native20:METHOD.KANBAN｜existing Hermes kanban`；原 ID=`Native20:METHOD.KANBAN`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:METHOD.KANBAN`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0137`** `[SOURCE:FHS-BODY-08:L231:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：METHOD.SWARM bounded delegate / METHOD_OR_FORMAT；W18 跨域四方 dogfood／HGK PLAN；Producer/Consumer 依 SRC-08:L588 原 Owner，不由外部 plugin 篡位。 / Trigger 按本案 Goal/Mode/Host 的適用性與 只有任務能分獨立無寫」；Parent=`L229:#### Native20:METHOD.SWARM｜bounded delegate`；原 ID=`Native20:METHOD.SWARM`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:METHOD.SWARM`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0138`** `[SOURCE:FHS-BODY-08:L248:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：METHOD.OPENSPEC Fission-AI OpenSpec / METHOD_OR_FORMAT；SBL Donor/24 Slot 的 SELECTIVE_NATIVE_REUSE；https://github.com/Fission-AI/OpenSpec；Producer/Consumer 依 SRC-08:L589 原 Owner」；Parent=`L246:#### Native20:METHOD.OPENSPEC｜Fission-AI OpenSpec`；原 ID=`Native20:METHOD.OPENSPEC`；NEG=`EXPLICIT:NEG,不得`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:METHOD.OPENSPEC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0139`** `[SOURCE:FHS-BODY-08:L265:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：METHOD.GSTACK gstack workflow / METHOD_OR_FORMAT；SBL Donor 分類 REFERENCE/EVAL_ONLY；https://github.com/garrytan/gstack；Producer/Consumer 依 SRC-08:L590 原 Owner，不由外部 plugin 篡位。 / T」；Parent=`L263:#### Native20:METHOD.GSTACK｜gstack workflow`；原 ID=`Native20:METHOD.GSTACK`；NEG=`EXPLICIT:NEG,NoFit`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:METHOD.GSTACK`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0140`** `[SOURCE:FHS-BODY-08:L282:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：METHOD.SUPERPOWERS obra Superpowers / METHOD_OR_FORMAT；SBL 25 Method/Donor 的 METHOD_REUSE；https://github.com/obra/superpowers；Producer/Consumer 依 SRC-08:L591 原 Owner，不由外部 plugi」；Parent=`L280:#### Native20:METHOD.SUPERPOWERS｜obra Superpowers`；原 ID=`Native20:METHOD.SUPERPOWERS`；NEG=`EXPLICIT:NEG,不能`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:METHOD.SUPERPOWERS`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0141`** `[SOURCE:FHS-BODY-08:L299:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：METHOD.SPEC_KIT GitHub Spec Kit / METHOD_OR_FORMAT；六 Donor 原 OPTIONAL_GREENFIELD；https://github.com/github/spec-kit；Producer/Consumer 依 SRC-08:L592 原 Owner，不由外部 plugin 篡位。 / Tr」；Parent=`L297:#### Native20:METHOD.SPEC_KIT｜GitHub Spec Kit`；原 ID=`Native20:METHOD.SPEC_KIT`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:METHOD.SPEC_KIT`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0142`** `[SOURCE:FHS-BODY-08:L316:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：METHOD.MATTP_SKILLS Matt Pocock Skills / METHOD_OR_FORMAT；六 Donor 原 METHOD_REUSE；https://github.com/mattpocock/skills；Producer/Consumer 依 SRC-08:L593 原 Owner，不由外部 plugin 篡位。 / 」；Parent=`L314:#### Native20:METHOD.MATTP_SKILLS｜Matt Pocock Skills`；原 ID=`Native20:METHOD.MATTP_SKILLS`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:METHOD.MATTP_SKILLS`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0143`** `[SOURCE:FHS-BODY-08:L333:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：METHOD.GSD Get Shit Done donor（來源中的 GSD 名稱） / METHOD_OR_FORMAT；六 Donor 原 REFERENCE_ONLY/ARCHIVED_LINEAGE_CHECK，外部 pin 未確認；Producer/Consumer 依 SRC-08:L594 原 Owner，不由外部 plugin 篡位」；Parent=`L331:#### Native20:METHOD.GSD｜Get Shit Done donor（來源中的 GSD 名稱）`；原 ID=`Native20:METHOD.GSD`；NEG=`EXPLICIT:NEG,不得`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:METHOD.GSD`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0144`** `[SOURCE:FHS-BODY-08:L350:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：METHOD.FABRIC_COMPRESS 知識/Prompt/Skill 壓製 / METHOD_OR_FORMAT；SBL DOC06/10、Fabric FAR 受控技術准入；Producer/Consumer 依 SRC-08:L595 原 Owner，不由外部 plugin 篡位。 / Trigger 按本案 Goal/Mode/Host」；Parent=`L348:#### Native20:METHOD.FABRIC_COMPRESS｜知識/Prompt/Skill 壓製`；原 ID=`Native20:METHOD.FABRIC_COMPRESS`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:METHOD.FABRIC_COMPRESS`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0145`** `[SOURCE:FHS-BODY-08:L367:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：PIPD.P4 PIPD-LS-SP Public Skills+CLI / OWNER_COMPONENT；19 Canonical schema, 13 CLI, 8 Skills；https://github.com/shw097-team/PIPD-LS-SP；Producer/Consumer 依 SRC-08:L596 原 Owner，不」；Parent=`L365:#### Native20:PIPD.P4｜PIPD-LS-SP Public Skills+CLI`；原 ID=`Native20:PIPD.P4`；NEG=`EXPLICIT:NEG,不能,不得`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:PIPD.P4`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0146`** `[SOURCE:FHS-BODY-08:L384:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：SBL.PRODUCT SBL Shared Core+Three SP / OWNER_COMPONENT；https://github.com/shw097-team/SBL；Producer/Consumer 依 SRC-08:L597 原 Owner，不由外部 plugin 篡位。 / Trigger 按本案 Goal/Mode/Host 的」；Parent=`L382:#### Native20:SBL.PRODUCT｜SBL Shared Core+Three SP`；原 ID=`Native20:SBL.PRODUCT`；NEG=`EXPLICIT:NEG,NoFit,不得`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 11/17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Native20:SBL.PRODUCT`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0147`** `[SOURCE:FHS-BODY-08:L402:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：P0-TOOL-001 Hermes Agent / DEFAULT_ENABLED_AFTER_QUALIFICATION 原選用；原決策 DEFAULT_ENABLED_AFTER_QUALIFICATION；DIRECT_CORE；成果：governed durable task dispatch / Host/Pack：RUNTIME.HER」；Parent=`L400:#### Default30:P0-TOOL-001｜Hermes Agent`；原 ID=`Default30:P0-TOOL-001`；NEG=`EXPLICIT:NEG,NoFit,NOFIT,不得`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Default30:P0-TOOL-001`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0148`** `[SOURCE:FHS-BODY-08:L450:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：P0-TOOL-005 Codex / DEFAULT_ENABLED_AFTER_QUALIFICATION 原選用；原決策 DEFAULT_ENABLED_AFTER_QUALIFICATION；DIRECT_CORE；成果：bounded primary code worker / Host/Pack：RUNTIME.CODE_WORKER_P」；Parent=`L448:#### Default30:P0-TOOL-005｜Codex`；原 ID=`Default30:P0-TOOL-005`；NEG=`EXPLICIT:NEG,NoFit,NOFIT,不得`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Default30:P0-TOOL-005`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0149`** `[SOURCE:FHS-BODY-08:L690:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：P0-TOOL-062 GitHub Actions / DEFAULT_ENABLED_AFTER_QUALIFICATION 原選用；原決策 DEFAULT_ENABLED_AFTER_QUALIFICATION；SUPPLY_CHAIN_DEPENDENCY；成果：GitHub Actions CI runtime / Host/Pack：SU」；Parent=`L688:#### Default30:P0-TOOL-062｜GitHub Actions`；原 ID=`Default30:P0-TOOL-062`；NEG=`EXPLICIT:NEG,NoFit,NOFIT,不得`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Default30:P0-TOOL-062`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0150`** `[SOURCE:FHS-BODY-08:L750:sha256=1df04680319796aa]`：原文實質片段「- 原功能/Producer/Consumer/專屬POS+NEG：P0-TOOL-072 SQLite / DEFAULT_ENABLED_AFTER_QUALIFICATION 原選用；原決策 DEFAULT_ENABLED_AFTER_QUALIFICATION；DIRECT_CORE；成果：SQLite durable state store / Host/Pack：CORE.SQLITE→HGK exist」；Parent=`L748:#### Default30:P0-TOOL-072｜SQLite`；原 ID=`Default30:P0-TOOL-072`；NEG=`EXPLICIT:NEG,NoFit,NOFIT,不得`。本章觸發/Consumer=Original technology/Host Asset Reader；承接 `WP 17`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.ASSET.Default30:P0-TOOL-072`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。

### F.2 本章 WP 與 Producer／typed I/O／FirstFail（每項獨立）

- **WP-FHS-11**：Producer=各 Host 原 Skill/Plugin Reader+每 SP original Consumer；Input=TPM-SP、Commander Guide-SP、Acceptance Challenge-SP 各自 artifact digest；Host compatibility+8 PIPD skills 各自 registry；Output=每 SP×Host 真 Loaded/Invoked/Used/nontrigger/Remove Raw；不共用收據；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=Portable Host Dogfood 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=用 TPM-SP 的 Loaded SHA 冒 Challenge-SP；Maker 以模型結論簽 Protected Checker；EDGE=Installed 後 loader 未 Loaded，或 Loaded 但 nontrigger 仍被啟動：不得宣稱 Used；FirstFail=`HOST_SKILL_TRIGGER_NONTRIGGER_NACK`；rollback=原 Host disable/remove entrypoint、還原 last-good manifest；清理 residue。
- **WP-FHS-17**：Producer=原 HGK Issuer+Host Installer/Capability Registry；Input=NeedKey+scope、原 Policy Loaded ACK+HGK Issuer admitted installer+license/asset digest；Output=Needed Capability 之 Installed/Loaded/Invoked/ConsumerACK+last-good，NONE=CAPABILITY_GAP_HOLD；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=CAP-BOOT Native Occupants 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=未有原 Issuer/Asset provenance 卻執行 Host installer；或第二套 Queue/Issuer 被包進工具；EDGE=Installer 解壓成功但載入失敗，需回上版 qualified last-good，不可把 Installed 當 Active；FirstFail=`CAP_INSTALLER_ORIGIN_PARTIAL_ROLLBACK`；rollback=原 installer inverse/restore manifest+LoadedSHA+residue；不得 Git revert 取代 Host inverse。

### F.3 複合原義拆解、反向閉包與受影退出

- **「各有」**：本 CH 的每個原 clause locator 各自保留 SourceSHA/Parent/OriginalConsumer、POS/NEG；若原文有多個 named roles/Host/Case，不可用單一結果冒全數。
- **「分別」**：strict JSON body／@2 sidecar、Original Policy Active／Host Loaded、Maker challenge／Protected Checker、Selected／ActualServed 是不同欄位與收據，不得合併。
- **「對應」**：必 `original source line → SCL-W1 id → CH → W1 WP → expected Case → original source line` 可機械重算；原 OriginalID 未明者只引用明示的 SourceSpan，不可猜 ID。
- **「不得／若／除非」**：否定作用域保留到原 Parent context；本章只標作者候選，原 Source Reader 取得 ACK 才能宣告原語義接受。
- **退出**：原 Reader NACK 僅 PARK 本章受影的 PI/PD/DEV/OPS/Host operation；合法 SOURCE_READ、隔離草稿及不依賴該 ABI 的 W0/W2 工作照原許可前進。

## 本章 L2-r4 設計義務接收卡（逐 ID；不可省略原 NEG）

- `FHS-DR-042` (`L1-r4:L839`, `L2-r4:L380`)：工具／A＋B；Need→Existing Capability→Occupant→Loaded/Used→Consumer；OriginalDisposition/License/Pin/NoFit/Backout 各槽；[CH-22](#ch-22)/[CH-23](#ch-23)/[CH-47](#ch-47)；POS `需求由已合格工具解決`；NEG/FirstFail `用外部宣傳文即自稱 loaded；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `Original Tech/License/Host/Method Owner → Capability Consumer`；本輪只有 EXPECTED_NOT_OBSERVED。

## CH-22 專屬退出與回退

DraftMaker 後續須填 `original_reader_ref`, `original_schema_version_or_HOLD`, `source_span_sha`, `same_subject_and_scope`, `Case/Oracle`, `positive_raw_expected`, `negative_raw_expected`, `first_fail`, `resume_predicate`, `last_good`, `consumer_ack_or_HOLD`。`DOC_AUTHOR_DONE` 是本檔可檢索，不是 `Native20：現役唯一原生核心與維護權` 已原 Host Qualified。若權限／能力尚缺，只 PARK 受影操作；回退到該 Domain 上次有效 Reader/Host 版本、保留跨波合法 READ/DRAFT，且不得刪原 NEG 或憑此文件自簽。



## AUTHOR-FINAL｜CH-22 受影交付契約

**Input / Operation / Output**：保留本章原有專屬 I/O、原句與 NEG；以當期 Registry 對同 SourceSHA/Subject/Scope 重算受影子圖，輸出 CH-22 的原 Reader BindingRequest，實質輸出與業務 FirstFail 以本章上文專屬契約及下列子義為準。

**Original Reader / Original Consumer**：Original Tech/License/Windows Host Reader；原 Consumer Raw=EXPECTED_NOT_OBSERVED。L1 起始 2048、終止 2318，section SHA `bb94a5153139251963a27df10dbd8b8c5c78f19cf6f3052b7fac9c6d1745ce4a`。

**POS / NEG / FirstFail**：本章專屬正負條件逐筆如下；沒有適用子義的跨 ABI 章以原本章完整 POS/NEG 為準，不從別章借用 PASS。**EDGE**：SourceSHA/Host/PolicyEpoch 其中一欄改變，只 invalidate 受影接線；**SEC**：Maker 假 ACK 或跨 Principal 原回條均拒收。**ExpectedRaw**：同 Subject/Candidate/Scope 原 Consumer/World bytes；本輪 NOT_RUN。**Stop**：缺該 Effect 必需原 Reader 即 PARK 其效果；**Resume**：同 Scope 原 Reader 提供具名 Raw；**NextWave**：W2 原 Effect Receiver，四 Host/Cell/W18 交 W3，CI/Publisher 交 W4。

- `S-W1-FHS-DR-042-01`：Input=原五集合身份/Disposition 每個 Need 保留；POS=符合原 Required 才有 qualified Occupant；NEG=將 default mandatory 偷改 optional；FirstFail=`DESIGN_DEFAULT_DOWNGRADE`；Consumer=Original Technology/License/Host Owner (primary W3)；Case=`AUTHOR.W1.FHS-DR-042.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-042-02`：Input=install/load/used 是分立原 Host 證據；POS=same Need+Scope 一個活躍 Occupant；NEG=外部介紹文當原 Host Loaded；FirstFail=`CAPABILITY_LOAD_UNVERIFIED`；Consumer=Original Technology/License/Host Owner (primary W3)；Case=`AUTHOR.W1.FHS-DR-042.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-042-03`：Input=NoFit/替換需原 Owner 採許可且有 LastGood；POS=受影 Replacement POS+NEG/rollback；NEG=任意雙 active occupant；FirstFail=`DOUBLE_ACTIVE_OCCUPANT_DENY`；Consumer=Original Technology/License/Host Owner (primary W3)；Case=`AUTHOR.W1.FHS-DR-042.03.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。

<a id="ch-23"></a>

# CH-23｜Default30：默認能力、可配置佔用與 NoFit

**唯一主波** `W3`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L2319–2696`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Default Capability/Host Owner；L2-r4:L913。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W3 Normative 主責）

W1 保持此章完整源身份、Need/Host/Consumer 的交接 locator；全產品分母/普通模式及其原 Reader 由 W3 主波驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W3 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L2319–2696` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-23 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-23",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W3",
  "OriginalReader": "Default Capability/Host Owner；L2-r4:L913",
  "consumer": "Default Capability/Host Owner；L2-r4:L913",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-23",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 2319,
    "end": 2696
  }
}
```

<a id="ch-24"></a>

# CH-24｜Donor24：可借用外部輪子與授權條件

**唯一主波** `W3`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L2697–3015`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Donor License/Host Owner；L2-r4:L914。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W3 Normative 主責）

W1 保持此章完整源身份、Need/Host/Consumer 的交接 locator；全產品分母/普通模式及其原 Reader 由 W3 主波驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W3 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L2697–3015` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-24 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-24",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W3",
  "OriginalReader": "Donor License/Host Owner；L2-r4:L914",
  "consumer": "Donor License/Host Owner；L2-r4:L914",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-24",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 2697,
    "end": 3015
  }
}
```

<a id="ch-25"></a>

# CH-25｜Method25：演算法／流程工具方法的原用途

**唯一主波** `W3`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L3016–3336`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Method Consumer；L2-r4:L915。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W3 Normative 主責）

W1 保持此章完整源身份、Need/Host/Consumer 的交接 locator；全產品分母/普通模式及其原 Reader 由 W3 主波驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W3 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L3016–3336` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-25 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-25",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W3",
  "OriginalReader": "Method Consumer；L2-r4:L915",
  "consumer": "Method Consumer；L2-r4:L915",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-25",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 3016,
    "end": 3336
  }
}
```

<a id="ch-26"></a>

# CH-26｜TECH386：逐原 ID 技術功能與非降級 Disposition

**唯一主波** `W3`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L3337–6880`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Tech Need/License/Host Owner；L2-r4:L916。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W3 Normative 主責）

W1 保持此章完整源身份、Need/Host/Consumer 的交接 locator；全產品分母/普通模式及其原 Reader 由 W3 主波驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W3 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L3337–6880` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-26 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-26",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W3",
  "OriginalReader": "Tech Need/License/Host Owner；L2-r4:L916",
  "consumer": "Tech Need/License/Host Owner；L2-r4:L916",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-26",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 3337,
    "end": 6880
  }
}
```

<a id="ch-27"></a>

# CH-27｜SBL 50 Parent／149 Child：原生產品分母專章

**唯一主波** `W3`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L6881–7683`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** SBL Product Parent/Child Reader；L2-r4:L917。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W3 Normative 主責）

W1 保持此章完整源身份、Need/Host/Consumer 的交接 locator；全產品分母/普通模式及其原 Reader 由 W3 主波驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W3 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L6881–7683` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-27 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-27",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W3",
  "OriginalReader": "SBL Product Parent/Child Reader；L2-r4:L917",
  "consumer": "SBL Product Parent/Child Reader；L2-r4:L917",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-27",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 6881,
    "end": 7683
  }
}
```

<a id="ch-28"></a>

# CH-28｜R15 949 原產品原子與 B1 66／254／629 映射

**唯一主波** `W3`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L7684–20103`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** SBL Full Product R15 Reader；L2-r4:L918。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W3 Normative 主責）

W1 保持此章完整源身份、Need/Host/Consumer 的交接 locator；全產品分母/普通模式及其原 Reader 由 W3 主波驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W3 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L7684–20103` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-28 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-28",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W3",
  "OriginalReader": "SBL Full Product R15 Reader；L2-r4:L918",
  "consumer": "SBL Full Product R15 Reader；L2-r4:L918",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-28",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 7684,
    "end": 20103
  }
}
```

<a id="ch-29"></a>

# CH-29｜Kind×Mode×Host×LegacyToken 192 Cell 的原始逐格行為

**唯一主波** `W3`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L20104–22662`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Host Cell Reader；L2-r4:L919。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W3 Normative 主責）

W1 保持此章完整源身份、Need/Host/Consumer 的交接 locator；全產品分母/普通模式及其原 Reader 由 W3 主波驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W3 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L20104–22662` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-29 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-29",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W3",
  "OriginalReader": "Original Host Cell Reader；L2-r4:L919",
  "consumer": "Original Host Cell Reader；L2-r4:L919",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-29",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 20104,
    "end": 22662
  }
}
```

<a id="ch-30"></a>

# CH-30｜Original 96 Oracle：Test Class×Oracle 的型別與逐格準則

**唯一主波** `W3`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L22663–23590`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Assurance Oracle Reader；L2-r4:L920。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W3 Normative 主責）

W1 保持此章完整源身份、Need/Host/Consumer 的交接 locator；全產品分母/普通模式及其原 Reader 由 W3 主波驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W3 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L22663–23590` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-30 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-30",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W3",
  "OriginalReader": "Original Assurance Oracle Reader；L2-r4:L920",
  "consumer": "Original Assurance Oracle Reader；L2-r4:L920",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-30",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 22663,
    "end": 23590
  }
}
```

<a id="ch-31"></a>

# CH-31｜Acceptance Challenge 15 條異構 Sender→Receiver Edge

**唯一主波** `W2`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L23591–23804`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Challenge/Protected Checker；L2-r4:L921。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W2 Normative 主責）

W1 只交原受影 Effect/Repo/Host/Reader request，世界效果、TQAEP 真 Raw 與 FirstFail 由 W2 在原准入後驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W2 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L23591–23804` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-31 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-31",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W2",
  "OriginalReader": "Original Challenge/Protected Checker；L2-r4:L921",
  "consumer": "Original Challenge/Protected Checker；L2-r4:L921",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-31",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 23591,
    "end": 23804
  }
}
```

<a id="ch-32"></a>

# CH-32｜B1 120 Parent／124 Child／38 Node＝282 Case 的獨立驗收

**唯一主波** `W3`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L23805–25800`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original B1 CaseRunner Reader；L2-r4:L922。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W3 Normative 主責）

W1 保持此章完整源身份、Need/Host/Consumer 的交接 locator；全產品分母/普通模式及其原 Reader 由 W3 主波驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W3 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L23805–25800` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-32 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-32",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W3",
  "OriginalReader": "Original B1 CaseRunner Reader；L2-r4:L922",
  "consumer": "Original B1 CaseRunner Reader；L2-r4:L922",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-32",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 23805,
    "end": 25800
  }
}
```

<a id="ch-33"></a>

# CH-33｜B1 原 27 PI→31 PD Slot：拓撲與 Effect ECP

**唯一主波** `W3`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L25801–26232`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original PI/PD Slot Reader；L2-r4:L923。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W3 Normative 主責）

W1 保持此章完整源身份、Need/Host/Consumer 的交接 locator；全產品分母/普通模式及其原 Reader 由 W3 主波驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W3 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L25801–26232` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-33 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-33",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W3",
  "OriginalReader": "Original PI/PD Slot Reader；L2-r4:L923",
  "consumer": "Original PI/PD Slot Reader；L2-r4:L923",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-33",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 25801,
    "end": 26232
  }
}
```

<a id="ch-34"></a>

# CH-34｜Portable Commander Guide A／B／C 與原 Native PLAN

### r2 受影修補（2026-11-05｜AUTHOR_FINAL_AFFECTED_REPAIR）

**受影 Finding**：`F-09、N-04`。**原位差額**：Commander Guide A/B/C 只產 Native PLAN 請求；同 WorkID／Revision 的 CAS 回執是唯一 ACK 來源，缺回執不得稱 PLAN accepted；E26 不阻本章。

**未變更**：本章 H1 標題、L1 span／section SHA、OriginalID／Parent／NEG 與原 Reader 法位皆不變；原域 Raw 未取得者維持 `EXPECTED_NOT_OBSERVED`，不以作者推斷補值。

**下一個 Reader**：Original Native PLAN CAS Reader；FirstFail 見本章 POS／NEG／SEC 卡與 `AFFECTED_FINDINGS.jsonl` 對應列。

## W1 草案當期完成契約｜CH-34（DRAFT-W1-CH34）

**使用者可得結果**：Commander Guide A/B/C to Native PLAN；合法執行範圍限 `LOCAL_DRAFT_WRITE` 與作者端規格審閱，無真 Host 准入或新 Writer 權限。

| 受影型別 | 本章可驗證的確定規則 |
|---|---|
| Input／觸發 | 三 SPEC/PI/PD/ECP/TQAEP Frozen Readers、PLAN revision、Scoped WriteSet；強制 `subject_id/source_manifest_sha/scope` 來源釘選 |
| 操作／Producer | A 唯讀讀 source/effect→PlanRevisionProposal；B 只能隔離輸出 diff；C 缺 Reader 則 PARK；需原 Native PLAN CAS(base_revision,proposal_hash) ACK 才進 admission；Producer＝W1 DraftMaker（僅文字/Sidecar），正式效果由原域 Producer 執行 |
| Output／交付 | PLAN Proposal、base revision/ExpectedCAS、Recipient BindingRequest；所有未觀測 Reader Raw 留空並具名 `EXPECTED_NOT_OBSERVED` |
| Original Reader | Original HGK Native PLAN Producer+CurrentRevisionReader；原 Writer／Issuer／Checker 不因本稿改權 |
| Downstream Consumer | HGK PLAN (W2)；Native Exec；綁同 Subject／Scope，需 Original ACK 才可升級 |
| POS／Expected Raw | 原 Native CAS Reader 接受同 hash proposal；預期由原 Consumer 返回原格式 Raw（本輪 `NOT_RUN`） |
| NEG／首拒收 | 舊 `$sbl-commander-sp` 自行改 main 或自簽 WorkOrder；FirstFail=`PLAN_CAS_OR_READER_UNBOUND` |
| EDGE | base revision 漂移 -> rebase 受影 proposal；只 PARK 受影 scope，合法 READ/DRAFT 不受波及 |
| SEC | 任一 suggestion 寫入 HGK protected queue；缺憑證、Owner、ACL 或 Checker 證物拒效果 |
| Stop／Resume／Rollback | 遇 `PLAN_CAS_OR_READER_UNBOUND` 記 `hold_id+original_reader+required_raw`，停止受影寫入；Resume 需同 SourceSHA/Scope 的原 Reader 結果；READ 丟棄快照、DRAFT 刪除隔離候選；世界效果不在 W1 自行 rollback |
| Cross-wave | W2 WP06/08；交 `AUTHOR.FHS.W1ToW{next}@design` typed envelope，禁止偽裝 WorkOrder |

**受影源句拆義**：`actor/trigger/action/object`（見 Input/操作）；`condition/exception`（見 EDGE）；`prohibition`（見 NEG/SEC）；`outcome/consumer`（見 Output/Original Reader）；`POS/NEG/FirstFail` 必綁同一原 RequirementID。來源的原始句、Span、SHA、Parent/Child/NEG 以 r5 本章及附錄 `obligation_registry.jsonl` 回指；缺具體原 Reader 即 `ORIGINAL_OWNER_HOLD`，不自行創造簽核。


### R5 本章受影精確契約／業務負例（整合 r4，非歷史附錄）

Commander A 原 frozen read、B isolated `PlanRevisionProposal`、C 原 PLAN Writer CAS(expected_revision,proposal_hash) 分離；不能先等 W2 WP06 建 WorkOrder 才草擬 plan。NEG=stale base 偷蓋現行 Native PLAN → `PLAN_CAS_STALE_BASE`。


**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L26233–26296`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Native PLAN Producer；L2-r4:L924。原 Domain Reader/Writer 不因本章轉移。

## r4 當期原 Reader 鎖與非降級本體

本章 L1-r4 依以上真實行區間及原域 Reader；無單獨 R4-BEGIN 增量不等於以歷史 r2 取代 L1。W1 契約下文僅是對該 L1 已定義原義的工程操作化。

## r4 對齊之 W1 主波操作規格、草案必填欄、逐項 POS/NEG／FirstFail（高保留整合）

**Protected Original H1 / CURRENT L1-r4**：`FHS_PIPD-LS-PKG_藍圖_2026-11-04_r4_HIGH_RETENTION_AUDIT_REPAIRED_實質正文(1).md:L26233–L26296`；`source_file_sha256=cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`；`section_sha256=0738e008777ea1aefc449313e24d406dcaa6438f5ad9d195d5b5a175342edc25`；`heading_exact=# CH-34｜Portable Commander Guide A／B／C 與原 Native PLAN`；**HISTORICAL_LOCATOR_NOT_EFFECTIVE**=`L1:25394–25443` / `L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`，L2 作者端路由 `L2:672`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W1 不取得原 Writer。

## A. 本章實質功能與不能壓平的原義

Portable Commander Guide A/B/C：A readonly、B isolated proposal、C original PLAN CAS。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。

## B. 來源 r5 skeleton 必填核對欄（已由上方 W1 草案當期完成契約受影回填）

| 必填欄 | 欄位設計／不可空條件 |
|---|---|
<!-- HISTORICAL_R5_SKELETON_FILL_REQUEST_SUPERSEDED: transition wording only; all substantive constraints retained -->
| `chapter_id` / `primary_wave` / `author_writer` | `CH-34` / `W1` / `W1:DraftMaker`（歷史 r5 階段欄；當期為作者端定案候選） |
| `original_sources[]` | 本章 L1 行與下面原冊 SHA／OriginalClause Span；不得用語義假定的 ID 補空缺 |
| `same_subject` / `candidate_sha` / `source_manifest_sha` / `affected_scope` | 必攜相同 Subject/Scope，未原 Reader 認證則 `AUTHOR_CANDIDATE` |
| `effect_class` / `original_owner` / `consumer_abi` / `schema_version` | 依 Operation Reader；缺 `$id` 或 Receiver 不自造 |
| `input` / `typed_output` / `fuo` / `non_goals` | 應有真使用者結果與 Receiver（非檔案數） |
| `positive_fixture` / `negative_fixture` / `security_fixture` | 原 Source Case/Oracle 逐受影引用，未有 Runner/Raw 就 `EXPECTED_NOT_OBSERVED` |
| `first_fail` / `hold` / `stop_scope` / `resume_predicate` | 明確停止受影子圖，不全域凍結 READ／DRAFT |
| `rollback` / `w2_handoff` / `original_ack_nack` | 回退路由與 same scope 的預期接收；不得填假 PASS |

## C. Input → Producer → 原 Reader／Consumer → Output

- **Input/Guard**：Goal+KnownAnswer+W0 three SPEC+original CurrentRevisionReader/base_revision。
- **Producer**：該 Original Domain 的 Reader/Compiler/Host/Guide 依本章功能生產；W1 Curator 僅記設計；**Original Consumer**：原 HGK PLAN Writer。
- **Typed Output/FUO**：PlanRevisionProposal；CAS original ACK/NACK（本輪預期值）。
- **版本要求**：至少 `Subject,CandidateSHA,SourceSHA,OriginalID+SourceSpan,Scope,Host/PolicyEpoch（受影才填）,ABI $id/version,OriginalReader,OutputRawExpected`，少一欄只停需該欄的出口。

## D. POS／NEG／FirstFail／HOLD／退出

- **POS（期待）**：不用未建立的 WorkOrder 也能先給 source-bound plan proposal。
- **NEG／SEC（期待拒收）**：啟動 disabled legacy sbl-commander-sp 或要求 WP06 作前置。
- **FirstFail**：`COMMANDER_BOOTSTRAP_INVERSION`；禁止只有泛稱 `VALIDATION_FAILED` 而不給首次失敗位置。
- **HOLD/Owner**：`ORIGINAL_PLAN_CAS_READER_HOLD`。需同 Subject/Scope/Host/原 Reader 的真 Raw/ACK 解除；本輪 `NOT_RUN`。
- **Stop/Resume**：保留原 SourceSHA/受影 Reader/cursor/last-good；READ/DRAFT 合法部分繼續；UNKNOWN 必原 Reader reconcile。
- **Rollback**：只回復該 Need/Host 的原 last-good，Host/OPS 效果走原 inverse；不得以檔案 ZIP 作回復收據。

## E. 來源追溯、波次邊界與下一手

| 源鍵／檔案 | 原文 SHA | 此 W1 處理方式 |
|---|---|---|
| SBL-DOC-04 | ee90cb1c86f6f7350c11c9c962233a89b035ca41ff82c8968f7968608fc6f6e0 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-05 | ee47e07455767c063fd0700440b46d27592caea4638c39407b9af1309a2b44d5 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
W0 提供原 Source/三 SPEC/索引；本 `CH-34` 不修改 W0 成果。W1 WaveCurator 交 W1 DraftMaker 按原 Reader 定位填入真 Requirements；W2 僅領同 Subject/Scope 的需要的 Effect/Case/HOLD，不得借 W3/W4 收據。原 L1 CH-34 的詳細原義仍在 L1 主體，不移作本冊第二 Canonical。

## F. r2 原位修補：CH-34 可直接交接的受影實質規格（非證據附錄）

**本章不可壓平功能**：Original PLAN proposal/CAS and Commander Guide。與 W0 三份獨立 SPEC 維持同 SourceSHA/Subject/Scope；將原讀者真接收的 **Output／Consumer** 優先於填滿文件欄位。依 L1 原 CH 身份與 L2 W1 主責修訂，不移轉原 Writer。

### F.1 原句→原 Consumer→本章測例的逐子義槽（已從原物理檔定位）

- **`SCL-W1-0100`** `[SOURCE:SBL-DOC-04:L2094:sha256=ee90cb1c86f6f735]`：原文實質片段「/ SBL-PROP-D04-A151 / AUDIT §5 named slot / HLPE: long planning/budget/checkpoint donor, Checkpoint/CostBudget proposal→C37 resume / D04-SLOT-16 / R05.Projection@r4 → Technology Admission/Host owner; SPEC-SBL-P」；Parent=`L1940:#### R06.8.1｜Atom→Typed SPEC/ACC/NEG/VER/EEXP/DELIVER（165 個受影條目逐一列出）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=HGK Native PLAN Writer CAS Reader；承接 `WP 07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH34.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0101`** `[SOURCE:SBL-DOC-04:L2420:sha256=ee90cb1c86f6f735]`：原文實質片段「- **TestInput**：{"case":"NEG-D04-SECOND-WRITER","subject_sha":"<compute exact bytes>","tamper":"OpenSpec/Spec Kit writes official PI canonical","candidate_status":"FROZEN_FOR_TEST"}。**Expected**：DENY/HOLD, Firs」；Parent=`L2417:### 07.15 `NEG-D04-SECOND-WRITER` 完整預期 Fixture`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG,不得`。本章觸發/Consumer=HGK Native PLAN Writer CAS Reader；承接 `WP 07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH34.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0102`** `[SOURCE:SBL-DOC-04:L2729:sha256=ee90cb1c86f6f735]`：原文實質片段「R05.6 每張技術卡配 TechResearchDecision@1 {source_tag/full_commit_sha,source_readback_time,licence_spdx,NOTICE,SBOM,advisory_snapshot,host_compat_probe,ABI_input_output,contradicting_evidence,OwnerDecision,NoFit,Exit」；Parent=`L2727:### R09.2｜本次 20 槽逐項技術研究的合法驗證輸入（不偽造授權已定案）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NoFit,不得`。本章觸發/Consumer=HGK Native PLAN Writer CAS Reader；承接 `WP 07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH34.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0103`** `[SOURCE:FHS-BODY-05:L31:sha256=ee47e07455767c06]`：原文實質片段「/ **Native FHS-Commander** / 有權原 PLAN／Guide Request→原 Writer CAS Replan/Scope/Epoch→同 WorkID 可恢復 Cursor / 原 HGK/TPM；沒有原 Enum/Adapter 則 COMMANDER_ABI_HOLD，不得製作新 issuer。 /」；Parent=`L24:### 1.3 三 SP：Portable 與 Native 雙形態，不混 Writer／Checker`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不得`。本章觸發/Consumer=HGK Native PLAN Writer CAS Reader；承接 `WP 07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH34.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0104`** `[SOURCE:FHS-BODY-05:L45:sha256=ee47e07455767c06]`：原文實質片段「A READONLY：Portable Guide 讀 frozen SPEC/PI/PD/ECP/TQAEP、原 CurrentRevisionReader，回 PlanRevisionProposal；不需要它尚未建立的 WorkOrder，不能寫 Target Repo。B ADVISORY_LOCAL_WRITE：只在本輪隔離建議目錄記 proposal/diff，effect=LOCAL_DRAFT_WRI」；Parent=`L43:## R2-05-ABC：Guide 與 Native PLAN 的反循環輸入`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不能`。本章觸發/Consumer=HGK Native PLAN Writer CAS Reader；承接 `WP 07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH34.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0105`** `[SOURCE:FHS-BODY-05:L59:sha256=ee47e07455767c06]`：原文實質片段「已讀原HGK profiles/construction-commander/README.runtime-contract.md：Denied candidate write / AcceptanceReceipt / promotion / release。本候選Guide只產隔離proposal，該profile本身不因此獲Writer權。Native PLAN Producer/CurrentRevision」；Parent=`L51:## R2-05-ACTUAL-PLAN：原Source入口讀回`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=HGK Native PLAN Writer CAS Reader；承接 `WP 07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH34.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。

### F.2 本章 WP 與 Producer／typed I/O／FirstFail（每項獨立）

- **WP-FHS-07**：Producer=原 HGK Native PLAN Writer/Reader；Input=W0 WP15 三 SPEC/QuestionLedger、PLAN base_revision、original Native PLAN CAS Reader；Output=PlanRevisionProposal + original CAS(base_revision, proposal_hash) ACK/NACK；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=Native PLAN Commander A/B/C 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=跳過原 PLAN Writer 直接送 ECP→Issuer 或停用 legacy commander 提升成新 Gate；EDGE=兩個 proposal 同 base_revision 競逐，僅一個 Writer CAS 成功；另一個明確 NACK；FirstFail=`PLAN_CAS_STALE_BASE`；rollback=CAS mismatch 丟棄提案並重讀 base；不寫 Target Repo/second Queue。

### F.3 複合原義拆解、反向閉包與受影退出

- **「各有」**：本 CH 的每個原 clause locator 各自保留 SourceSHA/Parent/OriginalConsumer、POS/NEG；若原文有多個 named roles/Host/Case，不可用單一結果冒全數。
- **「分別」**：strict JSON body／@2 sidecar、Original Policy Active／Host Loaded、Maker challenge／Protected Checker、Selected／ActualServed 是不同欄位與收據，不得合併。
- **「對應」**：必 `original source line → SCL-W1 id → CH → W1 WP → expected Case → original source line` 可機械重算；原 OriginalID 未明者只引用明示的 SourceSpan，不可猜 ID。
- **「不得／若／除非」**：否定作用域保留到原 Parent context；本章只標作者候選，原 Source Reader 取得 ACK 才能宣告原語義接受。
- **退出**：原 Reader NACK 僅 PARK 本章受影的 PI/PD/DEV/OPS/Host operation；合法 SOURCE_READ、隔離草稿及不依賴該 ABI 的 W0/W2 工作照原許可前進。

## 本章 L2-r4 設計義務接收卡（逐 ID；不可省略原 NEG）

- `FHS-DR-008` (`L1-r4:L805`, `L2-r4:L346`)：產品／A；三 SP 均保留 Portable/Native 對照而不混權限；TPM/Commander/Challenge 各自讀合法原 Consumer；[CH-08](#ch-08)/[CH-11](#ch-11)/[CH-34](#ch-34)；POS `同 WorkID/Source/Case 的適用讀回`；NEG/FirstFail `任一 Portable Skill 自行發 Grant/Checker；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `SBL Product/Kind/Host Original Consumer`；本輪只有 EXPECTED_NOT_OBSERVED。

## CH-34 專屬退出與回退

DraftMaker 後續須填 `original_reader_ref`, `original_schema_version_or_HOLD`, `source_span_sha`, `same_subject_and_scope`, `Case/Oracle`, `positive_raw_expected`, `negative_raw_expected`, `first_fail`, `resume_predicate`, `last_good`, `consumer_ack_or_HOLD`。`DOC_AUTHOR_DONE` 是本檔可檢索，不是 `Portable Commander Guide A／B／C 與原 Native PLAN` 已原 Host Qualified。若權限／能力尚缺，只 PARK 受影操作；回退到該 Domain 上次有效 Reader/Host 版本、保留跨波合法 READ/DRAFT，且不得刪原 NEG 或憑此文件自簽。



## AUTHOR-FINAL｜CH-34 受影交付契約

**Input / Operation / Output**：保留本章原有專屬 I/O、原句與 NEG；以當期 Registry 對同 SourceSHA/Subject/Scope 重算受影子圖，輸出 CH-34 的原 Reader BindingRequest，實質輸出與業務 FirstFail 以本章上文專屬契約及下列子義為準。

**Original Reader / Original Consumer**：Original HGK PLAN Revision/CAS Reader；原 Consumer Raw=EXPECTED_NOT_OBSERVED。L1 起始 26233、終止 26296，section SHA `0738e008777ea1aefc449313e24d406dcaa6438f5ad9d195d5b5a175342edc25`。

**POS / NEG / FirstFail**：本章專屬正負條件逐筆如下；沒有適用子義的跨 ABI 章以原本章完整 POS/NEG 為準，不從別章借用 PASS。**EDGE**：SourceSHA/Host/PolicyEpoch 其中一欄改變，只 invalidate 受影接線；**SEC**：Maker 假 ACK 或跨 Principal 原回條均拒收。**ExpectedRaw**：同 Subject/Candidate/Scope 原 Consumer/World bytes；本輪 NOT_RUN。**Stop**：缺該 Effect 必需原 Reader 即 PARK 其效果；**Resume**：同 Scope 原 Reader 提供具名 Raw；**NextWave**：W2 原 Effect Receiver，四 Host/Cell/W18 交 W3，CI/Publisher 交 W4。

- `S-W1-FHS-DR-008-01`：Input=TPM／Commander／Challenge 三 SP 各有 Portable 入口；POS=3 個 Host Pack 身份獨立；NEG=把 TPM LoadedSHA 當 Challenge；FirstFail=`SP_PACK_IDENTITY_COLLISION`；Consumer=SBL Product Original Consumer and original Protected Checker；Case=`AUTHOR.W1.FHS-DR-008.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-008-02`：Input=Portable Guide 不能簽 Native Permit/Checker；POS=原 Native consumer 各有獨立 Ack；NEG=Portable Plugin 自簽 Checker；FirstFail=`PORTABLE_NATIVE_AUTHORITY_CROSSING_DENY`；Consumer=SBL Product Original Consumer and original Protected Checker；Case=`AUTHOR.W1.FHS-DR-008.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。

<a id="ch-35"></a>

# CH-35｜FHS-EXECUTE：Lease、Journal、UNKNOWN、World Reconcile

**唯一主波** `W2`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L26297–26368`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original HGK reducer/world reader；L2-r4:L925。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W2 Normative 主責）

W1 只交原受影 Effect/Repo/Host/Reader request，世界效果、TQAEP 真 Raw 與 FirstFail 由 W2 在原准入後驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W2 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L26297–26368` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-35 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-35",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W2",
  "OriginalReader": "Original HGK reducer/world reader；L2-r4:L925",
  "consumer": "Original HGK reducer/world reader；L2-r4:L925",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-35",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 26297,
    "end": 26368
  }
}
```

<a id="ch-36"></a>

# CH-36｜B1 自舉與 W18：Fresh PID 普通 Goal 的第一成果

**唯一主波** `W3`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L26369–26445`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Hermes normal-mode Host Consumer；L2-r4:L926。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W3 Normative 主責）

W1 保持此章完整源身份、Need/Host/Consumer 的交接 locator；全產品分母/普通模式及其原 Reader 由 W3 主波驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W3 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L26369–26445` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-36 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-36",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W3",
  "OriginalReader": "Hermes normal-mode Host Consumer；L2-r4:L926",
  "consumer": "Hermes normal-mode Host Consumer；L2-r4:L926",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-36",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 26369,
    "end": 26445
  }
}
```

<a id="ch-37"></a>

# CH-37｜Program SPEC：W0～W3、原 22 WP／36 DAG 邊及 W0-A/B

**唯一主波** `W0`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L26446–26989`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Program/WP Reader；L2-r4:L927。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W0 Normative 主責）

W0 的原文/Source/SPEC/QuestionLedger/Program 只有 SourceSpan+same Subject/Scope 作 W1 受影依據，W1 不重寫或簽 W0 原草案與定案。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W0 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L26446–26989` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-37 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-37",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W0",
  "OriginalReader": "Original Program/WP Reader；L2-r4:L927",
  "consumer": "Original Program/WP Reader；L2-r4:L927",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-37",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 26446,
    "end": 26989
  }
}
```

<a id="ch-38"></a>

# CH-38｜最小 Native E2E、GJ01–03、Golden/V2-T 與停止規則

**唯一主波** `W2`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L26990–27079`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original E2E/Golden Reader；L2-r4:L928。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W2 Normative 主責）

W1 只交原受影 Effect/Repo/Host/Reader request，世界效果、TQAEP 真 Raw 與 FirstFail 由 W2 在原准入後驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W2 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L26990–27079` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-38 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-38",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W2",
  "OriginalReader": "Original E2E/Golden Reader；L2-r4:L928",
  "consumer": "Original E2E/Golden Reader；L2-r4:L928",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-38",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 26990,
    "end": 27079
  }
}
```

<a id="ch-39"></a>

# CH-39｜安全：SoD、Process ACL、秘鑰、原授權、Consent/Privacy

### r2 受影修補（2026-11-05｜AUTHOR_FINAL_AFFECTED_REPAIR）

**受影 Finding**：`F-13、N-05`。**原位差額**：SoD 以原 OS principal／ACL／簽章為準；本輪僅觀測到單一 principal，故 Maker≠Checker 的技術隔離仍是 `PRINCIPAL_SOD_UNPROVEN`，受護效果不做。

**未變更**：本章 H1 標題、L1 span／section SHA、OriginalID／Parent／NEG 與原 Reader 法位皆不變；原域 Raw 未取得者維持 `EXPECTED_NOT_OBSERVED`，不以作者推斷補值。

**下一個 Reader**：Original HGK Protected Reader；FirstFail 見本章 POS／NEG／SEC 卡與 `AFFECTED_FINDINGS.jsonl` 對應列。

## W1 草案當期完成契約｜CH-39（DRAFT-W1-CH39）

**使用者可得結果**：安全/SoD/Consent/ACL；合法執行範圍限 `LOCAL_DRAFT_WRITE` 與作者端規格審閱，無真 Host 准入或新 Writer 權限。

| 受影型別 | 本章可驗證的確定規則 |
|---|---|
| Input／觸發 | single Human Owner + protected Checker distinct principal；EffectClass、SecretHandle、Scope、Consent；強制 `subject_id/source_manifest_sha/scope` 來源釘選 |
| 操作／Producer | 最小權限，Reader 把 SourceRead/Draft/Dev/Ops/User/Release 各自分派；用原 Owner 已有 scoped approval；永不把一人多角色等於技術 Principal 同一 Credential；Producer＝W1 DraftMaker（僅文字/Sidecar），正式效果由原域 Producer 執行 |
| Output／交付 | PermissionMatrix、EffectScoping、NegativeFixtures、SensitiveDataPolicy；所有未觀測 Reader Raw 留空並具名 `EXPECTED_NOT_OBSERVED` |
| Original Reader | HGK Original ACL/Issuer；User consent Reader；Protected Checker；原 Writer／Issuer／Checker 不因本稿改權 |
| Downstream Consumer | W2 protected effect；W4 Checker/Publisher；綁同 Subject／Scope，需 Original ACK 才可升級 |
| POS／Expected Raw | Read/Draft 不因 OPS token 缺失被拒，全 effect 精確閘口；預期由原 Consumer 返回原格式 Raw（本輪 `NOT_RUN`） |
| NEG／首拒收 | Maker 在自身 schema 造獨立 PASS 或寫入原 private keys；FirstFail=`SEC_EFFECT_OR_SOD_NACK` |
| EDGE | Scope/TTL/PolicyEpoch 小差額只影響相依 effect；只 PARK 受影 scope，合法 READ/DRAFT 不受波及 |
| SEC | 曝露 raw credentials/cross-scope consent；缺憑證、Owner、ACL 或 Checker 證物拒效果 |
| Stop／Resume／Rollback | 遇 `SEC_EFFECT_OR_SOD_NACK` 記 `hold_id+original_reader+required_raw`，停止受影寫入；Resume 需同 SourceSHA/Scope 的原 Reader 結果；READ 丟棄快照、DRAFT 刪除隔離候選；世界效果不在 W1 自行 rollback |
| Cross-wave | W2 security admission；W4 checker；交 `AUTHOR.FHS.W1ToW{next}@design` typed envelope，禁止偽裝 WorkOrder |

**受影源句拆義**：`actor/trigger/action/object`（見 Input/操作）；`condition/exception`（見 EDGE）；`prohibition`（見 NEG/SEC）；`outcome/consumer`（見 Output/Original Reader）；`POS/NEG/FirstFail` 必綁同一原 RequirementID。來源的原始句、Span、SHA、Parent/Child/NEG 以 r5 本章及附錄 `obligation_registry.jsonl` 回指；缺具體原 Reader 即 `ORIGINAL_OWNER_HOLD`，不自行創造簽核。


### R5 本章受影精確契約／業務負例（整合 r4，非歷史附錄）

原 Owner 可依 same Subject/Scope/Host/Epoch 復用已有效 grant/KnownAnswer；Maker/Issuer/Checker/Publisher 技術 Principal 不能借單人 Owner 名義混權。未見原 `OwnerGrantRef` schema → `OWNER_GRANT_SCHEMA_HOLD`，退回原 grant reader，不建立新 Principal。


**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L27080–27152`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Security/Consent Owner；L2-r4:L929。原 Domain Reader/Writer 不因本章轉移。

## r4 當期受影修補（直接摘取 L1 r4 本章有效增量）

## r4｜AUDIT r3 受影整合／覆蓋／取代（現行作者端規範）

**Protected Checker 技術獨立性**：同一 Human Owner 的操作便利不等於 Maker/Checker 共享唯一 Credentials；每受影 Case 需原 `Subject/Candidate/SourceSHA/Scope/Host/PolicyEpoch`、Frozen Raw、independent checker identity/role credential、original Oracle、NEG；不存在真 Checker 收據就只 `PLANNED`，即使 50 H1 或 84 卡已補齊也不提升。NEG：Maker 用另一個 GPT 角色簽 Qualified → `SELF_ATTESTED_CHECKER_NACK`。

## r4 對齊之 W1 主波操作規格、草案必填欄、逐項 POS/NEG／FirstFail（高保留整合）

**Protected Original H1 / CURRENT L1-r4**：`FHS_PIPD-LS-PKG_藍圖_2026-11-04_r4_HIGH_RETENTION_AUDIT_REPAIRED_實質正文(1).md:L27080–L27152`；`source_file_sha256=cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`；`section_sha256=1d15d487b70197195d62451b7ceab4caf1c7fa7f78627bfd1ccf0952c2cf9ad1`；`heading_exact=# CH-39｜安全：SoD、Process ACL、秘鑰、原授權、Consent/Privacy`；**HISTORICAL_LOCATOR_NOT_EFFECTIVE**=`L1:26052–26102` / `L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`，L2 作者端路由 `L2:677`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W1 不取得原 Writer。

## A. 本章實質功能與不能壓平的原義

SoD、SID/ACL、Secret、User Consent 與 effect-specific permission 各自嚴守。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。

## B. 來源 r5 skeleton 必填核對欄（已由上方 W1 草案當期完成契約受影回填）

| 必填欄 | 欄位設計／不可空條件 |
|---|---|
<!-- HISTORICAL_R5_SKELETON_FILL_REQUEST_SUPERSEDED: transition wording only; all substantive constraints retained -->
| `chapter_id` / `primary_wave` / `author_writer` | `CH-39` / `W1` / `W1:DraftMaker`（歷史 r5 階段欄；當期為作者端定案候選） |
| `original_sources[]` | 本章 L1 行與下面原冊 SHA／OriginalClause Span；不得用語義假定的 ID 補空缺 |
| `same_subject` / `candidate_sha` / `source_manifest_sha` / `affected_scope` | 必攜相同 Subject/Scope，未原 Reader 認證則 `AUTHOR_CANDIDATE` |
| `effect_class` / `original_owner` / `consumer_abi` / `schema_version` | 依 Operation Reader；缺 `$id` 或 Receiver 不自造 |
| `input` / `typed_output` / `fuo` / `non_goals` | 應有真使用者結果與 Receiver（非檔案數） |
| `positive_fixture` / `negative_fixture` / `security_fixture` | 原 Source Case/Oracle 逐受影引用，未有 Runner/Raw 就 `EXPECTED_NOT_OBSERVED` |
| `first_fail` / `hold` / `stop_scope` / `resume_predicate` | 明確停止受影子圖，不全域凍結 READ／DRAFT |
| `rollback` / `w2_handoff` / `original_ack_nack` | 回退路由與 same scope 的預期接收；不得填假 PASS |

## C. Input → Producer → 原 Reader／Consumer → Output

- **Input/Guard**：原 maker/checker principal、HostID/SID、TTL、Scopes、Consent / privacy tags。
- **Producer**：該 Original Domain 的 Reader/Compiler/Host/Guide 依本章功能生產；W1 Curator 僅記設計；**Original Consumer**：原 Security Owner、HGK Issuer、Protected Checker、User/Consent Reader。
- **Typed Output/FUO**：Threat/Permission matrix，合法 denied request/Raw 期待。
- **版本要求**：至少 `Subject,CandidateSHA,SourceSHA,OriginalID+SourceSpan,Scope,Host/PolicyEpoch（受影才填）,ABI $id/version,OriginalReader,OutputRawExpected`，少一欄只停需該欄的出口。

## D. POS／NEG／FirstFail／HOLD／退出

- **POS（期待）**：跨 OS principal 使用 token 拒絕；保護秘鑰不落正文。
- **NEG／SEC（期待拒收）**：SourceRead ACL 推出 OPS Grant、Maker 自簽、秘密傳入 ZIP。
- **FirstFail**：`NATIVE_PERMISSION_DENIED`；禁止只有泛稱 `VALIDATION_FAILED` 而不給首次失敗位置。
- **HOLD/Owner**：`H-OS-08`。需同 Subject/Scope/Host/原 Reader 的真 Raw/ACK 解除；本輪 `NOT_RUN`。
- **Stop/Resume**：保留原 SourceSHA/受影 Reader/cursor/last-good；READ/DRAFT 合法部分繼續；UNKNOWN 必原 Reader reconcile。
- **Rollback**：只回復該 Need/Host 的原 last-good，Host/OPS 效果走原 inverse；不得以檔案 ZIP 作回復收據。

## E. 來源追溯、波次邊界與下一手

| 源鍵／檔案 | 原文 SHA | 此 W1 處理方式 |
|---|---|---|
| SBL-DOC-07 | a366d3783c82089c5593ffabb0704d8507632cce45622684f7a0186f2ae310f8 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-03 | 58628861e63956ae31b1ac17404c093533226688f975f5fa11b9b82adecd1284 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-04 | a7d54bdeb9129e7e1979bbc1af1944189b1054760e76424f8ffd8547a682eb1f | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
W0 提供原 Source/三 SPEC/索引；本 `CH-39` 不修改 W0 成果。W1 WaveCurator 交 W1 DraftMaker 按原 Reader 定位填入真 Requirements；W2 僅領同 Subject/Scope 的需要的 Effect/Case/HOLD，不得借 W3/W4 收據。原 L1 CH-39 的詳細原義仍在 L1 主體，不移作本冊第二 Canonical。

## F. r2 原位修補：CH-39 可直接交接的受影實質規格（非證據附錄）

**本章不可壓平功能**：Single human owner, distinct technical principals, least permissions。與 W0 三份獨立 SPEC 維持同 SourceSHA/Subject/Scope；將原讀者真接收的 **Output／Consumer** 優先於填滿文件欄位。依 L1 原 CH 身份與 L2 W1 主責修訂，不移轉原 Writer。

### F.1 原句→原 Consumer→本章測例的逐子義槽（已從原物理檔定位）

- **`SCL-W1-0106`** `[SOURCE:SBL-DOC-07:L845:sha256=a366d3783c82089c]`：原文實質片段「/ SUPPLY-17 / GitHub Actions/OIDC. / OWNER_SOURCE_DISPOSITION_PENDING (r1 scan field MISSING_LITERAL) / OWNER_SELECT_AND_QUALIFY; UNVERIFIED; positive: source+qualified scope; negative / DOC06:C33.2.9:L844 / SB」；Parent=`L732:### C44.1bb｜DOC06 OriginalID 386/386 不覆寫安全讀取投影（r4 ACTIVE）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:neg,NEG`。本章觸發/Consumer=Original Security/Issuer/ACL/Consent Reader；承接 `WP 02/03/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH39.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0107`** `[SOURCE:SBL-DOC-07:L907:sha256=a366d3783c82089c]`：原文實質片段「/ P0-TOOL-062 / GitHub Actions / upstream=PRIMARY_ADAPTER\ / \ci.evidence_producer; disposition=DEFAULT_ENABLED_AFTER_QUALIFICATION; observed=TARGET_CONTRACT_DEFINED / OBSERVED_NOT_INSTALLED; runtime=NOT_EXECUT」；Parent=`L732:### C44.1bb｜DOC06 OriginalID 386/386 不覆寫安全讀取投影（r4 ACTIVE）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=Original Security/Issuer/ACL/Consent Reader；承接 `WP 02/03/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH39.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0108`** `[SOURCE:SBL-DOC-07:L2028:sha256=a366d3783c82089c]`：原文實質片段「**唯一先發碼**：四筆官方 FX-DOC-07-* 在受保護 FullDOC 下 no-effect、DENY_NO_NATIVE_EFFECT、PROMPT_INJECTION_DENIED、SECRET_EXPOSURE_STOP 是本冊應保留的 expected 字面。SBLDetailCode 不得拿去當原 Native wire；原生 issuer schema、版本及 CodeOwner 的 ratif」；Parent=`L2026:### R04.2b｜OriginalFirstFailID → SBLDetailCode → ConsumerWireCode 單向解譯`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不得`。本章觸發/Consumer=Original Security/Issuer/ACL/Consent Reader；承接 `WP 02/03/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH39.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0109`** `[SOURCE:FHS-BODY-03:L32:sha256=58628861e63956ae]`：原文實質片段「/ Fabric 316b691460638bdf38475c2c58aaad406aa6eb4f / FABRIC/fabric/consumers/hgk_policy_consumer.py route_event、load_router；rp002/RP002_CHANGE_CLASS_ROUTER.yaml / route_event 依 change_class 選原 HERMES_NATIVE/ORAC」；Parent=`L28:## 四庫 2026-10-30 `main` 原始碼錨定（GitHub 唯讀）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不能`。本章觸發/Consumer=Original Security/Issuer/ACL/Consent Reader；承接 `WP 02/03/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH39.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0110`** `[SOURCE:FHS-BODY-03:L75:sha256=58628861e63956ae]`：原文實質片段「NONE 只做記憶體計算；無 Permission/Receipt 欄時標 NA(no effect)，不能強迫捏造 token。LOCAL_DRAFT_WRITE 可以是 L0 隔離產物；Repo/product build 若有源碼/工具變更必為 L2。SWOF_W2_SHADOW_NO_WRITE 只有 SOURCE_READ，build 必另開 PRODUCT_BUILD_LOCAL subject，不能共用」；Parent=`L63:## R2-03-EFFECT：效果與退出按類處理`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不能`。本章觸發/Consumer=Original Security/Issuer/ACL/Consent Reader；承接 `WP 02/03/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH39.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0111`** `[SOURCE:FHS-BODY-03:L83:sha256=58628861e63956ae]`：原文實質片段「5. PlannedTQAEP → Checker request：receipt-free 計畫只列 case/oracle/fixtures；原受保護 Reader 解析 Raw、確認不同 principal 才可簽 verdict。Maker 的 expected/fixture 不得轉成 actual raw。」；Parent=`L77:## R2-03-ABI：五個 typed handoff`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不得`。本章觸發/Consumer=Original Security/Issuer/ACL/Consent Reader；承接 `WP 02/03/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH39.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0112`** `[SOURCE:FHS-BODY-04:L36:sha256=a7d54bdeb9129e7e]`：原文實質片段「/ SBL/sbl_core/modes.py / ack_signature(issuer,permit_id,subject_id,key) HMAC length-prefixed；_ack_state() 驗三欄＋Issuer Allowlist/secret / HMAC 作 ModeGate 初篩可以保留，真正 Effect 仍交原 HGK Receiver 檢 Scope/Epoch/TTL/Opera」；Parent=`L26:### 4.1 本次實查 Source 摘要（不要把假想方法寫成 HGK API）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不得`。本章觸發/Consumer=Original Security/Issuer/ACL/Consent Reader；承接 `WP 02/03/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH39.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0113`** `[SOURCE:FHS-BODY-04:L46:sha256=a7d54bdeb9129e7e]`：原文實質片段「5. **Checker Flow**：Frozen World Raw+Original Oracle+Same Subject/Candidate/Scope→原 AC15 Handoff→有獨立 Credential/ACL 之 Protected Checker 判定→原 HGK Reducer ACK/HOLD；同模型不同不保證 SoD、同 Principal 更不能。正式 Release 需原 Publi」；Parent=`L40:### 4.2 五條正式 Typed Adapter Flow：Input/Producer→輸出→Consumer、正負例`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不能`。本章觸發/Consumer=Original Security/Issuer/ACL/Consent Reader；承接 `WP 02/03/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH39.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0114`** `[SOURCE:FHS-BODY-04:L118:sha256=a7d54bdeb9129e7e]`：原文實質片段「POS：同一 Subject 的 Policy digest 在 Active/Loaded/Consumer 三 Reader 一致，原 Issuer 才檢 scope/nonce/TTL。NEG：Stage-only、別 Host Loaded、過期 epoch 或別 task served → POLICY_NOT_LOADED / FOREIGN_HOST_RECEIPT。本輪 Repo HEAD 與 Git」；Parent=`L112:## R2-04-CURRENT：五層證據與現役唯讀起跑`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG,不能`。本章觸發/Consumer=Original Security/Issuer/ACL/Consent Reader；承接 `WP 02/03/11`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH39.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。

### F.2 本章 WP 與 Producer／typed I/O／FirstFail（每項獨立）

- **WP-FHS-02**：Producer=Fabric Policy Owner → HGK policy consumer；Input=Original Fabric Policy Owner/current epoch; applicable Policy manifest SHA; HGK original policy consumer process identity；Output=ActiveEpoch+LoadedDigest+ConsumerACK（由 Fabric+HGK 原 Reader 同 Subject 讀回）；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=Fabric Policy Consumer 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=把未批准 Stage SHA 當 ActiveEpoch、HGK LoadedDigest 與 active 不符；EDGE=Owner 在 Stage 後切 epoch，舊 HGK process 尚載前 epoch；僅停受影 OPS，READ 繼續；FirstFail=`POLICY_EPOCH_LOADED_MISMATCH`；rollback=原 Fabric/HGK Owner 以原 epoch migration/inverse 回 last-good，Stage 不可當 Active。
- **WP-FHS-03**：Producer=HGK Original Registry/Issuer/Receiver；Input=原 HGK Registry、OS PID/SID、scope/nonce/TTL/ProcessACL/PolicyEpoch，非 Maker credentials；Output=IssuerReceiverBinding+original typed refusal/ACK; no self-issued Permit；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=HGK Registry / Issuer 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=用不同 PID/SID、過期 nonce、重用 TTL 或 scope widening 要求原 Issuer 放行；EDGE=在授權後 Worker PID 重啟；原 Receiver 必以新 process ACL / nonce 再認，不借舊票；FirstFail=`HGK_ISSUER_ACL_NONCE_TTL_NACK`；rollback=原 HGK Owner revoke affected grant/expire nonce, readback remaining WorkIDs，不清全域 Registry。
- **WP-FHS-11**：Producer=各 Host 原 Skill/Plugin Reader+每 SP original Consumer；Input=TPM-SP、Commander Guide-SP、Acceptance Challenge-SP 各自 artifact digest；Host compatibility+8 PIPD skills 各自 registry；Output=每 SP×Host 真 Loaded/Invoked/Used/nontrigger/Remove Raw；不共用收據；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=Portable Host Dogfood 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=用 TPM-SP 的 Loaded SHA 冒 Challenge-SP；Maker 以模型結論簽 Protected Checker；EDGE=Installed 後 loader 未 Loaded，或 Loaded 但 nontrigger 仍被啟動：不得宣稱 Used；FirstFail=`HOST_SKILL_TRIGGER_NONTRIGGER_NACK`；rollback=原 Host disable/remove entrypoint、還原 last-good manifest；清理 residue。

### F.3 複合原義拆解、反向閉包與受影退出

- **「各有」**：本 CH 的每個原 clause locator 各自保留 SourceSHA/Parent/OriginalConsumer、POS/NEG；若原文有多個 named roles/Host/Case，不可用單一結果冒全數。
- **「分別」**：strict JSON body／@2 sidecar、Original Policy Active／Host Loaded、Maker challenge／Protected Checker、Selected／ActualServed 是不同欄位與收據，不得合併。
- **「對應」**：必 `original source line → SCL-W1 id → CH → W1 WP → expected Case → original source line` 可機械重算；原 OriginalID 未明者只引用明示的 SourceSpan，不可猜 ID。
- **「不得／若／除非」**：否定作用域保留到原 Parent context；本章只標作者候選，原 Source Reader 取得 ACK 才能宣告原語義接受。
- **退出**：原 Reader NACK 僅 PARK 本章受影的 PI/PD/DEV/OPS/Host operation；合法 SOURCE_READ、隔離草稿及不依賴該 ABI 的 W0/W2 工作照原許可前進。

## 本章 L2-r4 設計義務接收卡（逐 ID；不可省略原 NEG）

- `FHS-DR-032` (`L1-r4:L829`, `L2-r4:L370`)：治理／B/PROTECTED；不同技術 Principal 不能被 GPT persona 假造；runtime user SID 與維護 Token 實際隔離；[CH-18](#ch-18)/[CH-39](#ch-39)；POS `直接修改 HGK 的一般 Profile 被拒`；NEG/FirstFail `兩個 Hermes Profile 名稱即宣稱 OS 隔離；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `HGK Original Issuer/SharedSpine/Protected Checker Reader`；本輪只有 EXPECTED_NOT_OBSERVED。

## CH-39 專屬退出與回退

DraftMaker 後續須填 `original_reader_ref`, `original_schema_version_or_HOLD`, `source_span_sha`, `same_subject_and_scope`, `Case/Oracle`, `positive_raw_expected`, `negative_raw_expected`, `first_fail`, `resume_predicate`, `last_good`, `consumer_ack_or_HOLD`。`DOC_AUTHOR_DONE` 是本檔可檢索，不是 `安全：SoD、Process ACL、秘鑰、原授權、Consent/Privacy` 已原 Host Qualified。若權限／能力尚缺，只 PARK 受影操作；回退到該 Domain 上次有效 Reader/Host 版本、保留跨波合法 READ/DRAFT，且不得刪原 NEG 或憑此文件自簽。



## AUTHOR-FINAL｜CH-39 受影交付契約

**Input / Operation / Output**：保留本章原有專屬 I/O、原句與 NEG；以當期 Registry 對同 SourceSHA/Subject/Scope 重算受影子圖，輸出 CH-39 的原 Reader BindingRequest，實質輸出與業務 FirstFail 以本章上文專屬契約及下列子義為準。

**Original Reader / Original Consumer**：Original OS ACL/Issuer/Protected Checker Reader；原 Consumer Raw=EXPECTED_NOT_OBSERVED。L1 起始 27080、終止 27152，section SHA `1d15d487b70197195d62451b7ceab4caf1c7fa7f78627bfd1ccf0952c2cf9ad1`。

**POS / NEG / FirstFail**：本章專屬正負條件逐筆如下；沒有適用子義的跨 ABI 章以原本章完整 POS/NEG 為準，不從別章借用 PASS。**EDGE**：SourceSHA/Host/PolicyEpoch 其中一欄改變，只 invalidate 受影接線；**SEC**：Maker 假 ACK 或跨 Principal 原回條均拒收。**ExpectedRaw**：同 Subject/Candidate/Scope 原 Consumer/World bytes；本輪 NOT_RUN。**Stop**：缺該 Effect 必需原 Reader 即 PARK 其效果；**Resume**：同 Scope 原 Reader 提供具名 Raw；**NextWave**：W2 原 Effect Receiver，四 Host/Cell/W18 交 W3，CI/Publisher 交 W4。

- `S-W1-FHS-DR-032-01`：Input=單人 Owner 不等於 Maker/Issuer/Checker 技術混權；POS=原 Host OS principle 不同且 ACL 有拒絕；NEG=建立兩個 Profile 名就算 OS 隔離；FirstFail=`OS_PRINCIPAL_SEPARATION_UNVERIFIED`；Consumer=HGK original OS ACL/Protected Checker Reader；Case=`AUTHOR.W1.FHS-DR-032.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-032-02`：Input=普通 Runtime 不可直接改 Protected Authority；POS=原 ACL deny 測例可重播；NEG=Maker 讀取並使用 Checker credential；FirstFail=`MAKER_CHECKER_CREDENTIAL_DENY`；Consumer=HGK original OS ACL/Protected Checker Reader；Case=`AUTHOR.W1.FHS-DR-032.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。

<a id="ch-40"></a>

# CH-40｜三 SPEC／PI／PD／ECP／TQAEP 對原 Reader 的交接矩陣

### r2 受影修補（2026-11-05｜AUTHOR_FINAL_AFFECTED_REPAIR）

**受影 Finding**：`F-06、F-09、N-07、N-08`。**原位差額**：交接矩陣四份 Envelope 的 Subject／Scope／Source／Candidate／Host／Epoch 逐欄綁定；W0→W1 保留原 W0 Subject，W1→W2/3/4 綁 r2 candidate；三 SPEC 角色不合併。

**未變更**：本章 H1 標題、L1 span／section SHA、OriginalID／Parent／NEG 與原 Reader 法位皆不變；原域 Raw 未取得者維持 `EXPECTED_NOT_OBSERVED`，不以作者推斷補值。

**下一個 Reader**：Original W1/W2/W3/W4 Readers；FirstFail 見本章 POS／NEG／SEC 卡與 `AFFECTED_FINDINGS.jsonl` 對應列。

## W1 草案當期完成契約｜CH-40（DRAFT-W1-CH40）

**使用者可得結果**：三 SPEC→PI/PD/ECP/TQAEP 原 Reader handoff；合法執行範圍限 `LOCAL_DRAFT_WRITE` 與作者端規格審閱，無真 Host 准入或新 Writer 權限。

| 受影型別 | 本章可驗證的確定規則 |
|---|---|
| Input／觸發 | three distinct SPEC refs、same Subject/Scope、Original SourceManifest、OriginalID/NEG、Case Registry；強制 `subject_id/source_manifest_sha/scope` 來源釘選 |
| 操作／Producer | 依七段 Intent→Authority→Profile→PI→PD→ECP→TQAEP 使用每一原 Reader、SID/ABI、POS/NEG；文件包只產 Candidate Envelope，不新建另一 canonical graph；Producer＝W1 DraftMaker（僅文字/Sidecar），正式效果由原域 Producer 執行 |
| Output／交付 | W1CandidateHandoff@design、每段 Reader ACK/NACK/ErrorEnvelope、next owner/stop/resume；所有未觀測 Reader Raw 留空並具名 `EXPECTED_NOT_OBSERVED` |
| Original Reader | SBL Canonical PIPD Reader+Original Host/Checker Reader；原 Writer／Issuer／Checker 不因本稿改權 |
| Downstream Consumer | W2 source-bound plan/Effect; W4 trace closure；綁同 Subject／Scope，需 Original ACK 才可升級 |
| POS／Expected Raw | 原 SBL Reader 可重算 artifact hash 和 lineage；預期由原 Consumer 返回原格式 Raw（本輪 `NOT_RUN`） |
| NEG／首拒收 | 缺 PI 仍自信已完成 PD／Receiver ACK；將自己的測試當 Checker；FirstFail=`PIPD_HANDOFF_READER_HOLD` |
| EDGE | Source/Repo/Policy變更只重跑受影段；只 PARK 受影 scope，合法 READ/DRAFT 不受波及 |
| SEC | 用成功字串假造原 Registry receipt；缺憑證、Owner、ACL 或 Checker 證物拒效果 |
| Stop／Resume／Rollback | 遇 `PIPD_HANDOFF_READER_HOLD` 記 `hold_id+original_reader+required_raw`，停止受影寫入；Resume 需同 SourceSHA/Scope 的原 Reader 結果；READ 丟棄快照、DRAFT 刪除隔離候選；世界效果不在 W1 自行 rollback |
| Cross-wave | W2 WP06/08；W4 final trace；交 `AUTHOR.FHS.W1ToW{next}@design` typed envelope，禁止偽裝 WorkOrder |

**受影源句拆義**：`actor/trigger/action/object`（見 Input/操作）；`condition/exception`（見 EDGE）；`prohibition`（見 NEG/SEC）；`outcome/consumer`（見 Output/Original Reader）；`POS/NEG/FirstFail` 必綁同一原 RequirementID。來源的原始句、Span、SHA、Parent/Child/NEG 以 r5 本章及附錄 `obligation_registry.jsonl` 回指；缺具體原 Reader 即 `ORIGINAL_OWNER_HOLD`，不自行創造簽核。


### R5 本章受影精確契約／業務負例（整合 r4，非歷史附錄）

明列 W1 DOC→original reader→W2 Native World→W3 W18→W4 Publisher 五個 FUO/Receiver。W1 blueprint author accepted、W1 scoped author-final、Original Domain Effective 是三個不同法位；W1→W3/W4 非權威 TypedProjection 另見上段，不可把 PRE_READ_16 當 192/192、或把 Maker/gstack 當 protected Checker。


**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L27153–27225`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original PIPD + affected Host Receiver；L2-r4:L930。原 Domain Reader/Writer 不因本章轉移。

## r4 當期原 Reader 鎖與非降級本體

本章 L1-r4 依以上真實行區間及原域 Reader；無單獨 R4-BEGIN 增量不等於以歷史 r2 取代 L1。W1 契約下文僅是對該 L1 已定義原義的工程操作化。

## r4 對齊之 W1 主波操作規格、草案必填欄、逐項 POS/NEG／FirstFail（高保留整合）

**Protected Original H1 / CURRENT L1-r4**：`FHS_PIPD-LS-PKG_藍圖_2026-11-04_r4_HIGH_RETENTION_AUDIT_REPAIRED_實質正文(1).md:L27153–L27225`；`source_file_sha256=cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`；`section_sha256=d4108e3b235e8dff2a7409cf6a334a5b44b99da807b4f66a7d963232cd32320a`；`heading_exact=# CH-40｜三 SPEC／PI／PD／ECP／TQAEP 對原 Reader 的交接矩陣`；**HISTORICAL_LOCATOR_NOT_EFFECTIVE**=`L1:26103–26161` / `L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`，L2 作者端路由 `L2:678`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W1 不取得原 Writer。

## A. 本章實質功能與不能壓平的原義

三 SPEC→PI→PD→ECP→TQAEP 五 Seam 逐出口、原 Writer/Consumer/ACK-NACK 閉環。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。

## B. 來源 r5 skeleton 必填核對欄（已由上方 W1 草案當期完成契約受影回填）

| 必填欄 | 欄位設計／不可空條件 |
|---|---|
<!-- HISTORICAL_R5_SKELETON_FILL_REQUEST_SUPERSEDED: transition wording only; all substantive constraints retained -->
| `chapter_id` / `primary_wave` / `author_writer` | `CH-40` / `W1` / `W1:DraftMaker`（歷史 r5 階段欄；當期為作者端定案候選） |
| `original_sources[]` | 本章 L1 行與下面原冊 SHA／OriginalClause Span；不得用語義假定的 ID 補空缺 |
| `same_subject` / `candidate_sha` / `source_manifest_sha` / `affected_scope` | 必攜相同 Subject/Scope，未原 Reader 認證則 `AUTHOR_CANDIDATE` |
| `effect_class` / `original_owner` / `consumer_abi` / `schema_version` | 依 Operation Reader；缺 `$id` 或 Receiver 不自造 |
| `input` / `typed_output` / `fuo` / `non_goals` | 應有真使用者結果與 Receiver（非檔案數） |
| `positive_fixture` / `negative_fixture` / `security_fixture` | 原 Source Case/Oracle 逐受影引用，未有 Runner/Raw 就 `EXPECTED_NOT_OBSERVED` |
| `first_fail` / `hold` / `stop_scope` / `resume_predicate` | 明確停止受影子圖，不全域凍結 READ／DRAFT |
| `rollback` / `w2_handoff` / `original_ack_nack` | 回退路由與 same scope 的預期接收；不得填假 PASS |

## C. Input → Producer → 原 Reader／Consumer → Output

- **Input/Guard**：W0 three distinct specs+Original IDs、SourceSHA、PI、true RepoContext、EffectClass、original Case registry。
- **Producer**：該 Original Domain 的 Reader/Compiler/Host/Guide 依本章功能生產；W1 Curator 僅記設計；**Original Consumer**：原 PIPD Reader / HGK adapter / 原 TQAEP Case Reader。
- **Typed Output/FUO**：原 canonical PI/PD/ECP/TQAEP candidates + @2 sidecars；W2 handoff typed binding requests。
- **版本要求**：至少 `Subject,CandidateSHA,SourceSHA,OriginalID+SourceSpan,Scope,Host/PolicyEpoch（受影才填）,ABI $id/version,OriginalReader,OutputRawExpected`，少一欄只停需該欄的出口。

## D. POS／NEG／FirstFail／HOLD／退出

- **POS（期待）**：同 Subject/Scope/SourceSHA 的原 Receiver response 和 POS/NEG fixture。
- **NEG／SEC（期待拒收）**：Skeleton seal 或 planned TQAEP 當 Qualified、混用 DEV OPS ECP。
- **FirstFail**：`PIPD_HANDOFF_CEILING_VIOLATION`；禁止只有泛稱 `VALIDATION_FAILED` 而不給首次失敗位置。
- **HOLD/Owner**：`H-PIPD-04/ORIGINAL_TQAEP_EXPORT_HOLD`。需同 Subject/Scope/Host/原 Reader 的真 Raw/ACK 解除；本輪 `NOT_RUN`。
- **Stop/Resume**：保留原 SourceSHA/受影 Reader/cursor/last-good；READ/DRAFT 合法部分繼續；UNKNOWN 必原 Reader reconcile。
- **Rollback**：只回復該 Need/Host 的原 last-good，Host/OPS 效果走原 inverse；不得以檔案 ZIP 作回復收據。

## E. 來源追溯、波次邊界與下一手

| 源鍵／檔案 | 原文 SHA | 此 W1 處理方式 |
|---|---|---|
| SBL-DOC-05 | 3b47a0b6224b1984a4047cf53aac5ac50615c93a560fea46e1b43d079a5d9f27 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| SBL-DOC-08 | c7029c1ff07abe3135d33d3abf858a5fecedd911b494cd69c16eb1ddb8158288 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-02 | c336d3d9d702834e84bc2e45037e21e6ac56fb99c7abcb3adea372d901824ea2 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
| FHS-BODY-12 | e4f7512a27ecbec1ce6a4569654ce33c4bf3265361a5ec141418a313fd25dd45 | 原文定位於 03；未 original U0–U4 ratified＝HOLD |
W0 提供原 Source/三 SPEC/索引；本 `CH-40` 不修改 W0 成果。W1 WaveCurator 交 W1 DraftMaker 按原 Reader 定位填入真 Requirements；W2 僅領同 Subject/Scope 的需要的 Effect/Case/HOLD，不得借 W3/W4 收據。原 L1 CH-40 的詳細原義仍在 L1 主體，不移作本冊第二 Canonical。

## F. r2 原位修補：CH-40 可直接交接的受影實質規格（非證據附錄）

**本章不可壓平功能**：Three SPEC→PI/PD/ECP/TQAEP actual original receiver。與 W0 三份獨立 SPEC 維持同 SourceSHA/Subject/Scope；將原讀者真接收的 **Output／Consumer** 優先於填滿文件欄位。依 L1 原 CH 身份與 L2 W1 主責修訂，不移轉原 Writer。

### F.1 原句→原 Consumer→本章測例的逐子義槽（已從原物理檔定位）

- **`SCL-W1-0115`** `[SOURCE:SBL-DOC-05:L986:sha256=3b47a0b6224b1984]`：原文實質片段「TaskSpecSeed{pi_ref,requirements,acceptance_hints,prohibited_effects}、WorkOrder{native_order_id,subject_hash,actor,scope,change_set_ref,tests,ecp_ref} 為**上游正式 TypedRef 的消費投影**，由 HGK/SWOF/PIPD 相應原生 Writer 產生；DOC」；Parent=`L982:### R03.1.A｜TaskSpecSeed→WorkOrder 的唯一原生 Writer：原版反證與核心設計保留`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH40.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0116`** `[SOURCE:SBL-DOC-05:L5858:sha256=3b47a0b6224b1984]`：原文實質片段「/ SBL_PIPD-LS-PKG_DOC-05_藍圖+skeleton.md#L873 / C28.4 授權矩陣與失敗補償 / D05-ATOM-028 → SBL-D05-SPEC-ATOM-028（承接 C28 的具名 Typed IO；同來源 digest、subject_sha） / ACC-D05-ATOM-028：至少原子 source_ref+owner+非空可解析 Typed Output；FX-D」；Parent=`L5825:## R08.6｜52 個歷史 H2 → 原始 Clause／原子 SPEC／ACC／雙向 Fixture／EExp／DELIVER（作者端候選）`；原 ID=`SPEC-ATOM-028`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH40.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0117`** `[SOURCE:SBL-DOC-05:L5878:sha256=3b47a0b6224b1984]`：原文實質片段「/ SBL_PIPD-LS-PKG_DOC-05_藍圖+skeleton.md#L2519 / R10.3 Release 與跨件下游準備（而非本次發布） / D05-ATOM-048 → SBL-D05-SPEC-ATOM-048（承接 R10 的具名 Typed IO；同來源 digest、subject_sha） / ACC-D05-ATOM-048：至少原子 source_ref+owner+非空可解析 Ty」；Parent=`L5825:## R08.6｜52 個歷史 H2 → 原始 Clause／原子 SPEC／ACC／雙向 Fixture／EExp／DELIVER（作者端候選）`；原 ID=`SPEC-ATOM-048`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH40.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0118`** `[SOURCE:SBL-DOC-08:L5606:sha256=c7029c1ff07abe31]`：原文實質片段「/ U14.4 / SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L5517 / SBL_PIPD-LS-PKG_總藍圖(4).md:L287 / TPM 具名對應 OPS ECP、DEV ECP 分別 / (L5517) / TPM_PRODUCT_PIPD_OWNER / ECP_Route.ops_dev_subject_binding / ECP_Route.ops_dev_」；Parent=`L5559:## R08-03.1｜原意恢復算法與拒絕殘句自稱條款`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH40.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0119`** `[SOURCE:SBL-DOC-08:L5615:sha256=c7029c1ff07abe31]`：原文實質片段「/ U17.4 / SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L5520 / SBL_PIPD-LS-PKG_總藍圖(4).md:L296 / Commander 完整理解凍結 PI/PD／ECP／TQAEP / TQAEP (L5520) / CAPC_COMMANDER_OWNER / Commander_Readset.tqaep_not_overwritten / Com」；Parent=`L5559:## R08-03.1｜原意恢復算法與拒絕殘句自稱條款`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH40.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0120`** `[SOURCE:SBL-DOC-08:L5626:sha256=c7029c1ff07abe31]`：原文實質片段「/ U22.2 / SBL｜SpecBuild Loop：整合工程總藍圖_v2.0r1(1).md:L5525 / SBL_PIPD-LS-PKG_總藍圖(4).md:L307 / HGK Commander Profile 接收 Prompt/Handoff並控制任務路由 / Handoff並控制任務路由 (L5525) / HGK_FABRIC_OWNER / HGK_Commander_Profile.type」；Parent=`L5559:## R08-03.1｜原意恢復算法與拒絕殘句自稱條款`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH40.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0121`** `[SOURCE:FHS-BODY-02:L32:sha256=c336d3d9d702834e]`：原文實質片段「K0 ImmutableCorpusBundle：14 SBL＋10 PIPD DOC bytes/sha/Owner/License→原 Host Reader，24/24 可校驗；K1 ClauseIndex：Heading/Line/TextSHA/ACL 索引；K2 SupersessionConflictRegistry：依同 Domain Writer/Scope/Supersedes 判 current」；Parent=`L30:### 2.1 K0→K3 Cold Host 導入，不要求使用者重上傳24 DOC`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不能`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH40.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0122`** `[SOURCE:FHS-BODY-02:L411:sha256=c336d3d9d702834e]`：原文實質片段「7. pipd-assurance-tqaep：本輪為 SBL.PlannedTQAEP@1，每原 atom/case 有 POS/NEG、Oracle/fixture、raw expectation；真 TQAEP 的 checker_execution_receipt 必須是不同 principal、真正受保護 Reader 提供，禁止 SELF_ATTESTED。」；Parent=`L403:## 依 sbl-tpm-sp 實讀 SkillContract 的八階候選包（不冒正式 Canonical）`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:NEG,禁止`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH40.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0123`** `[SOURCE:FHS-BODY-02:L457:sha256=c336d3d9d702834e]`：原文實質片段「/ PM:T4 / ['productspecdraft', 'acc_neg', 'source_sha256'] → issue user-facing POS/NEG proposal, not Native verdict → ProductAcceptanceProposal@1(pos,neg,raw_expect) / ProductOwner → ProductOwner/PIPD Reader / 」；Parent=`L447:## R2-02-STAGE：K0–K3 與原18-stage投影`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:neg,NEG`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH40.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0124`** `[SOURCE:FHS-BODY-12:L18:sha256=e4f7512a27ecbec1]`：原文實質片段「一次輕量全局一致性回歸核完整17冊/14SBL升級冊、2221原ID唯一Locator、原負例與未受影內容保留、來源/Reader SHA、原DAG、Schema、relative links、原工作樹未改，最後兩ZIP各只正式封裝一次並逐檔讀回。成功只標PIPD_CONSTRUCTION_HANDOFF_READY，不得讀為NATIVE_ADMITTED、NATIVE_VERIFIED、INDEPENDENT_PA」；Parent=`L14:## HANDOFF-v1｜最小交接靜態驗收與 ClaimCeiling`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`EXPLICIT:不得`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH40.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0125`** `[SOURCE:FHS-BODY-12:L55:sha256=e4f7512a27ecbec1]`：原文實質片段「/ 10B / 27 PI/31 PD Edge OBS/DEV/OPS/USER / 原 Effect/ECP/TQAEP Consumer、Exact Oracle /」；Parent=`L37:### 11.2 BODY-00～12 逐冊實質修改與輸出`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH40.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0126`** `[SOURCE:FHS-BODY-12:L139:sha256=e4f7512a27ecbec1]`：原文實質片段「Goal「為普通目標產來源綁定變更規格」→ PM/SE/TPgM 三 SPEC（Portable TPM producer）→ IntentCard/Authority/Profile 候選（原 PIPD Reader）→ PI 候選（原 Writer ACK 前不 promotion）→ 真 RepoContext 的 PD 候選→DEV/OPS ECP 候選分開→Native PLAN proposal→Fabr」；Parent=`L137:## R2-12-JOURNEY：同一 Subject 的可逆作者端切片`；原 ID=`ORIGINAL_ID_READER_HOLD`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 05/07`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CH40.SRC`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0153`** `[SOURCE:FHS-BODY-09B:L47:sha256=aed2234821768307]`：原文實質片段「### CELL-6582a70fd427｜CLI_TOOL/STANDALONE｜Codex｜legacy=ON」；Parent=`L33:### CELL-e8a4077d37ad｜CLI_TOOL/STANDALONE｜Hermes Agent｜legacy=OFF`；原 ID=`CELL-6582a70fd427`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CELL.SELECTED_SCOPE_ONLY`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0154`** `[SOURCE:FHS-BODY-09B:L61:sha256=aed2234821768307]`：原文實質片段「### CELL-434c21c50bc3｜CLI_TOOL/STANDALONE｜Codex｜legacy=OFF」；Parent=`L47:### CELL-6582a70fd427｜CLI_TOOL/STANDALONE｜Codex｜legacy=ON`；原 ID=`CELL-434c21c50bc3`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CELL.SELECTED_SCOPE_ONLY`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0157`** `[SOURCE:FHS-BODY-09B:L271:sha256=aed2234821768307]`：原文實質片段「### CELL-62767ea0b8e8｜CLI_TOOL/SWOF_CONNECTED｜Codex｜legacy=ON」；Parent=`L257:### CELL-09a9c6d13bb7｜CLI_TOOL/SWOF_CONNECTED｜Hermes Agent｜legacy=OFF`；原 ID=`CELL-62767ea0b8e8`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CELL.SELECTED_SCOPE_ONLY`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0158`** `[SOURCE:FHS-BODY-09B:L285:sha256=aed2234821768307]`：原文實質片段「### CELL-739b3b5375fc｜CLI_TOOL/SWOF_CONNECTED｜Codex｜legacy=OFF」；Parent=`L271:### CELL-62767ea0b8e8｜CLI_TOOL/SWOF_CONNECTED｜Codex｜legacy=ON`；原 ID=`CELL-739b3b5375fc`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CELL.SELECTED_SCOPE_ONLY`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0161`** `[SOURCE:FHS-BODY-09B:L383:sha256=aed2234821768307]`：原文實質片段「### CELL-cab792bba33a｜AGENT_SKILL/STANDALONE｜Codex｜legacy=ON」；Parent=`L369:### CELL-a488c020ca0b｜AGENT_SKILL/STANDALONE｜Hermes Agent｜legacy=OFF`；原 ID=`CELL-cab792bba33a`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CELL.SELECTED_SCOPE_ONLY`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0162`** `[SOURCE:FHS-BODY-09B:L397:sha256=aed2234821768307]`：原文實質片段「### CELL-220de7b8b1e7｜AGENT_SKILL/STANDALONE｜Codex｜legacy=OFF」；Parent=`L383:### CELL-cab792bba33a｜AGENT_SKILL/STANDALONE｜Codex｜legacy=ON`；原 ID=`CELL-220de7b8b1e7`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CELL.SELECTED_SCOPE_ONLY`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0165`** `[SOURCE:FHS-BODY-09B:L607:sha256=aed2234821768307]`：原文實質片段「### CELL-75634c7787b2｜AGENT_SKILL/SWOF_CONNECTED｜Codex｜legacy=ON」；Parent=`L593:### CELL-aab24b0f82f9｜AGENT_SKILL/SWOF_CONNECTED｜Hermes Agent｜legacy=OFF`；原 ID=`CELL-75634c7787b2`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CELL.SELECTED_SCOPE_ONLY`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。
- **`SCL-W1-0166`** `[SOURCE:FHS-BODY-09B:L621:sha256=aed2234821768307]`：原文實質片段「### CELL-e341b6d0f605｜AGENT_SKILL/SWOF_CONNECTED｜Codex｜legacy=OFF」；Parent=`L607:### CELL-75634c7787b2｜AGENT_SKILL/SWOF_CONNECTED｜Codex｜legacy=ON`；原 ID=`CELL-e341b6d0f605`；NEG=`NOT_EXPLICIT_IN_THIS_LINE; ORIGINAL_PARENT_NEG_HOLD`。本章觸發/Consumer=PIPD original PI/PD/ECP/TQAEP + downstream Consumer；承接 `WP 20`，POS=原 Reader 以**同 SourceSHA+Scope** 可重算需求/取得對應具名輸出，NEG=不接受脫離原 Parent、跨 Host/Scope 借收據或抹去原禁令；Case=`DESIGN.CELL.SELECTED_SCOPE_ONLY`；未有 Original Reader 補全時標 `ORIGINAL_ID_OR_PARENT_READER_HOLD`，不是已核簽。

### F.2 本章 WP 與 Producer／typed I/O／FirstFail（每項獨立）

- **WP-FHS-05**：Producer=SBL-hosted original PIPD Compiler/Reader；Input=三份不同 SPECDraft、原 SourceManifest/Authority/Profile safety veto、原 PIPD Writer version；Output=非空 strict PI，真 RepoContext 才有 PD，DEV/OPS EffectIntent 分開，PlannedTQAEP 不冒 Checker；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=PIPD Native Compiler 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=把 _profile_meta 側掛塞進 strict PI；或憑 Caller HEAD 虛構本機 Repo binding；EDGE=PI SourceSHA 不變而 RepoHEAD 改變，只使 PD/ECP stale；不可偷重寫 PI requirement 原義；FirstFail=`PIPD_STRICT_SCHEMA_OR_SOURCE_NACK`；rollback=隔離候選刪除/回復 preimage；SourceSHA/HEAD 變更僅重編受影 PD/ECP。
- **WP-FHS-07**：Producer=原 HGK Native PLAN Writer/Reader；Input=W0 WP15 三 SPEC/QuestionLedger、PLAN base_revision、original Native PLAN CAS Reader；Output=PlanRevisionProposal + original CAS(base_revision, proposal_hash) ACK/NACK；原 Reader 未綁需 `ORIGINAL_SCHEMA_BIND_HOLD`；POS=Native PLAN Commander A/B/C 的可觀察原 Consumer 功能，不是本章文字 PASS；NEG=跳過原 PLAN Writer 直接送 ECP→Issuer 或停用 legacy commander 提升成新 Gate；EDGE=兩個 proposal 同 base_revision 競逐，僅一個 Writer CAS 成功；另一個明確 NACK；FirstFail=`PLAN_CAS_STALE_BASE`；rollback=CAS mismatch 丟棄提案並重讀 base；不寫 Target Repo/second Queue。

### F.3 複合原義拆解、反向閉包與受影退出

- **「各有」**：本 CH 的每個原 clause locator 各自保留 SourceSHA/Parent/OriginalConsumer、POS/NEG；若原文有多個 named roles/Host/Case，不可用單一結果冒全數。
- **「分別」**：strict JSON body／@2 sidecar、Original Policy Active／Host Loaded、Maker challenge／Protected Checker、Selected／ActualServed 是不同欄位與收據，不得合併。
- **「對應」**：必 `original source line → SCL-W1 id → CH → W1 WP → expected Case → original source line` 可機械重算；原 OriginalID 未明者只引用明示的 SourceSpan，不可猜 ID。
- **「不得／若／除非」**：否定作用域保留到原 Parent context；本章只標作者候選，原 Source Reader 取得 ACK 才能宣告原語義接受。
- **退出**：原 Reader NACK 僅 PARK 本章受影的 PI/PD/DEV/OPS/Host operation；合法 SOURCE_READ、隔離草稿及不依賴該 ABI 的 W0/W2 工作照原許可前進。

## 本章 L2-r4 設計義務接收卡（逐 ID；不可省略原 NEG）

- `FHS-DR-030` (`L1-r4:L827`, `L2-r4:L368`)：治理／A＋B；Fabric Policy/FAR 原 Reader/Consumer 可實際回讀；PolicyEpoch/RequiredSet/Producer/Original R8 Consumer ACK；[CH-17](#ch-17)/[CH-40](#ch-40)；POS `R8 真 ACK 不被研究文件代替`；NEG/FirstFail `工具回應被視為 Policy Applied；`DESIGN_OBLIGATION_MISSING`（若失卡）`；原 Receiver `Fabric FHS Navigation/Policy/FAR Reader → Original Consumer`；本輪只有 EXPECTED_NOT_OBSERVED。

## CH-40 專屬退出與回退

DraftMaker 後續須填 `original_reader_ref`, `original_schema_version_or_HOLD`, `source_span_sha`, `same_subject_and_scope`, `Case/Oracle`, `positive_raw_expected`, `negative_raw_expected`, `first_fail`, `resume_predicate`, `last_good`, `consumer_ack_or_HOLD`。`DOC_AUTHOR_DONE` 是本檔可檢索，不是 `三 SPEC／PI／PD／ECP／TQAEP 對原 Reader 的交接矩陣` 已原 Host Qualified。若權限／能力尚缺，只 PARK 受影操作；回退到該 Domain 上次有效 Reader/Host 版本、保留跨波合法 READ/DRAFT，且不得刪原 NEG 或憑此文件自簽。



## AUTHOR-FINAL｜CH-40 受影交付契約

**Input / Operation / Output**：保留本章原有專屬 I/O、原句與 NEG；以當期 Registry 對同 SourceSHA/Subject/Scope 重算受影子圖，輸出 CH-40 的原 Reader BindingRequest，實質輸出與業務 FirstFail 以本章上文專屬契約及下列子義為準。

**Original Reader / Original Consumer**：SBL/Fabric/HGK Original Receiver；原 Consumer Raw=EXPECTED_NOT_OBSERVED。L1 起始 27153、終止 27225，section SHA `d4108e3b235e8dff2a7409cf6a334a5b44b99da807b4f66a7d963232cd32320a`。

**POS / NEG / FirstFail**：本章專屬正負條件逐筆如下；沒有適用子義的跨 ABI 章以原本章完整 POS/NEG 為準，不從別章借用 PASS。**EDGE**：SourceSHA/Host/PolicyEpoch 其中一欄改變，只 invalidate 受影接線；**SEC**：Maker 假 ACK 或跨 Principal 原回條均拒收。**ExpectedRaw**：同 Subject/Candidate/Scope 原 Consumer/World bytes；本輪 NOT_RUN。**Stop**：缺該 Effect 必需原 Reader 即 PARK 其效果；**Resume**：同 Scope 原 Reader 提供具名 Raw；**NextWave**：W2 原 Effect Receiver，四 Host/Cell/W18 交 W3，CI/Publisher 交 W4。

- `S-W1-FHS-DR-030-01`：Input=Fabric Source/Stage/Approval/Active 各獨立；POS=Active epoch 與源 hash 可回讀；NEG=只有 stage 就宣 Active；FirstFail=`POLICY_STAGE_AS_ACTIVE_NACK`；Consumer=Fabric Policy Owner and HGK R8 Consumer；Case=`AUTHOR.W1.FHS-DR-030.01.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。
- `S-W1-FHS-DR-030-02`：Input=HGK Loaded epoch/Consumer ACK 同 Scope 另有證據；POS=original R8 Consumer Raw 狀態；NEG=工具回應即視為 Policy Applied；FirstFail=`POLICY_LOADED_CONSUMER_ACK_MISSING`；Consumer=Fabric Policy Owner and HGK R8 Consumer；Case=`AUTHOR.W1.FHS-DR-030.02.NEG`；OriginalID/Parent/Oracle=`ORIGINAL_OWNER_HOLD`。

<a id="ch-41"></a>

# CH-41｜TQAEP：POS／NEG／FirstFail／獨立 Oracle 的可執行計畫

**唯一主波** `W2`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L27226–27298`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Oracle/Protected Checker；L2-r4:L931。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W2 Normative 主責）

W1 只交原受影 Effect/Repo/Host/Reader request，世界效果、TQAEP 真 Raw 與 FirstFail 由 W2 在原准入後驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W2 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L27226–27298` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-41 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-41",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W2",
  "OriginalReader": "Original Oracle/Protected Checker；L2-r4:L931",
  "consumer": "Original Oracle/Protected Checker；L2-r4:L931",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-41",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 27226,
    "end": 27298
  }
}
```

<a id="ch-42"></a>

# CH-42｜來源／要求／Case／Evidence／Delivery LEDGER：一筆一真值

**唯一主波** `W0`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L27299–27359`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Evidence Ledger/Reader；L2-r4:L932。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W0 Normative 主責）

W0 的原文/Source/SPEC/QuestionLedger/Program 只有 SourceSpan+same Subject/Scope 作 W1 受影依據，W1 不重寫或簽 W0 原草案與定案。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W0 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L27299–27359` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-42 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-42",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W0",
  "OriginalReader": "Original Evidence Ledger/Reader；L2-r4:L932",
  "consumer": "Original Evidence Ledger/Reader；L2-r4:L932",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-42",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 27299,
    "end": 27359
  }
}
```

<a id="ch-43"></a>

# CH-43｜ClaimCeiling、測量層、Producer/Checker/Publisher 的不同責任

**唯一主波** `W4`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L27360–27436`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original ClaimCeiling Owner；L2-r4:L933。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W4 Normative 主責）

W1 只交 Source/OriginalID/Case/ExpectedRaw/受影 HOLD，TraceClosure／獨立 Checker／Publisher cutover 不可在 W1 宣稱。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W4 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L27360–27436` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-43 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-43",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W4",
  "OriginalReader": "Original ClaimCeiling Owner；L2-r4:L933",
  "consumer": "Original ClaimCeiling Owner；L2-r4:L933",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-43",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 27360,
    "end": 27436
  }
}
```

<a id="ch-44"></a>

# CH-44｜CI、供應鏈、部署、Cutover、Rollback 的原服務區分

**唯一主波** `W4`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L27437–27509`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Publisher/SupplyChain Owner；L2-r4:L934。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W4 Normative 主責）

W1 只交 Source/OriginalID/Case/ExpectedRaw/受影 HOLD，TraceClosure／獨立 Checker／Publisher cutover 不可在 W1 宣稱。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W4 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L27437–27509` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-44 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-44",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W4",
  "OriginalReader": "Original Publisher/SupplyChain Owner；L2-r4:L934",
  "consumer": "Original Publisher/SupplyChain Owner；L2-r4:L934",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-44",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 27437,
    "end": 27509
  }
}
```

<a id="ch-45"></a>

# CH-45｜L0–L3 文件包、DELIVER、原 Consumer ACK 與長期可維護性

**唯一主波** `W4`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L27510–27588`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** FHS L3 Curator + Original Domain Owner；L2-r4:L935。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W4 Normative 主責）

W1 只交 Source/OriginalID/Case/ExpectedRaw/受影 HOLD，TraceClosure／獨立 Checker／Publisher cutover 不可在 W1 宣稱。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W4 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L27510–27588` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-45 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-45",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W4",
  "OriginalReader": "FHS L3 Curator + Original Domain Owner；L2-r4:L935",
  "consumer": "FHS L3 Curator + Original Domain Owner；L2-r4:L935",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-45",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 27510,
    "end": 27588
  }
}
```

<a id="ch-46"></a>

# CH-46｜成本／FinOps／KnownAnswer 復用及三種 Dogfood Loop

**唯一主波** `W3`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L27589–27648`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Product FinOps/Dogfood Owner；L2-r4:L936。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W3 Normative 主責）

W1 保持此章完整源身份、Need/Host/Consumer 的交接 locator；全產品分母/普通模式及其原 Reader 由 W3 主波驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W3 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L27589–27648` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-46 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-46",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W3",
  "OriginalReader": "Product FinOps/Dogfood Owner；L2-r4:L936",
  "consumer": "Product FinOps/Dogfood Owner；L2-r4:L936",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-46",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 27589,
    "end": 27648
  }
}
```

<a id="ch-47"></a>

# CH-47｜OpenSpec、gstack、Hermes 外部研究與 Build-or-Use 准入

**唯一主波** `W3`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L27649–27749`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Tech/License/Host Reader；L2-r4:L937。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W3 Normative 主責）

W1 保持此章完整源身份、Need/Host/Consumer 的交接 locator；全產品分母/普通模式及其原 Reader 由 W3 主波驗。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W3 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L27649–27749` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-47 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-47",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W3",
  "OriginalReader": "Original Tech/License/Host Reader；L2-r4:L937",
  "consumer": "Original Tech/License/Host Reader；L2-r4:L937",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-47",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 27649,
    "end": 27749
  }
}
```

<a id="ch-48"></a>

# CH-48｜受界 ChangeSet、風險／具名 HOLD、Stop-Resume 與決策閉環

**唯一主波** `W0`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L27750–27878`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Affected Original Owner/FirstFail Reader；L2-r4:L938。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W0 Normative 主責）

W0 的原文/Source/SPEC/QuestionLedger/Program 只有 SourceSpan+same Subject/Scope 作 W1 受影依據，W1 不重寫或簽 W0 原草案與定案。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W0 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L27750–27878` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。



## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-48 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-48",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W0",
  "OriginalReader": "Affected Original Owner/FirstFail Reader；L2-r4:L938",
  "consumer": "Affected Original Owner/FirstFail Reader；L2-r4:L938",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-48",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 27750,
    "end": 27878
  }
}
```

<a id="ch-49"></a>

# CH-49｜逐章正式驗收標準、H1 防壓平測試與裁決

**唯一主波** `W4`｜**本波法位** `CROSS_WAVE_READ_ONLY_HANDOFF`｜**當期上位章位** `L1-r4:L27879–28004`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Checker/Publisher (as affected)；L2-r4:L939。原 Domain Reader/Writer 不因本章轉移。

## Cross-wave handoff（唯一 W4 Normative 主責）

W1 只交 Source/OriginalID/Case/ExpectedRaw/受影 HOLD，TraceClosure／獨立 Checker／Publisher cutover 不可在 W1 宣稱。

**W1 受影輸入**：`subject_id, affected_scope, source_sha256, original_requirement_locator, consumer_reader, need_or_case_if_applicable, proposed_POS/NEG, first_fail_or_hold, original_ACK_EXPECTED_NOT_OBSERVED`。**不得**將原 W4 正文摘要成 W1 平行有效法位；正例=具有 `L1-r4:L27879–28004` 真定位、Source/NEG 和主波標記；負例=`W1_SHADOW_WAVE_WRITER_NACK`（W1 複製本章正式內容或假造原 Reader 收據）；失敗只 PARK 受影 W1 handoff。

## AUTHOR-FINAL｜具名原波交接

本章原實質條文與先前專屬跨波責任仍保留。以下是 CH-49 的 typed author projection，只有原 Receiver 能核定它的實效；W1 不獲本章 WriteSet。

```json
{
  "schema_name": "AUTHOR.FHS.ChapterHandoff@design_r1",
  "chapter": "CH-49",
  "source_l1_sha": "cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b",
  "OriginalWave": "W4",
  "OriginalReader": "Original Checker/Publisher (as affected)；L2-r4:L939",
  "consumer": "Original Checker/Publisher (as affected)；L2-r4:L939",
  "scope": "FHS/PIPD-LS-PKG/W1/author-design/CH-49",
  "implementation_status": "AUTHOR_READONLY_PROJECTION; ORIGINAL_IMPLEMENTATION_NOT_RUN",
  "NoWriteSetTransfer": true,
  "original_reader_ack": "EXPECTED_NOT_OBSERVED",
  "NEG": "W1 claims OriginalWave writer or reuses foreign ACK",
  "FirstFail": "W1_SHADOW_WAVE_WRITER_NACK",
  "resume": "Same chapter source span and original owner same-scope raw readback",
  "l1_span": {
    "start": 27879,
    "end": 28004
  }
}
```


## FINAL-INT24｜原完整來源行與方法角色

| `INT-24` | `FHS_設計與升級原意_完整規劃_2026-11-04_r2_HIGH_RETENTION_FULL_SUBSTANTIVE_AUDIT_REPAIR.md:L173`／Native-first:L306–361；上游 v1.16.0/v1.92.55.0 | OpenSpec/gstack 是方法而非再一套法定流程 | OpenSpec proposal/validate；gstack review/QA 轉原 Consumer | [CH-47](#ch-47) | Original Tech/License/Host/Method Owner → Capability Consumer | POS：OpenSpec proposal/validate；gstack review/QA 轉原 Consumer | NEG：OpenSpec/gstack 自發 Canonical PI/Independent Verdict/Publisher Release | MANDATORY_SPEC；Native 依受影 Effect | OWNER_SEMANTIC_ACK_PENDING |

此行為 L1 原 bytes 引文；其中 v1.92.55.0 僅歷史研究值，當期單值 pin 以 asset_decision_registry.jsonl 為準。原方法 Consumer 未 ACK，保留具名 HOLD。

## FINAL-REMOTE｜本次三庫與 W0 候選差額讀回

〔R1-2026-11-06 更正〕FINAL-REMOTE 的三個 main 與 PR HEAD 皆為 2026-11-05 讀值。2026-11-06 實測：Fabric main `ef4fe187e706bb309a905c2f88c7477b53cf5839`、SBL main `8f5161a306d46775b71ff2bc7817e447cfd8f96e`、HGK main `a7046a36956e2179d7125449ce9b6f05fa5451cf`；SBL PR41 HEAD 已由 `c01410bb8eeae25b12d7ce5df9986ce30981b912` 變為 `d10362d7`（203 changed files、mergeable_state=dirty，仍 open／unmerged）；Fabric PR27 HEAD `8fb0b6e0`、HGK PR11 HEAD `8da3cb3c` 仍 open，原文該兩值仍成立。以上仍只是 remote source readback，非本機 RepoContext、Host Loaded 或 Reader acceptance。、HGK main `0143b50331f7fef007a5921bb743e61f59b0a7bd` 已唯讀重新取得原 bytes/blob SHA；紀錄於 evidence/current_remote/readback.json。SBL PR41 本次 HEAD `c01410bb8eeae25b12d7ce5df9986ce30981b912` 仍 open/unmerged；Fabric PR27 HEAD `8fb0b6e03e3ed30fdbe63bfde1a652e970970f4a`；HGK PR11 HEAD `8da3cb3c942f38799dd481c9e784fc4c69cecb5c`。這些是 remote source readback，非本地 RepoContext、Host Loaded 或 Reader acceptance。

較新 closure_formal 的 70 個 OPEN 已逐 ID 讀回：68 carried；新 ID 為 `W1_RECEIVER_ACK_HOLD`, `WP19_DEP_DEVTOOL_HOLD`；無封存 ID 被關閉。WP19 作者分析為 6 PASS/1 FAIL，殘留 `UNDECLARED_DEPENDENCY@hg_kseos`，原 CI Reader ACK 仍 NOT_OBSERVED，E26 未滿足。舊表 68/5:2 僅描述 ARCHIVED_R4C，不與候選互蓋。**r2 追加（N-01）**：當期作者封存再進一層為 `W0_FINAL_1203`＝**71 OPEN**（70 carried + 1 new，`all_open=true`）、WP19 作者端 7 PASS／0 FAIL、`wp19_done=false`、`w0_full_closeout=false`、E26 `UNSATISFIED_WP19_ORIGINAL_RAW_MISSING`；四層以 `W0_STATUS_THREE_WAY.json` 與 FINAL-01 §1 為準。


## FINAL-WP｜八 WP 當期案例與異質 SEC

下列當期作者案例取代歷史 r2 安全 FirstFail 的顯示值；業務原 NEG 與原世界效果仍保持。所有 native case=NOT_RUN；作者驗證只測契約拒錯。

### WP-FHS-02

- `CASE-W1-02-POS` / POS：Input={"business_case_original_text": "- **`CASE-W1-02-POS`**：`POS`；Trigger/Input＝對同 Subject/SourceSHA、受影 operation 執行原 Reader 候選驗證：Original Fabric Policy Owner/current epoch; applicable Policy manifest SHA; HGK original policy consumer process identity。預期 `ActiveEpoch+LoadedDigest+ConsumerACK（由 Fabric+HGK 原 Reader 同 Subject 讀回）` 的 typed 原 Consumer 回條或具名 `HOLD`，不以檔案存在冒驗收。；`design_fixture_sha256=fe73c68a6026bca8669822b5a9e8cf018c3644ace9dc74572a816e0c9d44b215`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=READER_ACK_OR_POLICY_EPOCH_LOADED_MISMATCH`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-02 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "POS"}；Principal=authorized original operation producer；AttackSurface=WP02_business_pos；FirstFail=`READER_ACK_OR_POLICY_EPOCH_LOADED_MISMATCH`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-02-NEG` / NEG：Input={"business_case_original_text": "- **`CASE-W1-02-NEG`**：`NEG`；Trigger/Input＝從合法候選刪掉/錯配本 WP 必需前置：把未批准 Stage SHA 當 ActiveEpoch、HGK LoadedDigest 與 active 不符。原 Reader 應 NACK，合法 READ/DRAFT 仍可續。；`design_fixture_sha256=4d67772ca1e0f1ce7343ae6b5d4ba405d622a23a3e532928cf0b1074f32a3fa5`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=POLICY_EPOCH_LOADED_MISMATCH`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-02 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "NEG"}；Principal=authorized original operation producer；AttackSurface=WP02_business_neg；FirstFail=`POLICY_EPOCH_LOADED_MISMATCH`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-02-EDGE` / EDGE：Input={"business_case_original_text": "- **`CASE-W1-02-EDGE`**：`EDGE`；Trigger/Input＝獨立邊界或半成品擾動：Owner 在 Stage 後切 epoch，舊 HGK process 尚載前 epoch；僅停受影 OPS，READ 繼續。要求保留原 Raw/last_good，依本 WP 退出 `原 Fabric/HGK Owner 以原 epoch migration/inverse 回 last-good，Stage 不可當 Active` 後有界續工；UNKNOWN 禁重放。；`design_fixture_sha256=cc32673987c77f80b40a320c30cc63cff861148071dd671c3f0453efbcd2356d`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=POLICY_EPOCH_LOADED_MISMATCH`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-02 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "EDGE"}；Principal=authorized original operation producer；AttackSurface=WP02_business_edge；FirstFail=`POLICY_EPOCH_LOADED_MISMATCH`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-02-SEC` / SEC：Input={"actor": "Fabric policy signer", "attack_surface": "policy_signature_and_epoch", "credential": "SYNTHETIC_DESCRIPTOR_ONLY_NO_TOKEN", "operation_scope": "same-subject-design-fixture"}；Principal=Fabric policy signer；AttackSurface=policy_signature_and_epoch；FirstFail=`FABRIC_POLICY_SIGNER_OR_EPOCH_DENY`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
### WP-FHS-03

- `CASE-W1-03-POS` / POS：Input={"business_case_original_text": "- **`CASE-W1-03-POS`**：`POS`；Trigger/Input＝對同 Subject/SourceSHA、受影 operation 執行原 Reader 候選驗證：原 HGK Registry、OS PID/SID、scope/nonce/TTL/ProcessACL/PolicyEpoch，非 Maker credentials。預期 `IssuerReceiverBinding+original typed refusal/ACK; no self-issued Permit` 的 typed 原 Consumer 回條或具名 `HOLD`，不以檔案存在冒驗收。；`design_fixture_sha256=7a7bba7006b6053729b16932235b2e58762cc830f86165357be6fe6a82cecaae`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=READER_ACK_OR_HGK_ISSUER_ACL_NONCE_TTL_NACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-03 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "POS"}；Principal=authorized original operation producer；AttackSurface=WP03_business_pos；FirstFail=`READER_ACK_OR_HGK_ISSUER_ACL_NONCE_TTL_NACK`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-03-NEG` / NEG：Input={"business_case_original_text": "- **`CASE-W1-03-NEG`**：`NEG`；Trigger/Input＝從合法候選刪掉/錯配本 WP 必需前置：用不同 PID/SID、過期 nonce、重用 TTL 或 scope widening 要求原 Issuer 放行。原 Reader 應 NACK，合法 READ/DRAFT 仍可續。；`design_fixture_sha256=67b80fb489ac7480a299b47cfd389cf1c772aa4e50be37db8914f680e4679bc9`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=HGK_ISSUER_ACL_NONCE_TTL_NACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-03 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "NEG"}；Principal=authorized original operation producer；AttackSurface=WP03_business_neg；FirstFail=`HGK_ISSUER_ACL_NONCE_TTL_NACK`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-03-EDGE` / EDGE：Input={"business_case_original_text": "- **`CASE-W1-03-EDGE`**：`EDGE`；Trigger/Input＝獨立邊界或半成品擾動：在授權後 Worker PID 重啟；原 Receiver 必以新 process ACL / nonce 再認，不借舊票。要求保留原 Raw/last_good，依本 WP 退出 `原 HGK Owner revoke affected grant/expire nonce, readback remaining WorkIDs，不清全域 Registry` 後有界續工；UNKNOWN 禁重放。；`design_fixture_sha256=aa23ebf87da2dfd98705bbd780a502c28c0edbf445c81d0fb5941ffc47f11c07`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=HGK_ISSUER_ACL_NONCE_TTL_NACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-03 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "EDGE"}；Principal=authorized original operation producer；AttackSurface=WP03_business_edge；FirstFail=`HGK_ISSUER_ACL_NONCE_TTL_NACK`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-03-SEC` / SEC：Input={"actor": "ordinary Hermes runtime SID", "attack_surface": "issuer_process_acl", "credential": "SYNTHETIC_DESCRIPTOR_ONLY_NO_TOKEN", "operation_scope": "same-subject-design-fixture"}；Principal=ordinary Hermes runtime SID；AttackSurface=issuer_process_acl；FirstFail=`HGK_ISSUER_PRINCIPAL_DENY`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
### WP-FHS-04

- `CASE-W1-04-POS` / POS：Input={"business_case_original_text": "- **`CASE-W1-04-POS`**：`POS`；Trigger/Input＝對同 Subject/SourceSHA、受影 operation 執行原 Reader 候選驗證：Hermes v0.22.5 pin；ProfileSHA、WorkID、lease generation、run budget 原 Reader。預期 `Fresh PID+LoadedProfileSHA+Raw三Lane Required/Selected/Invoked/ActualServed + JournalCursor` 的 typed 原 Consumer 回條或具名 `HOLD`，不以檔案存在冒驗收。；`design_fixture_sha256=1bf25993e2c828547f8200b78630769ec047cea6ec8b948adeb8a496114d579c`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=READER_ACK_OR_HERMES_LEASE_UNKNOWN_RECONCILE`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-04 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "POS"}；Principal=authorized original operation producer；AttackSurface=WP04_business_pos；FirstFail=`READER_ACK_OR_HERMES_LEASE_UNKNOWN_RECONCILE`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-04-NEG` / NEG：Input={"business_case_original_text": "- **`CASE-W1-04-NEG`**：`NEG`；Trigger/Input＝從合法候選刪掉/錯配本 WP 必需前置：以過期 lease_generation 重播非冪等 WorkID 並把 Picker Selected 假稱 ActualServed。原 Reader 應 NACK，合法 READ/DRAFT 仍可續。；`design_fixture_sha256=ed88507327a2c86d323e556ab6c5cb506239d544492ac572e6367201964afb0b`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=HERMES_LEASE_UNKNOWN_RECONCILE`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-04 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "NEG"}；Principal=authorized original operation producer；AttackSurface=WP04_business_neg；FirstFail=`HERMES_LEASE_UNKNOWN_RECONCILE`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-04-EDGE` / EDGE：Input={"business_case_original_text": "- **`CASE-W1-04-EDGE`**：`EDGE`；Trigger/Input＝獨立邊界或半成品擾動：worker crash 在 effect 之後/Raw 入帳之前：維持 UNKNOWN，必 original World Reconcile。要求保留原 Raw/last_good，依本 WP 退出 `原 Journal 查 WorldRaw/last-good 再 Resume WorkID；UNKNOWN 禁盲重試` 後有界續工；UNKNOWN 禁重放。；`design_fixture_sha256=c901e37c671f728579b34803210954cc3149a4559c7d48312ef5891b0cbe7601`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=HERMES_LEASE_UNKNOWN_RECONCILE`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-04 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "EDGE"}；Principal=authorized original operation producer；AttackSurface=WP04_business_edge；FirstFail=`HERMES_LEASE_UNKNOWN_RECONCILE`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-04-SEC` / SEC：Input={"actor": "foreign Profile principal", "attack_surface": "profile_secret_boundary", "credential": "SYNTHETIC_DESCRIPTOR_ONLY_NO_TOKEN", "operation_scope": "same-subject-design-fixture"}；Principal=foreign Profile principal；AttackSurface=profile_secret_boundary；FirstFail=`HERMES_CROSS_PROFILE_SECRET_DENY`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
### WP-FHS-05

- `CASE-W1-05-POS` / POS：Input={"business_case_original_text": "- **`CASE-W1-05-POS`**：`POS`；Trigger/Input＝對同 Subject/SourceSHA、受影 operation 執行原 Reader 候選驗證：三份不同 SPECDraft、原 SourceManifest/Authority/Profile safety veto、原 PIPD Writer version。預期 `非空 strict PI，真 RepoContext 才有 PD，DEV/OPS EffectIntent 分開，PlannedTQAEP 不冒 Checker` 的 typed 原 Consumer 回條或具名 `HOLD`，不以檔案存在冒驗收。；`design_fixture_sha256=db25380618cf4dbe09ecaf0e2f2fa63afcb30c7e2d32a5676915eb8526521c50`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=READER_ACK_OR_PIPD_STRICT_SCHEMA_OR_SOURCE_NACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-05 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "POS"}；Principal=authorized original operation producer；AttackSurface=WP05_business_pos；FirstFail=`READER_ACK_OR_PIPD_STRICT_SCHEMA_OR_SOURCE_NACK`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-05-NEG` / NEG：Input={"business_case_original_text": "- **`CASE-W1-05-NEG`**：`NEG`；Trigger/Input＝從合法候選刪掉/錯配本 WP 必需前置：把 _profile_meta 側掛塞進 strict PI；或憑 Caller HEAD 虛構本機 Repo binding。原 Reader 應 NACK，合法 READ/DRAFT 仍可續。；`design_fixture_sha256=a2627116e950378a13972ef14da8fb29be58758b09ebb2690f874e7ddee8a960`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=PIPD_STRICT_SCHEMA_OR_SOURCE_NACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-05 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "NEG"}；Principal=authorized original operation producer；AttackSurface=WP05_business_neg；FirstFail=`PIPD_STRICT_SCHEMA_OR_SOURCE_NACK`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-05-EDGE` / EDGE：Input={"business_case_original_text": "- **`CASE-W1-05-EDGE`**：`EDGE`；Trigger/Input＝獨立邊界或半成品擾動：PI SourceSHA 不變而 RepoHEAD 改變，只使 PD/ECP stale；不可偷重寫 PI requirement 原義。要求保留原 Raw/last_good，依本 WP 退出 `隔離候選刪除/回復 preimage；SourceSHA/HEAD 變更僅重編受影 PD/ECP` 後有界續工；UNKNOWN 禁重放。；`design_fixture_sha256=dd98865cc46aae6a7a357a0f767c9991a05e820468ed718aa0ddf3b05ba709ae`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=PIPD_STRICT_SCHEMA_OR_SOURCE_NACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-05 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "EDGE"}；Principal=authorized original operation producer；AttackSurface=WP05_business_edge；FirstFail=`PIPD_STRICT_SCHEMA_OR_SOURCE_NACK`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-05-SEC` / SEC：Input={"actor": "untrusted source author", "attack_surface": "source_to_original_writer_boundary", "credential": "SYNTHETIC_DESCRIPTOR_ONLY_NO_TOKEN", "operation_scope": "same-subject-design-fixture"}；Principal=untrusted source author；AttackSurface=source_to_original_writer_boundary；FirstFail=`PIPD_UNTRUSTED_SOURCE_WRITER_BYPASS_DENY`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
### WP-FHS-07

- `CASE-W1-07-POS` / POS：Input={"business_case_original_text": "- **`CASE-W1-07-POS`**：`POS`；Trigger/Input＝對同 Subject/SourceSHA、受影 operation 執行原 Reader 候選驗證：W0 WP15 三 SPEC/QuestionLedger、PLAN base_revision、original Native PLAN CAS Reader。預期 `PlanRevisionProposal + original CAS(base_revision, proposal_hash) ACK/NACK` 的 typed 原 Consumer 回條或具名 `HOLD`，不以檔案存在冒驗收。；`design_fixture_sha256=7bdf630773ebf5607a500e8eab19b10710a48168493535d1011c7f8ab4b2617d`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=READER_ACK_OR_PLAN_CAS_STALE_BASE`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-07 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "POS"}；Principal=authorized original operation producer；AttackSurface=WP07_business_pos；FirstFail=`READER_ACK_OR_PLAN_CAS_STALE_BASE`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-07-NEG` / NEG：Input={"business_case_original_text": "- **`CASE-W1-07-NEG`**：`NEG`；Trigger/Input＝從合法候選刪掉/錯配本 WP 必需前置：跳過原 PLAN Writer 直接送 ECP→Issuer 或停用 legacy commander 提升成新 Gate。原 Reader 應 NACK，合法 READ/DRAFT 仍可續。；`design_fixture_sha256=0a21567fcd179714613a78425cff705f6eac773f0d8ecaf7a48fb3fed3c2053f`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=PLAN_CAS_STALE_BASE`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-07 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "NEG"}；Principal=authorized original operation producer；AttackSurface=WP07_business_neg；FirstFail=`PLAN_CAS_STALE_BASE`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-07-EDGE` / EDGE：Input={"business_case_original_text": "- **`CASE-W1-07-EDGE`**：`EDGE`；Trigger/Input＝獨立邊界或半成品擾動：兩個 proposal 同 base_revision 競逐，僅一個 Writer CAS 成功；另一個明確 NACK。要求保留原 Raw/last_good，依本 WP 退出 `CAS mismatch 丟棄提案並重讀 base；不寫 Target Repo/second Queue` 後有界續工；UNKNOWN 禁重放。；`design_fixture_sha256=a3ebd3eb2ec9fa831cd506c454173a54471cc088618c769e90cdc1c24c5c3aa3`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=PLAN_CAS_STALE_BASE`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-07 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "EDGE"}；Principal=authorized original operation producer；AttackSurface=WP07_business_edge；FirstFail=`PLAN_CAS_STALE_BASE`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-07-SEC` / SEC：Input={"actor": "foreign WorkID signer", "attack_surface": "plan_cas_signer_audience", "credential": "SYNTHETIC_DESCRIPTOR_ONLY_NO_TOKEN", "operation_scope": "same-subject-design-fixture"}；Principal=foreign WorkID signer；AttackSurface=plan_cas_signer_audience；FirstFail=`PLAN_FOREIGN_WORKID_SIGNER_DENY`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
### WP-FHS-11

- `CASE-W1-11-POS` / POS：Input={"business_case_original_text": "- **`CASE-W1-11-POS`**：`POS`；Trigger/Input＝對同 Subject/SourceSHA、受影 operation 執行原 Reader 候選驗證：TPM-SP、Commander Guide-SP、Acceptance Challenge-SP 各自 artifact digest；Host compatibility+8 PIPD skills 各自 registry。預期 `每 SP×Host 真 Loaded/Invoked/Used/nontrigger/Remove Raw；不共用收據` 的 typed 原 Consumer 回條或具名 `HOLD`，不以檔案存在冒驗收。；`design_fixture_sha256=c0955e3662b61f0781efc2860e057c77a8c4e426b50e433e2f76cc9b5d2e6f3e`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=READER_ACK_OR_HOST_SKILL_TRIGGER_NONTRIGGER_NACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-11 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "POS"}；Principal=authorized original operation producer；AttackSurface=WP11_business_pos；FirstFail=`READER_ACK_OR_HOST_SKILL_TRIGGER_NONTRIGGER_NACK`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-11-NEG` / NEG：Input={"business_case_original_text": "- **`CASE-W1-11-NEG`**：`NEG`；Trigger/Input＝從合法候選刪掉/錯配本 WP 必需前置：用 TPM-SP 的 Loaded SHA 冒 Challenge-SP；Maker 以模型結論簽 Protected Checker。原 Reader 應 NACK，合法 READ/DRAFT 仍可續。；`design_fixture_sha256=786f33e914af4c2a211c40142f6a979721e3f045e7a1fb66b61a8aff48675097`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=HOST_SKILL_TRIGGER_NONTRIGGER_NACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-11 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "NEG"}；Principal=authorized original operation producer；AttackSurface=WP11_business_neg；FirstFail=`HOST_SKILL_TRIGGER_NONTRIGGER_NACK`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-11-EDGE` / EDGE：Input={"business_case_original_text": "- **`CASE-W1-11-EDGE`**：`EDGE`；Trigger/Input＝獨立邊界或半成品擾動：Installed 後 loader 未 Loaded，或 Loaded 但 nontrigger 仍被啟動：不得宣稱 Used。要求保留原 Raw/last_good，依本 WP 退出 `原 Host disable/remove entrypoint、還原 last-good manifest；清理 residue` 後有界續工；UNKNOWN 禁重放。；`design_fixture_sha256=45b759a576b2b07290535e6eba72b8727fda367235b55757c7427ffbcedccf3f`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=HOST_SKILL_TRIGGER_NONTRIGGER_NACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-11 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "EDGE"}；Principal=authorized original operation producer；AttackSurface=WP11_business_edge；FirstFail=`HOST_SKILL_TRIGGER_NONTRIGGER_NACK`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-11-SEC` / SEC：Input={"actor": "unqualified external Host", "attack_surface": "protected_checker_role", "credential": "SYNTHETIC_DESCRIPTOR_ONLY_NO_TOKEN", "operation_scope": "same-subject-design-fixture"}；Principal=unqualified external Host；AttackSurface=protected_checker_role；FirstFail=`HOST_CHECKER_ROLE_SPOOF_DENY`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
### WP-FHS-17

- `CASE-W1-17-POS` / POS：Input={"business_case_original_text": "- **`CASE-W1-17-POS`**：`POS`；Trigger/Input＝對同 Subject/SourceSHA、受影 operation 執行原 Reader 候選驗證：NeedKey+scope、原 Policy Loaded ACK+HGK Issuer admitted installer+license/asset digest。預期 `Needed Capability 之 Installed/Loaded/Invoked/ConsumerACK+last-good，NONE=CAPABILITY_GAP_HOLD` 的 typed 原 Consumer 回條或具名 `HOLD`，不以檔案存在冒驗收。；`design_fixture_sha256=973419854ebc928437959747c73bb78f4701f4909284929cc65fec5b1da0b695`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=READER_ACK_OR_CAP_INSTALLER_ORIGIN_PARTIAL_ROLLBACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-17 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "POS"}；Principal=authorized original operation producer；AttackSurface=WP17_business_pos；FirstFail=`READER_ACK_OR_CAP_INSTALLER_ORIGIN_PARTIAL_ROLLBACK`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-17-NEG` / NEG：Input={"business_case_original_text": "- **`CASE-W1-17-NEG`**：`NEG`；Trigger/Input＝從合法候選刪掉/錯配本 WP 必需前置：未有原 Issuer/Asset provenance 卻執行 Host installer；或第二套 Queue/Issuer 被包進工具。原 Reader 應 NACK，合法 READ/DRAFT 仍可續。；`design_fixture_sha256=80be3ebb6f04a23ecba2d7d3638e7c9d92ec98cce489e3d9e8d050a7df1b44b0`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=CAP_INSTALLER_ORIGIN_PARTIAL_ROLLBACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-17 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "NEG"}；Principal=authorized original operation producer；AttackSurface=WP17_business_neg；FirstFail=`CAP_INSTALLER_ORIGIN_PARTIAL_ROLLBACK`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-17-EDGE` / EDGE：Input={"business_case_original_text": "- **`CASE-W1-17-EDGE`**：`EDGE`；Trigger/Input＝獨立邊界或半成品擾動：Installer 解壓成功但載入失敗，需回上版 qualified last-good，不可把 Installed 當 Active。要求保留原 Raw/last_good，依本 WP 退出 `原 installer inverse/restore manifest+LoadedSHA+residue；不得 Git revert 取代 Host inverse` 後有界續工；UNKNOWN 禁重放。；`design_fixture_sha256=473e05189bac3f56fa01c83097459d0e1ca23c245f154ee2f723fe3657b0346f`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=CAP_INSTALLER_ORIGIN_PARTIAL_ROLLBACK`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-17 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "EDGE"}；Principal=authorized original operation producer；AttackSurface=WP17_business_edge；FirstFail=`CAP_INSTALLER_ORIGIN_PARTIAL_ROLLBACK`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-17-SEC` / SEC：Input={"actor": "unadmitted installer principal", "attack_surface": "installer_admin_credential", "credential": "SYNTHETIC_DESCRIPTOR_ONLY_NO_TOKEN", "operation_scope": "same-subject-design-fixture"}；Principal=unadmitted installer principal；AttackSurface=installer_admin_credential；FirstFail=`CAPABILITY_INSTALLER_PRIVILEGE_DENY`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
### WP-FHS-20

- `CASE-W1-20-POS` / POS：Input={"business_case_original_text": "- **`CASE-W1-20-POS`**：`POS`；Trigger/Input＝對同 Subject/SourceSHA、受影 operation 執行原 Reader 候選驗證：CellID+original Kind/Mode/Host/RawToken，Host Capability/Provider state 原 Owner 必須核對。預期 `Selected/NotAffected/OwnerHold per Cell + raw Host-specific Consumer outcome` 的 typed 原 Consumer 回條或具名 `HOLD`，不以檔案存在冒驗收。；`design_fixture_sha256=bbfc2e1676c9b9cd6055b5f754ce76be137a082cb0319ce917b4bce171ccbd1d`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=READER_ACK_OR_CELL_TOKEN_OWNER_MAP_UNBOUND`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-20 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "POS"}；Principal=authorized original operation producer；AttackSurface=WP20_business_pos；FirstFail=`READER_ACK_OR_CELL_TOKEN_OWNER_MAP_UNBOUND`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-20-NEG` / NEG：Input={"business_case_original_text": "- **`CASE-W1-20-NEG`**：`NEG`；Trigger/Input＝從合法候選刪掉/錯配本 WP 必需前置：把 ON/OFF source token 私譯成 provider_off bool 或借不同 Host/Provider Raw。原 Reader 應 NACK，合法 READ/DRAFT 仍可續。；`design_fixture_sha256=d24697d250ba54e3a5c461d6eaac03e2a50999d101d6e1d02eede926803e917a`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=CELL_TOKEN_OWNER_MAP_UNBOUND`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-20 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "NEG"}；Principal=authorized original operation producer；AttackSurface=WP20_business_neg；FirstFail=`CELL_TOKEN_OWNER_MAP_UNBOUND`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-20-EDGE` / EDGE：Input={"business_case_original_text": "- **`CASE-W1-20-EDGE`**：`EDGE`；Trigger/Input＝獨立邊界或半成品擾動：Same Kind/Mode 從 Hermes 改到 Codex，原 Cell ID 改變；舊 Cell receipt 不可重用。要求保留原 Raw/last_good，依本 WP 退出 `撤受影 Host adapter/probe，恢復同 Need qualified last-good，保留 raw ON/OFF` 後有界續工；UNKNOWN 禁重放。；`design_fixture_sha256=e1c4ac1e7397df8542280485d763b1fc2178626dcdacdab4a33012eaaae5d58b`；Expected Raw=`ORIGINAL_CONSUMER_ACK_OR_TYPED_NACK_NOT_OBSERVED`；`FirstFail=CELL_TOKEN_OWNER_MAP_UNBOUND`；`status=PLANNED_NOT_EXECUTED`；Requalification=`WP-20 same Subject/Candidate/Scope/Host/PolicyEpoch affected only`。", "kind": "EDGE"}；Principal=authorized original operation producer；AttackSurface=WP20_business_edge；FirstFail=`CELL_TOKEN_OWNER_MAP_UNBOUND`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。
- `CASE-W1-20-SEC` / SEC：Input={"actor": "foreign Host consumer", "attack_surface": "cell_consumer_credential_audience", "credential": "SYNTHETIC_DESCRIPTOR_ONLY_NO_TOKEN", "operation_scope": "same-subject-design-fixture"}；Principal=foreign Host consumer；AttackSurface=cell_consumer_credential_audience；FirstFail=`CELL_FOREIGN_CONSUMER_CREDENTIAL_DENY`；ExpectedRaw=Original consumer raw; NOT_OBSERVED；Stop=PARK only this affected original effect on missing reader or failed precondition；Resume=Re-read same Subject/SourceSHA/Candidate/Scope/Host/PolicyEpoch; UNKNOWN requires World reconcile。

## FINAL-FUO｜P01–P07 的當期量測分層

- **P01 選型難**：W1_DESIGN_FUO=NeedKey→24 Slot 唯一 Build-or-Use / NoFit / License 原 Reader 請求；LATER_NATIVE_FUO=W2/W3 真 Capability Loaded＋Actual Consumer Used；失配 `NOFIT` 確實撤回；Consumer=Original Tech/Host Capability Consumer；Measurement=W2/W3 真 Capability Loaded＋Actual Consumer Used；失配 `NOFIT` 確實撤回；NEG=Author documents or another pain/Host receipt presented as this native outcome；FirstFail=`FUO_CLAIM_CEILING_NACK`；原生測量 NOT_RUN。
- **P02 交接斷裂**：W1_DESIGN_FUO=三 SPEC／S1-S5 與 W1→W2 typed NACK；LATER_NATIVE_FUO=原 SBL PI/PD/ECP/TQAEP 同 Source/SHA ACK → HGK World Raw、跨 Seam re-read；Consumer=Original SBL PIPD/HGK Seam Reader；Measurement=原 SBL PI/PD/ECP/TQAEP 同 Source/SHA ACK → HGK World Raw、跨 Seam re-read；NEG=Author documents or another pain/Host receipt presented as this native outcome；FirstFail=`FUO_CLAIM_CEILING_NACK`；原生測量 NOT_RUN。
- **P03 重問問題**：W1_DESIGN_FUO=KnownAnswer / QuestionLedger keyed Subject+SourceSHA+Scope；LATER_NATIVE_FUO=普通 Goal 同源免重問；Source/Scope drift 僅重問變動項；Consumer=Original QuestionLedger Reader；Measurement=普通 Goal 同源免重問；Source/Scope drift 僅重問變動項；NEG=Author documents or another pain/Host receipt presented as this native outcome；FirstFail=`FUO_CLAIM_CEILING_NACK`；原生測量 NOT_RUN。
- **P04 Writer 碰撞**：W1_DESIGN_FUO=唯一 PIPD Writer/HGK Issuer/PLAN CAS 合約；LATER_NATIVE_FUO=原 Native 單控制面無 shadow producer；foreign WorkID/Issuer 應 NACK；Consumer=Original HGK Issuer/PLAN CAS Reader；Measurement=原 Native 單控制面無 shadow producer；foreign WorkID/Issuer 應 NACK；NEG=Author documents or another pain/Host receipt presented as this native outcome；FirstFail=`FUO_CLAIM_CEILING_NACK`；原生測量 NOT_RUN。
- **P05 假 PASS**：W1_DESIGN_FUO=Maker/Checker 及 POS/NEG/EDGE/SEC/FirstFail 設計；LATER_NATIVE_FUO=Protected Checker 真不同 Principal／同 Scope Raw；缺 Receipt 保持 HOLD；Consumer=Original Protected Checker；Measurement=Protected Checker 真不同 Principal／同 Scope Raw；缺 Receipt 保持 HOLD；NEG=Author documents or another pain/Host receipt presented as this native outcome；FirstFail=`FUO_CLAIM_CEILING_NACK`；原生測量 NOT_RUN。
- **P06 Host 假掛載**：W1_DESIGN_FUO=4 Host×3 SP、每一 `SELECTED→LOADED→INVOKED→USED` 期待原 Reader；LATER_NATIVE_FUO=W2/W3 每 Host 自身 PID/LoadedSHA/trigger/nontrigger/Consumer Result，不互借；Consumer=Each original Host Loader/Runtime Reader；Measurement=W2/W3 每 Host 自身 PID/LoadedSHA/trigger/nontrigger/Consumer Result，不互借；NEG=Author documents or another pain/Host receipt presented as this native outcome；FirstFail=`FUO_CLAIM_CEILING_NACK`；原生測量 NOT_RUN。
- **P07 最後一哩**：W1_DESIGN_FUO=W1 可直接交原 Consumer 的 source-bound functional/restore design；LATER_NATIVE_FUO=W3 W18 fresh PID 的普通 Goal→自動 Lane→真 Worker→可取用結果→crash-resume；W4 原 Publisher 独立判斷；Consumer=Hermes Original Runtime/User Consumer; W3 W18；Measurement=W3 W18 fresh PID 的普通 Goal→自動 Lane→真 Worker→可取用結果→crash-resume；W4 原 Publisher 独立判斷；NEG=Author documents or another pain/Host receipt presented as this native outcome；FirstFail=`FUO_CLAIM_CEILING_NACK`；原生測量 NOT_RUN。

## FINAL-TECH｜固定來源本次重核

Hermes v0.22.5、OpenSpec v1.16.0 的官方 release/License 已讀回；gstack `6bdafb2cf5acf05e6e9ab23a74e682e155d1fdde` 的 VERSION、package.json、MIT License、README 已取得 exact bytes，SHA 見 evidence/public_pins/readback.json。唯一設計 pin 保持不變；公開來源相容性描述不是 Windows 本機可用性，所有 slot 的 Installed/Loaded/Invoked/ConsumerUsed/Verified 仍 NOT_OBSERVED。方法層不強制安裝，Native singleton 不做任意卸載。

---

## 實作後回寫（As-Built）— W1 r4

> **ArtifactID**：`FHS_PIPD-LS-PKG_W1_r4_ASBUILT@2026-11-07`  
> **Parent／Supersedes**：`FHS_PIPD-LS-PKG_W1_r3.md` @ `936a8bcb62e16cd205ac8e5799e802293916bbb9de6e5ba8260ea3e1dd013cbf`（868,138 bytes）  
> **本版 SHA256**：見同目錄 `*_REVISION_MANIFEST.json`（本檔不記錄自身 digest，避免自我指涉）  
> **產生時間**：2026-11-07T23:10:08+0800  
> **性質**：As-Built 追加章節。母本正文逐位元保留，未改寫、未摘要、未刪除任何 OriginalID／NEG／SourceSHA／Reader；本章只補本輪**實作與驗收差額**。  
> **ClaimCeiling**：`DOCUMENT_RECONCILIATION_COMPLETE_WITH_SCOPED_HOLDS`。本章不授權任何世界效果，也不代表原域 Reader ACK。

### A.1 狀態詞彙（本章只用這七個，避免「完成」一詞混用）

| 詞 | 含義 |
|---|---|
| `IMPLEMENTED` | 程式已在受權分支或已合併 main 落地，但未取得原域 ACK |
| `TESTED` | 有可重算的 Raw（含指令、exit code、digest），層級限於其所測對象 |
| `ORIGINAL_ACK` | 原域 Reader 對其 DonePredicate 出具收據（本輪**無任何**一項達到） |
| `NATIVE_WORLDRAW` | 真世界效果 Raw（本輪**無**） |
| `INDEPENDENT` | 不同技術 SID 的 Protected Checker 判決（本輪**無**） |
| `NOT_RUN` | 未執行 |
| `HOLD` | 前置未成立，已具名 ResumePredicate |

### A.2 本波受影 WP 對帳

| OriginalWP | 狀態 | 本輪實際發生什麼 | 尚未成立的部分 |
|---|---|---|---|
| `WP-FHS-02` | `IMPLEMENTED` | the Fabric policy binding now has real readers: source/stage open an artifact and recompute its digest; the epoch leg binds only through a pinned-key signed FABRIC_ACTIVE_EPOCH@1; a receipt cannot satisfy source/stage and an artifact cannot satisfy active_epoch (POLICY_LEG_EVIDENCE_MISMATCH) | no FABRIC_ACTIVE_EPOCH@1 has been signed by a Policy Owner, no Host has loaded a policy, no HGK consumer receipt has been produced for GJ02, and the pin is a caller-supplied registry - BOUND is not policy-effective |
| `WP-FHS-03` | `HOLD` | R1 is prepared and frozen (ceremony a9194d05, preflight 7/7, registry 3254714b rev13, 31/31, signing-capability challenge with a passing negative control); the fixture mechanics are 10/10 and the admission permit POS/NEG is 6/6 | rev14 does not exist: only the OWNER can run --reissue-issuer. No permit has been minted for GJ02. |
| `WP-FHS-04` | `IMPLEMENTED` | patches 0001-0007 deployed to the runtime root; the live store migrated additively (121 -> 132 objects at schema_version 32); a v99 store is now refused before any DDL; restart produced PID 15180 loading the patched tree; cross-restart row counts reconcile (sessions 363/363, leases 1/1, receipts 78/78) | T2 is NOT_VERIFIED: the only wake observed came from a work item the maker created, which the ruling forbids as evidence. Two scheduler defects were found and only worked around (D-26 script path outside HERMES_HOME/scripts, D-27 tick reading the 1.2 GB root store instead of the profile store). |
| `WP-FHS-05` | `TESTED` | the merged SBL binds a real RepoContext from live git probes (head 70757870, index e9981083, dirty false, untracked 0), checks writable_scope as a subset of the authorised set, and refuses a missing root with RepoContextMissing | PI -> PD -> DEV ECP is blocked: pipeline.intake requires a clause-bound source locator and no GJ02 case source exists in the SBL tree |
| `WP-FHS-07` | `ORIGINAL_ACK` | HG-KSEOS #15 (PLAN ACK bound to a reader receipt) is merged into main at acd9196f | a merge is not a PLAN reader acceptance; no PLAN A/B/C acceptance was performed against the merged code this session |
| `WP-FHS-11` | `NOT_RUN` | the three SPs remain loaded/invoked/non-trigger in the target profile; nothing this session changed that | ConsumerUsed / Remove semantics not measured |
| `WP-FHS-17` | `HOLD` | the rev-13 registry still verifies (OwnerRowLeaf@2, 31/31, rows_unverified []), and the deployed build still verifies it after restart | the two CAP needs (sp.host.load, python.dist:pyyaml) are not qualified, and rev14 cannot exist before the OWNER's ceremony |
| `WP-FHS-20` | `NOT_RUN` | the 192-cell identities are untouched; the missing prose row and the OFF/UNBOUND_OWNER_CONFLICT distinction remain open | no source-owner prose repair, and no token was promoted |

### A.3 證據指標（可重算；路徑相對於本回合根目錄）

| EvidenceRef | sha256 | 證明了什麼 |
|---|---|---|
| `out/REPO_WIRING_R4.json` | `098020c935a963d3…` | the four merges (Fabric #32/#33, SBL #48, HG-KSEOS #15) with merge shas and reader runs on the merged code |
| `out/D24_SCOPED_PR.json` | `bdd082666253d1ad…` | Fabric #34 scope, before/after matrix, refusal codes and honest limits |
| `out/D24_INTEGRATION.json` | `0546c6d232fd700e…` | the two D-24 lanes and their merge |
| `out/GJ02_ORACLE_RED_GREEN.json` | `6bddca21543be99c…` | the same runner separating RED from GREEN with identical oracle bytes |
| `out/FIRSTFAIL_GJ02_CASE_SOURCE.json` | `9c8a6d3e58db4687…` | why DEV ECP cannot be produced (no clause-bound GJ02 case source) |
| `out/P3_MAINTENANCE_WINDOW.json` | `3799177b77d47ba5…` | deploy 0001-0007, additive migration, schema-99 refusal, rollback drill |
| `out/P3_POST_RESTART_ACCEPTANCE.json` | `63e61382fc1841fb…` | new gateway PID, loaded-tree proof, cross-restart data integrity |
| `out/T1_CHILDWORKITEMS.json` | `deb374ed94f9e59e…` | two child work items dispatched and collected with reader-level results |
| `out/R5_RULING_AND_WIRING.json` | `72344550853e3520…` | T2 reclassification, scheduler defects, SBL RepoContext POS/NEG |
| `out/R1_PRERUN_CHECKS.json` | `129933cf5a322580…` | R1 preflight 7/7, ceremony pin, signing-capability challenge |
| `out/OWNER_RULING_D24.json` | `0a780c56b6885a63…` | scope map for the D-24 lanes and the Host Load receipt acceptance |

### A.4 Scoped Holds（具名 ResumePredicate）

- **H-W1-1** FABRIC_ACTIVE_EPOCH@1 signed by the Policy Owner — 原因：no owner signature exists; the producer is only a candidate in Fabric #34；恢復條件：merge #34, then the policy owner signs an epoch receipt with a pinned key against the real policy digest
- **H-W1-2** rev14 registry / Issuer permit — 原因：only the OWNER can run --reissue-issuer in a protected terminal；恢復條件：preflight 7/7 -> owner runs --reissue-issuer once -> original HGK reader verifies rev14, Leaf@2, new-permit POS and old-permit NEG
- **H-W1-3** T2 wake/resume — 原因：the only observed wake used a maker-created due item, which the ruling excludes；恢復條件：a work item admitted by the original scheduler with a genuine due condition, then WakeReceipt/LeaseFence/LastGood read back
- **H-W1-4** DEV ECP — 原因：no clause-bound GJ02 case source in SBL; authoring one would make the maker the author of its own requirement；恢復條件：original GJ02 case artifact, or an OWNER ruling that the round runner+oracle constitute the case
- **H-W1-5** CAP qualification (sp.host.load, python.dist:pyyaml) — 原因：no installer/host-fit evidence this session；恢復條件：original CAP installer run against the GJ02 scope, then the CAP reader

### A.5 本輪明確**不**主張的事

- 不主張任何 WP 達到 `ORIGINAL_ACK`：18 個原主責 WP 的原域 Reader 收據數為 **0**。
- 不主張 `W0_W1_W2_ALL_APPLICABLE_ORIGINAL_WP_DONE=true`；該查詢值仍為 `false`。
- 不主張 Fabric policy 生效：`BOUND` 只表示 artifact 被打開並重算，`FABRIC_ACTIVE_EPOCH@1` 尚無 Policy Owner 簽章，Host 亦未載入。
- 不主張 Issuer 恢復：registry 仍為 rev 13（`3254714b…`），rev 14 須由唯一 OWNER 在受保護終端執行。
- 不主張 T2：唯一觀測到的喚醒來自 maker 自造的到期項，依裁決不得作為 T2 證據。
- 不主張 DEV：本輪**未對任何世界寫入**；WP06 的 RED 是既存 checkout 上的正當缺陷，不是受權效果。

### A.6 母本保全聲明

本檔 = `FHS_PIPD-LS-PKG_W1_r3.md` 全文（868,138 bytes, sha256 `936a8bcb62e16cd205ac8e5799e802293916bbb9de6e5ba8260ea3e1dd013cbf`）＋本章。母本的所有章節、OriginalID、ParentNEG、SourceSHA、Writer/Reader、POS/NEG/SEC、FirstFail、Rollback、HOLD 與 Handoff 均逐字保留；本章不得被引用為對母本條款的修改。
