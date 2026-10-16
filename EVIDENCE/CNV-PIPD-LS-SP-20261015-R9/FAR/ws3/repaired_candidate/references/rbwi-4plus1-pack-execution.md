# RBWI 4+1 PACK 實跑執行／續跑（TW-ICT RBWI v3.0.0 r2）

> 建立 2026-08-20（Gate-0 完成、看板停在 K6、Q2–Q4 需 HITL + 真實市場時段）。
> 任何 resume 此 run 的 session 先讀本檔，再讀 pack 檔本身。

## Pack 位置與拓撲

- Pack root: `知識庫\實作相關DOC\SQS-THC\實作方案、評估\SQS實跑規劃\RBWI_NATIVE_TIME_SEGMENT_4_PLUS_1_PACK_v2026.08.14-r2\`
- 拓撲：1 Master + 4 qualification overlays + 4 thin prompts = 9 MD，**0 第五 prompt**（第五 prompt 禁止 — Master 自己做 final E2E）。
- `PACK_R2_BUILD_MANIFEST.json` 內含每檔 bytes/lines/sha256/static_checks（全 true, failures=[]）。
- Blueprint: 同目錄上一層 `RBWI_NATIVE_TIME_SEGMENT_4_PLUS_1_藍圖_v2026.08.14-r2.md` sha256 `e8462c2a…`。
- Master: `TW_ICT_RBWI_FULL_RUN_MASTER_EXECUTION_OVERLAY_4PLUS1_2026-08-14_r2.md` sha256 `345e150f…`（與 manifest 一致，已驗）。
- Canonical RBWI: `知識庫\SQS-THC & TW-ICT_FSDT-Stack_SSOT\TW-ICT_RBWI_v3.0.0_r2_2026-07-30.md`
  sha256 `a94b2ec00cf4ae9d24f77bb548e799ffac7fad3eb0e84198129e131121a74c0e`（10,269 行）。
- pack 靜態檢查：9/9 MD、SHA256SUMS.txt 全 OK、fences 成對。

## Gate-0（2026-08-20 已完成）

- 13 receipts 已生成於 **`SQS-THC\evidence\rbwi-fullrun\`**（primary home，Step 6B）：
  AUTHORITY_INVENTORY / MACHINE_STATE / HGK_HEALTH / SQS_TESTS(stdout+exitcode) /
  DATASET_INVENTORY / RBWI_SUBJECT_MANIFEST / FAR_RUNTIME / FDA_XQ_SUBJECT /
  XQ_ACCOUNT_MODE / GSTACK_OPENSPEC_STATE / REQUIRED_CAPABILITY_PREFLIGHT /
  RECEIPT_CROSSWALK.tsv / GATE0_RECEIPTS_SUMMARY.json。
- 生成器：`SQS-THC\var\rbwi-fullrun\gate0_baseline.py`（可重跑；idempotent 覆寫）。
- Gate-0 判語：`G0_PASS_CONDITIONAL_Q2Q4_PENDING_LIVE_SESSION`（Q2–Q4 需 live 市場時段）。
- BASELINE_SQS_TESTS: 231 tests OK（1.07s, Python311 fallback, PYTHONPATH=src）。
- 日線層狀態：DSV-DAILY-2026-08-13-r2（258 TWSE symbols、221,349 rows、
  TWSE_STOCK_DAY、2023-01-03..2026-08-13、external r4 GRANTED
  `DAILY_OHLCV_LOCAL_BACKTEST_DATA_LAYER_PASS`）；backtest.duckdb → daily_bars；
  asof/known_at 為 duckdb 保留字需引號；cron d0d31ffedd07 每日 20:00 增量更新。

## 既有 Spine / 看板狀態（續跑基準，勿重複 admission）

- Spine: **WO-RBWI-FULLRUN-001 已存在** — state=CREATED, writer=codex,
  rollback_pointer=RB-WO-RBWI-FULLRUN-001, created 2026-08-14T02:29Z。
  續跑 = resume，**不可再 create 同名 WO**。
- 注意 spine `checkpoints` 表 schema：`(checkpoint_id, wave, state_digest, source_digest,
  repo_head, rollback_pointer, created_at)` — **沒有 segment_id**。
  RBWI segment checkpoint 是檔案 artifact（SEGMENT_DENOMINATOR_<Qx>.tsv + RBWI_CHECKPOINTS/），
  不是 spine row。查 RBWI checkpoint 別查這張表。
- Kanban board `rbwi-fullrun-2026-08-14`（08-14 10:36 建）：K1–K5 done、K2b done、
  **K0 admission + K6–K9 ready**（K0/K6 的 claim 過期 reclaimed — resume 時先 claim）。
  K6 = FDA XQ/XS 盤前準備（前次 session 死在這裡，claim stale）。
  `hermes kanban show <task_id>` 可看 event/run/result 歷史。
- 前次 08-14 K1–K5 產出（續跑前先 re-read 磁碟驗 survival，勿只信 board result）：
  K2 D-00~D-08 全 PASS candidate 131/258；K3 回測 analyzed=131 qualified=22 wait=57
  rejected=52；K5 Codex 修 3 檔/12 gates/101 objects/231 tests。

## Segment 契約摘要（4+1 執行順序）

| Seg | SF 範圍 | 時鐘 | 可執行時機 | Exit |
|---|---|---|---|---|
| Q1 CONTEXT_PREOPEN | SF-01→02→03 | SIM_BACKTEST_CLOCK | **任何時間**（歷史回測） | Q1_SEGMENT_PASS_AND_FROZEN |
| Q2 OPENING_S1 | SF-04→05→06 +15/17(+11 if pos) | XQ_PAPER_RUNTIME_CLOCK | **live 市場時段 + FDA + HITL** | Q2_SEGMENT_PASS_AND_FROZEN |
| Q3 MIDDAY_S2 | SF-07→10 +11/15/17 | XQ_PAPER_RUNTIME_CLOCK | live 時段；S2 必須 fresh 不得 reuse S1 | Q3_SEGMENT_PASS_AND_FROZEN |
| Q4 CLOSE_POSTMARKET | SF-12→13→14 +11/15/17 | 雙時鐘 | live 收盤/盤後 | Q4_SEGMENT_PASS_AND_FROZEN |
| Final | SF-16 preflight→SF-00..14 | 單調 sim 鐘 | Q1–Q4 全 frozen 後 Master 啟動 | FINAL_E2E |

- Q1 產出：WeeklyContextPackage / DailyRunExecutionPackage / PlanSnapshot /
  SessionCandidatePool-S1 / BacktestRunReceipt（欄位見 overlay §5）/ FAR_RUN_RECEIPT /
  METHOD_ACTUAL_USE_RECEIPTS。Q1 需跑 FAR R0–R8 + 一個 justified Swarm fan-out +
  gstack plan-eng-review + 至少一個 certified slice。
- 每 segment 都要 `SEGMENT_DENOMINATOR_<Qx>.tsv`（從 RBWI_EXECUTION_DENOMINATOR.tsv 投影，
  digest 必綁 checkpoint）；Qx PASS 條件 = subset denominator 100% terminal + 無 orphan。
- **Q1 是唯一今晚/離線即可完整執行的 segment**；Q2–Q4 缺 live 市場時段即 BLOCK。

## HITL 事實（COV-11-06 不能自我批准）

- Pack §0.1 approval `HITL-PACK-R2-20260814T1507+0800` 只蓋 **documentation/construction
  landing**，`financial_side_effect_authority: NOT_GRANTED` — 不構成任何金融 side-effect 授權。
- Q2–Q4 金融動作必須使用 Master §8 `HITL-APPROVAL/1`（approver known + candidate/policy hash
  匹配 + account_mode=PAPER_ONLY + 未過期 + scope 相符）；`HITL_APPROVAL_RECEIPTS/<id>` 為憑。
- FDA route `ROUTE-SQS-XQ-GLOBALWINNER-001`（owner=SQS, **ACTIVE**, expires 2026-12-31,
  binding WO-SQS-FDA-XQ-ROUTE-001 + `SQS-THC\adapters\fda-xq-globalwinner-route.yaml`）：
  action_classes = XQ_LAUNCH_LOCATE / XQ_PAPER_CONFIG / XQ_LOG_EXPORT_READBACK /
  XS_COMPILE_PASS / XS_COMPILE_FAIL_READBACK；**ACTIVE_POSITION 需 HUMAN_ENTRY_APPROVAL**。
  此 route 滿足 FDA guardrail 條件 2（已登記受治理路由），Q2–Q4 的設定/唯讀 XQ 操作可走；
  進場（entry）仍需 user 明確批准。
- 2026-08-20 20:23 台北時間：XQ 未啟動、台股已收盤（13:30）→ 本日 Q2–Q4 不可執行；
  下一工作日 09:00–13:30 窗口 + 每動作 HITL 批准後方可續跑。

## 工具 / 方法 facts

- codex: `%LOCALAPPDATA%\HG-KSEOS\runtime\codex-0.147.0-alpha.6.5\codex.exe` → `codex-cli 0.147.0-alpha.6.5`
  （verified）。lane config: `HG-KSEOS\config\hermes-codex-lane.json`（ACTIVE_FAIL_CLOSED,
  credential_env=OPENCODE_GO_API_KEY, hermes_codex_home=`%LOCALAPPDATA%\HG-KSEOS\codex-hermes`）。
  opencodex daemon port 10101 並非常駐 — **on-demand（StartOpenCodex→Hermes）為藍圖設計，
  勿啟動常駐 daemon**。
- gstack / openspec **不是獨立 CLI**（`gstack --version` 不存在）。方法 registry =
  `HG-KSEOS\src\hg_kseos\named_methods.py`：openspec `CERTIFIED_ACTIVE_BROWNFIELD`、
  gstack.* `CERTIFIED_ACTIVE_SELECTED_SLICES`（plan-eng-review / review / qa / security…）。
  route check = 讀 registry 後記錄 `selected_route/reason_code`（本 run 為 NATIVE/
  HGK_HERMES_ORCHESTRATES_DIRECTLY）；**lane ≠ execution method** — Kanban/Swarm/Codex
  surfaces 仍全開。
- FDA assets（reuse-first）：`Fabric\fabric-desktop-automation\`（fda_router.py /
  fda_preflight.py / screen_state_check.py / FDA_DESKTOP_CAPABILITY_MATRIX.yaml /
  FDA_ASSET_REGISTRY.json）；SQS 端：`SQS-THC\adapters\fda-xq-globalwinner-route.yaml`。
- SQS profiles 已存在：`SQS-THC\agents\profiles\{sqs-orchestrator,sqs-data-analysis,sqs-risk}`。

## Windows / Python 陷阱（Gate-0 生成實證）

- **subprocess text=True + 非 UTF-8 輸出 → UnicodeDecodeError**（thread reader crash、
  stdout=None）：git-bash 下 `tasklist` / `codex --version` 輸出為 ANSI/MBCS。修法：
  `subprocess.run(cmd, capture_output=True, text=True, errors="replace", encoding="mbcs")`
  （把 `encoding="mbcs"` 與 `errors="replace"` 一起包進 helper，全部呼叫共用）。
- **importlib 載入 hg_kseos.named_methods（或任何 by-path module）必須先註冊 sys.modules**：
  `nm = module_from_spec(spec); sys.modules["named_methods"] = nm; spec.loader.exec_module(nm)`
  否則 dataclass 裝飾器報 `AttributeError: 'NoneType' object has no attribute '__dict__'`。
- HGK venv python 呼叫一律用引號反斜線路徑 `".venv\Scripts\python.exe"`（SKILL.md §Step 0
  既有 note，實測仍成立）；MSYS 正斜線形式會觸發 lifecycle guard crash。
- HGK doctor 標準：`PYTHONPATH="C:\Projects\Agent_Workspace\HG-KSEOS\src" ".venv\Scripts\python.exe"
  -m hg_kseos --root "C:\Projects\Agent_Workspace\HG-KSEOS" doctor` → verdict PASS。
- `hermes kanban boards switch <slug>` 後 `hermes kanban list` 才顯示該 board 卡片；
  檢查 task 細節用 `hermes kanban show <task_id>`（events/runs/result）。

## 「已成日期」模擬時鐘最快加速度 + 任意日期參數化補跑（verified 2026-08-21）

適用：Q2–Q4 在當日 live 時窗對不上（無 FDA/HITL/live session）時，使用者裁決以
「已成日期（如 8/20）模擬時鐘」補跑。執行器可支援任一 8 月交易日。

- **執行器**：`SQS-THC/var/rbwi-fullrun/q234_engine.py`（date-parameterized）；
  另有 `q234_executor.py`（8/20 單日版）。`python q234_engine.py <YYYY-MM-DD>` 跑單日，
  `python q234_engine.py all` 跑 8/1–8/20 全月（14 交易日）。
- **最快加速度語義**：已成日期直接跳至當日完整資料一次算完（無即時 tick），換取模擬效率；
  每份收據 `sim_clock.mode = SIM_FASTEST_ACCEL` 標記。
- **decisions**：任何此類 scope 改變**先** freeze `USER_DECISION_<topic>_<date>-001.md`
  （hash 綁進 REQ source_locator），明列 claim ceiling（SIM only / 禁 production / live PENDING）。
- **誠實 proxy 界線**：daily-based 決策鏈真實計算；intraday / XQ market-watch / PAPER-fill =
  `qualification-proxy`，**不假造成交**；HUMAN_ENTRY_APPROVAL 未 mint → 全 `NO_TRADE`/`PENDING_HITL`、
  `filled==0`、`broker_write==False`。
- **資料前置**：daily 層 max 若 < 目標日，需 force-refetch 該月（`var/rbwi-fullrun/force_aug_daily.py`
  失效該月收據→重抓→rebuild core+duckdb）。minute 層常態落後（8/10、50 sym）→ 盤中標 proxy。
- **8/1–8/20 全月補跑（2026-08-21 verified）**：14 交易日 × Q2/Q3/Q4 = 42 收據，
  52/52 functional checks PASS，AO VERIFY_ONLY `PASS-with-observation`（非宣稱驗證零越界），
  單一 Evidence MD `RBWI_Q234_820_SIMCLOCK_SINGLE_EVIDENCE.md` 三 root byte-identical。
- **陷阱**：duckdb `asof` 為保留字需引號；`.venv-data` 基底直譯器壞需用 Python311 + PYTHONPATH=site-packages；
  依賴 polars to_dicts 的 json.dumps 需 `default=_ser` 處理 date 序列化。

## 續跑 SOP（下一 session）

1. 重讀本檔 + Master overlay（34021→33467 bytes 版本與 manifest 一致）。
2. 基線 readback（SKILL.md Step 0）+ 讀 `SQS-THC\evidence\rbwi-fullrun\` receipts 確認仍在。
3. `hermes kanban boards switch rbwi-fullrun-2026-08-14` → claim K0/K6（stale claims 先 reclaim）。
4. 完成 Q1（SIM 時鐘，離線可跑）：分母投影 → FAR R0-R8 → backtest qualification →
   Swarm fan-out → gstack slice → Codex（若 durable repair）→ Q1 checkpoint freeze。
5. 到 Q2 gate 停：呈報用戶需（a）下一交易日 live 窗口（b）每金融動作 HITL-APPROVAL/1
   （entry 尤其 HUMAN_ENTRY_APPROVAL）。不得自我批准、不得假造 Q2–Q4 執行結果。
6. Final：Q1–Q4 全 frozen → Master dependency revalidation → final clean E2E →
   SQS data/domain/risk checker → fresh AcceptanceOfficer VERIFY_ONLY → 單一 evidence MD
   （primary home `SQS-THC\evidence\rbwi-fullrun\` + 三 root 鏡像 byte-identical）。

## FAR 根因教訓（2026-08-21 用戶 challenge 後補強）

- **「無 live 窗 + 建倉需 HITL」≠「不可用 FDA/XQ」**。前次誤讀成整段跳過 FDA，靜默以日線 SIM 頂替，
  被用戶 challenge「這是實跑卻沒開 XQ」。真解：FDA 條件 2 有 ACTIVE 已登記路由
  （ROUTE-SQS-XQ-GLOBALWINNER-001：XQ_LAUNCH_LOCATE/XQ_PAPER_CONFIG/XQ_LOG_EXPORT_READBACK/
  XS_COMPILE_PASS/XS_COMPILE_FAIL_READBACK），preflight 要帶 `--route-id` 才 PASS；XQ 已安裝可跑
  （`C:\SysJust\XQLite\daqxqlite.exe`, fingerprint 收據）。非建倉 XQ 桌面 op 應以條件 2 執行；
  **建倉才需條件 3 逐筆 HITL**。
- **實跑 ≠ 精簡決策鏈**。canonical RBWI SF-00..17（18 JobCards）+ Spartoi SF-00..31 每卡有 Required
  Outputs/Artifacts（analysis/bias/劇本/各級股池/位置/HITL/封存）。只做 thin 決策鏈 = 0/18 完整，
  大量 PARTIAL/MISSING（前次 SF-05/09/10/11/14 MISSING）。**每 JobCard 逐一產出 canonical outputs**。
- 全量補齊實現：`SQS-THC\var\rbwi-fullrun\full_jobcard_executor.py`（SF-00..17, 18 收據）+ Spartoi
  `full_intraday_supplement.py`（SF-04..12）。自檢 `check_full_jobcards.py`（108/108）。盤中段仍標
  `qualification-proxy`（SIM），不宣稱成交。
- FDA preflight `no_authorization` 是「沒帶 route-id」的誤判，不是「不能碰 FDA」。解法見
  `references/fda-guardrail-operations.md` / `FDA_ROUTE_REGISTRY.json`。

## 8/20（及全 8 月）模擬時鐘補跑（2026-08-21 實證）

當 Q2–Q4 live 時窗對不上（開盤窗已過 / 無 FDA token / XQ 未跑 / 無 HITL entry）且 user 授權
「以已成日期最快加速度」補跑（USER_DECISION_RBWI_Q234_0820_SIMCLOCK_2026-08-21-001）時：

- **引擎**: `SQS-THC\var\rbwi-fullrun\q234_engine.py` — date-parameterized，`python q234_engine.py <date|all>`。
  Spartoi 日級同理：`var\spartoi-preopen\spartoi_day_engine.py`（SF-02/03/13/14 per-day）。
- **fastest-acceleration 語義**: 這些日期已發生 → 模擬**直接跳到當日完整資料一次算完**，無即時 tick；
  sim_clock.mode=`SIM_FASTEST_ACCEL`。這正是 user 要的「不以正常時間流逝速度」效率。
- **任意日期**: 引擎掃 backtest.duckdb 內 `2026-08-01..08-31` 全部交易日（08-03..08-20 = 14 日）；
  日線資料需先強制重抓 8 月（`var\rbwi-fullrun\force_aug_daily.py`，因增量更新被「8 月月度收據已匹配」擋住
  → 失效化 8 月 artifact+receipt 再 re-run），新 DSV-DAILY-2026-08-21-r1。
- **誠實界線**: filled=0 / broker_write=false / 盤中/XQ/market-watch/paper-fill = **qualification-proxy**；
  Q2 order_intent 全 NO_TRADE（HUMAN_ENTRY_APPROVAL 未 mint）；live 維持 PENDING（COV-11-06 不可自批）。
- **結果**: 14 日 × Q2/Q3/Q4 = 42 收據（RBWI）+ Spartoi dayflow 98 artifacts，全 `SEGMENT_PASS_AND_FROZEN_SIM`。
- **驗證**: `check_q234_corpus.py`（52/52）、`check_spartoi_aug_corpus.py`（129/129）、fresh AO PASS-with-observation、
  單一 MD `RBWI_Q234_820_SIMCLOCK_SINGLE_EVIDENCE.md` 三 root byte-identical。
- **陷阱**: daily_bars 欄位是 `date`（`asof` 為 duckdb 保留字需引號）；8/11,8/13 真實為 162 rows（一檔缺）。

## Q1 完成狀態（2026-08-20 晚間，本 session 執行）

- Q1 = BIND-RBWI-Q1-20260820-001（BIND-RBWI-Q1 下同）：**Q1_SEGMENT_PASS_PREOPEN_100PCT**。
  SEGMENT_DENOMINATOR_Q1_CONTEXT_PREOPEN.tsv digest=81175b24…（37 rows, 0 orphan, 150 global）。
- **開盤前工作事項 100% 覆蓋（canonical RBWI §11/§12 逐項）**：`evidence\rbwi-fullrun\PREOPEN_WORKING\`
  有 W-00..W-08（週層級 9 步）+ D-00..D-09（日層級 10 步）+ SF-16/SF-00/SF-17（3 modules）
  = **22 receipts + 25/25 coverage（含既有 SF-01/02/03）**。每份有 schema/title/owner/checker/
  veto/action/inputs/outputs/state_machine 實質欄位。RBWI_PREOPEN_100PCT_COVERAGE_CHECK.json
  與 RBWI_PREOPEN_COVERAGE_MANIFEST.json 為覆蓋證明。D-09 試撮 live part 標
  PREPARED_PENDING_LIVE（需 Q2/XQ 窗口）——開盤前 admission 已凍結，live 觀察屬 Q2。
- receipts 於 `SQS-THC\evidence\rbwi-fullrun\`：sf-01/02/03-receipt.json、
  BACKTEST_RUN_RECEIPTS/BACKTEST_RUN_RECEIPT_Q1.json（PIT PASS + deterministic=True +
  walk-forward IS/OOS + TWSE fee/tax/slippage model）、FAR_RUN_RECEIPT.json（R0-R8 應用）、
  RBWI_METHOD_ACTUAL_USE_LEDGER.tsv（kanban/swarm/gstack/openspec/codex 7 rows）、
  RBWI_CHECKPOINTS/Q1_SEGMENT_CHECKPOINT.json（SEGMENT_PASS + preopen_coverage 100 綁定）。
- 4 個 segment bindings 已物化：`evidence\rbwi-fullrun\RBWI_SEGMENT_BINDINGS\BIND-RBWI-Q{1..4}-20260820-001.json`
  （同 parent WO=WO-RBWI-FULLRUN-001 / board=rbwi-fullrun-2026-08-14）；RUN_LEDGER.jsonl append。
- SF-03 分層（daily-layer proxy）：PRIMARY=138 / EXCLUDE=120（liquidity_below_floor），
  **不含 OBSERVE/SECONDARY**（daily 代理無 pre-open 試撮資料 — Q2 用 live pre-open 資料）。
- Swarm 雙 lane readback（deleg_5ce69ab4, 2026-08-20 20:35 UTC+8 啟動）：HGK lane 驗
  denominator crosswalk 150/37 子集精確 + checkpoint 欄位；SQS lane 重算 duckdb PIT/
  row/symbol/tier 與 receipt 比對。AO fresh-context lane（deleg_8ba4af8b）**PASS** 7 items
  + 2 nonclaims（NO-LIVE-WRITE + Q2-Q4 未假造）。開盤前 100% 覆蓋另有 fresh verify lane
  （deleg_2519fb9c）。單一 evidence MD（RBWI_PACK_Q1_SEGMENT_SINGLE_EVIDENCE.md, sha256
  dcd237ce…）已 53 artifacts × 3 roots byte-identical 鏡像。
- **PIT 檢查語義陷阱（本 session 實證）**：daily 層 canonical 語義是 `known_at == asof + 1d`
  （T+1 才知日線），違規 = `known_at <= asof`（且結構性 `known_at != asof+1d` 也算違規，
  check_daily C10/C11 同定義）。**不要用 minute 層的 `known_at > asof` 當 leak 檢查** —
  會得到全表違規的假 FAIL（本 session 第一次跑 PIT_bad=221349 即此誤判）。

## Q2–Q4 SIM-clock 補跑（2026-08-21 上午，USER_DECISION_RBWI_Q234_0820_SIMCLOCK_2026-08-21-001）

- 用戶裁決：Q2–Q4 無法 live 時窗執行時，改以 **8/20（及全 8 月）模擬時鐘**補跑（fastest-accel）。
- Executor：`var/rbwi-fullrun/q234_engine.py`（date-parameterized）+ `q234_executor.py`（8/20 單日）。
- 產出：42 sim receipts（14 交易日 × Q2/Q3/Q4）+ 9 checkpoints（SIM）+ denominators FINAL_SIM +
  AO/Codex/FINAL checkers + `RBWI_Q234_820_SIMCLOCK_SINGLE_EVIDENCE.md`；`check_q234_corpus.py` 52/52 PASS。
- **Claim ceiling**：`LOCAL_PAPER_SIMULATION_ONLY`；filled==0、broker_write==False、
  HUMAN_ENTRY_APPROVAL 未 mint → 全部 NO_TRADE/PENDING_HITL；live XQ+PAPER 維持 PENDING
  （live 段仍待下交易日開盤窗 + 逐筆 HUMAN_ENTRY_APPROVAL，COV-11-06 不可自批）。
- Resume token：`RESUME:RBWI_Q234_820_SIMCLOCK_FROZEN`。

## Mirror pitfall（2026-08-21 更新，self-repair receipt RBWI_SELF_REPAIR_MIRROR_GAP_2026-08-21-001）

- **mirror「byte-identical」claim 必須 fresh re-verify，不能只信 session 自報**——上午 session 宣稱
  「mirror 3-root byte-identical」，但實體 primary 112 artifacts、roots 只鏡了先前 snapshot，
  **後續 append 的 57 檔（42 SIM receipts + 9 checkpoints + AO/Codex/FINAL checkers +
  USER_DECISION + SWARM/ROUTE receipts）從未鏡到 roots**，`RBWI_RUN_LEDGER.jsonl` 亦 stale。
  已用 fresh scan 偵測並 re-mirror 全 112 → 三 root byte-identical。
  **Step 6B PRIMARY-HOME GATE 反向也成立**：每次新增 evidence 到 primary 後，須重跑 mirror
  而非假設已鏡。驗證方式：
  `for each r in roots: identical==primary_count and missing==0`。
