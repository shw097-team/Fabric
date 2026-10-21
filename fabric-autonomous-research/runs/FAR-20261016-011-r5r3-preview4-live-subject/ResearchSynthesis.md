# FAR synthesis — FAR-20261016-011-r5r3-preview4-live-subject

## Route decision
- task_class `RESEARCH_LITERATURE_REPO` → primary `fabric-autoresearch-native`，reason `FAR_ROUTE_NATIVE_ARIS`，
  challenger `aris` / method `research-review`（`challenge_required=True`）。
- 路徑由 FAR router（`governance/FAR_CAPABILITY_MATRIX.yaml`）決定，未新增第二套流程。

## Adjudication (verdict: PARTIAL — S4_PREVIEW_MVP_PHASE_TEMP_CLOSED 可對 preview.4 這個受驗主體宣告，但 release/main 漂移與 OQ-01 保留給 Owner)
1. **delta-only 下唯一仍成立的 CONFIRMED_DEFECT**：install 路線與 release 身分不一致
   （README 的私人 Plugin 路線指向已被取代的 68,355/`2f9ae0…` evidence-branch ZIP，
   而 release 供應 68,357/`545e359a…`；`docs/install/README.md` 指向不存在的 `RELEASE_TUPLE_v0.1.1-preview.4.json` asset；
   `docs/RELEASE_TUPLE.json` 無 preview.4 條目 → repo 內完全沒有 served 身分紀錄）。
   本輪以 docs/metadata + 一個 derived guard 修補，並保留 R5Y 歷史段落（加註 superseded）。
2. **不受本輪影響者**：D1/D2/TYPE5 在 main 上 22/22 PASS；served assets 與 SHA256SUMS 6/6 一致；
   ZIP 單一 root/8 skills/CRC 全通過。故 R5 裁決所列 P1/P2 缺陷已落地且可重驗。
3. **release/main 漂移**：served wheel 對 `Do task A.Task B must run.` 產生 1 個 atom（main 產生 2 個）。
   差異可精確歸因於 PR #13（R5R2）在 preview.4 發布**之後**才進 main。是否為此切新版本屬 **Release Owner**（OQ-01），
   本輪**不**自行切 tag（RA-02）。
4. **人力閘門**：私人帳號 Upload/Install smoke（OQ-02）、公開 Directory / Production（`NOT_GRANTED`）。
5. **工具鏈**：HG-KSEOS `check_drift` 的 `codex_sha256` DRIFT_VALUE 為投影期望過時（config 值＝實測 `E98C516F…`），
   registry 修正需 WorkOrder（OQ-03）。

## Answers
- Q1 仍存偏離：僅「install 路線/release 身分」一項，本輪已修；其餘為 Owner 閘門或已登記的後續 change set。
- Q2 是否切新 immutable release：**是者屬 Owner**；本輪提供封版所需全部可驗輸入（tag 身分、served digests、漂移量測）。
- Q3 發佈形狀：**新分支＋PR**，不回寫已合併的 preview.4 tag/tree 與其 7 個 assets。

## Claim ceiling
本 run 為 local/candidate-only 研究產物；`PASS_CHALLENGE`/`ACCEPTANCE`/`RELEASE` 皆不在本 run 的宣稱範圍。