"""FAR research router: deterministic decision contract.

This module is a decision contract, not a control plane. It never admits,
schedules, or executes work, and it never promotes provider output. Output
produced under any route stays candidate until an independent acceptance
officer verifies it. Every WorkOrder defaults to exactly one primary
provider; challengers and method donors are named only when the task class
requires them. The vocabulary is bounded by blueprint r2 section 18 and the
task class catalog in CLASS_ROUTES; this module adds no gates, no policies,
and no authority of its own.
"""

PROVIDER_STATES = {
    "native": {
        "state": "ACTIVE_DEFAULT",
        "reason_base": "FAR_ROUTE_NATIVE_DEFAULT",
    },
    "prime": {
        "state": "CANDIDATE_DISABLED_UNTIL_QUALIFIED",
        "reason": "FAR_BLOCK_PROVIDER_UNQUALIFIED",
        "degrade": "FAR_DEGRADE_NATIVE",
    },
    "longhorizon": {
        "state": "METHOD_DONOR_FIRST",
        "provider_activation": "BLOCKED_UNTIL_FIT_GAP",
    },
    "autoresearchclaw": {
        "state": "DEFAULT_OFF",
        "scope": "science_only",
        "blockers": ("DOCKER_SANDBOX_UNAVAILABLE",),
    },
    "evoagentx": {
        "state": "LAB_ONLY",
        "scope": ("CandidateWorkflow", "CandidateEvolution"),
    },
    "aris": {
        "state": "SELECTED_PINNED_METHOD_PACK",
        "layer": "method_layer_not_manager",
    },
}

REASON_CODES = (
    "FAR_ROUTE_NATIVE_DEFAULT",
    "FAR_ROUTE_NATIVE_ARIS",
    "FAR_ROUTE_PRIME_ACP_RLM",
    "FAR_ROUTE_PRIME_TRAJECTORY",
    "FAR_ROUTE_ARC_SCIENCE",
    "FAR_ROUTE_LONGHORIZON_QUALIFIED",
    "FAR_ROUTE_EVO_LAB",
    "FAR_CHALLENGE_ARIS",
    "FAR_DEGRADE_NATIVE",
    "FAR_BLOCK_PROVIDER_UNQUALIFIED",
    "FAR_BLOCK_REQUIRED_CHALLENGE_UNAVAILABLE",
    "FAR_BLOCK_SANDBOX_UNAVAILABLE",
    "FAR_BLOCK_NETWORK_POLICY",
    "FAR_BLOCK_CREDENTIAL",
    "FAR_ABORT_NO_PROGRESS",
    "FAR_ABORT_BUDGET",
)

PROVIDER_CAPABILITIES = {
    "native": frozenset({
        "research", "git", "web", "docs", "memory", "fts5", "long_horizon",
    }),
    "prime": frozenset({
        "rlm", "recursive", "trajectory", "huge_corpus", "refine_candidate",
    }),
    "longhorizon": frozenset({"verified_state_loop"}),
    "autoresearchclaw": frozenset({
        "science_experiment", "benchmark", "claim_verification",
    }),
    "evoagentx": frozenset({"workflow_autoconstruction_candidate"}),
}

CLASS_ROUTES = {
    "RESEARCH_GENERAL": {
        "decision_rule": "NATIVE",
        "reason": "FAR_ROUTE_NATIVE_DEFAULT",
    },
    "RESEARCH_LITERATURE_REPO": {
        "decision_rule": "NATIVE_WITH_SELECTED_ARIS",
        "reason": "FAR_ROUTE_NATIVE_ARIS",
        "methods": ("research-lit", "novelty-check", "research-review"),
    },
    "RLM_CONTEXT_HEAVY": {
        "decision_rule": (
            "PRIME_IF_QUALIFIED_ELSE_NATIVE_IF_MINIMUM_ELSE_BLOCK"
        ),
        "prime_reason": "FAR_ROUTE_PRIME_ACP_RLM",
        "degrade": "FAR_DEGRADE_NATIVE",
        "block": "FAR_BLOCK_PROVIDER_UNQUALIFIED",
    },
    "RESEARCH_ADVERSARIAL_CHALLENGE": {
        "decision_rule": "ARIS_SELECTED_CHALLENGE",
        "reason": "FAR_CHALLENGE_ARIS",
        "final_acceptance": False,
        "block": "FAR_BLOCK_REQUIRED_CHALLENGE_UNAVAILABLE",
    },
    "RESEARCH_LONG_HORIZON": {
        "decision_rule": "HERMES_LONG_HORIZON_NATIVE",
        "reason": "FAR_ROUTE_NATIVE_DEFAULT",
        "optional_provider": "longhorizon",
        "qualification": "qualified_and_fit_gap_proven",
    },
    "RESEARCH_SCIENTIFIC_EXPERIMENT": {
        "decision_rule": "ARC_IF_QUALIFIED_ELSE_RESEARCH_ONLY",
        "reason": "FAR_ROUTE_ARC_SCIENCE",
        "unqualified_behavior": "RESEARCH_ONLY",
        "no_experiment_result_without_real_run": True,
    },
    "RESEARCH_TRAJECTORY_MINING": {
        "decision_rule": "PRIME_IF_QUALIFIED_ELSE_NATIVE",
        "reason": "FAR_ROUTE_PRIME_TRAJECTORY",
        "degrade": "FAR_DEGRADE_NATIVE",
    },
    "RESEARCH_WORKFLOW_OPTIMIZATION": {
        "decision_rule": "HGK_GOVERNED_EVOLUTION",
        "donors": ("prime_refine", "aris_meta", "evoagentx_lab"),
        "reason": "FAR_ROUTE_EVO_LAB",
    },
    "RESEARCH_FINANCIAL_METHOD": {
        "decision_rule": "NATIVE_WITH_SQS_OWNER_BOUNDARY",
        "mutation_authority": "NONE",
        "route_after": ("sqs-data-analysis", "sqs-risk", "domain_owner"),
        "hard_boundary": "CandidateResearch != Financial Truth",
    },
}


def _network_policy_satisfies(provider_state, req):
    """Return True when the request network requirement is satisfiable."""
    requirement = req.get("network_requirement", "DENY")
    if requirement != "ALLOW":
        return True
    return provider_state.get("network_policy") == "ALLOW"


def _runtime_provider_state(name, req):
    """Build the per-request runtime state for one provider."""
    req = req or {}
    state = {
        "name": name,
        "qualification_state": "ACTIVE",
        "capabilities": set(PROVIDER_CAPABILITIES.get(name, ())),
        "resume_supported": True,
        "sandbox_ready": False,
        "network_policy": "DENY",
        "cost_floor": 0,
    }
    if name == "native":
        state["sandbox_ready"] = True
        state["network_policy"] = "ALLOW"
    elif name == "prime":
        state["sandbox_ready"] = True
        state["network_policy"] = "ALLOW"
    elif name == "autoresearchclaw":
        state["qualification_state"] = (
            "ACTIVE" if req.get("arc_qualified") else "CANDIDATE"
        )
        state["sandbox_ready"] = bool(req.get("arc_sandbox_ready"))
    elif name == "longhorizon":
        state["qualification_state"] = (
            "ACTIVE" if req.get("longhorizon_qualified") else "CANDIDATE"
        )
    elif name == "evoagentx":
        state["qualification_state"] = (
            "ACTIVE" if req.get("evo_qualified") else "CANDIDATE"
        )
    elif name == "aris":
        state["qualification_state"] = (
            "ACTIVE" if req.get("aris_qualified") else "CANDIDATE"
        )
    return state


def eligible(provider_state, req):
    """Return True when a provider satisfies blueprint 18.1 for a request.

    req fields: required_capabilities (list), resume_required (bool),
    sandbox_required (bool), network_requirement (str DENY or ALLOW),
    cost_budget (int), blocking_finding (bool).
    """
    req = req or {}
    if provider_state.get("qualification_state") != "ACTIVE":
        return False
    capabilities = set(provider_state.get("capabilities", ()))
    required = set(req.get("required_capabilities", ()))
    if not required.issubset(capabilities):
        return False
    if req.get("resume_required") and not provider_state.get(
            "resume_supported"):
        return False
    if req.get("sandbox_required") and not provider_state.get("sandbox_ready"):
        return False
    if not _network_policy_satisfies(provider_state, req):
        return False
    if provider_state.get("cost_floor", 0) > req.get("cost_budget", 0):
        return False
    if req.get("blocking_finding"):
        return False
    return True


def _eligible_providers(req):
    """Return the sorted names of providers eligible for this request."""
    return [
        name for name in sorted(PROVIDER_CAPABILITIES)
        if eligible(_runtime_provider_state(name, req), req)
    ]


def route(task_class, req=None):
    """Resolve one task class to a deterministic provider route."""
    req = dict(req or {})
    if task_class not in CLASS_ROUTES:
        raise ValueError("Unknown FAR task class: {0}".format(task_class))
    rule = CLASS_ROUTES[task_class]
    result = {
        "task_class": task_class,
        "decision": rule["decision_rule"],
        "reason_code": rule.get("reason"),
        "primary": None,
        "challenger": None,
        "providers_eligible": _eligible_providers(req),
        "block_reason": None,
        "degrade_note": None,
    }
    if task_class == "RESEARCH_GENERAL":
        result["primary"] = "fabric-autoresearch-native"
        result["reason_code"] = "FAR_ROUTE_NATIVE_DEFAULT"
    elif task_class == "RESEARCH_LITERATURE_REPO":
        result["primary"] = "fabric-autoresearch-native"
        result["methods"] = list(rule["methods"])
        result["reason_code"] = "FAR_ROUTE_NATIVE_ARIS"
        if req.get("challenge_required"):
            result["challenger"] = "aris"
            result["challenger_method"] = "research-review"
    elif task_class == "RLM_CONTEXT_HEAVY":
        if eligible(_runtime_provider_state("prime", req), req):
            result["decision"] = "PRIME"
            result["primary"] = "prime"
            result["reason_code"] = "FAR_ROUTE_PRIME_ACP_RLM"
        elif req.get("native_capability_minimum"):
            result["decision"] = "NATIVE"
            result["primary"] = "fabric-autoresearch-native"
            result["reason_code"] = "FAR_DEGRADE_NATIVE"
            result["degrade_note"] = "FAR_DEGRADE_NATIVE"
        else:
            result["decision"] = "BLOCK"
            result["block_reason"] = "FAR_BLOCK_PROVIDER_UNQUALIFIED"
            result["reason_code"] = "FAR_BLOCK_PROVIDER_UNQUALIFIED"
    elif task_class == "RESEARCH_ADVERSARIAL_CHALLENGE":
        result["challenger"] = "aris"
        result["final_acceptance"] = False
        if eligible(_runtime_provider_state("aris", req), req):
            result["primary"] = "fabric-autoresearch-native"
            result["reason_code"] = "FAR_CHALLENGE_ARIS"
        elif req.get("challenge_required"):
            result["decision"] = "BLOCK"
            result["block_reason"] = "FAR_BLOCK_REQUIRED_CHALLENGE_UNAVAILABLE"
            result["reason_code"] = "FAR_BLOCK_REQUIRED_CHALLENGE_UNAVAILABLE"
        else:
            result["decision"] = "NATIVE_NO_CHALLENGE"
            result["primary"] = "fabric-autoresearch-native"
            result["reason_code"] = "FAR_ROUTE_NATIVE_DEFAULT"
            result["degrade_note"] = "FAR_BLOCK_REQUIRED_CHALLENGE_UNAVAILABLE"
    elif task_class == "RESEARCH_LONG_HORIZON":
        result["primary"] = "fabric-autoresearch-native"
        result["reason_code"] = "FAR_ROUTE_NATIVE_DEFAULT"
        if req.get("fit_gap_proven") and eligible(
                _runtime_provider_state("longhorizon", req), req):
            result["optional_provider"] = "longhorizon"
            result["reason_code"] = "FAR_ROUTE_LONGHORIZON_QUALIFIED"
    elif task_class == "RESEARCH_SCIENTIFIC_EXPERIMENT":
        result["experiment_claim"] = False
        if eligible(_runtime_provider_state("autoresearchclaw", req), req):
            result["decision"] = "ARC_IF_QUALIFIED_ELSE_RESEARCH_ONLY"
            result["primary"] = "autoresearchclaw"
            result["reason_code"] = "FAR_ROUTE_ARC_SCIENCE"
            result["experiment_claim"] = True
        else:
            result["decision"] = "RESEARCH_ONLY"
            result["primary"] = "fabric-autoresearch-native"
            result["reason_code"] = "FAR_ROUTE_ARC_SCIENCE"
            result["degrade_note"] = "NO_EXPERIMENT_RESULT_WITHOUT_REAL_RUN"
    elif task_class == "RESEARCH_TRAJECTORY_MINING":
        if eligible(_runtime_provider_state("prime", req), req):
            result["primary"] = "prime"
            result["reason_code"] = "FAR_ROUTE_PRIME_TRAJECTORY"
        else:
            result["primary"] = "fabric-autoresearch-native"
            result["reason_code"] = "FAR_DEGRADE_NATIVE"
            result["degrade_note"] = "FAR_DEGRADE_NATIVE"
    elif task_class == "RESEARCH_WORKFLOW_OPTIMIZATION":
        result["primary"] = "fabric-autoresearch-native"
        result["donors"] = list(rule["donors"])
        result["reason_code"] = "FAR_ROUTE_EVO_LAB"
    elif task_class == "RESEARCH_FINANCIAL_METHOD":
        result["primary"] = "fabric-autoresearch-native"
        result["mutation_authority"] = "NONE"
        result["route_after"] = list(rule["route_after"])
        result["hard_boundary"] = rule["hard_boundary"]
        result["reason_code"] = "FAR_ROUTE_NATIVE_DEFAULT"
    return result


def route_decision_summary(route_result):
    """Return a compact one-line summary of a route result."""
    parts = [
        str(route_result.get("task_class", "?")),
        str(route_result.get("decision", "?")),
        str(route_result.get("reason_code", "?")),
    ]
    primary = route_result.get("primary")
    if primary:
        parts.append("primary={0}".format(primary))
    challenger = route_result.get("challenger")
    if challenger:
        parts.append("challenger={0}".format(challenger))
    block = route_result.get("block_reason")
    if block:
        parts.append("block={0}".format(block))
    return " | ".join(parts)
