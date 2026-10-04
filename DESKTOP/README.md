# Desktop-Effect Plane (governed)

Artifacts of the governed desktop-effect plane: the desktop adapter, its routing/preflight
guards, capability matrix and asset registry, the verified action-class receipts, and the
supporting documentation set.

## Governance position

This plane is the **effect layer** of the system. Its binding:

- **HG-KSEOS** is the sole control plane; this plane executes only under an admitted WorkOrder.
- Execution is gated by a **fail-closed mechanical authorization hook**: an operation runs only
  when the session holds a live authorization token, or a registered ACTIVE route id is supplied.
- **Zero-mouse hard route**: foreground/pixel/cursor input is forbidden; only message-level
  invocation is allowed (posted button messages, text-set messages, accessibility patterns).

## What an acceptance officer can verify here

1. The **authorization gate is real**: the pre-tool-call guard denies an operation whose session
   token is absent/expired, and the preflight refuses without `--route-id`/token.
2. The **zero-mouse rule is enforced by a script scanner**, not by convention: the guard rejects
   cursor/foreground/input-injection APIs before a script may run.
3. The **capability matrix** records, per action class, the qualified backend and the
   build-drift firewall state.

## Curation note

Third-party vendored material (a downloaded distribution archive and its extraction) is
**excluded** from this mirror: it is not a governance artifact. Excluded here: ~133 MB of
vendored blobs.
