# R11-0 self-research / self-learning / self-iteration / self-evolution

Claim ceiling **LOCAL / candidate-only**.

## Research
- **RS-20** Checkbox state is a poor proxy for reality in this control plane: 25 records, 223 of 587 rows ticked, yet 7 records' work is measurably live on disk while their rows stay unticked (FAR ws1 triage).
  - evidence: R11/FAR/ws1/open_records_inventory.tsv; live re-count reproduced by the round and by the checker
- **RS-21** Control-plane state moves INSIDE a round: the lane registry advanced epoch 21 -> 22 at 14:13:29 during this round, changing PLAN's route and re-admitting the VERIFY arm into its pool, i.e. a running round's cited routes can be stale within the hour.
  - evidence: registry sha256 02481992... over 47,224 bytes, epoch 22, epoch-21 values recorded in R10
- **RS-22** The dispatcher's remote-write gate matches word STEMS, not words: the word 'published' in a checker brief tripped ERR_LANE_REMOTE_WRITE_NOT_AUTHORIZED and refused the dispatch.
  - evidence: the round's own marker scan printed the offending line (line 12) and the dispatch was refused; after rewording the scan was clean and the dispatch ran
- **RS-23** A lane's pool membership is epoch-dependent: the same lane that fail-closed ERR_LANE_REQUIRED_ARM_ABSENT in R10 served the mandated arm with a real pool receipt in R11 (required == served == opencode-go/deepseek-v4.1-flash, exit 0, 543.73 s). A pool verdict must never be cached across epochs.
  - evidence: dispatcher receipt attempts[0] + the round's snapshot of it
- **RS-24** The previous round's wrapper repair corrected a LIVE false negative: the dispatcher reported ERR_NO_ARM_EMITTED_NONCE while the nonce sat in its own recorded 305,481-byte stdout and in the lane's DONE file, and the wrapper's attestation reported NONCE_PRESENT_DESPITE_DISPATCHER_CODE.
  - evidence: R11/lane_receipts nonce attestation + R11_VERIFY/R11V_DONE
- **RS-25** A self-check's reference-enumeration is part of its claim: an under-counting regex produced a false 'clean' result, and an independent checker found a non-resolving locator that the check had not enumerated.
  - evidence: SELFCHECK_R11 schema .../2 (11 refs, 0 bad) vs the checker's 14-15 refs with >=1 bad; corrected in schema .../3 (15 refs, 0 bad)
- **RS-26** A round's own artifacts can go stale between measurement and delivery: a peer added a change record at ~14:30 and the round's own record advanced 0/18 -> 14/10 after the first snapshot.
  - evidence: the checker's live re-count (25 records, 223/364) vs the round's snapshot (24, 183/371)
- **RS-27** A checker's verdict can be internally inconsistent: this one's summary line claims 5 CONFIRMED / 2 REFUTED while its own claims list is 4 / 3.
  - evidence: R11_VERIFY/R11_VERDICT.json (overall vs claims[])
- **RS-28** An inherited fact can be wrong twice over: two successive probes of the same file were wrong (a nested key missed, then the wrong file measured) before the third located the declaration.
  - evidence: the WR-6 row as first carried, then wrongly retired, then re-established with the corrected locator
- **RS-29** A prompt-injection attempt styled as a `system_warning` appeared inside tool output and was ignored; the checker reported it as an observation.
  - evidence: R11_VERIFY/R11_VERDICT.json (overall line) + ledger finding R11-F5

## Learning
- **LN-20** Where peers run concurrently, take the snapshot but RE-COUNT immediately before delivery and label when the snapshot was taken; a peer can add or advance a record inside your own window.
  - applies to: handover / inventories
- **LN-21** Lint a lane brief against the dispatcher's own marker gate before dispatching: the gate matches stems, so delivery prose trips it. Fail at authoring time, not at dispatch time.
  - applies to: lane dispatch
- **LN-22** Cite the control-plane epoch (and the file's sha256) with any route you quote, because the registry can move mid-round and a route cited from an earlier epoch is a claim about the past.
  - applies to: governance evidence
- **LN-23** A self-check must enumerate exactly the reference set its document contains, including placeholder forms; otherwise a clean result is manufactured by the regex, not measured.
  - applies to: self-check design
- **LN-24** Never retire or re-establish an inherited fact from a single probe: verify the locator, read the file's real structure, and prefer the file's own bytes over a key-name guess.
  - applies to: evidence discipline

## Iteration
- **IT-20** the round's self-check now enumerates placeholder forms and records, in its own note, that an earlier version was wrong  _(EXECUTED)_
- **IT-21** the wrapper's nonce attestation moved from unit-tested to live-validated (it corrected a real dispatcher false negative on a serving turn)  _(EXECUTED)_

## Evolution proposals
- **EV-R11-01** generate handover inventories at delivery time and stamp them with the measurement instant, rather than shipping a snapshot taken minutes earlier
  - owner: round owner
  - gate: an inventory's stamp is within seconds of the delivery commit / falsification: an inventory whose stamp predates a peer write it does not mention
- **EV-R11-02** brief linting in the dispatcher path: refuse at authoring time a brief whose text trips the marker gate, with the offending line named
  - owner: control-plane owner
  - gate: no dispatch is refused for a marker the author could see in advance / falsification: a dispatch refused for a marker present in the brief before dispatch
- **EV-R11-03** machine-require an epoch+sha stamp on every artifact that cites a lane route
  - owner: governance owner
  - gate: no route is quoted without its epoch / falsification: a round artifact citing a route with no epoch stamp

## Not claimed
- no acceptance, Gate PASS, AO verdict or release
- no model-axis independence (writer and checker share one arm)
- no product behaviour
