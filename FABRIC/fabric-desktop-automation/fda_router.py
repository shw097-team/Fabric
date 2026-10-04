from dataclasses import dataclass
from typing import Literal

Provider = Literal['CUA', 'UFO2', 'HITL', 'BLOCKED']


@dataclass(frozen=True)
class Request:
    app: str
    app_version: str
    action_class: str
    risk_class: str
    requires_secret: bool
    financial_side_effect: bool
    active_position_policy_mutation: bool


def route(req: Request, matrix: dict) -> Provider:
    if req.requires_secret:
        return 'HITL'
    if req.financial_side_effect:
        return 'HITL'
    if req.active_position_policy_mutation:
        return 'BLOCKED'
    key = (req.app, req.app_version, req.action_class)
    certified = matrix.get(key, {})
    if certified.get('cua') == 'PASS':
        return 'CUA'
    if certified.get('ufo2') == 'PASS':
        return 'UFO2'
    return 'BLOCKED'


def failover(primary: Provider, outcome: str, alternate_certified: bool) -> Provider:
    if outcome == 'PASS':
        return primary
    if outcome not in ('DETECTED_FAIL', 'SAFE_HALT'):
        return 'BLOCKED'
    if not alternate_certified:
        return 'BLOCKED'
    return 'UFO2' if primary == 'CUA' else 'CUA'