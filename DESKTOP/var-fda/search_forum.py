# -*- coding: utf-8 -*-
"""Fetch XQ forum threads about radar usage (start button location)."""
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

t = fetch("https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(
    "forum.xq.com.tw 策略雷達 使用 啟動 按鈕 綠色"))
links = re.findall(r'result__a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', t)
snips = re.findall(r'result__snippet[^>]*>(.*?)</a>', t, re.S)
for i, (u, txt) in enumerate(links[:6]):
    txt = html.unescape(re.sub(r"<[^>]+>", "", txt))
    print(f"{i+1}. {txt[:60]}")
    print(f"   {u[:120]}")
    if i < len(snips):
        s = html.unescape(re.sub(r"<[^>]+>", "", snips[i]))
        print(f"   {s[:140]}")
    print()
