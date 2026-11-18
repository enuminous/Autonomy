"""Proposed hard gates. Confidence never compensates for absent authorization."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Request:
    action: str
    resource: str
    counterparty: str
    authority_current: bool | None
    rights_clear: bool | None
    evidence_ready: bool | None
    review_required: bool
    review_route_verified: bool | None
    operator_paused: bool = False


def decide(request):
    if not isinstance(request, Request):
        raise ValueError("Typed request required")
    if not all(isinstance(x, str) and x for x in (request.action, request.resource, request.counterparty)):
        raise ValueError("Exact scope required")
    if type(request.review_required) is not bool or type(request.operator_paused) is not bool:
        raise ValueError("Explicit review/pause flags required")
    values = (request.authority_current, request.rights_clear, request.evidence_ready, request.review_route_verified)
    if any(x is not None and type(x) is not bool for x in values):
        raise ValueError("Evidence findings must be true, false or unknown")
    if request.operator_paused:
        return {"decision": "HOLD", "reason": "accountable_operator_pause"}
    if request.authority_current is False:
        return {"decision": "DENY", "reason": "authorization_absent_or_revoked"}
    if request.rights_clear is False:
        return {"decision": "DENY", "reason": "rights_conflict"}
    if request.authority_current is None or request.rights_clear is None:
        return {"decision": "HOLD", "reason": "authority_or_rights_unresolved"}
    if request.review_required and request.review_route_verified is not True:
        return {"decision": "HOLD", "reason": "required_review_route_unverified"}
    if request.evidence_ready is not True:
        return {"decision": "HOLD", "reason": "evidence_not_released"}
    return {"decision": "ELIGIBLE", "reason": "within_scope_discretion_remains"}
