"""Focused test: the edit/apply write path CONSULTS the existing lint primitive.

Phase 3 wires a bounded reader (skill_manager_tool._consult_skill_lint) into the
edit/apply action and forwards its two keys through batch mode. This proves the reader
fires for an oversized subject and reports exactly the findings the primitive returns
when called directly - no second linter, no cap/threshold change.
"""

import json
from contextlib import contextmanager
from unittest.mock import patch

from tools.skill_linter import lint_skill, _BODY_SOFT_BUDGET_CHARS
from tools.skill_manager_tool import (
    _create_skill,
    _edit_skill,
    _lint_finding_repr,
)
from tools.skill_manager_batch import _skill_manage_batch

FRONTMATTER = """\
---
name: big-skill
description: A skill whose SKILL.md body is oversized for test purposes.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [test]
    related_skills: []
---

# Big Skill

## When to Use
- When the reader must observe an oversized subject.
"""

# Body comfortably past the soft budget so oversized-body is the rule under test.
_OVERSIZED_BODY = ("- Prefer the native tool; the shell path loses the structured result.\n"
                   * (_BODY_SOFT_BUDGET_CHARS // 60 + 40))


@contextmanager
def _skill_dir(tmp_path):
    """Search only tmp_path for skills (never the real ~/.hermes/skills/)."""
    with patch("tools.skill_manager_tool.SKILLS_DIR", tmp_path), \
         patch("agent.skill_utils.get_all_skills_dirs", return_value=[tmp_path]):
        yield


def _rules(dicts):
    return {d["rule"] for d in dicts}


def test_edit_reader_fires_for_oversized_subject_and_matches_primitive(tmp_path):
    oversized = FRONTMATTER + _OVERSIZED_BODY
    with _skill_dir(tmp_path):
        _create_skill("big-skill", FRONTMATTER)
        skill_md = tmp_path / "big-skill" / "SKILL.md"
        # The edit/apply path: a full rewrite that pushes the body past the soft budget.
        result = _edit_skill("big-skill", oversized)
        assert result["success"] is True
        # Reader fired: explicit status + the full current finding set.
        assert result["lint_evaluation_status"] == "EVALUATED"
        assert "oversized-body" in _rules(result["full_current_lint_findings"])
        # Same findings the primitive returns when consulted directly (same shape, same order).
        direct = [_lint_finding_repr(f) for f in lint_skill(skill_md)]
        assert result["full_current_lint_findings"] == direct
        # Batch mode reports the SAME findings shape as single mode.
        batch_raw = _skill_manage_batch([
            {"action": "patch", "name": "big-skill",
             "old_string": "When the reader must observe an oversized subject.",
             "new_string": "When the reader must observe an oversized subject (batch)."}])
        entry = json.loads(batch_raw)["results"][0]
        assert entry["lint_evaluation_status"] == "EVALUATED"
        assert "oversized-body" in _rules(entry["full_current_lint_findings"])