# -*- coding: utf-8 -*-
"""FAR R1g: scan ALL astro chunks of /module page for module names + features."""
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

t = fetch("https://www.xq.com.tw/module")
if t.startswith("ERR"):
    print("module page:", t[:60])
    raise SystemExit(2)

# all scripts + link preloads
scripts = re.findall(r'<(?:script[^>]*src|link[^>]*href)="([^"]*_astro/[^"]+\.js)"', t)
print("astro chunks:", len(scripts))
allnames = set()
for src in set(scripts):
    if not src.startswith("http"):
        src = "https://www.xq.com.tw" + src
    js = fetch(src)
    if js.startswith("ERR"):
        continue
    # module names: Chinese 2-10 chars followed by 模組 or standalone module names
    for m in re.finditer(r'[\u4e00-\u9fff]{2,12}模組', js):
        allnames.add(m.group(0))
    # feature keywords
    for m in re.finditer(r'"(?:盤中量化交易|策略雷達|自動交易中心|選股中心|盤後選股|雲端監控|XScript|XS編輯器|回測中心|即時行情|海外行情|期權|大戶投|點數|盯盤|雷達|警示)"', js):
        allnames.add(m.group(1))
    # prices
print("=== module names found ===")
for n in sorted(allnames):
    print("  ", n)
