# -*- coding: utf-8 -*-
"""FAR R1e: parse xq_module_compare.html for embedded JSON (module data) + API endpoints."""
import json
import re
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0"
t = open(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\xq_module_compare.html", encoding="utf-8").read()

# look for embedded JSON / module names / API endpoints
print("=== embedded module-ish tokens ===")
for m in re.finditer(r'"(module|Module|name|title|feature|price)[^"]*"\s*:\s*"([^"]{2,40})"', t):
    print("  ", m.group(1), "=", m.group(2))
print("\n=== api endpoints ===")
for m in re.finditer(r'["\'](/api/[^"\']+)["\']', t):
    print("  ", m.group(1))
print("\n=== script srcs ===")
for m in re.finditer(r'src="([^"]*\.js[^"]*)"', t):
    print("  ", m.group(1)[:100])
