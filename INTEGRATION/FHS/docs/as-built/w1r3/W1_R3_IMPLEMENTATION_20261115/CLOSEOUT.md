# W1 r3 八 WP 實作｜結案（2026-11-15）

**輪次**：`W1_R3_IMPLEMENTATION_20261115`
**Subject**：`W1-REPAIR-r3-2026-11-15` sha256 `5aca7b5e2bdc67d13dff95432b14d7e152f18e3d341971490b7a77c395345a6b`
**Claim ceiling**：`AUTHOR_W1_CHECK / LOCAL_CHECK / NOT_NATIVE / NOT_INDEPENDENT / NOT_RELEASE`
**Owner**：單人單機 Human Owner（語義接受另由 owner key 簽，見 §6）

---

## 一、一句話

r3 正文的八張 W1 主責 WP 卡，已逐卡變成**可執行的作者側裁判**：POS 全層通過、每個宣告的 NEG 由 POS 單點變異導出並在第一失敗層回該卡自己的碼；35 個工作清單單元與 GJ01–03 三條旅程全部有實測，gate 全綠，獨立回合第 4 輪 `APPROVED`。

## 二、實測數字（全部由收據計算，非手寫）

| 項 | 值 | 收據 |
|---|---|---|
| 工作清單單元 | 8 WP ＋ 18 findings ＋ 3 旅程 ＋ 6 效果 ＝ **35** | `out/W1R3_WORKLIST.json` |
| WP 受影案例 | **50**（8 POS ＋ 42 NEG） | `out/GATE_W1R3.json` A 段 |
| 旅程案例 | **17**（3 POS ＋ 14 NEG） | 同上 C 段 |
| findings 證據存在 | **18/18** | 同上 B 段 |
| 六效果條款完整 | **6/6** | 同上 D 段 |
| FALSE_GREEN 變異自檢 | **8/8 咬住**（清空 evidence／借別 scope／刪必要欄位） | 同上 SELFTEST |
| gate 判定 | `PASS`，failures `0`，missing `0` | `out/GATE_W1R3.json` |
| 裁判模組 | 9 支／73,716 bytes | 下表 |
| 案例檔 | 77 個 JSON | `tests/affected/W1/` |
| 獨立回合 | 4 輪：10 → 2 → 1 → 0（失敗集合單調不增）；最終 **APPROVED** | `out/REVIEW_CYCLES.json` |

裁判模組逐檔 sha256（前 16 碼）：

| 模組 | bytes | sha256 |
|---|---|---|
| `wp_fhs_02.py` | 5,421 | `4ffdf67a8b183603…` |
| `wp_fhs_03.py` | 6,327 | `0abcad8e0e88edf5…` |
| `wp_fhs_04.py` | 6,302 | `73da8b90aa3529b3…` |
| `wp_fhs_05.py` | 7,491 | `8731cdb694e3062e…` |
| `wp_fhs_07.py` | 6,597 | `a9d789e82e3a2419…` |
| `wp_fhs_11.py` | 6,515 | `3ee62511f6dda561…` |
| `wp_fhs_17.py` | 10,561 | `50757a59a4e84416…` |
| `wp_fhs_20.py` | 9,775 | `855f95f67530d1ef…` |
| `journey_referee.py` | 14,727 | `765ff19282c97b91…` |

## 三、八張卡怎麼被實作

每張卡都照正文的「依序 Operation」變成層序；第一層失敗即回該層的碼，後面的層不再判（§10.6 第 4 條）。碼全部是卡上宣告的碼，沒有新造原 RequirementID／CaseID／OperationType，命名一律 `AUTHOR.W1.*`。

| 卡 | 輸出型別 | 層數 | 首拒碼（NEG） | 安全反例碼 |
|---|---|---|---|---|
| WP-FHS-02 | PolicyLoadedConsumerACK | 4 | POLICY_NOT_LOADED / POLICY_LOADED_ACK_MISSING | POLICY_SIGNER_OR_EPOCH_DENY |
| WP-FHS-03 | IssuerReceiverBinding | 5 | GUARD_RAW_MISMATCH / ISSUER_WORK_BINDING_NACK / RETIREMENT_BOUNDARY_UNPROVEN | ISSUER_PRINCIPAL_ACL_DENY |
| WP-FHS-04 | WakeLeaseRuntimeBinding | 5 | RUNTIME_USE_NOT_OBSERVED / SERVED_ASSIGNMENT_OVERWRITE | CROSS_PROFILE_SECRET_DENY |
| WP-FHS-05 | SourceBoundPipdHandoffDesign | 5 | ORIGINAL_PIPD_REPARSE_UNBOUND / PD_REPOCONTEXT_UNBOUND | PIPD_SHADOW_WRITER_DENY |
| WP-FHS-07 | PlanRevisionProposal | 4 | PLAN_RECEIVER_UNBOUND / PLAN_CAS_ACK_MISSING | CROSS_WORK_PLAN_AUTH_DENY |
| WP-FHS-11 | HostSPQualificationPlan | 4 | HOST_SP_NOT_QUALIFIED / HOST_LOADED_UNPROVEN / HOST_EVIDENCE_FOREIGN_NACK | HOST_CHECKER_IMPERSONATION_DENY |
| WP-FHS-17 | CapabilityOccupancyAndQualificationPlan | 5 | TECH_NEED_OR_LICENSE_HOLD / CAPABILITY_NOT_QUALIFIED | INSTALLER_PRIVILEGE_DENY |
| WP-FHS-20 | ProductCellApplicabilityHandoff | 5 | PRODUCT_APPLICABILITY_HOLD / CELL_TOKEN_OWNER_ACK_MISSING | CELL_RECEIPT_CROSS_HOST_DENY |
| GJ01/02/03（A-01） | SourceAnswer / SpecDelta / DevWorkOrder | 5/5/4 | KNOWN_ANSWER_REASK、POLICY_NOT_LOADED、UNRELATED_HOST_GATE、UNRELATED_RELEASE_GATE、FUO_NOT_DELIVERED、SECOND_CANONICAL_WRITER、HOST_WRITESET_BIND_HOLD、ISSUE_WRITE_NOT_OBSERVED、UNKNOWN_RECONCILE_REQUIRED、PD_REPOCONTEXT_UNBOUND、PLAN_CAS_ACK_MISSING | — |

## 四、怎麼跑（複製即用）

```bash
PY=C:/Users/user/AppData/Local/hermes/cache/scratch/fhs_next/venv311/Scripts/python.exe
cd C:/Projects/Agent_Workspace/FHS_NEXT_Workspace/W1_R3_IMPLEMENTATION_20261115
$PY build/00_extract_worklist.py            # 抽 35 單元（會驗 subject sha）
$PY build/mk_neg.py --all                   # 由 POS＋mutation 導出全部 NEG（單點變更驗證）
$PY build/gate_w1r3.py --selftest           # 全案 gate ＋ FALSE_GREEN 變異自檢
$PY build/verify_round.py --show            # 看收斂回合
```

期望：`verdict: PASS`；A 50/50、B 18/18、C 17/17、D 6/6、SELFTEST 8/8。

## 五、路線決定（重要，已排除的錯誤路線）

- **Codex CLI 沙盒路線已依業主裁定廢止**。本輪先誤走該路線（`codex exec -s workspace-write`），8 個並行回合全部在統 exec helper 啟動失敗，未產生任何檔案；判為錯誤路由後停止，未再使用。
- 正確路線＝**已建成的 3L&M 入口 ＋ 直連 loopback router**：
  1. `ops/tools/fhs_3lm_pathadapter.py --menu`（epoch registry `3583f71b…`），
  2. `--bind EXECUTE primary`（DEEPSEEK V4.1 FLASH／opencode-go，pool_rank 1）、`--bind VERIFY opt1`（同 arm），
  3. 每次寫入回合是一次 `POST http://127.0.0.1:10102/v1/chat/completions`（`deepseek-v4.1-flash`），憑證由 router 持有，本輪不接觸任何 key 值。
- 直連 `https://opencode.ai/...` 對本機三把 key 皆回 `HTTP 403 error code: 1010`（邊緣阻擋），故不作路線；已記錄而非繞過。

## 六、Owner key（預授權與語義接受）

- 評估：本輪唯一需要 owner key 的消費者為 `owner_semantic_accept`（見 `docs/OWNER_KEY_EVALUATION.md`）；不需要也不需要代簽 release／sourcefreeze／original_reader_ack。
- 窗口：`WIN-16ed4dc875b8`，task `W1_R3_IMPLEMENTATION_20261115`，scope `owner_semantic_accept`，max_ops 8、TTL 3h，口令一次由業主輸入，之後 broker headless 簽。
- 簽章結果與 body digest 見 `out/OWNER_SEMANTIC_ACCEPT.json`。

## 七、本輪未主張（不可被引用為已通過）

- **未主張**：`NATIVE_SIGNED`、`INDEPENDENT_PASS`（本輪的獨立回合是同家族模型的獨立回合，非原域 Protected Checker）、原域接受、`RELEASE_GRANTED`。
- **未執行**：任何產品碼改動、原 Host 安裝、Canonical PIPD 編譯（除既有進口位元外）、relay／registry 變更、三庫 main 寫入。
- **局部 HOLD**（皆為原權限，不是本輪缺工）：`H-ORIGINAL-CASE-RUNNER`（原 Case/Oracle/Runner 三 fixture pins）、`H-ENTRY`、`H-GUARD-RAW-MISMATCH`、`H-RETIREMENT-BOUNDARY`、`H-READER-PIPD`、`H-SUPPLYCHAIN-RAW`。
- **證據邊界**：WP-FHS-03…20 的**寫入回合收據**被後續單 WP 重跑覆蓋（RC-3），本輪不補造；那些卡的產物由 gate 收據與模組／fixture 逐檔 sha 承載。

## 八、更正紀錄

`docs/CORRECTIONS.json` RC-1…RC-7：stale NEG、迴圈判定優先序、回合收據覆蓋、write-guard 拒絕新路徑、borrowed_scope 落層、旅程碼無覆蓋（A-01）、兩個空集合層（vacuous gate）。

## 九、接手

1. 要跑同一 gate：§四 四條命令。
2. 要把某張卡接回原域：把該卡的 `POS/NEG` 換成原 Case Registry 提供的三實體（POS input／NEG input／Raw schema），本輪的裁判模組只作作者側前置，不取代原 Runner。
3. 要推進 W2：W1 這一輪提供的是「八卡的拒收語義已被實測」，不是「八卡已原生完成」；W2 仍需原准入與 exact WriteSet。
