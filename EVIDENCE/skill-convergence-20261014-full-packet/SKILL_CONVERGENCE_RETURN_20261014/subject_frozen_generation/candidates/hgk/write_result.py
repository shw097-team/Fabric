import hashlib, json, os

ROOT = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\SKILL-CONVERGENCE-20261014\candidates\hgk"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def rsha(rel):
    return sha(os.path.join(ROOT, *rel.split("/")))


PY = ("C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0"
      "\\LocalCache\\Local\\hermes\\hermes-agent\\venv\\Scripts\\python.exe")

batch = json.load(open(os.path.join(ROOT, "topic_batch_1.json"), encoding="utf-8"))

result = {
    "schema": "SKCV-HGK-PHASE2-RESULT/1",
    "workorder": "WO-SKCV-20261014-HGK",
    "phase": "phase 2",
    "batch": 1,
    "theme": "external-evidence-closure",
    "maker": "Codex CLI (opencode-go/deepseek-v4.1-flash)",
    "shell": "pwsh (Windows)",
    "python": PY,
    "absorbed": [
        {
            "absorbed_path": e["absorbed_path"],
            "bytes": e["bytes"],
            "sha256": e["sha256"],
            "byte_offset": e["byte_offset"],
            "payload_byte_end": e["payload_byte_end"],
            "stub_path": e["stub_path"],
            "stub_sha256": rsha(e["stub_path"]),
        }
        for e in batch["absorbed"]
    ],
    "topic_file": {
        "path": batch["topic_file"]["path"],
        "bytes": batch["topic_file"]["bytes"],
        "sha256": batch["topic_file"]["sha256"],
    },
    "deliverables": {
        "topic_file": "skill/references/topics/external-evidence-closure.md",
        "stubs": [e["stub_path"] for e in batch["absorbed"]],
        "batch_json": "topic_batch_1.json",
        "checker": "topic_check.py",
        "result": "phase2_result.json",
    },
    "untouched": [
        "skill/SKILL.md",
        "entry_map.json",
        "skill/references/topics/construction-wave-and-remaining-procedures.md",
    ],
    "commands": [
        {"cmd": PY + " build_phase2.py",
         "exit_code": 0,
         "note": "wrote topic file, 5 stubs, topic_batch_1.json"},
        {"cmd": PY + " verify_bytes.py",
         "exit_code": 0,
         "note": "ALL_OK True: each segment == original bytes and recomputes to recorded sha256"},
        {"cmd": PY + " topic_check.py",
         "exit_code": 0,
         "note": "good case: status OK, 5 segments, 12 skill name tokens resolved"},
        {"cmd": PY + " topic_check.py --topic scratch\\negatives\\missing.md",
         "exit_code": 11, "note": "ERR_SKCV_SEGMENT_MISSING"},
        {"cmd": PY + " topic_check.py --topic scratch\\negatives\\duplicated.md",
         "exit_code": 12, "note": "ERR_SKCV_SEGMENT_DUPLICATED"},
        {"cmd": PY + " topic_check.py --topic scratch\\negatives\\reordered.md",
         "exit_code": 13, "note": "ERR_SKCV_SEGMENT_REORDERED"},
        {"cmd": PY + " topic_check.py --topic scratch\\negatives\\mutated.md",
         "exit_code": 14, "note": "ERR_SKCV_SEGMENT_MUTATED"},
        {"cmd": PY + " test_guards.py",
         "exit_code": 0,
         "note": "sandbox probes: GOOD OK; ERR_SKCV_STUB_MISMATCH(20), "
                 "ERR_SKCV_STUB_MISSING(20), ERR_SKCV_SKILL_NAME_UNRESOLVED(21)"},
        {"cmd": PY + " refcount.py",
         "exit_code": 0,
         "note": "after: recursive=113 top-level=111"},
    ],
    "checker_ran": {
        "good_case": 1,
        "negative_probes": 4,
        "extra_guard_probes": 3,
    },
    "checker_skipped": 0,
    "typed_refusals_observed": [
        "ERR_SKCV_SEGMENT_MISSING",
        "ERR_SKCV_SEGMENT_DUPLICATED",
        "ERR_SKCV_SEGMENT_REORDERED",
        "ERR_SKCV_SEGMENT_MUTATED",
        "ERR_SKCV_STUB_MISSING",
        "ERR_SKCV_STUB_MISMATCH",
        "ERR_SKCV_SKILL_NAME_UNRESOLVED",
    ],
    "reference_file_count": {
        "root": "skill/references",
        "before": {"recursive": 112, "top_level": 111},
        "after": {"recursive": 113, "top_level": 111},
        "delta": {
            "recursive": 1,
            "top_level": 0,
            "explanation": ("the 5 original reference files were replaced 1:1 by "
                            "one-line stubs (top-level count unchanged at 111); one new "
                            "topic file was added under topics/ (recursive 112 -> 113)"),
        },
        "count_claim": "the physical reference-file count did NOT fall; it rose by 1",
    },
    "remaining_themes": {
        "statement": ("This is batch 1 of the SKCV-HGK reference themes. All remaining "
                      "HGK reference themes stay OPEN; no other theme was absorbed, and no "
                      "whole-tree consolidation was performed."),
        "status": "OPEN",
    },
    "nonclaims": [
        "no canonical acceptance / promotion / release claim",
        "no cap, threshold, linter, lock or policy change",
        "no underscored/hidden files created",
        "no deletion; the 5 original paths now carry pointer stubs",
        "no whole-tree scan; only the 6 permitted files were read",
    ],
}

with open(os.path.join(ROOT, "phase2_result.json"), "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("wrote phase2_result.json")
