# METHOD — FAR-20261021-026 (SBL R10, handover round)

## The order and what it changed
The owner did not ask for another build round. Two things changed: the lane mandate (PLAN and
EXECUTE swap), and the deliverable (a handover a fresh session can resume from). So the round
has two halves, and the honest order is mandate-gate first, handover second — because the
mandate order itself said to pause if the models were unavailable.

## Method
1. Read the live pool before assuming what a "rebind" means. The two target arms were already
   present at rank 2 in their lanes, so the operation was a RE-ORDER, not an insertion.
2. Probe the target arms at their CURRENT rank, by --force-rank, BEFORE changing anything.
   This is the only ordering in which the rebind cannot be the step that discovers a dead arm.
   Measured: PLAN rank2 minimax 5.43 s, EXECUTE rank2 deepseek 2.51 s, VERIFY rank1 gpt 3.60 s,
   all ok, all usage 200, all nonce echoed. The pause clause was never reached.
3. Apply the re-order by LOADING the R8 builder module and overriding two globals. Forking it
   would repeat D3 (fix the artifact, leave the generator wrong).
4. Re-probe all three at rank 1 after the swap: 3.75 / 3.57 / 3.05 s.
5. Then check the runtime declarations. The drift gate returned 0 findings while all three
   still named superseded models — D1 again. Close it, re-run, follow the gate when it turns red.
6. Write the handover with the open items enumerated FIRST and the traps before the file map,
   because the next session's failure mode is inheriting a false picture, not lacking a map.
7. Self-check 9/9, with C4 comparing the three surfaces to each other and C7 asserting no
   acceptance pass exists for this programme's subjects.

## Anti-method
- No percentage of SBL completion anywhere. The control package declares its own semantic
  denominator UNKNOWN in three places; a number would be our counting choice in its costume.
- No FABRIC target invented to make a five-plane claim look whole.
- No staging of the six files concurrent writers had modified, even though staging them would
  have made the diff look tidier.
