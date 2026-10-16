#!/usr/bin/env python3
"""Single-use authorization claim on the EXISTING Spine (round HGK-GCM-REPAIR-20261013, Phase C2).

Why this exists (the recorded overrun)
--------------------------------------
In round HGK-GCM-APPLY-20261013 **one** authorized live-measurement window was consumed **twice**
(2 vs 1): a repair lane was dispatched before the prior attempt was confirmed ended. The window was
an *authorization budget*, and nothing structurally stopped a second claimant. Discipline was the
only control, and discipline failed.

This module turns that budget into a **single-use claim on the existing Spine `leases` table**,
acquired through the already-present typed API ``SharedSpine.acquire_lease`` / ``release_lease``
(``src/hg_kseos/spine.py``). It adds NO new database, NO new table, NO scheduler: the `leases`
table's ``resource_id`` PRIMARY KEY plus ``acquire_lease``'s conflict detection is the whole
mechanism. A second concurrent claim of the same resource raises ``LeaseConflict``.

Consumption policy (single-use, on the EXISTING leases table) — round HGK-GCM-REPAIR2-20261013
------------------------------------------------------------------------------------------------
ROUND-1 DEFECT (D4): the wrapper only gave *mutual exclusion* while held, not *single use*. Both
sequential distinct holders won (A released, then B acquired), and the SAME holder won twice
(``acquire_lease`` treats a re-acquire by the same ``holder`` + a live lease as a no-op "renew").
The dispatcher imported this module but never acquired or checked it, so "structurally impossible"
overrun was FALSE. This revision fixes that with a durable CONSUMED tombstone on the SAME leases
table (no new database, no new table, no scheduler):

* ``acquire()`` refuses with :class:`ClaimAlreadyConsumed` when the resource already carries a live
  CONSUMED tombstone — BEFORE taking the window lease. So a second acquisition by ANY holder (the
  same holder string or a different one) fails, sequentially or concurrently.
* ``consume()`` is called by the dispatcher AFTER a successful spawn. It writes a tombstone lease on
  ``<resource>:consumed`` (holder ``__consumed__``, a very long TTL) that :meth:`release` never
  removes. This is the durable single-use state that round 1 lacked.
* Window TTL (default 900 s) is STILL the anti-deadlock bound for an in-flight window that never
  reached a successful spawn: a crashed/failed holder's window lease expires and is reclaimable, so a
  burned-but-unused window does not deadlock the round. Consumption, once written, is the single-use
  bound and does NOT expire within the round (100-year TTL; see :data:`CONSUMED_TTL_SECONDS`).

Honest boundary (stated, not hidden)
------------------------------------
* Single-use holds **once the window is consumed**. A window that is acquired but never consumed
  (the holder crashed, or the spawn failed) is released and reclaimable after the window TTL. That is
  deliberate: an authorization that was never exercised should not be permanently burned.
* The CONSUMED tombstone uses a 100-year TTL on the existing leases row. It is durable in practice,
  not literally immortal: an operator ``--reset`` (which releases the tombstone) or the passage of
  100 years reclaims it. That reset is the documented rollback path.
* This still proves nothing about the WORK behind the claim; it only proves the budget was taken
  once and consumed once.
"""
from __future__ import annotations

import json
from pathlib import Path

DEFAULT_TTL_SECONDS = 900

# The durable CONSUMED tombstone: a lease on ``<resource>:consumed`` that ``release`` never removes.
# 100 years is "does not expire within any realistic round"; it is still a TTL on an existing row, so
# the honest statement is "durable in practice, reclaimable by an explicit --reset (or in 100 years)".
CONSUMED_TTL_SECONDS = 60 * 60 * 24 * 365 * 100
CONSUMED_SUFFIX = ":consumed"
CONSUMED_HOLDER = "__consumed__"


class ClaimAlreadyConsumed(Exception):
    """The resource was already CONSUMED by an earlier successful spawn. A second use is refused."""


def _load_spine(hgk_root):
    """Import SharedSpine from the repo tree without requiring it to be installed."""
    import sys

    root = Path(hgk_root)
    src = str(root / "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    from hg_kseos.spine import SharedSpine  # noqa: E402

    return SharedSpine


def default_db_path(hgk_root) -> Path:
    return Path(hgk_root) / "var" / "shared-spine" / "hg-kseos.db"


def resource_for_round(round_name: str, budget: str = "gcm-live-measurement") -> str:
    """The conventional resource id, e.g. ``gcm-live-measurement-HGK-GCM-REPAIR-20261013``."""
    return f"{budget}-{round_name}"


def consumed_resource(resource_id: str) -> str:
    """The tombstone resource id for a claimed resource, e.g. ``<resource>:consumed``."""
    return f"{resource_id}{CONSUMED_SUFFIX}"


def _consumed_token_for(resource_id: str) -> str:
    """A stable token for the tombstone lease (the tombstone is not a secret; it is a durable mark)."""
    return f"consumed:::{resource_id}"


class AuthorizationClaim:
    """A single-use claim over one Spine resource. Use as a context manager."""

    def __init__(self, spine, resource_id: str, holder: str, token: str,
                 ttl_seconds: int = DEFAULT_TTL_SECONDS):
        self.spine = spine
        self.resource_id = resource_id
        self.consumed_resource = consumed_resource(resource_id)
        self.holder = holder
        self.token = token
        self.ttl_seconds = int(ttl_seconds)
        self.acquired = False
        self.released = False
        self.consumed = False

    def acquire(self) -> "AuthorizationClaim":
        # CONSUMED check FIRST: a resource that already carries a live tombstone is spent. Refuse
        # BEFORE taking the window lease. The tombstone lives on the SAME leases table; this is what
        # makes the claim single-use (durable consumption) rather than mere mutual exclusion (D4).
        if is_consumed(self.spine, self.resource_id):
            raise ClaimAlreadyConsumed(
                f"ERR_AUTHORIZATION_ALREADY_CONSUMED:{self.resource_id}:{CONSUMED_HOLDER}")
        # Raises LeaseConflict (ERR_DUAL_WRITER) if another live holder owns this resource.
        self.spine.acquire_lease(self.resource_id, self.holder, self.token,
                                 ttl_seconds=self.ttl_seconds)
        self.acquired = True
        return self

    def consume(self) -> bool:
        """Mark the resource permanently used. Called by the dispatcher AFTER a successful spawn.

        The mark is a lease row on ``<resource>:consumed`` with a 100-year TTL, held by
        ``__consumed__``. It is written through the SAME existing Spine surface (``acquire_lease``)
        and is NEVER removed by :meth:`release`, so a later acquisition by any holder fails at
        :meth:`acquire`. Idempotent: re-consuming the same resource is a no-op returning True.
        """
        if self.consumed:
            return True
        self.consumed = consume(self.spine, self.resource_id, _consumed_token_for(self.resource_id))
        return self.consumed

    def release(self) -> bool:
        """Release the WINDOW lease (never the tombstone). Idempotent; a non-holder/absent release is
        a no-op, never a crash. The CONSUMED tombstone, once written, is left in place on purpose."""
        if self.released:
            return False
        self.released = True
        if not self.acquired:
            return False
        try:
            self.spine.release_lease(self.resource_id, self.holder, self.token)
            return True
        except Exception:
            # Already gone (expired + reclaimed, or released by another path). The TTL is the
            # structural bound; a failed release must NOT mask the work result.
            return False

    def __enter__(self) -> "AuthorizationClaim":
        return self.acquire()

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.release()
        return False  # never swallow the body's exception


def claim(spine, resource_id: str, holder: str, token: str,
          ttl_seconds: int = DEFAULT_TTL_SECONDS) -> AuthorizationClaim:
    """Acquire a single-use claim. Raises ``LeaseConflict`` if a live holder already owns the window,
    and :class:`ClaimAlreadyConsumed` if the resource was already consumed by a prior successful
    spawn (the durable tombstone)."""
    return AuthorizationClaim(spine, resource_id, holder, token, ttl_seconds).acquire()


def consume(spine, resource_id: str, consumed_token: str) -> bool:
    """Write the durable CONSUMED tombstone for ``resource_id`` (called after a successful spawn)."""
    try:
        spine.acquire_lease(consumed_resource(resource_id), CONSUMED_HOLDER, consumed_token,
                            ttl_seconds=CONSUMED_TTL_SECONDS)
        return True
    except Exception:
        return False


def is_consumed(spine, resource_id: str) -> bool:
    """Read-only: is this resource already consumed (a live tombstone present)?"""
    return bool(lease_status(spine, consumed_resource(resource_id)).get("held"))


def release(spine, resource_id: str, holder: str, token: str) -> bool:
    try:
        spine.release_lease(resource_id, holder, token)
        return True
    except Exception:
        return False


def reset(spine, resource_id: str) -> bool:
    """FUNCTIONAL ROLLBACK: drop the CONSUMED tombstone so the resource can be claimed again.

    This is the documented rollback path for the single-use state. It is intentionally an explicit,
    named operation (never an automatic side effect), so a consumed window is freed only by a
    deliberate operator action.
    """
    try:
        with spine.transaction() as connection:
            connection.execute("DELETE FROM leases WHERE resource_id=?", (consumed_resource(resource_id),))
        return True
    except Exception:
        return False


def lease_status(spine, resource_id: str) -> dict:
    """Read-only: who holds the resource, and until when (or None)."""
    with spine.connect() as connection:
        row = connection.execute(
            "SELECT holder,expires_at,created_at FROM leases WHERE resource_id=?",
            (resource_id,)).fetchone()
    if not row:
        return {"resource_id": resource_id, "held": False}
    return {"resource_id": resource_id, "held": True, "holder": row["holder"],
            "expires_at": row["expires_at"], "created_at": row["created_at"]}


def _open_spine(args):
    SharedSpine = _load_spine(args.hgk_root)
    db = Path(args.db) if args.db else default_db_path(args.hgk_root)
    return SharedSpine(db, Path(args.hgk_root) / "src" / "hg_kseos" / "schema.sql")


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(prog="authorization_claim.py")
    ap.add_argument("--hgk-root", default=str(Path(__file__).resolve().parents[2]))
    ap.add_argument("--db", default=None, help="override the Spine DB path (default: var/shared-spine/hg-kseos.db)")
    ap.add_argument("--round", default=None, help="round name; resource becomes gcm-live-measurement-<round>")
    ap.add_argument("--resource", default=None, help="explicit resource id (overrides --round)")
    ap.add_argument("--holder", required=True)
    ap.add_argument("--token", required=True)
    ap.add_argument("--ttl", type=int, default=DEFAULT_TTL_SECONDS)
    ap.add_argument("--hold-seconds", type=float, default=0.0,
                    help="keep the claim for this long, then release (0 = acquire, report, release)")
    ap.add_argument("--status", action="store_true", help="read-only: report who holds the resource")
    ap.add_argument("--release", action="store_true", help="release an existing claim")
    ap.add_argument("--consume", action="store_true",
                    help="write the durable CONSUMED tombstone for the resource (single-use mark)")
    ap.add_argument("--reset", action="store_true",
                    help="ROLLBACK: drop the CONSUMED tombstone so the resource can be claimed again")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    resource = args.resource or resource_for_round(args.round or "UNNAMED-ROUND")
    spine = _open_spine(args)

    if args.status:
        out = {"action": "status", **lease_status(spine, resource),
               "consumed": is_consumed(spine, resource),
               "consumed_lease": lease_status(spine, consumed_resource(resource))}
    elif args.release:
        out = {"action": "release", "released": release(spine, resource, args.holder, args.token),
               "resource_id": resource}
    elif args.consume:
        out = {"action": "consume", "resource_id": resource,
               "consumed": consume(spine, resource, _consumed_token_for(resource))}
    elif args.reset:
        out = {"action": "reset", "resource_id": resource, "reset": reset(spine, resource),
               "consumed": is_consumed(spine, resource)}
    else:
        import time

        try:
            c = claim(spine, resource, args.holder, args.token, ttl_seconds=args.ttl)
        except ClaimAlreadyConsumed as exc:
            out = {"action": "claim", "resource_id": resource, "ok": False,
                   "code": "ERR_AUTHORIZATION_ALREADY_CONSUMED",
                   "detail": f"{type(exc).__name__}: {exc}"}
            if args.json:
                print(json.dumps(out, indent=2))
            else:
                print(out["code"], out["detail"])
            return 3
        except Exception as exc:  # LeaseConflict or a real error: fail closed, non-zero
            out = {"action": "claim", "resource_id": resource, "ok": False,
                   "code": "ERR_AUTHORIZATION_CLAIM_REFUSED",
                   "detail": f"{type(exc).__name__}: {exc}"}
            if args.json:
                print(json.dumps(out, indent=2))
            else:
                print(out["code"], out["detail"])
            return 3
        out = {"action": "claim", "resource_id": resource, "ok": True, "holder": args.holder,
               "ttl_seconds": args.ttl, "acquired_utc": True}
        try:
            if args.hold_seconds and args.hold_seconds > 0:
                time.sleep(args.hold_seconds)
        finally:
            out["released"] = c.release()
    if args.json:
        print(json.dumps(out, indent=2, default=str))
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
