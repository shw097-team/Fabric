# U1 調查：`lane_assignment_resync.py` 與 `model-lane-assignment.json` 是不是「模型選單」？

**結論：是既建成的選單／佈線機器，不是「兩份權威對 PLAN 的臂不一致」。我先前那句話是錯的，錯在我用 `sed` 讀到 YAML 裡**非權威**的那一段。**

## 四份文件的實測分工（全部讀自本機 HG-KSEOS）

| 文件 | schema / 身分 | epoch | 自述 | 角色 |
|---|---|---|---|---|
| `config/lane-route-slots.candidate.json` | `HGK-LANE-ROUTE-SLOTS/1`、`LANE_ROUTE_SLOTS_CANDIDATE`、rev 36、`status: CANDIDATE` | **41** | `ordered_pool` 每臂帶 `rank` + `role: DEFAULT/首選`、`FALLBACK1/備援1`…；`selection_semantics`；`identity_overlaps_recorded_not_enforced` | **這就是「模型選單」**：三個車道 × 排名池，`fhs_3lm.py --menu/--bind` 讀它 |
| `config/lane-routing-registry.yaml` | `HGK-LANE-ROUTING-REGISTRY/1` | **41** | `routes[]` 的 PLAN 列 = `openai-codex/gpt-6.1-sol` | 車道→provider/model 的**權威** |
| `config/model-lane-assignment.json` | `HGK-MODEL-LANE-ASSIGNMENT/1`、rev 43（main 為 rev 35） | projected from **40** | `authority_note`：「Operator-declared routing policy. **Not an authority source**; the runtime wiring named in `effective_wiring` is the machine truth.」 | **投影／編碼**，dispatcher 機械路由的輸入 |
| `scripts/lane_assignment_resync.py` | 修補工具 | — | 「make the assignment a projection of the registry」 | 把投影重導回 registry 的**既有工具** |

## 三項決定性量測

1. **選單本身就承認 9 個槽全可用**：`fhs_3lm.py --menu`（`--hgk-root` 指本機 clone）回
   `policy_epoch 41 / IN_FORCE / slot_count 9 / admitted_count 9 / all_admitted true`。
   PLAN 排名池：`1 gpt-6.1-sol（首選）`、`2 deepseek-v4.1-flash`、`3 glm-5.3-flash`、`4 mimo-v2.6-flash`、`5 nvidia/z-ai/glm-5.3-flash`、`6 nvidia/deepseek-ai/deepseek-v4.1-flash`。
2. **投影已經是乾淨的**：在本機 clone 跑 `lane_assignment_resync.py` → **`changes: 0`**。
   （在我以 `origin/main` 切的 worktree 跑同一個工具 → 5 項變更，全部是 `automatic_selection` 的**排序**差異，不是 provider/model 差異：main 是 `chain[1]=gpt-6.1-sol auto=True`，epoch-40 投影是 `chain[0]=gpt-6.1-sol auto=True`。兩邊**都選 gpt-6.1-sol**。）
3. **我先前說的「registry 把 PLAN 指向 deepseek」不成立**：用 `routes[]` 過濾後，PLAN 列就是 `openai-codex/gpt-6.1-sol`。
   我先前的 `sed -n "$(grep -n 'lane: PLAN' …)"` 抓到的是 YAML 內**另一段歷史區塊**，不是權威的 `routes[]` 列。這是我讀法的錯。

## 因此 B5「5 個槽被拒」的真正原因

被拒的四次探針是在 **`origin/main` 衍生的 worktree** 上跑的：那邊是 rev 35、`registry_epoch 34`、`lane_chains` 沒有 epoch-41 的排名池，`lane_assigned_arms()` 只看到主臂 → 其餘被 `ERR_ARM_NOT_IN_ASSIGNMENT` 拒。
**在機器現行的 epoch 41（本機 clone）上，選單 9/9 admitted、投影 0 變更**。所以那不是缺陷，是**對著過期 base 量測**的產物。

## 與 SoD 的關係（owner 指令）

選單自己就寫明：`openai-codex/gpt-6.1-sol appears at PLAN rank 1, VERIFY_SECURITY rank 1 … BY OWNER ORDER … SOD006-C4 (OPEN_OWNER_ORDERED)`，並列在 `identity_overlaps_recorded_not_enforced`。
3LM 綁定記錄也帶 `sod_mandated: false`，VERIFY 綁定時 `same_arm_lanes: true` 只**記錄**、不拒絕。
⇒ 本輪不得把「PLAN 與 VERIFY 同模型」當成不通過的點。

## 已建立的綁定證據（用既有 `--bind`，未改任何設定）

| 車道 | slot | arm | same_arm_lanes | 檔案 |
|---|---|---|---|---|
| PLAN | primary | `openai-codex/gpt-6.1-sol` | false | `evidence/U1_3LM/bind_PLAN.json` |
| EXECUTE | primary | `opencode-go/deepseek-v4.1-flash` | false | `evidence/U1_3LM/bind_EXECUTE.json` |
| VERIFY | primary | `openai-codex/gpt-6.1-sol` | **true（記錄，不拒絕）** | `evidence/U1_3LM/bind_VERIFY.json` |

綁定記錄自身宣告：`plane: LANE_CONTROL_PLANE`、`not_a_session_pin: true`、
「a session pin in the desktop app is a conversation setting and does not bind a lane; this record is the lane binding, and only this record is read by `--assert`」——
這正是「車道平面 ≠ 會話平面」的既有實作。
