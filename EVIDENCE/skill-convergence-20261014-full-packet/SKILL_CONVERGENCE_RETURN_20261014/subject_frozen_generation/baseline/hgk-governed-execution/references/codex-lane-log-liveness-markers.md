# Judging a CODEX CLI lane's liveness from its log

## Why
A sealed CODEX lane writes to a plain redirect file that grows continuously, so unlike a Hermes
one-shot it is *not* empty while running. That invites a different wrong heuristic: gating on the
launcher's terminal marker.

A lane log DOES contain `^EXIT=` lines that are **not** the terminal marker: the launcher appends
`EXIT=$RC` as the last line at exit, but the lane's own body also prints `EXIT=...` while discussing
or running things. Measured: the marker appeared at line 1216 of 1936 and at line 6146 of a longer
log, in both cases mid-run with the lane still working.

## Rules

1. **`grep -c '^EXIT='` on a lane log is unreliable in BOTH directions.** Non-zero does not mean the
   lane closed; a single marker does not mean only one exit happened.
2. **Liveness needs at least two of these, all positive:**
   - the marker is the **last non-empty line** (not merely present), AND
   - the log **size/mtime still advances** across two samples >=15 s apart, AND
   - the lane's declared **target files are still not written/unchanged** (a lane writes bodies before
     it edits its main target), AND
   - the child process is still present.
3. **Never conclude "no artifacts" from a listing whose stderr was swallowed.** `ls ... 2>/dev/null`
   prints the same empty-looking result for "the lane has not written it yet" and "the path is wrong".
   Probe each path explicitly (`stat`) and report ABSENT separately from unchanged.
4. **Check the target file, not the log, for progress on the real deliverable.** A lane can be deep in
   context for a long time before it touches `its main target`; the log growing proves work, not closure.
5. **Repair-dispatch discipline:** never dispatch a repair/retry lane until rule 2 is satisfied. The
   cost of waiting is minutes; the cost of a premature repair dispatch is a duplicated side effect that
   can exceed a one-use authorization (recorded defect, round HGK-GCM-APPLY-20261013).
