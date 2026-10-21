# FAR synthesis — FAR-20261015-010-r6r7-closure-and-r7-slice

## Route decision
- task_class `RESEARCH_LITERATURE_REPO` → primary `fabric-autoresearch-native`，reason `FAR_ROUTE_NATIVE_ARIS`，
  challenger `aris` / method `research-review`（challenge_required=True）。
- FAR router 依 FAR_CAPABILITY_MATRIX.yaml 決定路徑；本 run 不新增第二套流程。

## Adjudication (verdict PARTIAL)
1. **必須現在工程化（P0）**：R7-02 validator hardening（M04/M06/M16 必拒收）與 R7-03 checker 檔案系統層隔離。
   兩者共通的性質是「一旦缺失，之後所有驗收都可能建立在假綠與被污染的證據上」，因此優先於任何分母工作。
2. **人力閘門（不可自動化）**：Fresh G1、DOC-05 effect Admission、AO、Release。
3. **分母工作需先簽核適用性**：221 / G-A..G-H / AUD-24 / trace 圖譜；先 applicable vs lawful N/A，再抽樣真跑，最後全量。
4. **文件與政策缺陷**：KP `*-R04` 極性（已隔離）、source #6 裁決、94>60 維持 warning。
5. **工具鏈缺陷記錄**：HGK taskspec id 尾段碰撞＋ambient cwd、dispatcher nonce 通道。

## Answers to the three questions
- Q1 未閉合項：見 `CandidateResearch.yaml` 的 P0 / human-gate / sequenced / doc-fix 四類，每項附成本、風險與最小修補。
- Q2 R7：**開跑，但只有 R7-0 = R7-02 + R7-03**；其餘立 TaskSpec 不本輪執行。
- Q3 三個 workspace-only 收據：**必須進 REPO**，但以**新前綴**發布（`EVIDENCE/CNV-PIPD-LS-SP-20261015-R7/`），
  已合併的封存不回寫，維持 main 上 581 blob 的 byte-stability 與既有外部讀回的有效性。

## Rejected alternatives
見 `RejectedAlternativeLedger.tsv`（回寫舊前綴、建第二控制平面、221 全跑、maker 自簽、以 lane 名稱代替隔離）。

## Confidence and limits
- 高信心：P0 兩項的必要性與最小修補形狀（直接由 R6 原始碼與 EIA 裁決交叉得出）。
- 中信心：適用性簽核的格式與 owner 指派（列 OpenQuestion OQ-01）。
- 本 run 的輸出是 **CandidateResearch / ProposedEvolution**，不是接受、不是 promotion。
