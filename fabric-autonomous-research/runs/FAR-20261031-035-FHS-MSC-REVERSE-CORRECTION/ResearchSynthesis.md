# FAR-035｜反向修正：我上一輪的四份「缺席」有三份是誤讀

日期：2026-10-31（台北）
路由：Fabric 治理契約 → SBL 產品工程指揮入口 → HG-KSEOS 授權／狀態／驗收控制平面
車道：PLAN `openai-codex/gpt-6.1-sol`｜EXECUTE `opencode-go/deepseek-v4.1-flash`｜VERIFY `openai-codex/gpt-6.1-sol`
權威：`work_queue` — 22 條 = **18 PASS / 4 FAIL / 0 NOT_RUN**

---

## 0. 結論先行

**你懷疑得對。我上一輪說「這四包被點名的對象不在這台機器上」，是誤讀。**

交付文件自己把 Host 寫成四個具名宿主：

> **四 Host**：Hermes Agent、Codex、Claude Code、ChatGPT；前 3 的 CLI/Skill/Plugin 能力各以真 Loader/Process/Security 驗證；ChatGPT Web/API-only …不可假定具有 OS process runner。每 Host 要 Install→Register→Effective Load→Trigger/Nontrigger→Uninstall/Retire。
> — `01_PRODUCT_AUTHORITY_SPINE.md:47`

而我實測這台機器：

| Host | 狀態 |
| --- | --- |
| Hermes Agent | `v0.22.5` ✓ |
| Codex | `codex-cli 0.164.0` ✓ |
| Claude Code | `2.1.314` ✓ |
| ChatGPT | web/API-only，規格自己禁止聲稱本地安裝 |

**三個在、一個規格禁止。** 所以 WP-11/12/13/20 不是「做不到」，是**沒做**。ALL PASS 可達，工作量在 Host 端，不在治理端。

我上一輪的搜尋用 `host_loader|host_reader|toolautoselect|technologyadmission` 找「叫這個名字的程式」，命中 0 就下結論「對象不存在」。用較寬的名稱族重搜，同一個 workspace 有 **848** 個 Python 檔命中；其中就有真正的 packager、admission engine、profile 與 host loader。**這是我的過度解讀，不是系統的限制。**

---

## 1. 尚未 PASS 的完整清單

| 包 | clause 要求的 | 實測存在的 | 真正缺的 |
| --- | --- | --- | --- |
| **WP-FHS-11** Portable Host Dogfood | 3 SP × 各 Host 的 install/load/invoke/remove manifest；Reader = 各 Host 原 Skill Reader | Portable SP packager：`PIPD/src/pipd_ls_sp/export_bundle.py`（確定性 tar.gz + manifest + checksums）。Host 檢查器：`tools/host_projection_check.py` → `projection.check_host_surfaces` | 三個宿主上各一輪 Install→Register→Effective Load→Trigger/Nontrigger→Uninstall 的**實測**。目前 9 cell / 0 qualified |
| **WP-FHS-12** W18 Normal Mode | 原 normal Profile / ToolAutoSelect Reader；NEG：B1 專用 Prompt 或 test plugin 充 NormalMode | `PIPD/src/pipd_ls_sp/profiles.py`（LITE/STANDARD/ASSURED）；Hermes 本身就是 normal-entry host | 一次**普通 Goal** 的 W18 實跑與 E33–E42 raw；`C:/wg/queue/WP-FHS-12` **目錄不存在**（brief 從沒寫過） |
| **WP-FHS-13** CAP On-Demand + HotSwap | 原 TechnologyAdmission → HotSwap admission ABI → 原 Consumer 與 Host Loader | `PIPD/tools/admit_technologies.py`（22 列，含 disposition/pin/licence/TTL/fallback）**存在** | **HotSwap 本身 0 實作**：全 workspace 20 個 `hotswap` 命中全是 QA 修補工具與 officer verify 腳本「提到」這個詞；規格 `08_TECHNOLOGY_DEFAULT_HOTSWAP.md` 有 **81** 處。屬於「有規格、無實作」 |
| **WP-FHS-20** Kind×Mode×Host×Provider 192 | 8 Kind × 3 Mode × 4 Host × Provider，每 Cell 的原 Host Reader | 三個 host projection 實體存在（`host_generic-skills` / `host_hgk-receiver` / `host_genie-adapter`，含 `receiver-map.json`、`object-crosswalk.json`） | 192 cell 中 1 個 Kind 列已建；其餘 7 列未建。**另有規格內部矛盾**，見 §3 |

---

## 2. 反向修正：三個誤讀、一個真缺口、一個規格矛盾

### 誤讀 1：把「原 Host」讀成一個叫 `host_loader` 的程式

規格裡 `09B` 的某個 Cell 寫得更直白：

> route/HostCaps：**原 Hermes tool/skill loader** 與 worker fresh PID；OS process runner，**不要求 Host skill loader**。

Host 就是宿主自己。我卻去找一個獨立程式，找不到就宣告缺席。**ABSENT-01 / 02 / 04 已撤回**（`var/FHS-ALLPASS-20261031/ABSENT_OBJECTS/WITHDRAWALS.json`），因為它們各自寫下的「可推翻條件」已經成立——一份可證偽的拒絕在被證偽之後必須撤回，不能因為方便而留著。

### 誤讀 2：把 schema 名稱當成服務不存在

`TechnologyAdmission` 在 `registry.py` 裡是 19 個 machine contract 之一（schema 名）。真正的 admission 引擎是 `tools/admit_technologies.py`，563 行，處理 22 列，帶 disposition 集合 `{ADOPT, REFERENCE, EVAL_ONLY, QUARANTINE, REJECT}` 與「非 ADOPT 永不得報 active/installed」的規則。**它存在。**

### 誤讀 3：把 fixture-grade 當成不存在

`tools/host_projection_check.py --strict` 我實跑了：

```json
{"mode":"STRICT_CHECK_ONLY","candidate_head":"995c7ad",
 "claims":{"live_hgk_genie_integration":"NOT_CLAIMED","s5_s6":"NOT_AUTHORISED",
           "adapter_checks":"FIXTURE_MOCK_ONLY","live_status":"NOT_RUN"},
 "first_failing_invariant":"STALE_SOURCE: stale source hash for S0:PI-PKG",
 "failures":[{"path":"host_genie-adapter/object-crosswalk.json","mutation":"MUT-STALE-SOURCE"},
             {"path":"host_genie-adapter/object-crosswalk.json","mutation":"MUT-WEB-WRONGSET"}]}
```

**它有跑、有判、有 10 個 mutation code，而且自己宣告「effective load 是 fixture/mock，S5/S6 未授權，live 未跑」。** 這是產品自己寫下的天花板，不是我猜的。缺的不是程式，是**授權一個 live 整合**，以及把 stale 的 genie-adapter projection 重新推導。

### 真缺口：HotSwap

| 事實 | 數值 |
| --- | --- |
| 程式實作 | **0** |
| 規格提及 | 81（`08_TECHNOLOGY_DEFAULT_HOTSWAP.md`） |
| 名稱族命中 | 20，全為 QA 修補／verify 腳本「提到」 |

這是真的缺口，`ABSENT-03` 已改寫為它（`refusal_gate` → `REFUSALS_FALSIFIABLE`，1/1）。

### 規格矛盾（需要反向修正的是規格，不是判準）

WP-20 要求 **4 Host × 192 Cell** 每格的原 Host Reader。但同一份交付又寫「ChatGPT Web/API-only …不可假定具有 OS process runner」「Web GPT 不聲稱本地 CLI / Repo install」。

**那 48 個 ChatGPT cell 在定義上永遠不可能 native PASS。** 把它們留在分母裡，等於要求一個規格自己禁止的結果；把它們算成 PASS，就是換判準。唯一誠實的做法是**修正分母的定義**：ChatGPT 的 cell 標 `NOT_ADMITTED_BY_SPEC`，分母改為 144，並在收據裡同時列出 `192 total / 144 admitted / 48 not-admitted-by-spec`。這需要 owner 簽（`registry_row_sign`）。

---

## 3. 你點名的三條替代路徑，逐一評估

| 路徑 | 判定 | 理由 |
| --- | --- | --- |
| **獨立車道** | 可用，但不解決問題 | 三條車道本輪全部 `required==served`（PLAN 12.05 s、EXECUTE 2.70 s、VERIFY 6.11 s）。車道能加速「做」，不能替代「Host 上的 install/load」。 |
| **本地 Docker 沙盒** | 部分可用，對簽章是負面 | `docker version` → daemon 未啟動（npipe 連不上）；WSL `Ubuntu-24.04`、`docker-desktop` 都是 Stopped。可啟動，但三個 Host 都是 Windows 原生 CLI，容器內跑不了；且容器內 DPAPI 更不可用（本輪已實測沙箱內簽不出授權）。**不用於簽章路徑。** |
| **owner key passphrase envelope** | 已在開、可用，但它是授權不是能力 | 視窗 `WIN-68f2056b1972` 仍開（剩 24,598 s、指紋 `412b351937be72a1` 一致）。它能簽 install 授權，**不能生出 HotSwap**。用它假裝能力已具備，就是換判準。 |

**裁示**：三者都不能把「沒做」變成「做不到」，也都不能把「做不到」變成「PASS」。真正能關掉這四包的只有一件事：**在三個宿主上各跑一輪真實的 install→load→trigger→uninstall。**

---

## 4. 達成 ALL PASS 的執行方案

### Phase A — 先把一格做到真（WP-FHS-11 第一格，Hermes）

```bash
# 1. 用真正的 packager 產出 Portable SP（不是手寫 manifest）
cd /c/Projects/Agent_Workspace/PIPD && python -m pipd_ls_sp.cli export --help

# 2. 在 Hermes 上做 install→register→effective load→trigger→uninstall
#    Reader = Hermes 自己的 skill loader（profiles/hgk-governed/skills，現有 13 個）
#    收據必須含 09_SBL_DOC00_13_FULL_UPGRADE.md:264 的欄位：
#    host, host_version, skill_id, manifest_sha, source_pin, install_dir, discover_ok, bind_ok,
#    trigger_input_ref, trigger_raw_result, exit_code, unload_verification, provider_off_parity
```

**驗收判據（不可替換）**：空 trigger 或只有 install log → `HOST_NOT_EFFECTIVE`。這是規格原文，不是我加的。

### Phase B — 換宿主，不換方法（Codex、Claude Code）

```bash
codex --version   # 0.164.0
claude --version  # 2.1.314
```

同一組 install/load/trigger/uninstall，Reader 換成該宿主的 loader。三格成功 = WP-11 的 3/9；加上 NEG（一 SP 安裝 receipt 當三 SP 9/9 → `HOST_SP_MATRIX_INCOMPLETE`）才是 9/9。

### Phase C — 其餘三包

| 包 | 第一步 | 完成判據 |
| --- | --- | --- |
| WP-12 | 立 brief（目錄不存在）→ 一次普通 Goal 的 W18 實跑 | E33–E42 raw + `NORMAL_MODE_NOT_QUALIFIED` 負測 |
| WP-13 | HotSwap 立項（唯一真缺口） | 換手後 POS（新 occupant 服務）+ NEG（舊 occupant 不再服務）+ parity |
| WP-20 | 先簽分母修正（§2 規格矛盾），再逐 Kind 建列 | 144 admitted cell 逐格有原 Host Reader 的 raw |

---

## 5. 全部殘留如何關閉（每一項都有會拒絕假關閉的 gate）

| 殘留 | 關閉物 | 誰會拒絕假關閉 |
| --- | --- | --- |
| WP-11/12/13/20 FAIL | 各宿主實測收據 | `ir_gate`（IR-1/IR-4）+ 收據缺 trigger raw → `HOST_NOT_EFFECTIVE` |
| HotSwap 0 實作 | 換手程式 + parity 證據 | `CAPABILITY_PARITY_NOT_PROVEN`（規格原文） |
| genie-adapter projection stale | 重新推導並過 `--strict` | `MUT-STALE-SOURCE` / `MUT-WEB-WRONGSET`（已實測會拒） |
| WP-12/13 無目錄 | 立 brief | `work_queue` DELIVERY 量測解析（無 brief 無法建 candidate） |
| WP-20 分母矛盾 | owner 簽 `NOT_ADMITTED_BY_SPEC` | `refusal_gate`（需 cited_text + falsifier + expiry） |
| 四份錯誤缺席記錄 | **已撤回**（本輪） | `WITHDRAWALS.json` 記錄了「為何撤回」與「撤回不等於 PASS」 |
| rollout 身份未綁定 | `REQ-SEC-ROLLOUT-BINDING` | `--require-rollout-binding` 目前拒絕，修好才放行 |
| DPAPI 沙箱內不可用 | 已在沙箱外預簽 | `wp17_owner_preissue.py` 四輪收斂 |
| scoreboard | 已 CONSISTENT | 投影由 `work_queue render` 產生 |

---

## 6. 待 OWNER / issuer 決策（需簽章）

| # | 決策 | 建議 | scope | 不簽的後果 |
| --- | --- | --- | --- | --- |
| **D-A** | WP-20 分母修正：ChatGPT 48 cell → `NOT_ADMITTED_BY_SPEC`，分母 192→144 | **簽** | `registry_row_sign` | 192 cell 永遠不可能全 PASS，且每次都要重複解釋 |
| **D-B** | live HGK/GENIE 整合授權（S5/S6） | **簽（有條件）**：只授權 fixture→live 的單格試點，不授權全面 live | `admission_bundle_sign` | WP-11 native 永遠 HOLD；bounded 仍可 PASS |
| **D-C** | HotSwap 立項（WP-13） | **簽** | `permit_sign` | WP-13 永遠 FAIL，且它是唯一「有規格無實作」的缺口 |
| **D-D** | r18 具名 graft 併入 main | **簽**：`git merge --allow-unrelated-histories`，保留 provenance | `registry_row_sign` | 本輪 20+ commits 只存在 r18，main 永遠看不到 |
| **D-E** | `lane/epoch-40-identity-source-20261031` 併入 main | **簽**：4 ahead / 0 behind，可 fast-forward | `registry_row_sign` | 車道 epoch 40 只在分支上 |
| **D-F** | FAR 分支併入 | 建議保留為 audit branch，不合 main | — | — |

**否決**：任何「bounded 改叫 native」的提案；任何把 ChatGPT cell 算成 PASS 的提案。

---

## 7. 升格與併 MAIN（已檢測的實測事實）

| 分支／候選 | 拓撲 | 判定 |
| --- | --- | --- |
| `lane/epoch-40-identity-source-20261031` | merge-base `303395be`，**4 ahead / 0 behind** | **可併**（fast-forward），建議 D-E |
| `candidate/r18-fhs-skeleton-spine-20261029` | merge-base **NONE**（unrelated histories） | 需**具名 graft**；不可正常 merge |
| `candidate/r19-fhs-implementation` | merge-base **NONE** | 同上 |
| `far/far-031-…`（Fabric） | 獨立 audit branch | 保留，不合 main |
| WP-FHS-17 bounded PASS | 已驗收（`EVT-e7a55272fd18a6ac`） | **可升格為模板**（已用於 WP-11 規劃） |
| WP-FHS-17 native | 六條 clause 五條 OPEN | **不可升格** |

---

## 8. 裁示：是設計筆誤還是我的誤讀？

| 問題 | 裁示 |
| --- | --- |
| 「原 Host 不存在」 | **我的誤讀**。規格寫得很清楚，是我搜錯名字族。已撤回三份記錄。 |
| WP-20 192 vs ChatGPT 不得本地安裝 | **規格缺口**，需反向修正分母定義（D-A）。這不是判準放寬，是把不可能的格子從分母裡拿掉並具名。 |
| HotSwap | **實作缺口**，不是規格缺口（規格 81 處）。 |
| DPAPI 沙箱內不可用 | **設計缺口已修**（沙箱外預簽），不是誤讀。 |
| 四包「做不到」 | **誤讀**。三個宿主在，第四個規格自己排除。可達 ALL PASS，缺的是工作量。 |

---

## 9. 下一步（單一指令）

```bash
cd /c/Projects/Agent_Workspace/HG-KSEOS && python scripts/work_queue.py show   # 18/4/0
# 然後 Phase A 第一格：
cd /c/Projects/Agent_Workspace/PIPD && python -m pipd_ls_sp.cli export --help
```

**不要做**：不要用 Docker 繞簽章；不要把 ChatGPT cell 算 PASS；不要為讓 gate 變綠手改投影。
