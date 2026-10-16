# FAR 裁決附錄 A — 執行期發現（ROUND3-LANE-REBIND-AND-CLOSURE-20261016）

本附錄為 `FAR_RULING.md` 的**加性**補充：原裁決 R1–R9 一字不改，僅補入**執行 R1–R3 時才被量測出來**的
缺陷與其裁決。每一條都附量測依據、選項、否決選項與宣稱上限。

## A2 — R10（DO）：pre-dispatch 守衛必須承認「業主令宣告的碰撞」

**量測（本回合，活體）**：以新令的實際模型呼叫守衛 →

    hgk-lane-guard.py --lane VERIFY_SECURITY --maker-model opencode-go/deepseek-v4.1-flash \
                      --target-model opencode-go/deepseek-v4.1-flash --admission ADMITTED --expected-epoch 22
    → decision=REFUSE exit=2 errors=[ERR_LANE_SOD_VIOLATION]
      detail: SOD_VIOLATION maker_model=deepseek-v4.1-flash == checker_model=deepseek-v4.1-flash

`check_sod()` 是**純二值比較**（`src/hg_kseos/lane_policy.py`），守衛只把 `--maker-model`/`--target-model`
餵進去 → **結構上不讀 registry**。因此在新令下，VERIFY/SECURITY 車道**永遠不可能通過 pre-dispatch 閘門**。

**為何這是缺陷而非政策**：產品自己的 conformance 測試（`tests/test_lane_policy.py`）已明文寫出意圖 ——
「a pair may be explicitly demoted … with the collision declared in `declared_conflicts` — the sweep must then
assert the DECLARATION exists instead of asserting separation」。registry 也確實帶著 `SOD006-C3`
（`OWNER_ORDERED_IN_FORCE`）。**兩個執行面彼此矛盾**：宣告面允許，閘門面硬拒。

**裁決（DO）**：讓守衛與 registry 一致，且不開任何後門——只在**同時**滿足下列兩條件時豁免：
(i) `sod_invariants.pairs` 有一筆 maker/checker 對應此 pair 且 `distinct_required: false`；
(ii) `sod_invariants.declared_conflicts` 有一筆**指名同一 pair** 且 `status == OWNER_ORDERED_IN_FORCE`。
且**每個回執必須帶 `declared_conflict: <id>`**（豁免可見、絕不靜默）；maker 車道未給時只在**唯一** route
的預設臂與 `--maker-model` 相符時推斷，否則 fail-closed 不豁免。實作交由**受令的 EXECUTE bounded writer**
（`WO-ROUND3-LANE-REBIND-AND-CLOSURE-20261016-EXECUTE`），RED-first 測試，再由**受令的 VERIFY 車道**獨立複核。

**否決選項**：
(a) 直接放寬 `check_sod()` —— 會破壞其他呼叫者依賴的純規則，且把「owner-ordered」的判斷從資料面移進程式常數；
(b) 只看 `distinct_required: false` 就豁免 —— 手改一行的 registry 即可**靜默**放行自我驗收；
(c) 派工時改餵別的車道 model 以繞過檢查 —— 不誠實：被檢物的真 maker 就是 EXECUTE writer；
(d) 只報告不修 —— 等於留下「業主令無法派工、本回合無任何獨立檢查」，比修更糟。

**殘留（明列）**：豁免把信任邊界從「程式常數」移到「registry 宣告」。registry 本身受 `source_of_routes`
digest、`epoch`、conformance 測試與業主覆核把關；但**手改 registry 仍可自我宣告**——此風險在 VERIFY 車道
被判為必查項，並在本回合作為 accepted risk 揭露，不聲稱為合規。

## A3 — R11（REPORT，部分 DO）：守衛要求的 ADMITTED 回執在生產路徑上沒有產生器

**量測**：`_load_admission()` 只接受**回執檔**（`status: ADMITTED`）作為 ADMITTED 的來源，裸字串僅在
UNPROVEN/REFUSED 被接受（fail-closed 設計）。全 repo 搜尋 `"status": "ADMITTED"` 只在
`tests/test_lane_guard.py` 的 fixture 出現 → **生產路徑無產生器**。實務後果：此閘門「只能拒絕、無法放行」。

**裁決**：本回合**不**新造探針產生器（那是新能力，需自身 WorkOrder 與驗收）；如實記錄為缺口 R11，並在
本回合把 VERIFY 車道的 `admission_status` 維持為 `UNPROVEN`，車道證據使用車道自身的 serving receipt
（`required_arm == served_arm`），**明確標示它不是守衛的 admission 回執**。

## A4 — R12／SC-12（DO＋揭露）：備份時序缺陷，且 `config/` 未被 git 追蹤

**量測**：`apply_R1_R2_R3.commit()` 先寫入、後 `backup()` → 四份 `.bak-round3-*` 實為**後編輯**副本；
`git show HEAD:config/lane-routing-registry.yaml` → `exists on disk, but not in 'HEAD'`（`config/` 未追蹤）
→ git 亦不持有 preimage。

**裁決（DO）**：以**摘要比對**從回合 2 的凍結 subject 樹尋回四份 preimage（`38f0436b…`、`e7be2dea…`、
`9fd0835f…`、`15556fd2…`），安裝於 `preimages/` 並附來源；此為**已證實等價**（逐位元 sha256）而非推定。
缺陷本身以 SC-12 揭露（備份時序、以及 `config/` 不在版控內使 git 無法作為回滾來源）。

## A5 — NF-05（REPORT）：派工池自稱 CANDIDATE，卻被 dispatcher 當作權威讀取

**量測**：`scripts/hgk-lane-dispatch.py:77 DEFAULT_POOL = ROOT/"config/lane-route-slots.candidate.json"`，
而該檔自載 `status: CANDIDATE`、`claim_ceiling: CANDIDATE_ONLY. Not promoted, not active.`
→ **宣告面與運作面不一致**（潛在的誤導來源）。裁決：本回合僅**如實標註**於該檔 `selection_note`（並改其
rank 以符合新令），不擅自改其 status（status 的變更屬推廣，超出本回合宣稱上限）。

## A6 — 執行順序與宣稱上限

順序：R1–R3 已落地（registry/pool/fixture/projections；`check_drift` 0 error；conformance 3/3 OK）→
R10 交 EXECUTE writer → 推入 canonical → **重新凍結** subject → 派 VERIFY 車道（新 checker 臂）→
閘門 → 發布 → 結案 → 移交 → 自演化。

**宣稱上限**：`CANDIDATE_ONLY`；`hgk_canonical_acceptance: NOT_PERFORMED`；合併/分支刪除屬 OWNER；
R10 的豁免為**業主令下的具名例外**，不是合規；R11 未解；SC-12 已揭露並以摘要證明修補。
