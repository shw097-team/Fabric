# W1 r3 實作工作清單（機器抽取）

Subject `5aca7b5e2bdc67d1…` / 13944 行 / 2064944 bytes

| 單元 | 類別 | 標題 | 首拒碼 |
|---|---|---|---|
| `WP-FHS-02` | W1 WP | Fabric Policy Consumer｜主波 W1 | POLICY_LOADED_ACK_MISSING; POLICY_SIGNER_OR_EPOCH_DENY |
| `WP-FHS-03` | W1 WP | HGK Registry/Issuer｜主波 W1 | ISSUER_PRINCIPAL_ACL_DENY; ISSUER_WORK_BINDING_NACK |
| `WP-FHS-04` | W1 WP | Hermes Durable Runtime｜主波 W1 | ACTUAL_SERVED_NOT_OBSERVED; CROSS_PROFILE_SECRET_DENY |
| `WP-FHS-05` | W1 WP | PIPD Native Compiler｜主波 W1 | PD_REPOCONTEXT_UNBOUND; PIPD_SHADOW_WRITER_DENY |
| `WP-FHS-07` | W1 WP | Native PLAN Commander A/B/C｜主波 W1 | CROSS_WORK_PLAN_AUTH_DENY; PLAN_CAS_ACK_MISSING |
| `WP-FHS-11` | W1 WP | Portable Host Dogfood｜主波 W1 | HOST_CHECKER_IMPERSONATION_DENY; HOST_EVIDENCE_FOREIGN_NACK |
| `WP-FHS-17` | W1 WP | CAP-BOOT Native Occupants｜主波 W1 | CAPABILITY_NOT_QUALIFIED; INSTALLER_PRIVILEGE_DENY |
| `WP-FHS-20` | W1 WP | CLI/Agent/Host Kind Matrix｜主波 W1 | CELL_RECEIPT_CROSS_HOST_DENY; CELL_TOKEN_OWNER_ACK_MISSING |
| `F01` | 受影發現 | 舊source path/整檔SHA不再current | – |
| `F02` | 受影發現 | 摘要交付會丟原子義、NEG、Consumer | – |
| `F03` | 受影發現 | 可能倒置17/06、額外15→05或全域卡read | – |
| `F04` | 受影發現 | 長正文複合句拒收，短卡不得冒全集 | – |
| `F05` | 受影發現 | caller錯HEAD仍exit0/verified | – |
| `F06` | 受影發現 | typed ECP非全不可用，但demo scope非W1許可 | – |
| `F07` | 受影發現 | TQAEP缺receipt；partial PASS易誤讀 | – |
| `F08` | 受影發現 | 1/7已superseded；舊7/7不屬r3 | – |
| `F09` | 受影發現 | 不可得/僅總數說法失準 | – |
| `F10` | 受影發現 | 已建repo不應重建；版本不能用舊文猜 | – |
| `F11` | 受影發現 | 34/39/16M70錯混W1分母 | – |
| `F12` | 受影發現 | 本地資料庫測不能冒原准入 | – |
| `F13` | 受影發現 | 有原輪子，未必真派工/恢復全鏈 | – |
| `F14` | 受影發現 | 進口缺mirror；原frozen payload真漂移 | – |
| `F15` | 受影發現 | 作者角色/自簽/不存在source冒安全 | – |
| `F16` | 受影發現 | 12Delta與九交接不能只列數或倒扣W0 | – |
| `F17` | 受影發現 | 16Moments/38Surface未具原身份便會壓平 | – |
| `F18` | 受影發現 | 文件交付冒啟用、hash循環或遞交冒接收 | – |
| `GJ01` | 旅程 | 普通問題，READ最短FUO | UNRELATED_HOST_GATE / POLICY_NOT_LOADED |
| `GJ02` | 旅程 | 普通改稿，DRAFT交付 | SECOND_CANONICAL_WRITER / HOST_WRITESET_BIND_HOLD / ISSUE_WRITE_NOT_OBSERVED |
| `GJ03` | 旅程 | 真正建置，受護DEV與長工 |  |
| `EFFECT_READ` | 六效果 | 權限錯誤或無法讀取卻標READ_BYTES | – |
| `EFFECT_DRAFT` | 六效果 | 覆寫CURRENT、產品檔或先前r8交付 | – |
| `EFFECT_DEV` | 六效果 | 未probe填ABSENT、`git add -A`、reset整根 | – |
| `EFFECT_OPS` | 六效果 | 用DEV許可安裝、profile名冒OS隔離、git revert冒Host回復 | – |
| `EFFECT_USER` | 六效果 | no-effect referral冒Issue已建、跨資料scope借Consent | – |
| `EFFECT_RELEASE` | 六效果 | ZIP/CI/gstack ship/自批PR冒受權Release | – |
