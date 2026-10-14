# EVIDENCE/skill-convergence-20261014 — round record for external planners

> 本目錄是本回合（`SKILL-CONVERGENCE-20261014`）的**結案證據投影**，供外部工程師在本 repo 內参
> 照與規劃升級。它是**投影**，不是 authority：唯一控制平面是 `HG-KSEOS`。
>
> `NOT_EXTERNALLY_ACCEPTED · NOT_MERGED · NOT_RELEASED · NOT_PRODUCTION · NO_LIVE_WORLD_EFFECT`

## 這回合做了什麼（一句話）

在既有 Fabric 治理契約下，以 HG-KSEOS 為唯一控制平面、current canonical Hermes 為受治理
Runtime／Orchestration Plane，對 canonical Hermes 的兩個近硬限入口 skill 做**無損抽取＋主題 references
整併＋既有 consumer 複用**，建立回退點與收斂不變式，並以獨立車道（advisory）查核；全程
**candidate-only**。

## 這裡有什麼

| 文件 | 內容／可信度 |
|---|---|
| `ROUND-CLOSURE.md` | 結案主文：交付項、逐項天花板、殘留缺口 R1–R7、失敗紀錄、續作指示 |
| `FAR-CLOSURE-REPORT.md` | FAR 裁決＋低阻力執行方案（本回合實際執行的那一份） |
| `INDEPENDENT-CHECK-VERDICT.md` | 結案複核車道的 **advisory** verdict，加上我方對其主張的**獨立重算**（不採信自述） |
| `SECURITY-CHECK.md` | 安全車道 verdict 的逐位元疑點裁決（從該回合自身紀錄重算） |
| `PUBLICATION-RECORD.md` | 發布紀錄：完整回傳包（現址為本 repo 的分支）與本 mirror 的策展投影 |
| `APPROVAL-LIST.md` | 本 change-set 的變更清單與審核依據（mirror §4.5 要求） |
| `closure_manifest.json` | 結案依據 artifact → sha256 對照（可由隨附腳本重生） |
| `*.json` | 機器收據：verdict 裁決、看板結案回讀、收斂／回退檢查 |

## 讀者最需要先知道的四件事（不得讀成完成）

1. **全部 verdict 都是 advisory**，不是 acceptance；`WARN_LANE_CREDENTIAL_POSTURE_INCONCLUSIVE`
   為 inconclusive，**非 pass**。
2. **canonical 未被寫入**：canonical skill 未 apply、未 promote；控制平面分派器的逾時缺陷**只有候選補丁**。
3. **失敗紀錄完整保留**：本回合有 12 次逾時、2 次無 nonce、1 次污染、1 次空答案的車道派送失敗，
   逐項列於 `ROUND-CLOSURE.md`；沒有任何一項被洗成 PASS。
4. **references 檔數仍是 94**（`references/` 90 ＋ `references/topics/` 4），高於 linter 的 60 檔
   警告線 34 檔；本回合只完成一個 14 檔試點群。

## 完整證據在哪裡

本目錄是**策展投影**（mirror 排除 raw stores）。完整回傳包（638 檔：全部 lane 逐字稿、brief、harness、
manifest、結案集）在**本 repo 的分支** `evidence/skill-convergence-20261014-full-packet` 之
`EVIDENCE/skill-convergence-20261014-full-packet/SKILL_CONVERGENCE_RETURN_20261014/`，可免憑證 clone 並重跑
驗收命令。該分支的 `BRANCH-NOTE.md` 說明它為何放在分支上、推送前做過哪些檢查，以及 Windows 長路徑注意事項。

> **落點更正（2026-10-14）**：此回傳包最初被推到 `shw097-team/PIPD-LS-SP`（分支
> `feat/skill-convergence-return-20261014`，tip `e8997254…`）。owner 指出本回合的落點應為 Fabric repo，
> 故已改發佈於本 repo 的上述分支，並**刪除** PIPD-LS-SP 上的該分支（該 repo 的 `main` 全程未動，
> 仍為 `f4021ae`）。此為本回合第二次落點更正，事件本身記於
> `INTEGRATION/KNOWN-FINDINGS.md` 的 K-20。

## 重現

```bash
git clone --depth 1 --branch evidence/skill-convergence-20261014-full-packet \
  https://github.com/shw097-team/Fabric.git
cd Fabric/EVIDENCE/skill-convergence-20261014-full-packet/SKILL_CONVERGENCE_RETURN_20261014
# 依 README.md 的驗收命令執行 → 期待 `files 638 mismatch []` 與 `scan NO_HITS`
```
