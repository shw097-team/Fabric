# FHS Engineering Entry (Fabric-hosted candidate)

**NAVIGATION_ONLY · NOT OWNER RATIFIED · NOT AN ISSUER · NOT A COMPILER · NOT A CHECKER.**

This directory is a single non-authoritative engineering index. It has no repository or native write permissions. The existing Fabric `INTEGRATION/MANIFEST.json` governs the mirror and must not be silently expanded.

| Task class | Public source pointer | Original reader and next action | Affected repositories |
|---|---|---|---|
| `sbl_product` | [SBL TPM Skill](https://github.com/shw097-team/SBL/blob/main/sbl_sp/plugins/tpm_sp/SKILL.md) | SBL Product Reader; verify PIPD Compiler binding before handoff | PIPD |
| `fabric_policy` | [Fabric source projection](https://github.com/shw097-team/Fabric/blob/main/INTEGRATION/SOURCE-PROJECTION.md) | This is a **mirror**, not the authoritative Policy Reader. Ask original Fabric Policy Owner and HGK consumer | HGK |
| `hgk_admission` | [HGK source export](https://github.com/shw097-team/HG-KSEOS/blob/main/README.md) | Original HGK Native Issuer / permit / consumer readback is REQUIRED; GitHub is insufficient | Fabric, SBL |
| `pipd_canonical` | [PIPD Compiler pipeline](https://github.com/shw097-team/PIPD-LS-SP/blob/main/src/pipd_ls_sp/pipeline.py) | Original PIPD Compiler / CLI / U04 source and compatibility reader | SBL |
| `cross_repo` | Each affected original repository | Make separately scoped PR candidates. Shared ChangeSet ID is not HGK WorkID | SBL, Fabric, HGK, PIPD |
| `hermes_runtime` | **MISSING: original host source link must be resolved** | Fresh profile / PID / loaded / invoked / ActualServed from original Host Reader, not GitHub | HGK, Fabric |

To statically validate from the Fabric repository root:

```bash
python3 INTEGRATION/FHS/validate_entry.py
python3 INTEGRATION/FHS/validate_entry.py --route pipd_canonical
python3 -m unittest discover -s INTEGRATION/FHS/tests -v
```

`STATIC_VALID_ONLY` does **not** mean GitHub merge, native acceptance, actual host load, release, or cross-repository write authority. Online HEAD comparison requires an external, operator-provided fresh expected-head snapshot and is still only GitHub-source observation.

If the index is missing or stale, read each repository's original README/AGENTS or approved Source Reader. HOLD only the affected write; permitted source reads and local drafts may continue. PIPD-LS-SP remains active until a separately ratified U04 cutover.
