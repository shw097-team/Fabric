# EVIDENCE CLOSURE — FAR-20261016-018 (R7～R11 殘留結案與移交)

generated_utc: 2026-10-16T11:40:26.678555+00:00

## 0. Claim ceiling and binding

| field | value |
|---|---|
| claim ceiling | `LOCAL` — 本地可重導的完成 |
| external acceptance | **NOT ISSUED**（待真實驗收官） |
| full_convergence_verdict | `TEMP_CLOSED_CHALLENGE` |
| production_verdict | `FAIL_CLOSED` |
| canonical_AO_acceptance | `NOT_ISSUED` |
| reviewer of this pack | none — 本 pack 未經任何外部驗收官接受 |

## 1. 本輪是什麼

FAR 研究輪：對 R7～R11 證據歸檔輪遺留的全部殘留／缺口／阻斷、待 OWNER 決策項、候選未落地資產與本 SESSION 結案移交事項，提出唯一份排名工程裁決並執行其中 agent 可執行項目；OWNER-gated 僅備妥、未執行。

## 2. 執行面（皆有收據）

| 面 | 證據 |
|---|---|
| Gate-1 route | `{"flow": "RESEARCH_LITERATURE_REPO", "route": "NATIVE", "reason_code": null}`；負控制 `PURE_QA_CHAT` → `GSTACK` |
| CAPC contract | `PROMPT_COMPILE_PASS`（lint／activation／acceptance／compile 皆 exit 0） |
| HGK admission | `ADMISSION_OK` project `FAR-018-R7R11-RESIDUAL` |
| Kanban | 17 卡／67 次 CLI；histogram `{"done": 4, "running": 8, "blocked": 5}` |
| OpenSpec | `hgk-far-018-r7r11-residual-closure` strict-valid |
| EXECUTE lane | `opencode-go/deepseek-v4.1-flash` exit 0 nonce True |
| VERIFY lane | `openai-codex/gpt-6.1-sol` exit 0 nonce True |
| model-axis diversity | **PRESENT**（EXECUTE `deepseek-v4.1-flash` vs VERIFY `gpt-6.1-sol`） |

## 3. 殘留暫存器（自 artifact 重算）

| 量 | 值 |
|---|---|
| w1_items_total | 118 |
| w2_defects | 5 |
| w2_confirmed_defects | 4 |
| w1 by_kind | `{"UNLANDED_CANDIDATE": 13, "BLOCKED": 14, "OWNER_DECISION": 14, "GAP": 28, "CLOSED_ALREADY": 31, "RESIDUAL": 18}` |
| w1 by_authority | `{"other-round": 49, "owner-gated": 58, "agent-executable-now": 11}` |
| agent-executable 仍開放 | `["MUTABLE-SOURCE-HASH-METADATA", "CROSS-INDEX-PRESENCE-NONVacuity", "SELF-CHECK-NONVacuity"]` |

## 4. 本輪執行的動作與其殘留

| # | 動作 | 優先 | 收據存在 | 執行後仍留的殘留 |
|---|---|---|---|---|
| A1 | OS-enforced checker isolation harness (fail-able) | P0 | True | an immutable, non-liftable boundary still needs a distinct OS identity (owner-gated OG6) |
| A2 | de-vacuum the previous round's S8b check | P1 | True | — |
| A3 | reconstruct the skill index from verified pointers (partial) | P1 | True | the original index's full field set is unrecoverable from the pointers alone |
| A4 | mutable-subject metadata semantics | P2 | True | — |
| A5 | de-vacuum the presence indicator | P2 | True | — |
| A6 | register + ruling + handover + single evidence MD + publish/readback | P0 | True | — |

## 5. 獨立 checker（不同模型軸）

- served arm `openai-codex/gpt-6.1-sol`，required arm 由 `--require-arm` pin（pool rank 1 是 writer 自己的模型，故 pin rank 2）
- verdict file: `lane/VERIFY_VERDICT.json`；overall `PARTIAL`
  - `V1` AGREE — The independently recomputed W1 totals match its counts object and FAR_RULING.md §0.
  - `V2` UNVERIFIABLE — The isolation harness detects its deny-skipped mutation, demonstrates actual write denial, and cleans up.
  - `V3` AGREE — The revised S8b check changes its computed verdict when disclosure is stripped.
  - `V4` AGREE — All five recorded pointer slices match; the reconstruction explicitly declares partial coverage; digest mutati
  - `V5` AGREE — The previous round's S8b success argument is literal True, and sod_declared is unused.
  - `V6` AGREE — The inspected artifacts preserve non-achieved convergence, production, and canonical acceptance values; R7-03 
  - `V7` UNVERIFIABLE — D0 records a refused guarded write, distinguishes lane measurement from orchestrator persistence, and attribut
- could_not_verify: `["V2: Fresh isolation normal and self-test runs were prohibited by the enforced read-only filesystem restriction. Existing receipts and source are not substitutes for those runs.", "V2: Independently observed that the stored probe directory is absent, but did not reproduce the deny operation or freshly verify its ACL lifecycle.", "V7: The dossier's error string and actor distinction are present; t`

## 6. OWNER-gated（本輪未執行）

- `OG1` peer chain #6/#8/#10 merge
- `OG2` R7-02 validator cross-repo code promotion
- `OG3` R7-04 Fresh G1 owner certificate
- `OG4` canonical codex_executable pin repair
- `OG5` KP R04 polarity (20 clauses) + source#6 status
- `OG6` immutable checker boundary (distinct OS identity)
- `OG7` PR #12 promotion out of draft
- `OG8` guard predicate precision (runtime plane)

## 7. 自檢測

`SELF_CHECK_RECEIPT.json`: {"PASS": 14, "FAIL": 0, "NOT_RUN": 0, "total": 14} verdict `PASS`

## 8. Nonclaims

- no acceptance-report finding is claimed closed except those this register names as closed
- the checker boundary demonstrated in A1 is ordinary OS denial, not an immutable boundary
- no merge, release, cross-repo promotion or canonical control-plane edit was performed by this round
- external acceptance remains with a real acceptance officer; canonical_AO_acceptance stays NOT_ISSUED
- 本輪未合併任何 PR、未晉升任何 Draft、未編輯 canonical 控制平面、未執行任何歸檔腳本。
- A1 證明的 OS 寫入拒絕是**普通拒絕**，同身分可自行解除其 deny ACE，**不是**不可解除的安全邊界。

## 9. STOP / resume

STOP：本輪到此為止，claim ceiling `LOCAL`；正式 `R7-03` 關閉需 OG6（不同 OS 身分），`R7-04` 需 OG3，`R7-02` 需 OG2，canonical pin 修復需 OG4，peer chain 需 OG1，guard 精度需 OG8。
resume：讀 `RESIDUAL_REGISTER.json` 取殘留與 owner，讀 `HANDOVER_FAR018.md` 取 checkpoint 與下一步。

## 10. Raw artifact index（本 pack 實際攜帶的檔案）

| path | bytes | sha256 |
|---|---|---|
| `.gitattributes` | 9 | `8b9c3028d6467ff3be7c7931…` |
| `ADJUDICATION_AND_LIMITATIONS.json` | 8216 | `268aff186ecc2ee9685f48b9…` |
| `build_pack.py` | 13050 | `04b712ca73a4cfb546d88c93…` |
| `build_register.py` | 5712 | `3378bff28c20e11e5dabfde3…` |
| `compiler/acceptance.stdout.txt` | 80 | `9b718dd02a8f35fb25777044…` |
| `compiler/activation.stdout.txt` | 80 | `9b718dd02a8f35fb25777044…` |
| `compiler/compile.stdout.txt` | 269 | `16293c657c8a6ae2dd46604a…` |
| `compiler/compiler-receipt.json` | 579 | `4d966571a56c6b0a94a484fc…` |
| `compiler/compiler-report.json` | 261 | `515f0363b39561479a60f69f…` |
| `compiler/duplication.stdout.txt` | 269 | `59836837b0003c24990a94ae…` |
| `compiler/hash.stdout.txt` | 66 | `f14afee8f06972cb940723c9…` |
| `compiler/lint.stdout.txt` | 80 | `9b718dd02a8f35fb25777044…` |
| `emit_closure.py` | 15409 | `329f61c1d6ab0953b34b22f7…` |
| `far018_admission.py` | 9523 | `a716fe8605558e169502d2d0…` |
| `far018_contract.py` | 12687 | `fe53812c4a2dc8cedc579366…` |
| `far018_kanban.py` | 5258 | `9501634e716b1541441329cd…` |
| `FAR_RULING.md` | 7231 | `5b5d58470337c25b7a00f644…` |
| `HANDOVER_FAR018.md` | 3059 | `b2bb76092785af350185552f…` |
| `HGK_TYPED_ADMISSION_FAR018.json` | 6229 | `fdad8e5da19f7d2460e2f126…` |
| `HGK_WORKORDER_RESULTS_AND_DELIVERY.json` | 5337 | `c273bdd94a8a722b4a18f441…` |
| `isolation_probe_receipt.json` | 4782 | `ecd040dd9980472b820acef0…` |
| `KANBAN_LIFECYCLE_RECEIPT.json` | 28833 | `38df5f0d7d0ca970791b8b0f…` |
| `lane/EXECUTE_BRIEF.md` | 7480 | `45d772536d2ad08b0edbae16…` |
| `lane/EXECUTE_RECEIPT.json` | 6706 | `bd3522f43c241bfe4e9b7c18…` |
| `lane/VERIFY_ATTEMPT1_REFUSED.json` | 1494 | `696d0d3ed6b8b0244c0b3d60…` |
| `lane/VERIFY_BRIEF.md` | 5277 | `f3c4afa927b232b0cfccbcc9…` |
| `lane/VERIFY_RECEIPT.json` | 8053 | `340a71a47a3847cfb15e8e0a…` |
| `lane/VERIFY_VERDICT.json` | 12696 | `c86bad758da2e32fdbe88173…` |
| `persist_firstfail.py` | 2966 | `2f2be9c4dddb3542ad56f2bd…` |
| `prompt-contract.json` | 62492 | `70b227969c3e35f4527d5113…` |
| `publish_followup2.py` | 8124 | `a55574ad8199435fce23527f…` |
| `recon_route.py` | 4620 | `dc7884a29d1b84367fe3022a…` |
| `RESIDUAL_REGISTER.json` | 5018 | `dfb44d55eb4598e030aea86e…` |
| `ROUTE_CHECK.json` | 4755 | `d999906a2535c38d21f1b375…` |
| `self_check.py` | 12997 | `75ce1af810cd746b09e998e2…` |
| `SELF_CHECK_RECEIPT.json` | 3610 | `6ef3355594bf27d77ecdb43c…` |
| `SELF_EVOLUTION_RECORD.json` | 2752 | `7107be8eb64a0d58ca4498d3…` |
| `skill_entry_map_install_receipt.json` | 1618 | `792360db4e09ab7cfa86a5f6…` |
| `verify_pack_local.py` | 1113 | `95ff86a232d9ee5f3280bf4a…` |
| `W1_RESIDUAL_UNIVERSE.json` | 185506 | `5493d4abee20b68d6ac8c3a8…` |
| `W2_DEFECT_DOSSIER.json` | 10540 | `05df0ac376ea33da1b970d84…` |
| `writer/checker_isolation_probe.py` | 8368 | `2147eccc4410f8f69a3d355c…` |
| `writer/CROSS_INDEX_V2.json` | 6701 | `25582fa269e487bf7e900376…` |
| `writer/cross_index_v2.py` | 6413 | `f10e6c16c2ee22f253e29427…` |
| `writer/entry_map.json` | 4427 | `dbd6f556e5bf9e743cc3c093…` |
| `writer/metadata_semantics.py` | 7676 | `6df34a59c20e900421325b8e…` |
| `writer/METADATA_SEMANTICS_V2.json` | 34343 | `065249f3235658c3c01158af…` |
| `writer/regen_entry_map.py` | 8839 | `dbc69152bd1d579f33c5f582…` |
| `writer/self_check_v2.py` | 8786 | `81f27680f220f1dcd52ce3dc…` |
| `writer/WRITER_MANIFEST.json` | 4627 | `584445a0313b16df78b4e0bf…` |

`PACK_INDEX.json` is not listed above and does not list itself: a file cannot contain its own digest. Its digest is carried by `PUBLISH_RECEIPT.json`, `REMOTE_READBACK_VERIFY.json` and `PUBLICATION_ADDENDUM.json` instead. (A self-row was tried in the first publication attempt and failed a live remote readback with exactly one mismatch — recorded, not hidden.)

