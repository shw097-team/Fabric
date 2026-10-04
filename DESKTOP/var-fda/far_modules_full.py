# -*- coding: utf-8 -*-
"""FAR R1c: fetch FULL module list from xq.com.tw/module/ — all 10 modules."""
import html
import re
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0"
t = urllib.request.urlopen(urllib.request.Request("https://www.xq.com.tw/module/", headers={"User-Agent": UA}), timeout=30).read().decode("utf-8", errors="replace")
# save raw html for detailed parsing
open(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\xq_module_page.html", "w", encoding="utf-8").write(t)
print("saved, len:", len(t))

# extract module names — look for patterns like 模組名 + 描述
# modules likely listed with class or headings
txt = re.sub(r"<script.*?</script>", "", t, flags=re.S)
txt = re.sub(r"<style.*?</style>", "", t, flags=re.S)
txt = re.sub(r"<[^>]+>", "\n", txt)
txt = html.unescape(txt)
lines = [l.strip() for l in txt.splitlines() if l.strip()]
# find module-related lines
for i, l in enumerate(lines):
    if any(k in l for k in ("模組", "進階", "即時", "EOD", "選股", "量化", "自動交易", "回測", "XS", "盤中", "盤後", "期權", "海外", "訂閱", "點數")):
        print(f"{i}: {l[:80]}")
