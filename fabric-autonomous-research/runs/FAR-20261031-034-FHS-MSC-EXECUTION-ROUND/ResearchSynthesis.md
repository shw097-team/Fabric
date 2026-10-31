# FAR-034｜本輪執行：七項裁決落地、WP-17 由 FAIL 轉 PASS、四包殘留的單一原因

日期：2026-10-31（台北）
路由：Fabric 治理契約 → SBL 產品工程指揮入口 → HG-KSEOS 授權／狀態／驗收控制平面
車道：PLAN `openai-codex/gpt-6.1-sol`(medium)｜EXECUTE `opencode-go/deepseek-v4.1-flash`｜VERIFY `openai-codex/gpt-6.1-sol`(medium)
權威：`work_queue` — 22 條 = **18 PASS / 4 FAIL / 0 NOT_RUN**

---

## 一、這一輪真正改變了什麼

上一輪我交的是裁決與方案（FAR-033）。這一輪把其中七項**做完並實測**，並且把 WP-FHS-17 從 FAIL 推到 PASS。

| 裁決 | 上輪狀態 | 本輪狀態 | 證據 |
| --- | --- | --- | --- |
| R-2 四份缺席記錄 | 待簽 | **已落 gate** | `refusal_gate.py` → `REFUSALS_FALSIFIABLE` 4/4 |
| R-3 D-16 固定路徑 | 誤判為「pin 不可用」 | **誤判已推翻並修好** | `EXECUTE_pin3` 2.70 s，`required==served` |
| R-4 nonce 契約 | 待改 | **已改並落欄位** | `round_seed`/`sitting`/`nonce_contract` |
| R-5 EVIDENCE_GAP | 誤稱存在 | **已補檔，六條 OPEN 列名** | `WP-FHS-17/EVIDENCE_GAP.md` |
| R-6 C4 rollout 綁定 | 待立項 | **已可被要求、且要求就拒絕** | `ERR_ROLLOUT_BINDING_UNIMPLEMENTED` |
| R-7 記分板 | DIVERGENT | **CONSISTENT** | `work_queue.py render` + liveness 重分類 |
| R-9 guard-subject | 待加警告 | **已加並落收據** | `WARN_GUARD_SUBJECT_OUTSIDE_REPO` |
| R-1 雙天花板 | 待拆 | **已拆成 JSON 裁定** | `CEILING_SPLIT.json` |
| R-8 收據可審計 | 上輪已完成 | 保持 | — |

---

## 二、D-16 不是 pin：一個被我自己製造的假設

我上輪把 EXECUTE 的固定失敗歸因為「Codex 帳戶不支持該 provider 的限定模型 id」。這一輪交叉比對兩份收據後推翻：

| 收據 | `--relay-base` | 結果 |
| --- | --- | --- |
| `EXECUTE_probe` | **未帶**（預設 loopback） | `ok:true` 3.89 s |
| `EXECUTE_reqarm` | `https://chatgpt.com/backend-api/codex` | exit 3，2.84 s，「model is not supported…」 |
| `EXECUTE_pin3`（本輪） | **未帶** | `ok:true` 2.70 s，`required_arm == served_arm` |

**pin 從來不是問題；是那條 `--relay-base` 被當成樣板複製到每一次派發。** 上游只服務 OpenAI 模型，把
`opencode-go/*` 的臂指向上游，Codex 會在 3 秒內拒絕——讀起來完全像一條死臂。

修法不是「不要 pin」（那會讓 `required==served` 永遠無法證明），而是**讓 transport 成為臂的 provider 的函數**：
派發前若臂的 provider ≠ `openai-codex` 而 `--relay-base` 指向上游，直接拒絕
`ERR_RELAY_BASE_INCOMPATIBLE_WITH_ARM` 並給出正確指令。三個測試釘住。

三條車道因此全部「可服務且可固定」：PLAN 12.05 s、EXECUTE 2.70 s、VERIFY 6.11 s，`required==served`、nonce 回顯。

---

## 三、WP-FHS-17：三次坐席，三個不同的「不能」

| 坐席 | 結果 | 真正的原因 | 學到什麼 |
| --- | --- | --- | --- |
| E | `ERR_CHECKER_MUTATED_SUBJECT` | 驗收員**跑得動**了（257 s，exit 0，nonce 回顯），但 `build_evidence.py` 把 install root、load 收據、negatives 寫進被測樹 | 門禁是對的：改過的樹不是被測的樹 |
| F | `UNVERIFIABLE` | 沙箱內 DPAPI 不可用：`issue_grant.py` 回「262 bytes, expected a 32-byte seed」 | 驗收員不該持有簽章能力 |
| G | **PASS** | — | 三者同時成立：能執行、能取得真授權、不動記錄 |

**修法（兩個，都不靠放寬門禁）**

1. `--guard-subject`（可寫的工作副本）與 `--guard-record`（必須逐位元不變的記錄）分離；副本在坐席開始前
   與記錄比對，不一致就 `ERR_SUBJECT_COPY_DIVERGES`（不 spawn）。
2. 主體**請求**、owner **在沙箱外簽**、主體**消費**：`WP17_PREPARE_ONLY=1` 寫出它需要的確切 argv，
   `wp17_owner_preissue.py` 迴圈簽章，`WP17_PREISSUED` 消費。驗收員全程不持有私鑰。

**坐席 G 實測**：`INSTALLED → LOADED_AND_INVOKED → CONSUMER_ACK`，15/15 負測因**被測原因**拒絕，
install 收據 `14:25:29.101966Z` 晚於 run 起點 `14:25:20Z`；記錄 481 檔前後 `CLEAN`（0 改、0 刪）。

**天花板照寫**：六條 clause 中五條仍 OPEN（native admission、原 consumer、CAP-BOOT ABI、stage vs install root、
rollout 綁定），只有 `officer_could_execute_subject` 由 OPEN 轉 **CLOSED**。這是 bounded 鏈的 PASS，不是
native admission，不是 canonical acceptance，不是升格。

---

## 四、剩下四包：不是四個問題，是一個

`work_queue` 仍 4 FAIL，全部是 HOST_OP。它們不是「還沒做」，是**被點名的對象不在這台機器上**：

| 包 | bounded 實測 | native |
| --- | --- | --- |
| WP-FHS-11 | NOT_DELIVERED：9 cell、0 qualified、1342 檔、無 EVIDENCE_GAP | ABSENT-01 |
| WP-FHS-12 | **目錄不存在**（`C:/wg/queue/WP-FHS-12` 沒有這個目錄） | ABSENT-02 |
| WP-FHS-13 | **目錄不存在** | ABSENT-03 |
| WP-FHS-20 | PARTIAL：8 個 Kind 列建了 1 個、192 cell 待做 | ABSENT-04 |

四份缺席記錄都通過 `refusal_gate`：引用原文、具名缺席對象、實際跑過的命令、可推翻條件、到期日。
**這不是 PASS，是把「做不到」變成「可證偽」。** 任何人把 WP-17 的 bounded receiver 改名成 native admission
都是在換判準，本輪明確否決。

**更正**：上一輪報告把 WP-12/13 寫成「空目錄」。它們不是空的，是不存在——空目錄是待辦，不存在是 brief 從沒寫過，
兩者的下一步不同。

---

## 五、狀態與下一步

```
work_queue      22 = 18 PASS / 4 FAIL / 0 NOT_RUN
scoreboard      CONSISTENT（1 筆 informational：STATUS.json 為 liveness 文件且已過期）
lanes           ALL_THREE_LANES_SERVE_AND_PIN
tests           20/20 OK（policy 12、identity 2、relay-base 3、rollout 3 含 2 條 refusal、guard-record 2）
```

**下一輪的第一步（單一指令）**

```bash
cd /c/Projects/Agent_Workspace/HG-KSEOS && python scripts/work_queue.py show
# 然後：WP-FHS-11 的 9-cell bounded 矩陣，以 WP-17 樹為模板
#   cd /c/wg/queue/WP-FHS-11 && python tools/build_cells.py   # 先看它要求什麼
```

**不要做的事**：不要把 bounded 改叫 native；不要為了讓 gate 變綠去手改 `TODO.md`；不要給驗收員私鑰。

---

## 六、自研究／自學習／自迭代

三條這輪學到、已寫進工具與測試的規則：

1. **失敗碼命名的對象，必須是真正失敗的對象。** 三次「臂壞了」實際上是「寫根」「relay base」「nonce 契約」。
2. **判據要落成欄位，不能靠缺席推斷。** `required_arm`、`durable_gates`、`guard_record`、`round_seed` 都是為此。
3. **一個永遠會說「不」的門禁，和一個永遠說「是」的門禁一樣壞。** 副本保真度檢查第一版比對絕對路徑，
   對逐位元相同的副本報 962 筆差異——現在比對相對路徑。

（另有兩條屬於「我自己的錯」而非系統缺陷：把 `--relay-base` 當樣板複製；把 WP-17 的 docstring 當成檔案存在。
兩者都已更正並留下痕跡。）
