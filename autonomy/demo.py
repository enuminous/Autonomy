"""Local reversible access decision; no real introductions or external actions."""

import json
from pathlib import Path
from .evidence import POLICY, create_demo_keys, digest, sign, verify


def build_case(directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    keys, registry = create_demo_keys()
    records = {}
    case_id = "AUT-001-synthetic-001"
    scope = {"action": "read", "resource": "public-synthetic-note", "counterparty": "counterparty"}

    def add(stage, role, tick, **fields):
        records[stage] = sign(role, {"policy": POLICY, "case_id": case_id, "stage": stage, "tick": tick, **fields}, keys[role])
        return digest(records[stage])

    mandate = add("mandate", "authority", 0, authorized_agent="decider", subject="synthetic-owner",
                  counterparty="counterparty", reviewer="reviewer", scope=scope, version=1, expires_tick=100)
    basis = add("basis", "decider", 1, mandate_hash=mandate, scope=scope,
                rationale="Deny access because the synthetic note is thought to remain under review.",
                evidence_refs=["fixture:stale-status-record"])
    custody = add("custody", "custodian", 2, basis_hash=basis)
    decision = add("decision", "decider", 3, basis_hash=basis, custody_hash=custody, outcome="DENY")
    state_path = directory / "mock-resource-state.json"
    state_path.write_text(json.dumps({"resource": scope["resource"], "outcome": "DENY"}))
    challenge = add("challenge", "counterparty", 4, decision_hash=decision,
                    grounds="Synthetic release receipt predates this denial; request authorized independent review.")
    review = add("review", "reviewer", 5, decision_hash=decision, challenge_hash=challenge,
                 outcome="OVERTURN", replacement="ALLOW", reason="The pre-existing synthetic release receipt resolves the stale-status error.")
    before = json.loads(state_path.read_text())["outcome"]
    state_path.write_text(json.dumps({"resource": scope["resource"], "outcome": "ALLOW"}))
    effect = add("effect", "executor", 6, review_hash=review, mandate_hash=mandate, scope=scope,
                 before=before, after="ALLOW", authorization_version=1, consent_current=True, rights_clear=True)
    observed = json.loads(state_path.read_text())
    add("observation", "observer", 7, effect_hash=effect, resource=observed["resource"],
        observed=observed["outcome"], state_sha256=digest(observed))
    bundle = {"policy": POLICY, "case_id": case_id, "synthetic": True, "records": records}
    for stage, envelope in records.items():
        custody_dir = directory / "records" / envelope["role"]
        custody_dir.mkdir(parents=True, exist_ok=True)
        (custody_dir / (stage + ".json")).write_text(json.dumps(envelope, indent=2) + "\n")
    for filename, data in [("bundle.json", bundle), ("demo-registry.json", registry), ("verification.json", verify(bundle, registry))]:
        (directory / filename).write_text(json.dumps(data, indent=2) + "\n")
    return bundle, registry, keys
