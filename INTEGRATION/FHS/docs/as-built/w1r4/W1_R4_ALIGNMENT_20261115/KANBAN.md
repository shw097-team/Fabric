# KANBAN｜W1_R4_ALIGNMENT_20261115

| 卡 | 內容 | 依據 | 狀態 | 收據 |
|---|---|---|---|---|
| R4-01 | 開輪次、KANBAN、工作區 | — | DONE | 本檔 |
| R4-02 | CH-13/14/16/20/39 五章契約抽取（帶行號） | r3 §04／§07、W0 章表 | DONE | `docs/CH_LAYER_SPEC.json` |
| R4-03 | 五張章卡裁判 ＋ POS／NEG | D1 | DONE | `build/ch_ch*.py`、`tests/affected/W1/CH-*/` |
| R4-04 | 七個 VN 增量 | D8a | DONE | `build/vn_referee.py`、`tests/affected/W1/VN-0*/` |
| R4-05 | 24 槽一版決定內容 | D8b | DONE（3 槽 licence HOLD 如實標示） | `out/SLOTS_24_FULL.json`、`tests/affected/W1/SLOTS24/` |
| R4-06 | 四閉環契約 checkpoint／resume／watchdog／budget | D6 | DONE | `build/loop_referee.py`、`tests/affected/W1/LOOP/` |
| R4-07 | gate B2 逐檔 sha256 重算 | D8c | DONE | `out/GATE_W1R4.json` B2 18/18 |
| R4-08 | gate E 章覆蓋段 | D1 驗收面 | DONE | 13/13 |
| R4-09 | 全案 gate ＋ 變異自檢 | — | DONE | `PASS` failures 0 |
| R4-10 | 收斂 VERIFY（凍結 V1–V8） | D10 | IN_PROGRESS | `logs/verify_r4_c*.log` |
| R4-11 | D7 FAR 通道 waiver（非自授） | D7 | DONE（waiver 已具名，未自授） | `docs/FAR_CHANNEL_WAIVER.json` |
| R4-12 | OpenSpec change | 任務要求 | DONE（strict 通過） | `openspec/changes/w1r4-thirteen-chapter-w1-closure/` |
| R4-13 | owner_semantic_accept 簽章 | 任務要求 | PENDING | `out/OWNER_SEMANTIC_ACCEPT.json` |
| R4-14 | 推送 Fabric ＋ FHS_vNEXT | 任務要求 | PENDING | — |
| R4-15 | 結案 CLOSEOUT／SESSION_STATE／selfcheck | — | PENDING | — |
