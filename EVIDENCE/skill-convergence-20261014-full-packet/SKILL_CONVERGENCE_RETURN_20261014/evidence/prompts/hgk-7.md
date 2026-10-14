# Bounded EXECUTE lane — HGK reference-sprawl remediation, pilot batch

Your writable directory is this lane's cwd. The subject is `skill/` inside it. Work only inside the cwd.

Context you can rely on, measured by the round harness before this lane started:
- `skill/references/` holds 108 markdown files. The live linter warns at more than 60 under `references/` (`references-sprawl`).
- 37 of those files are unreachable: their path appears in no other file of the skill, main document included.
- The pilot batch is the fourteen smallest of those unreachable files, 42,985 bytes in total.

INPUT: read the JSON list at
`C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014/evidence/postfreeze/hgk_unreachable.json`
It is an array of `[relative_path, byte_size]` pairs, ascending by size, paths relative to `candidates/hgk`.
Use exactly the first 14 entries. Do not add or drop entries.

TASK, in this order:
1. For each of the fourteen files, record its byte size and sha256 BEFORE any change.
2. Create ONE new topic file: `skill/references/topics/lane-bootstrap-and-guard-notes.md`.
   Its structure: for each source file, in the order the list gives, a heading line `## <original relative path>`
   followed by that file's content bytes VERBATIM (no rewording, no reflow, no trimming of the body).
3. Delete the fourteen originals.
4. Do NOT create stubs for them. This is deliberate and is the point of the pilot: nothing references them, so no
   name needs to survive as a file; the original names survive as headings inside the topic file and stay greppable.
5. Verify, from the bytes on disk after the change, that each original's content still appears byte-for-byte inside
   the topic file, and record the sha256 that was computed before the deletion next to a check that it is present.
6. Do NOT touch `skill/SKILL.md` or any file other than the fourteen and the new topic file.

OUTPUT: write `remediation_result.json` in the cwd with:
  schema, lane, observed_at, merged[ {path, bytes_before, sha256_before, present_verbatim_in_topic: true} ],
  topic_file {path, bytes, sha256}, counts {references_md_before, references_md_after},
  deleted[], stubs_created (must be []), sha256_of_skill_md_before and _after (must be equal),
  exact_commands[], coverage, and claim_ceiling.
The claim ceiling must say this is a candidate-only edit whose byte-level checks were recomputed in this lane, that
it is not acceptance, and that it does not reach the 60-file warning cap.

Facts you must not overstate: the merge reduces the file count by 13 net (14 removed, 1 added). The cap is still
not met. Say so.

Interpreter for any script you write: `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`.
Write scripts to files under the cwd and run them by path; do not build long inline PowerShell commands.

Final literal transport token (not an acceptance): SKCV_HGK_7_OK
