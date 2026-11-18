# Threat model and limits

Scope: evidence for consequential discretionary decisions, including introductions, access and publication. The local reference model is educational/research code, not a production enforcement boundary.

| Threat | Local check or demonstration | Remaining production requirement |
|---|---|---|
| Altered basis after signing | Signature and linked digest checks | Independent custody before act |
| Decider signs its own review | Role key and distinct-key checks | Independent enrollment and control investigation |
| Common owner fabricates every role | Explicitly not solved; replacement registry demo | Trusted external registry and independent witnesses |
| Invented timestamps or omitted events | Model ordering only; missing stages unresolved | External timing, completeness and retention controls |
| Review says corrected but state unchanged | Signed effect/observation consistency; local readback | Direct endpoint inspection by independent observer |
| Permission expires or changes | Version, expiry and permission assertion checks | Live authenticated revocation checks and atomic execution |
| Replay of a valid bundle | Case bindings checked | Durable replay prevention and idempotent effect receipts |
| Reviewer orders overbroad action | Scope equality check | Full mandate policy and least-privilege executor |
| Confidential rationale leaks | Synthetic fixtures contain no private material | Redaction, access control, retention and consent |
| Third-party rights block reversal | Proposed hard gate | Qualified conflict review and permitted alternative remedy |
| Review route exists only on paper | No live assurance claim | Reachable channel, response commitment and exercised authority |
| Emergency pause becomes indefinite suppression | Pause supported, not adjudicated | Accountable pause review and notice appropriate to risk |
| Irreversible effect disguised as reversal | Deliberately reversible mock only | Residual harm assessment and truthful remedy wording |

Malformed signatures and contradictory evidence are rejected. Missing evidence is not automatically deception. More cryptography cannot substitute for agreed institutional authority.

Python JSON canonicalization is implementation-specific. Package transitive dependencies and all platform versions are not fully locked by the single direct dependency pin. The manifest records Python, cryptography, source hashes and working-tree state; it does not attest the host. CI is a reproducibility aid, not an independent institutional audit.
