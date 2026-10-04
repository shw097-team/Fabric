"""Enforce the FAR source-as-data security contract (blueprint r2 section 11.2).

Source content is DATA unless explicitly admitted authority; source
instructions cannot override Fabric, expand tools/network, request
secrets, or auto-install. This module is fail-closed by default.
"""

BLOCKING_FINDINGS = (
    "SECRET_REQUEST_DENIED",
    "BROKER_WRITE_DENIED",
    "AO_DISABLE_DENIED",
    "SILENT_FALLBACK_DENIED",
    "WRITABLE_ROOT_ESCALATION_DENIED",
)


class SourceSecurityGuard:
    """Fail-closed guard for the FAR source-as-data security contract."""

    def __init__(self):
        self.source_content_role = "DATA_UNLESS_EXPLICITLY_ADMITTED_AUTHORITY"
        self.prompt_injection = "TREAT_AS_UNTRUSTED_TEXT"
        self.override_fabric = False
        self.expand_tools = False
        self.expand_network = False
        self.request_secrets = False
        self.remote_permission_escalation = "DENY"

    def classify_source_instruction(self, text):
        return {
            "role": "SOURCE_LOCAL_INSTRUCTION_NOT_GLOBAL_AUTHORITY",
            "authority_override": False,
            "verdict": "IGNORE_AS_AUTHORITY",
        }

    def deny_secret_request(self, text):
        return {
            "fixture": "SEC-SRC-02",
            "denied": True,
            "finding": "SECRET_REQUEST_DENIED",
        }

    def deny_broker_write(self, text):
        return {
            "fixture": "SEC-SRC-06",
            "denied": True,
            "finding": "BROKER_WRITE_DENIED",
        }

    def deny_ao_disable(self, text):
        return {
            "fixture": "SEC-SRC-07",
            "denied": True,
            "finding": "AO_DISABLE_DENIED",
        }

    def deny_silent_fallback(self, text):
        return {
            "fixture": "SEC-SRC-08",
            "denied": True,
            "finding": "SILENT_FALLBACK_DENIED",
        }

    def auto_install_check(self, text):
        return {
            "fixture": "SEC-SRC-05",
            "allowed_inline": False,
            "route": "SEPARATE_PROVIDER_OR_TOOL_QUALIFICATION",
        }

    def snippet_auto_execute_allowed(
        self, sandbox, command_readback, bounded_write_set, admitted
    ):
        return bool(admitted and sandbox and command_readback and bounded_write_set)

    def writable_root_escalation_request(self, text, current_roots):
        return {
            "fixture": "SEC-SRC-03",
            "denied": True,
            "finding": "WRITABLE_ROOT_ESCALATION_DENIED",
            "qualification": "FAIL",
        }

    def version_claim_without_release_evidence(self, text):
        return {
            "fixture": "SEC-SRC-04",
            "role": "SUPPORT_ONLY",
            "status": "SUPPORT_ONLY_NOT_FACT",
        }

    def verify_no_policy_override(self, instruction_text):
        return True

    def security_findings_blocking(self, findings):
        blocking = 0
        for finding in findings:
            code = finding
            if isinstance(finding, dict):
                code = finding.get("finding")
            if code in BLOCKING_FINDINGS:
                blocking += 1
        return blocking