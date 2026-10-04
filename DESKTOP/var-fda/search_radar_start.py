# -*- coding: utf-8 -*-
"""DDG search: XQ radar start shortcut / toolbar button description."""
import html
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", errors="replace")

for q in [
    "XQ 策略雷達 啟動 快捷鍵 F5 執行",
    "XQ 策略雷達 功能列 按鈕 啟動 停止",
    "XQ 策略雷達 啟動 按鈕 在哪",
]:
    t = fetch("https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q))
    links = re.findall(r'result__a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', t)
    snips = re.findall(r'result__snippet[^>]*>(.*?)</a>', t, re.S)
    print(f"=== {q[:36]} ===")
    for i, (u, txt) in enumerate(links[:5]):
        txt = html.unescape(re.sub(r"<[^>]+>", "", txt))
        print(f"  {i+1}. {txt[:60]}")
        if i < len(snips):
            s = html.unescape(re.sub(r"<[^>]+>", "", snips[i]))
            print(f"     {s[:130]}")
    print()
