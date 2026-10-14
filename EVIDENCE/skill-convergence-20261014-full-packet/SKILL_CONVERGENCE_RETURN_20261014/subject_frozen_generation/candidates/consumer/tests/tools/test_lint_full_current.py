"""Focused tests for the additive full-current lint evidence in ``_attach_lint_findings``.

Scope of THIS turn is PARTIAL_PRIMITIVE_ONLY: only the primitive in
``tools/skill_manager_tool._attach_lint_findings`` (+ its representation helper). These tests
pin four properties:
  1. a standing finding stays in ``full_current_lint_findings`` even when the write introduces
     no new rule (delta empty -> no ``lint_warnings``), so old-warning visibility is additive;
  2. a genuinely clean evaluation reports ``EVALUATED`` with an explicit empty list;
  3. a linter import/evaluation failure reports ``UNAVAILABLE`` and never fabricates a clean list;
  4. the pre-existing delta/error result shape is unchanged for the existing callers.
"""

from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from tools.skill_manager_tool import (
    _attach_lint_findings,
    _create_skill,
    _patch_skill,
)

# Peer-shaped SKILL.md; body keeps a "## When to Use" section so lint is genuinely clean.
CLEAN_SKILL = """\
---
name: my-skill
description: Search arXiv papers by keyword, author, or ID.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [arxiv, research]
    related_skills: []
---

# My Skill

## Overview
Does a thing.

## When to Use
- When the user wants X.

## Procedure
1. Use `read_file` to load it.
"""

# Standing finding (no "When to Use"): any patch keeps this rule, so the delta stays empty.
STANDING_FINDING_CONTENT = """\
---
name: test-skill
description: A test skill for unit testing.
---

# Test Skill

Step 1: Do the thing.
"""


@contextmanager
def _skill_dir(tmp_path):
    """Search only ``tmp_path`` for skills (never the real ``~/.hermes/skills/``)."""
    with patch("tools.skill_manager_tool.SKILLS_DIR", tmp_path), \
         patch("agent.skill_utils.get_all_skills_dirs", return_value=[tmp_path]):
        yield


def _rules(dicts):
    return {d["rule"] for d in dicts}


def test_clean_evaluation_is_empty_and_evaluated(tmp_path):
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(CLEAN_SKILL, encoding="utf-8")
    result = {}
    _attach_lint_findings(result, skill_md)
    assert result["lint_evaluation_status"] == "EVALUATED"
    assert result["full_current_lint_findings"] == []
    assert "lint_warnings" not in result
    assert "lint_hint" not in result


def test_standing_finding_persists_in_full_when_delta_empty(tmp_path):
    # A tiny patch to VALID_SKILL_CONTENT changes nothing about the standing 'missing-section'
    # rule: the delta is empty (no lint_warnings, exactly as before), yet the full current list
    # additively exposes the standing warning the delta intentionally hides.
    with _skill_dir(tmp_path):
        _create_skill("my-skill", STANDING_FINDING_CONTENT)
        quiet = _patch_skill("my-skill", "Do the thing.", "Do the new thing.")
    assert quiet["success"] is True
    # Old, unchanged behavior: delta-only stays silent when no new rule was introduced.
    assert "lint_warnings" not in quiet
    assert "lint_hint" not in quiet
    # New, additive behavior: the standing finding is visible and evaluation is explicit.
    assert quiet["lint_evaluation_status"] == "EVALUATED"
    assert "missing-section" in _rules(quiet["full_current_lint_findings"])
    for finding in quiet["full_current_lint_findings"]:
        assert set(finding) == {"severity", "rule", "message"}
        assert finding["severity"] in ("error", "warning")


def test_delta_introduced_rule_rides_both_lists(tmp_path):
    from tools.skill_linter import _BODY_SOFT_BUDGET_CHARS
    filler = "- Prefer the native tool; the shell path loses the structured result.\n"
    with _skill_dir(tmp_path):
        _create_skill("my-skill", STANDING_FINDING_CONTENT)
        grown = _patch_skill("my-skill", "Do the thing.",
                             filler * (_BODY_SOFT_BUDGET_CHARS // len(filler) + 1))
    assert grown["success"] is True
    # Unchanged delta semantics: only the newly crossed rule is in lint_warnings ...
    assert "oversized-body" in _rules(grown["lint_warnings"])
    assert "missing-section" not in _rules(grown["lint_warnings"])
    # ... while the full list carries the whole current set.
    full = _rules(grown["full_current_lint_findings"])
    assert "oversized-body" in full and "missing-section" in full
    assert grown["lint_evaluation_status"] == "EVALUATED"


def test_evaluation_failure_is_unavailable_not_clean(tmp_path):
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(CLEAN_SKILL, encoding="utf-8")
    result = {}
    with patch("tools.skill_linter.lint_skill", side_effect=RuntimeError("boom")):
        _attach_lint_findings(result, skill_md)
    # Distinct from a clean evaluated empty list: status is UNAVAILABLE and no list is emitted.
    assert result["lint_evaluation_status"] == "UNAVAILABLE"
    assert "full_current_lint_findings" not in result
    assert "lint_warnings" not in result
    assert "lint_hint" not in result


def test_import_failure_is_unavailable(tmp_path, monkeypatch):
    import builtins
    real_import = builtins.__import__

    def _boom(name, *args, **kwargs):
        if name == "tools.skill_linter":
            raise ImportError("skill_linter missing")
        return real_import(name, *args, **kwargs)

    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(CLEAN_SKILL, encoding="utf-8")
    result = {}
    monkeypatch.setattr(builtins, "__import__", _boom)
    _attach_lint_findings(result, skill_md)
    assert result["lint_evaluation_status"] == "UNAVAILABLE"
    assert "full_current_lint_findings" not in result
    assert "lint_warnings" not in result


def test_original_error_result_shape_unchanged(tmp_path):
    # The attach helper does not touch error results: a rejected patch keeps its exact shape and
    # gains no lint keys (no regression in existing error compatibility).
    with _skill_dir(tmp_path):
        _create_skill("my-skill", STANDING_FINDING_CONTENT)
        rejected = _patch_skill("my-skill", "no-such-text-to-match", "x")
    assert rejected["success"] is False
    assert "error" in rejected
    assert "lint_evaluation_status" not in rejected
    assert "full_current_lint_findings" not in rejected
    assert "lint_warnings" not in rejected
