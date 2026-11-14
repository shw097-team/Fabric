# FHS_vNEXT_PLP_W1｜工程實質正文（r2 修訂版，base 位元保留）

**修訂版**：`W1-CONSTRUCTION-BASELINE-r2-2026-11-14`
**base**：`FHS_vNEXT_PLP_W1_實質正文_施工定案版_2026-11-14_r1.md`｜`base_sha256 = 5cb9ebc5a768ecdfde0441a327ee22b501b6b0a9a615feb81fbffef5c356701a`｜`base_bytes = 115090`
**supersedes**：`5cb9ebc5a768ecdfde0441a327ee22b501b6b0a9a615feb81fbffef5c356701a`（r1 原檔；本版不編輯其任何一個字元）
**修訂人**：W1_R2 施工輪（`W1R2-b840e9285cbc407d`）
**效力**：`OWNER_RULED_CONSTRUCTION_BASELINE`／施工依據不變；本版只把施工輪量測到的三處行為更正、以及四項 owner 裁決，編號加在 base 之前。

```
SOURCE_READ / LOCAL_DRAFT_WRITE / LOCAL_CHECK / AUTHOR_DESIGN
NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / RELEASE_NOT_GRANTED
```

## 修訂表（先讀這一張；可逐列駁回，不必重讀 base）

| # | base 錨點 | 原文讀法 | 修訂後 | POS | NEG | 證據 |
|---|---|---|---|---|---|---|
| AM-01 | §B4.4 TQAEP 的三個必讀欄位 | 「具名 checker 即可取得 TQAEP」的讀法 | 實測：具名 checker 但**沒有** `--checker-receipt` 會 exit 2 `TQ_SOD`（`an independent checker must supply a checker_execution_receipt`）；給了偽回執會 exit 0 但封頂 `TQAEP_DESIGNED`／`independent_acceptance=NOT_GRANTED`／`requires=S5_LIVE_RUNTIME_CHECKER` | POS：`compile-tqaep` 帶真回執 → exit 0，三欄可讀 | NEG：只給名字不給回執 → `TQ_SOD`；偽回執 → 不得提升 ceiling | out/WP05_PIPD_CHAIN.json、out/WP05_BUNDLE4.json |
| AM-02 | §B4.3 validate 的入口形狀 | 「不完整 bundle 會 FAIL」的讀法 | 實測：不完整 bundle 仍回 exit 0、`verdict=PASS`、`scope=PARTIAL_BUNDLE`、`complete=false`、`missing=[…]` | POS：四物件 bundle → `checked=4`、`closure=FULL`、`complete=true`、`scope=FOUR_OBJECT` | NEG：把不完整 bundle 的 `verdict=PASS` 讀成通過 | out/WP05_BUNDLE4.json |
| AM-03 | §B4.1 第 2 步 intake | 「可直接以本文作 intake 來源」的讀法 | 實測：以 115 KB 本文作 `--source` → exit 2 `INTAKE_INVALID`（`ambiguous compound: explicit subjects and predicates required`）；改以短 goal card 作來源 → exit 0，本文仍為權威引用 | POS：goal card 作來源，intent card 記 `source_sha256` | NEG：把分派語法（各有／分別／對應）塞進單一 clause | out/WP05_PIPD_CHAIN.json |
| AM-04 | §E.4 `H-ORIGINAL-ACK` | 「需原 Domain Reader 同 scope 簽署」 | **撤回**：W0 已建成的 `FHS_ORIGINAL_ACK`（`FHS.W0.FhsOriginalAck/3`，6/6，subject W0 r26）本身記 `traditional_definition_status=NOT_APPLICABLE_BY_DESIGN`（L1 18.3 HIST-01／23.4 退役）→ 原域逐域簽署不是規範要求；W1 只做 owner 那一片，計 1/7，不代簽 reader | POS：`owner_semantic_accept` 已簽並驗簽（payload `2b6a9ad6…`） | NEG：把 1/7 讀成 6/6，或由 maker 代簽 reader receipts | out/W1_ORIGINAL_ACK_PARTIAL.json、out/OWNER_ENVELOPE_EVALUATION.json |
| AM-05 | §D.1c `H-485-KEYS` | 「485 逐鍵清冊本地不可得」 | 實測：L2 §08.22–08.26 已逐鍵具名 485 列（20/30/24/25/386），每集合 exact-key digest 可重算（合併 `b3cf9d40…`）；殘餘（原 Tech Registry 登錄檔）依 owner 裁定屬證據稽核瑕疵，不阻斷 | POS：485/485 具名且每列有來源行號 | NEG：以數量相加代替逐鍵 | out/WP17_485_LEDGER.json |
| AM-06 | §D.2 `H-REPO-CREATE` | 「新 `FHS_vNEXT` Repo 未建立」 | 依 Owner 2026-11-14 明示授權：`shw097-team/FHS_vNEXT` 已建立（private、default `main`、head `828bfca4`）；分支保護仍待具 administration 權限的憑證（`H-REPO-PROTECT`） | POS：repo 存在且 private | NEG：以「已建立」推論「已受保護」 | out/REPO_CREATE_READBACK.json |
| AM-07 | §D.3 OpenSpec 版本 | 「選定 2.0.0、本機 1.8.0」 | 已升級：本機 `@fission-ai/openspec@2.0.0`；本輪變更在 2.0.0 下 `validate --strict` 回 `valid` | POS：`openspec --version` = 2.0.0 且 `validate --strict` exit 0 | NEG：以 1.8.0 的行為宣稱 2.0.0 | out/OPENSPEC_UPGRADE.json |

**用法**：要否決某一列，只需指出 `AM-xx`；base 本體未被改寫，所以任何既有條號、錨點與引用都仍然解析。

---

<!-- BEGIN BASE BYTES: retained verbatim, do not edit between the markers -->
# FHS_vNEXT_PLP_W1｜工程實質正文（施工定案版）

**版本**：`W1-CONSTRUCTION-BASELINE-r1-2026-11-14`（Owner 裁決之施工定案版）
**任務書**：`GPT_Work_ThinPrompt_FHS_vNEXT_PLP_W1_2026-11-14.md`，sha256 `85c2bf8f3eae630d3e4ac84294ec69d0bb0418629bcba3538d14d763517db6e6`（Owner 2026-11-14 裁決指定）
**主體**：`FHS_vNEXT_PLP_W1`｜**角色**：`R41` 主編（`R00` 路由；按需短時掛 `R37` W1 Repo／ABI、`R42` 技術現況、`R43` 來源覆蓋）
**裁決**：Owner 2026-11-14 明示「已無擋住開工的缺口，產出可施工定案版」——本檔即該定案版
**生成**：2026-11-14（台北 UTC+08:00）｜**工作區**：`<WORKSPACE>\FHS_NEXT_Workspace\W1_GPTWORK_20261114`
**語言／換行**：zh-TW／UTF-8／LF

## 效力（Owner 裁決定案）

**Owner 裁決（2026-11-14）**：現版已無擋住開工的缺口，故本檔為 **可施工定案版**，全部條款可直接用於 W1 施工；不再是候選或草案。

**授權範圍**：施工（施工順序、I/O、Consumer、POS/NEG、Exit、HOLD/Resume/Rollback 依本檔執行）。
**不在授權範圍**：Native 准入、Independent 驗收、Release、origin `main` 變更、Repo 建立——這四項仍須原域各自程序。

```
OWNER_RULED_CONSTRUCTION_BASELINE / HOST_PENDING / EXECUTOR_UNBOUND /
NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / RELEASE_NOT_GRANTED
```

| 本版可以主張 | 本版不主張 |
|---|---|
| `SOURCE_READ`：每個母本有實檔 SHA | `NATIVE_SIGNED`：無原生准入 |
| `AUTHOR_DESIGN`：可施工的 W1 規劃與條款 | `INDEPENDENT_PASS`：無受保護 Checker 簽署 |
| `LOCAL_CHECK`：本機可重跑的命令與結果（第 B4、E 節） | `RELEASE_GRANTED`：無 Publisher／Release |
| 原 ID／原 Consumer／原 NEG 未被刪改（可逐條回查） | 任何 origin `main` 變更、PR merge、Repo 建立 |

**三個治理角色（本輪先掛載，再寫一個字）**

| 角色 | 掛載物 | 本輪實際狀態 |
|---|---|---|
| Fabric＝治理契約 | `FHS_NEXT/Fabric/INTEGRATION/FHS/{README.md,repository-map.json,validate_entry.py}` | `effect_permission=NONE`、`unknown_route=HOLD_AFFECTED_WRITE_ONLY`、`source_state=PROPOSED_NOT_OWNER_RATIFIED`；實跑 `validate_entry.py --route …`：已知路由 exit 0（`claim_ceiling=NAVIGATION_ONLY`）、未知路由 exit 3（`HOLD_AFFECTED_WRITE`） |
| SBL＝產品工程指揮入口 | `FHS_NEXT/SBL/AGENTS.md`、`SBL/integrations/pipd`（Canonical Writer／Reader，13 commands／19 families） | 以 `PYTHONPATH=…/integrations/pipd/src` 在沙箱驅動；未修改 origin |
| HG-KSEOS＝原生授權／狀態／驗收平面 | `FHS_NEXT/HG-KSEOS/AGENTS.md`、`src/hg_kseos/{spine,recovery}.py`、`scripts/hgk-lane-guard.py` | lane guard raw：`decision=REFUSE`、`epoch=41` vs `live_epoch=44`、`admission_status=UNPROVEN`；`SharedSpine` 在沙箱 DB 實測 14/14（見 E 節） |

---

## 0｜怎麼用這份正文

1. **要開工**：讀 §1（W1 法位與 13 主責章）→ §C（逐章條款）→ §B3（WP／DAG／輪次）。施工者不需要附錄即可依 WP 落工。
2. **要接鏈路**：讀 §B4（PI／PD／ECP／TQAEP 的作者調用方式與實測退出碼）。
3. **要判能不能做**：讀 §D1（485 與受保護分母）、§E（POS／NEG／FirstFail）、§E.4（受影 HOLD）。
4. **要搬 Repo／換工具**：讀 §D2（新 `FHS_vNEXT` Repo 與逐路徑遷移）、§D3（每個工具指定一版）。
5. **要交原域**：讀 §F（跨波 handoff 與終態）。

本正文**不依賴附錄補條款**；附錄只放來源 SHA、逐列證據、外部研究 URL 與自審原始輸出。

**用語說明**：引用原 r9 條文時保留其原文用詞（含「候選」字樣），那是對來源的逐字引述；在本檔的定案效力下，那些受影輸出即為施工定案輸出，不再另行等待版本升級。

---

## 1｜W1 的法位、主責範圍與不可讓渡邊界

### 1.1 法位

- W1 位於 L0《FHS_vNEXT_總藍圖》→ L1《FHS_vNEXT_PLP_藍圖》→ L2《FHS_vNEXT_PLP_全波次藍圖》→ W0 交付版（r9，`aeeab20d…`）之下，是**產品工程波**。
- 對 W0 與 W2–W4 的關係固定為 `CROSS_WAVE_READ_ONLY_HANDOFF`（CH-49）：W1 只交 `Source／OriginalID／Case／ExpectedRaw／受影 HOLD`，不得宣稱 TraceClosure、獨立 Checker 或 Publisher cutover。
- 母本候選：`FHS_vNEXT_PLP_W1_藍圖_r8`（`2026-11-14_r8_AUTHOR_DRAFT`，`sha256` 見附錄 A）與作者候選正文 r9。**兩者皆為候選，不因版本號較新而生效。**

### 1.2 13 個 W1 主責章（固定）

`CH-08`、`CH-12`、`CH-13`、`CH-14`、`CH-16`、`CH-17`、`CH-18`、`CH-19`、`CH-20`、`CH-22`、`CH-34`、`CH-39`、`CH-40`
（其餘 37 章維持原名／原序，只做消費與 typed handoff，不偷移主責。）

### 1.3 W1 八 WP（固定）

`WP-FHS-02`、`WP-FHS-03`、`WP-FHS-04`、`WP-FHS-05`、`WP-FHS-07`、`WP-FHS-11`、`WP-FHS-17`、`WP-FHS-20`
（與全域 22 WP／36 Edge 的關係見 §B3；本輪 W0 已完成範圍不重跑、不倒扣。）

### 1.4 不可讓渡的四條線

1. **唯一 Human OWNER／issuer**：本版任何段落都不得被讀成 Native 許可、Permit、Release。
2. **Maker 不得自簽**：本版雖為 Owner 裁決之施工定案，仍不構成原 Reader ACK、Native E2E、Independent PASS 或 Release；定案的是施工依據，不是驗收結論。
3. **不得新造第二套** Issuer／Compiler／Queue／Checker／Publisher；PIPD 原 Canonical Writer 是 `SBL/integrations/pipd`，HG-KSEOS 是原生平面，Fabric 只是導覽（`effect_permission=NONE`）。
4. **不刪舊資料、不轉移原 Domain 權威**：原 ID、原 Parent、原 NEG、原 Consumer 一律保留可回查。

---

## A｜來源、差額與本版如何收斂前版審查

### A.1 六步 SOP 的落地結果

| 步 | 做法 | 本輪結果 |
|---|---|---|
| ① 索引 | 先讀三庫入口與知識庫索引，不把長文塞進常駐上下文 | 三入口已掛載（見封面表） |
| ② 定位實質條文 | 以檔名＋SHA 定位 L0／L1／L2／W0 r9／W1 r8／W1 r9／升級藍圖 r4／W1 r5 | 全部落地，SHA 見附錄 A |
| ③ 核心詞全文檢索 | 對「各有／分別／對應／若／不得」與原 ID 做全文檢索 | 引用 166 條、18 個來源 ID、0 個同 ID 混版（附錄 A.3） |
| ④ 交叉驗證 | 上游條文 × Repo As-Built × 原 Registry exact-set | 13 CLI／19 families／8 skills 以 registry 實檔核對（§B4.1） |
| ⑤ 拆子要求 | 把複合句拆成獨立可判定子要求 | 13 主責章 × 12 欄契約（§C） |
| ⑥ 正文判定 | 每條要有具體功能、I/O、Consumer、POS/NEG | §C／§E |

### A.2 母本與版本（皆以實檔 SHA 認定）

| 代號 | 檔案 | 角色 | 本版用法 |
|---|---|---|---|
| UP4 | `FHS_NEXT_升級藍圖_r4.md` | 校準 Fabric／HG-KSEOS／SBL 原意、痛點、定位 | 校準 §B1 的 P01–P07 與 §D3 的技術現況 |
| L0／L1／L2 | `FHS_vNEXT_總藍圖.md`／`FHS_vNEXT_PLP_藍圖.md`／`FHS_vNEXT_PLP_全波次藍圖.md` | 上位法位與全波次 | §C 章法位、§B3 DAG、§D1 485 皆引 L2 |
| W0 r9 | `FHS_vNEXT_PLP_W0_2026-11-14_r9_交付版.md` | 已完成範圍（`W0_SCOPE_COMPLETE`） | 不重跑、不倒扣；只接手 handoff |
| W1 r8 | `FHS_vNEXT_PLP_W1_藍圖_r8.md` | 前代候選母本 | 差異比對，不因較新而生效 |
| W1 r9 | `FHS_vNEXT_PLP_W1_實質正文_AUTHOR_DRAFT.md` | 作者候選正文（本版基底） | 高保留整合；逐列證據不重複搬運，原檔 SHA 可回查 |
| W1 r5 | `FHS_PIPD-LS-PKG_W1_藍圖_skeleton_2026-11-04_r5.md` | 歷史規格 | 原義與原 ID 來源 |
| 角色表 | `FHS_vNEXT_專業角色總表_r2.md` | R00 路由與角色定義 | 見封面角色欄 |

### A.3 本版吸收的前版審查結論（十項，逐項有處置）

本輪之前已對 r9 做過破壞性審查；本版不重複貼證據，只寫**處置**（證據在附錄 B）：

| 前版裁決 | 本版處置 |
|---|---|
| F-01 §09 的 `TASK` 列 bytes 欄錯（宣告 99,558，實檔 9,604） | 來源改以 Owner 指定的任務書 SHA 認定（`85c2bf8f…`）；bytes 欄不再引用 |
| F-02 `validate` 入口形狀（PI 當 bundle 會誤導） | §B4.3 明訂四物件 bundle 與 `complete` 讀法 |
| F-03 偽／缺回執不提升 ceiling | §E.2 N-03 以「不得提升 `claim_ceiling`」表述 |
| F-04 caller `--head` 無效但 `verified:true` 易誤讀 | §E.2 N-04 要求只讀 `matches_host` |
| F-05 外部 producer 證據會被接受 | §B2.4 保證降級為「registered evidence binding」 |
| F-06 effect ECP 需 git 正本 registry | §B4.2 標 `NOT_EXERCISED_ON_THIS_TREE`＋恢復條件 |
| F-07 lane guard epoch 41 vs 44 `REFUSE` | §E.4 `H-GUARD-EPOCH` 具名 HOLD |
| F-08 三根非 git | §D2 遷移設計的前提；不以 commit 對齊宣稱 |
| F-09 `init` 後 `doctor` FAIL、exit code 不穩 | §B4.1 以 source-mode 解析為前置，`doctor` 連 exit code 記錄 |
| F-10 結構宣告與實測未綁 | §C 以實測 50／24／57／22／36／13／19／8 作權威數字 |

---

## B｜三份 SPEC（Product／Architecture／Program）

### B1｜Product SPEC

**Owner／形狀**：唯一 Human OWNER，單人單機；不做發行級過度治理。任何「已通過」都必須能被指名到 Owner 的原始簽署物件，否則只是作者設計。

**JTBD → FUO**

| Job | FUO（唯一輸出物） | 可判定完成 |
|---|---|---|
| 產品負責人要能在**一台機器**上把 Fabric／HG-KSEOS／SBL 的原意、權限與狀態串起來用 | 可施工的 W1 正文＋可驗的 POS/NEG | 13 主責章每章 I/O／Operation／Consumer／POS／NEG／Exit 齊備 |
| 工程者要能依 WP 落工而**不需要再翻舊冊** | 8 W1 WP × 22 WP／36 Edge × R0–R8 輪次 | 每 WP 有依賴、Consumer、Exit、HOLD 與回退點 |
| 驗收者要能**獨立重跑**同一結論 | 命令＋退出碼＋輸出片段（§B4、§E） | 同命令在同樹重跑得同一 SHA（已驗：`compile-pi`／`compile-ecp` 連跑兩次同 SHA） |

**P01–P07 七痛點（原義，逐列 POS/NEG）**

| 痛點 | 當期功能定義（原文） | POS | NEG | 章／WP |
|---|---|---|---|---|
| P01 選型困難 | Need×Kind×Host×Effect×License→一個當期Occupant/具名NoFit，原24槽必需功能不降optional | 24槽各有功能結果與Consumer；未部署仍SELECTED_NOT_QUALIFIED | 485槽全安裝或NoFit後私裝 | CH22/WP17→W3 WP13 |
| P02 跨工具交接斷裂 | 同Subject/SourceSHA/Scope/ABI的Producer輸出經原Consumer ACK/NACK | 五Seam逐欄round-trip；CH12保to-tickets五路 | 只有箭頭/PR merge即稱跨域完成 | CH16/WP05→W2 WP06/08 |
| P03 重問／決策失憶 | QUESTION_LEDGER_REUSE按Subject＋Scope＋SourceSHA及同題原Reader查KnownAnswer/pending | 同鍵REUSED_ANSWER新問0；真未知未pending才問1次；pending問0 | typed-review替原QuestionLedger或來源漂移仍沿用 | CH22/WP17/11；W0 CH10原責保留 |
| P04 Writer碰撞 | SBL/Fabric/HGK原域各一Writer；方法及@2側車不寫Canonical/Permit | 原13CLI/19Family/8Skill與S1–S5不增第二Writer | OpenSpec造PI、FHS造Issuer/Queue、角色冒Principal | CH12/18/WP05/03 |
| P05 虛假PASS | 原Case/Oracle/Host/WorldRaw及不同受護Principal Checker，各證據只證自身scope | 作者自檢、原Runner與Protected verdict分欄且NEG不借證 | CI綠、零測試exit0、PLAN_VALID、自簽Receipt冒Native | CH39/40/WP05→W2 WP09/W3 WP10 |
| P06 Host掛載失真 | Installed→Loaded→Invoked→Consumed→Uninstalled，模型另分Selected/ActualServed/Usage | 每Host×SP各有trigger/nontrigger/remove Raw；新PID及ProfileSHA可核 | UI Selected/檔案存在/worker_bound當實際使用 | CH08/19/WP11/04→W3 WP12 |
| P07 FUO最後一哩 | 普通Goal最短READ/DRAFT成果；受權Diff可回退，長工沿原WorkID可續行 | GJ01/02/03分案，SourceAnswer/三SPEC/真Diff/Resume均有原Consumer | ZIP檔數或Kanban Done當完整產品；UNKNOWN盲重試 | CH20/34/WP04/07→W2/3/4原出口 |

**Must（不可降級）**：單人單機可自治；原 ID／原 Consumer 不得改；受保護效果分治；W1 不得以「尚未 Host-qualified」刪除必需功能；任何工具缺口只停該槽（`SELECTED_NOT_QUALIFIED`），不得改 optional。
**Non-goal**：不做發行級治理產品；不自建第二套 Issuer／Compiler／Checker／Publisher；不在本輪建立 Repo、不改三庫 `main`、不簽 Native／Release；不把 W1 正文摘要成 W2–W4 的平行法位。

### B2｜Architecture SPEC

**五個 Seam（原身份，來自 L0 §04.2；不得重編）**

| Seam | 接口（原 Writer → 原 Reader） | 承載 | 拒收／FirstFail |
|---|---|---|---|
| S1 Source/Intent/Profile→PI | 原 Source/Authority/Profile Reader → SBL-hosted PIPD Writer | contained SourceManifest、OriginalID/Parent/NEG、profile veto → strict PI；crosswalk放@2側車 | Source漂移／側車塞strict → `PI_SCHEMA_NACK` |
| S2 PI→PD/ECP/TQAEP | 原 PI Writer → Repo/Case/Construction Reader | PI digest＋live RepoContext→PD；ConstructionContract/ECP 各 effect；TQAEP原Case/Oracle | 假HEAD／stale preimage／假Runner → `PD_BINDING_HOLD` |
| S3 PLAN/Policy→HGK Admission | 原 PLAN CAS／Fabric Policy Consumer → 原 HGK Issuer | ExpectedRevision、ActiveEpoch、LoadedDigest、exact WriteSet/TTL/Nonce→原Issuer決定 | stage當active／ECP當Permit → `ADMISSION_DENY` |
| S4 Work→Hermes/Codex→World | 原 HGK SharedSpine → 既有 Hermes native task／指定Worker → 原 World Reader | WorkID/TaskID/operation/lease generation/cursor 對照；結果與 Raw 回同scope | card Done充世界結果／ACK loss重播 → `UNKNOWN_RECONCILE` |
| S5 Raw/Oracle→Checker/Publisher | 原 Case/World Reader → 不同受保護Principal Checker → 原 Publisher | 同Candidate/Host/Scope/FUO的Raw；需要發行才進原Publisher | Maker自核／gstack ship冒發行 → `CHECKER_SCOPE_NACK` |

**ABI 的 exact-set（以原 Registry 實檔核對，非照抄過期列舉）**

| 集合 | 數量 | 成員（實測） |
|---|---|---|
| CLI | 13 | `init`、`intake`、`profile`、`compile-pi`、`bind-pd`、`compile-ecp`、`compile-tqaep`、`validate`、`doctor`、`project`、`export`、`diff`、`repair`（`pipd_ls_sp.cli --help` 實印） |
| Contract family | 19 | ArtifactIdentity、AuthorityBinding、RequirementAtom、ProfileBinding、TechnologyAdmission、PI-PKG、PD-PKG、ECP、TQAEP、TraceLink、ClaimCeiling、EvidenceExpectation、ConstructionContract、ExecutionHandoff、ExecutionBindingRef、WorkOrderCandidate、TaskSpecSeed、SurfaceProjectionManifest、GENIEProjectionRef（`schemas/registry.json`） |
| Skill | 8 | `pipd-authority-source`、`pipd-route-intake`、`pipd-profile-tailor`、`pipd-pi-compile`、`pipd-pd-bind`、`pipd-execution-contract`、`pipd-assurance-tqaep`、`pipd-package-project` |
| Effect（六類分治） | 6 | `SOURCE_READ`、`LOCAL_DRAFT_WRITE`、`DEV_REPO_WRITE`、`HOST_OPS`、`USER_EFFECT`、`RELEASE_EFFECT` |
| Lane | 3 | `PLAN`、`EXECUTE`、`VERIFY_SECURITY` |
| Host surface | 12 | `{Hermes,Codex,ClaudeCode,ChatGPT}×{TPM,Commander,Challenge}` |
| Capability card | 57 | `A01`–`A57` |

每個 effect 各自有 permission、World readback、recovery；**不得用路徑推效果、不得借 DEV Grant 做 OPS、不得用 `git revert` 冒 Host 回復**。

**六個 ADR（本版必須遵守的架構決策）**

| ADR | 決定 | 邊界／不可做 |
|---|---|---|
| ADR-W1-01 單庫不奪原權 | 未來單一產品 Git root；三原庫以 immutable ref／經許可 snapshot 接入 | 不複製成第二 Compiler／Issuer／Policy Writer |
| ADR-W1-02 原生優先 | Hermes v0.23.1 原 Profiles/Kanban/Delegation/Swarm/Runtime；不加第二排程器 | 各 Host／Provider 的實際 Loaded/Invoked/Used 另核 |
| ADR-W1-03 方法不奪權 | OpenSpec v2.0.0、gstack v1.99.2.0 及四 source-pinned 方法產建議／SpecDelta | 不讓方法 archive/ship／review文字變 Grant、Verdict、Release |
| ADR-W1-04 PI/PD 晚綁 | PI 保來源語義；PD 只依真 Git/HEAD/Scope/preimage 綁定 | 原 Compiler 未用則 EXECUTOR_UNBOUND；不拿摘要 ACK 代重解析 |
| ADR-W1-05 六效果分治 | READ/DRAFT/DEV/OPS/USER/RELEASE 各有 permission、World readback、recovery | 不用路徑推效果、不借 DEV Grant 做 OPS、不用 git revert 冒 Host 回復 |
| ADR-W1-06 受影驗證 | 先固定原預期、原子義與正負案例；只驗本次改動及依賴錐 | 不重做 W0、不改 Oracle 湊綠、不宣作者檢查為 Independent |

### B3｜Program SPEC

**22 WP／36 Edge／R0–R8（實測自 r9 結構，已驗無環）**

| 輪次 | 可施工 WP（依依賴圖實推） |
|---|---|
| 輪次 | 可施工 WP（依依賴圖實推） |
|---|---|
| R0 | `WP-FHS-00` |
| R1 | `WP-FHS-01`、`WP-FHS-04`、`WP-FHS-15`、`WP-FHS-16`、`WP-FHS-19` |
| R2 | `WP-FHS-02`、`WP-FHS-03`、`WP-FHS-05`、`WP-FHS-07`、`WP-FHS-21` |
| R3 | `WP-FHS-11`、`WP-FHS-17`、`WP-FHS-20` |
| R4 | `WP-FHS-06`、`WP-FHS-13` |
| R5 | `WP-FHS-08` |
| R6 | `WP-FHS-09`、`WP-FHS-18` |
| R7 | `WP-FHS-10`、`WP-FHS-14` |
| R8 | `WP-FHS-12` |

W1 主責 8 WP 落在 R1–R3（`04` 在 R1；`02/03/05/07` 在 R2；`11/17/20` 在 R3），施工順序即上表；`WP-FHS-05` 僅依 `WP-FHS-01`（未被 `WP-FHS-15` 硬綁），`E10` 為 `WP-FHS-17 → WP-FHS-06`（非反向）。

**每個 WP 的 Exit 與回退**：Exit＝該 WP 的輸出契約在其原 Consumer 手上可解析且有同 scope 證據或 typed HOLD；回退＝撤本 WP 受影輸出，不撤原波已完成的合法作用（見 §B4.4 的實測）。

**Stop／Resume／Rollback（以原生平面實測語義為準）**

| 情境 | 行為（實測） | 對 W1 的規定 |
|---|---|---|
| 第二寫者搶同一 resource | `ERR_DUAL_WRITER` | 並行寫入立即停，只停該 resource |
| ACK 遺失後重送同一 idempotency key | 回原 `event_id`、`idempotent_replay=true` | 可直接重試，不得產生第二事件 |
| 同一 key 用到別的 subject | `ERR_IDEMPOTENCY_KEY_REUSED_FOR_OTHER_SUBJECT` | 停該結案，不得借他主體結果 |
| 終局 verdict 再改 | `ERR_ACCEPTANCE_ILLEGAL_TRANSITION` | 歷史不重寫；撤銷是另一件受治理事件 |
| lease 過期 | `ERR_LEASE_EXPIRED` | 重新取 lease 才能續寫 |
| 備份竄改／還原覆蓋 | `ERR_BACKUP_DIGEST_MISMATCH`／`ERR_RESTORE_TARGET_EXISTS` | Rollback 只回舊快照，不覆蓋現行庫 |

### B4｜PI／PD／ECP／TQAEP：可執行範圍與實跑結果

> 本節全部在沙箱（`sbx/`）執行，origin 未修改；指令可直接照抄進 W1 施工。命令前綴：`PYTHONPATH=<repo>/SBL/integrations/pipd/src`、`PYTHONDONTWRITEBYTECODE=1`。

#### B4.1 正向鏈（實測 exit 0）

| 步 | 命令 | 產物 | 實測 |
|---|---|---|---|
| 1 | `pipd init` | `docs/ schemas/ src/ tests/ dist/` | exit 0；注意：`schemas/` 為空會使 `doctor` 轉 workspace-local 並 FAIL（見 §E.3） |
| 2 | `pipd intake --goal … --source … --constraint … --non-goal …` | `intent.card.json`（帶 atoms） | exit 0 |
| 3 | `pipd profile --profile STANDARD` | `profile.json` | exit 0；`--profile` 收**名稱列舉**，給檔案路徑會 `PROFILE_VETO`（exit 2） |
| 4 | `pipd compile-pi --intent intent.card.json --profile STANDARD` | `pi.json`（帶 `_profile_meta`） | exit 0；連跑兩次同 SHA `e6f5922e…` |
| 5 | `pipd bind-pd --pi pi.json --repo-root <git toplevel>` | `pd.json` | exit 0；`RepoContext.head`＝live `826ca066…` |
| 6 | `pipd compile-ecp --pd pd.json --pi pi.json` | `ecp.json` | exit 0；連跑兩次同 SHA `8278c952…` |
| 7 | `pipd compile-tqaep --pi … --ecp … --maker M --checker C [--checker-receipt R]` | TQAEP | exit 0；必讀 `claim_ceiling`／`independent_acceptance` |

#### B4.2 effect 型 ECP：本樹不可執行（`NOT_EXERCISED_ON_THIS_TREE`）

- 帶 `--effect-intent <EFFECT> --operation-registry … --operation-registry-sha256 …` → exit 2 `REGISTRY_NOT_CANONICAL`（registry 必須是 git 已提交正本）。
- 帶 `--effect-intent` 但不給 registry → exit 2 `GIT_PROBE_FAILED`。
- 恢復條件（最小）：把 `integrations/pipd` 放進 git 正本樹或 worktree，令 `schemas/registry.json` 的 blob 與 `--operation-registry-sha256` 相符，再重跑同命令。

#### B4.3 `validate`：入口形狀決定成敗

| 輸入 | exit | 結果 |
|---|---|---|
| 四物件 bundle（`PI-PKG`／`PD-PKG`／`ECP`／`TQAEP`） | 0 | `verdict=PASS`、`checked=4`、`closure=FULL`、`complete=true`、`findings=[]` |
| 只給 `{"PI-PKG": pi}` | 0 | `checked=1`、`complete=false`、`missing=[PD-PKG,ECP,TQAEP]` |
| 把 `pi.json` 直接當 bundle | 2 | `INPUT_SHAPE_INVALID`，訊息指向不存在的 `_profile_meta.schema.json`（誤導） |

規矩：**驗收一律用四物件 bundle**；`complete=false` 不得讀成 PASS。

#### B4.4 TQAEP 的三個必讀欄位與兩種「不可以」

| 欄位 | 實測值樣態 | 讀法 |
|---|---|---|
| `acceptance[0].claim_ceiling` | `TQAEP_DESIGNED` | 設計期產物（非驗收結論） |
| `acceptance[0].independent_acceptance` | `NOT_GRANTED` | 未取得獨立接受 |
| `acceptance[0].independent_proof_requires` | `S5_LIVE_RUNTIME_CHECKER` | 要獨立必須 live runtime checker 重跑 |

- 不可以：把「有回執字串」讀成「已驗證」（自寫偽簽／他主體／不存在的路徑都 exit 0 但不提升 ceiling）。
- 不可以：把 `caller_claims.head.verified=true` 讀成「caller 的 HEAD 已驗證」——`verified` 來自 host 證據；任用端只讀 `matches_host`。

---

## C｜50 章：13 主責章實質、37 章原義與跨波交接

**結構事實（實測）**：`CH-00`–`CH-49` 共 50 章，依序、無重複；R6 marker 324 對全數配對；anchor 353、重複 0；內部連結 132 條（去重 61）全數可解析；HOLD 45 列。
**13 主責章**：`CH-08`、`CH-12`、`CH-13`、`CH-14`、`CH-16`、`CH-17`、`CH-18`、`CH-19`、`CH-20`、`CH-22`、`CH-34`、`CH-39`、`CH-40`——每章 12 欄契約全數在場（Source／Input／Producer→原Reader／Consumer／Operation／Output／POS／NEG／Case／FirstFail／Dependency／Exit／HOLD／Resume／Rollback）。
**其餘 37 章**：保留原名、原序、原法位與原 Consumer，只做消費與 typed handoff；不重寫、不偷施工原主波。

### C.1 13 主責章（每章：法位 → 12 欄契約 → 章內結構 → 原文 SHA）

### CH-08｜SBL SharedCore 六模組與三 SP 的完整產品鏈

**法位（原文）**：**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L992–1051`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** SBL Product/三 SP；L2-r4:L898。原 Domain Reader/Writer 不因本章轉移。

**原文位置**：r9 `CH-08`，63,098 bytes，sha256 `605eb792fd4f14127499e07cce0f6fd8fff22a9d68c22fa5e44d9f3259b3aa60`（本版未刪原文，僅未重複搬運逐列證據）


**R6 當期實質操作（逐字）**

- **Source**：`W1-SKEL:L1445@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- **Input**：SBL SharedCore 原六模組及 TPM／Commander／Challenge。
- **Producer→原Reader／Consumer**：作者編設計、正式產物沿原Writer→原 SBL SharedCore／SP Product Reader。
- **Operation**：逐模組沿原 DOC-01/03 Reader；TPM 編三 SPEC，Commander 只提 Native PLAN，Challenge 只 advisory。
- **Output**：SharedCore／ThreeSP QualificationPlan，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。
- **POS**：三 SP 功能和 permission 互不混淆。
- **NEG**：TPM 代 Challenge 簽核或新造 SharedCore Writer。
- **Case／FirstFail**：`AUTHOR.W1.CH-08.POS/NEG/SEC`／`AUTHOR.W1.CH-08.SOURCE_OR_CONSUMER_NACK`；安全反例是本章跨原權限/Scope借據，由原邊界判，不是作者安全verdict。
- **Dependency／施工序**：先原Source/已知答案，後本章對應WP/36Edge的具名Receiver；本章無W1主責時只消費/typed handoff，不偷施工原主波。
- **Exit**：上述I/O和正反案例在正文可用；原域完成須原 SBL SharedCore／SP Product Reader真正接受本次受影body及適用Raw，本文不代簽。
- **HOLD／Resume**：相應HOLD見CH48，缺原ID/ABI/例外/Runner就只停該受護效果；補原Reader同scope ref後重綁受影輸出。合法READ/DRAFT持續。
- **Rollback**：撤受影 Host-SP activation，不拆原 Core。

**本章結構（原文節標題與首句）**

- `本版主責章實質契約｜CH-08`：**Input**：Owner Goal、Persona/Pain、原 Kind/Mode/Host、六 SBLM 與 TPM/Commander/Challenge 各自責任。
- `R6 當期實質操作｜W1主責`：- **Source**：`W1-SKEL:L1445@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- `r4 當期原 Reader 鎖與非降級本體`：本章 L1-r4 依以上真實行區間及原域 Reader；無單獨 R4-BEGIN 增量不等於以歷史 r2 取代 L1。W1 契約下文僅是對該 L1 已定義原義的工程操作化。
- `W1 整合操作規格、已填契約與逐項 POS/NEG／FirstFail`：**Protected Original H1**：`L1:650–695`（`L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`），L2 作者端路由 `L2:646`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W1 …
- `A. 本章實質功能與不能壓平的原義`：Goal → SBL Shared Core（M01 Intake／M02 SPEC／M03 Routing／M04 Bridge／M05 Evidence／M06 Bounded Repair）→ TPM/Commander/Challenge 三 SP 的原產品鏈。保全原 Source/OriginalID/Parent/否定作用域、版本及 Recei…
- `B. 本版已完成的章契約與工程操作`：| 契約欄 | 本版具體內容 |
- `C. Input → Producer → 原 Reader／Consumer → Output`：- **Input/Guard**：Goal/OriginalRequirementRefs/Persona/Kind/Scope/three distinct SP-role facts。
- `D. POS／NEG／FirstFail／HOLD／退出`：- **POS（期待）**：各模組有獨立可觀測 FUO 與拒越權；Reader 回 typed NACK 仍可追蹤。

### CH-12｜PIPD 13 CLI／19 Contract Families／8 Skills 與唯一 Writer

**法位（原文）**：**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L1257–1383`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original PIPD Registry/Compiler；L2-r4:L902。原 Domain Reader/Writer 不因本章轉移。

**原文位置**：r9 `CH-12`，96,521 bytes，sha256 `1a4119bd095c0912732e322f69ad889d52070b524884fac9f076bd68bca414be`（本版未刪原文，僅未重複搬運逐列證據）


**R6 當期實質操作（逐字）**

- **Source**：`W1-SKEL:L1583@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- **Input**：原 SBL Registry JSON、CLI COMMANDS、八 SKILL 正文。
- **Producer→原Reader／Consumer**：作者編設計、正式產物沿原Writer→原 SBL PIPD Registry／Compiler Reader。
- **Operation**：使用本版逐項清單驗 13/19/8 exact-set；schema seam-only 不得冒執行 Writer。
- **Output**：PipdExactSet／OriginalWriterHandoff，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。
- **POS**：ExecutionBindingRef 保第19；無 compile-cc。
- **NEG**：第14 verb、ExecutionBinding 替名或自簽 Canonical。
- **Case／FirstFail**：`AUTHOR.W1.CH-12.POS/NEG/SEC`／`AUTHOR.W1.CH-12.SOURCE_OR_CONSUMER_NACK`；安全反例是本章跨原權限/Scope借據，由原邊界判，不是作者安全verdict。
- **Dependency／施工序**：先原Source/已知答案，後本章對應WP/36Edge的具名Receiver；本章無W1主責時只消費/typed handoff，不偷施工原主波。
- **Exit**：上述I/O和正反案例在正文可用；原域完成須原 SBL PIPD Registry／Compiler Reader真正接受本次受影body及適用Raw，本文不代簽。
- **HOLD／Resume**：相應HOLD見CH48，缺原ID/ABI/例外/Runner就只停該受護效果；補原Reader同scope ref後重綁受影輸出。合法READ/DRAFT持續。
- **Rollback**：恢復原 registry pin；只重編受影候選。

**本章結構（原文節標題與首句）**

- `本版主責章實質契約｜CH-12`：**Input**：非空來源、Goal、原 13 CLI help／19 Schema family／8 skill、原 operation registry 與 to-tickets 原需求。
- `R6 當期實質操作｜W1主責`：- **Source**：`W1-SKEL:L1583@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- `r4 當期原 Reader 鎖與非降級本體`：本章 L1-r4 依以上真實行區間及原域 Reader；無單獨 R4-BEGIN 增量不等於以歷史 r2 取代 L1。W1 契約下文僅是對該 L1 已定義原義的工程操作化。
- `W1 整合操作規格、已填契約與逐項 POS/NEG／FirstFail`：**Protected Original H1**：`L1:847–959`（`L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`），L2 作者端路由 `L2:650`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W1 …
- `A. 本章實質功能與不能壓平的原義`：SBL-hosted PIPD Canonical Reader 規格，13 CLI／19 families／8 skills 並列驗證，不創第14命令。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。
- `B. 本版已完成的章契約與工程操作`：| 契約欄 | 本版具體內容 |
- `C. Input → Producer → 原 Reader／Consumer → Output`：- **Input/Guard**：原 SBL Current HEAD/registry SHA、PIPD installed version、CLI help/doctor Raw、Source refs。
- `D. POS／NEG／FirstFail／HOLD／退出`：- **POS（期待）**：命令 13 unique，family 19 exact，skill packs 8；可見真正原 Reader response。

### CH-13｜Authority SourceFreeze／Profile Tailoring／原 PI 的 18 領域

**法位（原文）**：**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L1384–1448`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original PIPD Authority/Profile/PI Writer；L2-r4:L903。原 Domain Reader/Writer 不因本章轉移。

**原文位置**：r9 `CH-13`，31,487 bytes，sha256 `95c1c553577d9db81a3406b9269e6e2e95e251dab21ea4e4be74adfbf8944c71`（本版未刪原文，僅未重複搬運逐列證據）


**R6 當期實質操作（逐字）**

- **Source**：`W1-SKEL:L1682@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- **Input**：SourceFreeze／ProfileBinding／IntentCard 與 18 領域原 PI。
- **Producer→原Reader／Consumer**：作者編設計、正式產物沿原Writer→原 Authority／Profile／PI Reader。
- **Operation**：原 Writer 先讀來源與 veto 後編 PI；18 領域的原定義沿原 Reader，@2 側車不得進 strict payload。
- **Output**：PI CompileRequest／原 PI 候選期待，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。
- **POS**：原 ID/parent/NEG/Oracle trace 齊，安全深度不降。
- **NEG**：未凍 source 或用側車欄位塞 strict PI。
- **Case／FirstFail**：`AUTHOR.W1.CH-13.POS/NEG/SEC`／`AUTHOR.W1.CH-13.SOURCE_OR_CONSUMER_NACK`；安全反例是本章跨原權限/Scope借據，由原邊界判，不是作者安全verdict。
- **Dependency／施工序**：先原Source/已知答案，後本章對應WP/36Edge的具名Receiver；本章無W1主責時只消費/typed handoff，不偷施工原主波。
- **Exit**：上述I/O和正反案例在正文可用；原域完成須原 Authority／Profile／PI Reader真正接受本次受影body及適用Raw，本文不代簽。
- **HOLD／Resume**：相應HOLD見CH48，缺原ID/ABI/例外/Runner就只停該受護效果；補原Reader同scope ref後重綁受影輸出。合法READ/DRAFT持續。
- **Rollback**：重凍受影 source/profile，重編 PI 下游。

**本章結構（原文節標題與首句）**

- `本版主責章實質契約｜CH-13`：**Input**：真 SourceID/path/SHA/span、原 parent/child/否定作用域、AuthorityBinding 衝突與 Profile axes。
- `R6 當期實質操作｜W1主責`：- **Source**：`W1-SKEL:L1682@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- `r4 當期原 Reader 鎖與非降級本體`：本章 L1-r4 依以上真實行區間及原域 Reader；無單獨 R4-BEGIN 增量不等於以歷史 r2 取代 L1。W1 契約下文僅是對該 L1 已定義原義的工程操作化。
- `W1 整合操作規格、已填契約與逐項 POS/NEG／FirstFail`：**Protected Original H1**：`L1:960–1010`（`L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`），L2 作者端路由 `L2:651`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W1…
- `A. 本章實質功能與不能壓平的原義`：Authority → Profile nine-axis safety veto → 原 PI-01..18：身份不變，OriginalID/Parent/NEG 可反查。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reade…
- `B. 本版已完成的章契約與工程操作`：| 契約欄 | 本版具體內容 |
- `C. Input → Producer → 原 Reader／Consumer → Output`：- **Input/Guard**：W0 three SPEC+Original SourceSet/Scope/AuthorityBinding/ProfileRequirement。
- `D. POS／NEG／FirstFail／HOLD／退出`：- **POS（期待）**：同 SourceSpan SHA 重導 RequirementAtom；九軸 veto 不可降低 safety。

### CH-14｜PD-01..10、RepoContext Currentness、Scope 與晚綁

**法位（原文）**：**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L1449–1520`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original PD / RepoContext Reader；L2-r4:L904。原 Domain Reader/Writer 不因本章轉移。

**原文位置**：r9 `CH-14`，25,362 bytes，sha256 `f2d798a1bd27a23fd56671f884537a88ecee9c5d5abbb3abaf25078b35d2d88a`（本版未刪原文，僅未重複搬運逐列證據）


**R6 當期實質操作（逐字）**

- **Source**：`W1-SKEL:L1782@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- **Input**：原 PD-01..10 及真 Git Root/HEAD/index/untracked/preimage。
- **Producer→原Reader／Consumer**：作者編設計、正式產物沿原Writer→原 SBL Repo／PD Reader。
- **Operation**：由原 Repo Probe 取得即時狀態再晚綁；fake caller HEAD 或 foreign root 一律拒收。
- **Output**：RepoContext／PD BindRequest，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。
- **POS**：exact WriteSet 路徑受界且 preimage 可比。
- **NEG**：HEAD 明文假值、junction/path traversal、git add -A。
- **Case／FirstFail**：`AUTHOR.W1.CH-14.POS/NEG/SEC`／`AUTHOR.W1.CH-14.SOURCE_OR_CONSUMER_NACK`；安全反例是本章跨原權限/Scope借據，由原邊界判，不是作者安全verdict。
- **Dependency／施工序**：先原Source/已知答案，後本章對應WP/36Edge的具名Receiver；本章無W1主責時只消費/typed handoff，不偷施工原主波。
- **Exit**：上述I/O和正反案例在正文可用；原域完成須原 SBL Repo／PD Reader真正接受本次受影body及適用Raw，本文不代簽。
- **HOLD／Resume**：相應HOLD見CH48，缺原ID/ABI/例外/Runner就只停該受護效果；補原Reader同scope ref後重綁受影輸出。合法READ/DRAFT持續。
- **Rollback**：漂移只重綁 PD 及其下游；不重寫 PI 原義。

**本章結構（原文節標題與首句）**

- `本版主責章實質契約｜CH-14`：**Input**：原 PI digest、目標 exact WriteSet、真 Repo root/HEAD/branch/index/dirty/untracked、ACL及逐檔 preimage。
- `R6 當期實質操作｜W1主責`：- **Source**：`W1-SKEL:L1782@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- `r4 當期受影修補（直接摘取 L1 r4 本章有效增量）`：
- `r4｜AUDIT r3 受影整合／覆蓋／取代（現行作者端規範）`：**Original RepoContext Late Binding（GJ02/DR025/DR048）**：Repo 必有當期 root/HEAD/branch/index/dirty/untracked、ACL、Exact WriteSet、Preimage SHA、Subject+SourceSHA+CandidateSHA；只有原 PIPD PD…
- `W1 整合操作規格、已填契約與逐項 POS/NEG／FirstFail`：**Protected Original H1**：`L1:1011–1060`（`L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`），L2 作者端路由 `L2:652`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W…
- `A. 本章實質功能與不能壓平的原義`：真 Git RepoContext 晚綁 PD-01..10，原範圍/HEAD/index/untracked/ACL/preimage 足夠才可接。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。
- `B. 本版已完成的章契約與工程操作`：| 契約欄 | 本版具體內容 |
- `C. Input → Producer → 原 Reader／Consumer → Output`：- **Input/Guard**：live repo_root/HEAD/branch/dirty/index/untracked、allowlisted WriteSet/Scope/Reader ABI。

### CH-16｜跨庫 Typed ABI、Producer→Consumer、Same Subject 交接

**法位（原文）**：**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L1616–1680`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original ABI Consumer；L2-r4:L906。原 Domain Reader/Writer 不因本章轉移。

**原文位置**：r9 `CH-16`，27,739 bytes，sha256 `90332e1c2981db5c67f29d56422c6819e0b6147b37f601518e0b16cd926687cd`（本版未刪原文，僅未重複搬運逐列證據）


**R6 當期實質操作（逐字）**

- **Source**：`W1-SKEL:L1895@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- **Input**：S1–S5 的同 Subject／scope／producer／version。
- **Producer→原Reader／Consumer**：作者編設計、正式產物沿原Writer→五個原 Seam Consumer。
- **Operation**：五條 seam 分別綁原 ABI/Receiver，查 ACK 與 NACK 的原 body；原版本未知不能自造有效 schema。
- **Output**：FiveSeamJoin 設計，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。
- **POS**：五個獨立 ACK 期待可分開拒收。
- **NEG**：跨 Candidate/Scope 借 Raw 或只畫空箭頭。
- **Case／FirstFail**：`AUTHOR.W1.CH-16.POS/NEG/SEC`／`AUTHOR.W1.CH-16.SOURCE_OR_CONSUMER_NACK`；安全反例是本章跨原權限/Scope借據，由原邊界判，不是作者安全verdict。
- **Dependency／施工序**：先原Source/已知答案，後本章對應WP/36Edge的具名Receiver；本章無W1主責時只消費/typed handoff，不偷施工原主波。
- **Exit**：上述I/O和正反案例在正文可用；原域完成須五個原 Seam Consumer真正接受本次受影body及適用Raw，本文不代簽。
- **HOLD／Resume**：相應HOLD見CH48，缺原ID/ABI/例外/Runner就只停該受護效果；補原Reader同scope ref後重綁受影輸出。合法READ/DRAFT持續。
- **Rollback**：失效該 seam 和真正受影下游。

**本章結構（原文節標題與首句）**

- `本版主責章實質契約｜CH-16`：**Input**：五 Seam 原身份、Producer/Consumer、原 schema $id/version、Subject/SourceSHA及 effect 所需 scope/Host/epoch。
- `R6 當期實質操作｜W1主責`：- **Source**：`W1-SKEL:L1895@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- `r4 當期原 Reader 鎖與非降級本體`：本章 L1-r4 依以上真實行區間及原域 Reader；無單獨 R4-BEGIN 增量不等於以歷史 r2 取代 L1。W1 契約下文僅是對該 L1 已定義原義的工程操作化。
- `W1 整合操作規格、已填契約與逐項 POS/NEG／FirstFail`：**Protected Original H1**：`L1:1121–1171`（`L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`），L2 作者端路由 `L2:654`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W…
- `A. 本章實質功能與不能壓平的原義`：五 Seam 以原 schema/version/Subject/Candidate/Scope/SourceSHA/Effect/Reader 作 typed 連接。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗…
- `B. 本版已完成的章契約與工程操作`：| 契約欄 | 本版具體內容 |
- `C. Input → Producer → 原 Reader／Consumer → Output`：- **Input/Guard**：W0 S1 payload + 每 Seam Receiver ABI/version/Reader capability。
- `D. POS／NEG／FirstFail／HOLD／退出`：- **POS（期待）**：同 Candidate 和 Scope 的原 Consumer 回顯或原 typed NACK。

### CH-17｜Fabric Policy／FAR／治理鏡像與 FHS 工程入口

**法位（原文）**：**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L1681–1741`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Fabric Policy Owner/Consumer；L2-r4:L907。原 Domain Reader/Writer 不因本章轉移。

**原文位置**：r9 `CH-17`，26,130 bytes，sha256 `870f23773c1a7d0f999d67005148795180fa2b8eabcda5dbef24415dd11e6f3b`（本版未刪原文，僅未重複搬運逐列證據）


**R6 當期實質操作（逐字）**

- **Source**：`W1-SKEL:L1989@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- **Input**：Fabric FHS-NAV/v2 與原 Policy／HGK consumer。
- **Producer→原Reader／Consumer**：作者編設計、正式產物沿原Writer→原 Fabric Policy Owner／HGK consumer。
- **Operation**：先導航六路由，再向原域取 source/stage/approve/active/loaded/consumed；鏡像非授權。
- **Output**：PolicyLoadedConsumerACK 期待，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。
- **POS**：六個狀態同 scope 分欄且 digest 相符。
- **NEG**：PR 或 Source 檔案當已載入 policy。
- **Case／FirstFail**：`AUTHOR.W1.CH-17.POS/NEG/SEC`／`AUTHOR.W1.CH-17.SOURCE_OR_CONSUMER_NACK`；安全反例是本章跨原權限/Scope借據，由原邊界判，不是作者安全verdict。
- **Dependency／施工序**：先原Source/已知答案，後本章對應WP/36Edge的具名Receiver；本章無W1主責時只消費/typed handoff，不偷施工原主波。
- **Exit**：上述I/O和正反案例在正文可用；原域完成須原 Fabric Policy Owner／HGK consumer真正接受本次受影body及適用Raw，本文不代簽。
- **HOLD／Resume**：相應HOLD見CH48，缺原ID/ABI/例外/Runner就只停該受護效果；補原Reader同scope ref後重綁受影輸出。合法READ/DRAFT持續。
- **Rollback**：原 Policy Owner 恢復 LastGood epoch。

**本章結構（原文節標題與首句）**

- `本版主責章實質契約｜CH-17`：**Input**：Fabric INTEGRATION/FHS 原入口與repository-map、原Policy source/epoch、FAR R0研究問題與read roots。
- `R6 當期實質操作｜W1主責`：- **Source**：`W1-SKEL:L1989@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- `r4 當期原 Reader 鎖與非降級本體`：本章 L1-r4 依以上真實行區間及原域 Reader；無單獨 R4-BEGIN 增量不等於以歷史 r2 取代 L1。W1 契約下文僅是對該 L1 已定義原義的工程操作化。
- `W1 整合操作規格、已填契約與逐項 POS/NEG／FirstFail`：**Protected Original H1**：`L1:1172–1218`（`L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`），L2 作者端路由 `L2:655`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W…
- `A. 本章實質功能與不能壓平的原義`：Fabric Source/Stage/OwnerApproval/ActiveEpoch/LoadedSHA/ConsumerACK 六階分離，FHS-NAV 只導航。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader …
- `B. 本版已完成的章契約與工程操作`：| 契約欄 | 本版具體內容 |
- `C. Input → Producer → 原 Reader／Consumer → Output`：- **Input/Guard**：Fabric Policy SourceSHA、Mirror4、原 Owner decision、active/loaded Consumer 認證。
- `D. POS／NEG／FirstFail／HOLD／退出`：- **POS（期待）**：同 epoch 的 Effective policy 與 consumer loaded 回顯。

### CH-18｜HG-KSEOS 唯一 Native Issuer／SharedSpine／WorkID／許可

**法位（原文）**：**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L1742–1822`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** HGK Original Issuer/SharedSpine；L2-r4:L908。原 Domain Reader/Writer 不因本章轉移。

**原文位置**：r9 `CH-18`，31,663 bytes，sha256 `4d921d593cdac140633ce436dacd7636e060d272a9aa41b8f1e94c0fbb764efe`（本版未刪原文，僅未重複搬運逐列證據）


**R6 當期實質操作（逐字）**

- **Source**：`W1-SKEL:L2087@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- **Input**：原 HGK WorkID/Issuer/SharedSpine／guard Raw。
- **Producer→原Reader／Consumer**：作者編設計、正式產物沿原Writer→原 HGK Issuer／Guard／World Reader。
- **Operation**：先保 W0 raw REFUSE；修 _live_epoch 後仍須核 SoD/arm/ACL/TTL/nonce，重取原 guard 全部結果。
- **Output**：IssuerReceiverBinding／GuardReadbackRequest，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。
- **POS**：同 WorkID/Scope 的原准入及 World 回應。
- **NEG**：只改 epoch 就填 ALLOW；影子 Issuer。
- **Case／FirstFail**：`AUTHOR.W1.CH-18.POS/NEG/SEC`／`AUTHOR.W1.CH-18.SOURCE_OR_CONSUMER_NACK`；安全反例是本章跨原權限/Scope借據，由原邊界判，不是作者安全verdict。
- **Dependency／施工序**：先原Source/已知答案，後本章對應WP/36Edge的具名Receiver；本章無W1主責時只消費/typed handoff，不偷施工原主波。
- **Exit**：上述I/O和正反案例在正文可用；原域完成須原 HGK Issuer／Guard／World Reader真正接受本次受影body及適用Raw，本文不代簽。
- **HOLD／Resume**：相應HOLD見CH48，缺原ID/ABI/例外/Runner就只停該受護效果；補原Reader同scope ref後重綁受影輸出。合法READ/DRAFT持續。
- **Rollback**：原域撤 permit／lease，UNKNOWN 先 reconcile。

**本章結構（原文節標題與首句）**

- `本版主責章實質契約｜CH-18`：**Input**：原 HGK WorkID/Issuer/SharedSpine/PLAN CAS、PolicyEpoch、各 effect intent 與 PermissionScope。
- `R6 當期實質操作｜W1主責`：- **Source**：`W1-SKEL:L2087@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- `r4 當期受影修補（直接摘取 L1 r4 本章有效增量）`：
- `r4｜AUDIT r3 受影整合／覆蓋／取代（現行作者端規範）`：**Single Human Owner ≠ single technical principal**：原 HGK Issuer/SharedSpine/WorkID、Fabric Policy、Protected Checker credentials 不可因一位人類 Owner 就共用同 OS token。Host 必驗 `SID, ACL, prin…
- `W1 整合操作規格、已填契約與逐項 POS/NEG／FirstFail`：**Protected Original H1**：`L1:1219–1277`（`L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`），L2 作者端路由 `L2:656`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W…
- `A. 本章實質功能與不能壓平的原義`：HGK 唯一 Registry／Issuer／WorkID／Lease／Permit；Maker/Checker 是分離技術主體。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。
- `B. 本版已完成的章契約與工程操作`：| 契約欄 | 本版具體內容 |
- `C. Input → Producer → 原 Reader／Consumer → Output`：- **Input/Guard**：原 registry ABI、Host/SID/ACL、Scope/PolicyEpoch/TTL/nonce，source identity。

### CH-19｜Hermes 三 Lane、模型路由、Profiles、ActualServed

**法位（原文）**：**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L1823–1901`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Hermes Original Host / Lane Reader；L2-r4:L909。原 Domain Reader/Writer 不因本章轉移。

**原文位置**：r9 `CH-19`，35,781 bytes，sha256 `48c3ab492dbacdd7b5999f47e62fe3fa9200d2fa7d1921df655abc3cb256fee1`（本版未刪原文，僅未重複搬運逐列證據）


**R6 當期實質操作（逐字）**

- **Source**：`W1-SKEL:L2193@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- **Input**：Hermes v0.23.1／三 lane assignment／ActualServed。
- **Producer→原Reader／Consumer**：作者編設計、正式產物沿原Writer→原 Hermes Host／HGK dispatcher Reader。
- **Operation**：分 Required、Selected、PromptDelivered、ActualServed、Usage、ToolResult；fallback 不改 primary，缺 Raw 不宣 served。
- **Output**：LaneServedEvidenceExpectation，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。
- **POS**：三 lane 各有自己 Request/Result/Usage。
- **NEG**：模型名、profile 或主模型選中即稱服務完成。
- **Case／FirstFail**：`AUTHOR.W1.CH-19.POS/NEG/SEC`／`AUTHOR.W1.CH-19.SOURCE_OR_CONSUMER_NACK`；安全反例是本章跨原權限/Scope借據，由原邊界判，不是作者安全verdict。
- **Dependency／施工序**：先原Source/已知答案，後本章對應WP/36Edge的具名Receiver；本章無W1主責時只消費/typed handoff，不偷施工原主波。
- **Exit**：上述I/O和正反案例在正文可用；原域完成須原 Hermes Host／HGK dispatcher Reader真正接受本次受影body及適用Raw，本文不代簽。
- **HOLD／Resume**：相應HOLD見CH48，缺原ID/ABI/例外/Runner就只停該受護效果；補原Reader同scope ref後重綁受影輸出。合法READ/DRAFT持續。
- **Rollback**：恢復同 Host LastGood profile；撤受影 token。

**本章結構（原文節標題與首句）**

- `本版主責章實質契約｜CH-19`：**Input**：Hermes v0.23.1 固定origin、Profiles、原 lane assignment/required arms、模型backend與使用回執。
- `R6 當期實質操作｜W1主責`：- **Source**：`W1-SKEL:L2193@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- `r4 當期受影修補（直接摘取 L1 r4 本章有效增量）`：
- `r4｜AUDIT r3 受影整合／覆蓋／取代（現行作者端規範）`：**Hermes v0.22.5 pinned baseline**：PLAN/EXECUTE/VERIFY_SECURITY 每 Lane 依原 Policy `required→selected→actual_served`，證 `profile_hash, process_PID, prompt_delivered, API_mode, reques…
- `W1 整合操作規格、已填契約與逐項 POS/NEG／FirstFail`：**Protected Original H1**：`L1:1278–1328`（`L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`），L2 作者端路由 `L2:657`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W…
- `A. 本章實質功能與不能壓平的原義`：Hermes v0.22.5 三 Lane 真模型調用需要 Required／Selected／Invoked／ActualServed 四欄。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。
- `B. 本版已完成的章契約與工程操作`：| 契約欄 | 本版具體內容 |
- `C. Input → Producer → 原 Reader／Consumer → Output`：- **Input/Guard**：profile_sha、fresh_pid、provider/model request、Original Lane raw、host version。

### CH-20｜Hermes Native Kanban／Delegation／Swarm／長任務編排

**法位（原文）**：**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L1902–1978`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Hermes Kanban/Delegation Reader；L2-r4:L910。原 Domain Reader/Writer 不因本章轉移。

**原文位置**：r9 `CH-20`，31,574 bytes，sha256 `fa543eca4738c110a1cc07316c1b5afc43909186687e64003b6369ca548745f3`（本版未刪原文，僅未重複搬運逐列證據）


**R6 當期實質操作（逐字）**

- **Source**：`W1-SKEL:L2306@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- **Input**：原 Hermes Kanban／delegate／create_swarm／task store。
- **Producer→原Reader／Consumer**：作者編設計、正式產物沿原Writer→原 Hermes Task/Runtime Reader。
- **Operation**：普通任務 Direct，獨立子任務才 Delegate，持久流程沿原 Kanban；有界 Swarm 不另建 queue。
- **Output**：WakeLeaseRuntimeBinding，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。
- **POS**：checkpoint/cursor/lease 恢復無重複 world effect。
- **NEG**：卡片 Done 代 world 完成或第二 TaskDB。
- **Case／FirstFail**：`AUTHOR.W1.CH-20.POS/NEG/SEC`／`AUTHOR.W1.CH-20.SOURCE_OR_CONSUMER_NACK`；安全反例是本章跨原權限/Scope借據，由原邊界判，不是作者安全verdict。
- **Dependency／施工序**：先原Source/已知答案，後本章對應WP/36Edge的具名Receiver；本章無W1主責時只消費/typed handoff，不偷施工原主波。
- **Exit**：上述I/O和正反案例在正文可用；原域完成須原 Hermes Task/Runtime Reader真正接受本次受影body及適用Raw，本文不代簽。
- **HOLD／Resume**：相應HOLD見CH48，缺原ID/ABI/例外/Runner就只停該受護效果；補原Reader同scope ref後重綁受影輸出。合法READ/DRAFT持續。
- **Rollback**：沿原 store resume，UNKNOWN 先 World 再 retry。

**本章結構（原文節標題與首句）**

- `本版主責章實質契約｜CH-20`：**Input**：bounded Goal、原HGK WorkID、Hermes原task store、scope/預算、依賴圖與checkpoint。
- `R6 當期實質操作｜W1主責`：- **Source**：`W1-SKEL:L2306@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- `r4 當期受影修補（直接摘取 L1 r4 本章有效增量）`：
- `r4｜AUDIT r3 受影整合／覆蓋／取代（現行作者端規範）`：**Kanban/Delegation/Swarm Use-before-Build**：按普通 Goal 的最小 FUO：直接答覆/READ→必要時 bounded delegation→長任務 Kanban→確實需要多 Role 協作才 Swarm；所有共享原 Hermes Queue/Lease/Journal/WorkID，非原本能力不足不另建 s…
- `W1 整合操作規格、已填契約與逐項 POS/NEG／FirstFail`：**Protected Original H1**：`L1:1329–1379`（`L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`），L2 作者端路由 `L2:658`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W…
- `A. 本章實質功能與不能壓平的原義`：Kanban／Delegation／Kanban Swarm／原 Runtime Job/Queue/Lease 不新造持久工作層。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。
- `B. 本版已完成的章契約與工程操作`：| 契約欄 | 本版具體內容 |
- `C. Input → Producer → 原 Reader／Consumer → Output`：- **Input/Guard**：既有 admitted WorkID、queue cursor、lease gen、checkpoint、allowed delegation profile。

### CH-22｜Native20：現役唯一原生核心與維護權

**法位（原文）**：**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L2048–2318`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Native Owner/Registry；L2-r4:L912。原 Domain Reader/Writer 不因本章轉移。

**原文位置**：r9 `CH-22`，204,949 bytes，sha256 `75b4bc07f8d37556d78c691280cc134cf84724c9b8f002eac13666a7a49bf973`（本版未刪原文，僅未重複搬運逐列證據）


**R6 當期實質操作（逐字）**

- **Source**：`W1-SKEL:L2423@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- **Input**：Native20 中本波20個 Slot 與本版一版 Occupant。
- **Producer→原Reader／Consumer**：作者編設計、正式產物沿原Writer→原 Technology／Host／Native Owner。
- **Operation**：按下方24槽專卡接原 Need，不替換 singleton；原 native component 用 readback，不假裝二進位安裝。
- **Output**：CapabilityOccupancyAndQualificationPlan，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。
- **POS**：同 Need 最多一 qualified active。
- **NEG**：第二 Issuer/Compiler/Queue/Checker/Publisher。
- **Case／FirstFail**：`AUTHOR.W1.CH-22.POS/NEG/SEC`／`AUTHOR.W1.CH-22.SOURCE_OR_CONSUMER_NACK`；安全反例是本章跨原權限/Scope借據，由原邊界判，不是作者安全verdict。
- **Dependency／施工序**：先原Source/已知答案，後本章對應WP/36Edge的具名Receiver；本章無W1主責時只消費/typed handoff，不偷施工原主波。
- **Exit**：上述I/O和正反案例在正文可用；原域完成須原 Technology／Host／Native Owner真正接受本次受影body及適用Raw，本文不代簽。
- **HOLD／Resume**：相應HOLD見CH48，缺原ID/ABI/例外/Runner就只停該受護效果；補原Reader同scope ref後重綁受影輸出。合法READ/DRAFT持續。
- **Rollback**：Owner 受界回 epoch/ABI，未知世界先查。

**本章結構（原文節標題與首句）**

- `本版主責章實質契約｜CH-22`：**Input**：485原槽台帳、24本波槽、各原Need/OriginalDisposition、Kind/Host/Effect及工具已選版本。
- `R6 當期實質操作｜W1主責`：- **Source**：`W1-SKEL:L2423@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- `08.23｜Default30：30項獨立功能`：<!-- R6:SLOT:Native20:SBL.PRODUCT:END -->
- `08.24｜Donor24：24項獨立功能`：<!-- R6:SLOT:Default30:P0-TOOL-072:END -->
- `r4 當期受影修補（直接摘取 L1 r4 本章有效增量）`：
- `r4｜AUDIT r3 受影整合／覆蓋／取代（現行作者端規範）`：**五正交集合不變**：Native20/Default30/Donor24/Method25/TECH386 是五種不同的原資產身分，485 只是 20+30+24+25+386 的來源卡數，不是 485 件必裝工具／同一驗收分母。每個實際 Need 需先讀原佔位義務和原 Capability；NoFit 只停該需求，不可把缺 License 的 TOO…
- `W1 整合操作規格、已填契約與逐項 POS/NEG／FirstFail`：**Protected Original H1**：`L1:1427–1675`（`L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`），L2 作者端路由 `L2:660`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader，W…
- `A. 本章實質功能與不能壓平的原義`：Native20 全部原身份不失、真 Singleton/RoleWorker/Method 格式不可混裝。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。

### CH-34｜Portable Commander Guide A／B／C 與原 Native PLAN

**法位（原文）**：**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L26233–26296`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Native PLAN Producer；L2-r4:L924。原 Domain Reader/Writer 不因本章轉移。

**原文位置**：r9 `CH-34`，24,865 bytes，sha256 `9730802ddc78e9e88d409320dcef1818336f5cf8c81ee9b37f4bd6e1de3c3667`（本版未刪原文，僅未重複搬運逐列證據）


**R6 當期實質操作（逐字）**

- **Source**：`W1-SKEL:L2675@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- **Input**：Guide A/B/C、同WorkID與base_revision。
- **Producer→原Reader／Consumer**：作者編設計、正式產物沿原Writer→原 HGK PLAN CAS Reader。
- **Operation**：依原Guide適用動作提出PLAN candidate；原Native Receiver CAS決定，衝突先讀最新再提受影差額。
- **Output**：NativePlanCASProposal，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。
- **POS**：同base_revision原ACK或typed NACK。
- **NEG**：disabled Commander重開第二Gate或overwrite PLAN。
- **Case／FirstFail**：`AUTHOR.W1.CH-34.POS/NEG/SEC`／`AUTHOR.W1.CH-34.SOURCE_OR_CONSUMER_NACK`；安全反例是本章跨原權限/Scope借據，由原邊界判，不是作者安全verdict。
- **Dependency／施工序**：先原Source/已知答案，後本章對應WP/36Edge的具名Receiver；本章無W1主責時只消費/typed handoff，不偷施工原主波。
- **Exit**：上述I/O和正反案例在正文可用；原域完成須原 HGK PLAN CAS Reader真正接受本次受影body及適用Raw，本文不代簽。
- **HOLD／Resume**：相應HOLD見CH48，缺原ID/ABI/例外/Runner就只停該受護效果；補原Reader同scope ref後重綁受影輸出。合法READ/DRAFT持續。
- **Rollback**：保留proposal歷史，原revision補償。

**本章結構（原文節標題與首句）**

- `本版主責章實質契約｜CH-34`：**Input**：Commander Guide A/B/C、原Native PLAN/ExpectedRevision、Goal/三SPEC及各 effect decision。
- `R6 當期實質操作｜W1主責`：- **Source**：`W1-SKEL:L2675@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- `r4 當期原 Reader 鎖與非降級本體`：本章 L1-r4 依以上真實行區間及原域 Reader；無單獨 R4-BEGIN 增量不等於以歷史 r2 取代 L1。W1 契約下文僅是對該 L1 已定義原義的工程操作化。
- `W1 整合操作規格、已填契約與逐項 POS/NEG／FirstFail`：**Protected Original H1**：`L1:25394–25443`（`L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`），L2 作者端路由 `L2:672`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader…
- `A. 本章實質功能與不能壓平的原義`：Portable Commander Guide A/B/C：A readonly、B isolated proposal、C original PLAN CAS。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另…
- `B. 本版已完成的章契約與工程操作`：| 契約欄 | 本版具體內容 |
- `C. Input → Producer → 原 Reader／Consumer → Output`：- **Input/Guard**：Goal+KnownAnswer+W0 three SPEC+original CurrentRevisionReader/base_revision。
- `D. POS／NEG／FirstFail／HOLD／退出`：- **POS（期待）**：不用未建立的 WorkOrder 也能先給 source-bound plan proposal。

### CH-39｜安全：SoD、Process ACL、秘鑰、原授權、Consent/Privacy

**法位（原文）**：**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L27080–27152`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original Security/Consent Owner；L2-r4:L929。原 Domain Reader/Writer 不因本章轉移。

**原文位置**：r9 `CH-39`，27,605 bytes，sha256 `803c486ec5704ee7e9fe681c11d1f1aa09c7f38cec7690ba3e9ed5b020e192ce`（本版未刪原文，僅未重複搬運逐列證據）


**R6 當期實質操作（逐字）**

- **Source**：`W1-SKEL:L2816@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- **Input**：Maker/Checker/Issuer/Publisher真principal及ACL。
- **Producer→原Reader／Consumer**：作者編設計、正式產物沿原Writer→原 Protected Checker／Issuer／OS ACL Reader。
- **Operation**：同一Human Owner不等同同一技術principal；維護與運行分權，測跨PID/nonce/TTL/撤權/credential；不讀秘密。
- **Output**：SecurityBoundaryPlan，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。
- **POS**：不可由Maker取得Checker credential，拒例真由原邊界判。
- **NEG**：兩persona或Profile冒OS隔離；作者自簽。
- **Case／FirstFail**：`AUTHOR.W1.CH-39.POS/NEG/SEC`／`AUTHOR.W1.CH-39.SOURCE_OR_CONSUMER_NACK`；安全反例是本章跨原權限/Scope借據，由原邊界判，不是作者安全verdict。
- **Dependency／施工序**：先原Source/已知答案，後本章對應WP/36Edge的具名Receiver；本章無W1主責時只消費/typed handoff，不偷施工原主波。
- **Exit**：上述I/O和正反案例在正文可用；原域完成須原 Protected Checker／Issuer／OS ACL Reader真正接受本次受影body及適用Raw，本文不代簽。
- **HOLD／Resume**：相應HOLD見CH48，缺原ID/ABI/例外/Runner就只停該受護效果；補原Reader同scope ref後重綁受影輸出。合法READ/DRAFT持續。
- **Rollback**：原Broker撤權隔離受影進程，World reconcile。

**本章結構（原文節標題與首句）**

- `本版主責章實質契約｜CH-39`：**Input**：逐effect權限、OS Principal/ACL、source taint、secret/Consent資料scope、凍結case與原Checker責任。
- `R6 當期實質操作｜W1主責`：- **Source**：`W1-SKEL:L2816@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- `r4 當期受影修補（直接摘取 L1 r4 本章有效增量）`：
- `r4｜AUDIT r3 受影整合／覆蓋／取代（現行作者端規範）`：**Protected Checker 技術獨立性**：同一 Human Owner 的操作便利不等於 Maker/Checker 共享唯一 Credentials；每受影 Case 需原 `Subject/Candidate/SourceSHA/Scope/Host/PolicyEpoch`、Frozen Raw、independent checker …
- `W1 整合操作規格、已填契約與逐項 POS/NEG／FirstFail`：**Protected Original H1**：`L1:26052–26102`（`L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`），L2 作者端路由 `L2:677`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader…
- `A. 本章實質功能與不能壓平的原義`：SoD、SID/ACL、Secret、User Consent 與 effect-specific permission 各自嚴守。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。
- `B. 本版已完成的章契約與工程操作`：| 契約欄 | 本版具體內容 |
- `C. Input → Producer → 原 Reader／Consumer → Output`：- **Input/Guard**：原 maker/checker principal、HostID/SID、TTL、Scopes、Consent / privacy tags。

### CH-40｜三 SPEC／PI／PD／ECP／TQAEP 對原 Reader 的交接矩陣

**法位（原文）**：**唯一主波** `W1`｜**本波法位** `W1_PRIMARY_SUBSTANTIVE`｜**當期上位章位** `L1-r4:L27153–27225`，SHA-256 `cbdd75fd609b5353cd9bd4893feffa19a68389300869091c618239ef2cabdf5b`｜**原 Consumer 路由** Original PIPD + affected Host Receiver；L2-r4:L930。原 Domain Reader/Writer 不因本章轉移。

**原文位置**：r9 `CH-40`，182,754 bytes，sha256 `4757121fda1cbbb74af945a7e9b1c10da4c4e7f0f749ea7e958a3ee95701eade`（本版未刪原文，僅未重複搬運逐列證據）


**R6 當期實質操作（逐字）**

- **Source**：`W1-SKEL:L2917@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- **Input**：三SPEC、PI/PD/ECP/TQAEP及五seam對原Consumer。
- **Producer→原Reader／Consumer**：作者編設計、正式產物沿原Writer→原 SPEC／PIPD／Native各Receiver。
- **Operation**：按正文handoff矩陣逐產物指定Producer/Reader/typed NACK；未綁原版本/$id用HOLD不是作者新ABI。
- **Output**：SourceBoundPipdHandoffDesign，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。
- **POS**：每種產物有自己Consumer及同scope回應期待。
- **NEG**：截斷Receiver清單或借別的candidate receipt。
- **Case／FirstFail**：`AUTHOR.W1.CH-40.POS/NEG/SEC`／`AUTHOR.W1.CH-40.SOURCE_OR_CONSUMER_NACK`；安全反例是本章跨原權限/Scope借據，由原邊界判，不是作者安全verdict。
- **Dependency／施工序**：先原Source/已知答案，後本章對應WP/36Edge的具名Receiver；本章無W1主責時只消費/typed handoff，不偷施工原主波。
- **Exit**：上述I/O和正反案例在正文可用；原域完成須原 SPEC／PIPD／Native各Receiver真正接受本次受影body及適用Raw，本文不代簽。
- **HOLD／Resume**：相應HOLD見CH48，缺原ID/ABI/例外/Runner就只停該受護效果；補原Reader同scope ref後重綁受影輸出。合法READ/DRAFT持續。
- **Rollback**：撤受影交接候選，其他合法READ/DRAFT續行。

**本章結構（原文節標題與首句）**

- `本版主責章實質契約｜CH-40`：**Input**：三SPEC、24DesignID/57子義、原13CLI/19family/8skill、原Case/Oracle/Runner與逐effect ECP意圖。
- `R6 當期實質操作｜W1主責`：- **Source**：`W1-SKEL:L2917@6b60f9f64cfb8589ae4a572cce724be07f57a2a8eca0996e0ad66ebf80ee86fb`；當期L0/L1/L2/SPEC/CH50共同約束，原冊逐行證據另見附錄，原Domain仍有權。
- `r4 當期原 Reader 鎖與非降級本體`：本章 L1-r4 依以上真實行區間及原域 Reader；無單獨 R4-BEGIN 增量不等於以歷史 r2 取代 L1。W1 契約下文僅是對該 L1 已定義原義的工程操作化。
- `W1 整合操作規格、已填契約與逐項 POS/NEG／FirstFail`：**Protected Original H1**：`L1:26103–26161`（`L1_SHA=bfbf9490125b2e3983e5f90fda8b5ad9e9bf676f932924114da6970d96aad6fa`），L2 作者端路由 `L2:678`；**Primary wave**＝`W1`；本章仍指向原各 Domain Reader…
- `A. 本章實質功能與不能壓平的原義`：三 SPEC→PI→PD→ECP→TQAEP 五 Seam 逐出口、原 Writer/Consumer/ACK-NACK 閉環。保全原 Source/OriginalID/Parent/否定作用域、版本及 Receiver 的獨立性；輸出由 W1 **作者端受界設計** 說明，真正 Original Reader 驗收另行執行。
- `B. 本版已完成的章契約與工程操作`：| 契約欄 | 本版具體內容 |
- `C. Input → Producer → 原 Reader／Consumer → Output`：- **Input/Guard**：W0 three distinct specs+Original IDs、SourceSHA、PI、true RepoContext、EffectClass、original Case registry。
- `D. POS／NEG／FirstFail／HOLD／退出`：- **POS（期待）**：同 Subject/Scope/SourceSHA 的原 Receiver response 和 POS/NEG fixture。

### C.2 37 章非主責（原義保留＋typed handoff）

以下每章給：法位、Input→Output、POS/NEG、Consumer/Exit、HOLD 接點。完整原文仍在 r9 對應章（SHA 可回查），本版未刪。

| 章 | 標題 | 主波／法位 | I→O | POS／NEG | 原 Consumer | Exit／HOLD |
|---|---|---|---|---|---|---|
| CH-00 | 正式入口、主體法位、不可降級 H1 規則 | W0／CROSS_WAVE_READ_ONLY_HANDOFF | L0/AXIS/CH50 與本版版本及 Subject。 → ChapterRoute＋ClaimCeiling，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 原章序與原名皆可反查。 ／ 用全域摘要刪去受保護 H1。 | L3 Pack Curator；L2-r4:L890。原 Domain Reader/Writer… | 上述I/O和正反案例在正文可用；原域完成須原 Domain Reader／L0 Owner真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-01 | FHS 產品定位、Owner／JTBD／FUO 和非目標 | W0／CROSS_WAVE_READ_ONLY_HANDOFF | 唯一 Owner、普通 B Goal 及 A 建置旅程。 → ProductSuccess＋FUO 分層，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 普通 Goal 不被五波工程強迫阻塞。 ／ 每個 Goal 強跑三 lane／22 WP。 | SBL Product/Owner；L2-r4:L891。原 Domain Reader/Writ… | 上述I/O和正反案例在正文可用；原域完成須Human Owner／原 Product Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-02 | 七大痛點、原始動機與逐產品旅程 | W0／CROSS_WAVE_READ_ONLY_HANDOFF | 七痛點及來源來源語句。 → Pain→Journey→Acceptance，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 七個痛點各有產品退出條件。 ／ 有報表就稱普通使用者任務完成。 | SBL Product/Owner；L2-r4:L892。原 Domain Reader/Writ… | 上述I/O和正反案例在正文可用；原域完成須原產品 Owner／各 Journey Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-03 | 功能需求、OriginalID、強弱語義及完整不變量 | W0／CROSS_WAVE_READ_ONLY_HANDOFF | 24 原 DesignID、57 子要求、7 VN 增量。 → OriginalID/Parent/NEG crosswalk，帶source/原ID/極性/必要Scope與同scope evidence期待或typed … | 每一原子有 POS/NEG/Consumer。 ／ 把 24 父要求和 57 子項加成同一完成分母。 | Original Requirement Reader；L2-r4:L893。原 Domain R… | 上述I/O和正反案例在正文可用；原域完成須原 Requirement／Case Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-04 | 31 冊 SourceFreeze、AuthorityBinding、Curr… | W0／CROSS_WAVE_READ_ONLY_HANDOFF | 31 冊版本、來源 SHA、權威衝突。 → SourceFreeze／AuthorityBinding 設計，帶source/原ID/極性/必要Scope與同scope evidence期待或typed… | 每來源保原路徑、SHA、衝突去向。 ／ 鏡像或 PR 當生效原權威。 | Original Source Authority Reader；L2-r4:L894。原 Dom… | 上述I/O和正反案例在正文可用；原域完成須原 Authority/Profile Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-05 | U0 全位元組內容盤點：表格、負條件、Code、原版附錄 | W0／CROSS_WAVE_READ_ONLY_HANDOFF | 原表格、否定句、code、原附錄與完整標頭索引。 → ContentInventory 與未選取條位清單，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 正文、附錄與 code 都有內容路由。 ／ 只讀 Markdown heading 就說全 bytes 語義已接受。 | Original Corpus Reader；L2-r4:L895。原 Domain Reader… | 上述I/O和正反案例在正文可用；原域完成須原 U0 Reader／R43真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-06 | U1 子要求逐義拆解：各有／分別／對應／若／不得 | W0／CROSS_WAVE_READ_ONLY_HANDOFF | 各有／分別／對應／若／除非／不得句。 → AtomicRequirement 分解設計，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 正反語義各自對回 parent。 ／ 把四 Host 的一個 PASS 當四個結果。 | Original Requirement Atom Reader；L2-r4:L896。原 Dom… | 上述I/O和正反案例在正文可用；原域完成須原 U1／Requirement Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-07 | U2–U4 Crosswalk、版本去向、Owner 語義核簽與反例 | W0／CROSS_WAVE_READ_ONLY_HANDOFF | source→條文→WP→Case→Consumer 的雙向關係。 → ReplacementCrosswalk／OwnerSelectionHold，帶source/原ID/極性/必要Scope與同scope evidence期… | 任何來源和條款均可反向找到原句或具名 HOLD。 ／ 自檢 PASS 代 Owner ratification。 | Original Domain Owner + Trace Reader；L2-r4:L897。原… | 上述I/O和正反案例在正文可用；原域完成須原 U2–U4／語義 Owner真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-09 | 八 Kind、三 Mode、四 Host、16 Moments、38 Deli… | W3／CROSS_WAVE_READ_ONLY_HANDOFF | 八 Kind、三 Mode、四 Host、16 Moments、38 Surfaces 原身份。 → ProductDimensionHandoff，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 適用與不適用理由逐原 ID 可追。 ／ 只報數量、自己猜 Kind 名補足分母。 | Original Kind/Mode/Host Product Reader；L2-r4:L899… | 上述I/O和正反案例在正文可用；原域完成須原 Kind／Host／Moment／Surface Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-10 | 已知答案、Source-bound 檢索、FAR／知識服務 | W0／CROSS_WAVE_READ_ONLY_HANDOFF | KnownAnswer、Source refs、FAR R0–R2/R8 及 FDA 原服務。 → KnownAnswer／TypedFinding，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 研究答案帶來源與時效，R8 ACK 另列。 ／ FTS/GET 成功等同 Policy Applied。 | FAR/G-KNOW Consumer；L2-r4:L900。原 Domain Reader/Wr… | 上述I/O和正反案例在正文可用；原域完成須原 FAR／FDA／Policy Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-11 | TPM 三 SPEC：Product、Architecture、Program… | W0／CROSS_WAVE_READ_ONLY_HANDOFF | Product、Architecture、Program 各自 SPEC 與 18 stage。 → 三個不同 SPEC 設計＋StageReferral，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 三 SPEC 不同 Consumer／ACC 且共同 Goal。 ／ 同文改三個標題或將 DESIGN_PROJECTION 當 formal。 | SBL TPM/PIPD Intake；L2-r4:L901。原 Domain Reader/Wr… | 上述I/O和正反案例在正文可用；原域完成須原 SPEC／PIPD Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-15 | ConstructionContract／ECP：DEV、OPS、USER、R… | W2／CROSS_WAVE_READ_ONLY_HANDOFF | PD、原 Operation Registry、DEV/OPS/USER/RELEASE。 → ConstructionContract／ECP 候選期待，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HO… | 六 effect 的 guard 和 recovery 各別。 ／ DEV grant 用於 OPS 或 ECP 文件當 Permit。 | Original ECP Writer / HGK effect receiver；L2-r4:L… | 上述I/O和正反案例在正文可用；原域完成須原 ECP／Operation／Issuer Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-21 | Windows Host／CLI／Plugin／Skill：安裝與實際載入三段… | W3／CROSS_WAVE_READ_ONLY_HANDOFF | 四 Host 原 loader、版本、權限、trigger/nontrigger。 → HostSPQualificationPlan，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 每個 pair 自己有 source/pin/Raw。 ／ Hermes 證據借給 Codex/Claude/ChatGPT。 | Original Host Install/Loader Reader；L2-r4:L911。原 … | 上述I/O和正反案例在正文可用；原域完成須各原 Host Loader／Product Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-23 | Default30：默認能力、可配置佔用與 NoFit | W3／CROSS_WAVE_READ_ONLY_HANDOFF | Default30 中本波4個 Slot、原 Disposition。 → DefaultSlotQualification，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 原 default 處置及 NoFit 理由保留。 ／ 未安裝就將 Default 改 DEFER/Optional。 | Default Capability/Host Owner；L2-r4:L913。原 Domain… | 上述I/O和正反案例在正文可用；原域完成須原 Capability／Host Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-24 | Donor24：可借用外部輪子與授權條件 | W3／CROSS_WAVE_READ_ONLY_HANDOFF | Donor24 原 ID、來源與授權條件。 → DonorExtractionDesign，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 提取有原條文與 permission，未抽取不冒無影響。 ／ fork／copy 全 donor 然後稱可分發。 | Donor License/Host Owner；L2-r4:L914。原 Domain Read… | 上述I/O和正反案例在正文可用；原域完成須原 Donor／License／Owner Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-25 | Method25：演算法／流程工具方法的原用途 | W3／CROSS_WAVE_READ_ONLY_HANDOFF | Method25 原用途及 W0 WP16 輸出。 → MethodOutput／原 Case Referral，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOL… | 方法的 POS/NEG 有原 Consumer。 ／ 流程方法必須偽造 Installed receipt 才能用。 | Method Consumer；L2-r4:L915。原 Domain Reader/Writer… | 上述I/O和正反案例在正文可用；原域完成須原 Method／Technology Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-26 | TECH386：逐原 ID 技術功能與非降級 Disposition | W3／CROSS_WAVE_READ_ONLY_HANDOFF | TECH386 原鍵／Disposition／485 exact-key 集合。 → AffectedTechSlice／ExactKeyReferral，帶source/原ID/極性/必要Scope與同scope evidence期待或typ… | 20/30/24/25/386 身份集合各自保存。 ／ 485個全部當安裝任務或合併不同原鍵。 | Tech Need/License/Host Owner；L2-r4:L916。原 Domain … | 上述I/O和正反案例在正文可用；原域完成須原 Technology／Owner Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-27 | SBL 50 Parent／149 Child：原生產品分母專章 | W3／CROSS_WAVE_READ_ONLY_HANDOFF | SBL 50 Parent／149 Child 原產品分母。 → ProductFunctionHandoff，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 父子及獨立 NEG 可追。 ／ 只驗24個W1ID就稱50/149全產品完成。 | SBL Product Parent/Child Reader；L2-r4:L917。原 Doma… | 上述I/O和正反案例在正文可用；原域完成須原 SBL Product／Case Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-28 | R15 949 原產品原子與 B1 66／254／629 映射 | W3／CROSS_WAVE_READ_ONLY_HANDOFF | R15 949 原子與 B1 66/254/629 映射。 → OriginalAtomCrosswalkReferral，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HO… | 每層原ID和mapping可獨立查。 ／ 949數量等於949原義已接受。 | SBL Full Product R15 Reader；L2-r4:L918。原 Domain R… | 上述I/O和正反案例在正文可用；原域完成須原 R15／B1 Product Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-29 | Kind×Mode×Host×LegacyToken 192 Cell 的原始… | W3／CROSS_WAVE_READ_ONLY_HANDOFF | 8×3×4×2 的192原Cell與 applicability。 → ProductCellApplicabilityHandoff，帶source/原ID/極性/必要Scope與同scope evidence期待或typed … | 原 Cell 同 Host/Mode/LegacyToken 原義不丟。 ／ 16格例子或12Host-SP冒192全部通過。 | Original Host Cell Reader；L2-r4:L919。原 Domain Rea… | 上述I/O和正反案例在正文可用；原域完成須原 SBL Cell Reader／W3 WP10真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-30 | Original 96 Oracle：Test Class×Oracle 的型… | W3／CROSS_WAVE_READ_ONLY_HANDOFF | Original96 Oracle 計畫及原 TestClass/Oracle 身份。 → OracleReferral／TQAEP plan，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 測試class與oracle分別綁且具NEG。 ／ 96列計畫等於96個獨立PASS。 | Original Assurance Oracle Reader；L2-r4:L920。原 Dom… | 上述I/O和正反案例在正文可用；原域完成須原 Oracle96／Case Runner真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-31 | Acceptance Challenge 15 條異構 Sender→Rece… | W2／CROSS_WAVE_READ_ONLY_HANDOFF | Acceptance Challenge 原15條異構Sender→Receiver。 → AC15EdgeReferral，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 異構語義與正反方向分開。 ／ 15條箭頭只有同一假Reader。 | Original Challenge/Protected Checker；L2-r4:L921。原… | 上述I/O和正反案例在正文可用；原域完成須原 AC15 Sender／Receiver Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-32 | B1 120 Parent／124 Child／38 Node＝282 Cas… | W3／CROSS_WAVE_READ_ONLY_HANDOFF | B1 120 Parent/124 Child/38 Node＝282 Case。 → B1CaseReferral，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 三層282身份不混為generic checklist。 ／ 用282檔案或CLI --help充282Case。 | Original B1 CaseRunner Reader；L2-r4:L922。原 Domain… | 上述I/O和正反案例在正文可用；原域完成須原 B1 Case／Protected Checker真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-33 | B1 原 27 PI→31 PD Slot：拓撲與 Effect ECP | W3／CROSS_WAVE_READ_ONLY_HANDOFF | 原27PI→31PD slot／type／effect。 → PItoPDTopologyReferral，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 31出口有原parent/type/effect。 ／ 靠27總數宣31拓撲完整。 | Original PI/PD Slot Reader；L2-r4:L923。原 Domain Re… | 上述I/O和正反案例在正文可用；原域完成須原 B1 PI／PD／Effect Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-35 | FHS-EXECUTE：Lease、Journal、UNKNOWN、World… | W2／CROSS_WAVE_READ_ONLY_HANDOFF | Lease/journal/cursor、effect key與World結果。 → ExecutionRecoveryReferral，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 同key不重複effect且journal可恢復。 ／ retry當成補償、UNKNOWN直接重播。 | Original HGK reducer/world reader；L2-r4:L925。原 Do… | 上述I/O和正反案例在正文可用；原域完成須原 HGK Worker／World Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-36 | B1 自舉與 W18：Fresh PID 普通 Goal 的第一成果 | W3／CROSS_WAVE_READ_ONLY_HANDOFF | B1自舉／W18 fresh PID 普通Goal與原home。 → FreshPIDGoalReferral，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | fresh PID與實際Goal結果相連。 ／ 自己做的文件或舊FIRST_FUO冒新Goal完成。 | Hermes normal-mode Host Consumer；L2-r4:L926。原 Dom… | 上述I/O和正反案例在正文可用；原域完成須原 B1／Host／World Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-37 | Program SPEC：W0～W3、原 22 WP／36 DAG 邊及 W0… | W0／CROSS_WAVE_READ_ONLY_HANDOFF | 22 WP／36 Edge／五波主責。 → ProgramDAG／TypedEdgeHandoff，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 精確邊集合且無cycle，W0-A/B不變。 ／ 倒置17/06或加15→05硬依賴。 | Original Program/WP Reader；L2-r4:L927。原 Domain Re… | 上述I/O和正反案例在正文可用；原域完成須原 Program／Dependency Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-38 | 最小 Native E2E、GJ01–03、Golden/V2-T 與停止規則 | W2／CROSS_WAVE_READ_ONLY_HANDOFF | GJ01–03／Golden／V2-T 與最小Native E2E。 → MinimalE2EReferral，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | Source→Work→Tool→World同scope閉合。 ／ 全部gate全時強制或plan自簽PASS。 | Original E2E/Golden Reader；L2-r4:L928。原 Domain Re… | 上述I/O和正反案例在正文可用；原域完成須原 Golden／World／Protected Checker真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-41 | TQAEP：POS／NEG／FirstFail／獨立 Oracle 的可執行計畫 | W2／CROSS_WAVE_READ_ONLY_HANDOFF | PI/ECP、原Case/Oracle與獨立Checker referral。 → TQAEPPlan／EvidenceExpectation，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HO… | 正例、業務反例、安全反例獨立。 ／ 偽Checker回執或schema valid等於Case通過。 | Original Oracle/Protected Checker；L2-r4:L931。原 Do… | 上述I/O和正反案例在正文可用；原域完成須原 TQAEP／Protected Checker真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-42 | 來源／要求／Case／Evidence／Delivery LEDGER：一筆一… | W0／CROSS_WAVE_READ_ONLY_HANDOFF | source／requirement／Case／evidence／delivery refs。 → TraceClosureDesign，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 同ID去向唯一且反向可查。 ／ 第二ledger改寫原源狀態或掉NEG。 | Original Evidence Ledger/Reader；L2-r4:L932。原 Doma… | 上述I/O和正反案例在正文可用；原域完成須原 Trace／Ledger Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-43 | ClaimCeiling、測量層、Producer/Checker/Publi… | W4／CROSS_WAVE_READ_ONLY_HANDOFF | SOURCE_READ／DRAFT／Host／Native／Independent／Release層。 → ClaimCeiling／EvidenceExpectation，帶source/原ID/極性/必要Scope與同scope evidence期待或typed… | 每一claim有同scope證據或具名HOLD。 ／ 作者靜態PASS冒Native/Independent/Release。 | Original ClaimCeiling Owner；L2-r4:L933。原 Domain R… | 上述I/O和正反案例在正文可用；原域完成須原 Checker／Publisher真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-44 | CI、供應鏈、部署、Cutover、Rollback 的原服務區分 | W4／CROSS_WAVE_READ_ONLY_HANDOFF | 原CI workflow、supply-chain、deploy/cutover/rollback。 → DeploymentReferral／原RollbackPlan，帶source/原ID/極性/必要Scope與同scope evidence期待或typed… | readback、rollback與原permission分別綁。 ／ PR綠燈或ZIP可解壓冒產品發行。 | Original Publisher/SupplyChain Owner；L2-r4:L934。原… | 上述I/O和正反案例在正文可用；原域完成須原 CI／Deployment／Publisher真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-45 | L0–L3 文件包、DELIVER、原 Consumer ACK 與長期可維護性 | W4／CROSS_WAVE_READ_ONLY_HANDOFF | L0–L3文件包、版本、DELIVER與Consumer ACK。 → VersionedDocumentHandoff，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 文件能讀回、來源可追、原ACK未混淆。 ／ ZIP完整就稱Semantic Replacement Accepted。 | FHS L3 Curator + Original Domain Owner；L2-r4:L935… | 上述I/O和正反案例在正文可用；原域完成須原文件Consumer／L3 Owner真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-46 | 成本／FinOps／KnownAnswer 復用及三種 Dogfood Loop | W3／CROSS_WAVE_READ_ONLY_HANDOFF | 成本／known-answer／三Dogfood Loop／長任務預算。 → BudgetedGoalReferral，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 成本可定位request，fuo而非文件數衡量。 ／ 全任務強跑Swarm或以模型同名推成本。 | Product FinOps/Dogfood Owner；L2-r4:L936。原 Domain … | 上述I/O和正反案例在正文可用；原域完成須原 Owner／Runtime／FinOps Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-47 | OpenSpec、gstack、Hermes 外部研究與 Build-or-U… | W3／CROSS_WAVE_READ_ONLY_HANDOFF | Hermes/OpenSpec/gstack確定pin與上游license/support。 → ToolAdoptionDecision，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOLD。 | 一版選定有license及NoFit/HotSwap規則。 ／ 只留候選待決、用README推已安裝。 | Original Tech/License/Host Reader；L2-r4:L937。原 Do… | 上述I/O和正反案例在正文可用；原域完成須原 Technology／License／Host Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-48 | 受界 ChangeSet、風險／具名 HOLD、Stop-Resume 與決策… | W0／CROSS_WAVE_READ_ONLY_HANDOFF | Risk/HOLD、exact ChangeSet與前像。 → AffectedChangeSet／ResumePlan，帶source/原ID/極性/必要Scope與同scope evidence期待或typed HOL… | 只停必要effect，非受影READ/DRAFT繼續。 ／ 所有HOLD都全域卡死或預授權無限未來。 | Affected Original Owner/FirstFail Reader；L2-r4:L9… | 上述I/O和正反案例在正文可用；原域完成須原 Scope／Repo／Host Reader真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |
| CH-49 | 逐章正式驗收標準、H1 防壓平測試與裁決 | W4／CROSS_WAVE_READ_ONLY_HANDOFF | 50H1、24DO/57sub/24Slot、13/19/8、22/36與正文輸出。 → AuthorStaticCheck／DeliveryReadback，帶source/原ID/極性/必要Scope與同scope evidence期待或typ… | 結構/集合/trace/互鏈/CRC可重算。 ／ 檢查器只掃保全舊文命中就當r6正文完整。 | Original Checker/Publisher (as affected)；L2-r4:L9… | 上述I/O和正反案例在正文可用；原域完成須Human Owner／原各Reader後續接手真正接受本次受影body及適用Raw，本文不代簽。；HOLD→§E.4 |

---

## D｜受保護分母、485 五集合、Repo 與選型

### D.1 受保護分母（原 ID 全部保留，不以數量代逐項）

| 分母 | 數量 | 本波處置 | 原 Consumer／HOLD |
|---|---|---|---|
| CH 章 | 50 | 13 主責實質、37 消費／handoff | 原章 Consumer 不變 |
| W1 主責章 | 13 | 逐章 12 欄契約（§C.1） | 原 Domain Reader |
| WP | 8（W1）／22（全域） | §B3 輪次施工 | 原 WP Owner |
| Edge | 36 | 逐 edge typed payload 與 FirstFail | 原 edge Consumer |
| DesignID／子義 | 24／57 | 逐 ID 保留原名與子義數（§D.1b） | 原 Design Owner |
| 受影 AssetSlot | 24 | 逐槽功能結果與 Consumer；未部署標 `SELECTED_NOT_QUALIFIED` | 原 Tech/Host Owner |
| 五集合 Slot | 485（20/30/24/25/386） | 見 §D.1c：逐集合處置＋每 Need 唯一 Occupant＋exact-key digest | 原 Tech Registry／Product Reader |
| CLI／Family／Skill | 13／19／8 | §B2 exact-set 已對 registry 實檔 | PIPD 原 Writer |
| SBL 條目 | 50／149 | 原名與去向保留；W1 只受影 | SBL 原 Reader |
| R15 | 949 | 不作全量 Native 再驗；受影者具名 | R15 原 Owner |
| Cell／ModeGate／Oracle／Acceptance Edge | 192／39／96／15 | 受影子集才有 W1 動作；其餘原波 | 原 Gate/Oracle Owner |
| B1 Case | 282（120/124/38） | 只接手受影案例 | B1 原 Runner |
| PI→PD | 27→31 | 見 §B4.1 的 PI/PD 實測 | PIPD 原 Compiler |

### D.1b 24 DesignID × 57 子義（原 ID 不重編）

| DesignID | 子義數 |
|---|---|
| `INT-05` | 3 |
| `INT-06` | 3 |
| `INT-07` | 3 |
| `INT-13` | 5 |
| `INT-14` | 3 |
| `INT-24` | 3 |
| `FHS-DR-007` | 2 |
| `FHS-DR-008` | 2 |
| `FHS-DR-023` | 2 |
| `FHS-DR-024` | 2 |
| `FHS-DR-025` | 2 |
| `FHS-DR-026` | 2 |
| `FHS-DR-027` | 2 |
| `FHS-DR-028` | 2 |
| `FHS-DR-029` | 2 |
| `FHS-DR-030` | 2 |
| `FHS-DR-031` | 2 |
| `FHS-DR-032` | 2 |
| `FHS-DR-034` | 2 |
| `FHS-DR-035` | 2 |
| `FHS-DR-036` | 2 |
| `FHS-DR-042` | 3 |
| `FHS-DR-043` | 2 |
| `FHS-DR-044` | 2 |
| **合計** | **57**（24 個 DesignID） |

### D.1c 485 五集合：不變量、逐集合處置與 exact-key 要求

**不變量（原文）**：Native20／Default30／Donor24／Method25／TECH386 是五種不同的原資產身分；485 只是 `20+30+24+25+386` 的**來源卡數**，不是 485 件必裝工具、也不是同一個驗收分母。每筆保留原名／處置／功能／Consumer／專屬 NEG，再按 `AssetType` 給不同建造、綁定、調用與退場規格。

| 集合 | 卡數 | 本波處置 | 專屬 NEG | 原 Consumer |
|---|---|---|---|---|
| Native20 | 20 | 原生能力優先復用；不足才 Build | 以外部工具冒充原生能力 | 原 Host／Native Owner |
| Default30 | 30 | 預設必備不降 optional；缺則 `SELECTED_NOT_QUALIFIED` | 把必備功能改 optional | 原 Product Reader |
| Donor24 | 24 | 只取可授權部分；License 未知即 `NOT_BOUND` | 從檔案 SHA 猜 upstream license | 原 Tech/License Owner |
| Method25 | 25 | 方法只產建議／SpecDelta，不產 Grant/Verdict | 方法 archive/ship 當 Release | 原 Method Owner |
| TECH386 | 386 | 逐 ID 保留 Need／Disposition／Parent／NEG／Consumer | 刪成「採用現有套件」或 386 套必裝 | 原 Tech Registry |

**exact-key 要求**：`WP-FHS-17／20` 必須**重算 exact-key digest**（不是只加總 20+30+24+25+386）；known-unknown 一律 `NOT_BOUND`。本地沒有逐列 386 清冊可直接引用，故本版給出**逐集合＋逐 Need 的處置與 digest 規則**，並具名 HOLD：

- `H-485-KEYS`：**485 全鍵**（Native20＋Default30＋Donor24＋Method25＋TECH386）的逐鍵清冊須由原 Tech Registry 提供；本地只有不變量、五集合處置與逐 Need Occupant，**不冒充逐鍵已列**。解除條件：原 Tech Owner 提供同 Scope 登錄檔（每鍵 Need／Disposition／Consumer／Host）。
- `H-TECH-LICENSE`：`TT-TECH-001`（SBL DOC-11 已登錄 `OPEN_HOLD`）——donor license/tag/security/host effective load 未解。
- `H-SLOT-24`：24 受影槽若無原 Host 實測，只能標 `SELECTED_NOT_QUALIFIED`，不得改 optional。

**每 Need 唯一 Occupant（逐 Need 判定，不以集合數量代替）**

| Need | 當期 Occupant／NoFit | 原 Consumer | POS | NEG（應拒） |
|---|---|---|---|---|
| 來源與權威綁定 | PIPD `AuthorityBinding` ＋ 原 Source Reader | SBL 原 Source Reader | 同 SourceSHA 可回查 | 以摘要或鄰卡充原句 |
| 編譯與綁定 | SBL `integrations/pipd`（13 verbs） | PIPD 原 Compiler | PI/PD 可重現（同 SHA） | 自建第二編譯器 |
| 執行契約 | `pipd-execution-contract` ＋ ECP | 原 Runner | 四物件 `validate` PASS | 用 PI 當 bundle 冒 PASS |
| 驗收與 Oracle | `pipd-assurance-tqaep` ＋ 原 Oracle | 原 Checker | 回執＋ceiling 同讀 | 偽回執讀成 PASS |
| 原生准入 | HG-KSEOS Issuer（`REFUSE` 現狀） | HGK 原 Issuer | 同 epoch/scope 才可續 | 以本地判定改寫 guard |
| 導覽與政策 | Fabric `INTEGRATION/FHS`（`effect_permission=NONE`） | Fabric Policy Owner | 未知路由 exit 3 | 把導覽當授權 |
| 宿主與 Worker | Hermes native（Profiles/Kanban/Delegation/Swarm/Runtime） | 原 Host Reader | WorkerPID/Lease 可讀 | 卡片 Done 當世界結果 |
| 技術資產 | 五集合逐 Need 唯一 Occupant | 原 Tech Registry | 未部署仍 `SELECTED_NOT_QUALIFIED` | 485 全裝或全拒 |

### D.2 新 `FHS_vNEXT` Repo 與本地遷移（設計，不在本輪執行）

**邊界**：本輪**不建立** Repo、不 push／PR／merge、不改三庫 `main`。以下只是可施工設計。

| 項目 | 決定 | 理由／限制 |
|---|---|---|
| 名稱 | `shw097-team/FHS_vNEXT`（備選 `FHS-vNEXT`） | 與既有 `FHS`、`FHS_NEXT` 不撞名；建立前需 Owner 核可用性 |
| 可見性 | private（預設） | 內含產品設計與原域條款；公開需 Owner 另裁 |
| Owner／權限 | shw097-team；只 Owner 有 admin | 單人單機；不給 bot admin |
| 單一 Git root | repo 根即 root；`FHS_NEXT/{SBL,HG-KSEOS,Fabric}` 以 **submodule 或 immutable snapshot** 接入 | 不複製成第二 Compiler／Issuer／Policy Writer（ADR-W1-01） |
| 分支／保護 | `main` 受保護（禁 force-push、需 review）；工作分支 `w1/*` | 對齊三庫 AGENTS.md 的 candidate-only 規則 |
| CI | lint＋schema validate＋selfcheck＋ZIP CRC；**不做** Native／Release | CI 不得冒 Issuer／Checker |
| 法務 | `LICENSE`（待 Owner 選）、`NOTICE`（三庫原授權與來源）、`SBOM`（每 donor 的 tag/commit／license） | donor license 未證即 `NOT_BOUND` |

**逐路徑可追溯抽取（FHS → FHS_NEXT）**

| 類別 | 路徑樣式 | 處置 | 回退 |
|---|---|---|---|
| 來源匯入（read-only） | `FHS/SBL/**`、`FHS/HG-KSEOS/**`、`FHS/Fabric/**` | 以原 commit 為 pin 的 snapshot／submodule；`provenance/SOURCE_IMPORT_MAP.json` 記錄每檔 origin SHA | 刪 snapshot，不動原庫 |
| 產品程式 | `FHS_NEXT/SBL/integrations/pipd/**`（現行 canonical） | 原地保留，逐檔 SHA 對齊；改動須走 PR | `git revert` 該 PR（僅限程式，非 Host 狀態） |
| 作者文件 | `FHS_NEXT/deliverables/**`、`_local/**` | 隨 repo 版本化；`CURRENT.json` 指針 | 回上一個 `CURRENT.json` |
| 環境設定／秘密 | `.env`、`*.key`、`*.enc`、token、DB、WAL | **不得複製**；以 Host secret 管理 | 不進版控即無需回退 |
| 需原 Reader／Issuer 才可執行的寫 | Host install、native effect、policy publish、release | 只寫設計與 HOLD；不得代簽 | 由原域各自回退 |

**舊 Repo 退場**：`PIPD-LS-SP` 已 archived，維持 `historical_repositories`、`write_authority=NONE`；`FHS` 單體庫轉 read-only 歷史來源（保留 tag/asset），不再接受新 work；三庫（SBL／HG-KSEOS／Fabric）維持權威，不退場。

### D.3 工具／方法／Skill／角色：各指定一版

**原則**：原生優先復用；同一 Need 只留一個 Occupant；不因最新版自動升級；未資格化標 `SELECTED_NOT_QUALIFIED`，但**必需功能不得因此改 optional**。

**本機實測現況（不是文件推論）**

| 元件 | 本機狀態（實測） | 用途邊界 |
|---|---|---|
| `openspec` | 1.8.0，`openspec init／validate --strict` 實跑（本輪變更紀錄 valid） | 只產變更提案與 SpecDelta；不得 archive/ship 當 Release |
| `codex` CLI | 存在（`command -v codex`） | 作為 bounded writer／checker lane；不得自簽 Native |
| `node`／`npx` | 存在 | 執行工具鏈；不引入第二排程器 |
| `gstack`／`kanban` CLI | **不存在**（已搜 0 命中） | 以工作區檔案實作同語義；不得聲稱已使用 |
| PIPD | 0.1.1a5、13 commands、19 families | 唯一 Canonical Writer／Reader |
| HG-KSEOS spine | schema_version 3、lease/idempotency/backup 可用 | 原生平面；`admission_status=UNPROVEN` 現狀 |

**一 Need 一 Occupant（本波定案，不留「永久 candidate」）**

| Need | Occupant（釘版） | 不選誰／為什麼 |
|---|---|---|
| 執行與編排面 | Hermes Agent `v0.23.1` | 不另造 scheduler／queue；Kanban 卡不得當 HGK WorkID |
| Spec 變更作者 | OpenSpec `2.0.0` | 不與 Spec Kit 併用作者面（其 constitution 會生第二份原則權威） |
| Process／phase 迴圈 | GSD Core `v1.21.0` | 不選 Superpowers（同 Need）；GSD 只取規劃面，其 Ship 不得當發行 |
| Skill 撰寫與審查紀律 | Matt Pocock skills `v1.3.2` | 只補 skill 層，不接管 process |
| 研究契約與 progress 判準 | FAR（commit `a6f1fa89…`） | 授權未宣告 → 只作研究輔助，不進可發行鏈 |
| 交付／發行 | **原域 Publisher**（本波無 Occupant） | gstack `/ship`、GSD Ship、Superpowers finishing 皆 `NOT_QUALIFIED` |
| 受保護檢查 | **原 Protected Checker**（本波無 Occupant） | OpenSpec `validate` 只作自家產物 lint |

**禁止的重複角色**：Publisher（gstack `/ship` × GSD Ship × Superpowers finishing）→ 全部不得在 FHS 內執行；Checker（OpenSpec validate × GSD Verify × Spec Kit analyze × Matt code-review × Superpowers verification）→ 只留 OpenSpec 作自家 lint，其餘不得升格；Scheduler／Queue → 只有 Hermes Kanban；原則／Canonical 權威 → 只有 Fabric 契約與 SBL／PIPD canonical。

**選型的兩個缺口（具名）**

- `H-GSD-NAMING`：本波以現行維護線 `open-gsd/gsd-core v1.21.0` 為準；若原意是已 archived 的 `gsd-build/get-shit-done`（v1.42.3），須改釘並承擔無人維護風險——需 Owner 一句話確認。
- `H-OPENSPEC-VERSION`：選定 `2.0.0`，本機 `INSTALLED=1.8.0`；`SELECTED` 不等於 `INSTALLED`，在升級前不得宣稱 2.0.0 的行為（如 `.agents/skills/` 與 `/openspec-*` 指令）。


**外部選型（官方來源、版本、授權、Windows fit）**

| 工具／方法 | 版本（發布日） | 授權 | Windows | 角色分類 | 本輪決定 | 本機狀態 | 驗證 |
|---|---|---|---|---|---|---|---|
| Hermes Agent | v0.23.1 (2026-11-10) | MIT | 原生（install.ps1 安裝器、Desktop 安裝器；官方另有 Win… | 執行與編排面（Runtime／Orchestration Plan… | SELECTED_ONE_VERSION v0.23.1 | present（codex-cli 0.164.0／node v24.19.0 為相鄰工具） | GitHub API 實查 v0.23.1（2026-11-10，MIT） |
| OpenSpec | 2.0.0 (2026-11-11) | MIT | 原生（Release 提供 openspec-windows-x64／arm6… | 規劃輔助（spec delta 作者＋自家產物 lint）—非治理… | SELECTED_ONE_VERSION 2.0.0 | 1.8.0（低於選定版） | GitHub API 實查 v2.0.0（2026-11-11，MIT）；本機 INSTA… |
| gstack | v1.99.3.0 (2026-11-13) | MIT | 原生但受限（Windows 11 需 Git Bash 或 WSL；官方列為 … | 規劃＋交付輔助，含 Publisher 相鄰能力（`/ship` … | SELECTED_NOT_QUALIFIED：Windows 僅 minimal … | ABSENT | GitHub API 實查 v1.99.3.0（2026-11-13，MIT）；本機 AB… |
| Superpowers | v7.0.2 (2026-11-03) | MIT | 原生但依賴 Git Bash（hooks 以 .cmd 轉呼 bash，官方有… | 規劃輔助（方法論＋15 個 skill 庫）—非治理級 | SELECTED_NOT_QUALIFIED：與 GSD Core 爭同一個「pr… | 未安裝（本輪不裝） | GitHub API 實查 v7.0.2（2026-11-03，MIT） |
| Spec Kit | v1.4.0 (2026-11-10) | MIT | 原生（官方明列 Linux／macOS／Windows；repo 內含 12 … | 規劃輔助（重型 SDD 工具箱；含 `/speckit-const… | SELECTED_NOT_QUALIFIED：與 OpenSpec 爭同一個 sp… | 未安裝（本輪不裝） | 官方 releases 頁實查 v1.4.0 |
| GSD Core | v1.21.0 (2026-11-13) | MIT | WSL／Git Bash（原生未驗證）：官方 install 頁只列 Node… | 規劃輔助（Discuss→Plan→Execute→Verify→… | SELECTED_ONE_VERSION v1.21.0 | 未安裝（本輪不裝） | npm 實查 @opengsd/gsd-core 1.21.0 |
| Matt Pocock skills | v1.3.2 (2026-10-29) | MIT | 原生（39 個 SKILL.md 皆為 Markdown；4 支 helper… | 規劃輔助（小型可組裝 skill：grill-me／to-spec… | SELECTED_ONE_VERSION v1.3.2 | 未安裝（本輪不裝） | 官方 releases 頁實查 v1.3.2 |
| FAR | 無語意版本；釘定 commit a6f1fa897052cb4a3bcba316e774721d3d4fe62b (2026-11-10（該 commit 提交日；Fabric repo 無任何 release）) | NOT_VERIFIED（repo 根目錄無 LICENSE／LICENSE.md，GitHub API 回報 license=null） | 不適用（文件、契約與收據集，無可執行安裝） | 研究產品（research product）—Fabric REA… | SELECTED_ONE_VERSION（以 commit a6f1fa89705… | 未安裝（本輪不裝） | 本地 repo 目錄實查：Fabric 無 LICENSE（API license=nul… |

> 研究窗：2026-10-01 以後的官方來源（GitHub releases／repo tree／npm registry／官方 docs）；每一項的版本與日期都取自實際抓取的頁面，未以記憶推定。1) 版本與日期：Hermes v0.23.1（2026-11-10，穩定；同日另有 +canary 預發佈不選）、OpenSpec 2.0.0（2026-11-11）、gstack v1.99.3.0（2026-11-13）、Superpowers v7.0.2（2026-11-03）、Spec Kit v1.4.0（2026-11-10）、GSD Core v1.21.0（2026-11-13）、mattpocock/skills v1.3.2（2026-10-29）、FAR 無版本（commit a6f1fa8，2026-11-10）。2) NOT_VERIFIED／待補：(a) FAR 授權——shw097-team/Fabric 無 LICENSE 檔、GitHub license=null，故記 NOT_VERIFIED；(b) GSD Core 的 Windows 原生支援——官方 install 頁未列 Windows，repo 內 0 支 .cmd／.ps1、15 支 .sh hook，故記「原生未驗證，實務需 Git Bash／WSL」；(c) GSD Core No…

---

## E｜受影自審（POS／NEG／FirstFail）與具名 HOLD

### E.1 原則

只驗本次改動與其依賴錐；不重跑 W0；不改 Oracle 湊綠；作者靜態通過**不得**宣稱 Independent。每個重要功能至少一個可執行 POS、一個會拒收的 NEG。

### E.2 受影案例表

| # | 類 | 情境 | 預期（可判定） | 依據 |
|---|---|---|---|---|
| N-01 | POS | 四物件 bundle 驗收 | exit 0、`checked=4`、`closure=FULL`、`findings=[]` | §B4.3 實測 |
| N-02 | NEG | 把 PI 當 bundle | exit 2 `INPUT_SHAPE_INVALID`（且不得當 PASS） | §B4.3 實測 |
| N-03 | NEG | 自寫／他主體／不存在的 Checker 回執 | `claim_ceiling` 不得提升、`independent_acceptance=NOT_GRANTED` | §B4.4 實測 |
| N-04 | NEG | caller `--head` 自報（含全零） | PD `head`＝live HEAD；只讀 `matches_host`，不讀 `verified` | §B4.4 實測 |
| N-05 | NEG | 用他 producer 的 evidence 結案 | 只保證「已註冊」，不得表述為 subject-bound | 上一輪 S8 實測 |
| N-06 | NEG | 非 git 根／路徑穿越 | `REPO_CONTEXT_MISSING` | 上一輪實測（exit 2） |
| N-07 | NEG | 非 canonical registry 走 effect | `REGISTRY_NOT_CANONICAL` | §B4.2 實測 |
| N-08 | NEG | maker 兼 checker | `TQ_SOD` | 上一輪實測（exit 2） |
| N-09 | NEG | 寫到授權根外 | `UNSAFE_DESTINATION` | 上一輪實測（exit 2） |
| N-10 | NEG | 未知導覽 route | exit 3 `HOLD_AFFECTED_WRITE`（只停受影寫入） | 本輪實測 |
| N-11 | POS | ACK 遺失重放同一 key | 同 `event_id`、`idempotent_replay=true` | 上一輪 S4 |
| N-12 | NEG | 同 key 用於別的 subject | `ERR_IDEMPOTENCY_KEY_REUSED_FOR_OTHER_SUBJECT` | 上一輪 S5 |
| N-13 | NEG | 終局 verdict 再改 | `ERR_ACCEPTANCE_ILLEGAL_TRANSITION` | 上一輪 S6 |
| N-14 | NEG | 未註冊 evidence | `ERR_ACCEPTANCE_EVIDENCE_UNKNOWN` | 上一輪 S7 |
| N-15 | NEG | 備份竄改／還原覆蓋 | `ERR_BACKUP_DIGEST_MISMATCH`／`ERR_RESTORE_TARGET_EXISTS` | 上一輪 S12／S11 |
| N-16 | POS | 乾淨還原到新目標 | OK（可驗的 Rollback 路徑） | 上一輪 S13 |

**FirstFail 原則**：任一 NEG 觸發只停該受影效果；合法 READ／DRAFT／沙箱 probe 續行。`SOURCE_OR_CONSUMER_NACK`、`PD_BINDING_HOLD`、`ADMISSION_DENY`、`CHECKER_SCOPE_NACK` 等原字面保留，不自造泛用 FAIL。

### E.3 本輪新發現（作者端可用性，非安全）

- `pipd init` 會建立空的 `schemas/`，之後 `doctor` 轉 workspace-local 並 `verdict=FAIL`（同一 FAIL 曾出現 exit 0 與 exit 1 兩種）：施工前置改為**先在無 `schemas/` 的目錄以 source-mode 解析（`families=19`）**，`doctor` 一律連 exit code 記錄。
- §09 的 bytes 欄曾與實檔不符（宣告 99,558，實檔 9,604）：本版一律以**實檔 SHA** 認定來源，不引 bytes 欄。

### E.4 具名 HOLD（只停受影效果）

| HOLD | 內容 | 解除條件 |
|---|---|---|
| `H-GUARD-EPOCH` | lane guard raw：`decision=REFUSE`、`epoch 41` vs `live_epoch 44`、`admission_status=UNPROVEN` | HG-KSEOS 發佈對齊 epoch 並重跑 |
| `H-EFFECT-ECP` | effect 型 ECP 在本樹 `REGISTRY_NOT_CANONICAL` | git 正本 registry ＋ sha 對齊 |
| `H-485-KEYS` | 485 全鍵（20/30/24/25/386）逐鍵清冊未在本地 | 原 Tech Registry 提供登錄檔 |
| `H-TECH-LICENSE` | `TT-TECH-001` donor license/tag/SBOM/Host load | 原 Tech/License/Host Owner 補 probe |
| `H-SLOT-24` | 24 受影槽缺原 Host 實測 | 原 Host Owner 實測或維持 `SELECTED_NOT_QUALIFIED` |
| `H-ORIGINAL-ACK` | 13 主責章 body 與 Raw 未經原 Reader 接受 | 原 Domain Reader 同 Scope 簽署 |
| `H-W0-INHERIT` | W0 r9 已完成範圍不得重跑；只接 handoff | 已由 W0 `CURRENT.json` 固定 |
| `H-REPO-CREATE` | 新 `FHS_vNEXT` Repo 未建立 | Owner 明示授權＋可用性核對 |

---

## F｜交付、跨波 handoff 與終態

### F.1 W1 → W2／W3／W4 只交五件

| 交接物 | 內容 | 接收方 |
|---|---|---|
| Source | 每條引用的 `ID:Ln@sha256`（166 條／18 ID／0 混版） | 原域 Reader |
| OriginalID | 原卡／原 requirement 識別，不改名不重編 | 原 Writer |
| Case | `AUTHOR.W1.CH-xx.POS/NEG/SEC` | TQAEP／Oracle |
| ExpectedRaw | 該 case 的可判定原始輸出期待 | 原 Runner |
| HOLD | §E.4 具名 HOLD | 原 Owner |

**不可交接**：TraceClosure、獨立 Checker 結論、Publisher cutover、任何 Native／Release 狀態。

### F.2 驗收門檻對照（本輪自檢結果見附錄 C）

| 門檻 | 本版狀態 |
|---|---|
| 正文可讓工程者按 WP 施工而不需附錄補核心條款 | ✅ 13 主責章 12 欄齊備；37 章有法位／I-O／POS-NEG／Exit |
| 50 章／13 主責／8 WP／保護分母可追 | ✅ §C、§B3、§D.1 |
| 各原義 POS／NEG／Consumer 不丟 | ✅ 原字面保留，逐列可回查 |
| 上游與 W0 對齊 | ✅ §A.2；W0 不重跑 |
| 外部選型非空且已釘版 | ✅ §D.3（一 Need 一 Occupant，來源與版本見附錄 C） |
| Repo／遷移邊界清楚 | ✅ §D.2 |
| 受影 HOLD 能局部恢復 | ✅ §E.4 每列有解除條件 |
| 三檔真存在且互鏈 | ✅ 見 §F.3 |

### F.3 三檔交付

| 檔 | 用途 |
|---|---|
| `FHS_vNEXT_PLP_W1_實質正文_施工定案版_2026-11-14_r1.md` | 本檔（工程實質正文，可直接施工） |
| `FHS_vNEXT_PLP_W1_證據型附錄_施工定案版_2026-11-14_r1.md` | 來源 SHA、逐列證據、外部研究、自審與驗收挑戰原始輸出 |
| `FHS_vNEXT_PLP_W1_施工定案包_2026-11-14_r1.zip` | 只含上述兩 MD；CRC＋成員 SHA 回讀 |

**終態（施工定案不改變 Native／Independent／Release 三項未取得）**：
`OWNER_RULED_CONSTRUCTION_BASELINE / HOST_PENDING / EXECUTOR_UNBOUND / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / RELEASE_NOT_GRANTED`
<!-- END BASE BYTES -->

---

## 施工輪回報（r1 → r2 之間實際量測到的狀態）

| WP | 實際 | 證據 |
|---|---|---|
| WP-FHS-02 | 唯讀觀測＋拒收；consumer ABI 缺席 → effect HOLD | `out/WP02_WP03_READONLY.json` |
| WP-FHS-03 | 六 epoch 欄位、guard REFUSE、spine 14/14 | `out/WP03_HGK_SPINE.json` |
| WP-FHS-04 | WorkID／Kanban／GSTACK／SWARM 帳 | `out/WP04_RUNTIME.json` |
| WP-FHS-05 | 13 verbs、PI/ECP 決定性、四物件 bundle 4/4、8 個 typed 拒收 | `out/WP05_PIPD_CHAIN.json、out/WP05_BUNDLE4.json` |
| WP-FHS-07 | Commander A/B/C 三份 Guide | `deliverables/WP07_COMMANDER_ABC.md` |
| WP-FHS-11 | 宿主階段實測＋每 Host 四階段方案 | `out/WP11_HOST_DOGFOOD.json、deliverables/WP11_HOST_PLAN_2026-11-14.md` |
| WP-FHS-17 | 485 逐鍵＋digest | `out/WP17_485_LEDGER.json` |
| WP-FHS-20 | 39 格設計矩陣＋12 格宿主矩陣 | `out/WP20_MODEGATE39.json、out/WP20_MATRIX.json` |

**凍結 rubric 自檢**：8/8（`out/ACCEPTANCE_EVAL.json`）；**FHS_NEXT selfcheck**：16/16。
**驗收挑戰**：三輪 nonce 歸屬判決皆 REJECT（R1 G2/G3、R2 G7、R3 G7 代理條款），每項已更正並保留（`docs/CORRECTIONS.json`）。
**Owner 裁定**：`docs/OWNER_RULINGS_W1R2.json`（OD-W1R2-1..5）。
**ACK**：`FHS_ORIGINAL_ACK(W1)` = 1/7（owner 片已簽，reader receipts 未由 maker 代簽）。

