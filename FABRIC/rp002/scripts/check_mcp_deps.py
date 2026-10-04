# -*- coding: utf-8 -*-
"""Check which mcp dependencies exist in the canonical venv (clean env)."""
import subprocess, sys

VENV_PY = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\hermes-v020\venv\Scripts\python.exe"
mods = ["anyio", "httpx", "httpx_sse", "pydantic", "pydantic_core", "pydantic_settings",
        "sse_starlette", "starlette", "uvicorn", "mcp"]
env = {"PATH": r"C:\Projects\Agent_Workspace\HG-KSEOS\var\hermes-v020\venv\Scripts"}
import os
env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH",)}
for m in mods:
    p = subprocess.run([VENV_PY, "-c", f"import {m}; print('{m} OK', getattr({m}, '__file__', ''))"],
                       capture_output=True, text=True, timeout=60, env=env)
    print(p.stdout.strip() if p.returncode == 0 else f"{m} MISSING: {p.stderr.strip()[:80]}")
