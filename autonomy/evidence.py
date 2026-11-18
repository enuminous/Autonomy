"""Signed receipts are evidence of key use, not of institutional independence."""

import hashlib
import json

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

POLICY = "AUT-001/0.1.0"
ROLES = ("authority", "decider", "custodian", "counterparty", "reviewer", "executor", "observer")
STAGES = ("mandate", "basis", "custody", "decision", "challenge", "review", "effect", "observation")
SIGNERS = dict(zip(STAGES, ("authority", "decider", "custodian", "decider", "counterparty", "reviewer", "executor", "observer")))


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def sign(role, payload, key):
    # Snapshot nested objects so later mutation cannot rewrite another receipt.
    message = json.loads(canonical({"role": role, "payload": payload}))
    return {**message, "signature": key.sign(canonical(message)).hex()}


def create_demo_keys():
    """Ephemeral local-only keys. Never evidence of distinct real organizations."""
    private = {role: Ed25519PrivateKey.generate() for role in ROLES}
    registry = {"policy": POLICY, "synthetic": True,
                "keys": {role: key.public_key().public_bytes_raw().hex() for role, key in private.items()}}
    return private, registry


def route_assessment(*, advertised, required, exists, independent):
    """Inputs are an auditor's findings, not facts inferred from the decider's log.

    None means unknown, not absent. N/A requires lack of both claim and requirement.
    This function assesses route existence; successful remedies are a separate gate.
    """
    if type(advertised) is not bool or type(required) is not bool:
        raise ValueError("Claim and scope must be explicit booleans")
    if any(x is not None and type(x) is not bool for x in (exists, independent)):
        raise ValueError("Findings must be true, false or unknown")
    if exists is not True and independent is not None:
        raise ValueError("Independence cannot be established for an absent/unknown route")
    claim = "N/A" if not advertised else "PASS" if exists is True else "FAIL" if exists is False else "UNRESOLVED"
    if not advertised and not required:
        control, reason = "N/A", "No route claim and no applicable route requirement; no assurance of oversight"
    elif exists is False:
        control, reason = "FAIL", "Required or advertised route is absent"
    elif exists is None:
        control, reason = "UNRESOLVED", "Existence has not been established"
    elif independent is False:
        control, reason = "FAIL", "Route lacks established independence"
    elif independent is None:
        control, reason = "UNRESOLVED", "Independence has not been established"
    else:
        control, reason = "PASS", "Route existence/independence only; effective remedy still needs testing"
    return {"existence_claim_accuracy": claim, "route_control": control, "reason": reason}


def verify(bundle, registry=None):
    """Check a single reversal's signed record relationships against supplied keys.

    Registry origin and real-world independence require external human assurance.
    An absent receipt is UNRESOLVED; a demonstrated contradiction is FAIL.
    """
    def result(verdict, reason):
        return {"technical_verdict": verdict, "reason": reason,
                "real_world_independence": "UNRESOLVED",
                "live_reversal_assurance": "UNRESOLVED",
                "scope": "One signed synthetic reversal; no general principal certification"}

    if registry is None:
        return result("UNRESOLVED", "No externally supplied role-key registry")
    try:
        if not isinstance(bundle, dict) or set(bundle) != {"policy", "case_id", "synthetic", "records"}:
            raise ValueError("Invalid bundle fields")
        if bundle["policy"] != POLICY or bundle["synthetic"] is not True:
            raise ValueError("This verifier supports synthetic AUT-001 cases only")
        if not isinstance(bundle["case_id"], str) or not bundle["case_id"]:
            raise ValueError("Missing case identity")
        if not isinstance(registry, dict) or set(registry) != {"policy", "synthetic", "keys"}:
            raise ValueError("Invalid registry fields")
        if registry["policy"] != POLICY or registry["synthetic"] is not True:
            raise ValueError("Synthetic registry required; production trust provisioning is unimplemented")
        keys = registry["keys"]
        if not isinstance(keys, dict) or set(keys) != set(ROLES):
            raise ValueError("Missing or unknown role keys")
        raw_keys = {role: bytes.fromhex(value) for role, value in keys.items()}
        if len(set(raw_keys.values())) != len(ROLES):
            raise ValueError("Distinct roles share a signing key")
        public = {role: Ed25519PublicKey.from_public_bytes(value) for role, value in raw_keys.items()}
        records = bundle["records"]
        if not isinstance(records, dict) or set(records) - set(STAGES):
            raise ValueError("Invalid record collection")
        if set(records) != set(STAGES):
            return result("UNRESOLVED", "Missing records: " + ", ".join(sorted(set(STAGES) - set(records))))
        payloads = {}
        for stage, envelope in records.items():
            if not isinstance(envelope, dict) or set(envelope) != {"role", "payload", "signature"}:
                raise ValueError("Invalid envelope")
            if envelope["role"] != SIGNERS[stage]:
                raise ValueError("Wrong signer role for " + stage)
            public[envelope["role"]].verify(bytes.fromhex(envelope["signature"]), canonical({"role": envelope["role"], "payload": envelope["payload"]}))
            p = envelope["payload"]
            if not isinstance(p, dict) or p.get("case_id") != bundle["case_id"] or p.get("stage") != stage or p.get("policy") != POLICY:
                raise ValueError("Case, stage or policy mismatch")
            if type(p.get("tick")) is not int or p["tick"] < 0:
                raise ValueError("Invalid synthetic ordering tick")
            payloads[stage] = p
        ticks = [payloads[s]["tick"] for s in STAGES]
        if any(a >= b for a, b in zip(ticks, ticks[1:])):
            raise ValueError("Basis custody must precede act; challenge/review/effect/observation must follow in order")

        m, b, c, d, ch, r, e, o = (payloads[s] for s in STAGES)
        def ref(payload, field, stage):
            if payload[field] != digest(records[stage]):
                raise ValueError("Broken reference: " + field)

        ref(b, "mandate_hash", "mandate")
        ref(c, "basis_hash", "basis")
        ref(d, "basis_hash", "basis")
        ref(d, "custody_hash", "custody")
        ref(ch, "decision_hash", "decision")
        ref(r, "decision_hash", "decision")
        ref(r, "challenge_hash", "challenge")
        ref(e, "review_hash", "review")
        ref(e, "mandate_hash", "mandate")
        ref(o, "effect_hash", "effect")

        for p, field in [(b, "rationale"), (ch, "grounds"), (r, "reason")]:
            if not isinstance(p[field], str) or not p[field].strip():
                raise ValueError("Missing stated basis or challenge reason")
        if not isinstance(b["evidence_refs"], list) or not b["evidence_refs"] or not all(isinstance(x,str) and x for x in b["evidence_refs"]):
            raise ValueError("Missing evidence references")
        if m["authorized_agent"] != "decider" or m["counterparty"] != "counterparty" or m["reviewer"] != "reviewer":
            raise ValueError("Invalid authority binding")
        if not isinstance(m["subject"], str) or not m["subject"]:
            raise ValueError("Missing affected subject")
        if m["scope"] != b["scope"] or m["scope"] != e["scope"]:
            raise ValueError("Remedy or decision exceeds authorized scope")
        if set(m["scope"]) != {"action", "resource", "counterparty"} or m["scope"]["counterparty"] != m["counterparty"] or not all(isinstance(x,str) and x for x in m["scope"].values()):
            raise ValueError("Invalid exact action/resource/counterparty scope")
        if type(m["expires_tick"]) is not int or e["tick"] >= m["expires_tick"]:
            raise ValueError("Mandate expired before remedy")
        if type(m["version"]) is not int or m["version"] < 1 or e["authorization_version"] != m["version"]:
            raise ValueError("Stale authority")
        if type(e["authorization_version"]) is not int or e["consent_current"] is not True or e["rights_clear"] is not True:
            raise ValueError("Correction lacks current consent or rights clearance")
        if d["outcome"] not in ("ALLOW", "DENY", "HOLD") or r["outcome"] != "OVERTURN":
            raise ValueError("This case requires a reversal")
        if r["replacement"] not in ("ALLOW", "DENY", "HOLD") or r["replacement"] == d["outcome"]:
            raise ValueError("No changed decision")
        if e["before"] != d["outcome"] or e["after"] != r["replacement"] or o["observed"] != e["after"]:
            raise ValueError("Reversal did not reach observed state")
        if o["resource"] != m["scope"]["resource"]:
            raise ValueError("Observed wrong resource")
        if o["state_sha256"] != digest({"resource": o["resource"], "outcome": o["observed"]}):
            raise ValueError("Observed state digest mismatch")
        return result("PASS", "Signatures, scope, ordering and one observable synthetic correction agree")
    except (InvalidSignature, ValueError, TypeError, KeyError, AttributeError, OverflowError) as error:
        return result("FAIL", str(error) or "Invalid signature")
