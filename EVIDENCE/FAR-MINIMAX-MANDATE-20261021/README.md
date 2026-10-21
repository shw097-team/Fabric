# FAR-MINIMAX-MANDATE-20261021 — 證據包（外部驗收用）

**控制平面**：HG-KSEOS
**業主指令（2026-10-21）**：PLAN、EXECUTE（Codex CLI）、VERIFY/SECURITY（Codex CLI）
**三車道全部**使用 `opencode-go/minimax-m3.1-flash-free`（MiniMax M3.1 Flash, OPENCODE GO）。
**Registry epoch**：24 → 25

> **CLAIM CEILING — 請先讀這段**
> 本證據包證明的是：這條綁定在**本機**被量測過、並由獨立 Acceptance Officer
> 從工件重新推導過。它**不是** acceptance、**不是** release、**不是** merge、
> **不是** promotion。沒有聲稱任何上游 provider 狀態、外部驗收或發布動作。
> 證據包自身的收據也寫明：一個 pass 不是任何標的的 acceptance。

---

## 1. 外部驗收官怎麼驗

1. 取分支 `pub/far-minimax-mandate-20261021`（**不是** `pub/far-lane-remediation-20261021`，
   理由見 `PUBLISH-BRANCH-INCIDENT.md`）。
2. 讀 `PACKET_MANIFEST.json`，對每個 `path` 重算 SHA-256，與 `sha256` 比對。
3. 對 `config/` 下的三個檔案，確認它們與 HG-KSEOS 控制平面的對應檔案位元組相同。
4. 讀 `ao_evidence_bundle.json`：那是 AO 逐項核對過的事實集合。
5. 讀 `FAR-RULING-REPORT.md`：裁決建議，**等待業主確認**。

重算指令（Windows / bash）：

```bash
cd <clone>
python - <<'PY'
import json,hashlib,pathlib
m=json.load(open('EVIDENCE/FAR-MINIMAX-MANDATE-20261021/PACKET_MANIFEST.json',encoding='utf-8'))
base=pathlib.Path('EVIDENCE/FAR-MINIMAX-MANDATE-20261021')
bad=[f['path'] for f in m['files']
     if not (base/f['path']).is_file()
     or hashlib.sha256((base/f['path']).read_bytes()).hexdigest()!=f['sha256']]
print(f"{len(m['files'])-len(bad)}/{len(m['files'])} match, mismatches: {bad}")
PY
```

---

## 2. 檔案導覽

| 檔案 | 內容 |
|---|---|
| `FAR-RULING-REPORT.md` | **本次 FAR 裁決建議全文**（A/B/C/D/E 五組裁決，含實測基線與自揭露） |
| `VAR-DISPOSITION-INDEX.md` | 120 個 `var/` 目錄的逐項分類索引（0 破壞性動作） |
| `OPENSPEC-UNCHECKED-INDEX.md` | 460 個未勾項的索引（0 tick） |
| `SBL-EXCLUSION-NOTE.md` | 與並行 SBL 施工的干擾排除記錄 |
| `PUBLISH-BRANCH-INCIDENT.md` | **發布分支事故記錄**（上一回合誤提交 177 檔 + 本分支被 SBL session 共用） |
| `config/` | 綁定後的三個治理檔案（pool / registry / assignment） |
| `admission-{PLAN,EXECUTE,VERIFY_SECURITY}.json` | 三車道的 HGK admission 收據 |
| `{PLAN,EXECUTE,VERIFY}_admit.json` | 三車道的 dispatcher 收據（`required_arm == served_arm`） |
| `ao_evidence_bundle.json` | AO 核對過的事實集合（epoch / routes / pool / drift / admission / secret scan / SBL） |
| `AO_minimax_binding.json` | AO 車道收據 |
| `apply_minimax_binding.py` | 綁定腳本（冪等、錨點式、跑得完可重現） |
| `apply_assignment_derivation.py` | assignment 推導腳本（chain/row/selector 由 pool 推導，不手寫） |
| `build_var_disposition_index.py` | `var/` 索引腳本（不刪任何東西） |
| `build_openspec_unchecked_index.py` | OpenSpec 索引腳本（不打任何勾） |
| `compare_pytest_isolated.py` | pytest 新舊失敗集比對（在 detached worktree 內跑，不碰工作樹） |
| `admit_minimax_lanes.py` | admission 執行腳本 |
| `create_kanban_board.py` | KANBAN board 建立腳本（17 卡：12 done / 5 blocked 待業主裁決） |
| `openspec-{proposal,tasks,spec-lane-routing}.md` | OpenSpec change（`--strict` valid） |

---

## 3. 三個殘留主題的實測基線（業主引用的數字已過時）

| 主題 | 業主引用 | 實測 | 說明 |
|---|---:|---:|---|
| OpenSpec 未勾項 | 471 | **460** | 471 是估計值；實測 38 active / 34 有未勾 / 460 項 |
| `var/` 頂層目錄 | 114 | **120** | 114 是舊快照；且**不是** 120 個未結案回合（只有 83 個是回合產物） |
| TT ledger `status == OPEN` | 2 | **2** | 一致（`HGK-EBC-TT-001` / `HGK-EBC-TT-002`） |

---

## 4. 模型軸獨立性（必須讓驗收官知情）

業主的模型方案讓**三車道同一個模型**。因此：

- **模型軸獨立性 = 0。**
- 已在 registry 宣告為 `SOD006-C5`（`OPEN_OWNER_ORDERED`），
  並把 `sod_invariants.pairs` 中 `EXECUTE → VERIFY_SECURITY` 的 `distinct_required`
  由 `true` 改為 `false`，**同時記錄了原因**。
- 剩下的分離只有：PROCESS（獨立 Codex-CLI 程序）、LANE（角色不同）、
  EVIDENCE-PATH（checker 從工件重新推導，不讀 writer 的摘要）、
  以及 no-self-acceptance 規則。
- **共享模型家族的相關盲點不被主張為不存在。**
- 舊臂**全部保留**（`gpt-6.1-sol` 仍在 VERIFY 的 operator-selectable 臂），
  所以恢復模型分離不需要重做池綁定。

---

## 5. 本回合**沒有**做的事（自揭露）

- 沒有打任何 OpenSpec 的勾（`ticks_applied_by_this_script = 0`）
- 沒有刪除、搬移或改名任何 `var/` 檔案（`destructive_actions_taken = 0`）
- 沒有變更 TT ledger 的任何狀態
- 沒有改動 canonical Hermes **會話** profile（會話平面與車道平面是兩個平面）
- 沒有寫入 `fabric-autonomous-research/`（並行 SBL 施工）
- 沒有把需要業主裁決的動作（回填 tick、刪除目錄、變更 ledger）自行執行——
  這 5 項在 KANBAN 上是 `blocked` 狀態，明確標記「待業主裁決」

---

## 最終狀態補記（本回合結束時）

**主體提交**：`a1bd583`（HG-KSEOS）
**測量**（隔離 detached worktree，live 工作樹全程未被修改）：

| 腿 | 結果 |
|---|---|
| BEFORE（本回合前的 config + 已提交的測試） | `8 failed, 436 passed, 90 subtests passed` |
| AFTER（epoch 25 config + 修補後的測試） | `8 failed, 436 passed, 90 subtests passed` |
| **本回合引入的新失敗** | **0** |

剩餘 8 個失敗全部**在本回合之前就存在**，且屬另一個 session 的 task-013/014/015 工作範圍
（`test_task013_hermes_v020_closure`、`test_task014_named_method_closure`、
`test_task015_coherence_closure`、`test_hlpe` 2 個、`test_c2_case_run` 1 個）。
**它們不是本回合造成的，本回合也沒有越權去修它們。**

**本回合揭露並修好的治理缺陷**：`check_drift()` 比對的是「registry 的 projections vs 現場」，
**不檢查 registry 自身的 route rows vs pool**。因此 registry 在 pool 與 assignment 都已是
MiniMax 的情況下，仍對外宣告 `gpt-6.1-sol`（PLAN、VERIFY_SECURITY）與
`deepseek-v4.1-flash`（EXECUTE），而 `check_drift()` 仍回 `[]`；另有兩條車道的
`admission_status` 是 `UNPROVEN`，但其 admission 實際已被量測。
已由 `scripts/apply_registry_route_sync.py` 從 pool 重建 15 個欄位修正（重跑 0 變更，冪等）。

**測試 oracle 的根因修補**：stub child 的 usage row 改為**從 dispatcher 傳給它的 `--model`
推導** provider/model —— 被派發的臂就是被回報的臂。硬編模型的 stub 會在每次 pool 重綁時
以「與被測行為無關」的理由失敗。同時 `tests/fixtures/` 整個目錄**納入版控**
（17 個測試引用 `stub_lane_child.py`，但它此前未被 git 追蹤，clean checkout 無法重建測試套件）。

**獨立驗收**：AO 收據見 `probes/AO_FINAL_receipt.json` 與 `probes/AO_FINAL_verdict.json`。
AO 的作業前提是**從提交位元組重新推導**（`git archive a1bd583`），不是讀工作樹。

**殘留裁決（等業主確認，未執行）**：460 個 OpenSpec 未勾項、120 個歷史 `var/` 目錄、
2 筆 TT ledger OPEN —— 全部只建立索引，**0 tick、0 刪除、0 關閉**。

### 獨立 AO 找到的第二層缺陷（已修）

第一輪 AO（`probes/attempt-21612-1792566884-1-stdout.txt`，230KB）在 check 4 找到真實缺陷：
route row 的**頂層** auth posture（`auth` / `oauth` / `reasoning_effort`）是 arm posture 的**第二份副本**，
不在 `arms[]` 裡，所以第一次同步沒有覆蓋到：

```
PLAN            route.auth='openai_oauth' != pool.rank1.auth='env_ref:OPENCODE_GO_API_KEY'
PLAN            route.oauth=True         != pool.rank1.oauth=False
PLAN            route.reasoning_effort='medium' != pool.rank1.reasoning_effort=None
VERIFY_SECURITY （同樣三項）
```

這是治理事實而非格式問題——它會讓外部驗收者誤判 MiniMax 臂是 OAuth 臂（實際是 key-auth 臂）。
已修於 HG-KSEOS `1cbb9d2`；修後 `drift = 0`、重跑 0 變更（冪等）、目標套件 `141 passed / 90 subtests`。

**這是「獨立驗收有價值」的直接證據**：本回合自己的自檢測（drift gate + 測試）全程綠，
獨立 AO 仍從**提交位元組**出發重推，找到內部閘門結構上不可能找到的第二層缺陷。

### 自我研究（`SELF-REVIEW.md` / `SELF-REVIEW.json`）

回顧「這一回合的缺陷是怎麼被找到的」：4 個已修缺陷中，1 個由獨立 AO 找到、2 個由人工跨欄位稽核找到、
1 個由自動化測試套件找到。**活下來的都是自檢測結構上不可能看到的**——
一個事實存兩份，以及一個把「今天 rank-1 是誰」寫死的測試。

誠實的解讀：**綠的 drift gate 加綠的目標測試套件，不是跨欄位一致性的證據**。
它只證明了閘門自己負責的範圍被滿足了。

最高價值的下一步：把 registry-vs-pool 的比對**接進 `check_drift`**，
把「記得去跑的腳本」變成「繞不掉的閘門」。
