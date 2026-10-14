# HGK External-Submission Gates (2026-08-14, external 5-defect FAR root-cause)

外部驗收反覆不過的 5 個根因與對應 gate。任何外部證據提交前**必須**遵守。

## 根因（外部認定，FAR 三源確認）

1. 沒有真正 atomic finalization —— reducer 渲染後仍手動修 placeholder/stale fields
2. 沒有 machine preflight —— RR6 時 3 個 checker 數字（98/185/194）並存仍提交
3. stale fields 手動帶到下一版 —— 5 個 self-hash 舊 MD 殘留；RR6-004 標題 179 body 98
4. manifest/checker/root 沒有一次性重生 —— manifest 每輪 +1 累加；checker 從未 clean regenerate
5. 過早把 finding 標 CLOSED —— RR6-005/RR8-A 標 CLOSED 但外部判 PARTIAL/NOT_CLOSED

## Gate 1 — MACHINE PREFLIGHT（提交前必跑）

```bash
python var/fda/hgk_evidence_preflight.py   # PASS = 可提交 / BLOCKED = 先修
```

5 項阻擋檢查：
- (a) 單一 current checker denominator：舊 checker receipts 的 **JSON body** 須含
  `status: HISTORICAL` + `superseded_by`（只改檔名不算；只認最新 FINAL_RR7 為 current）
- (b) 最新 single-evidence MD（LATEST FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_*）無
  `this_file_sha256` self-hash（舊 MD 殘留不算——current-series 掃描只看最新）
- (c) manifest 0 missing / 0 hash mismatch
- (d) 三向 subject binding：manifest.subject_root == checker.subject_root == MD 宣告 final_subject_root
  （比較用前 12 字元，勿用 full-vs-truncated 混合比較）
- (e) 每個 CLOSED finding 有 authority receipt 在 disk

## Gate 2 — ONE-TIME REGENERATION

- 每個 external repair round **從零重生成** manifest（不得 +1 累加）
- 舊 receipts → JSON body 標 HISTORICAL（不刪除，保留 audit trail）
- 舊 evidence MD 留在 evidence/ 但**排除於 current-series 掃描**
- 永不用手 edit manifest row「carry forward」stale value —— 一律從 disk bytes 重算

## Gate 3 — CLOSED AUTHORITY

finding 標 CLOSED 的條件：
- 有 machine-readable authority receipt 在 disk（receipt JSON 含 verdict）
- evidence MD 中引用該 receipt 的**確切路徑**
- 無 receipt 即 CLOSED = premature（外部 r6: RR6-005; r8: RR8-A 實例）

## Gate 4 — ATOMIC RESEAL（RR8-final 實證，2026-08-14）

外部指「manifest 仍有 stale duplicated metadata」時的最後閉合步驟（evidence-only，
**不得**重跑 F01/F06/UFO²/PAPER、不得加新 gate）。執行 `scripts/atomic_reseal.py`：
- artifact_count **由 len(artifacts[]) 自動 derive**（不再手動維護數字——「54 vs 實際不符」類 defect 的根因）
- checker_history：最新者 ONLY CURRENT，全部前代 HISTORICAL + `superseded_by` 最新
- 清除舊 round 的 version/schema 殘留（RR4 時代 `FINAL_RR4_...` 等）
- 每個 artifact sha 從 bundle bytes 重算 → 0 missing / 0 mismatch
- 單一 serialization（sort_keys）+ 單一 SHA

## Gate 5 — 內嵌 manifest body SHA 陷阱（RR8 實證）

把 EvidenceManifest **內嵌進單一證據 MD** 時：
- `json.dumps(man)` 重序列化後 bytes 與磁碟檔**不同** → 內嵌 body 的 SHA ≠ 磁碟檔 SHA
- **MD 內宣告的 sha 必須是「內嵌 body 的 sha」**（外部 reviewer re-hash 才能 MATCH），
  磁碟檔 sha 另以註記列出並說明差異原因（僅 JSON re-serialization）
- 檢查「manifest 有無內嵌」要比對 embedded-body sha，不是磁碟檔 sha（`man_sha in body` 恆 False 誤報）
- MD builder 用 **placeholder `.replace()`**（如 `__MANIFEST_BODY__`），不要用 f-string 內嵌
  大量 `{...}`（f-string 的 `{` 會與 JSON/manifest 內容衝突）

## Gate 6 — checker 記錄 ID 唯一性（T100 實證）

- checker 的 T100_NOSECRET 掃描若用 `f.name` 當 check ID，**同名檔在不同子目錄會 duplicate ID**
  （r7 抓出 194 records 但 192 unique）→ **ID 改用相對路徑**
  （`str(f.relative_to(FDA)).replace("\\","_").replace("/","_")`）
- 外部驗收要求：actual record count == declared total == unique IDs，duplicate=0

## 執行者

- preflight：`scripts/hgk_evidence_preflight.py`（skill 內建，RR6 時代驗證）
- atomic reseal：`scripts/atomic_reseal.py`（skill 內建，RR8-final 驗證）
- 驗證：提交前跑 preflight → 全 PASS 才 pack/upload；reseal 後跑 derive/count/unique invariants

## r10/r11 Fixed-Contract Lessons (2026-08-14, external acceptance GRANTED)

**Identity separation model (no-moving-goalpost):** `candidate_root != evaluator_sha256 !=
evidence_bundle_root` — three distinct layers. Never demand candidate root change because
evidence changed; never treat a different JSON serialization of the same manifest as a second
canonical identity (on-disk re-serialization = `NON_CANONICAL_RENDERING`).

**FINAL reseal — the 3 fields that kept failing external review (r10):**
1. **exact_set counters must be DERIVED** from `len(artifacts[])` — `manifest_row_count ==
   payload_file_count == artifact_count`. Hand-set numbers (54 vs actual 63) fail; derive, never type.
2. **Chronology:** `generated_at_utc` must be AFTER every bound evidence timestamp. Scan all
   bound receipts' generated_at, take the max, generate the manifest LAST. Stale timestamp =
   EXT-FDA-R10-002.
3. **Evaluator must be machine-readable structured field** — prose in a note is NOT enough:
   ```json
   "evaluator": {"artifact": "independent_checker.py", "sha256": "9009713...", "mode": "VERIFY_ONLY"}
   ```
   Must equal the checker receipt's `script_sha256` exactly.

**Full reseal preflight (12 checks, ALL PASS before submit):**
candidate_root=1 · current_checker=1 (history has 0 CURRENT; the one current lives in the
checker field) · serialization SINGLE_CANONICAL · artifact_count==len(artifacts) ·
unique paths==count · manifest_row_count==count · payload_file_count==count ·
checker total==raw==unique==passed · failed=0/errors=0/exit=0 · evaluator_sha match ·
generated_at > latest bound · 0 missing / 0 mismatch.

**After GRANTED (r11):** update README/AGENTS/TEAM/USER_GUIDE in one commit with acceptance
state + claim ceiling (SQS_LIVE_TRADING still NOT_AUTHORIZED); run docs internal acceptance
check (27/27 pattern) before closing.

## FDA tool-path drift (2026-08-14, parallel-session rename)

Docs/skills may cite a tool at `var/fda/<NAME>.py` that a parallel session renamed (real case:
`FDA_PREFLIGHT_GUARD.py` → `fda_script_guard.py`). Before trusting a documented path:
- `find C:\Projects\Agent_Workspace -name "<NAME>.py"` to locate the actual file
- canonical copies live in skill `references/` / `scripts/` (stable across session churn)
- if a rename happened, prefer the skill-copy path over the doc-cited var/fda path, and note
  the drift in the doc gap-audit (run `docs_acceptance_check.py` pattern: file existence +
  knowledge-placement + discoverability in one pass). Re-runnable probe:
  `scripts/docs_gap_audit.py <project_root>` (themes A/B/C + tool-path + discoverability).
