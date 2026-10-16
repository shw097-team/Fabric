# External-challenge closure round (EXT-FDA-001..008 pattern, verified 2026-08-13)

After an external `PARTIAL_CHALLENGE` review returns `EVIDENCE_GAP` findings on the
submitted evidence MD, the resume is a **smallest-repair evidence closure**, not a
rebuild. This is the FDA round's recipe (same family as the R1-EVIDENCE_ONLY round
in `external-evidence-closure.md`, but with the subject-root + raw-bundle + DoD-matrix
extensions the FDA external reviewer demanded).

## What external reviewers actually fail you on

| Finding class | What they need |
|---|---|
| EXT-FDA-001 "no exact frozen subject root" | ONE `FINAL_GIT_HEAD` (or package digest) the whole evidence set binds to, recomputable by `git checkout <head>` |
| EXT-FDA-002 "51 raw artifacts not submitted" | RAW bytes of every artifact (a review bundle), not a hash pointer table |
| EXT-FDA-003 "checker denominator conflict" | ONE current denominator (e.g. 146), embedded fresh-run receipt, no stale value |
| EXT-FDA-004 "DoD pass-list self-contradiction" | Full 36-row machine matrix, no omitted IDs, PASS/PARTIAL/BLOCKED mutually consistent |
| EXT-FDA-005/006 "runtime gate not closed" | Either close it (see UFO2 below) or keep it HONESTLY BLOCKED/PARTIAL with the authority-gate owner named |

## Subject root via git commits (EXT-FDA-001)

Freeze identity by committing, not by hashing files in a dirty tree:

```bash
cd Fabric
git add fabric-desktop-automation/ profiles/fabric-desktop-cua/ profiles/fabric-desktop-ufo2/ \
        rp002/RP002_PROFILE_TEAM_MANIFEST.yaml rp002/RP002_TOOL_AND_INHERITED_CAPABILITY_MATRIX.yaml
git commit -m "FDA (WO-...): ..."
git rev-parse HEAD        # -> subject root; external verifier can git checkout this
```

Two-commit model (avoids the self-referential MD-embeds-own-HEAD loop):
- commit 1: all artifacts + evidence MD
- commit 2: EvidenceManifest + raw review bundle (manifest lives in the bundle dir)
- final HEAD = subject root; the evidence MD cites the artifact commit, not the
  commit that contains the MD itself. If the MD's text must mention the final HEAD,
  accept that the MD's own hash is a separate evidence artifact (never embed the MD's
  own hash in its body — single-direction binding).

## Raw review bundle + EvidenceManifest (EXT-FDA-002)

External reviewers cannot re-verify hash pointers without the bytes. Build:

```
Fabric/evidence/review/FDA_RAW_REVIEW_BUNDLE/
  FDA_EVIDENCE_MANIFEST.json     # generated LAST
  BUNDLE_INDEX.md
  <mirror of every artifact path>  # byte copies (cp), not symlinks
```

Manifest binds, per artifact: `path`, `sha256`, `size`; plus `subject_root.git_head`,
a fresh checker run (`verdict/checks/failed/run_at`), a fresh tests run, the DoD-36
matrix, and the claim ceiling. Manifest `sha256` is the bundle's own identity.

Generator pitfalls (all hit live):
- Path prefixes: `RAW_PATHS` must be repo-relative (`Fabric/fabric-desktop-automation/...`,
  `HG-KSEOS/var/fda/...`) against the workspace ROOT — omitting `Fabric/` reports all
  artifacts MISSING.
- `python -m unittest discover` writes "Ran N tests" to **stderr**, not stdout —
  combine `stdout + "\n" + stderr` before regex.
- Checker counts GROW as receipts are added (each new receipt file adds no-secret
  checks) — the denominator is a fresh-run snapshot, never a stale number from an
  earlier freeze. Regenerate the manifest at the END.

## Checker denominator (EXT-FDA-003)

Symptom: evidence MD said `checks: 126`, fresh run says `144`/`146`. Root cause: the
MD was generated at an earlier freeze and the checker grew. Fix: single current value
everywhere (MD §4 + manifest + verifier checklist), and note the old value was stale.
Never "pick" a denominator — run the checker once more and record that exact output.

## DoD-36 machine matrix (EXT-FDA-004)

Symptom: evidence MD claimed "DoD items 1–16 verified PASS" while also listing
UFO2 effective-load BLOCKED (DoD-13 ∈ 1..16) — a confirmed report-semantics defect.
Fix: materialize the full 36-row table with machine predicates, no omitted IDs
(21/22/25 were silently dropped in an earlier version), and explicit
PASS/PARTIAL/BLOCKED per row. Summary line `PASS=N PARTIAL=M BLOCKED=K` must equal
the row count. Keep DoD-17/35 PARTIAL honest with the authority-gate owner named.

## UFO² effective-load does NOT need an external API key (EXT-FDA-005 correction)

The earlier `BLOCKED_HITL (LLM API key = credential)` claim was OVER-CONSERVATIVE.
UFO² v3.0.8 supports three no-key paths:
- **Ollama local**: `API_TYPE: "ollama"`, `API_BASE: http://localhost:11434`,
  `API_KEY: "ollama"` (placeholder, not used)
- **Custom model**: subclass `ufo.llm.base.BaseService` (see `ufo/llm/placeholder.py`)
- **PlaceHolderService**: no-LLM module/config/UIA-backend verification mode

Effective-load probe = import package + import `ufo.llm.*` + instantiate
`PlaceHolderService` + import `ufo.automator.ui_control` + parse `config/ufo/system.yaml`
+ import `app_agent`/`host_agent` → 7/7 PASS.

### opencode-go as UFO² LLM backend (user-authorized, verified live)

- Hermes credential: `hermes_cli.config.get_env_value_prefer_dotenv("OPENCODE_GO_API_KEY")`
  (reads `AppData\Local\hermes\.env`); key never written to any file/evidence.
- **URLLIB IS BLOCKED**: `urllib.request` to `https://opencode.ai/zen/go/...` → `HTTP 403
  error code: 1010` (Cloudflare browser-signature block). This is NOT a bad key —
  the OpenAI SDK works: `OpenAI(api_key=key, base_url="https://opencode.ai/zen/go/v1")`,
  `chat.completions.create(model="deepseek-v4-flash", ...)` → 200, finish=stop.
- `max_tokens` too small (≤16) on deepseek-v4-flash returns `finish=length` + empty
  content — use ≥256 for canaries.
- Record in the receipt: base_url + model + `key_storage: Hermes dotenv; never written`.

### UFO² dependency install (venv, verified)

- `env -u PYTHONPATH` before any venv python (global hermes path shadows site-packages).
- `pip install --target .venv\Lib\site-packages <pkg>` — plain `pip install` under the
  shadowed env silently installs to the wrong place (`six` import failed until --target).
- pywinauto needs `pywin32_postinstall.py -install` + DLLs:
  `cp .venv\Lib\site-packages\pywin32_system32\pythoncom312.dll pywintypes312.dll .venv` (root).
- **langchain conflict**: UFO² v3.0.8 requires `langchain.docstore.document` (removed in
  langchain ≥0.3) → install `langchain==0.2.17 + langchain-community==0.2.19 +
  langchain-core==0.2.43`; uninstall the 0.3/1.x residue first (mixed dist-info dirs
  shadow the 0.2 package).

## XQ strategy radar PAPER runtime (EXT-FDA-006 — CLOSED 2026-08-14)

- Trial-mode radar: menu 策略(D) → 策略雷達(開放體驗)(L) → the 試用說明 dialog is a
  Win32 dialog invisible to UIA — dismiss with `press_key return` ("我知道了").
- Trial radar's strategy library is EMPTY (folder categories exist, no leaf nodes;
  search "KD" returns nothing). System strategies are read-only in trial
  (`請複製成自訂策略才能修改內容`). PAPER start/stop therefore cannot run on the
  trial subject — record `QUALIFIED_SURFACE / RUNTIME_START_STOP_BLOCKED_TRIAL_LIBRARY_EMPTY`
  and name the unblock owner (SQS/XQ PAPER fixture authority) per the external
  finding's `earliest_owner`. Do NOT fake a run; 0 wrong action / 0 broker write stays.
- **CLOSURE (verified 2026-08-14, NOT trial-era speculation):** subscribing the
  **盤中量化交易模組** (個人版策略雷達所在的加值模組) makes custom strategies
  **persist across XQ restart** and removes the 開放體驗警示 notice. DoD-17 then
  closes via the **SensorLog truth layer**, NOT the radar UI (XTP grid is
  uia-invisible): `DAQXQLITE_SHW097_SensorLog.sqlite` Table_YYYYMMDD records the
  full execution state machine per strategy (XSSensorState 2→3→1, ExecState 1→8,
  SymbolID, TriggerTime) — 56 records across 3 FDA strategies. Full recipe:
  `references/xq-radar-paper-runtime.md` §3b.

## External RE-REVIEW single-file packaging (r2 pattern, verified 2026-08-14)

When the reviewer asks "確認 previous findings 是否都已解決" (or the user asks for
ONE consolidated file for a second review), produce a **single self-contained
re-review evidence MD** — the answer to every prior finding + the full current
evidence, in one file, with NO local-path dependency (reviewer can't open MEDIA):

1. **Per-finding closure block** — one section per EXT-FDA-XXX: review requirement
   (quote) → closure evidence (concrete: commit hash, counts, receipt content) →
   external re-verify instruction (exact command the reviewer runs). Mark each
   CLOSED; keep genuinely-open items in a 誠實保留 section (e.g. 盤中觸發視覺驗證
   time-gated) — never promote FAIL_CLOSED yourself.
2. **Self-contained contract** — include the DoD matrix, checker denominator,
   raw-bundle manifest sha256, XQ fingerprint, and a 10-row external-verifier
   checklist (git rev-parse / sha256sum / checker rerun / SensorLog read) all inline.
3. **Finalize-sha loop** (the sha must be IN the file AND cover the file):
   write MD with placeholder → sha256 the file → patch placeholder (header yaml +
   body) with the real sha → re-hash → that final sha is the file's identity.
4. **Mirror byte-identical ×3** (Fabric/HGK/SQS evidence\review) + update
   EvidenceManifest subject_root to the CURRENT HEAD (not the last artifact commit)
   and append the re-review MD to the manifest artifacts. Verify equality with a
   3-way hash check (evidence MD itself stays 4-way).
5. Commit: subject root moves forward (e.g. cf24b65 → 75499ba) — the re-review MD
   is a NEW artifact; the frozen subject for the reviewer is the new HEAD.

Trap: keep the re-review MD's claim ceiling identical to the evidence MD's
(FDA_PROFILE_TEAM_ACTIVE stays FAIL_CLOSED until the EXTERNAL verdict — the file
answers the review, it does not self-accept).

