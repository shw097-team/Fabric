# OpenSpec 未勾項索引（本回合產出，未自動打勾）

- 產出時間（UTC）：`2026-10-21T06:27:50.945758Z`
- active changes：**38**
- 有未勾項的 change：**34**
- 未勾項總數：**460**（業主引用的 471 為舊估計值）
- 本回合自身 change 之外的 change：**34** 個，合計 **460** 個未勾項
- **本腳本套用的 tick 數：0**

## 逐 change 索引

| change | 未勾 | 已勾 | 自身產物檔 | 名稱出現於 git log |
|---|---:|---:|---:|---|
| `hermes-incident-2026-10-05-repair` | 35 | 0 | 6 | 是 |
| `lane-mandate-rebinding-and-d01-revocation` | 27 | 11 | 5 | 是 |
| `lane-sod-enforcement` | 27 | 0 | 5 | 是 |
| `verification-artifact-contract` | 26 | 7 | 5 | 是 |
| `hgk-far-remediation-20261016` | 25 | 0 | 3 | 是 |
| `hgk-checker-upgrade-adapter` | 23 | 0 | 5 | 是 |
| `lane-verify-dual-routing-and-plan-high` | 23 | 5 | 5 | 是 |
| `pipd-s4r6-closeout-doc-identity-and-update-route` | 23 | 0 | 3 | 否 |
| `hgk-lane-brief-and-guard-hardening-20261015` | 22 | 0 | 5 | 是 |
| `hgk-r8-eia-closure-skill-slim-20261016` | 22 | 0 | 5 | 是 |
| `pipd-r17-install-doc-identity-guard` | 21 | 0 | 3 | 否 |
| `pipd-repo-hygiene-and-handover-20261016` | 21 | 0 | 5 | 否 |
| `strict-declaration-20261011` | 17 | 5 | 5 | 否 |
| `hgk-lane-reliability-closure-20261016` | 16 | 5 | 3 | 是 |
| `hgk-far-019-owner-authorized-closure` | 14 | 7 | 3 | 是 |
| `lane-verify-routing-remediation` | 14 | 0 | 5 | 是 |
| `hgk-skill-convergence-20261014` | 13 | 3 | 5 | 是 |
| `lane-model-chain-rebind-20261015` | 13 | 0 | 5 | 是 |
| `skill-mainfile-cap-remediation` | 11 | 0 | 4 | 否 |
| `hgk-cnv-evidence-archive-r7r11-20261016` | 10 | 11 | 3 | 是 |
| `hgk-far-018-r7r11-residual-closure` | 9 | 3 | 3 | 是 |
| `lane-toolchain-identity-and-failure-classification` | 9 | 18 | 5 | 是 |
| `gcm-noninteractive-default-containment` | 8 | 36 | 4 | 否 |
| `hgk-cnv-far018-far019-archive` | 5 | 10 | 3 | 是 |
| `hgk-plan-plane-rebind-20261015` | 5 | 3 | 2 | 是 |
| `hgk-r10-session-closure-20261016` | 5 | 25 | 3 | 是 |
| `hgk-r9-far-residual-closure-20261016` | 5 | 20 | 5 | 是 |
| `lane-health-repair-20261011` | 4 | 30 | 5 | 是 |
| `sod-independent-verify-enforcement` | 2 | 3 | 4 | 否 |
| `hgk-r11-session-handover-20261016` | 1 | 26 | 3 | 是 |
| `hgk-round3-lane-rebind-20261016` | 1 | 26 | 3 | 是 |
| `lane-supervisor-windowless-convergence` | 1 | 12 | 4 | 是 |
| `pipd-unmerged-candidate-merge-20261016` | 1 | 7 | 5 | 否 |
| `s4-final-pr18-closeout-20261016` | 1 | 22 | 5 | 否 |
| `archive` | 0 | 33 | 5 | 否 |
| `far-lane-remediation-20261021` | 0 | 19 | 3 | 是 |
| `hgk-cnv-hygiene-readme-closure` | 0 | 17 | 4 | 是 |
| `hgk-cnv-owner-decision-main-landing` | 0 | 11 | 3 | 是 |

### `[~]` 具名殘留不計入本索引（openspec 自身的完成語意）

openspec 的完成語意是：**全勾 = Complete；部分未完成 = `[~]` 具名殘留**。
本索引只數 `[ ]`。實測全部 38 個 active change 裡：
`[ ]` 共 465 筆（含本回合自己的 5 筆 → 其他 34 個 change 共 **460** 筆），
`[~]` 共 **1** 筆（`s4-final-pr18-closeout-20261016` 5.1「Dispatch the VERIFY_SECURITY lane
against the frozen packet (running)」）——**不計入 460**。

這個區分正是 460 項的性質所在：**它們無一處於 openspec 原生可接受的「具名殘留」形態**。
一個 change 若「做完了、只剩幾項具名殘留」，開著完全合理；但 16 個 change 處於近 185 筆未勾，
那是**未開工的工程工作**，不是可接受的殘留。
