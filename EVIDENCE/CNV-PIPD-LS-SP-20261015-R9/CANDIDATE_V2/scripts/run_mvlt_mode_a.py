#!/usr/bin/env python3
"""
Template: Mode A (pure Hermes ephemeral) runner for MVLT-style A/B experiments.
Uses exact canonical Hermes config/credentials but with isolated HERMES_HOME.
Run with: python run_mvlt_mode_a.py
"""
import os, sys, json, subprocess, tempfile, time, hashlib
from pathlib import Path

# === USER CONFIG ===
INPUT_FILE = Path(r"C:\Projects\Agent_Workspace\var\mvlt\input.json")
OUTPUT_DIR = Path(r"C:\Projects\Agent_Workspace\var\mvlt\mode_a")
N_RUNS = 3

# === DERIVED ===
with open(INPUT_FILE, 'r') as f:
    input_content = f.read()
INPUT_SHA256 = hashlib.sha256(input_content.encode('utf-8')).hexdigest()

HERMES_EXE = str(Path(os.environ["LOCALAPPDATA"]).joinpath("hermes", "hermes-agent", "venv", "Scripts", "hermes.exe"))
CANONICAL_CONFIG = Path(os.environ["LOCALAPPDATA"]).joinpath("hermes", "config.yaml")
CANONICAL_ENV = Path(os.environ["LOCALAPPDATA"]).joinpath("hermes", ".env")

TASK_TEMPLATE = """Read the input file at {input_file} and produce a single artifact JSON at the given output path with schema MVLT-ARTIFACT/1 containing:
- schema: "MVLT-ARTIFACT/1"
- input_sha256: "{input_sha256}"
- computed_sha256: <sha256 of the input file content you read>
- field_count: <number of top-level keys in the input JSON>
- mode: "A"
- model: "deepseek-v4-flash"
- finished_at_utc: <ISO timestamp when done>

The artifact must be valid JSON. Use the write_file tool to write it to {output_file}.
Then reply ONLY with: DONE"""

def clean_env(home):
    e = dict(os.environ)
    for k in list(e):
        if k.startswith("HERMES_"):
            del e[k]
    e["HERMES_HOME"] = str(home)
    return e

def write_home(home, config_yaml, env_content):
    home.mkdir(parents=True, exist_ok=True)
    (home / "config.yaml").write_text(config_yaml, encoding="utf-8")
    (home / ".env").write_text(env_content, encoding="utf-8")

def run_one(run_num: int) -> dict:
    with tempfile.TemporaryDirectory(prefix=f"mvlt_mode_a_run{run_num}_") as tmpdir:
        hermes_home = Path(tmpdir) / "hermes_home"
        hermes_home.mkdir(parents=True)

        output_file = OUTPUT_DIR / f"artifact_{run_num}.json"

        config_yaml = CANONICAL_CONFIG.read_text() if CANONICAL_CONFIG.exists() else ""
        env_content = CANONICAL_ENV.read_text() if CANONICAL_ENV.exists() else ""

        write_home(hermes_home, config_yaml, env_content)

        task_prompt = TASK_TEMPLATE.format(
            input_file=INPUT_FILE,
            input_sha256=INPUT_SHA256,
            output_file=str(output_file).replace("\\", "\\\\")
        )

        e = clean_env(hermes_home)
        cmd = [HERMES_EXE, "chat", "-q", task_prompt, "-Q"]

        start = time.time()
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, env=e)
            wall_clock = round(time.time() - start, 2)
            artifact = None
            if output_file.exists():
                with open(output_file, 'r') as f:
                    artifact = json.load(f)
            return {
                "run": run_num,
                "exit_code": result.returncode,
                "wall_clock_s": wall_clock,
                "stdout": result.stdout[-2000:] if result.stdout else "",
                "stderr": result.stderr[-2000:] if result.stderr else "",
                "artifact_path": str(output_file),
                "artifact": artifact,
                "artifact_exists": output_file.exists()
            }
        except subprocess.TimeoutExpired:
            return {"run": run_num, "exit_code": 124, "wall_clock_s": 300.0, "error": "timeout", "artifact_path": str(output_file), "artifact_exists": False}
        except Exception as ex:
            return {"run": run_num, "exit_code": -1, "wall_clock_s": time.time() - start, "error": str(ex), "artifact_path": str(output_file), "artifact_exists": False}

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for i in range(1, N_RUNS + 1):
        print(f"Running Mode A run {i}/{N_RUNS}...")
        res = run_one(i)
        results.append(res)
        print(f"  exit_code={res['exit_code']}, wall_clock={res['wall_clock_s']}s, artifact_exists={res['artifact_exists']}")

    metrics = {
        "mode": "A",
        "runs": results,
        "input_sha256": INPUT_SHA256,
        "summary": {
            "successful_runs": sum(1 for r in results if r.get('exit_code') == 0 and r.get('artifact_exists')),
            "median_wall_clock": sorted([r['wall_clock_s'] for r in results if r['exit_code'] == 0])[1] if len([r for r in results if r['exit_code'] == 0]) >= 3 else None
        }
    }

    metrics_file = OUTPUT_DIR / "metrics_mode_a.json"
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    print(f"\nMode A complete. Metrics saved to {metrics_file}")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())