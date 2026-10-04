# -*- coding: utf-8 -*-
"""UFO2 LLM backend canary — opencode-go (Hermes existing credential, in-memory only).
Reads API key from Hermes auth.json credential_pool at runtime; NEVER writes it
to any file. Sends ONE minimal chat_completion to opencode-go endpoint to prove
the LLM backend route works for UFO2.
"""
import json
import sys
from pathlib import Path

# load key in-memory only
auth = json.loads(Path(r"C:\Users\user\AppData\Local\hermes\auth.json").read_text(encoding="utf-8"))
cred = auth["credential_pool"]["opencode-go"][0]
API_KEY = cred.get("secret_value") or cred.get("api_key") or cred.get("key") or ""
BASE = cred.get("base_url", "https://opencode.ai/zen/go/v1")
print(f"base_url: {BASE} | key_len: {len(API_KEY)} | fields: {list(cred.keys())}")
