# -*- coding: utf-8 -*-
"""Search XQ '新增腳本' dialog structure — how to pick 警示腳本 type."""
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

# XQ official: find the 新增腳本/警示腳本 lesson
t = fetch("https://www.xq.com.tw/learn/xs/")
links = re.findall(r'href="([^"]+)"[^>]*>([^<]{4,80})</a>', t)
print("=== XQ XS LESSONS ===")
seen = set()
for u, txt in links:
    txt = html.unescape(txt.strip())
    if txt and ("警示" in txt or "新增" in txt or "編輯器" in txt) and u not in seen:
        seen.add(u)
        print("  ", txt[:60], "->", u[:90])
    if len(seen) >= 8:
        break

# DDG retry after pause
time.sleep(3)
t2 = fetch("https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(
    "XQ XS 新增腳本 警示腳本 如何選擇 類型"))
if "anomaly" not in t2.lower():
    links2 = re.findall(r'result__a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', t2)
    snips = re.findall(r'result__snippet[^>]*>(.*?)</a>', t2, re.S)
    print("\n=== DDG ===")
    for i, (u, txt) in enumerate(links2[:5]):
        txt = html.unescape(re.sub(r"<[^>]+>", "", txt))
        print(f"  {i+1}. {txt[:60]}")
        if i < len(snips):
            print("     ", html.unescape(re.sub(r"<[^>]+>", "", snips[i]))[:130])
else:
    print("\nDDG captcha")
