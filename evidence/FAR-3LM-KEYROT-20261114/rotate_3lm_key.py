#!/usr/bin/env python3
"""rotate_3lm_key.py — 3LM 車道憑證輪替（v2，已吸收 VERIFY 車道三項 FAIL）

設計原則
  1. 金鑰「值」只在記憶體與子程序環境中出現；輸出只給 sha256 前 12 碼與長度。
  2. 預設 dry-run（完整檢查＋探針，不寫檔）；`--apply` 才寫。
  3. 有效性判準只有一個：codex 探針（provider=opencode_go、model=deepseek-v4.1-flash）回固定字串。
     provider 的 /v1/models 對有效與無效 key 都回 403，不可當 gate（2026-11-14 實測）。
  4. 兩階段套用：plan（不寫）→ backup_all → probe → apply_plan。
     探針失敗時不改任何檔案，但仍寫收據（含 plan 與備份清單）。
  5. toolchain pin 預設唯讀報告；要寫入需 `--pin-refresh --i-approve-pin-change --apply`。

Exit codes（互斥）
  0 OK｜2 KEY_FILE_MISSING｜3 KEY_FILE_EMPTY｜4 KEY_FILE_CRLF｜5 KEY_FILE_MULTILINE
  6 MANIFEST_INVALID｜7 CONSUMER_PATTERN_MISS｜8 BACKUP_FAILED｜9 PROBE_FAILED
 10 PROBE_BINARY_MISSING｜11 PIN_REFRESH_NOT_APPROVED
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
MANIFEST = HERE / "3lm_consumers.json"
OUT_DIR = HERE.parent / "out"
CODEX_EXE = pathlib.Path(r"<HOST_HOME>/AppData/Local/OpenAI/Codex/bin/9e1da79431da526b/codex.exe")


def utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def fingerprint(value: str) -> dict:
    raw = value.encode("utf-8")
    return {"sha256_12": hashlib.sha256(raw).hexdigest()[:12], "len": len(raw)}


def die(code: int, label: str, detail: str = "") -> None:
    print(json.dumps({"code": label, "detail": detail, "verdict": "FAIL", "secret_printed": False},
                     ensure_ascii=False, indent=1))
    sys.exit(code)


def read_key(path: pathlib.Path) -> str:
    if not path.exists():
        die(2, "KEY_FILE_MISSING", str(path))
    raw = path.read_bytes()
    if b"\r" in raw:
        die(4, "KEY_FILE_CRLF", "檔案含 CR：請存成單行、無 CR 的 UTF-8")
    val = raw.decode("utf-8", "replace").strip().strip("\ufeff").strip()
    if not val:
        die(3, "KEY_FILE_EMPTY", "憑證檔為空")
    if "\n" in val:
        die(5, "KEY_FILE_MULTILINE", f"偵測到多行（{val.count(chr(10)) + 1} 行）；需單行")
    if len(val) < 16:
        die(5, "KEY_FILE_MULTILINE", f"長度={len(val)} < 16，疑似截斷")
    return val


def load_manifest() -> dict:
    if not MANIFEST.exists():
        die(6, "MANIFEST_INVALID", f"缺少 manifest: {MANIFEST}")
    try:
        man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        die(6, "MANIFEST_INVALID", f"{MANIFEST}: {e}")
    for k in ("credential", "consumers", "probe"):
        if k not in man:
            die(6, "MANIFEST_INVALID", f"缺少鍵 {k}")
    return man


def build_plan(man: dict, new_pointer: str) -> list:
    plan = []
    for c in man["consumers"]:
        p = pathlib.Path(c["file"])
        if not p.exists():
            die(7, "CONSUMER_PATTERN_MISS", f"{c['label']}: 檔案不存在 {p}")
        text = p.read_text(encoding="utf-8")
        m = re.search(c["pattern"], text)
        if not m:
            die(7, "CONSUMER_PATTERN_MISS", f"{c['label']}: 樣式未命中 {c['pattern']}")
        old = m.group(1)
        plan.append({"label": c["label"], "file": str(p), "pattern": c["pattern"],
                     "old": old, "new": new_pointer,
                     "changed": os.path.normcase(old) != os.path.normcase(new_pointer),
                     "restart": c.get("restart", ""),
                     "restart_required": c.get("restart_required", False)})
    return plan


def backup_all(plan: list, run_id: str) -> None:
    for item in plan:
        if not item["changed"]:
            continue
        src = pathlib.Path(item["file"])
        bak = src.with_suffix(src.suffix + f".bak-{run_id}")
        try:
            shutil.copy2(src, bak)
        except Exception as e:  # noqa: BLE001
            die(8, "BACKUP_FAILED", f"{src}: {e}")
        item["backup"] = str(bak)


def apply_plan(plan: list) -> None:
    for item in plan:
        if not item["changed"]:
            continue
        src = pathlib.Path(item["file"])
        text = src.read_text(encoding="utf-8")
        new_text = re.sub(item["pattern"],
                          lambda mm: mm.group(0).replace(item["old"], item["new"], 1),
                          text, count=1)
        if new_text == text:
            die(7, "CONSUMER_PATTERN_MISS", f"{item['label']}: 套用後內容未變")
        src.write_text(new_text, encoding="utf-8", newline="\n")
        item["sha256_after"] = hashlib.sha256(src.read_bytes()).hexdigest()


def probe(man: dict, key: str) -> dict:
    p = man["probe"]
    exe = str(CODEX_EXE) if CODEX_EXE.exists() else (shutil.which("codex") or "")
    if not exe:
        die(10, "PROBE_BINARY_MISSING", "找不到 codex 可執行檔")
    cmd = [exe] + list(p["command"][1:])
    env = dict(os.environ, **{man["credential"]["env_name_in_consumer"]: key})
    try:
        r = subprocess.run(cmd, env=env, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=420)
    except FileNotFoundError:
        die(10, "PROBE_BINARY_MISSING", exe)
    ok = (r.returncode == 0) and (p["expect_stdout_contains"] in (r.stdout or ""))
    return {"exit": r.returncode, "ok": ok,
            "stdout_sha12": hashlib.sha256((r.stdout or "").encode()).hexdigest()[:12],
            "stderr_len": len((r.stderr or "").encode()),
            "raw_output_stored": False}


def pin_report(rec: dict) -> None:
    cfg = pathlib.Path(r"<WORKSPACE>/FHS_NEXT/HG-KSEOS/config/hermes-codex-lane.json")
    try:
        d = json.loads(cfg.read_text(encoding="utf-8"))
        declared = pathlib.Path(str(d.get("codex_executable", "")))
        rec["pin_drift"] = {
            "declared_executable": d.get("codex_executable"),
            "declared_exists": declared.exists(),
            "declared_version": d.get("codex_version"),
            "installed_executable": str(CODEX_EXE),
            "installed_exists": CODEX_EXE.exists(),
            "action": "owner approval required: --pin-refresh --i-approve-pin-change --apply",
        }
    except Exception as e:  # noqa: BLE001
        rec["pin_drift"] = {"error": str(e)}


def apply_pin(rec: dict, run_id: str) -> None:
    cfg = pathlib.Path(r"<WORKSPACE>/FHS_NEXT/HG-KSEOS/config/hermes-codex-lane.json")
    d = json.loads(cfg.read_text(encoding="utf-8"))
    rec["pin_before"] = {k: d.get(k) for k in ("codex_executable", "codex_version", "codex_sha256")}
    bak = cfg.with_suffix(cfg.suffix + f".bak-{run_id}")
    shutil.copy2(cfg, bak)
    ver = subprocess.run([str(CODEX_EXE), "--version"], capture_output=True, text=True).stdout.strip()
    d["codex_executable"] = str(CODEX_EXE).replace("/", "\\")
    d["codex_version"] = ver.split()[-1] if ver else d.get("codex_version")
    d["codex_sha256"] = hashlib.sha256(CODEX_EXE.read_bytes()).hexdigest()
    cfg.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    rec["pin_backup"] = str(bak)
    rec["pin_after"] = {k: d.get(k) for k in ("codex_executable", "codex_version", "codex_sha256")}


def main() -> int:
    ap = argparse.ArgumentParser(description="3LM lane credential rotation (dry-run by default)")
    ap.add_argument("--key-file", help="新的憑證檔（預設沿用 manifest 的 current_pointer）")
    ap.add_argument("--apply", action="store_true", help="真的寫入（預設 dry-run：完整檢查＋探針，不寫）")
    ap.add_argument("--pin-refresh", action="store_true", help="同時檢查 codex binary pin（預設唯讀報告）")
    ap.add_argument("--i-approve-pin-change", action="store_true", help="寫入 pin 需 Owner 明確核准")
    a = ap.parse_args()

    man = load_manifest()
    key_path = pathlib.Path(a.key_file or man["credential"]["current_pointer"])
    key = read_key(key_path)
    run_id = utc()
    rec = {"schema": "FHS-3LM-ROTATION-RECEIPT/2", "run_id": run_id,
           "mode": "apply" if a.apply else "dry-run",
           "key_file": str(key_path), "key_fingerprint": fingerprint(key),
           "secret_printed": False, "order": "plan -> backup_all -> probe -> apply_plan"}

    def write_receipt(state: str) -> str:
        rec["state"] = state
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        rp = OUT_DIR / f"ROTATION_RECEIPT_{run_id}.json"
        rp.write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
        return str(rp)

    plan = build_plan(man, str(key_path))
    rec["plan"] = plan

    if a.pin_refresh and not a.i_approve_pin_change:
        pin_report(rec)
        rp = write_receipt("OK_PIN_DRIFT_REPORT_ONLY")
        print(json.dumps({"verdict": "PASS", "receipt": rp, "pin_drift": rec["pin_drift"],
                          "mutated": False, "secret_printed": False}, ensure_ascii=False, indent=1))
        return 0

    if a.apply:
        backup_all(plan, run_id)
        rec["backups_done"] = [c.get("backup") for c in plan if c["changed"]]

    pr = probe(man, key)
    rec["probe"] = pr
    if not pr["ok"]:
        rp = write_receipt("PROBE_FAILED_NO_MUTATION")
        print(json.dumps({"code": "PROBE_FAILED", "receipt": rp, "mutated": False,
                          "probe": pr, "secret_printed": False}, ensure_ascii=False, indent=1))
        return 9

    if a.pin_refresh and a.i_approve_pin_change and a.apply:
        apply_pin(rec, run_id)

    if a.apply:
        apply_plan(plan)
        rec["applied"] = [{"label": c["label"], "file": c["file"], "backup": c.get("backup"),
                           "sha256_after": c.get("sha256_after")} for c in plan if c["changed"]]
    else:
        rec["next"] = "確認後加 --apply：先備份、先探針、後套用；探針失敗不改檔"

    rp = write_receipt("OK")
    print(json.dumps({"verdict": "PASS", "receipt": rp, "mode": rec["mode"],
                      "changes": [{"label": c["label"], "changed": c["changed"]} for c in plan],
                      "probe_ok": pr["ok"], "mutated": bool(a.apply),
                      "secret_printed": False}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
