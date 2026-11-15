# PLAN lane brief — FAR research R1 plan + the blocked-item re-read

Read-only. You may read files and reason. Do not write, do not push, do not call a provider.

## Why this run exists

A governed delivery (FHS W0) has just finished a repair round. Thirteen external findings were dispositioned;
what remains is a short list of **holds**. The owner's question is second-order and blunt:

> are those holds real blocks, or am I over-reading the blueprint, mis-reading a record, missing an
> implementation that already exists, or refusing a legitimate alternative (an independent lane, a local
> container sandbox, an owner-passphrase envelope)?

Answering that by repairing more files is not research. Read the records instead.

## Sources you must actually read (paths are absolute; open them, quote them)

1. The round that produced the holds: `C:/Projects/Agent_Workspace/FHS_W0_R26_POSTREPAIR_20261110/out/FHS_W0_R27_POSTREPAIR_RESULT.md`
   (sections 1, 2, 5.1, 7, 11) and `.../evidence/ACCEPTANCE_RERUN/ACCEPTANCE_RERUN.json`.
2. The external challenge that set the bar: `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/FHS／FHS-MSC／SBL/FHS/FHS_PIPD-LS-PKG/實作/W0/FHS_W0_r26_External_Challenge_PostRepair_Acceptance_Report_2026-11-09.md`
3. **The history of every previous W0 round** (the owner explicitly requires this):
   `C:/Projects/Agent_Workspace/FHS/FHS_W0_R13_ACCEPTANCE_20261108/` — at least
   `HANDOVER_R19.md` … `HANDOVER_R26_2026-11-08.md`, `out/SELF_ERRORS.md`, `out/OWNER_RULING_W0_R12.json`
   (if present), `lanes/VERIFY_R26_VERDICT.json`, `lanes/PACK_R25_VOTE.md`, and the `out/GATE_R*.json` set.
   Look for: how a previous round unblocked the *same* obstacle, and which instrument it used.
4. The upstream intent, so you can test whether a hold is stricter than the design:
   `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/FHS／FHS-MSC／SBL/FHS/FHS_PIPD-LS-PKG/藍圖/FHS_總藍圖_r4.md`
   and `FHS_PIPD-LS-PKG_藍圖_r4.md` — only the passages about Native E2E closure, unattended operation,
   single-owner-single-machine, and who may sign what.
5. The capabilities that already exist and are often forgotten:
   - owner signing window + key vault: `C:/Projects/Agent_Workspace/FHS/HG-KSEOS/ops/session-20261031/tools/{owner_window.py,owner_vault.py,owner_prompt.py}`
   - issuer grants: `C:/Projects/Agent_Workspace/FHS/HG-KSEOS/scripts/issue_grant.py`
   - owner delegation envelope: `C:/Projects/Agent_Workspace/FHS/HG-KSEOS/ops/session-20261031/r18-durable/tools/owner_delegation.py`
   - lane dispatcher + wrapper: `C:/Projects/Agent_Workspace/FHS/HG-KSEOS/scripts/{hgk-lane-dispatch.py,hgk-lane-run.sh}`
   - the guard just installed: `C:/Projects/Agent_Workspace/FHS_R26_WT/hgk-hook/scripts/fhs_entry_guard.py`
   - FAR itself: `C:/Projects/Agent_Workspace/FHS_R26_WT/fabric-far/FABRIC/fabric-autonomous-research/`

## The items to judge (each gets the same four tests)

B1 HGK epoch-41 not in `main`; PR #16 is draft and CI-red by construction.
B2 No mechanical cross-session entry for hosts other than this repo's dispatcher.
B3 `NATIVE_SIGNED` / `PASS_CHALLENGE` / `RELEASE` never granted.
B4 Full 22-gate profile cannot run (`--profile full` exits 2; the 31-volume corpus is not on this host).
B5 Five menu slots are refused pre-spawn `ERR_ARM_NOT_IN_ASSIGNMENT` (assignment declares no fallbacks).
B6 122 pre-existing dispatcher tests fail closed since the guard landed.
B7 `R26-01` session/process identity is enforced only under `--strict`; 4/4 real votes carry none.
B8 126 legacy dict-style votes carry no candidate binding.
B9 The independent checker's long turn could not execute Python (`spawn … ENOENT`) and hit git "dubious ownership".

For **each** item, answer in this order and do not skip a step:

1. **Is the block real?** Quote the record that says so. If the record is a summary rather than a measurement, say so.
2. **Over-read?** Does the upstream blueprint actually require this to be true *now*, or did a prior round import a stricter
   bar (a report, an external reviewer, an owner aside) and then treat it as the design? Quote the blueprint line.
3. **Already implemented?** Name the command/file/row a reader could run to see it work. If you find one, say exactly where.
4. **Alternative instrument?** Test each of: an independent lane with its own evidence path; a local container/isolated
   sandbox; an owner-passphrase envelope session that pre-authorises the effect; an issuer grant bound to a writeset.
   For each: does it satisfy the *letter* of the requirement, or only its convenience? Say which.
5. **Design flaw?** If none of the above, is the requirement itself wrong for a single-owner single-machine unattended
   system? If you claim so, name the exact clause that should change and who may change it.

## Also produce (R1 plan shape)

`ResearchPlan`: subquestions, claim classes, source classes, query strategy, candidate methods/providers,
challenge trigger, experiment trigger, stop criteria, abstain criteria, budget allocation.

## Output

A single reply in three parts: **(A)** the R1 plan, **(B)** the B1–B9 table with the five-step answer per row
(columns: item | verdict ∈ {REAL_BLOCK, OVER_READ, MISREAD, ALREADY_BUILT, SOLVABLE_BY_ALTERNATIVE, DESIGN_FLAW} |
the record you quoted | the command or file that proves it | what it would take to close it), and
**(C)** the three items where you are least confident, with the observation that would settle them.

Quote identifiers verbatim. Where you could not open a file, write `UNREADABLE <path>` — never guess its contents.
