# -*- coding: utf-8 -*-
"""FAR self-research: web search on XQ automation + Windows UI automation best practices."""
import html
import re
import urllib.parse
import urllib.request
import time

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"ERR: {e}"

queries = [
    "XQ全球贏家 策略雷達 XScript 自動化 按鍵精靈 啟動策略",
    "Windows UI automation Afx MFC UIA deadlock workaround SendInput",
    "XQ 策略雷達 警示腳本 新增 加入 自動啟動",
    "cua-driver background automation user mouse conflict foreground",
]
for q in queries:
    t = fetch("https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q))
    if "anomaly" in t.lower() or "captcha" in t.lower():
        print(f"=== {q[:36]} === DDG blocked")
        time.sleep(4)
        continue
    links = re.findall(r'result__a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', t)
    snips = re.findall(r'result__snippet[^>]*>(.*?)</a>', t, re.S)
    print(f"=== {q[:36]} ===")
    for i, (u, txt) in enumerate(links[:4]):
        txt = html.unescape(re.sub(r"<[^>]+>", "", txt))
        print(f"  {i+1}. {txt[:70]}")
        if i < len(snips):
            s = html.unescape(re.sub(r"<[^>]+>", "", snips[i]))
            print(f"     {s[:150]}")
    print()
    time.sleep(3)
