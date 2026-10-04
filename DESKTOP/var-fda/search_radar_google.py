# -*- coding: utf-8 -*-
"""Search XQ blog / forum for radar execution UI instructions."""
import html
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"ERR: {e}"

queries = [
    "site:blog.xq.com.tw 策略雷達 執行",
    "XQ 策略雷達 開放體驗 執行 按鈕 位置",
    "XQ全球贏家 策略雷達 如何啟動 執行",
]
for q in queries:
    t = fetch("https://www.google.com/search?q=" + urllib.parse.quote(q))
    clean = re.sub(r"<[^>]+>", " ", t)
    clean = html.unescape(re.sub(r"\s+", " ", clean))
    # strip script/style
    clean = re.sub(r"function[^{]*\{[^}]*\}", " ", clean)
    hits = re.findall(r"[^。；]{0,50}(?:策略雷達|開放體驗|執行按鈕|啟動)[^。；]{0,120}", clean)
    print(f"=== {q[:40]} ===")
    shown = 0
    for h in hits:
        h = h.strip()
        if len(h) > 40 and "XQ" in h or "雷達" in h:
            print("  ", h[:170])
            shown += 1
            if shown >= 3:
                break
    print()
