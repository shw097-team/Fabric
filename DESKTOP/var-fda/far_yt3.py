# -*- coding: utf-8 -*-
"""FAR R2e: fetch 策略模組 video description + search 10-module list."""
import html
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"ERR: {e}"

def yt(q, n=10):
    t = fetch("https://www.youtube.com/results?search_query=" + urllib.parse.quote(q))
    if t.startswith("ERR"):
        return []
    vids = re.findall(r'"videoId":"([^"]+)"', t)
    titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"', t)
    return list(zip(vids, titles))[:n]

# 1. 策略模組 video description
vid = None
for v, ti in yt("XQ 策略模組 盤中大量監控個股"):
    vid = v
    break
if vid:
    t = fetch(f"https://www.youtube.com/watch?v={vid}")
    if not t.startswith("ERR"):
        desc = re.search(r'"shortDescription":"(.*?)","isCrawlable', t, re.S)
        if desc:
            d = desc.group(1).encode().decode("unicode_escape", errors="replace")
            print("=== 策略模組 video desc ===")
            print(d[:1500])

# 2. search for explicit module list
print("\n=== searches for module list ===")
for q in ("XQ 模組 清單 10種", "XQ 全球贏家 模組 有哪些 訂閱方案", "XQ 個人版 模組 全部 列表"):
    print(f"--- {q}")
    for v, ti in yt(q, 6):
        print(f"  {ti[:60]} | {v}")
