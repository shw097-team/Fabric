# -*- coding: utf-8 -*-
"""FAR R2: locate XQ 3.19.03 installer — official download page + archive candidates."""
import re
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0"

def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read() if binary else r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"ERR: {e}"

# 1. official download page
t = fetch("https://www.xq.com.tw/download/")
if not t.startswith("ERR"):
    print("=== xq.com.tw/download/ ===")
    for m in re.finditer(r'href="([^"]*(?:XQ|XQLite)[^"]*)"', t, re.I):
        print("  href:", m.group(1)[:120])
    # look for version mentions
    for m in re.finditer(r"(3\.\d{1,2}\.\d{1,2})", t):
        print("  version:", m.group(1))
else:
    print("download page:", t[:100])
