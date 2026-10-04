import hashlib


class LeaseDenied(Exception):
    pass


class UnknownState(Exception):
    pass


class DesktopLeaseManager:
    def __init__(self):
        self._writers = {}
        self._checkpoints = {}

    def acquire(self, session_id: str, writer_profile: str, after_checkpoint=None) -> str:
        if session_id in self._writers:
            raise LeaseDenied('second writer denied for session ' + session_id)
        if after_checkpoint is not None:
            if session_id not in self._checkpoints:
                raise ValueError('no checkpoint')
            if self._checkpoints[session_id]['ref'] != after_checkpoint:
                raise ValueError('stale checkpoint')
        self._writers[session_id] = writer_profile
        return writer_profile

    def current_writer(self, session_id: str):
        return self._writers.get(session_id)

    def release(self, session_id: str, writer_profile: str) -> None:
        if self._writers.get(session_id) == writer_profile:
            del self._writers[session_id]

    def checkpoint(self, session_id: str, ref: str, desktop_state_digest=None) -> None:
        self._checkpoints[session_id] = {'ref': ref, 'desktop_state_digest': desktop_state_digest}

    def transfer(self, session_id: str, from_writer: str, to_writer: str) -> str:
        if self._writers.get(session_id) != from_writer:
            raise LeaseDenied('not holder')
        if session_id not in self._checkpoints:
            raise ValueError('transfer requires checkpoint first')
        del self._writers[session_id]
        self._writers[session_id] = to_writer
        return to_writer

    def replay_allowed(self, side_effect_class: str, prior_effect_receipt_ref, current_state_confirms_applied) -> bool:
        if current_state_confirms_applied is None:
            raise UnknownState('desktop state unknown')
        if prior_effect_receipt_ref is not None and current_state_confirms_applied:
            return False
        if side_effect_class == 'NONE':
            return True
        if side_effect_class == 'EXTERNAL_APPROVAL_GATED':
            return False
        return True


def idempotency_key(workorder_id: str, task_id: str, application_id: str,
                    application_version: str, action_class: str, target_identity: str) -> str:
    payload = '|'.join([workorder_id, task_id, application_id, application_version,
                        action_class, target_identity])
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()