# -*- coding: utf-8 -*-
"""FAR R1m: fetch /feature/ page — feature->module mapping."""
import html
import re
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0"
t = urllib.request.urlopen(urllib.request.Request("https://www.xq.com.tw/feature/", headers={"User-Agent": UA}), timeout=25).read().decode("utf-8", errors="replace")
txt = re.sub(r"<script.*?</script>", "", t, flags=re.S)
txt = re.sub(r"<[^>]+>", "\n", txt)
txt = html.unescape(txt)
lines = [l.strip() for l in txt.splitlines() if l.strip()]
print(f"lines: {len(lines)}")
for i, l in enumerate(lines):
    if l and len(l) < 70 and any(k in l for k in ("模組", "量化", "選股", "雷達", "自動", "回測", "盤中", "盤後", "警示", "XS", "下單", "盯盤", "進階", "即時", "EOD", "期權", "海外", "資料", "監控")):
        print(f"{i}: {l}")
