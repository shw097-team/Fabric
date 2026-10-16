# Self-evolution — ROUND3-LANE-REBIND-AND-CLOSURE-20261016

Under FABRIC & HGK governance this section is not rhetoric: it names what changed in the *apparatus* as a
result of this round, what remains unvalidated, and what the next round must not have to rediscover.

## What the apparatus learned (and where it was written down)

1. **A lane rebind is a five-surface change, not a registry edit.** The declaring surfaces that must move
   together are: the registry route row (provider/model/identity/auth/oauth), the arm and fallback arrays
   with their `automatic_selection` flags, the assignment site's `lane_chains`, the **dispatch-time pool**
   that `scripts/hgk-lane-dispatch.py` actually reads (`config/lane-route-slots.candidate.json`), and the
   conformance fixture whose invariant *is* the current owner order. Plus the coupling: `epoch`, `revision`,
   the `source_of_routes` digest pin, and every `projections[].bindings[].expected` that names a moved value.
2. **The WorkOrder's persisted `role_binding` is a third authority.** The dispatcher derives the required
   arm and rank from the WorkOrder's `permissions_json[role_binding]` before spawn and refuses a contradicting
   `--require-arm`/`--force-rank`; an omitted one is derived, never defaulted. Admission is therefore
   load-bearing, not paperwork.
3. **Two enforcement surfaces can silently disagree.** The registry's declarative SoD model permits an
   owner-ordered demotion with a recorded declaration — the conformance test enforces exactly that — while
   the pre-dispatch guard hard-refused any same-model pair. The owner's own order was undispatchable until
   the two agreed. **Lesson: when a policy is expressed in two places, measure both against the mandated
   configuration, not just the one you edited.**
4. **Back up before you write.** A commit helper that records the backup after the write leaves no preimage;
   on a tree whose `config/` is not tracked, git cannot substitute for it. Recovery was possible only because
   the previous round had frozen a copy elsewhere, and it was proven by digest, not assumed.
5. **A long YAML note is a scalar, and a plain scalar may not contain ": ".** An unquoted prose note made the
   entire registry unparseable — the failure surfaced as a `ScannerError`, not as a wrong value.
6. **A coverage binding is not litter.** When a structured rewrite dropped a field the registry binds, the
   honest repair was to restore the field, not to delete the binding: deleting it would have traded coverage
   for a green light.
7. **Long-path failures masquerade as access failures.** A bounded `os.walk(..., onerror=...)` is the correct
   enumerator on this host; a recursive glob dies on `WinError 3`.

## What remains unvalidated

* The `sod_declaration_exemption` path is validated by the round's own oracle and by an independent checker
  that **shares the writer's model**. Neither is an external review.
* The guard's full `exit 0` ADMIT path is unreachable in production until something produces an admission
  receipt (gap **R11**).
* Whether the exemption's trust boundary (an owner-ordered declaration in the registry) is the right place
  for this decision is a policy question for the OWNER. This round records the risk; it does not settle it.
* No whole-tree regression run was attempted in this round: the previous round measured that absolute counts
  are host-limited and that only paired differences reproduce.

## Next round must not rediscover

* That the pool is read while its own `status` says CANDIDATE (NF-05) — recorded in the file's own
  `selection_note`.
* That the enumeration obstruction is long-path, not permissions (NF-01) — corrected here.
* That a receipt rewritten by a re-runnable tool cannot be frozen (the `SELF_REF` set carries forward).
* That a rebind must move the conformance fixture in the same change, or its own suite fails.
