# Learning — FAR-20261031-028

## L1. A hiding flag governs one edge of a process tree, not the tree
`CREATE_NO_WINDOW` hides the child it is applied to and hands it **no console**; the next console program it
starts is again consoleless and gets a fresh visible one. Hiding must give the child **one console created
hidden** (`CREATE_NEW_CONSOLE` + `STARTF_USESHOWWINDOW`, `wShowWindow = 0`) so the whole subtree inherits it.

## L2. Govern the spawn site, not the task that owns it
Two prior rounds each fixed one named scheduled task and the window came back from a different launcher.
The unit of governance is the **spawn site**; there are 31 of them, so the control must be a single choke
point plus an invariant test, never a per-task patch.

## L3. A launcher that cannot see its child is not a launcher
`Win32_Process.Create` returned `ok: true` with a pid for children that died in the same second (30 vanished
attempts on one unit). Success must mean **alive and the right image**, measured after a bounded delay.

## L4. A launch marker is not a spent round
Six 310-byte `PRE_ATTEMPT` receipts with no `attempts[]` halted all three open units. A round is spent when a
model turn was attempted; an orphan marker older than the lane budget is a dead attempt.

## L5. A loop that tops up a decided unit is a money/CPU furnace
Relaunching a halted unit every ~10 s produced 517 churn records and 48 refusals, none of which could ever
succeed. The fan-out must read the decision (halted, spent, in-flight) before it spawns.

## L6. "It did not reproduce" is a finding, not a failure to report
The synthetic positive control fired zero windows at 1.5 s sampling. Recording that as INCONCLUSIVE — instead
of claiming the mechanism was proven — is what keeps the rest of the attribution admissible. The deciding
instrument must sample at ~20 ms, because the event is shorter than a snapshot.

## L7. CPU load follows from process churn, not from model work
Measured idle-ish load 7–32 % with no lane running, driven by `pwsh`/WMI startup per launch, 229 live
processes, and a second Hermes instance outside this repo. The lever that matters is **spawns per minute**,
which is exactly what F1–F6 reduce.
