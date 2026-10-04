# -*- coding: utf-8 -*-
"""FAR R1b: fetch XQ official pages directly — pricing/module pages."""
import html
import re
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"ERR: {e}"

def clean(t):
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    t = re.sub(r"<style.*?</style>", "", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()

candidates = [
    ("https://www.xq.com.tw/", "home"),
    ("https://www.xq.com.tw/pricing/", "pricing"),
    ("https://www.xq.com.tw/price/", "price"),
    ("https://www.xq.com.tw/subscription/", "subscription"),
    ("https://www.xq.com.tw/module/", "module"),
    ("https://www.xq.com.tw/plan/", "plan"),
]
for url, tag in candidates:
    t = fetch(url)
    if t.startswith("ERR") or len(t) < 500:
        print(f"{tag} ({url}): {t[:60] if t.startswith('ERR') else 'too short'}")
        continue
    txt = clean(t)
    print(f"=== {tag} ({url}) len={len(txt)} ===")
    # find module/price keywords
    for kw in ("模組", "訂閱", "盤中量化", "台股進階", "自動交易", "策略雷達", "選股中心", "XS", "費用", "月費", "方案"):
        idxs = [m.start() for m in re.finditer(kw, txt)]
        for i in idxs[:2]:
            print(f"  [{kw}] ...{txt[max(0,i-60):i+100]}...")
    print()
