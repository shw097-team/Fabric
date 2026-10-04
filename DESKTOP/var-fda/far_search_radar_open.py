# -*- coding: utf-8 -*-
"""FAR R2c: multi-source search — XQ radar open hotkey / command / automation tips."""
import html
import re
import urllib.parse
import urllib.request
import time

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"ERR: {e}"

def ddg(q, maxn=8):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
    t = fetch(url)
    if t.startswith("ERR"):
        return [f"{q}: {t[:50]}"]
    out = []
    for m in re.finditer(r'result__a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', t, re.S):
        href, title = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        out.append((html.unescape(title.strip())[:60], href[:90]))
        if len(out) >= maxn:
            break
    return out or [f"{q}: (empty)"]

queries = [
    "XQ 策略雷達 快捷鍵 開啟",
    "XQ 全球贏家 策略雷達 熱鍵",
    "XQ 策略雷達 開啟 方式 教學",
    "XQ 策略雷達 automation 自動化",
]
for q in queries:
    print(f"=== {q} ===")
    for t, h in ddg(q):
        print(f"  {t} | {h}")
    time.sleep(2)
