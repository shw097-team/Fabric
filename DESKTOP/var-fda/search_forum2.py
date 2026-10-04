# -*- coding: utf-8 -*-
"""Search XQ forum via DDG with different terms."""
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

for q in [
    "XQ策略雷達 執行 綠燈 啟動 停止 按鈕",
    "XQ 策略雷達 按開始 執行",
    "XQ全球贏家 策略雷達 啟動方法",
]:
    t = fetch("https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q))
    links = re.findall(r'result__a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', t)
    snips = re.findall(r'result__snippet[^>]*>(.*?)</a>', t, re.S)
    print(f"=== {q[:30]} ===")
    for i, (u, txt) in enumerate(links[:4]):
        txt = html.unescape(re.sub(r"<[^>]+>", "", txt))
        print(f"  {i+1}. {txt[:60]} | {u[:80]}")
        if i < len(snips):
            s = html.unescape(re.sub(r"<[^>]+>", "", snips[i]))
            print(f"     {s[:120]}")
    print()
