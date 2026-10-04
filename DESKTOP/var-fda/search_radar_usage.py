# -*- coding: utf-8 -*-
"""Search XQ radar usage via Google/Bing with urllib."""
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
    "XQ 策略雷達 試用版 執行 按鈕 啟動",
    "XQ 策略雷達 開放體驗 如何執行",
    "XQ 策略雷達 使用教學 啟動策略",
]
for q in queries:
    url = "https://www.bing.com/search?q=" + urllib.parse.quote(q)
    t = fetch(url)
    clean = re.sub(r"<[^>]+>", " ", t)
    clean = html.unescape(re.sub(r"\s+", " ", clean))
    # find snippets mentioning 雷達/執行
    hits = [m for m in re.findall(r"[^。；]{0,60}(?:策略雷達|開放體驗|執行)[^。；]{0,100}", clean) if len(m) > 30]
    print(f"=== {q[:30]} ===")
    for h in hits[:4]:
        print("  ", h.strip()[:160])
    print()
