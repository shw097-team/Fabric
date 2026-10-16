"""RED driver: drive the EXISTING production guard/registry, print observed behaviour.

Not a test-suite run. It exercises scripts/hgk-lane-guard.py::evaluate against a registry
fixture built from the live registry, exactly as a real pre-dispatch call would.
Run with cwd = the round candidate root.
"""
import copy
import importlib.util
import json
import pathlib
import tempfile

ROOT = pathlib.Path.cwd()

_spec = importlib.util.spec_from_file_location("hgk_lane_guard", ROOT / "scripts" / "hgk-lane-guard.py")
guard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(guard)

_spec2 = importlib.util.spec_from_file_location("lane_policy_mod", ROOT / "src" / "hg_kseos" / "lane_policy.py")
lp = importlib.util.module_from_spec(_spec2)
_spec2.loader.exec_module(lp)


def _fixture(path, model, provider, engine):
    path.write_text(json.dumps({
        "status": "ADMITTED",
        "arm": {"engine": engine, "model": model, "provider": provider},
        "served": {"engine": engine, "model": model, "provider": provider},
    }), encoding="utf-8")
    return str(path)


def _registry_with_pair(tmp, *, status, distinct_required):
    """Copy the live registry, force the EXECUTE/VERIFY pair declaration, re-pin the source digest."""
    reg = copy.deepcopy(lp.load_registry())
    reg["source_of_routes"]["sha256"] = lp._sha256_file(ROOT / reg["source_of_routes"]["path"])
    for pair in reg["sod_invariants"]["pairs"]:
        if {pair.get("maker"), pair.get("checker")} == {"EXECUTE", "VERIFY_SECURITY"}:
            pair["distinct_required"] = distinct_required
    for conflict in reg["sod_invariants"]["declared_conflicts"]:
        if conflict.get("id") == "SOD006-C3":
            conflict["status"] = status
    path = tmp / "registry_fixture.json"
    path.write_text(json.dumps(reg), encoding="utf-8")
    return str(path)


def evaluate(argv):
    return guard.evaluate(guard.build_parser().parse_args(argv))


def main():
    tmp = pathlib.Path(tempfile.mkdtemp())
    fix = _fixture(tmp / "adm.json", "deepseek-v4.1-flash", "opencode-go", "hermes")
    same_arm = ["--lane", "VERIFY_SECURITY", "--maker-engine", "opencode-go",
                "--maker-model", "deepseek-v4.1-flash", "--target-engine", "hermes",
                "--target-model", "deepseek-v4.1-flash", "--target-provider", "opencode-go",
                "--admission", fix]
    distinct_arm = ["--lane", "VERIFY_SECURITY", "--maker-engine", "opencode-go",
                    "--maker-model", "glm-5.3-flash", "--target-engine", "hermes",
                    "--target-model", "deepseek-v4.1-flash", "--target-provider", "opencode-go",
                    "--admission", fix]

    print("== CASE 1: live registry, undeclared same-model pair ==")
    v = evaluate(same_arm)
    print("exit_code:", v["exit_code"], "errors:", v["errors"])
    print("declared_conflict in verdict:", "declared_conflict" in v)

    print("== CASE 2: fixture declares SOD006-C3 OWNER_ORDERED_IN_FORCE + distinct_required=false ==")
    reg = _registry_with_pair(tmp, status="OWNER_ORDERED_IN_FORCE", distinct_required=False)
    v = evaluate(same_arm + ["--registry", reg, "--root", str(ROOT)])
    print("exit_code:", v["exit_code"], "errors:", v["errors"])
    print("declared_conflict in verdict:", "declared_conflict" in v)

    print("== CASE 3: distinct pair ==")
    v = evaluate(distinct_arm)
    print("exit_code:", v["exit_code"], "declared_conflict present:", "declared_conflict" in v)

    print("== CASE 4a: declared but distinct_required still true ==")
    reg = _registry_with_pair(tmp, status="OWNER_ORDERED_IN_FORCE", distinct_required=True)
    v = evaluate(same_arm + ["--registry", reg, "--root", str(ROOT)])
    print("exit_code:", v["exit_code"], "errors:", v["errors"])

    print("== CASE 4b: distinct_required false but status not OWNER_ORDERED_IN_FORCE ==")
    reg = _registry_with_pair(tmp, status="SUPERSEDED", distinct_required=False)
    v = evaluate(same_arm + ["--registry", reg, "--root", str(ROOT)])
    print("exit_code:", v["exit_code"], "errors:", v["errors"])


if __name__ == "__main__":
    main()
