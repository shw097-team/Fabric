# -*- coding: utf-8 -*-
"""FAR R1i: XQ official YouTube channel search + module page sub-paths."""
import html
import json
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

# 1. XQ official blog posts about modules (xq.com.tw/xstrader)
t = fetch("https://www.xq.com.tw/xstrader/")
if not t.startswith("ERR"):
    print("=== xstrader blog titles ===")
    for m in re.finditer(r'<a[^>]*href="(/xstrader/[^"]+)"[^>]*>(.*?)</a>', t, re.S):
        title = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if title and any(k in title for k in ("模組", "訂閱", "量化", "自動交易", "策略雷達", "選股")):
            print("  ", title[:60], "|", m.group(1)[:60])

# 2. module sub-pages
for path in ("/module", "/module-compare", "/module/盤中量化交易", "/module/台股進階"):
    t = fetch("https://www.xq.com.tw" + path)
    if t.startswith("ERR") or len(t) < 800:
        continue
    txt = re.sub(r"<[^>]+>", " ", t)
    txt = html.unescape(re.sub(r"\s+", " ", txt))
    m = re.search(r"(盤中量化交易|台股進階|自動交易|策略雷達|模組)(.{0,200})", txt)
    if m:
        print(f"=== {path} ===")
        print("  ", m.group(0)[:220])
