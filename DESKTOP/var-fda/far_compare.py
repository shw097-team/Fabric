# -*- coding: utf-8 -*-
"""FAR R1d: fetch module-compare page — full module list + features matrix."""
import html
import re
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0"
t = urllib.request.urlopen(urllib.request.Request("https://www.xq.com.tw/module-compare", headers={"User-Agent": UA}), timeout=30).read().decode("utf-8", errors="replace")
open(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\xq_module_compare.html", "w", encoding="utf-8").write(t)
print("saved len:", len(t))

# extract module names + feature cells — look for structured blocks
txt = re.sub(r"<script.*?</script>", "", t, flags=re.S)
txt = re.sub(r"<style.*?</style>", "", t, flags=re.S)
txt = re.sub(r"<[^>]+>", "\n", txt)
txt = html.unescape(txt)
lines = [l.strip() for l in txt.splitlines() if l.strip()]
print(f"lines: {len(lines)}")
for i, l in enumerate(lines):
    if l and len(l) < 60 and any(k in l for k in ("模組", "進階", "即時", "EOD", "選股", "量化", "自動", "回測", "盤中", "盤後", "期權", "海外", "雲端", "手機", "XS", "點數", "盯盤", "策略", "雷達", "下單", "AI", "日報", "資料")):
        print(f"{i}: {l}")
