# R10-0 independent verdict (VERIFY / SECURITY)

Nonce: `R10V-CHECKER-NONCE-4f7a2b`
Overall: **PARTIALLY_VERIFIED**
Brief executed: `R10_VERIFIER_BRIEF.md`. The file the order named, `R10_CHECKER_SHOT_PROMPT.md`, does not exist anywhere on this host.
Measurement window: 2026-10-16 13:49:30 - 13:59 local (UTC+8). Raw outputs: `R10_VERIFY/raw/`.

This is advisory evidence for the owner. It is not an acceptance, a Gate PASS, an AO verdict or a
release, and it asserts no product behaviour.

## 摘要（繁中）

本輪的可交付項本身**大體成立、但記錄不精確**：兩項 wrapper 修復與其測試、registry 的關鍵值、
TSV 的裁決計數、以及「檔案沒有被偽造」都可被我獨立重現；然而 (1) 同角色多回合共用收據路徑的
受影響回合數被少算（我量到 11，本輪記 8）、(2) 對 0-byte 探測的「反駁理由」不成立（該檔案的內容
其實是在探測報告之後、由另一個 session 於 13:35:06 才寫入；寫入日誌在探測的時間窗內對該檔案
完全沒有寫入紀錄）、(3) 本輪「canonical 技能樹沒有可偵測的內容變更」的說法被技能樹自己的
寫入日誌推翻。因此總評為 PARTIALLY_VERIFIED，不是 VERIFIED。

## 1. What I re-derived and confirmed

1. **Wrapper repair A - test-backed.** Running the brief's own command produced `8 passed in 0.08s`
   (exit 0, no skips) against the revision in place when I started (12,319 bytes, digest prefix
   `645c1b6de005`), and `8 passed in 0.06s` against the revision live now (12,497 bytes, digest prefix
   `a308b1cea808`). The file's digest was unchanged across my re-run. Logs: `raw/t1_pytest_raw.txt`,
   `raw/t1b_pytest_live.txt`.

2. **Wrapper repair A - the underlying defect is real.** In
   `_handover/CNV-PIPD-LS-SP-20261015/lane_runs/` there is exactly one file per attempt label, while the
   dispatcher's own attempt directories carry distinct per-turn stamps: I count **7 EXECUTE** turns
   labelled `attempt-1` and **4 VERIFY_SECURITY** turns labelled `attempt-1`, against one
   `EXECUTE_dispatch_receipt_attempt1.json` and one `VERIFY_SECURITY_dispatch_receipt_attempt1.json`.
   The surviving EXECUTE file (7,701 B, mtime 12:40:52, digest prefix `e4a5db9b7ea4`) holds
   `attempt-1-20261016T042656Z`, `generated_utc 04:40:52Z`, `seconds 835.74` - the **last** of the seven.
   The earlier turn's 364.5 s receipt survives only outside `lane_runs`, as the R9 packet's hand-named
   copy `WS_A/receipts/EXECUTE_dispatch_receipt_W2_20261016T042550Z.json`. So yes: one path served several
   turns of one role. Log: `raw/t1c_turn_mapping.txt`.

3. **Wrapper repair B - the underlying defect is real.** From R9's real receipt with none of this
   round's helpers: `code=ERR_NO_ARM_EMITTED_NONCE`, `attempts[0].nonce_present=false`,
   `nonce_source="item.completed/agent_message"`, `stdout_bytes=429783`, and also
   `nonce_present_raw_stdout=true`, `used_rank`/`used_transport_model` null. The surface that same
   receipt recorded is 429,783 bytes with digest prefix `5d07b4c4053e` (equal to its recorded
   `stdout_sha256`) and contains `R9V-CHECKER-NONCE-5c1d84` (from `R9_VERIFIER_BRIEF.md` line 7)
   **6 times**, the last being the final token before `turn.completed`; the receipt's own `stdout_tail`
   also ends with it. Log: `raw/t2_bytesurface.txt`.

4. **Change-record adjudication - values and counts.** Re-derived with the project's own reader
   (`lane_policy.load_registry/route_for_lane/check_drift/check_sod`): epoch **21**; `PLAN` =
   `openai-codex/gpt-6.1-sol` medium, `admission_status ADMITTED`, `selection_authority
   owner-order-20261016-plan-model-rebind-gpt61-sol`; `EXECUTE` = `opencode-go/deepseek-v4.1-flash`
   UNPROVEN; `VERIFY_SECURITY` = `openai-codex/gpt-6.1-sol` medium UNPROVEN; `check_drift(registry=reg)
   == []`; `check_sod(PLAN, VERIFY_SECURITY) == (False, 'SOD_VIOLATION maker_model=gpt-6.1-sol ==
   checker_model=gpt-6.1-sol')`. Registry 42,948 bytes, digest prefix `38f0436b9bde` (full-length match),
   mtime 12:36:30. The TSV counts by my own `awk`: 24 DONE_MEASURED, 9 OPEN_OWNER, 1 SUPERSEDED,
   2 NOT_OWED over 36 rows, split 25 + 11 per change. All 23 artifact paths named by the rows that I
   checked exist, including the V3c checker verdict (C1 AGREE, C2/C3/C6 DISAGREE, C4 UNCERTAIN,
   C5/C7 AGREE) and its `dispatch.json` (VERIFY lane actually served `openai-codex/gpt-6.1-sol`, exit 0,
   798.81 s). **No row I could test closes by naming an artifact that does not exist.** Logs:
   `raw/t3_registry_probe.txt`, `raw/t3b_t5_artifact_existence.txt`, `raw/t3c_checker_and_publish.txt`.

5. **The 0-byte probe.** My own measurement of
   `.../hermes/skills/hgk-lifecycle-admission/SKILL.md`: 35,739 bytes, 361 lines, digest prefix
   `2911867811a5`, mtime 13:35:06 - byte-identical to the round's re-derivation, twice read with an
   identical result. The only zero-byte file under the skills tree is `.hub/audit.log`. The skill is not
   corrupt today. Log: `raw/t4_skill_measure.txt`.

6. **Wrapper behaviour on a failed dispatch.** The round-root attestation records
   `dispatcher_code=ERR_LANE_REQUIRED_ARM_ABSENT`, `arms_from_attempts=[]`, `nonce_found_in=[]`,
   `verdict=NO_ATTEMPTS_RECORDED`, and I independently confirmed its `expected_nonce_sha256_prefix`
   `d9cd7c3990001b29` **is** `sha256('R10V-CHECKER-NONCE-4f7a2b')` - the nonce is derived from the
   dispatched brief, not from the lane. The same record's snapshot filename carries the doubled
   `VERIFY_SECURITY_turn1_..._VERIFY_SECURITY_turn1_...` prefix, the live trace of the `snapshot()` bug
   patched at 13:50:22. Log: `raw/t2b_t5e_nonce_and_m2.txt`.

7. **Claim discipline.** A keyword scan of all eight round records returns only one blocker id and six
   explicit disclaimers ("LOCAL / candidate-only ... not an acceptance, a Gate PASS, an AO verdict or a
   release"). No sentence inflates a local measurement into an acceptance. Log: `raw/t6_claim_scan.txt`.

## 2. What I refute or dispute

- **D1 - the collision count is understated.** The round records 8 affected turns (5 EXECUTE, 3
  VERIFY_SECURITY); I measure **11** attempt-1 turns sharing the two attempt-1 receipt paths
  (7 + 4), i.e. up to 9 destroyed receipts.
- **D2 - the nonce mechanism is described imprecisely.** `README_R10_TOOLING.md` says the dispatcher
  reads the nonce only from `item.completed/agent_message` events; the receipt itself records
  `nonce_present_raw_stdout=true`, so the token *was* seen in raw stdout and the code path declined to
  accept it. The defect and the repair verdict stand.
- **D3 - the 0-byte refutation's reasoning fails.** The tree's own write log (`.curator_ledger.jsonl`,
  871 records) shows the file's content changed **twice**: at 12:15:21 (by this session) and at 13:35:06
  (by a **different** session, `20261016_105348_b4b537`, whose "after" digest is exactly the digest I
  measured). In the probe's read window (13:19-13:24) the log records **no write to that file at all**,
  so the "single size read can race a rewrite" explanation has no support; and the adjudication's
  ancillary claim that the file "loaded successfully into this session at 13:16" matches no artifact.
  The probe's reading at its own time is therefore **not re-measurable**, and neither is its refutation.
- **D4 - stale evidence basis.** The same WS2 report that produced the 0-byte reading reported
  `hgk-kanban-and-lane-routing/SKILL.md` = 86,198 bytes; that file has been **88,115** bytes since
  13:38:54. The adjudication carried the stale value forward without noting the drift.
- **D5 - the side-effect audit is refuted.** The claim that in-window skills-tree mtimes are "consistent
  with skill LOADS ... no content change ... detectable" is contradicted by the tree's own log: two
  SKILL.md files were **content-rewritten inside the round's research window** (13:35:06 and 13:38:54)
  by peer sessions, and this session (`20261015_125956_d5f877`, per `SESSION_LEDGER_R10.json`) has
  **16 canonical-tree content write records** on 2026-10-16 between 11:13 and 13:07 local across six
  skills - `hgk-lifecycle-admission/SKILL.md` at 12:15:21 plus a new `references/far-run-binding.md`,
  `hgk-kanban-and-lane-routing/SKILL.md` at 13:03:50, and others - which the round's records attribute
  only to R9. Attribution caveat: the two in-window rewrites are by **peer** sessions, not by the R10-0
  round itself, whose own window (13:16-13:50) shows no write by the R10 session.
- **D6 - one row is scored as a pass while recording a defect.** Row `T5` is DONE_MEASURED although its
  own note says the pointer integrity claim has "one broken load path": the live `SKILL.md` names
  `entry_map.json` at lines 66 and 71 and I measured that no `entry_map.json` exists in the live skill
  directory.
- **D7 - the round was not frozen.** `dispatch_r10.py` grew 12,319 -> 12,497 bytes at 13:50:22, and
  `SESSION_LEDGER_R10.json` plus `SELF_EVOLUTION_R10.md/.json` were written at 13:49:43, i.e. **after**
  the brief (13:46:03) and after my first measurement (13:50:15). Claims that name neither a revision
  nor a digest cannot be reproduced.
- **D8 - the ordered file is absent.** `R10_CHECKER_SHOT_PROMPT.md` exists nowhere on this host (a
  workspace-wide name search returns 0 hits); I executed `R10_VERIFIER_BRIEF.md`.

## 3. Procedural compliance

- **Write root respected: yes.** Everything I created is under `R10_VERIFY/`
  (`raw/` logs and probe scripts, `R10_VERDICT.json`, `R10_VERDICT.md`, `R10V_DONE`). A listing of the
  round root for files newer than 13:52 returns only my own `R10_VERIFY` files.
- **Write verbs: file writes only, no git write, no network write.** Shell redirection for raw command
  output plus `write_file` for scripts and verdicts. No git command was invoked at all (only find, stat,
  ls, cat, awk, sed, wc, grep, sha256sum, date, ps, and the HG-KSEOS venv python/pytest). Disclosed side
  effect: the brief's exact pytest command maintains the pre-existing `tooling/.pytest_cache`;
  a first run at 13:50:15 was followed by a cache update at 13:50:30 that I cannot attribute, because a
  concurrent process was running that same suite then. My later runs used `-p no:cacheprovider` and
  `PYTHONDONTWRITEBYTECODE=1`, and `dispatch_r10.py`'s digest was unchanged across my run.
- **Forbidden locations: no forbidden write; required reads were read-only.** I read `lane_runs/**`
  (brief items 1-2), the canonical skills tree (item 4), and the registry through the project reader
  (item 3); I wrote nothing under `R6_DELIVERY/`, `-R9/WS_A/`, `-R9/WS_B/`, `-R9/FAR/` or any config or
  skill tree. No credential value was read or printed: `M2_TRUSTED_SCOPE_SECRETS_R10.json` was parsed for
  key names and types only, and its token fields are reported as presence/counts.
- **Network: none attempted.**
- **Nonce: disclosed deviation.** The brief orders the nonce as the first line of the first message; my
  first message was already sent before I read the brief. It is written into `R10V_DONE` and carried in
  this verdict.

## 4. Could not verify

1. The 0-byte state at 13:19-13:24 is not re-measurable: the file was rewritten at 13:35:06, its
   previous content (digest prefix `8af86f502767`) has no copy on this host, and the write log records
   digests only, not byte sizes.
2. `R10/PACKET_MANIFEST.json` does not exist, so brief item 5's delivery set cannot be enumerated.
3. The round's remote claims were not re-fetched (the brief forbids remote operations); only the local
   records were checked and they are mutually consistent.
4. The round's HGK Spine claims were not re-derived (spine database not read).
5. Row 1's Spine re-admission and row 4's `openspec --strict` were not re-executed.
6. Whether the peer sessions' in-window canonical-tree rewrites were owner-authorised is not
   determinable from artifacts I may read.
7. The maker's live lane behaviour under the successor wrapper: no live lane turn was dispatched here.

## 5. Overall

`PARTIALLY_VERIFIED`. The two harness repairs, the registry adjudication values, the TSV counts, the
no-manufacture check and the claim discipline all reproduce. The recorded magnitudes are low (D1), the
0-byte refutation's reasoning does not hold (D3), a stale measurement was carried forward (D4), the
side-effect audit's blanket statement is refuted by the tree's own write log (D5), and the artifact set
mutated during verification (D7).
