# -*- coding: utf-8 -*-
"""FAR R3e: fetch XQ forum radar thread + check community repo for module requirements."""
import html
import re
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"ERR: {e}"

# 1. XQ forum — search via site fetch of thread listing
t = fetch("https://forum.xq.com.tw/category/")
if not t.startswith("ERR"):
    for m in re.finditer(r'href="(/thread/[^"]+)"[^>]*>([^<]{4,60})', t):
        if "策略" in m.group(2) or "雷達" in m.group(2) or "模組" in m.group(2):
            print("FORUM:", m.group(2).strip()[:50], "|", m.group(1)[:60])

# 2. community repo README — module requirements mentions
t2 = fetch("https://raw.githubusercontent.com/would2000/XQ-Auto-Writer-Skill/main/README.md")
if not t2.startswith("ERR"):
    for m in re.finditer(r"[^。\n]*(?:模組|訂閱|付費|加值|盤中量化|自動交易中心|策略雷達)[^。\n]*。?", t2):
        s = m.group(0).strip()
        if len(s) < 200:
            print("README:", s[:180])
