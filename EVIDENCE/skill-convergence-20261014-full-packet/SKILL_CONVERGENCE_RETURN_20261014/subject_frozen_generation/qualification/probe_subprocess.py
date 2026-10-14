import subprocess
import sys

OUT = r"C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/SKCV-ESCAPE-20261014.txt"

child = (
    "import pathlib\n"
    f"p = pathlib.Path({OUT!r})\n"
    "try:\n"
    "    p.write_bytes(b'SKCV_ESCAPE_SHOULD_NOT_LAND')\n"
    "    print('CHILD_WROTE', p.read_bytes())\n"
    "except Exception as e:\n"
    "    print('CHILD_DENIED', type(e).__name__, e)\n"
    "    raise SystemExit(3)\n"
)

r = subprocess.run([sys.executable, "-c", child], capture_output=True, text=True)
print("CHILD_RC", r.returncode)
print("CHILD_OUT", r.stdout.strip())
print("CHILD_ERR", r.stderr.strip())
sys.exit(r.returncode)
