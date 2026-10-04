# -*- coding: utf-8 -*-
"""FAR R1: XQ module/subscription structure — official pricing page research."""
import html
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"ERR: {e}"

def ddg(q, maxn=8):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
    t = fetch(url)
    if t.startswith("ERR"):
        return [(f"{q}: {t[:50]}", "")]
    out = []
    for m in re.finditer(r'result__a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', t, re.S):
        href, title = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        out.append((html.unescape(title.strip())[:70], href[:100]))
        if len(out) >= maxn:
            break
    return out or [(f"{q}: (empty)", "")]

queries = [
    "XQ 全球贏家 模組 訂閱 費用 台股進階",
    "XQ 盤中量化交易模組 價格",
    "XQ 個人版 模組 加購 策略雷達 自動交易",
    "XQ 企業版 模組 差異",
    "site:xq.com.tw 模組 訂閱",
    "XQ 自動交易中心 模組 訂閱",
]
for q in queries:
    print(f"=== {q} ===")
    for t, h in ddg(q):
        print(f"  {t} | {h}")
    print()
