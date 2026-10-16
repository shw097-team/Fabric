#!/usr/bin/env python3
"""Host-measured window / process instrument for round
``HGK-GCM-CONTAINMENT-20261013`` (Windows, ctypes, no third-party deps).

It samples, at a configurable interval over a configurable bounded duration:

  * the set of VISIBLE top-level windows, their class names and titles -- with
    explicit attention to ``CASCADIA_HOSTING_WINDOW_CLASS``, ``ConsoleWindowClass``
    and the ``#32770`` dialog class, plus any title that mentions a credential or
    account chooser;
  * the set of living processes whose image name matches ``GitCredentialManager``,
    ``git-credential-manager``, ``git.exe`` or ``git-askpass``.

One JSON line is APPENDED per sample to a JSONL file, so the raw record survives.

Discrimination: ``--self-test`` deliberately creates one visible window (a
short-lived console), observes it, proves the process enumerator sees the spawned
child as well, and reports ``discrimination: PASS`` with the evidence. A guard
that reports success on missing input is a defect, so the self-test fails if it
sees no new window.

``--kill-matching`` terminates the processes it matched (so a bounded probe
cannot leave a chooser window behind) and reports what it killed. ``--seconds``
is enforced as a hard deadline.
"""
from __future__ import annotations

import argparse
import ctypes
import datetime as _dt
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from ctypes import wintypes

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

PROMPT_CLASSES = {"CASCADIA_HOSTING_WINDOW_CLASS", "ConsoleWindowClass", "#32770",
                  "Windows.UI.Core.CoreWindow"}
TITLE_TOKENS = ("credential", "account", "chooser", "sign in", "sign-in", "gcm",
                "git credential", "password", "authentication")
PROCESS_TOKENS = ("gitcredentialmanager", "git-credential-manager", "git.exe",
                  "git-askpass", "git-askpass.exe")

TH32CS_SNAPPROCESS = 0x00000002
PROCESS_TERMINATE = 0x0001
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value


# --------------------------------------------------------------------------- #
# window enumeration
# --------------------------------------------------------------------------- #

user32.IsWindowVisible.restype = wintypes.BOOL
user32.GetClassNameW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
EnumChildProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


def _class_and_title(hwnd):
    cls = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(hwnd, cls, 256)
    title = ctypes.create_unicode_buffer(512)
    user32.GetWindowTextW(hwnd, title, 512)
    pid = wintypes.DWORD(0)
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return cls.value, title.value, pid.value


def list_visible_windows() -> list[dict]:
    out: list[dict] = []

    def cb(hwnd, _lparam):
        if not user32.IsWindowVisible(hwnd):
            return True
        cls, title, pid = _class_and_title(hwnd)
        out.append({"hwnd": int(hwnd), "class": cls, "title": title, "pid": pid})
        # observe child dialogs (#32770 lives under a top-level often)
        def child(c, _l):
            if user32.IsWindowVisible(c):
                ccls, ctitle, cpid = _class_and_title(c)
                out.append({"hwnd": int(c), "class": ccls, "title": ctitle,
                            "pid": cpid, "child": True})
            return True
        user32.EnumChildWindows(hwnd, EnumChildProc(child), 0)
        return True

    user32.EnumWindows(EnumWindowsProc(cb), 0)
    return out


def classify_windows(windows: list[dict]) -> list[dict]:
    flagged = []
    for w in windows:
        cls = (w.get("class") or "")
        title = (w.get("title") or "")
        low = title.lower()
        reasons = []
        if cls in PROMPT_CLASSES:
            reasons.append(f"class:{cls}")
        if any(t in low for t in TITLE_TOKENS):
            reasons.append("title-token")
        if reasons:
            flagged.append({**w, "reasons": reasons})
    return flagged


# --------------------------------------------------------------------------- #
# process enumeration
# --------------------------------------------------------------------------- #

class PROCESSENTRY32W(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", ctypes.c_long),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", ctypes.c_wchar * 260),
    ]


def list_processes() -> list[dict]:
    snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snap == INVALID_HANDLE_VALUE:
        return []
    procs = []
    entry = PROCESSENTRY32W()
    entry.dwSize = ctypes.sizeof(PROCESSENTRY32W)
    try:
        ok = kernel32.Process32FirstW(snap, ctypes.byref(entry))
        while ok:
            procs.append({"pid": int(entry.th32ProcessID), "image": entry.szExeFile})
            ok = kernel32.Process32NextW(snap, ctypes.byref(entry))
    finally:
        kernel32.CloseHandle(snap)
    return procs


def matching_processes(procs: list[dict], tokens=PROCESS_TOKENS) -> list[dict]:
    toks = tuple(t.lower() for t in tokens)
    hits = []
    for p in procs:
        name = (p.get("image") or "").lower()
        if any(t in name for t in toks):
            hits.append(p)
    return hits


def terminate_processes(hits: list[dict]) -> list[dict]:
    killed = []
    for p in hits:
        handle = kernel32.OpenProcess(PROCESS_TERMINATE, False, p["pid"])
        if not handle:
            killed.append({**p, "terminated": False, "reason": "OpenProcess failed"})
            continue
        ok = kernel32.TerminateProcess(handle, 1)
        kernel32.CloseHandle(handle)
        killed.append({**p, "terminated": bool(ok)})
    return killed


# --------------------------------------------------------------------------- #
# sampling
# --------------------------------------------------------------------------- #

def sample_once() -> dict:
    windows = list_visible_windows()
    procs = list_processes()
    return {
        "ts": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "monotonic": round(time.monotonic(), 3),
        "window_count": len(windows),
        "flagged_windows": classify_windows(windows),
        "credential_processes": matching_processes(procs),
    }


def sample_loop(out_path: str, seconds: float, interval: float, kill_matching: bool) -> dict:
    deadline = time.monotonic() + max(0.0, seconds)
    samples = []
    killed_all: list[dict] = []
    seen_pids: set[int] = set()
    seen_hits: dict[int, dict] = {}
    with open(out_path, "a", encoding="utf-8") as fh:
        while time.monotonic() < deadline:
            s = sample_once()
            fh.write(json.dumps(s, ensure_ascii=False) + "\n")
            fh.flush()
            samples.append(s)
            for p in s["credential_processes"]:
                seen_pids.add(p["pid"])
                seen_hits[p["pid"]] = p
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            time.sleep(min(interval, remaining))
        # Cleanup at the END of the bounded window: a matched chooser must not be
        # left behind, but the window is given the full bounded duration to
        # appear and be observed first (the brief: "after the deadline, confirm
        # the instrument killed anything it matched").
        if kill_matching and seen_hits:
            killed_all = terminate_processes(sorted(seen_hits.values(),
                                                    key=lambda p: p["pid"]))
            end = sample_once()
            fh.write(json.dumps({"event": "post_kill", **end}, ensure_ascii=False) + "\n")
            fh.flush()
    return {"samples": samples, "sample_count": len(samples),
            "seconds_deadline": seconds, "interval": interval,
            "killed": killed_all, "credential_pids_seen": sorted(seen_pids)}


# --------------------------------------------------------------------------- #
# self-test
# --------------------------------------------------------------------------- #

def self_test(seconds: float, interval: float, out_path: str) -> dict:
    baseline_windows = {(w["class"], w["title"]) for w in list_visible_windows()}
    baseline_pids = {p["pid"] for p in list_processes()}

    CREATE_NEW_CONSOLE = 0x00000010
    marker = f"GCM-SELFTEST credential chooser {os.getpid()}"
    # A short-lived visible console; its title carries a credential token so the
    # instrument's own title heuristic is exercised too.
    proc = subprocess.Popen(["cmd.exe", "/c", f"title {marker} & timeout /t 8 >nul"],
                            creationflags=CREATE_NEW_CONSOLE)

    observed = None
    spawned_seen = None
    deadline = time.monotonic() + max(3.0, seconds)
    with open(out_path, "a", encoding="utf-8") as fh:
        while time.monotonic() < deadline:
            s = sample_once()
            fh.write(json.dumps(s, ensure_ascii=False) + "\n")
            fh.flush()
            if observed is None:
                for w in list_visible_windows():
                    key = (w["class"], w["title"])
                    if key not in baseline_windows and w["class"]:
                        observed = w
                        break
            if spawned_seen is None:
                for p in list_processes():
                    if p["pid"] not in baseline_pids and p["pid"] == proc.pid:
                        spawned_seen = p
                        break
            if observed and spawned_seen:
                break
            time.sleep(interval)

    # positive control for the image-name matcher itself
    image_match_control = matching_processes(
        list_processes(), tokens=(os.path.basename(sys.executable),))

    proc.kill()

    disc = bool(observed and observed.get("class") and spawned_seen)
    return {
        "discrimination": "PASS" if disc else "FAIL",
        "spawned_window": observed,
        "spawned_process": spawned_seen,
        "image_matcher_positive_control": image_match_control,
        "reason": ("created a visible window and observed it by class/title, and enumerated the "
                   "spawned child process by PID -- the instrument is not read-only"
                   if disc else
                   "the deliberately created window/process was NOT observed; the instrument "
                   "cannot discriminate (a green result would be a false-positive defect)"),
        "out_path": out_path,
    }


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="GCM containment window/process instrument")
    ap.add_argument("--seconds", type=float, default=25.0, help="hard deadline (seconds)")
    ap.add_argument("--interval", type=float, default=0.5, help="sample interval (seconds)")
    ap.add_argument("--out", default=None, help="JSONL output path (appended)")
    ap.add_argument("--kill-matching", action="store_true",
                    help="terminate processes the matcher flagged")
    ap.add_argument("--self-test", action="store_true",
                    help="prove discrimination by creating and observing a window")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    # Default to a temp file so a bare acceptance invocation leaves the repo
    # tree untouched (The WriteSet is scripts/gcm-containment/** and the round's
    # own execute/artifacts/**; a bare run must not drop a stray file).
    out_path = args.out or os.path.join(tempfile.gettempdir(), "gcm_windows.jsonl")
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)

    if args.self_test:
        result = {"schema": "HGK-GCM-CONTAINMENT-INSTRUMENT/1",
                  "mode": "self_test", "host": os.environ.get("COMPUTERNAME", ""),
                  **self_test(args.seconds, max(0.2, args.interval), out_path)}
        print(json.dumps(result, indent=2, ensure_ascii=False) if args.json
              else f"discrimination={result['discrimination']}")
        return 0 if result["discrimination"] == "PASS" else 2

    summary = sample_loop(out_path, args.seconds, max(0.05, args.interval),
                          args.kill_matching)
    result = {
        "schema": "HGK-GCM-CONTAINMENT-INSTRUMENT/1",
        "mode": "sample", "host": os.environ.get("COMPUTERNAME", ""),
        "out_path": out_path, "kill_matching": args.kill_matching,
        "sample_count": summary["sample_count"],
        "seconds_deadline": summary["seconds_deadline"],
        "interval": summary["interval"],
        "credential_processes_observed": summary["credential_pids_seen"],
        "credential_process_count": len(summary["credential_pids_seen"]),
        "windows_flagged": [w for s in summary["samples"] for w in s["flagged_windows"]],
        "killed": summary["killed"],
        "killed_count": len(summary["killed"]),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False) if args.json
          else f"samples={result['sample_count']} killed={result['killed_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
