# -*- coding: utf-8 -*-
"""FAR R2e: fetch XQ official blog (Gemini radar) + opop.tw automation tutorial."""
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

def clean(t):
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    t = re.sub(r"<style.*?</style>", "", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()

# XQ official blog
u1 = "https://www.xq.com.tw/xstrader/%E7%94%A8xqgemini%E5%AF%AB%E7%AD%96%E7%95%A5%E9%9B%B7%E9%81%94/"
t1 = fetch(u1)
if t1.startswith("ERR"):
    print("blog:", t1[:60])
else:
    txt = clean(t1)
    # find radar-related sentences
    for m in re.finditer(r"[^。]*策略雷達[^。]*。", txt):
        s = m.group(0).strip()
        if any(k in s for k in ("開啟", "啟動", "加入", "執行", "操作", "按")):
            print("BLOG:", s[:160])
    print("--- blog len:", len(txt))

# opop.tw automation tutorial
u2 = "https://opop.tw/xq-auto-screener-and-alerts/"
t2 = fetch(u2)
if t2.startswith("ERR"):
    print("opop:", t2[:60])
else:
    txt = clean(t2)
    for m in re.finditer(r"[^。]*策略雷達[^。]*。", txt):
        s = m.group(0).strip()
        if any(k in s for k in ("開啟", "啟動", "加入", "執行", "操作", "按", "設定")):
            print("OPOP:", s[:160])
    print("--- opop len:", len(txt))
