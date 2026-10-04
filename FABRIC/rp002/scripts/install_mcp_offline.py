# -*- coding: utf-8 -*-
"""CF1 — offline install of mcp SDK + missing pure-python deps into canonical venv (rollback = delete)."""
import os, shutil, subprocess, sys
from pathlib import Path

SRC = Path(r"C:\Users\user\AppData\Local\hermes\hermes-agent\venv\Lib\site-packages")
DST = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\hermes-v020\venv\Lib\site-packages")
PACKAGES = ["mcp", "mcp-1.28.1.dist-info", "httpx_sse", "httpx_sse-0.4.3.dist-info",
            "pydantic_settings", "pydantic_settings-2.14.2.dist-info",
            "sse_starlette", "sse_starlette-3.3.2.dist-info",
            "jsonschema", "jsonschema-4.26.0.dist-info",
            "jsonschema_specifications", "jsonschema_specifications-2025.9.1.dist-info",
            "referencing", "referencing-0.37.0.dist-info",
            "rpds", "rpds_py-0.30.0.dist-info",
            "attrs", "attrs-25.4.0.dist-info"]

installed = []
for pkg in PACKAGES:
    src = SRC / pkg
    dst = DST / pkg
    if dst.exists():
        continue
    if not src.exists():
        print(f"MISSING_SRC {pkg}")
        sys.exit(1)
    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)
    installed.append(pkg)

print("INSTALLED", installed)
# verify import under clean env
env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
p = subprocess.run([str(DST.parent.parent / "Scripts" / "python.exe"), "-c",
                    "import mcp; from mcp.server.fastmcp import FastMCP; print('MCP_IMPORT_OK', mcp.__version__ if hasattr(mcp,'__version__') else '1.28.1')"],
                   capture_output=True, text=True, timeout=60, env=env)
print(p.stdout.strip() or p.stderr.strip())
sys.exit(0 if p.returncode == 0 else 1)
