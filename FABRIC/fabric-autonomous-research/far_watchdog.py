"""FAR watchdog: no-progress and budget abort semantics.

Implements blueprint r2 sections 12.1 (verified progress classes) and 23
(budget semantics). The watchdog never continues indefinitely: when a
no-progress limit or a budget limit is exceeded, the run must checkpoint and
stop. This module only observes and reports; it does not schedule or stop
work itself.
"""

import collections
import time

FAR_ABORT_NO_PROGRESS = "FAR_ABORT_NO_PROGRESS"
FAR_ABORT_BUDGET = "FAR_ABORT_BUDGET"


class VerifiedProgress:
    """Whitelist of progress classes that count as real progress (12.1)."""

    PROGRESS_CLASSES = frozenset({
        "new_required_source_resolved",
        "new_source_snapshot_admitted",
        "new_claim_status_changed_with_evidence",
        "new_contradiction_resolved",
        "new_experiment_result_bound",
        "new_open_question_closed",
        "new_rejected_alternative_with_evidence",
        "new_candidate_artifact_digest",
    })

    NON_PROGRESS = (
        "file_touched_no_evidence",
        "retry_same_action",
        "llm_vote_no_source",
        "summary_regenerated",
        "provider_called_no_new_claim",
        "doc_rewritten_no_new_fact",
    )

    def is_progress(self, signature):
        """Return True only for verified progress class signatures."""
        return signature in self.PROGRESS_CLASSES


class ActionWatchdog:
    """Abort on repeated identical actions, no-progress cycles, failures."""

    def __init__(self, max_identical_action_repeat=3,
                 max_no_progress_cycles=3, max_same_failure_signature=2,
                 max_retry_per_provider=1, action_signature_window=8):
        self.max_identical_action_repeat = max_identical_action_repeat
        self.max_no_progress_cycles = max_no_progress_cycles
        self.max_same_failure_signature = max_same_failure_signature
        self.max_retry_per_provider = max_retry_per_provider
        self.action_signature_window = action_signature_window
        self._action_window = collections.deque(maxlen=action_signature_window)
        self._progress = VerifiedProgress()
        self._no_progress_cycles = 0
        self._failure_counts = {}
        self._retry_counts = {}
        self._last_failure_signature = None
        self._same_failure_streak = 0

    def record_action(self, signature):
        """Record an action; verified progress resets the cycle."""
        self._action_window.append(signature)
        if self._progress.is_progress(signature):
            self._no_progress_cycles = 0
        else:
            self._no_progress_cycles += 1

    def record_failure(self, signature):
        """Record a failure; provider prefix is derived from the signature."""
        self._failure_counts[signature] = self._failure_counts.get(
            signature, 0) + 1
        if signature == self._last_failure_signature:
            self._same_failure_streak += 1
        else:
            self._same_failure_streak = 1
            self._last_failure_signature = signature
        provider = self._provider_of(signature)
        self._retry_counts[provider] = self._retry_counts.get(provider, 0) + 1

    @staticmethod
    def _provider_of(signature):
        """Derive the provider name from a 'provider:detail' signature."""
        if ":" in signature:
            return signature.split(":", 1)[0]
        return "unknown"

    def identical_action_exceeded(self):
        """True when a signature repeats at or past its limit in the window."""
        for signature in self._action_window:
            if self._action_window.count(signature) >= (
                    self.max_identical_action_repeat):
                return True
        return False

    def no_progress_exceeded(self):
        """True when non-progress cycles reach the configured limit."""
        return self._no_progress_cycles >= self.max_no_progress_cycles

    def same_failure_exceeded(self):
        """True when a failure signature repeats at or past its limit."""
        return self._same_failure_streak >= self.max_same_failure_signature

    def retry_exceeded(self):
        """True when any provider is retried beyond its retry budget."""
        return any(
            count > self.max_retry_per_provider
            for count in self._retry_counts.values())

    def check(self):
        """Return the current watchdog status dict."""
        identical = self.identical_action_exceeded()
        no_progress = self.no_progress_exceeded()
        same_failure = self.same_failure_exceeded()
        reason = None
        if identical:
            reason = "IDENTICAL_ACTION_REPEAT_EXCEEDED"
        elif no_progress:
            reason = "NO_PROGRESS_CYCLES_EXCEEDED"
        elif same_failure:
            reason = "SAME_FAILURE_SIGNATURE_EXCEEDED"
        return {
            "identical_action_exceeded": identical,
            "no_progress_exceeded": no_progress,
            "same_failure_exceeded": same_failure,
            "reason": reason,
        }

    def verdict(self):
        """Return FAR_ABORT_NO_PROGRESS when any limit is exceeded."""
        status = self.check()
        if any((status["identical_action_exceeded"],
                status["no_progress_exceeded"],
                status["same_failure_exceeded"])):
            return FAR_ABORT_NO_PROGRESS
        return None


class BudgetGuard:
    """Abort when wall clock, tokens, cost, retries, or subagents run out."""

    def __init__(self, wall_clock_seconds, token_budget=None,
                 cost_budget=None, retry_budget=2, subagent_budget=None):
        self.wall_clock_seconds = wall_clock_seconds
        self.token_budget = token_budget
        self.cost_budget = cost_budget
        self.retry_budget = retry_budget
        self.subagent_budget = subagent_budget
        self.tokens_used = 0
        self.cost_used = 0
        self.retries = 0
        self.subagents = 0
        self._started_at = time.monotonic()

    def consume_tokens(self, n):
        """Consume tokens; reaching the token budget triggers terminal."""
        self.tokens_used += n

    def record_cost(self, c):
        """Record cost; reaching the cost budget triggers terminal."""
        self.cost_used += c

    def record_retry(self):
        """Record a retry; reaching the retry budget triggers terminal."""
        self.retries += 1

    def spawn_subagent(self):
        """Record a subagent; reaching its budget triggers terminal."""
        self.subagents += 1

    def _wall_clock_exceeded(self):
        return time.monotonic() - self._started_at >= self.wall_clock_seconds

    def _token_exceeded(self):
        if self.token_budget is None:
            return False
        return self.tokens_used >= self.token_budget

    def _cost_exceeded(self):
        if self.cost_budget is None:
            return False
        return self.cost_used >= self.cost_budget

    def _retry_exceeded(self):
        if self.retry_budget is None:
            return False
        return self.retries >= self.retry_budget

    def _subagent_exceeded(self):
        if self.subagent_budget is None:
            return False
        return self.subagents >= self.subagent_budget

    def check(self):
        """Return the current budget status dict."""
        return {
            "wall_clock_exceeded": self._wall_clock_exceeded(),
            "token_exceeded": self._token_exceeded(),
            "cost_exceeded": self._cost_exceeded(),
            "retry_exceeded": self._retry_exceeded(),
            "subagent_exceeded": self._subagent_exceeded(),
        }

    def terminal(self):
        """Return FAR_ABORT_BUDGET when any budget limit is exceeded.

        Hard rule: budget exhausted means checkpoint and stop; never continue
        indefinitely once a limit is reached.
        """
        if any(self.check().values()):
            return FAR_ABORT_BUDGET
        return None
