# -*- coding: utf-8 -*-
"""Search latest XQ radar usage (DDG + XQ official) — root-cause re-analysis."""
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
    "XQ 策略雷達 啟動 執行 快捷鍵 2024",
    "XQ全球贏家 策略雷達 怎麼啟動 新版",
    "XQ 策略雷達 啟動 按鈕 在哪 功能列",
]
for q in queries:
    t = fetch("https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q))
    links = re.findall(r'result__a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', t)
    snips = re.findall(r'result__snippet[^>]*>(.*?)</a>', t, re.S)
    print(f"=== {q[:34]} ===")
    for i, (u, txt) in enumerate(links[:5]):
        txt = html.unescape(re.sub(r"<[^>]+>", "", txt))
        print(f"  {i+1}. {txt[:65]}")
        if i < len(snips):
            s = html.unescape(re.sub(r"<[^>]+>", "", snips[i]))
            print(f"     {s[:150]}")
    print()
