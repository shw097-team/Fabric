# W0 As-Built — r8（2026-11-08）

本目錄是 **非權威鏡像**，`NON_AUTHORITATIVE`、`NOT_EXTERNALLY_ACCEPTED`。

`r8/` 是對 r7 的**驗收後回寫**：`FHS_PIPD-LS-PKG_W0_r8.md` 以 r7 全文（492,290 bytes，
sha256 `264787b0…`）逐位元為前綴，追加驗證章節；六個 W0 工作包的頭條數字在獨立 process
重算後全部重現，並量到七個文件層缺陷（`V-01`…`V-07`）與一個閘缺口（新增 `G10-DOC-PARENT-CLAIM`）。

**原域 Reader 收據仍為 0。** 綠燈不是驗收，PR 未併。

實體產物（三份 SPEC、交叉表、投影、oracle 計畫、逐車道報告）在 SBL
`evidence/fhs-w0-r8-verify-20261108/`；本鏡像只放文件與對帳，不放寬任何路由或權限
（`INTEGRATION/FHS/repository-map.json`，`FHS-NAV/v2`，`effect_permission=NONE`）。
