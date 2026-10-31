# FAR-20261031-033｜八項殘留的裁決、授權與可執行方案

Subject：`FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`
前案：`FAR-20261031-031`（研究）、`FAR-20261031-032`（執行輪）
量測時間：2026-10-31T13:40Z 起
治理：Fabric = 契約；SBL = 產品工程指揮入口；HG-KSEOS = 原生授權／狀態／驗收控制平面
車道：PLAN `openai-codex/gpt-6.1-sol` medium；EXECUTE `opencode-go/deepseek-v4.1-flash`；VERIFY `openai-codex/gpt-6.1-sol` medium

---

## 0. 三句話

1. **四個 HOST_OP 不是「同一條鏈」。** 實測分母：`WP-FHS-11` 需 9 個原生 cell + 146 個靜態檔；`WP-FHS-20` 需 192 個 cell × 8 Kind；`WP-FHS-12`、`WP-FHS-13` 目錄**完全空白**（連 brief 都沒有）。把它們當成「把 WP-17 腳本再跑四次」是錯的，這是本報告最重要的一條。
2. **四個包所點名的原服務，在四個 repo 裡都不存在為程式。** 我對 `HG-KSEOS`／`SBL`／`PIPD-LS-SP` 做了 `host_loader|host_reader|toolautoselect|technologyadmission` 的全庫掃描，命中全部是文件／corpus 引用，**零個實作**。所以「native admission 未動」不是怠惰，是**被點名的對象不在這台機器上**——這是一個必須由 owner 裁決的事實，不是工程進度問題。
3. **九項裡有三項本輪已經關掉並留下證據**（pin 遺失、門禁不落痕、失敗折疊進凍結碼），四項有明確可執行裁決但需動路由／政策（D-16、oracle nonce 契約、C4 身份綁定、記分板投影），兩項需 owner 簽章（native 天花板、C4 安全要求）。

---

## 1. 分母：九項的實測狀態

| # | 項目 | 實測狀態（本輪） | 可自解？ |
|---|---|---|---|
| 1 | WP-11 | `verdict FAIL`，`first_fail HOST_SP_MATRIX_INCOMPLETE`，`required_cells 9`／`qualified 0`，`missing_required_static_files 146`，`execution_status NOT_RUN` | 需原 Portable SP packager + Host Loader |
| 2 | WP-12 | 目錄空（無 brief／無 candidate／無 receipt） | 需先立 brief；依賴 WP-10+WP-11 |
| 3 | WP-13 | 目錄空 | 依賴 WP-16+**WP-17**（17 現為 FAIL） |
| 4 | WP-20 | 192 cell、`qualified 0`、`NoFit 0`、`NOT_RUN 192`、Kind 交付 1/8、原 Host Reader 0/4、provider token mapping 0/192 | 需 4 個原 Host Reader |
| 5 | Native admission | 被點名的原 Host Installer／Loader／Registry **不在任何 repo** | 需 owner 裁決 |
| 6 | D-16 EXECUTE 固定路徑 | `ERR_LANE_ALL_ROUTES_EXHAUSTED`，`required_arm null`，診斷 `ERR_ARM_PIN_UNROUTABLE` | **是**（本輪已加診斷，路由修正待做） |
| 7 | 驗收員 C2/C3/C5（nonce 契約） | oracle 寫「全輪一個 nonce」，實測每條車道各帶自己的 nonce | **是** |
| 8 | C4（codex-rollout 同目錄無關 rollout 被接受） | 驗收員以 in-memory probe 重現：同 cwd 的無關 rollout 被接受、不同 cwd 被拒 | **是**（但屬安全語義變更） |
| 9 | 記分板 DIVERGENT／pin 遺失／失敗折疊／門禁不落痕／guard-subject | 記分板仍 DIVERGENT（3 舊行 + STATUS 9950 s）；**pin／門禁／診斷三項本輪已修並實測** | 部分 |

**事實更正**：`FAR-20261031-032` 的 handoff 寫「`EVIDENCE_GAP.md` in the same tree」——**WP-17 樹裡沒有這個檔**（`find` 零命中）。有 `EVIDENCE_GAP.md` 的是 **WP-20**。WP-17 的缺口只存在於 `wp17_receiver.py` 的 docstring 與 `EXECUTED_BOUNDED_LOCAL` 這個 ceiling 字串裡。我上一輪把 docstring 當成了檔案，這是我的錯，已在 R-5 更正。

---

## 2. 關鍵結構發現：原服務不存在

```
grep -rliE "host[_ -]?loader|host[_ -]?reader|toolautoselect|technologyadmission" \
     HG-KSEOS SBL PIPD-LS-SP --include=*.py --include=*.md --include=*.ps1
→ HG-KSEOS: 5 命中，全部在 evidence/ openspec/ 文件與 site-packages
→ SBL:     5 命中，全部在 references/corpus/ 的 PIPD 文件
→ PIPD-LS-SP: 0
```

四個包的 Producer／Consumer 位置點名的是：原 Portable SP packager／Host Loader（11）、原 normal Profile／ToolAutoSelect Reader（12）、原 TechnologyAdmission／Host Loader（13）、原四 Host Reader（20）。**這些在這台機器上沒有可執行實作。**

這決定了 R-1／R-2 的形狀：**在 native 天花板上，這四包今天不可能 PASS；在 bounded 天花板上，它們可以，但代價差三個數量級。**

---

## 3. 裁決

### R-1｜四個 HOST_OP 包：拆成「bounded 交付」與「native 交付」兩個 ceiling，並依序推進

**裁定**：不要再用「同一條鏈」描述這四包。每包拆成兩個可分別驗收的交付：

| 包 | bounded 交付（可今天做） | native 交付（今天不可做） | 建議順序 |
|---|---|---|---|
| WP-11 | 3 SP × 3 操作的本機 install/load/invoke raw，bounded receiver 如 WP-17 | 三 archive + 9 原生 lifecycle cell 於 Host SP matrix | **第 1**（最接近，已有 build/hosts harness） |
| WP-13 | Need/Occupant/HotSwap admission 的 bounded parity POS/NEG | 原 TechnologyAdmission + Host Loader 參與 | **第 2**（依賴 WP-17，17 已測到 FUNCTIONALLY_QUALIFIED） |
| WP-12 | 新 PID 普通 Goal 的 E33–E42 raw（bounded profile reader） | 原 normal Profile／ToolAutoSelect Reader | 第 3（依賴 11） |
| WP-20 | 8 Kind 的 bounded 實作 + 192 cell 的 ON/OFF 判定 | 每 cell 由原 Host Reader 出 raw | **最後**（192 cell，量級最大） |

**理由**：`WP-17` 已證明 bounded 鏈可在一棵 WP 樹裡完整量測（`INSTALLED→HOST_LOADED→INVOKED→FUNCTIONALLY_QUALIFIED`，15/15 負測），代價是 8 個缺陷與一次驗收員 FAIL。四包各自複製這個代價，但 **WP-20 的 192 cell 不是「複製」，是 192 次**。

**否決的替代**：
- 「四包一起跑」→ 會被 WP-20 拖死，且 12/13 連 brief 都沒有。
- 「用 WP-17 的 receiver 直接當四包的 receiver」→ 拒絕。WP-17 的 receiver 綁 CAP-BOOT 的單一 occupant；WP-20 是 8 Kind × 3 Mode × 4 Host × 2 的矩陣，不是一個 occupant。
- 「先做 native」→ 對象不存在（§2）。

**精確改動**：無程式碼改動；改的是**分母**。在 `work_queue` 為每包加兩個子需求（`-B` bounded、`-N` native），使 `FAIL` 不再混淆「bounded 沒做」與「native 做不到」。

**防再發測試**：`scripts/scoreboard_consistency.py` 增加 ceiling 維度——一個 WP 的 verdict 必須帶 ceiling，缺 ceiling 即 `DIVERGENT`。

**簽章**：不需要（不動驗收標準，只是把兩個 ceiling 分開陳述）。

---

### R-2｜Native admission：立「缺席對象」記錄，不要立「無能」記錄

**裁定**：對四個原服務各寫一份 `refusal_gate` 合規的缺席記錄（`cited_text`＝DAG 該行原文、`absent_object`＝服務名、`reproduction`＝§2 的 grep 與 WP-17 receiver 的 `EVIDENCE_GAP`、`falsifier`＝該服務出現並回應一次、`expiry`＝下次 review）。這**不是** PASS，也**不是** FAIL——它是 `NOT_CLOSABLE_ON_THIS_HOST`，並且可被推翻。

**理由**：目前 `EVIDENCE_GAP` 在 WP-20 有、WP-17 沒有，四包各自缺席。缺席必須是**具名且可證偽**的物件；否則下一個 session 會再次把「沒有實作」讀成「沒有能力」，就像上輪把 `PARK` 字串讀成 `NO-HOST-CAPABILITY`。

**否決的替代**：把 bounded 改叫 native（換掉成功判準）——明確拒絕。

**精確改動**：新增 `var/FHS-ALLPASS-20261031/ABSENT_OBJECTS/`，四份 JSON，schema 對齊 `scripts/refusal_gate.py` 的五個必填欄位。

**防再發測試**：`refusal_gate.py` 已存在且會拒收缺欄位者；把它掛進 `acceptance_default.py` 的收尾路徑（目前只掛在部分路徑）。

**簽章**：**需要 owner**。這是對「native 天花板今天不可達」的正式承認，屬於驗收語義，必須由 owner 簽。

---

### R-3｜D-16：`--require-arm` 只能是「事後斷言＋候選過濾」，不得注入模型

**裁定**：pin 的語義是「這一輪必須由 arm X 服務」，不是「把 X 的限定 id 塞給 Codex CLI」。修法：

1. `--require-arm` 只做候選過濾（現有 `selection_filter` 已正確）。
2. spawn 時**永不**把 `provider/model` 限定 id 當 `--model` 傳給 CLI；非 `openai-codex` provider 的 arm 一律走其 relay 路徑（與未 pin 時完全相同）。
3. 收據在 `ok:false` 時仍記 `required_arm`／`required_arm_satisfied:false`（**本輪已做，實測 `EXECUTE_pin2.json`**）。
4. 診斷 `ERR_ARM_PIN_UNROUTABLE`（**本輪已做，實測**）。

**理由**：未 pin 時同一 arm 3.89 s 服務、pin 時 2.84 s 被 CLI 拒絕——差別只在誰拿到那個字串。這是接線錯，不是能力缺。

**否決的替代**：「EXECUTE 就永遠不要 pin」——拒絕。那等於放棄 `required==served` 這個唯一能證明「這一輪真的是 deepseek 在寫」的機制，也讓驗收員 C1 永遠無法 discharge。

**精確改動**：`scripts/hgk-lane-dispatch.py` 的 pinned spawn 分支（約 2499–2510 與 spawn 前的 model 組裝處），把 arm 的 `transport_model` 與 CLI `--model` 解耦；relay 路徑沿用未 pin 時的同一條。

**防再發測試**：`tests/test_lane_pin_routing.py`——pin 一個非 `openai-codex` arm，斷言子命令列**不含**該限定 id、且 `required_arm_satisfied` 在成功時為 true；並用一個 stub CLI 斷言「pin 與未 pin 產生相同 argv」。

**簽章**：不需要（純接線修正，不改政策）。

---

### R-4｜oracle nonce 契約：一輪一 seed，逐車道派生

**裁定**：oracle 的 C1–C6 寫「全輪一個 nonce」是錯的規格——每條車道各帶自己的 nonce 才可能各自被證明。改成：

- 一輪一個 **round seed**（如 `FHS-ALLPASS-20261031`）；
- 每條車道／每次 sitting 的 nonce = `NONCE-<LANE>-<ROUNDSEED>-<SITTING>`；
- oracle 條款改寫為「每個 child 的回應必須回顯**該 sitting 的** nonce」，並要求收據記錄 `round_seed` 與 `sitting`。

**理由**：驗收員 C2 的 NOT_DISCHARGED 有一半是我方規格錯，不是車道錯——它被要求在一條 EXECUTE 的回應裡找 PLAN 的 nonce。這種「條款本身不可滿足」是比缺陷更糟的東西：它保證永遠 FAIL。

**否決的替代**：讓所有車道共用一個 nonce——拒絕。那會讓「哪條車道回了話」不可區分，正好是這輪要修的病。

**精確改動**：`oracle/ORACLE_LANE_ACCEPTANCE.md` 條款改寫 + dispatcher 收據加 `round_seed`／`sitting`（各一行）。

**防再發測試**：oracle 檔的自我檢查——每個 clause 必須指名它要讀哪個 sitting 的 nonce；缺則 `scripts/acceptance_default.py` 拒收。

**簽章**：不需要（規格修正）。

---

### R-5｜WP-17 的 ceiling 更正：沒有 `EVIDENCE_GAP.md`，只有 docstring

**裁定**：把「`EVIDENCE_GAP.md` 仍開」更正為「**WP-17 樹內無此檔**；缺口陳述僅存在於 `wp17_receiver.py` 的 docstring 與 `EXECUTED_BOUNDED_LOCAL` ceiling 字串」。並在 WP-17 樹內補一份真正的 `EVIDENCE_GAP.md`（照 WP-20 的格式），列出六條 clause 的實際狀態。

**理由**：我上一輪把 docstring 當檔案引用。一個「宣稱有缺口文件」的 handoff，比沒有文件更危險——下一個人會去找那個檔，找不到，然後開始懷疑整份 handoff。

**否決的替代**：算了，口頭說明即可——拒絕。缺席必須落成檔案。

**精確改動**：`C:/wg/queue/WP-FHS-17/EVIDENCE_GAP.md`（新檔），照 WP-20 的表格格式；同時更正 `ROUND_HANDOFF.md` 的那一行。

**防再發測試**：`acceptance_default.py` 收尾時，若 receipt 的 ceiling 含 `BOUNDED`，要求同樹存在 `EVIDENCE_GAP.md`，否則拒收。

**簽章**：不需要。

---

### R-6｜C4（codex-rollout 同目錄無關 rollout 被接受）：升為 SEC 需求，不就地改

**裁定**：驗收員的 probe 顯示 `codex-rollout` 以「同 cwd 的最近 rollout」解析身份，**不要求 child binding**。這意味著同目錄下任何無關 rollout 都能冒充本輪的身份來源。裁定：

1. 立 `REQ-SEC-ROLLOUT-BINDING`（新需求），不動現行 `codex-rollout` 的行為。
2. 過渡期：收據必須同時記 `identity_source` 與 `rollout_binding`（`child_pid`／`turn_id`／`cwd`），使「有綁定」與「只有 cwd」可區分。
3. 真正修法（下一輪）：解析時要求 rollout 的 `session_id` 或 `turn_id` 與本次 spawn 相符，否則 `ERR_ROLLOUT_UNBOUND`。

**理由**：這是一個真實的**身份冒充面**——不是「車道不可用」，而是「車道可用但身份可被同目錄污染」。把它就地改掉會立刻打破現在唯一能服務的三條車道；把它留著不改則是已知漏洞。所以：**先讓它可見（欄位），再讓它可修（需求＋測試）**。

**否決的替代**：立刻改成嚴格綁定——拒絕。會讓 PLAN／VERIFY 全滅，且沒有備援身份來源。

**精確改動**：收據加 `rollout_binding`；新需求文件 + 失敗測試（先紅）。

**簽章**：**需要 owner**（安全語義變更 + 過渡期接受已知風險）。

---

### R-7｜記分板：投影由 driver 重寫，gate 拒絕對 stale 認證

**裁定**：`TODO.md`／`STATUS.json` 是 driver 的投影，**不得手改**（本輪我手改了 `GOAL.json` 的 counts，那是投影，已記錄 reconcile 來源；`TODO.md`／`STATUS.json` 我不動）。改法是：

1. `work_queue.py` 加 `--write-projections`，從權威渲染 `TODO.md`／`STATUS.md`／`GOAL.json`。
2. `scoreboard_consistency.py` 在 `stale` 為真時**拒絕輸出 CONSISTENT**（現行已是 `DIVERGENT`，正確）。
3. driver 每次 tick 後呼叫 `--write-projections`，使投影不會落後超過一個 tick。

**理由**：權威已是 17/5/0，投影落後 9950 秒。手改投影等於製造第二個權威——正是這輪要消滅的東西。

**否決的替代**：手改 `TODO.md` 讓 gate 變綠——拒絕。那是把 gate 弄瞎。

**精確改動**：`scripts/work_queue.py` 新增 render 子命令；driver 加一行呼叫。

**防再發測試**：`scoreboard_consistency.py` 已有負向（stale → DIVERGENT）；再加一個正向：render 後立刻 gate 必須 CONSISTENT。

**簽章**：不需要。

---

### R-8｜收據不得靠缺席推斷（本輪已關）

**裁定與實作**：三項已修並實測（commit `4661a48`）：

| 缺陷 | 修法 | 實測 |
|---|---|---|
| pin 在失敗時遺失 | `required_arm` 一律記錄 + `required_arm_satisfied` + note | `EXECUTE_pin2.json`：`required_arm` 有值、`satisfied:false` |
| 門禁 GO 不落痕 | `durable_gates: {verdict, subject, tool, detail}` | `VERIFY_gate.json`：`verdict GO`、subject 正確 |
| 失敗折疊進凍結碼 | 三個具名診斷，凍結碼不動 | `diagnostic: ERR_ARM_PIN_UNROUTABLE` |

**防再發測試**：`tests/test_lane_identity_source_default.py` 已釘住凍結碼；新增斷言「帶 `--require-arm` 的失敗收據必有 `required_arm`」。

**簽章**：不需要。

---

### R-9｜`--guard-subject` 的語義：寫進文件，並在派發時拒絕跨 repo subject

**裁定**：`--guard-subject` 是**摘要錨點**，`workspace-write` 的根永遠是派發所在 repo。因此：

1. 文件更正（skill 已改）。
2. dispatcher 在 `--guard-subject` 指向 repo 外時，於**派發前**發出 `WARN_GUARD_SUBJECT_OUTSIDE_REPO`（不是拒絕——它對 read-only 檢查仍有效），使「檢查員跑不動 subject」不再以 `ERR_NO_ARM_EMITTED_NONCE` 的形式出現。
3. 要讓 VERIFY 真正跑 WP 樹，**把 subject 放進 repo**（`HG-KSEOS/fhs_msc_handoff_20261030/WP-FHS-17/`），這是下輪的第一個動作。

**理由**：這輪三次失敗（PLAN 寫 oracle、驗收員 B、驗收員 C 的 WP-17 clause）都是同一個機制，而收據三次都把原因歸給臂。

**簽章**：不需要。

---

## 4. 授權與簽章建議

| 項目 | 需要 owner 簽章？ | 用哪個 scope | 建議 |
|---|---|---|---|
| R-1 分母拆分（bounded/native 子需求） | 否 | — | 直接做 |
| R-2 四份缺席記錄 | **是** | `registry_row_sign` | 建議簽：它把「今天做不到」變成可證偽的事實，且不降低任何標準 |
| R-3 D-16 接線修正 | 否 | — | 直接做，附 `test_lane_pin_routing.py` |
| R-4 nonce 契約改寫 | 否 | — | 直接做 |
| R-5 WP-17 EVIDENCE_GAP 補檔 + handoff 更正 | 否 | — | 直接做 |
| R-6 C4 rollout 綁定 | **是** | `admission_bundle_sign` | 建議**分兩步簽**：先簽「記錄 `rollout_binding`、接受過渡風險」，修法另案 |
| R-7 投影渲染 | 否 | — | 直接做 |
| R-8 收據欄位 | 否 | — | **已完成** |
| R-9 guard-subject 語義 | 否 | — | 直接做 |
| 任何「把 bounded 當 native」 | **否決** | — | 這是換掉成功判準，不簽 |

Owner key window：`WIN-68f2056b1972`（本輪開啟，8 h，`REPOSITORY_WRITE`，指紋 `412b351937be72a1`）。R-2 與 R-6 的簽章可在同一視窗內完成，不需再開。

---

## 5. 可執行方案

### Phase A（不需簽章，今天可做完）
```
A1  R-3  D-16 接線：pin 只做過濾，relay 路徑與未 pin 相同 + tests/test_lane_pin_routing.py
A2  R-4  oracle 條款改寫為 per-sitting nonce；收據加 round_seed/sitting
A3  R-5  C:/wg/queue/WP-FHS-17/EVIDENCE_GAP.md（照 WP-20 格式）+ 更正 ROUND_HANDOFF.md
A4  R-7  work_queue.py --write-projections；driver tick 後呼叫
A5  R-9  WARN_GUARD_SUBJECT_OUTSIDE_REPO
A6  把 WP-17 樹複製進 HG-KSEOS/fhs_msc_handoff_20261030/WP-FHS-17/（讓 VERIFY 跑得動）
```
驗收：`PYTHONPATH="src;tests" python -m unittest` 全綠；`scoreboard_consistency.py` 在 render 後 CONSISTENT；EXECUTE pinned 回 `ok:true`。

### Phase B（需 owner 簽章，一次視窗內完成）
```
B1  R-2  四份 ABSENT_OBJECTS/*.json，掛進 refusal_gate
B2  R-6  REQ-SEC-ROLLOUT-BINDING + rollout_binding 欄位 + 先紅的測試
```

### Phase C（bounded 交付，依 R-1 順序）
```
C1  WP-11 bounded：3 SP × 3 操作的本機 install/load/invoke raw
C2  WP-13 bounded：Need/Occupant/HotSwap parity POS/NEG（WP-17 已可作模板）
C3  WP-12 bounded：新 PID 普通 Goal 的 E33–E42 raw
C4  WP-20 bounded：8 Kind 實作 + 192 cell ON/OFF（量級最大，最後）
```
每包的收尾條件：`install→fresh load→invoke→consumer ack` + 全部負測按**被測理由**拒絕 + 同樹 `EVIDENCE_GAP.md` + VERIFY 在 repo 內跑得動。

---

## 6. 本輪已做 / 未做（claim ceiling）

**已做並實測**：R-8 三項（commit `4661a48`，`EXECUTE_pin2.json`／`VERIFY_gate.json` 為證）；§1 的全部分母量測；§2 的原服務缺席掃描；事實更正（WP-17 無 EVIDENCE_GAP）。

**未做**：R-1～R-7、R-9 的任何程式改動；四包的 bounded 交付；任何 native 效果。

**Ceiling**：本報告是**裁決與方案**，不是 PASS。`work_queue` 仍為 22 條 = **17 PASS / 5 FAIL / 0 NOT_RUN**；`WP-17` 仍是 FAIL（驗收員無法在寫根內執行 subject）。R-2 的缺席記錄若簽署，也**不會**把任何 FAIL 變成 PASS——它只會把「做不到」變成「可證偽」。
